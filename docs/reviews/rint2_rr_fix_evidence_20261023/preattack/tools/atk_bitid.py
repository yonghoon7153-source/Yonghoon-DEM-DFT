"""Dump main-solve outputs for knob-off / knob-on cases (for old↔new bit comparison).  usage: atk_bitid.py <out.json>"""
import io, contextlib, json, math, os, sys
SRC = os.environ['RINT_REVIEW_SOURCE']
sys.path.insert(0, os.path.join(SRC, 'scripts'))
import numpy as np
import carbon_junction as CJ
import step3_sigma as S3
import step3_conv_cert as CC
import test_carbon_junction as T
T.CJ, T.S3 = CJ, S3


def ser(x):
    if isinstance(x, dict):
        return {str(k): ser(v) for k, v in x.items() if not str(k).startswith('_')}
    if isinstance(x, (list, tuple)):
        return [ser(v) for v in x]
    if isinstance(x, np.ndarray):
        return {'ndarray_sha': __import__('hashlib').sha256(np.ascontiguousarray(x).tobytes()).hexdigest(), 'dtype': str(x.dtype),
                'shape': list(x.shape)}
    if isinstance(x, np.generic):
        return ser(x.item())
    if isinstance(x, float):
        return repr(x)
    return x


out = {}
P = T.cat_rows(T.rows(T.SVX), T.rows(T.SVX_SDCP, phase=5, kind=0, fid0=700))
sid, _ = T.bed(P, T.SVX_N)
reg = T.registry(sid, P, tol_sj_um=.1, r_sdcp_um=.5)


def run(cj, cert, label):
    old = S3._solve_cg, S3.CONV_CERT, S3.CG_RTOL
    from scipy.sparse.linalg import spsolve
    S3._solve_cg = lambda L, b, *a, **k: (spsolve(L.tocsc(), b), 0)
    S3.CONV_CERT, S3.CG_RTOL = cert, (1e-12 if cert else old[2])
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            r = S3.solve_sigma_z(sid, T.sig_e(), T.H, z_top_um=float(T.SVX_N[2]) * T.H, z_bot_um=0.0, cjunc=cj)
    finally:
        S3._solve_cg, S3.CONV_CERT, S3.CG_RTOL = old
    out[label] = ser(r)


run(None, False, 'nocj_certoff')
run(None, True, 'nocj_certon')
run(T.plan(reg, T.SVX_RJ), False, 'cj_nosv_certoff')
run(T.plan(reg, T.SVX_RJ), True, 'cj_nosv_certon')
run(T.plan(reg, T.SVX_RJ, sv_counterfactual={'threshold': None}), False, 'cj_sv_certoff')
run(T.plan(reg, T.SVX_RJ, sv_counterfactual={'threshold': None}), True, 'cj_sv_certon')
# random small networks — certify dicts
rng = np.random.default_rng(20261023)
from scipy.sparse import csr_matrix
nets = []
for case in range(60):
    n = int(rng.integers(2, 8))
    def g(): return float((int(rng.integers(1, 17)) / 16.) * 2. ** int(rng.integers(-30, 31)))
    edges = [(i, i + 1, g()) for i in range(n - 1)] + [(i, j, g()) for i in range(n) for j in range(i + 2, n) if rng.random() < .35]
    bot = [(0, g())]; top = [(n - 1, g())]
    a = np.zeros((n, n)); b = np.zeros(n)
    for u, v, w in edges:
        a[u, u] += w; a[v, v] += w; a[u, v] -= w; a[v, u] -= w
    for i, w in bot:
        a[i, i] += w; b[i] += w
    for i, w in top:
        a[i, i] += w
    L = csr_matrix(a)
    Ab = np.array([i for i, _ in bot]); gb = np.array([w for _, w in bot]); At = np.array([i for i, _ in top]); gt = np.array([w for _, w in top])
    from scipy.sparse.linalg import spsolve
    phi = spsolve(L.tocsc(), b) * (1 + 1e-9 * rng.standard_normal(n))
    c = CC.certify(L, b, phi, 0, 1e-13, 1e-12, Ab, gb, At, gt, 1.0, lambda L_, b_, x0, rt: (np.asarray(x0), 0))
    nets.append(ser(c))
out['certify_random60'] = nets
json.dump(out, open(sys.argv[1], 'w'), indent=0, sort_keys=True)
print('ok', len(out))
