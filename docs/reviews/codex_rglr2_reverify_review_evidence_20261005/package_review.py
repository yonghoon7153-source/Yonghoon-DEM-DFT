"""Package reviewer-created artifacts and verified source, never production state."""
from pathlib import Path
import hashlib
import json
import zipfile

R = Path(__file__).resolve().parent
manifest = json.loads((R / 'source_manifest.json').read_text(encoding='utf8'))
assert all(row['verified'] for row in manifest['files'])
files = {R / 'source' / row['path'] for row in manifest['files']}
top = ['README.md', 'codex_review_rglr2_reverify_20261005.md', 'findings_review.json',
       'environment.json', 'source_manifest.json', 'compare_metadata.json',
       'acquisition.json', 'unchanged_files.json', 'prepare_snapshot.py',
       'run_tests.py', 'run_probes.py', 'run_host_smoke.py', 'verify_snapshot.py',
       'record_environment.py', 'package_review.py', 'verify_delivery.py']
files.update(R / name for name in top)

def add_tree(p):
    p = p.resolve()
    assert p.is_relative_to(R)
    files.update(f for f in p.rglob('*')
                 if f.is_file() and '__pycache__' not in f.parts)

for d in ('probes', 'inputs', 'diffs'):
    add_tree(R / d)
files.update(p for p in (R / 'evidence').iterdir() if p.is_file())
for row in json.loads((R / 'evidence/network_adversarial.json').read_text(encoding='utf8')):
    add_tree(R / row['path'])
new = json.loads((R / 'evidence/new_probes.json').read_text(encoding='utf8'))
add_tree(R / new['fixture'])
add_tree(R / new['launcher']['path'])
add_tree(R / 'evidence/host_smoke')
for p in (R / 'evidence').glob('rgl08_replay_*'):
    if p.is_dir():
        add_tree(p)
rows = [dict(path=p.relative_to(R).as_posix(), bytes=p.stat().st_size,
             sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(files)]
pm = R / 'package_manifest.json'
pm.write_text(json.dumps(dict(commit=manifest['commit'], files=rows,
              scope='review evidence only; not a production seal'),
              ensure_ascii=False, indent=2), encoding='utf8')
files.add(pm)
z = R.parent / 'codex_rglr2_reverify_review_20261005.zip'
with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as out:
    for p in sorted(files):
        out.write(p, (Path(R.name) / p.relative_to(R)).as_posix())
with zipfile.ZipFile(z) as inp:
    assert inp.testzip() is None
    assert len(inp.namelist()) == len(set(inp.namelist())) == len(files)
    for row in rows:
        b = inp.read(R.name + '/' + row['path'])
        assert len(b) == row['bytes'] and hashlib.sha256(b).hexdigest() == row['sha256']
receipt = dict(zip=z.name, bytes=z.stat().st_size,
               sha256=hashlib.sha256(z.read_bytes()).hexdigest(),
               commit=manifest['commit'], entries=len(files),
               manifest_sha256=hashlib.sha256(pm.read_bytes()).hexdigest(),
               verified_archive_entries=True)
z.with_suffix('.receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf8')
print(json.dumps(receipt, ensure_ascii=False, indent=2))
