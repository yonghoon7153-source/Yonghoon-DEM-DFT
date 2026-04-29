"""3D-viewer auxiliary data extractor.

Computes per-particle and per-contact metadata that the front-end
viewer uses to colour / size / filter particles in different "view
modes":

  brittle hotspots   — AM-AM δ/R > Auerbach threshold
  cluster coloring   — percolating vs broken vs dead components
  stress hot spots   — per-particle max contact stress (MPa)
  coverage heat      — per-AM SE coverage (%)
  fracture-prone SE  — SE-SE with high δ/R (sub-Auerbach but stressed)

All scales are in display units (μm, MPa) so the front-end can use
them directly without further conversion.

Outputs a single dict that the Flask /3d-data endpoint merges into
its response. Pure-function with no side effects.
"""
from __future__ import annotations
from typing import Iterable
import math
from collections import defaultdict


# ── NCM brittle fracture (Auerbach + Lawn 1998) ──────────────────────────
# Material constants — see scripts/fracture_model.py for full citation list.
K_IC_AM_S = 1.0e6     # Pa·m^0.5  Liu 2020 (single crystal NCM)
K_IC_AM_P = 0.3e6     # Pa·m^0.5  Quinn 2020 (polycrystalline NCM)
E_AM      = 150e9     # Pa        Xu 2017 (NCM811 nanoindentation)
NU_AM     = 0.25
A_AUERBACH = 200.0    # Lawn 1998 §3.4 geometric constant

# δ-multiplier thresholds for damage stages (Lawn 1998 Table 3.4).
MULT_MICROCRACK    = 1.0
MULT_MULTICRACK    = 2.0
MULT_FRAGMENTATION = 5.0
MULT_PULVERIZATION = 10.0

# SE Tabor plastic regime threshold (kept for SE-side highlighting).
DR_SE_PLASTIC = 0.0078    # fully plastic Tabor
DR_SE_YIELD   = 0.0011    # elastic-plastic transition


def auerbach_delta_critical(R_min_sim: float, K_IC: float,
                             E: float = E_AM, nu: float = NU_AM,
                             A: float = A_AUERBACH,
                             scale: float = 1000.0) -> float:
    """Critical δ (sim units) at which a Hertzian cone crack initiates.

    R_min_sim : the smaller of the two contacting particle radii in
                simulation units (e.g. mm if scale=1000).
    Returns δ_c in sim units so it is directly comparable to the δ
    field in contacts.csv.
    """
    if R_min_sim <= 0 or K_IC <= 0:
        return float('inf')
    R_min_m = R_min_sim / scale     # sim → m (assuming scale = sim/m ratio)
    R_star  = R_min_m / 2.0
    E_star  = E / (2.0 * (1.0 - nu * nu))
    P_c     = A * K_IC * K_IC * R_min_m / E_star
    delta_c_m = (3.0 * P_c / (4.0 * E_star * math.sqrt(R_star))) ** (2.0 / 3.0)
    return delta_c_m * scale         # back to sim units


def fracture_stage(delta_sim: float, R_min_sim: float, contact_type: str,
                   scale: float = 1000.0) -> tuple[str, float, float]:
    """Classify a contact's brittle damage stage.

    Returns (stage, delta_c, multiplier).
      stage ∈ {'intact', 'microcrack', 'multicrack',
               'fragmentation', 'pulverization'}
    """
    # Pick K_IC by contact type
    if contact_type == 'AM_S-AM_S':
        K_IC = K_IC_AM_S
    elif contact_type == 'AM_P-AM_P':
        K_IC = K_IC_AM_P
    elif 'AM' in contact_type:
        K_IC = math.sqrt(K_IC_AM_S * K_IC_AM_P)
    else:  # SE involved — fall back to AM_P (more brittle); SE handled separately
        K_IC = K_IC_AM_P

    delta_c = auerbach_delta_critical(R_min_sim, K_IC, scale=scale)
    if delta_c <= 0 or delta_sim <= 0:
        return ('intact', delta_c, 0.0)
    m = delta_sim / delta_c
    if   m < MULT_MICROCRACK:    stage = 'intact'
    elif m < MULT_MULTICRACK:    stage = 'microcrack'
    elif m < MULT_FRAGMENTATION: stage = 'multicrack'
    elif m < MULT_PULVERIZATION: stage = 'fragmentation'
    else:                        stage = 'pulverization'
    return (stage, delta_c, m)


# ── Per-particle aggregation across contacts ─────────────────────────────

