#!/usr/bin/env python3
"""fig_bv_path_annotated.py — BV 경로 프로파일 **자리 라벨 + 구간별 장벽** 판.

1저자 질문(2026-08-05): 외부 발표자료(POSCO)의 "경로별 energy barrier" 그림처럼
우리도 되나? → 된다. 그 그림에 있고 우리 4계 판에 없던 두 가지를 채운다:
  ① 골짜기/봉우리마다 **결정학적 정체**를 붙인다 (어느 Li 자리인가 · 어느 음이온 창인가)
  ② **구간별 장벽**(직전 골짜기 → 그 봉우리)을 각각 표기한다 — 전체 문턱 하나가 아니라

우리가 그쪽보다 더 하는 것:
  - 병목을 만드는 **음이온 3개(창)** 를 이름과 반지름으로 명시 (그쪽은 s1/s2/s3 라벨만)
  - E_perc 와 **MD Eₐ 를 같은 그림에** — 프록시 한계를 그림이 스스로 말하게
  - E_1D/2D/3D 를 함께 표기 (차원별 문턱)
⚠ 그쪽 슬라이드의 σ(T) 표는 **모델 생성값**으로 판정됐다(kb/concepts/bvse.md §9).
  우리는 σ 표를 BV 로 만들지 않는다 — σ·Eₐ 는 MD 담당.

  python3 tools/figures/fig_bv_path_annotated.py --system modelc
"""
import argparse
import csv
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "figures"))
from house_style import INK, MUT, SYS                                   # noqa: E402
import fig_bv_path_profile as bvp                                       # noqa: E402

ANION = ("S", "Cl", "O")
MD_EA = {"comp1": "0.253", "modelc": "0.197±0.032",
         "lpsocl": "0.287±0.024", "b2o3": "0.199±0.034"}


def mic_fn(cell):
    inv = np.linalg.inv(cell.T)

    def mic(v):
        f = inv @ v
        f -= np.round(f)
        return cell.T @ f
    return mic


def label_valley(r, atoms, mic):
    """골짜기 = Li 후보 자리. 가장 가까운 Li 와 음이온 배위로 정체를 쓴다."""
    dLi = sorted((float(np.linalg.norm(mic(p - r))), i)
                 for i, (s, p) in enumerate(atoms) if s == "Li")
    shell = sorted((float(np.linalg.norm(mic(p - r))), s)
                   for s, p in atoms if s in ANION)
    coord = {}
    for dist, s in shell:
        if dist <= 3.2:
            coord[s] = coord.get(s, 0) + 1
    cstr = "+".join(f"{n}{s}" for s, n in sorted(coord.items())) or "—"
    kind = "on Li" if dLi and dLi[0][0] < 0.6 else "vacant"
    return f"{kind}\n{cstr}", dLi[0][0] if dLi else np.nan


def label_saddle(r, atoms, mic):
    """봉우리 = 병목. 이온이 실제로 통과하는 **음이온 창**(가장 가까운 3개)."""
    near = sorted((float(np.linalg.norm(mic(p - r))), s)
                  for s, p in atoms if s in ANION)[:3]
    names = "".join(s for _, s in near)
    return f"{names}\nwindow {near[0][0]:.2f} Å", near[0][0]


# ── 케이지 (argyrodite) ────────────────────────────────────────────────
#   케이지 중심 = **P 에 결합하지 않은 음이온** = free S²⁻ / Cl⁻ (그리고 free O).
#   PS₄ 의 S 는 골격이라 중심이 아니다. 이 정의로 골짜기를 케이지에 배정하면
#   "케이지 안 도약(intra)" vs "케이지 사이 도약(inter)" 이 객관적으로 갈린다 —
#   우리 vacancy paradox 서술("케이지 안은 넓은데 케이지 사이 점프가 드물다")의
#   그림 버전이다.
P_BOND = {"S": 2.4, "O": 1.9, "Cl": 3.0}


def cage_centers(atoms, mic):
    P = [p for s, p in atoms if s == "P"]
    out = []
    for k, (s, p) in enumerate(atoms):
        if s not in ANION:
            continue
        rc = P_BOND.get(s, 2.4)
        if not any(np.linalg.norm(mic(q - p)) < rc for q in P):
            out.append((k, s, p))
    return out


def cage_of(r, cages, mic):
    ds = [(float(np.linalg.norm(mic(p - r))), k, s) for k, s, p in cages]
    ds.sort()
    return (ds[0][1], ds[0][2], ds[0][0]) if ds else (-1, "?", np.nan)


