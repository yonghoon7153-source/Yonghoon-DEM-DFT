#!/usr/bin/env python3
"""Phase B + Phase C: local relax on top-K sites and orientation sweep.

Reads scan_rigid_<form>.json (from scan_binding_rigid.py), picks the
K best (lowest E_bind) sites, and for each:

  Phase B — Short UMA relax of the complex (SDCP free, bottom 50% slab
            frozen), measure E_bind_relax = E_relaxed - E_slab_iso - E_SDCP_iso
            with E_slab_iso re-evaluated for the SAME constraint set (free
            top layers) for self-consistency.

  Phase C — At each top site (fixed dx,dy,dz), rotate the molecule around
            the z-axis at multiple azimuthal angles and re-evaluate
            single-point E_bind. Find the best orientation.

Output: phase_BC_<form>.json with per-site relax + orientation results.

Usage:
    python3 phase_bc.py \\
        --scan_json scan_rigid_doped.json \\
        --slab slab_init.xyz \\
        --molecule sdcp_doped.xyz \\
        --form doped \\
        --top_k 5 \\
        --rot_angles 0,30,60,90,120,150,180,210,240,270,300,330 \\
        --device cuda --task oc20
"""
import argparse, json, time
from pathlib import Path
import numpy as np


def find_anchor_S(atoms):
    sym = np.array(atoms.get_chemical_symbols())
    pos = atoms.positions
    s_idx = np.where(sym == "S")[0]
    best, best_no = -1, -1
    for i in s_idx:
        dists = np.linalg.norm(pos - pos[i], axis=1)
        n_o = int(((sym == "O") & (dists < 2.0) & (dists > 0)).sum())
        if n_o > best_no:
            best_no = n_o; best = i
    return int(best)


def orient_so3_down(atoms, anchor_idx):
    """Sulfonate S→COM vector aligned with +z (sulfonate down)."""
    pos = atoms.positions.copy()
    com = pos.mean(axis=0)
    v = com - pos[anchor_idx]; v = v / np.linalg.norm(v)
    target = np.array([0.0, 0.0, 1.0])
    axis = np.cross(v, target)
    if np.linalg.norm(axis) < 1e-6:
        return atoms
    axis = axis / np.linalg.norm(axis)
    cos_t = float(np.dot(v, target))
    sin_t = float(np.linalg.norm(np.cross(v, target)))
    K = np.array([[0,-axis[2],axis[1]],[axis[2],0,-axis[0]],[-axis[1],axis[0],0]])
    R = np.eye(3) + sin_t*K + (1-cos_t)*(K @ K)
    pos_c = pos - pos[anchor_idx]
    atoms.positions = pos_c @ R.T + pos[anchor_idx]
    return atoms


def rotate_around_z(atoms, anchor_idx, theta_deg):
    """Rotate molecule by theta around the z-axis through the anchor."""
    theta = np.radians(theta_deg)
    c, s = np.cos(theta), np.sin(theta)
    R = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    pos = atoms.positions.copy()
    pos_c = pos - pos[anchor_idx]
    atoms.positions = pos_c @ R.T + pos[anchor_idx]
    return atoms


def place_molecule_at(slab, mol_template, anchor_idx, dx_frac, dy_frac, dz_A):
    from ase import Atoms
    z_top = slab.positions[:, 2].max()
    cell = slab.cell.array
    target = dx_frac * cell[0] + dy_frac * cell[1]
    target[2] = z_top + dz_A
    mol_pos = mol_template.positions.copy()
    shift = target - mol_pos[anchor_idx]
    mol_pos += shift
    combined = Atoms(
        symbols=list(slab.symbols) + list(mol_template.symbols),
        positions=np.vstack([slab.positions, mol_pos]),
        cell=cell, pbc=True,
    )
    return combined


def expand_cell_c(slab, max_dz, mol_z_extent, vacuum=15.0):
    z_top = slab.positions[:, 2].max()
    new_c = z_top + max_dz + mol_z_extent + vacuum
    if new_c > slab.cell.array[2, 2]:
        new_cell = slab.cell.array.copy()
        new_cell[2] = [0, 0, new_c]
        slab.set_cell(new_cell, scale_atoms=False)
        print(f"  Expanded cell c → {new_c:.2f} Å")
    return slab


def load_uma(device, task):
    from fairchem.core.units.mlip_unit.api.inference import InferenceSettings
    from fairchem.core import pretrained_mlip, FAIRChemCalculator
    predictor = pretrained_mlip.get_predict_unit(
        "uma-s-1p1", device=device,
        inference_settings=InferenceSettings(
            tf32=True, activation_checkpointing=False, merge_mole=False,
            compile=False, wigner_cuda=False,
        ),
    )
    return FAIRChemCalculator(predictor, task_name=task)


