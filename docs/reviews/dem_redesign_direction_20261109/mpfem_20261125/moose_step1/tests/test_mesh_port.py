#!/usr/bin/env python3
"""Tests for ../make_disk_msh.py (written before the port).

1. Same O-grid as the Kratos design mesher: runs ../../mpfem_plan/step1_inputs/make_disk_mesh.py
   --dim 2 (needs numpy; skipped with a message if numpy is missing) and compares nodes
   (bit for bit), quads, boundary segments, plate faces, SymX / SymY and the shared stats.
2. Gmsh file structure the MOOSE input relies on: tags, counts, sides, nodesets, CCW quads.
"""
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = os.path.join(os.path.dirname(HERE), "make_disk_msh.py")
ORIG = os.path.join(os.path.dirname(os.path.dirname(HERE)), "mpfem_plan", "step1_inputs",
                    "make_disk_mesh.py")
MESHES = {"m13": (8, 2, 128, 145, 32, 20), "m26": (16, 4, 512, 545, 64, 41)}


def sh(args):
    p = subprocess.run([sys.executable] + args, capture_output=True, text=True)
    if p.returncode != 0:
        raise AssertionError("command failed: %s\n%s" % (" ".join(args), p.stdout + p.stderr))
    return p.stdout


def read_msh(path):
    with open(path, encoding="ascii") as f:
        lines = f.read().split("\n")
    assert lines[0] == "$MeshFormat" and lines[1] == "2.2 0 8" and lines[2] == "$EndMeshFormat", lines[:3]
    i = lines.index("$Nodes")
    n = int(lines[i + 1])
    nodes = {}
    for k in range(n):
        p = lines[i + 2 + k].split()
        nodes[int(p[0])] = (float(p[1]), float(p[2]), float(p[3]))
    assert lines[i + 2 + n] == "$EndNodes"
    j = lines.index("$Elements")
    m = int(lines[j + 1])
    elems = []
    for k in range(m):
        p = [int(x) for x in lines[j + 2 + k].split()]
        eid, etype, ntags = p[0], p[1], p[2]
        tags, conn = p[3:3 + ntags], p[3 + ntags:]
        elems.append((eid, etype, tags[0], tags, conn))
    assert lines[j + 2 + m] == "$EndElements"
    assert [e[0] for e in elems] == list(range(1, m + 1)), "element ids must be 1..N"
    assert sorted(nodes) == list(range(1, n + 1)), "node ids must be 1..N"
    return nodes, elems


def read_mdpa(path):
    nodes, elems, conds, smp = {}, [], [], {}
    with open(path, encoding="ascii") as f:
        lines = [l.strip() for l in f]
    sec, name, sub = None, None, None
    for l in lines:
        if not l or l.startswith("//"):
            continue
        w = l.split()
        if w[0] == "Begin":
            if w[1] == "SubModelPart":
                name = w[2]
                smp[name] = {"Nodes": [], "Elements": [], "Conditions": []}
                sec = "smp"
            elif w[1].startswith("SubModelPart"):
                sub = w[1][len("SubModelPart"):]
            else:
                sec = w[1]
            continue
        if w[0] == "End":
            if w[1].startswith("SubModelPart") and w[1] != "SubModelPart":
                sub = None
            elif w[1] == "SubModelPart":
                sec, name = None, None
            else:
                sec = None
            continue
        if sec == "Nodes":
            nodes[int(w[0])] = (float(w[1]), float(w[2]), float(w[3]))
        elif sec == "Elements":
            elems.append((int(w[1]), [int(x) for x in w[2:]]))
        elif sec == "Conditions":
            conds.append((int(w[1]), [int(x) for x in w[2:]]))
        elif sec == "smp" and sub:
            smp[name][sub].append(int(w[0]))
    return nodes, elems, conds, smp


def build(tmp, tag):
    ns, nr = MESHES[tag][:2]
    out = os.path.join(tmp, "disk_" + tag)
    sh([PORT, "--ns", str(ns), "--nr", str(nr), "--out", out])
    with open(out + ".mesh.json", encoding="ascii") as f:
        stats = json.load(f)
    return out, stats


def by_tag(elems, etype, tag):
    return [e[4] for e in elems if e[1] == etype and e[2] == tag]


