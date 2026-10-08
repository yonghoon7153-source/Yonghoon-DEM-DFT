"""Independent read-only recomputation of supplied WSL pilot evidence (no job launch)."""
from pathlib import Path, PurePosixPath
from collections import Counter
import json, hashlib, sys
R=Path(__file__).resolve().parents[1]; S=R/'source'; E=R/'evidence'
sys.path[:0]=[str(S/'scripts'),str(S/'webapp')]
import run_network_194_parallel as rn
import g2_network_reread as rr
J=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda x:sha(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())
sub=R/'submitted'; pilot=sub/'g2pre_pilot_839dbac6b_1007_2224'; received=sub/'g2rr5_839dbac6b_1007_2224'
man=J(pilot/'manifest.json'); audit=J(pilot/'seal_audit.json'); reread=J(pilot/'reread.json')
result={'checks':[],'case_details':[]}
def check(name,ok,detail=None):
    result['checks'].append(dict(name=name,ok=bool(ok),detail=detail))
hashes={p:sha((S/p).read_bytes()) for p in rn.CODE_FILES}
check('32 code bytes equal manifest', hashes==man['code_hashes'],len(hashes))
check('seal code_fp independent recompute', rn.code_fp(hashes)==man['seal']['code_fp'],rn.code_fp(hashes))
for p in received.glob('*.rc'):check('received rc '+p.stem,p.read_text().strip()=='0',p.read_text().strip())
mainroot=PurePosixPath(man['repo_root']); logs=pilot/'import_obs/log'; by={}; observed=set(); heads=[]
for st in sorted(logs.glob('*.start.json')):
    tok=st.name.removesuffix('.start.json'); sj=J(st); fp=logs/(tok+'.txt'); lines=fp.read_text().splitlines(); h=json.loads(lines[0]); mods=lines[1:]
    check('receipt pair '+tok,sj['proc']==tok==h['proc'] and sj['pid']==h['pid'] and sj['identity']==h['identity'] and h['n']==len(mods) and h['complete'] is True)
    ident=h['identity']; k=(ident['case'],ident['run_no'],ident['attempt']); main=str(PurePosixPath(h['main']).relative_to(mainroot))
    check('run identity '+tok,ident['run_id']==man['import_obs_run_id'])
    by.setdefault(k,Counter())[('worker' if main=='scripts/lhs_webapp_batch.py' else main)]+=1
    observed.update(str(PurePosixPath(m).relative_to(mainroot)) for m in mods)
    heads.append(h)
check('15 distinct pairs',len(heads)==15,len(heads))
eligible={p for p in observed if p.endswith('.py') and p.startswith(('scripts/','webapp/')) and p not in rn.IMPORT_OBS_HARNESS}
check('observed module subset',eligible<=set(rn.CODE_FILES),dict(n=len(eligible),outside=sorted(eligible-set(rn.CODE_FILES))))
for e in man['plan']['queue']:
    case=e['case']; cd=pilot/'cases'/case; st=J(cd/'out/status.json'); rec=st['cases'][case]; worker=J(cd/'worker.json'); a=worker['attempts'][0]
    check('record sha '+case,canon(rec)==a['seal']['record_sha'],canon(rec))
    check('attempt stage snapshot '+case,a['stage_plan']==rn.stage_plan_of(rec))
    k=(case,str(a['run']),str(a['attempt'])); expectations=Counter({'worker':1})
    # Independently map literal app stage labels for this observed path; do not call stage_expectations.
    mapping={'Parse':'scripts/parse_liggghts.py','Bimodal Contact Analysis':'scripts/analyze_contacts_bimodal.py','Contact Analysis':'scripts/analyze_contacts.py','Coverage Physics vs Hertzian':'scripts/coverage_physics_vs_hertzian.py','Network Solver (both modes)':'scripts/network_conductivity.py'}
    for stage in rec['stages']:
        if stage['step'] in mapping:expectations[mapping[stage['step']]]+=1
    seen=by[k];check('actual stage inventory '+case,expectations==seen,dict(expected=dict(expectations),observed=dict(seen)))
    binding=audit['import_observation']['stage_binding']['attempts']['|'.join(k)]
    check('audit counts match raw receipts '+case,binding['expected']==dict(expectations) and binding['observed']==dict(seen))
    result['case_details'].append(dict(case=case,raw_sha=rec['sha'],record_sha=canon(rec),stages=rec['stages'],process_count=sum(seen.values())))
check('no failed reread leaves',all(x['ok'] is True for x in reread['meta']) and all(x['ok'] is True for c in reread['cases'] for x in c['checks']))
expected={(x['case'],x['cohort']) for x in man['plan']['queue']}
check('fresh detailed contract',not rr.launcher_detail_problems(reread,expected),rr.launcher_detail_problems(reread,expected))
old=J(received/'old_reread.json');check('old detailed contract',not rr.launcher_detail_problems(old,expected),rr.launcher_detail_problems(old,expected))
oa=J(received/'old_audit.json');check('old three fallback plans',len(oa['import_observation']['stage_binding']['attempts'])==3 and all(x['plan_source'].startswith('out/status.json') for x in oa['import_observation']['stage_binding']['attempts'].values()))
check('fresh three snapshot plans',len(audit['import_observation']['stage_binding']['attempts'])==3 and all(x['plan_source'].startswith('worker.json') for x in audit['import_observation']['stage_binding']['attempts'].values()))
result['module_inventory']=sorted(eligible);result['passed']=sum(x['ok'] for x in result['checks']);result['total']=len(result['checks'])
(E/'submitted_verify.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(dict(passed=result['passed'],total=result['total'],failed=[x for x in result['checks'] if not x['ok']]),ensure_ascii=False))
sys.exit(result['passed']!=result['total'])
