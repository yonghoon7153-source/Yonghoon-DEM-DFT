#!/usr/bin/env python3
"""Adatom surface-diffusion barrier — binding-site discovery + CI-NEB (MLIP).

Robust replacement for hand-picked NEB endpoints, written after 4 failed
Li3N attempts that all produced "downhill-into-valley" profiles (interior
image lower than the endpoints → the chosen endpoints were NOT true minima).

The fix: never guess endpoints. Discover the TRUE adatom binding sites by
relaxing the adatom from a grid of starting positions, cluster the relaxed
positions into unique sites, then run CI-NEB only between adjacent TRUE
minima. A valley-detector flags any residual pathology.

Reference (Kim & Cui, ACS Nano 2023, 17, 3168; Li3N(001)):
    adatom binding ≈ -3.44 eV (near surface N),  diffusion barrier 0.133 eV.
    LiC6/graphene Li adatom: ~0.2-0.3 eV (literature).

Stages (each checkpoints to OUTDIR so you can resume / inspect):
  relax  : relax the bare slab (bottom layers frozen)
  sites  : grid-relax the adatom → cluster → unique binding sites + energies
  neb    : CI-NEB between two chosen adjacent sites → barrier + valley check

Usage:
  python3 adatom_diffusion.py relax --slab li3n_001_init.xyz --out li3n_run \\
      --freeze_frac 0.5 --device cuda
  python3 adatom_diffusion.py sites --out li3n_run --adatom Li \\
      --height 1.8 --grid 5 --device cuda
  python3 adatom_diffusion.py neb   --out li3n_run --site_a 0 --site_b 1 \\
      --images 7 --device cuda
"""
import argparse
import json
from pathlib import Path
import numpy as np


# --------------------------------------------------------------------------
# MLIP calculator
# --------------------------------------------------------------------------
def make_predictor(model="uma-s-1p1", device="cuda"):
    from fairchem.core import pretrained_mlip
    return pretrained_mlip.get_predict_unit(model, device=device)


def calc_from(predictor, task="oc20"):
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    return FAIRChemCalculator(predictor, task_name=task)


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def bottom_frozen_indices(atoms, freeze_frac, exclude_top_n=0):
    """Indices of slab atoms with z below z_min + freeze_frac*(z_max-z_min).
    exclude_top_n: ignore the topmost N atoms when measuring the slab span
    (used when an adatom is already present)."""
    z = atoms.positions[:, 2]
    if exclude_top_n > 0:
        order = np.argsort(z)
        span_idx = order[:-exclude_top_n]
    else:
        span_idx = np.arange(len(atoms))
    zmin, zmax = z[span_idx].min(), z[span_idx].max()
    zt = zmin + freeze_frac * (zmax - zmin)
    return [i for i in range(len(atoms)) if z[i] < zt], zmin, zmax, zt


def pbc_xy_dist(p, q, cell):
    """Minimum-image in-plane distance between two cartesian points."""
    d = np.array(p[:2]) - np.array(q[:2])
    # use 2D part of cell
    A = cell[:2, :2]
    try:
        f = np.linalg.solve(A.T, d)
    except np.linalg.LinAlgError:
        return np.linalg.norm(d)
    f -= np.round(f)
    d2 = A.T @ f
    return np.linalg.norm(d2)


# --------------------------------------------------------------------------
# stage: relax bare slab
# --------------------------------------------------------------------------
def stage_relax(args):
    from ase.io import read, write
    from ase.optimize import BFGS
    from ase.constraints import FixAtoms

    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    slab = read(args.slab)
    frozen, zmin, zmax, zt = bottom_frozen_indices(slab, args.freeze_frac)
    print(f"[relax] {len(slab)} atoms, slab z=[{zmin:.2f},{zmax:.2f}], "
          f"freeze z<{zt:.2f} → {len(frozen)} frozen")
    slab.set_constraint(FixAtoms(indices=frozen))
    pred = make_predictor(args.model, args.device)
    slab.calc = calc_from(pred, args.task)
    e0 = slab.get_potential_energy()
    print(f"[relax] E_init = {e0:.4f} eV")
    opt = BFGS(slab, logfile=str(out / "relax_slab.log"),
               trajectory=str(out / "relax_slab.traj"))
    opt.run(fmax=args.fmax, steps=args.max_steps)
    e1 = slab.get_potential_energy()
    write(str(out / "slab_relaxed.xyz"), slab)
    meta = {"n_atoms": len(slab), "E_slab_eV": float(e1),
            "E_before": float(e0), "frozen_indices": frozen,
            "z_top": float(slab.positions[:, 2].max()),
            "freeze_frac": args.freeze_frac, "fmax": args.fmax}
    (out / "slab_meta.json").write_text(json.dumps(meta, indent=2))
    print(f"[relax] E_slab = {e1:.4f} eV (ΔE={e1-e0:.4f}) → {out/'slab_relaxed.xyz'}")


