"""Read receipts, recount checks; path translation only in a separate Windows test copy."""
from pathlib import Path
import sys,json,hashlib,collections,shutil,copy
R=Path(__file__).resolve().parents[1];S=R/'source';E=R/'evidence'
sys.path.insert(0,str(S/'scripts'))
import run_network_194_parallel as np194
load=lambda p:json.loads(p.read_text(encoding='utf8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
P=R/'submitted/g2pre_c3117438a_1007_1415/g2pre_pilot_c3117438a_1007_1415'
X=R/'submitted/g2pre_extra_c3117438a_1007_1415/g2pre_pilot_c3117438a_1007_1415'
m=load(P/'manifest.json');a=load(P/'seal_audit.json');rr=load(P/'reread.json')
o=dict(manifest_sha=sha(P/'manifest.json'),reread_manifest_sha=rr['manifest_sha256'],code_fp=np194.code_fp(np194.code_hashes()),
       code_mismatch=[p for p,h in m['code_hashes'].items() if sha(S/p)!=h],handover_mismatch=[p for p,h in m['handover_code_hashes'].items() if sha(S/p)!=h],
       hook_identical=(X/'import_obs/hook/sitecustomize.py').read_text(encoding='utf8')==np194.IMPORT_OBS_HOOK,
       audit_verdict_recount=dict(collections.Counter(x['verdict'] for x in a['cases'])),
       reread_checks_failed=[x for x in rr['meta'] if not x['ok']]+[x for c in rr['cases'] for x in c['checks'] if not x['ok']],
       reread_n_cases=len(rr['cases']))
assert o['manifest_sha']==o['reread_manifest_sha'] and not o['code_mismatch'] and o['hook_identical']
assert not o['reread_checks_failed'] and o['reread_n_cases']==3
origroot=m['repo_root'];newroot=str(S.resolve())
base=E/'receipt_path_translation';base.mkdir(exist_ok=True)
for w in X.glob('cases/*/worker.json'):
    dst=base/w.relative_to(X);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(w,dst)
ld=base/'import_obs/log';ld.mkdir(parents=True,exist_ok=True)
for f in (X/'import_obs/log').iterdir():
    (ld/f.name).write_text(f.read_text(encoding='utf8').replace(origroot,newroot.replace('\\','/')),encoding='utf8')
def inspect(root):
    obs=np194.import_observation(root/'import_obs',S);problems=np194.import_observation_problems(root,m,obs,a['cases'])
    return obs,problems
obs,problems=inspect(base)
o['receipt_counts']={k:obs[k] for k in ('n_processes','n_started','n_finalized','completed_attempts','observed','outside')};o['translated_problems']=problems
o['stage_census']={c:dict(collections.Counter(Path(p['main']).name for p in obs['processes'] if p['identity']['case']==c)) for c in sorted({p['identity']['case'] for p in obs['processes']})}
print('PATH_TRANSLATED_BASELINE',json.dumps(problems,ensure_ascii=False),flush=True)
assert not problems
mutants={}
for label in ('remove_helper_final','remove_helper_pair','remove_solver_pair','empty_final','wrong_run_id','failed_attempt_unfinalized'):
    root=E/('obs_'+label);shutil.copytree(base,root,dirs_exist_ok=True);logs=root/'import_obs/log'
    helper=next(p for p in obs['processes'] if p['role']=='other')
    solver=next(p for p in obs['processes'] if p['role']=='network_solver')
    if label=='remove_helper_final':(logs/(helper['proc']+'.txt')).unlink()
    if label in ('remove_helper_pair','remove_solver_pair'):
        p=helper if label=='remove_helper_pair' else solver
        for suffix in ('.txt','.start.json'):(logs/(p['proc']+suffix)).unlink()
    if label=='empty_final':(logs/(helper['proc']+'.txt')).write_text('',encoding='utf8')
    if label=='wrong_run_id':
        f=logs/(helper['proc']+'.start.json');j=load(f);j['identity']['run_id']='unrelated';f.write_text(json.dumps(j),encoding='utf8')
    if label=='failed_attempt_unfinalized':
        j=load(logs/(helper['proc']+'.start.json'));j.update(proc='999999-1234abcd',pid=999999);j['identity']['attempt']='0'
        (logs/'999999-1234abcd.start.json').write_text(json.dumps(j),encoding='utf8')
        wp=root/'cases'/j['identity']['case']/'worker.json';wj=load(wp);wj['attempts'].append(dict(attempt=0,run=1,outcome='failed'));wp.write_text(json.dumps(wj),encoding='utf8')
    oo,pp=inspect(root);mutants[label]=dict(problems=pp,n_started=oo['n_started'],n_finalized=oo['n_finalized'],outside=oo['outside'],unfinalized_noncompleted=oo['unfinalized_noncompleted'])
o['mutants']=mutants
(E/'submitted_evidence.json').write_text(json.dumps(o,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(o,ensure_ascii=False,indent=2))
