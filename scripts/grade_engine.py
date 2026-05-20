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
     'meaning': '<95%면 dead-zone 존재 → 이론 σ_ionic도 절반 이하 떨어짐 (Bielefeld 2019, Liu&Yin 2025).',
     'weight': 1.4},

    {'category': 'SE 네트워크 위상',
     'key': '__cut_fraction', 'label': 'Cut fraction (위상 robustness)',
     'direction': 'lower_corpus', 'corpus_key': 'cut_fraction',
     'formula': 'cut_fraction = n_articulation / n_percolating_SE',
     'meaning': 'Cut node 1개 제거 시 percolation 분리되는 비율. 낮을수록 redundancy ↑. '
                'Corpus percentile 기준 평가.',
     'weight': 1.0},

    {'category': 'SE 네트워크 위상',
     'key': '__bn_below_frac', 'label': 'Bottleneck burden',
     'direction': 'lower_corpus', 'corpus_key': 'bn_below_frac',
     'formula': 'n_bn_below_threshold / n_perc_edges  (A/r² < 10% × median)',
     'meaning': '폭이 corpus median의 10% 미만인 좁은 contact 비율. '
                'σ_ionic constriction loss 직접 원인. Corpus percentile.',
     'weight': 1.0},

    {'category': 'SE 네트워크 위상',
     'key': 'se_bn_median_norm', 'label': '백본 두께 (median A/r²)',
     'direction': 'higher_corpus', 'corpus_key': 'bn_median_norm',
     'formula': 'median(A_contact / r_min²) over percolating SE-SE edges',
     'meaning': '대표 contact의 dimensionless 크기. Hertz 이상 ≈ 0.03, '
                '본 corpus median ≈ 0.28. 높을수록 백본 두꺼움.',
     'weight': 0.8},

    # ── 3. SE 네트워크 통계 (Statistics) ──
    {'category': 'SE 네트워크 통계',
     'key': 'se_se_cn', 'label': '⟨z_SE-SE⟩ (coordination)',
     'direction': 'higher', 'thresholds': [5.5, 5.0, 4.5, 4.0, 3.5, 3.0],
     'formula': 'mean coordination number of SE particles to other SE',
     'meaning': '4–6 = packed, <3 = sparse (Mukhopadhyay 2014). RCP ≈ 6.',
     'weight': 0.6},

    {'category': 'SE 네트워크 통계',
     'key': 'se_se_cn_std', 'label': 'σ(z_SE-SE) (균질도)',
     'direction': 'lower', 'thresholds': [1.5, 1.7, 2.0, 2.3, 2.7, 3.2],
     'formula': 'std dev of SE coordination — packing inhomogeneity',
     'meaning': '낮으면 균일 packing, 높으면 일부 SE 고립/일부 over-coordinated.',
     'weight': 0.4},

    # ── 4. 경로 효율 (Path efficiency) ──
    {'category': '경로 효율 (Tortuosity)',
     'key': 'tortuosity_lap_eff', 'label': 'τ_Laplace,eff ⭐',
     'direction': 'lower', 'thresholds': [1.8, 2.2, 2.8, 3.5, 4.5, 6.0],
     'fallback_key': 'tortuosity_recommended',
     'formula': 'Laplacian inv-network tortuosity (COMSOL/EIS input)',
     'meaning': 'Tippens 2019, Famprikis 2019. <2.5 우수, >5 endpoint dominated.',
     'weight': 1.0},

    {'category': '경로 효율 (Tortuosity)',
     'key': 'tortuosity_lap_bulk', 'label': 'τ_Laplace,bulk (구조)',
     'direction': 'lower', 'thresholds': [1.2, 1.4, 1.7, 2.0, 2.5, 3.0],
     'fallback_key': 'tortuosity_mean',
     'formula': 'Laplacian without constriction (pure geometric)',
     'meaning': 'Bruggeman 가정시 φ^−0.5 ≈ 1.85.',
     'weight': 0.5},

    {'category': '경로 효율 (Tortuosity)',
     'key': '__constriction_overhead',
     'label': 'Constriction overhead τ_eff/τ_geo',
     'direction': 'lower', 'thresholds': [1.5, 1.8, 2.2, 2.8, 3.5, 5.0],
     'formula': 'τ_Laplace,eff / τ_Laplace,bulk (또는 τ_Dij)',
     'meaning': '좁은 contact으로 인한 추가 저항 비율. 1배=geometric만.',
     'weight': 0.7},

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
     'formula': '100 − ionic_active_pct (low-coverage / dead-zone fallback)',
     'meaning': '연결은 됐지만 SE coverage가 낮아 cycling시 끊길 risk 높은 AM.',
     'weight': 0.6},

    # ── 7. 전자 전도 (Electronic) ──
    {'category': '전자 전도',
     'key': '__am_percolation_pct', 'label': 'AM percolation top↔bot (%)',
     'direction': 'higher', 'thresholds': [90, 80, 70, 55, 40, 25],
     'formula': '% of AM in the connected component spanning bottom→top',
     'meaning': 'AM-AM contact 망의 top↔bot 연결성. <70%면 도전재 필수.',
     'weight': 0.9},

    {'category': '전자 전도',
     'key': '__electronic_active_pct', 'label': 'CC-connected AM (%)',
     'direction': 'higher', 'thresholds': [90, 80, 70, 55, 40, 25],
     'formula': 'electronic_active_fraction × 100',
     'meaning': '하단 current collector까지 전자가 도달 가능한 AM 비율.',
     'weight': 0.9},

    {'category': '전자 전도',
     'key': 'electronic_sigma_full_mScm_stage_e_physics',
     'label': 'σ_e Stage E (mS/cm) ⭐',
     'direction': 'higher', 'thresholds': [5, 2, 1, 0.5, 0.2, 0.05],
     'fallback_key': 'electronic_sigma_full_mScm_physics',
     'formula': 'Stage E final electronic conductivity (Trevisanello AM-crystallinity × size)',
     'meaning': 'sulfide cathode 무도전재 σ_e 0.5–5 mS/cm 권장 (Janek review). '
                '도전재 1wt%로 향상 가능 — What-if 토글에서 가시화.',
     'weight': 0.7},

    # ── 8. 기계적 안정성 (Mechanical) ──
    {'category': '기계적 안정성',
     'key': '__frac_severe_force_pct', 'label': 'Fragmentation+Pulv (%)',
     'direction': 'lower', 'thresholds': [0.5, 1.5, 3, 6, 10, 18],
     'formula': '(frac_fragmentation + frac_pulverization) [force-based]',
     'meaning': 'Lawn 1998 force-ratio classifier로 본 심각 손상 비율 (cycling crack risk).',
     'weight': 0.9},

    {'category': '기계적 안정성',
     'key': 'frac_multicrack_force_pct', 'label': 'Multi-crack (%)',
     'direction': 'lower', 'thresholds': [3, 6, 10, 16, 25, 40],
     'fallback_key': 'frac_multicrack_pct',
     'formula': 'frac_multicrack_force_pct — Lawn stage 2',
     'meaning': 'Hertzian → ring crack → multi-crack 단계 도달 비율.',
     'weight': 0.6},

    {'category': '기계적 안정성',
     'key': 'fracture_index_force', 'label': 'Fracture index',
     'direction': 'lower', 'thresholds': [0.05, 0.10, 0.20, 0.35, 0.55, 0.80],
     'fallback_key': 'fracture_index',
     'formula': 'Σ stage_weight × frac_stage / 4 — composite damage index 0=intact, 1=all pulv',
     'meaning': 'Lawn weights (intact 0, micro 1, multi 2, frag 3, pulv 4) — 통합 손상 척도.',
     'weight': 0.7},

    {'category': '기계적 안정성',
     'key': '__sigma_vm_cv_pct', 'label': 'CV(σ_VM) (%)',
     'direction': 'lower', 'thresholds': [100, 130, 160, 200, 250, 320],
     'formula': '100 × stress_cv  (CV = σ(stress) / ⟨stress⟩)',
     'meaning': '응력 분포 불균일도. 높을수록 hotspot 다수 → 국부 fracture.',
     'weight': 0.4},

    # ── 9. 전도도 (Absolute conductivity) ──
    {'category': '전도도 절대값',
     'key': 'sigma_full_mScm_stage_e_physics',
     'label': 'σ_ionic Stage E (mS/cm) ⭐',
     'direction': 'higher', 'thresholds': [0.5, 0.3, 0.15, 0.08, 0.04, 0.01],
     'fallback_key': 'sigma_full_mScm_physics',
     'formula': 'Stage E final ionic conductivity (Cronau SE-size factor)',
     'meaning': '실측 sulfide composite 0.1–0.5 mS/cm (Janek 2023 review).',
     'weight': 1.8},

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

    # ── 10. 셀 ASR ──
    {'category': '셀 단위 ASR',
     'key': '__asr_ionic_Ohm_cm2', 'label': 'ASR_ionic (Ω·cm²) ⭐',
     'direction': 'lower', 'thresholds': [30, 60, 100, 160, 250, 400],
     'formula': 'ASR = L_cathode(μm) × 0.1 / σ_ionic(mS/cm)',
     'meaning': '1mAh/cm² C/3에서 ≤100 Ω·cm² workable. >250면 high-rate 위험.',
     'weight': 2.0},

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
     'meaning': '전자전도 영역 저항. 도전재 무첨가 sulfide에서 ASR_ionic만큼 critical.',
     'weight': 0.7},

    {'category': '셀 단위 ASR',
     'key': '__asr_thermal_Kcm2_W', 'label': 'ASR_thermal (K·cm²/W)',
     'direction': 'lower', 'thresholds': [1.5, 2.5, 4, 6, 9, 14],
     'formula': 'ASR_th = L_cathode × 0.1 / κ',
     'meaning': '냉각 효율. sulfide cell에서 1차 성능 결정 인자 아님.',
     'weight': 0.15},

    # ── 11. 가공 / 신뢰성 (Manufacturability) ──
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


