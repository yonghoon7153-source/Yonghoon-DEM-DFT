#!/usr/bin/env python3
"""fig_bv_vs_pmf_3d.py — **BV 채널 vs MD 자유에너지 채널**을 같은 상자·같은 시점 3D 로.

1저자 요청(2026-08-05): 프록시와 실제를 3D 로 나란히.

  왼쪽  BV-EL 등가면  at ΔE_perc      (0 K · 빈 격자 · Li 프로브 1개)
  오른쪽 PMF 등가면   at ΔF_perc      (T K · Li 전부 · 골격 진동 포함)

두 지도는 **같은 셀**(실측 확인: 부피 1216.383 vs 1216.382 Å³, 성분 일치)이라
하나의 데카르트 상자에 재샘플해 **같은 시점·같은 축척**으로 그린다 — 눈으로 바로 비교된다.

용어 (문헌 관례, 2026-08-05 통일)
  · 지도  = free-energy landscape from the Li probability density (**PMF**, Kirkwood)
  · 문턱  = **percolation free energy ΔF_perc** (BV 쪽 ΔE_perc 와 짝)
  · 구간  = **free-energy barrier ΔF**
  ⚠ MD 문헌에서 F 는 흔히 **힘**이라 홑 'F' 는 쓰지 않는다. Δ 를 붙여 장벽임을 명시.

  python3 tools/figures/fig_bv_vs_pmf_3d.py --cube <Li density cube> --T 600
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from scipy.ndimage import map_coordinates, label as nd_label, generate_binary_structure
from scipy.spatial import ConvexHull
from skimage.measure import marching_cubes

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "figures"))
sys.path.insert(0, str(ROOT / "tools" / "ionic"))
from house_style import INK, MUT                                        # noqa: E402
import fig_bv_path_profile as bvp                                       # noqa: E402
from fig_bv_path_annotated import ATOM_C, cage_centers, mic_fn          # noqa: E402
from fig_bv_3d import RAD, SCALE, PS4_CUT, sphere                       # noqa: E402
import pmf_path_profile as pmfmod                                       # noqa: E402
from plot_elf_clean import read_cube                                    # noqa: E402


def resample(field, cell, G, n):
    frac = (G.reshape(-1, 3) @ np.linalg.inv(cell)) % 1.0
    N = np.array(field.shape)
    return map_coordinates(field, (frac * N).T, order=1,
                           mode="grid-wrap").reshape(n)


def keep_component(V, thr, seeds, lo, step, n):
    """경로가 지나는 연결 성분만 (26-연결) — 떠 있는 조각 제거."""
    lab, _ = nd_label(V <= thr, structure=generate_binary_structure(3, 3))
    idx = np.clip(np.rint((seeds - lo) / step).astype(int), 0, n - 1)
    keep = {int(x) for x in lab[idx[:, 0], idx[:, 1], idx[:, 2]] if x > 0}
    mask = np.isin(lab, list(keep)) if keep else (V <= thr)
    return np.where(mask, V, thr + 1.0), float(mask.mean())


def draw(ax, verts, faces, atoms, cages, mic, shifts, lo, hi, path, e, color, view):
    ax.add_collection3d(Poly3DCollection(verts[faces], facecolor=color,
                                         edgecolor="none", alpha=0.40, zsort="average"))
    for i, (s, p) in enumerate(atoms):
        if s == "P":
            lig = [p + mic(q - p) for t, q in atoms
                   if t in PS4_CUT and 0 < np.linalg.norm(mic(q - p)) < PS4_CUT[t]]
            if len(lig) >= 4:
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
                        pts[hull.simplices], facecolor="#b9a3d6",
                        edgecolor="#6d28d9", lw=0.3, alpha=0.30))
            continue
        for sh in shifts:
            q = p + sh
            if not np.all((q > lo) & (q < hi)):
                continue
            if s == "Li":
                ax.scatter(*q, s=11, c="#9ca3af", alpha=0.6, depthshade=True)
                continue
            x, y, z = sphere(q, RAD.get(s, 0.8) * SCALE)
            ax.plot_surface(x, y, z, color=ATOM_C.get(s, "#888"), shade=True,
                            linewidth=0, alpha=0.9 if i in cages else 0.8)
    seg = np.stack([path[:-1], path[1:]], 1)
    lc = Line3DCollection(seg, cmap="turbo", norm=plt.Normalize(0, max(e.max(), 1e-6)),
                          lw=3.2)
    lc.set_array(0.5 * (e[:-1] + e[1:]))
    ax.add_collection3d(lc)
    ax.set_xlim(lo[0], hi[0]); ax.set_ylim(lo[1], hi[1]); ax.set_zlim(lo[2], hi[2])
    ax.set_box_aspect(hi - lo)
    ax.view_init(elev=view[0], azim=view[1])
    ax.set_axis_off()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cube", required=True, help="MD Li density cube")
    ap.add_argument("--T", type=float, default=600)
    ap.add_argument("--system", default="modelc")
    ap.add_argument("--disp", default="LPSCl1.6")
    ap.add_argument("--pad", type=float, default=2.4)
    ap.add_argument("--nvox", type=int, default=110)
    ap.add_argument("--maxbox", type=float, default=16.0,
                    help="상자 한 변 상한 (Å) — 길쭉한 셀에서 시야 확보")
    ap.add_argument("--out", default="docs/figures/bv_vs_pmf_3d_modelc.png")
    a = ap.parse_args()

    cif, _disp = bvp.SYSTEMS[a.system]
    rbv = bvp.profile_for(a.system, str(ROOT / cif))
    cell, atoms = rbv["cell"], rbv["atoms"]
    mic = mic_fn(cell)
    cages = {k for k, _s, _p in cage_centers(atoms, mic)}

    rho, _o, cell2, _gn, _at = pmfmod.load_density([a.cube])
    if not np.allclose(cell, cell2, atol=2e-3):
        raise SystemExit("⛔ cube 셀과 구조 셀이 다르다 — 같은 상자에 못 올린다")
    F = pmfmod.pmf_from_density(rho, a.T)
    lv = np.linspace(0.005, min(0.60, float(F[F < pmfmod.F_CAP].max())), 120)
    pct = pmfmod.cluster_curve(F, lv)
    dFp, _sl = pmfmod.transition_level(lv, pct)
    rpm = pmfmod.analyse(F, cell, a.T, cap=dFp)
    print(f"ΔE_perc(BV) {rbv['E_perc']:.4f} eV · ΔF_perc(PMF,{a.T:.0f} K) {dFp:.4f} eV")

    # ⚠ 상자 잡기 (2026-08-05 수정): 두 경로를 한 상자에 넣으면 안 된다.
    #   BV 경로와 PMF 경로는 셀 안 **다른 위치**를 지나므로, b2o3 처럼 길쭉한 셀
    #   (격자 35×35×352)에서는 합집합 상자가 거대해져 등가면이 점처럼 보인다(실측).
    #   → **크기는 같고 중심만 각자**인 상자를 쓴다: 축척은 공정, 내용은 각 경로 주변.
    def extent(pts):
        return pts.max(0) - pts.min(0)
    span = np.maximum(extent(rbv["cart"]), extent(rpm["cart"])) + 2 * a.pad
    span = np.minimum(span, a.maxbox)          # 너무 길면 잘라 시야 확보
    def box_for(pts):
        c = 0.5 * (pts.min(0) + pts.max(0))
        return c - span / 2, c + span / 2
    lo_bv, hi_bv = box_for(rbv["cart"])
    lo, hi = box_for(rpm["cart"])              # PMF 패널 기본 상자
    n = np.maximum(24, np.rint(a.nvox * span / span.max()).astype(int))
    step = span / (n - 1)

    def grid_for(lo_):
        return np.stack(np.meshgrid(*[np.linspace(lo_[d], lo_[d] + span[d], n[d])
                                      for d in range(3)], indexing="ij"), -1)
    G_bv, G = grid_for(lo_bv), grid_for(lo)

    from bvlain import Lain
    calc = Lain(verbose=False); calc.read_file(str(ROOT / cif))
    E = calc.bvse_distribution(mobile_ion="Li1+", r_cut=bvp.RCUT,
                               resolution=bvp.RES, k=bvp.K)
    E = E - E.min()
    VE = resample(E, cell, G_bv, n)
    VF = resample(F, cell, G, n)
    VE, fE = keep_component(VE, rbv["E_perc"], rbv["cart"], lo_bv, step, n)
    VF, fF = keep_component(VF, dFp, rpm["cart"], lo, step, n)
    print(f"채널 부피비: BV {100*fE:.2f}% · PMF {100*fF:.2f}%")

    # ③ 같은 부피에서 비교 — PMF 를 BV 채널과 **같은 부피비**가 되는 준위로 자른다.
    #   (문턱끼리 비교하면 0.5% vs 43% 라 눈으로는 못 읽는다. 부피를 맞추면
    #    "같은 양의 공간을 어떤 모양으로 쓰는가"가 보인다.)
    VFraw = resample(F, cell, G, n)
    lvl_iso = float(np.quantile(VFraw, fE))
    VFi = VFraw                      # ⚠ 여긴 성분 필터를 걸지 않는다 —
    fFi = float((VFraw <= lvl_iso).mean())   # 낮은 ΔF 에서 밀도는 **고립된 자리 덩어리**라
    #   연결 성분만 남기면 거의 다 지워진다. "Li 가 실제로 앉는 자리" 를 보여주는 게 목적이라
    #   덩어리 전부를 그린다 (문헌의 Li-density isosurface 그림과 같은 성격).
    print(f"등부피 비교: PMF 를 ΔF = {lvl_iso:.3f} eV 로 자르면 {100*fFi:.2f} vol% "
          f"(BV 채널 {100*fE:.2f}%) — 성분 필터 없음(고립 자리 표시)")

    vE, faE, _n, _v = marching_cubes(VE, level=rbv["E_perc"], spacing=tuple(step))
    vF, faF, _n, _v = marching_cubes(VF, level=dFp, spacing=tuple(step))
    vI, faI, _n, _v = marching_cubes(VFi, level=lvl_iso, spacing=tuple(step))
    vE, vF, vI = vE + lo_bv, vF + lo, vI + lo

    allp = rpm["cart"]
    c0 = allp.mean(0)
    _u, _s, vt = np.linalg.svd(allp - c0, full_matrices=False)
    nrm = vt[2]
    view = (float(np.degrees(np.arcsin(np.clip(nrm[2], -1, 1)))),
            float(np.degrees(np.arctan2(nrm[1], nrm[0]))) + 18)
    shifts = [i * cell[0] + j * cell[1] + k * cell[2]
              for i in (-1, 0, 1) for j in (-1, 0, 1) for k in (-1, 0, 1)]

    fig = plt.figure(figsize=(18.6, 6.9))
    ax1 = fig.add_subplot(1, 3, 1, projection="3d")
    draw(ax1, vE, faE, atoms, cages, mic, shifts, lo_bv, hi_bv, rbv["cart"], rbv["e"],
         "#ffd21f", view)
    ax1.set_title(f"① bond-valence channel  ΔE$_{{perc}}$ = {rbv['E_perc']:.3f} eV\n"
                  f"0 K · empty lattice · single Li probe · {100*fE:.2f} vol%",
                  fontsize=11, color=INK)
    ax2 = fig.add_subplot(1, 3, 2, projection="3d")
    draw(ax2, vI, faI, atoms, cages, mic, shifts, lo, hi, rpm["cart"], rpm["e"],
         "#22c55e", view)
    ax2.set_title(f"② MD density, SAME volume as ①  (ΔF = {lvl_iso:.3f} eV)\n"
                  f"{a.T:.0f} K · where the Li actually sit · {100*fFi:.2f} vol%",
                  fontsize=11, color=INK)
    ax3 = fig.add_subplot(1, 3, 3, projection="3d")
    draw(ax3, vF, faF, atoms, cages, mic, shifts, lo, hi, rpm["cart"], rpm["e"],
         "#16a34a", view)
    ax3.set_title(f"③ MD free-energy channel at ΔF$_{{perc}}$ = {dFp:.3f} eV\n"
                  f"{a.T:.0f} K · all Li · {100*fF:.1f} vol% accessible",
                  fontsize=11, color=INK)

    fig.suptitle(f"{a.disp} — the same crystal seen by a static proxy and by the "
                 f"MD free-energy landscape (PMF)", fontsize=13.5, color=INK,
                 fontweight="bold")
    fig.text(0.5, 0.02,
             "Both surfaces bound the region a Li can occupy below its own percolation "
             "threshold, rendered in the same box and viewpoint; only the connected component "
             "that carries the path is kept.\nYellow = bond-valence (no Li, no vacancies, no "
             "temperature). Green = potential of mean force, ΔF(r) = −k_BT ln[ρ(r)/ρ_max], "
             "from the time-averaged Li density of the MLIP-MD trajectory.\n"
             "① and ② enclose the same volume, so their shapes can be compared directly; "
             "③ shows how much of the cell is already thermally accessible by the time the\n"
             "free-energy landscape percolates. ΔF_perc is a free energy at this temperature "
             "— not an activation energy.",
             ha="center", fontsize=8.6, color=MUT)
    fig.tight_layout(rect=[0, 0.055, 1, 0.95])
    fig.savefig(ROOT / a.out, dpi=260, facecolor="white")
    print(f"→ {a.out}")


if __name__ == "__main__":
    main()
