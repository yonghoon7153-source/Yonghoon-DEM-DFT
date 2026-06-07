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
    'Ba':  {'charge': +2, 'radius': 1.35},
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

# Per-site radius tolerance (Å), calibrated to observed LPSCl substitutions.
# Each cutoff is the smallest |Δr| that still admits ALL experimentally
# reported dopants on that site, while rejecting the next-larger un-reported
# one. Reference list (Shannon ionic radii):
#
#   Li site (host 0.76 Å) — passes up to Ba(|Δr|=0.59), rejects K(0.62)
#     ✅ Cu 0.01, Mg 0.04, Zn 0.02, Y 0.14, Al 0.225, Ca 0.24, Na 0.26,
#        Ag 0.39 (Nature Comm 2025), Sr 0.42 (Ca/Ba 사이, plausible),
#        Ba 0.59 (PMC 11106650 mechanochemical Li6-aBa_a/2 PS5Cl)
#     ❌ K 0.62 (pure-K argyrodite only, Li-K mixed not reported)
#     → cutoff 0.60 Å
#
#   P site (host 0.17 Å) — host radius too small for percent rule, use abs
#     ✅ Si 0.23, As 0.29, V 0.37, Ge 0.36, Sb 0.43, Nb 0.47, Sn 0.52
#        (MDPI 16(7), 2751, 2023 Sn-substituted Li6PS5Cl)
#     → cutoff 0.55 Å
#
#   S sites (16e and 4a, host 1.84 Å) — same cutoff (PS4 → PO4 is
#     energetically favorable, JMCA 2022; ACS AMI 2021 showed O prefers
#     S_16e over S_4a). Old 0.20/0.40 split was wrong.
#     ✅ Se 0.14, Te 0.37, N 0.38 (anion disorder), O 0.44 (ACS AMI 2021)
#     → cutoff 0.50 Å (both sites)
#
#   Cl site (host 1.81 Å)
#     ✅ Br 0.15, I 0.39, F 0.48 (ACS AMI 2022 fluorine-doped argyrodite)
#     → cutoff 0.50 Å
#
# The earlier ISOVALENT_TOL_FACTOR was a hack — observed cases now drive the
# cutoff directly, and a separate isovalent multiplier is no longer needed.
RADIUS_TOL = {
    'Li_24g': 0.60,
    'Li_48h': 0.60,
    'P_4b':   0.55,
    'S_16e':  0.50,
    'S_4a':   0.50,
    'Cl_4d':  0.50,
}


