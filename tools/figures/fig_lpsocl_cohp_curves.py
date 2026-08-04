#!/usr/bin/env python3
"""fig_lpsocl_cohp_curves.py — LPSOCl bonding/antibonding **곡선** (-pCOHP vs E).

입력은 gabia 에서 회수한 압축 CSV (tools/figures/extract_cohp_curves.py 산출):
    db/properties/lpsocl_cohp_curves_origin.csv

⚠ 곡선은 **결합당 평균**이다 (extract 쪽 규약). 그래서 패널 높이를 그대로 비교해도 되고,
   E_F 까지의 면적이 곧 ICOHP/bond 다. family 의 sum 곡선과는 정규화가 다르니
   nd/modelc 4-panel 과 세로 눈금을 직접 비교하지 말 것.

⚠ x 눈금은 **행 안에서만** 공유한다. P 계 결합(-6~-8 eV/bond)과 Li 계(-1~-2)를 한 눈금에
   두면 Li 패널이 뭉개진다. 행마다 눈금을 밝혀 적는다 — 행이 다르면 높이 비교 금지.

  python3 tools/figures/fig_lpsocl_cohp_curves.py
"""
import argparse
import csv
import json
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "figures"))
from house_style import INK, MUT, ELEM, apply_axes                  # noqa: E402

SRC = ROOT / "db" / "properties" / "lpsocl_cohp_curves_origin.csv"
OUT = ROOT / "docs" / "figures" / "icohp" / "lpsocl_COHP_curves.png"

# 패널색 = 그 결합의 '주역' 원소색 (P-O/Li-O 가 같은 crimson 인 건 의도 — O 패널 묶음)
PANEL_COLOR = {"P-S": ELEM["P"], "P-O": ELEM["O"], "Li-S": ELEM["S"],
               "Li-Cl": ELEM["Cl"], "Li-O": ELEM["O"], "S-S": MUT}
DASH_ON = {"Li-O"}          # 같은 색 두 패널을 구분하는 테두리 표시


def read_csv(path):
    """→ (E, {label: mean curve}, meta dict)"""
    meta, header, rows = {}, None, []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                body = line[1:].strip()
                if body.startswith("{"):
                    try:
                        meta = json.loads(body)
                    except json.JSONDecodeError:
                        pass
                continue
            if header is None:
                header = next(csv.reader([line]))
                continue
            rows.append(next(csv.reader([line])))
    A = np.array(rows, dtype=float)
    E = A[:, 0]
    curves = {h[len("mean_pCOHP_"):]: A[:, i]
              for i, h in enumerate(header) if h.startswith("mean_pCOHP_")}
    return E, curves, meta


