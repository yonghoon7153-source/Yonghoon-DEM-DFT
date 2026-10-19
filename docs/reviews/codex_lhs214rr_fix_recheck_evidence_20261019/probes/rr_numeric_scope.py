"""Read-only scope controls: channel metadata versus ionic branch certificate policy."""
from pathlib import Path
import copy
import json
import os
import sys

ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT.parent
SOURCE=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT/'source'
TAG='base_' if len(sys.argv)>1 else ''
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
sys.path[:0]=[str(SOURCE/'scripts'),str(SOURCE/'webapp'),str(WORK/'lhs_coverage_review_20260930/deps'),str(WORK/'gen2_network_reverify3_20261007/deps')]
import tau_flux as tf
import pipeline_service as ps

ind=json.loads((ROOT/'evidence/rr_numeric_independent.json').read_text(encoding='utf8'))
original=ind['fresh_normal']['record']
ledger=dict(thickness_um=20.,thickness_mass_conserving_um=20.,phi_se_mass_conserving=21*4*__import__('math').pi/3/180,percolation_pct=100.)
rid='rr-numeric-scope-independent'

def run(name,dual):
    folder=ROOT/'tmp'/('rr_numeric_scope_'+TAG+name);folder.mkdir(exist_ok=True)
    for filename,obj in [('network_conductivity_dual.json',dual),('network_conductivity_hertzian.json',dual['hertzian']),
                         ('network_conductivity.json',dual['hertzian']),('network_conductivity_physics.json',dual['physics'])]:
        (folder/filename).write_text(json.dumps(obj,ensure_ascii=False),encoding='utf8')
    fm=dict(ledger,network_run_id=rid,active_network_run_id=rid,network_solver_status='success')
    h,p=dual['hertzian'],dual['physics']
    fm.update({k:h[k] for k in ps.NET_MERGE_KEYS if h.get(k) is not None})
    fm.update({k+'_physics':p[k] for k in ps.NET_PHYSICS_MIRROR_KEYS if p.get(k) is not None})
    fm.update({k:p[k] for k in ps.NET_PHYSICS_TAILED_KEYS if p.get(k) is not None})
    (folder/'full_metrics.json').write_text(json.dumps(fm,ensure_ascii=False),encoding='utf8')
    row=tf.ion_columns(dual,ledger,100.)
    return dict(content=ps.network_content_verdict(str(folder)),record=ps.network_record_verdict(str(folder)),
                stop=ps.network_stop_verdict(str(folder),rid,fm),generation=tf.network_generation_contract(dual),
                tau_status=row['ion_net_status_hertz'],f=row['f_ion_hertz'],tau2=row['tau2_ion_hertz'],
                channel=ps.channel_verdict(h,'ionic','hertz'),full_status=h['sigma_full_status'],full_sigma=h['sigma_full'],
                ionic_status=h['ionic_status'],ionic_status_reason=h.get('ionic_status_reason'),folder=str(folder))

out={'source':str(SOURCE),'baseline':run('baseline',original),'channel_mutants':{},'excluded_cert_labels':{}}
for state in ('valid_zero','valid_null','no_result'):
    d=copy.deepcopy(original);d['hertzian']['ionic_status']=state
    d['hertzian']['ionic_status_reason']='no_through_path'
    out['channel_mutants'][state]=run(state,d)
for prefix in ('thermal_','electronic_'):
    for suffix in ('full','bulk_net','constr_net'):
        key=prefix+'solve_certificate_'+suffix
        c=original['hertzian'].get(key)
        if not isinstance(c,dict):continue
        d=copy.deepcopy(original);d['hertzian'][key]['status']='model_over_conduction';d['hertzian'][key]['reason']='q_gt_1p5'
        out['excluded_cert_labels'][key]={'original_status':c['status'],'original_reason':c.get('reason'),'result':run(key,d)}
target=ROOT/'evidence'/('rr_numeric_scope_'+TAG.rstrip('_')+'.json' if TAG else 'rr_numeric_scope.json')
target.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'baseline':out['baseline'],
                  'channel_mutants':{k:{x:v[x] for x in ('content','record','stop','tau_status','f','full_sigma','ionic_status')} for k,v in out['channel_mutants'].items()},
                  'excluded_cert_labels':{k:v['result']['stop'] for k,v in out['excluded_cert_labels'].items()}},ensure_ascii=False))
