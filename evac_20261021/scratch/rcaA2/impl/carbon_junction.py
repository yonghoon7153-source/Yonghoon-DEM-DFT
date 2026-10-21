#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② S2 탄소 접합 R_j v0 (VGCF–VGCF) + S3 SDCP 접합 수정자 — 기구 (2026-10-20 · 기본 끔).

정본 = 설계 v1 `docs/reviews/rint_carbon_additive_design_v1_20261020.md` §4 (S2 v0) · §5 (S3) · 계약 v2 §3-8 J1–J8 ·
v3 §5 J2a–J12 · v3.1 (겹치면 뒤가 이긴다) · 1저자 10-20 N1–N18 = 권고대로.  시험 = `scripts/test_carbon_junction.py`.

⛔ 지위 = **기구만** (mechanism_only): R_j 는 모형 내부 보정값 (재료값 아님 · 포트 직접 간선에 반셀 없음 = RINTG-09) ·
  VGCF–VGCF 만 정량 · VA · SV · SA 면 = 옛 융합 그대로 (선언 · 필수 한정어 "SDCP–VGCF 접촉 저항 0 가정") · payload CLI 미배선 ·
  `PROTOCOL_FIELDS` 밖 · `solve_sigma_z(cjunc=None)` (기본) = 옛 경로 비트 같음.

세 단 (①′ 와 같은 꼴):
  reg  = cjunc_registry(sid, lo, vox, add_pts, add_phase, add_fid, add_kind, r_f_um=…, tol_ff_um=…, L_par_um=…, r_port_um=…)
         기하만 — 멤버십 (J1) · instance (J2a · J2c · 자기 접합) · 포트 (J3 · J4) · 면 표 (축방향 · 접합 자리 절단 · 미등록 · VX) ·
         SDCP 근접 · PTFE 덮임 · census · 지문
  plan = cjunc_plan(reg, R_j_ohm, unreg_law=…, ptfe_stamp=…, ptfe_jlaw='P0', sdcp_mod=None)
         instance 마다 간선 · 축약 (R_j′ = 0) · 절단 (P1) · 미실현 — S3: R_j′ = R_j,0·(1 − c·a_j) · c = 1 = 축약 경로
  solve_sigma_z(…, cjunc=plan) → res['cjunc'] (기록) · res['_cjunc'] (dof 수준 원장 — 시험 · 진단)

구현이 정한 것 (설계에 식이 없던 자리 · 1저자 확인 대상 — 보고에 적는다):
  L_c (접촉 길이) = 두 가닥 각각에서 **중심선 거리 ≤ r_fi + r_fj (닿음)** 인 구간 길이의 최댓값 (`CJUNC_LC_RULE`) —
    L_par = 2(r_fi + r_fj) 가 "직교 교차의 최대 닿음 길이" 와 같아지는 읽기 (직교 교차 = 배율 1 · 비스듬한 깊은 교차는 길 수 있다).
  ★ 길이 법칙 v0 (`CJUNC_LEN_LAW` · 1저자 10-20 밤 Q17 · 옛 J8 "긴 접촉 = 정량 거부" 대체): 접합 G = max(1, L_c/L_par) / R_j,0 —
    긴 접촉 = 점 접합 L_c/L_par 개 병렬 (선 접촉 협착 컨덕턴스 ∝ 길이의 1차 근사) · 새 손잡이 없음 (R_j,0 하나).  L_c ≤ L_par·(1 + 1e-9)
    이면 배율 = 정확히 1 (`junction_len_mult`) — 법칙은 경계에서 연속이라 묶음의 크기 ≤ 1e-9 상대이고, 깊은 직교 교차 (L_c = L_par) 의
    선분 길이 합 반올림 몇 ulp 가 점 접합 결과를 비트에서 바꾸지 않게 한다 (긴 접촉 표지 · 집계 = 같은 문턱).
  ★★ 분산판 v0 (`CJUNC_DIST_RULE` · 10-21 Codex RCA-05 · 1저자 Q3 (가) — 옛 '한 포트에 총 G 집중 (lumped) · 분산판 = v1 후보' 를 당겼다):
    instance 마다 k = ceil(L_c/L_par) 간선 (L_c ≤ L_par·(1 + 1e-9) = k 1 = 옛 점 접합 그대로 · 비트 같음 · 정수 경계 = 같은 1e-9 띠) ·
    간선마다 G = (총 G_j = max(1, L_c/L_par)/R_j,0)/k (총 G = 길이 법칙 그대로 · 새 손잡이 없음) · 위치 = 정의 쪽 (닿음 길이가 긴 가닥 ·
    1e-9 상대 안 동률 = i 쪽) 의 닿음 구간 (경로 순서 합집합) 을 k 등분한 칸의 가운데 점 X · 맞은편 가닥 최근접점 Y (ε 띠 · 사전식) ·
    포트 = X · Y 의 기하 정준 포트 (아래) · **간선마다** PTFE 덮임 (P0/P1) · SDCP 근접 (c) 판정 (간선 접점 = (X + Y)/2).
  ★★ 조각 = 섬유 (`CJUNC_PIECE_RULE` · 10-21 사전 리뷰 (구현) PRE-impl-01 · 06 · 1저자 Q-A): 생산 끊기 규칙 (`fibre_pieces`) 이 가른 같은 fid 의
    두 조각은 경로로 이어지지 않는다 → 서로 다른 섬유와 같은 접합 규칙 (중심선 d ≤ D → R_j · s 규칙 없음 · 옛: 같은 fid = 자기 후보 · 조각
    사이 간격 현을 지나는 s 로 '연속' → 같은 셀 끝 = 경로로만 (σ 0) · 면 인접 끝 = 옛 융합).  호 좌표 = 조각 안 누적 (조각마다 0 부터).
    닫힌 경로 (첫 점 = 끝 점 · 비트) 의 이음매 = 연속: 끊김이 있으면 끝 조각 + 첫 조각을 이음매를 지나 한 조각으로 · 없으면 고리 조각 (s =
    둘레 짧은 쪽 · 첫 · 끝 위치 같은 셀 = 별칭 한 dof · 면 이웃 = 축방향 둘레).
  ★★ 자기 접합 (`CJUNC_SELF_RULE` · 10-21 PRE-impl-02 · 1저자 Q-B) = 서로 다른 섬유와 같은 탐지 — 같은 조각 중심선 선분 쌍 (최근접 d ≤ D) 마다
    s = 최근접점 사이 조각 호 길이 · 바닥 (`_self_floor`: s > D 그리고 s > (π/2)·d — 곧은 이웃 · 꼭짓각 ≥ 79° 꺾임 모서리 = 어느 s_min 에서도
    연속) · 접합 쌍 = 바닥 쌍 중 s ≥ s_min (s < s_min = 같은 가닥의 연속 · 접합 아님) · 이웃 선분 쌍 무리 (union-find · 고리 = 둘레) 하나 =
    instance 하나 (접점 · d0 = 서로 다른 섬유와 같은 CP 규칙 · L_c = 그 무리 접합 쌍의 닿음 · 같은 길이 법칙 · 같은 분산판 (맞은편 = 그 쌍만)).
    셀 인접 (면 · 같은 셀) 은 후보를 만들지 않는다 (옛: 셀 인접 = 후보 · 중심선 거리 검사 없음 → 닿지 않는 다리에 접합 · 닿는 모서리 인접 다리에
    없음).  같은 조각 면 (축방향 아님) = 두 위치가 연속 (`_continuity` — 같은 바닥 · s_min) 이면 옛 융합 · 아니면 자기 instance 발자국 = 절단 ·
    아니면 미등록.  s_min = 필수 · 기본값 없음 (None = 미등록 → 정량 거부 · 시험 모드 = 바닥만).
    ★ 멤버십 열쇠 = (cell, fid, branch) (`CJUNC_BRANCH_RULE` · 10-21 Codex RCA-03 · 1저자 Q1 (가)): branch = 그 셀을 지나는 연속 경로 구간
      (위치 하나) — 같은 셀의 같은 조각 다른 가지는 **합치지 않는다**.  접합 쌍이 잇지 않은 재방문 = 경로로만 (`n_self_revisits_path_only` ·
      사이에 덮인 위치가 있으면 `n_self_revisits_path_broken`).
  ★★ 포트 = 옮기지 않음 (`CJUNC_PORT_RULE` v3 · 10-21 PRE-impl-03 · 1저자 Q-C): 후보 = 그 조각 (자기 접합 = 그 쪽) 의 위치 **살았든 덮였든** ·
    고른 위치가 덮였으면 (SDCP · PTFE · 상자 밖) 미실현 (covered_<상> · out_of_box) — 덮은 상의 법칙만 (SDCP = SV 융합 · S3 c · PTFE =
    face_alpha P0/P1) · 같은 접촉을 두 번 세지 않는다 (옛: 살아있는 이웃 셀로 옮겨 SV 융합과 병렬 · centerline 은 절연체를 더해 σ 상승).
    접합 + ptfe_stamp centerline = 거부 (계획 · 솔브 입구 · `ca_ext_cjunc` protocol).
  절단 발자국 = instance 로 묶인 **선분 쌍 run 전체** (`_footprint_segs` — 구현 B 부터 최근접 쌍만이 아니었다) · 긴 접촉의 run 위
    융합 i|j 면이 접합 간선을 우회하지 않는다.
  ★★ 포트 = 방향 무관 기하 정준 규칙 (`CJUNC_PORT_RULE` · 10-21 Codex RCA-04 · 1저자 Q2 (가)): 접점까지 후보 셀 중심 거리 (r_port 안) →
    ε 띠 (거리² 1e-9 µm²) 안 동률 = 셀 정수 좌표 사전식 최소 → 같은 셀의 여러 가지 = 접점까지 그 가지 중심선 거리 (ε 띠) → 그래도 같으면
    정준 (조각, 번호).  경로 열 번호 (옛 '정준 방향 경로 번호가 작은 위치') 를 쓰지 않는다 — 먼 끝이 바뀌어 정준 방향이 뒤집혀도 같다.
  ★★ 경로 순서 = 기하 정준 (`CJUNC_ORDER_RULE` · fid 라벨 무관): 경로마다 정준 방향 (역순 점열이 사전식으로 작으면 뒤집음) 의 (첫 점,
    끝 점, 점열) 사전식 순 · 조각 = 그 방향 순서 · 주 위치 · 동률 · instance 방향 · 순서 = (조각, 번호) 와 기하만 — fid 재명명 · 경로 반전 ·
    (끝점이 다른 경로들의) 공선 세분에 원장 · 간선 원장 · σ 비트 같음 (같은 기하 · 역순 포함 = 거부 · 두 끝점이 다 같은 두 경로 · 닫힌
    고리는 점열이 가른다 = 세분 의존 · 남은 한계).
  instance 접점 (`CJUNC_CP_RULE`) = 최근접 선분 쌍들 중 거리² ε 띠 안 · 중점 사전식 최소 (나란한 접촉의 비유일 최근접점 = 세분 · 순서 무관).
  교차 셀의 비탄소 면 · 판 결합 · 미등록 융합 면 = 기하 최근접 멤버십 (J9 · ε 띠 1e-9 µm² · 최근접점 → 방향 → (조각, 번호)).
  ★ SV (10-21 Codex RCA-06 · 1저자 Q4 (가)): 옛 `sv_dominant` (SV 면 + SDCP 셀 소산 ≥ VV 접합 소산 = '지배' 표지) **철회** — 소산 몫은
    국소 저항 민감도이지 경로 지배 · 우회 크기가 아니다 (판정문 반례: SV 경로 전류 90.5 % 인데 가드 false).  남는 것 = 진단
    `sv_local_dissipation` (몫만) · 반사실 대조 (선택 노브 `cjunc_plan(sv_counterfactual={'threshold': t})` — 같은 침대 · 같은 R_j 에서
    ★ 10-21 (PRE-impl-04 · 1저자 Q-D · `CJUNC_SV_CF_RULE`) **SV 다리만** 끊은 판 (서로 다른 섬유 · 접합으로 갈린 가지를 잇는 SDCP 성분의 SV
    면 · SDCP 를 지나는 섬유의 자기 연속은 남긴다 · 끊기만 = 비 ≥ 1) 의 단자 G 와의 비 `sv_counterfactual_ratio` (기록 종류
    `CJUNC_SV_CF_KIND` · 옛 'SV 면 전부' = SDCP 를 지나는 섬유 하나도 비 ∞) · 문턱 = 기본값 없음 (등록이 채운다) · 표지 `SV_DEPENDENT` 는
    문턱이 주어질 때만).
