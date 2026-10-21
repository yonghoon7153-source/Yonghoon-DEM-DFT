"""Small hand attacks on the new guarantees (fixed tree) — G1 broken pieces fid-independent · G2 ring seam position / reversal ·
G4 counterfactual ratio >= 1 on random SDCP beds · G5 realized ports live."""
import math
import os
import sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/probes')
os.environ.setdefault('PRE_REPO', '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1ea4b71aa06a03ee')
from pcommon import *   # noqa: F401,F403

out = {}
rj = 1e3
# G1 — one fid, two pieces (gap) vs two fids, same points
N = (3, 3, 8)
pA = densify([(1.5, 1.5, 0.5), (1.5, 1.5, 3.15)]); pB = densify([(1.5, 1.5, 3.85), (1.5, 1.5, 7.5)])
one = rows_pts([np.vstack([pA, pB])], fids=[10])
two = rows_pts([pA, pB], fids=[10, 20])
r1 = registry(bed(one, N)[0], one); r2 = registry(bed(two, N)[0], two)
sid1 = bed(one, N)[0]
I1 = I_of(solve(sid1, sig_e(), N, plan(r1, rj)), N); I2 = I_of(solve(bed(two, N)[0], sig_e(), N, plan(r2, rj)), N)
k = ('Lc', 'mult', 'd0', 'nsub')
out['G1'] = {'same_records': all(np.array_equal(np.asarray(r1['instances'][x]), np.asarray(r2['instances'][x])) for x in k),
             'ports_same': [tuple(r1['positions']['ijk'][r1['instances']['port_i'][0]])] == [tuple(r2['positions']['ijk'][r2['instances']['port_i'][0]])],
             'I_one': I1, 'I_two': I2, 'rel': abs(I1 - I2) / I2}
# G2 — ring seam position and reversal
RN = (5, 3, 8)
base = [(1.5, 1.5, 4.2), (1.5, 1.5, 7.5), (3.5, 1.5, 7.5), (3.5, 1.5, 0.5), (1.5, 1.5, 0.5), (1.5, 1.5, 4.2)]
alt = [(3.5, 1.5, 2.0), (3.5, 1.5, 0.5), (1.5, 1.5, 0.5), (1.5, 1.5, 7.5), (3.5, 1.5, 7.5), (3.5, 1.5, 2.0)]
res = {}
for nm, poly in (('seam_left', base), ('seam_right', alt), ('seam_left_reversed', base[::-1])):
    P = rows([poly]); sid = bed(P, RN)[0]
    reg = registry(sid, P)
    res[nm] = (I_of(solve(sid, sig_e(), RN, plan(reg, rj)), RN), int(np.sum(reg['instances']['self'])), reg['census'].get('n_seam_alias'),
               sid.tobytes() == bed(rows([base]), RN)[0].tobytes())
out['G2'] = res
# G4/G5 — random beds with fibres + SDCP points: ratio >= 1 · realized ports live · unrealized reasons in the closed set
rng = np.random.default_rng(20261021)
bad, n_ok, ratios = [], 0, []
for t in range(12):
    n = (6, 6, 8)
    box = np.array(n, float)
    polys = []
    for f in range(int(rng.integers(3, 6))):
        p0 = rng.uniform(0.5, box - 0.5); p1 = rng.uniform(0.5, box - 0.5)
        polys.append([tuple(p0), tuple(p1)])
    polys.append([(rng.uniform(1, 5), rng.uniform(1, 5), 0.5), (rng.uniform(1, 5), rng.uniform(1, 5), 7.5)])
    P = rows(polys)
    sd = rng.uniform(0.5, box - 0.5, (int(rng.integers(2, 6)), 3))
    Ps = cat_rows(P, rows_pts([sd], phase=5, kind=0, fid0=700))
    # SDCP points are separate fids (kind 0) — one fid each
    Ps = (Ps[0], Ps[1], np.r_[P[2], 700 + np.arange(len(sd))].astype(np.int64), Ps[3])
    sid = bed(Ps, n)[0]
    try:
        reg = registry(sid, Ps, tol_sj_um=0.1, r_sdcp_um=0.5)
        r = solve(sid, sig_e(), n, plan(reg, rj, sv_counterfactual={'threshold': None}, quantitative=False))
    except Exception as e:                                  # noqa: BLE001
        bad.append((t, f'{type(e).__name__}: {e}'))
        continue
    I = reg['instances']; pos = reg['positions']
    for q in range(len(I['fi'])):
        if I['realized'][q]:
            if not (pos['live'][I['port_i'][q]] and pos['live'][I['port_j'][q]]):
                bad.append((t, 'realized port dead'))
        elif str(I['reason'][q]) not in ('no_port_in_rport', 'out_of_box') and not str(I['reason'][q]).startswith('covered_'):
            bad.append((t, f'reason {I["reason"][q]!r}'))
    cf = ((r.get('cjunc') or {}).get('sv_counterfactual') or {})
    rt = cf.get('sv_counterfactual_ratio')
    if cf.get('status') == 'computed':
        ratios.append(rt)
        if not (rt >= 1.0 - 1e-12):
            bad.append((t, f'ratio {rt}'))
    n_ok += 1
out['G45'] = {'beds': n_ok, 'bad': bad, 'ratios': ratios}
print(out)
