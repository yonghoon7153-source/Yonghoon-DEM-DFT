"""내부 반박 리뷰 산술 (읽기만) — 초안 B §2 의 랭크 경계 쌍 어림을 받은 A(N) 덤프로 다시 센다.
쓰임: python3 -I rb_count.py <atom_N 덤프> <c_N 쌍 덤프>
"""
import sys
from collections import Counter


def read_dump(path):
    with open(path, encoding='ascii') as f:
        lines = f.read().splitlines()
    k = next(i for i, x in enumerate(lines) if x.startswith('ITEM: BOX BOUNDS'))
    box = [tuple(float(v) for v in lines[k + 1 + a].split()) for a in range(3)]
    h = next(i for i, x in enumerate(lines) if x.startswith('ITEM: ATOMS') or x.startswith('ITEM: ENTRIES'))
    cols = lines[h].split()[2:]
    rows = [ln.split() for ln in lines[h + 1:] if ln.strip()]
    return box, cols, rows


def main(atom_path, pair_path):
    box, acols, arows = read_dump(atom_path)
    ia = {c: i for i, c in enumerate(acols)}
    pos, typ, rad = {}, Counter(), {}
    zr = 0.0
    for r in arows:
        i = int(r[ia['id']])
        x, y, z = float(r[ia['x']]), float(r[ia['y']]), float(r[ia['z']])
        pos[i] = (x, y, z)
        typ[int(r[ia['type']])] += 1
        rad[i] = float(r[ia['radius']])
        zr = max(zr, z + rad[i])
    print('atoms', len(pos), 'types', dict(sorted(typ.items())), 'max z+r', zr, 'box', box)
    _, pcols, prows = read_dump(pair_path)
    pairs = [(int(float(r[6])), int(float(r[7])), int(float(r[8]))) for r in prows]
    print('pairs', len(pairs), 'flag', dict(Counter(p[2] for p in pairs)))
    (xlo, xhi), (ylo, yhi), (zlo, zhi) = box

    def owner(i, g):
        x, y, z = pos[i]
        px, py, pz = g
        # 고른 나눔: lo + L·k/P 경계 · 칸 = floor((x - lo)/L · P) (경계 위 = 위 칸)
        cx = min(int((x - xlo) / (xhi - xlo) * px), px - 1)
        cy = min(int((y - ylo) / (yhi - ylo) * py), py - 1)
        cz = min(int((z - zlo) / (zhi - zlo) * pz), pz - 1)
        return (cx, cy, cz)

    def near(i, g, tol):
        x, y, z = pos[i]
        out = False
        for v, lo, hi, p in ((x, xlo, xhi, g[0]), (y, ylo, yhi, g[1]), (z, zlo, zhi, g[2])):
            for k in range(1, p):
                b = lo + (hi - lo) * k / p
                if abs(v - b) <= tol * (hi - lo):
                    out = True
        return out

    for g in ((2, 1, 1), (1, 2, 1), (2, 2, 1), (3, 2, 1), (2, 3, 1), (1, 1, 2), (1, 1, 4), (1, 1, 6)):
        c = Counter()
        for i, j, f in pairs:
            same = owner(i, g) == owner(j, g)
            c[(f, same)] += 1
        amb = sum(1 for i in pos if near(i, g, 1e-12))
        print('grid', g, 'flag0 cross', c[(0, False)], 'flag0 same', c[(0, True)],
              'flag1 cross', c[(1, False)], 'flag1 same', c[(1, True)], 'atoms within 1e-12 L of boundary', amb)
    # 하위영역 · 절단 산술
    rmax = max(rad.values())
    print('r_max', rmax, '2r_max + skin(0.0005)', 2 * rmax + 0.0005)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
