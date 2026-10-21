#!/usr/bin/env python3
"""Diagnose remaining V-shape difference: which system arrays differ between B step 0.25 and 0.125."""
import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
import test_carbon_junction as T  # noqa: E402
import step3_sigma as S3  # noqa: E402
import carbon_junction as CJ  # noqa: E402

T.S3, T.CJ = S3, CJ


def run(stepB):
    P = T.cat_rows(T.rows([T.VSH[0]], fids=[10]), T.rows([T.VSH[1]], step=stepB, fids=[20]))
    return T._solve_full(P, T.VSH_N)


a, b = run(0.25), run(0.125)
sa, sb = a[2]['_cjunc']['sys'], b[2]['_cjunc']['sys']
for k in ('u', 'v', 'G', 'CAT', 'Ab', 'gb', 'At', 'gt'):
    xa, xb = np.asarray(sa[k]), np.asarray(sb[k])
    same = xa.shape == xb.shape and xa.tobytes() == xb.tobytes()
    print(k, xa.shape, xb.shape, 'same' if same else 'DIFF')
    if not same and xa.shape == xb.shape:
        d = np.flatnonzero(xa != xb)
        print('   idx', d[:10], xa[d[:5]], xb[d[:5]])
ra, rb = a[1], b[1]
print('n positions', len(ra['positions']['lin']), len(rb['positions']['lin']))
print('pos lin same', ra['positions']['lin'].tobytes() == rb['positions']['lin'].tobytes())
print('n_extra', ra['n_extra_dofs'], rb['n_extra_dofs'])
print('Lc', ra['instances']['Lc'], rb['instances']['Lc'], 'mult', ra['instances']['mult'], rb['instances']['mult'])
print('nsub', ra['instances']['nsub'], rb['instances']['nsub'])
sua, sub_ = ra['subedges'], rb['subedges']
print('X_i', sua['X_i'], sub_['X_i'])
print('X_j', sua['X_j'], sub_['X_j'])
print('faces same', all(np.asarray(ra['faces'][k]).tobytes() == np.asarray(rb['faces'][k]).tobytes() for k in ra['faces']))
for k in ra['faces']:
    if np.asarray(ra['faces'][k]).tobytes() != np.asarray(rb['faces'][k]).tobytes():
        print('  face key diff', k, np.asarray(ra['faces'][k])[:12], np.asarray(rb['faces'][k])[:12])
