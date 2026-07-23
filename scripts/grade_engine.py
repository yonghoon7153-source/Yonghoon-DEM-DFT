"""
grade_engine.py — Multi-axis quantitative grading for ASSB cathode cases.

Computes letter grades (A / B+ / B / B- / C+ / C / D) on 30+ axes spanning
structure, SE network topology, ionic/electronic/thermal transport,
interface coverage, electrochemical activity, mechanical stability,
cell-level ASR, and manufacturing quality.  Each axis has either
literature-anchored absolute thresholds or corpus-percentile thresholds
(read from docs/data/se_diagnostics_82.csv).

Literature anchors (sulfide ASSB cathode):
  • Porosity ε ≈ 10–15%        — Yoon 2025, Park 2023, Ohno 2020
  • SE percolation ≥ 99 %      — Bielefeld 2019, Liu & Yin 2025
  • τ_Laplace,eff ≤ 2.5         — Tippens 2019, Famprikis 2019
  • σ_ionic ≥ 0.1 mS/cm        — Janek/Zeier 2023 review threshold
  • σ_e   ≥ 0.5 mS/cm          — minimum for high-rate sulfide cathode
  • ASR_ionic ≤ 100 Ω·cm²       — workable @ 1 mAh/cm² C/3
  • Coverage AM ≥ 60 %          — Tabor-corrected, Mücke 2025
  • Ionic-active AM = 100 %     — Verma 2020 dead-zone criterion
  • Fragmentation+pulv ≤ 3 %    — Lawn 1998 force-ratio classifier

Output:
  build_overall_grade(metrics, corpus_rows=None) → {
      'axes':      [{label, value, grade, score, category,
                     formula, basis, meaning, direction}, …],
      'composite': {grade, score, weighted_score, n_axes},
      'category_scores': {cat_label: avg_score},
  }
"""
from __future__ import annotations
import csv
import math
import os
import statistics as _stat
from typing import Any, Iterable

# ── Letter grade scale ───────────────────────────────────────────────────
# Score 0–100 → letter via these cutoffs.  GPA-equivalent on a 4.3 scale
# so "composite_score" maps to a familiar 0-4.3 axis if needed.
GRADE_SCALE = [
    ('A',  92, 4.3),
    ('B+', 85, 3.7),
    ('B',  78, 3.3),
    ('B-', 70, 2.7),
    ('C+', 62, 2.3),
    ('C',  55, 2.0),
    ('D',   0, 1.0),
]
GRADE_COLOR = {
    'A':  '#10b981',   # emerald  — top tier
    'B+': '#84cc16',   # lime
    'B':  '#eab308',   # amber
    'B-': '#f97316',   # orange
    'C+': '#ef4444',   # red
    'C':  '#dc2626',   # darker red
    'D':  '#7f1d1d',   # deep red — fail
    '—':  '#6b7280',   # gray     — N/A
}


def score_to_grade(score: float) -> str:
    for label, cutoff, _gpa in GRADE_SCALE:
        if score >= cutoff:
            return label
    return 'D'


def grade_to_gpa(grade: str) -> float:
    for label, _cutoff, gpa in GRADE_SCALE:
        if label == grade:
            return gpa
    return 0.0


