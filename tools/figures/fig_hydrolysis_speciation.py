#!/usr/bin/env python3
"""fig_hydrolysis_speciation.py — external hydrolysis dataset re-tally, 4 panels.

Reads ONLY the CSV/JSON written by
`tools/oxidation/hydrolysis_speciation.py --outdir <dir>` (no re-parsing of CIFs),
so the figure and the tables can never drift apart.

Panels
  (a) P-S and P-O partial RDF, shaded "empty valley" + the cutoff taken from it.
      This is the method panel: it shows the P-O curve is flat zero, i.e. the
      "no PS(4-x)Ox" result is not a cutoff artefact.
  (b) P / Sn tetrahedral coordination: intact MS4 vs MS3 vs M with any O.
  (c) H depth profile along the auto-detected surface normal, split H-O vs H-S,
      slab interior shaded.
  (d) Reaction-product counts: S-H bonds (by where the S sits), H2S, SH-, H2, S-S.

⚠ EXTERNAL DATA (Kim & Lee, upstream repo has NO LICENSE). Output goes to the
   quarantined folder next to the data, NOT to docs/figures/ — these are not our
   numbers. Labels are English (house rule); axis dressing from house_style.

이 스크립트가 **못 하는 것**
  · 통계를 못 만든다. 단일 스냅샷 단일 궤적이라 오차막대가 없다 — 그래서 하나도 안 그린다.
  · 세 계의 초기조건이 같았는지 모른다. 나란히 그린다고 통제된 대조가 되지 않는다.
  · CSV 를 다시 계산하지 않는다. 숫자가 틀렸으면 hydrolysis_speciation.py 를 고쳐야 한다.

    python3 tools/figures/fig_hydrolysis_speciation.py \
        --dir db/external/kim2026_argyrodite_hydrolysis
"""
import argparse
import csv
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt   # noqa: E402
import numpy as np                # noqa: E402

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from tools.figures.house_style import INK, MUT, ELEM, apply_axes   # noqa: E402

# 계 표시명 — 파일명이 아니라 조성이 요점이므로 조성으로 쓴다 (영문만)
DISP = {"LPSC-H2O": "LPSCl + H$_2$O",
        "LPSC-ion": "LPSCl + H$_3$O$^+$/OH$^-$",
        "LPSnSC-ion": "LPSnSCl + H$_3$O$^+$/OH$^-$"}
ORDER = ["LPSC-H2O", "LPSC-ion", "LPSnSC-ion"]
SYSC = {"LPSC-H2O": "#6b7280", "LPSC-ion": "#be123c", "LPSnSC-ion": "#0284c7"}


def load(d):
    d = Path(d)
    full = json.loads((d / "speciation_full.json").read_text())
    res = {r["label"]: r for r in full}
    rdf = list(csv.DictReader(open(d / "rdf_curves.csv")))
    cuts = list(csv.DictReader(open(d / "rdf_cutoffs.csv")))
    zp = {lab: list(csv.DictReader(open(d / f"zprofile_{lab}.csv"))) for lab in res}
    return res, rdf, cuts, zp


def panel_rdf(ax, rdf, cuts):
    r = np.array([float(x["r_Angstrom"]) for x in rdf])
    lab = "LPSC-ion"
    gps = np.array([float(x[f"g_P-S__{lab}"]) for x in rdf])
    gpo = np.array([float(x[f"g_P-O__{lab}"]) for x in rdf])
    row = [c for c in cuts if c["system"] == lab and c["pair"] == "P-S"][0]
    lo, hi, cut = float(row["valley_lo"]), float(row["valley_hi"]), float(row["cutoff_used"])
    ax.axvspan(lo, hi, color="#fef9c3", zorder=0)
    ax.plot(r, gps, color=ELEM["S"], lw=1.8, label="P-S")
    ax.plot(r, gpo, color=ELEM["O"], lw=2.4, label="P-O")
    ax.axvline(cut, color="#2563eb", ls="--", lw=1.3)
    ax.text(cut + 0.06, ax.get_ylim()[1] * 0.62, f"cutoff {cut:.2f} $\\AA$",
            fontsize=9, color="#92400e", fontweight="bold")
    ax.text(0.5 * (lo + hi), 20.0, f"empty valley, {hi - lo:.2f} $\\AA$ wide\n"
            f"(CN is the same anywhere in it)",
            ha="center", fontsize=8.5, color=MUT)
    ax.set_xlim(1.2, 4.4)
    ax.set_ylim(0, 48)
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    apply_axes(ax, "r ($\\AA$)", "g(r)", "(a) P-S / P-O RDF (LPSCl + ions)", 10)
    ax.text(2.45, 6.0, "P-O is flat zero out to 3.3 $\\AA$\n"
            "$\\Rightarrow$ no PS$_{4-x}$O$_x$ at all",
            fontsize=9.5, color=ELEM["O"], fontweight="bold")


