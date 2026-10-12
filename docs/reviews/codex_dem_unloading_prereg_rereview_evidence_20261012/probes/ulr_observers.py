"""Synthetic observer-contract arithmetic only; no DEM, source mutation or git.

Run from the review folder: python -X utf8 -B probes/ulr_observers.py
The alternative policies below are illustrations of choices left unspecified,
not a proposed implementation and not measured unloading results.
"""
import json
import math
import statistics


def main():
    dt0, dt_half, w0 = 1e-6, 5e-7, 5000
    tol = 1e-3
    forces = (1e-5, -1e-5)
    denominator = 1e-2
    per_particle = sum(abs(f) for f in forces) / denominator
    globally_cancelled = abs(sum(forces)) / denominator
    assert per_particle > tol and globally_cancelled <= tol

    # The stated 1 MPa >= 3 sigma rule can reverse merely by ddof.
    samples = [1 - 0.33, 1 + 0.33] * 10
    sigma_population = statistics.pstdev(samples)
    sigma_sample = statistics.stdev(samples)
    assert 3 * sigma_population <= 1 < 3 * sigma_sample

    # 99 filled cells at 100 um, one empty cell; no particle moves.
    occupied_mean = 99 * 100 / 99
    fixed_grid_zero_mean = 99 * 100 / 100
    # Conventional linear interpolation vs nearest-rank on 99*100, 1*200.
    n, p = 100, 0.999
    linear_index = (n - 1) * p
    p_linear = 100 + (linear_index - math.floor(linear_index)) * 100
    p_nearest_rank = 200

    # Same S0 exclusion set vs per-frame plate cutoff on unchanged atoms.
    fixed_id_surface = (100 + 100) / 2
    reentered_surface = (100 + 100 + 120) / 3

    report = {
        "evidence_class": "synthetic arithmetic illustrating unspecified observer policies",
        "is_simulation": False,
        "contains_unloading_results": False,
        "S3_norm_order": {
            "total_particle_forces_N": forces,
            "common_denominator_N": denominator,
            "tolerance": tol,
            "sum_particle_norms_residual": per_particle,
            "norm_global_sum_residual": globally_cancelled,
            "conclusion": "Local imbalance can disappear under a global vector sum; freeze the exact functional form."
        },
        "windows": {
            "baseline_dt_s": dt0,
            "half_dt_s": dt_half,
            "baseline_W_steps": w0,
            "baseline_T_W_s": w0 * dt0,
            "half_dt_fixed_5000_T_W_s": w0 * dt_half,
            "half_dt_same_time_W_steps": int(w0 * dt0 / dt_half),
            "baseline_hold_4_12_s": [4 * w0 * dt0, 12 * w0 * dt0],
            "half_dt_fixed_5000_hold_4_12_s": [4 * w0 * dt_half, 12 * w0 * dt_half],
            "correct_half_dt_hold_4_12_steps": [40000, 120000],
            "correct_half_dt_UV_hold_8_24_steps": [80000, 240000],
            "k0_3_complete_windows_adjacent_differences": 2,
            "R_2000_complete_5000_windows": 0,
            "constant_surface_speed_um_per_deck_s": 0.6,
            "surface_change_base_um": 0.6 * w0 * dt0,
            "surface_change_half_dt_fixed_5000_um": 0.6 * w0 * dt_half,
            "registered_S4_limit_um_per_window": 0.002,
        },
        "sigma_sample_rule": {
            "sample_count": len(samples),
            "sample_values_MPa": samples,
            "population_sigma_MPa": sigma_population,
            "sample_sigma_MPa": sigma_sample,
            "three_population_sigma_MPa": 3 * sigma_population,
            "three_sample_sigma_MPa": 3 * sigma_sample,
            "Pmeas_MPa": 1.0,
            "population_rule_noise_floor": False,
            "sample_rule_noise_floor": True,
        },
        "surface_empty_cell": {
            "grid_cells": 100,
            "filled_cells": 99,
            "filled_height_um": 100,
            "omit_empty_cell_mean_um": occupied_mean,
            "zero_empty_cell_mean_um": fixed_grid_zero_mean,
            "absolute_policy_difference_um": occupied_mean - fixed_grid_zero_mean,
        },
        "surface_quantile": {
            "sample_description": "99 values equal to 100 um and one value equal to 200 um",
            "percentile": 99.9,
            "linear_um": p_linear,
            "nearest_rank_um": p_nearest_rank,
        },
        "surface_fixed_ID": {
            "unchanged_particle_heights_um": [100, 100, 120],
            "S0_plate_height_um": 110,
            "later_plate_height_um": 130,
            "S0_excluded_IDs": [3],
            "fixed_ID_mean_um": fixed_id_surface,
            "per_frame_plate_cut_mean_um": reentered_surface,
            "spurious_recovery_percent": 100 * (reentered_surface - fixed_id_surface) / fixed_id_surface,
        },
        "accepted_units": {
            "report_MPa_per_Ps": 1000,
            "Ps_for_report_1_MPa": 0.001,
            "W_report_per_W_deck": 1e-6,
        },
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
