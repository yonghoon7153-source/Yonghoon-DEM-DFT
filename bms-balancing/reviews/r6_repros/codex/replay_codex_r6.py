"""Codex R6 재현 패키지를 **우리 트리에서** 다시 돌린다 — 발견별로 따로, 한 건이 죽어도 나머지를 본다.

받은 원본(`harness_r6_final_*.py`)은 한 스크립트가 여러 probe 를 순서대로 돌고 첫 실패에서 멈춘다. 닫은 뒤의 트리에서는
첫 probe 가 바로 실패하므로 나머지가 안 보인다 — 그래서 probe 를 하나씩 부르고 예외를 잡아 기록한다. **probe 코드는
원본 그대로**(import 해서 호출), 이 파일이 하는 일은 호출·격리·판정 기록뿐이다.

읽는 법: `재현` = 발견이 그 트리에 아직 있다 · `안 재현` = probe 의 assertion 이 깨졌다(닫혔거나 fixture 가 더는
성립하지 않는다 — `detail` 에 이유) · `기대대로`/`달라짐` = 닫힘 확인용 probe (port·inference).

    python3 replay_codex_r6.py --target <bms-balancing> --old <bfc4623^ 의 out> --output <json>
"""
from __future__ import annotations
import argparse, importlib.util, io, json, pathlib, subprocess, sys, tempfile, traceback, contextlib

HERE = pathlib.Path(__file__).resolve().parent


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def _guard(fn):
    """probe 하나 → (상태, 세부). 출력은 삼키고 예외는 마지막 줄만 남긴다."""
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            return "재현", fn()
    except BaseException:                                        # noqa: BLE001 — 어떤 실패든 판정 자료다
        tb = traceback.format_exc().strip().splitlines()
        where = [l.strip() for l in tb if l.strip().startswith("File ")][-1:] or [""]
        return "안 재현", {"error": tb[-1][:400], "at": where[0][:200]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=pathlib.Path, required=True, help="bms-balancing 디렉터리")
    ap.add_argument("--old", type=pathlib.Path, help="bfc4623^ 의 out (inference u14/table 용)")
    ap.add_argument("--output", type=pathlib.Path)
    a = ap.parse_args()
    target = a.target.resolve()
    sys.path.insert(0, str(target)); sys.path.insert(0, str(target / "scripts"))
    head = subprocess.check_output(["git", "-C", str(target), "rev-parse", "HEAD"], text=True).strip()

    ex = _load("r6_codex_exec", HERE / "harness_r6_final_execution_repros.py")
    cl = _load("r6_codex_claims", HERE / "harness_r6_final_claims_repros.py")
    from bms_balancing import verify as v                        # noqa: E402 — target 트리의 것
    import provenance as pv                                      # noqa: E402
    reader = ex.load("r6_reader", target / "scripts/compare_states.py")
    shape = ex.load("r6_shape", target / "scripts/ne_shape.py")

    out: dict = {"target_head": head, "probes": {}}
    with tempfile.TemporaryDirectory(prefix="r6-codex-replay-") as tmp:
        root_of = lambda n: (pathlib.Path(tmp) / n, (pathlib.Path(tmp) / n).mkdir())[0]
        probes = [
            ("R6-01a snapshot_metadata_mix", lambda: ex.metadata_sample_mix(target, root_of("p1"), v, pv, reader)),
            ("R6-01b matrix_after_verification", lambda: ex.matrix_after_verification(target, root_of("p2"), v, pv, reader)),
            ("R6-02 missing_modern_metadata", lambda: ex.missing_modern_metadata(target, root_of("p3"), v, pv, reader, shape)),
            ("R6-04 old_version_selected", lambda: ex.old_version_selected(target, root_of("p4"), pv, reader)),
            ("R6-03a shape_and_matrix", lambda: cl.shape_and_matrix(target)),
            ("R6-03b fullcell_build_signature", lambda: cl.fullcell_build_signature(target)),
            ("R6-05 role_checks", lambda: cl.role_checks(target)),
        ]
        for name, fn in probes:
            st, detail = _guard(fn)
            out["probes"][name] = {"상태": st, "세부": detail}

    # port·inference 는 닫힘 확인용 — 원본 스크립트를 그대로 돌려 rc 만 본다
    for name, script, extra in (("port(닫힘 확인)", "harness_r6_final_port_repros.py", []),
                                ("inference(닫힘 확인)", "harness_r6_final_inference_repros.py",
                                 ["--old", str(a.old.resolve())] if a.old else [])):
        r = subprocess.run([sys.executable, str(HERE / script), "--target", str(target)] + extra,
                           capture_output=True, text=True)
        out["probes"][name] = {"상태": "기대대로" if r.returncode == 0 else "달라짐",
                               "세부": {"rc": r.returncode,
                                        "error": (r.stderr.strip().splitlines() or [""])[-1][:400]}}
    text = json.dumps(out, ensure_ascii=False, indent=2)
    print(text)
    if a.output:
        a.output.write_text(text + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
