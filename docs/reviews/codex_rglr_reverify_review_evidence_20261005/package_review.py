"""Package reviewer-created artifacts and verified source, never production state."""
from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
manifest=json.loads((R/'source_manifest.json').read_text(encoding='utf8'))
files={R/'source'/r['path'] for r in manifest['files']}
top=['codex_review_rglr_reverify_20261005.md','findings_review.json','environment.json',
     'source_manifest.json','compare_metadata.json','run_tests.py','run_probes.py','verify_source.py','record_environment.py','package_review.py']
files.update(R/n for n in top)
for d in ('probes','inputs','diffs'):
 files.update(p for p in (R/d).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
files.update(p for p in (R/'evidence').iterdir() if p.is_file())
# Exact current network-run fixture directories referred to by the evidence index.
for row in json.loads((R/'evidence/network_adversarial.json').read_text(encoding='utf8')):
 p=(R/row['path']).resolve()
 assert p.is_relative_to((R/'evidence').resolve())
 files.update(f for f in p.rglob('*') if f.is_file() and '__pycache__' not in f.parts)
rows=[dict(path=p.relative_to(R).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(files)]
pm=R/'package_manifest.json'
pm.write_text(json.dumps(dict(commit=manifest['commit'],files=rows,scope='review evidence only; not a production seal'),ensure_ascii=False,indent=2),encoding='utf8')
files.add(pm)
z=R.parent/'codex_rglr_reverify_review_20261005.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as out:
 for p in sorted(files):out.write(p,(Path(R.name)/p.relative_to(R)).as_posix())
with zipfile.ZipFile(z) as inp:
 assert inp.testzip() is None
 for r in rows:
  b=inp.read(R.name+'/'+r['path']);assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
receipt=dict(zip=z.name,bytes=z.stat().st_size,sha256=hashlib.sha256(z.read_bytes()).hexdigest(),
 commit=manifest['commit'],entries=len(files),manifest_sha256=hashlib.sha256(pm.read_bytes()).hexdigest(),verified_archive_entries=True)
rp=z.with_suffix('.receipt.json');rp.write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
