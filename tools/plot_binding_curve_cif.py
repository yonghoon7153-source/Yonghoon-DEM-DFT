#!/usr/bin/env python3
"""
Full pipeline: 20-seed screening + binding curve + CIF snapshots + pretty plot.

For each composition:
  1. If --n-seeds N (default 20): screen N random xy-shift registries,
     pick the one whose Wad is closest to --target-wad (100-seed mean from DB).
     Seed 0 = input xyz as-is.
  2. For the chosen seed: sweep interface gap d, relax at each d, save CIFs:
        {comp}_d{d:.2f}_initial.cif
        {comp}_d{d:.2f}_relaxed.cif
        {comp}_separated.cif      (one per comp, d=+30 Å reference)
  3. Combined plot of 5 comps (WSe2/MoSe2 paper style), + per-comp JSONs.

Two input modes:
  (A) Pre-built xyz (NCM-first ordering, e.g. v5xy files for (001) LiNiO2):
        --xyz comp1_v5xy_s45.xyz ... comp5_v5xy_s50.xyz

  (B) Build fresh from SE CIF with chosen NCM facet (e.g. (104)):
        --se-cif /path/comp1_V0.cif /path/comp2_V0.cif ...
        --facet 104 --se-repeat 2 2 1

Usage:
    # (001) pre-built
    python tools/plot_binding_curve_cif.py \\
        --xyz /data/work/test_xyz/comp*_v5xy_s*.xyz \\
        --n-seeds 20 --d-min 1.5 --d-max 5.5 --n-d 20 \\
        --out-dir /data/work/binding/001

    # (104) build fresh
    python tools/plot_binding_curve_cif.py \\
        --se-cif /data/work/bml/manuscript_support/comp*/v*.cif \\
        --facet 104 --se-repeat 2 2 1 \\
        --n-seeds 20 --out-dir /data/work/binding/104
"""
import argparse
import json
import os
from pathlib import Path

import numpy as np

# 100-seed Wad means (from kb/results/adhesion_final.md) for best-seed picking
DB_WAD_MEAN = {
    "comp1":  1.151,
    "comp2":  1.615,  # = comp2B in our files
    "comp2B": 1.615,
    "comp3":  2.328,
    "comp4":  2.250,
    "comp5":  2.280,
}

# Pretty colors (matches our draft figures)
COLORS = {
    "comp1":  "#9B5DE5",  # purple (Li6, Cl only)
    "comp2":  "#2A9D8F",  # teal
    "comp2B": "#2A9D8F",
    "comp3":  "#4FBDFF",  # sky blue (Li5.4, Cl-rich)
    "comp4":  "#52B788",  # green (Li5.4, mixed)
    "comp5":  "#F4A261",  # orange (Li5.4, Br-rich)
}
MARKERS = {
    "comp1": "D", "comp2": "v", "comp2B": "v",
    "comp3": "o", "comp4": "s", "comp5": "^",
}


# ────────────────────────────────────────────────────────────────────
# NCM / SE construction
# ────────────────────────────────────────────────────────────────────
def detect_n_ncm(atoms):
    """NCM-first atom order convention. Auto-detect by count or element."""
    n = len(atoms)
    if n == 820: return 196   # Li6 family 7x7x1
    if n == 348: return 100   # Li5.4 family 5x5x1
    for i, s in enumerate(atoms.symbols):
        if s in ("P", "S", "Cl", "Br"):
            return i
    raise ValueError(f"Cannot infer n_ncm ({n} atoms)")


