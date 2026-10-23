"""Q9 design attacks (no implementation exists — emulate the design's merge = Predict.run with key-lookup fetch over unit runs)."""
import json, os, sys
SRC = os.environ['RINT_REVIEW_SOURCE']
sys.path.insert(0, os.path.join(SRC, 'scripts'))
import rint_r_chain as rr

LIM = (0.5, 1.0, 2.0)
KEYS = dict(zip(rr.RJ_ROLES, map(rr.rj_key, LIM)))
LADS = {law: dict(KEYS, r0_sigma=1.63e-3) for law in rr.LAWS}


def arm(s, err=0.0):
    return {'sigma': float(s), 'err_rel': float(err), 'state': 'positive', 'n_sdcp_near': 0}


def unit_runs(sig, noop_sigma=1.63e-3, nc_at=None):
    """All runs the 12 units would produce (design §3-1): per (c, law, R): corner arm0 (+SV) + origin arms 1,2;
    SBE no-op per law attached to (c1, law, R_j0).  nc_at = key whose corner read raises NOT_COMPUTED (e.g. ELECTRODE_SHORT)."""
    runs = {}
    for law in rr.LAWS:
        runs[('sbe_noop', rr.SBE_KIT, law, '1', LADS[law]['R_j0'], (0,))] = [arm(noop_sigma)]
        for role in rr.RJ_ROLES:
            for c in rr.CS:
                key = LADS[law][role]
                runs[('corner', rr.DBE_KIT, law, c, key, (0,))] = ('NC' if nc_at == (c, law, role) else [arm(sig(c, law, role, 0))])
                runs[('origin', rr.DBE_KIT, law, c, key, (1, 2))] = [arm(sig(c, law, role, i)) for i in (1, 2)]
    return runs


def merge(runs):
    used = []

    def fetch(kit, role, law, c, key, arms, sv_cf=False):
        idx = tuple(range(arms)) if isinstance(arms, int) else tuple(sorted(arms))
        k = (role, kit, law, c, key, idx)
        if k not in runs:
            raise rr.Stop('UNIT_MISSING', f'{k}')
        used.append(k)
        v = runs[k]
        if v == 'NC':
            raise rr.Stop('NOT_COMPUTED', 'ELECTRODE_SHORT (emulated read_run)')
        return v
    p = rr.Predict(fetch, LADS, None)
    try:
        p.run()
        st = 'PREDICTED'
    except rr.Stop as e:
        st = e.code
    extra = [k for k in runs if k not in used]
    return st, len(used), len(extra), extra[:3]


base = {'R_j_lo': 5.0, 'R_j0': 4.7, 'R_j_hi': 4.4}
sig = lambda c, law, role, i: base[role] * (1.2 if c == '1' else 1.0) * 1e-3
out = {}
st, nu, ne, ex = merge(unit_runs(sig))
out['D0 normal'] = {'predict': st, 'used': nu, 'unused': ne}
st, nu, ne, ex = merge(unit_runs(sig, nc_at=('0', 'P0', 'R_j_lo')))
out['D1 first corner NOT_COMPUTED (registered outcome in the single-machine chain)'] = {
    'predict status (emulated merge replay)': st, 'runs used': nu, 'runs NOT used (design: UNIT_EXTRA stop?)': ne, 'example unused': ex}
# D3: SBE no-op compares bitwise to the ladder R_j0 sigma — a no-op unit on another machine (bits differ ~1e-10)
st, nu, ne, ex = merge(unit_runs(sig, noop_sigma=1.63e-3 * (1 + 2e-10)))
out['D3 no-op sigma differs by 2e-10 rel (another machine)'] = {'predict': st, 'used': nu, 'unused': ne}
print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
