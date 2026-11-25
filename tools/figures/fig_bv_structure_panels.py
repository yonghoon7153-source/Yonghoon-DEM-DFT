#!/usr/bin/env python3
"""fig_bv_structure_panels.py — 외부 발표자료식 **3패널 구조 그림** (pymatgen 기반).

1저자 요청(2026-08-05): POSCO 슬라이드의 3패널(구조 / 자리·경로 / BV 채널)을 우리 구조로.

  panel 1  framework  — PS₄ 사면체(투영 다각형) + 음이온 + Li
  panel 2  + 자리 라벨(P#·S#·Cl#·Li#) + **우리 percolation 경로**(화살표)
  panel 3  + **BV 채널** — 슬랩 안 최소투영 min_w E(x,y,w) ≤ E_perc 영역
            (= "이 두께 안에서 어디든 문턱 아래로 지나갈 수 있는 자리")

pymatgen 담당: 구조 읽기 · 격자/주기 이미지 · 근접 이웃(PS₄ 사면체 판정) · 분수좌표 변환.
BV 지도·경로는 fig_bv_path_profile.py(bvlain)에서 그대로 가져와 **같은 데이터**를 쓴다.

⚠ 채널 색(노랑)은 **표시**다. 단위·문턱은 캡션에 적고, 정량은 CSV.
⚠ 이 그림도 empty-lattice proxy — 조성 간 순위 인용 금지 (kb/concepts/bvse.md §8-10).

  python3 tools/figures/fig_bv_structure_panels.py --system modelc
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from scipy.ndimage import map_coordinates

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "figures"))
from house_style import INK, MUT                                        # noqa: E402
import fig_bv_path_profile as bvp                                       # noqa: E402
from fig_bv_path_annotated import ATOM_C, ATOM_R, cage_centers, mic_fn  # noqa: E402

PS4_CUT = {"S": 2.4, "O": 1.9}


def tetrahedra(struct, mic):
    """P 중심 사면체 = P 주변 결합 음이온 묶음 (pymatgen 구조 + MIC)."""
    sym = [str(s.specie) for s in struct]
    pos = np.array([s.coords for s in struct])
    out = []
    for i, s in enumerate(sym):
        if s != "P":
            continue
        lig = []
        for j, t in enumerate(sym):
            if t in PS4_CUT and np.linalg.norm(mic(pos[j] - pos[i])) < PS4_CUT[t]:
                lig.append(pos[i] + mic(pos[j] - pos[i]))
        if len(lig) >= 3:
            out.append((pos[i], np.array(lig)))
    return out


def project(v, e1, e2, nrm):
    return float(v @ e1), float(v @ e2), float(v @ nrm)


def draw_panel(ax, struct, tets, cages, e1, e2, nrm, c0, shifts, xlim, ylim,
               thick, labels=False):
    sym = [str(s.specie) for s in struct]
    pos = np.array([s.coords for s in struct])
    cage_ids = {k for k, _s, _p in cages}

    for p0, lig in tets:                       # PS₄ 사면체 = 투영 다각형
        for sh in shifts:
            q = np.array([project(x + sh - c0, e1, e2, nrm) for x in lig])
            cq = project(p0 + sh - c0, e1, e2, nrm)
            if abs(cq[2]) > thick + 1.6:
                continue
            if not (xlim[0] < cq[0] < xlim[1] and ylim[0] < cq[1] < ylim[1]):
                continue
            pts = q[:, :2]
            k = pts - pts.mean(0)
            order = np.argsort(np.arctan2(k[:, 1], k[:, 0]))
            ax.add_patch(Polygon(pts[order], closed=True, facecolor="#a78bc4",
                                 edgecolor="#7c3aed", lw=0.6, alpha=0.55, zorder=1))

    for k, (s, p) in enumerate(zip(sym, pos)):
        for sh in shifts:
            x, y, w = project(p + sh - c0, e1, e2, nrm)
            if abs(w) > thick or not (xlim[0] < x < xlim[1] and ylim[0] < y < ylim[1]):
                continue
            fade = 1.0 - 0.5 * abs(w) / thick
            ax.scatter([x], [y], s=ATOM_R.get(s, 40), c=ATOM_C.get(s, "#888"),
                       alpha=fade, edgecolors="white", linewidths=0.6, zorder=3)
            if k in cage_ids and abs(w) < 1.3:
                ax.scatter([x], [y], s=ATOM_R.get(s, 40) * 3.2, facecolors="none",
                           edgecolors=ATOM_C.get(s, "#888"), lw=0.9, alpha=0.5, zorder=2)
            if labels and abs(w) < 1.3:
                ax.text(x, y, f"{s}{k+1}", fontsize=4.6, color="black", ha="center",
                        va="center", zorder=6, fontweight="bold")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--system", default="modelc", choices=list(bvp.SYSTEMS))
    ap.add_argument("--thick", type=float, default=2.8, help="투영 슬랩 반두께 (Å)")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    from pymatgen.core import Structure

    cif, disp = bvp.SYSTEMS[a.system]
    r = bvp.profile_for(a.system, str(ROOT / cif))
    cart, cell = r["cart"], r["cell"]
    struct = Structure(cell, [s for s, _p in r["atoms"]],
                       np.array([p for _s, p in r["atoms"]]), coords_are_cartesian=True)
    mic = mic_fn(cell)
    cages = cage_centers(r["atoms"], mic)
    tets = tetrahedra(struct, mic)
    print(f"{disp}: {len(struct)} atoms · PS₄-type polyhedra {len(tets)} · cage centres {len(cages)}")

    # 투영면 = 경로 주평면 (경로가 안 뭉개짐)
    c0 = cart.mean(0)
    _u, _s, vt = np.linalg.svd(cart - c0, full_matrices=False)
    e1, e2, nrm = vt[0], vt[1], vt[2]
    P = np.array([project(v - c0, e1, e2, nrm) for v in cart])
    pad = 3.4
    xlim = (P[:, 0].min() - pad, P[:, 0].max() + pad)
    ylim = (P[:, 1].min() - pad, P[:, 1].max() + pad)
    shifts = [i * cell[0] + j * cell[1] + k * cell[2]
              for i in (-1, 0, 1) for j in (-1, 0, 1) for k in (-1, 0, 1)]

    fig, axes = plt.subplots(1, 3, figsize=(15.6, 5.6))
    for ax in axes:
        ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal")
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color("#d1d5db")

    draw_panel(axes[0], struct, tets, cages, e1, e2, nrm, c0, shifts, xlim, ylim, a.thick)
    axes[0].set_title("① framework — PS$_4$ polyhedra + anions + Li", fontsize=11, color=INK)

    draw_panel(axes[1], struct, tets, cages, e1, e2, nrm, c0, shifts, xlim, ylim,
               a.thick, labels=True)
    axes[1].plot(P[:, 0], P[:, 1], color="#dc2626", lw=2.6, zorder=5, alpha=0.9)
    n = len(P)
    for f in (0.22, 0.62):                       # 굵은 진행 화살표 (그쪽 Path 화살표 대응)
        i = int(f * n)
        axes[1].annotate("", xy=P[i + 4, :2], xytext=P[i, :2],
                         arrowprops=dict(arrowstyle="-|>,head_width=0.45,head_length=0.8",
                                         color="#dc2626", lw=3.0), zorder=6)
    axes[1].set_title(f"② sites + percolation path  {r['axis']}", fontsize=11, color=INK)

    # ── ③ BV 채널 (슬랩 최소투영) ──────────────────────────────────────
    from bvlain import Lain
    calc = Lain(verbose=False)
    calc.read_file(str(ROOT / cif))
    E = calc.bvse_distribution(mobile_ion="Li1+", r_cut=bvp.RCUT,
                               resolution=bvp.RES, k=bvp.K)
    E = E - E.min()
    N = np.array(E.shape)
    gx = np.linspace(xlim[0], xlim[1], 320)
    gy = np.linspace(ylim[0], ylim[1], 320)
    GX, GY = np.meshgrid(gx, gy)
    ws = np.linspace(-a.thick, a.thick, 13)
    inv = np.linalg.inv(cell)
    best = np.full(GX.shape, np.inf)
    for w in ws:                                  # 슬랩 두께 방향 최소 투영
        R = (c0 + GX[..., None] * e1 + GY[..., None] * e2 + w * nrm).reshape(-1, 3)
        f = (R @ inv) % 1.0
        # 삼선형 + 주기 랩 (최근접이면 윤곽이 계단진다)
        v = map_coordinates(E, (f * N).T, order=1, mode="grid-wrap")
        best = np.minimum(best, v.reshape(GX.shape))
    draw_panel(axes[2], struct, tets, cages, e1, e2, nrm, c0, shifts, xlim, ylim, a.thick)
    axes[2].contourf(GX, GY, best, levels=[0, r["E_perc"]], colors=["#ffe000"],
                     alpha=0.62, zorder=0)
    axes[2].contour(GX, GY, best, levels=[r["E_perc"]], colors=["#b45309"],
                    linewidths=0.7, zorder=1)
    axes[2].plot(P[:, 0], P[:, 1], color="#dc2626", lw=2.2, zorder=5, alpha=0.9)
    axes[2].set_title(f"③ BV channel  (min over ±{a.thick:.1f} Å slab ≤ "
                      f"$E_{{perc}}$ {r['E_perc']:.3f} eV)", fontsize=11, color=INK)

    fig.suptitle(f"{disp} — framework, Li percolation path, and BV channel   "
                 f"(projected on the path's principal plane)",
                 fontsize=13, color=INK, fontweight="bold")
    fig.text(0.5, 0.012,
             "Empty-lattice bond-valence proxy (one Li probe, frozen framework). "
             "The channel is where the BV energy stays below the percolation threshold "
             "somewhere within the slab.\nAbsolute barriers and composition ranking are "
             "determined by seed-ensemble MLIP-MD, not by this map.",
             ha="center", fontsize=8.8, color=MUT)
    fig.tight_layout(rect=[0, 0.045, 1, 0.96])
    out = a.out or f"docs/figures/bv_structure_panels_{a.system}.png"
    fig.savefig(ROOT / out, dpi=300, facecolor="white")
    print(f"→ {out}")


if __name__ == "__main__":
    main()
