#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② R 런 사슬 — SBE 보정 사다리 (등록 R §3) · DBE holdout 예측 (§4) · 판정 (§5) · 다시 판정.

정본 = 등록 R `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` §3 (3-1 – 3-5) · §4 (4-1 · 4-2) · §5 · §6 · §7-1 ·
§10 (명령 꼴 (3)–(5) · 멈춤 목록 · 런 수) · §11 · 설계 v1 `docs/reviews/rint_carbon_additive_design_v1_20261020.md` §6 (수렴 증서 ⓐ ⓑ ⓒ) ·
§7 (세대 `p3ca-` · 영수증 · LEAN 표 · 판정 계산기 · 다시 판정).  꼴 = 앞선 같은 부류 사슬 `scripts/sdcp_anchor_v2_chain.py`
(사슬이 점을 고른다 · 값 봉인 · 멈춤 · 요약에서 다음 단계가 읽는다 · 사람이 옮겨 적지 않는다).

  # (3) 보정 사다리 — 법칙 끝마다 (SBE arm 0 · LEAN 2 · 값 봉인)
  python3 scripts/rint_r_chain.py --stage ladder --law P0 --target 1.63 --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh \\
      --root ~/sdcp --plan ~/sdcp/ca1_plan.json --max-hours H --out ~/sdcp/ca1_ladder_P0
  # (4) 예측 — 네 모서리 × {R_j,lo · R_j,0 · R_j,hi} (DBE arm 0 · R_j 는 사다리 요약에서 읽는다)
  python3 scripts/rint_r_chain.py --stage predict --ladders ~/sdcp/ca1_ladder_P0 ~/sdcp/ca1_ladder_P1 --kit kit_DBE_sdcp1um_vgcf100 \\
      --runner … --root ~/sdcp --max-hours H --out ~/sdcp/ca1_predict
  # (5) 판정 — 원 팔 JSON 전부에서 (값은 --show-results 로 한 번) · 다시 판정 (읽기 전용 · 바이트 대조)
  python3 scripts/rint_r_chain.py --stage verdict --runs <사다리 · 예측 · 감도 폴더 …> --out ~/sdcp/ca1_verdict [--show-results]
  python3 scripts/rint_r_chain.py --stage verdict --reverify ~/sdcp/ca1_verdict
  # 감도 (등록 R §5-6 · 필수): --variant FIBRE | UNREG | GRID (사다리 둘 + 예측) · SVORDER (예측만 · 주 사다리)

값 봉인: 사슬은 σ 를 읽어 점을 고르지만 화면 · 로그 · 공개 요약에는 σ 를 쓰지 않는다 (반복 수 · 잔차 · 판 전류 불균형 · 시간 · 상태만 ·
  σ 가 든 멈춤 사유는 그 수를 가린다).  σ 는 팔 JSON 에만 있고, 판정 결과 (`verdict_results.json`) 는 `--show-results` 로 연다.
⚠ 지금 코드 상태 (Z1 이 러너 · run_contract 를 같이 고치는 중) — 극한 런 (CJUNC_RJ=inf · 0) · face_alpha + 접합 · P1 · SIGMA_FIBRE_BULK 는
  지금 러너가 거부한다 (rc 2) → 사슬은 그 자리에서 RUNNER_RC 로 멈춘다 (fail-closed).  필요한 API 는 보고서에.
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

TOOL = 'rint_r_chain'
SCHEMA = 'rint-r-chain-v1'
REGISTRATION_DEFAULT = HERE.parent / 'docs' / 'reviews' / 'rint_carbon_additive_registration_R_draft_20261020.md'

# ═════════════════════════ 등록 R 의 숫자 — 한 곳 · 이름 (값 = 등록 정본 · 시험 X05 가 문서와 대조) ═════════════════════════
TARGET_SBE_MS = 1.63                 # §0 · §3 — SBE DC 1.63 mS/cm (보정 표적 · 판정선 · 결과 보고 옮기지 않는다)
EXP_DBE_MS = 4.68                    # §0 · §5 — DBE DC 4.68 mS/cm (holdout · 판정에 한 번)
CUR_GEN_DBE_MS = 1.8877              # §5-2 — 현 세대 SBE 보정 모형의 DBE (G0 의 기준 · 보고에 나란히)
CUR_GEN_SIGMA_STAR_DBE = 2.618       # §1 · §8 — 현 세대 DBE σ*_VGCF S/cm (보고만 · 맞추지 않는다)
EXP_RATIO = 2.86                     # §0 — 실험 비 DBE/SBE (보고만)
G0 = math.log(EXP_DBE_MS / CUR_GEN_DBE_MS)   # §5-2 G0 = ln(4.68/1.8877) = 0.908
GRADE_INFORMATIVE_MAX = G0 / 2.0     # §5-2 W ≤ G0/2 = 0.454 = 정보 있음
GRADE_WEAK_MAX = G0                  # §5-2 W ≤ G0 = 0.908 = 약함 · 넘으면 정보 없음
SENS_SHIFT_FRAC_G0 = 0.1             # §5-6 끝이 0.1 G0 (= 0.091) 넘게 움직이면 크기 보고
CONFIRM_TOL = 0.02                   # ±2 % — §3-1 EDGE · §3-2 확인 런 · §3-2b R_j,lo · R_j,hi
E_MIN = CONFIRM_TOL / math.log(math.sqrt(10.0))   # §3-2 식별성 e_min = 0.02 / ln √10 ≈ 0.017
TAU_MONO = 1e-3                      # §3-2 비단조 · §4-1 같은 P 일관 (ln σ)
NEIGHBOR_LOG10_MAX = 0.5             # §3-2 끼는 이웃 비 ≤ 10^0.5
LADDER_START_LOG10 = (4.0, 6.0, 8.0)  # §3-2 다음 점 {1e4, 1e6, 1e8} Ω
LADDER_EXT_LOG10 = 2.0               # §3-2 끼지 않으면 같은 쪽으로 ×100
MAX_LADDER_POINTS = 12               # §3-2 점 수 상한 (바닥 · 천장 · 사다리 · 확인 런 · origin 팔 제외)
MAX_CONFIRM = 2                      # §3-2 확인 런 최대 두 번
ORIGIN_SBE_MAX = 0.02                # §3-3 SBE arm 0 · 1 · 2 의 ln(max/min) ≤ 0.02
ORIGIN_DBE_FRAC_W = 0.1              # §4-2 DBE 모서리 arm 0 · 1 · 2 의 ln(max/min) ≤ 0.1 W
SIG_DIGITS = 3                       # §3-2 R_j,0 = 유효숫자 3 자리

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
L_PAR_UM, R_PORT_UM = 0.30, 0.30     # §2-1 지금 고정 (물리 단위)
VARIANTS = ('FIBRE', 'UNREG', 'GRID', 'SVORDER')   # §5-6 필수 감도
VARIANT_ENV = {'FIBRE': {'SIGMA_FIBRE_BULK': '1e3'}, 'UNREG': {'CJUNC_UNREG_LAW': 'fused'}, 'GRID': {'VOX': '0.125'},
               'SVORDER': {'SDCP_YIELD_VGCF': '1'}}
LIMIT_RJ = {'floor': 'inf', 'ceiling': '0'}   # §3-1 R_j → ∞ (바닥 · 간선 없음) · R_j → 0 (천장 · 정확 축약) — 러너 env 꼴
LIMIT_OF = {v: k for k, v in LIMIT_RJ.items()}
LEAN2_PLAN = {'electronic': True, 'ionic': False, 'thermal': False, 'pore': False, 'collector': False}
LEAN2_RECEIPTS = {'electronic_main': ('applied', 'absent_geometry'), 'electronic_wetted': ('disabled',),
                  'electronic_bare': ('disabled',), 'ionic': ('disabled',)}   # 설계 §7 LEAN 표 (LEAN 2)
PLAN_SCHEMA = 'rint-r-plan-v1'
PLAN_KEYS = ('schema', 'len_law', 'unreg_law', 's_min_um', 'tol_ff_um', 'step3_rtol', 'p2_extra')
PLAN_UNREG_MAIN = 'cut'              # 설계 §1-2 #12 — 주 cut · 감도 fused (UNREG)
#: 러너가 읽는 env (부모 셸에서 물려받으면 지운다 — 사슬이 런마다 정확히 정한다 · 지운 이름은 요약에)
ENV_SCRUB_RE = re.compile(r'^(SIGMA_|SDCP_|PTFE_|CJUNC|STEP3_)')
ENV_SCRUB_NAMES = frozenset({'VOX', 'BRIDGE_UM', 'ARMS', 'KITS', 'OUTDIR', 'LEAN', 'FIBRE_STAMP', 'MPM_PERIODIC_SIGMA', 'P2_EXTRA',
                             'EXPECT_BACKEND', 'EXPECT_PROTOCOL', 'P2_SCR', 'P2_SELF', 'P2_ENV_GUARD_ONLY'})
