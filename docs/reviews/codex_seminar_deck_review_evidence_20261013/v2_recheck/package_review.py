"""Package read-only review outputs, excluding internal reviewer working notes."""
from pathlib import Path
import hashlib, json, zipfile
R=Path(__file__).resolve().parent
report=R/'codex_review_seminar_v2_recheck_20261013.md'
manifest=json.loads((R/'evidence/input_manifest.json').read_text(encoding='utf8'))
body=report.read_text(encoding='utf8')
for item in manifest['originals']:
    assert item['sha256'] in body,(item['name'],'missing hash')
    original=Path('C:/Users/Administrator/Downloads')/item['name']
    assert hashlib.sha256(original.read_bytes()).hexdigest()==item['sha256'],('original changed',item['name'])
assert '\ufffd' not in body
assert len(list((R/'renders').glob('page-*.png')))==19
paths=sorted(p for p in R.rglob('*') if p.is_file() and p.relative_to(R).parts[0]!='notes' and p.name!='PACKAGE_MANIFEST.json')
inventory=[{'path':p.relative_to(R).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]
(R/'PACKAGE_MANIFEST.json').write_text(json.dumps({'review_report':report.name,'files':inventory,'note':'This inventory excludes itself. Input files are preserved unchanged. Internal working notes are not delivery verdicts and are omitted.'},ensure_ascii=False,indent=2),encoding='utf8')
target=R.parent/'codex_seminar_v2_recheck_20261013.zip'
assert not target.exists(),f'Refusing overwrite: {target}'
with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in paths+[R/'PACKAGE_MANIFEST.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(target) as z:
    assert z.testzip() is None
    for row in inventory:assert hashlib.sha256(z.read(row['path'])).hexdigest()==row['sha256']
print(json.dumps({'zip':str(target),'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'file_count':len(paths)+1,'report_bytes':report.stat().st_size,'originals_unchanged':True},ensure_ascii=False,indent=2))
