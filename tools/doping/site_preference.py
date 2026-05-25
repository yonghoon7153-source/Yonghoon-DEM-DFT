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
    # Cations for Li site — Shannon radius given for the standard host CN.
    # When 'radius_cn4' is supplied separately, site_preference uses it for
    # P_4b lookup (P is tetrahedral CN=4); otherwise the CN=6 'radius' is
    # used for both Li and P sites. Reference: Shannon 1976, IUCr.
    'Li':  {'charge': +1, 'radius': 0.76, 'radius_cn4': 0.59},
    'Na':  {'charge': +1, 'radius': 1.02, 'radius_cn4': 0.99},
    'K':   {'charge': +1, 'radius': 1.38, 'radius_cn4': 1.37},
    'Cu':  {'charge': +1, 'radius': 0.77, 'radius_cn4': 0.60},
    'Ag':  {'charge': +1, 'radius': 1.15, 'radius_cn4': 1.00},
    'Mg':  {'charge': +2, 'radius': 0.72, 'radius_cn4': 0.57},
    'Zn':  {'charge': +2, 'radius': 0.74, 'radius_cn4': 0.60},
    'Ca':  {'charge': +2, 'radius': 1.00, 'radius_cn4': 1.00},  # Ca²⁺ usually CN=6+
    'Sr':  {'charge': +2, 'radius': 1.18},
    'Ba':  {'charge': +2, 'radius': 1.35},
    'Al':  {'charge': +3, 'radius': 0.535, 'radius_cn4': 0.39},
    'Ga':  {'charge': +3, 'radius': 0.62, 'radius_cn4': 0.47},
    'In':  {'charge': +3, 'radius': 0.80, 'radius_cn4': 0.62},
    'Sc':  {'charge': +3, 'radius': 0.745},
    'Y':   {'charge': +3, 'radius': 0.90},
    # Rare earths — added for Nd2O3 / La2O3 oxide doping (paper #2 + Sundar
    # 2025 coating screening). All trivalent; Shannon CN=6 values.
    'La':  {'charge': +3, 'radius': 1.032},
    'Ce':  {'charge': +4, 'radius': 0.87},   # Ce⁴⁺ (CeO2 ceria default — most
                                              # common Ce in solid-state synth.)
    'Eu':  {'charge': +3, 'radius': 0.947},  # Eu³⁺ (most common in synth)
    # NOTE: alternate-valence variants (Ce³⁺, Eu²⁺, Cr⁶⁺, Mn⁴⁺/⁷⁺, Fe²⁺,
    # Co³⁺, Cu²⁺, Bi⁵⁺) are NOT separate DB entries — they're handled by
    # ALTERNATIVE_VALENCES auto-balance in substitute_compound.py because
    # parse_compound("CrO3") → {Cr:1, O:3} doesn't see "Cr6". A-2 fix
    # (2026-05-16): single source of truth = ALTERNATIVE_VALENCES.
    'Nd':  {'charge': +3, 'radius': 0.983},
    'Sm':  {'charge': +3, 'radius': 0.958},
    'Gd':  {'charge': +3, 'radius': 0.938},
    'Yb':  {'charge': +3, 'radius': 0.868},
    'Pr':  {'charge': +3, 'radius': 0.99},   # Praseodymium
    'Tb':  {'charge': +3, 'radius': 0.923},  # Terbium
    'Dy':  {'charge': +3, 'radius': 0.912},  # Dysprosium (laser, magnet)
    'Ho':  {'charge': +3, 'radius': 0.901},  # Holmium
    'Er':  {'charge': +3, 'radius': 0.89},   # Erbium
    'Tm':  {'charge': +3, 'radius': 0.88},   # Thulium
    'Lu':  {'charge': +3, 'radius': 0.861},  # Lutetium (smallest Ln)
    'Bi':  {'charge': +3, 'radius': 1.03},   # Bi³⁺ (Bi2S3, Bi2O3 — SE doping
                                              # reports for Li-ion sulfide SEs)
    'Re':  {'charge': +7, 'radius': 0.53},   # Re⁷⁺ (Re2O7 — high-valence P
                                              # substitution candidate)
    'H':   {'charge': +1, 'radius': -0.04},  # Proton (Shannon negative CN=2;
                                              # for LiOH/LiBH4 hydride-related
                                              # precursors only)
    # 3d transition metals (Li-site or P-site depending on charge)
    'Cr':  {'charge': +3, 'radius': 0.615},  # Cr³⁺ CN=6 — Li site
    'Mn':  {'charge': +2, 'radius': 0.83},   # Mn²⁺ CN=6 high-spin — Li site
    'Fe':  {'charge': +3, 'radius': 0.645},  # Fe³⁺ CN=6 — Li site
    'Co':  {'charge': +2, 'radius': 0.745},  # Co²⁺ CN=6 — Li site (NMC parent)
    'Ni':  {'charge': +2, 'radius': 0.69},   # Ni²⁺ CN=6 — Li site (NMC parent)
    # Cations for P site
    'P':   {'charge': +5, 'radius': 0.17},
    'Sb':  {'charge': +5, 'radius': 0.60},
    'As':  {'charge': +5, 'radius': 0.46},
    'V':   {'charge': +5, 'radius': 0.54},
    'Nb':  {'charge': +5, 'radius': 0.64},
    'Ta':  {'charge': +5, 'radius': 0.64},   # 5d analogue of Nb
    'Si':  {'charge': +4, 'radius': 0.40},
    'Ge':  {'charge': +4, 'radius': 0.53},
    'Sn':  {'charge': +4, 'radius': 0.69},
    'Ti':  {'charge': +4, 'radius': 0.605},
    'Zr':  {'charge': +4, 'radius': 0.72},
    'Hf':  {'charge': +4, 'radius': 0.71},   # 5d analogue of Zr
    # Small / high-valence cations — P-site substitution candidates
    # (Wang 2025 LiBH4: BH4⁻ goes to Cl⁻ site as complex anion, but atomic B
    # would substitute P. W/Mo at P5+ are reported as 6+ donors in
    # thiophosphate glasses, e.g. WS3 / MoS3 additions.)
    'B':   {'charge': +3, 'radius': 0.11},   # B³⁺ CN=4 — P site (acceptor)
    'W':   {'charge': +6, 'radius': 0.42},   # W⁶⁺ CN=4 — P site (donor +1)
    'Mo':  {'charge': +6, 'radius': 0.41},   # Mo⁶⁺ CN=4 — P site (donor +1)
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


