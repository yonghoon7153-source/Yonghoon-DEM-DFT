#!/usr/bin/env python3
"""Plot AIMD MLIP results: MSD vs t, Arrhenius, σ(T).

Reads JSON files written by tools/modelc_v3/aimd_mlip.py:
    <out_root>/T{T_K}/aimd_results.json
    <out_root>/arrhenius_summary.json

Generates:
  - Figure 1: MSD vs t for Li at each T (overlay) + linear fit
  - Figure 2: Arrhenius plot log D vs 1000/T + linear fit + 300 K extrapolation
  - Figure 3: MSD vs t for ALL elements at a chosen T (default 1000 K) —
            shows Li-dominant vs PS4/Cl framework immobility

Usage:
    python3 plot_aimd.py \\
        --out_root /home/ubuntu/work/runs/modelC_v3/aimd \\
        --out_dir  /home/ubuntu/work/runs/modelC_v3/aimd/figs
"""
import argparse
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, FuncFormatter


T_COLOR = {
    600: "#3B5BA0",   # blue
    800: "#E89C2B",   # amber
    1000: "#C44536",  # red
}
ELEM_COLOR = {
    "Li": "#C44536", "Cl": "#3E8E41", "P": "#9B5DE5",
    "S": "#E89C2B", "C": "#222222", "N": "#3F7BB6",
}


def load_t_results(out_root: Path):
    """Return list of (T_K, json_data) sorted by T."""
    results = []
    for d in sorted(out_root.glob("T*")):
        f = d / "aimd_results.json"
        if not f.exists():
            continue
        with open(f) as fh:
            results.append((float(d.name[1:]), json.load(fh)))
    return sorted(results, key=lambda x: x[0])


def plot_msd_li(results, fit_window, out_path):
    fig, ax = plt.subplots(figsize=(7.0, 5.0))
    for T, d in results:
        times = np.array(d["msd_data"]["times_ps"])
        if "Li" not in d["msd_data"]["msd_per_elem_A2"]:
            continue
        msd = np.array(d["msd_data"]["msd_per_elem_A2"]["Li"])
        col = T_COLOR.get(int(T), "#666")
        ax.plot(times, msd, '-', color=col, lw=1.8,
                label=f"{int(T)} K  D = {d['diffusion_fits']['Li']['D_cm2_per_s']:.2e} cm²/s")
        # overlay linear fit
        mask = (times >= fit_window[0]) & (times <= fit_window[1])
        if mask.sum() >= 2:
            p = np.polyfit(times[mask], msd[mask], 1)
            tfit = np.linspace(fit_window[0], fit_window[1], 50)
            ax.plot(tfit, np.polyval(p, tfit), '--', color=col, lw=1.0, alpha=0.7)

    ax.axvspan(fit_window[0], fit_window[1], color='#888', alpha=0.10,
               label=f"linear-fit window ({fit_window[0]}–{fit_window[1]} ps)")
    ax.set_xlabel("Time  (ps)", fontsize=12)
    ax.set_ylabel("Li MSD  (Å²)", fontsize=12)
    ax.set_title("Li ion mean-squared displacement — modelC_v3 AIMD (UMA)", fontsize=12)
    ax.legend(loc='upper left', fontsize=9, frameon=False)
    ax.grid(alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"  → {out_path}")


