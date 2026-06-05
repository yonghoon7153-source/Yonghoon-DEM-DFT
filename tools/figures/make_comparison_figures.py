#!/usr/bin/env python3
"""LPSCl vs LPSCl1.6 — paper comparison figures + Origin-ready CSVs.

Reads authoritative DB values (db/properties/*.json + per_bond_json) and emits,
into paper_figures/:
  - one CSV per panel (Origin import: header row + units)
  - one matplotlib preview PNG per panel (draft; Origin = final)

All values are paper-grade (comp1 k444, modelc k663). Elastic comp1 relaxed-ion
is flagged provisional (k221 geometry, k444 refit pending — RMS 0.003 Å so ~same).

Usage:  python3 tools/figures/make_comparison_figures.py
"""
import json
import csv
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "paper_figures"
OUT.mkdir(exist_ok=True)
kB = 8.617333e-5  # eV/K

C1, CM = "#1f77b4", "#d62728"   # comp1 (LPSCl) blue, modelc (LPSCl1.6) red
LB1, LBM = "LPSCl (Li6)", "LPSCl1.6 (Li5.4)"

plt.rcParams.update({"figure.dpi": 130, "font.size": 11, "axes.grid": True,
                     "grid.alpha": 0.3, "axes.axisbelow": True})


def write_csv(name, header, rows):
    p = OUT / f"{name}.csv"
    with open(p, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"  csv  → {p.name}  ({len(rows)} rows)")


def save(fig, name):
    p = OUT / f"{name}.png"
    fig.savefig(p, bbox_inches="tight")
    plt.close(fig)
    print(f"  png  → {p.name}")


# ----------------------------------------------------------------------
# 1. AIMD Arrhenius  (ln D vs 1000/T)  + diffusivity table
# ----------------------------------------------------------------------
def fig_arrhenius():
    T = np.array([600.0, 800.0, 1000.0])
    D1 = np.array([2.677e-6, 5.907e-6, 1.019e-5])   # comp1 [2,50]
    DM = np.array([7.90e-6, 2.05e-5, 4.55e-5])       # modelc
    x = 1000.0 / T
    # fit ln D = ln D0 - Ea/(kB T)
    def fit(D):
        A = np.vstack([1.0 / (kB * T), np.ones_like(T)]).T
        sl, ic = np.linalg.lstsq(A, np.log(D), rcond=None)[0]
        return -sl, np.exp(ic)  # Ea, D0
    Ea1, D01 = fit(D1)
    EaM, D0M = fit(DM)

    write_csv("fig1_arrhenius",
              ["T_K", "1000_over_T", "D_LPSCl_cm2s", "lnD_LPSCl",
               "D_LPSCl16_cm2s", "lnD_LPSCl16"],
              [[T[i], round(x[i], 4), D1[i], round(np.log(D1[i]), 4),
                DM[i], round(np.log(DM[i]), 4)] for i in range(3)])
    write_csv("fig1_arrhenius_fit",
              ["system", "Ea_eV", "D0_cm2s", "R2"],
              [["LPSCl", round(Ea1, 4), f"{D01:.3e}", 0.999],
               ["LPSCl1.6", round(EaM, 4), f"{D0M:.3e}", 0.992]])

    fig, ax = plt.subplots(figsize=(5.2, 4.2))
    xf = np.linspace(x.min() * 0.97, x.max() * 1.03, 50)
    Tf = 1000.0 / xf
    ax.plot(x, np.log(D1), "o", color=C1, ms=8, label=f"{LB1}  Ea={Ea1:.3f} eV")
    ax.plot(xf, np.log(D01) - Ea1 / (kB * Tf), "-", color=C1, lw=1.5)
    ax.plot(x, np.log(DM), "s", color=CM, ms=8, label=f"{LBM}  Ea={EaM:.3f} eV")
    ax.plot(xf, np.log(D0M) - EaM / (kB * Tf), "-", color=CM, lw=1.5)
    # crossover
    Tc = (EaM - Ea1) / (kB * np.log(D0M / D01))
    ax.axvline(1000.0 / Tc, color="gray", ls=":", lw=1)
    ax.text(1000.0 / Tc, ax.get_ylim()[0] + 0.3, f" Tcross≈{Tc:.0f}K",
            color="gray", fontsize=9, rotation=90, va="bottom")
    ax.set_xlabel("1000 / T  (K$^{-1}$)")
    ax.set_ylabel("ln D  (D in cm$^2$/s)")
    ax.set_title("AIMD Arrhenius (UMA-s-1p1, [2,50] ps)")
    ax.legend(fontsize=9)
    save(fig, "fig1_arrhenius")


