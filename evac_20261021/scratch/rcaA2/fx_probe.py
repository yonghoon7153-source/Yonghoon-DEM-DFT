# -*- coding: utf-8 -*-
"""fixture sanity (scratch) — cell sequences, non-consecutive face-adjacent pairs, base behaviour."""
import math
import os
import sys
REPO = os.environ.get('PRE_REPO', '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1ea4b71aa06a03ee')
sys.path.insert(0, '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prereview_impl')
os.environ['PRE_REPO'] = REPO
from pcommon import *   # noqa: F401,F403
from fibre_segment_raster import segment_cells


def seqc(pts, vox=H):
    cs = np.vstack([segment_cells(pts[i], pts[i + 1], vox) for i in range(len(pts) - 1)])
    keep = np.ones(len(cs), bool); keep[1:] = np.any(cs[1:] != cs[:-1], axis=1)
    return [tuple(int(v) for v in c) for c in cs[keep]]


def contact_pairs(seq):
    out = []
    for a in range(len(seq)):
        for b in range(a + 2, len(seq)):
            d = np.abs(np.array(seq[a]) - np.array(seq[b]))
            if d.sum() == 1:
                out.append((a, b, seq[a], seq[b]))
    return out


XC = [(1.5, 1.5, 0.5), (1.5, 1.5, 4.5), (1.5, 4.5, 4.5), (2.3, 4.5, 4.5), (2.3, 4.5, 2.5), (2.3, 0.5, 2.5), (2.3, 0.5, 7.5)]
s = seqc(densify(XC))
print('XC seq', len(s), s)
print('XC face pairs', contact_pairs(s))
RING = [(1.5, 1.5, 4.2), (1.5, 1.5, 7.5), (3.5, 1.5, 7.5), (3.5, 1.5, 0.5), (1.5, 1.5, 0.5), (1.5, 1.5, 4.2)]
pr = densify(RING)
print('RING npts', len(pr), pr[0], pr[-1], np.array_equal(pr[0], pr[-1]))
# gap on right leg: remove z 4.25, 4.0, 3.75 at x 3.5
m = ~((np.abs(pr[:, 0] - 3.5) < 1e-9) & (pr[:, 2] > 3.6) & (pr[:, 2] < 4.4))
pg = pr[m]
print('RING_GAP removed', int((~m).sum()), 'pts', [tuple(x) for x in pr[~m]])
d = np.linalg.norm(np.diff(pg, axis=0), axis=1)
print('RING_GAP max step', d.max(), 'median', np.median(d))
SVY_A = [(1.5, 1.5, 0.5), (1.5, 1.5, 7.5)]
SVY_B = [(1.5, 2.5, 3.5), (4.5, 2.5, 3.5), (4.5, 2.5, 7.5)]
print('SVY B seq', seqc(densify(SVY_B)))
UF = [(1.5, 1.5, 0.5), (1.5, 1.5, 4.5), (2.5, 1.5, 4.5), (2.3, 1.5, 1.5), (4.5, 1.5, 1.5), (4.5, 1.5, 7.5)]
# base behaviour of XC
P = rows([XC])
sid, _ = bed(P, (5, 6, 8))
for smin in (5.0, 15.0):
    reg = registry(sid, P, s_min_um=smin)
    I = reg['instances']
    print('XC base smin', smin, 'n', len(I['fi']), 'self', int(I['self'].sum()), 'Lc', I['Lc'].tolist(), 's', I['s'].tolist(),
          'cen', {k: reg['census'].get(k) for k in ('n_self_candidates', 'n_self_kept', 'n_self_fused_faces')})
    r = solve(sid, sig_e(), (5, 6, 8), plan(reg, 1e3))
    print('   I', I_of(r, (5, 6, 8)), r.get('reason'))
with direct_solver():
    rl = quiet(S3.solve_sigma_z, sid, sig_e(), H, z_top_um=8.0, z_bot_um=0.0)
print('XC legacy', I_of(rl, (5, 6, 8)))
