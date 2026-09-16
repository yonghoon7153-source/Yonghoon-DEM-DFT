"""R11 패키지 probe 의 **닫힘 재생기** — 보관한 원본(`codex/`)은 대상 SHA(2add074)와 리뷰어 워크스페이스 경로를
전제하므로 현재 트리에서 그대로는 돌지 않는다. 이 러너는 네 스크립트를 **자식 프로세스로** 그 계약 그대로 돌리고,
case 마다 "반례가 아직 있는가" 를 **봉인한 술어**로 판정한다 (R7·R9·R10 러너와 같은 세 칸: 도달 · 상태 · 멈춘_곳).

R11 의 네 스크립트는 assert 하지 않고 **field 로** 보고한다 — 그래서 닫힘 판정은 아래 `CLOSED` 표가 정본이고,
표에 없는 case 는 닫힘으로 세지 않는다 (Codex R11 P1-12 가 R10 러너에서 지적한 것과 같은 규율).

증거 계약은 `reviews/evidence_gate.py` 한 자리에서 온다: `python -O` 거부 · `git` rc 확인 · index skip flag(소문자와
대문자 `S` 둘 다) 거부 · **gate import 전** bytecode 격리 · expected commit 의 sparse worktree 에서 실행 ·
**풀린 bytes 를 blob 과 재대조**(checkout filter) · 도구 자신의 봉인 · full 40 자 expected head. 전부 통과해야
`evidence_eligible: true`.

    python3 reviews/r11_repros/replay_codex_r11.py --target . --expected-head <40-hex> [--output x.json]
"""
from __future__ import annotations

# ⚠ Codex R13 P1-4: 재실행은 **어떤 앱 의존성 import 보다 앞**이다. 전 판은 아래 `import argparse, …`
#   가 먼저 돌았고 `sys.path[0]` 이 저장소 안이라 untracked 모듈 하나가 봉인 앞에서 실행될 수 있었다
#   (C08 의 남은 절반). `os`·`sys` 는 인터프리터 시작 때 이미 로드돼 sys.path 로 가로챌 수 없다.
import os
import sys

if globals().get("__name__") == "__main__" and not sys.flags.safe_path:
    # ⚠ `-E` 는 `PYTHONOPTIMIZE` 도 무시한다 — 그냥 재실행하면 R10 P2-4 의 "`-O` 에서는 증거를 만들지 않는다" 가
    #   **조용히 사라진다** (거부도 준수도 아닌 정규화). 재실행 **전에** 그 요청을 보고 거부한다.
    if sys.flags.optimize or os.environ.get("PYTHONOPTIMIZE"):
        print("! 이 러너는 `python -O`(PYTHONOPTIMIZE) 에서 증거를 만들지 않는다 — 보관한 probe 의 반례는 "
              "`assert` 로 쓰여 있고 optimize 모드는 그것을 통째로 지운다 (Codex R10 P2-4)", file=sys.stderr)
        raise SystemExit(2)
    os.environ.pop("PYTHONPATH", None)
    os.execv(sys.executable, [sys.executable, "-P", "-E", "-B", os.path.abspath(__file__), *sys.argv[1:]])

import argparse, contextlib, importlib.util, io, json, os, pathlib, shutil, subprocess, sys, tempfile, traceback

# ⚠ Codex R11 P1-10 반례 A: gate 를 **import 하기 전에** bytecode 캐시를 돌린다.
# ⚠ 자체 리뷰 C08: 그것은 bytecode 만 막았다 — `sys.path[0]`(이 러너가 든 저장소 안 디렉터리)에 놓인 untracked
#   `traceback.py` 하나가 gate 보다 먼저 실행되고 `INSTRUMENT` 밖이라 봉인에 안 걸렸다. `-P -E` 로 재실행한다.
# ⚠ 재실행은 **스크립트로 직접 돌 때만** 한다. 회귀(`test_e11_11`·`test_e11_12`)는 이 파일을 `exec` 해서
#   `child_ok`·`_classify` 를 직접 부르는데, module level 에서 `execv` 하면 **그 테스트 프로세스가 갈아치워진다**
#   (실측: pytest 가 26 번째 항목에서 조용히 죽었다).

