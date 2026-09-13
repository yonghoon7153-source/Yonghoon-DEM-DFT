"""R7 패키지 probe 의 **닫힘 재생기** (Codex R8-07) — 보관한 원본 probe 는 SHA(521be85) 를 고정해 두어 현재 트리에서는
첫 assertion 에서 rc 1 이다. 그것은 옳지만 "수정 뒤 각 probe 가 자기 반례 assertion 에서 실패한다" 를 재생할 명령이
없었다. 이 러너는 원본 probe 함수를 **직접** 불러(pin 우회) 세 가지를 따로 기록한다:

  · 도달   — 대상 검증·fixture 를 지나 실제 반례 case 에 닿았는가 (probe 별 반례 assertion 줄 목록으로 판정)
  · 상태   — `재현`(반례가 아직 있다) · `반례 소멸`(자기 반례 assertion 에서 멈췄다) · `오류`(도달 전에 죽었다)
  · 멈춘_곳 — 실패한 소스 줄 (있으면)

R7-05·06 은 원본 probe 가 옛 내부 이름(`M`, baseline 기본값)에 묶여 있어 현행 API 로 **적응**한 positive-closure
검사를 같이 둔다 (`적응` 필드가 True 인 항목). 원본 파일은 건드리지 않는다.

⚠ Codex R9 P2-1: 전 판은 `--probes DOES_NOT_EXIST` 를 조용히 버리고 `probes: {}` rc 0 — 아무것도 안 돌린 실행이
  "반례 소멸" 로 읽혔다. 빈 이름·오타·중복·valid+unknown 은 전부 거부하고, 출력의 probe 집합은 요청 집합과 같아야 한다.
⚠ Codex R9 P2-2: 전 판은 대상 SHA·clean 여부·패키지 bytes 를 대조하지 않아 임의 HEAD 의 임의 트리에서도 rc 0 이었다.
  `--expected-head` 가 필수이고(불일치면 돌지 않는다), working tree 가 dirty 면 기본으로 거부한다(`--allow-dirty` 는
  목록을 기록하고 돌린다), 패키지 파일은 `HARNESS_R7_521BE85_SHA256SUMS.txt` 와 대조한다. 종료 코드는 재현·오류·
  mismatch·digest 불일치 중 하나라도 있으면 0 이 아니다.

    python3 reviews/r7_repros/replay_codex_r7.py --target <bms-balancing> --expected-head <sha> \\
        [--probes R7-01,R7-06] [--allow-dirty] [--output x.json]
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

import argparse, contextlib, hashlib, importlib.util, io, json, os, pathlib, subprocess, sys, tempfile, traceback

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
import evidence_gate as gate                                              # noqa: E402  — 증거 gate 는 한 자리 (R10 P2-4·P2-5)
HERE = pathlib.Path(__file__).resolve().parent
PKG = HERE / "codex"
PINNED = "521be85e74acef80feec45bd147dd339e25b8d0a"
PKG_REL = "reviews/r7_repros/codex"
SUMS_NAME = "HARNESS_R7_521BE85_SHA256SUMS.txt"
SUMS = PKG / SUMS_NAME
#: 증거를 만드는 **도구** — expected commit 과 같아야 그 증거가 그 커밋의 것이다 (Codex R10 P2-5)
INSTRUMENT = ("reviews/r7_repros/replay_codex_r7.py", "reviews/evidence_gate.py")
KNOWN_PROBES = ("R7-01", "R7-02", "R7-03", "R7-04", "R7-05", "R7-06")

# probe 별 "반례 assertion" 의 소스 조각 — 이 줄에서 멈추면 case 에 **도달**한 것이다
COUNTEREXAMPLE_LINES = {
    "R7-01": ('assert partial["rc"] == 0', 'assert empty_run["rc"] == 0'),
    "R7-02": ('assert A["sigma_at_k1_V"]!=mixed["sigma_at_k1_V"]',),
    "R7-03": ('assert not any("ref" in k', 'assert A["inputs_sha"]==B["inputs_sha"]'),
    "R7-04": ('assert p.returncode == 0',),
}


#: 수정이 원본 probe 의 전제를 무너뜨려 반례 assertion **전에** 죽는 case — (설명, fingerprint).
#: fingerprint 는 멈춘 자리의 문자열 조각이고, 전부 맞아야 전제 변경으로 적는다.
PREMISE_CHANGED = {
    "R7-03": ("Codex R11 P1-2 뒤: 원본 probe 의 fixture 는 한 조합만 도는 **좁힌** matrix 실행이라 이제 subset 이고 "
              "canonical(`A.csv`) 자리에 파일이 없다 — 원본은 그 파일을 무조건 열어 죽는다. 같은 축(행이 기준 입력 "
              "서명을 담는가)은 회귀 `test_d7_03` 이 `publish_target` 로 자리를 맞춰 본다",
              ("A.csv", "No such file or directory")),
}


def parse_probes(text):
    return gate.parse_probes(text, KNOWN_PROBES)


def package_digest():
    return gate.package_digest(PKG, SUMS)


def dirty_paths(target):
    return gate.dirty_paths(target)


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def _run_adapted(fn):
    """적응 probe: positive-closure assert 가 **서면** 반례 소멸, 깨지면 반례 재현, 그 밖의 예외는 오류."""
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            d = fn()
        return {"도달": True, "상태": "반례 소멸", "멈춘_곳": d.get("closure_assert"), "세부": {k: v for k, v in d.items() if k != "closure_assert"}}
    except AssertionError as e:
        return {"도달": True, "상태": "재현", "멈춘_곳": "positive-closure assert 가 깨졌다", "세부": str(e)[:400]}
    except BaseException:                                              # noqa: BLE001
        tb = traceback.format_exc().strip().splitlines()
        return {"도달": False, "상태": "오류", "멈춘_곳": tb[-1][:300], "세부": "도달 전에 예외"}


def _run_probe(pid, fn):
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            detail = fn()
        return {"도달": True, "상태": "재현", "멈춘_곳": None, "세부": str(detail)[:400]}
    except AssertionError:
        tb = traceback.extract_tb(sys.exc_info()[2])
        frames = [f for f in tb if str(PKG) in (f.filename or "")]
        line = (frames[-1].line or "").strip() if frames else ""
        reached = any(sn in line for sn in COUNTEREXAMPLE_LINES.get(pid, ()))
        return {"도달": reached, "상태": "반례 소멸" if reached else "오류",
                "멈춘_곳": f"{pathlib.Path(frames[-1].filename).name}:{frames[-1].lineno}: {line}" if frames else "?",
                "세부": ("자기 반례 assertion 에서 멈췄다" if reached else "반례 case 전에 assertion 이 깨졌다 — 원본 probe 의 전제가 현행 트리와 다르다")}
    except BaseException as e:                                          # noqa: BLE001
        tb = traceback.format_exc().strip().splitlines()
        return {"도달": False, "상태": "오류", "멈춘_곳": tb[-1][:300], "세부": "도달 전에 예외"}


def r7_05_adapted(target):
    """R7-05 (baseline 기본값): 원본은 `default_environment` rc 1 을 assert 한다 — 현행은 R6_OLD_OUT 없이 `mode: 부분` rc 0."""
    prog = target / "reviews/r6_repros/codex/replay_codex_r6_adapted.py"
    env = dict(os.environ); env.pop("R6_OLD_OUT", None)
    r = subprocess.run([sys.executable, str(prog), "--target", str(target)], capture_output=True, text=True, env=env, cwd=target)
    rep = json.loads(r.stdout) if r.stdout.strip().startswith("{") else {}
    mode = rep.get("mode", "")
    closure = 'assert r.returncode == 0 and mode.startswith("부분")'                # positive closure
    gate.need(r.returncode == 0 and mode.startswith("부분"), "R7-05 적응 닫힘이 서지 않는다", (r.returncode, mode))
    return {"rc": r.returncode, "mode": mode, "baseline": rep.get("baseline"), "closure_assert": closure}


def r7_06_adapted(target):
    """R7-06 (MISSED 에 rc 0): 원본은 옛 내부 이름 `M` 을 잘라 넣는다 — 현행 `MUTATIONS` 로 같은 대조를 한다."""
    prog = target / "reviews/r6_repros/codex_r6_mutation_audit.py"
    code = ("import importlib.util,sys\n"
            f"p={str(prog)!r}\n"
            "s=importlib.util.spec_from_file_location('audit_ctl',p)\n"
            "m=importlib.util.module_from_spec(s);s.loader.exec_module(m)\n"
            "old='MODES = (\"LAM_PE\", \"LAM_NE\", \"LLI\")'\n"
            "m.MUTATIONS=[('semantic no-op','c6_04','scripts/compare_states.py',old,old+'  # no-op')]\n"
            "sys.exit(m.main())\n")
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, cwd=target)
    closure = 'assert "MISSED: 1" in r.stdout and r.returncode != 0'                 # positive closure
    gate.need("MISSED: 1" in r.stdout and r.returncode != 0, "MISSED 에 비영 종료가 서지 않는다",
              (r.returncode, r.stdout[-300:]))
    return {"rc": r.returncode, "tail": r.stdout.strip().splitlines()[-2:], "closure_assert": closure}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=pathlib.Path, required=True)
    ap.add_argument("--probes", default=",".join(KNOWN_PROBES))
    ap.add_argument("--expected-head", required=True, metavar="SHA",
                    help="이 SHA 에서 돌아야 한다 — 대상 HEAD 가 다르면 돌지 않는다 (Codex R9 P2-2)")
    ap.add_argument("--allow-dirty", action="store_true",
                    help="격리 snapshot 없이 **현재 working tree 에서** 돌린다 (개발용). 결과는 `evidence_eligible: false` "
                         "로 표시되고 증거로 세지 않는다 (Codex R10 Q4)")
    ap.add_argument("--keep-materialized", type=pathlib.Path, default=None, metavar="DIR",
                    help="격리 snapshot 을 지우지 않고 이 자리에 남긴다 (회귀가 들여다본다)")
    ap.add_argument("--output", type=pathlib.Path)
    a = ap.parse_args()
    snapshot = cleanup = None
    try:
        gate.require_assertions()                       # Codex R10 P2-4: `-O` 에서는 증거를 만들지 않는다
        target = a.target.resolve()
        want, problems = parse_probes(a.probes)
        if problems:
            print("! --probes 거부: " + "; ".join(problems) + " — 아무것도 돌리지 않았다 (Codex R9 P2-1)", file=sys.stderr)
            return 2
        head = gate.git_head(target)                    # Codex R10 P2-5: git 의 rc 를 본다
        # ⚠ Codex R11 P2-6: prefix 는 커밋 하나를 지목하지 못한다 — full 40 자만 받고 exact 로 댄다
        exp = gate.full_head(target, a.expected_head)
        if head != exp:
            print(f"! HEAD mismatch — expected {exp}, 실제 {head}: 이 트리는 요청한 대상이 아니다 (다르다) — "
                  f"돌리지 않았다 (Codex R9 P2-2)", file=sys.stderr)
            return 2
        tree = gate.tree_of(target, head)
        dirty = gate.dirty_paths(target)
        skipped = gate.index_skip_flags(target)
        if skipped:
            print(f"! index 에 skip flag 가 걸린 tracked 파일이 있다 — 그 bytes 는 status 에 안 잡힌다: "
                  f"{skipped[:10]} (Codex R10 P2-5)", file=sys.stderr)
            return 2
        gate.isolate_bytecode()                         # 이미 놓인 __pycache__ 를 읽지 않는다 (P2-5 반례 C)
        sealed, seal_detail = gate.instrument_sealed(target, INSTRUMENT)
        if not a.allow_dirty:
            # ⚠ Codex R10 P2-5: 대상 bytes 를 expected commit 에서 새로 materialize 한다 — 아래 probe·패키지·
            #   production 코드는 전부 이 snapshot 것이다.
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
    digest_ok, digest = package_digest()
    out = {"target_head": head, "expected_head": exp, "expected_tree": tree, "head_ok": True,
           "dirty": bool(dirty), "dirty_allowed": bool(a.allow_dirty), "dirty_paths": dirty[:50],
           # ⚠ Codex R10 P2-5 · Q4: 증거로 셀 수 있는 실행은 expected commit 의 격리 snapshot 에서, 도구도 그 커밋의
           #   bytes 로 돈 것뿐이다. `--allow-dirty` 는 개발용이고 구조적으로 증거가 아니다.
           "evidence_eligible": bool(snapshot) and digest_ok and sealed,
           "instrument_sealed": sealed, "instrument": seal_detail,
           "materialized": ({"path": str(snapshot), "head": head, "mode": "sparse detached worktree",
                             "kept": bool(a.keep_materialized)} if snapshot else None),
           "ran_in": "격리 snapshot" if snapshot else "working tree (--allow-dirty)",
           "package_digest_ok": digest_ok, "package_digest": digest,
           "pinned_sha": PINNED, "pin_bypassed": True,
           "설명": "원본 probe 함수를 직접 불러 SHA pin 을 우회한다 — 도달·상태·멈춘_곳을 따로 적는다 (Codex R8-07); "
                 "요청 집합·대상 SHA·clean·패키지 digest 를 대조한다 (Codex R9 P2-1·2)",
           "requested": want, "probes": {}}
    if not digest_ok:
        out["오류"] = "패키지 bytes 가 SHA256SUMS 와 다르다 — probe 를 돌리지 않았다"
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 2
    sys.path.insert(0, str(target)); sys.path.insert(0, str(target / "scripts"))
    os.environ["PATH"] = str(pathlib.Path(sys.executable).parent) + os.pathsep + os.environ.get("PATH", "")
    ex = _load("r7c_exec", PKG / "harness_r7_execution_repros.py")
    cl = _load("r7c_claims", PKG / "harness_r7_claims_repros.py")
    inf = _load("r7c_inf", PKG / "harness_r7_inference_repros.py")
    from bms_balancing import verify as v                                # noqa: E402
    import provenance as pv                                              # noqa: E402
    with tempfile.TemporaryDirectory(prefix="r7-closure-") as tmp:
        root = pathlib.Path(tmp) / "agg"; root.mkdir()
        probes = {
            "R7-01": ("aggregate_completeness", lambda: ex.aggregate_completeness(target, root, v, pv)),
            "R7-02": ("noise_reopen", lambda: cl.noise_reopen(target)),
            "R7-03": ("matrix_reference_omission", lambda: cl.matrix_reference_omission(target)),
            "R7-04": ("r7_baseline_policy_split", lambda: inf.r7_baseline_policy_split(target)),
        }
        for pid in want:
            if pid in probes:
                name, fn = probes[pid]
                out["probes"][pid] = {"probe": name, "적응": False, **_run_probe(pid, fn)}
            elif pid == "R7-05":
                out["probes"][pid] = {"probe": "adapted_runs(적응)", "적응": True, **_run_adapted(lambda: r7_05_adapted(target))}
            elif pid == "R7-06":
                out["probes"][pid] = {"probe": "missed_exit_control(적응)", "적응": True, **_run_adapted(lambda: r7_06_adapted(target))}
    if snapshot is not None and not a.keep_materialized:
        cleanup()
    # ⚠ 수정이 원본 probe 의 **전제를 무너뜨린** case — 봉인한 fingerprint 와 맞을 때만 그렇게 적는다
    #   (아무 예외나 "전제 변경" 으로 읽으면 그것도 증거 위조다).
    for pid, (why, fingerprint) in PREMISE_CHANGED.items():
        rec = out["probes"].get(pid)
        if rec and rec["상태"] == "오류" and all(w in str(rec.get("멈춘_곳") or "") for w in fingerprint):
            out["probes"][pid] = {**rec, "상태": "전제 변경", "세부": why}
    statuses = {pid: r["상태"] for pid, r in out["probes"].items()}
    ok = ("반례 소멸", "전제 변경")
    out["closed"] = list(out["probes"]) == want and all(s in ok for s in statuses.values())
    out["rc_reason"] = ("모든 요청 probe 가 자기 반례 assertion 에서 멈췄다 (전제가 바뀐 것은 그렇게 적었다)"
                        if out["closed"]
                        else f"닫히지 않음: { {p: s for p, s in statuses.items() if s not in ok} }")
    text = json.dumps(out, ensure_ascii=False, indent=2)
    print(text)
    if a.output:
        a.output.write_text(text + "\n", encoding="utf-8")
    # ⚠ 자체 리뷰 C19: `evidence_eligible: false` 인 실행이 rc 0 으로 끝났다 — P1-11 이 자식에게 요구한 규율
    #   ("payload 를 읽기 전에 rc 를 본다")을 러너 자신이 어긴 것이다. 증거가 아닌 실행은 성공 코드로 끝나지 않는다.
    if not out["evidence_eligible"]:
        return 3
    return 0 if out["closed"] else 1


if __name__ == "__main__":
    sys.exit(main())
