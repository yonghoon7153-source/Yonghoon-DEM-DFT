"""Benign, data-free numerical checks for the R2 scientific claims.

Run with the target's requirements available. This reads target code and committed
artifacts; it does not change the checkout or access private measurements.
"""
from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import json
import math
from pathlib import Path
import sys
from unittest.mock import patch


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def gamma_realized_is_not_capacity(root):
    import numpy as np
    from bms_balancing.model import Blend, degradation_modes

    ns = load("review_ne_shape", root / "scripts/ne_shape.py")
    u = np.linspace(0, 1, 301)
    arrays = ((1 - u) ** 2, 0.1 + 0.7 * u, 1 - u, 0.1 + 0.7 * u)
    blend = Blend(*arrays, window=11, poly_order=3)
    ref_gamma, true_gamma, fitted_gamma = 0.15, 0.45, 0.16

    class InputPath:
        def __init__(self, state):
            self.state = state

        def is_file(self):
            return True

    class SyntheticHalfCell:
        def __init__(self, path, **kwargs):
            self.gamma = ref_gamma if path.state == "pristine" else true_gamma

        def E_NE(self, x):
            return blend.E(x, self.gamma)

    captured = io.StringIO()
    with contextlib.ExitStack() as stack:
        stack.enter_context(patch.object(ns.D, "STATES", ["pristine", "100"]))
        stack.enter_context(patch.object(ns.D, "data_root", return_value=Path("unused")))
        stack.enter_context(patch.object(ns.D, "half_cell_path", side_effect=lambda r, s, st: InputPath(st)))
        stack.enter_context(patch.object(ns.D, "load_literature", return_value=arrays))
        stack.enter_context(patch.object(ns, "HalfCell", SyntheticHalfCell))
        stack.enter_context(patch.object(ns, "raw_ne_capacity", return_value=1.0))
        stack.enter_context(patch.object(ns, "fitted_pair", return_value=(fitted_gamma, ref_gamma)))
        stack.enter_context(patch.object(sys, "argv", ["ne_shape.py", "--write", ""]))
        stack.enter_context(contextlib.redirect_stdout(captured))
        rc = ns.main()
    observed = captured.getvalue()
    da = float(np.max(np.abs(blend.E(ns.GRID, true_gamma) - blend.E(ns.GRID, ref_gamma)))) * 1000
    db = float(np.max(np.abs(blend.E(ns.GRID, fitted_gamma) - blend.E(ns.GRID, ref_gamma)))) * 1000
    exact_error = float(np.max(np.abs(blend.E(ns.GRID, true_gamma) - SyntheticHalfCell(InputPath("100")).E_NE(ns.GRID))))
    assert rc == 0 and db / da < 0.34 and exact_error == 0
    assert "표현할 수 있는 것보다" in observed and "그것이 곧 LAM_NE" in observed
    pref = [1.1, -0.1, 1.1, -0.05, 0.25]
    p = pref.copy()
    p[3] -= 0.01
    changed_modes = degradation_modes(pref, 1.0, p, 1.0)
    assert changed_modes["LAM_NE"] == 0.0 and changed_modes["LLI"] != 0.0
    return {
        "synthetic_input": "Measured OCPs are exact curves of the unmodified target Blend; equal capacities.",
        "reference_gamma": ref_gamma,
        "true_target_gamma": true_gamma,
        "supplied_fitted_target_gamma": fitted_gamma,
        "measured_change_mV": da,
        "realized_fitted_gamma_change_mV": db,
        "reported_ratio": db / da,
        "exact_representing_gamma_error_V": exact_error,
        "actual_stdout_conclusion": [line.strip() for line in observed.splitlines() if "표현할 수 있는" in line or "그것이 곧" in line],
        "b_NE_only_change_modes": changed_modes,
    }


def negative_threshold(root):
    audit = load("review_audit97", root / "scripts/audit97.py")
    rows = audit.mode_arithmetic(list(audit.load_rows()))["neg"]
    strong = [row for row in rows if row["LAM_NE"] < -10]
    checks = []
    for row in strong:
        threshold = row["a_NE_ref"] * row["need"]
        checks.append({
            "file": row["file"], "config": row["config"],
            "reported_LAM_NE_pct": row["LAM_NE"],
            "exact_zero_threshold_a_NE": threshold,
            "LAM_NE_pct_if_target_upper_bound_1_19_ref_fixed": 100 * (1 - 1.19 / threshold),
            "LAM_NE_pct_if_target_interior_1_30_ref_fixed": 100 * (1 - 1.30 / threshold),
        })
    assert len(checks) == 5
    assert any(row["LAM_NE_pct_if_target_upper_bound_1_19_ref_fixed"] < 0 for row in checks)
    return checks


