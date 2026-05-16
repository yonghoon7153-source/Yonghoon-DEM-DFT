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
from site_preference import DOPANT_DB, HOST_SITES, site_preference_filter
from substitute_struct import (
    find_host_indices, find_host_indices_for_site,
    select_substitution_sites, SITE_TO_HOST,
)


def compatible_sites_for_element(element: str, db: dict) -> set[str]:
    """Return the set of HOST_SITES names where ``element`` can sit,
    according to the literature-calibrated radius+charge filter in
    site_preference.py. Skipping incompatible (cation_site, anion_site)
    combinations saves UMA cost and avoids reporting non-physical
    placements (e.g., La³⁺ at S_4a, or O²⁻ at P_4b).
    """
    if element not in db:
        return set()
    info = db[element]
    matches = site_preference_filter(info['charge'], info['radius'])
    return {m['site_name'] for m in matches}


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


# Common alternative oxidation states per element — used by auto-valence
# inference when the default charge gives a non-neutral compound (e.g.,
# MnO2, CrO3, Fe3O4). Searched in order; first valence giving net_q==0 wins.
ALTERNATIVE_VALENCES = {
    'Cr': [+3, +6, +4, +2],     # Cr2O3 default; CrO3 needs +6; CrO2 needs +4
    'Mn': [+2, +4, +7, +3, +6], # MnO default; MnO2 +4; KMnO4 +7
    'Fe': [+3, +2],              # Fe2O3 default; FeO needs +2
    'Co': [+2, +3, +4],          # CoO default; Co2O3 +3; Co3O4 mixed
    'Ni': [+2, +3, +4],
    'Cu': [+1, +2],              # Cu2O default; CuO +2
    'V':  [+5, +4, +3, +2],      # V2O5 default; VO2 +4
    'Mo': [+6, +4, +5, +3],
    'W':  [+6, +4, +5],
    'Re': [+7, +6, +4],
    'Ti': [+4, +3],
    'Sn': [+4, +2],              # SnO2 default; SnO +2
    'Pb': [+4, +2],
    'Sb': [+5, +3],              # Sb2O5 default; Sb2O3 +3
    'Bi': [+3, +5],
    'Ce': [+4, +3],              # CeO2 default; Ce2O3 +3
    'Eu': [+3, +2],
    'U':  [+6, +5, +4, +3],
    'P':  [+5, +3],
}


def auto_balance_compound(composition: dict[str, int],
                         db: dict) -> tuple[dict, dict]:
    """If compound is non-neutral with default DB charges, search for a single
    cation whose valence can be substituted from ALTERNATIVE_VALENCES to
    achieve neutrality. Returns (modified_db_subset, info).

    Example: MnO2 = {Mn:1, O:2}. Default Mn=+2 gives net=-2.
    Try Mn=+4 → 1×4 + 2×(-2) = 0 ✓. Returns DB-overlay {Mn:+4}.
    """
    cations, anions, net_q = classify_compound(composition, db)
    if net_q == 0:
        return {}, {'status': 'already_neutral', 'net_q': 0}
    if len(cations) != 1:
        # Multi-cation: more complex; just report imbalance for now
        return {}, {'status': 'multi_cation_imbalance', 'net_q': net_q}
    # Try alternative valences for the single cation
    cat, n_cat = next(iter(cations.items()))
    if cat not in ALTERNATIVE_VALENCES:
        return {}, {'status': 'no_alt_valences_known',
                   'cation': cat, 'net_q': net_q}
    anion_q = sum(db[a]['charge'] * n for a, n in anions.items())
    for v in ALTERNATIVE_VALENCES[cat]:
        if v * n_cat + anion_q == 0:
            return {cat: {**db[cat], 'charge': v}}, {
                'status': 'auto_valence',
                'cation': cat,
                'old_charge': db[cat]['charge'],
                'new_charge': v,
            }
    return {}, {'status': 'no_neutral_valence_found',
               'cation': cat, 'tried': ALTERNATIVE_VALENCES[cat],
               'net_q': net_q}


def compute_substitution_count(n_units: int, multiplicity: int) -> int:
    """Atoms of one element introduced when ``n_units`` formula units of the
    compound enter the cell."""
    return n_units * multiplicity