# ----------------------------------------------------------------------
# 2. ICOHP per bond type  (grouped bar)
# ----------------------------------------------------------------------
def fig_icohp_type():
    pb = json.load(open(ROOT / "db/properties/per_bond_json/bonds_comp1_k444.json"))
    pm = json.load(open(ROOT / "db/properties/per_bond_json/bonds_modelc_k663.json"))
    keys = [("P-S", "P-S"), ("Li-Cl", "Cl-Li"), ("Li-S", "Li-S"), ("S-S", "S-S")]
    c1 = [pb["icohp_per_bond_type_eV"][k]["icohp_eV"] for _, k in keys]
    cm = [pm["icohp_per_bond_type_eV"][k]["icohp_eV"] for _, k in keys]
    labels = [k for k, _ in keys]
    write_csv("fig2_icohp_type",
              ["bond", "ICOHP_LPSCl_eV", "ICOHP_LPSCl16_eV", "delta_pct"],
              [[labels[i], c1[i], cm[i], round((cm[i] / c1[i] - 1) * 100, 1)]
               for i in range(4)])

    fig, ax = plt.subplots(figsize=(5.4, 4.0))
    xi = np.arange(4); w = 0.38
    ax.bar(xi - w / 2, c1, w, color=C1, label=LB1)
    ax.bar(xi + w / 2, cm, w, color=CM, label=LBM)
    ax.set_xticks(xi); ax.set_xticklabels(labels)
    ax.set_ylabel("ICOHP per bond (eV)  — more negative = stronger")
    ax.set_title("LOBSTER ICOHP per bond type (ext basis)")
    ax.legend(fontsize=9)
    ax.invert_yaxis()
    save(fig, "fig2_icohp_type")


# ----------------------------------------------------------------------
# 3. ICOHP per site  (universal anchor + 4d-Cl antisite)
# ----------------------------------------------------------------------
def fig_icohp_site():
    pb = json.load(open(ROOT / "db/properties/per_bond_json/bonds_comp1_k444.json"))
    pm = json.load(open(ROOT / "db/properties/per_bond_json/bonds_modelc_k663.json"))
    sites = ["Li-S(PS4)", "Li-S(4d)", "Li-Cl(4a)", "Li-Cl(4d)"]
    def g(d, s): return d["icohp_per_site"].get(s, {}).get("icohp_eV", np.nan)
    c1 = [g(pb, s) for s in sites]
    cm = [g(pm, s) for s in sites]
    write_csv("fig3_icohp_site",
              ["site", "ICOHP_LPSCl_eV", "ICOHP_LPSCl16_eV", "note"],
              [[sites[i], c1[i], cm[i],
                {"Li-S(4d)": "universal anchor (free S2-)",
                 "Li-Cl(4d)": "anti-site, LPSCl1.6 only"}.get(sites[i], "")]
               for i in range(4)])

    fig, ax = plt.subplots(figsize=(5.6, 4.0))
    xi = np.arange(4); w = 0.38
    b1 = ax.bar(xi - w / 2, np.nan_to_num(c1), w, color=C1, label=LB1)
    b2 = ax.bar(xi + w / 2, np.nan_to_num(cm), w, color=CM, label=LBM)
    # mark comp1 missing Li-Cl(4d)
    if np.isnan(c1[3]):
        ax.text(3 - w / 2, -0.1, "n/a", ha="center", fontsize=8, color=C1)
    ax.set_xticks(xi); ax.set_xticklabels(sites, fontsize=9)
    ax.set_ylabel("ICOHP per bond (eV)")
    ax.set_title("ICOHP per site — anchor & anti-site")
    ax.legend(fontsize=9); ax.invert_yaxis()
    save(fig, "fig3_icohp_site")


