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


def panel_a(ax, rows):
    # ── (a) 보호 곡선 ─────────────────────────────────────────────────
    xs = np.linspace(0.0, 0.22, 300)
    for cat, V, k, phase, col, mk in CLEAN:
        ax.plot(xs, np.minimum(1.0, k * xs / (1 - xs)) * 100, "--", color=col, lw=1.3, alpha=.75, zorder=1)
        pts = sorted((r for r in rows if r["cathode"] == cat and r["voltage_V"] == V and r["gate_pass"]),
                     key=lambda r: r["x_Nd"])
        ax.plot([r["x_Nd"] for r in pts], [r["protection_observed"] * 100 for r in pts],
               mk, color=col, ms=7, mec="white", mew=1.1, zorder=3,
               label=f"{cat}  {V:.1f} V   $k$ = {k:.0f}  ({phase})")
    ax.axhline(100, color=MUT, lw=.8, ls=":", zorder=0)
    ax.axvline(0.02, color=MUT, lw=.8, ls=":", zorder=0)
    ax.annotate("target\ncomposition", xy=(0.02, 10.3), xytext=(0.003, 34),
               fontsize=9, color=MUT,
               arrowprops=dict(arrowstyle="->", color=MUT, lw=.9,
                               connectionstyle="arc3,rad=-0.25"))
    ax.text(.004, 62, r"$\min\left(1,\ k\,\dfrac{x_{\mathrm{Nd}}}{1-x_{\mathrm{Nd}}}\right)$"
                     "\n(dashed)", fontsize=10.5, color=INK, va="center")
    ax.set_xlim(0, .22); ax.set_ylim(-4, 112)
    apply_axes(ax, "Nd content $x$ in Li$_{5.4+2x}$Nd$_x$P$_{1-x}$S$_{4.37}$O$_{0.03}$Cl$_{1.6}$",
               "Cathode TM spared from phosphate (%)",
               "(a)  One Nd sequesters $k$ phosphorus")
    ax.legend(frameon=False, fontsize=9, loc="lower right", labelcolor=INK)


def panel_b(ax, rows):
    # ── (b) P 가 어디로 가나 (LiCoO2) ────────────────────────────────
    for j, V in enumerate((4.3, 4.5)):
        pts = sorted((r for r in rows if r["cathode"] == "LiCoO2" and r["voltage_V"] == V),
                     key=lambda r: r["x_Nd"])
        xv = np.arange(len(pts)) + j * (len(pts) + 1.1)
        nd = np.array([r["P_taken_by_Nd"] for r in pts]) * 100
        th = np.array([r["P_to_thiophosphate"] for r in pts]) * 100
        ax.bar(xv, nd, .74, color=ND_DARK, label="Nd phosphate" if j == 0 else None)
        ax.bar(xv, 100 - nd - th, .74, bottom=nd, color=TMP,
              label="cathode TM phosphate" if j == 0 else None)
        ax.bar(xv, th, .74, bottom=100 - th, color=THIO,
              label="thiophosphate (P$_2$S$_7$)" if j == 0 else None)
        ax.text(xv.mean(), 108, f"{V:.1f} V", ha="center", fontsize=10, color=INK)
        if V == 4.5:
            ax.text(xv[-1] + .62, 56, "$x$ = 0.20\nnot shown:\nelectrolyte\nself-decomposes,\nno interface",
                   fontsize=8.2, color=MUT, ha="left", va="center", linespacing=1.35)
        for xx, r in zip(xv, pts):
            ax.text(xx, -7, f"{r['x_Nd']:.2f}", ha="center", fontsize=7.4, color=MUT)
    ax.set_xticks([]); ax.set_ylim(0, 116); ax.set_xlim(-.75, 12.6)
    ax.text(.5, -.19, "Nd content $x$", transform=ax.transAxes, ha="center", fontsize=12, color=INK)
    apply_axes(ax, None, "Share of the electrolyte's P (%)",
               "(b)  Where the phosphorus goes")
    ax.legend(frameon=False, fontsize=9, loc="lower left", labelcolor=INK,
             bbox_to_anchor=(0.0, 0.02))


def panel_c(ax, rows):
    # ── (c) 게이트 — **열 단위**로 그린다. 점만 뿌리면 "어느 열이 살았나" 를 못 읽는다.
    ax.axhspan(0, DX_MAX, color="#dcfce7", zorder=0)
    ax.axhline(DX_MAX, color="#16a34a", lw=1.0, zorder=1)
    ax.text(.208, DX_MAX * .42, f"$\\Delta x \\leq$ {DX_MAX:.2f}\ncomparable",
           fontsize=9, color="#166534", ha="right")
    cols = sorted({(r["cathode"], r["voltage_V"]) for r in rows})
    survivors = {(x[0], x[1]) for x in CLEAN}
    for cat, V in cols:
        pts = sorted((r for r in rows if r["cathode"] == cat and r["voltage_V"] == V),
                     key=lambda r: r["x_Nd"])
        live = (cat, V) in survivors
        col = ND_DARK if cat == "LiCoO2" else ND_LIGHT
        ax.plot([r["x_Nd"] for r in pts], [r["delta_x"] for r in pts],
               "-" if live else ":", color=col if live else MUT,
               lw=2.0 if live else 1.0, alpha=1 if live else .55,
               marker="o" if cat == "LiCoO2" else "s",
               ms=6 if live else 4, mec="white" if live else MUT,
               mew=1.1 if live else .6, zorder=4 if live else 2)
        xl, yl = pts[-1]["x_Nd"], pts[-1]["delta_x"]
        ax.annotate(f"{cat[2:]}  {V:.1f} V", xy=(xl, yl), xytext=(4, 0),
                   textcoords="offset points", va="center", fontsize=8.5,
                   color=col if live else MUT, weight="bold" if live else "normal")
    ax.set_xlim(0, .255); ax.set_ylim(0, .20)
    apply_axes(ax, "Nd content $x$", "$|\\Delta x_{\\mathrm{mix}}|$ vs undoped control",
               "(c)  Why only two columns survive")
    ax.text(.004, .193,
           "bold = every point comparable\n"
           "dotted = the minimum kink moves to a\ndifferent mixing ratio, so the\ndenominators are not the same quantity",
           fontsize=8.5, color=MUT, va="top")


