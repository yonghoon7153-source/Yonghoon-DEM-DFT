"""3D-viewer auxiliary data extractor.

Computes per-particle and per-contact metadata that the front-end
viewer uses to colour / size / filter particles in different "view
modes":

  brittle hotspots   — AM-AM δ/R > Auerbach threshold
  cluster coloring   — percolating vs broken vs dead components
  stress hot spots   — per-particle max contact stress (MPa)
  coverage heat      — per-AM SE coverage (%)
  SE Tabor regime    — SE particles classified into idle / elastic /
                       yield-onset / fully-plastic by their worst
                       contact, with optional pair-type filter
                       (SE-SE vs AM_P-SE vs AM_S-SE).  Replaces the
                       legacy "fracture-prone SE" mode whose name was
                       misleading: SE is ductile and does not
                       brittle-fracture; it plastically flows.

All scales are in display units (μm, MPa) so the front-end can use
them directly without further conversion.

Outputs a single dict that the Flask /3d-data endpoint merges into
its response. Pure-function with no side effects.
"""
from __future__ import annotations
from typing import Iterable
import math
from collections import defaultdict

# Brittle fracture classification — single source of truth in
# scripts/fracture_model.py. Re-exported aliases below preserve any
# external callers that previously imported from this module.
from fracture_model import (
    fracture_classify_force_sim as fracture_stage,     # FORCE-based ← used here
    fracture_classify_sim,                             # δ-based (Hertzian; kept for callers)
    auerbach_delta_critical as _auerbach_m,            # SI-only base
    K_IC_AM_S, K_IC_AM_P, E_AM, NU_AM, A_AUERBACH,
)
# Why force-based: LIGGGHTS uses Hooke (linear) contact, so the
# Hertzian P ∝ δ^(3/2) assumption behind the δ-based classifier does
# NOT hold.  F/P_c with Lawn 1998 §3.4 force multipliers (1, 3, 11, 32)
# is the recommended, model-agnostic form and matches the Stage E
# pipeline (run_network_full_corrections.py) + the diagnostic script
# (scripts/diag_brittle_per_type.py).  Prior δ-based version severely
# under-counted AM_P damage because the Hooke δ→F mapping differs from
# Hertzian, making large-R AM_P appear less cracked than it actually is.

# SE Tabor plastic regime thresholds (kept for SE-side highlighting).
# Same δ/R values are reused for the AM-SE interface — the soft side
# (SE) yields first regardless of which AM it contacts.
DR_SE_PLASTIC = 0.0078    # fully plastic Tabor (H ≈ 3·σ_y, δ/R cutoff)
DR_SE_YIELD   = 0.0011    # elastic-plastic transition (yield onset)


# Regime rank for "worst state across contacts" aggregation per particle.
_REGIME_RANK = {'elastic': 1, 'yield': 2, 'plastic': 3}


def _classify_dr(dr: float) -> str:
    """Return one of 'elastic' / 'yield' / 'plastic' for an SE-touching
    contact.  A particle with no recorded contact is treated as 'idle'
    upstream (this function never returns 'idle').
    """
    if dr > DR_SE_PLASTIC:
        return 'plastic'
    if dr > DR_SE_YIELD:
        return 'yield'
    return 'elastic'


