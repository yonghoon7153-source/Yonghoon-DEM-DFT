#!/usr/bin/env python
"""substitute_struct.py — Generate LPSCl + dopant structures.

For each (dopant, target_site, concentration) combo from
site_preference_initial.json, generates LPSCl-doped structure with
appropriate charge compensation (Li vacancy for donor, etc.).

Usage:
  # Default: all candidates from site_preference_initial.json, conc 0.05~0.20
  python3 substitute_struct.py \\
      --base data/lpscl_bulk.cif \\
      --site_pref data/doping_screening/site_preference_initial.json \\
      --concentrations 0.05 0.10 0.20 \\
      --out data/doping_screening/structures/

  # Single dopant test
  python3 substitute_struct.py --base data/lpscl_bulk.cif \\
      --dopant Mg --site Li_24g --conc 0.10 --out test_struct/
"""
import argparse
import json
import sys
from pathlib import Path
import numpy as np
from ase.io import read, write
from ase import Atoms

sys.path.insert(0, str(Path(__file__).parent))
from _provenance import get_provenance

# Map site labels to host element (used to find substitution targets)
SITE_TO_HOST = {
    'Li_24g': 'Li', 'Li_48h': 'Li',
    'P_4b': 'P',
    'S_16e': 'S', 'S_4a': 'S',
    'Cl_4d': 'Cl',
}


def fetch_lpscl_from_mp(api_key: str = None, mp_id: str = 'mp-985592') -> Atoms:
    """Fetch Li6PS5Cl bulk structure from Materials Project.

    Common MP IDs for Li6PS5Cl: mp-985592, mp-987601 (variants).
    Falls back to manual structure if API not available.
    """
    try:
        from mp_api.client import MPRester
        with MPRester(api_key) as mpr:
            doc = mpr.materials.summary.search(material_ids=[mp_id])[0]
            struct = doc.structure
            from pymatgen.io.ase import AseAtomsAdaptor
            return AseAtomsAdaptor.get_atoms(struct)
    except Exception as e:
        print(f"  MP fetch failed: {e}")
        return None


def find_host_indices(atoms: Atoms, host_element: str) -> list[int]:
    """Find all atom indices matching host element."""
    return [i for i, sym in enumerate(atoms.get_chemical_symbols())
            if sym == host_element]


def find_host_indices_for_site(atoms: Atoms, site_name: str,
                               ps_cutoff: float = 2.7) -> list[int]:
    """Return indices matching host element AND specific Wyckoff site.

    Distinguishes the two crystallographically inequivalent S²⁻ environments
    in argyrodite Li6PS5Cl (cubic F-43m):

      * S_16e — bonded to P (P–S < ``ps_cutoff`` Å) → PS₄ tetrahedral S.
      * S_4a  — not bonded to P → free S²⁻ in the Li2S-like sublattice.

    For Li sites (Li_24g / Li_48h), Cl_4d, and P_4b, returns every host
    element atom: distinguishing Li 24g vs 48h reliably requires the
    Wyckoff metadata of the input file (not always available), and the
    other host sites have only one Wyckoff per element in this system.
    """
    host = SITE_TO_HOST[site_name]
    host_idx = [i for i, sym in enumerate(atoms.get_chemical_symbols())
                if sym == host]
    if site_name not in ('S_16e', 'S_4a'):
        return host_idx
    p_idx = [i for i, sym in enumerate(atoms.get_chemical_symbols())
             if sym == 'P']
    if not p_idx:
        return host_idx
    from ase.geometry import get_distances
    s_pos = atoms.get_positions()[host_idx]
    p_pos = atoms.get_positions()[p_idx]
    _, dists = get_distances(s_pos, p_pos,
                             cell=atoms.cell.array, pbc=atoms.pbc)
    bonded = (dists < ps_cutoff).any(axis=1)
    if site_name == 'S_16e':
        return [host_idx[i] for i, b in enumerate(bonded) if b]
    return [host_idx[i] for i, b in enumerate(bonded) if not b]


