#!/usr/bin/env python3
"""fig_bv_path_explainer.py — BV percolation 경로 프로파일 **처음 보는 사람용 주석판**.

1저자 요청(2026-08-05): "어떻게 해석하면 되는지 처음 보는 사람도 이해되게".
bv_path_profile_4sys.png 는 4계 비교용이라 설명이 없다. 이건 한 계(LPSCl1.6)만 크게
띄우고 골짜기·봉우리·문턱·홉거리에 라벨을 달아 **그림 하나로 읽는 법이 닫히게** 한다.

입력은 등록 CSV (db/properties/bv_path_profile_origin.csv) — 다시 계산하지 않는다.
따라서 bvlain 없이도 돌고, 4계 그림과 **같은 데이터**임이 보장된다.

  python3 tools/figures/fig_bv_path_explainer.py
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
from house_style import INK, MUT, SYS                                  # noqa: E402

CSV = ROOT / "db/properties/bv_path_profile_origin.csv"
OUT = ROOT / "docs/figures/bv_path_profile_explainer.png"
# 그림에 쓸 계 — 봉우리가 규칙적이라 '우물–안장 반복'이 가장 또렷하다
SYSTEM, DISPLAY, E_PERC, AXIS = "modelc", "LPSCl1.6", 0.2283, "[010]"


def load(system):
    with open(CSV, encoding="utf-8-sig") as f:
        rows = [r for r in csv.reader(f) if r and not r[0].lstrip('"').startswith("#")]
    hdr = rows[0]
    ix, iy = hdr.index(f"{system}_d_A"), hdr.index(f"{system}_E_eV")
    d, e = [], []
    for r in rows[1:]:
        if r[ix].strip():
            d.append(float(r[ix])); e.append(float(r[iy]))
    return np.array(d), np.array(e)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()

    d, e = load(SYSTEM)
    col = SYS[SYSTEM]

    fig, ax = plt.subplots(figsize=(10.2, 5.4))
    # 문턱 아래 = 서로 이어진 영역
    ax.axhspan(0, E_PERC, color="#f1f5f9", zorder=0)
    ax.plot(d, e, color=col, lw=2.0, zorder=3)
    ax.axhline(E_PERC, ls="--", lw=1.2, color=INK, zorder=2)

    # 봉우리·골짜기 찾기
    pk = [i for i in range(1, len(e) - 1) if e[i] > e[i - 1] and e[i] >= e[i + 1]]
    vl = [i for i in range(1, len(e) - 1) if e[i] < e[i - 1] and e[i] <= e[i + 1]]
    imax = int(np.argmax(e))

    # ── 라벨 (영어만 — 하우스 규칙) ────────────────────────────────────
    ax.annotate("valley = a Li site\n(comfortable spot)",
                xy=(d[vl[2]], e[vl[2]]), xytext=(d[vl[2]] - 0.4, -0.052),
                ha="center", fontsize=10.5, color=INK,
                arrowprops=dict(arrowstyle="->", color=MUT, lw=1.1))
    ax.annotate("peak = bottleneck between two sites\n(the squeeze the ion must pass)",
                xy=(d[pk[1]], e[pk[1]]), xytext=(d[pk[1]] + 2.6, 0.310),
                ha="center", fontsize=10.5, color=INK,
                arrowprops=dict(arrowstyle="->", color=MUT, lw=1.1))
    ax.annotate(f"$E_{{perc}}$ = {E_PERC:.3f} eV — the highest bottleneck\n"
                f"on the easiest path that still crosses the cell {AXIS}",
                xy=(d[imax], e[imax]), xytext=(d[-1] * 0.60, 0.288),
                ha="left", fontsize=10.5, color=INK, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.2))

    # 봉우리 간격 = 경로상 부자리 간격 (⚠ 직선 Li–Li 홉 거리 3 Å 과 다른 양 —
    #   2026-08-05 리뷰 정정: 'one hop' 표기는 n_hop 의 d_hop 과 혼동을 유발해 철회)
    i0, i1 = pk[4], pk[5]
    y = 0.255
    ax.annotate("", xy=(d[i0], y), xytext=(d[i1], y),
                arrowprops=dict(arrowstyle="<->", color=MUT, lw=1.1))
    ax.text((d[i0] + d[i1]) / 2, y + 0.006,
            f"adjacent bottlenecks ≈ {d[i1] - d[i0]:.1f} Å apart along the path\n"
            f"(sub-site spacing — not the 3 Å straight-line Li–Li hop distance)",
            ha="center", fontsize=9, color=MUT)

    ax.text(10.4, 0.038, "below the dashed line =\nthe pockets that link into a crossing path",
            fontsize=10, color=MUT, va="center", ha="center",
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.9))

    ax.set_xlabel("Reaction coordinate — distance travelled along the path (Å)", fontsize=11.5)
    ax.set_ylabel("Bond-valence energy (eV)", fontsize=11.5)
    ax.set_title(f"How to read a BV percolation-path profile — {DISPLAY}, axis {AXIS}",
                 fontsize=13, color=INK, fontweight="bold")
    ax.set_xlim(-0.6, d[-1] + 0.6)
    ax.set_ylim(-0.075, 0.35)
    ax.set_yticks(np.arange(0, 0.36, 0.05))
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

    fig.text(0.5, -0.045,
             "One Li probe in a frozen, otherwise empty lattice: the y value is what a single "
             "ion would feel, not a measured barrier.\n"
             "Use it for the shape of the landscape and for screening — the barrier ranking "
             "between compositions is decided by MD.",
             ha="center", fontsize=9.5, color=MUT)
    fig.tight_layout()
    fig.savefig(a.out, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"→ {a.out}")
    print(f"   원본 데이터 {CSV.name} · {SYSTEM} · 봉우리 {len(pk)}개 · 길이 {d[-1]:.1f} Å")


if __name__ == "__main__":
    main()