# ── Axis definitions ─────────────────────────────────────────────────────
# Each axis: (key, direction, thresholds, ...)
#   direction: 'higher' (large value good) or 'lower' (small value good)
#   thresholds: 6 cutoffs corresponding to A / B+ / B / B- / C+ / C
#               (anything beyond C drops to D)
#   For 'corpus' axes, the threshold is a list of percentiles (1-99) read
#   from the corpus CSV at runtime.
AXES: list[dict[str, Any]] = [

    # ── 1. 구조 (Structure) ──
    {'category': '구조 (Structure)',
     'key': 'porosity', 'label': 'Porosity ε (%)',
     'direction': 'band', 'optimum': 13.0, 'band_width': 4.0,
     # band: |val − optimum| ≤ 1.0 → A, ≤ 2.0 → B+, ≤ 3.0 → B, …
     'formula': 'ε = 1 − V_particles/V_electrode',
     'meaning': 'Sulfide ASSB cathode target 10–15% (Ohno 2020, Park 2023). '
                '너무 낮으면 SE 변형 한계, 너무 높으면 contact 부족.',
     'weight': 0.6},

    {'category': '구조 (Structure)',
     'key': 'thickness_um', 'label': '두께 T (μm)',
     'direction': 'band', 'optimum': 95.0, 'band_width': 35.0,
     'formula': 'T = z_max(plate) − z_min(substrate)  (target 60–130 μm)',
     'meaning': '60–130 μm = full-cell cathode 실용 범위. 박막(<40μm)은 '
                'unit cell test일 가능성 ↑, 후막(>150μm)은 ASR 폭증.',
     'weight': 0.4},

    # ── 2. SE 네트워크 위상 (Topology) ──
    {'category': 'SE 네트워크 위상',
     'key': 'percolation_pct', 'label': 'SE percolation top↔bot (%)',
     'direction': 'higher', 'thresholds': [99.0, 97.5, 95, 90, 80, 60],
     'formula': '% of SE in the connected component spanning bottom→top plates',
     'meaning': '★ 이온 percolation = 회복 불가능한 본질적 측면.  <95%면 dead-zone '
                '존재 → 이론 σ_ionic도 절반 이하 떨어짐 (Bielefeld 2019, Liu&Yin 2025).',
     'weight': 1.5},

    {'category': 'SE 네트워크 위상',
     'key': '__cut_fraction', 'label': 'Cut fraction (위상 robustness)',
     'direction': 'lower_corpus', 'corpus_key': 'cut_fraction',
     'corpus_filter_key': 'n_percolating',
     'formula': 'cut_fraction = n_articulation / n_percolating_SE',
     'meaning': '★ Cut node 1개 제거시 percolation 분리되는 비율 — 이온 path '
                'redundancy.  비가역 본질적 측면.',
     'weight': 1.2},

    {'category': 'SE 네트워크 위상',
     'key': '__bn_below_frac', 'label': 'Bottleneck burden',
     'direction': 'lower_corpus', 'corpus_key': 'bn_below_frac',
     'corpus_filter_key': 'n_percolating',
     'formula': 'n_bn_below_threshold / n_perc_edges  (A/r² < 10% × median)',
     'meaning': '★ 좁은 contact 비율 — σ_ionic constriction loss 직접 원인. '
                'sintering 압력으로만 개선 가능, 이미 다져진 cathode는 비가역.',
     'weight': 1.2},

    {'category': 'SE 네트워크 위상',
     'key': '__bn_median_norm', 'label': '백본 두께 (median A/r²)',
     'direction': 'higher_corpus', 'corpus_key': 'bn_median_norm',
     'corpus_filter_key': 'n_percolating',
     'formula': 'median(A_contact / r_min²) over percolating SE-SE edges',
     'meaning': '대표 contact의 dimensionless 크기. corpus median ≈ 0.28.',
     'weight': 0.7},

    # ── 3. SE 네트워크 통계 (Statistics) ──
    {'category': 'SE 네트워크 통계',
     'key': 'se_se_cn', 'label': '⟨z_SE-SE⟩ (coordination)',
     'direction': 'higher', 'thresholds': [5.5, 5.0, 4.5, 4.0, 3.5, 3.0],
     'formula': 'mean coordination number of SE particles to other SE',
     'meaning': '4–6 = packed, <3 = sparse (Mukhopadhyay 2014). RCP ≈ 6.',
     'weight': 0.4},

    {'category': 'SE 네트워크 통계',
     'key': 'se_se_cn_std', 'label': 'σ(z_SE-SE) (균질도)',
     'direction': 'lower', 'thresholds': [1.5, 1.7, 2.0, 2.3, 2.7, 3.2],
     'formula': 'std dev of SE coordination — packing inhomogeneity',
     'meaning': '낮으면 균일 packing, 높으면 일부 SE 고립/일부 over-coordinated.',
     'weight': 0.3},

    # ── 4. 경로 효율 (Path efficiency) ──
    {'category': '경로 효율 (Tortuosity)',
     'key': '__tau_lap_eff', 'label': 'τ_Laplace,eff ⭐',
     'direction': 'lower', 'thresholds': [1.8, 2.2, 2.8, 3.5, 4.5, 6.0],
     'formula': '√(φ_SE × σ_grain / σ_full)  — Stage E physics 우선, σ_grain=3 mS/cm',
     'meaning': 'COMSOL/EIS input tortuosity (Tippens 2019, Famprikis 2019). '
                '<2.5 우수, >5 endpoint dominated.  app.py 표시값과 동일 공식.',
     'weight': 1.0},

    {'category': '경로 효율 (Tortuosity)',
     'key': '__tau_lap_bulk', 'label': 'τ_Laplace,bulk (구조)',
     'direction': 'lower', 'thresholds': [1.2, 1.4, 1.7, 2.0, 2.5, 3.0],
     'formula': '√(φ_SE × σ_grain / σ_bulk_net)  — constriction 제외 (geometric Laplacian)',
     'meaning': 'Bruggeman 가정 φ^−0.5 ≈ 1.85.  τ_Dij와 다른 정량.',
     'weight': 0.5},

    {'category': '경로 효율 (Tortuosity)',
     'key': '__constriction_overhead',
     'label': 'Constriction overhead τ_eff/τ_bulk',
     'direction': 'lower', 'thresholds': [1.5, 1.8, 2.2, 2.8, 3.5, 5.0],
     'formula': 'τ_Laplace,eff / τ_Laplace,bulk — needs both Laplacian values',
     'meaning': '좁은 contact으로 인한 추가 저항 비율. 1배=geometric만, '
                '높을수록 constriction loss 큼.',
     'weight': 0.7},

    {'category': '경로 효율 (Tortuosity)',
     'key': 'tortuosity_recommended', 'label': 'τ_Dijkstra (geodesic)',
     'direction': 'lower', 'thresholds': [1.15, 1.25, 1.40, 1.60, 1.90, 2.40],
     'fallback_key': 'tortuosity_mean',
     'formula': 'Dijkstra median geodesic tortuosity (geometric path length / z)',
     'meaning': '구조적 우회만 (constriction 미포함). Laplacian과 다른 정량 — 일반적으로 '
                'τ_Lap_eff보다 훨씬 낮음.',
     'weight': 0.3},

    {'category': '경로 효율 (Tortuosity)',
     'key': 'path_hop_area_mean_physics', 'label': '⟨A_hop⟩ (μm², 평균)',
     'direction': 'higher', 'thresholds': [0.5, 0.3, 0.2, 0.1, 0.05, 0.02],
     'fallback_key': 'path_hop_area_mean',
     'formula': 'mean per-hop contact area along percolating paths',
     'meaning': '경로상 평균 contact 면적. Tabor (physics)에서 일반적으로 3-5배 더 큼.',
     'weight': 0.5},

    # ── 5. 계면 (Interface coverage) ──
    {'category': '계면 (Interface)',
     'key': 'coverage_AM_P_mean_physics', 'label': 'Coverage AM_P (%)',
     'direction': 'higher', 'thresholds': [70, 60, 50, 40, 30, 20],
     'fallback_key': 'coverage_AM_P_mean',
     'formula': 'Tabor-corrected SE-covered surface fraction of AM_P particles',
     'meaning': 'AM_P (대입자) 표면 중 SE가 닿은 비율. Mücke 2025 기준 ≥60% 권장.',
     'weight': 0.8},

    {'category': '계면 (Interface)',
     'key': 'coverage_AM_S_mean_physics', 'label': 'Coverage AM_S (%)',
     'direction': 'higher', 'thresholds': [70, 60, 50, 40, 30, 20],
     'fallback_key': 'coverage_AM_S_mean',
     'formula': 'Tabor-corrected SE-covered surface fraction of AM_S particles',
     'meaning': 'AM_S (소입자) 표면 coverage. bimodal 케이스에서 AM_P보다 더 균일해야 좋음.',
     'weight': 0.8},

    {'category': '계면 (Interface)',
     'key': 'coverage_AM_mean_physics_rough',
     'label': 'Coverage AM, shape-corr ⭐ (B3)',
     'direction': 'higher', 'thresholds': [65, 55, 45, 35, 25, 15],
     'fallback_key': 'coverage_AM_mean_physics',
     'formula': 'Tier-1 B3 shape-corrected total AM SE-coverage (%)',
     'meaning': 'Tier-1 보정 — 입자 ellipsoid 형상까지 반영한 가장 신뢰도 높은 coverage.',
     'weight': 0.7},

    {'category': '계면 (Interface)',
     'key': 'am_se_cn_mean', 'label': '⟨z_AM-SE⟩ (배위수)',
     'direction': 'higher', 'thresholds': [80, 60, 40, 25, 15, 8],
     'formula': 'mean # SE in contact per AM particle',
     'meaning': '활성 표면 redundancy. AM 입자마다 닿는 SE 개수 평균.',
     'weight': 0.5},

    # ── 6. 전기화학 활성도 (Activity) ──
    {'category': '전기화학 활성도',
     'key': 'ionic_active_pct', 'label': 'Ionic Active AM (%)',
     'direction': 'higher', 'thresholds': [99.5, 98, 95, 90, 80, 65],
     'formula': '% of AM connected to a top-reaching SE cluster',
     'meaning': '이온 공급이 닿는 AM 비율. <100%면 dead-zone AM 존재 (Verma 2020).',
     'weight': 1.2},

    {'category': '전기화학 활성도',
     'key': '__vulnerable_pct', 'label': 'Vulnerable AM (%)',
     'direction': 'lower', 'thresholds': [1, 3, 7, 12, 20, 30],
     'formula': 'am_vulnerable_pct (실제 metric, fallback: 100 − ionic_active)',
     'meaning': '연결은 됐지만 SE coverage가 낮아 cycling시 끊길 risk 높은 AM. '
                '실측 metric 우선 사용.',
     'weight': 0.6},

    # ── 7. 전자 전도 (Electronic) — VGCF 도전재로 회복 가능 → weight 낮음 ──
    {'category': '전자 전도',
     'key': '__am_percolation_pct', 'label': 'AM percolation top↔bot (%)',
     'direction': 'higher', 'thresholds': [90, 80, 70, 55, 40, 25],
     'formula': '% of AM in the connected component spanning bottom→top',
     'meaning': 'AM-AM contact percolation.  <70%면 VGCF 등 도전재 첨가 권장 — '
                '회복 가능한 측면이라 가중치 낮음.',
     'weight': 0.5},

    {'category': '전자 전도',
     'key': '__electronic_active_pct', 'label': 'CC-connected AM (%)',
     'direction': 'higher', 'thresholds': [90, 80, 70, 55, 40, 25],
     'formula': 'electronic_active_fraction × 100',
     'meaning': '하단 current collector까지 전자가 도달 가능한 AM 비율. '
                'VGCF로 회복 가능.',
     'weight': 0.5},

    {'category': '전자 전도',
     'key': 'electronic_sigma_full_mScm_stage_e_physics',
     'label': 'σ_e Stage E (mS/cm)',
     'direction': 'higher', 'thresholds': [5, 2, 1, 0.5, 0.2, 0.05],
     'fallback_key': 'electronic_sigma_full_mScm_physics',
     'formula': 'Stage E final electronic conductivity',
     'meaning': '★ 무도전재 sulfide cathode σ_e.  단, VGCF / carbon black 1-3 wt% '
                '첨가로 10-100× 회복 가능한 metric (Mücke 2025).  따라서 가중치 낮음 '
                '— ranking에서 핵심 차별 요소 아님.  What-if 도전재 토글로 시뮬레이션.',
     'weight': 0.35},

    # ── 8. 기계적 안정성 (Mechanical) ───────────────────────────────────
    # DEM 초기 compaction (300 MPa) 시점의 fracture만 측정 — cycling-induced
    # fracture와는 다른 메커니즘.  Stage별 Li 저장 손실 (문헌 consensus):
    #   • Microcrack: precursor only — SE infiltration으로 healing 가능 (NPG
    #     Asia 2024 "Infiltration-driven enhancement", Sci Direct 2023
    #     "Revealing crack-healing mechanism").  → low weight.
    #   • Multi-crack: 일부 healable + fresh AM-SE interface 생성 (Lee 2025
    #     ACS EL이 7:3 P-heavy에서 multi-crack 많아도 87.8% retention 최고
    #     보고한 이유).  → low weight.
    #   • Fragmentation: 부분 electrical disconnect → 부분 capacity loss.
    #   • Pulverization: 완전 분해 → electronic contact 끊김 → 진짜 capacity loss.
    # → severe(frag+pulv)만 강하게, multi-crack/index는 약하게.
    {'category': '기계적 안정성',
     'key': '__frac_severe_force_pct', 'label': 'Fragmentation+Pulv (%)',
     'direction': 'lower', 'thresholds': [0.5, 1.5, 3, 6, 10, 18],
     'formula': '(frac_fragmentation + frac_pulverization) [force-based]',
     'meaning': '입자 완전 파괴 비율 — 비가역 capacity loss.  '
                'multi-crack과 달리 진짜 손상.',
     'weight': 0.8},

    {'category': '기계적 안정성',
     'key': 'frac_multicrack_force_pct', 'label': 'Multi-crack (%)',
     'direction': 'lower', 'thresholds': [3, 6, 10, 16, 25, 40],
     'fallback_key': 'frac_multicrack_pct',
     'formula': 'frac_multicrack_force_pct — Lawn stage 2 (compaction-time)',
     'meaning': 'DEM compaction 시점 multi-crack.  ASSB에서는 일부 multi-crack '
                '이 fresh AM-SE interface 생성 (Lee 2025).  weight 낮음.',
     'weight': 0.25},

    {'category': '기계적 안정성',
     'key': 'fracture_index_force', 'label': 'Fracture index (compaction)',
     'direction': 'lower', 'thresholds': [0.05, 0.10, 0.20, 0.35, 0.55, 0.80],
     'fallback_key': 'fracture_index',
     'formula': 'Σ stage_weight × frac_stage / 4 (compaction-time only)',
     'meaning': 'DEM compaction fracture composite index — cycling-induced fracture '
                '아님.  Lee 2025 ACS EL: P-heavy (7:3)가 DEM multi-crack 많아도 '
                'cycling capacity retention 1순위 87.8%.  weight 낮춤.',
     'weight': 0.4},

    {'category': '기계적 안정성',
     'key': '__sigma_vm_cv_pct', 'label': 'CV(σ_VM) (%)',
     'direction': 'lower', 'thresholds': [100, 130, 160, 200, 250, 320],
     'formula': '100 × stress_cv  (CV = σ(stress) / ⟨stress⟩)',
     'meaning': '응력 분포 불균일도 — hotspot 식별.',
     'weight': 0.3},

    # ── 9. 전도도 (Absolute conductivity) ──
    {'category': '전도도 절대값',
     'key': 'sigma_full_mScm_stage_e_physics',
     'label': 'σ_ionic Stage E (mS/cm) ⭐★',
     'direction': 'higher', 'thresholds': [0.5, 0.3, 0.15, 0.08, 0.04, 0.01],
     'fallback_key': 'sigma_full_mScm_physics',
     'formula': 'Stage E final ionic conductivity (Cronau SE-size factor)',
     'meaning': '★★ 이온 전도도 — 회복 불가능한 본질적 측면.  '
                '실측 sulfide composite 0.1–0.5 mS/cm (Janek 2023).  TOP KPI.',
     'weight': 2.0},

    {'category': '전도도 절대값',
     'key': 'thermal_sigma_full_mScm_stage_e_physics',
     'label': 'κ Stage E (mS/cm equiv) ⭐',
     'direction': 'higher', 'thresholds': [8, 5, 3, 1.5, 0.7, 0.2],
     'fallback_key': 'thermal_sigma_full_mScm_physics',
     'formula': 'Stage E final thermal conductivity (Wang phonon GB-scattering)',
     'meaning': '열 발산 능력. sulfide cell에서 1차 성능 결정 인자 아님.',
     'weight': 0.2},

    {'category': '전도도 절대값',
     'key': 'R_brug_over_full_physics',
     'label': 'Bruggeman overestimation',
     'direction': 'lower', 'thresholds': [2.0, 3.0, 4.5, 6.5, 9.0, 13.0],
     'fallback_key': 'R_brug_over_full',
     'formula': 'σ_Bruggeman_EMT / σ_full_network — EMT theoretical vs actual ratio',
     'meaning': '이상 균질 매질 가정의 과대평가 배수. σ_ionic과 정보 일부 중복.',
     'weight': 0.3},

    {'category': '전도도 절대값',
     'key': '__constriction_R_fraction_pct',
     'label': 'Constriction R fraction (%)',
     'direction': 'lower', 'thresholds': [40, 55, 65, 75, 85, 92],
     'formula': '100 × (1 − bulk_resistance_fraction)  — fraction from contact constriction',
     'meaning': '전체 저항 중 contact constriction 기여도. bn_below_frac과 정보 일부 중복.',
     'weight': 0.3},

    # ── 10. 셀 ASR + 에너지 밀도 ──
    {'category': '에너지 밀도 (Energy density)',
     'key': '__Q_gravimetric_mAhg', 'label': 'Q_gravimetric (mAh/g 복합체) ⭐★',
     'direction': 'higher', 'thresholds': [160, 148, 135, 120, 100, 80],
     'formula': 'wt_AM × C_AM  (NCM811 real C ≈ 190 mAh/g)',
     'meaning': '★★★ 비용량 = 무게당 에너지.  산업 KPI 1위 (Wh/kg).  '
                '85:15 → 162, 82:18 → 156, 75:25 → 142, 72:28 → 137, 60:40 → 114 mAh/g.',
     'weight': 5.0},

    {'category': '에너지 밀도 (Energy density)',
     'key': '__Q_volumetric_mAhcc', 'label': 'Q_volumetric (mAh/cc) ⭐★',
     'direction': 'higher', 'thresholds': [600, 520, 440, 360, 290, 220],
     'formula': 'ρ_composite × wt_AM × C_AM × (1−ε) — 부피 용량',
     'meaning': '★★★ 부피당 에너지 = Wh/L.  ASSB 상용화 목표 ≥500 mAh/cc (Janek 2023). '
                '산업 KPI 1위와 동격.',
     'weight': 4.5},

    {'category': '에너지 밀도 (Energy density)',
     'key': '__commercial_composition', 'label': '상용 조성 band (AM:SE) ⭐★',
     'direction': 'band', 'optimum': 82.0, 'band_width': 6.0,
     'formula': 'wt_AM(%) 의 band-around-optimum (82±6 = 76-88% 상용 sweet spot)',
     'meaning': '★★ commercial sulfide cathode 75-90% AM가 sweet spot (Janek 2023, '
                'Mücke 2025).  비용 + 에너지 밀도 두 측면 동시 반영.',
     'weight': 2.5},

    {'category': '에너지 밀도 (Energy density)',
     'key': '__wt_am_pct', 'label': 'wt_AM (%) — 활물질 무게비',
     'direction': 'higher', 'thresholds': [85, 82, 78, 73, 65, 55],
     'formula': '100 × m_AM / (m_AM + m_SE)',
     'meaning': '활물질 무게 비율.  Q_gravimetric이 이미 반영하지만 '
                '70% 미만 strong drop은 별도 시각화 위해 유지.',
     'weight': 1.5},

    {'category': '에너지 밀도 (Energy density)',
     'key': '__Q_target_match_pct', 'label': '목표 면용량 달성도 (%)',
     'direction': 'higher', 'thresholds': [95, 88, 80, 70, 55, 40],
     'formula': 'min(Q_actual/Q_target, Q_target/Q_actual) × 100',
     'meaning': '"6 mAh/cm² 의도한 case가 실제 달성하는가" 정합성 체크. '
                'tier 없는 case (particulate / S)는 N/A.',
     'weight': 0.8},

    {'category': '에너지 밀도 (Energy density)',
     'key': '__ps_ratio_band', 'label': 'P:S 조성 band (P-heavy 7:3) ⭐',
     'direction': 'band', 'optimum': 70.0, 'band_width': 15.0,
     'formula': 'P:S ratio의 P fraction (%) — band around 70% (= 7:3)',
     'meaning': '★ 다수 문헌 일관: bimodal cathode P:S 7:3 최적.  '
                '(a) Lee 2025 ACS EL: 87.8% retention@200cyc 최고. '
                '(b) ScienceDirect 2021 "cathode architecture": geometric packing '
                '큰 입자 위주 + 작은 입자 void 채움.  '
                '(c) ACS Appl Mater 2025 "Toughened Bimodal": interface heterogeneity 이득. '
                '주의: 우리 DEM은 geometric packing만 잡고 crystallinity (poly vs SC) 차이 못 잡음 — '
                'axis는 절반만 직접 측정.  ★ monomodal case는 N/A (P:S 무의미) — '
                'monomodal로서 평가됨, 페널티 없음.',
     'weight': 1.2},

    # ── 11. 설계 / 입자 정보 (Design info — informational only) ──
    # NOTE: r_SE / λ_eff는 input 파라미터일 뿐 성능 측정이 아니므로 weight 매우 낮게.
    # 성능 측정은 cell이 실제로 보이는 σ_ionic / ASR / fracture로 평가됨.
    {'category': '설계 정보 (Design info)',
     'key': '__r_SE_um', 'label': 'r_SE (μm) — SE 입자 반경',
     'direction': 'lower', 'thresholds': [0.4, 0.6, 0.9, 1.2, 1.5, 2.0],
     'formula': 'input_params.r_SE × scale → μm',
     'meaning': '입력 SE 입자 크기.  점수 영향 작음 (informational).  '
                '실제 성능은 σ_ionic / cut_fraction / bn_below_frac이 측정.',
     'weight': 0.1},

    {'category': '설계 정보 (Design info)',
     'key': '__lambda_eff', 'label': 'λ_eff = r_AM / r_SE',
     'direction': 'higher', 'thresholds': [8, 6, 4, 3, 2, 1.5],
     'formula': 'r_AM (P 우선) / r_SE',
     'meaning': '설계 비율.  점수 영향 작음 (informational).  '
                '실제 fragility는 cut_fraction (corpus percentile)이 측정.',
     'weight': 0.1},

    {'category': '설계 정보 (Design info)',
     'key': '__stage_e_available', 'label': 'Stage E 보정 적용',
     'direction': 'higher', 'thresholds': [1, 1, 1, 0.5, 0.5, 0.5],
     'formula': '1 if Stage E σ 존재 else 0.5',
     'meaning': 'QA flag — Stage E (Cronau / Trevisanello / Wang) 적용 여부. '
                '미적용시 σ 과대평가 가능.',
     'weight': 0.3},

    {'category': '설계 정보 (Design info)',
     'key': '__compaction_efficiency', 'label': '압축 효율 (300 MPa porosity)',
     'direction': 'band', 'optimum': 15.0, 'band_width': 5.0,
     'formula': 'porosity (%) at target_press_sim ≈ 0.3 (300 MPa)',
     'meaning': '300 MPa 압축시 실험 sulfide cathode porosity 12-18% 범위. '
                '<10% over-compress (fracture risk), >22% under-compress (poor contact).',
     'weight': 0.4},

    {'category': '설계 정보 (Design info)',
     'key': '__bimodal_design', 'label': 'bimodal 설계 (packing efficiency) ⭐',
     'direction': 'higher', 'thresholds': [1, 1, 1, 0.5, 0.5, 0.5],
     'formula': 'bimodal → 1.0 (A);  monomodal → N/A (페널티 없음)',
     'meaning': '★ commercial NCM cathode는 거의 항상 bimodal (대입자+소입자) '
                'packing density ↑.  ★ monomodal은 N/A — "bimodal 아님" 페널티 '
                '대신 monomodal로서 평가.  bimodal 우위는 실제 porosity / σ_ionic / '
                'energy density axes에 이미 반영됨 (double-count 방지).',
     'weight': 1.0},

    {'category': '설계 정보 (Design info)',
     'key': '__volume_change_buffer', 'label': '부피변화 buffer (porosity 적정성)',
     'direction': 'higher', 'thresholds': [15, 12, 10, 8, 6, 4],
     'formula': 'porosity (%) — NCM 충방전시 ~5% 부피 변화 흡수 가능한 여유',
     'meaning': 'cycling 동안 NCM 부피 ~5% 변화 → SE 박리 위험. '
                '≥10% porosity = 충분한 buffer, <6% = 위험.  '
                '압축 효율의 cycling-stability side.',
     'weight': 0.4},

    # ── 12. 셀 ASR — 이온 측 강화, 전자 측 축소 ──
    {'category': '셀 단위 ASR',
     'key': '__asr_ionic_Ohm_cm2', 'label': 'ASR_ionic (Ω·cm²) ⭐★',
     'direction': 'lower', 'thresholds': [30, 60, 100, 160, 250, 400],
     'formula': 'ASR = L_cathode(μm) × 0.1 / σ_ionic(mS/cm)',
     'meaning': '★★ 이온 ASR — 회복 불가능.  1mAh/cm² C/3에서 ≤100 workable. '
                '주의: SE-rich (72:28)가 자동으로 낮은 ASR → 에너지 밀도와 함께 봐야.',
     'weight': 2.5},

    {'category': '셀 단위 ASR',
     'key': '__Q_areal_mAhcm2', 'label': 'Q_areal (mAh/cm²) ⭐',
     'direction': 'higher', 'thresholds': [5.0, 3.5, 2.5, 1.5, 0.8, 0.3],
     'formula': 'Q_areal = T(μm) × ρ_AM × C_AM × wt_AM × 1e-4 '
                '(ρ_NMC ≈ 4.7, C_NMC ≈ 175 mAh/g)',
     'meaning': '면용량 — high-capacity cell이면 같은 ASR이라도 더 가치 ↑. '
                '박막(<2 mAh/cm²)은 unit-cell test, >5는 commercial target.',
     'weight': 1.5},

    {'category': '셀 단위 ASR',
     'key': '__ASR_per_capacity', 'label': 'ASR/Q_areal (Ω·cm²/mAh/cm²) ⭐',
     'direction': 'lower', 'thresholds': [10, 20, 35, 55, 90, 150],
     'formula': '(L × 0.1 / σ_ionic) / Q_areal  — 두께·용량 보정 ASR',
     'meaning': '★ "후막일수록 harsh" 패널티의 핵심 — 같은 ASR이라도 박막은 '
                '낮은 capacity로 인해 ratio가 나빠짐. <20 = 우수, >100 = 위험.',
     'weight': 1.6},

    {'category': '셀 단위 ASR',
     'key': '__asr_electronic_Ohm_cm2', 'label': 'ASR_electronic (Ω·cm²)',
     'direction': 'lower', 'thresholds': [2, 5, 10, 20, 40, 80],
     'formula': 'ASR_e = L_cathode × 0.1 / σ_e_stage_e',
     'meaning': '전자전도 영역 저항.  σ_e 동일 — VGCF/도전재로 회복 가능하므로 '
                '가중치 낮음.  본질적 차별 측면 아님.',
     'weight': 0.35},

    {'category': '셀 단위 ASR',
     'key': '__asr_thermal_Kcm2_W', 'label': 'ASR_thermal (K·cm²/W)',
     'direction': 'lower', 'thresholds': [1.5, 2.5, 4, 6, 9, 14],
     'formula': 'ASR_th = L_cathode × 0.1 / κ',
     'meaning': '냉각 효율. sulfide cell에서 1차 성능 결정 인자 아님.',
     'weight': 0.15},

    {'category': '셀 단위 ASR',
     'key': '__ASR_total_Ohm_cm2', 'label': 'ASR_total (Ω·cm²) — i+e 합 ⭐',
     'direction': 'lower', 'thresholds': [40, 80, 130, 200, 320, 500],
     'formula': 'ASR_ionic + ASR_electronic — same circuit, 더해서 셀 전체 저항',
     'meaning': '단일 저항 axis로는 ASR_ionic만으로 전체 그림 못 봄.  '
                '도전재 없는 sulfide cathode는 ASR_e도 비교 가능 규모.',
     'weight': 1.2},

    {'category': '셀 단위 ASR',
     'key': '__c_rate_capability', 'label': 'C-rate proxy (1/ASR_total)',
     'direction': 'higher', 'thresholds': [0.025, 0.012, 0.008, 0.005, 0.003, 0.002],
     'formula': '1 / ASR_total  — 단위 mhos/cm² (역수)',
     'meaning': '같은 capacity면 ASR 낮을수록 high-rate 가능.  ASR_total과 정보 중복 '
                '있으나 "rate capability" 직관적 해석용.',
     'weight': 0.4},

    {'category': '셀 단위 ASR',
     'key': '__polarization_mV_at_C3', 'label': '분극 η @ C/3 (mV) ⭐',
     'direction': 'lower', 'thresholds': [30, 60, 100, 160, 250, 400],
     'formula': 'η = i × (ASR_ionic + ASR_e),  i = 0.33 mA/cm² (C/3 of 1 mAh/cm²)',
     'meaning': '★ 실제 작동 분극 전압 drop.  관측 가능량.  EIS / 셀 측정 직접 비교.',
     'weight': 1.5},

    # ── 12. 안전성 (Safety) ──
    {'category': '안전성 (Safety)',
     'key': '__am_am_short_risk_cn', 'label': 'AM-AM ⟨z⟩ (short risk)',
     'direction': 'band', 'optimum': 2.5, 'band_width': 1.5,
     'fallback_key': 'am_am_cn',
     'formula': 'am_am_cn — AM 입자 평균 AM-AM 접촉 수',
     'meaning': 'AM-AM 연결도. 2-3이 sweet spot — 너무 낮으면(<1) 전자전도 빈약, '
                '너무 높으면(>4.5) electrons direct path 형성 → internal short risk + '
                'SE 침투 어려움. Band-around-optimum scoring.',
     'weight': 0.5},

    # NOTE: 'Stress hotspot density' 축 제거됨.  CV(σ_VM) × 0.05 같은 근사 대신
    # 실 데이터 (particle_max_fpc per-particle count)가 metrics에 들어오면
    # 그때 진짜 axis로 추가.  현재는 stress_cv 자체로 충분 (기계적 안정성에 있음).

    # ── 13. 수명 (Cycling) — 비가역 KPI ──
    {'category': '수명 (Cycling)',
     'key': '__cycle_stable_AM_pct', 'label': 'Cycle-stable AM (%) ⭐★',
     'direction': 'higher', 'thresholds': [95, 90, 80, 70, 55, 40],
     'formula': '(1 − fracture_severe/100) × (ionic_active/100) × (electronic_active/100) × 100',
     'meaning': '★★ 합성 cycling 안정성 — 활성+전자연결+심각손상없음 동시 만족 AM 비율. '
                '비가역 (한번 fracture된 입자는 영구).  cycling life KPI 1순위.',
     'weight': 1.8},

    {'category': '수명 (Cycling)',
     'key': '__sigma_e_fracture_loss_pct',
     'label': 'σ_e fracture-induced loss (%)',
     'direction': 'lower', 'thresholds': [10, 25, 40, 55, 70, 85],
     'formula': '100 × (σ_e_baseline − σ_e_stage_e) / σ_e_baseline',
     'meaning': 'fracture로 σ_e 손실 비율.  단, σ_e 자체는 VGCF로 회복 가능 → weight 낮음.',
     'weight': 0.3},

    # ── 14. 가공 / 신뢰성 (Manufacturability) ──
    {'category': '가공 신뢰성',
     'key': '__validation_pass_pct', 'label': 'Validation trust (%)',
     'direction': 'higher', 'thresholds': [95, 85, 75, 60, 45, 25],
     'formula': '% of validation_flags marked OK in trust card',
     'meaning': 'Stage E self-report card 통과율. 100=fully reproducible, <60=의심.',
     'weight': 0.5},
]


