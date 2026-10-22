# -*- coding: utf-8 -*-
"""PF2 — QD2 circuits on a tree (census, cut rows, lower ratio)."""
import os
import sys

WT = sys.argv[1]
sys.path.insert(0, os.path.join(WT, 'scripts'))
sys.argv = [sys.argv[0]]
import test_carbon_junction as T   # noqa: E402
import step3_sigma as S3           # noqa: E402
import carbon_junction as CJ       # noqa: E402
T.S3, T.CJ = S3, CJ


def run(tag, polys, sdcp, n, thr=2.0):
    P = T.cat_rows(T.rows(polys), T.rows([[p] for p in sdcp], phase=5, kind=0, fid0=700))
    sid, _ = T.bed(P, n, sdcp_sphere_d_um=0.0)
    reg = T.registry(sid, P, tol_sj_um=0.1, r_sdcp_um=0.5)
    r = T.solve(sid, T.sig_e(), n, T.plan(reg, 1e3, sv_counterfactual={'threshold': thr}))
    cf = (r.get('cjunc') or {}).get('sv_counterfactual') or {}
    keys = ('status', 'sv_counterfactual_ratio', 'n_sv_faces_cut', 'n_bridging_components', 'n_unsplit_bridging_components',
            'G_full_code', 'G_cut_code', 'flag', 'sv_counterfactual_ratio_hi', 'status_hi', 'n_unsplit_cells')
    print(tag, 'I', T.I_of(r, n), 'sdcp', int((sid == 5).sum()), 'inst', len(reg['instances']['fi']),
          {k: cf.get(k) for k in keys}, 'upper', cf.get('upper'))
    return sid, reg, r, cf


run('QD2-1', [[(1.5, 1.5, 0.5), (1.5, 1.5, 6.5)], [(3.5, 1.5, 2.5), (3.5, 1.5, 8.5)]],
    [(1.5, 1.5, 4.5), (2.5, 1.5, 4.5), (3.5, 1.5, 4.5)], (5, 3, 9))
run('QD2-2', [[(1.5, 1.5, 0.5), (1.5, 1.5, 6.5)], [(3.5, 1.5, 4.5), (3.5, 1.5, 8.5)]],
    [(1.5, 1.5, 4.5), (2.5, 1.5, 4.5), (3.5, 1.5, 4.5)], (5, 3, 9))
run('QD2-3', [[(1.5, 1.5, 0.5), (1.5, 1.5, 8.5)], [(3.5, 1.5, 0.5), (3.5, 1.5, 5.5)], [(7.5, 1.5, 0.5), (7.5, 1.5, 8.5)]],
    [(1.5, 1.5, 3.5), (2.5, 1.5, 3.5), (3.5, 1.5, 3.5)], (9, 3, 9))
run('QD2-4', [[(1.5, 1.5, 0.5), (1.5, 1.5, 8.5)], [(5.5, 1.5, 0.5), (5.5, 1.5, 8.5)], [(3.5, 1.5, 4.5), (3.5, 1.5, 8.5)]],
    [(1.5, 1.5, 3.5), (2.5, 1.5, 3.5), (3.5, 1.5, 3.5), (4.5, 1.5, 3.5), (5.5, 1.5, 3.5)], (7, 3, 9))
run('QD2-5', [[(2.5, 1.5, 0.5), (2.5, 1.5, 8.5)], [(4.5, 1.5, 0.5), (4.5, 1.5, 8.5)]],
    [(3.5, 1.5, 3.5), (2.5, 1.5, 3.5), (2.5, 1.5, 4.5), (2.5, 1.5, 5.5), (3.5, 1.5, 5.5)], (6, 3, 9))
