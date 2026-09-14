"""R7 scientific artifact audit at 521be85; inherited R6 probes rerun, not assumed.

Never edits the target. No private MATLAB or raw battery workbook is executed.
"""
from __future__ import annotations

import argparse
from collections import Counter
import contextlib
import csv
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
import re
import sys
import subprocess
import tempfile
from types import SimpleNamespace
from unittest.mock import patch
import warnings


def clean(value):
    if isinstance(value, dict): return {k: clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)): return [clean(v) for v in value]
    if isinstance(value, float) and not math.isfinite(value): return str(value)
    return value


def emit(name, value):
    print(name + " " + json.dumps(clean(value), ensure_ascii=False, allow_nan=False))


def load_tests(root):
    spec = importlib.util.spec_from_file_location("r6_inference_tests", root / "tests/test_review_findings.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def constants(values):
    from bms_balancing.model import Objective

    class ConstantMetrics(Objective):
        def __init__(self):
            self.use_peak_weight = False
            self.w_pocv = self.w_dvdq = self.w_dqdv = 1.
            self.c_cell = 1.
            self.scale_seed, self.n_scale_samples = 0, 50
            self.calls = Counter()
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.scales = self._auto_scales(0, 50)
        def metric(self, key):
            self.calls[key] += 1
            val = values[key]
            if isinstance(val, Exception): raise val
            return val
        def rmse_pocv(self, p): return self.metric("pocv")
        def rmse_dvdq(self, p): return self.metric("dvdq")
        def rmse_dqdv(self, p, weighted=False): return self.metric("dqdv")

    return ConstantMetrics()


def positive_closure(tests):
    tests.test_r5_06_scale_audit_records_eps_relative_effect_and_an_equivalence_flag()
    tests.test_r5_10_auto_scale_counts_each_sample_once_even_when_a_metric_raises()
    tests.test_r5_docs_u12_scope_and_summary_qualifiers()
    tests.test_u13_scale_audit_transcript_meets_the_equivalence_condition_and_covers_the_recompare_configs()
    tests.test_section_1_8_192_values_are_backed_by_committed_recompare_artifacts()
    with tempfile.TemporaryDirectory(prefix="r6-existing-matrix-") as td:
        import pytest
        with pytest.MonkeyPatch.context() as mp:
            tests.test_r5_07_matrix_rows_carry_scales_and_audits_for_target_and_reference(Path(td), mp)
    emit("R5_INFERENCE_CLOSURE", {"production_regressions_passed": 6})


def scale_domains():
    from bms_balancing.model import SCALE_EQUIV_REL
    cases = [("ordinary", 1., True), ("tiny", 1e-20, False), ("zero", 0., False),
             ("infinite", float("inf"), False), ("nan", float("nan"), False),
             ("exception", ValueError("controlled"), False)]
    records = []
    for name, val, expected in cases:
        o = constants({k: val for k in ("pocv", "dvdq", "dqdv")})
        assert all(v["n"] == 50 and v["equivalent_within_rel"] is expected for v in o.scale_audit.values())
        if expected:
            rec = o.scale_audit["pocv"]
            actual_relative = abs(rec["scale"] - rec["raw_lower_half_mean"]) / rec["raw_lower_half_mean"]
            assert actual_relative <= SCALE_EQUIV_REL
        records.append({"case": name, "audit": o.scale_audit["pocv"]})
    partial = constants({"pocv": 1., "dvdq": ValueError("controlled"), "dqdv": 2.})
    assert all(v["n"] == 50 for v in partial.scale_audit.values())
    assert partial.scale_audit["dvdq"]["n_exception"] == 50
    assert partial.scale_audit["pocv"]["n_exception"] == partial.scale_audit["dqdv"]["n_exception"] == 0
    emit("SCALE_DOMAIN_AND_EXCEPTION_CLOSURE", {"cases": records, "second_metric_exceptions": partial.scale_audit})


def plateau(tests):
    import numpy as np
    from bms_balancing.model import Objective, LB5, UB5
    class Plateau(tests._FinitePlateau, Objective):
        def __init__(self):
            tests._FinitePlateau.__init__(self)
            self.c_cell, self.scale_seed, self.n_scale_samples = 1., 0, 50
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.scales = self._auto_scales(0, 50)
    obj = Plateau()
    samples = LB5 + np.random.default_rng(0).random((50, 5)) * (UB5 - LB5)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        good = next(p for p in samples if np.isfinite(obj.rmse_dqdv(p)))
    return obj, good


def matrix_independent_axes(tests):
    from bms_balancing import verify
    for inf_side in ("target", "ref"):
        with tempfile.TemporaryDirectory(prefix="r6-matrix-audit-") as td:
            base = Path(td)
            stub = base / "present.xlsx"
            stub.write_text("presence fixture only", encoding="utf-8")
            out = base / "matrix.csv"
            actual_objects = {}
            _, good = plateau(tests)

            def build(root, source, state, si, **kw):
                side = "ref" if state == "pristine" else "target"
                obj = plateau(tests)[0] if side == inf_side else constants({k: 1. for k in ("pocv", "dvdq", "dqdv")})
                actual_objects[side] = obj
                return obj

            args = SimpleNamespace(data_root=str(base), source="GITT", state="100", seed=0, starts=1,
                                   w_dqdv=1., only_source=True, only_wdqdv=True, out=str(out), run_id="r6-" + inf_side)
            buf = io.StringIO()
            with patch.object(verify.D, "data_root", return_value=base), \
                 patch.object(verify.D, "HALF_FILE", {"GITT": {"pristine": "x", "100": "x"}}), \
                 patch.object(verify.D, "SI_SOURCES", ("Li",)), \
                 patch.object(verify.D, "half_cell_path", return_value=stub), \
                 patch.object(verify, "build", side_effect=build), \
                 patch.object(verify, "multistart", side_effect=lambda obj, **kw: (good, obj(good), [])), \
                 contextlib.redirect_stdout(buf):
                verify.cmd_matrix(args)
            with out.open(encoding="utf-8") as stream:
                rows = list(csv.DictReader(stream))
            assert len(rows) == 1
            row = rows[0]
            flags = {}
            for side in ("target", "ref"):
                audit = json.loads(row["scale_audit_" + side])
                assert audit == actual_objects[side].scale_audit
                flags[side] = audit["dqdv"]["equivalent_within_rel"]
                assert flags[side] is (side != inf_side)
                assert audit["dqdv"]["n_inf"] == (36 if side == inf_side else 0)
                for metric in ("pocv", "dvdq", "dqdv"):
                    assert float(row[f"scale_{metric}_{side}"]) == actual_objects[side].scales[metric]
            assert "scale_audit" in buf.getvalue()
            emit("MATRIX_INDEPENDENT_AUDIT_AXIS", {"only_inf_side": inf_side, "published_flags": flags,
                 "published_scales_equal_live_objects": True, "synthetic_forward": True,
                 "fit_stubbed_for_bounded_serialization_test": True})


def u13_coverage(root, tests):
    text = (root / "out/scale_audit_eval_u13.txt").read_text(encoding="utf-8")
    lines = [line for line in text.splitlines() if line.startswith("# scale_audit,")]
    head = re.compile(r"state=(\S+) source=(\S+) si=(\S+) seed=(\d+) n=(\d+)")
    keys = Counter(tuple(head.search(line).groups()[:3]) for line in lines)
    values = [float(v) for line in lines for v in re.findall(r"/eps_rel=([0-9.e+-]+)", line)]
    assert len(lines) == 18 and len(values) == 54
    emit("U13_REPORTED_SCOPE", {"lines": len(lines), "metric_records": len(values),
         "configuration_counts": [{"config": k, "count": v} for k, v in sorted(keys.items())],
         "printed_eps_rel_min": min(values), "printed_eps_rel_max": max(values),
         "root_identity_independently_verified": False,
         "root_order_claim_is_explicitly_admitted": True})
    cases = {
        "missing_Kunz": ("source=GITT si=Kunz", "source=GITT si=Li"),
        "missing_step_005C": ("source=step_005C si=Li", "source=GITT si=Li"),
        "eps_condition_only": ("eps_rel=1.45e-15/equiv=1", "eps_rel=1e-8/equiv=1"),
        "flag_only": ("eps_rel=1.45e-15/equiv=1", "eps_rel=1.45e-15/equiv=0"),
    }
    with tempfile.TemporaryDirectory(prefix="r6-u13-negative-") as td:
        scratch = Path(td)
        (scratch / "out").mkdir()
        (scratch / "FINDINGS.md").write_text((root / "FINDINGS.md").read_text(encoding="utf-8"), encoding="utf-8")
        f = scratch / "out/scale_audit_eval_u13.txt"
        for name, (old, new) in cases.items():
            assert old in text
            f.write_text(text.replace(old, new, 1), encoding="utf-8")
            with patch.object(tests, "ROOT", scratch):
                try:
                    tests.test_u13_scale_audit_transcript_meets_the_equivalence_condition_and_covers_the_recompare_configs()
                except AssertionError:
                    emit("U13_AXIS_NEGATIVE_CONTROL", {"case": name, "rejected": True})
                else:
                    raise AssertionError("U13 regression accepted " + name)


def scale_equivalence_not_argmin_equivalence():
    import numpy as np
    from bms_balancing.model import SCALE_EQUIV_REL
    raw = np.array([.001, 1.])
    eps = np.finfo(float).eps
    port = raw + eps
    assert np.all(eps / raw <= SCALE_EQUIV_REL)
    # Two finite metric vectors. This illustrates what a scale perturbation
    # bound does NOT promise; it is not a defect in the newly restricted flag.
    metrics = np.array([[.001, 0.], [0., 1. - 1e-14]])
    original_values = (metrics / raw).sum(axis=1)
    port_values = (metrics / port).sum(axis=1)
    assert int(np.argmin(original_values)) == 1 and int(np.argmin(port_values)) == 0
    emit("DESIGN_NOTE_SCALE_BOUND_NOT_ARGMIN_BOUND", {
         "all_eps_conditions_hold": True, "raw_scale_objectives": original_values.tolist(),
         "port_scale_objectives": port_values.tolist(), "winner_raw": "B", "winner_port": "A",
         "new_defect_claim": False, "real_battery_result_reversal_claim": False})


def finite_reduction_overflow_stress():
    o = constants({k: 1e308 for k in ("pocv", "dvdq", "dqdv")})
    rec = o.scale_audit["pocv"]
    assert rec["n_finite"] == 50 and math.isinf(rec["raw_lower_half_mean"])
    assert rec["eps_rel"] == 0. and rec["equivalent_within_rel"] is True
    emit("OPTIONAL_FINITE_REDUCTION_OVERFLOW_STRESS", {
         "audit": rec, "classification": "helper hardening, not a proved live battery path",
         "normal_raw_rmse_methods_cannot_return_1e308_finitely": True})


def module_at(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def derived_closure_and_grid(root):
    import numpy as np
    sys.path.insert(0, str(root / "tests"))
    internal = module_at(root / "tests/test_r6_internal.py", "r6_final_internal_tests")
    for name in (
        "test_i6d_01_section_3_4_says_the_profile_grid_contains_the_constrained_endpoints",
        "test_i6d_03_raw_lli_ratio_names_its_statistic",
        "test_i6d_05_the_192_values_are_raw_rmse_and_the_docs_do_not_tie_u13_to_them",
        "test_i6d_07_section_1_10_carries_the_lower_bound_qualifier",
        "test_i6d_08_section_4_1_free_reference_width_is_the_width_of_the_values",
        "test_i6d_09_section_3_3_cites_the_matrix_row_that_actually_matches",
    ):
        getattr(internal, name)()
    records = []
    for filename in ("archive/degeneracy_300_0009_Li_v2.json", "degeneracy_300_0009_Li.json"):
        data = json.loads((root / "out" / filename).read_text(encoding="utf-8"))
        for mode in ("LAM_PE", "LAM_NE", "LLI"):
            info = data[mode + "_percent"]
            ext, prof = info["from_constrained_extrema"], info["from_mode_profile"]
            grid = np.linspace(*prof["grid_range_pct"], 21)
            assert abs(grid[5] - ext["min"]) < 1e-12
            assert abs(grid[15] - ext["max"]) < 1e-12
            assert prof["max"] == ext["max"] and info["is_lower_bound"]
            records.append({"artifact": filename, "mode": mode, "width_lower_bound": info["span"],
                 "profile_min_equals_constrained": prof["min"] == ext["min"],
                 "profile_max_equals_constrained": True,
                 "has_attainable_grid": "attainable_pct" in prof})
    emit("DF01_AND_DERIVED_CLOSURE", {"actual_regressions_passed": 6, "grid_records": records,
         "independent_convergence_claim": False,
         "raw_private_data_rechecked_for_endpoint_feasibility": False})


def csv_rows(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def threshold_summary(rows, threshold):
    selected = [r for r in rows if 1000. * float(r["rmse_pocv"]) <= threshold]
    vals = [float(r["LAM_NE_pct"]) for r in selected]
    gammas = [float(r["gamma_Si"]) for r in selected]
    return {"n": len(selected), "gamma_min": min(gammas), "gamma_max": max(gammas),
            "LAM_NE_width_pct": max(vals) - min(vals),
            "worst_objective_ratio": max(float(r["obj_ratio_to_best"]) for r in selected)}


def u14_compare(root, old):
    check = module_at(root / "scripts/check_u14.py", "r6_final_check_u14")
    states = ("100", "200", "300_0009", "300_0147")
    report = []
    for state in states:
        new_m = root / "out" / f"matrix_{state}.csv"
        old_m = check.baseline_for(new_m, old)
        assert old_m is not None
        key = lambda r: (r["half_cell"], r["si"], float(r["w_dqdv"]))
        a_rows, b_rows = csv_rows(old_m), csv_rows(new_m)
        a, b = {key(r): r for r in a_rows}, {key(r): r for r in b_rows}
        assert len(a_rows) == len(a) == len(b) == len(b_rows) and set(a) == set(b)
        differences = []
        numeric_cells = 0
        for k in a:
            for col in set(a[k]) & set(b[k]):
                if col in check.ROW_SKIP: continue
                try: av, bv = float(a[k][col]), float(b[k][col])
                except ValueError:
                    assert a[k][col] == b[k][col], (state, k, col)
                    continue
                numeric_cells += 1
                if av != bv: differences.append((k, col, av, bv))
        assert not differences, differences[:3]
        new_d = root / "out" / f"degeneracy_{state}_Li.json"
        old_d = check.baseline_for(new_d, old)
        da, db = json.loads(old_d.read_text(encoding="utf-8")), json.loads(new_d.read_text(encoding="utf-8"))
        spans = {}
        for mode in ("LAM_PE", "LAM_NE", "LLI"):
            av, bv = da[mode + "_percent"]["span"], db[mode + "_percent"]["span"]
            assert av == bv
            spans[mode] = bv
        new_p = root / "out" / f"profile_gamma_{state}_Li.csv"
        old_p = check.baseline_for(new_p, old)
        pa, pb = csv_rows(old_p), csv_rows(new_p)
        a, b = {float(r["gamma_Si"]): r for r in pa}, {float(r["gamma_Si"]): r for r in pb}
        assert len(a) == len(pa) == len(b) == len(pb) and set(a) == set(b)
        maxima = {}
        for gamma in a:
            for col in set(a[gamma]) & set(b[gamma]):
                if col in check.ROW_SKIP: continue
                try: av, bv = float(a[gamma][col]), float(b[gamma][col])
                except ValueError: continue
                rel = abs(bv - av) / max(abs(av), 1e-300)
                if col not in maxima or rel > maxima[col]["relative"]:
                    maxima[col] = {"relative": rel, "absolute": abs(bv - av), "gamma": gamma,
                                   "old": av, "new": bv}
        report.append({"state": state, "matrix_baseline": old_m.name, "matrix_numeric_cells_equal": numeric_cells,
                       "degeneracy_baseline": old_d.name, "degeneracy_spans_equal": spans,
                       "profile_baseline": old_p.name, "profile_rows": len(pb),
                       "profile_n_tried": sorted({int(r["n_tried"]) for r in pb}),
                       "profile_min_successes": min(int(r["n_ok"]) for r in pb),
                       "profile_relative_maxima": {k: maxima[k] for k in ("LAM_NE_pct", "b_NE", "rmse_pocv")}})
        if state == "300_0009":
            thresholds = [{"threshold_mV": t, "old": threshold_summary(pa, t), "new": threshold_summary(pb, t)}
                          for t in (8, 10, 11, 12)]
            assert [r["new"]["n"] for r in thresholds] == [6, 10, 12, 13]
            for r in thresholds:
                assert r["old"]["n"] == r["new"]["n"]
                assert r["old"]["gamma_min"] == r["new"]["gamma_min"]
                assert r["old"]["gamma_max"] == r["new"]["gamma_max"]
                assert f'{r["old"]["LAM_NE_width_pct"]:.3f}' == f'{r["new"]["LAM_NE_width_pct"]:.3f}'
                assert f'{r["old"]["worst_objective_ratio"]:.3f}' == f'{r["new"]["worst_objective_ratio"]:.3f}'
            emit("U14_SECTION_5_1_THRESHOLDS", thresholds)
    emit("U14_12_ARTIFACT_NUMERIC_COMPARISON", report)
    starts = [json.loads((root / "out" / f"profile_gamma_{s}_Li.csv.meta.json").read_text(encoding="utf-8"))["starts"]
              for s in states]
    assert starts == [24] * 4 and all(r["profile_n_tried"] == [25] for r in report)
    emit("U14_PROFILE_BUDGET_FACT", {"requested_random_starts_per_gamma": starts,
         "actual_attempts_per_gamma": [25] * 4,
         "source": "cmd_profile: best[:4] plus args.starts random starts",
         "gamma_profile_has_fewer_starts_than_ordinary_multistart": False,
         "cause_of_profile_change_inferred": False})


def section5_printed_rows(root):
    findings = (root / "FINDINGS.md").read_text(encoding="utf-8")
    sec = findings.split("## 5. γ_Si", 1)[1].split("### 5-1.", 1)[0]
    raw_rows = csv_rows(root / "out/profile_gamma_300_0009_Li.csv")
    rows = {round(float(r["gamma_Si"]), 12): r for r in raw_rows}
    assert len(rows) == len(raw_rows)
    columns = (("rmse_pocv", 1000.), ("a_NE", 1.), ("LAM_NE_pct", 1.), ("LAM_PE_pct", 1.), ("LLI_pct", 1.))
    checked, mismatches = 0, []
    for line in sec.splitlines():
        if not re.match(r"\| 0\.\d", line): continue
        cells = [x.strip().replace("**", "").replace("−", "-") for x in line.split("|")[1:-1]]
        gamma = round(float(cells[0]), 12); row = rows[gamma]
        for cell, (column, factor) in zip(cells[1:], columns):
            tok = re.search(r"[-+]?\d+(?:\.\d+)?", cell).group(0)
            decimals = len(tok.split(".")[1]) if "." in tok else 0
            actual = float(row[column]) * factor
            checked += 1
            if abs(actual - float(tok)) > .5 * 10. ** (-decimals) + 1e-12:
                mismatches.append({"gamma": gamma, "column": column, "printed": tok, "actual": actual})
    emit("CURRENT_SECTION_5_PRINTED_TABLE", {"numeric_cells_checked": checked, "mismatches": mismatches})
    assert checked == 35 and not mismatches


def r7_current_canonical(root, tests, previous=None):
    import numpy as np
    read_unit = module_at(root / "scripts/provenance.py", "r7_provenance_canon").read_unit
    compare = module_at(root / "scripts/compare_states.py", "r7_compare")
    dg, mx = compare.load_degeneracy(root / "out"), compare.load_matrix_axis(root / "out")
    assert dg["300_0009"]["file"] == "degeneracy_300_0009_Li.json"
    assert mx["300_0009"]["file"] == "matrix_300_0009.csv"
    records = []
    for family in ("degeneracy", "matrix", "profile_gamma"):
        for state in ("100", "200", "300_0009", "300_0147"):
            name = (f"matrix_{state}.csv" if family == "matrix" else
                    f"{family}_{state}_Li." + ("json" if family == "degeneracy" else "csv"))
            path = root / "out" / name
            ok, why, data, meta = read_unit(path)
            assert ok is True, (name, why)
            rec = {"name": name, "verified": ok, "sha256": hashlib.sha256(data).hexdigest()}
            if previous:
                assert data == (previous / "out" / name).read_bytes(), name
                rec["identical_to_d431404_bytes"] = True
            records.append(rec)
    for name in (
        "test_quoted_spreads_match_artifact",
        "test_dump_table_in_matlab_readme_matches_artifact",
        "test_section_1_12_physical_normalization_and_misfit_tables_match_artifacts",
        "test_section_1_10_table_prints_best_min_max_and_width",
        "test_section_1_12_pouch_pe_fixing_did_not_reproduce_the_wide_lli_band",
        "test_section_1_12_pe_axis_strength_table_matches_the_csv",
    ):
        getattr(tests, name)()
    emit("R7_CURRENT_CANONICAL_12_UNITS", {"records": records, "six_scientific_regressions_passed": True,
        "private_raw_data_reexecuted": False})


def r7_document_closures(root):
    import numpy as np
    from scipy.optimize import minimize
    sys.path.insert(0, str(root / "tests"))
    internal = module_at(root / "tests/test_r6_internal.py", "r7_internal_doc_tests")
    internal.test_c6_06_profile_budget_is_stated_as_it_is_run()
    with tempfile.TemporaryDirectory(prefix="r7-q3-") as td:
        internal.test_c6_q3_precision_conflict_is_partial_only_when_the_option_absorbed_a_difference(Path(td))
    emit("R7_06_AND_Q3_ACTUAL_REGRESSIONS", {"passed": 2, "equal_values_conflict": "complete",
        "override_only_absorbs_difference": "partial"})
    # This smooth, bounded numerical example rejects only the inference that
    # equal numbers of starts establish adequate search. It is not a battery
    # model and does not identify the cause of the preserved U14 differences.
    def fun(x):
        return float((x[0] * x[0] - 1.) ** 2 + .2 * x[0] + 2.)
    def jac(x):
        return np.array([4. * x[0] * (x[0] * x[0] - 1.) + .2])
    def search(starts):
        rs = [minimize(fun, [x], jac=jac, method="L-BFGS-B", bounds=[(-2., 2.)]) for x in starts]
        assert all(r.success for r in rs)
        best = min(rs, key=lambda r: r.fun)
        return {"n_tried": len(rs), "best_x": float(best.x[0]), "best_objective": float(best.fun)}
    a, b = search(np.linspace(-1.01, -.99, 25)), search(np.linspace(.99, 1.01, 25))
    combined = search(list(np.linspace(.99, 1.01, 25)) + [-1.])
    assert a["n_tried"] == b["n_tried"] and a["best_objective"] < b["best_objective"]
    assert combined["best_objective"] < b["best_objective"]
    text = (root / "FINDINGS.md").read_text(encoding="utf-8")
    ledger = (root / "reviews/R6_LEDGER.md").read_text(encoding="utf-8")
    assert "시작 예산 부족이 아니라" in text
    assert "야생에서 확인된 것" in ledger and '**가설**이고' in ledger
    emit("R7_EQUAL_BUDGET_NOT_A_CONVERGENCE_CERTIFICATE", {"25_start_A": a, "25_start_B": b,
        "B_plus_one_start": combined, "reported_budget_regression_passes_with_causal_language": True,
        "synthetic_only": True, "cause_of_real_U14_drift_claimed": False,
        "actual_U14_25_starts_disputed": False})


def r7_baseline_policy_split(root):
    read_unit = module_at(root / "scripts/provenance.py", "r7_provenance_baseline").read_unit
    compare = module_at(root / "scripts/compare_states.py", "r7_compare_baseline")
    check = module_at(root / "scripts/check_u14.py", "r7_check_baseline")
    source = root / "out/degeneracy_100_Li.json"
    a = json.loads(source.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix="r7-current-old-policy-") as td:
        old, new = Path(td) / "current", Path(td) / "rerun"
        old.mkdir(); new.mkdir()
        original_meta = json.loads(source.with_name(source.name + ".meta.json").read_text(encoding="utf-8"))
        def publish(d, body, rid):
            body = dict(body, run_id=rid)
            data = (json.dumps(body, ensure_ascii=False) + "\n").encode("utf-8")
            p = d / source.name
            p.write_bytes(data)
            meta = dict(original_meta, run_id=rid, sha256=hashlib.sha256(data).hexdigest(), artifact=source.name)
            p.with_name(p.name + ".meta.json").write_text(json.dumps(meta), encoding="utf-8")
            assert read_unit(p)[0] is True
            return data
        b = json.loads(json.dumps(a))
        old_span = b["LLI_percent"]["span"]
        b["LLI_percent"]["span"] += 1.
        b["LLI_percent"]["max"] += 1.
        assert math.isclose(b["LLI_percent"]["max"] - b["LLI_percent"]["min"],
                            b["LLI_percent"]["span"], rel_tol=1e-12)
        publish(old, a, "r7-current-A")
        b_bytes = publish(new, b, "r7-rerun-B")
        legacy_name = source.stem + "_v2.json"
        (old / legacy_name).write_bytes(b_bytes)
        # The normal current reader excludes the numbered sibling, while the
        # normal --old directory CLI silently gives it the historical rule.
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            selected = compare.load_degeneracy(old)["100"]
        assert selected["j"]["LLI_percent"]["span"] == old_span
        assert "archive" in err.getvalue()
        argv = [sys.executable, str(root / "scripts/check_u14.py"), "--new", str(new), "--old", str(old)]
        p = subprocess.run(argv, cwd=root, text=True, capture_output=True)
        assert p.returncode == 0, (p.returncode, p.stdout, p.stderr)
        assert legacy_name in p.stdout and "compare_states" in p.stdout
        assert check.baseline_for(new / source.name, old).name == legacy_name
        emit("R7_CURRENT_BASELINE_POLICY_SPLIT", {"current_reader_file": selected["file"],
            "current_span": old_span, "rerun_span": b["LLI_percent"]["span"],
            "historical_helper_file": legacy_name, "cli_rc": p.returncode,
            "cli_stdout": p.stdout, "current_reader_stderr": err.getvalue(),
            "synthetic_fixture_from_public_schema": True,
            "committed_current_out_has_numbered_siblings": False})
        # Negative control: without the ignored sibling, the very same new
        # data is correctly reported as numerically different from current A.
        (old / legacy_name).unlink()
        q = subprocess.run(argv, cwd=root, text=True, capture_output=True)
        assert q.returncode == 1, (q.returncode, q.stdout, q.stderr)
        emit("R7_CURRENT_BASELINE_NEGATIVE_CONTROL", {"numbered_sibling_removed": True,
            "unchanged_rerun_vs_current_cli_rc": q.returncode, "stdout": q.stdout})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, default=Path.cwd())
    parser.add_argument("--old", type=Path, help="Extracted bfc4623^/bms-balancing/out, required for --case u14/all")
    parser.add_argument("--previous", type=Path, help="Optional d431404 bms-balancing checkout for 12 bytewise comparisons")
    parser.add_argument("--case", choices=("all", "closure", "scale", "matrix", "u13", "argmin", "overflow", "derived", "u14", "table", "canon", "docs", "baseline"), default="all")
    args = parser.parse_args()
    root = args.target.resolve()
    sys.path.insert(0, str(root))
    tests = load_tests(root)
    cases = {"closure": lambda: positive_closure(tests), "scale": scale_domains,
             "matrix": lambda: matrix_independent_axes(tests), "u13": lambda: u13_coverage(root, tests),
             "argmin": scale_equivalence_not_argmin_equivalence,
             "overflow": finite_reduction_overflow_stress,
             "derived": lambda: derived_closure_and_grid(root),
             "u14": lambda: u14_compare(root, args.old.resolve()),
             "table": lambda: section5_printed_rows(root),
             "canon": lambda: r7_current_canonical(root, tests, args.previous.resolve() if args.previous else None),
             "docs": lambda: r7_document_closures(root),
             "baseline": lambda: r7_baseline_policy_split(root)}
    for name, fn in cases.items():
        if args.case == name or (args.case == "all" and name != "overflow"): fn()
    print("R7_INFERENCE_CHECKS_PASSED")