ENV_FORBIDDEN = ('SIGMA_VGCF_OVERRIDE',)   # §10 — 있으면 멈춤 (지워서 넘어가지 않는다)

# ═════════════════════════ 판정 이름 · 표지 · 문장 ═════════════════════════
CALIB_ORDER = ('CALIB_IMPOSSIBLE', 'CALIB_EDGE', 'CALIB_UNIDENTIFIED', 'CALIB_UNCONFIRMED', 'CALIB_NONMONOTONE',
               'CALIB_LADDER_EXHAUSTED', 'NOT_COMPUTED')   # §3-2c — 판정 전체 이름 (이 순서로 하나)
REGISTERED_OUTCOMES = frozenset(CALIB_ORDER)
SENTENCE_PASS = ('SBE 한 점으로 접합 저항을 보정하고 PTFE · SDCP 법칙을 독립 자료와 시나리오 끝으로 고정한 모형이 DBE 를 '
                 '등록 구간 안에서 예측했다.')    # §7-1 (PASS_INFORMATIVE · 표지 없음일 때만)
GRID_SENTENCE = 'not_computed'       # §9 '격자 의존이 현 세대보다 작았다' — 현 세대 vox 0.125 대조는 이 사슬 밖 (그 문장 금지 · GRID 표지와 별개)
SENTENCE_BY_VERDICT = {'CONSISTENT_WEAK': '넓은 시나리오 구간 안에 들었다', 'UNINFORMATIVE': None, 'FAIL': None}   # §5-5
QUALIFIERS = ('Q1_holdout_known_one_sided', 'Q2_Rj0_model_internal', 'Q3_scenario_ends_not_material', 'Q4_two_electrode_n1',
              'Q5_grid_flag', 'Q6_sensitivity_flags', 'Q7_S1P_pellet', 'Q8_SV_contact_zero', 'DIA_UNCHECKED',
              'Q10_junction_geometric_proximity')   # §7-1 필수 한정어 ①–⑩ (⑨ = DIA_UNCHECKED · 늘)

STOPS = {
    'OUTDIR_NOT_EMPTY': '출력 폴더가 이미 있고 비어 있지 않다 (러너 SKIP 캐시 · 옛 산출물)',
    'NOT_REGISTERED': '인자가 등록 R 과 다르다 (표적 · 법칙 · 킷 · 변이)',
    'ENV_SIGMA_VGCF_OVERRIDE': 'env 에 SIGMA_VGCF_OVERRIDE (복셀값 직접 · 다음 세대 판정 런 금지)',
    'REGISTRATION_UNREADABLE': '등록 문서 · §2-1 계획 해시 줄을 못 읽는다',
    'PLAN_HASH_UNREGISTERED': '등록 §2-1 계획 해시가 아직 없다 (⬜)',
    'PLAN_HASH_MISMATCH': '계획 해시 ≠ 등록 §2-1 개정값',
    'PLAN_INVALID': '계획 파일 꼴이 틀렸다',
    'KIT_MISSING': '킷 폴더 · 러너가 없다',
    'RUNNER_RC': '러너 rc ≠ 0',
    'REJECTED_MARKER': '러너 기각 기록 .rejected_*',
    'ARM_JSON_COUNT': '팔 JSON 개수 · 번호 · 이름 ≠ 요청',
    'ARM_UNREADABLE': '팔 JSON 을 못 읽는다',
    'ARM_CONTRACT': '러너 팔 계약 (check_arm) 실패',
    'GENERATION': 'physics_protocol_id 가 p3ca- 아님 (unknown:* 포함) · 저장 ≠ 다시 계산',
    'CA_EXT_RECORD': 'ca_ext_record_ok 실패',
    'MANIFEST_MISMATCH': '매니페스트 · 영수증 ≠ 요청 (σ · vox · 브리지 · PTFE · SDCP 구 · ca_ext 지문 · rtol)',
    'RECEIPT_LEAN': '솔브 영수증 ≠ LEAN 2 표 (설계 §7)',
    'PTFE_CELLS_OBSERVED': 'face_alpha 런의 ptfe_cells_observed > 0',
    'SID_GRID': 'sid 격자 지문이 같은 킷 · 같은 래스터 런 사이에서 다르다 (off 격자 대조)',
    'SAME_P_CONSISTENCY': '같은 P 일관 검사 위반 (SBE c no-op · DBE c 순서)',
    'TIME_LIMIT': '시간 상한',
    'DUPLICATE_RUN': '같은 킷 · 같은 계획 두 번',
    'INPUT_SHA_MISMATCH': '판정 입력 sha256 ≠ 런 산출',
    'INPUT_MISSING': '판정 입력이 모자란다',
    'INPUT_STAGE_STOPPED': '판정 입력 단계가 멈춘 채다',
    'INPUT_NOT_STAGE': '판정 입력 폴더에 단계 요약이 없다',
    'LADDER_NOT_CALIBRATED': '사다리가 보정되지 않았다 (예측 안 함)',
    'LADDER_SET': '사다리 묶음이 법칙 끝 둘이 아니다',
    'PREDICT_LADDER_MISMATCH': '예측이 쓴 사다리 ≠ 판정 입력 사다리',
    'REPLAY_MISMATCH': '원 팔 JSON 에서 다시 계산한 결정 ≠ 기록',
    'CODE_PIN_MISMATCH': '단계마다 코드 (사슬 · 러너) 가 다르다',
    **{k: k for k in CALIB_ORDER},
}


class Stop(Exception):
    """구조화 멈춤 — code (STOPS 이름) · cause (원인 칸 · σ 를 가린 문장) · run (그 런 이름)."""

    def __init__(self, code, cause, run=None):
        super().__init__(f'{code}: {cause}')
        self.code, self.cause, self.run = code, str(cause), run

    def record(self):
        return {'code': self.code, 'what': STOPS.get(self.code, self.code), 'cause': self.cause, 'run': self.run}


class RealContract:
    """정본 계약 위임 — 사슬은 이 계약을 다시 적지 않는다 (규율 ① · `run_contract` 머리말).  시험은 이 자리에 가짜 인지 계약을 넣는다."""

    def arm_problem(self, path, receipt):
        """러너가 팔을 OUTDIR 로 옮기기 전에 거는 검사와 같은 함수 (`sr01_stamp_compare.check_arm`) — 쓴 뒤 바뀐 팔을 다시 잡는다."""
        import sr01_stamp_compare as SC
        return SC.check_arm(path, 'segment', expect_backend='gpu', receipt=receipt)

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
    """§3-2 ln σ ↔ ln R_j 직선 보간 → target 을 지나는 R_j."""
    t = (math.log(target) - math.log(sa)) / (math.log(sb) - math.log(sa))
    return math.exp(math.log(Ra) + t * (math.log(Rb) - math.log(Ra)))


def elasticity(Ra, sa, Rb, sb):
    """§3-2 할선 탄성 e = |Δ ln σ / Δ ln R_j|."""
    return abs((math.log(sb) - math.log(sa)) / (math.log(Rb) - math.log(Ra)))


def sbe_origin_ok(vals):
    """§3-3 SBE arm 0 · 1 · 2 → (통과?, ln(max/min))."""
    sp = math.log(max(vals) / min(vals))
    return sp <= ORIGIN_SBE_MAX, sp


def dbe_origin_ok(vals, W0):
    """§4-2 DBE 모서리 arm 0 · 1 · 2 → (통과?, ln(max/min)) — 문턱 0.1 W (W = arm 0 값들로 낸 첫 폭)."""
    sp = math.log(max(vals) / min(vals))
    return sp <= ORIGIN_DBE_FRAC_W * W0, sp


def grade(lo, hi):
    """§5-2 – §5-5 — 구간 [lo, hi] (mS/cm) → 판정 이름 · W · p · d · d/G0 · 방향 · S.  4.68 ∈ I 는 양끝 포함."""
    x = EXP_DBE_MS
    W = math.log(hi / lo)
    inside = lo <= x <= hi
    if inside:
        name = ('PASS_INFORMATIVE' if W <= GRADE_INFORMATIVE_MAX else
                'CONSISTENT_WEAK' if W <= GRADE_WEAK_MAX else 'UNINFORMATIVE')
        d, direction = 0.0, 'inside'
    elif x < lo:
        name, d, direction = 'FAIL', math.log(lo / x), 'below'      # 4.68 이 구간 아래 = 모형이 높다
    else:
        name, d, direction = 'FAIL', math.log(x / hi), 'above'      # 4.68 이 구간 위 = 모형이 낮다
    mid = math.sqrt(lo * hi)
    return {'verdict': name, 'interval_mScm': [lo, hi], 'W': W, 'p': (math.log(x / lo) / W if W > 0 else None), 'd': d,
            'd_over_G0': d / G0, 'direction': direction, 'S': 1.0 - abs(math.log(x / mid)) / G0, 'sigma_mid_mScm': mid}


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