# ---------------------------------------------------------------- tests
def t_same_ogrid_as_design_mesher(tmp):
    try:
        import numpy  # noqa: F401
    except ImportError:
        print("  SKIP (numpy missing): original mesher not run")
        return
    for tag, (ns, nr, nq, ndn, nseg, pnx) in MESHES.items():
        out, stats = build(tmp, tag)
        ref = os.path.join(tmp, "orig_" + tag)
        sh([ORIG, "--dim", "2", "--ns", str(ns), "--nr", str(nr), "--out", ref])
        rn, re_, rc, rs = read_mdpa(ref + ".mdpa")
        with open(ref + ".mesh.json", encoding="ascii") as f:
            rstats = json.load(f)
        n, e = read_msh(out + ".msh")
        assert len(n) == len(rn), (tag, len(n), len(rn))
        for i in rn:
            assert n[i] == rn[i], (tag, "node", i, n[i], rn[i])          # bit for bit
        for prop, phys in ((1, 1), (2, 2), (3, 3)):
            assert [c for p, c in re_ if p == prop] == by_tag(e, 3, phys), (tag, "quads", prop)
        seg = lambda L: sorted(tuple(sorted(c)) for c in L)
        disk_lines = by_tag(e, 1, 11) + by_tag(e, 1, 12)
        assert seg([c for p, c in rc if p == 1]) == seg(disk_lines), (tag, "disk boundary")
        assert seg([c for p, c in rc if p == 2]) == seg(by_tag(e, 1, 20)), (tag, "bottom face")
        assert seg([c for p, c in rc if p == 3]) == seg(by_tag(e, 1, 30)), (tag, "top face")
        pts = lambda t: sorted(c[0] for c in by_tag(e, 15, t))
        assert pts(41) == sorted(rs["SymX"]["Nodes"]), (tag, "symx")
        assert pts(42) == sorted(rs["SymY"]["Nodes"]), (tag, "symy")
        for k in ("disk_quads", "disk_nodes_2d", "boundary_segments", "plate_nx", "ns", "nr",
                  "alpha", "D_m", "R_m", "gap_m", "h0_between_plates_m", "plate_contact_y_m",
                  "per_diameter_area_equiv", "boundary_segment_over_D", "Rb_over_R",
                  "polygon_area_ratio_exact_radius", "sagitta_over_D", "symx_nodes_2d",
                  "symy_nodes_2d", "radius_mode"):
            assert stats[k] == rstats[k], (tag, k, stats[k], rstats[k])
        a, b = stats["disk_area_mesh_m2"], rstats["disk_area_mesh_m2"]
        assert abs(a - b) <= 1e-12 * b, (tag, a, b)


def t_counts_and_tags(tmp):
    for tag, (ns, nr, nq, ndn, nseg, pnx) in MESHES.items():
        out, st = build(tmp, tag)
        n, e = read_msh(out + ".msh")
        assert st["disk_quads"] == nq and st["disk_nodes_2d"] == ndn, st
        assert st["boundary_segments"] == nseg and st["plate_nx"] == pnx, st
        assert len(by_tag(e, 3, 1)) == nq and len(by_tag(e, 3, 2)) == pnx and len(by_tag(e, 3, 3)) == pnx
        assert len(by_tag(e, 1, 11)) == nseg // 2 and len(by_tag(e, 1, 12)) == nseg // 2
        assert len(by_tag(e, 1, 20)) == pnx and len(by_tag(e, 1, 30)) == pnx
        assert len(n) == ndn + 2 * 2 * (pnx + 1)
        used = {"tags": sorted({(x[1], x[2]) for x in e})}
        assert used["tags"] == [(1, 11), (1, 12), (1, 20), (1, 30), (3, 1), (3, 2), (3, 3),
                                (15, 13), (15, 14), (15, 22), (15, 32), (15, 41), (15, 42)], used
        assert abs(st["per_diameter_area_equiv"] - {"m13": 12.8, "m26": 25.5}[tag]) < 0.06, st
        assert st["msh_sha256"] and len(st["msh_sha256"]) == 64


