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
    assert v.get("legacy_transition_approved") is True, ("승인 기록이 소비되지 않았다", v, out[-1200:])
    assert v.get("legacy_transition"), ("승인 id 를 안 적는다", v)
    b = v["blocked_by"]
    assert b["inputs_uncomparable"] > 0 and b["env_uncomparable"] > 0, b
    assert all(b[k] == 0 for k in ("schema", "content", "unit", "controls", "env", "numbers",
                                   "alias", "provenance", "inputs", "stale")), b


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