def plot_arrhenius(results, arr_summary, out_path):
    fig, ax = plt.subplots(figsize=(7.0, 5.5))

    # Data points
    Ts = np.array([T for T, _ in results])
    Ds = np.array([d["diffusion_fits"]["Li"]["D_cm2_per_s"] for _, d in results])
    inv_T_1000 = 1000.0 / Ts
    log10_D = np.log10(Ds)

    for T, lnD in zip(Ts, log10_D):
        col = T_COLOR.get(int(T), "#666")
        ax.plot(1000.0 / T, lnD, 'o', mfc=col, mec='k', mew=1.0, ms=12,
                label=f"{int(T)} K", zorder=5)

    # Arrhenius fit line: ln(D) = ln(D0) - Ea/(kT) → log10(D) = log10(D0) - Ea/(2.303 kT)
    Ea = arr_summary["Ea_eV"]
    D0 = arr_summary["D0_cm2_per_s"]
    kB_eV = 8.617333262e-5
    # Plot fit line over wider range including 300 K extrapolation
    T_fit = np.linspace(280, max(Ts) * 1.1, 200)
    log10_D_fit = np.log10(D0) - Ea / (2.302585 * kB_eV * T_fit)
    ax.plot(1000.0 / T_fit, log10_D_fit, '-', color='#444', lw=1.5, zorder=4,
            label=f"Arrhenius  Ea = {Ea:.3f} eV")

    # 300 K extrapolation marker
    D_300 = arr_summary["D_300K_cm2_per_s_extrapolated"]
    log10_D_300 = np.log10(D_300)
    ax.plot(1000.0 / 300.0, log10_D_300, 'D', mfc='#fffabb', mec='k', mew=1.2, ms=14,
            label=f"300 K extrap  D = {D_300:.2e} cm²/s", zorder=6)

    ax.axvline(1000.0 / 300.0, color='#888', ls=':', lw=0.8, alpha=0.6)
    ax.text(1000.0/300.0 + 0.05, log10_D_300 - 0.6, "300 K\nextrap",
            fontsize=9, color='#666', va='top')

    ax.set_xlabel(r"1000 / T  (K$^{-1}$)", fontsize=12)
    ax.set_ylabel(r"log$_{10}$(D / cm² s$^{-1}$)", fontsize=12)
    ax.set_title("Arrhenius fit — Li diffusion in modelC_v3 (LPSCl1.6)", fontsize=12)
    ax.legend(loc='upper right', fontsize=9, frameon=False)
    ax.grid(alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)

    # Inset: Top-X-axis with T values
    ax2 = ax.twiny()
    xticks_T = [300, 500, 700, 1000, 1500]
    ax2.set_xlim(ax.get_xlim())
    ax2.set_xticks([1000.0 / T for T in xticks_T])
    ax2.set_xticklabels([f"{T}" for T in xticks_T])
    ax2.set_xlabel("T  (K)", fontsize=11)
    ax2.spines['top'].set_visible(True)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"  → {out_path}")


