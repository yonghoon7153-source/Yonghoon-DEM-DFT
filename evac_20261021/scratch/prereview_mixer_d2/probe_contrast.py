#!/usr/bin/env python3
"""Probe G — the D2 confirmation contrast (same rho world: uncoated AM gamma = rho vs coated AM gamma = 1) as deck pairs.

(1) which CED entries differ between the two decks (read from the printed decks)
(2) can scripts/mixer_deck_diff.py (HEAD, read only) certify the pair under any existing allowlist (A · B · U · E · EB)?
(3) SE-SE ceiling bound in the lab generation (D3 design §1-1 quotes gen1 numbers): run HEAD CLI at Bo_SE grid, gamma 1.
usage: python3 -I -B probe_contrast.py <repo_worktree>
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from probe_d2_readback import parse, SEED2PH  # noqa: E402

REPO = sys.argv[1]
GEN = os.path.join(HERE, 'gen', 'mmd_HEAD.py')
DF = os.path.join(REPO, 'scripts', 'mixer_deck_diff.py')
BASE = ['--n-total', '100000', '--cgf', '151.4', '--seed', '32452843', '--revolutions', '2', '--dens-gen', 'lab20261014',
        '--stiffen-se', '20', '--hold-bo-pairwise']
env = dict(os.environ, OPENBLAS_NUM_THREADS='1')
R = {}
with tempfile.TemporaryDirectory(dir=HERE) as td:
    U, C = os.path.join(td, 'unc'), os.path.join(td, 'coat')
    for out, gg in ((U, 'AM_P=0.3,AM_S=0.3'), (C, 'AM_P=1,AM_S=1')):
        p = subprocess.run([sys.executable, '-I', '-B', GEN, '--out', out] + BASE + ['--gm-gamma', gg, '--gm-wall-ncm', '0.3',
                                                                                      '--gm-bo-se', '0.21244'],
                           capture_output=True, text=True, env=env)
        assert p.returncode == 0, p.stderr[-400:]
    Du, Dc = parse(open(os.path.join(U, 'in.mixer'), encoding='utf-8').read()), parse(open(os.path.join(C, 'in.mixer'), encoding='utf-8').read())
    n = Du['n']
    nm = {at: SEED2PH[v['seed']] for at, v in Du['tpl'].items()}
    nm[n] = 'WALL'
    diff = []
    for i in range(n):
        for j in range(i, n):
            a, b = Du['ced'][i][j], Dc['ced'][i][j]
            if a != b:
                diff.append((f'{nm[i + 1]}-{nm[j + 1]}', a, b, b / a if a else None))
    R['changed_pairs'] = diff
    R['n_changed'] = len(diff)
    R['diff_tool'] = {}
    for allow in ('A', 'B', 'U', 'E', 'EB'):
        p = subprocess.run([sys.executable, '-I', '-B', DF, os.path.join(U, 'in.mixer'), os.path.join(C, 'in.mixer'), '--allow', allow],
                           capture_output=True, text=True, env=env)
        R['diff_tool'][allow] = dict(rc=p.returncode, tail=(p.stdout + p.stderr).strip().splitlines()[-2:])
    # (3) ceiling bound, lab, soft (the soft matrix is checked first)
    soft = ['--n-total', '100000', '--cgf', '151.4', '--seed', '32452843', '--revolutions', '2', '--dens-gen']
    R['ceiling'] = {}
    for gen_ in ('gen1', 'lab20261014'):
        row = {}
        for bo in (637.32, 830, 850, 1000, 1010, 1020, 1050):
            p = subprocess.run([sys.executable, '-I', '-B', GEN, '--out', os.path.join(td, f'c_{gen_}_{bo}')] + soft + [gen_] +
                               ['--gm-gamma', 'AM_P=1,AM_S=1', '--gm-gamma-wall', '0.0256', '--gm-bo-se', f'{bo:g}'],
                               capture_output=True, text=True, env=env)
            row[f'{bo:g}'] = 'accepted' if p.returncode == 0 else ('refused: ' + (p.stderr.strip().splitlines() or [''])[-1].split(':')[-1][:60])
        R['ceiling'][gen_] = row
json.dump(R, open(os.path.join(HERE, 'probe_contrast.json'), 'w'), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1)[:5000])
