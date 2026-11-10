"""Document-only independent branch audit; no DEM/MPM or project imports.

Derived first from memo_v3_1.md, before reading pa3/fork_enum.py or s4_enum.py.
All numbers below are synthetic and dimensionless except labeled GPa/% values.
This audits proposed rules; it generates no scientific result or execution GO.
"""
from __future__ import annotations

import itertools as it
import json
import math
from pathlib import Path

D, E, O, I, X = "different", "same", "opposite", "intermediate", "discard"
GRADES = (D, E, O, I)


def ratio_predicates(rs):
    # Lines 319-326. This function deliberately exposes all matching predicates.
    gm = math.exp(sum(math.log(r) for r in rs) / len(rs))
    return {
        D: gm >= 1.3 and min(rs) >= 1.15,
        E: 1 / 1.15 <= gm <= 1.15 and min(rs) >= 1 / 1.3 and max(rs) <= 1.3,
        O: gm <= 1 / 1.3 and max(rs) <= 1 / 1.15,
    }


def ratio_grade(rs):
    matched = [g for g, truth in ratio_predicates(rs).items() if truth]
    assert len(matched) <= 1
    return matched[0] if matched else I


def raw_point_grade(pairs, noise=0.008):
    # Lines 331-337: None = upper-bound nonarrival. Positive scalar = read stress.
    if any(num is not None and den is None for num, den in pairs):
        return O
    if any((num is None and den is None) or
           (num is not None and den is not None and num < noise and den < noise)
           for num, den in pairs):
        return X
    rs = [math.inf if num is None else max(num, noise) / max(den, noise)
          for num, den in pairs]
    return ratio_grade(rs)


def test_grade(points):
    # Line 341, in its stated priority order.
    kept = [p for p in points if p != X]
    if O in kept:
        return O
    if kept.count(D) >= 2:
        return D
    if len(kept) >= 2 and all(p == E for p in kept):
        return E
    return I


def resolution_grade(g12, g16, g24):
    # Line 348; g24 is unused when g12 == g16.
    if g12 == g16:
        return g16, 16
    if g16 == g24:
        return g24, 24
    return I, 24


def a_predicates(deltas):
    mean = sum(deltas) / 3
    mean_abs = sum(abs(d) for d in deltas) / 3
    return {
        "insufficient": mean >= .02 and min(deltas) >= .01,
        "sufficient": mean_abs <= .01 and max(abs(d) for d in deltas) <= .02,
        "opposite": mean <= -.02 and max(deltas) <= -.01,
    }


def a_grade(deltas):
    matched = [g for g, truth in a_predicates(deltas).items() if truth]
    assert len(matched) <= 1
    return matched[0] if matched else I


def combine(g_a, g_b):
    # Line 358.
    if O in (g_a, g_b):
        return O
    if D in (g_a, g_b):
        return D
    return E if g_a == g_b == E else I


def route3(g_a, g_b, band_in, a, technical=False, friction=False):
    # Line 360, then 364-375. 라 has priority; A can only modify 가/마.
    g = combine(g_a, g_b)
    if technical or friction or a == "opposite" or not band_in or g == O:
        return "라"
    basic = {D: "나", E: "가", I: "마"}[g]
    if basic in ("가", "마") and a == "insufficient":
        return "나"
    if basic == "가" and a == I:
        return "마"
    return basic


def route4(actual, softened):
    # Lines 398-401, assuming arm statuses already exist and are exclusive.
    if "hold" in (actual, softened):
        return "hold"
    if (actual, softened) in (("below", "cross"), ("below", "above"),
                             ("cross", "above")):
        return "hold"
    if actual == "cross":
        return "4-i"
    if actual == "above" and softened == "cross":
        return "4-ii"
    if actual != "cross" and softened != "cross":
        return "4-iii"
    raise AssertionError((actual, softened))