def auerbach_delta_critical(R_min_sim: float, K_IC: float,
                             E: float = E_AM, nu: float = NU_AM,
                             A: float = A_AUERBACH,
                             scale: float = 1000.0) -> float:
    """Sim-units wrapper around fracture_model.auerbach_delta_critical.
    Kept for backward compatibility with any caller that imported it
    from viewer3d_data.
    """
    R_min_m = R_min_sim / scale
    return _auerbach_m(R_min_m, K_IC, E=E, nu=nu, A=A) * scale


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
    se_stress_pairs: list[dict] = []      # SE-SE pairs above yield (legacy key)
    am_se_stress_pairs: list[dict] = []   # AM-SE pairs above yield (NEW)

    # ── Per-particle fracture aggregates (Phase A1) ──────────────────────
    # For every AM particle, track:
    #   - particle_max_fpc: largest F/P_c (mult) it experienced
    #   - particle_worst_stage: the stage at that worst contact
    #   - particle_n_brittle: count of non-intact AM-AM contacts
    # particle_worst_partner_brittle: the partner id at the worst contact
    particle_max_fpc:        dict[int, float] = defaultdict(float)
    particle_worst_stage:    dict[int, str]   = {}
    particle_n_brittle:      dict[int, int]   = defaultdict(int)
    particle_worst_partner_brittle: dict[int, int] = {}
    particle_worst_pair_type:       dict[int, str] = {}

    # ── Stress-chain segment list (Phase A4) ─────────────────────────────
    # Every AM-AM contact (intact OR brittle) with non-zero force, so the
    # viewer can render load-path lines (thickness ∝ log(F/P_c+1)).
    # Capped to top-N by mult to keep payload reasonable.
    stress_chain_segments: list[dict] = []

    # ── AM_P-AM_P brittle edges (Phase A3 input — graph for skeleton) ────
    # connected-component pass happens AFTER the loop completes.
    am_p_brittle_edges: list[tuple[int, int]] = []

    # Per-SE-particle worst regime, split by which AM type (if any) it
    # touches.  Three independent state tracks because the view-mode
    # filter lets the user toggle pair-type (SE-SE / AM_P-SE / AM_S-SE).
    # Values are the regime rank from _REGIME_RANK so 'plastic' wins
    # over 'yield' wins over 'elastic'.
    se_state_se_se:   dict[int, int] = {}
    se_state_am_p_se: dict[int, int] = {}
    se_state_am_s_se: dict[int, int] = {}

    # Per-SE-particle ENGAGEMENT tracking (across ALL contact partners).
    # The user wants to see SE that has contacts but few-of-them-plastic
    # ("pre-switch SE in AM-AM void" or "incomplete plastic flow that
    # might leave micro-pores after compaction release").  We count
    # contacts by regime per particle, plus track the absolute max δ/R
    # to derive an "over-plastic excess" score for micro-pore risk.
    se_contact_counts: dict[int, dict[str, int]] = defaultdict(
        lambda: {'plastic': 0, 'yield': 0, 'elastic': 0})
    se_dr_max:    dict[int, float] = defaultdict(float)   # any-partner δ/R max

    # Total pair counts per type, for the legend stats panel.  We also
    # track all-elastic pair counts (where SE just sits there in
    # Hertz-elastic regime, no plasticity) — visualised as the "idle SE
    # in AM-AM void" population the user wanted to surface.
    pair_counts = {
        'se_se':   {'elastic': 0, 'yield': 0, 'plastic': 0},
        'am_p_se': {'elastic': 0, 'yield': 0, 'plastic': 0},
        'am_s_se': {'elastic': 0, 'yield': 0, 'plastic': 0},
    }
    # Track every SE particle that participated in any contact (so the
    # frontend can compute idle = all_SE - (any-regime SE)).
    se_with_contact: set[int] = set()

    pressure_conv = scale / 1.0e6     # sim Pa → real MPa (calibrated to scale)

    def _bump_state(d: dict[int, int], sid: int, regime: str) -> None:
        rank = _REGIME_RANK[regime]
        if rank > d.get(sid, 0):
            d[sid] = rank

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
        dr = 0.0
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
            # FORCE-based: m = F/P_c with multipliers (1, 3, 11, 32) per
            # Lawn 1998 §3.4.  P_c here is the Auerbach onset force, not
            # an equivalent overlap.  See fracture_model.py and the
            # diagnostic script for agreement.
            stage, P_c, mult = fracture_stage(fn, r_min, ct, scale=scale)

            # Phase A1 — per-particle worst F/P_c
            for pid, other in ((i1, i2), (i2, i1)):
                if mult > particle_max_fpc[pid]:
                    particle_max_fpc[pid] = mult
                    particle_worst_stage[pid] = stage
                    particle_worst_partner_brittle[pid] = other
                    particle_worst_pair_type[pid] = ct
                if stage != 'intact':
                    particle_n_brittle[pid] += 1

            # Phase A4 — stress-chain segment (all AM-AM contacts incl. intact).
            # Filter on BOTH delta > 0 AND fn > 0 to match dem_analysis_core's
            # n_total_AM_AM (dashboard count).  LIGGGHTS dumps sometimes carry
            # lingering tangential-history fn > 0 with delta = 0, which inflated
            # earlier viewer counts vs the dashboard's 1692-style total.
            if fn > 0 and delta > 0:
                stress_chain_segments.append({
                    'id1': i1, 'id2': i2,
                    'mult': round(mult, 2),
                    'pair_type': ct,
                    'stage': stage,
                })

            # Phase A3 — AM_P-AM_P brittle edge (skeleton input)
            if ct == 'AM_P-AM_P' and mult >= 1.0:
                am_p_brittle_edges.append((i1, i2))

            if stage != 'intact':
                brittle_pairs.append({
                    'id1': i1, 'id2': i2,
                    'dr': round(dr, 4),
                    'mult': round(mult, 2),
                    'stage': stage,
                    'pressure_MPa': round(p_MPa, 1),
                    'pair_type': ct,
                })
            continue

        # ─── SE-touching contact (either SE-SE or AM-SE) ──────────────
        if not (is_se1 or is_se2):
            continue
        if dr <= 0:
            continue   # no overlap → not a real contact

        regime = _classify_dr(dr)

        # ── ENGAGEMENT bookkeeping (any-partner) ─────────────────────
        # Per-SE-particle contact tally by regime + worst-δ/R tracker,
        # so we can later compute (a) engagement_score = plastic-share
        # of contacts and (b) pore_risk = how-far-over-plastic the
        # worst contact is.  Counted ONCE per contact per SE — i.e.
        # for SE-SE both endpoints are SE so we bump both; for AM-SE
        # we only bump the SE side.  The AM endpoint's engagement is
        # not tracked (AM is rigid, doesn't yield).
        for sid in [i1, i2]:
            if type_map.get(int(atoms_by_id[sid].get('type', -1)), '?') == 'SE':
                se_contact_counts[sid][regime] += 1
                if dr > se_dr_max[sid]:
                    se_dr_max[sid] = dr

        if is_se1 and is_se2:
            pair_counts['se_se'][regime] += 1
            se_with_contact.add(i1); se_with_contact.add(i2)
            _bump_state(se_state_se_se, i1, regime)
            _bump_state(se_state_se_se, i2, regime)
            if regime != 'elastic':
                # Legacy se_stress_pairs key — yield+plastic only
                se_stress_pairs.append({
                    'id1': i1, 'id2': i2,
                    'dr': round(dr, 4),
                    'pressure_MPa': round(p_MPa, 1),
                    'plastic': regime == 'plastic',
                })
        else:
            # Mixed AM-SE contact.  Track which AM type so the filter
            # can distinguish AM_P-SE (small-soft against large-hard)
            # from AM_S-SE (small-soft against medium-hard).
            am_type = t1 if is_am1 else t2
            se_id   = i2 if is_am1 else i1
            se_with_contact.add(se_id)
            pair_key = 'am_p_se' if 'AM_P' in am_type else 'am_s_se'
            pair_counts[pair_key][regime] += 1
            target = (se_state_am_p_se if pair_key == 'am_p_se'
                       else se_state_am_s_se)
            _bump_state(target, se_id, regime)
            if regime != 'elastic':
                am_se_stress_pairs.append({
                    'id1': i1, 'id2': i2,
                    'se_id': se_id,
                    'am_type': am_type,
                    'pair_type': pair_key,    # 'am_p_se' or 'am_s_se'
                    'dr': round(dr, 4),
                    'pressure_MPa': round(p_MPa, 1),
                    'plastic': regime == 'plastic',
                })

    # ── Convert worst-regime rank back into labels per pair-type ──────
    _rank_to_label = {v: k for k, v in _REGIME_RANK.items()}

    def _emit_state_lists(state_dict: dict[int, int]) -> dict:
        out = {'elastic_ids': [], 'yield_ids': [], 'plastic_ids': []}
        for sid, rank in state_dict.items():
            label = _rank_to_label.get(rank)
            if label:
                out[f'{label}_ids'].append(int(sid))
        return out

    # All SE particle IDs, so the frontend can compute the "idle" set
    # (geometrically present in AM-AM voids but with no recorded
    # contact stress in any pair type) by exclusion.
    all_se_ids = [int(aid) for aid, a in atoms_by_id.items()
                  if type_map.get(int(a.get('type', -1)), '?') == 'SE']

    # ── ENGAGEMENT + PORE-RISK per SE particle ────────────────────────
    # engagement = (plastic + 0.5·yield) / total_contacts
    #   1.0 = every contact plastic → fully integrated in force chain
    #   0.0 = every contact pre-yield → "stuck SE", AM-AM bypassing
    #
    # pore_risk = max(0, dr_max − DR_SE_PLASTIC) / DR_SE_PLASTIC
    #   0 = right at Tabor plastic threshold (no excess)
    #   1 = 2× the threshold → micro-pore likely during spring-back
    #
    # Particles with NO contacts are excluded (they're the "void idle"
    # set, separate from "low engagement" — both are highlighted
    # differently in the frontend SE engagement view).
    se_engagement: dict[int, dict] = {}
    for sid in all_se_ids:
        c = se_contact_counts.get(sid)
        if not c:
            continue   # truly idle (no contacts) — emitted as null elsewhere
        n_p = c['plastic']; n_y = c['yield']; n_e = c['elastic']
        n_tot = n_p + n_y + n_e
        if n_tot == 0:
            continue
        score = (n_p + 0.5 * n_y) / n_tot
        # Payload-compact form: emit just the engagement score (single
        # float) per SE particle.  For fine-SE particulate cases the
        # corpus reaches 620k SE — a 6-field dict per particle would
        # produce a 60 MB JSON response that truncates over the dev-
        # server transport.  The frontend visualises by score only;
        # the auxiliary counts (n_plastic/n_yield/dr_max/pore_risk)
        # are no longer rendered (over-plastic overlay was removed in
        # the pore-risk semantics flip — commit 3c20a40).
        se_engagement[int(sid)] = round(score, 3)

    tabor_stats = {
        'pair_counts': pair_counts,
        'totals': {
            'se_se':   sum(pair_counts['se_se'].values()),
            'am_p_se': sum(pair_counts['am_p_se'].values()),
            'am_s_se': sum(pair_counts['am_s_se'].values()),
        },
        # Per-pair-type SE-particle counts at worst-regime (excludes
        # idle by construction; idle = total_SE - any-contact SE).
        'particle_counts': {
            'se_se':   {k: 0 for k in ('elastic', 'yield', 'plastic')},
            'am_p_se': {k: 0 for k in ('elastic', 'yield', 'plastic')},
            'am_s_se': {k: 0 for k in ('elastic', 'yield', 'plastic')},
        },
        'n_se_total':       len(all_se_ids),
        'n_se_with_contact': len(se_with_contact),
        'n_se_idle':        max(0, len(all_se_ids) - len(se_with_contact)),
    }
    for sid, rank in se_state_se_se.items():
        tabor_stats['particle_counts']['se_se'][_rank_to_label[rank]] += 1
    for sid, rank in se_state_am_p_se.items():
        tabor_stats['particle_counts']['am_p_se'][_rank_to_label[rank]] += 1
    for sid, rank in se_state_am_s_se.items():
        tabor_stats['particle_counts']['am_s_se'][_rank_to_label[rank]] += 1

    # ── Payload-size guard rails ──────────────────────────────────────
    # The full se_stress_pairs / am_se_stress_pairs lists can reach
    # 2-3 M entries on fine-SE particulate cases (every plastic-regime
    # contact emits one entry) → 360 MB JSON, untransportable.  Cap to
    # the top-N most-stressed pairs by pressure_MPa.  All frontend view
    # modes after commit 4d3f39b read per-particle state via
    # `se_engagement`, so these pair lists are now diagnostic only.
    _PAIR_CAP = 20_000
    if len(se_stress_pairs) > _PAIR_CAP:
        se_stress_pairs.sort(key=lambda p: p['pressure_MPa'], reverse=True)
        se_stress_pairs = se_stress_pairs[:_PAIR_CAP]
    if len(am_se_stress_pairs) > _PAIR_CAP:
        am_se_stress_pairs.sort(key=lambda p: p['pressure_MPa'], reverse=True)
        am_se_stress_pairs = am_se_stress_pairs[:_PAIR_CAP]

    # ── Phase A4 — cap stress-chain segments to top-N by mult ────────────
    # Typical AM-AM count ~1700, no cap needed.  Particulate cases with
    # very fine AM_S can hit 50k — cap at 5000 most-stressed.
    _SC_CAP = 5_000
    if len(stress_chain_segments) > _SC_CAP:
        stress_chain_segments.sort(key=lambda s: s['mult'], reverse=True)
        stress_chain_segments = stress_chain_segments[:_SC_CAP]

    # ── Phase A3 — connected components of AM_P brittle skeleton ─────────
    # Union-find over AM_P-AM_P edges with F/P_c >= 1.  Each component is
    # a load-bearing fracture-prone backbone segment.
    parent: dict[int, int] = {}
    def _find(x: int) -> int:
        while parent.get(x, x) != x:
            parent[x] = parent.get(parent[x], parent[x])
            x = parent[x]
        return x
    def _union(a: int, b: int) -> None:
        ra, rb = _find(a), _find(b)
        if ra != rb: parent[ra] = rb
    for a, b in am_p_brittle_edges:
        parent.setdefault(a, a); parent.setdefault(b, b)
        _union(a, b)
    am_p_skeleton_clusters: dict[int, list[int]] = defaultdict(list)
    for node in parent:
        am_p_skeleton_clusters[_find(node)].append(node)
    # Convert to list-of-lists, sorted by size (largest first)
    am_p_skeleton: list[list[int]] = sorted(
        ([sorted(v) for v in am_p_skeleton_clusters.values() if len(v) >= 2]),
        key=len, reverse=True)

    return {
        'stress_max':       {int(k): round(v, 2) for k, v in stress_max.items()},
        'dr_max':           {int(k): round(v, 4) for k, v in dr_max.items()},
        'worst_partner':    {int(k): int(v)      for k, v in worst_partner.items()},
        'brittle_pairs':    brittle_pairs,
        'se_stress_pairs':  se_stress_pairs,      # capped: top-N by pressure
        'am_se_stress_pairs': am_se_stress_pairs, # capped: top-N by pressure
        # ── Phase A1: per-particle worst F/P_c ────────────────────────────
        'particle_max_fpc': {int(k): round(v, 3) for k, v in particle_max_fpc.items()},
        'particle_worst_stage':   {int(k): v for k, v in particle_worst_stage.items()},
        'particle_n_brittle':     {int(k): int(v) for k, v in particle_n_brittle.items()},
        'particle_worst_partner_brittle': {int(k): int(v) for k, v in particle_worst_partner_brittle.items()},
        'particle_worst_pair_type':       {int(k): v for k, v in particle_worst_pair_type.items()},
        # ── Phase A3: AM_P fracture skeleton ──────────────────────────────
        'am_p_skeleton': am_p_skeleton,            # list of clusters (lists of pid)
        # ── Phase A4: AM-AM stress-chain segments ─────────────────────────
        'stress_chain_segments': stress_chain_segments,
        # se_states emit dropped — was only consumed by the old SE
        # Tabor 4-bin view mode (removed in commit 4d3f39b).  Keeping
        # this empty dict for backward-compat with any cached payloads
        # that still reference the key.
        'se_states': {},
        'tabor_stats':  tabor_stats,
        # Emit just the count, not the full id list — the frontend
        # only uses `all_se_ids.length` to compute percentages, and
        # a 620k-element id array adds ~5 MB to the JSON response
        # for sub-μm SE particulate cases.  Backward compat: keep
        # the key name but value is now just a number; the
        # JS-side fallback uses `seMeshCount` when this is 0.
        'all_se_ids_count': len(all_se_ids),
        # Per-SE engagement score (single float per particle).  Was
        # a 6-field dict pre-commit-42b3ea6 — frontend visualises by
        # score only, so flattening saves ~50 MB JSON for the
        # particulate corpus.
        'se_engagement': se_engagement,
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


# ── Phase A5 + A6: SE network diagnostics ───────────────────────────────
#  - articulation points (cut vertices) in the percolating subgraph
#  - narrowest contacts (bottleneck edges)
#  - dead-end clusters (touching bottom or top but not both)

def compute_se_network_diagnostics(contacts,
                                    atoms_by_id: dict,
                                    type_map: dict,
                                    plate_z: float,
                                    scale: float = 1000.0,
                                    boundary_factor: float = 2.0,
                                    bn_threshold_factor: float = 0.10,
                                    bn_min: int = 10,
                                    bn_max: int = 200,
                                    verbose: bool = False) -> dict:
    """Build SE-SE contact graph, identify percolation breakage points.

    Inputs are sim units (plate_z in sim length).  Output areas are
    converted to real μm² so the viewer can render them with the same
    units the dashboard uses.

    Returns dict with:
      percolating_se:        sorted list of SE pid in the bottom↔top cluster
      articulation_points:   SE pid whose removal would split percolation
      bottleneck_edges:      top-N narrowest contact-area edges in perc subgraph
                              [{id1, id2, area_um2}]
      dead_end_clusters:     clusters touching bottom XOR top but not both
                              [{ids:[pid], type:'bottom_only'|'top_only', size}]
      n_percolating:         convenience count
    """
    import networkx as nx  # local import — only loaded when diagnostics requested

    se_ids = {pid for pid, a in atoms_by_id.items()
              if type_map.get(int(a.get('type', -1))) == 'SE'}
    if not se_ids:
        return {'percolating_se': [], 'articulation_points': [],
                'bottleneck_edges': [], 'dead_end_clusters': [],
                'n_percolating': 0}

    area_conv = (1.0 / (scale ** 2)) * 1.0e12   # sim m² → real μm²

    # Build SE-SE graph.  Edges keep contact_area as weight for bn analysis,
    # but the EDGE EXISTENCE is gated on the same criteria as dem_analysis_core
    # calc_percolation (which gates only on "both ends are SE", no area > 0
    # filter).  Earlier we required area > 0 which dropped SE-SE pairs whose
    # LIGGGHTS dump emitted contact_area = 0 (sub-threshold overlap with
    # nonzero force), causing many real percolating cases to report perc=0.
    G = nx.Graph()
    G.add_nodes_from(se_ids)
    for c in contacts:
        i1 = int(c.get('id1', -1)); i2 = int(c.get('id2', -1))
        if i1 not in se_ids or i2 not in se_ids:
            continue
        area = float(c.get('contact_area', 0) or 0)
        # Keep largest area if duplicate edges appear
        if G.has_edge(i1, i2):
            if area > G[i1][i2].get('area', 0):
                G[i1][i2]['area'] = area
        else:
            G.add_edge(i1, i2, area=area)

    # Boundary identification — per-particle radius gate (matches calc_percolation)
    bottom_se, top_se = set(), set()
    for pid in se_ids:
        a = atoms_by_id[pid]
        z = float(a.get('z', 0))
        r = float(a.get('radius', 0))
        if z <= r * boundary_factor:
            bottom_se.add(pid)
        if z >= plate_z - r * boundary_factor:
            top_se.add(pid)

    # Fallback L1: if strict per-radius gate finds < 3 boundary SE on
    # either side, widen to 15% / 85% of plate_z.  Matches dem_analysis_core
    # calc_percolation's 2-stage fallback so dashboard and viewer agree.
    if len(bottom_se) < 3 or len(top_se) < 3:
        z_bottom = plate_z * 0.15
        z_top    = plate_z * 0.85
        bottom_se = {pid for pid in se_ids
                     if atoms_by_id[pid].get('z', 0) <= z_bottom}
        top_se    = {pid for pid in se_ids
                     if atoms_by_id[pid].get('z', 0) >= z_top}

    # Fallback L2: anchor to observed SE z-range when mesh_info.plate_z
    # overshoots actual packed top (common after DEM re-analysis).
    if len(bottom_se) < 3 or len(top_se) < 3:
        z_vals = [atoms_by_id[pid].get('z', 0) for pid in se_ids]
        if z_vals:
            z_min_obs, z_max_obs = min(z_vals), max(z_vals)
            span = z_max_obs - z_min_obs
            if span > 0:
                z_bottom = z_min_obs + span * 0.15
                z_top    = z_max_obs - span * 0.15
                bottom_se = {pid for pid in se_ids
                             if atoms_by_id[pid].get('z', 0) <= z_bottom}
                top_se    = {pid for pid in se_ids
                             if atoms_by_id[pid].get('z', 0) >= z_top}

    if verbose:
        print(f'           graph: nodes={G.number_of_nodes()}, '
              f'edges={G.number_of_edges()}, '
              f'bottom_se={len(bottom_se)}, top_se={len(top_se)}')

    # Identify percolating component(s) + dead-end clusters
    percolating_se = set()
    dead_end_clusters = []
    components = list(nx.connected_components(G))
    if verbose:
        sizes = sorted((len(c) for c in components), reverse=True)
        print(f'           n_components={len(components)}, '
              f'top sizes={sizes[:5]}')
    for comp in components:
        has_b = bool(comp & bottom_se)
        has_t = bool(comp & top_se)
        if has_b and has_t:
            percolating_se.update(comp)
        elif (has_b or has_t) and len(comp) >= 3:
            dead_end_clusters.append({
                'ids':  sorted(int(x) for x in comp),
                'type': 'bottom_only' if has_b else 'top_only',
                'size': len(comp),
            })
    # Sort dead-ends largest-first, cap to top-20 to keep payload small
    dead_end_clusters.sort(key=lambda d: d['size'], reverse=True)
    dead_end_clusters = dead_end_clusters[:20]

    if not percolating_se:
        return {'percolating_se': [], 'articulation_points': [],
                'bottleneck_edges': [], 'dead_end_clusters': dead_end_clusters,
                'n_percolating': 0}

    Gp = G.subgraph(percolating_se).copy()

    # Articulation points (cut vertices) in the percolating subgraph
    try:
        art_pts = sorted(int(p) for p in nx.articulation_points(Gp))
    except Exception:
        art_pts = []

    # Bottleneck edges — dimensionless A/r_min² threshold (Phase C refinement)
    # A typical Hertz contact has a/R ~ 0.1 → A/R² ~ 0.03.  We flag
    # edges below median(A/r²) × bn_threshold_factor (default 10%).
    # Bounded by [bn_min, bn_max] so visualization always has signal.
    import statistics as _stat
    edges = []
    for u, v, d in Gp.edges(data=True):
        area = float(d.get('area', 0) or 0)
        r1 = float(atoms_by_id.get(u, {}).get('radius', 0) or 0)
        r2 = float(atoms_by_id.get(v, {}).get('radius', 0) or 0)
        r_min = min(r1, r2)
        if r_min <= 0 or area <= 0:
            continue
        norm = area / (r_min ** 2)   # dimensionless
        edges.append((int(u), int(v), area, norm, r_min))

    bottleneck_edges = []
    bn_median_norm = 0.0
    bn_threshold_norm = 0.0
    n_bn_below_threshold = 0   # uncapped count of edges below threshold
    if edges:
        edges.sort(key=lambda e: e[3])   # by normalized metric
        norms = [e[3] for e in edges]
        bn_median_norm = float(_stat.median(norms))
        bn_threshold_norm = bn_median_norm * bn_threshold_factor

        # True count (no cap) of below-threshold edges
        n_bn_below_threshold = sum(1 for n in norms if n < bn_threshold_norm)

        # Capped display list — keeps payload bounded for viewer rendering
        for u, v, area, norm, r_min in edges:
            is_below_threshold = (norm < bn_threshold_norm)
            if (not is_below_threshold) and len(bottleneck_edges) >= bn_min:
                break
            if len(bottleneck_edges) >= bn_max:
                break
            bottleneck_edges.append({
                'id1':       u,
                'id2':       v,
                'area_um2':  round(area * area_conv, 5),
                'area_norm': round(norm, 5),
                'r_min_um':  round(r_min * scale, 3),
            })

    return {
        'percolating_se':      sorted(int(x) for x in percolating_se),
        'articulation_points': art_pts,
        'bn_median_norm':      round(bn_median_norm, 5),
        'bn_threshold_norm':   round(bn_threshold_norm, 5),
        'n_bn_below_threshold': n_bn_below_threshold,
        'bottleneck_edges':    bottleneck_edges,
        'dead_end_clusters':   dead_end_clusters,
        'n_percolating':       len(percolating_se),
    }


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
