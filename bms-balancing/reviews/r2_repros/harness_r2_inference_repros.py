"""R2 scientific-inference counterexamples; run from target bms-balancing/.

No private data, network calls, or target-file writes.  The analytic examples
exercise the committed production extrema and profile implementations.
"""
from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import json
import math
import pathlib
import sys
import warnings


def normalization():
    """Equal objective curvature is not corrected by width / best_obj."""
    rows = []
    for base in (0.30, 0.75):
        curvature = 100.0
        halfwidth = math.sqrt(0.01 * base / curvature)
        rows.append({"best_obj": base, "objective": f"{base} + 100*x*x",
                     "halfwidth": halfwidth,
                     "halfwidth_over_best": halfwidth / base,
                     "halfwidth_over_sqrt_best": halfwidth / math.sqrt(base)})
    print("NORMALIZATION_QUADRATIC", json.dumps(rows))
    print("NORMALIZATION_SAME_CURVATURE_RATIO", rows[1]["halfwidth_over_best"] /
          rows[0]["halfwidth_over_best"])
    assert math.isclose(rows[0]["halfwidth_over_sqrt_best"],
                        rows[1]["halfwidth_over_sqrt_best"])
    assert not math.isclose(rows[0]["halfwidth_over_best"],
                            rows[1]["halfwidth_over_best"])

    # Multiplying the entire objective by 10 changes neither its optimum nor
    # the relative 1% set.  A purported correction should not invent a 10x gap.
    base, width = 0.30, rows[0]["halfwidth"]
    print("NORMALIZATION_SCALE_INVARIANCE", json.dumps({
        "f": "0.30 + 100*x*x", "g": "10*f",
        "same_relative_feasible_set": True,
        "raw_width_ratio": 1.0,
        "normalized_width_ratio": (width / (10 * base)) / (width / base)}))

    # The stored best/width pair does not identify response at a common tolerance.
    # Two nonnegative objectives have fixed points f(0)=.5, f(.01)=.505 and
    # g(0)=.75, g(.1)=.7575; g enters a shallow tail after radius .002.
    # The current per-best 1% comparison gives a 10x raw / 6.667x "corrected"
    # gap.  Re-evaluating both at excess loss .005 reverses it to .2x.
    def f(x):
        return 0.5 + 50 * x * x

    def g(x):
        radius = abs(x)
        return 0.75 + (1250 * radius * radius if radius <= .002 else
                       .005 + .0025 * (radius - .002) / .098)

    assert math.isclose(f(.01), .505)
    assert math.isclose(g(.1), .7575)
    assert math.isclose(g(.002), .755)
    print("NORMALIZATION_COMMON_TOL_REVERSAL", json.dumps({
        "pouch_relative_halfwidth": .01, "cylinder_relative_halfwidth": .1,
        "relative_width_ratio": 10., "width_over_best_ratio": (.1/.75)/(.01/.5),
        "common_excess_loss": .005, "common_loss_width_ratio": .002/.01,
        "note": "Analytic counterexample, not a rerun or estimate of real cells."}))


