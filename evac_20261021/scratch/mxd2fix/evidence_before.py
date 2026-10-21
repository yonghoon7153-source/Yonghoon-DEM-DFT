"""Evidence (scratch, read-only on the repo) — how the UNFIXED tools behave on lab / D2 decks (the review's PRE-01 · 02 counterexamples).
usage: python3 -B evidence_before.py <repo>   — prints one line per probe."""
import os
import re
import sys

REPO = sys.argv[1]
sys.path.insert(0, os.path.join(REPO, 'scripts'))
import make_mixer_deck as g  # noqa: E402
import mixer_deck_readback as rb  # noqa: E402
import mixer_deck_diff as dd  # noqa: E402
import mixer_smoke_blind as sb  # noqa: E402

LAB = 'lab20261014'


def gm_deck(gp, gs, rho, bo, F, gen=LAB):
    p = g.plan(100000, cgf=151.4, stiffen_se=F, dens_gen=gen)
    a = g.gm_arm({'AM_P': gp, 'AM_S': gs, 'SE': 1.0}, gamma_wall=g.gm_wall_from_ncm(rho), bo_se=bo, rho_uncoated_ncm=rho)
    nm = g.register_arm('GMEV', a)
    try:
        return g.deck(p, g.resolve_rpm(p['R']), 2, seed=32452843, arm=nm, hold_bo_pairwise=(F != 1.0))
    finally:
        g.ARMS.pop(nm, None)


def lc_lab(F):
    p = g.plan(100000, cgf=151.4, stiffen_se=F, dens_gen=LAB)
    return g.deck(p, g.resolve_rpm(p['R']), 2, seed=32452843, arm='LC', hold_bo_pairwise=(F != 1.0))


T = rb.compare('E', rb.read_deck(lc_lab(1.0), 'LC_lab_soft'), rb.read_deck(lc_lab(20.0), 'LC_lab_ref'))
print('readback E LC lab soft->ref20:', T['verdict'], '|', (T['failures'] or ['-'])[0][:170])
T = rb.compare('E', rb.read_deck(gm_deck(0.3, 0.3, 0.3, 0.5, 1.0), 'GM_lab_soft'), rb.read_deck(gm_deck(0.3, 0.3, 0.3, 0.5, 20.0), 'GM_lab_ref'))
print('readback E GMuu lab soft->ref20:', T['verdict'], '|', (T['failures'] or ['-'])[0][:170])
uu, cc = gm_deck(0.3, 0.3, 0.3, 0.5, 20.0), gm_deck(1.0, 1.0, 0.3, 0.5, 20.0)
for allow in ('A', 'B', 'U', 'E', 'EB'):
    r = dd.diff_decks(uu, cc, allow)
    print(f'diff --allow {allow} GMuu->GMcc:', r['verdict'], '| outside', r.get('outside'), '| e_rule', (r.get('e_rule') or [])[:1])
try:
    dd.diff_decks(uu, cc, 'GM')
    print('diff --allow GM: (no exception)')
except Exception as e:  # noqa: BLE001
    print('diff --allow GM:', type(e).__name__, str(e)[:80])
k = (2.00 / 1.64) ** (1.0 / 3.0)


def scale(t):
    return re.sub(r'(?m)^(fix mC .*\n)((?:    .*\n){4})',
                  lambda mm: mm.group(1) + ''.join('    ' + ' '.join(f'{float(x) * k:g}' if float(x) else x for x in ln.rstrip().rstrip('&').split())
                                                   + (' &' if ln.rstrip().endswith('&') else '') + '\n' for ln in mm.group(2).split('\n')[:4]), t, count=1)


soft, ref = gm_deck(0.3, 0.3, 0.3, 0.5, 1.0), gm_deck(0.3, 0.3, 0.3, 0.5, 20.0)
r = dd.diff_decks(scale(soft), scale(ref), 'E')
print('diff --allow E on M04-like pair (all CED x (2.00/1.64)^(1/3), header still says Bo 0.5):', r['verdict'])
for nm in ('GMuu_rho0p3_bo0p5_lab20261014_ref_r2_s32452843',):
    try:
        dd.parse_cell(nm)
        print('parse_cell D2 name: accepted')
    except ValueError as e:
        print('parse_cell D2 name: ValueError', str(e)[:90])
print('smoke _expected_counts(dict(stiffen_se=20, dens_gen=lab)):', sb._expected_counts(dict(stiffen_se=20.0, dens_gen=LAB)),
      '| lab plan:', {i + 1: g.plan(100000, cgf=151.4, dens_gen=LAB)['n'][t] for i, t in enumerate(g.TYPES)})