# ── Per-axis scoring ─────────────────────────────────────────────────────
def _interp_score(value: float, thresholds: list[float],
                   direction: str) -> float:
    """Linearly interpolate value→score(0–100) using 6-cutoff thresholds.

    thresholds = [t_A, t_B+, t_B, t_B-, t_C+, t_C]
      direction='higher' → t_A ≥ t_B+ ≥ … (large is good)
      direction='lower'  → t_A ≤ t_B+ ≤ … (small is good)
    Anchor scores at 95, 88, 80, 72, 64, 56.  Beyond C → linear toward 30.
    """
    anchors = [95, 88, 80, 72, 64, 56]
    if direction == 'higher':
        if value >= thresholds[0]: return 100
        for i in range(len(thresholds) - 1):
            t_hi, t_lo = thresholds[i], thresholds[i + 1]
            if value >= t_lo:
                if t_hi == t_lo: return anchors[i]
                u = (value - t_lo) / (t_hi - t_lo)
                return anchors[i + 1] + (anchors[i] - anchors[i + 1]) * u
        t_lo = thresholds[-1]
        if value <= 0: return 0
        return max(0, 56 * (value / max(t_lo, 1e-12)))
    else:  # 'lower'
        if value <= thresholds[0]: return 100
        for i in range(len(thresholds) - 1):
            t_lo, t_hi = thresholds[i], thresholds[i + 1]
            if value <= t_hi:
                if t_hi == t_lo: return anchors[i]
                u = (t_hi - value) / (t_hi - t_lo)
                return anchors[i + 1] + (anchors[i] - anchors[i + 1]) * u
        t_hi = thresholds[-1]
        if value <= 0: return 100
        return max(0, 56 - 30 * (value / max(t_hi, 1e-12) - 1))