def li_vacancies_needed(atoms: Atoms, cations: dict[str, int],
                       cation_site: str, n_units: int, db: dict) -> int:
    """Compute charge surplus from cation placement; positive value = need
    that many Li vacancies; negative value = need Li interstitials (NOT
    modelled — acceptor cations like B³⁺ at P⁵⁺, Si⁴⁺ at P⁵⁺ leave the cell
    charge-unbalanced and will rank low under UMA's energy filter).

    Each cation at the cation_site introduces ``(q_cation - q_host)`` extra
    charge per atom. Sum across all compound cations gives net surplus.
    """
    host_q = HOST_SITES[cation_site]['charge']
    n_vac = 0
    for cat, mult in cations.items():
        dq_per_atom = db[cat]['charge'] - host_q
        n_atoms = compute_substitution_count(n_units, mult)
        n_vac += dq_per_atom * n_atoms
    return max(n_vac, 0)  # only remove Li if net positive surplus
    # NOTE: when n_vac < 0 (acceptor case, e.g., B/Si/Al at P site), the
    # cell ends up charge-imbalanced. UMA energy will reflect this through a
    # higher binding penalty. Future work: model Li interstitials or
    # reverse-halide-rich (Cl→S swap with extra Li) as compensation paths.


def substitute_compound_at_sites(atoms: Atoms, composition: dict[str, int],
                                 n_units: int, cation_site: str, anion_site: str,
                                 method: str, seed: int, db: dict,
                                 vacancy_method: str = 'random'
                                 ) -> tuple[Atoms, dict]:
    """Place all atoms of one compound unit-cluster into target sites.

    ``vacancy_method`` is decoupled from ``method`` and defaults to 'random'.
    Real LPSCl₁₊ₓ-style halide-rich phases have *disordered* Li vacancies
    (Kraft 2017 NMR / Adeli 2019 PDF) — using 'spread' for vacancies would
    create an artificial ordered Li-vacancy superlattice that does not match
    experiment. Subsitution sites for the dopant atoms themselves can still
    use 'spread' or 'cluster' to model precursor placement geometry.
    """
    new = atoms.copy()
    # Auto-valence inference (MnO2, CrO3, Fe3O4, …) before charge check.
    overlay, av_info = auto_balance_compound(composition, db)
    if overlay:
        db = {**db, **overlay}
    cations, anions, net_q = classify_compound(composition, db)
    if net_q != 0:
        raise ValueError(
            f"Compound {composition} is not charge-neutral (Σq={net_q:+d}, "
            f"auto-valence search status={av_info.get('status', 'n/a')}). "
            "Use --halide_rich, split into separate Type A + B steps, or "
            "add a custom valence to ALTERNATIVE_VALENCES.")

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
        targets = select_substitution_sites(host_idx, n_sub, method, seed_local, atoms=new)
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
        targets = select_substitution_sites(host_idx, n_sub, method, seed_local, atoms=new)
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
        # Reference for 'near_cation': aliovalent cation positions
        # (Mg, Al, Nd, etc. — the actually substituted atoms)
        ref_idx = [i for i, s in enumerate(new.get_chemical_symbols())
                  if s in cations]
        vac_targets = select_substitution_sites(
            li_idx, n_vac, vacancy_method, seed_local + 100, atoms=new,
            reference_indices=ref_idx)
        keep = [i for i in range(len(new)) if i not in vac_targets]
        new = new[keep]
        placement_log['li_vacancies'] = {'n': n_vac, 'indices': vac_targets}
    else:
        placement_log['li_vacancies'] = {'n': 0, 'indices': []}

    return new, placement_log


