"""Finite arithmetic examples for the unloading preregistration re-review.

No DEM, source-code import, trajectory integration, external data, or network.
The selector below is a literal model of prereg.md:627-636, not a kit reader.
Run: python -X utf8 -B probes/ulr_state.py
"""

from decimal import Decimal as D
import json


T = D("0.10")
H0 = D("111.052")


def num(x):
    return float(x) if isinstance(x, D) else x


def select(d_dt, d_v):
    if d_dt is None or d_v is None:
        return "NO_REGISTERED_ROW"
    if not d_dt.is_finite() or not d_v.is_finite():
        return "NO_REGISTERED_ROW"
    if d_dt <= T:
        return "UB" if d_v <= T else "UV_dt0"
    return "UT" if d_v <= T else "UV_dt0_half"


def rho(lift):
    return D(100) * D(lift) / H0


valid_cases = []
for d_dt, d_v, expected in [
    (D("0.04"), D("0.04"), "UB"),
    (D("0.04"), D("0.20"), "UV_dt0"),
    (D("0.20"), D("0.04"), "UT"),
    (D("0.20"), D("0.20"), "UV_dt0_half"),
]:
    selected = select(d_dt, d_v)
    assert selected == expected
    valid_cases.append({"delta_dt_pp": num(d_dt), "delta_v_pp": num(d_v), "selected": selected})

width_a = rho("0.20")
ub_i = (D("1.00"), D("1.00") + width_a)
ut_i = (D("1.04"), D("1.04") + width_a)
# A coarse first-crossing pair may be 3.4 -> 0.4 MPa, giving fraction 0.8.
# Both shifted intervals use this same physically admissible interpolation.
fraction = D("0.8")
interpolant_difference = abs((ub_i[0] + fraction * width_a) - (ut_i[0] + fraction * width_a))
max_bracket_difference = max(abs(ub_i[0] - ut_i[1]), abs(ub_i[1] - ut_i[0]))
assert interpolant_difference == D("0.04")
assert max_bracket_difference > T

f_plus, f_minus_magnitude, p_meas = D("1.6"), D("0.6"), D("1")
net_pressure = f_plus - f_minus_magnitude
is_contact_by_line_650 = net_pressure > 0
is_tension_by_line_651 = f_minus_magnitude >= D("0.5") * p_meas
assert is_contact_by_line_650 and is_tension_by_line_651

lift0, lift1, p0, p1 = D("0.20"), D("0.25"), D("1.2"), D("0.8")
cross_lift = lift0 + (p_meas - p0) * (lift1 - lift0) / (p1 - p0)
valid_measurement = rho(cross_lift)
last_lift_after_two = D("0.35")
old_timeout_lower = rho(last_lift_after_two)
assert valid_measurement < old_timeout_lower

physical_windows = []
for arm, dt, w_steps, n_min, n_max in [
    ("UB", "0.000001", 5000, 4, 12),
    ("UT_keep_physical_time_line_288", "0.0000005", 10000, 4, 12),
    ("UT_literal_line_660", "0.0000005", 5000, 4, 12),
    ("UV_half_dt_keep_physical_time", "0.0000005", 10000, 8, 24),
    ("UV_half_dt_literal_line_660", "0.0000005", 5000, 8, 24),
]:
    w_time = D(dt) * w_steps
    physical_windows.append({"arm": arm, "dt_s": float(dt), "window_steps": w_steps,
                             "window_s": num(w_time), "hold_s": [num(w_time * n_min), num(w_time * n_max)]})

# Three observations leave the fourth factorial corner unconstrained.
ub, ut, uv, unmeasured_slow_half = D("1.00"), D("1.04"), D("1.20"), D("1.80")
delta_dt, delta_v = abs(ut - ub), abs(uv - ub)
assert select(delta_dt, delta_v) == "UV_dt0"
assert abs(unmeasured_slow_half - uv) == D("0.60")

