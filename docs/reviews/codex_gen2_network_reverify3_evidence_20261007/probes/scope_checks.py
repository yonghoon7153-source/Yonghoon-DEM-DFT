"""Independent positive/negative contract checks. No batch or S3 campaign."""
from pathlib import Path
import sys,os,json,copy,contextlib,io,hashlib,subprocess,math,shutil
from unittest.mock import patch
R=Path(__file__).resolve().parents[1];S=R/'source';D=R/'evidence/scope_checks';D.mkdir(exist_ok=True)
sys.path[:0]=[str(S/'scripts'),str(S/'webapp')]
import run_network_194_parallel as rn,network_conductivity as nc,tau_flux as tf
import seal_s3_prerun as sp,run_s3_psi as s3
PIN='0801d4ceb540f5a5813761b20a5e0f304ed80a03'
def quiet(fn,*a,**kw):
 with contextlib.redirect_stdout(io.StringIO()):return fn(*a,**kw)
def jload(p):return json.loads(Path(p).read_text(encoding='utf8'))
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
out={}
base=jload(R/'evidence/seal_paths/baseline/manifest.json');out['current']=rn.launch_eligibility(base)
rows=[]
for key in rn.NEW_FORMAT_KEYS+('git','code_hashes','plan'):
 for how in ['delete','null']:
  m=copy.deepcopy(base)
  if how=='delete':m.pop(key,None)
  else:m[key]=None
  try:r=rn.launch_eligibility(m);rows.append(dict(key=key,how=how,kind=r['kind'],problems=r['problems']))
  except Exception as ex:rows.append(dict(key=key,how=how,exception=str(ex)))
out['deletions']=rows
hist=jload(S/'docs/data/lhs_network194_11fcf91e8/manifest.json');out['historical']=rn.launch_eligibility(hist)
hcases=[]
for name in ['baseline','git_changed','hash_changed','new_marker_added']:
 m=copy.deepcopy(hist)
 if name=='git_changed':m['git']['sha']='f'*40
 if name=='hash_changed':m['code_hashes']['scripts/network_conductivity.py']='0'*64
 if name=='new_marker_added':m['input_digest']=None
 hcases.append(dict(label=name,result=rn.launch_eligibility(m)))
out['history_mutants']=hcases
hd=D/'history';hd.mkdir(exist_ok=True);save(hd/'manifest.json',hist)
hc=[]
for extra in [[],['--historical']]:
 p=subprocess.run([sys.executable,str(S/'scripts/run_network_194_parallel.py'),'audit','--root',str(hd),*extra],capture_output=True,text=True,encoding='utf8')
 hc.append(dict(args=extra,rc=p.returncode,tail=p.stdout.splitlines()[-6:],stderr=p.stderr))
out['history_cli']=hc
out['fingerprint']=dict(code_fp=rn.code_fp(rn.code_hashes()),files=len(rn.CODE_FILES),closure=rn.code_dependency_closure(S),census=rn.lazy_import_census(S))
A={i:dict(type=1,x=0.,y=0.,z=float(i),radius=1.) for i in range(21)}
C=[dict(id1=i,id2=i+1,contact_area=.01,delta=.05) for i in range(20)]
temps=[]
for T,ea in [(None,None),(-40,None),(0,None),(25,None),(60,None),(120,None),(60,.29),(60,.46)]:
 du={cm:quiet(nc._run_all_networks,A,C,[1],[],{1:'SE'},1.,20.,10.,10.,None,contact_mode=cm,temp_c=T,ea_ion_ev=ea) for cm in ['hertzian','physics']}
 con=tf.network_generation_contract(du)
 temps.append(dict(T=T,ea=ea,generation=con['generation'],problems=con['problems'],sigma0=du['hertzian']['sigma_grain_S_cm'],q=du['hertzian']['sigma_full']))
out['temperature_positive']=temps
out['s3_dependencies']=sp.numeric_dependency_problems(S)
manifest={x['path']:x for x in jload(R/'source_manifest.json')}
bundle=dict(git_sha=PIN,numeric_modules_dirty=[],modules={m:manifest['scripts/'+m]['sha256'] for m in sp.NUMERIC_MODULES})
checks=[]
# Git adapter returns already SHA1-verified connector blobs; solver, dependency checker and hash comparisons are real.
with patch.object(sp,'blob_sha256',lambda sha,path:manifest.get(path,{}).get('sha256') if sha==PIN else None),patch.object(sp,'code_bundle',lambda:copy.deepcopy(bundle)):
 for label in ['valid_six','old_four','wrong_lens_hash','wrong_se_hash','missing_sha']:
  b=copy.deepcopy(bundle)
  if label=='old_four':
   for k in ['lens_geometry.py','se_material.py']:b['modules'].pop(k)
  if label=='wrong_lens_hash':b['modules']['lens_geometry.py']='0'*64
  if label=='wrong_se_hash':b['modules']['se_material.py']='0'*64
  if label=='missing_sha':b['git_sha']=''
  why=s3.verify_code_bundle(dict(code_bundle=b,generation_git_sha=PIN));checks.append(dict(label=label,accepted=not why,why=why))
out['s3_bundle_adapter_checks']=checks
# A six-particle raw fixture from author's test, not a real bed or a campaign.
txt=(S/'scripts/seal_s3_prerun.py').read_text(encoding='utf8');a=txt.index("    _pr = td / 'pos'");b=txt.index('    #  TSV 는',a)
import textwrap,tempfile
# The author's fixture creates directories exclusively; give every replay its own workspace.
ns=dict(td=Path(tempfile.mkdtemp(prefix='raw_',dir=D)),_math=math);exec(compile(textwrap.dedent(txt[a:b]),'<pinned raw fixture>','exec'),ns)
from audit_constriction_deleted import case_networks
res,prov=quiet(s3.run_case,ns['_cs'],str(ns['_cs']),('ionic','electronic','thermal'),case_networks,nc.solve_network)
out['s3_synthetic_raw']=res
out['s3_scope']='synthetic run_case only; no registered S3 cohort, no new seal. Git proof adapter uses independently verified pinned blobs.'
save(R/'evidence/scope_checks.json',out)
print(json.dumps(dict(current=out['current']['kind'],deletions=[(r['key'],r['how'],r.get('kind')) for r in rows],history=out['historical']['kind'],history_cli=[r['rc'] for r in hc],fingerprint=out['fingerprint']['code_fp'],closure=len(out['fingerprint']['closure']['files']),lazy=len(out['fingerprint']['census']['lazy']),unclassified=out['fingerprint']['census']['unclassified'],temperatures=temps,s3=checks,synthetic=res),ensure_ascii=False))
