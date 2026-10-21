"""Replay Codex RCA-07 counterexamples against a given scripts/ dir (argv[1])."""
import json
import sys

import numpy as np

sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1])
from scipy.sparse import csr_matrix  # noqa: E402
import step3_conv_cert as cert  # noqa: E402
import step3_sigma as s3  # noqa: E402


def chain(which):
    k = np.array([0.03542843081279895, 21.113990671509995, 0.20370714955448593,
                  0.000808971961390796, 0.06976120349186236, 1.6912757790891766,
                  0.021238765753829096, 0.0007609288395839504, 0.20701635367585214,
                  0.004052240218237343, 31752.40122359974, 0.00015528936294781815,
                  2.8720471611538324e-05, 0.33794145566284794, 0.035436507440546515,
                  5.089363857396167, 0.0020462968348843712, 4.924555717512331,
                  0.10125977682414762, 1.3150225184986553, 1.1619900367249028,
                  9.217092548952976e-05, 3.113347553856885e-05, 225.4217993099028])
    G = 6507979.172281959
    bridge_factor = None
    if which == 'main':
        k = np.array([3.9749047010591427, 0.006535081136400995, 0.003293084534476289,
                      22992.948551542082, 0.00035278660732561336, 0.0004798389751913557,
                      1339.2933113393337, 70807.2008252101, 0.4385075410195556,
                      3.1577098692370925e-05, 84788.55607773518])
        G = 20815016.44294986
        k = k / 16384
        G = G / 16384
    if which == 'connected':
        k = np.array([0.1036251621769631, 77264.71177376187, 115.83302628384007,
                      188.05389893808805, 15.658598399603378, 7.184589096729567e-05, 0.004872796993466964])
        G = 36509171569.75918
        bridge_factor = 0.0009451405762888877 / float(k.min())
        k = k / (2 ** 25)
        G = G / (2 ** 25)
    n = len(k) - 1
    a = np.zeros((n + 1, n + 1))
    b = np.zeros(n + 1)
    a[0, 0] = k[0]
    a[n - 1, n - 1] = k[-1]
    a[n, n] = G
    b[0] = k[0]
    b[n] = G
    for i in range(n - 1):
        a[i, i] += k[i + 1]
        a[i + 1, i + 1] += k[i + 1]
        a[i, i + 1] -= k[i + 1]
        a[i + 1, i] -= k[i + 1]
    eps = 0. if bridge_factor is None else float(k.min() * bridge_factor)
    if eps:
        a[n, n] += eps
        a[0, 0] += eps
        a[n, 0] -= eps
        a[0, n] -= eps
    L = csr_matrix(a)
    k_eff = k.copy()
    k_eff[0] += G * eps / (G + eps)
    true = 1 / np.sum(1 / k_eff)
    return L, b, n, k, G, true


s3.GPU_SOLVE = False
s3.AMG_SOLVE = False
s3.CG_MAXITER = 1000
out = {}
for which in ('main', 'connected', 'iter23'):
    L, b, n, k, G, true = chain(which)
    phi, info = s3._solve_cg(L, b, rtol=1e-12)
    resid = float(np.linalg.norm(L @ phi - b) / np.linalg.norm(b))
    c = cert.certify(L, b, phi, int(info), resid, 1e-12, np.array([0, n]), np.array([k[0], G]), np.array([n - 1]),
                     np.array([k[-1]]), 1.0, lambda LL, bb, xx, rt: s3._solve_cg(LL, bb, x0=xx, rtol=rt))
    out[which] = {'true': true, 'rel_err': c['sigma'] / true - 1,
                  **{kk: c.get(kk) for kk in ('pass_a', 'pass_b', 'pass_c', 'pass_d', 'ok', 'status', 'imbalance',
                                              'target_lo', 'target_hi', 'target_err_bound_rel', 'target_width_rel',
                                              'target_in_bracket')}}
print(json.dumps(out, indent=1, default=str))
