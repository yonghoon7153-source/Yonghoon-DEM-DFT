#!/usr/bin/env python3
"""
Core DEM analysis functions.
Used by both analyze_contacts.py and analyze_contacts_bimodal.py.

Scale convention (LIGGGHTS units si: m, kg, s, N, Pa):
  DEM scaling: R×1000, E÷1000 → k preserved, δ×1000, F×1000, P÷1000
  - Length: real(μm) = sim(m) / SCALE × 1e6    → ÷SCALE for real, ×1e6 for μm
  - Area:   real(μm²) = sim(m²) / SCALE² × 1e12  (equivalently: sim × SCALE²)
  - Force:  real(N) = sim(N) / SCALE             → real(μN) = sim × SCALE
  - Pressure: real(Pa) = sim(Pa) × SCALE         → real(MPa) = sim × SCALE / 1e6
"""
import numpy as np
import json
import os
from collections import defaultdict
import networkx as nx


# ─── Shape factor (B3 patch) ──────────────────────────────────────────────
# Roughness/non-sphericity factor: real surface area = factor × 4πr²
# Polycrystalline NCM: secondary particle is an aggregate of primaries, so the
# accessible surface is ~40% larger than a perfect sphere (Quinn 2020, Lim 2017).
# Single-crystal NCM is closer to a faceted sphere (Liu 2020, Wang 2022).
# Quenched-glass SE is near-spherical with mild surface roughness (Sakuda 2013).
SHAPE_FACTOR = {
    'AM_P': 1.40,   # polycrystalline secondary
    'AM_S': 1.10,   # single crystal
    'SE':   1.05,   # quenched glass
}


# ─── Porosity & Thickness ──────────────────────────────────────────────────

def calc_porosity(atoms, plate_z, box_xy=0.05):
    """
    Porosity = 1 - V_solid / V_box (sphere-sum convention, current production)
    V_box uses mesh plate_z (= actual electrode thickness).
    All in sim units.
    """
    V_solid = sum(4/3 * np.pi * a['radius']**3 for a in atoms.values())
    V_box = box_xy * box_xy * plate_z
    porosity = (1 - V_solid / V_box) * 100
    return porosity


def calc_porosity_dual(atoms, contacts, plate_z, box_xy=0.05):
    """Multiple porosity definitions for full diagnostic (Stage 2026-06-03).

    Returns dict with:
      porosity_spheresum   : 1 - N×V_sphere / V_box     (current production method)
      porosity_union       : 1 - V_union / V_box        (overlap-corrected, literature)
      overlap_fraction_pct : V_lens / V_sphere_sum × 100  (plastic deformation indicator)

    V_lens computed from each contact's delta (overlap depth).
    For equal-radius spheres: V_lens = π × δ² × (6r - δ) / 12
    For unequal: more general formula (used when r1 ≠ r2).

    Used to expose:
      - Real geometric ε (union) for literature comparison
      - Plastic compaction extent via overlap fraction
      - Both stored alongside legacy 'porosity' field for backward compat.
    """
    # Sphere-sum (legacy)
    V_sphere_sum = sum(4/3 * np.pi * a['radius']**3 for a in atoms.values())
    V_box = box_xy * box_xy * plate_z
    eps_spheresum = (1 - V_sphere_sum / V_box) * 100

    # Lens volume from contacts (overlap-corrected union)
    V_lens_total = 0.0
    for c in contacts:
        # contacts may be list of dict or list of dict-like
        delta = c.get('delta') if isinstance(c, dict) else getattr(c, 'delta', None)
        id1 = c.get('id1') if isinstance(c, dict) else getattr(c, 'id1', None)
        id2 = c.get('id2') if isinstance(c, dict) else getattr(c, 'id2', None)
        if delta is None or delta <= 0:
            continue
        if id1 in atoms and id2 in atoms:
            r1 = atoms[id1]['radius']
            r2 = atoms[id2]['radius']
        else:
            # Fallback: use mean radius (all same for monodisperse)
            r1 = r2 = next(iter(atoms.values()))['radius']
        # Two-sphere lens volume:
        # V_lens = (π × δ² × (3(r1+r2) - δ)) / 12 × correction
        # Simpler: for equal r, V_lens = π δ² (6r - δ) / 12
        # For unequal, use general formula with d = r1+r2-δ
        d = r1 + r2 - delta
        if d <= 0: continue
        # General two-sphere intersection lens volume:
        V_lens = (np.pi * delta**2 / (12 * d)) * (
            d**2 + 2*d*(r1 + r2) - 3*(r1 - r2)**2
        )
        if V_lens > 0:
            V_lens_total += V_lens

    V_union = V_sphere_sum - V_lens_total
    eps_union = (1 - V_union / V_box) * 100
    overlap_pct = (V_lens_total / V_sphere_sum * 100) if V_sphere_sum > 0 else 0.0

    return {
        'porosity_spheresum': eps_spheresum,           # legacy = current production
        'porosity_union': eps_union,                    # overlap-corrected (literature)
        'overlap_fraction_pct': overlap_pct,            # plastic deformation indicator
        'V_sphere_sum_sim': V_sphere_sum,
        'V_lens_total_sim': V_lens_total,
        'V_box_sim': V_box,
    }


def get_plate_z(results_dir, atoms, scale):
    """Get plate_z from mesh_info.json, or estimate from atoms.
    Fallback: max of particle CENTERS (no +radius). Adding the radius on top
    of the highest center overshoots the actual plate plane, which in turn
    makes z_top = plate_z - r_se×boundary_factor land ABOVE every SE center.
    That silently empties top_se → percolation falsely = 0 for thick
    electrodes that lack mesh_info.json (observed for results/260418_165025_e7453f,
    input_9, etc. at ~4/20 16:45).
    """
    mesh_file = os.path.join(results_dir, 'mesh_info.json')
    if os.path.exists(mesh_file):
        with open(mesh_file) as f:
            info = json.load(f)
        return info['plate_z'], 'mesh'
    z_max = max(a['z'] for a in atoms.values())
    return z_max, 'estimated_center'


# ─── Interface Area ────────────────────────────────────────────────────────

def calc_interface_area(atoms, contacts, type_map, scale):
    """
    Contact area by type. Returns dict with real μm² values.
    contactArea (sim m²) → real μm² = sim / scale² × 1e12
    """
    area_conv = 1.0 / (scale ** 2) * 1e12  # sim m² → real μm²
    ca = defaultdict(float)
    cc = defaultdict(int)

    for c in contacts:
        if c['id1'] in atoms and c['id2'] in atoms:
            t1 = type_map.get(atoms[c['id1']]['type'], '?')
            t2 = type_map.get(atoms[c['id2']]['type'], '?')
            ct = '-'.join(sorted([t1, t2]))
            ca[ct] += c['contact_area']
            cc[ct] += 1

    result = {}
    for ct in ca:
        result[ct] = {
            'total_area': ca[ct] * area_conv,
            'n_contacts': cc[ct],
            'mean_area': (ca[ct] / cc[ct]) * area_conv if cc[ct] > 0 else 0,
        }

    # AM_total-SE
    am_se_total = sum(v['total_area'] for k, v in result.items()
                      if 'SE' in k and k != 'SE-SE')
    am_se_n = sum(v['n_contacts'] for k, v in result.items()
                  if 'SE' in k and k != 'SE-SE')
    result['AM전체-SE'] = {
        'total_area': am_se_total,
        'n_contacts': am_se_n,
        'mean_area': am_se_total / am_se_n if am_se_n > 0 else 0,
    }

    return result


