#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② — R 주 판정 시간 다시 어림 v2 (추정) · 2026-11-11 · 표준 라이브러리만 · 몇 초.

등록 스크립트 (리포 docs/reviews/rint2_rr_fix_evidence_20261023/q9_time_budget.py) 와 같은 꼴
(1 대 · 2 대 나눔 · 3 대 나눔 · 지금 사슬 · 넘침 하나) 에 입력만 바꾼다:
  옛 입력 = 옛 세대 팔 시간 (SBE 879 s · DBE 2,578 s) × 합성 침대 반복 비 (×6.05 – ×7.37)
  새 입력 = ⑥ 숫자 탐침 시도 2 의 실측 (SBE 팔 한 점) + 손잡이 (가정) — 아래 KNOBS.

입력의 지위:
  [실측]   SBE · arm 0 · R_j 1e6 Ω · P0 · c 0 · rtol 1e-12 · kgy RTX 3090 (다른 프로세스와 GPU 같이 씀) 한 점
  [관찰]   같은 묶음 samples.tsv 의 gpu_util · gpu_used 전이로 가른 주 풀이 / 이어 풀기 / CPU 구간 (10 s 해상도)
  [가정]   s (GPU 혼자 쓸 때 풀이 배수) · r (DBE / SBE) · m (다른 점의 반복 수 배수) · 원장 재사용 · 기계 속도 같음 ·
           사다리 점 수 12 · 지문 시간 (REPORT_B2 추정) · 넘침 없음
  [미확인] DBE 의 준비 · 반복 수 전부 · 다른 R_j · 법칙 · c · origin 의 반복 수 · gabia 속도 · 원장 재사용의 읽기 시간

꼴 둘:
  F0 = 등록 스크립트 꼴 그대로 (SBE 38 팔 · DBE 12 단위 × 4–5 "팔" · 팔마다 준비 + 풀이 하나)
  F1 = 사슬 코드대로 센 꼴 (참고): 단위 = 팔 프로세스 3 + 봉인 원천 (조립만) 런 1 · 차가운 풀이 4–5 (SV 반사실 풀이는
       모서리 팔 프로세스 안 = 준비를 다시 하지 않는다) · 단위 뒤 = 합치기 · 판정 · 다시 판정이 봉인 원천을 각각 12 번 다시 돈다 (GPU 없음)