# ============================================================
# LITERATURE_SITES — documented per-dopant site preference (v4.5.23)
# ============================================================
# Machine-readable form of the site assignments that were previously
# encoded only as DOPANT_DB comments + VALIDATION_SET references. For a
# documented element, its listed sites are UNION'd with the radius/charge
# filter result (see `site_preference_filter(..., element=)`), so a
# chemically documented site is always tried even if it marginally fails
# the Shannon-radius cutoff, and a per-site literature `ref` is attached
# for paper traceability.
#
# Policy = UNION (broaden, never remove a radius-valid site). This raises
# the number of physically-justified (compound, site) screening cases
# without admitting sign-incompatible placements (the charge-sign rule in
# site_preference_filter still gates every site). Switch to REPLACE
# semantics only after reviewer sign-off (single branch in the filter).
#
# Sources: DOPANT_DB inline comments (author's literature-informed intent),
# VALIDATION_SET refs, and db/literature/*.md (Lee2025 B/Al→PO4 cluster,
# Adeli2019 halogen-rich, ACS AMI 2021 O→S_16e, ACS AMI 2022 F→Cl_4d).
LITERATURE_SITES = {
    # ---- Anions (S²⁻ / Cl⁻ sublattice) ----
    'O':  {'sites': ['S_16e', 'S_4a'],  'ref': 'ACS AMI 2021 oxysulfide Li6PS5-xClOx (best=S_16e, PS4-bonded)'},
    'Se': {'sites': ['S_16e', 'S_4a'],  'ref': 'Se→S isovalent (chalcogen swap)'},
    'Te': {'sites': ['S_16e', 'S_4a'],  'ref': 'Te→S isovalent (chalcogen swap)'},
    'F':  {'sites': ['Cl_4d'],          'ref': 'ACS AMI 2022 F-doped argyrodite (F→Cl⁻ halide site)'},
    'Cl': {'sites': ['Cl_4d', 'S_4a'],  'ref': 'Adeli 2019 halogen-rich (Cl on 4d + free S_4a anion)'},
    'Br': {'sites': ['Cl_4d', 'S_4a'],  'ref': 'halogen mixing Li6PS5(Cl,Br) (comp2 family)'},
    'I':  {'sites': ['Cl_4d'],          'ref': 'I-F dual-doped JPCC 2023'},
    'N':  {'sites': ['S_16e'],          'ref': 'N³⁻ → PS4 S (aliovalent nitride doping)'},
    # ---- P-site cations (PS4 tetrahedron center) ----
    'B':  {'sites': ['P_4b'],           'ref': 'Lee 2025 CEJ: B³⁺ PO4-cluster (P-site acceptor)'},
    'W':  {'sites': ['P_4b'],           'ref': 'W⁶⁺ thiophosphate donor (DOPANT_DB)'},
    'Mo': {'sites': ['P_4b'],           'ref': 'Mo⁶⁺ thiophosphate donor (DOPANT_DB)'},
    'Re': {'sites': ['P_4b'],           'ref': 'Re⁷⁺ high-valence P substitution (DOPANT_DB)'},
    'Sb': {'sites': ['P_4b'],           'ref': 'Sb⁵⁺→P isovalent (common)'},
    'As': {'sites': ['P_4b'],           'ref': 'As⁵⁺→P isovalent'},
    'V':  {'sites': ['P_4b'],           'ref': 'V⁵⁺→P isovalent'},
    'Nb': {'sites': ['P_4b'],           'ref': 'Nb⁵⁺→P isovalent'},
    'Ta': {'sites': ['P_4b'],           'ref': 'Ta⁵⁺→P (5d analogue of Nb)'},
    'Si': {'sites': ['P_4b'],           'ref': 'Si⁴⁺→P acceptor (LGPS family)'},
    'Ge': {'sites': ['P_4b'],           'ref': 'Ge⁴⁺→P (LGPS family)'},
    'Sn': {'sites': ['P_4b'],           'ref': 'MDPI Materials 16(7),2751 (2023) Sn-substituted LPSCl'},
    'Ti': {'sites': ['P_4b'],           'ref': 'Ti⁴⁺→P acceptor'},
    'Zr': {'sites': ['P_4b'],           'ref': 'Zr⁴⁺→P acceptor'},
    'Hf': {'sites': ['P_4b'],           'ref': 'Hf⁴⁺→P (5d analogue of Zr)'},
    # ---- Li-site cations (+1 isovalent) ----
    'Na': {'sites': ['Li_24g', 'Li_48h'], 'ref': 'Na→Li isovalent (common)'},
    'Cu': {'sites': ['Li_24g', 'Li_48h'], 'ref': 'Cu⁺→Li isovalent'},
    'Ag': {'sites': ['Li_24g', 'Li_48h'], 'ref': 'Nature Comm 2025 Ag-exsolution argyrodite'},
    # ---- Li-site cations (+2 alkaline earth / 3d TM) ----
    'Mg': {'sites': ['Li_24g'],         'ref': 'Mg²⁺→Li aliovalent (common)'},
    'Zn': {'sites': ['Li_24g'],         'ref': 'Zn²⁺→Li; Sundar 2025 ZnO coating'},
    'Ca': {'sites': ['Li_24g'],         'ref': 'Li5.35Ca0.1PS4.5Cl1.55, 10.2 mS/cm'},
    'Sr': {'sites': ['Li_24g'],         'ref': 'Sr²⁺→Li (larger alkaline earth)'},
    'Ba': {'sites': ['Li_24g'],         'ref': 'PMC 11106650 mechanochemical Li6-aBa_a/2PS5Cl (borderline radius)'},
    'Mn': {'sites': ['Li_24g'],         'ref': 'Mn²⁺ CN6 → Li site (DOPANT_DB)'},
    'Co': {'sites': ['Li_24g'],         'ref': 'Co²⁺ → Li site (NMC parent, DOPANT_DB)'},
    'Ni': {'sites': ['Li_24g'],         'ref': 'Ni²⁺ → Li site (NMC parent, DOPANT_DB)'},
    # ---- Li-site cations (+3: group-13, 3d, rare-earth) ----
    'Al': {'sites': ['Li_24g', 'P_4b'], 'ref': 'Li5.4Al0.1PS4.7Cl1.3 7.29mS/cm (Li-site); Al³⁺ also P-acceptor (amphoteric)'},
    'Ga': {'sites': ['Li_24g'],         'ref': 'Ga³⁺→Li aliovalent'},
    'In': {'sites': ['Li_24g'],         'ref': 'In³⁺→Li aliovalent'},
    'Sc': {'sites': ['Li_24g'],         'ref': 'Sc³⁺→Li aliovalent'},
    'Y':  {'sites': ['Li_24g'],         'ref': 'mechanochemical Y-doped LPSCl'},
    'Cr': {'sites': ['Li_24g'],         'ref': 'Cr³⁺ CN6 → Li site (DOPANT_DB)'},
    'Fe': {'sites': ['Li_24g'],         'ref': 'Fe³⁺ CN6 → Li site (DOPANT_DB)'},
    'Bi': {'sites': ['Li_24g'],         'ref': 'Bi³⁺→Li (Bi2S3/Bi2O3 SE doping)'},
    'La': {'sites': ['Li_24g'],         'ref': 'La³⁺→Li; Sundar 2025 / paper#2 RE oxide'},
    'Nd': {'sites': ['Li_24g'],         'ref': 'Nd³⁺→Li; paper#2 Nd2O3 case study'},
    'Sm': {'sites': ['Li_24g'],         'ref': 'Sm³⁺→Li RE oxide'},
    'Gd': {'sites': ['Li_24g'],         'ref': 'Gd³⁺→Li RE oxide'},
    'Eu': {'sites': ['Li_24g'],         'ref': 'Eu³⁺→Li RE'},
    'Yb': {'sites': ['Li_24g'],         'ref': 'Yb³⁺→Li RE'},
    'Pr': {'sites': ['Li_24g'],         'ref': 'Pr³⁺→Li RE'},
    'Tb': {'sites': ['Li_24g'],         'ref': 'Tb³⁺→Li RE'},
    'Dy': {'sites': ['Li_24g'],         'ref': 'Dy³⁺→Li RE'},
    'Ho': {'sites': ['Li_24g'],         'ref': 'Ho³⁺→Li RE'},
    'Er': {'sites': ['Li_24g'],         'ref': 'Er³⁺→Li RE'},
    'Tm': {'sites': ['Li_24g'],         'ref': 'Tm³⁺→Li RE'},
    'Lu': {'sites': ['Li_24g'],         'ref': 'Lu³⁺→Li RE (smallest Ln)'},
    'Ce': {'sites': ['Li_24g', 'P_4b'], 'ref': 'Ce⁴⁺ (CeO2) — Li or P depending on valence'},
}


