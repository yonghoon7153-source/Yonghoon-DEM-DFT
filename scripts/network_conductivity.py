"""
DEM-Native Transport Framework v2.0
====================================
Kirchhoff resistor network solver for effective conductivity in ASSB composite cathodes.

Each SE-SE (or AM-AM) contact → edge with R = R_bulk + R_constriction (series).
  R_bulk: geometric normalization for particle bulk resistance
  R_constriction: Maxwell spreading resistance R = 1/(2σa), Holm (1967)

Three decomposition runs:
  1. FULL: R_bulk + R_constriction → σ_full (physical ground truth)
  2. CONTACT_FREE: R_constriction=0 → σ_cf (upper bound, ideal contact limit)
  3. CONSTRICTION_ONLY: R_bulk=0 → σ_constr (spreading resistance limit)

σ_eff/σ_bulk = G_eff × L / A  (Ohm's law, dimensionless)

Networks: ionic (SE-SE), electronic (AM-AM), thermal (all contacts)

References:
  - Holm 1967: Electric Contacts — Maxwell constriction resistance
  - Bruggeman 1935: σ_eff = σ_0 × φ^n (EMT, for comparison)
  - Minnmann et al. 2021: Electronic percolation in SSB cathodes
"""

import numpy as np
import json
import os
import sys
from scipy import sparse
from scipy.sparse.linalg import spsolve, cg

# Plastic-physics contact-area model (used when contact_mode='physics')
# See docs: scripts/plastic_coverage.py → film_area_from_overlap()
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)
try:
    from plastic_coverage import film_area_from_overlap as _film_area
except Exception:
    _film_area = None  # graceful fallback if numpy/import issue


# LPSCl argyrodite grain interior conductivity (NOT pellet value)
SIGMA_BULK_DEFAULT = 3.0e-3  # S/cm (grain interior, ionic)

# NCM electronic conductivity (typical, SOC-dependent)
SIGMA_AM_ELECTRONIC = 0.05  # S/cm (50 mS/cm, discharged NCM)

# Thermal conductivity (W/(m·K) = W/(m·K) × 10⁻⁴ = W/(cm·K))
K_AM_THERMAL = 4.0e-2   # W/(cm·K) ≈ 4 W/(m·K), NCM
K_SE_THERMAL = 0.7e-2   # W/(cm·K) ≈ 0.7 W/(m·K), LPSCl (Ketter 2025)


# ─── D1-C / D1-F: σ_disk / σ_bulk ratios ──────────────────────────────────
# Constriction at the contact disk traverses a region whose σ may differ
# from grain interior σ. Two physical sources:
#   D1-F (regime-based): plastic contact has compressed/amorphized disk
#                        → σ_disk < σ_grain. Hertzian (elastic) contact
#                        retains crystalline σ. Bracketed by Sakuda 2013
#                        single-crystal (3.0) vs cold-pressed pellet (0.31)
#                        — geometric mean ~1.0, so factor ~0.33 for fully
#                        amorphized disk.
#   D1-C (AM-environment): SE close to polycrystalline AM_P inherits more
#                          GB content; near single-crystal AM_S retains
#                          high σ. Multiplicative on top of D1-F.
SIGMA_DISK_RATIO_AMORPH = 0.50   # plastic-disk σ / grain σ (D1-F)
SIGMA_DISK_RATIO_AM_P   = 0.80   # AM_P-environment factor (D1-C)
SIGMA_DISK_RATIO_AM_S   = 0.95   # AM_S-environment factor (D1-C)


def get_sigma_disk_factor(regime, t1, t2, sigma_model='uniform',
                          am_p_types=None, am_s_types=None):
    """σ_disk / σ_bulk for this contact.

    sigma_model:
      'uniform'  : 1.0 (current default — no per-contact σ variation).
      'regime'   : D1-F only. Plastic regimes get amorphized σ_disk.
      'gb_aware' : D1-C + D1-F. Adds AM-environment modulation for
                   SE-AM and AM-AM contacts on top of regime factor.
    """
    if sigma_model == 'uniform':
        return 1.0
    factor = 1.0
    # D1-F: amorphization in plastic regimes (Tabor / volume / geometric caps)
    if regime in ('tabor', 'volume', 'geom'):
        factor *= SIGMA_DISK_RATIO_AMORPH
    if sigma_model == 'gb_aware':
        # D1-C: only applies when AM is involved (AM environment affects σ
        # in the contact-disk region). For pure SE-SE contacts, no effect.
        if am_p_types and (t1 in am_p_types or t2 in am_p_types):
            factor *= SIGMA_DISK_RATIO_AM_P
        elif am_s_types and (t1 in am_s_types or t2 in am_s_types):
            factor *= SIGMA_DISK_RATIO_AM_S
    return factor