def panel(ax, E, y, color, label, icohp, n, xlim, ylim, dashed=False, cov=None):
    ax.fill_betweenx(E, 0, np.where(y > 0, y, 0), color=color, alpha=0.5, lw=0)
    ax.fill_betweenx(E, 0, np.where(y < 0, y, 0), color=color, alpha=0.5, lw=0)
    ax.plot(y, E, color=color, lw=1.1, ls="--" if dashed else "-")
    ax.axvline(0, color=INK, lw=0.7)
    ax.axhline(0, color=MUT, ls="--", lw=0.8)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    dx, dy = xlim[1] - xlim[0], ylim[1] - ylim[0]
    ax.text(xlim[0] + dx * 0.06, ylim[1] - dy * 0.06, "Antibonding",
            fontsize=8.5, style="italic", color=MUT, ha="left", va="top")
    ax.text(xlim[1] - dx * 0.06, ylim[0] + dy * 0.30, "Bonding",
            fontsize=8.5, style="italic", color=MUT, ha="right")
    ax.text(xlim[1] - dx * 0.04, 0.15, "$E_F$", fontsize=9, color=MUT,
            ha="right", va="bottom")
    ax.text(xlim[1] - dx * 0.04, ylim[1] - dy * 0.005, f"{label}  (N={n})",
            fontsize=11.5, fontweight="bold", ha="right", va="top", color=INK,
            bbox=dict(facecolor=color, alpha=0.18, edgecolor="none",
                      boxstyle="round,pad=0.3"))
    # ⚠ 상자의 ICOHP 는 LOBSTER 의 **전 에너지** 적분이다. COHPCAR 격자가 -inf 에서
    #   시작하지 않아 깊은 결합 기여가 그림 밖에 있는 경우가 있다 (LPSOCl P-O 는 30%만 창 안).
    #   그때 "상자 값 = 보이는 면적" 으로 읽히면 안 되므로 커버리지를 같이 적는다.
    txt = f"ICOHP = {icohp:.2f} eV/bond"
    if cov is not None and cov < 0.95:
        txt += f"\n({cov*100:.0f}% inside window)"
    ax.text(0, ylim[0] + dy * 0.035, txt,
            ha="center", va="bottom", fontsize=9.5, fontweight="bold", color=INK,
            bbox=dict(boxstyle="round,pad=0.35", facecolor="white",
                      edgecolor=("#b91c1c" if (cov is not None and cov < 0.6) else MUT),
                      lw=(1.3 if (cov is not None and cov < 0.6) else 0.8)))
    apply_axes(ax, xlabel=r"$-$pCOHP per bond")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=str(SRC))
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--groups", default="P-S,P-O|Li-S,Li-Cl,Li-O",
                    help="행 구분 '|' — 행 안에서만 x 눈금 공유")
    ap.add_argument("--ylim", type=float, nargs=2, default=[-12, 6])
    args = ap.parse_args()

    E, curves, meta = read_csv(args.csv)
    pairs = meta.get("pairs", meta)
    rows = [[l for l in g.split(",") if l.strip() in curves] for g in args.groups.split("|")]
    rows = [r for r in rows if r]
    if not rows:
        raise SystemExit(f"CSV 안에 요청한 패널이 없다. 있는 것: {list(curves)}")
    ncol = max(len(r) for r in rows)
    ylim = tuple(args.ylim)
    win = (E >= ylim[0]) & (E <= ylim[1])

    fig = plt.figure(figsize=(3.5 * ncol, 5.4 * len(rows)))
    # 행마다 패널 수가 다를 수 있다 (2 + 3). 열 수를 그 lcm 으로 잡아야 어느 행이든
    # 균등 분할된다 — ncol 이나 ncol*nrow 로 잡으면 (3,4) 같은 조합에서 칸이 어긋난다.
    span = math.lcm(*[len(r) for r in rows]) if len(rows) > 1 else ncol
    gs = fig.add_gridspec(len(rows), span, hspace=0.30, wspace=0.16)
    k = 0
    for ri, labs in enumerate(rows):
        xmax = max(float(np.abs(curves[l][win]).max()) for l in labs) * 1.18
        w = span // len(labs)
        for ci, lab in enumerate(labs):
            c0 = ci * w
            ax = fig.add_subplot(gs[ri, c0:c0 + w])
            m = pairs.get(lab, {})
            panel(ax, E, curves[lab], PANEL_COLOR.get(lab, MUT), lab,
                  float(m.get("ICOHP_per_bond_eV", 0.0)), int(m.get("N", 0)),
                  (-xmax, xmax), ylim, dashed=lab in DASH_ON,
                  cov=(float(m["window_coverage"]) if m.get("window_coverage") is not None else None))
            if ci == 0:
                ax.set_ylabel(r"$E - E_F$  (eV)", fontsize=12, color=INK)
            else:
                ax.set_yticklabels([])
            ax.text(-0.06, 1.03, "abcdefgh"[k], transform=ax.transAxes,
                    fontsize=15, fontweight="bold", color=INK, ha="right", va="bottom")
            k += 1
        fig.text(0.012, 1 - (ri + 0.5) / len(rows),
                 f"x-scale row {ri+1}: $\\pm${xmax:.2f}", rotation=90, va="center",
                 ha="left", fontsize=8.5, color=MUT)

    covs = [pairs.get(l, {}).get("window_coverage") for r in rows for l in r]
    covs = [c for c in covs if c is not None]
    # ⚠ suptitle 을 한 줄로 길게 쓰면 bbox_inches='tight' 가 그림 폭을 늘려버린다
    #   (2857 → 3636 px). 두 줄로 접는다.
    sub = ("\nboxed % = ICOHP fraction inside the plotted window"
           if covs and min(covs) < 0.95 else "")
    fig.suptitle("LPSOCl1.6 (Li$_{27}$P$_5$S$_{21}$OCl$_8$) COHP — LOBSTER 5.1.1, "
                 "per-bond average;  rows have independent x-scales" + sub,
                 fontsize=11, color=MUT, y=1.0)
    outp = Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(outp, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"→ {outp}")
    for labs in rows:
        for l in labs:
            m = pairs.get(l, {})
            print(f"   {l:6s} N={m.get('N','?'):>4}  ICOHP/bond {m.get('ICOHP_per_bond_eV','?')} eV")


if __name__ == "__main__":
    main()