def build_ncm_slab(facet=(0, 0, 1), min_slab=10.0, symmetrize=False):
    """LiNiO2 slab at (hkl) using pymatgen SlabGenerator.

    Args:
        facet: Miller index tuple, e.g. (0,0,1) or (1,0,4).
        min_slab: minimum slab thickness in Å.
                  ~10 = 1-layer (001) / few layers (104).
                  ~25 = 5-layer for (104).
        symmetrize: enforce symmetric termination (recommended for non-polar).
    """
    from pymatgen.core import Structure, Lattice
    from pymatgen.core.surface import SlabGenerator
    from pymatgen.io.ase import AseAtomsAdaptor

    bulk = Structure(
        Lattice.hexagonal(2.878, 14.19),
        ["Li", "Ni", "O", "O"],
        [[0, 0, 0.5], [0, 0, 0], [0, 0, 0.2584], [0, 0, 0.7416]],
    )
    gen = SlabGenerator(
        bulk, miller_index=facet,
        min_slab_size=min_slab, min_vacuum_size=2.0,
        center_slab=True, in_unit_planes=False,
    )
    slabs = gen.get_slabs(symmetrize=symmetrize)
    if not slabs:
        raise RuntimeError(f"No slabs for facet {facet}")
    slab = slabs[0]
    return AseAtomsAdaptor.get_atoms(slab)


def apply_bottom_fix(atoms, n_ncm, fix_frac=0.6):
    """FixAtoms on bottom fraction of NCM (bulk-like layer).

    Args:
        fix_frac: 0.6 = freeze bottom 60% of NCM atoms, top 40% free.
                  Set to 0 to disable.
    """
    if fix_frac <= 0:
        return atoms
    from ase.constraints import FixAtoms
    pos = atoms.get_positions()
    ncm_z = pos[:n_ncm, 2]
    z_cut = ncm_z.min() + (ncm_z.max() - ncm_z.min()) * fix_frac
    mask = np.array([
        (i < n_ncm) and (pos[i, 2] < z_cut) for i in range(len(atoms))
    ])
    atoms.set_constraint(FixAtoms(mask=mask))
    print(f"    FixAtoms on bottom {fix_frac*100:.0f}% of NCM "
          f"(z<{z_cut:.2f}): {mask.sum()} atoms frozen")
    return atoms


def stack_interface(ncm, se, gap=2.5, vacuum=30.0, dx=0.0, dy=0.0):
    from ase import Atoms
    ncm_cell = ncm.cell.array.copy()
    se_cart = se.get_positions().copy()
    ncm_inv = np.linalg.inv(ncm_cell)
    se_frac = se_cart @ ncm_inv
    se_frac[:, 0] = (se_frac[:, 0] + dx) % 1.0
    se_frac[:, 1] = (se_frac[:, 1] + dy) % 1.0
    se_pos = se_frac @ ncm_cell
    ncm_pos = ncm.get_positions().copy()
    ncm_pos[:, 2] -= ncm_pos[:, 2].min()
    ncm_zmax = ncm_pos[:, 2].max()
    se_pos[:, 2] -= se_pos[:, 2].min()
    se_pos[:, 2] += ncm_zmax + gap
    combined_cell = ncm_cell.copy()
    combined_cell[2] = [0, 0, se_pos[:, 2].max() + vacuum]
    symbols = list(ncm.symbols) + list(se.symbols)
    positions = np.vstack([ncm_pos, se_pos])
    interface = Atoms(symbols=symbols, positions=positions,
                      cell=combined_cell, pbc=True)
    return interface, len(ncm)


def build_from_cif(se_cif, se_repeat, facet, ncm_repeat=None,
                   gap=2.5, vacuum=30.0, dx=0.0, dy=0.0,
                   min_slab=10.0, symmetrize=False):
    from pymatgen.core import Structure
    from pymatgen.io.ase import AseAtomsAdaptor
    se_struct = Structure.from_file(se_cif)
    se_struct.make_supercell(se_repeat)
    se = AseAtomsAdaptor.get_atoms(se_struct)
    ncm = build_ncm_slab(facet=facet, min_slab=min_slab, symmetrize=symmetrize)
    if ncm_repeat is None:
        se_a = np.linalg.norm(se.cell[0])
        se_b = np.linalg.norm(se.cell[1])
        ncm_a = np.linalg.norm(ncm.cell[0])
        ncm_b = np.linalg.norm(ncm.cell[1])
        nx = max(1, round(se_a / ncm_a))
        ny = max(1, round(se_b / ncm_b))
    else:
        nx, ny = ncm_repeat
    ncm = ncm.repeat((nx, ny, 1))
    return stack_interface(ncm, se, gap=gap, vacuum=vacuum, dx=dx, dy=dy)


