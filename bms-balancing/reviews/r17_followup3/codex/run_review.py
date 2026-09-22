"""Reviewer command capture; fixed target, synthetic tests only, no target edits."""
import datetime, hashlib, importlib.metadata, json, os, pathlib, shutil, subprocess, sys, tempfile, time
sys.stdout.reconfigure(encoding='utf-8')
HERE=pathlib.Path(__file__).resolve().parent
WORK=HERE.parents[1]
REPO=WORK/'work/r17-followup3-head'; ROOT=REPO/'bms-balancing'
PY=WORK/'work/r17-venv/Scripts/python.exe'
EXPECTED='e834b01e4066c5e78c06b6ed1f77878e5a27a481'
def git(*args):
 return subprocess.check_output(['git','-c','http.sslBackend=openssl','-C',str(REPO),*args]).decode('utf-8').strip()
def dump(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert git('rev-parse','HEAD')==EXPECTED
mode=sys.argv[1]
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
env.pop('PYTEST_ADDOPTS',None)
if mode=='identity':
 files=['CLAUDE.md',*[str(p.relative_to(REPO)).replace('\\','/') for p in ROOT.rglob('*.py') if 'reviews/r17_followup' not in p.as_posix()]]
 docs=['bms-balancing/reviews/R17_FOLLOWUP2_RESPONSE.md','bms-balancing/WORKING_STATE.md']
 rec=dict(head=EXPECTED,bms_fix=git('rev-parse','7f09804'),tree=git('rev-parse','HEAD^{tree}'),
  status=git('status','--porcelain'),bms_diff_after_fix=git('diff','--name-status','7f09804','HEAD','--','bms-balancing'),
  utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,
  packages={p:importlib.metadata.version(p) for p in ('numpy','scipy','pandas','openpyxl','pytest')},
  files=[dict(path=p,sha256=hashlib.sha256((REPO/p).read_bytes()).hexdigest(),bytes=(REPO/p).stat().st_size) for p in sorted(set(files+docs))])
 dump(HERE/'IDENTITY.json',rec)
 (HERE/'code.diff').write_bytes(subprocess.check_output(['git','-c','http.sslBackend=openssl','-C',str(REPO),'diff','a4c311eff898615932ae6f333bbb26b605abf762','HEAD','--','bms-balancing/*.py','bms-balancing/*.sh']))
 old=WORK/'outputs/r17_followup2_a4c311ef'
 for script in ('repro_followup2.py','repro_producer_reader.py'):
  p=HERE/script
  if p.exists():assert p.read_bytes()==(old/script).read_bytes()
  else:shutil.copyfile(old/script,p)
 print(json.dumps({k:rec[k] for k in ('head','bms_fix','bms_diff_after_fix','status')},ensure_ascii=True));sys.exit(0)
if mode in ('focused','full'):
 temp=tempfile.mkdtemp(prefix='r17f3pt_');env['PYTEST_DEBUG_TEMPROOT']=temp
 files=['tests/test_r17_followup2.py'] if mode=='focused' else ['tests/']
 cmd=[str(PY),'-m','pytest',*files,'-q','-p','no:cacheprovider','--junitxml='+str(HERE/(mode+'.xml'))]
elif mode=='old-repros':cmd=[str(PY),str(HERE/'repro_followup2.py'),'--target',str(ROOT)]
elif mode=='producer':cmd=[str(PY),str(HERE/'repro_producer_reader.py'),'--target',str(ROOT)]
elif mode=='schema':cmd=[str(PY),'scripts/check_u14.py','--new','out','--schema-only']
elif mode=='legacy':cmd=[str(PY),'scripts/check_u14.py','--new','out/archive/legacy_r6_u14','--schema-only']
else:raise ValueError(mode)
t=time.monotonic()
try:
 r=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,timeout=1800)
 stdout,stderr,rc=r.stdout,r.stderr,r.returncode
except subprocess.TimeoutExpired as e:stdout,stderr,rc=e.stdout or b'',e.stderr or b'',None
(HERE/(mode+'.stdout.bin')).write_bytes(stdout);(HERE/(mode+'.stderr.bin')).write_bytes(stderr)
meta=dict(command=cmd,cwd=str(ROOT),rc=rc,seconds=time.monotonic()-t,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 env_overrides={k:env.get(k) for k in ('PYTHONUTF8','PYTHONIOENCODING','PYTHONDONTWRITEBYTECODE','OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','PYTEST_DEBUG_TEMPROOT')})
dump(HERE/(mode+'.json'),meta)
print(json.dumps(meta,ensure_ascii=True));print(stdout.decode('utf-8','replace')[-1600:]);print(stderr.decode('utf-8','replace')[-1200:])
sys.exit(rc if rc is not None else 124)