def freeze_slab_atoms(atoms, n_slab):
    """Freeze ALL slab atoms (paper-standard adsorption convention).

    For adsorbate-on-surface relax, freezing the whole slab eliminates the
    'slab co-relax' artifact (the slab also rearranging, dragging the
    molecule energy down to unphysical regions). Only molecule atoms move.
    """
    from ase.constraints import FixAtoms
    mask = np.zeros(len(atoms), dtype=bool)
    mask[:n_slab] = True
    atoms.set_constraint(FixAtoms(mask=mask))
    return atoms, int(mask.sum())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan_json", required=True)
    ap.add_argument("--slab", required=True)
    ap.add_argument("--molecule", required=True)
    ap.add_argument("--form", required=True)
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--top_k", type=int, default=5)
    ap.add_argument("--rot_angles", default="0,30,60,90,120,150,180,210,240,270,300,330")
    ap.add_argument("--fmax", type=float, default=0.1)
    ap.add_argument("--max_steps", type=int, default=50)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--task", default="oc20")
    args = ap.parse_args()

    out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    rot_angles = [float(x) for x in args.rot_angles.split(",")]

    from ase.io import read, write
    from ase.optimize import LBFGS

    print(f"=== Phase B+C for {args.form} ===")
    scan = json.load(open(args.scan_json))
    E_bind = np.array(scan["E_bind"])  # (nx, ny, nz)
    dx_vals = np.array(scan["dx_vals"])
    dy_vals = np.array(scan["dy_vals"])
    dz_vals = np.array(scan["dz_vals"])
    E_slab_iso_scan = scan["E_slab_iso"]
    E_SDCP_iso_scan = scan["E_SDCP_iso"]

    # Pick top-K (lowest E_bind) sites
    flat = E_bind.flatten()
    idx_sorted = np.argsort(flat)[:args.top_k]
    top_sites = []
    for fi in idx_sorted:
        i, j, k = np.unravel_index(fi, E_bind.shape)
        top_sites.append({
            "i": int(i), "j": int(j), "k": int(k),
            "dx_frac": float(dx_vals[i]), "dy_frac": float(dy_vals[j]),
            "dz_A": float(dz_vals[k]),
            "E_bind_rigid": float(E_bind[i, j, k]),
        })
    print(f"Top {args.top_k} rigid sites (E_bind):")
    for s in top_sites:
        print(f"  ({s['dx_frac']:.2f}, {s['dy_frac']:.2f}, {s['dz_A']:.1f}Å)  → {s['E_bind_rigid']:.4f} eV")

    # Load slab + molecule, prep
    slab = read(args.slab)
    mol_orig = read(args.molecule)
    anchor = find_anchor_S(mol_orig)
    mol_orig = orient_so3_down(mol_orig, anchor)
    mol_z_extent = mol_orig.positions[:, 2].max() - mol_orig.positions[:, 2].min()
    slab = expand_cell_c(slab, args.max_steps and 6.0, mol_z_extent, 15.0)
    n_slab = len(slab)

    # Re-evaluate references with top-2-layer-free slab (Phase B consistency)
    print(f"\nLoading UMA-s-1p1 (task={args.task})...")
    calc = load_uma(args.device, args.task)

    # E_slab_iso with same constraint as Phase B (bottom 50% frozen)
    slab_for_ref = slab.copy()
    slab_for_ref, n_frozen = freeze_slab_atoms(slab_for_ref, n_slab)
    slab_for_ref.calc = calc
    print(f"  slab freeze: {n_frozen}/{n_slab} atoms")
    # Note: for relax-consistent reference we should also relax the bare slab,
    # but since rigid scan used E_slab_iso = SP of init slab and it gave physical
    # E_bind, we keep that here too (just SP). Pure consistency note for paper:
    # E_bind_relax uses E_slab_iso(init,SP) — that's a self-consistent rigid
    # baseline; full DFT-grade would relax the slab separately.
    E_slab_iso = float(slab_for_ref.get_potential_energy())
    print(f"  E_slab_iso (init SP) = {E_slab_iso:.4f} eV")
    print(f"  E_SDCP_iso (from scan) = {E_SDCP_iso_scan:.4f} eV")

    # === Phase C: orientation sweep at top-1 (best) site ===
    print(f"\n=== Phase C: orientation sweep at top-1 site ===")
    s = top_sites[0]
    phaseC_results = []
    best_C = None
    for theta in rot_angles:
        m = mol_orig.copy()
        m = rotate_around_z(m, anchor, theta)
        complex_atoms = place_molecule_at(slab, m, anchor, s["dx_frac"], s["dy_frac"], s["dz_A"])
        complex_atoms.calc = calc
        t0 = time.time()
        E = float(complex_atoms.get_potential_energy())
        E_bind = E - E_slab_iso_scan - E_SDCP_iso_scan
        rec = {"theta_deg": theta, "E_complex": E, "E_bind": E_bind, "time_s": time.time()-t0}
        phaseC_results.append(rec)
        marker = ""
        if best_C is None or E_bind < best_C["E_bind"]:
            best_C = rec; marker = " ★"
        print(f"  θ={theta:6.1f}°  E_bind = {E_bind:8.4f} eV  ({rec['time_s']:.2f}s){marker}")

    print(f"\nPhase C best: θ={best_C['theta_deg']:.1f}°  E_bind={best_C['E_bind']:.4f} eV")
    print(f"  (rigid scan was at θ=0°, E_bind={top_sites[0]['E_bind_rigid']:.4f} eV)")

    # === Phase B: local relax on top-K sites ===
    # ★ Apply Phase C best orientation (θ) so Phase B starts from the most
    # favorable rotation found above — self-consistent. For doped this is
    # usually θ=0° (no-op); for neutral it's typically a nonzero θ.
    best_theta = best_C["theta_deg"]
    print(f"\n=== Phase B: local relax on top-{args.top_k} sites "
          f"(starting orientation: θ={best_theta:.1f}° from Phase C) ===")
    phaseB_results = []
    for idx, s in enumerate(top_sites):
        print(f"\n--- Site {idx+1}/{args.top_k}: ({s['dx_frac']:.2f}, {s['dy_frac']:.2f}, {s['dz_A']:.1f}Å) "
              f"rigid={s['E_bind_rigid']:.4f} θ={best_theta:.1f}° ---")
        m = mol_orig.copy()
        if abs(best_theta) > 1e-3:
            m = rotate_around_z(m, anchor, best_theta)
        complex_atoms = place_molecule_at(slab, m, anchor,
                                           s["dx_frac"], s["dy_frac"], s["dz_A"])
        complex_atoms, _ = freeze_slab_atoms(complex_atoms, n_slab)
        complex_atoms.calc = calc

        t0 = time.time()
        opt = LBFGS(complex_atoms, logfile=str(out_dir / f"relax_site{idx+1}.log"))
        opt.run(fmax=args.fmax, steps=args.max_steps)
        relax_dt = time.time() - t0

        E_relax = float(complex_atoms.get_potential_energy())
        fmax_final = float(np.max(np.linalg.norm(complex_atoms.get_forces(), axis=1)))
        E_bind_relax = E_relax - E_slab_iso - E_SDCP_iso_scan

        # Anchor S final position (after relax)
        anchor_final_z = float(complex_atoms.positions[n_slab + anchor, 2])
        z_top = slab.positions[:, 2].max()

        rec = {
            **s,
            "start_theta_deg": float(best_theta),
            "E_complex_relax": E_relax,
            "E_bind_relax": E_bind_relax,
            "fmax_final": fmax_final,
            "anchor_z_after_relax": anchor_final_z,
            "dz_after_relax": anchor_final_z - z_top,
            "relax_steps": opt.get_number_of_steps(),
            "time_s": relax_dt,
        }
        phaseB_results.append(rec)
        write(out_dir / f"site{idx+1}_relaxed.xyz", complex_atoms, format="extxyz")
        print(f"  E_bind_relax = {E_bind_relax:.4f} eV  (Δ from rigid: {E_bind_relax - s['E_bind_rigid']:+.4f})")
        print(f"  fmax = {fmax_final:.4f} eV/Å, {opt.get_number_of_steps()} steps, {relax_dt:.0f}s")
        print(f"  dz: {s['dz_A']:.2f} → {rec['dz_after_relax']:.2f} Å")

    # Save combined results
    result = {
        "form": args.form,
        "scan_source": str(args.scan_json),
        "uma_task": args.task,
        "E_slab_iso": E_slab_iso,
        "E_SDCP_iso": E_SDCP_iso_scan,
        "phase_C_orientation": phaseC_results,
        "phase_C_best": best_C,
        "phase_B_top_sites": phaseB_results,
        "phase_B_best": min(phaseB_results, key=lambda r: r["E_bind_relax"]),
    }
    out_json = out_dir / f"phase_BC_{args.form}.json"
    json.dump(result, open(out_json, "w"), indent=2)
    print(f"\n→ {out_json}")

    # Headline summary
    print("\n" + "="*60)
    print(f"SUMMARY — {args.form}")
    print(f"  rigid best:       {top_sites[0]['E_bind_rigid']:+.4f} eV")
    print(f"  Phase C best (rot): {result['phase_C_best']['E_bind']:+.4f} eV at θ={result['phase_C_best']['theta_deg']}°")
    print(f"  Phase B best (relax): {result['phase_B_best']['E_bind_relax']:+.4f} eV")
    print("="*60)


if __name__ == "__main__":
    main()
