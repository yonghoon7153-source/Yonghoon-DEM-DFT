#!/usr/bin/env python3
"""Materialize Part B inputs from local git objects (read-only on the repo).

W = rint2rev_repro work folder.  X = untouched Codex mini bundle (reference hashes only).
1. part_b/evidence (Codex copy in the work folder) -> part_b/evidence_codex_copy (fresh dir for our runs).
2. part_b/baseline/early/source/scripts/rint_iface_join.py  <- git show dcb97f1ed:scripts/rint_iface_join.py
   part_b/baseline/early/tmp/join_independent/<30>       <- source/docs/reviews/codex_rint_g2_impl_fix_recheck_evidence_20261015/evidence/join_fixtures/
   every file checked against part_b/baseline/MANIFEST.json sha256.
3. oldsrc_2b9efa253/source: the 8 modules Codex's 179/324 run imported (its .imports.json) at 2b9efa253 + 7 data files.
4. oldtest_2b9efa253/source/scripts/test_rint_g2_join.py <- git show 2b9efa253:scripts/test_rint_g2_join.py
"""
import hashlib, json, os, shutil, subprocess, sys

REPO = '/home/user/Yonghoon-DEM-DFT'
W, X, REPORT = sys.argv[1], sys.argv[2], sys.argv[3]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def gshow(rev, path):
    r = subprocess.run(['git', '-C', REPO, 'show', f'{rev}:{path}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if r.returncode:
        raise SystemExit(f'git show {rev}:{path} failed: {r.stderr.decode()[:200]}')
    return r.stdout


def put(dst, data):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, 'wb') as f:
        f.write(data)


rep = {'steps': []}
pb = os.path.join(W, 'part_b')
ev, evc = os.path.join(pb, 'evidence'), os.path.join(pb, 'evidence_codex_copy')
if os.path.isdir(ev) and not os.path.exists(evc):
    os.rename(ev, evc)
    rep['steps'].append('renamed part_b/evidence -> part_b/evidence_codex_copy')

man = json.load(open(os.path.join(X, 'part_b/baseline/MANIFEST.json'), encoding='utf-8'))
fix_dir = os.path.join(W, 'source/docs/reviews/codex_rint_g2_impl_fix_recheck_evidence_20261015/evidence/join_fixtures')
rows = []
for f in man['files']:
    p, want = f['path'], f['sha256']
    dst = os.path.join(pb, 'baseline', p)
    if p == 'early/source/scripts/rint_iface_join.py':
        data = gshow('dcb97f1ed', 'scripts/rint_iface_join.py'); src = 'git dcb97f1ed:scripts/rint_iface_join.py'
        put(dst, data)
    elif p.startswith('early/tmp/join_independent/'):
        name = p.rsplit('/', 1)[1]
        data = open(os.path.join(fix_dir, name), 'rb').read(); src = 'pin source join_fixtures/' + name
        put(dst, data)
    else:
        data = open(dst, 'rb').read(); src = 'codex bundle (already present)'
        if p == 'old_join/scripts/rint_iface_join.py':
            g = gshow('2b9efa253', 'scripts/rint_iface_join.py')
            src += ' ; git 2b9efa253 sha=' + sha(g) + (' (same)' if g == data else ' (DIFF)')
    rows.append({'path': p, 'want': want, 'got': sha(data), 'ok': sha(data) == want, 'from': src})
rep['baseline_manifest'] = {'n': len(rows), 'ok': sum(r['ok'] for r in rows), 'rows': rows}

imp = json.load(open(os.path.join(X, 'part_b/evidence/test_rint_join_q7_recheck_20261020_test_rint_g2_join.py_lf_adapter.imports.json'), encoding='utf-8'))
old_root = os.path.join(W, 'oldsrc_2b9efa253', 'source')
orow = []
for rel, want in sorted(imp.items()):
    data = gshow('2b9efa253', rel); put(os.path.join(old_root, rel), data)
    orow.append({'path': rel, 'want_codex_import_sha': want, 'got': sha(data), 'ok': sha(data) == want})
DATA = ['docs/data/heckel_sweep_scaffolds/LOOSE_am_scaffold.csv', 'docs/data/real14_am_scaffold.csv',
        'docs/data/real14_reference_20260928/atom_2060000.liggghts.gz',
        'docs/data/real14_reference_20260928/contact_2060000.liggghts.gz',
        'docs/data/case15_corner_20261001/case15_am_scaffold.csv',
        'docs/data/case15_corner_20261001/atom_v4_1710000.liggghts.gz',
        'docs/data/case15_corner_20261001/contact_v4_1710000.liggghts.gz']
for rel in DATA:
    data = gshow('2b9efa253', rel); put(os.path.join(old_root, rel), data)
    cur = open(os.path.join(W, 'source', rel), 'rb').read()
    orow.append({'path': rel, 'got': sha(data), 'same_as_pin_source': data == cur, 'ok': data == cur})
rep['oldsrc_2b9efa253'] = {'n': len(orow), 'ok': sum(r['ok'] for r in orow), 'rows': orow}

t = gshow('2b9efa253', 'scripts/test_rint_g2_join.py')
put(os.path.join(W, 'oldtest_2b9efa253', 'source', 'scripts', 'test_rint_g2_join.py'), t)
rep['oldtest_2b9efa253'] = {'path': 'scripts/test_rint_g2_join.py', 'sha256': sha(t), 'bytes': len(t)}

json.dump(rep, open(REPORT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('baseline', rep['baseline_manifest']['n'], 'ok', rep['baseline_manifest']['ok'])
print('oldsrc', rep['oldsrc_2b9efa253']['n'], 'ok', rep['oldsrc_2b9efa253']['ok'])
print('oldtest sha', rep['oldtest_2b9efa253']['sha256'])
for r in rows:
    if not r['ok'] or 'old_join' in r['path']:
        print(r)
for r in orow:
    if not r['ok']:
        print('BAD', r)