def t_geometry_and_sides(tmp):
    for tag in MESHES:
        out, st = build(tmp, tag)
        n, e = read_msh(out + ".msh")
        R, tol = st["R_m"], 1e-9 * st["R_m"]
        quads = {1: by_tag(e, 3, 1), 2: by_tag(e, 3, 2), 3: by_tag(e, 3, 3)}
        sides = {}
        for blk, qs in quads.items():
            for q in qs:
                x = [n[i][0] for i in q]
                y = [n[i][1] for i in q]
                area = 0.5 * sum(x[k] * y[(k + 1) % 4] - y[k] * x[(k + 1) % 4] for k in range(4))
                assert area > 0, (tag, "quad not CCW", q)
                for k in range(4):
                    s = tuple(sorted((q[k], q[(k + 1) % 4])))
                    sides.setdefault(s, []).append(blk)
        for t, blk in ((11, 1), (12, 1), (20, 2), (30, 3)):
            for c in by_tag(e, 1, t):
                owners = sides.get(tuple(sorted(c)), [])
                assert owners == [blk], (tag, t, c, owners)     # a side of exactly one quad
        for c in by_tag(e, 1, 11):
            assert n[c[0]][1] + n[c[1]][1] > 0, (tag, "top half", c)
        for c in by_tag(e, 1, 12):
            assert n[c[0]][1] + n[c[1]][1] < 0, (tag, "bottom half", c)
        bnodes = {i for t in (11, 12) for c in by_tag(e, 1, t) for i in c}
        up = {c[0] for c in by_tag(e, 15, 13)}
        down = {c[0] for c in by_tag(e, 15, 14)}
        assert up == {i for i in bnodes if n[i][1] > tol}, tag
        assert down == {i for i in bnodes if n[i][1] < -tol}, tag
        assert len(bnodes - up - down) == 2, (tag, "two equator nodes")
        for t, blk in ((22, 2), (32, 3)):
            assert {c[0] for c in by_tag(e, 15, t)} == {i for q in quads[blk] for i in q}, (tag, t)
        disk_nodes = {i for q in quads[1] for i in q}
        assert {c[0] for c in by_tag(e, 15, 41)} == {i for i in disk_nodes if abs(n[i][0]) < tol}
        assert {c[0] for c in by_tag(e, 15, 42)} == {i for i in disk_nodes if abs(n[i][1]) < tol}
        yb, yt = st["plate_contact_y_m"]
        assert all(n[i][1] == yt for c in by_tag(e, 1, 30) for i in c), tag
        assert all(n[i][1] == yb for c in by_tag(e, 1, 20) for i in c), tag
        assert abs(st["h0_between_plates_m"] - (2 * R + 2 * st["gap_m"])) < 1e-15
        ymax = max(n[i][1] for i in disk_nodes)
        assert abs((yt - ymax) - st["gap_m"]) < 1e-15, (tag, "gap to top plate")
        a = sum(0.5 * sum(n[q[k]][0] * n[q[(k + 1) % 4]][1] - n[q[k]][1] * n[q[(k + 1) % 4]][0]
                          for k in range(4)) for q in quads[1])
        assert abs(a - st["disk_area_mesh_m2"]) <= 1e-14, (tag, a, st["disk_area_mesh_m2"])


def t_deterministic(tmp):
    out1, st1 = build(tmp, "m13")
    d2 = os.path.join(tmp, "again")
    os.makedirs(d2)
    out2, st2 = build(d2, "m13")
    with open(out1 + ".msh", "rb") as a, open(out2 + ".msh", "rb") as b:
        assert a.read() == b.read()
    assert st1["msh_sha256"] == st2["msh_sha256"]


TESTS = [v for k, v in sorted(globals().items()) if k.startswith("t_")]


def main():
    npass = nfail = 0
    for t in TESTS:
        tmp = tempfile.mkdtemp(prefix="mesh_")
        try:
            t(tmp)
            npass += 1
            print("PASS", t.__name__)
        except Exception as exc:
            nfail += 1
            print("FAIL", t.__name__, "-", type(exc).__name__, str(exc)[:300].replace("\n", " | "))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    print("mesh port tests: %d passed, %d failed, %d total" % (npass, nfail, npass + nfail))
    return 0 if nfail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
