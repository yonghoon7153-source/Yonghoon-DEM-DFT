"""Independent post-fix probes: actual consumers and launcher merge, no campaigns."""
import sys,json,copy,shutil,tempfile,contextlib,io,hashlib,math,random,csv
from pathlib import Path
from fractions import Fraction as F
R=Path(__file__).resolve().parents[1];S=R/'source';E=R/'evidence'
sys.path[:0]=[str(S/'scripts'),str(S/'webapp')]
import lhs_design_dataset as L, pipeline_service as PS, tau_flux as TF
import run_network_194_parallel as NP
from dem_analysis_core import diag_von_mises, VM_RESOLVE_K
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
prior=json.loads((E/'network_adversarial.json').read_text(encoding='utf8'))
base=next(x for x in prior if x['name']=='positive');origin=R/base['path']
root=Path(tempfile.mkdtemp(prefix='handover_provenance_',dir=E));cd=root/'lhs00_000';shutil.copytree(origin,cd)
fm=json.loads((cd/'full_metrics.json').read_text(encoding='utf8'));dual=json.loads((cd/'network_conductivity_dual.json').read_text(encoding='utf8'))
wv=dict(stop_after='network',source='independent_synthetic_batch',status={'lhs00_000':dict(status='done',network_run_id=fm['network_run_id'])},
 rows={'lhs00_000':{k:('' if v is None else str(v)) for k,v in fm.items()}})
tau=[]
for label in ('baseline','dual_band_only','dual_sigma0_only','atom_input_mutation','dual_sigma_ratio_only','run_id_mismatch'):
 shutil.copyfile(origin/'atoms.csv',cd/'atoms.csv');save(cd/'full_metrics.json',fm);d=copy.deepcopy(dual)
 if label=='dual_band_only':
  for mode in ('hertzian','physics'):d[mode]['boundary_rule']='L1'
 if label=='dual_sigma0_only':
  for mode in ('hertzian','physics'):
   d[mode]['sigma_grain_S_cm']*=2;d[mode]['sigma_full_mScm']=round(1000*d[mode]['sigma_grain_S_cm']*d[mode]['sigma_full'],6)
 if label=='dual_sigma_ratio_only':
  d['hertzian']['sigma_full']*=4
 if label=='atom_input_mutation':
  with (cd/'atoms.csv').open('a',encoding='utf8') as f:f.write('\n')
 if label=='run_id_mismatch':
  mf=copy.deepcopy(fm);mf['network_run_id']='other';save(cd/'full_metrics.json',mf)
 save(cd/'network_conductivity_dual.json',d)
 try:
  out=L.load_tau_results(root,wv)
  row=out['cases']['lhs00_000']['cells'];accepted=True;why=''
 except L.FillRefusal as ex:row={};accepted=False;why=str(ex)
 stop_ok,stop_why=PS.network_stop_verdict(str(cd),fm['network_run_id'])
 tau.append(dict(name=label,accepted=accepted,why=why,stop_contract_ok=stop_ok,stop_contract_why=stop_why,
                 cells={k:row.get(k) for k in ('f_ion_hertz','tau2_ion_hertz','ion_net_status_hertz','ion_sigma0_mScm')}))
if not all(x['accepted'] for x in tau[:3]):print(json.dumps(tau,ensure_ascii=False,indent=2))
assert tau[0]['accepted'] and tau[1]['accepted'] and tau[2]['accepted']
assert not any(x['accepted'] for x in tau[3:])
# Minimal successful worker records, built through actual writer, for actual merge.
rr=Path(tempfile.mkdtemp(prefix='launcher_merge_',dir=E));case='lhs00_000'
cs=dict(name='lhs',harvest_dir='sealed_harvest',cohort='sealed_cohort',expect_n=1,union='',design='')
q=dict(case=case,cohort='lhs',contacts=100,est_mem_mb=150.5)
h0=NP.code_hashes();gh='11fcf91e8a1f4837b83892b7e4a81125eaeee4e5'
man=dict(schema=NP.SCHEMA,git=dict(sha=gh,short=gh[:9]),code_hashes=h0,plan=dict(cohorts=[cs],queue=[q]),lanes=20,network_lock='per-case')
save(rr/'manifest.json',man);cdir=NP.case_dir(rr,case)
status=dict(schema=NP.LWB.SCHEMA,stop_after='network',harvest_dir=cs['harvest_dir'],cohort=cs['cohort'],
 cases={case:dict(case=case,status='done',network_run_id='r1')},runs=[dict(git_sha=gh,dirty=False)])
NP.LWB.write_outputs(cdir/'out',status,{case:dict(case=case)})
save(cdir/'worker.json',dict(attempts=[dict(rc=0,outcome='done',run=1,attempt=1)]))
save(rr/'runs/run_001.json',dict(code_changed_during_run=[]))
# Current bytes changed between attempts at same git commit; h0=h1 inside retry.
real_hash=NP.code_hashes;changed=copy.deepcopy(h0);changed['scripts/network_conductivity.py']='0'*64
NP.code_hashes=lambda:changed
try:
 rc=NP.merge(rr,out=lambda *a,**k:None);report=NP.read_json(rr/'merged/merge_report.json')
