"""R7 result-snapshot closures and public aggregate completeness, synthetic records only."""
from __future__ import annotations
import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from unittest.mock import patch


def load(name, path):
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def fixture(target, root):
    (root / "scripts").mkdir()
    (root / "out").mkdir()
    shutil.copyfile(target / "scripts/provenance.py", root / "scripts/provenance.py")
    (root / "code.py").write_text("value = 1\n", encoding="utf-8")
    git = ["git", "-C", str(root)]
    subprocess.run(git + ["init", "-q"], check=True, capture_output=True)
    subprocess.run(git + ["add", "."], check=True, capture_output=True)
    subprocess.run(git + ["-c", "user.name=R7 Review", "-c", "user.email=r7@example.invalid",
                         "commit", "-qm", "synthetic fixture"], check=True, capture_output=True)


def write_meta(target, root, art, rid, state="100"):
    text = (target / "scripts/run_states.sh").read_text(encoding="utf-8")
    code = (text[text.index("write_meta ()"):text.index('\nmkdir -p "$OUT"')] + "\n" +
            text[text.index("say ()"):text.index("\nfail=0")] +
            '\nLAST_RUN_ID="$2"; write_meta "$1" "$3" GITT\n')
    env = dict(os.environ, STARTS="24", SI="Li", BMS_DATA_ROOT="synthetic", OUT=str(root / "out"))
    proc = subprocess.run(["bash", "-c", code, "r7", str(art), rid, state], cwd=root,
                          env=env, capture_output=True, text=True, timeout=30)
    assert proc.returncode == 0, (proc.stdout, proc.stderr)


def deg(state, rid, spans):
    return {
        "run_id": rid, "state": state, "half_cell": "GITT", "si_source": "Li", "n_starts": 24,
        "best_modes_percent": {m: 0.0 for m in spans},
        **{m + "_percent": {"min": 0.0, "max": v, "span": v, "is_lower_bound": True}
           for m, v in spans.items()},
    }


def matrix(rid, width):
    return [dict(run_id=rid, half_cell="GITT", si=si, w_dqdv=0,
                 gamma_Si=.16, ref_gamma_Si=.15, bounds="-", ref_bounds="-",
                 LAM_PE_pct=i * width, LAM_NE_pct=i * width, LLI_pct=i * width)
            for i, si in enumerate(("Li", "Kunz"))]


def snapshot_cases(target, root, v, pv, cs):
    fixture(target, root)
    results = []
    for kind in ("json", "csv"):
        for timing in ("before_data", "after_data", "before_meta", "after_meta", "after_verify"):
            for how in ("complete", "data_only"):
                out = root / "out" / f"{kind}_{timing}_{how}"
                out.mkdir()
                art = out / ("degeneracy_100_Li.json" if kind == "json" else "matrix_100.csv")
                mp = Path(str(art) + ".meta.json")

                def publish(rid, val, complete=True):
                    if kind == "json":
                        v.atomic_write_json(art, deg("100", rid, {"LAM_PE": val, "LAM_NE": val, "LLI": val}))
                    else:
                        rows = matrix(rid, val)
                        v.atomic_write_csv(art, rows, list(rows[0]))
                    if complete:
                        write_meta(target, root, art, rid)

                publish("attempt-A", 3.0)
                assert pv.verify_unit(art)[0] is True
                fired = False
                real_bytes, real_text, real_verify = Path.read_bytes, Path.read_text, pv.verify_unit_bytes

                def fire():
                    nonlocal fired
                    if not fired:
                        fired = True
                        publish("attempt-B", 79.0, how == "complete")

                def read_bytes(p, *a, **kw):
                    if p == art and timing == "before_data":
                        fire()
                    data = real_bytes(p, *a, **kw)
                    if p == art and timing == "after_data":
                        fire()
                    return data

                def read_text(p, *a, **kw):
                    if p == mp and timing == "before_meta":
                        fire()
                    txt = real_text(p, *a, **kw)
                    if p == mp and timing == "after_meta":
                        fire()
                    return txt

                def verify_bytes(name, data, meta, rid=None):
                    result = real_verify(name, data, meta, rid)
                    if name == art.name and timing == "after_verify":
                        fire()
                    return result

                with patch.object(Path, "read_bytes", read_bytes), patch.object(Path, "read_text", read_text), \
                     patch.object(pv, "verify_unit_bytes", verify_bytes), contextlib.redirect_stderr(io.StringIO()):
                    got = cs.load_degeneracy(out) if kind == "json" else cs.load_matrix_axis(out)
                assert fired, (kind, timing, how)
                if not got:
                    outcome = "incomplete"
                else:
                    entry = got["100"]
                    rid = entry["j"]["run_id"] if kind == "json" else entry["run_id"]
                    val = entry["j"]["LLI_percent"]["span"] if kind == "json" else entry["per"]["GITT"]["LLI"]
                    assert rid == entry["meta"]["run_id"], entry
                    assert val == {"attempt-A": 3.0, "attempt-B": 79.0}[rid], entry
                    outcome = rid
                results.append(dict(kind=kind, boundary=timing, publication=how, outcome=outcome))
    assert {r["outcome"] for r in results} == {"attempt-A", "attempt-B", "incomplete"}
    return results