def _corpus_percentile(rows: Iterable[dict], key: str,
                        value: float) -> dict | None:
    """Return {pct, n, lo, med, hi} — value's percentile rank in corpus[key]."""
    arr = []
    for r in rows:
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
                              direction: str) -> list[float] | None:
    """Derive 6 percentile cutoffs from corpus for corpus-relative axes.

    direction='lower_corpus'  → [p10, p25, p40, p55, p70, p85] (low percentile = high grade)
    direction='higher_corpus' → [p90, p75, p60, p45, p30, p15] (high percentile = high grade)
    """
    arr = []
    for r in rows:
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

    if key == '__frac_severe_force_pct':
        a = metrics.get('frac_fragmentation_force_pct') or 0
        b = metrics.get('frac_pulverization_force_pct') or 0
        if a == 0 and b == 0:
            a = metrics.get('frac_fragmentation_pct') or 0
            b = metrics.get('frac_pulverization_pct') or 0
        return a + b

    if key == '__sigma_vm_cv_pct':
        cv = metrics.get('stress_cv')
        if cv is None:
            return None
        try:
            cv = float(cv)
        except (TypeError, ValueError):
            return None
        # stress_cv stored as fraction (0-3.x) OR already as %; auto-detect
        return cv * 100 if cv < 10 else cv

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
        # If a dedicated metric exists use it; else fall back to (100 − active)
        for k in ('ionic_vulnerable_pct', 'vulnerable_am_pct'):
            v = metrics.get(k)
            if v is not None:
                try: return float(v)
                except (TypeError, ValueError): pass
        act = metrics.get('ionic_active_pct')
        if act is not None:
            try: return max(0.0, 100.0 - float(act))
            except (TypeError, ValueError): return None
        return None

    if key == '__constriction_overhead':
        # τ_eff / τ_geo  — use lap_eff when present, else fall back to tau_dij
        for ne, nd in (('tortuosity_lap_eff',     'tortuosity_lap_bulk'),
                        ('tortuosity_lap_eff',     'tortuosity_recommended'),
                        ('tortuosity_recommended', 'tortuosity_mean')):
            num = metrics.get(ne); den = metrics.get(nd)
            try:
                num = float(num) if num is not None else None
                den = float(den) if den is not None else None
            except (TypeError, ValueError):
                continue
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

    if key == '__Q_areal_mAhcm2':
        # Areal capacity = T(μm) × ρ_composite × C_AM × wt_AM × (1 − ε) × 1e-4
        # Use AM mass-fraction parsed from AM:SE input ratio when present
        # (form "82:18" means 82% AM by weight), else fall back to 0.80.
        L = metrics.get('thickness_um')
        if not L:
            return None
        wt_am = 0.80
        amse = metrics.get('am_se_ratio')
        if isinstance(amse, str) and ':' in amse:
            try:
                a, s = (float(x) for x in amse.split(':'))
                if a + s > 0:
                    wt_am = a / (a + s)   # → 0.82 for "82:18"
            except ValueError:
                pass
        rho_am = 4.7    # g/cc, NMC bulk
        C_am   = 175    # mAh/g, NMC811 @ 4.3V cutoff (representative)
        # Solid (non-porous) fraction of the electrode by volume
        eps = metrics.get('porosity')
        try:
            solid = 1.0 - float(eps) / 100.0
        except (TypeError, ValueError):
            solid = 0.85
        # AM volume fraction in the solid = wt_am × ρ_composite / ρ_am
        # Approximating ρ_composite ≈ wt_am × ρ_AM + (1-wt_am) × ρ_SE
        rho_se = 1.85   # LPSCl bulk g/cc
        rho_comp = wt_am * rho_am + (1 - wt_am) * rho_se
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
        thresholds = _corpus_threshold_scores(
            corpus_rows, axis['corpus_key'], direction)
        if thresholds is None:
            return out
        score = _interp_score(value, thresholds, base_dir)
        pctile = _corpus_percentile(corpus_rows, axis['corpus_key'], value)
        if pctile:
            out['basis'] = (f"corpus n={pctile['n']}, percentile = {pctile['pct']} "
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
def detect_unit_cell(metrics: dict, case_id: str | None = None) -> dict:
    """Decide if a case is a small periodic unit-cell test rather than a
    full ASSB cathode.  Such cases lack realistic top↔bottom percolation
    challenges and shouldn't be ranked against full cells without caveat.

    Returns {'is_unit_cell': bool, 'reasons': [str, ...]}.
    """
    reasons = []
    if case_id and 'particulate' in case_id.lower():
        reasons.append('case_id contains "particulate"')
    L = metrics.get('thickness_um')
    try:
        if L is not None and float(L) < 30:
            reasons.append(f'thickness {L} μm < 30 μm (unit-cell scale)')
    except (TypeError, ValueError):
        pass
    am_perc = metrics.get('am_percolation_pct')
    ion_act = metrics.get('ionic_active_pct')
    try:
        # Diagnostic geometry: no AM connectivity but 100% activity
        # (typical of periodic unit cell tests)
        if (am_perc is not None and float(am_perc) == 0 and
            ion_act is not None and float(ion_act) >= 99):
            reasons.append('am_percolation=0 + ionic_active=100% (periodic UC)')
    except (TypeError, ValueError):
        pass
    return {'is_unit_cell': bool(reasons), 'reasons': reasons}


# ── Top-level entry point ───────────────────────────────────────────────
def build_overall_grade(metrics: dict,
                         corpus_csv: str | None = None,
                         se_aux: dict | None = None,
                         carbon_wt_pct: float | None = None,
                         case_id: str | None = None) -> dict:
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
    """
    inject = {}
    if se_aux:
        inject['_aux_se_diag'] = se_aux
    if carbon_wt_pct and carbon_wt_pct > 0:
        wi = whatif_carbon_additive(metrics, wt_pct=carbon_wt_pct)
        if wi.get('available') and wi.get('sigma_e_new') is not None:
            inject['_sigma_e_override_mScm'] = wi['sigma_e_new']
            inject['_carbon_wt_pct'] = carbon_wt_pct
    if inject:
        metrics = {**metrics, **inject}

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

    composite = {
        'score':          round(weighted, 1),
        'grade':          score_to_grade(weighted),
        'gpa':            round(grade_to_gpa(score_to_grade(weighted)), 2),
        'n_axes':         len(scored),
        'n_total':        len(AXES),
        'is_unit_cell':   uc['is_unit_cell'],
        'unit_cell_reasons': uc['reasons'],
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
