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


#: 입자별 배위수 (CN) 의 접촉 정의 — 3D 뷰어 '배위수' 보기 · AM 접촉 확대의 범례에 그대로 실린다 (2026-10-06 · 1저자 보고 슬라이드).
CN_CONTACT_RULE = (
    '접촉 = contacts.csv 행 하나 (입자–입자 덤프 · δ · 면적으로 거르지 않는다 · 두 id 가 원자 표에 있어야 한다 · 같은 행이 두 번이면 두 번) '
    '= dem_analysis_core.calc_se_se_cn · calc_am_isolation_risk · calc_am_am_cn 과 같은 집합 · 평균 = 그 상의 모든 입자 (접촉 0 포함) '
    '= full_metrics se_se_cn · {상}_se_cn_mean · am_se_cn_mean · am_am_cn · 벽 · 플래튼 접촉은 덤프에 없다')


def _cn_stats(vals: list) -> dict:
    """정수 CN 목록 → 평균 · 모집단 표준편차 · 중앙값 · 최소 · 최대 · 0 개수 (np.mean · np.std · np.median 과 같은 정의).
    평균 = 정수 합 ÷ n (정확한 정수 합의 올바른 반올림 — np.mean 과 비트 같음)."""
    n = len(vals)
    if not n:
        return {'n': 0, 'mean': None, 'std': None, 'median': None, 'min': None, 'max': None, 'n_zero': 0}
    s = sorted(vals)
    mean = sum(vals) / n
    return {'n': n, 'mean': mean, 'std': math.sqrt(sum((v - mean) ** 2 for v in vals) / n),
            'median': (s[(n - 1) // 2] + s[n // 2]) / 2, 'min': s[0], 'max': s[-1],
            'n_zero': sum(1 for v in vals if v == 0)}


def cn_summary(atoms_by_id: dict, type_map: dict, cn_se_se: dict, cn_am_se: dict, cn_am_am: dict,
               n_rows: dict) -> dict:
    """상별 CN 요약 — AM 상마다 AM–SE (활물질 주위 SE) · AM–AM, SE 는 SE–SE.  모든 입자 (접촉 0 포함) 위의 통계."""
    by_lbl: dict = defaultdict(list)
    for aid, a in atoms_by_id.items():
        by_lbl[type_map.get(int(a.get('type', -1)), '?')].append(int(aid))
    phases: dict = {}
    all_am: list = []
    for lbl in sorted(by_lbl):
        ids = by_lbl[lbl]
        if lbl == 'SE':
            st = _cn_stats([cn_se_se.get(i, 0) for i in ids])
            phases[lbl] = {'kind': 'SE', 'n': st['n'], 'se_se_mean': st['mean'], 'se_se_std': st['std'],
                           'se_se_median': st['median'], 'se_se_min': st['min'], 'se_se_max': st['max'],
                           'se_se_n_zero': st['n_zero']}
        elif 'AM' in lbl:
            all_am += ids
            st = _cn_stats([cn_am_se.get(i, 0) for i in ids])
            aa = _cn_stats([cn_am_am.get(i, 0) for i in ids])
            phases[lbl] = {'kind': 'AM', 'n': st['n'], 'am_se_mean': st['mean'], 'am_se_std': st['std'],
                           'am_se_median': st['median'], 'am_se_min': st['min'], 'am_se_max': st['max'],
                           'am_se_n_zero': st['n_zero'], 'am_am_mean': aa['mean'], 'am_am_std': aa['std']}
    st_all = _cn_stats([cn_am_se.get(i, 0) for i in all_am])
    aa_all = _cn_stats([cn_am_am.get(i, 0) for i in all_am])
    return {'rule': CN_CONTACT_RULE, 'phases': phases,
            'am_se_mean_all': st_all['mean'], 'am_am_mean_all': aa_all['mean'], 'n_am_all': st_all['n'],
            'n_rows': dict(n_rows)}


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

    # ── 입자별 배위수 (CN · 2026-10-06 · 3D 뷰어 '배위수' 보기 · AM 접촉 확대) ─────────────────
    # 행 하나 = 접촉 하나 — δ · 면적 거르기 **앞**에서 센다 (CN_CONTACT_RULE · dem_analysis_core 의 CN 함수와 같은 집합).
    # 0 인 입자는 항목이 없다 (= 측정된 0 · 요약 평균은 원자 표 전체 위).
    cn_se_se: dict[int, int] = defaultdict(int)
    cn_am_se: dict[int, int] = defaultdict(int)
    cn_am_am: dict[int, int] = defaultdict(int)
    cn_rows = {'se_se': 0, 'am_se': 0, 'am_am': 0, 'other': 0, 'unknown_id': 0}

    pressure_conv = scale / 1.0e6     # sim Pa → real MPa (calibrated to scale)

    def _bump_state(d: dict[int, int], sid: int, regime: str) -> None:
        rank = _REGIME_RANK[regime]
        if rank > d.get(sid, 0):
            d[sid] = rank

    for c in contacts:
        i1 = int(c.get('id1', -1)); i2 = int(c.get('id2', -1))
        if i1 < 0 or i2 < 0:
            cn_rows['unknown_id'] += 1
            continue
        a1 = atoms_by_id.get(i1); a2 = atoms_by_id.get(i2)
        if a1 is None or a2 is None:
            cn_rows['unknown_id'] += 1
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

        # CN — 아래의 δ/R 거르기 (dr <= 0 → continue) 앞에서 센다
        if is_se1 and is_se2:
            cn_se_se[i1] += 1; cn_se_se[i2] += 1; cn_rows['se_se'] += 1
        elif is_am1 and is_am2:
            cn_am_am[i1] += 1; cn_am_am[i2] += 1; cn_rows['am_am'] += 1
        elif (is_am1 and is_se2) or (is_am2 and is_se1):
            cn_am_se[i1 if is_am1 else i2] += 1; cn_rows['am_se'] += 1
        else:
            cn_rows['other'] += 1

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
        # 입자별 배위수 (0 이면 항목 없음) + 상별 요약 — 3D 뷰어 '배위수' 보기 (2026-10-06 · 캐시 스키마 12)
        'cn_se_se': {int(k): int(v) for k, v in cn_se_se.items()},
        'cn_am_se': {int(k): int(v) for k, v in cn_am_se.items()},
        'cn_am_am': {int(k): int(v) for k, v in cn_am_am.items()},
        'cn_summary': cn_summary(atoms_by_id, type_map, cn_se_se, cn_am_se, cn_am_am, cn_rows),
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
    n_bn_below_threshold = 0      # true count of edges below threshold (uncapped)
    n_perc_edges = 0              # total edges in percolating subgraph
    # Full-distribution percentiles over ALL percolating edges (no cap)
    bn_stats_norm = {'min': 0.0, 'p1': 0.0, 'p5': 0.0, 'p10': 0.0,
                     'p25': 0.0, 'p50': 0.0, 'p75': 0.0, 'max': 0.0}
    bn_stats_area = {'min_um2': 0.0, 'p10_um2': 0.0, 'p50_um2': 0.0}

    if edges:
        edges.sort(key=lambda e: e[3])   # by normalized metric
        norms = [e[3] for e in edges]
        areas_um2 = [e[2] * area_conv for e in edges]
        n_perc_edges = len(norms)

        bn_median_norm = float(_stat.median(norms))
        bn_threshold_norm = bn_median_norm * bn_threshold_factor
        n_bn_below_threshold = sum(1 for n in norms if n < bn_threshold_norm)

        # Percentiles on the FULL distribution (uncapped) — these are the
        # scientific stats used in CSV/figures.  Display list cap below
        # does not affect these.
        def _pct(arr, p):
            i = max(0, min(len(arr) - 1, int(round(p / 100.0 * (len(arr) - 1)))))
            return float(arr[i])
        bn_stats_norm = {
            'min': _pct(norms,  0), 'p1':  _pct(norms,  1),
            'p5':  _pct(norms,  5), 'p10': _pct(norms, 10),
            'p25': _pct(norms, 25), 'p50': _pct(norms, 50),
            'p75': _pct(norms, 75), 'max': _pct(norms, 100),
        }
        bn_stats_area = {
            'min_um2': _pct(areas_um2,  0),
            'p10_um2': _pct(areas_um2, 10),
            'p50_um2': _pct(areas_um2, 50),
        }

        # Display list — capped at bn_max for viewer payload only.
        # Does NOT affect statistics above.
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
        'n_perc_edges':        n_perc_edges,
        # full-distribution stats (uncapped) — for CSV/figures
        'bn_stats_norm':       {k: round(v, 6) for k, v in bn_stats_norm.items()},
        'bn_stats_area':       {k: round(v, 6) for k, v in bn_stats_area.items()},
        'bottleneck_edges':    bottleneck_edges,
        'dead_end_clusters':   dead_end_clusters,
        'n_percolating':       len(percolating_se),
    }


# ── Per-AM coverage map (μm² SE / μm² total surface) ─────────────────────

def coverage_map_column(coverage_per_am_csv_path) -> str | None:
    """build_coverage_map 이 **실제로 읽는 열** — 'coverage_physics_pct' (Physics v1) · 'coverage_hertzian_pct'
    (physics 열이 없을 때의 Hertz 계열 대체 = LIGGGHTS c_cpl[22] 기하 교차 원판) · None (파일 · 열 없음).
    3D 뷰어 범례가 대체를 표지하도록 (웹앱 ②-b · LHS-24 (f) — 두 값 ≈ 2.7 배가 같은 범례로 섞이던 것)."""
    import os
    if not (coverage_per_am_csv_path and os.path.exists(coverage_per_am_csv_path)):
        return None
    try:
        import csv
        with open(coverage_per_am_csv_path, newline='') as fh:
            header = next(csv.reader(fh), [])
    except Exception:
        return None
    if 'am_id' not in header:
        return None
    for col in ('coverage_physics_pct', 'coverage_hertzian_pct'):
        if col in header:
            return col
    return None


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


# ── AM 접촉 확대 — 3D 뷰어 모달 (2026-10-06 · 1저자 보고 슬라이드 "Coverage 확대" · "활물질 주위 SE") ─────────
#  /results/<id>/am-contacts · /archive/results/<folder>/am-contacts 가 부른다 (app.py).  계산은 새로 짜지 않는다:
#  면적 = contacts.csv 의 c_cpl[22] 그대로 · 세대 2 면적 = plastic_coverage.film_area_g2 (생산 합집합 피복과 같은 인자) ·
#  합집합 = plastic_coverage.union_cap_coverage · 보고 규칙 합집합 = coverage_physics_vs_hertzian.union_coverage_bed 를 이 AM 의
#  행만으로 부른 값 (AM 하나의 cap 은 그 AM 의 접촉으로만 정해지므로 침대 전체 값과 같다 — webapp/test_viewer_am_contacts.py Q2).

#: 경로가 contacts.csv 에서 읽는 열 (있는 것만 · 접촉점 cp_* 는 덤프에 contactPoint 가 있을 때만).
AM_CLOSEUP_CONTACT_COLS = ('id1', 'id2', 'delta', 'contact_area', 'cp_x', 'cp_y', 'cp_z')
#: cap 규칙 — 그림 · 범례 · 합집합이 같은 식을 쓴다 (viewer3d.js capHalfAngle · plastic_coverage.union_cap_coverage).
AM_CLOSEUP_CAP_RULE = ('접촉 하나 = AM 구면 위 cap 하나 — 중심 = AM → 상대 중심 방향 (x · y 주기 최소영상) · 넓이 A → '
                       'cos θ = 1 − A/(2πR²) (A ≥ 2πR² 은 반구로 자름) · SE 접촉 = 노란 cap · AM–AM 접촉 = 회색 cap')

_AM_INDEX_CACHE: dict = {}


def _fin(x):
    """유한한 실수 → float · 아니면 None (JSON 에 NaN 을 싣지 않는다 — 브라우저 JSON.parse 가 깨진다)."""
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return v if math.isfinite(v) else None


def _file_sig(path):
    import os
    st = os.stat(path)
    return (os.path.realpath(path), st.st_mtime_ns, st.st_size)


def load_am_contact_index(atoms_csv, contacts_csv, type_map: dict) -> dict:
    """atoms.csv 배열 + contacts.csv 에서 **AM 이 낀 행만** — 한 칸 캐시 (두 파일의 경로 · mtime · 크기 · type_map).
    다음 · 이전 AM 으로 넘길 때 contacts.csv 를 다시 읽지 않는다 (AM 이 안 낀 SE–SE 행은 버린다)."""
    import pandas as pd
    key = (_file_sig(atoms_csv), _file_sig(contacts_csv), tuple(sorted((int(k), str(v)) for k, v in type_map.items())))
    hit = _AM_INDEX_CACHE.get(key)
    if hit is not None:
        return hit
    adf = pd.read_csv(atoms_csv)
    miss_a = [c for c in ('id', 'type', 'x', 'y', 'z', 'radius') if c not in adf.columns]
    if miss_a:
        raise ValueError(f'atoms.csv 에 {miss_a} 열이 없다')
    adf = adf[['id', 'type', 'x', 'y', 'z', 'radius']].apply(pd.to_numeric, errors='coerce')
    adf = adf[adf['id'].notna()].reset_index(drop=True)
    ids = adf['id'].astype('int64').to_numpy()
    types = adf['type'].fillna(-1).astype('int64').to_numpy()
    cdf = pd.read_csv(contacts_csv, usecols=lambda c: c in AM_CLOSEUP_CONTACT_COLS, low_memory=False)
    cdf = cdf.apply(pd.to_numeric, errors='coerce')
    missing = [c for c in ('id1', 'id2', 'delta', 'contact_area') if c not in cdf.columns]
    am_ids = sorted({int(a) for a, t in zip(ids, types) if 'AM' in str(type_map.get(int(t), ''))})
    if missing:
        rows = cdf.iloc[0:0]
    else:
        rows = cdf[cdf['id1'].isin(am_ids) | cdf['id2'].isin(am_ids)].reset_index(drop=True)
    idx = {'atoms_df': adf, 'ids': ids, 'types': types, 'rad': adf['radius'].to_numpy(dtype=float),
           'xyz': adf[['x', 'y', 'z']].to_numpy(dtype=float), 'pos': {int(a): k for k, a in enumerate(ids)},
           'rows': rows, 'missing_cols': missing, 'n_rows_total': int(len(cdf)),
           'has_cp': all(c in cdf.columns for c in ('cp_x', 'cp_y', 'cp_z'))}
    _AM_INDEX_CACHE.clear()
    _AM_INDEX_CACHE[key] = idx
    return idx


def am_contact_closeup(idx: dict, type_map: dict, am_id: int, *, scale=1000.0, box_xy=None,
                       box_source: str = 'input_params', box_reason: str | None = None, full_metrics: dict | None = None):
    """AM 하나의 접촉 (3D 뷰어 'AM 접촉 확대') → `(payload, http status)`.

    payload (길이 µm = 덤프 × scale · 넓이 µm² = 덤프 × scale² — /3d-data 의 입자 좌표와 같은 단위):
      am {id · type · r · x · y · z} · contacts [상대 id · 상 · 쌍 (AM_SE · AM_AM · OTHER) · 반경 · 중심 (AM 옆 최소영상 자리) ·
      wrapped (주기 영상으로 옮겼나) · area_um2 (c_cpl[22]) · area_g2_um2 (세대 2 표면 면적 · 생산 합집합과 같은 인자) · delta_um ·
      cp (접촉점 · AM 옆으로 최소영상) · geom_ok (|d| = r1 + r2 − δ · 생산과 같은 허용폭)] · n_se (= 이 AM 의 AM–SE CN) · n_am ·
      n_other · n_wrapped · n_dir_inconsistent · n_unknown_id · n_self · n_g2_rejected ·
      cap_sum_pct {hertz · g2} (= Σ A_SE ÷ 4πR² × 100 — 겹친 cap 을 두 번 센다 · 그림 설명용) ·
      union_pct {hertz: c_cpl[22] cap 합집합 (= 기본 그림의 노란 면적) · g2: 보고 규칙 (⑥ Physics 합집합 · 이 AM)} ·
      reported {케이스 표 침대 평균 — full_metrics coverage_<상>_mean_physics_union · 상태 · Hertz 계열 합-클립} ·
      box_um · box_source ('input_params' | 'default_0.05' — 그리기만 뷰어와 같은 0.05 기본으로 · 보고 규칙 합집합은 생산처럼 빈칸).
    오류: am_id 가 원자 표에 없음 404 · AM 이 아님 · scale · 열 없음 400."""
    import numpy as np
    from plastic_coverage import film_area_g2, union_cap_coverage, fibonacci_sphere, UNION_FIB_N
    from coverage_physics_vs_hertzian import (union_coverage_bed, UNION_DIST_TOL_REL, UNION_DIST_TOL_BOX,
                                              UNION_LENGTH_SCALE_UM)
    s = _fin(scale)
    if not (s and s > 0):
        return {'error': f'scale={scale!r} 가 유한 양수가 아니다'}, 400
    if idx.get('missing_cols'):
        return {'error': f'contacts.csv 에 {idx["missing_cols"]} 열이 없다 — 접촉 면적 · δ 없이 cap 을 그릴 수 없다'}, 400
    am_id = int(am_id)
    k_am = idx['pos'].get(am_id)
    if k_am is None:
        return {'error': f'id {am_id} 가 atoms.csv 에 없다'}, 404
    lbl = type_map.get(int(idx['types'][k_am]), f'T{int(idx["types"][k_am])}')
    if 'AM' not in str(lbl):
        return {'error': f'id {am_id} 는 {lbl} — AM 이 아니다 (AM 접촉 확대는 AM 입자만)'}, 400
    R, p_am = float(idx['rad'][k_am]), idx['xyz'][k_am]
    if not (math.isfinite(R) and R > 0 and np.isfinite(p_am).all()):
        return {'error': f'id {am_id} 의 반경 · 좌표가 유한하지 않다 (r={R!r})'}, 400
    Lx, Ly = (float(box_xy[0]), float(box_xy[1])) if box_xy else (0.05, 0.05)
    tol_box = UNION_DIST_TOL_BOX * max(Lx, Ly)
    rows = idx['rows']
    sel = rows[(rows['id1'] == am_id) | (rows['id2'] == am_id)]
    cnt = dict(n_se=0, n_am=0, n_other=0, n_wrapped=0, n_dir_inconsistent=0, n_unknown_id=0, n_self=0, n_g2_rejected=0)
    contacts, partner_k = [], set()
    se_d, se_a, se_g, am_d, am_a = [], [], [], [], []
    has_cp = idx.get('has_cp')
    for row in sel.itertuples(index=False):
        i1, i2 = int(row.id1), int(row.id2)
        if i1 == i2:
            cnt['n_self'] += 1
            continue
        pid = i2 if i1 == am_id else i1
        k = idx['pos'].get(pid)
        if k is None:
            cnt['n_unknown_id'] += 1
            continue
        plbl = type_map.get(int(idx['types'][k]), f'T{int(idx["types"][k])}')
        pair = 'AM_SE' if plbl == 'SE' else ('AM_AM' if 'AM' in str(plbl) else 'OTHER')
        raw = idx['xyz'][k] - p_am
        v = raw.copy()
        v[0] -= Lx * round(v[0] / Lx)                     # 최소영상 (생산 union_coverage_bed 와 같은 식)
        v[1] -= Ly * round(v[1] / Ly)
        wrapped = bool(v[0] != raw[0] or v[1] != raw[1])
        rp, dl, ca = float(idx['rad'][k]), float(row.delta), float(row.contact_area)
        err = abs(float(np.linalg.norm(v)) - (R + rp - dl))
        geom_ok = bool(math.isfinite(err) and err <= UNION_DIST_TOL_REL * (R + rp) + tol_box)
        cnt['n_dir_inconsistent'] += int(not geom_ok)
        cnt['n_wrapped'] += int(wrapped)
        a_g2 = None
        if pair != 'OTHER':
            try:
                a_g2, _b = film_area_g2(dl * s, R * s, rp * s, pair=pair, ligg_area=ca * s * s,
                                        length_scale=UNION_LENGTH_SCALE_UM, consumer='surface')
            except (ValueError, TypeError):
                cnt['n_g2_rejected'] += 1
        cp = None
        if has_cp:
            w = np.array([row.cp_x, row.cp_y, row.cp_z], dtype=float) - p_am
            if np.isfinite(w).all():
                w[0] -= Lx * round(w[0] / Lx)
                w[1] -= Ly * round(w[1] / Ly)
                cp = [_fin((p_am[j] + w[j]) * s) for j in range(3)]
        q = (p_am + v) * s
        contacts.append({'partner_id': pid, 'partner_type': plbl, 'pair': pair, 'partner_r': _fin(rp * s),
                         'x': _fin(q[0]), 'y': _fin(q[1]), 'z': _fin(q[2]), 'wrapped': wrapped,
                         'area_um2': _fin(ca * s * s), 'area_g2_um2': _fin(a_g2), 'delta_um': _fin(dl * s),
                         'cp': cp, 'geom_ok': geom_ok})
        partner_k.add(k)
        if pair == 'AM_SE':
            cnt['n_se'] += 1
            se_d.append(v)
            se_a.append(ca * s * s)
            se_g.append(a_g2)
        elif pair == 'AM_AM':
            cnt['n_am'] += 1
            am_d.append(v)
            am_a.append(ca * s * s)
        else:
            cnt['n_other'] += 1
    Rum = R * s
    surf = 4.0 * math.pi * Rum * Rum

    #  그림 합집합 (c_cpl[22] cap = 기본 그림의 노란 면적) — 생산 함수 그대로 · 방향 검사 실패가 있으면 생산처럼 빈칸
    hz = {'value': None, 'status': 'ok'}
    if cnt['n_dir_inconsistent']:
        hz['status'] = (f'blank: {cnt["n_dir_inconsistent"]} 접촉의 방향 검사 실패 (최소영상 거리 ≠ r1 + r2 − δ — '
                        '상자 · 프레임 어긋남)')
    else:
        try:
            cov, info = union_cap_coverage(Rum, se_d, se_a, am_d, am_a, points=fibonacci_sphere(UNION_FIB_N))
            if cov is None:
                hz['status'] = f'blank: {info.get("reason")}'
            else:
                hz['value'] = float(cov)
        except (ValueError, TypeError) as e:
            hz['status'] = f'blank: {type(e).__name__}: {e}'
    #  보고 규칙 합집합 (⑥ Physics · 세대 2) — 생산 union_coverage_bed 를 이 AM 의 행만으로.  상자는 input_params.json 이 있을 때만
    #  (생산처럼 0.05 기본값으로 떨어지지 않는다 — 없으면 빈칸 + 사유).
    sub_atoms = idx['atoms_df'].iloc[[k_am] + sorted(partner_k)]
    sub_rows = sel[['id1', 'id2', 'delta', 'contact_area']]
    try:
        ukeys, uper = union_coverage_bed(sub_atoms, sub_rows, type_map, scale=s,
                                         box_xy=((Lx, Ly) if box_xy else None), box_reason=box_reason)
        ust = ukeys.get('coverage_status_physics_union')
        g2 = {'value': _fin(uper.get(am_id)) if ust == 'ok' else None, 'status': ust}
    except Exception as e:                                         # noqa: BLE001 — 사유로 남긴다 (경로는 그림을 계속 준다)
        g2 = {'value': None, 'status': f'blank: 합집합 계산 오류 — {type(e).__name__}: {e}'}
    fm = full_metrics or {}
    payload = {
        'am': {'id': am_id, 'type': lbl, 'r': _fin(Rum), 'x': _fin(p_am[0] * s), 'y': _fin(p_am[1] * s),
               'z': _fin(p_am[2] * s)},
        'contacts': contacts, **cnt,
        'cap_sum_pct': {'hertz': _fin(sum(se_a) / surf * 100.0),
                        'g2': (_fin(sum(se_g) / surf * 100.0) if all(a is not None for a in se_g) else None)},
        'union_pct': {'hertz': hz, 'g2': g2},
        'reported': {'label': lbl, 'union_mean_pct': _fin(fm.get(f'coverage_{lbl}_mean_physics_union')),
                     'union_status': fm.get('coverage_status_physics_union'),
                     'hertz_mean_pct': _fin(fm.get(f'coverage_{lbl}_mean'))},
        'box_um': [Lx * s, Ly * s], 'box_source': box_source, 'box_reason': box_reason, 'scale': s,
        'n_fib': int(UNION_FIB_N),
        'rules': {'cn': CN_CONTACT_RULE, 'cap': AM_CLOSEUP_CAP_RULE,
                  'area_hertz': 'c_cpl[22] = LIGGGHTS 기하 교차 원판 (Hertz 계열 — 이름만 Hertz · L1-04)',
                  'area_g2': '세대 2 표면 면적 film_area_g2(consumer=surface) = 케이스 표 Physics 합집합 피복의 cap (⑥ · LHS-25)'},
    }
    return payload, 200


# ── 입자 하중 보기 — 3D 뷰어 'AM 만 칠하기' · 'Max contact pressure' (2026-10-07 · 1저자 결정 · 웹앱 묶음 #11 · WEB-06) ─────────
#  계산은 새로 짜지 않는다: 읽기 = analyze_contacts.load_atoms_raw · load_contacts_raw (생산 분석기와 같은 읽기) · 판 높이 · 상자 =
#  dem_analysis_core.get_plate_z · _get_box_xy (run_full_analysis 와 같은 기하) · 입자 응력 = dem_analysis_core.calc_love_weber_stress
#  (full_metrics stress_ratio_<상>_lw 를 만든 그 함수 · return_arrays) · 힘 환산 = calc_contact_force_distribution 의 1e6/scale ·
#  압력 환산 = calc_contact_pressure · aggregate_particle_metrics 의 scale/1e6.
#  ⚠ 3D 데이터 (/3d-data aux) 에 싣는 것은 webapp/app.py (194 봉인) 의 일이다 — 봉인 중에는 그 파일을 바꾸지 않고 발사 뒤 패치
#    docs/reviews/webapp_load_view_deferred_20261007.patch 로 aux['load_view'] = particle_load_view_for_case(…) + 캐시 스키마 13.

LOAD_VIEW_SCHEMA = 'particle_load_view/v1'
#: LW 는 접촉 행을 dict 목록으로 읽는다 (생산 읽기 그대로 · 행당 ~1 kB) — 이보다 많으면 LW 만 계산하지 않는다 (압력 · 힘은 열 배열로 계산)
LW_VIEW_ROW_BUDGET = 1_000_000
CONTACT_SIGN_RULE = ('부호 = 덤프 법선력 fn (c_cpl[13–15] = id1 이 받는 힘) · (x_id1 − x_id2) — 양수 = 두 중심을 떼어 놓는 힘 (압축 접촉) · '
                     '음수 = 당기는 힘 (당김 · 접착 접촉) · x · y 는 최소영상 (상자) · 상자 없이 주기 너머면 접촉점 쪽 가지 (x_id1 − x_c 또는 '
                     'x_c − x_id2) · 그래도 못 정하면 판정 불가 (0) · |fn| = 0 도 0 (docs/data/contact_pressure_check_20261007 과 같은 부호)')
PRESSURE_MAX_RULE = ('Max contact pressure = 입자별 최대 |Fn| / A (A = 덤프 접촉 면적 c_cpl[22] · × scale / 1e6 = MPa) — 압축 접촉만 '
                     '(당김 · 접착 접촉 · δ ≤ 0 · 면적 0 · 힘 0 · 부호 판정 불가 행은 뺀다).  hooke/hysteresis 에서 압축 접촉의 p 는 쌍 유형마다 '
                     '거의 일정 (p ≈ k/(2πR*) · real14 PC–PC 4151–4294 MPa) — 접촉 유형 표지에 가깝고 하중이 아니다 (WEB-06).  '
                     '당김 접촉은 δ ≈ 0 면적이라 10⁴–10⁶ MPa 로 튄다.  하중 (z 차이) 은 AM 만 — 입자 응력 (LW) 보기로')
FN_MAX_RULE = ('최대 AM–AM 접촉 법선력 = AM 입자마다 그 입자의 AM–AM 접촉 중 압축 접촉 (δ > 0 · |Fn| > 0) 의 |Fn| 최대 × 1e6 / scale (µN · '
               'calc_contact_force_distribution 과 같은 환산 · fn_<쌍>_mean 과 같은 단위) · 당김 · 판정 불가 · δ ≤ 0 은 뺀다 · '
               '모델 단위 (덱 축척 환산 — 조성 비교 절대값에 쓰지 않는다)')
LW_VIEW_RULE = ('Love–Weber 입자 응력 = dem_analysis_core.calc_love_weber_stress (full_metrics stress_ratio_<상>_lw 와 같은 함수 · 같은 읽기 · '
                '같은 판 · 상자) 의 입자별 σ_VM · 비 = σ_VM,i / ⟨σ_VM⟩ (전 입자 · 접촉 없는 입자 포함 — stress_ratio 와 같은 분모) · '
                'MPa = × scale / 1e6 (모델 단위) · 벽 (바닥 · 판) 에 닿은 입자는 벽 힘이 없다 (접촉 덤프에 벽 접촉이 없다 — 그 입자의 값은 불완전)')
WALL_RULE = ('벽 표지 = calc_love_weber_stress 와 같은 규칙: 바닥 = z − r < 0 · 판 = z + r > plate_z (plate_z 가 mesh_info.json 의 판일 때만)')


def contact_force_sign(fn, p1, p2, r1, r2, box_xy=None, cp=None):
    """접촉 법선력의 부호 (열 배열) → int8 배열: +1 압축 (밀어냄) · −1 당김 (접착) · 0 판정 불가 · 힘 0 (CONTACT_SIGN_RULE).

    fn · p1 · p2 · cp = (n, 3) (sim) · r1 · r2 = (n,) · box_xy = (Lx, Ly) 이면 x · y 최소영상.  최소영상 뒤 중심 거리가 0 이거나
    1.5 (r1 + r2) 보다 멀면 (상자 없이 주기 경계 너머) 접촉점 cp 쪽 가지로 정한다 (|x_id1 − x_c| ≤ 1.05 r1 이면 그 가지 · 아니면
    |x_c − x_id2| ≤ 1.05 r2) · 그래도 못 정하면 0."""
    import numpy as np
    fn = np.asarray(fn, dtype=float).reshape(-1, 3)
    p1 = np.asarray(p1, dtype=float).reshape(-1, 3)
    p2 = np.asarray(p2, dtype=float).reshape(-1, 3)
    r1 = np.asarray(r1, dtype=float).reshape(-1)
    r2 = np.asarray(r2, dtype=float).reshape(-1)
    out = np.zeros(len(fn), dtype=np.int8)
    if not len(fn):
        return out

    def _mi(d):
        d = d.copy()
        if box_xy is not None:
            for ax, L in ((0, box_xy[0]), (1, box_xy[1])):
                L = float(L)
                if math.isfinite(L) and L > 0:
                    d[:, ax] -= L * np.round(d[:, ax] / L)
        return d
    with np.errstate(invalid='ignore', over='ignore'):
        fmag = np.linalg.norm(fn, axis=1)
        d = _mi(p1 - p2)
        dist = np.linalg.norm(d, axis=1)
        s = np.einsum('ij,ij->i', fn, d)
    live = np.isfinite(fmag) & (fmag > 0)
    valid = live & np.isfinite(dist) & (dist > 0) & (dist <= 1.5 * (r1 + r2)) & np.isfinite(s)
    out[valid & (s > 0)] = 1
    out[valid & (s < 0)] = -1
    if cp is not None:
        rest = live & ~valid
        if rest.any():
            cp = np.asarray(cp, dtype=float).reshape(-1, 3)
            with np.errstate(invalid='ignore', over='ignore'):
                b1, b2 = _mi(p1 - cp), _mi(cp - p2)
                n1, n2 = np.linalg.norm(b1, axis=1), np.linalg.norm(b2, axis=1)
                s1, s2 = np.einsum('ij,ij->i', fn, b1), np.einsum('ij,ij->i', fn, b2)
            near1 = rest & np.isfinite(n1) & (n1 > 0) & (n1 <= 1.05 * r1) & np.isfinite(s1)
            near2 = rest & ~near1 & np.isfinite(n2) & (n2 > 0) & (n2 <= 1.05 * r2) & np.isfinite(s2)
            out[near1 & (s1 > 0)] = 1
            out[near1 & (s1 < 0)] = -1
            out[near2 & (s2 > 0)] = 1
            out[near2 & (s2 < 0)] = -1
    return out


def _sig6(x):
    """유한값 → 유효 6 자리 float (전 입자 맵의 JSON 크기) · 아니면 None."""
    v = _fin(x)
    return float(f'{v:.6g}') if v is not None else None


def particle_load_view(cdf, atoms_raw, type_map, *, scale=1000.0, box_xy=None, box_source=None, plate_z=None,
                       plate_z_source=None, contacts_raw=None, lw_skip_reason=None):
    """입자 하중 보기 자료 (aux['load_view']) — 열 배열 (cdf: contacts.csv 표) 로 압력 · 힘 · 벽 · 부호, contacts_raw (생산 읽기
    dict 목록) 가 있으면 LW (정본 calc_love_weber_stress).  모든 맵의 키 = 원자 id (JSON 에서 문자열).  값 없는 칸은 0 으로 채우지 않는다.

    반환: schema · status · inputs {n_atoms · n_rows · n_rows_unknown_id · scale · box_xy · box_source · plate_z · plate_z_source · has_cp} ·
      sign {rule · n_compressive · n_attractive · n_unknown · n_zero_force} ·
      pressure {rule · max_MPa {id: 압축만 최대 · 유효 6 자리} · n_used · n_excluded_attractive · n_excluded_unknown · n_excluded_no_overlap ·
                n_particles · n_particles_legacy_higher (옛 stress_max 가 더 큰 입자 — 당김 · δ ≤ 0 · 힘 0 행에서 온 최대) · legacy_rule} ·
      am {n_am · n_am_by_type · fn_max_uN {AM id: µN} · fn_rule · n_am_without_am_contact · lw_status · lw_definition · lw_contract ·
          lw_quantity · lw_vm_MPa {AM id} · lw_ratio {AM id} · lw_mean_all_MPa · lw_type_ratio {상} · lw_rule · wall {AM id: floor · plate ·
          floor+plate} · wall_rule · wall_counts {n_floor · n_plate (전 입자)} · wall_counts_match_lw}."""
    import numpy as np
    import pandas as pd
    s = float(scale)
    out = {'schema': LOAD_VIEW_SCHEMA, 'status': None}
    ids = np.fromiter((int(a) for a in atoms_raw.keys()), dtype=np.int64, count=len(atoms_raw))
    vals = list(atoms_raw.values())
    pos = np.array([[a.get('x'), a.get('y'), a.get('z')] for a in vals], dtype=float).reshape(-1, 3)
    rad = np.array([a.get('radius') for a in vals], dtype=float)
    lbl = np.array([str(type_map.get(int(a.get('type', -1)), '')) for a in vals], dtype=object)
    is_am = np.array(['AM' in x for x in lbl], dtype=bool)
    n = len(ids)
    has_cp = all(c in cdf.columns for c in ('cp_x', 'cp_y', 'cp_z'))
    out['inputs'] = {'n_atoms': int(n), 'n_rows': int(len(cdf)), 'scale': s,
                     'box_xy': [float(box_xy[0]), float(box_xy[1])] if box_xy is not None else None, 'box_source': box_source,
                     'plate_z': _fin(plate_z), 'plate_z_source': plate_z_source, 'has_cp': bool(has_cp)}
    need = ('id1', 'id2', 'fn_x', 'fn_y', 'fn_z', 'contact_area', 'delta')
    miss = [c for c in need if c not in cdf.columns]
    if miss:
        out['status'] = f'NOT_COMPUTED (contacts.csv 에 {miss} 열이 없다)'
        return out
    idx = pd.Index(ids)

    def _ids(col):
        v = pd.to_numeric(cdf[col], errors='coerce').to_numpy(dtype=float)
        v = np.where(np.isfinite(v), v, -1).astype(np.int64)
        return idx.get_indexer(v)
    k1, k2 = _ids('id1'), _ids('id2')
    ok = (k1 >= 0) & (k2 >= 0)
    out['inputs']['n_rows_unknown_id'] = int((~ok).sum())
    k1, k2 = k1[ok], k2[ok]

    def num(c):
        return pd.to_numeric(cdf[c], errors='coerce').to_numpy(dtype=float)[ok]
    fn = np.stack([num('fn_x'), num('fn_y'), num('fn_z')], axis=1)
    area, delta = num('contact_area'), num('delta')
    cp = np.stack([num('cp_x'), num('cp_y'), num('cp_z')], axis=1) if has_cp else None
    with np.errstate(invalid='ignore', over='ignore'):
        fmag = np.linalg.norm(fn, axis=1)
    sgn = contact_force_sign(fn, pos[k1], pos[k2], rad[k1], rad[k2], box_xy=box_xy, cp=cp)
    live = np.isfinite(fmag) & (fmag > 0)
    out['sign'] = {'rule': CONTACT_SIGN_RULE, 'n_compressive': int((live & (sgn > 0)).sum()),
                   'n_attractive': int((live & (sgn < 0)).sum()), 'n_unknown': int((live & (sgn == 0)).sum()),
                   'n_zero_force': int((~live).sum())}

    # ── WEB-06 최대 접촉 압력 — 압축만 · 옛 stress_max (aggregate_particle_metrics: 면적 > 0 인 모든 행) 와 나란히 센다
    pconv = s / 1.0e6
    has_area = np.isfinite(area) & (area > 0)
    with np.errstate(invalid='ignore', over='ignore', divide='ignore'):
        p = np.where(has_area, fmag / np.where(has_area, area, 1.0) * pconv, 0.0)
    p = np.where(np.isfinite(p), p, 0.0)
    usable = has_area & np.isfinite(delta) & (delta > 0) & live
    comp, attr, unk = usable & (sgn > 0), usable & (sgn < 0), usable & (sgn == 0)
    pmax = np.zeros(n)
    np.maximum.at(pmax, k1[comp], p[comp])
    np.maximum.at(pmax, k2[comp], p[comp])
    leg = np.zeros(n)
    np.maximum.at(leg, k1[has_area], p[has_area])
    np.maximum.at(leg, k2[has_area], p[has_area])
    out['pressure'] = {
        'rule': PRESSURE_MAX_RULE,
        'max_MPa': {int(ids[k]): _sig6(pmax[k]) for k in np.flatnonzero(pmax > 0)},
        'n_used': int(comp.sum()), 'n_excluded_attractive': int(attr.sum()), 'n_excluded_unknown': int(unk.sum()),
        'n_excluded_no_overlap': int((~usable).sum()),
        'n_particles': int((pmax > 0).sum()),
        'n_particles_legacy_higher': int((leg > pmax * (1.0 + 1e-12)).sum()),
        'legacy_rule': ('옛 stress_max (aggregate_particle_metrics) = 면적 > 0 인 모든 행의 |Fn| / A 입자별 최대 — 당김 · δ ≤ 0 · 부호 없음 · '
                        '그대로 둔다 (바이트 같음)'),
    }

    # ── #11 AM 만 — 최대 AM–AM 접촉 법선력 (압축만 · µN)
    fconv = 1e6 / s
    am_pair = is_am[k1] & is_am[k2] & comp
    fmax = np.zeros(n)
    np.maximum.at(fmax, k1[am_pair], fmag[am_pair] * fconv)
    np.maximum.at(fmax, k2[am_pair], fmag[am_pair] * fconv)
    am_k = np.flatnonzero(is_am)
    by_type = {}
    for k in am_k:
        by_type[str(lbl[k])] = by_type.get(str(lbl[k]), 0) + 1
    am = {'n_am': int(len(am_k)), 'n_am_by_type': by_type,
          'fn_max_uN': {int(ids[k]): float(fmax[k]) for k in am_k if fmax[k] > 0}, 'fn_rule': FN_MAX_RULE,
          'n_am_without_am_contact': int(sum(1 for k in am_k if not fmax[k] > 0))}

    # ── 벽 표지 (calc_love_weber_stress 의 규칙)
    pz = _fin(plate_z)
    floor = (pos[:, 2] - rad) < 0.0
    plate_ok = plate_z_source == 'mesh' and pz is not None and pz > 0
    plate = ((pos[:, 2] + rad) > pz) if plate_ok else np.zeros(n, dtype=bool)
    wall = {}
    for k in am_k:
        tag = '+'.join(t for t, f in (('floor', floor[k]), ('plate', plate[k])) if f)
        if tag:
            wall[int(ids[k])] = tag
    am.update(wall=wall, wall_rule=WALL_RULE,
              wall_counts={'n_floor': int(floor.sum()), 'n_plate': int(plate.sum()) if plate_ok else None})

    # ── #11 AM 만 — Love–Weber (정본 함수 · 생산 읽기)
    am.update(lw_rule=LW_VIEW_RULE, lw_vm_MPa={}, lw_ratio={}, lw_mean_all_MPa=None, lw_type_ratio={}, wall_counts_match_lw=None,
              lw_definition=None, lw_contract=None, lw_quantity=None)
    if contacts_raw is None:
        am['lw_status'] = lw_skip_reason or 'NOT_COMPUTED (생산 읽기 접촉 목록이 없다)'
    else:
        try:
            from dem_analysis_core import calc_love_weber_stress
            bx, by = (box_xy if box_xy is not None else (None, None))
            ref = calc_love_weber_stress(atoms_raw, contacts_raw, type_map, plate_z, box_x=bx, box_y=by,
                                         plate_z_source=plate_z_source, return_arrays=True)
        except Exception as e:                                      # noqa: BLE001 — 상태로 남긴다 (압력 · 힘은 그대로)
            ref = {'status': f'FAILED ({type(e).__name__}: {e})'}
        am['lw_status'] = ref.get('status')
        for k_ in ('definition', 'contract', 'quantity'):
            am['lw_' + k_] = ref.get(k_)
        rw = ref.get('wall') or {}
        if rw:
            am['wall_counts_match_lw'] = bool(rw.get('n_floor') == am['wall_counts']['n_floor']
                                              and rw.get('n_plate') == am['wall_counts']['n_plate'])
        if ref.get('status') == 'OK':
            vm = ref['arrays_vm']
            mean_all = float(vm.mean())
            pos_lw = {int(a): j for j, a in enumerate(ref['ids'])}
            for k in am_k:
                j = pos_lw.get(int(ids[k]))
                if j is None:
                    continue
                am['lw_vm_MPa'][int(ids[k])] = float(vm[j]) * s / 1e6
                am['lw_ratio'][int(ids[k])] = float(vm[j]) / mean_all
            am['lw_mean_all_MPa'] = mean_all * s / 1e6
            am['lw_type_ratio'] = {str(t): float(v['ratio']) for t, v in (ref.get('type_stress') or {}).items()}
    out['am'] = am
    out['status'] = 'OK'
    return out


def particle_load_view_for_case(results_dir, type_map, scale=1000.0, row_budget=LW_VIEW_ROW_BUDGET):
    """케이스 폴더 → particle_load_view (생산 분석기와 같은 읽기 · 같은 판 높이 · 같은 상자).  /3d-data 가 aux['load_view'] 로 싣는다
    (발사 뒤 패치).  contacts.csv 행 수가 row_budget 보다 많으면 LW 만 계산하지 않는다 (상태 = NOT_COMPUTED (예산))."""
    import os
    import json
    import pandas as pd
    a_csv, c_csv = os.path.join(results_dir, 'atoms.csv'), os.path.join(results_dir, 'contacts.csv')
    if not (os.path.exists(a_csv) and os.path.exists(c_csv)):
        return {'schema': LOAD_VIEW_SCHEMA, 'status': 'NOT_COMPUTED (atoms.csv · contacts.csv 없음 — 접촉 덤프 없는 케이스)'}
    import analyze_contacts as _AC
    import dem_analysis_core as _D
    atoms_raw, _adf = _AC.load_atoms_raw(a_csv)
    with open(c_csv, 'rb') as f:
        n_rows = max(0, sum(1 for _ in f) - 1)
    contacts_raw, lw_skip = None, None
    if n_rows <= int(row_budget):
        contacts_raw, cdf = _AC.load_contacts_raw(c_csv)
    else:
        cdf = pd.read_csv(c_csv, low_memory=False)
        lw_skip = (f'NOT_COMPUTED (contacts.csv 행 {n_rows} > 예산 {int(row_budget)} — LW 를 계산하지 않았다 (생산 읽기 dict 목록의 메모리) · '
                   '압력 · 힘 · 벽 표지는 계산)')
    plate_z, pz_src = _D.get_plate_z(results_dir, atoms_raw, scale)
    box = _D._get_box_xy(results_dir)
    box_src = 'default_0.05'
    try:
        with open(os.path.join(results_dir, 'input_params.json')) as f:
            ip = json.load(f)
        if float(ip.get('box_x', 0)) > 0 and float(ip.get('box_y', 0)) > 0:
            box_src = 'input_params'
    except (OSError, ValueError, TypeError):
        pass
    return particle_load_view(cdf, atoms_raw, type_map, scale=scale, box_xy=box, box_source=box_src, plate_z=plate_z,
                              plate_z_source=pz_src, contacts_raw=contacts_raw, lw_skip_reason=lw_skip)
