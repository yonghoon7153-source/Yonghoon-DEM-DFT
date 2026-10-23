#!/usr/bin/env python3
"""Read-only analytical witnesses for the D3 v2 DESIGN, not a production judge.

No experimental measurements, DEM runs, decks, or files are created. Numbers in
synthetic witnesses are examples, never registration values. Stdout is JSON.
The tests establish the counterexamples and arithmetic, not coverage guarantees
or implementation of the proposed D3 workflow.
"""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import statistics
import subprocess
import sys

sys.dont_write_bytecode = True
ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path, required=True)
args = ap.parse_args()
repo = args.repo.resolve()
checks = []
results = {}


def check(name, condition, detail):
    checks.append({'name': name, 'pass': bool(condition), 'detail': detail})


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, repo / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


m = load('d3_generator', 'scripts/make_mixer_deck.py')
ccv = load('d3_contract', 'scripts/check_contact_validity.py')
source_files = ['scripts/make_mixer_deck.py', 'scripts/check_contact_validity.py',
                'dem_scripts/mixer_20260921/launch_policy.json',
                'docs/reviews/mixer_d3_se_flowability_anchor_design_20261015.md',
                'docs/reviews/codex_mixer_d3_design_request_20261021.md']
results['provenance'] = {
    'head': subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip(),
    'sha256': {p: hashlib.sha256((repo / p).read_bytes()).hexdigest() for p in source_files},
    'python': sys.version.split()[0],
    'kind': 'analytical witnesses; no production judge, calibration, registration, or experiment',
}

# D3K-01: a common nuisance direction moves both inversions together.
xtrue, delta = 1.0, 0.0375
x1 = xtrue - (40.0 / 5.0) * delta
x2 = xtrue - (40.0 / 5.0) * delta
check('D3K-01-common-bias', x1 == x2 and x1 != xtrue,
      {'true_log10Bo': xtrue, 'both_inferred': x1, 'nuisance_delta': delta})
dmin = (2 * 1.5 / 5 + 2 * 1.5 / 5) / abs(40 / 5 - 10 / 5)
check('D3K-01-detection-limit', math.isclose(dmin, 0.2) and dmin > 0.5 * 0.075,
      {'minimum_detectable_delta': dmin, 'old_probe_half_width': 0.5 * 0.075})

# D3K-02: finite sample agreement cannot bound arbitrary within-cell curves.
# A piecewise-linear triangle has zeros at the original endpoints AND midpoint.
def bump(x):
    return max(0.0, 10.0 * (1.0 - abs(x - 0.125) / 0.125))

sample = [bump(x) for x in (0.0, 0.25, 0.5)]
check('D3K-02-hidden-bump', sample == [0, 0, 0] and bump(0.125) == 10,
      {'samples': sample, 'unsampled_value': bump(0.125), 'half_endpoint_difference': 0})
# Even monotonicity alone gives the whole endpoint range, not half the difference.
actual = 10.0  # jump completed before x=0.05 inside [0,0.5]
linear = 10.0 * 0.05 / 0.5
check('D3K-02-half-difference-not-bound', abs(actual - linear) > 0.5 * 10,
      {'monotone_step_value': actual, 'linear_prediction': linear,
       'absolute_error': abs(actual - linear), 'claimed_half_range': 5})

# D3K-03: interval hull erases a scientifically meaningful gap.
S = [(0.672, 2.12), (67.2, 212.0)]
hull_centre = math.sqrt(S[0][0] * S[-1][1])
check('D3K-03-centre-outside-set', not any(a <= hull_centre <= b for a, b in S),
      {'components': S, 'hull_geometric_centre': hull_centre})
check('D3K-03-empty-vs-disjoint', set([1, 2]).isdisjoint([3, 4]) and set() != set([1, 2]),
      {'test_A': [1, 2], 'test_B': [3, 4], 'each_nonempty_joint_empty': True,
       'different_case_one_test_empty': []})

# D3K-04: one seed cannot supply a sample SD; two seeds are noisy.
try:
    statistics.stdev([1.0])
    one_seed_undefined = False
except statistics.StatisticsError:
    one_seed_undefined = True
check('D3K-04-one-seed-sd', one_seed_undefined, {'n': 1, 'sample_sd': None})
p_under = math.erf(0.5 / math.sqrt(2))
check('D3K-04-two-seed-probability', 0.3829 < p_under < 0.3830,
      {'normal_iid_example_probability_s_below_half_sigma': p_under, 'df': 1})

