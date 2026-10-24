import sys, warnings, numpy as np, scipy
from scipy import sparse
from scipy.sparse.linalg import cg, spsolve
sys.path.insert(0, sys.argv[1] + '/scripts')
import test_step3_conv_cert as T          # reuse the same _lap
rng = np.random.default_rng(9)
L, b = T._lap(500, rng)
xs = spsolve(L.tocsc(), b)
diag = L.diagonal(); M = sparse.diags(1.0 / diag)
r0 = np.linalg.norm(b - L @ xs); bn = np.linalg.norm(b)
print('scipy', scipy.__version__, '| |r0|', r0, '|b|', bn, '|r0|/|b|', r0 / bn)
for label, kw in (('tol only (legacy atol)', dict(tol=1e-14)), ('tol + atol=0', dict(tol=1e-14, atol=0.0))):
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        try:
            x, info = cg(L, b, x0=xs, maxiter=30000, M=M, **kw)
        except TypeError as e:
            print(label, 'TypeError', e); continue
    print(f'{label:24s} info={info} maxdiff/max={np.max(np.abs(x - xs)) / np.max(np.abs(xs)):.3e} |r|/|b|={np.linalg.norm(b - L @ x) / bn:.3e}')
try:
    x, info = cg(L, b, x0=xs, rtol=1e-14, maxiter=30000, M=M)
    print(f'{"rtol=1e-14":24s} info={info} maxdiff/max={np.max(np.abs(x - xs)) / np.max(np.abs(xs)):.3e}')
except TypeError as e:
    print('rtol kw: TypeError', e)
