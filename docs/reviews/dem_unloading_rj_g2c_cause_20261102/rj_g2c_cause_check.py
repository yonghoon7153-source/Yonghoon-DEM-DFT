#!/usr/bin/env python3
"""RJ 323957 G2c cause check (read-only, stdlib only, NOT a verdict).

Tests two source-derived mechanisms on the two existing contact dumps plus the
RJ R-stage full-precision atom dump written at the same setup:
  M1  periodic `restart N` file stores pair contact history from pre_exchange
      (before the step's pair compute); the in-run dump used the updated history.
      Prediction for sticking pairs: dFt(test-orig) = kt*dt*vtr  (tangential column).
  M2  in-run output evaluates ghost atoms with half-step v/omega (no forward comm
      after final_integrate). Prediction (original ghost pairs only, normal column):
      dFn(test-orig, on lower id a, along e_ab) = -gamma_n*(0.5*dt*f_a/m_a . e_ab).
Writes nothing; prints one JSON object. Exit 0 = complete breakdown, 2 = refused/incomplete.
"""
import array
import hashlib
import heapq
import json
import math
import os
import re
import sys
from decimal import Decimal
from pathlib import Path

REL = 1e-5
BOX = 0.05
DT = 1.0e-6
MU = 0.5
E_REST = 0.3
CHARVEL = 2.0
YM = {1: 1.4e8, 2: 1.4e8, 3: 1.35e6}
NU = {1: 0.25, 2: 0.25, 3: 0.30}
ORIG_GRID = (6, 4)      # r8 log line 29: "6 by 4 by 1 MPI processor grid"
TEST_GRIDS = [(3, 2), (2, 3), (6, 1), (1, 6)]   # candidates for NP 6 (informational only)
COLUMNS = ['c_cpl[%d]' % i for i in range(1, 27)]
PERIODIC = {0, 1, 3, 4, 17, 18}
ATOM_COLS = ['id', 'type', 'x', 'y', 'z', 'radius', 'mass', 'vx', 'vy', 'vz',
             'omegax', 'omegay', 'omegaz', 'fx', 'fy', 'fz']
MAX_ROWS = 600000
MAX_LINE = 8192
MAX_BYTES = 512 * 1024 * 1024
SHIFT = 1 << 20


def require(cond, msg):
    if not cond:
        raise ValueError(msg)


def exact_id(tok):
    if re.fullmatch(r'[+-]?[0-9]+', tok):
        v = int(tok)
    else:
        f = float(tok)
        require(math.isfinite(f) and f.is_integer(), 'invalid ID ' + tok)
        require(Decimal(tok) == Decimal(int(f)), 'fractional ID ' + tok)
        v = int(f)
    require(0 < v < SHIFT, 'ID out of range ' + tok)
    return v


def sig(st):
    return (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns)


class Reader:
    def __init__(self, path):
        self.path = Path(path)
        self.h = hashlib.sha256()
        self.f = open(self.path, 'rb')
        self.before = os.fstat(self.f.fileno())
        require(self.before.st_size <= MAX_BYTES, '%s exceeds byte cap' % path)

    def raw(self):
        b = self.f.readline(MAX_LINE + 1)
        require(len(b) <= MAX_LINE, 'line exceeds cap')
        if b:
            self.h.update(b)
        return b

    def line(self):
        b = self.raw()
        require(bool(b), '%s: unexpected EOF' % self.path)
        return b.decode('utf-8').rstrip('\r\n')

    def close(self, meta):
        after = os.fstat(self.f.fileno())
        self.f.close()
        require(sig(self.before) == sig(after) == sig(os.stat(self.path)), 'file changed while reading')
        meta.update(path=str(self.path), bytes=self.before.st_size, sha256=self.h.hexdigest(),
                    stat_signature=list(sig(self.before)))


