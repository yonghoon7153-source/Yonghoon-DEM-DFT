#!/usr/bin/env python3
"""Reproduce review arithmetic only; no DEM run and no measured outputs.

All lengths in contact-law examples are expressed in micrometres. The gravity
example uses the original deck's nominal particle counts, not S0 observations.
Run from the review root:
    python probes/physics_arithmetic.py --output evidence/physics_arithmetic.json
"""

import argparse
import json
import math
from pathlib import Path


def contact_thresholds(name, ri, rj, a, c, phi, wall=False):
    reff = ri if wall else ri * rj / (ri + rj)
    delta_lim = a / (a - 1.0) * phi * 2.0 * reff
    delta_zero = phi * 2.0 * reff
    delta_adhesion = (a - 1.0) * delta_lim / (a + c)
    return {
        "pair": name,
        "r_i_um": ri,
        "r_j_um": None if wall else rj,
        "is_wall": wall,
        "r_eff_um": reff,
        "k2Max_over_kn": a,
        "kc_over_kn": c,
        "phiF": phi,
        "delta_lim_um": delta_lim,
        "delta_zero_um": delta_zero,
        "delta_adhesion_switch_um": delta_adhesion,
    }


def calculate():
    thresholds = [
        contact_thresholds("SE-SE", 0.5, 0.5, 5.0, 1e6, 0.005),
        contact_thresholds("AM_S-SE", 2.0, 0.5, 3.0, 2e5, 0.01),
        contact_thresholds("AM_P-SE", 4.5, 0.5, 3.0, 2e5, 0.01),
        contact_thresholds("wall-SE (wall type 1)", 0.5, 0.0, 3.0, 2e5, 0.01, True),
        contact_thresholds("AM_S-AM_S", 2.0, 2.0, 1.5, 1e5, 0.05),
        contact_thresholds("AM_P-AM_S", 4.5, 2.0, 1.5, 1e5, 0.05),
        contact_thresholds("AM_P-AM_P", 4.5, 4.5, 1.5, 1e5, 0.05),
    ]
    # Every scale below is deck / physical-reference, under the registered
    # length/pressure convention. It is not proof of complete model similarity.
    s_length, s_density, s_pressure = 1000.0, 1.0, 0.001
    s_mass = s_density * s_length**3
    s_force = s_pressure * s_length**2
    s_acceleration = s_force / s_mass
    g, area_deck = 9.81, 0.0025
    components = [
        {"type": "AM_P", "nominal_count": 282, "radius_deck_m": 4.5e-3, "density_kg_m3": 4800.0},
        {"type": "AM_S", "nominal_count": 1375, "radius_deck_m": 2e-3, "density_kg_m3": 4800.0},
        {"type": "SE", "nominal_count": 158765, "radius_deck_m": 0.5e-3, "density_kg_m3": 2000.0},
    ]
    mass_deck = sum(
        x["nominal_count"] * x["density_kg_m3"] * (4.0 * math.pi / 3.0) * x["radius_deck_m"]**3
        for x in components
    )
    weight_pressure_deck_pa = mass_deck * g / area_deck
    weight_pressure_reported_pa = weight_pressure_deck_pa / s_pressure
    physical_mass = mass_deck / s_mass
    physical_area = area_deck / s_length**2
    physical_weight_pressure_pa = physical_mass * g / physical_area

    # Synthetic non-saturated S0: deltaMax = 0.6 delta_lim, current overlap
    # = 0.15 delta_lim. k2/kn comes directly from HYS line 180.
    a, stored_max, current_overlap = 1.5, 0.6, 0.15
    k2_over_kn = 1.0 + (a - 1.0) * stored_max
    zero_overlap = (1.0 - 1.0 / k2_over_kn) * stored_max
    remaining_recovery = current_overlap - zero_overlap
    remaining_percent = 100.0 * remaining_recovery / current_overlap

    # Synthetic pair of contacts, normalized by delta_lim and kn*delta_lim.
    # Both retain saturated history; both current overlaps are positive.
    # Normal velocities are zero, so the damping term is zero in this probe.
    cancellation_contacts = []
    for overlap in [0.75, 7.0 / 12.0]:
        linear_force = 3.0 * (overlap - 1.0) + 1.0
        adhesion_force = -2e5 * overlap
        cancellation_contacts.append({
            "delta_over_delta_lim": overlap,
            "stored_deltaMax_over_delta_lim": 1.0,
            "linear_force_over_kn_delta_lim": linear_force,
            "adhesion_bound_over_kn_delta_lim": adhesion_force,
            "force_over_kn_delta_lim": max(linear_force, adhesion_force),
            "selected_branch": "saturated un/reloading",
            "geometric_contact_present": overlap > 0.0,
        })
    cancellation_total = sum(x["force_over_kn_delta_lim"] for x in cancellation_contacts)

    assert math.isclose(s_acceleration, 1e-6, rel_tol=1e-12)
    assert math.isclose(weight_pressure_reported_pa / physical_weight_pressure_pa, 1e6, rel_tol=1e-12)
    assert math.isclose(remaining_percent, 100.0 / 13.0, rel_tol=1e-12)
    assert math.isclose(cancellation_total, 0.0, abs_tol=1e-12)
    assert all(x["geometric_contact_present"] for x in cancellation_contacts)

    return {
        "status": "arithmetic_checks_passed",
        "evidence_class": "source-equation arithmetic; synthetic counterexamples and nominal-deck calculation",
        "is_simulation": False,
        "contains_measured_unloading_results": False,
        "source_references": {
            "law": "upstream/normal_model_hooke_hysteresis.h:117,150-198 (fixed 3d5c00f)",
            "gravity": "upstream/fix_gravity.cpp:331-338,377-397 (fixed 3d5c00f)",
            "deck": "source/docs/reviews/codex_ps45_porosity_evidence_20261001/reference/dem_scripts/ps_sweep_6mah_20260914/in.ps_7_3_r45.liggghts:3-4,25,39-41,48,55-90,107-109,189,193",
        },
        "threshold_formulas": {
            "delta_lim": "a/(a-1) * phiF * 2*r_eff",
            "delta_zero": "(1-1/a)*delta_lim = phiF*2*r_eff",
            "delta_adhesion_switch": "(a-1)/(a+c)*delta_lim",
            "condition": "Stored deltaMax >= delta_lim. Zero and adhesion thresholds describe the saturated elastic/cohesive law; normal damping is excluded.",
        },
        "contact_thresholds": thresholds,
        "gravity_scales": {
            "interpretation": "deck/reference ratio under registered length and pressure convention; not full Hooke similarity",
            "length": s_length,
            "density": s_density,
            "pressure": s_pressure,
            "mass": s_mass,
            "force": s_force,
            "acceleration": s_acceleration,
            "deck_g_for_physical_weight_stress_ratio_m_s2": g * s_acceleration,
            "same_g_deck_weight_pressure_amplification": s_length,
            "same_g_reported_weight_pressure_amplification": s_length / s_pressure,
        },
        "nominal_7_3_selfweight": {
            "evidence_class": "nominal deck particle counts; NOT actual S0 particle counts or measured force",
            "components": components,
            "area_deck_m2": area_deck,
            "mass_deck_kg": mass_deck,
            "full_height_weight_pressure_deck_pa": weight_pressure_deck_pa,
            "full_height_weight_pressure_reported_mpa": weight_pressure_reported_pa / 1e6,
            "physical_reference_mass_kg": physical_mass,
            "physical_reference_area_m2": physical_area,
            "physical_reference_weight_pressure_pa": physical_weight_pressure_pa,
            "reported_to_physical_weight_pressure_ratio": weight_pressure_reported_pa / physical_weight_pressure_pa,
        },
        "synthetic_non_saturated_S0": {
            "evidence_class": "synthetic source-law counterexample, NOT observed S0 data",
            "k2Max_over_kn": a,
            "stored_deltaMax_over_delta_lim": stored_max,
            "current_delta_S0_over_delta_lim": current_overlap,
            "k2_over_kn": k2_over_kn,
            "zero_overlap_over_delta_lim": zero_overlap,
            "remaining_recovery_over_delta_lim": remaining_recovery,
            "remaining_recovery_percent_of_current_overlap": remaining_percent,
            "recovery_if_starting_at_deltaMax_over_delta_lim": stored_max / k2_over_kn,
        },
        "synthetic_contact_force_cancellation": {
            "evidence_class": "synthetic two-contact counterexample, NOT measured wall forces",
            "k2Max_over_kn": 3.0,
            "kc_over_kn": 2e5,
            "normal_velocity": 0.0,
            "contacts": cancellation_contacts,
            "total_force_over_kn_delta_lim": cancellation_total,
            "contact_count": len(cancellation_contacts),
            "conclusion": "Zero total normal force does not imply zero contacts.",
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = calculate()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "output": str(args.output), "is_simulation": False}))


if __name__ == "__main__":
    main()
