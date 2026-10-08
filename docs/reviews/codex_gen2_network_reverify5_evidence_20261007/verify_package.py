from pathlib import Path
import hashlib,json,sys,importlib,platform
R=Path(__file__).resolve().parent
rows=json.loads((R/'source_manifest.json').read_text(encoding='utf8'))
problems=[]
for x in rows:
    p=R/'source'/x['path'];b=p.read_bytes()
    git=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    if git!=x['sha'] or hashlib.sha256(b).hexdigest()!=x['sha256'] or len(b)!=x['bytes']:problems.append(x['path'])
expected={x['path'] for x in rows};extras=[p.relative_to(R/'source').as_posix() for p in (R/'source').rglob('*') if p.is_file() and p.relative_to(R/'source').as_posix() not in expected]
out=dict(verified=len(rows),problems=problems,extra_files=extras)
(R/'evidence/source_final_verification.json').write_text(json.dumps(out,indent=2),encoding='utf8')
assert not problems and not extras,out
sys.path[:0]=[str(R.parent/'lhs_coverage_review_20260930/deps'),str(R.parent/'gen2_network_reverify3_20261007/deps')]
versions={}
from importlib.metadata import version
for m in ('numpy','scipy','networkx','Flask','matplotlib'):
    try:versions[m]=version(m)
    except Exception as e:versions[m]=str(e)
(R/'evidence/runtime.json').write_text(json.dumps(dict(python=sys.version,executable=sys.executable,platform=platform.platform(),packages=versions),indent=2),encoding='utf8')
print(json.dumps(out))
