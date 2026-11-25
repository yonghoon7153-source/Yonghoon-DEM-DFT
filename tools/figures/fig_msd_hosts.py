#!/usr/bin/env python3
"""fig_msd_hosts.py — Li MSD(t): LPSCl1.6 호스트와 그 변형 두 가지 (+O, +B2O3).

1저자 요청 §3 (LPSOCl 추가) 반영판. 600/800/1000 K 3패널, 점선 = 2-50 ps 적합.

⚠⚠ **화학량론 LPSCl(comp1)은 기본에서 뺐다 (2026-08-03 판단).** 두 가지 이유:
  ① 그 200 ps 런은 **확산영역 게이트를 전부 탈락**했다(beta 0.17-0.79). 200 ps 를 다
     그리면 600 K 에서 49 ps 13.9 A^2 -> 199 ps 16.07 A^2 로 **150 ps 동안 2.2 A^2 밖에
     안 늘었다**(2-50 ps 기울기가 유지됐다면 56 A^2 여야 한다). 완전히 갇힌 곡선이라
     같은 축에 올리면 "느린 확산"으로 오독된다 — 확산이 아니라 **측정 실패**다.
  ② 남는 셋이 오히려 일관된다: **LPSCl1.6 이 호스트**고 LPSOCl·B2O3 는 그 변형이다.
     화학량론 LPSCl 은 다른 호스트라 같은 그림에 섞을 이유도 약하다.
  → 넣어야 하면 --with-lpscl. 그때는 캡션에 게이트 탈락을 반드시 명시할 것.

  # 1) 먼저 곡선을 수확한다 (런 디렉토리가 있는 서버에서)
  python3 tools/figures/harvest_msd_curves.py --run lpsocl=~/work/runs/lpsocl_md/ladder \\
      --merge db/properties/msd_LPSCl_LPSCl16_b2o3.csv \\
      --out db/properties/msd_hosts_origin.csv
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

SRC = REPO / "db/properties/msd_hosts_origin.csv"
FALLBACK = REPO / "db/properties/msd_LPSCl_LPSCl16_b2o3.csv"
OUTPNG = REPO / "docs/figures/msd_hosts.png"
OUTCSV = REPO / "db/properties/msd_hosts_plotted.csv"

# (CSV 열 접두어, 범례, 색, 마커)
SERIES_MAIN = [
    ("LPSCl1.6",  "LPSCl1.6 (host)",         "#2563eb", "s"),
    ("lpsocl",    "LPSOCl1.6",               "#7c3aed", "D"),
    ("b2o3",      r"B$_2$O$_3$-doped",       "#c0392b", "^"),
]
# ⚠ 게이트 탈락 계열. 기본에서 뺀다(위 docstring). --with-lpscl 로만 들어온다.
SERIES_OPT = [("LPSCl", r"LPSCl (Li$_6$PS$_5$Cl) — gate-failed", "#9ca3af", "o")]
TEMPS = (600, 800, 1000)
FIT = (2.0, 50.0)          # 캠페인 규약 창. **여기서만** 기울기를 읽는다.
# ⚠ 궤적은 200 ps 인데 창은 2-50 ps 다. 창 밖까지 그리는 게 중요하다 —
#   확산영역 게이트가 생긴 뒤로는 "창 밖에서도 직선인가"가 판정의 일부이고,
#   창만 보여 주면 독자가 그걸 확인할 수 없다. 창은 음영으로 표시한다.


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
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--with-lpscl", action="store_true",
                    help="화학량론 LPSCl 도 그린다. ⚠ 그 런은 확산영역 게이트 탈락 — "
                         "캡션에 반드시 명시할 것")
    ap.add_argument("--src", default=None, help="MSD CSV 경로 (기본 db/properties/msd_hosts_origin.csv)")
    A = ap.parse_args()
    global SERIES
    SERIES = (SERIES_OPT + SERIES_MAIN) if A.with_lpscl else SERIES_MAIN
    src = Path(A.src) if A.src else (SRC if SRC.exists() else FALLBACK)
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
        # 적합 창을 음영으로 — 어디서 D 를 읽었는지가 그림에 남아야 한다
        ax.axvspan(FIT[0], min(FIT[1], t.max()), color="#94a3b8", alpha=.10, zorder=0)
        if T == TEMPS[0]:
            ax.text(FIT[1], ax.get_ylim()[1] * .02, f"  fit {FIT[0]:g}-{FIT[1]:g} ps",
                    fontsize=8, color=MUT, va="bottom")
        apply_axes(ax, xlabel="time (ps)",
                   ylabel=r"Li MSD  ($\mathrm{\AA}^2$)" if T == TEMPS[0] else None)
        ax.set_title(f"{T} K", fontsize=13, fontweight="bold", color=INK)
        ax.set_xlim(0, t.max())
        ax.set_ylim(bottom=0)
        ax.grid(alpha=.25, lw=.6)
    axes[0].legend(frameon=True, fontsize=9.5, loc="upper left")

    ttl = ("Li mean-squared displacement  —  LPSCl1.6 host and its modifications  (MLIP-MD)"
           if not A.with_lpscl else
           "Li mean-squared displacement  —  sulfide compositions  (MLIP-MD)")
    fig.suptitle(ttl, fontsize=14, fontweight="bold", color=INK, y=1.02)
    # ⚠ 규율을 그림 안에 적는다. 그림만 떼어 가는 사람이 D 를 읽지 않도록.
    cap = ("Single-seed trajectories — illustrative hierarchy only. "
           "Quantitative D / $E_a$ / $\\sigma$ come from the multiseed Arrhenius sets.")
    if A.with_lpscl:
        # ⚠ 게이트 탈락 계열을 그렸으면 그 사실이 그림에 남아야 한다.
        cap += ("\nLPSCl (grey) fails the diffusive-regime gate over this window "
                "($\\beta$ = 0.17–0.79); its slope is NOT a diffusion coefficient.")
    fig.text(0.5, -0.06, cap, ha="center", fontsize=9, color=MUT)
    OUTPNG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPNG, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"→ {OUTPNG}")
    for lab, D in used:
        print(f"   {lab:28s} 600 K 기울기/6 = {D * 1e-16 / 1e-12:.3e} cm²/s (표시용)")

    # Origin-ready CSV (하우스 규약: 데이터 그림은 CSV 동시 출력)
    with open(OUTCSV, "w", newline="", encoding="utf-8-sig") as f:
        f.write('"# Plotted Li MSD curves for docs/figures/msd_hosts.png."\n')
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
