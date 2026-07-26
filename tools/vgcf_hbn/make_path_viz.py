#!/usr/bin/env python3
"""make_path_viz.py — one structure file that DRAWS the Li hop path for VESTA.

  python3 make_path_viz.py --min <case>_min.vasp --ts <case>_ts.xyz --out <case>_pathviz

Reaction coordinates and the saddle image index come from the case preset / the
"image N/M" stamp in the TS xyz, so the same command works for every case.

ILLUSTRATION ONLY — do not feed this to any calculation. Only three Li positions
in it are DFT: endpoint A (from the relaxed minimum), the CI-NEB saddle (from the
TS frame), and endpoint B (= A + one hollow-lattice vector, degenerate with A by
symmetry — the NEB last image sits 1.5 meV from the first, so this is exact to
within the calculation). The remaining markers are a quadratic interpolation
through those three, sampled at the real NEB reaction coordinates, so the trail
bows the way the true path does without pretending to be the true path.

Marker species are dummies picked so VESTA colours them apart with no styling:
  Li  x2  the two endpoint hollow sites   (real, relaxed)
  S   x1  the CI-NEB saddle               (real; yellow in VESTA)
  O   x4  interpolated trail markers      (bright red in VESTA)
Recolour freely in VESTA: Objects -> Properties -> Atoms.

Outputs an xyz + POSCAR(.vasp) pair per house convention (xyz carries no lattice,
so Boundary tiling has to be done from the .vasp).
"""
import argparse
import re

# reaction coordinates of the 7 NEB images, per case (neb.x <prefix>.dat col 1).
# Defaults so the common cases need no --xi; anything else passes its own list.
XI = {
    "Li_in_gallery_2L2L": [0.0, 0.1895986772, 0.3446900038, 0.4885989580,
                           0.6335860707, 0.7984897818, 1.0],
    "Li_on_graphene": [0.0, 0.1946143614, 0.3553932821, 0.4998587133,
                       0.6445009937, 0.8053800471, 1.0],
}


def read_poscar(path):
    L = open(path).read().splitlines()
    scale = float(L[1].split()[0])
    cell = [[float(v) * scale for v in L[i].split()[:3]] for i in (2, 3, 4)]
    species, counts = L[5].split(), [int(v) for v in L[6].split()]
    assert L[7].strip().lower().startswith("c"), "Cartesian POSCAR만 지원"
    at, k = [], 8
    for s, n in zip(species, counts):
        for _ in range(n):
            x, y, z = (float(v) for v in L[k].split()[:3])
            at.append((s, x, y, z)); k += 1
    return cell, at


def read_xyz_last(path):
    L = open(path).read().splitlines()
    s = L[2 + int(L[0].strip()) - 1].split()
    return (s[0], float(s[1]), float(s[2]), float(s[3]))


def ts_index_from_comment(path):
    """mk_vesta stamps 'CI-NEB saddle, image N/M' — N-1 is the 0-based TS index."""
    m = re.search(r"image\s+(\d+)\s*/\s*(\d+)", open(path).read().splitlines()[1])
    return (int(m.group(1)) - 1, int(m.group(2))) if m else (None, None)


def quad(p0, pt, p1, xt):
    """Quadratic through (0,p0), (xt,pt), (1,p1); returns f(xi)."""
    out = []
    for c0, ct, c1 in zip(p0, pt, p1):
        # c(xi) = c0 + b*xi + c*xi^2 with c0+b+c = c1 and the mid point pinned
        b_plus_c = c1 - c0
        c = (ct - c0 - xt * b_plus_c) / (xt * xt - xt)
        b = b_plus_c - c
        out.append((c0, b, c))
    return lambda xi: tuple(a + b * xi + c * xi * xi for a, b, c in out)


def write_xyz(path, at, comment):
    with open(path, "w") as f:
        f.write(f"{len(at)}\n{comment}\n")
        for e, x, y, z in at:
            f.write(f"{e:2s} {x:14.8f} {y:14.8f} {z:14.8f}\n")


