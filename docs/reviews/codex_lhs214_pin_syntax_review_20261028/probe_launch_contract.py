"""Synthetic manifests, actual launch_eligibility and full receipt validators. No launch."""
from pathlib import Path
import sys,json,types,copy
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'repo/scripts'))
import run_network_194_parallel as N
import supp20_input_receipt as S
O=R/'independent';O.mkdir(exist_ok=True)
pin='35f0327377a4213774010a090df4d224e50d29e1'
def manifest(cohorts):
 plan=N.build_plan(cohorts,N.cohort_specs(types.SimpleNamespace()),(),'cost');h=N.code_hashes()
 return dict(schema=N.SCHEMA,launch_format=N.LAUNCH_FORMAT,plan=plan,input_digest=N.plan_input_digest(plan),code_hashes=h,code_dependency_closure=list(N.CODE_FILES),handover_code_hashes={p:N.sha256_file(N.ROOT/p) for p in N.HANDOVER_FILES},git=dict(sha=pin,short=pin[:9],dirty=False),observe_imports=True,import_obs_run_id='cd'*16,generation_probe=dict(generation='g2',problems=[]),**{N.GEN_KEY:'g2'},seal=dict(schema=N.LAUNCH_SEAL_SCHEMA,launch_format=N.LAUNCH_FORMAT,code_fp=N.code_fp(h),files=len(h),**{N.GEN_KEY:'g2'}))
ms=manifest(['lhss']);mp=manifest(['lhs','lhsx']);base=S.receipt();assert base['rc']==0,base
ps=O/'synthetic_supp/manifest.json';pp=O/'synthetic_primary/manifest.json';out=[]
ps.parent.mkdir(exist_ok=True);pp.parent.mkdir(exist_ok=True)
for name,vals in [('normal',(pin,pin)),('supp_LF',(pin+'\n',pin)),('primary_LF',(pin,pin+'\n')),('both_LF',(pin+'\n',pin+'\n')),('both_wrong_last',(pin[:-1]+'0',pin[:-1]+'0'))]:
 a,b=copy.deepcopy(ms),copy.deepcopy(mp);a['git']['sha'],b['git']['sha']=vals;ps.write_text(json.dumps(a),encoding='utf8');pp.write_text(json.dumps(b),encoding='utf8')
 for mode,approval in [('full',pin),('prefix7',pin[:7]),('none',None)]:
  v=S.receipt(manifest=ps,primary_manifest=pp,approved_sha=approval)
  failed=sorted(c['id'] for c in v['checks'] if not c['ok'])
  expected={'normal':[],'supp_LF':['F7','H1'] if approval else ['H1'],'primary_LF':['G7','H1'] if approval else ['H1'],'both_LF':['F7','G7'] if approval else [],'both_wrong_last':['F7','G7'] if mode=='full' else []}[name]
  assert failed==expected,(name,mode,failed,expected)
  out.append({'case':name,'approval':mode,'rc':v['rc'],'bad':failed,'expected':expected,'eligibility_supp':N.launch_eligibility(a),'eligibility_primary':N.launch_eligibility(b)})
ps.write_text(json.dumps(ms),encoding='utf8');pp.write_text(json.dumps(mp),encoding='utf8')
(O/'launch_contract_probe.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps([{k:v for k,v in x.items() if not k.startswith('eligibility')} for x in out],ensure_ascii=False,indent=2))
