#!/usr/bin/env python3
"""Fig. 2 — Nd 가 고전압에서 P 를 가로채 양극 TM 의 인산염 소모를 막는다.

자료: db/properties/cei_figs/cei_nd_protection_curve.csv (34 행, gate_pass 열)
기록: db/properties/cei_nd_p_capture_result_2026_09_18.json

⛔ 이 그림이 **하지 않는 것**
  · 게이트 탈락 칸을 (a) 에 그리지 않는다 — 대신 (c) 가 왜 탈락했는지를 그린다.
    (조용히 버리면 "왜 세 점뿐이지" 가 된다.)
  · 속도·두께·연속성을 말하지 않는다. 0 K hull 열역학이다.
  · 절대 반응에너지를 쓰지 않는다 (Li 장부 교란 — 감사 기록 참조).

색 규약: Nd 는 하우스 팔레트에 #db2777 이지만 이 family(Fig. 1)가 O(crimson)와
  안 갈려 보라 #6d28d9 로 고정했다. 그것을 승계하고, **두 양극은 명도 램프**로
  가른다 (Fig. 5 가 전압을 그렇게 처리한 관례). 양극은 원소가 아니라 조건이므로
  원소 팔레트를 쓰지 않는다.
"""
import csv, pathlib, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from house_style import INK, MUT, apply_axes  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parents[2]
SRC = REPO / "db/properties/cei_figs/cei_nd_protection_curve.csv"
OUT = REPO / "db/properties/cei_figs"

ND_DARK, ND_LIGHT = "#6d28d9", "#a78bfa"       # 명도 램프 (양극 = 조건)
THIO = "#c05621"                               # S 계열 = sienna (하우스 ELEM["S"])
TMP = "#6b7280"
DX_MAX = 0.05

# 게이트를 전부 통과한 열 둘 — 기록 §3 와 같은 값이어야 한다
CLEAN = [("LiCoO2", 4.3, 5.0, "NdP$_5$O$_{14}$", ND_DARK, "o"),
         ("LiNiO2", 3.5, 4.0, "LiNd(PO$_3$)$_4$", ND_LIGHT, "s")]


def load():
    rows = []
    with SRC.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows.append({**r,
                         "voltage_V": float(r["voltage_V"]), "x_Nd": float(r["x_Nd"]),
                         "delta_x": float(r["delta_x"]), "gate_pass": r["gate_pass"] == "True",
                         "protection_observed": float(r["protection_observed"]),
                         "P_taken_by_Nd": float(r["P_taken_by_Nd"]),
                         "P_to_thiophosphate": float(r["P_to_thiophosphate"])})
    return rows