_PYC = tempfile.mkdtemp(prefix="evidence-pycache-")
sys.pycache_prefix = _PYC
os.environ["PYTHONPYCACHEPREFIX"] = _PYC
sys.dont_write_bytecode = True
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import evidence_gate as gate                                              # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
PKG_REL = "reviews/r11_repros/codex"
SUMS_NAME = "HARNESS_R11_SHA256SUMS.txt"
PKG = HERE / "codex"
SUMS = PKG / SUMS_NAME
PINNED = "2add074cf0c3ebfaa02b22d2311dd4330f0879b0"
INSTRUMENT = ("reviews/r11_repros/replay_codex_r11.py", "reviews/evidence_gate.py")
#: 리뷰어 워크스페이스가 `../work/harness-r11-target-wsl/bms-balancing` 을 대상 트리로 본다 (publish 스크립트는
#: 인자를 안 받고 이 상대 경로를 쓴다). snapshot 안에 그 자리를 만들어 준다 — 원본 스크립트는 안 고친다.
WSL_REL = pathlib.Path("work") / "harness-r11-target-wsl" / "bms-balancing"


def _eligible(promotion):
    return bool(promotion) and promotion.get("promotion_eligible") is True


def _blocked(promotion, key):
    return bool(promotion) and int((promotion.get("blocked_by") or {}).get(key, 0)) > 0


# ── case 별 닫힘 술어 (봉인) ────────────────────────────────────────────────────────────────────
#   값은 (한 줄 설명, 판정 함수). 판정 함수는 그 case 의 결과 dict 를 받아 True(닫힘)/False(재현) 를 낸다.
#: `r11_root_repros.py` 는 case 마다 자기 반례를 **assert** 한다 — 그 줄에서 멈춰야만 닫힘이다. 아무 AssertionError
#: 나 닫힘으로 읽으면 무관한 불변식이 증거를 위조한다 (Codex R11 P1-12 가 R10 러너에서 지적한 것과 같은 축).
COUNTEREXAMPLE_LINES = {
    "root:schema_only": ('assert got["rc"] == 0 and got["promotion"]["promotion_eligible"] is True',),
    "root:input_bytes": ('assert got["rc"] == 0 and got["promotion"]["promotion_eligible"] is True',),
    "root:dirty_code": ('assert got["rc"] == 0 and got["promotion"]["promotion_eligible"] is True',),
    "root:invalid_numeric": ('assert not problems and got["rc"] == 0',),
    "root:matrix_authority": ("assert rc_full == rc_small == 0 and n_full == 8",),
    "root:profile_grid": ("assert rc_full == rc_small == 0 and n_full == 3",),
}

