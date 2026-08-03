#!/usr/bin/env python3
"""fig_msd_4sys.py — Li MSD(t) 4계 비교: LPSCl · LPSCl1.6 · LPSOCl · B2O3-doped.

기존 3계 그림(msd_LPSCl_LPSCl16_b2o3)에 **LPSOCl 을 추가**한 판. 1저자 요청 §3.
600/800/1000 K 3패널, 각 패널에 4계. 점선 = 2-50 ps 창의 선형 적합(D = 기울기/6).

  # 1) 먼저 곡선을 수확한다 (런 디렉토리가 있는 서버에서)
  python3 tools/figures/harvest_msd_curves.py --run lpsocl=~/work/runs/lpsocl_md/ladder \\
      --merge db/properties/msd_LPSCl_LPSCl16_b2o3.csv \\
      --out db/properties/msd_4sys_origin.csv
  # 2) 그림
  python3 tools/figures/fig_msd_4sys.py

⚠⚠ **이 그림의 곡선은 단일 시드다 — 계층(누가 빠른가)만 보여 준다.**
  D·Ea·sigma 정량은 멀티시드 산출물에서 가져온다. 곡선 기울기를 읽어 D 라고 인용 금지.
  (기존 CSV 머리말도 같은 규율을 적어 두었다.)

⚠ 색 배정: house_style.SYS 는 lpsocl=#be123c(진홍)인데, **이 그림 family 에서는
  b2o3 가 이미 빨강**이라 충돌한다. 이미 논문에 나간 3계 색을 그대로 두는 것이
  우선이므로 LPSOCl 만 보라(#7c3aed)로 뺀다. 다른 계열 그림에서는 SYS 를 따른다.
"""
import csv
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from tools.figures.house_style import INK, MUT, apply_axes  # noqa: E402

SRC = REPO / "db/properties/msd_4sys_origin.csv"
FALLBACK = REPO / "db/properties/msd_LPSCl_LPSCl16_b2o3.csv"
OUTPNG = REPO / "docs/figures/msd_4sys.png"
OUTCSV = REPO / "db/properties/msd_4sys_plotted.csv"

# (CSV 열 접두어, 범례, 색, 마커)
SERIES = [
    ("LPSCl",     r"LPSCl (Li$_6$PS$_5$Cl)", "#6b7280", "o"),
    ("LPSCl1.6",  "LPSCl1.6 (Cl-rich)",      "#2563eb", "s"),
    ("lpsocl",    "LPSOCl (O-substituted)",  "#7c3aed", "D"),
    ("b2o3",      r"B$_2$O$_3$-doped",       "#c0392b", "^"),
]
TEMPS = (600, 800, 1000)
FIT = (2.0, 50.0)          # 캠페인 규약 창. 여기서만 기울기를 읽는다.


def load(path):
    L = [l for l in path.read_text(encoding="utf-8-sig").splitlines()
         if l.strip() and not l.lstrip().startswith(('#', '"#'))]
    r = list(csv.reader(L))
    head, body = r[0], r[1:]
    t = np.array([float(x[0]) for x in body])
    cols = {}
    for j, name in enumerate(head[1:], 1):
        v = np.array([np.nan if not x[j].strip() else float(x[j]) for x in body])
        cols[name] = v
    return t, cols


def main():
    src = SRC if SRC.exists() else FALLBACK
    if src is FALLBACK:
        print(f"⚠ {SRC.name} 이 없다 — 기존 3계 CSV 로 그린다(LPSOCl 빠짐).")
        print("   LPSOCl 을 넣으려면 harvest_msd_curves.py 를 서버에서 먼저 돌릴 것.")
    t, cols = load(src)

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.6))
    used = []
    for ax, T in zip(axes, TEMPS):
        for pref, lab, c, mk in SERIES:
            key = f"{pref}_{T}K"
            if key not in cols:
                continue
            y = cols[key]
            m = np.isfinite(y)
            if m.sum() < 5:
                continue
            ax.plot(t[m], y[m], color=c, lw=1.5, alpha=.9, zorder=3)
            # ⚠ 마커를 전 점에 찍으면 곡선이 안 보인다. 3점마다.
            ax.plot(t[m][::3], y[m][::3], marker=mk, ms=4.5, ls="none",
                    color=c, label=lab if T == TEMPS[0] else None, zorder=4)
            w = m & (t >= FIT[0]) & (t <= FIT[1])
            if w.sum() >= 3:
                a, b = np.polyfit(t[w], y[w], 1)
                ax.plot(t, a * t + b, color=c, ls="--", lw=1.1, alpha=.55, zorder=2)
                if T == TEMPS[0]:
                    used.append((lab, a / 6.0))
        apply_axes(ax, xlabel="time (ps)",
                   ylabel=r"Li MSD  ($\mathrm{\AA}^2$)" if T == TEMPS[0] else None)
        ax.set_title(f"{T} K", fontsize=13, fontweight="bold", color=INK)
        ax.set_xlim(0, t.max())
        ax.set_ylim(bottom=0)
        ax.grid(alpha=.25, lw=.6)
    axes[0].legend(frameon=True, fontsize=9.5, loc="upper left")

    fig.suptitle("Li mean-squared displacement  —  four sulfide compositions  (MLIP-MD)",
                 fontsize=14, fontweight="bold", color=INK, y=1.02)
    # ⚠ 규율을 그림 안에 적는다. 그림만 떼어 가는 사람이 D 를 읽지 않도록.
    fig.text(0.5, -0.06,
             "Single-seed trajectories — illustrative hierarchy only. "
             "Quantitative D / $E_a$ / $\\sigma$ come from the multiseed Arrhenius sets.",
             ha="center", fontsize=9, color=MUT)
    OUTPNG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPNG, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"→ {OUTPNG}")
    for lab, D in used:
        print(f"   {lab:28s} 600 K 기울기/6 = {D * 1e-16 / 1e-12:.3e} cm²/s (표시용)")

    # Origin-ready CSV (하우스 규약: 데이터 그림은 CSV 동시 출력)
    with open(OUTCSV, "w", newline="", encoding="utf-8-sig") as f:
        f.write('"# Plotted Li MSD curves for docs/figures/msd_4sys.png."\n')
        f.write('"# Single-seed, illustrative hierarchy ONLY — do not read D from these slopes."\n')
        f.write(f'"# Dashed guides = linear fit over {FIT[0]}-{FIT[1]} ps (campaign window)."\n')
        w = csv.writer(f)
        keys = [f"{p}_{T}K" for p, _, _, _ in SERIES for T in TEMPS if f"{p}_{T}K" in cols]
        w.writerow(["t_ps"] + keys)
        for i, tt in enumerate(t):
            w.writerow([f"{tt:.1f}"] + ["" if not np.isfinite(cols[k][i]) else f"{cols[k][i]:.3f}"
                                        for k in keys])
    print(f"→ {OUTCSV}")


if __name__ == "__main__":
    main()
