#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② — R 주 판정 시간 다시 어림 v3 (추정) · 2026-11-17 · 표준 라이브러리만 · 몇 초 · 읽기 · 쓰기 없음 (화면 · --json).

2 판 (리포 docs/reviews/rint2_time_reestimate_20261111/time_budget_v2.py) 과 같은 꼴에 입력을 바꾼다:
  옛 입력 = ⑥ 시도 2 (옛 핀 5bca50c88 · 전처리 A 꼴 · 저장본 없음 · 팔마다 탄소 접합 준비 4,040 s)
  새 입력 = ⑥ 시도 3 · 4 (최종 핀 64e4d213e · 전처리 C 꼴 · 탄소 접합 원장 저장본) + 11-16 S0 저장본 시험 + 11-12 합성 벤치 (기계 비)
새로 넣은 꼴:
  (1) 저장본 = 열쇠에 기계 지문 · sid 격자 (origin) · 침대 입력 · 격자 · 문턱이 든다 (scripts/cjunc_store.py 13 · 583–589 줄) → 기계마다 · 침대마다 ·
      origin 마다 한 번 짓고 나머지 팔은 읽는다.  봉인 원천 (조립만) 런은 저장본을 읽지 않는다 (scripts/rint_r_chain.py 5901 줄 · 러너 594 줄) →
      준비 전체 그대로 (2 판 표의 '재사용이면 봉인 원천도 준다' 가정은 구현과 다르다).
  (2) 두 기계 속도가 다를 수 있다 (gabia GPU = 벤치 C 꼴 비 · CPU = 가정) → 단위 나눔을 정수로 골라 늦은 기계 끝을 줄인다 (배정은 봉인하지 않는다).
  (3) 단위는 사다리 둘이 다 끝난 뒤 시작한다 (2 판 B-7 · [사슬] 6268–6282 · 6881 줄) → 사다리 단계 끝 = 늦은 기계의 사다리 끝.
