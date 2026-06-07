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
import itertools
import json
from pathlib import Path
import numpy as np
from ase.io import read, write
from ase import Atoms

# Map site labels to host element (used to find substitution targets)
SITE_TO_HOST = {
    'Li_24g': 'Li', 'Li_48h': 'Li',
    'P_4b': 'P',
    'S_16e': 'S', 'S_4a': 'S',
    'Cl_4d': 'Cl',
}

# Evidence strength rank (lower = stronger). Used by --min_evidence to optionally
# skip weak LITERATURE sites (e.g. 'rietveld' XRD-only) in production runs while
# still generating them by default. Heuristic sites (evidence=None) are unaffected.
EVIDENCE_RANK = {'dft_exp': 0, 'exp': 1, 'analog': 2, 'rietveld': 3}


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


def select_substitution_sites(host_indices: list[int], n_sub: int,
                              method: str = 'first', seed: int = 42) -> list[int]:
    """Pick n_sub indices to substitute.

    method:
      'first': lowest indices (deterministic, reproducible)
      'random': random selection (use ``seed`` for reproducibility)
      'spread': maximize distance between chosen sites (anti-clustering)
    """
    if n_sub >= len(host_indices):
        return host_indices
    if method == 'first':
        return host_indices[:n_sub]
    if method == 'random':
        rng = np.random.default_rng(seed)
        return sorted(rng.choice(host_indices, size=n_sub, replace=False).tolist())
    # spread: greedy farthest-first (use simple index spacing as proxy)
    step = len(host_indices) // n_sub
    return [host_indices[i * step] for i in range(n_sub)]


def substitute(atoms: Atoms, dopant: str, host_element: str,
               n_sub: int, method: str = 'spread', seed: int = 42) -> Atoms:
    """Replace n_sub host atoms with dopant atoms."""
    new = atoms.copy()
    host_idx = find_host_indices(new, host_element)
    if not host_idx:
        raise ValueError(f"No {host_element} atoms in structure")
    targets = select_substitution_sites(host_idx, n_sub, method, seed=seed)
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
    targets = select_substitution_sites(li_idx, n_vac, method, seed=seed + 1)
    keep = [i for i in range(len(atoms)) if i not in targets]
    return atoms[keep]


def find_interstitial_sites(atoms: Atoms, n_sites: int, seed: int = 42,
                            d_min: float = 2.0, d_anion_max: float = 3.0,
                            grid_spacing: float = 0.6) -> list:
    """Find ``n_sites`` Li-interstitial positions = empty anion-coordinated
    pockets, for ACCEPTOR charge compensation (dopant charge < host charge).

    Method (deps: numpy + scipy only): scan a coarse fractional grid; keep grid
    points that are (a) >= ``d_min`` Å from EVERY atom (min-image, no overlap)
    and (b) within ``d_anion_max`` Å of >= 2 anions (S/Cl/O/...) so the spot is a
    real Li coordination pocket, not vacuum. Pick ``n_sites`` by farthest-first
    to spread them. Positions are APPROXIMATE — downstream UMA/DFT relaxation
    moves Li to its true site; the only requirement here is a charge-neutral,
    non-overlapping starting cell. Returns up to ``n_sites`` cartesian positions
    (fewer if no suitable pocket exists)."""
    from scipy.spatial import cKDTree
    cell = np.asarray(atoms.get_cell())
    pos = atoms.get_positions()
    sym = np.array(atoms.get_chemical_symbols())
    anion = np.isin(sym, ['S', 'Cl', 'O', 'Se', 'Te', 'Br', 'I', 'F', 'N'])
    # 3x3x3 periodic images so grid→atom distances are min-image correct
    shifts = np.array(list(itertools.product([-1, 0, 1], repeat=3))) @ cell
    img = (pos[None, :, :] + shifts[:, None, :]).reshape(-1, 3)
    img_anion = np.tile(anion, len(shifts))
    tree_all = cKDTree(img)
    tree_an = cKDTree(img[img_anion]) if img_anion.any() else None
    n = [max(3, int(round(np.linalg.norm(cell[i]) / grid_spacing))) for i in range(3)]
    fr = np.stack(np.meshgrid(
        *[np.linspace(0, 1, n[i], endpoint=False) for i in range(3)],
        indexing='ij'), -1).reshape(-1, 3)
    cart = fr @ cell
    keep = tree_all.query(cart)[0] >= d_min
    if tree_an is not None:
        keep &= (tree_an.query_ball_point(cart, d_anion_max, return_length=True) >= 2)
    cand = cart[keep]
    if len(cand) == 0:
        return []
    rng = np.random.default_rng(seed)
    chosen = [cand[rng.integers(len(cand))]]
    while len(chosen) < n_sites and len(chosen) < len(cand):
        d = np.min([np.linalg.norm(cand - c, axis=1) for c in chosen], axis=0)
        chosen.append(cand[int(np.argmax(d))])
    return chosen[:n_sites]


