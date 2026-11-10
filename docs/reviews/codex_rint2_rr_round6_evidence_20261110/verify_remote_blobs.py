import json, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
inv = json.loads((ROOT / 'input_verification.json').read_text(encoding='utf-8'))
trees = json.loads((ROOT / 'remote_tree_manifest.json').read_text(encoding='utf-8'))
flat = {}
for prefix, record in trees.items():
    assert record['truncated'] is False, prefix
    for entry in record['tree']:
        p = (prefix + '/' if prefix else '') + entry['path']
        if entry['type'] == 'blob':
            flat[p] = entry
rows = []
for row in inv['blobs']:
    p = row['path']
    data = (ROOT / 'package/repo' / p).read_bytes()
    sha = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    remote = flat.get(p)
    rows.append({'path': p, 'local_blob': sha, 'remote_blob': remote['sha'] if remote else None,
                 'equal': bool(remote and remote['sha'] == sha and remote.get('size') == len(data))})
base = json.loads((ROOT / 'remote_root_1.json').read_text(encoding='utf-8'))
head = json.loads((ROOT / 'remote_root_0.json').read_text(encoding='utf-8'))
# Saved root files may be decoded API records or tool envelopes.
def unwrap(d):
    if 'tree' in d: return d
    d = d.get('value', d)
    d = d.get('structuredContent', d)
    return json.loads(d['content']) if 'content' in d and isinstance(d['content'], str) else d
base, head = unwrap(base), unwrap(head)
subtrees = []
for p in ('scripts', 'webapp'):
    a = next(x['sha'] for x in base['tree'] if x['path'] == p)
    b = next(x['sha'] for x in head['tree'] if x['path'] == p)
    subtrees.append({'path': p, 'base': a, 'head': b, 'equal': a == b})
result = {'pin': inv['pin'], 'repo_files': len(rows), 'matched': sum(x['equal'] for x in rows),
          'mismatches': [x for x in rows if not x['equal']], 'subtrees': subtrees, 'files': rows}
(ROOT / 'remote_blob_verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k != 'files'}, ensure_ascii=False, indent=2))
raise SystemExit(0 if all(x['equal'] for x in rows + subtrees) else 1)
