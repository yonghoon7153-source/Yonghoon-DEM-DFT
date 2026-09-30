"""Reviewer-only units, log, CSV and external-boundary data checks."""
import csv
import hashlib
import json
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parent
R=ROOT/'received'; S=ROOT/'supplement'; T=R/'run/tables'
checks=[]
def check(name,ok):
    checks.append({'check':name,'pass':bool(ok)})
    assert ok,name
def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))
def identity(p):
    with p.open('rb') as f:
        return {'bytes':p.stat().st_size,'sha256':hashlib.file_digest(f,'sha256').hexdigest()}
def rows(p):
    with p.open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))
units={
 'eguard':['s']+['mol/m^3']*5+['1']*3,
 'nglobal':['s']+['mol/m^2']*3+['1']*7+['A/m^2']*3,
 'point1':['s','V','V','V','V','V','1','1','mol/m^3','mol/m^3','mol/m^3','V','A/m^2'],
 'point4':['s','V','V','V','V','V','1','1','mol/m^3','mol/m^3','mol/m^3','V','A/m^2'],
 'MinLinece':['s','mol/m^3'],'MaxLinece':['s','mol/m^3'],
 'profiletimes':['s'],'profileN':['s','m','1','1','V','V','V','1'],'profileP':['s','m','1','1','V','V','V','1']}
for tag,expected in units.items():
    for phase in (['inferred','configured','evaluated'] if tag=='eguard' else ['configured','evaluated']):
        a=expected.copy()
        if phase!='configured':
            for i in ([6,7,8] if tag=='eguard' else [10] if tag=='nglobal' else [7] if tag in ['profileN','profileP'] else []): a[i]=''
        value='['+', '.join(a)+']'
        check(tag+' '+phase,rows(T/f'units_{tag}_{phase}.csv')==[{'tag':tag,'phase':phase,'expected':value,'actual':value}])
markers=[
 'AXES_PHYSICAL_MESH_DOMAIN=1|numelem=120',
 'AXES_PHYSICAL_MESH_DOMAIN=2|numelem=60',
 'AXES_PHYSICAL_MESH_DOMAIN=3|numelem=120',
 'AXES_PARTICLE=pce1|Nel=320|Nord=1|Distribution=CubicRoot',
 'AXES_PARTICLE=pce2|Nel=320|Nord=1|Distribution=CubicRoot',
 'AXES_ACTUAL_MESH=mesh1|edges=300|vertices=301',
 'PREFLIGHT_SOLVE_BEGIN=0..240 seconds; NO full protocol or sweep',
 'ELECTROLYTE_THRESHOLD_EXPRESSION=0[mol/m^3]',
 'ELECTROLYTE_THRESHOLD_SI=0.0']
counts=dict.fromkeys(markers,0)
with (R/'run/batch_console.log').open(encoding='utf-8-sig') as f:
    for line in f:
        if line.strip() in counts:counts[line.strip()]+=1
for k,v in counts.items():check(k,v==1)
java=(R/'candidate/src/Normal240Candidate.java').read_text(encoding='utf-8-sig')
check('one textual runAll call',java.count('.runAll();')==1)
ps=(R/'candidate/PARENT_COMMAND.ps1').read_text(encoding='utf-8-sig')
check('STOP is parent no-rerun instruction','STOP. No rerun, cleanup fallback, policy toggle or additional solve. Preserve this output.' in ps)
g={D(r['time_s']):D(r['ce_min_all_mol_m3']) for r in rows(T/'electrolyte_guard.csv')}
mn={D(r['time_s']):D(r['ce_mol_m3']) for r in rows(T/'preflight_MinLine_ce.csv')}
check('MinLine and guard have same time set',g.keys()==mn.keys())
minline_delta=max(abs(v-mn[t]) for t,v in g.items())
check('MinLine matches coupling minimum within1e-9',minline_delta<=D('1e-9'))
post=read(S/'POST_WRITE_USER_RETURN.json'); value=post['value']
check('post-return provenance explicitly subsequent transcription','subsequent transcription' in post['source'] and 'not independent OS observation' in post['source'])
check('parent transcript does not claim to reconstruct truncated analyzer output','not reconstructed' in post['normalization'])
check('post-return binds final boundary', {k:value['boundary'][k] for k in ['bytes','sha256']}==identity(R/'parent/FINAL_BOUNDARY.json'))
boundary=read(R/'parent/FINAL_BOUNDARY.json')
check('post-write follows pre-write',value['snapshot_seconds']>=boundary['elapsed_seconds']==value['pre_write_seconds'])
check('final budgets and recording errors',value['snapshot_seconds']<=7200 and value['delivery_elapsed_seconds']<=300 and value['within_limits'] and value['record_errors']==[])
check('NoExit does not invent process rc',value['raw_host_rc'] is None and boundary['raw_host_rc'] is None and value['host_boundary']=='SCRIPT_FINAL_RECORD_NOT_PROCESS_EXIT')
main,supplement=read(ROOT/'ARCHIVE_AUDIT.json')
ret=read(ROOT/'USER_SUPPLIED_FINAL_RETURN.json')['completion']; out=json.loads(ret['output'])
check('supplied final supplement return rc0',ret['exit_code']==0 and ret['chunk_id']=='5d1af4' and out['status']=='SUPPLEMENT_VERIFIED')
check('final return supplement raw identity',all(out['supplement'][k]==supplement[k] for k in ['bytes','sha256']))
check('generation recipient stays null',out['recipient'] is None)
check('final snapshot is before tool return',out['scope']=='After supplement readback, before tool return')
pack=read(S/'PACKAGING_TOOL_RETURN.json')['completion']; pout=json.loads(pack['output'])
check('main package return rc and identity',pack['exit_code']==0 and pack['chunk_id']=='11faaa' and all(pout['zip'][k]==main[k] for k in ['bytes','sha256']))
check('main package native counts',pout['stored_count']==3340 and pout['profile_rows']==1609880 and pout['payloads']==8099)
check('package return creates no next approval',pout['new_execution_authorized'] is False)
result={
 'status':'PASS','checks':checks,'check_count':len(checks),
 'scope':'Independent recipient data checks, not functional tests or new native execution.',
 'minline_coupling_max_delta_mol_m3':str(minline_delta),
 'final_return_provenance':'Current user message transcribed by reviewer; sender host call not independently observed.',
 'parent_boundary':'User-console script final record, null outer PowerShell process rc; post-write user transcription.',
 'final_return_call_wall_seconds':ret['wall_time_seconds'],
 'final_return_snapshot_seconds':out['elapsed_seconds'],
 'native_post_write_seconds':value['snapshot_seconds'],
 'separate_collection_post_receipt_seconds':pout['post_receipt_snapshot_seconds']}
(ROOT/'SUPPLEMENTAL_AUDIT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'PASS','checks':len(checks),'minline_delta':str(minline_delta)},ensure_ascii=False))
