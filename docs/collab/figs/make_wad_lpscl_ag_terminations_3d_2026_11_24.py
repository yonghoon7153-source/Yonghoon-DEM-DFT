#!/usr/bin/env python3
"""make_wad_lpscl_ag_terminations_3d_2026_11_24.py — VESTA-like pseudo-3D view of the two LPSCl|Ag(111) terminations.

Report figure 2 of docs/collab/wad_dem_interface_adhesion_report_2026_11_24.html
(the flat side view with contact outlines stays as figure 3: make_wad_lpscl_ag_terminations_2026_11_24.py).

Input : db/raw/wad_se_pairs_uma_2026_10_01/relax/P1_{s_outer,li_outer}/A/relaxed.extxyz (UMA+D3 relaxed · registry A)
Shown : first two Ag(111) layers + SE down to 6.2 A below the lowest Ag · one lateral cell (wrapped)
        PS4 tetrahedra (P with its 4 nearest S, minimum image) · Ag-S contacts (S-Ag <= 2.9 A, minimum image —
        a contact that crosses the cell edge draws that Ag image as an extra sphere)
Style : house palette (tools/figures/house_style.py) · English labels only · dpi 300

What this tool cannot do
  · It is not a ray tracer: depth is painter's order (sphere centre / face centroid). Spheres that interpenetrate
    are not clipped against each other and translucent faces do not refract.
  · Li-Ag and Cl-Ag contacts are not drawn (figure 3 marks them) — only Ag-S contacts.
  · It reads geometry only; it does not compute or show any energy.
"""
import argparse
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Polygon
from ase.geometry import find_mic, get_distances
from ase.io import read

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(REPO, "tools", "figures"))
import house_style as H  # noqa: E402

D = os.path.join(REPO, "db", "raw", "wad_se_pairs_uma_2026_10_01", "relax")
COL = {"Li": H.ELEM["Li"], "P": H.ELEM["P"], "S": H.ELEM["S"], "Cl": H.ELEM["Cl"], "Ag": "#c3c8d1"}
RAD = {"Li": 0.42, "P": 0.34, "S": 0.60, "Cl": 0.60, "Ag": 0.70}
CUT_S = 2.9          # Ag-S contact [A] (same cut as figure 3 and the contact CSV)
R_PS = 2.5           # P-S bond [A]
SE_DEPTH = 6.2       # SE shown down to this far below the lowest Ag [A]
AG_TOP = 2.9         # Ag shown up to this far above the lowest Ag [A] (two layers)
CONTACT = "#1f2937"
FACE = "#a78bfa"     # PS4 face (lighter violet than P so the P sphere reads through it)
EDGE = "#6d28d9"

LIGHT = np.array([-0.45, 0.55, 1.0]); LIGHT /= np.linalg.norm(LIGHT)
HALF = LIGHT + np.array([0.0, 0.0, 1.0]); HALF /= np.linalg.norm(HALF)


def sprite(color, fog, n=180):
    """Shaded sphere image (RGBA): soft ambient + diffuse + small specular, faint limb darkening, white fog blend."""
    c = np.array(to_rgb(color))
    y, x = np.mgrid[-1:1:n * 1j, -1:1:n * 1j]
    r2 = x * x + y * y
    z = np.sqrt(np.clip(1 - r2, 0, 1))
    N = np.dstack([x, y, z])
    dif = np.clip(N @ LIGHT, 0, 1)
    spe = np.clip(N @ HALF, 0, 1) ** 40
    rgb = c[None, None, :] * (0.46 + 0.56 * dif[..., None]) * (0.86 + 0.14 * z[..., None]) + 0.38 * spe[..., None]
    rgb = np.clip(rgb, 0, 1) * (1 - fog) + fog
    a = np.clip((1 - np.sqrt(r2)) * n / 3, 0, 1)
    return np.dstack([rgb, a])


def fogged(color, fog):
    return tuple(np.array(to_rgb(color)) * (1 - fog) + fog)


