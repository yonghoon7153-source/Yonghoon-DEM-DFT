"""Verify pinned copies, rerun bounded arithmetic, and package this review. No DEM."""
from pathlib import Path, PurePosixPath
import hashlib, json, platform, re, subprocess, sys, zipfile
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def save(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')

verified = []
for manifest, folder in [('source_manifest.json', 'source'), ('upstream_manifest.json', 'upstream')]:
    data = json.loads((ROOT / manifest).read_text(encoding='utf-8'))
    for item in data['files']:
        if 'sha256' not in item:
            continue
        path = ROOT / folder / item['path']
        assert sha(path) == item['sha256'], str(path)
        if 'blob_sha' in item:
            contents = path.read_bytes()
            blob = hashlib.sha1(b'blob ' + str(len(contents)).encode() + b'\0' + contents).hexdigest()
            assert blob == item['blob_sha'], str(path)
        verified.append(str(path.relative_to(ROOT)))

commands = [[sys.executable, '-X', 'utf8', '-B', str(ROOT/'probes'/name)] for name in
            ['review_counterexamples.py', 'recheck_original_log.py', 'physics_arithmetic.py']]
commands[-1].extend(['--output', str(ROOT/'evidence/physics_arithmetic.json')])
commands.append(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', str(ROOT/'probes/design_arithmetic.ps1')])
runs=[]
for cmd in commands:
    result = subprocess.run(cmd, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace')
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip(), cmd
    parsed = json.loads(result.stdout)
    runs.append(dict(command=cmd, returncode=result.returncode, output_json=True, stderr=result.stderr))

report = ROOT/'codex_review_dem_unloading_prereg_20261011.md'
content=report.read_text(encoding='utf-8')
assert not re.search(r'[\u3040-\u30ff]', content), 'Unexpected Japanese text'
assert content.count('```') % 2 == 0, 'Unclosed code fence'
for i in range(1,11):
    assert f'UL-{i:02}' in content
save(ROOT/'evidence/reproduction_receipt.json', dict(
    no_simulation=True, no_production_edits=True, python=sys.version,
    python_executable=sys.executable, numpy=np.__version__, platform=platform.platform(),
    pinned_files_verified=len(verified), runs=runs,
    report_sha256=sha(report), report_lines=len(content.splitlines())))

manifest_path=ROOT/'review_bundle_manifest.json'
files=sorted(p for p in ROOT.rglob('*') if p.is_file() and p!=manifest_path and '__pycache__' not in p.parts)
entries=[dict(path=p.relative_to(ROOT).as_posix(), bytes=p.stat().st_size, sha256=sha(p)) for p in files]
save(manifest_path, dict(schema='read_only_review_bundle/v1', review='DEM unloading preregistration 2026-10-11',
    excludes=['review_bundle_manifest.json (self)'], files=entries))
archive=ROOT.parent/'codex_dem_unloading_prereg_review_20261011.zip'
with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for p in files+[manifest_path]:
        z.write(p, ROOT.name+'/'+p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(archive) as z:
    names=z.namelist()
    assert len(names)==len(set(names))
    assert z.testzip() is None
    for n in names:
        q=PurePosixPath(n)
        assert not q.is_absolute() and '..' not in q.parts
    expected={ROOT.name+'/'+e['path']:e['sha256'] for e in entries}
    expected[ROOT.name+'/'+manifest_path.name]=sha(manifest_path)
    assert set(names)==set(expected)
    for name, digest in expected.items():
        assert hashlib.sha256(z.read(name)).hexdigest()==digest
receipt=dict(zip=str(archive), bytes=archive.stat().st_size, sha256=sha(archive),
    entries=len(names), all_entry_hashes_verified=True, pinned_files_verified=len(verified),
    report_sha256=sha(report), no_simulation=True)
save(archive.with_suffix('.receipt.json'), receipt)
print(json.dumps(receipt, ensure_ascii=False, indent=2))
