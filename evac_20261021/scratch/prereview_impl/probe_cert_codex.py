# -*- coding: utf-8 -*-
"""탐침 B1 (RCA-07 · 13) — Codex 10-21 수렴 반례 (convergence_probes.py 의 망 그대로) 를 HEAD 증서 (ⓐ–ⓓ · 상태) 에 넣는다.
OPENBLAS_CORETYPE 은 부르는 쪽 환경이 정한다 (기본 = 이 기계 · Haswell = Codex 경로).  결과 = JSON (환경 이름 꼬리)."""
import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pcommon  # noqa: F401  (sys.path)
import numpy as np
from fractions import Fraction
from scipy.sparse import csr_matrix
import step3_conv_cert as cert
import step3_sigma as s3


def chain_case(kind):
    k = np.array([0.03542843081279895, 21.113990671509995, 0.20370714955448593, 0.000808971961390796, 0.06976120349186236,
                  1.6912757790891766, 0.021238765753829096, 0.0007609288395839504, 0.20701635367585214, 0.004052240218237343,
                  31752.40122359974, 0.00015528936294781815, 2.8720471611538324e-05, 0.33794145566284794, 0.035436507440546515,
                  5.089363857396167, 0.0020462968348843712, 4.924555717512331, 0.10125977682414762, 1.3150225184986553,
                  1.1619900367249028, 9.217092548952976e-05, 3.113347553856885e-05, 225.4217993099028])
    G = 6507979.172281959
    bridge_factor = None
    if kind == 'small':
        k = np.array([3.9749047010591427, 0.006535081136400995, 0.003293084534476289, 22992.948551542082, 0.00035278660732561336,
                      0.0004798389751913557, 1339.2933113393337, 70807.2008252101, 0.4385075410195556, 3.1577098692370925e-05,
                      84788.55607773518])
        G = 20815016.44294986
        k = k / 16384; G = G / 16384
    if kind == 'connected':
        k = np.array([0.1036251621769631, 77264.71177376187, 115.83302628384007, 188.05389893808805, 15.658598399603378,
                      7.184589096729567e-05, 0.004872796993466964])
        G = 36509171569.75918
        bridge_factor = 0.0009451405762888877 / float(k.min())
        k = k / (2 ** 25); G = G / (2 ** 25)
    n = len(k) - 1
    a = np.zeros((n + 1, n + 1)); b = np.zeros(n + 1)
    a[0, 0] = k[0]; a[n - 1, n - 1] = k[-1]; a[n, n] = G; b[0] = k[0]; b[n] = G
    for i in range(n - 1):
        a[i, i] += k[i + 1]; a[i + 1, i + 1] += k[i + 1]
        a[i, i + 1] -= k[i + 1]; a[i + 1, i] -= k[i + 1]
    eps = 0. if bridge_factor is None else float(k.min() * bridge_factor)
    if eps:
        a[n, n] += eps; a[0, 0] += eps
        a[n, 0] -= eps; a[0, n] -= eps
    L = csr_matrix(a)
    s3.GPU_SOLVE = False; s3.AMG_SOLVE = False; s3.CG_MAXITER = 1000
    phi, info = s3._solve_cg(L, b, rtol=1e-12)
    resid = float(np.linalg.norm(L @ phi - b) / np.linalg.norm(b))
    c = cert.certify(L, b, phi, int(info), resid, 1e-12, np.array([0, n]), np.array([k[0], G]), np.array([n - 1]),
                     np.array([k[-1]]), 1., lambda LL, bb, xx, rt: s3._solve_cg(LL, bb, x0=xx, rtol=rt))
    k_eff = k.copy()
    k_eff[0] += G * eps / (G + eps)
    true = float(Fraction(1) / sum(Fraction(float(x)) ** -1 for x in k_eff)) if not eps else float(1 / np.sum(1 / k_eff))
    lo, hi = c.get('target_lo'), c.get('target_hi')
    return {'kind': kind, 'true_G': true, 'posted_G': c.get('I_bot'), 'rel_err': c.get('I_bot') / true - 1.0,
            'pass_a': c['pass_a'], 'pass_b': c['pass_b'], 'pass_c': c['pass_c'], 'pass_d': c.get('pass_d'), 'ok': c['ok'],
            'status': c.get('status'), 'imbalance': c.get('imbalance'), 'lo': lo, 'hi': hi,
            'true_in_bracket': (None if lo is None or hi is None else bool(lo <= true <= hi)),
            'err_bound_rel': c.get('target_err_bound_rel'), 'width_rel': c.get('target_width_rel'), 'why': c.get('target_why')}


def warm_candidate():
    G = 1e15
    L = csr_matrix([[2., -1., 0.], [-1., 2., 0.], [0., 0., G]])
    b = np.array([1., 0., G])
    p = np.array([.75, .25, 1.])
    resid = float(np.linalg.norm(L @ p - b) / np.linalg.norm(b))
    c = cert.certify(L, b, p, 0, resid, 1e-12, np.array([0, 2]), np.array([1., G]), np.array([1]), np.array([1.]), 1.,
                     lambda LL, bb, xx, rt: s3._solve_cg(LL, bb, x0=xx, rtol=rt))
    return {'true_G': 1 / 3, 'posted_G': c.get('I_bot'), 'pass_a': c['pass_a'], 'pass_b': c['pass_b'], 'pass_c': c['pass_c'],
            'pass_d': c.get('pass_d'), 'ok': c['ok'], 'status': c.get('status'), 'lo': c.get('target_lo'),
            'hi': c.get('target_hi'), 'why': c.get('target_why')}


def valid_zero():
    from scipy.sparse import diags
    L = diags([1., 1.], format='csr')
    b = np.array([1., 0.]); p = b.copy()
    c = cert.certify(L, b, p, 0, 0., 1e-12, np.array([0]), np.array([1.]), np.array([1]), np.array([1.]), 1.,
                     lambda LL, bb, xx, rt: s3._solve_cg(LL, bb, x0=xx, rtol=rt))
    return {'status': c.get('status'), 'ok': c['ok'], 'pass_a': c['pass_a'], 'pass_b': c['pass_b'], 'pass_c': c['pass_c'],
            'pass_d': c.get('pass_d'), 'zero_exact': c.get('zero_exact'), 'why': c.get('target_why')}


env = os.environ.get('OPENBLAS_CORETYPE', 'default')
import numpy  # noqa: E402
try:
    from threadpoolctl import threadpool_info
    tp = [{'internal_api': x.get('internal_api'), 'architecture': x.get('architecture'), 'num_threads': x.get('num_threads')}
          for x in threadpool_info()]
except Exception as e:                                          # noqa: BLE001
    tp = f'threadpoolctl 없음 ({type(e).__name__})'
out = {'env_OPENBLAS_CORETYPE': env, 'threadpool': tp, 'numpy': numpy.__version__,
       'main': chain_case('main'), 'small': chain_case('small'), 'connected': chain_case('connected'),
       'warm_candidate': warm_candidate(), 'valid_zero': valid_zero()}
print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f'probe_cert_codex_{env}.json'), 'w', encoding='utf-8') as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1, default=str)
