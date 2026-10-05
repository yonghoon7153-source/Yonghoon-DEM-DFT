"""Copy only blob-verified unchanged files into independent review snapshot."""
import hashlib,json,shutil
from pathlib import Path
R=Path(__file__).resolve().parent; OLD=R.parent/'rglr_reverify_20261005'
m=json.loads((OLD/'source_manifest.json').read_text(encoding='utf8'));c=json.loads((R/'compare_metadata.json').read_text(encoding='utf8'))
assert c['status']=='ahead' and len(c['files'])<300 and c['base']==m['commit']
changed={x['filename'] for x in c['files']};copied=[]
for row in m['files']:
 p=row['path']
 if p in changed:continue
 src=OLD/'source'/p;b=src.read_bytes();blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 assert blob==row['git_blob'] and row['verified'],p
 dst=R/'source'/p;dst.parent.mkdir(parents=True,exist_ok=True);assert not dst.exists();shutil.copyfile(src,dst);copied.append(dict(path=p,sha=blob))
(R/'unchanged_files.json').write_text(json.dumps(dict(base=c['base'],pin=c['head'],files=copied),indent=2),encoding='utf8')
for d in ('inputs','evidence','probes','diffs'):(R/d).mkdir(exist_ok=True)
shutil.copyfile(OLD/'codex_review_rglr_reverify_20261005.md',R/'inputs/prior_review.md')
shutil.copyfile(Path('C:/Users/Administrator/Downloads/codex_rglr2_reverify_request_20261005.md'),R/'inputs/request_user.md')
for p in (OLD/'probes').iterdir():
 if p.is_file():shutil.copyfile(p,R/'probes'/p.name)
shutil.copyfile(OLD/'run_tests.py',R/'run_tests.py')
shutil.copyfile(OLD/'run_probes.py',R/'run_probes.py')
print(dict(copied=len(copied)))