def build_network(atoms_raw, contacts_raw, target_types, scale,
                  plate_z, box_x=0.05, box_y=0.05, boundary_factor=2.0,
                  mode='ionic', type_map=None, results_dir=None,
                  contact_mode='hertzian'):
    """
    Build resistor network from DEM data.
    mode='ionic': SE-SE network only (uses percolation_sets.json for boundaries)
    mode='electronic': AM-AM network only
    mode='thermal': ALL contacts (AM-AM, AM-SE, SE-SE)
    contact_mode='hertzian'  : use LIGGGHTS-reported contact_area directly (DEM-native)
    contact_mode='physics'   : use plastic-film area from δ/R* Tabor+volume model
                               (literature-anchored, 0 free params — see plastic_coverage.py)
    Returns nodes, edges, bottom/top boundary sets.
    """
    if mode == 'thermal':
        target_ids = list(atoms_raw.keys())
    else:
        target_ids = [aid for aid, a in atoms_raw.items() if a['type'] in target_types]

    if not target_ids:
        return None

    # Boundary detection: z-coordinate based (consistent with EIS measurement)
    bottom_ids = None
    top_ids = None

    # ── C4 patch: per-particle plate-contact test ───────────────────────
    # Match calc_percolation behavior — each particle judged by its own
    # radius, not a global min(r) threshold. r_SE-independent → fair across
    # D0.5 vs D1.5 cases.
    if not bottom_ids or not top_ids:
        bottom_ids = {aid for aid in target_ids
                      if atoms_raw[aid]['z'] <= atoms_raw[aid]['radius'] * boundary_factor}
        top_ids = {aid for aid in target_ids
                   if atoms_raw[aid]['z'] >= plate_z - atoms_raw[aid]['radius'] * boundary_factor}

        # Fallback L1: thin electrodes / strict boundary → 15%/85% of plate_z
        if len(bottom_ids) < 3 or len(top_ids) < 3:
            z_bottom = plate_z * 0.15
            z_top = plate_z * 0.85
            bottom_ids = {aid for aid in target_ids if atoms_raw[aid]['z'] <= z_bottom}
            top_ids = {aid for aid in target_ids if atoms_raw[aid]['z'] >= z_top}

        # Fallback L2: when plate_z overshoots the actual particle range
        # (mesh_info.json absent → plate_z uses atom max z+r which overshoots
        # the true top plane by one AM radius), anchor the 15/85% split to the
        # OBSERVED z-range of target particles. Prevents silent percolation=0
        # for thick electrodes where top_ids empties under plate_z-based bounds.
        if len(bottom_ids) < 3 or len(top_ids) < 3:
            z_vals = [atoms_raw[aid]['z'] for aid in target_ids]
            z_min_obs = min(z_vals); z_max_obs = max(z_vals)
            span = z_max_obs - z_min_obs
            z_bottom = z_min_obs + span * 0.15
            z_top = z_max_obs - span * 0.15
            bottom_ids = {aid for aid in target_ids if atoms_raw[aid]['z'] <= z_bottom}
            top_ids = {aid for aid in target_ids if atoms_raw[aid]['z'] >= z_top}

    # Determine SE types for thermal mode
    se_type_set = set()
    if type_map:
        se_type_set = {k for k, v in type_map.items() if v == 'SE'}

    # Build contact map (area + delta). Delta is required for physics contact_mode
    # so each edge can recompute A_plastic from overlap geometry.
    contact_map = {}  # pair → {'ca': Hertzian area, 'delta': overlap}
    for c in contacts_raw:
        id1, id2 = c['id1'], c['id2']
        if id1 in atoms_raw and id2 in atoms_raw:
            if mode == 'thermal':
                pair = (min(id1, id2), max(id1, id2))
                ca = c.get('contact_area', 0)
                delta_c = c.get('delta', 0)
                if ca > 0 or delta_c > 0:
                    contact_map[pair] = {'ca': ca, 'delta': delta_c}
            else:
                if atoms_raw[id1]['type'] in target_types and atoms_raw[id2]['type'] in target_types:
                    pair = (min(id1, id2), max(id1, id2))
                    ca = c.get('contact_area', 0)
                    delta_c = c.get('delta', 0)
                    if ca > 0 or delta_c > 0:
                        contact_map[pair] = {'ca': ca, 'delta': delta_c}

    # Build edges with physical resistances
    # All distances in μm, areas in μm², resistivity in Ω·μm
    # ρ = 1/σ, σ = 1.3e-3 S/cm = 1.3e-7 S/μm → ρ = 7.69e6 Ω·μm
    # But we normalize: set ρ=1, then σ_eff comes out as ratio to σ_bulk

    edges = []
    for pair, cdat in contact_map.items():
        id1, id2 = pair
        a1, a2 = atoms_raw[id1], atoms_raw[id2]
        ca_sim = cdat['ca']
        delta_sim = cdat['delta']

        # Hop distance (μm) with periodic boundary
        dx = abs(a1['x'] - a2['x'])
        dy = abs(a1['y'] - a2['y'])
        dz = a1['z'] - a2['z']
        dx = min(dx, box_x - dx)
        dy = min(dy, box_y - dy)
        d_ij = np.sqrt(dx**2 + dy**2 + dz**2) * scale  # μm

        # Particle radii (sim units → μm)
        r1_sim = a1['radius']
        r2_sim = a2['radius']
        r1 = r1_sim * scale
        r2 = r2_sim * scale

        # Hertzian area (LIGGGHTS-reported, sim→μm²)
        A_hertzian = ca_sim * scale**2  # μm²

        # Physics (plastic-film) area: Tabor+volume, literature-anchored
        # Compute in sim units then scale to μm²
        # 5-case decomposition (when components available):
        #   Lower bounds: A_hertzian (πR*δ), A_ligg (LIGGGHTS internal)
        #   Upper caps:   A_tabor (F/H), A_volume (V/h_min), A_geom (2πR_min²)
        #   Final:        A_physics = max(lower, min(caps))
        A_components = None
        if delta_sim > 0 and r1_sim > 0 and r2_sim > 0:
            R_star_sim = (r1_sim * r2_sim) / (r1_sim + r2_sim)
            R_min_sim = min(r1_sim, r2_sim)
            delta_over_R = delta_sim / R_star_sim if R_star_sim > 0 else 0.0
            if _film_area is not None:
                A_phys_sim, regime, comp = _film_area(
                    delta_sim, R_star_sim,
                    R_min=R_min_sim, ligg_area=ca_sim,
                    mode='physics', return_components=True)
                A_physics = A_phys_sim * scale**2  # μm²
                # Convert components to μm² (skip None entries)
                A_components = {
                    'A_hertzian_um2': comp['A_hertzian'] * scale**2,
                    'A_ligg_um2':     None if comp['A_ligg'] is None else comp['A_ligg'] * scale**2,
                    'A_tabor_um2':    None if comp['A_tabor'] is None else comp['A_tabor'] * scale**2,
                    'A_volume_um2':   None if comp['A_volume'] is None else comp['A_volume'] * scale**2,
                    'A_geom_um2':     None if comp['A_geom'] is None else comp['A_geom'] * scale**2,
                    'A_final_um2':    A_physics,
                    'binding':        comp['binding'],
                }
            else:
                A_physics = A_hertzian  # fallback if import failed
                regime = 'hertzian_fallback'
        else:
            delta_over_R = 0.0
            A_physics = A_hertzian
            regime = 'no_delta'

        # Select active area for this run
        A_contact = A_physics if contact_mode == 'physics' else A_hertzian
        a_contact = np.sqrt(A_contact / np.pi) if A_contact > 0 else 0.0

        # Thermal mode: material-specific conductivity weighting
        # k_AM ≈ 4.0 W/m·K, k_SE ≈ 0.7 W/m·K
        # AM-AM: weight=k_AM/k_SE, SE-SE: weight=1, AM-SE: harmonic mean
        if mode == 'thermal' and se_type_set:
            t1_is_se = a1['type'] in se_type_set
            t2_is_se = a2['type'] in se_type_set
            k_ratio = K_AM_THERMAL / K_SE_THERMAL  # ~5.7
            if not t1_is_se and not t2_is_se:
                # AM-AM: high thermal conductivity
                k_weight = k_ratio
            elif t1_is_se and t2_is_se:
                # SE-SE: baseline
                k_weight = 1.0
            else:
                # AM-SE: harmonic mean
                k_weight = 2 * k_ratio / (1 + k_ratio)
        else:
            k_weight = 1.0

        # Normalized resistances (ρ=1, scaled by k_weight for thermal):
        # R_bulk = d / (k_weight × π × r²)
        R_bulk_1 = (d_ij / 2) / (k_weight * np.pi * r1**2) if r1 > 0 else 0
        R_bulk_2 = (d_ij / 2) / (k_weight * np.pi * r2**2) if r2 > 0 else 0
        R_bulk = R_bulk_1 + R_bulk_2

        # Contact resistance.
        #   Hertzian mode (point contact, a ≪ r):
        #     R_constriction = 1/(2a)   — Maxwell spreading (Holm 1967)
        #     Exact for point-contact-on-halfspace geometry.
        #   Physics mode (surface contact via Tabor + hemisphere caps):
        #     R_constriction = (1 - a/r_min)^1.5 / (2a)   — Mikic (1974)
        #     Rigorous correction for finite contact on a finite cylinder:
        #     reduces to Maxwell when a/r_min → 0, and vanishes as a → r_min
        #     (full contact, no constriction left, bulk alone dominates).
        #     Replaces the earlier phenomenological 'Maxwell + 2δ/A film'
        #     ansatz — same qualitative saturation behaviour but derived.
        r_min_real = min(r1, r2)  # μm (smaller sphere's radius)
        R_Maxwell = 1.0 / (k_weight * 2 * a_contact) if a_contact > 0 else 1e12
        if contact_mode == 'physics' and a_contact > 0 and r_min_real > 0:
            # Clamp a to r_min — our plastic cap 2πR_min² gives a > r_min, which
            # is geometrically impossible for a disk contact between spheres.
            a_eff = min(a_contact, r_min_real)
            psi = max(1.0 - a_eff / r_min_real, 0.0) ** 1.5
            if psi > 1e-4:
                R_constriction = 1.0 / (k_weight * 2 * a_eff * psi)
            else:
                # Full contact limit: spreading vanishes, R_bulk carries it.
                R_constriction = 0.0
        else:
            R_constriction = R_Maxwell
        # Legacy per-edge R_film field kept for backward compat with readers;
        # under Mikic it's folded into R_constriction so reported here as 0.
        R_film = 0.0

        edges.append({
            'id1': id1, 'id2': id2,
            'R_bulk': R_bulk,
            'R_constriction': R_constriction,
            'R_Maxwell': R_Maxwell,
            'R_film': R_film,
            'R_total': R_bulk + R_constriction,
            'd_ij': d_ij,
            'A_contact': A_contact,
            # Raw-dump fields (both modes carry both areas for comparison)
            'A_hertzian': A_hertzian,
            'A_physics':  A_physics,
            # 5-case Tabor/volume/geom decomposition (None when not in physics regime)
            'A_components': A_components,
            'delta':       delta_sim,
            'delta_over_R': delta_over_R,
            'regime':      regime,
            'r1': r1, 'r2': r2,
            'type1': a1['type'], 'type2': a2['type'],
        })

    return {
        'nodes': target_ids,
        'edges': edges,
        'bottom': bottom_ids,
        'top': top_ids,
        'plate_z': plate_z,
        'box_x': box_x,
        'box_y': box_y,
        'scale': scale,
        'contact_mode': contact_mode,
        # Resistance-model tag:
        #   'maxwell' (point-contact only) for Hertzian
        #   'mikic'   (Mikic 1974 constriction w/ finite-cylinder correction)
        #              for Physics. Vanishes correctly at full-contact limit.
        'resistance_model': ('mikic' if contact_mode == 'physics'
                             else 'maxwell'),
    }


