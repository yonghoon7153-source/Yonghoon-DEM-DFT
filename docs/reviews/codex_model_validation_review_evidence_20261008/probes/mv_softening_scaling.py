"""Deterministic dimensional/contact arithmetic only; never launches DEM.

Sources: branch B deck at repository 61ebd181b1ae5b47a76fe69d4400e4a3950dc8a3;
CFDEMproject/LIGGGHTS-PUBLIC normal_model_hooke_hysteresis.h at
3d5c00f20519e6bb6eb6756f51f1ad36564e649d; official check/timestep/gran docs.
"""
import json
import math


def rayleigh(r, rho, E, nu):
    G = E / (2 * (1 + nu))
    return math.pi * r * math.sqrt(rho / G) / (0.1631 * nu + 0.8766)


def yeff(E1, nu1, E2, nu2):
    return 1 / ((1 - nu1**2) / E1 + (1 - nu2**2) / E2)


def contact(r1, rho1, E1, nu1, r2, rho2, E2, nu2):
    m1 = 4 * math.pi * r1**3 * rho1 / 3
    m2 = 4 * math.pi * r2**3 * rho2 / 3
    meff = m1 * m2 / (m1 + m2)
    reff = r1 * r2 / (r1 + r2)
    Y = yeff(E1, nu1, E2, nu2)
    cv = 2.0
    kn = 16 / 15 * math.sqrt(reff) * Y * (15 * meff * cv**2 / (16 * math.sqrt(reff) * Y))**0.2
    gamma = math.sqrt(4 * meff * kn / (1 + (math.pi / math.log(0.3))**2))
    return {"Yeff_Pa": Y, "kn_N_per_m": kn, "contact_gamma_kg_per_s": gamma, "sqrt_meff_over_kn_s": math.sqrt(meff / kn)}


L, stress, density = 1000.0, 0.001, 1.0
time = L * math.sqrt(density / stress)
velocity = L / time
force = stress * L**2
rows = []
for factor in (1, 2, 4, 24 / 1.35, 18):
    E_se = 1.35e6 * factor
    rp = rayleigh(4.5e-3, 4800, 1.4e8, .25)
    rs = rayleigh(2e-3, 4800, 1.4e8, .25)
    re = rayleigh(.5e-3, 2000, E_se, .30)
    Y_mix = yeff(1.4e8, .25, E_se, .30)
    Y_mix0 = yeff(1.4e8, .25, 1.35e6, .30)
    rows.append({
        "factor_SE": factor, "E_SE_real_GPa": E_se * 1000 / 1e9,
        "E_AM_over_E_SE": 1.4e8 / E_se,
        "kn_SE_SE_ratio": factor**.8,
        "kn_AM_SE_ratio": (Y_mix / Y_mix0)**.8,
        "gamma_SE_SE_ratio": factor**.4,
        "Rayleigh_AM_P_us": rp * 1e6, "Rayleigh_AM_S_us": rs * 1e6,
        "Rayleigh_SE_us": re * 1e6,
        "dt_1us_over_min_Rayleigh": 1e-6 / min(rp, rs, re),
        "dt_preserve_SE_Rayleigh_margin_us": factor**-.5,
        "dt_preserve_SE_SE_Hooke_margin_us": factor**-.4,
    })

result = {
    "scope": "arithmetic and model-law probes only, no DEM execution or validation claim",
    "units_sim_over_real": {
        "length": L, "stress_and_E": stress, "density": density,
        "mass": density * L**3, "force": force, "stiffness_F_over_L": force / L,
        "time": time, "velocity": velocity, "acceleration": L / time**2,
        "viscous_gamma_F_over_v": force / velocity, "energy": force * L,
    },
    "gravity": {
        "required_g_deck_m_per_s2": 9.81 * L / time**2,
        "current_selfweight_amplification": L / stress,
        "readme_bulk_density_kg_m3_ESTIMATE": 3260,
        "window_93um_current_selfweight_MPa": 3260 * 9.81 * (93e-6 * L) / stress / 1e6,
        "height_132um_current_selfweight_MPa": 3260 * 9.81 * (132e-6 * L) / stress / 1e6,
        "window_93um_physical_selfweight_Pa": 3260 * 9.81 * 93e-6,
        "window_93um_current_over_165": 3260 * 9.81 * (93e-6 * L) / stress / (165e6),
        "settling_g_98_1_current_amplification_over_earth": 10 * L / stress,
        "fall_from_rest_0_295m_at_scaled_g_seconds": math.sqrt(2 * .295 / (9.81e-6)),
        "fall_at_scaled_g_in_200000_steps_of_1us_deck_m": .5 * 9.81e-6 * .2**2,
    },
    "mapped_velocities_real_m_per_s": {"press_0_01": .01 / velocity, "characteristic_2": 2 / velocity, "insertion_0_5": .5 / velocity},
    "target_force_N": {"165_MPa": 165e6 * stress * .05**2, "300_MPa": 300e6 * stress * .05**2},
    "E_and_timestep": rows,
    "baseline_contact": {
        "SE_SE": contact(.5e-3, 2000, 1.35e6, .30, .5e-3, 2000, 1.35e6, .30),
        "AM_S_SE": contact(2e-3, 4800, 1.4e8, .25, .5e-3, 2000, 1.35e6, .30),
    },
    "limitations": [
        "Rayleigh estimates use original constant radius/density deck, not parsed restart atom minima.",
        "Rayleigh/Hertz checks and sqrt(m/k) scaling do not certify hysteretic, adhesive, frictional, wall or servo stability.",
        "Bulk density 3260 is the source README approximation, not a particle-mass sum.",
        "E ratios do not predict force-share ratios after equilibrium, slip, contact changes or history evolution.",
    ],
}
print(json.dumps(result, indent=2))