def mixed_halide_swap(atoms: Atoms, halide_excess: dict[str, float],
                     n_fu: int, anion_site: str, method: str, seed: int,
                     vacancy_method: str = 'random') -> tuple[Atoms, dict]:
    """Multi-halide halide-rich substitution (LPSClBr-style precursors).

    ``halide_excess`` = {'Cl': 0.3, 'Br': 0.3} → 0.3 + 0.3 = 0.6 total excess
    per f.u., giving Li5.4PS4.4Cl1.3Br0.3 (4 fu = 24 Li → 22.4 ≈ 22 Li after
    2 S→halide swaps + 2 Li vacancies; halides split 1 Cl + 1 Br for the 2
    swaps). Replicates comp2/3/4/5 chemistry (Cl₁₋ₓBrₓ argyrodite family).
    """
    new = atoms.copy()
    host_idx = find_host_indices_for_site(new, anion_site)
    n_swap_per_halide = {h: max(1, int(round(n_fu * x)))
                         for h, x in halide_excess.items()}
    total_swap = sum(n_swap_per_halide.values())
    if total_swap > len(host_idx):
        raise ValueError(
            f"Need {total_swap} S→halide swaps at {anion_site}, "
            f"but only {len(host_idx)} sites")

    # Pick total_swap S sites then partition by halide stoichiometry
    targets = select_substitution_sites(host_idx, total_swap, method, seed,
                                       atoms=new)
    syms = new.get_chemical_symbols()
    idx_iter = iter(targets)
    placements = {}
    for halide, n in n_swap_per_halide.items():
        these = [next(idx_iter) for _ in range(n)]
        for i in these:
            syms[i] = halide
        placements[halide] = these
    new.set_chemical_symbols(syms)

    li_idx = find_host_indices(new, 'Li')
    if total_swap >= len(li_idx):
        raise ValueError(
            f"Need {total_swap} Li vacancies but only {len(li_idx)} Li remain")
    vac_targets = select_substitution_sites(
        li_idx, total_swap, vacancy_method, seed + 1, atoms=new)
    keep = [i for i in range(len(new)) if i not in vac_targets]
    new = new[keep]

    return new, {
        'mixed_halides': halide_excess,
        'n_swap_per_halide': n_swap_per_halide,
        'swap_targets': placements,
        'li_vacancies': vac_targets,
    }


