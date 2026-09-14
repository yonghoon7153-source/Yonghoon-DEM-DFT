"""R8 numerical consumers. No target edits and no private source data.

Benign local fixtures use production atomic writers and actual reader/CLI paths.
Synthetic electrode loaders are disclosed; ne_shape arithmetic/readers/publisher
remain production functions. Passing means expected counterexamples observed.
"""
from __future__ import annotations

import argparse
import contextlib
import copy
import csv
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from types import SimpleNamespace
from unittest.mock import patch


def emit(name, obj):
    print(name + " " + json.dumps(obj, ensure_ascii=False, allow_nan=False))


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    sys.modules[name] = obj
    spec.loader.exec_module(obj)
    return obj


def cli(root, script, *args):
    p = subprocess.run([sys.executable, str(root / "scripts" / script), *map(str, args)],
                       cwd=root, capture_output=True, text=True, timeout=60)
    return {"rc": p.returncode, "stdout": p.stdout, "stderr": p.stderr}


def read_json(p):
    return json.loads(p.read_text(encoding="utf-8"))


def sign(path, rid, original=None):
    meta = dict(original or {}, artifact=path.name, run_id=rid,
                sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    path.with_name(path.name + ".meta.json").write_text(json.dumps(meta), encoding="utf-8")


def template(root, state="100"):
    f = root / "out" / f"degeneracy_{state}_Li.json"
    return read_json(f), read_json(f.with_name(f.name + ".meta.json"))


def deg(root, out, state, si, spans, rid):
    from bms_balancing.verify import atomic_write_json
    obj, meta = template(root)
    obj.update(state=state, si_source=si, run_id=rid,
               best_modes_percent={k: 0. for k in spans},
               best_active_bounds=[], ref_active_bounds=[])
    for k, span in spans.items():
        obj[k + "_percent"] = {"min": 0., "max": span, "span": span, "is_lower_bound": True}
    out.mkdir(parents=True, exist_ok=True)
    f = out / f"degeneracy_{state}_{si}.json"
    atomic_write_json(f, obj)
    sign(f, rid, meta)
    return f


def summary(record):
    lines = record["stdout"].splitlines()
    return {"rc": record["rc"],
            "census": [s for s in lines if "대조에 쓴" in s],
            "verdict": [s for s in lines if "항상 가장 좁은가" in s],
            "stderr": record["stderr"]}


def aggregate(root, prov):
    cs = module(root / "scripts/compare_states.py", "r8_compare_aggregate")
    narrow = {"LAM_PE": 2., "LAM_NE": 3., "LLI": 1.}
    wide = {"LAM_PE": 1., "LAM_NE": 2., "LLI": 9.}
    with tempfile.TemporaryDirectory(prefix="r8-si-census-") as td:
        base = Path(td)
        # Two supported Si values, same state, independent normal units.
        kunz = deg(root, base, "100", "Kunz", wide, "r8-Kunz")
        only_kunz = cli(root, "compare_states.py", "case=" + str(base))
        assert "아니오" in only_kunz["stdout"] and only_kunz["rc"] == 0
        li = deg(root, base, "100", "Li", narrow, "r8-Li")
        assert prov.read_unit(kunz)[0] is True and prov.read_unit(li)[0] is True
        exc = []
        selected = cs.load_degeneracy(base, excluded=exc)
        both = cli(root, "compare_states.py", "case=" + str(base))
        assert selected["100"]["si"] == "Li" and not exc
        assert both["rc"] == 0 and summary(both)["verdict"][0].rstrip().endswith("예")
        assert "**1/1**" in both["stdout"]
        emit("R8_AGGREGATE_SI_KEY_COLLISION", {"Kunz_only": summary(only_kunz),
            "Kunz_plus_Li": summary(both), "actual_verified_files": 2,
            "retained_dictionary_entries": len(selected), "ignored_file": kunz.name,
            "same_state_different_supported_Si": True})
    with tempfile.TemporaryDirectory(prefix="r8-root-census-") as td:
        base = Path(td)
        good, empty = base / "good", base / "empty"
        deg(root, good, "100", "Li", narrow, "r8-one-root")
        empty.mkdir()
        one_empty = cli(root, "compare_states.py", "empty=" + str(empty))
        multiple = cli(root, "compare_states.py", "good=" + str(good), "empty=" + str(empty))
        absent = cli(root, "compare_states.py", "good=" + str(good), "absent=" + str(base / "absent"))
        assert one_empty["rc"] == 2
        assert multiple["rc"] == absent["rc"] == 0
        assert summary(multiple)["verdict"][0].rstrip().endswith("예")
        emit("R8_AGGREGATE_REQUESTED_ROOT_MISSING", {"empty_only": summary(one_empty),
            "valid_plus_empty": summary(multiple), "valid_plus_nonexistent": summary(absent),
            "explicitly_requested_roots": 2})


def unit_check(root, prov):
    from bms_balancing.verify import atomic_write_json
    with tempfile.TemporaryDirectory(prefix="r8-u14-unit-") as td:
        base = Path(td)
        old, new = base / "old", base / "new"
        old.mkdir(); new.mkdir()
        a, meta = template(root)
        a["run_id"] = "r8-unit-A"
        oldf = old / "degeneracy_100_Li.json"
        newf = new / oldf.name
        for f in (oldf, newf):
            atomic_write_json(f, a); sign(f, a["run_id"], meta)
        before = cli(root, "check_u14.py", "--new", new, "--old", old)
        assert before["rc"] == 0 and prov.read_unit(newf)[0] is True
        b = dict(a, run_id="r8-unit-B")
        # Another normal identical numeric rerun publishes data before its meta.
        atomic_write_json(newf, b)
        unit = prov.read_unit(newf)[:2]
        during = cli(root, "check_u14.py", "--new", new, "--old", old)
        assert unit[0] is False and during["rc"] == 0
        assert "전부 같다" in during["stdout"]
        sign(newf, b["run_id"], meta)
        after = cli(root, "check_u14.py", "--new", new, "--old", old)
        assert after["rc"] == 0 and prov.read_unit(newf)[0] is True
        emit("R8_CHECK_U14_INCOMPLETE_NORMAL_RERUN", {"before_rc": before["rc"],
            "during_read_unit": unit, "during_check": during, "after_rc": after["rc"],
            "numeric_payload_unchanged": True, "different_execution_ids": True})


def duplicate_rows(root, prov):
    from bms_balancing.verify import atomic_write_csv
    cs = module(root / "scripts/compare_states.py", "r8_compare_rows")
    with tempfile.TemporaryDirectory(prefix="r8-u14-rows-") as td:
        base = Path(td)
        old, new = base / "old", base / "new"
        old.mkdir(); new.mkdir()
        source = root / "out/matrix_100.csv"
        meta = read_json(source.with_name(source.name + ".meta.json"))
        with source.open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        for r in rows: r["run_id"] = "r8-rows-A"
        oldf = old / source.name
        atomic_write_csv(oldf, rows, list(rows[0])); sign(oldf, "r8-rows-A", meta)
        idx = next(i for i, r in enumerate(rows) if float(r["w_dqdv"]) == 0 and r["half_cell"] == "GITT")
        changed = copy.deepcopy(rows)
        original = copy.deepcopy(changed[idx])
        changed[idx]["LLI_pct"] = str(float(changed[idx]["LLI_pct"]) + 3.)
        changed.append(original)
        for r in changed: r["run_id"] = "r8-rows-B"
        newf = new / source.name
        atomic_write_csv(newf, changed, list(changed[0])); sign(newf, "r8-rows-B", meta)
        assert prov.read_unit(newf)[0] is True
        p = cli(root, "check_u14.py", "--new", new, "--old", old)
        assert p["rc"] == 0 and "전부 같다" in p["stdout"]
        old_span = cs.load_matrix_axis(old)["100"]["per"]["GITT"]["LLI"]
        new_span = cs.load_matrix_axis(new)["100"]["per"]["GITT"]["LLI"]
        assert new_span > old_span + 2.
        changed.pop()
        atomic_write_csv(newf, changed, list(changed[0])); sign(newf, "r8-rows-B", meta)
        q = cli(root, "check_u14.py", "--new", new, "--old", old)
        assert q["rc"] == 1
        emit("R8_CHECK_U14_DUPLICATE_KEY_COLLAPSE", {"old_rows": len(rows), "new_rows": len(changed) + 1,
            "old_consumer_LLI_span": old_span, "new_consumer_LLI_span": new_span,
            "with_duplicate_check": p, "remove_only_duplicate_rc": q["rc"],
            "duplicate_key": [original[k] for k in ("half_cell", "si", "w_dqdv")],
            "fixture_not_claimed_as_existing_production_output": True})


def shape(root, prov):
    import numpy as np
    import pytest
    from bms_balancing.model import Blend
    from bms_balancing.verify import atomic_write_csv
    ns = module(root / "scripts/ne_shape.py", "r8_shape")
    u = np.linspace(0., 1., 301)
    arrays = ((1. - u) ** 2, .1 + .7 * u, 1. - u, .1 + .7 * u)
    blend = Blend(*arrays, window=11, poly_order=3)
    offsets = {"pristine": 0., "100": .01, "200": .1}
    class P:
        def __init__(self, state): self.state = state
        def is_file(self): return True
    class IB:
        def __init__(self, p): self.p = p
        def stream(self): return self.p
        def identity(self): return {"path": self.p.state, "sha256": hashlib.sha256(self.p.state.encode()).hexdigest()}
    class HC:
        def __init__(self, p, **kw): self.state = p.state
        def E_NE(self, x): return blend.E(x, .2) + offsets[self.state]
        def E_PE(self, x): return 4.2 - .7 * np.asarray(x)
    with tempfile.TemporaryDirectory(prefix="r8-ne-shape-partial-") as td:
        base = Path(td)
        matrix, out = base / "matrix", base / "shape"
        matrix.mkdir()
        def pair(state):
            f = matrix / f"matrix_{state}.csv"
            row = dict(half_cell="GITT", si="Li", w_dqdv="0", gamma_Si=".25", ref_gamma_Si=".2",
                       run_id="r8-matrix-" + state)
            atomic_write_csv(f, [row], list(row)); sign(f, row["run_id"])
            assert prov.read_unit(f)[0] is True
        pair("100")
        def run():
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf): rc = ns.main()
            f = out / "ne_shape_GITT_Li.csv"
            rows = list(csv.DictReader(io.StringIO(f.read_text(encoding="utf-8"))))
            return rc, buf.getvalue(), rows, prov.read_unit(f)[:2]
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(ns.D, "STATES", list(offsets))
            mp.setattr(ns.D, "data_root", lambda *a, **k: base)
            mp.setattr(ns.D, "half_cell_path", lambda r, src, state: P(state))
            mp.setattr(ns.D, "read_input", lambda p: IB(p))
            mp.setattr(ns.D, "load_literature", lambda *a, **k: arrays)
            mp.setattr(ns, "HalfCell", HC)
            mp.setattr(ns, "raw_ne_capacity", lambda p: 1.)
            mp.setattr(sys, "argv", ["ne_shape.py", "--out-dir", str(matrix), "--write", str(out)])
            partial = run()
            assert partial[0] == 0 and partial[3][0] is True
            assert float(partial[2][1]["measured_shape_mV"]) == 100.
            assert partial[2][1]["gamma_target"] == ""
            assert "측정된 음극 모양 변화 최대 10.00 mV" in partial[1]
            pair("200")
            complete = run()
            assert complete[0] == 0 and "측정된 음극 모양 변화 최대 100.00 mV" in complete[1]
            emit("R8_NE_SHAPE_PARTIAL_MEASURED_MAXIMUM", {"half_cell_states": list(offsets),
                "partial_rc": partial[0], "partial_output_unit": partial[3],
                "partial_csv_rows": [{k: r[k] for k in ("state", "measured_shape_mV", "gamma_target", "gamma_ref")} for r in partial[2]],
                "partial_summary": [s for s in partial[1].splitlines() if "최대" in s][:5],
                "complete_rc": complete[0], "complete_summary": [s for s in complete[1].splitlines() if "측정된 음극" in s],
                "actual_reader_and_arithmetic_publisher": True, "synthetic_electrode_loaders": True,
                "only_added_matrix_pair_for_200": True})


