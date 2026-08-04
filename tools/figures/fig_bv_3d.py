#!/usr/bin/env python3
"""fig_bv_3d.py — BV 채널 **3D 등가면** + 골격 + percolation 경로 (VESTA 없이 repo 안에서).

1저자 요청(2026-08-05): 2D 투영판이 답답하다 → 3D 로.

만드는 법
  1. 경로를 감싸는 **데카르트 박스**를 잡고 그 안에서 BV 지도를 정규 격자로 재샘플
     (삼선형 + 주기 랩). 비스듬한 셀을 그대로 marching cubes 에 넣으면 격자가
     기울어져 면이 찌그러지는데, 데카르트 재샘플이 그걸 없앤다.
  2. `skimage.measure.marching_cubes(level=E_perc)` → 채널 등가면 (진짜 3D 표면)
  3. PS₄ 다면체는 ConvexHull 면으로, 음이온/Li 는 구, 경로는 3D 선
  4. 두 시점(경로 주평면 정면 / 비스듬)을 나란히

⚠ 등가면 높이 = **E_perc** (percolation 문턱) — "이 안이면 셀을 관통해 이어진다"는
  면이지 등확률면이 아니다. 단위 eV(above-min), empty-lattice proxy.
⚠ 조성 간 순위 인용 금지 (kb/concepts/bvse.md §8-10). 그림은 지형·연결성 담당.

  python3 tools/figures/fig_bv_3d.py --system modelc
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from scipy.ndimage import map_coordinates
from scipy.spatial import ConvexHull
from skimage.measure import marching_cubes

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "figures"))
from house_style import INK, MUT                                        # noqa: E402
import fig_bv_path_profile as bvp                                       # noqa: E402
from fig_bv_path_annotated import ATOM_C, cage_centers, mic_fn          # noqa: E402

SCALE = 0.62          # 구 반지름 축소 — 채널이 가려지지 않게
RAD = {"Li": 0.45, "P": 0.62, "S": 0.95, "Cl": 1.00, "O": 0.72, "B": 0.55}
PS4_CUT = {"S": 2.4, "O": 1.9}


def sphere(c, r, n=11):
    u = np.linspace(0, 2 * np.pi, 2 * n)
    v = np.linspace(0, np.pi, n)
    x = c[0] + r * np.outer(np.cos(u), np.sin(v))
    y = c[1] + r * np.outer(np.sin(u), np.sin(v))
    z = c[2] + r * np.outer(np.ones_like(u), np.cos(v))
    return x, y, z


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--system", default="modelc", choices=list(bvp.SYSTEMS))
    ap.add_argument("--pad", type=float, default=2.6, help="경로 둘레 여백 (Å)")
    ap.add_argument("--nvox", type=int, default=110, help="재샘플 격자 최장변 분할 수")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    cif, disp = bvp.SYSTEMS[a.system]
    r = bvp.profile_for(a.system, str(ROOT / cif))
    cart, cell, Eperc = r["cart"], r["cell"], r["E_perc"]
    mic = mic_fn(cell)
    atoms = r["atoms"]
    cages = {k for k, _s, _p in cage_centers(atoms, mic)}

    # ── 1. 경로를 감싸는 데카르트 박스 ────────────────────────────────
    lo = cart.min(0) - a.pad
    hi = cart.max(0) + a.pad
    span = hi - lo
    n = np.maximum(24, np.rint(a.nvox * span / span.max()).astype(int))
    gx = [np.linspace(lo[d], hi[d], n[d]) for d in range(3)]
    G = np.stack(np.meshgrid(*gx, indexing="ij"), -1)

    from bvlain import Lain
    calc = Lain(verbose=False)
    calc.read_file(str(ROOT / cif))
    E = calc.bvse_distribution(mobile_ion="Li1+", r_cut=bvp.RCUT,
                               resolution=bvp.RES, k=bvp.K)
    E = E - E.min()
    N = np.array(E.shape)
    frac = (G.reshape(-1, 3) @ np.linalg.inv(cell)) % 1.0
    V = map_coordinates(E, (frac * N).T, order=1, mode="grid-wrap").reshape(n)
    print(f"{disp}: 박스 {span.round(1)} Å · 격자 {tuple(n)} · 채널 부피비 "
          f"{100*(V <= Eperc).mean():.1f}% @ E_perc {Eperc:.3f} eV")

    # 경로가 지나는 **연결 성분만** 남긴다 (26-연결) — 떠 있는 조각이 사라져
    #   그림이 깨끗해지고, 남는 것이 곧 "관통하는 그 통로"라 의미도 정확해진다.
    from scipy.ndimage import label as nd_label, generate_binary_structure
    lab, _nf = nd_label(V <= Eperc, structure=generate_binary_structure(3, 3))
    pidx = np.rint((cart - lo) / (span / (n - 1))).astype(int)
    pidx = np.clip(pidx, 0, n - 1)
    keep = {int(x) for x in lab[pidx[:, 0], pidx[:, 1], pidx[:, 2]] if x > 0}
    mask = np.isin(lab, list(keep)) if keep else (V <= Eperc)
    Vm = np.where(mask, V, Eperc + 1.0)
    print(f"   채널 성분 {len(keep)}개 유지 · 부피비 {100*mask.mean():.2f}%")
    verts, faces, _nrm, _val = marching_cubes(Vm, level=Eperc,
                                              spacing=tuple(span / (n - 1)))
    verts = verts + lo
    print(f"   등가면: {len(verts)} verts · {len(faces)} faces")

    # ── 2. 그림 (두 시점) ────────────────────────────────────────────
    c0 = cart.mean(0)
    _u, _s, vt = np.linalg.svd(cart - c0, full_matrices=False)
    nrm = vt[2]
    el0 = float(np.degrees(np.arcsin(np.clip(nrm[2], -1, 1))))
    az0 = float(np.degrees(np.arctan2(nrm[1], nrm[0])))
    views = [(el0, az0, "view along path normal"), (22, az0 + 55, "tilted view")]
    shifts = [i * cell[0] + j * cell[1] + k * cell[2]
              for i in (-1, 0, 1) for j in (-1, 0, 1) for k in (-1, 0, 1)]

    fig = plt.figure(figsize=(14.6, 7.4))
    for k, (el, az, vname) in enumerate(views):
        ax = fig.add_subplot(1, 2, k + 1, projection="3d")
        ax.add_collection3d(Poly3DCollection(
            verts[faces], facecolor="#ffd21f", edgecolor="none",
            alpha=0.42, zsort="average"))

        for i, (s, p) in enumerate(atoms):        # PS₄ 다면체 (주기 이미지 포함)
            if s != "P":
                continue
            lig = [p + mic(q - p) for t, q in atoms
                   if t in PS4_CUT and 0 < np.linalg.norm(mic(q - p)) < PS4_CUT[t]]
            if len(lig) < 4:
                continue
            base = np.array(lig)
            for sh in shifts:
                pts = base + sh
                if not (np.all(pts.mean(0) > lo - 1.0) and np.all(pts.mean(0) < hi + 1.0)):
                    continue
                try:
                    hull = ConvexHull(pts)
                except Exception:
                    continue
                ax.add_collection3d(Poly3DCollection(
                    pts[hull.simplices], facecolor="#b9a3d6", edgecolor="#6d28d9",
                    lw=0.35, alpha=0.34))

        for i, (s, p) in enumerate(atoms):        # 원자 구 (주기 이미지 포함)
            if s == "P":
                continue                          # 다면체 안이라 생략
            for sh in shifts:
                q = p + sh
                if not np.all((q > lo) & (q < hi)):
                    continue
                if s == "Li":
                    ax.scatter(*q, s=13, c="#9ca3af", alpha=0.7, depthshade=True)
                    continue
                x, y, z = sphere(q, RAD.get(s, 0.8) * SCALE)
                ax.plot_surface(x, y, z, color=ATOM_C.get(s, "#888"),
                                shade=True, linewidth=0,
                                alpha=0.95 if i in cages else 0.85)

        seg = np.stack([cart[:-1], cart[1:]], 1)  # 경로 (에너지 색)
        lc = Line3DCollection(seg, cmap="turbo",
                              norm=plt.Normalize(0, r["e"].max()), lw=3.4)
        lc.set_array(0.5 * (r["e"][:-1] + r["e"][1:]))
        ax.add_collection3d(lc)

        ax.set_xlim(lo[0], hi[0]); ax.set_ylim(lo[1], hi[1]); ax.set_zlim(lo[2], hi[2])
        ax.set_box_aspect(span)
        ax.view_init(elev=el, azim=az)
        ax.set_axis_off()
        ax.set_title(vname, fontsize=11, color=MUT)
        if k == 1:
            cb = fig.colorbar(lc, ax=ax, pad=0.02, fraction=0.022, aspect=24)
            cb.set_label("BV energy along path (eV)", fontsize=9)
            cb.ax.tick_params(labelsize=8)

    fig.suptitle(f"{disp} — BV channel isosurface at $E_{{perc}}$ = {Eperc:.3f} eV "
                 f"with the percolation path  (axis {r['axis']})",
                 fontsize=13.5, color=INK, fontweight="bold")
    fig.text(0.5, 0.025,
             "Yellow surface = the boundary of the region a Li probe can occupy below the "
             "percolation threshold (empty-lattice bond-valence map, eV above minimum).\n"
             "Purple polyhedra = PS₄/PS₃O units · spheres = S / Cl / O · small grey = Li · "
             "coloured line = the min-energy percolation path. Ranking of Ea between "
             "compositions is set by MLIP-MD, not by this map.",
             ha="center", fontsize=8.8, color=MUT)
    fig.tight_layout(rect=[0, 0.06, 1, 0.95])
    out = a.out or f"docs/figures/bv_3d_{a.system}.png"
    fig.savefig(ROOT / out, dpi=260, facecolor="white")
    print(f"→ {out}")


if __name__ == "__main__":
    main()