# --------------------------------------------------------------------------
# stage: discover binding sites
# --------------------------------------------------------------------------
def stage_sites(args):
    from ase import Atom
    from ase.io import read, write
    from ase.optimize import BFGS
    from ase.constraints import FixAtoms

    out = Path(args.out)
    slab = read(str(out / "slab_relaxed.xyz"))
    meta = json.loads((out / "slab_meta.json").read_text())
    frozen = meta["frozen_indices"]
    z_top = meta["z_top"]
    E_slab = meta["E_slab_eV"]
    cell = np.array(slab.cell)

    pred = make_predictor(args.model, args.device)

    # reference chemical potential for the adatom (single atom in a box) —
    # only affects absolute binding energy, not the diffusion barrier.
    mu = None
    if args.mu_ref_ev is not None:
        mu = args.mu_ref_ev

    print(f"[sites] grid {args.grid}x{args.grid} over surface cell, "
          f"adatom {args.adatom} at z_top+{args.height} Å")
    results = []
    g = args.grid
    for i in range(g):
        for j in range(g):
            fa, fb = (i + 0.5) / g, (j + 0.5) / g
            xy = fa * cell[0] + fb * cell[1]
            ad = slab.copy()
            ad.append(Atom(args.adatom, (xy[0], xy[1], z_top + args.height)))
            ad.set_constraint(FixAtoms(indices=frozen))
            ad.calc = calc_from(pred, args.task)
            opt = BFGS(ad, logfile=None)
            opt.run(fmax=args.fmax, steps=args.max_steps)
            E = ad.get_potential_energy()
            pos = ad.positions[-1].copy()
            results.append({"start_frac": [fa, fb], "E_eV": float(E),
                            "adatom_pos": pos.tolist()})
            print(f"  start({fa:.2f},{fb:.2f}) → xy=({pos[0]:.2f},{pos[1]:.2f}) "
                  f"z={pos[2]:.2f}  E={E:.4f}")

    # cluster relaxed adatom xy positions (PBC) into unique sites
    tol = args.cluster_tol
    clusters = []  # list of dict: {members:[idx], E_min, pos, slab_with_ad}
    for r in results:
        placed = False
        for c in clusters:
            if pbc_xy_dist(r["adatom_pos"], c["pos"], cell) < tol:
                c["members"].append(r)
                if r["E_eV"] < c["E_min"]:
                    c["E_min"] = r["E_eV"]; c["pos"] = r["adatom_pos"]
                placed = True
                break
        if not placed:
            clusters.append({"members": [r], "E_min": r["E_eV"],
                             "pos": r["adatom_pos"]})

    clusters.sort(key=lambda c: c["E_min"])
    e_global = clusters[0]["E_min"]
    print(f"\n[sites] {len(clusters)} unique binding site(s) "
          f"(cluster tol {tol} Å):")
    sites = []
    for k, c in enumerate(clusters):
        binding = (c["E_min"] - E_slab - mu) if mu is not None else None
        rel = c["E_min"] - e_global
        sites.append({
            "site_id": k, "pos": c["pos"], "E_eV": c["E_min"],
            "E_rel_to_global_eV": rel,
            "binding_eV": binding, "n_grid_hits": len(c["members"]),
        })
        bstr = f"binding={binding:.3f}" if binding is not None else "binding=n/a"
        print(f"  site {k}: xy=({c['pos'][0]:.2f},{c['pos'][1]:.2f}) z={c['pos'][2]:.2f}"
              f"  E_rel={rel:+.4f} eV  {bstr}  ({len(c['members'])} hits)")

    # save the relaxed slab+adatom for each unique site (for NEB endpoints)
    from ase import Atom as _Atom
    for s in sites:
        ad = slab.copy()
        ad.append(_Atom(args.adatom, s["pos"]))
        ad.set_constraint(FixAtoms(indices=frozen))
        write(str(out / f"site_{s['site_id']}.xyz"), ad)

    # adjacency (nearest-neighbor site pairs)
    print("\n[sites] adjacent site pairs (candidate hops):")
    pairs = []
    for a in range(len(sites)):
        for b in range(a + 1, len(sites)):
            d = pbc_xy_dist(sites[a]["pos"], sites[b]["pos"], cell)
            if d < args.hop_cutoff:
                pairs.append({"a": a, "b": b, "dist_A": float(d)})
                print(f"  hop {a}→{b}: {d:.2f} Å  "
                      f"(ΔE_site={sites[b]['E_eV']-sites[a]['E_eV']:+.4f} eV)")

    (out / "sites.json").write_text(json.dumps(
        {"E_slab_eV": E_slab, "mu_ref_eV": mu, "adatom": args.adatom,
         "height": args.height, "grid": args.grid, "cluster_tol": tol,
         "sites": sites, "hop_pairs": pairs,
         "all_grid_results": results}, indent=2))
    print(f"\n[sites] → {out/'sites.json'}  + site_*.xyz")
    if mu is None:
        print("  (binding energy n/a — pass --mu_ref_ev <E_Li_metal_per_atom> "
              "to compare with reference -3.44 eV)")


