import pathlib,zipfile,hashlib,json
R=pathlib.Path(__file__).resolve().parent
out=R.parent/'codex_lhs_release_final_review_20261001.zip'
manifest=json.loads((R/'evidence/snapshot_manifest.json').read_text(encoding='utf-8'))
for x in manifest:
    b=(R/'snapshot'/x['path']).read_bytes()
    assert hashlib.sha256(b).hexdigest()==x['sha256'], x['path']
    assert x['match'],x['path']
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(R.rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts:
            z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
    entries=len(z.namelist())
sha=hashlib.sha256(out.read_bytes()).hexdigest()
print(json.dumps(dict(zip=str(out),entries=entries,bytes=out.stat().st_size,sha256=sha),indent=2))