CLOSED = {
    # r11_data_contract_repros.py
    "data:receipt_identity": (
        "네 digest 가 다르면 check_u14 가 막는다 (P1-1)",
        lambda r: not _eligible(r.get("promotion")) and _blocked(r.get("promotion"), "inputs")),
    "data:receipt_shape": (
        "path 뒤바꿈은 role→path 로 드러나고, 평탄화 중복 역할은 거부된다 (P1-6 · P2-3)",
        lambda r: bool(r.get("duplicate_role_validate_problems"))),
    "data:allowlist": (
        "부재 allowlist 가 실제 파일과 모순되면 hard-fail (P1-4)",
        lambda r: r.get("canonical_written") is False),
    "data:matrix_subset": (
        "caller 가 좁힌 matrix 는 canonical 이 아니다 (P1-2)",
        lambda r: r.get("canonical_written") is False),
    "data:profile_grid": (
        "`--grid 1` 은 canonical 이 아니다 (P1-3)",
        lambda r: r.get("canonical_written") is False),
    "data:shape_reader": (
        "production reader 가 공용 validator 를 거쳐 error 행을 안 먹는다 (P1-7)",
        # 수정 뒤 reader 는 아예 **거부한다** — 원본 probe 는 그 예외에서 죽는다. 그 예외 문구가 이 case 의 닫힘
        # fingerprint 다 (아무 예외나 닫힘으로 읽지 않는다).
        lambda r: r.get("reader_used_error_row") is False
        or ("공용 스키마 검증 실패" in str(r.get("error", "")) and "`error` 행" in str(r.get("error", "")))),
    # r11_publish_schema_repros.py
    "publish:matrix_filtered_canonical": (
        "좁힌 matrix 는 canonical 자리에 없다 (P1-2)",
        lambda r: r.get("canonical_exists") is False),
    "publish:profile_grid1_canonical": (
        "`--grid 1` 산출은 canonical 자리에 없다 (P1-3)",
        lambda r: r.get("canonical_exists") is False),
    "publish:profile_partial_stdout": (
        "sink 가 stdout 이어도 부분은 rc 3 이다 (P2-1)",
        lambda r: r.get("rc") != 0),
    "check:schema_only_no_baseline": (
        "schema-only 는 승격 증명서가 아니다 (P1-6)",
        lambda r: not _eligible(r.get("promotion"))),
    "check:schema_only_skips_env_controls_argv": (
        "같음 (P1-6)", lambda r: not _eligible(r.get("promotion"))),
    "check:full_compare_missing_argv_and_roster": (
        "argv·roster 가 없으면 승격 못 한다 (P1-6 · P2-3)",
        lambda r: not _eligible(r.get("promotion")) and _blocked(r.get("promotion"), "schema")),
    "check:changed_git_state_promoted": (
        "실행 중 git 상태가 바뀐 산출은 승격 못 한다 (P1-9)",
        lambda r: not _eligible(r.get("promotion")) and _blocked(r.get("promotion"), "provenance")),
    "check:artifact_env_disagrees_with_meta_promoted": (
        "본문과 meta 의 조건이 어긋나면 막는다 (P1-9)",
        lambda r: not _eligible(r.get("promotion"))),
    "check:per_file_alias_self_comparison": (
        "파일 단위 hardlink 자기대조는 승격 근거가 아니다 (P1-5)",
        lambda r: not _eligible(r.get("promotion")) and _blocked(r.get("promotion"), "alias")),
    "check:matrix_inf_promoted": (
        "matrix 의 inf 는 스키마 문제다 (P1-8)",
        lambda r: not _eligible(r.get("promotion"))),
    "check:degeneracy_infinity_promoted": (
        "degeneracy 의 Infinity 는 스키마 문제다 (P1-8)",
        lambda r: not _eligible(r.get("promotion"))),
    "check:profile_gamma_roster_not_validated": (
        "gamma_roster 는 parse 해서 본다 (P2-4)",
        lambda r: bool(r.get("problems"))),
    "check:changed_valid_input_digests_promoted": (
        "유효하지만 다른 입력 digest 는 막는다 (P1-1)",
        lambda r: not _eligible(r.get("promotion")) and _blocked(r.get("promotion"), "inputs")),
    "check:duplicate_receipt_direct": (
        "평탄화된 중복 논리 역할은 거부된다 (P2-3)",
        lambda r: bool(r.get("problems"))),
    "check:changed_equivocal_receipt_promoted": (
        "모호한 receipt 로 바뀐 입력은 막는다 (P1-1 · P2-3)",
        lambda r: not _eligible(r.get("promotion"))),
    "publish:shape_step": (
        "rc 0 인데 meta 가 partial 이면 모순으로 막고, stale canonical 을 안 읽는다 (P2-2)",
        lambda r: "SHAPE_STEP_RC=0" not in (r.get("stdout") or [])),
    # r11_evidence_gate_repros.py — case 이름이 곧 key
    "evidence:early-gate-pyc": ("gate import 전에 bytecode 를 격리한다 (P1-10 A)",
                                lambda r: r.get("false_identity") is False),
    "evidence:abbreviated-head": ("짧은 expected head 를 거부한다 (P2-6)",
                                  lambda r: r.get("abbreviated_identity_accepted") is False),
    "evidence:skip-worktree": ("대문자 `S` skip-worktree 를 잡는다 (P2-5)",
                               lambda r: r.get("skip_flag_accepted") is False),
    "evidence:materialize-smudge": ("풀린 bytes 를 blob 과 재대조한다 (P1-10 B)",
                                    lambda r: r.get("materialized_bytes_not_commit_bytes") is False),
    "evidence:r10-assertion-alias": ("무관한 AssertionError 를 닫힘으로 읽지 않는다 (P1-12)",
                                     lambda r: r.get("unrelated_assertion_certified_closed") is False),
    "evidence:r10-child-rc": ("자식 rc 0 을 강제한다 (P1-11)",
                              lambda r: r.get("nonzero_children_certified_closed") is False),
    "evidence:u18-dirty-meta": ("unsafe git meta 는 승격 못 한다 (P1-9)",
                                lambda r: r.get("unsafe_git_meta_promoted") is False),
    "evidence:untracked-sitecustomize": ("산출 root 밖 untracked 는 코드로 센다 (P1-9)",
                                         lambda r: r.get("untracked_code_reported_clean") is False),
}

