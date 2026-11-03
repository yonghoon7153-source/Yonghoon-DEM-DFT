from pathlib import Path
import hashlib, json

root = Path(__file__).resolve().parent
meta = json.loads((root / 'intake_metadata.json').read_text(encoding='utf-8'))
rows = []
for rec in meta['remote_files']:
    p = root / 'source/repo' / rec['path']
    b = p.read_bytes()
    blob = hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
    rows.append(dict(path=rec['path'], expected_git_blob=rec['sha'], actual_git_blob=blob,
                     sha256=hashlib.sha256(b).hexdigest(), bytes=len(b), match=blob==rec['sha']))
result = dict(reviewed_candidate_pin=meta['reviewed_candidate_pin'],
              checked=len(rows), passed=sum(x['match'] for x in rows), rows=rows)
(root / 'snapshot_verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='rows'}, ensure_ascii=False))
assert all(x['match'] for x in rows)