def header(rd, expect_step, count_item, body_prefix):
    require(rd.line() == 'ITEM: TIMESTEP', 'TIMESTEP header')
    step = int(rd.line())
    require(step == expect_step, 'step %d != %d' % (step, expect_step))
    require(rd.line() == count_item, 'count header')
    n = int(rd.line())
    require(0 < n <= MAX_ROWS, 'row count outside limit')
    bh = rd.line().split()
    require(bh[:3] == ['ITEM:', 'BOX', 'BOUNDS'] and not {'xy', 'xz', 'yz'} & set(bh[3:]), 'BOX header')
    for _ in range(3):
        lo, hi = map(float, rd.line().split())
        require(math.isfinite(lo) and math.isfinite(hi) and lo < hi, 'BOX bounds')
    cols = rd.line().split()
    require(cols[:2] == body_prefix, 'body header')
    return step, n, cols[2:]


def normalized(v, rev):
    if rev:
        v = v[3:6] + v[:3] + v[6:9] + [-x for x in v[9:18]] + v[18:]
    r = v[:6] + v[9:18] + v[21:26]
    for c in PERIODIC:
        r[c] %= BOX
    return r


def contact_rows(path, meta, step):
    rd = Reader(path)
    _, n, cols = header(rd, step, 'ITEM: NUMBER OF ENTRIES', ['ITEM:', 'ENTRIES'])
    require(cols == COLUMNS, 'contact columns')
    count = 0
    while True:
        b = rd.raw()
        if not b:
            break
        t = b.decode('utf-8').split()
        if not t:
            continue
        require(t[0] != 'ITEM:', 'multiple frames')
        require(len(t) == 26, 'row width')
        i, j = exact_id(t[6]), exact_id(t[7])
        require(i != j, 'self pair')
        vals = [float(x) for x in t]
        require(all(map(math.isfinite, vals)), 'nonfinite')
        count += 1
        require(count <= n, 'more rows than declared')
        lo, hi = (i, j) if i < j else (j, i)
        yield lo * SHIFT + hi, normalized(vals, i > j), i > j, t
    require(count == n, 'row count %d != %d' % (count, n))
    rd.close(meta)
    meta.update(rows=count, step=step)


def read_atoms(path, meta, step):
    rd = Reader(path)
    _, n, cols = header(rd, step, 'ITEM: NUMBER OF ATOMS', ['ITEM:', 'ATOMS'])
    pos = [cols.index(c) for c in ATOM_COLS]
    index, typ, data = {}, bytearray(), array.array('d')
    while True:
        b = rd.raw()
        if not b:
            break
        t = b.decode('utf-8').split()
        if not t:
            continue
        require(t[0] != 'ITEM:', 'multiple frames')
        require(len(t) == len(cols), 'atom row width')
        aid = exact_id(t[pos[0]])
        require(aid not in index, 'duplicate atom id')
        ty = int(t[pos[1]])
        require(ty in YM, 'unknown type')
        vals = [float(t[k]) for k in pos[2:]]
        require(all(map(math.isfinite, vals)), 'nonfinite atom value')
        index[aid] = len(typ)
        typ.append(ty)
        data.extend(vals)
    require(len(typ) == n, 'atom count')
    rd.close(meta)
    meta.update(atoms=n, step=step)
    return index, typ, data


def cell(x, y, grid):
    nx, ny = grid
    ix = sum(1 for k in range(1, nx) if x >= 0.0 + BOX * (k * (1.0 / nx)))
    iy = sum(1 for k in range(1, ny) if y >= 0.0 + BOX * (k * (1.0 / ny)))
    amb = (min([abs(x - BOX * (k * (1.0 / nx))) for k in range(0, nx + 1)]) < 1e-12 or
           min([abs(y - BOX * (k * (1.0 / ny))) for k in range(0, ny + 1)]) < 1e-12)
    return ix, iy, amb


def fin(x):
    return x if isinstance(x, float) and math.isfinite(x) else None


def res6(v):
    return 0.0 if v == 0 else 0.5 * 10.0 ** (math.floor(math.log10(abs(v))) - 5)


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def norm(a):
    return math.sqrt(dot(a, a))


def mimage(d):
    return d - BOX * round(d / BOX)