def closures(root, previous, old):
    import provenance
    sys.path.insert(0, str(root / "tests"))
    tests = module(root / "tests/test_r7_codex.py", "r8_closure_tests")
    with tempfile.TemporaryDirectory(prefix="r8-positive-") as td:
        tests.test_d7_01_aggregate_says_incomplete_instead_of_certifying_the_states_that_survived(Path(td))
    with tempfile.TemporaryDirectory(prefix="r8-positive-") as td:
        tests.test_d7_04_check_u14_does_not_prefer_a_versioned_sibling_in_a_current_directory(Path(td))
    tests.test_d7_07_docs_state_the_profile_budget_without_settling_the_cause()
    verified = []
    for family in ("degeneracy", "matrix", "profile_gamma"):
        for state in ("100", "200", "300_0009", "300_0147"):
            name = (f"matrix_{state}.csv" if family == "matrix" else
                    f"{family}_{state}_Li." + ("json" if family == "degeneracy" else "csv"))
            data = (root / "out" / name).read_bytes()
            assert provenance.read_unit(root / "out" / name)[0] is True
            if previous: assert data == (previous / "out" / name).read_bytes()
            verified.append({"name": name, "sha256": hashlib.sha256(data).hexdigest(),
                             "byte_equal_to_R7": bool(previous), "unit_verified": True})
    emit("R8_POSITIVE_CLOSURES_AND_12_DATA_ARTIFACTS", {"actual_regressions": 3, "artifacts": verified})
    if old:
        check = module(root / "scripts/check_u14.py", "r8_policy_check")
        f = root / "out/degeneracy_300_0009_Li.json"
        current, historical = check.baseline_for(f, old, "current"), check.baseline_for(f, old, "historical")
        assert current.name == f.name and historical.name.endswith("_v2.json")
        emit("R8_EXTRACTED_HISTORICAL_POLICY_EXPLICIT", {"current_policy_file": current.name,
            "historical_policy_file": historical.name,
            "current_LLI_span": read_json(current)["LLI_percent"]["span"],
            "historical_LLI_span": read_json(historical)["LLI_percent"]["span"],
            "new_defect_claim": False, "explicit_historical_required_for_manual_extract": True})


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--target", type=Path, default=Path.cwd())
    p.add_argument("--previous", type=Path)
    p.add_argument("--old", type=Path)
    p.add_argument("--case", choices=("all", "aggregate", "unit", "rows", "shape", "closures"), default="all")
    a = p.parse_args()
    root = a.target.resolve()
    sys.path[:0] = [str(root), str(root / "scripts")]
    prov = module(root / "scripts/provenance.py", "provenance")
    cases = {"closures": lambda: closures(root, a.previous.resolve() if a.previous else None, a.old.resolve() if a.old else None),
             "aggregate": lambda: aggregate(root, prov), "unit": lambda: unit_check(root, prov),
             "rows": lambda: duplicate_rows(root, prov), "shape": lambda: shape(root, prov)}
    for k, fn in cases.items():
        if a.case in ("all", k): fn()
    print("R8_INFERENCE_REPROS_PASSED")