# ─── Coverage ──────────────────────────────────────────────────────────────

def calc_coverage(atoms, contacts, type_map, scale, apply_shape_factor=False):
    """
    Coverage = SE접촉면적 / (전체표면적 - AM-AM접촉면적) per AM particle.
    Returns per-type mean, std, min, max.

    apply_shape_factor: if True, multiply 4πr² by SHAPE_FACTOR[label] to
    account for surface roughness / non-sphericity (B3 patch).
    """
    am_types = [k for k, v in type_map.items() if 'AM' in v]
    se_types = [k for k, v in type_map.items() if v == 'SE']

    am_surf = {}
    am_se_area = defaultdict(float)
    am_am_area = defaultdict(float)

    for aid, a in atoms.items():
        if a['type'] in am_types:
            lbl = type_map.get(a['type'], '')
            factor = SHAPE_FACTOR.get(lbl, 1.0) if apply_shape_factor else 1.0
            am_surf[aid] = factor * 4 * np.pi * a['radius']**2

    for c in contacts:
        if c['id1'] not in atoms or c['id2'] not in atoms:
            continue
        t1, t2 = atoms[c['id1']]['type'], atoms[c['id2']]['type']

        if t1 in am_types and t2 in se_types:
            am_se_area[c['id1']] += c['contact_area']
        elif t2 in am_types and t1 in se_types:
            am_se_area[c['id2']] += c['contact_area']

        if t1 in am_types and t2 in am_types:
            am_am_area[c['id1']] += c['contact_area']
            am_am_area[c['id2']] += c['contact_area']

    result = {}
    for lbl in set(type_map.values()):
        if 'AM' not in lbl:
            continue
        tids = [k for k, v in type_map.items() if v == lbl]
        covs = []
        for aid, a in atoms.items():
            if a['type'] in tids:
                free = am_surf.get(aid, 0) - am_am_area.get(aid, 0)
                se = am_se_area.get(aid, 0)
                covs.append(min(se / free * 100, 100) if free > 0 else 0)
        if covs:
            covs = np.array(covs)
            result[lbl] = {
                'mean': float(np.mean(covs)),
                'std': float(np.std(covs)),
                'min': float(np.min(covs)),
                'max': float(np.max(covs)),
                'n': len(covs),
            }
    return result


# ─── SE-SE Coordination Number ─────────────────────────────────────────────

