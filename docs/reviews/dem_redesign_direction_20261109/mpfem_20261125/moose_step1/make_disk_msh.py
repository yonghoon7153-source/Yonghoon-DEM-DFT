"""MPFEM step 1 (MOOSE): one O-grid disk + two plates -> Gmsh MSH 2.2 ASCII + .mesh.json.

Development data.  Standard library only.  Port of the 2D part of
../mpfem_plan/step1_inputs/make_disk_mesh.py (ogrid_numpy + plate, radius mode 'exact',
same defaults): same nodes in the same order, same quads.  m13 = --ns 8 --nr 2,
m26 = --ns 16 --nr 4.  Units SI, D = 0.1 m, gap to each plate 0.0017272 D.

Numeric tags used by step1_disk.i (libMesh GmshIO: quad tag -> block, edge tag -> sideset,
point tag -> nodeset):
  quads  1 disk   2 bottom plate   3 top plate
  edges  11 disk boundary, midpoint y > 0     12 disk boundary, midpoint y < 0
         20 bottom plate contact face          30 top plate contact face
  points 13 disk boundary nodes y > tol        14 disk boundary nodes y < -tol
         22 all bottom plate nodes             32 all top plate nodes
         41 disk nodes |x| < tol (SymX)        42 disk nodes |y| < tol (SymY)
  tol = 1e-9 R (as the design mesher).
"""
import argparse
import hashlib
import json
import math
import sys

D, GAP_D, ALPHA, PLATE_W_D, PLATE_T_D = 0.1, 0.0017272, 0.6, 2.0, 0.1


def signed_area(xy, q):
    s = 0.0
    for k in range(4):
        x0, y0 = xy[q[k]]
        x1, y1 = xy[q[(k + 1) % 4]]
        s += x0 * y1 - y0 * x1
    return 0.5 * s


def ogrid(R, Rb, alpha, ns, nr):
    """Same construction and node order as ogrid_numpy of the design mesher."""
    a = alpha * R
    xy = []

    def add(p):
        xy.append(p)
        return len(xy) - 1

    G = [[add((-a + 2 * a * i / ns, -a + 2 * a * j / ns)) for j in range(ns + 1)]
         for i in range(ns + 1)]
    inner = [
        [G[ns][j] for j in range(ns + 1)],
        [G[ns - i][ns] for i in range(ns + 1)],
        [G[0][ns - j] for j in range(ns + 1)],
        [G[i][0] for i in range(ns + 1)],
    ]
    P = []
    for p in range(4):
        cols = []
        for m in range(ns + 1):
            th = -math.pi / 4 + p * math.pi / 2 + (math.pi / 2) * m / ns
            x0, y0 = xy[inner[p][m]]
            x1, y1 = Rb * math.cos(th), Rb * math.sin(th)
            col = [inner[p][m]]
            for k in range(1, nr + 1):
                if m == 0 and p > 0:
                    col.append(P[p - 1][ns][k])
                elif m == ns and p == 3:
                    col.append(P[0][0][k])
                else:
                    t = k / nr
                    col.append(add(((1 - t) * x0 + t * x1, (1 - t) * y0 + t * y1)))
            cols.append(col)
        P.append(cols)
    quads = [[G[i][j], G[i + 1][j], G[i + 1][j + 1], G[i][j + 1]]
             for i in range(ns) for j in range(ns)]
    for p in range(4):
        for m in range(ns):
            for k in range(nr):
                quads.append([P[p][m][k], P[p][m][k + 1], P[p][m + 1][k + 1], P[p][m + 1][k]])
    boundary = [P[p][m][nr] for p in range(4) for m in range(ns)]
    return [tuple(map(float, c)) for c in xy], quads, boundary


def linspace(x0, x1, n):
    """numpy.linspace(x0, x1, n + 1) bit for bit: i * step + x0, last point = x1."""
    step = (x1 - x0) / n
    v = [i * step + x0 for i in range(n + 1)]
    v[-1] = x1
    return v


