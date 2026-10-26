#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② S0 — 표현 원장 (raster-only · 솔브 없음 · CPU) — 설계 v1 §2 · 등록 R §2-1 · §11 ④ (2026-10-20).

정본 = docs/reviews/rint_carbon_additive_design_v1_20261020.md §2 (① 양 · ② 입출력 · ③ 계약 · ④ 시험 S0-1 … S0-7) ·
등록 R docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md §2-1 (문턱 식 = 지금 고정 · 숫자 = 단계 1 (SBE)) ·
1저자 10-20 *"다 권고대로 해"* (설계 §10 N1–N18).  시험 = scripts/test_ca_s0_census.py.

무엇 (σ · 전류 · 소산 칸 없음 — 문턱을 σ 보기 전에 정하는 근거):
  · 상별 표현 부피 비 (셀 수 × vox³ / mpm_metrics.additives.<상>.vol_um3) — 생산 격자 · off 격자
  · PTFE 가 덮은 탄소 · SDCP 셀 (centerline 생산 격자의 sid 7 셀이 PTFE 없이는 무엇이었나) · PTFE 경로 셀의 off sid 분포
  · PTFE 가 끊은 VGCF 경로 (경로 셀 집합에서 sid 7 셀을 빼면 6-면 성분이 늘어난 경로 수 · 늘어난 조각 수)
  · SDCP 가 덮은 VGCF · AM 셀 · SDCP 가 덮은 섬유 구간 (경로 셀 열의 연속 구간) · SDCP 경유 섬유 연결 수 (둘 이상 fid 에 닿는 SDCP 덩어리)
  · 교차 셀 멤버십 (≥ 2 · ≥ 3) · 캡슐 부피 비 (F11) · 문턱 입력 u (VGCF 경로 점 간격 중앙값 / 2)
  · 접합 census — **판정 · 보고 판** (`junction_census` · 2 일 차) = B3 `carbon_junction.cjunc_registry` 를 **그대로** 부른다
    (사본 없음 · 설계 §2 ① · §4-1 끝): off 격자 (= face_alpha 의 sid 격자) · 계획 문턱 · s_min 안 씀 (거르지 않음) →
    원장 census · 긴 접촉 수 · L_c 분포 (요약 + 후보별 npz) · 자기 (같은 가닥) 후보마다 경로 호 길이 s (s_min 근거 · 목록) ·
    길이 법칙 배율 합 · PTFE 덮임 · SDCP 근접 수 (`s0_junctions_<킷>.npz` = 후보별 배열)
  · 접합 기하 census — **B0 미리보기** (표지 `b0_preview` · 판정 · 보고에 쓰지 않는다):
    VV instance (J2a · J2c) 수 · 표면 틈 · 접촉 길이 (두 판) · 각 · 긴 접촉 수 (J8) · 위치 · 포트 (직접 · 덮임 → 탐색 · 미실현) ·
    복셀 관계 · PTFE · SDCP 근접 · 부피로 이미 이어진 몫 (k = 2) · VA (J2b) · SV · SA 후보 · 섬유당 접합 간격 ℓ_j

어떻게 — **생산 raster 를 사본 없이 잡는다**:
  ① 킷 `run_mpm.sh` 의 payload 호출을 러너와 같은 함수 (`sr01_stamp_compare.extract_payload_cmd`) 로 뽑고, 셸 변수 · 따옴표는
     bash 가 풀게 한다 (python3 를 argv 기록 함수로 가린다).  ② payload `main()` 을 이 프로세스에서 돌리며
     `step3_sigma.rasterize` 를 가로채 (BaseException) 인자를 잡고 멈춘다 — payload 의 좌표 변환 · 상 선택 · 플래그 해석을
     다시 쓰지 않는다 · STEP3 솔브 0.  ③ 잡은 인자로 `rasterize` 를 다시 부른다: 생산 (PTFE centerline) · off (PTFE 행 제거 =
     `ptfe_stamp off` 의 `_cond_ph` 와 같다 = face_alpha 의 sid 격자 · 설계 §3-2) · SDCP 없는 판 (SDCP 가 있을 때).
  ④ 섬유 경로 셀 = 생산 함수 `step3_sigma._fibre_segment_ijk` 를 섬유마다 부른 것.  census 의 조각 (gap_tol 규칙) 은 이 파일의
     세 줄 (`pieces_of`) 인데, 섬유마다 그 조각으로 다시 만든 셀이 생산 셀과 **같은지 실행 때 대조**한다 (다르면 거부).

단계 (설계 §2 머리 · 등록 R §2-1 · N17):
  단계 1 = SBE 침대 **하나** (SDCP 점이 하나라도 있으면 거부) → 원장 + census 미리보기 + 계획 `cjunc_plan.json` (정준 바이트) ·
           sha256.  1저자 확인 → 등록 R §2-1 개정 커밋 (숫자 + 계획 sha256 + 계획 파일 · 결과 0 건).
  단계 2 = DBE 침대들 — `--threshold-commit <개정 커밋>` · `--plan-path <리포 안 계획 경로>` · `--r-plan-path <같은 커밋의 R 런 사슬
           계획>` 필수.  도구가 확인: 커밋이 이 작업 트리 HEAD 의 조상 · 그 커밋 등록 R 문서의 `| S0 계획 해시 |` 줄 (하나) 끝 칸 = 계획
           파일 sha256 · 계획 식 재유도 · 정준 바이트 · ★ 10-21 (사전 리뷰 PRE-design-04 · 등록 R §2-1 · §2-1b · §11 ④) 같은 문서의
           `| 계획 해시 |` 줄 (하나 · 사슬 `rint_r_chain.registration_plan_hash` 그대로 · ⬜ = 거부) = R 런 계획 파일 sha256 · 그 꼴
           (`rint_r_chain.load_plan` — s_min 숫자 등록) · 두 계획 대조 (tol_ff_um = S0 values_um.tol_ff · len_law = 원장의 길이 법칙).

한정 (보고에 같이 싣는다): 기하만 · MPM 마지막 프레임 · instance = 관통 포함 기하 근접 (MPM 은 섬유 접촉 역학을 풀지 않는다) ·
  접촉 길이 L_c = 설계 §1-2 #13 (Q17) touch (판정 · 보고 판 = cjunc_registry) · 미리보기는 touch · band 두 판을 비교용으로 낸다 ·
  포트 · 자기 접촉 · VA 문턱 (미리보기) = 미리보기 정의 (보고의 notes) ·
  α 분포 = S1 `ptfe_face_alpha` 함수 그대로 (`alpha_census` · off 격자 · 면 자격 = 생산 σ 표 함수의 양수 패턴 · raster-only · 2 일 차).

  python3 scripts/ca_s0_census.py --stage 1 --kit ~/sdcp/kit_SBE_vgcf100 --out ~/sdcp/ca1_s0_sbe
  python3 scripts/ca_s0_census.py --stage 2 --threshold-commit <sha> --plan-path docs/data/<…>/cjunc_plan.json \\
          --r-plan-path docs/data/<…>/<R 런 계획>.json --kit ~/sdcp/kit_DBE_sdcp1um_vgcf100 --kit ~/sdcp/kit_DBE --out ~/sdcp/ca1_s0_dbe