# Literature-reported dopant→site assignments, tagged by EVIDENCE STRENGTH.
# These are admitted as candidate sites regardless of the RADIUS_TOL cutoff
# (so we never silently drop a reported case like Y→P), but they are NOT treated
# as ground truth — each carries an evidence level so the downstream UMA/DFT
# screening can ADJUDICATE. The pipeline's job is precisely to confirm or refute
# weak claims by energy, not to trust them blindly.
#
#   EVIDENCE levels (strong → weak):
#     'dft_exp'  : ab-initio + experiment agree (trust; e.g. Si/Ge thio-LISICON)
#     'exp'      : solid experimental (multiple probes / well-established chemistry)
#     'analog'   : inferred from isovalent group analog (chemically safe, e.g. As/Sb)
#     'rietveld' : XRD Rietveld site assignment ONLY, no computation — WEAK for a
#                  dilute dopant (Y@P vs Y@Li poorly separable by XRD); GENERATE
#                  and let our UMA/DFT decide (may refute the paper).
# Format: element -> {site: (evidence, reference)}.
KNOWN_SUBSTITUTIONS = {
    # ---- P_4b (PS4 center, replaces P5+) ----
    'Y':  {'P_4b': ('rietveld', 'J. Power Sources 2022 S0378775322008357 — Y3+→P5+ '
                    'by Rietveld ONLY, no ab-initio; |Δr|=0.73>cutoff. VERIFY w/ our DFT')},
    'Si': {'P_4b': ('dft_exp', 'RSC Mater. Adv. 2024 D3MA01042B + LGPS-type — Si4+→P5+')},
    'Ge': {'P_4b': ('dft_exp', 'thio-LISICON Li10GeP2S12 — Ge4+→P5+')},
    'Sn': {'P_4b': ('exp', 'MDPI Materials 16(7),2751 (2023); RSC MCF 2025 D5QM00394F — '
                    'Sn4+→P5+ (easier in LPSBr/LPSI; small Cl framework limits)')},
    'Sb': {'P_4b': ('analog', 'Sb5+→P5+ isovalent group 15')},
    'As': {'P_4b': ('analog', 'As5+→P5+ isovalent group 15')},
    'V':  {'P_4b': ('analog', 'V5+→P5+ tetrahedral VS4')},
    'Nb': {'P_4b': ('analog', 'Nb5+→P5+ (A=…,V,Nb,Ta family)')},
    'Ti': {'P_4b': ('analog', 'Ti4+→P5+ (A=Ti family)')},
    'Zr': {'P_4b': ('analog', 'Zr4+→P5+ (A=Zr family)')},
    # (Ta5+, Bi5+ also reported for P — add to DOPANT_DB if screened)
    # ---- Li_24g (Li sublattice) ----
    'Al': {'Li_24g': ('exp', 'MDPI Nanomaterials 12(24),4355 (2022) — Al3+→Li+, lattice '
                      'CONTRACTION confirms Li site (P-site would expand; not seen)')},
    'Ag': {'Li_24g': ('exp', 'Nature Comm 2025 silver-exsolution argyrodite')},
    'Na': {'Li_24g': ('exp', 'Na+→Li+ common')},
    'Ca': {'Li_24g': ('exp', 'Li5.35Ca0.1PS4.5Cl1.55, 10.2 mS/cm')},
    'Ba': {'Li_24g': ('exp', 'PMC 11106650 mechanochemical Li6-aBa_a/2PS5Cl')},
    'Mg': {'Li_24g': ('exp', 'PMC 9054619 multivalent-cation-doped LPSCl')},
    'Zn': {'Li_24g': ('exp', 'PMC 9054619 multivalent-cation-doped LPSCl')},
    # ---- anion sites ----
    'O':  {'S_16e': ('dft_exp', 'ACS AMI 2021 Li6PS5-xClOx — O→S_16e (P-O covalent) > S_4a')},
    'Se': {'S_16e': ('exp', 'Se2-→S2-')},
    'Te': {'S_16e': ('exp', 'Te2-→S2-')},
    'F':  {'Cl_4d': ('exp', 'ACS AMI 2022 fluorine-doped argyrodite')},
    'Br': {'Cl_4d': ('exp', 'halogen mixing')},
    'I':  {'Cl_4d': ('exp', 'I-F dual-doped JPCC 2023; Li6PS5I')},
    'N':  {'S_16e': ('analog', 'anion disorder (nitrogen)')},
}


# Literature validation set: (element, expected_pass_or_fail, reference).
# Used by `--validate` to make sure RADIUS_TOL cutoffs reproduce the
# experimentally observed pattern.
VALIDATION_SET = [
    # element, must_pass, primary reference
    ('Cu',  True,  'isovalent Li sub, common'),
    ('Mg',  True,  'aliovalent +2, common'),
    ('Zn',  True,  'aliovalent +2, common'),
    ('Ca',  True,  'Li5.35Ca0.1PS4.5Cl1.55, 10.2 mS/cm'),
    ('Na',  True,  'Na→Li, common'),
    ('Ag',  True,  'Nature Comm 2025 silver-exsolution argyrodite'),
    ('Ba',  True,  'PMC 11106650 mechanochemical Li6-aBa_a/2 PS5Cl '
                   '(NOTE: known to work but radius=1.35 outside our cutoff; '
                   'expected to be borderline)'),
    ('K',   False, 'Pure-K argyrodite only; Li-K mixed not reported'),
    ('Al',  True,  'Li5.4Al0.1PS4.7Cl1.3, 7.29 mS/cm'),
    ('Y',   True,  'mechanochemical Y-doped LPSCl'),
    ('Sb',  True,  'Sb→P, common'),
    ('Sn',  True,  'MDPI Materials 16(7), 2751 (2023) Sn-substituted LPSCl'),
    ('Ge',  True,  'Ge→P, common'),
    ('O',   True,  'ACS AMI 2021 Li6PS5-xClOx oxysulfide (best site = S_16e)'),
    ('Se',  True,  'Se→S, common'),
    ('Te',  True,  'Te→S, common'),
    ('F',   True,  'ACS AMI 2022 fluorine-doped argyrodite'),
    ('Br',  True,  'halogen mixing, common'),
    ('I',   True,  'I-F dual-doped JPCC 2023'),
]