def solve_network(network_data, mode='full', return_field=False):
    """
    Solve resistor network for effective conductance.

    mode: 'full' (R_bulk + R_constriction),
          'bulk_only' (R_bulk, R_constriction=0),
          'constriction_only' (R_constriction, R_bulk=0)
    return_field: if True, also return per-node voltages and per-edge currents
                  (used by dump_network_raw for reviewer-auditable output).

    Returns:
        G_eff: effective conductance (normalized, ρ=1)
        sigma_ratio: σ_eff / σ_bulk
        field (optional): {'node_V': {id: V}, 'edge_records': [{...}]}
    """
    nodes = network_data['nodes']
    edges = network_data['edges']
    bottom = network_data['bottom']
    top = network_data['top']
    scale = network_data['scale']
    plate_z = network_data['plate_z']
    box_x = network_data['box_x']
    box_y = network_data['box_y']

    if not bottom or not top or not edges:
        if return_field:
            return None, None, None
        return None, None

    # Build networkx graph to find percolating component
    import networkx as nx
    G_nx = nx.Graph()
    for e in edges:
        G_nx.add_edge(e['id1'], e['id2'])

    # Find components that connect bottom to top
    perc_nodes = set()
    for comp in nx.connected_components(G_nx):
        has_bot = len(comp & bottom) > 0
        has_top = len(comp & top) > 0
        if has_bot and has_top:
            perc_nodes |= comp

    if not perc_nodes:
        # Diagnostic: WHY did percolation fail?
        n_comp = nx.number_connected_components(G_nx)
        comp_sizes = sorted(
            (len(c) for c in nx.connected_components(G_nx)),
            reverse=True)[:5]
        reaches_bot = sum(1 for c in nx.connected_components(G_nx)
                         if len(c & bottom) > 0)
        reaches_top = sum(1 for c in nx.connected_components(G_nx)
                         if len(c & top) > 0)
        print(f"  No percolating component. DIAGNOSTIC:")
        print(f"    n_target_nodes={len(nodes)}, n_graph_nodes={G_nx.number_of_nodes()}, n_edges={G_nx.number_of_edges()}")
        print(f"    bottom={len(bottom)}, top={len(top)}  (plate_z={plate_z:.4f})")
        print(f"    n_components={n_comp}, top-5 sizes={comp_sizes}")
        print(f"    components reaching bottom={reaches_bot}, top={reaches_top} (need overlap for percolation)")
        if return_field:
            return None, None, None
        return None, None

    # Filter to percolating nodes only
    perc_bottom = bottom & perc_nodes
    perc_top = top & perc_nodes
    perc_edges = [e for e in edges if e['id1'] in perc_nodes and e['id2'] in perc_nodes]

    print(f"  Percolating component: {len(perc_nodes)} nodes, {len(perc_edges)} edges")

    # Node index mapping (percolating only)
    all_ids = list(perc_nodes)
    id_to_idx = {nid: i for i, nid in enumerate(all_ids)}
    N = len(all_ids)

    # Virtual source (idx=N) and sink (idx=N+1)
    source_idx = N
    sink_idx = N + 1
    total_nodes = N + 2

    # Build conductance matrix (sparse)
    row, col, val = [], [], []

    def add_conductance(i, j, g):
        if g <= 0:
            return
        # Add g to (i,i), (j,j) and subtract from (i,j), (j,i)
        row.extend([i, j, i, j])
        col.extend([i, j, j, i])
        val.extend([g, g, -g, -g])

    for e in perc_edges:
        i = id_to_idx[e['id1']]
        j = id_to_idx[e['id2']]

        if mode == 'full':
            R = e['R_total']
        elif mode == 'bulk_only':
            R = e['R_bulk'] if e['R_bulk'] > 0 else 1e-12
        elif mode == 'constriction_only':
            R = e['R_constriction']
        else:
            R = e['R_total']

        if R > 0:
            g = 1.0 / R
            add_conductance(i, j, g)

    # Connect bottom SE to source with large conductance (low resistance).
    # Adaptive g_boundary fixes σ-inflation observed across two regimes:
    #
    # (1) Original baseline anomaly (commit 1c24bd2): hardcoded g_boundary
    #     = 1e6 caused 10^6 boundary/bulk ratio for thin-pellet AM-AM
    #     graphs where Σg_bulk was ~160. spsolve LU mis-converged → V_source
    #     ~2e-6 instead of ~0.006 → σ inflated 3000×.
    #
    # (2) Stage-E inflation (this fix): network_conductivity is re-invoked
    #     by run_network_full_corrections.py with contacts.csv having
    #     contact_area × σ_factor (0.02-1.0) per Lawn fracture stage.
    #     For high-fracture cases, ALL AM-AM edges get scaled to ~0.02,
    #     making g_max_bulk and Σg_bulk both very small. The previous
    #     floor of 100 in `max(100*g_max, 100)` then forced boundary g_total
    #     = N_electrodes × 100 ≫ Σg_bulk, re-creating the ill-conditioning.
    #
    # Robust criterion (independent of edge magnitude):
    #   boundary g_total ≈ 100 × bulk g_total
    # so the matrix has dynamic range ~100, safely within spsolve LU
    # accuracy. Plus a 10×g_max safety floor so boundary R is at least 10×
    # smaller than any single bulk edge (boundary not the rate-limiting
    # step).
    g_max_bulk = 0.0
    sum_g_bulk = 0.0
    for e in perc_edges:
        if mode == 'full':
            R = e['R_total']
        elif mode == 'bulk_only':
            R = e['R_bulk'] if e['R_bulk'] > 0 else 1e-12
        elif mode == 'constriction_only':
            R = e['R_constriction']
        else:
            R = e['R_total']
        if R and R > 0:
            g = 1.0 / R
            sum_g_bulk += g
            g_max_bulk = max(g_max_bulk, g)

    n_electrodes = max(len(perc_bottom) + len(perc_top), 1)
    g_boundary_from_sum = 100.0 * sum_g_bulk / n_electrodes
    g_boundary_from_max = 10.0 * g_max_bulk
    g_boundary = max(g_boundary_from_sum, g_boundary_from_max, 1e-6)
    for bid in perc_bottom:
        add_conductance(id_to_idx[bid], source_idx, g_boundary)

    # Connect top SE to sink
    for tid in perc_top:
        add_conductance(id_to_idx[tid], sink_idx, g_boundary)

    # Build sparse Laplacian
    L = sparse.csr_matrix((val, (row, col)), shape=(total_nodes, total_nodes))

    # Right-hand side: inject current at source, extract at sink
    b = np.zeros(total_nodes)
    b[source_idx] = 1.0
    b[sink_idx] = -1.0

    # Ground one node to make system solvable (pin sink to V=0)
    # Zero out sink row and set diagonal to 1 (V_sink = 0)
    # Use CSR manipulation directly to avoid memory-heavy tolil() conversion
    L_csr = L.tocsr()
    start, end = L_csr.indptr[sink_idx], L_csr.indptr[sink_idx + 1]
    L_csr.data[start:end] = 0.0
    # Set diagonal
    sink_diag_mask = L_csr.indices[start:end] == sink_idx
    if sink_diag_mask.any():
        L_csr.data[start:end][sink_diag_mask] = 1.0
    else:
        # Fallback: rebuild with sink row replaced
        L_csr = L_csr.tolil()
        L_csr[sink_idx, :] = 0
        L_csr[sink_idx, sink_idx] = 1.0
        L_csr = L_csr.tocsr()
    b[sink_idx] = 0.0
    L_csr.eliminate_zeros()

    n_nodes = L_csr.shape[0]
    # 3-stage robust solve: CG → CG with ILU preconditioner → spsolve fallback.
    # Silent-None bug root cause was: pure CG can return info != 0 (not
    # converged) yet leave V nearly zeros, so V_source ≈ 0 triggered our
    # "V_source ≤ 0" bail-out even though the network was perfectly
    # percolating (e.g. input_9 with SE_perc = 99%).
    V = None
    solve_method = None
    try:
        if n_nodes > 30000:
            print(f"  Large network: {n_nodes} nodes — trying CG solver first...")
            try:
                V, info = cg(L_csr, b, tol=1e-8, maxiter=10000)
            except TypeError:
                V, info = cg(L_csr, b, atol=1e-8, maxiter=10000)
            V_src_trial = V[source_idx] if V is not None else 0.0
            if info == 0 and V_src_trial > 1e-12:
                solve_method = "cg"
            else:
                # CG failed or gave noisy V — try ILU-preconditioned CG
                print(f"  CG didn't converge (info={info}, V_src={V_src_trial:.3e}). "
                      f"Trying ILU-preconditioned CG...")
                try:
                    from scipy.sparse.linalg import spilu, LinearOperator
                    ilu = spilu(L_csr.tocsc(), drop_tol=1e-4, fill_factor=10)
                    M = LinearOperator(L_csr.shape, ilu.solve)
                    try:
                        V, info = cg(L_csr, b, M=M, tol=1e-8, maxiter=5000)
                    except TypeError:
                        V, info = cg(L_csr, b, M=M, atol=1e-8, maxiter=5000)
                    V_src_trial = V[source_idx] if V is not None else 0.0
                    if info == 0 and V_src_trial > 1e-12:
                        solve_method = "cg+ilu"
                    else:
                        raise RuntimeError(f"ILU-CG failed (info={info}, V_src={V_src_trial:.3e})")
                except Exception as ilu_err:
                    print(f"  ILU-CG failed: {ilu_err}. Falling back to direct spsolve...")
                    V = spsolve(L_csr, b)
                    solve_method = "spsolve_fallback"
        else:
            V = spsolve(L_csr, b)
            solve_method = "spsolve"
    except Exception as e:
        print(f"  Network solve failed: {e}")
        if return_field:
            return None, None, None
        return None, None

    if solve_method:
        print(f"  Solve: {solve_method}")

    V_source = V[source_idx]
    V_sink = V[sink_idx]  # = 0

    if V_source <= 0:
        if return_field:
            return None, None, None
        return None, None

    # G_eff = I / ΔV = 1.0 / V_source  (since I=1, V_sink=0)
    G_eff = 1.0 / V_source

    # ── Sanity check: G_eff must satisfy G_eff ≤ Σg_bulk (mathematical
    #    upper bound for any electrical network — all bulk edges in
    #    parallel between source and sink).
    #    spsolve LU mis-converges for some sparse-graph topologies (e.g.
    #    Stage E modified contacts where σ_factor scaling creates wide
    #    g dynamic range), producing G_eff > Σg_bulk by 5-10×. Detect
    #    this violation and retry with CG (which handles ill-conditioning
    #    better via iterative solver and natural regularization).
    sum_g_check = 0.0
    for e in perc_edges:
        if mode == 'full':       _R = e['R_total']
        elif mode == 'bulk_only': _R = e['R_bulk'] if e['R_bulk'] > 0 else 1e-12
        elif mode == 'constriction_only': _R = e['R_constriction']
        else:                     _R = e['R_total']
        if _R and _R > 0:
            sum_g_check += 1.0 / _R

    if G_eff > sum_g_check * 1.1 and solve_method == 'spsolve':
        # spsolve gave non-physical G_eff (mathematical bound G ≤ Σg
        # violated). Threshold 1.1 catches even mild violations; basic
        # numerical noise typically stays within 1.05.
        if os.environ.get('NETWORK_DEBUG'):
            print(f"  ⚠ spsolve G_eff={G_eff:.3e} > 1.1·Σg={sum_g_check:.3e} "
                  f"— retrying with CG …")
        cg_succeeded = False
        try:
            try:
                V_cg, info_cg = cg(L_csr, b, tol=1e-8, maxiter=20000)
            except TypeError:
                V_cg, info_cg = cg(L_csr, b, atol=1e-8, maxiter=20000)
            V_src_cg = V_cg[source_idx] if V_cg is not None else 0.0
            if info_cg == 0 and V_src_cg > 1e-12:
                G_eff_cg = 1.0 / V_src_cg
                if G_eff_cg <= sum_g_check * 1.1:
                    # CG result mathematically valid — adopt it
                    V = V_cg
                    V_source = V_src_cg
                    G_eff = G_eff_cg
                    solve_method = "cg_after_spsolve"
                    cg_succeeded = True
                    if os.environ.get('NETWORK_DEBUG'):
                        print(f"  ✓ CG retry succeeded: G_eff={G_eff:.3e}, "
                              f"G/Σg={G_eff/sum_g_check:.3f}")
                elif os.environ.get('NETWORK_DEBUG'):
                    print(f"  ✗ CG retry insufficient: G_eff_cg={G_eff_cg:.3e} "
                          f"still > 1.1·Σg={1.1*sum_g_check:.3e}")
        except Exception as cg_err:
            if os.environ.get('NETWORK_DEBUG'):
                print(f"  ✗ CG retry failed: {cg_err}")

        if not cg_succeeded:
            # Both solvers gave non-physical G_eff for this topology.
            # Return None instead of propagating the garbage value to σ_eff.
            # This typically happens for σ_e on very-small graphs (~10³
            # nodes) where the boundary-to-interior ratio exceeds 50 %
            # — the AM-AM percolation is geometrically too weak for any
            # solver to reliably extract σ_e. The case is then excluded
            # by the section7 anomaly filter rather than producing a
            # wildly inflated σ value.
            if os.environ.get('NETWORK_DEBUG'):
                print(f"  ⚠ Both spsolve and CG produced G/Σg > 1.2 — "
                      f"returning None (case fundamentally ill-conditioned)")
            if return_field:
                return None, None, None
            return None, None

    # ── Anomaly diagnostic: sanity-bound G_eff against sum-of-conductances ─
    # Theoretical upper bound: G_eff ≤ Σ g  (all edges in parallel between
    # source and sink — physically impossible to exceed). When numerical
    # spsolve mis-converges for ill-conditioned topologies (sparse top
    # electrode + dense bulk), V_source can come out vanishingly small and
    # make G_eff exceed Σ g by orders of magnitude. Emit a clear warning so
    # downstream scripts can flag/exclude the case rather than silently
    # propagate a non-physical σ.
    if os.environ.get('NETWORK_DEBUG'):
        sum_g_bulk = 0.0
        for e in perc_edges:
            R = e['R_total'] if mode == 'full' else (
                e['R_bulk'] if mode == 'bulk_only' else e['R_constriction'])
            if R and R > 0:
                sum_g_bulk += 1.0 / R
        print(f"  DEBUG[{mode}]: V_source={V_source:.4e}  G_eff={G_eff:.4e}  "
              f"Σg_bulk={sum_g_bulk:.4e}  G/Σg={G_eff/sum_g_bulk:.4f}  "
              f"perc(b/t)={len(perc_bottom)}/{len(perc_top)}",
              flush=True)
        if G_eff > sum_g_bulk * 2:
            print(f"  ⚠ G_eff exceeds Σg×2 — NUMERICAL ANOMALY (likely "
                  f"ill-conditioned Laplacian for this topology)", flush=True)

    # Convert to σ_eff / σ_bulk
    # G_eff is in normalized units (ρ=1)
    # σ_eff = G_eff × L / A where L = plate_z*scale (μm), A = box_x*box_y*scale² (μm²)
    T_um = plate_z * scale
    A_um2 = box_x * box_y * scale**2

    # σ_ratio = σ_eff / σ_bulk = G_eff × T / A  (dimensionless when ρ=1)
    sigma_ratio = G_eff * T_um / A_um2

    if return_field:
        # Per-node voltages (percolating component only)
        node_V = {nid: float(V[id_to_idx[nid]]) for nid in all_ids}
        # Per-edge currents I = G·(V_i - V_j) for the chosen mode
        edge_records = []
        for e in perc_edges:
            i, j = id_to_idx[e['id1']], id_to_idx[e['id2']]
            if mode == 'full':
                R = e['R_total']
            elif mode == 'bulk_only':
                R = e['R_bulk'] if e['R_bulk'] > 0 else 1e-12
            elif mode == 'constriction_only':
                R = e['R_constriction']
            else:
                R = e['R_total']
            g = 1.0 / R if R > 0 else 0.0
            dV = V[i] - V[j]
            I_edge = g * dV
            edge_records.append({
                'id1': e['id1'], 'id2': e['id2'],
                'type1': e['type1'], 'type2': e['type2'],
                'delta': e['delta'], 'delta_over_R': e['delta_over_R'],
                'regime': e['regime'],
                'r1': e['r1'], 'r2': e['r2'], 'd_ij': e['d_ij'],
                'A_hertzian': e['A_hertzian'], 'A_physics': e['A_physics'],
                'A_used':    e['A_contact'],
                'R_bulk': e['R_bulk'], 'R_constr': e['R_constriction'],
                'R_total': e['R_total'],
                'V1': float(V[i]), 'V2': float(V[j]),
                'I':  float(I_edge),
                'abs_I': float(abs(I_edge)),
            })
        field = {
            'node_V': node_V,
            'edge_records': edge_records,
            'V_source': float(V_source),
            'G_eff':    float(G_eff),
            'sigma_ratio': float(sigma_ratio),
            'n_perc_nodes': len(all_ids),
            'n_perc_edges': len(perc_edges),
        }
        return G_eff, sigma_ratio, field

    return G_eff, sigma_ratio