# --------------------------------------------------------------------------
# stage: CI-NEB between two true sites
# --------------------------------------------------------------------------
def stage_neb(args):
    from ase.io import read, write
    from ase.mep import NEB
    from ase.optimize import BFGS, FIRE
    from ase.constraints import FixAtoms

    out = Path(args.out)
    meta = json.loads((out / "slab_meta.json").read_text())
    frozen = meta["frozen_indices"]
    init = read(str(out / f"site_{args.site_a}.xyz"))
    final = read(str(out / f"site_{args.site_b}.xyz"))
    print(f"[neb] {args.site_a}→{args.site_b}, {args.images} images")

    from ase.constraints import FixedPlane
    ad_idx = len(init) - 1  # adatom is last atom
    images = [init.copy() for _ in range(args.images - 1)] + [final.copy()]
    for im in images:
        cons = [FixAtoms(indices=frozen)]
        if args.constrain_z:
            # adatom may move only in xy (z pinned) → no incorporation dive,
            # NEB still finds the curved in-plane minimum-energy path
            cons.append(FixedPlane(ad_idx, direction=[0, 0, 1]))
        im.set_constraint(cons)
    neb = NEB(images, k=args.spring_k, climb=False, method="improvedtangent",
              allow_shared_calculator=False)
    neb.interpolate(mic=True)
    if args.constrain_z:
        # force all interpolated images to the endpoint adatom height
        z_ad = init.positions[ad_idx, 2]
        for im in images:
            im.positions[ad_idx, 2] = z_ad
        print(f"[neb] adatom z constrained to {z_ad:.2f} Å (planar diffusion)")

    pred = make_predictor(args.model, args.device)
    for im in images:
        im.calc = calc_from(pred, args.task)

    Opt = BFGS if args.optimizer == "bfgs" else FIRE
    # Phase 1: regular
    print(f"[neb] phase 1 (regular, max {args.steps1})")
    opt = Opt(neb, logfile=str(out / "neb.log"),
              trajectory=str(out / "neb.traj"))
    opt.run(fmax=args.fmax, steps=args.steps1)
    # Phase 2: climbing image
    print(f"[neb] phase 2 (CI, max {args.steps2})")
    neb.climb = True
    opt = Opt(neb, logfile=str(out / "neb.log"),
              trajectory=str(out / "neb.traj"))
    opt.run(fmax=args.fmax, steps=args.steps2)

    energies = [im.get_potential_energy() for im in images]
    e0 = energies[0]
    rel = [e - e0 for e in energies]
    imax = int(np.argmax(rel))
    barrier_fwd = rel[imax] - rel[0]
    barrier_rev = rel[imax] - rel[-1]
    interior_min = min(rel[1:-1]) if args.images > 2 else 0.0

    # valley detector
    valley = interior_min < min(rel[0], rel[-1]) - args.valley_tol
    asym = abs(rel[0] - rel[-1])

    print(f"\n[neb] === profile ===")
    for i, r in enumerate(rel):
        mark = " ← TS" if i == imax else ""
        print(f"  img {i}: {r:+.4f} eV{mark}")
    print(f"\n  forward barrier : {barrier_fwd:.4f} eV")
    print(f"  reverse barrier : {barrier_rev:.4f} eV")
    print(f"  endpoint asym   : {asym:.4f} eV")
    if valley:
        vidx = 1 + int(np.argmin(rel[1:-1]))
        print(f"  ⚠ VALLEY DETECTED: interior img {vidx} ({interior_min:+.4f}) "
              f"below endpoints → endpoints are NOT true minima.")
        print(f"     → re-run 'sites' (finer grid) or add the valley image as a "
              f"new site and NEB to it.")
    else:
        print(f"  ✓ clean barrier (no valley)")

    write(str(out / f"neb_path_{args.site_a}_{args.site_b}.xyz"), images)
    res = {"site_a": args.site_a, "site_b": args.site_b,
           "n_images": args.images, "energies_eV": energies,
           "rel_energies_eV": rel, "barrier_fwd_eV": barrier_fwd,
           "barrier_rev_eV": barrier_rev, "ts_image": imax,
           "endpoint_asymmetry_eV": asym, "valley_detected": bool(valley),
           "interior_min_eV": interior_min, "fmax": args.fmax,
           "model": args.model, "task": args.task}
    (out / f"neb_result_{args.site_a}_{args.site_b}.json").write_text(
        json.dumps(res, indent=2))
    print(f"\n[neb] → neb_result_{args.site_a}_{args.site_b}.json")


