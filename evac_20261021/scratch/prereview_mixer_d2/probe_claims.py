#!/usr/bin/env python3
"""Probe C — numbers claimed in the D2 commit / devlog v1.6 / MIX-12 / thesis §2-3, recomputed from PRINTED deck values.

Decks (HEAD generator CLI, CGF 151.4, 100k, seed 32452843, 2 revs, soft):
  LC gen1 (no --dens-gen)   ·  LC lab20261014  ·  GM gamma 1 gen1  ·  GM gamma 1 lab
Claims checked:
  devlog table (same gamma, soft): old min / new geomean F0/F0_SS  AM_P-SE 0.826/1.80 · AM_S-SE 0.653/1.60 · AM_P-AM_S 3.41/5.54 ·
    SE-WALL 0.162/0.32 · AM_P-WALL 4.06/2.88
  MIX-12: old SE-WALL/SE-SE 0.162 · AM-WALL/AM-AM 0.4516
  GM1 extended: GM gamma-1 diagonal CED = LC diagonal CED for BOTH density generations (selftest checks gen1 only)
  thesis 2-3: same-gamma Bo_SS/Bo_PP ~194 · Bo_SS/Bo_SS(AM_S) ~38 (gen1 densities) -> lab value
usage: python3 -I probe_claims.py   (writes probe_claims.json)
"""
import json
import math
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from probe_d2_readback import parse, SEED2PH  # noqa: E402  (my own parser; probe_d2_readback runs its cases on import guard below)

GEN = os.path.join(HERE, 'gen', 'mmd_HEAD.py')
BASE = ['--n-total', '100000', '--cgf', '151.4', '--seed', '32452843', '--revolutions', '2']


def deck_vals(text):
    D = parse(text)
    n = D['n']
    names = {at: SEED2PH[v['seed']] for at, v in D['tpl'].items()}
    names[n] = 'WALL'
    ph = {nm: at for at, nm in names.items()}
    r = {nm: D['tpl'][at]['r'] for at, nm in names.items() if nm != 'WALL'}
    rho = {nm: D['tpl'][at]['rho'] for at, nm in names.items() if nm != 'WALL'}

    def Rst(a, b):
        if a == 'WALL':
            a, b = b, a
        return r[a] if b == 'WALL' else r[a] * r[b] / (r[a] + r[b])

    def Est(a, b):
        ia, ib = ph[a] - 1, ph[b] - 1
        return 1.0 / ((1 - D['nu'][ia] ** 2) / D['E'][ia] + (1 - D['nu'][ib] ** 2) / D['E'][ib])

    def ced(a, b):
        return D['ced'][ph[a] - 1][ph[b] - 1]

    def F0(a, b):
        return 4.5 * math.pi ** 3 * Rst(a, b) ** 2 * ced(a, b) ** 3 / Est(a, b) ** 2
    W = {k: (4.0 / 3.0) * math.pi * r[k] ** 3 * rho[k] * 9.81 for k in r}
    return dict(F0=F0, ced=ced, W=W, r=r, rho=rho)


res = {}
with tempfile.TemporaryDirectory(dir=HERE) as td:
    def mk(label, args):
        out = os.path.join(td, label)
        p = subprocess.run([sys.executable, '-I', GEN, '--out', out] + BASE + args, capture_output=True, text=True)
        assert p.returncode == 0, (label, p.stderr[-500:])
        return open(os.path.join(out, 'in.mixer'), encoding='utf-8').read()
    T = dict(LC_gen1=mk('LC_gen1', ['--arm', 'LC']),
             LC_lab=mk('LC_lab', ['--arm', 'LC', '--dens-gen', 'lab20261014']),
             GM1_gen1=mk('GM1_gen1', ['--gm-gamma', 'AM_P=1,AM_S=1', '--gm-gamma-wall', '0.0256', '--gm-bo-se', '0.21244',
                                      '--dens-gen', 'gen1']),
             GM1_lab=mk('GM1_lab', ['--gm-gamma', 'AM_P=1,AM_S=1', '--gm-gamma-wall', '0.0256', '--gm-bo-se', '0.21244',
                                    '--dens-gen', 'lab20261014']))
V = {k: deck_vals(v) for k, v in T.items()}
pairs = [('AM_P', 'SE'), ('AM_S', 'SE'), ('AM_P', 'AM_S'), ('SE', 'WALL'), ('AM_P', 'WALL'), ('AM_S', 'WALL'),
         ('AM_P', 'AM_P'), ('AM_S', 'AM_S')]
for g in ('gen1', 'lab'):
    old, new = V[f'LC_{g}'], V[f'GM1_{g}']
    tab = {}
    for a, b in pairs:
        o = old['F0'](a, b) / old['F0']('SE', 'SE')
        n_ = new['F0'](a, b) / new['F0']('SE', 'SE')
        tab[f'{a}-{b}'] = dict(old=o, new=n_, new_over_old=n_ / o)
    tab['MIX12_old_SE-WALL/SE-SE'] = old['F0']('SE', 'WALL') / old['F0']('SE', 'SE')
    tab['MIX12_old_AMP-WALL/AMP-AMP'] = old['F0']('AM_P', 'WALL') / old['F0']('AM_P', 'AM_P')
    tab['MIX12_old_AMS-WALL/AMS-AMS'] = old['F0']('AM_S', 'WALL') / old['F0']('AM_S', 'AM_S')
    tab['GM_SE-WALL/SE-SE'] = new['F0']('SE', 'WALL') / new['F0']('SE', 'SE')
    tab['GM_AMP-WALL/AMP-AMP'] = new['F0']('AM_P', 'WALL') / new['F0']('AM_P', 'AM_P')
    tab['diag_ced_GM1_over_LC'] = {t: new['ced'](t, t) / old['ced'](t, t) for t in ('AM_P', 'AM_S', 'SE')}
    # same-gamma Bo ratios (thesis 2-3): Bo_tt = F0_tt / W_t
    bo = {t: new['F0'](t, t) / new['W'][t] for t in ('AM_P', 'AM_S', 'SE')}
    tab['thesis_Bo_SS/Bo_PP'] = bo['SE'] / bo['AM_P']
    tab['thesis_Bo_SS/Bo_AMS'] = bo['SE'] / bo['AM_S']
    tab['Bo_SE_read'] = bo['SE']
    res[g] = tab
json.dump(res, open(os.path.join(HERE, 'probe_claims.json'), 'w'), ensure_ascii=False, indent=1)
for g, tab in res.items():
    print('==', g)
    for k, v in tab.items():
        if isinstance(v, dict) and 'old' in v:
            print(f'  {k:12s} old {v["old"]:.4f}  new {v["new"]:.4f}  new/old {v["new_over_old"]:.3f}')
        else:
            print(f'  {k}: {v}')