def objective_normalization():
    records = []
    for best in [0.25, 1.0]:
        width = math.sqrt(0.01 * best)
        records.append({"objective": f"{best} + x**2", "curvature": 2,
                        "relative_1pct_halfwidth": width,
                        "document_normalized_halfwidth": width / best,
                        "quadratic_halfwidth_over_sqrt_best": width / math.sqrt(best)})
    assert records[0]["document_normalized_halfwidth"] != records[1]["document_normalized_halfwidth"]
    assert records[0]["quadratic_halfwidth_over_sqrt_best"] == records[1]["quadratic_halfwidth_over_sqrt_best"]
    return {"same_curvature_different_baseline": records,
            "scale_invariance": "Multiplying any whole objective by k>0 preserves its relative near-optimal set exactly, but (halfwidth/best) changes by 1/k."}


def interval_hull_overlap(root):
    import ast
    source = (root / "tests/test_review_findings.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    function = next(node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name == "overlaps")
    isolated = ast.Module(body=[function], type_ignores=[])
    scope = {}
    exec(compile(isolated, "target_test_overlap_predicate", "exec"), scope)
    # For A: J=1+[x(x-4)]**2. For B: J=1+(x-2)**2.
    # Both best=1 and the relative 1% cap is 1.01.
    observed_a = {"LLI": (0.0, 2.0, 0.0, 4.0)}
    observed_b = {"LLI": (2.0, 0.1, 1.9, 2.1)}
    overlap = scope["overlaps"](observed_a, observed_b, "LLI")
    minimum_a_on_b = 1 + (1.9 * (1.9 - 4)) ** 2
    assert overlap and minimum_a_on_b > 1.01
    return {"A_objective": "1+[x(x-4)]**2", "B_objective": "1+(x-2)**2",
            "relative_tolerance": 0.01, "observed_feasible_A_modes": [0.0, 4.0],
            "all_feasible_B_modes": [1.9, 2.1],
            "actual_target_test_predicate_reports_overlap": overlap,
            "minimum_A_objective_on_all_B_feasible_modes": minimum_a_on_b,
            "maximum_allowed_objective": 1.01,
            "actual_feasible_sets_intersect": False}


def committed_normalization(root):
    compare = load("review_compare_scales", root / "scripts/compare_states.py")
    groups = {"pouch": [], "cylindrical": []}
    for directory, group in [("out", "pouch"), ("out/cells_pouch_fixedhc", "pouch"),
                             ("out/cells_c168", "cylindrical"), ("out/cells_c171", "cylindrical")]:
        for entry in compare.load_degeneracy(root / directory).values():
            record = entry["j"]
            groups[group].append((record["best_obj"], record["LLI_percent"]["span"] / 2))
    ratios = {}
    for power, label in [(0.0, "raw"), (1.0, "document_width_over_best"), (0.5, "quadratic_illustration_width_over_sqrt_best")]:
        ratios[label] = max(width / best ** power for best, width in groups["cylindrical"]) / max(width / best ** power for best, width in groups["pouch"])
    ratios["document_ratio_if_cylindrical_objectives_renamed_times_100"] = ratios["document_width_over_best"] / 100
    return ratios


def transportability_completion():
    # Rounded state-200 committed widths, exactly as FINDINGS table 1-12 prints.
    # C0 is unobserved: any positive value leaves all four observed data unchanged.
    observed = {"pouch_unsubstituted": 0.43, "pouch_substituted": 0.46,
                "c168_substituted": 6.07, "c171_substituted": 4.68}
    completions = []
    for label, unobserved in [("zero cylindrical treatment effect", (6.07, 4.68)),
                              ("all cylindrical excess caused by substitution", (0.43, 0.43))]:
        completions.append({"model": label,
                            "c168_unsubstituted_unobserved": unobserved[0],
                            "c171_unsubstituted_unobserved": unobserved[1],
                            "c168_substitution_effect": observed["c168_substituted"] - unobserved[0],
                            "c171_substitution_effect": observed["c171_substituted"] - unobserved[1]})
    return {"same_observed_data": observed, "compatible_completions": completions}


def artifact_gamma_label(root):
    import csv
    ns = load("review_ne_shape_labels", root / "scripts/ne_shape.py")
    rows = list(csv.DictReader((root / "out/ne_shape_GITT_Li.csv").open()))
    out = []
    for row in rows:
        target_gamma, reference_gamma = ns.fitted_pair(root / "out", row["state"], "GITT", "Li")
        saved = float(row["gamma_ref"])
        assert abs(saved - target_gamma) < 1e-6
        out.append({"state": row["state"], "column_named_gamma_ref": saved,
                    "actual_target_gamma": target_gamma,
                    "actual_reference_gamma": reference_gamma})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1] / "work/harness-r2-target/bms-balancing")
    args = ap.parse_args()
    sys.path.insert(0, str(args.root))
    result = {
        "gamma_capacity": gamma_realized_is_not_capacity(args.root),
        "negative_lam_threshold": negative_threshold(args.root),
        "objective_normalization": objective_normalization(),
        "committed_normalization": committed_normalization(args.root),
        "interval_hull_overlap": interval_hull_overlap(args.root),
        "halfcell_causal_identification": transportability_completion(),
        "artifact_gamma_label": artifact_gamma_label(args.root),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
