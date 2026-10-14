from pathlib import Path
import hashlib,json,zipfile,sys
R=Path(__file__).resolve().parent
out=R.parent/'codex_sup20_fix_reverify_20261014.zip'
def wide(p):return Path('\\\\?\\'+str(p.resolve())) if sys.platform=='win32' else p
paths=sorted(R/p.relative_to(wide(R)) for p in wide(R).rglob('*') if p.is_file() and p.relative_to(wide(R)).parts[0]!='tmp' and '__pycache__' not in p.relative_to(wide(R)).parts and p.suffix not in ('.pyc','.pyo') and p!=wide(R)/'MANIFEST.sha256.json')
source_manifest=json.loads((R/'source_manifest.json').read_text(encoding='utf8'))
missing=[e['path'] for e in source_manifest['files'] if R/'source'/e['path'] not in paths]
assert not missing,missing
entries=[dict(path=p.relative_to(R).as_posix(),bytes=wide(p).stat().st_size,sha256=hashlib.sha256(wide(p).read_bytes()).hexdigest()) for p in paths]
man=R/'MANIFEST.sha256.json';man.write_text(json.dumps(dict(schema='review_evidence_sha256/v1',pin='a9422d2e772f28417a6e0a5167aaab8d987bf27a',files=entries),ensure_ascii=False,indent=2),encoding='utf8')
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in paths+[man]:z.writestr('sup20_fix_reverify_20261014/'+p.relative_to(R).as_posix(),wide(p).read_bytes())
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
    for e in entries:
        b=z.read('sup20_fix_reverify_20261014/'+e['path']);assert hashlib.sha256(b).hexdigest()==e['sha256']
print(json.dumps(dict(file=str(out),entries=len(entries)+1,bytes=out.stat().st_size,sha256=hashlib.sha256(out.read_bytes()).hexdigest()),ensure_ascii=False))