def dump_network_raw(dump_dir, atoms_raw, net, field_full, tag='hertzian'):
    """Write per-node/per-edge raw CSV + solution JSON for reviewer audit.
    dump_dir/
      edges_<tag>.csv    — one row per percolating edge
      nodes_<tag>.csv    — one row per percolating node
      solution_<tag>.json — summary (σ, V_source, top-10 hot edges)
    """
    if not field_full:
        return
    os.makedirs(dump_dir, exist_ok=True)
    import csv as _csv

    # edges.csv
    erecs = field_full.get('edge_records', [])
    if erecs:
        # Rank edges by |I| for hot-spot analysis
        ranked = sorted(range(len(erecs)), key=lambda i: erecs[i]['abs_I'], reverse=True)
        for rank, idx in enumerate(ranked):
            erecs[idx]['hotspot_rank'] = rank + 1
        edge_csv = os.path.join(dump_dir, f'edges_{tag}.csv')
        with open(edge_csv, 'w', newline='') as f:
            w = _csv.DictWriter(f, fieldnames=list(erecs[0].keys()))
            w.writeheader()
            w.writerows(erecs)

    # nodes.csv
    nvs = field_full.get('node_V', {})
    if nvs:
        node_csv = os.path.join(dump_dir, f'nodes_{tag}.csv')
        with open(node_csv, 'w', newline='') as f:
            w = _csv.writer(f)
            w.writerow(['id', 'type', 'x', 'y', 'z', 'radius', 'V'])
            for nid, V in nvs.items():
                a = atoms_raw.get(nid)
                if a is None:
                    continue
                w.writerow([nid, a.get('type'), a.get('x'), a.get('y'),
                            a.get('z'), a.get('radius'), V])

    # solution.json: σ, V_source, top-10 hot edges, basic stats
    top10 = []
    if erecs:
        for r in erecs[:10] if erecs else []:
            pass  # placeholder (erecs not re-sorted here)
        top10_ranked = sorted(erecs, key=lambda r: r['abs_I'], reverse=True)[:10]
        top10 = [{k: r[k] for k in ('id1', 'id2', 'type1', 'type2',
                                     'delta_over_R', 'A_hertzian', 'A_physics',
                                     'A_used', 'abs_I', 'hotspot_rank')
                  if k in r} for r in top10_ranked]
    summary = {
        'tag': tag,
        'sigma_ratio': field_full.get('sigma_ratio'),
        'G_eff':        field_full.get('G_eff'),
        'V_source':     field_full.get('V_source'),
        'n_perc_nodes': field_full.get('n_perc_nodes'),
        'n_perc_edges': field_full.get('n_perc_edges'),
        'contact_mode': net.get('contact_mode', 'unknown'),
        'top10_hot_edges': top10,
    }
    with open(os.path.join(dump_dir, f'solution_{tag}.json'), 'w') as f:
        json.dump(summary, f, indent=2)


