"""R6 d431404 scientific result-unit reader checks.

Uses actual atomic writers, shell metadata helper, verify_unit and result readers.
Synthetic numerical records only. TemporaryDirectory contains all edits.
Exit 0 confirms expected controls/counterexamples, not a GO decision.
"""
from __future__ import annotations
import argparse
import csv
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from unittest.mock import patch


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def fixture_repo(target, root):
    (root / "scripts").mkdir()
    (root / "out").mkdir()
    shutil.copyfile(target / "scripts/provenance.py", root / "scripts/provenance.py")
    (root / "code.py").write_text("value = 1\n", encoding="utf-8")
    git = ["git", "-C", str(root)]
    subprocess.run(git + ["init", "-q"], check=True, capture_output=True)
    subprocess.run(git + ["add", "."], check=True, capture_output=True)
    subprocess.run(git + ["-c", "user.name=R6 Fixture", "-c", "user.email=r6@example.invalid",
                         "commit", "-qm", "numerical fixture"], check=True, capture_output=True)


def helpers(target):
    text = (target / "scripts/run_states.sh").read_text(encoding="utf-8")
    return (text[text.index("write_meta ()"):text.index('\nmkdir -p "$OUT"')]
            + "\n" + text[text.index("say ()"):text.index("\nfail=0")])


def write_meta(target, root, art, rid, starts=24):
    env = dict(os.environ, STARTS=str(starts), SI="Li", BMS_DATA_ROOT="synthetic", OUT=str(root / "out"))
    code = helpers(target) + '\nLAST_RUN_ID="$2"; write_meta "$1" 100 GITT\n'
    p = subprocess.run(["bash", "-c", code, "r6", str(art), rid], cwd=root, env=env,
                       capture_output=True, text=True, timeout=30)
    assert p.returncode == 0, (p.stdout, p.stderr)
    return json.loads(Path(str(art) + ".meta.json").read_text(encoding="utf-8"))


def deg(rid, value):
    return {"run_id": rid, "half_cell": "GITT",
            "best_modes_percent": {"LAM_PE": value, "LAM_NE": value, "LLI": value},
            **{mode + "_percent": {"min": value, "max": value + 1, "span": 1.0}
               for mode in ("LAM_PE", "LAM_NE", "LLI")}}


def mx(rid, value):
    return [{"run_id": rid, "half_cell": "GITT", "si": si, "w_dqdv": 0,
             "gamma_Si": .16, "ref_gamma_Si": .15, "bounds": "-", "ref_bounds": "-",
             "LAM_PE_pct": value + i, "LAM_NE_pct": value + 2*i, "LLI_pct": value + 3*i}
            for i, si in enumerate(("Li", "Kunz"))]


def metadata_sample_mix(target, root, v, pv, reader):
    fixture_repo(target, root)
    art = root / "out/degeneracy_100_Li.json"
    v.atomic_write_json(art, deg("attempt-A", 1.0))
    write_meta(target, root, art, "attempt-A", starts=4)
    assert pv.verify_unit(art)[0] is True
    original_read = Path.read_text
    switched = False

    def scheduled_read(p, *args, **kwargs):
        nonlocal switched
        text = original_read(p, *args, **kwargs)
        if p == art and not switched:
            # Reader already copied A JSON. A second ordinary publisher commits
            # its own B/B unit before the reader asks verify_unit about the path.
            switched = True
            v.atomic_write_json(art, deg("attempt-B", 20.0))
            write_meta(target, root, art, "attempt-B", starts=24)
        return text

    with patch.object(Path, "read_text", scheduled_read):
        loaded = reader.load_degeneracy(root / "out")["100"]
    disk_ok = pv.verify_unit(art)
    assert switched and disk_ok[0] is True
    assert loaded["j"]["run_id"] == "attempt-A"
    assert loaded["meta"]["run_id"] == "attempt-B"
    return {"actual_reader": "compare_states.load_degeneracy", "loaded_value": loaded["j"]["best_modes_percent"]["LLI"],
            "loaded_data_run_id": loaded["j"]["run_id"], "loaded_meta_run_id": loaded["meta"]["run_id"],
            "loaded_meta_starts": loaded["meta"]["starts"], "disk_value": 20.0, "disk_unit": disk_ok,
            "scope": "Both publishers have distinct IDs and valid metadata; no copied ID and no malformed record."}


