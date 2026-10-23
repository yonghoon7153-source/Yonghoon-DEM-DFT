"""R-monotone scope: (c) arm0 non-monotone inside an adjusted corner (mean8 monotone); (d) origin 3 non-monotone, mean8 monotone."""
import json, os, sys
SRC = os.environ['RINT_REVIEW_SOURCE']
sys.path.insert(0, os.path.join(SRC, 'scripts'))
import rint_r_chain as rr
LIM = (0.5, 1.0, 2.0)
KEYS = dict(zip(rr.RJ_ROLES, map(rr.rj_key, LIM)))
LADS = {law: dict(KEYS, r0_sigma=1.63e-3) for law in rr.LAWS}


def arm(s):
    return {'sigma': float(s), 'err_rel': 0.0, 'state': 'positive', 'n_sdcp_near': 0}


def run(func):
    def fetch(kit, role, law, c, key, arms, sv_cf=False):
        ids = range(arms) if isinstance(arms, int) else arms
        if kit == rr.SBE_KIT:
            return [arm(1.63e-3) for _ in ids]
        return [arm(func(rr.rj_float(key), i, c) * 1e-3) for i in ids]
    p = rr.Predict(fetch, LADS, None)
    try:
        p.run(); st = 'PREDICTED'
    except rr.Stop as e:
        st = 'STOP ' + e.code
    return st, len(p.adj), sorted({x['estimator'] for x in p.checks['r_monotone']})


base = {0.5: 5.0, 1.0: 4.7, 2.0: 4.4}
fc = lambda r, i, c: ({0.5: 4.6, 1.0: 4.7, 2.0: 4.4}[r] if i == 0 else base[r]) * (1.5 if c == '1' else 1.0)
fd = lambda r, i, c: (base[r] * 1.08 if (i in (1, 2) and r == 0.5) else
                      ({0.5: 4.4, 1.0: 4.7, 2.0: 4.4}[r] if i == 3 else base[r])) * (1.5 if c == '1' else 1.0)
print(json.dumps({'R1c arm0 4.6/4.7/4.4 (impossible order) inside adjusted corner': run(fc),
                  'R1d origin 3 4.4/4.7/4.4 inside adjusted corner (arms 1,2 raised at R_lo to force adjustment)': run(fd)}, indent=1))
