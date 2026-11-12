#!/usr/bin/env python3
"""Pre-attack final (independent) — recompute 15-5b W metric on the 11-12 sandbox dumps and
probe counterexamples.  Read-only on the received dumps.  Usage: python3 -I pfa_w_check.py <run40000 dir>"""
import math
import random
import sys

D = sys.argv[1]
BOX = 0.012


def load(path):
    rows = {}
    with open(path) as f:
        lines = f.read().splitlines()
    i = lines.index(next(l for l in lines if l.startswith('ITEM: ENTRIES')))
    for ln in lines[i + 1:]:
        if not ln.strip():
            continue
        v = [float(x) for x in ln.split()]
        a, b = int(v[6]), int(v[7])
        if a > b:   # orient: swap positions, negate forces (9..17) and shear (21..23)
            v = v[3:6] + v[0:3] + [v[7], v[6]] + v[8:9] + [-x for x in v[9:18]] + v[18:21] + [-x for x in v[21:24]] + v[24:]
        key = (min(a, b), max(a, b))
        assert key not in rows, ('dup', key)
        rows[key] = v
    return rows


def norm(x):
    return math.sqrt(sum(t * t for t in x))


def metrics(T, O, lost=frozenset()):
    """W etc. of test T vs orig O; 'lost' = keys whose test Ft is replaced by 0 (loss model, damping ignored)."""
    common = sorted(set(T) & set(O))
    miss, extra = len(set(O) - set(T)), len(set(T) - set(O))
    num = den = 0.0
    nreset = ncol = 0
    rs = []
    for k in common:
        fo = O[k][15:18]
        ft = [0.0, 0.0, 0.0] if k in lost else T[k][15:18]
        no = norm(fo)
        den += no
        if no > 0:
            r = norm([a - b for a, b in zip(ft, fo)]) / no
            rs.append(r)
            if r > 0.5:
                nreset += 1
                num += no
            if norm(ft) < 0.5 * no:
                ncol += 1
    rs.sort()
    med = rs[len(rs) // 2] if len(rs) % 2 else 0.5 * (rs[len(rs) // 2 - 1] + rs[len(rs) // 2])
    return dict(n=len(common), miss=miss, extra=extra, reset=nreset, share=nreset / len(common), W=num / den if den else None,
                rmed=med, collapse=ncol / len(common), den=den)


def owner_cell(x, y, gx, gy):
    return (min(int((x % BOX) / BOX * gx), gx - 1), min(int((y % BOX) / BOX * gy), gy - 1))


A = load(f'{D}/A/post/c_40000.txt')
B = load(f'{D}/B/post/c_40000.txt')
C = load(f'{D}/C/post/c_40000.txt')
Apre = load(f'{D}/A/post/cpre_39999.txt')

print('== honest (my recomputation)')
for name, T in (('B<->A(N)', B), ('C<->A(N)', C)):
    m = metrics(T, A)
    print(name, {k: (round(v, 6) if isinstance(v, float) else v) for k, v in m.items()},
          'margin 0.05/W =', round(0.05 / m['W'], 1) if m['W'] else None)

# periodic-flag of reset pairs in C
mC = [k for k in sorted(set(C) & set(A)) if norm(A[k][15:18]) > 0
      and norm([a - b for a, b in zip(C[k][15:18], A[k][15:18])]) > 0.5 * norm(A[k][15:18])]
print('C reset pairs periodic flags:', [int(A[k][8]) for k in mC])

# bottom-10 % membership of B reset pairs
fts = sorted(norm(A[k][15:18]) for k in A)
q10 = fts[int(0.10 * len(fts))]
mB = [k for k in sorted(set(B) & set(A)) if norm(A[k][15:18]) > 0
      and norm([a - b for a, b in zip(B[k][15:18], A[k][15:18])]) > 0.5 * norm(A[k][15:18])]
print('B reset pairs:', len(mB), 'with |Ft_o| < q10:', sum(1 for k in mB if norm(A[k][15:18]) < q10), 'q10 =', q10)

# load concentration
tot = sum(fts)
desc = sorted(fts, reverse=True)
acc, kmin = 0.0, None
for i, v in enumerate(desc):
    acc += v
    if acc / tot > 0.05 and kmin is None:
        kmin = i + 1
print('pairs (largest first) needed to exceed W 0.05 alone:', kmin, 'of', len(desc),
      '| top 1 % share', round(sum(desc[:len(desc) // 100]) / tot, 4))

print('== partition fact: per-chunk W of a whole-chunk loss sums to ~1 (mean = 1/ncell)')
for gx, gy, label in ((6, 4, 'NP24 6x4x1 (7:3 writer)'), (11, 1, 'NP11 11x1x1 (10:0 writer)'), (5, 1, 'NP5 5x1x1 (0:10 · 5:5 writer)'),
                      (2, 2, 'NP4 2x2x1 (3:7 writer)'), (3, 2, 'NP6 3x2x1 (reader)')):
    cells = {}
    for k in A:
        # owner = atom with larger tag (dump copy) — approx: pair position of atom of larger id = cols 3..5 after orientation
        x, y = A[k][3], A[k][4]
        cells.setdefault(owner_cell(x, y, gx, gy), set()).add(k)
    Ws = []
    for c, ks in sorted(cells.items()):
        Ws.append(metrics(B, A, lost=frozenset(ks))['W'])
    nc = gx * gy
    print(f'  {label}: cells {nc} · mean W {sum(Ws)/len(Ws):.4f} (1/n = {1/nc:.4f}) · min {min(Ws):.4f} · max {max(Ws):.4f} · '
          f'caught (>0.05) {sum(w > 0.05 for w in Ws)}/{len(Ws)}')

print('== honest one-step change along the trajectory: A(N-1) vs A(N) (not a lag test; scale only)')
m = metrics(Apre, A)
print('  A(N-1)<->A(N)', {k: (round(v, 6) if isinstance(v, float) else v) for k, v in m.items()})

print('== random subsets (seeded) — W spread at fixed lost fraction 5 % (production uniformity proxy)')
rng = random.Random(20261112)
keys = sorted(set(B) & set(A))
for frac in (0.0417, 0.05):
    ws = []
    for _ in range(400):
        lost = frozenset(rng.sample(keys, int(round(frac * len(keys)))))
        ws.append(metrics(B, A, lost=lost)['W'])
    ws.sort()
    print(f'  lost {frac:.4f}: W median {ws[200]:.4f} · p05 {ws[20]:.4f} · p95 {ws[380]:.4f} · caught {sum(w > 0.05 for w in ws)}/400')