def run_decomposition(atoms_raw, contacts_raw, target_types, scale,
                      plate_z, box_x=0.05, box_y=0.05,
                      sigma_bulk=SIGMA_BULK_DEFAULT, results_dir=None,
                      type_map=None, contact_mode='hertzian',
                      dump_raw_dir=None, dump_tag=None):
    """
    Run full decomposition analysis:
    1. FULL (R_bulk + R_constriction): physical ground truth
    2. CONTACT_FREE (R_constriction=0): ideal contact upper bound
    3. CONSTRICTION_ONLY (R_bulk=0): spreading resistance limit

    contact_mode: 'hertzian' (default, LIGGGHTS area) or 'physics' (Tabor+volume)
    dump_raw_dir: if set, write edges/nodes CSV + solution JSON here
    dump_tag: file suffix for raw dump (e.g. 'hertzian_ionic', 'physics_ionic')

    Also computes analytical Bruggeman prediction (σ = σ₀ × φ^1.5) for comparison.
    """
    print(f"  Building resistor network ({len(target_types)} target types, "
          f"contact_mode={contact_mode})...")
    net = build_network(atoms_raw, contacts_raw, target_types, scale,
                        plate_z, box_x, box_y, results_dir=results_dir,
                        type_map=type_map, contact_mode=contact_mode)

    if net is None:
        print("  No network found")
        return None

    n_nodes = len(net['nodes'])
    n_edges = len(net['edges'])
    n_bottom = len(net['bottom'])
    n_top = len(net['top'])
    print(f"  Network: {n_nodes} nodes, {n_edges} edges, {n_bottom} bottom, {n_top} top")

    # Edge statistics
    R_bulks = [e['R_bulk'] for e in net['edges']]
    R_constrs = [e['R_constriction'] for e in net['edges']]
    R_totals = [e['R_total'] for e in net['edges']]

    bulk_frac = np.mean([rb/(rb+rc) for rb, rc in zip(R_bulks, R_constrs) if rb+rc > 0])
    print(f"  R_bulk fraction: {bulk_frac:.1%} (vs R_constriction: {1-bulk_frac:.1%})")

    # === Run 1: FULL ===
    print("  Solving FULL network (bulk + constriction)...")
    if dump_raw_dir:
        G_full, sigma_full, _field = solve_network(net, mode='full', return_field=True)
        if _field and dump_tag:
            dump_network_raw(dump_raw_dir, atoms_raw, net, _field, tag=dump_tag)
    else:
        G_full, sigma_full = solve_network(net, mode='full')

    # === Run 2: CONTACT-FREE (ideal contacts, upper bound) ===
    print("  Solving CONTACT_FREE network (R_constriction=0)...")
    G_bulk, sigma_cf = solve_network(net, mode='bulk_only')

    # === Run 3: CONSTRICTION ONLY (spreading resistance limit) ===
    print("  Solving CONSTRICTION_ONLY network (R_bulk=0)...")
    G_constr, sigma_constr_net = solve_network(net, mode='constriction_only')

    # === Volume fraction & Bruggeman analytical prediction ===
    V_se = sum(4/3 * np.pi * atoms_raw[aid]['radius']**3
               for aid in net['nodes'])
    V_box = box_x * box_y * plate_z
    phi_se = V_se / V_box if V_box > 0 else 0
    # Analytical Bruggeman EMT: σ_eff/σ_bulk = φ^1.5 (spheres, n=3/2)
    sigma_bruggeman = phi_se ** 1.5 if phi_se > 0 else 0

    # Active fraction: percolating nodes / total nodes
    import networkx as nx
    G_active = nx.Graph()
    for e in net['edges']:
        G_active.add_edge(e['id1'], e['id2'])

    # Bottom-reachable (electronic active)
    bottom_reachable = set()
    # Top+bottom percolating
    perc_nodes = set()
    for comp in nx.connected_components(G_active):
        has_bot = len(comp & net['bottom']) > 0
        has_top = len(comp & net['top']) > 0
        if has_bot:
            bottom_reachable |= comp
        if has_bot and has_top:
            perc_nodes |= comp

    active_fraction = len(bottom_reachable) / n_nodes if n_nodes > 0 else 0
    perc_fraction = len(perc_nodes) / n_nodes if n_nodes > 0 else 0

    # Results
    results = {
        'contact_mode': contact_mode,
        'resistance_model': ('mikic' if contact_mode == 'physics'
                             else 'maxwell'),
        'n_nodes': n_nodes,
        'n_edges': n_edges,
        'n_bottom': n_bottom,
        'n_top': n_top,
        'phi_se': round(phi_se, 4),
        'bulk_resistance_fraction': round(bulk_frac, 4),
        'active_fraction': round(active_fraction, 4),
        'percolating_fraction': round(perc_fraction, 4),
        'sigma_full': round(sigma_full, 8) if sigma_full else None,
        'sigma_bulk_net': round(sigma_cf, 8) if sigma_cf else None,  # contact-free (legacy key kept for compat)
        'sigma_constr_net': round(sigma_constr_net, 8) if sigma_constr_net else None,
        'sigma_full_mScm': round(sigma_full * sigma_bulk * 1000, 6) if sigma_full else None,
        'sigma_bulk_net_mScm': round(sigma_cf * sigma_bulk * 1000, 6) if sigma_cf else None,
        'sigma_constr_net_mScm': round(sigma_constr_net * sigma_bulk * 1000, 6) if sigma_constr_net else None,
        'sigma_bruggeman': round(sigma_bruggeman, 8),
        'sigma_bruggeman_mScm': round(sigma_bruggeman * sigma_bulk * 1000, 6),
    }

    # Overestimation ratios
    if sigma_cf and sigma_full:
        results['R_brug_over_full'] = round(sigma_cf / sigma_full, 4)  # contact-free / full
    if sigma_bruggeman > 0 and sigma_full:
        results['R_bruggeman_over_full'] = round(sigma_bruggeman * sigma_bulk * 1000 / (sigma_full * sigma_bulk * 1000), 4)

    # Print summary
    print(f"\n  ═══ Decomposition Results ═══")
    print(f"  φ = {phi_se:.4f}")
    print(f"  R_bulk fraction: {bulk_frac:.1%} | R_constriction: {1-bulk_frac:.1%}")
    print(f"")
    print(f"  {'Mode':<22s} {'σ/σ_bulk':>10s} {'σ (mS/cm)':>10s}")
    print(f"  {'─'*44}")
    if sigma_full:
        print(f"  {'FULL (ground truth)':22s} {sigma_full:10.6f} {sigma_full*sigma_bulk*1000:10.4f}")
    if sigma_cf:
        print(f"  {'CONTACT_FREE (upper)':22s} {sigma_cf:10.6f} {sigma_cf*sigma_bulk*1000:10.4f}")
    if sigma_constr_net:
        print(f"  {'CONSTRICTION_ONLY':22s} {sigma_constr_net:10.6f} {sigma_constr_net*sigma_bulk*1000:10.4f}")
    print(f"  {'Bruggeman (φ^1.5)':22s} {sigma_bruggeman:10.6f} {sigma_bruggeman*sigma_bulk*1000:10.4f}")
    print(f"")
    if sigma_cf and sigma_full:
        print(f"  Contact-free overestimation: {sigma_cf/sigma_full:.2f}×")
    if sigma_bruggeman > 0 and sigma_full:
        print(f"  Bruggeman EMT overestimation: {sigma_bruggeman/sigma_full:.2f}×")

    return results


