"""Adversarial probes on the fixed readback / diff (scratch, not part of the repo)."""
import re
import sys
sys.path.insert(0, sys.argv[1] + '/scripts')
import make_mixer_deck as g  # noqa: E402
import mixer_deck_readback as rb  # noqa: E402
import mixer_deck_diff as dd  # noqa: E402

LAB = 'lab20261014'


def mk(gp, gs, rho, bo, F, gen=LAB, wall=None):
    p = g.plan(100000, cgf=151.4, stiffen_se=F, dens_gen=gen)
    a = (g.gm_arm({'AM_P': gp, 'AM_S': gs, 'SE': 1.0}, gamma_wall=wall, bo_se=bo) if wall is not None else
         g.gm_arm({'AM_P': gp, 'AM_S': gs, 'SE': 1.0}, gamma_wall=g.gm_wall_from_ncm(rho), bo_se=bo, rho_uncoated_ncm=rho))
    nm = g.register_arm('GMADV', a)
    try:
        rpm = g.resolve_rpm(p['R'])
        t = g.deck(p, rpm, 2, seed=32452843, arm=nm, hold_bo_pairwise=(F != 1.0))
        m = g.deck_meta(p, rpm, 2, 32452843, nm, t, argv=['x'], hold_bo_pairwise=(F != 1.0))
    finally:
        g.ARMS.pop(nm, None)
    return t, m


def probs(t, m=None):
    return rb.d2_check(rb.read_deck(t, 'x', meta=m))['problems']


uu, mu = mk(0.3, 0.3, 0.3, 0.5, 20.0)
uus, _ = mk(0.3, 0.3, 0.3, 0.5, 1.0)
uub, _ = mk(0.3, 0.3, 0.3, 0.4, 1.0)
cc, mc = mk(1.0, 1.0, 0.3, 0.5, 20.0)
ccx, _ = mk(1.0, 1.0, None, 0.5, 20.0, wall=g.gm_wall_from_ncm(0.3))
R = {}
dup = uu.replace('#   γ/γ_SE: AM_P', '#   γ/γ_SE: AM_P 0.3 · AM_S 0.3 · SE 1 · γ_W/γ_SE 0.00768 · SE–SE Bo_code 0.5 (x)\n#   γ/γ_SE: AM_P', 1)
R['a dup decl line'] = probs(dup)[:1]
R['b nan token'] = probs(uu.replace('γ/γ_SE: AM_P 0.3 ', 'γ/γ_SE: AM_P nan ', 1))[:1]
R['f fullwidth token'] = probs(uu.replace('γ/γ_SE: AM_P 0.3 ', 'γ/γ_SE: AM_P ０.３ ', 1))[:1]
T = rb.compare('E', rb.read_deck(uus, 'soft05'), rb.read_deck(re.sub(r'Bo_code 0\.5 \(', 'Bo_code 0.5 (', uu), 'ref05'))
R['c0 E soft->ref same Bo (control)'] = T['verdict']
Tc = rb.compare('E', rb.read_deck(uub, 'soft04'), rb.read_deck(uu, 'ref05'))
R['c readback E soft Bo0.4 -> ref Bo0.5'] = (Tc['verdict'], [f for f in Tc['failures'] if '같은 팔' in f][:1])
dE = dd.diff_decks(uub, uu, 'E')
R['c diff E soft Bo0.4 -> ref Bo0.5'] = (dE['verdict'], (dE.get('d2_rule') or [])[:1], (dE.get('e_rule') or [])[:1])
Tg = rb.compare('GM', rb.read_deck(uu, 'uu'), rb.read_deck(ccx, 'cc_explicit'))
R['d readback GM uu(ncm) -> cc(explicit same γ_W)'] = (Tg['verdict'], [f for f in Tg['failures'] if 'ρ 세계' in f][:1])
dG = dd.diff_decks(uu, ccx, 'GM')
R['d diff GM uu(ncm) -> cc(explicit)'] = (dG['verdict'], (dG.get('d2_rule') or [])[:1])
dB = dd.diff_decks(uu, cc, 'B')
R['e diff B with D2 decks'] = (dB['verdict'], dB.get('d2_rule'), dB.get('outside'))
strip = '\n'.join(l for l in uu.split('\n') if not l.startswith('# ★ D2 결합 규칙'))
R['g header head removed + meta'] = probs(strip, dict(mu, deck_sha256=rb.read_deck(strip, 'x')['sha256']))[:1]
dH = dd.diff_decks(uus, strip, 'E')
R['h diff E D2 soft -> head-stripped ref'] = (dH['verdict'], (dH.get('d2_rule') or [])[:2])
R['i GM ok control'] = (dd.diff_decks(uu, cc, 'GM')['verdict'], rb.compare('GM', rb.read_deck(uu, 'a', meta=mu), rb.read_deck(cc, 'b', meta=mc))['verdict'])
R['j GM reversed (cc -> uu)'] = (dd.diff_decks(cc, uu, 'GM')['verdict'], rb.compare('GM', rb.read_deck(cc, 'a'), rb.read_deck(uu, 'b'))['verdict'])
for k, v in R.items():
    print(f'{k:48s} {v}')
