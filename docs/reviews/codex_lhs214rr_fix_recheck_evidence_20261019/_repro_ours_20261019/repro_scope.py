"""읽기 전용 파생 — Codex rr_numeric_scope.py (L214RR2-03) 와 같은 절차를 우리 트리에서.  Codex 탐침 파일은 실행하지 않는다.
python3 -B repro_scope.py <우리 트리> <반입 증거 폴더> <작업 폴더> <out.json>"""
import copy
import json
import math
import os
import sys
from pathlib import Path
TREE, EV, WORK, OUT = (Path(a).resolve() for a in sys.argv[1:5])
for k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[k] = '1'
sys.path[:0] = [str(TREE / 'scripts'), str(TREE / 'webapp')]
sys.dont_write_bytecode = True
import tau_flux as tf  # noqa: E402
import pipeline_service as ps  # noqa: E402
ind = json.loads((EV / 'evidence/rr_numeric_independent.json').read_text(encoding='utf-8'))
original = ind['fresh_normal']['record']
ledger = dict(thickness_um=20., thickness_mass_conserving_um=20., phi_se_mass_conserving=21 * 4 * math.pi / 3 / 180, percolation_pct=100.)
rid = 'rr-numeric-scope-independent'


def run(name, dual):
    folder = WORK / ('scope_' + name)
    folder.mkdir(parents=True, exist_ok=True)
    for fn, obj in (('network_conductivity_dual.json', dual), ('network_conductivity_hertzian.json', dual['hertzian']),
                    ('network_conductivity.json', dual['hertzian']), ('network_conductivity_physics.json', dual['physics'])):
        (folder / fn).write_text(json.dumps(obj, ensure_ascii=False), encoding='utf-8')
    fm = dict(ledger, network_run_id=rid, active_network_run_id=rid, network_solver_status='success')
    h, p = dual['hertzian'], dual['physics']
    fm.update({k: h[k] for k in ps.NET_MERGE_KEYS if h.get(k) is not None})
    fm.update({k + '_physics': p[k] for k in ps.NET_PHYSICS_MIRROR_KEYS if p.get(k) is not None})
    fm.update({k: p[k] for k in ps.NET_PHYSICS_TAILED_KEYS if p.get(k) is not None})
    (folder / 'full_metrics.json').write_text(json.dumps(fm, ensure_ascii=False), encoding='utf-8')
    row = tf.ion_columns(dual, ledger, 100.)
    return dict(content=ps.network_content_verdict(str(folder)), record=ps.network_record_verdict(str(folder)),
                stop=ps.network_stop_verdict(str(folder), rid, fm), generation=tf.network_generation_contract(dual),
                tau_status=row['ion_net_status_hertz'], f=row['f_ion_hertz'], tau2=row['tau2_ion_hertz'],
                channel=ps.channel_verdict(h, 'ionic', 'hertz'), full_status=h['sigma_full_status'], full_sigma=h['sigma_full'],
                ionic_status=h['ionic_status'], ionic_status_reason=h.get('ionic_status_reason'))


out = {'baseline': run('baseline', original), 'channel_mutants': {}}
for state in ('valid_zero', 'valid_null', 'no_result'):
    d = copy.deepcopy(original)
    d['hertzian']['ionic_status'] = state
    d['hertzian']['ionic_status_reason'] = 'no_through_path'
    out['channel_mutants'][state] = run(state, d)
cx = json.loads((EV / 'evidence/rr_numeric_scope.json').read_text(encoding='utf-8'))
KEYS = ('content', 'record', 'stop', 'tau_status', 'f', 'tau2', 'full_status', 'full_sigma', 'ionic_status', 'ionic_status_reason')
diff = []
for grp in ('baseline',):
    for k in KEYS:
        if json.dumps(cx[grp].get(k), default=str) != json.dumps(out[grp].get(k), default=str):
            diff.append((grp, k, cx[grp].get(k), out[grp].get(k)))
for st in out['channel_mutants']:
    for k in KEYS:
        a, b = cx['channel_mutants'][st].get(k), out['channel_mutants'][st].get(k)
        if json.dumps(a, default=str) != json.dumps(b, default=str):
            diff.append((st, k, a, b))
out['differences_vs_codex'] = diff
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
print(json.dumps({'baseline': {k: out['baseline'][k] for k in ('content', 'record', 'stop', 'tau_status', 'f')},
                  'mutants': {s: {k: v[k] for k in ('content', 'record', 'stop', 'tau_status', 'f', 'ionic_status')} for s, v in out['channel_mutants'].items()},
                  'n_diff': len(diff), 'diff': diff[:6]}, ensure_ascii=False, default=str)[:3000])