# ----------------------------------------------------------------------
# 4. Bader charges  (grouped bar)
# ----------------------------------------------------------------------
def fig_bader():
    pb = json.load(open(ROOT / "db/properties/per_bond_json/bonds_comp1_k444.json"))
    pm = json.load(open(ROOT / "db/properties/per_bond_json/bonds_modelc_k663.json"))
    els = ["Li", "Cl", "S", "P"]
    c1 = [pb["bader_charges"][e]["q_e"] for e in els]
    cm = [pm["bader_charges"][e]["q_e"] for e in els]
    write_csv("fig4_bader",
              ["element", "q_LPSCl_e", "q_LPSCl16_e"],
              [[els[i], c1[i], cm[i]] for i in range(4)])

    fig, ax = plt.subplots(figsize=(5.2, 4.0))
    xi = np.arange(4); w = 0.38
    ax.bar(xi - w / 2, c1, w, color=C1, label=LB1)
    ax.bar(xi + w / 2, cm, w, color=CM, label=LBM)
    ax.axhline(0, color="k", lw=0.8)
    ax.set_xticks(xi); ax.set_xticklabels(els)
    ax.set_ylabel("Bader charge q (e)")
    ax.set_title("Bader charges (AE density, plot_num=17)")
    ax.legend(fontsize=9)
    save(fig, "fig4_bader")


# ----------------------------------------------------------------------
# 5. Bond lengths  (bar + error)
# ----------------------------------------------------------------------
def fig_bonds():
    # from comparison MD (DFT V0, cutoff-unified)
    data = {  # bond: (comp1 mean, comp1 sig, modelc mean, modelc sig)
        "P-S":   (2.073, 0.036, 2.064, 0.011),
        "Li-S":  (2.461, 0.106, 2.465, 0.094),
        "Li-Cl": (2.607, 0.129, 2.532, 0.119),
        "S-S":   (3.595, 0.199, 3.519, 0.178),
    }
    labels = list(data)
    write_csv("fig5_bond_lengths",
              ["bond", "d_LPSCl_A", "sig_LPSCl", "d_LPSCl16_A", "sig_LPSCl16"],
              [[k, *data[k]] for k in labels])

    fig, ax = plt.subplots(figsize=(5.4, 4.0))
    xi = np.arange(len(labels)); w = 0.38
    ax.bar(xi - w / 2, [data[k][0] for k in labels], w, yerr=[data[k][1] for k in labels],
           color=C1, label=LB1, capsize=3)
    ax.bar(xi + w / 2, [data[k][2] for k in labels], w, yerr=[data[k][3] for k in labels],
           color=CM, label=LBM, capsize=3)
    ax.set_xticks(xi); ax.set_xticklabels(labels)
    ax.set_ylabel("Bond length (Å)")
    ax.set_title("Bond lengths (DFT V0)")
    ax.legend(fontsize=9)
    save(fig, "fig5_bond_lengths")


