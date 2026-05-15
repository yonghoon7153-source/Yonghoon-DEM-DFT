#!/usr/bin/env python
"""site_preference.py — LPSCl dopant site preference filter (Tier-1).

For a given dopant (element + charge + ionic radius), returns compatible
substitution sites in Li6PS5Cl argyrodite based on:
  (1) charge sign matching (cation vs anion)
  (2) ionic radius compatibility with host site
  (3) charge balance feasibility

This is the FAST filter (no DFT), used as Tier-1 screening before UMA.

Usage:
  python3 site_preference.py --dopant Mg --charge 2 --radius 0.72
  python3 site_preference.py --batch dopants.json
"""
import argparse
import json
from pathlib import Path

# Argyrodite Li6PS5Cl host site database
HOST_SITES = {
    'Li_24g':   {'host': 'Li',  'charge': +1, 'radius': 0.76,
                 'wyckoff': '24g', 'env': 'tetrahedral, Li sublattice'},
    'Li_48h':   {'host': 'Li',  'charge': +1, 'radius': 0.76,
                 'wyckoff': '48h', 'env': 'partial occupancy site'},
    'P_4b':     {'host': 'P',   'charge': +5, 'radius': 0.17,
                 'wyckoff': '4b', 'env': 'PS4 tetrahedron center'},
    'S_16e':    {'host': 'S',   'charge': -2, 'radius': 1.84,
                 'wyckoff': '16e', 'env': 'PS4-bonded S (covalent P-S)'},
    'S_4a':     {'host': 'S',   'charge': -2, 'radius': 1.84,
                 'wyckoff': '4a', 'env': 'free S2- (Li2S layer, surface)'},
    'Cl_4d':    {'host': 'Cl',  'charge': -1, 'radius': 1.81,
                 'wyckoff': '4d', 'env': 'halide site (bulk)'},
}

# Shannon ionic radii for common dopants (4-coord or 6-coord, charge-appropriate)
DOPANT_DB = {
    # Cations for Li site
    'Li':  {'charge': +1, 'radius': 0.76},
    'Na':  {'charge': +1, 'radius': 1.02},
    'K':   {'charge': +1, 'radius': 1.38},
    'Cu':  {'charge': +1, 'radius': 0.77},
    'Ag':  {'charge': +1, 'radius': 1.15},
    'Mg':  {'charge': +2, 'radius': 0.72},
    'Zn':  {'charge': +2, 'radius': 0.74},
    'Ca':  {'charge': +2, 'radius': 1.00},
    'Sr':  {'charge': +2, 'radius': 1.18},
    'Al':  {'charge': +3, 'radius': 0.535},
    'Ga':  {'charge': +3, 'radius': 0.62},
    'In':  {'charge': +3, 'radius': 0.80},
    'Sc':  {'charge': +3, 'radius': 0.745},
    'Y':   {'charge': +3, 'radius': 0.90},
    # Cations for P site
    'P':   {'charge': +5, 'radius': 0.17},
    'Sb':  {'charge': +5, 'radius': 0.60},
    'As':  {'charge': +5, 'radius': 0.46},
    'V':   {'charge': +5, 'radius': 0.54},
    'Nb':  {'charge': +5, 'radius': 0.64},
    'Si':  {'charge': +4, 'radius': 0.40},
    'Ge':  {'charge': +4, 'radius': 0.53},
    'Sn':  {'charge': +4, 'radius': 0.69},
    'Ti':  {'charge': +4, 'radius': 0.605},
    'Zr':  {'charge': +4, 'radius': 0.72},
    # Anions for S or Cl site
    'S':   {'charge': -2, 'radius': 1.84},
    'O':   {'charge': -2, 'radius': 1.40},
    'Se':  {'charge': -2, 'radius': 1.98},
    'Te':  {'charge': -2, 'radius': 2.21},
    'F':   {'charge': -1, 'radius': 1.33},
    'Cl':  {'charge': -1, 'radius': 1.81},
    'Br':  {'charge': -1, 'radius': 1.96},
    'I':   {'charge': -1, 'radius': 2.20},
    'N':   {'charge': -3, 'radius': 1.46},
    'P_anion': {'charge': -3, 'radius': 2.12},  # phosphide
}

# Tolerance for radius matching (15% rule + extra for anion site disorder)
RADIUS_TOL = {
    'cation': 0.30,   # Å, for Li/P sites
    'anion_4a': 0.40, # Å, S 4a is more flexible (anion disorder)
    'anion_16e': 0.20, # Å, S 16e is constrained (PS4 covalent)
    'anion_4d': 0.40, # Å, Cl 4d also flexible
}


