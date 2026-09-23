"""R14 가 **열어 둔 채로** 종결된 셋을 닫는다 — 리뷰어 §7 의 답 2·3·4.

| 항목 | 리뷰어가 요구한 것 | 여기서 고정하는 계약 |
|---|---|---|
| U18-05 | 기본은 **단일 commit**. 이번 혼재는 두 full commit 과 코드 동등성 검토 범위를 고정한 **이전 예외로 기록** | `blocked_by.bundle_commits` · 예외는 `reviews/PROMOTION_DECISIONS.json` 의 **정확한 commit 집합**에만 걸린다 |
| `legacy_transition_approved` | 포괄 `--accept-uncomparable` 로 rc 0 을 만들지 말고 **별도 판정**을 남긴다. `promotion_eligible: false` 를 지우지 않는다 | 판정 키 둘(`legacy_transition_approved` · `legacy_transition`) · rc 4 그대로 · 승격은 여전히 false |
| 기록용 CLI 인자 | 인자 생략을 **오류**로. 기본 out 진단을 남기면 **별도 명시 모드**로 가른다 | `provenance.py <art>` 는 rc 2 · `--default-out-diagnostic` 만 옛 기본값 |

셋 다 **고치기 전에 실패를 봤다.** RED 관측은 `WORKING_STATE.md` 의 R15 절에 적는다.

⚠ 이 시험들은 정본 `out/` 의 bytes 를 **읽기만** 한다. 합성은 전부 `tmp_path` 안이다.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

ROOT = pathlib.Path(__file__).resolve().parents[1]
CHECK = ROOT / "scripts" / "check_u14.py"
DECISIONS = ROOT / "reviews" / "PROMOTION_DECISIONS.json"

#: U18-05 의 두 full commit — 정본 `out/` 의 13 산출이 실제로 나뉘어 있는 자리다 (9 + 4).
C_MAIN = "066866595ab71827ef2d98e7a6cf26136df21495"
C_REPUB = "419c1abaeec9fa981d7f5829d5803167288f7f1e"
#: 어느 실행에도 속하지 않는 40-hex — 예외가 **넓어지지 않는다**는 것을 재는 대조군
C_ALIEN = "0" * 39 + "1"


def _run_check(*argv: str) -> tuple[int, dict, str]:
    """`check_u14.py` 를 돌리고 (rc, PROMOTION dict, 전체 출력) 을 준다."""
    r = subprocess.run([sys.executable, str(CHECK), *argv], cwd=ROOT,
                       capture_output=True, text=True, timeout=600)
    out = r.stdout + r.stderr
    verdict: dict = {}
    for line in out.splitlines():
        if line.startswith("PROMOTION "):
            verdict = json.loads(line[len("PROMOTION "):])
    assert verdict, ("PROMOTION 줄이 없다 — 판정을 못 읽는다", r.returncode, out[-1200:])
    return r.returncode, verdict, out


def _bundle(tmp_path: pathlib.Path, spec: dict[str, str | None]) -> pathlib.Path:
    """정본 산출을 복사해 후보 묶음을 만든다. `spec` = {산출 이름: 덮어쓸 git commit (None 이면 그대로)}.

    본문 bytes 와 sha256·receipt 는 건드리지 않는다 — 움직이는 것은 sidecar 의 커밋 좌표뿐이다.
    """
    d = tmp_path / "cand"
    d.mkdir(parents=True, exist_ok=True)
    for name, commit in spec.items():
        src = ROOT / "out" / name
        if not src.is_file():
            pytest.skip(f"{name} 이 정본에 없다")
        (d / name).write_bytes(src.read_bytes())
        meta = json.loads(src.with_name(name + ".meta.json").read_text(encoding="utf-8"))
        if commit is not None:
            meta["git_commit_at_start"] = commit
            meta["git_commit"] = commit
        (d / (name + ".meta.json")).write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
    return d


# ── U18-05 — 묶음의 commit 혼재 ──────────────────────────────────────────────────────────────

def test_the_decisions_file_exists_and_pins_full_commits():
    """예외 원장 자체가 **자기완결**이어야 한다 — 40-hex full commit 과 코드 동등성 검토 범위를 담는다.

    리뷰어 답 3: "일반 허용 규칙으로 승격하지 말고 두 full commit 과 코드 동등성 검토 범위를 고정한
    이전 예외로 기록한다." 짧은 sha·와일드카드·빈 목록은 예외를 **넓힌다** — 그래서 형식부터 막는다.
    """
    assert DECISIONS.is_file(), f"{DECISIONS} 가 없다 — 예외를 기록할 자리가 없다"
    doc = json.loads(DECISIONS.read_text(encoding="utf-8"))
    ex = doc["bundle_commit_exceptions"]
    assert ex, "예외 목록이 비었다"
    for e in ex:
        assert set(e) >= {"id", "commits", "artifacts", "code_equivalence", "approved_utc",
                          "approved_by", "scope"}, e
        assert len(e["commits"]) >= 2 and len(set(e["commits"])) == len(e["commits"]), e
        for c in e["commits"]:
            assert isinstance(c, str) and len(c) == 40 and all(ch in "0123456789abcdef" for ch in c), c
        assert e["artifacts"], e
        assert e["code_equivalence"].get("command") and "result" in e["code_equivalence"], e


def test_a_mixed_commit_bundle_that_no_record_covers_is_refused(tmp_path):
    """[U18-05] 두 산출이 **서로 다른 커밋**에서 나왔는데 게이트가 아무 말도 안 했다.

    `check_u14` 는 sidecar 마다 `git_commit_at_start` 를 형식으로만 봤고(40-hex 인가),
    **묶음 전체가 한 코드 상태에서 나왔는가**는 아무도 안 봤다. 우리는 이번 실제 혼재를
    `git diff --name-only A B -- '*.py' '*.sh'` = 0 으로 손수 확인했지만 게이트가 그것을
    강제하지 않는다 — 리뷰어가 지적한 그대로 `.m`·설정·의존성은 그 diff 가 안 덮는다.
    """
    d = _bundle(tmp_path, {"matrix_100.csv": C_MAIN, "matrix_200.csv": C_ALIEN})
    rc, v, out = _run_check("--new", str(d), "--schema-only")
    assert v["blocked_by"]["bundle_commits"] >= 1, ("혼재를 안 세었다", v["blocked_by"], out[-900:])
    assert rc == 2, ("혼재한 묶음이 통과했다", rc, out[-900:])
    assert v.get("bundle_commit_exception") is None, v.get("bundle_commit_exception")
    assert C_ALIEN[:12] in out and C_MAIN[:12] in out, ("어느 두 커밋인지 안 말한다", out[-900:])


def test_a_single_commit_bundle_is_not_flagged(tmp_path):
    """대조군 — 한 커밋에서 나온 묶음은 이 축으로 막히지 않는다 (검사가 늘 켜지면 신호가 죽는다)."""
    d = _bundle(tmp_path, {"matrix_100.csv": C_MAIN, "matrix_200.csv": C_MAIN})
    rc, v, out = _run_check("--new", str(d), "--schema-only")
    assert v["blocked_by"]["bundle_commits"] == 0, (v["blocked_by"], out[-900:])
    assert rc == 0, (rc, out[-900:])


def test_the_recorded_exception_covers_exactly_its_two_commits(tmp_path):
    """예외는 **그 두 커밋**에만 걸린다 — 하나라도 다르면 여전히 거부다.

    `{C_MAIN, C_REPUB}` 는 기록된 집합이므로 통과하고, `{C_MAIN, C_ALIEN}` 은 아니다.
    셋이 섞이면(기록된 둘 + 낯선 하나) 집합이 달라지므로 역시 거부다 — 예외가 **부분집합으로
    번지지 않는다**는 뜻이다.
    """
    ok = _bundle(tmp_path / "a", {"matrix_100.csv": C_MAIN, "matrix_300_0147.csv": C_REPUB})
    rc, v, out = _run_check("--new", str(ok), "--schema-only")
    assert v["blocked_by"]["bundle_commits"] == 0, ("기록된 예외가 안 걸렸다", v["blocked_by"], out[-900:])
    assert v.get("bundle_commit_exception"), ("예외 id 를 안 적는다", v, out[-900:])
    assert rc == 0, (rc, out[-900:])

    three = _bundle(tmp_path / "b", {"matrix_100.csv": C_MAIN, "matrix_200.csv": C_ALIEN,
                                     "matrix_300_0147.csv": C_REPUB})
    rc, v, out = _run_check("--new", str(three), "--schema-only")
    assert v["blocked_by"]["bundle_commits"] >= 1, ("낯선 커밋이 섞였는데 예외가 덮었다", v["blocked_by"])
    assert rc == 2 and v.get("bundle_commit_exception") is None, (rc, v.get("bundle_commit_exception"))


def test_the_canonical_bundle_is_the_recorded_exception():
    """정본 `out/` 은 실제로 9 + 4 혼재다 — 기록된 예외가 그것을 이름으로 덮는다.

    이 시험이 R14 §7-3 의 "이전 예외로 기록한다" 를 실물로 고정한다. 예외를 지우면 정본이
    rc 2 로 떨어져 **아무도 모르게 넘어가지 않는다**.
    """
    rc, v, out = _run_check("--new", "out", "--schema-only")
    assert v["blocked_by"]["bundle_commits"] == 0, (v["blocked_by"], out[-900:])
    assert v.get("bundle_commit_exception") == "U18-05", (v.get("bundle_commit_exception"), out[-900:])
    assert rc == 0, (rc, out[-900:])


# ── legacy_transition_approved — 별도 판정 ───────────────────────────────────────────────────

def test_a_legacy_transition_is_a_separate_verdict_that_does_not_promote():
    """[리뷰어 §7-2] 옛 정본과의 대조는 rc 4 이고 **승격은 여전히 false** 여야 한다.

    포괄 `--accept-uncomparable` 로 rc 0 을 만들면 그 줄만 인용된다. 대신 별도 판정을 남긴다 —
    old/new 묶음 식별 · 대상 코드 · 검사 결과 · 허용된 unknown 사유 · 승인 기록을 담은 것.
    """
    rc, v, out = _run_check("--new", "out", "--old-rev", "42314198")
    assert rc == 4, ("옛 baseline 대조는 rc 4 다", rc, out[-900:])
    assert v["promotion_eligible"] is False, ("승격 자격이 생겼다 — 판정을 지운 것이다", v)
    b = v["blocked_by"]
    assert b["inputs_uncomparable"] > 0 and b["env_uncomparable"] > 0, b
    assert all(b[k] == 0 for k in ("schema", "content", "unit", "controls", "env", "numbers",
                                   "alias", "provenance", "inputs", "stale")), b

    # ⚠ R16 (2026-09-16) — 이 승인은 **더 이상 소비되지 않는다.** `openpyxl` 을 env 축에 더하면서 새 unknown
    #   사유(`env_contract_legacy`)가 생겼는데, `U18B-2026-09-14` 기록은 스스로 "이 승인은 **unknown 사유
    #   둘**만 덮는다" 고 적어 두었다. 셋째를 그 기록에 몰래 끼워 넣는 것은 **기록된 사용자 결정을 고쳐 쓰는
    #   일**이라 하지 않았다 — 승인은 fail-closed 로 사라진다.
    #
    #   승인은 fail-closed 로 사라졌고, 사용자가 **새 기록**(`U18B-R16-2026-09-16`, 축 셋을 명시)을 승인해
    #   되살렸다. 옛 기록은 **그대로 둔다** — 그것이 무엇을 승인했는지는 그때의 사실이다.
    assert b["env_contract_legacy"] > 0, ("정본은 openpyxl 이전 세대다 — 그 사실이 세어져야 한다", b)
    assert v.get("legacy_transition_approved") is True, ("승인 기록이 소비되지 않았다", v, out[-1200:])
    assert v.get("legacy_transition") == "U18B-R16-2026-09-16", (
        "셋째 축까지 명시한 새 기록이 소비돼야 한다 — 옛 기록은 스스로 '둘만' 이라고 적었다", v)


def test_an_unapproved_comparison_is_not_a_legacy_transition(tmp_path):
    """승인 기록이 없는 대조는 `legacy_transition_approved: false` — 부재는 안전값이 아니다."""
    d = _bundle(tmp_path, {"matrix_100.csv": None})
    rc, v, out = _run_check("--new", str(d), "--schema-only")
    assert v.get("legacy_transition_approved") is False, (v, out[-900:])
    assert v.get("legacy_transition") is None, v


def test_an_approval_never_covers_a_real_contract_violation(tmp_path):
    """승인은 **unknown 사유**만 덮는다 — 계약이 깨진 대조는 절대 승인되지 않는다 (fail-closed).

    승인 기록이 있는 묶음의 sidecar 에서 `env` 를 깎으면 그것은 새 산출의 위반이다 (R14 P2-2).
    그 상태에서 `legacy_transition_approved` 가 true 면 승인이 위반을 덮은 것이다.
    """
    d = _bundle(tmp_path, {"matrix_100.csv": None})
    name = "matrix_100.csv"
    meta = json.loads((d / (name + ".meta.json")).read_text(encoding="utf-8"))
    meta["env"] = {"python": (meta.get("env") or {}).get("python", "3.11")}
    (d / (name + ".meta.json")).write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
    rc, v, out = _run_check("--new", str(d), "--schema-only")
    assert rc == 2, (rc, out[-900:])
    assert v.get("legacy_transition_approved") is False, ("위반을 승인이 덮었다", v, out[-900:])


# ── 기록용 CLI 의 산출 root 인자 ──────────────────────────────────────────────────────────────

def _prov_cli(*argv: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(ROOT / "scripts/provenance.py"), *argv],
                          cwd=ROOT, capture_output=True, text=True, timeout=180)


def test_the_record_cli_refuses_an_omitted_output_root(tmp_path):
    """[리뷰어 §7-4] 기록용 CLI 가 산출 root 를 **말없이 `out` 으로** 가정했다.

    U18-02 가 실측한 고장이 정확히 그것이다 — `OUT=out_u18` 실행의 시작 provenance 가 기본값으로
    답해 13 산출 중 11 개가 `git_state_changed_during_run: true` 였다. 인자를 고쳐 부르는 쪽은
    고쳤지만 **CLI 자신은 여전히 침묵으로 기본값을 쓴다.** 생략은 오류여야 한다.
    """
    art = tmp_path / "matrix_100.csv"
    art.write_text("a,b\n1,2\n", encoding="utf-8")
    r = _prov_cli(str(art))
    assert r.returncode != 0, ("산출 root 없이도 답했다", r.returncode, r.stdout[-400:])
    assert "root" in (r.stdout + r.stderr), (r.stdout + r.stderr)[-400:]


def test_an_empty_output_root_is_not_an_output_root(tmp_path):
    """`OUT` 이 안 잡힌 쉘에서 `"$OUT"` 은 빈 문자열이다 — 그것은 root 를 준 것이 아니다."""
    art = tmp_path / "matrix_100.csv"
    art.write_text("a,b\n1,2\n", encoding="utf-8")
    r = _prov_cli(str(art), "")
    assert r.returncode != 0, ("빈 문자열이 root 로 통했다", r.returncode, r.stdout[-400:])


def test_the_explicit_default_out_mode_is_a_separate_flag(tmp_path):
    """호환을 위한 기본 out 진단은 **명시 모드**로만 남는다 (리뷰어: "별도 명시 모드로 구분")."""
    art = tmp_path / "matrix_100.csv"
    art.write_text("a,b\n1,2\n", encoding="utf-8")
    r = _prov_cli("--default-out-diagnostic", str(art))
    assert r.returncode == 0, (r.returncode, (r.stdout + r.stderr)[-400:])
    pv = json.loads(r.stdout)
    assert "git_commit" in pv, pv
    assert pv.get("output_roots_mode") == "default-out-diagnostic", pv


def test_an_explicit_root_still_answers(tmp_path):
    """대조군 — root 를 명시하면 예전처럼 답한다 (production 경로가 이것이다)."""
    art = tmp_path / "matrix_100.csv"
    art.write_text("a,b\n1,2\n", encoding="utf-8")
    r = _prov_cli(str(art), "out_r15")
    assert r.returncode == 0, (r.returncode, (r.stdout + r.stderr)[-400:])
    pv = json.loads(r.stdout)
    assert "git_commit" in pv and "git_dirty" in pv, pv


def test_the_other_subcommands_are_untouched(tmp_path):
    """`--verify-unit` · `--check-run-id` 는 산출 root 를 묻는 기록 모드가 아니다 — 계약을 안 바꾼다."""
    art = tmp_path / "matrix_100.csv"
    art.write_text("a,b\n1,2\n", encoding="utf-8")
    for argv in ((("--verify-unit", str(art))), (("--check-run-id", str(art), "rid"))):
        r = _prov_cli(*argv)
        assert r.returncode in (0, 1), (argv, r.returncode, (r.stdout + r.stderr)[-300:])
        assert "root" not in r.stdout, (argv, r.stdout[-300:])


def test_production_shares_one_explicit_output_root():
    """시작·끝이 **같은 명시 설정**을 공유한다 — `run_states.sh` 가 기본값에 기대지 않는다."""
    src = (ROOT / "scripts" / "run_states.sh").read_text(encoding="utf-8")
    assert "scripts/provenance.py" in src
    for line in src.splitlines():
        if "scripts/provenance.py" in line and "--verify-unit" not in line and "--check-run-id" not in line:
            assert '"$OUT"' in line, ("기록용 호출이 명시 root 를 안 넘긴다", line.strip())


# ── 브랜치 이름이 살아 있는 곳은 요청문만이 아니다 (2026-09-15 실측) ─────────────────────────

def _owner_branch() -> str:
    """루트 `CLAUDE.md` 의 브랜치 표가 정본이다 — 이름을 옮겨 적지 않는다."""
    import re

    claude_md = ROOT.parent / "CLAUDE.md"
    if not claude_md.is_file():
        pytest.skip("루트 CLAUDE.md 가 없다 — 정본을 읽을 수 없다")
    for line in claude_md.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*\|\s*`(claude/[^`]+)`\s*\|([^|]*)\|", line)
        if m and "bms-balancing/" in m.group(2):
            return m.group(1)
    pytest.fail("CLAUDE.md 브랜치 표에서 bms-balancing/ 소유 브랜치를 못 찾았다")


def test_no_script_tells_the_operator_to_push_to_a_retired_branch():
    """★ 2026-09-15 실측 — `preserve_handoff.sh` 가 마지막에 찍는 안내가
    **흡수된 서브 브랜치**로 push 하라고 말하고 있었다.

    사용자가 `physical600_b` 원문을 보존하고 그 안내를 그대로 따랐다면, 본진이
    흡수해 새 커밋을 얹지 않기로 한 브랜치(루트 `CLAUDE.md` 하드룰 1)에 1 GB 짜리
    묶음의 보존 커밋이 올라갔을 것이다. 요청문 쪽은
    `test_review_request_clones_the_branch_that_owns_bms_balancing` 이 막고 있었고
    **스크립트 쪽은 아무도 안 봤다** — 2026-08-20 에 여덟 곳이 대체된 이름을 붙들고
    있던 것과 같은 형태다.

    사람이 그대로 복사해 치는 줄이므로, 이름은 **정본 하나**에서만 온다.
    """
    import re

    owner = _owner_branch()
    bad = []
    for path in sorted(ROOT.glob("scripts/*.sh")) + sorted(ROOT.glob("scripts/*.py")):
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for br in re.findall(r"claude/[A-Za-z0-9._/-]+", line):
                if br != owner:
                    bad.append(f"{path.name}:{n}: {br}")
    assert not bad, (
        f"스크립트가 소유 브랜치(`{owner}`)가 아닌 이름을 찍는다:\n  " + "\n  ".join(bad))


def test_the_printed_recheck_block_says_where_to_stand():
    """★ 2026-09-15 실측 — 스크립트가 찍는 재대조 블록이 **저장소 루트 기준** 경로를
    쓰는데, 그 명령을 찍는 자리는 `bms-balancing/` 안이다.

    사용자가 그대로 복사해 쳤더니 `FileNotFoundError: 'bms-balancing/reviews/…'` 였다.
    안내문은 사람이 **그대로 붙여 넣는** 것이므로, 어디에 서 있어야 하는지를 스스로
    말해야 한다. 앞의 git 명령 셋은 이 디렉터리 기준이라 옳고, python 블록만 루트다 —
    그래서 블록 **앞에** 루트로 옮기는 줄이 있어야 한다.

    같은 함정이 브랜치 이름에서도 났다(위 시험). 안내문은 코드와 같은 규율로 본다.
    """
    src = (ROOT / "scripts" / "preserve_handoff.sh").read_text(encoding="utf-8")
    assert "${PREFIX}${DEST}" in src, "재대조 블록의 루트 기준 경로가 사라졌다 — 시험을 고칠 것"
    head = src.partition("${PREFIX}${DEST}")[0]
    # 루트로 옮기는 줄은 `git push` 안내(이 디렉터리 기준)와 루트 기준 경로 **사이**에 있어야
    # 한다 — 앞에 두면 그 위의 git 명령 셋이 깨진다.
    assert "git rev-parse --show-toplevel" in head, (
        "루트 기준 경로를 쓰는 블록인데 어디에 서야 하는지 말하지 않는다 — "
        "복사해 치면 FileNotFoundError 다")
    assert head.index("git rev-parse --show-toplevel") > head.rindex("git push -u origin"), (
        "루트로 옮기는 줄이 git push 안내보다 앞이다 — 그러면 그 세 줄이 깨진다")


def test_the_manifest_search_finds_both_bundle_conventions(tmp_path):
    """★ 2026-09-15 실측 — `desktop_postproc` 묶음의 manifest 는 이름이 `manifest.json` 인데
    스크립트는 `package_manifest.json` 만 찾았다.

    ZIP 의 크기·SHA 는 전달값과 정확히 일치했는데도 4 단계에서 "전달값을 가진 manifest 가
    ZIP 안에 없다" 로 멈췄다. 실제로는 있었다 — 그 ZIP 안의 `manifest.json` 해시가 바로
    전달값 `134ceb89…` 이고, 스크립트가 찾은 것은 **재사용 증거로 딸려 온 이전 묶음의**
    `package_manifest.json`(`7945b6a7…`) 하나뿐이었다.

    멈춘 것 자체는 옳다 (엉뚱한 manifest 로 보존하면 무엇을 대조한 것인지 알 수 없다).
    고칠 것은 **후보 집합**이다. `--expect-manifest-sha` 가 해시로 고르므로 이름을 넓혀도
    fail-closed 는 그대로다.

    스크립트의 `find` 표현식을 그대로 꺼내 임시 트리에서 돌린다 — 소스에 그 이름이
    적혀 있는지가 아니라 **실제로 찾는지**를 잰다.
    """
    import re
    import subprocess

    src = (ROOT / "scripts" / "preserve_handoff.sh").read_text(encoding="utf-8")
    m = re.search(r'ALL_MAN="\$\(find "\$TMP" (.+?) -type f \| sort\)"', src)
    assert m, "manifest 후보를 찾는 줄의 모양이 바뀌었다 — 시험을 고칠 것"
    expr = m.group(1)

    (tmp_path / "outputs" / "desktop").mkdir(parents=True)
    (tmp_path / "manifest.json").write_text("{}", encoding="utf-8")
    (tmp_path / "outputs" / "desktop" / "package_manifest.json").write_text("{}", encoding="utf-8")
    (tmp_path / "outputs" / "desktop" / "normal_raw_csv_manifest.json").write_text("{}", encoding="utf-8")

    r = subprocess.run(["bash", "-c", f'find "$1" {expr} -type f | sort', "_", str(tmp_path)],
                       capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr[-400:]
    found = {pathlib.Path(x).name for x in r.stdout.split()}
    assert found >= {"manifest.json", "package_manifest.json"}, (
        "두 묶음 규약 중 하나만 찾는다 — desktop_postproc 이 여기서 멈췄다", sorted(found))
    assert "normal_raw_csv_manifest.json" not in found, (
        "이름에 manifest 가 들어간 것을 전부 후보로 삼으면 골라야 할 것이 늘기만 한다", sorted(found))


def test_the_manifest_search_also_finds_the_b_a8r1_three_layer_names(tmp_path):
    """★ 2026-09-24 실측 — B_A8R1 묶음은 세 겹이고 manifest 이름이 겹마다 다르다: 겉 wrapper
    `HANDOFF_MANIFEST.json` · 안쪽 배치 `PACKAGE_MANIFEST.json`(대문자) · 바깥 최종화
    `EXTERNAL_PACKAGE_MANIFEST.json`. 기존 `find` 는 소문자 두 이름만 찾아 세 겹 **전부** 4 단계에서
    멈춘다 (ZIP 크기·SHA 는 전달값과 정확히 일치했다).

    멈춘 것은 옳다. 넓히는 것은 후보 집합뿐이고 고르는 것은 여전히 `--expect-manifest-sha` 다.
    `CODE_MANIFEST.json`(24 개 코드 파일의 부분 목록)은 후보에 넣지 않는다 — 전체 묶음의 대조 기준이
    아니라서, 이름만 보고 담으면 골라야 할 것이 늘기만 한다.
    """
    import re
    import subprocess

    src = (ROOT / "scripts" / "preserve_handoff.sh").read_text(encoding="utf-8")
    m = re.search(r'ALL_MAN="\$\(find "\$TMP" (.+?) -type f \| sort\)"', src)
    assert m, "manifest 후보를 찾는 줄의 모양이 바뀌었다 — 시험을 고칠 것"
    expr = m.group(1)

    (tmp_path / "dep").mkdir()
    for name in ("HANDOFF_MANIFEST.json", "EXTERNAL_PACKAGE_MANIFEST.json"):
        (tmp_path / name).write_text("{}", encoding="utf-8")
    for name in ("PACKAGE_MANIFEST.json", "CODE_MANIFEST.json"):
        (tmp_path / "dep" / name).write_text("{}", encoding="utf-8")
    r = subprocess.run(["bash", "-c", f'find "$1" {expr} -type f | sort', "_", str(tmp_path)],
                       capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr[-400:]
    found = {pathlib.Path(x).name for x in r.stdout.split()}
    assert found >= {"HANDOFF_MANIFEST.json", "PACKAGE_MANIFEST.json", "EXTERNAL_PACKAGE_MANIFEST.json"}, (
        "B_A8R1 세 겹의 manifest 이름 중 일부를 못 찾는다 — 그 겹은 4 단계에서 멈춘다", sorted(found))
    assert "CODE_MANIFEST.json" not in found, ("부분 목록을 후보로 삼았다", sorted(found))


# ── manifest 의 항목 목록 키가 묶음마다 다르다 (2026-09-15 실측) ─────────────────────────────

def _hm():
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "handoff_manifest", ROOT / "scripts" / "handoff_manifest.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_the_entry_list_key_differs_between_bundles():
    """★ 2026-09-15 실측 — 세 묶음이 5 단계에서 `manifest 에 entries 가 없다` 로 멈췄다.

    ZIP 크기·SHA·manifest 해시는 셋 다 전달값과 **정확히 일치**했다. 다른 것은 자료가 아니라
    **목록 키**다 — `desktop_postproc` 은 `entries`, guard 와 review 기록은 `files`,
    복구 기록은 `payload` 다. 항목 모양은 셋 다 같다 (`path` · `bytes` · `sha256`).

    멈춘 것 자체는 옳다. 고칠 것은 **아는 키를 늘리는 것**이고, 모르는 모양은 계속 멈춘다.
    """
    hm = _hm()
    item = {"path": "a/b.json", "bytes": 3, "sha256": "0" * 64}
    for key in ("entries", "files", "payload"):
        assert hm.entry_list({key: [item]}) == [item], key


def test_an_entry_may_name_its_path_with_the_key_file():
    """★ 2026-09-24 실측 — B_A8R1 세 manifest 의 항목 키가 `file` · `bytes` · `sha256` 이다 (`path` 가
    아니다). 기존 규칙은 이것을 "경로 없음" 으로 거부해 세 겹 전부 5 단계에서 멈춘다.

    `file` 을 `path` 의 별칭으로 받되, 돌려주는 항목은 **`path` 로 정규화**한다 — 소비 자리 셋(5 단계 ·
    6 단계 · 안내문)이 전부 `e["path"]` 를 읽기 때문이다. 둘 다 있는데 서로 다르면 어느 쪽을 대조한
    것인지 알 수 없으므로 거부한다.
    """
    hm = _hm()
    out = hm.entry_list({"files": [{"file": "a/b.json", "bytes": 3, "sha256": "0" * 64}]})
    assert len(out) == 1 and out[0]["path"] == "a/b.json" and out[0]["sha256"] == "0" * 64, out
    same = hm.entry_list({"files": [{"file": "a", "path": "a", "sha256": "0" * 64}]})
    assert same[0]["path"] == "a"
    with pytest.raises(ValueError):
        hm.entry_list({"files": [{"file": "a", "path": "b", "sha256": "0" * 64}]})


def test_an_entry_list_without_a_path_or_sha_is_refused():
    """대조할 수 없는 것을 보존하면 보존의 뜻이 사라진다 — 항목마다 경로와 sha256 을 **둘 다** 요구한다."""
    hm = _hm()
    for bad in ({"files": [{"path": "a"}]},                      # sha 없음
                {"files": [{"sha256": "0" * 64}]},               # 경로 없음
                {"files": ["a/b.json"]},                         # dict 가 아님
                {"files": []},                                   # 비었음
                {"manifest_version": 3},                         # 목록이 아예 없음
                {"notes": "무엇도 아님"}):
        with pytest.raises(ValueError):
            hm.entry_list(bad)


def test_two_plausible_entry_lists_are_an_ambiguity_not_a_guess():
    """키가 둘 다 있으면 **고르지 않는다** — 무엇을 대조한 것인지 사람이 정해야 한다."""
    hm = _hm()
    item = {"path": "a", "sha256": "0" * 64}
    with pytest.raises(ValueError, match="둘 이상|ambiguous|여럿"):
        hm.entry_list({"entries": [item], "files": [item]})


def test_the_preserve_script_uses_that_one_rule():
    """규칙이 두 벌이면 언젠가 갈린다 — 스크립트의 **모든** 소비 자리가 같은 함수를 부른다.

    ★ 2026-09-15 — 첫 수정판은 5 단계만 고쳤다. 시험이 `m.get("entries")` 한 철자만 막아서
      6 단계의 `m["entries"]` 와 안내문의 같은 줄을 놓쳤고, 사용자 기계에서 세 묶음이 전부
      6 단계 `KeyError: 'entries'` 로 죽었다 (5 단계는 통과한 뒤였다).

      **규칙이 두 벌이면 언젠가 갈린다** 는 문장을 시험이 한 벌만 보고 있었던 셈이다.
      이제 철자가 아니라 **모든 접근 자리**를 센다.
    """
    import re

    src = (ROOT / "scripts" / "preserve_handoff.sh").read_text(encoding="utf-8")
    assert "handoff_manifest" in src and "entry_list" in src, (
        "보존 스크립트가 자기만의 목록 판별을 들고 있다")
    direct = re.findall(r'm(?:\w*)\s*(?:\.get\(\s*"entries"|\[\s*"entries"\s*\])', src)
    assert not direct, ("manifest 의 목록을 직접 꺼내는 자리가 남아 있다 — 규칙이 두 벌이다", direct)
    # 소비 자리는 셋이다: 5 단계 대조 · 6 단계 복사 뒤 재대조 · 사람이 치는 안내문
    assert src.count("entry_list(") >= 3, (
        "소비 자리 셋(5 단계 · 6 단계 · 안내문) 중 일부가 공유 규칙을 안 부른다",
        src.count("entry_list("))