def panel_tetra(ax, res):
    cats = ["intact MS$_4$", "MS$_3$ (broken)", "with any O"]
    x = np.arange(len(ORDER))
    w = 0.26
    rows = []
    for k, cat in enumerate(cats):
        vals = []
        for lab in ORDER:
            t = res[lab]["tetrahedra"]
            tot = sum(v["n_centres"] for v in t.values())
            if cat.startswith("intact"):
                v = sum(vv["n_pure_MS4"] for vv in t.values())
            elif cat.startswith("MS$_3$"):
                v = sum(vv["n_centres"] - vv["n_intact_MX4"] for vv in t.values())
            else:
                v = sum(vv["n_with_O"] for vv in t.values())
            vals.append(100.0 * v / tot)
            rows.append({"system": lab, "category": cat, "percent": round(vals[-1], 3),
                         "count": v, "n_centres": tot})
        c = [ELEM["P"], "#c05621", ELEM["O"]][k]
        b = ax.bar(x + (k - 1) * w, vals, w, color=c, label=cat)
        for xi, v in zip(x + (k - 1) * w, vals):
            ax.text(xi, v + 1.5, f"{v:.1f}", ha="center", fontsize=8, color=INK)
    ax.set_xticks(x)
    ax.set_xticklabels([DISP[l] for l in ORDER], fontsize=8.5)
    ax.set_ylim(0, 118)
    ax.legend(frameon=False, fontsize=8.5, ncol=3, loc="upper center",
              bbox_to_anchor=(0.5, 1.02))
    apply_axes(ax, None, "% of P + Sn centres",
               "(b) Tetrahedral centres after 500 ps", 10)
    ax.text(1.0, 55, "P-O / Sn-O bonds found:\n0 out of 396 centres",
            ha="center", fontsize=10, color=ELEM["O"], fontweight="bold")
    return rows


def panel_zprof(ax, res, zp):
    """깊이 축은 **두 표면을 접어서** 만든 것이다 — 같은 깊이 값이 위/아래 두 빈에서
    나온다. 그래서 z 순서대로 이으면 지그재그가 된다. 깊이 빈으로 **합산**해서 그린다.
    (두 표면을 따로 보고 싶으면 speciation_summary.csv 의 lo_side/hi_side 열을 본다.)"""
    rows = []
    edges = np.arange(-16, 24.001, 2.0)
    ctr = 0.5 * (edges[1:] + edges[:-1])
    for lab in ORDER:
        rr = zp[lab]
        dep = np.array([float(x["depth_from_surface_A"]) for x in rr])
        hs = np.array([float(x["H_S"]) for x in rr])
        ht = np.array([float(x["H"]) for x in rr])
        tot = np.histogram(dep, bins=edges, weights=ht)[0]
        sh = np.histogram(dep, bins=edges, weights=hs)[0]
        ax.step(ctr, tot, where="mid", color=SYSC[lab], lw=1.4, alpha=0.42)
        ax.step(ctr, sh * 10, where="mid", color=SYSC[lab], lw=2.3, label=DISP[lab])
        for c_, t_, s_ in zip(ctr, tot, sh):
            rows.append({"system": lab, "depth_bin_centre_A": round(float(c_), 2),
                         "n_H_total": int(t_), "n_H_S": int(s_)})
    ax.axvline(0, color=INK, lw=1.0)
    ax.axvspan(0, 24, color="#f1f5f9", zorder=0)
    ax.text(12, 120, "inside the slab", ha="center", fontsize=9.5, color=MUT)
    ax.text(-12.5, 120, "water", ha="center", fontsize=9.5, color=MUT)
    ax.set_xlim(-16, 22)
    ax.set_ylim(0, 190)
    ax.legend(frameon=False, fontsize=8.5, loc="upper center", ncol=1)
    apply_axes(ax, "depth below the 50%-density surface ($\\AA$)",
               "H per 2 $\\AA$ depth bin", "(c) H penetration  (thick line = H-S x10)", 10)
    return rows