# ────────────────────────────────────────────────────────────────────
# Screening + binding curve
# ────────────────────────────────────────────────────────────────────
def setup_calc(device):
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device=device)
    return lambda: FAIRChemCalculator(predictor, task_name="omat")


def relax_quick(atoms, new_calc, fmax=0.05, steps=50):
    from ase.optimize import LBFGS
    a = atoms.copy()
    a.calc = new_calc()
    try:
        LBFGS(a, logfile=None).run(fmax=fmax, steps=steps)
    except Exception as e:
        print(f"    LBFGS warning: {e}")
    return a


def compute_wad(interface, n_ncm, new_calc):
    """Relax → E_int, then separated (+30Å no relax) → E_sep. Wad = (E_sep-E_int)/A·16.0218."""
    area = float(np.linalg.norm(
        np.cross(interface.cell.array[0], interface.cell.array[1])))
    # Relax
    a_int = relax_quick(interface, new_calc, fmax=0.05, steps=60)
    a_int.calc = new_calc()
    E_int = a_int.get_potential_energy()
    # Separated
    a_sep = a_int.copy()
    pos = a_sep.get_positions()
    pos[n_ncm:, 2] += 30.0
    a_sep.set_positions(pos)
    cell = a_sep.cell.array.copy()
    cell[2, 2] += 30.0
    a_sep.set_cell(cell)
    a_sep.calc = new_calc()
    E_sep = a_sep.get_potential_energy()
    Wad = (E_sep - E_int) / area * 16.0218
    return Wad, E_int, E_sep, area, a_int


