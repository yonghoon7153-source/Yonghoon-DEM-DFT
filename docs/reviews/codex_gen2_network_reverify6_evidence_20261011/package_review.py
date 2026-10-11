from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
m=json.loads((R/'source_manifest.json').read_text(encoding='utf8'))
for e in m['files']:
    b=(R/'source'/e['path']).read_bytes()
    assert hashlib.sha256(b).hexdigest()==e['sha256'],e['path']
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['sha'],e['path']
files=[p for p in R.rglob('*') if p.is_file() and p.relative_to(R).parts[0]!='tmp' and '__pycache__' not in p.parts and not p.name.endswith('.pyc') and p.name!='PACKAGE_SHA256SUMS.json']
rows=[dict(path=p.relative_to(R).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(files)]
(R/'PACKAGE_SHA256SUMS.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
out=R.parent/'codex_gen2_network_reverify6_20261011.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in files+[R/'PACKAGE_SHA256SUMS.json']:z.write(p,R.name+'/'+p.relative_to(R).as_posix())
with zipfile.ZipFile(out) as z:assert z.testzip() is None
print(json.dumps(dict(path=str(out),bytes=out.stat().st_size,sha256=hashlib.sha256(out.read_bytes()).hexdigest(),source_verified=len(m['files']),files=len(files)+1),ensure_ascii=False))