# D3K-05: the old wall range misses rho<0.31; endpoints also do not
# bound all interior behavior without a separately justified shape assumption.
wall = {str(rho): 2 * math.sqrt(0.0256 * rho) for rho in (0, 0.01, 0.1, 0.31, 1)}
check('D3K-05-old-wall-range-misses-low-rho', wall['0.1'] < wall['0.31'], wall)
check('D3K-05-endpoints-not-envelope', 0 * (1 - 0) == 1 * (1 - 1) == 0 and 0.5 * (1 - 0.5) > 0,
      {'synthetic_response_at_wall_0_05_1': [0, 0.25, 0]})

# D3K-08: blind curve sealing does not repair post-measurement SOP registration.
synthetic_timeline = {'measurement_start': 1, 'sop_commit': 2, 'curve_seal': 3, 'analyst_open': 4}
check('D3K-08-order', synthetic_timeline['curve_seal'] < synthetic_timeline['analyst_open']
      and synthetic_timeline['sop_commit'] > synthetic_timeline['measurement_start'], synthetic_timeline)

# D3K-10: exercise the actual contract entry point, not a copied name list.
unsupported = {}
for name in ('Funnel', 'TapFloor'):
    try:
        ccv.container_at('/nonexistent_d3_probe', {'used': [name], 'meshes': {}, 'moves': {}}, 0)
        unsupported[name] = None
    except ValueError as exc:
        unsupported[name] = str(exc)
check('D3K-10-actual-contract', all(unsupported.values()), unsupported)

# D3K-13 / MXD2-07: independent closed-form same-size-particle ceiling.
# Equilibrium: delta = [3 CED 2 pi sqrt(R*)/(4 E*)]^2.
# With delta/r=q and R*=r/2, solve CED; then F=2 pi R* CED delta.
def analytic_ceiling(E, nu, radius, rho_gcc, q=0.01):
    E_star = E / (2 * (1 - nu * nu))
    R_star = radius / 2
    ced = 4 * E_star * math.sqrt(q * radius) / (6 * math.pi * math.sqrt(R_star))
    F = 2 * math.pi * R_star * ced * q * radius
    weight = 4 / 3 * math.pi * radius**3 * rho_gcc * 1000 * 9.81
    return F / weight

numbers = {}
for gen in ('gen1', 'lab20261014'):
    p = m.plan(100000, cgf=151.4, stiffen_se=20, dens_gen=gen)
    radius, rho, nu = p['d']['SE'] / 2, p['dens']['SE'], m.PHASE_MECH['SE'][0]
    Esoft = m.E_PHASE['SE']
    cap = analytic_ceiling(Esoft, nu, radius, rho)
    reconstructed = m.overlap_for_ced(m.ced_for_bond(cap, radius, nu, rho, E=Esoft), radius, nu, E=Esoft)
    check(f'MXD2-07-{gen}-closed-form', math.isclose(reconstructed, 0.01, rel_tol=1e-12),
          {'soft_ceiling_Bo': cap, 'generator_overlap_at_cap': reconstructed})
    ov = {}
    for bo in (637.32, 849.76, 1010.0, 1020.0):
        ov[str(bo)] = 100 * m.overlap_for_ced(m.ced_for_bond(bo, radius, nu, rho, E=Esoft), radius, nu, E=Esoft)
    numbers[gen] = {'density_g_cm3': p['dens'], 'soft_ceiling_Bo': cap,
                    'soft_overlap_percent': ov, 'stiff20_analytic_ceiling_Bo': 20 * cap,
                    'soft_upper_extension_factor': cap / 637.32,
                    'drum_D_mm': 2000 * p['R'], 'drum_L_mm': 1000 * p['L'],
                    'rpm_at_Fr': m.rpm_for_fr(m.FR_ANCHOR, p['R']), 'dt_stiff20_s': p['dt'],
                    'one_s_wall_hours_if_63_70_steps_s': [1 / p['dt'] / 70 / 3600, 1 / p['dt'] / 63 / 3600]}
    check(f'D3K-13-{gen}-extension-truncated', cap / 637.32 < math.sqrt(10),
          {'allowed_factor': cap / 637.32, 'sqrt10': math.sqrt(10)})