def variant_vox(variant):
    return VOX_GRID if variant == 'GRID' else VOX_MAIN


def variant_raster(kit, variant):
    """sid 격자 무리 키 — R_j · c · P 는 래스터를 안 바꾼다 · vox · SDCP 양보는 바꾼다."""
    return f'{kit}|vox={variant_vox(variant)}|yield={variant == "SVORDER"}'


def origins_for(vox):
    """러너의 팔 번호 ↔ origin (러너 SHIFTS 순서 그대로 — H = vox/2 소수 6 자리)."""
    h = float(f'{vox / 2:.6f}')
    return [(x, y, z) for x in (0.0, h) for y in (0.0, h) for z in (0.0, h)]


# ═════════════════════════ 등록 · 계획 ═════════════════════════
def registration_plan_hash(path):
    """등록 R §2-1 의 계획 해시 칸 → (sha256 hex, 문서 sha256).  ⬜ 이면 PLAN_HASH_UNREGISTERED (사람이 옮겨 적지 않는다)."""
    try:
        raw = Path(path).read_bytes()
        text = raw.decode('utf-8')
    except (OSError, UnicodeDecodeError) as e:
        raise Stop('REGISTRATION_UNREADABLE', f'{path} ({type(e).__name__})')
    rows = [ln for ln in text.splitlines() if ln.startswith('| 계획 해시 |')]
    if len(rows) != 1:
        raise Stop('REGISTRATION_UNREADABLE', f'§2-1 "| 계획 해시 |" 줄이 {len(rows)} 개 (1 이어야)')
    cells = [c.strip() for c in rows[0].strip().strip('|').split('|')]
    val = cells[-1].strip('` ')
    if not re.fullmatch(r'[0-9a-f]{64}', val):
        raise Stop('PLAN_HASH_UNREGISTERED', f'§2-1 계획 해시 칸 = {val!r} — 개정 커밋 (숫자 + 계획 해시 · 결과 0 건) 전에는 σ 런 없음')
    return val, hashlib.sha256(raw).hexdigest()


def _reject_constant(tok):
    raise ValueError(f'JSON 상수 {tok} 거부')


def load_plan(path):
    """계획 파일 (S0 단계 1 의 숫자 · 등록 §2-1 개정 커밋의 대상) → (dict, sha256).  사슬은 이 값을 러너 env 로 편다."""
    try:
        raw = Path(path).read_bytes()
        obj = json.loads(raw.decode('utf-8'), parse_constant=_reject_constant)
    except (OSError, UnicodeDecodeError, ValueError) as e:
        raise Stop('PLAN_INVALID', f'{path}: {type(e).__name__}: {e}')
    bad = []
    if not isinstance(obj, dict) or set(obj) != set(PLAN_KEYS):
        raise Stop('PLAN_INVALID', f'칸 {sorted(obj) if isinstance(obj, dict) else type(obj).__name__} ≠ {sorted(PLAN_KEYS)}')
    if obj['schema'] != PLAN_SCHEMA:
        bad.append(f'schema {obj["schema"]!r}')
    if not (isinstance(obj['len_law'], str) and re.fullmatch(r'[A-Za-z0-9_]+', obj['len_law'])):
        bad.append(f'len_law {obj["len_law"]!r}')
    if obj['unreg_law'] != PLAN_UNREG_MAIN:
        bad.append(f'unreg_law {obj["unreg_law"]!r} ≠ {PLAN_UNREG_MAIN!r} (주 = cut · fused = UNREG 감도)')
    for k, pos in (('s_min_um', False), ('tol_ff_um', False), ('step3_rtol', True)):
        v = obj[k]
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or v < 0 or (pos and v == 0):
            bad.append(f'{k} {v!r}')
    if not (isinstance(obj['p2_extra'], str) and re.fullmatch(r'[A-Za-z0-9._=/ -]*', obj['p2_extra'])):
        bad.append(f'p2_extra {obj["p2_extra"]!r}')
    if bad:
        raise Stop('PLAN_INVALID', ' · '.join(bad))
    return obj, hashlib.sha256(raw).hexdigest()


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


# ═════════════════════════ 팔 읽기 · 계약 (런 하나 = 폴더 하나) ═════════════════════════
def expected_request(req, plan):
    """러너에 요청한 다음 세대 선언 (영수증 `ca_ext_request` 와 매니페스트 protocol 이 같아야 한다)."""
    rj = req['rj']
    unreg = 'fused' if req['variant'] == 'UNREG' else plan['unreg_law']
    cj = {'R_j_ohm': (None if rj == 'inf' else rj_float(rj)), 'len_law': plan['len_law'], 'unreg_law': unreg,
          's_min_um': float(plan['s_min_um']), 'tol_ff_um': float(plan['tol_ff_um']), 'ptfe_jlaw': req['law']}
    out = {'cjunc': cj}
    if req['c'] != '':
        out['sdcp_mod'] = {'c': float(req['c'])}
    return out


def manifest_problems(man, rcpt, req, plan, idx, cert):
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
    cjp = ((ca.get('cjunc') or {}).get('protocol') or {}) if isinstance(ca.get('cjunc'), dict) else {}
    lim = LIMIT_OF.get(req['rj'])
    if lim:
        if not (cjp.get('rj_limit') == lim and cjp.get('allow_rj_limits') is True and cjp.get('quantitative') is False):
            bad.append(f'극한 런 ({lim}) 표지 — rj_limit {cjp.get("rj_limit")!r} · allow_rj_limits {cjp.get("allow_rj_limits")!r} · '
                       f'quantitative {cjp.get("quantitative")!r}')
        if lim == 'ceiling' and not _same(cjp.get('R_j_ohm'), 0.0):
            bad.append(f'천장 R_j_ohm {cjp.get("R_j_ohm")!r} ≠ 0')
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
    if not _same((cert or {}).get('rtol_used'), float(plan['step3_rtol'])):
        bad.append(f'증서 rtol_used {(cert or {}).get("rtol_used")!r} ≠ 계획 {plan["step3_rtol"]!r}')
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
    for k, v in (('arms', req['arms']), ('ptfe_stamp', 'face_alpha'), ('vox_um', vox), ('sdcp_yield_to_vgcf', yv)):
        if not _same(rcpt.get(k), v):
            bad.append(f'영수증 {k} {rcpt.get(k)!r} ≠ {v!r}')
    if 'sigma_vgcf_S_cm' in rcpt:
        bad.append(f'영수증이 σ_VGCF 를 직접 정했다 ({rcpt["sigma_vgcf_S_cm"]!r} · SIGMA_VGCF_OVERRIDE 세대)')
    ok, why = RC.receipt_match(rcpt, man, origin=man.get('origin_shift_um'))
    if not ok:
        bad.append(f'영수증 ↔ 매니페스트 {why}')
    return bad


def lean_problems(man):
    ca = man.get('ca_ext') if isinstance(man.get('ca_ext'), dict) else {}
    bad = []
    for sub in ('ptfe_face', 'cjunc'):
        rc_ = ((ca.get(sub) or {}).get('evidence') or {}).get('receipts') if isinstance(ca.get(sub), dict) else None
        if not isinstance(rc_, dict) or set(rc_) != set(LEAN2_RECEIPTS):
            bad.append(f'{sub} 영수증 키 {sorted(rc_) if isinstance(rc_, dict) else rc_!r}')
            continue
        for name, ok_st in LEAN2_RECEIPTS.items():
            st = (rc_.get(name) or {}).get('status') if isinstance(rc_.get(name), dict) else None
            if st not in ok_st:
                bad.append(f'{sub}.{name} = {st!r} (LEAN 2 표 {ok_st})')
    return bad


