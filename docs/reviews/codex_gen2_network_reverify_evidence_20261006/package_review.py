"""Package reviewer artifacts without temp folders or original Git state."""
from pathlib import Path
import json,hashlib,zipfile,sys,platform,importlib.metadata
R=Path(__file__).resolve().parent
env=dict(python=sys.version,platform=platform.platform(),pin='165d0cf61a3e15367a3d1bf68e8f98178b70c25c',packages={})
for p in ('numpy','scipy','networkx','flask','pandas'):
 try:env['packages'][p]=importlib.metadata.version(p)
 except importlib.metadata.PackageNotFoundError:env['packages'][p]='unavailable'
(R/'evidence/environment.json').write_text(json.dumps(env,indent=2),encoding='utf8')
files=[]
for top in ('source','probes','evidence'):
 files.extend(p for p in (R/top).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
for name in ('source_manifest.json','README.md','run_tests.py','verify_evidence.py','verify_bundle.py','package_review.py','codex_review_gen2_network_reverify_20261006.md'):
 files.append(R/name)
rows=[dict(path=p.relative_to(R).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(files)]
mp=R/'bundle_manifest.json';mp.write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf8');files.append(mp)
zp=R.parent/'codex_gen2_network_reverify_20261006.zip'
with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(files):z.write(p,arcname=R.name+'/'+p.relative_to(R).as_posix())
with zipfile.ZipFile(zp) as z:
 assert z.testzip() is None
 for row in rows:
  b=z.read(R.name+'/'+row['path']);assert hashlib.sha256(b).hexdigest()==row['sha256']
att=dict(zip=str(zp),bytes=zp.stat().st_size,sha256=hashlib.sha256(zp.read_bytes()).hexdigest(),entries=len(files),crc_and_hashes='PASS')
(R.parent/'codex_gen2_network_reverify_20261006_receipt.json').write_text(json.dumps(att,indent=2),encoding='utf8')
print(json.dumps(att))