def _run_all_networks(atoms_raw, contacts_raw, target_types, am_types, type_map,
                       scale, plate_z, box_x, box_y, output_dir,
                       contact_mode='hertzian', dump_raw_dir=None):
    """Run ionic + electronic + thermal decomposition under a fixed contact_mode.
    Returns the merged ionic-centric results dict.
    """
    tag_ionic = f"{contact_mode}_ionic"
    tag_el    = f"{contact_mode}_electronic"
    tag_th    = f"{contact_mode}_thermal"

    print("\n" + "="*60)
    print(f"IONIC CONDUCTIVITY (SE-SE network) — contact_mode={contact_mode}")
    print("="*60)
    results = run_decomposition(atoms_raw, contacts_raw, target_types, scale,
                                plate_z, box_x, box_y, sigma_bulk=SIGMA_BULK_DEFAULT,
                                results_dir=output_dir, type_map=type_map,
                                contact_mode=contact_mode,
                                dump_raw_dir=dump_raw_dir, dump_tag=tag_ionic)

    results_el = None
    if am_types:
        print("\n" + "="*60)
        print(f"ELECTRONIC CONDUCTIVITY (AM-AM network) — contact_mode={contact_mode}")
        print("="*60)
        try:
            results_el = run_decomposition(atoms_raw, contacts_raw, am_types, scale,
                                           plate_z, box_x, box_y,
                                           sigma_bulk=SIGMA_AM_ELECTRONIC,
                                           type_map=type_map,
                                           contact_mode=contact_mode,
                                           dump_raw_dir=dump_raw_dir, dump_tag=tag_el)
        except Exception as e:
            print(f"  Electronic solver failed: {e}")

    results_th = None
    try:
        print("\n" + "="*60)
        print(f"THERMAL CONDUCTIVITY (ALL contacts) — contact_mode={contact_mode}")
        print("="*60)
        all_types = list(type_map.keys())
        results_th = run_decomposition(atoms_raw, contacts_raw, all_types, scale,
                                       plate_z, box_x, box_y, sigma_bulk=K_SE_THERMAL,
                                       type_map=type_map,
                                       contact_mode=contact_mode,
                                       dump_raw_dir=dump_raw_dir, dump_tag=tag_th)
    except Exception as e:
        print(f"  Thermal solver failed: {e}")

    # Merge electronic + thermal into ionic-centric dict (matches legacy schema)
    if results:
        if results_el:
            results['electronic_sigma_full']      = results_el.get('sigma_full')
            results['electronic_sigma_full_mScm'] = results_el.get('sigma_full_mScm')
            results['electronic_R_brug']          = results_el.get('R_brug_over_full')
            results['electronic_bulk_frac']       = results_el.get('bulk_resistance_fraction')
            results['electronic_n_nodes']         = results_el.get('n_nodes')
            results['electronic_n_edges']         = results_el.get('n_edges')
            results['electronic_active_fraction']      = results_el.get('active_fraction')
            results['electronic_percolating_fraction'] = results_el.get('percolating_fraction')
        if results_th:
            results['thermal_sigma_full']      = results_th.get('sigma_full')
            results['thermal_sigma_full_mScm'] = results_th.get('sigma_full_mScm')
            results['thermal_R_brug']          = results_th.get('R_brug_over_full')
            results['thermal_bulk_frac']       = results_th.get('bulk_resistance_fraction')
    return results


