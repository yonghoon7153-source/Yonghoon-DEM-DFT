#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② R 런 사슬 — SBE 보정 사다리 (등록 R §3) · DBE holdout 예측 (§4) · 판정 (§5) · 다시 판정.

정본 = 등록 R `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` §3 (3-1 – 3-5) · §4 (4-1 · 4-2) · §5 · §6 · §7-1 ·
§10 (명령 꼴 (3)–(5) · 멈춤 목록 · 런 수) · §11 · 설계 v1 `docs/reviews/rint_carbon_additive_design_v1_20261020.md` §6 (수렴 증서 ⓐ ⓑ ⓒ ⓓ) ·
§7 (세대 `p3ca-` · 영수증 · LEAN 표 · 판정 계산기 · 다시 판정).  꼴 = 앞선 같은 부류 사슬 `scripts/sdcp_anchor_v2_chain.py`
(사슬이 점을 고른다 · 값 봉인 · 멈춤 · 요약에서 다음 단계가 읽는다 · 사람이 옮겨 적지 않는다).

  # (3) 보정 사다리 — 법칙 끝마다 (SBE arm 0 · LEAN 2 · 값 봉인)
  python3 scripts/rint_r_chain.py --stage ladder --law P0 --target 1.63 --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh \\
      --root ~/sdcp --plan ~/sdcp/ca1_plan.json --s0-plan <리포 S0 계획> --s0-stage2-report <S0 단계 2 보고 (DBE 새 침대)> \\
      --max-hours H --out ~/sdcp/ca1_ladder_P0
  # (4) 예측 — 네 모서리 × {R_j,lo · R_j,0 · R_j,hi} (DBE arm 0 · R_j · 계획 · S0 계획은 사다리 요약에서 읽는다)
  python3 scripts/rint_r_chain.py --stage predict --ladders ~/sdcp/ca1_ladder_P0 ~/sdcp/ca1_ladder_P1 --kit kit_DBE_sdcp1um_vgcf100 \\
      --runner … --root ~/sdcp --max-hours H --out ~/sdcp/ca1_predict
  # 감도 (등록 R §5-6 · 필수 · ★ 주 판정 단계 뒤에만 — Q-F): --variant FIBRE | UNREG | GRID (사다리 둘 + 예측) · SVORDER (예측만 · 주 사다리)
  #   … --variant FIBRE --after-main ~/sdcp/ca1_predict
  # (5) 판정 — 원 팔 JSON 전부에서 (값은 --show-results 로 한 번) · 다시 판정 (읽기 전용 · 바이트 대조)
  python3 scripts/rint_r_chain.py --stage verdict --runs <사다리 · 예측 · 감도 폴더 …> --out ~/sdcp/ca1_verdict [--show-results]
  python3 scripts/rint_r_chain.py --stage verdict --reverify ~/sdcp/ca1_verdict

값 봉인: 사슬은 σ 를 읽어 점을 고르지만 화면 · 로그 · 공개 요약에는 σ 를 쓰지 않는다 (반복 수 · 잔차 · 판 전류 불균형 · 시간 · 상태만 ·
  σ 가 든 멈춤 사유는 그 수를 가린다).  σ 는 팔 JSON 에만 있고, 판정 결과 (`verdict_results.json`) 는 `--show-results` 로 연다.
★ Z3 (10-20) — 러너 · payload API 와 맞춤: face_alpha + 접합 (+ P1) 한 런 · 극한 런 (env `CJUNC_RJ=inf` · `0`) · origin 검사 = `ARM_LIST=1,2`
  한 런 (a0 = 앞 런의 값 그대로 · 넘으면 8 팔 = `ARMS=8`) · off 격자 sid 지문 (`sid_off` = 접합 원장 `fp.sid` · 같은 킷 · 같은 래스터 ·
  같은 origin 런끼리) · CG 반복 수 (공개 기록) · 계약 = 정본 (`ca_ext_record_ok` · `check_arm` · backend = `EXPECT_BACKEND`).
★ 3판 (10-21 · D · 등록 R 3판 · Codex RCA-01 · 02 · 06 · 08 · 09 · 10 · 13 · 사전 리뷰 PRE-design-01 · 05 · 코디네이터 Q-E · Q-F · Q-G):
  · 계획 `rint-r-plan-v2` = v1 칸 + 결과 전 등록 숫자 넷 (점 수 상한 · 역상 R 비 상한 · SV 반사실 문턱 · 범위) — 하나라도 null = 멈춤
  · 두 계획 대조 (S0 `ca-cjunc-plan-v1` ↔ R) · 등록 `| S0 계획 해시 |` 줄 (§2-1 · §10-2 ⑪)
  · 해 상태 (positive · zero · short — `run_contract.next_gen_state`) = 확장 실수 0 · ~~+∞~~ (★ 4판 Q1: short = NOT_COMPUTED) · 모든 비교 = ln
    (단위 불변 · §5-0)
  · 끝 규칙 (§3-2b · 실제 SBE 역상 · 끝 확인 런 · 바깥 실측 이웃) + 끝 origin (세 origin 합집합을 바깥에서 · PRE-design-01 Q-E) ·
    e_min = 국소 진단 (멈추지 않는다) · 역상 R 비 상한 = 계획 (⬜ · 'none' = 상한 없음으로 등록)
  · DBE origin = 네 모서리 × 세 R (§4-2) · 한 R 이라도 넘으면 그 모서리 세 R 전부 8 팔 평균
  · 감도 = 주 판정과 같은 판정 함수 (§5-6 · RCA-09) · 법칙별 I_P · U · E · `GAP_ENVELOPE_ONLY` (§5-1 · RCA-08) · 결정표 (§5-7)
  · 차단 표지 = 닫힌 집합 (§5-6a · RCA-10) · 보고 범주 `ASSUMED_UNVALIDATED` · §7-1 문장 = 판정문 §5-3 문안
  · SV 반사실 (CJUNC_SV_CF · 계획 범위 · 비 > 문턱 = `SV_DEPENDENT` · 못 읽음 = `SV_UNCHECKED` · 옛 `SV_DOMINANT` 철회 · RCA-06) —
    사슬은 비 · 상태만 읽는다 (끊는 면의 정의 무관 · PRE-impl-04 · `ca_ext_svcf.chain_view`) · ★ 10-22 (사전 리뷰 2 회차 PRE2-impl-01 ·
    1저자 Q1 (다)) 괄호 판정 — 모서리마다 아래 끝 (못 가른 덩어리 그대로) > 문턱 = `SV_DEPENDENT` · 두 끝을 읽고 위 끝 (덩어리를 통째로 뺀 판)
    ≤ 문턱 = 표지 없음 · 걸침 · 못 읽음 = `SV_UNCHECKED` (`sv_assess`)
  · 감도 단계 = 주 판정 단계 (사다리 둘 · 예측) 가 끝난 뒤에만 (`--after-main` · 판정이 묶음을 대조 · Q-F)
★ 4판 (10-21 · DQ · 등록 R 4판 · 1저자 10-21 Q1 · Q2 "권고대로"):
  · Q1 (§5-0 ①–③ · §4-2 ③ · R4-Q5) 단락 (ELECTRODE_SHORT · J11) = 생산자 미게시 → 그 런 = NOT_COMPUTED (사유 = 상태 이름 ELECTRODE_SHORT) —
    +∞ 로 판정에 오지 않는다 · 이 등록의 풀이 상태 = POSITIVE_SOLVED · VALID_ZERO_TOPOLOGY · NOT_COMPUTED 셋 (`registration_state`) ·
    예측 단계의 NOT_COMPUTED = 등록 결과 (사다리와 같은 뜻 · 판정이 원 팔에서 다시 계산) · 판정 기록 `reasons` = 단계 · 법칙 · 사유
  · Q2 (규칙 여섯) — ① §3-2c 이름 우선순위 (하나라도 NOT_COMPUTED 면 NOT_COMPUTED · PRE-design-08 · `judge_set`) ② §3-2b ③″ 보호 띠
    (판독 [σ(1 − e), σ(1 + e)] · e = 그 런 증서 ⓓ 보장 오차 `target_err_bound_rel` (read_run 이 증서 구간에서 `step3_conv_cert.target_judge` 로
    다시 계산 · 팔 기록 `err_rel`) · 걸치면 보수 쪽 — 끝 = 바깥으로 · EDGE = EDGE · `outside_band` · `edge_hit` · PRE-design-12) ③ §4-2 origin
    상태 다름 = 넘음 · W ∈ {+∞, 0} → W₊ (`dbe_origin_ok` · PRE-design-10) ④ §5-5b 결정표 (오른쪽 칸 · 점 구간 · ⑰ 감도 미완료 · ⑱ ·
    `decide_sentence` · 표지마다 사유 `blocking_reasons` · PRE-design-09) ⑤ §5-6 변이 표지 (NOT_COMPUTED · 변이 자신의 CALIB_ORIGIN_SENSITIVE
    → <V>_UNCHECKED · `variant_flag` · PRE-design-17) ⑥ §7-1 한정어 ⑰ ⑱ (`QUALIFIERS` 18)
  · ★ RI (10-21 · §5-6 ③ "변이 판정 = NOT_COMPUTED (… 멈춤) → <V>_UNCHECKED" · 1저자 Q2 범위 = 코드를 등록에 맞춤) — 감도 변이 단계가 멈추면
    (STOPPED) 그 변이 판정 = NOT_COMPUTED → <V>_UNCHECKED (차단 · 주 판정은 그대로 계산 · `variant_stage_stopped`) · 주 판정 단계의 멈춤 = 판정
    전체 NOT_COMPUTED (INPUT_STAGE_STOPPED · `stopped_stage_rejects_verdict`) · 판정 입력 검사는 멈춘 변이 단계에도 그대로
★ PF2 (10-22 · 사전 리뷰 2 회차 · 1저자 10-22 Q1 (다) · Q2 · Q3 권고대로):
  · B (PRE2-design-01 · Q2) — 순서 = S0 단계 1 → ⑥ 숫자 탐침 (SBE · σ 봉인) → 계획 하나 봉인 → S0 단계 2 (DBE) → R 런.  사다리가
    `--s0-stage2-report` (단계 2 보고) 의 봉인 계획 해시 (`plan.r_plan.sha256` = R 계획 · `plan.sha256` = S0 계획) 를 지금 두 계획과 **정확히**
    대조 · 다르면 멈춤 (`S0_REPORT_MISMATCH`) · 예측 · 판정은 요약 기록으로 같은 함수 (`s0_stage2_problem`) 로 다시 대조
