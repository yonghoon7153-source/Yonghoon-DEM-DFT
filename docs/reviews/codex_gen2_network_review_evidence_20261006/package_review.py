"""Package only the local review directory; no source repair or Git operations."""
from pathlib import Path
import sys, os, json, hashlib, platform, importlib.metadata, zipfile
R=Path(__file__).resolve().parent
sys.stdout.reconfigure(encoding='utf8')
PIN='c13da95a3d1b583e853365a93d96d55285ad91a8'
env={'python':sys.version,'platform':platform.platform(),'review_pin':PIN,
     'packages':{},'runtime_note':'Existing bundled runtime and existing local SciPy dependency; no installation by this review.',
     'actions_not_run':['DEM simulation','MPM simulation','new 194 campaign','check_all.sh full suite','git mutations']}
for p in ('numpy','scipy','networkx','flask','pandas'):
    try:env['packages'][p]=importlib.metadata.version(p)
    except importlib.metadata.PackageNotFoundError:env['packages'][p]='not discoverable'
(R/'evidence/environment.json').write_text(json.dumps(env,ensure_ascii=False,indent=2),encoding='utf8')
from verify_bundle import blob
for row in json.loads((R/'source_manifest.json').read_text(encoding='utf8')):
    b=(R/'source'/row['path']).read_bytes()
    assert blob(b)==row['sha'],row['path']
    assert hashlib.sha256(b).hexdigest()==row['sha256'],row['path']
paths=sorted(p for p in R.rglob('*') if p.is_file() and '__pycache__' not in p.parts
             and p.name not in ('bundle_manifest.json','bundle_receipt.json') and p.suffix!='.pyc')
rows=[]
for p in paths:
    b=p.read_bytes();rows.append(dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
(R/'bundle_manifest.json').write_text(json.dumps(dict(review_pin=PIN,files=rows),ensure_ascii=False,indent=2),encoding='utf8')
from verify_bundle import main
main()
dest=R.parent/'codex_gen2_network_review_20261006.zip'
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in paths+[R/'bundle_manifest.json']:
        z.write(p,'gen2_network_review_20261006/'+p.relative_to(R).as_posix())
with zipfile.ZipFile(dest) as z:
    assert z.testzip() is None
    for row in rows:
        b=z.read('gen2_network_review_20261006/'+row['path'])
        assert hashlib.sha256(b).hexdigest()==row['sha256']
receipt=dict(zip=dest.name,bytes=dest.stat().st_size,sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),
             review_pin=PIN,files_in_zip=len(paths)+1,pinned_git_blobs=130,zip_crc_check='PASS',content_hash_check='PASS')
(R/'bundle_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
