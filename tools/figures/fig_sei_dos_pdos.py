#!/usr/bin/env python3
"""fig_sei_dos_pdos.py — SEI 분해상 6종의 DOS/PDOS 패널 + 갭 사다리.

무엇을 보여 주나
  SEI 의 임무는 **Li⁺ 통과 · 전자 차단**이다. 그래서 축은 "전자 절연이 되나" 하나다.
  6종 중 **Li₃P 만 0.709 eV** 로 한 자릿수 좁다 — 전자가 새면 전해질 분해가
  자기종결(self-limiting)되지 않는다. 그 대비가 그림의 전부다.

⚠⚠ 데이터 규율
  · 갭은 **fixed-occ nscf 고유값**(db/properties/sei_electronic.json)이다.
    그림의 노란 띠는 그 값으로 그린다 — **DOS 곡선에서 문턱을 읽어 그리지 않는다.**
  · PBE 갭은 넓은 갭 절연체에서 30–50% 과소다. 그림 안에 그 문구를 박아 둔다.
  · Nd 계 3종은 4f 를 원자가에 넣은 PBE 라 갭이 닫힌다 — **이 그림에서 제외**한다.
    (진단이 필요하면 --with-nd 로 별도 파일에 그린다. 인용 금지 표식이 붙는다.)
  · tools/figures/plot_nd_sei_gaps.py 의 숫자는 **MP 소환값**이다(LiCl 6.65 / Li₂S 3.90 …).
    이 그림은 **우리 QE 값**이다. 두 세트를 한 그림·한 표에 섞지 말 것.

  python3 tools/figures/fig_sei_dos_pdos.py
  python3 tools/figures/fig_sei_dos_pdos.py --with-nd     # 진단용 Nd 3종 추가 파일
"""
import argparse
import csv
import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from tools.figures.house_style import INK, MUT, ELEM, GAPBAND, GAPLINE, GAPTEXT, apply_axes

EL = json.load(open("db/properties/sei_electronic.json"))["results"]
DOSDIR = "db/properties/sei_dos"
FIGDIR = "docs/figures/sei"
CSVDIR = "db/properties"

# 표시명 · 패널 순서 = **갭 내림차순**(절연 잘 되는 것부터 → Li₃P 가 맨 끝에 홀로 남는다)
DISP = {
    "licl_mp-22905":    "LiCl",
    "li3po4_mp-13725":  r"Li$_3$PO$_4$ ($\beta$)",
    "li3po4g_mp-2878":  r"Li$_3$PO$_4$ ($\gamma$)",
    "li2o_mp-1960":     r"Li$_2$O",
    "li2s_mp-1153":     r"Li$_2$S",
    "li3p_mp-736":      r"Li$_3$P",
    "lindo2_mp-1222355": r"LiNdO$_2$",
    "nd2o3_mp-2763":    r"Nd$_2$O$_3$",
    "nd2s3_mp-438":     r"Nd$_2$S$_3$",
}
CITABLE = ["licl_mp-22905", "li3po4_mp-13725", "li3po4g_mp-2878",
           "li2o_mp-1960", "li2s_mp-1153", "li3p_mp-736"]
ND = ["lindo2_mp-1222355", "nd2o3_mp-2763", "nd2s3_mp-438"]
ELEM_X = dict(ELEM, Nd="#a21caf")           # Nd 는 house 팔레트에 없다 — 진단용에만 쓴다
SIG_EV = 0.10                               # 가우시안 평활 폭 [eV]


def load(tag):
    """PDOS CSV 를 읽어 원소별로 합산한다(s+p+d+f). 궤도 분해는 이 그림의 요점이 아니다."""
    p = os.path.join(DOSDIR, f"{tag}_pdos.csv")
    with open(p, encoding="utf-8") as f:
        f.readline()                                    # '#' 출처 주석
        r = csv.reader(f); hdr = next(r)
        rows = np.array([[float(x) for x in v] for v in r if len(v) == len(hdr)])
    E = rows[:, hdr.index("E_minus_VBM_eV")]
    by_el = {}
    for i, h in enumerate(hdr):
        if "_" not in h or h.startswith("E_"):
            continue
        el = h.split("_")[0]
        by_el[el] = by_el.get(el, 0.0) + rows[:, i]
    # total 은 dos.x 산출을 쓴다 — projwfc 합은 투영 손실 때문에 항상 조금 모자란다
    pd_ = os.path.join(DOSDIR, f"{tag}_dos.csv")
    with open(pd_, encoding="utf-8") as f:
        f.readline(); r = csv.reader(f); h2 = next(r)
        d2 = np.array([[float(x) for x in v] for v in r if len(v) == len(h2)])
    Et = d2[:, h2.index("E_minus_VBM_eV")]
    tot = np.interp(E, Et, d2[:, h2.index("DOS_states_per_eV")])
    return E, tot, by_el


