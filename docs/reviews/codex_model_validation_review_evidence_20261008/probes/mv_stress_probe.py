"""Read-only arithmetic checks of supplied records; no DEM simulation."""
import json
import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
(ROOT / 'evidence').mkdir(exist_ok=True)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
SRC = ROOT / 'source'
DATA = SRC / 'docs/data'
def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

ps = read(DATA / 'ps45_plane_load_20261007/ps45_v2/plane_load.json')
sn = read(DATA / 'ps73_damping_branch_20261007/snap_3100000_20261008/plane/plane_load.json')
real = read(DATA / 'ps45_plane_load_20261007/real14_validation/plane_load.json')
vm = read(DATA / 'ps73_damping_branch_20261007/snap_moments_20261008/results_20261008/vm_moments.json')
report = {'scope': 'Derived JSON arithmetic only; raw dump identities and numerical values not independently reconstructed.', 'cases': {}}
for name, obj in [('ps45', ps), ('snapshot', sn), ('real14', real)]:
    for label, r in obj['cases'].items():
        weights = np.array([q['load_mpa'] for q in r['cuts']])
        contrib = {g: sum(q['load_mpa'] * q['share_group_pct'][g] for q in r['cuts']) / weights.sum() for g in r['contribution_sigma_zz_pct']}
        a = r['alpha']
        vf = a['volume_frac_window']
        phase_share = {p: 100 * v * a['alpha_zz'][p] for p, v in vf.items()}
        c = a['cross_check']
        report['cases'][name + ':' + label] = {
            'n_cuts': len(weights), 'mean_mpa_recalc': float(weights.mean()),
            'contribution_recalc_pct': contrib,
            'contribution_max_abs_error_pp': max(abs(contrib[g] - r['contribution_sigma_zz_pct'][g]) for g in contrib),
            'contribution_integral_difference_pp': {g: contrib[g] - r['contribution_sigma_zz_integral_pct'][g] for g in contrib},
            'phase_contact_virial_share_pct': phase_share,
            'phase_share_sum_pct': sum(phase_share.values()),
            'ratio_lw_planes': c['ratio_lw_over_planes'],
            'lw_edge_fraction': c['edge_lw_mpa'] / c['lw_window_sigma_zz_mpa'],
            'lw_integral_bias_pct': 100 * (c['lw_window_sigma_zz_mpa'] / c['window_integral_sigma_zz_mpa'] - 1),
            'recorded_lw_checks': a['lw']['checks'],
            'n_window': a['n_window'], 'wall_in_window': c['n_window_touching_wall'],
        }

end = ps['cases']['7:3']
snap = next(iter(sn['cases'].values()))
report['snap_to_relaxed'] = {
    'contribution_change_pp': {g: end['contribution_sigma_zz_pct'][g] - snap['contribution_sigma_zz_pct'][g] for g in end['contribution_sigma_zz_pct']},
    'alpha_change': {p: end['alpha']['alpha_zz'][p] - snap['alpha']['alpha_zz'][p] for p in end['alpha']['alpha_zz']},
    'alpha_change_relative_pct': {p: 100 * (end['alpha']['alpha_zz'][p] / snap['alpha']['alpha_zz'][p] - 1) for p in end['alpha']['alpha_zz']},
    'mean_plane_change_pct': 100 * (end['sigma_zz_planes_mean_mpa'] / snap['sigma_zz_planes_mean_mpa'] - 1),
}
report['vm_arithmetic'] = []
for r in vm['moments']:
    item = {'step': r['step'], 'phase_ratios': {}, 'AM_SE_volume_mean_vm_ratio': r['AM']['mean_vm_MPa'] / r['SE']['mean_vm_MPa'], 'all_particle_number_mean_MPa': r['mean_vm_all_MPa']}
    for p in ['AM', 'SE']:
        z = r[p]
        item['phase_ratios'][p] = {'ratio_recalc': z['top_third_mean_vm_MPa'] / z['bottom_third_mean_vm_MPa'], 'wall_excluded_number_pct': 100 * z['n_wall'] / z['n']}
    report['vm_arithmetic'].append(item)
report['provenance_record_matches'] = {k: vm['moments'][-1]['inputs_sha256'][k] == end['inputs_sha256'][k] for k in vm['moments'][-1]['inputs_sha256']}

# Independent analytic counterexamples, explicitly not validation of raw DEM data.
def von_mises(tensor):
    s = .5 * (tensor + tensor.T)
    d = s - np.trace(s) / 3 * np.eye(3)
    return float(np.sqrt(1.5 * np.sum(d * d)))
stresses = [np.diag([3., 0., 0.]), np.diag([0., 3., 0.]), np.diag([0., 0., 3.])]
report['negative_controls'] = {
    'mean_vm_not_vm_mean': {'mean_vm': float(np.mean([von_mises(s) for s in stresses])), 'vm_mean_tensor': von_mises(np.mean(stresses, axis=0))},
    'hydrostatic_stress': {'tensor': (100 * np.eye(3)).tolist(), 'vm': von_mises(100 * np.eye(3)), 'zz': 100.},
    'wall_mean_normalization': {'interior_vm': [10., 10.], 'incomplete_wall_vm': 0., 'mean_interior': 10., 'mean_all': 20/3, 'interior_ratio_by_all': 1.5},
}
b = np.array([.4, .2, .1]); f = np.array([-3., 1., 2.]); V = .2
T = np.outer(b, f) / V
angle = .71
Q = np.array([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1.]])
Tq = np.outer(Q @ b, Q @ f) / V
report['negative_controls']['tensor_rotation'] = {'tensor_covariance_max_error': float(np.max(np.abs(Tq - Q @ T @ Q.T))), 'vm_invariance_abs_error': abs(von_mises(Tq) - von_mises(T))}
# Changing mixed-contact partition changes phase ratios while preserving global virial.
report['negative_controls']['same_global_virial_different_phase_shares'] = {
    'global_virial': 1., 'equal_partition_phase_shares': [.5, .5], 'branch_ratio_4_to_1_shares': [.8, .2],
    'same_equal_phase_volumes_alpha_equal': [1., 1.], 'same_equal_phase_volumes_alpha_branch': [1.6, .4]
}
out = ROOT / 'evidence/mv_stress_arithmetic.json'
out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'snap_to_relaxed': report['snap_to_relaxed'], 'negative_controls': report['negative_controls'], 'case_count': len(report['cases']), 'provenance_record_matches': report['provenance_record_matches'], 'output': str(out)}, indent=2, ensure_ascii=False))
