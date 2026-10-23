#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② S2 탄소 접합 R_j v0 (VGCF–VGCF) + S3 SDCP 접합 수정자 — 시험 먼저 (규율 ② · 2026-10-20).

정본 = 설계 v1 `docs/reviews/rint_carbon_additive_design_v1_20261020.md` §4 · §5 (+ 계약 v2 §3-8 J1–J8 · v3 §5 J2a–J12 · v3.1) ·
1저자 10-20 N1–N18 = 권고대로.  ⚠ 이 시험의 PASS 는 **계약 · 구현의 증거**이지 R_j 값 · 판정 (R) 의 증거가 아니다.
기대값은 **모듈 밖에서** 손으로 세운 회로 (직렬 사슬 · 사다리) 를 직접 풀어 만든다 — 같은 함수로 정답을 다시 만들지 않는다.

  python3 scripts/test_carbon_junction.py            # 현 구현
  python3 scripts/test_carbon_junction.py --quick    # 끔 비트 동일 (C0) 의 무작위 침대 수를 줄인다

픽스처 단위: h = 1 µm · r_f = 0.5 µm (섬유 지름 = 1 복셀 — 생산 Ø0.15 @ vox 0.15 와 같은 비) · tol_ff = 0.1 · L_par = 2(r_fi + r_fj) = 2.0 ·
r_port = 2.0 (= 2h) · gap_tol 2.0 · σ_VGCF = 100 S/cm → 축방향 면 g = σ·h = 100 · 판 결합 g = σ·h²/(h/2) = 200 (코드 단위 S/cm·µm) ·
접합 간선 g = 1e4/R_j (설계 §4-1 J5).

묶음 (설계 §4-4 · §5-4 · 브리프 B):
  C0     끔 = 옛 경로 비트 동일 (기준 = 커밋 d1768cf0c 의 step3_sigma · 무작위 침대 16 입력 · σ · φ · n_dof · cg_info · resid · sid)
  C1     cross_shared — 판 ↔ A ↔ 교차 셀 (멤버십 dof 둘) ↔ B ↔ 판 = 해석 직렬 사슬 (1e-12) · R_j 스윕 Rayleigh 단조
  T1-7   R_j → 0 = 축약 그래프 (C1 = 옛 융합 · C2a = 포트 병합 회로) · R_j = ∞ = 가닥 사이 전류 0 · 가닥 안 연속
  C2     cross_face (옛 융합 면 절단 + 간선 하나) · cross_edge (옛 단절 → 접합으로 연결 · 가지치기가 안 지움 = J12)
  C3     pass_through — 교차 셀을 지나는 가닥은 R_j 와 무관 (J6 · J12)
  C4     series_chain — R = 기저 + (N−1)·R_j (기울기 정확) · 단위 변이 (1e4 빠짐 · ×1e8) 실패
  C5     instance — 같은 접촉을 조각 더 잘게 · 섬유 순서 · 점 역순 = instance 수 · σ 불변 (J2c) · 같은 쌍 두 곳 = instance 둘
  T1-6   junction_multi — 두 자리 사다리 회로 (1e-12) · 등전위 극한 R → R_j/2
  T1-8   crossing_k3 / J9 — 한 셀 세 가닥 → dof 셋 · instance 셋 · 포트 dof 서로 다름
  T1-9   fiber_sphere_threshold (J2b) — r_f 0.075 · R_AM 2 · d 2.12 µm = 접촉 아님 (문자식 2.15 오판 아님)
  T1-10  self_contact — 같은 fid 비연속 두 셀 면 → 자기 접합 instance 하나 · 0 저항 지름길 없음
  T1-11  port_tie — 등거리 두 후보 → 정준 방향 경로 번호가 작은 셀 · 동률 수 · 점 역순 · 섬유 순서에 σ 불변
  T1-12  site_cut — 같은 쌍 두 자리 중 한 자리만 instance → 그 발자국 면만 절단 · 다른 자리 = 미등록 법칙 (cut ≤ fused)
  T1-5′  lead_reference — 단자 기준 R_j · 리드 빼기 · 음수 = 거부 (v0 = 모형 내부값만)
  ── 길이 법칙 v0 (1저자 10-20 밤 Q17 · J8 "긴 접촉 = 정량 거부" 를 대체): G_j = max(1, L_c/L_par)/R_j,0 ──
  LEN-X  깊은 직교 교차 (L_c = L_par) → 배율 1 · σ = 옛 점 접합 회로 (1e-12)
  LEN-BIT 긴 접촉 없는 침대 9 개 = 구현 B (61b6a9ec5 · 점 접합) 와 σ · n_dof · cg_info · resid · 접합 전류 비트 같음
  LEN-P  나란한 두 섬유 L_c = 3 L_par → 배율 3 → σ = 판 + 섬유 + 접합 1/(3/R_j,0) 해석 회로 (기계 정밀도 · cut · fused)
  LEN-O  비스듬한 깊은 교차 → 배율 = 1/sin θ · 90° 에서 1 정확히 · 연속 · 각도에 단조
  J8     long_contact — 긴 접촉 = 표지 · 집계 칸 그대로 · 정량 거부 없음 (옛 동작 제거) · 정량 솔브 진행
  FOOT   절단 발자국 = 접촉 run 전체 — fused 법칙에서도 run 위 A|B 융합 면 0 (면 tombstone · 간선 원장 · σ 해석)
  KINK   U 자로 접힌 한 섬유 — 경로 호 길이 s (손으로 잰 값) · s < s_min = 접합 없음 (옛 복셀 융합 그대로 = 옛 경로 σ) ·
         s ≥ s_min = 자기 접합 하나 (절단 + R_j 간선 × 같은 배율) · s_min 없음 + 정량 = 구조화 거부 · 자기 L_c = 닿음 규칙
  INV    점 역순 · 원점 이동 · 섬유 번호 바꿈 → sid · instance 수 · 배율 · σ 같음 (LP · KU)
  SMIN   s_min_um = 필수 키워드 · 기본값 없음 · 비유한 · 음수 · bool · 문자 거부
  REC    기록 — 법칙 이름 len_scaled_v0 · s_min · L_c 분위 · 배율 합 · 자기 접합 (후보 · 거른 수 · 남은 수 · s 분포) · 지문에 s_min
  MUT-LEN 변이 넷 (배율 제곱 · max(1, ·) 빼기 · s 거르기 끔 · 발자국 = 최근접 쌍만) 이 위 시험에 걸린다
  J11    electrode_short — 축약 무리가 두 판에 다 닿으면 단락 상태 (유한 σ 로 위장하지 않는다)
  C6     energy — Σ P (면 + 접합 + 판) = I·ΔV · 접합 몫 = −∂lnσ/∂lnR_j (중심 FD)
  C8     guards — r1 · ①′ · 주기 · return_field · 다른 vox · sid · 계획 · 원장 변조 · NaN · 길이 불일치 · 떨어진 같은 fid · kind 없음 ·
         VGCF 절연 채널 · 법칙 미선언 · R_j 극한 → 조립 전 거부 (CG 호출 0)
  P-1/2  PTFE–접합 법칙 — P1 = 덮인 instance 만 절단 · P0 = 영향 없음 · 경계 = 정확히 tol_P 포함 · centerline + P1 = 거부 ·
         (P1, c = 1) = 절단 먼저 (N18)
  FA+CJ  S1 face_alpha × S2 cjunc 를 한 솔브에 같이 = ★ Z3 (10-20) 받음 (설계 조합 규칙 — α 먼저 · 접합 훅 다음 · α 는 접합 간선에 안 걸림 ·
         옛 임시 거부를 뺐다) · 각각 홀로도 받음 · 조합 σ ≤ 접합만 σ (α ≤ 1 · Rayleigh) · 접합 기록 = 접합만과 같음
         (조합 규칙의 전수 시험 = `scripts/test_ca_ext_z3.py` A)
  S3-1…11 SDCP 접합 수정자 (c = 0 비트 같음 · SBE no-op · c 단조 · c = 1 축약 · 순열 · 경계 · 펠릿 no-op · 변이 · S2 없이 거부 ·
         sid 불변 · 우선순위)
  SV     SV 면 · SDCP 셀 소산 몫 · SV_DOMINANT 표지 · SDCP 경유 섬유 연결 수
  PIECE  멤버십 셀 = `_fibre_segment_ijk` 의 VGCF 셀 (같은 끊기 규칙 · 복제 + 동등 시험)
  PIECE4 끊기 규칙 사본 대조 (2 일 차) — 생산 `step3_sigma._fibre_segment_ijk` ↔ B `carbon_junction.fibre_pieces` ↔
         C `ca_s0_census.pieces_of` ↔ A `ptfe_face_alpha.build_capsules`: 끊김이 있는 합성 침대에서 조각 경계 · 셀 열 · 셀 집합 같음 ·
         네 곳 각각의 `>` → `>=` 변이 사본이 시험을 떨어뜨린다 (하나로 합치는 리팩터는 하지 않는다 — 생산 경로 비트 동일 부담)
  FP     지문 재현 (RINT-23 · 2 일 차) — 같은 내용 · 다른 객체 → 같은 지문 · 별도 `python3 -I` 하위 프로세스 둘 → 같은 지문 ·
         한 글자 다름 → 다른 지문.  `carbon_junction._fp` (객체 배열 = 내용 직렬화 · 숫자 배열 = dtype · 모양 · C 순서 바이트) ·
         원장 · 계획 지문 · 격자 지문 감싸개 (`_grid_fp` — 객체 격자 거부) · 같은 꼴 확인 = `ptfe_face_alpha` (캡슐 · 행 · 계획 ·
         간선) · `ca_s0_census` (계획 sha256 · 파일 sha256) · `step3_conv_cert` (지문 함수 없음 — 목록 시험이 지킨다)
  ── RCA (Codex 10-21 판정문 RCA-03 · 04 · 05 · 06 + Q11 일부 · 1저자 10-21 Q1–Q4 (가) · 시험 먼저 — Codex 반례를 우리 시험으로) ──
  RCA03  (Q1) 멤버십 열쇠 (cell, fid, branch) — 판정문 RCA-03 폴리라인 (h 0.15 · r_f 0.075 · 리드 붙임): 같은 셀 다른 가지를
         합치지 않는다 (s < s_min = 경로로만 → 5 Ω 꼴 직렬 사슬 그대로 · 옛 = 2 Ω 꼴 단락) · s ≥ s_min = 그 가지 둘 사이 R_j 간선
         (기하 접점 포트) · R_j = ∞ = 사슬 · c = 1 (SDCP 근접) — 접합 아닌 재방문은 축약되지 않는다 · 다른 셀 자기 접근 (KU) c = 1 ·
         KINK-R 재방문 (경로로만 · 합침 변이 = 벗어남)
  RCA04  (Q2) 포트 = 방향 무관 기하 정준 규칙 (접점까지 셀 중심 거리 · ε 띠 동률 → 셀 정수 좌표 사전식 최소 · 경로 번호 안 씀) —
         먼 끝만 바꿔 정준 방향이 뒤집혀도 포트 · 간선 원장 · σ 비트 같음 · 경로 반전 · 공선 세분 (이진 정확) · fid 재명명 (교차 셀
         추가 dof 있는 침대) → 포트 · 간선 원장 · σ 비트 같음 · 무작위 점 섞기 = 다름 (판별력)
  RCA05  (Q3) 분산판 v0 — Codex 5 노드 회로 (분산 1.366013071895 S · 왼쪽 집중 5 · 중앙 집중 0.238095238095) 재현 + 같은 꼴의
         침대 (단자 = 접촉 같은 끝) 에서 k = ceil(L_c/L_par) 간선 · 각 G/k · 등분점 최근접 포트 · σ = 손 회로 · 간선마다 PTFE 덮임
         (P1 = 덮인 간선만 절단) · SDCP 근접 (c = 1 = 근접 간선만 축약) · L_c ≤ L_par = 옛 점 접합 비트 같음 (LEN-BIT · 정준 번호)
  RCA06  (Q4) `SV_DOMINANT` → 진단 `SV_local_dissipation` (지배성 표지 철회 · 기록에 sv_dominant 없음) + 반사실 대조 (선택 노브 ·
         SV 면 끊은 판의 단자 G 비 `sv_counterfactual_ratio` · 문턱 = 기본값 없음 · `SV_DEPENDENT` 는 문턱이 주어질 때만) —
         Codex 반례 꼴 (SV 경로 전류 ≈ 0.92 · 옛 가드 false) 에서 비 ≈ 10 = 손 회로 · SDCP 없음 = 비 1 정확
  CEN    (Q11 일부) census 보탬 — 같은 셀 비연속 재방문 (쌍 · 셀 · 섬유 · s) · 포트 동률 수 · 긴 접촉 간선 · 간선별 PTFE 덮임 ·
         부분 덮임 instance (같은 함수 `cjunc_registry` · σ 칸 없음)
  ── RCA2 (사전 리뷰 (구현) 10-21 · PRE-impl-01–06 · 09 · 1저자 Q-A–Q-D 권고대로 · 시험 먼저 — 탐침 반례를 우리 시험으로) ──
  GAP    (Q-A · 01) 같은 섬유의 끊긴 두 조각 = 서로 다른 섬유와 같은 규칙 (중심선 d ≤ D → R_j 접합) — 같은 셀 · 면 인접 · 생산 단위 →
         손 회로 (조각 사슬 + R_j) · s_min 무관 · census (같은 fid 조각 쌍 · 같은 셀 조각 만남 · '경로로만' 거짓 칸 정정)
  RING   (Q-A · 06) 닫힌 경로 이음매 = 연속 (접합 · 끊김 없음 · 손 고리 회로) · 틈 하나 있는 고리 = 이음매를 지나 한 조각 + 틈 R_j 접합
  SELFD  (Q-B · 02) 자기 접합 = 중심선 d ≤ D (서로 다른 섬유와 같은 탐지) — 닿지 않는 다리 (KW 1.2 > D) = 접합 없음 · 미등록 면 (fid 와
         무관) · 닿는 모서리 인접 다리 (0.1414) = 같은 fid 도 접합 · 기록 (L_c · 배율 · k · 포트 셀 · d0) = 둘로 나눈 서로 다른 섬유와 같음
  XC     (Q-B) 자기 교차 (닿음 0.8 · s 10.8 · L_c 1.2) — s ≥ s_min = R_j 간선 (손 회로) · s < s_min = 옛 융합 (= cjunc 끔) · 바닥 s > D ·
         s > (π/2)·d ·
         s_min 없음 + 정량 = 거부 · fid 무관 (나눈 섬유 기록 같음) — 옛 KU 기반 KINK · INV · REC 의 접합 꼴을 이 픽스처로 옮겼다 (쌍마다
         s 규칙에서 KU 다리는 s 가 높이에 따라 연속으로 바뀐다)
  QC     (Q-C · 03) 덮인 접점 = 옮기지 않음 (미실현 covered_SDCP · SV 융합 한 번 · 손 회로 = R_j ∞ 와 같음) · 접합 + centerline = 거부
         (계획 · 솔브 입구 · protocol 기록)
  QD     (Q-D · 04) SV 반사실 = 서로 다른 섬유 사이 SV 우회만 끊음 · 섬유 자기 연속 (SDCP 가 덮은 셀을 지나는 같은 조각) 은 남김 ·
         cut-only (비 ≥ 1) — SDCP 를 지나는 섬유 하나 = 비 1 · F1 + 먼 SDCP = 비 1 · SVY (지나는 A + 닿는 B) = 손 회로 비 · SVX 10.29 그대로
  QD2    ★ 10-22 (사전 리뷰 2 회차 PRE2-impl-01 · 04 · 1저자 Q1 (다)) SV 반사실 괄호 — 못 가른 덩어리 (섬유 둘 이상이 함께 지나는 SDCP 성분)
         가 있으면 두 번 푼다 (아래 끝 = 덩어리 그대로 · 위 끝 = 덩어리 셀 면 전부 끊음) · 리뷰어 회로 [1, ∞] → SV_UNCHECKED · 대조 (한 섬유만
         지남) = SV_DEPENDENT · 괄호 성질 (손 참 비가 아래 < 참 < 위) · 변이 J1 회로 (닿기만 하는 C) · J2 회로 (덮이지 않은 사이로 두 번 닿음) ·
         덩어리 0 = 다시 풀지 않음 · 값 봉인 · census 변조 = fail-closed · 주 해 미수렴 · 주 전류 ≤ 0 의 괄호 칸 · 덩어리가 판에 닿으면 위 끝이
         판 결합까지 뺀다 (⑪) (사슬 = 실제 `sv_assess`) · ★ 10-23 판정을 보는 자리 (① ② ③ ④ ⑪) = 증서 켠 런 (사슬 판정 = 증서 구간 · 증서
         없는 런 = 진단 → SV_UNCHECKED)
  QD3    ★ 10-23 (Codex 재검토 RCA2-01 · 04 · 1저자 Q1 (가)) SV 문턱 = 증서 구간 판정 — 판정문 실제 반례 꼴 (SVX · 첫 선형 해에만 +1e-8 ·
         나머지 직접해 · 실제 생산자 → 투영 → 검증기 → 사슬): nominal < 문턱 < 증서 구간 아래 끝 → SV_DEPENDENT (옛 = 표지 없음) · 정확 풀이
         구간 ∋ 손 회로 참 비 · +∞ = 영값 위상 증서 · 증서 없는 런 = 진단 (SV_UNCHECKED · uncertified) · 괄호 회로 구간 ∋ 손 참 비 · 한 끝
         증서 실패 = 위 끝 못 읽음 · 실제 기록 변이 (증서 없음 · 외부 증서 · 임의 규칙 · 제거 수 · 10^400 · census · I_bot_code · fp · 판정
         근거 칸 · 지위) = 거부 · 진단 + 무증서 = 받음 (판정 입력 아님)
  KBND   (05 · 한계 기록) k 경계 (90° → 89.99°) σ 뜀 크기 = 생산 단위 R_j 1e2 · 1e4 · 1e6 에서 −0.98 % · −2.1e-4 · −2.1e-6 (± 10 % · ∝ 1/R_j)
  MUT-RCA2 새 보장 변이 (조각 = fid 규칙 · 포트 옮김 · SV 전부 끊음 · 이음매 별칭 끔 · 바닥 = s > D 만 · ★ 10-22 못 가른 다리 지킴 끔 = 2 회차
         변이 J1 → QD2 ④ · '지남' 에 덮임 · 같은 성분 조건 뺌 = 2 회차 변이 J2 → QD2 ⑤ (훅 `_sv_passes`)) 가 위 시험에 옳은 이유로 걸린다 ·
         변이 안 예외 = 하네스 실패
  FLOOR  (Q-B) 같은 조각 쌍의 바닥 = s > D · s > (π/2)·d — L 자 90° 모서리 = 어느 s_min (없음 · 0) 에서도 자기 후보 0 · 날카로운 V = 후보
  (변이 시험 다지기 · 10-21) KINK KU s_min 없음 L_c 손 값 (자기 L_c = 접합 쌍만) · RING 닫힌 머리핀 = 자기 하나 (쌍 무리 고리 둘레) ·
         CEN 재방문 사이 덮인 위치 = 경로 끊김 (경로로만 아님) · KINK U 분산판 맞은편 = 등분점 선분의 접합 짝 위 (L_par 0.25 · 손 값)
  MUT-RCA (09) 반사실 변이 = 생산 서명 (certify= · ★ 10-22 backend=) · 변이 안 예외 (`_try` 가 삼킨 것 포함) = 하네스 실패 (옳은 이유 아님)
"""
import argparse
import ast
import contextlib
import hashlib
import importlib.util
import io
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, 'scripts')
sys.path.insert(0, SCRIPTS)

BASE_COMMIT = 'd1768cf0c'          # 끔 비트 동일의 기준 (이 묶음 전 원격 HEAD)

S3 = None
CJ = None
QUICK = False
_ok, _fail = 0, []


def chk(name, cond, why=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'  ({why})' if why else ''))
    return bool(cond)


CASES = []


def case(tag):
    def deco(fn):
        CASES.append((tag, fn))
        return fn
    return deco


def quiet(fn, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*a, **k)


_CG_CALLS = [0]


@contextlib.contextmanager
def direct_solver():
    """작은 픽스처 = 직접 풀이 (기계 정밀도) — 조립 · 항등식을 CG 허용오차 없이 본다.  생산 경로 아님."""
    from scipy.sparse.linalg import spsolve
    old = S3._solve_cg

    def _direct(L, b, *a, **k):
        _CG_CALLS[0] += 1
        return spsolve(L.tocsc(), b), 0
    S3._solve_cg = _direct
    try:
        yield
    finally:
        S3._solve_cg = old


def raises(fn, exc=(ValueError, TypeError)):
    try:
        quiet(fn)
    except exc:
        return True
    except Exception:                                      # noqa: BLE001 — 다른 예외 = 거부 계약 위반
        return False
    return False


# ═════════════════════════ 픽스처 도구 ═════════════════════════
H = 1.0
RF = 0.5
TOL = 0.1
LPAR = 2.0 * (RF + RF)
RPORT = 2.0
SV = 100.0                       # σ_VGCF (S/cm)
G_AX = SV * H                    # 축방향 면 g (코드 단위)
G_PL = SV * H * H / (0.5 * H)    # 판 결합 g (셀 중심이 판에서 h/2)


def sig_e(s_vgcf=SV, s_am=0.010, s_sdcp=250.0):
    return S3.electronic_sigma_table(s_am, s_am * 0.5, s_vgcf, 10.0, s_sdcp)


def densify(verts, step=0.25):
    """꼭짓점 폴리라인 → 간격 ≤ step 인 점열 (끊기 규칙 gap_tol·중앙값 에 걸리지 않게 거의 고른 간격)."""
    V = np.asarray(verts, np.float64)
    out = [V[0]]
    for a, b in zip(V[:-1], V[1:]):
        n = max(1, int(math.ceil(np.linalg.norm(b - a) / step - 1e-12)))
        for i in range(1, n + 1):
            out.append(a + (b - a) * (i / n))
    return np.asarray(out)


def rows(polys, phase=2, kind=1, fid0=10, fid_step=10, step=0.25, fids=None):
    """폴리라인들 → (add_pts, add_phase, add_fid, add_kind) — fid 마다 행이 붙어 있다 (생산 규약)."""
    P, PH, F, K = [], [], [], []
    for i, v in enumerate(polys):
        pts = densify(v, step) if len(v) > 1 else np.asarray(v, np.float64)
        f = fids[i] if fids is not None else fid0 + fid_step * i
        P.append(pts); PH.append(np.full(len(pts), phase)); F.append(np.full(len(pts), f)); K.append(np.full(len(pts), kind))
    return (np.vstack(P), np.concatenate(PH).astype(np.int64), np.concatenate(F).astype(np.int64),
            np.concatenate(K).astype(np.int64))


def cat_rows(*rs):
    return tuple(np.concatenate([r[i] for r in rs]) for i in range(4))


NO_AM = (np.zeros((0, 3)), np.zeros(0), np.zeros(0, np.int64))


def bed(addr, n, am=NO_AM, stamp=None, vox=H, lo=(0.0, 0.0, 0.0), **kw):
    """격자 (sid, pid) — 생산 `rasterize` (선분 스탬프).  stamp = 스탬프할 행 마스크 (None = 전부) — face_alpha 침대는 PTFE 를 뺀다.
    lo = 상자 원점 (원점 이동 불변 시험 · 격자는 lo 기준이라 sid 는 같아야 한다)."""
    P, PH, F, K = addr
    m = np.ones(len(P), bool) if stamp is None else stamp
    lo = tuple(float(x) for x in lo)
    hi = tuple(lo[i] + float(n[i]) * vox for i in range(3))
    sid, pid = S3.rasterize(am[0], am[1], am[2], P[m], PH[m], lo, hi, vox, add_fid=F[m], add_kind=K[m], **kw)
    return sid, pid


S_MIN = 3.0                      # 꺾임 자기 접합 거르기 문턱 s_min [µm · fixture 단위] — 시험 명시 값 (생산 숫자 = S0 단계 1 뒤 R §2-1)


def _cj_has_smin():
    import inspect
    try:
        return 's_min_um' in inspect.signature(CJ.cjunc_registry).parameters
    except (TypeError, ValueError, AttributeError):
        return False


def reg_kw(kw):
    """cjunc_registry 문턱 키워드 — s_min_um 은 필수 (기본값 없음) 라 시험은 명시 값을 넘긴다.
    ⚠ 고치기 전 코드 (61b6a9ec5 · s_min 인자 없음) 에서는 그 키만 빼고 부른다 — 그 결손은 SMIN 시험이 따로 잡고, 나머지 시험은
      서명 오류로 한꺼번에 무너지지 않고 **각자의 이유**로 통과 · 실패한다 (반례 수 ≠ 검사 수 · SELF-124).  고친 코드에서는 늘 넘긴다."""
    k = dict(kw)
    if 's_min_um' in k and not _cj_has_smin():
        k.pop('s_min_um')
    return k


def registry(sid, addr, vox=H, lo=(0.0, 0.0, 0.0), **kw):
    P, PH, F, K = addr
    k = dict(r_f_um=RF, tol_ff_um=TOL, L_par_um=LPAR, r_port_um=RPORT, gap_tol=2.0, s_min_um=S_MIN)
    k.update(kw)
    return quiet(CJ.cjunc_registry, sid, tuple(float(x) for x in lo), vox, P, PH, F, K, **reg_kw(k))


def plan(reg, rj, **kw):
    k = dict(unreg_law='cut', ptfe_stamp='off')
    k.update(kw)
    return CJ.cjunc_plan(reg, rj, **k)


def solve(sid, sig, n, cj=None, vox=H, **kw):
    with direct_solver():
        return quiet(S3.solve_sigma_z, sid, sig, vox, z_top_um=float(n[2]) * vox, z_bot_um=0.0, cjunc=cj, **kw)


def solve_legacy(sid, sig, n, vox=H, **kw):
    with direct_solver():
        return quiet(S3.solve_sigma_z, sid, sig, vox, z_top_um=float(n[2]) * vox, z_bot_um=0.0, **kw)


def I_of(res, n, vox=H):
    """해 → 단자 전류 (코드 단위 · ΔV = 1) = σ_eff · A / L.  조기 반환 해 (판 칸 없음 · σ 0) = 0."""
    if 'plate_z_um' not in res:
        return float(res.get('sigma_eff', 0.0))
    zb, zt = res['plate_z_um']
    return res['sigma_eff'] * (n[0] * n[1] * vox * vox) / (zt - zb)


def chain_I(gs):
    return 1.0 / sum(1.0 / g for g in gs)


def ref_I(nn, edges, bot, top):
    """손으로 세운 회로 (독립 기준) — 노드 nn 개 · edges = [(i, j, g)] · bot/top = [(i, g)] · ΔV = 1 → 아래 판 전류.
    어느 간선 · 판에도 안 쓰인 노드 (축약으로 합쳐 사라진 노드) 는 빼고 푼다 (특이 방지 · 전류 0 이라 값 불변)."""
    used = sorted({i for i, _, _ in edges} | {j for _, j, _ in edges} | {i for i, _ in bot} | {i for i, _ in top})
    if len(used) < nn:
        m = {v: k for k, v in enumerate(used)}
        return ref_I(len(used), [(m[i], m[j], g) for i, j, g in edges], [(m[i], g) for i, g in bot],
                     [(m[i], g) for i, g in top])
    L = np.zeros((nn, nn)); b = np.zeros(nn)
    for i, j, g in edges:
        L[i, i] += g; L[j, j] += g; L[i, j] -= g; L[j, i] -= g
    for i, g in bot:
        L[i, i] += g; b[i] += g
    for i, g in top:
        L[i, i] += g
    phi = np.linalg.solve(L, b)
    return float(sum(g * (1.0 - phi[i]) for i, g in bot))


def rel(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


def rjc(rj):
    """R_j [Ω] → 코드 단위 저항 (1/g · g = 1e4/R_j)."""
    return rj / 1.0e4


# ── 픽스처 정의 (꼭짓점 = 셀 중심 · µm) ──
#  F1 cross_shared: A 위로 (1,1,0..3) 끝 · B 는 A 끝점에서 +x 로 (1..4,1,3) 뒤 +z 로 (4,1,4..7) → 교차 셀 (1,1,3) = 멤버십 둘
F1_N = (6, 3, 8)
F1 = [[(1.5, 1.5, 0.5), (1.5, 1.5, 3.5)],
      [(1.5, 1.5, 3.5), (4.5, 1.5, 3.5), (4.5, 1.5, 7.5)]]
F1_I = lambda rj: chain_I([G_PL] + [G_AX] * 3 + ([1e4 / rj] if rj != 0 else []) + [G_AX] * 7 + [G_PL])   # noqa: E731
#  F2 cross_face: A (1,1,0..3) · B (2,1,3..7) — A 끝 ↔ B 시작 중심선 거리 1.0 (= r_A + r_B) · 면 (1,1,3)|(2,1,3)
F2_N = (5, 3, 8)
F2 = [[(1.5, 1.5, 0.5), (1.5, 1.5, 3.5)], [(2.5, 1.5, 3.5), (2.5, 1.5, 7.5)]]
#  F3 cross_edge: A 기둥 (1,1) · B 기둥 (2,2) — 모서리 인접 (옛 단절) · 중심선 거리 0.1414
F3_N = (4, 4, 8)
F3 = [[(1.95, 1.95, 0.5), (1.95, 1.95, 3.5)], [(2.05, 2.05, 3.5), (2.05, 2.05, 7.5)]]
#  F4 pass_through: A 전 높이 (1,1,0..7) · B 가로 (0..4,1,3) 가 교차 셀 (1,1,3) 을 지난다 (B = 매달린 가지)
F4_N = (6, 3, 8)
F4 = [[(1.5, 1.5, 0.5), (1.5, 1.5, 7.5)], [(0.5, 1.5, 3.5), (4.5, 1.5, 3.5)]]
#  F5 series: A (1,1,0..2) → B (2,2,2..4) → C (1,1,4..7) — 접합 둘 (모서리 인접 끝–끝)
F5_N = (4, 4, 8)
F5 = [[(1.95, 1.95, 0.5), (1.95, 1.95, 2.5)], [(2.05, 2.05, 2.5), (2.05, 2.05, 4.5)],
      [(1.95, 1.95, 4.5), (1.95, 1.95, 7.5)]]
#  F6 two_sites: A (1,1,0..4) 아래 판 · B 는 (2,1,1) 에서 A 에 닿고 돌아 (2,1,4) 에서 다시 닿은 뒤 위로 (2,1,4..8) 위 판
F6_N = (6, 3, 9)
F6 = [[(1.5, 1.5, 0.5), (1.5, 1.5, 4.5)],
      [(2.5, 1.5, 1.5), (4.5, 1.5, 1.5), (4.5, 1.5, 4.5), (2.5, 1.5, 4.5), (2.5, 1.5, 8.5)]]
#  F10 site_cut: F6 의 둘째 자리를 x 2.9 로 — 셀은 면 인접 (2,1,4)|(1,1,4) 인데 중심선 거리 1.4 > 1.1 (미등록)
F10 = [[(1.5, 1.5, 0.5), (1.5, 1.5, 4.5)],
       [(2.5, 1.5, 1.5), (4.5, 1.5, 1.5), (4.5, 1.5, 4.5), (2.9, 1.5, 4.5), (2.9, 1.5, 8.5)]]
#  K3 crossing_k3 (T1-8): 한 셀 (2,2,2) 에서 세 가닥 직교 교차
K3_N = (5, 5, 5)
K3 = [[(2.5, 2.5, 0.5), (2.5, 2.5, 4.5)], [(0.5, 2.5, 2.5), (4.5, 2.5, 2.5)], [(2.5, 0.5, 2.5), (2.5, 4.5, 2.5)]]
#  T110 self_contact (T1-10): 같은 fid 가 돌아와 (1,1,1)|(2,1,1) 면으로 닿는다 (경로 호 길이 s = 7 > S_MIN)
T110_N = (5, 5, 8)
T110 = [[(1.5, 1.5, 0.5), (1.5, 1.5, 3.5), (3.5, 1.5, 3.5), (3.5, 1.5, 1.5), (2.5, 1.5, 1.5), (2.5, 3.5, 1.5),
         (2.5, 3.5, 7.5)]]

# ── 길이 법칙 v0 픽스처 (J8 대체 · 1저자 10-20 밤 Q17) ──
#  LX 깊은 직교 교차: A (1,1,0..5) 아래 판 · B 가로 (0..4,1,3) 뒤 위로 (4,1,3..7) 위 판 — 중심선이 (1.5,1.5,3.5) 에서 만난다 (d0 = 0) ·
#     닿음 길이 = 각 가닥 2·(r_A + r_B) = L_par 정확히 → 배율 1 · 회로 = 판 + A 3 면 + 접합 + B 7 면 + 판
LX_N = (6, 3, 8)
LX = [[(1.5, 1.5, 0.5), (1.5, 1.5, 5.5)], [(0.5, 1.5, 3.5), (4.5, 1.5, 3.5), (4.5, 1.5, 7.5)]]
LX_I = lambda rj: chain_I([G_PL] + [G_AX] * 3 + [1e4 / rj] + [G_AX] * 7 + [G_PL])   # noqa: E731
#  LP 나란한 두 섬유: A (1,1,0..7) 아래 판 · B (2,1,2..10) 위 판 · 중심선 거리 0.6 (< r_A + r_B = 1) · 겹침 z [2.5, 7.7] = 5.2 →
#     닿음 길이 = 겹침 + √(1 − 0.6²) = 5.2 + 0.8 = 6.0 = 3 L_par (A 는 아래로 · B 는 위로 0.8 더 닿는다) → 배율 3 ·
#     포트는 같은 높이 (평행 최근접점 · 동률 = 같은 방향 규칙) → 회로 = 판 + 섬유 10 면 + 접합 1/(3/R_j,0) + 판.
#     ⚠ 거리를 정확히 r_A + r_B (1.0) 로 두면 닿음 경계가 접선이라 (거리 = √(1 + δ²)) sqrt 반올림이 δ ≲ 1.5e-8 을 닿음으로 세어
#       L_c = 6 + 1.8e-8 (구현 B 실측 · 고치기 전 실행) — 기계 정밀도 회로 대조가 깨진다.  0.6 이면 경계가 횡단 (기울기 0.8) 이다.
LP_N = (5, 3, 11)
LP = [[(1.5, 1.5, 0.5), (1.5, 1.5, 7.7)], [(2.1, 1.5, 2.5), (2.1, 1.5, 10.5)]]
LP_I = lambda rj, m=3.0: chain_I([G_PL] + [G_AX] * 10 + [m * 1e4 / rj] + [G_PL])   # noqa: E731
#  KU U 자로 접힌 한 섬유: 다리 1 위로 (1,1,0..4) · 위 가로 · 다리 2 아래로 (x 2.5 → 2.3 기울어 다리 1 에 다가간다 · (2,1,4..1)) ·
#     아래 가로 (2..4,1,1) · 다리 3 위로 (4,1,1..7) 위 판.  다리 1 ↔ 다리 2 = 같은 fid 비연속 면 셋 (z 1 · 2 · 3) = 자기 접합 후보 하나.
#     두 최근접점 = (1.5,1.5,1.5) ↔ (2.3,1.5,1.5) (거리 0.8 · 유일) → 경로 호 길이 s = 3 + 1 + √(0.2² + 3²)
KU_N = (6, 3, 8)
KU = [[(1.5, 1.5, 0.5), (1.5, 1.5, 4.5), (2.5, 1.5, 4.5), (2.3, 1.5, 1.5), (4.5, 1.5, 1.5), (4.5, 1.5, 7.5)]]
KU_S = 3.0 + 1.0 + math.sqrt(0.2 ** 2 + 3.0 ** 2)
#  KW 같은 U 인데 다리 2 가 x 2.7 (중심선 거리 1.2 > r_f + r_f) — 셀은 면으로 닿지만 중심선은 닿지 않는다 → 자기 L_c (닿음) = 0
#  ★ 10-21 (PRE-impl-02 · Q-B) — 중심선 1.2 > D (2 r_f + tol_ff = 1.1) = 자기 접합 후보조차 아니다 (서로 다른 섬유와 같은 탐지) ·
#    다리 사이 면 = 미등록 법칙 (KW_SMIN 1.0 — 세 면의 경로 호 간격 6.2 · 4.2 · 2.2 가 모두 연속 문턱 위 = 융합 아님)
KW = [[(1.5, 1.5, 0.5), (1.5, 1.5, 4.5), (2.7, 1.5, 4.5), (2.7, 1.5, 1.5), (4.5, 1.5, 1.5), (4.5, 1.5, 7.5)]]
KW_SMIN = 1.0
#  XC 자기 교차 (★ 10-21 · Q-B — 쌍마다 s 규칙의 손 회로용): 다리 1 위로 (1,1,0..4) → +y (z 4.5) → +x 0.8 → 아래로 (x 2.3 · y 4.5 · z 2.5 까지)
#     → −y (x 2.3 · z 2.5) 로 다리 1 위를 0.8 떨어져 수직으로 지나간다 (교차 접점 (1.5,1.5,2.5) ↔ (2.3,1.5,2.5) · 셀 (1,1,2) · (2,1,2)) →
#     (2.3, 0.5, 2.5) 에서 위로 위 판.  교차 쌍의 경로 호 길이 s = 10.8 (손) · 닿음 길이 = 각 가닥 2·√(1 − 0.8²) = 1.2 ≤ L_par → 배율 1 · k 1 ·
#     비연속 면 = (1,1,2)|(2,1,2) 하나 (셀 열 20 · 재방문 없음).  모서리 쌍 (s ≤ √2·D 남짓) 은 s_min 5 · 15 에서 연속.
XC_N = (5, 6, 8)
XC = [[(1.5, 1.5, 0.5), (1.5, 1.5, 4.5), (1.5, 4.5, 4.5), (2.3, 4.5, 4.5), (2.3, 4.5, 2.5), (2.3, 0.5, 2.5), (2.3, 0.5, 7.5)]]
XC_S = 2.0 + 0.8 + 2.0 + 3.0 + 3.0           # 교차 접점 사이 호: 다리 1 남은 2.0 + y 3.0 + x 0.8 + 아래 2.0 + −y 3.0 = 10.8
XC_LC = 2.0 * math.sqrt(1.0 - 0.8 ** 2)       # 1.2
XC_A = [(1.5, 1.5, 0.5), (1.5, 1.5, 4.5)]                                # 나눈 꼴 (서로 다른 섬유 · 교차 둘레만 같은 기하)
XC_B = [(2.3, 4.5, 2.5), (2.3, 0.5, 2.5), (2.3, 0.5, 7.5)]


def seq_cells(verts, vox=H):
    """폴리라인 → 셀 열 (연속 중복 제거) — 기대 회로를 세우는 독립 도구 (생산 스탬프와 같은 원시 함수 `segment_cells`)."""
    from fibre_segment_raster import segment_cells
    pts = densify(verts)
    cs = np.vstack([segment_cells(pts[i], pts[i + 1], vox) for i in range(len(pts) - 1)])
    keep = np.ones(len(cs), bool)
    keep[1:] = np.any(cs[1:] != cs[:-1], axis=1)
    return [tuple(int(v) for v in c) for c in cs[keep]]


# ═════════════════════════ C0 — 끔 비트 동일 ═════════════════════════
def _load_base():
    try:
        src = subprocess.run(['git', '-C', ROOT, 'show', f'{BASE_COMMIT}:scripts/step3_sigma.py'],
                             capture_output=True, check=True).stdout
    except Exception as e:                                 # noqa: BLE001
        return None, f'git show 실패 {type(e).__name__}: {e}'
    d = tempfile.mkdtemp(prefix='s3base_')
    p = os.path.join(d, 'step3_sigma_base_d1768.py')
    with open(p, 'wb') as fh:
        fh.write(src)
    spec = importlib.util.spec_from_file_location('step3_sigma_base_d1768', p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m, ''


def _random_bed(seed, mod, vox=0.25, n=(24, 24, 32)):
    rng = np.random.default_rng(seed)
    box = np.array(n, float) * vox
    na = int(rng.integers(5, 10))
    am_c = rng.uniform([0.5, 0.5, 0.5], box - 0.5, (na, 3)); am_r = rng.uniform(0.7, 1.4, na)
    am_t = rng.integers(1, 3, na)
    polys, ph = [], []
    for _ in range(int(rng.integers(4, 8))):                       # VGCF 경로
        p0 = rng.uniform(0.2, box - 0.2); d = rng.normal(size=3); d /= np.linalg.norm(d)
        p1 = np.clip(p0 + d * rng.uniform(2.0, 5.0), 0.05, box - 0.05)
        polys.append([p0, p1]); ph.append(2)
    for _ in range(2):                                              # PTFE 경로 (centerline 스탬프)
        p0 = rng.uniform(0.2, box - 0.2); d = rng.normal(size=3); d /= np.linalg.norm(d)
        polys.append([p0, np.clip(p0 + 3.0 * d, 0.05, box - 0.05)]); ph.append(4)
    P, PH, F, K = [], [], [], []
    for i, (v, p) in enumerate(zip(polys, ph)):
        pts = densify(v, 0.1)
        P.append(pts); PH.append(np.full(len(pts), p)); F.append(np.full(len(pts), 100 + i)); K.append(np.full(len(pts), 1))
    sd = rng.uniform(0.2, box - 0.2, (int(rng.integers(10, 30)), 3))    # SDCP 점 (구 스탬프)
    P.append(sd); PH.append(np.full(len(sd), 5)); F.append(np.arange(len(sd)) + 500); K.append(np.zeros(len(sd), int))
    P = np.vstack(P); PH = np.concatenate(PH); F = np.concatenate(F); K = np.concatenate(K)
    se = rng.uniform(0, box, (4000, 3))
    sid, pid = mod.rasterize(am_c, am_r, am_t, P, PH, (0., 0., 0.), tuple(box), vox, se_pts=se,
                             sdcp_sphere_d_um=0.5, add_fid=F, add_kind=K, bridge_um=0.3)
    return sid, pid, box


@case('C0')
def t_c0_off_bitid():
    base, why = _load_base()
    if not chk('C0 기준 모듈 (커밋 d1768cf0c 의 step3_sigma) 을 읽었다', base is not None, why):
        return
    nbed = 4 if QUICK else 8
    allsame, n_in = True, 0
    for s in range(nbed):
        sid_b, pid_b, box = quiet(_random_bed, 1000 + s, base)
        sid_c, pid_c, _ = quiet(_random_bed, 1000 + s, S3)
        same_raster = sid_b.tobytes() == sid_c.tobytes() and pid_b.tobytes() == pid_c.tobytes()
        allsame &= same_raster
        te_b = base.electronic_sigma_table(0.010, 0.005, 100.0, 10.0, 250.0)
        ti_b = base.ionic_sigma_table(0.3e-3, 3.0e-3)
        for tab, per in ((te_b, False), (ti_b, False) if s % 2 == 0 else (te_b, True)):
            n_in += 1
            rb = quiet(base.solve_sigma_z, sid_b, tab, 0.25, return_field=True, z_top_um=float(box[2]), z_bot_um=0.0,
                       periodic_xy=per)
            rc = quiet(S3.solve_sigma_z, sid_c, tab, 0.25, return_field=True, z_top_um=float(box[2]), z_bot_um=0.0,
                       periodic_xy=per)
            same = (np.float64(rb['sigma_eff']).tobytes() == np.float64(rc['sigma_eff']).tobytes()
                    and rb['n_dof'] == rc['n_dof'] and rb.get('cg_info') == rc.get('cg_info')
                    and np.float64(rb.get('resid', 0.0)).tobytes() == np.float64(rc.get('resid', 0.0)).tobytes()
                    and (('phi' not in rb and 'phi' not in rc) or rb['phi'].tobytes() == rc['phi'].tobytes())
                    and sorted(rb) == sorted(rc))
            if not same:
                print(f'    C0 차이 seed {1000 + s} per {per}: σ {rb["sigma_eff"]!r} ↔ {rc["sigma_eff"]!r} · '
                      f'키 {sorted(set(rb) ^ set(rc))}')
            allsame &= same
    chk(f'C0 끔 (cjunc=None · 수렴 증서 끔) = 옛 경로 비트 동일 — raster · σ · φ · n_dof · cg_info · resid · 결과 키 ({n_in} 입력)',
        allsame)


# ═════════════════════════ PIECE — 멤버십 셀 = 생산 스탬프 셀 ═════════════════════════
@case('PIECE')
def t_piece():
    rng = np.random.default_rng(7)
    allok = True
    for trial in range(12):
        n = (16, 16, 16); box = np.array(n, float) * 0.5
        polys = []
        for _ in range(5):
            p = [rng.uniform(1, box - 1)]
            for _ in range(int(rng.integers(1, 5))):
                d = rng.normal(size=3); d /= np.linalg.norm(d)
                p.append(np.clip(p[-1] + d * rng.uniform(0.5, 2.5), 0.01, box - 0.01))
            polys.append(p)
        P, PH, F, K = rows(polys, step=0.12)
        if trial % 3 == 0:                                  # 끊기 (gap) 가 걸리는 경로 하나
            m = F == F[0]
            idx = np.flatnonzero(m)
            if len(idx) > 6:
                keep = np.ones(len(P), bool); keep[idx[2:4]] = False
                P, PH, F, K = P[keep], PH[keep], F[keep], K[keep]
        sid, _ = S3.rasterize(*NO_AM, P, PH, (0., 0., 0.), tuple(box), 0.5, add_fid=F, add_kind=K)
        ijk, ph = S3._fibre_segment_ijk(P, PH, F, np.zeros(3), 0.5, np.array(n), 2.0, add_kind=K)
        want = {tuple(c) for c in ijk[ph == 2]}
        try:
            reg = quiet(CJ.cjunc_registry, sid, (0., 0., 0.), 0.5, P, PH, F, K,
                        **reg_kw(dict(r_f_um=0.25, tol_ff_um=0.05, L_par_um=1.0, r_port_um=1.0, gap_tol=2.0, s_min_um=1.5)))
            pos = reg['positions']
            inb = pos['lin'] >= 0
            got = {tuple(int(v) for v in np.unravel_index(int(l), n)) for l in pos['lin'][inb]}
        except Exception as e:                             # noqa: BLE001
            got = None
            print(f'    PIECE trial {trial}: {type(e).__name__}: {e}')
        allok &= (got == want)
    chk('PIECE 멤버십 셀 (상자 안 위치 전부) = `_fibre_segment_ijk` 의 VGCF 셀 (12 무작위 · 끊기 포함 · 같은 끊기 규칙)', allok)


# ═════════════════════════ C1 · T1-7 ═════════════════════════
@case('C1')
def t_c1_cross_shared():
    P = rows(F1)
    sid, _ = bed(P, F1_N)
    reg = registry(sid, P)
    inst = reg['instances']
    chk('C1 instance 하나 (A–B · 교차 셀) · 교차 셀 = 멤버십 둘 (추가 dof 1)',
        len(inst['fi']) == 1 and reg['n_extra_dofs'] == 1, f"n {len(inst['fi'])} extra {reg['n_extra_dofs']}")
    errs, Is = [], []
    for rj in (1.0e1, 1.0e3, 1.0e5):
        r = solve(sid, sig_e(), F1_N, plan(reg, rj))
        Is.append(I_of(r, F1_N)); errs.append(rel(Is[-1], F1_I(rj)))
    chk('C1 σ = 해석 직렬 사슬 판 + A 3 면 + R_j + B 7 면 + 판 (R_j 10 · 1e3 · 1e5 Ω · 1e-12)', max(errs) < 1e-12, f'{errs}')
    chk('C1 Rayleigh — R_j 가 커지면 σ 엄격히 줄어든다 (같은 그래프)', Is[0] > Is[1] > Is[2], f'{Is}')
    pe = r['plate_edges']
    chk('C1 판 간선 원장 = 남은 결합만 (좌표 · g 길이 같음 · 해의 판 전류와 같은 계)',
        all(len(pe[s][0][0]) == len(pe[s][1]) for s in ('bot', 'top')) and r['cjunc']['solved'] is True)
    r0 = solve(sid, sig_e(), F1_N, plan(reg, 0.0, allow_rj_limits=True))
    rl = solve_legacy(sid, sig_e(), F1_N)
    chk('T1-7 R_j → 0 (축약) = 축약 그래프 = 옛 융합 교차 셀 (1e-12)', rel(I_of(r0, F1_N), I_of(rl, F1_N)) < 1e-12
        and rel(I_of(r0, F1_N), F1_I(0)) < 1e-12, f'{I_of(r0, F1_N)} ↔ {I_of(rl, F1_N)}')
    ri = solve(sid, sig_e(), F1_N, plan(reg, math.inf, allow_rj_limits=True))
    chk('T1-7 R_j = ∞ → 가닥 사이 전류 0 (A–B 가 접합으로만 이어진다 → 관통 없음)',
        ri['sigma_eff'] == 0.0 and ri.get('reason') == 'no_through_component', f"{ri.get('reason')} σ {ri['sigma_eff']}")


@case('C2')
def t_c2_face_edge():
    P = rows(F2)
    sid, _ = bed(P, F2_N)
    reg = registry(sid, P)
    rj = 2.0e3
    r = solve(sid, sig_e(), F2_N, plan(reg, rj))
    want = chain_I([G_PL] + [G_AX] * 3 + [1e4 / rj] + [G_AX] * 4 + [G_PL])
    chk('C2a cross_face — 옛 융합 면 절단 + 접합 간선 하나 (해석 사슬 1e-12)', rel(I_of(r, F2_N), want) < 1e-12,
        f'{I_of(r, F2_N)} ↔ {want}')
    rl = solve_legacy(sid, sig_e(), F2_N)
    chk('C2a 옛 경로 = 융합 면 g (대조 · 다른 값)', rel(I_of(rl, F2_N), chain_I([G_PL] + [G_AX] * 8 + [G_PL])) < 1e-12)
    r0 = solve(sid, sig_e(), F2_N, plan(reg, 0.0, allow_rj_limits=True))
    want0 = chain_I([G_PL] + [G_AX] * 3 + [G_AX] * 4 + [G_PL])          # 포트 두 dof 병합 = 그 면이 사라진 사슬
    chk('T1-7 R_j → 0 = 포트 병합 회로 (옛 융합보다 강하다 · 1e-12)', rel(I_of(r0, F2_N), want0) < 1e-12,
        f'{I_of(r0, F2_N)} ↔ {want0}')
    P3 = rows(F3)
    sid3, _ = bed(P3, F3_N)
    reg3 = registry(sid3, P3)
    r3 = solve(sid3, sig_e(), F3_N, plan(reg3, rj))
    rl3 = solve_legacy(sid3, sig_e(), F3_N)
    want3 = chain_I([G_PL] + [G_AX] * 3 + [1e4 / rj] + [G_AX] * 4 + [G_PL])
    chk('C2b cross_edge — 옛 경로 단절 (관통 없음)', rl3['sigma_eff'] == 0.0)
    chk('C2b · J12 접합으로만 이어진 성분을 가지치기가 안 지운다 (해석 사슬 1e-12)', rel(I_of(r3, F3_N), want3) < 1e-12,
        f'{I_of(r3, F3_N)} ↔ {want3}')


@case('C3')
def t_c3_pass_through():
    P = rows(F4)
    sid, _ = bed(P, F4_N)
    reg = registry(sid, P)
    want = chain_I([G_PL] + [G_AX] * 7 + [G_PL])
    Is = [I_of(solve(sid, sig_e(), F4_N, plan(reg, rj, allow_rj_limits=True)), F4_N) for rj in (10.0, 1.0e5, math.inf)]
    chk('C3 · J6 교차 셀을 지나는 가닥 A 는 R_j 와 무관 · R_j = ∞ 에서도 연속 (1e-12)', max(rel(x, want) for x in Is) < 1e-12,
        f'{Is} ↔ {want}')
    chk('C3 교차 셀 = dof 둘 (A · B 각자 축방향 연결)', reg['n_extra_dofs'] == 1, f"{reg['n_extra_dofs']}")


@case('C4')
def t_c4_series_units():
    P = rows(F5)
    sid, _ = bed(P, F5_N)
    reg = registry(sid, P)
    base = [G_PL] + [G_AX] * 2 + [G_AX] * 2 + [G_AX] * 3 + [G_PL]
    rA, rB = 1.0e3, 5.0e3
    IA = I_of(solve(sid, sig_e(), F5_N, plan(reg, rA)), F5_N)
    IB = I_of(solve(sid, sig_e(), F5_N, plan(reg, rB)), F5_N)
    wA = chain_I(base + [1e4 / rA] * 2); wB = chain_I(base + [1e4 / rB] * 2)
    chk('C4 series_chain N = 3 · 접합 둘 — 해석 (1e-12) · 기울기 dR/dR_j = N − 1', rel(IA, wA) < 1e-12 and rel(IB, wB) < 1e-12
        and abs(((1 / IB - 1 / IA) / (rjc(rB) - rjc(rA))) - 2.0) < 1e-9, f'{IA} {wA} · {IB} {wB}')
    old = CJ.junction_g_code
    detected = []
    for nm, fn in (('1e4 빠짐', lambda r: 1.0 / r), ('×1e8', lambda r: 1.0e12 / r)):
        CJ.junction_g_code = fn
        try:
            Im = I_of(solve(sid, sig_e(), F5_N, plan(reg, rA)), F5_N)
            detected.append(rel(Im, wA) > 1e-6)
        except Exception:                                  # noqa: BLE001
            detected.append(True)
        finally:
            CJ.junction_g_code = old
    chk('C4 단위 변이 (1e4 빠짐 · ×1e8) 를 해석 대조가 잡는다', all(detected), f'{detected}')


@case('C5')
def t_c5_instances():
    P = rows(F5)
    sid, _ = bed(P, F5_N)
    reg = registry(sid, P)
    I0 = I_of(solve(sid, sig_e(), F5_N, plan(reg, 1e3)), F5_N)
    Pf = rows(F5, step=0.11)                                       # 같은 접촉을 더 잘게 (조각 수 ↑)
    sidf, _ = bed(Pf, F5_N)
    regf = registry(sidf, Pf)
    If = I_of(solve(sidf, sig_e(), F5_N, plan(regf, 1e3)), F5_N)
    chk('C5 · J2c 조각을 잘게 해도 instance 수 · σ 같다', len(regf['instances']['fi']) == len(reg['instances']['fi']) == 2
        and rel(If, I0) < 1e-12 and sidf.tobytes() == sid.tobytes(), f"{len(regf['instances']['fi'])} {If} {I0}")
    Pr = rows([F5[2], F5[0], F5[1]], fids=[30, 10, 20])            # 섬유 순서 바꿈 (fid 그대로)
    sidr, _ = bed(Pr, F5_N)
    regr = registry(sidr, Pr)
    Ir = I_of(solve(sidr, sig_e(), F5_N, plan(regr, 1e3)), F5_N)
    Pv = rows([v[::-1] for v in F5])                               # 점 역순
    sidv, _ = bed(Pv, F5_N)
    regv = registry(sidv, Pv)
    Iv = I_of(solve(sidv, sig_e(), F5_N, plan(regv, 1e3)), F5_N)
    chk('C5 · J2c 섬유 순서 · 점 역순에 instance 수 · σ 불변 (1e-12)',
        len(regr['instances']['fi']) == 2 and len(regv['instances']['fi']) == 2 and rel(Ir, I0) < 1e-12 and rel(Iv, I0) < 1e-12,
        f'{Ir} {Iv} {I0}')
    P6 = rows(F6)
    sid6, _ = bed(P6, F6_N)
    reg6 = registry(sid6, P6)
    chk('C5 같은 쌍 떨어진 두 곳 = instance 둘 (쌍 ID 로 접지 않는다)', len(reg6['instances']['fi']) == 2
        and len(set(zip(reg6['instances']['fi'].tolist(), reg6['instances']['fj'].tolist()))) == 1, f"{reg6['instances']['fi']}")


def _f6_reference(rj, sv=SV, second_site=True, fused_second=False):
    """F6/F10 사다리 — 노드: A (1,1,0..4) = 0..4 · B 셀 열 = 5.. · 접합 자리 1: A1 ↔ B0 · 자리 2: A4 ↔ B (2,1,4)."""
    A = [(1, 1, k) for k in range(5)]
    Bc = seq_cells(F6[1] if not fused_second else F10[1])
    nA = len(A)
    gax = sv * H; gpl = sv * H * H / (0.5 * H)
    E = [(i, i + 1, gax) for i in range(nA - 1)] + [(nA + i, nA + i + 1, gax) for i in range(len(Bc) - 1)]
    jB0 = nA + Bc.index((2, 1, 1)); jB4 = nA + Bc.index((2, 1, 4))
    E.append((1, jB0, 1e4 / rj))
    if second_site:
        E.append((4, jB4, gax if fused_second else 1e4 / rj))
    bot = [(0, gpl)]; top = [(nA + len(Bc) - 1, gpl)]
    return ref_I(nA + len(Bc), E, bot, top)


@case('T1-6')
def t_t16_multi():
    P = rows(F6)
    sid, _ = bed(P, F6_N)
    reg = registry(sid, P)
    rj = 3.0e3
    r6 = solve(sid, sig_e(), F6_N, plan(reg, rj))
    I = I_of(r6, F6_N)
    want = _f6_reference(rj)
    chk('T1-6 두 자리 사다리 회로 (손으로 세운 기준 · 1e-12)', rel(I, want) < 1e-12, f'{I} ↔ {want}')
    jI = r6['_cjunc']['junction_current_code']
    chk('T1-6 원장 — instance 마다 접합 전류 · 두 자리 합 = 단자 전류 (A → B 는 접합으로만 · 1e-10)',
        len(jI) == 2 and np.all(np.isfinite(jI)) and rel(float(np.sum(np.abs(jI))), I) < 1e-10, f'{jI} {I}')
    big = sig_e(s_vgcf=1.0e9)
    Ib = I_of(solve(sid, big, F6_N, plan(reg, rj)), F6_N)
    chk('T1-6 등전위 극한 (σ 1e9) — R → R_j/2 (상대 1e-5)', rel(1.0 / Ib, rjc(rj) / 2.0) < 1e-5, f'{1 / Ib} ↔ {rjc(rj) / 2}')


@case('T1-8')
def t_t18_k3():
    n = K3_N
    P = rows(K3)
    sid, _ = bed(P, n)
    reg = registry(sid, P)
    inst = reg['instances']
    pos = reg['positions']
    ok_ports = True
    for k in range(len(inst['fi'])):
        pi, pj = int(inst['port_i'][k]), int(inst['port_j'][k])
        ok_ports &= (pi >= 0 and pj >= 0 and pi != pj and pos['lin'][pi] == pos['lin'][pj])
    chk('T1-8 한 셀 세 가닥 → 추가 dof 2 · instance 3 (쌍마다) · J9 포트 = 같은 셀 · 서로 다른 dof',
        reg['n_extra_dofs'] == 2 and len(inst['fi']) == 3 and ok_ports, f"extra {reg['n_extra_dofs']} n {len(inst['fi'])}")
    want = chain_I([G_PL] + [G_AX] * 4 + [G_PL])
    Is = [I_of(solve(sid, sig_e(), n, plan(reg, rj, allow_rj_limits=True)), n) for rj in (1.0, 1e6, math.inf)]
    chk('T1-8 축 연결이 각자 fid 로 — 세로 가닥 σ 가 R_j 와 무관 (1e-12)', max(rel(x, want) for x in Is) < 1e-12, f'{Is} {want}')


@case('T1-9')
def t_t19_fiber_sphere():
    P = rows([[(0.0, 0.0, -1.0), (0.0, 0.0, 1.0)]], step=0.1)
    am_c = np.array([[2.12, 0.0, 0.0]]); am_r = np.array([2.0])
    n0 = CJ.va_census(P[0], P[1], P[2], P[3], am_c, am_r, r_f_um=0.075, tol_fs_um=0.0, gap_tol=2.0)
    am_c2 = np.array([[2.07, 0.0, 0.0]])
    n1 = CJ.va_census(P[0], P[1], P[2], P[3], am_c2, am_r, r_f_um=0.075, tol_fs_um=0.0, gap_tol=2.0)
    chk('T1-9 J2b 섬유–구 = 중심선 ↔ 구 중심 ≤ r_f + R_AM + tol_fs — d 2.12 = 접촉 아님 (2.15 문자식 오판 아님) · d 2.07 = 접촉',
        n0 == 0 and n1 == 1, f'{n0} {n1}')


@case('T1-10')
def t_t110_self():
    n = T110_N
    poly = T110
    P = rows(poly)
    sid, _ = bed(P, n)
    reg = registry(sid, P)
    inst = reg['instances']
    nself = int(np.sum(inst['self']))
    chk('T1-10 같은 fid 비연속 두 셀 면 → 자기 접합 instance (f, f) 하나', nself == 1 and len(inst['fi']) == 1,
        f"self {nself} n {len(inst['fi'])}")
    seq = seq_cells(poly[0])
    k1, k8 = seq.index((1, 1, 1)), seq.index((2, 1, 1))
    rj = 4.0e3
    E = [(i, i + 1, G_AX) for i in range(len(seq) - 1)] + [(k1, k8, 1e4 / rj)]
    want = ref_I(len(seq), E, [(0, G_PL)], [(len(seq) - 1, G_PL)])
    I = I_of(solve(sid, sig_e(), n, plan(reg, rj)), n)
    chk('T1-10 자기 접합 = R_j 간선 (0 저항 지름길 아님 · 사다리 기준 1e-12)', rel(I, want) < 1e-12, f'{I} ↔ {want}')
    Ii = I_of(solve(sid, sig_e(), n, plan(reg, math.inf, allow_rj_limits=True)), n)
    wi = chain_I([G_PL] + [G_AX] * (len(seq) - 1) + [G_PL])
    chk('T1-10 R_j = ∞ → 우회로 전부 (면 지름길 없음 · 1e-12)', rel(Ii, wi) < 1e-12, f'{Ii} ↔ {wi}')


@case('T1-11')
def t_t111_tie():
    #  A 아래 판 (1,1,0..5) · B 는 A 옆 x 2.5 · z = 3.0 (셀 경계) 에서 시작해 +x 뒤 위 판 — A 의 접점 (1.5,1.5,3.0) 은 A 의 두 셀
    #  (1,1,2) · (1,1,3) 중심에서 등거리 (0.5) → 동률.  B 가 전류를 나르므로 어느 포트냐가 회로를 바꾼다 (판별력).
    n = (6, 3, 8)
    polys = [[(1.5, 1.5, 0.5), (1.5, 1.5, 5.5)], [(2.5, 1.5, 3.0), (4.5, 1.5, 3.0), (4.5, 1.5, 7.5)]]
    P = rows(polys)
    sid, _ = bed(P, n)
    reg = registry(sid, P)
    inst = reg['instances']
    pos = reg['positions']
    ok = len(inst['fi']) == 1
    tie = int(reg['census'].get('n_port_ties', -1))
    pa = int(inst['port_i'][0]) if ok else -1
    cell = tuple(int(v) for v in np.unravel_index(int(pos['lin'][pa]), n)) if pa >= 0 else None
    chk('T1-11 등거리 두 후보 포트 → 셀 정수 좌표 사전식 최소 (1,1,2) (★ 10-21 RCA-04 — 옛 = 정준 경로 번호) · 동률 수 1 기록',
        ok and tie == 1 and cell == (1, 1, 2), f'tie {tie} cell {cell}')
    rj = 1e3
    I0 = I_of(solve(sid, sig_e(), n, plan(reg, rj)), n)
    want = chain_I([G_PL] + [G_AX] * 2 + [1e4 / rj] + [G_AX] * 6 + [G_PL])
    chk('T1-11 포트 (1,1,2) 회로 = 해석 사슬 (A 2 면 + R_j + B 6 면 · 1e-12)', rel(I0, want) < 1e-12, f'{I0} ↔ {want}')
    Pv = rows([polys[0][::-1], polys[1][::-1]])
    sidv = bed(Pv, n)[0]
    Iv = I_of(solve(sidv, sig_e(), n, plan(registry(sidv, Pv), rj)), n)
    Pr = rows([polys[1], polys[0]], fids=[20, 10])
    sidr = bed(Pr, n)[0]
    Ir = I_of(solve(sidr, sig_e(), n, plan(registry(sidr, Pr), rj)), n)
    chk('T1-11 점 역순 · 섬유 순서에 σ 불변 (동률 규칙이 방향 · 행 순서와 무관 · 1e-12)', rel(Iv, I0) < 1e-12 and rel(Ir, I0) < 1e-12,
        f'{I0} {Iv} {Ir}')


@case('T1-12')
def t_t112_site():
    P = rows(F10)
    sid, _ = bed(P, F6_N)
    reg = registry(sid, P)
    chk('T1-12 같은 쌍 두 자리 중 한 자리만 instance', len(reg['instances']['fi']) == 1, f"{len(reg['instances']['fi'])}")
    rj = 3.0e3
    Ic = I_of(solve(sid, sig_e(), F6_N, plan(reg, rj, unreg_law='cut')), F6_N)
    If = I_of(solve(sid, sig_e(), F6_N, plan(reg, rj, unreg_law='fused')), F6_N)
    wc = _f6_reference(rj, second_site=False, fused_second=True)
    wf = _f6_reference(rj, second_site=True, fused_second=True)
    chk('T1-12 미등록 자리 cut = 첫 자리 접합만 (1e-12) · fused = 첫 자리 접합 + 둘째 자리 융합 면 (1e-12)',
        rel(Ic, wc) < 1e-12 and rel(If, wf) < 1e-12, f'{Ic} {wc} · {If} {wf}')
    chk('T1-12 같은 그래프 Rayleigh: cut ≤ fused', Ic <= If * (1 + 1e-12))
    chk('T1-12 법칙 미선언 = 거부 (자동 fallback 없음)', raises(lambda: CJ.cjunc_plan(reg, rj, unreg_law=None, ptfe_stamp='off')))


@case('T1-5p')
def t_t15_lead():
    P = rows(F1)
    sid, _ = bed(P, F1_N)
    reg = registry(sid, P)
    chk("T1-5′ 단자 기준 R_j (리드 빼기 기록 없음) = 거부", raises(lambda: plan(reg, 1e3, rj_reference='terminal_two_probe')))
    chk("T1-5′ 리드 빼기 기록이 와도 v0 = 거부 (모형 내부값만)", raises(lambda: plan(reg, 1e3, lead_subtraction={'R_leads_ohm': 2.0})))
    chk('T1-5′ 음수 · NaN R_j = 거부', raises(lambda: plan(reg, -1.0)) and raises(lambda: plan(reg, float('nan'))))
    chk('T1-5′ R_j 극한 (0 · ∞) = 사다리 천장 · 바닥 표지 없이 정량 거부', raises(lambda: plan(reg, 0.0)) and raises(lambda: plan(reg, math.inf)))


# ═════════════════════════ 길이 법칙 v0 (J8 대체 · 1저자 10-20 밤 Q17 = 권고대로) ═════════════════════════
#  G_j = max(1, L_c/L_par) / R_j,0 — 긴 접촉 = 점 접합 L_c/L_par 개가 나란히 (선 접촉 협착 ∝ 길이의 1차 근사) · 새 손잡이 없음 ·
#  L_c = 닿음 (두 가닥 각각에서 중심선 거리 ≤ r_fi + r_fj 인 길이의 최댓값 · B 정의) · 간선 = instance 하나 (lumped) ·
#  절단 발자국 = 접촉 run 전체 · 꺾임 자기 접합 = 두 최근접점 사이 경로 호 길이 s < s_min 이면 접합 아님 (옛 복셀 융합 그대로).
#  기대값 = 손으로 세운 회로 · 손으로 잰 길이 (모듈 함수로 정답을 다시 만들지 않는다).
BASE_CJ_COMMIT = '73c640dc2'     # 점 접합 (길이 법칙 전 · 구현 B 끝) — 긴 접촉 없는 침대의 비트 같음 기준
#  ★ 10-22 — 옛 값 61b6a9ec5 는 원격 어느 브랜치에도 없는 SHA 였다 (새로 받은 저장소에서 늘 실패 · SELF-116 부류) →
#    원격의 같은 판 73c640dc2 (길이 법칙 c5a3473d3 앞에서 carbon_junction.py 를 마지막으로 바꾼 커밋) 로 바꿨다.


def _plan_mult(p):
    """계획의 instance 배율 배열 (없으면 None — 고치기 전 코드)."""
    m = p.get('mult') if isinstance(p, dict) else None
    return None if m is None else np.asarray(m, np.float64)


_TRY_EXC = [0]                   # ★ 10-21 (PRE-impl-09) — `_try` 가 삼킨 예외 수 (변이 하네스가 '예외로 잡힘' 을 '옳은 이유' 와 가른다)


def _try(fn, default=math.nan):
    try:
        return quiet(fn)
    except Exception as e:                                 # noqa: BLE001 — 거부 · 예외 = 기대값을 못 냄 (그 검사 실패)
        _TRY_EXC[0] += 1
        print(f'    (예외 {type(e).__name__}: {str(e)[:160]})')
        return default


def _load_base_cj():
    try:
        src = subprocess.run(['git', '-C', ROOT, 'show', f'{BASE_CJ_COMMIT}:scripts/carbon_junction.py'],
                             capture_output=True, check=True).stdout
    except Exception as e:                                 # noqa: BLE001
        return None, f'git show 실패 {type(e).__name__}: {e}'
    d = tempfile.mkdtemp(prefix='cjbase_')
    p = os.path.join(d, 'carbon_junction_base_61b6.py')
    with open(p, 'wb') as fh:
        fh.write(src)
    spec = importlib.util.spec_from_file_location('carbon_junction_base_61b6', p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m, ''


@contextlib.contextmanager
def cj_module(mod):
    """solve_sigma_z 는 호출 때 `import carbon_junction` 을 한다 — 기준 모듈로 풀 때 그 이름을 잠시 바꿔 끼운다."""
    old = sys.modules.get('carbon_junction')
    sys.modules['carbon_junction'] = mod
    try:
        yield
    finally:
        if old is None:
            sys.modules.pop('carbon_junction', None)
        else:
            sys.modules['carbon_junction'] = old


def _chain_edges(nn):
    return [(i, i + 1, G_AX) for i in range(nn - 1)]


@case('LEN-X')
def t_len_cross():
    P = rows(LX)
    sid, _ = bed(P, LX_N)
    reg = registry(sid, P)
    inst = reg['instances']
    chk('LEN-X 깊은 직교 교차 — instance 하나 · d0 = 0 · L_c = L_par = 2(r_A + r_B) (손으로 잰 닿음 길이 · 1e-12)',
        len(inst['fi']) == 1 and abs(float(inst['d0'][0])) < 1e-12 and abs(float(inst['Lc'][0]) - LPAR) < 1e-12,
        f"n {len(inst['fi'])} d0 {inst['d0']} Lc {inst['Lc']}")
    m = _plan_mult(plan(reg, 1e3))
    chk('LEN-X 배율 = 1 정확히 (max(1, L_c/L_par) · 경계 L_c = L_par 에서 연속)', m is not None and len(m) == 1 and m[0] == 1.0,
        f'{m}')
    errs = [rel(_try(lambda rj=rj: I_of(solve(sid, sig_e(), LX_N, plan(reg, rj)), LX_N)), LX_I(rj)) for rj in (1e1, 1e3, 1e5)]
    chk('LEN-X σ = 옛 점 접합 회로 (판 + A 3 면 + R_j + B 7 면 + 판 · R_j 10 · 1e3 · 1e5 Ω · 1e-12)', max(errs) < 1e-12, f'{errs}')


def canon_fids(polys, step=0.25):
    """★ 10-21 (RCA-04 · Q2) — 경로의 기하 정준 순서 (시험 쪽 독립 정의): 점열을 정준 방향 (역순 점열이 사전식으로 작으면 뒤집음) 으로 놓고
    점열 사전식으로 줄 세운 순위 → fid 10 · 20 · … .  옛 코드 (fid 순) 에 이 fid 를 주면 옛 경로 순서 = 새 정준 순서 (번호 효과를 뺀 대조)."""
    keys = []
    for v in polys:
        Q = densify(v, step) if len(v) > 1 else np.asarray(v, np.float64)
        fw = [tuple(map(float, q)) for q in Q]
        bw = fw[::-1]
        keys.append(min(fw, bw))
    order = sorted(range(len(polys)), key=lambda i: keys[i])
    fid = [0] * len(polys)
    for r_, i in enumerate(order):
        fid[i] = 10 * (r_ + 1)
    return fid


@case('LEN-BIT')
def t_len_bitid():
    """긴 접촉 없는 침대 (배율 전부 1) = 구현 B (61b6a9ec5 · 점 접합) 와 σ · n_dof · cg_info · resid · 접합 전류 비트 같음.
    ★ 10-21 (RCA-04 · Q2) — 새 코드는 경로 순서를 fid 가 아니라 기하 정준 순서로 둔다 (fid 무관).  옛 코드 (fid 순) 에는 정준 순위 fid
    (`canon_fids`) 를 준다 — 번호 효과를 뺀 '옛 점 접합 = L_c ≤ L_par 간선' 대조.  새 코드는 원래 fid · 정준 fid 둘 다 같은 비트여야 한다."""
    base, why = _load_base_cj()
    if not chk(f'LEN-BIT 기준 모듈 (커밋 {BASE_CJ_COMMIT} 의 carbon_junction) 을 읽었다', base is not None, why):
        return
    fx = (('F1', F1, F1_N), ('F2', F2, F2_N), ('F3', F3, F3_N), ('F5', F5, F5_N), ('F6', F6, F6_N), ('F10', F10, F6_N),
          ('LX', LX, LX_N), ('K3', K3, K3_N), ('T110', T110, T110_N))
    bad = []
    for nm, polys, n in fx:
        P = rows(polys)
        Pc = rows(polys, fids=canon_fids(polys))
        sid, _ = bed(P, n)
        sidc, _ = bed(Pc, n)
        if sidc.tobytes() != sid.tobytes():
            bad.append(f'{nm}: 정준 fid 침대 sid 다름')
            continue
        for rj in (1e2, 3e3):
            try:
                rn = solve(sid, sig_e(), n, plan(registry(sid, P), rj))
                rnc = solve(sid, sig_e(), n, plan(registry(sid, Pc), rj))
                if not (np.float64(rn['sigma_eff']).tobytes() == np.float64(rnc['sigma_eff']).tobytes()
                        and np.asarray(rn['_cjunc']['junction_current_code']).tobytes()
                        == np.asarray(rnc['_cjunc']['junction_current_code']).tobytes()):
                    bad.append(f'{nm}@{rj:g}: 새 코드 fid 의존')
                kb = dict(r_f_um=RF, tol_ff_um=TOL, L_par_um=LPAR, r_port_um=RPORT, gap_tol=2.0)
                regb = quiet(base.cjunc_registry, sid, (0.0, 0.0, 0.0), H, *Pc, **kb)   # 옛 코드 = 정준 순위 fid (번호 효과 제거)
                pb = base.cjunc_plan(regb, rj, unreg_law='cut', ptfe_stamp='off')
                with cj_module(base):
                    rb = solve(sid, sig_e(), n, pb)
                same = (np.float64(rn['sigma_eff']).tobytes() == np.float64(rb['sigma_eff']).tobytes()
                        and rn['n_dof'] == rb['n_dof'] and rn.get('cg_info') == rb.get('cg_info')
                        and np.float64(rn.get('resid', 0.0)).tobytes() == np.float64(rb.get('resid', 0.0)).tobytes()
                        and np.asarray(rn['_cjunc']['junction_current_code']).tobytes()
                        == np.asarray(rb['_cjunc']['junction_current_code']).tobytes())
            except Exception as e:                         # noqa: BLE001
                same = False
                print(f'    LEN-BIT {nm} R_j {rj}: {type(e).__name__}: {e}')
            if not same:
                bad.append(f'{nm}@{rj:g}')
    chk(f'LEN-BIT 긴 접촉 없는 침대 {len(fx)} 개 × R_j 둘 = 점 접합 (구현 B · 정준 순위 fid) 과 σ · n_dof · cg_info · resid · 접합 전류 '
        f'비트 같음 · 새 코드는 원래 fid = 정준 fid (비트)', not bad, f'{bad}')


@case('LEN-P')
def t_len_parallel():
    P = rows(LP)
    sid, _ = bed(P, LP_N)
    reg = registry(sid, P)
    inst = reg['instances']
    chk('LEN-P 나란한 두 섬유 — instance 하나 · L_c = 6.0 = 3 L_par (손으로 센 겹침 · 1e-12)',
        len(inst['fi']) == 1 and abs(float(inst['Lc'][0]) - 3.0 * LPAR) < 1e-12, f"n {len(inst['fi'])} Lc {inst['Lc']}")
    m = _plan_mult(plan(reg, 1e3))
    chk('LEN-P 배율 = max(1, L_c/L_par) = 3 (1e-12)', m is not None and len(m) == 1 and abs(m[0] - 3.0) < 1e-12, f'{m}')
    errs = []
    for rj in (1e1, 1e3, 1e5):
        for law in ('cut', 'fused'):
            errs.append(rel(_try(lambda rj=rj, law=law: I_of(solve(sid, sig_e(), LP_N, plan(reg, rj, unreg_law=law)), LP_N)),
                            _lp_ref(rj)))
    #  ★ 10-21 (RCA-05 · Q3 (가)) — 분산판 v0: 옛 기대 (한 포트에 총 3/R_j,0 집중 = `LP_I`) 를 등분 간선 셋 사다리로 바꿨다
    chk('LEN-P σ = 분산판 사다리 회로 (판 + A · B 사슬 + 등분 간선 셋 z 2 · 4 · 6 각 (3/R_j,0)/3 + 판 · R_j 10 · 1e3 · 1e5 Ω · '
        '미등록 cut · fused · 기계 정밀도 1e-12)', max(errs) < 1e-12, f'{errs}')


@case('LEN-O')
def t_len_oblique():
    n = (12, 12, 5)
    C = np.array([6.0, 6.0, 2.5])
    ths = (90.0, 89.9, 80.0, 60.0, 45.0, 30.0)
    ms, n_inst = [], []
    for th in ths:
        u = np.array([math.cos(math.radians(th)), math.sin(math.radians(th)), 0.0])
        polys = [[(2.0, 6.0, 2.5), (10.0, 6.0, 2.5)], [tuple(C - 4.0 * u), tuple(C + 4.0 * u)]]
        P = rows(polys)
        sid, _ = bed(P, n)
        reg = registry(sid, P)
        n_inst.append(len(reg['instances']['fi']))
        m = _plan_mult(plan(reg, 1e3, quantitative=False))
        ms.append(float(m[0]) if m is not None and len(m) == 1 else math.nan)
    want = [1.0 / math.sin(math.radians(t)) for t in ths]     # 깊은 교차 (d0 = 0) · 각 θ: 닿음 길이 = 2(r_i + r_j)/sin θ
    chk('LEN-O 비스듬한 깊은 교차 — instance 하나씩 · 배율 = 1/sin θ (손으로 잰 닿음 길이 · 1e-9)',
        n_inst == [1] * len(ths) and all(abs(a - b) <= 1e-9 * b for a, b in zip(ms, want)), f'{n_inst} {ms} ↔ {want}')
    chk('LEN-O 경계 연속 — 직교 (90°) 배율 = 1 정확히 · 89.9° = 1 + (0, 2e-6) (뛰지 않는다)',
        ms[0] == 1.0 and 0.0 < ms[1] - 1.0 < 2e-6, f'{ms[:2]}')
    chk('LEN-O 각도에 단조 — θ 가 작아질수록 배율이 엄격히 커진다 (90 · 89.9 · 80 · 60 · 45 · 30°) · 모두 ≥ 1',
        all(ms[i + 1] > ms[i] for i in range(len(ms) - 1)) and min(ms) >= 1.0, f'{ms}')


@case('LEN-G')
def t_len_gate():
    """배율 기록 ↔ 쓰는 값 결합 — 계획의 배율만 바꾸고 행 지문을 다시 만든 변이 (g 는 옛 값) 는 솔브 입구에서 거부 (CG 0).
    구현과 같은 커밋에서 더한 시험 (자기 리뷰 · 증서 ↔ 결과 결합 부류)."""
    P = rows(LP)
    sid, _ = bed(P, LP_N)
    pl = plan(registry(sid, P), 1e3)
    ok_base = _try(lambda: I_of(solve(sid, sig_e(), LP_N, pl), LP_N)) > 0
    bad = []
    for nm, f in (('배율 ×2', 2.0), ('배율 ×0.5 (< 1)', 0.5)):
        pm = dict(pl)
        pm['mult'] = np.asarray(pl['mult'], np.float64) * f
        pm['fp_rows'] = CJ.plan_rows_fp(pm)
        _CG_CALLS[0] = 0
        rej = raises(lambda pm=pm: solve(sid, sig_e(), LP_N, pm))
        if not (rej and _CG_CALLS[0] == 0):
            bad.append(nm)
    chk('LEN-G 배율만 바꾸고 지문을 다시 만든 계획 (×2 · ×0.5) = 솔브 입구 거부 · CG 0 (정상 계획은 풀린다)', ok_base and not bad,
        f'base {ok_base} 통과한 변이 {bad}')


@case('J8')
def t_j8_long():
    P = rows(LP)
    sid, _ = bed(P, LP_N)
    reg = registry(sid, P)
    cen = reg['census']
    nl = int(np.sum(reg['instances']['long']))
    chk('J8 긴 접촉 (L_c > L_par) = 표지 · 집계 칸 그대로 (instance long · census n_long_distinct · L_c 최댓값)',
        nl == 1 and cen.get('n_long_distinct') == 1 and abs(float((cen.get('Lc_um') or {}).get('max', math.nan)) - 6.0) < 1e-12,
        f"{nl} {cen.get('n_long_distinct')} {cen.get('Lc_um')}")
    pq = plan(reg, 1e3)
    chk('J8 옛 동작 제거 — 긴 접촉이 있어도 정량 계획에 거부 사유 없음 (long_contact · 길이 법칙이 그 자리를 맡는다)',
        not pq['rejections'], f"{[x['code'] for x in pq['rejections']]}")
    r = _try(lambda: solve(sid, sig_e(), LP_N, pq), None)
    chk('J8 정량 솔브 진행 · 기록 (긴 접촉 수 1 영수증 · solved)',
        r is not None and r['sigma_eff'] > 0 and r['cjunc'].get('n_long') == 1 and r['cjunc'].get('solved') is True)


@case('FOOT')
def t_footprint():
    """절단 발자국 = 접촉 run 전체 — 긴 접촉 위의 A|B 융합 면이 하나라도 남으면 (미등록 법칙 fused) 접합 간선을 병렬로 우회한다."""
    P = rows(LP)
    sid, _ = bed(P, LP_N)
    reg = registry(sid, P)
    ft = reg['faces']
    pos = reg['positions']
    vv = (ft['pa'] >= 0) & (ft['pb'] >= 0)
    fa = np.where(vv, pos['fid'][np.maximum(ft['pa'], 0)], -1)
    fb = np.where(vv, pos['fid'][np.maximum(ft['pb'], 0)], -1)
    pair = vv & (np.minimum(fa, fb) == 10) & (np.maximum(fa, fb) == 20)
    n_site = int(np.sum(pair & (ft['kind'] == CJ.K_CUT_SITE)))
    n_unreg = int(np.sum(pair & (ft['kind'] == CJ.K_UNREG)))
    chk('FOOT 원장 — A|B 접촉 면 6 개 (z 2..7 · 손으로 센 run) 전부 자리 절단 · 미등록 0', n_site == 6 and n_unreg == 0,
        f'site {n_site} unreg {n_unreg}')
    rj = 1e3
    rt = _try(lambda: solve(sid, sig_e(), LP_N, plan(reg, rj, unreg_law='fused', quantitative=False)), None)
    ok_t = (rt is not None and rt['cjunc']['tombstones']['cut_site'] == 6 and rt['cjunc']['n_unreg_fused'] == 0
            and not np.any(rt['_cjunc']['sys']['CAT'] == 2))           # 간선 원장에 vv_unreg_fused (2) 없음
    chk('FOOT 미등록 법칙 fused 에서도 run 위 융합 i|j 면 0 — 면 tombstone 6 · 미등록 융합 0 · 간선 원장에 융합 VV 간선 없음', ok_t)
    I = _try(lambda: I_of(solve(sid, sig_e(), LP_N, plan(reg, rj, unreg_law='fused')), LP_N))
    chk('FOOT fused · 정량 σ = 분산판 사다리 회로 (우회 없음 · 1e-12)', rel(I, _lp_ref(rj)) < 1e-12, f'{I} ↔ {_lp_ref(rj)}')


def _face_kinds(reg, ca, cb):
    """원장 면 표에서 셀 ca ↔ cb (면 인접 · 순서 무관) 의 행 종류 목록 (K_*) — 고치기 전 코드에도 같은 칸 (lin · ax · kind)."""
    ca, cb = (tuple(ca), tuple(cb)) if tuple(ca) < tuple(cb) else (tuple(cb), tuple(ca))
    d = [cb[k] - ca[k] for k in range(3)]
    if sorted(map(abs, d)) != [0, 0, 1] or sum(d) != 1:
        return None
    ax = d.index(1)
    n = reg['shape']
    lin = int(np.ravel_multi_index(ca, n))
    ft = reg['faces']
    m = (ft['lin'] == lin) & (ft['ax'] == ax)
    return sorted(int(k) for k in ft['kind'][m])


@case('KINK')
def t_kink():
    """꺾임 자기 접합 — ★ 10-21 (PRE-impl-02 · 1저자 Q-B): 자기 접합 = 중심선 쌍 d ≤ D (서로 다른 섬유와 같은 탐지) + 같은 조각 쌍마다
    s 규칙 (s ≥ s_min = 진짜 접힘 · 고리 접촉 = 절단 + R_j 간선 · 같은 길이 법칙 · 같은 분산판 / s < s_min = 같은 가닥의 연속 = 면은 옛
    융합 그대로) · 바닥 s > D (늘 · 곧은 가닥의 이웃 쌍은 접합이 아니다) · s_min 없음 + 정량 = 구조화 거부 · 자기 L_c = 닿음 규칙 (중심선).
    접합 꼴 = XC (교차 · s 10.8 · 손 회로) · 연속 꼴 = KU (U 자 · 쌍 s 전부 < 20) · 닿지 않는 꼴 = KW (중심선 1.2 > D → 후보 아님 ·
    다리 사이 면 = 미등록 법칙 — 옛 판 = L_c 0 의 자기 접합 하나 · σ +4.25 %).
    옛 판의 KU 접합 꼴 (s_min = KU_S − 0.5 · 대표 최근접 쌍의 s 하나로 후보 전체를 거름) 은 쌍마다 규칙에서 다리 아래쪽만 남아 (s 가 높이에
    따라 바뀐다) 손 회로가 달라진다 — 그 꼴은 XC 로 옮겼다."""
    rj = 1e3
    P = rows(XC)
    sid, _ = bed(P, XC_N)
    seq = seq_cells(XC[0])
    nn = len(seq)
    i2, i13 = seq.index((1, 1, 2)), seq.index((2, 1, 2))
    lo_ = _try(lambda: registry(sid, P, s_min_um=5.0), None)             # s ≥ s_min → 고리 접촉 (접합)
    hi_ = _try(lambda: registry(sid, P, s_min_um=15.0), None)            # s < s_min → 같은 가닥의 연속
    I = (lo_ or {}).get('instances') or {}
    qs = [q for q in range(len(I.get('fi', []))) if I['self'][q]]
    q = qs[0] if len(qs) == 1 else None
    chk('KINK XC s ≥ s_min (5) — 자기 접합 하나 · s = 교차 접점 사이 경로 호 10.8 · L_c = 닿음 (중심선) 2·√(1 − 0.8²) = 1.2 (손 · 1e-9) · '
        '배율 1 · k 1 · 포트 (1,1,2) · (2,1,2) · 면 (1,1,2)|(2,1,2) = 자기 절단',
        q is not None and abs(float(I['s'][q]) - XC_S) < 1e-9 and abs(float(I['Lc'][q]) - XC_LC) < 1e-9
        and float(I['mult'][q]) == 1.0 and int(np.asarray(I.get('nsub', [0]))[q]) == 1
        and {_pcells(lo_, q, 'i'), _pcells(lo_, q, 'j')} == {(1, 1, 2), (2, 1, 2)}
        and _face_kinds(lo_, (1, 1, 2), (2, 1, 2)) == [CJ.K_CUT_SELF],
        f"{qs} {None if q is None else (I['s'][q], I['Lc'][q], I['mult'][q], _pcells(lo_, q, 'i'), _pcells(lo_, q, 'j'))} · "
        f"면 {None if lo_ is None else _face_kinds(lo_, (1, 1, 2), (2, 1, 2))}")
    Ih = (hi_ or {}).get('instances') or {}
    chi = (hi_ or {}).get('census') or {}
    chk('KINK XC s < s_min (15) — 자기 접합 0 · 거른 후보 = 후보 전부 (교차 하나 이상) · 면 (1,1,2)|(2,1,2) = 연속 융합',
        hi_ is not None and int(np.sum(Ih['self'])) == 0 and chi.get('n_self_kept') == 0
        and (chi.get('n_self_candidates') or 0) >= 1 and chi.get('n_self_filtered') == chi.get('n_self_candidates')
        and _face_kinds(hi_, (1, 1, 2), (2, 1, 2)) == [CJ.K_SELF_FUSED],
        f"{None if hi_ is None else (int(np.sum(Ih['self'])), {k: chi.get(k) for k in ('n_self_candidates', 'n_self_kept', 'n_self_filtered')}, _face_kinds(hi_, (1, 1, 2), (2, 1, 2)))}")
    w_f = chain_ref(nn, extra=[(i2, i13, G_AX)])
    I_leg = I_of(solve_legacy(sid, sig_e(), XC_N), XC_N)
    Ihs = _try(lambda: I_of(solve(sid, sig_e(), XC_N, plan(hi_, rj)), XC_N))
    chk('KINK XC s < s_min — 접합 · 절단 없음 = 옛 복셀 융합 그대로 (σ = 옛 경로 = 손 사슬 + 융합 면 1e-12)',
        rel(Ihs, I_leg) < 1e-12 and rel(Ihs, w_f) < 1e-12, f'{Ihs} ↔ 옛 {I_leg} · 손 {w_f}')
    errs = [rel(_try(lambda r_=r_: I_of(solve(sid, sig_e(), XC_N, plan(lo_, r_)), XC_N)), chain_ref(nn, extra=[(i2, i13, 1e4 / r_)]))
            for r_ in (1e1, 1e3, 1e5)]
    Ii = _try(lambda: I_of(solve(sid, sig_e(), XC_N, plan(lo_, math.inf, allow_rj_limits=True)), XC_N))
    chk('KINK XC s ≥ s_min — 면 절단 + R_j 간선 (1,1,2)–(2,1,2) (손 사슬 + 1e4/R_j · R_j 10 · 1e3 · 1e5 Ω · 1e-12) · R_j = ∞ = 사슬만',
        max(errs) < 1e-12 and rel(Ii, chain_ref(nn)) < 1e-12, f'{errs} · ∞ {Ii} ↔ {chain_ref(nn)}')
    rn = _try(lambda: registry(sid, P, s_min_um=None), None)
    pq = _try(lambda: plan(rn, rj), None) if rn is not None else None
    chk('KINK s_min 없음 + 정량 = 구조화 거부 (계획 거부 사유 self_s_min_missing · 솔브 입구 거부 · CG 전)',
        pq is not None and any(x.get('code') == 'self_s_min_missing' for x in pq['rejections'])
        and raises(lambda: solve(sid, sig_e(), XC_N, pq)))
    pt = _try(lambda: plan(rn, rj, quantitative=False), None) if rn is not None else None
    In = (rn or {}).get('instances') or {}
    sn = [(float(In['s'][q_]), float(In['d0'][q_])) for q_ in range(len(In.get('fi', []))) if In['self'][q_]]
    D_ = 2.0 * RF + TOL
    chk('KINK s_min 없음 + 시험 모드 = 진행 · 거르기 안 함 표지 (self_filter = off_s_min_missing) · 교차 접합 (s 10.8) 이 그 안에 · '
        '바닥 = 모든 자기 접합 s > D · s > (π/2)·d0 (곧은 이웃 · 꺾임 모서리 아님)',
        pt is not None and not pt['rejections'] and rn['census'].get('self_filter') == 'off_s_min_missing'
        and any(abs(x - XC_S) < 1e-9 for x, _ in sn) and all(x > D_ and x > 0.5 * math.pi * d for x, d in sn), f'{sn}')
    PK = rows(KU)
    sidk, _ = bed(PK, KU_N)
    rk = _try(lambda: registry(sidk, PK, s_min_um=20.0), None)
    Ik = _try(lambda: I_of(solve(sidk, sig_e(), KU_N, plan(rk, rj)), KU_N))
    chk('KINK KU (U 자 · 쌍 s 전부 < 20) s_min 20 — 자기 접합 0 · σ = 옛 경로 (면 셋 융합 · 1e-12)',
        rk is not None and int(np.sum(rk['instances']['self'])) == 0 and rel(Ik, I_of(solve_legacy(sidk, sig_e(), KU_N), KU_N)) < 1e-12,
        f'{Ik}')
    #  ★ 10-21 (변이 시험 다지기 · M10) — s_min 없음 (바닥 쌍 = 접합 쌍) · U 자기 접합 하나 · L_c = 그 쌍들의 닿음만: 다리 1 쪽 = z 0.9 (다리 2
    #    아래끝 (2.3, 1.5) 까지 1) … z* = 다리 1 맨 위 선분이 바닥을 지나는 짝 (다리 2 둘째 선분 · 위끝 (2.5 − 0.2/13, 4.5 − 3/13) 까지 1) —
    #    다리 2 첫 선분 짝은 바닥 밖 (s 1.46 < (π/2)·0.985) 인데 닿는다 (거리 0.985 ≤ 1) → 두 쪽 선분 전부를 짝으로 쓰면 z 4.5 까지 (L_c 3.6)
    rkn = _try(lambda: registry(sidk, PK, s_min_um=None), None)
    Ikn = (rkn or {}).get('instances') or {}
    qn = [q_ for q_ in range(len(Ikn.get('fi', []))) if Ikn['self'][q_]]
    ku_lc = (4.5 - 3.0 / 13.0) + math.sqrt(1.0 - (2.5 - 0.2 / 13.0 - 1.5) ** 2) - 0.9
    chk('KINK KU s_min 없음 — U 자기 접합 하나 · s = KU_S · L_c = 접합 쌍의 닿음만 = 손 값 %.9f (1e-9 · 두 쪽 선분 전부 짝 = 3.6)' % ku_lc,
        len(qn) == 1 and abs(float(Ikn['s'][qn[0]]) - KU_S) < 1e-9 and abs(float(Ikn['Lc'][qn[0]]) - ku_lc) < 1e-9,
        f"{qn} {None if len(qn) != 1 else (float(Ikn['s'][qn[0]]), float(Ikn['Lc'][qn[0]]))} ↔ {KU_S} · {ku_lc}")
    #  ★ 10-21 (변이 시험 다지기 · M19) — 자기 분산판의 맞은편 = 그 등분점이 놓인 선분의 접합 짝만 (같은 instance 의 다른 쌍 짝은 안 쓴다).
    #    곧은 U (다리 1 x 1.5 ↓ · 바닥 z 0.5 · 다리 2 x 2.3 ↑ · 간격 0.8 < D 1.1) · s_min 6 · L_par 0.25.  다리 1 점 z₁ ↔ 다리 2 점 z₂ 의 호
    #    s = z₁ + z₂ − 0.2.  다리 1 선분 [2.75, 3.0] 의 접합 짝 = 다리 2 [3.25, 3.5] 부터 (s = 3.0 + 3.25 − 0.2 = 6.05 ≥ 6 · 같은 높이 짝
    #    [2.75, 3.0] · [3.0, 3.25] 는 s ≤ 5.8) · 그 아래 [2.5, 2.75] 의 짝 [3.5, 3.75] 는 닿지 않는다 (높이 차 ≥ 0.75 > √(1 − 0.8²) 0.6) ⇒
    #    닿음 구간 = 다리 1 [2.75, 8.5] (L_c 5.75 · k 23) · 맨 아래 등분점 X_i = (1.5, 1.5, 2.875) · 맞은편 X_j = 짝 선분 위 최근접
    #    (2.3, 1.5, 3.25).  짝 제한을 끄면 다리 2 [2.75, 3.0] (다른 쌍 [3.25, 3.5] 의 짝) 의 수선발 (2.3, 1.5, 2.875).
    PU = rows([[(1.5, 1.5, 8.5), (1.5, 1.5, 0.5), (2.3, 1.5, 0.5), (2.3, 1.5, 8.5)]])
    sidu, _ = bed(PU, (4, 3, 9))
    ru = _try(lambda: registry(sidu, PU, s_min_um=6.0, L_par_um=0.25), None)
    Iu = (ru or {}).get('instances') or {}
    su_ = (ru or {}).get('subedges') or {}
    qu = [q_ for q_ in range(len(Iu.get('fi', []))) if Iu['self'][q_]]
    rows_u = [x for x in range(len(su_.get('inst', []))) if qu and int(su_['inst'][x]) == qu[0]] if len(qu) == 1 else []
    low = min(rows_u, key=lambda x: float(su_['X_i'][x][2])) if rows_u else None
    chk('KINK U s_min 6 · L_par 0.25 — 자기 접합 하나 · L_c 5.75 · k 23 · 맨 아래 등분점 X_i (1.5, 1.5, 2.875) 의 맞은편 X_j = 그 선분의 접합 짝 위 '
        '(2.3, 1.5, 3.25) (손 · 1e-9 · 짝 제한 끔 = 수선발 2.875)',
        len(qu) == 1 and abs(float(Iu['Lc'][qu[0]]) - 5.75) < 1e-9 and int(Iu['nsub'][qu[0]]) == 23 and len(rows_u) == 23
        and low is not None and np.allclose(su_['X_i'][low], (1.5, 1.5, 2.875), rtol=0.0, atol=1e-9)
        and np.allclose(su_['X_j'][low], (2.3, 1.5, 3.25), rtol=0.0, atol=1e-9),
        f"{qu} {None if len(qu) != 1 else (float(Iu['Lc'][qu[0]]), int(Iu['nsub'][qu[0]]))} · 행 {len(rows_u)} · "
        f"{None if low is None else (su_['X_i'][low].tolist(), su_['X_j'][low].tolist())}")
    #    정의 쪽 = j (side 1) 갈래 — 다리 1 위끝 7.5 · 다리 2 위끝 8.5 (s 식 그대로): 다리 2 닿음 = [2.75, 7.5 + 0.6] (L_c 5.35 · k 22) > 다리 1
    #    [2.75, 7.5] → side 1 · 맨 아래 등분점 X_j = (2.3, 1.5, 2.75 + 5.35/44) · 맞은편 X_i = 그 선분 [2.75, 3.0] 의 접합 짝 위 (1.5, 1.5, 3.25)
    PV = rows([[(1.5, 1.5, 7.5), (1.5, 1.5, 0.5), (2.3, 1.5, 0.5), (2.3, 1.5, 8.5)]])
    sidv, _ = bed(PV, (4, 3, 9))
    rv = _try(lambda: registry(sidv, PV, s_min_um=6.0, L_par_um=0.25), None)
    Iv = (rv or {}).get('instances') or {}
    sv_ = (rv or {}).get('subedges') or {}
    qv = [q_ for q_ in range(len(Iv.get('fi', []))) if Iv['self'][q_]]
    rows_v = [x for x in range(len(sv_.get('inst', []))) if qv and int(sv_['inst'][x]) == qv[0]] if len(qv) == 1 else []
    lowv = min(rows_v, key=lambda x: float(sv_['X_j'][x][2])) if rows_v else None
    zv = 2.75 + 5.35 / 44.0
    chk('KINK U 비대칭 (다리 2 가 길다) — side 1 · L_c 5.35 · k 22 · 맨 아래 등분점 X_j (2.3, 1.5, %.9f) 의 맞은편 X_i = 그 선분의 접합 짝 위 '
        '(1.5, 1.5, 3.25) (손 · 1e-9 · 짝 제한 끔 = 수선발)' % zv,
        len(qv) == 1 and abs(float(Iv['Lc'][qv[0]]) - 5.35) < 1e-9 and int(Iv['nsub'][qv[0]]) == 22 and len(rows_v) == 22
        and lowv is not None and int(sv_['side'][lowv]) == 1
        and np.allclose(sv_['X_j'][lowv], (2.3, 1.5, zv), rtol=0.0, atol=1e-9)
        and np.allclose(sv_['X_i'][lowv], (1.5, 1.5, 3.25), rtol=0.0, atol=1e-9),
        f"{qv} {None if len(qv) != 1 else (float(Iv['Lc'][qv[0]]), int(Iv['nsub'][qv[0]]))} · 행 {len(rows_v)} · "
        f"{None if lowv is None else (int(sv_['side'][lowv]), sv_['X_i'][lowv].tolist(), sv_['X_j'][lowv].tolist())}")
    PW = rows(KW)
    sidw, _ = bed(PW, KU_N)
    rw = _try(lambda: registry(sidw, PW, s_min_um=KW_SMIN), None)
    fk = [_face_kinds(rw, (1, 1, z), (2, 1, z)) for z in (1, 2, 3)] if rw is not None else None
    chk('KINK KW (다리 중심선 1.2 > D 1.1) — 자기 접합 후보 아님 (instance 0) · 다리 사이 면 셋 = 미등록 법칙 (중심선 탐지 · fid 무관)',
        rw is not None and len(rw['instances']['fi']) == 0 and fk == [[CJ.K_UNREG]] * 3,
        f"{None if rw is None else len(rw['instances']['fi'])} 면 {fk}")


#  KR 꺾임 재방문: 위로 (1,1,0..3) → 오른쪽 (2,1,3) → 위 (2,1,4) → 왼쪽 (1,1,4) → 아래로 셀 (1,1,3) 에 **다시** 들어옴 → 왼쪽 (0,1,3) →
#     위로 (0,1,3..7) 위 판.  자기 후보 둘 = 재방문 (1,1,3) (s = 1.0 + 1.3 + 1.2 + 0.9 = 4.4) · 면 (1,1,4)|(0,1,4) (s ≲ 2.6).
KR_N = (4, 3, 8)
KR = [[(1.5, 1.5, 0.5), (1.5, 1.5, 3.2), (2.5, 1.5, 3.2), (2.5, 1.5, 4.5), (1.3, 1.5, 4.5), (1.3, 1.5, 3.6), (0.5, 1.5, 3.6),
       (0.5, 1.5, 7.5)]]


@case('KINK-R')
def t_kink_revisit():
    """★ 10-21 (RCA-03 · Q1 (가)) — s < s_min 재방문 = 가지 (traversal) 마다 따로 · **합치지 않는다** (경로로만 이어진다).
    옛 판 (구현 B · 10-20) = 옛 복셀 한 셀 (두 위치를 한 노드로) — 판정문 RCA-03 이 그 합침을 비연속 가닥 단락으로 반증했다.
    변이 = 옛 합침을 켠다 (같은 셀 두 가지를 한 노드로) → 새 기준에서 벗어난다 (판별력)."""
    P = rows(KR)
    sid, _ = bed(P, KR_N)
    seq = seq_cells(KR[0])
    nn = len(seq)
    occ = {}
    for i_, c in enumerate(seq):
        occ.setdefault(c, []).append(i_)
    rv = occ.get((1, 1, 3), [])
    i14, i04 = seq.index((1, 1, 4)), seq.index((0, 1, 4))
    w_new = chain_ref(nn, extra=[(i14, i04, G_AX)])                       # 재방문 = 따로 · 면 (1,1,4)|(0,1,4) = 옛 융합 그대로
    w_old = chain_ref(nn, merge=[tuple(rv)], extra=[(i14, i04, G_AX)])    # 옛 = 재방문 두 가지 한 노드
    rc = _try(lambda: registry(sid, P, s_min_um=10.0), None)            # 쌍 s 전부 < s_min → 같은 가닥의 연속 (접합 아님)
    cc = (rc or {}).get('census') or {}
    #  ★ 10-21 (Q-B) — 후보 = 바닥 (s > D) 을 넘는 같은 조각 중심선 쌍의 무리 (모서리 · 닫힘 · 머리핀 · 수는 기하가 정한다 — 옛 '셀 인접
    #    항목 2' 와 다른 셈) → 후보 ≥ 1 · 거른 수 = 후보 수 · 남은 0
    chk('KINK-R s < s_min — 후보 ≥ 1 · 거른 수 = 후보 수 · 경로로만 이은 재방문 1 (합친 수 칸 없음 · 0) · 융합 자기 면 1 · 접합 0',
        rc is not None and len(rv) == 2 and (cc.get('n_self_candidates') or 0) >= 1
        and cc.get('n_self_filtered') == cc.get('n_self_candidates')
        and cc.get('n_self_revisits_path_only') == 1 and not cc.get('n_self_merged_revisits')
        and cc.get('n_self_fused_faces') == 1 and len(rc['instances']['fi']) == 0, f'{cc}')
    rj = 1e3
    r = _try(lambda: solve(sid, sig_e(), KR_N, plan(rc, rj)), None)
    chk('KINK-R s < s_min — σ = 손 회로 (재방문 두 가지 따로 · 면 융합 · 1e-12) · 옛 합침 회로와 다르다',
        r is not None and rel(I_of(r, KR_N), w_new) < 1e-12 and rel(w_new, w_old) > 1e-6
        and not (r.get('cjunc') or {}).get('n_self_merged_revisits'),
        f"{None if r is None else I_of(r, KR_N)} ↔ {w_new} (옛 {w_old})")
    base_cls = CJ.CjuncAssembler
    pairs = np.asarray((rc or {}).get('self_revisit_pairs', np.zeros((0, 2), np.int64)), np.int64).reshape(-1, 2)

    class Merge(base_cls):                                  # 변이 — 옛 합침을 켠다 (같은 셀 두 가지 → 한 노드 · 원장의 재방문 쌍)
        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            for p_, q_ in pairs:
                self.pos_dof[q_] = self.pos_dof[p_]
    CJ.CjuncAssembler = Merge
    try:
        Im = _try(lambda: I_of(solve(sid, sig_e(), KR_N, plan(rc, rj)), KR_N))
    finally:
        CJ.CjuncAssembler = base_cls
    chk('KINK-R 변이 (옛 재방문 합침 켬) → 새 기준에서 벗어난다 (원장 재방문 쌍 1)', len(pairs) == 1 and not rel(Im, w_new) < 1e-12,
        f'{Im} ↔ {w_new} · 쌍 {len(pairs)}')
    rj_ = _try(lambda: registry(sid, P, s_min_um=0.5), None)            # s_min < D → 바닥 (s > D) 만 거른다
    cj_ = (rj_ or {}).get('census') or {}
    #  ★ 10-21 (Q-B) — 닫힘 접촉 (접점 = (1.5,1.5,3.2) ↔ (1.3,1.5,3.6) · 둘 다 셀 (1,1,3) 의 두 가지) 이 재방문 두 가지를 잇는다 → 경로로만 0
    chk('KINK-R s ≥ s_min — 자기 접합 ≥ 1 · 재방문 두 가지 = 접합 포트 (경로로만 이은 재방문 0) · 융합 자기 면 0',
        rj_ is not None and int(np.sum(rj_['instances']['self'])) >= 1 and cj_.get('n_self_revisits_path_only') == 0
        and cj_.get('n_self_fused_faces') == 0, f'{cj_}')


@case('INV')
def t_invariance():
    rj = 1e3

    def run(polys, n, smin, fids=None, shift=(0.0, 0.0, 0.0), rev=False):
        pl_ = [v[::-1] for v in polys] if rev else polys
        P0 = rows(pl_, fids=fids)
        P = (P0[0] + np.asarray(shift, np.float64), P0[1], P0[2], P0[3])
        sid, _ = bed(P, n, lo=shift)
        reg = registry(sid, P, lo=shift, s_min_um=smin)
        pq = plan(reg, rj)
        return sid, len(reg['instances']['fi']), _plan_mult(pq), I_of(solve(sid, sig_e(), n, pq), n)

    #  ★ 10-21 (Q-B) — 자기 접합 꼴 = XC (옛 KU · s_min KU_S − 0.5 는 쌍마다 s 규칙에서 다리 아래쪽만 남는 경계 꼴)
    for nm, polys, n, smin, fids in (('LP', LP, LP_N, S_MIN, [77, 33]), ('XC', XC, XC_N, 5.0, [55])):
        b = _try(lambda: run(polys, n, smin), None)
        outs = {'점 역순': _try(lambda: run(polys, n, smin, rev=True), None),
                '원점 이동 (8, −4, 16)': _try(lambda: run(polys, n, smin, shift=(8.0, -4.0, 16.0)), None),
                '섬유 번호 바꿈': _try(lambda: run(polys, n, smin, fids=fids), None)}
        for what, o in outs.items():
            ok = (b is not None and o is not None and b[2] is not None and o[2] is not None and o[0].tobytes() == b[0].tobytes()
                  and o[1] == b[1] and len(o[2]) == len(b[2])
                  and np.allclose(np.sort(o[2]), np.sort(b[2]), rtol=1e-12, atol=0.0) and rel(o[3], b[3]) < 1e-12)
            chk(f'INV {nm} {what} → sid · instance 수 · 배율 · σ 같음 (1e-12)', ok,
                f'{None if b is None else (b[1], b[2], b[3])} ↔ {None if o is None else (o[1], o[2], o[3])}')


@case('SMIN')
def t_smin():
    import inspect
    try:
        prm = inspect.signature(CJ.cjunc_registry).parameters.get('s_min_um')
    except (TypeError, ValueError, AttributeError):
        prm = None
    chk('SMIN s_min_um = 필수 키워드 · 기본값 없음 (r_f · tol_ff · L_par · r_port 와 같은 꼴)',
        prm is not None and prm.kind == prm.KEYWORD_ONLY and prm.default is prm.empty, f'{prm}')
    P = rows(KU)
    sid, _ = bed(P, KU_N)
    k = dict(r_f_um=RF, tol_ff_um=TOL, L_par_um=LPAR, r_port_um=RPORT, gap_tol=2.0)
    chk('SMIN 빠뜨림 = 거부 (TypeError · 조용한 기본값 없음)',
        prm is not None and raises(lambda: CJ.cjunc_registry(sid, (0.0, 0.0, 0.0), H, *P, **k), TypeError))
    bad = (float('nan'), -1.0, math.inf, True, 'x')
    chk('SMIN 비유한 · 음수 · bool · 문자 = 거부 (조립 전)',
        prm is not None and all(raises(lambda v=v: CJ.cjunc_registry(sid, (0.0, 0.0, 0.0), H, *P, s_min_um=v, **k)) for v in bad))


@case('REC')
def t_record():
    P = rows(LP)
    sid, _ = bed(P, LP_N)
    reg = registry(sid, P)
    cen, thr, rules = reg['census'], reg['thresholds'], reg['rules']
    lc = cen.get('Lc_um') or {}
    lm = cen.get('len_mult') or {}
    chk('REC 원장 — 법칙 이름 len_scaled_v0 · s_min 문턱 · L_c 분포 (최댓값 · 분위 p90 · p99 · 중앙값) · 배율 합 (3)',
        rules.get('len_law') == 'len_scaled_v0' and thr.get('s_min_um') == S_MIN
        and all(x in lc for x in ('max', 'p90', 'p99', 'median'))
        and abs(float(lm.get('sum', math.nan)) - 3.0) < 1e-12 and abs(float(lm.get('max', math.nan)) - 3.0) < 1e-12,
        f"{rules.get('len_law')} {thr.get('s_min_um')} {lc} {lm}")
    pr = plan(reg, 1e3)['record']
    cn = pr.get('counts', {})
    chk('REC 계획 기록 — 법칙 이름 · 긴 접촉 수 1 · 간선 배율 합 3 · 한정어 = 길이 법칙 (J8 정량 거부 문장 없음)',
        pr.get('len_law') == 'len_scaled_v0' and cn.get('n_long') == 1
        and abs(float(cn.get('len_mult_sum_edge', math.nan)) - 3.0) < 1e-12
        and any('L_c/L_par' in q for q in pr.get('qualifiers', ())) and not any('정량 거부 (J8)' in q for q in pr.get('qualifiers', ())),
        f"{pr.get('len_law')} {cn}")
    #  ★ 10-21 (Q-B) — 자기 접합 꼴 = XC (교차 s 10.8 · 모서리 후보 s ≤ √2·D 남짓 = 거름) · 후보 = 바닥 (s > D) 쌍 무리 (모서리 포함)
    PK = rows(XC)
    sidk, _ = bed(PK, XC_N)
    r1 = _try(lambda: registry(sidk, PK, s_min_um=5.0), None)
    r2 = _try(lambda: registry(sidk, PK, s_min_um=15.0), None)
    c1 = (r1 or {}).get('census') or {}
    chk('REC 자기 접합 기록 — 후보 (≥ 1) · 남은 수 1 (교차) · 거른 수 = 후보 − 1 · s 분포 (최솟값 · 중앙값 · 최댓값) · 거르기 적용 표지',
        (c1.get('n_self_candidates') or 0) >= 1 and c1.get('n_self_kept') == 1
        and c1.get('n_self_filtered') == (c1.get('n_self_candidates') or 0) - 1
        and all(x in (c1.get('self_s_um') or {}) for x in ('min', 'median', 'max')) and c1.get('self_filter') == 'applied',
        f'{c1}')
    r3 = _try(lambda: registry(sidk, PK, s_min_um=6.0), None)              # r1 과 같은 분류 (교차 = 접합) — s_min 숫자만 다르다
    chk('REC 지문에 s_min 포함 — 분류가 같고 s_min 숫자만 다른 두 원장의 원장 지문이 다르다 (instance 표는 같다)',
        r1 is not None and r3 is not None and r1['thresholds'].get('s_min_um') != r3['thresholds'].get('s_min_um')
        and len(r1['instances']['fi']) == len(r3['instances']['fi']) == 1 and r1['fp']['registry'] != r3['fp']['registry'])
    chk('REC 거른 원장 (s < s_min · 15) — 거른 수 = 후보 수 (≥ 1) · 남은 수 0', r2 is not None
        and (r2['census'].get('n_self_candidates') or 0) >= 1
        and r2['census'].get('n_self_filtered') == r2['census'].get('n_self_candidates') and r2['census'].get('n_self_kept') == 0)


@case('J11')
def t_j11_short():
    n = (5, 5, 2)
    polys = [[(0.5, 2.5, 0.5), (4.5, 2.5, 0.5)], [(2.5, 0.5, 1.5), (2.5, 4.5, 1.5)]]   # 아래 층 · 위 층 십자 (거리 1.0)
    P = rows(polys)
    sid, _ = bed(P, n)
    reg = registry(sid, P)
    r0 = solve(sid, sig_e(), n, plan(reg, 0.0, allow_rj_limits=True))
    chk('J11 축약 무리가 두 판에 다 닿음 = 단락 상태 (유한 σ 로 위장 안 함 · 게시 안 함)',
        r0.get('reason') == 'cjunc_electrode_short' and r0['sigma_eff'] == 0.0, f"{r0.get('reason')}")
    r1 = solve(sid, sig_e(), n, plan(reg, 1e3))
    chk('J11 R_j > 0 = 정상 σ (단락 아님)', r1['sigma_eff'] > 0 and not r1.get('reason'))


@case('C6')
def t_c6_energy():
    P = rows(F6)
    sid, _ = bed(P, F6_N)
    reg = registry(sid, P)
    rj = 3.0e3
    r = solve(sid, sig_e(), F6_N, plan(reg, rj))
    cj = r['cjunc']
    I = I_of(r, F6_N)
    sh = cj['dissipation_share']
    chk('C6 에너지 항등식 Σ P (면 + 접합 + 판) = I·ΔV (코드 단위 · 1e-10)', rel(cj['P_total_code'], I) < 1e-10,
        f"{cj['P_total_code']} ↔ {I}")
    d = 1e-4
    Ip = I_of(solve(sid, sig_e(), F6_N, plan(reg, rj * (1 + d))), F6_N)
    Im = I_of(solve(sid, sig_e(), F6_N, plan(reg, rj * (1 - d))), F6_N)
    fd = -(math.log(Ip) - math.log(Im)) / (math.log(1 + d) - math.log(1 - d))
    chk('C6 접합 소산 몫 = −∂lnσ/∂lnR_j (중심 FD · 1e-6)', abs(sh['vv_junction'] - fd) < 1e-6, f"{sh['vv_junction']} ↔ {fd}")
    chk('C6 소산 몫 합 = 1', abs(sum(v for k, v in sh.items()) - 1.0) < 1e-12, f'{sh}')


@case('C8')
def t_c8_guards():
    P = rows(F1)
    sid, pid = bed(P, F1_N)
    reg = registry(sid, P)
    pl = plan(reg, 1e3)
    _CG_CALLS[0] = 0
    g = []
    g.append(('r1 표 동시', raises(lambda: solve(sid, sig_e(), F1_N, pl, rint={(3, 3): 1e-3}, pid=pid))))
    g.append(('주기', raises(lambda: solve(sid, sig_e(), F1_N, pl, periodic_xy=True))))
    g.append(('return_field (장 진단은 원장을 안 읽는다)', raises(lambda: solve(sid, sig_e(), F1_N, pl, return_field=True))))
    g.append(('솔버 vox ×2', raises(lambda: solve(sid, sig_e(), F1_N, pl, vox=2.0))))
    sid2 = sid.copy(); sid2[0, 0, 0] = 1
    g.append(('다른 sid', raises(lambda: solve(sid2, sig_e(), F1_N, pl))))
    pt = dict(pl); pt['g_code'] = pl['g_code'] * 2.0
    g.append(('계획 행 변조 (지문)', raises(lambda: solve(sid, sig_e(), F1_N, pt))))
    pt2 = dict(pl); pt2['g_code'] = np.full_like(pl['g_code'], np.nan)
    pt2['fp_rows'] = CJ.plan_rows_fp(pt2)
    g.append(('계획 g NaN (지문 다시 만든 변이 · Q7 불변량)', raises(lambda: solve(sid, sig_e(), F1_N, pt2))))
    rt = dict(reg); rt['instances'] = dict(reg['instances'])
    rt['instances']['port_i'] = reg['instances']['port_j'].copy()           # 포트를 다른 위치로 (값이 실제로 바뀐다)
    g.append(('원장 변조 (지문)', bool(np.any(rt['instances']['port_i'] != reg['instances']['port_i']))
              and raises(lambda: plan(rt, 1e3))))
    g.append(('VGCF 절연 채널 (이온 표)', raises(lambda: solve(sid, S3.ionic_sigma_table(0.3e-3, 3e-3), F1_N, pl))))
    cg_before = _CG_CALLS[0]
    Pn = (P[0].copy(), P[1], P[2], P[3]); Pn[0][3, 1] = np.nan
    g.append(('NaN 좌표', raises(lambda: registry(sid, Pn))))
    Pl = (P[0], P[1], P[2][:-1], P[3])
    g.append(('길이 불일치 (fid 한 줄 모자람)', raises(lambda: registry(sid, Pl))))
    g.append(('kind 없음 (연속 중심선 아님)', raises(lambda: quiet(CJ.cjunc_registry, sid, (0., 0., 0.), H, P[0], P[1], P[2], None,
                                                              **reg_kw(dict(r_f_um=RF, tol_ff_um=TOL, L_par_um=LPAR,
                                                                            r_port_um=RPORT, s_min_um=S_MIN))))))
    Fs = P[2].copy(); i0 = np.flatnonzero(Fs == 10)[2]; Fs[i0] = 20
    Ps = (P[0], P[1], Fs, P[3])
    rs = registry(sid, Ps)
    g.append(('떨어진 같은 fid = 정량 거부', any(x['code'] == 'fid_noncontiguous' for x in rs['rejections'])))
    pts_only = rows(F1, kind=0)
    sid_pt, _ = bed(pts_only, F1_N)
    rpt = registry(sid_pt, pts_only)
    g.append(('점 스탬프 VGCF (kind 0) = 정량 거부', any(x['code'] in ('vgcf_nonpath_fid', 'vgcf_orphan_cells')
                                                         for x in rpt['rejections'])))
    for nm, okk in g:
        chk(f'C8 거부 — {nm}', okk)
    chk('C8 거부 경로에서 CG 호출 0 (솔브 관문 아홉 · 조립 전)', cg_before == 0, f'{cg_before}')
    chk('C8 계획 · 기록 = 기구 표지 (mechanism_only · 모형 내부 R_j · 반셀 없음 · SDCP–VGCF 접촉 저항 0 가정)',
        pl['record']['status'].startswith('mechanism_only') and pl['record']['rj_reference_plane'] == 'model_internal_port_centre'
        and pl['record']['half_cell_in_edge'] is False
        and any('SDCP–VGCF 접촉 저항 0' in q for q in pl['record']['qualifiers']))


def _ptfe_rows(polys, fid0=900):
    return rows(polys, phase=4, fid0=fid0)


@case('P-junc')
def t_pjunc():
    P = rows(F1)
    #  PTFE 피브릴이 접점 (1.5,1.5,3.5) 근처를 지난다 — 중심선 거리 = r_P + r_f + tol_P 정확히 (경계 = 포함).
    #  경계값이 이진 정확 (0.25 + 0.5 + 0.25 = 1.0 · 좌표 2.5 − 1.5) 이어야 경계 시험이 반올림이 아닌 규칙을 본다.
    rP, tP = 0.25, 0.25
    dist = rP + RF + tP
    pt = _ptfe_rows([[(0.5, 1.5 + dist, 3.5), (5.5, 1.5 + dist, 3.5)]])
    allr = cat_rows(P, pt)
    sid, _ = bed(allr, F1_N, stamp=allr[1] != 4)                    # face_alpha 침대 = PTFE 셀 없음 (off 격자)
    reg = registry(sid, allr, tol_P_um=tP, r_ptfe_um=rP)
    cov = reg['instances']['ptfe_cov']
    chk('P-1 덮임 경계 = 정확히 tol_P 포함 (≤)', len(cov) == 1 and bool(cov[0]), f'{cov}')
    I0 = I_of(solve(sid, sig_e(), F1_N, plan(reg, 1e3, ptfe_stamp='face_alpha', ptfe_jlaw='P0')), F1_N)
    r1 = solve(sid, sig_e(), F1_N, plan(reg, 1e3, ptfe_stamp='face_alpha', ptfe_jlaw='P1'))
    chk('P-1 P0 = 영향 없음 (해석 사슬) · P1 = 덮인 instance 절단 (관통 없음)',
        rel(I0, F1_I(1e3)) < 1e-12 and r1['sigma_eff'] == 0.0 and r1['cjunc']['n_cut_p1'] == 1, f"{I0} {r1.get('reason')}")
    pt_far = _ptfe_rows([[(0.5, 1.5 + dist + 1e-9, 3.5), (5.5, 1.5 + dist + 1e-9, 3.5)]])
    allf = cat_rows(P, pt_far)
    regf = registry(sid, allf, tol_P_um=tP, r_ptfe_um=rP)
    chk('P-1 경계 밖 (+1e-9 µm) = 덮이지 않음', not bool(regf['instances']['ptfe_cov'][0]))
    chk('P-1 centerline + P1 = 거부 (centerline 이 이미 VGCF 셀을 sid 7 로 자른다)',
        raises(lambda: plan(reg, 1e3, ptfe_stamp='centerline', ptfe_jlaw='P1')))
    chk('P-1 off + P1 = 거부 (face_alpha 에서만)', raises(lambda: plan(reg, 1e3, ptfe_stamp='off', ptfe_jlaw='P1')))
    sd = rows([[(1.5, 2.5, 3.5)]], phase=5, kind=0, fid0=700)            # SDCP 점이 접점에 근접 (면 이웃 빈 셀)
    alls = cat_rows(P, pt, sd)
    sids, _ = bed(alls, F1_N, stamp=alls[1] != 4)
    regs = registry(sids, alls, tol_P_um=tP, r_ptfe_um=rP, tol_sj_um=0.5, r_sdcp_um=0.5)
    pp = plan(regs, 1e3, ptfe_stamp='face_alpha', ptfe_jlaw='P1', sdcp_mod={'c': 1.0})
    chk('P-2 PTFE 덮임 ∧ SDCP 근접 · (P1, c = 1) → 절단 먼저 (축약 아님 · N18)',
        int(pp['mode'][0]) == CJ.MODE_CUT_P1 and bool(regs['instances']['a_sdcp'][0]), f"{pp['mode']}")


# ═════════════════════════ FA+CJ — S1 face_alpha × S2 cjunc 한 솔브 (★ Z3 10-20 = 받음 · 옛 B6 임시 거부 뺌) ═════════════════════════
@case('FA+CJ')
def t_fa_cj_both_refused():
    """한 솔브에 S1 면 개구율 (face_alpha 계획) 과 S2 탄소 접합 (cjunc 계획) 을 **같이** 준다 — ★ Z3 (10-20) 설계 조합 규칙 (설계 §3 · §4 ·
    등록 R §10 꼴): α 를 `couple()` 에서 먼저 융합 면에 곱하고 (α = 0 면 = `_keep` 제거) · 그 다음 접합 훅이 발자국 면을 끊고 접합 간선을
    넣는다 · PTFE 가 접합 끝을 덮을 때는 P0/P1 법칙만 (α 를 접합 간선에 곱하지 않는다).  옛 판 (B6 통합) 은 이 조합을 조립 전에 임시로
    거부했다 (그 거부를 뺐다 — 함수 이름은 회귀 기록용으로 둔다).  양성 대조 = 같은 침대 · 같은 두 계획이 각각 홀로도 받아들여진다."""
    import ptfe_face_alpha as FA
    P = rows(F1)
    sd = rows([[(1.5, 2.5, 3.5)]], phase=5, kind=0, fid0=700)          # SDCP 셀 (1,2,3) — 교차 VGCF 셀 (1,1,3) 과 y 면 (y = 2) 공유
    pt = _ptfe_rows([[(1.5, 0.5, 3.5), (1.5, 2.5, 3.5)]])              # PTFE 가 그 VGCF|SDCP 면을 가로지른다 (α = 60/64 · 면 하나)
    allr = cat_rows(P, sd, pt)
    sid, pid = bed(allr, F1_N, stamp=allr[1] != 4)                     # face_alpha 침대 = PTFE 셀 없음 (off 격자)
    sig = sig_e()
    cj = plan(registry(sid, allr), 1e3, ptfe_stamp='face_alpha', ptfe_jlaw='P0')
    m4 = allr[1] == 4
    fa = FA.build_plan(sid, sig, FA.build_capsules(allr[0][m4], allr[2][m4], allr[3][m4]), lo=(0.0, 0.0, 0.0), vox=H,
                       channel='electronic', pid=pid)
    r_fa = solve(sid, sig, F1_N, None, face_alpha=fa, pid=pid)
    r_cj = solve(sid, sig, F1_N, cj)
    chk('FA+CJ 양성 대조 — face_alpha 홀로 = 받아들임 · 계획 행을 실제로 씀 (VGCF|SDCP 면 α 60/64)',
        r_fa['sigma_eff'] > 0.0 and r_fa['face_alpha']['n_rows_used'] == 1 and 'cjunc' not in r_fa,
        f"{r_fa.get('reason')} {r_fa.get('face_alpha')}")
    chk('FA+CJ 양성 대조 — cjunc 홀로 (ptfe_stamp face_alpha 선언) = 받아들임', r_cj['sigma_eff'] > 0.0
        and r_cj['cjunc']['solved'] is True and 'face_alpha' not in r_cj, f"{r_cj.get('reason')}")
    _CG_CALLS[0] = 0
    err, res = None, None
    try:
        res = solve(sid, sig, F1_N, cj, face_alpha=fa, pid=pid)
    except (ValueError, TypeError) as e:
        err = e
    res = res or {}
    _rj = (res.get('cjunc') or {})
    _keys = ('n_junction_edges', 'n_contracted', 'n_extra_dofs', 'tombstones')
    chk('FA+CJ 동시 (face_alpha + cjunc) = ★ Z3 받음 · 두 기록 다 · 계획 행 씀 · 조합 σ ≤ 접합만 σ (α ≤ 1 · Rayleigh) · '
        '접합 기록 (간선 · 축약 · 추가 dof · 끊은 면) = 접합만과 같음 (α 가 접합 간선에 안 걸림)',
        err is None and _CG_CALLS[0] >= 1 and (res.get('face_alpha') or {}).get('n_rows_used') == 1 and _rj.get('solved') is True
        and 0.0 < res.get('sigma_eff', 0.0) <= r_cj['sigma_eff'] * (1.0 + 1e-12)
        and all(_rj.get(k) == r_cj['cjunc'].get(k) for k in _keys),
        f'예외 {type(err).__name__ if err else None}: {str(err)[:120]} · CG {_CG_CALLS[0]} · '
        f"σ {res.get('sigma_eff')} ↔ 접합만 {r_cj['sigma_eff']} · {[(k, _rj.get(k), r_cj['cjunc'].get(k)) for k in _keys]}")


# ═════════════════════════ S3 ═════════════════════════
def _s3_fixture(with_sdcp=True, sdcp_pos=(1.5, 2.5, 3.5)):
    P = rows(F1)
    parts = [P]
    if with_sdcp:
        parts.append(rows([[sdcp_pos]], phase=5, kind=0, fid0=700))
    allr = cat_rows(*parts)
    sid, _ = bed(allr, F1_N)                                       # SDCP 점 스탬프 (h 1 에서 구 스탬프는 d/vox ≥ 2 게이트)
    reg = registry(sid, allr, tol_sj_um=0.5, r_sdcp_um=0.5)
    return sid, reg, allr


def _rows_sig(p):
    return (p['mode'].tobytes(), p['g_code'].tobytes(), p['rj_eff'].tobytes())


@case('S3')
def t_s3():
    sid, reg, allr = _s3_fixture()
    chk('S3 근접 판정 (SDCP 1 차 입자 표면 ↔ 접점 ≤ tol_sj)', bool(reg['instances']['a_sdcp'][0]))
    p_s2 = plan(reg, 1e3)
    p_c0 = plan(reg, 1e3, sdcp_mod={'c': 0.0})
    r_s2 = solve(sid, sig_e(), F1_N, p_s2)
    r_c0 = solve(sid, sig_e(), F1_N, p_c0)
    chk('S3-1 c = 0 → 계획 행 · σ 가 S2 와 비트 같음', _rows_sig(p_s2) == _rows_sig(p_c0)
        and np.float64(r_s2['sigma_eff']).tobytes() == np.float64(r_c0['sigma_eff']).tobytes())
    sid_n, reg_n, _ = _s3_fixture(with_sdcp=False)
    s2n = plan(reg_n, 1e3)
    same = True
    for c in (0.0, 0.5, 1.0):
        pc = plan(reg_n, 1e3, sdcp_mod={'c': c}, quantitative=(c in (0.0, 1.0)))
        same &= _rows_sig(pc) == _rows_sig(s2n)
        rc = solve(sid_n, sig_e(), F1_N, pc)
        same &= np.float64(rc['sigma_eff']).tobytes() == np.float64(solve(sid_n, sig_e(), F1_N, s2n)['sigma_eff']).tobytes()
    chk('S3-2 SBE (SDCP 없음) — 모든 c 에서 계획 행 · σ 비트 같음 (셀 · 원장 단위 no-op)', same)
    Is = [I_of(solve(sid, sig_e(), F1_N, plan(reg, 1e3, sdcp_mod={'c': c}, quantitative=False)), F1_N)
          for c in (0.0, 0.5, 0.9, 0.99)]
    TAU = 1e-12                                                    # 봉인 (직접 풀이 · 같은 그래프 = Rayleigh 정확)
    chk(f'S3-3 c 단조 — σ(c) 비감소 (c 격자 0 · 0.5 · 0.9 · 0.99 · 허용폭 {TAU} 봉인)',
        all(Is[i + 1] >= Is[i] * (1 - TAU) for i in range(len(Is) - 1)) and Is[-1] > Is[0], f'{Is}')
    want_c = [F1_I(1e3 * (1 - c)) for c in (0.0, 0.5, 0.9, 0.99)]
    chk('S3-3 R_j′ = R_j,0·(1 − c·a_j) — 해석 사슬 (1e-12)', max(rel(a, b) for a, b in zip(Is, want_c)) < 1e-12, f'{Is} {want_c}')
    p1 = plan(reg, 1e3, sdcp_mod={'c': 1.0})
    r1 = solve(sid, sig_e(), F1_N, p1)
    chk('S3-4 c = 1 = 근접 instance 축약 (축약 경로 · 정량 허용 예외 · 축약 수 기록 · 옛 융합과 같음 1e-12)',
        int(p1['mode'][0]) == CJ.MODE_CONTRACT and r1['cjunc']['n_contracted'] == 1
        and rel(I_of(r1, F1_N), F1_I(0)) < 1e-12, f"{p1['mode']} {r1['cjunc'].get('n_contracted')}")
    chk('S3 정량 모드 c ∈ {0, 1} 만 (0.5 = 거부)', raises(lambda: plan(reg, 1e3, sdcp_mod={'c': 0.5})))
    chk('S3 c 범위 밖 · NaN = 거부', raises(lambda: plan(reg, 1e3, sdcp_mod={'c': 1.5}, quantitative=False))
        and raises(lambda: plan(reg, 1e3, sdcp_mod={'c': float('nan')}, quantitative=False)))
    P, PH, F, K = allr
    m5 = np.flatnonzero(PH == 5)
    order = np.arange(len(P)); order[m5] = m5[::-1]
    regp = registry(sid, (P[order], PH[order], F[order], K[order]), tol_sj_um=0.5, r_sdcp_um=0.5)
    chk('S3-5 SDCP 점 순열 불변 (근접 · 계획 행 비트 같음)', _rows_sig(plan(regp, 1e3, sdcp_mod={'c': 1.0})) == _rows_sig(p1))
    d_edge = 0.5 + 0.5                                             # 접점 (1.5,1.5,3.5) ↔ SDCP 중심 = r_s + tol_sj 정확히
    sid_e, reg_e, _ = _s3_fixture(sdcp_pos=(1.5, 1.5 + d_edge, 3.5))
    sid_o, reg_o, _ = _s3_fixture(sdcp_pos=(1.5, 1.5 + d_edge + 1e-9, 3.5))
    chk('S3-6 근접 문턱 경계 = 포함 (≤) · +1e-9 µm = 밖', bool(reg_e['instances']['a_sdcp'][0])
        and not bool(reg_o['instances']['a_sdcp'][0]))
    #  S3-7 원고 펠릿 LPSCl:SDCP 9:1 (탄소 없음) — v0 의 S3 은 구성상 no-op (판별력 없음 · 그렇게 기록)
    rng = np.random.default_rng(3)
    n = (12, 12, 12); box = np.array(n, float) * 0.5
    sd = rng.uniform(0.2, box - 0.2, (60, 3))
    rp = (sd, np.full(len(sd), 5), np.arange(len(sd)) + 1, np.zeros(len(sd), int))
    sidp, _ = S3.rasterize(*NO_AM, rp[0], rp[1], (0., 0., 0.), tuple(box), 0.5, se_pts=rng.uniform(0, box, (20000, 3)),
                           sdcp_sphere_d_um=1.0, add_fid=rp[2], add_kind=rp[3])
    regp = quiet(CJ.cjunc_registry, sidp, (0., 0., 0.), 0.5, *rp,
                 **reg_kw(dict(r_f_um=0.25, tol_ff_um=0.05, L_par_um=1.0, r_port_um=1.0, tol_sj_um=0.05, r_sdcp_um=0.5,
                               s_min_um=1.5)))
    pc0 = plan(regp, 1e3, sdcp_mod={'c': 0.0}); pc1 = plan(regp, 1e3, sdcp_mod={'c': 1.0})
    rc0 = solve(sidp, sig_e(), n, pc0, vox=0.5); rc1 = solve(sidp, sig_e(), n, pc1, vox=0.5)
    chk('S3-7 펠릿 9:1 (탄소 없음) — c 0 ↔ 1 σ_e 비트 같음 = 구성상 no-op (판별력 없음 기록)',
        len(regp['instances']['fi']) == 0 and np.float64(rc0['sigma_eff']).tobytes() == np.float64(rc1['sigma_eff']).tobytes()
        and rc1['cjunc'].get('s3_discriminating') is False)
    #  S3-8 변이 — 비근접에 c · (1 − c) 뒤집힘 · G 에 곱함 · c = 1 을 큰 g 로 = 실패해야
    old = CJ.sdcp_rj_eff
    det = []
    muts = (('비근접에 c', lambda r0, c, a: r0 * (1.0 - c)),
            ('(1 − c) 뒤집힘', lambda r0, c, a: r0 * (c * a if a else 1.0)),
            ('G 에 곱함', lambda r0, c, a: r0 / (1.0 - c * a) if c * a < 1 else math.inf),
            ('c = 1 을 큰 g 로', lambda r0, c, a: r0 * (1.0 - c * a) if c * a < 1 else 1e-12))
    for nm, fn in muts:
        CJ.sdcp_rj_eff = fn
        try:
            bad = False
            pm = plan(reg, 1e3, sdcp_mod={'c': 1.0})
            if int(pm['mode'][0]) != CJ.MODE_CONTRACT:
                bad = True
            pmh = plan(reg, 1e3, sdcp_mod={'c': 0.5}, quantitative=False)
            Im = I_of(solve(sid, sig_e(), F1_N, pmh), F1_N)
            if rel(Im, F1_I(500.0)) > 1e-12:
                bad = True
            pn = plan(reg_n, 1e3, sdcp_mod={'c': 1.0})
            if _rows_sig(pn) != _rows_sig(s2n):
                bad = True
            det.append(bad)
        except Exception:                                  # noqa: BLE001
            det.append(True)
        finally:
            CJ.sdcp_rj_eff = old
    chk('S3-8 변이 넷 (비근접에 c · 뒤집힘 · G 곱 · c = 1 큰 g) 을 시험이 잡는다', all(det), f'{det}')
    chk('S3-9 S2 없이 (원장 없이) = 거부', raises(lambda: CJ.cjunc_plan(None, 1e3, unreg_law='cut', ptfe_stamp='off',
                                                                     sdcp_mod={'c': 1.0}))
        and raises(lambda: solve(sid, sig_e(), F1_N, {'c': 1.0})))
    fp0 = reg['fp']['sid']
    chk('S3-10 sid 불변 — 모든 c 에서 원장의 sid 지문 = 솔브 sid', all(plan(reg, 1e3, sdcp_mod={'c': c}, quantitative=False)
                                                                    ['registry']['fp']['sid'] == fp0 for c in (0.0, 0.5, 1.0))
        and fp0 == S3._grid_fp(sid))


@case('SV')
def t_sv():
    #  SV 면 우회: A 와 B 사이에 SDCP 덩어리가 끼어 SV 면 (융합) 으로 이어진다 — 접합 저항이 크면 SV 경로가 소산을 지배
    n = (7, 3, 8)
    polys = [[(1.5, 1.5, 0.5), (1.5, 1.5, 3.5)], [(3.5, 1.5, 3.5), (3.5, 1.5, 7.5)]]   # A–B 중심선 거리 2.0 (접합 아님)
    P = rows(polys)
    sd = rows([[(2.5, 1.5, 3.5)]], phase=5, kind=0, fid0=700)
    allr = cat_rows(P, sd)
    sid, _ = bed(allr, n)                                          # SDCP 점 스탬프 → 셀 (2,1,3) = A 와 B 사이
    reg = registry(sid, allr, tol_sj_um=0.1, r_sdcp_um=0.5)
    chk('SV SDCP 경유 섬유 연결 수 (S0 꼴 · σ 전) = 1 성분 · fid 쌍 1', reg['census'].get('n_sdcp_bridging_components') == 1
        and reg['census'].get('n_sdcp_bridged_fid_pairs') == 1, f"{reg['census']}")
    r = solve(sid, sig_e(), n, plan(reg, 1e3))
    cj = r['cjunc']
    sld = cj.get('sv_local_dissipation') or {}
    #  ★ 10-21 (RCA-06 · Q4 (가)) — `sv_dominant` (지배성 표지) 철회 → 진단 `sv_local_dissipation` (국소 소산 몫 · 지배성 보증 아님)
    chk('SV 접합 instance 0 → 소산 = SV 면 + SDCP 셀 몫 > 0 · 진단 SV_local_dissipation (sv_share) · 지배성 표지 sv_dominant 없음',
        cj['n_instances'] == 0 and cj['dissipation_share']['sv_face'] + cj['dissipation_share']['sdcp_cell'] > 0
        and 'sv_dominant' not in cj and isinstance(sld.get('sv_share'), float) and sld['sv_share'] > 0.0,
        f"{cj.get('dissipation_share')} {sld} {'sv_dominant' in cj}")
    P2 = rows(F1)
    sid2, _ = bed(P2, F1_N)
    r2 = solve(sid2, sig_e(), F1_N, plan(registry(sid2, P2), 1e3))
    sl2 = r2['cjunc'].get('sv_local_dissipation') or {}
    chk('SV SDCP 없음 → SV 몫 0 · 진단 sv_share 0.0 · 지배성 표지 없음', r2['cjunc']['dissipation_share']['sv_face'] == 0.0
        and sl2.get('sv_share') == 0.0 and 'sv_dominant' not in r2['cjunc'])


@case('MUT')
def t_mutants():
    """설계 §4-4 변이 — 조립기를 바꿔 끼운 변이가 위 시험 (해석 회로) 에 **걸려야** 한다 (판별력 · 안 걸리면 시험 무효)."""
    base_cls = CJ.CjuncAssembler

    class SingleWinner(base_cls):                          # 멤버십 단일 승자 — 교차 셀의 추가 dof 를 주 dof 로 접는다
        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            pos = self.reg['positions']
            ex = np.flatnonzero(pos['live'] & ~pos['primary'])
            prim_of = {int(pos['lin'][p]): int(self.pos_dof[p]) for p in np.flatnonzero(pos['primary'])}
            for p in ex:
                self.pos_dof[p] = prim_of[int(pos['lin'][p])]

    class KeepTomb(base_cls):                              # tombstone 삭제 — 접합 자리 면을 옛 융합으로 남긴다
        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            ft = dict(self.ft)
            ft['kind'] = np.where(ft['kind'] == CJ.K_CUT_SITE, CJ.K_AXIAL, ft['kind'])
            self.ft = ft

    class WrongDof(base_cls):                              # 간선을 다른 dof 에 — 포트 j 를 그 경로의 다음 위치로
        def build(self, *a, **k):                          #  (★ 10-21 — 조립기는 분산 간선 표 'subedges' 를 읽는다 → 그 포트도 옮긴다)
            inst = self.reg['instances']
            pj = inst['port_j'].copy()
            self.reg = dict(self.reg)
            self.reg['instances'] = dict(inst)
            self.reg['instances']['port_j'] = np.minimum(pj + 1, len(self.reg['positions']['lin']) - 1)
            if isinstance(self.reg.get('subedges'), dict):
                sub = dict(self.reg['subedges'])
                sub['port_j'] = np.minimum(np.asarray(sub['port_j']) + 1, len(self.reg['positions']['lin']) - 1)
                self.reg['subedges'] = sub
            return super().build(*a, **k)

    class PairCut(base_cls):                               # 쌍 단위 절단 — 미등록 자리도 그 쌍이면 절단
        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            ft = dict(self.ft)
            ft['kind'] = np.where(ft['kind'] == CJ.K_UNREG, CJ.K_CUT_SITE, ft['kind'])
            self.ft = ft

    def run_with(cls, fn):
        CJ.CjuncAssembler = cls
        try:
            v = fn()
            print(f'    MUT {cls.__name__}: σ 기반 전류 {v!r}')
            return v
        except Exception as e:                             # noqa: BLE001 — 변이가 예외로 끝나도 '걸렸다' (기록한다)
            print(f'    MUT {cls.__name__}: 예외 {type(e).__name__}: {e}')
            return None
        finally:
            CJ.CjuncAssembler = base_cls

    P1_ = rows(F1); sid1, _ = bed(P1_, F1_N); reg1 = registry(sid1, P1_)
    P2_ = rows(F2); sid2, _ = bed(P2_, F2_N); reg2 = registry(sid2, P2_)
    P10 = rows(F10); sid10, _ = bed(P10, F6_N); reg10 = registry(sid10, P10)
    rj = 1e3
    I1 = run_with(SingleWinner, lambda: I_of(solve(sid1, sig_e(), F1_N, plan(reg1, rj)), F1_N))
    chk('MUT 멤버십 단일 승자 → C1 해석 사슬에서 벗어난다 (R_j 가 사라짐)', I1 is None or rel(I1, F1_I(rj)) > 1e-6, f'{I1}')
    w2 = chain_I([G_PL] + [G_AX] * 3 + [1e4 / rj] + [G_AX] * 4 + [G_PL])
    I2 = run_with(KeepTomb, lambda: I_of(solve(sid2, sig_e(), F2_N, plan(reg2, rj)), F2_N))
    chk('MUT tombstone 삭제 (옛 융합 면이 접합을 우회) → C2a 해석에서 벗어난다', I2 is None or rel(I2, w2) > 1e-6, f'{I2} {w2}')
    I3 = run_with(WrongDof, lambda: I_of(solve(sid1, sig_e(), F1_N, plan(reg1, rj)), F1_N))
    chk('MUT 접합 간선을 다른 dof 에 → C1 해석에서 벗어난다', I3 is None or rel(I3, F1_I(rj)) > 1e-6, f'{I3}')
    I4 = run_with(PairCut, lambda: I_of(solve(sid10, sig_e(), F6_N, plan(reg10, 3e3, unreg_law='fused')), F6_N))
    wf = _f6_reference(3e3, second_site=True, fused_second=True)
    chk('MUT 쌍 단위 절단 (미등록 자리까지 자름) → T1-12 fused 기준에서 벗어난다', I4 is None or rel(I4, wf) > 1e-6, f'{I4} {wf}')


@case('MUT-LEN')
def t_mut_len():
    """길이 법칙 변이 넷 — 모듈 훅을 바꿔 끼운 변이가 새 시험 (해석 회로 · 원장) 에 **걸려야** 한다.  훅이 없으면 (고치기 전) 실패."""
    def hook(name):
        return CJ is not None and callable(getattr(CJ, name, None))

    @contextlib.contextmanager
    def patched(name, fn):
        old = getattr(CJ, name)
        setattr(CJ, name, fn)
        try:
            yield
        finally:
            setattr(CJ, name, old)

    rj = 1e3
    Plp = rows(LP)
    sidlp, _ = bed(Plp, LP_N)
    P1_ = rows(F1)
    sid1, _ = bed(P1_, F1_N)
    Pku = rows(KU)
    sidku, _ = bed(Pku, KU_N)

    def lp_err(law='cut'):
        return rel(_try(lambda: I_of(solve(sidlp, sig_e(), LP_N, plan(registry(sidlp, Plp), rj, unreg_law=law)), LP_N)), _lp_ref(rj))

    def f1_err():
        return rel(_try(lambda: I_of(solve(sid1, sig_e(), F1_N, plan(registry(sid1, P1_), rj)), F1_N)), F1_I(rj))

    def ku_cont_ok():
        """s < s_min — 자기 접합 0 · σ = 옛 경로 (1e-12).  ★ 10-21 (Q-B) — s_min 20 (KU 의 쌍 s 전부 아래 · 옛 KU_S + 0.5 는 쌍마다 규칙에서
        다리 1 아래 끝 ↔ 아래 가로 쌍 (s ≈ 7.6) 이 넘는다)."""
        reg = _try(lambda: registry(sidku, Pku, s_min_um=20.0), None)
        if reg is None:
            return False
        Ih = _try(lambda: I_of(solve(sidku, sig_e(), KU_N, plan(reg, rj)), KU_N))
        return int(np.sum(reg['instances']['self'])) == 0 and rel(Ih, I_of(solve_legacy(sidku, sig_e(), KU_N), KU_N)) < 1e-12

    #  (이름 · 훅 · 변이 · 검사) — 변이 전 검사 통과 · 변이 뒤 같은 검사 실패 (예외로 멈춰도 '걸렸다' · B 의 MUT 와 같은 규약:
    #   max(1, ·) 빼기는 계획의 배율 ≥ 1 불변량이 해석 대조 전에 막는다)
    cases = (
        ('배율 제곱 → LEN-P 해석에서 벗어난다', 'junction_len_mult',
         lambda Lc, Lp: np.maximum(1.0, np.asarray(Lc, np.float64) / Lp) ** 2, lambda: lp_err() < 1e-12),
        ('max(1, ·) 빼기 (짧은 접촉이 약해짐) → C1 해석 · 배율 불변량에 걸린다', 'junction_len_mult',
         lambda Lc, Lp: np.asarray(Lc, np.float64) / Lp, lambda: f1_err() < 1e-12),
        ('s 거르기 끔 → s < s_min 인데 자기 접합이 생긴다 (KINK 연속 기준 실패)', '_self_is_junction',
         lambda s, smin: np.ones(np.shape(np.atleast_1d(s)), bool), ku_cont_ok),
        ('발자국 = 최근접 선분 쌍만 → run 위 A|B 면이 fused 로 남아 LEN-P (fused) 해석에서 벗어난다', '_footprint_segs',
         lambda inst, k: (np.atleast_1d(inst['si_min'][k]), np.atleast_1d(inst['sj_min'][k])),
         lambda: lp_err('fused') < 1e-12),
    )
    for nm, name, fn, check in cases:
        h = hook(name)
        b = bool(check()) if h else False
        c = None
        if h:
            with patched(name, fn):
                c = not bool(check())
        chk(f'MUT-LEN {nm} (훅 `{name}` 있음 · 변이 전 통과 · 변이 실패)', h and b and c is True, f'hook {h} base {b} caught {c}')


# ═════════════════════════ RCA — Codex 10-21 (RCA-03 · 04 · 05 · 06 + Q11 일부) · 1저자 10-21 Q1–Q4 (가) ═════════════════════════
#  판정문 docs/reviews/codex_review_rint2_carbon_additive_design_20261021.md · 반례 = 증거 geometry/geometry_probes.py.
#  기대값 = 손으로 세운 회로 (`ref_I`) · 셀 열 (`segment_cells`) — 모듈 함수로 정답을 만들지 않는다.

def seq_cells_v(verts, vox, step):
    """폴리라인 → 셀 열 (연속 중복 제거) · 임의 vox · 점 간격 (생산 원시 함수 `segment_cells` — 기대 회로용 독립 도구)."""
    from fibre_segment_raster import segment_cells
    pts = densify(verts, step)
    cs = np.vstack([segment_cells(pts[i], pts[i + 1], vox) for i in range(len(pts) - 1)])
    keep = np.ones(len(cs), bool)
    keep[1:] = np.any(cs[1:] != cs[:-1], axis=1)
    return [tuple(int(v) for v in c) for c in cs[keep]]


def chain_ref(nn, merge=(), extra=(), g_ax=G_AX, g_pl=G_PL):
    """노드 0..nn−1 직렬 사슬 (축 g_ax) + 판 (0 아래 · nn−1 위) — merge = [(a, b)] 두 노드를 한 노드로 · extra = [(a, b, g)] 간선."""
    rep = list(range(nn))

    def f(x):
        while rep[x] != x:
            x = rep[x]
        return x
    for a, b in merge:
        ra, rb = f(a), f(b)
        if ra != rb:
            rep[max(ra, rb)] = min(ra, rb)
    E = [(f(i), f(i + 1), g_ax) for i in range(nn - 1)] + [(f(a), f(b), g) for a, b, g in extra]
    E = [(a, b, g) for a, b, g in E if a != b]
    return ref_I(nn, E, [(f(0), g_pl)], [(f(nn - 1), g_pl)])


def sys_bytes(res):
    """해의 간선 원장 (조립기가 실제로 쓴 계) — 비트 대조용 바이트 묶음."""
    s = (res.get('_cjunc') or {}).get('sys') or {}
    return tuple(np.asarray(s[k]).tobytes() for k in ('u', 'v', 'G', 'Ab', 'gb', 'At', 'gt')) if s else None


def _pcells(reg, q, side):
    """instance q 의 포트 셀 (i, j, k) — side 'i' · 'j'."""
    p = int(reg['instances']['port_' + side][q])
    pos = reg['positions']
    return None if p < 0 else tuple(int(v) for v in pos['ijk'][p])


def _sub(reg):
    return reg.get('subedges') if isinstance(reg, dict) else None


def _sub_cells(reg):
    """분산 간선 (원장 'subedges') 마다 (포트 i 셀, 포트 j 셀) — 고치기 전 코드 = None."""
    s = _sub(reg)
    if s is None:
        return None
    pos = reg['positions']
    out = []
    for a, b in zip(s['port_i'], s['port_j']):
        out.append((None if a < 0 else tuple(int(v) for v in pos['ijk'][a]),
                    None if b < 0 else tuple(int(v) for v in pos['ijk'][b])))
    return out


# ── RCA03 픽스처 — 판정문 RCA-03 폴리라인 (h 0.15 µm · r_f 0.075) 을 z 로 0.30 올리고 아래 · 위 리드를 붙였다 (판 결합).
#    리드 (0,0,0..2) → 고리 시작 (0,0,2) → +x (1,0,2) (2,0,2) → +y (2,1,2) (2,2,2) → 위 (2,2,2) 안 → −y (2,1,2) (2,0,2) →
#    −x (1,0,2) (0,0,2) → 리드 (0,0,3..5).  같은 fid 가 셀 넷 ((0,0,2) (1,0,2) (2,0,2) (2,1,2)) 을 두 번씩 지난다 (비연속).
#    (0,0,2) 의 두 가닥 중심선 거리 = √(0.13² + 0.13²) = 0.184 > 지름 0.15 (닿지 않는다).
RC_H, RC_RF, RC_TOL, RC_LPAR, RC_RPORT = 0.15, 0.075, 0.03, 0.30, 0.30
RC_N = (4, 3, 6)
RC_LOOP = [(.01, .01, .02), (.01, .01, .31), (.44, .01, .31), (.44, .44, .31), (.44, .44, .44), (.44, .14, .44),
           (.01, .14, .44), (.01, .14, .88)]
RC_STEP = 0.05
RC_GAX = SV * RC_H                                      # 축 면 g = σ·h (코드 단위)
RC_GPL = SV * RC_H * RC_H / (0.5 * RC_H)                # 판 결합 g = σ·h²/(h/2)
RC_SDCP = [[(.52, .22, .375)]]                          # 셀 (3,1,2) — (2,1,2) 옆 빈 셀 (SV 면 하나 · 매달린 셀) · 머리핀 다리 전체가 근접 거리 안


def _rc_reg(sid, P, smin, **kw):
    k = dict(r_f_um=RC_RF, tol_ff_um=RC_TOL, L_par_um=RC_LPAR, r_port_um=RC_RPORT, s_min_um=smin)
    k.update(kw)
    return registry(sid, P, vox=RC_H, **k)


def _rc_bed(with_sdcp=False):
    P = rows([RC_LOOP], step=RC_STEP)
    if with_sdcp:
        P = cat_rows(P, rows(RC_SDCP, phase=5, kind=0, fid0=700))
    sid, _ = bed(P, RC_N, vox=RC_H)
    return P, sid


@case('RCA03')
def t_rca03_branch():
    seq = seq_cells_v(RC_LOOP, RC_H, RC_STEP)
    nn = len(seq)
    occ = {}
    for i_, c in enumerate(seq):
        occ.setdefault(c, []).append(i_)
    rev = {c: v for c, v in occ.items() if len(v) > 1}
    chk('RCA03 픽스처 — 같은 fid 비연속 재방문 셀 넷 (각 두 가지) · 실제 segment_cells (판정문 폴리라인)',
        sorted(rev) == [(0, 0, 2), (1, 0, 2), (2, 0, 2), (2, 1, 2)] and all(len(v) == 2 for v in rev.values()), f'{rev}')
    P, sid = _rc_bed()
    I_chain = chain_ref(nn, g_ax=RC_GAX, g_pl=RC_GPL)
    #  (가) s < s_min — 접합 없음 · 가지를 합치지 않는다 → σ = 직렬 사슬 그대로 (판정문 5 Ω 꼴) · 옛 = 셀 합침 단락 (2 Ω 꼴)
    rh = _try(lambda: _rc_reg(sid, P, 5.0), None)
    Ih = _try(lambda: I_of(solve(sid, sig_e(), RC_N, plan(rh, 1e3), vox=RC_H), RC_N, vox=RC_H))
    I_short = chain_ref(nn, merge=[tuple(v) for v in rev.values()], g_ax=RC_GAX, g_pl=RC_GPL)
    print(f'    RCA03 사슬 I {I_chain:.9g} · 합친 꼴 (옛) {I_short:.9g} (×{I_short / I_chain:.3f}) · 지금 {Ih:.9g}')
    chk('RCA03 (가) s < s_min — 같은 셀 다른 가지를 합치지 않는다 → σ = 직렬 사슬 (손 회로 1e-12 · 판정문 5 → 2 Ω 단락 없음)',
        rel(Ih, I_chain) < 1e-12, f'{Ih} ↔ 사슬 {I_chain} · 합친 꼴 {I_short}')
    cen = (rh or {}).get('census') or {}
    #  ★ 10-21 (Q-B) — 후보 = 바닥 (s > D) 쌍 무리 (머리핀 + 모서리 · 수는 기하) → 남은 0 · 거른 수 = 후보 수 · 재방문 넷 = 경로로만
    chk('RCA03 (가) 기록 — 자기 후보 ≥ 1 · 남은 0 · 거른 수 = 후보 수 · 경로로만 이은 재방문 쌍 4 (합친 수 칸 없음 · 0)',
        (cen.get('n_self_candidates') or 0) >= 1 and cen.get('n_self_kept') == 0
        and cen.get('n_self_filtered') == cen.get('n_self_candidates') and cen.get('n_self_revisits_path_only') == 4
        and not cen.get('n_self_merged_revisits'), f'{ {k: cen.get(k) for k in ("n_self_candidates", "n_self_kept", "n_self_filtered", "n_self_revisits_path_only", "n_self_merged_revisits")} }')
    #  (나) s ≥ s_min (거름 0) · R_j = ∞ — 가지 사이 전류 0 → 사슬 그대로
    rl = _try(lambda: _rc_reg(sid, P, 0.0), None)
    Ii = _try(lambda: I_of(solve(sid, sig_e(), RC_N, plan(rl, math.inf, allow_rj_limits=True), vox=RC_H), RC_N, vox=RC_H))
    chk('RCA03 (나) s ≥ s_min · R_j = ∞ → σ = 직렬 사슬 (1e-12)', rel(Ii, I_chain) < 1e-12, f'{Ii} ↔ {I_chain}')
    #  (다) s ≥ s_min · R_j 유한 — 자기 접합 하나 = 두 가닥이 실제로 닿는 머리핀 다리 셀 ((2,0,2) · (2,1,2) — 중심선 거리 0.13 < 지름
    #       0.15) 하나의 두 가지 사이 R_j 간선 (s 를 정한 최근접점 쌍 = 기하 접점 · L_c < L_par → 배율 1 · 간선 하나).  옛 = 대표 항목
    #       (셀 번호 최소) = 두 가닥이 닿지 않는 (0,0,2) (거리 0.184) 에 접합을 놓았다.  기대 회로 = 독립 셀 열의 그 셀 두 위치 사이 R_j 간선.
    #       ★ 10-21 (Q-B · 쌍마다 s 규칙) — s_min 0.6 · 머리핀 쌍 s = 2(0.44 − y) + 0.13 ≥ 0.6 → y ≤ 0.205 (닿음 L_c < L_par · 간선 하나) ·
    #       90° 모서리 쌍은 바닥 (s > D · s > (π/2)·d — 모서리 s ≤ √2·d) 이 어느 s_min 에서도 거른다
    rj = 1e3
    rl6 = _try(lambda: _rc_reg(sid, P, 0.6), None)
    qs = np.flatnonzero(rl6['instances']['self']) if rl6 is not None else []
    pc = ((_pcells(rl6, int(qs[0]), 'i'), _pcells(rl6, int(qs[0]), 'j')) if len(qs) == 1 else None)
    cell = pc[0] if pc is not None and pc[0] == pc[1] else None
    a, b = rev.get(cell, (0, 0))
    I_j = chain_ref(nn, extra=[(a, b, 1e4 / rj)], g_ax=RC_GAX, g_pl=RC_GPL)
    Ij = _try(lambda: I_of(solve(sid, sig_e(), RC_N, plan(rl6, rj), vox=RC_H), RC_N, vox=RC_H))
    chk('RCA03 (다) s ≥ s_min — 자기 접합 하나 · 포트 = 닿는 머리핀 다리 셀 ((2,0,2) · (2,1,2)) 한 셀의 두 가지 (닿지 않는 (0,0,2) · '
        '(1,0,2) 아님) · σ = 사슬 + 그 두 가지 사이 R_j 간선 (1e-12)',
        cell in ((2, 0, 2), (2, 1, 2)) and rel(Ij, I_j) < 1e-12, f'포트 {pc} · {Ij} ↔ {I_j}')
    #  (라) c = 1 · SDCP 가 머리핀 접점 옆 — 접합 아닌 재방문 (s < s_min) 은 c 와 무관 (축약 0 · 사슬 그대로)
    Ps, sids = _rc_bed(with_sdcp=True)
    rsh = _try(lambda: _rc_reg(sids, Ps, 5.0, tol_sj_um=RC_TOL, r_sdcp_um=0.15), None)
    rsc = _try(lambda: solve(sids, sig_e(), RC_N, plan(rsh, 1e3, sdcp_mod={'c': 1.0}), vox=RC_H), None)
    chk('RCA03 (라) c = 1 · s < s_min — 재방문이 축약되지 않는다 (축약 0 · σ = 사슬 · SDCP 셀 = 매달린 셀)',
        rsc is not None and (rsc.get('cjunc') or {}).get('n_contracted') == 0 and rel(I_of(rsc, RC_N, vox=RC_H), I_chain) < 1e-12,
        f"{None if rsc is None else ((rsc.get('cjunc') or {}).get('n_contracted'), I_of(rsc, RC_N, vox=RC_H))} ↔ {I_chain}")
    #  (마) c = 1 · s ≥ s_min — 근접 자기 접합 = 축약 (설계대로 · 시나리오 끝) = 그 두 가지 한 노드
    rsl = _try(lambda: _rc_reg(sids, Ps, 0.6, tol_sj_um=RC_TOL, r_sdcp_um=0.15), None)
    r1 = _try(lambda: solve(sids, sig_e(), RC_N, plan(rsl, 1e3, sdcp_mod={'c': 1.0}), vox=RC_H), None)
    I_c = chain_ref(nn, merge=[(a, b)], g_ax=RC_GAX, g_pl=RC_GPL)
    chk('RCA03 (마) c = 1 · s ≥ s_min — 근접 자기 접합 하나 축약 (설계 시나리오 끝) = (다) 의 그 셀 두 가지 한 노드 (1e-12)',
        r1 is not None and (r1.get('cjunc') or {}).get('n_contracted') == 1 and rel(I_of(r1, RC_N, vox=RC_H), I_c) < 1e-12,
        f"{None if r1 is None else ((r1.get('cjunc') or {}).get('n_contracted'), I_of(r1, RC_N, vox=RC_H))} ↔ {I_c}")
    #  (바) 다른 셀 자기 접근 · c = 1 — ★ 10-21 (Q-B) 꼴 = XC (교차 접점 (1.9,1.5,2.5) · 옛 KU 는 쌍마다 s 규칙에서 경계 꼴) · SDCP 점 하나가
    #       (0,1,2) (다리 1 셀 (1,1,2) 옆 빈 셀 = 매달린 셀 · 다른 VGCF 셀과 면을 안 나눈다) · 근접 (중심 ↔ 간선 접점 1.4 − r 0.5 ≤ tol 1.0) →
    #       교차 자기 접합 축약 · 면 (1,1,2)|(2,1,2) 절단 그대로 (손 회로 = 그 두 노드 합침)
    sdk = rows([[(0.5, 1.5, 2.5)]], phase=5, kind=0, fid0=700)
    Pk = cat_rows(rows(XC), sdk)
    sidk, _ = bed(Pk, XC_N)
    seqk = seq_cells(XC[0])
    ixk = {c: seqk.index(c) for c in seqk}
    rk = _try(lambda: registry(sidk, Pk, s_min_um=5.0, tol_sj_um=1.0, r_sdcp_um=0.5), None)
    rkc = _try(lambda: solve(sidk, sig_e(), XC_N, plan(rk, 1e3, sdcp_mod={'c': 1.0})), None)
    I_k = chain_ref(len(seqk), merge=[(ixk[(1, 1, 2)], ixk[(2, 1, 2)])])
    chk('RCA03 (바) 다른 셀 자기 접근 (교차) · c = 1 — 근접 자기 접합 축약 1 · 면 절단 (손 회로 1e-12)',
        rkc is not None and (rkc.get('cjunc') or {}).get('n_contracted') == 1 and rel(I_of(rkc, XC_N), I_k) < 1e-12,
        f"{None if rkc is None else ((rkc.get('cjunc') or {}).get('n_contracted'), I_of(rkc, XC_N))} ↔ {I_k}")
    rki = _try(lambda: solve(sidk, sig_e(), XC_N, plan(rk, math.inf, allow_rj_limits=True)), None)
    chk('RCA03 (바) 다른 셀 자기 접근 · R_j = ∞ → 면 절단 · 간선 없음 → 사슬 그대로 (1e-12)',
        rki is not None and rel(I_of(rki, XC_N), chain_ref(len(seqk))) < 1e-12)


# ── RCA04 (Q2) 픽스처 — T1-11 꼴 (A 의 접점 (1.5,1.5,3.0) 이 (1,1,2) · (1,1,3) 중심에서 등거리) · 이진 정확 점 (축 정렬 · 간격 0.25)
T4_N = (6, 3, 8)
T4_A = [(1.5, 1.5, 0.5), (1.5, 1.5, 5.5)]
T4_A_FAR = [(1.5, 1.5, 0.5), (1.5, 1.5, 5.5), (1.25, 1.5, 5.5)]     # 먼 끝 (셀 (1,1,5) 안) 만 바꿈 → 정준 방향 (사전식 작은 끝) 이 뒤집힌다
T4_B = [(2.5, 1.5, 3.0), (4.5, 1.5, 3.0), (4.5, 1.5, 7.5)]


def densify_exact(verts, step):
    """축 정렬 꼭짓점 폴리라인 → 간격 step 의 정확 점열 (a + u·(step·i) · 이진 정확) — 공선 세분이 같은 기하를 비트로 준다."""
    V = np.asarray(verts, np.float64)
    out = [V[0]]
    for a_, b_ in zip(V[:-1], V[1:]):
        d = b_ - a_
        assert np.count_nonzero(d) == 1, '축 정렬 선분만'
        L = float(np.abs(d).sum())
        u = d / L
        n = int(round(L / step))
        assert n * step == L, '간격의 정수배 길이만'
        for i in range(1, n + 1):
            out.append(a_ + u * (step * i))
    return np.asarray(out)


def rows_exact(polys, step=0.25, fids=None, fid0=10):
    P, PH, F, K = [], [], [], []
    for i, v in enumerate(polys):
        pts = densify_exact(v, step)
        f = fids[i] if fids is not None else fid0 + 10 * i
        P.append(pts); PH.append(np.full(len(pts), 2)); F.append(np.full(len(pts), f)); K.append(np.full(len(pts), 1))
    return (np.vstack(P), np.concatenate(PH).astype(np.int64), np.concatenate(F).astype(np.int64),
            np.concatenate(K).astype(np.int64))


def _solve_full(addr, n, rj=1e3, **kw):
    sid, _ = bed(addr, n)
    reg = registry(sid, addr, **kw)
    res = solve(sid, sig_e(), n, plan(reg, rj))
    return sid, reg, res


@case('RCA04')
def t_rca04_port():
    rj = 1e3
    want = chain_I([G_PL] + [G_AX] * 2 + [1e4 / rj] + [G_AX] * 6 + [G_PL])       # 포트 (1,1,2) 회로 (T1-11)
    b0 = _try(lambda: _solve_full(rows_exact([T4_A, T4_B]), T4_N), None)
    bf = _try(lambda: _solve_full(rows_exact([T4_A_FAR, T4_B]), T4_N), None)
    ok = b0 is not None and bf is not None
    p0 = _pcells(b0[1], 0, 'i') if ok else None
    pf = _pcells(bf[1], 0, 'i') if ok else None
    chk('RCA04 (가) 동률 접점 → 셀 정수 좌표 사전식 최소 (1,1,2) · 먼 끝만 바꿔 정준 방향이 뒤집혀도 같은 포트 · σ = 손 회로 · '
        '간선 원장 · σ 비트 같음 (옛 = 정준 경로 번호 → (1,1,3) 로 뒤집힘)',
        ok and p0 == (1, 1, 2) and pf == (1, 1, 2) and rel(I_of(b0[2], T4_N), want) < 1e-12
        and sys_bytes(b0[2]) == sys_bytes(bf[2])
        and np.float64(b0[2]['sigma_eff']).tobytes() == np.float64(bf[2]['sigma_eff']).tobytes(),
        f'포트 {p0} · {pf} · I {None if not ok else (I_of(b0[2], T4_N), I_of(bf[2], T4_N))} ↔ {want}')
    br = _try(lambda: _solve_full(rows_exact([T4_A[::-1], T4_B[::-1]]), T4_N), None)
    bs = _try(lambda: _solve_full(rows_exact([T4_A, T4_B], step=0.125), T4_N), None)
    for nm, o in (('경로 반전 (두 섬유 점 역순)', br), ('공선 세분 (간격 0.25 → 0.125 · 이진 정확 중간점)', bs)):
        chk(f'RCA04 (나) {nm} → sid · 포트 · 간선 원장 · σ 비트 같음',
            ok and o is not None and o[0].tobytes() == b0[0].tobytes() and _pcells(o[1], 0, 'i') == p0
            and _pcells(o[1], 0, 'j') == _pcells(b0[1], 0, 'j') and sys_bytes(o[2]) == sys_bytes(b0[2])
            and np.float64(o[2]['sigma_eff']).tobytes() == np.float64(b0[2]['sigma_eff']).tobytes())
    #  (다) fid 재명명 — 교차 셀 (1,1,3) 에 멤버십 둘 (추가 dof) 인 LX: 옛 = fid 순으로 주 dof · 추가 dof 가 갈려 간선 원장이 바뀐다
    lx1 = _try(lambda: _solve_full(rows(LX, fids=[10, 20]), LX_N), None)
    lx2 = _try(lambda: _solve_full(rows(LX, fids=[20, 10]), LX_N), None)
    chk('RCA04 (다) fid 재명명 (교차 셀 추가 dof 침대 LX · 10 ↔ 20) → 포트 셀 · 간선 원장 (u · v · G · 판) · σ 비트 같음',
        lx1 is not None and lx2 is not None and lx1[2]['n_dof'] == lx2[2]['n_dof']
        and sorted([_pcells(lx1[1], 0, 'i'), _pcells(lx1[1], 0, 'j')]) == sorted([_pcells(lx2[1], 0, 'i'), _pcells(lx2[1], 0, 'j')])
        and sys_bytes(lx1[2]) == sys_bytes(lx2[2])
        and np.float64(lx1[2]['sigma_eff']).tobytes() == np.float64(lx2[2]['sigma_eff']).tobytes(),
        'sys 다름' if (lx1 and lx2 and sys_bytes(lx1[2]) != sys_bytes(lx2[2])) else '')
    #  (라) 판별력 — 같은 점을 무작위로 섞은 경로 (다른 기하) 는 같지 않다
    rng = np.random.default_rng(1021)
    A_ = densify_exact(T4_A, 0.25)
    sh = np.concatenate([A_[:1], A_[1:-1][rng.permutation(len(A_) - 2)], A_[-1:]])
    Bp = rows_exact([T4_B], fid0=20)
    Ps = (np.vstack([sh, Bp[0]]), np.concatenate([np.full(len(sh), 2), Bp[1]]), np.concatenate([np.full(len(sh), 10), Bp[2]]),
          np.concatenate([np.ones(len(sh), np.int64), Bp[3]]))
    bx = _try(lambda: _solve_full(Ps, T4_N), None)
    chk('RCA04 (라) 판별력 — 무작위 점 섞기 (다른 기하) → σ 또는 간선 원장이 다르다 (반전 · 세분과 구별)',
        ok and (bx is None or sys_bytes(bx[2]) != sys_bytes(b0[2])
                or np.float64(bx[2]['sigma_eff']).tobytes() != np.float64(b0[2]['sigma_eff']).tobytes()))
    chk('RCA04 (마) 원장 규칙 이름 — 포트 = ε 띠 · 사전식 셀 좌표 (경로 번호 아님) · 경로 순서 = 기하 정준 (fid 무관)',
        ok and 'lex' in str(b0[1]['rules'].get('port', '')) and 'seq' not in str(b0[1]['rules'].get('port', ''))
        and bool(b0[1]['rules'].get('order')), f"{b0[1]['rules'] if ok else None}")


# ── RCA05 (Q3) — Codex 5 노드 회로 + 같은 꼴 침대 (CX) ──
#  CX: A 세로 (1,1,0..10) 아래 판 · B 는 x 2.1 에서 위 (z 10.5) 부터 아래 (z 1.2) 로 내려와 +x 로 돌아 (6.5, ·, 1.2) 에서 위로 위 판.
#  두 가닥의 단자가 접촉의 같은 끝 (z ≈ 1) — Codex 회로 ("두 가닥 왼쪽 끝 사이 전압") 꼴.  닿음 길이: A 쪽 = z [0.5, 10.5] 전부 (B 까지
#  거리 ≤ 1 · 손계산) = 10.0 · B 쪽 = 9.3 + 0.4 = 9.7 → L_c = 10.0 = 5 L_par · k = 5 · 간선 G = (5/R_j,0)/5 · 등분점 z = 1.5 · 3.5 ·
#  5.5 · 7.5 · 9.5 (A 셀 중심 · 동률 없음) → 포트 (1,1,z) ↔ (2,1,z).  R_j,0 = 200 Ω → 간선 g = 50 = G_AX/2 = 두 축 면 직렬 →
#  홀수 z 의 두 레일 (A1..A9 · B1..B9) = Codex 5 노드 회로 × 50.
CX_N = (8, 3, 14)
CX = [[(1.5, 1.5, 0.5), (1.5, 1.5, 10.5)], [(2.1, 1.5, 10.5), (2.1, 1.5, 1.2), (6.5, 1.5, 1.2), (6.5, 1.5, 13.5)]]
CODEX_G = {'distributed': 1.366013071895, 'left': 5.0, 'centre': 0.238095238095}


def _rails(n, axial, junction, src, snk, lump=None):
    """두 레일 (각 n 노드 · 축 g axial) · 접합 (g junction — 각 위치 · 또는 lump=(위치, 총 G)) · src → snk 단자 G (Codex 회로 꼴)."""
    E = [(r * n + i, r * n + i + 1, axial) for r in range(2) for i in range(n - 1)]
    if lump is None:
        E += [(i, n + i, junction) for i in range(n)]
    else:
        E += [(lump[0], n + lump[0], lump[1])]
    L = np.zeros((2 * n, 2 * n))
    for a_, b_, g in E:
        L[a_, a_] += g; L[b_, b_] += g; L[a_, b_] -= g; L[b_, a_] -= g
    free = [i for i in range(2 * n) if i not in (src, snk)]
    u = np.zeros(2 * n); u[src] = 1.0
    u[free] = np.linalg.solve(L[np.ix_(free, free)], -L[free, src])
    return float((L @ u)[src])


def _cx_ref(rj, contract=(), cut=(), ptfe_extra=()):
    """CX 손 회로 — A 노드 0..10 · B 노드 = B 셀 열 (seq) · 등분 접합 z ∈ {1,3,5,7,9} (g = 1e4/R_j) — contract (z 축약) · cut (z 절단)."""
    seqA = seq_cells(CX[0]); seqB = seq_cells(CX[1])
    nA = len(seqA)
    ia = {c: i for i, c in enumerate(seqA)}
    ib = {c: nA + i for i, c in enumerate(seqB)}
    E = [(i, i + 1, G_AX) for i in range(nA - 1)] + [(nA + i, nA + i + 1, G_AX) for i in range(len(seqB) - 1)]
    merges = []
    for z in (1, 3, 5, 7, 9):
        a_, b_ = ia[(1, 1, z)], ib[(2, 1, z)]
        if z in cut:
            continue
        if z in contract:
            merges.append((a_, b_))
        else:
            E.append((a_, b_, 1e4 / rj))
    rep = list(range(nA + len(seqB)))
    for a_, b_ in merges:
        rep[b_] = a_
    E = [(rep[a_], rep[b_], g) for a_, b_, g in E if rep[a_] != rep[b_]]
    return ref_I(nA + len(seqB), E, [(0, G_PL)], [(rep[nA + len(seqB) - 1], G_PL)])


#  RCA04-V — 두 VGCF 가 정확히 같은 점에서 시작하는 V 꼴 (첫 선분 방향 (1,0,1) · (2,0,1) — x 성분 둘 다 양수).  옛 경로 순서 키 = 정준 점열
#  사전식 → 첫 점이 같으면 **둘째 점** 이 가른다 → B 만 공선 세분 (0.25 → 0.125) 하면 둘째 점이 시작점 쪽으로 다가와 순서가 뒤집힌다 (조각 ·
#  dof 번호 · 계 바이트 · σ 끝자리 — 10-21 사전 공격 리뷰 탐침 8.55011429066427 ↔ …29).  새 키 = (정준 첫 점, 정준 끝 점, 점열) — 끝점은
#  공선 세분 · 점 역순에 불변.  ⚠ 남은 한계: 두 끝점이 **다** 같은 두 경로 · 닫힌 고리 (끝점 같음) 는 점열이 가른다 (세분 의존).
#  ⚠ 이 접촉은 길다 (L_c 3.13 > L_par 2 → k 2 · 배율 1.565) — 접합 G = 배율/k·1e4/R_j 의 L_c 가 선분별 닿음 길이의 **부동소수 합** 이라
#    (정확하지 않은) 세분에서는 G 가 끝자리 몇 ulp 다를 수 있다 → 계의 구조 (u · v · 부류 · 판) 는 비트 · G · σ 는 상대 1e-13 로 본다
#    (k = 1 점 접합 · 이진 정확 세분의 비트 같음 = RCA04 · PCP).
VSH_N = (6, 3, 8)
VSH = [[(1.25, 1.5, 0.5), (3.25, 1.5, 2.5), (3.25, 1.5, 7.5)], [(1.25, 1.5, 0.5), (5.25, 1.5, 2.5), (5.25, 1.5, 7.5)]]


@case('RCA04-V')
def t_rca04_vshape():
    def run(stepB, fids=(10, 20), rev=False):
        vb = VSH[1][::-1] if rev else VSH[1]
        P = cat_rows(rows([VSH[0]], fids=[fids[0]]), rows([vb], step=stepB, fids=[fids[1]]))
        return _try(lambda: _solve_full(P, VSH_N), None)

    def struct(o):
        s = (o[2].get('_cjunc') or {}).get('sys') or {}
        return tuple(np.asarray(s[k]).tobytes() for k in ('u', 'v', 'CAT', 'Ab', 'gb', 'At', 'gt')) if s else None

    def g_rel(o, b):
        ga, gb_ = np.asarray(o[2]['_cjunc']['sys']['G']), np.asarray(b[2]['_cjunc']['sys']['G'])
        return float(np.max(np.abs(ga - gb_) / np.abs(gb_))) if ga.shape == gb_.shape else math.inf
    b0 = run(0.25)
    order0 = None if b0 is None else [int(b0[1]['positions']['fid'][np.flatnonzero(b0[1]['positions']['piece'] == g)[0]])
                                      for g in sorted(set(b0[1]['positions']['piece'].tolist()))]
    chk('RCA04-V 바탕 — 접촉 instance 1 (긴 접촉 · k 2) · 정준 경로 순서 = A (끝점 (3.25,…) < (5.25,…)) 먼저',
        b0 is not None and len(b0[1]['instances']['fi']) == 1 and int(b0[1]['instances']['nsub'][0]) == 2 and order0 == [10, 20],
        f'{order0}')
    for nm, o in (('B 공선 세분 0.125', run(0.125)), ('fid 재명명', run(0.25, (20, 10))), ('세분 + 재명명', run(0.125, (20, 10))),
                  ('B 점 역순', run(0.25, rev=True))):
        ok_ = b0 is not None and o is not None
        chk(f'RCA04-V {nm} → 같은 sid · 간선 포트 셀 · 계 구조 (u · v · 부류 · 판) 비트 같음 · G · σ 상대 ≤ 1e-13 (L_c 합 반올림)',
            ok_ and o[0].tobytes() == b0[0].tobytes() and _sub_cells(o[1]) == _sub_cells(b0[1]) and struct(o) == struct(b0)
            and g_rel(o, b0) <= 1e-13 and rel(o[2]['sigma_eff'], b0[2]['sigma_eff']) <= 1e-13,
            f"{None if not ok_ else (repr(o[2]['sigma_eff']), _sub_cells(o[1]), g_rel(o, b0))} ↔ "
            f"{None if b0 is None else (repr(b0[2]['sigma_eff']), _sub_cells(b0[1]))}")


#  RCA04-EPS — T1-11 꼴을 비이진 원점 (0.6, 0.6, 0.6) · (0.123, 0.456, 0.789) 으로 통째로 옮긴 침대: 접점 (A 위 z 3 + o_z) 이 두 셀
#  (1,1,2) · (1,1,3) 중심에서 수학적으로 등거리인데 반올림으로 (1,1,3) 쪽이 4.4e-16 µm² 가깝게 계산된다 (10-21 변이 M3 생존 → 보탬 ·
#  시험은 구현 뒤).  ε 띠 (1e-9 µm²) 동률 → 셀 정수 좌표 사전식 최소 (1,1,2) · 동률 표지 · σ = 옮기기 전 침대 · 손 회로 (1e-12).
#  ε 띠를 빼면 (정확 최소만) 반올림이 포트를 (1,1,3) 으로 정한다 (원점 이동에 포트가 바뀐다).
@case('RCA04-EPS')
def t_rca04_eps():
    rj = 1e3
    want = chain_I([G_PL] + [G_AX] * 2 + [1e4 / rj] + [G_AX] * 6 + [G_PL])       # 포트 (1,1,2) 회로 (T1-11)
    b0 = _try(lambda: _solve_full(rows([T4_A, T4_B]), T4_N), None)
    for o in ((0.6, 0.6, 0.6), (0.123, 0.456, 0.789)):
        for nm, A in (('A', T4_A), ('A 먼 끝 바꿈', T4_A_FAR)):
            sh = lambda poly: [tuple(np.asarray(p, np.float64) + np.asarray(o)) for p in poly]   # noqa: E731
            P = rows([sh(A), sh(T4_B)])
            sid = _try(lambda: bed(P, T4_N, lo=o)[0], None)
            reg = _try(lambda: registry(sid, P, lo=o), None)
            r = _try(lambda: solve(sid, sig_e(), T4_N, plan(reg, rj)), None) if reg is not None else None
            I = (reg or {}).get('instances') or {}
            chk(f'RCA04-EPS 원점 {o} · {nm} — 같은 sid · ε 띠 동률 → 포트 (1,1,2) · 동률 표지 · σ = 옮기기 전 · 손 회로 (1e-12)',
                b0 is not None and sid is not None and r is not None and sid.tobytes() == b0[0].tobytes() and len(I.get('fi', [])) == 1
                and _pcells(reg, 0, 'i') == (1, 1, 2) and bool(I['tie_i'][0]) and rel(I_of(r, T4_N), want) < 1e-12
                and rel(r['sigma_eff'], b0[2]['sigma_eff']) < 1e-12,
                f"{None if reg is None else (_pcells(reg, 0, 'i'), bool(I['tie_i'][0]) if len(I.get('fi', [])) else None)} · "
                f"{None if r is None else I_of(r, T4_N)} ↔ {want}")


@case('RCA04-DUP')
def t_rca04_duplicate():
    """같은 기하 경로 둘 (fid 둘) — 기하 정준 순서 (`CJUNC_ORDER_RULE`) 로 갈리지 않는 짝 (★ 10-21 RCA-04 · 시험은 구현 뒤에 보탬 — 고치기 전
    판 47d23baba 에서 역순 꼴이 실패하는 것은 따로 확인): 정확 중복 (점 배열 비트 같음) = 옛 'duplicate_path' · 점 역순 중복 (정준 점열 같음 ·
    점 배열 다름) = 'duplicate_path_reversed' → 정량 계획 = 거부 (입구 관문 ValueError) · 시험 모드 (quantitative=False) 는 받는다 ·
    한 점만 다른 (공선 아님) 두 경로 = 거부 없음 (중복 아님)."""
    A = [(1.5, 1.5, 0.5), (1.5, 1.5, 5.5)]
    A2 = [(1.5, 1.5, 0.5), (1.5, 1.5, 3.0), (1.6, 1.5, 5.5)]
    N = (3, 3, 7)
    for nm, polys, want in (('정확 중복', [A, A], 'duplicate_path'), ('역순 중복', [A, A[::-1]], 'duplicate_path_reversed'),
                            ('한 점만 다른 두 경로', [A, A2], None)):
        P = rows(polys)
        sid, _ = bed(P, N)
        reg = _try(lambda: registry(sid, P), None)
        codes = [x.get('code') for x in (reg or {}).get('rejections', [])]
        pq = _try(lambda: plan(reg, 1e3), None)
        pt = _try(lambda: plan(reg, 1e3, quantitative=False), None)
        if want is None:
            chk(f'RCA04-DUP {nm} → 중복 거부 사유 없음', reg is not None and not any(str(c).startswith('duplicate') for c in codes), codes)
            continue
        chk(f'RCA04-DUP {nm} → 원장 사유 {want} · 정량 계획 = 입구 거부 · 시험 모드 계획 = 사유 없음',
            reg is not None and want in codes and pq is not None and any(x.get('code') == want for x in pq['rejections'])
            and raises(lambda: CJ.cjunc_require_quantitative(pq, sid, H)) and pt is not None and pt['rejections'] == [],
            f'{codes}')


@case('RCA05')
def t_rca05_distributed():
    gd = _rails(5, 1.0, 1.0, 0, 5)
    gl = _rails(5, 1.0, 1.0, 0, 5, lump=(0, 5.0))
    gc = _rails(5, 1.0, 1.0, 0, 5, lump=(2, 5.0))
    chk('RCA05 Codex 5 노드 회로 재현 — 분산 1.366013071895 · 총 5 S 왼쪽 집중 5.0 · 중앙 집중 0.238095238095 S (1e-12)',
        abs(gd - CODEX_G['distributed']) < 1e-12 and abs(gl - CODEX_G['left']) < 1e-12 and abs(gc - CODEX_G['centre']) < 1e-12,
        f'{gd} {gl} {gc}')
    P = rows(CX)
    sid, _ = bed(P, CX_N)
    reg = _try(lambda: registry(sid, P), None)
    inst = (reg or {}).get('instances') or {}
    ok_i = reg is not None and len(inst.get('fi', ())) == 1 and abs(float(inst['Lc'][0]) - 10.0) < 1e-12
    chk('RCA05 CX — instance 하나 · L_c = 10.0 = 5 L_par (손계산 닿음 길이 · 1e-12)', ok_i,
        f"{None if reg is None else (len(inst.get('fi', ())), inst.get('Lc'))}")
    sc = _sub_cells(reg) if reg is not None else None
    want_c = [((1, 1, z), (2, 1, z)) for z in (1, 3, 5, 7, 9)]
    chk('RCA05 CX — 분산 간선 k = ceil(L_c/L_par) = 5 · 등분점 최근접 포트 (1,1,z) ↔ (2,1,z) z = 1 · 3 · 5 · 7 · 9',
        sc is not None and sorted(sc) == want_c, f'{sc}')
    rj = 200.0
    pl = _try(lambda: plan(reg, rj), None)
    g = None if pl is None else np.asarray(pl['g_code'], np.float64)
    chk('RCA05 CX — 간선마다 G = (총 max(1, L_c/L_par)/R_j,0)/k = 1e4/R_j (5 간선 · 상대 1e-15 · 총 G 보존 5e4/R_j)',
        g is not None and len(g) == 5 and np.all(np.abs(g - 1e4 / rj) <= 1e-15 * (1e4 / rj))
        and abs(float(g.sum()) - 5e4 / rj) <= 1e-12 * 5e4 / rj, f'{g}')
    I = _try(lambda: I_of(solve(sid, sig_e(), CX_N, pl), CX_N))
    want = _cx_ref(rj)
    rails = _rails(5, G_AX / 2.0, 1e4 / rj, 0, 5)
    lead = 1.0 / (1.0 / G_PL + 1.0 / G_AX + 1.0 / rails + 16.0 / G_AX + 1.0 / G_PL)
    chk('RCA05 CX — σ = 손 회로 (판 + A0→A1 + 두 레일 사다리 + B 리드 16 면 + 판 · 1e-12) · 두 레일 = Codex 분산 회로 × 50 (1e-12)',
        rel(I, want) < 1e-12 and abs(rails / 50.0 - CODEX_G['distributed']) < 1e-12 and rel(want, lead) < 1e-12,
        f'{I} ↔ {want} · 레일 {rails / 50.0} · 직렬 {lead}')
    I_left = 1.0 / (1.0 / G_PL + 1.0 / G_AX + 1.0 / (5e4 / rj) + 16.0 / G_AX + 1.0 / G_PL)
    chk('RCA05 CX — 분산 ≠ 한 포트 집중 (왼쪽 끝 집중 회로와 다르다 · 판별력)', rel(want, I_left) > 1e-3, f'{want} {I_left}')
    #  (나) 간선마다 PTFE 덮임 (P1) — LP 의 첫 등분점 (z 2.7) 위를 가로지르는 PTFE 피브릴: 덮인 간선 하나만 절단
    Plp = rows(LP)
    rP, tP = 0.25, 0.25
    pt = _ptfe_rows([[(1.8, 0.5, 2.7), (1.8, 2.5, 2.7)]])
    allr = cat_rows(Plp, pt)
    sidp, _ = bed(allr, LP_N, stamp=allr[1] != 4)
    regp = _try(lambda: registry(sidp, allr, tol_P_um=tP, r_ptfe_um=rP), None)
    sp = _sub(regp) if regp is not None else None
    rjp = 1e3
    rp = _try(lambda: solve(sidp, sig_e(), LP_N, plan(regp, rjp, ptfe_stamp='face_alpha', ptfe_jlaw='P1')), None)
    want_p = _lp_ref(rjp, cut=(2,))
    chk('RCA05 (나) 간선마다 PTFE 덮임 — LP 등분 간선 셋 중 z 2 간선만 덮임 · P1 = 그 간선만 절단 · σ = 손 회로 (1e-12 · 옛 = '
        'instance 대표점 하나로 전체 절단)',
        sp is not None and list(np.asarray(sp['ptfe_cov'], bool)) == [True, False, False] and rp is not None
        and (rp.get('cjunc') or {}).get('n_cut_p1') == 1 and rel(I_of(rp, LP_N), want_p) < 1e-12,
        f"{None if sp is None else list(sp['ptfe_cov'])} · {None if rp is None else (rp.get('reason'), I_of(rp, LP_N))} ↔ {want_p}")
    #  (다) 간선마다 SDCP 근접 — z 6 간선 옆 SDCP 점: c = 1 = 그 간선만 축약
    sd = rows([[(1.8, 2.5, 6.7)]], phase=5, kind=0, fid0=700)
    alls = cat_rows(Plp, sd)
    sids, _ = bed(alls, LP_N)
    regs = _try(lambda: registry(sids, alls, tol_sj_um=0.6, r_sdcp_um=0.5), None)
    ss = _sub(regs) if regs is not None else None
    rs = _try(lambda: solve(sids, sig_e(), LP_N, plan(regs, rjp, sdcp_mod={'c': 1.0})), None)
    want_s = _lp_ref(rjp, contract=(6,))
    chk('RCA05 (다) 간선마다 SDCP 근접 — z 6 간선만 근접 · c = 1 = 그 간선만 축약 · σ = 손 회로 (1e-12)',
        ss is not None and list(np.asarray(ss['a_sdcp'], bool)) == [False, False, True] and rs is not None
        and (rs.get('cjunc') or {}).get('n_contracted') == 1 and rel(I_of(rs, LP_N), want_s) < 1e-12,
        f"{None if ss is None else list(ss['a_sdcp'])} · {None if rs is None else I_of(rs, LP_N)} ↔ {want_s}")
    #  (라) L_c ≤ L_par → 분산 간선 = instance 하나 = 옛 점 접합 (포트 · 접점 · g 같음)
    P1_ = rows(F1)
    sid1, _ = bed(P1_, F1_N)
    r1 = _try(lambda: registry(sid1, P1_), None)
    s1 = _sub(r1) if r1 is not None else None
    p1 = _try(lambda: plan(r1, 1e3), None)
    chk('RCA05 (라) L_c ≤ L_par (F1) → 분산 간선 하나 = instance (포트 · 접점 같음 · g = 1e4/R_j 비트)',
        s1 is not None and len(s1['inst']) == 1 and int(s1['port_i'][0]) == int(r1['instances']['port_i'][0])
        and int(s1['port_j'][0]) == int(r1['instances']['port_j'][0])
        and np.asarray(s1['cp'])[0].tobytes() == np.asarray(r1['instances']['cp'])[0].tobytes()
        and p1 is not None and np.float64(p1['g_code'][0]).tobytes() == np.float64(1e4 / 1e3).tobytes())


def _lp_ref(rj, contract=(), cut=()):
    """LP 분산 손 회로 — A (1,1,0..7) · B (2,1,2..10) · 등분 간선 z = 2 · 4 · 6 (g = (3·1e4/R_j)/3) · contract · cut (z)."""
    seqA = [(1, 1, z) for z in range(8)]
    seqB = [(2, 1, z) for z in range(2, 11)]
    nA = len(seqA)
    E = [(i, i + 1, G_AX) for i in range(nA - 1)] + [(nA + i, nA + i + 1, G_AX) for i in range(len(seqB) - 1)]
    rep = list(range(nA + len(seqB)))
    for z in (2, 4, 6):
        a_, b_ = z, nA + (z - 2)
        if z in cut:
            continue
        if z in contract:
            rep[b_] = a_
        else:
            E.append((a_, b_, 3.0 * 1e4 / rj / 3.0))
    E = [(rep[a_], rep[b_], g) for a_, b_, g in E if rep[a_] != rep[b_]]
    return ref_I(nA + len(seqB), E, [(0, G_PL)], [(rep[nA + len(seqB) - 1], G_PL)])


# ── RCA06 (Q4) 픽스처 — A 세로 (1,1,0..20) 아래 판 · B 는 A 아래쪽 (2.1, ·, 1.5) 에서 시작해 +x 로 (3.5) 돌아 위로 위 판 (3,1,1..21) ·
#    A–B 접합 (z 1 · L_c 1.6 < L_par) · A 윗끝 (1,1,20) 과 B (3,1,20) 사이 SDCP 셀 (2,1,20) = SV 면 둘 (융합).
#    R_j,0 = 2e4 Ω (g 0.5): SV 경로가 단자 전류의 ≈ 0.915 · 옛 가드 (SV + SDCP 셀 소산 ≥ VV 접합 소산) = false · SV 면 끊은 판 대비 비 ≈ 10.3
SVX_N = (5, 3, 22)
SVX = [[(1.5, 1.5, 0.5), (1.5, 1.5, 20.5)], [(2.1, 1.5, 1.5), (3.5, 1.5, 1.5), (3.5, 1.5, 21.5)]]
SVX_SDCP = [[(2.5, 1.5, 20.5)]]
SVX_RJ = 2.0e4


def _svx_ref(rj, with_sv=True, s_sdcp=250.0):
    """SVX 손 회로 → (I, φ, 노드 표) — A 0..20 · b0 (2,1,1) · b1..b21 (3,1,1..21) · s (SDCP)."""
    nA = 21
    B0 = nA
    B = [B0 + i for i in range(22)]                   # b0 (2,1,1) · b1..b21 = (3,1,1..21)
    S = B0 + 22
    gsv = 2.0 * SV * s_sdcp / (SV + s_sdcp) * H
    E = [(i, i + 1, G_AX) for i in range(nA - 1)] + [(B[i], B[i + 1], G_AX) for i in range(21)] + [(1, B[0], 1e4 / rj)]
    if with_sv:
        E += [(20, S, gsv), (S, B[20], gsv)]
    nn = S + 1
    L = np.zeros((nn, nn)); b = np.zeros(nn)
    for i, j, g in E:
        L[i, i] += g; L[j, j] += g; L[i, j] -= g; L[j, i] -= g
    L[0, 0] += G_PL; b[0] += G_PL
    L[B[21], B[21]] += G_PL
    if not with_sv:
        L[S, S] += 1.0                                  # 떠 있는 노드 (특이 방지 · 전류 0)
    phi = np.linalg.solve(L, b)
    I = float(G_PL * (1.0 - phi[0]))
    return I, phi, {'gsv': gsv, 'S': S, 'B': B}


@case('RCA06')
def t_rca06_sv():
    P = cat_rows(rows(SVX), rows(SVX_SDCP, phase=5, kind=0, fid0=700))
    sid, _ = bed(P, SVX_N)
    reg = _try(lambda: registry(sid, P, tol_sj_um=0.1, r_sdcp_um=0.5), None)
    I_full, phi, nd = _svx_ref(SVX_RJ)
    I_cut, _, _ = _svx_ref(SVX_RJ, with_sv=False)
    P_sv = nd['gsv'] * ((phi[20] - phi[nd['S']]) ** 2 + (phi[nd['S']] - phi[nd['B'][20]]) ** 2)
    P_vv = (1e4 / SVX_RJ) * (phi[1] - phi[nd['B'][0]]) ** 2
    frac_sv = nd['gsv'] * (phi[20] - phi[nd['S']]) / I_full
    print(f'    RCA06 손 회로: I {I_full:.9g} · SV 끊은 판 {I_cut:.9g} · 비 {I_full / I_cut:.6f} · SV 전류 몫 {frac_sv:.4f} · '
          f'P_SV {P_sv:.4g} < P_VV {P_vv:.4g}')
    chk('RCA06 반례 꼴 (손 회로) — SV 경로 전류 몫 > 0.9 · 옛 가드 (P_SV ≥ P_VV) = false · SV 면 끊은 판 대비 비 > 5',
        frac_sv > 0.9 and P_sv < P_vv and I_full / I_cut > 5.0, f'{frac_sv} {P_sv} {P_vv} {I_full / I_cut}')
    r_off = _try(lambda: solve(sid, sig_e(), SVX_N, plan(reg, SVX_RJ)), None)
    cj = (r_off or {}).get('cjunc') or {}
    cf_off = cj.get('sv_counterfactual')
    chk('RCA06 기본 (노브 끔) — σ = 손 회로 (1e-12) · 기록에 sv_dominant 없음 (지배성 표지 철회) · SV_local_dissipation 진단 있음 · '
        '반사실 = 요청 없음 (칸 없음)',
        r_off is not None and rel(I_of(r_off, SVX_N), I_full) < 1e-12 and 'sv_dominant' not in cj
        and isinstance(cj.get('sv_local_dissipation'), dict) and cf_off is None,
        f"{None if r_off is None else (I_of(r_off, SVX_N), sorted(k for k in cj if k.startswith('sv')))}")
    sld = cj.get('sv_local_dissipation') or {}
    old_guard = None
    if isinstance(cj.get('dissipation_share'), dict):
        dsh = cj['dissipation_share']
        old_guard = (dsh.get('sv_face', 0.0) + dsh.get('sdcp_cell', 0.0)) >= dsh.get('vv_junction', 0.0)
    chk('RCA06 SV_local_dissipation = 국소 소산 몫 (SV 면 + SDCP 셀 · 원장) · 이 반례에서 VV 접합 몫보다 작다 (옛 가드라면 false)',
        isinstance(sld.get('sv_share'), float) and isinstance(sld.get('vv_junction_share'), float)
        and sld['sv_share'] < sld['vv_junction_share'] and old_guard is False, f'{sld} {old_guard}')
    r_cf = _try(lambda: solve(sid, sig_e(), SVX_N, plan(reg, SVX_RJ, sv_counterfactual={'threshold': None})), None)
    cf = ((r_cf or {}).get('cjunc') or {}).get('sv_counterfactual') or {}
    chk('RCA06 반사실 대조 (노브 켬 · 문턱 없음) — sv_counterfactual_ratio = 손 회로 I / SV 면 끊은 I (1e-10) · SV 면 2 끊음 · '
        '표지 없음 (문턱 없음 = 판정 문장 없음)',
        cf.get('status') == 'computed' and rel(float(cf.get('sv_counterfactual_ratio', math.nan)), I_full / I_cut) < 1e-10
        and cf.get('n_sv_faces_cut') == 2 and cf.get('flag') is None, f'{cf}')
    r_th = _try(lambda: solve(sid, sig_e(), SVX_N, plan(reg, SVX_RJ, sv_counterfactual={'threshold': 2.0})), None)
    ct = ((r_th or {}).get('cjunc') or {}).get('sv_counterfactual') or {}
    chk('RCA06 문턱이 주어질 때만 비교 표지 — 문턱 2.0 (시험 값 · 기본값 아님) · 비 ≈ 10 → SV_DEPENDENT',
        ct.get('flag') == 'SV_DEPENDENT' and ct.get('threshold') == 2.0, f'{ct}')
    bad = [v for v in (0.5, float('nan'), math.inf, True, 'x', -1.0, 10 ** 400, np.bool_(True))
           if not raises(lambda v=v: plan(reg, SVX_RJ, sv_counterfactual={'threshold': v}))]
    chk('RCA06 문턱 = 유한 ≥ 1 실수만 (0.5 · NaN · inf · bool · 문자 · 음수 · float 넘침 정수 10^400 · np.bool_ = 거부 · ValueError/TypeError '
        '로만) · 모르는 칸 거부',
        not bad and raises(lambda: plan(reg, SVX_RJ, sv_counterfactual={'threshold': None, 'x': 1})), f'통과 {bad}')
    P2 = rows(F1)
    sid2, _ = bed(P2, F1_N)
    r2 = _try(lambda: solve(sid2, sig_e(), F1_N, plan(registry(sid2, P2), 1e3, sv_counterfactual={'threshold': None})), None)
    c2 = ((r2 or {}).get('cjunc') or {}).get('sv_counterfactual') or {}
    chk('RCA06 SDCP 없음 (SBE 꼴) — SV 면 0 · 비 = 1 정확 (같은 계를 다시 푼다)',
        c2.get('status') == 'computed' and c2.get('n_sv_faces_cut') == 0 and c2.get('sv_counterfactual_ratio') == 1.0, f'{c2}')
    #  주 해 미수렴 (info ≠ 0 표지) → 반사실 비를 내지 않는다 (분자 G 를 믿을 수 없다 · status main_unconverged · 표지 없음)
    from scipy.sparse.linalg import spsolve
    old = S3._solve_cg

    def _flagged(L, b, *a, **k):
        return spsolve(L.tocsc(), b), 1
    S3._solve_cg = _flagged
    try:
        r_u = _try(lambda: S3.solve_sigma_z(sid, sig_e(), H, z_top_um=float(SVX_N[2]) * H, z_bot_um=0.0,
                                            cjunc=plan(reg, SVX_RJ, sv_counterfactual={'threshold': 2.0})), None)
    finally:
        S3._solve_cg = old
    cu = ((r_u or {}).get('cjunc') or {}).get('sv_counterfactual') or {}
    #  ★ 10-21 (Q-D) — 미수렴 기록의 종류도 원장 정본 상수 (반사실 = SV 다리만 끊음 · 옛 'counterfactual_cut_sv_faces' 문자열 고정 아님)
    chk('RCA06 주 해 미수렴 → 반사실 비 없음 (status main_unconverged · 비 None · 표지 None · 해 unconverged True · 종류 = CJUNC_SV_CF_KIND)',
        r_u is not None and r_u.get('unconverged') is True and cu.get('status') == 'main_unconverged'
        and cu.get('sv_counterfactual_ratio') is None and cu.get('flag') is None
        and cu.get('kind') == getattr(CJ, 'CJUNC_SV_CF_KIND', None), f"{None if r_u is None else r_u.get('unconverged')} {cu}")


@case('RCA06-H')
def t_rca06_hygiene():
    """반사실 대조의 위생 (10-21 사전 공격 리뷰 · 증서 ↔ 결과 결합 · 전역 상태) — 반사실 솔브는 진단이다:
    ① 주 해의 출처 기록 (모듈 전역 `LAST_BACKEND` · `LAST_CG` — 매니페스트 'backend_last_solve' 가 읽는다) 을 바꾸지 않고, 자기 솔브의
       backend 는 자기 기록에 싣는다 (노브 켬 = 주 결과 출처가 노브 끔과 같다)
    ② 수렴 증서 (`CONV_CERT`) 를 켠 런에서는 반사실 솔브도 **같은 증서 함수** (`step3_conv_cert.certify`) 를 지나야 비를 낸다 —
       증서 실패 = 비 없음 · 표지 없음 (주 해 증서만 보고 분모를 믿지 않는다)."""
    P = cat_rows(rows(SVX), rows(SVX_SDCP, phase=5, kind=0, fid0=700))
    sid, _ = bed(P, SVX_N)
    reg = _try(lambda: registry(sid, P, tol_sj_um=0.1, r_sdcp_um=0.5), None)
    I_full, _, _ = _svx_ref(SVX_RJ)
    I_cut, _, _ = _svx_ref(SVX_RJ, with_sv=False)
    from scipy.sparse.linalg import spsolve

    def _run(fake, cert=False, th=None):
        old_s, old_cc, old_rt = S3._solve_cg, S3.CONV_CERT, S3.CG_RTOL
        S3._solve_cg = fake
        S3.CONV_CERT = bool(cert)
        if cert:
            S3.CG_RTOL = 1.0e-12                            # 증서 ⓐ 봉인 (정지 rtol ≤ 1e-12) — 직접 풀이 픽스처
        try:
            return _try(lambda: quiet(S3.solve_sigma_z, sid, sig_e(), H, z_top_um=float(SVX_N[2]) * H, z_bot_um=0.0,
                                      cjunc=plan(reg, SVX_RJ, sv_counterfactual={'threshold': th})), None)
        finally:
            S3._solve_cg, S3.CONV_CERT, S3.CG_RTOL = old_s, old_cc, old_rt

    calls = [0]

    def _marked(L, b, *a, **k):                             # 첫 호출 = 주 해 · 둘째 = 반사실 — backend 표지를 다르게 남긴다
        calls[0] += 1
        S3.LAST_BACKEND.update(requested='cpu', used=('cpu-main' if calls[0] == 1 else 'cpu-counterfactual'),
                               fallback_reason=None, precond='jacobi')
        S3.LAST_CG['iters'] = 111 if calls[0] == 1 else 777
        return spsolve(L.tocsc(), b), 0
    bk0, cg0 = dict(S3.LAST_BACKEND), dict(S3.LAST_CG)
    try:
        r1 = _run(_marked)
        bk1, cg1 = dict(S3.LAST_BACKEND), dict(S3.LAST_CG)
    finally:
        S3.LAST_BACKEND.clear(); S3.LAST_BACKEND.update(bk0); S3.LAST_CG.clear(); S3.LAST_CG.update(cg0)
    c1 = ((r1 or {}).get('cjunc') or {}).get('sv_counterfactual') or {}
    chk('RCA06-H ① 반사실 솔브 뒤 모듈 전역 출처 = 주 해 그대로 (LAST_BACKEND used cpu-main · LAST_CG iters 111) · 반사실 기록에 자기 '
        'backend (cpu-counterfactual) · 솔브 2 번 · 비 = 손 회로 (1e-10)',
        r1 is not None and calls[0] == 2 and bk1.get('used') == 'cpu-main' and cg1.get('iters') == 111
        and (c1.get('backend_last_solve') or {}).get('used') == 'cpu-counterfactual'
        and c1.get('status') == 'computed' and rel(float(c1.get('sv_counterfactual_ratio') or math.nan), I_full / I_cut) < 1e-10,
        f"calls {calls[0]} · 전역 {bk1.get('used')} / {cg1.get('iters')} · 기록 {c1.get('backend_last_solve')} · {c1.get('status')}")
    chk('RCA06-H ① 증서 끔 = 반사실 기록 conv_cert None (칸 있음 · 증서 없이 CG 술어만)',
        'conv_cert' in c1 and c1['conv_cert'] is None, f"{sorted(c1)}")

    def _direct(L, b, *a, **k):
        return spsolve(L.tocsc(), b), 0
    r2 = _run(_direct, cert=True)
    c2 = ((r2 or {}).get('cjunc') or {}).get('sv_counterfactual') or {}
    cc2 = c2.get('conv_cert') if isinstance(c2.get('conv_cert'), dict) else {}
    chk('RCA06-H ② 증서 켬 (rtol 1e-12 · 직접 풀이) — 주 해 증서 ok · 반사실 솔브도 같은 증서 함수 (판본 conv-cert · ok · ⓐⓑⓒ) · '
        '비 = 손 회로 (1e-10)',
        r2 is not None and (r2.get('conv_cert') or {}).get('ok') is True and r2.get('unconverged') is False
        and cc2.get('ok') is True and cc2.get('version') == getattr(sys.modules.get('step3_conv_cert'), 'CERT_VERSION', '?')
        and cc2.get('pass_a') is True and cc2.get('pass_b') is True and cc2.get('pass_c') is True
        and c2.get('status') == 'computed' and rel(float(c2.get('sv_counterfactual_ratio') or math.nan), I_full / I_cut) < 1e-10,
        f"주 {(r2 or {}).get('conv_cert', {}).get('ok') if r2 else None} · 반사실 {c2.get('status')} {cc2.get('ok')}")
    cc_mod = sys.modules.get('step3_conv_cert') or importlib.import_module('step3_conv_cert')   # 반사실 증서 실패 변이를 끼울 모듈
    real_cert = cc_mod.certify
    n_cert = [0]

    def _cert_fail_second(*a, **k):                          # 둘째 증서 (= 반사실 솔브) 만 실패 — 주 해 증서는 그대로
        n_cert[0] += 1
        out = real_cert(*a, **k)
        if n_cert[0] >= 2:
            out = dict(out, pass_c=False, ok=False)
        return out
    cc_mod.certify = _cert_fail_second
    try:
        r3 = _run(_direct, cert=True, th=2.0)
    finally:
        cc_mod.certify = real_cert
    c3 = ((r3 or {}).get('cjunc') or {}).get('sv_counterfactual') or {}
    chk('RCA06-H ② 반사실 솔브 증서 실패 → 비 없음 · 표지 없음 (문턱 2.0 이어도) · status unconverged · 주 해는 그대로 (증서 ok · σ = 손 회로)',
        r3 is not None and n_cert[0] == 2 and r3.get('unconverged') is False and rel(I_of(r3, SVX_N), I_full) < 1e-12
        and c3.get('status') == 'unconverged' and c3.get('sv_counterfactual_ratio') is None and c3.get('flag') is None
        and (c3.get('conv_cert') or {}).get('ok') is False,
        f"증서 호출 {n_cert[0]} · {c3.get('status')} · 비 {c3.get('sv_counterfactual_ratio')} · 표지 {c3.get('flag')}")
    #  ③ 비 inf ('SV 없이 관통 없음') 는 **위상** (조립 그래프에 관통 성분 없음) 에서만 — 관통 성분이 있는데 푼 I_cut ≤ 0 은 수치 실패다.
    #    SVA = SVX 에서 VV 접합을 빼고 (B 곧은 기둥) A–B 사이 AM 셀 하나 (2,1,10 · σ 1e-9) 를 둔 꼴: SV 를 끊으면 관통 = AM 경로뿐 (I_cut ≈ 1e-9 ·
    #    ‖b‖ = 판 결합 200 의 1e-6 보다 훨씬 작다) → 증서를 끈 CG 술어 (상대 잔차 ≤ 1e-6) 를 지나는 φ 로 I_cut 부호가 뒤집힐 수 있다
    #    (판 전류 = Σ b (1 − φ) 를 −I 로 옮긴 φ · 잔차 ~1e-11).  옛 판 = 'no_through_without_sv' · 비 inf · 문턱 2 에서 SV_DEPENDENT.
    SVA_B = [(3.5, 1.5, 1.5), (3.5, 1.5, 21.5)]
    s_am = 1.0e-9
    PA = cat_rows(rows([SVX[0], SVA_B]), rows(SVX_SDCP, phase=5, kind=0, fid0=700))
    am = (np.array([[2.5, 1.5, 10.5]]), np.array([0.5]), np.array([1], np.int64))
    sidA, _ = bed(PA, SVX_N, am=am)
    regA = _try(lambda: registry(sidA, PA, tol_sj_um=0.1, r_sdcp_um=0.5), None)
    tab = sig_e(s_am=s_am)
    sA = float(tab[int(sidA[2, 1, 10])])
    gva = 2.0 * SV * sA / (SV + sA) * H
    gsv = 2.0 * SV * 250.0 / (SV + 250.0) * H
    nA, nB = 21, 21                                          # A0..A20 = (1,1,0..20) · B1..B21 = (3,1,1..21) · S · M
    Bn = lambda z: nA + z - 1                                # noqa: E731
    S_, M_ = nA + nB, nA + nB + 1
    E0 = [(i, i + 1, G_AX) for i in range(nA - 1)] + [(Bn(z), Bn(z + 1), G_AX) for z in range(1, 21)]
    E_am = [(10, M_, gva), (M_, Bn(10), gva)]
    E_sv = [(20, S_, gsv), (S_, Bn(20), gsv)]
    IA_full = ref_I(M_ + 1, E0 + E_am + E_sv, [(0, G_PL)], [(Bn(21), G_PL)])
    IA_cut = ref_I(M_ + 1, E0 + E_am, [(0, G_PL)], [(Bn(21), G_PL)])

    def _runA(fake):
        old_s = S3._solve_cg
        S3._solve_cg = fake
        try:
            return _try(lambda: quiet(S3.solve_sigma_z, sidA, tab, H, z_top_um=float(SVX_N[2]) * H, z_bot_um=0.0,
                                      cjunc=plan(regA, SVX_RJ, sv_counterfactual={'threshold': 2.0})), None)
        finally:
            S3._solve_cg = old_s
    rA = _runA(_direct)
    cA = ((rA or {}).get('cjunc') or {}).get('sv_counterfactual') or {}
    chk('RCA06-H ③ SVA 양성 대조 — AM 셀 sid 2 · 주 σ = 손 회로 (1e-9) · 반사실 computed · 비 = 손 회로 (1e-3 · I_cut ≈ 1e-9 의 판 전류 상쇄) '
        '· 비 > 1e6 → SV_DEPENDENT',
        rA is not None and int(sidA[2, 1, 10]) == 2 and rel(I_of(rA, SVX_N), IA_full) < 1e-9 and cA.get('status') == 'computed'
        and rel(float(cA.get('sv_counterfactual_ratio') or math.nan), IA_full / IA_cut) < 1e-3
        and IA_full / IA_cut > 1e6 and cA.get('flag') == 'SV_DEPENDENT',
        f"σ {None if rA is None else I_of(rA, SVX_N)} ↔ {IA_full} · {cA.get('status')} · 비 {cA.get('sv_counterfactual_ratio')} ↔ "
        f'{IA_full / IA_cut:.6g}')
    nA_calls = [0]

    def _flip_second(L, b, *a, **k):                         # 둘째 풀이 (반사실) — 정확 해에서 판 전류를 −I 로 옮긴 φ (잔차 ~1e-11)
        nA_calls[0] += 1
        x = spsolve(L.tocsc(), b)
        if nA_calls[0] >= 2:
            nzb = np.flatnonzero(b)
            Ic = float(np.sum(b[nzb] * (1.0 - x[nzb])))
            x = x.copy()
            x[nzb] += 2.0 * Ic / float(np.sum(b[nzb]))
        return x, 0
    rF = _runA(_flip_second)
    cF = ((rF or {}).get('cjunc') or {}).get('sv_counterfactual') or {}
    chk('RCA06-H ③ 관통 성분이 있는데 푼 I_cut ≤ 0 (CG 술어는 통과 · 잔차 ≤ 1e-6) → 비 inf 아님 · 비 None · 표지 None · status ≠ '
        "'no_through_without_sv' (위상 서술 금지)",
        rF is not None and nA_calls[0] == 2 and float(cF.get('G_cut_code') if cF.get('G_cut_code') is not None else 1.0) <= 0.0
        and float(cF.get('resid') if cF.get('resid') is not None else 1.0) <= 1e-6
        and cF.get('status') not in (None, 'computed', 'no_through_without_sv') and cF.get('sv_counterfactual_ratio') is None
        and cF.get('flag') is None,
        f"풀이 {nA_calls[0]} · G_cut {cF.get('G_cut_code')} · 잔차 {cF.get('resid')} · {cF.get('status')} · 비 "
        f"{cF.get('sv_counterfactual_ratio')} · 표지 {cF.get('flag')}")
    #  ④ 분자 (주 해 단자 전류) ≤ 0 이면 비를 내지 않는다 — SVA 에 SDCP σ 도 1e-9 (주 관통 ≈ 2e-9 ≪ 1e-6 × 판 결합) · 첫 풀이 (주 해) 의
    #    판 전류를 −I 로 옮긴 φ (잔차 ~1e-11 · CG 술어 통과 · 주 σ = max(0, ·) = 0 은 옛 생산 술어 그대로 = 이 묶음 밖) → 옛 판 = 반사실을 풀어
    #    'computed' · 비 ≈ −2 (음수 비 게시).
    tab4 = sig_e(s_am=s_am, s_sdcp=1.0e-9)
    n4 = [0]

    def _flip_first(L, b, *a, **k):
        n4[0] += 1
        x = spsolve(L.tocsc(), b)
        if n4[0] == 1:
            nzb = np.flatnonzero(b)
            Ic = float(np.sum(b[nzb] * (1.0 - x[nzb])))
            x = x.copy()
            x[nzb] += 2.0 * Ic / float(np.sum(b[nzb]))
        return x, 0
    old_s = S3._solve_cg
    S3._solve_cg = _flip_first
    try:
        r4 = _try(lambda: quiet(S3.solve_sigma_z, sidA, tab4, H, z_top_um=float(SVX_N[2]) * H, z_bot_um=0.0,
                                cjunc=plan(regA, SVX_RJ, sv_counterfactual={'threshold': 2.0})), None)
    finally:
        S3._solve_cg = old_s
    c4 = ((r4 or {}).get('cjunc') or {}).get('sv_counterfactual') or {}
    chk('RCA06-H ④ 주 해 단자 전류 ≤ 0 (CG 술어 통과) → 반사실을 풀지 않는다 · 비 None · 표지 None · status nonpositive_full_current',
        r4 is not None and n4[0] == 1 and float(c4.get('G_full_code') if c4.get('G_full_code') is not None else 1.0) <= 0.0
        and c4.get('status') == 'nonpositive_full_current' and c4.get('sv_counterfactual_ratio') is None and c4.get('flag') is None,
        f"풀이 {n4[0]} · G_full {c4.get('G_full_code')} · {c4.get('status')} · 비 {c4.get('sv_counterfactual_ratio')}")
    #  ⑤ (지킴) 위상 inf — SVA 에서 AM 셀도 뺀 꼴 (A–B 가 SDCP 로만 이어진다): SV 면을 끊으면 조립 그래프에 관통 성분이 없다 → 풀지 않고
    #    'no_through_without_sv' · 비 inf · 문턱 2 → SV_DEPENDENT · G_cut 0 (주 σ = 손 회로).
    sidN, _ = bed(PA, SVX_N)
    regN = _try(lambda: registry(sidN, PA, tol_sj_um=0.1, r_sdcp_um=0.5), None)
    nN = [0]

    def _count_direct(L, b, *a, **k):
        nN[0] += 1
        return spsolve(L.tocsc(), b), 0
    old_s = S3._solve_cg
    S3._solve_cg = _count_direct
    try:
        rN = _try(lambda: quiet(S3.solve_sigma_z, sidN, sig_e(), H, z_top_um=float(SVX_N[2]) * H, z_bot_um=0.0,
                                cjunc=plan(regN, SVX_RJ, sv_counterfactual={'threshold': 2.0})), None)
    finally:
        S3._solve_cg = old_s
    cN = ((rN or {}).get('cjunc') or {}).get('sv_counterfactual') or {}
    IN_full = ref_I(M_ + 1, E0 + E_sv, [(0, G_PL)], [(Bn(21), G_PL)])
    chk("RCA06-H ⑤ (지킴) SV 만 잇는 침대 — 끊으면 관통 성분 없음 (위상) → 풀이 1 번 (주 해만) · 'no_through_without_sv' · 비 inf · "
        'SV_DEPENDENT · G_cut 0 · 주 σ = 손 회로 (1e-12)',
        rN is not None and int(sidN[2, 1, 10]) == 0 and nN[0] == 1 and rel(I_of(rN, SVX_N), IN_full) < 1e-12
        and cN.get('status') == 'no_through_without_sv' and cN.get('sv_counterfactual_ratio') == math.inf
        and cN.get('flag') == 'SV_DEPENDENT' and cN.get('G_cut_code') == 0.0,
        f"풀이 {nN[0]} · {cN.get('status')} · 비 {cN.get('sv_counterfactual_ratio')} · 표지 {cN.get('flag')}")


#  PCP — 나란한 짧은 접촉 (L_c 1.78 ≤ L_par 2 → 간선 1) 의 접점 (`CJUNC_CP_RULE`): 최근접 쌍이 겹침 [4.0, 5.0] 전체에 비유일 → ε 띠 안 중점
#  사전식 최소 = 겹침 아래 끝 z 4.0 → A 접점이 (1,1,3) · (1,1,4) 중심에서 등거리 → 사전식 (1,1,3) · B = (2,1,4).  이진 정확 좌표 (간격 0.625 ·
#  점 간격 0.25) → 점 역순 · 공선 세분 (0.125) 에 포트 · 간선 원장 · σ 비트 같음 (옛 'argmin 첫 쌍' = 쌍 목록 순서 의존).
PCP_N = (5, 3, 10)
PCP = [[(1.5, 1.5, 0.5), (1.5, 1.5, 5.0)], [(2.125, 1.5, 4.0), (2.125, 1.5, 9.5)]]
#  PCP-F — B 위 끝을 셀 (1,1,9) 쪽으로 꺾어 (x 1.875) B 의 정준 방향을 위 → 아래로 뒤집은 꼴.  fid 를 바꾸면 옛 판은 쌍 방향 (fid) 이 바뀌어
#  'argmin 첫 쌍' 이 겹침의 다른 끝 (z 5.0) 으로 옮겨 포트가 달라졌다 — 새 판 (중점 사전식) = fid 무관.
PCP_BF = [(2.125, 1.5, 4.0), (2.125, 1.5, 9.5), (1.875, 1.5, 9.5)]


@case('PCP')
def t_pcp():
    rj = 1e3
    want = chain_I([G_PL] + [G_AX] * 3 + [1e4 / rj] + [G_AX] * 5 + [G_PL])
    b0 = _try(lambda: _solve_full(rows_exact(PCP), PCP_N), None)
    ok = b0 is not None
    pc = (_pcells(b0[1], 0, 'i'), _pcells(b0[1], 0, 'j')) if ok else None
    chk('PCP 나란한 짧은 접촉 — instance 1 · k 1 · 접점 z 4.0 (ε 띠 중점 사전식) · 포트 (1,1,3)–(2,1,4) · σ = 손 회로 (1e-12)',
        ok and len(b0[1]['instances']['fi']) == 1 and int(np.asarray(b0[1]['instances'].get('nsub', [1]))[0]) == 1
        and abs(float(b0[1]['instances']['Ci'][0][2]) - 4.0) == 0.0 and pc == ((1, 1, 3), (2, 1, 4))
        and rel(I_of(b0[2], PCP_N), want) < 1e-12,
        f"{None if not ok else (b0[1]['instances']['Ci'], pc, I_of(b0[2], PCP_N))} ↔ {want}")
    for nm, polys, step in (('점 역순', [v[::-1] for v in PCP], 0.25), ('공선 세분 0.125', PCP, 0.125),
                            ('점 역순 + 세분', [v[::-1] for v in PCP], 0.125)):
        o = _try(lambda polys=polys, step=step: _solve_full(rows_exact(polys, step=step), PCP_N), None)
        chk(f'PCP {nm} → 접점 · 포트 · 간선 원장 · σ 비트 같음',
            ok and o is not None and np.asarray(o[1]['instances']['Ci']).tobytes() == np.asarray(b0[1]['instances']['Ci']).tobytes()
            and (_pcells(o[1], 0, 'i'), _pcells(o[1], 0, 'j')) == pc and sys_bytes(o[2]) == sys_bytes(b0[2])
            and np.float64(o[2]['sigma_eff']).tobytes() == np.float64(b0[2]['sigma_eff']).tobytes(),
            f"{None if o is None else (o[1]['instances']['Ci'], _pcells(o[1], 0, 'i'))}")
    f1 = _try(lambda: _solve_full(rows_exact([PCP[0], PCP_BF], fids=[10, 20]), PCP_N), None)
    f2 = _try(lambda: _solve_full(rows_exact([PCP[0], PCP_BF], fids=[20, 10]), PCP_N), None)

    def _cp_cells(o):
        if o is None or len(o[1]['instances']['fi']) != 1:
            return None
        cs = sorted([_pcells(o[1], 0, 'i'), _pcells(o[1], 0, 'j')])
        return cs, sorted([tuple(map(float, o[1]['instances']['Ci'][0])), tuple(map(float, o[1]['instances']['Cj'][0]))])
    chk('PCP-F fid 재명명 (B 정준 방향 위 → 아래 · 옛 = fid 로 정한 i 가닥의 첫 쌍 → 겹침 다른 끝) → 접점 · 포트 · 간선 원장 · σ 비트 같음 '
        '(접점 z 4.0 · A 포트 (1,1,3))',
        f1 is not None and f2 is not None and _cp_cells(f1) == _cp_cells(f2) and (1, 1, 3) in _cp_cells(f1)[0]
        and sys_bytes(f1[2]) == sys_bytes(f2[2])
        and np.float64(f1[2]['sigma_eff']).tobytes() == np.float64(f2[2]['sigma_eff']).tobytes(),
        f'{_cp_cells(f1)} ↔ {_cp_cells(f2)}')


@case('CAX-SUB')
def t_cax_subedges():
    """증거 검증기 (`ca_ext_cjunc.cjunc_block_problem`) 의 분산 간선 수 (10-21 · RCA-05 v0 · 사전 공격 리뷰 — 증서 ↔ 결과 결합) — 합성
    매니페스트 = test_ca_ext_b6.cj_manifest (봉인 코호트 바탕 · 모듈 기록 함수) 를 고친 꼴.  정확한 불변량: 배율 최대 (len_mult_max) = 1 ⟺
    모든 instance k = 1 ⟺ n_subedges = n_instances (k = ceil(L_c/L_par) 문턱 `_n_sub` = 배율 법칙 `junction_len_mult` 와 같은 식 r > 1 + 1e-9 ·
    긴 접촉 표지 n_long 은 곱 꼴 (L_c > L_par·(1 + 1e-9)) 이라 1 ulp 경계에서 다를 수 있어 쓰지 않는다)."""
    import importlib
    RCm = importlib.import_module('run_contract')
    CWm = importlib.import_module('ca_ext_cjunc')
    B6 = importlib.import_module('test_ca_ext_b6')
    B6.RC, B6.CW = RCm, CWm
    m = B6.cj_manifest(n_inst=3)

    def var(extra=0, **upd):
        x = B6.deep(m)
        ev = x['ca_ext']['cjunc']['evidence']
        ev['counts'].update(upd)
        for k_, v_ in list(ev['counts'].items()):
            if v_ == '__drop__':
                ev['counts'].pop(k_)
        if extra:
            ev['solve']['n_junction_edges'] += extra
            ev['receipts']['electronic_main']['n_junction_edges'] += extra
        return x

    def ok(x):
        return RCm.ca_ext_record_ok(x)[0]
    good_k = dict(extra=2, n_subedges=5, n_edge=5, len_mult_max=2.5, n_long=1)
    chk('CAX-SUB 바탕 (k 1 · n_subedges 칸 없음 = instance 수) · k > 1 꼴 (instance 3 · 간선 5 · 배율 최대 2.5) = 받는다 (지킴)',
        ok(m) and ok(var(**good_k)), (RCm.ca_ext_record_ok(m), RCm.ca_ext_record_ok(var(**good_k))))
    #  옛 꼴 기록 (배율 최대 · n_subedges 칸 둘 다 없음 = 점 접합만 · test_rint_r_chain 합성 매니페스트 꼴) = 받는다 — 칸이 없으면 간선 = instance
    #  여야 한다 (k > 1 기록이 칸을 빼면 거부).  ★ 10-21 회귀 (test_rint_r_chain 32/89) 로 고침 — 첫 판은 칸 없음을 무조건 거부했다.
    chk('CAX-SUB 옛 꼴 (배율 최대 칸 없음 · 간선 = instance · n_long 1) = 받는다 (지킴 · 옛 합성 매니페스트)',
        ok(var(len_mult_max='__drop__', n_long=1)), RCm.ca_ext_record_ok(var(len_mult_max='__drop__', n_long=1)))
    bad_new = {
        '간선 5 > instance 3 인데 배율 최대 1.0 (긴 접촉 없음 = 모든 k 1)': dict(good_k, len_mult_max=1.0),
        '배율 최대 2.5 (긴 접촉 있음 = k ≥ 2) 인데 간선 = instance': dict(len_mult_max=2.5),
        '배율 최대 NaN': dict(len_mult_max=float('nan')),
        '배율 최대 0.5 (< 1)': dict(len_mult_max=0.5),
        '배율 최대 True (bool == 1.0)': dict(len_mult_max=True),
        "배율 최대 문자열 '1.0'": dict(len_mult_max='1.0'),
        '배율 최대 빠짐인데 간선 5 > instance 3 (k > 1 기록이 칸을 뺌)': dict(good_k, len_mult_max='__drop__'),
        '배율 최대 None (instance > 0)': dict(len_mult_max=None),
    }
    for nm, upd in bad_new.items():
        chk(f'CAX-SUB 거부 [{nm}]', not ok(var(**upd)), RCm.ca_ext_record_ok(var(**upd)))
    bad_guard = {
        'n_subedges 칸 없음인데 모드 합 5 (instance 3)': dict(extra=2, n_edge=5, len_mult_max=2.5, n_long=1),
        'n_subedges True': dict(good_k, n_subedges=True),
        'n_subedges 5.0 (실수)': dict(good_k, n_subedges=5.0),
        'n_subedges 2 < instance 3 (모드 합 2)': dict(n_subedges=2, n_edge=2),
    }
    for nm, upd in bad_guard.items():
        chk(f'CAX-SUB 거부 (지킴) [{nm}]', not ok(var(**upd)), RCm.ca_ext_record_ok(var(**upd)))


@case('PCP-EPS')
def t_pcp_eps():
    """PCP 를 비이진 원점으로 통째로 옮긴 침대 (10-21 변이 M16 생존 → 보탬 · 시험은 구현 뒤): 나란한 겹침의 최근접 쌍 거리가 반올림으로
    조금씩 달라진다 → 접점 = ε 띠 (거리² 1e-9 µm²) 안 중점 사전식 최소 = 겹침 아래 끝 (z 4.0 + o_z) · 포트 (1,1,3)–(2,1,4) · σ = 손 회로
    (1e-12).  옛 'argmin 첫 쌍' 은 반올림이 고른 쌍 (원점 이동에 접점이 움직인다)."""
    rj = 1e3
    want = chain_I([G_PL] + [G_AX] * 3 + [1e4 / rj] + [G_AX] * 5 + [G_PL])
    for o in ((0.6, 0.6, 0.6), (0.123, 0.456, 0.789)):     # 옮긴 꼭짓점 사이 길이가 점 간격의 정수배로 남는 원점 (densify_exact 조건)
        sh = [[tuple(np.asarray(p, np.float64) + np.asarray(o)) for p in v] for v in PCP]
        P = rows_exact(sh)
        sid = _try(lambda: bed(P, PCP_N, lo=o)[0], None)
        reg = _try(lambda: registry(sid, P, lo=o), None)
        r = _try(lambda: solve(sid, sig_e(), PCP_N, plan(reg, rj)), None) if reg is not None else None
        I = (reg or {}).get('instances') or {}
        ok_ = r is not None and len(I.get('fi', [])) == 1
        chk(f'PCP-EPS 원점 {o} — 접점 z = 4.0 + o_z (1e-12) · 포트 (1,1,3)–(2,1,4) · σ = 손 회로 (1e-12)',
            ok_ and abs(float(I['Ci'][0][2]) - (4.0 + o[2])) < 1e-12 and (_pcells(reg, 0, 'i'), _pcells(reg, 0, 'j')) == ((1, 1, 3), (2, 1, 4))
            and rel(I_of(r, PCP_N), want) < 1e-12,
            f"{None if not ok_ else (I['Ci'][0].tolist(), _pcells(reg, 0, 'i'), _pcells(reg, 0, 'j'), I_of(r, PCP_N))} ↔ {want}")


#  PCP-FAR — PCP 의 A 아래 끝에만 짧은 꼬리 ((1.5 → 1.75, ·, 0.5) · 같은 셀 (1,1,0) · B 와 멀다) 를 단 꼴: 끝점 사전식이 바뀌어 A 의 정준
#  방향이 위 → 아래로 뒤집힌다 → 겹침 [4.0, 5.0] 을 내려가며 지난다.  접점 = ε 띠 중점 사전식 최소 = z 4.0 (방향 무관) → 포트 · 계 · σ =
#  PCP 와 같다.  옛 'argmin 첫 쌍' (정준 경로 순서의 첫 최근접 쌍) 은 겹침 위 끝 z 5.0 → A 포트 (1,1,4) (10-21 변이 M16 생존 → 보탬 ·
#  시험은 구현 뒤).
PCP_AFAR = [(1.75, 1.5, 0.5), (1.5, 1.5, 0.5), (1.5, 1.5, 5.0)]


@case('PCP-FAR')
def t_pcp_far():
    rj = 1e3
    want = chain_I([G_PL] + [G_AX] * 3 + [1e4 / rj] + [G_AX] * 5 + [G_PL])
    b0 = _try(lambda: _solve_full(rows_exact(PCP), PCP_N), None)
    for nm, polys in (('A 아래 끝 꼬리', [PCP_AFAR, PCP[1]]), ('A 아래 끝 꼬리 + 점 역순', [PCP_AFAR[::-1], PCP[1][::-1]])):
        o = _try(lambda polys=polys: _solve_full(rows_exact(polys), PCP_N), None)
        I = (o[1]['instances'] if o is not None else {})
        flip = None
        if o is not None:
            A_ = o[1]['positions']
            m = A_['fid'] == 10
            flip = bool(A_['ijk'][m][0][2] > A_['ijk'][m][-1][2])          # A 의 정준 첫 위치가 위쪽 = 내려간다
        chk(f'PCP-FAR {nm} — 같은 sid · A 정준 방향 = 내려감 · 접점 z 4.0 · 포트 (1,1,3)–(2,1,4) · 계 바이트 · σ 비트 = PCP · σ = 손 회로 '
            '(1e-12)',
            b0 is not None and o is not None and o[0].tobytes() == b0[0].tobytes() and flip is True and len(I['fi']) == 1
            and float(I['Ci'][0][2]) == 4.0 and (_pcells(o[1], 0, 'i'), _pcells(o[1], 0, 'j')) == ((1, 1, 3), (2, 1, 4))
            and sys_bytes(o[2]) == sys_bytes(b0[2])
            and np.float64(o[2]['sigma_eff']).tobytes() == np.float64(b0[2]['sigma_eff']).tobytes()
            and rel(I_of(o[2], PCP_N), want) < 1e-12,
            f"{None if o is None else (flip, I['Ci'][0].tolist(), _pcells(o[1], 0, 'i'), _pcells(o[1], 0, 'j'), I_of(o[2], PCP_N))}")


@case('CP-ORD')
def t_cp_order():
    """instance 접점 (`CJUNC_CP_RULE`) 은 후보 쌍 나열 순서에 무관해야 한다 — 후보 쌍은 `cKDTree.query_pairs` 의 출력 (순서 = 구현 정의 · 트리
    모양) 이다.  그 출력을 뒤집거나 (시드 고정) 무작위로 섞어도 접점 · 포트 · 간선 원장 · 계 · σ 비트 같음 (PCP · PCP-FAR · LP 긴 접촉 ·
    CX 5 노드 꼴).  ★ 10-21 변이 M16 ('argmin 첫 쌍' = 나열 순서의 첫 최소 쌍) 이 고정 침대 전부를 통과해 (트리 순서가 우연히 사전식 최소
    쌍을 먼저 냈다) 보탬 · 시험은 구현 뒤."""
    import scipy.spatial as SPS
    real = SPS.cKDTree

    class _Wrap:
        def __init__(self, t, how):
            self._t, self._how = t, how

        def __getattr__(self, k):
            return getattr(self._t, k)

        def query_pairs(self, *a, **k):
            out = self._t.query_pairs(*a, **k)
            if not isinstance(out, np.ndarray) or len(out) < 2:
                return out
            if self._how == 'rev':
                return out[::-1].copy()
            return out[np.random.default_rng(7).permutation(len(out))].copy()

    @contextlib.contextmanager
    def order(how):
        SPS.cKDTree = (lambda *a, **k: _Wrap(real(*a, **k), how)) if how else real
        try:
            yield
        finally:
            SPS.cKDTree = real

    def rec(P, n):
        sid, _ = bed(P, n)
        reg = registry(sid, P)
        r = solve(sid, sig_e(), n, plan(reg, 1e3))
        I, S = reg['instances'], reg['subedges']
        return (np.asarray(I['Ci']).tobytes(), np.asarray(I['Cj']).tobytes(), np.asarray(S['X_i']).tobytes(),
                np.asarray(S['X_j']).tobytes(), tuple(_sub_cells(reg)), sys_bytes(r), np.float64(r['sigma_eff']).tobytes())
    beds = (('PCP', rows_exact(PCP), PCP_N), ('PCP-FAR', rows_exact([PCP_AFAR, PCP[1]]), PCP_N), ('LP 긴 접촉', rows(LP), LP_N),
            ('CX 5 노드 꼴', rows(CX), CX_N))
    for nm, P, n in beds:
        base = _try(lambda P=P, n=n: rec(P, n), None)
        for how in ('rev', 'perm'):
            with order(how):
                o = _try(lambda P=P, n=n: rec(P, n), None)
            chk(f'CP-ORD {nm} · 후보 쌍 {"뒤집음" if how == "rev" else "무작위 섞음 (시드 7)"} → 접점 · 등분점 · 간선 포트 셀 · 계 · σ 비트 같음',
                base is not None and o is not None and o == base,
                None if (base is None or o is None) else [k for k, (x, y) in enumerate(zip(o, base)) if x != y])


#  BR3 — 포트 규칙 ③ (같은 셀에 후보 가지 여럿 = 접점까지 그 가지 중심선 거리): B 가 머리핀으로 셀 기둥 (2,1,·) 을 두 번 지난다 —
#  다리 2 (x 2.8 · A 에서 1.3 = 안 닿음) 를 정준 순서로 먼저 · 다리 1 (x 2.3 · A 에서 0.8 = 닿음) 을 나중에.  A–B 접촉의 B 쪽 점 (X_j) 이
#  다리 1 위 셀 (2,1,2) · (2,1,3) 에 있으면 그 셀의 후보 = 두 다리 → ③ = X_j 를 지나는 다리 1.  ③ 을 빼면 (조각, 번호) 최소 = 안 닿는
#  다리 2 (10-21 변이 M22 생존 → 보탬 · 시험은 구현 뒤).  B 아래 끝 z 1.5 (판에 안 닿음) · A 아래 판 · B 위 판.
BR3_N = (7, 3, 8)
BR3 = [[(1.5, 1.5, 0.5), (1.5, 1.5, 6.5)],
       [(2.8, 1.5, 1.5), (2.8, 1.5, 4.0), (2.3, 1.5, 4.0), (2.3, 1.5, 2.0), (2.3, 2.5, 2.0), (5.5, 2.5, 2.0), (5.5, 2.5, 7.5)]]


@case('BR3')
def t_branch_tie():
    P = rows(BR3)
    sid, _ = bed(P, BR3_N)
    reg = _try(lambda: registry(sid, P), None)
    if reg is None:
        chk('BR3 원장', False, 'registry 실패')
        return
    I, S, pos, segs = reg['instances'], reg['subedges'], reg['positions'], reg['segments']
    dis = [q for q in range(len(I['fi'])) if not I['self'][q]]
    rows_ = [e for e in range(len(S['inst'])) if int(S['inst'][e]) in dis and bool(S['realized'][e])]

    def d_branch(p, X):
        sg = np.arange(pos['s0'][p], pos['s1'][p] + 1)
        d2, _, _ = CJ.pt_seg_d2(np.repeat(np.asarray(X, np.float64)[None], len(sg), 0), segs['P0'][sg], segs['P1'][sg])
        return float(np.sqrt(d2.min()))
    two = []
    for e in rows_:
        p = int(S['port_j'][e])
        c = tuple(int(v) for v in pos['ijk'][p])
        same = np.flatnonzero(np.all(pos['ijk'] == pos['ijk'][p], axis=1) & (pos['fid'] == pos['fid'][p]))
        if len(same) > 1:
            two.append((e, c, len(same), d_branch(p, S['X_j'][e]), min(d_branch(int(x), S['X_j'][e]) for x in same)))
    chk('BR3 A–B 접촉 (서로 다른 섬유) 의 B 쪽 포트 중 같은 셀 두 가지 후보가 있는 간선 ≥ 1 (픽스처가 ③ 을 실제로 건드린다)',
        len(two) >= 1, f'{two} · 간선 {len(rows_)}')
    chk('BR3 그 간선마다 B 포트 가지 = 접점 (X_j) 을 지나는 가지 (중심선 거리 ≤ 1e-9 · 같은 셀 다른 가지의 최소와 같다)',
        len(two) >= 1 and all(dp <= 1e-9 and dp == dm for _, _, _, dp, dm in two), f'{two}')


#  SIDE — 분산판 v0 의 정의 쪽 = 닿음 길이가 긴 가닥 (손 해석): A (i · x 1.5 · z 3–6) 가 B (j · x 2.1 · z 0.5–7.7) 안에 든다 (거리 0.6 ·
#  닿음 T = r_i + r_j = 1.0 → 끝 덮개 c = √(1 − 0.36) = 0.8).  A 쪽 닿음 = A 전체 3.0 · B 쪽 = [2.2, 6.8] = 4.6 → L_c 4.6 · k 3 · 정의 쪽 = B
#  (side 1) · 등분점 X_j z = 2.2 + (j + ½)·4.6/3 = 2.9667 · 4.5 · 6.0333 · 맞은편 A 최근접 = (1.5, 1.5, clamp(z, 3, 6)) · B 포트 셀 (2,1,2) ·
#  (2,1,4) · (2,1,6).  정의 쪽을 늘 i 로 두면 A 위 3.5 · 4.5 · 5.5 (10-21 변이 M23 생존 → 보탬 · 시험은 구현 뒤).
SIDE_N = (5, 3, 9)
SIDE = [[(1.5, 1.5, 3.0), (1.5, 1.5, 6.0)], [(2.1, 1.5, 0.5), (2.1, 1.5, 7.7)]]


@case('SIDE')
def t_side():
    P = rows(SIDE)
    sid, _ = bed(P, SIDE_N)
    reg = _try(lambda: registry(sid, P), None)
    I = (reg or {}).get('instances') or {}
    S = (reg or {}).get('subedges') or {}
    ok_ = reg is not None and len(I.get('fi', [])) == 1 and not bool(I['self'][0])
    zj = [2.2 + (j + 0.5) * 4.6 / 3.0 for j in range(3)]
    chk('SIDE 손 해석 — L_c 4.6 · k 3 · 정의 쪽 = B (side 1) · 등분점 X_j = (2.1, 1.5, 2.9667 · 4.5 · 6.0333) · 맞은편 X_i = (1.5, 1.5, 3 · 4.5 · 6) '
        '(1e-9) · B 포트 셀 (2,1,2) · (2,1,4) · (2,1,6)',
        ok_ and abs(float(I['Lc'][0]) - 4.6) < 1e-9 and int(I['nsub'][0]) == 3 and len(S['inst']) == 3
        and all(int(x) == 1 for x in S['side'])
        and np.allclose(np.asarray(S['X_j']), [[2.1, 1.5, z] for z in zj], rtol=0, atol=1e-9)
        and np.allclose(np.asarray(S['X_i']), [[1.5, 1.5, min(max(z, 3.0), 6.0)] for z in zj], rtol=0, atol=1e-9)
        and [c[1] for c in _sub_cells(reg)] == [(2, 1, 2), (2, 1, 4), (2, 1, 6)],
        f"{None if not ok_ else (float(I['Lc'][0]), int(I['nsub'][0]), list(S['side']), np.asarray(S['X_j']).round(6).tolist(), _sub_cells(reg))}")


#  NEAR — 분산판 등분점의 맞은편 최근접점이 둘 (ε 띠) 인 꼴 (손 해석): A (i) = x 축 (y 1.5 · z 1.5 · x 0.5–8.5) · B (j) = 얕은 Λ (밑 (2.5, 2.1) ·
#  꼭짓점 (4.5, 2.3) · 밑 (6.5, 2.1) · z 1.5) 뒤 오른 밑에서 위 (z 4.5) 로 · −x 로 (1.5, 2.1, 4.5) 끝 → B 정준 시작 = (1.5, 2.1, 4.5) (끝점 사전식)
#  → 오른 팔을 먼저 지난다.  A 닿음 [1.7, 7.3] = 5.6 > B 4.82 → L_c 5.6 · k 3 · 정의 쪽 A · 가운데 등분점 X_i = (4.5, 1.5, 1.5) → B 의 두 팔
#  수선발 (대칭 · 꼭짓점 0.8 보다 가깝다 · t = (a² − d·h)/(a² + h²) = 0.960396 · a 2 · h 0.2 · d 0.6) = (4.5 ∓ 0.079208, 2.292079) 등거리 →
#  ε 띠 안 사전식 최소 = 왼 팔 (x 4.420792).  띠를 빼고 첫 점 = 정준 순서 첫 (오른 팔 · 10-21 변이 M25 생존 → 보탬 · 시험은 구현 뒤).
NEAR_N = (10, 4, 6)
NEAR = [[(0.5, 1.5, 1.5), (8.5, 1.5, 1.5)],
        [(1.5, 2.1, 4.5), (6.5, 2.1, 4.5), (6.5, 2.1, 1.5), (4.5, 2.3, 1.5), (2.5, 2.1, 1.5)]]


@case('NEAR')
def t_near_tie():
    P = rows(NEAR)
    sid, _ = bed(P, NEAR_N)
    reg = _try(lambda: registry(sid, P), None)
    I = (reg or {}).get('instances') or {}
    S = (reg or {}).get('subedges') or {}
    dis = [q for q in range(len(I.get('fi', []))) if not I['self'][q]]
    t = (4.0 - 0.6 * 0.2) / (4.0 + 0.2 * 0.2)
    foot_l = (2.5 + 2.0 * t, 2.1 + 0.2 * t, 1.5)
    ok_ = reg is not None and len(dis) == 1 and int(I['nsub'][dis[0]]) == 3
    rows_ = [e for e in range(len(S.get('inst', []))) if ok_ and int(S['inst'][e]) == dis[0]]
    mid = [e for e in rows_ if int(S['j'][e]) == 1]
    chk('NEAR 손 해석 — A–B instance 1 · L_c 5.6 · k 3 · 정의 쪽 A (side 0) · 가운데 등분점 X_i = (4.5, 1.5, 1.5) · 맞은편 X_j = 왼 팔 수선발 '
        '(4.420792, 2.292079, 1.5) (1e-9 · 두 팔 등거리 ε 띠 → 사전식 최소)',
        ok_ and abs(float(I['Lc'][dis[0]]) - 5.6) < 1e-9 and len(mid) == 1 and int(S['side'][mid[0]]) == 0
        and np.allclose(np.asarray(S['X_i'][mid[0]]), [4.5, 1.5, 1.5], rtol=0, atol=1e-9)
        and np.allclose(np.asarray(S['X_j'][mid[0]]), foot_l, rtol=0, atol=1e-9),
        f"{None if not ok_ else (float(I['Lc'][dis[0]]), [np.asarray(S['X_j'][e]).round(6).tolist() for e in rows_])} ↔ {foot_l}")


@case('JI-KNOB')
def t_ji_knob():
    """원장 기록 둘 (10-21 · 시험은 구현 뒤 · 변이 표에서 보탬):
    ① instance 접합 전류 = 그 instance 분산 간선 전류의 **합** — CX (A → B 가 접합으로만 · 간선 5) 에서 instance 하나의 전류 = 단자 전류 (1e-10)
       · 간선별 전류 합과 같다 (분산판 v0 의 record · 옛 = instance 하나 = 간선 하나).
    ② 반사실 노브는 계획 지문 (`plan_rows_fp`) 에 든다 — 계획을 만든 뒤 문턱만 바꾸면 (2.0 → 1.0) 솔브 입구 거부 · 노브를 빼도 거부."""
    P = rows(CX)
    sid, _ = bed(P, CX_N)
    reg = _try(lambda: registry(sid, P), None)
    r = _try(lambda: solve(sid, sig_e(), CX_N, plan(reg, 200.0)), None)
    ok_ = r is not None and len(reg['instances']['fi']) == 1
    jI = np.asarray(r['_cjunc']['junction_current_code']) if ok_ else None
    sub_I = None
    if ok_:
        s = r['_cjunc']['sys']
        js = np.flatnonzero(np.asarray(s['CAT']) == CJ._CAT['vv_junction'])
        phi = np.asarray(r['_cjunc']['phi_dof'])
        sub_I = float(np.sum(np.asarray(s['G'])[js] * (phi[np.asarray(s['u'])[js]] - phi[np.asarray(s['v'])[js]])))
    I = I_of(r, CX_N) if ok_ else math.nan
    chk('JI-KNOB ① CX — instance 접합 전류 = 분산 간선 5 전류 합 = 단자 전류 (1e-10)',
        ok_ and len(jI) == 1 and len(np.flatnonzero(np.asarray(r['_cjunc']['sys']['CAT']) == CJ._CAT['vv_junction'])) == 5
        and rel(abs(float(jI[0])), I) < 1e-10 and rel(float(jI[0]), sub_I) < 1e-12, f'{jI} · 간선 합 {sub_I} · I {I}')
    P2 = cat_rows(rows(SVX), rows(SVX_SDCP, phase=5, kind=0, fid0=700))
    sid2, _ = bed(P2, SVX_N)
    reg2 = _try(lambda: registry(sid2, P2, tol_sj_um=0.1, r_sdcp_um=0.5), None)
    pl = _try(lambda: plan(reg2, SVX_RJ, sv_counterfactual={'threshold': 2.0}), None)
    good = _try(lambda: solve(sid2, sig_e(), SVX_N, pl), None) if pl is not None else None
    pl_t = dict(pl or {}, sv_counterfactual={'threshold': 1.0})
    pl_d = dict(pl or {}, sv_counterfactual=None)
    chk('JI-KNOB ② 노브 = 계획 지문 — 정상 계획은 풀린다 · 만든 뒤 문턱만 바꿈 (2.0 → 1.0) = 입구 거부 · 노브 뺌 = 입구 거부',
        good is not None and good.get('cjunc', {}).get('sv_counterfactual', {}).get('threshold') == 2.0
        and raises(lambda: solve(sid2, sig_e(), SVX_N, pl_t)) and raises(lambda: solve(sid2, sig_e(), SVX_N, pl_d)),
        f"{None if good is None else good.get('cjunc', {}).get('sv_counterfactual', {}).get('threshold')}")


@case('OFF-IND')
def t_off_independent():
    """보장 — 접합 끔 (cjunc=None) 솔브는 carbon_junction 을 부르지도 읽지도 않는다 (구조 증거 · C0 의 옛 기준 비트 대조와 별개):
    sys.modules 의 carbon_junction 을 속성 접근 즉시 실패하는 가짜로 바꿔도 끔 솔브가 돌고 결과 (σ · φ · n_dof · cg_info · resid) 비트 같음."""
    import types
    P = rows(LP)
    sid, _ = bed(P, LP_N)
    r0 = solve_legacy(sid, sig_e(), LP_N, return_field=True)

    class _Boom(types.ModuleType):
        def __getattr__(self, name):
            raise AssertionError(f'접합 끔 경로가 carbon_junction.{name} 을 읽었다')
    old = sys.modules.get('carbon_junction')
    sys.modules['carbon_junction'] = _Boom('carbon_junction')
    try:
        r1 = _try(lambda: solve_legacy(sid, sig_e(), LP_N, return_field=True), None)
    finally:
        if old is None:
            sys.modules.pop('carbon_junction', None)
        else:
            sys.modules['carbon_junction'] = old
    chk('OFF-IND 접합 끔 솔브 = carbon_junction 무관 (가짜 모듈로도 돈다) · σ · φ · n_dof · cg_info · resid 비트 같음',
        r1 is not None and np.float64(r1['sigma_eff']).tobytes() == np.float64(r0['sigma_eff']).tobytes()
        and r1['phi'].tobytes() == r0['phi'].tobytes() and r1['n_dof'] == r0['n_dof'] and r1.get('cg_info') == r0.get('cg_info')
        and np.float64(r1['resid']).tobytes() == np.float64(r0['resid']).tobytes() and 'cjunc' not in r1)


@case('MUT-RCA')
def t_mut_rca():
    """10-21 RCA 보장의 판별력 (상주 변이) — 모듈 함수를 바꿔 끼운 변이가 위 시험 (손 회로 · 비트 대조) 에 **옳은 이유로** 걸려야 한다:
    변이 전 통과 · 변이 뒤 같은 검사 실패.  (한 줄 소스 변이 표는 보고 · 이 묶음은 그중 함수 단위로 상주시킬 수 있는 것)."""
    rj = 1e3

    @contextlib.contextmanager
    def patched(obj, name, fn):
        if not hasattr(obj, name):                         # 훅이 없는 판 (고치기 전) — 변이를 끼울 수 없다 = 그 검사 실패로 센다
            raise AttributeError(f'변이 훅 {name} 없음')
        old = getattr(obj, name)
        setattr(obj, name, fn)
        try:
            yield
        finally:
            setattr(obj, name, old)

    real_pick = getattr(CJ, '_port_pick', None)

    def pick_lexmax(C, cand, pos, segs, lo, vox, r_port=None):      # 변이 — 동률을 사전식 **최대** 셀로
        cand = np.asarray(cand, np.int64)
        if len(cand) == 0:
            return -1, False, np.inf
        cc = lo + (pos['ijk'][cand].astype(np.float64) + 0.5) * vox
        d2 = np.sum((cc - np.asarray(C)) ** 2, axis=1)
        if r_port is not None:
            ok = np.sqrt(d2) <= r_port
            if not ok.any():
                return -1, False, np.inf
            cand, d2 = cand[ok], d2[ok]
        bnd = cand[d2 <= float(d2.min()) + CJ.CJUNC_EPS_D2_UM2]
        ijk = pos['ijk'][bnd]
        return int(bnd[np.lexsort((-ijk[:, 2], -ijk[:, 1], -ijk[:, 0]))[0]]), bool(len(bnd) > 1), float(np.sqrt(d2.min()))

    def pick_kmin(C, cand, pos, segs, lo, vox, r_port=None):        # 변이 — 동률을 정준 경로 번호 작은 쪽으로 (옛 규칙)
        p, t, d = real_pick(C, cand, pos, segs, lo, vox, r_port)
        if p < 0 or not t:
            return p, t, d
        cand = np.asarray(cand, np.int64)
        cc = lo + (pos['ijk'][cand].astype(np.float64) + 0.5) * vox
        d2 = np.sum((cc - np.asarray(C)) ** 2, axis=1)
        bnd = cand[d2 <= float(d2.min()) + CJ.CJUNC_EPS_D2_UM2]
        return int(bnd[np.argmin(pos['k'][bnd])]), t, d

    def t11_far_ok():
        b0 = _try(lambda: _solve_full(rows_exact([T4_A, T4_B]), T4_N), None)
        bf = _try(lambda: _solve_full(rows_exact([T4_A_FAR, T4_B]), T4_N), None)
        want = chain_I([G_PL] + [G_AX] * 2 + [1e4 / rj] + [G_AX] * 6 + [G_PL])
        return (b0 is not None and bf is not None and _pcells(b0[1], 0, 'i') == (1, 1, 2) and _pcells(bf[1], 0, 'i') == (1, 1, 2)
                and rel(I_of(b0[2], T4_N), want) < 1e-12 and sys_bytes(b0[2]) == sys_bytes(bf[2]))

    def fid_ok():
        a_ = _try(lambda: _solve_full(rows(LX, fids=[10, 20]), LX_N), None)
        b_ = _try(lambda: _solve_full(rows(LX, fids=[20, 10]), LX_N), None)
        return a_ is not None and b_ is not None and sys_bytes(a_[2]) == sys_bytes(b_[2])

    def cx_ok():
        P = rows(CX)
        sid, _ = bed(P, CX_N)
        reg = _try(lambda: registry(sid, P), None)
        sc = _sub_cells(reg) if reg is not None else None
        I = _try(lambda: I_of(solve(sid, sig_e(), CX_N, plan(reg, 200.0)), CX_N))
        return sc is not None and sorted(sc) == [((1, 1, z), (2, 1, z)) for z in (1, 3, 5, 7, 9)] and rel(I, _cx_ref(200.0)) < 1e-12

    def sv_ok():
        P = cat_rows(rows(SVX), rows(SVX_SDCP, phase=5, kind=0, fid0=700))
        sid, _ = bed(P, SVX_N)
        reg = _try(lambda: registry(sid, P, tol_sj_um=0.1, r_sdcp_um=0.5), None)
        r = _try(lambda: solve(sid, sig_e(), SVX_N, plan(reg, SVX_RJ, sv_counterfactual={'threshold': None})), None)
        cf = ((r or {}).get('cjunc') or {}).get('sv_counterfactual') or {}
        I_full, _, _ = _svx_ref(SVX_RJ)
        I_cut, _, _ = _svx_ref(SVX_RJ, with_sv=False)
        return rel(float(cf.get('sv_counterfactual_ratio') or math.nan), I_full / I_cut) < 1e-10

    def rc_ok():
        seq = seq_cells_v(RC_LOOP, RC_H, RC_STEP)
        P, sid = _rc_bed()
        rh = _try(lambda: _rc_reg(sid, P, 5.0), None)
        Ih = _try(lambda: I_of(solve(sid, sig_e(), RC_N, plan(rh, 1e3), vox=RC_H), RC_N, vox=RC_H))
        return rel(Ih, chain_ref(len(seq), g_ax=RC_GAX, g_pl=RC_GPL)) < 1e-12

    base_cls = CJ.CjuncAssembler

    class MergeRevisits(base_cls):                          # 변이 — 옛 재방문 합침 (같은 셀 두 가지 → 한 노드)
        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            for p_, q_ in np.asarray(self.reg.get('self_revisit_pairs', np.zeros((0, 2))), np.int64).reshape(-1, 2):
                self.pos_dof[q_] = self.pos_dof[p_]

    real_cf = getattr(base_cls, 'sv_counterfactual', None)

    def cf_nodrop(self, solve_, I_full, request, certify=None, backend=None, **extra):   # 변이 — 반사실이 SV 면을 끊지 않는다 (★ 10-21
        orig = self._assemble                                       #  PRE-impl-09 — 생산 호출 서명 그대로 (certify= · ★ 10-22 backend= ·
        self._assemble = lambda *a, **k: orig(*a, **dict(k, counterfactual=False))   # ★ 10-23 main_cert= · certify_zero= — 생산이 넘길 때만
        try:                                                        #  넘긴다) · 옛 변이는 TypeError 로만 '잡혔다')
            kw = {'certify': certify} if backend is None else {'certify': certify, 'backend': backend}
            kw.update(extra)
            return real_cf(self, solve_, I_full, request, **kw)
        finally:
            del self._assemble

    @contextlib.contextmanager
    def assembler(cls):
        old = CJ.CjuncAssembler
        CJ.CjuncAssembler = cls
        try:
            yield
        finally:
            CJ.CjuncAssembler = old

    cases = (
        ('포트 동률 = 사전식 최대 셀 → T1-11 · 먼 끝 뒤집힘 검사 실패', patched(CJ, '_port_pick', pick_lexmax), t11_far_ok),
        ('포트 동률 = 정준 경로 번호 (옛 규칙) → 먼 끝만 바꾼 침대에서 포트가 뒤집힌다', patched(CJ, '_port_pick', pick_kmin), t11_far_ok),
        ('경로 순서 = fid 순 (기하 정준 끔) → fid 재명명 침대 간선 원장이 달라진다',
         patched(CJ, '_canonical_paths', lambda paths, P, rej, label: sorted(paths, key=lambda t: t[0])), fid_ok),
        ('분산 끔 (k = 1 · 한 포트 집중) → CX 분산 간선 · σ 손 회로 실패', patched(CJ, '_n_sub', lambda Lc, L_par: 1), cx_ok),
        ('옛 재방문 합침 → RCA-03 고리 사슬 (5 Ω 꼴) 실패 (단락)', assembler(MergeRevisits), rc_ok),
        ('반사실이 SV 면을 안 끊음 → 비 1 · 손 회로 비 실패', patched(base_cls, 'sv_counterfactual', cf_nodrop), sv_ok),
    )
    for nm, ctx, check in cases:
        #  ★ 10-21 (PRE-impl-09) — 변이 안에서 난 예외 (`_try` 가 삼킨 것 포함) = 하네스 실패 (잡힘 아님 · T18 '기준선 통과 단언만' 과 같게) ·
        #    기준선 검사도 예외 없이 통과해야 한다
        _TRY_EXC[0] = 0
        b = bool(check())
        e0 = _TRY_EXC[0]
        c, why = None, ''
        try:
            with ctx:
                _TRY_EXC[0] = 0
                c = not bool(check())
                if _TRY_EXC[0]:
                    c, why = None, f'변이 안 예외 {_TRY_EXC[0]} 건 = 하네스 실패 (옳은 이유 아님)'
        except Exception as e:                              # noqa: BLE001 — 훅 없음 (고치기 전 판) · 변이 예외 = 하네스 실패
            c, why = None, f'{type(e).__name__}: {e}'
        if why:
            print(f'    MUT-RCA {nm}: {why}')
        chk(f'MUT-RCA {nm} (변이 전 통과 · 변이 실패 · 예외 없음)', b and e0 == 0 and c is True, f'base {b} (예외 {e0}) caught {c} {why}')


@case('CEN')
def t_census_q11():
    P, sid = _rc_bed()
    #  ★ 10-21 (Q-B) — s_min 0.6 (머리핀 접합 하나 · L_c < L_par · 90° 모서리는 바닥 (s > (π/2)·d) 이 거른다) · 재방문 s = 그 쌍 (같은
    #    조각 · 같은 셀 두 가지) 의 경로 호 간격 (쌍마다 · 옛 = 그 쌍이 든 자기 후보마다 하나)
    r = _try(lambda: _rc_reg(sid, P, 0.6), None)
    c = (r or {}).get('census') or {}
    rs = c.get('revisit_s_um') or {}
    chk('CEN 같은 셀 비연속 재방문 — 쌍 4 · 셀 4 · 섬유 1 · s 분포 (재방문 쌍마다 4 · 유한 · 양수)',
        c.get('n_revisit_pairs') == 4 and c.get('n_revisit_cells') == 4 and c.get('n_revisit_fibres') == 1
        and rs.get('n') == 4 and math.isfinite(float(rs.get('min', math.nan))) and float(rs.get('min', 0.0)) > 0.0,
        f"{ {k: c.get(k) for k in ('n_revisit_pairs', 'n_revisit_cells', 'n_revisit_fibres', 'revisit_s_um')} }")
    #  KR (재방문 1 + 비연속 면 1 · 서로 다른 후보) — 재방문 census 는 면 항목을 세지 않는다 (변이 '면까지 셈' 을 가른다)
    Pk = rows(KR)
    sidk, _ = bed(Pk, KR_N)
    rk = _try(lambda: registry(sidk, Pk, s_min_um=10.0), None)
    ck = (rk or {}).get('census') or {}
    chk('CEN KR — 재방문 쌍 1 · 셀 1 ((1,1,3)) · 섬유 1 · 재방문 s 1 개 (면 항목은 세지 않는다 · 자기 후보 ≥ 1)',
        ck.get('n_revisit_pairs') == 1 and ck.get('n_revisit_cells') == 1 and ck.get('n_revisit_fibres') == 1
        and (ck.get('revisit_s_um') or {}).get('n') == 1 and (ck.get('n_self_candidates') or 0) >= 1,
        f"{ {k: ck.get(k) for k in ('n_revisit_pairs', 'n_revisit_cells', 'n_revisit_fibres', 'revisit_s_um', 'n_self_candidates')} }")
    #  ★ 10-21 (사전 리뷰 PRE-impl-01 '경로로만 = 실제로 이어진 경로가 있을 때만' · 변이 시험 다지기 M27) — 같은 KR 에 SDCP 점이 두 가지
    #    사이 위치 (2,1,4) 를 덮으면 재방문 쌍은 경로로 안 이어진다 → 경로 끊김 1 · 경로로만 0 (접합 없음 · s_min 10)
    Pkb = cat_rows(rows(KR), rows([[(2.5, 1.5, 4.5)]], phase=5, kind=0, fid0=700))
    sidkb, _ = bed(Pkb, KR_N)
    rkb = _try(lambda: registry(sidkb, Pkb, s_min_um=10.0), None)
    ckb = (rkb or {}).get('census') or {}
    chk('CEN KR + SDCP 가 두 가지 사이 위치 (2,1,4) 를 덮음 — 재방문 쌍 1 · 경로 끊김 1 · 경로로만 0 (덮인 위치 = 경로 아님)',
        int(sidkb[2, 1, 4]) == 5 and ckb.get('n_revisit_pairs') == 1 and ckb.get('n_self_revisits_path_broken') == 1
        and ckb.get('n_self_revisits_path_only') == 0,
        f"{int(sidkb[2, 1, 4])} { {k: ckb.get(k) for k in ('n_revisit_pairs', 'n_self_revisits_path_broken', 'n_self_revisits_path_only')} }")
    t11 = _try(lambda: _solve_full(rows_exact([T4_A, T4_B]), T4_N), None)
    ct = (t11[1]['census'] if t11 is not None else {})
    chk('CEN 포트 동률 수 (간선 단위) — 고리 (동률 없음) = 0 · T1-11 꼴 (A 접점이 두 셀 중심에서 등거리 · ε 띠) = 1',
        c.get('n_port_ties') == 0 and ct.get('n_port_ties') == 1, f"{c.get('n_port_ties')} {ct.get('n_port_ties')}")
    Plp = rows(LP)
    pt = _ptfe_rows([[(1.8, 0.5, 2.7), (1.8, 2.5, 2.7)]])
    allr = cat_rows(Plp, pt)
    sidp, _ = bed(allr, LP_N, stamp=allr[1] != 4)
    rp = _try(lambda: registry(sidp, allr, tol_P_um=0.25, r_ptfe_um=0.25), None)
    cp = (rp or {}).get('census') or {}
    chk('CEN 긴 접촉 · 간선별 PTFE 덮임 — 분산 간선 3 (긴 접촉 간선 3) · 덮인 간선 1 · 부분 덮임 instance 1 · σ 칸 없음',
        cp.get('n_subedges') == 3 and cp.get('n_subedges_long') == 3 and cp.get('n_subedges_ptfe_cov') == 1
        and cp.get('n_instances_ptfe_partial') == 1 and cp.get('n_long_distinct') == 1
        and not [k for k in cp if any(s in k.lower() for s in ('sigma', 'current', 'dissip', 'conduct', 'resist'))],
        f"{ {k: cp.get(k) for k in ('n_subedges', 'n_subedges_long', 'n_subedges_ptfe_cov', 'n_instances_ptfe_partial', 'n_long_distinct')} }")


# ═════════════════════════ RCA2 — 사전 리뷰 (구현 · 10-21) PRE-impl-01–06 · 09 · 1저자 Q-A–Q-D 권고대로 ═════════════════════════
#  반례 = 사전 리뷰 (impl) 탐침 (probe_gap_revisit · _prod · probe_closed_loop · probe_self_vs_distinct · probe_ptfe_monotone ·
#  probe_sdcp_relocate · probe_sv_cf · probe_k_boundary_prod · probe_mut_cf) 을 우리 시험으로 — 기대 = 손 회로 · 독립 셀 열.

def rows_pieces(pieces, fid=10, phase=2, kind=1):
    """한 fid 의 점열 조각들 (점 배열 그대로 · 순서대로 붙임) → (P, PH, F, K) — 끊긴 섬유 (조각 사이 틈 > gap_tol × 중앙 간격) 를 만든다."""
    P = np.vstack([np.asarray(p, np.float64).reshape(-1, 3) for p in pieces])
    n = len(P)
    return P, np.full(n, phase, np.int64), np.full(n, fid, np.int64), np.full(n, kind, np.int64)


def _cells_of_pts(pts, vox=H):
    """점열 → 셀 열 (연속 중복 제거) — 독립 도구 (생산 원시 함수 `segment_cells`)."""
    from fibre_segment_raster import segment_cells
    pts = np.asarray(pts, np.float64)
    cs = np.vstack([segment_cells(pts[i], pts[i + 1], vox) for i in range(len(pts) - 1)])
    keep = np.ones(len(cs), bool)
    keep[1:] = np.any(cs[1:] != cs[:-1], axis=1)
    return [tuple(int(v) for v in c) for c in cs[keep]]


def _graph_ref(cells_seq, n, extra=(), drop=(), g_ax=G_AX, g_pl=G_PL):
    """셀 열 손 회로 — 같은 셀 = 한 노드 (고리 이음매) · 연속 이웃 = 축 간선 g_ax · drop = 뺄 축 간선 (셀 쌍) · extra = (셀, 셀, g) ·
    판 = z 0 셀 (아래) · z n−1 셀 (위) 전부 g_pl (셀 중심이 판에서 h/2) → 아래 판 전류."""
    uniq = sorted(set(cells_seq))
    ix = {c: i for i, c in enumerate(uniq)}
    E = set()
    for a_, b_ in zip(cells_seq[:-1], cells_seq[1:]):
        if a_ != b_:
            E.add(tuple(sorted((ix[a_], ix[b_]))))
    for a_, b_ in drop:
        E.discard(tuple(sorted((ix[a_], ix[b_]))))
    edges = [(a_, b_, g_ax) for a_, b_ in sorted(E)] + [(ix[a_], ix[b_], g) for a_, b_, g in extra]
    bot = [(ix[c], g_pl) for c in uniq if c[2] == 0]
    top = [(ix[c], g_pl) for c in uniq if c[2] == n[2] - 1]
    return ref_I(len(uniq), edges, bot, top)


def _inst_rec(reg, q):
    """instance q 의 기록 — L_c · 배율 · k · 분산 간선 포트 셀 (정렬) · d0 (서로 다른 섬유 ↔ 같은 fid 대조 · fid 무관 보장)."""
    I = reg['instances']
    S = reg.get('subedges') or {}
    pos = reg['positions']
    cells = []
    for e in range(len(S.get('inst', []))):
        if int(S['inst'][e]) != q:
            continue
        a_, b_ = int(S['port_i'][e]), int(S['port_j'][e])
        cells.append((None if a_ < 0 else tuple(int(v) for v in pos['ijk'][a_]),
                      None if b_ < 0 else tuple(int(v) for v in pos['ijk'][b_])))
    return {'Lc': float(I['Lc'][q]), 'mult': float(I['mult'][q]), 'nsub': int(np.asarray(I.get('nsub', [-1] * (q + 1)))[q]),
            'cells': sorted(cells, key=str), 'd0': float(I['d0'][q])}


def _rec_same(a, b):
    return (a is not None and b is not None and abs(a['Lc'] - b['Lc']) <= 1e-12 * max(1.0, abs(b['Lc']))
            and abs(a['mult'] - b['mult']) <= 1e-12 * b['mult'] and a['nsub'] == b['nsub'] and a['cells'] == b['cells']
            and abs(a['d0'] - b['d0']) <= 1e-15)


GAP_N = (3, 3, 8)


@case('GAP')
def t_gap():
    """★ PRE-impl-01 (P1) · 1저자 Q-A — 같은 섬유의 끊긴 두 조각 (`fibre_pieces` 끊기 = 섬유 경로로 안 이어짐) = 서로 다른 섬유와 같은 규칙
    (중심선 거리 ≤ D → R_j 접합 · instance = 조각 쌍 · s 규칙 없음).  옛 판 (기반 a76f59d0d): 두 끝이 같은 셀 = 같은 fid 재방문 '경로로만'
    (경로가 없다 = 거짓 기록) → σ 0 (no_through_component) · 면 인접 = 옛 융합 (12.5 = 끊김 없는 섬유처럼).  기대 = 손 회로 (조각 사슬 +
    R_j 간선 하나) · s_min 무관 · census 칸 정정 · 생산 단위 (h 0.15 · r_f 0.075 · tol_ff 0.03 · 점 간격 0.05 · 틈 0.12 · 옛 판 = 0 ↔ 872.66)."""
    rj = 1e3
    for nm, ze, zs, ca, cb in (('같은 셀 (끝 z 3.15 · 3.85 · 셀 (1,1,3))', 3.15, 3.85, 3, 3),
                               ('면 인접 (끝 z 2.85 · 3.5 · 셀 (1,1,2)|(1,1,3))', 2.85, 3.5, 2, 3)):
        P = rows_pieces([densify([(1.5, 1.5, 0.5), (1.5, 1.5, ze)]), densify([(1.5, 1.5, zs), (1.5, 1.5, 7.5)])])
        sid, _ = bed(P, GAP_N)
        want = chain_I([G_PL] + [G_AX] * ca + [1e4 / rj] + [G_AX] * (7 - cb) + [G_PL])
        I_leg = I_of(solve_legacy(sid, sig_e(), GAP_N), GAP_N)
        okreg = oks = okinf = okc = True
        msg = []
        for smin in (S_MIN, 0.5):
            reg = _try(lambda smin=smin: registry(sid, P, s_min_um=smin), None)
            if reg is None:
                okreg = oks = okinf = okc = False
                continue
            I_, cen = reg['instances'], reg['census']
            okreg &= bool(cen.get('n_pieces') == 2 and len(I_['fi']) == 1 and not bool(I_['self'][0])
                          and int(I_['fi'][0]) == int(I_['fj'][0]) == 10 and int(I_['piece_i'][0]) != int(I_['piece_j'][0])
                          and bool(I_['realized'][0]) and (_pcells(reg, 0, 'i'), _pcells(reg, 0, 'j')) == ((1, 1, ca), (1, 1, cb)))
            r = _try(lambda reg=reg: solve(sid, sig_e(), GAP_N, plan(reg, rj)), None)
            I = I_of(r, GAP_N) if r is not None else math.nan
            oks &= rel(I, want) < 1e-12
            ri = _try(lambda reg=reg: solve(sid, sig_e(), GAP_N, plan(reg, math.inf, allow_rj_limits=True)), None)
            okinf &= bool(ri is not None and ri['sigma_eff'] == 0.0 and ri.get('reason') == 'no_through_component')
            okc &= bool(cen.get('n_instances_same_fid_pieces') == 1 and cen.get('n_self_revisits_path_only') == 0
                        and cen.get('n_revisit_pairs') == 0 and cen.get('n_piece_cell_meets') == (1 if ca == cb else 0))
            msg.append((smin, len(I_['fi']), I, None if ri is None else ri.get('reason'),
                        {k: cen.get(k) for k in ('n_pieces', 'n_instances_same_fid_pieces', 'n_self_revisits_path_only',
                                                 'n_revisit_pairs', 'n_piece_cell_meets')}))
        print(f'    GAP {nm}: 손 {want:.9g} · 옛 경로 (접합 끔) {I_leg:.9g} · {msg}')
        chk(f'GAP {nm} — 조각 2 · instance 1 (조각 쌍 · 같은 fid · 자기 아님 · 실현) · 포트 = (1,1,{ca}) · (1,1,{cb}) (s_min 3 · 0.5)', okreg,
            f'{msg}')
        chk(f'GAP {nm} — σ = 손 회로 (조각 사슬 + R_j 간선 하나 · 1e-12) · s_min 무관', oks, f'{msg}')
        chk(f'GAP {nm} — R_j = ∞ → 조각 사이 전류 0 (no_through_component · 조각은 접합으로만 이어진다)', okinf, f'{msg}')
        chk(f"GAP {nm} — census: 같은 fid 조각 쌍 instance 1 · 같은 셀 조각 만남 {1 if ca == cb else 0} · 같은 조각 재방문 0 · "
            f"'경로로만' 0 (옛 = 거짓 1)", okc, f'{msg}')
    VP, NPd, sv = 0.15, (3, 3, 8), 7853.98
    gax, gpl = sv * VP, sv * VP * VP / (0.5 * VP)
    sig = sig_e(s_vgcf=sv, s_am=0.0041)
    for nm, ze, zs, ca, cb in (('같은 셀 (끝 z 0.47 · 0.59)', 0.47, 0.59, 3, 3), ('면 인접 (끝 z 0.40 · 0.52)', 0.40, 0.52, 2, 3)):
        P = rows_pieces([densify([(0.225, 0.225, 0.075), (0.225, 0.225, ze)], 0.05),
                         densify([(0.225, 0.225, zs), (0.225, 0.225, 1.125)], 0.05)])
        sid, _ = bed(P, NPd, vox=VP)
        reg = _try(lambda: registry(sid, P, vox=VP, r_f_um=0.075, tol_ff_um=0.03, L_par_um=0.30, r_port_um=0.30, s_min_um=0.3), None)
        r = _try(lambda: solve(sid, sig, NPd, plan(reg, 1e6), vox=VP), None) if reg is not None else None
        want = chain_I([gpl] + [gax] * ca + [1e4 / 1e6] + [gax] * (7 - cb) + [gpl])
        I = I_of(r, NPd, vox=VP) if r is not None else math.nan
        rl = solve_legacy(sid, sig, NPd, vox=VP)
        print(f"    GAP 생산 단위 {nm}: σ {None if r is None else r['sigma_eff']} S/cm · 옛 경로 (접합 끔) {rl['sigma_eff']} · 손 I {want:.9g}")
        #  허용 1e-9 — 생산 단위 대비 (축 g ≈ 1.2e3 ↔ 접합 g 1e-2 · 1e5 배) 에서 직접 풀이 반올림이 ~1e-11 상대 · 구조 차이 (축 면 하나
        #  더 · 덜) = ~1e-5 상대 → 1e-9 로도 판별
        chk(f'GAP 생산 단위 {nm} (h 0.15 · r_f 0.075 · tol_ff 0.03 · 틈 0.12 · s_min 0.3 · R_j 1e6) — instance 1 (조각 쌍) · '
            f'σ = 손 회로 (1e-9 · 대비 1e5)',
            reg is not None and len(reg['instances']['fi']) == 1 and not bool(reg['instances']['self'][0]) and rel(I, want) < 1e-9,
            f'{I} ↔ {want}')


RING_N = (5, 3, 8)
RING = [(1.5, 1.5, 4.2), (1.5, 1.5, 7.5), (3.5, 1.5, 7.5), (3.5, 1.5, 0.5), (1.5, 1.5, 0.5), (1.5, 1.5, 4.2)]


@case('RING')
def t_ring():
    """★ PRE-impl-06 · 1저자 Q-A — 닫힌 경로 (첫 점 = 끝 점 · 좌표 비트 같음) 의 이음매 = 연속 (접합도 끊김도 아님).  옛 판: 이음매 셀의 첫 ·
    끝 위치 = 같은 fid 재방문 (s = 고리 길이 18) → s ≥ s_min 이면 R_j 접합 (18.47 · −28 %) · s < s_min 이면 경로로만 (끊김 · 12.93 · −50 %).
    기대 = 손 연속 고리 회로 (= 옛 경로 25.641) · s_min 무관.  틈 하나 있는 고리 = 이음매를 지나 한 조각 (열린 가닥) + 틈 두 끝 사이 자기 접합
    (중심선 1.0 · s 17 · 손 회로 = 고리에서 틈 축 간선 하나를 R_j 간선으로)."""
    rj = 1e3
    pts = densify(RING)
    cells = _cells_of_pts(pts)
    want = _graph_ref(cells, RING_N)
    P = rows([RING])
    sid, _ = bed(P, RING_N)
    I_leg = I_of(solve_legacy(sid, sig_e(), RING_N), RING_N)
    for smin in (S_MIN, 100.0):
        reg = _try(lambda smin=smin: registry(sid, P, s_min_um=smin), None)
        r1 = _try(lambda reg=reg: solve(sid, sig_e(), RING_N, plan(reg, rj)), None) if reg is not None else None
        ri = _try(lambda reg=reg: solve(sid, sig_e(), RING_N, plan(reg, math.inf, allow_rj_limits=True)), None) if reg is not None else None
        I1 = I_of(r1, RING_N) if r1 is not None else math.nan
        Ii = I_of(ri, RING_N) if ri is not None else math.nan
        cen = (reg or {}).get('census') or {}
        chk(f'RING s_min {smin:g} — 이음매 = 연속: 자기 접합 0 · σ = 손 연속 고리 회로 (= 옛 경로 · 1e-12) · R_j = ∞ 도 같음',
            reg is not None and int(np.sum(reg['instances']['self'])) == 0 and rel(I1, want) < 1e-12 and rel(Ii, want) < 1e-12
            and rel(I_leg, want) < 1e-12,
            f"{None if reg is None else int(np.sum(reg['instances']['self']))} · {I1} · {Ii} ↔ {want} (옛 경로 {I_leg})")
        chk(f'RING s_min {smin:g} — census: 고리 조각 1 · 이음매 별칭 1 · 같은 조각 재방문 0 (첫 · 끝 위치 = 한 가지)',
            cen.get('n_ring_pieces') == 1 and cen.get('n_seam_alias') == 1 and cen.get('n_revisit_pairs') == 0,
            f"{ {k: cen.get(k) for k in ('n_ring_pieces', 'n_seam_alias', 'n_revisit_pairs', 'n_pieces')} }")
    m = ~((np.abs(pts[:, 0] - 3.5) < 1e-9) & (pts[:, 2] > 3.6) & (pts[:, 2] < 4.4))
    Pg = rows_pieces([pts[m]])
    sidg, _ = bed(Pg, RING_N)
    gapc = ((3, 1, 3), (3, 1, 4))
    wg = _graph_ref(cells, RING_N, drop=[gapc], extra=[(gapc[0], gapc[1], 1e4 / rj)])
    wgi = _graph_ref(cells, RING_N, drop=[gapc])
    regg = _try(lambda: registry(sidg, Pg, s_min_um=S_MIN), None)
    Ig = (regg or {}).get('instances') or {}
    cg = (regg or {}).get('census') or {}
    qs = [q for q in range(len(Ig.get('fi', []))) if Ig['self'][q]]
    rg = _try(lambda: solve(sidg, sig_e(), RING_N, plan(regg, rj)), None) if regg is not None else None
    rgi = _try(lambda: solve(sidg, sig_e(), RING_N, plan(regg, math.inf, allow_rj_limits=True)), None) if regg is not None else None
    chk('RING 틈 하나 (오른 다리 z 4.25 · 4.0 · 3.75 점 지움 · 틈 1.0) — 같은 sid · 이음매를 지나 한 조각 (조각 1 · 이음매 이음 1) · '
        '틈 두 끝 사이 자기 접합 하나 (포트 (3,1,3) · (3,1,4))',
        regg is not None and sidg.tobytes() == sid.tobytes() and cg.get('n_pieces') == 1 and cg.get('n_closed_paths_joined') == 1
        and len(qs) == 1 and {_pcells(regg, qs[0], 'i'), _pcells(regg, qs[0], 'j')} == set(gapc),
        f"{ {k: cg.get(k) for k in ('n_pieces', 'n_closed_paths_joined', 'n_ring_pieces')} } · 자기 {qs}")
    chk('RING 틈 하나 — σ = 손 회로 (연속 이음매 + 틈 R_j 간선 · 1e-12) · R_j = ∞ = 틈에서 열린 가닥 (1e-12)',
        rg is not None and rgi is not None and rel(I_of(rg, RING_N), wg) < 1e-12 and rel(I_of(rgi, RING_N), wgi) < 1e-12,
        f"{None if rg is None else I_of(rg, RING_N)} ↔ {wg} · {None if rgi is None else I_of(rgi, RING_N)} ↔ {wgi}")
    #  ★ 10-21 (변이 시험 다지기 · M12) — 닫힌 머리핀 (다리 둘 0.8 · 닿음) 의 이음매 = 다리 1 가운데 (z 3.5): 다리 사이 접합 쌍은 이음매 앞 · 뒤
    #    선분 번호로 갈리지만 고리 둘레로 이웃 → 접촉 하나 = 자기 instance 하나 (둘레 잇기를 끄면 둘)
    RH = [(1.5, 1.5, 3.5), (1.5, 1.5, 6.5), (2.3, 1.5, 6.5), (2.3, 1.5, 0.5), (1.5, 1.5, 0.5), (1.5, 1.5, 3.5)]
    Ph = rows([RH])
    sidh, _ = bed(Ph, RING_N)
    regh = _try(lambda: registry(sidh, Ph, s_min_um=S_MIN), None)
    Ih_ = (regh or {}).get('instances') or {}
    nh = int(np.sum(Ih_['self'])) if regh is not None else -1
    chk('RING 닫힌 머리핀 (이음매 = 다리 가운데) — 고리 조각 1 · 다리 사이 자기 접합 = 하나 (이음매를 지나는 쌍 무리 · 고리 둘레 이웃)',
        regh is not None and regh['census'].get('n_ring_pieces') == 1 and nh == 1,
        f"{None if regh is None else regh['census'].get('n_ring_pieces')} · 자기 {nh}")


SFR_N = (5, 8, 8)
SFR = [(1.95, 1.95, 0.5), (1.95, 1.95, 3.5), (1.95, 6.5, 3.5), (1.95, 6.5, 6.5), (2.05, 6.5, 6.5), (2.05, 6.5, 6.6), (3.5, 6.5, 6.6),
       (3.5, 2.05, 6.6), (2.05, 2.05, 6.6), (2.05, 2.05, 1.5)]


@case('SELFD')
def t_self_vs_distinct():
    """★ PRE-impl-02 · 1저자 Q-B — 자기 접합 탐지 = 서로 다른 섬유와 같은 중심선 근접 (d ≤ D) · 같은 섬유 쌍만 덧붙여 s 규칙.
    (i) KW (다리 중심선 1.2 > D 1.1 · 면 인접 셀): 옛 판 = 같은 fid 만 자기 접합 1 (L_c 0 · σ +4.25 %) ↔ 다른 fid instance 0 →
        같은 fid 도 instance 0 · 다리 사이 면 = 미등록 (fid 무관) · σ 가 R_j 와 무관 (= 손 사슬)
    (ii) SFR (다리 중심선 0.1414 < 2 r_f · 모서리 인접 셀 · 면 없음): 옛 판 = 같은 fid 접합 0 ↔ 다른 fid instance 1 →
        같은 fid 도 그 접합 · 기록 = 둘로 나눈 서로 다른 섬유와 같음 (L_c · 배율 · k · 포트 셀 · d0)
    (iii) XC (교차 · 닿음 0.8) 같은 fid ↔ 둘로 나눔 — 기록 같음."""
    rj = 1e3
    PW = rows(KW)
    sidw, _ = bed(PW, KU_N)
    rw = _try(lambda: registry(sidw, PW, s_min_um=KW_SMIN), None)
    seqw = seq_cells(KW[0])
    w_chain = chain_ref(len(seqw))
    rc = _try(lambda: solve(sidw, sig_e(), KU_N, plan(rw, rj)), None) if rw is not None else None
    rinf = _try(lambda: solve(sidw, sig_e(), KU_N, plan(rw, math.inf, allow_rj_limits=True)), None) if rw is not None else None
    rf = _try(lambda: solve(sidw, sig_e(), KU_N, plan(rw, rj, unreg_law='fused')), None) if rw is not None else None
    I_leg = I_of(solve_legacy(sidw, sig_e(), KU_N), KU_N)
    ok_i = (rw is not None and rc is not None and rinf is not None and rf is not None and len(rw['instances']['fi']) == 0
            and np.float64(rc['sigma_eff']).tobytes() == np.float64(rinf['sigma_eff']).tobytes()
            and rel(I_of(rc, KU_N), w_chain) < 1e-12 and rel(I_of(rf, KU_N), I_leg) < 1e-12)
    chk('SELFD (i) KW 같은 fid — instance 0 · σ(R_j 1e3) = σ(R_j ∞) (비트 · 접합 효과 0 · 옛 판 +4.25 %) = 손 사슬 (cut · 1e-12) · '
        'fused 법칙 = 옛 경로 (1e-12)', ok_i,
        f"{None if rw is None else len(rw['instances']['fi'])} · {None if rc is None else I_of(rc, KU_N)} · "
        f"{None if rinf is None else I_of(rinf, KU_N)} ↔ {w_chain} · fused {None if rf is None else I_of(rf, KU_N)} ↔ {I_leg}")
    PWd = rows([KW[0][:2], KW[0][2:]])
    sidwd, _ = bed(PWd, KU_N)
    rwd = _try(lambda: registry(sidwd, PWd, s_min_um=KW_SMIN), None)
    fk_s = [_face_kinds(rw, (1, 1, z), (2, 1, z)) for z in (1, 2, 3)] if rw is not None else None
    fk_d = [_face_kinds(rwd, (1, 1, z), (2, 1, z)) for z in (1, 2, 3)] if rwd is not None else None
    chk('SELFD (i) KW 같은 fid ↔ 둘로 나눈 서로 다른 섬유 — 둘 다 instance 0 · 다리 사이 면 셋 (z 1 · 2 · 3) = 미등록 (분류 fid 무관)',
        rw is not None and rwd is not None and len(rwd['instances']['fi']) == 0 and fk_s == fk_d == [[CJ.K_UNREG]] * 3,
        f'같은 fid {fk_s} · 나눔 {fk_d}')
    Ps = rows([SFR])
    sids, _ = bed(Ps, SFR_N)
    rs = _try(lambda: registry(sids, Ps, s_min_um=S_MIN), None)
    Pd = rows([SFR[:4], SFR[6:]])
    sidd, _ = bed(Pd, SFR_N)
    rd = _try(lambda: registry(sidd, Pd, s_min_um=S_MIN), None)
    leg = None
    if rs is not None:
        Is = rs['instances']
        cand = [q for q in range(len(Is['fi'])) if Is['self'][q]]
        leg = cand[0] if len(cand) == 1 else None
    rec_s = _inst_rec(rs, leg) if leg is not None else None
    rec_d = _inst_rec(rd, 0) if (rd is not None and len(rd['instances']['fi']) == 1) else None
    #  접점 = 최소 거리 0.1 (위 가로 (1.95, y, 3.5) 가 끝 다리 (2.05, 2.05, ·) 곁을 지나는 자리 · 셀 (1,2,3)) — 다리 둘 (0.1414) 보다 가깝다
    chk('SELFD (ii) SFR 같은 fid (모서리 인접 다리 · 중심선 0.1414 < 2 r_f · 다리 셀 면 공유 없음) — 자기 접합 하나 (옛 판 = 면 항목 셀 조각의 '
        '다른 기록) · 기록 (L_c · 배율 · k · 분산 간선 포트 셀 · d0) = 둘로 나눈 서로 다른 섬유 instance (하나) 와 같음 (1e-12)',
        _rec_same(rec_s, rec_d), f'같은 fid {rec_s} · 나눔 {rec_d}')
    Px = rows(XC)
    sidx, _ = bed(Px, XC_N)
    rx = _try(lambda: registry(sidx, Px, s_min_um=5.0), None)
    Pxd = rows([XC_A, XC_B])
    sidxd, _ = bed(Pxd, XC_N)
    rxd = _try(lambda: registry(sidxd, Pxd, s_min_um=5.0), None)
    qx = [q for q in range(len(((rx or {}).get('instances') or {}).get('fi', []))) if rx['instances']['self'][q]]
    rec_x = _inst_rec(rx, qx[0]) if len(qx) == 1 else None
    rec_xd = _inst_rec(rxd, 0) if (rxd is not None and len(rxd['instances']['fi']) == 1) else None
    chk('SELFD (iii) XC 교차 같은 fid ↔ 둘로 나눔 — 기록 같음 (L_c 1.2 · 배율 1 · k 1 · 포트 (1,1,2)–(2,1,2) · d0 0.8)',
        _rec_same(rec_x, rec_xd) and rec_xd is not None and abs(rec_xd['Lc'] - XC_LC) < 1e-9 and abs(rec_xd['d0'] - 0.8) < 1e-12,
        f'같은 fid {rec_x} · 나눔 {rec_xd}')


@case('QC')
def t_no_relocation():
    """★ PRE-impl-03 · 1저자 Q-C — 덮인 접점은 이웃 셀로 옮기지 않는다 (미실현 `covered_<sid>` · 덮은 상의 법칙만 = SDCP 는 SV 융합 한 번 ·
    같은 접촉을 두 번 세지 않는다) · 접합 + centerline PTFE = 거부 (옛 판: PTFE 피브릴이 포트 셀을 sid 7 로 덮으면 포트가 옆 셀로 옮겨
    σ 5.556 → 5.882 (+5.88 % · 절연체를 더해 σ 상승 = Rayleigh 위반) · SDCP 덮임 (DBE) = 옮긴 접합 + SV 융합 병렬 12.154 (+2.09 %))."""
    rj = 1e3
    P = cat_rows(rows(F2), rows([[(1.5, 1.5, 3.5)]], phase=5, kind=0, fid0=700))
    sid, _ = bed(P, F2_N)
    reg = _try(lambda: registry(sid, P, tol_sj_um=0.1, r_sdcp_um=0.5), None)
    gsv = 2.0 * SV * 250.0 / (SV + 250.0) * H
    E = [(0, 1, G_AX), (1, 2, G_AX), (2, 3, gsv), (3, 4, gsv)] + [(4 + i, 5 + i, G_AX) for i in range(4)]
    w_sv = ref_I(9, E, [(0, G_PL)], [(8, G_PL)])
    w_old = ref_I(9, E + [(2, 4, 1e4 / rj)], [(0, G_PL)], [(8, G_PL)])
    I_ = (reg or {}).get('instances') or {}
    S_ = (reg or {}).get('subedges') or {}
    chk('QC ① SDCP 가 접점 셀 (A 위끝 (1,1,3)) 을 덮음 — sid 5 · instance 1 · 미실현 (사유 covered_SDCP · instance · 간선) · 옮긴 포트 없음',
        reg is not None and int(sid[1, 1, 3]) == 5 and len(I_['fi']) == 1 and not bool(I_['realized'][0])
        and str(I_['reason'][0]) == 'covered_SDCP' and len(S_['inst']) == 1 and not bool(S_['realized'][0])
        and str(S_['reason'][0]) == 'covered_SDCP',
        f"{None if reg is None else (len(I_['fi']), list(I_['realized']), list(I_['reason']), list(S_.get('reason', [])))}")
    Ir = _try(lambda: I_of(solve(sid, sig_e(), F2_N, plan(reg, rj, ptfe_stamp='face_alpha')), F2_N))
    Ii = _try(lambda: I_of(solve(sid, sig_e(), F2_N, plan(reg, math.inf, allow_rj_limits=True, ptfe_stamp='face_alpha')), F2_N))
    print(f'    QC ① σ 접합 {Ir!r} · R_j ∞ {Ii!r} · 손 SV 만 {w_sv!r} · 옛 (옮긴 접합 + SV) {w_old!r}')
    chk('QC ① σ = SV 융합만 손 회로 (1e-12) = R_j ∞ (같은 접촉 한 번 · 옛 판 = 옮긴 접합 + SV 병렬 = +2.09 %)',
        rel(Ir, w_sv) < 1e-12 and rel(Ii, w_sv) < 1e-12, f'{Ir} · {Ii} ↔ {w_sv} (옛 {w_old})')
    P2 = rows(F2)
    sid2, _ = bed(P2, F2_N)
    reg2 = registry(sid2, P2)
    pl2 = plan(reg2, rj)
    pm = dict(pl2)
    pm['ptfe_stamp'] = 'centerline'
    pm['record'] = dict(pl2['record'], ptfe_stamp='centerline')
    pm['fp_rows'] = CJ.plan_rows_fp(pm)
    import ca_ext_cjunc as CW
    req = dict(R_j_ohm=1e6, len_law=CJ.CJUNC_LEN_LAW, unreg_law='cut', s_min_um=0.5, tol_ff_um=0.03)
    _CG_CALLS[0] = 0
    g = [('계획 centerline P0 (정량)', raises(lambda: plan(reg2, rj, ptfe_stamp='centerline', ptfe_jlaw='P0'))),
         ('계획 centerline P0 (시험 모드 · quantitative False)',
          raises(lambda: plan(reg2, rj, ptfe_stamp='centerline', ptfe_jlaw='P0', quantitative=False))),
         ('솔브 입구 — 계획 ptfe_stamp 만 centerline 으로 · 행 지문 다시 만듦', raises(lambda: solve(sid2, sig_e(), F2_N, pm))),
         ('protocol 기록 (ca_ext_cjunc.cjunc_protocol_record) centerline P0',
          raises(lambda: CW.cjunc_protocol_record(ptfe_stamp='centerline', ptfe_jlaw='P0', **req)))]
    cg = _CG_CALLS[0]
    for nm, okk in g:
        chk(f'QC ② 접합 + centerline = 거부 — {nm}', okk)
    pos_ok = _try(lambda: solve(sid2, sig_e(), F2_N, pl2)['sigma_eff'] > 0.0, False) is True
    fa_ok = _try(lambda: CW.cjunc_protocol_record(ptfe_stamp='face_alpha', ptfe_jlaw='P0', **req)['ptfe_stamp'] == 'face_alpha',
                 False) is True
    chk('QC ② 거부 경로 CG 0 · 양성 대조 (off 계획 풀림 · face_alpha protocol 받음)', cg == 0 and pos_ok and fa_ok,
        f'CG {cg} · off {pos_ok} · face_alpha {fa_ok}')


SVY_N = (6, 3, 8)
SVY = [[(1.5, 1.5, 0.5), (1.5, 1.5, 7.5)], [(1.5, 2.5, 3.5), (4.5, 2.5, 3.5), (4.5, 2.5, 7.5)]]


@case('QD')
def t_sv_split():
    """★ PRE-impl-04 · 1저자 Q-D — SV 반사실 대조 = 서로 다른 섬유 (또는 접합으로 갈린 같은 섬유 가지) 사이 SV 우회만 끊는다 · 섬유 자기
    연속 (SDCP 가 덮은 섬유 셀을 지나는 같은 조각의 길) 은 남긴다 · 끊기만 (부분 그래프 → 비 ≥ 1 · Rayleigh).  옛 판 = SV 면 전부 끊음 →
    SDCP 를 지나는 섬유 하나도 비 ∞ · SV_DEPENDENT (판정 문장 늘 제한 · 정보 없음)."""
    rj = 1e3
    gsv = 2.0 * SV * 250.0 / (SV + 250.0) * H

    def cf(sid, P, n):
        reg = _try(lambda: registry(sid, P, tol_sj_um=0.1, r_sdcp_um=0.5), None)
        r = _try(lambda: solve(sid, sig_e(), n, plan(reg, rj, sv_counterfactual={'threshold': 2.0})), None) if reg is not None else None
        return reg, r, (((r or {}).get('cjunc') or {}).get('sv_counterfactual') or {})
    n1 = (3, 3, 8)
    P1 = cat_rows(rows([[(1.5, 1.5, 0.5), (1.5, 1.5, 7.5)]]), rows([[(1.5, 1.5, 3.5)]], phase=5, kind=0, fid0=700))
    sid1, _ = bed(P1, n1)
    reg1, r1, c1 = cf(sid1, P1, n1)
    w1 = chain_I([G_PL] + [G_AX] * 2 + [gsv, gsv] + [G_AX] * 3 + [G_PL])
    chk('QD ① 섬유 하나가 SDCP 셀 (1,1,3) 을 지남 (접합 0) — σ = 손 사슬 (SV 두 면 · 1e-12) · 반사실 비 = 1 정확 (자기 연속 남김 · '
        '옛 = ∞ · SV_DEPENDENT) · 끊은 SV 면 0 · 표지 없음',
        r1 is not None and int(sid1[1, 1, 3]) == 5 and rel(I_of(r1, n1), w1) < 1e-12 and c1.get('status') == 'computed'
        and c1.get('sv_counterfactual_ratio') == 1.0 and c1.get('n_sv_faces_cut') == 0 and c1.get('flag') is None,
        f"{None if r1 is None else I_of(r1, n1)} ↔ {w1} · {c1}")
    P2 = cat_rows(rows(F1), rows([[(1.5, 1.5, 1.5)]], phase=5, kind=0, fid0=700))
    sid2, _ = bed(P2, F1_N)
    reg2, r2, c2 = cf(sid2, P2, F1_N)
    w2 = chain_I([G_PL] + [gsv, gsv] + [G_AX] + [1e4 / rj] + [G_AX] * 7 + [G_PL])
    chk('QD ② F1 (접합 하나) + 접합에서 먼 SDCP (A 셀 (1,1,1) 덮음) — σ = 손 사슬 (1e-12) · 접합 실현 · 반사실 비 1 정확 · 표지 없음',
        r2 is not None and int(sid2[1, 1, 1]) == 5 and rel(I_of(r2, F1_N), w2) < 1e-12
        and bool(reg2['instances']['realized'][0]) and c2.get('sv_counterfactual_ratio') == 1.0 and c2.get('flag') is None,
        f"{None if r2 is None else I_of(r2, F1_N)} ↔ {w2} · {c2}")
    P3 = cat_rows(rows(SVY), rows([[(1.5, 1.5, 3.5)]], phase=5, kind=0, fid0=700))
    sid3, _ = bed(P3, SVY_N)
    reg3, r3, c3 = cf(sid3, P3, SVY_N)
    #  손 회로 — A0..A2 (1,1,0..2) = 0..2 · S (1,1,3) = 3 · A4..A7 (1,1,4..7) = 4..7 · B 셀 열 (1,2,3) (2,2,3) (3,2,3) (4,2,3) (4,2,4..7) = 8..15
    E3 = ([(0, 1, G_AX), (1, 2, G_AX), (2, 3, gsv), (3, 4, gsv), (4, 5, G_AX), (5, 6, G_AX), (6, 7, G_AX), (3, 8, gsv)]
          + [(8 + i, 9 + i, G_AX) for i in range(7)])
    bot, top = [(0, G_PL)], [(7, G_PL), (15, G_PL)]
    I_full = ref_I(16, E3, bot, top)
    I_cut = ref_I(16, [e for e in E3 if e[:2] != (3, 8)], bot, top)
    I3 = (reg3 or {}).get('instances') or {}
    chk('QD ③ SVY (A 가 SDCP 셀 (1,1,3) 을 지남 · B 가 그 셀에 닿음) — A–B 접점 = SDCP 덮임 (미실현 covered_SDCP) · σ = 손 회로 (1e-12)',
        r3 is not None and int(sid3[1, 1, 3]) == 5 and len(I3['fi']) == 1 and not bool(I3['realized'][0])
        and str(I3['reason'][0]) == 'covered_SDCP' and rel(I_of(r3, SVY_N), I_full) < 1e-12,
        f"{None if r3 is None else I_of(r3, SVY_N)} ↔ {I_full} · {None if reg3 is None else (list(I3['realized']), list(I3['reason']))}")
    chk('QD ③ SVY 반사실 = B 의 SV 면만 끊음 (A 자기 연속 남김) — 비 = 손 I_full/I_cut (1e-10 · 옛 = A 도 끊음) · 끊은 SV 면 1 · '
        '다리 놓는 SDCP 성분 1 · 못 가른 성분 0 · 문턱 2 → SV_DEPENDENT 여부 = 비 ≥ 2',
        c3.get('status') == 'computed' and rel(float(c3.get('sv_counterfactual_ratio') or math.nan), I_full / I_cut) < 1e-10
        and c3.get('n_sv_faces_cut') == 1 and c3.get('n_bridging_components') == 1 and c3.get('n_unsplit_bridging_components') == 0
        and c3.get('flag') == ('SV_DEPENDENT' if I_full / I_cut >= 2.0 else None),
        f'{c3} ↔ 손 비 {I_full / I_cut}')
    kd = c3.get('kind')
    nfields = ('n_sdcp_components_touching', 'n_bridging_components', 'n_sv_faces_cut', 'n_sv_faces_kept_self',
               'n_unsplit_bridging_components')
    chk('QD ④ 기록 꼴 — 종류 counterfactual… (옛 counterfactual_cut_sv_faces 아님 · 정의가 바뀌었다) · 수 칸 다섯 = 정수',
        isinstance(kd, str) and kd.startswith('counterfactual') and kd != 'counterfactual_cut_sv_faces'
        and all(type(c3.get(k)) is int for k in nfields), f'{kd} · {[(k, c3.get(k)) for k in nfields]}')


#  ★ 10-22 (사전 리뷰 2 회차 PRE2-impl-01 · 04 · 1저자 Q1 (다)) — SV 반사실 괄호 회로 (셀 단위 · vox 1 · SDCP 점 = 셀 하나 · 손으로 풀림)
QD2_N1 = (5, 3, 9)                                                   # ① 리뷰어 회로 — A · B 가 같은 덩어리를 지남 (길 = A → 덩어리 → B 하나)
QD2_A1 = [(1.5, 1.5, 0.5), (1.5, 1.5, 6.5)]                          #    A = 아래 판 → z 6 끝 (위 판에 안 닿음)
QD2_B1 = [(3.5, 1.5, 2.5), (3.5, 1.5, 8.5)]                          #    B = z 2 시작 → 위 판 (A ↔ B 중심선 2.0 > D 1.1 · 접합 없음)
QD2_B1C = [(3.5, 1.5, 4.5), (3.5, 1.5, 8.5)]                         # ② 대조 — B 가 덩어리 안에서 시작 (A 만 지남)
QD2_S1 = [(1.5, 1.5, 4.5), (2.5, 1.5, 4.5), (3.5, 1.5, 4.5)]         #    덩어리 = (1..3, 1, 4) — A · B 의 z 4 셀을 덮는다
QD2_N3 = (9, 3, 9)                                                   # ③ 괄호 성질 — 참 비를 손으로 가를 수 있는 꼴 (다리 셀 (2,1,3) 이 따로)
QD2_A3 = [(1.5, 1.5, 0.5), (1.5, 1.5, 8.5)]                          #    A = 판–판 (덩어리 (1,1,3) 을 지남)
QD2_B3 = [(3.5, 1.5, 0.5), (3.5, 1.5, 5.5)]                          #    B = 아래 판 → z 5 끝 (덩어리 (3,1,3) 을 지남 · 위 판에 안 닿음)
QD2_C3 = [(7.5, 1.5, 0.5), (7.5, 1.5, 8.5)]                          #    C = 판–판 (덩어리와 먼 병렬 길)
QD2_S3 = [(1.5, 1.5, 3.5), (2.5, 1.5, 3.5), (3.5, 1.5, 3.5)]
QD2_N4 = (7, 3, 9)                                                   # ④ (변이 J1) — 지나는 섬유 둘 (A · B) + 닿기만 하는 섬유 C
QD2_A4 = [(1.5, 1.5, 0.5), (1.5, 1.5, 8.5)]
QD2_B4 = [(5.5, 1.5, 0.5), (5.5, 1.5, 8.5)]
QD2_C4 = [(3.5, 1.5, 4.5), (3.5, 1.5, 8.5)]                          #    C = 덩어리 가운데 셀 위에서 시작 → 위 판 (지나지 않음)
QD2_S4 = [(1.5, 1.5, 3.5), (2.5, 1.5, 3.5), (3.5, 1.5, 3.5), (4.5, 1.5, 3.5), (5.5, 1.5, 3.5)]
QD2_N5 = (6, 3, 9)                                                   # ⑤ (변이 J2) — A 는 지남 · B 는 덮이지 않은 사이 셀 (4,1,4) 을 두고 두 번 닿음
QD2_A5 = [(2.5, 1.5, 0.5), (2.5, 1.5, 8.5)]
QD2_B5 = [(4.5, 1.5, 0.5), (4.5, 1.5, 8.5)]
QD2_S5 = [(2.5, 1.5, 3.5), (2.5, 1.5, 4.5), (2.5, 1.5, 5.5), (3.5, 1.5, 3.5), (3.5, 1.5, 5.5)]
QD2_N11 = (5, 3, 6)                                                  # ⑪ 못 가른 덩어리가 아래 판에 닿음 — A · B (판–판) 가 (1,1,1) · (3,1,1) 을
QD2_A11 = [(1.5, 1.5, 0.5), (1.5, 1.5, 5.5)]                         #    지나고 덩어리 = (1..3,1,1) + (2,1,0) (아래 판 결합 셀 하나)
QD2_B11 = [(3.5, 1.5, 0.5), (3.5, 1.5, 5.5)]
QD2_S11 = [(1.5, 1.5, 1.5), (2.5, 1.5, 1.5), (3.5, 1.5, 1.5), (2.5, 1.5, 0.5)]


@contextlib.contextmanager
def cert_on(solver=None):
    """증서 켠 풀이 (★ 10-23 · 생산 `--step3-rtol` 꼴 — CONV_CERT · 정지 rtol 1e-12 · 직접해 (또는 주어진 풀이)) — SV 반사실 기록이 증서 구간
    지위로 나온다 (사슬 판정 = 증서 구간 비).  끝나면 셋 다 되돌린다."""
    from scipy.sparse.linalg import spsolve

    def _direct(L, b, *a, **k):
        _CG_CALLS[0] += 1
        return spsolve(L.tocsc(), b), 0
    old = S3._solve_cg, S3.CONV_CERT, S3.CG_RTOL
    S3._solve_cg, S3.CONV_CERT, S3.CG_RTOL = (solver or _direct), True, 1.0e-12
    try:
        yield
    finally:
        S3._solve_cg, S3.CONV_CERT, S3.CG_RTOL = old


def _qd2_run(polys, sdcp, n, rj=1e3, thr=None, reg_hook=None, cert=False):
    """괄호 회로 하나 → (sid, 원장, 해, 반사실 원 기록).  reg_hook = 원장을 계획 전에 바꾸는 함수 (변조 시험) · ★ 10-23 cert = 증서 켠 풀이
    (`cert_on` · 사슬 판정을 보는 자리)."""
    P = cat_rows(rows(polys), rows([[p] for p in sdcp], phase=5, kind=0, fid0=700))
    sid, _ = bed(P, n, sdcp_sphere_d_um=0.0)
    reg = _try(lambda: registry(sid, P, tol_sj_um=0.1, r_sdcp_um=0.5), None)
    if reg is not None and reg_hook is not None:
        reg_hook(reg)
    if reg is None:
        r = None
    elif cert:
        with cert_on():
            r = _try(lambda: quiet(S3.solve_sigma_z, sid, sig_e(), H, z_top_um=float(n[2]) * H, z_bot_um=0.0,
                                   cjunc=plan(reg, rj, sv_counterfactual={'threshold': thr})), None)
    else:
        r = _try(lambda: solve(sid, sig_e(), n, plan(reg, rj, sv_counterfactual={'threshold': thr})), None)
    return sid, reg, r, (((r or {}).get('cjunc') or {}).get('sv_counterfactual') or {})


def _qd2_census(r):
    """해의 접합 기록 census (= 원장 census · 증거 `census` 꼴 — JSON 정수) — 검증기에 실제 census 를 준다 (★ 10-23 · RCA2-04)."""
    return json.loads(json.dumps(((r or {}).get('cjunc') or {}).get('census') or {}, default=int))


def _qd2_ref_I(nn, edges, bot, top):
    """손 회로 (`ref_I`) — 간선을 뺀 뒤 판에 닿지 않는 조각 (떠 있는 막다른 가지 · 전류 0) 은 빼고 푼다 (특이 방지 · 값 불변).  두 판을 잇는
    길이 없으면 0 (관통 없음)."""
    adj = {}
    for i, j, _g in edges:
        adj.setdefault(i, set()).add(j)
        adj.setdefault(j, set()).add(i)

    def reach(seeds):
        seen, st = set(seeds), list(seeds)
        while st:
            for w in adj.get(st.pop(), ()):
                if w not in seen:
                    seen.add(w)
                    st.append(w)
        return seen
    rb, rt = reach([i for i, _ in bot]), reach([i for i, _ in top])
    if not (rb & rt):
        return 0.0
    keep = rb | rt
    return ref_I(nn, [e for e in edges if e[0] in keep and e[1] in keep], [b for b in bot if b[0] in keep],
                 [t for t in top if t[0] in keep])


def _qd2_ref3():
    """QD2 ③ 괄호 회로의 손 회로 (모듈 밖) → (I_full · I_참 (다리 셀 (2,1,3) 의 면만 끊음) · I_위 (덩어리 셀 셋을 뺀 판)) — QD2 ③ · QD3 ⑤ 공용.
    노드 — A0..A2 = 0..2 · S1 (1,1,3) = 3 · A4..A8 = 4..8 · S2 (2,1,3) = 9 · S3 (3,1,3) = 10 · B0..B2 = 11..13 · B4 · B5 = 14 · 15 · C0..C8 = 16..24."""
    gsv = 2.0 * SV * 250.0 / (SV + 250.0) * H
    gss = 250.0 * H
    E3 = ([(0, 1, G_AX), (1, 2, G_AX), (2, 3, gsv), (3, 4, gsv)] + [(4 + i, 5 + i, G_AX) for i in range(4)]
          + [(3, 9, gss), (9, 10, gss)] + [(11, 12, G_AX), (12, 13, G_AX), (13, 10, gsv), (10, 14, gsv), (14, 15, G_AX)]
          + [(16 + i, 17 + i, G_AX) for i in range(8)])
    bot3, top3 = [(0, G_PL), (11, G_PL), (16, G_PL)], [(8, G_PL), (24, G_PL)]
    return (_qd2_ref_I(25, E3, bot3, top3), _qd2_ref_I(25, [e for e in E3 if e[:2] not in ((3, 9), (9, 10))], bot3, top3),
            _qd2_ref_I(25, [e for e in E3 if not ({e[0], e[1]} & {3, 9, 10})], bot3, top3))


def _qd2_flags(cf, thr):
    """반사실 원 기록 → 증거 투영 → 사슬 꼴 → 사슬 판정 (실제 `ca_ext_svcf` · `rint_r_chain.sv_assess` · 모서리 하나 · 범위 R_j0)."""
    import ca_ext_svcf as _SV
    import rint_r_chain as _RRC
    view = _SV.chain_view(_SV.sv_cf_record(cf))
    return _RRC.sv_assess({('1', 'P0', 'R_j0'): {'sv_cf': view}}, thr, 'R_j0')[0]


def _qd2_j1_ok():
    """④ 아래 끝 = 덩어리 그대로 (지나지 않는 C 의 SV 면도 끊지 않는다 · 끊은 면 0 · 비 1 정확) — 변이 J1 (못 가른 다리 지킴 끔) 이 떨어뜨린다."""
    _s, _r, r, c = _qd2_run([QD2_A4, QD2_B4, QD2_C4], QD2_S4, QD2_N4)
    return r is not None and c.get('n_unsplit_bridging_components') == 1 and c.get('n_sv_faces_cut') == 0 \
        and c.get('sv_counterfactual_ratio') == 1.0


def _qd2_j2_ok():
    """⑤ B (덮이지 않은 사이 셀 (4,1,4) 을 두고 두 번 닿음) 는 덩어리를 지나지 않는다 → 못 가른 덩어리 0 · B 의 SV 면 둘을 끊음 — 변이 J2
    ('지남' = 사이 위치가 상자 안이기만 · 덮였는지 · 같은 성분인지 안 봄) 가 떨어뜨린다 (B 도 '지남' → 못 가른 덩어리 1 · 끊은 면 0)."""
    _s, _r, r, c = _qd2_run([QD2_A5, QD2_B5], QD2_S5, QD2_N5)
    return r is not None and c.get('n_unsplit_bridging_components') == 0 and c.get('n_sv_faces_cut') == 2


@case('QD2')
def t_sv_bracket():
    """★ 10-22 (사전 리뷰 2 회차 PRE2-impl-01 · 04 · 1저자 Q1 (다) · 등록 R §5-6 SV 행 개정) — SV 반사실 괄호 판정.  못 가른 덩어리 (섬유 둘
    이상이 함께 지나는 SDCP 성분 — 셀 단위로 섬유 자기 길과 다리를 못 가른다) 가 있으면 반사실을 두 번 푼다: 아래 끝 = 덩어리를 그대로 둔 판
    (옛 판) · 위 끝 = 그 덩어리 SDCP 셀의 면 (판 결합 포함) 을 전부 끊은 판 (아래 판이 끊은 다리 면도 그대로 끊는다 → 위 ⊇ 아래 · Rayleigh).
    덩어리 0 = 다시 풀지 않음 (위 = 아래).  사슬 판정 = 아래 끝 > 문턱 → SV_DEPENDENT · 위 끝 ≤ 문턱 → 표지 없음 · 걸침 · 못 읽음 →
    SV_UNCHECKED.  기대값 = 손 회로 (`ref_I` · 모듈 밖) · 판정 = 실제 `ca_ext_svcf` · `rint_r_chain.sv_assess` (옛 판 = 리뷰어 회로에서 비 1.0 ·
    computed · 표지 없음)."""
    import ca_ext_svcf as SVCF
    gsv = 2.0 * SV * 250.0 / (SV + 250.0) * H
    gss = 250.0 * H
    # ① 리뷰어 회로
    sid1, _r1, r1, c1 = _qd2_run([QD2_A1, QD2_B1], QD2_S1, QD2_N1, cert=True)
    w1 = chain_I([G_PL] + [G_AX] * 3 + [gsv, gss, gss, gsv] + [G_AX] * 3 + [G_PL])
    up1 = c1.get('upper') if isinstance(c1.get('upper'), dict) else {}
    chk('QD2 ① 리뷰어 회로 (A · B 가 같은 덩어리 (1..3,1,4) 를 지남) — σ = 손 사슬 (1e-12) · 못 가른 덩어리 1 · 아래 끝 = 덩어리 그대로 (끊은 면 0 · '
        '비 1 정확 · computed) · 위 끝 = 덩어리 셀 셋을 뺀 판 (관통 없음 → +∞ · no_through_without_sv · 위 끝 풀이 기록 · 뺀 셀 3 · 판 결합 0)',
        r1 is not None and all(int(sid1[x, 1, 4]) == 5 for x in (1, 2, 3)) and rel(I_of(r1, QD2_N1), w1) < 1e-12
        and c1.get('n_unsplit_bridging_components') == 1 and c1.get('status') == 'computed'
        and c1.get('sv_counterfactual_ratio') == 1.0 and c1.get('n_sv_faces_cut') == 0
        and c1.get('status_hi') == 'no_through_without_sv' and c1.get('sv_counterfactual_ratio_hi') == math.inf
        and up1.get('status') == 'no_through_without_sv' and up1.get('sv_counterfactual_ratio') == math.inf
        and up1.get('n_cells_removed') == 3 and up1.get('n_plate_couplings_cut') == 0,
        f'{None if r1 is None else I_of(r1, QD2_N1)} ↔ {w1} · {c1}')
    f1a, f1b = _try(lambda: _qd2_flags(c1, 2.0), None), _try(lambda: _qd2_flags(c1, 1.0e9), None)
    chk('QD2 ① 사슬 판정 — 괄호 [1, ∞] 가 문턱에 걸침 → SV_UNCHECKED (문턱 2 · 1e9 — 위 끝 ∞ · 옛 = 표지 없음 = PRE2-impl-01)',
        f1a == ['SV_UNCHECKED'] and f1b == ['SV_UNCHECKED'], f'{f1a} · {f1b}')
    # ② 대조 (한 섬유만 지남)
    _s2, _r2, r2, c2 = _qd2_run([QD2_A1, QD2_B1C], QD2_S1, QD2_N1, cert=True)
    f2 = _try(lambda: _qd2_flags(c2, 2.0), None)
    chk('QD2 ② 대조 (B 가 덩어리 안에서 시작 · A 만 지남) — σ = ① 과 같은 손 사슬 · 못 가른 덩어리 0 · B 의 SV 면을 끊음 (끊은 면 1 · 지금처럼) · '
        '비 +∞ (no_through_without_sv) · 다시 풀지 않음 (위 끝 풀이 기록 None · 위 = 아래) · 사슬 = SV_DEPENDENT',
        r2 is not None and rel(I_of(r2, QD2_N1), w1) < 1e-12 and c2.get('n_unsplit_bridging_components') == 0
        and c2.get('n_sv_faces_cut') == 1 and c2.get('status') == 'no_through_without_sv' and c2.get('sv_counterfactual_ratio') == math.inf
        and 'upper' in c2 and c2.get('upper') is None and c2.get('status_hi') == 'no_through_without_sv'
        and c2.get('sv_counterfactual_ratio_hi') == math.inf and f2 == ['SV_DEPENDENT'], f'{c2} · {f2}')
    # ③ 괄호 성질 — 아래 ≤ 참 ≤ 위 (참 = 섬유 자기 길 (A · B 가 덮인 셀을 지나는 면) 은 살리고 다리 셀 (2,1,3) 의 면만 끊은 판 · 손 회로)
    _s3, _r3, r3, c3 = _qd2_run([QD2_A3, QD2_B3, QD2_C3], QD2_S3, QD2_N3, cert=True)
    I3, I3_true, I3_hi = _qd2_ref3()
    lo3, hi3 = c3.get('sv_counterfactual_ratio'), c3.get('sv_counterfactual_ratio_hi')
    t3, h3 = I3 / I3_true, I3 / I3_hi
    up3 = c3.get('upper') if isinstance(c3.get('upper'), dict) else {}
    chk('QD2 ③ 괄호 성질 — σ = 손 회로 (1e-12) · 못 가른 덩어리 1 · 아래 끝 = 1 정확 (덩어리 그대로) · 위 끝 = 손 I_full/I_C (덩어리 셋을 뺀 판 · '
        '1e-12 · computed) · 손 참 비 (다리 셀 면만 끊음) 가 아래 < 참 < 위 (넓은 괄호 · Rayleigh)',
        r3 is not None and rel(I_of(r3, QD2_N3), I3) < 1e-12 and c3.get('n_unsplit_bridging_components') == 1
        and lo3 == 1.0 and c3.get('status_hi') == 'computed' and isinstance(hi3, float) and rel(hi3, h3) < 1e-12
        and up3.get('status') == 'computed' and up3.get('n_cells_removed') == 3 and 1.0 < t3 < h3 and lo3 <= t3 <= hi3,
        f'σ {None if r3 is None else I_of(r3, QD2_N3)} ↔ {I3} · 아래 {lo3} · 참 {t3} · 위 {hi3} ↔ 손 {h3} · {up3}')
    #  ★ 10-23 (RCA2-01 · Q1 (가)) — 판정 = 증서 구간: "문턱 = 위 끝" 의 위 끝 = 증서 구간 위비 (nominal 위 끝이 아니다 · 그 위비 ≥ nominal)
    import ca_ext_svcf as _SVq
    v3 = _try(lambda: _SVq.chain_view(_SVq.sv_cf_record(c3)), {}) or {}
    hc3 = v3.get('ratio_cert_hi')
    th3 = (1.0, 0.5 * (t3 + h3), (hc3 if isinstance(hc3, float) else math.nan), 2.0 * h3)
    f3 = [_try(lambda th=th: _qd2_flags(c3, th), None) for th in th3]
    chk('QD2 ③ 사슬 판정 (증서 구간 · 10-23) — 문턱 1 (아래비 ≤ 1 · 넘지 않음) · 참과 위 사이 = 걸침 → SV_UNCHECKED · 문턱 = 증서 구간 위비 (그 값) · '
        '위 끝 2 배 = 표지 없음 (위비 ≤ 문턱)',
        f3[0] == ['SV_UNCHECKED'] and f3[1] == ['SV_UNCHECKED'] and f3[2] == [] and f3[3] == [], f'{list(zip(th3, f3))}')
    # ④ 변이 J1 회로 — 지나는 섬유 둘 + 닿기만 하는 C
    _s4, _r4, r4, c4 = _qd2_run([QD2_A4, QD2_B4, QD2_C4], QD2_S4, QD2_N4, cert=True)
    #  노드 — A0..A2 = 0..2 · S1 = 3 · A4..A8 = 4..8 · S2..S4 = 9..11 · B0..B2 = 12..14 · S5 = 15 · B4..B8 = 16..20 · C4..C8 = 21..25
    E4 = ([(0, 1, G_AX), (1, 2, G_AX), (2, 3, gsv), (3, 4, gsv)] + [(4 + i, 5 + i, G_AX) for i in range(4)]
          + [(3, 9, gss), (9, 10, gss), (10, 11, gss), (11, 15, gss)]
          + [(12, 13, G_AX), (13, 14, G_AX), (14, 15, gsv), (15, 16, gsv)] + [(16 + i, 17 + i, G_AX) for i in range(4)]
          + [(10, 21, gsv)] + [(21 + i, 22 + i, G_AX) for i in range(4)])
    bot4, top4 = [(0, G_PL), (12, G_PL)], [(8, G_PL), (20, G_PL), (25, G_PL)]
    I4 = _qd2_ref_I(26, E4, bot4, top4)
    I4_j1 = _qd2_ref_I(26, [e for e in E4 if e[:2] != (10, 21)], bot4, top4)
    f4 = _try(lambda: _qd2_flags(c4, 2.0), None)
    chk('QD2 ④ 변이 J1 회로 (A · B 가 덩어리 (1..5,1,3) 를 지남 · C 는 닿기만) — σ = 손 회로 (1e-12) · 못 가른 덩어리 1 · 아래 끝 = 덩어리 그대로 '
        '(C 의 SV 면도 남김 · 끊은 면 0 · 비 1 정확 — J1 이면 C 를 끊어 손 비 I_full/I_C끊음 > 1) · 위 끝 = +∞ (뺀 셀 5) · 사슬 = SV_UNCHECKED',
        r4 is not None and rel(I_of(r4, QD2_N4), I4) < 1e-12 and c4.get('n_unsplit_bridging_components') == 1
        and c4.get('n_sv_faces_cut') == 0 and c4.get('sv_counterfactual_ratio') == 1.0 and I4 / I4_j1 > 1.0 + 1e-6
        and c4.get('sv_counterfactual_ratio_hi') == math.inf
        and (c4.get('upper') if isinstance(c4.get('upper'), dict) else {}).get('n_cells_removed') == 5 and f4 == ['SV_UNCHECKED'],
        f'σ {None if r4 is None else I_of(r4, QD2_N4)} ↔ {I4} · J1 꼴 비 {I4 / I4_j1} · {c4} · {f4}')
    # ⑤ 변이 J2 회로 — B 가 덮이지 않은 사이로 두 번 닿음 (지나지 않음)
    sid5, _r5, r5, c5 = _qd2_run([QD2_A5, QD2_B5], QD2_S5, QD2_N5)
    #  노드 — A0..A2 = 0..2 · Sa3..Sa5 (2,1,3..5) = 3..5 · A6..A8 = 6..8 · Sb3 (3,1,3) = 9 · Sb5 (3,1,5) = 10 · B0..B8 (4,1,0..8) = 11..19
    E5 = ([(0, 1, G_AX), (1, 2, G_AX), (2, 3, gsv), (3, 4, gss), (4, 5, gss), (5, 6, gsv), (6, 7, G_AX), (7, 8, G_AX)]
          + [(3, 9, gss), (5, 10, gss), (9, 14, gsv), (10, 16, gsv)] + [(11 + i, 12 + i, G_AX) for i in range(8)])
    bot5, top5 = [(0, G_PL), (11, G_PL)], [(8, G_PL), (19, G_PL)]
    I5 = _qd2_ref_I(20, E5, bot5, top5)
    I5_cut = _qd2_ref_I(20, [e for e in E5 if e[:2] not in ((9, 14), (10, 16))], bot5, top5)
    w5 = I5 / I5_cut
    chk('QD2 ⑤ 변이 J2 회로 (A 는 덩어리를 지남 · B 는 덮이지 않은 사이 셀 (4,1,4) 을 두고 두 번 닿음 = 지나지 않음) — σ = 손 회로 (1e-12) · '
        '못 가른 덩어리 0 · B 의 SV 면 둘을 끊음 · 비 = 손 I_full/I_cut (1e-10 · > 1) · 다시 풀지 않음 (위 = 아래 · 위 끝 기록 None) · J2 (사이 셀이 '
        '덮였는지 · 같은 성분인지 안 봄) 이면 B 도 지남 → 못 가른 덩어리 1 · 끊은 면 0',
        r5 is not None and int(sid5[4, 1, 4]) == 3 and rel(I_of(r5, QD2_N5), I5) < 1e-12
        and c5.get('n_unsplit_bridging_components') == 0 and c5.get('n_bridging_components') == 1 and c5.get('n_sv_faces_cut') == 2
        and c5.get('status') == 'computed' and rel(float(c5.get('sv_counterfactual_ratio') or math.nan), w5) < 1e-10 and w5 > 1.0 + 1e-9
        and 'upper' in c5 and c5.get('upper') is None and c5.get('status_hi') == 'computed'
        and c5.get('sv_counterfactual_ratio_hi') == c5.get('sv_counterfactual_ratio'),
        f'σ {None if r5 is None else I_of(r5, QD2_N5)} ↔ {I5} · 손 비 {w5} · {c5}')
    # ⑥ 덩어리 0 인 회로 (QD ③ SVY) — 기록의 옛 칸은 그대로 · 새 칸 = 위 끝 = 아래 끝 · 값 봉인 (위 끝만 따로 풀지 않음)
    P6 = cat_rows(rows(SVY), rows([[(1.5, 1.5, 3.5)]], phase=5, kind=0, fid0=700))
    sid6, _ = bed(P6, SVY_N)
    reg6 = _try(lambda: registry(sid6, P6, tol_sj_um=0.1, r_sdcp_um=0.5), None)
    n_before = _CG_CALLS[0]
    r6 = _try(lambda: solve(sid6, sig_e(), SVY_N, plan(reg6, 1e3, sv_counterfactual={'threshold': None})), None) if reg6 is not None else None
    n_solves6 = _CG_CALLS[0] - n_before
    c6 = (((r6 or {}).get('cjunc') or {}).get('sv_counterfactual') or {})
    chk('QD2 ⑥ 못 가른 덩어리 0 (QD ③ SVY) — 솔브 두 번 (주 + 아래 끝 · 위 끝을 따로 풀지 않음) · 위 끝 풀이 기록 None · 위 끝 상태 · 비 = 아래 끝 · '
        '괄호 규칙 칸',
        r6 is not None and c6.get('n_unsplit_bridging_components') == 0 and n_solves6 == 2 and 'upper' in c6 and c6.get('upper') is None
        and c6.get('status_hi') == c6.get('status') == 'computed' and c6.get('sv_counterfactual_ratio_hi') == c6.get('sv_counterfactual_ratio')
        and isinstance(c6.get('bracket_rule'), str) and bool(c6.get('bracket_rule')),
        f'솔브 {n_solves6} · {c6}')
    n_before = _CG_CALLS[0]
    _qd2_run([QD2_A3, QD2_B3, QD2_C3], QD2_S3, QD2_N3)
    n_solves3 = _CG_CALLS[0] - n_before
    chk('QD2 ⑦ 값 봉인 — 못 가른 덩어리가 있으면 아래 끝 값 (1 = 문턱 아래) 과 무관하게 위 끝도 푼다 (③ 꼴: 주 + 아래 끝 + 위 끝 = 솔브 3 · '
        '① 의 위 끝은 관통 없음 = 위상으로 끝 = 풀이 없이 +∞)',
        n_solves3 == 3, f'③ 꼴 솔브 {n_solves3}')
    # ⑧ 원장 census 변조 (지문 밖) — 위 끝은 지문 묶인 원장으로 다시 가른다 → 다르면 위 끝을 풀지 않는다 (fail-closed) · 검증기 거부
    def _tamper(reg):
        reg['census']['n_unsplit_bridging_components'] = 0
    _s8, _r8, r8, c8 = _qd2_run([QD2_A1, QD2_B1], QD2_S1, QD2_N1, reg_hook=_tamper)
    up8 = c8.get('upper') if isinstance(c8.get('upper'), dict) else {}
    ev8 = {'sv_counterfactual_request': {'threshold': None}, 'solve': {'sv_counterfactual': SVCF.sv_cf_record(c8)},
           'census': _qd2_census(r8)}
    p8 = _try(lambda: SVCF.sv_cf_problem(ev8, True), 'EXC')
    f8 = _try(lambda: _qd2_flags(c8, 2.0), None)
    chk('QD2 ⑧ 원장 census 의 못 가른 덩어리 수를 0 으로 변조 (지문 밖) — 위 끝 = 다시 가른 원장과 다름 → 풀지 않음 (위 끝 상태 = 비 없는 이름 · 사유) · '
        '검증기 거부 (덩어리 0 인데 위 끝 기록) · 사슬 = SV_UNCHECKED',
        r8 is not None and c8.get('n_unsplit_bridging_components') == 0 and bool(up8) and up8.get('sv_counterfactual_ratio') is None
        and up8.get('status') not in ('computed', 'no_through_without_sv') and bool(up8.get('why'))
        and isinstance(p8, str) and p8.startswith('sv_cf|') and f8 == ['SV_UNCHECKED'], f'{c8} · {p8} · {f8}')
    # ⑨ 주 해 미수렴 (`step3_sigma` 조기 기록) · 주 단자 전류 ≤ 0 (`sv_counterfactual` 첫 갈래) — 괄호 칸이 같은 꼴 (풀이 없음)
    from scipy.sparse.linalg import spsolve as _sps

    @contextlib.contextmanager
    def _unconv_solver():
        old = S3._solve_cg
        S3._solve_cg = lambda L, b, *a, **k: (_sps(L.tocsc(), b), 1)
        try:
            yield
        finally:
            S3._solve_cg = old
    P9 = cat_rows(rows([QD2_A1, QD2_B1]), rows([[p] for p in QD2_S1], phase=5, kind=0, fid0=700))
    sid9, _ = bed(P9, QD2_N1, sdcp_sphere_d_um=0.0)
    reg9 = registry(sid9, P9, tol_sj_um=0.1, r_sdcp_um=0.5)
    with _unconv_solver():
        r9 = _try(lambda: quiet(S3.solve_sigma_z, sid9, sig_e(), H, z_top_um=float(QD2_N1[2]), z_bot_um=0.0,
                                cjunc=plan(reg9, 1e3, sv_counterfactual={'threshold': None})), None)
    c9 = (((r9 or {}).get('cjunc') or {}).get('sv_counterfactual') or {})
    up9 = c9.get('upper') if isinstance(c9.get('upper'), dict) else {}
    ev9 = {'sv_counterfactual_request': {'threshold': None}, 'solve': {'sv_counterfactual': SVCF.sv_cf_record(c9)},
           'census': _qd2_census(r9)}
    chk('QD2 ⑨ 주 해 미수렴 (조기 기록 main_unconverged) — 옛 칸 그대로 (비 · 표지 · 증서 · backend None) + 못 가른 덩어리 1 · 위 끝 = 같은 상태 '
        '(풀이 없음) · 검증기 받음 · 사슬 = SV_UNCHECKED',
        r9 is not None and c9.get('status') == 'main_unconverged' and c9.get('sv_counterfactual_ratio') is None and c9.get('flag') is None
        and c9.get('conv_cert') is None and c9.get('backend_last_solve') is None and c9.get('n_unsplit_bridging_components') == 1
        and c9.get('status_hi') == 'main_unconverged' and c9.get('sv_counterfactual_ratio_hi') is None
        and up9.get('status') == 'main_unconverged' and _try(lambda: SVCF.sv_cf_problem(ev9, True), 'EXC') is None
        and _try(lambda: _qd2_flags(c9, 2.0), None) == ['SV_UNCHECKED'], f'{c9}')
    _orig_cf = CJ.CjuncAssembler.sv_counterfactual

    def _zero_I(self, solve_, I_full, request, **kw):
        return _orig_cf(self, solve_, 0.0, request, **kw)
    CJ.CjuncAssembler.sv_counterfactual = _zero_I
    try:
        _s10, _r10, r10, c10 = _qd2_run([QD2_A1, QD2_B1], QD2_S1, QD2_N1)
    finally:
        CJ.CjuncAssembler.sv_counterfactual = _orig_cf
    up10 = c10.get('upper') if isinstance(c10.get('upper'), dict) else {}
    chk('QD2 ⑩ 주 단자 전류 ≤ 0 (nonpositive_full_current — 풀지 않음) · 못 가른 덩어리 1 — 위 끝도 같은 상태 (풀이 없음) · 위 끝 비 None',
        r10 is not None and c10.get('status') == 'nonpositive_full_current' and c10.get('n_unsplit_bridging_components') == 1
        and c10.get('status_hi') == 'nonpositive_full_current' and c10.get('sv_counterfactual_ratio_hi') is None
        and up10.get('status') == 'nonpositive_full_current' and up10.get('cg_info') is None, f'{c10}')
    # ⑪ 덩어리가 판에 닿음 — 위 끝 = 그 셀의 판 결합까지 뺀다 (덩어리를 통째로 뺀 판 · 판 결합 1 · 면 9 = 손으로 센 수)
    sid11, _r11, r11, c11 = _qd2_run([QD2_A11, QD2_B11], QD2_S11, QD2_N11, cert=True)
    up11 = c11.get('upper') if isinstance(c11.get('upper'), dict) else {}
    #  손으로 센 면 (덩어리 셀 넷에 닿는 면): SDCP–SDCP (1,1,1)|(2,1,1) · (2,1,1)|(3,1,1) · (2,1,0)|(2,1,1) = 3 · SV (1,1,0)|(1,1,1) · (1,1,1)|(1,1,2) ·
    #  (3,1,0)|(3,1,1) · (3,1,1)|(3,1,2) · (1,1,0)|(2,1,0) · (2,1,0)|(3,1,0) = 6 → 9 · 판 결합 = (2,1,0) 아래 판 하나
    chk('QD2 ⑪ 못 가른 덩어리가 아래 판에 닿음 (A · B 판–판 · 덩어리 (1..3,1,1) + (2,1,0)) — 못 가른 덩어리 1 · 아래 끝 = 덩어리 그대로 (끊은 면 0 · '
        '비 1 정확) · 위 끝 = 셀 넷 · 면 9 · 판 결합 1 을 뺀 판 (A · B 둘 다 끊김 → 관통 없음 = +∞) · 사슬 = SV_UNCHECKED',
        r11 is not None and all(int(sid11[x, 1, 1]) == 5 for x in (1, 2, 3)) and int(sid11[2, 1, 0]) == 5
        and c11.get('n_unsplit_bridging_components') == 1 and c11.get('n_sv_faces_cut') == 0 and c11.get('sv_counterfactual_ratio') == 1.0
        and c11.get('status_hi') == 'no_through_without_sv' and c11.get('sv_counterfactual_ratio_hi') == math.inf
        and up11.get('n_cells_removed') == 4 and up11.get('n_edges_cut') == 9 and up11.get('n_plate_couplings_cut') == 1
        and _try(lambda: _qd2_flags(c11, 2.0), None) == ['SV_UNCHECKED'], f'{c11}')


# ═════════════════════════ ★ 10-23 QD3 — SV 문턱 = 증서 구간 판정 (Codex 재검토 RCA2-01 · 04 · 1저자 Q1 (가)) ═════════════════════════
def _qd3_run(polys, sdcp, n, rj=1e3, cert=True, solver=None):
    """괄호 회로 한 런 (증서 켬 기본) → (원장, 계획, 해, 반사실 원 기록) — 증거 fp 의 계획 행 지문을 계획에서 바로 읽으려고 계획을 돌려준다."""
    P = cat_rows(rows(polys), rows([[p] for p in sdcp], phase=5, kind=0, fid0=700))
    sid, _ = bed(P, n, sdcp_sphere_d_um=0.0)
    reg = registry(sid, P, tol_sj_um=0.1, r_sdcp_um=0.5)
    pl = plan(reg, rj, sv_counterfactual={'threshold': None})
    if cert:
        with cert_on(solver):
            r = quiet(S3.solve_sigma_z, sid, sig_e(), H, z_top_um=float(n[2]) * H, z_bot_um=0.0, cjunc=pl)
    else:
        r = solve(sid, sig_e(), n, pl)
    return reg, pl, r, (((r or {}).get('cjunc') or {}).get('sv_counterfactual') or {})


def _qd3_svx(cert=True, solver=None):
    """SVX (RCA06 픽스처 · 손 회로 `_svx_ref` · 비 ≈ 10.29) 반사실 한 런 → (원장, 계획, 해, 반사실 원 기록)."""
    P = cat_rows(rows(SVX), rows(SVX_SDCP, phase=5, kind=0, fid0=700))
    sid, _ = bed(P, SVX_N)
    reg = registry(sid, P, tol_sj_um=0.1, r_sdcp_um=0.5)
    pl = plan(reg, SVX_RJ, sv_counterfactual={'threshold': None})
    if cert:
        with cert_on(solver):
            r = quiet(S3.solve_sigma_z, sid, sig_e(), H, z_top_um=float(SVX_N[2]) * H, z_bot_um=0.0, cjunc=pl)
    else:
        r = solve(sid, sig_e(), SVX_N, pl)
    return reg, pl, r, (((r or {}).get('cjunc') or {}).get('sv_counterfactual') or {})


def _qd3_ev(reg, pl, r, cf):
    """실제 증거 꼴 (payload `ca_ext_cjunc.payload_blocks` · `ca_ext_svcf.attach_evidence` 와 같은 칸) — 요청 · 투영 · 솔브 기록 `I_bot_code` ·
    원장 census (JSON 정수) · fp (원장 sid · registry · 계획 행 지문)."""
    import ca_ext_svcf as SVCF
    return {'sv_counterfactual_request': {'threshold': None},
            'solve': {'sv_counterfactual': SVCF.sv_cf_record(cf), 'I_bot_code': ((r or {}).get('cjunc') or {}).get('I_bot_code')},
            'census': json.loads(json.dumps(reg['census'], default=int)),
            'fp': {'sid': reg['fp']['sid'], 'registry': reg['fp']['registry'], 'plan_rows': pl['fp_rows']}}


def _qd3_assess(view, thr):
    import rint_r_chain as _RRC
    return _RRC.sv_assess({('1', 'P1', 'R_j0'): {'sv_cf': view}}, thr, 'R_j0')


@case('QD3')
def t_sv_cert_interval():
    """★ 10-23 (Codex 재검토 RCA2-01 · 04 · 1저자 Q1 (가) · author 10-23 ratified Q1-Q8) — SV 문턱을 증서 구간으로 판정한다.
    판정문 반례 (`docs/reviews/codex_rint2_rereview_evidence_20261022/geometry/run_review.py` → `actual_certified_threshold_crossing`): 실제 SVX
    raster → 원장 → 계획 → 풀이 (첫 선형 해 벡터에만 +1e-8 · 나머지 직접해) → 증서 → 기록 → 검증기 → `sv_assess` 에서 nominal 비는 문턱 바로
    아래인데 증서가 보장하는 참 비 구간 전체가 문턱 위 → 옛 판 = 표지 없음.  고친 판 = 아래비 (Gfull_lo / Gcut_lower_hi) > 문턱 →
    SV_DEPENDENT · 위비 ≤ 문턱 → 표지 없음 · 그 밖 → SV_UNCHECKED · ∞ = 위상 증명 · 증서 없는 런 = 진단.  기대 = 손 회로 (모듈 밖)."""
    import ca_ext_svcf as SVCF
    from scipy.sparse.linalg import spsolve
    CERT = getattr(SVCF, 'STANDING_CERTIFIED', 'certified_interval')
    DIAG = getattr(SVCF, 'STANDING_DIAGNOSTIC', 'diagnostic_uncertified')
    I_full, _, _ = _svx_ref(SVX_RJ)
    I_cut, _, _ = _svx_ref(SVX_RJ, with_sv=False)
    true_r = I_full / I_cut
    # ① 판정문 실제 반례 꼴
    calls = [0]

    def _pert(L, b, *a, **k):
        calls[0] += 1
        phi = spsolve(L.tocsc(), b)
        return (phi + 1.0e-8 if calls[0] == 1 else phi), 0
    reg1, pl1, r1, c1 = _qd3_svx(cert=True, solver=_pert)
    p1 = SVCF.sv_cf_record(c1)
    v1 = SVCF.chain_view(p1)
    nom = c1.get('sv_counterfactual_ratio')
    thr = 0.5 * (nom + true_r) if isinstance(nom, float) else math.nan
    lo1, hi1 = v1.get('ratio_cert_lo'), v1.get('ratio_cert_hi')
    f1, _d1 = _qd3_assess(v1, thr)
    pr1 = _try(lambda: SVCF.sv_cf_problem(_qd3_ev(reg1, pl1, r1, c1), True), 'EXC')
    mc1, lc1 = (r1 or {}).get('conv_cert') or {}, c1.get('conv_cert') or {}
    print(f'    QD3 ① nominal {nom!r} · 문턱 {thr!r} · 증서 구간 [{lo1!r}, {hi1!r}] · 손 참 비 {true_r!r} · 풀이 {calls[0]}')
    chk('QD3 ① 판정문 실제 반례 꼴 (SVX · 첫 선형 해에만 +1e-8 · 증서 켬) — 주 해 · 아래 끝 증서 통과 · nominal < 문턱 < 증서 구간 아래비 ≤ 손 회로 '
        '참 비 ≤ 위비 · 사슬 = SV_DEPENDENT (옛 nominal 판정 = 표지 없음) · 실제 증거 꼴 검증기 받음 · 지위 증서 구간 · 판정 근거 칸 = 사슬 꼴 값',
        r1 is not None and calls[0] >= 2 and mc1.get('ok') is True and lc1.get('ok') is True and c1.get('standing') == CERT
        and isinstance(nom, float) and nom < thr and isinstance(lo1, float) and isinstance(hi1, float) and thr < lo1 <= true_r <= hi1
        and f1 == ['SV_DEPENDENT'] and pr1 is None and p1.get('ratio_cert_interval') == [lo1, hi1],
        f'표지 {f1} · 검증 {pr1!r} · 지위 {c1.get("standing")!r} · 판정 근거 칸 {p1.get("ratio_cert_interval")!r}')
    f1n, _ = _qd3_assess({'standing': CERT, 'ratio': nom, 'ratio_hi': nom, 'ratio_cert_lo': nom, 'ratio_cert_hi': nom}, thr)
    chk('QD3 ① 옛 판정 재현 — 두 끝에 nominal 을 두면 표지 없음 (반례 = nominal 판정의 결함 · 증서 구간이 판정을 바꾼다)', f1n == [], f1n)
    # ② 정확 풀이 (증서 켬)
    reg2, pl2, r2, c2 = _qd3_svx(cert=True)
    v2 = SVCF.chain_view(SVCF.sv_cf_record(c2))
    lo2, hi2 = v2.get('ratio_cert_lo'), v2.get('ratio_cert_hi')
    ok2 = isinstance(lo2, float) and isinstance(hi2, float) and lo2 <= true_r <= hi2
    fa = _qd3_assess(v2, lo2 * (1.0 - 1e-9))[0] if ok2 else None
    fb = _qd3_assess(v2, hi2 * (1.0 + 1e-9))[0] if ok2 else None
    pr2 = _try(lambda: SVCF.sv_cf_problem(_qd3_ev(reg2, pl2, r2, c2), True), 'EXC')
    chk('QD3 ② 정확 풀이 (증서 켬) — 증서 구간 ∋ 손 회로 참 비 · 문턱 = 아래비 × (1 − 1e-9) → SV_DEPENDENT · 위비 × (1 + 1e-9) → 표지 없음 · 검증기 받음',
        ok2 and fa == ['SV_DEPENDENT'] and fb == [] and pr2 is None, f'[{lo2!r}, {hi2!r}] ∋ {true_r!r}? · {fa} · {fb} · {pr2!r}')
    # ③ +∞ = 위상 증명 (QD2 ② 꼴 — 아래 끝 관통 없음)
    reg3, pl3, r3, c3 = _qd3_run([QD2_A1, QD2_B1C], QD2_S1, QD2_N1)
    p3 = SVCF.sv_cf_record(c3)
    v3 = SVCF.chain_view(p3)
    zc, mc3 = c3.get('conv_cert') or {}, (r3 or {}).get('conv_cert') or {}
    f3 = _qd3_assess(v3, 2.0)[0]
    pr3 = _try(lambda: SVCF.sv_cf_problem(_qd3_ev(reg3, pl3, r3, c3), True), 'EXC')
    chk('QD3 ③ +∞ = 위상이 증명한 0 분모 (QD2 ② 꼴 · 아래 끝 no_through_without_sv) — 그 끝 증서 = 영값 위상 (VALID_ZERO_TOPOLOGY · 조기 반환 · '
        '관통 dof 0 · 결합 칸 = 주 해 증서) · 증서 구간 [∞, ∞] (투영 = "inf") · 사슬 SV_DEPENDENT · 검증기 받음',
        c3.get('status') == 'no_through_without_sv' and zc.get('status') == 'VALID_ZERO_TOPOLOGY' and zc.get('zero_source') == 'early_return'
        and zc.get('n_through_dof') == 0 and all(zc.get(k) == mc3.get(k) for k in ('fp_sid', 'fp_sig', 'fp_cjunc_registry', 'fp_cjunc_rows'))
        and v3.get('ratio_cert_lo') == math.inf and v3.get('ratio_cert_hi') == math.inf and p3.get('ratio_cert_interval') == ['inf', 'inf']
        and f3 == ['SV_DEPENDENT'] and pr3 is None, f'{zc} · {v3} · {f3} · {pr3!r}')
    # ④ 증서 없는 런 = 진단
    reg4, pl4, r4, c4 = _qd3_svx(cert=False)
    p4 = SVCF.sv_cf_record(c4)
    f4, d4 = _qd3_assess(SVCF.chain_view(p4), 2.0)
    pr4 = _try(lambda: SVCF.sv_cf_problem(_qd3_ev(reg4, pl4, r4, c4), True), 'EXC')
    chk('QD3 ④ 증서 없는 런 (rtol 노브 없음) = 진단 기록 — 지위 diagnostic_uncertified · 주 해 · 끝 증서 없음 · 증서 구간 [None, None] · nominal 비 > 문턱 2 '
        '인데 사슬 = SV_UNCHECKED (판정 입력 아님 · 세부 uncertified · 옛 = SV_DEPENDENT) · 검증기 받음',
        c4.get('standing') == DIAG and c4.get('conv_cert_full') is None and c4.get('conv_cert') is None
        and p4.get('ratio_cert_interval') == [None, None] and isinstance(c4.get('sv_counterfactual_ratio'), float)
        and c4['sv_counterfactual_ratio'] > 2.0 and f4 == ['SV_UNCHECKED'] and d4.get('uncertified') == ['c1_P1_R_j0'] and pr4 is None,
        f'{c4.get("standing")!r} · {p4.get("ratio_cert_interval")!r} · {f4} · {d4.get("uncertified")} · {pr4!r}')
    # ⑤ 괄호 회로 (QD2 ③ · 못 가른 덩어리 1 · 두 끝 computed) — 증서 구간 ∋ 손 회로 참값
    I3_, I3t, I3h = _qd2_ref3()
    t5, h5 = I3_ / I3t, I3_ / I3h
    reg5, pl5, r5, c5 = _qd3_run([QD2_A3, QD2_B3, QD2_C3], QD2_S3, QD2_N3)
    v5 = SVCF.chain_view(SVCF.sv_cf_record(c5))
    lo5, hi5 = v5.get('ratio_cert_lo'), v5.get('ratio_cert_hi')
    ev5 = _qd3_ev(reg5, pl5, r5, c5)
    pr5 = _try(lambda: SVCF.sv_cf_problem(ev5, True), 'EXC')
    chk('QD3 ⑤ 괄호 회로 (QD2 ③ · 못 가른 덩어리 1 · 증서 켬) — 아래비 ≤ 아래 끝 손 참값 1 · 손 참 비 (다리만 끊음) ∈ [아래비, 위비] · 위 끝 손 참값 ≤ 위비 · '
        '검증기 받음',
        isinstance(lo5, float) and isinstance(hi5, float) and lo5 <= 1.0 and lo5 <= t5 <= hi5 and h5 <= hi5 and pr5 is None,
        f'[{lo5!r}, {hi5!r}] · 참 {t5!r} · 위 끝 {h5!r} · {pr5!r}')
    # ⑥ 한 끝 실패 — 위 끝 증서 실패 (세 번째 증서 = 위 끝 풀이) → 위 끝 미수렴 · 위비 못 정함
    cc_mod = sys.modules.get('step3_conv_cert') or importlib.import_module('step3_conv_cert')
    real_cert, n_cert = cc_mod.certify, [0]

    def _fail_third(*a, **k):
        n_cert[0] += 1
        out = real_cert(*a, **k)
        return dict(out, pass_c=False, ok=False) if n_cert[0] == 3 else out
    cc_mod.certify = _fail_third
    try:
        reg6, pl6, r6, c6 = _qd3_run([QD2_A3, QD2_B3, QD2_C3], QD2_S3, QD2_N3)
    finally:
        cc_mod.certify = real_cert
    v6 = SVCF.chain_view(SVCF.sv_cf_record(c6))
    lo6 = v6.get('ratio_cert_lo')
    f6a, d6a = _qd3_assess(v6, 1.5)
    f6b = _qd3_assess(v6, 0.5)[0]
    pr6 = _try(lambda: SVCF.sv_cf_problem(_qd3_ev(reg6, pl6, r6, c6), True), 'EXC')
    chk('QD3 ⑥ 한 끝 실패 (위 끝 풀이 증서 실패) — 위 끝 상태 unconverged · 위비 None · 문턱 1.5 (≥ 아래비) → SV_UNCHECKED (못 읽음) · 문턱 0.5 '
        '(< 아래비) → SV_DEPENDENT (아래만으로) · 검증기 받음 (구조화 상태)',
        n_cert[0] == 3 and c6.get('status_hi') == 'unconverged' and isinstance(lo6, float) and v6.get('ratio_cert_hi') is None
        and f6a == ['SV_UNCHECKED'] and d6a.get('unreadable') == ['c1_P1_R_j0'] and f6b == ['SV_DEPENDENT'] and pr6 is None,
        f'증서 {n_cert[0]} · {c6.get("status_hi")!r} · {v6} · {f6a} · {f6b} · {pr6!r}')
    # ⑦ 실제 기록 (⑤) 변이 — 실제 소비자가 부르는 검증기 (`ca_ext_svcf.sv_cf_problem`) 가 자기 문장으로 거부
    foreign = (SVCF.sv_cf_record(c1) or {}).get('conv_cert')         # 다른 실제 회로 (SVX) 의 통과 증서

    def _mut(fn):
        ev = json.loads(json.dumps(ev5))
        fn(ev, ev['solve']['sv_counterfactual'])
        return _try(lambda: SVCF.sv_cf_problem(ev, True), 'EXC'), ev
    muts = {
        '아래 끝 증서 없음 (증서 구간 기록)': lambda e, s: s.update(conv_cert=None),
        '위 끝 증서 없음': lambda e, s: s['upper'].update(conv_cert=None),
        '주 해 증서 없음 (분자 G_full 을 묶을 증서)': lambda e, s: s.update(conv_cert_full=None),
        '외부 증서 — 다른 실제 회로 (SVX) 의 통과 증서를 위 끝에': lambda e, s: s['upper'].update(conv_cert=dict(foreign or {})),
        '외부 증서 — 게시 판 전류만 그 끝 G 로 고침 (목표량 구간 · 결합 칸 = 다른 회로)':
            lambda e, s: s['upper'].update(conv_cert=dict(foreign or {}, I_bot=s['upper'].get('G_cut_code'))),
        '임의 괄호 규칙': lambda e, s: s.update(bracket_rule='not-the-registered-rule'),
        '제거 성분 수 0 (못 가른 덩어리 1)': lambda e, s: s['upper'].update(n_components_removed=0),
        '제거 셀 수 0 (< 성분 수)': lambda e, s: s['upper'].update(n_cells_removed=0),
        '못 가른 덩어리 수 10**400': lambda e, s: s.update(n_unsplit_bridging_components=10 ** 400),
        '실제 census 와 다름 (census 못 가른 덩어리 0)': lambda e, s: e['census'].update(n_unsplit_bridging_components=0),
        'I_bot_code ≠ G_full': lambda e, s: e['solve'].update(I_bot_code=2.0 * s['G_full_code']),
        '증거 fp sid = 다른 런': lambda e, s: e['fp'].update(sid='f' * 32),
        '판정 근거 칸 변조': lambda e, s: s.update(ratio_cert_interval=[9.0, 9.0]),
        '지위 칸 없음 (옛 기록)': lambda e, s: s.pop('standing'),
        '지위 = 진단 인데 증서가 실려 있다': lambda e, s: s.update(standing=DIAG),
        '아래 끝 증서 옛 판': lambda e, s: s['conv_cert'].update(version='conv-cert-v1'),
        '아래 끝 증서 ⓓ 거짓 (ok True 그대로)': lambda e, s: s['conv_cert'].update(pass_d=False),
    }
    chk('QD3 ⑦ 변이 전 기록 (⑤ 실제 증거 꼴) = 검증기 받음', pr5 is None, pr5)
    for nm, fn in muts.items():
        why, _e = _mut(fn)
        chk(f'QD3 ⑦ 실제 기록 변이 거부 [{nm}] — 검증기 자신의 문장 (sv_cf| · 예외 아님)', isinstance(why, str) and why.startswith('sv_cf|'),
            why)

    def _diag(e, s):
        s.update(standing=DIAG, conv_cert_full=None, conv_cert=None, ratio_cert_interval=[None, None])
        s['upper']['conv_cert'] = None
    why_d, ev_d = _mut(_diag)
    fd, dd = _qd3_assess(SVCF.chain_view(ev_d['solve']['sv_counterfactual']), 1.5)
    chk('QD3 ⑦ 같은 기록을 진단 (지위 진단 · 증서 전부 없음 · 판정 근거 칸 [None, None]) 으로 = 검증기 받음 · 사슬 = SV_UNCHECKED (uncertified · 판정 '
        '입력 아님)',
        why_d is None and fd == ['SV_UNCHECKED'] and dd.get('uncertified') == ['c1_P1_R_j0'], f'{why_d!r} · {fd} · {dd.get("uncertified")}')


@case('KBND')
def t_k_boundary():
    """PRE-impl-05 (P3 · 한계 기록 · 고치지 않음) — 분산판 v0 간선 수 k = ceil(L_c/L_par) 의 경계 (깊은 교차 90° → 89.99° · k 1 → 2 · 배율 차
    1.5e-8) 에서 σ 가 뛴다 (반쪽 간선이 셀 경계로 가 사전식 최소 셀로 옮겨진다 — 크기 ∝ h·r′/R_j).  생산 단위 (h 0.15 · r_f 0.075 · L_par 0.30
    · σ_VGCF 7853.98) R_j 1e2 · 1e4 · 1e6 Ω 의 뜀 = 사전 리뷰 탐침 값 (−0.978 % · −2.10e-4 · −2.11e-6) ± 10 % 로 묶는다 · ∝ 1/R_j ·
    같은 sid.  ⚠ 이 시험은 맞는 값이 아니라 이산화 오차 크기의 기록이다 (바뀌면 알린다 · `carbon_junction._n_sub` 주석)."""
    VP, NK = 0.15, (9, 3, 10)
    want = {1e2: -0.009782110461166504, 1e4: -0.000209786930659428, 1e6: -2.1066342607012345e-06}

    def run(th, rj):
        t = math.radians(th)
        C = np.array([3.5, 1.5, 3.5]) * VP
        u = np.array([math.sin(t), 0.0, math.cos(t)])
        b0, b1 = C - 3.0 * VP * u, C + 3.0 * VP * u
        A = [(3.5 * VP, 1.5 * VP, 0.5 * VP), (3.5 * VP, 1.5 * VP, 5.5 * VP)]
        B = [tuple(b0), tuple(b1), (b1[0], 1.5 * VP, 9.5 * VP)]
        P = rows([A, B], step=0.05)
        sid, _ = bed(P, NK, vox=VP)
        reg = registry(sid, P, vox=VP, r_f_um=0.075, tol_ff_um=0.03, L_par_um=0.30, r_port_um=0.30, s_min_um=3.0)
        r = solve(sid, sig_e(s_vgcf=7853.98, s_am=0.0041), NK, plan(reg, rj), vox=VP)
        return int(np.asarray(reg['instances']['nsub'])[0]), float(r['sigma_eff']), sid.tobytes()
    jumps, ok = {}, True
    for rj in (1e2, 1e4, 1e6):
        k0, s0, h0 = _try(lambda rj=rj: run(90.0, rj), (None, math.nan, b''))
        k1, s1, h1 = _try(lambda rj=rj: run(89.99, rj), (None, math.nan, b''))
        j = s1 / s0 - 1.0 if s0 == s0 and s0 != 0.0 else math.nan
        jumps[rj] = (k0, k1, j)
        ok &= bool(k0 == 1 and k1 == 2 and h0 == h1 and h0 != b'' and abs(j - want[rj]) <= 0.1 * abs(want[rj]))
    chk('KBND k 경계 σ 뜀 (90° → 89.99° · k 1 → 2 · 같은 sid) = 사전 리뷰 값 ± 10 % (R_j 1e2 · 1e4 · 1e6 Ω · 생산 단위)', ok, f'{jumps}')
    r42 = jumps[1e4][2] / jumps[1e2][2] if jumps[1e2][2] else math.nan
    r64 = jumps[1e6][2] / jumps[1e4][2] if jumps[1e4][2] else math.nan
    chk('KBND 크기 ∝ 1/R_j (큰 R_j 에서) — 뜀(1e6)/뜀(1e4) ∈ [0.009, 0.011] · 뜀(1e4)/뜀(1e2) ∈ [0.015, 0.03]',
        0.009 <= r64 <= 0.011 and 0.015 <= r42 <= 0.03, f'{r64} · {r42}')


@case('MUT-RCA2')
def t_mut_rca2():
    """새 보장의 판별력 (10-21 · PRE-impl 01 · 03 · 04 · 06) — 모듈 훅을 바꿔 끼운 변이가 위 시험 (손 회로) 에 옳은 이유로 걸려야 한다 ·
    변이 전 통과 (예외 없이) · 변이 뒤 같은 검사 실패 · 변이 안 예외 (`_try` 가 삼킨 것 포함) = 하네스 실패 (PRE-impl-09 규칙)."""
    rj = 1e3

    @contextlib.contextmanager
    def patched(name, fn):
        if not hasattr(CJ, name):
            raise AttributeError(f'변이 훅 {name} 없음')
        old = getattr(CJ, name)
        setattr(CJ, name, fn)
        try:
            yield
        finally:
            setattr(CJ, name, old)

    def gap_ok():
        P = rows_pieces([densify([(1.5, 1.5, 0.5), (1.5, 1.5, 3.15)]), densify([(1.5, 1.5, 3.85), (1.5, 1.5, 7.5)])])
        sid, _ = bed(P, GAP_N)
        I = _try(lambda: I_of(solve(sid, sig_e(), GAP_N, plan(registry(sid, P), rj)), GAP_N))
        return rel(I, chain_I([G_PL] + [G_AX] * 3 + [1e4 / rj] + [G_AX] * 4 + [G_PL])) < 1e-12

    def qc_ok():
        P = cat_rows(rows(F2), rows([[(1.5, 1.5, 3.5)]], phase=5, kind=0, fid0=700))
        sid, _ = bed(P, F2_N)
        gsv = 2.0 * SV * 250.0 / (SV + 250.0) * H
        E = [(0, 1, G_AX), (1, 2, G_AX), (2, 3, gsv), (3, 4, gsv)] + [(4 + i, 5 + i, G_AX) for i in range(4)]
        I = _try(lambda: I_of(solve(sid, sig_e(), F2_N, plan(registry(sid, P, tol_sj_um=0.1, r_sdcp_um=0.5), rj,
                                                            ptfe_stamp='face_alpha')), F2_N))
        return rel(I, ref_I(9, E, [(0, G_PL)], [(8, G_PL)])) < 1e-12

    def qd_ok():
        n1 = (3, 3, 8)
        P = cat_rows(rows([[(1.5, 1.5, 0.5), (1.5, 1.5, 7.5)]]), rows([[(1.5, 1.5, 3.5)]], phase=5, kind=0, fid0=700))
        sid, _ = bed(P, n1)
        r = _try(lambda: solve(sid, sig_e(), n1, plan(registry(sid, P, tol_sj_um=0.1, r_sdcp_um=0.5), rj,
                                                    sv_counterfactual={'threshold': None})), None)
        return (((r or {}).get('cjunc') or {}).get('sv_counterfactual') or {}).get('sv_counterfactual_ratio') == 1.0

    def ring_ok():
        sid, _ = bed(rows([RING]), RING_N)
        I = _try(lambda: I_of(solve(sid, sig_e(), RING_N, plan(registry(sid, rows([RING])), rj)), RING_N))
        return rel(I, _graph_ref(_cells_of_pts(densify(RING)), RING_N)) < 1e-12

    def floor_ok():
        out = _try(lambda: _floor_case(FL_L, None), None)
        return out is not None and out[0]['census'].get('n_self_candidates') == 0 and not out[1]

    def live_only(piece, pos, piece_pos):
        a0, a1 = piece_pos[piece]
        c = np.arange(a0, a1)
        return c[pos['live'][c]]

    def j1_rows(info):                                      # ★ 10-22 (2 회차 변이 J1) — 못 가른 다리 (지나는 무리 ≥ 2) 지킴 줄을 뺀 `_sv_cut_rows`
        comp, grp, pas = info['comp'], info['group'], info['passing']
        cut = np.zeros(len(comp), bool)
        for c_ in np.unique(comp):
            m_ = comp == c_
            if len(np.unique(grp[m_])) <= 1:
                continue
            cut |= m_ & ~pas
        return cut
    cases = (
        ('조각 = fid 규칙 (옛 · 같은 fid 조각 쌍을 서로 다른 섬유 규칙에서 뺌) → GAP 같은 셀 σ 0', '_distinct_keep',
         lambda segs, i, j: segs['fid'][i] != segs['fid'][j], gap_ok),
        ('포트 = 살아 있는 위치만 (옛 · 덮이면 r_port 안 이웃 셀로 옮김) → QC ① 옮긴 접합 + SV 병렬', '_piece_cand', live_only, qc_ok),
        ('반사실 = SV 면 전부 끊음 (옛) → QD ① SDCP 를 지나는 섬유 하나도 비 ∞', '_sv_cut_rows',
         lambda info: np.ones(len(info['comp']), bool), qd_ok),
        ('★ 10-22 못 가른 다리 지킴 끔 (2 회차 변이 J1) → QD2 ④ 아래 끝이 닿기만 하는 C 의 SV 면을 끊음 (덩어리 그대로가 아님)', '_sv_cut_rows',
         j1_rows, _qd2_j1_ok),
        ('★ 10-22 \'지남\' 에 덮임 · 같은 성분 조건 뺌 (2 회차 변이 J2) → QD2 ⑤ 덮이지 않은 사이로 두 번 닿는 B 도 \'지남\' (못 가른 덩어리 1 · '
         'B 를 안 끊음)', '_sv_passes', lambda btw, pos, labf, c_: bool(len(btw) and np.all(pos['lin'][btw] >= 0)), _qd2_j2_ok),
        ('고리 이음매 별칭 끔 → 이음매 첫 · 끝 위치가 따로 (고리가 끊긴다)', '_ring_alias', lambda cu, is_ring: False, ring_ok),
        ('바닥 = s > D 만 ((π/2)·d 없음) → L 자 90° 모서리가 자기 후보', '_self_floor', lambda s_, d_, D_: s_ > D_, floor_ok),
    )
    for nm, name, fn, check in cases:
        _TRY_EXC[0] = 0
        b = bool(check())
        e0 = _TRY_EXC[0]
        c, why = None, ''
        try:
            with patched(name, fn):
                _TRY_EXC[0] = 0
                c = not bool(check())
                if _TRY_EXC[0]:
                    c, why = None, f'변이 안 예외 {_TRY_EXC[0]} 건 = 하네스 실패'
        except Exception as e:                              # noqa: BLE001 — 훅 없음 (고치기 전) · 변이 예외 = 하네스 실패
            c, why = None, f'{type(e).__name__}: {e}'
        if why:
            print(f'    MUT-RCA2 {nm}: {why}')
        chk(f'MUT-RCA2 {nm} (훅 `{name}` · 변이 전 통과 · 변이 실패 · 예외 없음)', b and e0 == 0 and c is True,
            f'base {b} (예외 {e0}) caught {c} {why}')


FL_N = (6, 3, 8)
FL_L = [[(1.5, 1.5, 0.5), (1.5, 1.5, 4.5), (4.5, 1.5, 4.5)]]            # 90° 모서리 하나
FL_V = [[(1.5, 1.5, 0.5), (1.5, 1.5, 6.5), (2.3, 1.5, 0.5)]]            # 날카로운 V (꼭짓각 7.6° · 두 팔이 D 안)


def _floor_case(poly, smin):
    P = rows(poly)
    sid, _ = bed(P, FL_N)
    reg = registry(sid, P, s_min_um=smin)
    I = reg['instances']
    return reg, [(float(I['s'][q]), float(I['d0'][q])) for q in range(len(I['fi'])) if I['self'][q]]


@case('FLOOR')
def t_self_floor():
    """★ 10-21 (사전 리뷰 PRE-impl-02 · 1저자 Q-B) — 같은 조각 쌍의 바닥 = s > D 그리고 s > (π/2)·d: 곧은 이웃 (s = d) · 꺾임 모서리
    (꼭짓각 θ ≥ 79° 이면 s/d ≤ 1/sin(θ/2) ≤ π/2) 는 어떤 s_min 에서도 접합 후보가 아니다 · 반원 굽힘 (s = (π/2)·d) 이 경계.
    s_min 없음 (S0 census) · s_min 0 에서도 L 자 = 후보 0 · V 자 (꼭짓각 7.6°) = 후보 ≥ 1 · 모든 자기 instance s > D · s > (π/2)·d0."""
    D_ = 2.0 * RF + TOL
    for nm, poly, smin, want0 in (('L 자 · s_min 없음', FL_L, None, True), ('L 자 · s_min 0', FL_L, 0.0, True),
                                 ('V 자 · s_min 없음', FL_V, None, False), ('V 자 · s_min 0', FL_V, 0.0, False)):
        out = _try(lambda poly=poly, smin=smin: _floor_case(poly, smin), None)
        reg, sv = out if out is not None else (None, [])
        c = (reg or {}).get('census') or {}
        if want0:
            ok = reg is not None and len(sv) == 0 and c.get('n_self_candidates') == 0
        else:
            ok = reg is not None and len(sv) >= 1 and all(s_ > D_ and s_ > 0.5 * math.pi * d_ for s_, d_ in sv)
        chk(f'FLOOR {nm} — ' + ('자기 후보 0 · instance 0 (90° 모서리 = 바닥 안)' if want0 else
                                '자기 instance ≥ 1 · 모두 s > D · s > (π/2)·d0'), ok, f'{sv} · 후보 {c.get("n_self_candidates")}')


# ═════════════════════════ FP — 지문 재현 (RINT-23 · 같은 꼴 확인 · 2 일 차) ═════════════════════════
#  계약: 같은 내용 · 다른 객체 → 같은 지문 · 별도 `python3 -I` 하위 프로세스 둘 → 같은 지문 · 내용 한 글자 다름 → 다른 지문.
#  RINT-23 — `_fp` 가 dtype=object 배열의 **포인터 바이트** (`x.data`) 를 해시했다.  원장 `instances['reason']` (포트 미실현 사유 ·
#  f-문자열 = 호출마다 새 객체) 이 그 배열이라, 같은 입력으로 다시 만든 원장 · 계획 지문이 프로세스 안에서도 사이에서도 갈렸다 (거짓 거부).
#  픽스처 = F1 + 교차 셀 (1,1,3) 을 덮는 SDCP 점 (r_port 0.5 → 포트 미실현 'covered_SDCP') + z = 3 면 위 PTFE (S1 VGCF|SDCP 면 α < 1).
_FP_SDCP = [[(1.5, 1.5, 3.5)]]
_FP_PTFE = [[(0.5, 1.5, 3.0), (2.5, 1.5, 3.0)]]
_FP_RPORT = 0.5
_FP_WORDS = ('covered_SDCP', '', 'out_of_box', '탄소 접합 · 포트 (UTF-8)', 'no_live_port_in_rport')

#  하위 프로세스 · 이 프로세스가 **같은 글** 을 돌린다 (지문을 만드는 경로 하나 — 기대값을 이 파일이 따로 만들지 않는다).
_FP_PROG = r'''
def fp_values(cfg):
    import hashlib
    import numpy as np
    import step3_sigma as S3
    import carbon_junction as CJ
    import ptfe_face_alpha as FA
    import ca_s0_census as S0
    z = np.load(cfg['npz'])
    P, PH, F, K = z['P'], z['PH'], z['F'], z['K']
    n = tuple(int(x) for x in z['n'])
    vox = float(z['vox'])
    lo = (0.0, 0.0, 0.0)
    hi = tuple(n[i] * vox for i in range(3))
    m = PH != 4                                                # face_alpha 침대 = PTFE 셀 없음 (off 격자)
    sid, pid = S3.rasterize(np.zeros((0, 3)), np.zeros(0), np.zeros(0, np.int64), P[m], PH[m], lo, hi, vox,
                            add_fid=F[m], add_kind=K[m])
    reg = CJ.cjunc_registry(sid, lo, vox, P, PH, F, K, **cfg['thr'])
    pl = CJ.cjunc_plan(reg, 1.0e3, unreg_law='cut', ptfe_stamp='off')
    obj = np.empty(len(cfg['words']), dtype=object)
    for i, w in enumerate(cfg['words']):
        obj[i] = ''.join(list(w))                              # 실행 중 만든 문자열 (상수 · 인턴 객체 아님)
    m4 = PH == 4
    caps = FA.build_capsules(P[m4], F[m4], K[m4])
    sig = S3.electronic_sigma_table(0.010, 0.005, 100.0, 10.0, 250.0)
    fa = FA.build_plan(sid, sig, caps, lo=lo, vox=vox, channel='electronic', pid=pid)
    used = tuple({'lin': fa['axes'][a]['lin'], 'alpha': fa['axes'][a]['alpha'], 'g': fa['axes'][a]['alpha'] * 2.0}
                 for a in range(3))
    plan0, pbytes, psha = S0.make_plan(0.15, 0.075, 2.0, {'stage': 1, 'kit_name': ''.join(['kit', '_fp'])})
    return {'cj_objarr': CJ._fp(obj), 'cj_reg_sid': reg['fp']['sid'], 'cj_reg_centreline': reg['fp']['centreline'],
            'cj_reg_membership': reg['fp']['membership'], 'cj_reg_registry': reg['fp']['registry'],
            'cj_plan_rows': pl['fp_rows'], 'cj_plan_record_registry': pl['record']['fp_registry'],
            'fa_caps': caps['fp'], 'fa_rows': fa['fp_rows'], 'fa_plan': fa['fp_plan'], 'fa_edges': FA.edges_fp(used),
            'fa_grid_sid': FA._grid_fp(sid), 'fa_grid_pid': FA._grid_fp(pid),
            's0_plan_sha': psha, 's0_plan_bytes_sha': hashlib.sha256(S0.plan_bytes_of(plan0)).hexdigest(),
            's0_file_sha': S0._sha256_file(cfg['npz'])}
'''
_FP_CHILD_MAIN = r'''
import json, sys
cfg = json.loads(sys.argv[1])
for p in cfg['paths']:
    if p not in sys.path:
        sys.path.insert(0, p)
_junk = [str(i) * 7 for i in range(int(cfg['junk']))]        # 힙 배치를 바꾼다 (ASLR 이 꺼진 기계에서도 객체 주소가 갈리게)
g = {}
exec(compile(cfg['prog'], '<fp-prog>', 'exec'), g)
print('FPJSON ' + json.dumps(g['fp_values'](cfg), sort_keys=True))
'''


def _rt(s):
    """실행 중 새로 만든 같은 내용 문자열 — 두 글자 이상이면 다른 객체 (CPython 은 '' · 한 글자만 공유한다)."""
    return ''.join(list(s))


def _objarr(items):
    a = np.empty(len(items), dtype=object)
    for i, v in enumerate(items):
        a[i] = v
    return a


def _fp_numeric_formula(x):
    """숫자 배열 지문의 **독립** 식 (모듈 밖) — blake2b-16 (dtype.str · repr(모양) · C 순서 바이트)."""
    c = np.ascontiguousarray(x)
    h = hashlib.blake2b(digest_size=16)
    h.update(c.dtype.str.encode()); h.update(repr(c.shape).encode()); h.update(c.tobytes(order='C'))
    return h.hexdigest()


def _fp_fixture():
    P = cat_rows(rows(F1), rows(_FP_SDCP, phase=5, kind=0, fid0=700), _ptfe_rows(_FP_PTFE))
    sid, pid = bed(P, F1_N, stamp=P[1] != 4)
    return P, sid, pid


def _fp_thr():
    return dict(r_f_um=RF, tol_ff_um=TOL, L_par_um=LPAR, r_port_um=_FP_RPORT, gap_tol=2.0, s_min_um=S_MIN)


def _fp_children(tmpd, P):
    """같은 글 (`_FP_PROG`) 을 별도 `python3 -I` 하위 프로세스 둘 (힙 선할당 0 · 20000) 과 이 프로세스에서 돌린다 → (자식 둘, 이 프로세스)."""
    npz = os.path.join(tmpd, 'fp_fixture.npz')
    np.savez(npz, P=P[0], PH=P[1], F=P[2], K=P[3], n=np.array(F1_N), vox=np.float64(H))
    paths = [SCRIPTS]
    for mod in (np, __import__('scipy')):                 # 사용자 site 의 numpy 도 -I 에서 찾게 (명시 경로 · 암묵 경로 없음)
        d = os.path.dirname(os.path.dirname(os.path.abspath(mod.__file__)))
        if d not in paths:
            paths.append(d)
    thr = reg_kw(_fp_thr())
    cfg = {'paths': paths, 'npz': npz, 'thr': thr, 'words': list(_FP_WORDS), 'prog': _FP_PROG}
    kids = []
    for junk in (0, 20000):
        c = dict(cfg, junk=junk)
        r = subprocess.run([sys.executable, '-I', '-c', _FP_CHILD_MAIN, json.dumps(c)], capture_output=True, text=True,
                           timeout=600)
        line = [x for x in r.stdout.splitlines() if x.startswith('FPJSON ')]
        if r.returncode != 0 or not line:
            print(f'    FP 하위 프로세스 (junk {junk}) rc {r.returncode}: {(r.stderr or r.stdout)[-400:]}')
            kids.append(None)
        else:
            kids.append(json.loads(line[-1][len('FPJSON '):]))
    g = {}
    exec(compile(_FP_PROG, '<fp-prog>', 'exec'), g)
    here = quiet(g['fp_values'], dict(cfg, junk=0))
    return kids, here


#: 지문 · 해시 함수 목록 (AST — 본문이 `hashlib` 을 쓰는 함수) — 이 표 밖의 함수가 생기면 FP 시험이 그것을 덮지 못한다 → 실패.
FP_INVENTORY = {
    'carbon_junction': {'_fp': 'FP-a…h · FP-i (원장 · 계획 · 객체 배열)'},
    'ptfe_face_alpha': {'_h16': 'FP-i · FP-k (캡슐 · 행 · 계획 · 간선 지문 — 고정 dtype 바이트 · 문자열)',
                        '_path_radius': '두 집단 지름 분류 해시 (점열 float64 바이트 · F-DIA 순열 불변) — 지문 아님'},
    'ca_s0_census': {'_sha256_file': 'FP-i · FP-l', 'make_plan': 'FP-i · FP-l (정준 JSON 바이트)',
                     'verify_plan_commit': '커밋 안 계획 파일 바이트 sha256 (L3 시험)',
                     'validate_kit_arrays': '정확 중복 경로 = 점열 float64 바이트 sha256 (S0-5i)',
                     'census_kit': 'payload argv sha256 (NUL 결합 UTF-8 · 기록만)'},
    'step3_conv_cert': {},
}


def _hash_users(path):
    tree = ast.parse(open(path, encoding='utf-8').read())
    out = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if any(isinstance(x, ast.Name) and x.id == 'hashlib' for x in ast.walk(node)):
                out.add(node.name)
    return out


@case('FP')
def t_fp():
    import ptfe_face_alpha as FA
    import ca_s0_census as S0
    # ── FP-a · b · c · d · e · f — `_fp` 자체 ──
    a = _objarr([_rt(w) for w in _FP_WORDS])
    b = _objarr([_rt(w) for w in _FP_WORDS])
    distinct = any(x is not y for x, y in zip(a, b))
    chk('FP-a 객체 배열 — 같은 내용 · 다른 객체 (실행 중 만든 문자열 · UTF-8 · 빈 문자열) → 같은 지문 (원소 · dict 안 · 목록 안)',
        distinct and CJ._fp(a) == CJ._fp(b) and CJ._fp({'reason': a, 'k': 1}) == CJ._fp({'reason': b, 'k': 1})
        and CJ._fp([a, 3]) == CJ._fp([b, 3]), f'다른 객체 {distinct}')
    w2 = list(_FP_WORDS); w2[0] = 'covered_SDCQ'
    w3 = list(_FP_WORDS); w3[3] = w3[3].replace('접합', '접힙')
    chk('FP-b 한 글자 다름 (ASCII · 한글) → 다른 지문', CJ._fp(a) != CJ._fp(_objarr([_rt(w) for w in w2]))
        and CJ._fp(a) != CJ._fp(_objarr([_rt(w) for w in w3])))
    #  같은 모양 쌍이 경계 · 길이 접두를 본다 (모양이 다르면 머리의 모양만으로도 갈린다) — 변이 판별: '|'·'' 결합 · repr 결합 ([1, 23] ~
    #  [12, 3]) · 형 표지만 있고 길이 접두 없음 (['aSb', 'c'] ~ ['a', 'bSc'])
    pairs = ((['ab', 'c'], ['a', 'bc']), (['a|b', 'c'], ['a', 'b|c']), (['aSb', 'c'], ['a', 'bSc']), ([1, 23], [12, 3]),
             (['a', 'b'], ['b', 'a']), (['x'], ['x', '']), (['1'], [1]), ([None], ['None']), ([True], [1]), ([1.0], [1]),
             ([b'ab'], ['ab']))
    bad = [f'{p}~{q}' for p, q in pairs if CJ._fp(_objarr([_rt(x) if isinstance(x, str) else x for x in p]))
           == CJ._fp(_objarr([_rt(x) if isinstance(x, str) else x for x in q]))]
    sq = _objarr([_rt('ab'), _rt('cd')])
    if CJ._fp(sq) == CJ._fp(sq.reshape(1, 2)):
        bad.append('모양 (2,)~(1,2)')
    chk('FP-c 경계 · 순서 · 개수 · 모양 · 형 (길이 접두 · 순서 보존 · 형 표지) → 다른 지문', not bad, f'{bad}')

    def _mixed():
        k = int('1000') + 7
        return _objarr([None, bool(k), k, float(k) / 4.0, np.float64(k) / 8.0, np.int64(k) * 3, bytes([120, 121]),
                        (_rt('ab'), k), _rt('끝')])
    m1, m2 = _mixed(), _mixed()
    chk('FP-d 섞인 원소 (None · bool · int · float · numpy 수 · bytes · 튜플) — 같은 내용 · 다른 객체 → 같은 지문',
        CJ._fp(m1) == CJ._fp(m2))
    a2 = np.arange(12, dtype=np.int64).reshape(3, 4)
    nums = (a2, np.linspace(0.0, 1.0, 7), a2.T, a2[:, ::2], np.zeros((0, 3)), np.array([True, False]))
    chk('FP-e 숫자 배열 = dtype · 모양 · C 순서 바이트 그대로 (독립 식 · 연속 아닌 뷰 = 연속 사본) — 옛 지문 비트 유지',
        all(CJ._fp(x) == _fp_numeric_formula(x) for x in nums) and CJ._fp(a2.T) == CJ._fp(np.ascontiguousarray(a2.T)))
    refused = [raises(lambda v=v: CJ._fp(v), TypeError) for v in
               (_objarr([object()]), _objarr([_rt('ok'), {1, 2}]), object(), {1, 2}, np.zeros(2, dtype=[('a', 'O')]))]
    chk('FP-f 내용 직렬화가 없는 원소 · 값 (object() · set · 구조체 객체 칸) = 거부 (주소 · 해시 순서로 지문을 만들지 않는다)',
        all(refused), f'{refused}')
    # ── FP-g · h — 원장 · 계획 지문 (픽스처: 포트 미실현 사유 'covered_SDCP' = f-문자열) ──
    P, sid, pid = _fp_fixture()
    r1 = registry(sid, P, r_port_um=_FP_RPORT)
    r2 = registry(sid, P, r_port_um=_FP_RPORT)
    rs1, rs2 = r1['instances']['reason'], r2['instances']['reason']
    pre = (len(rs1) == 1 and rs1.dtype == object and rs1[0] == 'covered_SDCP' and rs1[0] is not rs2[0])
    p1 = _try(lambda: plan(r1, 1e3), None)
    p2 = _try(lambda: plan(r2, 1e3), None)
    chk('FP-g 같은 입력으로 다시 만든 원장 — 원장 지문 · 계획 행 지문 같음 (사유 = 실행 중 만든 다른 문자열 객체)',
        pre and r1['fp']['registry'] == r2['fp']['registry'] and p1 is not None and p2 is not None
        and p1['fp_rows'] == p2['fp_rows'], f"전제 {pre} · {r1['fp']['registry']} ↔ {r2['fp']['registry']}")
    rsame = dict(r1); rsame['instances'] = dict(r1['instances'])
    rsame['instances']['reason'] = _objarr([_rt(x) for x in rs1])
    ok_same = (CJ.registry_fp(rsame) == r1['fp']['registry']) and (_try(lambda: plan(rsame, 1e3), None) is not None)
    chk('FP-h 같은 내용 새 객체로 바꾼 원장 → 지문 같음 · 계획이 받아들인다 (거짓 거부 없음)', ok_same)
    rdiff = dict(r1); rdiff['instances'] = dict(r1['instances'])
    rdiff['instances']['reason'] = _objarr([_rt(x).replace('SDCP', 'SDCQ') for x in rs1])
    chk('FP-h 한 글자 바꾼 원장 (사유 SDCP → SDCQ) → 지문 다름 · 계획 거부 (E5)',
        CJ.registry_fp(rdiff) != r1['fp']['registry'] and raises(lambda: plan(rdiff, 1e3)))
    # ── FP-i — 별도 `python3 -I` 하위 프로세스 둘 · 이 프로세스 ──
    tmpd = tempfile.mkdtemp(prefix='cjfp_')
    try:
        kids, here = _fp_children(tmpd, P)
    finally:
        shutil.rmtree(tmpd, ignore_errors=True)
    for grp, nm in (('cj_', 'carbon_junction (객체 배열 · 원장 · 계획)'), ('fa_', 'ptfe_face_alpha (캡슐 · 행 · 계획 · 간선 · 격자)'),
                    ('s0_', 'ca_s0_census (계획 sha256 · 정준 바이트 · 파일 sha256)')):
        keys = sorted(k for k in (here or {}) if k.startswith(grp))
        same = (bool(keys) and all(k_ is not None for k_ in kids)
                and all(kids[0].get(k) == kids[1].get(k) == here[k] for k in keys))
        diff = [k for k in keys if not (kids[0] and kids[1]) or not (kids[0].get(k) == kids[1].get(k) == here.get(k))]
        chk(f'FP-i 별도 `python3 -I` 하위 프로세스 둘 (힙 선할당 0 · 20000) = 이 프로세스 — {nm} ({len(keys)} 지문)', same,
            f'다름 {diff}')
    # ── FP-j — 격자 지문 감싸개 (`_grid_fp` → step3_sigma._grid_fp) ──
    g0 = np.arange(24, dtype=np.int8).reshape(2, 3, 4)
    g1 = g0.copy()
    g2 = g0.copy(); g2[1, 2, 3] += 1
    gobj = np.empty((2, 2, 2), dtype=object)
    for i in range(gobj.size):
        gobj.flat[i] = int('100') + i
    for nm_, fn in (('carbon_junction', CJ._grid_fp), ('ptfe_face_alpha', FA._grid_fp)):
        chk(f'FP-j {nm_}._grid_fp 숫자 격자 — 같은 내용 다른 객체 = 같음 · 한 칸 다름 · dtype 다름 = 다름',
            fn(g0) == fn(g1) and fn(g0) != fn(g2) and fn(g0) != fn(g0.astype(np.int16)) and fn(None) is None)
        chk(f'FP-j {nm_}._grid_fp 객체 격자 = 거부 (포인터 바이트 · 격자는 수치 배열 계약)', raises(lambda f_=fn: f_(gobj), TypeError))
    # ── FP-k — S1 지문 (내용 기반 확인 · 옛 코드도 통과해야 한다) ──
    m4 = P[1] == 4
    Q, Fq, Kq = P[0][m4], P[2][m4], P[3][m4]
    big = np.repeat(Q, 2, axis=0)
    variants = (Q.copy(), np.asfortranarray(Q), big[::2], Q.tolist())
    fps = [FA.build_capsules(v, Fq, Kq)['fp'] for v in variants]
    Qd = Q.copy(); Qd[1, 0] = np.nextafter(Qd[1, 0], np.inf)
    sig = sig_e()
    pa = FA.build_plan(sid, sig, FA.build_capsules(Q, Fq, Kq), lo=(0.0, 0.0, 0.0), vox=H, channel='electronic', pid=pid)
    pb = FA.build_plan(sid.copy(), sig.copy(), FA.build_capsules(Q.copy(), Fq.copy(), Kq.copy()), lo=(0.0, 0.0, 0.0), vox=H,
                       channel='electronic', pid=pid.copy())
    ax = tuple({'lin': pa['axes'][k]['lin'].astype(np.int32), 'alpha': pa['axes'][k]['alpha']} for k in range(3))
    e1 = tuple({'lin': pa['axes'][k]['lin'], 'alpha': pa['axes'][k]['alpha'], 'g': pa['axes'][k]['alpha'] * 2.0} for k in range(3))
    e2 = tuple({kk: np.array(vv) for kk, vv in e.items()} for e in e1)
    e3 = tuple({kk: np.array(vv) for kk, vv in e.items()} for e in e1)
    nz = [k for k in range(3) if len(e3[k]['g'])]
    if nz:
        e3[nz[0]]['g'][0] = np.nextafter(e3[nz[0]]['g'][0], np.inf)
    chk('FP-k ptfe_face_alpha — 캡슐 지문 (사본 · F 순서 · 연속 아닌 뷰 · 목록 = 같음 · 좌표 1 ulp = 다름) · 계획 행 · 계획 · 간선 '
        '(같은 내용 = 같음 · 1 ulp = 다름)',
        len(set(fps)) == 1 and FA.build_capsules(Qd, Fq, Kq)['fp'] != fps[0] and pa['n_rows'] > 0
        and pa['fp_rows'] == pb['fp_rows'] and pa['fp_plan'] == pb['fp_plan'] and FA.rows_fp(ax) == pa['fp_rows']
        and FA.edges_fp(e1) == FA.edges_fp(e2) and bool(nz) and FA.edges_fp(e1) != FA.edges_fp(e3),
        f"캡슐 {len(set(fps))} · 행 {pa['n_rows']}")
    # ── FP-l — S0 계획 · 파일 sha256 ──
    _, b1, h1 = S0.make_plan(0.15, 0.075, 2.0, {'stage': 1, 'kit_name': _rt('kit_fp')})
    _, b2, h2 = S0.make_plan(float('0.15'), 0.075, 2.0, dict({'kit_name': _rt('kit_fp')}, stage=1))
    _, b3, h3 = S0.make_plan(0.15, 0.075, 2.0, {'stage': 1, 'kit_name': _rt('kit_fq')})
    tmpd = tempfile.mkdtemp(prefix='s0fp_')
    try:
        fa_, fb_, fc_ = (os.path.join(tmpd, x) for x in ('a.bin', 'b.bin', 'c.bin'))
        for pth, data in ((fa_, b1), (fb_, bytes(bytearray(b1))), (fc_, b1[:-2] + b'X\n')):
            with open(pth, 'wb') as fh:
                fh.write(data)
        same_f = S0._sha256_file(fa_) == S0._sha256_file(fb_) and S0._sha256_file(fa_) != S0._sha256_file(fc_)
    finally:
        shutil.rmtree(tmpd, ignore_errors=True)
    chk('FP-l ca_s0_census — 계획 sha256 · 정준 바이트 (다른 객체로 만든 같은 계획 = 같음 · 출처 한 글자 = 다름) · 파일 sha256',
        h1 == h2 and b1 == b2 and h1 != h3 and same_f)
    # ── FP-m — 목록 (이 시험이 덮는 지문 · 해시 함수 = 모듈 본문의 hashlib 사용 함수 전부) ──
    got = {m_: _hash_users(os.path.join(SCRIPTS, m_ + '.py')) for m_ in FP_INVENTORY}
    want = {m_: set(v) for m_, v in FP_INVENTORY.items()}
    chk('FP-m 지문 · 해시 함수 목록 = 이 시험의 표 (새 함수 = 덮을 때까지 실패 · step3_conv_cert = 없음)', got == want,
        f'{ {m_: sorted(got[m_] ^ want[m_]) for m_ in got if got[m_] != want[m_]} }')


# ═════════════════════════ PIECE4 — 끊기 규칙 사본 대조 (생산 · B · C · A · 2 일 차) ═════════════════════════
#  같은 gap_tol 규칙 (연속 점 간격 > gap_tol × 그 경로 간격 중앙값 → 끊음) 이 네 곳에 따로 있다: 생산 `step3_sigma._fibre_segment_ijk`
#  (셀만 낸다) · B `carbon_junction.fibre_pieces` · C `ca_s0_census.pieces_of` · A `ptfe_face_alpha.build_capsules` (안쪽 줄).
#  하나로 합치지 않는다 (생산 경로 비트 동일 부담) — 이 시험이 넷을 묶는다.  침대 (µm · vox 0.1): 틈 > 2 셀 · 한 점 조각 (앞 · 가운데 ·
#  뒤) · 정확히 경계인 틈 (d = gap_tol × 중앙값 → 끊지 않는다 · 이진 정확 좌표) · 두 점 · 한 점 경로 · 무작위 3D (지운 점 = 틈).
#  ① 조각 경계 (점 번호 구간) B = C = A ② 생산 셀 열 = 각 사본의 조각을 생산 원시 함수 (`segment_cells`) 로 다시 구운 셀 열 (순서 그대로)
#  ③ C 의 셀 빌더 (`_cells_from_pieces`) = 생산 셀 열 · B 의 멤버십 위치 셀 집합 = 생산 셀 집합.
PIECE4_VOX = 0.1
PIECE4_N = (40, 40, 40)
_PIECE4_MUT = {'step3_sigma': 'np.nonzero(d > gap_tol * med)', 'carbon_junction': 'np.nonzero(d > gap_tol * med)',
               'ca_s0_census': 'np.nonzero(d > gap_tol * med)', 'ptfe_face_alpha': 'np.nonzero(d > g_t * med)'}


def _piece4_beds():
    def line(x0, n, dx=0.1, y=1.05, z=1.05):
        return [(x0 + dx * k, y, z) for k in range(n)]
    beds = []
    beds.append(('틈 하나 (0.6 µm = 6 셀)', np.array(line(0.15, 10) + line(1.65, 10))))
    beds.append(('한 점 조각 — 앞 · 가운데 · 뒤', np.array([(0.15, 2.05, 1.05)] + line(0.75, 5, y=2.05) + [(1.85, 2.05, 1.05)]
                                                       + line(2.45, 4, y=2.05) + [(3.55, 2.05, 1.05)])))
    #  정확 경계: 간격 0.25 (이진 정확) · 0.5 = 2 × 중앙값 (끊지 않음 · 엄격 >) · 0.75 (끊음) — `>=` 변이는 0.5 에서도 끊는다
    xs = [0.25, 0.5, 0.75, 1.0, 1.5, 1.75, 2.0, 2.75, 3.0, 3.25]
    beds.append(('정확히 경계인 틈 (0.5 = 2 × 0.25 · 끊지 않음) + 끊는 틈 0.75', np.array([(x, 0.375, 2.125) for x in xs])))
    beds.append(('두 점 경로', np.array([(0.35, 3.05, 3.05), (0.95, 3.05, 3.05)])))
    beds.append(('한 점 경로', np.array([(2.35, 3.05, 3.05)])))
    rng = np.random.default_rng(20261020)
    box = np.array(PIECE4_N, float) * PIECE4_VOX
    for t in range(6):
        p = [rng.uniform(0.6, box - 0.6)]
        for _ in range(int(rng.integers(25, 45))):
            d = rng.normal(size=3); d /= np.linalg.norm(d)
            p.append(np.clip(p[-1] + d * rng.uniform(0.07, 0.12), 0.02, box - 0.02))
        Q = np.asarray(p)
        keep = np.ones(len(Q), bool)
        for _ in range(int(rng.integers(1, 4))):                # 지운 점 = 틈 (시더가 AM 안 점을 드랍하는 꼴)
            a = int(rng.integers(2, len(Q) - 6)); keep[a:a + int(rng.integers(3, 7))] = False
        beds.append((f'무작위 3D {t}', Q[keep]))
    return beds


def _piece4_ranges_index(Q, pcs):
    out, a = [], 0
    for ix in pcs:
        ix = np.asarray(ix)
        if not np.array_equal(ix, np.arange(a, a + len(ix))):
            return None
        out.append((a, a + len(ix))); a += len(ix)
    return out if a == len(Q) else None


def _piece4_ranges_points(Q, pcs):
    out, a = [], 0
    for R in pcs:
        R = np.asarray(R, np.float64).reshape(-1, 3)
        if not np.array_equal(R, Q[a:a + len(R)]):
            return None
        out.append((a, a + len(R))); a += len(R)
    return out if a == len(Q) else None


def _piece4_capsule_pieces(caps):
    """A — 캡슐 선분 (A→B) 에서 조각 점열을 되읽는다: 새 조각 = 앞 선분 끝 ≠ 이 선분 시작 · 선분 하나 · 길이 0 = 한 점 조각."""
    A, B = np.asarray(caps['A']), np.asarray(caps['B'])
    pieces = []
    for i in range(len(A)):
        if i == 0 or not np.array_equal(A[i], B[i - 1]):
            pieces.append([A[i], B[i]])
        else:
            pieces[-1].append(B[i])
    return [np.asarray(p[:1]) if len(p) == 2 and np.array_equal(p[0], p[1]) else np.asarray(p) for p in pieces]


def _piece4_cells(Q, ranges, lo, vox, n):
    from fibre_segment_raster import segment_cells
    out = []
    for a, b in ranges:
        R = Q[a:b]
        if len(R) == 1:
            out.append(np.floor((R - lo) / vox).astype(int))
        else:
            out.append(np.vstack([segment_cells(R[i] - lo, R[i + 1] - lo, vox) for i in range(len(R) - 1)]))
    ijk = np.vstack(out).astype(int) if out else np.zeros((0, 3), int)
    return ijk[((ijk >= 0) & (ijk < n)).all(1)]


def _piece4_compare(mods, gap_tols=(2.0, 3.0)):
    """네 구현 (mods = 생산 · B · C · A 모듈) 대조 → (불일치 목록, 정확 경계 틈이 있던 침대 수)."""
    s3m, cjm, s0m, fam = (mods[k] for k in ('step3_sigma', 'carbon_junction', 'ca_s0_census', 'ptfe_face_alpha'))
    lo = np.zeros(3); n = np.array(PIECE4_N); vox = PIECE4_VOX
    bad, n_exact = [], 0
    for nm, Q in _piece4_beds():
        Q = np.asarray(Q, np.float64)
        if len(Q) >= 2:
            d = np.linalg.norm(np.diff(Q, axis=0), axis=1)
            n_exact += int(np.any(d == 2.0 * float(np.median(d))))
        for gt in gap_tols:
            tag = f'{nm} · gap_tol {gt}'
            m = len(Q)
            prod, _ph = quiet(s3m._fibre_segment_ijk, Q, np.full(m, 2), np.full(m, 7), lo, vox, n, gt,
                              add_kind=np.ones(m, int))
            rB = _piece4_ranges_index(Q, cjm.fibre_pieces(Q, gt))
            pcsC = s0m.pieces_of(Q, gt)
            rC = _piece4_ranges_points(Q, pcsC)
            caps = fam.build_capsules(Q, np.zeros(m, np.int64), np.ones(m, np.int64), gap_tol=gt)
            rA = _piece4_ranges_points(Q, _piece4_capsule_pieces(caps))
            if rB is None or rC is None or rA is None or not (rB == rC == rA):
                bad.append(f'{tag}: 조각 경계 B {rB} · C {rC} · A {rA}')
                continue
            if caps['n_pieces'] != len(rA) or caps['n_point_pieces'] != sum(1 for a, b in rA if b - a == 1):
                bad.append(f'{tag}: A 조각 수 기록 {caps["n_pieces"]} · 한 점 {caps["n_point_pieces"]} ↔ {rA}')
            for who, rr in (('B', rB), ('C', rC), ('A', rA)):
                if not np.array_equal(_piece4_cells(Q, rr, lo, vox, n), prod):
                    bad.append(f'{tag}: 생산 셀 열 ≠ {who} 조각으로 다시 구운 셀 열')
            if not np.array_equal(s0m._cells_from_pieces(pcsC, lo, vox, n), prod):
                bad.append(f'{tag}: C 셀 빌더 ≠ 생산 셀 열')
            segs, pcs = cjm._segments_of([(7, np.arange(m), True)], Q, gt)
            pos, _pp = cjm._positions(pcs, segs, lo, vox, n, np.zeros(PIECE4_N, np.int8))
            inb = pos['lin'] >= 0
            if {tuple(int(v) for v in c) for c in pos['ijk'][inb]} != {tuple(int(v) for v in c) for c in prod}:
                bad.append(f'{tag}: B 멤버십 셀 집합 ≠ 생산 셀 집합')
    return bad, n_exact


def _piece4_mutant(modname, tmpd):
    src = open(os.path.join(SCRIPTS, modname + '.py'), encoding='utf-8').read()
    old = _PIECE4_MUT[modname]
    if src.count(old) != 1:
        return None, f'변이 대상 문자열 {old!r} 이 {modname}.py 에 {src.count(old)} 번 (1 번이어야)'
    p = os.path.join(tmpd, f'{modname}_piece4_mut.py')
    with open(p, 'w', encoding='utf-8') as fh:
        fh.write(src.replace(old, old.replace(' > ', ' >= ')))
    spec = importlib.util.spec_from_file_location(f'{modname}_piece4_mut', p)
    m = importlib.util.module_from_spec(spec)
    quiet(spec.loader.exec_module, m)
    return m, ''


@case('PIECE4')
def t_piece4():
    import ptfe_face_alpha as FA
    import ca_s0_census as S0
    real = {'step3_sigma': S3, 'carbon_junction': CJ, 'ca_s0_census': S0, 'ptfe_face_alpha': FA}
    bad, n_exact = _piece4_compare(real)
    nb = len(_piece4_beds())
    chk(f'PIECE4 네 구현 (생산 · B · C · A) — 조각 경계 같음 · 생산 셀 열 = 각 사본 조각을 다시 구운 셀 열 · C 셀 빌더 = 생산 · '
        f'B 멤버십 셀 집합 = 생산 ({nb} 침대 × gap_tol 2 · 3 · 정확 경계 틈 침대 {n_exact})', not bad and n_exact >= 1,
        f'{bad[:4]} · 정확 경계 {n_exact}')
    tmpd = tempfile.mkdtemp(prefix='piece4_')
    try:
        for modname in ('step3_sigma', 'carbon_junction', 'ca_s0_census', 'ptfe_face_alpha'):
            mut, why = _piece4_mutant(modname, tmpd)
            caught = False
            if mut is not None:
                mods = dict(real)
                mods[modname] = mut
                try:
                    mb, _ = _piece4_compare(mods)
                    caught = bool(mb)
                except Exception as e:                     # noqa: BLE001 — 변이가 예외로 끝나도 '걸렸다' (기록)
                    print(f'    PIECE4 변이 {modname}: 예외 {type(e).__name__}: {e}')
                    caught = True
            chk(f'PIECE4 변이 — {modname} 사본의 `>` → `>=` (나머지 셋은 그대로) → 시험이 떨어진다 (정확 경계 틈)',
                mut is not None and caught, why or 'not caught')
    finally:
        shutil.rmtree(tmpd, ignore_errors=True)


def main():
    global S3, CJ, QUICK
    ap = argparse.ArgumentParser(description='Rint ② S2/S3 시험 (시험 먼저)')
    ap.add_argument('--quick', action='store_true', help='C0 무작위 침대 수를 줄인다')
    ap.add_argument('--only', default='', help='쉼표로 묶음 태그만 (예: C1,S3)')
    a = ap.parse_args()
    QUICK = a.quick
    import step3_sigma as _s3
    S3 = _s3
    try:
        import carbon_junction as _cj
        CJ = _cj
    except Exception as e:                                 # noqa: BLE001
        print(f'  ⚠ carbon_junction import 실패: {type(e).__name__}: {e}')
        CJ = None
    only = {x.strip() for x in a.only.split(',') if x.strip()}
    for tag, fn in CASES:
        if only and tag not in only:
            continue
        print(f'── {tag}')
        try:
            fn()
        except Exception as e:                             # noqa: BLE001 — 묶음 하나의 예외 = 그 묶음 실패 (다음 묶음은 계속)
            import traceback
            traceback.print_exc(limit=2)
            chk(f'{tag} 묶음 예외 없이 끝남', False, f'{type(e).__name__}: {e}')
    print(f'\n== test_carbon_junction: {_ok}/{_ok + len(_fail)} PASS')
    if _fail:
        print('FAIL: ' + ' · '.join(_fail))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