def plate(x0, x1, y0, y1, nx):
    xs, ys = linspace(x0, x1, nx), linspace(y0, y1, 1)
    xy = [(x, y) for y in ys for x in xs]
    quads = [[i, i + 1, nx + 1 + i + 1, nx + 1 + i] for i in range(nx)]
    return xy, quads, list(range(nx + 1)), list(range(nx + 1, 2 * (nx + 1)))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True, help="output path without extension")
    ap.add_argument("--ns", type=int, default=8)
    ap.add_argument("--nr", type=int, default=2)
    args = ap.parse_args(argv)
    if args.ns % 2 or args.ns < 2 or args.nr < 1:
        ap.error("ns must be even and nr >= 1")

    R, nc = D / 2, 4 * args.ns
    poly_ratio = (nc / (2 * math.pi)) * math.sin(2 * math.pi / nc)
    Rb = R                                               # radius mode 'exact'
    dxy, dq, bnd = ogrid(R, Rb, ALPHA, args.ns, args.nr)
    for q in dq:
        if signed_area(dxy, q) < 0:
            q.reverse()
    if len({n for q in dq for n in q}) != len(dxy):
        raise RuntimeError("disk mesh has nodes not used by any quad")
    disk_area = sum(signed_area(dxy, q) for q in dq)

    gap = GAP_D * D
    yb, yt = -R - gap, R + gap
    W, T = PLATE_W_D * D, PLATE_T_D * D
    nx = max(2, int(round(W / (2 * math.pi * R / nc))))
    bxy, bq, _, b_top = plate(-W / 2, W / 2, yb - T, yb, nx)
    txy, tq, t_bot, _ = plate(-W / 2, W / 2, yt, yt + T, nx)
    nd, nb = len(dxy), len(bxy)
    xy = dxy + bxy + txy
    tol = 1e-9 * R
    nid = lambda i: i + 1                                # 1-based, design mesher order

    elems = []                                           # (type, tag, [node ids])
    for tag, qs, off in ((1, dq, 0), (2, bq, nd), (3, tq, nd + nb)):
        elems += [(3, tag, [nid(n + off) for n in q]) for q in qs]
    for i in range(nc):
        a, b = bnd[i], bnd[(i + 1) % nc]
        elems.append((1, 11 if dxy[a][1] + dxy[b][1] > 0 else 12, [nid(a), nid(b)]))
    elems += [(1, 20, [nid(nd + b_top[i + 1]), nid(nd + b_top[i])]) for i in range(nx)]
    elems += [(1, 30, [nid(nd + nb + t_bot[i]), nid(nd + nb + t_bot[i + 1])]) for i in range(nx)]
    up = [n for n in bnd if dxy[n][1] > tol]
    down = [n for n in bnd if dxy[n][1] < -tol]
    symx = [i for i in range(nd) if abs(dxy[i][0]) < tol]
    symy = [i for i in range(nd) if abs(dxy[i][1]) < tol]
    for tag, ids in ((13, up), (14, down), (22, range(nd, nd + nb)),
                     (32, range(nd + nb, nd + 2 * nb)), (41, symx), (42, symy)):
        elems += [(15, tag, [nid(i)]) for i in sorted(ids)]

    lines = ["$MeshFormat", "2.2 0 8", "$EndMeshFormat", "$Nodes", str(len(xy))]
    lines += ["%d %r %r 0" % (i + 1, x, y) for i, (x, y) in enumerate(xy)]
    lines += ["$EndNodes", "$Elements", str(len(elems))]
    lines += ["%d %d 2 %d %d %s" % (k + 1, et, tag, tag, " ".join(map(str, c)))
              for k, (et, tag, c) in enumerate(elems)]
    lines += ["$EndElements", ""]
    data = "\n".join(lines).encode("ascii")
    with open(args.out + ".msh", "wb") as f:
        f.write(data)

    count = lambda et, tag: sum(1 for e in elems if e[0] == et and e[1] == tag)
    stats = {
        "label": "DEVELOPMENT_ONLY", "generator": "make_disk_msh.py (port of make_disk_mesh.py, 2D)",
        "argv": sys.argv[1:] if argv is None else list(argv), "format": "gmsh MSH 2.2 ASCII",
        "dim": 2, "D_m": D, "R_m": R, "gap_m": gap,
        "plate_contact_y_m": [yb, yt], "h0_between_plates_m": yt - yb,
        "ns": args.ns, "nr": args.nr, "alpha": ALPHA,
        "disk_quads": len(dq), "disk_nodes_2d": nd, "boundary_segments": nc,
        "per_diameter_area_equiv": math.sqrt(len(dq) / (math.pi / 4)),
        "boundary_segment_over_D": math.pi * 2 * Rb / nc / D,
        "radius_mode": "exact", "Rb_over_R": Rb / R,
        "polygon_area_ratio_exact_radius": poly_ratio,
        "disk_area_mesh_m2": disk_area, "disk_area_circle_m2": math.pi * R * R,
        "sagitta_over_D": Rb * (1 - math.cos(math.pi / nc)) / D,
        "plate_nx": nx, "plate_ny": 1, "plate_width_m": W, "plate_thick_m": T,
        "symx_nodes_2d": len(symx), "symy_nodes_2d": len(symy),
        "tag_counts": {"quad_1": count(3, 1), "quad_2": count(3, 2), "quad_3": count(3, 3),
                       "edge_11": count(1, 11), "edge_12": count(1, 12), "edge_20": count(1, 20),
                       "edge_30": count(1, 30), "node_13": count(15, 13), "node_14": count(15, 14),
                       "node_22": count(15, 22), "node_32": count(15, 32),
                       "node_41": count(15, 41), "node_42": count(15, 42)},
        "msh_sha256": hashlib.sha256(data).hexdigest(),
    }
    with open(args.out + ".mesh.json", "w", encoding="ascii") as f:
        json.dump(stats, f, indent=1)
    print(json.dumps({k: stats[k] for k in ("disk_quads", "boundary_segments", "plate_nx",
                                             "per_diameter_area_equiv", "disk_area_mesh_m2")}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