def validate_against_literature() -> int:
    """Cross-check RADIUS_TOL cutoffs against documented LPSCl substitutions.
    Returns number of mismatches (0 = all consistent)."""
    print(f"\n{'='*72}")
    print(f"Validation against literature ({len(VALIDATION_SET)} cases)")
    print('=' * 72)
    print(f"{'Elem':<6}{'Expect':<8}{'Got':<8}{'OK?':<6}{'Note'}")
    print('-' * 72)
    mismatches = 0
    for elem, must_pass, note in VALIDATION_SET:
        if elem not in DOPANT_DB:
            print(f"{elem:<6}{'?':<8}{'(missing in DB)':<8}{'⚠':<6}{note}")
            mismatches += 1
            continue
        d = DOPANT_DB[elem]
        sites = site_preference_filter(d['charge'], d['radius'], element=elem)
        got_pass = bool(sites)
        ok = (got_pass == must_pass)
        if not ok:
            mismatches += 1
        mark = '✓' if ok else '✗'
        expected = 'PASS' if must_pass else 'FAIL'
        actual = 'pass' if got_pass else 'fail'
        print(f"{elem:<6}{expected:<8}{actual:<8}{mark:<6}{note[:55]}")
    print('-' * 72)
    print(f"Mismatches: {mismatches} / {len(VALIDATION_SET)}")
    return mismatches