def add_li_interstitial(atoms: Atoms, n_add: int, seed: int = 42):
    """Add ``n_add`` Li at interstitial pockets (acceptor compensation).
    Returns (new_atoms, ok); ok=False if fewer than ``n_add`` pockets were found
    so the caller can gate the (then charge-unbalanced) cell out."""
    sites = find_interstitial_sites(atoms, n_add, seed=seed)
    if len(sites) < n_add:
        return atoms, False
    new = atoms.copy()
    for p in sites:
        new += Atoms('Li', positions=[p])
    return new, True


def apply_charge_compensation(atoms: Atoms, host_charge: int,
                              dopant_charge: int, n_dopants: int,
                              vacancy_method: str = 'spread',
                              seed: int = 42) -> Atoms:
    """Apply automatic charge compensation.

    Donor (Δq>0): remove Li (vacancy). Acceptor (Δq<0): ADD Li at interstitial
    pockets. If no pocket can be found the cell is left uncompensated and labelled
    'imbalanced_*' — generate_for_dopant gates those out so an unphysical charged
    cell never reaches UMA/DFT (which would otherwise score it high-energy for the
    wrong reason and spuriously 'refute' a real substitution)."""
    delta_q = (dopant_charge - host_charge) * n_dopants
    if delta_q == 0:
        return atoms, 'isovalent'
    elif delta_q > 0:
        # Donor: remove Li (each removal = +1 charge correction)
        return add_li_vacancy(atoms, n_vac=delta_q, method=vacancy_method,
                              seed=seed), f'Li_vac_{delta_q}'
    else:
        # Acceptor: add |delta_q| Li interstitials to neutralize the cell.
        new, ok = add_li_interstitial(atoms, n_add=-delta_q, seed=seed + 2)
        if ok:
            return new, f'Li_int_{-delta_q}'
        return atoms, f'imbalanced_{delta_q}'


def generate_for_dopant(base_atoms: Atoms, dopant_entry: dict,
                       concentrations: list[float], out_dir: Path,
                       dopant_db: dict, method: str = 'spread',
                       n_seeds: int = 1, base_seed: int = 42,
                       polymorph: str = 'unknown',
                       li_ordering: str = 'unknown',
                       min_evidence: str = None) -> list[dict]:
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
        # Optional evidence gate: skip weak LITERATURE sites (e.g. 'rietveld') in
        # production. Heuristic sites (no evidence) and strong literature pass.
        if min_evidence and site_info.get('source') == 'literature':
            ev = site_info.get('evidence')
            if ev is not None and EVIDENCE_RANK.get(ev, 99) > EVIDENCE_RANK[min_evidence]:
                print(f"  ⏭ skip {element} on {site}: evidence '{ev}' weaker than "
                      f"--min_evidence '{min_evidence}'")
                continue
        host = SITE_TO_HOST[site]
        host_indices = find_host_indices(base_atoms, host)
        n_host = len(host_indices)

        for conc in concentrations:
            n_sub = max(1, int(round(n_host * conc)))
            actual_conc = n_sub / n_host
            for seed in seeds:
                try:
                    doped, sub_idx = substitute(base_atoms, element, host,
                                                n_sub, method=method, seed=seed)
                    doped, comp_label = apply_charge_compensation(
                        doped, site_info['host_charge'], d_info['charge'],
                        n_sub, vacancy_method=method, seed=seed)

                    # GATE: never emit a charge-unbalanced cell — UMA/DFT would
                    # score it high-energy for the wrong reason (missing
                    # compensation, not bad site) and spuriously refute the site.
                    if comp_label.startswith('imbalanced'):
                        print(f"  ⏭ skip {element} on {site} conc={conc:.2f}: "
                              f"{comp_label} (no interstitial pocket found — "
                              f"charge-unbalanced cell gated out)")
                        continue

                    # diagnostic: closest approach of any added Li interstitial to
                    # the rest of the cell — lets downstream flag a relax that may
                    # diverge from a too-tight start (should be >~2.0 Å).
                    min_int_dist = None
                    if comp_label.startswith('Li_int'):
                        k = int(comp_label.split('_')[-1])
                        dmat = doped.get_all_distances(mic=True)
                        others = list(range(len(doped) - k))
                        min_int_dist = float(min(
                            dmat[i][others].min() for i in range(len(doped) - k, len(doped))))

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
                        # provenance from site_preference: literature vs heuristic,
                        # evidence strength + citation (carried so downstream
                        # analyze_screening can tier/flag by evidence).
                        'site_source': site_info.get('source'),
                        'evidence': site_info.get('evidence'),
                        'reference': site_info.get('reference'),
                        'min_int_dist': min_int_dist,
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
    parser.add_argument('--min_evidence', default=None,
                       choices=['dft_exp', 'exp', 'analog', 'rietveld'],
                       help="Skip LITERATURE sites weaker than this evidence level "
                            "(e.g. 'analog' drops rietveld-only claims like Y in "
                            "production). Default: generate all. Heuristic sites "
                            'are never gated by this.')
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
                     li_ordering=args.li_ordering, min_evidence=args.min_evidence)

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
        n_host = len(find_host_indices(base, host))
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
