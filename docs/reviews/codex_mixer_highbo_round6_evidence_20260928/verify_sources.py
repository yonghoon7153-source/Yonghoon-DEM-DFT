"""Verify the exact read-only source mirror against Git blob IDs, no Git commands."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
meta = json.loads((ROOT / 'sources.json').read_text(encoding='utf-8'))
rows = []
for item in meta['files']:
    raw = (ROOT / item['path']).read_bytes()
    actual = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    rows.append({'path': item['path'], 'bytes': len(raw), 'git_blob_sha': actual,
                 'expected_blob_sha': item['blob_sha'], 'sha256': hashlib.sha256(raw).hexdigest(),
                 'matches': actual == item['blob_sha']})
result = {'pin': meta['pin'], 'checked': len(rows), 'matched': sum(x['matches'] for x in rows), 'files': rows}
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(0 if all(x['matches'] for x in rows) else 1)