DATA_CASES = ("receipt_identity", "receipt_shape", "allowlist", "matrix_subset", "profile_grid",
              "shape_reader", "shape_wrapper")
EVIDENCE_CASES = ("early-gate-pyc", "abbreviated-head", "skip-worktree", "materialize-smudge",
                  "r10-assertion-alias", "r10-child-rc", "u18-dirty-meta", "untracked-sitecustomize")
#: 이 환경에서 **실행 자체가 불가능한** case — 무엇이 대신 보는지 같이 적는다 (닫힘으로 세지 않는다).
# ⚠ Codex R13 P2-5: 전 판 값은 괄호만 있고 쉼표가 없는 **문자열**이라 `[0]` 이 첫 글자("원")를 냈다. 구조로 두고,
#   환경상 불가는 `FileNotFoundError` 접두어가 아니라 **구체적 의존성**(`wsl.exe`) 이 fingerprint 에 있을 때만이다.
ENVIRONMENT_LIMITED = {
    "data:shape_wrapper": {
        "why": ("원본이 `wsl.exe` 로 wrapper 를 부른다 (리뷰어는 Windows). 같은 축은 "
                "`publish:shape_step` 이 native 로 재생하고 회귀는 `test_e11_14` 가 고정한다"),
        "substitute": "publish:shape_step",
        "fingerprint": ("FileNotFoundError", "wsl.exe"),
    },
}
#: publication 그룹의 leaf — 그룹이 첫 case 에서 중단돼도 **각 leaf 를 남긴다** (35 record 가 아니라 37 leaf).
PUBLICATION_LEAVES = ["publish:matrix_filtered_canonical", "publish:profile_grid1_canonical", "publish:profile_partial_stdout"]
#: 제외 case 의 대체 증거 이름. 없는 것은 없다고 둔다 — 지어내지 않는다.
SUBSTITUTES = {
    "data:shape_wrapper": "publish:shape_step",
    "publish:matrix_filtered_canonical": "data:matrix_subset",
    "publish:profile_grid1_canonical": "data:profile_grid",
    "root:profile_grid": "data:profile_grid (canonical_written False) + test_d10_03 (회귀)",
    # ⚠ R16 (2026-09-16): 이 leaf 는 publication 그룹이 **첫 case 에서 중단**돼 미실행으로 남았고, 그동안
    #   대체 증거가 없어 `closed_with_substitutes: false` 였다. 대체는 **이미 저장소에 있었다** —
    #   `test_e11_13` 이 `out=None` 부분 실행에서 rc 3 을 직접 관측한다. 여기 적힌 술어(`rc != 0`)보다
    #   **더 강한** 주장이다 (3 을 정확히 요구한다). 이름을 여기 등록해 "있는데 안 세던" 상태를 닫는다.
    #   ⚠ 이름만 적고 끝내지 않는다 — `test_r16_21` 이 여기 적힌 test 이름이 **실재하는지** 댄다
    #     (신고된 위험은 값으로 소비한다, R11 P1-9).
    "publish:profile_partial_stdout": "test_e11_13 (회귀 — sink 없는 부분 실행이 rc 3)",
}
EXPECTED_LEAVES = ["root:schema_only", "root:input_bytes", "root:dirty_code", "root:invalid_numeric", "root:matrix_authority", "root:profile_grid", "data:receipt_identity", "data:receipt_shape", "data:allowlist", "data:matrix_subset", "data:profile_grid", "data:shape_reader", "data:shape_wrapper", "check:schema_only_no_baseline", "check:schema_only_skips_env_controls_argv", "check:full_compare_missing_argv_and_roster", "check:changed_git_state_promoted", "check:artifact_env_disagrees_with_meta_promoted", "check:per_file_alias_self_comparison", "check:matrix_inf_promoted", "check:degeneracy_infinity_promoted", "check:profile_gamma_roster_not_validated", "check:changed_valid_input_digests_promoted", "check:duplicate_receipt_direct", "check:changed_equivocal_receipt_promoted", "publish:matrix_filtered_canonical", "publish:profile_grid1_canonical", "publish:profile_partial_stdout", "publish:shape_step", "evidence:early-gate-pyc", "evidence:abbreviated-head", "evidence:skip-worktree", "evidence:materialize-smudge", "evidence:r10-assertion-alias", "evidence:r10-child-rc", "evidence:u18-dirty-meta", "evidence:untracked-sitecustomize"]


