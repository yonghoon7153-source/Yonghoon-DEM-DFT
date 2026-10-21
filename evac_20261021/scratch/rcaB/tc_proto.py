"""Prototype of the target-quantity certificate (scratch; not production)."""
import math

import numpy as np
from scipy import sparse
from scipy.sparse.csgraph import connected_components

_U = 2.0 ** -53
_FSUM_CHUNK = 1 << 20


def _fsum_bound(x):
    x = np.asarray(x, np.float64).ravel()
    if x.size <= _FSUM_CHUNK:
        s = math.fsum(x.tolist())
        return s, 2.0 * _U * abs(s)
    parts = [math.fsum(x[i:i + _FSUM_CHUNK].tolist()) for i in range(0, x.size, _FSUM_CHUNK)]
    s = math.fsum(parts)
    return s, 2.0 * _U * (math.fsum(abs(p) for p in parts) + abs(s))


def ledger(L, b, Ab, gb, At, gt):
    L = sparse.csr_matrix(L, dtype=np.float64)
    n = L.shape[0]
    Lc = L if L.has_canonical_format else L.copy()
    if not Lc.has_canonical_format:
        Lc.sum_duplicates()
        Lc.sort_indices()
    up = sparse.triu(Lc, k=1, format='csr')
    lo = sparse.tril(Lc, k=-1, format='csr').T.tocsr()
    up.sum_duplicates(); up.sort_indices(); lo.sum_duplicates(); lo.sort_indices()
    if not (np.array_equal(up.indptr, lo.indptr) and np.array_equal(up.indices, lo.indices)):
        return {'problem': 'asym_pattern'}
    if (np.abs(up.data - lo.data) > 4 * _U * np.maximum(np.abs(up.data), np.abs(lo.data))).any():
        return {'problem': 'asym_value'}
    if (up.data > 0).any():
        return {'problem': 'positive_offdiag'}
    rows = np.repeat(np.arange(n, dtype=np.int64), np.diff(up.indptr))
    keep = up.data < 0
    eu, ev, eg = rows[keep], up.indices[keep].astype(np.int64), -up.data[keep]
    Ab = np.asarray(Ab, np.int64); At = np.asarray(At, np.int64)
    gb = np.asarray(gb, np.float64); gt = np.asarray(gt, np.float64)
    rs = np.asarray(Lc.sum(axis=1)).ravel()
    ar = np.asarray(abs(Lc).sum(axis=1)).ravel()
    pl = np.bincount(Ab, gb, n) + np.bincount(At, gt, n)
    if (np.abs(rs - pl) > 64 * _U * (ar + pl)).any():
        return {'problem': 'rowsum'}
    bb = np.bincount(Ab, gb, n)
    bv = np.asarray(b, np.float64)
    if (np.abs(bv - bb) > 64 * _U * (np.abs(bv) + bb)).any():
        return {'problem': 'rhs'}
    return {'problem': None, 'n': n, 'eu': eu, 'ev': ev, 'eg': eg, 'Ab': Ab, 'gb': gb, 'At': At, 'gt': gt}


def reps(n, Ab, gb, At, gt):
    node = np.concatenate([Ab, At]).astype(np.int64)
    g = np.concatenate([gb, gt])
    kind = np.concatenate([np.ones(len(Ab), np.int8), np.full(len(At), 2, np.int8)])
    idx = np.concatenate([np.arange(len(Ab)), np.arange(len(At))]).astype(np.int64)
    o = np.lexsort((idx, kind, -g, node))
    node, kind, idx = node[o], kind[o], idx[o]
    f = np.r_[True, node[1:] != node[:-1]] if len(node) else np.zeros(0, bool)
    return node[f], kind[f], idx[f]


def bfs(n, eu, ev, eg, rn, rk, ri):
    m = len(eu)
    A = sparse.csr_matrix((np.r_[np.arange(m), np.arange(m)].astype(np.int64) + 1, (np.r_[eu, ev], np.r_[ev, eu])), shape=(n, n))
    indptr = A.indptr.astype(np.int64); nbrs = A.indices.astype(np.int64); eids = A.data.astype(np.int64) - 1
    depth = np.full(n, -1, np.int64)
    parent = np.full(n, -1, np.int64); pkind = np.full(n, -1, np.int8); pedge = np.full(n, -1, np.int64)
    if not len(rn):
        return depth, parent, pkind, pedge, []
    depth[rn] = 1; parent[rn] = n; pkind[rn] = rk; pedge[rn] = ri
    levels = [rn]
    front = rn
    lev = 1
    while True:
        st = indptr[front]
        ln = indptr[front + 1] - st
        tot = int(ln.sum())
        if tot == 0:
            break
        base = np.repeat(st - (np.cumsum(ln) - ln), ln)
        pos = base + np.arange(tot, dtype=np.int64)
        nb = nbrs[pos]; ed = eids[pos]; pa = np.repeat(front, ln)
        new = depth[nb] < 0
        if not new.any():
            break
        nb, ed, pa = nb[new], ed[new], pa[new]
        o = np.lexsort((ed, pa, -eg[ed], nb))
        nb, ed, pa = nb[o], ed[o], pa[o]
        f = np.r_[True, nb[1:] != nb[:-1]]
        nb, ed, pa = nb[f], ed[f], pa[f]
        lev += 1
        depth[nb] = lev; parent[nb] = pa; pkind[nb] = 0; pedge[nb] = ed
        levels.append(nb)
        front = nb
    return depth, parent, pkind, pedge, levels


