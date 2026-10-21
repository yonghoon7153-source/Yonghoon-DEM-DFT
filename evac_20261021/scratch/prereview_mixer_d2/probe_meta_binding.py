#!/usr/bin/env python3
"""Probe I — sealed-record (deck_meta.json adhesion_rule) <-> deck CED binding, with two surviving mutants.

For HEAD and mutants M04 (F0_SS uses gen1 SE density) and M16 (meta bo_se written as the constant BO_BASE):
  1) generate lab20261014 D2 decks soft and x20 (same gamma 0.3/0.5, --gm-wall-ncm 0.3, --gm-bo-se 0.5)
  2) read Bo_SE back from the PRINTED deck (my parser · SE template radius + density · g) and compare with meta.adhesion_rule.bo_se
  3) run the repo checkers (HEAD scripts, read only) on soft -> x20:  mixer_deck_readback --table E  ·  mixer_deck_diff --allow E
Shows whether any repo tool notices that the sealed record and the deck disagree.
usage: python3 -I -B probe_meta_binding.py <repo_worktree>
"""
import json
import math
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from probe_d2_readback import parse, SEED2PH  # noqa: E402

REPO = sys.argv[1]
GENS = {'HEAD': os.path.join(HERE, 'gen', 'mmd_HEAD.py'),
        'M04_F0SS_gen1_density': os.path.join(HERE, 'mut', 'M04_F0SS_gen1_density', 'make_mixer_deck.py'),
        'M16_meta_bo_const': os.path.join(HERE, 'mut', 'M16_meta_bo_const', 'make_mixer_deck.py')}
RB = os.path.join(REPO, 'scripts', 'mixer_deck_readback.py')
DF = os.path.join(REPO, 'scripts', 'mixer_deck_diff.py')
BASE = ['--n-total', '100000', '--cgf', '151.4', '--seed', '32452843', '--revolutions', '2', '--dens-gen', 'lab20261014',
        '--gm-gamma', 'AM_P=0.3,AM_S=0.5', '--gm-wall-ncm', '0.3', '--gm-bo-se', '0.5']
env = dict(os.environ, OPENBLAS_NUM_THREADS='1')


def bo_read(path):
    D = parse(open(path, encoding='utf-8').read())
    n = D['n']
    names = {at: SEED2PH[v['seed']] for at, v in D['tpl'].items()}
    ph = {nm: at for at, nm in names.items()}
    i = ph['SE'] - 1
    r = D['tpl'][ph['SE']]['r']
    rho = D['tpl'][ph['SE']]['rho']
    es = 1.0 / (2 * (1 - D['nu'][i] ** 2) / D['E'][i])
    rs = r / 2.0
    f0 = 4.5 * math.pi ** 3 * rs ** 2 * D['ced'][i][i] ** 3 / es ** 2
    return f0 / ((4.0 / 3.0) * math.pi * r ** 3 * rho * D.get('g', 9.81))


R = {}
with tempfile.TemporaryDirectory(dir=HERE) as td:
    for lab, gen in GENS.items():
        rec = {}
        outs = {}
        for lvl, extra in (('soft', []), ('ref20', ['--stiffen-se', '20', '--hold-bo-pairwise'])):
            o = os.path.join(td, f'{lab}_{lvl}')
            p = subprocess.run([sys.executable, '-I', '-B', gen, '--out', o] + BASE + extra, capture_output=True, text=True, env=env)
            if p.returncode != 0:
                rec[lvl] = dict(rc=p.returncode, err=(p.stderr.strip().splitlines() or [''])[-1][:160])
                continue
            meta = json.load(open(os.path.join(o, 'deck_meta.json'), encoding='utf-8'))
            br = bo_read(os.path.join(o, 'in.mixer'))
            rec[lvl] = dict(rc=0, meta_bo_se=meta['adhesion_rule']['bo_se'], deck_bo_se_read=br,
                            deck_over_meta=br / meta['adhesion_rule']['bo_se'], meta_dens_gen=meta.get('dens_gen'))
            outs[lvl] = os.path.join(o, 'in.mixer')
        if len(outs) == 2:
            js = os.path.join(td, f'{lab}_rb.json')
            p = subprocess.run([sys.executable, '-I', '-B', RB, '--table', 'E', outs['soft'], outs['ref20'], '--json', js],
                               capture_output=True, text=True, env=env)
            fails = []
            if os.path.exists(js):
                for T in json.load(open(js, encoding='utf-8')).get('tables', []):
                    fails += T.get('failures', [])
            rec['repo_readback_E'] = dict(rc=p.returncode, first_failure=(fails[:1] or ['PASS'])[0][:180])
            p = subprocess.run([sys.executable, '-I', '-B', DF, outs['soft'], outs['ref20'], '--allow', 'E'],
                               capture_output=True, text=True, env=env)
            rec['repo_diff_E'] = dict(rc=p.returncode, tail=(p.stdout + p.stderr).strip().splitlines()[-1:])
        R[lab] = rec
json.dump(R, open(os.path.join(HERE, 'probe_meta_binding.json'), 'w'), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1))
