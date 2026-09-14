"""Data-free and committed-artifact counterexamples for the R3 gamma claims.

Does not edit the target. Synthetic measurements replace only the external data
source; actual Blend and ne_shape.main execute from the reviewed checkout.
"""
from __future__ import annotations

import argparse
import contextlib
import csv
import importlib.util
import io
import json
from pathlib import Path
import sys
from unittest.mock import patch


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def artifact_headroom(root):
    from bms_balancing.model import LB5, UB5
    ns = load("r3_shape_artifact", root / "scripts/ne_shape.py")
    rows = list(csv.DictReader((root / "out/ne_shape_GITT_Li.csv").open(encoding="utf-8")))
    result = []
    for row in rows:
        target, reference = ns.fitted_pair(root / "out", row["state"], "GITT", "Li")
        slope = float(row["gamma_shape_mV"]) / abs(target - reference)
        needed = float(row["measured_shape_mV"]) / slope
        signs = {"positive": reference + needed, "negative": reference - needed}
        entry = {
            "state": row["state"], "gamma_reference": reference,
            "allowed_gamma_interval": [float(LB5[4]), float(UB5[4])],
            "legal_negative_delta": float(LB5[4] - reference),
            "legal_positive_delta": float(UB5[4] - reference),
            "fitted_secant_slope_mV_per_gamma": slope,
            "document_extrapolated_delta_magnitude": needed,
            "extrapolated_gamma_plus": signs["positive"],
            "extrapolated_gamma_minus": signs["negative"],
            "either_sign_fits_bounds": any(LB5[4] <= val <= UB5[4] for val in signs.values()),
        }
        result.append(entry)
    aged = next(row for row in result if row["state"] == "300_0009")
    assert not aged["either_sign_fits_bounds"]
    return result