def screen_seeds(base_interface, n_ncm, n_seeds, new_calc, target_wad=None):
    """Generate n_seeds xy-shifted variants, compute Wad, pick best."""
    print(f"  ── screening {n_seeds} seeds ──")
    ncm_cell = base_interface.cell.array
    rng = np.random.RandomState(42)
    seeds = []
    for s in range(n_seeds):
        if s == 0:
            dx, dy = 0.0, 0.0   # base (no shift)
        else:
            dx, dy = rng.random(), rng.random()
        # apply shift to SE part only
        a = base_interface.copy()
        pos = a.get_positions()
        ncm_inv = np.linalg.inv(ncm_cell)
        se_frac = pos[n_ncm:] @ ncm_inv
        se_frac[:, 0] = (se_frac[:, 0] + dx) % 1.0
        se_frac[:, 1] = (se_frac[:, 1] + dy) % 1.0
        pos[n_ncm:] = se_frac @ ncm_cell
        a.set_positions(pos)

        Wad, E_int, E_sep, area, a_relaxed = compute_wad(a, n_ncm, new_calc)
        print(f"    seed={s} dxdy=({dx:.2f},{dy:.2f})  Wad={Wad:.3f}  E_int={E_int:.2f}")
        seeds.append({"seed": s, "dx": dx, "dy": dy, "Wad": Wad,
                      "E_int": E_int, "E_sep": E_sep, "area": area,
                      "atoms_relaxed": a_relaxed})

    if target_wad is not None:
        best = min(seeds, key=lambda x: abs(x["Wad"] - target_wad))
        print(f"  ★ best seed = #{best['seed']} (Wad={best['Wad']:.3f}, "
              f"target={target_wad:.3f}, Δ={abs(best['Wad']-target_wad):.3f})")
    else:
        # median Wad
        sorted_seeds = sorted(seeds, key=lambda x: x["Wad"])
        best = sorted_seeds[len(sorted_seeds) // 2]
        print(f"  ★ best seed = #{best['seed']} (median Wad={best['Wad']:.3f})")
    return best, seeds


def sweep_d(best_interface_relaxed, n_ncm, new_calc,
            d_min, d_max, n_d, relax=True, fmax=0.05, steps=60,
            cif_dir=None, comp=None):
    from ase.io import write
    from ase.optimize import LBFGS

    pos0 = best_interface_relaxed.get_positions()
    ncm_zmax = pos0[:n_ncm, 2].max()
    area = float(np.linalg.norm(
        np.cross(best_interface_relaxed.cell.array[0],
                 best_interface_relaxed.cell.array[1])))

    # Separated reference
    a_sep = best_interface_relaxed.copy()
    pos_s = a_sep.get_positions()
    pos_s[n_ncm:, 2] += 30.0
    a_sep.set_positions(pos_s)
    cell_s = a_sep.cell.array.copy()
    cell_s[2, 2] += 30.0
    a_sep.set_cell(cell_s)
    a_sep.calc = new_calc()
    E_sep = a_sep.get_potential_energy()
    if cif_dir:
        write(cif_dir / f"{comp}_separated.cif", a_sep)
    print(f"  E_sep = {E_sep:.4f} eV")

    ds = np.linspace(d_min, d_max, n_d)
    E_initial, E_relaxed, d_final = [], [], []

    for d in ds:
        a_d = best_interface_relaxed.copy()
        pos_d = a_d.get_positions()
        shift = (ncm_zmax + d) - pos_d[n_ncm:, 2].min()
        pos_d[n_ncm:, 2] += shift
        a_d.set_positions(pos_d)

        # Initial
        a_d.calc = new_calc()
        E_i = a_d.get_potential_energy()
        E_initial.append(E_i)
        if cif_dir:
            write(cif_dir / f"{comp}_d{d:.2f}_initial.cif", a_d)

        if relax:
            a_r = a_d.copy()
            a_r.calc = new_calc()
            try:
                LBFGS(a_r, logfile=None).run(fmax=fmax, steps=steps)
            except Exception:
                pass
            E_r = a_r.get_potential_energy()
            pos_r = a_r.get_positions()
            d_f = float(pos_r[n_ncm:, 2].min() - pos_r[:n_ncm, 2].max())
            E_relaxed.append(E_r)
            d_final.append(d_f)
            if cif_dir:
                write(cif_dir / f"{comp}_d{d:.2f}_relaxed.cif", a_r)
            Wad_r = (E_sep - E_r) / area * 16.0218
            print(f"    d={d:.2f}→{d_f:.2f}  E_r={E_r:.3f}  Wad={Wad_r:+.3f}")
        else:
            Wad_i = (E_sep - E_i) / area * 16.0218
            print(f"    d={d:.2f}  E_i={E_i:.3f}  Wad={Wad_i:+.3f}")

    E_initial = np.array(E_initial)
    Wad_initial = (E_sep - E_initial) / area * 16.0218
    result = {
        "n_ncm": n_ncm,
        "area_A2": area,
        "d_values_A": ds.tolist(),
        "E_initial_eV": E_initial.tolist(),
        "Wad_initial_Jm2": Wad_initial.tolist(),
        "E_sep_eV": float(E_sep),
    }
    if relax:
        E_relaxed = np.array(E_relaxed)
        d_final_arr = np.array(d_final)
        Wad_relaxed = (E_sep - E_relaxed) / area * 16.0218
        result.update({
            "E_relaxed_eV": E_relaxed.tolist(),
            "d_final_A": d_final_arr.tolist(),
            "Wad_relaxed_Jm2": Wad_relaxed.tolist(),
            "d_eq_A": float(d_final_arr[E_relaxed.argmin()]),
            "Wad_eq_Jm2": float(Wad_relaxed.max()),
        })
    else:
        result.update({
            "d_eq_A": float(ds[E_initial.argmin()]),
            "Wad_eq_Jm2": float(Wad_initial.max()),
        })
    return result


# ────────────────────────────────────────────────────────────────────
# Pretty plot
# ────────────────────────────────────────────────────────────────────
def plot_combined(data_dict, outpath, use_relaxed=True):
    import matplotlib.pyplot as plt
    import matplotlib as mpl

    mpl.rcParams["font.family"] = "DejaVu Sans"
    mpl.rcParams["axes.linewidth"] = 1.2

    fig, ax = plt.subplots(figsize=(7.5, 6))

    for comp, d in data_dict.items():
        if use_relaxed and "Wad_relaxed_Jm2" in d:
            dvals = np.array(d["d_final_A"])
            Wad = np.array(d["Wad_relaxed_Jm2"])
        else:
            dvals = np.array(d["d_values_A"])
            Wad = np.array(d["Wad_initial_Jm2"])
        d_eq = d["d_eq_A"]

        c = COLORS.get(comp, "#666666")
        m = MARKERS.get(comp, "o")
        ax.plot(dvals, -Wad, marker=m, markersize=5, color=c, lw=1.6,
                markeredgecolor="#2a2a2a", markeredgewidth=0.5,
                label=f"{comp}  ({d['Wad_eq_Jm2']:.2f} J/m²)")
        ax.scatter(d_eq, -d["Wad_eq_Jm2"], s=200, marker="*",
                   color=c, edgecolor="#2a2a2a", lw=0.9, zorder=5)

    ax.axhline(0, color="#2a2a2a", lw=0.8, ls="--", alpha=0.5)
    ax.set_xlabel("Interface gap $d$ (Å)", fontsize=13)
    ax.set_ylabel("Adhesion energy (J/m²)", fontsize=13)
    ax.tick_params(labelsize=11)
    title = "Binding curves — argyrodite SE / LiNiO₂"
    ax.set_title(title, fontsize=13)
    leg = ax.legend(loc="upper right", fontsize=10, frameon=True, framealpha=0.9)
    leg.get_frame().set_edgecolor("#aaaaaa")
    ax.grid(alpha=0.25, lw=0.5)
    fig.tight_layout()
    fig.savefig(outpath, dpi=300, bbox_inches="tight")
    print(f"\n✓ {outpath}")


# ────────────────────────────────────────────────────────────────────
# Main
# ────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description=__doc__)
    # input mode A: pre-built xyz
    ap.add_argument("--xyz", nargs="*", default=[],
                    help="pre-built interface xyz (NCM-first)")
    # input mode B: build from SE CIF
    ap.add_argument("--se-cif", nargs="*", default=[],
                    help="SE bulk CIF; NCM is built from scratch")
    ap.add_argument("--facet", default="001",
                    help="NCM Miller facet, e.g. '001' or '104'")
    ap.add_argument("--se-repeat", type=int, nargs=3, default=[2, 2, 1])
    ap.add_argument("--min-slab", type=float, default=10.0,
                    help="NCM slab min thickness Å. (001): 10~14 = 1L. "
                         "(104): 10 = ~2-3L, 25 = ~5L (Choi2025-style).")
    ap.add_argument("--symmetrize", action="store_true",
                    help="force symmetric slab termination (recommended for 104)")
    ap.add_argument("--fix-bottom", type=float, default=0.0,
                    help="FixAtoms on bottom fraction of NCM. "
                         "0 = no fix (default, 1L slab). "
                         "0.6 = freeze bottom 60%% (DFT-standard for 5L). ")

    # screening
    ap.add_argument("--n-seeds", type=int, default=20,
                    help="N xy-shift seeds to screen per comp (0 = use input as-is)")

    # sweep
    ap.add_argument("--d-min", type=float, default=1.5)
    ap.add_argument("--d-max", type=float, default=5.5)
    ap.add_argument("--n-d", type=int, default=20)
    ap.add_argument("--no-relax", action="store_true")
    ap.add_argument("--fmax", type=float, default=0.05)
    ap.add_argument("--steps", type=int, default=60)

    # I/O
    ap.add_argument("--out-dir", default="/data/work/binding_results")
    ap.add_argument("--device", default="cuda")
    args = ap.parse_args()

    from ase.io import read

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    cif_root = out_dir / "cifs"
    cif_root.mkdir(exist_ok=True)

    new_calc = setup_calc(args.device)

    # Build list of (comp, base_interface, n_ncm) to process
    targets = []
    for xyz in args.xyz:
        path = Path(xyz)
        if not path.exists():
            print(f"! skip {xyz} (not found)")
            continue
        atoms = read(path)
        n_ncm = detect_n_ncm(atoms)
        comp = path.stem.split("_")[0]
        targets.append((comp, atoms, n_ncm, f"xyz:{path.name}"))
    for cif in args.se_cif:
        path = Path(cif)
        if not path.exists():
            print(f"! skip {cif} (not found)")
            continue
        comp = path.stem.split("_")[0]
        facet = tuple(int(c) for c in args.facet)
        interface, n_ncm = build_from_cif(
            cif, args.se_repeat, facet, ncm_repeat=None,
            gap=2.5, vacuum=30.0, dx=0.0, dy=0.0,
            min_slab=args.min_slab, symmetrize=args.symmetrize)
        if args.fix_bottom > 0:
            interface = apply_bottom_fix(interface, n_ncm, args.fix_bottom)
        targets.append((comp, interface, n_ncm,
                        f"cif:{path.name} facet=({args.facet}) "
                        f"slab={args.min_slab}Å fix={args.fix_bottom:.1f}"))

    if not targets:
        print("! no input provided")
        return

    all_data = {}
    for comp, base, n_ncm, src in targets:
        print(f"\n═══════════════════════════════════════════════════")
        print(f"  {comp}  ({src})  atoms={len(base)}  n_ncm={n_ncm}")
        print(f"═══════════════════════════════════════════════════")

        if args.n_seeds > 0:
            target_wad = DB_WAD_MEAN.get(comp)
            best, _ = screen_seeds(base, n_ncm, args.n_seeds, new_calc, target_wad)
            best_relaxed = best["atoms_relaxed"]
            chosen_seed = best["seed"]
            chosen_wad = best["Wad"]
        else:
            # Just relax input once, use that
            print(f"  no screening: using input as-is (relax then sweep)")
            best_relaxed = relax_quick(base, new_calc, fmax=0.05, steps=60)
            chosen_seed = 0
            chosen_wad = None

        cif_dir = cif_root / comp
        cif_dir.mkdir(exist_ok=True)

        print(f"\n  ── sweep d: {args.d_min}→{args.d_max} Å, n={args.n_d} ──")
        data = sweep_d(
            best_relaxed, n_ncm, new_calc,
            d_min=args.d_min, d_max=args.d_max, n_d=args.n_d,
            relax=(not args.no_relax), fmax=args.fmax, steps=args.steps,
            cif_dir=cif_dir, comp=comp,
        )
        data["comp"] = comp
        data["source"] = src
        data["chosen_seed"] = chosen_seed
        data["chosen_Wad_Jm2"] = chosen_wad
        all_data[comp] = data

        # per-comp JSON
        json_path = out_dir / f"{comp}_binding.json"
        with open(json_path, "w") as fp:
            json.dump(data, fp, indent=2)
        print(f"  ✓ {json_path}")

    # Combined plot
    if len(all_data) >= 2:
        plot_combined(all_data,
                      out_dir / "binding_curves_combined.png",
                      use_relaxed=(not args.no_relax))

    # Summary JSON
    summary_path = out_dir / "summary.json"
    with open(summary_path, "w") as fp:
        json.dump(all_data, fp, indent=2)
    print(f"✓ {summary_path}")

    print(f"\n★★★ DONE — results in {out_dir}")


if __name__ == "__main__":
    main()