def select_substitution_sites(host_indices: list[int], n_sub: int,
                              method: str = 'first', seed: int = 42,
                              atoms: Atoms | None = None,
                              reference_indices: list[int] | None = None,
                              cluster_radius: float = 4.0) -> list[int]:
    """Pick n_sub indices to substitute. Selection strategy via ``method``:

      'first':  lowest indices (truly deterministic — same atoms regardless
                of seed). For reproducibility tests / ablation only.
      'random': uniform random subset; SEED-REPRODUCIBLE (same ``seed``
                gives same output, but different seeds give different
                outputs — this is the only mode that varies across seeds).
      'spread': PBC-aware farthest-point sampling. SEED-REPRODUCIBLE
                with random initial seed atom — different ``seed``
                values give different starting points (so the resulting
                set varies seed-to-seed even though selection is greedy
                deterministic afterwards). Models a homogeneous solid
                solution from extensive ball milling (Yu 2022, Kraft 2017).
                Requires ``atoms`` for PBC distance calc.
      'cluster': greedy chain growth — pick a seed atom (random per seed)
                and at each step add the host atom NEAREST to the already-
                chosen set. NOT a true radius-based cluster: this is
                'chain' clustering, where the selection extends through
                successive nearest neighbours. May leave the seed PS4 and
                hop into adjacent PS4 if those S atoms are closer to the
                last pick than the remaining same-PS4 S atoms. The mean
                pair distance ≈ PS4 S-S edge (~3.4 Å) on canonical LPSCl
                because the F-43m geometry happens to place inter-PS4 S
                farther than intra-PS4 S, but for distorted geometries
                this approximation breaks down.

    ``atoms`` must be supplied for 'spread' / 'cluster' so PBC distances
    can be computed (MIC = minimum image convention).
    """
    if n_sub >= len(host_indices):
        return host_indices
    if method == 'first':
        return host_indices[:n_sub]
    if method == 'random':
        rng = np.random.default_rng(seed)
        return sorted(rng.choice(host_indices, size=n_sub, replace=False).tolist())

    if method in ('spread', 'cluster'):
        if atoms is None:
            step = max(1, len(host_indices) // n_sub)
            return [host_indices[i * step] for i in range(n_sub)]
        rng = np.random.default_rng(seed)
        D_full = atoms.get_all_distances(mic=True)
        D = D_full[np.ix_(host_indices, host_indices)]
        chosen_local = [int(rng.integers(0, len(host_indices)))]
        for _ in range(n_sub - 1):
            min_d_to_chosen = D[:, chosen_local].min(axis=1)
            min_d_to_chosen[chosen_local] = -np.inf if method == 'spread' else np.inf
            if method == 'spread':
                next_local = int(np.argmax(min_d_to_chosen))
            else:  # cluster (chain — nearest to already chosen)
                next_local = int(np.argmin(min_d_to_chosen))
            chosen_local.append(next_local)
        return sorted(host_indices[i] for i in chosen_local)

    if method == 'near_cation':
        # Bias selection toward host atoms close to reference_indices (the
        # aliovalent cation positions). Models local charge compensation:
        # Li vacancy forms preferentially near a Mg²⁺/Al³⁺/Nd³⁺ dopant to
        # minimize Madelung energy of the defect pair.
        if atoms is None or not reference_indices:
            # Fallback to random when no reference available
            rng = np.random.default_rng(seed)
            return sorted(rng.choice(host_indices, size=n_sub,
                                    replace=False).tolist())
        D_full = atoms.get_all_distances(mic=True)
        # For each host_idx, distance to nearest reference atom
        min_d_to_ref = D_full[np.ix_(host_indices, reference_indices)].min(axis=1)
        # Probability weight ∝ exp(-d/cutoff) — exponential decay matches
        # Coulomb 1/r decay roughly while keeping things normalized.
        rng = np.random.default_rng(seed)
        weights = np.exp(-min_d_to_ref / cluster_radius)
        weights = weights / weights.sum()
        picks = rng.choice(len(host_indices), size=n_sub, replace=False,
                          p=weights)
        return sorted(host_indices[i] for i in picks)

    raise ValueError(f"Unknown selection method: {method!r}")


def substitute(atoms: Atoms, dopant: str, host_element: str,
               n_sub: int, method: str = 'spread', seed: int = 42,
               site_name: str | None = None) -> Atoms:
    """Replace n_sub host atoms with dopant atoms.

    If ``site_name`` is given (e.g., 'S_16e'), restrict the substitution to
    that specific Wyckoff site via :func:`find_host_indices_for_site`.
    Otherwise fall back to the chemical-element-only filter (legacy).
    """
    new = atoms.copy()
    if site_name is not None:
        host_idx = find_host_indices_for_site(new, site_name)
        if not host_idx:
            raise ValueError(
                f"No atoms at Wyckoff site {site_name} (host {host_element})")
    else:
        host_idx = find_host_indices(new, host_element)
        if not host_idx:
            raise ValueError(f"No {host_element} atoms in structure")
    targets = select_substitution_sites(host_idx, n_sub, method, seed=seed,
                                        atoms=new)
    syms = new.get_chemical_symbols()
    for i in targets:
        syms[i] = dopant
    new.set_chemical_symbols(syms)
    return new, targets


def add_li_vacancy(atoms: Atoms, n_vac: int = 1, method: str = 'spread',
                   seed: int = 42) -> Atoms:
    """Remove n_vac Li atoms (for donor charge compensation)."""
    li_idx = find_host_indices(atoms, 'Li')
    if n_vac >= len(li_idx):
        raise ValueError(f"Cannot remove {n_vac} Li from {len(li_idx)} atoms")
    # Use seed+1 so vacancy != substitution sites for the same nominal seed
    targets = select_substitution_sites(li_idx, n_vac, method, seed=seed + 1,
                                        atoms=atoms)
    keep = [i for i in range(len(atoms)) if i not in targets]
    return atoms[keep]


def apply_charge_compensation(atoms: Atoms, host_charge: int,
                              dopant_charge: int, n_dopants: int,
                              vacancy_method: str = 'spread',
                              seed: int = 42) -> Atoms:
    """Apply automatic charge compensation."""
    delta_q = (dopant_charge - host_charge) * n_dopants
    if delta_q == 0:
        return atoms, 'isovalent'
    elif delta_q > 0:
        # Donor: remove Li (each removal = +1 charge correction)
        return add_li_vacancy(atoms, n_vac=delta_q, method=vacancy_method,
                              seed=seed), f'Li_vac_{delta_q}'
    else:
        # Acceptor: simplest = add Li interstitial. For now, leave imbalanced
        # with note. (Proper treatment needs Li interstitial site finding.)
        return atoms, f'imbalanced_{delta_q}'


def generate_for_dopant(base_atoms: Atoms, dopant_entry: dict,
                       concentrations: list[float], out_dir: Path,
                       dopant_db: dict, method: str = 'spread',
                       n_seeds: int = 1, base_seed: int = 42,
                       polymorph: str = 'unknown',
                       li_ordering: str = 'unknown') -> list[dict]:
    """Generate structures for one dopant across all sites + concentrations.

    method: 'spread' (deterministic, default) or 'random' (paired with n_seeds).
    n_seeds: number of independent seeds when method='random' — required to build
        a Li-ordering ensemble that lets downstream UMA screening report mean±std
        of B0/E (Pustorino 2025, D'Amore 2022).
    polymorph / li_ordering: metadata stamped on every generated record so the
        downstream pipeline can group results by baseline polymorph/ordering.
    """
    element = dopant_entry['element']
    if element not in dopant_db:
        return []
    d_info = dopant_db[element]

    seeds = ([base_seed] if method != 'random'
             else [base_seed + i for i in range(n_seeds)])

    generated = []
    for site_info in dopant_entry.get('compatible_sites', []):
        site = site_info['site_name']
        host = SITE_TO_HOST[site]
        host_indices = find_host_indices_for_site(base_atoms, site)
        n_host = len(host_indices)
        if n_host == 0:
            print(f"  ⚠ {element} on {site}: 0 atoms at this Wyckoff site, "
                  f"skipping all concentrations")
            continue

        for conc in concentrations:
            n_sub = max(1, int(round(n_host * conc)))
            actual_conc = n_sub / n_host
            for seed in seeds:
                try:
                    doped, sub_idx = substitute(base_atoms, element, host,
                                                n_sub, method=method, seed=seed,
                                                site_name=site)
                    doped, comp_label = apply_charge_compensation(
                        doped, site_info['host_charge'], d_info['charge'],
                        n_sub, vacancy_method=method, seed=seed)

                    base_name = (f"{element}_{site}_x{int(actual_conc*1000):03d}"
                                 f"_{comp_label}")
                    name = (base_name if method != 'random'
                            else f"{base_name}_s{seed - base_seed:02d}")
                    xyz_path = out_dir / f'{name}.xyz'
                    write(xyz_path, doped)

                    generated.append({
                        'name': name,
                        'dopant': element,
                        'host': host,
                        'site': site,
                        'concentration': actual_conc,
                        'n_sub': n_sub,
                        'charge_compensation': comp_label,
                        'compatibility_score': site_info['compatibility_score'],
                        'n_atoms': len(doped),
                        'composition': dict(zip(*np.unique(
                            doped.get_chemical_symbols(), return_counts=True))),
                        'xyz_file': str(xyz_path),
                        'polymorph': polymorph,
                        'li_ordering': li_ordering,
                        'selection_method': method,
                        'seed': seed,
                    })
                except Exception as e:
                    print(f"  ❌ {element} on {site} conc={conc:.2f} "
                          f"seed={seed}: {e}")
    return generated


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--base', required=True,
                       help='LPSCl base structure (cif/xyz/POSCAR)')
    parser.add_argument('--site_pref', help='site_preference_initial.json')
    parser.add_argument('--dopant', help='Single dopant (e.g., Mg)')
    parser.add_argument('--site', help='Single site (e.g., Li_24g)')
    parser.add_argument('--conc', type=float, help='Single concentration')
    parser.add_argument('--concentrations', nargs='+', type=float,
                       default=[0.05, 0.10, 0.20],
                       help='Concentration list (mole fraction)')
    parser.add_argument('--out', required=True, help='Output directory')
    parser.add_argument('--polymorph', default='unknown',
                       choices=['unknown', 'cubic_F-43m', 'pseudo_cubic_P1',
                                'monoclinic_Pm'],
                       help='Baseline polymorph label (metadata only — pass the '
                            'matching --base file). See '
                            'kb/literature_db/damore_2022_lpscl_symmetry_breaking_qha.md.')
    parser.add_argument('--li_ordering', default='unknown',
                       choices=['unknown', '24G', '48H', '48HR', '48HR_inv',
                                '48H_low'],
                       help='Baseline Li ordering label (metadata only — pass the '
                            'matching --base file). See '
                            'kb/literature_db/pustorino_2025_lpscl_li_ordering_mechanical.md.')
    parser.add_argument('--method', default='spread',
                       choices=['spread', 'random', 'first'],
                       help="Substitution-site selection: 'spread' (deterministic, "
                            "default) or 'random' (use with --n_seeds for ensemble).")
    parser.add_argument('--n_seeds', type=int, default=1,
                       help='Number of random seeds per (dopant, site, conc) when '
                            "--method=random. Enables Li-ordering ensemble for "
                            'mean±std B0/E (Pustorino 2025: ~16 GPa B0 spread).')
    parser.add_argument('--seed', type=int, default=42,
                       help='Base RNG seed (used directly when --method!=random).')
    args = parser.parse_args()

    if args.method == 'random' and args.n_seeds < 2:
        print("⚠ --method=random with --n_seeds=1 gives a single configuration "
              "(no ensemble). Set --n_seeds≥3 for B0/E mean±std.")
    if args.polymorph == 'unknown' or args.li_ordering == 'unknown':
        print("⚠ Baseline polymorph or Li ordering is 'unknown'. Recommended: "
              "--polymorph monoclinic_Pm --li_ordering 48HR (ground state). "
              "mp-985592 is metastable cubic_F-43m / 24G.")

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading LPSCl base from: {args.base}")
    base = read(args.base)
    print(f"  base: {len(base)} atoms, "
          f"composition: {dict(zip(*np.unique(base.get_chemical_symbols(), return_counts=True)))}")
    print(f"  polymorph={args.polymorph}, li_ordering={args.li_ordering}, "
          f"method={args.method}, n_seeds={args.n_seeds}")

    # Load DOPANT_DB from site_preference module
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from site_preference import DOPANT_DB

    common_kw = dict(method=args.method, n_seeds=args.n_seeds,
                     base_seed=args.seed, polymorph=args.polymorph,
                     li_ordering=args.li_ordering)

    if args.site_pref:
        site_pref_data = json.loads(Path(args.site_pref).read_text())
        all_generated = []
        for entry in site_pref_data:
            gens = generate_for_dopant(base, entry, args.concentrations,
                                      out_dir, DOPANT_DB, **common_kw)
            all_generated.extend(gens)
            print(f"  {entry['element']}: {len(gens)} structures")
    elif args.dopant and args.site and args.conc:
        # Single mode
        d_info = DOPANT_DB[args.dopant]
        host = SITE_TO_HOST[args.site]
        n_host = len(find_host_indices_for_site(base, args.site))
        n_sub = max(1, int(round(n_host * args.conc)))
        from site_preference import HOST_SITES
        site_info = {**HOST_SITES[args.site], 'site_name': args.site,
                    'host_charge': HOST_SITES[args.site]['charge']}
        entry = {'element': args.dopant, 'compatible_sites': [{
            **site_info, 'compatibility_score': 1.0,
        }]}
        all_generated = generate_for_dopant(base, entry, [args.conc],
                                           out_dir, DOPANT_DB, **common_kw)
    else:
        parser.error("Provide --site_pref OR (--dopant --site --conc)")

    summary_path = out_dir / 'structures_summary.json'
    summary_path.write_text(json.dumps({
        'provenance': get_provenance(),  # v4.5.13 NEW-1 fix
        'baseline': {
            'base_file': args.base,
            'polymorph': args.polymorph,
            'li_ordering': args.li_ordering,
            'selection_method': args.method,
            'n_seeds': args.n_seeds,
            'base_seed': args.seed,
        },
        'structures': all_generated,
    }, indent=2, default=str))
    print(f"\n✓ Generated {len(all_generated)} structures")
    print(f"✓ Summary: {summary_path}")


if __name__ == '__main__':
    main()
