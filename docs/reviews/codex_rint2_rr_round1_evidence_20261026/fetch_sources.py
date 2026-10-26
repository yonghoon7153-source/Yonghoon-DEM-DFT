"""Pinned read-only source intake; no checkout or Git mutation."""
from pathlib import Path
import ast,sys,os,json,hashlib,concurrent.futures,urllib.request,urllib.parse
R=Path(__file__).resolve().parent;REPO='yonghoon7153-source/Yonghoon-DEM-DFT';PIN='9bec6b7646374daed0d3edbb9647f9f46d302750';BASE='0b3012460fb8e8b7d53484b0efe399e2dc506aec'
def lp(p):
 s=str(p.absolute())
 return Path('\\\\?\\'+s) if os.name=='nt' and not s.startswith('\\\\?\\') else p
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def get(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Pinned-review'}),timeout=60) as f:return f.read()
def save(p,b):
 p=lp(p);p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():assert p.read_bytes()==b,str(p)
 else:p.write_bytes(b)
def meta(name,url):
 p=R/'evidence'/name
 if not p.exists():save(p,get(url))
 return json.loads(p.read_text('utf8'))
trees={}
for side,sha in [('repo',PIN),('baseline',BASE)]:
 d=meta(side+'_tree.json',f'https://api.github.com/repos/{REPO}/git/trees/{sha}?recursive=1');assert not d.get('truncated');trees[side]={x['path']:x for x in d['tree'] if x['type']=='blob'}
checks=[]
for row in json.loads((R/'evidence/intake.json').read_text('utf8'))['files']:
 if not row['path'].startswith('repo/'):continue
 p=row['path'][5:];b=lp(R/row['path']).read_bytes();ok=p in trees['repo'] and blob(b)==trees['repo'][p]['sha'];checks.append(dict(path=p,same=ok,git_blob=trees['repo'].get(p,{}).get('sha')))
assert all(x['same'] for x in checks);save(R/'evidence/zip_pin_checks.json',json.dumps(checks,indent=2).encode());print('ZIP blob matches',len(checks),flush=True)
paths={p for p in trees['repo'] if p in ('AGENTS.md','CLAUDE.md') or p.endswith('/AGENTS.md')}
paths|={p for p in trees['repo'] if p.startswith('scripts/') and len(Path(p).parts)==2 and p.endswith('.py') and Path(p).name.startswith(('ca_','carbon_','rint_','step3_','ptfe_','test_ca_','test_carbon_','test_rint_','test_step3_','test_ptfe_'))}
paths|={x['path'] for x in checks if x['path'].startswith(('scripts/','webapp/'))}
paths|={'scripts/se_material.py','scripts/physical_constants.py','scripts/check_arm.py','scripts/payload_utils.py'}
cache_roots=[R/'repo',R/'baseline',R.parent/'rint2_rereview_20261022/source',R.parent/'rint2_review_20261021/source']
files=[]
def fetch(side,p):
 sha=PIN if side=='repo' else BASE;expected=trees[side][p]['sha'];b=None
 for root in cache_roots:
  q=lp(root/p)
  if q.is_file() and blob(q.read_bytes())==expected:b=q.read_bytes();break
 if b is None:b=get(f'https://raw.githubusercontent.com/{REPO}/{sha}/'+urllib.parse.quote(p))
 assert blob(b)==expected,p;save(R/side/p,b)
 return dict(side=side,path=p,git_blob=expected,sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
pending={(side,p) for side in trees for p in paths if p in trees[side]};seen=set()
while pending:
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:got=list(ex.map(lambda x:fetch(*x),sorted(pending)))
 files.extend(got);seen|=pending;more=set()
 for x in got:
  if not x['path'].endswith('.py'):continue
  try:tr=ast.parse(lp(R/x['side']/x['path']).read_bytes())
  except SyntaxError:continue
  for n in ast.walk(tr):
   names=[a.name for a in n.names] if isinstance(n,ast.Import) else [n.module] if isinstance(n,ast.ImportFrom) and n.module else []
   for name in names:
    candidate='scripts/'+name.split('.')[0]+'.py'
    if candidate in trees[x['side']]:more.add((x['side'],candidate))
 pending=more-seen
 print('Fetched source files',len(files),'next',len(pending),flush=True)
for ref,path in [('d1768cf0c','scripts/step3_sigma.py'),('49a1af626','scripts/step3_conv_cert.py'),('73c640dc2','scripts/carbon_junction.py')]:
 p=R/'historical'/ref/path
 if not p.exists():save(p,get(f'https://raw.githubusercontent.com/{REPO}/{ref}/{path}'))
save(R/'evidence/source_manifest.json',json.dumps(dict(pin=PIN,baseline=BASE,files=files),indent=2).encode());print('DONE',len(files),flush=True)
