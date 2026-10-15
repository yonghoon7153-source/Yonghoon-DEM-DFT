"""Preserve the exact generated input fixtures in the review evidence directory."""
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / 'tmp/join_independent'
dst = ROOT / 'evidence/join_fixtures'
dst.mkdir(parents=True, exist_ok=True)
rows = []
for path in sorted(src.iterdir()):
    if path.is_file():
        target = dst / path.name
        shutil.copyfile(path, target)
        raw = target.read_bytes()
        rows.append({'path': str(target.relative_to(ROOT)), 'bytes': len(raw),
                     'sha256': hashlib.sha256(raw).hexdigest()})
(ROOT / 'evidence/join_fixture_manifest.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')
print('preserved', len(rows), 'fixtures')