ARM_PUBLIC = ('file', 'index', 'sha256', 'protocol_id', 'cg_info', 'cg_resid', 'imbalance', 'cert_pass', 'sid_fp')


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
    """런 폴더 하나 → [팔 기록 …] (번호 순).  등록 R §10 멈춤 목록의 팔 쪽 전부 — 어긋나면 Stop (원인 칸 = σ 를 가린 문장)."""
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
    if sorted(byi) != list(range(req['arms'])):
        raise Stop('ARM_JSON_COUNT', f'{outdir.name}: 팔 번호 {sorted(byi)} ≠ 0..{req["arms"] - 1}', name)
    pref = f'p2_{req["kit"][len("kit_"):]}_'
    if any(not os.path.basename(p).startswith(pref) for p in byi.values()):
        raise Stop('ARM_JSON_COUNT', f'{outdir.name}: 팔 이름이 킷 {req["kit"]} 의 것이 아니다', name)
    if want_sha is not None and len(want_sha) != req['arms']:
        raise Stop('INPUT_SHA_MISMATCH', f'{outdir.name}: 기록된 sha256 {len(want_sha)} 개 ≠ 팔 {req["arms"]}', name)
    try:
        rcpt = json.loads((outdir / 'run_receipt.json').read_text(encoding='utf-8'))
    except (OSError, ValueError):
        rcpt = None
    out = []
    for i in range(req['arms']):
        p = byi[i]
        if want_sha is not None:
            why = sha_mismatch(p, want_sha[i])
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

        def stop(code, why):
            raise Stop(code, mask_sigma(f'{os.path.basename(p)}: {why}', sv), name)
        ok, why = RC.conv_ok(s3.get('cg_info'), s3.get('unconverged'), s3.get('cg_resid'))
        if not ok:
            stop('NOT_COMPUTED', f'수렴 계약 {why}')
        ok, why = RC.next_gen_cert_ok(s3)
        if not ok:
            stop('NOT_COMPUTED', f'수렴 증서 (ⓐ ⓑ ⓒ) {why}')
        pid = RC.physics_protocol_id(man)
        if not str(pid).startswith(RC.CA_EXT_PREFIX + '-'):
            stop('GENERATION', f'다시 계산한 id = {pid!r} (p3ca- 이어야)')
        if man.get('physics_protocol_id') != pid:
            stop('GENERATION', f'저장 id {man.get("physics_protocol_id")!r} ≠ 다시 계산 {pid!r}')
        ok, why = contract.ca_ext_record(man)
        if not ok:
            stop('CA_EXT_RECORD', why)
        why = contract.arm_problem(p, rcpt)
        if why:
            stop('ARM_CONTRACT', why)
        bad = manifest_problems(man, rcpt, req, plan, i, cert)
        if bad:
            stop('MANIFEST_MISMATCH', ' · '.join(bad[:6]) + (f' (+{len(bad) - 6})' if len(bad) > 6 else ''))
        bad = lean_problems(man)
        if bad:
            stop('RECEIPT_LEAN', ' · '.join(bad))
        if man.get('ptfe_cells_observed') != 0:
            stop('PTFE_CELLS_OBSERVED', f'ptfe_cells_observed = {man.get("ptfe_cells_observed")!r} (face_alpha = PTFE 셀 0)')
        ca = man['ca_ext']
        fp = (ca['cjunc'].get('evidence') or {}).get('fp') or {}
        sid = fp.get('sid')
        off = ((ca['ptfe_face'].get('evidence') or {}).get('fp') or {}).get('sid_off')
        if not isinstance(sid, str) or not sid or (off is not None and off != sid):
            stop('SID_GRID', f'sid 지문 {sid!r} · off 격자 지문 {off!r}')
        key = variant_raster(req['kit'], req['variant'])
        if sid_reg.setdefault(key, sid) != sid:
            stop('SID_GRID', f'{key} 의 sid 지문이 앞 런과 다르다')
        sig = s3.get('sigma_e_eff_S_cm')
        if isinstance(sig, bool) or not isinstance(sig, (int, float)) or not math.isfinite(sig) or sig <= 0:
            stop('ARM_UNREADABLE', 'σ_e 가 유한 양수가 아니다')
        solve = (ca['cjunc'].get('evidence') or {}).get('solve') or {}
        svd = solve.get('sv_dominant')
        out.append({'file': os.path.basename(p), 'index': i, 'sha256': hashlib.sha256(raw).hexdigest(), 'protocol_id': pid,
                    'cg_info': s3.get('cg_info'), 'cg_resid': s3.get('cg_resid'), 'imbalance': (cert or {}).get('imbalance'),
                    'cert_pass': [(cert or {}).get('pass_a'), (cert or {}).get('pass_b'), (cert or {}).get('pass_c')],
                    'sid_fp': sid, 'sigma': float(sig), 'dsigma_rel': (cert or {}).get('dsigma_rel'),
                    'sv_dominant': svd if isinstance(svd, bool) else None,
                    'dissipation_share': solve.get('dissipation_share'),
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
        d.update({'KITS': req['kit'], 'ARMS': str(req['arms']), 'OUTDIR': str(outdir), 'CJUNC_RJ': req['rj'],
                  'CJUNC_PTFE_JLAW': req['law']})
        if req['c'] != '':
            d['SDCP_MOD_C'] = req['c']
        return d

    def run(self, kit, role, law, c, rj, arms):
        """런 하나 → 팔 기록 목록.  같은 킷 · 같은 계획 두 번 · 출력 폴더 있음 · 시간 · rc · 팔 계약 = Stop."""
        self.n += 1
        name = f'{self.prefix}{self.n:02d}_{role}'
        req = {'name': name, 'role': role, 'kit': kit, 'law': law, 'c': c, 'rj': rj, 'arms': int(arms), 'variant': self.variant}
        key = (kit, variant_raster(kit, self.variant), self.variant, law, c, rj_float(rj), int(arms))
        if key in self.keys:
            raise Stop('DUPLICATE_RUN', f'{kit} · {law} · c {c} · R_j {disp_rj(rj)} · arms {arms} 를 두 번 요청', name)
        self.keys.add(key)
        outdir = self.out / (f'{name}_arm{arms}' if int(arms) != 8 else name)
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
        ok = '✓' if all(x is True for x in a0['cert_pass']) else '✗'
        print(f'  {name}: {role} · R_j {disp_rj(rj)} · {law} · c {c or "-"} · arms {arms} → rc 0 · {rec["seconds"]:.1f} s · '
              f'cg_info {a0["cg_info"]} · 잔차 {_e(a0["cg_resid"])} · 판 전류 불균형 {_e(a0["imbalance"])} · 증서 ⓐⓑⓒ {ok}')
        return arms_


class Replay:
    """판정 단계의 fetch — 기록된 런을 순서대로 대조해 원 팔 JSON 을 다시 읽는다 (sha256 대조 · 같은 계약)."""

    def __init__(self, stage_dir, summary, plan, contract, sid_reg, cert_reg=None):
        self.dir, self.plan, self.contract, self.sid_reg = Path(stage_dir), plan, contract, sid_reg
        self.recs = list(summary.get('runs') or [])
        self.variant = summary.get('variant')
        self.i = 0
        self.cert_reg = {} if cert_reg is None else cert_reg

    def run(self, kit, role, law, c, rj, arms):
        if self.i >= len(self.recs):
            raise Stop('REPLAY_MISMATCH', f'{self.dir.name}: 다시 계산이 {role} · R_j {disp_rj(rj)} 를 요구하는데 기록에 더 없다')
        r = self.recs[self.i]
        want, got = (kit, role, law, c, rj, int(arms)), (r.get('kit'), r.get('role'), r.get('law'), r.get('c'), r.get('rj'), r.get('arms'))
        if want != got or r.get('rc') != 0 or r.get('variant') != self.variant:
            raise Stop('REPLAY_MISMATCH', f'{self.dir.name}: 다시 계산 {want} ≠ 기록 {got} (rc {r.get("rc")!r})', r.get('name'))
        self.i += 1
        req = {k: r[k] for k in ('name', 'role', 'kit', 'law', 'c', 'rj', 'arms', 'variant')}
        arms_ = read_run(self.dir / r['outdir'], req, self.plan, self.contract, self.sid_reg,
                         want_sha=[a.get('sha256') for a in r.get('arms_read') or []])
        self.cert_reg[f'{self.dir.name}/{r["name"]}'] = [a['dsigma_rel'] for a in arms_]   # §8 수렴 증서 ⓒ 값 (판정 결과로만)
        return arms_

    def done(self):
        if self.i != len(self.recs):
            raise Stop('REPLAY_MISMATCH', f'{self.dir.name}: 기록에 다시 계산이 쓰지 않은 런 {len(self.recs) - self.i} 개')


# ═════════════════════════ 보정 사다리 (§3-1 – §3-3) ═════════════════════════
class Ladder:
    """fetch(role, rj, arms) → 팔 기록 목록 · arm 0 σ 로 점을 고른다.  공개 상태 (st) 에는 σ 가 없다 · 봉인 칸 (sealed) 은 판정만 연다."""

    def __init__(self, fetch, target_ms=None):
        self.fetch = fetch
        self.T = (TARGET_SBE_MS if target_ms is None else target_ms) * 1e-3
        self.st = {'order': [], 'n_runs': 0, 'n_ext': 0, 'n_bisect': 0, 'bracket': None, 'identifiable': None, 'confirms': [],
                   'flat_pairs': [], 'R_j0': None, 'R_j_lo': None, 'R_j_hi': None, 'origin': None}
        self.sealed = {'points': {}, 'e': None, 'delta': None, 'origin': None}
        self.pts = {}
        self.flags = []

    def _get(self, role, key):
        if self.st['n_runs'] >= MAX_LADDER_POINTS:
            raise Stop('CALIB_LADDER_EXHAUSTED', f'점 수 상한 {MAX_LADDER_POINTS} — 다음 {role} R_j {disp_rj(key)} 를 돌리지 않는다')
        recs = self.fetch(role, key, 1)
        s = recs[0]['sigma']
        self.st['n_runs'] += 1
        self.st['order'].append(key)
        self.pts[key] = (rj_float(key), s)
        self.sealed['points'][key] = s
        self._monotone()
        return s

    def _monotone(self):
        ps = sorted((R, k, s) for k, (R, s) in self.pts.items())
        for (_ra, ka, sa), (_rb, kb, sb) in zip(ps, ps[1:]):
            d = math.log(sb) - math.log(sa)
            if d > TAU_MONO:
                raise Stop('CALIB_NONMONOTONE', f'R_j {disp_rj(ka)} → {disp_rj(kb)} 에서 ln σ 가 τ_mono {TAU_MONO:g} 넘게 오른다 '
                                                '(구현 결함 의심)')
            if d > 0 and [ka, kb] not in self.st['flat_pairs']:
                self.st['flat_pairs'].append([ka, kb])           # τ 안 흔들림 = 평탄으로 기록 (멈추지 않는다)

    def run(self):
        T = self.T
        sF = self._get('floor', LIMIT_RJ['floor'])
        sC = self._get('ceiling', LIMIT_RJ['ceiling'])
        if not (sF <= T <= sC):
            raise Stop('CALIB_IMPOSSIBLE', '1.63 mS/cm 이 [바닥, 천장] 밖 (값은 봉인)')
        if abs(sF / T - 1.0) <= CONFIRM_TOL or abs(sC / T - 1.0) <= CONFIRM_TOL:
            raise Stop('CALIB_EDGE', f'1.63 이 바닥 또는 천장의 {CONFIRM_TOL:.0%} 안 — R_j,0 가 하나로 안 정해진다')
        for e in LADDER_START_LOG10:
            self._get('point', rj_key(10.0 ** e))
        while True:
            fin = sorted((R, k, s) for k, (R, s) in self.pts.items() if 0.0 < R < math.inf)
            br = None
            for a, b in zip(fin, fin[1:]):
                if min(a[2], b[2]) <= T <= max(a[2], b[2]):
                    br = (a, b)
                    break
            if br is None:
                if T > max(x[2] for x in fin):
                    e_new = math.log10(fin[0][0]) - LADDER_EXT_LOG10
                else:
                    e_new = math.log10(fin[-1][0]) + LADDER_EXT_LOG10
                self.st['n_ext'] += 1
                self._get('point', rj_key(10.0 ** e_new))
                continue
            (Ra, ka, sa), (Rb, kb, sb) = br
            if math.log10(Rb / Ra) > NEIGHBOR_LOG10_MAX + 1e-9:
                self.st['n_bisect'] += 1
                self._get('point', rj_key(10.0 ** ((math.log10(Ra) + math.log10(Rb)) / 2.0)))
                continue
            self.st['bracket'] = [ka, kb]
            e = elasticity(Ra, sa, Rb, sb)
            self.sealed['e'] = e
            if not (e >= E_MIN):
                self.st['identifiable'] = False
                raise Stop('CALIB_UNIDENTIFIED', f'끼는 이웃 {disp_rj(ka)} · {disp_rj(kb)} 의 할선 탄성 < e_min {E_MIN:.4f} (값은 봉인)')
            self.st['identifiable'] = True
            R0 = sig3(interp_lnln(Ra, sa, Rb, sb, T))
            k0 = rj_key(R0)
            reused = k0 in self.pts
            s0 = self.pts[k0][1] if reused else self._get('confirm', k0)
            ok = abs(s0 / T - 1.0) <= CONFIRM_TOL
            self.st['confirms'].append({'rj': k0, 'ok': ok, 'reused': reused})
            if ok:
                self.st['R_j0'] = k0
                self.st['R_j_lo'] = rj_key(interp_lnln(Ra, sa, Rb, sb, T * (1.0 + CONFIRM_TOL)))
                self.st['R_j_hi'] = rj_key(interp_lnln(Ra, sa, Rb, sb, T * (1.0 - CONFIRM_TOL)))
                self.sealed['delta'] = math.log(s0 / T)
                return
            if len(self.st['confirms']) >= MAX_CONFIRM:
                raise Stop('CALIB_UNCONFIRMED', f'확인 {MAX_CONFIRM} 번 다 ±{CONFIRM_TOL:.0%} 밖 (값은 봉인)')

    def origin(self):
        """§3-3 — R_j,0 에서 arm 1 · 2 (ARMS 3 한 런 · a0 는 재현 대조만) → ln(max/min) ≤ 0.02 · 넘으면 8 팔 평균 · 표지 (R_j,0 그대로)."""
        k0 = self.st['R_j0']
        s0 = self.pts[k0][1]
        r3 = self.fetch('origin3', k0, 3)
        ok, sp = sbe_origin_ok([s0, r3[1]['sigma'], r3[2]['sigma']])
        o = {'status': 'pass' if ok else 'sensitive', 'arms': 3, 'a0_replay_exact': r3[0]['sigma'] == s0}
        self.sealed['origin'] = {'spread': sp, 'a0_replay': r3[0]['sigma'], 'arms': [x['sigma'] for x in r3], 'mean8': None}
        if not ok:
            r8 = self.fetch('origin8', k0, 8)
            o['arms'] = 8
            self.sealed['origin']['mean8'] = sum(x['sigma'] for x in r8) / 8.0
            self.flags.append('CALIB_ORIGIN_SENSITIVE')
        self.st['origin'] = o


# ═════════════════════════ 예측 (§4-1 · §4-2) ═════════════════════════
RJ_ROLES = ('R_j_lo', 'R_j0', 'R_j_hi')


class Predict:
    """fetch(kit, role, law, c, rj, arms).  ladders = {법칙: {'R_j0', 'R_j_lo', 'R_j_hi', 'r0_sigma'}} (사다리에서 읽은 값 그대로)."""

    def __init__(self, fetch, ladders, variant):
        self.fetch, self.ladders, self.variant = fetch, ladders, variant
        self.main = variant is None
        self.checks = {'sbe_noop': [], 'same_p': []}
        self.origin = []
        self.vals = {}                       # (c, 법칙, 역할) → arm 0 팔 기록
        self.adj = {}                        # (c, 법칙) → Δ (8 팔 평균으로 옮긴 로그 차)
        self.sealed = {'W0': None, 'origin': {}}

    def run(self):
        if self.main:
            for law in LAWS:
                r = self.fetch(SBE_KIT, 'sbe_noop', law, '1', self.ladders[law]['R_j0'], 1)[0]
                ok = r['sigma'] == self.ladders[law]['r0_sigma'] and r['n_sdcp_near'] == 0
                self.checks['sbe_noop'].append({'law': law, 'ok': ok})
                if not ok:
                    raise Stop('SAME_P_CONSISTENCY', f'SBE c 1 ↔ c 0 (사다리 R_j,0 확인 팔) 비트 다름 또는 SDCP 근접 '
                                                     f'{r["n_sdcp_near"]!r} ≠ 0 ({law}) — S3 이 SBE 에서 no-op 이 아니다')
        roles = RJ_ROLES if self.main else ('R_j0',)
        for law in LAWS:
            for rr in roles:
                for c in CS:
                    self.vals[(c, law, rr)] = self.fetch(DBE_KIT, 'corner', law, c, self.ladders[law][rr], 1)[0]
                d = math.log(self.vals[('1', law, rr)]['sigma']) - math.log(self.vals[('0', law, rr)]['sigma'])
                ok = d >= -TAU_MONO
                self.checks['same_p'].append({'law': law, 'rj_role': rr, 'ok': ok})
                if not ok:
                    raise Stop('SAME_P_CONSISTENCY', f'σ_DBE(c1, {law}) < σ_DBE(c0, {law}) − τ_mono at {rr} — 같은 그래프 · 같은 R_j 에서 '
                                                     f'Rayleigh 순서 위반 (구현 결함)')
        if not self.main:
            return
        allv = [v['sigma'] for v in self.vals.values()]
        W0 = math.log(max(allv) / min(allv))
        self.sealed['W0'] = W0
        for law in LAWS:
            for c in CS:
                a0 = self.vals[(c, law, 'R_j0')]['sigma']
                r3 = self.fetch(DBE_KIT, 'origin3', law, c, self.ladders[law]['R_j0'], 3)
                ok, sp = dbe_origin_ok([a0, r3[1]['sigma'], r3[2]['sigma']], W0)
                ent = {'c': c, 'law': law, 'status': 'pass' if ok else 'adjusted', 'a0_replay_exact': r3[0]['sigma'] == a0}
                so = {'spread': sp, 'arms': [x['sigma'] for x in r3]}
                if not ok:
                    r8 = self.fetch(DBE_KIT, 'origin8', law, c, self.ladders[law]['R_j0'], 8)
                    mean8 = sum(x['sigma'] for x in r8) / 8.0
                    self.adj[(c, law)] = math.log(mean8 / a0)
                    so['mean8'] = mean8
                self.origin.append(ent)
                self.sealed['origin'][f'c{c}_{law}'] = so

    def values(self):
        """모서리 값 (S/cm) — origin 규칙이 옮긴 모서리는 R_j,0 = 8 팔 평균 · lo · hi = 같은 로그 차 (§4-2)."""
        out = {}
        for (c, law, rr), r in self.vals.items():
            d = self.adj.get((c, law))
            out[(c, law, rr)] = r['sigma'] if d is None else r['sigma'] * math.exp(d)
        return out


# ═════════════════════════ 단계 공통 ═════════════════════════
def summary_base(stage, a):
    return {'tool': TOOL, 'schema': SCHEMA, 'stage': stage, 'status': None, 'stop': None, 'flags': [],
            'code': {'chain': git_identity(HERE / 'rint_r_chain.py'),
                     'runner': (git_identity(a.runner) if getattr(a, 'runner', None) else None),
                     'runner_path': (str(Path(a.runner).resolve()) if getattr(a, 'runner', None) else None)},
            'constants': {'target_sbe_mScm': TARGET_SBE_MS, 'confirm_tol': CONFIRM_TOL, 'e_min': E_MIN, 'tau_mono': TAU_MONO,
                          'neighbor_log10_max': NEIGHBOR_LOG10_MAX, 'max_ladder_points': MAX_LADDER_POINTS,
                          'origin_sbe_max': ORIGIN_SBE_MAX, 'origin_dbe_frac_w': ORIGIN_DBE_FRAC_W}}


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


# ═════════════════════════ (3) 사다리 단계 ═════════════════════════
def stage_ladder(a, contract):
    out = Path(a.out)
    try:
        outdir_empty_or_stop(out)
    except Stop as e:
        print_stop(e)
        return 3
    s = summary_base('ladder', a)
    s.update({'law': a.law, 'variant': a.variant, 'kit': a.kit or SBE_KIT, 'runs': [], 'ladder': None, 'env_scrubbed': []})
    ran = False
    try:
        if not _same(a.target, TARGET_SBE_MS) or a.law not in LAWS or (a.kit or SBE_KIT) != SBE_KIT or a.variant == 'SVORDER':
            raise Stop('NOT_REGISTERED', f'--target {a.target} (등록 {TARGET_SBE_MS}) · --law {a.law} · --kit {a.kit} '
                                         f'(등록 {SBE_KIT}) · --variant {a.variant} (SVORDER 는 사다리 없음 — 주 사다리 그대로)')
        env_forbidden_or_stop()
        plan, plan_sha = load_plan(a.plan)
        s['plan'] = {'path': str(Path(a.plan).resolve()), 'sha256': plan_sha, 'content': plan}
        s['registration'] = check_plan_registered(plan_sha, a.registration)
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
        lad = Ladder(lambda role, rj, arms: rn.run(SBE_KIT, role, a.law, LADDER_C, rj, arms))
        try:
            try:
                lad.run()
                if a.variant is None:          # §3-3 origin = 주 사다리만 (§10 런 수 — 감도 변이는 사다리 ≤ 12 × 2 + DBE 4)
                    lad.origin()
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
        print(f'보정 = CALIBRATED · R_j,0 = {disp_rj(L["R_j0"])} · R_j,lo {disp_rj(L["R_j_lo"])} · R_j,hi {disp_rj(L["R_j_hi"])} · '
              f'런 {L["n_runs"]} · ×100 {L["n_ext"]} · 반씩 {L["n_bisect"]} · 확인 {len(L["confirms"])} · '
              f'origin {(L["origin"] or {}).get("status", "— (감도 변이 · §10)")}'
              + (f' · 표지 {s["flags"]}' if s['flags'] else ''))
    else:
        print(f'보정 = {s["status"]}')
    print(f'요약 → {out / "ladder_summary.json"}')
    return 0 if s['status'] == 'CALIBRATED' else 3


# ═════════════════════════ (4) 예측 단계 ═════════════════════════
def load_ladders(dirs, variant, reg_path, contract, sid_reg):
    """사다리 요약 둘 → {법칙: {...}} · 계획 · 코드.  R_j 는 요약에서 그대로 (사람이 옮겨 적지 않는다) · R_j,0 확인 팔을 다시 읽는다."""
    want_var = None if variant == 'SVORDER' else variant
    out, plan, plan_sha, code = {}, None, None, None
    seen = set()
    for d in dirs:
        rd = Path(d).resolve()
        if rd in seen:
            raise Stop('DUPLICATE_RUN', f'같은 사다리 폴더 두 번 {rd}')
        seen.add(rd)
        s, sha = read_summary(rd, 'ladder_summary.json')
        if s is None or s.get('stage') != 'ladder':
            raise Stop('LADDER_SET', f'{rd}: ladder_summary.json 이 없다')
        if s.get('status') != 'CALIBRATED':
            raise Stop('LADDER_NOT_CALIBRATED', f'{rd.name}: 사다리 상태 {s.get("status")} — 예측하지 않는다 (판정 = 그 이름)')
        if s.get('variant') != want_var:
            raise Stop('LADDER_SET', f'{rd.name}: 사다리 변이 {s.get("variant")!r} ≠ {want_var!r}')
        law = s.get('law')
        if law in out:
            raise Stop('DUPLICATE_RUN', f'{law} 사다리가 둘 ({out[law]["dir"]} · {rd}) — 같은 킷 · 같은 계획 두 번')
        if plan_sha is not None and s['plan']['sha256'] != plan_sha:
            raise Stop('PLAN_HASH_MISMATCH', '두 사다리의 계획이 다르다')
        if code is not None and not same_code(s.get('code', {}).get('chain'), code.get('chain')):
            raise Stop('CODE_PIN_MISMATCH', '두 사다리의 사슬 코드가 다르다')
        plan, plan_sha, code = s['plan']['content'], s['plan']['sha256'], s.get('code') or {}
        L = s['ladder']
        r0run = [r for r in s['runs'] if r.get('rj') == L['R_j0'] and r.get('arms') == 1 and r.get('role') in ('confirm', 'point')]
        if not r0run:
            raise Stop('LADDER_SET', f'{rd.name}: R_j,0 확인 팔 기록이 없다')
        r = r0run[-1]
        req = {k: r[k] for k in ('name', 'role', 'kit', 'law', 'c', 'rj', 'arms', 'variant')}
        arm = read_run(rd / r['outdir'], req, plan, contract, sid_reg, want_sha=[x['sha256'] for x in r['arms_read']])[0]
        out[law] = {'dir': str(rd), 'summary_sha256': sha, 'variant': s.get('variant'), 'R_j0': L['R_j0'], 'R_j_lo': L['R_j_lo'],
                    'R_j_hi': L['R_j_hi'], 'r0_sigma': arm['sigma']}
    if sorted(out) != sorted(LAWS):
        raise Stop('LADDER_SET', f'사다리 법칙 {sorted(out)} ≠ {list(LAWS)}')
    check_plan_registered(plan_sha, reg_path)
    return out, plan, plan_sha, code


def stage_predict(a, contract):
    out = Path(a.out)
    try:
        outdir_empty_or_stop(out)
    except Stop as e:
        print_stop(e)
        return 3
    s = summary_base('predict', a)
    s.update({'variant': a.variant, 'kit': a.kit or DBE_KIT, 'runs': [], 'ladders': {}, 'checks': None, 'origin': None,
              'env_scrubbed': []})
    ran = False
    try:
        if (a.kit or DBE_KIT) != DBE_KIT:
            raise Stop('NOT_REGISTERED', f'--kit {a.kit} (등록 {DBE_KIT})')
        env_forbidden_or_stop()
        sid_reg = {}
        lads, plan, plan_sha, code = load_ladders(a.ladders, a.variant, a.registration, contract, sid_reg)
        if not same_code(code.get('chain'), s['code']['chain']):
            raise Stop('CODE_PIN_MISMATCH', '사다리 사슬 코드 ≠ 지금 사슬 코드 (같은 핀 작업 트리에서 돌릴 것)')
        s['ladders'] = {k: {kk: v[kk] for kk in ('dir', 'summary_sha256', 'variant', 'R_j0', 'R_j_lo', 'R_j_hi')} for k, v in lads.items()}
        s['plan'] = {'sha256': plan_sha, 'content': plan}
        s['registration'] = check_plan_registered(plan_sha, a.registration)
        for p in (Path(a.root) / SBE_KIT, Path(a.root) / DBE_KIT, Path(a.runner)):
            if not p.exists():
                raise Stop('KIT_MISSING', f'{p}')
        rn = Runner(a.runner, a.root, out, plan, a.variant, time.time() + a.max_hours * 3600.0, contract, dry=a.dry_run, prefix='P')
        rn.sid_reg = sid_reg
        s['env_scrubbed'] = rn.scrubbed
        if a.dry_run:
            print('dry-run — 예측 런의 env (러너를 부르지 않는다 · origin 런은 arm 0 값으로 정해진다)')
            if a.variant is None:
                for law in LAWS:
                    rn.run(SBE_KIT, 'sbe_noop', law, '1', lads[law]['R_j0'], 1)
            for law in LAWS:
                for rr in (RJ_ROLES if a.variant is None else ('R_j0',)):
                    for c in CS:
                        rn.run(DBE_KIT, 'corner', law, c, lads[law][rr], 1)
            return 0
        out.mkdir(parents=True, exist_ok=True)
        ran = True
        print(f'예측{" · 변이 " + a.variant if a.variant else ""} — DBE arm 0 · 네 모서리 × '
              f'{"{R_j,lo · R_j,0 · R_j,hi}" if a.variant is None else "R_j,0"} (값은 봉인)')
        pr = Predict(rn.run, lads, a.variant)
        try:
            try:
                pr.run()
                s['status'] = 'PREDICTED'
            finally:
                s['checks'], s['origin'], s['runs'] = pr.checks, (pr.origin if a.variant is None else None), rn.records
        except Stop:
            s['status'] = 'STOPPED'
            raise
    except Stop as e:
        s['stop'] = e.record()
        s['status'] = 'STOPPED'
        print_stop(e)
    if a.dry_run and not ran:
        return 3
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / 'predict_summary.json', s)
    if s['status'] == 'PREDICTED':
        n_adj = sum(1 for o in (s['origin'] or []) if o['status'] == 'adjusted')
        print(f'예측 = PREDICTED · 런 {len(s["runs"])} · 같은 P 일관 통과 · origin 규칙이 옮긴 모서리 {n_adj}')
    print(f'요약 → {out / "predict_summary.json"}')
    return 0 if s['status'] == 'PREDICTED' else 3


# ═════════════════════════ (5) 판정 단계 ═════════════════════════
def _replay_ladder(d, s, contract, sid_reg, cert_reg):
    rp = Replay(d, s, s['plan']['content'], contract, sid_reg, cert_reg)
    lad = Ladder(lambda role, rj, arms: rp.run(SBE_KIT, role, s['law'], LADDER_C, rj, arms))
    status = 'CALIBRATED'
    try:
        lad.run()
        if s.get('variant') is None:
            lad.origin()
    except Stop as e:
        if e.code not in REGISTERED_OUTCOMES:
            raise
        status = e.code
    rp.done()
    if status != s.get('status') or lad.st != s.get('ladder') or lad.flags != s.get('flags'):
        diff = [k for k in set(lad.st) | set(s.get('ladder') or {}) if lad.st.get(k) != (s.get('ladder') or {}).get(k)]
        raise Stop('REPLAY_MISMATCH', f'{Path(d).name}: 원 팔에서 다시 계산한 사다리 ≠ 요약 (상태 {status} ↔ {s.get("status")} · 칸 {sorted(diff)})')
    return {'status': status, 'st': lad.st, 'sealed': lad.sealed, 'flags': lad.flags, 'pts': lad.pts}


def _replay_predict(d, s, lads, contract, sid_reg, cert_reg):
    rp = Replay(d, s, s['plan']['content'], contract, sid_reg, cert_reg)
    pr = Predict(rp.run, lads, s.get('variant'))
    pr.run()
    rp.done()
    if pr.checks != s.get('checks') or (pr.origin if s.get('variant') is None else None) != s.get('origin'):
        raise Stop('REPLAY_MISMATCH', f'{Path(d).name}: 원 팔에서 다시 계산한 예측 검사 · origin 결정 ≠ 요약')
    return pr


def verdict_compute(dirs, reg_path, contract):
    """판정 계산기 (§5 · 설계 §7) — 원 팔 JSON 전부에서.  → (공개 dict, 결과 dict | None).  입력 계약 실패 = Stop."""
    pub = {'tool': TOOL, 'schema': SCHEMA, 'stage': 'verdict', 'verdict': None, 'stop': None, 'flags': [],
           'qualifiers': list(QUALIFIERS), 'sentence_allowed': False, 'sentence': None, 'calib': {}, 'variants': {},
           'inputs': [], 'arms': [], 'registration': None, 'grid_sentence': GRID_SENTENCE}
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
            raise Stop('INPUT_NOT_STAGE', f'{rd}: 이 사슬의 요약이 아니다')
        stages.append((rd, s, h))
    stages.sort(key=lambda x: (x[1].get('variant') or '', x[1].get('stage'), x[1].get('law') or '', str(x[0])))
    plan_hash, reg_sha = registration_plan_hash(reg_path)
    pub['registration'] = {'path': str(Path(reg_path).resolve()), 'sha256': reg_sha, 'plan_hash': plan_hash}
    code0 = None
    for rd, s, h in stages:
        pub['inputs'].append({'dir': str(rd), 'stage': s.get('stage'), 'law': s.get('law'), 'variant': s.get('variant'),
                              'status': s.get('status'), 'summary_sha256': h})
        if s.get('status') == 'STOPPED':
            raise Stop('INPUT_STAGE_STOPPED', f'{rd.name}: {(s.get("stop") or {}).get("code")} — 멈춘 단계는 판정 입력이 아니다')
        if (s.get('plan') or {}).get('sha256') != plan_hash:
            raise Stop('PLAN_HASH_MISMATCH', f'{rd.name}: 계획 sha256 ≠ 등록 §2-1 개정값')
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
    lad_in = {}
    pred_in = {}
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
            out[law] = (rd, s, h, _replay_ladder(rd, s, contract, sid_reg, cert_reg))
        return out
    main_l = ladders_of(None)
    if main_l is None:
        raise Stop('INPUT_MISSING', '주 사다리 P0 · P1 둘이 다 있어야 한다')
    flags = []
    for law, (rd, s, h, L) in main_l.items():
        pub['calib'][law] = L['status']
        flags += L['flags']
        res['ladders'][law] = {'status': L['status'], 'R_j0': L['st']['R_j0'], 'R_j_lo': L['st']['R_j_lo'], 'R_j_hi': L['st']['R_j_hi'],
                               'floor_mScm': L['sealed']['points'].get('inf', math.nan) * 1e3,
                               'ceiling_mScm': L['sealed']['points'].get('0', math.nan) * 1e3,
                               'e': L['sealed']['e'], 'delta': L['sealed']['delta'],
                               'points_mScm': {k: v * 1e3 for k, v in L['sealed']['points'].items()},
                               'origin': L['sealed']['origin']}
    bad = [pub['calib'][law] for law in LAWS if pub['calib'][law] != 'CALIBRATED']
    if bad:
        pub['verdict'] = min(bad, key=CALIB_ORDER.index)
        pub['flags'] = sorted(set(flags))
        res['certificates_dsigma_rel'] = dict(cert_reg)
        return pub, _clean(res)

    def predict_of(variant, lads):
        if variant not in pred_in:
            return None
        rd, s, h = pred_in[variant]
        for law in LAWS:
            ref = (s.get('ladders') or {}).get(law) or {}
            if ref.get('summary_sha256') != lads[law][2]:
                raise Stop('PREDICT_LADDER_MISMATCH', f'{rd.name}: {law} 사다리 요약 sha256 ≠ 판정 입력')
        lin = {law: {'R_j0': lads[law][3]['st']['R_j0'], 'R_j_lo': lads[law][3]['st']['R_j_lo'], 'R_j_hi': lads[law][3]['st']['R_j_hi'],
                     'r0_sigma': lads[law][3]['pts'][lads[law][3]['st']['R_j0']][1]} for law in LAWS}
        return _replay_predict(rd, s, lin, contract, sid_reg, cert_reg)
    pr = predict_of(None, main_l)
    if pr is None:
        raise Stop('INPUT_MISSING', '주 예측 폴더가 없다 (사다리 둘 다 보정됨)')
    vals = pr.values()
    ms = {k: v * 1e3 for k, v in vals.items()}
    g = grade(min(ms.values()), max(ms.values()))
    pub['verdict'] = g['verdict']
    res.update(g)
    res['corners_mScm'] = {f'c{c}_{law}': {rr: ms[(c, law, rr)] for rr in RJ_ROLES} for c in CS for law in LAWS}
    res['corners_arm0_mScm'] = {f'c{c}_{law}': {rr: pr.vals[(c, law, rr)]['sigma'] * 1e3 for rr in RJ_ROLES} for c in CS for law in LAWS}
    res['origin'] = {'W0': pr.sealed['W0'], 'corners': pr.sealed['origin'], 'adjusted_log': {f'c{c}_{law}': d for (c, law), d in pr.adj.items()}}
    band = math.log((1.0 + CONFIRM_TOL) / (1.0 - CONFIRM_TOL))
    res['s'] = {f'c{c}_{law}': (math.log(vals[(c, law, 'R_j_lo')]) - math.log(vals[(c, law, 'R_j_hi')])) / band for c in CS for law in LAWS}
    res['P_effect_log'] = {f'c{c}': math.log(vals[(c, 'P1', 'R_j0')] / vals[(c, 'P0', 'R_j0')]) for c in CS}
    res['c_effect_log'] = {law: math.log(vals[('1', law, 'R_j0')] / vals[('0', law, 'R_j0')]) for law in LAWS}
    res['ratio_dbe_sbe'] = {f'c{c}_{law}': ms[(c, law, 'R_j0')] / TARGET_SBE_MS for c in CS for law in LAWS}
    res['dissipation_share'] = {f'c{c}_{law}_{rr}': pr.vals[(c, law, rr)]['dissipation_share'] for c in CS for law in LAWS for rr in RJ_ROLES}
    sv = [pr.vals[k]['sv_dominant'] for k in sorted(pr.vals)]
    if any(x is not False for x in sv):
        flags.append('SV_DOMINANT')                           # §5-6 — True 이거나 원장을 못 읽음 (NOT_COMPUTED) = 걸린 것과 같게
    main4 = [pr.vals[(c, law, 'R_j0')]['sigma'] * 1e3 for c in CS for law in LAWS]
    g4 = grade(min(main4), max(main4))
    res['main_R0_only'] = g4
    for V in VARIANTS:
        vl = main_l if V == 'SVORDER' else ladders_of(V)
        if vl is None or V not in pred_in and all(vl[law][3]['status'] == 'CALIBRATED' for law in LAWS):
            pub['variants'][V] = {'checked': False, 'verdict': None, 'grade_changed': None}
            flags.append(f'{V}_UNCHECKED')
            continue
        vbad = [vl[law][3]['status'] for law in LAWS if vl[law][3]['status'] != 'CALIBRATED']
        if vbad:
            vname, vg = min(vbad, key=CALIB_ORDER.index), None
        else:
            vp = predict_of(V, vl)
            v4 = [vp.vals[(c, law, 'R_j0')]['sigma'] * 1e3 for c in CS for law in LAWS]
            vg = grade(min(v4), max(v4))
            vname = vg['verdict']
        changed = vname != g4['verdict']
        pub['variants'][V] = {'checked': True, 'verdict': vname, 'grade_changed': changed}
        if changed:
            flags.append(f'{V}_SENSITIVE')
        ent = {'verdict': vname, 'grade': vg}
        if vg is not None:
            sh = [abs(math.log(vg['interval_mScm'][i] / g4['interval_mScm'][i])) for i in (0, 1)]
            ent.update(end_shift_log=sh, end_shift_exceeds_0p1G0=max(sh) > SENS_SHIFT_FRAC_G0 * G0)
        res['variants'][V] = ent
    pub['flags'] = sorted(set(flags))
    blocking = [f for f in pub['flags'] if f.endswith('_SENSITIVE') or f.endswith('_UNCHECKED') or f in ('SV_DOMINANT',
                                                                                                      'CALIB_ORIGIN_SENSITIVE')]
    pub['sentence_allowed'] = pub['verdict'] == 'PASS_INFORMATIVE' and not blocking
    pub['sentence'] = SENTENCE_PASS if pub['sentence_allowed'] else SENTENCE_BY_VERDICT.get(pub['verdict'])
    res['certificates_dsigma_rel'] = dict(cert_reg)          # §8 수렴 증서 ⓒ (런마다 · 판정 결과로만)
    return pub, _clean(res)


def _clean(obj):
    """결과 JSON — NaN · inf 를 null 로 (allow_nan=False 직렬화 · 다시 판정 바이트 대조)."""
    if isinstance(obj, dict):
        return {str(k): _clean(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_clean(v) for v in obj]
    if isinstance(obj, float) and not math.isfinite(obj):
        return None
    return obj


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
        pub = {'tool': TOOL, 'schema': SCHEMA, 'stage': 'verdict', 'verdict': 'NOT_COMPUTED', 'stop': e.record(), 'flags': [],
               'qualifiers': list(QUALIFIERS), 'sentence_allowed': False, 'sentence': None, 'calib': {}, 'variants': {},
               'grid_sentence': GRID_SENTENCE,
               'inputs': [str(Path(d).resolve()) for d in a.runs], 'arms': [], 'registration': str(Path(a.registration).resolve())}
        res, rc_ = None, 3
    pub['input_dirs'] = [str(Path(d).resolve()) for d in a.runs]
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / 'verdict.json', pub)
    if res is not None:
        write_json(out / 'verdict_results.json', res)
        try:
            os.chmod(out / 'verdict_results.json', 0o600)
        except OSError:
            pass
    print(f'판정 = {pub["verdict"]} · 표지 {pub["flags"] or "없음"} · §7-1 문장 {"허용" if pub["sentence_allowed"] else "금지"}'
          + (f' · 사다리 {pub["calib"]}' if pub.get('calib') else ''))
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
        pub = {'tool': TOOL, 'schema': SCHEMA, 'stage': 'verdict', 'verdict': 'NOT_COMPUTED', 'stop': e.record(), 'flags': [],
               'qualifiers': list(QUALIFIERS), 'sentence_allowed': False, 'sentence': None, 'calib': {}, 'variants': {},
               'grid_sentence': GRID_SENTENCE,
               'inputs': [str(Path(d).resolve()) for d in dirs], 'arms': [], 'registration': str(Path(reg).resolve()) if reg else None}
        res = None
    pub['input_dirs'] = dirs
    new_pub, new_res = canon_bytes(pub), (canon_bytes(res) if res is not None else None)
    if new_pub == old_pub and new_res == old_res:
        print(f'REVERIFY_SAME — 판정 JSON · 결과 JSON 바이트 같음 ({len(dirs)} 입력 · 판정 {pub["verdict"]})')
        return 0
    keys = sorted(k for k in set(pub) | set(pub0) if pub.get(k) != pub0.get(k))
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
    ap.add_argument('--variant', choices=VARIANTS, default=None, help='감도 (등록 R §5-6 · 필수)')
    ap.add_argument('--kit', default=None, help=f'ladder = {SBE_KIT} · predict = {DBE_KIT} (등록 · 다르면 멈춤)')
    ap.add_argument('--runner')
    ap.add_argument('--root', help='킷 폴더가 있는 곳 = 러너 작업 폴더')
    ap.add_argument('--plan', help='ladder — 계획 파일 (등록 §2-1 개정 커밋의 대상 · sha256 = 그 칸)')
    ap.add_argument('--registration', default=str(REGISTRATION_DEFAULT), help='등록 R 문서 (§2-1 계획 해시를 읽는다)')
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
    if a.stage == 'ladder':
        if not (a.law and a.runner and a.root and a.plan and a.out and a.max_hours is not None):
            ap.error('--stage ladder 는 --law · --runner · --root · --plan · --max-hours · --out 이 필요하다')
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