def write_vasp(path, at, cell, comment):
    order = []
    for e, *_ in at:
        if e not in order:
            order.append(e)
    with open(path, "w") as f:
        f.write(comment + "\n1.0\n")
        for v in cell:
            f.write(f" {v[0]:18.10f} {v[1]:18.10f} {v[2]:18.10f}\n")
        f.write(" " + " ".join(f"{e:>4s}" for e in order) + "\n")
        f.write(" " + " ".join(f"{sum(1 for a in at if a[0] == e):>4d}" for e in order) + "\n")
        f.write("Cartesian\n")
        for e in order:
            for a in at:
                if a[0] == e:
                    f.write(f" {a[1]:18.10f} {a[2]:18.10f} {a[3]:18.10f}\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min", required=True, help="relaxed minimum POSCAR (Cartesian)")
    ap.add_argument("--ts", required=True, help="CI-NEB saddle xyz")
    ap.add_argument("--out", required=True, help="output basename")
    ap.add_argument("--hop", type=float, default=2.46, help="hop along +x (A)")
    ap.add_argument("--case", default="",
                    help="reaction-coordinate preset key (default: guess from --ts name)")
    ap.add_argument("--xi", default="",
                    help="comma-separated NEB reaction coordinates (overrides --case)")
    ap.add_argument("--dense", type=int, default=0,
                    help="if >0, draw this many evenly spaced trail markers instead "
                         "of the 7 NEB image positions")
    a = ap.parse_args()

    cell, at = read_poscar(a.min)
    assert at[-1][0] == "Li", "마지막 원자가 Li가 아님"
    host, (_, ax, ay, az) = at[:-1], at[-1]
    A = (ax, ay, az)
    B = (ax + a.hop, ay, az)
    _, tx, ty, tz = read_xyz_last(a.ts)
    TS = (tx, ty, tz)

    ts_i, n_img = ts_index_from_comment(a.ts)
    if a.xi:
        xis_all = [float(v) for v in a.xi.split(",")]
    else:
        key = a.case or next((k for k in XI if k in a.ts), "")
        if key in XI:
            xis_all = XI[key]
        else:
            n = n_img or 7
            xis_all = [i / (n - 1) for i in range(n)]
            print(f"      (반응좌표 프리셋 없음 — {n}점 등간격으로 대체)")
    if ts_i is None:
        ts_i = min(range(len(xis_all)), key=lambda i: abs(xis_all[i] - 0.5))
    assert len(xis_all) == (n_img or len(xis_all)), "이미지 수와 반응좌표 개수 불일치"
    xt = xis_all[ts_i]
    f = quad(A, TS, B, xt)

    if a.dense:
        xis = [i / (a.dense + 1) for i in range(1, a.dense + 1)]
    else:
        xis = [x for i, x in enumerate(xis_all)
               if i not in (0, ts_i, len(xis_all) - 1)]

    out = list(host)
    out.append(("Li", *A))
    out.append(("Li", *B))
    out.append(("S", *TS))
    for xi in xis:
        out.append(("O", *f(xi)))

    cm = (f"PATH ILLUSTRATION ONLY - Li=endpoint sites, S=CI-NEB saddle, "
          f"O=interpolated trail markers (NOT atoms). hop {a.hop} A")
    write_xyz(f"{a.out}.xyz", out, cm)
    write_vasp(f"{a.out}.vasp", out, cell, cm)
    print(f"[viz] {a.out}.vasp / .xyz  —  host {len(host)} + Li 2 + saddle 1 "
          f"+ trail {len(xis)}  = {len(out)} sites")
    print(f"      A  {A[0]:8.3f} {A[1]:8.3f} {A[2]:8.3f}")
    print(f"      TS {TS[0]:8.3f} {TS[1]:8.3f} {TS[2]:8.3f}   (xi={xt:.4f}, "
          f"bows {A[1]-TS[1]:+.3f} A in y, rises {TS[2]-A[2]:+.3f} A in z)")
    print(f"      B  {B[0]:8.3f} {B[1]:8.3f} {B[2]:8.3f}")


if __name__ == "__main__":
    main()