PANELS = {"a": (panel_a, "One Nd sequesters k P"),
          "b": (panel_b, "Where the phosphorus goes"),
          "c": (panel_c, "Why only two columns survive")}
#: 패널 하나당 폭. 3패널 13.2 인치를 그대로 나눈 값이라 `--panels abc` 가 원본과 같다.
PANEL_W, FIG_H = 4.4, 4.3


def build(which="abc", out=None, rows=None):
    """선택한 패널만 그린다 → 저장 경로.

    왜 (2026-09-21): 주간보고 슬라이드에는 (c)(게이트 진단)가 군더더기다.
    ⛔ 그런데 **(c) 를 지우는 것이 아니다** — 24 칸 중 12 칸이 탈락했고 (c) 가 그 이유다.
      기본은 abc 그대로이고, 발표용으로 줄일 때만 플래그를 준다. 줄인 판을 쓰면
      **캡션에 탈락 수를 적어야 한다** (그래서 도구가 화면에 경고를 찍는다).
    """
    which = "".join(dict.fromkeys(which))          # 중복 제거, 순서 유지
    bad = [ch for ch in which if ch not in PANELS]
    if bad:
        raise SystemExit(f"⛔ 그런 패널이 없다: {bad} (가능: {sorted(PANELS)})")
    if not which:
        raise SystemExit("⛔ 패널을 하나도 안 골랐다")
    rows = load() if rows is None else rows
    fig, axes = plt.subplots(1, len(which), figsize=(PANEL_W * len(which), FIG_H))
    axes = [axes] if len(which) == 1 else list(axes)
    for ch, ax in zip(which, axes):
        PANELS[ch][0](ax, rows)
        ax.tick_params(labelsize=10)
    fig.tight_layout()
    png = pathlib.Path(out) if out else (
        OUT / ("cei_nd_protection.png" if which == "abc"
               else f"cei_nd_protection_{which}.png"))
    fig.savefig(png, dpi=300, bbox_inches="tight")
    plt.close(fig)
    if "c" not in which:
        print("  ⚠ (c) 를 뺐다 — 캡션에 **'24 칸 중 12 칸은 혼합비·P2S7 로 탈락'** 을 반드시 적는다")
    return png


def write_pred_csv(xs=None):
    """예측선 Origin CSV (실측점은 cei_nd_protection_curve.csv 에 이미 있다)."""
    xs = np.linspace(0.0, 0.22, 300) if xs is None else xs
    pc = OUT / "cei_nd_protection_fig.csv"
    with pc.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["x_Nd", "predicted_protection_percent_k5_NdP5O14",
                    "predicted_protection_percent_k4_LiNdPO34"])
        for x in xs:
            w.writerow([f"{x:.5f}", f"{min(1, 5 * x / (1 - x)) * 100:.4f}",
                        f"{min(1, 4 * x / (1 - x)) * 100:.4f}"])
    return pc


def _selftest():
    import tempfile, shutil
    ok = True

    def chk(c, m):
        nonlocal ok
        ok = ok and bool(c)
        print(f"  {'✓' if c else '✗'} {m}")

    rows = load()
    chk(len(rows) == 34, f"[양성] 원자료 34 행 (얻은 {len(rows)})")
    nfail = sum(1 for r in rows if not r["gate_pass"])
    chk(sum(1 for r in rows if r["gate_pass"]) == 22,
        f"[양성] gate_pass 22 행 · 탈락 {nfail} 행도 CSV 에 남아 있다")
    td = pathlib.Path(tempfile.mkdtemp(prefix="cnp_"))
    for w in ("abc", "ab", "a"):
        f = build(w, out=td / f"{w}.png", rows=rows)
        chk(f.exists() and f.stat().st_size > 20000, f"[양성] --panels {w} 가 그려진다")

    def dies(w):
        try:
            build(w, out=td / "x.png", rows=rows)
        except SystemExit:
            return True
        except Exception:
            return False
        return False

    chk(dies("abz"), "[음성] 없는 패널 이름을 거부한다")
    chk(dies(""), "[음성] 패널을 하나도 안 고르면 거부한다")
    #: ⛔ 기본값이 바뀌면 기존 그림이 조용히 달라진다 — 그걸 막는 시험이다.
    chk(build.__defaults__[0] == "abc", "[배선] 기본값은 여전히 abc (기존 그림 불변)")
    shutil.rmtree(td, ignore_errors=True)
    print("selftest " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--panels", default="abc",
                    help="그릴 패널 (기본 abc). 슬라이드용은 ab — ⛔ 줄이면 캡션에 탈락 수를 적는다")
    ap.add_argument("--out", default=None, help="저장 경로 (기본: cei_figs/ 아래 자동)")
    a = ap.parse_args(argv)
    png = build(a.panels, out=a.out)
    print(f"✓ {png}")
    if a.panels == "abc" and a.out is None:
        pc = write_pred_csv()
        print(f"✓ {pc.relative_to(REPO)}  (예측선; 실측점은 cei_nd_protection_curve.csv)")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    main()