def halide_rich_swap(atoms: Atoms, halide: str, n_swap: int,
                    anion_site: str, method: str, seed: int,
                    vacancy_method: str = 'random') -> tuple[Atoms, dict]:
    """Type B — replace ``n_swap`` S atoms at ``anion_site`` with ``halide``,
    and remove the same number of Li atoms.

    Reproduces the Li6−xPS5−xCl1+x family stoichiometry. Charge balance is
    automatic: each S→Cl swap drops the local charge by +1, each Li vacancy
    drops it by −1; the two cancel.

    Li vacancies use ``vacancy_method='random'`` by default — Kraft 2017
    NMR / Adeli 2019 PDF show Li vacancies are positionally disordered, not
    ordered into a superlattice.
    """
    new = atoms.copy()
    host_idx = find_host_indices_for_site(new, anion_site)
    if n_swap > len(host_idx):
        raise ValueError(
            f"Need {n_swap} S→{halide} swaps at {anion_site}, but only "
            f"{len(host_idx)} sites available")
    targets = select_substitution_sites(host_idx, n_swap, method, seed, atoms=new)
    syms = new.get_chemical_symbols()
    for i in targets:
        syms[i] = halide
    new.set_chemical_symbols(syms)

    li_idx = find_host_indices(new, 'Li')
    if n_swap >= len(li_idx):
        raise ValueError(
            f"Need {n_swap} Li vacancies but only {len(li_idx)} Li remain")
    vac_targets = select_substitution_sites(
        li_idx, n_swap, vacancy_method, seed + 1, atoms=new)
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
    parser.add_argument('--supercell', nargs=3, type=int, default=[1, 1, 1],
                       metavar=('NX', 'NY', 'NZ'),
                       help='Multiply base cell (default 1 1 1 = 4 f.u. / 52 atoms; '
                            '2 1 1 = 8 f.u., 2 2 1 = 16 f.u., 2 2 2 = 32 f.u. — '
                            'needed when combining Type A + Type B doping at low '
                            'concentrations so a single integer atom does not '
                            'exceed the requested mole fraction).')
    parser.add_argument('--auto_anion_sites', action='store_true',
                       help='For Type A: generate one structure per available '
                            'anion site (S_16e, S_4a, Cl_4d) instead of using '
                            'a single --anion_site. Lets UMA energy decide '
                            'whether O prefers PS4→PO4 (S_16e), free O²⁻ (S_4a), '
                            'or oxychloride (Cl_4d).')
    parser.add_argument('--auto_cation_sites', action='store_true',
                       help='For Type A: also iterate cation sites '
                            '{Li_24g, Li_48h, P_4b}.')
    parser.add_argument('--allow_exotic', action='store_true',
                       help='Bypass the site_preference radius filter and let '
                            'UMA energy rank chemically unusual placements '
                            '(e.g., La at P_4b, B at Li_24g, O at P_4b). '
                            'Useful when --auto_*_sites would otherwise drop '
                            'a combination you want to explore manually.')

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
    parser.add_argument('--mixed_halides',
                       help="Multi-halide co-substitution as 'Cl:0.3,Br:0.3' — "
                            "reproduces LPSClBr / comp2-5 chemistry. Excess "
                            "values sum to total S→halide swap fraction per f.u.")
    parser.add_argument('--vacancy_method', default='random',
                       choices=['random', 'spread', 'cluster', 'first',
                                'near_cation'],
                       help='Method for Li vacancy placement (default random — '
                            'matches experimental Kraft 2017 NMR / Adeli 2019 '
                            'PDF showing Li vacancies are disordered, not '
                            'arranged in a superlattice). "near_cation" '
                            'biases vacancy formation toward Li atoms within '
                            '--vacancy_cutoff Å of the aliovalent dopant, '
                            'matching the local charge-compensation picture '
                            '(Pham 2021 oxysulfide; aliovalent defect '
                            'theory).')
    parser.add_argument('--vacancy_cutoff', type=float, default=5.0,
                       help='Radius (Å) for --vacancy_method near_cation; '
                            'default 5.0 ≈ 2× P-S bond, captures the dopant '
                            "cation's first/second coordination shells.")

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

    if not args.compound and not args.halide_rich and not args.mixed_halides:
        parser.error(
            "Provide --compound (Type A), --halide_rich (Type B), or "
            "--mixed_halides (Type B' — comp2/3/4/5 chemistry)")

    base = read(args.base)
    if args.supercell != [1, 1, 1]:
        base = base.repeat(args.supercell)
        # Scale n_fu by the supercell multiplier
        cell_mult = args.supercell[0] * args.supercell[1] * args.supercell[2]
        n_fu_actual = args.n_fu * cell_mult
        print(f"Supercell {args.supercell}: base now {len(base)} atoms, "
              f"n_fu={n_fu_actual}")
    else:
        n_fu_actual = args.n_fu
    print(f"Loaded base: {len(base)} atoms, composition: {composition_summary(base)}")
    print(f"Effective f.u. per cell: {n_fu_actual}")

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    seeds = ([args.seed] if args.method != 'random'
             else [args.seed + i for i in range(args.n_seeds)])

    # Decide the (cation_site, anion_site) combinations to iterate.
    if args.auto_cation_sites:
        cation_sites = ['Li_24g', 'Li_48h', 'P_4b']
    else:
        cation_sites = [args.cation_site]
    if args.auto_anion_sites:
        anion_sites = ['S_16e', 'S_4a', 'Cl_4d']
    else:
        anion_sites = [args.anion_site]

    # Pre-filter site combinations against site_preference (only when iterating
    # auto modes — explicit single-site requests are kept as-is to let the user
    # force unusual placements like Sundar-style oxide-at-anion-site coatings).
    # --allow_exotic bypasses the filter so every combination is tried.
    if args.compound and not args.allow_exotic:
        compound_atoms = parse_compound(args.compound)
        cations_in = [el for el, _ in compound_atoms.items()
                      if DOPANT_DB.get(el, {}).get('charge', 0) > 0]
        anions_in = [el for el, _ in compound_atoms.items()
                     if DOPANT_DB.get(el, {}).get('charge', 0) < 0]
        if args.auto_cation_sites:
            allowed_c = set.intersection(*(compatible_sites_for_element(c, DOPANT_DB)
                                           for c in cations_in)) if cations_in else set()
            before = list(cation_sites)
            cation_sites = [s for s in cation_sites if s in allowed_c]
            if before != cation_sites:
                print(f"  site_preference filter (cations {cations_in}): "
                      f"{before} → {cation_sites}")
        if args.auto_anion_sites:
            allowed_a = set.intersection(*(compatible_sites_for_element(a, DOPANT_DB)
                                           for a in anions_in)) if anions_in else set()
            before = list(anion_sites)
            anion_sites = [s for s in anion_sites if s in allowed_a]
            if before != anion_sites:
                print(f"  site_preference filter (anions {anions_in}): "
                      f"{before} → {anion_sites}")
        if args.auto_cation_sites and not cation_sites:
            parser.error(f"No compatible cation sites for {cations_in}")
        if args.auto_anion_sites and not anion_sites:
            parser.error(f"No compatible anion sites for {anions_in}")

    print(f"Iterating: {len(cation_sites)} cation sites × "
          f"{len(anion_sites)} anion sites × {len(seeds)} seeds = "
          f"{len(cation_sites)*len(anion_sites)*len(seeds)} structures")

    generated: list[dict] = []
    for cation_site in cation_sites:
      for anion_site in anion_sites:
        for seed in seeds:
            doped = base.copy()
            info: dict = {
                'seed': seed,
                'cation_site_used': cation_site,
                'anion_site_used': anion_site,
                'steps': [],
            }

            # --- Type A ---
            if args.compound:
                composition = parse_compound(args.compound)
                n_units = max(1, int(round(n_fu_actual * args.x_compound)))
                actual_x = n_units / n_fu_actual
                try:
                    doped, log = substitute_compound_at_sites(
                        doped, composition, n_units,
                        cation_site, anion_site,
                        args.method, seed, DOPANT_DB,
                        vacancy_method=args.vacancy_method)
                    info['steps'].append({
                        'type': 'A_compound',
                        'compound': args.compound,
                        'composition': composition,
                        'n_units': n_units,
                        'actual_x': actual_x,
                        **log,
                    })
                except ValueError as e:
                    print(f"  ⚠ skip {args.compound} @ ({cation_site}, "
                          f"{anion_site}) seed={seed}: {e}")
                    continue

            # --- Type B (single halide) ---
            if args.halide_rich:
                if args.excess_per_fu is None:
                    parser.error("--halide_rich requires --excess_per_fu")
                n_swap = max(1, int(round(n_fu_actual * args.excess_per_fu)))
                doped, log = halide_rich_swap(
                    doped, args.halide_rich, n_swap,
                    anion_site if anion_site.startswith('S') else 'S_4a',
                    args.method, seed + 50,
                    vacancy_method=args.vacancy_method)
                info['steps'].append({
                    'type': 'B_halide_rich',
                    'halide': args.halide_rich,
                    'n_swap': n_swap,
                    'actual_excess': n_swap / n_fu_actual,
                    **log,
                })
            # --- Type B' (mixed halides — LPSClBr) ---
            elif args.mixed_halides:
                # Parse 'Cl:0.3,Br:0.3' format
                mix = {}
                for entry in args.mixed_halides.split(','):
                    h, x = entry.split(':')
                    mix[h.strip()] = float(x)
                doped, log = mixed_halide_swap(
                    doped, mix, n_fu_actual,
                    anion_site if anion_site.startswith('S') else 'S_4a',
                    args.method, seed + 60,
                    vacancy_method=args.vacancy_method)
                info['steps'].append({
                    'type': 'B_mixed_halide',
                    'mix': mix,
                    **log,
                })
            elif args.also_halide_rich:
                if args.excess_per_fu is None:
                    parser.error("--also_halide_rich requires --excess_per_fu")
                n_swap = max(1, int(round(n_fu_actual * args.excess_per_fu)))
                doped, log = halide_rich_swap(
                    doped, args.also_halide_rich, n_swap,
                    'S_4a', args.method, seed + 70,
                    vacancy_method=args.vacancy_method)
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
                parts.append(
                    f"{args.halide_rich}rich_x{int(args.excess_per_fu*1000):03d}")
            if args.also_halide_rich:
                parts.append(
                    f"chain_{args.also_halide_rich}_x{int(args.excess_per_fu*1000):03d}")
            # Disambiguate by site combination only when iterating multiple
            if len(cation_sites) > 1 or len(anion_sites) > 1:
                site_tag = f"c{cation_site.replace('_','')}a{anion_site.replace('_','')}"
                parts.append(site_tag)
            if args.supercell != [1, 1, 1]:
                parts.append("sc" + "x".join(str(s) for s in args.supercell))
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
                'n_fu_actual': n_fu_actual,
                'supercell': args.supercell,
            })
            generated.append(info)
            print(f"  ✓ {name}: {len(doped)} atoms, {composition_summary(doped)}")

    summary = {
        'base_file': args.base,
        'n_fu': args.n_fu,
        'n_fu_actual': n_fu_actual,
        'supercell': args.supercell,
        'method': args.method,
        'n_seeds': args.n_seeds,
        'cation_sites_tried': cation_sites,
        'anion_sites_tried': anion_sites,
        'structures': generated,
    }
    summary_path = out_dir / 'compound_summary.json'
    summary_path.write_text(json.dumps(summary, indent=2, default=str))
    print(f"\n✓ Generated {len(generated)} structures")
    print(f"✓ Summary: {summary_path}")


if __name__ == '__main__':
    main()
