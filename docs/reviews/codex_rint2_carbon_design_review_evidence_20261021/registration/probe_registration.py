"""Independent, tiny passive-resistor and decision-logic counterexamples.

No repository code is modified or imported.  A+B/(r+C) is the conductance of
a fixed parallel conductance A and a series branch (r+C)/B; all coefficients
used here are positive.  Therefore each response is a passive-resistor
network, not an arbitrary nonmonotone fitted curve.  Units are mS/cm after
one fixed geometrical conversion; r is a dimensionless scaled R_j.
"""
from __future__ import annotations
import json
import math
import ast
from pathlib import Path
from types import SimpleNamespace


def response(r, a, b, c):
    return a + b / (r + c)


def inverse(y, a, b, c):
    return b / (y - a) - c


def verdict(lo, hi, target=4.68):
    w = math.log(hi / lo)
    if not lo <= target <= hi:
        label = "FAIL"
    elif w <= 0.454:
        label = "PASS_INFORMATIVE"
    elif w <= 0.908:
        label = "CONSISTENT_WEAK"
    else:
        label = "UNINFORMATIVE"
    return {"lo": lo, "hi": hi, "W": w, "label": label}


def calibration_counterexample():
    target = 1.63
    abc = (1.597, 0.0363, 0.1)
    scale = 10 ** 4.75
    r1, r2 = 10 ** (-0.25), 10 ** 0.25
    s1, s2 = (response(r, *abc) for r in (r1, r2))
    e = math.log(s1 / s2) / math.log(r2 / r1)
    emin = 0.02 / math.log(math.sqrt(10))
    r0 = math.exp(math.log(r1) + math.log(s1 / target) / e)
    r0_rounded = float(f"{r0 * scale:.3g}") / scale
    rlo = r0 * math.exp(-math.log(1.02) / e)
    rhi = r0 * math.exp(-math.log(0.98) / e)
    true_lo = inverse(target * 1.02, *abc)
    true_hi = inverse(target * 0.98, *abc)
    d = lambda r: response(r, 3.0, 1.0, 0.1)
    draft = verdict(d(rhi), d(rlo))
    exact = verdict(d(true_hi), d(true_lo))
    assert e > emin
    assert abs(response(r0_rounded, *abc) / target - 1) < 0.02
    # Neither extremum is within 2% under either common denominator reading.
    floor, ceiling = abc[0], response(0, *abc)
    assert min(abs(target / x - 1) for x in (floor, ceiling)) > 0.02
    assert min(abs(x / target - 1) for x in (floor, ceiling)) > 0.02
    assert draft["label"] == "PASS_INFORMATIVE"
    assert exact["label"] == "CONSISTENT_WEAK"
    # Initial 10^4 / 10^6 / 10^8 ladder plus two log bisections reaches this
    # bracket. With the two extrema and one confirmation it uses eight points,
    # within the 12-point limit (even when extrema count toward the limit).
    ladder_R = [1e4, 1e6, 1e8, 1e5, math.sqrt(1e4 * 1e5)]
    ladder_S = [response(x / scale, *abc) for x in ladder_R]
    assert ladder_S[0] > target > ladder_S[1]
    assert ladder_S[-1] > target > ladder_S[-2]
    assert len(ladder_R) + 2 + 1 <= 12
    assert abs(math.log(r2/r1) - math.log(math.sqrt(10))) < 1e-14
    return {
        "SBE_A_B_C": abc, "Rj_scale_ohm": scale,
        "last_bracket_Rj_ohm": [r1 * scale, r2 * scale],
        "last_bracket_SBE_mScm": [s1, s2], "e": e, "emin": emin,
        "r0": r0, "rounded_Rj0_ohm": r0_rounded * scale,
        "confirmed_SBE_mScm": response(r0_rounded, *abc),
        "floor_ceiling": [floor, ceiling],
        "extrema_distance_pct_denominator_target": [100*abs(x/target-1) for x in (floor, ceiling)],
        "extrema_distance_pct_denominator_extremum": [100*abs(target/x-1) for x in (floor, ceiling)],
        "ladder_Rj_ohm": ladder_R, "ladder_SBE_mScm": ladder_S,
        "points_including_extrema_and_confirmation": len(ladder_R) + 2 + 1,
        "draft_r_bounds": [rlo, rhi],
        "SBE_at_draft_bounds": [response(rlo, *abc), response(rhi, *abc)],
        "true_r_bounds": [true_lo, true_hi],
        "true_r_bound_ratio": true_hi / true_lo,
        "draft_DBE_verdict": draft, "exact_DBE_verdict": exact,
        "ratio_bound_at_emin": math.exp(math.log(1.02 / 0.98) / emin),
    }