"""
import hashlib
import math
import struct

import numpy as np
from scipy import ndimage, sparse

CJUNC_MODEL_VERSION = 'r3-carbon-junction-port-v3'   # v3 (10-21 사전 리뷰 impl · Q-A 조각 = 섬유 · 고리 이음매 · Q-B 자기 = 중심선 근접 + 쌍 s · Q-C 옮김 없음 · Q-D SV 다리만 끊음)
CJUNC_SCHEMA = 'cjunc-v2'                  # v2 = 계획 행 = 분산 간선 (원장 'subedges') · 수 = 간선 단위 + n_subedges
CJUNC_LC_RULE = 'touch_len_max_v1'
CJUNC_SELF_LC_RULE = 'touch_len_max_junction_pairs_v2'   # 자기 접합 L_c — 같은 닿음 규칙 · 짝 = 그 instance 의 접합 쌍 (바닥 · s 규칙을 지난 쌍) 만
CJUNC_SELF_S_RULE = 'arc_at_closest_points_piece_cyclic_v2'   # s = 쌍의 최근접점 사이 조각 호 길이 (고리 = 짧은 쪽) · 쌍마다
CJUNC_LEN_LAW = 'len_scaled_v0'            # 총 G_j = max(1, L_c/L_par) / R_j,0 (1저자 10-20 밤 Q17 · 분산판 v0 이 k 간선으로 나눈다)
CJUNC_DIST_RULE = 'ceil_Lc_over_Lpar_equal_split_midpoints_nearest_port_v0'   # 10-21 RCA-05 (Q3 (가)) — k 간선 · 각 G/k
CJUNC_PORT_RULE = 'nearest_cell_centre_any_liveness_within_rport_no_relocation_eps_band_tie_lex_ijk_branch_dist_v3'   # 10-21 Q-C
CJUNC_FOOTPRINT_RULE = 'owner_cells_within_D_plus_half_diag_v1'   # 발자국 선분 = instance run 전체 (`_footprint_segs` · B 와 같은 동작)
CJUNC_SELF_RULE = 'same_piece_centreline_pairs_d_le_D_floor_s_gt_D_and_halfpi_d_s_ge_s_min_v3'          # 10-21 Q-B
CJUNC_PIECE_RULE = 'piece_is_fibre_closed_path_seam_continuous_v1'           # 10-21 Q-A — 조각 = 섬유 · 닫힌 경로 이음매 = 연속
CJUNC_SV_CF_KIND = 'counterfactual_cut_sv_bridges_keep_self_v1'              # 10-21 Q-D — 반사실 대조 기록 종류 (옛 counterfactual_cut_sv_faces)
CJUNC_SV_CF_RULE = 'sdcp_component_owner_groups_same_piece_continuity_or_covered_through_cut_nonpassing_v1'
CJUNC_BRANCH_RULE = 'membership_cell_fid_traversal_branch_v1'                 # 위치 = (셀, fid, 그 셀을 지나는 연속 구간)
CJUNC_ORDER_RULE = 'canonical_first_last_then_point_sequence_lex_v2'           # 경로 순서 = 기하 정준 (fid 라벨 무관 · 끝점 먼저)
CJUNC_CP_RULE = 'nearest_pairs_eps_band_lexmin_midpoint_v1'                  # instance 접점 (나란한 접촉 비유일 최근접점)
CJUNC_OWNER_RULE = 'nearest_centreline_eps_band_point_dir_lex_v1'
CJUNC_EPS_D2_UM2 = 1.0e-9                  # J9 집합 규칙 ε 띠 (거리² µm²) — 봉인 (①′ ε_p 와 같은 꼴) · 자기 접합 최근접점 띠도 같은 값
#: L_c ↔ L_par 비교의 **수치** 허용 (상대) — 깊은 직교 교차 (d0 = 0) 의 닿음 길이는 정확히 L_par = 2(r_fi + r_fj) 다.  선분 길이 합의
#:   반올림 (몇 ulp) 이 그 경계를 넘기지 않게 L_c > L_par·(1 + 이 값) 만 긴 접촉 (표지 · 집계) · 그 아래 배율 = 정확히 1 (점 접합과 비트
#:   같게) — 길이 법칙은 경계에서 연속이라 배율 쪽 묶음의 크기는 ≤ 이 값 (1e-9 상대 · 기하 뜻 없음 · 봉인).
CJUNC_LPAR_RTOL = 1.0e-9
RJ_REFERENCE_PLANE = 'model_internal_port_centre'
VGCF_R_UM = 0.075                          # 생산 VGCF Ø0.15 µm (`additives.VGCF_D`)
SDCP_R_UM = 0.15                           # SDCP 1 차 입자 Ø0.30 µm (설계 §5-1)
PTFE_R_UM = 0.124                          # PTFE rope Ø0.248 µm (설계 §3-1 (가) · 규약 선택)
UNREG_LAWS = ('cut', 'fused')
PTFE_JLAWS = ('P0', 'P1')
PTFE_STAMPS = ('off', 'face_alpha', 'centerline')
RJ_OHM_TO_CODE = 1.0e4                     # g_code [S/cm·µm] = 1e4 / R_j [Ω]  (물리 G = 1e−4 · g_code · `iface_code_G_S`)

MODE_EDGE, MODE_CONTRACT, MODE_CUT_P1, MODE_UNREALIZED, MODE_NONE_INF = 1, 2, 3, 4, 5
MODE_NAME = {MODE_EDGE: 'edge', MODE_CONTRACT: 'contract', MODE_CUT_P1: 'cut_p1', MODE_UNREALIZED: 'unrealized',
             MODE_NONE_INF: 'none_inf'}
K_AXIAL, K_VX, K_CUT_SITE, K_CUT_SELF, K_UNREG, K_SELF_FUSED = 1, 2, 3, 4, 5, 6

CJUNC_STATUS = ('mechanism_only — 탄소 접합 R_j v0 (VGCF–VGCF) · 정량 판정 = 등록 R 비준 · Codex GO · S0 문턱 개정 뒤 · '
                'payload 미배선 (B6) · 웹앱 표지 = 봉인 파일 (mpm_lab_register) 이라 보류')
CJUNC_QUALIFIERS = (
    'R_j = 모형 내부 보정값 (재료값 아님 · 포트 = 셀 중심 · 직접 간선에 반셀 · 접근 몫 없음 → 그 몫이 R_j 에 묶인다)',
    'VGCF–VGCF 만 정량 — VGCF–AM · SDCP–VGCF · SDCP–AM 면 = 옛 융합 (SDCP–VGCF 접촉 저항 0 가정)',
    'instance = 중심선 기하 근접 (관통 포함 · MPM 은 섬유 접촉 역학을 풀지 않는다) · 중심선 위치 불확도 = MPM 점 간격',
    'R_j,0 는 모든 VV instance 에 같은 값 · 접합 총 G = max(1, L_c/L_par)/R_j,0 (길이 법칙 v0 — 선 접촉 협착 ∝ 길이의 1차 근사 · '
    '점 접합 L_c/L_par 개 병렬) · 분산판 v0: k = ceil(L_c/L_par) 간선 · 각 G/k · 닿음 구간 k 등분 점의 기하 포트 · 간선마다 PTFE 덮임 · '
    'SDCP 근접 (L_c ≤ L_par = 점 접합 하나) · L_c = 닿음 길이 (중심선 기하 근접) · 분산 간선 = 같은 R_j,0 의 균일 분포 근사 '
    '(접점 저항 분포 · 전달 길이 미검증) · k 가 바뀌는 L_c/L_par 정수 경계에서 σ 가 계단으로 뛴다 (이산화 오차 · 크기 ∝ h·r′/R_j)',
    '조각 = 섬유 — 같은 fid 의 끊긴 조각 (생산 끊기 규칙) 은 서로 다른 섬유와 같은 접합 규칙 (중심선 d ≤ D → R_j) · 닫힌 경로의 '
    '이음매 = 연속 · 자기 접합 = 같은 조각 중심선 쌍 d ≤ D 가 바닥 (s > D · s > (π/2)·d) 을 넘고 s ≥ s_min (s = 쌍의 경로 호 길이) — '
    's < s_min = 같은 가닥의 연속 (접합 아님 · 면 = 옛 융합) · 같은 셀 재방문 = 가지 (연속 구간) 마다 따로 (합치지 않는다 · RCA-03) · '
    's_min = 등록 문턱 (없으면 정량 거부)',
    '덮인 접점 (포트로 고른 셀이 SDCP · PTFE · 상자 밖) = 옮기지 않고 미실현 — 덮은 상의 법칙만 (SDCP = SV 융합 · S3 c · PTFE = '
    'face_alpha P0/P1 · 같은 접촉을 두 번 세지 않는다) · 접합 + PTFE centerline = 거부',
    'S3 c ∈ {0, 1} = 시나리오 끝 (재료 예측 아님 · c = 1 = 근접 접합 축약 끝 · 젖음 상한 아님)',
    'SV_local_dissipation = SV 면 + SDCP 셀 소산 몫 (국소 저항 민감도 진단) — 경로 지배 · 우회 크기 보증 아님 (RCA-06 · 옛 '
    'SV_DOMINANT 표지 철회) · 반사실 대조 (서로 다른 섬유 · 접합으로 갈린 가지를 잇는 SV 다리만 끊고 SDCP 를 지나는 섬유의 자기 '
    '연속은 남긴 판의 단자 G 비) = 선택 노브 · 문턱 = 등록',
)

_TINY = 1.0e-24                            # 퇴화 선분 (길이² µm² · 1e-12 µm 미만)
_SID_NAME = {0: 'void', 1: 'AM_S', 2: 'AM_P', 3: 'VGCF', 4: 'SuperP', 5: 'SDCP', 6: 'SE', 7: 'PTFE', 8: 'SWCNT', 9: 'SE_blk'}


def junction_g_code(R_ohm):
    """접합 간선 코드 컨덕턴스 [S/cm·µm] = 1e4 / R_j [Ω] (설계 §4-1 J5 · 계약 v2 §3-5)."""
    return RJ_OHM_TO_CODE / np.asarray(R_ohm, np.float64)


def sdcp_rj_eff(R0, c, a):
    """S3 — R_j′ = R_j,0 · (1 − c · a_j) (설계 §5-1).  a ∈ {0, 1} · c ∈ [0, 1]."""
    return R0 * (1.0 - c * a)


def junction_len_mult(Lc, L_par):
    """길이 법칙 v0 (`CJUNC_LEN_LAW`) — instance 배율 m = max(1, L_c/L_par) · 접합 g_code = 1e4 · m / R_j.
    L_c ≤ L_par·(1 + `CJUNC_LPAR_RTOL`) = 정확히 1.0 (법칙은 연속 · 묶음 크기 ≤ 1e-9 상대 · 긴 접촉 없는 침대 = 점 접합과 비트 같음 —
    깊은 직교 교차의 L_c 는 L_par 보다 1–3 ulp 클 때가 많다).  NaN L_c = NaN (조용히 1 로 만들지 않는다 · 계획의 불변량이 거부)."""
    r = np.asarray(Lc, np.float64) / float(L_par)
    return np.where(np.isnan(r), np.nan, np.where(r > 1.0 + CJUNC_LPAR_RTOL, r, 1.0))


def _self_is_junction(s_um, s_min_um):
    """꺾임 자기 접합 거르기 — s ≥ s_min = 진짜 접힘 · 고리 접촉 (접합) · s < s_min = 같은 가닥의 연속 (접합 아님)."""
    return np.asarray(s_um, np.float64) >= float(s_min_um)


def _self_floor(s_um, d_um, D):
    """같은 조각 중심선 쌍의 바닥 (★ 10-21 사전 리뷰 PRE-impl-02 · 1저자 Q-B) — s > D (곧은 가닥의 이웃 쌍은 s = d ≤ D) 그리고
    s > (π/2)·d (꺾임 모서리: 꼭짓각 θ 에서 s/d ≤ 1/sin(θ/2) — θ ≥ 79° 이면 ≤ π/2 · 반원 굽힘 s = (π/2)·d 가 경계).  바닥 밖 쌍 =
    어느 s_min 에서도 같은 가닥의 연속 (접합 후보 아님)."""
    s = np.asarray(s_um, np.float64)
    d = np.asarray(d_um, np.float64)
    return (s > float(D)) & (s > 0.5 * math.pi * d)


def _distinct_keep(segs, i, j):
    """서로 다른 섬유 규칙의 선분 쌍 — ★ 10-21 (사전 리뷰 PRE-impl-01 · 1저자 Q-A) 조각이 다르면 (같은 fid 의 끊긴 조각 포함 · 조각 사이엔
    축방향 경로가 없다) 서로 다른 섬유와 같은 규칙 (d ≤ D → R_j · s 규칙 없음).  옛 = fid 가 다를 때만."""
    return segs['piece'][i] != segs['piece'][j]


def _ring_alias(cu, is_ring):
    """닫힌 경로 고리 조각 (★ 10-21 PRE-impl-06 · Q-A) 의 이음매 — 셀 열의 첫 · 끝 셀이 같으면 끝 위치를 첫 위치의 별칭 (한 dof) 으로 둔다
    (이음매 = 연속 · 옛: 첫 · 끝 위치 = 비연속 재방문 → s ≥ s_min 이면 R_j 접합 · 아니면 끊김)."""
    return bool(is_ring and len(cu) >= 2 and np.array_equal(cu[0], cu[-1]))


def _sv_cut_rows(info):
    """SV 반사실 대조가 끊을 SV 면 행 (★ 10-21 사전 리뷰 PRE-impl-04 · 1저자 Q-D · `CJUNC_SV_CF_RULE`) — SDCP 6-면 성분마다 그 성분에 SV 면으로
    닿는 VGCF 주인 위치를 무리 짓는다 (같은 조각 · 연속 (호 간격 = 같은 가닥) 또는 그 사이 위치가 전부 그 성분에 덮인 채 지남).  무리가 둘
    이상 = 다리 (서로 다른 섬유 · 접합으로 갈린 가지를 SV 가 잇는다) → 지나는 무리 (섬유가 그 성분을 지난다 = 자기 연속) 가 하나 이하면
    지나지 않는 무리의 행을 끊는다 · 지나는 무리가 둘 이상이면 못 가른다 (그대로 · 수 기록).  끊기만 = 부분 그래프 → 비 ≥ 1 (Rayleigh).
    info = {'comp': 성분 번호, 'group': 무리 번호, 'passing': 그 무리가 성분을 지나는가} (SV 행마다)."""
    comp, grp, pas = info['comp'], info['group'], info['passing']
    cut = np.zeros(len(comp), bool)
    for c in np.unique(comp):
        m = comp == c
        if len(np.unique(grp[m])) <= 1:
            continue
        if len(np.unique(grp[m & pas])) >= 2:
            continue
        cut |= m & ~pas
    return cut


def _footprint_segs(inst, k):
    """J3 자리 발자국의 선분 — distinct instance k 로 묶인 선분 쌍 run 전체 (d ≤ r_fi + r_fj + tol_ff 인 쌍들의 i · j 선분).
    최근접 쌍만이면 긴 접촉 run 의 나머지 융합 i|j 면이 미등록 법칙 (fused) 으로 남아 lumped 접합 간선을 병렬로 우회한다."""
    return inst['seg_i'][k], inst['seg_j'][k]


# ═════════════════════════ 기하 원시 함수 ═════════════════════════
def _dot(a, b):
    return np.einsum('ij,ij->i', a, b)


def seg_seg_closest(P1, Q1, P2, Q2):
    """선분 P1→Q1 · P2→Q2 최근접 (Ericson 5.1.9 · 퇴화 · 평행 처리) — 배열 (m, 3) → (거리, s, t, C1, C2)."""
    P1 = np.asarray(P1, np.float64).reshape(-1, 3); Q1 = np.asarray(Q1, np.float64).reshape(-1, 3)
    P2 = np.asarray(P2, np.float64).reshape(-1, 3); Q2 = np.asarray(Q2, np.float64).reshape(-1, 3)
    d1 = Q1 - P1; d2 = Q2 - P2; r = P1 - P2
    a = _dot(d1, d1); e = _dot(d2, d2); f = _dot(d2, r); c = _dot(d1, r); bb = _dot(d1, d2)
    m = len(a)
    s = np.zeros(m); t = np.zeros(m)
    z1 = a <= _TINY; z2 = e <= _TINY
    a_ = np.where(z1, 1.0, a); e_ = np.where(z2, 1.0, e)
    k1 = z1 & ~z2
    t[k1] = np.clip(f[k1] / e_[k1], 0.0, 1.0)
    k2 = ~z1 & z2
    s[k2] = np.clip(-c[k2] / a_[k2], 0.0, 1.0)
    g = ~z1 & ~z2
    if g.any():
        den = a * e - bb * bb
        np_ = g & (den > 1.0e-14 * a * e)
        sg = np.zeros(m)
        sg[np_] = np.clip((bb[np_] * f[np_] - c[np_] * e[np_]) / den[np_], 0.0, 1.0)
        tg = (bb * sg + f) / e_
        lo = tg < 0.0; hi = tg > 1.0
        sg = np.where(lo, np.clip(-c / a_, 0.0, 1.0), np.where(hi, np.clip((bb - c) / a_, 0.0, 1.0), sg))
        tg = np.where(lo, 0.0, np.where(hi, 1.0, tg))
        s[g] = sg[g]; t[g] = tg[g]
    C1 = P1 + s[:, None] * d1; C2 = P2 + t[:, None] * d2
    return np.linalg.norm(C1 - C2, axis=1), s, t, C1, C2


def pt_seg_d2(X, A, B):
    """점 X ↔ 선분 A→B 거리² · 최근접점 · 매개 t (배열)."""
    X = np.asarray(X, np.float64).reshape(-1, 3); A = np.asarray(A, np.float64).reshape(-1, 3)
    B = np.asarray(B, np.float64).reshape(-1, 3)
    d = B - A; dd = _dot(d, d)
    t = np.where(dd > _TINY, np.clip(_dot(X - A, d) / np.where(dd > _TINY, dd, 1.0), 0.0, 1.0), 0.0)
    C = A + t[:, None] * d
    w = X - C
    return _dot(w, w), C, t


def _touch_intervals(S0, S1, Q0, Q1, T, ustar):
    """선분 S 위 점 S(u) 의 선분 Q 까지 거리 f(u) (볼록) ≤ T 인 u 구간 [ua, ub] — **안쪽 경계** (이분 60 회 · 길이를 늘리지 않는다).
    f(u*) > T 이면 (nan, nan)."""
    def f(u):
        X = S0 + u[:, None] * (S1 - S0)
        d2, _, _ = pt_seg_d2(X, Q0, Q1)
        return np.sqrt(d2)
    m = len(ustar)
    ua = np.full(m, np.nan); ub = np.full(m, np.nan)
    if m == 0:
        return ua, ub
    ok = f(ustar) <= T
    if not ok.any():
        return ua, ub
    S0o, S1o, Q0o, Q1o, us = S0[ok], S1[ok], Q0[ok], Q1[ok], ustar[ok]

    def fo(u):
        X = S0o + u[:, None] * (S1o - S0o)
        d2, _, _ = pt_seg_d2(X, Q0o, Q1o)
        return np.sqrt(d2)
    z = np.zeros(len(us)); one = np.ones(len(us))
    a_full = fo(z) <= T
    lo = z.copy(); hi = us.copy()
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        ins = fo(mid) <= T
        hi = np.where(ins, mid, hi); lo = np.where(ins, lo, mid)
    la = np.where(a_full, 0.0, hi)
    b_full = fo(one) <= T
    lo = us.copy(); hi = one.copy()
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        ins = fo(mid) <= T
        lo = np.where(ins, mid, lo); hi = np.where(ins, hi, mid)
    lb = np.where(b_full, 1.0, lo)
    ua[ok] = la; ub[ok] = lb
    return ua, ub


def _canon_dir(d):
    """선분 방향 단위 벡터 · 첫 비영 성분이 양수 (정준) — 퇴화 = 0 벡터."""
    n = np.linalg.norm(d, axis=1)
    u = np.where(n[:, None] > 0.0, d / np.where(n > 0.0, n, 1.0)[:, None], 0.0)
    first = np.where(u[:, 0] != 0.0, u[:, 0], np.where(u[:, 1] != 0.0, u[:, 1], u[:, 2]))
    return np.where((first < 0.0)[:, None], -u, u)


def _seq_less(A, B):
    """점열 A < B — 행 단위 사전식 (앞 행이 같으면 다음 행 · 공통 앞부분이 같으면 짧은 쪽).  (n, 3) float."""
    A = np.asarray(A, np.float64).reshape(-1, 3); B = np.asarray(B, np.float64).reshape(-1, 3)
    n = min(len(A), len(B))
    if n:
        ne = np.any(A[:n] != B[:n], axis=1)
        if ne.any():
            i = int(np.argmax(ne))
            for c in range(3):
                if A[i, c] != B[i, c]:
                    return bool(A[i, c] < B[i, c])
    return len(A) < len(B)


def _canon_flip(Q):
    """정준 방향 (`CJUNC_ORDER_RULE`) — 역순 점열이 사전식으로 더 작으면 뒤집는다.  끝점이 다르면 옛 규칙 ('끝점 사전식 작은 쪽에서')
    과 같고 (첫 행 = 두 끝점 비교), 닫힌 경로 (끝점 같음) 도 입력 방향과 무관하게 정해진다 (10-21 RCA-04)."""
    return len(Q) > 1 and _seq_less(np.asarray(Q)[::-1], Q)


def _canonical_paths(paths, P, rej, label):
    """경로 순서 = 기하 정준 (`CJUNC_ORDER_RULE` · 10-21 RCA-04) — 경로마다 정준 방향의 (첫 점, 끝 점, 점열) 사전식 순 (fid 라벨 무관 ·
    재명명 · 반전에 같은 순서 · 끝점이 먼저라 공선 세분에도 같다 — 두 경로가 같은 점에서 시작하면 옛 '점열' 키는 둘째 점이 갈라 세분에
    뒤집혔다 · 10-21 사전 공격 리뷰 RCA04-V).  ⚠ 두 끝점이 다 같은 두 경로 · 닫힌 고리 (끝점 같음) 는 점열이 가른다 (세분 의존 · 남은
    한계).  같은 기하 (역순 포함 · 점 배열은 다름) 둘 = 거부 (정확 중복은 `_paths_of` 의 'duplicate_path' 가 이미 막는다)."""
    keyed = []
    for f, r, kp in paths:
        Q = P[r]
        Qc = Q[::-1] if (kp and _canon_flip(Q)) else Q
        seq = tuple(map(tuple, Qc.tolist()))
        keyed.append(((seq[0], seq[-1], seq), int(f), r, kp))
    keyed.sort(key=lambda t: t[0])
    dup = [[keyed[x][1], keyed[x + 1][1]] for x in range(len(keyed) - 1)
           if keyed[x][0] == keyed[x + 1][0] and P[keyed[x][2]].tobytes() != P[keyed[x + 1][2]].tobytes()]
    if dup:
        rej.append({'code': 'duplicate_path_reversed', 'n': len(dup), 'detail': dup[:8], 'phase': label,
                    'why': '같은 기하 경로 둘 (점 역순 · 정준 점열 같음) — 병합 규칙 미등록 (순서가 fid 에 기댄다)'})
    return [(f, r, kp) for _, f, r, kp in keyed]


def fibre_pieces(Q, gap_tol):
    """같은 끊기 규칙 (`step3_sigma._fibre_segment_ijk` 의 gap_tol × 연속 점 간격 중앙값) → 점 번호 조각 목록.
    ⚠ 복제 (그 함수는 셀만 낸다) — 시험 PIECE 가 셀 집합으로 동등을 대조한다 (다른 판본이 되면 실패)."""
    Q = np.asarray(Q, np.float64)
    ar = np.arange(len(Q))
    if len(Q) < 2:
        return [ar]
    d = np.linalg.norm(np.diff(Q, axis=0), axis=1)
    med = float(np.median(d)) if len(d) else 0.0
    brk = (np.nonzero(d > gap_tol * med)[0] + 1) if med > 0 else np.array([], int)
    return np.split(ar, brk) if len(brk) else [ar]


#: 지문 (RINT-23 · 2026-10-20 2 일 차) — 같은 내용 = 같은 지문 (객체 · 프로세스 무관) · 내용 한 글자 다름 = 다른 지문.
#:   숫자 배열 = dtype · 모양 · C 순서 바이트 (옛 그대로 · 비트 유지) · 객체 배열 = 원소 **내용** 직렬화 (형 표지 · 길이 접두 · UTF-8 ·
#:   C 순서) — 옛 판은 객체 배열의 `x.data` = 원소 **포인터** 바이트를 해시했다 (원장 `instances['reason']` 의 f-문자열 사유 → 같은 입력으로
#:   다시 만든 원장 · 계획 지문이 프로세스 안 · 사이에서 갈렸다 = 거짓 거부).  내용 직렬화가 정의되지 않은 값 (임의 객체 · set — repr 에
#:   주소 · 해시 순서가 들어간다) = TypeError (조용히 주소로 지문을 만들지 않는다).
_FP_OBJ_HEADER = b'objarr-v1'
_FP_SCALARS = (str, bytes, bool, int, float, complex, type(None))
_FP_NP_KINDS = 'biufcSUMm'                 # repr 이 내용만 담는 numpy 스칼라 종류 (객체 'O' · 구조체 'V' 제외)


def _fp_len(b):
    return len(b).to_bytes(8, 'big')


def _fp_obj_item(v):
    """객체 배열 원소 하나 → 내용 바이트 (형 표지 + 길이 접두 · 문자열 = UTF-8 · 실수 = float64 큰 끝 바이트 · 중첩 = 그 `_fp`)."""
    if v is None:
        return b'N'
    if isinstance(v, (bool, np.bool_)):
        return b'T' if bool(v) else b'F'
    if isinstance(v, str):                                   # np.str_ 포함
        b = v.encode('utf-8')
        return b'S' + _fp_len(b) + b
    if isinstance(v, (bytes, bytearray)):                    # np.bytes_ 포함
        b = bytes(v)
        return b'Y' + _fp_len(b) + b
    if isinstance(v, (int, np.integer)):
        b = str(int(v)).encode('ascii')
        return b'I' + _fp_len(b) + b
    if isinstance(v, float) or (isinstance(v, np.floating) and v.dtype.itemsize <= 8):
        return b'R' + struct.pack('>d', float(v))
    if isinstance(v, (list, tuple, dict, np.ndarray)):
        return b'X' + _fp(v).encode('ascii')                 # 고정 길이 (32 hex)
    raise TypeError(f'② 탄소 접합 지문: 객체 배열 원소 형 {type(v).__name__} — 내용 직렬화가 정의되지 않았다 '
                    f'(포인터 · repr 주소로 지문을 만들지 않는다 · RINT-23) — 거부')


def _fp(*parts):
    """원장 · 계획 지문 (E5) — dict (키 정렬) · 목록 · 배열 · 스칼라.  RINT-23 규칙은 위 머리 주석."""
    h = hashlib.blake2b(digest_size=16)
    for p in parts:
        if isinstance(p, dict):
            for k in sorted(p):
                h.update(str(k).encode())
                h.update(_fp(p[k]).encode())
        elif isinstance(p, (list, tuple)):
            h.update(b'(')
            for q in p:
                h.update(_fp(q).encode())
            h.update(b')')
        elif isinstance(p, np.ndarray):
            if p.dtype.hasobject:                            # 객체 (· 구조체 객체 칸) 배열 = 내용 직렬화 (포인터 바이트 아님)
                h.update(_FP_OBJ_HEADER); h.update(repr(p.shape).encode())
                for v in p.reshape(-1, order='C'):
                    h.update(_fp_obj_item(v))
            else:
                x = np.ascontiguousarray(p)
                h.update(x.dtype.str.encode()); h.update(repr(x.shape).encode()); h.update(x.data)
        elif isinstance(p, _FP_SCALARS) or (isinstance(p, np.generic) and p.dtype.kind in _FP_NP_KINDS):
            h.update(repr(p).encode())
        else:
            raise TypeError(f'② 탄소 접합 지문: 값 형 {type(p).__name__} — 내용 직렬화가 정의되지 않았다 (repr 에 주소 · 해시 순서가 '
                            f'들어갈 수 있다 · RINT-23) — 거부')
    return h.hexdigest()


def _grid_fp(a):
    """격자 지문 — `step3_sigma._grid_fp` (사본 금지).  격자는 수치 배열 계약 — 객체 (· 구조체 객체 칸) dtype 격자는 원소 **포인터**
    바이트가 지문에 들어가 재현되지 않으므로 (RINT-23 부류) 넘기기 전에 거부한다."""
    if a is not None and np.asarray(a).dtype.hasobject:
        raise TypeError(f'② 탄소 접합: 격자 지문 — 객체 dtype ({np.asarray(a).dtype}) 격자 거부 (포인터 바이트 · RINT-23 부류 · '
                        f'격자는 수치 배열)')
    import step3_sigma as _s3
    return _s3._grid_fp(a)


# ═════════════════════════ 입력 · 경로 ═════════════════════════
def _input_check(add_pts, add_phase, add_fid, add_kind):
    if add_kind is None:
        raise ValueError('② 탄소 접합: 경로 의미 (`<fibre>_kind.npy`) 없음 — 연속 중심선 (MPM 끝 점 + fibre.npy + kind) 없는 침대 = 거부 '
                         '(점 · 복셀 인접으로 대신하지 않는다 · 설계 §4-2)')
    P = np.asarray(add_pts)
    PH = np.asarray(add_phase); F = np.asarray(add_fid); K = np.asarray(add_kind)
    if P.ndim != 2 or P.shape[1] != 3:
        raise ValueError(f'② 탄소 접합: 점 배열 모양 {P.shape} (N, 3) 이 아니다')
    n = len(P)
    if not (PH.shape == (n,) and F.shape == (n,) and K.shape == (n,)):
        raise ValueError(f'② 탄소 접합: 길이 불일치 — 점 {n} · phase {PH.shape} · fid {F.shape} · kind {K.shape} (조용한 강등 없음 · RIMPR-01)')
    if P.dtype.kind not in 'fiu' or not np.issubdtype(PH.dtype, np.integer) or not np.issubdtype(F.dtype, np.integer) \
            or not np.issubdtype(K.dtype, np.integer):
        raise ValueError('② 탄소 접합: 좌표 = 수치 · phase · fid · kind = 정수 배열 (텍스트 토큰 없음)')
    P = P.astype(np.float64)
    if not np.isfinite(P).all():
        raise ValueError('② 탄소 접합: 좌표 비유한 (NaN · ±inf) — 조립 전 거부 (RIMPR-02 · 04)')
    return P, PH.astype(np.int64), F.astype(np.int64), K.astype(np.int64)


def _paths_of(P, PH, F, K, phase, rej, label):
    """phase 의 fid 마다 행 (붙어 있어야 한다 · 정확 중복 경로 = 거부)."""
    out = []
    m = PH == phase
    if not m.any():
        return out
    sig = {}
    nc, mixed = [], []
    for f in np.unique(F[m]):
        r = np.flatnonzero(F == f)
        if not np.all(PH[r] == phase):
            mixed.append(int(f))
            r = r[PH[r] == phase]
        if len(r) > 1 and np.any(np.diff(r) != 1):
            nc.append(int(f))
        kind_path = bool(np.all(K[r] == 1))
        key = (len(r), P[r].tobytes())
        sig.setdefault(key, []).append(int(f))
        out.append((int(f), r, kind_path))
    if nc:
        rej.append({'code': 'fid_noncontiguous', 'test': 'S0-5', 'n': len(nc), 'detail': nc[:8], 'phase': label,
                    'why': '같은 fid 의 행이 떨어진 두 블록 — 경로 순서가 모호 (설계 §2 ③ · §3-3)'})
    if mixed:
        rej.append({'code': 'fid_phase_mixed', 'n': len(mixed), 'detail': mixed[:8], 'phase': label,
                    'why': '한 fid 가 두 상에 걸친다 (전역 고유 fid 규약 위반)'})
    dup = [v for v in sig.values() if len(v) > 1]
    if dup:
        rej.append({'code': 'duplicate_path', 'n': len(dup), 'detail': dup[:8], 'phase': label,
                    'why': '정확 중복 경로 (점 배열 비트 같음) — 병합 규칙 미등록'})
    return out


def _closed_path(Q, kind_path):
    """닫힌 경로 (`CJUNC_PIECE_RULE`) — 경로 (kind 1) · 점 셋 이상 · 첫 점 = 끝 점 (좌표 비트 같음).  반올림으로 조금 떨어진 두 끝은 닫힌 것이
    아니다 (열린 경로의 두 끝이 만나는 접촉 = 같은 조각 쌍의 s 규칙)."""
    return bool(kind_path and len(Q) >= 3 and np.array_equal(Q[0], Q[-1]))


def _segments_of(paths, P, gap_tol):
    """경로 → 조각 (정준 방향) → 선분 표.  → dict(arrays) · 조각마다 (fid, 점 배열, kind_path).
    arc_a · arc_b = 선분 두 끝의 **조각 호 좌표** (꺾임 자기 접합 s) — 조각마다 그 조각의 저장 방향 (정준) 으로 연속 점 거리를 누적 ·
    점 역순 입력에서도 같은 비트.  선분 위 호 좌표 = arc_a + t·(arc_b − arc_a).
    ★ 10-21 (사전 리뷰 PRE-impl-01 · 1저자 Q-A) — 다른 조각 = 다른 섬유 (경로로 이어지지 않는다) → 호 좌표는 조각 안에서만 뜻이 있다
    (옛: fid 경로 전체 누적 · 조각 사이 간격 현 포함 = 끊긴 두 조각을 '같은 가닥의 연속' 으로 읽었다).
    ★ 닫힌 경로 (PRE-impl-06 · Q-A — 이음매 = 연속): 끊김이 있으면 마지막 조각 + 첫 조각을 이음매를 지나 한 조각으로 잇는다 (열린 조각 ·
    이음매는 조각 안 · 'piece_closed' 1) · 끊김이 없으면 고리 조각 하나 (`ring_L` = 고리 길이 > 0 · s = 고리 위 짧은 쪽 호 · 'piece_closed' 2 ·
    위치 첫 · 끝 = 이음매 = `_positions` 가 한 dof (별칭) 또는 축방향 이웃으로 잇는다).  끊김 판정은 원래 점열 그대로 (`fibre_pieces` — 생산
    스탬프와 같은 끊김 · 멤버십 셀 집합 불변).  조각마다 칸 (선분 표와 길이가 다름): piece_closed · piece_L."""
    sP0, sP1, sfid, spiece, sk, sa0, sa1, sring = [], [], [], [], [], [], [], []
    pieces = []
    pclosed, pL = [], []
    for f, r, kind_path in paths:
        Q = P[r]
        flip = bool(kind_path and _canon_flip(Q))
        Qc = Q[::-1] if flip else Q
        #  ★ 10-21 (RCA-04) — 조각 = 정준 방향 경로 (Qc) 의 순서 (옛: 입력 방향 순서 → 점 역순이 조각 번호 · 위치 순서를 바꿨다)
        ixs = fibre_pieces(Qc, gap_tol) if kind_path else [np.arange(len(Q))]
        closed = _closed_path(Qc, kind_path)
        ring_whole = bool(closed and len(ixs) == 1)
        joined = bool(closed and len(ixs) >= 2)
        if joined:                                           # 이음매를 지나 마지막 + 첫 조각을 잇는다 (Qc[−1] = Qc[0] — 점 하나 빼고)
            ixs = list(ixs[1:-1]) + [np.r_[ixs[-1], ixs[0][1:]].astype(np.int64)]
        for x_, ix in enumerate(ixs):
            R = Qc[ix]
            if kind_path and len(R) > 1 and _canon_flip(R):
                R = R[::-1]
            gp = len(pieces)
            pieces.append((f, R, kind_path))
            if len(R) == 1 or not kind_path:
                A = R; B = R                                  # 점 = 퇴화 선분 (경로 아닌 fid 도 점마다)
                a0 = np.zeros(len(R)); a1 = np.zeros(len(R))
                L_ring = 0.0
                Lp = 0.0
            else:
                A = R[:-1]; B = R[1:]
                cum = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(R, axis=0), axis=1))]
                a0 = cum[:-1]; a1 = cum[1:]
                Lp = float(cum[-1])
                L_ring = Lp if ring_whole else 0.0
            pclosed.append(2 if ring_whole else (1 if (joined and x_ == len(ixs) - 1) else 0))
            pL.append(Lp)
            sP0.append(A); sP1.append(B); sa0.append(a0); sa1.append(a1)
            sfid.append(np.full(len(A), f)); spiece.append(np.full(len(A), gp)); sk.append(np.arange(len(A)))
            sring.append(np.full(len(A), L_ring))
    if not pieces:
        z = np.zeros((0, 3))
        return {'P0': z, 'P1': z.copy(), 'fid': np.zeros(0, np.int64), 'piece': np.zeros(0, np.int64),
                'k': np.zeros(0, np.int64), 'arc_a': np.zeros(0), 'arc_b': np.zeros(0), 'ring_L': np.zeros(0),
                'piece_closed': np.zeros(0, np.int64), 'piece_L': np.zeros(0)}, pieces
    return {'P0': np.vstack(sP0), 'P1': np.vstack(sP1), 'fid': np.concatenate(sfid).astype(np.int64),
            'piece': np.concatenate(spiece).astype(np.int64), 'k': np.concatenate(sk).astype(np.int64),
            'arc_a': np.concatenate(sa0).astype(np.float64), 'arc_b': np.concatenate(sa1).astype(np.float64),
            'ring_L': np.concatenate(sring).astype(np.float64), 'piece_closed': np.asarray(pclosed, np.int64),
            'piece_L': np.asarray(pL, np.float64)}, pieces


def _positions(pieces, segs, lo, vox, n, sid):
    """조각 → 셀 열 (연속 중복 제거 · 정준 방향 번호) = 멤버십 위치.  생산 스탬프와 같은 원시 함수 (`segment_cells`) · 같은 셀.
    ★ 10-21 (Q-A · PRE-impl-06) — 고리 조각 (닫힌 경로 · 끊김 없음): 셀 열의 첫 · 끝 셀이 같으면 끝 위치 = 첫 위치의 별칭 ('alias' = 목표
    위치 · 조립기가 같은 dof · 비연속 재방문 아님) · 첫 · 끝 셀이 면으로 이웃이면 축방향 이웃 (면 표가 'ring' · 'piece_ng' 로 둘레를 잇는다)."""
    from fibre_segment_raster import segment_cells
    pf, pp, pk, plin, pijk, ps0, ps1, pal, prg, png = [], [], [], [], [], [], [], [], [], []
    seg_base = 0
    piece_pos = []
    npos = 0                                                 # 지금까지 위치 수 (조각마다 [시작, 끝) — 누적 · O(조각))
    ring_p = np.asarray(segs.get('piece_closed', np.zeros(len(pieces), np.int64)), np.int64) == 2
    for gp, (f, R, kind_path) in enumerate(pieces):
        nseg = 1 if (len(R) == 1 or not kind_path) else len(R) - 1
        if not kind_path:
            seg_base += len(R)
            piece_pos.append((npos, npos))
            continue
        if len(R) == 1:
            cells = np.floor((R - lo) / vox).astype(np.int64)
            sidx = np.zeros(1, np.int64)
        else:
            cl, si = [], []
            for i in range(len(R) - 1):
                c = segment_cells(R[i] - lo, R[i + 1] - lo, vox)
                cl.append(c); si.append(np.full(len(c), i))
            cells = np.vstack(cl).astype(np.int64); sidx = np.concatenate(si)
        new = np.ones(len(cells), bool)
        new[1:] = np.any(cells[1:] != cells[:-1], axis=1)
        grp = np.cumsum(new) - 1
        ng = int(grp[-1]) + 1
        cu = cells[new]
        s0 = np.full(ng, np.iinfo(np.int64).max); s1 = np.full(ng, -1)
        np.minimum.at(s0, grp, sidx); np.maximum.at(s1, grp, sidx)
        inb = ((cu >= 0) & (cu < n)).all(1)
        lin = np.full(ng, -1, np.int64)
        lin[inb] = np.ravel_multi_index(tuple(cu[inb].T), tuple(n))
        is_ring = bool(gp < len(ring_p) and ring_p[gp])
        al = np.full(ng, -1, np.int64)
        if _ring_alias(cu, is_ring):
            al[ng - 1] = npos                                 # 끝 위치 → 첫 위치 (전역 위치 번호)
        pf.append(np.full(ng, f)); pp.append(np.full(ng, gp)); pk.append(np.arange(ng)); plin.append(lin)
        pijk.append(cu); ps0.append(s0 + seg_base); ps1.append(s1 + seg_base)
        pal.append(al); prg.append(np.full(ng, is_ring)); png.append(np.full(ng, ng))
        piece_pos.append((npos, npos + ng))
        npos += ng
        seg_base += nseg
    if pf:
        pos = {'fid': np.concatenate(pf).astype(np.int64), 'piece': np.concatenate(pp).astype(np.int64),
               'k': np.concatenate(pk).astype(np.int64), 'lin': np.concatenate(plin).astype(np.int64),
               'ijk': np.vstack(pijk).astype(np.int64), 's0': np.concatenate(ps0).astype(np.int64),
               's1': np.concatenate(ps1).astype(np.int64), 'alias': np.concatenate(pal).astype(np.int64),
               'ring': np.concatenate(prg).astype(bool), 'piece_ng': np.concatenate(png).astype(np.int64)}
    else:
        z = np.zeros(0, np.int64)
        pos = {'fid': z, 'piece': z.copy(), 'k': z.copy(), 'lin': z.copy(), 'ijk': np.zeros((0, 3), np.int64),
               's0': z.copy(), 's1': z.copy(), 'alias': z.copy(), 'ring': np.zeros(0, bool), 'piece_ng': z.copy()}
    flat = np.asarray(sid).reshape(-1)
    pos['live'] = (pos['lin'] >= 0) & (flat[np.maximum(pos['lin'], 0)] == 3)
    return pos, piece_pos


def _owner_select(qid, pid, X, pos, segs, nq):
    """J9 집합 규칙 — 질의마다 후보 위치 중 중심선 최근접 (거리² ε 띠 · 정준 키 = 최근접점 → 방향 → (fid, 조각, 번호)).
    qid/pid = 후보 쌍 (질의 번호 · 위치 번호) · X = 질의 점 (nq, 3).  → owner (nq,) · 정준 키 못 가른 수."""
    owner = np.full(nq, -1, np.int64)
    if len(qid) == 0:
        return owner, 0
    cnt = pos['s1'][pid] - pos['s0'][pid] + 1
    rq = np.repeat(np.arange(len(qid)), cnt)
    off = np.arange(len(rq)) - np.repeat(np.cumsum(cnt) - cnt, cnt)
    sg = np.repeat(pos['s0'][pid], cnt) + off
    d2, C, _ = pt_seg_d2(X[qid[rq]], segs['P0'][sg], segs['P1'][sg])
    order = np.lexsort((d2, rq))
    first = np.ones(len(order), bool); first[1:] = rq[order][1:] != rq[order][:-1]
    best = order[first]                                      # 쌍마다 최근접 선분
    bd2 = d2[best]; bC = C[best]; bdir = _canon_dir(segs['P1'][sg[best]] - segs['P0'][sg[best]])
    q = qid; p = pid
    dmin = np.full(nq, np.inf)
    np.minimum.at(dmin, q, bd2)
    band = bd2 <= dmin[q] + CJUNC_EPS_D2_UM2
    #  ★ 10-21 (RCA-04) — 마지막 대체 키 = 정준 (조각, 번호) 만 (fid 라벨 없음 · 조각 번호 = 기하 정준 경로 순서)
    keys = (pos['k'][p], pos['piece'][p], bdir[:, 2], bdir[:, 1], bdir[:, 0], bC[:, 2], bC[:, 1], bC[:, 0], ~band, q)
    o = np.lexsort(keys)
    fq = np.ones(len(o), bool); fq[1:] = q[o][1:] != q[o][:-1]
    owner[q[o][fq]] = p[o][fq]
    # 정준 키 (점 · 방향) 가 못 가른 띠 안 동률 = (조각, 번호) 대체 — 수만 센다 (질의마다 첫째 · 둘째 후보)
    tie = 0
    sec = np.flatnonzero(~fq)
    if len(sec):
        prev = sec - 1
        qo = q[o]; bo = band[o]
        geo = np.c_[bC[o], bdir[o]]
        tie = int(np.sum(fq[prev] & (qo[sec] == qo[prev]) & bo[sec] & bo[prev] & np.all(geo[sec] == geo[prev], axis=1)))
    return owner, tie


class _UF:
    def __init__(self):
        self.p = {}

    def find(self, x):
        p = self.p
        p.setdefault(x, x)
        r = x
        while p[r] != r:
            r = p[r]
        while p[x] != r:
            p[x], x = r, p[x]
        return r

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            if rb < ra:
                ra, rb = rb, ra
            self.p[rb] = ra


# ═════════════════════════ 원장 (기하만) ═════════════════════════
def cjunc_registry(sid, box_lo, vox, add_pts, add_phase, add_fid, add_kind, *, r_f_um, tol_ff_um, L_par_um, r_port_um,
                   s_min_um, gap_tol=2.0, tol_P_um=None, tol_sj_um=None, r_ptfe_um=PTFE_R_UM, r_sdcp_um=SDCP_R_UM):
    """② 탄소 접합 원장 — **기하만** (σ · 전류 없음).  문턱 = 식 고정 · 숫자 = S0 단계 1 (설계 §4-1 · R §2-1) — 기본값을 두지 않는다
    (r_f · tol_ff · L_par · r_port · s_min 필수).  tol_P · tol_sj 기본 = tol_ff (설계: 한 숫자).  → dict (지문 포함).
    s_min_um = 꺾임 자기 접합 거르기 문턱 (경로 호 길이 µm) — None = 미등록 (구조화 거부 `self_s_min_missing` · 정량 계획이 막는다 ·
    시험 모드는 거르지 않고 진행 · 표지 `off_s_min_missing` · 바닥은 늘 적용).
    ★ 10-21 (사전 리뷰 impl · 1저자 Q-A–Q-D): 조각 = 섬유 (끊긴 조각 = 서로 다른 섬유 규칙 · 닫힌 경로 이음매 = 연속) · 자기 접합 = 같은
    조각 중심선 쌍 (d ≤ D · 바닥 · 쌍마다 s 규칙) · 포트 = 옮기지 않음 (덮였으면 미실현) · SV 반사실 대조 = 다리 SV 면만 끊는 표지 ('sv_cut')."""
    sid = np.asarray(sid)
    if sid.ndim != 3:
        raise ValueError('② 탄소 접합: sid 는 3 차원 격자')
    vox = float(vox)
    lo = np.asarray(box_lo, np.float64).reshape(3)
    if not (math.isfinite(vox) and vox > 0.0 and np.isfinite(lo).all()):
        raise ValueError(f'② 탄소 접합: vox · 상자 원점 유한 (vox > 0) — {vox!r} {lo!r}')
    thr = {'r_f_um': r_f_um, 'tol_ff_um': tol_ff_um, 'L_par_um': L_par_um, 'r_port_um': r_port_um, 'gap_tol': gap_tol,
           'tol_P_um': tol_ff_um if tol_P_um is None else tol_P_um, 'tol_sj_um': tol_ff_um if tol_sj_um is None else tol_sj_um,
           'r_ptfe_um': r_ptfe_um, 'r_sdcp_um': r_sdcp_um}
    for k_, v_ in thr.items():
        if isinstance(v_, bool) or not isinstance(v_, (int, float, np.floating, np.integer)) or not math.isfinite(float(v_)) \
                or float(v_) < 0.0:
            raise ValueError(f'② 탄소 접합: 문턱 {k_} = {v_!r} — 유한한 0 이상 실수 (R §2-1 · 숫자 = S0 단계 1)')
    thr = {k_: float(v_) for k_, v_ in thr.items()}
    if thr['r_f_um'] <= 0.0 or thr['gap_tol'] <= 0.0:
        raise ValueError('② 탄소 접합: r_f · gap_tol > 0')
    if thr['L_par_um'] <= 0.0:
        raise ValueError('② 탄소 접합: L_par > 0 (길이 법칙 v0 의 분모 · 배율 = max(1, L_c/L_par))')
    if s_min_um is not None and (isinstance(s_min_um, bool) or not isinstance(s_min_um, (int, float, np.floating, np.integer))
                                 or not math.isfinite(float(s_min_um)) or float(s_min_um) < 0.0):
        raise ValueError(f'② 탄소 접합: s_min = {s_min_um!r} — None (미등록 · 정량 거부) 또는 유한한 0 이상 실수 '
                         f'(꺾임 자기 접합 경로 호 길이 µm · 숫자 = S0 단계 1 뒤 R §2-1)')
    thr['s_min_um'] = None if s_min_um is None else float(s_min_um)
    P, PH, F, K = _input_check(add_pts, add_phase, add_fid, add_kind)
    n = np.array(sid.shape, np.int64)
    rej = []
    vg_paths = _paths_of(P, PH, F, K, 2, rej, 'VGCF')
    nonpath = [f for f, _, kp in vg_paths if not kp]
    if nonpath:
        rej.append({'code': 'vgcf_nonpath_fid', 'n': len(nonpath), 'detail': nonpath[:8],
                    'why': 'VGCF fid 가 경로 (kind 1) 가 아니다 — 점 스탬프 VGCF 는 중심선이 없다 (설계 §4-2 · 거부)'})
    vg_paths_ok = _canonical_paths([(f, r, kp) for f, r, kp in vg_paths if kp], P, rej, 'VGCF')   # ★ 10-21 RCA-04 기하 정준 순서
    segs, pieces = _segments_of(vg_paths_ok, P, thr['gap_tol'])
    pos, piece_pos = _positions(pieces, segs, lo, vox, n, sid)
    flat = sid.reshape(-1)
    # 위치 정렬 (셀 → 멤버십 · 정준 순서) · 주 위치 (셀의 기본 dof) — 10-21: (셀, 조각, 번호) 만 (fid 라벨 없음 · RCA-04)
    live = np.flatnonzero(pos['live'])
    o = live[np.lexsort((pos['k'][live], pos['piece'][live], pos['lin'][live]))]
    primary = np.zeros(len(pos['lin']), bool)
    if len(o):
        fl = np.ones(len(o), bool); fl[1:] = pos['lin'][o][1:] != pos['lin'][o][:-1]
        primary[o[fl]] = True
    pos['primary'] = primary
    cell_lin, cell_cnt = (np.unique(pos['lin'][o], return_counts=True) if len(o) else
                          (np.zeros(0, np.int64), np.zeros(0, np.int64)))
    cell_ptr = np.r_[0, np.cumsum(cell_cnt)].astype(np.int64)
    cell_pos = o
    s3cells = np.flatnonzero(flat == 3)
    orphan = np.setdiff1d(s3cells, cell_lin, assume_unique=False)
    if len(orphan):
        rej.append({'code': 'vgcf_orphan_cells', 'n': int(len(orphan)),
                    'why': '멤버십 없는 VGCF 셀 (점 스탬프 · SDCP–VGCF 브리지 진단 팔 · 다른 입력) — 정량 거부'})
    n_extra = int(np.sum(pos['live'] & ~primary & (pos['alias'] < 0)))   # ★ 고리 이음매 별칭 = 목표 위치의 dof (새 dof 아님)

    def _cell_positions(lins):
        """셀 선형 번호들 → (질의 번호, 위치 번호) 쌍 (그 셀의 살아있는 위치 전부)."""
        j = np.searchsorted(cell_lin, lins)
        okj = (j < len(cell_lin))
        okj[okj] = cell_lin[j[okj]] == lins[okj]
        q = np.flatnonzero(okj)
        a0 = cell_ptr[j[q]]; cnt = cell_ptr[j[q] + 1] - a0
        qq = np.repeat(q, cnt)
        off = np.arange(len(qq)) - np.repeat(np.cumsum(cnt) - cnt, cnt)
        return qq, cell_pos[np.repeat(a0, cnt) + off]

    # ── distinct-fiber instances (J2a · J2c · ★ 10-21 Q-A: 조각이 다르면 — 같은 fid 의 끊긴 조각 포함) ──
    rf = thr['r_f_um']
    D = 2.0 * rf + thr['tol_ff_um']
    T_touch = 2.0 * rf
    inst = _distinct_instances(segs, D, T_touch)
    # ── 자기 접합 (★ 10-21 Q-B — 같은 조각 중심선 쌍 · 바닥 · 쌍마다 s 규칙) ──
    sp = _self_pairs(segs, D, thr['s_min_um'])
    selfinst = _self_instances(sp, segs, T_touch)
    cgroups = _pair_groups(sp['i'], sp['j'], segs, np.ones(len(sp['i']), bool))   # 후보 무리 (바닥 쌍) — census
    nD = len(inst['fi'])
    nSf = len(selfinst['fi'])
    # ── 면 표 ──
    stride = np.array([n[1] * n[2], n[2], 1], np.int64)
    rows_lin, rows_ax, rows_kind, rows_pa, rows_pb, rows_inst = [], [], [], [], [], []
    contact = []                                             # (lin_a, ax, oa, ob)
    owner_ties = 0
    for ax in range(3):
        sa = [slice(None)] * 3; sb = [slice(None)] * 3
        sa[ax] = slice(0, -1); sb[ax] = slice(1, None)
        g3 = sid[tuple(sa)] == 3; h3 = sid[tuple(sb)] == 3
        cand = g3 | h3
        if not cand.any():
            continue
        ii = np.nonzero(cand)
        la = np.ravel_multi_index(ii, tuple(n)).astype(np.int64)
        lb = la + stride[ax]
        fc = lo + (np.stack(ii, 1).astype(np.float64) + 0.5) * vox
        fc[:, ax] += 0.5 * vox                               # 면 중심
        qa, pa_all = _cell_positions(la)
        qb, pb_all = _cell_positions(lb)
        has_a = np.zeros(len(la), bool); has_a[qa] = True
        has_b = np.zeros(len(lb), bool); has_b[qb] = True
        # 축방향 쌍 (같은 fid · 조각 · 번호 차 1 · ★ 10-21 고리 조각 = 둘레 (첫 ↔ 끝) 도)
        vv = has_a & has_b
        axial_face = np.zeros(len(la), bool)
        if vv.any():
            # 면마다 a 위치 × b 위치 펼치기
            ca = np.bincount(qa, minlength=len(la)); cb = np.bincount(qb, minlength=len(la))
            sa_ = np.r_[0, np.cumsum(ca)]; sb_ = np.r_[0, np.cumsum(cb)]
            fv = np.flatnonzero(vv)
            na = ca[fv]; nb = cb[fv]
            rep = na * nb
            face_r = np.repeat(fv, rep)
            off = np.arange(len(face_r)) - np.repeat(np.cumsum(rep) - rep, rep)
            ia = off // np.repeat(nb, rep); ib = off % np.repeat(nb, rep)
            PA = pa_all[np.argsort(qa, kind='stable')][sa_[face_r] + ia]
            PB = pb_all[np.argsort(qb, kind='stable')][sb_[face_r] + ib]
            dkk = np.abs(pos['k'][PA] - pos['k'][PB])
            wrap = pos['ring'][PA] & (dkk == pos['piece_ng'][PA] - 1) & (pos['piece_ng'][PA] > 2)
            isax = (pos['fid'][PA] == pos['fid'][PB]) & (pos['piece'][PA] == pos['piece'][PB]) & ((dkk == 1) | wrap)
            if isax.any():
                axial_face[face_r[isax]] = True
                rows_lin.append(la[face_r[isax]]); rows_ax.append(np.full(int(isax.sum()), ax))
                rows_kind.append(np.full(int(isax.sum()), K_AXIAL)); rows_pa.append(PA[isax]); rows_pb.append(PB[isax])
                rows_inst.append(np.full(int(isax.sum()), -1))
        # 접촉 면 (VV · 축방향 쌍 없음) · VX 면 (한쪽만 멤버십)
        need_a = (has_a & ~axial_face)
        need_b = (has_b & ~axial_face)
        sel_a = np.isin(qa, np.flatnonzero(need_a)); sel_b = np.isin(qb, np.flatnonzero(need_b))
        oa, ta = _owner_select(qa[sel_a], pa_all[sel_a], fc, pos, segs, len(la))
        ob, tb = _owner_select(qb[sel_b], pb_all[sel_b], fc, pos, segs, len(la))
        owner_ties += ta + tb
        cf = np.flatnonzero(vv & ~axial_face)
        for i in cf:
            contact.append((int(la[i]), ax, int(oa[i]), int(ob[i]), fc[i]))
        vx = np.flatnonzero(has_a ^ has_b)                    # 한쪽만 멤버십 (VGCF ↔ 비탄소 · 고아 VGCF 셀) — 축방향일 수 없다
        if len(vx):
            rows_lin.append(la[vx]); rows_ax.append(np.full(len(vx), ax)); rows_kind.append(np.full(len(vx), K_VX))
            rows_pa.append(np.where(has_a[vx], oa[vx], -1)); rows_pb.append(np.where(has_b[vx], ob[vx], -1))
            rows_inst.append(np.full(len(vx), -1))
    # ── 접촉 면 분류 (★ 10-21 Q-A · Q-B): 다른 조각 = 접합 자리 절단 (서로 다른 섬유 instance 발자국) · 미등록 /
    #    같은 조각 = 연속 (바닥 밖 · s < s_min) 이면 옛 융합 · 아니면 자기 instance 발자국 = 절단 · 미등록 ──
    D_fp = D + math.sqrt(3.0) * 0.5 * vox
    by_pair = {}
    for k in range(nD):
        by_pair.setdefault((int(inst['piece_i'][k]), int(inst['piece_j'][k])), []).append(k)
    by_self = {}
    for q in range(nSf):
        by_self.setdefault(int(selfinst['piece_i'][q]), []).append(q)
    n_cut_site = 0
    n_unreg = 0
    multi_site = 0
    n_self_fused = 0
    self_face_n = np.zeros(nSf, np.int64)

    def _near(c, segset):
        return float(np.sqrt(np.min(pt_seg_d2(np.repeat(c[None], len(segset), 0), segs['P0'][segset], segs['P1'][segset])[0])))

    for (lin_a, ax, oa_, ob_, fcen) in contact:
        if oa_ < 0 or ob_ < 0:
            continue
        pa_, pb_ = int(pos['piece'][oa_]), int(pos['piece'][ob_])
        ca = lo + (np.array(np.unravel_index(lin_a, tuple(n)), np.float64) + 0.5) * vox
        cb_ = ca.copy(); cb_[ax] += vox
        if pa_ == pb_:
            s_f, d_f = _pos_pair_sd(oa_, ob_, pos, segs, lo, vox)
            if bool(np.asarray(_continuity(s_f, d_f, D, thr['s_min_um']))):
                rows_lin.append(np.array([lin_a])); rows_ax.append(np.array([ax])); rows_kind.append(np.array([K_SELF_FUSED]))
                rows_pa.append(np.array([oa_])); rows_pb.append(np.array([ob_])); rows_inst.append(np.array([-1]))
                n_self_fused += 1
                continue
            best, bestd = -1, math.inf
            for q in by_self.get(pa_, ()):
                Si, Sj = _footprint_segs(selfinst, q)
                for A_, B_ in ((Si, Sj), (Sj, Si)):
                    da = _near(ca, B_); db = _near(cb_, A_)
                    if da <= D_fp and db <= D_fp and da + db < bestd:
                        best, bestd = q, da + db
            if best >= 0:
                rows_lin.append(np.array([lin_a])); rows_ax.append(np.array([ax])); rows_kind.append(np.array([K_CUT_SELF]))
                rows_pa.append(np.array([oa_])); rows_pb.append(np.array([ob_])); rows_inst.append(np.array([nD + best]))
                self_face_n[best] += 1
            else:
                rows_lin.append(np.array([lin_a])); rows_ax.append(np.array([ax])); rows_kind.append(np.array([K_UNREG]))
                rows_pa.append(np.array([oa_])); rows_pb.append(np.array([ob_])); rows_inst.append(np.array([-1]))
                n_unreg += 1
            continue
        key = (min(pa_, pb_), max(pa_, pb_))
        best, bestd = -1, math.inf
        nmatch = 0
        for k in by_pair.get(key, ()):
            Si, Sj = _footprint_segs(inst, k)                # run 전체 (긴 접촉 = lumped 간선 · run 위 면이 남으면 우회)
            seg_of_fa = Si if int(inst['piece_i'][k]) == pa_ else Sj
            seg_of_fb = Sj if int(inst['piece_i'][k]) == pa_ else Si
            da = _near(ca, seg_of_fb)
            db = _near(cb_, seg_of_fa)
            if da <= D_fp and db <= D_fp:
                nmatch += 1
                if da + db < bestd:
                    best, bestd = k, da + db
        if best >= 0:
            multi_site += int(nmatch > 1)
            rows_lin.append(np.array([lin_a])); rows_ax.append(np.array([ax])); rows_kind.append(np.array([K_CUT_SITE]))
            rows_pa.append(np.array([oa_])); rows_pb.append(np.array([ob_])); rows_inst.append(np.array([best]))
            n_cut_site += 1
        else:
            rows_lin.append(np.array([lin_a])); rows_ax.append(np.array([ax])); rows_kind.append(np.array([K_UNREG]))
            rows_pa.append(np.array([oa_])); rows_pb.append(np.array([ob_])); rows_inst.append(np.array([-1]))
            n_unreg += 1
    # ── 같은 셀 비연속 재방문 (같은 조각 · 별칭 짝 아님 · 가지마다 따로 · 합치지 않음 · RCA-03) — census · 경로로만 쌍 ──
    jset = set(zip(sp['i'][sp['junc']].tolist(), sp['j'][sp['junc']].tolist()))
    rv, rv_s = [], []
    for c_i in range(len(cell_lin)):
        mem = cell_pos[cell_ptr[c_i]:cell_ptr[c_i + 1]]
        if len(mem) < 2:
            continue
        for x in range(len(mem)):
            for y in range(x + 1, len(mem)):
                p, q = int(mem[x]), int(mem[y])
                if pos['piece'][p] != pos['piece'][q] or int(pos['alias'][p]) == q or int(pos['alias'][q]) == p:
                    continue
                dk_ = abs(int(pos['k'][p]) - int(pos['k'][q]))
                if pos['ring'][p]:
                    dk_ = min(dk_, int(pos['piece_ng'][p]) - dk_)
                if dk_ < 2:
                    continue
                rv.append((p, q, int(cell_lin[c_i])))
                rv_s.append(_pos_pair_sd(p, q, pos, segs, lo, vox)[0])

    def _covered(p, q):
        return any((a, b) in jset or (b, a) in jset for a in range(int(pos['s0'][p]), int(pos['s1'][p]) + 1)
                   for b in range(int(pos['s0'][q]), int(pos['s1'][q]) + 1))

    path_only, path_broken = [], 0
    for (p, q, _l) in rv:
        if _covered(p, q):
            continue
        a0_, a1_ = sorted((p, q))
        if np.all(pos['live'][a0_:a1_ + 1]):
            path_only.append((p, q))                          # 경로 (같은 조각 살아있는 위치 사슬) 로만 이어진다
        else:
            path_broken += 1                                  # 사이에 덮인 위치 — 경로도 끊김 (SV · 다른 상 법칙만)
    # ── 자기 접합 census (후보 = 바닥 쌍 무리 · 남은 = 접합 instance · 거른 = 접합 쌍 없는 후보 무리) ──
    ncand = len(cgroups)
    cs = np.asarray([float(sp['s'][_group_cp(m, sp)]) for m in cgroups], np.float64)
    nfilt = int(sum(1 for m in cgroups if not sp['junc'][m].any()))
    if thr['s_min_um'] is None:
        self_filter = 'off_s_min_missing'
        rej.append({'code': 'self_s_min_missing', 'test': 'J8-self', 'n': int(ncand),
                    'why': 's_min (꺾임 자기 접합 거르기 · 경로 호 길이) 미등록 — 숫자 = S0 단계 1 의 분포를 본 뒤 등록 R §2-1 개정 · '
                           '기본값 없음 (시험 모드 = 거르지 않고 진행 · 바닥은 늘 적용)'})
    else:
        self_filter = 'applied'
    rv_s = np.asarray(rv_s, np.float64)
    rv_s = rv_s[np.isfinite(rv_s)]
    self_census = {'self_filter': self_filter, 'n_self_candidates': int(ncand), 'n_self_kept': int(nSf),
                   'n_self_filtered': int(nfilt), 'n_self_s_undefined': 0,
                   'n_self_fused_faces': int(n_self_fused), 'n_self_revisits_path_only': int(len(path_only)),
                   'n_self_revisits_path_broken': int(path_broken),
                   'self_s_um': ({'min': float(cs.min()), 'median': float(np.median(cs)), 'max': float(cs.max())}
                                 if len(cs) else None),
                   'n_revisit_pairs': int(len(rv)),
                   'n_revisit_cells': int(len({x[2] for x in rv})),
                   'n_revisit_fibres': int(len({int(pos['fid'][x[0]]) for x in rv})),
                   'revisit_s_um': ({'n': int(len(rv_s)), 'min': float(rv_s.min()), 'median': float(np.median(rv_s)),
                                     'max': float(rv_s.max())} if len(rv_s) else None)}
    # ── instance 합치기 (distinct + self) · 포트 ──
    allinst = _merge_instances(inst, selfinst)
    ports = _ports(allinst, pos, piece_pos, segs, lo, vox, n, flat, thr['r_port_um'])
    allinst.update(ports)
    nI = len(allinst['fi'])
    nrv = np.zeros(nI, np.int64)
    for (p, q, _l) in rv:
        for kq in range(nD, nI):
            A_, B_ = allinst['self_A'][kq], allinst['self_B'][kq]
            if (np.any(A_ == p) and np.any(B_ == q)) or (np.any(A_ == q) and np.any(B_ == p)):
                nrv[kq] += 1
    allinst['self_n_revisit'] = nrv
    allinst['self_n_face'] = np.r_[np.zeros(nD, np.int64), self_face_n].astype(np.int64)
    allinst['long'] = allinst['Lc'] > thr['L_par_um'] * (1.0 + CJUNC_LPAR_RTOL)   # 긴 접촉 표지 (집계 · 거부 아님) — 원장에서 한 번
    allinst['mult'] = np.asarray(junction_len_mult(allinst['Lc'], thr['L_par_um']), np.float64).reshape(nI)   # 길이 법칙 v0
    # ── 분산판 v0 (10-21 RCA-05 · Q3 (가)) — instance 마다 k = ceil(L_c/L_par) 간선 (k 1 = instance 그대로 = 옛 점 접합) ──
    sub, nsub = _subedges(allinst, pos, piece_pos, segs, lo, vox, n, flat, thr, T_touch)
    allinst['nsub'] = nsub
    allinst['sub_ptr'] = np.r_[0, np.cumsum(nsub)].astype(np.int64)
    #  경로로만 쌍은 접합 간선이 실제로 잇지 않은 것만 (실현 간선의 포트 짝이 그 두 위치면 이어졌다)
    if len(path_only):
        jp = {(int(a), int(b)) for a, b, ok in zip(sub['port_i'], sub['port_j'], sub['realized']) if ok}
        path_only = [(p, q) for (p, q) in path_only if (p, q) not in jp and (q, p) not in jp]
        self_census['n_self_revisits_path_only'] = int(len(path_only))
    # ── SDCP 근접 · PTFE 덮임 — instance 대표점 (옛 칸 · census) + 간선마다 (계획이 읽는 것) ──
    cp = allinst['cp']
    a_sdcp = np.zeros(nI, bool)
    sd = P[PH == 5]
    scp = sub['cp']
    nS = len(sub['inst'])
    s_a = np.zeros(nS, bool)
    if len(sd) and (nI or nS):
        from scipy.spatial import cKDTree
        tree = cKDTree(sd)
        if nI:
            dd, _ = tree.query(cp)
            a_sdcp = (dd - thr['r_sdcp_um']) <= thr['tol_sj_um']
        if nS:
            ds, _ = tree.query(scp)
            s_a = (ds - thr['r_sdcp_um']) <= thr['tol_sj_um']
    ptfe_cov = np.zeros(nI, bool)
    s_cov = np.zeros(nS, bool)
    pt_paths = _paths_of(P, PH, F, K, 4, rej, 'PTFE')
    psegs, _ = _segments_of(pt_paths, P, thr['gap_tol'])
    if len(psegs['P0']):
        lim = thr['r_ptfe_um'] + rf + thr['tol_P_um']
        for k in range(nI):
            d2, _, _ = pt_seg_d2(np.repeat(cp[k][None], len(psegs['P0']), 0), psegs['P0'], psegs['P1'])
            ptfe_cov[k] = math.sqrt(float(np.min(d2))) <= lim
        for e in range(nS):
            d2, _, _ = pt_seg_d2(np.repeat(scp[e][None], len(psegs['P0']), 0), psegs['P0'], psegs['P1'])
            s_cov[e] = math.sqrt(float(np.min(d2))) <= lim
    allinst['a_sdcp'] = a_sdcp
    allinst['ptfe_cov'] = ptfe_cov
    sub['a_sdcp'] = s_a
    sub['ptfe_cov'] = s_cov
    # ── 면 표 정렬 ──
    if rows_lin:
        ft = {'lin': np.concatenate(rows_lin).astype(np.int64), 'ax': np.concatenate(rows_ax).astype(np.int64),
              'kind': np.concatenate(rows_kind).astype(np.int64), 'pa': np.concatenate(rows_pa).astype(np.int64),
              'pb': np.concatenate(rows_pb).astype(np.int64), 'inst': np.concatenate(rows_inst).astype(np.int64)}
        oo = np.lexsort((ft['pb'], ft['pa'], ft['kind'], ft['ax'], ft['lin']))
        ft = {k_: v_[oo] for k_, v_ in ft.items()}
    else:
        z = np.zeros(0, np.int64)
        ft = {'lin': z, 'ax': z.copy(), 'kind': z.copy(), 'pa': z.copy(), 'pb': z.copy(), 'inst': z.copy()}
    ft['key'] = ft['lin'] * 3 + ft['ax']
    # ── SV 반사실 대조 표지 (★ 10-21 Q-D · 면 행마다 · 기하만) ──
    ft['sv_cut'], sv_census = _sv_split(sid, ft, pos, piece_pos, segs, n, lo, vox, D, thr['s_min_um'])
    # ── census ──
    census = _census(allinst, pos, ft, cell_lin, cell_ptr, cell_pos, sid, flat, owner_ties, multi_site, n_cut_site, n_unreg,
                     segs, len(vg_paths_ok), len(pieces), rf)
    census.update(_sdcp_bridging(sid, ft, pos, n))
    census.update(self_census)
    census.update(_sub_census(allinst, sub))
    census.update(sv_census)
    pc = np.asarray(segs['piece_closed'], np.int64)
    meets = 0
    for c_i in range(len(cell_lin)):
        mem = cell_pos[cell_ptr[c_i]:cell_ptr[c_i + 1]]
        fp_ = {}
        for p in mem:
            fp_.setdefault(int(pos['fid'][p]), set()).add(int(pos['piece'][p]))
        meets += int(any(len(v) >= 2 for v in fp_.values()))
    census.update({'n_instances_same_fid_pieces': int(np.sum((allinst['fi'] == allinst['fj']) & ~allinst['self'])),
                   'n_piece_cell_meets': int(meets), 'n_ring_pieces': int(np.sum(pc == 2)),
                   'n_closed_paths_joined': int(np.sum(pc == 1)), 'n_seam_alias': int(np.sum(pos['alias'] >= 0)),
                   'piece_rule': CJUNC_PIECE_RULE})
    reg = {'kind': 'cjunc_registry', 'version': CJUNC_MODEL_VERSION, 'schema': CJUNC_SCHEMA, 'vox': vox, 'lo': lo,
           'shape': tuple(int(x) for x in n), 'thresholds': thr,
           'rules': {'lc': CJUNC_LC_RULE, 'port': CJUNC_PORT_RULE, 'footprint': CJUNC_FOOTPRINT_RULE, 'self': CJUNC_SELF_RULE,
                     'owner': CJUNC_OWNER_RULE, 'eps_d2_um2': CJUNC_EPS_D2_UM2, 'lpar_rtol': CJUNC_LPAR_RTOL,
                     'len_law': CJUNC_LEN_LAW, 'self_lc': CJUNC_SELF_LC_RULE, 'self_s': CJUNC_SELF_S_RULE,
                     'dist': CJUNC_DIST_RULE, 'branch': CJUNC_BRANCH_RULE, 'order': CJUNC_ORDER_RULE, 'cp': CJUNC_CP_RULE,
                     'piece': CJUNC_PIECE_RULE, 'sv_cf': CJUNC_SV_CF_RULE},
           'positions': pos, 'segments': segs, 'instances': allinst, 'subedges': sub, 'faces': ft, 'cell_lin': cell_lin,
           'cell_ptr': cell_ptr, 'cell_pos': cell_pos, 'n_extra_dofs': n_extra,
           'self_revisit_pairs': np.asarray(path_only, np.int64).reshape(-1, 2), 'rejections': rej, 'census': census}
    reg['fp'] = {'sid': _grid_fp(sid), 'centreline': _fp(segs), 'membership': _fp(pos), 'registry': registry_fp(reg)}
    return reg


def registry_fp(reg):
    """원장 지문 (E5) — 기하 · 문턱 · 규칙 · 표 전부 (만든 뒤 바뀐 원장 = 계획 거부)."""
    return _fp(reg['vox'], reg['lo'], reg['shape'], reg['thresholds'], reg['rules'], reg['positions'], reg['segments'],
               reg['instances'], reg['subedges'], reg['faces'], reg['cell_lin'], reg['cell_ptr'], reg['cell_pos'],
               reg['n_extra_dofs'], reg['self_revisit_pairs'], [x['code'] for x in reg['rejections']])


def _distinct_instances(segs, D, T):
    """J2a · J2c — 서로 다른 섬유 (★ 10-21 Q-A: `_distinct_keep` = 조각이 다름 · 같은 fid 의 끊긴 조각 포함) 선분 쌍 중 최근접 ≤ D ·
    같은 조각 이웃 선분끼리 이어진 쌍 = instance 하나."""
    P0, P1 = segs['P0'], segs['P1']
    ns = len(P0)
    empty = {'fi': np.zeros(0, np.int64), 'fj': np.zeros(0, np.int64), 'self': np.zeros(0, bool), 'd0': np.zeros(0),
             'Lc': np.zeros(0), 'Ci': np.zeros((0, 3)), 'Cj': np.zeros((0, 3)), 'seg_i': [], 'seg_j': [],
             'piece_i': np.zeros(0, np.int64), 'piece_j': np.zeros(0, np.int64), 'si_min': np.zeros(0, np.int64),
             'sj_min': np.zeros(0, np.int64)}
    if ns < 2:
        return empty
    from scipy.spatial import cKDTree
    mid = 0.5 * (P0 + P1)
    half = 0.5 * np.linalg.norm(P1 - P0, axis=1)
    rad = 2.0 * float(half.max()) + D
    pr = cKDTree(mid).query_pairs(rad, output_type='ndarray')
    if len(pr) == 0:
        return empty
    i, j = pr[:, 0], pr[:, 1]
    keep = np.asarray(_distinct_keep(segs, i, j), bool)
    i, j = i[keep], j[keep]
    if len(i) == 0:
        return empty
    sw = segs['piece'][i] > segs['piece'][j]                 # ★ 10-21 RCA-04 — 쌍 방향 = 정준 조각 순 (fid 라벨 아님)
    i, j = np.where(sw, j, i), np.where(sw, i, j)
    d, s, t, C1, C2 = seg_seg_closest(P0[i], P1[i], P0[j], P1[j])
    close = d <= D
    i, j, d, s, t, C1, C2 = i[close], j[close], d[close], s[close], t[close], C1[close], C2[close]
    if len(i) == 0:
        return empty
    uf = _UF()
    keyof = {}
    pi_, pj_ = segs['piece'], segs['piece']
    for x in range(len(i)):
        keyof[(int(pi_[i[x]]), int(segs['k'][i[x]]), int(pj_[j[x]]), int(segs['k'][j[x]]))] = x
    for x in range(len(i)):
        a0, ka, b0, kb = int(pi_[i[x]]), int(segs['k'][i[x]]), int(pj_[j[x]]), int(segs['k'][j[x]])
        for da in (-1, 0, 1):
            for db in (-1, 0, 1):
                y = keyof.get((a0, ka + da, b0, kb + db))
                if y is not None:
                    uf.union(x, y)
    groups = {}
    for x in range(len(i)):
        groups.setdefault(uf.find(x), []).append(x)
    out = {k: [] for k in ('fi', 'fj', 'd0', 'Ci', 'Cj', 'seg_i', 'seg_j', 'piece_i', 'piece_j', 'si_min', 'sj_min')}
    for g, mem in groups.items():
        mem = np.asarray(mem)
        #  ★ 10-21 (`CJUNC_CP_RULE` · RCA-04/05) — 접점 = 최근접 쌍들 중 거리² ε 띠 안 · 중점 사전식 최소 (나란한 접촉의 비유일 최근접점 ·
        #    쌍 목록 순서 · 선분 세분 무관) · d0 = 무리의 최소 거리 (옛 argmin 과 같은 값)
        dm2 = d[mem] * d[mem]
        bnd = mem[dm2 <= float(dm2.min()) + CJUNC_EPS_D2_UM2]
        mid = 0.5 * (C1[bnd] + C2[bnd])
        b = bnd[np.lexsort((j[bnd], i[bnd], mid[:, 2], mid[:, 1], mid[:, 0]))[0]]
        Si = np.unique(i[mem]); Sj = np.unique(j[mem])
        out['fi'].append(int(segs['fid'][i[b]])); out['fj'].append(int(segs['fid'][j[b]]))
        out['d0'].append(float(np.min(d[mem]))); out['Ci'].append(C1[b]); out['Cj'].append(C2[b])
        out['seg_i'].append(Si); out['seg_j'].append(Sj)
        out['piece_i'].append(int(segs['piece'][i[b]])); out['piece_j'].append(int(segs['piece'][j[b]]))
        out['si_min'].append(int(i[b])); out['sj_min'].append(int(j[b]))
    out['Lc'] = _touch_len_all(out['seg_i'], out['seg_j'], segs, T)
    #  ★ 10-21 (RCA-04) — instance 순서 = (정준 조각 i, 조각 j, 접점) — fid 라벨 아님
    o = np.lexsort((np.array([c[2] for c in out['Ci']]), np.array([c[1] for c in out['Ci']]),
                    np.array([c[0] for c in out['Ci']]), np.array(out['piece_j']), np.array(out['piece_i'])))
    res = {'fi': np.asarray(out['fi'], np.int64)[o], 'fj': np.asarray(out['fj'], np.int64)[o],
           'self': np.zeros(len(o), bool), 'd0': np.asarray(out['d0'])[o], 'Lc': np.asarray(out['Lc'])[o],
           'Ci': np.asarray(out['Ci']).reshape(-1, 3)[o], 'Cj': np.asarray(out['Cj']).reshape(-1, 3)[o],
           'seg_i': [out['seg_i'][x] for x in o], 'seg_j': [out['seg_j'][x] for x in o],
           'piece_i': np.asarray(out['piece_i'], np.int64)[o], 'piece_j': np.asarray(out['piece_j'], np.int64)[o],
           'si_min': np.asarray(out['si_min'], np.int64)[o], 'sj_min': np.asarray(out['sj_min'], np.int64)[o]}
    return res


def _touch_len_all(seg_i, seg_j, segs, T):
    """L_c (J8 · `CJUNC_LC_RULE`) — instance 마다 두 가닥 각각에서 상대 instance 선분까지 중심선 거리 ≤ T (닿음) 인 구간 길이
    (선분마다 구간 합집합 · 안쪽 경계) 의 최댓값.  모든 instance · 선분 쌍을 한 번에 (이분 한 번)."""
    P0, P1 = segs['P0'], segs['P1']
    nI = len(seg_i)
    Lc = np.zeros(nI)
    if nI == 0:
        return Lc
    K, SIDE, S, Q = [], [], [], []
    for k in range(nI):
        for side, (A, B) in enumerate(((seg_i[k], seg_j[k]), (seg_j[k], seg_i[k]))):
            S.append(np.repeat(A, len(B))); Q.append(np.tile(B, len(A)))
            K.append(np.full(len(A) * len(B), k)); SIDE.append(np.full(len(A) * len(B), side))
    K = np.concatenate(K); SIDE = np.concatenate(SIDE); S = np.concatenate(S).astype(np.int64)
    Q = np.concatenate(Q).astype(np.int64)
    _, us, _, _, _ = seg_seg_closest(P0[S], P1[S], P0[Q], P1[Q])
    ua, ub = _touch_intervals(P0[S], P1[S], P0[Q], P1[Q], T, us)
    ok = np.isfinite(ua)
    seglen = np.linalg.norm(P1 - P0, axis=1)
    if not ok.any():
        return Lc
    K, SIDE, S, ua, ub = K[ok], SIDE[ok], S[ok], ua[ok], ub[ok]
    o = np.lexsort((ua, S, SIDE, K))
    K, SIDE, S, ua, ub = K[o], SIDE[o], S[o], ua[o], ub[o]
    tot = np.zeros((nI, 2))
    start = 0
    n = len(K)
    while start < n:                                         # (instance, 쪽, 선분) 무리마다 구간 합집합
        end = start
        while end < n and K[end] == K[start] and SIDE[end] == SIDE[start] and S[end] == S[start]:
            end += 1
        cur_a, cur_b = ua[start], ub[start]
        acc = 0.0
        for x in range(start + 1, end):
            if ua[x] <= cur_b:
                cur_b = max(cur_b, ub[x])
            else:
                acc += cur_b - cur_a
                cur_a, cur_b = ua[x], ub[x]
        acc += cur_b - cur_a
        tot[K[start], SIDE[start]] += acc * seglen[S[start]]
        start = end
    return tot.max(axis=1)


def _continuity(s_um, d_um, D, s_min_um):
    """같은 조각 두 자리 (선분 쌍 · 면의 두 위치) 가 같은 가닥의 연속인가 — 바닥 (`_self_floor`) 밖이거나 s < s_min (등록 문턱 · 없으면
    바닥만).  아니면 접촉 (자기 접합 쌍 · 면 = 접합 자리 절단 또는 미등록)."""
    fl = np.asarray(_self_floor(s_um, d_um, D), bool)
    if s_min_um is None:
        return ~fl
    return ~fl | ~np.asarray(_self_is_junction(s_um, s_min_um), bool)


def _pos_arc_ranges(p, pos, segs, lo, vox):
    """위치 p 의 셀 조각 (그 셀 닫힌 상자로 자른 중심선) → (조각 끝점 X0 · X1, 호 구간 [lo, hi] 목록) · 고리 이음매 별칭이면 짝 위치의 조각도."""
    plist = [int(p)]
    a = int(pos['alias'][p])
    if a >= 0:
        plist.append(a)
    else:
        tgt = np.flatnonzero(pos['alias'] == int(p))
        plist += [int(t) for t in tgt]
    X0, X1, a0, a1 = _pos_portions(plist, pos, segs, lo, vox)
    return X0, X1, np.minimum(a0, a1), np.maximum(a0, a1)


def _arc_gap(rp, rq, L):
    """두 호 구간 묶음 (lo, hi 배열) 사이 최소 호 간격 — 고리 (L > 0) = 둘레 짧은 쪽."""
    lo_p, hi_p = rp
    lo_q, hi_q = rq
    if len(lo_p) == 0 or len(lo_q) == 0:
        return math.inf
    g = np.maximum(0.0, np.maximum(lo_p[:, None], lo_q[None, :]) - np.minimum(hi_p[:, None], hi_q[None, :]))
    if L > 0.0:
        span = np.maximum(hi_p[:, None], hi_q[None, :]) - np.minimum(lo_p[:, None], lo_q[None, :])
        g = np.minimum(g, np.maximum(0.0, L - span))
    return float(g.min())


def _pos_pair_sd(p, q, pos, segs, lo, vox):
    """같은 조각 두 위치의 (호 간격 s · 중심선 최소 거리 d) — 면 · 재방문 · SV 무리의 연속 판정 (`_continuity`) 입력."""
    Xp0, Xp1, lp, hp = _pos_arc_ranges(p, pos, segs, lo, vox)
    Xq0, Xq1, lq, hq = _pos_arc_ranges(q, pos, segs, lo, vox)
    L = float(segs['ring_L'][pos['s0'][p]]) if len(segs['ring_L']) else 0.0
    s = _arc_gap((lp, hp), (lq, hq), L)
    if len(Xp0) == 0 or len(Xq0) == 0:
        return s, math.inf
    ia = np.repeat(np.arange(len(Xp0)), len(Xq0))
    ib = np.tile(np.arange(len(Xq0)), len(Xp0))
    d, _, _, _, _ = seg_seg_closest(Xp0[ia], Xp1[ia], Xq0[ib], Xq1[ib])
    return s, float(d.min())


def _self_pairs(segs, D, s_min):
    """★ 10-21 (사전 리뷰 PRE-impl-02 · 1저자 Q-B · `CJUNC_SELF_RULE`) — 자기 접합 탐지 = 서로 다른 섬유와 같은 중심선 근접: 같은 조각 선분 쌍
    (i < j) 중 최근접 d ≤ D · 쌍마다 s = 최근접점 사이 조각 호 길이 (고리 = 짧은 쪽) · 바닥 (`_self_floor`) 을 넘는 쌍만 (후보 쌍) ·
    접합 쌍 = 후보 쌍 중 s ≥ s_min (s_min 없음 = 후보 쌍 전부 · 시험 모드 · S0 census).  셀 인접 (면 · 같은 셀) 은 쓰지 않는다 (옛: 셀
    인접 = 후보 · 중심선 거리 검사 없음 → 닿지 않는 다리에도 접합 · 닿는 모서리 인접 다리엔 접합 없음).  → dict(i, j, d, s, C1, C2, junc)."""
    P0, P1 = segs['P0'], segs['P1']
    ns = len(P0)
    empty = {'i': np.zeros(0, np.int64), 'j': np.zeros(0, np.int64), 'd': np.zeros(0), 's': np.zeros(0),
             'C1': np.zeros((0, 3)), 'C2': np.zeros((0, 3)), 'junc': np.zeros(0, bool)}
    if ns < 2:
        return empty
    from scipy.spatial import cKDTree
    mid = 0.5 * (P0 + P1)
    half = 0.5 * np.linalg.norm(P1 - P0, axis=1)
    rad = 2.0 * float(half.max()) + D
    pr = cKDTree(mid).query_pairs(rad, output_type='ndarray')
    if len(pr) == 0:
        return empty
    i, j = pr[:, 0], pr[:, 1]
    keep = segs['piece'][i] == segs['piece'][j]
    i, j = i[keep], j[keep]
    if len(i) == 0:
        return empty
    sw = i > j
    i, j = np.where(sw, j, i), np.where(sw, i, j)
    o = np.lexsort((j, i))
    i, j = i[o], j[o]
    d, sp_, tp_, C1, C2 = seg_seg_closest(P0[i], P1[i], P0[j], P1[j])
    close = d <= D
    i, j, d, sp_, tp_, C1, C2 = i[close], j[close], d[close], sp_[close], tp_[close], C1[close], C2[close]
    if len(i) == 0:
        return empty
    ai = segs['arc_a'][i] + sp_ * (segs['arc_b'][i] - segs['arc_a'][i])
    aj = segs['arc_a'][j] + tp_ * (segs['arc_b'][j] - segs['arc_a'][j])
    s = np.abs(aj - ai)
    L = segs['ring_L'][i]
    s = np.where(L > 0.0, np.minimum(s, L - s), s)
    fl = np.asarray(_self_floor(s, d, D), bool).reshape(len(s))
    if s_min is None:
        jn = np.ones(len(s), bool)
    else:
        jn = np.asarray(_self_is_junction(s, s_min), bool).reshape(len(s))
    m = fl
    return {'i': i[m], 'j': j[m], 'd': d[m], 's': s[m], 'C1': C1[m], 'C2': C2[m], 'junc': (fl & jn)[m]}


def _pair_groups(pi, pj, segs, sel):
    """같은 조각 쌍 무리 (union-find) — 이웃 선분 (k ± 1 · 고리 조각 = 둘레) 끼리 이어진 쌍 = 한 무리 (서로 다른 섬유 J2c 와 같은 꼴).
    sel = 쓸 쌍 마스크.  → 무리마다 쌍 번호 배열 (정준 순 = 무리 안 최소 (i, j))."""
    idx = np.flatnonzero(sel)
    if len(idx) == 0:
        return []
    piece, kk = segs['piece'], segs['k']
    nseg = np.bincount(piece, minlength=int(piece.max()) + 1 if len(piece) else 0)
    ring = segs['ring_L'] > 0.0
    keyof = {}
    for x in idx:
        keyof[(int(piece[pi[x]]), int(kk[pi[x]]), int(kk[pj[x]]))] = x
    uf = _UF()
    for x in idx:
        p_, ka, kb = int(piece[pi[x]]), int(kk[pi[x]]), int(kk[pj[x]])
        rg = bool(ring[pi[x]])
        n_ = int(nseg[p_])
        uf.find(x)
        for da in (-1, 0, 1):
            for db in (-1, 0, 1):
                a_, b_ = ka + da, kb + db
                if rg:
                    a_, b_ = a_ % n_, b_ % n_
                y = keyof.get((p_, a_, b_))
                if y is None:
                    y = keyof.get((p_, b_, a_))
                if y is not None:
                    uf.union(x, y)
    groups = {}
    for x in idx:
        groups.setdefault(uf.find(x), []).append(x)
    out = [np.asarray(sorted(m), np.int64) for m in groups.values()]
    out.sort(key=lambda m: (int(pi[m].min()), int(pj[m].min())))
    return out


def _group_cp(mem, sp):
    """쌍 무리의 접점 (`CJUNC_CP_RULE` — 서로 다른 섬유와 같은 규칙): 거리² ε 띠 안 · 중점 사전식 최소 · 그래도 같으면 (i, j)."""
    dm2 = sp['d'][mem] * sp['d'][mem]
    bnd = mem[dm2 <= float(dm2.min()) + CJUNC_EPS_D2_UM2]
    mid = 0.5 * (sp['C1'][bnd] + sp['C2'][bnd])
    return int(bnd[np.lexsort((sp['j'][bnd], sp['i'][bnd], mid[:, 2], mid[:, 1], mid[:, 0]))[0]])


def _touch_len_pairs(pi, pj, segs, T):
    """자기 접합 L_c (`CJUNC_SELF_LC_RULE`) — `_touch_len_all` 과 같은 닿음 규칙 · 짝 = 그 instance 의 접합 쌍만 (바닥 · s 규칙을 지난 쌍 ·
    같은 가닥의 연속 짝은 닿아도 넣지 않는다) · 쪽마다 선분별 구간 합집합 (안쪽 경계) 길이의 합 · 두 쪽의 최댓값."""
    best = 0.0
    for S, Q in ((pi, pj), (pj, pi)):
        su = np.unique(S); qu = np.unique(Q)
        si = np.searchsorted(su, S); qi = np.searchsorted(qu, Q)
        tot = _touch_runs_on(segs['P0'][su], segs['P1'][su], segs['P0'][qu], segs['P1'][qu], si, qi, T)[3]
        best = max(best, tot)
    return best


def _self_instances(sp, segs, T):
    """자기 접합 instance — 접합 쌍 무리마다 하나 (★ 10-21 Q-B).  접점 = `_group_cp` · d0 = 무리 최소 거리 · s = 접점 쌍의 s · L_c =
    `_touch_len_pairs` · 두 쪽 선분 = 무리의 i · j 선분 (발자국 · 분산판 · 포트 후보) · 쌍 목록 (분산판 짝 제한).  순서 = (조각, 접점)."""
    groups = _pair_groups(sp['i'], sp['j'], segs, sp['junc'])
    out = {k: [] for k in ('fi', 'fj', 'd0', 'Lc', 's', 'Ci', 'Cj', 'seg_i', 'seg_j', 'piece_i', 'piece_j', 'si_min', 'sj_min',
                           'pair_i', 'pair_j')}
    for mem in groups:
        b = _group_cp(mem, sp)
        pi_ = sp['i'][mem]; pj_ = sp['j'][mem]
        f = int(segs['fid'][sp['i'][b]]); p_ = int(segs['piece'][sp['i'][b]])
        out['fi'].append(f); out['fj'].append(f); out['piece_i'].append(p_); out['piece_j'].append(p_)
        out['d0'].append(float(np.min(sp['d'][mem]))); out['s'].append(float(sp['s'][b]))
        out['Ci'].append(sp['C1'][b].copy()); out['Cj'].append(sp['C2'][b].copy())
        out['seg_i'].append(np.unique(pi_)); out['seg_j'].append(np.unique(pj_))
        out['pair_i'].append(pi_.copy()); out['pair_j'].append(pj_.copy())
        out['si_min'].append(int(sp['i'][b])); out['sj_min'].append(int(sp['j'][b]))
        out['Lc'].append(_touch_len_pairs(pi_, pj_, segs, T))
    nq = len(out['fi'])
    if nq:
        C = np.asarray(out['Ci'], np.float64).reshape(-1, 3)
        o = np.lexsort((C[:, 2], C[:, 1], C[:, 0], np.asarray(out['piece_i'])))
    else:
        o = np.zeros(0, np.int64)
    res = {'fi': np.asarray(out['fi'], np.int64)[o], 'fj': np.asarray(out['fj'], np.int64)[o],
           'self': np.ones(nq, bool), 'd0': np.asarray(out['d0'], np.float64)[o], 'Lc': np.asarray(out['Lc'], np.float64)[o],
           's': np.asarray(out['s'], np.float64)[o], 'Ci': np.asarray(out['Ci'], np.float64).reshape(-1, 3)[o],
           'Cj': np.asarray(out['Cj'], np.float64).reshape(-1, 3)[o],
           'piece_i': np.asarray(out['piece_i'], np.int64)[o], 'piece_j': np.asarray(out['piece_j'], np.int64)[o],
           'si_min': np.asarray(out['si_min'], np.int64)[o], 'sj_min': np.asarray(out['sj_min'], np.int64)[o]}
    for k in ('seg_i', 'seg_j', 'pair_i', 'pair_j'):
        res[k] = [out[k][x] for x in o]
    return res


def _clip_box(P0, P1, bmin, bmax):
    """선분 P0→P1 ∩ 닫힌 상자 [bmin, bmax] (배열 · Liang–Barsky) → 매개 (t0, t1) · 빈 = t0 > t1."""
    d = P1 - P0
    t0 = np.zeros(len(P0))
    t1 = np.ones(len(P0))
    for ax in range(3):
        da = d[:, ax]
        z = da == 0.0
        out = z & ((P0[:, ax] < bmin[:, ax]) | (P0[:, ax] > bmax[:, ax]))
        den = np.where(z, 1.0, da)
        ta = np.where(z, -np.inf, (bmin[:, ax] - P0[:, ax]) / den)
        tb = np.where(z, np.inf, (bmax[:, ax] - P0[:, ax]) / den)
        t0 = np.maximum(t0, np.minimum(ta, tb))
        t1 = np.minimum(t1, np.maximum(ta, tb))
        t0 = np.where(out, 1.0, t0)
        t1 = np.where(out, 0.0, t1)
    return t0, t1


def _pos_portions(plist, pos, segs, lo, vox):
    """위치들의 셀 안 중심선 조각 — 각 위치의 선분 (s0..s1) 을 그 셀의 **닫힌 상자 그대로** (띠 없음) 로 자른 것.
    이웃 셀 상자는 같은 식 (lo + ijk·vox) 이라 경계가 비트로 같고, 경계에만 닿는 선분 (스냅된 셀) 은 길이 0 점이다 —
    띠를 두면 조각이 셀 밖으로 늘어 자기 L_c 가 부풀어진다.  → (X0, X1, a0, a1) = 조각 끝점 · 끝의 경로 호 좌표 (선분 위 선형)."""
    pl = np.asarray(sorted({int(p) for p in plist}), np.int64)
    if len(pl) == 0:
        z = np.zeros((0, 3))
        return z, z.copy(), np.zeros(0), np.zeros(0)
    cnt = pos['s1'][pl] - pos['s0'][pl] + 1
    rp = np.repeat(pl, cnt)
    sg = pos['s0'][rp] + (np.arange(len(rp)) - np.repeat(np.cumsum(cnt) - cnt, cnt))
    ijk = pos['ijk'][rp].astype(np.float64)
    bmin = lo + ijk * vox
    bmax = lo + (ijk + 1.0) * vox
    P0, P1 = segs['P0'][sg], segs['P1'][sg]
    t0, t1 = _clip_box(P0, P1, bmin, bmax)
    ok = t0 <= t1
    d = (P1 - P0)[ok]
    X0 = P0[ok] + t0[ok, None] * d
    X1 = P0[ok] + t1[ok, None] * d
    aa, ab = segs['arc_a'][sg][ok], segs['arc_b'][sg][ok]
    return X0, X1, aa + t0[ok] * (ab - aa), aa + t1[ok] * (ab - aa)


def _merge_instances(inst, selfinst):
    """distinct + self instance 표 (distinct 먼저 · 자기 instance 번호 = distinct 수 + 자기 번호).  자기 접합의 접점 (Ci · Cj) = 그 무리
    접점 쌍 (옛 칸 self_xa · self_xb = 같은 값 · 분산판 k 1 이 읽는다) · 두 쪽 위치 · 재방문 · 면 수는 호출자가 채운다."""
    nI = len(inst['fi']); nS = len(selfinst['fi'])
    out = {'fi': np.r_[inst['fi'], selfinst['fi']].astype(np.int64), 'fj': np.r_[inst['fj'], selfinst['fj']].astype(np.int64),
           'self': np.r_[np.zeros(nI, bool), np.ones(nS, bool)],
           'd0': np.r_[inst['d0'], selfinst['d0']].astype(np.float64),
           'Lc': np.r_[inst['Lc'], selfinst['Lc']].astype(np.float64),
           's': np.r_[np.full(nI, np.nan), selfinst['s']].astype(np.float64),          # 자기 접합 경로 호 길이 (distinct = NaN)
           'Ci': np.r_[inst['Ci'], selfinst['Ci']].reshape(-1, 3), 'Cj': np.r_[inst['Cj'], selfinst['Cj']].reshape(-1, 3),
           'piece_i': np.r_[inst['piece_i'], selfinst['piece_i']].astype(np.int64),
           'piece_j': np.r_[inst['piece_j'], selfinst['piece_j']].astype(np.int64),
           'si_min': np.r_[inst['si_min'], selfinst['si_min']].astype(np.int64),
           'sj_min': np.r_[inst['sj_min'], selfinst['sj_min']].astype(np.int64)}
    out['self_xa'] = np.r_[np.full((nI, 3), np.nan), selfinst['Ci']].reshape(-1, 3)
    out['self_xb'] = np.r_[np.full((nI, 3), np.nan), selfinst['Cj']].reshape(-1, 3)
    out['seg_i'] = list(inst['seg_i']) + list(selfinst['seg_i'])
    out['seg_j'] = list(inst['seg_j']) + list(selfinst['seg_j'])
    out['pair_i'] = [np.zeros(0, np.int64)] * nI + list(selfinst['pair_i'])
    out['pair_j'] = [np.zeros(0, np.int64)] * nI + list(selfinst['pair_j'])
    return out


def _port_pick(C, cand, pos, segs, lo, vox, r_port=None):
    """★ 10-21 (`CJUNC_PORT_RULE` · Codex RCA-04 · 1저자 Q2 (가)) — 접점 C → 후보 위치 중 포트 하나 (방향 무관 기하 정준 규칙):
    ① 셀 중심까지 거리 (r_port 가 주어지면 그 안만) ② 거리² ε 띠 (`CJUNC_EPS_D2_UM2`) 안 동률 = 셀 정수 좌표 사전식 최소 ③ 그 셀에 후보
    가지가 여럿 (같은 fid 재방문 · 같은 조각 다른 번호) = 접점까지 그 가지 중심선 거리 (ε 띠) ④ 그래도 같으면 정준 (조각, 번호).
    경로 열 번호로 동률을 풀지 않는다 (옛: '정준 방향 경로 번호가 작은 위치' — 먼 끝이 바뀌면 정준 방향이 뒤집혀 포트가 바뀌었다).
    → (위치 | −1, 동률 (② 또는 ③ 에서 후보 둘 이상), 셀 중심 거리)."""
    cand = np.asarray(cand, np.int64)
    if len(cand) == 0:
        return -1, False, np.inf
    C = np.asarray(C, np.float64)
    cc = lo + (pos['ijk'][cand].astype(np.float64) + 0.5) * vox
    d2 = np.sum((cc - C) ** 2, axis=1)
    if r_port is not None:
        okc = np.sqrt(d2) <= r_port
        if not okc.any():
            return -1, False, np.inf
        cand, d2 = cand[okc], d2[okc]
    m = float(d2.min())
    bnd = cand[d2 <= m + CJUNC_EPS_D2_UM2]
    ijk = pos['ijk'][bnd]
    o = np.lexsort((ijk[:, 2], ijk[:, 1], ijk[:, 0]))
    first = bnd[o[0]]
    same = bnd[np.all(pos['ijk'][bnd] == pos['ijk'][first], axis=1)]
    tie = bool(len(bnd) > 1)
    if len(same) > 1:                                          # ③ 같은 셀 여러 가지 — 접점까지 가지 중심선 거리
        bd = np.empty(len(same))
        for x, p in enumerate(same):
            sg = np.arange(pos['s0'][p], pos['s1'][p] + 1)
            dd, _, _ = pt_seg_d2(np.repeat(C[None], len(sg), 0), segs['P0'][sg], segs['P1'][sg])
            bd[x] = float(dd.min())
        near = same[bd <= float(bd.min()) + CJUNC_EPS_D2_UM2]
        first = near[np.lexsort((pos['k'][near], pos['piece'][near]))[0]]
    return int(first), tie, float(math.sqrt(m))


def _piece_cand(piece, pos, piece_pos):
    """조각의 포트 후보 = 그 조각의 위치 **전부** (★ 10-21 사전 리뷰 PRE-impl-03 · 1저자 Q-C — 덮인 위치도 · 고른 뒤 `_port_take` 가 살았는지
    본다 · 옛: 살아있는 위치만 → 접점 셀이 덮이면 r_port 안 이웃 셀로 옮겨 붙었다)."""
    a0, a1 = piece_pos[piece]
    return np.arange(a0, a1)


def _side_cand(S, piece, pos, piece_pos):
    """자기 접합 한 쪽의 포트 후보 = 그 조각의 위치 중 선분 범위 [s0, s1] 가 그 쪽 선분 (접합 쌍의 그 쪽) 과 겹치는 것 (살았든 덮였든 —
    다른 쪽 가닥의 셀을 고르지 않는다)."""
    a0, a1 = piece_pos[piece]
    c = np.arange(a0, a1)
    S = np.asarray(S, np.int64)
    if len(c) == 0 or len(S) == 0:
        return c[:0]
    lo_ = np.searchsorted(S, pos['s0'][c], 'left')
    hi_ = np.searchsorted(S, pos['s1'][c], 'right')
    return c[hi_ > lo_]


def _port_take(C, cand, pos, segs, lo, vox, flat, r_port):
    """★ 10-21 (사전 리뷰 PRE-impl-03 · 1저자 Q-C · `CJUNC_PORT_RULE`) — 포트 = 후보 위치 (살았든 덮였든) 중 `_port_pick` 규칙 하나 · 고른
    위치가 덮였으면 (다른 상 · 상자 밖) **옮기지 않고** 미실현 (사유 covered_<상> · out_of_box) — 덮은 상의 법칙만 남는다 (SDCP = SV
    융합 · S3 c · PTFE face_alpha = P0/P1 · 같은 접촉을 두 번 세지 않는다).  r_port 안 후보 없음 = no_port_in_rport.
    → (위치 | −1, 동률, 셀 중심 거리, 사유)."""
    p, tie, dist = _port_pick(C, cand, pos, segs, lo, vox, r_port)
    if p < 0:
        return -1, False, math.inf, 'no_port_in_rport'
    if not pos['live'][p]:
        lin = int(pos['lin'][p])
        why = 'out_of_box' if lin < 0 else f'covered_{_SID_NAME.get(int(flat[lin]), str(int(flat[lin])))}'
        return -1, bool(tie), float(dist), why
    return int(p), bool(tie), float(dist), ''


def _ports(allinst, pos, piece_pos, segs, lo, vox, n, flat, r_port):
    """J3 · J4 — instance 접점 → 포트 (`_port_take` · 방향 무관 기하 정준 규칙 · 10-21 RCA-04 · ★ Q-C 옮김 없음).  서로 다른 섬유 = 그 조각의
    위치 중 r_port 안 · 자기 접합 = 그 쪽 위치 (`_side_cand`) 중 r_port 안 — 같은 규칙 (fid 무관).  자기 접합 k 차 (self_dk_min) = 두 포트
    위치 번호 차 (고리 = 둘레 짧은 쪽 · 미실현 = −1)."""
    nI = len(allinst['fi'])
    port_i = np.full(nI, -1, np.int64); port_j = np.full(nI, -1, np.int64)
    reason = np.array([''] * nI, dtype=object)
    tie_i = np.zeros(nI, bool); tie_j = np.zeros(nI, bool)
    disp = np.zeros(nI, bool); sdist = np.full(nI, np.nan)
    cp = np.zeros((nI, 3))
    dk = np.full(nI, -1, np.int64)
    side_A, side_B = [], []
    for k in range(nI):
        Ci, Cj = allinst['Ci'][k], allinst['Cj'][k]
        cp[k] = 0.5 * (Ci + Cj)
        if allinst['self'][k]:
            ci = _side_cand(allinst['seg_i'][k], int(allinst['piece_i'][k]), pos, piece_pos)
            cj = _side_cand(allinst['seg_j'][k], int(allinst['piece_j'][k]), pos, piece_pos)
        else:
            ci = _piece_cand(int(allinst['piece_i'][k]), pos, piece_pos)
            cj = _piece_cand(int(allinst['piece_j'][k]), pos, piece_pos)
        side_A.append(np.asarray(ci, np.int64)); side_B.append(np.asarray(cj, np.int64))
        pi_, ti, di, wi = _port_take(Ci, ci, pos, segs, lo, vox, flat, r_port)
        pj_, tj, dj, wj = _port_take(Cj, cj, pos, segs, lo, vox, flat, r_port)
        port_i[k], port_j[k] = pi_, pj_
        tie_i[k], tie_j[k] = ti, tj
        if pi_ < 0 or pj_ < 0:
            reason[k] = wi or wj
            continue
        sdist[k] = max(di, dj)
        ni = np.floor((Ci - lo) / vox).astype(np.int64); nj = np.floor((Cj - lo) / vox).astype(np.int64)
        disp[k] = bool(np.any(pos['ijk'][pi_] != ni) or np.any(pos['ijk'][pj_] != nj))
        if allinst['self'][k]:
            d_ = abs(int(pos['k'][pj_]) - int(pos['k'][pi_]))
            if pos['ring'][pi_]:
                d_ = min(d_, int(pos['piece_ng'][pi_]) - d_)
            dk[k] = d_
    return {'port_i': port_i, 'port_j': port_j, 'realized': (port_i >= 0) & (port_j >= 0), 'reason': reason,
            'tie_i': tie_i, 'tie_j': tie_j, 'port_displaced': disp, 'port_search_um': sdist, 'cp': cp,
            'long': np.zeros(nI, bool), 'self_dk_min': dk, 'self_A': side_A, 'self_B': side_B}


# ═════════════════════════ 분산판 v0 (10-21 Codex RCA-05 · 1저자 Q3 (가)) ═════════════════════════
def _touch_runs(S0, S1, Q0, Q1, T):
    """선분 열 S (순서 = 정준 경로 순서) 의 선분마다 선분 집합 Q 까지 중심선 거리 ≤ T 인 구간 합집합 (안쪽 경계) → (선분 번호 · ua · ub ·
    길이 합).  `_touch_len_all` · `_touch_len_pairs` 의 한 쪽과 같은 원시 (`_touch_intervals`) · 같은 합집합 · 같은 합산 순서 — 그 길이 =
    L_c 의 그 쪽 값 (비트).  짝 = S × Q 전부 (서로 다른 섬유)."""
    ns, nq = len(S0), len(Q0)
    if ns == 0 or nq == 0:
        z = np.zeros(0)
        return np.zeros(0, np.int64), z, z.copy(), 0.0
    return _touch_runs_on(S0, S1, Q0, Q1, np.repeat(np.arange(ns), nq), np.tile(np.arange(nq), ns), T)


def _touch_runs_on(S0, S1, Q0, Q1, si, qi, T):
    """`_touch_runs` 의 몸체 — 짝 (si, qi) 를 준다 (★ 10-21 Q-B 자기 접합 = 그 instance 의 접합 쌍만 · 서로 다른 섬유 = S × Q 전부)."""
    z = np.zeros(0)
    si = np.asarray(si, np.int64); qi = np.asarray(qi, np.int64)
    if len(si) == 0:
        return np.zeros(0, np.int64), z, z.copy(), 0.0
    _, us, _, _, _ = seg_seg_closest(S0[si], S1[si], Q0[qi], Q1[qi])
    ua, ub = _touch_intervals(S0[si], S1[si], Q0[qi], Q1[qi], T, us)
    ok = np.isfinite(ua)
    if not ok.any():
        return np.zeros(0, np.int64), z, z.copy(), 0.0
    si, ua, ub = si[ok], ua[ok], ub[ok]
    o = np.lexsort((ua, si))
    si, ua, ub = si[o], ua[o], ub[o]
    seglen = np.linalg.norm(S1 - S0, axis=1)
    rs, ra, rb = [], [], []
    tot = 0.0
    start, n = 0, len(si)
    while start < n:                                         # 선분마다 구간 합집합 (`_touch_len_sets` 와 같은 고리)
        end = start
        while end < n and si[end] == si[start]:
            end += 1
        cur_a, cur_b = ua[start], ub[start]
        acc = 0.0
        for x in range(start + 1, end):
            if ua[x] <= cur_b:
                cur_b = max(cur_b, ub[x])
            else:
                acc += cur_b - cur_a
                rs.append(si[start]); ra.append(cur_a); rb.append(cur_b)
                cur_a, cur_b = ua[x], ub[x]
        acc += cur_b - cur_a
        rs.append(si[start]); ra.append(cur_a); rb.append(cur_b)
        tot += acc * seglen[si[start]]
        start = end
    return np.asarray(rs, np.int64), np.asarray(ra, np.float64), np.asarray(rb, np.float64), float(tot)


def _divide_runs(rs, ra, rb, S0, S1, k):
    """닿음 구간 (정준 경로 순서) 을 길이로 k 등분한 칸의 가운데 점 k 개 — 칸 j 의 점 = 누적 길이 (j + ½)·L/k (L = 구간 길이 합)."""
    return _divide_runs_idx(rs, ra, rb, S0, S1, k)[0]


def _divide_runs_idx(rs, ra, rb, S0, S1, k):
    """`_divide_runs` + 점마다 그 점이 놓인 선분 번호 (S 안 번호 · 자기 접합 분산판의 짝 제한)."""
    seglen = np.linalg.norm(S1 - S0, axis=1)
    lens = (rb - ra) * seglen[rs]
    cum = np.r_[0.0, np.cumsum(lens)]
    L = float(cum[-1])
    out = np.zeros((k, 3))
    sidx = np.zeros(k, np.int64)
    for j in range(k):
        t = (j + 0.5) * L / k
        m = min(max(int(np.searchsorted(cum, t, side='right')) - 1, 0), len(lens) - 1)
        while m < len(lens) - 1 and lens[m] <= 0.0:          # 길이 0 구간 (접선 한 점) 은 건너뛴다
            m += 1
        f = 0.0 if lens[m] <= 0.0 else min(max((t - cum[m]) / lens[m], 0.0), 1.0)
        u = ra[m] + f * (rb[m] - ra[m])
        s = rs[m]
        out[j] = S0[s] + u * (S1[s] - S0[s])
        sidx[j] = int(s)
    return out, sidx


def _nearest_on(X, Q0, Q1):
    """점 X → 선분 집합 Q 의 최근접점 (거리² ε 띠 안 = 사전식 최소 점 — 나란한 맞은편의 비유일 최근접점)."""
    d2, C, _ = pt_seg_d2(np.repeat(np.asarray(X, np.float64)[None], len(Q0), 0), Q0, Q1)
    b = np.flatnonzero(d2 <= float(d2.min()) + CJUNC_EPS_D2_UM2)
    Cb = C[b]
    return Cb[np.lexsort((Cb[:, 2], Cb[:, 1], Cb[:, 0]))[0]]


def _n_sub(Lc, L_par):
    """간선 수 k = ceil(L_c/L_par) — L_c ≤ L_par·(1 + `CJUNC_LPAR_RTOL`) = 1 (점 접합 · 긴 접촉 표지와 같은 문턱) · 정수 경계도 같은 1e-9 띠
    (L_c/L_par = 2 + 몇 ulp 가 3 이 되지 않게).
    ⚠ 10-21 (사전 리뷰 PRE-impl-05 · 한계 기록 · 고치지 않음): k 는 계단이라 L_c/L_par 가 정수 경계를 넘으면 (깊은 교차 90° → 89.99° ·
      배율 차 1.5e-8) 간선 자리가 바뀌어 σ 가 뛴다 — 반쪽 간선이 셀 경계 (±L_c/4 = ±h/2) 로 가 사전식 최소 셀로 옮겨진다 · 크기 ∝ h·r′/R_j
      (생산 단위 R_j 1e2 · 1e4 · 1e6 Ω 에서 −0.98 % · −2.1e-4 · −2.1e-6 — 시험 KBND 가 묶는다).  분산판 v0 = 계단 근사 (이산화 오차) ·
      origin · 순서 대조에서 이 뜀이 잡음으로 섞일 수 있다 (한정어) · 경계 연속 배치는 v1 후보."""
    r = float(Lc) / float(L_par)
    if not (r > 1.0 + CJUNC_LPAR_RTOL):
        return 1
    return max(2, int(math.ceil(r - CJUNC_LPAR_RTOL)))


def _subedges(allinst, pos, piece_pos, segs, lo, vox, n, flat, thr, T):
    """분산판 v0 (`CJUNC_DIST_RULE`) — instance 마다 k 간선.  k = 1 = instance 그대로 (포트 · 접점 · 사유 · 동률 = 옛 점 접합 · 비트 같음).
    k > 1 = 정의 쪽 (닿음 길이가 긴 가닥 · 1e-9 상대 안 동률 = i 쪽) 의 닿음 구간을 k 등분한 칸 가운데 점 X · 맞은편 최근접점 Y (ε 띠 ·
    사전식) · 포트 = `_port_take` (서로 다른 섬유 = 그 조각 / 자기 접합 = 그 쪽 위치 · 둘 다 r_port 안 · 덮였으면 미실현) · 간선 접점 =
    (X_i + X_j)/2.  ★ 10-21 (Q-B) 자기 접합 = 닿음 · 맞은편 = 그 instance 의 접합 쌍만 (같은 가닥의 연속 짝은 쓰지 않는다).
    PTFE 덮임 · SDCP 근접은 호출자가 간선 접점에서 잰다.  → (간선 표 dict, instance 마다 k)."""
    nI = len(allinst['fi'])
    L_par, r_port = thr['L_par_um'], thr['r_port_um']
    rec = {k_: [] for k_ in ('inst', 'j', 'k', 'side', 'port_i', 'port_j', 'cp', 'X_i', 'X_j', 'realized', 'reason', 'tie_i',
                              'tie_j', 'port_search_um')}
    nsub = np.ones(nI, np.int64)

    def add(q, j, kq, side, pi_, pj_, xi, xj, cp_, ok, why, ti, tj, sd):
        for k_, v_ in (('inst', q), ('j', j), ('k', kq), ('side', side), ('port_i', pi_), ('port_j', pj_), ('cp', cp_),
                       ('X_i', xi), ('X_j', xj), ('realized', ok), ('reason', why), ('tie_i', ti), ('tie_j', tj),
                       ('port_search_um', sd)):
            rec[k_].append(v_)
    for q in range(nI):
        kq = _n_sub(allinst['Lc'][q], L_par)
        nsub[q] = kq
        isself = bool(allinst['self'][q])
        if kq == 1:                                          # 점 접합 — instance 그대로 (옛 점 접합과 비트 같음)
            add(q, 0, 1, -1, int(allinst['port_i'][q]), int(allinst['port_j'][q]), np.asarray(allinst['Ci'][q], np.float64).copy(),
                np.asarray(allinst['Cj'][q], np.float64).copy(), allinst['cp'][q].copy(), bool(allinst['realized'][q]),
                str(allinst['reason'][q]), bool(allinst['tie_i'][q]), bool(allinst['tie_j'][q]),
                float(allinst['port_search_um'][q]))
            continue
        Si, Sj = np.asarray(allinst['seg_i'][q], np.int64), np.asarray(allinst['seg_j'][q], np.int64)
        I0, I1 = segs['P0'][Si], segs['P1'][Si]
        J0, J1 = segs['P0'][Sj], segs['P1'][Sj]
        if isself:
            pa = np.searchsorted(Si, np.asarray(allinst['pair_i'][q], np.int64))
            pb = np.searchsorted(Sj, np.asarray(allinst['pair_j'][q], np.int64))
            rI = _touch_runs_on(I0, I1, J0, J1, pa, pb, T)
            rJ = _touch_runs_on(J0, J1, I0, I1, pb, pa, T)
        else:
            rI = _touch_runs(I0, I1, J0, J1, T)
            rJ = _touch_runs(J0, J1, I0, I1, T)
        ci = np.asarray(allinst['self_A'][q], np.int64)
        cj_ = np.asarray(allinst['self_B'][q], np.int64)
        side = 1 if rJ[3] > rI[3] * (1.0 + CJUNC_LPAR_RTOL) else 0
        if side == 0:
            Xd, Xs = _divide_runs_idx(rI[0], rI[1], rI[2], I0, I1, kq)
        else:
            Xd, Xs = _divide_runs_idx(rJ[0], rJ[1], rJ[2], J0, J1, kq)
        for j in range(kq):
            if side == 0:
                xi = Xd[j]
                if isself:
                    m_ = pb[pa == Xs[j]]
                    xj = _nearest_on(xi, J0[m_], J1[m_])
                else:
                    xj = _nearest_on(xi, J0, J1)
            else:
                xj = Xd[j]
                if isself:
                    m_ = pa[pb == Xs[j]]
                    xi = _nearest_on(xj, I0[m_], I1[m_])
                else:
                    xi = _nearest_on(xj, I0, I1)
            pi_, ti, di, wi = _port_take(xi, ci, pos, segs, lo, vox, flat, r_port)
            pj_, tj, dj, wj = _port_take(xj, cj_, pos, segs, lo, vox, flat, r_port)
            ok = pi_ >= 0 and pj_ >= 0
            why = '' if ok else (wi or wj)
            add(q, j, kq, side, pi_, pj_, xi.copy(), xj.copy(), 0.5 * (xi + xj), ok, why, ti, tj,
                (max(di, dj) if ok else np.nan))
    nS = len(rec['inst'])
    reason = np.empty(nS, dtype=object)
    for x, w in enumerate(rec['reason']):
        reason[x] = w
    sub = {'inst': np.asarray(rec['inst'], np.int64), 'j': np.asarray(rec['j'], np.int64), 'k': np.asarray(rec['k'], np.int64),
           'side': np.asarray(rec['side'], np.int64), 'port_i': np.asarray(rec['port_i'], np.int64),
           'port_j': np.asarray(rec['port_j'], np.int64), 'cp': np.asarray(rec['cp'], np.float64).reshape(-1, 3),
           'X_i': np.asarray(rec['X_i'], np.float64).reshape(-1, 3), 'X_j': np.asarray(rec['X_j'], np.float64).reshape(-1, 3),
           'realized': np.asarray(rec['realized'], bool).reshape(nS), 'reason': reason,
           'tie_i': np.asarray(rec['tie_i'], bool).reshape(nS), 'tie_j': np.asarray(rec['tie_j'], bool).reshape(nS),
           'port_search_um': np.asarray(rec['port_search_um'], np.float64).reshape(nS),
           'a_sdcp': np.zeros(nS, bool), 'ptfe_cov': np.zeros(nS, bool)}
    return sub, nsub


def _sub_census(inst, sub):
    """분산 간선 census (Q11 · S0 보탬) — 간선 수 · 긴 접촉 간선 · 간선별 PTFE 덮임 · 부분 덮임 instance · SDCP 근접 · 미실현 · 포트 동률
    (간선 단위 · k 1 = instance 단위와 같다).  σ 칸 없음."""
    nS = len(sub['inst'])
    nI = len(inst['fi'])
    io = sub['inst']
    cov = np.asarray(sub['ptfe_cov'], bool)
    ncov = np.bincount(io[cov], minlength=nI) if nI else np.zeros(0, np.int64)
    k = np.asarray(inst['nsub'], np.int64)
    return {'n_subedges': int(nS), 'n_subedges_long': (int(np.sum(np.asarray(inst['long'], bool)[io])) if nS else 0),
            'n_subedges_ptfe_cov': int(cov.sum()), 'n_instances_ptfe_partial': int(np.sum((ncov > 0) & (ncov < k))),
            'n_subedges_sdcp_near': int(np.sum(np.asarray(sub['a_sdcp'], bool))),
            'n_subedges_unrealized': int(np.sum(~np.asarray(sub['realized'], bool))),
            'n_port_ties': int(np.sum(sub['tie_i']) + np.sum(sub['tie_j'])), 'subedge_rule': CJUNC_DIST_RULE}


def _census(inst, pos, ft, cell_lin, cell_ptr, cell_pos, sid, flat, owner_ties, multi_site, n_cut_site, n_unreg, segs, nfib,
            npiece, rf):
    cnt = np.diff(cell_ptr)
    if len(cell_pos):                                        # ★ 고리 이음매 별칭 = 같은 위치 (교차 셀 수에서 뺀다)
        al = (pos['alias'][cell_pos] >= 0).astype(np.int64)
        cnt = cnt - np.add.reduceat(al, cell_ptr[:-1]) if len(cnt) else cnt
    nI = len(inst['fi'])
    real = inst['realized']
    rel = {'same_cell': 0, 'face': 0, 'edge': 0, 'corner': 0, 'apart': 0}
    for k in np.flatnonzero(real):
        d = np.abs(pos['ijk'][inst['port_i'][k]] - pos['ijk'][inst['port_j'][k]])
        s = int(d.sum()); mx = int(d.max())
        rel['same_cell' if s == 0 else ('face' if s == 1 and mx == 1 else
                                         ('edge' if s == 2 and mx == 1 else ('corner' if s == 3 and mx == 1 else 'apart')))] += 1
    reasons = {}
    for r_ in inst['reason'][~real]:
        reasons[str(r_)] = reasons.get(str(r_), 0) + 1
    vx_by = {}
    vx = ft['kind'] == K_VX
    if vx.any():
        n3 = np.array(sid.shape)
        stride = np.array([n3[1] * n3[2], n3[2], 1])
        la = ft['lin'][vx]; lb = la + stride[ft['ax'][vx]]
        other = np.where(ft['pa'][vx] >= 0, flat[lb], flat[la])
        for s_, c_ in zip(*np.unique(other, return_counts=True)):
            vx_by[_SID_NAME.get(int(s_), str(int(s_)))] = int(c_)
    gap = inst['d0'][~inst['self']] - 2.0 * rf
    lc = inst['Lc']
    dk = inst['self_dk_min'][inst['self'] & (inst['self_dk_min'] >= 0)]
    return {'n_vgcf_fibres': int(nfib), 'n_pieces': int(npiece), 'n_segments': int(len(segs['P0'])),
            'n_positions': int(len(pos['lin'])), 'n_live_positions': int(np.sum(pos['live'])),
            'n_cross_cells': int(np.sum(cnt >= 2)), 'n_kway_cells_ge3': int(np.sum(cnt >= 3)),
            'n_instances': int(nI), 'n_instances_distinct': int(np.sum(~inst['self'])),
            'n_instances_self': int(np.sum(inst['self'])), 'n_realized': int(np.sum(real)), 'n_unrealized_by_reason': reasons,
            'n_port_ties': int(np.sum(inst['tie_i']) + np.sum(inst['tie_j'])), 'n_port_displaced': int(np.sum(inst['port_displaced'])),
            'port_relation': rel, 'n_cut_site_faces': int(n_cut_site), 'n_unreg_faces': int(n_unreg),
            'n_cut_self_faces': int(np.sum(ft['kind'] == K_CUT_SELF)), 'n_vx_faces_by_sid': vx_by,
            'owner_tie_noncanonical': int(owner_ties), 'n_faces_multi_site': int(multi_site),
            'surface_gap_um': ({'min': float(gap.min()), 'median': float(np.median(gap)), 'max': float(gap.max())}
                               if len(gap) else None),
            'Lc_um': ({'min': float(lc.min()), 'median': float(np.median(lc)), 'p90': float(np.quantile(lc, 0.90)),
                       'p99': float(np.quantile(lc, 0.99)), 'max': float(lc.max())} if len(lc) else None),
            #  길이 법칙 v0 배율 (max(1, L_c/L_par)) — 합 · 최댓값 · 1 넘는 수 (긴 접촉이 σ 에 얼마나 들어가는가 · S0 용)
            'len_mult': ({'sum': float(np.sum(inst['mult'])), 'max': float(np.max(inst['mult'])),
                          'n_gt1': int(np.sum(inst['mult'] > 1.0))} if len(lc) else None),
            #  긴 접촉이 꺾임 (같은 조각 · 경로 간격 작음) 에서 생기는지 고리 · 머리핀 (간격 큼) 에서 생기는지 가르는 진단 (S0 용 · 판정 아님)
            'n_long_distinct': int(np.sum(inst['long'] & ~inst['self'])) if 'long' in inst else None,
            'n_long_self': int(np.sum(inst['long'] & inst['self'])) if 'long' in inst else None,
            'self_dk_min': ({'min': int(dk.min()), 'median': float(np.median(dk)), 'max': int(dk.max()),
                             'n_le_4': int(np.sum(dk <= 4))} if len(dk) else None)}


def _sdcp_bridging(sid, ft, pos, n):
    """SDCP 경유 섬유 연결 수 (설계 §2 · §4-5) — SDCP 셀 6-면 성분 중 서로 다른 VGCF fid 둘 이상의 셀과 면으로 닿는 성분 · 이어지는 fid 쌍."""
    s5 = sid == 5
    if not s5.any():
        return {'n_sdcp_bridging_components': 0, 'n_sdcp_bridged_fid_pairs': 0}
    lab, _ = ndimage.label(s5)
    flat = sid.reshape(-1)
    labf = lab.reshape(-1)
    stride = np.array([n[1] * n[2], n[2], 1])
    vx = ft['kind'] == K_VX
    la = ft['lin'][vx]; lb = la + stride[ft['ax'][vx]]
    a_is3 = ft['pa'][vx] >= 0
    lin3 = np.where(a_is3, la, lb); lin5 = np.where(a_is3, lb, la)
    m = flat[lin5] == 5
    comp = {}
    order = np.argsort(pos['lin'])
    plin = pos['lin'][order]
    for c3, c5 in zip(lin3[m], lin5[m]):
        a0 = np.searchsorted(plin, c3, 'left'); a1 = np.searchsorted(plin, c3, 'right')
        fids = {int(pos['fid'][order[x]]) for x in range(a0, a1) if pos['live'][order[x]]}
        comp.setdefault(int(labf[c5]), set()).update(fids)
    nb = 0
    pairs = set()
    for fs in comp.values():
        if len(fs) >= 2:
            nb += 1
            fs = sorted(fs)
            for x in range(len(fs)):
                for y in range(x + 1, len(fs)):
                    pairs.add((fs[x], fs[y]))
    return {'n_sdcp_bridging_components': int(nb), 'n_sdcp_bridged_fid_pairs': int(len(pairs))}


def _sv_split(sid, ft, pos, piece_pos, segs, n, lo, vox, D, s_min):
    """★ 10-21 (사전 리뷰 PRE-impl-04 · 1저자 Q-D · `CJUNC_SV_CF_RULE`) — SV 반사실 대조가 끊을 SV 면 (면 행마다 'sv_cut') · census.
    SDCP 6-면 성분마다 SV 면 (VGCF 셀 ↔ 그 성분 SDCP 셀) 의 VGCF 주인 위치를 무리 짓는다: 같은 조각이고 (그 사이 위치가 전부 덮인 채
    그 성분 셀이다 — 섬유가 성분을 지난다 · 또는 두 위치가 같은 가닥의 연속 (`_continuity`)).  무리마다 '지남' = 덮인 채 지나는 이음이
    하나라도 있다.  끊을 행 = `_sv_cut_rows` (무리 둘 이상 = 다리 · 지나는 무리 하나 이하 → 지나지 않는 무리의 행).  → (행 마스크, census)."""
    nr = len(ft['lin'])
    cut = np.zeros(nr, bool)
    cen = {'n_sdcp_components_touching': 0, 'n_bridging_components': 0, 'n_sv_faces_cut_rows': 0,
           'n_sv_faces_kept_self': 0, 'n_unsplit_bridging_components': 0, 'sv_cf_rule': CJUNC_SV_CF_RULE}
    s5 = np.asarray(sid) == 5
    if not s5.any() or nr == 0:
        return cut, cen
    lab, _ = ndimage.label(s5)
    labf = lab.reshape(-1)
    flat = np.asarray(sid).reshape(-1)
    stride = np.array([n[1] * n[2], n[2], 1], np.int64)
    vx = np.flatnonzero(ft['kind'] == K_VX)
    la = ft['lin'][vx]; lb = la + stride[ft['ax'][vx]]
    a3 = ft['pa'][vx] >= 0
    lin5 = np.where(a3, lb, la)
    own = np.where(a3, ft['pa'][vx], ft['pb'][vx])
    m = (flat[lin5] == 5) & (own >= 0)
    rows = vx[m]
    if len(rows) == 0:
        return cut, cen
    comp = labf[lin5[m]].astype(np.int64)
    own = own[m].astype(np.int64)
    #  무리 — 같은 성분 · 같은 조각 주인 쌍마다 (사이 위치가 전부 덮인 채 그 성분 셀 = 지남 · 또는 연속)
    uf = _UF()
    passing_root = set()
    oc = sorted({(int(c), int(p)) for c, p in zip(comp, own)})
    by_c = {}
    for c, p in oc:
        by_c.setdefault(c, []).append(p)
        uf.find((c, p))
    for c, ps in by_c.items():
        for x in range(len(ps)):
            for y in range(x + 1, len(ps)):
                p, q = ps[x], ps[y]
                if pos['piece'][p] != pos['piece'][q]:
                    continue
                a0, a1 = piece_pos[int(pos['piece'][p])]
                kp, kq = int(pos['k'][p]), int(pos['k'][q])
                lo_k, hi_k = min(kp, kq), max(kp, kq)
                runs = [np.arange(a0 + lo_k + 1, a0 + hi_k)]
                if pos['ring'][p]:
                    ng = int(pos['piece_ng'][p])
                    runs.append(np.r_[np.arange(a0 + hi_k + 1, a0 + ng), np.arange(a0, a0 + lo_k)])
                through = False
                for btw in runs:
                    btw = btw[pos['alias'][btw] < 0] if len(btw) else btw
                    if len(btw) and np.all(~pos['live'][btw]) and np.all(pos['lin'][btw] >= 0) \
                            and np.all(labf[np.maximum(pos['lin'][btw], 0)] == c):
                        through = True
                if through:
                    uf.union((c, p), (c, q))
                    passing_root.add((c, p))
                    continue
                s_, d_ = _pos_pair_sd(p, q, pos, segs, lo, vox)
                if bool(np.asarray(_continuity(s_, d_, D, s_min))):
                    uf.union((c, p), (c, q))
    pas_root = {uf.find(x) for x in passing_root}
    roots = [uf.find((int(c), int(p))) for c, p in zip(comp, own)]
    gid = {}
    grp = np.asarray([gid.setdefault(r, len(gid)) for r in roots], np.int64)
    pas = np.asarray([r in pas_root for r in roots], bool)
    mask = np.asarray(_sv_cut_rows({'comp': comp, 'group': grp, 'passing': pas}), bool).reshape(len(rows))
    cut[rows[mask]] = True
    ncomp_touch = len(np.unique(comp))
    nbridge = nunsplit = kept_self = 0
    for c in np.unique(comp):
        mc = comp == c
        if len(np.unique(grp[mc])) < 2:
            continue
        nbridge += 1
        if len(np.unique(grp[mc & pas])) >= 2:
            nunsplit += 1
            continue
        kept_self += int(np.sum(mc & pas & ~mask))
    cen.update(n_sdcp_components_touching=int(ncomp_touch), n_bridging_components=int(nbridge),
               n_sv_faces_cut_rows=int(mask.sum()), n_sv_faces_kept_self=int(kept_self),
               n_unsplit_bridging_components=int(nunsplit))
    return cut, cen


# ═════════════════════════ 계획 ═════════════════════════
def plan_rows_fp(plan):
    parts = [plan['mode'], plan['g_code'], plan['rj_eff'], plan['mult'], plan['registry']['fp']['registry'], plan['unreg_law'],
             plan['ptfe_jlaw'], plan['ptfe_stamp'], plan['sdcp_mod'], plan['quantitative']]
    if plan.get('sv_counterfactual') is not None:           # ★ 10-21 RCA-06 — 노브를 켠 계획만 (끈 계획의 지문은 옛 꼴 그대로)
        parts.append(('sv_counterfactual', plan['sv_counterfactual']))
    return _fp(*parts)


def _sv_cf_request(v):
    """반사실 대조 노브 (10-21 RCA-06 · Q4 (가)) — None (끔 · 기본) 또는 {'threshold': None | 유한 ≥ 1 실수}.  문턱 = 기본값 없음
    (등록이 채운다) · 문턱이 있을 때만 `SV_DEPENDENT` 비교 표지 (비 = G_full/G_SV끊음 ≥ 1 이 Rayleigh 로 늘 성립 → 문턱 < 1 은 뜻 없음 = 거부)."""
    if v is None:
        return None
    if not isinstance(v, dict) or set(v) != {'threshold'}:
        raise TypeError(f"cjunc_plan: sv_counterfactual = {{'threshold': None | 실수 ≥ 1}} 만: {v!r}")
    t = v['threshold']
    if t is None:
        return {'threshold': None}
    if isinstance(t, (bool, np.bool_)) or not isinstance(t, (int, float, np.floating, np.integer)):
        raise TypeError(f'cjunc_plan: sv_counterfactual 문턱 = 실수: {t!r}')
    try:
        tf = float(t)
    except OverflowError:                                    # float 로 못 옮기는 큰 정수 (10**400) — 거부 계약 (ValueError) 으로
        raise ValueError(f'cjunc_plan: sv_counterfactual 문턱 = 유한 ≥ 1 (float 넘침): {t!r}') from None
    if not (math.isfinite(tf) and tf >= 1.0):
        raise ValueError(f'cjunc_plan: sv_counterfactual 문턱 = 유한 ≥ 1 (비 G_full/G_cut ≥ 1 · Rayleigh): {t!r}')
    return {'threshold': tf}


def cjunc_plan(reg, R_j_ohm, *, unreg_law, ptfe_stamp, ptfe_jlaw='P0', sdcp_mod=None, quantitative=True,
               allow_rj_limits=False, rj_reference=RJ_REFERENCE_PLANE, lead_subtraction=None, sv_counterfactual=None):
    """분산 간선 (원장 'subedges') 마다 간선 (g = 1e4·m/(k·R_j′) · m = 길이 법칙 v0 배율 · k = 그 instance 의 간선 수) · 축약 (R_j′ = 0) ·
    절단 (P1 · 간선마다 덮임) · 미실현.  S3 = sdcp_mod {'c': c} (간선마다 근접 · S2 원장 없이 = 거부).  정량 (quantitative=True): R_j 유한
    > 0 (극한 0 · ∞ = allow_rj_limits 사다리 진단 전용) · c ∈ {0, 1} · 원장 거부 사유 (s_min 미등록 포함) = 거부.  긴 접촉은 거부하지
    않는다 (옛 J8 · 길이 법칙 + 분산판 v0 이 맡는다 · 수는 기록).  sv_counterfactual = 반사실 대조 노브 (`_sv_cf_request` · 기본 끔).
    ★ 10-21 (사전 리뷰 PRE-impl-03 · 1저자 Q-C) — ptfe_stamp centerline = 거부 (시험 모드 포함 · 접합은 off · face_alpha 에서만)."""
    if not isinstance(reg, dict) or reg.get('kind') != 'cjunc_registry':
        raise TypeError('cjunc_plan: 원장은 cjunc_registry 의 결과여야 한다 (S3 = S2 원장 없이 거부 · 설계 §5-2)')
    if registry_fp(reg) != reg.get('fp', {}).get('registry'):
        raise ValueError('cjunc_plan: 원장이 만든 뒤 바뀌었다 (지문 불일치 · E5)')
    if rj_reference != RJ_REFERENCE_PLANE:
        raise ValueError(f'cjunc_plan: R_j 기준면 {rj_reference!r} — v0 는 모형 내부값 ({RJ_REFERENCE_PLANE}) 만 받는다 (T1-5′ · J4)')
    if lead_subtraction is not None:
        raise ValueError('cjunc_plan: 리드 빼기 (단자 기준 R_j) = v0 미지원 · 거부 (T1-5′ — 실측 순접촉값 주장 없음)')
    if isinstance(R_j_ohm, bool) or not isinstance(R_j_ohm, (int, float, np.floating, np.integer)):
        raise TypeError(f'cjunc_plan: R_j = 실수 (Ω): {R_j_ohm!r}')
    R0 = float(R_j_ohm)
    if math.isnan(R0) or R0 < 0.0:
        raise ValueError(f'cjunc_plan: R_j 는 NaN · 음수일 수 없다: {R_j_ohm!r}')
    if (R0 == 0.0 or math.isinf(R0)) and not allow_rj_limits:
        raise ValueError('cjunc_plan: R_j 극한 (0 = 사다리 천장 축약 · ∞ = 바닥) 은 allow_rj_limits 표지 (사다리 진단) 와만 — 정량 거부')
    if unreg_law not in UNREG_LAWS:
        raise ValueError(f'cjunc_plan: 미등록 VV 면 법칙 {unreg_law!r} — 선언 필수 {UNREG_LAWS} (자동 fallback 없음 · v2 §3-6)')
    if ptfe_stamp not in PTFE_STAMPS:
        raise ValueError(f'cjunc_plan: ptfe_stamp 선언 필수 {PTFE_STAMPS}: {ptfe_stamp!r}')
    if ptfe_stamp == 'centerline':
        raise ValueError('cjunc_plan: 접합 + ptfe_stamp centerline = 거부 (10-21 사전 리뷰 PRE-impl-03 · 1저자 Q-C — centerline 은 VGCF 셀을 '
                         'sid 7 로 덮는다: 옛 판은 덮인 접점의 포트를 옆 셀로 옮겨 절연체를 더해 σ 가 올랐다 (Rayleigh 위반) · '
                         '접합은 off · face_alpha 에서만)')
    if ptfe_jlaw not in PTFE_JLAWS:
        raise ValueError(f'cjunc_plan: PTFE–접합 법칙 {ptfe_jlaw!r} ∉ {PTFE_JLAWS}')
    if ptfe_jlaw == 'P1' and ptfe_stamp != 'face_alpha':
        raise ValueError(f'cjunc_plan: P1 은 face_alpha 에서만 ({ptfe_stamp} — off 는 PTFE 표현이 없다 · 설계 §4-1)')
    svc = _sv_cf_request(sv_counterfactual)
    c = None
    if sdcp_mod is not None:
        if not isinstance(sdcp_mod, dict) or set(sdcp_mod) - {'c'} or 'c' not in sdcp_mod:
            raise TypeError(f"cjunc_plan: sdcp_mod = {{'c': c}} 만: {sdcp_mod!r}")
        cv = sdcp_mod['c']
        if isinstance(cv, bool) or not isinstance(cv, (int, float, np.floating, np.integer)):
            raise TypeError(f'cjunc_plan: c = 실수: {cv!r}')
        c = float(cv)
        if not (math.isfinite(c) and 0.0 <= c <= 1.0):
            raise ValueError(f'cjunc_plan: c ∈ [0, 1] 유한: {cv!r}')
        if quantitative and c not in (0.0, 1.0):
            raise ValueError(f'cjunc_plan: 정량 R 런의 c 는 {{0, 1}} 만 (시험 격자는 quantitative=False): {c}')
    inst = reg['instances']
    sub = reg['subedges']
    nI = len(inst['fi'])
    nS = len(sub['inst'])
    mult = np.asarray(inst['mult'], np.float64).copy()       # 길이 법칙 v0 (원장에서 한 번 · 계획은 읽기만)
    if not (np.isfinite(mult).all() and (mult >= 1.0).all()):
        raise ValueError('cjunc_plan: 길이 법칙 배율은 유한 · ≥ 1 이어야 한다 (max(1, L_c/L_par)) — 원장 이상')
    kk = np.asarray(inst['nsub'], np.int64)
    io = np.asarray(sub['inst'], np.int64)
    if len(kk) != nI or (nI and (kk < 1).any()) or int(kk.sum()) != nS or (nS and not np.array_equal(np.bincount(io, minlength=nI), kk)):
        raise ValueError('cjunc_plan: 분산 간선 표 ↔ instance 간선 수 (k) 가 맞지 않는다 — 원장 이상')
    mode = np.zeros(nS, np.int64)
    g = np.zeros(nS, np.float64)
    rje = np.full(nS, np.nan)
    a = np.asarray(sub['a_sdcp'], bool).astype(np.float64)
    for e in range(nS):
        q = int(io[e])
        if not sub['realized'][e]:
            mode[e] = MODE_UNREALIZED
            continue
        if ptfe_jlaw == 'P1' and sub['ptfe_cov'][e]:
            mode[e] = MODE_CUT_P1                            # N18 — 덮인 간선은 c 와 무관하게 먼저 절단 (간선마다 · RCA-05)
            continue
        if c is not None and math.isinf(R0) and c * a[e] == 1.0:
            r = 0.0                                          # Z3 — 바닥 (R_j,0 = ∞) 의 c = 1 근접 = 축약 (∞·0 = NaN 금지 · 유한 R_j,0 은 아래 식 그대로)
        else:
            r = R0 if c is None else float(sdcp_rj_eff(R0, c, a[e]))
        rje[e] = r
        if r == 0.0:
            mode[e] = MODE_CONTRACT
        elif math.isinf(r):
            mode[e] = MODE_NONE_INF
        else:
            mode[e] = MODE_EDGE
            g[e] = float(junction_g_code(r)) * float(mult[q]) / float(kk[q])   # 간선 G = (max(1, L_c/L_par) / R_j′)/k (분산판 v0)
    long = np.asarray(inst['long'], bool)
    rej = [dict(x) for x in reg['rejections']]               # 긴 접촉 = 거부 아님 (길이 법칙 v0 · 1저자 10-20 Q17)
    if not quantitative:
        rej = []
    near = int(np.sum(np.asarray(sub['a_sdcp'], bool) & np.asarray(sub['realized'], bool)))
    share = (mult[io] / kk[io]) if nS else np.zeros(0)       # 간선마다 배율 몫 (m/k) — k 1 = 옛 instance 배율 그대로
    counts = {'n_instances': nI, 'n_subedges': nS, 'n_edge': int(np.sum(mode == MODE_EDGE)),
              'n_contract': int(np.sum(mode == MODE_CONTRACT)),
              'n_cut_p1': int(np.sum(mode == MODE_CUT_P1)), 'n_unrealized': int(np.sum(mode == MODE_UNREALIZED)),
              'n_none_inf': int(np.sum(mode == MODE_NONE_INF)), 'n_long': int(np.sum(long)), 'n_sdcp_near': near,
              'n_contracted_by_c': int(np.sum((mode == MODE_CONTRACT) & (R0 > 0.0))),
              'n_ptfe_cov': int(np.sum(np.asarray(sub['ptfe_cov'], bool))),
              'len_mult_sum_edge': float(np.sum(share[mode == MODE_EDGE])),
              'len_mult_max': (float(np.max(mult)) if nI else None)}
    record = {'model': CJUNC_MODEL_VERSION, 'schema': CJUNC_SCHEMA, 'status': CJUNC_STATUS,
              'qualifiers': list(CJUNC_QUALIFIERS), 'R_j_ohm': (R0 if math.isfinite(R0) else 'inf'),
              'len_law': CJUNC_LEN_LAW, 'dist_rule': CJUNC_DIST_RULE, 's_min_um': reg['thresholds']['s_min_um'],
              'rj_reference_plane': RJ_REFERENCE_PLANE, 'half_cell_in_edge': False, 'unreg_law': unreg_law,
              'ptfe_jlaw': ptfe_jlaw, 'ptfe_stamp': ptfe_stamp,
              'sdcp_mod': (None if c is None else {'c': c, 'tol_sj_um': reg['thresholds']['tol_sj_um'],
                                                   'r_sdcp_um': reg['thresholds']['r_sdcp_um']}),
              's3_discriminating': (None if c is None else bool(near > 0)),
              'sv_counterfactual_request': (None if svc is None else dict(svc)),
              'quantitative': bool(quantitative), 'allow_rj_limits': bool(allow_rj_limits),
              'thresholds': dict(reg['thresholds']), 'rules': dict(reg['rules']), 'census': dict(reg['census']),
              'counts': counts, 'fp_registry': reg['fp']['registry'], 'fp_sid': reg['fp']['sid']}
    plan = {'kind': 'cjunc_plan', 'version': CJUNC_MODEL_VERSION, 'registry': reg, 'mode': mode, 'g_code': g, 'rj_eff': rje,
            'mult': mult, 'unreg_law': unreg_law, 'ptfe_jlaw': ptfe_jlaw, 'ptfe_stamp': ptfe_stamp,
            'sdcp_mod': (None if c is None else {'c': c}), 'quantitative': bool(quantitative), 'rejections': rej,
            'sv_counterfactual': svc, 'record': record}
    plan['fp_rows'] = plan_rows_fp(plan)
    return plan


def cjunc_require_quantitative(plan, sid, vox, sigma_of_sid=None, rint=None, iface=None, periodic_xy=False,
                               return_field=False):
    """솔브 입구 관문 (조립 전 · CG 0) — 계획 모양 · 지문 · 불변량 · 거부 사유 · 동시 사용 · 격자 결합 · 채널 · ★ 10-21 PTFE 규약
    (centerline = 거부 · Q-C)."""
    if not isinstance(plan, dict) or plan.get('kind') != 'cjunc_plan':
        raise TypeError('cjunc 는 cjunc_plan 의 결과여야 한다 (S3 sdcp_mod 단독 = 거부)')
    if plan.get('version') != CJUNC_MODEL_VERSION or plan.get('record', {}).get('schema') != CJUNC_SCHEMA:
        raise ValueError(f"cjunc: 다른 판본 계획 ({plan.get('version')!r}) — 거부")
    reg = plan['registry']
    if registry_fp(reg) != reg['fp']['registry']:
        raise ValueError('cjunc: 원장이 계획 뒤 바뀌었다 (지문 · E5)')
    if plan_rows_fp(plan) != plan.get('fp_rows'):
        raise ValueError('cjunc: 계획 행이 만든 뒤 바뀌었다 (지문 · E5)')
    if plan.get('ptfe_stamp') not in ('off', 'face_alpha') or plan.get('record', {}).get('ptfe_stamp') != plan.get('ptfe_stamp'):
        raise ValueError(f"cjunc: ptfe_stamp {plan.get('ptfe_stamp')!r} (기록 {plan.get('record', {}).get('ptfe_stamp')!r}) — 접합은 off · "
                         f'face_alpha 에서만 (centerline = 거부 · 10-21 사전 리뷰 PRE-impl-03 · Q-C · 조립 전)')
    if reg.get('rules', {}).get('len_law') != CJUNC_LEN_LAW or plan.get('record', {}).get('len_law') != CJUNC_LEN_LAW:
        raise ValueError(f"cjunc: 다른 접합 길이 법칙의 원장 · 계획 ({reg.get('rules', {}).get('len_law')!r}) — "
                         f'{CJUNC_LEN_LAW} 만 (옛 점 접합 · J8 거부 판 섞임 거부)')
    g = np.asarray(plan['g_code'], np.float64)
    mode = np.asarray(plan['mode'], np.int64)
    sub = reg.get('subedges') if isinstance(reg.get('subedges'), dict) else None
    if sub is None or g.shape != mode.shape or len(g) != len(sub['inst']):
        raise ValueError('cjunc: 계획 행 ↔ 원장 분산 간선 표 모양 불일치 (간선마다 한 행 · cjunc-v2) — 조립 전 거부')
    e = mode == MODE_EDGE
    if not (np.isfinite(g).all() and (g >= 0.0).all() and (g[e] > 0.0).all()):
        raise ValueError('cjunc: 계획 간선 g 는 유한 · 0 이상 (간선 행 > 0) — NaN · 음수 · inf = 조립 전 거부 (Q7 와 같은 꼴 · 지문을 다시 만든 변이도)')
    m = np.asarray(plan.get('mult'), np.float64)
    nI = len(reg['instances']['fi'])
    if m.shape != (nI,) or not (np.isfinite(m).all() and (m >= 1.0).all()):
        raise ValueError('cjunc: 계획 배율 (길이 법칙 v0) 은 instance 마다 유한 · ≥ 1 — 조립 전 거부')
    io = np.asarray(sub['inst'], np.int64)
    kk = np.asarray(reg['instances']['nsub'], np.float64)
    if e.any() and not np.array_equal(g[e], junction_g_code(np.asarray(plan['rj_eff'], np.float64)[e]) * m[io[e]] / kk[io[e]]):
        raise ValueError('cjunc: 계획 간선 g ≠ 1e4·m/(k·R_j′) — 배율 · 간선 수 기록과 쓰는 값이 묶이지 않았다 (지문을 다시 만든 변이 · '
                         '조립 전 거부)')
    if plan.get('sv_counterfactual') is not None and _sv_cf_request(plan['sv_counterfactual']) != plan['sv_counterfactual']:
        raise ValueError('cjunc: 반사실 대조 노브 모양 이상 — 조립 전 거부')
    if plan['rejections']:
        raise ValueError('cjunc 정량 모드 거부 — ' + ' · '.join(f"{x['code']}(n={x.get('n')})" for x in plan['rejections']))
    if rint:
        raise ValueError('cjunc: r1 탐침 표 (--step3-rint-e/-i) 와 동시 사용 거부 (설계 §4-3)')
    if iface is not None:
        raise ValueError('cjunc: ①′ AM–AM 막 (iface) 과 동시 사용 거부 (생산 HOLD · 설계 §4-3)')
    if periodic_xy:
        raise ValueError('cjunc: 주기 경계 정량 거부 (raster 가 주기 영상을 안 만든다 · J10)')
    if return_field:
        raise ValueError('cjunc v0 = σ_e 전용 — 장 · je · 분담 · Joule 진단은 원장을 읽기 전이라 거부 (return_field · 설계 §3-3 · §7 LEAN 4)')
    if tuple(np.asarray(sid).shape) != tuple(reg['shape']) or _grid_fp(sid) != reg['fp']['sid']:
        raise ValueError('cjunc: 다른 격자 (sid 지문 · 모양) — 원장을 그 sid 에서 다시 만들 것 (E5)')
    v = float(vox)
    if not (math.isfinite(v) and v == float(reg['vox'])):
        raise ValueError(f"cjunc: 솔버 vox {vox!r} ≠ 원장 vox {reg['vox']!r} (RIMP-05 와 같은 부류)")
    if sigma_of_sid is not None:
        a = np.asarray(sigma_of_sid, np.float64)
        s = np.asarray(sid)
        bad = (not (a.shape[0] > 3 and a[3] > 0.0)) if a.ndim == 1 else (not (a[s == 3] > 0.0).all())
        if bad and len(reg['positions']['lin']):
            raise ValueError('cjunc: 이 채널에서 VGCF 절연 (σ_VGCF = 0 · 이온 표) — 접합 요청은 전자 채널뿐 (조용한 무효 금지)')
    return plan


# ═════════════════════════ 조립 (solve_sigma_z 훅) ═════════════════════════
_CAT = {'other_bulk': 0, 'vv_axial': 1, 'vv_unreg_fused': 2, 'va_face': 3, 'sv_face': 4, 'vx_other': 5, 'vv_junction': 6,
        'vv_self_fused': 7}
_CAT_NAME = {v: k for k, v in _CAT.items()}


class CjuncAssembler:
    """`solve_sigma_z` 가 셀 dof 로 만든 면 (couple) · 판 결합을 받아 멤버십 dof · 접합 간선 · 절단 · 축약 · 실제 그래프 가지치기를
    한 계를 만든다 (J1 · J3 · J5 · J6 · J7 · J9 · J11 · J12 · E1 · E3 · E6)."""

    def __init__(self, plan, sid, cond, idx, n_cells, sig, vox):
        self.plan = plan
        self.reg = reg = plan['registry']
        self.sid = sid
        self.flat = np.asarray(sid).reshape(-1)
        self.sigf = np.asarray(sig, np.float64).reshape(-1)
        self.vox = float(vox)
        self.cells_lin = np.flatnonzero(np.asarray(cond).reshape(-1))
        self.n_cells = int(n_cells)
        pos = reg['positions']
        live = pos['live'].copy()
        if live.any() and not np.asarray(cond).reshape(-1)[pos['lin'][live]].all():
            raise ValueError('cjunc: 멤버십 셀이 이 채널에서 도체가 아니다 (σ_VGCF > 0 이어야 · 조용한 무효 금지)')
        alias = np.asarray(pos.get('alias', np.full(len(pos['lin']), -1)), np.int64)
        self.pos_dof = np.full(len(pos['lin']), -1, np.int64)
        prim = pos['primary']
        self.pos_dof[prim] = np.asarray(idx).reshape(-1)[pos['lin'][prim]]
        extra = np.flatnonzero(live & ~prim & (alias < 0))
        self.pos_dof[extra] = self.n_cells + np.arange(len(extra))
        al = np.flatnonzero(live & (alias >= 0))              # ★ 10-21 (Q-A) 고리 이음매 별칭 = 목표 위치의 dof (이음매 = 연속)
        self.pos_dof[al] = self.pos_dof[alias[al]]
        self.n_total = self.n_cells + len(extra)
        ft = reg['faces']
        self.ft = ft
        self.tkey = ft['key']
        self.E = []                                          # (u, v, g, cat, sa, sb, sida, sidb, 간선 행, 반사실 끊음)
        self.tomb = {'cut_site': 0, 'cut_self': 0, 'unreg_cut': 0}
        self.n_unreg_fused = 0
        self.n_self_fused = 0

    def add_faces(self, axis, a2, b2, g):
        if axis is None:
            raise ValueError('cjunc: 주기 면 (axis None) — 정량 거부 (입구에서 막혀야 한다)')
        a2 = np.asarray(a2, np.int64); b2 = np.asarray(b2, np.int64); g = np.asarray(g, np.float64)
        la = self.cells_lin[a2]; lb = self.cells_lin[b2]
        key = la * 3 + axis
        lo_ = np.searchsorted(self.tkey, key, 'left'); hi_ = np.searchsorted(self.tkey, key, 'right')
        hit = hi_ > lo_
        pt = ~hit
        if pt.any():
            self._emit(a2[pt], b2[pt], g[pt], np.full(int(pt.sum()), _CAT['other_bulk']), la[pt], lb[pt])
        if not hit.any():
            return
        fh = np.flatnonzero(hit)
        nr = (hi_ - lo_)[fh]
        fi = np.repeat(fh, nr)
        row = np.repeat(lo_[fh], nr) + (np.arange(len(fi)) - np.repeat(np.cumsum(nr) - nr, nr))
        kind = self.ft['kind'][row]
        pa = self.ft['pa'][row]; pb = self.ft['pb'][row]
        svc = np.asarray(self.ft.get('sv_cut', np.zeros(len(self.ft['kind']), bool)), bool)[row]
        m = kind == K_AXIAL
        if m.any():
            self._emit(self.pos_dof[pa[m]], self.pos_dof[pb[m]], g[fi[m]], np.full(int(m.sum()), _CAT['vv_axial']),
                       la[fi[m]], lb[fi[m]])
        m = kind == K_VX
        if m.any():
            u = np.where(pa[m] >= 0, self.pos_dof[np.maximum(pa[m], 0)], a2[fi[m]])
            v = np.where(pb[m] >= 0, self.pos_dof[np.maximum(pb[m], 0)], b2[fi[m]])
            sa_, sb_ = self.flat[la[fi[m]]], self.flat[lb[fi[m]]]
            pair = np.minimum(sa_, sb_) * 10 + np.maximum(sa_, sb_)
            cat = np.where(np.isin(pair, (13, 23)), _CAT['va_face'], np.where(pair == 35, _CAT['sv_face'], _CAT['vx_other']))
            self._emit(u, v, g[fi[m]], cat, la[fi[m]], lb[fi[m]], cf=svc[m] & (cat == _CAT['sv_face']))
        m = kind == K_UNREG
        if m.any():
            if self.plan['unreg_law'] == 'fused':
                self._emit(self.pos_dof[pa[m]], self.pos_dof[pb[m]], g[fi[m]], np.full(int(m.sum()), _CAT['vv_unreg_fused']),
                           la[fi[m]], lb[fi[m]])
                self.n_unreg_fused += int(m.sum())
            else:
                self.tomb['unreg_cut'] += int(m.sum())
        m = kind == K_SELF_FUSED
        if m.any():                                          # 같은 가닥의 연속 (바닥 밖 · s < s_min) — 옛 복셀 융합 그대로 (접합 아님)
            self._emit(self.pos_dof[pa[m]], self.pos_dof[pb[m]], g[fi[m]], np.full(int(m.sum()), _CAT['vv_self_fused']),
                       la[fi[m]], lb[fi[m]])
            self.n_self_fused += int(m.sum())
        self.tomb['cut_site'] += int(np.sum(kind == K_CUT_SITE))
        self.tomb['cut_self'] += int(np.sum(kind == K_CUT_SELF))

    def _emit(self, u, v, g, cat, la, lb, cf=None):
        u = np.asarray(u, np.int64)
        cfa = np.zeros(len(u), bool) if cf is None else np.asarray(cf, bool).reshape(len(u))
        self.E.append((u, np.asarray(v, np.int64), np.asarray(g, np.float64), np.asarray(cat, np.int64), self.sigf[la],
                       self.sigf[lb], self.flat[la], self.flat[lb], np.full(len(u), -1, np.int64), cfa))

    def _plate_owner(self, A, top):
        """판 결합 셀이 VGCF (멤버십) 이면 판 쪽 면 중심에 최근접 멤버십 dof (J9) — 아니면 그대로."""
        A = np.asarray(A, np.int64)
        if len(A) == 0:
            return A
        reg = self.reg
        pos = reg['positions']
        lin = self.cells_lin[A]
        j = np.searchsorted(reg['cell_lin'], lin)
        okj = j < len(reg['cell_lin'])
        okj[okj] = reg['cell_lin'][j[okj]] == lin[okj]
        if not okj.any():
            return A
        q = np.flatnonzero(okj)
        a0 = reg['cell_ptr'][j[q]]; cnt = reg['cell_ptr'][j[q] + 1] - a0
        qq = np.repeat(q, cnt)
        off = np.arange(len(qq)) - np.repeat(np.cumsum(cnt) - cnt, cnt)
        pp = reg['cell_pos'][np.repeat(a0, cnt) + off]
        ijk = np.stack(np.unravel_index(lin, reg['shape']), 1).astype(np.float64)
        X = reg['lo'] + (ijk + 0.5) * self.vox
        X[:, 2] += (0.5 if top else -0.5) * self.vox
        own, _ = _owner_select(qq, pp, X, pos, reg['segments'], len(A))
        out = A.copy()
        sel = own >= 0
        out[sel] = self.pos_dof[own[sel]]
        return out

    def build(self, Ab, gb, At, gt, cb=None, ct=None):
        """주 계 — 멤버십 dof · 분산 접합 간선 · 축약 · 절단 · 실제 그래프 가지치기 · 관통 · 단락 (J11).  반사실 대조가 같은 판 입력을
        다시 쓰도록 보관한다 (`sv_counterfactual`)."""
        self._plate_in = (Ab, gb, At, gt, cb, ct)
        out, st = self._assemble(Ab, gb, At, gt, cb, ct, counterfactual=False)
        self.junction_edge_sub = st['e']
        self.junction_edge_inst = np.asarray(self.reg['subedges']['inst'], np.int64)[st['e']]
        self.n_contracted = st['n_contracted']
        self.stats = st['stats']
        self.n_sv_edges = st['n_sv_edges']
        if 'reason' not in out:
            self.sys = st['sys']
            self._jidx = st['jidx']
            self._jsub = st['jsub']
        return out

    def _assemble(self, Ab, gb, At, gt, cb=None, ct=None, counterfactual=False):
        """계 조립 (부작용 없음) — counterfactual = 반사실 대조 판 (원장이 'sv_cut' 로 표지한 SV 다리 면 간선을 뺀다 · ★ 10-21 Q-D ·
        옛 = SV 면 부류 전부).  → (솔버 입력 | 사유, 상태)."""
        plan, reg = self.plan, self.reg
        sub = reg['subedges']
        #  분산 접합 간선 (간선마다 한 행 · 10-21 RCA-05) · 축약 — 주 계의 간선 목록 (self.E) 은 바꾸지 않는다 (지역 사본)
        mode = plan['mode']
        pu = self.pos_dof[np.maximum(sub['port_i'], 0)]; pv = self.pos_dof[np.maximum(sub['port_j'], 0)]
        e = np.flatnonzero(mode == MODE_EDGE)
        Elist = list(self.E)
        if len(e):
            gj = plan['g_code'][e]
            Elist.append((pu[e], pv[e], gj, np.full(len(e), _CAT['vv_junction']), np.full(len(e), np.nan),
                          np.full(len(e), np.nan), np.full(len(e), 3), np.full(len(e), 3), e.astype(np.int64),
                          np.zeros(len(e), bool)))
        rep = np.arange(self.n_total)
        #  ★ 10-21 (RCA-03) — 재방문 가지는 합치지 않는다 (옛: s < s_min 재방문 = 두 위치 한 노드 · 비연속 가닥 단락).
        #  접합 축약 (R_j′ = 0 · J6) — 단락 판정 (J11) 대상은 이 무리뿐
        con = np.flatnonzero(mode == MODE_CONTRACT)
        uf = _UF()
        for k in con:
            uf.union(int(rep[pu[k]]), int(rep[pv[k]]))
        members = {}
        for x in list(uf.p):
            members.setdefault(uf.find(x), []).append(x)
        if members:
            jr = np.arange(self.n_total)
            for r_, ms in members.items():
                jr[np.asarray(ms)] = r_
            rep = jr[rep]
        n_contracted = int(len(con))
        Ab2 = rep[self._plate_owner(Ab, False)] if Ab is not None else np.zeros(0, np.int64)
        At2 = rep[self._plate_owner(At, True)] if At is not None else np.zeros(0, np.int64)
        gb = np.asarray(gb if gb is not None else [], np.float64); gt = np.asarray(gt if gt is not None else [], np.float64)
        U = np.concatenate([x[0] for x in Elist]) if Elist else np.zeros(0, np.int64)
        V = np.concatenate([x[1] for x in Elist]) if Elist else np.zeros(0, np.int64)
        G = np.concatenate([x[2] for x in Elist]) if Elist else np.zeros(0)
        CAT = np.concatenate([x[3] for x in Elist]) if Elist else np.zeros(0, np.int64)
        SA = np.concatenate([x[4] for x in Elist]) if Elist else np.zeros(0)
        SB = np.concatenate([x[5] for x in Elist]) if Elist else np.zeros(0)
        IA = np.concatenate([x[6] for x in Elist]) if Elist else np.zeros(0, np.int64)
        IB = np.concatenate([x[7] for x in Elist]) if Elist else np.zeros(0, np.int64)
        TG = np.concatenate([x[8] for x in Elist]) if Elist else np.zeros(0, np.int64)
        CF = np.concatenate([x[9] for x in Elist]) if Elist else np.zeros(0, bool)
        U = rep[U]; V = rep[V]
        keep = (U != V) & (G > 0.0)
        n_sv_edges = int(np.sum(keep & (CAT == _CAT['sv_face'])))
        n_cf_edges = int(np.sum(keep & CF))
        if counterfactual:
            keep &= ~CF
        U, V, G, CAT, SA, SB, IA, IB, TG = (U[keep], V[keep], G[keep], CAT[keep], SA[keep], SB[keep], IA[keep], IB[keep],
                                            TG[keep])
        # 단락 (J11) — 축약 무리가 두 판에 다 닿음
        short = False
        big = [r_ for r_, ms in members.items() if len(ms) >= 2]
        if big:
            bs = set(Ab2.tolist()); ts = set(At2.tolist())
            short = any((r_ in bs and r_ in ts) for r_ in big)
        # 실제 그래프 연결 성분 (J7 · J12 · E3)
        from scipy.sparse.csgraph import connected_components
        n = self.n_total
        A = sparse.coo_matrix((np.ones(len(U), np.int8), (U, V)), shape=(n, n))
        ncomp, lab = connected_components(A, directed=False)
        is_rep = rep == np.arange(n)
        bot_c = np.zeros(ncomp, bool); top_c = np.zeros(ncomp, bool)
        bot_c[lab[Ab2]] = True; top_c[lab[At2]] = True
        kept_c = bot_c | top_c
        thr_c = bot_c & top_c
        kept = kept_c[lab] & is_rep
        n_kept = int(kept.sum())
        n_through = int((thr_c[lab] & is_rep).sum())
        n_path_only = int(len(np.asarray(reg.get('self_revisit_pairs', np.zeros((0, 2)))).reshape(-1, 2)))
        stats = {'n_extra_dofs': int(self.n_total - self.n_cells), 'n_contracted': n_contracted,
                 'n_floating_dropped': int((is_rep & ~kept).sum()), 'n_through_dof': n_through,
                 'n_plate_reachable_dof': n_kept, 'short': bool(short), 'tombstones': dict(self.tomb),
                 'n_unreg_fused': int(self.n_unreg_fused), 'n_junction_edges': int(np.sum(TG >= 0)),
                 'n_self_fused_faces': int(self.n_self_fused), 'n_self_revisits_path_only': n_path_only}
        st = {'e': e, 'n_contracted': n_contracted, 'stats': stats, 'n_sv_edges': n_sv_edges, 'n_cf_edges': n_cf_edges}
        if short:
            return {'reason': 'cjunc_electrode_short'}, st
        if n_kept == 0:
            return {'reason': 'all_floating_dropped'}, st
        if n_through == 0:
            return {'reason': 'no_through_component'}, st
        new = -np.ones(n, np.int64)
        new[kept] = np.arange(n_kept)
        ek = kept[U] & kept[V]
        U, V, G, CAT, SA, SB, IA, IB, TG = U[ek], V[ek], G[ek], CAT[ek], SA[ek], SB[ek], IA[ek], IB[ek], TG[ek]
        jidx = np.flatnonzero(TG >= 0)
        st['jidx'] = jidx
        st['jsub'] = TG[jidx]
        u, v = new[U], new[V]
        bk = kept[Ab2]; tk = kept[At2]
        Abn, gbn = new[Ab2[bk]], gb[bk]
        Atn, gtn = new[At2[tk]], gt[tk]
        cbn = tuple(np.asarray(x)[bk] for x in cb) if cb is not None else None
        ctn = tuple(np.asarray(x)[tk] for x in ct) if ct is not None else None
        diag = np.zeros(n_kept)
        np.add.at(diag, u, G); np.add.at(diag, v, G)
        np.add.at(diag, Abn, gbn); np.add.at(diag, Atn, gtn)
        b = np.zeros(n_kept)
        np.add.at(b, Abn, gbn)
        L = sparse.coo_matrix((np.concatenate([-G, -G, diag]), (np.concatenate([u, v, np.arange(n_kept)]),
                                                                  np.concatenate([v, u, np.arange(n_kept)]))),
                              shape=(n_kept, n_kept)).tocsr()
        st['sys'] = {'u': u, 'v': v, 'G': G, 'CAT': CAT, 'SA': SA, 'SB': SB, 'IA': IA, 'IB': IB, 'Ab': Abn, 'gb': gbn,
                     'At': Atn, 'gt': gtn, 'n': n_kept}
        return {'L': L, 'b': b, 'Ab': Abn, 'gb': gbn, 'At': Atn, 'gt': gtn, 'cb': cbn, 'ct': ctn, 'n_dof': n_kept}, st

    def record(self, phi):
        """원장을 읽는 소산 분담 · 접합 전류 (E1 · E2 · E4′) — 같은 단위 (코드) 로만 합친다.  접합 전류 = instance 마다 그 간선 합.
        ★ 10-21 (RCA-06) — 옛 `sv_dominant` (지배성 표지) 철회 → `sv_local_dissipation` (국소 소산 몫 진단 · 지배성 보증 아님)."""
        s = self.sys
        u, v, G, CAT = s['u'], s['v'], s['G'], s['CAT']
        dphi = phi[u] - phi[v]
        P = G * dphi * dphi
        Pb = s['gb'] * (phi[s['Ab']] - 1.0) ** 2
        Pt = s['gt'] * (phi[s['At']]) ** 2
        Ptot = float(P.sum() + Pb.sum() + Pt.sum())
        share = {k: 0.0 for k in _CAT}
        share['sdcp_cell'] = 0.0
        share['plate'] = float(Pb.sum() + Pt.sum())
        sv = CAT == _CAT['sv_face']
        share['sv_face'] = float(P[sv].sum())
        rest = ~sv
        ia5 = (s['IA'] == 5) & rest; ib5 = (s['IB'] == 5) & rest
        with np.errstate(invalid='ignore', divide='ignore'):
            fa = np.where(ia5, s['SB'] / (s['SA'] + s['SB']), 0.0)        # a 쪽 (SDCP) 반셀 몫 = σb/(σa+σb)
            fb = np.where(ib5, s['SA'] / (s['SA'] + s['SB']), 0.0)
        fa = np.nan_to_num(fa); fb = np.nan_to_num(fb)
        ps = P * (fa + fb)
        share['sdcp_cell'] = float(ps[rest].sum())
        for k, c in _CAT.items():
            if k == 'sv_face':
                continue
            m = CAT == c
            share[k] = float((P[m] * (1.0 - fa[m] - fb[m])).sum())
        tot = sum(share.values())
        frac = {k: (x / Ptot if Ptot > 0 else 0.0) for k, x in share.items()}
        nI = len(self.reg['instances']['fi'])
        jI = np.full(nI, np.nan)                             # instance 마다 접합 전류 (그 간선 합 · 간선 없는 instance = NaN)
        if len(self._jidx):
            qi = np.asarray(self.reg['subedges']['inst'], np.int64)[self._jsub]
            acc = np.zeros(nI)
            np.add.at(acc, qi, G[self._jidx] * dphi[self._jidx])
            has = np.zeros(nI, bool); has[qi] = True
            jI[has] = acc[has]
        I_bot = float(np.sum(s['gb'] * (1.0 - phi[s['Ab']])))
        sv_I = float(np.sum(np.abs(G[sv] * dphi[sv]))) / I_bot if I_bot > 0 else None
        sld = {'kind': 'diagnostic_local_dissipation', 'sv_share': float(frac['sv_face'] + frac['sdcp_cell']),
               'vv_junction_share': float(frac['vv_junction']),
               'meaning': 'SV 면 + SDCP 셀 소산 몫 = 국소 저항 민감도 — 경로 지배 · 우회 크기 보증 아님 (RCA-06 · 반사실 대조 = 선택 노브)'}
        return {'P_total_code': Ptot, 'P_sum_check_code': float(tot), 'dissipation_share': frac,
                'sv_local_dissipation': sld,
                'sv_face_abs_current_over_I': sv_I, 'junction_current_code': jI, 'I_bot_code': I_bot}

    def sv_counterfactual(self, solve, I_full, request, certify=None):
        """반사실 대조 (10-21 Codex RCA-06 · 1저자 Q4 (가) · 선택 노브) — 같은 침대 · 같은 R_j · 같은 판 입력에서 ★ 10-21 (사전 리뷰
        PRE-impl-04 · 1저자 Q-D) **SV 다리만** 끊은 계의 단자 전류 I_cut → `sv_counterfactual_ratio` = I_full / I_cut (≥ 1 · Rayleigh —
        끊기만 = 부분 그래프).  다리 = 서로 다른 섬유 · 접합으로 갈린 가지를 잇는 SDCP 성분의 SV 면 (원장 'sv_cut' · `_sv_split`) ·
        SDCP 를 지나는 섬유의 자기 연속은 남긴다 (옛: SV 면 전부 → SDCP 를 지나는 섬유 하나도 비 ∞ · 정보 없음).  문턱 (request) 이 있을
        때만 비교 표지 `SV_DEPENDENT` (비 ≥ 문턱) — 문턱 기본값 없음 (등록이 채운다).
        비 inf (`no_through_without_sv`) = **위상** 에서만 — 다리 SV 면을 끊은 조립 그래프에 관통 성분이 없을 때 (가지치기 사유).  관통 성분이
        있는데 푼 I_cut ≤ 0 · 비유한 = 수치 실패 (`nonpositive_cut_current` · 비 없음 — 양의 컨덕턴스 그래프의 관통 전류는 해석적으로 > 0).
        certify = 수렴 증서 (주 해와 같은 함수 · `step3_sigma` 가 CONV_CERT 일 때 넘긴다) — (L, b, φ, info, 잔차, Ab, gb, At, gt) → dict ·
        증서 실패 = 미수렴 (비 · 표지 없음 · 주 해 증서만 보고 분모를 믿지 않는다 · 10-21 사전 공격 리뷰)."""
        thr = request.get('threshold') if isinstance(request, dict) else None
        Ab, gb, At, gt, cb, ct = self._plate_in
        out, st = self._assemble(Ab, gb, At, gt, cb, ct, counterfactual=True)
        cen = self.reg.get('census') or {}
        rec = {'kind': CJUNC_SV_CF_KIND, 'rule': CJUNC_SV_CF_RULE, 'requested': True, 'threshold': thr,
               'n_sv_faces_cut': int(st['n_cf_edges']),
               'n_sdcp_components_touching': int(cen.get('n_sdcp_components_touching', 0)),
               'n_bridging_components': int(cen.get('n_bridging_components', 0)),
               'n_sv_faces_kept_self': int(cen.get('n_sv_faces_kept_self', 0)),
               'n_unsplit_bridging_components': int(cen.get('n_unsplit_bridging_components', 0)),
               'G_full_code': float(I_full), 'G_cut_code': None,
               'sv_counterfactual_ratio': None, 'flag': None, 'cg_info': None, 'resid': None, 'conv_cert': None}
        if not (math.isfinite(float(I_full)) and float(I_full) > 0.0):
            rec.update(status='nonpositive_full_current')       # 주 해 단자 전류 ≤ 0 · 비유한 — 비의 분자를 믿을 수 없다 (풀지 않는다)
        elif out.get('reason'):
            if out['reason'] in ('no_through_component', 'all_floating_dropped'):
                rec.update(status='no_through_without_sv', G_cut_code=0.0, sv_counterfactual_ratio=math.inf)
            else:
                rec.update(status=str(out['reason']))
        else:
            phi_c, info = solve(out['L'], out['b'])
            resid = float(np.linalg.norm(out['L'] @ phi_c - out['b']) / max(np.linalg.norm(out['b']), 1e-30))
            I_c = float(np.sum(out['gb'] * (1.0 - phi_c[out['Ab']])))
            rec.update(cg_info=int(info) if info else 0, resid=resid, G_cut_code=I_c)
            cert = None
            if certify is not None:
                cert = certify(out['L'], out['b'], phi_c, info, resid, out['Ab'], out['gb'], out['At'], out['gt'])
                rec['conv_cert'] = cert
            if bool(info) or not np.isfinite(resid) or resid > 1e-6 or (cert is not None and not cert.get('ok')):
                rec.update(status='unconverged')
            elif math.isfinite(I_c) and I_c > 0.0:
                rec.update(status='computed', sv_counterfactual_ratio=float(I_full / I_c))
            else:
                rec.update(status='nonpositive_cut_current')       # 관통 성분이 있는데 I_cut ≤ 0 — 수치 실패 (위상 서술 아님)
        r_ = rec['sv_counterfactual_ratio']
        if thr is not None and r_ is not None and r_ >= thr:
            rec['flag'] = 'SV_DEPENDENT'
        return rec


def early_record(plan, reason=None):
    r = dict(plan['record'])
    r.update(r['counts'])
    r['solved'] = False
    if reason:
        r['reason'] = reason
    return r


# ═════════════════════════ J2b census (VA · v0 = 간선 없음) ═════════════════════════
def va_census(add_pts, add_phase, add_fid, add_kind, am_c, am_r, *, r_f_um, tol_fs_um, gap_tol=2.0):
    """J2b fiber–sphere — 중심선 선분 ↔ 구 **중심** 최근접 ≤ r_f + R_AM + tol_fs 인 (fid, AM) 쌍 수 (v3 §5 · 판정문: 2.12 > 2.075)."""
    P, PH, F, K = _input_check(add_pts, add_phase, add_fid, add_kind)
    rej = []
    paths = [(f, r, kp) for f, r, kp in _paths_of(P, PH, F, K, 2, rej, 'VGCF') if kp]
    segs, _ = _segments_of(paths, P, gap_tol)
    am_c = np.asarray(am_c, np.float64).reshape(-1, 3); am_r = np.asarray(am_r, np.float64).ravel()
    n = 0
    for f in np.unique(segs['fid']):
        m = segs['fid'] == f
        for c, r in zip(am_c, am_r):
            d2, _, _ = pt_seg_d2(np.repeat(c[None], int(m.sum()), 0), segs['P0'][m], segs['P1'][m])
            if math.sqrt(float(d2.min())) <= float(r_f_um) + float(r) + float(tol_fs_um):
                n += 1
    return n