def site_preference_filter(dopant_charge: int, dopant_radius: float,
                          allow_aliovalent: bool = True) -> list[dict]:
    """Returns compatible substitution sites for a dopant.

    Args:
        dopant_charge: signed integer charge (+1, +2, -1, -2, ...)
        dopant_radius: ionic radius in Å (Shannon)
        allow_aliovalent: if False, only same-charge substitution allowed.

    Returns:
        list of {site_name, host, host_charge, host_radius, charge_diff,
                 radius_diff, compatibility_score} for compatible sites,
        sorted by best fit first.
    """
    candidates = []
    for site_name, info in HOST_SITES.items():
        # (1) Sign of charge must match (cation ↔ cation, anion ↔ anion)
        if dopant_charge * info['charge'] <= 0:
            continue

        # (2) If isovalent only, skip aliovalent
        charge_diff = dopant_charge - info['charge']
        if (not allow_aliovalent) and (charge_diff != 0):
            continue

        # (3) Radius tolerance
        if site_name in ['Li_24g', 'Li_48h', 'P_4b']:
            tol = RADIUS_TOL['cation']
        elif site_name == 'S_4a':
            tol = RADIUS_TOL['anion_4a']
        elif site_name == 'S_16e':
            tol = RADIUS_TOL['anion_16e']
        else:  # Cl_4d
            tol = RADIUS_TOL['anion_4d']
        radius_diff = dopant_radius - info['radius']
        if abs(radius_diff) > tol:
            continue

        # (4) Score: smaller |radius_diff| + smaller |charge_diff| = better
        compat = 1.0 / (1.0 + abs(radius_diff) + abs(charge_diff) * 0.5)
        candidates.append({
            'site_name': site_name,
            'host': info['host'],
            'host_charge': info['charge'],
            'host_radius': info['radius'],
            'wyckoff': info['wyckoff'],
            'env': info['env'],
            'charge_diff': charge_diff,
            'radius_diff': round(radius_diff, 3),
            'compatibility_score': round(compat, 3),
        })

    candidates.sort(key=lambda x: -x['compatibility_score'])
    return candidates


def charge_balance(host_charge: int, dopant_charge: int, n_dopants: int) -> dict:
    """Determines charge compensation strategy."""
    delta_q = (dopant_charge - host_charge) * n_dopants
    if delta_q == 0:
        return {'compensation': 'isovalent', 'extra_defects': None, 'n_extra': 0}
    elif delta_q > 0:
        return {
            'compensation': 'aliovalent_donor',
            'extra_defects': ['cation_vacancy', 'anion_higher_charge_substitution'],
            'n_extra': delta_q,
        }
    else:
        return {
            'compensation': 'aliovalent_acceptor',
            'extra_defects': ['anion_vacancy', 'cation_higher_charge_substitution'],
            'n_extra': -delta_q,
        }


def evaluate_dopant(element: str, n_dopants: int = 1,
                   verbose: bool = True) -> dict:
    """Full evaluation of a dopant: site preference + charge balance."""
    if element not in DOPANT_DB:
        raise ValueError(f"Element {element} not in DOPANT_DB. Add it manually.")
    d = DOPANT_DB[element]
    sites = site_preference_filter(d['charge'], d['radius'])
    if not sites:
        return {'element': element, 'compatible_sites': [],
                'note': 'No compatible site found.'}

    result = {
        'element': element,
        'charge': d['charge'],
        'radius_A': d['radius'],
        'n_dopants': n_dopants,
        'compatible_sites': [],
    }
    for site in sites:
        balance = charge_balance(site['host_charge'], d['charge'], n_dopants)
        site_full = {**site, **balance}
        result['compatible_sites'].append(site_full)

    if verbose:
        print(f"\n=== Dopant: {element} (charge {d['charge']:+d}, radius {d['radius']} Å) ===")
        print(f"{'Site':<10} {'host':<5} {'Δq':>4} {'Δr':>6} {'score':>6} {'compensation':<30}")
        print("-" * 78)
        for s in result['compatible_sites']:
            print(f"{s['site_name']:<10} {s['host']:<5} {s['charge_diff']:>+4d} "
                  f"{s['radius_diff']:>+6.3f} {s['compatibility_score']:>6.3f} "
                  f"{s['compensation']:<30}")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dopant', help='Element symbol (e.g., Mg)')
    parser.add_argument('--n', type=int, default=1, help='Number of dopants')
    parser.add_argument('--batch', help='JSON file with list of elements')
    parser.add_argument('--list', action='store_true', help='List known dopants')
    parser.add_argument('--out', default=None, help='Save results to JSON')
    args = parser.parse_args()

    if args.list:
        print("Known dopants in DOPANT_DB:")
        for e, info in DOPANT_DB.items():
            print(f"  {e:<6} charge={info['charge']:+d} radius={info['radius']} Å")
        return

    results = []
    if args.batch:
        elements = json.loads(Path(args.batch).read_text())
        for e in elements:
            results.append(evaluate_dopant(e, n_dopants=args.n))
    elif args.dopant:
        results.append(evaluate_dopant(args.dopant, n_dopants=args.n))
    else:
        parser.print_help()
        return

    if args.out:
        Path(args.out).write_text(json.dumps(results, indent=2))
        print(f"\nSaved {len(results)} results to {args.out}")


if __name__ == '__main__':
    main()
