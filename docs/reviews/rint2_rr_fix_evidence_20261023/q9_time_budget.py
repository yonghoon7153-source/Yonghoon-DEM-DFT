#!/usr/bin/env python3
"""R 주 판정 시간 어림 (추정) — SV all3 (Q5 (가)) · 기계 1–3 대 · 예측 단계를 단위로 나눌 때 / 안 나눌 때.

입력은 전부 등록 R §10-4 표의 값 그대로 (새 측정 없음):
  팔 하나 기준 시간 SBE 879 s · DBE 2,578 s · 풀이 몫 704/879 · 접합 꼴 반복 비 ×6.05 – ×7.37 (합성 침대).
팔 수 (등록 §10-4 · §10): SBE 38 = 사다리 24 (법칙마다 12) + 끝 origin 8 + SBE origin 4 + no-op 2 (예측 단계 · 법칙마다 1).
  DBE (all3) = 모서리 arm 0 12 + DBE origin 24 (모서리 × R 마다 arm 1 · 2) + SV 반사실 아래 12 + 위끝 0–12 (못 가른 덩어리가 있는 점만).
가정 (추정 표지): 기계 속도 같음 · origin 넘침 없음 · 사다리 단계 = 법칙마다 한 기계에서 차례로 (18 풀이) · 두 법칙 동시 ·
  예측 단위 = (c, 법칙, R) 12 개 (단위마다 DBE 4–5 풀이) · no-op = 법칙마다 한 단위에 붙음 · 단위를 기계에 고르게 나눔.
"""
import json
import math
import sys

S, D = 879.0, 2578.0
F = 704.0 / 879.0
R_LO, R_HI = 6.05, 7.37
M = {k: (1.0 - F) + F * r for k, r in (('lo', R_LO), ('hi', R_HI))}
LADDER_PER_LAW = 12 + 4 + 2          # 사다리 12 · 끝 origin 4 · SBE origin 2 (법칙마다)
NOOP = 2                              # 예측 단계 SBE no-op (법칙마다 1)
UNITS = 12                            # (c, 법칙, R)
UNIT_DBE = {'lo': 1 + 2 + 1, 'hi': 1 + 2 + 1 + 1}   # arm 0 · origin 2 · SV 아래 · (위끝)


def hours(sec, k):
    return round(sec * M[k] / 3600.0, 1)


def one_machine(k):
    dbe = UNITS * UNIT_DBE[k]
    return hours((2 * LADDER_PER_LAW + NOOP) * S + dbe * D, k)


def split(n, k):
    """사다리 두 줄 동시 (n ≥ 2) → 예측 단위를 n 대에 고르게 (가장 많이 받은 기계가 끝 시각)."""
    per = math.ceil(UNITS / n)
    noop_on_busiest = min(NOOP, 1) if n >= 2 else NOOP
    return hours(LADDER_PER_LAW * S + (per * UNIT_DBE[k]) * D + noop_on_busiest * S, k)


def no_split(n, k):
    """예측 단계 = 한 기계 (지금 사슬) · 사다리 두 줄만 n ≥ 2 에서 동시."""
    dbe = UNITS * UNIT_DBE[k]
    lad = LADDER_PER_LAW if n >= 2 else 2 * LADDER_PER_LAW
    return hours(lad * S + NOOP * S + dbe * D, k)


out = {
    'inputs': {'sbe_arm_s': S, 'dbe_arm_s': D, 'solve_fraction': F, 'iter_ratio': [R_LO, R_HI],
               'multiplier': {k: round(v, 4) for k, v in M.items()},
               'ladder_per_law': LADDER_PER_LAW, 'noop': NOOP, 'units': UNITS, 'unit_dbe_solves': UNIT_DBE,
               'source': 'docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md §10-4 (값 그대로)'},
    'label': '추정 · 합성 침대 반복 비 · 기계 속도 같음 · origin 넘침 없음 · 위끝 = 0 (lo) / 12 (hi)',
    'old_registration_82_R0_only_one_machine_h': [hours(38 * S + 44 * D, 'lo'), hours(38 * S + 44 * D, 'hi')],
    'all3_one_machine_h': [one_machine('lo'), one_machine('hi')],
    'all3_no_split_h': {str(n): [no_split(n, 'lo'), no_split(n, 'hi')] for n in (2, 3)},
    'all3_split_units_h': {str(n): [split(n, 'lo'), split(n, 'hi')] for n in (2, 3)},
    'overflow_note': '등록 §10-4: 모서리 하나 origin 넘침 = +24 팔 ≈ +87 h (×6.05 · 한 기계) — 이 표에 넣지 않았다',
}
json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
sys.stdout.write('\n')