# The revised bracket rule keeps the first crossing; the old nonmonotone
# eligibility rule still invokes removed b when a second crossing occurs.
first_lift = D("1.025")
last_lift = D("1.10") + (D("1") - D("1.3")) * D("0.05") / (D("0.7") - D("1.3"))

result = {
    "kind": "finite_synthetic_arithmetic_not_DEM_not_production_implementation_test",
    "source": "submitted/prereg.md",
    "four_finite_rows": valid_cases,
    "equality_boundary": {"delta_dt_pp": 0.1, "delta_v_pp": 0.1, "selected": select(T, T)},
    "undefined_inputs": [
        {"cause": "UT endpoint invalid, delta_dt unavailable", "selected": select(None, D("0.04"))},
        {"cause": "UV endpoint invalid, delta_v unavailable", "selected": select(D("0.04"), None)},
        {"cause": "NaN is neither registered <= nor >", "selected": select(D("NaN"), D("0.04"))},
    ],
    "pressure_positive_cancellation": {
        "force_equivalent_pressure_MPa": {"compression": num(f_plus), "tension_magnitude": num(f_minus_magnitude)},
        "net_pressure_MPa": num(net_pressure),
        "CONTACT_predicate_line_650": is_contact_by_line_650,
        "TENSION_assignment_line_651": is_tension_by_line_651,
        "primary_eligibility": "not_fixed_by_label_alone",
    },
    "temporal_state_fixtures_needed": [
        {"contact_counts_per_window": [2, 0, 0], "pressures_MPa": [0.4, 0, 0],
         "question": "zero-contact first window and CONTACT to SEPARATED without a TENSION visit"},
        {"contact_counts_per_window": [0, 0, 1, 1], "pressures_MPa": [0, 0, 0.2, 0.2],
         "question": "recontact during four post-separation hold windows; reset or invalidate surface endpoint"},
    ],
    "time_window_interpretations": physical_windows,
    "final_slow_arm_dt_context": {
        "observed_rho_pp": {"UB_fast_dt0": num(ub), "UT_fast_dt0_half": num(ut), "UV_slow_dt0": num(uv)},
        "delta_dt_fast_pp": num(delta_dt), "delta_v_at_dt0_pp": num(delta_v),
        "selected": select(delta_dt, delta_v),
        "unmeasured_corner_consistent_with_all_observations": {"slow_dt0_half_rho_pp": num(unmeasured_slow_half), "slow_dt_difference_pp": num(abs(unmeasured_slow_half - uv))},
    },
    "point_threshold_vs_bracket": {
        "h0_um": num(H0), "A_width_pp": num(width_a),
        "UB_interval_pp": list(map(num, ub_i)), "UT_interval_pp": list(map(num, ut_i)),
        "interpolant_abs_difference_pp": num(interpolant_difference),
        "possible_abs_difference_range_from_brackets_pp": [0, num(max_bracket_difference)],
        "interpretation": "point-estimate selector remains deterministic; bracket-robust pass is not established",
    },
    "post_measurement_timeout": {
        "lift_um": [0.2, 0.25, 0.3, 0.35], "pressure_MPa": [1.2, 0.8, 0.6, 0.4],
        "assumptions": "all four endpoints normal and contacting; +2 check complete; separation not reached before timeout",
        "interpolated_lift_um": num(cross_lift), "valid_rho_percent": num(valid_measurement),
        "old_unconditional_timeout_claim_rho_greater_than_percent": num(old_timeout_lower),
        "contradiction": valid_measurement < old_timeout_lower,
    },
    "live_nonmonotone_b_reference": {
        "lift_um": [1.0, 1.05, 1.10, 1.15], "pressure_MPa": [1.2, 0.8, 1.3, 0.7],
        "first_crossing_rho_percent": num(rho(first_lift)), "last_crossing_rho_percent": num(rho(last_lift)),
        "span_pp": num(rho(last_lift - first_lift)), "b": "removed_in_revision_but_still_invoked_by_line_320",
    },
}

print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
