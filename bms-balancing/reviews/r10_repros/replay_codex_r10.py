"""R10 패키지 probe 의 **닫힘 재생기** — 보관한 원본(`codex/`)은 SHA(bd6ba47)를 고정하거나 pre-fix 상태를 전제해
현재 트리에서는 그대로 돌지 않는다. 이 러너는 원본 case 함수를 **직접** 불러(pin 우회) R7·R9 러너와 같은 세 가지를
기록한다: 도달 · 상태(재현 / 반례 소멸 / 오류) · 멈춘_곳.

증거 계약은 `reviews/evidence_gate.py` 한 자리에서 온다 (Codex R10 P2-4·P2-5): `python -O` 거부 · `git` rc 확인 ·
index skip flag 거부 · `__pycache__` 격리 · **expected commit 의 sparse worktree 에서 대상 bytes 실행** · 도구 자신의
봉인까지 본 뒤에만 `evidence_eligible: true`.

세 스크립트의 성격이 다르다:

- `r10_snapshot_repros.py` · `r10_u18_shape_repros.py` — case 안에서 **assert 로** bad state 를 주장한다. 수정 뒤에는
  그 assertion 에서 멈추면 닫힌 것이다.
- `r10_evidence_repros.py` — assert 하지 않고 **field 로** 보고한다 (`false_positive`·`false_clean`·`false_identity`·
  `mutant_survived`·`corrupt_package_accepted`·`claim_gap`). 수정 뒤에는 그 flag 가 전부 False 여야 닫힌 것이다.

    python3 reviews/r10_repros/replay_codex_r10.py --target . --expected-head <sha> [--output x.json]
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

import argparse, contextlib, importlib.util, io, json, os, pathlib, subprocess, sys, tempfile, traceback

# ⚠ Codex R11 P1-10 반례 A: gate 를 **import 하기 전에** bytecode 캐시를 돌린다. 전 판은 gate 안에서
#   `isolate_bytecode()` 를 불렀는데, 그때는 이미 ignored `reviews/__pycache__/evidence_gate…pyc` (timestamp·size 를
#   맞춘 위조본)가 load 된 뒤였다 — 봉인 함수 자체가 위조본이었고 결과는 eligible true 였다.
#
# ⚠ 자체 리뷰 C08: 그것은 **bytecode 만** 막았다. 그보다 먼저 위의 `import argparse, …, traceback` 이 돌고
#   `sys.path[0]` 은 이 러너가 든 **저장소 안 디렉터리**다 — untracked `traceback.py` 하나면 gate 보다 먼저 실행되고
#   `INSTRUMENT` 밖이라 봉인에 안 걸린다. shim 이 gate 를 `sys.modules` 에 선주입하면 tracked 러너가 수정된
#   채로도 `dirty_paths: []` · `instrument: ok` · eligible true 가 나왔다 (실측). 봉인을 import 보다 앞에 두는
#   방법은 하나뿐이다 — `-P`(sys.path[0] 삽입 끔) · `-E`(PYTHON* 환경변수 무시)로 **한 번 재실행**한다.
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
PKG_REL = "reviews/r10_repros/codex"
SUMS_NAME = "HARNESS_R10_BD6BA474_SHA256SUMS.txt"
PKG = HERE / "codex"
SUMS = PKG / SUMS_NAME
PINNED = "bd6ba4749a92f8d441b4d9176eb876bfc6cc287c"
INSTRUMENT = ("reviews/r10_repros/replay_codex_r10.py", "reviews/evidence_gate.py")

#: 수정 뒤 False 여야 하는 evidence 스크립트의 flag (그 스크립트는 assert 하지 않고 field 로 말한다)
EVIDENCE_FLAGS = {
    "optimized-assertions": "false_positive",
    "git-status-error": "false_clean",
    "assume-unchanged": "false_identity",
    "ignored-pyc": "false_identity",
    "argv-binding-mutant": "mutant_survived",
    "package-enforcement-mutant": "corrupt_package_accepted",
    "wrapper-coverage": "claim_gap",
}
#: 우리 코드를 보지 않는 case — bash 의 `$*` 의미 자체를 보인다. 우리 쪽 닫힘은 `run_states.sh` 가 `$*` 를 안 쓰는
#: 것이고 그것은 아래 적응 probe 와 `test_d10_11` 이 본다.
LANGUAGE_LEVEL = {"argv", "argv-flatten-collision"}
#: 수정이 **전제를 바꿔** 원본이 반례 assertion 앞에서 죽는 case — 무엇이 바뀌었는지 적고 적응 probe 로 닫는다.
PREMISE_CHANGED = {
    "u18:shape_duplicates": ("중복 요청은 이제 rc 2 로 거부되고 **아무것도 게시하지 않는다** — 원본은 게시된 meta 를 "
                             "읽으려다 TypeError 로 죽는다. 닫힘은 적응 probe `adapted:duplicate-states` 가 본다"),
}
KNOWN_PROBES = ("snapshot", "u18", "evidence", "adapted")


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


#: case 별 **자기 반례 assertion** 의 소스 조각 (Codex R11 P1-12). 보관한 패키지의 그 줄에서 멈춰야만 "반례 소멸"
#: 이다. 전 판은 패키지 파일 안이면 **아무 AssertionError** 나 닫힘으로 읽었다 — production 이 무관한 불변식
#: (`AssertionError("UNRELATED production invariant")`) 을 던져도 `도달: true · 반례 소멸` 이었다.
COUNTEREXAMPLE_LINES = {
    "snapshot:eval-self-overwrite": ('assert rc == 0 and result["original_destroyed"]',),
    "snapshot:profile-partial": ('assert rc == 0 and len(rows) == 1 and not problems',),
    "snapshot:matrix-errors": ("assert rc_obj is None and rows and problems",),
    "snapshot:stdout-invalid": ("assert rc_obj is None and problems and isinstance(j, dict)",),
    "snapshot:receipt-roles": ('assert result["same_aggregate"] and not result["validator_swapped"]',),
    "snapshot:error-skip": ('assert p.returncode == 0 and not result["direct_schema_problems"]',),
    "snapshot:argv": ('assert result["same_recorded_argv"] and result["different_execution"]',),
    "u18:same_root": ('assert p.returncode == 0 and result["claims_all_same"]',),
    "u18:receipt_roles": ('assert p.returncode == 0 and result["claims_schema_complete"]',),
    "u18:controls": ('assert p.returncode == 0 and records[mode]["claims_all_same"]',
                     'assert not records[mode]["reports_control_mismatch"]'),
    "u18:error_bypass": ('assert result["provenance_cells_blank"]',
                         'assert p.returncode == 0 and result["claims_schema_complete"]'),
    "u18:shape_subset": ('assert rc1 == 0 and [r["state"] for r in rows1] == ["100", "200"]',
                         'assert rc2 == 0 and [r["state"] for r in rows2] == ["100"]',
                         'assert meta2["status"] == "complete" and result["canonical_replaced"]'),
    "u18:shape_duplicates": ('assert rc == 0 and result["rows"] == ["100", "100"]',
                             'assert meta["pairing"]["requested"] == ["100", "100"]'),
}


def child_ok(proc) -> bool:
    """자식 프로세스의 결과를 **받아들일 수 있는가** (Codex R11 P1-11).

    전 판은 stdout 의 JSON 만 parse 하고 rc 를 안 봤다 — checksum 에 든 evidence probe 일곱 개가 전부 rc 7 로
    죽었는데 기대 boolean 만 찍혀 있으면 parent 가 `closed: true · evidence_eligible: true` 를 냈다. rc 0 이
    아니면(비영·signal·timeout) 그 실행은 증거가 아니다.
    """
    rc = getattr(proc, "returncode", None)
    return rc == 0


def _classify(fn, pkg_dir, case_key=None):
    """원본 case 를 돌린다 → 도달·상태·멈춘_곳.

    **자기 반례 assertion** 에서 멈췄을 때만 반례 소멸이다 (Codex R11 P1-12). `case_key` 가 봉인 표에 있으면 멈춘
    소스 줄이 그 case 의 fingerprint 중 하나여야 하고, 아니면 오류로 적는다 — 어디서 왜 멈췄는지 같이 남긴다.
    """
    buf = io.StringIO()
    want = COUNTEREXAMPLE_LINES.get(case_key or "")
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            detail = fn()
        return {"도달": True, "상태": "재현", "멈춘_곳": None, "세부": str(detail)[:400]}
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
                    "세부": f"이 case 의 반례 assertion 이 아니다 (기대 {list(want)}): {str(e)[:200]}"}
        return {"도달": True, "상태": "반례 소멸", "멈춘_곳": where, "세부": str(e)[:400]}
    except BaseException:                                                  # noqa: BLE001
        tb = traceback.format_exc().strip().splitlines()
        return {"도달": False, "상태": "오류", "멈춘_곳": tb[-1][:300], "세부": "반례 assertion 전에 예외"}


def adapted_argv_vector(target):
    """`argv` case 의 우리 쪽 대응 — production 이 `$*` 를 안 쓰고 sidecar 가 vector 를 담는가 (Codex R10 P2-3)."""
    src = (target / "scripts/run_states.sh").read_text(encoding="utf-8")
    flat = 'LAST_ARGV="$*"' in src
    vector = src.count('LAST_ARGV_JSON="$(') == 1
    gate.need(not flat and vector, "run_states.sh 가 아직 argv 를 평탄화한다", {"flat": flat, "vector": vector})
    return {"flat_form_gone": not flat, "vector_form": vector,
            "closure_assert": 'assert not `LAST_ARGV="$*"` and one `LAST_ARGV_JSON="$("'}


def adapted_duplicate_states(target, shape_harness, pair):
    """u18 `shape_duplicates` 의 적응판 — 원본은 canonical 이 없을 때 meta 를 읽다 죽는다 (그 자체가 닫힘의 결과)."""
    import pytest, tempfile
    with tempfile.TemporaryDirectory(prefix="r10-adapt-dup-") as td:
        base = pathlib.Path(td); matrix, out = base / "matrix", base / "shape"; matrix.mkdir()
        mp = pytest.MonkeyPatch()
        try:
            ns = shape_harness(mp, base, {"pristine": 0.0, "100": 0.01, "200": 0.10})
            mp.setattr(ns.D, "HALF_FILE", {"GITT": {"pristine": "p", "100": "a", "200": "b"}})
            pair(matrix, "100")
            buf = io.StringIO()
            mp.setattr(sys, "argv", ["ne_shape.py", "--out-dir", str(matrix), "--write", str(out), "--states", "100,100"])
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                rc = ns.main()
            text = buf.getvalue()
            published = list(out.rglob("ne_shape_*.csv"))
            gate.need(rc == 2 and "중복" in text and not published,
                      "중복 요청 상태를 거부하지 않는다", {"rc": rc, "published": [str(x) for x in published]})
            return {"rc": rc, "published": [], "closure_assert": 'assert rc == 2 and "중복" in text and 게시 없음'}
        finally:
            mp.undo()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=pathlib.Path, required=True)
    ap.add_argument("--expected-head", required=True, metavar="SHA")
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
        # ⚠ Codex R11 P2-6: full 40 자 object id 만 받는다
        exp = gate.full_head(target, a.expected_head)
        if head != exp:
            print(f"! HEAD mismatch — expected {exp}, 실제 {head} (다르다) — 돌리지 않았다", file=sys.stderr)
            return 2
        tree = gate.tree_of(target, head)
        dirty = gate.dirty_paths(target)
        skipped = gate.index_skip_flags(target)
        if skipped:
            print(f"! index skip flag: {skipped[:10]}", file=sys.stderr)
            return 2
        gate.isolate_bytecode()
        sealed, seal_detail = gate.instrument_sealed(target, INSTRUMENT)
        if not a.allow_dirty:
            snapshot, cleanup = gate.materialize(target, head, keep=a.keep_materialized)
            # ⚠ Codex R11 P1-10 반례 B: checkout 은 filter(smudge)·eol 을 거친다 — 풀린 bytes 를 blob 과 다시 댄다
            drift = gate.verify_snapshot_bytes(snapshot, head)
            if drift:
                raise gate.EvidenceError("snapshot 의 bytes 가 expected commit 의 blob 과 다르다 "
                                         f"(checkout filter/smudge?): {drift[:5]}")
            target = snapshot
            globals()["PKG"] = snapshot / PKG_REL
            globals()["SUMS"] = snapshot / PKG_REL / SUMS_NAME
    except gate.EvidenceError as e:
        print(f"! {e}", file=sys.stderr)
        return 2

    digest_ok, digest = gate.package_digest(PKG, SUMS)
    out = {"target_head": head, "expected_head": exp, "expected_tree": tree,
           "pinned_sha": PINNED, "pin_bypassed": True,
           "dirty": bool(dirty), "dirty_allowed": bool(a.allow_dirty),
           "evidence_eligible": bool(snapshot) and digest_ok and sealed,
           "instrument_sealed": sealed, "instrument": seal_detail,
           "materialized": ({"path": str(snapshot), "head": head, "kept": bool(a.keep_materialized)}
                            if snapshot else None),
           "ran_in": "격리 snapshot" if snapshot else "working tree (--allow-dirty)",
           "package_digest_ok": digest_ok, "package_digest": digest,
           "설명": "원본 case 함수를 직접 불러 SHA pin 을 우회한다. assert 하는 두 스크립트는 자기 반례 assertion 에서 "
                 "멈추면 닫힘, field 로 말하는 evidence 스크립트는 그 flag 가 False 면 닫힘",
           "probes": {}}
    if not digest_ok:
        out["오류"] = "패키지 bytes 가 SHA256SUMS 와 다르다 — probe 를 돌리지 않았다"
        print(json.dumps(out, ensure_ascii=False, indent=2))
        if cleanup:
            cleanup()
        return 2

    os.environ["PATH"] = str(pathlib.Path(sys.executable).parent) + os.pathsep + os.environ.get("PATH", "")
    R = out["probes"]
    try:
        snap_mod = _load("r10c_snapshot", PKG / "r10_snapshot_repros.py")
        for name, fn in snap_mod.CASES.items():
            rec = _classify(lambda f=fn: f(target), PKG, f"snapshot:{name}")
            if name in LANGUAGE_LEVEL and rec["상태"] == "재현":
                rec["상태"] = "우리 코드 밖"
                rec["세부"] = "bash 의 `$*` 의미 자체를 보이는 case — 우리 쪽 닫힘은 적응 probe `argv-vector` 가 본다"
            R[f"snapshot:{name}"] = rec

        u18 = _load("r10c_u18", PKG / "r10_u18_shape_repros.py")
        t2, S2, verify2, sign2, full_rows2, pair2, shape2 = u18.boot(target)
        u18_cases = {
            "same_root": lambda: u18.same_root_is_vacuous(t2, verify2, sign2, full_rows2),
            "receipt_roles": lambda: u18.receipt_role_roster_is_not_checked(t2, S2, verify2, sign2, full_rows2),
            "controls": lambda: u18.environment_and_controls_are_not_closed(t2, verify2, sign2, full_rows2),
            "error_bypass": lambda: u18.error_column_bypasses_row_validation(t2, S2, verify2, sign2, full_rows2),
            "shape_subset": lambda: u18.states_subset_replaces_complete_canonical(pair2, shape2),
            "shape_duplicates": lambda: u18.duplicate_requested_states_are_complete(pair2, shape2),
        }
        for name, fn in u18_cases.items():
            R[f"u18:{name}"] = _classify(fn, PKG, f"u18:{name}")

        # ⚠ evidence 묶음은 **자식 프로세스**로 돌린다. 그 probe 들은 `importlib.util.cache_from_source` 의 기본
        #   위치에 위조 pyc 를 놓는 식으로 자기 기법을 만드는데, 우리 러너가 프로세스 전역에 pycache prefix 를
        #   걸어 두면 그 기법 자체가 성립하지 않는다 (닫힘이 아니라 측정 불가가 된다). 리뷰어가 돌린 방식 그대로.
        ev_env = {k: v for k, v in os.environ.items() if k != "PYTHONPYCACHEPREFIX"}
        for name, flag in EVIDENCE_FLAGS.items():
            proc = subprocess.run([sys.executable, str(PKG / "r10_evidence_repros.py"),
                                   "--target", str(target), "--case", name],
                                  cwd=str(target), capture_output=True, text=True, env=ev_env, timeout=1800)
            if not child_ok(proc):                 # ⚠ Codex R11 P1-11: payload 를 **읽기 전에** rc 를 본다
                R[f"evidence:{name}"] = {"도달": False, "상태": "오류",
                                         "멈춘_곳": f"child rc {proc.returncode} — 이 실행은 증거가 아니다 (R11 P1-11)",
                                         "세부": (proc.stderr.strip()[-300:] or proc.stdout[-300:] or "출력 없음")}
                continue
            try:
                got = json.loads(proc.stdout)["cases"][name]
            except (json.JSONDecodeError, KeyError):
                R[f"evidence:{name}"] = {"도달": False, "상태": "오류", "멈춘_곳": (proc.stderr.strip()[-300:] or "출력 없음"),
                                         "세부": proc.stdout[-400:]}
                continue
            closed = got.get(flag) is False
            R[f"evidence:{name}"] = {"도달": True, "상태": "반례 소멸" if closed else "재현",
                                     "멈춘_곳": f"{flag} = {got.get(flag)}",
                                     "세부": {k: v for k, v in got.items() if k != "git_status_porcelain"}}

        R["adapted:argv-vector"] = {"적응": True, **_run_adapted(lambda: adapted_argv_vector(target))}
        R["adapted:duplicate-states"] = {"적응": True,
                                         **_run_adapted(lambda: adapted_duplicate_states(target, shape2, pair2))}
    finally:
        if cleanup and not a.keep_materialized:
            cleanup()

    for key, why in PREMISE_CHANGED.items():
        if key in R and R[key]["상태"] == "오류":
            R[key] = {**R[key], "상태": "전제 변경", "세부": why}
    statuses = {k: v["상태"] for k, v in R.items()}
    unresolved = {k: s for k, s in statuses.items() if s not in ("반례 소멸", "우리 코드 밖", "전제 변경")}
    out["closed"] = not unresolved
    out["rc_reason"] = "모든 case 가 닫혔다" if out["closed"] else f"닫히지 않음: {unresolved}"
    text = json.dumps(out, ensure_ascii=False, indent=2, default=str)
    print(text)
    if a.output:
        a.output.write_text(text + "\n", encoding="utf-8")
    # ⚠ 자체 리뷰 C19: `evidence_eligible: false` 인 실행이 rc 0 으로 끝났다 — P1-11 이 자식에게 요구한 규율
    #   ("payload 를 읽기 전에 rc 를 본다")을 러너 자신이 어긴 것이다. 증거가 아닌 실행은 성공 코드로 끝나지 않는다.
    if not out["evidence_eligible"]:
        return 3
    return 0 if out["closed"] else 1


def _run_adapted(fn):
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            d = fn()
        return {"도달": True, "상태": "반례 소멸", "멈춘_곳": d.pop("closure_assert", None), "세부": d}
    except gate.EvidenceError as e:
        return {"도달": True, "상태": "재현", "멈춘_곳": "closure 조건이 서지 않았다", "세부": str(e)[:400]}
    except BaseException:                                                  # noqa: BLE001
        tb = traceback.format_exc().strip().splitlines()
        return {"도달": False, "상태": "오류", "멈춘_곳": tb[-1][:300], "세부": "도달 전에 예외"}


if __name__ == "__main__":
    sys.exit(main())