def aggregate_particle_metrics(contacts: Iterable[dict],
                                atoms_by_id: dict,
                                type_map: dict,
                                scale: float = 1000.0) -> dict:
    """Walk contacts; produce per-particle dicts:
        stress_max[id]   — max contact pressure in MPa (real units)
        dr_max[id]       — max δ/R across this particle's contacts
        worst_partner[id]— other particle id at the dr_max contact
    Also returns per-AM-AM brittle-stage list for highlighting.
    """
    stress_max:    dict[int, float] = defaultdict(float)
    dr_max:        dict[int, float] = defaultdict(float)
    worst_partner: dict[int, int]   = {}
    brittle_pairs: list[dict] = []
    se_stress_pairs: list[dict] = []

    pressure_conv = scale / 1.0e6     # sim Pa → real MPa (calibrated to scale)

    for c in contacts:
        i1 = int(c.get('id1', -1)); i2 = int(c.get('id2', -1))
        if i1 < 0 or i2 < 0:
            continue
        a1 = atoms_by_id.get(i1); a2 = atoms_by_id.get(i2)
        if a1 is None or a2 is None:
            continue

        delta = float(c.get('delta', 0) or 0)
        area  = float(c.get('contact_area', 0) or 0)
        fn    = c.get('fn')
        if fn in (None, 0):
            fn = math.sqrt(
                (c.get('fn_x', 0) or 0) ** 2 +
                (c.get('fn_y', 0) or 0) ** 2 +
                (c.get('fn_z', 0) or 0) ** 2)
        fn = float(fn or 0)

        # contact pressure in real MPa
        p_MPa = (fn / area * pressure_conv) if area > 0 else 0.0
        if p_MPa > stress_max[i1]: stress_max[i1] = p_MPa
        if p_MPa > stress_max[i2]: stress_max[i2] = p_MPa

        r_min = min(float(a1.get('radius', 0)), float(a2.get('radius', 0)))
        if r_min > 0 and delta > 0:
            dr = delta / r_min
            if dr > dr_max[i1]:
                dr_max[i1] = dr; worst_partner[i1] = i2
            if dr > dr_max[i2]:
                dr_max[i2] = dr; worst_partner[i2] = i1

        # Type-specific bucketing for highlight lists
        t1 = type_map.get(int(a1.get('type', -1)), '?')
        t2 = type_map.get(int(a2.get('type', -1)), '?')
        is_am1 = 'AM' in t1; is_am2 = 'AM' in t2
        is_se1 = t1 == 'SE'; is_se2 = t2 == 'SE'

        if is_am1 and is_am2:
            ct = '-'.join(sorted([t1, t2]))
            stage, delta_c, mult = fracture_stage(delta, r_min, ct, scale=scale)
            if stage != 'intact':
                brittle_pairs.append({
                    'id1': i1, 'id2': i2,
                    'dr': round(dr if r_min > 0 and delta > 0 else 0, 4),
                    'mult': round(mult, 2),
                    'stage': stage,
                    'pressure_MPa': round(p_MPa, 1),
                    'pair_type': ct,
                })
        elif is_se1 and is_se2:
            # SE-SE: highlight only those above plastic Tabor threshold
            if r_min > 0 and delta > 0 and (delta / r_min) > DR_SE_YIELD:
                se_stress_pairs.append({
                    'id1': i1, 'id2': i2,
                    'dr': round(delta / r_min, 4),
                    'pressure_MPa': round(p_MPa, 1),
                    'plastic': (delta / r_min) > DR_SE_PLASTIC,
                })

    return {
        'stress_max':       {int(k): round(v, 2) for k, v in stress_max.items()},
        'dr_max':           {int(k): round(v, 4) for k, v in dr_max.items()},
        'worst_partner':    {int(k): int(v)      for k, v in worst_partner.items()},
        'brittle_pairs':    brittle_pairs,
        'se_stress_pairs':  se_stress_pairs,
    }


# ── SE cluster classification (percolating / top-only / bottom-only / dead) ─

def classify_clusters(se_clusters_json: dict) -> dict:
    """Convert the existing se_clusters.json into a flat per-cluster
    table with status + display color.

    Returns dict keyed by cluster index (string for JSON-friendly):
        {"0": {"status": "percolating", "size": 234,
               "color": "#1e40af", "opacity": 1.0},
         ...}
    """
    out: dict = {}
    clusters = (se_clusters_json or {}).get('clusters') or []
    for i, cl in enumerate(clusters):
        size  = int(cl.get('size', len(cl.get('ids', []))))
        has_b = bool(cl.get('has_bottom') or cl.get('touches_bottom'))
        has_t = bool(cl.get('has_top')    or cl.get('touches_top'))
        is_p  = bool(cl.get('percolating'))
        if is_p or (has_b and has_t):
            status, color, opacity = 'percolating', '#1e40af', 1.00
        elif has_t and not has_b:
            status, color, opacity = 'top_only',    '#93c5fd', 0.50
        elif has_b and not has_t:
            status, color, opacity = 'bottom_only', '#fbbf24', 0.50
        else:
            status, color, opacity = 'dead',        '#9ca3af', 0.15
        out[str(i)] = {
            'status':  status, 'size': size,
            'color':   color,  'opacity': opacity,
        }
    return out


def build_cluster_id_map(se_clusters_json: dict) -> dict[int, int]:
    """Per-SE-particle cluster index. Returns {se_id: cluster_idx}."""
    out: dict[int, int] = {}
    clusters = (se_clusters_json or {}).get('clusters') or []
    for i, cl in enumerate(clusters):
        for pid in cl.get('ids', []) or []:
            out[int(pid)] = i
    return out


# ── Per-AM coverage map (μm² SE / μm² total surface) ─────────────────────

def build_coverage_map(coverage_per_am_csv_path) -> dict[int, float]:
    """Read coverage_per_am.csv (created by coverage_physics_vs_hertzian).
    Returns {am_id: coverage_pct (0-100)} using the *physics* column when
    available, otherwise hertzian.
    """
    import os
    out: dict[int, float] = {}
    if not (coverage_per_am_csv_path and os.path.exists(coverage_per_am_csv_path)):
        return out
    try:
        import pandas as pd
        df = pd.read_csv(coverage_per_am_csv_path)
        col = ('coverage_physics_pct' if 'coverage_physics_pct' in df.columns
               else 'coverage_hertzian_pct')
        if 'am_id' in df.columns and col in df.columns:
            for _, r in df.iterrows():
                out[int(r['am_id'])] = float(r[col])
    except Exception:
        pass
    return out
