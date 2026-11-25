#!/usr/bin/env python3
"""G1 one-disk mesh for Kratos: O-grid disk + two rigid plates -> .mdpa + .mesh.json.

DRAFT for the MPFEM plan, step 1.  Written but NOT executed by its author.

Geometry = reg1 G1 (docs/reviews/suyoung_next_registrations_20261125/
reg1_contact_mini_20261125.md): one disk of diameter D, gap g_p = 0.0017272 D
to the bottom plate and to the top plate.  Units SI, D = 0.1 m by default.

--dim 2 : plane-strain quads (law decides plane strain).
--dim 3 : one-layer slab of hexahedra; plane strain comes from u_z = 0 on every
          node (imposed in ProjectParameters, not here).
--mesher numpy : O-grid by linear (transfinite) blending, numpy only (default).
--mesher gmsh  : the same O-grid with gmsh transfinite surfaces.  "import gmsh"
                 needs libGLU.so.1, which the cloud container does not have.
--radius-mode exact : boundary nodes on the circle (first-contact geometry exact).
--radius-mode area  : boundary radius scaled so the polygon area equals pi R^2.

Mesh sizes used by the plan (O-grid, ns x ns inner square + 4 patches of ns x nr):
  m13 : ns 8,  nr 2 -> 128 quads,  32 boundary segments, sqrt(Nel/(pi/4)) = 12.8
  m26 : ns 16, nr 4 -> 512 quads,  64 boundary segments, 25.5
  m52 : ns 32, nr 8 -> 2048 quads, 128 boundary segments, 51.1
(Zhou 2019 used 132 elements per disk = 13.0 per diameter by the same measure:
 litdb-canon:zhou2019_mpfem_2d_copper_powder_die_compaction_release section 3-1.)
"""
import argparse
import json
import math
import sys

import numpy as np


def signed_area(xy, quad):
    pts = xy[list(quad)]
    x, y = pts[:, 0], pts[:, 1]
    return 0.5 * float(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))