def defects(n, eu, ev, c, Ab, cb, At, ct):
    return np.bincount(Ab, cb, n) - np.bincount(At, ct, n) - np.bincount(eu, c, n) + np.bincount(ev, c, n)


def bracket(L, b, phi, Ab, gb, At, gt, tree=True, defect_term=True):
    led = ledger(L, b, Ab, gb, At, gt)
    if led['problem']:
        return {'problem': led['problem']}
    n, eu, ev, eg, Ab, gb, At, gt = (led[k] for k in ('n', 'eu', 'ev', 'eg', 'Ab', 'gb', 'At', 'gt'))
    phi = np.asarray(phi, np.float64)
    adj = sparse.coo_matrix((np.ones(len(eu), np.int8), (eu, ev)), shape=(n, n))
    ncomp, lab = connected_components(adj, directed=False)
    cbm = np.zeros(ncomp, bool); ctm = np.zeros(ncomp, bool)
    cbm[lab[Ab]] = True; ctm[lab[At]] = True
    thr = cbm & ctm
    if not thr.any():
        return {'problem': None, 'topology': 'zero'}
    dphi = phi[eu] - phi[ev]
    c = eg * dphi
    cb = gb * (1.0 - phi[Ab])
    ct = gt * phi[At]
    s1, e1 = _fsum_bound(c * dphi)
    s2, e2 = _fsum_bound(cb * (1.0 - phi[Ab]))
    s3, e3 = _fsum_bound(ct * phi[At])
    U = math.fsum([s1, s2, s3])
    hi = (U + e1 + e2 + e3) * (1.0 + 8.0 * _U)
    rn, rk, ri = reps(n, Ab, gb, At, gt)
    depth, parent, pkind, pedge, levels = bfs(n, eu, ev, eg, rn, rk, ri)
    unr = depth < 0
    c = c.copy(); cb = cb.copy(); ct = ct.copy()
    c[unr[eu]] = 0.0
    d = defects(n, eu, ev, c, Ab, cb, At, ct)
    kcl_raw = float(np.abs(d).sum())
    if tree:
        acc = d.copy()
        for lv in reversed(levels):
            a = acc[lv]
            k = pkind[lv]
            m0 = k == 0
            if m0.any():
                vv = lv[m0]; ee = pedge[vv]; aa = a[m0]
                out = eu[ee] == vv
                c[ee[out]] += aa[out]
                c[ee[~out]] -= aa[~out]
                np.add.at(acc, parent[vv], aa)
            m1 = k == 1
            if m1.any():
                cb[pedge[lv[m1]]] -= a[m1]
            m2 = k == 2
            if m2.any():
                ct[pedge[lv[m2]]] += a[m2]
            acc[lv] = 0.0
    d2 = defects(n, eu, ev, c, Ab, cb, At, ct)
    a2 = np.bincount(Ab, np.abs(cb), n) + np.bincount(At, np.abs(ct), n) + np.bincount(eu, np.abs(c), n) + np.bincount(ev, np.abs(c), n)
    deg = np.bincount(Ab, minlength=n) + np.bincount(At, minlength=n) + np.bincount(eu, minlength=n) + np.bincount(ev, minlength=n)
    err = (2.0 * deg + 8.0) * _U * a2
    if defect_term:
        dp, dpe = _fsum_bound(np.maximum(d2 + err, 0.0))
        dm, dme = _fsum_bound(np.maximum(-d2 + err, 0.0))
        Dp = (dp + dpe) * (1 + 4 * _U); Dm = (dm + dme) * (1 + 4 * _U)
    else:
        Dp = Dm = 0.0
    FB, FBe = _fsum_bound(cb)
    FT, FTe = _fsum_bound(ct)
    w1, we1 = _fsum_bound(c * c / eg)
    w2, we2 = _fsum_bound(cb * cb / gb)
    w3, we3 = _fsum_bound(ct * ct / gt)
    W = math.fsum([w1, w2, w3])
    Whi = (W + we1 + we2 + we3) * (1 + 8 * _U)
    num = max(FB - FBe - Dp, FT - FTe - Dm)
    lo = (num * num / Whi) * (1 - 4 * _U) if (num > 0 and Whi > 0) else 0.0
    return {'problem': None, 'topology': 'through', 'lo': lo, 'hi': hi, 'U': U, 'W': W, 'FB': FB, 'FT': FT, 'Dp': Dp, 'Dm': Dm,
            'kcl_raw': kcl_raw, 'levels': len(levels), 'n_unreach': int(unr.sum())}
