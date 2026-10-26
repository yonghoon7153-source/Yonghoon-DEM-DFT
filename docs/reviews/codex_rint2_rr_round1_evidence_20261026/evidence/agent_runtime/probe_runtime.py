import runtime_bootstrap as boot
import json, math, random, struct, sys, warnings
from fractions import Fraction
import numpy as np
import scipy
from scipy import sparse
from scipy.sparse.linalg import cg, spsolve
import ca_ext_svcf as sv
import step3_conv_cert as cc
import step3_sigma as s3

report = {'environment': {'python': sys.version, 'numpy': np.__version__, 'scipy': scipy.__version__}}
real_next = math.nextafter
bits = lambda v: struct.pack('<d', v)
rng = random.Random(20261026)
edges = [0., -0., math.inf, -math.inf, math.nan, sys.float_info.max, -sys.float_info.max,
         sys.float_info.min, -sys.float_info.min, 5e-324, -5e-324, 1., -1.]
pairs = [(a, b) for a in edges for b in edges]
pairs += [(struct.unpack('<d', rng.getrandbits(64).to_bytes(8, 'little'))[0],
           struct.unpack('<d', rng.getrandbits(64).to_bytes(8, 'little'))[0]) for _ in range(200000)]
expected = [real_next(a, b) for a, b in pairs]
del math.nextafter
try:
    mismatches = [(a.hex(), b.hex(), got.hex(), want.hex()) for (a, b), want in zip(pairs, expected)
                  for got in [sv._nextafter(a, b)] if not (math.isnan(got) and math.isnan(want)) and bits(got) != bits(want)]
    div_bad, div_count = [], 0
    positives = [x for p in pairs[:10000] for x in p if math.isfinite(x) and x > 0.]
    for a, b in zip(positives[::2], positives[1::2]):
        exact = Fraction(a) / Fraction(b)
        lo, hi = sv._div_dir(a, b, False), sv._div_dir(a, b, True)
        div_count += 1
        good = (lo is not None and Fraction(lo) <= exact and
                (hi is None and exact > Fraction(sys.float_info.max) or hi is not None and Fraction(hi) >= exact))
        if not good: div_bad.append((a.hex(), b.hex(), lo, hi))
finally:
    math.nextafter = real_next
report['nextafter'] = {'pairs': len(pairs), 'mismatches': mismatches[:5], 'divisions': div_count, 'division_bad': div_bad[:5]}

def cert_case(n, gb_value, gt_value, p, diagonal=None):
    ix = np.arange(n)
    gb = np.full(n, gb_value, dtype=float)
    gt = np.full(n, gt_value, dtype=float)
    L = sparse.diags(gb + gt if diagonal is None else np.full(n, diagonal), format='csr')
    phi = np.full(n, p, dtype=float)
    args = (L, gb.copy(), phi, ix, gb, ix, gt)
    result = {}
    for name in ('target_bracket', 'certify'):
        try:
            with warnings.catch_warnings(record=True) as ws:
                warnings.simplefilter('always')
                if name == 'target_bracket': value = cc.target_bracket(*args)
                else:
                    value = cc.certify(L, gb.copy(), phi, 0, 0., 1e-12, ix, gb, ix, gt, 1.,
                                       lambda A, b, x0, rt: (x0.copy(), 0))
            result[name] = {k: value.get(k) for k in ('status', 'ok', 'target_ledger_ok', 'target_ledger_problem',
                                                    'target_lo', 'target_hi', 'target_kcl_raw')}
            result[name]['warnings'] = [str(w.message) for w in ws]
        except Exception as exc: result[name] = {'exception': repr(exc)}
    return result

report['overflow'] = {
    'original_5x8e307': cert_case(5, 8e307, 8e307, .5),
    'U_final_only_10x4e307': cert_case(10, 4e307, 4e307, .5),
    'W_final_only_5x3e307': cert_case(5, 3e307, 3e307, 1.),
    'hidden_ground': cert_case(1, 4e307, 4e307, .25, 1.6e308),
    'kcl_sum_stress': cert_case(100, 4e307, 1., .9),
}
report['cg_selected_native'] = s3.cg is s3._cg_scipy
gen = np.random.default_rng(20261026)
rows = []
for n in (1, 2, 3, 10, 31, 80):
    g = np.exp(gen.uniform(-6, 6, n - 1))
    d = np.r_[g, 0.] + np.r_[0., g]
    d[0] += 5.; d[-1] += 3.
    A = sparse.diags((-g, d, -g), (-1, 0, 1), shape=(n, n), format='csr')
    b = gen.normal(size=n)
    for mtype in ('identity', 'jacobi'):
        M = None if mtype == 'identity' else sparse.diags(1. / d)
        for xkind in ('none', 'exact', 'random', 'zero_rhs'):
            rhs = np.zeros(n) if xkind == 'zero_rhs' else b
            x0 = None if xkind == 'none' else spsolve(A, rhs) if xkind == 'exact' else gen.normal(size=n)
            for rt, mi in ((1e-8, n * 30), (1e-14, n * 50), (1e-12, 1)):
                counts = [0, 0]
                av, ai = s3._cg_v112(A, rhs, x0=x0, M=M, rtol=rt, maxiter=mi,
                                    callback=lambda _: counts.__setitem__(0, counts[0] + 1))
                bv, bi = cg(A, rhs, x0=x0, M=M, rtol=rt, maxiter=mi,
                            callback=lambda _: counts.__setitem__(1, counts[1] + 1))
                rows.append({'n': n, 'M': mtype, 'x0': xkind, 'rtol': rt, 'maxiter': mi,
                             'same': av.tobytes() == bv.tobytes() and ai == bi and counts[0] == counts[1],
                             'info': [int(ai), int(bi)], 'callbacks': counts})
report['cg'] = {'cases': len(rows), 'mismatches': [r for r in rows if not r['same']]}

def safe(x):
    if isinstance(x, float) and not math.isfinite(x): return repr(x)
    if isinstance(x, dict): return {k: safe(v) for k, v in x.items()}
    if isinstance(x, list): return [safe(v) for v in x]
    return x
report = safe(report)
path = boot.ROOT / 'evidence' / 'agent_runtime' / 'probe_runtime.json'
path.write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False))