def origin_counterexample():
    rlo, r0, rhi = 0.5, 1.0, 2.0
    arm0 = lambda r: response(r, 3.02, 1.0, 0.1)
    others = lambda r: response(r, 1.02, 3.2, 0.1)
    mean = lambda r: (arm0(r) + 7 * others(r)) / 8
    # Three tested origins and all eight origins agree exactly at r0.
    centre_range = math.log(max(arm0(r0), others(r0)) / min(arm0(r0), others(r0)))
    draft = verdict(arm0(rhi), arm0(rlo))
    exact = verdict(mean(rhi), mean(rlo))
    assert centre_range < 1e-15
    assert draft["label"] == "PASS_INFORMATIVE"
    assert exact["label"] == "CONSISTENT_WEAK"
    return {"r_bounds": [rlo, rhi], "centre_all_origins": [arm0(r0), others(r0)],
            "centre_origin_log_range": centre_range,
            "registered_origin_limit": 0.1 * draft["W"],
            "arm0_endpoints": [arm0(rhi), arm0(rlo)],
            "other_origin_endpoints": [others(rhi), others(rlo)],
            "draft_verdict": draft, "true_eight_origin_verdict": exact}


def contact_bias_counterexample():
    Rs, Rd, Rc, target = 7.016, 2.178, 1.0, 1.63
    fS = lambda r: response(r, 0.0, 9.78, 5.0)
    fD = lambda r: response(r, 1.0, 1.0, 0.01)
    invS = lambda y: inverse(y, 0.0, 9.78, 5.0)
    rlo, rhi = invS(target * 1.02), invS(target * 0.98)
    s_local = math.log(fD(rlo) / fD(rhi)) / math.log(1.02 / 0.98)
    S_true = target * Rs / (Rs - Rc)
    r_true = invS(S_true)
    fS_factor, fD_factor = Rs / (Rs - Rc), Rd / (Rd - Rc)
    threshold = math.log(fD_factor) / math.log(fS_factor)
    exact = fD_factor * fD(1.0) / fD(r_true)
    reported_formula = fD_factor * fS_factor ** (-s_local)
    s_finite = math.log(fD(r_true) / fD(1.0)) / math.log(S_true / target)
    # A fixed multiplier makes the exact measured DBE value 4.68; it cancels
    # from all ratios and elasticities, so this example uses the cited target.
    scaleD = 4.68 * fD_factor / fD(r_true)
    assert abs(fS(1) - target) < 1e-14
    assert s_local < threshold
    assert exact < 1 < reported_formula
    return {"R_measured_SBE_DBE_Rc_ohm": [Rs, Rd, Rc],
            "local_pm2pct_secant_s": s_local, "finite_range_s": s_finite,
            "threshold": threshold, "SBE_true_mScm": S_true,
            "r_at_true_SBE": r_true, "DBE_fixed_scale": scaleD,
            "DBE_measured": scaleD * fD(r_true) / fD_factor,
            "DBE_predicted": scaleD * fD(1),
            "registered_formula_prediction_over_measurement": reported_formula,
            "exact_prediction_over_measurement": exact}


def logic_counterexamples():
    centre = [4.40, 4.45, 4.50, 4.55]
    propagated = [4.30, 4.80, *centre]
    main = verdict(min(propagated), max(propagated))
    # A strict no-op UNREG sensitivity with zero unregistered faces has the
    # very same responses. The registered sensitivity run count has only the
    # four centre runs, so its grade is different if graded as that envelope.
    noop = verdict(min(centre), max(centre))
    assert main["label"] != noop["label"]
    mandatory_flags = ["DIA_UNCHECKED"]
    allowed_by_7_1 = not any(x.endswith(("_SENSITIVE", "_UNCHECKED")) for x in mandatory_flags)
    assert not allowed_by_7_1
    discrete_intervals = [(3.8, 4.0), (5.2, 5.4)]
    hull_grade = verdict(min(lo for lo, hi in discrete_intervals), max(hi for lo, hi in discrete_intervals))
    union_contains_target = any(lo <= 4.68 <= hi for lo, hi in discrete_intervals)
    assert hull_grade["label"] == "PASS_INFORMATIVE" and not union_contains_target
    return {"same_model_primary_with_calibration_bounds": main,
            "same_model_noop_sensitivity_centres_only": noop,
            "mandatory_flags": mandatory_flags,
            "PASS_sentence_allowed_by_literal_7_1": allowed_by_7_1,
            "discrete_P_intervals": discrete_intervals,
            "scenario_hull_verdict": hull_grade,
            "any_admissible_P_interval_contains_target": union_contains_target,
            "loading_rate_old": 0.2717,
            "loading_rate_new_conditional_arithmetic": 0.2717 * 2e-4 / 1.311e-4}


