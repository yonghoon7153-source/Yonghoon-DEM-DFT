#!/usr/bin/env python
"""substitute_compound.py — Compound-set substitution for LPSCl doping.

Mirrors real synthesis routes where dopants enter the lattice as ionic
compounds (Nd2O3, Al2O3, MgO, ZnO, Li2O, …) rather than single elements.
The cation and anion of the precursor enter their respective sites in
stoichiometric ratio, so the compound is charge-neutral by construction.

Three modes (see kb / db/literature/lpscl_doping_precursor_compounds_review.md):

Type A — Compound set substitution (Nd2O3, MgO, …):
  - cation(s) → ``--cation_site`` (default Li_24g)
  - anion(s) → ``--anion_site``   (default S_16e — PS4 → P-anion preferred,
    matches ACS AMI 2021 oxysulfide O-on-S_16e finding)
  - Net cation aliovalency at the Li site is compensated by additional Li
    vacancies (the compound itself is neutral, but cation Δq at the host
    site is positive for divalent+/trivalent dopants and demands vacancies).

Type B — Halide-rich (anion-only swap with auto Li vacancy):
  - S²⁻ → halide⁻ on the chosen S-site, one Li vacancy per swap.
    Reproduces the Li6−xPS5−xCl1+x / Li5.4PS4.4Cl1.6 family (Adeli 2019,
    Kraft 2017).

Type C — Aliovalent cation + halide co-doping:
  - Implementable as TWO sequential Type-A / Type-B calls; this script
    handles them via the ``--also_halide_rich`` flag.

Usage:
  # Type A — Nd2O3 5 mol% (Nd→Li_24g, O→S_16e)
  python3 substitute_compound.py \\
      --base db/structures/lpscl_F43m_24G_canonical.cif \\
      --compound Nd2O3 --x_compound 0.05 \\
      --cation_site Li_24g --anion_site S_16e \\
      --out runs/doping_compound/nd2o3_005/

  # Type B — Li5.4PS4.4Cl1.6 (halide-rich, x=0.6)
  python3 substitute_compound.py \\
      --base ... --halide_rich Cl --excess_per_fu 0.6 \\
      --anion_site S_4a --out runs/doping_compound/lpscl16/

  # Type C — Al-Cl co-doping (Li5.4Al0.1PS4.7Cl1.3)
  python3 substitute_compound.py \\
      --base ... --compound Al2O3 --x_compound 0.025 \\
      --also_halide_rich Cl --excess_per_fu 0.3 \\
      --out runs/doping_compound/al_cl/
"""
import argparse
import json
import re
from pathlib import Path
import numpy as np
from ase.io import read, write
from ase import Atoms

import sys
sys.path.insert(0, str(Path(__file__).parent))
from site_preference import DOPANT_DB, HOST_SITES
from substitute_struct import (
    find_host_indices, find_host_indices_for_site,
    select_substitution_sites, SITE_TO_HOST,
)


def parse_compound(formula: str) -> dict[str, int]:
    """Parse 'Nd2O3' → {'Nd': 2, 'O': 3}.

    Supports single capital + optional lowercase + optional integer.
    Numeric subscripts only; no parentheses or hydrate notation.
    """
    matches = re.findall(r'([A-Z][a-z]?)(\d*)', formula)
    parsed: dict[str, int] = {}
    for el, count in matches:
        if not el:
            continue
        parsed[el] = parsed.get(el, 0) + (int(count) if count else 1)
    if not parsed:
        raise ValueError(f"Could not parse compound formula: {formula!r}")
    return parsed


def classify_compound(composition: dict[str, int], db: dict
                      ) -> tuple[dict[str, int], dict[str, int], int]:
    """Split compound into (cations, anions, net charge)."""
    missing = [el for el in composition if el not in db]
    if missing:
        raise ValueError(f"Elements {missing} not in DOPANT_DB. Add them first.")
    cations = {el: n for el, n in composition.items() if db[el]['charge'] > 0}
    anions  = {el: n for el, n in composition.items() if db[el]['charge'] < 0}
    net_q = sum(db[el]['charge'] * n for el, n in composition.items())
    return cations, anions, net_q


def compute_substitution_count(n_units: int, multiplicity: int) -> int:
    """Atoms of one element introduced when ``n_units`` formula units of the
    compound enter the cell."""
    return n_units * multiplicity


def li_vacancies_needed(atoms: Atoms, cations: dict[str, int],
                       cation_site: str, n_units: int, db: dict) -> int:
    """How many Li atoms must be removed to keep the cell neutral.

    Each cation at the cation_site introduces ``(q_cation - q_host)`` extra
    positive charge per atom. Total positive surplus → that many Li vacancies.
    Anion replacement on an anion site of equal charge (e.g., O²⁻ → S²⁻) adds
    no charge; an aliovalent anion (e.g., Cl⁻ → S²⁻) adds its own correction
    handled separately under halide-rich mode.
    """
    host_q = HOST_SITES[cation_site]['charge']
    n_vac = 0
    for cat, mult in cations.items():
        dq_per_atom = db[cat]['charge'] - host_q
        n_atoms = compute_substitution_count(n_units, mult)
        n_vac += dq_per_atom * n_atoms
    return max(n_vac, 0)  # only remove Li if net positive surplus