def model(ta, tb, ra, rb, ma, mb):
    ye = 1.0 / ((1.0 - NU[ta] ** 2) / YM[ta] + (1.0 - NU[tb] ** 2) / YM[tb])
    reff = ra * rb / (ra + rb)
    meff = ma * mb / (ma + mb)
    sq = math.sqrt(reff)
    kn = 16.0 / 15.0 * sq * ye * (15.0 * meff * CHARVEL * CHARVEL / (16.0 * sq * ye)) ** 0.2
    lg = math.log(E_REST)
    gn = math.sqrt(4.0 * meff * kn / (1.0 + (math.pi / lg) * (math.pi / lg)))
    return kn, gn


def quant(arr, qs=(0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99)):
    if not len(arr):
        return None
    s = sorted(arr)
    n = len(s)
    out = {'n': n, 'min': s[0], 'max': s[-1]}
    for q in qs:
        out['q%02d' % round(q * 100)] = s[min(n - 1, int(q * (n - 1) + 0.5))]
    return out


class Fit:
    """pooled through-origin regression obs ~ k*pred over vector components"""
    def __init__(self):
        self.n = 0
        self.sop = self.spp = self.soo = self.sres = 0.0
        self.within10 = 0
        self.cos = array.array('d')
        self.ratio = array.array('d')

    def add(self, obs, pred):
        self.n += 1
        self.sop += dot(obs, pred)
        self.spp += dot(pred, pred)
        self.soo += dot(obs, obs)
        d = [obs[k] - pred[k] for k in range(3)]
        self.sres += dot(d, d)
        no, npd = norm(obs), norm(pred)
        self.within10 += norm(d) <= 0.1 * no
        if no > 0 and npd > 0:
            self.cos.append(dot(obs, pred) / (no * npd))
            self.ratio.append(no / npd)

    def out(self):
        if not self.n or not self.spp or not self.soo:
            return {'n': self.n}
        k = self.sop / self.spp
        r2 = 1.0 - (self.soo - 2 * k * self.sop + k * k * self.spp) / self.soo
        return {'n': self.n, 'slope_obs_on_pred': k, 'r2_through_origin': r2,
                'r2_unit_slope': 1.0 - self.sres / self.soo,
                'frac_resid_le_10pct': self.within10 / self.n,
                'cos': quant(self.cos), 'ratio_obs_over_pred': quant(self.ratio)}


class Scalar:
    def __init__(self):
        self.n = self.same_sign = 0
        self.sop = self.spp = self.soo = 0.0

    def add(self, o, p):
        self.n += 1
        self.same_sign += (o > 0) == (p > 0)
        self.sop += o * p
        self.spp += p * p
        self.soo += o * o

    def out(self):
        if not self.n or not self.spp or not self.soo:
            return {'n': self.n}
        k = self.sop / self.spp
        return {'n': self.n, 'sign_agreement': self.same_sign / self.n, 'slope_obs_on_pred': k,
                'r2_through_origin': 1.0 - (self.soo - 2 * k * self.sop + k * k * self.spp) / self.soo}


