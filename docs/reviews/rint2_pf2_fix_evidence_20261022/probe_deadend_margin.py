# -*- coding: utf-8 -*-
"""PF2 E measured basis — two production CG solves (rtol 1e-12, CPU) whose exact terminal G are equal.

System 1 = sealed probe bed seed 0 (step3_conv_cert.probe_system · the bed of tests T4c / T4e · 41,472 cells · fibre sigma
7,853.98 / AM 0.0041).  System 2 = the same matrix plus one dead-end node hung on an interior node (one edge, no plate
coupling): the exact G is unchanged (no current in a dead end), so the true ratio G1*/G2* = 1 = the true "upper / lower"
bracket ratio of a component whose removal changes nothing.  The recorded ratio G1/G2 differs from 1 only by solve error.
Question: does an exact comparison (ratio >= 1, upper >= lower) fail on such a legitimate pair, and how large is the solve
error against the certificate width tau (1e-4)?
Run: python3 -I probe_deadend_margin.py <worktree> <out.json> [n_nodes]
"""
import json
import os
import sys
import time

import numpy as np

WT = sys.argv[1]
OUT = sys.argv[2]
NN = int(sys.argv[3]) if len(sys.argv) > 3 else 6
sys.path.insert(0, os.path.join(WT, 'scripts'))
import step3_sigma as S3            # noqa: E402
import step3_conv_cert as CC        # noqa: E402
from scipy import sparse            # noqa: E402
from scipy.sparse.linalg import spsolve   # noqa: E402

S3.GPU_SOLVE = False
S3.AMG_SOLVE = False
S3.CG_MAXITER = 400000
RT = 1e-12


def G_of(phi, Ab, gb):
    return float(np.sum(gb * (1.0 - phi[Ab])))


t0 = time.time()
sid = CC.probe_bed(0)
sysd = CC.probe_system(sid, CC.probe_sigma_table(), s3=S3)
L, b, Ab, gb, At = sysd['L'].tocsr(), sysd['b'], sysd['Ab'], sysd['gb'], sysd['At']
n = L.shape[0]
Gd = G_of(sysd['phi_direct'], Ab, gb)
phi1, info1 = S3._solve_cg(L, b, rtol=RT)
G1 = G_of(phi1, Ab, gb)
print(f'base n {n} · G1 {G1!r} · direct {Gd!r} · err {abs(G1 - Gd) / Gd:.3e} · info {info1} · {time.time() - t0:.0f} s', flush=True)
plates = set(int(x) for x in Ab) | set(int(x) for x in At)
offd = L.tocoo()
gvals = -offd.data[(offd.row != offd.col) & (offd.data < 0)]
rng = np.random.default_rng(100)
cand = [int(i) for i in rng.permutation(n)[:400] if int(i) not in plates][:NN]
rows = []
for i in cand:
    gd = float(np.median(gvals)) * float(10.0 ** rng.uniform(-3, 3))
    L2 = sparse.bmat([[L + sparse.csr_matrix(([gd], ([i], [i])), shape=(n, n)), sparse.csr_matrix(([-gd], ([i], [0])), shape=(n, 1))],
                      [sparse.csr_matrix(([-gd], ([0], [i])), shape=(1, n)), sparse.csr_matrix(([gd], ([0], [0])), shape=(1, 1))]]).tocsr()
    b2 = np.concatenate([b, [0.0]])
    phi2, info2 = S3._solve_cg(L2, b2, rtol=RT)
    G2 = G_of(phi2, Ab, gb)
    G2d = G_of(spsolve(L2.tocsc(), b2), Ab, gb)
    r = G1 / G2
    rows.append({'node': i, 'g_deadend': gd, 'G1': G1, 'G2': G2, 'G_direct_1': Gd, 'G_direct_2': G2d, 'info2': int(info2),
                 'ratio_G1_over_G2': r, 'ratio_minus_1': r - 1.0, 'exact_ge_1': bool(r >= 1.0),
                 'G1_err_rel': abs(G1 - Gd) / Gd, 'G2_err_rel': abs(G2 - G2d) / G2d, 'direct_G_rel_diff': abs(G2d - Gd) / Gd})
    print(f'node {i} · g {gd:.3e} · G1/G2 − 1 = {r - 1.0:+.3e} · G2 err {abs(G2 - G2d) / G2d:.3e} · direct diff '
          f'{abs(G2d - Gd) / Gd:.3e} · {time.time() - t0:.0f} s', flush=True)
tau = CC.CERT_TARGET_TOL
floor = (1 - tau) / (1 + tau)
dev = [abs(x['ratio_minus_1']) for x in rows]
summary = {'n_pairs': len(rows), 'n_cells': int(n), 'rtol': RT, 'tau': tau, 'floor': floor, 'floor_minus_1': floor - 1.0,
           'max_abs_ratio_minus_1': max(dev), 'median_abs_ratio_minus_1': float(np.median(dev)),
           'n_ratio_below_1_exact': sum(1 for x in rows if not x['exact_ge_1']),
           'n_ratio_below_floor': sum(1 for x in rows if x['ratio_G1_over_G2'] < floor),
           'max_G_err_rel': max(max(x['G1_err_rel'], x['G2_err_rel']) for x in rows),
           'max_direct_G_rel_diff': max(x['direct_G_rel_diff'] for x in rows), 'seconds': round(time.time() - t0, 1)}
json.dump({'summary': summary, 'rows': rows}, open(OUT, 'w'), indent=1)
print(json.dumps(summary, indent=1))
