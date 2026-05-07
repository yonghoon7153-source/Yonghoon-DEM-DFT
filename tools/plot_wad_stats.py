#!/usr/bin/env python3
"""
Wad statistics plots — SI figure analogs for Choi 2025 style.

Uses RAW 20-seed Wad data from db/properties/adhesion.json.

Outputs (in output/):
  1. wad_seed_convergence.png  — running mean ± std vs # seeds (Fig S5 analog)
  2. wad_histogram.png          — normalized frequency per comp (Fig S13/S14 analog)
  3. wad_paired_deltas.png      — same-seed comp1 vs comp2B, comp3 vs comp4 etc.
  4. wad_summary.json           — structured output for easy re-plotting

Usage:
    python tools/plot_wad_stats.py
    python tools/plot_wad_stats.py --no-paired   # skip paired plot
"""
import json
import argparse
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "properties" / "adhesion.json"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

# BML color palette (from kb/papers/origin_adhesion_guide.md)
COLORS = {
    "comp3":  "#4FBDFF",   # sky blue
    "comp4":  "#52B788",   # green
    "comp5":  "#F4A261",   # orange
    "comp1":  "#9B5DE5",   # purple
    "comp2B": "#2A9D8F",   # teal
}
FAMILIES = {"comp1": "Li6", "comp2B": "Li6",
            "comp3": "Li5.4", "comp4": "Li5.4", "comp5": "Li5.4"}
ORDER = ["comp3", "comp4", "comp5", "comp1", "comp2B"]


def load_raw_wad():
    with open(DB) as f:
        data = json.load(f)
    xy = data["adhesion_v5_crystalline_slab"]["xy_shift"]["results"]
    raw = {}
    for comp in ORDER:
        if comp not in xy:
            continue
        d = xy[comp]
        wads = d.get("Wad_20seeds") or d.get("Wad")
        if wads is None:
            continue
        raw[comp] = np.asarray(wads, dtype=float)
    return raw


# ── 1. Seed convergence ──────────────────────────────────────────────
def plot_seed_convergence(raw, outpath):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for comp in ORDER:
        w = raw[comp]
        n = len(w)
        ks = np.arange(1, n + 1)
        running_mean = np.cumsum(w) / ks
        # running std: computed from first k samples
        running_std = np.array([w[:k].std(ddof=0) for k in ks])
        ax.plot(ks, running_mean, color=COLORS[comp], lw=1.8, label=comp)
        ax.fill_between(ks, running_mean - running_std, running_mean + running_std,
                        color=COLORS[comp], alpha=0.15)
    ax.set_xlabel("Number of seeds", fontsize=13)
    ax.set_ylabel(r"$W_\mathrm{ad}$ running mean (J/m²)", fontsize=13)
    ax.set_title("Seed convergence of adhesion energy (Choi Fig S5 analog)", fontsize=12)
    ax.legend(ncol=5, fontsize=10, frameon=False, loc="upper center",
              bbox_to_anchor=(0.5, -0.15))
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(outpath, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ {outpath.name}")


# ── 2. Wad distribution histograms ───────────────────────────────────
def plot_histogram(raw, outpath):
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)
    bins = np.arange(0.0, 5.0 + 0.3, 0.3)

    for comp in ["comp1", "comp2B"]:
        axes[0].hist(raw[comp], bins=bins, alpha=0.55, density=True,
                     color=COLORS[comp], label=comp,
                     edgecolor="#404040", lw=0.8)
    for comp in ["comp3", "comp4", "comp5"]:
        axes[1].hist(raw[comp], bins=bins, alpha=0.55, density=True,
                     color=COLORS[comp], label=comp,
                     edgecolor="#404040", lw=0.8)

    for ax, fam in zip(axes, ["Li6 family", "Li5.4 family"]):
        ax.set_xlabel(r"$W_\mathrm{ad}$ (J/m²)", fontsize=13)
        ax.set_title(fam, fontsize=12)
        ax.legend(frameon=False, fontsize=11)
        ax.grid(alpha=0.3)
    axes[0].set_ylabel("Normalized frequency", fontsize=13)
    fig.suptitle("Wad distribution (Choi Fig S13/S14 analog)", fontsize=12, y=1.02)
    fig.tight_layout()
    fig.savefig(outpath, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ {outpath.name}")


# ── 3. Paired deltas (same-seed registry) ────────────────────────────
def plot_paired(raw, outpath):
    # Only comp1 vs comp2B pair is guaranteed same seed (see adhesion.json)
    # Li5.4 family has same SE size so same seed = same registry
    if len(raw.get("comp1", [])) != len(raw.get("comp2B", [])):
        print("  ! comp1/2B raw arrays differ in length; skipping paired")
        return

    c1, c2 = raw["comp1"], raw["comp2B"]
    dW = c2 - c1   # positive = comp2B > comp1 (reversal)

    fig, ax = plt.subplots(figsize=(7, 4.2))
    n = len(dW)
    colors = ["#E63946" if d > 0 else "#2A9D8F" for d in dW]
    ax.bar(np.arange(n), dW, color=colors, edgecolor="#404040", lw=0.8)
    ax.axhline(0, color="#404040", lw=1)
    ax.axhline(dW.mean(), color="#404040", ls="--", lw=1.2,
               label=f"mean = {dW.mean():+.3f} (Δ>0 = comp2B > comp1)")
    ax.set_xlabel("Seed index", fontsize=13)
    ax.set_ylabel(r"$W_\mathrm{ad}$(comp2B) − $W_\mathrm{ad}$(comp1) (J/m²)",
                  fontsize=12)
    ax.set_title("Paired comparison: Li6 family Br effect (per seed)", fontsize=12)
    ax.legend(frameon=False, fontsize=10)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(outpath, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ {outpath.name}")


# ── 4. Summary JSON ──────────────────────────────────────────────────
def save_summary(raw, outpath):
    summary = {"per_composition": {}, "ordering": ORDER}
    for comp, w in raw.items():
        summary["per_composition"][comp] = {
            "n_seeds": int(len(w)),
            "mean": float(w.mean()),
            "std": float(w.std(ddof=0)),
            "median": float(np.median(w)),
            "min": float(w.min()),
            "max": float(w.max()),
            "family": FAMILIES.get(comp),
        }
    if len(raw.get("comp1", [])) == len(raw.get("comp2B", [])):
        dW = raw["comp2B"] - raw["comp1"]
        summary["paired_Li6"] = {
            "pair": "comp2B - comp1",
            "mean_delta": float(dW.mean()),
            "std_delta": float(dW.std(ddof=0)),
            "se_mean": float(dW.std(ddof=1) / np.sqrt(len(dW))),
            "n": int(len(dW)),
            "n_positive": int((dW > 0).sum()),
        }
    with open(outpath, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"  ✓ {outpath.name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-paired", action="store_true")
    args = ap.parse_args()

    print("Loading raw Wad data from", DB.relative_to(ROOT))
    raw = load_raw_wad()
    for comp in ORDER:
        if comp in raw:
            w = raw[comp]
            print(f"  {comp}: n={len(w)}, mean={w.mean():.3f}, std={w.std():.3f}")

    print("\nGenerating plots in", OUT.relative_to(ROOT))
    plot_seed_convergence(raw, OUT / "wad_seed_convergence.png")
    plot_histogram(raw, OUT / "wad_histogram.png")
    if not args.no_paired:
        plot_paired(raw, OUT / "wad_paired_deltas.png")
    save_summary(raw, OUT / "wad_summary.json")
    print("\nDone.")


if __name__ == "__main__":
    main()