# VESTA 풍 원소색 (진한 배경 없음 → 하우스 팔레트 대신 구조 그림 관례)
ATOM_C = {"Li": "#9ca3af", "P": "#7c3aed", "S": "#e0b000", "Cl": "#3E8E41",
          "O": "#E8482B", "B": "#0284c7"}
ATOM_R = {"Li": 26, "P": 62, "S": 78, "Cl": 82, "O": 58, "B": 50}


def draw_structure(ax, cart, atoms, cages, cell, e, seg, htype, disp, axis,
                   thick=2.6, box_ar=3.05):
    """경로를 **구조 위에** 얹은 투영도.

    투영면 = 경로 점들의 주성분 2개 (PCA) — 경로가 가장 넓게 펼쳐지는 평면이라
    굴곡이 안 뭉갠다. 원자는 주기 이미지 3³ 를 만들어 그 평면 ±thick Å 안의 것만.
    선 색 = BV 에너지 (아래 프로파일과 같은 물리량, 같은 스케일).
    """
    from matplotlib.collections import LineCollection
    c0 = cart.mean(0)
    _u, _s, vt = np.linalg.svd(cart - c0, full_matrices=False)
    e1, e2, nrm = vt[0], vt[1], vt[2]

    shifts = [i * cell[0] + j * cell[1] + k * cell[2]
              for i in (-1, 0, 1) for j in (-1, 0, 1) for k in (-1, 0, 1)]
    P = cart @ np.vstack([e1, e2]).T - c0 @ np.vstack([e1, e2]).T
    xlim = [P[:, 0].min() - 3.0, P[:, 0].max() + 3.0]
    ylim = [P[:, 1].min() - 2.2, P[:, 1].max() + 2.2]
    # 패널 상자를 꽉 채우도록 종횡비 보정 (equal aspect 유지 → 왜곡 없음)
    wx, wy = xlim[1] - xlim[0], ylim[1] - ylim[0]
    if wx / wy < box_ar:
        cx = 0.5 * (xlim[0] + xlim[1]); wx = wy * box_ar
        xlim = [cx - wx / 2, cx + wx / 2]
    else:
        cy = 0.5 * (ylim[0] + ylim[1]); wy = wx / box_ar
        ylim = [cy - wy / 2, cy + wy / 2]
    xlim, ylim = tuple(xlim), tuple(ylim)
    cage_ids = {k for k, _s, _p in cages}

    for k, (s, p) in enumerate(atoms):
        for sh in shifts:
            v = p + sh - c0
            w = float(v @ nrm)
            if abs(w) > thick:
                continue
            x, y = float(v @ e1), float(v @ e2)
            if not (xlim[0] < x < xlim[1] and ylim[0] < y < ylim[1]):
                continue
            fade = 1.0 - 0.55 * abs(w) / thick          # 평면에서 멀수록 흐리게
            ax.scatter([x], [y], s=ATOM_R.get(s, 40), c=ATOM_C.get(s, "#888"),
                       alpha=fade, edgecolors="white", linewidths=0.6, zorder=2)
            if k in cage_ids and abs(w) < 1.2:          # 케이지 중심 강조
                ax.scatter([x], [y], s=ATOM_R.get(s, 40) * 3.4, facecolors="none",
                           edgecolors=ATOM_C.get(s, "#888"), linewidths=1.0,
                           alpha=0.55, zorder=1)

    pts = np.column_stack([P[:, 0], P[:, 1]]).reshape(-1, 1, 2)
    lc = LineCollection(np.concatenate([pts[:-1], pts[1:]], axis=1), cmap="turbo",
                        norm=plt.Normalize(0, e.max()), linewidths=3.4, zorder=4)
    lc.set_array(0.5 * (e[:-1] + e[1:]))
    ax.add_collection(lc)
    cb = ax.figure.colorbar(lc, ax=ax, pad=0.010, fraction=0.020, aspect=26)
    cb.set_label("BV energy (eV)", fontsize=9)
    cb.ax.tick_params(labelsize=8)

    for (j, i, _b), ht in zip(seg, htype):              # 병목 표시
        ax.scatter([P[i, 0]], [P[i, 1]], s=95, marker="X",
                   c=("#dc2626" if ht == "inter" else "#2563eb"),
                   edgecolors="white", linewidths=0.9, zorder=5)
    ax.annotate("", xy=P[-1], xytext=P[-4],
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=2.0), zorder=6)

    hs = [plt.Line2D([], [], ls="", marker="X", ms=9, mfc=c, mec="white", label=t)
          for c, t in (("#dc2626", "inter-cage bottleneck"), ("#2563eb", "intra-cage"))]
    hs += [plt.Line2D([], [], ls="", marker="o", ms=8, mfc="none",
                      mec="#3E8E41", label="cage centre (free S²⁻/Cl⁻)")]
    ax.legend(handles=hs, fontsize=8.5, loc="lower left", ncol=3, frameon=True,
              framealpha=0.92, edgecolor="none", borderpad=0.4)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("#d1d5db")
    ax.set_title(f"Percolation path through the framework — {disp}, axis {axis}"
                 f"   (projected on the path's principal plane, ±{thick:.1f} Å slab)",
                 fontsize=11.5, color=INK)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--system", default="modelc", choices=list(bvp.SYSTEMS))
    ap.add_argument("--out_png", default=None)
    ap.add_argument("--out_csv", default=None)
    ap.add_argument("--min_prom", type=float, default=0.02,
                    help="봉우리 프로미넌스 컷 (eV) — 잔물결 제외")
    a = ap.parse_args()

    cif, disp = bvp.SYSTEMS[a.system]
    r = bvp.profile_for(a.system, str(ROOT / cif))
    d, e, cart, atoms = r["d"], r["e"], r["cart"], r["atoms"]
    mic = mic_fn(r["cell"])

    # 봉우리/골짜기 (프로미넌스 컷) ─────────────────────────────────────
    pk = [i for i in range(1, len(e) - 1) if e[i] > e[i - 1] and e[i] >= e[i + 1]]
    pk = [i for i in pk if e[i] - min(e[:i].min(), e[i:].min()) >= a.min_prom]
    seg, prev = [], 0
    for i in pk:                              # 구간 = 직전 골짜기 → 이 봉우리
        j = int(np.argmin(e[prev:i + 1])) + prev
        seg.append((j, i, float(e[i] - e[j])))
        prev = i

    # 케이지 배정 → intra / inter 분류 → Path 묶음 ─────────────────────
    cages = cage_centers(atoms, mic)
    vcage = [cage_of(cart[j], cages, mic) for j, _i, _b in seg]
    vcage.append(cage_of(cart[seg[-1][1]], cages, mic))     # 마지막 봉우리 이후
    htype = []
    for k in range(len(seg)):
        nxt = vcage[k + 1][0] if k + 1 < len(vcage) else vcage[k][0]
        htype.append("inter" if nxt != vcage[k][0] else "intra")
    groups, g = [], 1                                        # 같은 종류 연속 = 한 Path
    for k in range(len(seg)):
        if k and htype[k] != htype[k - 1]:
            g += 1
        groups.append(g)

    print(f"\n{disp} · {r['axis']} · {len(seg)} 구간 (프로미넌스 ≥ {a.min_prom} eV) · "
          f"케이지 중심 {len(cages)}개 · inter {htype.count('inter')} / intra {htype.count('intra')}")
    rows = []
    for k, (j, i, db) in enumerate(seg, 1):
        vl, dli = label_valley(cart[j], atoms, mic)
        sd, wr = label_saddle(cart[i], atoms, mic)
        cid, csym, cd = vcage[k - 1]
        print(f"  {k}: {d[j]:5.2f}→{d[i]:5.2f} Å  ΔE {db:.3f} eV  [{htype[k-1]:5s} P{groups[k-1]}]"
              f" | valley {vl.replace(chr(10), ' ')} (Li {dli:.2f} Å, cage {csym}#{cid+1} {cd:.2f} Å)"
              f" | saddle {sd.replace(chr(10), ' ')}")
        rows.append({"segment": k, "path_group": f"Path {groups[k-1]}", "hop_type": htype[k - 1],
                     "s_valley_A": f"{d[j]:.3f}", "s_saddle_A": f"{d[i]:.3f}",
                     "E_valley_eV": f"{e[j]:.4f}", "E_saddle_eV": f"{e[i]:.4f}",
                     "barrier_eV": f"{db:.4f}",
                     "valley_site": vl.replace("\n", " "), "nearest_Li_A": f"{dli:.2f}",
                     "cage_center": f"{csym}#{cid+1}", "cage_dist_A": f"{cd:.2f}",
                     "saddle_window": sd.replace("\n", " "), "window_r_A": f"{wr:.3f}"})

    # ── 그림 (2패널: 구조 위 경로 / 프로파일) ──────────────────────────
    col = SYS[a.system]
    fig = plt.figure(figsize=(11.4, 9.2))
    gs = fig.add_gridspec(2, 1, height_ratios=[0.82, 1.32], hspace=0.20)
    axs = fig.add_subplot(gs[0])
    draw_structure(axs, cart, atoms, cages, r["cell"], e, seg, htype, disp, r["axis"])
    ax = fig.add_subplot(gs[1])
    ax.axhspan(0, r["E_perc"], color="#f1f5f9", zorder=0)
    ax.plot(d, e, color=col, lw=2.0, zorder=3)
    ax.axhline(r["E_perc"], ls="--", lw=1.2, color=INK, zorder=2)
    ax.text(d[-1], r["E_perc"] + 0.004, f"$E_{{perc}}$ = {r['E_perc']:.3f} eV",
            ha="right", fontsize=10, color=INK, fontweight="bold")

    top = e.max() + 0.135
    for k, (j, i, db) in enumerate(seg, 1):
        ax.plot([d[i], d[i]], [e[j], e[i]], color=MUT, lw=0.9, ls=":", zorder=2)
        ax.annotate("", xy=(d[i], e[i]), xytext=(d[i], e[j]),
                    arrowprops=dict(arrowstyle="<->", color=MUT, lw=0.9))
        ax.text(d[i] + 0.12, (e[i] + e[j]) / 2, f"{db:.3f}", fontsize=8.5,
                color=INK, va="center", fontweight="bold")
        sd, _ = label_saddle(cart[i], atoms, mic)
        ax.text(d[i], top - 0.006 - 0.030 * (k % 2), sd, fontsize=7.5, color=MUT,
                ha="center", va="top", linespacing=1.15)
        ax.plot(d[i], e[i], "o", ms=5, mfc="white", mec=col, mew=1.4, zorder=4)
        vl, _ = label_valley(cart[j], atoms, mic)
        ax.text(d[j], e[j] - 0.014, vl, fontsize=7, color=MUT, ha="center",
                va="top", linespacing=1.1)

    # Path 묶음 막대 (연속 같은 종류 = 한 Path)
    for g in sorted(set(groups)):
        ks = [k for k in range(len(seg)) if groups[k] == g]
        x0, x1 = d[seg[ks[0]][0]], d[seg[ks[-1]][1]]
        ht = htype[ks[0]]
        c = "#dc2626" if ht == "inter" else "#2563eb"
        yb = -0.050
        ax.annotate("", xy=(x1, yb), xytext=(x0, yb),
                    arrowprops=dict(arrowstyle="|-|,widthA=0.4,widthB=0.4", color=c, lw=1.6))
        ax.text((x0 + x1) / 2, yb - 0.008, f"Path {g} ({ht})", fontsize=8.5, color=c,
                ha="center", va="top", fontweight="bold")

    ax.set_xlabel("Reaction coordinate (Å)", fontsize=11.5)
    ax.set_ylabel("Bond-valence energy (eV)", fontsize=11.5)
    ref = r["ref"]
    ax.set_title(f"BV percolation path, segment barriers — {disp}  axis {r['axis']}\n"
                 f"$E_{{1D}}$/$E_{{2D}}$/$E_{{3D}}$ = {ref['E_1D']:.3f} / {ref['E_2D']:.3f} / "
                 f"{ref['E_3D']:.3f} eV      MD $E_a$ = {MD_EA[a.system]} eV",
                 fontsize=12.5, color=INK, fontweight="bold")
    ax.set_xlim(-0.5, d[-1] + 0.9)
    ax.set_ylim(-0.082, top)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.text(0.5, -0.03,
             "Empty-lattice proxy: one Li probe in a frozen lattice. Segment barriers describe "
             "the landscape shape, not measured activation energies —\nthe Ea/σ ranking between "
             "compositions is determined by seed-ensemble MLIP-MD.",
             ha="center", fontsize=9, color=MUT)
    out = a.out_png or f"docs/figures/bv_path_annotated_{a.system}.png"
    fig.savefig(ROOT / out, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"→ {out}")

    outc = a.out_csv or f"db/properties/bv_path_segments_{a.system}.csv"
    with open(ROOT / outc, "w", newline="", encoding="utf-8-sig") as f:
        f.write(f"# BV percolation path segment barriers - {disp}, axis {r['axis']}, "
                f"E_perc {r['E_perc']:.4f} eV.\n")
        f.write("# barrier_eV = E(saddle) - E(preceding valley) along the min-energy-line-integral "
                "path under the percolation ceiling.\n")
        f.write("# valley_site: 'on Li' if a framework Li sits within 0.6 A, else 'vacant' "
                "(empty-lattice map: valleys are CANDIDATE sites); coordination = anions within 3.2 A.\n")
        f.write("# saddle_window: the three nearest anions forming the bottleneck; window_r_A = "
                "distance to the closest of them.\n")
        f.write("# EMPTY-LATTICE PROXY - not a measured barrier. Ea/sigma ranking is decided by MD "
                f"(MD Ea = {MD_EA[a.system]} eV). See kb/concepts/bvse.md sec 8-10.\n")
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    print(f"→ {outc}")


if __name__ == "__main__":
    main()
