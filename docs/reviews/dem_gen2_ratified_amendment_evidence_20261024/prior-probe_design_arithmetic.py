#!/usr/bin/env python3
"""Small exact/algebraic design probes. No DEM, repository writes, or network.

These are counterexamples to proposed guarantees, not observations of a real bed.
Run: python -I -B probe_design_arithmetic.py > arithmetic-results.json
"""
import json
import math


def porosity(mass_g, density_g_cm3, diameter_mm, thickness_mm):
    volume_cm3 = math.pi * (diameter_mm / 20) ** 2 * thickness_mm / 10
    return 1 - mass_g / (density_g_cm3 * volume_cm3)


def density_interval(thickness_mm):
    # Diameter held exactly at 10 mm only for this counterexample.
    # Real inference also needs measured diameter uncertainty and covariance.
    area_cm2 = math.pi * (10 / 20) ** 2
    mass_lo, mass_hi = 0.100 - 0.0001, 0.100 + 0.0001
    t_lo, t_hi = thickness_mm - 0.01, thickness_mm + 0.01
    rho_lo = mass_lo / (area_cm2 * t_hi / 10)
    rho_hi = mass_hi / (area_cm2 * t_lo / 10)
    return {
        "thickness_mm": thickness_mm,
        "assumed_mass_interval_g": [mass_lo, mass_hi],
        "assumed_thickness_interval_mm": [t_lo, t_hi],
        "apparent_density_interval_g_cm3": [rho_lo, rho_hi],
        "rejects_density_1_64_under_stated_bounds": rho_lo > 1.64,
    }


eps = 0.115
springback = [
    {"thickness_recovery_percent": r * 100,
     "porosity_percent": 100 * (1 - (1 - eps) / (1 + r)),
     "porosity_change_pp": 100 * ((1 - (1 - eps) / (1 + r)) - eps)}
    for r in (0.016, 0.07)
]
assert math.isclose(springback[0]["porosity_change_pp"], 1.39370078740157)
assert math.isclose(springback[1]["porosity_change_pp"], 5.78971962616822)

boundary_mm = 0.100 / (1.64 * math.pi * (10 / 20) ** 2) * 10
intervals = [density_interval(t) for t in (0.760, 0.770)]
assert intervals[0]["rejects_density_1_64_under_stated_bounds"]
assert not intervals[1]["rejects_density_1_64_under_stated_bounds"]
assert 0.770 < boundary_mm

# Linear, delay-free, unsaturated servo: e_next = (1 - a) e,
# a = K * kp * vmax * chunk_time / target_force. This model is not DEM.
servo = []
for stiffness in (4700.0, 47000.0, 470000.0, 1000000.0, 1100000.0):
    gain = stiffness * 30 * 0.01 * 0.005 / 750
    e = 0.001
    trace = [e]
    for _ in range(10):
        assert abs(30 * e) < 1, "probe must remain in the unsaturated branch"
        e = (1 - gain) * e
        trace.append(e)
    servo.append({"K_N_per_m": stiffness, "gain": gain,
                  "linear_stable": 0 < gain < 2,
                  "initial_relative_error": trace[0],
                  "relative_error_after_10_chunks": trace[-1]})
assert abs(servo[-1]["relative_error_after_10_chunks"]) > 0.001
assert math.isclose(abs(servo[-2]["relative_error_after_10_chunks"]), 0.001)

# Exact binomial coverage for an otherwise correct Monte Carlo volume estimate:
# indicator p=1/2, n=100, true standard error 0.05, acceptance [0.45, 0.55].
# A 1-sigma rule has nonzero false-failure probability even with correct code.
coverage = sum(math.comb(100, k) for k in range(45, 56)) / 2 ** 100
mc = {"n": 100, "true_probability": 0.5, "known_standard_error": 0.05,
      "acceptance_counts_inclusive": [45, 55],
      "exact_single_probe_coverage": coverage,
      "exact_single_probe_false_failure_probability": 1 - coverage,
      "exact_three_independent_probes_any_false_failure_probability": 1 - coverage ** 3}
assert 0.27 < mc["exact_single_probe_false_failure_probability"] < 0.28

# Two radius-1 spheres distance 1, fully inside their 3 x 2 x 2 bounding box.
# The exact intersection is pi*(4r+d)*(2r-d)^2/12 = 5pi/12.
v_box, v_spheres, v_intersection = 12, 8 * math.pi / 3, 5 * math.pi / 12
v_union = v_spheres - v_intersection
operators = {"sphere_porosity_percent": 100 * (1 - v_spheres / v_box),
             "exact_union_porosity_percent": 100 * (1 - v_union / v_box),
             "definition_difference_pp": 100 * v_intersection / v_box}
assert math.isclose(operators["definition_difference_pp"], 10.90830782496456)

am_one_pp = 100 * (4 * math.pi / 3) * 4.5 ** 3 / (2500 * 111.052)
loss = {"AM_radius_um": 4.5, "box_um3": 2500 * 111.052,
        "one_AM_loss_porosity_pp": am_one_pp,
        "fifty_AM_loss_porosity_pp": 50 * am_one_pp}
assert math.isclose(loss["fifty_AM_loss_porosity_pp"], 6.874320271785467)

energies = {"P_deck_Pa": 300000, "V_deck_m3": 0.05 * 0.05 * 0.1,
            "translation_0_5J_K_over_PV": 0.5 / (300000 * 0.05 * 0.05 * 0.1),
            "rotation_only_0_009J_K_over_PV": 0.009 / (300000 * 0.05 * 0.05 * 0.1),
            "two_opposed_residual_forces_N": [10, -10],
            "sum_residual_N": 0,
            "sum_absolute_residual_over_target": 20 / 750}

ladder = [1.35, 2.0, 3.0, 4.5, 6.75]
ratios = [b / a for a, b in zip(ladder, ladder[1:])]
assert not math.isclose(ratios[0], 1.5)
assert all(math.isclose(r, 1.5) for r in ratios[1:])

result = {"scope": "algebraic design probes only; no physical-run result",
          "springback": springback,
          "zero_porosity_thickness_mm_density_1_64": boundary_mm,
          "density_measurement_interval_counterexamples": intervals,
          "discrete_linear_servo": servo,
          "MC_one_sigma_acceptance": mc,
          "sphere_vs_union_operators": operators,
          "conservation": loss,
          "energy_and_local_cancellation": energies,
          "E_ladder_GPa": ladder, "successive_ratios": ratios,
          "checks": "all assertions passed"}
print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