def _band_score(value: float, optimum: float, band_width: float) -> float:
    """Band-around-optimum scoring (used for porosity, thickness).

    score = 100 at value == optimum, drops linearly to 56 at
    |value − optimum| == band_width, then continues linearly toward 0.
    """
    dist = abs(value - optimum)
    if dist <= band_width * 0.2:  return 100
    if dist >= band_width * 2.5:  return max(0, 30 - 5 * (dist / band_width - 2.5))
    # Linear interpolation between band stops 0.2/0.6/1.0/1.5/2.0/2.5 of band_width
    stops = [(0.2, 100), (0.6, 88), (1.0, 78), (1.5, 68), (2.0, 56), (2.5, 30)]
    for i in range(len(stops) - 1):
        u_lo, s_lo = stops[i]
        u_hi, s_hi = stops[i + 1]
        d_lo, d_hi = u_lo * band_width, u_hi * band_width
        if d_lo <= dist <= d_hi:
            if d_hi == d_lo: return s_lo
            u = (dist - d_lo) / (d_hi - d_lo)
            return s_lo + (s_hi - s_lo) * u
    return 30


# ── Corpus context for ranking-based axes ────────────────────────────────
def _load_corpus(csv_path: str | None) -> list[dict]:
    if not csv_path or not os.path.exists(csv_path):
        return []
    with open(csv_path, newline='') as f:
        return list(csv.DictReader(f))


def _passes_filter(row: dict, filter_key: str | None) -> bool:
    """Whether a corpus row should be included in percentile / threshold
    calculations.  When `filter_key` is set, the row must have a positive
    float value at that key (used to exclude non-percolating cases from
    percolation-only metrics like cut_fraction)."""
    if not filter_key:
        return True
    try:
        v = float(row.get(filter_key))
    except (TypeError, ValueError):
        return False
    return math.isfinite(v) and v > 0


