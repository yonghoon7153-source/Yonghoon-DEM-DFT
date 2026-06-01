#!/usr/bin/env python3
"""Plot 2D heatmap + 1D z-profile for rigid binding scan results.

Reads scan_rigid_<form>.json (from scan_binding_rigid.py) and emits:
  - heatmap_<form>.png : E_bind(dx, dy) at the dz of the global minimum,
                          plus a smaller z-profile inset at the best (dx, dy)
  - heatmap_compare.png: doped vs neutral side-by-side (same colorscale)

Usage:
    python3 plot_binding_heatmap.py \\
        --doped /path/to/sdcp_doped/scan_rigid_doped.json \\
        --neutral /path/to/sdcp_neutral/scan_rigid_neutral.json \\
        --out_dir /path/to/figs
"""
import argparse, json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def load(p):
    with open(p) as f:
        return json.load(f)


def plot_one(d, out_path, title):
    E_bind = np.array(d["E_bind"])  # shape (nx, ny, nz)
    dx = np.array(d["dx_vals"])
    dy = np.array(d["dy_vals"])
    dz = np.array(d["dz_vals"])
    best = d["best"]
    k_min = best["k"]
    i_min, j_min = best["i"], best["j"]

    fig, (axH, axZ) = plt.subplots(1, 2, figsize=(11, 4.6),
                                    gridspec_kw={"width_ratios": [1.4, 1]})

    # Heatmap at dz of global minimum
    plane = E_bind[:, :, k_min]
    # Clip upper bound for nicer colorscale (steric clashes shoot to +50)
    vmin, vmax = plane.min(), max(plane.min() + 8.0, 1.0)  # window: best..best+8 eV
    im = axH.pcolormesh(dx, dy, plane.T, shading="nearest",
                         cmap="viridis_r", vmin=vmin, vmax=vmax)
    axH.set_xlabel("dx (fractional surface a)")
    axH.set_ylabel("dy (fractional surface b)")
    axH.set_title(f"{title}\nE_bind heatmap at dz={dz[k_min]:.1f} Å")
    axH.scatter([dx[i_min]], [dy[j_min]], marker="*", s=180,
                 c="red", edgecolor="white", linewidth=1.5, label=f"best ({best['E_bind_eV']:.2f} eV)")
    axH.legend(loc="upper right", framealpha=0.9)
    cb = plt.colorbar(im, ax=axH); cb.set_label("E_bind (eV)")

    # z-profile at best (dx, dy)
    profile = E_bind[i_min, j_min, :]
    axZ.plot(dz, profile, "-o", color="C0", linewidth=2)
    axZ.axhline(0, color="grey", linestyle=":", linewidth=0.8)
    axZ.axvline(dz[k_min], color="red", linestyle="--", linewidth=1,
                 label=f"best dz={dz[k_min]:.1f} Å")
    axZ.set_xlabel("dz (Å above slab top)")
    axZ.set_ylabel("E_bind (eV)")
    axZ.set_title(f"Z-profile at (dx, dy) = ({dx[i_min]:.2f}, {dy[j_min]:.2f})")
    axZ.legend()
    axZ.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  → {out_path}")


def plot_compare(d_d, d_n, out_path):
    Ebd = np.array(d_d["E_bind"])
    Ebn = np.array(d_n["E_bind"])
    dx_d = np.array(d_d["dx_vals"]); dy_d = np.array(d_d["dy_vals"])
    dx_n = np.array(d_n["dx_vals"]); dy_n = np.array(d_n["dy_vals"])
    best_d = d_d["best"]; best_n = d_n["best"]

    # use each form's own best-dz plane
    plane_d = Ebd[:, :, best_d["k"]]
    plane_n = Ebn[:, :, best_n["k"]]
    # common colorscale: from global min to global min + 8 eV
    glob_min = min(plane_d.min(), plane_n.min())
    vmin = glob_min; vmax = glob_min + 8.0

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    for ax, plane, dx, dy, best, label in [
        (axes[0], plane_d, dx_d, dy_d, best_d, "doped (−SO₃⁻)"),
        (axes[1], plane_n, dx_n, dy_n, best_n, "neutral (−SO₃H)"),
    ]:
        im = ax.pcolormesh(dx, dy, plane.T, shading="nearest",
                            cmap="viridis_r", vmin=vmin, vmax=vmax)
        ax.scatter([dx[best["i"]]], [dy[best["j"]]], marker="*", s=180,
                    c="red", edgecolor="white", linewidth=1.5)
        ax.set_xlabel("dx (fractional)")
        ax.set_ylabel("dy (fractional)")
        ax.set_title(f"{label}\nbest E_bind = {best['E_bind_eV']:.2f} eV at dz={best['dz_A']:.1f} Å")
        plt.colorbar(im, ax=ax, label="E_bind (eV)")

    plt.suptitle("SDCP rigid binding on LiNiO₂ (104) — doped vs neutral",
                 fontsize=12, y=1.02)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  → {out_path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--doped", required=True)
    ap.add_argument("--neutral", required=True)
    ap.add_argument("--out_dir", required=True)
    args = ap.parse_args()

    out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)

    print("Loading scan results...")
    d_d = load(args.doped)
    d_n = load(args.neutral)
    print(f"  doped:   E_bind min = {d_d['best']['E_bind_eV']:.4f} eV")
    print(f"  neutral: E_bind min = {d_n['best']['E_bind_eV']:.4f} eV")

    print("\nPlotting...")
    plot_one(d_d, out_dir / "heatmap_doped.png", "SDCP doped (−SO₃⁻) on LiNiO₂(104)")
    plot_one(d_n, out_dir / "heatmap_neutral.png", "SDCP neutral (−SO₃H) on LiNiO₂(104)")
    plot_compare(d_d, d_n, out_dir / "heatmap_compare.png")
    print("\nDone.")


if __name__ == "__main__":
    main()