if __name__ == '__main__':
    import argparse
    sys.path.insert(0, os.path.dirname(__file__))
    from analyze_contacts import load_atoms_raw, load_contacts_raw

    parser = argparse.ArgumentParser(description='DEM-Native Ionic Transport Solver')
    parser.add_argument('atoms_csv', help='atoms.csv path')
    parser.add_argument('contacts_csv', help='contacts.csv path')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    parser.add_argument('-t', '--type-map', default='1:AM_S,2:SE', help='Type map')
    parser.add_argument('-s', '--scale', type=int, default=1000, help='Scale factor')
    parser.add_argument('--contact-mode', choices=['hertzian', 'physics', 'both'],
                        default='both',
                        help="Contact area model: 'hertzian' (DEM-native LIGGGHTS area), "
                             "'physics' (Tabor+volume, literature-anchored), "
                             "'both' (run each and emit *_hertzian/*_physics + dual JSON)")
    parser.add_argument('--dump-raw-dir', type=str, default=None,
                        help='If set, write per-edge/per-node raw CSV + solution JSON here')
    args = parser.parse_args()

    # Parse type map
    type_map = {}
    for pair in args.type_map.split(','):
        k, v = pair.split(':')
        type_map[int(k)] = v.strip()

    target_types = [k for k, v in type_map.items() if v == 'SE']
    am_types     = [k for k, v in type_map.items() if 'AM' in v]

    atoms_raw, _    = load_atoms_raw(args.atoms_csv)
    contacts_raw, _ = load_contacts_raw(args.contacts_csv)
    print(f"Loaded {len(atoms_raw)} atoms, {len(contacts_raw)} contacts")

    mesh_file = os.path.join(args.output, 'mesh_info.json')
    if os.path.exists(mesh_file):
        with open(mesh_file) as f:
            plate_z = json.load(f)['plate_z']
    else:
        # Fallback: use max z of particle CENTERS (NOT z+radius). Adding the
        # radius overshoots the actual plate plane by one particle radius,
        # which makes z_top = plate_z - r_se×2 land above every SE center →
        # silent percolation=0 (observed for results/ cases missing
        # mesh_info.json). See dem_analysis_core.get_plate_z for matching fix.
        plate_z = max(a['z'] for a in atoms_raw.values())

    box_x, box_y = 0.05, 0.05
    ip_path = os.path.join(args.output, 'input_params.json')
    if os.path.exists(ip_path):
        with open(ip_path) as f:
            ip = json.load(f)
        box_x = ip.get('box_x', 0.05)
        box_y = ip.get('box_y', 0.05)

    print(f"box={box_x}×{box_y}, plate_z={plate_z:.6f}, scale={args.scale}")

    modes_to_run = (['hertzian', 'physics'] if args.contact_mode == 'both'
                    else [args.contact_mode])
    per_mode_results = {}
    for cm in modes_to_run:
        res = _run_all_networks(atoms_raw, contacts_raw, target_types, am_types,
                                 type_map, args.scale, plate_z, box_x, box_y,
                                 args.output, contact_mode=cm,
                                 dump_raw_dir=args.dump_raw_dir)
        per_mode_results[cm] = res
        if res:
            out_path = os.path.join(args.output, f'network_conductivity_{cm}.json')
            with open(out_path, 'w') as f:
                json.dump(res, f, indent=2)
            print(f"\nResults saved: {out_path}")

    # Dual-view JSON (when both modes ran): elastic vs plastic side-by-side
    if len(per_mode_results) == 2 and all(per_mode_results.values()):
        rH = per_mode_results['hertzian']
        rP = per_mode_results['physics']
        def _ratio(a, b):
            try:
                return round(float(a) / float(b), 4) if (a and b and float(b) != 0) else None
            except Exception:
                return None
        dual = {
            'hertzian': rH,
            'physics':  rP,
            'ratio_physics_over_hertzian': {
                'sigma_full':        _ratio(rP.get('sigma_full'),        rH.get('sigma_full')),
                'sigma_constr_net':  _ratio(rP.get('sigma_constr_net'),  rH.get('sigma_constr_net')),
                'electronic_sigma_full': _ratio(rP.get('electronic_sigma_full'),
                                                rH.get('electronic_sigma_full')),
                'thermal_sigma_full':    _ratio(rP.get('thermal_sigma_full'),
                                                rH.get('thermal_sigma_full')),
            }
        }
        dual_path = os.path.join(args.output, 'network_conductivity_dual.json')
        with open(dual_path, 'w') as f:
            json.dump(dual, f, indent=2)
        print(f"Dual-view saved:  {dual_path}")

    # Back-compat: legacy filename points to Hertzian result (existing webapp reads this)
    if 'hertzian' in per_mode_results and per_mode_results['hertzian']:
        legacy_path = os.path.join(args.output, 'network_conductivity.json')
        with open(legacy_path, 'w') as f:
            json.dump(per_mode_results['hertzian'], f, indent=2)
        print(f"Legacy-compat:    {legacy_path}")
