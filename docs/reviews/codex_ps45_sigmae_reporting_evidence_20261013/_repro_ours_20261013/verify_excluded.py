"""Codex ps45 σ_e 보고 기준 검토 묶음 — 반입에서 뺄 사본이 우리 git blob 과 바이트 같은지 (읽기 전용).

python3 -I verify_excluded.py <묶음 폴더 (ps45_sigmae_review_20261013)> <리포 루트> <out.tsv>

· source/<경로>             ↔ git 46cd0bdb8:<경로>  (코드 핀 · source_manifest.json · evidence/extra_source_manifest.json)
· literature_cards/<경로>   ↔ git e739c9730:<경로>  (litdb 정본 핀)
· literature_figures/<경로> ↔ git e739c9730:<경로>
· evidence/network_conductivity_run0801.py ↔ git 0801d4ceb:scripts/network_conductivity.py
· code_tree.json / lit_tree.json ↔ git ls-tree -r <핀> (blob 경로 · SHA-1 전수)
· code_commit.json / lit_commit.json = GitHub API 커밋 응답 — sha 칸 = 핀
rc 0 = 전부 같음.
"""
import hashlib
import json
import os
import subprocess
import sys

CODE = '46cd0bdb872e7d6c85ca50ec4172e98377253130'
LIT = 'e739c9730f8758d2d61b2db22d940ee9a2440897'
RUN = '0801d4ceb540f5a5813761b20a5e0f304ed80a03'


def blob_sha1(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()


def git(repo, *a):
    return subprocess.run(['git', '-C', repo, *a], capture_output=True, check=True).stdout


def main():
    pkg, repo, out = sys.argv[1:4]
    rows, bad = [], []

    def one(rel_pkg, pin, git_path):
        b = open(os.path.join(pkg, rel_pkg), 'rb').read()
        try:
            want = git(repo, 'rev-parse', f'{pin}:{git_path}').decode().strip()
        except subprocess.CalledProcessError:
            want = 'MISSING'
        got = blob_sha1(b)
        ok = (got == want)
        rows.append((rel_pkg, len(b), hashlib.sha256(b).hexdigest(), f'{pin[:9]}:{git_path}', got,
                     'same' if ok else 'DIFF'))
        if not ok:
            bad.append(rel_pkg)

    for base, pin in (('source', CODE), ('literature_cards', LIT), ('literature_figures', LIT)):
        root = os.path.join(pkg, base)
        for r, ds, fs in os.walk(root):
            ds.sort()
            for f in sorted(fs):
                full = os.path.join(r, f)
                rel_in = os.path.relpath(full, root).replace(os.sep, '/')
                one(f'{base}/{rel_in}', pin, rel_in)
    one('evidence/network_conductivity_run0801.py', RUN, 'scripts/network_conductivity.py')

    # tree 응답 ↔ git ls-tree
    for name, pin in (('code_tree.json', CODE), ('lit_tree.json', LIT)):
        b = open(os.path.join(pkg, name), 'rb').read()
        tree = json.loads(b)
        api = {e['path']: e['sha'] for e in tree['tree'] if e['type'] == 'blob'}
        ls = {}
        for ln in git(repo, '-c', 'core.quotepath=false', 'ls-tree', '-r', pin).decode('utf-8').splitlines():
            meta, path = ln.split('\t', 1)
            mode, typ, sha = meta.split()
            if typ == 'blob':
                ls[path] = sha
        ok = (api == ls) and tree.get('sha') == pin and not tree.get('truncated')
        rows.append((name, len(b), hashlib.sha256(b).hexdigest(), f'git ls-tree -r {pin[:9]} ({len(ls)} blob)',
                     f'api {len(api)} blob', 'same' if ok else 'DIFF'))
        if not ok:
            only_api = sorted(set(api) - set(ls))[:5]
            only_git = sorted(set(ls) - set(api))[:5]
            diff = [p for p in api if p in ls and api[p] != ls[p]][:5]
            print(name, 'DIFF', only_api, only_git, diff)
            bad.append(name)
    for name, pin in (('code_commit.json', CODE), ('lit_commit.json', LIT)):
        b = open(os.path.join(pkg, name), 'rb').read()
        c = json.loads(b)
        ok = c.get('sha') == pin
        rows.append((name, len(b), hashlib.sha256(b).hexdigest(), f'git show {pin[:9]} (GitHub API 커밋 응답)',
                     f"sha {c.get('sha', '')[:9]}", 'same' if ok else 'DIFF'))
        if not ok:
            bad.append(name)

    with open(out, 'w', encoding='utf-8', newline='\n') as fo:
        fo.write('path_in_bundle\tbytes\tsha256\trestore_from\tgit_blob_sha1_or_note\tverdict\n')
        for r in rows:
            fo.write('\t'.join(str(x) for x in r) + '\n')
    print(f'rows {len(rows)} · DIFF {len(bad)}', bad[:10])
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
