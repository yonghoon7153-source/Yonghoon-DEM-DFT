#!/usr/bin/env python3
"""Build an approximate CUBIC LPSCl1.6 supercell from a comp1 LPSCl base.

Strategy (BVSE-visualization only — NOT a DFT-ready structure):
  1. Take LPSCl conventional cubic V0 (4 fu, 52 atoms) — already cubic.
  2. Tile 2×2×2 → 32 fu, 416 atoms (a ≈ 20.1 Å).
  3. Random S→Cl substitution at 4d sites (the non-PS4 S²⁻ positions):
       fu × 0.6 = 19.2 ≈ 19 substitutions
  4. Random Li removal: same count to keep charge balance (since
     replacing S²⁻ → Cl⁻ liberates one Li⁺ per substitution).
  5. Final stoichiometry ≈ Li5.41 P S4.41 Cl1.59 (0.4 % off ideal 5.4/4.4/1.6).

Output: CIF + .xyz + a tiny report JSON.

Seeded RNG so the structure is reproducible.

Usage:
    python3 build_lpscl16_approx_cubic.py \\
        --src_cif comp1/V0_init.cif \\
        --out_dir /tmp/lpscl16_cubic_approx \\
        --tile 2 --seed 42
"""
import argparse, json, random
from pathlib import Path
import numpy as np
from ase import Atoms
from ase.io import read, write


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src_cif", required=True,
                    help="comp1 V0_init.cif (LPSCl cubic, 4 fu)")
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--tile", type=int, default=2,
                    help="supercell repeat (default 2 → 2×2×2 = 32 fu)")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--li_per_fu_target", type=float, default=5.4)
    ap.add_argument("--cl_per_fu_target", type=float, default=1.6)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    np.random.seed(args.seed)

    out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)

    base = read(args.src_cif)
    sym0 = base.get_chemical_symbols()
    n0 = len(base)
    # Confirm 4 fu LPSCl base
    counts0 = {s: sym0.count(s) for s in set(sym0)}
    if counts0 != {"Li": 24, "P": 4, "S": 20, "Cl": 4}:
        print(f"[WARN] base composition is {counts0}, expected 4-fu LPSCl "
              "(Li24 P4 S20 Cl4). Continuing anyway.")

    super_cell = base.repeat((args.tile, args.tile, args.tile))
    n_super = len(super_cell)
    n_fu = (args.tile ** 3) * 4   # 4 fu per tile
    sym = super_cell.get_chemical_symbols()
    counts = {s: sym.count(s) for s in set(sym)}
    print(f"[base] {counts0}, V={base.get_volume():.3f} Å³, "
          f"a={np.linalg.norm(base.get_cell()[0]):.3f} Å")
    print(f"[super] tile={args.tile}^3 = {n_fu} fu = {n_super} atoms")
    print(f"        composition pre-substitution: {counts}")

    # Identify 4d S²⁻ vs PS4 S — 4d S has no P within 2.5 Å
    p_idx = [i for i, s in enumerate(sym) if s == "P"]
    s_idx = [i for i, s in enumerate(sym) if s == "S"]
    pos = super_cell.get_positions()
    cell = np.array(super_cell.get_cell())
    inv_cell = np.linalg.inv(cell)

    def min_image_dist(p1, p2):
        d = p2 - p1
        df = d @ inv_cell
        df -= np.round(df)
        return np.linalg.norm(df @ cell)

    s_4d, s_ps4 = [], []
    for si in s_idx:
        has_p = any(min_image_dist(pos[si], pos[pi]) < 2.5 for pi in p_idx)
        (s_ps4 if has_p else s_4d).append(si)
    print(f"        S(PS4)={len(s_ps4)}, S(4d)={len(s_4d)}")

    # === Substitutions ===
    target_cl_total = round(n_fu * args.cl_per_fu_target)
    cl_pre = sym.count("Cl")
    n_sub = target_cl_total - cl_pre
    print(f"[target] Cl total per cell = {target_cl_total}  → need "
          f"{n_sub} S→Cl substitutions")

    target_li_total = round(n_fu * args.li_per_fu_target)
    li_pre = sym.count("Li")
    n_li_remove = li_pre - target_li_total
    print(f"[target] Li total per cell = {target_li_total}  → need "
          f"{n_li_remove} Li removals")

    if n_sub > len(s_4d):
        print(f"[WARN] need {n_sub} subs but only {len(s_4d)} 4d S "
              "available. Allowing PS4 S as well — rare in real "
              "structures but ok for BVSE viz.")
        pool = s_4d + s_ps4
    else:
        pool = s_4d[:]

    sub_indices = sorted(rng.sample(pool, n_sub))
    print(f"        substituting indices: {sub_indices}")

    new_atoms = []
    new_pos = []
    li_pool = [i for i, s in enumerate(sym) if s == "Li"]
    removed_li = set(rng.sample(li_pool, n_li_remove))
    print(f"        removed Li (indices): {sorted(removed_li)}")

    for i, s in enumerate(sym):
        if i in removed_li:
            continue
        if i in sub_indices:
            new_atoms.append("Cl")
        else:
            new_atoms.append(s)
        new_pos.append(pos[i])

    out_atoms = Atoms(symbols=new_atoms, positions=new_pos,
                       cell=cell, pbc=True)

    counts_new = {s: new_atoms.count(s) for s in set(new_atoms)}
    li_per_fu = counts_new.get("Li", 0) / n_fu
    cl_per_fu = counts_new.get("Cl", 0) / n_fu
    s_per_fu  = counts_new.get("S", 0) / n_fu
    print(f"[final] {counts_new}, total = {len(out_atoms)} atoms")
    print(f"        composition Li{li_per_fu:.3f}PS{s_per_fu:.3f}"
          f"Cl{cl_per_fu:.3f}  (target Li5.4 S4.4 Cl1.6)")

    write(out / "V0_init.cif", out_atoms)
    write(out / "V0_init.xyz", out_atoms)

    report = {
        "source": args.src_cif,
        "tile": args.tile,
        "seed": args.seed,
        "n_fu": n_fu,
        "n_atoms_pre": n_super,
        "n_atoms_final": len(out_atoms),
        "composition": counts_new,
        "li_per_fu": li_per_fu,
        "s_per_fu":  s_per_fu,
        "cl_per_fu": cl_per_fu,
        "n_S_to_Cl_substitutions": n_sub,
        "n_Li_removed": n_li_remove,
        "s_4d_pool_size": len(s_4d),
        "s_ps4_pool_size": len(s_ps4),
        "substituted_indices": sub_indices,
        "removed_li_indices": sorted(removed_li),
        "cell_a_A": float(np.linalg.norm(cell[0])),
        "volume_A3": float(out_atoms.get_volume()),
        "_warning": ("Approximate cubic LPSCl1.6 for BVSE visualization "
                     "only. NOT DFT-relaxed. Real Li/Cl ordering will "
                     "differ from this random placement."),
    }
    (out / "build_report.json").write_text(json.dumps(report, indent=2))
    print(f"\n→ {out}/V0_init.cif")
    print(f"→ {out}/V0_init.xyz")
    print(f"→ {out}/build_report.json")


if __name__ == "__main__":
    main()