check('MXD2-07-generation-changes-acceptance',
      numbers['gen1']['soft_overlap_percent']['849.76'] > 1 > numbers['lab20261014']['soft_overlap_percent']['849.76'],
      {'Bo': 849.76, 'gen1': 'above ceiling', 'lab20261014': 'below ceiling'})
# Model floor mismatch is not an exclusive proof of which nuisance was wrong.
check('D3K-13-model-floor', min([10, 10.1, 10.2]) > 8 + 1,
      {'synthetic_prediction_near_zero': [10, 10.1, 10.2], 'measurement': 8,
       'band': 1, 'causal_attribution': 'not identified'})

# Other limitations: topology/observable, conditional transfer, binary censoring,
# daily component, and nonmonotone predictions over an accepted parameter set.
ring = [(1, 0), (0, 1), (-1, 0), (0, -1)]
xx = sum(x*x for x, y in ring) / 4
yy = sum(y*y for x, y in ring) / 4
xy = sum(x*y for x, y in ring) / 4
check('D3K-06-no-free-surface-angle', xx == yy and xy == 0,
      {'symmetric_ring_points': ring, 'second_moment': [[xx, xy], [xy, yy]],
       'principal_axis': 'degenerate; no preferred free-surface direction'})
bo, G = 212.44, 268.0
check('D3K-07-Bo-transfer-conditional', not math.isclose(bo, bo / G),
      {'Bo_1g': bo, 'G_example_only': G, 'Bo_over_G': bo / G,
       'actual_mixer_G': None, 'transfer_rule_approved_here': False})
check('D3K-09-binary-no-discrimination', len(set(['stopped'] * 8)) == 1,
      {'predictions_at_all_eight_levels': 'stopped', 'discriminating_levels': 0})
check('D3K-09-centre-and-ends-miss-interior',
      [int(abs(x - 0.25) < 0.01) for x in [0, 0.5, 1]] == [0, 0, 0],
      {'tested_end_centre': [0, 0.5, 1], 'hidden_transition_at': 0.25,
       'required_without_shape_proof': 'all accepted finite candidates, or explicit unvalidated subset'})
within, n, day_difference = 1.0, 5, 3.0
check('D3K-14-day-uncertainty', within / math.sqrt(n) < day_difference,
      {'within_day_se': within / math.sqrt(n), 'day_mean_difference': day_difference,
       'adequacy_of_actual_replication': 'pending'})
for gen in ('gen1', 'lab20261014'):
    p = m.plan(100000, cgf=151.4, dens_gen=gen)
    ratio = p['dens']['AM'] / p['dens']['SE'] * (p['d']['AM_P'] / p['d']['SE'])**2
    check(f'D3K-15-{gen}-ncm-ratio', ratio > 190,
          {'Bo_AM_P_over_Bo_SE': f'rho / {ratio:.8f}', 'rho_flow_causal_identity': False})
check('D3K-16-last-grid-ratio', math.isclose(3000 * m.BO_BASE / (1000 * m.BO_BASE), 3, rel_tol=1e-14),
      {'last_ratio': 3, 'sqrt10': math.sqrt(10)})

saved_types = m.TYPES
try:
    m.set_phases(('SE',))
    sole_se_rejected = False
except AssertionError:
    sole_se_rejected = True
finally:
    m.set_phases(saved_types)
check('D3K-11-SE-only-generator', sole_se_rejected,
      {'set_phases_SE_only': 'rejected', 'new_geometry_mode': 'not implemented'})
r_small = m.plan(50000, cgf=151.4, dens_gen='lab20261014')['R']
r_big = m.plan(100000, cgf=151.4, dens_gen='lab20261014')['R']
check('D3K-11-budget-changes-geometry', not math.isclose(r_small, r_big),
      {'R_N50000_mm': 1000*r_small, 'R_N100000_mm': 1000*r_big})
policy = json.loads((repo/'dem_scripts/mixer_20260921/launch_policy.json').read_text())
check('D3K-17-no-existing-D3-stage', all('d3' not in s.lower() for s in policy['allowed_stages']),
      {'schema': policy['schema'], 'allowed_stages': policy['allowed_stages']})
results['numerical_table'] = numbers
results['checks'] = checks
results['summary'] = {'passed': sum(c['pass'] for c in checks), 'total': len(checks),
                      'failed': [c['name'] for c in checks if not c['pass']]}
print(json.dumps(results, ensure_ascii=False, indent=2, allow_nan=False))
sys.exit(bool(results['summary']['failed']))
