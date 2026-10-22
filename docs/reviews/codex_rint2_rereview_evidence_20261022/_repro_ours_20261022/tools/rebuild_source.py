#!/usr/bin/env python3
"""Rebuild pinned source tree from local git objects (read-only on the repo).

For every entry in source_manifest.json: `git -C REPO show PIN:<path>` -> OUT/<path>,
then compare SHA256 and git blob id (sha1 of "blob <n>\0"+data) with the manifest.
No fetch / checkout / worktree. Paths are validated (no absolute, no '..').
"""
import hashlib, json, os, subprocess, sys
from pathlib import PurePosixPath

REPO = '/home/user/Yonghoon-DEM-DFT'
PIN = '0b3012460'
manifest_path, out_dir, report_path = sys.argv[1], sys.argv[2], sys.argv[3]

m = json.load(open(manifest_path, encoding='utf-8'))
assert m['pin'].startswith('0b3012460fb8e8b7d53484b0efe399e2dc506aec'), m['pin']
files = m['files']
out_root = os.path.realpath(out_dir)
os.makedirs(out_root, exist_ok=True)

ok = 0
bad = []
tot_bytes = 0
for ent in files:
    p = ent['path']
    pp = PurePosixPath(p)
    if pp.is_absolute() or '..' in pp.parts or p.startswith('-') or '\\' in p or '\0' in p:
        bad.append({'path': p, 'why': 'unsafe_path'}); continue
    dst = os.path.realpath(os.path.join(out_root, *pp.parts))
    if not dst.startswith(out_root + os.sep):
        bad.append({'path': p, 'why': 'escapes_out_root'}); continue
    r = subprocess.run(['git', '-C', REPO, 'show', f'{PIN}:{p}'],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if r.returncode != 0:
        bad.append({'path': p, 'why': 'git_show_failed', 'stderr': r.stderr.decode('utf-8', 'replace')[:300]}); continue
    data = r.stdout
    sha = hashlib.sha256(data).hexdigest()
    blob = hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, 'wb') as f:
        f.write(data)
    tot_bytes += len(data)
    probs = []
    if sha != ent['sha256']:
        probs.append('sha256')
    if blob != ent['git_blob']:
        probs.append('git_blob')
    if len(data) != ent.get('bytes', len(data)):
        probs.append('bytes')
    if probs:
        bad.append({'path': p, 'why': 'mismatch:' + ','.join(probs), 'sha256_ours': sha,
                    'sha256_codex': ent['sha256'], 'blob_ours': blob, 'blob_codex': ent['git_blob'],
                    'bytes_ours': len(data), 'bytes_codex': ent.get('bytes')})
    else:
        ok += 1

rep = {'pin': m['pin'], 'n_manifest': len(files), 'n_match': ok, 'n_bad': len(bad),
       'total_bytes_written': tot_bytes, 'bad': bad}
json.dump(rep, open(report_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f"manifest={len(files)} match={ok} bad={len(bad)} bytes={tot_bytes}")
for b in bad[:20]:
    print('BAD', b)
