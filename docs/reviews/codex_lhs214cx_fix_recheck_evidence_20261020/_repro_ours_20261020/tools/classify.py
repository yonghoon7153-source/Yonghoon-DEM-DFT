"""Classify bundle members and verify Codex manifests against our git trees.

usage: python3 -I classify.py <extracted_root> <repro_dir> <repo_root>
reads  <repro_dir>/lstree_{HEAD,34713ac96,685c2bbdb}.txt (git ls-tree -r -l)
writes <repro_dir>/classify.json  (per member: sha256, bytes, blob, matches)
prints a summary.
"""
import hashlib
import json
import os
import sys
from pathlib import Path


def blob(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()


def load_tree(p):
    rows = {}
    for line in Path(p).read_text(encoding='utf-8').splitlines():
        meta, path = line.split('\t', 1)
        mode, typ, sha, size = meta.split()
        rows[path] = dict(mode=mode, type=typ, sha=sha, size=size)
    return rows


def main():
    root = Path(sys.argv[1])
    repro = Path(sys.argv[2])
    repo = Path(sys.argv[3])
    trees = {k: load_tree(repro / f'lstree_{k}.txt') for k in ('HEAD', '34713ac96', '685c2bbdb')}
    by_blob_head = {}
    for p, r in trees['HEAD'].items():
        by_blob_head.setdefault(r['sha'], []).append(p)
    members = []
    for dp, dn, fn in os.walk(root):
        for n in fn:
            fp = Path(dp) / n
            rel = fp.relative_to(root).as_posix()
            b = fp.read_bytes()
            members.append(dict(path=rel, bytes=len(b), sha256=hashlib.sha256(b).hexdigest(),
                                blob=blob(b)))
    members.sort(key=lambda m: m['path'])
    for m in members:
        rel = m['path']
        m['head_same_blob_paths'] = by_blob_head.get(m['blob'], [])
        for pre, pin in (('source_review/', '34713ac96'), ('baseline_review/', '685c2bbdb')):
            if rel.startswith(pre):
                sub = rel[len(pre):]
                for k in ('HEAD', '34713ac96', '685c2bbdb'):
                    r = trees[k].get(sub)
                    m[f'same_as_{k}:{sub}'] = bool(r and r['sha'] == m['blob'])
    # tree.json vs git ls-tree 34713ac96
    tj = json.loads((root / 'evidence/tree.json').read_text(encoding='utf-8'))
    tblobs = {e['path']: e for e in tj['tree'] if e['type'] == 'blob'}
    gl = {p: r for p, r in trees['34713ac96'].items() if r['type'] == 'blob'}
    tree_cmp = dict(tree_json_sha=tj.get('sha'), truncated=tj.get('truncated'),
                    tree_json_blobs=len(tblobs), git_blobs=len(gl),
                    same_paths=set(tblobs) == set(gl),
                    sha_mismatch=sum(1 for p in tblobs if p in gl and tblobs[p]['sha'] != gl[p]['sha']),
                    mode_mismatch=sum(1 for p in tblobs if p in gl and tblobs[p]['mode'] != gl[p]['mode']),
                    non_blob_entries=sum(1 for e in tj['tree'] if e['type'] != 'blob'))
    # source manifests vs pin blobs
    man = {}
    for label, f, pin in (('current', 'source_manifest.json', '34713ac96'),
                          ('baseline', 'baseline_review/source_manifest.json', '685c2bbdb')):
        d = json.loads((root / f).read_text(encoding='utf-8'))
        files = d['files']
        ok = sum(1 for r in files if trees[pin].get(r['path'], {}).get('sha') == r['git_blob'])
        head_ok = sum(1 for r in files if trees['HEAD'].get(r['path'], {}).get('sha') == r['git_blob'])
        diff_head = [r['path'] for r in files if trees['HEAD'].get(r['path'], {}).get('sha') != r['git_blob']]
        man[label] = dict(pin=d.get('pin'), base=d.get('base'), files=len(files), match_pin=ok,
                          match_HEAD=head_ok, differ_from_HEAD=diff_head)
    # commit.json
    cj = json.loads((root / 'evidence/commit.json').read_text(encoding='utf-8'))
    commit_info = dict(sha=cj.get('sha'), parents=[p.get('sha') for p in cj.get('parents', [])],
                       n_files=len(cj.get('files', [])),
                       stats=cj.get('stats'))
    out = dict(members=members, tree_cmp=tree_cmp, manifests=man, commit=commit_info)
    (repro / 'classify.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
    print('members', len(members))
    print('tree_cmp', json.dumps(tree_cmp))
    for k, v in man.items():
        print('manifest', k, json.dumps({kk: (vv if kk != 'differ_from_HEAD' else vv[:20]) for kk, vv in v.items()}, ensure_ascii=False))
    print('commit', json.dumps(commit_info))
    for m in members:
        flags = {k: v for k, v in m.items() if k.startswith('same_as_')}
        if m['path'].startswith(('source_review/', 'baseline_review/')) or m['head_same_blob_paths']:
            print(f"{m['bytes']:>9} {m['path']}  head_paths={m['head_same_blob_paths'][:3]}{'...' if len(m['head_same_blob_paths'])>3 else ''} {flags}")


if __name__ == '__main__':
    main()
