"""Extra positive generator options for the MXD2R-04 strict form (not in the committed tests): revolutions 0 · explicit
settle time · explicit in-band rpm · stiffen 14 · 28 · restitution 0.5 (settle time only) · dt/4 + layered 2 phases ·
seeds near 2^31 · n tiny/large.  Each = three consumer APIs on the generator's own uncoated/coated pair."""
import sys

sys.path.insert(0, sys.argv[1])
import make_mixer_deck as gen
import mixer_deck_readback as rb
import mixer_deck_diff as dd
import mixer_smoke_blind as smoke


def pair(phases=('AM_P', 'AM_S', 'SE'), generation='lab20261014', stiff=20., rho=.3, bo=.73, n=100000, cgf=151.4, layered=True,
         seed=32452843, dt_factor=1., revolutions=2, settle_s=None, rpm=None, restitution=0.3, dump_full_precision=False):
    out = []
    old = gen.TYPES
    try:
        gen.set_phases(phases)
        for coated in (False, True):
            gamma = {p: 1. if coated or p == 'SE' else rho for p in phases}
            arm = gen.gm_arm(gamma, gamma_wall=gen.gm_wall_from_ncm(rho), bo_se=bo, rho_uncoated_ncm=rho)
            arm['layered'] = layered
            gen.ARMS['D2X'] = arm
            p = gen.plan(n, cgf=cgf, stiffen_se=stiff, dens_gen=generation)
            r = gen.resolve_rpm(p['R'], rpm=rpm) if rpm else gen.resolve_rpm(p['R'])
            text = gen.deck(p, r, revolutions, seed=seed, arm='D2X', hold_bo_pairwise=True, dt_factor=dt_factor, settle_s=settle_s,
                            restitution=restitution, dump_full_precision=dump_full_precision)
            meta = gen.deck_meta(p, r, revolutions, seed, 'D2X', text, hold_bo_pairwise=True, dt_factor=dt_factor, settle_s=settle_s,
                                 restitution=restitution, dump_full_precision=dump_full_precision)
            out.append((text, meta))
    finally:
        gen.ARMS.pop('D2X', None)
        gen.set_phases(old)
    return out


options = [dict(revolutions=0), dict(revolutions=0, layered=False, dt_factor=.5), dict(settle_s=0.37), dict(settle_s=1.9, dt_factor=.25),
           dict(rpm=60.0), dict(rpm=70.0), dict(rpm=72.5, layered=False), dict(stiff=14.), dict(stiff=28., phases=('AM_P', 'SE')), dict(restitution=0.5), dict(dt_factor=.25, phases=('AM_P', 'SE')),
           dict(seed=2147483647), dict(seed=2147483629, layered=False), dict(n=20000, cgf=302.8), dict(n=300000, cgf=75.7, generation='gen1'),
           dict(revolutions=8, dump_full_precision=True), dict(rho=1.), dict(bo=3.0, rho=.03), dict(dt_factor=1 / 3, layered=False, revolutions=0)]
bad = 0
for kw in options:
    try:
        (a, am), (b, bm) = pair(**kw)
    except SystemExit as exc:
        print('GENERATOR REFUSED', kw, str(exc)[:80])
        continue
    res = [rb.read_d2(a, am), dd.diff_d2_decks(a, b, am, bm), smoke.d2_plan_check(a, am), rb.read_d2(a.encode(), am)]
    verdicts = [r['verdict'] for r in res]
    ok = verdicts == ['PASS'] * 4
    bad += not ok
    print('ok ' if ok else 'BAD', kw, verdicts, '' if ok else (res[0]['failures'] or res[1]['failures'])[0][:200])
print('bad', bad, 'of', len(options))