def substitute_compound_at_sites(atoms: Atoms, composition: dict[str, int],
                                 n_units: int, cation_site: str, anion_site: str,
                                 method: str, seed: int, db: dict
                                 ) -> tuple[Atoms, dict]:
    """Place all atoms of one compound unit-cluster into target sites."""
    new = atoms.copy()
    cations, anions, net_q = classify_compound(composition, db)
    if net_q != 0:
        raise ValueError(
            f"Compound {composition} is not charge-neutral (Σq={net_q:+d}). "
            "Use --halide_rich or split into separate Type A + B steps.")

    placement_log = {'cation_site': cation_site, 'anion_site': anion_site,
                     'placements': []}

    # 1. Substitute cations
    seed_local = seed
    for cat, mult in cations.items():
        n_sub = compute_substitution_count(n_units, mult)
        host_idx = find_host_indices_for_site(new, cation_site)
        if n_sub > len(host_idx):
            raise ValueError(
                f"Need {n_sub} {cat} at {cation_site}, but only "
                f"{len(host_idx)} sites available")
        targets = select_substitution_sites(host_idx, n_sub, method, seed_local)
        syms = new.get_chemical_symbols()
        for i in targets:
            syms[i] = cat
        new.set_chemical_symbols(syms)
        placement_log['placements'].append(
            {'element': cat, 'site': cation_site, 'n': n_sub,
             'targets': targets})
        seed_local += 1

    # 2. Substitute anions
    for an, mult in anions.items():
        n_sub = compute_substitution_count(n_units, mult)
        host_idx = find_host_indices_for_site(new, anion_site)
        if n_sub > len(host_idx):
            raise ValueError(
                f"Need {n_sub} {an} at {anion_site}, but only "
                f"{len(host_idx)} sites available")
        targets = select_substitution_sites(host_idx, n_sub, method, seed_local)
        syms = new.get_chemical_symbols()
        for i in targets:
            syms[i] = an
        new.set_chemical_symbols(syms)
        placement_log['placements'].append(
            {'element': an, 'site': anion_site, 'n': n_sub,
             'targets': targets})
        seed_local += 1

    # 3. Li vacancies for cation aliovalency
    n_vac = li_vacancies_needed(new, cations, cation_site, n_units, db)
    if n_vac > 0:
        li_idx = find_host_indices(new, 'Li')
        if n_vac >= len(li_idx):
            raise ValueError(
                f"Need {n_vac} Li vacancies but only {len(li_idx)} Li remain")
        vac_targets = select_substitution_sites(
            li_idx, n_vac, method, seed_local + 100)
        keep = [i for i in range(len(new)) if i not in vac_targets]
        new = new[keep]
        placement_log['li_vacancies'] = {'n': n_vac, 'indices': vac_targets}
    else:
        placement_log['li_vacancies'] = {'n': 0, 'indices': []}

    return new, placement_log


def halide_rich_swap(atoms: Atoms, halide: str, n_swap: int,
                    anion_site: str, method: str, seed: int) -> tuple[Atoms, dict]:
    """Type B — replace ``n_swap`` S atoms at ``anion_site`` with ``halide``,
    and remove the same number of Li atoms.

    Reproduces the Li6−xPS5−xCl1+x family stoichiometry. Charge balance is
    automatic: each S→Cl swap drops the local charge by +1, each Li vacancy
    drops it by −1; the two cancel.
    """
    new = atoms.copy()
    host_idx = find_host_indices_for_site(new, anion_site)
    if n_swap > len(host_idx):
        raise ValueError(
            f"Need {n_swap} S→{halide} swaps at {anion_site}, but only "
            f"{len(host_idx)} sites available")
    targets = select_substitution_sites(host_idx, n_swap, method, seed)
    syms = new.get_chemical_symbols()
    for i in targets:
        syms[i] = halide
    new.set_chemical_symbols(syms)

    li_idx = find_host_indices(new, 'Li')
    if n_swap >= len(li_idx):
        raise ValueError(
            f"Need {n_swap} Li vacancies but only {len(li_idx)} Li remain")
    vac_targets = select_substitution_sites(
        li_idx, n_swap, method, seed + 1)
    keep = [i for i in range(len(new)) if i not in vac_targets]
    new = new[keep]

    return new, {
        'halide_rich': halide,
        'n_swap': n_swap,
        'swap_targets': targets,
        'li_vacancies': vac_targets,
    }