def execute_shape(root, name, reference, fitted, true_gamma=None, measured_offset=0.0):
    import numpy as np
    from bms_balancing.model import Blend
    ns = load("r3_ne_shape_" + name, root / "scripts/ne_shape.py")
    u = np.linspace(0.0, 1.0, 301)
    arrays = ((1-u)**2, 0.1 + 0.7*u, 1-u, 0.1 + 0.7*u)
    blend = Blend(*arrays, window=11, poly_order=3)

    class SyntheticPath:
        def __init__(self, state):
            self.state = state

        def is_file(self):
            return True

    class SyntheticHalfCell:
        def __init__(self, path, **unused):
            self.state = path.state

        def E_PE(self, x):
            return 4.2 - 0.7 * np.asarray(x)

        def E_NE(self, x):
            if self.state == "pristine":
                return blend.E(x, reference)
            return blend.E(x, reference if true_gamma is None else true_gamma) + measured_offset

    captured = io.StringIO()
    with contextlib.ExitStack() as stack:
        stack.enter_context(patch.object(ns.D, "STATES", ["pristine", "100"]))
        stack.enter_context(patch.object(ns.D, "data_root", return_value=Path("unused")))
        stack.enter_context(patch.object(ns.D, "half_cell_path", side_effect=lambda r, s, st: SyntheticPath(st)))
        stack.enter_context(patch.object(ns.D, "load_literature", return_value=arrays))
        stack.enter_context(patch.object(ns, "HalfCell", SyntheticHalfCell))
        stack.enter_context(patch.object(ns, "raw_ne_capacity", return_value=1.0))
        stack.enter_context(patch.object(ns, "fitted_pair", return_value=(fitted, reference)))
        stack.enter_context(patch.object(sys, "argv", ["ne_shape.py", "--write", ""]))
        stack.enter_context(contextlib.redirect_stdout(captured))
        rc = ns.main()
    observed = captured.getvalue()
    measured = SyntheticHalfCell(SyntheticPath("100")).E_NE(ns.GRID)
    pristine = blend.E(ns.GRID, reference)
    a = float(np.max(np.abs(measured - pristine))) * 1e3
    b = float(np.max(np.abs(blend.E(ns.GRID, fitted) - pristine))) * 1e3
    assert rc == 0 and b / a < 0.34
    assert "같은 크기를 낼 Δγ 는 상자 안에 있다" in observed
    assert "블렌드 모양이 아니라는(모델 부적합)" in observed
    # The synthetic Si/Gr curves have the same endpoint normalization and a
    # fixed ordering at every voltage. Their convex mixture has a fixed
    # monotone ordering in gamma, so the gamma endpoints bound every E(x,g).
    e0, e5 = blend.E(ns.GRID, 0.0), blend.E(ns.GRID, 0.5)
    envelope_min, envelope_max = np.minimum(e0, e5), np.maximum(e0, e5)
    maximum_endpoint_change = float(np.max(np.maximum(abs(e0-pristine), abs(e5-pristine)))) * 1e3
    dense_check = max(float(np.max(np.abs(blend.E(ns.GRID, g)-pristine))) * 1e3 for g in np.linspace(0, .5, 1001))
    assert abs(maximum_endpoint_change - dense_check) < 1e-9
    result = {
        "fixture": name, "reference_gamma": reference, "supplied_fitted_gamma": fitted,
        "capacity_change_percent": 0.0, "PE_curve_change_mV": 0.0,
        "measured_change_mV": a, "realized_gamma_change_mV": b, "ratio": b/a,
        "actual_stdout": [line.strip() for line in observed.splitlines()
                          if "상자 안" in line or "블렌드 모양이" in line],
        "whole_gamma_family_max_change_mV": maximum_endpoint_change,
    }
    if true_gamma is not None and measured_offset == 0:
        error = float(np.max(np.abs(blend.E(ns.GRID, true_gamma) - measured)))
        assert error == 0.0
        result.update({"exact_representing_gamma": true_gamma, "exact_representation_error_V": error})
    else:
        outside = np.maximum(np.maximum(envelope_min - measured, measured - envelope_max), 0.0)
        min_uniform_error_lower_bound = float(np.max(outside))
        assert a > maximum_endpoint_change and min_uniform_error_lower_bound > 0
        result.update({"no_legal_gamma_can_match_change_amplitude": True,
                       "uniform_error_lower_bound_V": min_uniform_error_lower_bound})
    return result


def preserved_corrections(root):
    ns = load("r3_shape_roles", root / "scripts/ne_shape.py")
    rows = list(csv.DictReader((root / "out/ne_shape_GITT_Li.csv").open(encoding="utf-8")))
    for row in rows:
        target, reference = ns.fitted_pair(root / "out", row["state"], "GITT", "Li")
        assert abs(float(row["gamma_target"]) - target) < 1e-6
        assert abs(float(row["gamma_ref"]) - reference) < 1e-6
    audit = load("r3_audit97", root / "scripts/audit97.py")
    arithmetic = audit.mode_arithmetic(list(audit.load_rows()))
    strong = [row for row in arithmetic["neg"] if row["LAM_NE"] < -10]
    thresholds = sorted(row["need"] * row["a_NE_ref"] for row in strong)
    assert len(strong) == 5
    return {"gamma_target_and_ref_match_matrix": True,
            "strong_negative_rows": len(strong), "exact_zero_thresholds": thresholds,
            "original_97row_arithmetic_max_error_pct_points": arithmetic["worst"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=Path, default=Path(__file__).resolve().parents[1] / "work/harness-r3-target/bms-balancing")
    args = ap.parse_args()
    sys.path.insert(0, str(args.target))
    result = {
        "committed_gamma_headroom": artifact_headroom(args.target),
        "exactly_representable_but_diagnosed_as_model_mismatch": execute_shape(args.target, "representable", .15, .16, true_gamma=.45),
        "amplitude_outside_family_but_reported_as_inside_bounds": execute_shape(args.target, "amplitude_outside", .25, .26, measured_offset=.10),
        "R2_corrections_preserved": preserved_corrections(args.target),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