def calc_se_se_cn(atoms, contacts, se_types, perc_set=None, scale=1000.0,
                   h_spread_sim=0.0):
    """SE-SE coordination number + F2 area-weighted + F1 plastic-augmented variants.

    perc_set: optional set of percolating SE ids. When provided, additional
    "_perc" metrics are computed restricted to that subpopulation.

    h_spread_sim: lateral-spread distance (sim units) for the F1 plastic-
    augmented CN. Pairs whose surface-to-surface gap is ≤ h_spread_sim are
    counted as "would-touch under plastic flow". A typical choice is
    h_spread_sim = 2 × h_film_min × scale = 10 nm × 1000 = 0.01 mm sim
    (i.e. ~1% of D=1 μm SE radius). Set 0 to disable F1.

    Returns:
      mean, std, ge2_pct      — all-SE plain CN (existing)
      cn_eff_area             — Σ A_contact / Σ (4π r²)  surface-fraction
                                 covered by SE-SE contacts (NEW — F2)
      mean_perc, cn_eff_area_perc — same restricted to perc_set (NEW — F2)
      mean_aug, n_extra_aug   — F1 augmented (LIGGGHTS contacts + near-miss
                                 pairs within h_spread_sim). Only populated
                                 when h_spread_sim > 0.
    """
    cn = defaultdict(int)
    cn_area = defaultdict(float)   # per-SE total contact area (sim m²)
    for c in contacts:
        if c['id1'] in atoms and c['id2'] in atoms:
            if atoms[c['id1']]['type'] in se_types and atoms[c['id2']]['type'] in se_types:
                cn[c['id1']] += 1
                cn[c['id2']] += 1
                a = float(c.get('contact_area', 0) or 0)
                cn_area[c['id1']] += a
                cn_area[c['id2']] += a

    se_ids = [aid for aid, a in atoms.items() if a['type'] in se_types]
    values = np.array([cn.get(aid, 0) for aid in se_ids])

    # Surface-fraction (CN_eff_area): Σ A_contact / Σ surface
    # Both numerator and denominator in sim m² → ratio is dimensionless.
    surf_total = sum(4 * np.pi * atoms[aid]['radius'] ** 2 for aid in se_ids)
    contact_total = sum(cn_area.get(aid, 0) for aid in se_ids)
    cn_eff_area = float(contact_total / surf_total) if surf_total > 0 else 0.0

    out = {
        'mean': float(np.mean(values)) if len(values) else 0.0,
        'std': float(np.std(values)) if len(values) else 0.0,
        'ge2_pct': float(np.sum(values >= 2) / len(values) * 100) if len(values) > 0 else 0,
        'cn_eff_area': cn_eff_area,
    }

    # F2: percolating-only metrics (when perc_set provided)
    if perc_set is not None and len(perc_set) > 0:
        perc_ids = [aid for aid in se_ids if aid in perc_set]
        perc_values = np.array([cn.get(aid, 0) for aid in perc_ids])
        surf_perc = sum(4 * np.pi * atoms[aid]['radius'] ** 2 for aid in perc_ids)
        contact_perc = sum(cn_area.get(aid, 0) for aid in perc_ids)
        out['mean_perc']         = float(np.mean(perc_values)) if len(perc_values) else 0.0
        out['std_perc']          = float(np.std(perc_values)) if len(perc_values) else 0.0
        out['n_perc']            = int(len(perc_ids))
        out['cn_eff_area_perc']  = float(contact_perc / surf_perc) if surf_perc > 0 else 0.0

    # F1: plastic-augmented CN — pairs whose surface-to-surface gap is
    # ≤ h_spread_sim are counted as "would-touch under plastic flow".
    # Implemented with a uniform-grid neighbor search to avoid O(N²) over
    # the full SE population; only pairs whose centers are within
    # (r_i + r_j + h_spread_sim) of each other are tested.
    if h_spread_sim > 0 and se_ids:
        # Cell size: max diameter + h_spread covers all candidate pairs.
        r_max = max(atoms[aid]['radius'] for aid in se_ids)
        cell = 2.0 * r_max + h_spread_sim
        if cell <= 0:
            return out
        from collections import defaultdict as _dd
        grid = _dd(list)
        for aid in se_ids:
            a = atoms[aid]
            grid[(int(a['x'] // cell), int(a['y'] // cell), int(a['z'] // cell))].append(aid)
        cn_aug = dict(cn)  # start from elastic CN counts
        n_extra = 0
        seen_pairs = set()
        for (cx, cy, cz), members in grid.items():
            # Inspect 3x3x3 neighbourhood — covers all pairs within `cell`.
            cands = []
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for dz in (-1, 0, 1):
                        cands.extend(grid.get((cx + dx, cy + dy, cz + dz), []))
            for i, aid_i in enumerate(members):
                ai = atoms[aid_i]
                for aid_j in cands:
                    if aid_j == aid_i:
                        continue
                    pair = (min(aid_i, aid_j), max(aid_i, aid_j))
                    if pair in seen_pairs:
                        continue
                    seen_pairs.add(pair)
                    aj = atoms[aid_j]
                    dx = ai['x'] - aj['x']; dy = ai['y'] - aj['y']; dz = ai['z'] - aj['z']
                    d = (dx * dx + dy * dy + dz * dz) ** 0.5
                    r_sum = ai['radius'] + aj['radius']
                    if d <= r_sum:
                        # Already an elastic contact — covered by `cn`.
                        continue
                    if d <= r_sum + h_spread_sim:
                        cn_aug[aid_i] = cn_aug.get(aid_i, 0) + 1
                        cn_aug[aid_j] = cn_aug.get(aid_j, 0) + 1
                        n_extra += 1
        aug_values = np.array([cn_aug.get(aid, 0) for aid in se_ids])
        out['mean_aug']    = float(np.mean(aug_values)) if len(aug_values) else 0.0
        out['std_aug']     = float(np.std(aug_values)) if len(aug_values) else 0.0
        out['n_extra_aug'] = int(n_extra)
        out['h_spread_sim'] = float(h_spread_sim)

    return out


def calc_am_am_cn(atoms, contacts, am_types, scale=1000.0):
    """AM-AM coordination number (for electronic percolation analysis).

    `scale` is sim→real length ratio (default 1000 for mm-scale sim / μm real).
    Contact areas are converted to μm² via area_conv = 1/scale² × 1e12.
    """
    cn = defaultdict(int)
    am_am_areas = []
    for c in contacts:
        if c['id1'] in atoms and c['id2'] in atoms:
            if atoms[c['id1']]['type'] in am_types and atoms[c['id2']]['type'] in am_types:
                cn[c['id1']] += 1
                cn[c['id2']] += 1
                am_am_areas.append(c.get('contact_area', 0))

    am_ids = [aid for aid, a in atoms.items() if a['type'] in am_types]
    if not am_ids:
        return {'mean': 0, 'std': 0, 'n_am': 0, 'n_contacts': 0, 'mean_area': 0}

    area_conv = 1.0 / (scale ** 2) * 1e12  # sim m² → real μm²
    values = np.array([cn.get(aid, 0) for aid in am_ids])
    return {
        'mean': float(np.mean(values)),
        'std': float(np.std(values)),
        'n_am': len(am_ids),
        'n_contacts': sum(values) // 2,
        'mean_area': float(np.mean(am_am_areas)) * area_conv if am_am_areas else 0,
        'total_area': float(np.sum(am_am_areas)) * area_conv if am_am_areas else 0,
    }


# ─── SE Percolation ────────────────────────────────────────────────────────

def calc_percolation(atoms, contacts, se_types, plate_z, boundary_factor=2.0, box_x=0.05, box_y=0.05):
    """
    SE-SE contact graph → percolation analysis.
    Boundary: bottom = z <= r_SE × boundary_factor, top = z >= plate_z - r_SE × boundary_factor
    """
    se_ids = [aid for aid, a in atoms.items() if a['type'] in se_types]
    if not se_ids:
        return {'se_count': 0, 'percolation_pct': 0, 'top_reachable_pct': 0,
                'n_components': 0, 'largest_pct': 0,
                'top_reachable_se': set(), 'bottom_se': set(), 'top_se': set(), 'graph': nx.Graph()}

    # ── C4 patch: per-particle plate-contact test ───────────────────────
    # Each particle judged by its OWN radius — no global threshold.
    # boundary_factor=2.0 keeps prior behavior: center within 1 radius of
    # the plate. r_SE-independent → fair across D0.5 vs D1.5 cases.
    G = nx.Graph()
    G.add_nodes_from(se_ids)
    for c in contacts:
        if c['id1'] in atoms and c['id2'] in atoms:
            if atoms[c['id1']]['type'] in se_types and atoms[c['id2']]['type'] in se_types:
                # Add edge with periodic-corrected distance as weight
                d = _periodic_dist(atoms[c['id1']], atoms[c['id2']], box_x, box_y)
                G.add_edge(c['id1'], c['id2'], distance=d)

    bottom_se = {aid for aid in se_ids
                 if atoms[aid]['z'] <= atoms[aid]['radius'] * boundary_factor}
    top_se = {aid for aid in se_ids
              if atoms[aid]['z'] >= plate_z - atoms[aid]['radius'] * boundary_factor}

    # Fallback L1: if boundary too strict, widen to 15% / 85% of plate_z
    if len(bottom_se) < 3 or len(top_se) < 3:
        z_bottom = plate_z * 0.15
        z_top = plate_z * 0.85
        bottom_se = {aid for aid in se_ids if atoms[aid]['z'] <= z_bottom}
        top_se = {aid for aid in se_ids if atoms[aid]['z'] >= z_top}

    # Fallback L2: if plate_z overshoots the actual particle range
    # (common when mesh_info.json is absent), anchor boundaries to the
    # observed SE z-range instead of plate_z. Without this, thick electrodes
    # silently report percolation=0% whenever plate_z ≠ actual top plane.
    if len(bottom_se) < 3 or len(top_se) < 3:
        z_vals = np.array([atoms[aid]['z'] for aid in se_ids])
        z_min_obs, z_max_obs = z_vals.min(), z_vals.max()
        span = z_max_obs - z_min_obs
        z_bottom = z_min_obs + span * 0.15
        z_top = z_max_obs - span * 0.15
        bottom_se = {aid for aid in se_ids if atoms[aid]['z'] <= z_bottom}
        top_se = {aid for aid in se_ids if atoms[aid]['z'] >= z_top}

    components = list(nx.connected_components(G))
    largest = max(len(c) for c in components) if components else 0
    n_large = sum(1 for c in components if len(c) >= 10)

    percolating_se = set()
    top_reachable_se = set()

    for comp in components:
        has_bottom = len(comp & bottom_se) > 0
        has_top = len(comp & top_se) > 0
        if has_bottom and has_top:
            percolating_se.update(comp)
        if has_top:
            top_reachable_se.update(comp)

    n = len(se_ids)
    return {
        'se_count': n,
        'percolation_pct': len(percolating_se) / n * 100,
        'top_reachable_pct': len(top_reachable_se) / n * 100,
        'n_components': len(components),
        'n_large_components': n_large,
        'largest_pct': largest / n * 100,
        'top_reachable_se': top_reachable_se,
        'percolating_se': percolating_se,   # F2: strictly bottom↔top percolating
        'bottom_se': bottom_se,
        'top_se': top_se,
        'graph': G,
    }


# ─── Tortuosity ────────────────────────────────────────────────────────────

def _periodic_dist(a1, a2, box_x=0.05, box_y=0.05):
    """Distance between two atoms with periodic boundary in x,y (NOT z)."""
    dx = abs(a1['x'] - a2['x']) % box_x  # wrap into primary cell first
    dy = abs(a1['y'] - a2['y']) % box_y
    dz = a1['z'] - a2['z']
    # Minimum image convention for periodic x,y
    dx = min(dx, box_x - dx)
    dy = min(dy, box_y - dy)
    return np.sqrt(dx**2 + dy**2 + dz**2)


def calc_tortuosity(atoms, perc_result, n_samples=200, box_xy=0.05, box_x=None, box_y=None):
    """tortuosity = path length / z distance.
    Uses distance-weighted shortest path (physical shortest distance)
    with periodic boundary correction.
    Sources = bottom boundary SE, Targets = top boundary SE (both percolating)."""
    if box_x is None:
        box_x = box_xy
    if box_y is None:
        box_y = box_xy
    G = perc_result['graph']
    top_reachable_se = perc_result['top_reachable_se']
    bottom_se = perc_result['bottom_se']
    top_se = perc_result['top_se']

    if not top_reachable_se:
        return {'mean': None, 'std': None, 'n_samples': 0}

    reach_top = list(top_se & top_reachable_se)
    if not reach_top:
        return {'mean': None, 'std': None, 'n_samples': 0}

    # Sources: bottom boundary SE that are in percolating components (connected to top)
    # This ensures z_dist ≈ electrode thickness → physically meaningful τ
    percolating_se = set()
    for comp in nx.connected_components(G):
        if (comp & bottom_se) and (comp & top_se):
            percolating_se |= comp
    src_candidates = list(bottom_se & percolating_se)

    # Fallback: if no bottom SE in percolating components, use lowest-z in each component
    if not src_candidates:
        for comp in nx.connected_components(G):
            comp_top_reach = comp & top_reachable_se
            if not comp_top_reach:
                continue
            lowest = min(comp_top_reach, key=lambda sid: atoms[sid]['z'])
            src_candidates.append(lowest)

    if not src_candidates:
        return {'mean': None, 'std': None, 'n_samples': 0}

    # Generate unique (src, tgt) pairs, shuffle for diverse sampling
    import random
    random.seed(42)
    pairs = [(s, t) for s in src_candidates for t in reach_top if s != t]
    random.shuffle(pairs)
    pairs = pairs[:n_samples]  # cap at n_samples

    taus = []
    for src, tgt in pairs:
        try:
            path = nx.shortest_path(G, src, tgt, weight='distance')
            path_len = sum(
                _periodic_dist(atoms[path[k]], atoms[path[k+1]], box_x, box_y)
                for k in range(len(path) - 1))
            z_dist = abs(atoms[tgt]['z'] - atoms[src]['z'])
            if z_dist > 0:
                tau_val = path_len / z_dist
                # Guard: τ must be >= 1.0 (path can't be shorter than z-distance)
                # and < 20 (physically unreasonable — likely bad src/tgt pair)
                if 1.0 <= tau_val < 20.0:
                    taus.append(tau_val)
        except nx.NetworkXNoPath:
            pass

    if not taus:
        return {'mean': None, 'median': None, 'std': None, 'n_samples': 0, 'use_median': False}

    t_mean = float(np.mean(taus))
    t_median = float(np.median(taus))
    t_std = float(np.std(taus)) if len(taus) > 1 else 0.0

    # Auto-select: use median if std/mean > 0.5 (high dispersion, outlier-dominated)
    use_median = t_std / t_mean > 0.5 if t_mean > 0 else False

    return {
        'mean': t_mean,
        'median': t_median,
        'std': t_std,
        'n_samples': len(taus),
        'use_median': use_median,
        'recommended': t_median if use_median else t_mean,
    }


# ─── Ionic Active AM ──────────────────────────────────────────────────────

def calc_ionic_active_am(atoms, contacts, perc_result, se_types, am_types, type_map):
    """
    Ionic Active AM = AM connected to SE that reaches top (SE pellet).
    """
    top_reachable_se = perc_result['top_reachable_se']
    am_ids = [aid for aid, a in atoms.items() if a['type'] in am_types]

    am_se_contacts = {}
    for c in contacts:
        if c['id1'] in atoms and c['id2'] in atoms:
            t1, t2 = atoms[c['id1']]['type'], atoms[c['id2']]['type']
            if t1 in am_types and t2 in se_types:
                am_se_contacts.setdefault(c['id1'], set()).add(c['id2'])
            elif t2 in am_types and t1 in se_types:
                am_se_contacts.setdefault(c['id2'], set()).add(c['id1'])

    ionic_active = set()
    ionic_dead = set()
    no_se = set()

    for aid in am_ids:
        if aid in am_se_contacts:
            if len(am_se_contacts[aid] & top_reachable_se) > 0:
                ionic_active.add(aid)
            else:
                ionic_dead.add(aid)
        else:
            no_se.add(aid)

    n_am = len(am_ids)
    result = {
        'n_am': n_am,
        'active_pct': len(ionic_active) / n_am * 100 if n_am > 0 else 0,
        'dead_pct': len(ionic_dead) / n_am * 100 if n_am > 0 else 0,
        'no_se_pct': len(no_se) / n_am * 100 if n_am > 0 else 0,
    }

    for lbl in set(type_map.values()):
        if 'AM' not in lbl:
            continue
        tids = [k for k, v in type_map.items() if v == lbl]
        sub = {aid for aid in am_ids if atoms[aid]['type'] in tids}
        sub_active = sub & ionic_active
        result[f'{lbl}_active_pct'] = len(sub_active) / len(sub) * 100 if sub else 0

    return result


# ─── Contact Force Distribution ───────────────────────────────────────────

def calc_contact_force_distribution(atoms, contacts, type_map, scale):
    """Normal force distribution by contact type. Returns stats in real units (μN)."""
    # DEM scaling: E_sim = E_real/scale, R_sim = R_real×scale → k preserved
    # δ_sim = δ_real × scale → F_sim = k×δ_sim = F_real × scale
    # F_real(N) = F_sim / scale,  F_real(μN) = F_sim × (1e6/scale) = F_sim × scale (for scale=1000)
    force_conv = 1e6 / scale  # sim(N) → real(μN)

    forces_by_type = defaultdict(list)
    for c in contacts:
        if c['id1'] in atoms and c['id2'] in atoms:
            t1 = type_map.get(atoms[c['id1']]['type'], '?')
            t2 = type_map.get(atoms[c['id2']]['type'], '?')
            ct = '-'.join(sorted([t1, t2]))
            fn = c.get('fn', 0) or np.sqrt(c.get('fn_x', 0)**2 + c.get('fn_y', 0)**2 + c.get('fn_z', 0)**2)
            forces_by_type[ct].append(fn * force_conv)

    result = {}
    for ct, forces in forces_by_type.items():
        f = np.array(forces)
        result[ct] = {
            'mean': float(np.mean(f)),
            'std': float(np.std(f)),
            'max': float(np.max(f)),
            'n': len(f),
        }
    return result


# ─── Contact Pressure ────────────────────────────────────────────────────

def calc_contact_pressure(atoms, contacts, type_map, scale):
    """Contact pressure = Fn / contact_area per contact. Returns stats in MPa."""
    # P_real = P_sim × scale (∵ E_sim = E_real/scale → σ_sim = σ_real/scale)
    # P_sim(Pa) = F_sim / A_sim,  P_real(Pa) = P_sim × scale
    # P_real(MPa) = F_sim / A_sim × scale / 1e6
    pressure_conv = scale / 1e6  # sim(Pa) → real(MPa)
    pressures_by_type = defaultdict(list)
    for c in contacts:
        if c['id1'] in atoms and c['id2'] in atoms:
            ca = c.get('contact_area', 0)
            if ca <= 0:
                continue
            t1 = type_map.get(atoms[c['id1']]['type'], '?')
            t2 = type_map.get(atoms[c['id2']]['type'], '?')
            ct = '-'.join(sorted([t1, t2]))
            fn = c.get('fn', 0) or np.sqrt(c.get('fn_x', 0)**2 + c.get('fn_y', 0)**2 + c.get('fn_z', 0)**2)
            pressure = fn / ca * pressure_conv  # real MPa
            pressures_by_type[ct].append(pressure)

    result = {}
    for ct, pressures in pressures_by_type.items():
        p = np.array(pressures)
        result[ct] = {
            'mean': float(np.mean(p)),
            'std': float(np.std(p)),
            'max': float(np.max(p)),
        }
    # Overall
    all_p = []
    for v in pressures_by_type.values():
        all_p.extend(v)
    if all_p:
        ap = np.array(all_p)
        result['overall'] = {
            'mean': float(np.mean(ap)),
            'std': float(np.std(ap)),
            'max': float(np.max(ap)),
        }
    return result


# ─── Overlap Ratio ────────────────────────────────────────────────────────

def calc_overlap_ratio(atoms, contacts):
    """δ/R ratio for each contact. High values (>5%) indicate DEM inaccuracy."""
    ratios = []
    for c in contacts:
        delta = abs(c.get('delta', 0))
        if delta <= 0:
            continue
        if c['id1'] in atoms and c['id2'] in atoms:
            r1 = atoms[c['id1']]['radius']
            r2 = atoms[c['id2']]['radius']
            r_eff = min(r1, r2)
            if r_eff > 0:
                ratios.append(delta / r_eff * 100)  # percentage

    if not ratios:
        return None
    r = np.array(ratios)
    return {
        'mean': float(np.mean(r)),
        'std': float(np.std(r)),
        'max': float(np.max(r)),
        'pct_above_5': float(np.sum(r > 5) / len(r) * 100),
    }


# ─── AM Isolation Risk ───────────────────────────────────────────────────

def calc_am_isolation_risk(atoms, contacts, type_map):
    """AM particles connected to only 1 SE = vulnerable (single point of failure).
    Returns aggregated AM-SE CN + per-AM-type breakdown (AM_P-SE, AM_S-SE) for bimodal.
    """
    am_types = [k for k, v in type_map.items() if 'AM' in v]
    se_types = [k for k, v in type_map.items() if v == 'SE']

    am_se_count = defaultdict(int)
    for c in contacts:
        if c['id1'] in atoms and c['id2'] in atoms:
            t1 = atoms[c['id1']]['type']
            t2 = atoms[c['id2']]['type']
            if t1 in am_types and t2 in se_types:
                am_se_count[c['id1']] += 1
            elif t2 in am_types and t1 in se_types:
                am_se_count[c['id2']] += 1

    am_ids = [aid for aid, a in atoms.items() if a['type'] in am_types]
    n_am = len(am_ids)
    if n_am == 0:
        return None

    no_se = sum(1 for aid in am_ids if am_se_count.get(aid, 0) == 0)
    single_se = sum(1 for aid in am_ids if am_se_count.get(aid, 0) == 1)
    counts = [am_se_count.get(aid, 0) for aid in am_ids]

    result = {
        'no_se_pct': float(no_se / n_am * 100),
        'single_se_pct': float(single_se / n_am * 100),
        'vulnerable_pct': float((no_se + single_se) / n_am * 100),
        'am_se_cn_mean': float(np.mean(counts)),
        'am_se_cn_std': float(np.std(counts)),
    }

    # ─── Per-AM-type breakdown (bimodal: AM_P-SE vs AM_S-SE) ────────────────
    # Physics: bimodal systems have size-dependent CN regimes. Large AM (P) sit
    # in interstitial-filling, small AM (S) sit near-monodisperse with SE. COMSOL
    # Butler-Volmer + solid diffusion require per-AM-type kinetics, so we expose
    # CN and surface-weighted effective CN separately.
    for lbl in set(type_map.values()):
        if 'AM' not in lbl:
            continue
        type_ids_for_lbl = [k for k, v in type_map.items() if v == lbl]
        am_lbl_ids = [aid for aid, a in atoms.items() if a['type'] in type_ids_for_lbl]
        if not am_lbl_ids:
            continue
        counts_lbl = np.array([am_se_count.get(aid, 0) for aid in am_lbl_ids])
        no_se_lbl = int(np.sum(counts_lbl == 0))
        single_lbl = int(np.sum(counts_lbl == 1))
        result[f'{lbl}_se_cn_mean'] = float(np.mean(counts_lbl))
        result[f'{lbl}_se_cn_std'] = float(np.std(counts_lbl))
        result[f'{lbl}_se_cn_median'] = float(np.median(counts_lbl))
        result[f'{lbl}_se_cn_max'] = int(np.max(counts_lbl))
        result[f'{lbl}_n_particles'] = len(am_lbl_ids)
        result[f'{lbl}_vulnerable_pct'] = float((no_se_lbl + single_lbl) / len(am_lbl_ids) * 100)

    # Surface-area-weighted effective AM-SE CN (for COMSOL pseudo-P2D)
    # CN_eff = Sum(N_i * R_i^2 * CN_i) / Sum(N_i * R_i^2)
    weighted_num = 0.0
    weighted_den = 0.0
    for aid in am_ids:
        r = atoms[aid]['radius']
        cn_aid = am_se_count.get(aid, 0)
        weighted_num += r * r * cn_aid
        weighted_den += r * r
    if weighted_den > 0:
        result['am_se_cn_surface_weighted'] = float(weighted_num / weighted_den)
    else:
        result['am_se_cn_surface_weighted'] = 0.0

    return result


# ─── Brittle Fracture Stage Classification ────────────────────────────────
# Wraps fracture_model (Auerbach + Lawn 1998) to produce per-case AM-AM
# fracture-stage statistics. Both δ-based (Hertzian-equivalent) and
# force-based (model-agnostic, recommended for hooke/hysteresis DEM) are
# computed in parallel so downstream tools can compare.

def calc_fracture_stages(atoms, contacts, type_map, scale=1000.0):
    """Per-case AM-AM brittle-fracture stage tally.

    Output keys (all flat, ready to merge into full_metrics.json):
      n_<stage>_AM_AM            δ-based count per stage
      n_<stage>_force_AM_AM      force-based count per stage
      n_total_AM_AM              total AM-AM contacts (δ-based denom)
      n_total_AM_AM_force        total AM-AM contacts with fn>0
      frac_<stage>_pct           δ-based stage share (%)
      frac_<stage>_force_pct     force-based stage share (%)
      fracture_index             δ-based (frag+pulv)/total ∈ [0,1]
      fracture_index_force       force-based (frag+pulv)/total
      n_<stage>_<pair_type>      per-pair-type breakdown (δ-based)
      n_<stage>_force_<pair>     per-pair-type breakdown (force-based)
      R_min_um_median_<pair>     median R_min for paper Section 2 footnote
      P_c_mN_median_<pair>       median Auerbach onset force (mN)
      F_mN_median_<pair>         median DEM normal force (mN, real units)
      F_over_Pc_median_<pair>    median F/P_c ratio (key indicator)

    Returns a dict (or empty dict if no AM-AM contacts).
    """
    # Local import to avoid circular dependency at module top
    from fracture_model import (
        fracture_classify_sim, fracture_classify_force_sim,
        ALL_STAGES, STAGE_RANK,
    )

    am_types = {k for k, v in type_map.items() if 'AM' in v}
    if not am_types:
        return {}

    stage_counts       = {f'n_{s}_AM_AM':       0 for s in ALL_STAGES}
    stage_counts_force = {f'n_{s}_force_AM_AM': 0 for s in ALL_STAGES}
    pair_types = ('AM_P-AM_P', 'AM_S-AM_S', 'AM_P-AM_S')
    pair_stage_counts       = {pt: {s: 0 for s in ALL_STAGES} for pt in pair_types}
    pair_stage_counts_force = {pt: {s: 0 for s in ALL_STAGES} for pt in pair_types}
    pair_samples = {pt: {'R_min': [], 'P_c': [], 'F': []} for pt in pair_types}

    for c in contacts:
        i1, i2 = int(c.get('id1', -1)), int(c.get('id2', -1))
        if i1 not in atoms or i2 not in atoms: continue
        a1, a2 = atoms[i1], atoms[i2]
        t1, t2 = a1['type'], a2['type']
        if t1 not in am_types or t2 not in am_types: continue
        delta = float(c.get('delta', 0) or 0)
        r_min = min(float(a1['radius']), float(a2['radius']))
        if r_min <= 0: continue

        pair_label = '-'.join(sorted([type_map.get(t1, ''), type_map.get(t2, '')]))

        # δ-based stage
        if delta > 0:
            stage, _dc, _m = fracture_classify_sim(
                delta, r_min, contact_type=pair_label, scale=scale)
            stage_counts[f'n_{stage}_AM_AM'] += 1
            if pair_label in pair_stage_counts:
                pair_stage_counts[pair_label][stage] += 1

        # Force-based stage (uses fn from contacts.csv; sim → real
        # conversion happens inside fracture_classify_force_sim)
        fn = float(c.get('fn', 0) or 0)
        if fn <= 0:
            fn = ((c.get('fn_x', 0) or 0) ** 2
                  + (c.get('fn_y', 0) or 0) ** 2
                  + (c.get('fn_z', 0) or 0) ** 2) ** 0.5
        if fn > 0:
            stage_f, P_c_N, _mult = fracture_classify_force_sim(
                fn, r_min, contact_type=pair_label, scale=scale)
            stage_counts_force[f'n_{stage_f}_force_AM_AM'] += 1
            if pair_label in pair_stage_counts_force:
                pair_stage_counts_force[pair_label][stage_f] += 1
            if pair_label in pair_samples:
                pair_samples[pair_label]['R_min'].append(r_min)
                pair_samples[pair_label]['P_c'].append(P_c_N)
                pair_samples[pair_label]['F'].append(fn)

    n_total = sum(stage_counts.values())
    n_total_force = sum(stage_counts_force.values())
    if n_total == 0 and n_total_force == 0:
        return {}

    out: dict = {}
    out.update(stage_counts)
    out.update(stage_counts_force)
    out['n_total_AM_AM']       = n_total
    out['n_total_AM_AM_force'] = n_total_force

    if n_total > 0:
        for s in ALL_STAGES:
            out[f'frac_{s}_pct'] = round(100.0 * stage_counts[f'n_{s}_AM_AM'] / n_total, 2)
        out['fracture_index'] = round(
            (stage_counts['n_fragmentation_AM_AM']
             + stage_counts['n_pulverization_AM_AM']) / n_total, 4)
    if n_total_force > 0:
        for s in ALL_STAGES:
            out[f'frac_{s}_force_pct'] = round(
                100.0 * stage_counts_force[f'n_{s}_force_AM_AM'] / n_total_force, 2)
        out['fracture_index_force'] = round(
            (stage_counts_force['n_fragmentation_force_AM_AM']
             + stage_counts_force['n_pulverization_force_AM_AM']) / n_total_force, 4)

    # Per-pair-type breakdown
    for pt, sc in pair_stage_counts.items():
        n_pair = sum(sc.values())
        out[f'n_total_{pt}'] = n_pair
        for s, n in sc.items():
            out[f'n_{s}_{pt}'] = n
            out[f'frac_{s}_{pt}_pct'] = round(100.0 * n / max(n_pair, 1), 2)
    for pt, sc in pair_stage_counts_force.items():
        n_pair = sum(sc.values())
        out[f'n_total_force_{pt}'] = n_pair
        for s, n in sc.items():
            out[f'n_{s}_force_{pt}'] = n
            out[f'frac_{s}_force_{pt}_pct'] = round(100.0 * n / max(n_pair, 1), 2)

    # Section-2 footnote medians (per-pair-type, real units)
    for pt, samples in pair_samples.items():
        if samples['R_min']:
            out[f'R_min_um_median_{pt}'] = round(
                float(np.median(samples['R_min']) / scale * 1e6), 3)
        if samples['P_c']:
            out[f'P_c_mN_median_{pt}'] = round(
                float(np.median(samples['P_c']) * 1e3), 4)
        if samples['F']:
            f_real = [f / scale for f in samples['F']]
            out[f'F_mN_median_{pt}'] = round(float(np.median(f_real) * 1e3), 4)
            if samples['P_c']:
                ratios = [(f / scale) / p for f, p in zip(samples['F'], samples['P_c']) if p > 0]
                if ratios:
                    out[f'F_over_Pc_median_{pt}'] = round(float(np.median(ratios)), 3)
    return out


# ─── Effective Ionic Conductivity ─────────────────────────────────────────

def calc_effective_conductivity(atoms, perc_result, porosity, tortuosity_result, type_map, plate_z, box_xy=0.05, box_x=None, box_y=None):
    """Estimate σ_brug/σ_grain (Bruggeman approximation, ignoring contact resistance).
    σ_brug/σ_grain = φ_SE × f_perc / τ²
    Note: overestimates by 3-10× vs network solver (no constriction resistance)."""
    se_types = [k for k, v in type_map.items() if v == 'SE']
    se_ids = [aid for aid, a in atoms.items() if a['type'] in se_types]

    if not se_ids:
        return None

    # SE volume fraction
    bx = box_x if box_x else box_xy
    by = box_y if box_y else box_xy
    v_electrode = bx * by * plate_z
    v_se = sum(4/3 * np.pi * atoms[aid]['radius']**3 for aid in se_ids)
    phi_se = v_se / v_electrode if v_electrode > 0 else 0

    # Use recommended τ (median if high dispersion, else mean)
    tau = tortuosity_result.get('recommended', tortuosity_result.get('mean'))
    if not tau or tau <= 0:
        return None

    # Connected SE fraction (percolating)
    perc_pct = perc_result.get('percolation_pct', 0) / 100

    # Effective conductivity ratio
    sigma_ratio = phi_se * perc_pct / (tau ** 2)

    return {
        'phi_se': float(phi_se),
        'tau': float(tau),
        'perc_fraction': float(perc_pct),
        'sigma_ratio': float(sigma_ratio),
    }


# ─── Von Mises Stress Analysis ─────────────────────────────────────────────

def calc_von_mises_stress(atoms_raw, type_map, scale, plate_z, n_layers=10):
    """
    Simplified Von Mises from diagonal stress components.
    σ_VM = √(σ_xx² + σ_yy² + σ_zz² - σ_xx·σ_yy - σ_yy·σ_zz - σ_xx·σ_zz)

    atoms_raw must have 'sigma_xx', 'sigma_yy', 'sigma_zz' keys (sim Pa).
    Returns: overall CV, type ratios, z-layer CV profile.
    Note: absolute values are not reliable (effective E used), only relative comparison.
    """
    # Check if stress data available
    sample = next(iter(atoms_raw.values()))
    if 'sigma_xx' not in sample:
        return None

    # Compute Von Mises for each atom (sim units, relative only)
    vm_data = {}
    for aid, a in atoms_raw.items():
        sxx = a.get('sigma_xx', 0)
        syy = a.get('sigma_yy', 0)
        szz = a.get('sigma_zz', 0)
        vm = np.sqrt(sxx**2 + syy**2 + szz**2 - sxx*syy - syy*szz - sxx*szz)
        vm_data[aid] = vm

    all_vm = np.array(list(vm_data.values()))
    vm_mean = float(np.mean(all_vm))
    vm_std = float(np.std(all_vm))
    vm_cv = (vm_std / vm_mean * 100) if vm_mean > 0 else 0

    # Type-specific mean (for ratio calculation)
    type_stress = {}
    for t_name in set(type_map.values()):
        t_ids = [aid for aid, a in atoms_raw.items() if type_map.get(a['type']) == t_name]
        if t_ids:
            t_vm = np.array([vm_data[aid] for aid in t_ids])
            type_stress[t_name] = {
                'mean': float(np.mean(t_vm)),
                'ratio': float(np.mean(t_vm) / vm_mean) if vm_mean > 0 else 0,
            }

    # Z-layer CV profile
    z_layer_cv = []
    z_values = np.array([a['z'] for a in atoms_raw.values()])
    z_min, z_max = 0.0, plate_z
    layer_edges = np.linspace(z_min, z_max, n_layers + 1)

    atom_ids = list(atoms_raw.keys())
    atom_z = np.array([atoms_raw[aid]['z'] for aid in atom_ids])
    atom_vm = np.array([vm_data[aid] for aid in atom_ids])

    for i in range(n_layers):
        mask = (atom_z >= layer_edges[i]) & (atom_z < layer_edges[i+1])
        if mask.sum() > 1:
            layer_vm = atom_vm[mask]
            layer_mean = np.mean(layer_vm)
            layer_cv = (np.std(layer_vm) / layer_mean * 100) if layer_mean > 0 else 0
            z_mid = (layer_edges[i] + layer_edges[i+1]) / 2 * scale  # to μm
            z_layer_cv.append({
                'z_mid_um': float(z_mid),
                'cv': float(layer_cv),
                'mean_normalized': float(layer_mean / vm_mean) if vm_mean > 0 else 0,
            })

    return {
        'vm_cv': vm_cv,
        'vm_mean': vm_mean,
        'type_stress': type_stress,
        'z_layer_cv': z_layer_cv,
    }


# ─── Full Analysis ─────────────────────────────────────────────────────────

def _get_box_xy(results_dir):
    """Read box_x, box_y from input_params.json. Falls back to 0.05."""
    params_path = os.path.join(results_dir, 'input_params.json')
    if os.path.exists(params_path):
        with open(params_path) as f:
            params = json.load(f)
        bx = params.get('box_x', 0.05)
        by = params.get('box_y', 0.05)
        if bx > 0 and by > 0:
            return bx, by
    return 0.05, 0.05


def run_full_analysis(atoms_raw, contacts_raw, type_map, scale, results_dir, box_xy=None):
    """
    Run all analyses. atoms_raw/contacts_raw are dicts in SIM units.
    box_xy is auto-detected from input_params.json if not specified.
    Returns comprehensive results dict.
    """
    se_types = [k for k, v in type_map.items() if v == 'SE']
    am_types = [k for k, v in type_map.items() if 'AM' in v]

    # Auto-detect box dimensions
    box_x, box_y = _get_box_xy(results_dir)
    if box_xy is not None:
        box_x = box_y = box_xy
    box_xy_val = box_x  # for functions that take single box_xy

    # Get plate_z
    plate_z, pz_source = get_plate_z(results_dir, atoms_raw, scale)
    thickness_um = plate_z * scale  # sim → μm

    print(f"  box_xy = {box_x:.4f} x {box_y:.4f}, plate_z = {plate_z:.6f} ({pz_source}), thickness = {thickness_um:.1f} μm")

    # 1. Porosity — sphere-sum (production calibration anchor) + union (overlap-corrected,
    # literature-comparable) + overlap_fraction (plastic deformation indicator).
    poro_dual = calc_porosity_dual(atoms_raw, contacts_raw, plate_z, box_xy_val)
    porosity = poro_dual['porosity_spheresum']       # back-compat: 'porosity' key stays sphere-sum
    porosity_union = poro_dual['porosity_union']
    overlap_fraction_pct = poro_dual['overlap_fraction_pct']
    print(f"  Porosity: {porosity:.2f}% (sphere-sum)  |  union {porosity_union:.2f}%  |  overlap {overlap_fraction_pct:.2f}%")

    # 2. Interface Area
    iface = calc_interface_area(atoms_raw, contacts_raw, type_map, scale)
    for ct, v in iface.items():
        print(f"  {ct}: {v['n_contacts']} contacts, total {v['total_area']:.1f} μm²")

    # 3. Coverage (Hertzian baseline; physics + rough variants computed
    # downstream by coverage_physics_vs_hertzian.py)
    cov = calc_coverage(atoms_raw, contacts_raw, type_map, scale)
    for lbl, v in cov.items():
        print(f"  Coverage {lbl}: {v['mean']:.1f}% ± {v['std']:.1f}%")

    # 5. Percolation (run BEFORE CN so we can pass perc_set into F2)
    perc = calc_percolation(atoms_raw, contacts_raw, se_types, plate_z, box_x=box_x, box_y=box_y)
    print(f"  Percolation: {perc['percolation_pct']:.1f}%, Top Reachable: {perc['top_reachable_pct']:.1f}%")
    print(f"  Components: {perc['n_components']}, Largest: {perc['largest_pct']:.1f}%")

    # 4. SE-SE CN (with F2 percolating-only + area-weighted variants and
    # F1 plastic-augmented variant). F1 spread distance set to ~10 nm
    # (= 2 × h_film_min) in real units, converted to sim units via 1/scale.
    H_SPREAD_REAL_M = 10e-9                     # 10 nm physical
    h_spread_sim = H_SPREAD_REAL_M * scale      # sim length: m × (sim/real) — for scale=1000 (μm→mm sim) gives 1e-5
    cn = calc_se_se_cn(atoms_raw, contacts_raw, se_types,
                       perc_set=perc.get('percolating_se'), scale=scale,
                       h_spread_sim=h_spread_sim)
    print(f"  SE-SE CN: {cn['mean']:.2f} ± {cn['std']:.2f}  "
          f"(perc-only: {cn.get('mean_perc', 0):.2f}, "
          f"cn_eff_area: {cn.get('cn_eff_area', 0):.4f}, "
          f"aug: {cn.get('mean_aug', 0):.2f} +{cn.get('n_extra_aug', 0)} extras)")

    # 4b. AM-AM CN
    am_am_cn = calc_am_am_cn(atoms_raw, contacts_raw, am_types, scale=scale)
    if am_am_cn['mean'] > 0:
        print(f"  AM-AM CN: {am_am_cn['mean']:.2f} ± {am_am_cn['std']:.2f}")

    # 6. Tortuosity
    tau = calc_tortuosity(atoms_raw, perc, box_x=box_x, box_y=box_y)
    tau_str = f"{tau['mean']:.2f} ± {tau['std']:.2f}" if tau['mean'] else "N/A"
    print(f"  Tortuosity: {tau_str} ({tau['n_samples']} samples)")

    # 7. Ionic Active AM
    ionic = calc_ionic_active_am(atoms_raw, contacts_raw, perc, se_types, am_types, type_map)
    print(f"  Ionic Active AM: {ionic['active_pct']:.1f}%")

    # 8. Von Mises Stress (relative)
    stress = calc_von_mises_stress(atoms_raw, type_map, scale, plate_z)
    if stress:
        print(f"  Stress CV: {stress['vm_cv']:.1f}%")
        for tn, sv in stress['type_stress'].items():
            print(f"    {tn}: σ/σ_mean = {sv['ratio']:.2f}")
    else:
        print("  Stress: N/A (no stress data)")

    # 9. Contact Force Distribution
    force_dist = calc_contact_force_distribution(atoms_raw, contacts_raw, type_map, scale)
    for ct, v in force_dist.items():
        print(f"  Force {ct}: {v['mean']:.3f} ± {v['std']:.3f} μN (max {v['max']:.3f})")

    # 10. Contact Pressure
    contact_pressure = calc_contact_pressure(atoms_raw, contacts_raw, type_map, scale)
    if 'overall' in contact_pressure:
        cp = contact_pressure['overall']
        print(f"  Contact Pressure: {cp['mean']:.1f} ± {cp['std']:.1f} MPa (max {cp['max']:.1f})")

    # 11. Overlap Ratio
    overlap = calc_overlap_ratio(atoms_raw, contacts_raw)
    if overlap:
        print(f"  Overlap δ/R: {overlap['mean']:.2f}% ± {overlap['std']:.2f}% (max {overlap['max']:.2f}%, >5%: {overlap['pct_above_5']:.1f}%)")

    # 12. AM Isolation Risk
    am_risk = calc_am_isolation_risk(atoms_raw, contacts_raw, type_map)
    if am_risk:
        print(f"  AM Risk: vulnerable {am_risk['vulnerable_pct']:.1f}% (no SE: {am_risk['no_se_pct']:.1f}%, single SE: {am_risk['single_se_pct']:.1f}%)")

    # 13. Effective Ionic Conductivity
    eff_cond = calc_effective_conductivity(atoms_raw, perc, porosity, tau, type_map, plate_z, box_x=box_x, box_y=box_y)
    if eff_cond:
        print(f"  σ_eff/σ_bulk: {eff_cond['sigma_ratio']:.4f} (φ_SE={eff_cond['phi_se']:.3f}, τ={eff_cond['tau']:.2f})")

    # 14. Brittle fracture stages (Auerbach + Lawn 1998) — auto-DB
    fracture = {}
    try:
        fracture = calc_fracture_stages(atoms_raw, contacts_raw, type_map, scale=scale)
        if fracture:
            n_total = fracture.get('n_total_AM_AM', 0)
            n_severe = (fracture.get('n_fragmentation_AM_AM', 0)
                        + fracture.get('n_pulverization_AM_AM', 0))
            print(f"  Fracture stages: {n_total} AM-AM contacts, "
                  f"{n_severe} severe (frag+pulv), "
                  f"index={fracture.get('fracture_index', 0):.3f}")
    except Exception as e:
        print(f"  [warn] fracture-stage calc failed: {e}")

    return {
        'plate_z': plate_z,
        'plate_z_source': pz_source,
        'thickness_um': thickness_um,
        'porosity': porosity,
        'porosity_spheresum': porosity,
        'porosity_union': porosity_union,
        'overlap_fraction_pct': overlap_fraction_pct,
        'interface': iface,
        'coverage': cov,
        'se_se_cn': cn,
        'am_am_cn': am_am_cn,
        'percolation': perc,
        'tortuosity': tau,
        'ionic_active': ionic,
        'stress': stress,
        'force_dist': force_dist,
        'contact_pressure': contact_pressure,
        'overlap_ratio': overlap,
        'am_isolation_risk': am_risk,
        'effective_conductivity': eff_cond,
        'fracture': fracture,
    }
