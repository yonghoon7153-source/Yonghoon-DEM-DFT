"""Read-only SHA-256 and Git blob verification of a delivered review bundle."""
from pathlib import Path
import hashlib
import json

R = Path(__file__).resolve().parent
bad = []
package = json.loads((R / 'package_manifest.json').read_text(encoding='utf8'))
for row in package['files']:
    p = (R / row['path']).resolve()
    if not p.is_relative_to(R) or not p.is_file():
        bad.append([row['path'], 'missing or unsafe'])
        continue
    b = p.read_bytes()
    if len(b) != row['bytes'] or hashlib.sha256(b).hexdigest() != row['sha256']:
        bad.append([row['path'], 'package mismatch'])
source = json.loads((R / 'source_manifest.json').read_text(encoding='utf8'))
for row in source['files']:
    b = (R / 'source' / row['path']).read_bytes()
    digest = hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
    if digest != row['expected']:
        bad.append([row['path'], 'Git blob mismatch'])
print(json.dumps({'package_files': len(package['files']),
                  'source_files': len(source['files']), 'bad': bad}, ensure_ascii=False))
raise SystemExit(bool(bad))