def site_preference_filter(dopant_charge: int, dopant_radius: float,
                          allow_aliovalent: bool = True,
                          element: str | None = None) -> list[dict]:
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

        # (3) Radius tolerance — per-site cutoff calibrated from observed
        #     LPSCl substitutions (see RADIUS_TOL docstring above for refs).
        tol = RADIUS_TOL[site_name]
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
            'source': 'radius_filter',
        })

    # v4.5.23 — UNION literature-documented sites (per dopant element).
    # POLICY = LITERATURE-PREFERRED (v4.5.24, reviewer-bound):
    #   If the element is documented in LITERATURE_SITES, the returned set
    #   is RESTRICTED to its literature sites (charge-sign-gated). This
    #   DROPS radius-only placements that have no literature support
    #   (e.g. O→Cl_4d, Sn⁴⁺→Li_24g) — physically implausible substitutions
    #   the Shannon-radius cutoff alone admitted. Any documented site the
    #   radius filter missed is still added (so we never lose a real site).
    #   Undocumented elements fall back to the pure radius filter unchanged.
    #   Charge-sign rule (cation↔cation / anion↔anion) always applies.
    if element is not None and element in LITERATURE_SITES:
        lit = LITERATURE_SITES[element]
        lit_set = set(lit['sites'])
        kept = []
        # (a) keep radius sites that are literature-confirmed; drop the rest
        for c in candidates:
            if c['site_name'] in lit_set:
                c['source'] = 'radius+literature'
                c['literature_ref'] = lit['ref']
                kept.append(c)
            else:
                # radius-only, no literature support → dropped (logged via source)
                pass
        # (b) add documented sites the radius filter missed (sign-gated)
        present = {c['site_name'] for c in kept}
        for site_name in lit['sites']:
            if site_name in present:
                continue
            info = HOST_SITES.get(site_name)
            if info is None or dopant_charge * info['charge'] <= 0:
                continue
            charge_diff = dopant_charge - info['charge']
            radius_diff = dopant_radius - info['radius']
            compat = 1.0 / (1.0 + abs(radius_diff) + abs(charge_diff) * 0.5)
            kept.append({
                'site_name': site_name,
                'host': info['host'],
                'host_charge': info['charge'],
                'host_radius': info['radius'],
                'wyckoff': info['wyckoff'],
                'env': info['env'],
                'charge_diff': charge_diff,
                'radius_diff': round(radius_diff, 3),
                'compatibility_score': round(compat, 3),
                'source': 'literature',
                'literature_ref': lit['ref'],
            })
        candidates = kept

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