def matrix_after_verification(target, root, v, pv, reader):
    fixture_repo(target, root)
    art = root / "out/matrix_100.csv"
    rows_a, rows_b = mx("attempt-A", 1.0), mx("attempt-B", 20.0)
    # Make the second matrix's span differ, not merely a common offset.
    rows_b[1]["LLI_pct"] = 99.0
    v.atomic_write_csv(art, rows_a, list(rows_a[0]))
    write_meta(target, root, art, "attempt-A")
    original_check = reader._unit_ok
    switched = False

    def scheduled_check(p):
        nonlocal switched
        ok = original_check(p)
        if p == art and not switched:
            assert ok is True
            switched = True
            # This is the real allowed gap between B's data publication and B
            # metadata publication, not a metadata forgery.
            v.atomic_write_csv(art, rows_b, list(rows_b[0]))
        return ok

    with patch.object(reader, "_unit_ok", scheduled_check):
        loaded = reader.load_matrix_axis(root / "out")["100"]
    final_check = pv.verify_unit(art)
    assert switched and final_check[0] is False
    assert loaded["per"]["GITT"]["LLI"] == 79.0
    return {"actual_reader": "compare_states.load_matrix_axis", "A_verified_span": 3.0,
            "B_consumed_span": loaded["per"]["GITT"]["LLI"], "unit_after_publication": final_check,
            "scope": "Reader passes real check on A, then a normal B data publication precedes B metadata."}


def missing_modern_metadata(target, root, v, pv, reader, shape):
    fixture_repo(target, root)
    dfile = root / "out/degeneracy_100_Li.json"
    mfile = root / "out/matrix_100.csv"
    v.atomic_write_json(dfile, deg("fresh-production-attempt", 7.0))
    rows = mx("fresh-production-attempt", 5.0)
    v.atomic_write_csv(mfile, rows, list(rows[0]))
    # First publication interrupted before write_meta: no sidecar has ever existed.
    dcheck, mcheck = pv.verify_unit(dfile), pv.verify_unit(mfile)
    ds, ms = reader.load_degeneracy(root / "out"), reader.load_matrix_axis(root / "out")
    pair = shape.fitted_pair_info(root / "out", "100", "GITT", "Li")
    assert dcheck[0] is None and mcheck[0] is None
    assert "100" in ds and "100" in ms and pair["row"]["run_id"] == "fresh-production-attempt"
    # Control: a signed unit passes; mismatching an existing modern sidecar
    # fails and is excluded (the internal F07 change is real).
    write_meta(target, root, mfile, "fresh-production-attempt")
    assert pv.verify_unit(mfile)[0] is True
    next_rows = mx("later-attempt", 8.0)
    v.atomic_write_csv(mfile, next_rows, list(next_rows[0]))
    assert pv.verify_unit(mfile)[0] is False and reader.load_matrix_axis(root / "out") == {}
    return {"modern_json_check": dcheck, "modern_csv_check": mcheck,
            "modern_record_has_run_id": True, "degeneracy_accepted": True, "matrix_accepted": True,
            "fitted_pair_accepted": True, "mismatching_present_meta_control_rejected": True,
            "scope": "No metadata deleted: new output committed by actual atomic writers before initial metadata exists."}


def old_version_selected(target, root, pv, reader):
    d = reader.load_degeneracy(target / "out")
    m = reader.load_matrix_axis(target / "out")
    names = {"degeneracy_selected": d["300_0009"]["file"], "matrix_selected": m["300_0009"]["file"]}
    names["selected_degeneracy_unit"] = pv.verify_unit(target / "out" / names["degeneracy_selected"])
    names["selected_matrix_unit"] = pv.verify_unit(target / "out" / names["matrix_selected"])
    names["new_degeneracy_unit"] = pv.verify_unit(target / "out/degeneracy_300_0009_Li.json")
    names["new_matrix_unit"] = pv.verify_unit(target / "out/matrix_300_0009.csv")
    assert names["degeneracy_selected"].endswith("_v2.json") and names["matrix_selected"].endswith("_v2.csv")
    assert names["selected_degeneracy_unit"][0] is None and names["selected_matrix_unit"][0] is None
    assert names["new_degeneracy_unit"][0] is True and names["new_matrix_unit"][0] is True
    names["numerical_difference_claim"] = False
    return names


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--target", type=Path, required=True)
    args = p.parse_args()
    target = args.target.resolve()
    sys.path.insert(0, str(target))
    sys.path.insert(0, str(target / "scripts"))
    os.environ["PATH"] = str(Path(sys.executable).parent) + os.pathsep + os.environ.get("PATH", "")
    from bms_balancing import verify as v
    import provenance as pv
    reader = load("r6_current_reader", target / "scripts/compare_states.py")
    shape = load("r6_current_shape_reader", target / "scripts/ne_shape.py")
    results = {}
    with tempfile.TemporaryDirectory(prefix="harness-r6-unit-") as tmp:
        for name, fn in (("snapshot_metadata_mix", metadata_sample_mix),
                         ("matrix_after_verification", matrix_after_verification),
                         ("missing_modern_meta", missing_modern_metadata),
                         ("old_version_selected", old_version_selected)):
            root = Path(tmp) / name
            root.mkdir()
            if fn is missing_modern_metadata:
                results[name] = fn(target, root, v, pv, reader, shape)
            elif fn is old_version_selected:
                results[name] = fn(target, root, pv, reader)
            else:
                results[name] = fn(target, root, v, pv, reader)
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

