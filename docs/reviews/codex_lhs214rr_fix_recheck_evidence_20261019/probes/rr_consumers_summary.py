"""Summarize retained evidence; only declared run identities/path roots normalize."""
import json
from pathlib import Path
import rr_consumers_run as R

def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def diff(a, b, prefix=''):
    if isinstance(a, dict) and isinstance(b, dict):
        return sum((diff(a.get(k), b.get(k), prefix + '.' + k) for k in sorted(set(a) | set(b))), [])
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        return sum((diff(x, y, prefix + f'[{i}]') for i, (x, y) in enumerate(zip(a, b))), [])
    return [] if a == b else [{'path': prefix, 'before': a, 'after': b}]

new = load(R.EV / 'consumers_probe.json')
old = load(R.WS / 'lhs214r_fix_recheck_20261017/evidence/consumers_probe.json')
ids = {r['run_id'] for report in (new, old) for r in report['cases'].values()}
def normalize(obj):
    if isinstance(obj, dict):
        return {k: normalize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [normalize(v) for v in obj]
    if isinstance(obj, str):
        for identity in ids:
            obj = obj.replace(identity, '<RUN_ID>')
        for root in ('lhs214r_fix_recheck_20261017', 'lhs214rr_recheck_20261019'):
            obj = obj.replace(root, '<REVIEW>')
        return obj.replace('evidence/rr_consumers/', 'evidence/').replace('evidence\\rr_consumers\\', 'evidence\\')
    return obj

resurrection = load(R.EV / 'resurrection_capture.json')
r04 = load(R.EV / 'independent_r04.json')
base = load(R.EV / 'baseline.json')
summary = {
    'old_chain_normalization': 'Only actual run_id strings, review folder names and new evidence subfolder; no numerical normalization.',
    'old_chain_differences': diff(normalize(old), normalize(new)),
    'five_fresh_producer_cases': {k: {'status': v['status'], 'reread_ok': all(c['ok'] for c in v['reread_checks']),
                                      'primary_hold': bool(v['release_primary_hold'])} for k, v in new['cases'].items()},
    'r01_original_counterexample': {
        'content': resurrection['after']['content']['value'][0],
        'record': resurrection['after']['record']['value'][0],
        'stop': resurrection['after']['stop']['value'][0],
        'numerical_certificate_unchanged': resurrection['after']['certificate_numeric_unchanged'],
        'generation': resurrection['after']['row']['ion_net_generation'],
        'load_refusal': resurrection['caught_exception'],
        'reread_failed': [c['name'].split()[0] for c in resurrection['independent_after_refusal_reread']['value']['checks'] if not c['ok']],
        'output_absent': not resurrection['release_output_exists'],
    },
    'normal_fresh_build': {'n_files': base['release_baseline']['value']['n_files'],
                          'warnings': base['release_baseline']['value']['warnings'],
                          'tau_reread': base['release_baseline']['value']['tau_reread'],
                          'check': base['release_baseline_check']},
    'r04_independent': {},
    'restored_check': r04['restored_existing_release_check'],
}
for name, v in r04['variants'].items():
    summary['r04_independent'][name] = {
        'numeric_unchanged': v['numerical_leaves_unchanged'],
        'content': v['content']['value'][0], 'record': v['record']['value'][0], 'stop': v['stop']['value'][0],
        'publication_general_rejects': bool(v['publication_general']['value'][1][0]),
        'publication_stop_rejects': bool(v['publication_stop_path']['value'][1][0]),
        'all_tau_blank': all(v['row'][f'f_ion_{m}'] is None and v['row'][f'ion_net_status_{m}'] == 'NOT_COMPUTED' for m in tf_modes) if (tf_modes := ('hertz', 'physics', 'hertz_h12')) else False,
        'fresh_source_rejects_R04': 'L214R-R04' in (v['fresh_build_stale_gate']['exception'] or ''),
        'fresh_actual_gate_rejects_K2': 'K2' in (v['fresh_build_actual_gate']['exception'] or ''),
        'existing_check_with_stale_gate': v['existing_release_check_with_unchanged_gate'],
        'outputs_absent': v['outputs_absent'],
    }
R.save('summary.json', summary)
print(json.dumps(summary, ensure_ascii=False, indent=2))