def artifact_display(root):
    spec = importlib.util.spec_from_file_location("r2_compare_states", root / "scripts/compare_states.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    capture = io.StringIO()
    previous_argv = sys.argv
    try:
        sys.argv = [str(root / "scripts/compare_states.py"),
                    "c168=" + str(root / "out/cells_c168")]
        with contextlib.redirect_stdout(capture):
            assert mod.main() == 0
    finally:
        sys.argv = previous_argv
    production_rows = [s for s in capture.getvalue().split("B. 모델 선택")[0].splitlines()
                       if "300_0009" in s or "degeneracy_200" in s]
    assert any("2.30±4.35" in s for s in production_rows)
    assert any("8.01±6.07" in s for s in production_rows)
    print("TARGET_COMPARE_STATES_ROWS", json.dumps(production_rows, ensure_ascii=False))
    all_rows = []
    for label, sub in (("pouch", "out"), ("fixedhc", "out/cells_pouch_fixedhc"),
                       ("c168", "out/cells_c168"), ("c171", "out/cells_c171")):
        for state, entry in mod.load_degeneracy(root / sub).items():
            j = entry["j"]
            for mode in mod.MODES:
                band, best = j[mode + "_percent"], j["best_modes_percent"][mode]
                width = band["span"] / 2
                all_rows.append({"cell": label, "state": state, "mode": mode,
                                 "actual_min": band["min"], "actual_max": band["max"],
                                 "printed": f"{best:.2f}±{width:.2f}",
                                 "implied_min": best - width, "implied_max": best + width,
                                 "center_error": best - (band["min"] + band["max"]) / 2})
    worst = sorted(all_rows, key=lambda r: abs(r["center_error"]), reverse=True)[:6]
    print("ARTIFACT_MIS_CENTERED_INTERVALS", json.dumps(worst))
    example = next(r for r in all_rows if
                   (r["cell"], r["state"], r["mode"]) == ("c168", "300_0009", "LAM_NE"))
    assert example["actual_min"] > 2.3 and example["implied_min"] < -2.0
    assert example["actual_max"] > 11 and example["implied_max"] < 6.7
    # The table's 8x value is arithmetically reproduced, not endorsed.
    groups = []
    for subs in (("out", "out/cells_pouch_fixedhc"), ("out/cells_c168", "out/cells_c171")):
        group = []
        for sub in subs:
            for e in mod.load_degeneracy(root / sub).values():
                j = e["j"]
                group.append((j["best_obj"], j["LLI_percent"]["span"]/2))
        groups.append(group)
    print("ARTIFACT_LLI_RATIOS", json.dumps({
        "raw": max(w for b,w in groups[1])/max(w for b,w in groups[0]),
        "width_over_best": max(w/b for b,w in groups[1])/max(w/b for b,w in groups[0]),
        "quadratic_approximation_only_width_over_sqrt_best":
            max(w/math.sqrt(b) for b,w in groups[1])/max(w/math.sqrt(b) for b,w in groups[0])}))


def disconnected_hulls(root):
    sys.path.insert(0, str(root))
    import numpy as np
    from bms_balancing.verify import near_optimal_extrema, mode_profile_extrema
    ref = np.array([1.2, -.1, 1.2, -.1, .25])
    radius = .005
    rows = []
    for tag, centers in (("A", (1.04, 1.36)), ("B", (1.16, 1.24))):
        def objective(p, centers=centers):
            return 1.0 + 400.0 * min((p[0] - c) ** 2 for c in centers)
        best = ref.copy()
        best[0] = centers[0]
        other = ref.copy()
        other[0] = centers[1]
        ext = near_optimal_extrema(objective, ref, 1., 1., best, 1., .01,
                                  seeds=[other], n_starts=1, seed=0)
        prof = mode_profile_extrema(objective, ref, 1., 1., best, 1., .01,
                                    n_grid=21, n_starts=1, seed=0,
                                    hint={k:(v["min"],v["max"]) for k,v in ext.items()})
        band = [min(ext["LAM_PE"]["min"], prof["LAM_PE"]["min"]),
                max(ext["LAM_PE"]["max"], prof["LAM_PE"]["max"])]
        components = sorted([[100*(1-(c+radius)/1.2), 100*(1-(c-radius)/1.2)] for c in centers])
        rows.append({"state": tag, "target_returned_hull": band,
                     "exact_feasible_components": components,
                     "is_lower_bound": ext["LAM_PE"]["is_lower_bound"],
                     "profile_grid_hits": prof["LAM_PE"]["n_grid_attainable"]})
    hull_overlap = min(r["target_returned_hull"][1] for r in rows) - max(
        r["target_returned_hull"][0] for r in rows)
    component_overlap = any(min(a[1], b[1]) >= max(a[0], b[0])
                            for a in rows[0]["exact_feasible_components"]
                            for b in rows[1]["exact_feasible_components"])
    print("DISCONNECTED_TARGET_OUTPUT", json.dumps(rows))
    print("DISCONNECTED_VERDICT", json.dumps({"hull_overlap_percentage_points": hull_overlap,
                                              "actual_shared_mode_exists": component_overlap}))
    assert hull_overlap > 7
    assert not component_overlap


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--case", choices=("all", "normalization", "display", "hulls"), default="all")
    args = parser.parse_args()
    warnings.filterwarnings("ignore", message="Values in x were outside bounds")
    if args.case in ("all", "normalization"):
        normalization()
    if args.case in ("all", "display"):
        artifact_display(args.root.resolve())
    if args.case in ("all", "hulls"):
        disconnected_hulls(args.root.resolve())
    print("REPRO_ASSERTIONS_PASSED")