#: 수정이 원본 probe 의 **전제를 무너뜨려** 그 자리에서 죽는 case — 무엇이 죽어야 하는지 fingerprint 로 봉인한다.
#: 아무 예외나 "전제 변경" 으로 읽으면 그것도 증거 위조다.
PREMISE_CHANGED = {
    "publish:*": ("좁힌 matrix 는 이제 canonical 자리에 안 쓴다 — 원본 probe 는 그 파일을 무조건 열어 죽는다 "
                  "(같은 축은 `data:matrix_subset`·`data:profile_grid`·`root:matrix_authority` 가 따로 본다)"),
    "root:profile_grid": ("원본의 '완전' 대조군이 `--grid 3` 이다 — 정본 격자(21)가 아니면 그것도 subset 이라 "
                          "canonical 자리에 파일이 없다. 원본은 그 파일을 열다 죽는다. 같은 축은 "
                          "`data:profile_grid`(canonical_written False) 와 회귀 `test_d10_03` 이 본다"),
}
PREMISE_FINGERPRINT = {
    "publish:*": ("publish/matrix_100.csv", "No such file or directory"),
    "root:profile_grid": ("profile_gamma_100_Li.csv", "No such file or directory"),
}


def _premise_matches(key, exc) -> bool:
    want = PREMISE_FINGERPRINT.get(key)
    text = f"{type(exc).__name__}: {exc}"
    return bool(want) and all(w in text for w in want)


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _classify(fn, pkg_dir, case_key):
    """assert 계약 case: 자기 반례 assertion 에서 멈춰야만 **반례 소멸** (Codex R11 P1-12)."""
    buf = io.StringIO()
    want = COUNTEREXAMPLE_LINES.get(case_key)
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            detail = fn()
        return {"도달": True, "상태": "재현", "멈춘_곳": None, "세부": str(detail)[:600]}
    except AssertionError as e:
        tb = traceback.extract_tb(sys.exc_info()[2])
        frames = [f for f in tb if str(pkg_dir) in (f.filename or "")]
        line = (frames[-1].line or "").strip() if frames else ""
        where = (f"{pathlib.Path(frames[-1].filename).name}:{frames[-1].lineno}: {line}" if frames else "?")
        if not frames:
            return {"도달": False, "상태": "오류", "멈춘_곳": where, "세부": str(e)[:400]}
        if want is None:
            return {"도달": True, "상태": "오류", "멈춘_곳": where,
                    "세부": f"case {case_key!r} 의 반례 fingerprint 가 봉인 표에 없다 — 닫힘으로 세지 않는다"}
        if not any(w in line for w in want):
            return {"도달": True, "상태": "오류", "멈춘_곳": where,
                    "세부": f"이 case 의 반례 assertion 이 아니다 (기대 {list(want)}): {str(e)[:300]}"}
        return {"도달": True, "상태": "반례 소멸", "멈춘_곳": where, "세부": str(e)[:600]}
    except BaseException:                                                  # noqa: BLE001
        tb = traceback.format_exc().strip().splitlines()
        return {"도달": False, "상태": "오류", "멈춘_곳": tb[-1][:300], "세부": "반례 assertion 전에 예외"}


def _record(status, where, detail, note=None):
    d = {"도달": status != "오류", "상태": status, "멈춘_곳": where, "세부": detail}
    if note:
        d["비고"] = note
    return d


def _judge(key, payload):
    """봉인한 술어로 판정. 표에 없으면 닫힘으로 세지 않는다 (Codex R11 P1-12 의 규율)."""
    if key not in CLOSED:
        return _record("오류", "봉인 표에 없다", f"{key} 의 닫힘 술어가 없다 — 닫힘으로 세지 않는다")
    why, pred = CLOSED[key]
    try:
        ok = bool(pred(payload))
    except BaseException as e:                                            # noqa: BLE001
        return _record("오류", f"{type(e).__name__}: {e}", payload)
    return _record("반례 소멸" if ok else "재현", why, payload)