"""
import argparse
import contextlib
import glob
import hashlib
import importlib.util
import inspect
import json
import math
import os
import platform
import re
import shlex
import subprocess
import sys
import tempfile
import time
import uuid

import numpy as np

_SELF_DIR = os.path.dirname(os.path.abspath(__file__))
if _SELF_DIR not in sys.path:
    sys.path.insert(0, _SELF_DIR)

import step3_sigma as s3                          # noqa: E402  (생산 raster · 경로 셀 · SID_NAME)
import carbon_junction as cj                      # noqa: E402  (접합 census 판정 · 보고 판 = cjunc_registry 그대로)
import ptfe_face_alpha as fa                      # noqa: E402  (α 분포 = S1 face_alpha 함수 그대로 · 사본 금지)
from fibre_segment_raster import cell_of, n_components_6face, segment_cells   # noqa: E402

#: 생산 모듈 (payload · raster) 이 있는 폴더 = step3_sigma 가 있는 곳 (정상 사용 = 이 도구와 같은 scripts/ · 변이 판을 리포 밖에서
#  불러도 생산 쪽은 리포 것을 쓴다).
SCRIPTS = os.path.dirname(os.path.abspath(s3.__file__))
ROOT = os.path.dirname(SCRIPTS)

SCHEMA = 'ca-s0-census-v4'                       # v2 (10-20 2 일 차) = junction_census 블록 (cjunc_registry 같은 함수) 추가 ·
#  ★ v3 (10-25 묶음 B · RCA2-03 · 1저자 10-23 Q3 (가)) = 같은 침대 칸 — inputs.settings_sha256 (킷 run_mpm.sh 의 payload 호출부 ·
#  `kit_settings_sha256`) · raster.sid_off_fp (off 격자의 `carbon_junction._grid_fp` = R 런 접합 원장 fp.sid 와 같은 함수) · 사슬
#  (`rint_r_chain.S0_REPORT_SCHEMA`) 이 이 schema 를 요구하고, R 직전 · 판정 때 `kit_input_record` 로 킷을 다시 해시해 대조한다 ·
#  ★ v4 (10-25 묶음 B · X6 · 1저자 10-23 Q20 (가)) = 단계 2 보고의 봉인 SV census (`sv_census_sealed` · 단계 1 = null · 단계 1 뜻 그대로)
PLAN_SCHEMA = 'ca-cjunc-plan-v1'
TOOL_VERSION = 's0-b3-registry-v1'               # 옛 s0-b0-preview-v1 = 미리보기 census 만
#: ★ 10-25 묶음 B (RCA2-03) — 원 입력 역할 = payload 호출의 입력 파일 (`kit_input_paths` · 이 모듈 · 사슬이 같은 이름을 쓴다) ·
#  fibre_dia 는 payload 호출에 --fibre-dia 가 있을 때만 (옛 `validate_kit_arrays` 와 같은 규칙)
KIT_ROLES = ('se', 'phase', 'fibre', 'fibre_kind', 'metrics_json', 'scaffold')
KIT_ROLES_OPTIONAL = ('fibre_dia',)
#: 접합 census (판정 · 보고 판) 의 격자 — off (= 잡은 생산 입력에서 PTFE 행을 뺀 raster = ptfe_stamp off · face_alpha 의 sid 격자 ·
#  다음 세대 판정 격자).  원장에는 PTFE 행을 포함한 전 상 입력을 준다 (P-junc 덮임 판정 · PTFE 는 셀을 찍지 않는다).
JUNCTION_GRID = 'off'
#: α 분포 (설계 §2 ① 끝 행 · 2 일 차) 의 면 자격 = 채널 도체 (σ > 0) 패턴 — 생산 σ 표 함수 (`step3_sigma.electronic_sigma_table` ·
#  `ionic_sigma_table`) 에 양수 단위값을 넣은 것 (payload 기본 = σ_PTFE 0 · σ_SWCNT > 0 · SWCNT 이온 투명).  α 는 면 기하 (캡슐 ∩ 면
#  구적) 라 σ 크기와 무관하고, 어느 sid 쌍 면에 α 를 거는가만 σ > 0 으로 정해진다 (`ptfe_face_alpha._channel_cond`).
ALPHA_SIG_E = s3.electronic_sigma_table(1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0)
ALPHA_SIG_I = s3.ionic_sigma_table(1.0, 1.0, False)
ALPHA_DIA_LAW = 'rope'                            # (가) 주 = 모든 경로 Ø0.248 µm (설계 §3-1 · N12 · DIA_UNCHECKED)
R_DOC_DEFAULT = 'docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md'
#: 등록 R §2-1 · 설계 §1-2 #11 · #18 · #29 — 식은 지금 고정 (N17).
R_PORT_UM = 0.30                 # 포트 탐색 반경 (물리 단위 · 격자에 묶지 않는다 · RINTG-05 부류)
L_PAR_FACTOR = 2.0               # L_par = 2 (r_fi + r_fj)
K_ALPHA = 8                      # S1 α 구적 (봉인 · 기록만)
K_SDCP_CELLS = 2                 # "부피로 이미 이어진 접합" 판정 셀 수 (보고 매개변수)
PTFE_ROPE_D_UM = 0.248           # (가) rope Ø — [카드] lee2025_dual_fibrous_ptfe_dry_electrode Fig. S2c · 1저자 규약 선택 (N12)
TOL_FS_PREVIEW_UM = 0.0          # VA (J2b) 문턱 — 설계에 숫자 없음 · J2b 판정문 예시 경계 = r_f + R_AM (v3 §5)
F11_BAND = (0.5, 2.0)            # 캡슐 부피 비 밴드 (CL-60 등록 2 배 · 설계 §3-4 F11)
PROX_CUTOFF_UM = 2.0             # PTFE 근접 분포의 계산 상한 (그 밖 = '> cutoff' 로 센다)
PATH_PHASES = (2, 4)             # 중심선이 필요한 상 (2 VGCF · 4 PTFE)
VGCF, SUPERP, PTFE, SDCP, SWCNT = 2, 3, 4, 5, 6
SID_ADDITIVE = {3: 'VGCF', 4: 'SuperP', 5: 'SDCP', 7: 'PTFE', 8: 'SWCNT'}
PHASE_ADDITIVE = {2: 'VGCF', 3: 'SuperP', 4: 'PTFE', 5: 'SDCP', 6: 'SWCNT'}
#: S0-2 — 출력 키에 이 낱말이 들어가면 안 된다 (σ · 전류 · 소산 · 풀이 칸 없음).
FORBIDDEN_KEY_STEMS = ('sigma', 'σ', 'current', 'dissip', 'conduct', 'resist', 'joule', 'flux', 'potential',
                       'n_dof', 'cg_')
FORMULAS = {
    'u': ('median of within-piece consecutive VGCF path point spacings of the stage-1 (SBE) bed, divided by 2 '
          '(pieces = the gap rule of step3_sigma._fibre_segment_ijk with gap_tol; the gap jumps are excluded)'),
    'tol_ff': 'min(u, r_f)',
    'L_par': '2 (r_fi + r_fj)',
    'r_port': '0.30 um (physical units)',
    'tol_P': 'tol_ff',
    'tol_sj': 'tol_ff',
    'K_alpha': '8 (sealed before F7)',
    'k_sdcp_cells': '2 (report parameter)',
}
GAP_TOL_PRODUCTION = float(inspect.signature(s3.rasterize).parameters['fid_gap_tol'].default)
R_F_UM = None                    # VGCF 반지름 — additives.VGCF_D / 2 (아래에서 한 번 읽는다)
try:
    import additives as _ad      # noqa: E402
    R_F_UM = float(_ad.VGCF_D) / 2.0
except Exception:                # noqa: BLE001
    R_F_UM = None
NOTES = (
    '접합 census 판정 · 보고 판 = junction_census (B3 carbon_junction.cjunc_registry 그대로 · off 격자 · 계획 문턱 · '
    's_min 안 씀 (S0 계획에 칸 없음) = 거르지 않음 · 후보별 배열 = s0_junctions_<킷>.npz) · census_preview = B0 미리보기 '
    '(판정 · 보고에 쓰지 않는다)',
    '자기 (같은 가닥) 후보 = 원장 규칙 (★ 10-21 Q-B: 같은 조각 중심선 쌍 d ≤ D · 바닥 s > D 그리고 s > (π/2)·d · 후보 무리마다 접점 쌍의 '
    '경로 호 길이 s — s_min None 이라 바닥 쌍 전부 · 그 L_c = 바닥 쌍의 닿음 (s_min 이 줄일 수 있다)) — s_min 을 정하는 근거 · s_min 숫자는 '
    '등록 R §2-1 개정 (이 도구는 고르지 않는다) · 같은 fid 의 끊긴 조각 = 서로 다른 섬유 규칙 (자기 후보 아님)',
    f'접촉 길이 L_c = 설계 §1-2 #13 (1저자 10-20 밤 Q17) touch — 두 가닥 각각에서 중심선 거리 ≤ r_fi + r_fj 인 구간 길이의 '
    f'최댓값 (판정 · 보고 판 junction_census = cjunc_registry 규칙 {cj.CJUNC_LC_RULE} · 길이 법칙 {cj.CJUNC_LEN_LAW}) · '
    'census_preview 의 두 판 (touch · band = d ≤ 검출 문턱 r_fi + r_fj + tol_ff 인 중심선 길이) 은 비교용 · band 판에서는 수직 '
    '스침도 2√(thr² − (2r_f)²) = 0.335 µm > L_par 0.30 (tol_ff 0.075 일 때)',
    'instance = 관통 포함 기하 근접 — MPM 은 섬유 접촉 역학을 풀지 않는다 · 중심선 위치 = MPM 점 간격만큼 불확도',
    '자기 접촉 (미리보기 정의) = 같은 fid · 선분 번호 차 ≥ 2 · d ≤ thr · 두 최근접점의 호 길이 차 > (π/2)·thr',
    '포트 (미리보기 정의) = 최근접점이 든 셀이 그 fid 경로 셀이고 sid 3 이면 직접 · 아니면 그 fid 경로 셀 중 sid 3 · '
    '최근접점 ↔ 셀 중심 유클리드 거리 ≤ r_port · 동률 = 경로 열 번호 작은 셀 · 없으면 미실현',
    'VA (J2b) 문턱 tol_fs = 0 — 설계 · 계획에 숫자 없음 · J2b 판정문 예시 (경계 = r_f + R_AM)',
    '조각 규칙 = step3_sigma._fibre_segment_ijk 의 gap_tol 규칙 — 이 도구의 세 줄 사본은 섬유마다 생산 함수 셀과 실행 때 대조 '
    '(다르면 거부)',
    'off 격자 = 잡은 생산 입력에서 PTFE (phase 4) 행을 뺀 raster = ptfe_stamp off 의 _cond_ph · face_alpha 의 sid 격자',
    '캡슐 부피 (F11) = 조각마다 Σ 선분 길이 × π r_P² + 구 하나 (4/3 π r_P³) · 겹침 미차감 · r_P = Ø0.248 / 2',
)
_STATE_KEYS = ('rasterize', 'GPU_SOLVE', 'REQUIRE_GPU', 'AMG_SOLVE', 'CG_MAXITER', 'LAST_PTFE_BLOCK', 'LAST_BACKEND')


class S0Error(Exception):
    """S0 입력 · 단계 계약 위반 — 조용히 강등하지 않고 거부한다."""


class _RasterCaptured(BaseException):
    """payload 의 STEP3 try (`except Exception`) 를 통과해 rasterize 직전에 멈추는 신호."""


# ══ 작은 도우미 ══════════════════════════════════════════════════════════════════════════════════════════════════
def _sha256_file(path, chunk=1 << 22):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def _hist(vals):
    u, c = np.unique(np.asarray(vals).ravel(), return_counts=True)
    return {str(int(a)): int(b) for a, b in zip(u, c)}


def _dist(x):
    x = np.asarray(x, np.float64).ravel()
    x = x[np.isfinite(x)]
    if not len(x):
        return {'n': 0}
    q = np.percentile(x, [0, 10, 50, 90, 100])
    return {'n': int(len(x)), 'min': float(q[0]), 'p10': float(q[1]), 'p50': float(q[2]), 'p90': float(q[3]),
            'max': float(q[4]), 'mean': float(x.mean())}


def _count(labels):
    out = {}
    for v in labels:
        out[v] = out.get(v, 0) + 1
    return dict(sorted(out.items()))


def schema_forbidden_keys(obj, path=''):
    """S0-2 — σ · 전류 · 소산 · 풀이 낱말이 든 키의 경로 목록 (중첩 dict · 목록)."""
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            ks = str(k)
            p = f'{path}.{ks}' if path else ks
            if any(stem in ks.lower() for stem in FORBIDDEN_KEY_STEMS):
                out.append(p)
            out.extend(schema_forbidden_keys(v, p))
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            out.extend(schema_forbidden_keys(v, f'{path}[{i}]'))
    return out


# ══ 기하 원시 ════════════════════════════════════════════════════════════════════════════════════════════════════
def seg_seg_closest(P1, Q1, P2, Q2):
    """선분 [P1,Q1] ↔ [P2,Q2] 최근접 (행마다 · Ericson RTCD 5.1.9) → (d, s, t, C1, C2) · float64.  퇴화 (점) · 평행 처리."""
    P1 = np.asarray(P1, np.float64).reshape(-1, 3); Q1 = np.asarray(Q1, np.float64).reshape(-1, 3)
    P2 = np.asarray(P2, np.float64).reshape(-1, 3); Q2 = np.asarray(Q2, np.float64).reshape(-1, 3)
    d1 = Q1 - P1; d2 = Q2 - P2; r = P1 - P2
    a = (d1 * d1).sum(1); e = (d2 * d2).sum(1); f = (d2 * r).sum(1)
    c = (d1 * r).sum(1); b = (d1 * d2).sum(1)
    n = len(a)
    s = np.zeros(n); t = np.zeros(n)
    tiny = 1e-30
    dg1 = a <= tiny; dg2 = e <= tiny
    m = dg1 & ~dg2
    t[m] = np.clip(f[m] / e[m], 0.0, 1.0)
    m = ~dg1 & dg2
    s[m] = np.clip(-c[m] / a[m], 0.0, 1.0)
    g = ~dg1 & ~dg2
    if g.any():
        ag, bg, cg, eg, fg = a[g], b[g], c[g], e[g], f[g]
        den = ag * eg - bg * bg
        par = den <= 1e-14 * ag * eg
        sg = np.where(par, 0.0, np.clip((bg * fg - cg * eg) / np.where(par, 1.0, den), 0.0, 1.0))
        tg = (bg * sg + fg) / eg
        lo = tg < 0.0; hi = tg > 1.0
        tg = np.clip(tg, 0.0, 1.0)
        sg = np.where(lo, np.clip(-cg / ag, 0.0, 1.0), np.where(hi, np.clip((bg - cg) / ag, 0.0, 1.0), sg))
        s[g] = sg; t[g] = tg
    C1 = P1 + d1 * s[:, None]; C2 = P2 + d2 * t[:, None]
    return np.sqrt(((C1 - C2) ** 2).sum(1)), s, t, C1, C2


def _pt_seg_d2(X, P, Q):
    d = Q - P
    e = (d * d).sum(-1)
    u = np.where(e > 0, ((X - P) * d).sum(-1) / np.where(e > 0, e, 1.0), 0.0)
    u = np.clip(u, 0.0, 1.0)
    C = P + d * u[..., None]
    return ((X - C) ** 2).sum(-1)


def _sublevel(Pa, Qa, Pb, Qb, D, tstar, iters=64):
    """선분 a 위 {t : dist(a(t), 선분 b) ≤ D} = 구간 [tl, tr] (볼록) — t* = 최근접 매개변수 · 이분법.  → (tl, tr, ok)."""
    da = Qa - Pa
    D2 = float(D) * float(D)

    def f(t):
        return _pt_seg_d2(Pa + da * t[:, None], Pb, Qb)
    ts = np.asarray(tstar, np.float64)
    ok = f(ts) <= D2 * (1.0 + 1e-12) + 1e-30
    z = np.zeros_like(ts); o = np.ones_like(ts)
    f0 = f(z) <= D2; f1 = f(o) <= D2
    lo, hi = z.copy(), ts.copy()                       # 왼쪽 경계: f(lo) > D², f(hi) ≤ D²
    need = ok & ~f0
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        ins = f(mid) <= D2
        hi = np.where(need & ins, mid, hi); lo = np.where(need & ~ins, mid, lo)
    tl = np.where(f0, 0.0, hi)
    lo, hi = ts.copy(), o.copy()                       # 오른쪽 경계: f(lo) ≤ D², f(hi) > D²
    need = ok & ~f1
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        ins = f(mid) <= D2
        lo = np.where(need & ins, mid, lo); hi = np.where(need & ~ins, mid, hi)
    tr = np.where(f1, 1.0, lo)
    tl = np.where(ok, tl, 0.0); tr = np.where(ok, np.maximum(tr, tl), 0.0)
    return tl, tr, ok


def _union_measure(group, tl, tr):
    """같은 group (같은 선분) 의 구간 [tl, tr] ⊂ [0, 1] 합집합 길이 → group 별 (dense group id 0..G-1).
    결정적 — (group, tl, tr) 정렬 뒤 차례로 합친다 (offset 더하기 없음 · 입력 행 순서 · group 번호와 무관한 비트)."""
    if not len(group):
        return np.zeros(0)
    G = int(group.max()) + 1
    order = np.lexsort((tr, tl, group))
    g = group[order]; a = tl[order]; b = tr[order]
    out = np.zeros(G)
    st = np.r_[0, np.nonzero(g[1:] != g[:-1])[0] + 1]
    en = np.r_[st[1:], len(g)]
    single = en - st == 1
    out[g[st[single]]] = b[st[single]] - a[st[single]]
    for s0, e0 in zip(st[~single], en[~single]):
        tot, cur_a, cur_b = 0.0, a[s0], b[s0]
        for q in range(s0 + 1, e0):
            if a[q] > cur_b:
                tot += cur_b - cur_a
                cur_a, cur_b = a[q], b[q]
            elif b[q] > cur_b:
                cur_b = b[q]
        out[g[s0]] = tot + (cur_b - cur_a)
    return out


def pieces_of(Q, gap_tol):
    """경로 점열 → 조각 — `step3_sigma._fibre_segment_ijk` 의 gap 규칙 (간격 > gap_tol · 중앙값 → 끊음) 과 같은 식.
    ⚠ 세 줄 사본 — `census_kit` 가 섬유마다 생산 함수 셀과 대조해 같을 때만 쓴다 (다르면 거부)."""
    Q = np.asarray(Q, np.float64).reshape(-1, 3)
    if len(Q) < 2:
        return [Q]
    d = np.linalg.norm(np.diff(Q, axis=0), axis=1)
    med = float(np.median(d))
    brk = (np.nonzero(d > gap_tol * med)[0] + 1) if med > 0 else np.array([], int)
    return np.split(Q, brk) if len(brk) else [Q]


def spacing_stats(paths_pieces):
    """조각 안 연속 점 간격 (틈 제외) → {'n', 'median_um', 'u_um' = 중앙값 / 2, …}."""
    ds = [np.linalg.norm(np.diff(np.asarray(R, np.float64), axis=0), axis=1)
          for pcs in paths_pieces for R in pcs if len(R) >= 2]
    v = np.concatenate(ds) if ds else np.zeros(0)
    if not len(v):
        return {'n': 0, 'median_um': None, 'u_um': None}
    med = float(np.median(v))
    return {'n': int(len(v)), 'median_um': med, 'u_um': med / 2.0, 'p10_um': float(np.percentile(v, 10)),
            'p90_um': float(np.percentile(v, 90)), 'max_um': float(v.max())}


def _segments(paths):
    """[(fid, 조각 목록)] → 선분 배열 (조각 안 연속 점 · 한 점 조각 = 길이 0 선분) · fid 안 번호 IDX · 호 길이 ARC."""
    P0, P1, F, IDX, ARC, LEN = [], [], [], [], [], []
    for fid, pcs in paths:
        k = 0
        arc = 0.0
        for R in pcs:
            R = np.asarray(R, np.float64).reshape(-1, 3)
            if not len(R):
                continue
            if len(R) == 1:
                a0, a1, ln = R, R, np.zeros(1)
            else:
                a0, a1 = R[:-1], R[1:]
                ln = np.linalg.norm(a1 - a0, axis=1)
            m = len(a0)
            P0.append(a0); P1.append(a1); LEN.append(ln)
            F.append(np.full(m, int(fid), np.int64)); IDX.append(np.arange(k, k + m, dtype=np.int64))
            ARC.append(arc + np.concatenate([[0.0], np.cumsum(ln)[:-1]]))
            k += m
            arc += float(ln.sum())
    if not P0:
        z3 = np.zeros((0, 3)); z = np.zeros(0)
        return {'P0': z3, 'P1': z3, 'F': z.astype(np.int64), 'IDX': z.astype(np.int64), 'ARC': z, 'LEN': z}
    return {'P0': np.vstack(P0), 'P1': np.vstack(P1), 'F': np.concatenate(F), 'IDX': np.concatenate(IDX),
            'ARC': np.concatenate(ARC), 'LEN': np.concatenate(LEN)}


def _lex_lt(A, B):
    """행마다 A < B (사전순) — 같은 행이면 False."""
    lt = np.zeros(len(A), bool)
    eq = np.ones(len(A), bool)
    for k in range(A.shape[1]):
        lt |= eq & (A[:, k] < B[:, k])
        eq &= A[:, k] == B[:, k]
    return lt


def _cand_pairs(M, h, rad):
    """|M_i − M_j| ≤ rad + h_i + h_j 인 쌍 (i < j) — 두 단 (짧은 선분 = 한 번의 query_pairs · 긴 선분 = 따로)."""
    from scipy.spatial import cKDTree
    n = len(M)
    if n < 2:
        return np.zeros((0, 2), np.int64)
    tree = cKDTree(M)
    hq = float(np.quantile(h, 0.99)); hmax = float(h.max())
    parts = []
    pr = tree.query_pairs(rad + 2.0 * hq, output_type='ndarray')
    if len(pr):
        parts.append(pr.astype(np.int64))
    for i in np.nonzero(h > hq)[0]:
        nb = np.asarray(tree.query_ball_point(M[i], rad + h[i] + hmax), np.int64)
        nb = nb[nb != i]
        if len(nb):
            parts.append(np.column_stack([np.full(len(nb), i, np.int64), nb]))
    if not parts:
        return np.zeros((0, 2), np.int64)
    pr = np.sort(np.vstack(parts), axis=1)
    key = np.unique(pr[:, 0] * np.int64(n) + pr[:, 1])
    pr = np.column_stack([key // n, key % n])
    dm = np.linalg.norm(M[pr[:, 0]] - M[pr[:, 1]], axis=1)
    return pr[dm <= rad + h[pr[:, 0]] + h[pr[:, 1]] + 1e-12]


def _components(keys, NI):
    """(fa, fb, ia, ib) 압축 키 → 이웃 (ia ± 1, ib ± 1) 연결 성분 라벨."""
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    n = len(keys)
    order = np.argsort(keys, kind='stable')
    ks = keys[order]
    rows, cols = [], []
    for da in (-1, 0, 1):
        for db in (-1, 0, 1):
            if da == 0 and db == 0:
                continue
            k2 = keys + da * NI + db
            pos = np.searchsorted(ks, k2)
            ok = pos < n
            ok[ok] = ks[pos[ok]] == k2[ok]
            rows.append(np.nonzero(ok)[0]); cols.append(order[pos[ok]])
    r = np.concatenate(rows) if rows else np.zeros(0, int)
    c = np.concatenate(cols) if cols else np.zeros(0, int)
    g = coo_matrix((np.ones(len(r)), (r, c)), shape=(n, n))
    _, lab = connected_components(g, directed=False)
    return lab


def vv_census(paths, r_f_um, tol_ff_um, L_par_um):
    """VGCF–VGCF 접합 instance (J2a · J2c · 자기 접촉) — B0 미리보기.

    paths = [(fid, 조각 목록)] (µm) · 반지름 r_f 공통.  instance = 같은 (fa, fb) 쌍에서 선분 번호가 (±1, ±1) 로 이어진 근접 쌍의 연결 성분
    (조각 · 선분 경계를 넘어도 하나 · 떨어진 두 자리 = 둘).  → dict (수 · 판별 · 인스턴스 배열 (정준 정렬))."""
    rf = float(r_f_um)
    thr = 2.0 * rf + float(tol_ff_um)
    Dt = 2.0 * rf
    sg = _segments(paths)
    P0, P1, F, IDX, ARC, LEN = (sg[k] for k in ('P0', 'P1', 'F', 'IDX', 'ARC', 'LEN'))
    lcdef = {'touch': 'length along the centreline where d <= r_fi + r_fj (surfaces touch or interpenetrate)',
             'band': 'length along the centreline where d <= r_fi + r_fj + tol_ff (the detection threshold)',
             'L': 'max over the two fibres; union over partner segments; long = L > L_par (strict)'}
    empty_inst = {k: np.zeros(0) for k in ('d_min', 'gap', 'theta_deg', 'L_touch', 'L_band')}
    empty_inst.update({'fa': np.zeros(0, np.int64), 'fb': np.zeros(0, np.int64), 'is_self': np.zeros(0, bool),
                       'C1': np.zeros((0, 3)), 'C2': np.zeros((0, 3)), 'mid': np.zeros((0, 3))})
    out = {'n_vv': 0, 'n_self': 0, 'n_long': {'touch': 0, 'band': 0}, 'thr_um': thr, 'L_par_um': float(L_par_um),
           'lc_definition': lcdef, 'n_segments': int(len(F)), 'n_rows': 0, 'inst': empty_inst}
    if len(F) < 2:
        return out
    M = 0.5 * (P0 + P1)
    pr = _cand_pairs(M, 0.5 * LEN, thr)
    rows = {k: [] for k in ('i', 'j', 'd', 's', 't', 'C1', 'C2')}
    CH = 1_000_000
    for c0 in range(0, len(pr), CH):
        i = pr[c0:c0 + CH, 0]; j = pr[c0:c0 + CH, 1]
        keep = ~((F[i] == F[j]) & (np.abs(IDX[i] - IDX[j]) <= 1))
        i, j = i[keep], j[keep]
        if not len(i):
            continue
        #  방향 정준 — 좌표 사전순으로 작은 선분을 먼저 넣어 계산한다 (입력 순서 · fid 이름이 바뀌어도 같은 비트 · S0-4).
        flip = _lex_lt(np.hstack([P0[j], P1[j]]), np.hstack([P0[i], P1[i]]))
        u, v = np.where(flip, j, i), np.where(flip, i, j)
        d, s_u, t_v, Cu, Cv = seg_seg_closest(P0[u], P1[u], P0[v], P1[v])
        s, t = np.where(flip, t_v, s_u), np.where(flip, s_u, t_v)
        C1, C2 = np.where(flip[:, None], Cv, Cu), np.where(flip[:, None], Cu, Cv)
        ok = d <= thr
        same = F[i] == F[j]
        sep = np.abs((ARC[i] + s * LEN[i]) - (ARC[j] + t * LEN[j]))
        ok &= ~same | (sep > 0.5 * math.pi * thr)
        for k, v in (('i', i), ('j', j), ('d', d), ('s', s), ('t', t), ('C1', C1), ('C2', C2)):
            rows[k].append(v[ok])
    if not rows['i'] or not sum(len(x) for x in rows['i']):
        return out
    i = np.concatenate(rows['i']); j = np.concatenate(rows['j']); d = np.concatenate(rows['d'])
    s = np.concatenate(rows['s']); t = np.concatenate(rows['t'])
    C1 = np.vstack(rows['C1']); C2 = np.vstack(rows['C2'])
    sw = (F[i] > F[j]) | ((F[i] == F[j]) & (IDX[i] > IDX[j]))
    i, j = np.where(sw, j, i), np.where(sw, i, j)
    s, t = np.where(sw, t, s), np.where(sw, s, t)
    C1, C2 = np.where(sw[:, None], C2, C1), np.where(sw[:, None], C1, C2)
    fa, fb, ia, ib = F[i], F[j], IDX[i], IDX[j]
    uf, inv = np.unique(np.concatenate([fa, fb]), return_inverse=True)
    ra, rb = inv[:len(fa)], inv[len(fa):]
    NF = int(len(uf)); NI = int(max(ia.max(), ib.max())) + 3
    if float(NF) ** 2 * float(NI) ** 2 >= 2.0 ** 62:
        raise S0Error('instance 키가 int64 를 넘는다 (섬유 · 선분 수) — 구현 한계')
    keys = ((ra.astype(np.int64) * NF + rb) * NI + (ia + 1)) * NI + (ib + 1)
    lab = _components(keys, NI)
    n_inst = int(lab.max()) + 1
    mid_r = 0.5 * (C1 + C2)
    o2 = np.lexsort((mid_r[:, 2], mid_r[:, 1], mid_r[:, 0], d, lab))
    first = np.r_[True, lab[o2][1:] != lab[o2][:-1]]
    rep = o2[first]                                   # instance 마다 최소 d 행 · 동률 = 중점 사전순 (행 순서 무관)
    # 접촉 길이 — 두 판 · 두 쪽
    L = {}
    for nm, D in (('touch', Dt), ('band', thr)):
        sides = []
        for (pa, qa, pb, qb, ts, seg_id, ln) in ((P0[i], P1[i], P0[j], P1[j], s, IDX[i], LEN[i]),
                                                 (P0[j], P1[j], P0[i], P1[i], t, IDX[j], LEN[j])):
            tl, tr, _ok = _sublevel(pa, qa, pb, qb, D, ts)
            gk = lab.astype(np.int64) * (NI + 2) + seg_id
            ug, gi = np.unique(gk, return_inverse=True)
            meas = _union_measure(gi.astype(np.int64), tl, tr)
            seglen = np.zeros(len(ug)); seglen[gi] = ln
            per = np.zeros(n_inst)
            np.add.at(per, (ug // (NI + 2)).astype(np.int64), meas * seglen)
            sides.append(per)
        L[nm] = np.maximum(sides[0], sides[1])
    ua = (P1[i[rep]] - P0[i[rep]]); ub = (P1[j[rep]] - P0[j[rep]])
    na = np.linalg.norm(ua, axis=1); nb = np.linalg.norm(ub, axis=1)
    with np.errstate(invalid='ignore', divide='ignore'):
        cosv = np.abs((ua * ub).sum(1)) / (na * nb)
    theta = np.where((na > 0) & (nb > 0), np.degrees(np.arccos(np.clip(cosv, 0.0, 1.0))), np.nan)
    inst = {'fa': fa[rep], 'fb': fb[rep], 'is_self': fa[rep] == fb[rep], 'd_min': d[rep], 'gap': d[rep] - 2.0 * rf,
            'theta_deg': theta, 'L_touch': L['touch'], 'L_band': L['band'], 'C1': C1[rep], 'C2': C2[rep]}
    inst['mid'] = 0.5 * (inst['C1'] + inst['C2'])
    order = np.lexsort(tuple(inst['C2'][:, k] for k in (2, 1, 0)) + tuple(inst['C1'][:, k] for k in (2, 1, 0))
                       + (inst['fb'], inst['fa']))
    inst = {k: v[order] for k, v in inst.items()}
    out.update({'n_vv': int((~inst['is_self']).sum()), 'n_self': int(inst['is_self'].sum()), 'n_rows': int(len(i)),
                'n_long': {'touch': int((inst['L_touch'] > float(L_par_um)).sum()),
                           'band': int((inst['L_band'] > float(L_par_um)).sum())}, 'inst': inst})
    return out


def fiber_sphere_instances(paths, centers, radii, r_f_um, tol_um):
    """섬유 중심선 ↔ 구 중심 d ≤ R + r_f + tol (J2b) — (구, fid) 마다 선분 번호가 이어진 묶음 = instance 하나."""
    from scipy.spatial import cKDTree
    sg = _segments(paths)
    C = np.asarray(centers, np.float64).reshape(-1, 3); R = np.asarray(radii, np.float64).reshape(-1)
    res = {'n_instances': 0, 'n_pairs': 0, 'gap_um': np.zeros(0), 'n_spheres_touching': 0, 'n_spheres_ge2_fibres': 0}
    if not len(sg['F']) or not len(C):
        return res
    M = 0.5 * (sg['P0'] + sg['P1'])
    h = 0.5 * sg['LEN']
    tree = cKDTree(M)
    lists = tree.query_ball_point(C, R + float(r_f_um) + float(tol_um) + float(h.max()))
    kk = np.concatenate([np.full(len(x), q, np.int64) for q, x in enumerate(lists)]) if len(C) else np.zeros(0, int)
    ss = np.concatenate([np.asarray(x, np.int64) for x in lists]) if len(C) else np.zeros(0, int)
    if not len(ss):
        return res
    dd = np.sqrt(_pt_seg_d2(C[kk], sg['P0'][ss], sg['P1'][ss]))
    ok = dd <= R[kk] + float(r_f_um) + float(tol_um)
    kk, ss, dd = kk[ok], ss[ok], dd[ok]
    if not len(kk):
        return res
    fid, idx = sg['F'][ss], sg['IDX'][ss]
    o = np.lexsort((idx, fid, kk))
    kk, fid, idx, dd = kk[o], fid[o], idx[o], dd[o]
    new = np.r_[True, (kk[1:] != kk[:-1]) | (fid[1:] != fid[:-1]) | (idx[1:] - idx[:-1] > 1)]
    inst = np.cumsum(new) - 1
    gmin = np.full(int(inst.max()) + 1, np.inf)
    np.minimum.at(gmin, inst, dd - R[kk] - float(r_f_um))
    pairs = np.unique(np.column_stack([kk, fid]), axis=0)
    _, per_sphere = np.unique(pairs[:, 0], return_counts=True)
    res.update({'n_instances': int(len(gmin)), 'n_pairs': int(len(pairs)), 'gap_um': np.sort(gmin),
                'n_spheres_touching': int(len(per_sphere)), 'n_spheres_ge2_fibres': int((per_sphere >= 2).sum())})
    return res


def _min_dist_to_segments(X, paths, cutoff):
    """점 X ↔ 선분 집합 최소 거리 (cutoff + 반선분 안의 후보만 · 없으면 inf)."""
    from scipy.spatial import cKDTree
    X = np.asarray(X, np.float64).reshape(-1, 3)
    sg = _segments(paths)
    out = np.full(len(X), np.inf)
    if not len(X) or not len(sg['F']):
        return out
    M = 0.5 * (sg['P0'] + sg['P1'])
    tree = cKDTree(M)
    lists = tree.query_ball_point(X, float(cutoff) + 0.5 * float(sg['LEN'].max()))
    xi = np.concatenate([np.full(len(x), q, np.int64) for q, x in enumerate(lists)])
    si = np.concatenate([np.asarray(x, np.int64) for x in lists])
    if not len(si):
        return out
    d2 = _pt_seg_d2(X[xi], sg['P0'][si], sg['P1'][si])
    m2 = np.full(len(X), np.inf)
    np.minimum.at(m2, xi, d2)
    out = np.sqrt(m2)
    out[out > cutoff] = np.inf
    return out


# ══ 격자 원시 ════════════════════════════════════════════════════════════════════════════════════════════════════
def voxel_relation(ca, cb):
    d = np.abs(np.asarray(ca, np.int64) - np.asarray(cb, np.int64))
    if d.max() == 0:
        return 'same'
    if d.max() >= 2:
        return 'apart'
    return {1: 'face', 2: 'edge', 3: 'vertex'}[int(d.sum())]


def port_of(C, path_cells, grid, lo, vox, r_port, tie_tol=1e-12):
    """instance 최근접점 C → 그 fid 의 포트 셀 (미리보기 정의 · 보고 notes).  → (상태, 셀 | None, 거리 | None)."""
    C = np.asarray(C, np.float64)
    lo = np.asarray(lo, np.float64)
    c = cell_of(C - lo, vox)
    shape = np.asarray(grid.shape)
    if (c < 0).any() or (c >= shape).any():
        return 'outside_box', None, None
    pc = np.asarray(path_cells, np.int64).reshape(-1, 3)
    inpath = bool(len(pc) and (pc == c).all(1).any())
    sc = int(grid[c[0], c[1], c[2]])
    if inpath and sc == 3:
        return 'direct', tuple(int(x) for x in c), float(np.linalg.norm(C - ((c + 0.5) * vox + lo)))
    reason = ('covered:' + s3.SID_NAME.get(sc, 'pore' if sc == 0 else f'sid{sc}')) if inpath else 'not_in_path'
    if not len(pc):
        return reason + '→unrealized', None, None
    sids = grid[pc[:, 0], pc[:, 1], pc[:, 2]]
    cand = np.nonzero(sids == 3)[0]
    if not len(cand):
        return reason + '→unrealized', None, None
    dist = np.linalg.norm((pc[cand] + 0.5) * vox + lo - C, axis=1)
    w = dist <= float(r_port) + 1e-12
    if not w.any():
        return reason + '→unrealized', None, None
    ci, dw = cand[w], dist[w]
    pick = int(ci[dw <= dw.min() + tie_tol].min())
    cell = pc[pick]
    return reason + '→searched', tuple(int(x) for x in cell), float(np.linalg.norm((cell + 0.5) * vox + lo - C))


_D6 = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))


def via_sdcp_depth(grid, pa, pb, k):
    """포트 pa → SDCP 셀 (sid 5) 사슬 (6-면) → pb 에 면으로 닿기까지의 SDCP 셀 수 ≤ k · 없으면 None."""
    pa = tuple(int(x) for x in pa); pb = tuple(int(x) for x in pb)
    sh = grid.shape

    def nbrs(c):
        for d in _D6:
            q = (c[0] + d[0], c[1] + d[1], c[2] + d[2])
            if 0 <= q[0] < sh[0] and 0 <= q[1] < sh[1] and 0 <= q[2] < sh[2]:
                yield q
    frontier, seen = [pa], {pa}
    for depth in range(1, int(k) + 1):
        nxt = []
        for c in frontier:
            for q in nbrs(c):
                if q not in seen and grid[q] == 5:
                    seen.add(q); nxt.append(q)
        if any(pb in set(nbrs(q)) for q in nxt):
            return depth
        if not nxt:
            return None
        frontier = nxt
    return None


def membership_counts(path_cells_list, shape):
    """섬유마다 경로 셀 (고유) → 셀별 멤버십 수 (교차 셀 = ≥ 2)."""
    lins = [np.unique(np.ravel_multi_index(np.asarray(c, np.int64).reshape(-1, 3).T, shape))
            for c in path_cells_list if len(c)]
    allv = np.concatenate(lins) if lins else np.zeros(0, np.int64)
    return np.unique(allv, return_counts=True)


def sdcp_via(grid, cell_lin, cell_fid):
    """SDCP 셀 (sid 5) 6-면 덩어리 중 서로 다른 VGCF fid 둘 이상의 sid 3 셀과 면으로 닿는 것 (SV 우회 후보 · 설계 §4-5)."""
    from scipy import ndimage
    lab, ncomp = ndimage.label(grid == 5)
    res = {'n_components': int(ncomp), 'n_bridging': 0, 'n_fid_pairs': 0, 'max_fibres_per_component': 0}
    if not ncomp or not len(cell_lin):
        return res
    order = np.argsort(cell_lin, kind='stable')
    Ls = np.asarray(cell_lin, np.int64)[order]; Fs = np.asarray(cell_fid, np.int64)[order]
    pl, pf = [], []
    for ax in range(3):
        for sgn in (1, -1):
            sa = [slice(None)] * 3; sb = [slice(None)] * 3
            if sgn > 0:
                sa[ax] = slice(0, -1); sb[ax] = slice(1, None)
            else:
                sa[ax] = slice(1, None); sb[ax] = slice(0, -1)
            A = lab[tuple(sa)]; B = grid[tuple(sb)]
            m = (A > 0) & (B == 3)
            if not m.any():
                continue
            ix = [x.astype(np.int64) for x in np.nonzero(m)]
            if sgn > 0:
                ix[ax] = ix[ax] + 1
            nl = np.ravel_multi_index(tuple(ix), grid.shape)
            labs = A[m].astype(np.int64)
            a0 = np.searchsorted(Ls, nl, 'left'); a1 = np.searchsorted(Ls, nl, 'right')
            cnt = a1 - a0
            if not cnt.sum():
                continue
            rep = np.repeat(np.arange(len(nl)), cnt)
            pos = np.repeat(a0, cnt) + (np.arange(int(cnt.sum())) - np.repeat(np.cumsum(cnt) - cnt, cnt))
            pl.append(labs[rep]); pf.append(Fs[pos])
    if not pl:
        return res
    pairs = np.unique(np.column_stack([np.concatenate(pl), np.concatenate(pf)]), axis=0)
    ul, cn = np.unique(pairs[:, 0], return_counts=True)
    fp = set()
    for L_ in ul[cn >= 2]:
        fs = np.sort(pairs[pairs[:, 0] == L_, 1])
        for a in range(len(fs)):
            for b in range(a + 1, len(fs)):
                fp.add((int(fs[a]), int(fs[b])))
    res.update({'n_bridging': int((cn >= 2).sum()), 'n_fid_pairs': int(len(fp)), 'max_fibres_per_component': int(cn.max())})
    return res


def _runs(mask):
    """True 연속 구간 길이들."""
    m = np.asarray(mask, bool)
    if not m.any():
        return []
    d = np.diff(np.r_[0, m.astype(np.int8), 0])
    st = np.nonzero(d == 1)[0]; en = np.nonzero(d == -1)[0]
    return (en - st).tolist()


# ══ 접합 census — 판정 · 보고 판 (B3 cjunc_registry 같은 함수) ═══════════════════════════════════════════════════════
def _jf(x):
    """JSON 칸 실수 — 비유한 (자기 후보가 아닌 행의 s · 자기 행의 d0 = NaN) 은 None."""
    x = float(x)
    return x if math.isfinite(x) else None


def junction_census(kw, sid, *, tol_ff, L_par, r_port, tol_P, tol_sj, r_ptfe, r_sdcp):
    """접합 census (판정 · 보고 판) — B3 `carbon_junction.cjunc_registry` 를 **그대로** 부른다 (사본 없음 · 설계 §2 ① · §4-1 끝).
    입력 = 잡은 생산 raster 입력 (전 상 — PTFE 행 포함 = P-junc 덮임 판정 · SDCP 점 = 근접 판정) + `sid` (off 격자) · 계획 문턱 ·
    s_min 미등록 (None — 거르지 않고 자기 후보 전부를 s 와 함께 낸다 = s_min 근거).  솔브 없음 (원장 = 기하만).
    → (보고 블록 · 후보별 배열 dict).  원장이 입력을 거부하면 S0Error (조용한 강등 없음)."""
    try:
        reg = cj.cjunc_registry(sid, tuple(float(x) for x in kw['box_lo']), float(kw['vox']), kw['add_pts'], kw['add_phase'],
                                kw['add_fid'], kw['add_kind'], r_f_um=R_F_UM, tol_ff_um=tol_ff, L_par_um=L_par,
                                r_port_um=r_port, s_min_um=None, gap_tol=float(kw['fid_gap_tol']), tol_P_um=tol_P,
                                tol_sj_um=tol_sj, r_ptfe_um=r_ptfe, r_sdcp_um=r_sdcp)
    except (ValueError, TypeError) as e:
        raise S0Error(f'접합 원장 (carbon_junction.cjunc_registry) 이 입력을 거부했다: {e}') from e
    I = reg['instances']
    n_i = len(I['fi'])
    isself = np.asarray(I['self'], bool)
    Lc = np.asarray(I['Lc'], np.float64)
    mult = np.asarray(I['mult'], np.float64)
    lng = np.asarray(I['long'], bool)
    s = np.asarray(I['s'], np.float64)
    real = np.asarray(I['realized'], bool)
    selfc = [{'fid': int(I['fi'][q]), 's_um': _jf(s[q]), 'Lc_um': _jf(Lc[q]), 'mult': _jf(mult[q]),
              'dk_min': int(I['self_dk_min'][q]), 'long': bool(lng[q]), 'realized': bool(real[q])}
             for q in np.flatnonzero(isself)]
    selfc.sort(key=lambda d: (d['s_um'] is None, d['s_um'] if d['s_um'] is not None else 0.0, d['fid']))
    longc = [{'kind': 'self' if isself[q] else 'distinct', 'fi': int(I['fi'][q]), 'fj': int(I['fj'][q]), 'Lc_um': _jf(Lc[q]),
              'mult': _jf(mult[q]), 'd0_um': _jf(I['d0'][q]), 's_um': _jf(s[q]), 'realized': bool(real[q])}
             for q in np.flatnonzero(lng)]
    longc.sort(key=lambda d: (-(d['Lc_um'] or 0.0), d['fi'], d['fj']))
    #  ★ 10-21 (Codex RCA-03 · 04 · 05 · 1저자 Q11 일부) — census 보탬: 같은 셀 비연속 재방문 · 포트 동률 (간선 단위) · 분산 간선 (긴 접촉) ·
    #    간선별 PTFE 덮임 · 부분 덮임 instance — 전부 원장 census (같은 함수) 그대로 옮긴다 (사본 계산 없음)
    S = reg['subedges']
    cen = reg['census']
    sub_inst = np.asarray(S['inst'], np.int64)
    revisit = {'n_pairs': cen.get('n_revisit_pairs'), 'n_cells': cen.get('n_revisit_cells'),
               'n_fibres': cen.get('n_revisit_fibres'), 's_um': cen.get('revisit_s_um'),
               'n_path_only': cen.get('n_self_revisits_path_only'),
               'rule': reg['rules'].get('branch'), 'meaning': '같은 조각이 같은 셀을 비연속으로 다시 지난 가지 쌍 (가지마다 따로 · 합치지 않음 · '
                                                           'RCA-03 · 고리 이음매 별칭 제외) — s = 그 쌍의 경로 호 간격 (쌍마다 · ★ 10-21)'}
    subedges = {'n': cen.get('n_subedges'), 'n_long': cen.get('n_subedges_long'), 'n_ptfe_cov': cen.get('n_subedges_ptfe_cov'),
                'n_instances_ptfe_partial': cen.get('n_instances_ptfe_partial'), 'n_sdcp_near': cen.get('n_subedges_sdcp_near'),
                'n_unrealized': cen.get('n_subedges_unrealized'), 'rule': reg['rules'].get('dist'),
                'k_per_instance': _dist(np.asarray(I['nsub'], np.float64))}
    block = {
        'status': 'registry',
        'function': 'carbon_junction.cjunc_registry',
        'verdict_use': '판정 · 보고의 instance census 판 (B3 · 길이 법칙 v0 · 설계 §2 ① · §4-1 끝) — 기하만 · 솔브 없음',
        'model': cj.CJUNC_MODEL_VERSION, 'schema': cj.CJUNC_SCHEMA, 'len_law': cj.CJUNC_LEN_LAW,
        'grid': JUNCTION_GRID,
        'grid_definition': 'captured production inputs minus PTFE rows (= ptfe_stamp off · face_alpha sid grid); '
                           'the registry gets every phase (PTFE paths = P-junc cover · SDCP points = proximity)',
        's_min_status': 'not_applied — S0 계획 (cjunc_plan.json) 에 s_min 칸이 없어 원장을 s_min None 으로 부른다 (거르지 않음 · '
                        '자기 후보 전부 + 후보마다 s = s_min 근거 · s_min 숫자 = 등록 R §2-1 · 이 도구는 고르지 않는다)',
        'thresholds': dict(reg['thresholds']), 'rules': dict(reg['rules']),
        'rejection_codes': [x['code'] for x in reg['rejections']],
        'census': reg['census'],
        'n_instances': int(n_i), 'n_long': int(lng.sum()), 'n_long_distinct': int((lng & ~isself).sum()),
        'n_long_self': int((lng & isself).sum()),
        'Lc_um': _dist(Lc), 'Lc_distinct_um': _dist(Lc[~isself]), 'Lc_self_um': _dist(Lc[isself]),
        'len_mult_sum': float(mult.sum()), 'len_mult_sum_realized': float(mult[real].sum()),
        'len_mult_max': (float(mult.max()) if n_i else None), 'n_mult_gt1': int((mult > 1.0).sum()),
        'self_s_um': _dist(s[isself]),
        'port_search_um': _dist(np.asarray(I['port_search_um'], np.float64)[real]),
        'n_ptfe_cov': int(np.sum(I['ptfe_cov'])), 'n_sdcp_near': int(np.sum(I['a_sdcp'])),
        'revisit': revisit, 'n_port_ties': cen.get('n_port_ties'), 'subedges': subedges,
        'self_candidates': selfc,
        'long_contacts': longc,
    }
    arrays = {'fi': np.asarray(I['fi'], np.int64), 'fj': np.asarray(I['fj'], np.int64), 'is_self': isself,
              'd0': np.asarray(I['d0'], np.float64), 'Lc': Lc, 'mult': mult, 'long': lng, 's': s,
              'self_dk_min': np.asarray(I['self_dk_min'], np.int64), 'realized': real,
              'reason': np.asarray([str(x) for x in I['reason']], dtype=str),
              'port_search_um': np.asarray(I['port_search_um'], np.float64), 'cp': np.asarray(I['cp'], np.float64),
              'ptfe_cov': np.asarray(I['ptfe_cov'], bool), 'a_sdcp': np.asarray(I['a_sdcp'], bool),
              'nsub': np.asarray(I['nsub'], np.int64), 'self_n_revisit': np.asarray(I['self_n_revisit'], np.int64),
              'sub_inst': sub_inst, 'sub_ptfe_cov': np.asarray(S['ptfe_cov'], bool),
              'sub_a_sdcp': np.asarray(S['a_sdcp'], bool), 'sub_realized': np.asarray(S['realized'], bool),
              'sub_cp': np.asarray(S['cp'], np.float64), 'sub_tie_i': np.asarray(S['tie_i'], bool),
              'sub_tie_j': np.asarray(S['tie_j'], bool)}
    return block, arrays


# ══ α 분포 — S1 face_alpha 함수 그대로 (raster-only) ══════════════════════════════════════════════════════════════
def alpha_census(kw, sid, pid, true_ptfe_um3):
    """α 분포 (설계 §2 ① 끝 행 · §3-2 출력) — S1 `ptfe_face_alpha` 함수를 **그대로** 부른다 (사본 금지 · 솔브 없음):
    캡슐 (`build_capsules` · 잡은 입력의 PTFE 행 전부 · 지름 법칙 rope) → 채널마다 계획 (`build_plan` · `sid` = off 격자 = face_alpha 의
    sid 격자 · 전자 = pid 로 같은 AM 입자 면제 · K = 봉인값) → 면 부류별 α < 1 · α = 0 수 · Σ(1 − α)h² (`plan_face_summary`) ·
    캡슐 부피 기록 (`volume_record` · 참부피 = mpm_metrics PTFE) · off 격자 PTFE 점 셀 sid 분포 (`ptfe_point_cell_census` — 설계 §3-2
    '"S0 와 같은 함수"').  면 자격 = `ALPHA_SIG_E` · `ALPHA_SIG_I` 의 σ > 0 패턴.  판 결합 면 = α 미적용 (S1 v0 `PLATE_RULE`).
    → 보고 블록.  S1 함수가 입력을 거부하면 S0Error."""
    P = np.asarray(kw['add_pts'], np.float64)
    m4 = np.asarray(kw['add_phase']) == PTFE
    lo = tuple(float(x) for x in kw['box_lo'])
    vox = float(kw['vox'])
    try:
        caps = fa.build_capsules(P[m4], np.asarray(kw['add_fid'])[m4], np.asarray(kw['add_kind'])[m4], dia_law=ALPHA_DIA_LAW)
        pe = fa.build_plan(sid, ALPHA_SIG_E, caps, lo=lo, vox=vox, channel='electronic', pid=pid)
        pi = fa.build_plan(sid, ALPHA_SIG_I, caps, lo=lo, vox=vox, channel='ionic')
    except (ValueError, TypeError) as e:
        raise S0Error(f'α 분포 (ptfe_face_alpha) 가 입력을 거부했다: {e}') from e
    return {
        'status': 'computed',
        'function': 'ptfe_face_alpha.build_capsules · build_plan · plan_face_summary · volume_record · ptfe_point_cell_census',
        'operator': fa.S1_OPERATOR_VERSION, 'K': int(pe['K']), 'dia_law': ALPHA_DIA_LAW, 'grid': JUNCTION_GRID,
        'eligible_sids': {'electronic': [int(i) for i in np.flatnonzero(ALPHA_SIG_E > 0)],
                          'ionic': [int(i) for i in np.flatnonzero(ALPHA_SIG_I > 0)]},
        'eligibility_rule': ('channel cells = sid with positive entries of the production table functions '
                             '(electronic_sigma_table / ionic_sigma_table) at unit values; alpha is face geometry '
                             '(capsule over face quadrature) and does not depend on the magnitudes'),
        'capsules': fa.capsule_summary(caps), 'volume': fa.volume_record(caps['volume_um3'], true_ptfe_um3),
        'faces': {'electronic': fa.plan_face_summary(pe), 'ionic': fa.plan_face_summary(pi)},
        'off_grid_ptfe_point_cells': fa.ptfe_point_cell_census(sid, P[m4], lo, vox),
        'plate_rule': fa.PLATE_RULE,
        'note': 'raster-only (솔브 없음) · S1 판정 런의 payload 는 같은 함수로 런의 σ 표를 써서 ca_ext.ptfe_face 에 싣는다',
    }


# ══ 계획 (등록 R §2-1) ══════════════════════════════════════════════════════════════════════════════════════════
def plan_bytes_of(plan):
    """정준 바이트 — 정렬 키 · ASCII · 공백 없음 · NaN 금지 · 끝 줄바꿈 하나."""
    return (json.dumps(plan, sort_keys=True, ensure_ascii=True, separators=(',', ':'), allow_nan=False)
            + '\n').encode('ascii')


def _num_ok(x):
    """유한 양수 — ★ PF2 E (10-22 · 사전 리뷰 2 회차 PRE2-impl-03) float 로 못 바꾸는 큰 정수 (10**400 · OverflowError) = 아님 (옛 = 잡히지 않은
    예외가 단계 2 관문 밖으로 샜다)."""
    if not isinstance(x, (int, float)) or isinstance(x, bool):
        return False
    try:
        return math.isfinite(float(x)) and float(x) > 0
    except OverflowError:
        return False


def _reject_dup(pairs):
    """★ PF2 E (PRE2-impl-03) — JSON 중복 칸 거부 (사람 = 앞 값 · 해석기 = 뒤 값으로 같은 바이트를 달리 읽지 않게 · 정준 바이트 검사 앞)."""
    out = {}
    for k, v in pairs:
        if k in out:
            raise S0Error(f'JSON 중복 칸 {k!r} — 거부 (같은 바이트를 달리 읽지 않게)')
        out[k] = v
    return out


def check_plan(plan):
    """계획 식 재유도 — 손댄 값 · 비유한 · 다른 스키마 · 다른 식 문구 = 거부 (S0Error)."""
    if not isinstance(plan, dict) or plan.get('schema') != PLAN_SCHEMA:
        raise S0Error(f'계획 스키마가 {PLAN_SCHEMA} 아님')
    if plan.get('formulas') != FORMULAS:
        raise S0Error('계획의 식 문구가 이 도구의 고정 식과 다르다 (식 개정 = 등록 R 개정 · 도구 판 올림)')
    v = plan.get('values_um')
    req = ('u', 'r_f', 'tol_ff', 'L_par', 'r_port', 'tol_P', 'tol_sj')
    if not isinstance(v, dict) or set(v) != set(req) or not all(_num_ok(v[k]) for k in req):
        raise S0Error('계획 values_um 결손 · 비유한 · 0 이하')
    if (v['tol_ff'] != min(v['u'], v['r_f']) or v['tol_P'] != v['tol_ff'] or v['tol_sj'] != v['tol_ff']
            or v['L_par'] != L_PAR_FACTOR * (v['r_f'] + v['r_f']) or v['r_port'] != R_PORT_UM):
        raise S0Error('계획 숫자가 식과 다르다 (tol_ff = min(u, r_f) · tol_P = tol_sj = tol_ff · L_par = 2(r_fi + r_fj) · '
                      'r_port 0.30)')
    if R_F_UM is not None and v['r_f'] != R_F_UM:
        raise S0Error(f"계획 r_f {v['r_f']} ≠ additives.VGCF_D/2 {R_F_UM}")
    if plan.get('integers') != {'K_alpha': K_ALPHA, 'k_sdcp_cells': K_SDCP_CELLS}:
        raise S0Error('계획 정수 (K_alpha 8 · k 2) 가 다르다')
    if plan.get('gap_tol') != GAP_TOL_PRODUCTION:
        raise S0Error(f"계획 gap_tol {plan.get('gap_tol')!r} ≠ 생산 rasterize 기본 {GAP_TOL_PRODUCTION}")
    return None


def make_plan(u_um, r_f_um, gap_tol, source):
    """단계 1 — 식으로 숫자를 낸다 (고르지 않는다).  → (계획, 정준 바이트, sha256)."""
    u, rf = float(u_um), float(r_f_um)
    if not (math.isfinite(u) and u > 0 and math.isfinite(rf) and rf > 0):
        raise S0Error(f'u · r_f 가 유한 양수가 아니다 ({u_um!r}, {r_f_um!r})')
    tol = min(u, rf)
    plan = {'schema': PLAN_SCHEMA, 'formulas': dict(FORMULAS),
            'values_um': {'u': u, 'r_f': rf, 'tol_ff': tol, 'L_par': L_PAR_FACTOR * (rf + rf), 'r_port': R_PORT_UM,
                          'tol_P': tol, 'tol_sj': tol},
            'integers': {'K_alpha': K_ALPHA, 'k_sdcp_cells': K_SDCP_CELLS}, 'gap_tol': float(gap_tol),
            'source': source}
    check_plan(plan)
    b = plan_bytes_of(plan)
    return plan, b, hashlib.sha256(b).hexdigest()


_SHA_RE = re.compile(r'[0-9a-f]{7,40}\Z')


def _git(repo, *args, text=True):
    return subprocess.run(['git', '-C', repo, *args], capture_output=True, text=text, timeout=120)


def _row_value(text, label):
    """등록 문서의 `| <label> |` 줄 (정확히 하나) 의 끝 칸 (백틱 · 공백 뺌) — 없거나 둘 이상 = S0Error."""
    rows = [ln for ln in text.splitlines() if ln.startswith(f'| {label} |')]
    if len(rows) != 1:
        raise S0Error(f'등록 R 문서의 "| {label} |" 줄이 {len(rows)} 개 (1 이어야)')
    cells = [c.strip() for c in rows[0].strip().strip('|').split('|')]
    return cells[-1].strip('` ')


def verify_plan_commit(repo, sha, plan_path, r_doc=R_DOC_DEFAULT, *, r_plan_path=None):
    """단계 2 관문 — 개정 커밋이 HEAD 의 조상 · 그 커밋 등록 R 문서의 `| S0 계획 해시 |` 줄 끝 칸 = 계획 파일 sha256 · 식 재유도 · 정준.
    ★ 10-21 (사전 리뷰 PRE-design-04 · 등록 R §2-1 · §2-1b · §11 ④) — 같은 커밋의 `| 계획 해시 |` 줄 (R 런 사슬 계획 · 사슬과 같은 함수
    `rint_r_chain.registration_plan_hash` · ⬜ = s_min 미등록 = 거부) = r_plan_path 파일 sha256 · 그 꼴 (`rint_r_chain.load_plan`) · 두 계획
    대조 (tol_ff_um = S0 values_um.tol_ff · len_law = 원장의 길이 법칙).  옛 관문 = S0 해시가 문서 어디에든 있으면 통과 · R 런 계획 · s_min 은
    보지 않았다 (DBE 를 s_min 봉인 전에 열 수 있었다).
    → (계획, sha256, 전체 sha, R 런 계획 결합 기록).  커밋 순서만으로는 시점 증명이 안 된다 (v3 판정) → 해시로 묶는다."""
    if not isinstance(sha, str) or not _SHA_RE.match(sha):
        raise S0Error('--threshold-commit 은 ASCII 16진 7–40 자 (전각 · 공백 · 다른 문자 거부)')
    if r_plan_path is None:
        raise S0Error('단계 2 관문 — --r-plan-path (같은 개정 커밋의 R 런 사슬 계획 · s_min 봉인) 가 없다 (★ 10-21 PRE-design-04)')
    for p in (plan_path, r_doc, r_plan_path):
        if (not isinstance(p, str) or not p or os.path.isabs(p) or '..' in p.split('/') or not p.isascii()
                or re.search(r'\s', p)):
            raise S0Error(f'리포 상대 ASCII 경로여야 한다: {p!r}')
    r = _git(repo, 'rev-parse', '--verify', '--quiet', sha + '^{commit}')
    if r.returncode != 0 or not r.stdout.strip():
        raise S0Error(f'커밋 {sha} 이 저장소 {repo} 에 없다 (git fetch 뒤 다시)')
    full = r.stdout.strip()
    r = _git(repo, 'merge-base', '--is-ancestor', full, 'HEAD')
    if r.returncode != 0:
        raise S0Error(f'커밋 {full[:12]} 이 이 작업 트리 HEAD 의 조상이 아니다 (가지 밖 · 또는 HEAD 가 개정 전)')
    r = _git(repo, 'show', f'{full}:{plan_path}', text=False)
    if r.returncode != 0:
        raise S0Error(f'커밋 {full[:12]} 에 계획 파일 {plan_path} 이 없다')
    pb = r.stdout
    h = hashlib.sha256(pb).hexdigest()
    r = _git(repo, 'show', f'{full}:{r_doc}', text=False)
    if r.returncode != 0:
        raise S0Error(f'커밋 {full[:12]} 에 등록 R 문서 {r_doc} 가 없다')
    doc_raw = r.stdout
    try:
        doc = doc_raw.decode('utf-8')
    except UnicodeDecodeError:
        raise S0Error(f'등록 R 문서 ({r_doc} @ {full[:12]}) 가 UTF-8 이 아니다') from None
    if _row_value(doc, 'S0 계획 해시') != h:
        raise S0Error(f'등록 R 문서 ({r_doc} @ {full[:12]}) 의 "| S0 계획 해시 |" 끝 칸 ≠ 계획 sha256 {h[:16]}… — §2-1 개정 커밋이 아니다 '
                      f'(★ 10-21 — 줄 밖 · 다른 칸에 적힌 해시는 세지 않는다)')
    try:
        plan = json.loads(pb.decode('ascii'), object_pairs_hook=_reject_dup)   # ★ PF2 E — 중복 칸 거부 (정준 바이트 검사 앞)
    except S0Error:
        raise
    except Exception as e:                                  # noqa: BLE001
        raise S0Error(f'계획 파일이 ASCII JSON 이 아니다 ({type(e).__name__})')
    check_plan(plan)
    if plan_bytes_of(plan) != pb:
        raise S0Error('계획 파일이 정준 바이트가 아니다 (손으로 고친 형식) — 단계 1 산출물 그대로 커밋할 것')
    #  ★ 10-21 (PRE-design-04) — R 런 사슬 계획 (같은 커밋 · s_min 봉인) — 사슬과 같은 함수 (사본 없음)
    import rint_r_chain as _rrc
    with tempfile.TemporaryDirectory(prefix='s0_r_') as td:
        dp = os.path.join(td, 'R.md')
        with open(dp, 'wb') as f:
            f.write(doc_raw)
        try:
            r_hash, _doc_sha = _rrc.registration_plan_hash(dp)
        except _rrc.Stop as e:
            raise S0Error(f'등록 R 문서 ({r_doc} @ {full[:12]}) 의 R 런 계획 줄 — {e.code}: {e.cause} (s_min 봉인 전 DBE 단계 2 금지)') from None
        r = _git(repo, 'show', f'{full}:{r_plan_path}', text=False)
        if r.returncode != 0:
            raise S0Error(f'커밋 {full[:12]} 에 R 런 계획 파일 {r_plan_path} 이 없다')
        rpb = r.stdout
        if hashlib.sha256(rpb).hexdigest() != r_hash:
            raise S0Error(f'R 런 계획 파일 {r_plan_path} sha256 {hashlib.sha256(rpb).hexdigest()[:16]}… ≠ 등록 "| 계획 해시 |" '
                          f'{r_hash[:16]}… (같은 커밋)')
        rp = os.path.join(td, 'r_plan.json')
        with open(rp, 'wb') as f:
            f.write(rpb)
        try:
            robj, _rsha = _rrc.load_plan(rp)
            #  ★ 4판 (10-21 · 1저자 Q-G 비준 · 등록 R 4판 §11 ④) — 결과 전 등록 숫자 넷 (점 수 상한 · 역상 폭 상한 · SV 반사실 문턱 · 범위) =
            #    Codex 회신 뒤 · 단계 2 (DBE) 열람 전 → 인자 커밋의 R 런 계획에 null (⬜) 이 있으면 단계 2 를 열지 않는다 (사슬과 같은 함수 ·
            #    옛 관문 = load_plan 꼴 검사만 · null 을 받았다)
            _rrc.require_plan_numbers(robj)
        except _rrc.Stop as e:
            raise S0Error(f'R 런 계획 파일 {r_plan_path} — {e.code}: {e.cause}') from None
    if robj['tol_ff_um'] != plan['values_um']['tol_ff']:
        raise S0Error(f"두 계획 대조 — R 런 계획 tol_ff_um {robj['tol_ff_um']!r} ≠ S0 계획 values_um.tol_ff {plan['values_um']['tol_ff']!r} "
                      f'(같은 float · 등록 R §2-1)')
    if robj['len_law'] != cj.CJUNC_LEN_LAW:
        raise S0Error(f"두 계획 대조 — R 런 계획 len_law {robj['len_law']!r} ≠ 원장의 길이 법칙 {cj.CJUNC_LEN_LAW!r}")
    rinfo = {'path': r_plan_path, 'sha256': r_hash, 's_min_um': float(robj['s_min_um']), 'tol_ff_um': float(robj['tol_ff_um']),
             'len_law': robj['len_law'], 'unreg_law': robj['unreg_law'], 'step3_rtol': float(robj['step3_rtol']),
             'checked': 'S0 row exact · R row (registration_plan_hash) · R plan sha256 · load_plan · tol_ff = S0 tol_ff · len_law'}
    return plan, h, full, rinfo


# ══ 킷 · payload 가로채기 ═════════════════════════════════════════════════════════════════════════════════════════
def find_run_dir(kit):
    """러너와 같은 규칙 — `latest_run` 이 있으면 그것 · 없으면 se_dump.npy 가 든 마지막 `run_*`."""
    kit = os.path.abspath(kit)
    lr = os.path.join(kit, 'latest_run')
    if os.path.lexists(lr):
        run = os.path.realpath(lr)
    else:
        cands = [d for d in sorted(glob.glob(os.path.join(kit, 'run_*'))) if os.path.isfile(os.path.join(d, 'se_dump.npy'))]
        if not cands:
            raise S0Error(f'{kit}: 압밀 런 없음 (latest_run · run_*/se_dump.npy)')
        run = os.path.realpath(cands[-1])
    if not os.path.isfile(os.path.join(run, 'se_dump.npy')):
        raise S0Error(f'{run}: se_dump.npy 없음')
    return run


_SHELL_BAD = re.compile(r'[\s\'"$`\\;&|<>()*?!#~{}\[\]]')


def resolve_payload_argv(kit, run_dir, out_dir, *, vox, bridge_um, sdcp_sphere_d, scripts_dir=SCRIPTS):
    """킷 run_mpm.sh 의 payload 호출 → 실제 argv (러너와 같은 추출 함수 + bash 가 변수 · 따옴표를 푼다).
    raster 플래그 (vox · 브리지 · SDCP 구 · PTFE centerline · 선분 스탬프 · origin 0) 를 덧붙이고, 출력은 전부 out_dir 로."""
    import sr01_stamp_compare as sc
    kit = os.path.abspath(kit)
    for p in (out_dir, kit, scripts_dir):
        if _SHELL_BAD.search(p):
            raise S0Error(f'경로에 공백 · 셸 문자가 있다 (bash 로 argv 를 풀 수 없다): {p!r}')
    for nm, v in (('vox', vox), ('bridge_um', bridge_um), ('sdcp_sphere_d', sdcp_sphere_d)):
        if not _num_ok(v):
            raise S0Error(f'{nm} 은 유한 양수 ({v!r})')
    rp = os.path.join(kit, 'run_mpm.sh')
    if not os.path.isfile(rp):
        raise S0Error(f'{rp} 없음')
    kname = os.path.basename(kit)
    outj = os.path.join(out_dir, f'_payload_never_{kname}.json')
    rlo = os.path.join(out_dir, f'_payload_rasterize_only_{kname}.json')
    extra = (f'--step3-vox {float(vox)!r} --step3-bridge-um {float(bridge_um)!r} --step3-origin-shift 0 0 0 '
             f'--step3-sdcp-sphere-d {float(sdcp_sphere_d)!r} --ptfe-stamp centerline '
             '--no-ion --no-field --no-pore --no-thermal --no-trackb --no-collector --no-step4 '
             f'--step3-rasterize-only {rlo}')
    try:
        with open(rp, encoding='utf-8') as f:
            body = sc.extract_payload_cmd(f.read(), outj, 'segment', extra_flags=extra, tag='s0')
    except SystemExit as e:
        raise S0Error(f'run_mpm.sh payload 호출 추출 실패: {e}')
    with tempfile.TemporaryDirectory(dir=out_dir) as td:
        af = os.path.join(td, 'argv.bin')
        script = ('set -u\n' f'KIT={shlex.quote(kit)}\n' f'SCR={shlex.quote(scripts_dir)}\n' 'PSIG=()\n'
                  f'python3() {{ printf "%s\\0" "$@" > {shlex.quote(af)}; }}\n' + body)
        r = subprocess.run(['bash', '-c', script], cwd=run_dir, capture_output=True, text=True, timeout=60)
        if r.returncode != 0 or not os.path.isfile(af):
            raise S0Error(f'payload argv 풀기 실패 (bash rc {r.returncode}): {(r.stderr or "")[-300:]}')
        with open(af, 'rb') as f:
            raw = f.read()
    parts = raw.split(b'\0')
    if parts[-1] != b'':
        raise S0Error('payload argv 기록이 잘렸다')
    argv = [p.decode('utf-8') for p in parts[:-1]]
    if not argv or not argv[0].endswith('mpm_webapp_payload.py'):
        raise S0Error(f'payload 호출이 아니다: {argv[:1]}')
    argv = argv[1:]
    for k in range(len(argv) - 1):
        if argv[k] == '--save-step4-grid':
            argv[k + 1] = os.path.join(out_dir, f'_payload_step4_{kname}.npz')
    return argv


def _argv_opt(argv, flag):
    v = None
    for k, tok in enumerate(argv):
        if tok == flag and k + 1 < len(argv):
            v = argv[k + 1]
        elif tok.startswith(flag + '='):
            v = tok.split('=', 1)[1]
    return v


def kit_input_paths(run_dir, argv):
    """★ 10-25 묶음 B (RCA2-03 · 1저자 10-23 Q3 (가)) — payload argv → 원 입력 역할별 경로 {역할: 경로} (`KIT_ROLES` + 호출에 있으면
    fibre_dia) · 파일이 없으면 거부.  `validate_kit_arrays` (S0 보고) 와 `kit_input_record` (사슬이 R 직전 · 판정 때 다시 해시) 가 이 함수 하나를
    부른다 (사본 없음 · 옛 = validate_kit_arrays 안 path_of)."""
    def path_of(flag, required=True):
        v = _argv_opt(argv, flag)
        if v is None:
            if required:
                raise S0Error(f'payload 호출에 {flag} 가 없다 — S0 는 그 입력이 필요하다')
            return None
        return v if os.path.isabs(v) else os.path.join(run_dir, v)
    p_se, p_ph, p_fi = path_of('--se'), path_of('--phase'), path_of('--fibre')
    p_dia, p_met, p_sc = path_of('--fibre-dia', False), path_of('--metrics-json'), path_of('--scaffold')
    p_kind = (p_fi[:-4] if p_fi.endswith('.npy') else p_fi) + '_kind.npy'
    files = {'se': p_se, 'phase': p_ph, 'fibre': p_fi, 'fibre_kind': p_kind, 'metrics_json': p_met, 'scaffold': p_sc}
    if p_dia:
        files['fibre_dia'] = p_dia
    for k, p in files.items():
        if not os.path.isfile(p):
            raise S0Error(f'{k} 파일 없음: {p}' + (' — fibre_kind 없이는 경로 · 그룹을 phase 로 추측해야 한다 (S0 = 거부)'
                                                  if k == 'fibre_kind' else ''))
    return files


def kit_files_record(files):
    """원 입력 경로 {역할: 경로} → {역할: {path, sha256, bytes}} (S0 보고 inputs.files · `kit_input_record` 같은 함수 · 경로는 기록만 —
    사슬은 sha256 · bytes 만 대조한다)."""
    return {k: {'path': p, 'sha256': _sha256_file(p), 'bytes': int(os.path.getsize(p))} for k, p in files.items()}


#: 설정 지문의 고정 인자 — `sr01_stamp_compare.extract_payload_cmd` (러너 · S0 의 payload 호출 추출 함수) 를 이 인자로 불러 킷마다
#  같은 꼴의 호출부 문자열을 만든다 (출력 · 스탬프 · 덧붙임 플래그 = 상수 · 그 밖은 킷 run_mpm.sh 의 payload 호출부 그대로)
SETTINGS_EXTRACT = {'out_name': 's0_settings.json', 'stamp': 'segment', 'extra_flags': '', 'tag': 's0settings'}


def kit_settings_sha256(kit):
    """★ 10-25 묶음 B (RCA2-03) — 킷 설정 지문 = 킷 run_mpm.sh 의 payload 호출부 (러너 · S0 가 쓰는 추출 함수 `extract_payload_cmd` ·
    고정 인자 `SETTINGS_EXTRACT`) 의 utf-8 sha256 (호출부 밖 줄 = 대조 밖 · --n-vox 같은 호출 인자 = 대조 안)."""
    import sr01_stamp_compare as sc
    rp = os.path.join(os.path.abspath(kit), 'run_mpm.sh')
    try:
        with open(rp, encoding='utf-8') as f:
            body = sc.extract_payload_cmd(f.read(), SETTINGS_EXTRACT['out_name'], SETTINGS_EXTRACT['stamp'],
                                          extra_flags=SETTINGS_EXTRACT['extra_flags'], tag=SETTINGS_EXTRACT['tag'])
    except SystemExit as e:
        raise S0Error(f'run_mpm.sh payload 호출 추출 실패 (설정 지문): {e}')
    except (OSError, UnicodeDecodeError) as e:
        raise S0Error(f'{rp}: {type(e).__name__}: {e}')
    return hashlib.sha256(body.encode('utf-8')).hexdigest()


def kit_input_record(kit, *, vox=0.15, bridge_um=0.48, sdcp_sphere_d=0.30, scripts_dir=SCRIPTS):
    """★ 10-25 묶음 B (RCA2-03 · 1저자 10-23 Q3 (가)) — 킷 → 원 입력 기록 {files (역할별 path · sha256 · bytes) · metrics (um_box_um ·
    thickness_um) · settings_sha256} — census_kit 과 같은 발견 함수 (find_run_dir · resolve_payload_argv · kit_input_paths ·
    kit_files_record · kit_settings_sha256 · 사본 없음).  사슬이 R 직전 · 판정 때 기계마다 자기 킷 사본에 이 함수를 불러 S0 보고 기록과
    대조한다 (경로 = 대조 밖).  읽지 못하면 S0Error (확인 못 함 = 거부).  metrics 값 = 유한 양수면 float · 아니면 None (값 검사는 S0
    보고 쪽 `validate_kit_arrays` · 이 함수는 기록 대조용 — metrics 파일 자체는 sha256 으로 대조된다)."""
    kit = os.path.abspath(kit)
    run_dir = find_run_dir(kit)
    with tempfile.TemporaryDirectory() as td:
        argv = resolve_payload_argv(kit, run_dir, td, vox=vox, bridge_um=bridge_um, sdcp_sphere_d=sdcp_sphere_d,
                                    scripts_dir=scripts_dir)
    files = kit_input_paths(run_dir, argv)
    try:
        with open(files['metrics_json'], encoding='utf-8') as fj:
            met = json.load(fj)
    except (OSError, UnicodeDecodeError, ValueError) as e:
        raise S0Error(f'{files["metrics_json"]}: {type(e).__name__}: {e}')
    met = met if isinstance(met, dict) else {}
    return {'files': kit_files_record(files),
            'metrics': {k: (float(met.get(k)) if _num_ok(met.get(k)) else None) for k in ('um_box_um', 'thickness_um')},
            'settings_sha256': kit_settings_sha256(kit)}


def validate_kit_arrays(run_dir, argv, *, stage):
    """S0-5 — 가로채기 **전에** 입력 계약: 길이 정확 일치 · float64 유한 · kind 파일 · 경로 fid 한 블록 · 상 하나 · 중복 경로 없음 ·
    VGCF Ø 균일 · metrics 척도 · 단계 1 = SDCP 없음.  → 입력 기록 (sha256 · 점 수 · metrics).  ★ 10-25 묶음 B — 경로 · 파일 기록 =
    `kit_input_paths` · `kit_files_record` (사슬의 다시 해시 `kit_input_record` 와 같은 함수)."""
    files = kit_input_paths(run_dir, argv)
    p_se, p_ph, p_fi, p_met = files['se'], files['phase'], files['fibre'], files['metrics_json']
    p_kind, p_dia = files['fibre_kind'], files.get('fibre_dia')
    se = np.load(p_se, mmap_mode='r')
    if se.ndim != 2 or se.shape[1] != 3 or not np.issubdtype(se.dtype, np.floating):
        raise S0Error(f'se_dump 모양 · 형이 (N,3) 실수가 아니다: {se.shape} {se.dtype}')
    N = int(se.shape[0])
    for c0 in range(0, N, 4_000_000):
        if not np.isfinite(np.asarray(se[c0:c0 + 4_000_000], np.float64)).all():
            raise S0Error('se_dump 에 NaN · ±inf 좌표')
    PH = np.load(p_ph); FI = np.load(p_fi); KI = np.load(p_kind)
    for nm, a in (('phase', PH), ('fibre', FI), ('fibre_kind', KI)):
        if a.shape != (N,):
            raise S0Error(f'{nm} 길이 {a.shape} ≠ 점 수 ({N},) — 조용히 강등하지 않는다 (RIMPR-01 부류)')
        if not np.issubdtype(a.dtype, np.integer):
            raise S0Error(f'{nm} 가 정수 배열이 아니다 ({a.dtype})')
    if not set(np.unique(PH).tolist()) <= {1, 2, 3, 4, 5, 6}:
        raise S0Error(f'phase 값이 1..6 밖: {sorted(set(np.unique(PH).tolist()))}')
    if not set(np.unique(KI).tolist()) <= {0, 1}:
        raise S0Error(f'fibre_kind 값이 0/1 밖: {sorted(set(np.unique(KI).tolist()))}')
    pm = np.isin(PH, PATH_PHASES)
    if ((FI[pm] < 0) | (KI[pm] != 1)).any():
        raise S0Error('VGCF · PTFE 점이 경로 (kind 1 · fid ≥ 0) 가 아니다 — 연속 중심선 없는 침대 = 거부 (설계 K5)')
    dia_rec = None
    if p_dia:
        DI = np.load(p_dia)
        if DI.shape != (N,) or not np.isfinite(DI.astype(np.float64)).all():
            raise S0Error('fibre_dia 길이 ≠ 점 수 또는 비유한')
        dv = DI[PH == VGCF].astype(np.float64)
        if len(dv) and dv.min() != dv.max():
            raise S0Error(f'VGCF 상대 Ø 가 균일하지 않다 ({dv.min()} … {dv.max()}) — r_f 공통 가정이 깨진다')
        dia_rec = float(dv[0]) if len(dv) else None
    idx = np.nonzero((KI == 1) & (FI >= 0))[0]
    blocks = []
    if len(idx):
        f = FI[idx]
        brk = np.nonzero((np.diff(f) != 0) | (np.diff(idx) != 1))[0] + 1
        st = np.r_[0, brk]; en = np.r_[brk, len(idx)]
        blocks = [(int(f[a]), int(idx[a]), int(idx[b - 1]) + 1) for a, b in zip(st, en)]
        bf = [b[0] for b in blocks]
        if len(set(bf)) != len(bf):
            raise S0Error('같은 경로 fid 가 떨어진 두 블록 — 점 순서가 경로 순서라는 전제가 깨진다 (거부)')
        if any(len(np.unique(PH[a:b])) != 1 for _, a, b in blocks):
            raise S0Error('한 경로 fid 에 상이 둘 이상')
        seen = {}
        for fid, a, b in blocks:
            hh = hashlib.sha256(np.ascontiguousarray(np.asarray(se[a:b], np.float64)).tobytes()).hexdigest()
            if hh in seen:
                raise S0Error(f'정확 중복 경로 (fid {seen[hh]} · {fid}) — 거부')
            seen[hh] = fid
    n5 = int((PH == SDCP).sum())
    if stage == 1 and n5:
        raise S0Error(f'단계 1 = SBE 침대만 — SDCP 점 {n5} 개 (DBE 분포는 §2-1 개정 커밋 뒤 단계 2 에서만 연다 · N17)')
    with open(p_met, encoding='utf-8') as fj:
        met = json.load(fj)
    umb, th = met.get('um_box_um'), met.get('thickness_um')
    if not (_num_ok(umb) and _num_ok(th)):
        raise S0Error(f'mpm_metrics.json 의 um_box_um · thickness_um 이 유한 양수가 아니다 ({umb!r}, {th!r})')
    adds = met.get('additives') or {}
    vols = {}
    for ph in sorted(set(np.unique(PH).tolist()) - {1}):
        nm = PHASE_ADDITIVE[ph]
        v = (adds.get(nm) or {}).get('vol_um3')
        if not _num_ok(v):
            raise S0Error(f'mpm_metrics.additives.{nm}.vol_um3 이 유한 양수가 아니다 ({v!r})')
        vols[nm] = float(v)
    counts = {'points_by_phase': _hist(PH), 'fids_by_phase': {}}
    for ph in PATH_PHASES:
        counts['fids_by_phase'][str(ph)] = int(sum(1 for _, a, _b in blocks if int(PH[a]) == ph))
    files_rec = kit_files_record(files)
    return {'files': files_rec, 'counts': counts, 'n_points': N, 'n_sdcp_points': n5, 'vgcf_rel_dia': dia_rec,
            'metrics': {'um_box_um': float(umb), 'thickness_um': float(th), 'E_anchor': met.get('E_anchor'),
                        'porosity_settled_pct': met.get('porosity_settled_pct'),
                        'porosity_at_target_pct': met.get('porosity_at_target_pct'), 'vol_um3': vols}}


def _s3_state():
    st = {k: getattr(s3, k, None) for k in _STATE_KEYS}
    st['_LAST_SEGSTAMP'] = dict(getattr(s3, 'LAST_SEGSTAMP', {}))
    return st


def _s3_restore(st):
    for k in _STATE_KEYS:
        setattr(s3, k, st[k])
    seg = getattr(s3, 'LAST_SEGSTAMP', None)
    if isinstance(seg, dict):
        seg.clear(); seg.update(st['_LAST_SEGSTAMP'])


def capture_raster_inputs(argv, run_dir, *, log_path=None, scripts_dir=SCRIPTS):
    """payload main() 을 이 프로세스에서 돌리며 step3_sigma.rasterize 첫 호출의 인자를 잡고 멈춘다 (솔브 0 · 쓰기 0).
    → rasterize 키워드 인자 dict (기본값 채움)."""
    orig = s3.rasterize
    sig = inspect.signature(orig)
    box = {}

    def hook(*a, **k):
        b = sig.bind(*a, **k)
        b.apply_defaults()
        box['kw'] = dict(b.arguments)
        raise _RasterCaptured()
    spec = importlib.util.spec_from_file_location(f'_s0_payload_{uuid.uuid4().hex}',
                                                  os.path.join(scripts_dir, 'mpm_webapp_payload.py'))
    pay = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pay)
    st = _s3_state()
    old_argv, old_cwd = sys.argv, os.getcwd()
    logf = open(log_path, 'w', encoding='utf-8') if log_path else None
    try:
        s3.rasterize = hook
        os.chdir(run_dir)
        sys.argv = ['mpm_webapp_payload.py'] + list(argv)
        cm_o = contextlib.redirect_stdout(logf) if logf else contextlib.nullcontext()
        cm_e = contextlib.redirect_stderr(logf) if logf else contextlib.nullcontext()
        with cm_o, cm_e:
            try:
                pay.main()
            except _RasterCaptured:
                pass
            except SystemExit as e:
                raise S0Error(f'payload 가 rasterize 전에 끝났다 (SystemExit {e.code}) — 로그 {log_path}')
            except Exception as e:                          # noqa: BLE001  (fail-closed — 어떤 예외든 거부)
                raise S0Error(f'payload 가 rasterize 전에 예외로 끝났다 ({type(e).__name__}: {e}) — 로그 {log_path}') from e
    finally:
        _s3_restore(st)
        sys.argv = old_argv
        os.chdir(old_cwd)
        if logf:
            logf.close()
    if 'kw' not in box:
        raise S0Error('payload 가 rasterize 를 부르지 않았다 (가로채기 안 걸림 · --no-step3 · AM 없음 등) — 생산 격자를 잡지 못함')
    return box['kw']


def _check_captured(kw, vox, bridge_um, sdcp_d):
    bad = []
    if float(kw['vox']) != float(vox):
        bad.append(f"vox {kw['vox']} ≠ {vox}")
    if kw.get('bridge_um') is None or float(kw['bridge_um']) != float(bridge_um):
        bad.append(f"bridge_um {kw.get('bridge_um')} ≠ {bridge_um}")
    if float(kw.get('sdcp_sphere_d_um') or 0.0) != float(sdcp_d):
        bad.append(f"sdcp_sphere_d {kw.get('sdcp_sphere_d_um')} ≠ {sdcp_d}")
    for nm, want in (('ptfe_block_um', 0.0), ('sdcp_bridge_um', 0.0)):
        if float(kw.get(nm) or 0.0) != want:
            bad.append(f'{nm} {kw.get(nm)} ≠ {want} (생산 규약 밖)')
    if kw.get('sdcp_yield_to_vgcf'):
        bad.append('sdcp_yield_to_vgcf 켜짐 (생산 규약 밖)')
    if kw.get('add_pts') is None or kw.get('add_fid') is None or kw.get('add_kind') is None:
        bad.append('첨가제 점 · fid · kind 가 rasterize 에 안 갔다 (선분 스탬프 아님 · kind 폴백)')
    if np.any(np.asarray(kw['box_lo'], np.float64) != 0.0):
        bad.append(f"box_lo {kw['box_lo']} ≠ 0 (origin 이동 없음이어야)")
    if bad:
        raise S0Error('잡은 rasterize 인자가 요청 규약과 다르다: ' + ' · '.join(bad))
    for nm in ('am_c', 'am_r', 'add_pts', 'box_hi'):
        a = np.asarray(kw[nm], np.float64)
        if not np.isfinite(a).all():
            raise S0Error(f'잡은 {nm} 에 비유한 값 (파생값 · RIMPR-04 부류)')
    se = kw.get('se_pts')
    if se is not None:
        for c0 in range(0, len(se), 4_000_000):
            if not np.isfinite(np.asarray(se[c0:c0 + 4_000_000], np.float64)).all():
                raise S0Error('잡은 se_pts 에 비유한 값')


def _raster(kw, drop=(), with_pid=False):
    k = dict(kw)
    if drop:
        keep = ~np.isin(np.asarray(k['add_phase']), drop)
        for nm in ('add_pts', 'add_phase', 'add_fid', 'add_kind'):
            if k.get(nm) is not None:
                k[nm] = np.asarray(k[nm])[keep]
    sid, pid = s3.rasterize(**k)
    if with_pid:
        return sid, pid
    del pid
    return sid


def _cells_from_pieces(pieces, lo, vox, n):
    out = []
    for R in pieces:
        if len(R) == 1:
            out.append(np.floor((R - lo) / vox).astype(int))
        else:
            out.append(np.vstack([segment_cells(R[q] - lo, R[q + 1] - lo, vox) for q in range(len(R) - 1)]))
    ijk = np.vstack(out).astype(int) if out else np.zeros((0, 3), int)
    ok = ((ijk >= 0) & (ijk < n)).all(1)
    return ijk[ok]


def _path_table(kw, shape):
    """잡은 첨가제 입력 → 경로 상 (VGCF · PTFE) 섬유마다 {'phase', 'pieces', 'seq' (생산 셀 · 연속 중복 제거)}.
    조각 (이 파일의 규칙) 으로 다시 만든 셀 == 생산 `_fibre_segment_ijk` 셀 (같은 섬유 · 같은 순서) 이 아니면 거부."""
    P = np.asarray(kw['add_pts'], np.float64); PH = np.asarray(kw['add_phase']); F = np.asarray(kw['add_fid'])
    K = np.asarray(kw['add_kind'])
    lo = np.asarray(kw['box_lo'], np.float64); vox = float(kw['vox']); gt = float(kw['fid_gap_tol'])
    n = np.asarray(shape)
    tab = {}
    for ph in PATH_PHASES:
        idx = np.nonzero((PH == ph) & (F >= 0))[0]
        if not len(idx):
            continue
        f = F[idx]
        brk = np.nonzero((np.diff(f) != 0) | (np.diff(idx) != 1))[0] + 1
        for a, b in zip(np.r_[0, brk], np.r_[brk, len(idx)]):
            i0, i1 = int(idx[a]), int(idx[b - 1]) + 1
            fid = int(f[a])
            if fid in tab:
                raise S0Error(f'잡은 입력에서 fid {fid} 가 떨어진 두 블록')
            prod, _ph = s3._fibre_segment_ijk(P[i0:i1], PH[i0:i1], F[i0:i1], lo, vox, n, gt, add_kind=K[i0:i1])
            pcs = pieces_of(P[i0:i1], gt)
            if not np.array_equal(_cells_from_pieces(pcs, lo, vox, n), prod):
                raise S0Error(f'fid {fid}: 조각 규칙 사본이 생산 _fibre_segment_ijk 셀과 다르다 — 거부 (사본 표류)')
            keep = np.ones(len(prod), bool)
            if len(prod) > 1:
                keep[1:] = (prod[1:] != prod[:-1]).any(1)
            tab[fid] = {'phase': ph, 'pieces': pcs, 'seq': prod[keep]}
    return tab


def _code_info():
    #  ★ PF2 D (10-22 · 사전 리뷰 2 회차 PRE2-design-08 · 등록 R §2-1b ⚠) — census · registry 일곱 파일 (옛 다섯 + carbon_junction.py ·
    #    ptfe_face_alpha.py) · R 런 사슬 (`rint_r_chain.S0_SAME_FILES`) 이 이 지문을 지금 코드와 대조한다
    names = ('ca_s0_census.py', 'step3_sigma.py', 'mpm_webapp_payload.py', 'fibre_segment_raster.py',
             'sr01_stamp_compare.py', 'carbon_junction.py', 'ptfe_face_alpha.py')
    files = {nm: _sha256_file(os.path.join(SCRIPTS, nm)) for nm in names}
    head = dirty = None
    try:
        r = _git(ROOT, 'rev-parse', 'HEAD')
        head = r.stdout.strip() if r.returncode == 0 else None
        r = _git(ROOT, 'status', '--porcelain', '--untracked-files=no')
        dirty = bool(r.stdout.strip()) if r.returncode == 0 else None
    except Exception:                                       # noqa: BLE001
        pass
    import scipy
    #  파일 지문은 {file, sha256} 목록 — 파일 이름 (step3_sigma.py) 을 키로 두면 S0-2 키 검사가 σ 칸으로 잡는다 (키 검사는 엄격히 둔다)
    return {'tool': TOOL_VERSION, 'tool_sha256': files['ca_s0_census.py'],
            'file_digests': [{'file': nm, 'sha256': files[nm]} for nm in names], 'git_head': head,
            'git_dirty': dirty, 'python': platform.python_version(), 'numpy': np.__version__, 'scipy': scipy.__version__}


def _snap(d):
    out = {}
    for base, _dirs, fs in os.walk(d):
        for nm in sorted(fs):
            p = os.path.join(base, nm)
            st = os.lstat(p)
            out[os.path.relpath(p, d)] = (st.st_size, st.st_mtime_ns)
    return out


def sv_census_sealed(kw, sid, *, s_min_um, tol_ff_um):
    """★ 10-25 묶음 B (X6 · 1저자 10-23 Q20 (가)) 단계 2 (s_min 봉인 뒤 · DBE) 봉인 SV census — 가로챈 입력 + off 격자 (`sid`) + R 계획의
    봉인 s_min · tol_ff → 블록.  원장 = `carbon_junction.cjunc_registry` (안의 `_sv_split` · 사본 없음) · 문턱 = `ca_ext_cjunc.registry_thresholds`
    (payload 가 R 런 원장에 넘기는 값과 같은 함수) → census 세 칸 (`ca_ext_svcf.CENSUS_KEYS`).  사슬 (`rint_r_chain.sv_census_problem`) 이 같은
    규약 DBE arm 0 의 SV 기록마다 (기록 census 사본 · 증거 census) 이 값과 대조한다.  지문 (sid · registry) = 기록만 (지금 대조 안 함)."""
    import ca_ext_cjunc as CX
    import ca_ext_svcf as SVCF
    th = CX.registry_thresholds(s_min_um=s_min_um, tol_ff_um=tol_ff_um)
    try:
        reg = cj.cjunc_registry(sid, tuple(float(x) for x in kw['box_lo']), float(kw['vox']), kw['add_pts'], kw['add_phase'],
                                kw['add_fid'], kw['add_kind'], **th)
    except (ValueError, TypeError) as e:
        raise S0Error(f'봉인 SV census — 접합 원장 (carbon_junction.cjunc_registry) 이 입력을 거부했다: {e}') from e
    return {'status': 'sealed', 'function': 'carbon_junction.cjunc_registry (_sv_split) · 문턱 = ca_ext_cjunc.registry_thresholds',
            'grid': JUNCTION_GRID, 's_min_um': th['s_min_um'], 'tol_ff_um': th['tol_ff_um'], 'thresholds': th,
            'census_keys': list(SVCF.CENSUS_KEYS), 'census': {k: int(reg['census'][k]) for k in SVCF.CENSUS_KEYS},
            'fp': {'sid': reg['fp']['sid'], 'registry': reg['fp']['registry']},
            'fp_use': 'record_only — 사슬 대조 = census 세 칸 · 지문은 기록만 (끝 증서 그래프 지문을 붙일 자리 · 지금 대조 안 함)'}


def census_kit(kit, out_dir, *, stage, plan=None, plan_sha=None, plan_source=None, vox=0.15, bridge_um=0.48,
               sdcp_sphere_d=0.30, scripts_dir=SCRIPTS, plan_extra=None):
    """킷 하나 → 보고 dict · 인스턴스 배열 dict · (단계 1) (계획, 바이트, sha256)."""
    if R_F_UM is None:
        raise S0Error('additives.VGCF_D 를 못 읽었다 — r_f 출처 없음')
    kit = os.path.abspath(kit)
    kname = os.path.basename(kit)
    run_dir = find_run_dir(kit)
    t0 = time.time()
    argv = resolve_payload_argv(kit, run_dir, out_dir, vox=vox, bridge_um=bridge_um, sdcp_sphere_d=sdcp_sphere_d,
                                scripts_dir=scripts_dir)
    info = validate_kit_arrays(run_dir, argv, stage=stage)
    snap0 = _snap(kit)
    kw = capture_raster_inputs(argv, run_dir, log_path=os.path.join(out_dir, f'payload_capture_{kname}.log'),
                               scripts_dir=scripts_dir)
    _check_captured(kw, vox, bridge_um, sdcp_sphere_d)
    st = _s3_state()
    try:
        prod = _raster(kw)
        off, off_pid = _raster(kw, drop=(PTFE,), with_pid=True)     # pid = α 전자 채널의 같은 AM 입자 면제 (face_alpha 계획 입력)
        has_sdcp = bool((np.asarray(kw['add_phase']) == SDCP).any())
        nos = _raster(kw, drop=(SDCP,)) if has_sdcp else None
        off_nos = _raster(kw, drop=(PTFE, SDCP)) if has_sdcp else None
        tab = _path_table(kw, prod.shape)
    finally:
        _s3_restore(st)
    shape = prod.shape
    sid_off_fp = cj._grid_fp(off)          # ★ 10-25 묶음 B (RCA2-03) — 파생 격자 지문 (R 런 접합 원장 fp.sid 와 같은 함수 · 같은 규약이면 같은 값)
    lo = np.asarray(kw['box_lo'], np.float64); hi = np.asarray(kw['box_hi'], np.float64); vx = float(kw['vox'])
    v_fids = sorted(f for f, r in tab.items() if r['phase'] == VGCF)
    p_fids = sorted(f for f, r in tab.items() if r['phase'] == PTFE)
    vpaths = [(f, tab[f]['pieces']) for f in v_fids]
    ppaths = [(f, tab[f]['pieces']) for f in p_fids]
    # ── 문턱 입력 · 계획 ──
    spc = spacing_stats([tab[f]['pieces'] for f in v_fids])
    if not spc['n']:
        raise S0Error('VGCF 경로 점 간격이 없다 (섬유 0) — u 를 낼 수 없다')
    plan_out = None
    if stage == 1:
        src = {'stage': 1, 'kit_name': kname, 'run_dir_name': os.path.basename(run_dir),
               'inputs_sha256': {k: v['sha256'] for k, v in info['files'].items()},
               'spacing': {'n': spc['n'], 'median_um': spc['median_um']}, 'tool': TOOL_VERSION,
               'tool_sha256': _sha256_file(os.path.abspath(__file__))}
        plan, pbytes, psha = make_plan(spc['u_um'], R_F_UM, GAP_TOL_PRODUCTION, src)
        plan_out = (plan, pbytes, psha)
        plan_sha, plan_source = psha, 'stage1_computed'
    pv = plan['values_um']
    tol_ff, L_par, r_port, tol_P, tol_sj = (float(pv[k]) for k in ('tol_ff', 'L_par', 'r_port', 'tol_P', 'tol_sj'))
    r_P = PTFE_ROPE_D_UM / 2.0
    r_s = float(sdcp_sphere_d) / 2.0
    # ── 표현 원장 ──
    vols = info['metrics']['vol_um3']

    def vratio(G):
        cnt = _hist(G)
        return {nm: cnt.get(str(sid), 0) * vx ** 3 / vols[nm] for sid, nm in SID_ADDITIVE.items() if nm in vols}
    ledger = {'volume_ratio': {'prod': vratio(prod), 'off': vratio(off)}}
    p_all = (np.vstack([tab[f]['seq'] for f in p_fids]) if p_fids else np.zeros((0, 3), int))
    p_lin = np.unique(np.ravel_multi_index(p_all.T, shape)) if len(p_all) else np.zeros(0, np.int64)
    ledger['ptfe_cover'] = {'prod_sid7_cells_by_off_sid': _hist(off[prod == 7]),
                            'ptfe_path_cells_by_off_sid': _hist(off.ravel()[p_lin]) if len(p_lin) else {}}
    ledger['ptfe_cover']['carbon_sdcp_cells_covered'] = int(sum(v for k, v in ledger['ptfe_cover']
                                                                ['prod_sid7_cells_by_off_sid'].items()
                                                                if k in ('3', '4', '5', '8')))
    cut = {'paths_total': len(v_fids), 'paths_with_ptfe_cells': 0, 'paths_cut': 0, 'extra_components': 0,
           'paths_component_lost': 0, 'cells_removed': 0}
    for f in v_fids:
        c = tab[f]['seq']
        cov = prod[c[:, 0], c[:, 1], c[:, 2]] == 7 if len(c) else np.zeros(0, bool)
        if not cov.any():
            continue
        cut['paths_with_ptfe_cells'] += 1; cut['cells_removed'] += int(cov.sum())
        n0 = n_components_6face(c)
        n1 = n_components_6face(c[~cov]) if (~cov).any() else 0
        if n1 > n0:
            cut['paths_cut'] += 1; cut['extra_components'] += n1 - n0
        elif n1 < n0:
            cut['paths_component_lost'] += 1
    ledger['ptfe_cut'] = cut
    ledger['sdcp_cover'] = ({'prod': _hist(nos[prod == 5]), 'off': _hist(off_nos[off == 5])} if has_sdcp else None)
    v_lin_l, v_fid_l = [], []
    for f in v_fids:
        u_ = np.unique(np.ravel_multi_index(tab[f]['seq'].T, shape))
        v_lin_l.append(u_); v_fid_l.append(np.full(len(u_), f, np.int64))
    v_lin = np.concatenate(v_lin_l) if v_lin_l else np.zeros(0, np.int64)
    v_fid = np.concatenate(v_fid_l) if v_fid_l else np.zeros(0, np.int64)
    if has_sdcp:
        stre, via = {}, {}
        for nm, G in (('off', off), ('prod', prod)):
            runs, aff, ax35 = [], 0, 0
            for f in v_fids:
                c = tab[f]['seq']
                gs = G[c[:, 0], c[:, 1], c[:, 2]]
                rr = _runs(gs == 5)
                if rr:
                    aff += 1; runs.extend(rr)
                if len(gs) > 1:                              # 섬유 자기 경로의 이웃 셀 쌍 중 3|5 면 (설계 §3-1 ⚠ — α 몫은 S1 뒤)
                    ax35 += int((((gs[:-1] == 3) & (gs[1:] == 5)) | ((gs[:-1] == 5) & (gs[1:] == 3))).sum())
            stre[nm] = {'n_runs': len(runs), 'cells_total': int(sum(runs)), 'fibres_affected': aff,
                        'run_cells_hist': _hist(runs) if runs else {},
                        'length_um_cellcount_x_vox': float(sum(runs) * vx), 'axial_3_5_faces': ax35}
            via[nm] = sdcp_via(G, v_lin, v_fid)
        ledger['sdcp_stretch'] = stre
        ledger['sdcp_via'] = via
    else:
        ledger['sdcp_stretch'] = ledger['sdcp_via'] = None
    mlin, mcnt = membership_counts([tab[f]['seq'] for f in v_fids], shape)
    cc = {'all': {'ge2': int((mcnt >= 2).sum()), 'ge3': int((mcnt >= 3).sum())}}
    for nm, G in (('off_sid3', off), ('prod_sid3', prod)):
        m3 = G.ravel()[mlin] == 3 if len(mlin) else np.zeros(0, bool)
        cc[nm] = {'ge2': int(((mcnt >= 2) & m3).sum()), 'ge3': int(((mcnt >= 3) & m3).sum())}
    ledger['crossing_cells'] = cc
    if p_fids:
        ps = _segments(ppaths)
        n_pc = sum(len(tab[f]['pieces']) for f in p_fids)
        capv = float(ps['LEN'].sum()) * math.pi * r_P ** 2 + n_pc * 4.0 / 3.0 * math.pi * r_P ** 3
        vr = capv / vols['PTFE']
        ledger['capsule'] = {'volume_ratio': vr, 'f11_band': list(F11_BAND), 'in_band': bool(F11_BAND[0] <= vr <= F11_BAND[1]),
                             'n_pieces': int(n_pc), 'r_P_um': r_P,
                             'definition': 'per piece: sum(segment length x pi r_P^2) + one sphere 4/3 pi r_P^3; overlaps not subtracted'}
    else:
        ledger['capsule'] = None
    ledger['alpha'] = alpha_census(kw, off, off_pid, vols.get('PTFE'))       # S1 ptfe_face_alpha 함수 그대로 (raster-only)
    del off_pid
    # ── 접합 census 미리보기 ──
    vv = vv_census(vpaths, R_F_UM, tol_ff, L_par)
    I = vv['inst']
    n_i = len(I['fa'])
    z_top = info['metrics']['thickness_um'] + float(lo[2])
    loc = []
    for m in I['mid']:
        if (m < lo).any() or (m >= hi).any():
            loc.append('outside_box')
        elif m[2] > z_top:
            loc.append('above_top_plate')
        elif m[2] > z_top - vx:
            loc.append('near_top_plate')
        elif m[2] < lo[2] + vx:
            loc.append('near_bottom_plate')
        else:
            loc.append('interior')
    ports = {}
    pcells = {}
    for nm, G in (('off', off), ('prod', prod)):
        sts, rels, dists = [], [], []
        pc_ = []
        for q in range(n_i):
            ra = port_of(I['C1'][q], tab[int(I['fa'][q])]['seq'], G, lo, vx, r_port)
            rb = port_of(I['C2'][q], tab[int(I['fb'][q])]['seq'], G, lo, vx, r_port)
            sts.extend([ra[0], rb[0]])
            dists.extend([x[2] for x in (ra, rb) if x[2] is not None])
            if ra[1] is not None and rb[1] is not None:
                rels.append(voxel_relation(ra[1], rb[1]))
            pc_.append((ra[1], rb[1]))
        ports[nm] = {'status_counts': _count(sts), 'relation_counts': _count(rels), 'dist_um': _dist(dists)}
        pcells[nm] = pc_
    ptfe_ex = (_min_dist_to_segments(I['mid'], ppaths, PROX_CUTOFF_UM) - (r_P + R_F_UM)) if n_i else np.zeros(0)
    sd_pts = np.asarray(kw['add_pts'], np.float64)[np.asarray(kw['add_phase']) == SDCP]
    if has_sdcp and n_i:
        from scipy.spatial import cKDTree
        dd, _ = cKDTree(sd_pts).query(I['mid'])
        sdcp_ex = dd - r_s
    else:
        sdcp_ex = np.full(n_i, np.nan)
    via_d = np.full(n_i, -1, np.int64)
    if has_sdcp:
        for q, (pa, pb) in enumerate(pcells['off']):
            if pa is not None and pb is not None:
                dq = via_sdcp_depth(off, pa, pb, K_SDCP_CELLS)
                via_d[q] = 0 if dq is None else dq
    am_c = np.asarray(kw['am_c'], np.float64); am_r = np.asarray(kw['am_r'], np.float64)
    va = fiber_sphere_instances(vpaths, am_c, am_r, R_F_UM, TOL_FS_PREVIEW_UM)
    sv = sa = None
    if has_sdcp:
        svr = fiber_sphere_instances(vpaths, sd_pts, np.full(len(sd_pts), r_s), R_F_UM, tol_sj)
        sv = {'n_pairs': svr['n_pairs'], 'n_instances': svr['n_instances'],
              'n_particles_touching': svr['n_spheres_touching'], 'n_particles_ge2_fibres': svr['n_spheres_ge2_fibres'],
              'gap_um': _dist(svr['gap_um'])}
        from scipy.spatial import cKDTree
        if len(am_c):
            lists = cKDTree(am_c).query_ball_point(sd_pts, r_s + float(am_r.max()) + tol_sj)
            npair, ntouch = 0, 0
            for q, L_ in enumerate(lists):
                if not L_:
                    continue
                L_ = np.asarray(L_, np.int64)
                hit = np.linalg.norm(am_c[L_] - sd_pts[q], axis=1) <= am_r[L_] + r_s + tol_sj
                npair += int(hit.sum()); ntouch += int(hit.any())
            sa = {'n_pairs': npair, 'n_particles_touching': ntouch}
        else:
            sa = {'n_pairs': 0, 'n_particles_touching': 0}
    arc = {f: float(_segments([(f, tab[f]['pieces'])])['LEN'].sum()) for f in v_fids}
    ninst = {f: 0 for f in v_fids}
    for q in range(n_i):
        ninst[int(I['fa'][q])] += 1
        if int(I['fb'][q]) != int(I['fa'][q]):
            ninst[int(I['fb'][q])] += 1
    lj_f = np.array([f for f in v_fids if ninst[f] > 0], np.int64)
    lj = np.array([arc[f] / ninst[f] for f in lj_f], np.float64)
    out_box = 0
    vp = np.asarray(kw['add_pts'], np.float64)[np.asarray(kw['add_phase']) == VGCF]
    if len(vp):
        out_box = int(((vp < lo) | (vp >= hi)).any(1).sum())
    info['counts']['vgcf_points_outside_box'] = out_box
    census = {
        'status': 'b0_preview',
        'verdict_use': 'forbidden — 판정 · 보고의 instance census 는 B3 cjunc_registry 와 같은 함수로만 (설계 §2 ① · §4-1)',
        'vv': {'n_instances': vv['n_vv'], 'n_self': vv['n_self'], 'n_long': vv['n_long'],
               'n_long_vv_only': {'touch': int(((~I['is_self']) & (I['L_touch'] > L_par)).sum()) if n_i else 0,
                                  'band': int(((~I['is_self']) & (I['L_band'] > L_par)).sum()) if n_i else 0},
               'lc_definition': vv['lc_definition'], 'thr_um': vv['thr_um'], 'n_segments': vv['n_segments'],
               'n_rows': vv['n_rows'], 'gap_um': _dist(I['gap']), 'L_touch_um': _dist(I['L_touch']),
               'L_band_um': _dist(I['L_band']), 'theta_deg': _dist(I['theta_deg']),
               'theta_hist_deg': _count(['00-10' if x < 10 else '10-30' if x < 30 else '30-60' if x < 60 else '60-90'
                                         for x in I['theta_deg'] if np.isfinite(x)]),
               'penetrating': int((I['gap'] < 0).sum()) if n_i else 0, 'location': _count(loc)},
        'ports': ports,
        'ptfe_proximity': {'excess_um': _dist(ptfe_ex), 'n_covered_tolP': int((ptfe_ex <= tol_P).sum()) if n_i else 0,
                           'n_beyond_cutoff': int(np.isinf(ptfe_ex).sum()) if n_i else 0, 'cutoff_um': PROX_CUTOFF_UM,
                           'r_P_um': r_P},
        'sdcp_proximity': ({'excess_um': _dist(sdcp_ex), 'n_near_tolsj': int((sdcp_ex <= tol_sj).sum()), 'r_s_um': r_s}
                           if has_sdcp else None),
        'volume_connected': ({'k_cells': K_SDCP_CELLS, 'n_with_ports': int((via_d >= 0).sum()),
                              'n_connected': int((via_d > 0).sum()),
                              'frac_connected': (float((via_d > 0).sum()) / max(1, int((via_d >= 0).sum()))),
                              'depth_counts': _hist(via_d[via_d > 0]) if (via_d > 0).any() else {}}
                             if has_sdcp else None),
        'va': {'n_instances': va['n_instances'], 'n_pairs': va['n_pairs'], 'gap_um': _dist(va['gap_um']),
               'tol_fs_um': TOL_FS_PREVIEW_UM},
        'sv': sv, 'sa': sa,
        'junction_spacing': {'lj_um': _dist(lj), 'fibres_without_instance': int(sum(1 for f in v_fids if ninst[f] == 0)),
                             'fibres_total': len(v_fids)},
    }
    # ── 접합 census — 판정 · 보고 판 = B3 cjunc_registry 그대로 (off 격자 · 계획 문턱 · s_min 미등록) ──
    junction, jarrays = junction_census(kw, off, tol_ff=tol_ff, L_par=L_par, r_port=r_port, tol_P=tol_P, tol_sj=tol_sj,
                                        r_ptfe=r_P, r_sdcp=r_s)
    junction['arrays_file'] = f's0_junctions_{kname}.npz'
    #  ★ 10-25 묶음 B (X6 · Q20 (가)) — 단계 2 = 봉인 SV census (R 계획의 s_min · tol_ff · 단계 2 관문이 커밋에서 읽은 값) · 단계 1 = null
    sv_sealed = None
    if stage == 2:
        rpl = (plan_extra or {}).get('r_plan') or {}
        sv_sealed = sv_census_sealed(kw, off, s_min_um=rpl.get('s_min_um'), tol_ff_um=rpl.get('tol_ff_um'))
    rep = {
        'schema': SCHEMA, 'stage': int(stage), 'tool': TOOL_VERSION,
        'kit': {'path': kit, 'name': kname, 'run_dir': run_dir, 'run_dir_name': os.path.basename(run_dir),
                'kit_scripts_realpath': (os.path.realpath(os.path.join(kit, 'scripts'))
                                         if os.path.exists(os.path.join(kit, 'scripts')) else None),
                'run_complete_marker': os.path.isfile(os.path.join(run_dir, 'mpm_done.marker'))},
        'code': _code_info(),
        'inputs': {'files': info['files'], 'counts': info['counts'], 'metrics': info['metrics'],
                   'payload_argv_sha256': hashlib.sha256('\0'.join(argv).encode('utf-8')).hexdigest(),
                   'vgcf_rel_dia': info['vgcf_rel_dia'],
                   #  ★ 10-25 묶음 B (RCA2-03) — 설정 지문 (킷 run_mpm.sh 의 payload 호출부 · 사슬 대조 · payload_argv_sha256 은 경로가 들어가
                   #    기록만)
                   'settings_sha256': kit_settings_sha256(kit)},
        'raster': {'convention': {'vox_um': vx, 'bridge_um': float(kw['bridge_um']), 'sdcp_sphere_d_um': float(sdcp_sphere_d),
                                  'ptfe_stamp_captured': 'centerline', 'fibre_stamp': 'segment',
                                  'origin_shift_um': [0.0, 0.0, 0.0], 'fid_gap_tol': float(kw['fid_gap_tol']),
                                  'off_grid': 'captured inputs minus PTFE rows (= ptfe_stamp off · face_alpha sid grid)'},
                   'grid_shape': [int(x) for x in shape], 'box_lo_um': lo.tolist(), 'box_hi_um': hi.tolist(),
                   'cells_by_sid': {'prod': _hist(prod), 'off': _hist(off),
                                    'nosdcp': _hist(nos) if has_sdcp else None,
                                    'off_nosdcp': _hist(off_nos) if has_sdcp else None},
                   'sid_off_fp': sid_off_fp},
        'ledger': ledger,
        'threshold_inputs': {'u_um': spc['u_um'], 'spacing_median_um': spc['median_um'], 'n_spacings': spc['n'],
                             'spacing_p10_um': spc.get('p10_um'), 'spacing_p90_um': spc.get('p90_um'),
                             'spacing_max_um': spc.get('max_um'), 'rule': FORMULAS['u'],
                             'used_for_plan': stage == 1},
        'thresholds_used': {'tol_ff_um': tol_ff, 'L_par_um': L_par, 'r_port_um': r_port, 'tol_P_um': tol_P,
                            'tol_sj_um': tol_sj, 'tol_fs_um': TOL_FS_PREVIEW_UM, 'r_f_um': R_F_UM},
        'plan': dict({'sha256': plan_sha, 'source': plan_source}, **(plan_extra or {})),
        'junction_census': junction,
        'sv_census': sv_sealed,
        'census_preview': census,
        'notes': list(NOTES),
        'elapsed_s': round(time.time() - t0, 1),
    }
    if _snap(kit) != snap0:
        raise S0Error(f'{kit}: S0 가 킷 폴더를 바꿨다 (쓰기 0 계약 위반)')
    bad = schema_forbidden_keys(rep)
    if bad:
        raise S0Error(f'보고에 σ · 전류 · 소산 칸: {bad[:5]}')
    arrays = {'fa': I['fa'], 'fb': I['fb'], 'is_self': I['is_self'], 'd_min': I['d_min'], 'gap': I['gap'],
              'theta_deg': I['theta_deg'], 'L_touch': I['L_touch'], 'L_band': I['L_band'], 'C1': I['C1'], 'C2': I['C2'],
              'mid': I['mid'], 'location': np.array(loc, dtype='<U24'), 'ptfe_excess_um': ptfe_ex,
              'sdcp_excess_um': sdcp_ex, 'via_depth': via_d, 'lj_um': lj, 'lj_fid': lj_f}
    return rep, arrays, plan_out, jarrays


def run_stage(stage, kits, out_dir, *, threshold_commit=None, plan_path=None, repo=None, r_doc=R_DOC_DEFAULT,
              vox=0.15, bridge_um=0.48, sdcp_sphere_d=0.30, scripts_dir=SCRIPTS, r_plan_path=None):
    """단계 1 (SBE 하나 → 원장 · 계획) · 단계 2 (개정 커밋 확인 → DBE 침대들).  → {'reports': […], 'plan': 경로 | None}."""
    if stage not in (1, 2):
        raise S0Error('--stage 는 1 또는 2')
    kits = list(kits or [])
    if not kits:
        raise S0Error('--kit 이 없다')
    plan = plan_sha = plan_source = plan_extra = None
    if stage == 1:
        if len(kits) != 1:
            raise S0Error('단계 1 = SBE 침대 하나 (계획은 한 침대의 기하에서만 나온다)')
        if threshold_commit or plan_path or r_plan_path:
            raise S0Error('단계 1 에는 --threshold-commit · --plan-path · --r-plan-path 를 주지 않는다')
    else:
        if not threshold_commit or not plan_path or not r_plan_path:
            raise S0Error('단계 2 는 --threshold-commit <§2-1 개정 커밋> · --plan-path <리포 안 계획> · --r-plan-path <같은 커밋의 R 런 '
                          '사슬 계획 · s_min 봉인> 가 있어야 돈다 (N17 · ★ 10-21 PRE-design-04)')
        plan, plan_sha, full, rinfo = verify_plan_commit(repo or ROOT, threshold_commit, plan_path, r_doc=r_doc,
                                                         r_plan_path=r_plan_path)
        plan_source = f'commit:{full}'
        plan_extra = {'r_plan': rinfo}
    out_dir = os.path.abspath(out_dir)
    if os.path.exists(out_dir) and (not os.path.isdir(out_dir) or os.listdir(out_dir)):
        raise S0Error(f'출력 폴더가 이미 있고 비어 있지 않다: {out_dir} (덮어쓰기 · 섞임 금지)')
    names = [os.path.basename(os.path.abspath(k)) for k in kits]
    if len(set(names)) != len(names):
        raise S0Error(f'같은 이름의 킷 둘: {names}')
    os.makedirs(out_dir, exist_ok=True)
    res = {'reports': [], 'plan': None, 'plan_sha256': plan_sha}
    for kit in kits:
        rep, arrays, pout, jarrays = census_kit(kit, out_dir, stage=stage, plan=plan, plan_sha=plan_sha,
                                                plan_source=plan_source, vox=vox, bridge_um=bridge_um,
                                                sdcp_sphere_d=sdcp_sphere_d, scripts_dir=scripts_dir, plan_extra=plan_extra)
        kn = rep['kit']['name']
        rp = os.path.join(out_dir, f's0_stage{stage}_{kn}.json')
        with open(rp, 'w', encoding='utf-8') as f:
            json.dump(rep, f, ensure_ascii=False, indent=1)
        np.savez(os.path.join(out_dir, f's0_instances_{kn}.npz'), **arrays)
        np.savez(os.path.join(out_dir, rep['junction_census']['arrays_file']), **jarrays)
        res['reports'].append(rp)
        if pout is not None:
            _p, pbytes, psha = pout
            pp = os.path.join(out_dir, 'cjunc_plan.json')
            with open(pp, 'wb') as f:
                f.write(pbytes)
            with open(os.path.join(out_dir, 'cjunc_plan.sha256'), 'w', encoding='ascii') as f:
                f.write(f'{psha}  cjunc_plan.json\n')
            res['plan'], res['plan_sha256'] = pp, psha
    return res


def _summary(rep):
    L, C = rep['ledger'], rep['census_preview']
    cb = rep['raster']['cells_by_sid']
    lines = [f"── {rep['kit']['name']} (단계 {rep['stage']}) · {rep['kit']['run_dir_name']} · {rep['elapsed_s']} s",
             f"  셀 (생산) {cb['prod']}  ·  (off) {cb['off']}",
             f"  PTFE 가 덮은 셀 (off sid) {L['ptfe_cover']['prod_sid7_cells_by_off_sid']} · 끊긴 VGCF 경로 "
             f"{L['ptfe_cut']['paths_cut']} / {L['ptfe_cut']['paths_total']} (조각 +{L['ptfe_cut']['extra_components']})",
             f"  표현 부피 비 (생산) {({k: round(v, 4) for k, v in L['volume_ratio']['prod'].items()})}"]
    if L['sdcp_cover']:
        lines.append(f"  SDCP 가 덮은 셀 (생산 · 없을 때 sid) {L['sdcp_cover']['prod']} · 섬유 구간 "
                     f"{L['sdcp_stretch']['off']['n_runs']} · SDCP 경유 섬유 연결 (off) {L['sdcp_via']['off']['n_bridging']}")
    if L['capsule']:
        lines.append(f"  캡슐 부피 비 {L['capsule']['volume_ratio']:.4f} (밴드 {L['capsule']['f11_band']} 안 = {L['capsule']['in_band']})")
    A = L.get('alpha') or {}
    if A.get('status') == 'computed':
        fe, fi = (A.get('faces') or {}).get('electronic') or {}, (A.get('faces') or {}).get('ionic') or {}
        lines.append(f"  α (S1 ptfe_face_alpha · {A.get('grid')} 격자 · K {A.get('K')} · {A.get('dia_law')}) 전자 α<1 면 "
                     f"{fe.get('n_rows')} (α=0 {fe.get('n_cut_rows')}) · 이온 α<1 면 {fi.get('n_rows')} (α=0 {fi.get('n_cut_rows')}) · "
                     f"캡슐 부피 {(A.get('volume') or {}).get('status')}")
    ti, tu = rep['threshold_inputs'], rep['thresholds_used']
    lines.append(f"  점 간격 중앙값 {ti['spacing_median_um']:.6g} µm (n {ti['n_spacings']}) → u {ti['u_um']:.6g} · "
                 f"tol_ff {tu['tol_ff_um']:.6g} · L_par {tu['L_par_um']:.6g} · r_port {tu['r_port_um']:.6g}")
    J = rep.get('junction_census') or {}
    if J:
        jc, ss = J.get('census') or {}, J.get('self_s_um') or {}
        lines.append(f"  [접합 census · cjunc_registry · {J.get('grid')} 격자] VV {jc.get('n_instances_distinct')} · 자기 후보 "
                     f"{jc.get('n_self_candidates')} (s 최소 {ss.get('min')} · 중앙 {ss.get('p50')} µm · 거르지 않음 = S0 는 s_min 안 씀) · "
                     f"긴 접촉 {J.get('n_long')} (distinct {J.get('n_long_distinct')} · self {J.get('n_long_self')}) · 배율 합 "
                     f"{J.get('len_mult_sum'):.6g} · 미실현 {jc.get('n_unrealized_by_reason')} · 후보별 → {J.get('arrays_file')}")
        rv, sb = J.get('revisit') or {}, J.get('subedges') or {}
        lines.append(f"  [census 보탬 10-21] 같은 셀 비연속 재방문 쌍 {rv.get('n_pairs')} · 셀 {rv.get('n_cells')} · 섬유 "
                     f"{rv.get('n_fibres')} · s {rv.get('s_um')} · 포트 동률 {J.get('n_port_ties')} · 분산 간선 {sb.get('n')} (긴 접촉 "
                     f"{sb.get('n_long')}) · 간선별 PTFE 덮임 {sb.get('n_ptfe_cov')} · 부분 덮임 instance {sb.get('n_instances_ptfe_partial')}")
    vv = C['vv']
    lines.append(f"  [B0 미리보기] VV {vv['n_instances']} · 자기 {vv['n_self']} · 긴 접촉 (> L_par) touch {vv['n_long']['touch']} "
                 f"· band {vv['n_long']['band']} · 관통 {vv['penetrating']} · 위치 {vv['location']}")
    lines.append(f"  포트 (off) {C['ports']['off']['status_counts']} · 관계 {C['ports']['off']['relation_counts']}")
    lines.append(f"  계획 sha256 {rep['plan']['sha256']} ({rep['plan']['source']})")
    return '\n'.join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description='Rint ② S0 표현 원장 (raster-only · 솔브 없음) — 설계 v1 §2 · 등록 R §2-1')
    ap.add_argument('--stage', type=int, choices=(1, 2), required=True, help='1 = SBE 하나 → 계획 · 2 = DBE 침대들 (개정 커밋 필요)')
    ap.add_argument('--kit', action='append', required=True, help='킷 폴더 (run_mpm.sh · latest_run) — 단계 2 는 여러 번')
    ap.add_argument('--out', required=True, help='새 출력 폴더 (있으면 비어 있어야)')
    ap.add_argument('--threshold-commit', default=None, help='단계 2 — 등록 R §2-1 개정 커밋 sha')
    ap.add_argument('--plan-path', default=None, help='단계 2 — 그 커밋 안 계획 파일의 리포 상대 경로')
    ap.add_argument('--r-plan-path', default=None, help='단계 2 — 같은 개정 커밋 안 R 런 사슬 계획 (사슬 3 판 rint-r-plan-v2 · s_min 봉인) 의 '
                                                         '리포 상대 경로 (sha256 = 등록 R "| 계획 해시 |" 줄)')
    ap.add_argument('--r-doc', default=R_DOC_DEFAULT, help='계획 sha256 이 적힌 등록 R 문서 (리포 상대)')
    ap.add_argument('--repo', default=ROOT, help='개정 커밋을 확인할 저장소 (기본 = 이 도구의 작업 트리)')
    ap.add_argument('--vox', type=float, default=0.15)
    ap.add_argument('--bridge-um', type=float, default=0.48)
    ap.add_argument('--sdcp-sphere-d', type=float, default=0.30)
    a = ap.parse_args(argv)
    try:
        res = run_stage(a.stage, a.kit, a.out, threshold_commit=a.threshold_commit, plan_path=a.plan_path, repo=a.repo,
                        r_doc=a.r_doc, vox=a.vox, bridge_um=a.bridge_um, sdcp_sphere_d=a.sdcp_sphere_d,
                        r_plan_path=a.r_plan_path)
    except S0Error as e:
        print(f'[S0] ⛔ 거부 — {e}', file=sys.stderr)
        return 2
    for rp in res['reports']:
        with open(rp, encoding='utf-8') as f:
            print(_summary(json.load(f)))
    if res['plan']:
        print(f"\n[S0] 단계 1 계획 → {res['plan']}\n      sha256 {res['plan_sha256']}\n"
              '      ⬜ 이 출력 (보고 JSON · 계획 · sha256) 을 보내 주세요 → 등록 R §2-1 개정 커밋 (숫자 + 계획 sha256 + 계획 파일 · '
              '결과 0 건) → 그 커밋 sha 로 단계 2')
    return 0


if __name__ == '__main__':
    sys.exit(main())
