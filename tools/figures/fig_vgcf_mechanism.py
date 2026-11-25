#!/usr/bin/env python3
"""fig_vgcf_mechanism.py — 209 meV 가 confinement 인지 substrate 인지 가르는 그림.

설계
  같은 물리적 변화(**그래핀 벽 1L → 2L**)를 두 배치에 각각 가한다.
    · 표면  : Li 가 한쪽만 접촉 (자유 표면)
    · 갤러리: Li 가 두 벽 사이에 갇힘
  두 배치가 같게 반응하면 substrate(스크리닝·분극, 일반화 가능),
  다르게 반응하면 confinement(갤러리 전용).

⚠⚠ **표면 쪽 +11.9 meV 를 '약간 악화' 로 읽으면 안 된다.**
  path_thr = 0.05 eV/Å 에 이미지 간격 ~0.41 Å 이면 에너지 불확도가 ~20 meV 다.
  즉 11.9 meV 는 **0 과 구별되지 않는다.** 그림에도 그 허용오차 띠를 같이 그려서
  "0 이 아니다" 로 오독하지 못하게 한다.

  python3 tools/figures/fig_vgcf_mechanism.py
"""
import csv
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "figures"))
from house_style import INK, MUT, apply_axes                        # noqa: E402

SRC = ROOT / "db/properties/vgcf_hbn_neb_barriers_origin.csv"
OUT = ROOT / "docs/figures/vgcf_hbn/vgcf_mechanism.png"
CSVOUT = ROOT / "db/properties/vgcf_mechanism_origin.csv"

TOL = 20.0          # NEB 에너지 허용오차 (meV) — path_thr × 이미지 간격
KT = 25.69          # kT at 300 K (meV)
C_SURF, C_GAL = "#6b7280", "#0d9488"


def load():
    with open(SRC, encoding="utf-8-sig") as f:
        lines = [l for l in f if not l.lstrip("﻿").startswith("#")]
    return {r["case"]: r for r in csv.DictReader(lines)}