def analyze(orig, test, atoms, step=3200000):
    prov = {'original': {}, 'test': {}, 'atoms': {}}
    idx, data, rev_o, tok_o = {}, array.array('d'), bytearray(), []
    for key, comp, rev, _ in contact_rows(orig, prov['original'], step):
        require(key not in idx, 'original duplicate pair')
        idx[key] = len(rev_o)
        data.extend(comp)
        rev_o.append(rev)
    n = len(rev_o)
    med = []
    for c in range(20):
        col = sorted(abs(data[k]) for k in range(c, len(data), 20))
        med.append(col[n // 2] if n % 2 else 0.5 * (col[n // 2 - 1] + col[n // 2]))
    have_atoms = atoms is not None and Path(atoms).is_file()
    if have_atoms:
        aidx, atyp, adat = read_atoms(atoms, prov['atoms'], step)
    seen = bytearray(n)
    fam = {'pos': (0, 6), 'total': (6, 9), 'normal': (9, 12), 'tangent': (12, 15), 'area': (15, 16),
           'delta': (16, 17), 'cpoint': (17, 20)}
    tables = {}

    def bump(name, *keys):
        t = tables.setdefault(name, {})
        k = '|'.join(str(x) for x in keys)
        t[k] = t.get(k, 0) + 1

    mismatch = 0
    rt, rn = array.array('d'), array.array('d')
    reset_like = sign_flip_like = 0
    fit = {'local_stick': Fit(), 'ghost_stick': Fit()}
    contrast_cos_Ft = array.array('d')
    m1_pred_fail = {'local': [0, 0], 'ghost': [0, 0]}
    m2 = {'ghost': Scalar(), 'local': Scalar()}
    switch_ratio = array.array('d')
    ghost_not_reversed = 0
    test_grid_viol = {'%dx%d' % g: 0 for g in TEST_GRIDS}
    top = []
    for key, comp_t, rev_t, _ in contact_rows(test, prov['test'], step):
        require(key in idx, 'extra test pair')
        k = idx[key]
        require(not seen[k], 'test duplicate pair')
        seen[k] = 1
        o = data[20 * k:20 * k + 20]
        failed = set()
        for c in range(20):
            d = abs(o[c] - comp_t[c])
            if c in PERIODIC:
                d = min(d, BOX - d)
            if d > REL * max(abs(o[c]), med[c]):
                for f, (lo, hi) in fam.items():
                    if lo <= c < hi:
                        failed.add(f)
        mismatch += bool(failed)
        fn_fail, ft_fail, tot_fail = 'normal' in failed, 'tangent' in failed, 'total' in failed
        Fn_o, Ft_o = o[9:12], o[12:15]
        Fn_t, Ft_t = comp_t[9:12], comp_t[12:15]
        dFt = [Ft_t[c] - Ft_o[c] for c in range(3)]
        dFn = [Fn_t[c] - Fn_o[c] for c in range(3)]
        nFt, nFn = norm(Ft_o), norm(Fn_o)
        if nFt > 0:
            rt.append(norm(dFt) / nFt)
            reset_like += norm(dFt) > 0.5 * nFt
            sign_flip_like += norm([Ft_t[c] + Ft_o[c] for c in range(3)]) < 0.1 * nFt
        if nFn > 0:
            rn.append(norm(dFn) / nFn)
        s_o = nFt / (MU * nFn) if nFn > 0 else float('inf')
        s_t = norm(Ft_t) / (MU * norm(Fn_t)) if norm(Fn_t) > 0 else float('inf')
        # sliding branch => |Ft| = mu*|Fn| exactly (no damping); sticking may exceed it (damping added after the test)
        slide_o, slide_t = abs(s_o - 1.0) <= 1e-4, abs(s_t - 1.0) <= 1e-4
        bump('slide_orig_test_x_tangent_fail', int(slide_o), int(slide_t), int(ft_fail))
        bump('orient_changed_x_normal_fail', int(rev_o[k] != rev_t), int(fn_fail))
        bump('orient_orig_reversed_x_normal_fail', int(rev_o[k]), int(fn_fail))
        if not have_atoms:
            continue
        a, b = key // SHIFT, key % SHIFT
        require(a in aidx and b in aidx, 'pair atom missing from atom dump')
        ia, ib = aidx[a], aidx[b]
        A, B = adat[14 * ia:14 * ia + 14], adat[14 * ib:14 * ib + 14]
        ta, tb = atyp[ia], atyp[ib]
        xa, xb = A[0:3], B[0:3]
        ca, cb = cell(xa[0] % BOX, xa[1] % BOX, ORIG_GRID), cell(xb[0] % BOX, xb[1] % BOX, ORIG_GRID)
        amb = ca[2] or cb[2]
        ghost = ca[:2] != cb[:2]
        gclass = 'ambiguous' if amb else ('ghost' if ghost else 'local')
        if gclass == 'ghost' and not rev_o[k]:
            ghost_not_reversed += 1
        for g in TEST_GRIDS:
            if (cell(xa[0] % BOX, xa[1] % BOX, g)[:2] != cell(xb[0] % BOX, xb[1] % BOX, g)[:2]) and not rev_t:
                test_grid_viol['%dx%d' % g] += 1
        bump('ghost_orig_x_fail_normal_tangent_total', gclass, int(fn_fail), int(ft_fail), int(tot_fail))
        bump('pairtype_x_ghost_x_normal_fail', '%d%d' % tuple(sorted((ta, tb))), gclass, int(fn_fail))
        dl = [mimage(xa[0] - xb[0]), mimage(xa[1] - xb[1]), xa[2] - xb[2]]
        r = norm(dl)
        require(r > 0, 'coincident pair atoms')
        e = [x / r for x in dl]
        ra, rb, ma, mb = A[3], B[3], A[4], B[4]
        va, vb, wa, wb, fa = A[5:8], B[5:8], A[8:11], B[8:11], A[11:14]
        vr = [va[c] - vb[c] for c in range(3)]
        vn = dot(vr, e)
        vt = [vr[c] - vn * e[c] for c in range(3)]
        dn = ra + rb - r
        cri, crj = ra - 0.5 * dn, rb - 0.5 * dn
        wr = [(cri * wa[c] + crj * wb[c]) / r for c in range(3)]
        vtr = [vt[0] - (dl[2] * wr[1] - dl[1] * wr[2]),
               vt[1] - (dl[0] * wr[2] - dl[2] * wr[0]),
               vt[2] - (dl[1] * wr[0] - dl[0] * wr[1])]
        kt, gam = model(ta, tb, ra, rb, ma, mb)
        p = [kt * DT * x for x in vtr]
        floor_t = math.sqrt(sum(res6(Ft_o[c]) ** 2 + res6(Ft_t[c]) ** 2 for c in range(3)))
        floor_n = math.sqrt(sum(res6(Fn_o[c]) ** 2 + res6(Fn_t[c]) ** 2 for c in range(3)))
        if gclass != 'ambiguous':
            pf = any(abs(p[c]) > REL * max(abs(Ft_o[c]), med[12 + c]) for c in range(3))
            m1_pred_fail[gclass][0] += pf
            m1_pred_fail[gclass][1] += 1
            bump('m1_predicted_fail_x_observed_tangent_fail', gclass, int(pf), int(ft_fail))
        if not slide_o and not slide_t and gclass != 'ambiguous' and norm(dFt) > 10 * floor_t:
            fit['%s_stick' % gclass].add(dFt, p)
            if gclass == 'local' and nFt > 0:
                contrast_cos_Ft.append(dot(dFt, Ft_o) / (norm(dFt) * nFt))
        if slide_o != slide_t and norm(vtr) > 0:
            switch_ratio.append(norm(dFt) / (gam * norm(vtr)))
        dfn_obs = dot(dFn, e)
        if gclass != 'ambiguous' and abs(dfn_obs) > 10 * floor_n:
            dv = [0.5 * DT * fa[c] / ma for c in range(3)]
            m2[gclass].add(dfn_obs, -gam * dot(dv, e))
        item = (norm(dFt), a, b)
        rec = dict(pair=[a, b], types=[ta, tb], ghost_orig=gclass, s_orig=fin(s_o), s_test=fin(s_t),
                   Ft_orig=nFt, dFt=norm(dFt), dFn=norm(dFn), m1_pred=norm(p), damping_scale=gam * norm(vtr),
                   cos_dFt_pred=(dot(dFt, p) / (norm(dFt) * norm(p))) if norm(dFt) and norm(p) else None)
        if len(top) < 20:
            heapq.heappush(top, (item, json.dumps(rec)))
        elif item > top[0][0]:
            heapq.heapreplace(top, (item, json.dumps(rec)))
    require(all(seen), 'missing test pairs')
    out = dict(status='COMPLETE_CAUSE_BREAKDOWN_NOT_A_VERDICT', provenance=prov, n_pairs=n,
               gate_equivalent_mismatch=mismatch, tables=tables,
               rel_dFt_over_Ft=quant(rt), rel_dFn_over_Fn=quant(rn),
               reset_like_pairs=reset_like, sign_flip_like_pairs=sign_flip_like,
               atoms_used=have_atoms)
    if have_atoms:
        out.update(
            orig_grid='%dx%d' % ORIG_GRID, orig_ghost_pairs_not_reversed=ghost_not_reversed,
            orig_ghost_class_counts=dict((c, sum(v for k3, v in tables.get('ghost_orig_x_fail_normal_tangent_total', {}).items()
                                                 if k3.split('|')[0] == c)) for c in ('local', 'ghost', 'ambiguous')),
            test_grid_violations=test_grid_viol,
            M1_fit=dict((k2, v.out()) for k2, v in fit.items()),
            M1_contrast_cos_dFt_vs_Ft_orig_local=quant(contrast_cos_Ft),
            M1_predicted_tangent_fail=dict((k2, dict(pred_fail=v[0], pairs=v[1])) for k2, v in m1_pred_fail.items()),
            M2_normal=dict((k2, v.out()) for k2, v in m2.items()),
            branch_switch_ratio_dFt_over_damping=quant(switch_ratio),
            top20_dFt=[json.loads(s) for _, s in sorted(top, reverse=True)])
    else:
        out['atoms_note'] = 'atom dump not found: M1/M2 quantitative checks NOT_RUN'
    out['limits'] = ('Read-only numerical breakdown. No threshold change, no acceptance verdict. '
                     'M1 prediction uses v(n), omega(n) from the setup dump (history increment used v(n-1/2)); '
                     'M2 uses setup forces as f(n). Material constants from the r8 deck.')
    return out


def main(argv):
    root = Path(argv[1]) if len(argv) > 1 else None
    require(root is not None and root.is_dir(), 'usage: - <UL_ROOT>  (folder that holds ps_7_3_r45/)')
    bed = root / 'ps_7_3_r45'
    orig = bed / 'in' / 'contact_3200000.liggghts'
    test = bed / 'RJ' / 'R' / 'g2' / 'contact_3200000.liggghts'
    atoms = bed / 'RJ' / 'R' / 'obs' / 'post_atom_3200000.dump'
    out = analyze(orig, test, atoms)
    screen = bed / 'RJ' / 'R' / 'screen.txt'
    if screen.is_file():
        grids = sorted(set(re.findall(r'(\d+) by (\d+) by (\d+) MPI processor grid',
                                      screen.read_text(encoding='utf-8', errors='replace'))))
        out['rj_screen_processor_grid'] = ['x'.join(g) for g in grids]
    else:
        out['rj_screen_processor_grid'] = 'screen.txt not found (informational only)'
    po, pt = out['provenance']['original'], out['provenance']['test']
    bound = (po['sha256'] == '53ae293b4586d091dfca58ab430c174f36b641dcd24678eb10d10fc3f416e65c' and
             po['bytes'] == 149687008 and
             pt['sha256'] == '193e6e6ca2e6833d3204fd26615b61b5de32f6e65d931fcdbd560c215365951f' and
             pt['bytes'] == 149729924 and out['n_pairs'] == 562605 and out['gate_equivalent_mismatch'] == 545583)
    out['recorded_binding_match'] = bound
    if not bound:
        return {'status': 'BINDING_MISMATCH_NOT_A_VERDICT', 'provenance': out['provenance'],
                'n_pairs': out['n_pairs'], 'gate_equivalent_mismatch': out['gate_equivalent_mismatch']}
    return out


def cli(argv):
    me = globals().get('__cause_sha256__')
    try:
        res = main(argv)
        res['check_sha256'] = me
        print(json.dumps(res, indent=1, allow_nan=False, default=str))
        return 0 if res.get('status') == 'COMPLETE_CAUSE_BREAKDOWN_NOT_A_VERDICT' else 2
    except Exception as err:
        print(json.dumps({'status': 'INCOMPLETE_NOT_A_VERDICT', 'error': str(err), 'type': type(err).__name__,
                          'check_sha256': me}))
        return 2


if __name__ == '__main__':
    sys.dont_write_bytecode = True
    raise SystemExit(cli(sys.argv))