def walk(grid, eps, start):
    """A small synthetic transcription of lines 392-394, with no failure events.

    The grid is the allowed final-box domain (extension applicability is external).
    eps is a mean percent porosity. Return every tied endpoint candidate, so the
    transcript does not silently add a tie-breaking policy not stated in the memo.
    """
    target = 11.5
    index = grid.index(start)
    seen = [index]
    direction = -1 if eps[index] > target else 1
    if eps[index] == target:
        return {"seen": [grid[index]], "cross": True, "sigma_star": [grid[index]]}
    while 0 <= index + direction < len(grid):
        previous = index
        index += direction
        seen.append(index)
        if (eps[index] - eps[previous]) * direction < -.5:
            return {"seen": [grid[i] for i in seen], "hold": "reverse > 0.5 pp"}
        if eps[index] == target:
            return {"seen": [grid[i] for i in seen], "cross": True,
                    "sigma_star": [grid[index]]}
        if (eps[previous] - target) * (eps[index] - target) < 0:
            fraction = (target - eps[previous]) / (eps[index] - eps[previous])
            sigma = math.exp(math.log(grid[previous]) + fraction *
                             (math.log(grid[index]) - math.log(grid[previous])))
            return {"seen": [grid[i] for i in seen], "cross": True,
                    "sigma_star": [sigma]}
    inside = [i for i in seen if 10 <= eps[i] <= 13]
    if not inside:
        return {"seen": [grid[i] for i in seen], "cross": False,
                "side": "above" if all(eps[i] > 13 for i in seen) else "below"}
    closest = min(abs(eps[i] - target) for i in inside)
    return {"seen": [grid[i] for i in seen], "cross": True,
            "sigma_star": [grid[i] for i in inside if abs(eps[i] - target) == closest]}