def loading_rate_arithmetic():
    """Pure arithmetic of pinned mpm3d_compaction.py:1904-1929,3073-3078.

    These are code time units (rho=1), not asserted to be SI seconds.
    Full MPM integration and physical calibration are deliberately not run.
    """
    def lame(E, nu):
        return E/(2*(1+nu)), E*nu/((1+nu)*(1-2*nu))
    def pmod(E, nu):
        mu, la = lame(E, nu)
        return la+2*mu
    se, old_vgcf, new_vgcf = pmod(1.53, .49), pmod(10, .30), pmod(100, .30)
    old_cfl = .4/263/math.sqrt(max(se, old_vgcf))
    new_cfl = .4/263/math.sqrt(max(se, new_vgcf))
    old_dt, new_dt = min(2e-4, old_cfl), min(2e-4, new_cfl)
    mu_se, _ = lame(1.53, .49)
    c_p, c_s = math.sqrt(se), math.sqrt(mu_se)
    m_old = .2717
    m_new = m_old * old_dt/new_dt
    inferred_H = m_old*c_p*40*old_dt/.008
    assert old_dt == 2e-4 and new_dt < old_dt
    # Execute only the actual pinned CFL/platen scalar blocks, not main(),
    # Taichi, file access, seeding or MPM. Match via source line locations and
    # assert against independent arithmetic so a moved/changed block fails.
    src_path = Path(__file__).parents[1] / "source/scripts/mpm3d_compaction.py"
    module = ast.parse(src_path.read_text(encoding="utf-8"))
    main_node = next(n for n in module.body if isinstance(n, ast.FunctionDef) and n.name == "main")
    scalar_nodes = [n for n in main_node.body if 1897 <= n.lineno <= 1929]
    scalar_nodes += [n for n in main_node.body if 3073 <= n.lineno <= 3078]
    assert len(scalar_nodes) > 10
    scalar_code = compile(ast.Module(body=scalar_nodes, type_ignores=[]), str(src_path), "exec")
    actual = []
    for E in [10.0, 100.0]:
        args = SimpleNamespace(n_grid=263, periodic=False, dt=2e-4, e_se=1.53,
                               nu_se=.49, e_am=140., sigma_y=.3, coh=.02,
                               preset="", material="mix", am_scaffold="fixture.csv",
                               add_recipe="VGCF:1,PTFE:1", platen_mach=0., sub=40)
        ns = {"args": args, "ADD_E_NU": {"VGCF":(E,.3),"PTFE":(1.8,.3)},
              "WALL0":inferred_H+.05, "FLOOR":.05}
        exec(scalar_code, ns)
        actual.append({k: ns[k] for k in ["_M","_dt_cfl_cap","dt","_c_p","_c_s","vmax","_v_platen"]})
    assert abs(actual[0]["dt"]-old_dt) < 1e-18
    assert abs(actual[1]["dt"]-new_dt) < 1e-18
    assert abs(actual[1]["_v_platen"]/actual[1]["_c_p"]-m_new) < 1e-14
    return {"SE_M_GPa": se, "VGCF10_M_GPa": old_vgcf, "VGCF100_M_GPa": new_vgcf,
            "actual_pinned_scalar_blocks": actual,
            "old_cfl_cap": old_cfl, "new_cfl_cap": new_cfl,
            "old_dt": old_dt, "new_dt": new_dt, "new_over_old_time": new_dt/old_dt,
            "speed_factor": old_dt/new_dt, "SE_cP_code_units": c_p, "SE_cS_code_units": c_s,
            "P_Mach_old_new": [m_old, m_new], "S_Mach_old_new": [m_old*c_p/c_s,m_new*c_p/c_s],
            "inferred_H_code_units_from_rounded_old_Mach": inferred_H,
            "150_frame_budget_time_old_new": [150*40*old_dt,150*40*new_dt],
            "40_frame_hold_time_old_new": [40*40*old_dt,40*40*new_dt],
            "ram_pressure_scale_factor_new_over_old": (old_dt/new_dt)**2}


def main():
    data = {"calibration": calibration_counterexample(),
            "origin": origin_counterexample(),
            "contact_bias": contact_bias_counterexample(),
            "logic": logic_counterexamples(),
            "loading_rate": loading_rate_arithmetic()}
    out = Path(__file__).with_name("registration_probe_results.json")
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
