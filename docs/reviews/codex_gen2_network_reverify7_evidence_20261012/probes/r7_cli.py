"""Actual S0/S0b consumer with three real synthetic publications, fixed 10-09 case15 report."""
from pathlib import Path
import os,sys,tempfile,json,copy,contextlib,io,shutil
R=Path(__file__).resolve().parents[1];S=R/'source';E=R/'evidence'
T=Path(tempfile.mkdtemp(prefix='r7_cli_',dir=R/'tmp'))
sys.path[:0]=[str(S/'scripts'),str(S/'webapp')]
os.environ.update(SUPABASE_URL='',SUPABASE_KEY='',PYTHONDONTWRITEBYTECODE='1')
for key,tail in [('WEBAPP_UPLOAD_FOLDER','uploads'),('WEBAPP_RESULTS_FOLDER','results'),('WEBAPP_ARCHIVE_FOLDER','archive'),('WEBAPP_MPM_LAB_FOLDER','mpm_lab')]:
    p=T/tail;p.mkdir();os.environ[key]=str(p)
import app,test_gen2_publication_handover as PH,wsl_network_smoke as sm,g2_network_reread as rr
root=T/'consumer';results=root/'work/results';results.mkdir(parents=True)
with contextlib.redirect_stdout(io.StringIO()):
    for bed in ('through','nonthrough','clamp'):
        d,status,failed,rid=PH._publish(app,'baseline',bed=bed)
        assert status=='done',(bed,status,failed)
        shutil.copytree(d,results/bed)
origin=S/'docs/reviews/codex_gen2_network_reverify6_evidence_20261011/evidence'
base=json.loads((origin/'r6_s0b_positive.input.json').read_text(encoding='utf8'))
cases=[]
for name in ('positive','raw_sha_missing','raw_sha_mismatch','negative_area_positive','negative_area_missing','raw_sha_flag_false','actual_permission_error'):
    cases.append((name,json.loads((origin/f'r6_s0b_{name}.input.json').read_text(encoding='utf8')),0 if name=='positive' else 1))
def add(name,fn,want):
    d=copy.deepcopy(base);fn(d['reports']['case15_network']);cases.append((name,d,want))
add('positive_row_reversed',lambda r:r['negctl']['negative_area'].reverse(),0)
add('positive_sha_reordered',lambda r:r.update(raw_sha=dict(reversed(list(r['raw_sha'].items())))),0)
add('positive_unknown_empty_tau',lambda r:r['tau'].update(extra=None),0)
add('area_positive_four_columns',lambda r:r['negctl']['negative_area'][0].__setitem__(2,.186036),1)
add('area_inf_four_columns',lambda r:r['negctl']['negative_area'][0].__setitem__(2,float('-inf')),1)
add('area_display_ulp',lambda r:r['negctl']['negative_area'][0].__setitem__(2,-.18603600000000003),1)
add('delta_zero',lambda r:r['negctl']['negative_area'][0].__setitem__(3,0.),1)
add('delta_inf',lambda r:r['negctl']['negative_area'][0].__setitem__(3,float('inf')),1)
add('id_bool',lambda r:r['negctl']['negative_area'][0].__setitem__(0,True),1)
add('raw_expected_forged_together',lambda r:r['raw_sha'].__setitem__('atom_v4_1710000.liggghts',['0123456789ab']*2),1)
add('raw_uppercase',lambda r:r['raw_sha'].__setitem__('atom_v4_1710000.liggghts',['F40F69ECCD79']*2),1)
add('failed_stage_extra',lambda r:r['failed_stages'].append('Parse'),1)
add('unknown_tau_zero',lambda r:r['tau'].update(extra_numeric=0),1)
add('unknown_tau_nan',lambda r:r['tau'].update(extra_numeric=float('nan')),1)
add('known_tau_string',lambda r:r['tau'].update(tau_ion_hertz='3.21'),1)
# Boundary probe, not a required mutation: producer supplies a flat selected mapping.
add('boundary_nested_tau_number',lambda r:r['tau'].update(extra={'number':3.21}),0)
rows=[]
for name,doc,want in cases:
    sm.write_json(root/'smoke_report.json',doc)
    output=E/f'cli_{name}.json';cap=io.StringIO()
    with contextlib.redirect_stdout(cap):rc=rr.main(['--smoke-root',str(root),'--json',str(output)])
    result=json.loads(output.read_text(encoding='utf8'))
    (E/f'cli_{name}.input.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2),encoding='utf8')
    (E/f'cli_{name}.log').write_text(cap.getvalue(),encoding='utf8')
    meta=result['meta']
    rows.append(dict(name=name,rc=rc,n_fail=result['n_fail'],expected_rc=want,meta=meta,matched=rc==want and result['n_fail']==want))
out=dict(scope=__doc__,root=str(root),no_dem_simulation=True,rows=rows,all_expected=all(x['matched'] for x in rows))
(E/'r7_cli.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(dict(rows=[{k:x[k] for k in ('name','rc','n_fail','expected_rc','matched')} for x in rows],all_expected=out['all_expected']),ensure_ascii=False))
assert out['all_expected']
