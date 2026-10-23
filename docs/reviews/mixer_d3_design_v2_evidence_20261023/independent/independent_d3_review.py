#!/usr/bin/env python3
"""Independent D3 design probes; no author test imports or simulator runs.

Usage: python -I independent_d3_review.py --repo /path/to/Yonghoon-DEM-DFT
Only optional production-function checks require the repository's numpy.
All numerical examples are synthetic, not measured material properties.
"""
import argparse
import hashlib
import importlib.util
import json
import math
import pathlib
import sys


def load_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=pathlib.Path, required=True)
    args = parser.parse_args()
    root = args.repo.resolve()
    result = {'scope': 'Independent analytic/synthetic probes; no DEM/measurement/ratification',
              'checks': [], 'numbers': {}, 'source_sha256': {}}

    def check(name, condition, detail):
        result['checks'].append({'name': name, 'pass': bool(condition), 'detail': detail})

    # Derive Bo from Hertz equilibrium force, avoiding the generator's CED inversion.
    r = 151.4e-6 / 2
    nu = 0.30
    e_soft = 1e7
    e_star = e_soft / (2 * (1 - nu**2))
    hertz = (4 / 3) * e_star * math.sqrt(r / 2) * r**1.5
    expected = {
        'gen1': (2.00, 4.80, 832.6622, .836744, 1.013643),
        'lab20261014': (1.64, 4.85, 1015.4417, .733052, .888030),
    }
    maker = load_file('d3_independent_maker', root / 'scripts/make_mixer_deck.py')
    for gen, (rho_gcc, am_rho, ceiling_print, low_print, high_print) in expected.items():
        mass = (4 / 3) * math.pi * r**3 * rho_gcc * 1000
        weight = mass * 9.81
        ceiling = hertz * .01**1.5 / weight
        delta = lambda bo: (bo * weight / hertz)**(2 / 3)
        soft = {str(bo): delta(bo) * 100 for bo in (637.32, 849.76)}
        dt = (.2 * math.pi * r * math.sqrt(rho_gcc * 1000 / (e_soft * 20 / (2 * (1 + nu))))
              / (.1631 * nu + .8766))
        plan = maker.plan(100000, cgf=151.4, stiffen_se=20, dens_gen=gen)
        d = {'AM_P': 9e-6 * 151.4, 'AM_S': 4e-6 * 151.4, 'SE': 1e-6 * 151.4}
        w = {'AM_P': 56, 'AM_S': 24, 'SE': 18}
        density = {'AM_P': am_rho, 'AM_S': am_rho, 'SE': rho_gcc}
        c = {k: w[k] / (density[k] * d[k]**3) for k in d}
        count = {k: round(100000 * c[k] / sum(c.values())) for k in d}
        solid_v = count['AM_P'] * math.pi * d['AM_P']**3 / 6
        phi_p = (56 / am_rho) / (80 / am_rho + 18 / rho_gcc)
        volume = solid_v / phi_p / (.3 * .6)
        radius = (2.5 * volume / math.pi)**(1 / 3)
        rpm = 60 / (2 * math.pi) * math.sqrt(.0827 * 9.81 / radius)
        result['numbers'][gen] = {
            'am_p_Bo_ratio_denominator': (am_rho / rho_gcc) * 9**2,
            'soft_ceiling_Bo': ceiling, 'stiff20_homogeneous_ceiling_Bo': ceiling * 20,
            'delta_percent': soft, 'upper_factor_from_637_32': ceiling / 637.32,
            'cgf200_delta_percent_Bo637_32': delta(637.32) * (200 / 151.4)**(2 / 3) * 100,
            'drum_diameter_mm': radius * 2000, 'drum_length_mm': radius / 2.5 * 1000,
            'rpm': rpm, 'dt_s': dt, 'assumed_hours_per_simulated_second': [1 / dt / s / 3600 for s in (70, 63)],
        }
        check(gen + '_printed_statics', abs(ceiling - ceiling_print) < .00005
              and abs(soft['637.32'] - low_print) < .0000005
              and abs(soft['849.76'] - high_print) < .0000005,
              result['numbers'][gen])
        ced = maker.ced_for_bond(637.32, r, nu, rho_gcc, E=e_soft)
        generated_delta = maker.overlap_for_ced(ced, r, nu, E=e_soft)
        check(gen + '_CED_vs_independent_Hertz', math.isclose(delta(637.32), generated_delta, rel_tol=1e-12),
              {'Hertz': delta(637.32), 'CED': generated_delta})
        check(gen + '_geometry_and_timestep', math.isclose(radius, plan['R'], rel_tol=1e-12)
              and math.isclose(dt, plan['dt'], rel_tol=1e-12)
              and math.isclose(rpm, maker.rpm_for_fr(.0827, plan['R']), rel_tol=1e-12),
              {'independent_R': radius, 'production_R': plan['R'], 'independent_dt': dt, 'production_dt': plan['dt']})

    # D3K-01: two observables can agree despite a wrong nuisance parameter.
    a1, a2, b1, b2, nuisance_delta = 2, 4, 6, 12, .1
    x1, x2 = -b1 / a1 * nuisance_delta, -b2 / a2 * nuisance_delta
    check('confounded_two_tests', x1 == x2 and x1 != 0, {'inferred_log10_Bo_shifts': [x1, x2]})
    det = (2 * 1.5 / 5 + 2 * 1.5 / 5) / abs(40 / 5 - 10 / 5)
    check('local_detection_threshold', math.isclose(det, .2), {'minimum_abs_delta_mu': det})

    # D3K-02: complete finite-grid rejection still cannot reject all continuous Bo.
    grid = [1.0, 2.0]
    forward = lambda b: (b - 1.5)**2
    accepted = [b for b in grid if abs(forward(b) - 0.0) <= .01]
    check('empty_complete_grid_not_continuous_rejection', not accepted and forward(1.5) == 0,
          {'grid': grid, 'grid_outputs': [forward(b) for b in grid], 'accepted': accepted,
           'interior_true_Bo': 1.5, 'interior_output': forward(1.5), 'm': 0, 'tolerance': .01})
    step = lambda x: 0 if x < .9 else 10
    check('monotone_half_difference_not_error_bound', abs(step(.89) - 8.9) > 5,
          {'monotone_actual_at_0_89': step(.89), 'endpoint_interpolant': 8.9, 'half_endpoint_difference': 5})
    center = math.sqrt(.672 * 212)
    check('disconnected_hull_center_outside', not (.672 <= center <= 2.12 or 67.2 <= center <= 212),
          {'geometric_hull_center': center})
    check('two_seed_small_SD_probability', math.isclose(math.erf(.5 / math.sqrt(2)), .3829249225480262),
          {'P_s_less_than_half_sigma_normal_iid_n2': math.erf(.5 / math.sqrt(2))})
    wall = lambda x: x * (1 - x)
    check('wall_endpoint_not_envelope', wall(0) == wall(1) == 0 and wall(.5) == .25,
          {'endpoints': [wall(0), wall(1)], 'midpoint': wall(.5)})

    # A spatially valid finite-frame contract is distinct from all-time validity.
    overlap = lambda t: .005 + .015 * math.sin(math.pi * t)**2
    check('stored_frames_not_all_time_guard', max(overlap(t) for t in (0, 1)) < .01 and overlap(.5) > .01,
          {'stored_max': max(overlap(t) for t in (0, 1)), 'between_frame': overlap(.5), 'limit': .01})
    check('static_ceiling_not_loaded_ceiling', 2**(2 / 3) * .01 > .01,
          {'overlap_if_applied_load_doubles_reference_force': 2**(2 / 3) * .01})
    # A finite positive candidate set cannot reject the zero-cohesion null.
    f0 = lambda b: 0 if b <= 1 else b - 1
    check('positive_candidates_not_positive_cohesion_evidence', f0(0) == f0(.21244) == 0,
          {'null_output': f0(0), 'positive_candidate_output': f0(.21244)})

    # Unknowns are neither rejected nor supported; partial validation needs its own result.
    holdout_predictions = {1: 0, 2: 10}
    passed = [b for b, prediction in holdout_predictions.items() if abs(prediction) <= 1]
    check('all_candidates_predicted_not_all_candidates_validated', len(passed) == 1 < len(holdout_predictions),
          {'calibration_candidates': [1, 2], 'holdout_predictions': holdout_predictions,
           'holdout_m': 0, 'tolerance': 1, 'passed': passed, 'failed': [2]})
    check('stop_for_all_candidates_has_no_discrimination', len(set(['STOP'] * 8)) == 1,
          {'n_candidates': 8, 'unique_holdout_outcomes': 1})
    check('two_independent_point95_not_joint95', math.isclose(.95**2, .9025),
          {'two_tests_joint_coverage_if_independent': .95**2,
           'any_false_accept_if_8_independent_rejections_at_95': 1 - .95**8})
    check('day_component_not_within_day_SE', 3 > 1 / math.sqrt(5),
          {'within_day_SE': 1 / math.sqrt(5), 'day_mean_shift': 3})
    initial = [maker.BO_BASE * 10**(k / 2) for k in range(7)] + [3000 * maker.BO_BASE]
    check('last_grid_ratio_is_three', math.isclose(initial[-1] / initial[-2], 3),
          {'grid': initial, 'last_ratio': initial[-1] / initial[-2]})
    check('Bo_G_is_separate_transform', not math.isclose(637.32, 637.32 / 268),
          {'hypothetical_G': 268, 'one_g_Bo': 637.32, 'transformed_Bo': 637.32 / 268})

    # Exercise actual production refusal without making any fixture deck.
    checker = load_file('d3_independent_validity', root / 'scripts/check_contact_validity.py')
    for mesh in ('Funnel', 'TapFloor'):
        try:
            checker.container_at(str(root), {'used': [mesh]}, 0)
        except ValueError as exc:
            rejected = '지원하지 않는다' in str(exc)
            message = str(exc)
        else:
            rejected, message = False, 'accepted'
        check('actual_' + mesh + '_unsupported', rejected, message)
    try:
        maker.set_phases(('SE',))
    except AssertionError as exc:
        rejected, message = True, str(exc)
    else:
        rejected, message = False, 'accepted'
    check('actual_SE_only_type_unsupported', rejected, message)

    for rel in ('scripts/make_mixer_deck.py', 'scripts/check_contact_validity.py',
                'docs/reviews/mixer_d3_se_flowability_anchor_design_20261015.md',
                'docs/reviews/codex_mixer_d3_design_request_20261021.md',
                'docs/mixer_paper_pipeline_draft_20261013.md'):
        result['source_sha256'][rel] = hashlib.sha256((root / rel).read_bytes()).hexdigest()
    result['summary'] = {'passed': sum(row['pass'] for row in result['checks']), 'total': len(result['checks'])}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if all(row['pass'] for row in result['checks']) else 1


if __name__ == '__main__':
    raise SystemExit(main())
