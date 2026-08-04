#!/usr/bin/env python3
"""fig_lpsocl_icohp.py — LPSOCl ICOHP 막대 그림 + Origin-ready CSV.

⚠ 이건 **적분값(ICOHP)** 그림이다. bonding/antibonding **곡선(-pCOHP vs E)** 은
   `COHPCAR.lobster` 원자료가 필요하고 그건 gabia
   (`/data/work/runs/lpsocl_dft/lobster_ext/`)에만 있다 —
   회수 후 `tools/modelc_v3/plot_lobster_4panel.py` 로 그린다.

  python3 tools/figures/fig_lpsocl_icohp.py
"""
import csv
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "figures"))
try:
    from house_style import INK, MUT, ELEM, apply_axes          # noqa
except Exception:                                                # 최소 폴백
    INK, MUT, ELEM = "#1f2937", "#6b7280", {}
    def apply_axes(ax, xlabel=None, ylabel=None, title=None, fontsize=12):
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        if xlabel: ax.set_xlabel(xlabel, fontsize=fontsize)
        if ylabel: ax.set_ylabel(ylabel, fontsize=fontsize)
        if title: ax.set_title(title, fontsize=fontsize)

SRC = ROOT / "db" / "properties" / "lpsocl_icohp.json"
OUTP = ROOT / "docs" / "figures" / "icohp"
OUTC = ROOT / "db" / "properties"

# 결합별 대표 원소색 (house_style 팔레트 우선)
BOND_COLOR = {"P-O": ELEM.get("O", "#be123c"), "P-S": ELEM.get("P", "#7c3aed"),
              "Li-Cl": ELEM.get("Cl", "#65a30d"), "Li-S": ELEM.get("S", "#c05621"),
              "Li-O": ELEM.get("O", "#be123c"), "S-S": MUT}


def main():
    d = json.loads(SRC.read_text())
    bonds = d["bonds"]
    cmp_ = d.get("comparison_vs_family", {})

    order = sorted(bonds, key=lambda k: bonds[k]["ICOHP_total_eV_per_bond"])
    vals = [-bonds[k]["ICOHP_total_eV_per_bond"] for k in order]      # −ICOHP: 클수록 강한 결합
    ns = [bonds[k]["N"] for k in order]

    # ── CSV (Origin-ready) ──────────────────────────────────────────────
    rows = []
    for k in order:
        b = bonds[k]
        c = cmp_.get(k, {})
        rows.append({
            "bond": k, "N_bonds": b["N"],
            "ICOHP_eV_per_bond": b["ICOHP_total_eV_per_bond"],
            "minus_ICOHP_eV": round(-b["ICOHP_total_eV_per_bond"], 3),
            "modelc": c.get("modelc", ""), "b2o3": c.get("b2o3", ""),
            "note": b.get("note", "") or c.get("note", ""),
        })
    cf = OUTC / "lpsocl_icohp_origin.csv"
    with open(cf, "w", newline="", encoding="utf-8-sig") as f:
        f.write("# LPSOCl1.6 (Li27P5S21OCl8, 62at) ICOHP per bond — Origin-ready\n")
        f.write(f"# {d['method'][:150]}\n")
        f.write(f"# charge spilling {d.get('charge_spilling_pct')}% (<2% 권장 범위)\n")
        f.write("# ⚠ ICOHP 는 **적분값**이다. bonding/antibonding 곡선은 COHPCAR.lobster 필요.\n")
        f.write("# ⚠ 부호 규약: ICOHP 가 음수일수록 결합성이 강하다. minus_ICOHP 는 막대용 양수 변환.\n")
        f.write("# ⚠ comp1 Bader 절대값은 이 표에 섞지 말 것 (다른 밀도 소스 — _comp1_caveat 참조).\n")
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)

    # per-site CSV
    ps = d.get("per_site", {})
    if ps:
        with open(OUTC / "lpsocl_icohp_persite_origin.csv", "w", newline="",
                  encoding="utf-8-sig") as f:
            f.write("# LPSOCl 자리별 ICOHP (Li 앵커 세기) — Origin-ready\n")
            f.write("# free-S(4d)가 PS4-S 보다 Li 를 약 1.5배 강하게 붙든다.\n")
            w = csv.DictWriter(f, fieldnames=["site", "ICOHP_eV_per_bond", "std", "n", "note"])
            w.writeheader()
            for k, v in ps.items():
                w.writerow({"site": k, "ICOHP_eV_per_bond": v["ICOHP_eV"],
                            "std": v.get("std", ""), "n": v.get("n", ""),
                            "note": v.get("note", "")})

    # ── 그림: (a) 결합별 −ICOHP  (b) 3계 비교 ───────────────────────────
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.6),
                                   gridspec_kw={"width_ratios": [1, 1.15]})
    y = np.arange(len(order))
    ax1.barh(y, vals, color=[BOND_COLOR.get(k, MUT) for k in order],
             edgecolor=INK, linewidth=0.6, height=0.66)
    for i, (v, n) in enumerate(zip(vals, ns)):
        ax1.text(v + 0.15, i, f"{v:.2f}  (N={n})", va="center", fontsize=9, color=INK)
    ax1.set_yticks(y); ax1.set_yticklabels(order, fontsize=10)
    ax1.set_xlim(0, max(vals) * 1.30)
    apply_axes(ax1, xlabel="$-$ICOHP per bond (eV)  $\\rightarrow$ stronger",
               title="(a) LPSOCl bond strength")

    # 3계 비교 (host 결합만 — P-O 는 modelc 에 없다)
    keys = [k for k in ("P-S", "Li-Cl", "Li-S", "S-S") if k in cmp_]
    x = np.arange(len(keys)); wd = 0.26
    series = [("modelc", "#0284c7"), ("lpsocl", "#be123c"), ("b2o3", "#7c3aed")]
    for j, (name, col) in enumerate(series):
        v = [-float(cmp_[k][name]) for k in keys]
        ax2.bar(x + (j - 1) * wd, v, wd, label=name, color=col,
                edgecolor=INK, linewidth=0.5)
    ax2.set_xticks(x); ax2.set_xticklabels(keys, fontsize=10)
    apply_axes(ax2, ylabel="−ICOHP per bond (eV)",
               title="(b) Host bonds unchanged by doping (within ~3%)")
    ax2.legend(frameon=False, fontsize=9)
    ax2.set_ylim(0, max(-float(cmp_[k]["lpsocl"]) for k in keys) * 1.25)

    fig.suptitle("LPSOCl1.6 (Li$_{27}$P$_5$S$_{21}$OCl$_8$) ICOHP — LOBSTER 5.1.1, "
                 f"charge spilling {d.get('charge_spilling_pct')}%",
                 fontsize=10.5, color=MUT, y=1.005)
    fig.tight_layout()
    OUTP.mkdir(parents=True, exist_ok=True)
    pf = OUTP / "lpsocl_icohp_bars.png"
    fig.savefig(pf, dpi=300, bbox_inches="tight")
    print(f"→ {pf}\n→ {cf}\n→ {OUTC/'lpsocl_icohp_persite_origin.csv'}")
    print("\n⚠ bonding/antibonding **곡선**은 COHPCAR.lobster 필요 — gabia 에서 회수 후")
    print("   python3 tools/modelc_v3/plot_lobster_4panel.py --cohpcar ... --icohplist ...")


if __name__ == "__main__":
    main()