# --------------------------------------------------------------------------
# stage: DRAG scan (reference method — adatom xy pinned along path, substrate
# relaxed). Robust when the adatom would otherwise incorporate into the slab,
# which makes free NEB collapse. Matches Kim & Cui's "threshold energies
# needed to adsorb Li adatom across the diffusion pathway".
# --------------------------------------------------------------------------
def stage_drag(args):
    from ase import Atom
    from ase.io import read, write
    from ase.optimize import BFGS
    from ase.constraints import FixAtoms, FixedLine

    out = Path(args.out)
    meta = json.loads((out / "slab_meta.json").read_text())
    frozen = list(meta["frozen_indices"])
    A = read(str(out / f"site_{args.site_a}.xyz"))
    B = read(str(out / f"site_{args.site_b}.xyz"))
    posA = A.positions[-1].copy()
    posB = B.positions[-1].copy()
    z_ads = args.ad_z if args.ad_z is not None else float(posA[2])
    slab = A[:-1]  # substrate only (adatom is last)
    ad_idx = len(slab)
    print(f"[drag] {args.site_a}→{args.site_b}, {args.n_points} points, "
          f"adatom z={'relaxed-in-z' if args.relax_z else f'fixed {z_ads:.2f}'}")
    print(f"[drag] xyA=({posA[0]:.2f},{posA[1]:.2f}) xyB=({posB[0]:.2f},{posB[1]:.2f})  "
          f"dist={np.hypot(*(posB[:2]-posA[:2])):.2f} Å")

    pred = make_predictor(args.model, args.device)
    energies, zs, xys = [], [], []
    for k in range(args.n_points):
        t = k / (args.n_points - 1)
        xy = (1 - t) * posA[:2] + t * posB[:2]
        atoms = slab.copy()
        atoms.append(Atom(args.adatom, (xy[0], xy[1], z_ads)))
        if args.relax_z:
            # adatom may move only along z (xy pinned); substrate free
            cons = [FixAtoms(indices=frozen),
                    FixedLine(ad_idx, direction=[0, 0, 1])]
        else:
            # adatom fully pinned (xyz); substrate free — rigid "threshold E"
            cons = [FixAtoms(indices=frozen + [ad_idx])]
        atoms.set_constraint(cons)
        atoms.calc = calc_from(pred, args.task)
        opt = BFGS(atoms, logfile=None)
        opt.run(fmax=args.fmax, steps=args.max_steps)
        E = atoms.get_potential_energy()
        energies.append(E); zs.append(float(atoms.positions[-1, 2]))
        xys.append([float(xy[0]), float(xy[1])])
        print(f"  pt {k}/{args.n_points-1} t={t:.2f} xy=({xy[0]:.2f},{xy[1]:.2f}) "
              f"z={atoms.positions[-1,2]:.2f}  E={E:.4f}")

    e0 = energies[0]
    rel = [e - e0 for e in energies]
    imax = int(np.argmax(rel))
    barrier_fwd = rel[imax] - rel[0]
    barrier_rev = rel[imax] - rel[-1]
    asym = abs(rel[0] - rel[-1])
    print(f"\n[drag] === profile ===")
    for k, r in enumerate(rel):
        mark = " ← max" if k == imax else ""
        print(f"  pt {k}: {r:+.4f} eV  (z={zs[k]:.2f}){mark}")
    print(f"\n  forward barrier : {barrier_fwd:.4f} eV")
    print(f"  reverse barrier : {barrier_rev:.4f} eV")
    print(f"  endpoint asym   : {asym:.4f} eV")
    # diving check: did the adatom drop far below its start height?
    if min(zs) < z_ads - args.dive_tol:
        print(f"  ⚠ adatom dropped to z={min(zs):.2f} (start {z_ads:.2f}) — "
              f"incorporation leaking in; use rigid mode (omit --relax_z) or raise floor")
    else:
        print(f"  ✓ adatom stayed on surface (z {min(zs):.2f}–{max(zs):.2f})")

    res = {"mode": "drag", "relax_z": args.relax_z, "site_a": args.site_a,
           "site_b": args.site_b, "n_points": args.n_points, "z_ads": z_ads,
           "energies_eV": energies, "rel_energies_eV": rel, "z_path": zs,
           "xy_path": xys, "barrier_fwd_eV": barrier_fwd,
           "barrier_rev_eV": barrier_rev, "endpoint_asymmetry_eV": asym,
           "max_point": imax, "model": args.model, "task": args.task}
    (out / f"drag_result_{args.site_a}_{args.site_b}.json").write_text(
        json.dumps(res, indent=2))
    print(f"\n[drag] → drag_result_{args.site_a}_{args.site_b}.json")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--out", required=True)
    common.add_argument("--model", default="uma-s-1p1")
    common.add_argument("--task", default="oc20")
    common.add_argument("--device", default="cuda")
    common.add_argument("--fmax", type=float, default=0.03)
    common.add_argument("--max_steps", type=int, default=300)

    pr = sub.add_parser("relax", parents=[common])
    pr.add_argument("--slab", required=True)
    pr.add_argument("--freeze_frac", type=float, default=0.5)

    ps = sub.add_parser("sites", parents=[common])
    ps.add_argument("--adatom", default="Li")
    ps.add_argument("--height", type=float, default=1.8)
    ps.add_argument("--grid", type=int, default=5)
    ps.add_argument("--cluster_tol", type=float, default=0.6,
                    help="xy distance (Å) to merge relaxed positions into one site")
    ps.add_argument("--hop_cutoff", type=float, default=4.0,
                    help="max site-site distance (Å) considered an adjacent hop")
    ps.add_argument("--mu_ref_ev", type=float, default=None,
                    help="reference Li chemical potential (eV/atom) for binding energy")

    pn = sub.add_parser("neb", parents=[common])
    pn.add_argument("--site_a", type=int, required=True)
    pn.add_argument("--site_b", type=int, required=True)
    pn.add_argument("--images", type=int, default=7)
    pn.add_argument("--spring_k", type=float, default=0.1)
    pn.add_argument("--steps1", type=int, default=20)
    pn.add_argument("--steps2", type=int, default=60)
    pn.add_argument("--optimizer", choices=["bfgs", "fire"], default="fire")
    pn.add_argument("--valley_tol", type=float, default=0.01,
                    help="interior dips more than this below endpoints → valley flag")
    pn.add_argument("--constrain_z", action="store_true",
                    help="pin adatom z (move only in xy) — prevents incorporation "
                         "dive, NEB still finds curved in-plane MEP")

    pd = sub.add_parser("drag", parents=[common])
    pd.add_argument("--site_a", type=int, required=True)
    pd.add_argument("--site_b", type=int, required=True)
    pd.add_argument("--adatom", default="Li")
    pd.add_argument("--n_points", type=int, default=9)
    pd.add_argument("--ad_z", type=float, default=None,
                    help="fixed adatom height (default: site_a adatom z)")
    pd.add_argument("--relax_z", action="store_true",
                    help="let adatom relax along z (xy still pinned); default rigid xyz")
    pd.add_argument("--dive_tol", type=float, default=1.0,
                    help="flag if adatom z drops more than this below z_ads")

    args = ap.parse_args()
    {"relax": stage_relax, "sites": stage_sites,
     "neb": stage_neb, "drag": stage_drag}[args.cmd](args)


if __name__ == "__main__":
    main()
