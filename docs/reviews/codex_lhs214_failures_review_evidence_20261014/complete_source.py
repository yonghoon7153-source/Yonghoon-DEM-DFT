from pathlib import Path
import concurrent.futures, hashlib, json, urllib.request, urllib.parse
R=Path(__file__).resolve().parent
PIN='1087a9b2f4a93aa6a3b0debc698a14fffa13488d'
TREE=R.parent/'rint_g2_impl_review_20261014/evidence/tree.json'
t=json.loads(TREE.read_text(encoding='utf8'));assert not t.get('truncated')
es={e['path']:e for e in t['tree'] if e['type']=='blob'}
paths={p for p in es if
       (p.startswith('webapp/') and p.endswith(('.py','.html','.js','.json'))) or
       p in ['docs/reviews/findings.json','docs/reviews/claims.json'] or
       (p.startswith('docs/') and p.endswith('.md') and any(w in p.lower() for w in
        ['lhs_network_batch_registration','supp20','sup20','supr_','gen2_network','lhs130_harvest_contract','lhs_structure_descriptor','lhs_handover','lhs_release']))}
roots=[R/'source',R.parent/'supr_reverify_20261014/source',R.parent/'gen2_network_reverify7_20261012/source',R.parent/'sup20_fix_reverify_20261014/source',R.parent/'supp20_support_review_20261012/source']
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def get(p):
 e=es[p];b=None;reuse=False
 for root in roots:
  f=root/p
  if f.is_file():
   x=f.read_bytes()
   if blob(x)==e['sha']:b=x;reuse=True;break
 if b is None:
  url='https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/'+PIN+'/'+urllib.parse.quote(p)
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Read-only-review'}),timeout=60) as s:b=s.read()
 assert blob(b)==e['sha'] and len(b)==e['size'],p
 dest=R/'source'/p;dest.parent.mkdir(parents=True,exist_ok=True)
 if not dest.exists():dest.write_bytes(b)
 else:assert dest.read_bytes()==b,p
 return {'path':p,'sha':e['sha'],'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'reused':reuse}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:rows=list(pool.map(get,sorted(paths)))
mf=R/'source_manifest.json';m=json.loads(mf.read_text(encoding='utf8'));files={r['path']:r for r in m['files']+rows};m['files']=[files[p] for p in sorted(files)]
for f in (R/'source').rglob('*'):
 if f.is_file():
  p=f.relative_to(R/'source').as_posix();b=f.read_bytes()
  assert p in es and blob(b)==es[p]['sha'],p
  files[p]={'path':p,'sha':es[p]['sha'],'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
m['files']=[files[p] for p in sorted(files)]
mf.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'pin':PIN,'requested':len(rows),'total':len(files),'reused':sum(r['reused'] for r in rows)},indent=2))
