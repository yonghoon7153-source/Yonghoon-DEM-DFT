#!/usr/bin/env python3
"""B2O3 — O-distribution resolver: full tetrahedral-corner enumeration + unit analysis.

The coarse bo4/distributed/free_s motifs (b2o3_uma_relax.py) showed bo4 vs distributed
are near-degenerate (~1-3 meV/atom) -> O does NOT form one clean unit; it distributes
among tetrahedral corners as a MIX of BS4 / BO_xS_4-x / PS_4-y O_y units (free-S 4a is
strongly avoided, ~1.3 eV/O). This resolves the actual distribution.

Method (on a fixed best (B,halogen,Li) config):
  1. corner S = S bonded to P or B (the 40 PS4/BS4 tetrahedral corners)
  2. enumerate ALL C(n_corner, n_O) O placements   (cap via --max_enum random subsample)
  3. UMA single-point screen -> rank
  4. UMA relax top --relax_top
  5. classify each relaxed structure into local units (B/P center, #O corners)
     -> ensemble + ground-state unit distribution (the NMR/XPS-testable prediction)

Deps: fairchem.core (UMA), ase, numpy.
Usage:
  python3 b2o3_o_distribution.py \
      --base_cif b2o3_stage0/cif/cfg0019_E-2265.418.cif \  # a NO-O (B/halogen/Li) config
      --n_O 3 --max_enum 9880 --relax_top 50 \
      --out b2o3_Odist --device cuda
"""
import argparse, json, itertools
from pathlib import Path
from collections import Counter
import numpy as np
from ase.io import read, write
from ase.neighborlist import neighbor_list
from ase.optimize import FIRE
from ase.filters import FrechetCellFilter


def make_calc(model, task, device):
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    return FAIRChemCalculator(pretrained_mlip.get_predict_unit(model, device=device),
                              task_name=task)


def corner_S(atoms):
    """S bonded to P or B (tetrahedral corners). Returns list of S indices."""
    s = atoms.get_chemical_symbols()
    out = set()
    for cen in ("P", "B"):
        ii, jj = neighbor_list("ij", atoms, {(cen, "S"): 2.5})
        for a, b in zip(ii, jj):
            if s[a] == "S": out.add(a)
            if s[b] == "S": out.add(b)
    return sorted(out)


def classify_units(atoms):
    """For each P/B center, count O among its 4 nearest chalcogen corners -> unit label."""
    s = atoms.get_chemical_symbols()
    D = atoms.get_all_distances(mic=True)
    chal = [i for i in range(len(atoms)) if s[i] in ("S", "O")]
    units = Counter()
    for c in range(len(atoms)):
        if s[c] not in ("P", "B"):
            continue
        near = sorted(chal, key=lambda j: D[c][j])[:4]
        nO = sum(1 for j in near if s[j] == "O")
        units[f"{s[c]}O{nO}S{4 - nO}"] += 1
    return dict(units)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base_cif", required=True, help="a NO-O (B/halogen/Li) config")
    ap.add_argument("--n_O", type=int, default=3)
    ap.add_argument("--max_enum", type=int, default=9880,
                    help="if C(corners,n_O) exceeds this, random-subsample to this many")
    ap.add_argument("--relax_top", type=int, default=50)
    ap.add_argument("--model", default="uma-s-1p1")
    ap.add_argument("--task", default="omat")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--fmax", type=float, default=0.05)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default="b2o3_Odist")
    A = ap.parse_args()
    rng = np.random.default_rng(A.seed)
    out = Path(A.out); (out / "relaxed").mkdir(parents=True, exist_ok=True)

    base = read(A.base_cif)
    corners = corner_S(base)
    print(f"base {A.base_cif}: {len(base)} atoms, {len(corners)} tetrahedral corner-S")

    combos = list(itertools.combinations(corners, A.n_O))
    print(f"C({len(corners)},{A.n_O}) = {len(combos)} O placements")
    if len(combos) > A.max_enum:
        idx = rng.choice(len(combos), A.max_enum, replace=False)
        combos = [combos[i] for i in idx]
        print(f"  subsampled to {len(combos)}")

    calc = make_calc(A.model, A.task, A.device)

    # --- UMA single-point screen ---
    print("single-point screen ...", flush=True)
    sp = []
    for k, osel in enumerate(combos):
        a = base.copy()
        syms = list(a.get_chemical_symbols())
        for o in osel:
            syms[o] = "O"
        a.set_chemical_symbols(syms)
        a.calc = calc
        E = a.get_potential_energy()
        sp.append((osel, float(E)))
        if k % 1000 == 0:
            print(f"  SP {k}/{len(combos)}", flush=True)
    sp.sort(key=lambda t: t[1])
    json.dump([{"O_sites": list(o), "E_sp": round(e, 4)} for o, e in sp[:200]],
              open(out / "sp_screen_top200.json", "w"), indent=1)

    # --- relax top ---
    print(f"relaxing top {A.relax_top} ...", flush=True)
    rows = []
    for rank, (osel, Esp) in enumerate(sp[:A.relax_top]):
        a = base.copy()
        syms = list(a.get_chemical_symbols())
        for o in osel:
            syms[o] = "O"
        a.set_chemical_symbols(syms)
        a.calc = calc
        try:
            FIRE(FrechetCellFilter(a), logfile=str(out / "fire.log")).run(fmax=A.fmax, steps=300)
            E = a.get_potential_energy()
        except Exception as e:
            print(f"  relax {rank} FAIL {e}"); continue
        units = classify_units(a)
        write(out / "relaxed" / f"o{rank:03d}.cif", a)
        rows.append(dict(rank=rank, E=round(float(E), 4),
                         E_per_atom=round(float(E) / len(a), 5),
                         O_sites=list(osel), units=units))
        if rank % 10 == 0:
            print(f"  relax {rank}: E/atom={rows[-1]['E_per_atom']} units={units}", flush=True)

    rows.sort(key=lambda r: r["E_per_atom"])
    json.dump(rows, open(out / "Odist_relaxed_ranked.json", "w"), indent=1)

    # --- unit distribution summary ---
    gs = rows[0] if rows else None
    # Boltzmann-ish ensemble over relaxed (300K) for unit populations
    kT = 0.02585
    Es = np.array([r["E"] for r in rows])
    w = np.exp(-(Es - Es.min()) / kT); w /= w.sum()
    ens = Counter()
    for r, wi in zip(rows, w):
        for u, n in r["units"].items():
            ens[u] += wi * n
    print("\n==== O-DISTRIBUTION (local-unit) ====")
    if gs:
        print(f"  ground state: E/atom={gs['E_per_atom']}  units={gs['units']}")
    print(f"  300K-weighted ensemble unit populations (per cell):")
    for u, n in sorted(ens.items(), key=lambda kv: -kv[1]):
        print(f"    {u:8s} {n:.2f}")
    json.dump(dict(ground_state_units=gs["units"] if gs else {},
                   ensemble_300K_units={u: round(float(n), 3) for u, n in ens.items()}),
              open(out / "Odist_unit_summary.json", "w"), indent=1)
    print(f"\n  -> {out}/Odist_unit_summary.json  (NMR/XPS-testable unit prediction)")
    print(f"  -> {out}/relaxed/ (top {len(rows)}); next: DFT-confirm a few")


if __name__ == "__main__":
    main()