# ----------------------------------------------------------------------
# 6. Elastic moduli  (clamped vs relaxed, B/G/E_VRH)
# ----------------------------------------------------------------------
def fig_elastic():
    # comparison MD II.8  (comp1 relaxed = provisional k221, k444 refit pending)
    rows = [
        # mode, modulus, comp1, modelc
        ("clamped", "B_VRH", 43.59, 44.47),
        ("clamped", "G_VRH", 20.12, 20.05),
        ("clamped", "E_VRH", 52.31, 52.30),
        ("relaxed", "B_VRH", 25.18, 23.40),
        ("relaxed", "G_VRH", 8.26, 10.61),
        ("relaxed", "E_VRH", 22.33, 27.66),
    ]
    write_csv("fig6_elastic",
              ["mode", "modulus", "LPSCl_GPa", "LPSCl16_GPa", "note"],
              [[*r, "comp1 relaxed=provisional(k444 pending)" if r[0] == "relaxed" else ""]
               for r in rows])

    fig, axes = plt.subplots(1, 2, figsize=(8.6, 4.0), sharey=True)
    for ax, mode in zip(axes, ["clamped", "relaxed"]):
        sub = [r for r in rows if r[0] == mode]
        labels = [r[1] for r in sub]
        xi = np.arange(3); w = 0.38
        ax.bar(xi - w / 2, [r[2] for r in sub], w, color=C1, label=LB1)
        ax.bar(xi + w / 2, [r[3] for r in sub], w, color=CM, label=LBM)
        ax.set_xticks(xi); ax.set_xticklabels(labels)
        ttl = mode + ("-ion" if mode == "relaxed" else "-ion")
        if mode == "relaxed":
            ttl += "  (comp1 † k444 pending)"
        ax.set_title(ttl)
        ax.legend(fontsize=8)
    axes[0].set_ylabel("Modulus (GPa)")
    fig.suptitle("Elastic moduli — vacancy paradox (relaxed-ion resolves it)")
    save(fig, "fig6_elastic")


# ----------------------------------------------------------------------
# 7. EOS  (V/atom, V/fu, B0)
# ----------------------------------------------------------------------
def fig_eos():
    rows = [["V0_per_atom_A3", 19.55, 19.62],
            ["V0_per_fu_A3", 254.16, 243.29],
            ["B0_GPa", 26.233, 21.71],
            ["B0_prime", 4.171, 7.01]]
    write_csv("fig7_eos", ["quantity", "LPSCl", "LPSCl16"], rows)

    fig, ax = plt.subplots(figsize=(4.6, 4.0))
    xi = np.arange(2); w = 0.5
    ax.bar(xi, [26.233, 21.71], w, color=[C1, CM])
    ax.set_xticks(xi); ax.set_xticklabels([LB1, LBM], fontsize=9)
    ax.set_ylabel("B0 (BM-EOS, GPa)")
    ax.set_title("Bulk modulus B0 (BM3 fit)")
    for i, v in enumerate([26.233, 21.71]):
        ax.text(i, v + 0.3, f"{v:.2f}", ha="center", fontsize=9)
    save(fig, "fig7_eos")


# ----------------------------------------------------------------------
# 8. Band gap  (bar) + edges
# ----------------------------------------------------------------------
def fig_gap():
    el = json.load(open(ROOT / "db/properties/electronic.json"))
    bg = {b["id"]: b for b in el["band_gaps"]}
    c, m = bg["comp1_v3"], bg["modelc_v3"]
    write_csv("fig8_gap",
              ["system", "gap_eV", "VBM_eV", "CBM_eV", "EF_eV"],
              [["LPSCl", c["gap_eV"], c["VBM_eV"], c["CBM_eV"], c["EF_eV_qe"]],
               ["LPSCl1.6", m["gap_eV"], m["VBM_eV"], m["CBM_eV"], m["EF_eV_qe"]]])

    fig, ax = plt.subplots(figsize=(4.4, 4.0))
    xi = np.arange(2); w = 0.5
    g = [c["gap_eV"], m["gap_eV"]]
    ax.bar(xi, g, w, color=[C1, CM])
    ax.set_xticks(xi); ax.set_xticklabels([LB1, LBM], fontsize=9)
    ax.set_ylabel("PBE band gap (eV)")
    ax.set_title("DOS gap (k-converged)")
    ax.set_ylim(0, 2.4)
    for i, v in enumerate(g):
        ax.text(i, v + 0.03, f"{v:.2f}", ha="center", fontsize=10)
    ax.text(0.5, 2.2, "Δ = −0.06 eV (≈same)", ha="center", fontsize=9, color="gray")
    save(fig, "fig8_gap")


if __name__ == "__main__":
    print(f"=== paper comparison figures → {OUT} ===")
    fig_arrhenius()
    fig_icohp_type()
    fig_icohp_site()
    fig_bader()
    fig_bonds()
    fig_elastic()
    fig_eos()
    fig_gap()
    print("done. CSV+PNG per panel in paper_figures/.")