def main():
    R = load()
    ea = lambda k: float(R[k]["Ea_forward_meV"])                     # noqa: E731

    s1, s2 = ea("Li_on_graphene_1L"), ea("Li_on_graphene_2L")
    g1, g2 = ea("Li_in_gallery_1L1L"), ea("Li_in_gallery_2L1L")
    ds, dg = s2 - s1, g2 - g1

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.0, 5.0),
                                   gridspec_kw={"width_ratios": [1.25, 1]})

    # ── (a) 같은 변화, 두 배치 ────────────────────────────────────────────
    x = np.arange(2); w = 0.34
    for j, (lab, v1, v2, col) in enumerate((
            ("Li on free graphene surface", s1, s2, C_SURF),
            ("Li confined in the gallery\n(h-BN wall fixed at 1L)", g1, g2, C_GAL))):
        ax1.bar(x[j] - w / 2, v1, w, color=col, alpha=0.45, edgecolor=INK, lw=0.6,
                label="graphene wall 1L" if j == 0 else None)
        ax1.bar(x[j] + w / 2, v2, w, color=col, edgecolor=INK, lw=0.6,
                label="graphene wall 2L" if j == 0 else None)
        for xi, v in ((x[j] - w / 2, v1), (x[j] + w / 2, v2)):
            ax1.text(xi, v + 7, f"{v:.0f}", ha="center", fontsize=9.5, color=INK)
        d = v2 - v1
        ax1.annotate("", xy=(x[j] + w / 2, v2), xytext=(x[j] - w / 2, v1),
                     arrowprops=dict(arrowstyle="->", color=col, lw=2.0,
                                     shrinkA=6, shrinkB=20,   # 화살촉이 값 라벨을 덮지 않게
                                     connectionstyle="arc3,rad=-0.25"))
        # ⚠ 델타 라벨은 **고정 높이**에 둔다. max(v1,v2)+42 로 두면 갤러리 쪽(357)에서
        #   범례와 겹친다(실측).
        ax1.text(x[j], 505, f"{d:+.0f} meV", ha="center", fontsize=12.5,
                 color=col, fontweight="bold")
    ax1.axhspan(0, TOL, color="#fecaca", alpha=0.55, zorder=0)
    ax1.text(1.48, TOL + 16, f"NEB tolerance ±{TOL:.0f} meV", ha="right", va="bottom",
             fontsize=8.5, color="#b91c1c")
    ax1.set_xticks(x)
    ax1.set_xticklabels(["Li on free graphene surface",
                         "Li confined in the gallery\n(h-BN wall fixed at 1L)"], fontsize=10)
    ax1.set_ylim(0, 560)
    ax1.set_yticks([0, 100, 200, 300, 400])
    ax1.legend(frameon=False, fontsize=9, loc="upper left", ncol=2,
               bbox_to_anchor=(0.0, 0.88))
    apply_axes(ax1, ylabel="CI-NEB migration barrier (meV)",
               title="(a) The same wall change, two settings", fontsize=11.5)

    # ── (b) 효과 크기만 나란히 ────────────────────────────────────────────
    labs = ["on free surface", "under confinement"]
    vals = [ds, dg]
    cols = [C_SURF, C_GAL]
    ax2.barh(labs, vals, color=cols, edgecolor=INK, lw=0.6, height=0.5)
    ax2.axvline(0, color=INK, lw=1.0)
    ax2.axvspan(-TOL, TOL, color="#fecaca", alpha=0.55, zorder=0)
    for i, v in enumerate(vals):
        ax2.text(v + (18 if v > 0 else -18), i, f"{v:+.0f}", va="center",
                 ha="left" if v > 0 else "right", fontsize=12.5, color=cols[i],
                 fontweight="bold")
    # ⚠ 허용오차 라벨은 축 **안쪽 머리 공간**에 — (0, 1.45) 는 제목과 겹쳤다(실측).
    ax2.set_ylim(-0.62, 1.75)
    ax2.text(0, 1.52, f"±{TOL:.0f} meV tolerance", ha="center", va="center",
             fontsize=8.5, color="#b91c1c")
    ax2.set_xlim(-285, 115)
    apply_axes(ax2, xlabel="change in barrier on going 1L → 2L (meV)",
               title="(b) Effect size — surface is null", fontsize=11.5)

    fig.suptitle("h-BN@VGCF — the 209 meV drop is CONFINEMENT, not a better substrate",
                 fontsize=12.5, color=INK, y=1.0)
    # 결론 상자는 **figure 좌표**에 둔다 — axes 아래에 두면 x 축 라벨을 덮는다(실측).
    fig.text(0.5, 0.015,
             "The bilayer wall works ONLY when Li is confined.   "
             f"On a free surface the same change is {ds:+.0f} meV — inside the tolerance band, i.e. zero.",
             ha="center", fontsize=10, color=INK,
             bbox=dict(boxstyle="round,pad=0.45", fc="#f0fdfa", ec=C_GAL, lw=1.0))
    fig.tight_layout(rect=[0, 0.10, 1, 0.96])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"→ {OUT}")

    with open(CSVOUT, "w", newline="", encoding="utf-8-sig") as f:
        f.write("# VGCF confinement-vs-substrate 판정 — Origin-ready\n")
        f.write("# 같은 변화(그래핀 벽 1L→2L)를 표면/갤러리 두 배치에 각각 가한 결과\n")
        f.write(f"# ⚠ NEB 에너지 허용오차 ~{TOL:.0f} meV (path_thr 0.05 eV/A × 이미지간격 0.41 A).\n")
        f.write("#   표면 쪽 변화는 이 안이라 **0 과 구별되지 않는다** — '약간 악화'로 읽지 말 것.\n")
        f.write(f"# kT(300 K) = {KT} meV\n")
        w = csv.writer(f)
        w.writerow(["setting", "Ea_1L_meV", "Ea_2L_meV", "delta_meV", "within_tolerance"])
        w.writerow(["Li on free graphene surface", f"{s1:.2f}", f"{s2:.2f}",
                    f"{ds:+.2f}", "yes"])
        w.writerow(["Li confined in gallery (hBN wall 1L)", f"{g1:.2f}", f"{g2:.2f}",
                    f"{dg:+.2f}", "no"])
    print(f"→ {CSVOUT}")
    print(f"\n표면 {s1:.1f} → {s2:.1f}  ({ds:+.1f} meV, 허용오차 ±{TOL:.0f} 안 → 0)")
    print(f"갤러리 {g1:.1f} → {g2:.1f}  ({dg:+.1f} meV)")
    print(f"→ 같은 변화인데 {abs(dg / ds):.0f}배 차이 · 부호도 반대 ⇒ CONFINEMENT")


if __name__ == "__main__":
    main()