def ogrid_numpy(R, Rb, alpha, ns, nr):
    """Disk centred at 0.  Returns xy (N,2), quads (M,4) CCW, boundary ids CCW from -45 deg."""
    a = alpha * R
    xy = []

    def add(p):
        xy.append(p)
        return len(xy) - 1

    G = [[add((-a + 2 * a * i / ns, -a + 2 * a * j / ns)) for j in range(ns + 1)]
         for i in range(ns + 1)]
    inner = [
        [G[ns][j] for j in range(ns + 1)],        # east  x=+a, y increasing
        [G[ns - i][ns] for i in range(ns + 1)],   # north y=+a, x decreasing
        [G[0][ns - j] for j in range(ns + 1)],    # west  x=-a, y decreasing
        [G[i][0] for i in range(ns + 1)],         # south y=-a, x increasing
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
    return np.array(xy, dtype=float), np.array(quads, dtype=int), np.array(boundary, dtype=int)


def ogrid_gmsh(R, Rb, alpha, ns, nr):
    """Same O-grid through gmsh (transfinite + recombine).  Needs a working 'import gmsh'."""
    import gmsh
    gmsh.initialize()
    try:
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.model.add("disk")
        g = gmsh.model.geo
        a, s2 = alpha * R, Rb / math.sqrt(2.0)
        c = g.addPoint(0, 0, 0)
        sq = [g.addPoint(a, -a, 0), g.addPoint(a, a, 0), g.addPoint(-a, a, 0), g.addPoint(-a, -a, 0)]
        ap = [g.addPoint(s2, -s2, 0), g.addPoint(s2, s2, 0), g.addPoint(-s2, s2, 0), g.addPoint(-s2, -s2, 0)]
        side = [g.addLine(sq[i], sq[(i + 1) % 4]) for i in range(4)]
        rad = [g.addLine(sq[i], ap[i]) for i in range(4)]
        arc = [g.addCircleArc(ap[i], c, ap[(i + 1) % 4]) for i in range(4)]
        surfs = [g.addPlaneSurface([g.addCurveLoop(side)])]
        for i in range(4):
            j = (i + 1) % 4
            surfs.append(g.addPlaneSurface([g.addCurveLoop([side[i], rad[j], -arc[i], -rad[i]])]))
        for l in side + arc:
            g.mesh.setTransfiniteCurve(l, ns + 1)
        for l in rad:
            g.mesh.setTransfiniteCurve(l, nr + 1)
        for s in surfs:
            g.mesh.setTransfiniteSurface(s)
            g.mesh.setRecombine(2, s)
        g.synchronize()
        gmsh.model.mesh.generate(2)
        tags, coords, _ = gmsh.model.mesh.getNodes()
        index = {int(t): i for i, t in enumerate(tags)}
        xy = np.array(coords, dtype=float).reshape(-1, 3)[:, :2]
        quads = []
        etypes, _, enodes = gmsh.model.mesh.getElements(2)
        for et, en in zip(etypes, enodes):
            if int(et) != 3:
                raise RuntimeError("gmsh produced non-quad 2D elements (type %d)" % int(et))
            quads += [[index[int(n)] for n in en[q:q + 4]] for q in range(0, len(en), 4)]
    finally:
        gmsh.finalize()
    quads = np.array(quads, dtype=int)
    # gmsh also meshes the arc-centre point: drop every node no quad uses (an orphan node
    # would carry DOFs without stiffness and make the Kratos system singular)
    used = np.unique(quads)
    remap = -np.ones(len(xy), dtype=int)
    remap[used] = np.arange(len(used))
    xy, quads = xy[used], remap[quads]
    edges = {}
    for q in quads:
        for e in range(4):
            k = tuple(sorted((int(q[e]), int(q[(e + 1) % 4]))))
            edges[k] = edges.get(k, 0) + 1
    bnodes = sorted({n for k, c in edges.items() if c == 1 for n in k})
    ang = [(math.atan2(xy[n, 1], xy[n, 0]) + math.pi / 4) % (2 * math.pi) for n in bnodes]
    boundary = np.array([n for _, n in sorted(zip(ang, bnodes))], dtype=int)
    if len(boundary) != 4 * ns:
        raise RuntimeError("boundary node count %d != 4*ns" % len(boundary))
    return xy, quads, boundary


def plate(x0, x1, y0, y1, nx, ny):
    xs, ys = np.linspace(x0, x1, nx + 1), np.linspace(y0, y1, ny + 1)
    xy = np.array([(x, y) for y in ys for x in xs], dtype=float)
    idx = lambda i, j: j * (nx + 1) + i
    quads = np.array([[idx(i, j), idx(i + 1, j), idx(i + 1, j + 1), idx(i, j + 1)]
                      for j in range(ny) for i in range(nx)], dtype=int)
    bottom_row = [idx(i, 0) for i in range(nx + 1)]     # left -> right
    top_row = [idx(i, ny) for i in range(nx + 1)]       # left -> right
    return xy, quads, bottom_row, top_row


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True, help="output path without extension")
    ap.add_argument("--dim", type=int, choices=(2, 3), default=3)
    ap.add_argument("--ns", type=int, default=8)
    ap.add_argument("--nr", type=int, default=2)
    ap.add_argument("--alpha", type=float, default=0.6, help="inner square half-side / R")
    ap.add_argument("--D", type=float, default=0.1, help="disk diameter [m]")
    ap.add_argument("--gap-d", type=float, default=0.0017272, help="plate gap / D (reg1 G1)")
    ap.add_argument("--plate-width-d", type=float, default=2.0)
    ap.add_argument("--plate-thick-d", type=float, default=0.1)
    ap.add_argument("--plate-nx", type=int, default=0, help="0 = match the disk boundary segment")
    ap.add_argument("--tz", type=float, default=0.005, help="slab thickness [m] (dim 3)")
    ap.add_argument("--radius-mode", choices=("exact", "area"), default="exact")
    ap.add_argument("--mesher", choices=("numpy", "gmsh"), default="numpy")
    ap.add_argument("--element-disk", default=None)
    ap.add_argument("--element-plate", default=None)
    args = ap.parse_args(argv)
    if args.ns % 2 or args.ns < 2 or args.nr < 1:
        ap.error("ns must be even (nodes on both diameters) and nr >= 1")

    D, R = args.D, args.D / 2
    nc = 4 * args.ns
    poly_ratio = (nc / (2 * math.pi)) * math.sin(2 * math.pi / nc)
    Rb = R / math.sqrt(poly_ratio) if args.radius_mode == "area" else R
    build = ogrid_numpy if args.mesher == "numpy" else ogrid_gmsh
    dxy, dq, bnd = build(R, Rb, args.alpha, args.ns, args.nr)
    for q in dq:
        if signed_area(dxy, q) < 0:
            q[:] = q[::-1].copy()
    if len(np.unique(dq)) != len(dxy):
        raise RuntimeError("disk mesh has nodes not used by any quad")
    disk_area = sum(signed_area(dxy, q) for q in dq)

    gap = args.gap_d * D
    yb, yt = -R - gap, R + gap
    W, T = args.plate_width_d * D, args.plate_thick_d * D
    nx = args.plate_nx or max(2, int(round(W / (2 * math.pi * R / nc))))
    bxy, bq, _, b_top = plate(-W / 2, W / 2, yb - T, yb, nx, 1)
    txy, tq, t_bot, _ = plate(-W / 2, W / 2, yt, yt + T, nx, 1)

    nd, nb = len(dxy), len(bxy)
    xy = np.vstack([dxy, bxy, txy])
    quads = {"disk": dq, "bottom": bq + nd, "top": tq + nd + nb}
    # contact edges, ordered so that a->b runs CCW around each body (outward normal = (dy,-dx))
    seg = {"disk": [(int(bnd[i]), int(bnd[(i + 1) % nc])) for i in range(nc)],
           "bottom": [(nd + b_top[i + 1], nd + b_top[i]) for i in range(nx)],
           "top": [(nd + nb + t_bot[i], nd + nb + t_bot[i + 1]) for i in range(nx)]}
    tol = 1e-9 * R
    symx = [i for i in range(nd) if abs(dxy[i, 0]) < tol]
    symy = [i for i in range(nd) if abs(dxy[i, 1]) < tol]
    n2 = len(xy)

    if args.dim == 2:
        layers = [0.0]
        nid = lambda i, l=0: i + 1
        el_disk = args.element_disk or "SmallDisplacementBbarElement2D4N"
        el_plate = args.element_plate or "SmallDisplacementElement2D4N"
        cond = "LineCondition2D2N"
        cells = lambda q: [[nid(int(n)) for n in qq] for qq in q]
        faces = lambda s: [[nid(a), nid(b)] for a, b in s]
    else:
        layers = [0.0, args.tz]
        nid = lambda i, l=0: l * n2 + i + 1
        el_disk = args.element_disk or "TotalLagrangianQ1P0MixedElement3D8N"
        el_plate = args.element_plate or "TotalLagrangianElement3D8N"
        cond = "SurfaceCondition3D4N"
        cells = lambda q: [[nid(int(n), 0) for n in qq] + [nid(int(n), 1) for n in qq] for qq in q]
        faces = lambda s: [[nid(a, 0), nid(b, 0), nid(b, 1), nid(a, 1)] for a, b in s]

    nodes = [(nid(i, l), xy[i, 0], xy[i, 1], z) for l, z in enumerate(layers) for i in range(n2)]
    eid, elements, sub = 0, {}, {}
    for part, prop, ename in (("disk", 1, el_disk), ("bottom", 2, el_plate), ("top", 3, el_plate)):
        rows = []
        for c in cells(quads[part]):
            eid += 1
            rows.append((eid, prop, c))
        elements.setdefault(ename, []).extend(rows)
        sub[part] = rows
    cid, conds = 0, {}
    for part, prop in (("disk", 1), ("bottom", 2), ("top", 3)):
        rows = []
        for f in faces(seg[part]):
            cid += 1
            rows.append((cid, prop, f))
        conds[part] = rows

    def nodes_of(rows):
        return sorted({n for _, _, c in rows for n in c})

    all_layers = lambda ids: sorted(nid(i, l) for l in range(len(layers)) for i in ids)
    smp = [
        ("Disk", nodes_of(sub["disk"]), [r[0] for r in sub["disk"]], []),
        ("BottomPlate", nodes_of(sub["bottom"]), [r[0] for r in sub["bottom"]], []),
        ("TopPlate", nodes_of(sub["top"]), [r[0] for r in sub["top"]], []),
        ("DiskSurface", nodes_of(conds["disk"]), [], [r[0] for r in conds["disk"]]),
        ("PlateSurfaces", nodes_of(conds["bottom"] + conds["top"]), [],
         [r[0] for r in conds["bottom"] + conds["top"]]),
        ("SymX", all_layers(symx), [], []),
        ("SymY", all_layers(symy), [], []),
    ]

    with open(args.out + ".mdpa", "w", encoding="ascii") as f:
        f.write("// G1 one-disk mesh (MPFEM plan step 1 draft) - generated by make_disk_mesh.py\n")
        f.write("Begin ModelPartData\nEnd ModelPartData\n\n")
        for p in (1, 2, 3):
            f.write("Begin Properties %d\nEnd Properties\n" % p)
        f.write("\nBegin Nodes\n")
        for n, x, y, z in nodes:
            f.write("%d %.16e %.16e %.16e\n" % (n, x, y, z))
        f.write("End Nodes\n\n")
        for ename, rows in elements.items():
            f.write("Begin Elements %s\n" % ename)
            for e, p, c in rows:
                f.write("%d %d %s\n" % (e, p, " ".join(map(str, c))))
            f.write("End Elements\n\n")
        f.write("Begin Conditions %s\n" % cond)
        for part in ("disk", "bottom", "top"):
            for c_, p, fc in conds[part]:
                f.write("%d %d %s\n" % (c_, p, " ".join(map(str, fc))))
        f.write("End Conditions\n\n")
        for name, ns_, es_, cs_ in smp:
            f.write("Begin SubModelPart %s\n" % name)
            for tag, ids in (("Nodes", ns_), ("Elements", es_), ("Conditions", cs_)):
                f.write("  Begin SubModelPart%s\n" % tag)
                for i in ids:
                    f.write("    %d\n" % i)
                f.write("  End SubModelPart%s\n" % tag)
            f.write("End SubModelPart\n\n")

    stats = {
        "label": "DEVELOPMENT_ONLY", "generator": "make_disk_mesh.py", "argv": sys.argv[1:],
        "mesher": args.mesher, "dim": args.dim, "D_m": D, "R_m": R, "gap_m": gap,
        "plate_contact_y_m": [yb, yt], "h0_between_plates_m": yt - yb,
        "ns": args.ns, "nr": args.nr, "alpha": args.alpha,
        "disk_quads": int(len(dq)), "disk_nodes_2d": int(nd), "boundary_segments": nc,
        "per_diameter_area_equiv": math.sqrt(len(dq) / (math.pi / 4)),
        "boundary_segment_over_D": math.pi * 2 * Rb / nc / D,
        "radius_mode": args.radius_mode, "Rb_over_R": Rb / R,
        "polygon_area_ratio_exact_radius": poly_ratio,
        "disk_area_mesh_m2": disk_area, "disk_area_circle_m2": math.pi * R * R,
        "sagitta_over_D": Rb * (1 - math.cos(math.pi / nc)) / D,
        "plate_nx": nx, "tz_m": args.tz if args.dim == 3 else None,
        "elements": {k: len(v) for k, v in elements.items()}, "conditions": cid,
        "element_disk": el_disk, "element_plate": el_plate, "condition": cond,
        "symx_nodes_2d": len(symx), "symy_nodes_2d": len(symy),
    }
    with open(args.out + ".mesh.json", "w", encoding="ascii") as f:
        json.dump(stats, f, indent=1)
    print(json.dumps({k: stats[k] for k in ("disk_quads", "boundary_segments",
                                             "per_diameter_area_equiv", "disk_area_mesh_m2")}))


if __name__ == "__main__":
    main()