"""
import argparse
import glob
import hashlib
import json
import math
import os
import re
import shlex
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import run_contract as RC                                    # noqa: E402 — 계약 정본 (사본 없음)
import ca_ext_svcf as SVCF                                   # noqa: E402 — SV 반사실 증거 꼴 (비 · 상태 · numpy 없음)

TOOL = 'rint_r_chain'
SCHEMA = 'rint-r-chain-v2'                                   # ★ 3판 — v1 (2판 규칙) 요약과 섞지 않는다
REGISTRATION_DEFAULT = HERE.parent / 'docs' / 'reviews' / 'rint_carbon_additive_registration_R_draft_20261020.md'

# ═════════════════════════ 등록 R 의 숫자 — 한 곳 · 이름 (값 = 등록 정본 · 시험 X05 가 문서와 대조) ═════════════════════════
TARGET_SBE_MS = 1.63                 # §0 · §3 — SBE DC 1.63 mS/cm (보정 표적 · 판정선 · 결과 보고 옮기지 않는다)
EXP_DBE_MS = 4.68                    # §0 · §5 — DBE DC 4.68 mS/cm (holdout · 판정에 한 번)
CUR_GEN_DBE_MS = 1.8877              # §5-2 — 현 세대 SBE 보정 모형의 DBE (G0 의 기준 · 보고에 나란히)
CUR_GEN_SIGMA_STAR_DBE = 2.618       # §1 · §8 — 현 세대 DBE σ*_VGCF S/cm (보고만 · 맞추지 않는다)
EXP_RATIO = 2.86                     # §0 — 실험 비 DBE/SBE (보고만)
G0 = math.log(EXP_DBE_MS / CUR_GEN_DBE_MS)   # §5-2 G0 = ln(4.68/1.8877) = 0.908
GRADE_INFORMATIVE_MAX = G0 / 2.0     # §5-2 W ≤ G0/2 = 0.454 = 정보 있음 (비교척도 · 신뢰수준 아님)
GRADE_WEAK_MAX = G0                  # §5-2 W ≤ G0 = 0.908 = 약함 · 넘으면 정보 없음
SENS_SHIFT_FRAC_G0 = 0.1             # §5-6 끝이 0.1 G0 (= 0.091) 넘게 움직이면 크기 보고
CONFIRM_TOL = 0.02                   # ±2 % — §3-1 EDGE · §3-2 확인 런 · §3-2b 끝 표적 T± = 1.63 × (1 ± 0.02)
E_MIN = CONFIRM_TOL / math.log(math.sqrt(10.0))   # §3-2 e_min = 0.02 / ln √10 ≈ 0.017 — ★ 3판: 국소 진단 (보고 · 멈추지 않는다)
TAU_MONO = 1e-3                      # §3-2 비단조 · §4-1 같은 P 일관 (ln σ 차 · 단위 불변)
NEIGHBOR_LOG10_MAX = 0.5             # §3-2 끼는 이웃 비 ≤ 10^0.5
LADDER_START_LOG10 = (4.0, 6.0, 8.0)  # §3-2 다음 점 {1e4, 1e6, 1e8} Ω
LADDER_EXT_LOG10 = 2.0               # §3-2 끼지 않으면 같은 쪽으로 ×100
MAX_CONFIRM = 2                      # §3-2 확인 런 최대 두 번
ORIGIN_SBE_MAX = 0.02                # §3-3 SBE arm 0 · 1 · 2 의 ln(max/min) ≤ 0.02 (R_j,0)
ORIGIN_DBE_FRAC_W = 0.1              # §4-2 DBE 모서리 · R 마다 arm 0 · 1 · 2 의 ln(max/min) ≤ 0.1 W
SIG_DIGITS = 3                       # §3-2 R_j,0 = 유효숫자 3 자리 (끝 = 반올림 없음 · §3-2b)

# ═════════════════════════ 런 규약 (등록 R §10 COMMON · 머리 줄 7 · §2) ═════════════════════════
SBE_KIT = 'kit_SBE_vgcf100'
DBE_KIT = 'kit_DBE_sdcp1um_vgcf100'
LAWS = ('P0', 'P1')                  # PTFE–접합 법칙 끝 (N2)
CS = ('0', '1')                      # SDCP 접점 c 두 끝 (N11)
LADDER_C = '0'                       # 사다리 = c 0 (SBE 에 SDCP 없음 · c 무관 → 예측 단계가 SBE c 1 비트 같음을 검사)
VOX_MAIN, VOX_GRID = 0.15, 0.125     # §9 격자 단계 = vox 0.125
VGCF_D_UM = 0.15                     # 직경 보존 기준 지름 (러너 D_REF · 설계 §1-2 #2 · #3)
FIBRE_BULK, FIBRE_BULK_DIV10 = 1e4, 1e3   # §2 Endo 흑연화 1e4 S/cm · FIBRE 감도 ÷ 10
ENV_FIXED = {'VOX': '0.15', 'SDCP_SPHERE_D': '0.30', 'PTFE_STAMP': 'face_alpha', 'BRIDGE_UM': '0.48',
             'SIGMA_AM_S_OVERRIDE': '0.0041', 'SIGMA_SDCP_OVERRIDE': '256.6', 'SIGMA_FIBRE_BULK': '1e4',
             'LEAN': '2', 'CJUNC': '1'}
MAN_FIXED = {'bridge_um': 0.48, 'sdcp_sphere_d_um': 0.30, 'sigma_am_s_S_cm': 0.0041, 'sigma_sdcp_S_cm': 256.6}
L_PAR_UM, R_PORT_UM = 0.30, 0.30     # §2-1 지금 고정 (물리 단위) — S0 계획 values_um.L_par · r_port 와 대조 (두 계획 대조)
VARIANTS = ('FIBRE', 'UNREG', 'GRID', 'SVORDER')   # §5-6 필수 감도
VARIANT_ENV = {'FIBRE': {'SIGMA_FIBRE_BULK': '1e3'}, 'UNREG': {'CJUNC_UNREG_LAW': 'fused'}, 'GRID': {'VOX': '0.125'},
               'SVORDER': {'SDCP_YIELD_VGCF': '1'}}
LIMIT_RJ = {'floor': 'inf', 'ceiling': '0'}   # §3-1 R_j → ∞ (바닥 · 간선 없음) · R_j → 0 (천장 · 정확 축약) — 러너 env 꼴
#: ★ Z3 — 극한 env → protocol · 영수증 요청의 표지 (정본 낱말 = `ca_ext_cjunc.RJ_LIMITS` · 시험 X07 이 대조 · 이 모듈은 numpy 없이 뜬다)
LIMIT_MARK = {'inf': 'inf', '0': 'zero'}
#: ★ Z3 — §3-3 · §4-2 origin 검사 팔 (러너 `ARM_LIST` · a0 = 앞 런의 값 그대로 · 다시 돌지 않는다)
ORIGIN_ARMS = (1, 2)
#: 러너 · 정본 check_arm 의 backend (등록 R §10 = GPU · 러너 기본값과 같다 — 사슬이 env 로 정한다 · 부모 셸 값은 지운다)
EXPECT_BACKEND = 'gpu'
LEAN2_PLAN = {'electronic': True, 'ionic': False, 'thermal': False, 'pore': False, 'collector': False}
LEAN2_RECEIPTS = {'electronic_main': ('applied', 'absent_geometry'), 'electronic_wetted': ('disabled',),
                  'electronic_bare': ('disabled',), 'ionic': ('disabled',)}   # 설계 §7 LEAN 표 (LEAN 2 · 양의 해)
#: ★ 3판 — R 런 계획 v2 = v1 칸 일곱 + 결과 전 등록 숫자 넷 (등록 R §3-2 점 수 상한 · §3-2b 역상 폭 상한 · §5-6 SV 반사실 문턱 · 범위)
PLAN_SCHEMA = 'rint-r-plan-v2'
PLAN_KEYS = ('schema', 'len_law', 'unreg_law', 's_min_um', 'tol_ff_um', 'step3_rtol', 'p2_extra',
             'max_ladder_points', 'calib_rj_ratio_max', 'sv_cf_threshold', 'sv_cf_scope')
#: 결과 전 등록 숫자 (⬜) — 하나라도 null 이면 사슬이 멈춘다 (σ 런 전 · ★ Q-G: SV 문턱이 ⬜ 인 채로 DBE 단계에 가지 않는다)
PLAN_REGISTERED_NUMBERS = ('max_ladder_points', 'calib_rj_ratio_max', 'sv_cf_threshold', 'sv_cf_scope')
PLAN_NO_CAP = 'none'                 # calib_rj_ratio_max = 'none' — "상한을 두지 않기로" 를 등록한 값 (§3-2b ④ · 실제 양끝을 그대로 전파)
SV_CF_SCOPES = ('R_j0', 'all3')      # §5-6 SV 행 — DBE 네 모서리 × R_j,0 · × 세 R (⬜ 1저자)
PLAN_UNREG_MAIN = 'cut'              # 설계 §1-2 #12 — 주 cut · 감도 fused (UNREG)
S0_PLAN_SCHEMA = 'ca-cjunc-plan-v1'  # §2-1 · §10-2 ⑪ — S0 단계 1 계획 (`scripts/ca_s0_census.py` · 정본 = 그 모듈)
#: ★ PF2 B (10-22 · 사전 리뷰 2 회차 PRE2-design-01 · 1저자 Q2 권고대로) — S0 단계 보고 (`ca_s0_census` · `s0_stage<n>_<킷>.json`) 의 schema
#   (= ca_s0_census.SCHEMA · 시험 B09 가 대조 · 이 모듈은 numpy 없이 뜬다)
S0_REPORT_SCHEMA = 'ca-s0-census-v2'
#: 러너가 읽는 env (부모 셸에서 물려받으면 지운다 — 사슬이 런마다 정확히 정한다 · 지운 이름은 요약에)
ENV_SCRUB_RE = re.compile(r'^(SIGMA_|SDCP_|PTFE_|CJUNC|STEP3_)')
ENV_SCRUB_NAMES = frozenset({'VOX', 'BRIDGE_UM', 'ARMS', 'ARM_LIST', 'KITS', 'OUTDIR', 'LEAN', 'FIBRE_STAMP', 'MPM_PERIODIC_SIGMA',
                             'P2_EXTRA', 'EXPECT_BACKEND', 'EXPECT_PROTOCOL', 'P2_SCR', 'P2_SELF', 'P2_ENV_GUARD_ONLY'})
ENV_FORBIDDEN = ('SIGMA_VGCF_OVERRIDE',)   # §10 — 있으면 멈춤 (지워서 넘어가지 않는다)

# ═════════════════════════ 판정 이름 · 표지 · 문장 ═════════════════════════
CALIB_ORDER = ('CALIB_IMPOSSIBLE', 'CALIB_EDGE', 'CALIB_UNIDENTIFIED', 'CALIB_UNCONFIRMED', 'CALIB_NONMONOTONE',
               'CALIB_LADDER_EXHAUSTED', 'NOT_COMPUTED')   # §3-2c — 판정 전체 이름 (이 순서로 하나)
REGISTERED_OUTCOMES = frozenset(CALIB_ORDER)
GRADES = ('PASS_INFORMATIVE', 'CONSISTENT_WEAK', 'UNINFORMATIVE', 'GAP_ENVELOPE_ONLY', 'FAIL')   # §5-5 (계산기 상태 이름)
#: §7-1 (3판 · 판정문 §5-3 문안 그대로) — PASS_INFORMATIVE 이고 차단 표지가 하나도 없을 때만
SENTENCE_PASS = ('SBE 측정 한 점으로 각 법칙의 내부 접합 저항을 보정하였다. 사전에 고정한 시나리오와 보정 허용집합의 계산 결과를 이미 알려진 '
                 'DBE 측정값과 비교하였다. 모형 종류와 시나리오 방향은 해당 DBE 값 및 기존 빗나감을 알고 선정했으므로, 이 비교는 독립 '
                 'holdout 검증이나 접합 물성의 식별이 아니다.')
SENTENCE_WEAK = '넓은 시나리오 구간 안에 들었다'                                  # §5-5 CONSISTENT_WEAK ("예측했다" 금지)
SENTENCE_GAP = '어느 법칙의 허용집합에도 포함되지 않았으나 전체 envelope 에는 포함'   # §5-5 · 판정문 §5-3 (GAP_ENVELOPE_ONLY)
#: ★ 4판 (Q2-4 · 등록 R 4판 §5-5b 결정표 · PRE-design-09 · R4-Q7) — 칸 글자 (등록 표 그대로 · 시험 X05b · U07 이 문서 · 독립 조립과 대조)
SENTENCE_UNINF = '예측 주장 없음 (구간이 현 세대 빗나감보다 넓다)'                     # §5-5b UNINFORMATIVE (§5-5 표의 짧은 꼴 아님)
SENTENCE_FAIL = '빗나감 d · d/G0 · 방향 · §8 보고 (해석 금지 §8)'                      # §5-5b FAIL
SENTENCE_CALIB = '판정 없음 — 법칙별 이름 · 사유 · 바닥 · 천장 · e · 끝 후보 보고'      # §5-5b CALIB_*
SENTENCE_NC = '판정 없음 — 사유 (상태 · 멈춤 코드) 보고'                               # §5-5b NOT_COMPUTED (사슬 멈춤 포함)
SENTENCE_Q18 = 'P 는 두 끝만 등록했다 (사이 감쇠는 모형 밖)'                           # §5-1 · §7-1 ⑱ (GAP 문장에 붙인다)
SENTENCE_PASS_HELD = '계산기 판정 이름 `PASS_INFORMATIVE` · 차단 표지 {} — 판정 문장 보류'   # §5-5b PASS + 차단 표지 ({} = <목록>)
SENTENCE_BLOCKED = '(차단 표지 {})'                                                    # §5-5b 그 밖 + 차단 표지 ({} = <목록>)
SENTENCE_POINT = '점 구간'                                                             # §5-5b 점 구간이면 덧붙임 (p = null)
SENTENCE_SENS = '감도 미완료'                                                          # §7-1 ⑰ (감도 변이를 다 돌리기 전 결과 문장마다)
SENTENCE_JOIN = ' · '                     # 덧붙임 · <목록> 의 이음 (★ 구현 꼴 — 등록 문장은 이음 글자를 정하지 않았다 · 보고 "결정 필요")
VERDICT_NOTE = ('판정 이름 (PASS_INFORMATIVE · CONSISTENT_WEAK · …) = 계산기 상태 이름 — 과학적 검증 성공이 아니다 · 독립 holdout 검증 아님 '
                '(등록 R §5-5 · §7-1 · 판정문 §5-3)')
GRID_SENTENCE = 'not_computed'       # §9 '격자 의존이 현 세대보다 작았다' — 현 세대 vox 0.125 대조는 이 사슬 밖 (그 문장 금지 · GRID 표지와 별개)
#: §5-6a — 차단 표지 **닫힌 집합** (이 목록 밖 이름은 차단하지 않는다 · 하나라도 있으면 §7-1 문장 금지 · 판정 이름은 그대로)
BLOCKING_FLAGS = ('FIBRE_SENSITIVE', 'UNREG_SENSITIVE', 'GRID_SENSITIVE', 'SVORDER_SENSITIVE', 'FIBRE_UNCHECKED', 'UNREG_UNCHECKED',
                  'GRID_UNCHECKED', 'SVORDER_UNCHECKED', 'CALIB_ORIGIN_SENSITIVE', 'SV_DEPENDENT', 'SV_UNCHECKED')
#: §5-6a — 보고 한정어 범주 (늘 붙는다 · 차단하지 않는다 · 미검증 사실을 지우지 않는다)
REPORT_CATEGORY = 'ASSUMED_UNVALIDATED'
ASSUMED_UNVALIDATED = ('ptfe_diameter_convention (DIA_UNCHECKED · Ø0.248 rope · 규약 선택)', 'sdcp_vgcf_contact_resistance_zero (SV 융합)',
                       'ptfe_impermeable', 'sdcp_cluster_fill_0.64', 'sdcp_am_attach_0.5')
#: §7-1 필수 한정어 ①–⑱ (⑨ = PTFE 지름 규약 = 보고 범주 ASSUMED_UNVALIDATED · ★ 4판 (Q2-6) ⑰ 감도 미완료 (§10-4 · 10-31 판정 = 주 판정만) ·
#  ⑱ P 는 두 끝 (P0 · P1) 만 등록했다 — 사이 감쇠는 모형 밖 (§5-1 · GAP_ENVELOPE_ONLY 는 이 선언에 달린다))
QUALIFIERS = ('Q1_holdout_known_one_sided', 'Q2_Rj0_model_internal', 'Q3_scenario_ends_not_material', 'Q4_two_electrode_n1',
              'Q5_grid_flag', 'Q6_sensitivity_flags', 'Q7_S1P_pellet', 'Q8_SV_contact_zero', 'Q9_ptfe_diameter_convention',
              'Q10_junction_geometric_proximity', 'Q11_s_min_development_choice', 'Q12_long_contact_distributed_v0',
              'Q13_sv_counterfactual_ratio_threshold', 'Q14_convergence_empirical_abcd_target_cert',
              'Q15_recompaction_generation_switch', 'Q16_calibration_set_outer_enclosure',
              'Q17_sensitivity_incomplete', 'Q18_P_two_ends_only')
#: §5-7 결정표 = ★ 4판 (Q2-4) 등록 R 4판 §5-5b 표 그대로 — 판정 이름 → (차단 표지 없음 칸, 차단 표지 있음 칸 꼴 · '{}' = <목록> (붙은 차단 표지
#  이름 전부 · 사전 순)) · CALIB_* · NOT_COMPUTED 의 차단 표지 칸 = "해당 없음" (None → 왼쪽 칸 그대로) · 점 구간 · ⑰ 덧붙임 = `decide_sentence`.
#  상태 (§5-0) 는 판정 이름을 통해서만 들어오고, 상태 ↔ 이름 짝은 STATE_VERDICTS 로 닫는다 (짝이 안 맞으면 구현 결함 = 예외).
_GAP_Q18 = SENTENCE_GAP + SENTENCE_JOIN + SENTENCE_Q18          # §5-5b GAP 칸 = 판정문 §5-3 문안 + ⑱
DECISION = {'PASS_INFORMATIVE': (SENTENCE_PASS, SENTENCE_PASS_HELD),
            'CONSISTENT_WEAK': (SENTENCE_WEAK, SENTENCE_WEAK + ' ' + SENTENCE_BLOCKED),
            'UNINFORMATIVE': (SENTENCE_UNINF, SENTENCE_UNINF + ' ' + SENTENCE_BLOCKED),
            'GAP_ENVELOPE_ONLY': (_GAP_Q18, _GAP_Q18 + ' ' + SENTENCE_BLOCKED),
            'FAIL': (SENTENCE_FAIL, SENTENCE_FAIL + ' ' + SENTENCE_BLOCKED),
            **{c: (SENTENCE_CALIB, None) for c in CALIB_ORDER if c != 'NOT_COMPUTED'},
            'NOT_COMPUTED': (SENTENCE_NC, None)}
STATE_VERDICTS = {'positive': frozenset(GRADES), 'point': frozenset({'PASS_INFORMATIVE', 'FAIL'}),
                  'extended': frozenset({'UNINFORMATIVE', 'GAP_ENVELOPE_ONLY', 'FAIL'}), 'calib': frozenset(CALIB_ORDER)}
#: ★ 4판 (10-21 · 1저자 Q1 "권고대로" · 등록 R 4판 §5-0 ①–③ · §4-2 ③ · R4-Q5) — 이 등록의 풀이 상태 셋 ↔ 생산자 기록 상태
#   (`run_contract.next_gen_state` · 정본): 단락 (ELECTRODE_SHORT · J11) = 생산자 미게시 (`run_contract.conv_cert_problem` — 게시 가능 =
#   POSITIVE_SOLVED · VALID_ZERO_TOPOLOGY 뿐) → 그 런 = NOT_COMPUTED · 사유 = 상태 이름 (σ +∞ 로 판정에 오지 않는다 · 다른 멈춤 이름
#   (RUNNER_RC · CA_EXT_RECORD …) 으로 흐리지 않는다 — 기록 자체는 온전해야 러너가 옮기고 사슬이 이 이름을 남긴다).
SHORT_STATUS = 'ELECTRODE_SHORT'          # = step3_conv_cert.STATUS_SHORT (시험 Z07 이 대조 · 이 모듈은 numpy 없이 뜬다)
REG_STATES = {'positive': ('POSITIVE_SOLVED', None), 'zero': ('VALID_ZERO_TOPOLOGY', None), 'short': ('NOT_COMPUTED', SHORT_STATUS)}
#: ★ 4판 (Q1) — 예측 단계의 등록 결과 (사다리의 REGISTERED_OUTCOMES 와 같은 뜻 · 판정이 원 팔에서 다시 계산한다) · 그 밖 멈춤 = STOPPED
PREDICT_OUTCOMES = frozenset({'NOT_COMPUTED'})


def stopped_stage_rejects_verdict(s):
    """★ RI (10-21 · 등록 R 4판 §5-6 ③ · 1저자 Q2 범위 = 코드를 등록에 맞춤) — 멈춘 단계 (STOPPED · 등록 결과 이름이 아닌 멈춤) 가 판정 전체를
    거부하나: **주 판정 단계만** (판정 전체 NOT_COMPUTED · INPUT_STAGE_STOPPED · §5-5 사슬 멈춤 행 그대로).  감도 변이 단계의 멈춤 = 그 변이 판정
    NOT_COMPUTED → <V>_UNCHECKED (`variant_stage_stopped` · 4판 사슬 = 변이 단계도 판정 전체 거부)."""
    return s.get('status') == 'STOPPED' and s.get('variant') is None


def variant_stage_stopped(s):
    """★ RI (§5-6 ③ "변이 판정 = NOT_COMPUTED (풀이 · 증서 실패 · 단락 · 멈춤) → <V>_UNCHECKED") — 멈춘 감도 변이 단계 (사다리 · 예측) = 결과 없음:
    원 팔에서 다시 계산하지 않고 그 법칙 · 예측 = NOT_COMPUTED (`judge_set` → 변이 판정 NOT_COMPUTED → `variant_flag` ③).  판정 입력 검사 (계획 ·
    S0 · 등록 숫자 · 코드 핀 · 주 예측 묶음 · 예측 ↔ 사다리) 는 멈춘 단계에도 그대로 (그 기록이 없으면 그 검사의 멈춤 = 판정 전체 NOT_COMPUTED)."""
    return s.get('status') == 'STOPPED' and s.get('variant') is not None

STOPS = {
    'OUTDIR_NOT_EMPTY': '출력 폴더가 이미 있고 비어 있지 않다 (러너 SKIP 캐시 · 옛 산출물)',
    'NOT_REGISTERED': '인자가 등록 R 과 다르다 (표적 · 법칙 · 킷 · 변이)',
    'ENV_SIGMA_VGCF_OVERRIDE': 'env 에 SIGMA_VGCF_OVERRIDE (복셀값 직접 · 다음 세대 판정 런 금지)',
    'REGISTRATION_UNREADABLE': '등록 문서 · §2-1 계획 해시 줄을 못 읽는다',
    'PLAN_HASH_UNREGISTERED': '등록 §2-1 계획 해시가 아직 없다 (⬜)',
    'PLAN_HASH_MISMATCH': '계획 해시 ≠ 등록 §2-1 개정값',
    'PLAN_INVALID': '계획 파일 꼴이 틀렸다',
    'PLAN_NUMBER_UNREGISTERED': 'R 계획의 결과 전 등록 숫자 (점 수 상한 · 역상 R 비 상한 · SV 반사실 문턱 · 범위) 가 아직 null (⬜) — σ 런 없음 (Q-G)',
    'S0_PLAN_INVALID': 'S0 계획 파일 꼴 · 식 · 정준 바이트가 틀렸다 (`ca_s0_census.check_plan`)',
    'S0_PLAN_HASH_UNREGISTERED': '등록 §2-1 S0 계획 해시가 아직 없다 (⬜)',
    'S0_PLAN_HASH_MISMATCH': 'S0 계획 해시 ≠ 등록 §2-1 개정값',
    'PLAN_CROSS_MISMATCH': '두 계획 대조 실패 (R 계획 ↔ S0 계획 ↔ 사슬 상수 · 등록 R §2-1 · §10-2 ⑪)',
    'S0_REPORT_MISMATCH': 'S0 단계 보고를 못 읽거나 꼴이 틀렸다 · 단계 2 보고가 봉인한 계획 해시 (R 계획 · S0 계획) ≠ 지금 계획 (★ PF2 B · Q2 — '
                          'DBE 열람 전 계획 하나 · 바꾸려면 새 등록 · 등록 R §2-1 · §2-1b · §11 ④)',
    'MAIN_NOT_DONE': '감도 단계인데 주 판정 단계 (사다리 둘 · 예측) 가 끝나지 않았다 · 묶음이 다르다 (--after-main · Q-F)',
    'MAIN_BINDING': '판정 입력의 감도 단계가 묶인 주 예측 ≠ 판정 입력의 주 예측 (Q-F)',
    'KIT_MISSING': '킷 폴더 · 러너가 없다',
    'RUNNER_RC': '러너 rc ≠ 0',
    'REJECTED_MARKER': '러너 기각 기록 .rejected_*',
    'ARM_JSON_COUNT': '팔 JSON 개수 · 번호 · 이름 ≠ 요청',
    'ARM_UNREADABLE': '팔 JSON 을 못 읽는다',
    'ARM_CONTRACT': '러너 팔 계약 (check_arm) 실패',
    'GENERATION': 'physics_protocol_id 가 p3ca- 아님 (unknown:* 포함) · 저장 ≠ 다시 계산',
    'CA_EXT_RECORD': 'ca_ext_record_ok 실패',
    'MANIFEST_MISMATCH': '매니페스트 · 영수증 ≠ 요청 (σ · vox · 브리지 · PTFE · SDCP 구 · ca_ext 지문 · rtol · SV 반사실 요청)',
    'RECEIPT_LEAN': '솔브 영수증 ≠ LEAN 2 표 (설계 §7 · 해 상태별)',
    'PTFE_CELLS_OBSERVED': 'face_alpha 런의 ptfe_cells_observed > 0',
    'SID_GRID': 'sid 격자 지문이 같은 킷 · 같은 래스터 런 사이에서 다르다 (off 격자 대조)',
    'SAME_P_CONSISTENCY': '같은 P 일관 검사 위반 (SBE c no-op · DBE c 순서)',
    'TIME_LIMIT': '시간 상한',
    'DUPLICATE_RUN': '같은 킷 · 같은 계획 두 번',
    'INPUT_SHA_MISMATCH': '판정 입력 sha256 ≠ 런 산출',
    'INPUT_MISSING': '판정 입력이 모자란다',
    'INPUT_STAGE_STOPPED': '주 판정 입력 단계가 멈춘 채다 (감도 변이 단계의 멈춤 = 그 변이 <V>_UNCHECKED · §5-6 ③)',
    'INPUT_NOT_STAGE': '판정 입력 폴더에 단계 요약이 없다',
    'LADDER_NOT_CALIBRATED': '사다리가 보정되지 않았다 (예측 안 함)',
    'LADDER_SET': '사다리 묶음이 법칙 끝 둘이 아니다',
    'PREDICT_LADDER_MISMATCH': '예측이 쓴 사다리 ≠ 판정 입력 사다리',
    'REPLAY_MISMATCH': '원 팔 JSON 에서 다시 계산한 결정 ≠ 기록',
    'CODE_PIN_MISMATCH': '단계마다 코드 (사슬 · 러너) 가 다르다',
    **{k: k for k in CALIB_ORDER},
}


class Stop(Exception):
    """구조화 멈춤 — code (STOPS 이름) · cause (원인 칸 · σ 를 가린 문장) · run (그 런 이름) · ★ 4판 (Q1) reason = 구조화 사유 (등록 문장이
    이름을 정한 것만 — 지금 = 단락의 상태 이름 `ELECTRODE_SHORT` · 그 밖 None)."""

    def __init__(self, code, cause, run=None, reason=None):
        super().__init__(f'{code}: {cause}')
        self.code, self.cause, self.run, self.reason = code, str(cause), run, reason

    def record(self):
        return {'code': self.code, 'what': STOPS.get(self.code, self.code), 'cause': self.cause, 'run': self.run, 'reason': self.reason}


class RealContract:
    """정본 계약 위임 — 사슬은 이 계약을 다시 적지 않는다 (규율 ① · `run_contract` 머리말).  시험은 이 자리에 가짜 인지 계약을 넣는다."""

    def arm_problem(self, path, receipt):
        """러너가 팔을 OUTDIR 로 옮기기 전에 거는 검사와 같은 함수 (`sr01_stamp_compare.check_arm`) — 쓴 뒤 바뀐 팔을 다시 잡는다."""
        import sr01_stamp_compare as SC
        return SC.check_arm(path, 'segment', expect_backend=EXPECT_BACKEND, receipt=receipt)

    def ca_ext_record(self, man):
        return RC.ca_ext_record_ok(man)


# ═════════════════════════ 작은 도구 ═════════════════════════
def canon_bytes(obj):
    return (json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True, allow_nan=False) + '\n').encode('utf-8')


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def sha_mismatch(path, want):
    """판정 입력 sha256 대조 → 문제 | None (§10 멈춤 · 판정 단계 입력 sha256 ≠ 런 산출)."""
    try:
        got = sha256_file(path)
    except OSError as e:
        return f'{Path(path).name} 를 못 읽는다 ({type(e).__name__})'
    return None if got == want else f'{Path(path).name} sha256 {got[:12]}… ≠ 기록 {str(want)[:12]}…'


def sig3(x):
    """유효숫자 3 자리 (§3-2 R_j,0) → float."""
    return float(f'{float(x):.{SIG_DIGITS}g}')


def rj_key(x):
    """R_j → 러너 env · 요약 문자열 (정규 · 무손실 repr) · 극한 = 'inf' · '0'."""
    x = float(x)
    if math.isinf(x) and x > 0:
        return 'inf'
    if x == 0.0:
        return '0'
    if not (math.isfinite(x) and x > 0):
        raise ValueError(f'R_j {x!r}')
    return repr(x)


def rj_float(key):
    return math.inf if key == 'inf' else float(key)


def disp_rj(key):
    return {'inf': '∞', '0': '0'}.get(key) or f'{float(key):.4g} Ω'


def interp_lnln(Ra, sa, Rb, sb, target):
    """§3-2 ln σ ↔ ln R_j 직선 보간 → target 을 지나는 R_j (양의 유한 σ 끼리만 — 부르는 쪽이 거른다)."""
    t = (math.log(target) - math.log(sa)) / (math.log(sb) - math.log(sa))
    return math.exp(math.log(Ra) + t * (math.log(Rb) - math.log(Ra)))


def elasticity(Ra, sa, Rb, sb):
    """§3-2 할선 탄성 e = |Δ ln σ / Δ ln R_j| — ★ 3판: 국소 진단 (보고 · e/e_min) · 식별 판정이 아니다 (RCA-01)."""
    return abs((math.log(sb) - math.log(sa)) / (math.log(Rb) - math.log(Ra)))


def registration_state(state):
    """★ 4판 (Q1 · 등록 R 4판 §5-0) — 생산자 기록 상태 (`run_contract.next_gen_state` 의 첫 값) → (이 등록의 풀이 상태, 사유).
    positive → POSITIVE_SOLVED · zero → VALID_ZERO_TOPOLOGY · short → NOT_COMPUTED (사유 ELECTRODE_SHORT · 생산자 미게시) · 상태가 안 섬
    (None) · 모르는 상태 → NOT_COMPUTED (사유 None — 그 상태 문장은 멈춤 원인 칸에)."""
    return REG_STATES.get(state, ('NOT_COMPUTED', None))


# ── §5-0 확장 실수 [0, +∞] (0 = VALID_ZERO_TOPOLOGY) — 모든 비교 = ln 차 (단위 불변 · RCA-13) · ★ 4판 (Q1): 단락은 +∞ 로 판정에 오지 않는다
#    (NOT_COMPUTED) — 아래 도구는 +∞ 를 다룰 수 있게 둔다 (값 쪽 일반성 · 판정 입력으로는 0 만 온다) ──
def ln_diff(a, b):
    """ln b − ln a 를 확장 실수에서 — 같은 끝 (0·0 · ∞·∞) = 0 · 0 → 양 · 양 → ∞ = +∞ · 그 반대 = −∞."""
    a, b = float(a), float(b)
    if a == b:
        return 0.0
    if a == 0.0 or b == math.inf:
        return math.inf
    if b == 0.0 or a == math.inf:
        return -math.inf
    return math.log(b) - math.log(a)


def ln_spread(vals):
    """ln(max/min) 을 확장 실수에서 — 다 같으면 0 (0 · +∞ 끼리 포함) · 0 이나 +∞ 가 다른 값과 섞이면 +∞."""
    vals = [float(v) for v in vals]
    return ln_diff(min(vals), max(vals))


def mean_ext(vals):
    """산술 평균 (8 팔) — +∞ 가 하나라도 있으면 +∞ (빼기 없음 · NaN 없음)."""
    vals = [float(v) for v in vals]
    return sum(vals) / len(vals)


def outside_band(s, X, lo, e=0.0):
    """§3-2b 끝 조건 — lo 끝: σ ≥ T⁺ (허용집합 아래쪽 밖) · hi 끝: σ ≤ T⁻ (위쪽 밖) · 확장 실수 그대로.
    ★ 4판 (Q2-2 · §3-2b ③″ · PRE-design-12) 보호 띠 — 판독 구간 [σ(1 − e), σ(1 + e)] (e = 그 런 증서의 보장 오차 `err_rel`) 이 띠 바깥에
    **다 있을 때만** 바깥 (lo: σ(1 − e) ≥ T⁺ · hi: σ(1 + e) ≤ T⁻) · 걸치면 모호 = False (보수 쪽 — 끝을 바깥으로 옮긴다) · e = 0 = 3판 그대로."""
    return s * (1.0 - e) >= X if lo else s * (1.0 + e) <= X


def edge_hit(s, e, T, tol=CONFIRM_TOL):
    """§3-1 EDGE (1.63 이 바닥 또는 천장의 2 % 안 = |σ/T − 1| ≤ 2 %) — ★ 4판 (Q2-2 · §3-2b ③″) 보호 띠: 판독 구간 [σ(1 − e), σ(1 + e)] 에서
    T 에 가장 가까운 점이 띠 안이면 EDGE (구간이 T 를 품으면 EDGE · 걸치면 모호 = EDGE 로 센다 = 보수 쪽) · e = 0 = 3판 식 그대로 · 확장 실수
    (σ 0 = 바닥 zero 정상 · EDGE 아님)."""
    a, b = s * (1.0 - e), s * (1.0 + e)
    if a <= T <= b:
        return True
    x = b if b < T else a
    return abs(x / T - 1.0) <= tol


def arm_err(rec):
    """★ 4판 (Q2-2) — 팔 기록의 판독 보장 오차 e (`err_rel` · read_run 이 증서에서 다시 계산) → float (유한 ≥ 0) · 없으면 멈춤 (보호 띠를 잴 수
    없다 — 0 으로 두면 보수 쪽이 아니다)."""
    e = rec.get('err_rel') if isinstance(rec, dict) else None
    if isinstance(e, bool) or not isinstance(e, float) or not math.isfinite(e) or e < 0.0:
        raise Stop('ARM_UNREADABLE', f'판독 보장 오차 err_rel {e!r} — 유한 0 이상 float 이어야 (§3-2b ③″ 보호 띠 · 증서 ⓓ target_err_bound_rel)')
    return e


def sbe_origin_ok(vals):
    """§3-3 SBE arm 0 · 1 · 2 → (통과?, ln(max/min)) — 확장 실수."""
    sp = ln_spread(vals)
    return sp <= ORIGIN_SBE_MAX, sp


def dbe_origin_ok(vals, W0, states=None, w_pos=None):
    """§4-2 DBE 모서리 · R 마다 arm 0 · 1 · 2 → (통과?, ln(max/min)) — 문턱 0.1 W (W = arm 0 값들로 낸 첫 폭).
    ★ 4판 (Q2-3 · §4-2 PRE-design-10 · R4-Q4) — ① 세 origin 의 상태 (`states` · POSITIVE_SOLVED ↔ VALID_ZERO_TOPOLOGY) 가 서로 다르면 = 넘음
    ② 상태는 같은데 W 가 +∞ (다른 모서리의 zero) 또는 0 (점 구간) 이면 문턱의 W = W₊ (`w_pos` = arm 0 의 양수 값들만으로 낸 폭 · 없으면 0) ·
    W₊ = 0 이면 문턱 0 (산포가 조금이라도 있으면 넘음 = 보수 쪽) ③ 단락 (ELECTRODE_SHORT) 은 NOT_COMPUTED 라 여기 오지 않는다."""
    sp = ln_spread(vals)
    if states is not None and len(set(states)) > 1:
        return False, sp
    W = W0 if (0.0 < W0 < math.inf) else (0.0 if w_pos is None else w_pos)
    return sp <= ORIGIN_DBE_FRAC_W * W, sp


def w_pos_of(vals):
    """★ 4판 (Q2-3 · §4-2 ②) — W₊ = arm 0 의 양수 값들만으로 낸 폭 ln(max/min) (양수 값이 없으면 0 · 하나면 0)."""
    pos = [float(v) for v in vals if float(v) > 0.0]
    return ln_spread(pos) if pos else 0.0


def _ln_dist(x, lo, hi):
    """x 에서 구간 [lo, hi] 까지 ln 거리 (안 = 0 · 유한 끝이 없으면 +∞) 와 방향 ('inside' · 'below' = x 가 아래 · 'above' = x 가 위)."""
    if lo <= x <= hi:
        return 0.0, 'inside'
    if x < lo:
        return (math.log(lo / x) if lo < math.inf else math.inf), 'below'
    return (math.log(x / hi) if hi > 0.0 else math.inf), 'above'


def grade_W(W):
    """§5-2 등급 (양의 구간 · 4.68 ∈ U) — W ≤ G0/2 정보 있음 · ≤ G0 약함 · 넘으면 정보 없음."""
    return 'PASS_INFORMATIVE' if W <= GRADE_INFORMATIVE_MAX else 'CONSISTENT_WEAK' if W <= GRADE_WEAK_MAX else 'UNINFORMATIVE'


def in_law_sets(I, x):
    """§5-1 3판 (RCA-08) — x 를 담는 법칙별 허용집합 I_P 의 법칙 목록 (U = ∪ I_P · envelope 가 아니다)."""
    return [law for law in sorted(I) if I[law][0] <= x <= I[law][1]]


def judge(vals, x=EXP_DBE_MS, ref=CUR_GEN_DBE_MS):
    """§5-0 – §5-5 판정 함수 (주 판정 · 감도 변이가 같은 것) — vals = {(c, 법칙, R 역할): σ} (같은 단위 · 확장 실수 0 (· +∞ = 도구만 ·
    ★ 4판 Q1 단락은 NOT_COMPUTED 라 판정 입력에 없다)) →
    법칙별 I_P · U = ∪ I_P · E (envelope) · 상태 (positive · point · extended) · 판정 이름 · W · p · d · 방향 · S.
    모든 비교 = ln (단위 불변 · x · ref 도 같은 단위 · RCA-13) · 등급 W = E 의 폭 (2판 그대로 · R3-Q5)."""
    G0x = math.log(x / ref)
    by_law = {}
    for (c, law, rr), v in sorted(vals.items()):
        by_law.setdefault(law, []).append(float(v))
    I = {law: [min(v), max(v)] for law, v in by_law.items()}
    allv = [float(v) for v in vals.values()]
    lo, hi = min(allv), max(allv)
    in_law = in_law_sets(I, x)
    inU, inE = bool(in_law), lo <= x <= hi
    ext = lo == 0.0 or hi == math.inf
    state = 'extended' if ext else ('point' if lo == hi else 'positive')
    W = math.inf if ext else (0.0 if lo == hi else math.log(hi / lo))
    if inU:
        verdict = 'UNINFORMATIVE' if ext else grade_W(W)
    elif inE:
        verdict = 'GAP_ENVELOPE_ONLY'
    else:
        verdict = 'FAIL'
    d, direction = _ln_dist(x, lo, hi)
    if inE and not inU:
        direction = 'gap'
    dU = min(_ln_dist(x, a, b)[0] for a, b in I.values())
    if state == 'positive':
        p, p_why = math.log(x / lo) / W, None
    else:
        p, p_why = None, ('point_interval' if state == 'point' else 'extended_interval (zero 끝 · W = +∞)')
    if ext:
        S, mid, S_why = None, None, 'extended_interval'
    else:
        mid = math.sqrt(lo * hi)
        S, S_why = 1.0 - abs(math.log(x / mid)) / G0x, None
    return {'verdict': verdict, 'state': state, 'interval_mScm': [lo, hi], 'I_law_mScm': I, 'in_law': in_law, 'in_U': inU,
            'in_E': inE, 'W': W, 'p': p, 'p_why': p_why, 'd': d, 'd_over_G0': d / G0x, 'direction': direction,
            'd_to_U': dU, 'S': S, 'S_why': S_why, 'sigma_mid_mScm': mid}


def grade(lo, hi):
    """한 법칙 · 두 값 구간의 판정 (보조 · 시험 V09) — judge 그대로 (U = E = [lo, hi])."""
    return judge({('0', 'P0', 'R_j_lo'): lo, ('1', 'P0', 'R_j_hi'): hi})


def decide_sentence(state, verdict, blocking, sens_incomplete=False):
    """§5-7 결정표 = ★ 4판 (Q2-4) 등록 R 4판 §5-5b — (상태, 판정 이름, 차단 표지 목록, 감도 미완료) → 문장 하나 (같은 레코드 = 같은 문장).
    차단 표지 없음 = 왼쪽 칸 · 있음 = 오른쪽 칸 (PASS = *"계산기 판정 이름 `PASS_INFORMATIVE` · 차단 표지 <목록> — 판정 문장 보류"* · 그 밖 =
    왼쪽 칸 + *"(차단 표지 <목록>)"* · <목록> = 붙은 차단 표지 이름 전부 · 사전 순) · 점 구간이면 *"점 구간"* · 감도 미완료 (⑰) 면 *"감도 미완료"* 를
    덧붙인다 · CALIB_* · NOT_COMPUTED = 판정 없음 칸 (차단 표지 · 점 · 감도 해당 없음).  짝이 안 맞는 상태 · 이름 · 닫힌 집합 (§5-6a) 밖 이름 =
    구현 결함 (ValueError) · 목록이 아닌 차단 표지 (bool · 문자열) · bool 아닌 감도 미완료 = TypeError."""
    if state not in STATE_VERDICTS or verdict not in STATE_VERDICTS[state]:
        raise ValueError(f'결정표 밖 — 상태 {state!r} · 판정 {verdict!r} (§5-0 · §5-5 짝이 아니다)')
    if not isinstance(blocking, (list, tuple)):
        raise TypeError(f'차단 표지 {blocking!r} — 이름 목록이어야 (bool · 문자열 아님 · §5-5b <목록>)')
    outside = [f for f in blocking if f not in BLOCKING_FLAGS]
    if outside:
        raise ValueError(f'차단 표지 닫힌 집합 (§5-6a) 밖 이름 {outside} — `blocking_of` 를 거친 목록이어야')
    if type(sens_incomplete) is not bool:                                   # noqa: E721
        raise TypeError(f'감도 미완료 {sens_incomplete!r} (bool 이어야)')
    left, right = DECISION[verdict]
    if right is None:                                    # CALIB_* · NOT_COMPUTED — 판정 없음 (예측 단계 전 · 해당 없음)
        return left
    s = right.format(SENTENCE_JOIN.join(sorted(set(blocking)))) if blocking else left
    if state == 'point':
        s += SENTENCE_JOIN + SENTENCE_POINT
    if sens_incomplete:
        s += SENTENCE_JOIN + SENTENCE_SENS
    return s


def blocking_of(flags):
    """§5-6a 닫힌 집합 — 이 목록 밖 이름 (예: 보고 한정어 DIA_UNCHECKED · 모르는 *_UNCHECKED) 은 차단하지 않는다."""
    return sorted(f for f in set(flags) if f in BLOCKING_FLAGS)


def sv_assess(recs, threshold, scope):
    """§5-6 SV 행 (RCA-06 · Q4) — 모서리 런 (arm 0) 의 반사실 기록 → (표지, 모서리별 기록).
    비 > 문턱 (등록 문장 '넘으면') = `SV_DEPENDENT` · 기록을 못 읽음 (없음 · 비를 싣지 않는 상태 · 주 해가 0) · 문턱 없음 = `SV_UNCHECKED` ·
    읽는 칸 = 비 · 상태 (`ca_ext_svcf.chain_view` · 끊는 면의 정의 무관 · PRE-impl-04).  ⚠ producer 의 자기 표지 비교는 ≥ (그 배선의 문턱
    = 늘 None · 이 사슬은 쓰지 않는다).
    ★ 10-22 (사전 리뷰 2 회차 PRE2-impl-01 · 1저자 Q1 (다) · 등록 R §5-6 SV 행 개정) 괄호 판정 — 모서리마다 아래 끝 (`ratio` · 못 가른 덩어리
    그대로) · 위 끝 (`ratio_hi` · 그 덩어리를 통째로 뺀 판 · 덩어리 0 = 아래 끝과 같다): 아래 끝 > 문턱 = 의존 (위 끝과 무관) · 두 끝을 읽고
    위 끝 ≤ 문턱 = 표지 없음 · 두 끝을 읽었는데 아래 ≤ 문턱 < 위 = 걸침 · 그 밖 = 못 읽음 (위 끝 칸 없는 옛 기록 포함 · 아래 끝을 못 읽은
    모서리 = 위 끝 값과 무관하게 못 읽음 = 지금 방식) → 걸침 · 못 읽음 = `SV_UNCHECKED`.  비교 = 지금 SV 비교 그대로 (증서 여유 없음 · 두 끝
    같게) · 모서리 묶기 = 지금 규칙 그대로 (하나라도 의존 → `SV_DEPENDENT` · 하나라도 걸침 · 못 읽음 · 문턱 없음 · 모서리 없음 →
    `SV_UNCHECKED` · 둘 다 붙을 수 있다)."""
    rr_scope = ('R_j_lo', 'R_j0', 'R_j_hi') if scope == 'all3' else ('R_j0',)
    out, unread, straddle, dep = {}, [], [], []
    for (c, law, rr), a in sorted(recs.items()):
        if rr not in rr_scope:
            continue
        v = a.get('sv_cf') if isinstance(a, dict) else None
        v = v if isinstance(v, dict) else {}
        st, r_, rh = v.get('status'), v.get('ratio'), v.get('ratio_hi')
        key = f'c{c}_{law}_{rr}'
        out[key] = {'status': st, 'ratio': r_, 'status_hi': v.get('status_hi'), 'ratio_hi': rh, 'n_unsplit': v.get('n_unsplit')}
        lo_ok, hi_ok = isinstance(r_, float), isinstance(rh, float)
        if threshold is None:
            if not (lo_ok and hi_ok):
                unread.append(key)
            continue
        t = float(threshold)
        if lo_ok and r_ > t:
            dep.append(key)
        elif lo_ok and hi_ok and rh <= t:
            pass
        elif lo_ok and hi_ok:
            straddle.append(key)
        else:
            unread.append(key)
    flags = []
    if threshold is None or unread or straddle or not out:
        flags.append('SV_UNCHECKED')
    if dep:
        flags.append('SV_DEPENDENT')
    return flags, {'threshold': threshold, 'scope': scope, 'corners': out, 'unreadable': unread, 'straddle': straddle,
                   'dependent': dep}


def mask_sigma(text, vals):
    """σ 값 (S/cm · mS/cm) 과 같은 수 토큰을 가린다 — 멈춤 사유 · 계약 문장에 σ 가 실려 화면에 나가지 않게."""
    vv = [v for v in vals if isinstance(v, float) and math.isfinite(v) and v != 0.0]

    def sub(m):
        try:
            x = float(m.group(0))
        except ValueError:
            return m.group(0)
        for v in vv:
            for c in (v, v * 1e3):
                if abs(x - c) <= 1e-6 * abs(c):
                    return '«σ 봉인»'
        return m.group(0)
    return re.sub(r'[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?', sub, str(text))


def git_identity(path):
    try:
        d = str(Path(path).resolve().parent if Path(path).is_file() else Path(path).resolve())
        head = subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
        dirty = subprocess.run(['git', '-C', d, 'status', '--porcelain', '--untracked-files=no'], capture_output=True,
                               text=True).stdout.strip()
        return {'head': head or None, 'dirty': bool(dirty) if head else None}
    except Exception as e:                                    # noqa: BLE001 — 기록용 (판정 칸 아님)
        return {'head': None, 'dirty': None, 'error': type(e).__name__}


def _same(a, b, rel=1e-12):
    if isinstance(a, bool) or isinstance(b, bool):
        return type(a) is type(b) and a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        fa, fb = float(a), float(b)
        return math.isfinite(fa) and math.isfinite(fb) and (fa == fb or abs(fa - fb) <= rel * max(abs(fa), abs(fb)))
    return a == b


def _int_or_none(x):
    """반복 수 칸 → int | None (bool · 수 아닌 것 · 음수 = None — 기록 칸이지 판정 칸이 아니다)."""
    return x if type(x) is int and x >= 0 else None          # noqa: E721 — bool 제외


def variant_vox(variant):
    return VOX_GRID if variant == 'GRID' else VOX_MAIN


def variant_raster(kit, variant):
    """sid 격자 무리 키 — R_j · c · P 는 래스터를 안 바꾼다 · vox · SDCP 양보는 바꾼다."""
    return f'{kit}|vox={variant_vox(variant)}|yield={variant == "SVORDER"}'


def sid_group(kit, variant, origin_idx):
    """★ Z3 — sid 지문 대조 무리 = 킷 · 래스터 · **origin** (팔 번호 — 격자 위상이 다르면 sid 격자도 다르다 · origin 검사 팔 1 · 2 가
    a0 와 다른 지문을 내는 것은 정상)."""
    return f'{variant_raster(kit, variant)}|origin={int(origin_idx)}'


def origins_for(vox):
    """러너의 팔 번호 ↔ origin (러너 SHIFTS 순서 그대로 — H = vox/2 소수 6 자리)."""
    h = float(f'{vox / 2:.6f}')
    return [(x, y, z) for x in (0.0, h) for y in (0.0, h) for z in (0.0, h)]


# ═════════════════════════ 등록 · 계획 ═════════════════════════
def registration_row_hash(path, prefix, code_unreg, label):
    """등록 R §2-1 의 해시 줄 하나 (`prefix` 로 시작하는 줄 · 하나뿐이어야) → (sha256 hex, 문서 sha256).  ⬜ = code_unreg."""
    try:
        raw = Path(path).read_bytes()
        text = raw.decode('utf-8')
    except (OSError, UnicodeDecodeError) as e:
        raise Stop('REGISTRATION_UNREADABLE', f'{path} ({type(e).__name__})')
    rows = [ln for ln in text.splitlines() if ln.startswith(prefix)]
    if len(rows) != 1:
        raise Stop('REGISTRATION_UNREADABLE', f'§2-1 "{prefix}" 줄이 {len(rows)} 개 (1 이어야)')
    cells = [c.strip() for c in rows[0].strip().strip('|').split('|')]
    val = cells[-1].strip('` ')
    if not re.fullmatch(r'[0-9a-f]{64}', val):
        raise Stop(code_unreg, f'§2-1 {label} 칸 = {val!r} — 개정 커밋 (숫자 + 계획 해시 · 결과 0 건) 전에는 σ 런 없음')
    return val, hashlib.sha256(raw).hexdigest()


def registration_plan_hash(path):
    """등록 R §2-1 의 R 런 계획 해시 칸 → (sha256 hex, 문서 sha256).  ⬜ 이면 PLAN_HASH_UNREGISTERED (사람이 옮겨 적지 않는다)."""
    return registration_row_hash(path, '| 계획 해시 |', 'PLAN_HASH_UNREGISTERED', '계획 해시')


def registration_s0_hash(path):
    """등록 R §2-1 의 S0 계획 해시 칸 (`| S0 계획 해시 |` · 위 줄과 다른 파일) → (sha256 hex, 문서 sha256)."""
    return registration_row_hash(path, '| S0 계획 해시 |', 'S0_PLAN_HASH_UNREGISTERED', 'S0 계획 해시')


def _reject_constant(tok):
    raise ValueError(f'JSON 상수 {tok} 거부')


def _num(v):
    return not isinstance(v, bool) and isinstance(v, (int, float)) and math.isfinite(v)


def load_plan(path):
    """R 런 계획 파일 (`rint-r-plan-v2` · 등록 §2-1 개정 커밋의 대상) → (dict, sha256).  사슬은 이 값을 러너 env 로 편다.
    결과 전 등록 숫자 넷은 null 이어도 꼴 검사는 지난다 (null = ⬜ · `require_plan_numbers` 가 멈춘다)."""
    try:
        raw = Path(path).read_bytes()
        obj = json.loads(raw.decode('utf-8'), parse_constant=_reject_constant)
    except (OSError, UnicodeDecodeError, ValueError) as e:
        raise Stop('PLAN_INVALID', f'{path}: {type(e).__name__}: {e}')
    bad = []
    if not isinstance(obj, dict) or set(obj) != set(PLAN_KEYS):
        raise Stop('PLAN_INVALID', f'칸 {sorted(obj) if isinstance(obj, dict) else type(obj).__name__} ≠ {sorted(PLAN_KEYS)}')
    if obj['schema'] != PLAN_SCHEMA:
        bad.append(f'schema {obj["schema"]!r} ≠ {PLAN_SCHEMA!r}')
    if not (isinstance(obj['len_law'], str) and re.fullmatch(r'[A-Za-z0-9_]+', obj['len_law'])):
        bad.append(f'len_law {obj["len_law"]!r}')
    if obj['unreg_law'] != PLAN_UNREG_MAIN:
        bad.append(f'unreg_law {obj["unreg_law"]!r} ≠ {PLAN_UNREG_MAIN!r} (주 = cut · fused = UNREG 감도)')
    for k, pos in (('s_min_um', False), ('tol_ff_um', False), ('step3_rtol', True)):
        v = obj[k]
        if not _num(v) or v < 0 or (pos and v == 0):
            bad.append(f'{k} {v!r}')
    if not (isinstance(obj['p2_extra'], str) and re.fullmatch(r'[A-Za-z0-9._=/ -]*', obj['p2_extra'])):
        bad.append(f'p2_extra {obj["p2_extra"]!r}')
    mp = obj['max_ladder_points']
    if mp is not None and not (type(mp) is int and mp >= 1):    # noqa: E721 — bool 제외
        bad.append(f'max_ladder_points {mp!r} (정수 ≥ 1 · null = ⬜)')
    cr = obj['calib_rj_ratio_max']
    if cr is not None and cr != PLAN_NO_CAP and not (_num(cr) and cr > 1.0):
        bad.append(f'calib_rj_ratio_max {cr!r} (유한 > 1 · {PLAN_NO_CAP!r} = 상한 없음으로 등록 · null = ⬜)')
    th = obj['sv_cf_threshold']
    if th is not None and not (_num(th) and th >= 1.0):
        bad.append(f'sv_cf_threshold {th!r} (유한 ≥ 1 · 비 G_full/G_cut ≥ 1 · null = ⬜)')
    if obj['sv_cf_scope'] is not None and obj['sv_cf_scope'] not in SV_CF_SCOPES:
        bad.append(f'sv_cf_scope {obj["sv_cf_scope"]!r} ∉ {SV_CF_SCOPES} (null = ⬜)')
    if bad:
        raise Stop('PLAN_INVALID', ' · '.join(bad))
    return obj, hashlib.sha256(raw).hexdigest()


def require_plan_numbers(plan):
    """결과 전 등록 숫자 넷 (⬜) 이 다 있어야 σ 런을 돈다 — 등록 R §3-2 · §3-2b · §5-6 (★ Q-G: SV 문턱이 ⬜ 인 채로는 못 간다)."""
    miss = [k for k in PLAN_REGISTERED_NUMBERS if plan.get(k) is None]
    if miss:
        raise Stop('PLAN_NUMBER_UNREGISTERED', f'R 계획 칸 {miss} = null (⬜ 결과 전 등록 · 1저자 · §10 개정 · 숫자를 사슬이 고르지 않는다)')


def ladder_cap(plan):
    """§3-2 점 수 상한 (⬜ = 계획 칸 · 2판 숫자 12 는 기본값이 아니다)."""
    return int(plan['max_ladder_points'])


def plan_env(plan):
    env = {'CJUNC_LEN_LAW': plan['len_law'], 'CJUNC_UNREG_LAW': plan['unreg_law'], 'CJUNC_S_MIN_UM': repr(float(plan['s_min_um'])),
           'CJUNC_TOL_FF_UM': repr(float(plan['tol_ff_um'])), 'STEP3_RTOL': repr(float(plan['step3_rtol']))}
    if plan['p2_extra']:
        env['P2_EXTRA'] = plan['p2_extra']
    return env


def check_plan_registered(plan_sha, reg_path):
    want, reg_sha = registration_plan_hash(reg_path)
    if plan_sha != want:
        raise Stop('PLAN_HASH_MISMATCH', f'계획 sha256 {plan_sha[:16]}… ≠ 등록 §2-1 {want[:16]}…')
    return {'path': str(Path(reg_path).resolve()), 'sha256': reg_sha, 'plan_hash': want}


def plans_cross_problems(plan, s0):
    """§2-1 · §10-2 ⑪ 두 계획 대조 → 문제 목록.  R 계획 tol_ff = S0 tol_ff (같은 float) · 사슬 L_par · r_port · r_f = S0 값 ·
    R 계획 step3_rtol = §3-5 봉인값 (`step3_conv_cert.CERT_RTOL_MAX`) · len_law = 등록 v0 길이 법칙 이름 (`carbon_junction.CJUNC_LEN_LAW` ·
    분산판 = 같은 총 G 법칙 · 표현 판은 원장 · model 이름) · unreg_law = cut."""
    import carbon_junction as _cj
    import step3_conv_cert as _cc
    v = (s0 or {}).get('values_um') if isinstance(s0, dict) else None
    v = v if isinstance(v, dict) else {}
    bad = []

    def eqf(name, a, b):
        if not (_num(a) and _num(b) and float(a) == float(b)):
            bad.append(f'{name}: {a!r} ≠ {b!r}')
    eqf('R 계획 tol_ff_um ↔ S0 values_um.tol_ff', plan.get('tol_ff_um'), v.get('tol_ff'))
    eqf('S0 values_um.tol_P ↔ tol_ff', v.get('tol_P'), v.get('tol_ff'))
    eqf('S0 values_um.tol_sj ↔ tol_ff', v.get('tol_sj'), v.get('tol_ff'))
    eqf('사슬 L_PAR_UM ↔ S0 values_um.L_par', L_PAR_UM, v.get('L_par'))
    eqf('사슬 R_PORT_UM ↔ S0 values_um.r_port', R_PORT_UM, v.get('r_port'))
    eqf('사슬 VGCF_D_UM/2 ↔ S0 values_um.r_f', VGCF_D_UM / 2.0, v.get('r_f'))
    eqf('R 계획 step3_rtol ↔ §3-5 봉인 CERT_RTOL_MAX', plan.get('step3_rtol'), _cc.CERT_RTOL_MAX)
    if plan.get('len_law') != _cj.CJUNC_LEN_LAW:
        bad.append(f'R 계획 len_law {plan.get("len_law")!r} ≠ 등록 v0 길이 법칙 {_cj.CJUNC_LEN_LAW!r}')
    if plan.get('unreg_law') != PLAN_UNREG_MAIN:
        bad.append(f'R 계획 unreg_law {plan.get("unreg_law")!r} ≠ {PLAN_UNREG_MAIN!r}')
    return bad


def _s0_check_obj(obj, raw):
    """S0 계획 dict · 바이트 → 문제 | None (정본 = `ca_s0_census.check_plan` · 정준 바이트 · 사본 없음)."""
    import ca_s0_census as _s0
    if not isinstance(obj, dict) or obj.get('schema') != S0_PLAN_SCHEMA:
        return f'schema {(obj or {}).get("schema") if isinstance(obj, dict) else type(obj).__name__!r} ≠ {S0_PLAN_SCHEMA!r}'
    try:
        _s0.check_plan(obj)
    except Exception as e:                                    # noqa: BLE001 — S0Error · 그 밖 = 확인 못 함 = 거부
        return f'check_plan: {type(e).__name__}: {e}'
    if raw is not None and _s0.plan_bytes_of(obj) != raw:
        return '정준 바이트가 아니다 (손으로 고친 형식 · 단계 1 산출물 그대로)'
    return None


def check_s0(s0_obj, s0_sha, raw, reg_path, plan):
    """S0 계획 → 기록 dict ({path?, sha256, content}) · 등록 `| S0 계획 해시 |` 대조 · 두 계획 대조.  실패 = Stop."""
    why = _s0_check_obj(s0_obj, raw)
    if why:
        raise Stop('S0_PLAN_INVALID', why)
    if raw is None:
        import ca_s0_census as _s0
        if hashlib.sha256(_s0.plan_bytes_of(s0_obj)).hexdigest() != s0_sha:
            raise Stop('S0_PLAN_INVALID', '기록된 S0 계획 sha256 ≠ 그 내용의 정준 바이트 sha256')
    want, _reg = registration_s0_hash(reg_path)
    if s0_sha != want:
        raise Stop('S0_PLAN_HASH_MISMATCH', f'S0 계획 sha256 {s0_sha[:16]}… ≠ 등록 §2-1 {want[:16]}…')
    bad = plans_cross_problems(plan, s0_obj)
    if bad:
        raise Stop('PLAN_CROSS_MISMATCH', ' · '.join(bad))
    return {'sha256': s0_sha, 'content': s0_obj}


def load_s0_plan(path, reg_path, plan):
    """--s0-plan 파일 → 기록 (path · sha256 · content) · 꼴 · 등록 · 대조 (`check_s0`)."""
    try:
        raw = Path(path).read_bytes()
        obj = json.loads(raw.decode('ascii'), parse_constant=_reject_constant)
    except (OSError, UnicodeDecodeError, ValueError) as e:
        raise Stop('S0_PLAN_INVALID', f'{path}: {type(e).__name__}: {e}')
    rec = check_s0(obj, hashlib.sha256(raw).hexdigest(), raw, reg_path, plan)
    return dict(rec, path=str(Path(path).resolve()))


def recheck_s0_record(rec, reg_path, plan):
    """요약에 기록된 S0 계획 (예측 · 판정 단계) — 내용 → 정준 바이트 sha256 = 기록 sha · 등록 · 대조 (같은 함수)."""
    if not isinstance(rec, dict) or not isinstance(rec.get('content'), dict) or not isinstance(rec.get('sha256'), str):
        raise Stop('S0_PLAN_INVALID', '요약에 S0 계획 기록 (sha256 · content) 이 없다')
    return check_s0(rec['content'], rec['sha256'], None, reg_path, plan)


# ═════════════════════════ ★ PF2 B (10-22) S0 단계 2 보고의 봉인 계획 해시 ═════════════════════════
def _hex64(x):
    return isinstance(x, str) and re.fullmatch(r'[0-9a-f]{64}', x) is not None


def s0_stage2_record(rep, sha, path):
    """S0 단계 2 보고 (dict) → 사슬 기록 (판정 칸만 · 보고 경로 · 파일 sha256) — 꼴이 틀려도 기록은 만들고 (값 그대로) 검사는
    `s0_stage2_problem` 이 한다 (예측 · 판정은 이 기록을 다시 검사한다 · 보고 파일을 다시 읽지 않는다)."""
    rp = rep if isinstance(rep, dict) else {}
    pl = rp.get('plan') if isinstance(rp.get('plan'), dict) else {}
    rr = pl.get('r_plan') if isinstance(pl.get('r_plan'), dict) else {}
    kit = rp.get('kit') if isinstance(rp.get('kit'), dict) else {}
    return {'path': path, 'sha256': sha, 'schema': rp.get('schema'), 'stage': rp.get('stage'), 'kit': kit.get('name'),
            'plan_sha256': pl.get('sha256'), 'plan_source': pl.get('source'), 'r_plan_sha256': rr.get('sha256'), 'r_plan_path': rr.get('path')}


def s0_stage2_problem(rec, plan_sha, s0_sha):
    """★ PF2 B (10-22 · 사전 리뷰 2 회차 PRE2-design-01 · 탐침 E · 1저자 Q2 권고대로 · 등록 R §2-1 · §2-1b · §11 ④) — 단계 2 기록 → 문제 | None.
    단계 2 (DBE 열람) 의 인자 커밋이 봉인한 계획 해시 = 지금 쓰는 두 계획의 sha256 (**정확히**): `r_plan_sha256` = R 계획 (`--plan`) ·
    `plan_sha256` = S0 계획 (`--s0-plan`) · 꼴 = 이 도구의 S0 보고 (schema · 단계 2 · DBE 새 침대 · source commit:<sha>).  DBE 를 본 뒤 계획을
    다시 등록하면 (s_min · 결과 전 숫자 · maxiter · 계획 B) 여기서 멈춘다 (옛 사슬 = 단계 2 보고를 읽지 않아 계획 B 로 CALIBRATED)."""
    r = rec if isinstance(rec, dict) else {}
    if r.get('schema') != S0_REPORT_SCHEMA or type(r.get('stage')) is not int or r.get('stage') != 2:   # noqa: E721 — bool 제외
        return f'S0 단계 2 보고 꼴 — schema {r.get("schema")!r} · 단계 {r.get("stage")!r} (= {S0_REPORT_SCHEMA!r} · 2)'
    if r.get('kit') != DBE_KIT:
        return f'S0 단계 2 보고의 킷 {r.get("kit")!r} ≠ {DBE_KIT!r} (R 런 DBE 침대의 보고여야)'
    if not (isinstance(r.get('plan_source'), str) and r['plan_source'].startswith('commit:')):
        return f'S0 단계 2 보고의 계획 출처 {r.get("plan_source")!r} (commit:<개정 커밋> 이어야 — 단계 2 의 인자 커밋)'
    if not (_hex64(r.get('r_plan_sha256')) and _hex64(r.get('plan_sha256'))):
        return f'S0 단계 2 보고의 봉인 계획 해시 꼴 — R 계획 {r.get("r_plan_sha256")!r} · S0 계획 {r.get("plan_sha256")!r} (64 자 소문자 hex)'
    if r['r_plan_sha256'] != plan_sha:
        return (f'S0 단계 2 가 봉인한 R 계획 {r["r_plan_sha256"][:16]}… ≠ 지금 R 계획 {str(plan_sha)[:16]}… — DBE 를 본 뒤 계획을 다시 등록했다 '
                f'(Q2: 계획 하나 · 바꾸려면 새 등록 · 등록 R §2-1b)')
    if r['plan_sha256'] != s0_sha:
        return f'S0 단계 2 가 봉인한 S0 계획 {r["plan_sha256"][:16]}… ≠ 지금 S0 계획 {str(s0_sha)[:16]}…'
    return None


def read_s0_stage2(path, plan_sha, s0_sha):
    """사다리 — `--s0-stage2-report` 파일 → 단계 2 기록 · 대조 (`s0_stage2_problem`) · 실패 = Stop S0_REPORT_MISMATCH."""
    try:
        raw = Path(path).read_bytes()
        rep = json.loads(raw.decode('utf-8'), parse_constant=_reject_constant)
    except (OSError, UnicodeDecodeError, ValueError, TypeError) as e:
        raise Stop('S0_REPORT_MISMATCH', f'S0 단계 2 보고 {path}: {type(e).__name__}: {e}')
    rec = s0_stage2_record(rep, hashlib.sha256(raw).hexdigest(), str(Path(path).resolve()))
    why = s0_stage2_problem(rec, plan_sha, s0_sha)
    if why:
        raise Stop('S0_REPORT_MISMATCH', why)
    return rec


def s0_reports_problem(recs, plan_sha, s0_sha):
    """예측 · 판정 — 단계 요약에 기록된 S0 보고 기록 → 문제 | None (같은 함수로 다시 대조 · 기록 없음 = 옛 요약 = 대조 불가)."""
    if not isinstance(recs, dict) or not isinstance(recs.get('stage2'), dict):
        return 'S0 단계 2 보고 기록이 없다 (--s0-stage2-report 없이 돈 단계 · 옛 요약 — 봉인 계획 해시를 대조할 수 없다)'
    return s0_stage2_problem(recs['stage2'], plan_sha, s0_sha)


# ═════════════════════════ 팔 읽기 · 계약 (런 하나 = 폴더 하나) ═════════════════════════
def expected_request(req, plan):
    """러너에 요청한 다음 세대 선언 (영수증 `ca_ext_request` 와 매니페스트 protocol 이 같아야 한다).
    ★ Z3 — 극한 런 = 러너 꼴 (`run_contract.runner_ca_ext`): 바닥 `R_j_ohm` null + `rj_limit` 'inf' · 천장 0.0 + 'zero' (정량 런엔 칸 없음)."""
    rj = req['rj']
    unreg = 'fused' if req['variant'] == 'UNREG' else plan['unreg_law']
    cj = {'R_j_ohm': (None if rj == 'inf' else rj_float(rj)), 'len_law': plan['len_law'], 'unreg_law': unreg,
          's_min_um': float(plan['s_min_um']), 'tol_ff_um': float(plan['tol_ff_um']), 'ptfe_jlaw': req['law']}
    if rj in LIMIT_MARK:
        cj['rj_limit'] = LIMIT_MARK[rj]
    out = {'cjunc': cj}
    if req['c'] != '':
        out['sdcp_mod'] = {'c': float(req['c'])}
    return out


def _solve_ran(state, cert):
    """그 해에서 CG 가 돌았나 — 양의 해 · 행렬 그래프 영값 (조기 반환 영값 · 단락 = 솔브 없음)."""
    return state == 'positive' or (state == 'zero' and (cert or {}).get('zero_source') == 'matrix_graph')


def manifest_problems(man, rcpt, req, plan, idx, cert, state='positive'):
    """매니페스트 · 영수증 ↔ 요청 (§10 멈춤 '매니페스트 ≠ 요청') → 문제 목록."""
    var = req['variant']
    vox = variant_vox(var)
    bulk = FIBRE_BULK_DIV10 if var == 'FIBRE' else FIBRE_BULK
    yv = var == 'SVORDER'
    bad = []

    def num(k, want, r=1e-9):
        if not _same(man.get(k), want, r):
            bad.append(f'{k} {man.get(k)!r} ≠ {want!r}')

    def eq(k, want):
        if not (type(man.get(k)) is type(want) and man.get(k) == want):   # noqa: E721 — bool ↔ int 섞임 거부
            bad.append(f'{k} {man.get(k)!r} ≠ {want!r}')
    num('vox_um', vox)
    for k, v in MAN_FIXED.items():
        num(k, v)
    num('sigma_vgcf_S_cm', bulk * math.pi * VGCF_D_UM ** 2 / (4.0 * vox * vox), 1e-5)   # 직경 보존 (러너 %.6g)
    eq('ptfe_stamp', 'face_alpha')
    eq('sdcp_stamp', 'sphere')
    eq('fibre_stamp', 'segment')
    eq('periodic_xy', False)
    eq('sdcp_yield_to_vgcf', yv)
    o = man.get('origin_shift_um')
    want_o = origins_for(vox)[idx]
    if not (isinstance(o, list) and len(o) == 3 and all(_same(a, b, 1e-9) or (a == 0 and b == 0) for a, b in zip(o, want_o))):
        bad.append(f'origin_shift_um {o!r} ≠ arm {idx} {list(want_o)!r}')
    if man.get('component_plan') != LEAN2_PLAN:
        bad.append(f'component_plan {man.get("component_plan")!r} ≠ LEAN 2 {LEAN2_PLAN}')
    want_req = expected_request(req, plan)
    if man.get(RC.CA_EXT_REQUEST_FIELD) != sorted(want_req):
        bad.append(f'{RC.CA_EXT_REQUEST_FIELD} {man.get(RC.CA_EXT_REQUEST_FIELD)!r} ≠ {sorted(want_req)}')
    ca = man.get('ca_ext') if isinstance(man.get('ca_ext'), dict) else {}
    want_blk = {'schema', 'ptfe_face'} | set(want_req)
    if set(ca) != want_blk:
        bad.append(f'ca_ext 하위 블록 {sorted(ca)} ≠ {sorted(want_blk)}')
    cjb = ca.get('cjunc') if isinstance(ca.get('cjunc'), dict) else {}
    cjp = cjb.get('protocol') if isinstance(cjb.get('protocol'), dict) else {}
    lim = LIMIT_MARK.get(req['rj'])
    if lim:
        if not (cjp.get('rj_limit') == lim and cjp.get('allow_rj_limits') is True and cjp.get('quantitative') is False):
            bad.append(f'극한 런 ({lim}) 표지 — rj_limit {cjp.get("rj_limit")!r} · allow_rj_limits {cjp.get("allow_rj_limits")!r} · '
                       f'quantitative {cjp.get("quantitative")!r}')
        if lim == 'zero' and not (type(cjp.get('R_j_ohm')) is float and cjp.get('R_j_ohm') == 0.0):   # noqa: E721
            bad.append(f'천장 R_j_ohm {cjp.get("R_j_ohm")!r} ≠ 0.0')
        if lim == 'inf' and cjp.get('R_j_ohm') is not None:
            bad.append(f'바닥 R_j_ohm {cjp.get("R_j_ohm")!r} ≠ null (JSON 은 inf 를 못 쓴다 · 표지 inf 와 한 꼴)')
    else:
        if not (cjp.get('allow_rj_limits') is False and cjp.get('quantitative') is True and 'rj_limit' not in cjp):
            bad.append('정량 런인데 극한 표지가 있다')
        if not _same(cjp.get('R_j_ohm'), rj_float(req['rj'])):
            bad.append(f'cjunc.R_j_ohm {cjp.get("R_j_ohm")!r} ≠ {req["rj"]}')
    for k in ('len_law', 'unreg_law', 's_min_um', 'tol_ff_um', 'ptfe_jlaw'):
        if not _same(cjp.get(k), want_req['cjunc'][k]):
            bad.append(f'cjunc.{k} {cjp.get(k)!r} ≠ {want_req["cjunc"][k]!r}')
    for k, v in (('ptfe_stamp', 'face_alpha'), ('L_par_um', L_PAR_UM), ('r_port_um', R_PORT_UM)):
        if not _same(cjp.get(k), v):
            bad.append(f'cjunc.{k} {cjp.get(k)!r} ≠ {v!r}')
    if 'sdcp_mod' in want_req:
        cv = (((ca.get('sdcp_mod') or {}).get('protocol') or {}) if isinstance(ca.get('sdcp_mod'), dict) else {}).get('c')
        if not _same(cv, want_req['sdcp_mod']['c']):
            bad.append(f'sdcp_mod.c {cv!r} ≠ {req["c"]}')
    #  ★ 3판 — 수렴 증서 rtol = 계획 (CG 가 돈 해만 · 조기 반환 영값 · 단락 증서엔 rtol 칸이 없다 → 영수증 rtol 로 결합)
    if _solve_ran(state, cert) and not _same((cert or {}).get('rtol_used'), float(plan['step3_rtol'])):
        bad.append(f'증서 rtol_used {(cert or {}).get("rtol_used")!r} ≠ 계획 {plan["step3_rtol"]!r}')
    #  ★ 3판 — SV 반사실 요청 (사슬이 정한 런만 · producer 문턱 = None · 문턱은 이 사슬의 계획)
    want_cf = bool(req.get('sv_cf'))
    cjev = cjb.get('evidence') if isinstance(cjb.get('evidence'), dict) else {}
    if ('sv_counterfactual_request' in cjev) != want_cf:
        bad.append(f'접합 증거의 SV 반사실 요청 {"있음" if "sv_counterfactual_request" in cjev else "없음"} ≠ 사슬 요청 {want_cf}')
    elif want_cf and cjev.get('sv_counterfactual_request') != {'threshold': None}:
        bad.append(f'SV 반사실 요청 {cjev.get("sv_counterfactual_request")!r} ≠ {{"threshold": None}} (문턱 = 사슬 계획)')
    # 영수증 (러너가 무엇으로 돌라고 했나) ↔ 요청
    if not isinstance(rcpt, dict):
        bad.append('run_receipt.json 이 없다')
        return bad
    rq = rcpt.get('ca_ext_request')
    if not isinstance(rq, dict) or sorted(rq) != sorted(want_req) or any(
            not isinstance(rq.get(s), dict) or set(rq[s]) != set(want_req[s]) or not all(_same(rq[s][k], v) for k, v in want_req[s].items())
            for s in want_req):
        bad.append(f'영수증 ca_ext_request {rq!r} ≠ 요청 {want_req!r}')
    if not _same(rcpt.get('step3_rtol'), float(plan['step3_rtol'])):
        bad.append(f'영수증 step3_rtol {rcpt.get("step3_rtol")!r} ≠ 계획 {plan["step3_rtol"]!r}')
    if (rcpt.get('sv_counterfactual') is True) != want_cf or ('sv_counterfactual' in rcpt and rcpt.get('sv_counterfactual') is not True):
        bad.append(f'영수증 sv_counterfactual {rcpt.get("sv_counterfactual")!r} ≠ 사슬 요청 {want_cf}')
    for k, v in (('arms', req['arms']), ('ptfe_stamp', 'face_alpha'), ('vox_um', vox), ('sdcp_yield_to_vgcf', yv),
                 ('expect_backend', EXPECT_BACKEND)):
        if not _same(rcpt.get(k), v):
            bad.append(f'영수증 {k} {rcpt.get(k)!r} ≠ {v!r}')
    al = req.get('arm_list')                                  # ★ Z3 — 팔 고르기 런 = 영수증 arm_list (정렬 목록) · 아닌 런 = 칸 없음
    if (al is None and 'arm_list' in rcpt) or (al is not None and rcpt.get('arm_list') != list(al)):
        bad.append(f'영수증 arm_list {rcpt.get("arm_list")!r} ≠ 요청 {al!r}')
    if 'sigma_vgcf_S_cm' in rcpt:
        bad.append(f'영수증이 σ_VGCF 를 직접 정했다 ({rcpt["sigma_vgcf_S_cm"]!r} · SIGMA_VGCF_OVERRIDE 세대)')
    ok, why = RC.receipt_match(rcpt, man, origin=man.get('origin_shift_um'))
    if not ok:
        bad.append(f'영수증 ↔ 매니페스트 {why}')
    return bad


def lean_problems(man, state='positive', s3=None):
    """솔브 영수증 ↔ LEAN 2 표 (설계 §7) — ★ 3판: 조기 반환 해 (영값 위상 · 단락) 는 주 솔브 영수증 = failed (사유 = 결과 사유)."""
    s3 = s3 if isinstance(s3, dict) else {}
    early = state == 'short' or (state == 'zero' and (s3.get('conv_cert') or {}).get('zero_source') == 'early_return')
    ca = man.get('ca_ext') if isinstance(man.get('ca_ext'), dict) else {}
    bad = []
    for sub in ('ptfe_face', 'cjunc'):
        rc_ = ((ca.get(sub) or {}).get('evidence') or {}).get('receipts') if isinstance(ca.get(sub), dict) else None
        if not isinstance(rc_, dict) or set(rc_) != set(LEAN2_RECEIPTS):
            bad.append(f'{sub} 영수증 키 {sorted(rc_) if isinstance(rc_, dict) else rc_!r}')
            continue
        for name, ok_st in LEAN2_RECEIPTS.items():
            r = rc_.get(name) if isinstance(rc_.get(name), dict) else {}
            if name == 'electronic_main' and early:
                ok_st = ('failed',)
                if r.get('why') != s3.get('reason'):
                    bad.append(f'{sub}.{name} 사유 {r.get("why")!r} ≠ 결과 사유 {s3.get("reason")!r} (조기 반환 해)')
            if r.get('status') not in ok_st:
                bad.append(f'{sub}.{name} = {r.get("status")!r} (LEAN 2 표 · 상태 {state} {ok_st})')
    return bad


ARM_PUBLIC = ('file', 'index', 'sha256', 'protocol_id', 'state', 'cg_info', 'cg_resid', 'imbalance', 'cert_pass', 'sid_fp',
              'cg_iters', 'resolve_iters', 'sv_cf_status',   # ★ Z3 — CG 반복 수 · ★ 3판 — 해 상태 · SV 반사실 상태 (σ · 비 아님)
              'err_rel')                                     # ★ 4판 (Q2-2) — 판독 보장 오차 e (증서 ⓓ · 상대값 · σ 아님)
#: 런 요청 칸 (요약 `runs` · 다시 판정 · 사다리 확인 팔 다시 읽기가 같은 칸을 쓴다)
REQ_KEYS = ('name', 'role', 'kit', 'law', 'c', 'rj', 'arms', 'arm_list', 'variant', 'sv_cf')


def arm_indices(req):
    """요청 → 팔 번호 (origin 번호) 목록 — `ARM_LIST` 런 = 그 목록 · 아니면 0..ARMS−1."""
    al = req.get('arm_list')
    return list(al) if al is not None else list(range(req['arms']))


def arm_file_shas(outdir):
    """읽기가 멈춘 런의 팔 파일 → [{file, index, sha256}] (번호 순 · 번호 없는 이름은 뺀다) — 계약 판정은 하지 않는다."""
    out = []
    for p in sorted(glob.glob(str(Path(outdir) / 'p2_*.json'))):
        m = re.search(r'_a(\d+)\.json$', p)
        if m:
            try:
                out.append({'file': os.path.basename(p), 'index': int(m.group(1)), 'sha256': sha256_file(p)})
            except OSError:
                pass
    return sorted(out, key=lambda x: (x['index'], x['file']))


def read_run(outdir, req, plan, contract, sid_reg, want_sha=None):
    """런 폴더 하나 → [팔 기록 …] (번호 순).  등록 R §10 멈춤 목록의 팔 쪽 전부 — 어긋나면 Stop (원인 칸 = σ 를 가린 문장).
    ★ 3판 — 해 상태 (§5-0 · `run_contract.next_gen_state` · 정본): positive (증서 ⓐ–ⓓ · σ > 0) · zero (VALID_ZERO_TOPOLOGY · σ = 0) ·
    ~~short (ELECTRODE_SHORT · σ = +∞)~~ · 그 밖 = NOT_COMPUTED.  팔 기록의 σ = 확장 실수 (0 그대로).
    ★ 4판 (10-21 · 1저자 Q1 · 등록 R 4판 §5-0 ①–③ · §4-2 ③) — short (ELECTRODE_SHORT · J11) = 생산자 미게시 → 기록 검사 (계약 · 매니페스트 ·
    LEAN · sid) 를 다 지난 뒤 이 런 = NOT_COMPUTED (멈춤 사유 reason = ELECTRODE_SHORT · `registration_state`) — 기록이 요청과 다르면 그 멈춤
    이름이 먼저다 (단락이 계약 위반을 가리지 않는다).
    ★ 10-21 (PRE-impl-07 병합) — 순서 = 세대 (GENERATION) · ca_ext 기록 (CA_EXT_RECORD) → 해 상태 (증서 · 증서 ↔ 런 결합) → 팔 계약 · 매니페스트."""
    outdir = Path(outdir)
    name = req.get('name')
    rej = sorted(os.path.basename(x) for x in glob.glob(str(outdir / '.rejected_*')))
    if rej:
        raise Stop('REJECTED_MARKER', f'{outdir.name}: {rej}', name)
    files = sorted(glob.glob(str(outdir / 'p2_*.json')))
    byi = {}
    for p in files:
        m = re.search(r'_a(\d+)\.json$', p)
        if not m or int(m.group(1)) in byi:
            raise Stop('ARM_JSON_COUNT', f'{outdir.name}: 팔 번호가 없거나 겹친다 ({os.path.basename(p)})', name)
        byi[int(m.group(1))] = p
    idx = arm_indices(req)
    if sorted(byi) != idx:
        raise Stop('ARM_JSON_COUNT', f'{outdir.name}: 팔 번호 {sorted(byi)} ≠ 요청 {idx}', name)
    pref = f'p2_{req["kit"][len("kit_"):]}_'
    if any(not os.path.basename(p).startswith(pref) for p in byi.values()):
        raise Stop('ARM_JSON_COUNT', f'{outdir.name}: 팔 이름이 킷 {req["kit"]} 의 것이 아니다', name)
    if want_sha is not None and len(want_sha) != len(idx):
        raise Stop('INPUT_SHA_MISMATCH', f'{outdir.name}: 기록된 sha256 {len(want_sha)} 개 ≠ 팔 {len(idx)}', name)
    try:
        rcpt = json.loads((outdir / 'run_receipt.json').read_text(encoding='utf-8'))
    except (OSError, ValueError):
        rcpt = None
    out = []
    for j, i in enumerate(idx):
        p = byi[i]
        if want_sha is not None:
            why = sha_mismatch(p, want_sha[j])
            if why:
                raise Stop('INPUT_SHA_MISMATCH', why, name)
        try:
            raw = Path(p).read_bytes()
            payload = json.loads(raw.decode('utf-8'))
        except (OSError, UnicodeDecodeError, ValueError) as e:
            raise Stop('ARM_UNREADABLE', f'{os.path.basename(p)}: {type(e).__name__}', name)
        s3 = RC.step3_of(payload) if isinstance(payload, dict) else None
        man = s3.get('manifest') if isinstance(s3, dict) else None
        if not isinstance(s3, dict) or not isinstance(man, dict):
            raise Stop('ARM_UNREADABLE', f'{os.path.basename(p)}: step3 · manifest 블록이 없다', name)
        cert = s3.get('conv_cert') if isinstance(s3.get('conv_cert'), dict) else None
        sv = [s3.get('sigma_e_eff_S_cm'), (cert or {}).get('sigma'), (cert or {}).get('sigma_resolve')]
        sv = [float(x) for x in sv if isinstance(x, (int, float)) and not isinstance(x, bool)]

        def stop(code, why, reason=None):
            raise Stop(code, mask_sigma(f'{os.path.basename(p)}: {why}', sv), name, reason=reason)
        #  ★ 10-21 (사전 리뷰 PRE-impl-07 병합 · B 권고) — 기록 (세대 · ca_ext) 먼저, 해 상태 (증서 · 증서 ↔ 런 결합) 는 그 뒤: 결합은 맞는 세대 ·
        #    맞는 기록 위에서만 뜻이 있다 (옛 순서 = 상태 먼저 → unknown:ca_ext 팔이 GENERATION 대신 CERT|bind| NOT_COMPUTED 로 멈췄다)
        pid = RC.physics_protocol_id(man)
        if not str(pid).startswith(RC.CA_EXT_PREFIX + '-'):
            stop('GENERATION', f'다시 계산한 id = {pid!r} (p3ca- 이어야)')
        if man.get('physics_protocol_id') != pid:
            stop('GENERATION', f'저장 id {man.get("physics_protocol_id")!r} ≠ 다시 계산 {pid!r}')
        ok, why = contract.ca_ext_record(man)
        if not ok:
            stop('CA_EXT_RECORD', why)
        state, swhy = RC.next_gen_state(s3)
        if state is None:
            stop('NOT_COMPUTED', f'해 상태 (§5-0) {swhy}')
        if state in ('positive', 'legacy'):
            ok, why = RC.conv_ok(s3.get('cg_info'), s3.get('unconverged'), s3.get('cg_resid'))
            if not ok:
                stop('NOT_COMPUTED', f'수렴 계약 {why}')
        why = contract.arm_problem(p, rcpt)
        if why:
            stop('ARM_CONTRACT', why)
        bad = manifest_problems(man, rcpt, req, plan, i, cert, state)
        if bad:
            stop('MANIFEST_MISMATCH', ' · '.join(bad[:6]) + (f' (+{len(bad) - 6})' if len(bad) > 6 else ''))
        bad = lean_problems(man, state, s3)
        if bad:
            stop('RECEIPT_LEAN', ' · '.join(bad))
        if man.get('ptfe_cells_observed') != 0:
            stop('PTFE_CELLS_OBSERVED', f'ptfe_cells_observed = {man.get("ptfe_cells_observed")!r} (face_alpha = PTFE 셀 0)')
        ca = man['ca_ext']
        fp = (ca['cjunc'].get('evidence') or {}).get('fp') or {}
        sid = fp.get('sid')
        off = ((ca['ptfe_face'].get('evidence') or {}).get('fp') or {}).get('sid_off')
        #  ★ Z3 — off 격자 지문 필수 (face_alpha 의 sid 격자 = off 격자 · 접합 원장과 같은 솔브 · 같은 지문 함수) · 정본 계약 뒤 둘째 겹
        if not isinstance(sid, str) or not sid or off != sid:
            stop('SID_GRID', f'접합 원장 sid 지문 {sid!r} · off 격자 지문 {off!r} (둘이 같아야 한다)')
        key = sid_group(req['kit'], req['variant'], i)
        if sid_reg.setdefault(key, sid) != sid:
            stop('SID_GRID', f'{key} 의 sid 지문이 앞 런과 다르다')
        reg, reg_why = registration_state(state)          # ★ 4판 (Q1) — 이 등록의 풀이 상태 셋 (§5-0)
        if reg == 'NOT_COMPUTED':
            stop('NOT_COMPUTED', f'해 상태 (§5-0 · 4판) {state} → {reg} (사유 {reg_why}) — 단락 (J11 · 판–판 0 저항 축약) = 생산자 미게시 · '
                                 f'σ 값 없음 (+∞ 로 판정에 오지 않는다 · 등록 R 4판 §5-0 ①–③)', reason=reg_why)
        if reg == 'VALID_ZERO_TOPOLOGY':
            sigma = 0.0
            err = 0.0                                    # ★ 4판 (Q2-2 · ③″) — σ = 0 정확 (위상 · 증서 대상 아님) → 판독 구간 [0, 0] (e 무관)
        else:
            sig = s3.get('sigma_e_eff_S_cm')
            if isinstance(sig, bool) or not isinstance(sig, (int, float)) or not math.isfinite(sig) or sig <= 0:
                stop('ARM_UNREADABLE', 'σ_e 가 유한 양수가 아니다')
            sigma = float(sig)
            #  ★ 4판 (Q2-2 · §3-2b ③″ · PRE-design-12 · R4-Q2) — 판독 보장 오차 e = 그 런 증서 ⓓ 의 target_err_bound_rel — 기록 칸을 믿지 않고
            #    증서 구간 · 게시 판 전류에서 생산 · 계약과 **같은 함수** (`step3_conv_cert.target_judge`) 로 다시 계산 (next_gen_state 가 ⓓ 통과를
            #    이미 확인했다 · e ≤ τ = 1e-4 · 등록 τ 가 아니라 그 런의 값)
            import step3_conv_cert as _cc
            jd = _cc.target_judge((cert or {}).get('target_lo'), (cert or {}).get('target_hi'), (cert or {}).get('I_bot'))
            err = jd.get('target_err_bound_rel')
            if jd.get('pass_d') is not True or isinstance(err, bool) or not isinstance(err, float) or not math.isfinite(err) or err < 0.0:
                stop('NOT_COMPUTED', f'증서 ⓓ 보장 오차를 다시 계산할 수 없다 ({jd.get("target_why")}) — 보호 띠 (§3-2b ③″) 를 잴 수 없다')
        solve = (ca['cjunc'].get('evidence') or {}).get('solve') or {}
        svr = solve.get('sv_counterfactual')
        cf = SVCF.chain_view(svr) if isinstance(svr, dict) else None
        out.append({'file': os.path.basename(p), 'index': i, 'sha256': hashlib.sha256(raw).hexdigest(), 'protocol_id': pid,
                    'state': state, 'cg_info': s3.get('cg_info'), 'cg_resid': s3.get('cg_resid'), 'imbalance': (cert or {}).get('imbalance'),
                    'cert_pass': [(cert or {}).get('pass_a'), (cert or {}).get('pass_b'), (cert or {}).get('pass_c'),
                                  (cert or {}).get('pass_d')],
                    'sid_fp': sid, 'cg_iters': _int_or_none(s3.get('cg_iters')),
                    'resolve_iters': _int_or_none((cert or {}).get('resolve_iters')),
                    'sigma': sigma, 'dsigma_rel': (cert or {}).get('dsigma_rel'), 'err_rel': err,
                    'sv_cf': cf, 'sv_cf_status': (cf or {}).get('status'),
                    'sv_local': solve.get('sv_local_dissipation'), 'dissipation_share': solve.get('dissipation_share'),
                    'n_sdcp_near': (((ca.get('sdcp_mod') or {}).get('evidence') or {}).get('n_sdcp_near')
                                    if isinstance(ca.get('sdcp_mod'), dict) else None)})
    return out


# ═════════════════════════ 러너 (런마다 새 폴더 · env 를 사슬이 정한다) ═════════════════════════
class Runner:
    def __init__(self, runner, root, out, plan, variant, deadline, contract, dry=False, parent_env=None, prefix='R'):
        self.runner, self.root, self.out = Path(runner), Path(root), Path(out)
        self.plan, self.variant, self.deadline, self.contract, self.dry, self.prefix = plan, variant, deadline, contract, dry, prefix
        parent = dict(os.environ if parent_env is None else parent_env)
        self.scrubbed = sorted(k for k in parent if ENV_SCRUB_RE.match(k) or k in ENV_SCRUB_NAMES)
        self.env_base = {k: v for k, v in parent.items() if k not in self.scrubbed}
        self.records, self.keys, self.sid_reg, self.n = [], set(), {}, 0
        self.dry_lines = []

    def env_delta(self, req, outdir):
        d = dict(ENV_FIXED)
        d.update(plan_env(self.plan))
        d.update(VARIANT_ENV.get(self.variant) or {})
        d.update({'KITS': req['kit'], 'OUTDIR': str(outdir), 'CJUNC_RJ': req['rj'], 'CJUNC_PTFE_JLAW': req['law'],
                  'EXPECT_BACKEND': EXPECT_BACKEND})
        if req.get('arm_list') is not None:                  # ★ Z3 — 팔 고르기 (러너: ARMS 와 동시 = 거부 · 팔 수 = 목록 길이)
            d['ARM_LIST'] = ','.join(str(i) for i in req['arm_list'])
        else:
            d['ARMS'] = str(req['arms'])
        if req['c'] != '':
            d['SDCP_MOD_C'] = req['c']
        if req.get('sv_cf'):                                  # ★ 3판 — SV 반사실 대조 (같은 런 안 추가 풀이 · 주 σ · 규약 id 그대로)
            d['CJUNC_SV_CF'] = '1'
        return d

    def run(self, kit, role, law, c, rj, arms, sv_cf=False):
        """런 하나 → 팔 기록 목록.  `arms` = 팔 수 (ARMS · 0..N−1) 또는 팔 번호 튜플 (ARM_LIST · 예 ORIGIN_ARMS) · sv_cf = SV 반사실 켬.
        같은 킷 · 같은 계획 두 번 · 출력 폴더 있음 · 시간 · rc · 팔 계약 = Stop."""
        self.n += 1
        name = f'{self.prefix}{self.n:02d}_{role}'
        al = None if isinstance(arms, int) else sorted(int(i) for i in arms)
        n_arms = int(arms) if al is None else len(al)
        if al is not None and (not al or len(set(al)) != len(al) or al[0] < 0 or al[-1] > 7 or al == list(range(n_arms))):
            raise Stop('NOT_REGISTERED', f'팔 고르기 {al} — 0–7 · 중복 없음 · 0..N−1 접두 아님 (그건 ARMS=N)', name)
        req = {'name': name, 'role': role, 'kit': kit, 'law': law, 'c': c, 'rj': rj, 'arms': n_arms, 'arm_list': al,
               'variant': self.variant, 'sv_cf': bool(sv_cf)}
        key = (kit, variant_raster(kit, self.variant), self.variant, law, c, rj_float(rj), tuple(arm_indices(req)))
        if key in self.keys:
            raise Stop('DUPLICATE_RUN', f'{kit} · {law} · c {c} · R_j {disp_rj(rj)} · 팔 {arm_indices(req)} 를 두 번 요청', name)
        self.keys.add(key)
        #  출력 폴더 = 러너가 강제하는 접미사 그대로 (`_arm<N>` · 팔 고르기면 `_arml<목록>`) — 다르면 러너가 다른 폴더에 쓴다
        sfx = '' if n_arms == 8 and al is None else f'_arm{n_arms}'
        if al is not None:
            sfx += '_arml' + '-'.join(str(i) for i in al)
        outdir = self.out / f'{name}{sfx}'
        delta = self.env_delta(req, outdir)
        if self.dry:
            self.dry_lines.append('  env ' + ' '.join(f'{k}={shlex.quote(delta[k])}' for k in sorted(delta)) + f' bash {self.runner}')
            print(self.dry_lines[-1])
            return None
        if outdir.exists() and any(outdir.iterdir()):
            raise Stop('OUTDIR_NOT_EMPTY', f'{outdir} — 러너 SKIP 캐시가 옛 팔을 재사용한다', name)
        left = self.deadline - time.time()
        if left <= 0:
            raise Stop('TIME_LIMIT', '시간 상한 (--max-hours) 을 넘었다', name)
        (self.out / 'logs').mkdir(parents=True, exist_ok=True)
        rec = dict(req, outdir=outdir.name, rc=None, seconds=None, arms_read=[])
        self.records.append(rec)
        t0 = time.time()
        logp = self.out / 'logs' / f'{name}.log'
        with open(logp, 'w', encoding='utf-8') as lf:
            try:
                r = subprocess.run(['bash', str(self.runner)], cwd=str(self.root), env=dict(self.env_base, **delta),
                                   stdout=lf, stderr=subprocess.STDOUT, timeout=left)
            except subprocess.TimeoutExpired:
                rec['seconds'] = round(time.time() - t0, 3)
                raise Stop('TIME_LIMIT', f'{name}: 시간 상한 안에 끝나지 않았다', name)
        rec['rc'], rec['seconds'] = r.returncode, round(time.time() - t0, 3)
        if r.returncode != 0:
            raise Stop('RUNNER_RC', f'rc {r.returncode} (로그 {logp})', name)
        try:
            arms_ = read_run(outdir, req, self.plan, self.contract, self.sid_reg)
        except Stop:
            #  읽기가 멈춰도 팔 파일 sha256 은 남긴다 — 등록 결과 (NOT_COMPUTED) 로 끝난 사다리를 판정이 원 팔에서 다시 계산할 수 있게.
            rec['arms_read'] = arm_file_shas(outdir)
            raise
        rec['arms_read'] = [{k: a[k] for k in ARM_PUBLIC} for a in arms_]
        a0 = arms_[0]
        ok = '✓' if all(x is True for x in a0['cert_pass']) else ('— (조기 반환 · 솔브 없음)' if a0['state'] != 'positive' else '✗')
        print(f'  {name}: {role} · R_j {disp_rj(rj)} · {law} · c {c or "-"} · 팔 {arm_indices(req)}{" · SV 반사실" if sv_cf else ""} → rc 0 · '
              f'{rec["seconds"]:.1f} s · 상태 {a0["state"]} · cg_info {a0["cg_info"]} · CG 반복 {a0["cg_iters"]} · 이어 풀기 '
              f'{a0["resolve_iters"]} · 잔차 {_e(a0["cg_resid"])} · 판 전류 불균형 {_e(a0["imbalance"])} · 증서 ⓐⓑⓒⓓ {ok} · '
              f'판독 보장 오차 e {_e(a0["err_rel"])}')
        return arms_


class Replay:
    """판정 단계의 fetch — 기록된 런을 순서대로 대조해 원 팔 JSON 을 다시 읽는다 (sha256 대조 · 같은 계약)."""

    def __init__(self, stage_dir, summary, plan, contract, sid_reg, cert_reg=None):
        self.dir, self.plan, self.contract, self.sid_reg = Path(stage_dir), plan, contract, sid_reg
        self.recs = list(summary.get('runs') or [])
        self.variant = summary.get('variant')
        self.i = 0
        self.cert_reg = {} if cert_reg is None else cert_reg

    def run(self, kit, role, law, c, rj, arms, sv_cf=False):
        if self.i >= len(self.recs):
            raise Stop('REPLAY_MISMATCH', f'{self.dir.name}: 다시 계산이 {role} · R_j {disp_rj(rj)} 를 요구하는데 기록에 더 없다')
        r = self.recs[self.i]
        al = None if isinstance(arms, int) else sorted(int(i) for i in arms)
        want = (kit, role, law, c, rj, int(arms) if al is None else len(al), al, bool(sv_cf))
        got = (r.get('kit'), r.get('role'), r.get('law'), r.get('c'), r.get('rj'), r.get('arms'), r.get('arm_list'), r.get('sv_cf'))
        if want != got or r.get('rc') != 0 or r.get('variant') != self.variant:
            raise Stop('REPLAY_MISMATCH', f'{self.dir.name}: 다시 계산 {want} ≠ 기록 {got} (rc {r.get("rc")!r})', r.get('name'))
        self.i += 1
        req = {k: r.get(k) for k in REQ_KEYS}
        arms_ = read_run(self.dir / r['outdir'], req, self.plan, self.contract, self.sid_reg,
                         want_sha=[a.get('sha256') for a in r.get('arms_read') or []])
        self.cert_reg[f'{self.dir.name}/{r["name"]}'] = [a['dsigma_rel'] for a in arms_]   # §8 수렴 증서 ⓒ 값 (판정 결과로만)
        return arms_

    def done(self):
        if self.i != len(self.recs):
            raise Stop('REPLAY_MISMATCH', f'{self.dir.name}: 기록에 다시 계산이 쓰지 않은 런 {len(self.recs) - self.i} 개')


# ═════════════════════════ 보정 사다리 (§3-1 – §3-3) ═════════════════════════
def end_pick(lad, side, X):
    """§3-2b ①–③ — 끝 하나 (arm 0): 끝 표적 X 를 사다리 규칙 그대로 끼운다 → 끼는 이웃 안 ln–ln 보간 = 후보 → 끝 확인 런 (후보 R 에서
    SBE arm 0) → 후보가 바깥 (lo: σ ≥ T⁺ · hi: σ ≤ T⁻) 이면 그 후보 · 아니면 그 점을 사다리에 넣고 **바깥 실측 이웃** (σ ≥ T⁺ 인 가장 큰 R ·
    σ ≤ T⁻ 인 가장 작은 R) → (끝 키, 기록).  반올림 없음 (끝 = 확인된 후보 또는 실측 점 · §10-2 ⑫ 3판).
    ★ 4판 (Q2-2 · ③″) — 확인 · 바깥 이웃 판정 = 판독 보호 띠 (`outside_band` · e = 그 점 런의 증서 보장 오차) · 끼우기 (후보 제안) 는 판독 그대로."""
    lo = side == 'lo'
    (Ra, ka, sa), (Rb, kb, sb) = lad._bracket_to(X, 'end_point')
    cand = rj_key(interp_lnln(Ra, sa, Rb, sb, X))
    reused = cand in lad.pts
    sc = lad.pts[cand][1] if reused else lad._get('end_confirm', cand)
    ok = outside_band(sc, X, lo, lad.err[cand])
    end = cand if ok else lad._outer_neighbor(X, lo)
    return end, {'bracket': [ka, kb], 'candidate': cand, 'confirm_reused': reused, 'confirm_ok': ok,
                 'source': 'candidate' if ok else 'outer_neighbor'}


def end_origin_push(lad, side, X, end):
    """★ Q-E (사전 리뷰 PRE-design-01 · 1저자 10-21 권고대로) — 끝에서 arm 1 · 2 도 돌려 세 origin 의 SBE 가 모두 띠 밖이어야 끝이다 ·
    하나라도 띠 안 (lo: σ < T⁺ · hi: σ > T⁻) 이면 끝을 다음 **바깥 실측 이웃** 으로 (없으면 같은 쪽 ×100 새 점 · 사다리 셈) → 세 origin
    허용집합의 합집합을 바깥에서 감싼다 (W = 그 끝들로).  → (끝 키, 민 횟수, 본 끝 목록).  origin 팔 런은 점 수에 안 센다 (§10-2 ③ 셈 그대로).
    ★ 4판 (Q2-2 · ③″) — 띠 밖 판정 = 판독 보호 띠 (팔마다 그 런 증서의 보장 오차)."""
    lo = side == 'lo'
    pushes, seen = 0, []
    while True:
        if outside_band(lad.pts[end][1], X, lo, lad.err[end]):
            s12 = lad._org('end_origin', end)
            seen.append(end)
            if all(outside_band(s, X, lo, e) for s, e in zip(s12, lad.org_err[end])):
                return end, pushes, seen
        pushes += 1
        end = lad._next_out(end, lo)


class Ladder:
    """fetch(role, rj, arms) → 팔 기록 목록 · arm 0 σ 로 점을 고른다.  공개 상태 (st) 에는 σ 가 없다 · 봉인 칸 (sealed) 은 판정만 연다.
    max_points = 계획 점 수 상한 (⬜ 등록) · ratio_max = 계획 역상 R 비 상한 (float · 'none')."""

    def __init__(self, fetch, target_ms=None, max_points=None, ratio_max=PLAN_NO_CAP):
        if not (type(max_points) is int and max_points >= 1):    # noqa: E721
            raise Stop('PLAN_NUMBER_UNREGISTERED', f'점 수 상한 {max_points!r} (계획 칸 · ⬜ 결과 전 등록)')
        self.fetch = fetch
        self.T = (TARGET_SBE_MS if target_ms is None else target_ms) * 1e-3
        self.max_points, self.ratio_max = max_points, ratio_max
        self.st = {'order': [], 'n_runs': 0, 'n_ext': 0, 'n_bisect': 0, 'bracket': None, 'local_e_ge_emin': None, 'confirms': [],
                   'flat_pairs': [], 'states': {}, 'err_rel': {}, 'R_j0': None, 'R_j_lo': None, 'R_j_hi': None, 'ends': {}, 'R_ratio': None,
                   'ratio_cap': ratio_max, 'width_ok': None, 'origin': None, 'origin_runs': []}
        self.sealed = {'points': {}, 'e': None, 'delta': None, 'origin': None, 'ends_sigma': {}, 'origin_points': {}}
        self.pts = {}            # 키 → (R, σ arm 0) — 사다리 점 (센다)
        self.org = {}            # 키 → [σ arm 1, σ arm 2] — origin 팔 (끝 · R_j,0 공용 · 같은 R 두 번 안 돈다 · 안 센다)
        self.err = {}            # ★ 4판 (Q2-2 · ③″) 키 → 판독 보장 오차 e (arm 0 · 그 런 증서 ⓓ · σ 아님 → 공개 st['err_rel'])
        self.org_err = {}        # 키 → [e arm 1, e arm 2]
        self.flags = []

    def _get(self, role, key):
        if self.st['n_runs'] >= self.max_points:
            raise Stop('CALIB_LADDER_EXHAUSTED', f'점 수 상한 {self.max_points} (계획) — 다음 {role} R_j {disp_rj(key)} 를 돌리지 않는다')
        recs = self.fetch(role, key, 1)
        s = recs[0]['sigma']
        e = arm_err(recs[0])
        self.st['n_runs'] += 1
        self.st['order'].append(key)
        self.st['states'][key] = recs[0].get('state', 'positive')
        self.st['err_rel'][key] = e
        self.pts[key] = (rj_float(key), s)
        self.err[key] = e
        self.sealed['points'][key] = s
        self._monotone()
        return s

    def _org(self, role, key):
        if key not in self.org:
            r12 = self.fetch(role, key, ORIGIN_ARMS)
            self.org_err[key] = [arm_err(x) for x in r12]
            self.org[key] = [x['sigma'] for x in r12]
            self.st['origin_runs'].append({'role': role, 'rj': key})
            self.sealed['origin_points'][key] = list(self.org[key])
        return self.org[key]

    def _monotone(self):
        """§3-2 비단조 — R 이 커지는데 ln σ 가 τ_mono 넘게 오르면 멈춤 · 확장 실수 그대로 (바닥 0 은 끝 점이라 위반이 못 된다 ·
        유한 R 의 0 다음 양수 = +∞ 오름 = 위반 · ★ 4판 Q1: 천장 단락은 NOT_COMPUTED 라 점으로 오지 않는다)."""
        ps = sorted((R, k, s) for k, (R, s) in self.pts.items())
        for (_ra, ka, sa), (_rb, kb, sb) in zip(ps, ps[1:]):
            d = ln_diff(sa, sb)
            if d > TAU_MONO:
                raise Stop('CALIB_NONMONOTONE', f'R_j {disp_rj(ka)} → {disp_rj(kb)} 에서 ln σ 가 τ_mono {TAU_MONO:g} 넘게 오른다 '
                                                '(구현 결함 의심)')
            if 0.0 < d < math.inf and [ka, kb] not in self.st['flat_pairs']:
                self.st['flat_pairs'].append([ka, kb])           # τ 안 흔들림 = 평탄으로 기록 (멈추지 않는다)

    def _fin(self):
        """유한 R 점 (σ 는 0 일 수 있다) · 그중 양의 유한 σ (bracket · 보간 · §5-0 ②)."""
        finR = sorted((R, k, s) for k, (R, s) in self.pts.items() if 0.0 < R < math.inf)
        return finR, [x for x in finR if 0.0 < x[2] < math.inf]

    def _bracket_to(self, X, role):
        """§3-2 사다리 규칙 — X 를 끼는 양의 유한 이웃 둘 (같은 쪽 ×100 · 로그 중점 · 이웃 비 ≤ 10^0.5) → ((Ra, ka, sa), (Rb, kb, sb))."""
        while True:
            finR, fin = self._fin()
            br = None
            for a, b in zip(fin, fin[1:]):
                if min(a[2], b[2]) <= X <= max(a[2], b[2]):
                    br = (a, b)
                    break
            if br is None:
                if not fin or X > max(x[2] for x in fin):
                    e_new = math.log10(finR[0][0]) - LADDER_EXT_LOG10      # 더 큰 σ 가 필요 → 작은 R 쪽
                else:
                    e_new = math.log10(finR[-1][0]) + LADDER_EXT_LOG10
                self.st['n_ext'] += 1
                self._get(role, rj_key(10.0 ** e_new))
                continue
            (Ra, ka, sa), (Rb, kb, sb) = br
            if math.log10(Rb / Ra) > NEIGHBOR_LOG10_MAX + 1e-9:
                self.st['n_bisect'] += 1
                self._get(role, rj_key(10.0 ** ((math.log10(Ra) + math.log10(Rb)) / 2.0)))
                continue
            return br

    def _outer_neighbor(self, X, lo):
        """§3-2b ③ 바깥 실측 이웃 — lo: σ ≥ T⁺ 인 가장 큰 유한 R · hi: σ ≤ T⁻ 인 가장 작은 유한 R (3판 = 끼는 이웃이 늘 하나 있다).
        ★ 4판 (Q2-2 · ③″) — '바깥' = 판독 보호 띠 (`outside_band` · 그 점의 e) · 띠에 걸친 점만 남아 바깥 실측 점이 하나도 없으면 (모호 = 보수 쪽 ·
        끝을 바깥으로) 사다리 규칙 그대로 같은 쪽 ×100 새 점을 돈다 (③′ 의 '없으면 바깥 ×100 연장' 과 같은 꼴 · 점 수 상한이 끝낸다 =
        CALIB_LADDER_EXHAUSTED · ③″ 반례의 '사다리가 먼저 소진된다')."""
        while True:
            finR, _fin = self._fin()
            pool = [(R, k) for R, k, s in finR if outside_band(s, X, lo, self.err[k])]
            if pool:
                return (max(pool) if lo else min(pool))[1]
            edge = finR[0][0] if lo else finR[-1][0]
            self.st['n_ext'] += 1
            self._get('end_point', rj_key(10.0 ** (math.log10(edge) + (-LADDER_EXT_LOG10 if lo else LADDER_EXT_LOG10))))

    def _next_out(self, end, lo):
        """끝을 한 칸 바깥으로 — 다음 실측 유한 점 (lo = 더 작은 R · hi = 더 큰 R) · 없으면 같은 쪽 ×100 새 점 (사다리 셈 · 상한이 끝낸다)."""
        R = rj_float(end)
        finR, _fin = self._fin()
        cand = [(r, k) for r, k, _s in finR if (r < R if lo else r > R)]
        if cand:
            return (max(cand) if lo else min(cand))[1]
        key = rj_key(10.0 ** (math.log10(R) + (-LADDER_EXT_LOG10 if lo else LADDER_EXT_LOG10)))
        self.st['n_ext'] += 1
        self._get('end_point', key)
        return key

    def run(self):
        T = self.T
        sF = self._get('floor', LIMIT_RJ['floor'])
        sC = self._get('ceiling', LIMIT_RJ['ceiling'])
        if not (sF <= T <= sC):
            raise Stop('CALIB_IMPOSSIBLE', '1.63 mS/cm 이 [바닥, 천장] 밖 (값은 봉인)')
        #  §3-1 · §5-0 ② — 바닥 zero (σ 0) 는 정상 (|0/T − 1| = 1 → EDGE 아님) · ★ 4판 (Q1) 천장 단락 (ELECTRODE_SHORT) = 게시 안 됨 →
        #    천장 런에서 이미 NOT_COMPUTED (사유 ELECTRODE_SHORT · `read_run`) — 여기 오지 않는다 · ★ 4판 (Q2-2 · ③″) 판독 보호 띠 — 걸치면 EDGE
        if edge_hit(sF, self.err[LIMIT_RJ['floor']], T) or edge_hit(sC, self.err[LIMIT_RJ['ceiling']], T):
            raise Stop('CALIB_EDGE', f'1.63 이 바닥 또는 천장의 {CONFIRM_TOL:.0%} 안 (판독 보호 띠 포함 · §3-2b ③″) — R_j,0 가 하나로 안 정해진다')
        for e in LADDER_START_LOG10:
            self._get('point', rj_key(10.0 ** e))
        while True:
            (Ra, ka, sa), (Rb, kb, sb) = self._bracket_to(T, 'point')
            self.st['bracket'] = [ka, kb]
            e = elasticity(Ra, sa, Rb, sb)
            self.sealed['e'] = e
            self.st['local_e_ge_emin'] = bool(e >= E_MIN)         # ★ 3판 — 국소 진단 (보고 · 멈추지 않는다 · RCA-01)
            R0 = sig3(interp_lnln(Ra, sa, Rb, sb, T))
            k0 = rj_key(R0)
            reused = k0 in self.pts
            s0 = self.pts[k0][1] if reused else self._get('confirm', k0)
            ok = abs(s0 / T - 1.0) <= CONFIRM_TOL
            self.st['confirms'].append({'rj': k0, 'ok': ok, 'reused': reused})
            if ok:
                self.st['R_j0'] = k0
                self.sealed['delta'] = math.log(s0 / T)
                break
            if len(self.st['confirms']) >= MAX_CONFIRM:
                raise Stop('CALIB_UNCONFIRMED', f'확인 {MAX_CONFIRM} 번 다 ±{CONFIRM_TOL:.0%} 밖 (값은 봉인)')
        self._ends()

    def _ends(self):
        """§3-2b — 실제 SBE 역상 양끝 (+ ★ Q-E 세 origin 합집합) · 폭 R_j,hi/R_j,lo · 상한 (계획 · 'none' = 상한 없음)."""
        T = self.T
        ends = {}
        for side, X, tag in (('lo', T * (1.0 + CONFIRM_TOL), 'T+ = 1.63 × 1.02'), ('hi', T * (1.0 - CONFIRM_TOL), 'T- = 1.63 × 0.98')):
            end, ent = end_pick(self, side, X)
            end2, pushes, seen = end_origin_push(self, side, X, end)
            ent.update(target=tag, arm0_end=end, end=end2, origin_pushes=pushes, origin_checked=seen,
                       source=(ent['source'] if pushes == 0 else 'outer_neighbor_origin'))
            ends[side] = ent
            self.sealed['ends_sigma'][side] = self.pts[end2][1]
        self.st['ends'] = ends
        self.st['R_j_lo'], self.st['R_j_hi'] = ends['lo']['end'], ends['hi']['end']
        ratio = rj_float(self.st['R_j_hi']) / rj_float(self.st['R_j_lo'])
        self.st['R_ratio'] = ratio
        if self.ratio_max == PLAN_NO_CAP:
            self.st['width_ok'] = None
        else:
            self.st['width_ok'] = bool(ratio <= float(self.ratio_max))
            if not self.st['width_ok']:
                raise Stop('CALIB_UNIDENTIFIED', f'실제 역상 R 비 R_j,hi/R_j,lo 가 계획 상한 {self.ratio_max} 를 넘는다 (§3-2b ④ · 보정 폭이 넓다)')

    def origin(self):
        """§3-3 — R_j,0 에서 arm 1 · 2 (★ Z3 — `ARM_LIST=1,2` 한 런 · a0 = 확인 팔 값 그대로 · 다시 돌지 않는다 · 끝 origin 과 같은 R 이면
        그 런 그대로) → ln(max/min) ≤ 0.02 · 넘으면 8 팔 평균 (`ARMS=8` 한 런) · 표지 (R_j,0 그대로)."""
        k0 = self.st['R_j0']
        s0 = self.pts[k0][1]
        vals = [s0] + list(self._org('origin', k0))
        ok, sp = sbe_origin_ok(vals)
        o = {'status': 'pass' if ok else 'sensitive', 'arm_list': list(ORIGIN_ARMS), 'mean8': False}
        self.sealed['origin'] = {'spread': sp, 'arms': vals, 'mean8': None}
        if not ok:
            r8 = self.fetch('origin8', k0, 8)
            o['mean8'] = True
            self.sealed['origin']['mean8'] = mean_ext([x['sigma'] for x in r8])
            self.flags.append('CALIB_ORIGIN_SENSITIVE')
        self.st['origin'] = o


# ═════════════════════════ 예측 (§4-1 · §4-2) ═════════════════════════
RJ_ROLES = ('R_j_lo', 'R_j0', 'R_j_hi')
#: §4-2 3판 (RCA-02) — DBE origin 을 점검하는 R (세 R 모두 · 2판 = R_j,0 만) · 넘으면 그 모서리 세 R 전부 8 팔 평균 (RJ_ROLES)
ORIGIN_CHECK_ROLES = RJ_ROLES


class Predict:
    """fetch(kit, role, law, c, rj, arms, sv_cf).  ladders = {법칙: {'R_j0', 'R_j_lo', 'R_j_hi', 'r0_sigma'}} (사다리에서 읽은 값 그대로).
    ★ 3판 — 주 판정 · 감도 변이가 같은 판정 함수 (네 모서리 × 세 R · DBE origin 세 R · §5-6 · RCA-09) · sv_scope (주 판정만) = SV 반사실을
    켤 모서리 런 ('R_j0' · 'all3')."""

    def __init__(self, fetch, ladders, variant, sv_scope=None):
        self.fetch, self.ladders, self.variant, self.sv_scope = fetch, ladders, variant, sv_scope
        self.main = variant is None
        self.checks = {'sbe_noop': [], 'same_p': []}
        self.origin = []
        self.vals = {}                       # (c, 법칙, 역할) → arm 0 팔 기록
        self.adj = {}                        # (c, 법칙, 역할) → 8 팔 평균 (origin 규칙이 바꾼 모서리 · 세 R 전부)
        self.sealed = {'W0': None, 'origin': {}}

    def _sv_on(self, rr):
        return self.main and (self.sv_scope == 'all3' or (self.sv_scope == 'R_j0' and rr == 'R_j0'))

    def run(self):
        if self.variant != 'SVORDER':        # SBE c 1 no-op — 주 · FIBRE · UNREG · GRID (SVORDER = 주 사다리 · SDCP 0 침대 양보 = no-op)
            for law in LAWS:
                r = self.fetch(SBE_KIT, 'sbe_noop', law, '1', self.ladders[law]['R_j0'], 1)[0]
                ok = r['sigma'] == self.ladders[law]['r0_sigma'] and r['n_sdcp_near'] == 0
                self.checks['sbe_noop'].append({'law': law, 'ok': ok})
                if not ok:
                    raise Stop('SAME_P_CONSISTENCY', f'SBE c 1 ↔ c 0 (사다리 R_j,0 확인 팔) 비트 다름 또는 SDCP 근접 '
                                                     f'{r["n_sdcp_near"]!r} ≠ 0 ({law}) — S3 이 SBE 에서 no-op 이 아니다')
        for law in LAWS:
            for rr in RJ_ROLES:
                for c in CS:
                    self.vals[(c, law, rr)] = self.fetch(DBE_KIT, 'corner', law, c, self.ladders[law][rr], 1, self._sv_on(rr))[0]
                d = ln_diff(self.vals[('0', law, rr)]['sigma'], self.vals[('1', law, rr)]['sigma'])
                ok = d >= -TAU_MONO
                self.checks['same_p'].append({'law': law, 'rj_role': rr, 'ok': ok})
                if not ok:
                    raise Stop('SAME_P_CONSISTENCY', f'σ_DBE(c1, {law}) < σ_DBE(c0, {law}) − τ_mono at {rr} — 같은 그래프 · 같은 R_j 에서 '
                                                     f'Rayleigh 순서 위반 (구현 결함)')
        W0 = ln_spread([v['sigma'] for v in self.vals.values()])
        W_pos = w_pos_of([v['sigma'] for v in self.vals.values()])     # ★ 4판 (Q2-3 · §4-2 ②) — W ∈ {+∞, 0} 일 때 문턱의 W
        self.sealed['W0'] = W0
        self.sealed['W_pos'] = W_pos
        for law in LAWS:
            for c in CS:
                ent = {'c': c, 'law': law, 'status': 'pass', 'arm_list': list(ORIGIN_ARMS), 'per_R': {}, 'states_differ': []}
                so = {}
                over = False
                for rr in ORIGIN_CHECK_ROLES:        # §4-2 3판 — 세 R 모두 (RCA-02)
                    a0r = self.vals[(c, law, rr)]
                    r12 = self.fetch(DBE_KIT, 'origin', law, c, self.ladders[law][rr], ORIGIN_ARMS)
                    vv = [a0r['sigma']] + [x['sigma'] for x in r12]
                    sts = [a0r.get('state', 'positive')] + [x.get('state', 'positive') for x in r12]
                    ok, sp = dbe_origin_ok(vv, W0, states=sts, w_pos=W_pos)   # ★ 4판 (Q2-3 · §4-2 ①) 상태 다름 = 넘음
                    ent['per_R'][rr] = 'pass' if ok else 'over'
                    if len(set(sts)) > 1:
                        ent['states_differ'].append(rr)
                    so[rr] = {'spread': sp, 'arms': vv, 'states': sts}
                    over = over or not ok
                if over:                             # 한 R 이라도 넘으면 그 모서리 세 R 전부 같은 8 origin 집합의 평균
                    ent['status'] = 'adjusted'
                    for rr in RJ_ROLES:
                        r8 = self.fetch(DBE_KIT, 'origin8', law, c, self.ladders[law][rr], 8)
                        m8 = mean_ext([x['sigma'] for x in r8])
                        self.adj[(c, law, rr)] = m8
                        so[rr]['mean8'] = m8
                self.origin.append(ent)
                self.sealed['origin'][f'c{c}_{law}'] = so

    def values(self):
        """모서리 값 (S/cm · 확장 실수) — origin 규칙이 바꾼 모서리는 세 R 전부 8 팔 평균 (§4-2 3판)."""
        return {k: (self.adj[k] if k in self.adj else r['sigma']) for k, r in self.vals.items()}

    def states(self):
        return {k: r.get('state', 'positive') for k, r in self.vals.items()}


# ═════════════════════════ 단계 공통 ═════════════════════════
def summary_base(stage, a):
    return {'tool': TOOL, 'schema': SCHEMA, 'stage': stage, 'status': None, 'stop': None, 'flags': [],
            'code': {'chain': git_identity(HERE / 'rint_r_chain.py'),
                     'runner': (git_identity(a.runner) if getattr(a, 'runner', None) else None),
                     'runner_path': (str(Path(a.runner).resolve()) if getattr(a, 'runner', None) else None)},
            'constants': {'target_sbe_mScm': TARGET_SBE_MS, 'confirm_tol': CONFIRM_TOL, 'e_min': E_MIN, 'tau_mono': TAU_MONO,
                          'neighbor_log10_max': NEIGHBOR_LOG10_MAX, 'origin_sbe_max': ORIGIN_SBE_MAX,
                          'origin_dbe_frac_w': ORIGIN_DBE_FRAC_W}}


def outdir_empty_or_stop(out):
    out = Path(out)
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise Stop('OUTDIR_NOT_EMPTY', f'{out} — 새 --out 을 쓸 것 (그 폴더에는 아무것도 쓰지 않는다)')


def env_forbidden_or_stop(env=None):
    env = os.environ if env is None else env
    hit = [k for k in ENV_FORBIDDEN if k in env]
    if hit:
        raise Stop('ENV_SIGMA_VGCF_OVERRIDE', f'{hit} 가 env 에 있다 — unset 하고 다시 (SIGMA_FIBRE_BULK 와 함께면 러너 거부 · §10)')


def write_json(path, obj):
    Path(path).write_bytes(canon_bytes(_clean(obj)))


def print_stop(e):
    print(f'멈춤 [{e.code}] {STOPS.get(e.code, e.code)} — {e.cause}' + (f' (런 {e.run})' if e.run else ''))


def read_summary(d, name):
    p = Path(d) / name
    try:
        raw = p.read_bytes()
        return json.loads(raw.decode('utf-8')), hashlib.sha256(raw).hexdigest()
    except (OSError, UnicodeDecodeError, ValueError):
        return None, None


def same_code(a, b):
    """코드 지문 대조 (HEAD) — 단계마다 같은 핀 작업 트리여야 한다 (등록 R §10 (0))."""
    return (a or {}).get('head') == (b or {}).get('head')


def _e(x):
    return f'{x:.1e}' if isinstance(x, (int, float)) and not isinstance(x, bool) else repr(x)


def check_after_main(after_dir, plan_sha, s0_sha, code):
    """★ Q-F — 감도 단계 = 주 판정 단계 (사다리 둘 · 예측) 가 끝난 뒤에만: 주 예측 요약 = PREDICTED · 변이 없음 · 같은 계획 · 같은 S0 계획 ·
    같은 사슬 코드 → 묶음 기록 {dir, summary_sha256} (판정이 판정 입력의 주 예측과 대조한다)."""
    if not after_dir:
        raise Stop('MAIN_NOT_DONE', '--variant 인데 --after-main (주 예측 폴더) 이 없다 — 감도는 주 판정 단계가 끝난 뒤에만 (Q-F)')
    d = Path(after_dir).resolve()
    s, sha = read_summary(d, 'predict_summary.json')
    if s is None or s.get('tool') != TOOL or s.get('schema') != SCHEMA or s.get('stage') != 'predict':
        raise Stop('MAIN_NOT_DONE', f'{d}: 이 사슬의 주 예측 요약이 아니다')
    if s.get('variant') is not None or s.get('status') != 'PREDICTED':
        raise Stop('MAIN_NOT_DONE', f'{d.name}: 변이 {s.get("variant")!r} · 상태 {s.get("status")!r} — 주 예측 (변이 없음 · PREDICTED) 이어야')
    if (s.get('plan') or {}).get('sha256') != plan_sha or (s.get('s0_plan') or {}).get('sha256') != s0_sha:
        raise Stop('MAIN_NOT_DONE', f'{d.name}: 주 예측의 계획 · S0 계획 ≠ 이 감도 단계의 것')
    if not same_code((s.get('code') or {}).get('chain'), (code or {}).get('chain')):
        raise Stop('MAIN_NOT_DONE', f'{d.name}: 주 예측의 사슬 코드 ≠ 지금 사슬 코드')
    return {'dir': str(d), 'summary_sha256': sha}


# ═════════════════════════ (3) 사다리 단계 ═════════════════════════
def stage_ladder(a, contract):
    out = Path(a.out)
    try:
        outdir_empty_or_stop(out)
    except Stop as e:
        print_stop(e)
        return 3
    s = summary_base('ladder', a)
    s.update({'law': a.law, 'variant': a.variant, 'kit': a.kit or SBE_KIT, 'runs': [], 'ladder': None, 'env_scrubbed': [],
              'after_main': None})
    ran = False
    try:
        if not _same(a.target, TARGET_SBE_MS) or a.law not in LAWS or (a.kit or SBE_KIT) != SBE_KIT or a.variant == 'SVORDER':
            raise Stop('NOT_REGISTERED', f'--target {a.target} (등록 {TARGET_SBE_MS}) · --law {a.law} · --kit {a.kit} '
                                         f'(등록 {SBE_KIT}) · --variant {a.variant} (SVORDER 는 사다리 없음 — 주 사다리 그대로)')
        env_forbidden_or_stop()
        plan, plan_sha = load_plan(a.plan)
        s['plan'] = {'path': str(Path(a.plan).resolve()), 'sha256': plan_sha, 'content': plan}
        s['registration'] = check_plan_registered(plan_sha, a.registration)
        s['s0_plan'] = load_s0_plan(a.s0_plan, a.registration, plan)
        require_plan_numbers(plan)
        #  ★ PF2 B (10-22 · Q2) — S0 단계 2 보고가 봉인한 계획 해시 = 지금 두 계획 (정확히 · DBE 열람 전 계획 하나)
        s['s0_reports'] = {'stage2': read_s0_stage2(a.s0_stage2_report, plan_sha, s['s0_plan']['sha256'])}
        s['constants']['max_ladder_points'] = ladder_cap(plan)
        if a.variant is not None:
            s['after_main'] = check_after_main(a.after_main, plan_sha, s['s0_plan']['sha256'], s['code'])
        for p in (Path(a.root) / SBE_KIT, Path(a.runner)):
            if not p.exists():
                raise Stop('KIT_MISSING', f'{p}')
        rn = Runner(a.runner, a.root, out, plan, a.variant, time.time() + a.max_hours * 3600.0, contract, dry=a.dry_run, prefix='L')
        s['env_scrubbed'] = rn.scrubbed
        if a.dry_run:
            print(f'dry-run — 사다리 {a.law} · 첫 런 (바닥 · 천장 · 1e4 · 1e6 · 1e8) 의 env (러너를 부르지 않는다 · 다음 점은 σ 로 정해진다)')
            for role, rj in (('floor', 'inf'), ('ceiling', '0')) + tuple(('point', rj_key(10.0 ** e)) for e in LADDER_START_LOG10):
                rn.run(SBE_KIT, role, a.law, LADDER_C, rj, 1)
            return 0
        out.mkdir(parents=True, exist_ok=True)
        ran = True
        print(f'사다리 {a.law}{" · 변이 " + a.variant if a.variant else ""} — SBE arm 0 · LEAN 2 · 표적 {TARGET_SBE_MS} mS/cm '
              f'(값은 봉인 — 상태 · 반복 · 잔차 · 시간만)')
        lad = Ladder(lambda role, rj, arms: rn.run(SBE_KIT, role, a.law, LADDER_C, rj, arms), max_points=ladder_cap(plan),
                     ratio_max=plan['calib_rj_ratio_max'])
        try:
            try:
                lad.run()
                lad.origin()                   # §3-3 — 주 · 감도 변이 같게 (같은 판정 함수 · §5-6 3판)
                s['status'] = 'CALIBRATED'
            finally:
                s['ladder'], s['flags'] = lad.st, list(lad.flags)
                s['runs'] = rn.records
        except Stop as e:
            s['status'] = e.code if e.code in REGISTERED_OUTCOMES else 'STOPPED'
            raise
    except Stop as e:
        s['stop'] = e.record()
        if s['status'] is None:
            s['status'] = 'STOPPED'
        print_stop(e)
    if a.dry_run and not ran:
        return 3
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / 'ladder_summary.json', s)
    L = s.get('ladder') or {}
    if s['status'] == 'CALIBRATED':
        e_lo, e_hi = (L.get('ends') or {}).get('lo') or {}, (L.get('ends') or {}).get('hi') or {}
        print(f'보정 = CALIBRATED · R_j,0 = {disp_rj(L["R_j0"])} · R_j,lo {disp_rj(L["R_j_lo"])} ({e_lo.get("source")}) · R_j,hi '
              f'{disp_rj(L["R_j_hi"])} ({e_hi.get("source")}) · 역상 R 비 {L["R_ratio"]:.4g} · 런 {L["n_runs"]} · ×100 {L["n_ext"]} · '
              f'반씩 {L["n_bisect"]} · 확인 {len(L["confirms"])} · 국소 e ≥ e_min {L["local_e_ge_emin"]} · origin {(L["origin"] or {}).get("status")}'
              + (f' · 표지 {s["flags"]}' if s['flags'] else ''))
    else:
        print(f'보정 = {s["status"]}' + (f' (사유 {(s.get("stop") or {}).get("reason")})' if (s.get('stop') or {}).get('reason') else ''))
    print(f'요약 → {out / "ladder_summary.json"}')
    return 0 if s['status'] == 'CALIBRATED' else 3


# ═════════════════════════ (4) 예측 단계 ═════════════════════════
def load_ladders(dirs, variant, reg_path, contract, sid_reg):
    """사다리 요약 둘 → {법칙: {...}} · 계획 · S0 계획 · 코드 · 변이 사다리의 주 예측 묶음.  R_j 는 요약에서 그대로 (사람이 옮겨 적지 않는다) ·
    R_j,0 확인 팔을 다시 읽는다."""
    want_var = None if variant == 'SVORDER' else variant
    out, plan, plan_sha, code, s0, after = {}, None, None, None, None, None
    s0reps, first = None, True
    seen = set()
    for d in dirs:
        rd = Path(d).resolve()
        if rd in seen:
            raise Stop('DUPLICATE_RUN', f'같은 사다리 폴더 두 번 {rd}')
        seen.add(rd)
        s, sha = read_summary(rd, 'ladder_summary.json')
        if s is None or s.get('stage') != 'ladder' or s.get('tool') != TOOL or s.get('schema') != SCHEMA:
            raise Stop('LADDER_SET', f'{rd}: 이 사슬 (3판) 의 ladder_summary.json 이 없다')
        if s.get('status') != 'CALIBRATED':
            raise Stop('LADDER_NOT_CALIBRATED', f'{rd.name}: 사다리 상태 {s.get("status")} — 예측하지 않는다 (판정 = 그 이름)')
        if s.get('variant') != want_var:
            raise Stop('LADDER_SET', f'{rd.name}: 사다리 변이 {s.get("variant")!r} ≠ {want_var!r}')
        law = s.get('law')
        if law in out:
            raise Stop('DUPLICATE_RUN', f'{law} 사다리가 둘 ({out[law]["dir"]} · {rd}) — 같은 킷 · 같은 계획 두 번')
        if plan_sha is not None and s['plan']['sha256'] != plan_sha:
            raise Stop('PLAN_HASH_MISMATCH', '두 사다리의 계획이 다르다')
        if s0 is not None and (s.get('s0_plan') or {}).get('sha256') != s0.get('sha256'):
            raise Stop('S0_PLAN_HASH_MISMATCH', '두 사다리의 S0 계획이 다르다')
        if code is not None and not same_code(s.get('code', {}).get('chain'), code.get('chain')):
            raise Stop('CODE_PIN_MISMATCH', '두 사다리의 사슬 코드가 다르다')
        if after is not None and s.get('after_main') != after:
            raise Stop('MAIN_NOT_DONE', '두 변이 사다리의 주 예측 묶음이 다르다')
        if not first and s.get('s0_reports') != s0reps:      # ★ PF2 B — 두 사다리가 같은 단계 2 봉인을 읽었나
            raise Stop('S0_REPORT_MISMATCH', '두 사다리의 S0 단계 보고 기록이 다르다')
        first, s0reps = False, s.get('s0_reports')
        plan, plan_sha, code, s0, after = s['plan']['content'], s['plan']['sha256'], s.get('code') or {}, s.get('s0_plan'), s.get('after_main')
        L = s['ladder']
        r0run = [r for r in s['runs'] if r.get('rj') == L['R_j0'] and r.get('arms') == 1 and r.get('arm_list') is None
                 and r.get('role') in ('confirm', 'point')]
        if not r0run:
            raise Stop('LADDER_SET', f'{rd.name}: R_j,0 확인 팔 기록이 없다')
        r = r0run[-1]
        req = {k: r.get(k) for k in REQ_KEYS}
        arm = read_run(rd / r['outdir'], req, plan, contract, sid_reg, want_sha=[x['sha256'] for x in r['arms_read']])[0]
        out[law] = {'dir': str(rd), 'summary_sha256': sha, 'variant': s.get('variant'), 'R_j0': L['R_j0'], 'R_j_lo': L['R_j_lo'],
                    'R_j_hi': L['R_j_hi'], 'r0_sigma': arm['sigma']}
    if sorted(out) != sorted(LAWS):
        raise Stop('LADDER_SET', f'사다리 법칙 {sorted(out)} ≠ {list(LAWS)}')
    check_plan_registered(plan_sha, reg_path)
    s0rec = recheck_s0_record(s0, reg_path, plan)
    require_plan_numbers(plan)
    why = s0_reports_problem(s0reps, plan_sha, s0rec['sha256'])   # ★ PF2 B — 사다리 기록의 단계 2 봉인 = 이 계획 (같은 함수로 다시)
    if why:
        raise Stop('S0_REPORT_MISMATCH', why)
    return out, plan, plan_sha, code, s0rec, after, s0reps


def stage_predict(a, contract):
    out = Path(a.out)
    try:
        outdir_empty_or_stop(out)
    except Stop as e:
        print_stop(e)
        return 3
    s = summary_base('predict', a)
    s.update({'variant': a.variant, 'kit': a.kit or DBE_KIT, 'runs': [], 'ladders': {}, 'checks': None, 'origin': None,
              'env_scrubbed': [], 'after_main': None, 'sv_cf': None})
    ran = False
    try:
        if (a.kit or DBE_KIT) != DBE_KIT:
            raise Stop('NOT_REGISTERED', f'--kit {a.kit} (등록 {DBE_KIT})')
        env_forbidden_or_stop()
        sid_reg = {}
        lads, plan, plan_sha, code, s0rec, lad_after, s0reps = load_ladders(a.ladders, a.variant, a.registration, contract, sid_reg)
        if not same_code(code.get('chain'), s['code']['chain']):
            raise Stop('CODE_PIN_MISMATCH', '사다리 사슬 코드 ≠ 지금 사슬 코드 (같은 핀 작업 트리에서 돌릴 것)')
        s['ladders'] = {k: {kk: v[kk] for kk in ('dir', 'summary_sha256', 'variant', 'R_j0', 'R_j_lo', 'R_j_hi')} for k, v in lads.items()}
        s['plan'] = {'sha256': plan_sha, 'content': plan}
        s['s0_plan'] = s0rec
        s['s0_reports'] = s0reps                             # ★ PF2 B — 사다리가 읽은 단계 2 봉인 (판정이 다시 대조)
        s['registration'] = check_plan_registered(plan_sha, a.registration)
        if a.variant is not None:
            s['after_main'] = check_after_main(a.after_main, plan_sha, s0rec['sha256'], s['code'])
            if a.variant != 'SVORDER' and lad_after != s['after_main']:
                raise Stop('MAIN_NOT_DONE', '변이 사다리가 묶인 주 예측 ≠ --after-main (같은 주 판정 단계 뒤여야)')
        scope = plan['sv_cf_scope'] if a.variant is None else None
        s['sv_cf'] = {'scope': scope, 'threshold': (plan['sv_cf_threshold'] if a.variant is None else None)}
        for p in (Path(a.root) / SBE_KIT, Path(a.root) / DBE_KIT, Path(a.runner)):
            if not p.exists():
                raise Stop('KIT_MISSING', f'{p}')
        rn = Runner(a.runner, a.root, out, plan, a.variant, time.time() + a.max_hours * 3600.0, contract, dry=a.dry_run, prefix='P')
        rn.sid_reg = sid_reg
        s['env_scrubbed'] = rn.scrubbed
        pr = Predict(rn.run, lads, a.variant, sv_scope=scope)
        if a.dry_run:
            print('dry-run — 예측 런의 env (러너를 부르지 않는다 · origin 런은 arm 0 값으로 정해진다)')
            if a.variant != 'SVORDER':
                for law in LAWS:
                    rn.run(SBE_KIT, 'sbe_noop', law, '1', lads[law]['R_j0'], 1)
            for law in LAWS:
                for rr in RJ_ROLES:
                    for c in CS:
                        rn.run(DBE_KIT, 'corner', law, c, lads[law][rr], 1, pr._sv_on(rr))
            return 0
        out.mkdir(parents=True, exist_ok=True)
        ran = True
        print(f'예측{" · 변이 " + a.variant if a.variant else ""} — DBE arm 0 · 네 모서리 × {{R_j,lo · R_j,0 · R_j,hi}} · origin 세 R '
              f'(값은 봉인){" · SV 반사실 범위 " + str(scope) if scope else ""}')
        try:
            try:
                pr.run()
                s['status'] = 'PREDICTED'
            finally:
                s['checks'], s['origin'], s['runs'] = pr.checks, pr.origin, rn.records
        except Stop as e:
            #  ★ 4판 (Q1) — NOT_COMPUTED (풀이 · 증서 실패 · 단락 ELECTRODE_SHORT) = 예측 단계의 등록 결과 (사다리와 같은 뜻 · 판정이 원 팔에서
            #    다시 계산해 이름 · 사유를 남긴다) · 그 밖 멈춤 (계약 · 기록 · 일관 검사 …) = STOPPED (판정 입력 아님)
            s['status'] = e.code if e.code in PREDICT_OUTCOMES else 'STOPPED'
            raise
    except Stop as e:
        s['stop'] = e.record()
        if s['status'] is None:
            s['status'] = 'STOPPED'
        print_stop(e)
    if a.dry_run and not ran:
        return 3
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / 'predict_summary.json', s)
    if s['status'] == 'PREDICTED':
        n_adj = sum(1 for o in (s['origin'] or []) if o['status'] == 'adjusted')
        print(f'예측 = PREDICTED · 런 {len(s["runs"])} · 같은 P 일관 통과 · origin 규칙이 옮긴 모서리 {n_adj}')
    else:
        print(f'예측 = {s["status"]}' + (f' (사유 {(s.get("stop") or {}).get("reason")})' if (s.get('stop') or {}).get('reason') else ''))
    print(f'요약 → {out / "predict_summary.json"}')
    return 0 if s['status'] == 'PREDICTED' else 3


# ═════════════════════════ (5) 판정 단계 ═════════════════════════
def _replay_ladder(d, s, contract, sid_reg, cert_reg):
    plan = s['plan']['content']
    rp = Replay(d, s, plan, contract, sid_reg, cert_reg)
    lad = Ladder(lambda role, rj, arms: rp.run(SBE_KIT, role, s['law'], LADDER_C, rj, arms), max_points=ladder_cap(plan),
                 ratio_max=plan['calib_rj_ratio_max'])
    status, stop = 'CALIBRATED', None
    try:
        lad.run()
        lad.origin()
    except Stop as e:
        if e.code not in REGISTERED_OUTCOMES:
            raise
        status, stop = e.code, e.record()                     # ★ 4판 (Q1) — 등록 결과의 사유 (멈춤 기록 · 원 팔에서 다시 계산)
    rp.done()
    if status != s.get('status') or lad.st != s.get('ladder') or lad.flags != s.get('flags'):
        diff = [k for k in set(lad.st) | set(s.get('ladder') or {}) if lad.st.get(k) != (s.get('ladder') or {}).get(k)]
        raise Stop('REPLAY_MISMATCH', f'{Path(d).name}: 원 팔에서 다시 계산한 사다리 ≠ 요약 (상태 {status} ↔ {s.get("status")} · 칸 {sorted(diff)})')
    return {'status': status, 'stop': stop, 'st': lad.st, 'sealed': lad.sealed, 'flags': lad.flags, 'pts': lad.pts}


def _replay_predict(d, s, lads, contract, sid_reg, cert_reg):
    """예측 단계 다시 계산 → (Predict, 상태 PREDICTED | NOT_COMPUTED, 멈춤 기록 | None) · ★ 4판 (Q1) — NOT_COMPUTED (단락 · 증서 실패) = 등록
    결과 (사다리 `_replay_ladder` 와 같은 꼴) · 다시 계산한 상태 · 검사 · origin 결정 ≠ 요약 = REPLAY_MISMATCH."""
    rp = Replay(d, s, s['plan']['content'], contract, sid_reg, cert_reg)
    pr = Predict(rp.run, lads, s.get('variant'), sv_scope=(s.get('sv_cf') or {}).get('scope'))
    status, stop = 'PREDICTED', None
    try:
        pr.run()
    except Stop as e:
        if e.code not in PREDICT_OUTCOMES:
            raise
        status, stop = e.code, e.record()
    rp.done()
    if status != s.get('status') or pr.checks != s.get('checks') or pr.origin != s.get('origin'):
        raise Stop('REPLAY_MISMATCH', f'{Path(d).name}: 원 팔에서 다시 계산한 예측 (상태 {status} ↔ {s.get("status")}) · 검사 · origin 결정 '
                                      f'≠ 요약')
    return pr, status, stop


def _why(stage, law, variant, stop):
    """★ 4판 (Q1) — 판정 기록의 사유 한 줄 (§5-5b NOT_COMPUTED · CALIB_* 행 '사유 (상태 · 멈춤 코드) 보고') — 멈춤 기록에서 (σ 를 가린 원인 칸)."""
    st = stop or {}
    return {'stage': stage, 'law': law, 'variant': variant, 'code': st.get('code'), 'reason': st.get('reason'), 'run': st.get('run'),
            'cause': st.get('cause')}


def judge_set(statuses, vals):
    """같은 판정 함수 (§5-6 · Codex RCA-09) — 법칙별 사다리 상태 + 예측 값 (S/cm · 확장 실수) → 판정 dict.  주 판정 · 감도 변이가 이것 하나.
    ★ 4판 (Q1 · §5-0 ①) — 사다리 둘이 보정됐는데 vals = None = 예측 단계가 NOT_COMPUTED (등록 결과) → 판정 NOT_COMPUTED.
    ★ 4판 (Q2-1 · §3-2c PRE-design-08) — 두 법칙 이름이 다르면 하나라도 NOT_COMPUTED 면 NOT_COMPUTED (상태 먼저 — 기록이 덜 된 법칙이 있으면
    등록된 결과 이름을 붙이지 않는다 · §5-0 ①) · 아니면 등록 나열 순서 (CALIB_ORDER) 의 첫 CALIB_* · 법칙별 이름은 늘 보고 (판정 기록 calib)."""
    bad = [statuses[law] for law in LAWS if statuses[law] != 'CALIBRATED']
    if bad:
        if 'NOT_COMPUTED' in bad:
            return {'verdict': 'NOT_COMPUTED', 'state': 'calib'}
        return {'verdict': min(bad, key=CALIB_ORDER.index), 'state': 'calib'}
    if vals is None:
        return {'verdict': 'NOT_COMPUTED', 'state': 'calib'}
    return judge({k: v * 1e3 for k, v in vals.items()})


def _end_shift(a, b):
    return [abs(ln_diff(a[i], b[i])) for i in (0, 1)]


def variant_flag(V, vJ, J, vflags):
    """★ 4판 (Q2-5 · 등록 R 4판 §5-6 PRE-design-17 ② ③ ④ · R4-Q8) — 변이 V 의 판정 vJ (같은 판정 함수) ↔ 주 판정 J · 변이 자신의 표지 vflags →
    (표지 | None, 이름 비교 (True 다름 · False 같음 · None 비교 안 함), 사유 | None).  순서 = ③ → ② → ④:
    ③ 변이 판정 NOT_COMPUTED (풀이 · 증서 실패 · 단락 · 멈춤) → <V>_UNCHECKED (결과가 없다 · 이름 비교 안 함 — 3판 = 이름 다름 → _SENSITIVE) ·
    ② 이름 ≠ 주 이름 → <V>_SENSITIVE (CALIB_* 도 결과 이름이라 비교한다) · ④ 이름이 같아도 변이 자신에게 CALIB_ORIGIN_SENSITIVE → <V>_UNCHECKED
    (둔감을 인증하지 않는다) · ⑤ 변이 자신의 표지는 주 표지 목록에 옮기지 않는다 (이 표지로만 · 변이 기록에 늘 보고)."""
    if vJ['verdict'] == 'NOT_COMPUTED':
        return (f'{V}_UNCHECKED', None,
                '변이 판정 NOT_COMPUTED (풀이 · 증서 실패 · 단락 · 멈춤 — 결과가 없다 · 이름 비교 안 함 · §5-6 ③)')
    if vJ['verdict'] != J['verdict']:
        return f'{V}_SENSITIVE', True, f'변이 판정 이름 {vJ["verdict"]} ≠ 주 판정 이름 {J["verdict"]} (같은 판정 함수 · §5-6 ②)'
    if 'CALIB_ORIGIN_SENSITIVE' in (vflags or ()):
        return (f'{V}_UNCHECKED', False,
                '변이 자신의 차단 표지 CALIB_ORIGIN_SENSITIVE (판정 이름은 주와 같다 · 둔감을 인증하지 않는다 · §5-6 ④)')
    return None, False, None


#: ★ 4판 (Q2-4 · §5-5b "표지마다 사유") — 주 판정 표지의 사유 (값 = 판정 결과에만 · 공개 칸에 σ · 비를 싣지 않는다)
WHY_ORIGIN_SENSITIVE = ('세 값 (주 사다리 R_j,0 의 arm 0 · 1 · 2) 의 ln(max/min) > 0.02 — 8 팔 평균 보고 · R_j,0 = arm 0 그대로 (§3-3 · '
                        '값 = 판정 결과에만)')
WHY_NOT_RUN = '안 돌림'


def sv_reasons(flags, det):
    """§5-5b 사유 — SV 표지 (§5-6 SV 행) → {표지: 사유} (대조 비 · 문턱 · 모서리 · 비 값 = 판정 결과에만)."""
    out = {}
    if 'SV_DEPENDENT' in flags:
        out['SV_DEPENDENT'] = (f'대조 비 > 문턱 {det.get("threshold")!r} — 모서리 {SENTENCE_JOIN.join(det.get("dependent") or [])} '
                               f'(범위 {det.get("scope")} · 비 = 판정 결과에만 · §5-6 SV 행)')
    if 'SV_UNCHECKED' in flags:
        parts = []
        if det.get('threshold') is None:
            parts.append('문턱 없음 (계획 sv_cf_threshold null)')
        if det.get('unreadable'):
            parts.append(f'대조 비를 못 읽음 — 모서리 {SENTENCE_JOIN.join(det["unreadable"])}')
        if det.get('straddle'):                         # ★ 10-22 (Q1 (다)) — 괄호가 문턱에 걸침 (비 값 = 판정 결과에만)
            parts.append(f'대조 비 괄호가 문턱에 걸침 (아래 끝 ≤ 문턱 < 위 끝 · 못 가른 덩어리) — 모서리 '
                         f'{SENTENCE_JOIN.join(det["straddle"])}')
        if not det.get('corners'):
            parts.append(f'범위 {det.get("scope")} 안 모서리 기록 없음')
        out['SV_UNCHECKED'] = SENTENCE_JOIN.join(parts) + ' (§5-6 SV 행)'
    return out


def assemble(main, variants, sv):
    """판정 조립 (순수 함수 · 시험이 직접 부른다) → (공개 칸, 결과 칸).
    main = {'statuses', 'vals' (S/cm) | None, 'flags'} · variants = {V: None (안 돌림) | {'statuses', 'vals', 'flags'}} ·
    sv = (표지, 세부) | None (주 예측이 없을 때).
    ★ 4판 — 변이 표지 = `variant_flag` (Q2-5) · 문장 = 결정표 (Q2-4 · `decide_sentence` · 감도 미완료 = 네 변이 중 하나라도 안 돌림 (⑰) ·
    판정 없음 (calib) 이면 None = 해당 없음) · 공개 `blocking_reasons` = 차단 표지마다 사유 (§5-5b)."""
    J = judge_set(main['statuses'], main['vals'])
    flags = list(main.get('flags') or [])
    why = {'CALIB_ORIGIN_SENSITIVE': WHY_ORIGIN_SENSITIVE} if 'CALIB_ORIGIN_SENSITIVE' in flags else {}
    pub_v, res_v = {}, {}
    sens_incomplete = None
    if J['state'] != 'calib':
        if sv is not None:
            flags += sv[0]
            why.update(sv_reasons(sv[0], sv[1] or {}))
        r0 = {k: v for k, v in main['vals'].items() if k[2] == 'R_j0'}
        J['main_R0_only'] = judge({k: v * 1e3 for k, v in r0.items()})      # 중앙 네 점 = 보조 · 보고만 (§5-6 · §10-2 ⑧)
        sens_incomplete = False
        for V in VARIANTS:
            vr = variants.get(V)
            if vr is None:
                pub_v[V] = {'checked': False, 'verdict': None, 'grade_changed': None, 'flag': f'{V}_UNCHECKED'}
                flags.append(f'{V}_UNCHECKED')
                why[f'{V}_UNCHECKED'] = WHY_NOT_RUN
                sens_incomplete = True                          # ⑰ — 감도 변이를 다 돌리기 전
                continue
            vJ = judge_set(vr['statuses'], vr['vals'])
            vf = sorted(set(vr.get('flags') or []))
            flag, changed, reason = variant_flag(V, vJ, J, vf)
            pub_v[V] = {'checked': True, 'verdict': vJ['verdict'], 'grade_changed': changed, 'flags': vf, 'flag': flag}
            if flag:
                flags.append(flag)
                why[flag] = reason
            ent = {'verdict': vJ['verdict'], 'judge': vJ}
            if vJ['state'] != 'calib':
                sh = _end_shift(vJ['interval_mScm'], J['interval_mScm'])
                ent.update(end_shift_log=sh, end_shift_exceeds_0p1G0=max(sh) > SENS_SHIFT_FRAC_G0 * G0)
                ent['variant_R0_only'] = judge({k: v * 1e3 for k, v in vr['vals'].items() if k[2] == 'R_j0'})
            res_v[V] = ent
    flags = sorted(set(flags))
    blocking = blocking_of(flags)
    sentence = decide_sentence(J['state'], J['verdict'], blocking, sens_incomplete=bool(sens_incomplete))
    pub = {'verdict': J['verdict'], 'state': J['state'], 'flags': flags, 'blocking_flags': blocking,
           'blocking_reasons': {f: why.get(f) for f in blocking}, 'sensitivity_incomplete': sens_incomplete,
           'sentence_allowed': J['verdict'] == 'PASS_INFORMATIVE' and not blocking, 'sentence': sentence,
           'variants': pub_v}
    return pub, {'judge': J, 'variants': res_v}


#: 판정 조립 (`assemble`) 의 공개 칸 → verdict.json (★ 4판 — 차단 표지 사유 · 감도 미완료 칸을 더했다)
PUB_FROM_ASSEMBLE = ('verdict', 'state', 'flags', 'blocking_flags', 'blocking_reasons', 'sensitivity_incomplete', 'sentence_allowed',
                     'sentence')


def verdict_compute(dirs, reg_path, contract):
    """판정 계산기 (§5 · 설계 §7) — 원 팔 JSON 전부에서.  → (공개 dict, 결과 dict | None).  입력 계약 실패 = Stop."""
    pub = {'tool': TOOL, 'schema': SCHEMA, 'stage': 'verdict', 'verdict': None, 'state': None, 'stop': None, 'flags': [],
           'blocking_flags': [], 'blocking_reasons': {}, 'sensitivity_incomplete': None, 'qualifiers': list(QUALIFIERS),
           'report_category': {REPORT_CATEGORY: list(ASSUMED_UNVALIDATED)},
           'verdict_note': VERDICT_NOTE, 'sentence_allowed': False, 'sentence': None, 'calib': {}, 'variants': {},
           'inputs': [], 'arms': [], 'registration': None, 'grid_sentence': GRID_SENTENCE, 'reasons': []}
    stages, seen = [], set()
    for d in dirs:
        rd = Path(d).resolve()
        if rd in seen:
            raise Stop('DUPLICATE_RUN', f'같은 입력 폴더 두 번 {rd}')
        seen.add(rd)
        got = [(n, *read_summary(rd, n)) for n in ('ladder_summary.json', 'predict_summary.json')]
        got = [(n, s, h) for n, s, h in got if s is not None]
        if len(got) != 1:
            raise Stop('INPUT_NOT_STAGE', f'{rd}: 단계 요약 {len(got)} 개 (1 이어야)')
        _n, s, h = got[0]
        if s.get('tool') != TOOL or s.get('schema') != SCHEMA:
            raise Stop('INPUT_NOT_STAGE', f'{rd}: 이 사슬 (3판) 의 요약이 아니다')
        stages.append((rd, s, h))
    stages.sort(key=lambda x: (x[1].get('variant') or '', x[1].get('stage'), x[1].get('law') or '', str(x[0])))
    plan_hash, reg_sha = registration_plan_hash(reg_path)
    s0_hash, _reg = registration_s0_hash(reg_path)
    pub['registration'] = {'path': str(Path(reg_path).resolve()), 'sha256': reg_sha, 'plan_hash': plan_hash, 's0_plan_hash': s0_hash}
    code0 = None
    plan = None
    s0r0, s0r_first = None, True
    for rd, s, h in stages:
        pub['inputs'].append({'dir': str(rd), 'stage': s.get('stage'), 'law': s.get('law'), 'variant': s.get('variant'),
                              'status': s.get('status'), 'summary_sha256': h})
        if stopped_stage_rejects_verdict(s):                 # ★ RI — 주 판정 단계만 (감도 변이 단계 = §5-6 ③ · 아래 입력 검사는 그대로)
            raise Stop('INPUT_STAGE_STOPPED', f'{rd.name}: {(s.get("stop") or {}).get("code")} — 멈춘 주 판정 단계는 판정 입력이 아니다')
        if (s.get('plan') or {}).get('sha256') != plan_hash:
            raise Stop('PLAN_HASH_MISMATCH', f'{rd.name}: 계획 sha256 ≠ 등록 §2-1 개정값')
        plan = (s.get('plan') or {}).get('content')
        recheck_s0_record(s.get('s0_plan'), reg_path, plan)
        require_plan_numbers(plan)
        #  ★ PF2 B (10-22 · Q2) — 단계마다 기록한 S0 단계 2 봉인 = 등록 계획 · S0 계획 (같은 함수) · 단계끼리 같은 기록
        why = s0_reports_problem(s.get('s0_reports'), plan_hash, s0_hash)
        if why:
            raise Stop('S0_REPORT_MISMATCH', f'{rd.name}: {why}')
        if not s0r_first and s.get('s0_reports') != s0r0:
            raise Stop('S0_REPORT_MISMATCH', f'{rd.name}: S0 단계 보고 기록 ≠ 다른 판정 입력 단계의 기록')
        s0r_first, s0r0 = False, s.get('s0_reports')
        c = (s.get('code') or {})
        key = ((c.get('chain') or {}).get('head'), (c.get('runner') or {}).get('head'), c.get('runner_path'))
        if code0 is None:
            code0 = key
            now = git_identity(HERE / 'rint_r_chain.py').get('head')
            if now != key[0]:
                raise Stop('CODE_PIN_MISMATCH', f'지금 사슬 HEAD {now} ≠ 단계를 만든 사슬 {key[0]} — 판정 계산기도 같은 핀에서 (다시 판정 = 같은 코드)')
        elif key != code0:
            raise Stop('CODE_PIN_MISMATCH', f'{rd.name}: 코드 {key} ≠ {code0}')
        for r in s.get('runs') or []:
            for x in r.get('arms_read') or []:
                pub['arms'].append({'path': str(rd / r['outdir'] / x['file']), 'sha256': x['sha256']})
    lad_in, pred_in = {}, {}
    for rd, s, h in stages:
        k = (s.get('variant'), s.get('law')) if s.get('stage') == 'ladder' else s.get('variant')
        tgt = lad_in if s.get('stage') == 'ladder' else pred_in
        if k in tgt:
            raise Stop('DUPLICATE_RUN', f'같은 단계 두 번 {k} ({tgt[k][0].name} · {rd.name})')
        tgt[k] = (rd, s, h)
    sid_reg, cert_reg = {}, {}
    res = {'reference': {'exp_dbe_mScm': EXP_DBE_MS, 'cur_gen_dbe_mScm': CUR_GEN_DBE_MS, 'cur_gen_sigma_star_dbe_S_cm': CUR_GEN_SIGMA_STAR_DBE,
                         'exp_ratio_dbe_sbe': EXP_RATIO, 'G0': G0}, 'ladders': {}, 'variants': {}}

    def ladders_of(variant):
        out = {}
        for law in LAWS:
            if (variant, law) not in lad_in:
                return None
            rd, s, h = lad_in[(variant, law)]
            #  ★ RI (§5-6 ③) — 멈춘 감도 변이 사다리 = 그 법칙 NOT_COMPUTED (다시 계산 없음 · 표지 없음) → 변이 판정 NOT_COMPUTED → <V>_UNCHECKED
            out[law] = (rd, s, h, ({'status': 'NOT_COMPUTED', 'stop': s.get('stop'), 'st': None, 'sealed': None, 'flags': [], 'pts': None}
                                   if variant_stage_stopped(s) else _replay_ladder(rd, s, contract, sid_reg, cert_reg)))
        return out
    main_l = ladders_of(None)
    if main_l is None:
        raise Stop('INPUT_MISSING', '주 사다리 P0 · P1 둘이 다 있어야 한다')
    m_flags = []
    for law, (rd, s, h, L) in main_l.items():
        pub['calib'][law] = L['status']
        m_flags += L['flags']
        res['ladders'][law] = {'status': L['status'], 'R_j0': L['st']['R_j0'], 'R_j_lo': L['st']['R_j_lo'], 'R_j_hi': L['st']['R_j_hi'],
                               'R_ratio': L['st']['R_ratio'], 'ends': L['st']['ends'], 'local_e_ge_emin': L['st']['local_e_ge_emin'],
                               'floor_mScm': L['sealed']['points'].get('inf', math.nan) * 1e3,
                               'ceiling_mScm': L['sealed']['points'].get('0', math.nan) * 1e3,
                               'states': L['st']['states'], 'e': L['sealed']['e'],
                               'e_over_emin': (L['sealed']['e'] / E_MIN if isinstance(L['sealed']['e'], float) else None),
                               'delta': L['sealed']['delta'], 'points_mScm': {k: v * 1e3 for k, v in L['sealed']['points'].items()},
                               'origin_points_mScm': {k: [x * 1e3 for x in v] for k, v in L['sealed']['origin_points'].items()},
                               'ends_sigma_mScm': {k: v * 1e3 for k, v in L['sealed']['ends_sigma'].items()},
                               'origin': L['sealed']['origin']}
    statuses = {law: main_l[law][3]['status'] for law in LAWS}
    #  ★ 4판 (Q1 · §5-5b NOT_COMPUTED · CALIB_* 행) — 판정 기록의 사유 (주 판정 단계만 · 원 팔에서 다시 계산한 멈춤 기록)
    pub['reasons'] = [_why('ladder', law, None, main_l[law][3]['stop']) for law in LAWS if statuses[law] != 'CALIBRATED']

    def predict_of(variant, lads):
        if variant not in pred_in:
            return None
        rd, s, h = pred_in[variant]
        for law in LAWS:
            ref = (s.get('ladders') or {}).get(law) or {}
            if ref.get('summary_sha256') != lads[law][2]:
                raise Stop('PREDICT_LADDER_MISMATCH', f'{rd.name}: {law} 사다리 요약 sha256 ≠ 판정 입력')
        if variant_stage_stopped(s):
            return None, 'STOPPED', s.get('stop')             # ★ RI (§5-6 ③) — 멈춘 감도 변이 예측 = 값 없음 → 그 변이 판정 NOT_COMPUTED
        lin = {law: {'R_j0': lads[law][3]['st']['R_j0'], 'R_j_lo': lads[law][3]['st']['R_j_lo'], 'R_j_hi': lads[law][3]['st']['R_j_hi'],
                     'r0_sigma': lads[law][3]['pts'][lads[law][3]['st']['R_j0']][1]} for law in LAWS}
        return _replay_predict(rd, s, lin, contract, sid_reg, cert_reg)
    if any(st != 'CALIBRATED' for st in statuses.values()):
        P, PJ = assemble({'statuses': statuses, 'vals': None, 'flags': m_flags}, {}, None)
        pub.update({k: P[k] for k in PUB_FROM_ASSEMBLE})
        res['certificates_dsigma_rel'] = dict(cert_reg)
        return pub, _clean(res)
    got_pr = predict_of(None, main_l)
    if got_pr is None:
        raise Stop('INPUT_MISSING', '주 예측 폴더가 없다 (사다리 둘 다 보정됨)')
    pr, p_status, p_stop = got_pr
    if p_status != 'PREDICTED':
        #  ★ 4판 (Q1 · §5-0 ① ③ · §4-2 ③) — 예측 단계 NOT_COMPUTED (DBE 모서리 · origin 팔의 단락 · 증서 실패) = 판정 NOT_COMPUTED (등록 결과 ·
        #    rc 0 · 멈춤 아님) · 사유 = 그 멈춤 기록 · 감도 · SV 대조는 보지 않는다 (주 판정이 없다)
        pub['reasons'].append(_why('predict', None, None, p_stop))
        P, PJ = assemble({'statuses': statuses, 'vals': None, 'flags': m_flags}, {}, None)
        pub.update({k: P[k] for k in PUB_FROM_ASSEMBLE})
        res['predict'] = {'status': p_status, 'stop': p_stop}
        res['certificates_dsigma_rel'] = dict(cert_reg)
        return pub, _clean(res)
    main_pred_sha = pred_in[None][2]
    vals = pr.values()
    plan_main = pred_in[None][1]['plan']['content']
    svf, svd = sv_assess(pr.vals, plan_main['sv_cf_threshold'], plan_main['sv_cf_scope'])
    vres = {}
    for V in VARIANTS:
        vl = main_l if V == 'SVORDER' else ladders_of(V)
        if V != 'SVORDER' and vl is None:
            vres[V] = None
            continue
        for d_ in ([pred_in[V]] if V in pred_in else []) + ([vl[law][:3] for law in LAWS] if V != 'SVORDER' else []):
            if (d_[1].get('after_main') or {}).get('summary_sha256') != main_pred_sha:      # ★ Q-F — 감도 = 이 주 예측 뒤에
                raise Stop('MAIN_BINDING', f'{d_[0].name}: 감도 단계가 묶인 주 예측 ≠ 판정 입력의 주 예측')
        vst = {law: vl[law][3]['status'] for law in LAWS}
        vflags = [] if V == 'SVORDER' else [f for law in LAWS for f in vl[law][3]['flags']]
        if all(x == 'CALIBRATED' for x in vst.values()):
            vp = predict_of(V, vl)
            if vp is None:
                vres[V] = None                          # 사다리는 됐는데 예측을 안 돌렸다 = 안 돌림
                continue
            vpr, v_status, _v_stop = vp
            #  ★ 4판 (Q1) — 변이 예측 NOT_COMPUTED (등록 결과) = 그 변이 판정 NOT_COMPUTED (vals None · `judge_set`)
            vres[V] = {'statuses': vst, 'vals': (vpr.values() if v_status == 'PREDICTED' else None), 'flags': vflags}
        else:
            vres[V] = {'statuses': vst, 'vals': None, 'flags': vflags}
    P, PJ = assemble({'statuses': statuses, 'vals': vals, 'flags': m_flags}, vres, (svf, svd))
    pub.update({k: P[k] for k in PUB_FROM_ASSEMBLE + ('variants',)})
    J = PJ['judge']
    res.update({k: J[k] for k in ('interval_mScm', 'I_law_mScm', 'in_law', 'in_U', 'in_E', 'W', 'p', 'p_why', 'd', 'd_over_G0',
                                  'direction', 'd_to_U', 'S', 'S_why', 'sigma_mid_mScm')})
    res['state'] = J['state']
    res['main_R0_only'] = J['main_R0_only']
    ms = {k: v * 1e3 for k, v in vals.items()}
    st_ = pr.states()
    res['corners_mScm'] = {f'c{c}_{law}': {rr: ms[(c, law, rr)] for rr in RJ_ROLES} for c in CS for law in LAWS}
    res['corners_state'] = {f'c{c}_{law}': {rr: st_[(c, law, rr)] for rr in RJ_ROLES} for c in CS for law in LAWS}
    res['corners_arm0_mScm'] = {f'c{c}_{law}': {rr: pr.vals[(c, law, rr)]['sigma'] * 1e3 for rr in RJ_ROLES} for c in CS for law in LAWS}
    res['origin'] = {'W0': pr.sealed['W0'], 'W_pos': pr.sealed['W_pos'], 'corners': pr.sealed['origin'],
                     'adjusted_mean8_mScm': {f'c{c}_{law}_{rr}': v * 1e3 for (c, law, rr), v in pr.adj.items()}}
    #  §6 s — R_j,lo ↔ R_j,hi 의 실제 역상 구간 할선 (분모 = 끝 두 점의 실제 Δ ln σ_SBE · §3-2b ⑦ · §10-2 ⑰ 3판)
    s_ = {}
    for c in CS:
        for law in LAWS:
            es = main_l[law][3]['sealed']['ends_sigma']
            den = ln_diff(es['hi'], es['lo'])
            num = ln_diff(vals[(c, law, 'R_j_hi')], vals[(c, law, 'R_j_lo')])
            s_[f'c{c}_{law}'] = (num / den if (math.isfinite(num) and math.isfinite(den) and den > 0) else None)
    res['s'] = s_
    res['P_effect_log'] = {f'c{c}': ln_diff(vals[(c, 'P0', 'R_j0')], vals[(c, 'P1', 'R_j0')]) for c in CS}
    res['c_effect_log'] = {law: ln_diff(vals[('0', law, 'R_j0')], vals[('1', law, 'R_j0')]) for law in LAWS}
    res['ratio_dbe_sbe'] = {f'c{c}_{law}': ms[(c, law, 'R_j0')] / TARGET_SBE_MS for c in CS for law in LAWS}
    res['dissipation_share'] = {f'c{c}_{law}_{rr}': pr.vals[(c, law, rr)]['dissipation_share'] for c in CS for law in LAWS for rr in RJ_ROLES}
    res['sv_local_dissipation'] = {f'c{c}_{law}_{rr}': pr.vals[(c, law, rr)].get('sv_local') for c in CS for law in LAWS
                                   for rr in RJ_ROLES}   # §5-6 진단 · 차단 표지 아님 (RCA-06)
    res['sv_counterfactual'] = svd
    res['variants'] = PJ['variants']
    res['certificates_dsigma_rel'] = dict(cert_reg)          # §8 수렴 증서 ⓒ (런마다 · 판정 결과로만)
    return pub, _clean(res)


def _clean(obj):
    """결과 JSON — NaN · inf 를 null 로 (allow_nan=False 직렬화 · 다시 판정 바이트 대조 · +∞ (zero 끝의 W 등) 는 상태 칸이 따로 적는다)."""
    if isinstance(obj, dict):
        return {str(k): _clean(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_clean(v) for v in obj]
    if isinstance(obj, float) and not math.isfinite(obj):
        return None
    return obj


def _stopped_pub(e, dirs, reg):
    """판정 계산기가 멈춤 (계약 · 기록 · 재현 · 입력 — 등록 판정 이름이 아닌 Stop 코드) → NOT_COMPUTED 기록 (§5-5 PRE-design-09 행 · ★ 4판 §5-5b
    NOT_COMPUTED 칸 = *"판정 없음 — 사유 (상태 · 멈춤 코드) 보고"* · 사유 = 그 멈춤 기록 · rc 3)."""
    rec = e.record()
    return {'tool': TOOL, 'schema': SCHEMA, 'stage': 'verdict', 'verdict': 'NOT_COMPUTED', 'state': 'calib', 'stop': rec, 'flags': [],
            'blocking_flags': [], 'blocking_reasons': {}, 'sensitivity_incomplete': None, 'qualifiers': list(QUALIFIERS),
            'report_category': {REPORT_CATEGORY: list(ASSUMED_UNVALIDATED)},
            'verdict_note': VERDICT_NOTE, 'sentence_allowed': False, 'sentence': decide_sentence('calib', 'NOT_COMPUTED', []),
            'calib': {}, 'variants': {}, 'grid_sentence': GRID_SENTENCE, 'inputs': [str(Path(d).resolve()) for d in dirs], 'arms': [],
            'registration': (str(Path(reg).resolve()) if reg else None), 'reasons': [_why('verdict', None, None, rec)]}


def stage_verdict(a, contract):
    if a.reverify:
        return reverify(a.reverify, contract)
    out = Path(a.out)
    try:
        outdir_empty_or_stop(out)
    except Stop as e:
        print_stop(e)
        return 3
    rc_ = 0
    try:
        pub, res = verdict_compute(a.runs, a.registration, contract)
    except Stop as e:
        print_stop(e)
        pub, res, rc_ = _stopped_pub(e, a.runs, a.registration), None, 3
    pub['input_dirs'] = [str(Path(d).resolve()) for d in a.runs]
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / 'verdict.json', pub)
    if res is not None:
        write_json(out / 'verdict_results.json', res)
        try:
            os.chmod(out / 'verdict_results.json', 0o600)
        except OSError:
            pass
    print(f'판정 = {pub["verdict"]} (상태 {pub.get("state")}) · 표지 {pub["flags"] or "없음"} · 차단 {pub.get("blocking_flags") or "없음"} · '
          f'§7-1 문장 {"허용" if pub["sentence_allowed"] else "금지"}' + (f' · 사다리 {pub["calib"]}' if pub.get('calib') else '')
          + (' · 사유 ' + ' · '.join(f'{w.get("stage")} {w.get("law") or ""} {w.get("code")} {w.get("reason") or ""}'.replace('  ', ' ').strip()
                                    for w in pub['reasons']) if pub.get('reasons') else ''))
    if a.show_results:
        if res is None:
            print('--show-results — 판정이 없어 열지 않는다 (멈춤)')
        else:
            print('══ 판정 결과 (값 열림 · 판정에 쓰는 런이 다 끝났다 · 등록 R §4-1) ══')
            print(canon_bytes(res).decode('utf-8'))
            with open(out / 'views.jsonl', 'a', encoding='utf-8') as f:
                f.write(json.dumps({'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                                    'results_sha256': sha256_file(out / 'verdict_results.json')}) + '\n')
    print(f'판정 → {out / "verdict.json"}')
    return rc_


def reverify(vdir, contract):
    """다시 판정 (읽기 전용) — 같은 입력 (판정 JSON 에 적힌 폴더 · 등록) 으로 다시 계산해 두 JSON 을 바이트 대조."""
    vdir = Path(vdir)
    try:
        old_pub = (vdir / 'verdict.json').read_bytes()
        pub0 = json.loads(old_pub.decode('utf-8'))
    except (OSError, UnicodeDecodeError, ValueError) as e:
        print(f'REVERIFY_DIFF — {vdir / "verdict.json"} 를 못 읽는다 ({type(e).__name__})')
        return 1
    rp = vdir / 'verdict_results.json'
    old_res = rp.read_bytes() if rp.exists() else None
    dirs = pub0.get('input_dirs') or []
    reg = (pub0.get('registration') or {}).get('path') if isinstance(pub0.get('registration'), dict) else pub0.get('registration')
    try:
        pub, res = verdict_compute(dirs, reg, contract)
    except Stop as e:
        pub, res = _stopped_pub(e, dirs, reg), None
    pub['input_dirs'] = dirs
    new_pub, new_res = canon_bytes(_clean(pub)), (canon_bytes(res) if res is not None else None)
    if new_pub == old_pub and new_res == old_res:
        print(f'REVERIFY_SAME — 판정 JSON · 결과 JSON 바이트 같음 ({len(dirs)} 입력 · 판정 {pub["verdict"]})')
        return 0
    keys = sorted(k for k in set(pub) | set(pub0) if _clean(pub).get(k) != pub0.get(k))
    print(f'REVERIFY_DIFF — 다시 계산한 판정이 저장본과 다르다 (공개 칸 {keys} · 결과 {"같음" if new_res == old_res else "다름"})'
          + (f' · 멈춤 {pub["stop"]["code"]}' if pub.get('stop') else ''))
    return 1


# ═════════════════════════ CLI ═════════════════════════
def main(argv=None, contract=None):
    try:                                   # ★ SELF-122 — 화면을 파일로 돌려도 줄마다 바로 쓴다
        sys.stdout.reconfigure(line_buffering=True)
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--stage', choices=('ladder', 'predict', 'verdict'), default='ladder')
    ap.add_argument('--law', choices=LAWS, help='ladder — PTFE–접합 법칙 끝')
    ap.add_argument('--target', type=float, default=TARGET_SBE_MS, help='ladder — 등록 표적 (1.63 이 아니면 멈춤)')
    ap.add_argument('--variant', choices=VARIANTS, default=None, help='감도 (등록 R §5-6 · 필수 · 주 판정 단계 뒤에만 — --after-main)')
    ap.add_argument('--after-main', default=None, help='ladder · predict 의 --variant — 끝난 주 예측 폴더 (Q-F · 판정이 묶음을 대조한다)')
    ap.add_argument('--kit', default=None, help=f'ladder = {SBE_KIT} · predict = {DBE_KIT} (등록 · 다르면 멈춤)')
    ap.add_argument('--runner')
    ap.add_argument('--root', help='킷 폴더가 있는 곳 = 러너 작업 폴더')
    ap.add_argument('--plan', help='ladder — R 런 계획 파일 (rint-r-plan-v2 · 등록 §2-1 개정 커밋의 대상 · sha256 = 그 칸)')
    ap.add_argument('--s0-plan', help='ladder — S0 단계 1 계획 (ca-cjunc-plan-v1 · 정준 바이트 · sha256 = 등록 §2-1 S0 계획 해시 칸) · '
                                      '두 계획 대조 (§2-1 · §10-2 ⑪)')
    ap.add_argument('--s0-stage2-report', help='ladder — S0 단계 2 보고 (s0_stage2_<DBE 킷>.json · ca_s0_census) · 그 보고가 봉인한 계획 '
                                               '해시 (R 계획 · S0 계획) = 지금 계획이어야 돈다 (★ PF2 B · Q2 · 등록 R §2-1b · §11 ④)')
    ap.add_argument('--registration', default=str(REGISTRATION_DEFAULT), help='등록 R 문서 (§2-1 계획 해시 · S0 계획 해시를 읽는다)')
    ap.add_argument('--ladders', nargs='+', help='predict — 사다리 폴더 둘 (P0 · P1)')
    ap.add_argument('--runs', nargs='+', help='verdict — 사다리 · 예측 · 감도 폴더 전부')
    ap.add_argument('--reverify', help='verdict — 판정 폴더를 같은 입력으로 다시 판정 (읽기 전용 · 바이트 대조)')
    ap.add_argument('--out', help='새 출력 폴더 (없거나 비어 있어야)')
    ap.add_argument('--max-hours', type=float, help='ladder · predict — 시간 상한 (등록 §10 · 숫자 탐침 뒤의 값 · 기본값 없음)')
    ap.add_argument('--dry-run', action='store_true', help='ladder · predict — 런 env 만 찍는다 (러너 · 출력 폴더 없음)')
    ap.add_argument('--show-results', action='store_true', help='verdict 만 — 판정에 쓰는 런이 다 끝난 뒤 값을 연다 (열람 기록)')
    a = ap.parse_args(argv)
    contract = RealContract() if contract is None else contract
    if a.show_results and a.stage != 'verdict':
        ap.error('--show-results 는 --stage verdict 에서만 (등록 R §4-1 — 판정에 쓰는 런이 다 끝난 뒤 한 번)')
    if a.after_main and not a.variant:
        ap.error('--after-main 은 --variant (감도 단계) 와만')
    if a.stage == 'ladder':
        if not (a.law and a.runner and a.root and a.plan and a.s0_plan and a.s0_stage2_report and a.out and a.max_hours is not None):
            ap.error('--stage ladder 는 --law · --runner · --root · --plan · --s0-plan · --s0-stage2-report · --max-hours · --out 이 필요하다')
        return stage_ladder(a, contract)
    if a.stage == 'predict':
        if not (a.ladders and a.runner and a.root and a.out and a.max_hours is not None):
            ap.error('--stage predict 는 --ladders · --runner · --root · --max-hours · --out 이 필요하다')
        return stage_predict(a, contract)
    if a.reverify:
        return stage_verdict(a, contract)
    if not (a.runs and a.out):
        ap.error('--stage verdict 는 --runs · --out 이 필요하다 (또는 --reverify <판정 폴더>)')
    return stage_verdict(a, contract)


if __name__ == '__main__':
    sys.exit(main())