def plot_msd_all_elements(results, T_show, out_path):
    """Show MSD for all elements at chosen T → Li mobile, framework frozen."""
    chosen = None
    for T, d in results:
        if int(T) == int(T_show):
            chosen = d; break
    if chosen is None:
        print(f"  [skip] T={T_show} not in results")
        return
    fig, ax = plt.subplots(figsize=(7.0, 5.0))
    times = np.array(chosen["msd_data"]["times_ps"])
    for elem, msd in chosen["msd_data"]["msd_per_elem_A2"].items():
        col = ELEM_COLOR.get(elem, "#666")
        lw = 2.4 if elem == "Li" else 1.4
        alpha = 1.0 if elem == "Li" else 0.85
        ax.plot(times, msd, '-', color=col, lw=lw, alpha=alpha,
                label=f"{elem}  D = {chosen['diffusion_fits'].get(elem,{}).get('D_cm2_per_s', 0):.2e} cm²/s")
    ax.set_xlabel("Time  (ps)", fontsize=12)
    ax.set_ylabel("MSD  (Å²)", fontsize=12)
    ax.set_title(f"MSD per element at {int(T_show)} K — Li-only conductor (PS₄ + Cl frozen)",
                 fontsize=11)
    ax.legend(loc='upper left', fontsize=9, frameon=False)
    ax.grid(alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"  → {out_path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out_root", required=True,
                    help="dir containing T600/, T800/, ... subdirs")
    ap.add_argument("--out_dir", default=None,
                    help="figure output dir (default: <out_root>/figs)")
    ap.add_argument("--T_msd_elements", type=int, default=1000,
                    help="T to use for per-element MSD plot")
    ap.add_argument("--fit_window_ps", type=float, nargs=2, default=[2.0, 50.0])
    args = ap.parse_args()

    out_root = Path(args.out_root)
    out_dir = Path(args.out_dir) if args.out_dir else out_root / "figs"
    out_dir.mkdir(parents=True, exist_ok=True)

    results = load_t_results(out_root)
    print(f"Loaded {len(results)} temperatures: {[int(T) for T, _ in results]}")

    arr_path = out_root / "arrhenius_summary.json"
    if not arr_path.exists():
        raise SystemExit(f"missing {arr_path}")
    with open(arr_path) as f:
        arr = json.load(f)
    print(f"Arrhenius: Ea = {arr['Ea_eV']:.4f} eV, D0 = {arr['D0_cm2_per_s']:.3e} cm²/s")

    plot_msd_li(results, tuple(args.fit_window_ps), out_dir / "fig_msd_li_vs_t.png")
    plot_arrhenius(results, arr, out_dir / "fig_arrhenius.png")
    plot_msd_all_elements(results, args.T_msd_elements,
                          out_dir / f"fig_msd_all_elements_T{args.T_msd_elements}.png")

    # Combined 1x3 panel for paper
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    # left: MSD Li
    ax = axes[0]
    for T, d in results:
        if "Li" not in d["msd_data"]["msd_per_elem_A2"]:
            continue
        times = np.array(d["msd_data"]["times_ps"])
        msd = np.array(d["msd_data"]["msd_per_elem_A2"]["Li"])
        col = T_COLOR.get(int(T), "#666")
        ax.plot(times, msd, '-', color=col, lw=1.8,
                label=f"{int(T)} K")
    ax.set_xlabel("Time (ps)"); ax.set_ylabel("Li MSD (Å²)")
    ax.set_title("(a) Li MSD vs t"); ax.legend(fontsize=9, frameon=False)
    ax.grid(alpha=0.3, ls='--')
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)

    # middle: Arrhenius
    ax = axes[1]
    Ts = np.array([T for T, _ in results])
    Ds = np.array([d["diffusion_fits"]["Li"]["D_cm2_per_s"] for _, d in results])
    for T, D in zip(Ts, Ds):
        ax.plot(1000.0/T, np.log10(D), 'o', mfc=T_COLOR.get(int(T), "#666"),
                mec='k', mew=1, ms=11, zorder=5)
    Ea = arr["Ea_eV"]; D0 = arr["D0_cm2_per_s"]
    kB = 8.617333262e-5
    Tf = np.linspace(280, max(Ts)*1.1, 200)
    ax.plot(1000.0/Tf, np.log10(D0) - Ea/(2.302585*kB*Tf), '-', color='#444', lw=1.5, zorder=4,
            label=f"Ea = {Ea:.3f} eV")
    ax.plot(1000.0/300.0, np.log10(arr["D_300K_cm2_per_s_extrapolated"]), 'D',
            mfc='#fffabb', mec='k', mew=1.2, ms=12, zorder=6,
            label=f"300K extrap: {arr['D_300K_cm2_per_s_extrapolated']:.2e} cm²/s")
    ax.axvline(1000.0/300.0, color='#888', ls=':', lw=0.8, alpha=0.6)
    ax.set_xlabel("1000 / T (K⁻¹)"); ax.set_ylabel("log₁₀(D / cm² s⁻¹)")
    ax.set_title("(b) Arrhenius fit"); ax.legend(fontsize=9, frameon=False)
    ax.grid(alpha=0.3, ls='--')
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)

    # right: per-element MSD at chosen T
    ax = axes[2]
    chosen = None
    for T, d in results:
        if int(T) == int(args.T_msd_elements):
            chosen = d; break
    if chosen is not None:
        times = np.array(chosen["msd_data"]["times_ps"])
        for elem, msd in chosen["msd_data"]["msd_per_elem_A2"].items():
            col = ELEM_COLOR.get(elem, "#666")
            lw = 2.4 if elem == "Li" else 1.3
            ax.plot(times, msd, '-', color=col, lw=lw,
                    label=f"{elem}")
    ax.set_xlabel("Time (ps)"); ax.set_ylabel("MSD (Å²)")
    ax.set_title(f"(c) MSD per element at {int(args.T_msd_elements)} K")
    ax.legend(fontsize=9, frameon=False, loc='upper left')
    ax.grid(alpha=0.3, ls='--')
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)

    plt.tight_layout()
    combined = out_dir / "fig_aimd_combined_3panel.png"
    plt.savefig(combined, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"  → {combined}  [3-panel combined for paper]")


if __name__ == "__main__":
    main()
