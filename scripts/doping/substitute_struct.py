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
                              method: str = 'first') -> list[int]:
    """Pick n_sub indices to substitute.

    method:
      'first': lowest indices (deterministic, reproducible)
      'random': random selection (with seed for reproducibility)
      'spread': maximize distance between chosen sites (anti-clustering)
    """
    if n_sub >= len(host_indices):
        return host_indices
    if method == 'first':
        return host_indices[:n_sub]
    if method == 'random':
        rng = np.random.default_rng(42)
        return sorted(rng.choice(host_indices, size=n_sub, replace=False).tolist())
    # spread: greedy farthest-first (use simple index spacing as proxy)
    step = len(host_indices) // n_sub
    return [host_indices[i * step] for i in range(n_sub)]


def substitute(atoms: Atoms, dopant: str, host_element: str,
               n_sub: int, method: str = 'spread') -> Atoms:
    """Replace n_sub host atoms with dopant atoms."""
    new = atoms.copy()
    host_idx = find_host_indices(new, host_element)
    if not host_idx:
        raise ValueError(f"No {host_element} atoms in structure")
    targets = select_substitution_sites(host_idx, n_sub, method)
    syms = new.get_chemical_symbols()
    for i in targets:
        syms[i] = dopant
    new.set_chemical_symbols(syms)
    return new, targets


def add_li_vacancy(atoms: Atoms, n_vac: int = 1, method: str = 'spread') -> Atoms:
    """Remove n_vac Li atoms (for donor charge compensation)."""
    li_idx = find_host_indices(atoms, 'Li')
    if n_vac >= len(li_idx):
        raise ValueError(f"Cannot remove {n_vac} Li from {len(li_idx)} atoms")
    targets = select_substitution_sites(li_idx, n_vac, method)
    keep = [i for i in range(len(atoms)) if i not in targets]
    return atoms[keep]


def apply_charge_compensation(atoms: Atoms, host_charge: int,
                              dopant_charge: int, n_dopants: int) -> Atoms:
    """Apply automatic charge compensation."""
    delta_q = (dopant_charge - host_charge) * n_dopants
    if delta_q == 0:
        return atoms, 'isovalent'
    elif delta_q > 0:
        # Donor: remove Li (each removal = +1 charge correction)
        return add_li_vacancy(atoms, n_vac=delta_q), f'Li_vac_{delta_q}'
    else:
        # Acceptor: simplest = add Li interstitial. For now, leave imbalanced
        # with note. (Proper treatment needs Li interstitial site finding.)
        return atoms, f'imbalanced_{delta_q}'


def generate_for_dopant(base_atoms: Atoms, dopant_entry: dict,
                       concentrations: list[float], out_dir: Path,
                       dopant_db: dict) -> list[dict]:
    """Generate structures for one dopant across all sites + concentrations."""
    element = dopant_entry['element']
    if element not in dopant_db:
        return []
    d_info = dopant_db[element]

    generated = []
    for site_info in dopant_entry.get('compatible_sites', []):
        site = site_info['site_name']
        host = SITE_TO_HOST[site]
        host_indices = find_host_indices(base_atoms, host)
        n_host = len(host_indices)

        for conc in concentrations:
            n_sub = max(1, int(round(n_host * conc)))
            actual_conc = n_sub / n_host
            try:
                doped, sub_idx = substitute(base_atoms, element, host, n_sub,
                                            method='spread')
                doped, comp_label = apply_charge_compensation(
                    doped, site_info['host_charge'], d_info['charge'], n_sub)

                # Output filename
                name = f"{element}_{site}_x{int(actual_conc*1000):03d}_{comp_label}"
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
                })
            except Exception as e:
                print(f"  ❌ {element} on {site} conc={conc:.2f}: {e}")
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
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading LPSCl base from: {args.base}")
    base = read(args.base)
    print(f"  base: {len(base)} atoms, "
          f"composition: {dict(zip(*np.unique(base.get_chemical_symbols(), return_counts=True)))}")

    # Load DOPANT_DB from site_preference module
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from site_preference import DOPANT_DB

    if args.site_pref:
        site_pref_data = json.loads(Path(args.site_pref).read_text())
        all_generated = []
        for entry in site_pref_data:
            gens = generate_for_dopant(base, entry, args.concentrations,
                                      out_dir, DOPANT_DB)
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
                                           out_dir, DOPANT_DB)
    else:
        parser.error("Provide --site_pref OR (--dopant --site --conc)")

    summary_path = out_dir / 'structures_summary.json'
    summary_path.write_text(json.dumps(all_generated, indent=2, default=str))
    print(f"\n✓ Generated {len(all_generated)} structures")
    print(f"✓ Summary: {summary_path}")


if __name__ == '__main__':
    main()