def main():
    rows = load()
    fig, (a, b, c) = plt.subplots(1, 3, figsize=(13.2, 4.3))

    # ── (a) 보호 곡선 ─────────────────────────────────────────────────
    xs = np.linspace(0.0, 0.22, 300)
    for cat, V, k, phase, col, mk in CLEAN:
        a.plot(xs, np.minimum(1.0, k * xs / (1 - xs)) * 100, "--", color=col, lw=1.3, alpha=.75, zorder=1)
        pts = sorted((r for r in rows if r["cathode"] == cat and r["voltage_V"] == V and r["gate_pass"]),
                     key=lambda r: r["x_Nd"])
        a.plot([r["x_Nd"] for r in pts], [r["protection_observed"] * 100 for r in pts],
               mk, color=col, ms=7, mec="white", mew=1.1, zorder=3,
               label=f"{cat}  {V:.1f} V   $k$ = {k:.0f}  ({phase})")
    a.axhline(100, color=MUT, lw=.8, ls=":", zorder=0)
    a.axvline(0.02, color=MUT, lw=.8, ls=":", zorder=0)
    a.annotate("target\ncomposition", xy=(0.02, 10.3), xytext=(0.003, 34),
               fontsize=9, color=MUT,
               arrowprops=dict(arrowstyle="->", color=MUT, lw=.9,
                               connectionstyle="arc3,rad=-0.25"))
    a.text(.004, 62, r"$\min\left(1,\ k\,\dfrac{x_{\mathrm{Nd}}}{1-x_{\mathrm{Nd}}}\right)$"
                     "\n(dashed)", fontsize=10.5, color=INK, va="center")
    a.set_xlim(0, .22); a.set_ylim(-4, 112)
    apply_axes(a, "Nd content $x$ in Li$_{5.4+2x}$Nd$_x$P$_{1-x}$S$_{4.37}$O$_{0.03}$Cl$_{1.6}$",
               "Cathode TM spared from phosphate (%)",
               "(a)  One Nd sequesters $k$ phosphorus")
    a.legend(frameon=False, fontsize=9, loc="lower right", labelcolor=INK)

    # ── (b) P 가 어디로 가나 (LiCoO2) ────────────────────────────────
    for j, V in enumerate((4.3, 4.5)):
        pts = sorted((r for r in rows if r["cathode"] == "LiCoO2" and r["voltage_V"] == V),
                     key=lambda r: r["x_Nd"])
        xv = np.arange(len(pts)) + j * (len(pts) + 1.1)
        nd = np.array([r["P_taken_by_Nd"] for r in pts]) * 100
        th = np.array([r["P_to_thiophosphate"] for r in pts]) * 100
        b.bar(xv, nd, .74, color=ND_DARK, label="Nd phosphate" if j == 0 else None)
        b.bar(xv, 100 - nd - th, .74, bottom=nd, color=TMP,
              label="cathode TM phosphate" if j == 0 else None)
        b.bar(xv, th, .74, bottom=100 - th, color=THIO,
              label="thiophosphate (P$_2$S$_7$)" if j == 0 else None)
        b.text(xv.mean(), 108, f"{V:.1f} V", ha="center", fontsize=10, color=INK)
        if V == 4.5:
            b.text(xv[-1] + .62, 56, "$x$ = 0.20\nnot shown:\nelectrolyte\nself-decomposes,\nno interface",
                   fontsize=8.2, color=MUT, ha="left", va="center", linespacing=1.35)
        for xx, r in zip(xv, pts):
            b.text(xx, -7, f"{r['x_Nd']:.2f}", ha="center", fontsize=7.4, color=MUT)
    b.set_xticks([]); b.set_ylim(0, 116); b.set_xlim(-.75, 12.6)
    b.text(.5, -.19, "Nd content $x$", transform=b.transAxes, ha="center", fontsize=12, color=INK)
    apply_axes(b, None, "Share of the electrolyte's P (%)",
               "(b)  Where the phosphorus goes")
    b.legend(frameon=False, fontsize=9, loc="lower left", labelcolor=INK,
             bbox_to_anchor=(0.0, 0.02))

    # ── (c) 게이트 — **열 단위**로 그린다. 점만 뿌리면 "어느 열이 살았나" 를 못 읽는다.
    c.axhspan(0, DX_MAX, color="#dcfce7", zorder=0)
    c.axhline(DX_MAX, color="#16a34a", lw=1.0, zorder=1)
    c.text(.208, DX_MAX * .42, f"$\\Delta x \\leq$ {DX_MAX:.2f}\ncomparable",
           fontsize=9, color="#166534", ha="right")
    cols = sorted({(r["cathode"], r["voltage_V"]) for r in rows})
    survivors = {(x[0], x[1]) for x in CLEAN}
    for cat, V in cols:
        pts = sorted((r for r in rows if r["cathode"] == cat and r["voltage_V"] == V),
                     key=lambda r: r["x_Nd"])
        live = (cat, V) in survivors
        col = ND_DARK if cat == "LiCoO2" else ND_LIGHT
        c.plot([r["x_Nd"] for r in pts], [r["delta_x"] for r in pts],
               "-" if live else ":", color=col if live else MUT,
               lw=2.0 if live else 1.0, alpha=1 if live else .55,
               marker="o" if cat == "LiCoO2" else "s",
               ms=6 if live else 4, mec="white" if live else MUT,
               mew=1.1 if live else .6, zorder=4 if live else 2)
        xl, yl = pts[-1]["x_Nd"], pts[-1]["delta_x"]
        c.annotate(f"{cat[2:]}  {V:.1f} V", xy=(xl, yl), xytext=(4, 0),
                   textcoords="offset points", va="center", fontsize=8.5,
                   color=col if live else MUT, weight="bold" if live else "normal")
    c.set_xlim(0, .255); c.set_ylim(0, .20)
    apply_axes(c, "Nd content $x$", "$|\\Delta x_{\\mathrm{mix}}|$ vs undoped control",
               "(c)  Why only two columns survive")
    c.text(.004, .193,
           "bold = every point comparable\n"
           "dotted = the minimum kink moves to a\ndifferent mixing ratio, so the\ndenominators are not the same quantity",
           fontsize=8.5, color=MUT, va="top")

    for ax in (a, b, c):
        ax.tick_params(labelsize=10)
    fig.tight_layout()
    png = OUT / "cei_nd_protection.png"
    fig.savefig(png, dpi=300, bbox_inches="tight")

    # Origin-ready CSV — 예측선 (원자료 CSV 는 이미 있다)
    pc = OUT / "cei_nd_protection_fig.csv"
    with pc.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["x_Nd", "predicted_protection_percent_k5_NdP5O14",
                    "predicted_protection_percent_k4_LiNdPO34"])
        for x in xs:
            w.writerow([f"{x:.5f}", f"{min(1, 5 * x / (1 - x)) * 100:.4f}",
                        f"{min(1, 4 * x / (1 - x)) * 100:.4f}"])
    print(f"✓ {png.relative_to(REPO)}")
    print(f"✓ {pc.relative_to(REPO)}  (예측선; 실측점은 cei_nd_protection_curve.csv)")


if __name__ == "__main__":
    main()
