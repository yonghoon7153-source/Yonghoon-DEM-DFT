#!/usr/bin/env python3
"""enumerate_anion.py — Stage-0 Step 1: anion (S2- / halogen) site enumeration.

The undoped-side counterpart to b2o3_enumerate.py (which does B2O3 doping pre-rank).
Pure HALOGEN site disorder with the Li sublattice FIXED: identify the free-anion
sites (free S = S not bonded to P, + all halogen Cl/Br/I), then enumerate which of
those sites carry halogen vs S2- (C(n_sites, n_halogen)), writing UMA-ready CIFs +
a manifest for the Step-2 UMA screen. numpy + ase only (no pymatgen/enumlib) so it
is testable anywhere ase runs.

Pipeline ref: kb/methodology/argyrodite_mechanical_pipeline.md Step 1.

  python3 tools/doping/enumerate_anion.py --struct db/structures/lpscl_bulk.cif \
      --out anion_enum --max_configs 70

If C(n,k) <= max_configs -> full enumeration; else random-sample max_configs unique.
"""
import argparse, itertools, hashlib, json
from math import comb
from pathlib import Path
import numpy as np
from ase.io import read, write
from ase.neighborlist import neighbor_list

HALOGENS = ("Cl", "Br", "I")


def identify_anion_sites(atoms, p_s_cut=2.6):
    """free-S sites (S with NO P neighbour < p_s_cut) + all halogen sites.
    These are the argyrodite 'free anion' (4a/4d-type) sublattice; PS4 sulfurs
    (S bonded to P) are excluded (they are the rigid thiophosphate, not disordered)."""
    syms = np.array(atoms.get_chemical_symbols())
    P = set(np.where(syms == "P")[0].tolist())
    S = np.where(syms == "S")[0].tolist()
    hal = np.where(np.isin(syms, HALOGENS))[0].tolist()
    s_with_p = set()
    if P and S:
        i, j, _ = neighbor_list("ijd", atoms, p_s_cut)
        for a, b in zip(i, j):
            if syms[a] == "S" and b in P:
                s_with_p.add(int(a))
    free_S = [s for s in S if s not in s_with_p]
    hal_sym = syms[hal[0]] if hal else "Cl"
    return sorted(free_S + hal), len(hal), str(hal_sym)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--struct", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--max_configs", type=int, default=70)
    ap.add_argument("--p_s_cut", type=float, default=2.6)
    ap.add_argument("--seed", type=int, default=0)
    A = ap.parse_args()

    atoms = read(A.struct)
    sites, k, hal_sym = identify_anion_sites(atoms, A.p_s_cut)
    n = len(sites)
    if n == 0 or k == 0:
        raise SystemExit(f"no anion disorder sites found (n={n}, halogen={k}); check structure / p_s_cut")
    total = comb(n, k)
    print(f"[enumerate_anion] {len(atoms)} atoms | anion sites n={n} "
          f"(free-S {n-k} + halogen {k}) | halogen={hal_sym} | C(n,k)={total}")

    if total <= A.max_configs:
        combos = list(itertools.combinations(range(n), k))
    else:
        rng = np.random.default_rng(A.seed)
        seen, combos = set(), []
        while len(combos) < A.max_configs:
            c = tuple(sorted(int(x) for x in rng.choice(n, k, replace=False)))
            if c not in seen:
                seen.add(c); combos.append(c)
        print(f"  C(n,k)={total} > {A.max_configs} -> random-sampled {A.max_configs} unique configs")

    out = Path(A.out); out.mkdir(parents=True, exist_ok=True)
    manifest = []
    for idx, combo in enumerate(combos):
        a = atoms.copy()
        syms = list(a.get_chemical_symbols())
        hal_pos = {sites[i] for i in combo}
        for s in sites:
            syms[s] = hal_sym if s in hal_pos else "S"
        a.set_chemical_symbols(syms)
        key = hashlib.md5(str(sorted(combo)).encode()).hexdigest()[:8]
        fname = f"anion_{idx:04d}_{key}.cif"
        write(str(out / fname), a)
        manifest.append({"id": idx, "halogen_sites": [int(sites[i]) for i in combo], "file": fname})

    (out / "manifest.json").write_text(json.dumps({
        "struct": A.struct, "n_anion_sites": n, "n_halogen": k, "halogen": hal_sym,
        "total_combinations": total, "emitted": len(combos),
        "note": "Li sublattice fixed; only free-S<->halogen identities permuted. "
                "Next: Step 2 UMA screen (relax + energy rank), then Step 3 anneal (b2o3_anneal.py).",
        "configs": manifest}, indent=2))
    print(f"-> {out}/ ({len(combos)} CIFs + manifest.json)  | next: UMA screen -> b2o3_anneal.py")


if __name__ == "__main__":
    main()