def smooth(E, y, sig=SIG_EV):
    dE = float(np.median(np.diff(E)))
    n = max(1.0, sig / max(dE, 1e-9))
    from scipy.ndimage import gaussian_filter1d
    return gaussian_filter1d(y, n)


def panel(ax, tag, xlim):
    g = EL[tag]
    E, tot, by_el = load(tag)
    m = (E >= xlim[0] - 1) & (E <= xlim[1] + 1)
    E, tot = E[m], smooth(E[m], tot[m])
    # ★ 갭 띠는 **고유값**으로 그린다 (DOS 문턱 아님)
    ax.axvspan(0.0, g["gap"], color=GAPBAND, zorder=0)
    for x in (0.0, g["gap"]):
        ax.axvline(x, color=GAPLINE, ls="--", lw=1.0, zorder=1)
    for el, y in sorted(by_el.items(), key=lambda kv: -np.max(kv[1])):
        ax.fill_between(E, 0, smooth(E, y[m]), color=ELEM_X.get(el, MUT),
                        alpha=0.45, lw=0, label=el, zorder=2)
    ax.plot(E, tot, color=INK, lw=1.3, zorder=5)
    ax.set_xlim(*xlim); ax.set_ylim(0, None)
    ax.text(0.015, 0.93, DISP.get(tag, tag), transform=ax.transAxes,
            fontsize=11.5, color=INK, va="top", fontweight="bold")
    lab = f"{g['gap']:.2f} eV" if g["gap"] > 0.05 else f"{g['gap']:.3f} eV (closed)"
    ax.text(g["gap"] / 2 if g["gap"] > 1.2 else g["gap"] + 0.35, 0.62,
            lab, transform=ax.get_xaxis_transform(),
            ha="center" if g["gap"] > 1.2 else "left",
            fontsize=9.5, color=GAPTEXT, fontweight="bold")
    # ⚠ 범례가 오른쪽 위에 있다 — 경고문을 같은 자리에 두면 글자가 겹쳐 둘 다 못 읽는다
    #   (2026-08-07 1차 렌더에서 LiCl 패널이 그랬다). 상 이름 바로 아래 왼쪽에 붙인다.
    if not g.get("dos_chain_complete", True):
        ax.text(0.015, 0.79, "⚠ curve from an earlier run (gap unaffected)",
                transform=ax.transAxes, va="top", fontsize=7.5, color="#b45309")
    apply_axes(ax)
    ax.legend(loc="upper right", fontsize=8, frameon=False, ncol=2,
              handlelength=1.1, labelspacing=0.25, columnspacing=0.9)
    return E, tot


def figure(tags, out, title, sub, xlim, csvname):
    n = len(tags)
    fig, axs = plt.subplots(n, 1, figsize=(7.6, 1.62 * n + 1.5), sharex=True)
    axs = np.atleast_1d(axs)
    curves = {}
    for ax, t in zip(axs, tags):
        curves[t] = panel(ax, t, xlim)
    axs[-1].set_xlabel(r"$E - E_{\mathrm{VBM}}$  (eV)", fontsize=12, color=INK)
    fig.text(0.012, 0.5, "DOS  (states / eV)", rotation=90, va="center",
             fontsize=12, color=INK)
    axs[0].set_title(title, fontsize=13, color=INK, pad=12)
    fig.text(0.5, 0.985, sub, ha="center", va="top", fontsize=8.6, color=MUT)
    fig.tight_layout(rect=[0.035, 0.0, 1, 0.972])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fig.savefig(out, dpi=300); plt.close(fig)
    print(f"  → {out}")

    # Origin-ready: 그림에 **실제로 그린** total 곡선(평활·창 적용)만 모아 낸다.
    # 원소분해 원자료는 db/properties/sei_dos/*.csv 에 이미 있다.
    grid = np.arange(xlim[0], xlim[1] + 1e-9, 0.01)
    cols = {t: np.interp(grid, curves[t][0], curves[t][1]) for t in tags}
    p = os.path.join(CSVDIR, csvname)
    with open(p, "w", encoding="utf-8") as f:
        f.write(f"# {title} — total DOS as plotted (Gaussian {SIG_EV} eV, "
                f"E referenced to each phase's own VBM). Gaps are fixed-occ nscf "
                f"eigenvalues, NOT read off these curves. QE/PBE — our calculation, "
                f"do not mix with Materials Project values.\n")
        f.write("E_minus_VBM_eV," + ",".join(
            f"{t.split('_mp')[0]}_DOS_states_per_eV" for t in tags) + "\n")
        for i, e in enumerate(grid):
            f.write(f"{e:.3f}," + ",".join(f"{cols[t][i]:.5g}" for t in tags) + "\n")
    print(f"  → {p}")