def composition_summary(atoms: Atoms) -> dict[str, int]:
    syms = atoms.get_chemical_symbols()
    return {el: int(c) for el, c in
            zip(*np.unique(syms, return_counts=True))}


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--base', required=True, help='LPSCl base structure')
    parser.add_argument('--out', required=True, help='Output directory')

    # Type A
    parser.add_argument('--compound',
                       help="Compound formula, e.g., 'Nd2O3', 'MgO', 'Al2O3'")
    parser.add_argument('--x_compound', type=float, default=0.05,
                       help='Mole fraction of compound per f.u. (default 0.05)')
    parser.add_argument('--cation_site', default='Li_24g',
                       help='Target site for cations (default Li_24g)')
    parser.add_argument('--anion_site', default='S_16e',
                       help='Target site for anions (default S_16e; ACS AMI 2021 '
                            'shows O prefers S_16e — PS4 → PO4 formation)')

    # Type B
    parser.add_argument('--halide_rich',
                       help="Halide element for Li6-xPS5-xX1+x family, e.g. 'Cl'")
    parser.add_argument('--excess_per_fu', type=float,
                       help='Halide excess x per f.u. (e.g., 0.6 for Li5.4PS4.4Cl1.6)')

    # Type C (chain Type A + Type B)
    parser.add_argument('--also_halide_rich',
                       help='After Type A, additionally do halide-rich swap')

    # Common
    parser.add_argument('--n_fu', type=int, default=4,
                       help='Number of formula units in the base cell (default 4)')
    parser.add_argument('--method', default='spread',
                       choices=['spread', 'random', 'first'])
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--n_seeds', type=int, default=1,
                       help='Ensemble size (only meaningful with --method random)')
    args = parser.parse_args()

    if not args.compound and not args.halide_rich:
        parser.error("Provide --compound (Type A) and/or --halide_rich (Type B)")

    base = read(args.base)
    print(f"Loaded base: {len(base)} atoms, composition: {composition_summary(base)}")
    print(f"Assuming {args.n_fu} f.u. per cell (4 × Li6PS5Cl by default).")

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    seeds = ([args.seed] if args.method != 'random'
             else [args.seed + i for i in range(args.n_seeds)])

    generated: list[dict] = []
    for seed in seeds:
        doped = base.copy()
        info: dict = {'seed': seed, 'steps': []}

        # --- Type A ---
        if args.compound:
            composition = parse_compound(args.compound)
            n_units = max(1, int(round(args.n_fu * args.x_compound)))
            actual_x = n_units / args.n_fu
            doped, log = substitute_compound_at_sites(
                doped, composition, n_units,
                args.cation_site, args.anion_site,
                args.method, seed, DOPANT_DB)
            info['steps'].append({
                'type': 'A_compound',
                'compound': args.compound,
                'composition': composition,
                'n_units': n_units,
                'actual_x': actual_x,
                **log,
            })

        # --- Type B ---
        if args.halide_rich:
            if args.excess_per_fu is None:
                parser.error("--halide_rich requires --excess_per_fu")
            n_swap = max(1, int(round(args.n_fu * args.excess_per_fu)))
            doped, log = halide_rich_swap(
                doped, args.halide_rich, n_swap,
                args.anion_site if args.anion_site.startswith('S') else 'S_4a',
                args.method, seed + 50)
            info['steps'].append({
                'type': 'B_halide_rich',
                'halide': args.halide_rich,
                'n_swap': n_swap,
                'actual_excess': n_swap / args.n_fu,
                **log,
            })
        elif args.also_halide_rich:
            if args.excess_per_fu is None:
                parser.error("--also_halide_rich requires --excess_per_fu")
            n_swap = max(1, int(round(args.n_fu * args.excess_per_fu)))
            doped, log = halide_rich_swap(
                doped, args.also_halide_rich, n_swap,
                'S_4a', args.method, seed + 70)
            info['steps'].append({
                'type': 'C_chain_halide_rich',
                'halide': args.also_halide_rich,
                'n_swap': n_swap,
                **log,
            })

        # Name + write
        parts = []
        if args.compound:
            parts.append(f"{args.compound}_x{int(args.x_compound*1000):03d}")
        if args.halide_rich:
            parts.append(f"{args.halide_rich}rich_x{int(args.excess_per_fu*1000):03d}")
        if args.also_halide_rich:
            parts.append(f"chain_{args.also_halide_rich}_x{int(args.excess_per_fu*1000):03d}")
        if args.method == 'random':
            parts.append(f"s{seed - args.seed:02d}")
        name = "_".join(parts) if parts else "doped"
        xyz_path = out_dir / f'{name}.xyz'
        write(xyz_path, doped)

        info.update({
            'name': name,
            'n_atoms': len(doped),
            'composition': composition_summary(doped),
            'xyz_file': str(xyz_path),
        })
        generated.append(info)
        print(f"  ✓ {name}: {len(doped)} atoms, {composition_summary(doped)}")

    summary = {
        'base_file': args.base,
        'n_fu': args.n_fu,
        'method': args.method,
        'n_seeds': args.n_seeds,
        'structures': generated,
    }
    summary_path = out_dir / 'compound_summary.json'
    summary_path.write_text(json.dumps(summary, indent=2, default=str))
    print(f"\n✓ Generated {len(generated)} structures")
    print(f"✓ Summary: {summary_path}")


if __name__ == '__main__':
    main()