def _corpus_percentile(rows: Iterable[dict], key: str, value: float,
                        filter_key: str | None = None) -> dict | None:
    """Return {pct, n, lo, med, hi} — value's percentile rank in corpus[key]."""
    arr = []
    for r in rows:
        if not _passes_filter(r, filter_key):
            continue
        v = r.get(key)
        try:
            v = float(v)
        except (TypeError, ValueError):
            continue
        if math.isfinite(v):
            arr.append(v)
    if not arr:
        return None
    arr.sort()
    i = 0
    while i < len(arr) and arr[i] < value:
        i += 1
    return {
        'pct': round(100 * i / len(arr), 1),
        'n':   len(arr),
        'lo':  arr[0], 'med': arr[len(arr) // 2], 'hi': arr[-1],
    }


def _corpus_threshold_scores(rows: Iterable[dict], corpus_key: str,
                              direction: str,
                              filter_key: str | None = None) -> list[float] | None:
    """Derive 6 percentile cutoffs from corpus for corpus-relative axes.

    direction='lower_corpus'  → [p10, p25, p40, p55, p70, p85] (low percentile = high grade)
    direction='higher_corpus' → [p90, p75, p60, p45, p30, p15] (high percentile = high grade)

    When `filter_key` is provided, only corpus rows where filter_key > 0
    are considered (so non-percolating cases don't skew the distribution
    for percolating-only metrics).
    """
    arr = []
    for r in rows:
        if not _passes_filter(r, filter_key):
            continue
        try:
            v = float(r.get(corpus_key))
        except (TypeError, ValueError):
            continue
        if math.isfinite(v):
            arr.append(v)
    if len(arr) < 5:
        return None
    arr.sort()

    def pct(p):
        i = max(0, min(len(arr) - 1,
                        int(round(p / 100 * (len(arr) - 1)))))
        return arr[i]

    if direction == 'lower_corpus':
        return [pct(10), pct(25), pct(40), pct(55), pct(70), pct(85)]
    else:
        return [pct(90), pct(75), pct(60), pct(45), pct(30), pct(15)]


# ── Derived metrics (not directly in full_metrics.json) ──────────────────
def _sigma_e_effective(metrics: dict) -> float | None:
    """Pick the best σ_e value available, honouring a carbon override.

    When metrics contains '_sigma_e_override_mScm' (injected by the What-if
    panel), that value wins.  Otherwise fall back through the Stage-E /
    physics / Hertzian chain.
    """
    override = metrics.get('_sigma_e_override_mScm')
    if override is not None:
        try:
            return float(override)
        except (TypeError, ValueError):
            pass
    for k in ('electronic_sigma_full_mScm_stage_e_physics',
              'electronic_sigma_full_mScm_physics',
              'electronic_sigma_full_mScm_stage_e',
              'electronic_sigma_full_mScm'):
        v = metrics.get(k)
        if v is not None:
            try:
                return float(v)
            except (TypeError, ValueError):
                continue
    return None


def _sigma_ionic_effective(metrics: dict) -> float | None:
    for k in ('sigma_full_mScm_stage_e_physics', 'sigma_full_mScm_physics',
              'sigma_full_mScm_stage_e', 'sigma_full_mScm'):
        v = metrics.get(k)
        if v is not None:
            try:
                return float(v)
            except (TypeError, ValueError):
                continue
    return None


def _kappa_effective(metrics: dict) -> float | None:
    for k in ('thermal_sigma_full_mScm_stage_e_physics',
              'thermal_sigma_full_mScm_physics',
              'thermal_sigma_full_mScm_stage_e',
              'thermal_sigma_full_mScm'):
        v = metrics.get(k)
        if v is not None:
            try:
                return float(v)
            except (TypeError, ValueError):
                continue
    return None


def _composition_of(metrics: dict) -> str:
    """Determine cathode morphology class from ps_ratio / particle counts.

    Returns 'bimodal' | 'mono AM_P' | 'mono AM_S' | 'unknown'.

    Monomodal cases (mono AM_P / mono AM_S) are valid design choices and
    should NOT be penalised against bimodal-specific criteria (P:S ratio
    band, bimodal-packing axis).  Those axes return N/A for monomodal so
    the case is judged on its own performance metrics instead.
    """
    # Particle counts (most reliable)
    n_p = metrics.get('AM_P_n_particles')
    n_s = metrics.get('AM_S_n_particles')
    try:
        if n_p is not None and n_s is not None:
            np_, ns_ = float(n_p), float(n_s)
            if np_ > 0 and ns_ > 0: return 'bimodal'
            if np_ > 0:             return 'mono AM_P'
            if ns_ > 0:             return 'mono AM_S'
    except (TypeError, ValueError):
        pass
    # ps_ratio "P:S"
    ps = metrics.get('ps_ratio') or metrics.get('_meta_ps_ratio') or ''
    if isinstance(ps, str) and ':' in ps:
        try:
            a, b = (float(x) for x in ps.replace(' ', '').split(':')[:2])
            if a > 0 and b > 0: return 'bimodal'
            if a > 0:           return 'mono AM_P'
            if b > 0:           return 'mono AM_S'
        except (ValueError, IndexError):
            pass
    # mode metadata
    mode = metrics.get('_meta_mode') or metrics.get('mode')
    if mode == 'bimodal':  return 'bimodal'
    return 'unknown'


def _derived_value(key: str, metrics: dict) -> float | None:
    """Compute axis values that aren't stored as a single metric key."""
    if key == '__cut_fraction':
        aux = metrics.get('_aux_se_diag') or {}
        n_perc = aux.get('n_percolating') or 0
        n_cut  = aux.get('n_articulation_points')
        if n_cut is None:
            apts = aux.get('articulation_points')
            n_cut = len(apts) if isinstance(apts, list) else None
        if n_perc and n_cut is not None:
            return n_cut / n_perc
        return None

    if key == '__bn_below_frac':
        aux = metrics.get('_aux_se_diag') or {}
        nb = aux.get('n_bn_below_threshold')
        ne = aux.get('n_perc_edges')
        if nb is not None and ne and ne > 0:
            return nb / ne
        return None

    if key == '__bn_median_norm':
        aux = metrics.get('_aux_se_diag') or {}
        v = aux.get('bn_median_norm') or aux.get('se_bn_median_norm')
        try:
            return float(v) if v is not None else None
        except (TypeError, ValueError):
            return None

    if key == '__frac_severe_force_pct':
        a = metrics.get('frac_fragmentation_force_pct') or 0
        b = metrics.get('frac_pulverization_force_pct') or 0
        if a == 0 and b == 0:
            a = metrics.get('frac_fragmentation_pct') or 0
            b = metrics.get('frac_pulverization_pct') or 0
        return a + b

    if key == '__sigma_vm_cv_pct':
        # stress_cv 는 case에 따라 fraction(0-3) 또는 percentage(50-300)로
        # 저장됨 — analyze_contacts.py vintage에 따라 다름.  자동 감지:
        cv = metrics.get('stress_cv')
        if cv is None:
            return None
        try:
            v = float(cv)
        except (TypeError, ValueError):
            return None
        # ≥ 5 면 이미 percentage (CV stress 5 fraction은 불가능하므로 안전)
        return v if v >= 5 else v * 100

    if key == '__electronic_active_pct':
        f = metrics.get('electronic_active_fraction')
        if f is None:
            return None
        try:
            return float(f) * 100
        except (TypeError, ValueError):
            return None

    if key == '__am_percolation_pct':
        # Prefer the flat key, else convert from electronic_percolating_fraction
        v = metrics.get('am_percolation_pct')
        if v is not None:
            try: return float(v)
            except (TypeError, ValueError): pass
        f = metrics.get('electronic_percolating_fraction')
        if f is not None:
            try: return float(f) * 100
            except (TypeError, ValueError): return None
        return None

    if key == '__vulnerable_pct':
        # Use REAL metric first: am_vulnerable_pct (from dem_analysis_core).
        # Falls back to dedicated alternatives, then to (100 − ionic_active)
        # as last resort.
        for k in ('am_vulnerable_pct', 'ionic_vulnerable_pct',
                  'vulnerable_am_pct'):
            v = metrics.get(k)
            if v is not None:
                try: return float(v)
                except (TypeError, ValueError): pass
        act = metrics.get('ionic_active_pct')
        if act is not None:
            try: return max(0.0, 100.0 - float(act))
            except (TypeError, ValueError): return None
        return None

    # τ_Laplace,eff (COMSOL/EIS input) — same formula as webapp/app.py:2026
    #   τ_Lap_eff = √(φ_SE × σ_grain / σ_full)
    if key == '__tau_lap_eff':
        phi_se = metrics.get('phi_se')
        sig_full = _sigma_ionic_effective(metrics)
        try:
            if phi_se and sig_full and sig_full > 0:
                return (float(phi_se) * 3.0 / float(sig_full)) ** 0.5
        except (TypeError, ValueError):
            return None
        return None

    if key == '__tau_lap_bulk':
        phi_se = metrics.get('phi_se')
        sig_bulk = metrics.get('sigma_bulk_net_mScm')
        try:
            if phi_se and sig_bulk and sig_bulk > 0:
                return (float(phi_se) * 3.0 / float(sig_bulk)) ** 0.5
        except (TypeError, ValueError):
            return None
        return None

    if key == '__constriction_overhead':
        # τ_eff / τ_bulk — both Laplacian derivations from φ_SE + σ.
        num = _derived_value('__tau_lap_eff', metrics)
        den = _derived_value('__tau_lap_bulk', metrics)
        if num and den and den > 0:
            return num / den
        return None

    if key == '__constriction_R_fraction_pct':
        for k in ('bulk_resistance_fraction_physics',
                  'bulk_resistance_fraction'):
            v = metrics.get(k)
            if v is not None:
                try:
                    bf = float(v)
                    # bulk_resistance_fraction stored 0-1
                    return (1.0 - bf) * 100 if bf <= 1.0 else max(0, 100 - bf)
                except (TypeError, ValueError):
                    continue
        return None

    if key == '__asr_ionic_Ohm_cm2':
        L = metrics.get('thickness_um')
        s = _sigma_ionic_effective(metrics)
        if L and s and s > 0:
            return float(L) * 0.1 / float(s)
        return None

    if key == '__asr_electronic_Ohm_cm2':
        L = metrics.get('thickness_um')
        s = _sigma_e_effective(metrics)
        if L and s and s > 0:
            return float(L) * 0.1 / float(s)
        return None

    if key == '__asr_thermal_Kcm2_W':
        L = metrics.get('thickness_um')
        k = _kappa_effective(metrics)
        if L and k and k > 0:
            return float(L) * 0.1 / float(k)
        return None

    # ── Energy density (user data: NCM811 C ≈ 190 mAh/g real, ρ 4.8 g/cc;
    #                              LPSCl ρ 2.0 g/cc) ─────────────────────
    if key == '__wt_am_pct':
        for src in ('am_se_ratio', '_input_am_se_ratio'):
            amse = metrics.get(src)
            if isinstance(amse, str) and ':' in amse:
                try:
                    a, s = (float(x) for x in amse.replace(' ', '').split(':')[:2])
                    if a + s > 0:
                        return 100 * a / (a + s)
                except (ValueError, IndexError):
                    continue
        return None

    if key == '__Q_gravimetric_mAhg':
        wt_pct = _derived_value('__wt_am_pct', metrics)
        if wt_pct is None:
            return None
        return (wt_pct / 100.0) * 190   # NCM811 real C ~ 190 mAh/g

    if key == '__Q_volumetric_mAhcc':
        wt_pct = _derived_value('__wt_am_pct', metrics)
        if wt_pct is None:
            return None
        wt_am = wt_pct / 100.0
        rho_am, rho_se, C_am = 4.8, 2.0, 175   # 정본 밀도(additives.DENS) + STEP4 x-window 정합 C_am (감사 F4)
        # 복합 고체밀도 = 질량분율의 조화평균 (부피 가산 1/ρ=Σw_i/ρ_i).  산술평균(wt·ρ 합)은 wt%를
        # vol%로 오용 → 80:20서 4.24 vs 정답 3.75 = +13% 과대 (감사 F1 수정 2026-07-23).
        rho_comp = 1.0 / (wt_am / rho_am + (1 - wt_am) / rho_se)
        eps = metrics.get('porosity')
        try:
            eps_f = float(eps)
            solid = 1.0 - (eps_f / 100.0 if eps_f > 1 else eps_f)
            if not (0.5 < solid < 1.0): solid = 0.85
        except (TypeError, ValueError):
            solid = 0.85
        return rho_comp * wt_am * C_am * solid

    # ── ASR_total + C-rate proxy + Volume buffer ──────────────────────
    if key == '__ASR_total_Ohm_cm2':
        asr_i = _derived_value('__asr_ionic_Ohm_cm2', metrics)
        asr_e = _derived_value('__asr_electronic_Ohm_cm2', metrics)
        if asr_i is None and asr_e is None:
            return None
        return (asr_i or 0) + (asr_e or 0)

    if key == '__c_rate_capability':
        asr_t = _derived_value('__ASR_total_Ohm_cm2', metrics)
        if asr_t and asr_t > 0:
            return 1.0 / asr_t
        return None

    if key == '__volume_change_buffer':
        # NCM 부피 ~5% 변화 → porosity가 흡수 buffer.
        # Pass through porosity (already 0-100 %).
        eps = metrics.get('porosity')
        try:
            return float(eps) if eps is not None else None
        except (TypeError, ValueError):
            return None

    # ── Operating polarization ─────────────────────────────────────────
    if key == '__polarization_mV_at_C3':
        # i = 0.33 mA/cm² (C/3 rate for 1 mAh/cm² electrode loading)
        # η (V) = i (A/cm²) × ASR (Ω·cm²) — convert to mV
        asr_i = _derived_value('__asr_ionic_Ohm_cm2', metrics)
        asr_e = _derived_value('__asr_electronic_Ohm_cm2', metrics)
        if asr_i is None and asr_e is None:
            return None
        asr_total = (asr_i or 0) + (asr_e or 0)
        if asr_total <= 0:
            return None
        return 0.33e-3 * asr_total * 1000   # mV

    # ── Safety ─────────────────────────────────────────────────────────
    if key == '__am_am_short_risk_cn':
        # Pass-through: directly use am_am_cn (band-around-optimum already
        # handles this in _band_score, just expose the value).
        v = metrics.get('am_am_cn')
        try:
            return float(v) if v is not None else None
        except (TypeError, ValueError):
            return None

    # __stress_hotspot_pct 제거 — 근사 대신 stress_cv axis (기계적 안정성)으로 충분.

    # ── Cycling life ────────────────────────────────────────────────────
    if key == '__cycle_stable_AM_pct':
        sev_pct = _derived_value('__frac_severe_force_pct', metrics)
        ion_act = metrics.get('ionic_active_pct')
        el_act_f = metrics.get('electronic_active_fraction')
        try:
            sev = float(sev_pct) / 100 if sev_pct is not None else 0
            ion = float(ion_act) / 100 if ion_act is not None else None
            el  = float(el_act_f) if el_act_f is not None else None
        except (TypeError, ValueError):
            return None
        if ion is None or el is None:
            return None
        return (1 - sev) * ion * el * 100

    # ── Target capacity tier match (from case_id) ────────────────────
    if key == '__Q_target_match_pct':
        cid = metrics.get('_case_id') or ''
        # Extract capacity tier from case_id (1mAh / 6mAh / 8mAh)
        import re as _re
        m = _re.search(r'(\d+)mAh', cid)
        if not m:
            return None   # particulate / S / etc. — no target → N/A axis
        target = float(m.group(1))
        actual = _derived_value('__Q_areal_mAhcm2', metrics)
        if not actual or actual <= 0 or target <= 0:
            return None
        ratio = min(actual / target, target / actual)
        return 100 * ratio

    # ── Design parameters from input_params ──────────────────────────
    if key == '__r_SE_um':
        # _input_box_x came in as box * scale already.  r_SE in
        # metrics is stored sim-units; convert via scale.
        for kk in ('_input_r_SE_um', '_input_r_SE'):
            v = metrics.get(kk)
            if v is not None:
                try:
                    fv = float(v)
                    # If stored as sim units (< 0.01), convert (× scale=1000)
                    return fv * 1000 if fv < 0.01 else fv
                except (TypeError, ValueError):
                    continue
        return None

    if key == '__lambda_eff':
        r_se = _derived_value('__r_SE_um', metrics)
        if not r_se or r_se <= 0:
            return None
        # effective r_AM: prefer AM_P, else AM_S
        r_am = None
        for kk in ('_input_r_AM_P_um', '_input_r_AM_P'):
            v = metrics.get(kk)
            if v is not None:
                try:
                    fv = float(v)
                    r_am = fv * 1000 if fv < 0.01 else fv
                    break
                except (TypeError, ValueError):
                    continue
        if r_am is None:
            for kk in ('_input_r_AM_S_um', '_input_r_AM_S'):
                v = metrics.get(kk)
                if v is not None:
                    try:
                        fv = float(v)
                        r_am = fv * 1000 if fv < 0.01 else fv
                        break
                    except (TypeError, ValueError):
                        continue
        if not r_am or r_am <= 0:
            return None
        return r_am / r_se

    if key == '__stage_e_available':
        # 1.0 if Stage E σ_ionic is present, 0.5 otherwise
        return 1.0 if metrics.get('sigma_full_mScm_stage_e_physics') is not None else 0.5

    if key == '__commercial_composition':
        # Pass-through wt_am_pct; band scoring (75-90% sweet spot) handles rest
        return _derived_value('__wt_am_pct', metrics)

    if key == '__ps_ratio_band':
        # P:S ratio band (optimum 70% P = 7:3) — Lee 2025 bimodal optimum.
        # ★ monomodal cases는 P:S ratio가 무의미 → N/A (페널티 안 줌).
        #   monomodal로서 평가하게 함.  bimodal일 때만 P fraction 반환.
        if _composition_of(metrics) != 'bimodal':
            return None
        ps = metrics.get('ps_ratio') or metrics.get('_meta_ps_ratio')
        if isinstance(ps, str) and ':' in ps:
            try:
                a, b = (float(x) for x in ps.replace(' ', '').split(':')[:2])
                if a + b > 0:
                    return 100 * a / (a + b)   # P fraction in %
            except (ValueError, IndexError):
                pass
        return None

    if key == '__bimodal_design':
        # ★ bimodal일 때만 평가 (A 등급으로 packing efficiency 인정).
        #   monomodal은 N/A — "bimodal 아님" 페널티 대신 monomodal로서
        #   해당 axis 미적용.  bimodal 우위는 실제 packing 성능 (porosity,
        #   σ_ionic, energy density) axes에 이미 반영됨.
        comp = _composition_of(metrics)
        if comp == 'bimodal':
            return 1.0
        if comp in ('mono AM_P', 'mono AM_S'):
            return None   # N/A — judged on own performance metrics
        return None

    if key == '__compaction_efficiency':
        # Pass-through porosity; band scoring handles the rest
        eps = metrics.get('porosity')
        try:
            return float(eps) if eps is not None else None
        except (TypeError, ValueError):
            return None

    if key == '__sigma_e_fracture_loss_pct':
        # Use REAL metric first: electronic_sigma_loss_pct_stage_e (analyze_contacts.py).
        # Fall back to deriving from σ_e before/after Stage E.
        for k in ('electronic_sigma_loss_pct_stage_e',
                  'electronic_sigma_loss_pct_stagewise',
                  'electronic_sigma_loss_pct'):
            v = metrics.get(k)
            if v is not None:
                try: return float(v)
                except (TypeError, ValueError): pass
        new = metrics.get('electronic_sigma_full_mScm_stage_e_physics')
        old = metrics.get('electronic_sigma_full_mScm_physics')
        try:
            if new is None or old is None:
                return None
            new = float(new); old = float(old)
            if old <= 0:
                return None
            return max(0, 100 * (old - new) / old)
        except (TypeError, ValueError):
            return None

    if key == '__Q_areal_mAhcm2':
        # Areal capacity = T(μm) × ρ_composite × C_AM × wt_AM × (1 − ε) × 1e-4
        # Robust AM mass-fraction parsing:
        #   - metrics['am_se_ratio'] (preferred)
        #   - metrics['_input_am_se_ratio'] (injected from input_params)
        #   - default 0.80 (typical sulfide cathode)
        L = metrics.get('thickness_um')
        if not L:
            return None
        wt_am = 0.80
        for src in ('am_se_ratio', '_input_am_se_ratio'):
            amse = metrics.get(src)
            if isinstance(amse, str) and ':' in amse:
                try:
                    parts = amse.replace(' ', '').split(':')
                    a, s = float(parts[0]), float(parts[1])
                    if a + s > 0:
                        wt_am = a / (a + s)   # → 0.82 for "82:18" or "8:2"
                        break
                except (ValueError, IndexError):
                    continue
        # Guard against degenerate values
        if not (0.05 < wt_am < 0.99):
            wt_am = 0.80
        rho_am = 4.8    # g/cc, NMC bulk — 정본 additives.DENS (was 4.7; 감사 F4 통일)
        C_am   = 175    # mAh/g, NMC811 STEP4 x-window 정합 (Q_volumetric과 통일)
        # Solid (non-porous) fraction of the electrode by volume
        eps = metrics.get('porosity')
        try:
            eps_f = float(eps)
            # porosity stored as % (0-100); guard against fraction form
            if eps_f > 1.0:
                solid = 1.0 - eps_f / 100.0
            else:
                solid = 1.0 - eps_f
            if not (0.5 < solid < 1.0):
                solid = 0.85
        except (TypeError, ValueError):
            solid = 0.85
        # AM volume fraction in the solid = wt_am × ρ_composite / ρ_am
        rho_se = 2.0    # LPSCl bulk g/cc — 정본 additives.DENS (was 1.85; 감사 F4 통일)
        # 복합 고체밀도 = 조화평균 (질량분율 → 부피 가산; 산술평균은 +13% 과대, 감사 F1)
        rho_comp = 1.0 / (wt_am / rho_am + (1 - wt_am) / rho_se)
        am_vol_frac = wt_am * rho_comp / rho_am
        return float(L) * solid * am_vol_frac * rho_am * C_am * 1e-4

    if key == '__ASR_per_capacity':
        L = metrics.get('thickness_um')
        s = _sigma_ionic_effective(metrics)
        Q = _derived_value('__Q_areal_mAhcm2', metrics)
        if not (L and s and s > 0 and Q and Q > 0):
            return None
        asr = float(L) * 0.1 / float(s)
        return asr / Q

    if key == '__validation_pass_pct':
        vf = metrics.get('validation_flags') or {}
        if not vf:
            return None
        n_total = 0
        n_pass  = 0
        for _flag, info in vf.items():
            if isinstance(info, dict) and 'ok' in info:
                n_total += 1
                if info['ok']:
                    n_pass += 1
            elif isinstance(info, bool):
                n_total += 1
                if info:
                    n_pass += 1
        if n_total == 0:
            return None
        return 100.0 * n_pass / n_total

    return None


_SIGMA_E_KEYS = {
    'electronic_sigma_full_mScm_stage_e_physics',
    'electronic_sigma_full_mScm_physics',
    'electronic_sigma_full_mScm_stage_e',
    'electronic_sigma_full_mScm',
}


def _resolve_value(axis: dict, metrics: dict) -> float | None:
    """Look up axis value with optional fallback key.

    Honours a carbon override on any σ_e axis: when
    metrics['_sigma_e_override_mScm'] is set, σ_e axes return that
    value instead of the original Stage-E σ_e.  ASR_electronic is a
    derived metric that already uses the override-aware
    _sigma_e_effective() helper, so it follows automatically.
    """
    key = axis.get('key')
    if key and key.startswith('__'):
        return _derived_value(key, metrics)
    # σ_e override takes precedence on the electronic-σ axes
    if key in _SIGMA_E_KEYS and metrics.get('_sigma_e_override_mScm') is not None:
        try:
            v = float(metrics['_sigma_e_override_mScm'])
            return v if math.isfinite(v) else None
        except (TypeError, ValueError):
            pass
    val = metrics.get(key) if key else None
    if val is None:
        fb = axis.get('fallback_key')
        if fb:
            val = metrics.get(fb)
    try:
        v = float(val)
        return v if math.isfinite(v) else None
    except (TypeError, ValueError):
        return None


# Derived axes whose VALUE is already exposed elsewhere (viewer_aux-derived
# raw keys in the plot param pool) — skip to avoid duplicate parameters.
_AXIS_VALUE_SKIP = {'__cut_fraction', '__bn_below_frac', '__bn_median_norm'}


def map_input_params(ip: dict | None, meta: dict | None) -> dict:
    """Map raw input_params.json + meta.json into the _input_*/_meta_* keys
    that the design-info / composition grade axes read.  Shared by the plot
    parameter-comparison tool (and mirrors webapp _inject_input_params)."""
    inj: dict = {}
    ip = ip or {}
    meta = meta or {}
    ratio = ip.get('am_se_ratio') or ip.get('AM_SE_ratio')
    if ratio:
        inj['_input_am_se_ratio'] = str(ratio)
    bx = ip.get('box_x'); by = ip.get('box_y'); scale = ip.get('scale') or 1000
    try:
        if bx is not None and by is not None:
            inj['_input_box_x'] = float(bx) * float(scale)
            inj['_input_box_y'] = float(by) * float(scale)
    except (TypeError, ValueError):
        pass
    for k_src, k_dst in (('r_SE', '_input_r_SE_um'),
                          ('r_AM_P', '_input_r_AM_P_um'),
                          ('r_AM_S', '_input_r_AM_S_um')):
        v = ip.get(k_src) or ip.get(k_src + '_sim')
        try:
            if v is not None:
                inj[k_dst] = float(v) * float(scale)
        except (TypeError, ValueError):
            continue
    tp = ip.get('target_press_sim') or ip.get('target_pressure_MPa')
    try:
        if tp is not None:
            inj['_input_target_press_MPa'] = (float(tp) * 1000 if float(tp) < 10
                                              else float(tp))
    except (TypeError, ValueError):
        pass
    if meta.get('mode'):
        inj['_meta_mode'] = meta['mode']
    if meta.get('ps_ratio'):
        inj['_meta_ps_ratio'] = meta['ps_ratio']
    return inj


def axis_values(metrics: dict, se_aux: dict | None = None,
                derived_only: bool = True) -> dict:
    """Resolve each grade axis's VALUE (not score — no corpus needed) for one
    case.  Returns {axis_label: float}.  Used to expose the grade engine's
    computed metrics (Q_gravimetric, ASR_*, τ_Laplace, cycle-stable, 분극 η …)
    as plottable parameters.  derived_only=True returns only the '__'-derived
    axes (the values not already present as raw full_metrics/viewer_aux keys),
    skipping those already exposed in the plot pool."""
    m = {**metrics, '_aux_se_diag': se_aux} if se_aux else metrics
    out: dict = {}
    for ax in AXES:
        key = ax.get('key', '')
        if derived_only and not key.startswith('__'):
            continue
        if key in _AXIS_VALUE_SKIP:
            continue
        v = _resolve_value(ax, m)
        if v is not None:
            out[ax['label']] = v
    return out


def _grade_axis(axis: dict, metrics: dict,
                 corpus_rows: list[dict]) -> dict:
    """Return scored row for one axis: value, score, grade, basis text."""
    value = _resolve_value(axis, metrics)
    out = {
        'label':     axis['label'],
        'category':  axis['category'],
        'direction': axis.get('direction'),
        'formula':   axis.get('formula', ''),
        'meaning':   axis.get('meaning', ''),
        'weight':    axis.get('weight', 1.0),
        'value':     value,
        'score':     None,
        'grade':     '—',
        'basis':     'no data',
    }
    if value is None:
        return out

    direction = axis.get('direction')
    if direction == 'band':
        score = _band_score(value, axis['optimum'], axis['band_width'])
        out['basis'] = (f"optimum = {axis['optimum']}, band = ±{axis['band_width']}; "
                        f"|value − optimum| = {abs(value - axis['optimum']):.2f}")
    elif direction in ('higher', 'lower'):
        thresholds = axis['thresholds']
        score = _interp_score(value, thresholds, direction)
        out['basis'] = (f"thresholds (A→C) = {thresholds}  "
                        f"({'larger' if direction == 'higher' else 'smaller'} = better)")
    elif direction in ('higher_corpus', 'lower_corpus'):
        base_dir = 'higher' if direction == 'higher_corpus' else 'lower'
        filter_key = axis.get('corpus_filter_key')
        thresholds = _corpus_threshold_scores(
            corpus_rows, axis['corpus_key'], direction, filter_key)
        if thresholds is None:
            return out
        score = _interp_score(value, thresholds, base_dir)
        pctile = _corpus_percentile(corpus_rows, axis['corpus_key'], value, filter_key)
        if pctile:
            filt = f' (filter: {filter_key} > 0)' if filter_key else ''
            out['basis'] = (f"corpus n={pctile['n']}{filt}, percentile = {pctile['pct']} "
                            f"(corpus [min/med/max] = [{pctile['lo']:.4g}, "
                            f"{pctile['med']:.4g}, {pctile['hi']:.4g}])")
        else:
            out['basis'] = f"corpus thresholds: {[round(t, 4) for t in thresholds]}"
    else:
        return out

    out['score'] = round(score, 1)
    out['grade'] = score_to_grade(score)
    return out


# ── Unit-cell detection ─────────────────────────────────────────────────
def _rve_area_um2(metrics: dict) -> float | None:
    """Extract RVE cross-section area (μm²) from metrics or injected
    input_params.  Used downstream as a finite-size confidence indicator
    (smaller RVE → noisier σ_ionic / ASR estimates)."""
    for k in ('_input_box_x', 'box_x_um'):
        bx = metrics.get(k)
        by = metrics.get(k.replace('x', 'y'))
        try:
            if bx and by:
                return float(bx) * float(by)
        except (TypeError, ValueError):
            continue
    return None


def detect_unit_cell(metrics: dict, case_id: str | None = None) -> dict:
    """Decide if a case is a small periodic unit-cell test rather than a
    full ASSB cathode.  Such cases lack realistic top↔bottom percolation
    challenges and shouldn't be ranked against full cells without caveat.

    Naming reminders (corrected per user clarification + case_summary.csv
    ground truth — see docs/CASE_NAMING.md for full reference):
      - "1mAh_*"     → target areal capacity 1 mAh/cm² (thin, ~15-20 μm).
      - "6mAh_*"     → target 6 mAh/cm² (~110-120 μm).
      - "8mAh_*"     → target 8 mAh/cm² (~140-185 μm).
      - "particulate_*" → SE particle-size sweep series (AM_S only,
                          RVE 30×30 μm).  NOT unit cells — full cathodes
                          with ~90-160 μm thickness.
      - "*_real"     → RVE 50×50 μm (full-size).
      - "*_real40"   → RVE 40×40 μm (smaller, finite-size variant of same
                       physical input).  NOT high-pressure sintering.
      - "*_100"      → RVE 100×100 μm (large RVE for 1mAh).
      - "*_S1..S5"   → random-seed replicates (5 statistical samples).
      - "*_AMP"      → ps_ratio 10:0 (AM_P-only mono cathode).
      - "*_AMS"      → ps_ratio 0:10 (AM_S-only mono cathode).
      - "*_E05/_E15" → (tentative) porosity-target variation.

    True unit-cell signature requires BOTH (rare in this corpus):
      • thickness < 25 μm  AND
      • AM-AM percolation = 0  +  ionic_active = 100% (periodic UC behavior)

    Returns {'is_unit_cell': bool, 'reasons': [str, ...]}.
    """
    reasons = []
    strict_signals = 0

    L = metrics.get('thickness_um')
    try:
        if L is not None and float(L) < 25:
            reasons.append(f'thickness {float(L):.1f} μm < 25 μm — possible unit-cell')
            strict_signals += 1
    except (TypeError, ValueError):
        pass

    am_perc = metrics.get('am_percolation_pct')
    ion_act = metrics.get('ionic_active_pct')
    try:
        if (am_perc is not None and float(am_perc) == 0 and
            ion_act is not None and float(ion_act) >= 99):
            reasons.append('am_percolation=0 + ionic_active=100% — periodic UC signature')
            strict_signals += 1
    except (TypeError, ValueError):
        pass

    return {'is_unit_cell': strict_signals >= 2, 'reasons': reasons}


# ── Top-level entry point ───────────────────────────────────────────────
def build_overall_grade(metrics: dict,
                         corpus_csv: str | None = None,
                         se_aux: dict | None = None,
                         carbon_wt_pct: float | None = None,
                         case_id: str | None = None,
                         corpus_rows: list[dict] | None = None) -> dict:
    """Compute multi-axis grades for one case.

    Args:
        metrics:        full_metrics.json contents (dict).
        corpus_csv:     optional path to docs/data/se_diagnostics_82.csv.
                        When omitted, corpus-relative axes drop to '—'.
        se_aux:         optional viewer aux dict (n_percolating,
                        articulation_points etc.) — used by derived axes.
        carbon_wt_pct:  when >0, apply the What-if carbon-additive model
                        to override σ_e (and downstream ASR_e) before
                        grading.  Other axes are unaffected.
        corpus_rows:    optional pre-built corpus (list of dicts).  When
                        provided it is used directly instead of reading
                        corpus_csv — this is how the webapp passes a dynamic
                        corpus (static baseline ∪ all live cases) so
                        percentile-ranked axes reflect the growing dataset.
    """
    inject = {}
    if se_aux:
        inject['_aux_se_diag'] = se_aux
    if case_id:
        inject['_case_id'] = case_id   # needed by __Q_target_match_pct
    if carbon_wt_pct and carbon_wt_pct > 0:
        wi = whatif_carbon_additive(metrics, wt_pct=carbon_wt_pct)
        if wi.get('available') and wi.get('sigma_e_new') is not None:
            inject['_sigma_e_override_mScm'] = wi['sigma_e_new']
            inject['_carbon_wt_pct'] = carbon_wt_pct
    if inject:
        metrics = {**metrics, **inject}

    if corpus_rows is None:
        corpus_rows = _load_corpus(corpus_csv)
    axes_out = [_grade_axis(ax, metrics, corpus_rows) for ax in AXES]

    # Composite weighted average over axes with a score
    scored = [(a['score'], a['weight']) for a in axes_out
              if a['score'] is not None]
    if scored:
        w_sum = sum(w for _s, w in scored)
        weighted = sum(s * w for s, w in scored) / max(w_sum, 1e-9)
    else:
        weighted = 0.0

    # Category averages
    cats: dict[str, list[float]] = {}
    for a in axes_out:
        if a['score'] is not None:
            cats.setdefault(a['category'], []).append(a['score'])
    cat_scores = {c: round(_stat.mean(v), 1) for c, v in cats.items()}

    uc = detect_unit_cell(metrics, case_id)
    rve_area = _rve_area_um2(metrics)

    # Compute base_case identifier for grouping.  Two grouping strategies:
    #   1. RVE-only twin:  real_X  ↔ real40_X  → base = "<cap>_rveX_<config>"
    #   2. Seed group:     *_S1 .. *_S5         → base = "<everything before _SN>"
    # particulate_X / capacity_* / config_* stay distinct otherwise (they
    # represent different physical inputs, not statistical replicates).
    base_case = None
    if case_id:
        import re as _re
        b = case_id
        # Collapse RVE marker first: real40 → rveX, real → rveX
        b = _re.sub(r'_real40(?=_)', '_rveX', b)
        b = _re.sub(r'_real(?=_)',   '_rveX', b)
        # Then collapse seed suffix _S1..S9 (single digit)
        b = _re.sub(r'_S[1-9]$', '_seedX', b)
        base_case = b

    composite = {
        'score':          round(weighted, 1),
        'grade':          score_to_grade(weighted),
        'gpa':            round(grade_to_gpa(score_to_grade(weighted)), 2),
        'n_axes':         len(scored),
        'n_total':        len(AXES),
        'is_unit_cell':   uc['is_unit_cell'],
        'unit_cell_reasons': uc['reasons'],
        'rve_area_um2':   rve_area,
        'base_case':      base_case,
    }

    return {
        'axes':            axes_out,
        'composite':       composite,
        'category_scores': cat_scores,
    }


# ── What-if 도전재 1 wt% scenario ────────────────────────────────────────
def whatif_carbon_additive(metrics: dict, wt_pct: float = 1.0,
                            sigma_carbon_mScm: float = 1000.0) -> dict:
    """Estimate σ_e and ASR_electronic shift if `wt_pct` carbon black is
    added to the cathode.

    Model — minimal Bruggeman-style series-of-conductors:
        φ_carbon ≈ wt_pct / 100 × (ρ_avg / ρ_carbon)
        σ_e^new  ≈ σ_e^old + (φ_carbon)^t × σ_carbon
    where t ≈ 2.0 (3D conductivity scaling, Kirkpatrick 1973).
    Carbon black bulk σ ≈ 100–1000 S/cm = 10⁵–10⁶ mS/cm.  Use a conservative
    1000 mS/cm effective value (after percolation losses in the carbon
    sub-network).

    This is a back-of-the-envelope: full simulation requires placing a
    secondary phase in the DEM and re-solving.  Useful only as an
    indicative direction.
    """
    sigma_e_old = (metrics.get('electronic_sigma_full_mScm_stage_e_physics')
                   or metrics.get('electronic_sigma_full_mScm_physics')
                   or metrics.get('electronic_sigma_full_mScm_stage_e')
                   or metrics.get('electronic_sigma_full_mScm'))
    if sigma_e_old is None:
        return {'available': False,
                'reason': 'electronic σ not in metrics — Stage E first'}
    sigma_e_old = float(sigma_e_old)

    # Density estimates for typical NMC + LPSCl + carbon
    rho_avg    = 3.5    # g/cc — composite average
    rho_carbon = 2.0    # g/cc — carbon black
    phi_carbon = (wt_pct / 100.0) * (rho_avg / rho_carbon)

    # Bruggeman-style scaling, t=2 for 3D
    delta_sigma = (phi_carbon ** 2.0) * sigma_carbon_mScm
    sigma_e_new = sigma_e_old + delta_sigma

    # ASR delta
    L_um = metrics.get('thickness_um')
    asr_e_old = None; asr_e_new = None
    if L_um:
        # ASR (Ω·cm²) = L(μm) × 1e-4 (cm/μm) / (σ × 1e-3 (S/mS)) = 0.1 × L / σ
        asr_e_old = 0.1 * L_um / sigma_e_old if sigma_e_old > 0 else None
        asr_e_new = 0.1 * L_um / sigma_e_new if sigma_e_new > 0 else None

    return {
        'available':    True,
        'wt_pct':       wt_pct,
        'phi_carbon':   round(phi_carbon, 4),
        'sigma_e_old':  round(sigma_e_old, 4),
        'sigma_e_new':  round(sigma_e_new, 4),
        'sigma_ratio':  round(sigma_e_new / max(sigma_e_old, 1e-9), 2),
        'asr_e_old':    round(asr_e_old, 3) if asr_e_old else None,
        'asr_e_new':    round(asr_e_new, 3) if asr_e_new else None,
        'asr_e_ratio':  round(asr_e_new / asr_e_old, 2) if asr_e_old and asr_e_new else None,
        'note':         ('단순 percolation 모델 (φ^t × σ_carbon, t=2). '
                          '실제 cathode에 carbon black 1 wt%를 첨가했을 때 '
                          '문헌 보고된 σ_e 향상 10–100배에 부합. '
                          '이온/구조축에는 영향 없음 (전자전도 단축만 갱신).'),
    }


# ── Literature-anchored multi-additive what-if (VGCF / Super P / PTFE) ────────
# Densities (g/cm³) match scripts/additives.py DENS.
_ADD_RHO   = {'VGCF': 2.00, 'SuperP': 1.90, 'PTFE': 2.20}
_RHO_SOLID = 3.5            # composite (NMC+LPSCl) average, g/cc

# ── ALL magnitudes are literature anchors (LPSCl + NCM same-material-system
#    where possible).  Sources cited per term; see docs/post_porosity_roadmap.md §2
#    and the lit_*.md digests.  This is a CPU analytic estimate (no sim); a full
#    MPM-additive run is the GPU cross-check.
_PTFE_DPOR_PER_WT   = -6.4     # %p porosity per 1 wt% PTFE  (Hong 2026: 28.7→22.3 vol% @1wt%)
_PTFE_SION_PER_WT   = 0.74     # σ_ion × per 1 wt% PTFE       (Hong 2026: 0.087→0.064 mS/cm @1wt%)
_POR_FLOOR          = 3.0      # %  pore cannot fibrillate below ~ this
_CARB_PC_WT         = 4.0      # wt% carbon e-percolation threshold (Reisacher 2023, C65/LPSCl)
_SION_BLOCK_VGCF    = 0.05     # σ_ion reduction slope /wt, VGCF (mild — concentrated fibre)
_SION_BLOCK_SUPERP  = 0.09     # σ_ion reduction slope /wt, Super P (~1.8× VGCF; our voxel + Kim2025 SP lowest)
_SIGMA_C_MSCM       = 1000.0   # ⚠§F1 ANALYTIC what-if hook (NOT measured) — effective carbon σ after
                               #   percolation losses (mS/cm).  ~10× above Reisacher 5wt% (≈1e-1 S/cm=100 mS/cm);
                               #   drives d_sig_e in the PURE-ANALYTIC grade axis only, not the STEP3 solve.


def _sat(x):
    return max(0.0, min(1.0, x))


def whatif_additives(metrics: dict, vgcf_wt: float = 0.0, superp_wt: float = 0.0,
                     ptfe_wt: float = 0.0, mixing: str = 'ballmill') -> dict:
    """Literature-anchored with/without estimate of σ_e, σ_ion and porosity when
    VGCF / Super P / PTFE are added, at a given mixing protocol.  PURE ANALYTIC
    (no sim) — a full MPM-additive run on the GPU is the cross-check.

    Anchored DIRECTIONS (each validated against LPSCl-ASSB literature):
      • PTFE  → porosity ↓ (−6.4 %p/wt, Hong 2026 fibrillar void-fill) AND
                σ_ion ↓ (×0.74/wt, binder occupation; confined ≫ NBR wet ×0.48).
      • carbon (VGCF/Super P), BULK (mixing=ballmill/handmix) → σ_e ↑ with a
                percolation gate at p_c≈4 wt% (Reisacher 2023); Super P ≥ VGCF per-wt
                at low loading (our voxel "density beats reach"); σ_ion ↓, Super P
                blocking ~1.8× VGCF (our voxel; Kim2025 σ_ion Super P lowest).
      • Super P, COATING (mixing=thinky dry-coat) → σ_e COLLAPSE up to ~3 decades
                (Kim2025: SE–SP@CAM 1.0e-5 vs SE@CAM 3.3e-2) — Super P-rich SE coating
                blocks CAM–CAM.  VGCF stays high (embedded, σ_e ≈ no-CA, Kim2025 1.4e-2).
                ⇒ the carbon-density sign FLIPS with position (bulk boost ↔ coating block).
    """
    # VGCF and Super P are both conductive carbon → mutually exclusive (use one OR the
    # other). Valid combos: VGCF / Super P / PTFE / VGCF+PTFE / Super P+PTFE.
    if vgcf_wt > 0 and superp_wt > 0:
        return {'available': False,
                'reason': 'VGCF와 Super P는 함께 사용 불가 — 도전재는 하나만 (유효 조합: '
                          'VGCF · Super P · PTFE · VGCF+PTFE · Super P+PTFE)'}
    sig_e = (metrics.get('electronic_sigma_full_mScm_stage_e_physics')
             or metrics.get('electronic_sigma_full_mScm_physics')
             or metrics.get('electronic_sigma_full_mScm_stage_e')
             or metrics.get('electronic_sigma_full_mScm'))
    sig_i = (metrics.get('ionic_sigma_full_mScm_stage_e_physics')
             or metrics.get('ionic_sigma_full_mScm_physics')
             or metrics.get('ionic_sigma_full_mScm_stage_e')
             or metrics.get('ionic_sigma_full_mScm'))
    por = metrics.get('porosity_pct', metrics.get('porosity'))
    if sig_e is None:
        return {'available': False, 'reason': 'electronic σ not in metrics — Stage E first'}
    sig_e = float(sig_e)
    sig_i = float(sig_i) if sig_i is not None else None
    por = float(por) * (100.0 if (por is not None and por <= 1.0) else 1.0) if por is not None else None

    carbon_wt = max(0.0, vgcf_wt) + max(0.0, superp_wt)
    # per-additive PROCESS regime from the (additive × mixing) matrix (additives.py) —
    # single source of truth shared with the MPM seeding. 'coat_block' (Super P dry-coat)
    # → σ_e collapse; 'coat_embed' (VGCF dry-coat) → σ_e ~recovers (A4 magnitude TBD,
    # today = bulk); 'bulk' → boost.
    try:
        import sys as _sys, os as _os
        _sd = _os.path.dirname(__file__)
        if _sd not in _sys.path:
            _sys.path.insert(0, _sd)
        from additives import additive_regime
    except Exception:
        additive_regime = lambda name, m: ('coat_block' if (name == 'SuperP' and m == 'thinky') else 'bulk')
    reg_sp = additive_regime('SuperP', mixing)
    reg_vgcf = additive_regime('VGCF', mixing)
    flags, notes = {}, []

    # ── σ_e (electronic) ────────────────────────────────────────────────────
    # carbon vol fraction (of composite solid)
    phi_C = sum(max(0.0, w) / 100.0 * (_RHO_SOLID / _ADD_RHO[k])
                for k, w in (('VGCF', vgcf_wt), ('SuperP', superp_wt)))
    g_perc = _sat(carbon_wt / _CARB_PC_WT)               # soft percolation gate (Reisacher p_c≈4wt%)
    # VGCF is the more efficient backbone per-wt once load-bearing; Super P wins at low bulk loading.
    eff = 1.0 + 0.6 * (vgcf_wt - superp_wt) / max(carbon_wt, 1e-9) if carbon_wt > 0 else 1.0
    d_sig_e = (phi_C ** 2) * _SIGMA_C_MSCM * g_perc * max(eff, 0.2)
    sig_e_new = sig_e + d_sig_e
    if reg_sp == 'coat_block' and superp_wt > 0:         # ★ Super P-rich SE-coating → σ_e collapse
        block = 10.0 ** (-3.0 * _sat(superp_wt / 2.9))   # 2.9 wt% → 3 decades (Kim2025); scales w/ wt
        sig_e_new *= block
        flags['superp_coating_collapse'] = round(block, 4)
        notes.append(f'{mixing}(dry-coat)+Super P [coat_block] → σ_e ×{block:.3g} 붕괴 (Kim2025 SE–SP@CAM, '
                     'Super P-rich coating이 CAM–CAM 전기연결 차단). VGCF면 회복.')
    if reg_vgcf == 'coat_embed' and vgcf_wt > 0:         # VGCF dry-coat embeds in porous SE coat
        # ★ A4 HOOK: Kim2025 SE–VGCF@CAM → σ_e RECOVERS to ≈ no-CA (not a full bulk boost).
        # Structural slot present; the embed σ magnitude is TBD until the A4 GPU result —
        # today it leaves σ_e as the bulk estimate (no change), only flags the regime.
        flags['vgcf_coat_embed'] = True                  # A4: set σ_e ≈ baseline-recover here
    if ptfe_wt > 0:                                      # PTFE insulator: mild σ_e drag
        sig_e_new *= (1.0 - 0.03 * ptfe_wt)
    sig_e_new = max(sig_e_new, 0.0)

    # ── σ_ion (ionic) ───────────────────────────────────────────────────────
    sig_i_new = sig_i
    if sig_i is not None:
        f = (1.0 - _SION_BLOCK_VGCF * max(0.0, vgcf_wt)) \
            * (1.0 - _SION_BLOCK_SUPERP * max(0.0, superp_wt)) \
            * (_PTFE_SION_PER_WT ** max(0.0, ptfe_wt))   # Hong: ×0.74 per wt PTFE
        sig_i_new = max(sig_i * f, 0.0)

    # ── porosity ────────────────────────────────────────────────────────────
    por_new = por
    if por is not None:
        d_por = _PTFE_DPOR_PER_WT * max(0.0, ptfe_wt)    # Hong 2026 fibrillar void-fill
        por_new = max(por + d_por, _POR_FLOOR)
        if ptfe_wt > 0:
            notes.append(f'PTFE {ptfe_wt:g} wt% → porosity {d_por:+.1f}%p (Hong 2026 fibrillation '
                         f'void-fill); σ_ion은 binder 점유로 ×{_PTFE_SION_PER_WT ** ptfe_wt:.2f} '
                         '감소(densification 이득 상회).')
    if carbon_wt > 0:
        _rg = ((f'Super P={reg_sp}' if superp_wt > 0 else '') + (' ' if superp_wt > 0 and vgcf_wt > 0 else '')
               + (f'VGCF={reg_vgcf}' if vgcf_wt > 0 else ''))
        notes.append(f'carbon {carbon_wt:g} wt% (p_c≈4, mixing={mixing} → {_rg}): σ_e {("↑" if d_sig_e>0 else "·")}'
                     + (f', Super P가 σ_ion {1-_SION_BLOCK_SUPERP:.2f}/wt로 VGCF({1-_SION_BLOCK_VGCF:.2f}/wt)보다 더 막음'
                        if superp_wt > 0 else ''))

    def _r(a, b):
        return round(b / a, 3) if (a and a > 1e-12) else None
    return {
        'available': True,
        'inputs': {'vgcf_wt': vgcf_wt, 'superp_wt': superp_wt, 'ptfe_wt': ptfe_wt, 'mixing': mixing},
        'phi_carbon': round(phi_C, 4),
        'sigma_e_old':  round(sig_e, 5),   'sigma_e_new':  round(sig_e_new, 5),  'sigma_e_ratio':  _r(sig_e, sig_e_new),
        'sigma_ion_old': (round(sig_i, 5) if sig_i is not None else None),
        'sigma_ion_new': (round(sig_i_new, 5) if sig_i_new is not None else None),
        'sigma_ion_ratio': (_r(sig_i, sig_i_new) if sig_i is not None else None),
        'porosity_old': (round(por, 2) if por is not None else None),
        'porosity_new': (round(por_new, 2) if por_new is not None else None),
        'porosity_delta_pp': (round(por_new - por, 2) if por is not None else None),
        'flags': flags,
        'notes': notes,
        'anchors': 'Hong2026(PTFE void/σion) · Reisacher2023(p_c≈4wt%) · Kim2025(SuperP coating σ_e collapse, σion) · voxel(SuperP 1.8× block)',
    }


# ── CLI smoke test ──────────────────────────────────────────────────────
if __name__ == '__main__':
    import argparse, json
    ap = argparse.ArgumentParser()
    ap.add_argument('metrics_json', help='Path to a full_metrics.json')
    ap.add_argument('--corpus',
                    default='docs/data/se_diagnostics_82.csv')
    args = ap.parse_args()
    with open(args.metrics_json) as f:
        m = json.load(f)
    out = build_overall_grade(m, args.corpus)
    print(f"Composite: {out['composite']['grade']} "
          f"({out['composite']['score']}/100, "
          f"{out['composite']['n_axes']}/{out['composite']['n_total']} axes scored)")
    print()
    last_cat = None
    for ax in out['axes']:
        if ax['category'] != last_cat:
            print(f"── {ax['category']} ──")
            last_cat = ax['category']
        v = ax['value']
        vstr = '—' if v is None else (f'{v:.3g}')
        print(f"  {ax['label']:<40s}  {vstr:>10s}  "
              f"score={ax['score'] if ax['score'] is not None else '—':>5}  "
              f"grade={ax['grade']}")
    print()
    print('Category averages:')
    for c, s in out['category_scores'].items():
        print(f"  {c:<30s}  {s}")
