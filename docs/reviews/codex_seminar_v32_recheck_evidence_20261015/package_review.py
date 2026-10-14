"""Package review evidence only; do not edit any input artifacts."""
from pathlib import Path
import hashlib, json, zipfile
R=Path(__file__).resolve().parent
report=R/'codex_review_seminar_v32_recheck_20261015.md'
body=report.read_text(encoding='utf8')
assert not [ord(x) for x in body if ord(x)<32 and x not in '\n\r\t']
assert all(f'Q{i}' in body for i in range(1,9))
assert all(f'SEMV32-0{i}' in body for i in range(1,5))
assert 'PowerPoint' in body and '새 P1' in body
paths=sorted(p for p in R.rglob('*') if p.is_file() and p.name!='REVIEW_MANIFEST.sha256' and '__pycache__' not in p.parts and p.suffix!='.base64')
manifest=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(R).as_posix()+'\n' for p in paths)
(R/'REVIEW_MANIFEST.sha256').write_text(manifest,encoding='utf8')
paths.append(R/'REVIEW_MANIFEST.sha256')
out=R.parent/'codex_seminar_v32_recheck_20261015.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in paths: z.write(p,arcname=R.name+'/'+p.relative_to(R).as_posix())
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
    for line in manifest.splitlines():
        expected,name=line.split('  ',1)
        assert hashlib.sha256(z.read(R.name+'/'+name)).hexdigest()==expected, name
print(json.dumps({'zip':str(out),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'files':len(paths),'report_bytes':report.stat().st_size,'report_sha256':hashlib.sha256(report.read_bytes()).hexdigest(),'manifest_verified':len(paths)-1},ensure_ascii=True,indent=2))