class View:
    def __init__(self, elev_deg, azim_deg):
        e, a = np.radians(elev_deg), np.radians(azim_deg)
        self.d = np.array([np.cos(e) * np.cos(a), np.cos(e) * np.sin(a), np.sin(e)])   # toward the viewer
        up = np.array([0.0, 0.0, 1.0]); fwd = -self.d
        self.right = np.cross(fwd, up); self.right /= np.linalg.norm(self.right)
        self.up = np.cross(self.right, fwd)

    def __call__(self, p):
        return float(p @ self.right), float(p @ self.up), float(p @ self.d)


def scene(term, view):
    """Primitive list for one termination: ('sphere', el, xyz) · ('stick', xyz_a, xyz_b, col_a, col_b, w) · ('face', [xyz]*3)."""
    a = read(os.path.join(D, f"P1_{term}", "A", "relaxed.extxyz"))
    a.wrap()
    sym = np.array(a.get_chemical_symbols())
    pos = a.positions.copy()
    ag = np.where(sym == "Ag")[0]
    pos[:, 2] -= pos[ag, 2].min()
    shown = [i for i in range(len(a)) if (sym[i] != "Ag" and pos[i, 2] >= -SE_DEPTH) or (sym[i] == "Ag" and pos[i, 2] <= AG_TOP)]
    shown_set = set(shown)
    prims, drawn_S = [], {}
    S_all = np.where(sym == "S")[0]
    for p in [i for i in shown if sym[i] == "P"]:
        vec, dist = find_mic(pos[S_all] - pos[p], a.cell, pbc=a.pbc)
        nb = np.argsort(dist)[:4]
        assert dist[nb].max() < R_PS, f"{term}: P{p} has fewer than 4 S within {R_PS} A"
        verts = [pos[p] + vec[k] for k in nb]
        for f in ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)):
            prims.append(("face", [verts[j] for j in f]))
        for k, v in zip(nb, verts):
            prims.append(("stick", pos[p], v, COL["P"], COL["S"], 0.095))
            drawn_S[int(S_all[k])] = v          # the tetrahedron corner is where this S is drawn
    ghost_ag = []
    S_pts = {i: drawn_S.get(i, pos[i]) for i in shown if sym[i] == "S"}
    for i, q in S_pts.items():
        for j in ag:
            dv, dd = find_mic(pos[j] - q, a.cell, pbc=a.pbc)
            if dd <= CUT_S:
                tip = q + dv
                prims.append(("stick", q, tip, COL["S"], CONTACT, 0.075))
                if j not in shown_set or np.linalg.norm(tip - pos[j]) > 1e-3:
                    ghost_ag.append(tip)
    for i in shown:
        el = sym[i]
        xyz = S_pts[i] if el == "S" else pos[i]
        prims.append(("sphere", el, xyz))
    for g in ghost_ag:
        prims.append(("sphere", "Ag", g))
    return prims


def extent(prims, view):
    xs, ys = [], []
    for pr in prims:
        pts = [pr[2]] if pr[0] == "sphere" else (pr[1] if pr[0] == "face" else [pr[1], pr[2]])
        for q in pts:
            X, Y, _ = view(q); xs.append(X); ys.append(Y)
    return min(xs), max(xs), min(ys), max(ys)


