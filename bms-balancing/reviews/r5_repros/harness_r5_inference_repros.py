"""R5 bounded numerical/evidence checks; never edits the reviewed checkout.

Synthetic forwards and temporary artifact copies are explicitly labeled.
No private cell data or private MATLAB code is used.
"""
from __future__ import annotations

import argparse
import contextlib
import csv
import importlib.util
import io
import json
from pathlib import Path
import re
import sys
import tempfile
from types import SimpleNamespace
from unittest.mock import patch
import warnings


def emit(name, obj):
    print(name + " " + json.dumps(obj, ensure_ascii=False, allow_nan=False))


def load_tests(root):
    spec = importlib.util.spec_from_file_location("r5_inference_tests", root / "tests/test_review_findings.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def make_plateau(tests):
    import numpy as np
    from bms_balancing.model import Objective, LB5, UB5

    class Plateau(tests._FinitePlateau, Objective):
        def __init__(self):
            tests._FinitePlateau.__init__(self)
            self.c_cell = 1.
            self.scale_seed, self.n_scale_samples = 0, 50
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.scales = self._auto_scales(0, 50)

    obj = Plateau()
    candidates = LB5 + np.random.default_rng(0).random((50, 5)) * (UB5 - LB5)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        good = next(p for p in candidates if np.isfinite(obj.rmse_dqdv(p)))
    return obj, good


def closure_checks(root, tests):
    with tempfile.TemporaryDirectory(prefix="r5-audit-positive-") as td:
        tests.test_r4_05_auto_scale_records_its_nonfinite_policy_and_findings_limits_u1(Path(td))
    tests.test_u12_scale_audit_transcript_has_no_nonfinite_samples_and_section_1_13_scopes_u1()
    tests.test_section_1_8_192_values_are_backed_by_committed_recompare_artifacts()
    obj, _ = make_plateau(tests)
    assert obj.scale_audit["dqdv"] == {"n": 50, "n_finite": 14, "n_inf": 36, "n_nan": 0}
    emit("R4_05_POSITIVE_CLOSURE", {"actual_regressions_passed": 3,
         "synthetic_plateau_audit": obj.scale_audit,
         "scale_dqdv": obj.scales["dqdv"], "private_matlab_run": False})


def audit_population_counterexample(root, tests):
    transcript = (root / "out/scale_audit_eval.txt").read_text(encoding="utf-8")
    lines = [s for s in transcript.splitlines() if s.startswith("# scale_audit,")]
    assert len(lines) == 16
    with tempfile.TemporaryDirectory(prefix="r5-audit-population-") as td:
        scratch = Path(td)
        (scratch / "out").mkdir()
        (scratch / "FINDINGS.md").write_text((root / "FINDINGS.md").read_text(encoding="utf-8"), encoding="utf-8")
        fake = scratch / "out/scale_audit_eval.txt"
        # A test-fixture counterexample, not a claim about how the user ran U12.
        # Exactly ONE preserved source record, repeated sixteen times; no builds run here.
        fake.write_text("## NEGATIVE FIXTURE: one root/state record repeated 16 times, NOT a 4x4 population.\n"
                        + (lines[0] + "\n") * 16, encoding="utf-8")
        with patch.object(tests, "ROOT", scratch):
            tests.test_u12_scale_audit_transcript_has_no_nonfinite_samples_and_section_1_13_scopes_u1()
            emit("U12_DUPLICATED_POPULATION_ACCEPTED", {
                "source_records": 1, "emitted_lines": 16, "actual_4x4_coverage": False,
                "actual_production_regression": "PASS", "committed_distinct_audit_lines": len(set(lines)),
                "does_not_prove_user_runs_missing": True})
            fake.write_text(fake.read_text(encoding="utf-8").replace(
                "dqdv:n=50/finite=50/inf=0/nan=0", "dqdv:n=50/finite=49/inf=1/nan=0", 1), encoding="utf-8")
            try:
                tests.test_u12_scale_audit_transcript_has_no_nonfinite_samples_and_section_1_13_scopes_u1()
            except AssertionError:
                emit("U12_NONFINITE_NEGATIVE_CONTROL", {"rejected": True})
            else:
                raise AssertionError("Nonfinite control unexpectedly accepted")


def audit_scope_counterexample(root):
    from bms_balancing import verify
    rows = []
    for file in sorted((root / "out/recompare").glob("dd_eval_*_r2.csv")):
        header = file.read_text(encoding="utf-8").splitlines()[0]
        source = re.search(r"halfcell=\S*/(GITT|step_005C)/", header).group(1)
        si = re.search(r"Si=(\S+)", header).group(1)
        state = re.search(r"state=(\S+)", header).group(1)
        anchors, values, cols = verify.read_dd_eval_csv(file)
        n = len(anchors) + len(values) * (len(cols) - 5)
        in_scope = source == "GITT" and si == "Li" and state in ("pristine", "100", "200", "300_0009")
        rows.append({"file": file.name, "half_cell": source, "si": si, "state": state,
                     "compared_values": n, "inside_stated_U12_configuration_scope": in_scope})
    assert sum(r["compared_values"] for r in rows) == 192
    covered = sum(r["compared_values"] for r in rows if r["inside_stated_U12_configuration_scope"])
    assert covered == 96
    text = (root / "FINDINGS.md").read_text(encoding="utf-8")
    assert "§1-8 의 192 값과 A축 산출" in text
    emit("U12_192_VALUE_SCOPE_MISMATCH", {"document_implies_inside": 192,
         "at_most_inside_reported_configurations": covered, "rows": rows,
         "192_empirical_value_comparison_invalidated": False})


def matrix_audit_not_emitted(root, tests):
    from bms_balancing import verify
    with tempfile.TemporaryDirectory(prefix="r5-matrix-audit-") as td:
        scratch = Path(td)
        data_stub = scratch / "present.xlsx"
        data_stub.write_text("synthetic presence fixture only", encoding="utf-8")
        output = scratch / "matrix.csv"
        actual_build_audits = []

        def synthetic_build(*args, **kwargs):
            obj, _ = make_plateau(tests)
            actual_build_audits.append(obj.scale_audit)
            return obj

        def deterministic_fit(obj, **kwargs):
            _, good = make_plateau(tests)
            return good, obj(good), []

        args = SimpleNamespace(data_root=str(scratch), source="GITT", state="100", seed=0,
                               starts=1, w_dqdv=1., only_source=True, only_wdqdv=True,
                               out=str(output), run_id="synthetic-audit-counterexample")
        captured = io.StringIO()
        with patch.object(verify.D, "data_root", return_value=scratch), \
             patch.object(verify.D, "HALF_FILE", {"GITT": {"pristine": "unused", "100": "unused"}}), \
             patch.object(verify.D, "SI_SOURCES", ("Li",)), \
             patch.object(verify.D, "half_cell_path", return_value=data_stub), \
             patch.object(verify, "build", side_effect=synthetic_build), \
             patch.object(verify, "multistart", side_effect=deterministic_fit), \
             contextlib.redirect_stdout(captured):
            verify.cmd_matrix(args)
        with output.open(encoding="utf-8") as stream:
            rows = list(csv.DictReader(stream))
        assert len(actual_build_audits) == 2 and len(rows) == 1
        assert all(a["dqdv"]["n_inf"] == 36 for a in actual_build_audits)
        audit_fields = [k for k in rows[0] if "audit" in k or "scale" in k]
        assert not audit_fields and "scale_audit" not in captured.getvalue()
        emit("MATRIX_DROPS_LIVE_NONFINITE_AUDIT", {
            "actual_command": "verify.cmd_matrix", "synthetic_forward": True,
            "reference_n_inf": 36, "target_n_inf": 36, "w_dqdv": rows[0]["w_dqdv"],
            "published_rows": len(rows),
            "audit_or_scale_csv_fields": audit_fields, "stdout_audit_present": False,
            "fit_stubbed_only_for_bounded_serialization_check": True})


def exception_audit_count_counterexample():
    from bms_balancing.model import Objective

    class SecondMetricRaises(Objective):
        def __init__(self):
            self.use_peak_weight = False
            self.pocv_calls = 0
        def rmse_pocv(self, p):
            self.pocv_calls += 1
            return 1.
        def rmse_dvdq(self, p):
            raise ValueError("controlled second-metric failure")
        def rmse_dqdv(self, p, weighted=False):
            raise AssertionError("not reached")

    obj = SecondMetricRaises()
    scales = obj._auto_scales(0, 50)
    assert obj.pocv_calls == 50
    assert obj.scale_audit["pocv"] == {"n": 100, "n_finite": 50, "n_inf": 0, "n_nan": 50}
    emit("EXCEPTION_PATH_DOUBLE_COUNTS_SAMPLES", {"requested_samples": 50,
         "actual_pocv_calls": obj.pocv_calls, "scale_audit": obj.scale_audit,
         "scales": scales, "all_finite_false_acceptance": False})


def finite_does_not_bound_epsilon_error():
    import numpy as np
    from bms_balancing.model import Objective

    class SmallFiniteMetric(Objective):
        def __init__(self):
            self.use_peak_weight = False
            self.w_pocv = self.w_dvdq = self.w_dqdv = 1.
        def rmse_pocv(self, p): return 1e-20
        def rmse_dvdq(self, p): return 1e-20
        def rmse_dqdv(self, p, weighted=False): return 1e-20

    obj = SmallFiniteMetric()
    obj.scales = obj._auto_scales(0, 50)
    port_scales = dict(obj.scales)
    port_value = obj(np.zeros(5))
    # Only the formula printed as the original in FINDINGS §1-13 is used.
    # No assertion is made that actual cell errors have this magnitude.
    reported_original_mean = float(np.mean(np.sort(np.full(50, 1e-20))[:25]))
    obj.scales = {key: reported_original_mean for key in obj.scales}
    original_formula_value = obj(np.zeros(5))
    assert all(a == {"n": 50, "n_finite": 50, "n_inf": 0, "n_nan": 0}
               for a in obj.scale_audit.values())
    ratio = port_scales["pocv"] / reported_original_mean
    assert ratio > 22000 and original_formula_value / port_value > 22000
    emit("ALL_FINITE_AUDIT_DOES_NOT_BOUND_EPS_ERROR", {
         "synthetic_constant_rmse": 1e-20, "scale_audit": obj.scale_audit,
         "reported_original_lower_half_mean": reported_original_mean,
         "port_scale": port_scales["pocv"], "scale_ratio": ratio,
         "objective_with_port_scales": port_value,
         "objective_with_reported_original_scales": original_formula_value,
         "private_matlab_run": False, "real_cell_scale_magnitude_claim": False})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, default=Path.cwd())
    parser.add_argument("--case", choices=("all", "closure", "population", "scope", "matrix", "exception", "epsilon"), default="all")
    args = parser.parse_args()
    root = args.target.resolve()
    sys.path.insert(0, str(root))
    tests = load_tests(root)
    cases = {"closure": lambda: closure_checks(root, tests),
             "population": lambda: audit_population_counterexample(root, tests),
             "scope": lambda: audit_scope_counterexample(root),
             "matrix": lambda: matrix_audit_not_emitted(root, tests),
             "exception": exception_audit_count_counterexample,
             "epsilon": finite_does_not_bound_epsilon_error}
    for name, fn in cases.items():
        if args.case in ("all", name):
            fn()
    print("R5_INFERENCE_REPRO_ASSERTIONS_PASSED")
