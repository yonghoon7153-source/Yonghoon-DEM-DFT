"""Exact comparison of Codex tree.json with NUL-separated ls-tree dumps.

usage: python3 -I tree_cmp.py <extracted_root> <repro_dir>
"""
import json
import sys
from pathlib import Path


def load(p):
    rows = {}
    for rec in Path(p).read_bytes().split(b'\0'):
        if not rec:
            continue
        meta, path = rec.split(b'\t', 1)
        mode, typ, sha, size = meta.decode().split()
        rows[path.decode('utf-8')] = dict(mode=mode, type=typ, sha=sha)
    return rows


def main():
    root, repro = Path(sys.argv[1]), Path(sys.argv[2])
    pin = load(repro / 'lstree_34713ac96.z')
    head = load(repro / 'lstree_HEAD.z')
    tj = json.loads((root / 'evidence/tree.json').read_text(encoding='utf-8'))
    tb = {e['path']: e for e in tj['tree'] if e['type'] == 'blob'}
    res = dict(
        tree_json_blobs=len(tb), pin_blobs=len(pin),
        same_paths=set(tb) == set(pin),
        sha_diff=sum(tb[p]['sha'] != pin[p]['sha'] for p in tb if p in pin),
        mode_diff=sum(tb[p]['mode'] != pin[p]['mode'] for p in tb if p in pin),
        only_tree_json=sorted(set(tb) - set(pin))[:5],
        only_pin=sorted(set(pin) - set(tb))[:5],
        tree_entries_total=len(tj['tree']),
        types={t: sum(1 for e in tj['tree'] if e['type'] == t) for t in sorted({e['type'] for e in tj['tree']})},
        truncated=tj.get('truncated'), tree_sha=tj.get('sha'))
    m = json.loads((root / 'source_manifest.json').read_text(encoding='utf-8'))['files']
    res['current_manifest_files'] = len(m)
    res['current_manifest_match_pin'] = sum(pin.get(r['path'], {}).get('sha') == r['git_blob'] for r in m)
    res['current_manifest_differ_HEAD'] = [r['path'] for r in m if head.get(r['path'], {}).get('sha') != r['git_blob']]
    print(json.dumps(res, ensure_ascii=False, indent=1))
    (repro / 'tree_cmp.json').write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
