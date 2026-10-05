"""Verify fetched snapshot against independently returned Git blob identities."""
import hashlib,json,platform,sys
from pathlib import Path
R=Path(__file__).resolve().parent; S=R/'source'
expect={}
for name,field in [('source_fetch_root.json','git_blob'),('evidence_g4/acquisition_manifest.json','git_blob_sha1'),('evidence_g23/fetched_dependencies.json','sha')]:
 d=json.loads((R/name).read_text(encoding='utf-8'))
 for rec in d.get('files',[]):
  path=rec['path'].replace('\\','/')
  sha=rec.get(field)
  if sha and (S/path).is_file():
   if path in expect and expect[path]!=sha: raise RuntimeError('conflicting blob metadata '+path)
   expect[path]=sha
rows=[]
for p in sorted(S.rglob('*')):
 if not p.is_file(): continue
 rel=p.relative_to(S).as_posix(); b=p.read_bytes()
 actual=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 rows.append({'path':rel,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob_actual':actual,'git_blob_expected':expect.get(rel),'verified':actual==expect.get(rel)})
out={'repository':'yonghoon7153-source/Yonghoon-DEM-DFT','commit':'30c8205c5efb3873ae6fa856881fa184bd041d4d',
 'python':sys.version,'platform':platform.platform(),'files':rows,
 'missing_binary_fixtures':['docs/data/real14_reference_20260928/atom_2060000.liggghts.gz','docs/data/real14_reference_20260928/contact_2060000.liggghts.gz'],
 'notes':['Not a complete Git checkout. No checkout/fetch/commit commands used.','findings.json returned empty content; no empty placeholder retained.']}
(R/'source_manifest.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
bad=[r for r in rows if not r['verified']]
print(json.dumps({'source_files':len(rows),'verified':len(rows)-len(bad),'unverified':bad},ensure_ascii=False,indent=2))
raise SystemExit(bool(bad))
