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

    return {
        'stress_max':       {int(k): round(v, 2) for k, v in stress_max.items()},
        'dr_max':           {int(k): round(v, 4) for k, v in dr_max.items()},
        'worst_partner':    {int(k): int(v)      for k, v in worst_partner.items()},
        'brittle_pairs':    brittle_pairs,
        'se_stress_pairs':  se_stress_pairs,      # capped: top-N by pressure
        'am_se_stress_pairs': am_se_stress_pairs, # capped: top-N by pressure
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