def _child(cmd, cwd, env=None, timeout=1800):
    e = dict(os.environ)
    e.update(env or {})
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, env=e, timeout=timeout)


def child_ok(proc) -> bool:
    """자식이 증거를 낼 수 있는 상태로 끝났는가 (Codex R11 P1-11: payload 를 읽기 **전에** rc 를 본다)."""
    return getattr(proc, "returncode", None) == 0


def _payload(proc):
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=pathlib.Path, default=pathlib.Path("."))
    ap.add_argument("--expected-head", required=True, metavar="SHA40")
    ap.add_argument("--allow-dirty", action="store_true",
                    help="격리 snapshot 없이 working tree 에서 (개발용, `evidence_eligible: false`)")
    ap.add_argument("--keep-materialized", type=pathlib.Path, default=None)
    ap.add_argument("--output", type=pathlib.Path)
    a = ap.parse_args()
    snapshot = cleanup = None
    try:
        gate.require_assertions()
        target = a.target.resolve()
        head = gate.git_head(target)
        exp = gate.full_head(target, a.expected_head)                     # P2-6: full 40 자만
        if head != exp:
            print(f"! HEAD mismatch — expected {exp}, 실제 {head} (다르다) — 돌리지 않았다", file=sys.stderr)
            return 2
        tree = gate.tree_of(target, head)
        dirty = gate.dirty_paths(target)
        skipped = gate.index_skip_flags(target)
        if skipped:
            print(f"! index 에 skip flag 가 걸린 tracked 파일: {skipped[:10]} (Codex R11 P2-5)", file=sys.stderr)
            return 2
        sealed, seal_detail = gate.instrument_sealed(target, INSTRUMENT)
        if not a.allow_dirty:
            snapshot, cleanup = gate.materialize(target, head, keep=a.keep_materialized)
            drift = gate.verify_snapshot_bytes(snapshot, head)             # P1-10 반례 B
            if drift:
                raise gate.EvidenceError(f"snapshot bytes 가 blob 과 다르다: {drift[:5]}")
            target = snapshot
            globals()["PKG"] = snapshot / PKG_REL
            globals()["SUMS"] = snapshot / PKG_REL / SUMS_NAME
    except gate.EvidenceError as e:
        print(f"! {e}", file=sys.stderr)
        return 2

    digest_ok, digest = gate.package_digest(PKG, SUMS)
    out = {"target_head": head, "expected_head": exp, "expected_tree": tree, "pinned_sha": PINNED,
           "pin_bypassed": True, "dirty": bool(dirty), "dirty_allowed": bool(a.allow_dirty),
           "dirty_paths": dirty[:50],
           "evidence_eligible": bool(snapshot) and digest_ok and sealed,
           "instrument_sealed": sealed, "instrument": seal_detail,
           "materialized": ({"path": str(snapshot), "head": head, "mode": "sparse detached worktree",
                             "kept": bool(a.keep_materialized)} if snapshot else None),
           "ran_in": "격리 snapshot" if snapshot else "working tree (--allow-dirty)",
           "package_digest_ok": digest_ok, "package_digest": digest,
           "설명": "R11 네 스크립트를 자식으로 그대로 돌리고 case 마다 **봉인한 술어**로 닫힘을 판정한다 — "
                 "술어가 표에 없으면 닫힘으로 세지 않는다 (Codex R11 P1-12)",
           "probes": {}}
    R = out["probes"]
    try:
        # ── (1) root: assert 계약 — 원본 case 함수를 **직접** 부르고 자기 반례 assertion 에서 멈추는지 본다
        root_mod = _load("r11c_root", PKG / "r11_root_repros.py")
        S_t, V_t = root_mod.load_target(target)
        root_cases = {
            "root:schema_only": lambda: root_mod.case_schema_only_promotes(target, S_t),
            "root:input_bytes": lambda: root_mod.case_different_input_bytes_promote(target, S_t),
            "root:dirty_code": lambda: root_mod.case_dirty_changed_code_promotes(target, S_t),
            "root:invalid_numeric": lambda: root_mod.case_invalid_numeric_schema(target, S_t),
            "root:matrix_authority": lambda: root_mod.case_matrix_authority_shrinks(S_t, V_t),
            "root:profile_grid": lambda: root_mod.case_profile_grid_shrinks(S_t, V_t),
        }
        for key, fn in root_cases.items():
            R[key] = _classify(fn, PKG, key)

        # ── (2) data contract: field 계약 — case 마다 자식으로 (원본이 그렇게 부른다)
        for case in DATA_CASES:
            key = f"data:{case}"
            proc = _child([sys.executable, str(PKG / "r11_data_contract_repros.py"),
                           "--target", str(target), "--case", case], target)
            payload = _payload(proc)
            rec = (payload or {}).get("results", {}).get(case)
            env_lim = ENVIRONMENT_LIMITED.get(key)
            if env_lim and all(w in (rec or {}).get("error", "") for w in env_lim["fingerprint"]):
                R[key] = _record("환경상 불가", (rec or {}).get("error"), env_lim["why"],
                                 note="이 환경에서 실행할 수 없다 — 닫힘으로 세지 않는다")
                continue
            if rec is None:
                R[key] = _record("오류", f"child rc {proc.returncode}, payload 없음",
                                 (proc.stderr.strip()[-400:] or proc.stdout[-400:] or "출력 없음"))
                continue
            R[key] = _judge(key, rec)
            R[key]["child_rc"] = proc.returncode          # 자식 rc 를 숨기지 않는다 (Codex R11 P1-11)

        # ── (3) publish/checker/shape_step: 인자를 안 받고 `../work/harness-r11-target-wsl/bms-balancing` 를 본다.
        #        그 자리를 **이 단계에서만** 만든다 — 트리 안에 자기 자신을 가리키는 symlink 를 남기면 다른 probe 의
        #        copytree 가 무한히 돈다 (실측).
        # ⚠ 자체 리뷰 C35: 전 판은 트리 **안에** 자기참조 symlink 를 만들었다. `finally` 는 파이썬 예외만 덮으므로
        #   SIGTERM 이면 남고, `.gitignore` 가 그것을 `git status` 에서 감춘다 — 그 뒤 `copytree` 를 쓰는 probe 들이
        #   무한 재귀로 터진다 (실측). 패키지 사본을 임시 디렉터리에 두고 거기서 상대 경로를 맞춘다.
        ws = pathlib.Path(tempfile.mkdtemp(prefix="r11-replay-ws-"))
        shutil.copytree(PKG, ws / "codex")
        wsl = ws / WSL_REL
        wsl.parent.mkdir(parents=True, exist_ok=True)
        wsl.symlink_to(target, target_is_directory=True)
        try:
            pub = _load("r11c_publish", ws / "codex" / "r11_publish_schema_repros.py")
            with tempfile.TemporaryDirectory(prefix="r11-replay-publish-") as td:
                tmp = pathlib.Path(td)
                for group, fn in (("publication", lambda: pub.publication_repros(tmp)),
                                  ("checker", lambda: pub.checker_repros(tmp))):
                    try:
                        got = fn()
                    except BaseException as e:            # noqa: BLE001
                        prefix = "publish" if group == "publication" else "check"
                        # ⚠ Codex R13 P2-5: 그룹이 첫 case 에서 중단돼도 **leaf 마다** 기록한다 — 첫 leaf 만
                        #   fingerprint 로 전제 변경, 나머지는 `미실행 (그룹 중단)`. 후속 leaf 의 전제가 바뀌었다고
                        #   추정하지 않는다.
                        leaves = PUBLICATION_LEAVES if group == "publication" else [k for k in EXPECTED_LEAVES if k.startswith("check:")]
                        hit = _premise_matches(f"{prefix}:*", e)
                        first = leaves[0]
                        R[first] = _record(
                            "전제 변경" if hit else "오류", f"{type(e).__name__}: {str(e)[:200]}",
                            PREMISE_CHANGED.get(f"{prefix}:*", "원본 probe 가 수정 전 상태를 전제한다")
                            if hit else f"기대한 전제 변경 fingerprint 가 아니다 — 닫힘으로 세지 않는다: {str(e)[:200]}")
                        for k in leaves[1:]:
                            R[k] = _record("미실행 (그룹 중단)", f"{first} 에서 그룹이 중단됐다",
                                           "이 leaf 는 돌지 않았다 — 전제가 바뀌었다고 추정하지 않는다", note="개별 판정 미완")
                        continue
                    for name, rec in (got or {}).items():
                        k = ("publish:" if group == "publication" else "check:") + name
                        R[k] = _judge(k, rec)
                R["publish:shape_step"] = _judge("publish:shape_step", pub.shape_step_repro())
        finally:
            shutil.rmtree(ws, ignore_errors=True)

        # ── (4) evidence gate: 원본 기법이 pycache 기본 자리를 쓰므로 우리 prefix 를 **빼고** 자식으로 돌린다
        # ⚠ 자체 리뷰 C30: 전 판은 **모든** evidence 자식의 env 에서 `PYTHONPYCACHEPREFIX` 를 벗겼고, 그 결과
        #   실행이 끝난 snapshot 에 `__pycache__` 가 7 개 남았다 (P1-10 A 가 쓰던 `reviews/__pycache__/` 포함).
        #   그런데 그것을 **전부** 다른 prefix 로 바꾸면 안 된다 — `early-gate-pyc` 는 `cache_from_source` 의
        #   **기본 자리**에 위조 pyc 를 놓는 것이 기법 자체라 prefix 가 있으면 성립하지 않는다 (실측: ValueError).
        #   기법이 그 자리를 요구하는 case 만 벗기고, 나머지는 우리 임시 prefix 로 보낸다.
        NEEDS_DEFAULT_PYCACHE = {"early-gate-pyc"}
        _child_pyc = tempfile.mkdtemp(prefix="evidence-child-pycache-")
        ev_env_clean = {k: v for k, v in os.environ.items() if k != "PYTHONPYCACHEPREFIX"}
        ev_env_isolated = dict(os.environ, PYTHONPYCACHEPREFIX=_child_pyc)
        for case in EVIDENCE_CASES:
            key = f"evidence:{case}"
            proc = subprocess.run([sys.executable, str(PKG / "r11_evidence_gate_repros.py"),
                                   "--target", str(target), "--case", case],
                                  cwd=str(target), capture_output=True, text=True, timeout=1800,
                                  env=(ev_env_clean if case in NEEDS_DEFAULT_PYCACHE else ev_env_isolated))
            payload = _payload(proc)
            rec = (payload or {}).get("cases", {}).get(case)
            if not child_ok(proc) or rec is None:         # ⚠ Codex R11 P1-11: payload 를 읽기 전에 rc 를 본다
                R[key] = _record("오류", f"child rc {proc.returncode}",
                                 (proc.stderr.strip()[-400:] or proc.stdout[-400:] or "출력 없음"))
                continue
            R[key] = _judge(key, rec)
    finally:
        if cleanup and not a.keep_materialized:
            cleanup()

    # ⚠ 수정이 원본 probe 의 전제를 무너뜨린 case — **봉인한 fingerprint 와 맞을 때만** 전제 변경으로 적는다.
    for key, why in PREMISE_CHANGED.items():
        rec = R.get(key)
        if rec and rec["상태"] == "오류":
            where = str(rec.get("멈춘_곳") or "")
            if all(w in where for w in PREMISE_FINGERPRINT.get(key, ("\0",))):
                R[key] = {**rec, "상태": "전제 변경", "세부": why}
    # ⚠ Codex R13 P1-3: 공용 집계 — 제외는 대체 증거 이름과 함께 적고 closed 에서 뺀다.
    out.update(gate.summarize_verdicts(R, requested=EXPECTED_LEAVES, substitutes=SUBSTITUTES))
    text = json.dumps(out, ensure_ascii=False, indent=2, default=str)
    print(text)
    if a.output:
        a.output.write_text(text + "\n", encoding="utf-8")
    # ⚠ 자체 리뷰 C19: `evidence_eligible: false` 인 실행이 rc 0 으로 끝났다 — P1-11 이 자식에게 요구한 규율
    #   ("payload 를 읽기 전에 rc 를 본다")을 러너 자신이 어긴 것이다. 증거가 아닌 실행은 성공 코드로 끝나지 않는다.
    if not out["evidence_eligible"]:
        return 3
    return 0 if out["report_complete"] else 1   # rc 0 = 보고 완료 (closed 아님)


if __name__ == "__main__":
    sys.exit(main())