def ladder(out):
    """갭 사다리 — '절연 되나 / 새나' 한 장 요약."""
    tags = sorted(CITABLE, key=lambda t: EL[t]["gap"])
    g = [EL[t]["gap"] for t in tags]

    def col(x):
        return "#15803d" if x >= 4.0 else "#ca8a04" if x >= 2.0 else "#b91c1c"

    fig, ax = plt.subplots(figsize=(7.4, 3.5))
    y = np.arange(len(tags))
    ax.barh(y, g, color=[col(x) for x in g], edgecolor=INK, lw=0.6, height=0.62, zorder=3)
    for i, x in enumerate(g):
        ax.text(x + 0.12, i, f"{x:.2f}", va="center", fontsize=10, color=INK)
    ax.set_yticks(y); ax.set_yticklabels([DISP[t] for t in tags], fontsize=11, color=INK)
    ax.axvline(2.0, color=MUT, ls=":", lw=1.0, zorder=1)
    # ⚠ 이 주석을 맨 위 막대 위에 그냥 두면 제목과 겹친다 — ylim 을 열어 자리를 만든다.
    ax.set_ylim(-0.62, len(tags) - 0.25)
    ax.text(2.05, len(tags) - 0.42, "electron leak  ←|→  insulating",
            fontsize=8.6, color=MUT, va="center")
    ax.set_xlim(0, max(g) * 1.18)
    apply_axes(ax, xlabel="Band gap (eV)  —  fixed-occupation nscf eigenvalues, PBE")
    ax.set_title("SEI decomposition phases: electronic insulation",
                 fontsize=12.5, color=INK, pad=10)
    fig.text(0.5, 0.005, "PBE underestimates wide gaps by 30–50% — use the ORDER, "
                         "not the absolute values. Our QE calculation (not Materials Project).",
             ha="center", fontsize=7.8, color=MUT)
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fig.savefig(out, dpi=300); plt.close(fig)
    print(f"  → {out}")

    p = os.path.join(CSVDIR, "sei_gap_ladder_origin.csv")
    with open(p, "w", encoding="utf-8") as f:
        f.write("# SEI decomposition phase band gaps — fixed-occ nscf eigenvalues (QE/PBE, ours).\n"
                "# NOT Materials Project values; do not mix with tools/figures/plot_nd_sei_gaps.py.\n")
        f.write("phase,material_id,VBM_eV,CBM_eV,gap_eV,verdict\n")
        for t in tags:
            d = EL[t]
            f.write(f"{t.split('_mp')[0]},{t.split('_')[-1]},"
                    f"{d['vbm']:.3f},{d['cbm']:.3f},{d['gap']:.3f},{d['verdict']}\n")
    print(f"  → {p}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--with-nd", action="store_true",
                    help="Nd 계 3종을 별도 파일로 (진단용 — 인용 금지 표식이 붙는다)")
    a = ap.parse_args()

    missing = [t for t in CITABLE if not os.path.isfile(os.path.join(DOSDIR, f"{t}_pdos.csv"))]
    if missing:
        sys.exit(f"⛔ PDOS CSV 없음: {missing} — tools/sei/collect_results.py 먼저")

    figure(CITABLE, os.path.join(FIGDIR, "sei_dos_pdos.png"),
           "SEI decomposition phases — DOS / PDOS",
           "Gap band (yellow) = fixed-occupation nscf eigenvalues, not a DOS threshold. "
           "QE/PBE; wide gaps underestimated 30–50%.",
           (-8.0, 10.0), "sei_dos_panels_origin.csv")
    ladder(os.path.join(FIGDIR, "sei_gap_ladder.png"))

    if a.with_nd:
        figure(ND, os.path.join(FIGDIR, "sei_dos_pdos_Nd_DIAGNOSTIC.png"),
               "Nd phases — DIAGNOSTIC ONLY, DO NOT CITE",
               "Nd 4f is in the valence: PBE puts the 4f band at E_F and closes the gap. "
               "This is a method failure, not metallicity. Cite MP frozen-4f gaps instead.",
               (-8.0, 10.0), "sei_dos_panels_Nd_DIAGNOSTIC_origin.csv")
    print("\n⚠ 갭은 fixed-occ nscf 고유값이 정본이다 — 이 곡선에서 문턱을 읽지 말 것.")
    print("⚠ 이 숫자는 **우리 QE 값**이다. plot_nd_sei_gaps.py 의 MP 소환값과 섞지 말 것.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