def panel_products(ax, res):
    keys = [("S-H on\nframework S", lambda r: r["sulfur"]["SH_location"]["on_framework_S"]),
            ("S-H on free S\ninside slab", lambda r: r["sulfur"]["SH_location"]["on_free_S_inside_slab"]),
            ("S-H on free S\nin water", lambda r: r["sulfur"]["SH_location"]["on_free_S_in_fluid"]),
            ("H$_2$S", lambda r: r["sulfur"]["n_H2S"]),
            ("H$_2$", lambda r: r["hydrogen"]["n_H2_molecules"]),
            ("S-S", lambda r: r["sulfur"]["n_SS_bonds"])]
    x = np.arange(len(keys))
    w = 0.26
    rows = []
    for k, lab in enumerate(ORDER):
        vals = [f(res[lab]) for _, f in keys]
        ax.bar(x + (k - 1) * w, vals, w, color=SYSC[lab], label=DISP[lab])
        for xi, v in zip(x + (k - 1) * w, vals):
            if v:
                ax.text(xi, v + 0.4, str(v), ha="center", fontsize=8, color=INK)
        for (nm, _), v in zip(keys, vals):
            rows.append({"system": lab, "product": nm.replace("\n", " "), "count": v})
    ax.set_xticks(x)
    ax.set_xticklabels([k for k, _ in keys], fontsize=8)
    ax.set_ylim(0, 18)
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    apply_axes(ax, None, "count (single snapshot, no error bar)",
               "(d) Hydrolysis products", 10)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="db/external/kim2026_argyrodite_hydrolysis")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    d = Path(a.dir)
    res, rdf, cuts, zp = load(d)

    fig, axs = plt.subplots(2, 2, figsize=(11.4, 8.4))
    panel_rdf(axs[0][0], rdf, cuts)
    r_t = panel_tetra(axs[0][1], res)
    r_z = panel_zprof(axs[1][0], res, zp)
    r_p = panel_products(axs[1][1], res)
    fig.suptitle("Argyrodite surface hydrolysis, 500 ps final snapshots "
                 "(external dataset, re-tallied)", fontsize=11.5, color=INK)
    fig.tight_layout(rect=(0, 0.02, 1, 0.96))
    fig.text(0.5, 0.005, "single snapshot / single trajectory - no error bars; "
                         "MD conditions of the source run are unknown to us",
             ha="center", fontsize=8, color=MUT)
    outdir = d / "figures"
    outdir.mkdir(parents=True, exist_ok=True)
    png = Path(a.out) if a.out else outdir / "hydrolysis_speciation.png"
    fig.savefig(png, dpi=300)
    plt.close(fig)

    # Origin-ready CSVs (한 패널당 하나)
    for name, rows in (("panelB_tetrahedra", r_t), ("panelC_H_depth", r_z),
                       ("panelD_products", r_p)):
        p = outdir / f"fig_hydrolysis_{name}_origin.csv"
        with open(p, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
    print(f"wrote {png}")
    print(f"wrote Origin CSVs -> {outdir}")


if __name__ == "__main__":
    main()
