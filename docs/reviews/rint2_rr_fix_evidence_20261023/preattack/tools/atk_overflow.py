"""Fuzz certify/target_bracket with extreme magnitudes: exceptions (not warnings) are the claim under test."""
import json, math, os, sys, warnings
SRC = os.environ['RINT_REVIEW_SOURCE']
sys.path.insert(0, os.path.join(SRC, 'scripts'))
import numpy as np
from scipy.sparse import csr_matrix
import step3_conv_cert as CC

warnings.simplefilter('ignore')
rng = np.random.default_rng(7)
exc, statuses, n = [], {}, 0
for case in range(3000):
    nn = int(rng.integers(1, 7))
    def g():
        return float(rng.choice([1e-300, 1e-200, 1e-50, 1.0, 1e50, 1e200, 1e300, 8e307, 1.7e308]) * rng.uniform(0.5, 1.0))
    edges = [(i, i + 1, g()) for i in range(nn - 1)] + [(i, j, g()) for i in range(nn) for j in range(i + 2, nn) if rng.random() < .3]
    bot = [(0, g())] + ([(int(rng.integers(nn)), g())] if rng.random() < .3 else [])
    top = [(nn - 1, g())] + ([(int(rng.integers(nn)), g())] if rng.random() < .3 else [])
    a = np.zeros((nn, nn)); b = np.zeros(nn)
    with np.errstate(all='ignore'):
        for u, v, w in edges:
            a[u, u] += w; a[v, v] += w; a[u, v] -= w; a[v, u] -= w
        for i, w in bot:
            a[i, i] += w; b[i] += w
        for i, w in top:
            a[i, i] += w
    L = csr_matrix(a)
    Ab = np.array([i for i, _ in bot]); gb = np.array([w for _, w in bot]); At = np.array([i for i, _ in top]); gt = np.array([w for _, w in top])
    phi = rng.choice([0.5, 1.0, 0.0, -1e150, 1e150, 1e300, -1e300, 1e-320], nn) * rng.uniform(0.5, 1.5, nn)
    n += 1
    try:
        c = CC.certify(L, b, phi, 0, 1e-13, 1e-12, Ab, gb, At, gt, float(rng.choice([1.0, 1e300, 1e-300])),
                       lambda L_, b_, x0, rt: (np.asarray(x0), 0))
        statuses[c["status"] + "|" + str(c.get("target_ledger_problem"))[:22]] = statuses.get(c["status"] + "|" + str(c.get("target_ledger_problem"))[:22], 0) + 1
        if c['status'] == CC.STATUS_POSITIVE and c['ok']:
            # independent sanity: posted G must be finite positive
            if not (math.isfinite(c['I_bot']) and c['I_bot'] > 0):
                exc.append(['ok-but-nonfinite', case])
    except Exception as e:  # noqa
        exc.append([case, type(e).__name__, str(e)[:160]])
print(json.dumps({'cases': n, 'exceptions': len(exc), 'examples': exc[:5], 'statuses': statuses}))