finally:NP.code_hashes=real_hash
assert rc==0 and report['code_changed_since_launch']==['scripts/network_conductivity.py'] and not report['mixed_generation']
# Exercise actual retry dispatch and actual merge: mock only OS lock/worker/git environmental answers.
# A same-commit dirty retry occurs between attempts; h0==h1 so change-during-run list is empty.
status['cases'][case]['status']='failed';NP.LWB.write_outputs(cdir/'out',status,{case:dict(case=case)})
originals={k:getattr(NP,k) for k in ('_guard_posix','root_lock','git_info','purge_pyc','run_queue','code_hashes','meminfo')}
called=[]
def synthetic_worker(*a,**kw):
 called.append(True);status['cases'][case]['status']='done';status['runs'].append(dict(git_sha=gh,dirty=True))
 NP.LWB.write_outputs(cdir/'out',status,{case:dict(case=case)})
 return dict(outcomes={'done':1},wall_h=0,max_concurrent=1,budget_events=0,backfills=0,events=0,interrupted=False)
NP._guard_posix=lambda:None;NP.root_lock=lambda *a:contextlib.nullcontext();NP.purge_pyc=lambda *a,**k:0
NP.git_info=lambda:dict(sha=gh,short=gh[:9],dirty=True,porcelain=[' M scripts/network_conductivity.py'])
NP.code_hashes=lambda:changed;NP.run_queue=synthetic_worker;NP.meminfo=lambda:{'MemAvailable':8*2**30}
try:
 with contextlib.redirect_stdout(io.StringIO()) as buf:retry_rc=NP.cmd_retry(NP._parse(['retry','--root',str(rr)]))
 retry_log=buf.getvalue();retry_report=NP.read_json(rr/'merged/merge_report.json')
 retry_run=NP.read_json(rr/'runs/run_002.json')
finally:
 for k,v in originals.items():setattr(NP,k,v)
assert called and retry_rc==0 and retry_run['code_changed_during_run']==[] and retry_report['mixed_generation']==[]
lines=[];NP.print_followups(rr,man,out=lambda *a,**k:lines.append(' '.join(map(str,a))))
# Registration hashes independently recomputed.
import re
reg=(S/'docs/reviews/lhs_network_batch_registration_20261005.md').read_text(encoding='utf8')
regrows=re.findall(r'^\| `([^`]+)` \| `([a-f0-9]{64})` \|$',reg,re.M)
regchecks=[dict(path=p,expected=h,actual=hashlib.sha256((S/p).read_bytes()).hexdigest()) for p,h in regrows]
assert len(regchecks)==19 and all(x['expected']==x['actual'] for x in regchecks)
# VM: exact rational arithmetic on represented floats, independent of selftest cases.
rng=random.Random(170005);samples=5000;stable=kept=0;max_rel=max_exact_rad=0.;bound_breaches=0;bit_diffs=0
for i in range(samples):
 p=math.ldexp(rng.uniform(.5,1),rng.randint(-250,250))*(1 if rng.random()<.5 else -1)
 eps=10**rng.uniform(-14,0);t=(p,p*(1+eps),p*(1-eps*.37))
 x,y,z=map(F,t);exact=((x-y)**2+(y-z)**2+(z-x)**2)/2
 got,st=diag_von_mises(*t);want=math.sqrt(float(exact))
 rel=abs(float(got)-want)/want if want else 0
 if st:stable+=1
 else:
  kept+=1;max_rel=max(max_rel,rel);bound_breaches+=int(rel>1/(VM_RESOLVE_K-1)+1e-15)
  a,b,c=t;old=math.sqrt(a*a+b*b+c*c-a*b-b*c-a*c);bit_diffs+=int(float(got).hex()!=old.hex())
res=dict(tau=tau,launcher=dict(merge_rc=rc,report=report,retry_rc=retry_rc,retry_worker_called=bool(called),retry_report=retry_report,retry_run=retry_run,retry_log=retry_log,followups=lines,path=str(rr.relative_to(R))),
 registration=dict(files=len(regchecks),match=True,checks=regchecks),
 vm=dict(samples=samples,stable=stable,legacy=kept,max_retained_vm_relative_error=max_rel,bound_breaches=bound_breaches,
         comparison_multiplication_vs_pow_bit_differences=bit_diffs),fixture=str(root.relative_to(R)))
save(E/'new_probes.json',res)
print(json.dumps({k:v for k,v in res.items() if k not in ('registration','launcher')},ensure_ascii=False,indent=2))
print(json.dumps(dict(registration_match=True,merge_rc=rc,code_changed=report['code_changed_since_launch'],mixed=report['mixed_generation']),ensure_ascii=False))