def site_preference_filter(dopant_charge: int, dopant_radius: float,
                          allow_aliovalent: bool = True,
                          element: str = None) -> list[dict]:
    """Returns compatible substitution sites for a dopant.

    Args:
        dopant_charge: signed integer charge (+1, +2, -1, -2, ...)
        dopant_radius: ionic radius in Å (Shannon)
        allow_aliovalent: if False, only same-charge substitution allowed.
        element: dopant symbol. If given and present in KNOWN_SUBSTITUTIONS,
            its literature-reported sites are admitted REGARDLESS of the radius
            cutoff (source='literature', tagged with evidence level); the radius
            heuristic then only adds further sites (source='heuristic'). Without
            `element`, behaviour is the pure radius heuristic (unchanged).

    Returns:
        list of {site_name, host, host_charge, host_radius, charge_diff,
                 radius_diff, compatibility_score, source[, evidence, reference]},
        literature sites first then heuristic, each by best fit.
    """
    def _make(site_name, info, source, evidence=None, ref=None):
        charge_diff = dopant_charge - info['charge']
        radius_diff = dopant_radius - info['radius']
        compat = 1.0 / (1.0 + abs(radius_diff) + abs(charge_diff) * 0.5)
        rec = {
            'site_name': site_name, 'host': info['host'],
            'host_charge': info['charge'], 'host_radius': info['radius'],
            'wyckoff': info['wyckoff'], 'env': info['env'],
            'charge_diff': charge_diff, 'radius_diff': round(radius_diff, 3),
            'compatibility_score': round(compat, 3), 'source': source,
        }
        if evidence:
            rec['evidence'] = evidence
        if ref:
            rec['reference'] = ref
        return rec

    candidates = []
    seen = set()

    # (0) Literature-reported sites — admit regardless of RADIUS_TOL (cutoff is a
    #     fallback, not a gate). Weak evidence (e.g. 'rietveld') still generated so
    #     the downstream UMA/DFT can confirm or refute it by energy.
    for site_name, (evidence, ref) in KNOWN_SUBSTITUTIONS.get(element, {}).items():
        if site_name not in HOST_SITES:
            continue
        if dopant_charge * HOST_SITES[site_name]['charge'] <= 0:
            continue  # sign sanity only
        candidates.append(_make(site_name, HOST_SITES[site_name],
                                'literature', evidence, ref))
        seen.add(site_name)

    # (1)-(3) Radius/charge heuristic for the remaining sites.
    for site_name, info in HOST_SITES.items():
        if site_name in seen:
            continue
        if dopant_charge * info['charge'] <= 0:          # (1) charge sign match
            continue
        charge_diff = dopant_charge - info['charge']
        if (not allow_aliovalent) and (charge_diff != 0):  # (2) isovalent-only
            continue
        if abs(dopant_radius - info['radius']) > RADIUS_TOL[site_name]:  # (3) radius
            continue
        candidates.append(_make(site_name, info, 'heuristic'))

    # literature sites first (documented), then heuristic; each by score desc
    candidates.sort(key=lambda x: (x['source'] != 'literature',
                                   -x['compatibility_score']))
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
    sites = site_preference_filter(d['charge'], d['radius'], element=element)
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
    parser.add_argument('--all', action='store_true',
                       help='Screen every element in DOPANT_DB (skip Li/P/S/Cl host)')
    parser.add_argument('--list', action='store_true', help='List known dopants')
    parser.add_argument('--validate', action='store_true',
                       help='Validate RADIUS_TOL against literature VALIDATION_SET')
    parser.add_argument('--out', default=None, help='Save results to JSON')
    parser.add_argument('--quiet', action='store_true',
                       help='Suppress per-dopant verbose table')
    args = parser.parse_args()

    if args.list:
        print("Known dopants in DOPANT_DB:")
        for e, info in DOPANT_DB.items():
            print(f"  {e:<6} charge={info['charge']:+d} radius={info['radius']} Å")
        return

    if args.validate:
        n_mismatch = validate_against_literature()
        raise SystemExit(0 if n_mismatch == 0 else 1)

    results = []
    if args.all:
        host_elements = {'Li', 'P', 'S', 'Cl', 'P_anion'}
        elements = [e for e in DOPANT_DB if e not in host_elements]
        for e in elements:
            results.append(evaluate_dopant(e, n_dopants=args.n,
                                          verbose=not args.quiet))
    elif args.batch:
        elements = json.loads(Path(args.batch).read_text())
        for e in elements:
            results.append(evaluate_dopant(e, n_dopants=args.n,
                                          verbose=not args.quiet))
    elif args.dopant:
        results.append(evaluate_dopant(args.dopant, n_dopants=args.n,
                                       verbose=not args.quiet))
    else:
        parser.print_help()
        return

    # Summary table
    print(f"\n{'='*70}")
    print(f"{'Dopant':<8}{'#sites':<8}{'best site':<12}{'best score':<12}")
    print('-' * 70)
    for r in results:
        sites = r.get('compatible_sites', [])
        if sites:
            best = sites[0]
            print(f"{r['element']:<8}{len(sites):<8}"
                  f"{best['site_name']:<12}{best['compatibility_score']:<12.3f}")
        else:
            print(f"{r['element']:<8}{'0':<8}{'(none)':<12}{'-':<12}")
    print(f"\nTotal: {sum(1 for r in results if r.get('compatible_sites'))} / "
          f"{len(results)} dopants have ≥1 compatible site.")

    if args.out:
        Path(args.out).write_text(json.dumps(results, indent=2))
        print(f"\nSaved {len(results)} results to {args.out}")


if __name__ == '__main__':
    main()