def draw(ax, prims, view, zlim, fog_max):
    z0, z1 = zlim
    fog = lambda Z: fog_max * (z1 - Z) / max(z1 - z0, 1e-9)
    cache = {}

    def spr(el, f):
        key = (el, round(f, 2))
        if key not in cache:
            cache[key] = sprite(COL[el], key[1])
        return cache[key]

    for pr in prims:
        if pr[0] == "sphere":
            _, el, xyz = pr
            X, Y, Z = view(xyz); r = RAD[el]
            ax.imshow(spr(el, fog(Z)), extent=(X - r, X + r, Y - r, Y + r), origin="lower",
                      zorder=20 + Z + 0.5, interpolation="bilinear")
        elif pr[0] == "face":
            P3 = [view(q) for q in pr[1]]
            Zc = float(np.mean([q[2] for q in P3]))
            ax.add_patch(Polygon([(q[0], q[1]) for q in P3], closed=True, facecolor=fogged(FACE, fog(Zc)) + (0.30,),
                                 edgecolor=fogged(EDGE, fog(Zc)), lw=0.7, joinstyle="round", zorder=20 + Zc))
        else:
            _, pa, pb, ca, cb, w = pr
            (xa, ya, za), (xb, yb, zb) = view(pa), view(pb)
            v = np.array([xb - xa, yb - ya]); ln = np.hypot(*v)
            if ln < 1e-6:
                continue
            nrm = np.array([-v[1], v[0]]) / ln
            m = ((xa + xb) / 2, (ya + yb) / 2)
            for (x0, y0), (x1, y1), col, zz in (((xa, ya), m, ca, za), (m, (xb, yb), cb, zb)):
                base = np.array(fogged(col, fog(zz)))
                for ww, shade, dz in ((w, 0.72, 0.0), (w * 0.42, 1.18, 0.01)):
                    cc = tuple(np.clip(base * shade, 0, 1))
                    pts = [(x0 + nrm[0] * ww, y0 + nrm[1] * ww), (x1 + nrm[0] * ww, y1 + nrm[1] * ww),
                           (x1 - nrm[0] * ww, y1 - nrm[1] * ww), (x0 - nrm[0] * ww, y0 - nrm[1] * ww)]
                    ax.add_patch(Polygon(pts, closed=True, facecolor=cc, edgecolor="none", zorder=20 + zz - 0.3 + dz))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "wad_lpscl_ag_terminations_3d_2026_11_24.png"))
    ap.add_argument("--elev", type=float, default=18.0, help="view elevation above the interface plane [deg]")
    ap.add_argument("--azim", type=float, default=16.7, help="view azimuth from the short cell axis x [deg]")
    ap.add_argument("--fog", type=float, default=0.22, help="white blend for the farthest atoms (depth cue)")
    ap.add_argument("--dpi", type=int, default=300)
    args = ap.parse_args()
    view = View(args.elev, args.azim)
    panels = [("s_outer", "S-outer termination  —  Ag touches 4 free S (no P bond) + 8 Li"),
              ("li_outer", "Li·PS$_4$-outer termination  —  Ag touches 8 S of PS$_4$ tetrahedra + 4 Li")]
    sc = [(t, ttl, scene(t, view)) for t, ttl in panels]
    ext = [extent(p, view) for _, _, p in sc]
    W = max(e[1] - e[0] for e in ext) + 2 * 0.9
    Hh = max(e[3] - e[2] for e in ext) + 2 * 0.9
    Zs = [view(pr[2])[2] for _, _, p in sc for pr in p if pr[0] == "sphere"]
    zlim = (min(Zs), max(Zs))
    fig_w = 10.0
    ax_h = fig_w * 0.96 * Hh / W
    fig, axs = plt.subplots(2, 1, figsize=(fig_w, 2 * ax_h + 1.3))
    for ax, (t, ttl, p), e in zip(axs, sc, ext):
        draw(ax, p, view, zlim, args.fog)
        cx, cy = (e[0] + e[1]) / 2, (e[2] + e[3]) / 2
        ax.set_xlim(cx - W / 2, cx + W / 2); ax.set_ylim(cy - Hh / 2, cy + Hh / 2)
        ax.set_aspect("equal"); ax.axis("off")
        ax.set_title(ttl, fontsize=12.5, color=H.INK, loc="left")
    hd = [Line2D([0], [0], marker="o", ls="", markerfacecolor=COL[e], markeredgecolor=H.MUT, markeredgewidth=0.6,
                 markersize=10, label=e) for e in ("Ag", "S", "P", "Li", "Cl")]
    hd.append(Patch(facecolor=to_rgb(FACE) + (0.30,), edgecolor=EDGE, label="PS$_4$ tetrahedron"))
    hd.append(Line2D([0], [0], color=CONTACT, lw=3, label="Ag–S contact (≤ 2.9 Å)"))
    fig.legend(handles=hd, loc="lower center", ncol=7, frameon=False, fontsize=10, labelcolor=H.INK)
    fig.tight_layout(rect=(0, 0.045, 1, 1))
    fig.savefig(args.out, dpi=args.dpi, facecolor="white")
    print("saved", args.out)


if __name__ == "__main__":
    main()