def main():
    ratios = (1 / 1.3 - .001, 1 / 1.3, 1 / 1.15 - .001, 1 / 1.15,
              1., 1.15, 1.1501, 1.3, 1.3001, math.inf)
    ratio_n = 0
    for rs in it.product(ratios, repeat=3):
        ratio_grade(rs)
        ratio_n += 1
    raw_states = (None, .004, .008, .01, .02)
    raw_n = 0
    for pairs in it.product(tuple(it.product(raw_states, repeat=2)), repeat=3):
        assert raw_point_grade(pairs) in GRADES + (X,)
        raw_n += 1
    for points in it.product(GRADES + (X,), repeat=3):
        grade = test_grade(points)
        if grade == D:
            # A 3-point test has exactly one near-jamming point (index zero).
            assert sum(p == D for p in points) >= 2
            assert D in points[1:]
    for grades in it.product(GRADES, repeat=3):
        assert resolution_grade(*grades)[0] in GRADES
    delta_values = (-.03, -.02, -.01, -.005, 0., .005, .01, .02, .03)
    for deltas in it.product(delta_values, repeat=3):
        a_grade(deltas)
    route_counts = {g: 0 for g in ("가", "나", "라", "마")}
    for ga, gb, band, a, tech, fric in it.product(
        GRADES, GRADES, (False, True),
        ("insufficient", "sufficient", "opposite", I),
        (False, True), (False, True)
    ):
        route_counts[route3(ga, gb, band, a, tech, fric)] += 1
    table4 = [{"actual": a, "softened": b, "route": route4(a, b)}
              for a, b in it.product(("below", "cross", "above", "hold"), repeat=2)]

    # A resolution disagreement can suppress even a final-resolution opposite.
    res24, chosen_res = resolution_grade(E, D, O)
    resolution_witness = {
        "grades_12_16_24": [E, D, O], "resolved_grade": res24,
        "decision_resolution": chosen_res,
        "other_test_grade": E, "F_band": "in", "A_grade": "sufficient",
        "final_route": route3(res24, E, True, "sufficient"),
        "status": "Defined by the explicit resolution rule; limitation, not a missing branch.",
    }

    # BR-01: all eight exploration points excluded. No final-box failure exists.
    all_failed = {
        "grid_GPa": [.03, .05, .08, .12, .18, .27, .40, .60],
        "first_attempt": ["failed"] * 8,
        "retry": ["failed"] * 8,
        "surviving_start_candidates": [],
        "final_box_attempts": 0,
        "missing_operation": "argmin over an empty candidate set",
        "assigned_arm_status_by_memo": None,
    }
    assert not all_failed["surviving_start_candidates"]

    # BR-02: mean porosity exactly hits the target, but qualification seed is free.
    qualification_by_seed = [
        {"fixed_seed": 1, "eight_cell_percent": 11.0, "twelve_cell_percent": 11.9,
         "difference_pp": .9, "qualified": True},
        {"fixed_seed": 2, "eight_cell_percent": 11.0, "twelve_cell_percent": 12.1,
         "difference_pp": 1.1, "qualified": False},
        {"fixed_seed": 3, "eight_cell_percent": 11.0, "twelve_cell_percent": 11.9,
         "difference_pp": .9, "qualified": True},
    ]
    seed_choice = {
        "walk_sigma_GPa": .18,
        "final_box_seed_porosity_percent": [11.4, 11.5, 11.6],
        "mean_percent": 11.5,
        "qualified_softened_arm": "cross",
        "qualification_observations": qualification_by_seed,
        "outcomes_by_chosen_seed": [
            route4("cross" if q["qualified"] else "hold", "cross")
            for q in qualification_by_seed],
    }
    assert set(seed_choice["outcomes_by_chosen_seed"]) == {"4-i", "hold"}

    # BR-03: the nested F re-opening clause omits the main table's not-on-hold guard.
    f_walk = walk([.18, .27], [11., 12.], .18)
    fallback = {
        "stage3_route": "마",
        "S_actual": "above", "S_softened": "cross",
        "initial_stage4_route": route4("above", "cross"),
        "F_actual_walk": f_walk,
        "F_actual_resolution_difference_pp": 1.2,
        "resolution_threshold_pp": 1.0,
        "F_actual_qualification": "hold",
        "F_softened_status": "cross",
        "line_400_literal_choice": "F-actual production",
        "line_409_prohibition": "Do not use values from the held arm",
        "main_table_result_if_applied": route4("hold", "cross"),
    }
    assert f_walk["cross"] and fallback["main_table_result_if_applied"] == "hold"

    # A small permitted nonmonotonic curve illustrates a wording limitation only.
    plateau = walk([.03, .05, .08], [12., 12., 12.], .08)
    observations = {
        "scope": "Independent document algebra and synthetic arithmetic only; no scientific runs.",
        "source": "docs/reviews/dem_redesign_direction_20261109/memo_v3_1.md",
        "derived_before_reading_author_self_tests": True,
        "checks": {
            "ratio_grade_samples": ratio_n,
            "raw_point_samples": raw_n,
            "test_point_grade_combinations": 5 ** 3,
            "resolution_grade_combinations": 4 ** 3,
            "A_grade_samples": len(delta_values) ** 3,
            "upper_stage3_combinations": sum(route_counts.values()),
            "upper_stage3_route_counts": route_counts,
            "upper_stage4_combinations": len(table4),
            "upper_stage4_table": table4,
            "claim": "The abstract upper tables are total and single-valued for supplied valid statuses.",
        },
        "counterexamples": {
            "BR-01_exploration_all_failed": all_failed,
            "BR-02_qualification_seed_choice": seed_choice,
            "BR-03_reopened_F_held_production": fallback,
        },
        "non_findings_and_limitations": {
            "resolution_opposite_masking": resolution_witness,
            "endpoint_plateau": {
                **plateau,
                "status": "Potential tie wording; line 394 first-encountered language may settle it, so not separately filed.",
            },
        },
    }
    outfile = Path(__file__).with_name("independent_results.json")
    outfile.write_text(json.dumps(observations, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(outfile), "checks": observations["checks"],
                      "counterexamples": list(observations["counterexamples"])},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