모든 출력 = 추정.  새 기준 · 합격선 없음.
"""
import json
import math
import sys
from datetime import datetime, timedelta

# ───────────────────────── [실측] ⑥ 시도 2 (리포 docs/data/rint2_probe6_a2_20261111/probe6_screen.txt) ─────────────────────────
MEAS = {
    'wall_s': 22345, 'pre_step3_s': 100, 'raster_prep_s': 4467, 'cjunc_prep_s': 4040, 'face_alpha_prep_s': 31,
    'cg_cert_s': 17748, 'save_end_s': 30, 'iters_main': 277885, 'iters_resolve': 84485, 'n_dof': 26529223,
    'maxiter_cap': 1500000, 'rss_max_kb': 34491680, 'point': 'SBE · arm 0 · R_j 1e6 Ω · P0 · c 0 · rtol 1e-12 · kgy (GPU 경합)',
}
# 시도 1 (리포 docs/data/rint2_probe6_a1_20261111/) — 반복–잔차 두 점용
MEAS_A1 = {'iters_main': 30000, 'resid': 4.81885e-07, 'cg_cert_s': 3049, 'raster_prep_s': 4487, 'cjunc_prep_s': 4038, 'wall_s': 7667}
MEAS_A2_RESID = 1.0519e-12
# ───────────────────────── [관찰] samples.tsv 전이 (10 s 표본) ─────────────────────────
#   gpu_util >= 97 % 연속 구간: 4567–17807 s (주 풀이) · 17847–21932 s (이어 풀기) · 사이 3 표본 (85–87 %) · 끝 21942– (84.9 %)
OBS = {'gpu_main_s': 13245, 'gap_cpu_s': 30, 'gpu_resolve_s': 4095, 'post_cpu_s': 378}
assert OBS['gpu_main_s'] + OBS['gap_cpu_s'] + OBS['gpu_resolve_s'] + OBS['post_cpu_s'] == MEAS['cg_cert_s']
assert MEAS['pre_step3_s'] + MEAS['raster_prep_s'] + MEAS['cg_cert_s'] + MEAS['save_end_s'] == MEAS['wall_s']

# ───────────────────────── 등록 값 (옛 표 · 리포 q9_time_budget.py 그대로) ─────────────────────────
REG_S, REG_D = 879.0, 2578.0
REG_F = 704.0 / 879.0
REG_R = {'lo': 6.05, 'hi': 7.37}
REG_M = {k: (1.0 - REG_F) + REG_F * r for k, r in REG_R.items()}
LADDER_PER_LAW = 12 + 4 + 2          # 사다리 12 · 끝 origin 4 · SBE origin 2 (법칙마다) — 등록 스크립트 그대로
NOOP = 2                              # SBE no-op (법칙마다 1 · 사다리 단계 끝)
UNITS = 12                            # (c, 법칙, R)
UNIT_DBE = {'lo': 4, 'hi': 5}         # 등록 스크립트: arm 0 · origin 2 · SV 아래 · (위끝)
REG_JSON = {'all3_one_machine_h': [220.2, 318.8], 'all3_no_split_h_2': [196.8, 290.5], 'all3_split_units_h_2': [110.1, 159.4],
            'all3_split_units_h_3': [81.2, 115.7], 'overflow_h': [86.7, 104.9]}     # 리포 q9_time_budget.json 의 값 (대조용)


def reg_hours(sec, k):
    return round(sec * REG_M[k] / 3600.0, 1)


def registered_table():
    def one(k):
        return reg_hours((2 * LADDER_PER_LAW + NOOP) * REG_S + UNITS * UNIT_DBE[k] * REG_D, k)

    def split(n, k):
        return reg_hours((LADDER_PER_LAW + NOOP // 2) * REG_S + math.ceil(UNITS / n) * UNIT_DBE[k] * REG_D, k)

    def no_split(k):
        return reg_hours((LADDER_PER_LAW + NOOP // 2) * REG_S + UNITS * UNIT_DBE[k] * REG_D, k)
    out = {'all3_one_machine_h': [one('lo'), one('hi')], 'all3_no_split_h_2': [no_split('lo'), no_split('hi')],
           'all3_split_units_h_2': [split(2, 'lo'), split(2, 'hi')], 'all3_split_units_h_3': [split(3, 'lo'), split(3, 'hi')],
           'overflow_h': [reg_hours(24 * REG_D, 'lo'), reg_hours(24 * REG_D, 'hi')]}
    assert out == REG_JSON, (out, REG_JSON)      # 같은 꼴임을 확인 (리포 JSON 값과 같다)
    return out


# ───────────────────────── 새 입력에서 만든 성분 (SBE 한 점 · 초) ─────────────────────────
PRE = MEAS['pre_step3_s']                                    # 런 전 (러너 관문 + payload 시작)
OTHER_PREP = MEAS['raster_prep_s'] - MEAS['cjunc_prep_s']    # 래스터 · face_alpha 31 s · 조립 (탄소 접합 준비 뺀 나머지) = 427
CJ = MEAS['cjunc_prep_s']                                    # 탄소 접합 준비 (원장 + 계획) = 4,040
GPU = OBS['gpu_main_s'] + OBS['gpu_resolve_s']               # GPU 에 묶인 시간 (주 풀이 + 이어 풀기) = 17,340  [관찰로 가름]
CERT_CPU = OBS['gap_cpu_s'] + OBS['post_cpu_s']              # 풀이 사이 · 뒤 CPU (증서 ⓓ 등) = 408            [관찰로 가름]
SAVE = MEAS['save_end_s']
FIXED = PRE + OTHER_PREP + SAVE                              # 팔 프로세스의 접합 준비 밖 CPU = 557
GFIX = PRE + OTHER_PREP                                      # 봉인 원천 (조립만) 런의 접합 준비 밖 CPU = 527
assert FIXED + CJ + GPU + CERT_CPU == MEAS['wall_s']

REG_RATIO = REG_D / REG_S                                    # 등록 비 DBE / SBE = 2,578 / 879 = 2.9329

# ───────────────────────── [가정] 손잡이 ─────────────────────────
KNOBS = {
    's': [1.0, 1.5, 2.0],                                    # (가) GPU 혼자 쓸 때 풀이 배수 (풀이 몫에만)
    'r': [0.5 * REG_RATIO, REG_RATIO, 2.0 * REG_RATIO],      # (나) DBE / SBE (등록 비의 0.5 · 1 · 2 배)
    'm': [0.5, 1.0, 2.0],                                    # (다) 다른 점의 반복 수 = 이 한 점의 0.5 · 1 · 2 배
    'reuse': [False, True],                                  # (라) 탄소 접합 준비 = 팔마다 / 침대 · origin 마다 한 번 (지금 코드 = 팔마다)
    'r_mode': ['arm', 'solve'],                              # DBE 비를 팔 전체에 (등록 꼴) / 풀이 몫에만 (준비 = SBE 와 같다고 가정)
}
FP_S = 240.0                 # 봉인 원천 런의 그래프 지문 시간 = 3 × 80 s (REPORT_B2 "지문 하나 ≈ 70–85 s · 추정 · SV 팔마다 2–3 개") — F1 만
N_SV_UNITS = 12              # sv_cf_scope = all3 (1저자 10-23 Q5 (가) · 계획 칸 = 봉인 때) → 모서리 팔 12 개 모두 SV 반사실
REUSE_ORIGINS = 3            # 원장이 달라지는 origin 수 (arm 0 · 1 · 2) — 넘침 (origin8) 은 5 개 더
REUSE_LOAD_S = 0.0           # 저장한 원장을 읽는 시간 = 미확인 (0 으로 둠)


def comp(s=1.0, r=REG_RATIO, m=1.0, reuse=False, r_mode='arm'):
    """성분 (초): SBE 팔 · DBE 팔 (차가운 풀이 하나) · 차가운 풀이 하나 · 준비 하나 · 봉인 원천 런 · 한 번만 드는 원장."""
    r_p, r_s = (r, r) if r_mode == 'arm' else (1.0, r)
    cj = 0.0 if reuse else CJ
    cold_s = GPU * m / s + CERT_CPU                     # SBE 차가운 풀이 하나 (+ 이어 풀기 + 증서 CPU)
    cold_d = r_s * cold_s
    prep_s = FIXED + cj + (REUSE_LOAD_S if reuse else 0.0)
    prep_d = r_p * prep_s
    return {'arm_s': prep_s + cold_s, 'arm_d': prep_d + cold_d, 'cold_s': cold_s, 'cold_d': cold_d, 'prep_s': prep_s, 'prep_d': prep_d,
            'g_d': r_p * (GFIX + cj) + FP_S,            # 봉인 원천 (조립만) 런 하나 (DBE)
            'once_s': (REUSE_ORIGINS * CJ) if reuse else 0.0,            # 재사용이면 기계마다 origin 3 개의 원장을 한 번씩
            'once_d': (REUSE_ORIGINS * CJ * r_p) if reuse else 0.0, 'r_p': r_p, 'r_s': r_s}


def h(sec):
    return round(sec / 3600.0, 1)


def f0(**kw):
    """등록 스크립트 꼴 그대로 — 입력만 바꿈 (팔 = 준비 + 풀이 하나 · DBE 단위 = 4–5 팔)."""
    c = comp(**kw)
    S, D = c['arm_s'], c['arm_d']
    lad1 = (LADDER_PER_LAW + NOOP // 2) * S + c['once_s']               # 한 기계의 사다리 한 법칙 (19 팔)
    out = {}
    for k in ('lo', 'hi'):
        dbe_all = UNITS * UNIT_DBE[k] * D
        out[k] = {
            'one_machine_h': h(2 * lad1 - c['once_s'] + dbe_all + c['once_d']),
            'no_split_2_h': h(lad1 + dbe_all + c['once_d']),            # 지금 사슬: 사다리 둘은 두 기계 · 예측은 한 기계
            'split_2_h': h(lad1 + math.ceil(UNITS / 2) * UNIT_DBE[k] * D + c['once_d']),
            'split_3_h': h(lad1 + math.ceil(UNITS / 3) * UNIT_DBE[k] * D + c['once_d']),
        }
    out['overflow_one_corner_h'] = h(24 * D)                           # 모서리 하나 origin 넘침 = +24 DBE 팔 (한 기계)
    out['arm_sbe_h'], out['arm_dbe_h'] = h(S), h(D)
    out['ladder_one_law_h'] = h(lad1)
    return out


def f1(**kw):
    """사슬 코드대로 센 꼴 (참고) — 단위 = 모서리 팔 (차가운 풀이 2 + 위끝 0–1) + 봉인 원천 런 1 + origin 팔 2 ·
    단위 뒤 (GPU 없음) = 합치기 12 + 판정 12 + 다시 판정 12 번의 봉인 원천 런 (한 기계 예측 꼴 = 판정 12 + 다시 판정 12)."""
    c = comp(**kw)
    lad1 = (LADDER_PER_LAW + NOOP // 2) * c['arm_s'] + c['once_s']
    out = {}
    for k, u in (('lo', 0), ('hi', 1)):
        unit = (c['prep_d'] + (2 + u) * c['cold_d']) + c['g_d'] + 2 * c['arm_d']
        post3 = 3 * N_SV_UNITS * c['g_d']                 # 단위 경로: 합치기 · 판정 · 다시 판정
        post2 = 2 * N_SV_UNITS * c['g_d']                 # 한 기계 예측 경로: 판정 · 다시 판정
        out[k] = {
            'unit_h': h(unit),
            'one_machine': {'sim_h': h(2 * lad1 - c['once_s'] + UNITS * unit + c['once_d']), 'post_h': h(post2)},
            'no_split_2': {'sim_h': h(lad1 + UNITS * unit + c['once_d']), 'post_h': h(post2)},
            'split_2': {'sim_h': h(lad1 + math.ceil(UNITS / 2) * unit + c['once_d']), 'post_h': h(post3)},
            'split_3': {'sim_h': h(lad1 + math.ceil(UNITS / 3) * unit + c['once_d']), 'post_h': h(post3)},
        }
    #  넘침: 모서리 하나 = 점 3 (R 셋) × 8 팔 · 두 기계에 점을 나누면 가장 많이 받은 기계 = 점 2 = 16 팔 · 끝 합치기가 봉인 원천 12 번 더
    out['overflow_one_corner'] = {'one_machine_h': h(24 * c['arm_d']), 'two_machines_h': h(16 * c['arm_d']),
                                  'second_merge_h': h(N_SV_UNITS * c['g_d'])}
    out['ladder_one_law_h'] = h(lad1)
    out['graph_only_run_h'] = h(c['g_d'])
    return out


def decomposition():
    """왜 오래 걸리나 — SBE 팔 한 점의 칸별 몫 [실측 · 관찰] 과 두 대 나눔 기준 줄 (s 1 · r 등록 비 · m 1 · 팔마다 준비 · 아래 끝) 의 몫."""
    w = float(MEAS['wall_s'])
    arm = [('런 전 (러너 관문 · payload 시작)', PRE, '실측'), ('래스터 · face_alpha · 조립', OTHER_PREP, '실측'),
           ('탄소 접합 준비 (원장 + 계획)', CJ, '실측'), ('주 풀이 (GPU CG · 277,885 반복)', OBS['gpu_main_s'], '관찰'),
           ('ⓒ 이어 풀기 (GPU CG · 84,485 반복)', OBS['gpu_resolve_s'], '관찰'),
           ('증서 CPU (풀이 사이 30 s + 뒤 378 s · ⓓ 등)', CERT_CPU, '관찰'), ('저장 · 끝', SAVE, '실측')]
    rows = [{'part': n, 'seconds': v, 'pct': round(100.0 * v / w, 1), 'standing': st} for n, v, st in arm]
    c = comp()
    lad = (LADDER_PER_LAW + NOOP // 2) * c['arm_s']
    dbe = math.ceil(UNITS / 2) * UNIT_DBE['lo'] * c['arm_d']
    tot = lad + dbe
    return {'sbe_arm_one_point': rows,
            'split_2_baseline': {'total_h': h(tot), 'ladder_19_sbe_arms_h': h(lad), 'ladder_pct': round(100 * lad / tot, 1),
                                 'dbe_24_arm_equiv_h': h(dbe), 'dbe_pct': round(100 * dbe / tot, 1),
                                 'note': 'DBE 몫 = 가정 (등록 비 2.933 × SBE 실측 팔) · DBE 는 재지 않았다'},
            'per_iter_s': {'whole_cg_cert_upper': round(MEAS['cg_cert_s'] / (MEAS['iters_main'] + MEAS['iters_resolve']), 5),
                           'main_gpu_obs': round(OBS['gpu_main_s'] / MEAS['iters_main'], 5),
                           'resolve_gpu_obs': round(OBS['gpu_resolve_s'] / MEAS['iters_resolve'], 5)},
            'iters_per_decade_obs': {
                'after_30000_to_1e-12': round((MEAS['iters_main'] - MEAS_A1['iters_main'])
                                              / math.log10(MEAS_A1['resid'] / MEAS_A2_RESID)),
                'resolve_1e-12_to_1e-14': round(MEAS['iters_resolve'] / math.log10(MEAS_A2_RESID / 1e-14)),
                'first_30000': round(MEAS_A1['iters_main'] / -math.log10(MEAS_A1['resid']))},
            'vs_registered_inputs': {'solve_s': [704, MEAS['cg_cert_s'], round(MEAS['cg_cert_s'] / 704.0, 1)],
                                     'non_solve_s': [175, MEAS['wall_s'] - MEAS['cg_cert_s'],
                                                     round((MEAS['wall_s'] - MEAS['cg_cert_s']) / 175.0, 1)],
                                     'arm_s': [879, MEAS['wall_s'], round(MEAS['wall_s'] / 879.0, 1)],
                                     'registered_arm_range_s': [round(879 * REG_M['lo']), round(879 * REG_M['hi'])],
                                     'measured_over_registered': [round(MEAS['wall_s'] / (879 * REG_M['hi']), 1),
                                                                  round(MEAS['wall_s'] / (879 * REG_M['lo']), 1)]}}


# ───────────────────────── 11-30 과 견주기 ─────────────────────────
DEADLINE = datetime(2026, 12, 1, 0, 0)       # 11-30 24:00 KST
REF_NOW = datetime(2026, 11, 12, 0, 0)       # 기준 시각 (시도 2 끝 = 11-11 19:45 KST 뒤의 자정)
HOURS_LEFT = (DEADLINE - REF_NOW).total_seconds() / 3600.0


def latest_start(hours):
    """그 시간이 걸리는 일을 11-30 24:00 KST 에 끝내려면 늦어도 언제 시작해야 하나 (기준 시각 전이면 '이미 지남')."""
    t = DEADLINE - timedelta(hours=hours)
    return t.strftime('%m-%d %H시') if t >= REF_NOW else f'이미 지남 (기준 {REF_NOW:%m-%d} 에 시작해도 {round(hours - HOURS_LEFT)} h 넘침)'


# ───────────────────────── 감도 (② · 표 밖 · 주 판정 뒤) ─────────────────────────
def sensitivity(**kw):
    """등록 §10-4 ② 감도 팔 수 그대로 (FIBRE · UNREG 각 74 = SBE 38 + DBE 36 · GRID 74 (dof ×1.728) · SVORDER 36 (DBE) · GRID 현 세대 대조 6)
    — 같은 팔 시간 가정 (GRID = 팔 시간 ×1.728 · 반복 수 같다고 가정) · 한 기계 합."""
    c = comp(**kw)
    S, D = c['arm_s'], c['arm_d']
    sec = 2 * (38 * S + 36 * D) + 1.728 * (38 * S + 36 * D) + 36 * D + 6 * 1.728 * D
    return {'arms': 264, 'one_machine_h': h(sec), 'two_machines_even_h': h(sec / 2.0)}


# ───────────────────────── C 의 재료 (정하지 않는다) ─────────────────────────
def stage_hours(**kw):
    """단계 (시간 상한이 걸리는 단위) 마다의 어림 — 사다리 한 법칙 (19 팔) · + R_j,0 origin 넘침 8 팔 · 단위 · 넘침 점 (8 팔) · 합치기 (봉인 원천 12) ·
    한 기계 예측 (단위 12 개를 한 단계로)."""
    c = comp(**kw)
    f = f1(**kw)
    lad = (LADDER_PER_LAW + NOOP // 2) * c['arm_s'] + c['once_s']
    return {'ladder_one_law_19_arms_h': h(lad), 'ladder_plus_origin8_h': h(lad + 8 * c['arm_s']),
            'unit_lo_hi_h': [f['lo']['unit_h'], f['hi']['unit_h']], 'point_origin8_8_arms_h': h(8 * c['arm_d']),
            'merge_12_graph_only_h': h(12 * c['g_d']),
            'predict_one_machine_lo_hi_h': [round(12 * f['lo']['unit_h'], 1), round(12 * f['hi']['unit_h'], 1)]}


def c_materials():
    spi = OBS['gpu_main_s'] / MEAS['iters_main']
    mx = [{'maxiter': v, 'x_main_iters': round(v / MEAS['iters_main'], 1),
           'one_solve_to_cap_h_at_measured_rate': h(v * spi), 'main_plus_resolve_to_cap_h': h(2 * v * spi)}
          for v in (560000, 1500000, 3000000)]
    stages = {'s1_r_registered': stage_hours(), 's2_r_registered': stage_hours(s=2.0),
              's1_r_x2': stage_hours(r=2.0 * REG_RATIO), 's1_r_x0.5': stage_hours(r=0.5 * REG_RATIO)}
    lad = stages['s1_r_registered']['ladder_one_law_19_arms_h']
    mh = [{'max_hours': v, 'x_ladder_stage_measured_rate': round(v / lad, 2),
           'x_point_origin8_r_registered': round(v / stages['s1_r_registered']['point_origin8_8_arms_h'], 2),
           'x_point_origin8_r_x2': round(v / stages['s1_r_x2']['point_origin8_8_arms_h'], 2)} for v in (150, 240, 360)]
    return {'maxiter_candidates': mx, 'stage_hours': stages, 'max_hours_candidates': mh,
            'this_point': {'main_iters': MEAS['iters_main'], 'pct_of_cap': round(100.0 * MEAS['iters_main'] / MEAS['maxiter_cap'], 1),
                           'resolve_iters': MEAS['iters_resolve'], 'per_iter_main_s_obs': round(spi, 5)}}


def counts():
    """프로세스 · 풀이 수 (사슬 코드대로 · all3 · 사다리 12 점 가정 · 넘침 없음)."""
    return {'sbe': {'arm_processes': 2 * LADDER_PER_LAW + NOOP, 'cold_solves': 2 * LADDER_PER_LAW + NOOP,
                    'resolve_solves': 2 * LADDER_PER_LAW + NOOP, 'runner_invocations': 2 * (12 + 2 + 1 + 1)},
            'dbe': {'arm_processes': 12 + 24, 'cold_solves_lo_hi': [12 + 12 + 24, 12 + 12 + 12 + 24],
                    'resolve_solves_lo_hi': [48, 60], 'graph_only_runs_unit_stage': N_SV_UNITS,
                    'graph_only_runs_merge_verdict_reverify': 3 * N_SV_UNITS},
            'registered_script': {'sbe_arms': 38, 'dbe_arm_equivalents_lo_hi': [48, 60]},
            'total_full_prep_processes': (2 * LADDER_PER_LAW + NOOP) + 36 + 4 * N_SV_UNITS,
            'total_cold_solves_lo_hi': [38 + 48, 38 + 60]}


def timeline(**kw):
    """두 대 나눔 (F1) 의 때 — 경과 h (추정): 사다리 첫 다섯 런 끝 · 사다리 끝 · 첫 단위의 모서리 팔 끝 · 단위 끝 (아래 · 위) · 판정까지."""
    c = comp(**kw)
    f = f1(**kw)
    lad = (LADDER_PER_LAW + NOOP // 2) * c['arm_s'] + c['once_s']
    first_corner = lad + c['once_d'] + c['prep_d'] + 2 * c['cold_d']
    return {'ladder_first_5_runs_h': h(5 * c['arm_s'] + c['once_s'] / 3.0), 'ladders_done_h': h(lad),
            'first_dbe_corner_arm_done_h': h(first_corner),
            'units_done_lo_hi_h': [f['lo']['split_2']['sim_h'], f['hi']['split_2']['sim_h']],
            'verdict_done_lo_hi_h': [round(f['lo']['split_2']['sim_h'] + f['lo']['split_2']['post_h'], 1),
                                     round(f['hi']['split_2']['sim_h'] + f['hi']['split_2']['post_h'], 1)]}


def main():
    reg = registered_table()
    grid = []
    for s in KNOBS['s']:
        for r in KNOBS['r']:
            for m in KNOBS['m']:
                for reuse in KNOBS['reuse']:
                    for r_mode in KNOBS['r_mode']:
                        kw = dict(s=s, r=r, m=m, reuse=reuse, r_mode=r_mode)
                        grid.append({'knobs': {'s': s, 'r': round(r, 4), 'm': m, 'reuse': reuse, 'r_mode': r_mode},
                                     'F0': f0(**kw), 'F1': f1(**kw)})
    base = dict(s=1.0, r=REG_RATIO, m=1.0, reuse=False, r_mode='arm')
    combos = [
        ('지금 그대로 — 한 대 (kgy · GPU 같이 씀 s 1) · 지금 사슬', 'F0.one_machine_h', dict(base)),
        ('결정된 것만 — 두 대 나눔 · GPU 혼자 s 1 (이득 없다고 볼 때)', 'F0.split_2_h', dict(base)),
        ('결정된 것만 — 두 대 나눔 · s 1.5', 'F0.split_2_h', dict(base, s=1.5)),
        ('결정된 것만 — 두 대 나눔 · s 2', 'F0.split_2_h', dict(base, s=2.0)),
        ('+ 코드 변경 없는 것 — 세 대 나눔 (v100 = 1저자 요청 때만) · s 1', 'F0.split_3_h', dict(base)),
        ('+ 코드 변경 없는 것 — 세 대 나눔 · s 2', 'F0.split_3_h', dict(base, s=2.0)),
        ('+ 봉인 전 코드 변경 (원장 재사용) — 두 대 나눔 · s 1', 'F0.split_2_h', dict(base, reuse=True)),
        ('+ 봉인 전 코드 변경 (원장 재사용) — 두 대 나눔 · s 2', 'F0.split_2_h', dict(base, s=2.0, reuse=True)),
        ('+ 봉인 전 코드 변경 (원장 재사용) — 세 대 나눔 · s 2', 'F0.split_3_h', dict(base, s=2.0, reuse=True)),
    ]
    combo_rows = []
    for name, key, kw in combos:
        row = {'name': name, 'knobs': {k: (round(v, 4) if isinstance(v, float) else v) for k, v in kw.items()}}
        for rname, rr in (('r_x0.5', 0.5 * REG_RATIO), ('r_x1', REG_RATIO), ('r_x2', 2.0 * REG_RATIO)):
            k2 = dict(kw, r=rr)
            v = f0(**k2)
            fld = key.split('.')[1]
            lo, hi = v['lo'][fld], v['hi'][fld]
            row[rname] = {'h': [lo, hi], 'days': [round(lo / 24.0, 1), round(hi / 24.0, 1)], 'latest_start_for_hi': latest_start(hi),
                          'latest_start_for_lo': latest_start(lo)}
        combo_rows.append(row)
    out = {
        'label': '추정 — 실측 한 점 (SBE) + 가정 (s · r · m · 재사용 · 기계 속도 같음 · 사다리 12 점 · 넘침 없음) · DBE 는 재지 않았다',
        'inputs': {'measured': MEAS, 'measured_attempt1': MEAS_A1, 'observed_split': OBS,
                   'components_s': {'PRE': PRE, 'OTHER_PREP': OTHER_PREP, 'CJ': CJ, 'GPU': GPU, 'CERT_CPU': CERT_CPU, 'SAVE': SAVE,
                                    'FIXED': FIXED, 'GFIX': GFIX},
                   'assumed_knobs': {k: [round(x, 4) if isinstance(x, float) else x for x in v] for k, v in KNOBS.items()},
                   'assumed_other': {'ladder_points_per_law': 12, 'sv_cf_scope': 'all3', 'graph_fp_s': FP_S,
                                     'reuse_origins': REUSE_ORIGINS, 'reuse_load_s': REUSE_LOAD_S, 'machines_equal_speed': True,
                                     'no_overflow': True, 'registered_ratio_D_over_S': round(REG_RATIO, 4)},
                   'unknown': ['DBE 준비 · 반복 수 (S0 단계 2 · 첫 DBE 모서리 팔 전까지)', '다른 R_j · 법칙 (P1) · c · origin 의 반복 수',
                               '바닥 · 천장 (극한) 런이 풀이를 도는지 (조기 반환이면 더 짧다)', 'gabia 의 준비 · 풀이 속도',
                               'kgy GPU 경합의 크기 (s)', '저장한 원장을 읽는 시간 (재사용 코드가 없다)',
                               'DBE 의 못 가른 덩어리 수 (위끝 풀이 0–12 — S0 단계 2 봉인 SV census 뒤)']},
        'registered_old_table_h': reg,
        'decomposition': decomposition(),
        'deadline': {'deadline_kst': '2026-11-30 24:00', 'reference_now_kst': '2026-11-12 00:00', 'hours_left': HOURS_LEFT,
                     'note': 'R 런은 봉인 전 남은 단계 뒤에 시작한다 (그 날 수는 여기 넣지 않았다)'},
        'combos_F0': combo_rows,
        'baseline_F0': f0(**base), 'baseline_F1': f1(**base), 'baseline_F1_solve_mode': f1(**dict(base, r_mode='solve')),
        'sensitivity_stage_outside_table': {'s1': sensitivity(**base), 's2': sensitivity(**dict(base, s=2.0)),
                                            'note': '주 판정 뒤에만 (등록 §10-4) · 같은 팔 시간 가정 · GRID 는 반복 수가 더 늘 수 있다 (미확인)'},
        'c_materials': c_materials(),
        'counts': counts(),
        'timeline_split_2_F1': {'s1_r_registered': timeline(**base), 's2_r_registered': timeline(**dict(base, s=2.0)),
                                's2_r_x0.5': timeline(**dict(base, s=2.0, r=0.5 * REG_RATIO)),
                                's2_r_registered_reuse': timeline(**dict(base, s=2.0, reuse=True))},
        'grid': grid,
    }
    if '--json' in sys.argv:
        json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
        sys.stdout.write('\n')
        return
    # ── 표 (사람이 읽는 꼴) ──
    p = print
    p('== 옛 표 (등록 값 · 리포 JSON 과 같음) ==')
    p(json.dumps(reg, ensure_ascii=False))
    d = out['decomposition']
    p('\n== SBE 팔 한 점의 칸별 몫 ==')
    for x in d['sbe_arm_one_point']:
        p(f"  {x['part']:<44} {x['seconds']:>7,} s  {x['pct']:>5} %  [{x['standing']}]")
    p(f"  반복당 (s): {d['per_iter_s']} · 자릿수당 반복 [관찰]: {d['iters_per_decade_obs']}")
    p(f"  옛 입력 대비: {d['vs_registered_inputs']}")
    p(f"  두 대 나눔 기준 줄: {d['split_2_baseline']}")
    p(f'\n== F0 (등록 꼴 · 입력만 바꿈) — 두 대 나눔 [h · 아래 끝–위 끝] · 남은 시간 {HOURS_LEFT:.0f} h (11-12 00:00 → 11-30 24:00 KST) ==')
    for mode in ('arm', 'solve'):
        for reuse in (False, True):
            p(f'  -- DBE 비 적용 = {mode} · 원장 재사용 = {reuse} · m = 1 --')
            p('     s \\ r      ' + '   '.join(f'r={r:.3f}' .ljust(22) for r in KNOBS['r']))
            for s in KNOBS['s']:
                cells = []
                for r in KNOBS['r']:
                    v = f0(s=s, r=r, m=1.0, reuse=reuse, r_mode=mode)
                    cells.append(f"{v['lo']['split_2_h']:>6.1f}–{v['hi']['split_2_h']:<6.1f} ({v['lo']['split_2_h'] / 24:.1f}–{v['hi']['split_2_h'] / 24:.1f} d)")
                p(f'     s={s:<4}     ' + '   '.join(cells))
    p('\n== F0 — m (반복 수 배수) 감도 · 두 대 나눔 · r 등록 비 · arm · 팔마다 준비 ==')
    for m in KNOBS['m']:
        p('   m=%-4s ' % m + '   '.join(f"s={s}: {f0(s=s, m=m)['lo']['split_2_h']:.1f}–{f0(s=s, m=m)['hi']['split_2_h']:.1f} h" for s in KNOBS['s']))
    p('\n== F0 — 꼴마다 (s 1 · r 등록 비 · m 1 · arm · 팔마다 준비) ==')
    p('  ' + json.dumps(out['baseline_F0'], ensure_ascii=False))
    p('\n== F1 (사슬 코드대로 · 참고) — 같은 기준 줄 (arm) · 그리고 DBE 비를 풀이에만 (solve) ==')
    p('  arm  : ' + json.dumps(out['baseline_F1'], ensure_ascii=False))
    p('  solve: ' + json.dumps(out['baseline_F1_solve_mode'], ensure_ascii=False))
    p('\n== 조합 (F0 · 아래 끝–위 끝 h · r = 등록 비의 0.5 / 1 / 2 배) ==')
    for row in combo_rows:
        p(f"  {row['name']}")
        for rn in ('r_x0.5', 'r_x1', 'r_x2'):
            x = row[rn]
            p(f"      {rn:<7} {x['h'][0]:>7.1f}–{x['h'][1]:<7.1f} h ({x['days'][0]}–{x['days'][1]} 일) · 늦어도 시작 (위 끝 기준): {x['latest_start_for_hi']}")
    p('\n== 감도 단계 (표 밖 · 주 판정 뒤) ==')
    p('  ' + json.dumps(out['sensitivity_stage_outside_table'], ensure_ascii=False))
    p('\n== C 재료 ==')
    p('  ' + json.dumps(out['c_materials'], ensure_ascii=False))
    p('\n== 수 (사슬 코드대로) ==')
    p('  ' + json.dumps(out['counts'], ensure_ascii=False))
    p('\n== 두 대 나눔의 때 (F1 · 경과 h) ==')
    p('  ' + json.dumps(out['timeline_split_2_F1'], ensure_ascii=False))


if __name__ == '__main__':
    main()
