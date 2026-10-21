"""D3 design number checks against the generator (read-only; imports scripts/make_mixer_deck.py)."""
import importlib.util
import math
import sys

REPO = sys.argv[1]
spec = importlib.util.spec_from_file_location('mmd', f'{REPO}/scripts/make_mixer_deck.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

print('BO_BASE', m.BO_BASE, 'MU_S', m.MU_S, 'MU_R', m.MU_R, 'COR', m.COR, 'FR', m.FR_ANCHOR)
print('E_PHASE', m.E_PHASE)
print('GM_WALL_HARE2026', m.GM_WALL_HARE2026)

grid = [m.BO_BASE * 10 ** (k / 2) for k in range(7)] + [3000 * m.BO_BASE]
print('grid (x sqrt10 from BO_BASE; last = 3000*BO_BASE):', [round(x, 4) for x in grid])
print('ratio of last step', grid[-1] / grid[-2], ' sqrt10 =', math.sqrt(10))


def se_overlap(bo, E_se, rho_se, d_se):
    r = d_se / 2.0
    nu = m.PHASE_MECH['SE'][0]
    ced = m.ced_for_bond(bo, r, nu, rho_se, E=E_se)
    return m.overlap_for_ced(ced, r, nu, E=E_se), ced


def v_stick(ced, E_se, rho_se, d_se):
    """same formula as generator self-test U5 (SE-SE)."""
    r = d_se / 2.0
    nu = m.PHASE_MECH['SE'][0]
    es = E_se / (2.0 * (1.0 - nu ** 2))
    rs = r / 2.0
    W = 0.2 * math.pi * ced * rs * (2.0 * math.pi * rs * ced / ((4.0 / 3.0) * es * math.sqrt(rs))) ** 4
    mi = (4.0 / 3.0) * math.pi * r ** 3 * rho_se * 1000.0
    ms = mi / 2.0
    return math.sqrt(2.0 * W * (1.0 - m.COR ** 2) / (m.COR ** 2 * ms)) * 1e3


for gen in (None, 'lab20261014'):
    for F in (1.0, 20.0):
        p = m.plan(100000, cgf=151.4, stiffen_se=F, dens_gen=gen)
        rho_se = p['dens']['SE']
        d_se = p['d']['SE']
        E_se = p['E']['SE']
        rpm = m.rpm_for_fr(m.FR_ANCHOR, p['R'])
        print(f'\n== gen {gen} x{F:g}: R {p["R"]*1e3:.4f} mm  D {2*p["R"]*1e3:.3f} mm  L {p["L"]*1e3:.4f} mm  rpm(Fr) {rpm:.3f}  '
              f'wR {2*math.pi*rpm/60*p["R"]*1e3:.2f} mm/s  dt {p["dt"]:.4e} s (by {p["dt_by"]})  n {p["n"]}')
        print('   phi', {k: round(v, 4) for k, v in p['phi'].items()})
        vdrum = math.pi * p['R'] ** 2 * p['L']
        vp = math.pi / 6 * d_se ** 3
        print(f'   V_drum {vdrum:.4e} m3  V_parcel {vp:.4e} m3  N(f, pack 0.6) per unit f = {vdrum*0.6/vp:.4e}')
        # mixer solid fill
        vs = sum(p['n'][k] * math.pi / 6 * p['d'][k] ** 3 for k in p['n'])
        print(f'   mixer solid {vs:.4e} m3 ; fill (pack 0.6) {vs/(vdrum*0.6):.4f}')
        for bo in (m.BO_BASE, 1000 * m.BO_BASE, 3000 * m.BO_BASE):
            ov, ced = se_overlap(bo, E_se, rho_se, d_se)
            print(f'   Bo {bo:9.4f}: SE-SE delta0/r {ov*100:.4f} %  CED {ced:.4e}  v_stick {v_stick(ced, E_se, rho_se, d_se):.3f} mm/s')
        # Bo at 1 % (bisection in log)
        lo, hi = 1.0, 1e7
        for _ in range(200):
            mid = math.sqrt(lo * hi)
            if se_overlap(mid, E_se, rho_se, d_se)[0] > 0.01:
                hi = mid
            else:
                lo = mid
        print(f'   Bo at SE-SE 1 % static ceiling: {lo:.1f}')
        # sec per simulated second at 63-70 step/s
        steps = 1.0 / p['dt']
        print(f'   steps per sim-second {steps:.4e}; hours at 70/63 step/s: {steps/70/3600:.2f} / {steps/63/3600:.2f}')

# rho_flow identifiability: Bo_AA / Bo_SS under the geomean rule, for given rho = gamma_NCM/gamma_SE
for gen in (None, 'lab20261014'):
    p = m.plan(100000, cgf=151.4, dens_gen=gen)
    dn = p['dens']
    d = p['d']
    w = {k: math.pi / 6 * d[k] ** 3 * dn[m.PHASE_MECH[k][1]] for k in d}
    rss = d['SE'] / 4.0
    for k in ('AM_P', 'AM_S'):
        raa = d[k] / 4.0
        # Bo_AA/Bo_SS = rho * (R*_AA/R*_SS) * (W_SE/W_AM)
        fac = (raa / rss) * (w['SE'] / w[k])
        print(f'gen {gen}: Bo_{k}{k}/Bo_SS = rho x {fac:.5f}  (1/{1/fac:.1f})')
        # Bo of SE->AM attachment relative to SE-SE (small particle = SE)
        ras = (d[k] / 2 * d['SE'] / 2) / (d[k] / 2 + d['SE'] / 2)
        print(f'   F_{k}SE/F_SS at rho=1 = R*_AS/R*_SS = {ras/rss:.4f};  thesis threshold rho < 1/(that)^2 = {1/(ras/rss)**2:.4f}')

# wall: SE-wall force ratio vs SE-SE for rho values (R*_SW = r_SE, R*_SS = r_SE/2)
for rho in (1.0, 0.31, 0.1, 0.01):
    gw = m.GM_WALL_HARE2026 * rho
    print(f'rho {rho}: gamma_W/gamma_SE {gw:.5f}  F_SW/F_SS = sqrt(gw) * 2 = {2*math.sqrt(gw):.4f}')

# T5 bed pressure check
for gen in (None, 'lab20261014'):
    p = m.plan(100000, cgf=151.4, dens_gen=gen)
    dn = p['dens']
    wt = p['wt']
    rho_mix = 100.0 / sum(wt[k] / dn[m.PHASE_MECH[k][1]] for k in wt)
    print(f'gen {gen}: solid mean density {rho_mix:.4f} g/cm3 ; bed p at 0.68R depth, 0.6 pack = {0.6*rho_mix*1000*9.81*0.68*p["R"]:.1f} Pa')

# segment fill fraction 0.30 -> depth/R
f = 0.30
lo, hi = 0.0, 2 * math.pi
for _ in range(200):
    th = (lo + hi) / 2
    if (th - math.sin(th)) / (2 * math.pi) > f:
        hi = th
    else:
        lo = th
print('fill 0.30 -> depth/R', 1 - math.cos(lo / 2))
