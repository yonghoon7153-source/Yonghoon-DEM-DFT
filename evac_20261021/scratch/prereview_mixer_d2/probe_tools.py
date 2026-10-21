#!/usr/bin/env python3
"""Probe D — do the repo deck checkers (HEAD scripts/mixer_deck_readback.py · scripts/mixer_deck_diff.py) cover D2 decks?

Generates decks with the HEAD generator CLI into decks/tools/, then runs the two checkers (python -I -B, read only) on pairs:
  readback --table E   D2 soft -> D2 x20 (gen1)            readback --table E   D2 soft -> D2 x20 (lab20261014)
  readback --table B   LC soft -> D2 gamma1 (gen1)          readback --table U   LC soft -> D2 gamma1 (gen1)
  readback --table E   LC soft lab -> LC x20 lab (old arm, new density generation)
  diff --allow E / B / U / A on the same pairs
Records rc + verdict lines.  usage: python3 -I -B probe_tools.py <repo_worktree>
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = sys.argv[1]
GEN = os.path.join(HERE, 'gen', 'mmd_HEAD.py')
RB = os.path.join(REPO, 'scripts', 'mixer_deck_readback.py')
DF = os.path.join(REPO, 'scripts', 'mixer_deck_diff.py')
OUT = os.path.join(HERE, 'decks', 'tools')
BASE = ['--n-total', '100000', '--cgf', '151.4', '--seed', '32452843', '--revolutions', '2']
GM1 = ['--gm-gamma', 'AM_P=1,AM_S=1', '--gm-gamma-wall', '0.0256', '--gm-bo-se', '0.21244']
GMU = ['--gm-gamma', 'AM_P=0.3,AM_S=0.3', '--gm-wall-ncm', '0.3', '--gm-bo-se', '0.21244']
ST20 = ['--stiffen-se', '20', '--hold-bo-pairwise']
DECKS = {
    'LC_soft_gen1': ['--arm', 'LC'],
    'LC_ref20_gen1': ['--arm', 'LC'] + ST20,
    'LC_soft_lab': ['--arm', 'LC', '--dens-gen', 'lab20261014'],
    'LC_ref20_lab': ['--arm', 'LC', '--dens-gen', 'lab20261014'] + ST20,
    'GM1_soft_gen1': GM1 + ['--dens-gen', 'gen1'],
    'GM1_ref20_gen1': GM1 + ['--dens-gen', 'gen1'] + ST20,
    'GM1_soft_lab': GM1 + ['--dens-gen', 'lab20261014'],
    'GM1_ref20_lab': GM1 + ['--dens-gen', 'lab20261014'] + ST20,
    'GMU_ref20_lab': GMU + ['--dens-gen', 'lab20261014'] + ST20,
}
env = dict(os.environ, OPENBLAS_NUM_THREADS='1')
res = dict(decks={}, readback=[], diff=[])
for name, args in DECKS.items():
    d = os.path.join(OUT, name)
    p = subprocess.run([sys.executable, '-I', '-B', GEN, '--out', d] + BASE + args, capture_output=True, text=True, env=env)
    res['decks'][name] = p.returncode
P = lambda n: os.path.join(OUT, n, 'in.mixer')
RBQ = [('E', 'GM1_soft_gen1', 'GM1_ref20_gen1'), ('E', 'GM1_soft_lab', 'GM1_ref20_lab'), ('E', 'LC_soft_lab', 'LC_ref20_lab'),
       ('E', 'LC_soft_gen1', 'LC_ref20_gen1'), ('B', 'LC_ref20_gen1', 'GM1_ref20_gen1'), ('U', 'LC_ref20_gen1', 'GM1_ref20_gen1'),
       ('B', 'LC_ref20_lab', 'GMU_ref20_lab')]
for kind, a, b in RBQ:
    js = os.path.join(OUT, f'rb_{kind}_{a}__{b}.json')
    p = subprocess.run([sys.executable, '-I', '-B', RB, '--table', kind, P(a), P(b), '--json', js], capture_output=True, text=True, env=env)
    fails = []
    try:
        J = json.load(open(js, encoding='utf-8'))
        for T in J.get('tables', []):
            fails += T.get('failures', [])[:3]
    except Exception as e:
        fails = [f'(no json: {e})']
    res['readback'].append(dict(kind=kind, old=a, new=b, rc=p.returncode, fails=fails[:3],
                                tail=(p.stdout + p.stderr).strip().splitlines()[-2:]))
DFQ = [('E', 'GM1_soft_gen1', 'GM1_ref20_gen1'), ('E', 'GM1_soft_lab', 'GM1_ref20_lab'), ('E', 'LC_soft_lab', 'LC_ref20_lab'),
       ('B', 'LC_ref20_gen1', 'GM1_ref20_gen1'), ('U', 'LC_ref20_gen1', 'GM1_ref20_gen1'), ('A', 'LC_ref20_gen1', 'GM1_ref20_gen1'),
       ('B', 'LC_ref20_lab', 'GMU_ref20_lab'), ('EB', 'LC_soft_lab', 'GMU_ref20_lab')]
for allow, a, b in DFQ:
    p = subprocess.run([sys.executable, '-I', '-B', DF, P(a), P(b), '--allow', allow], capture_output=True, text=True, env=env)
    res['diff'].append(dict(allow=allow, old=a, new=b, rc=p.returncode, tail=(p.stdout + p.stderr).strip().splitlines()[-3:]))
json.dump(res, open(os.path.join(HERE, 'probe_tools.json'), 'w'), ensure_ascii=False, indent=1)
print('decks rc', res['decks'])
for r in res['readback']:
    print('readback', r['kind'], r['old'], '->', r['new'], 'rc', r['rc'], '|', (r['fails'] or ['PASS'])[0][:160])
for r in res['diff']:
    print('diff', r['allow'], r['old'], '->', r['new'], 'rc', r['rc'], '|', ' / '.join(r['tail'])[:220])