모든 출력 = 추정.  새 기준 · 합격선 없음.  σ 값 없음.
"""
import json
import math
import sys
from datetime import datetime, timedelta

# ───────── [실측] ⑥ 시도 4 (저장본 적중 · 리포 docs/data/rint2_probe6_a4_20261116/probe6_screen.txt) ─────────
A4 = {'wall_s': 4932, 'pre_step3_s': 101, 'raster_prep_s': 504, 'cjunc_prep_s': 88, 'face_alpha_prep_s': 33, 'cg_cert_s': 4297,
      'step3_stage_s': 4800, 'iters_main': 277885, 'iters_resolve': 84485, 'rss_max_kb': 34164888, 'cg_cert_s_per_iter': 0.011858}
# ───────── [실측] ⑥ 시도 3 (저장본 짓고 씀 · 리포 docs/data/rint2_probe6_a3_20261116/probe6_screen.txt) ─────────
A3 = {'wall_s': 9045, 'pre_step3_s': 90, 'raster_prep_s': 4667, 'cjunc_prep_s': 4223, 'face_alpha_prep_s': 32, 'cg_cert_s': 4258,
      'step3_stage_s': 8919, 'iters_main': 277885, 'iters_resolve': 84485, 'rss_max_kb': 34349912, 'cg_cert_s_per_iter': 0.0117504}
# ───────── [실측] ⑥ 시도 2 (옛 핀 · 리포 docs/data/rint2_probe6_a2_20261111/probe6_screen.txt) — 대조용 ─────────
A2 = {'wall_s': 22345, 'pre_step3_s': 100, 'raster_prep_s': 4467, 'cjunc_prep_s': 4040, 'face_alpha_prep_s': 31, 'cg_cert_s': 17748}
A2_OBS = {'gpu_main_s': 13245, 'gap_cpu_s': 30, 'gpu_resolve_s': 4095, 'post_cpu_s': 378}     # 2 판 B-1 [관찰]
# ───────── [관찰] samples.tsv 전이 (10 s 표본 · 2 판과 같은 읽는 법: 주 = 마지막 ≥97 % − 처음 + 5 · 이어 = +10 · 뒤 = −5) ─────────
#   시도 4: CG 시작 605 (gpu_used 3,973→8,357) · 주 → 이어 풀기 전이 3,513→3,523 (gpu_used 8,331→11,313 · 낮은 gpu_util 표본 없음) ·
#           이어 풀기 마지막 ≥97 % 4,438 · step3 끝 줄 4,902 (= 605 + 4,297)
#   시도 3: CG 시작 4,757 · 주 마지막 ≥97 % 7,666 · 사이 4 표본 (gpu_util 55–62 %) · 이어 풀기 7,716–8,632 · step3 끝 줄 9,015 (= 4,757 + 4,258)
OBS4 = {'gpu_main_s': 3513 - 605 + 5, 'gap_cpu_s': 3523 - 3513 - 10, 'gpu_resolve_s': 4438 - 3523 + 10, 'post_cpu_s': 4902 - 4438 - 5}
OBS3 = {'gpu_main_s': 7666 - 4757 + 5, 'gap_cpu_s': 7716 - 7666 - 10, 'gpu_resolve_s': 8632 - 7716 + 10, 'post_cpu_s': 9015 - 8632 - 5}
assert sum(OBS4.values()) == A4['cg_cert_s'], OBS4
assert sum(OBS3.values()) == A3['cg_cert_s'], OBS3
SAVE4 = A4['wall_s'] - A4['pre_step3_s'] - A4['raster_prep_s'] - A4['cg_cert_s']            # 30
SAVE3 = A3['wall_s'] - A3['pre_step3_s'] - A3['raster_prep_s'] - A3['cg_cert_s']            # 30
# ───────── [실측] S0 저장본 시험 (리포 docs/data/rint2_s0_sbe_20261116/files/s0log_20261116T004809Z/store_probe.json · 11-13 판 = 같은 자리 20261113) ─────────
S0_STORE = {'build_s': 4011.155, 'encode_s': 8.877, 'write_s': 120.095, 'read_s': 86.327, 'bytes': 1340095705, 'n_instances': 117583,
            'build_s_1113': 4016.043, 'encode_s_1113': 8.685, 'write_s_1113': 119.827, 'read_s_1113': 86.82, 's0_stage1_s': 5562.2,
            's0_stage1_s_1113': 5575.0}
# ───────── [실측] 합성 벤치 (리포 docs/reviews/rint2_time_reestimate_20261111/bench/results_20261112/README.md §1) ─────────
BENCH = {'gabia_A': 0.060863, 'gabia_C': 0.017917, 'kgy_busy_A': 0.046712, 'kgy_busy_C': 0.012310, 'kgy_alone_A': 0.046674, 'kgy_alone_C': 0.012301}
G_GPU_C = BENCH['gabia_C'] / ((BENCH['kgy_busy_C'] + BENCH['kgy_alone_C']) / 2.0)          # 1.456 (C 꼴 · 두 기계 다 다른 부하 있음 · 추정)
G_GPU_A = BENCH['gabia_A'] / ((BENCH['kgy_busy_A'] + BENCH['kgy_alone_A']) / 2.0)          # 1.303 (A 꼴 · 결과 README 의 1.30)
Q11_RATIO = 4.447    # 진행 기록 11-16 (docs/session_20260923_progress.md 1474 · 1479 줄) — 실침대 옛 / 새 반복당 (621 반복 · S0 와 같은 기계에서 · 참고값)

# ───────── 성분 (초 · 저장본 적중 팔 = 시도 4 · 짓는 팔 = + BUILD_EXTRA) ─────────
PRE = A4['pre_step3_s']                                       # 101
OTHER = A4['raster_prep_s'] - A4['cjunc_prep_s']              # 416 (래스터 · face_alpha 33 · 조립)
READ = A4['cjunc_prep_s']                                     # 88 (저장본 읽기 + 계획 · 판독기 칸 하나)
SAVE = SAVE4                                                  # 30
GPU_MAIN, GPU_RES = OBS4['gpu_main_s'], OBS4['gpu_resolve_s']  # 2,913 · 925
CERT_CPU = OBS4['gap_cpu_s'] + OBS4['post_cpu_s']             # 0 + 459
GPU = GPU_MAIN + GPU_RES                                      # 3,838
FIXED = PRE + OTHER + SAVE                                    # 547
GFIX = PRE + OTHER                                            # 517
BUILD_EXTRA = A3['cjunc_prep_s'] - A4['cjunc_prep_s']         # 4,135 (같은 핀 · 같은 기계 · 같은 점 — 짓고 씀 − 읽음)
CJ_NOSTORE = A2['cjunc_prep_s']                               # 4,040 (봉인 원천 = 저장본 없이 짓기 · 옛 핀 실측을 씀 — 새 핀 짓기 4,011–4,016 (S0) 과 1 % 안)
FP_S = 240.0                                                  # 봉인 원천 그래프 지문 = 2 판 그대로 (REPORT_B2 추정)
HIT_ARM = FIXED + READ + GPU + CERT_CPU
assert HIT_ARM == A4['wall_s'], HIT_ARM
PER_ITER_MAIN = GPU_MAIN / A4['iters_main']                   # 0.010483 s
PER_ITER_RES = GPU_RES / A4['iters_resolve']                  # 0.010949 s
REG_RATIO = 2578.0 / 879.0                                    # 2.9329 (등록 비 · 2 판 B-1 (나))

# ───────── 사슬 수 (2 판 그대로 · all3 · 사다리 12 점 가정 · 넘침 없음) ─────────
LADDER_ARMS = 12 + 4 + 2 + 1      # 법칙마다: 사다리 12 · 끝 origin 4 · SBE origin 2 · no-op 1 = 19 팔 (한 기계)
ORIGINS = 3                       # arm 0 · 1 · 2 → 기계마다 · 침대마다 저장본 3 개
UNITS = 12
UNIT_DBE_F0 = {'lo': 4, 'hi': 5}  # 등록 꼴 (F0): 단위 = DBE "팔" 4–5
N_POST = 36                       # 합치기 12 + 판정 12 + 다시 판정 12 = 봉인 원천 런 36 (한 기계)
ORIGIN8_NEW = 5                   # 넘침 origin8 의 arm 3–7 = 새 저장본 5 개 (그 기계 · 그 침대에서 처음일 때)


def mach(name, gpu_f, cpu_f):
    return {'name': name, 'g': gpu_f, 'c': cpu_f}


def comp(M, s=1.0, r=REG_RATIO, m=1.0, r_mode='arm'):
    """기계 M 의 성분 (초).  r_mode = 'arm' (DBE 준비도 r 배 · 2 판 '팔 전체') · 'solve' (DBE 준비 = SBE · 2 판 '풀이에만')."""
    r_p = r if r_mode == 'arm' else 1.0
    cold_s = GPU * M['g'] * m / s + CERT_CPU * M['c']          # SBE 차가운 풀이 하나 + ⓒ + 증서 CPU
    prep_s = (FIXED + READ) * M['c']                             # 저장본 적중 팔의 준비 (+ 저장)
    build_s = BUILD_EXTRA * M['c']                               # 그 기계 · 침대 · origin 의 첫 팔에만
    g_s = (GFIX + CJ_NOSTORE) * M['c'] + FP_S * M['c']           # 봉인 원천 (SBE 꼴 — 쓰지 않음 · 참고)
    return {'cold_s': cold_s, 'prep_s': prep_s, 'arm_s': prep_s + cold_s, 'build_s': build_s,
            'cold_d': r * cold_s, 'prep_d': r_p * prep_s, 'arm_d': r_p * prep_s + r * cold_s, 'build_d': r_p * build_s,
            'g_d': r_p * (GFIX + CJ_NOSTORE) * M['c'] + FP_S * M['c'], 'g_s': g_s}


def ladder(M, **kw):
    c = comp(M, **kw)
    return LADDER_ARMS * c['arm_s'] + ORIGINS * c['build_s']


def unit_hit(M, u, **kw):
    """F1 단위 하나 (저장본 적중): 모서리 팔 (준비 + 차가운 풀이 2 + 위끝 u) + 봉인 원천 1 + origin 팔 2."""
    c = comp(M, **kw)
    return c['prep_d'] + (2 + u) * c['cold_d'] + c['g_d'] + 2 * c['arm_d']


def units_on(M, n, u, **kw):
    c = comp(M, **kw)
    return 0.0 if n == 0 else n * unit_hit(M, u, **kw) + ORIGINS * c['build_d']


def f1_two(K, G, u, split=None, **kw):
    """두 대 (K · G) · 사다리 법칙 하나씩 · 단위 n_K / 12 − n_K (split None = 늦은 기계 끝이 가장 이른 정수 나눔)."""
    lad = max(ladder(K, **kw), ladder(G, **kw))
    best = None
    rng = [split] if split is not None else range(0, UNITS + 1)
    for nk in rng:
        tk, tg = units_on(K, nk, u, **kw), units_on(G, UNITS - nk, u, **kw)
        t = lad + max(tk, tg)
        if best is None or t < best['sim_s'] - 1e-9:
            best = {'n_kgy': nk, 'n_gabia': UNITS - nk, 'sim_s': t, 'ladder_s': lad, 'units_kgy_s': tk, 'units_gabia_s': tg,
                    'ladder_kgy_s': ladder(K, **kw), 'ladder_gabia_s': ladder(G, **kw)}
    gk = comp(K, **kw)['g_d']
    best['post_merge_verdict_s'] = 24 * gk
    best['post_all_s'] = N_POST * gk
    best['g_d_kgy_s'] = gk
    return best


def f0_two_equal(**kw):
    """2 판 B-3 과 같은 꼴 (등록 꼴 F0 · 두 기계 같은 속도 · 12/2 = 6 단위 · 단위 = DBE "팔" 4–5) — 새 입력 · 저장본 짓기 포함."""
    K = mach('kgy', 1.0, 1.0)
    c = comp(K, **kw)
    lad = LADDER_ARMS * c['arm_s'] + ORIGINS * c['build_s']
    out = {}
    for k in ('lo', 'hi'):
        out[k] = lad + math.ceil(UNITS / 2) * UNIT_DBE_F0[k] * c['arm_d'] + ORIGINS * c['build_d']
    return out


def overflow_one_corner(K, G, **kw):
    """넘침 하나 (모서리 하나 · 세 R × 8 팔 = 점 3 개 · 점 하나 = 한 런) — 점을 두 기계에 나누는 가장 이른 꼴 + 끝 합치기 12 (kgy)."""
    ck, cg = comp(K, **kw), comp(G, **kw)

    def load(c, n):
        return 0.0 if n == 0 else n * 8 * c['arm_d'] + ORIGIN8_NEW * c['build_d']
    best = None
    for nk in range(0, 4):
        t = max(load(ck, nk), load(cg, 3 - nk))
        if best is None or t < best['points_s']:
            best = {'n_kgy': nk, 'points_s': t}
    best['final_merge_s'] = 12 * ck['g_d']
    best['point_first_kgy_s'] = 8 * ck['arm_d'] + ORIGIN8_NEW * ck['build_d']
    best['point_first_gabia_s'] = 8 * cg['arm_d'] + ORIGIN8_NEW * cg['build_d']
    best['point_hit_kgy_s'] = 8 * ck['arm_d']
    best['point_hit_gabia_s'] = 8 * cg['arm_d']
    return best


def stage_table(K, G, **kw):
    """시간 상한 (단계 하나하나의 마감 · 2 판 A-4) 재료 — 기계마다."""
    rows = {}
    for M in (K, G):
        c = comp(M, **kw)
        rows[M['name']] = {
            'ladder_19_arms_h': h(ladder(M, **kw)),
            'ladder_origin8_extra_h': h(8 * c['arm_s'] + ORIGIN8_NEW * c['build_s']),
            'unit_first_hi_h': h(unit_hit(M, 1, **kw) + ORIGINS * c['build_d']),
            'unit_hit_lo_h': h(unit_hit(M, 0, **kw)), 'unit_hit_hi_h': h(unit_hit(M, 1, **kw)),
            'point_first_8_arms_h': h(8 * c['arm_d'] + ORIGIN8_NEW * c['build_d']),
            'point_hit_8_arms_h': h(8 * c['arm_d']),
            'graph_only_run_h': h(c['g_d']), 'merge_12_graph_only_h': h(12 * c['g_d']),
            'dbe_arm_hit_h': h(c['arm_d']), 'sbe_arm_hit_h': h(c['arm_s']), 'dbe_build_extra_h': h(c['build_d']),
        }
    return rows


def h(sec):
    return round(sec / 3600.0, 1)


KGY = mach('kgy', 1.0, 1.0)
GAB = {'equal': mach('gabia', 1.0, 1.0), 'gpu146': mach('gabia', G_GPU_C, 1.0), 'gpu146_cpu2': mach('gabia', G_GPU_C, 2.0)}

START = datetime(2026, 11, 20, 0, 0)          # R 시작 가정 (KST) — 봉인 전 남은 단계의 날 수는 모른다 [가정]
DEADLINES = {'12-01 00:00 (= 11-30 24:00 · 옛 기준)': datetime(2026, 12, 1, 0, 0),
             '12-06 00:00 (= 12-05 24:00 · "12 월 초" 가정)': datetime(2026, 12, 6, 0, 0)}


def cal(sim_s):
    end = START + timedelta(seconds=sim_s)
    out = {'end_if_start_1120': end.strftime('%m-%d %H시')}
    for k, d in DEADLINES.items():
        slack = (d - end).total_seconds() / 3600.0
        latest = d - timedelta(seconds=sim_s)
        out[k] = {'slack_h': round(slack, 1), 'latest_start': latest.strftime('%m-%d %H시')}
    return out


def main_table(gname='gpu146', r_mode='arm', r=REG_RATIO, m=1.0):
    G = GAB[gname]
    rows = []
    for s in (1.0, 1.5, 2.0):
        lo = f1_two(KGY, G, 0, s=s, r=r, m=m, r_mode=r_mode)
        hi = f1_two(KGY, G, 1, s=s, r=r, m=m, r_mode=r_mode)
        rows.append({'s': s, 'sim_h': [h(lo['sim_s']), h(hi['sim_s'])], 'days': [round(lo['sim_s'] / 86400, 1), round(hi['sim_s'] / 86400, 1)],
                     'split_lo_hi': [[lo['n_kgy'], lo['n_gabia']], [hi['n_kgy'], hi['n_gabia']]],
                     'ladder_h': [h(lo['ladder_kgy_s']), h(lo['ladder_gabia_s'])],
                     'post_merge_verdict_h': h(lo['post_merge_verdict_s']), 'post_all_h': h(lo['post_all_s']),
                     'to_reverify_h': [h(lo['sim_s'] + lo['post_all_s']), h(hi['sim_s'] + hi['post_all_s'])],
                     'cal_lo': cal(lo['sim_s']), 'cal_hi': cal(hi['sim_s'])})
    return rows


def maxiter_table():
    out = []
    for v in (3000000, 4000000, 5000000, 6000000):
        one_k = v * PER_ITER_MAIN
        out.append({'maxiter': v, 'x_sbe_main': round(v / A4['iters_main'], 2),
                    'one_solve_to_cap_h_kgy': h(one_k), 'one_solve_to_cap_h_gabia': h(one_k * G_GPU_C),
                    'main_plus_resolve_to_cap_h_kgy': h(2 * one_k), 'main_plus_resolve_to_cap_h_gabia': h(2 * one_k * G_GPU_C)})
    return out


def main():
    out = {
        'label': '추정 — 실측 SBE 한 점 (시도 3 · 4) + 가정 (s · r · m · gabia 속도 · 사다리 12 점 · 넘침 없음) · DBE 는 재지 않았다',
        'components_s': {'PRE': PRE, 'OTHER': OTHER, 'READ': READ, 'SAVE': SAVE, 'GPU_MAIN': GPU_MAIN, 'GPU_RES': GPU_RES, 'CERT_CPU': CERT_CPU,
                         'GPU': GPU, 'FIXED': FIXED, 'GFIX': GFIX, 'BUILD_EXTRA': BUILD_EXTRA, 'CJ_NOSTORE': CJ_NOSTORE, 'FP_S': FP_S,
                         'HIT_ARM': HIT_ARM, 'BUILD_ARM_model': HIT_ARM + BUILD_EXTRA, 'BUILD_ARM_measured_a3': A3['wall_s']},
        'obs_split': {'a4': OBS4, 'a3': OBS3, 'a2': A2_OBS},
        'per_iter_s': {'a4_main': round(PER_ITER_MAIN, 6), 'a4_resolve': round(PER_ITER_RES, 6),
                       'a3_main': round(OBS3['gpu_main_s'] / A3['iters_main'], 6), 'a3_resolve': round(OBS3['gpu_resolve_s'] / A3['iters_resolve'], 6),
                       'a2_main': round(A2_OBS['gpu_main_s'] / 277885, 6), 'a2_resolve': round(A2_OBS['gpu_resolve_s'] / 84485, 6),
                       'ratio_a2_over_a4_main': round((A2_OBS['gpu_main_s'] / 277885) / PER_ITER_MAIN, 3),
                       'ratio_a2_over_a3_main': round((A2_OBS['gpu_main_s'] / 277885) / (OBS3['gpu_main_s'] / A3['iters_main']), 3),
                       'q11_real_ratio': Q11_RATIO, 'bench_kgy_A_over_C': [round(BENCH['kgy_busy_A'] / BENCH['kgy_busy_C'], 3),
                                                                           round(BENCH['kgy_alone_A'] / BENCH['kgy_alone_C'], 3)],
                       'contention_residual_a2a3_over_q11': round(((A2_OBS['gpu_main_s'] / 277885) / (OBS3['gpu_main_s'] / A3['iters_main'])) / Q11_RATIO, 3)},
        'machine_ratio': {'gabia_over_kgy_C': round(G_GPU_C, 3), 'gabia_over_kgy_A': round(G_GPU_A, 3)},
        'store': {'a3_minus_a4_wall': A3['wall_s'] - A4['wall_s'], 'build_extra_cjunc': BUILD_EXTRA,
                  's0_build_encode_write': round(S0_STORE['build_s'] + S0_STORE['encode_s'] + S0_STORE['write_s'], 1),
                  'a3_cjunc_minus_s0_sum': round(A3['cjunc_prep_s'] - (S0_STORE['build_s'] + S0_STORE['encode_s'] + S0_STORE['write_s']), 1),
                  'a4_cjunc_minus_s0_read': round(A4['cjunc_prep_s'] - S0_STORE['read_s'], 1)},
        'arm_vs_a2': {'a2_wall': A2['wall_s'], 'a4_wall': A4['wall_s'], 'ratio': round(A2['wall_s'] / A4['wall_s'], 2),
                      'a3_wall': A3['wall_s'], 'ratio_a2_a3': round(A2['wall_s'] / A3['wall_s'], 2)},
        'shares_a4': {k: round(100.0 * v / A4['wall_s'], 1) for k, v in
                      {'PRE': PRE, 'OTHER': OTHER, 'READ': READ, 'GPU_MAIN': GPU_MAIN, 'GPU_RES': GPU_RES, 'CERT_CPU': CERT_CPU, 'SAVE': SAVE}.items()},
        'f0_equal_two': {},
        'main_arm_gpu146': main_table('gpu146', 'arm'),
        'main_solve_gpu146': main_table('gpu146', 'solve'),
        'sens': {},
        'stage_s1_reg_arm': stage_table(KGY, GAB['gpu146'], s=1.0, r=REG_RATIO, r_mode='arm'),
        'stage_s1_x2_arm': stage_table(KGY, GAB['gpu146'], s=1.0, r=2 * REG_RATIO, r_mode='arm'),
        'stage_s1_reg_solve': stage_table(KGY, GAB['gpu146'], s=1.0, r=REG_RATIO, r_mode='solve'),
        'overflow': {},
        'maxiter': maxiter_table(),
        'start_assumed_kst': START.strftime('%Y-%m-%d %H:%M'),
    }
    for s in (1.0, 1.5, 2.0):
        v = f0_two_equal(s=s, r=REG_RATIO, m=1.0, r_mode='arm')
        out['f0_equal_two'][f's{s}'] = [h(v['lo']), h(v['hi'])]
        for rr, nm in ((0.5 * REG_RATIO, 'r0.5'), (2 * REG_RATIO, 'r2')):
            v = f0_two_equal(s=s, r=rr, m=1.0, r_mode='arm')
            out['f0_equal_two'][f's{s}_{nm}'] = [h(v['lo']), h(v['hi'])]
    # 감도 (s 1 · F1 · 단위 나눔 최적)
    sens = {}
    for label, gname, kw in (
            ('기준 (gabia GPU 1.456 · CPU 1 · r 등록 · m 1 · 팔 전체)', 'gpu146', dict(r=REG_RATIO, m=1.0, r_mode='arm')),
            ('두 기계 같음 (2 판 가정)', 'equal', dict(r=REG_RATIO, m=1.0, r_mode='arm')),
            ('gabia CPU 2 배', 'gpu146_cpu2', dict(r=REG_RATIO, m=1.0, r_mode='arm')),
            ('DBE 비 반 (1.467)', 'gpu146', dict(r=0.5 * REG_RATIO, m=1.0, r_mode='arm')),
            ('DBE 비 두 배 (5.866)', 'gpu146', dict(r=2 * REG_RATIO, m=1.0, r_mode='arm')),
            ('m 0.5', 'gpu146', dict(r=REG_RATIO, m=0.5, r_mode='arm')),
            ('m 2', 'gpu146', dict(r=REG_RATIO, m=2.0, r_mode='arm')),
            ('DBE 비 두 배 · m 2', 'gpu146', dict(r=2 * REG_RATIO, m=2.0, r_mode='arm')),
            ('풀이에만 · DBE 비 두 배', 'gpu146', dict(r=2 * REG_RATIO, m=1.0, r_mode='solve')),
    ):
        lo = f1_two(KGY, GAB[gname], 0, s=1.0, **kw)
        hi = f1_two(KGY, GAB[gname], 1, s=1.0, **kw)
        sens[label] = {'sim_h': [h(lo['sim_s']), h(hi['sim_s'])], 'split': [[lo['n_kgy'], lo['n_gabia']], [hi['n_kgy'], hi['n_gabia']]],
                       'post_all_h': h(lo['post_all_s']), 'cal_hi': cal(hi['sim_s'])}
    out['sens'] = sens
    for label, kw in (('s1 · r 등록 · 팔 전체', dict(s=1.0, r=REG_RATIO, r_mode='arm')),
                      ('s1 · r 등록 · 풀이에만', dict(s=1.0, r=REG_RATIO, r_mode='solve')),
                      ('s1 · r 두 배 · 팔 전체', dict(s=1.0, r=2 * REG_RATIO, r_mode='arm'))):
        ov = overflow_one_corner(KGY, GAB['gpu146'], **kw)
        out['overflow'][label] = {k: (h(v) if k.endswith('_s') else v) for k, v in ov.items()}
    # 같은 단위 나눔 고정 (6/6) 과 최적 나눔의 차
    lo66 = f1_two(KGY, GAB['gpu146'], 0, split=6, s=1.0, r=REG_RATIO, r_mode='arm')
    hi66 = f1_two(KGY, GAB['gpu146'], 1, split=6, s=1.0, r=REG_RATIO, r_mode='arm')
    out['split66_s1_reg_arm_h'] = [h(lo66['sim_s']), h(hi66['sim_s'])]
    # 시간 상한 재료 — m 2 · DBE 비 두 배 · m 2
    out['stage_s1_reg_m2_arm'] = stage_table(KGY, GAB['gpu146'], s=1.0, r=REG_RATIO, m=2.0, r_mode='arm')
    out['stage_s1_x2_m2_arm'] = stage_table(KGY, GAB['gpu146'], s=1.0, r=2 * REG_RATIO, m=2.0, r_mode='arm')
    # 넘침 하나가 GPU 팔 끝에 더하는 것 = 첫 합치기 (봉인 원천 12 · kgy · 넘침을 아는 자리) + 점 (두 기계 최적)
    inc = {}
    for label, kw in (('arm_s1_reg', dict(s=1.0, r=REG_RATIO, r_mode='arm')), ('solve_s1_reg', dict(s=1.0, r=REG_RATIO, r_mode='solve')),
                      ('arm_s1_x2', dict(s=1.0, r=2 * REG_RATIO, r_mode='arm'))):
        ov = overflow_one_corner(KGY, GAB['gpu146'], **kw)
        hi = f1_two(KGY, GAB['gpu146'], 1, **kw)
        add = ov['final_merge_s'] + ov['points_s']          # 첫 합치기 시간 = 끝 합치기와 같은 12 런
        inc[label] = {'first_merge_h': h(ov['final_merge_s']), 'points_h': h(ov['points_s']), 'gpu_end_add_h': h(add),
                      'gpu_end_hi_with_overflow_h': h(hi['sim_s'] + add), 'cal': cal(hi['sim_s'] + add)}
    out['overflow_gpu_end'] = inc
    # 다시 판정까지의 달력 (11-20 시작 가정)
    rv = {}
    for label, kw in (('arm_s1', dict(s=1.0, r=REG_RATIO, r_mode='arm')), ('solve_s1', dict(s=1.0, r=REG_RATIO, r_mode='solve')),
                      ('arm_s2', dict(s=2.0, r=REG_RATIO, r_mode='arm')), ('solve_s2', dict(s=2.0, r=REG_RATIO, r_mode='solve'))):
        lo, hi = f1_two(KGY, GAB['gpu146'], 0, **kw), f1_two(KGY, GAB['gpu146'], 1, **kw)
        rv[label] = {'verdict_h': [h(lo['sim_s'] + lo['post_merge_verdict_s']), h(hi['sim_s'] + hi['post_merge_verdict_s'])],
                     'reverify_h': [h(lo['sim_s'] + lo['post_all_s']), h(hi['sim_s'] + hi['post_all_s'])],
                     'reverify_end_if_start_1120': [(START + timedelta(seconds=lo['sim_s'] + lo['post_all_s'])).strftime('%m-%d %H시'),
                                                    (START + timedelta(seconds=hi['sim_s'] + hi['post_all_s'])).strftime('%m-%d %H시')]}
    out['reverify_cal'] = rv
    # kgy 가 gabia 사다리를 기다리는 시간 (단위 시작 전)
    out['kgy_wait_for_gabia_ladder_h'] = round(h(ladder(GAB['gpu146'])) - h(ladder(KGY)), 1)
    # 두 대 나눔이 무너질 때 (11-12 Q10 조립 비트 같음 미확인 · 2 판 B-9 의 4) — kgy 한 대 · 지금 사슬 (사다리 둘은 두 기계 · 예측 = kgy)
    fb = {}
    for label, kw in (('arm_s1', dict(s=1.0, r=REG_RATIO, r_mode='arm')), ('solve_s1', dict(s=1.0, r=REG_RATIO, r_mode='solve'))):
        c = comp(KGY, **kw)
        one_lad = 2 * LADDER_ARMS * c['arm_s'] + ORIGINS * c['build_s']        # 같은 기계 · 같은 침대 → SBE 저장본 3 개를 두 법칙이 같이 읽는다
        one = [one_lad + units_on(KGY, UNITS, u, **kw) for u in (0, 1)]
        nos = [max(ladder(KGY, **kw), ladder(GAB['gpu146'], **kw)) + units_on(KGY, UNITS, u, **kw) for u in (0, 1)]
        fb[label] = {'one_machine_kgy_h': [h(x) for x in one], 'one_machine_cal_hi': cal(one[1]),
                     'no_split_predict_on_kgy_h': [h(x) for x in nos], 'no_split_cal_hi': cal(nos[1])}
    out['fallback'] = fb
    # S0 단계 2 (DBE) 어림 = SBE 단계 1 실측 × {1 · r}
    out['s0_stage2_guess_h'] = [h(S0_STORE['s0_stage1_s']), h(S0_STORE['s0_stage1_s'] * REG_RATIO)]
    # 기계 사이 첫 팔 대조 (gabia 저장본 적중 팔 · 짓는 팔)
    cg = comp(GAB['gpu146'])
    out['gabia_sbe_hit_arm_s'] = round(cg['arm_s'])
    out['gabia_sbe_build_arm_s'] = round(cg['arm_s'] + cg['build_s'])
    ck = comp(KGY)
    out['kgy_dbe_hit_arm_arm_mode_s'] = round(ck['arm_d'])
    out['kgy_dbe_hit_arm_solve_mode_s'] = round(comp(KGY, r_mode='solve')['arm_d'])
    out['kgy_dbe_build_extra_arm_mode_s'] = round(ck['build_d'])
    out['graph_only_arm_mode_s'] = round(ck['g_d'])
    out['graph_only_solve_mode_s'] = round(comp(KGY, r_mode='solve')['g_d'])
    if '--json' in sys.argv:
        json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
        sys.stdout.write('\n')
        return
    p = print
    p('components', out['components_s'])
    p('obs', out['obs_split'])
    p('per_iter', out['per_iter_s'])
    p('machine', out['machine_ratio'])
    p('store', out['store'])
    p('arm_vs_a2', out['arm_vs_a2'])
    p('shares_a4', out['shares_a4'])
    p('F0 equal two', out['f0_equal_two'])
    for key in ('main_arm_gpu146', 'main_solve_gpu146'):
        p('==', key)
        for row in out[key]:
            p('  ', json.dumps(row, ensure_ascii=False))
    p('== sens')
    for k, v in out['sens'].items():
        p('  ', k, json.dumps(v, ensure_ascii=False))
    p('== stage s1 reg arm', json.dumps(out['stage_s1_reg_arm'], ensure_ascii=False))
    p('== stage s1 x2 arm', json.dumps(out['stage_s1_x2_arm'], ensure_ascii=False))
    p('== stage s1 reg solve', json.dumps(out['stage_s1_reg_solve'], ensure_ascii=False))
    p('== overflow', json.dumps(out['overflow'], ensure_ascii=False))
    p('== maxiter', json.dumps(out['maxiter'], ensure_ascii=False))
    p('== split 6/6 s1 reg arm', out['split66_s1_reg_arm_h'])
    p('== stage s1 reg m2 arm', json.dumps(out['stage_s1_reg_m2_arm'], ensure_ascii=False))
    p('== stage s1 x2 m2 arm', json.dumps(out['stage_s1_x2_m2_arm'], ensure_ascii=False))
    p('== overflow gpu end', json.dumps(out['overflow_gpu_end'], ensure_ascii=False))
    p('== reverify cal', json.dumps(out['reverify_cal'], ensure_ascii=False))
    p('== fallback', json.dumps(out['fallback'], ensure_ascii=False))
    for k in ('kgy_wait_for_gabia_ladder_h', 's0_stage2_guess_h', 'gabia_sbe_hit_arm_s', 'gabia_sbe_build_arm_s', 'kgy_dbe_hit_arm_arm_mode_s',
              'kgy_dbe_hit_arm_solve_mode_s', 'kgy_dbe_build_extra_arm_mode_s', 'graph_only_arm_mode_s', 'graph_only_solve_mode_s'):
        p(k, out[k])


if __name__ == '__main__':
    main()