def modern_incomplete_controls(target, root, v, pv, cs, ne):
    fixture(target, root)
    out = root / "out"
    jf = out / "degeneracy_100_Li.json"
    mf = out / "matrix_100.csv"
    v.atomic_write_json(jf, deg("100", "modern", {"LAM_PE": 2., "LAM_NE": 3., "LLI": 1.}))
    rows = matrix("modern", 4.0)
    v.atomic_write_csv(mf, rows, list(rows[0]))
    outcomes = []
    for meta_kind in ("absent", "old"):
        if meta_kind == "old":
            for path in (jf, mf):
                Path(str(path) + ".meta.json").write_text('{"starts": 24}\n', encoding="utf-8")
        checks = [pv.verify_unit(path) for path in (jf, mf)]
        with contextlib.redirect_stderr(io.StringIO()):
            assert cs.load_degeneracy(out) == {} and cs.load_matrix_axis(out) == {}
        try:
            ne.fitted_pair_info(out, "100", "GITT", "Li")
        except RuntimeError:
            raised = True
        else:
            raised = False
        assert all(ok is False for ok, _ in checks) and raised
        outcomes.append(dict(meta=meta_kind, unit_checks=checks, all_three_readers_refused=True))
    for path in (jf, mf):
        write_meta(target, root, path, "modern")
    assert all(pv.verify_unit(path)[0] is True for path in (jf, mf))
    # True historical data remain readable: no run_id in original legacy schema.
    legacy = out / "legacy"
    legacy.mkdir()
    legacy_obj = deg("100", "unused", {"LAM_PE": 2., "LAM_NE": 3., "LLI": 1.})
    del legacy_obj["run_id"]
    v.atomic_write_json(legacy / jf.name, legacy_obj)
    legacy_rows = matrix("unused", 4.0)
    for r in legacy_rows:
        del r["run_id"]
    v.atomic_write_csv(legacy / mf.name, legacy_rows, list(legacy_rows[0]))
    assert pv.verify_unit(legacy / jf.name)[0] is None
    assert "100" in cs.load_degeneracy(legacy)
    assert ne.fitted_pair_info(legacy, "100", "GITT", "Li") is not None
    return dict(cases=outcomes, signed_positive=True, true_legacy_compatible=True)


def aggregate_completeness(target, root, v, pv):
    fixture(target, root)
    out = root / "out"
    narrow = out / "degeneracy_100_Li.json"
    wide = out / "degeneracy_200_Li.json"
    v.atomic_write_json(narrow, deg("100", "state100-A", {"LAM_PE": 2., "LAM_NE": 3., "LLI": 1.}))
    v.atomic_write_json(wide, deg("200", "state200-A", {"LAM_PE": 1., "LAM_NE": 2., "LLI": 9.}))
    write_meta(target, root, narrow, "state100-A", "100")
    write_meta(target, root, wide, "state200-A", "200")

    def run(path):
        cmd = [sys.executable, str(target / "scripts/compare_states.py"), "case=" + str(path)]
        proc = subprocess.run(cmd, cwd=target, capture_output=True, text=True, timeout=30)
        conclusion = next(s for s in proc.stdout.splitlines() if "항상 가장 좁은가" in s)
        return dict(command=cmd, rc=proc.returncode, conclusion=conclusion, stdout=proc.stdout, stderr=proc.stderr)

    full = run(out)
    assert full["rc"] == 0 and "아니오" in full["conclusion"]
    # An ordinary new attempt has only published its data so far. Keep old meta.
    v.atomic_write_json(wide, deg("200", "state200-B", {"LAM_PE": 1., "LAM_NE": 2., "LLI": 9.}))
    rejected_unit = pv.verify_unit(wide)
    assert rejected_unit[0] is False
    partial = run(out)
    assert partial["rc"] == 0 and partial["conclusion"].rstrip().endswith("예")
    assert wide.name in partial["stderr"] and "표에서 뺀다" in partial["stderr"]
    write_meta(target, root, wide, "state200-B", "200")
    restored = run(out)
    assert restored["rc"] == 0 and "아니오" in restored["conclusion"]
    empty = root / "empty"
    empty.mkdir()
    empty_run = run(empty)
    assert empty_run["rc"] == 0 and empty_run["conclusion"].rstrip().endswith("예")
    return dict(complete=full, counterexample_unit_rejected=rejected_unit,
                interrupted=partial, finalized_again=restored, empty=empty_run,
                scope="Normal distinct-ID publishers; reader rejects incomplete unit correctly. The aggregate still asserts yes.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=Path, required=True)
    args = ap.parse_args()
    target = args.target.resolve()
    os.environ["PATH"] = str(Path(sys.executable).parent) + os.pathsep + os.environ.get("PATH", "")
    sys.path.insert(0, str(target))
    sys.path.insert(0, str(target / "scripts"))
    from bms_balancing import verify as v
    import provenance as pv
    cs = load("r7_compare_states", target / "scripts/compare_states.py")
    ne = load("r7_ne_shape", target / "scripts/ne_shape.py")
    results = {}
    with tempfile.TemporaryDirectory(prefix="harness-r7-execution-") as tmp:
        for name, fn, extras in [
            ("R6_snapshot_closure", snapshot_cases, (v, pv, cs)),
            ("R6_modern_incomplete_closure", modern_incomplete_controls, (v, pv, cs, ne)),
            ("aggregate_incomplete_counterexample", aggregate_completeness, (v, pv)),
        ]:
            root = Path(tmp) / name
            root.mkdir()
            results[name] = fn(target, root, *extras)
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

