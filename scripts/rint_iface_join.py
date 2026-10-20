#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""①′ 덤프 경로 **조인 관문** (T4-2 · N5′ · N1 · 2026-10-13) — G-geo (scaffold ↔ 원자 덤프 · 기하 대응) · G-frame (원자 덤프 ↔ 접촉 덤프 · 같은 프레임).

계약 = v2 §3-7 (조인 관문 1–4 · 거부) · §4 T4-2 · N1 · N5 + v3 §6-3 (G-geo · G-frame · 재사용 = 선언 · N5′) · §6-6 R3 · §8-2 D19
(docs/reviews/contact_resistance_pipeline_draft_v2_20261006.md · …_v3_20261006.md · …_v3_1_20261007.md).
지위 = **기구 · 시험 전용** — ①′ 정량 채택 · 생산 HOLD · PROTOCOL_FIELDS 밖 · payload CLI 미배선 · 웹앱 화면 없음.
이 관문은 **출처 증명**만 한다 — 덤프 경로의 부류 · 면적 (c_cpl[22]) 을 원장에 채택하지 않는다 (면적 원천 = scaffold lens 그대로 ·
`step3_sigma.am_iface_plan(join=…)` 이 결과를 `iface_join` · `iface_geom_reuse` 에 싣고, 실패면 정량 거부).

G-geo (기하 대응 · v3 §6-3 "v2 관문 1 · 3"):
  g1  scaffold 행 ↔ 원자 덤프 AM 원자 1:1 — 축마다 |Δ| ≤ h_s + h_d (+ 부동소수 여유) · h_s = scaffold 고정 소수 반폭 · h_d = 덤프 토큰 반폭
      (`lhs_contact_audit._half_ulp` · 파일 유효숫자 S = max(6, 실측)) · 주기 축은 최소 영상 · 형 (형 지도) · 반경도 같은 폭.
      후보 0 개 · 2 개 이상 · 짝 없는 덤프 AM · 두 번 짝지어진 덤프 AM = 거부.
  g2  AM–AM 접촉 행: δ_dump ↔ δ_scaffold (scaffold 좌표 · 최소 영상) 가 반올림 폭 안 — 폭 = √Σ(e_a + e_b)² + (h_s + h_r,a) + (h_s + h_r,b) + h_δ
      (e = h_s + h_d = scaffold 좌표의 참값 대비 상한).
  g3  AM–AM 접촉 행: A_dump (c_cpl[22]) ↔ lens_geometry(r1, r2, δ_dump) 포괄 구간 — `lhs_descriptor_harvest._contact_area_rows`
      (토큰 반올림 상자 · 생산자 산술 상한 · 같은 함수 · 규율 ①).
  g4  접촉 집합: scaffold 비주기 거리 (raster 가 보는 쌍) 에서 **확실한** 접촉 (δ_scaffold > 폭) 은 덤프에 행이 있어야 한다 · 덤프 AM–AM 중복 쌍 = 거부.
G-frame (같은 프레임 · v3 §6-3 "v2 관문 2 개정"):
  f1  프레임 각 1 개 (여러 프레임 = 거부 — 읽는 쪽마다 "마지막" 의 뜻이 달라질 수 있다 · DESC-06)
  f2  TIMESTEP 같음 — 다르면 거부 (N5′: 위치가 같아도) · **선언된 재사용**만 예외 (D19 · 두 step 기록 · 선언 ≠ 관측 = 거부 · 같은 step 에 선언 = 거부)
  f3  BOX BOUNDS (플래그 · 경계 토큰) 같음 · f4 원자 id 유일 · 머리 수 = 행 수 (두 덤프) · 접촉 id 전부 원자 덤프에 (고아 = 거부)
  f5  pos1/pos2 = 원자 위치 (주기 축 정수 영상 허용 · 토큰 반폭 안) — 행 단위 같은 프레임 증거 (RGL Q5: 해시는 프레임 증거가 아니다)
  f6  δ 자기 일관: δ_dump ↔ r1 + r2 − |최소 영상 (pos1 − pos2)| (토큰 반폭 전파) · δ_dump > 0 (접촉 행)
파생값 유한 (RIMPR-04 **부분** · Codex 10-20 판정문 §4 · 1저자 Q3 (가)) — 입력이 유한이어도 산술이 넘친다 (제곱합 · 곱 — `inf > inf` = 거짓이라
  허용폭 비교가 조용히 통과한다): f6 의 거리 · 허용폭 · 차 (고아 아닌 행) · G-geo 의 δ 반올림 폭 (delta_bound_um) · 내보내는 AM–AM δ · 면적 µm 값이
  비유한 = derived_nonfinite (REJECT).  안정한 거리 (hypot) 재작성 · 결과 유한성 전반 검토 = 정량 채택 전 (연기 조건 ④ · 원장 RIMPR-04 open).
scaffold 머리줄에 원 덤프 step 이 없으면 scaffold ↔ 덤프는 **G-geo 까지만** 주장한다 (v3 §6-3).  N1: dilate_z ≠ 1 = 거부 (기하가 DEM 이 아님).
입구 검사 (RIMP-02 · 03 · Codex 10-14 판정문 §3 · §4 · 1저자 Q2 (가) — 봉인 helper 는 그대로 · 이 소비자에서 엄격) — 관문 계산 **전**, 하나라도 걸리면
  REJECT (관문 계산 생략 · 사유만):
  e1  유한 — scaffold x y z r · 원자 x y z radius · 접촉 pos1 pos2 면적 δ 주기 플래그 · 상자 경계 (nan · inf · 못 읽는 토큰 = nonfinite_value).
      유한 = **실제로 쓰는 float64 값** 기준 (RIMPR-02 — scaffold 고정소수 토큰이 Decimal 로는 유한이어도 float64 로 ±inf 면 (1e309 · ±10^309) 비유한)
      + scaffold 의 µm 변환값 (×sim_to_um = 내보내는 c_um · r_um) 도 유한 (넘치면 nonfinite_value · `scaffold_um`)
  e2  양수 — scaffold r · 원자 radius > 0 (nonpositive_radius) · 상자 hi > lo (box_format)
  e3  정확 정수 — TIMESTEP · 머리 수 · 원자 id · type · 접촉 id1 · id2 · scaffold type 토큰 = 정수 문자열 · int64 범위만 (`2060000.9` · `201.0` · `1e+06` ·
      int64 를 넘는 토큰 = int_token · `int(float(…))` 로 줄이지 않는다 · OverflowError 로 끝나지 않는다).  TIMESTEP · NUMBER OF 절은 몸통 **전체**가
      정확히 한 토큰 (RIMPR-01 — `100 0.9` · `1 garbage` · 둘째 줄의 뒤 토큰을 버리지 않는다 = int_token) · 숫자 = **ASCII `[0-9]` 만** (RIMPR-03 —
      전각 `１` · 아라비아-인도 `١` 숫자 = int_token · 생산 덤프는 ASCII `%g`).
      scaffold 머리줄 (`#` 주석) 의 step 선언 (v5 · RIMPR-03 같은 부류) — v4 판 문법 (`(time)step` + `\\s` · `\\d` · re.I 유니코드) 으로 보이는 것은
      전부 선언이다 (조용히 버리지 않는다) · 값 = 선언 전체가 ASCII `(time)step[ \\t]*[=:]?[ \\t]*[0-9]+` (re.ASCII) 이고 수가 int64 일 때만 ·
      전각 · 유니코드 공백 · `ſ` (U+017F) · ASCII 뒤 섞인 비-ASCII 숫자 · int64 밖 긴 숫자열 = int_token (`scaffold_step` · `int()` 로 읽지 않는다)
  e4  지원 상자 — 직교 `ITEM: BOX BOUNDS f1 f2 f3` (플래그 [pfsm]² · p 는 pp 만) + 경계 줄 정확히 셋 · 줄마다 토큰 둘.  기울어진 머리 (xy xz yz) = box_tilted
      (지원 밖 · tilt 를 버리고 비교하지 않는다) · 그 밖 모양 (넷째 줄 포함) = box_format.  상자 동일 (f3) = 머리 · 경계 줄 **전 토큰** 비교
  e5  형식 = **6 유효숫자 `%g` 생산 포맷만** (LIGGGHTS dump 기본 · 토큰 = '%g' % 값) — 다른 정밀도 · 끝 0 · 혼합 포맷 = numeric_format.  면적 포괄
      helper 는 고정 6 자리 (`lhs_descriptor_harvest.AREA_CHECK_SIGFIG`) 라 지원 형식을 그 가정과 같게 묶는다 (기록 S 를 helper 에 넘기지 않는다 · 봉인 무변경).
      scaffold 실수 열 (x y z r · v5 · RIMPR-03 같은 부류) = **ASCII 고정소수 `[+-]?[0-9]+(\\.[0-9]+)?` 만** (생산 `mpm_input_from_case.write_csv` =
      `%.6f`) — 유한 토큰 중 전각 · 아라비아-인도 숫자 · 밑줄 · 지수 표기 · 유니코드 공백 덧붙임 = numeric_format (`scaffold_bad.scaffold_grammar` ·
      Decimal · float 은 그것들을 받는다) · scaffold 주석 아닌 줄의 글자 어휘 (TAB · CR · LF · 0x20–0x7E 밖 = `scaffold_bad.scaffold_lexical` · 중복
      방어 — 그 밖 글자는 어느 토큰 안에 남아 e1 · e3 · e5 에도 걸린다) · 빈 줄 · 주석 판정 · 토큰 앞뒤 떼기 = ASCII 공백 · 탭만 (옛 판 `strip()` 은 유니코드
      공백도 뗐다) · 주석 줄은 어휘 관문 밖 (case15 · kit 머리줄 U+2014 · 한국어)
  e6  전수 소비 (RIMPR-01 · Codex 10-15 판정문 §2 — 형식 검사를 적용할 원본을 **온전히** 읽는다 · 파서가 검사 전에 버리는 줄 · 열 · 토큰이 없다):
      행 절 (ITEM: ATOMS · ENTRIES) 의 비어 있지 않은 **모든** 행을 세고 열 수 ≠ 머리 열 수 = row_width (조용히 빼지 않는다) · 소비하는 필수 열 이름은
      정확히 한 번 (중복 = header_duplicate — 첫 열만 읽고 뒤 열을 검사 밖에 두지 않는다) · 마지막 프레임의 모든 줄은 아는 절 넷 (TIMESTEP ·
      NUMBER OF · BOX BOUNDS · 행) 중 하나에 한 번씩 — 모르는 ITEM 절 · 같은 절 두 번 · 첫 프레임 앞 비어 있지 않은 줄 · TIMESTEP · NUMBER OF 머리 줄의
      뒤 토큰 = frame_layout.  빈 줄 (공백뿐) 처리는 옛 판과 같다 — 행 절 안 · 절 끝의 빈 줄 = 내용 아님 · TIMESTEP · NUMBER OF · BOX BOUNDS
      절의 내용 앞 · 사이 빈 줄 = 모양 위반 (int_token · box_format).
      덤프 글자 어휘 (v5 · RIMPR-R01 같은 부류) — 파일 전체가 TAB · LF · CR · 출력 가능 ASCII (0x20–0x7E) 만: 그 밖 글자 (유니코드 공백 U+00A0 ·
      U+2003 · U+3000 · 제어 U+001F · 줄 경계 FF · VT · NEL · U+2028 …) = frame_layout (`lexical` — `str.split()` · `splitlines()` 가 그것들을 구분자 ·
      줄 끝으로 정상화해 값이 같은 채 통과하던 것 · 정상화하지 않고 거부).
      구역 머리 줄 (RIMPR-R01 · Codex 10-20 판정문 §3) — 구역 이름 = **정확한 단어 경계** (표지 `ITEM: TIMESTEP` · `ITEM: NUMBER OF …` ·
      `ITEM: BOX BOUNDS` · `ITEM: ATOMS` · `ITEM: ENTRIES` 바로 뒤 = 줄 끝 · 공백 (U+0020) · 탭 (U+0009) 만 — `isspace()` 아님 (v5 · U+00A0 · U+2003 ·
      U+3000 · U+001F 는 경계가 아니다) · `ITEM: ATOMSid …` · `ITEM: BOX BOUNDSff …` ·
      `ITEM: ATOMSITEM: ATOMS …` = frame_layout (header_boundary)) · 표지는 **앞에서 한 번만** 뗀다 (옛 판의 전역 `replace()` 아님) — 나머지 토큰은
      그대로 열 · 상자 검사로 (행 표지 후첨 = 머리 열 수 ≠ 행 폭 = row_width · 상자 표지 후첨 = 플래그 셋 아님 = box_format) · 정상 공백 · 탭 구분 ·
      끝 공백 · 쓰지 않는 진단 열은 그대로 받는다
  g3 보강 — AM–AM 행의 음수 면적 = area_negative · 포괄 미인증 (d 하한 ≤ 0 · 생산자 오차 상한 없음) = area_uncertified · PASS = 전 AM–AM 행 인증
      (n_area_tested = n_dem_am_am · `area_all_certified`).  AM–AM 밖 행 (AM–SE · SE–SE) 의 면적은 조인이 인증하지 않는다 (음수 수만 기록 —
      case15 AM_P–SE 2 행).

  python3 scripts/rint_iface_join.py --scaffold S.csv --atom A.liggghts[.gz] --contact C.liggghts[.gz] --type-map 1:AM_P,2:AM_S,3:SE [--json OUT]
"""
import argparse
import decimal
import gzip
import hashlib
import json
import os
import re
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
import step3_sigma as S3                                       # noqa: E402  지문 (fp_particles · fp_join) = 소비자와 같은 함수
import lhs_descriptor_harvest as H                             # noqa: E402  면적 포괄 구간 · 열 이름 (읽기만 · 봉인 파일 무변경)
from lhs_contact_audit import SIGFIG_FLOOR, _half_ulp, _sigfigs   # noqa: E402  반폭 규약 (규율 ①)

JOIN_KIND = 'am_iface_join'
JOIN_VERSION = 'g_geo_g_frame_v5'           # v5 (RIMPR-R01 · 03 같은 부류 · 10-20 내부 사전 리뷰) = 표지 경계 공백 · 탭만 · 덤프 글자 어휘 · scaffold ASCII 고정소수 + 주석 아닌 줄 어휘 · scaffold step 선언 ASCII · int64 / v4 (RIMPR-R01 · 03 · 04 부분) = 구역 이름 단어 경계 · 표지 한 번 · ASCII 정수 · 파생값 유한 / v3 (RIMPR-01 · 02) = e6 전수 소비 · e1 float64 + µm 변환 · e3 절 전체 · int64 / v2 (RIMP-02 · 03) = 입구 검사 e1–e5 + AM–AM 면적 전 행 인증 · v1 (10-13) = 그 전
SIM_TO_UM = 1000.0              # LIGGGHTS 상자 단위 → µm (덱 머리 "Scale: r*1000" · real_14 README)
AM_KINDS = ('AM_P', 'AM_S')
SCAFFOLD_TYPE = {1: 'AM_P', 2: 'AM_S'}                         # scaffold CSV 규약 (머리줄 "AM_P=1,AM_S=2")
POS1 = ('c_cpl[1]', 'c_cpl[2]', 'c_cpl[3]')                    # pair/gran/local pos (덱 `compute … pair/gran/local pos id force …`)
POS2 = ('c_cpl[4]', 'c_cpl[5]', 'c_cpl[6]')
_EPS = float(np.finfo(np.float64).eps)
_STEP_RE = re.compile(r'(?:time)?step[ \t]*[=:]?[ \t]*([0-9]+)', re.I | re.A)    # scaffold 머리줄 step 값 — ASCII 엄격 (v5 · re.A = 대소문자 접기도 ASCII 만)
_STEP_DECL_RE = re.compile(r'(?:time)?step\s*[=:]?\s*(\d+)', re.I)              # v4 판 문법 (\s · \d · re.I 유니코드 — 전각 · U+3000 · ſ 를 받는다) = 선언 찾기 전용 (v5)
_INT_RE = re.compile(r'[+-]?[0-9]+')                           # e3 정확 정수 토큰 (소수점 · 지수 · 밑줄 없음 · ASCII 숫자만 — `\d` 는 전각 · 아라비아-인도 숫자도 받는다 · RIMPR-03)
_LEX_BAD = re.compile(r'[^\t\n\r\x20-\x7e]')                   # 덤프 글자 · scaffold 주석 아닌 줄 어휘 — TAB · LF · CR · 출력 가능 ASCII (0x20–0x7E) 밖 (v5)
_FIX_RE = re.compile(r'[+-]?[0-9]+(?:\.[0-9]+)?')              # scaffold 실수 열 = ASCII 고정소수 (생산 `%.6f` · 지수 · 밑줄 · 유니코드 숫자 없음 · v5)
_I64_MIN, _I64_MAX = -(1 << 63), (1 << 63) - 1                  # e3 정수 토큰 범위 (id · type 은 int64 배열 · LIGGGHTS step = bigint) — RIMPR-02
_BOX_FLAG_RE = re.compile(r'[pfsm]{2}')                        # e4 LAMMPS 경계 플래그 (축마다 lo · hi)
_TILT_TOKENS = ('xy', 'xz', 'yz')
NUMERIC_FORMAT = 'g6'                                          # e5 — 지원하는 유일한 덤프 실수 형식 (6 유효숫자 `%g` · LIGGGHTS dump 기본)
SCAFFOLD_FORMAT = 'ascii_fixed_decimal'                        # e5 — scaffold 실수 열 형식 (`[+-]?[0-9]+(.[0-9]+)?` · 생산 `%.6f` · v5)
ENTRANCE_RULE = ('e1 유한 (실제로 쓰는 float64 값 · scaffold µm 변환값) · e2 양수 (반경 · 상자 길이) · e3 정확 정수 · ASCII [0-9] · int64 (step · 머리 수 · '
                 'id · type · TIMESTEP · NUMBER OF 절 몸통 전체 = 한 토큰 · scaffold 머리줄 step 선언 전체 ASCII) · e4 직교 상자만 (기울어진 머리 = 거부 · '
                 '경계 줄 정확히 셋) · e5 덤프 = 6 유효숫자 %g 생산 포맷만 (다른 정밀도 · 혼합 = 거부) · scaffold 실수 열 = ASCII 고정소수 + 주석 아닌 줄 어휘 · '
                 'e6 전수 소비 (행 열 수 · 필수 열 한 번 · 프레임 절 배치 · 구역 이름 단어 경계 = 줄 끝 · 공백 · 탭 · 표지 앞에서 한 번 · 덤프 글자 = TAB · LF · '
                 'CR · 0x20–0x7E — 버리는 줄 · 토큰 · 정상화 없음) — 하나라도 걸리면 관문 계산 없이 REJECT (RIMP-02 · 03 · RIMPR-01 · 02 · R01 · 03 · v5 같은 부류)')

WHY = {
    'dilate_z': 'N1 — dilate_z ≠ 1 이면 raster 기하가 DEM 이 아니다 (덤프 면적 · 접촉 집합을 쓸 수 없다)',
    'multi_frame': '덤프에 프레임이 둘 이상 — 읽는 쪽마다 "마지막" 의 뜻이 달라질 수 있다 (DESC-06) · 한 프레임 덤프만',
    'timestep_mismatch': 'N5′ — 원자 · 접촉 덤프 TIMESTEP 다름 (위치가 같아도 거부 · 선언된 재사용만 예외 · D19)',
    'geom_reuse_mismatch': '선언된 재사용의 두 step 이 관측 step 과 다르다',
    'geom_reuse_not_needed': '같은 step 인데 재사용 선언 — 선언은 다른 step 기하 재사용에만',
    'box_mismatch': 'BOX BOUNDS (플래그 · 경계값) 이 두 덤프에서 다르다',
    'count_mismatch': '머리의 원자 · 행 수 ≠ 실제 행 수',
    'atom_id_duplicate': '원자 덤프에 같은 id 두 행',
    'orphan_id': '접촉 행의 id 가 원자 덤프에 없다',
    'pos_mismatch': '접촉 pos1/pos2 ≠ 원자 위치 (주기 영상 · 토큰 반폭 밖) — 같은 프레임의 행 단위 증거가 깨졌다',
    'delta_pos_mismatch': 'δ_dump ≠ r1 + r2 − |pos1 − pos2| (토큰 반폭 전파 밖)',
    'delta_nonpositive': '접촉 행의 δ ≤ 0',
    'scaffold_type_unknown': 'scaffold 형이 1 (AM_P) · 2 (AM_S) 가 아니다',
    'scaffold_step_mismatch': 'scaffold 머리줄의 step ≠ 원자 덤프 step',
    'scaffold_row_unmatched': 'scaffold 행에 맞는 AM 원자가 없다 (반올림 폭 밖)',
    'scaffold_row_ambiguous': 'scaffold 행에 맞는 AM 원자가 둘 이상 (반올림 폭 안)',
    'dump_am_unmatched': '덤프 AM 원자가 어느 scaffold 행과도 짝이 아니다',
    'dump_am_multi': '덤프 AM 원자 하나에 scaffold 행 둘 이상',
    'type_mismatch': '짝지은 scaffold 행 ↔ 원자의 AM 종류가 다르다',
    'radius_mismatch': '짝지은 scaffold 행 ↔ 원자의 반경이 반올림 폭 밖',
    'delta_scaffold_mismatch': 'AM–AM 접촉의 δ_dump ≠ δ_scaffold (반올림 폭 밖)',
    'area_enclosure': 'AM–AM 접촉의 c_cpl[22] 이 lens_geometry(r1, r2, δ_dump) 포괄 구간 밖',
    'dem_contact_missing': 'scaffold 에서 확실한 AM–AM 접촉 (δ > 폭) 인데 접촉 덤프에 행이 없다',
    'dem_duplicate_pair': '접촉 덤프에 같은 AM–AM 쌍 두 행',
    'nonfinite_value': ('e1 — 비유한 (nan · inf) 또는 못 읽는 수 토큰 (NaN 비교는 어떤 허용폭 검사도 실패시키지 않는다 — 입구에서 거부 · RIMP-02) · '
                        '유한 = 실제로 쓰는 float64 값 (Decimal 유한 · float64 ±inf = 비유한) · scaffold µm 변환값 넘침 포함 (RIMPR-02)'),
    'nonpositive_radius': 'e2 — 반경 ≤ 0 (scaffold 또는 원자 덤프)',
    'int_token': ('e3 — 정수여야 할 토큰 (TIMESTEP · 머리 수 · id · type) 이 정확한 정수 문자열 · int64 범위가 아니다 (int(float(…)) 로 줄이지 않는다 · '
                  'RIMP-02) · TIMESTEP · NUMBER OF 절 몸통 전체가 정확히 한 토큰이 아니다 (뒤 토큰 · 둘째 줄을 버리지 않는다 · RIMPR-01) · '
                  'int64 를 넘는 토큰 (OverflowError 대신 · RIMPR-02) · ASCII 숫자 [0-9] 가 아닌 숫자 (전각 · 아라비아-인도 · RIMPR-03) · '
                  'scaffold 머리줄 step 선언이 ASCII `(time)step[ \\t]*[=:]?[ \\t]*[0-9]+` · int64 가 아니다 (전각 · 유니코드 공백 · ſ · 섞인 숫자 · 긴 숫자열 — '
                  'int() 로 읽지 않는다 · v5)'),
    'box_tilted': 'e4 — 기울어진 상자 머리 (xy xz yz) · 직교 상자만 지원 (tilt 를 버리고 비교하지 않는다 · RIMP-02)',
    'box_format': 'e4 — 상자 머리 · 경계 줄 모양이 직교 LAMMPS 꼴이 아니다 (플래그 셋 · 경계 줄 정확히 셋 · 줄마다 토큰 둘 · hi > lo)',
    'row_width': ('e6 — 행 절 (ITEM: ATOMS · ENTRIES) 의 비어 있지 않은 행의 열 수 ≠ 머리 열 수 — 조용히 빼면 머리 수 · 형식 · 유한 검사를 받지 않은 채 '
                  '남은 행만 인증된다 (RIMPR-01)'),
    'header_duplicate': ('e6 — 소비하는 필수 열 이름이 머리에 두 번 이상 — 첫 열만 읽으면 뒤 열은 검사에서 사라진다 (필수 열은 정확히 한 번 · '
                         'RIMPR-01)'),
    'frame_layout': ('e6 — 마지막 프레임의 줄이 아는 절 넷 (TIMESTEP · NUMBER OF · BOX BOUNDS · 행) 에 한 번씩 배정되지 않는다 — 모르는 ITEM 절 · '
                     '같은 절 두 번 · 첫 프레임 앞 비어 있지 않은 줄 · TIMESTEP · NUMBER OF 머리 줄의 뒤 토큰 (버리지 않고 거부 · RIMPR-01) · '
                     '구역 이름 뒤 단어 경계 없음 (`ITEM: ATOMSid …` · `ITEM: BOX BOUNDSITEM: …` — 정상화하지 않고 거부 · RIMPR-R01) · 경계 = 줄 끝 · '
                     '공백 · 탭만 (U+00A0 · U+2003 · U+3000 · U+001F 는 경계 아님 · v5) · 덤프 글자 어휘 — TAB · LF · CR · 출력 가능 ASCII (0x20–0x7E) 밖 '
                     '글자 (유니코드 공백 · 제어 문자 · 비-ASCII 줄 경계 — split() · splitlines() 가 정상화하던 것 · lexical · v5)'),
    'numeric_format': ('e5 — 실수 토큰이 6 유효숫자 %g 생산 포맷이 아니다 (다른 정밀도 · 끝 0 · 혼합 · 면적 포괄 helper 의 고정 6 자리 가정 밖 · RIMP-03) · '
                       'scaffold 실수 열 (x y z r) 이 ASCII 고정소수 `[+-]?[0-9]+(.[0-9]+)?` 가 아니다 (전각 · 아라비아-인도 숫자 · 밑줄 · 지수 · 유니코드 공백 — '
                       'Decimal · float 은 받는다 · scaffold_grammar · v5) · scaffold 주석 아닌 줄에 TAB · CR · LF · 0x20–0x7E 밖 글자 (scaffold_lexical · v5)'),
    'area_negative': 'g3 — AM–AM 접촉의 c_cpl[22] 가 음수 (진단 helper 는 음수 행을 포괄 비교에서 뺀다 — 뺀 것을 인증으로 읽지 않는다 · RIMP-02)',
    'area_uncertified': 'g3 — AM–AM 접촉의 면적 포괄을 인증할 수 없다 (토큰 상자 위 거리 하한 ≤ 0 · 생산자 오차 상한 없음 — "포괄 밖 0" ≠ "전 행 인증" · RIMP-02)',
    'derived_nonfinite': ('파생값 비유한 — 입력이 유한이어도 산술 (제곱합 · 곱) 이 넘친다: G-frame f6 거리 · 허용폭 · 차 (고아 아닌 행) · G-geo δ 반올림 폭 '
                          '(delta_bound_um) · 내보내는 AM–AM δ · 면적 µm 값 (`inf > inf` = 거짓이라 허용폭 비교가 조용히 통과한다 · inf 를 인증 값으로 발행하지 '
                          '않는다 · RIMPR-04 부분 — 안정한 hypot · 결과 유한성 전반 = 정량 채택 전)'),
}


# ═════════════════════════ 읽기 ═════════════════════════
def _open_text(path):
    return gzip.open(path, 'rt', encoding='utf-8') if str(path).endswith('.gz') else open(path, 'r', encoding='utf-8')


def _file_digest(path):
    """sha256 — 저장된 파일 바이트 (`sha256_file`) · 풀린 내용 바이트 (`sha256_content` · gz 아니면 같다) · 경로 대신 이름만 (기계 무관)."""
    with open(path, 'rb') as fh:
        raw = fh.read()
    content = gzip.decompress(raw) if str(path).endswith('.gz') else raw
    return {'name': os.path.basename(str(path)), 'sha256_file': hashlib.sha256(raw).hexdigest(),
            'sha256_content': hashlib.sha256(content).hexdigest()}


def _safe_float(t):
    try:
        return float(t)
    except (TypeError, ValueError):
        return float('nan')                                    # 못 읽는 토큰 = 비유한 (e1 이 거부한다)


def _float_col(tokens):
    """토큰 문자열 배열 → float64 (numpy 변환 · 실패하면 토큰마다 — 못 읽는 것 = NaN)."""
    tokens = np.asarray(tokens, dtype=str)
    try:
        return tokens.astype(np.float64)
    except ValueError:
        return np.array([_safe_float(t) for t in tokens.tolist()], np.float64)


def _int_token(tok):
    """e3 — 정확한 정수 문자열이고 int64 범위 안이면 (int, True) · 아니면 (None, False).  `int(float(…))` 로 줄이지 않는다 (RIMP-02 · Codex
    `2060000.9`).  int64 밖 (`9223372036854775808` …) = 정수 아님 — int64 배열에 담다 OverflowError 로 끝나지 않고 입구 int_token 거부 (RIMPR-02) ·
    자릿수가 int64 보다 긴 토큰은 int() 를 부르기 전에 거른다 (아주 긴 숫자열의 int() 변환 한도 ValueError 도 입구 거부로)."""
    if isinstance(tok, str) and _INT_RE.fullmatch(tok):
        digits = tok.lstrip('+-').lstrip('0') or '0'          # 앞 0 을 뗀 숫자열 (int() 한도는 앞 0 도 센다)
        if len(digits) <= 19:                                  # int64 최댓값 9223372036854775807 = 19 자리
            v = -int(digits) if tok.startswith('-') else int(digits)
            if _I64_MIN <= v <= _I64_MAX:
                return v, True
    return None, False


def _int_col(tokens):
    """정수 토큰 열 → (int64 값 · 정수가 아닌 토큰 수 · 보기 셋) — 정수가 아닌 자리는 0 (입구 검사가 거부하므로 값으로 쓰이지 않는다)."""
    out = np.zeros(len(tokens), np.int64)
    bad = []
    for k, t in enumerate(tokens):
        v, ok = _int_token(t)
        if ok:
            out[k] = v
        else:
            bad.append(t)
    return out, len(bad), bad[:3]


def _numeric_cols(columns):
    """실수 토큰 열 여럿 → (열마다 값 · 파일 유효숫자 S · 열마다 반폭 · 진단) — 고유 토큰마다 한 번.

    S = max(6, 유한 고유 토큰의 `_sigfigs` 최대) · 반폭 = `_half_ulp(tok, S)` (옛 `_tokens_sigfig_half` 와 같은 값 — 유한 토큰) · 비유한 토큰 반폭 = NaN.
    진단: n_nonfinite (비유한 · 못 읽음 · 출현 수) · n_not_g6 (유한인데 토큰 ≠ '%g' % 값 — e5 · 출현 수) · 보기."""
    info = {'n_nonfinite': 0, 'n_not_g6': 0, 'examples_nonfinite': [], 'examples_not_g6': []}
    if not columns or not sum(len(c) for c in columns):
        return [np.zeros(len(c)) for c in columns], SIGFIG_FLOOR, [np.zeros(len(c)) for c in columns], info
    allt = np.concatenate([np.asarray(c, dtype=str) for c in columns])
    u, inv = np.unique(allt, return_inverse=True)
    ul = u.tolist()
    vu = np.array([_safe_float(t) for t in ul], np.float64)
    fin = np.isfinite(vu)
    g6 = np.array([bool(fin[k]) and ('%g' % vu[k]) == t for k, t in enumerate(ul)], bool)
    S = max(SIGFIG_FLOOR, max((_sigfigs(t) for k, t in enumerate(ul) if fin[k]), default=0))
    hu = np.array([_half_ulp(t, S) if fin[k] else np.nan for k, t in enumerate(ul)], np.float64)
    nf_occ, ng_occ = (~fin)[inv], (fin & ~g6)[inv]
    info.update(n_nonfinite=int(nf_occ.sum()), n_not_g6=int(ng_occ.sum()),
                examples_nonfinite=[ul[k] for k in np.flatnonzero(~fin)[:3]],
                examples_not_g6=[ul[k] for k in np.flatnonzero(fin & ~g6)[:3]])
    vals, halves, k0 = [], [], 0
    for c in columns:
        n_ = len(c)
        vals.append(_float_col(c))
        halves.append(hu[inv[k0:k0 + n_]])
        k0 += n_
    return vals, int(S), halves, info


def half_ulp_tokens(tokens, sigfig):
    """토큰 문자열 배열 → 반폭 (`lhs_contact_audit._half_ulp(tok, S)` · 같은 함수)."""
    tokens = np.asarray(tokens)
    u, inv = np.unique(tokens, return_inverse=True)
    return np.array([_half_ulp(str(t), int(sigfig)) for t in u], np.float64)[inv].reshape(tokens.shape)


def _box_shape(hdr_tok, lines3):
    """e4 — 상자 머리 토큰 · 경계 줄 (BOX BOUNDS 절 몸통의 비어 있지 않은 **모든** 줄) → (모양 'orthogonal' | 'tilted' | 'malformed', 사유 목록)."""
    if any(t in _TILT_TOKENS for t in hdr_tok):
        return 'tilted', ['xy xz yz 머리 (삼사정계)']
    why = []
    if len(hdr_tok) != 3:
        why.append(f'플래그 수 {len(hdr_tok)} ≠ 3')
    for f in hdr_tok:
        if not _BOX_FLAG_RE.fullmatch(f) or (('p' in f) and f != 'pp'):
            why.append(f'플래그 {f!r}')
    if len(lines3) != 3:
        why.append(f'경계 줄 수 {len(lines3)} ≠ 3 (RIMPR-01 — 절 몸통 전수)')
    for k, b in enumerate(lines3):
        if len(b) != 2:
            why.append(f'경계 줄 {k} 토큰 {len(b)} ≠ 2')
    return ('orthogonal' if not why else 'malformed'), why


def _section_content(body):
    """절 몸통 → 내용 줄 — **끝**의 빈 줄 (공백뿐) 만 뗀다.  내용 앞 · 사이의 빈 줄은 남겨 모양 검사가 본다 (옛 판의 고정 위치 읽기와 같은 빈 줄
    결과: 머리 바로 다음 빈 줄 = 위반 · 내용 뒤 빈 줄 = 내용 아님 — 빈 줄 처리를 옛 판보다 느슨하게 하지 않는다)."""
    k = len(body)
    while k and not body[k - 1].strip():
        k -= 1
    return body[:k]


def _scalar_token(body):
    """TIMESTEP · NUMBER OF 절 몸통 → 토큰 문자열 — 내용 줄을 **전부** 담는다 (줄 앞뒤 공백만 뗀다 · 내용 앞 · 사이 빈 줄은 빈 문자열로 남는다 ·
    RIMPR-01: 뒤 토큰 · 둘째 줄을 버리지 않는다).  정확히 한 줄 · 한 토큰일 때만 정수 문법에 맞는다 (`100 0.9` · `100\\n0.9` · `\\n100` · 빈 몸통
    = e3 int_token)."""
    return '\n'.join(s.strip() for s in _section_content(body))


def _item_section(ln, items):
    """`ITEM:` 머리 줄 → (구역 · 표지 뒤 토큰 · 단어 경계 위반) — RIMPR-R01 (Codex 10-20 판정문 §3 최소 해결).
    items = ((구역, 표지), …) — 표지 (`ITEM: TIMESTEP` · `ITEM: NUMBER OF …` · `ITEM: BOX BOUNDS` · `ITEM: ATOMS` · `ITEM: ENTRIES`) 로 시작하면 그 구역.
    구역 이름 = **정확한 단어 경계**: 표지 바로 뒤가 줄 끝 · 공백 (U+0020) · 탭 (U+0009) 이 아니면 (`ITEM: ATOMSid …` · `ITEM: BOX BOUNDSff …` ·
    `ITEM: ATOMSITEM: ATOMS …` · v5: `isspace()` 가 참인 U+00A0 · U+2003 · U+3000 · U+001F 도 경계가 아니다 — RIMPR-R01 같은 부류)
    경계 위반 = 입구 frame_layout (header_boundary · 정상화하지 않고 거부 — 그 줄의 절은 그대로 읽어 나머지 검사도 돈다).  표지는 **앞에서 한 번만**
    뗀다 (옛 판의 전역 `replace()` 아님): 나머지 토큰 (반복 · 후첨 표지 포함) = `split()` 그대로 열 · 상자 검사로 (공백 · 탭 구분 · 쓰지 않는 진단 열은
    옛 판과 같게 받는다 · 비-ASCII 구분자는 덤프 어휘 관문 `_LEX_BAD` 가 따로 거부).  어느 표지로도 시작하지 않으면 (None, None, False) = 모르는 절."""
    for kind, mk in items:
        if ln.startswith(mk):
            rest = ln[len(mk):]
            return kind, rest.split(), bool(rest) and rest[0] not in ' \t'
    return None, None, False


def _scan_frame(path, count_item, rows_item):
    """마지막 프레임의 (step · 머리 수 · 상자 플래그 · 상자 토큰 · 열 머리 · 행) + 프레임 수 + 입구 검사 재료 (step · 머리 수 토큰 정수 여부 ·
    상자 머리 · 경계 줄 전 토큰 · 상자 모양 · e6 전수 소비 재료).  정수가 아닌 step · 머리 수 = None (줄이지 않는다).

    RIMPR-01 (Codex 10-15 판정문 §2) — 마지막 프레임의 **모든 줄**을 절 (`ITEM:` 머리 + 다음 `ITEM:` 전까지의 몸통) 에 배정해 읽는다 (검사 전에 버리는
    줄 · 토큰이 없다): TIMESTEP · NUMBER OF 절 = 몸통 전체가 한 토큰 (`_scalar_token`) · BOX BOUNDS 절 = 몸통의 내용 줄 전부 (`_box_shape` 가 정확히
    셋 · 줄마다 토큰 둘을 요구) · 행 절 = 비어 있지 않은 모든 행을 세고 열 수 ≠ 머리 열 수 인 행은 따로 센다 (값으로는 쓰지 않는다 · 입구 row_width) ·
    모르는 ITEM 절 · 같은 절 두 번 · 첫 프레임 앞 비어 있지 않은 줄 · TIMESTEP · NUMBER OF 머리 줄의 뒤 토큰 = 입구 frame_layout.
    빈 줄: 행 절 안 · 절 끝 = 내용 아님 (옛 판과 같음) · TIMESTEP · NUMBER OF · BOX BOUNDS 절의 내용 앞 · 사이 = 모양 위반 (옛 판과 같음 · `_section_content`).
    RIMPR-R01 (Codex 10-20 판정문 §3) — 구역 분류 = `_item_section` (구역 이름 정확한 단어 경계 · 표지 앞에서 한 번만 떼기): 경계 위반 머리 줄 = 입구
    frame_layout (header_boundary) · 상자 머리 · 열 머리 = 표지 뒤 토큰 그대로 (반복 · 후첨 표지가 남아 box_format · row_width 가 본다).
    v5 (RIMPR-R01 같은 부류) — 덤프 글자 어휘: 읽은 글 전체 (줄로 쪼개기 전 · 모든 프레임) 에서 TAB · LF · CR · 출력 가능 ASCII (0x20–0x7E) 밖 글자를
    센다 (`n_lexical` · 보기 = 줄 번호 + 부호점) → 입구 frame_layout (lexical).  `split()` · `splitlines()` 가 유니코드 공백 · 제어 문자 · FF · VT · NEL ·
    U+2028 을 구분자 · 줄 끝으로 정상화해 값이 같은 채 지나가던 것을 그 정상화 **전에** 잡는다 (쪼개기 · 읽기 규칙은 옛 판과 같다)."""
    with _open_text(path) as fh:
        txt = fh.read()
    n_lex, ex_lex = 0, []
    for m in _LEX_BAD.finditer(txt):
        n_lex += 1
        if len(ex_lex) < 3:
            ex_lex.append(f'줄 {txt.count(chr(10), 0, m.start()) + 1} U+{ord(m.group()):04X}')
    lines = txt.splitlines()
    starts = [i for i, ln in enumerate(lines) if ln.startswith('ITEM: TIMESTEP')]
    if not starts:
        raise ValueError(f'{path}: `ITEM: TIMESTEP` 이 없다 — LIGGGHTS 덤프가 아니다')
    heads = [k for k in range(starts[-1], len(lines)) if lines[k].startswith('ITEM:')]
    items = (('step', 'ITEM: TIMESTEP'), ('count', count_item), ('box', 'ITEM: BOX BOUNDS'), ('rows', rows_item))
    secs, unknown, dup_sec, head_extra, head_edge = {}, [], [], [], []
    for a, b in zip(heads, heads[1:] + [len(lines)]):
        ln = lines[a]
        kind, toks, edge_bad = _item_section(ln, items)
        if kind is None:
            unknown.append(ln.strip())
        elif kind in secs:
            dup_sec.append(kind)
        else:
            secs[kind] = (toks, lines[a + 1:b])
            if edge_bad:                                       # 구역 이름 뒤 단어 경계 없음 (`ITEM: ATOMSid …`) — 정상화하지 않는다 (RIMPR-R01)
                head_edge.append(ln.strip())
            if kind in ('step', 'count') and toks:            # 머리 줄의 뒤 토큰 (`ITEM: TIMESTEP 0.9`) 도 버리지 않는다
                head_extra.append(ln.strip())
    n_pre = sum(1 for ln in lines[:starts[0]] if ln.strip())
    step_tok = _scalar_token(secs['step'][1])
    step, step_ok = _int_token(step_tok)
    n_decl, n_decl_ok, n_decl_tok = None, True, None
    if 'count' in secs:
        n_decl_tok = _scalar_token(secs['count'][1])
        n_decl, n_decl_ok = _int_token(n_decl_tok)
    if 'rows' not in secs or 'box' not in secs:
        raise ValueError(f'{path}: `{rows_item}` 또는 `ITEM: BOX BOUNDS` 가 마지막 프레임에 없다')
    bhdr = list(secs['box'][0])                                # 표지 뒤 토큰 (앞에서 한 번만 뗐다 · RIMPR-R01)
    flags = tuple(bhdr[-3:]) if len(bhdr) >= 3 else None
    blines = [s.split() for s in _section_content(secs['box'][1])]     # 내용 앞 · 사이 빈 줄 = 토큰 0 줄 (box_format · 옛 판과 같음)
    btok = [tuple(b[:2]) for b in (blines + [[], [], []])[:3]]
    hdr = list(secs['rows'][0])                                # 열 머리 = 표지 뒤 토큰 (후첨 표지가 남으면 열 수 ≠ 행 폭 = row_width · RIMPR-R01)
    rows, wbad, n_phys = [], [], 0
    for s in secs['rows'][1]:
        v = s.split()
        if not v:
            continue
        if len(v) == len(hdr):
            rows.append(v)
        else:
            wbad.append((n_phys, len(v)))                     # 행 절 안 몇 째 (0 부터 · 빈 줄 제외) · 열 수
        n_phys += 1
    bvals, _S, _h, binfo = _numeric_cols([np.array([b[0] if len(b) > 0 else '' for b in btok], dtype=str),
                                          np.array([b[1] if len(b) > 1 else '' for b in btok], dtype=str)])
    shape, shape_why = _box_shape(bhdr, blines)
    lo, hi = bvals[0], bvals[1]
    if shape == 'orthogonal' and np.isfinite(lo).all() and np.isfinite(hi).all() and not (hi > lo).all():
        shape, shape_why = 'malformed', [f'hi ≤ lo (축 {np.flatnonzero(~(hi > lo)).tolist()})']
    return {'step': step, 'n_frames': len(starts), 'n_declared': n_decl, 'box_flags': flags, 'box_tokens': btok,
            'box_lo': lo, 'box_hi': hi, 'header': hdr, 'rows': rows,
            'entrance': {'step_token': step_tok, 'step_int_ok': step_ok, 'n_declared_token': n_decl_tok, 'n_declared_int_ok': n_decl_ok,
                         'box_header': list(bhdr), 'box_lines': [list(b) for b in blines], 'box_shape': shape, 'box_shape_why': shape_why,
                         'box_n_nonfinite': binfo['n_nonfinite'], 'box_n_not_g6': binfo['n_not_g6'],
                         'box_examples_not_g6': binfo['examples_not_g6'],
                         #  e6 전수 소비 재료 (RIMPR-01)
                         'n_rows_physical': int(n_phys), 'n_rows_width_bad': len(wbad),
                         'examples_width_bad': [f'행 절 {k} 째 열 {w} ≠ 머리 {len(hdr)}' for k, w in wbad[:3]],
                         'n_preamble_lines': int(n_pre), 'n_unknown_sections': len(unknown), 'unknown_sections': unknown[:3],
                         'duplicate_sections': dup_sec, 'scalar_header_extra': head_extra,
                         'header_boundary': head_edge,                  # 구역 이름 뒤 단어 경계 없음 (RIMPR-R01 · v5 = 공백 · 탭만)
                         'n_lexical': int(n_lex), 'examples_lexical': ex_lex}}   # 덤프 글자 어휘 (v5 · TAB · LF · CR · 0x20–0x7E 밖)


def read_atom_dump_frame(path):
    """원자 덤프 마지막 프레임 — id · type · x (N, 3) · r · 토큰 반폭 (hx · hr) · 파일 유효숫자 · step · 프레임 수 · 상자 · 입구 검사 재료
    (`entrance` — 비유한 · %g 아님 · 정수 아님 · 반경 ≤ 0 · 상자 모양)."""
    F = _scan_frame(path, 'ITEM: NUMBER OF ATOMS', 'ITEM: ATOMS')
    hdr, rows = F.pop('header'), F.pop('rows')
    need = ('id', 'type', 'x', 'y', 'z', 'radius')
    miss = [c for c in need if c not in hdr]
    if miss:
        raise ValueError(f'{path}: 원자 덤프에 열 {miss} 이 없다 (있는 열: {hdr})')
    F['entrance']['header_duplicate'] = [c for c in need if hdr.count(c) > 1]   # e6 — 필수 열은 정확히 한 번 (RIMPR-01 · 입구 거부)
    ix = {c: hdr.index(c) for c in need}
    cols = ('x', 'y', 'z', 'radius')
    tok = {c: np.array([r[ix[c]] for r in rows], dtype=str) for c in cols}
    vals, S, hs, info = _numeric_cols([tok[c] for c in cols])
    n = len(rows)
    ids, nb_id, ex_id = _int_col([r[ix['id']] for r in rows])
    types, nb_ty, ex_ty = _int_col([r[ix['type']] for r in rows])
    rr = vals[3]
    F.update(ids=ids, types=types,
             x=(np.stack(vals[:3], axis=1) if n else np.zeros((0, 3))), r=rr,
             hx=(np.stack(hs[:3], axis=1) if n else np.zeros((0, 3))), hr=hs[3], sigfig=int(S), n_rows=n)
    F['entrance'].update(n_nonfinite=info['n_nonfinite'], n_not_g6=info['n_not_g6'], examples_nonfinite=info['examples_nonfinite'],
                         examples_not_g6=info['examples_not_g6'], n_int_bad={'id': nb_id, 'type': nb_ty},
                         examples_int_bad=ex_id + ex_ty, n_nonpositive_radius=int((np.isfinite(rr) & ~(rr > 0.0)).sum()))
    return F


def read_contact_dump_frame(path):
    """접촉 덤프 (pair/gran/local) 마지막 프레임 — id1 · id2 · pos1 · pos2 · 면적 c_cpl[22] · δ c_cpl[23] · 주기 플래그 c_cpl[9] · 토큰 반폭 ·
    입구 검사 재료 (`entrance`)."""
    F = _scan_frame(path, 'ITEM: NUMBER OF ENTRIES', 'ITEM: ENTRIES')
    hdr, rows = F.pop('header'), F.pop('rows')
    need = POS1 + POS2 + (H.COL_D1, H.COL_D2, H.COL_PERIODIC, H.COL_AREA, H.COL_DELTA)
    miss = [c for c in need if c not in hdr]
    if miss:
        raise ValueError(f'{path}: 접촉 덤프에 열 {miss} 이 없다 — pos · id · 면적 · δ 규약을 모르는 채로 조인하지 않는다')
    F['entrance']['header_duplicate'] = [c for c in need if hdr.count(c) > 1]   # e6 — 필수 열은 정확히 한 번 (RIMPR-01 · 입구 거부)
    ix = {c: hdr.index(c) for c in need}
    cols = POS1 + POS2 + (H.COL_AREA, H.COL_DELTA, H.COL_PERIODIC)
    tok = {c: np.array([r[ix[c]] for r in rows], dtype=str) for c in cols}
    vals, S, hs, info = _numeric_cols([tok[c] for c in cols])
    n = len(rows)
    id1, nb1, ex1 = _int_col([r[ix[H.COL_D1]] for r in rows])
    id2, nb2, ex2 = _int_col([r[ix[H.COL_D2]] for r in rows])

    def _st(arrs):
        return np.stack(arrs, axis=1) if n else np.zeros((0, 3))
    F.update(id1=id1, id2=id2, pflag=vals[8],
             pos1=_st(vals[0:3]), pos2=_st(vals[3:6]), h_pos1=_st(hs[0:3]), h_pos2=_st(hs[3:6]),
             area=vals[6], delta=vals[7], h_area=hs[6], h_delta=hs[7], sigfig=int(S), n_rows=n)
    F['entrance'].update(n_nonfinite=info['n_nonfinite'], n_not_g6=info['n_not_g6'], examples_nonfinite=info['examples_nonfinite'],
                         examples_not_g6=info['examples_not_g6'], n_int_bad={'id1': nb1, 'id2': nb2}, examples_int_bad=ex1 + ex2)
    return F


def read_scaffold_csv(path):
    """AM scaffold CSV (`type,x,y,z,r` · 상자 단위 · 고정 소수) — 반폭 h_s = 0.5·10^(가장 고운 소수 지수) (고정 소수 형식이라 유효숫자가 아니라
    자릿수로 잰다 · 파일 전체의 가장 고운 자리 = 좁은 쪽 = 덜 통과시키는 쪽).  자릿수는 **유한** 토큰에서만 잰다 (nan · inf · 못 읽는 토큰 =
    `n_nonfinite` · type 정수 아님 = `n_int_bad` · r ≤ 0 = `n_nonpositive_r` — 입구 검사 e1–e3 이 거부한다 · 예외로 멈추지 않는다).
    유한 = Decimal 유한 **이고** 실제로 쓰는 float64 값도 유한 (RIMPR-02 — `1e309` · 고정소수 ±10^309 는 Decimal 로는 유한 · float64 로는 ±inf).
    µm 변환 (×sim_to_um) 뒤 유한은 단위를 아는 입구 검사 (`_entrance` · `scaffold_um`) 가 본다.
    v5 (RIMPR-03 같은 부류 · 입구 e3 · e5 재료 — 거부는 `_entrance`):
      빈 줄 · 주석 판정 · 토큰 앞뒤 떼기 = ASCII 공백 · 탭만 (옛 판 `strip()` 은 유니코드 공백도 뗐다 — 값이 같은 채 통과) · 주석 줄 (`#`) 은 어휘 관문 밖
      (case15 · kit 머리줄 U+2014 · 한국어) · 주석 아닌 줄의 TAB · CR · LF · 0x20–0x7E 밖 글자 = `n_lexical` · 유한 실수 토큰 중 ASCII 고정소수
      (`_FIX_RE`) 가 아닌 것 = `n_format_bad` (비유한 · 못 읽음 = 옛 판처럼 `n_nonfinite` 만) · 머리줄 step 선언 = `_STEP_DECL_RE` (v4 판 문법) 로 찾고
      선언 전체가 `_STEP_RE` (ASCII) 이고 수가 int64 일 때만 값 (`steps`) · 아니면 `n_step_bad` (`int()` 로 읽지 않는다 — 긴 숫자열도 예외 없이)."""
    header, rows, n_lex, ex_lex = [], [], 0, []
    with _open_text(path) as fh:
        for k, ln in enumerate(fh, 1):
            body = ln.rstrip('\r\n')
            s = body.strip(' \t')
            if not s:
                continue
            if s.startswith('#'):
                header.append(s)
                continue
            bad = _LEX_BAD.findall(body)
            if bad:
                n_lex += len(bad)
                ex_lex += [f'줄 {k} U+{ord(c):04X}' for c in bad[:3 - len(ex_lex)]]
            rows.append([x.strip(' \t') for x in s.split(',')])
    if not rows or any(len(r) != 5 for r in rows):
        raise ValueError(f'{path}: scaffold 행은 type,x,y,z,r 다섯 열이어야 한다')
    exps, n_nf, n_fmt, ex_fmt = set(), 0, 0, []
    for r in rows:
        for t in r[1:]:
            try:
                d = decimal.Decimal(t)
            except decimal.InvalidOperation:
                d = None
            if d is not None and d.is_finite() and np.isfinite(_safe_float(t)):   # float64 로도 유한 (RIMPR-02)
                exps.add(int(d.as_tuple().exponent))
                if not _FIX_RE.fullmatch(t):                   # 유한인데 ASCII 고정소수 아님 (전각 · 밑줄 · 지수 · 유니코드 공백 · v5)
                    n_fmt += 1
                    if len(ex_fmt) < 3:
                        ex_fmt.append(t)
            else:
                n_nf += 1
    steps, step_bad = [], []
    for h_ in header:
        for m in _STEP_DECL_RE.finditer(h_):
            sm = _STEP_RE.fullmatch(m.group(0))
            v, ok = _int_token(sm.group(1)) if sm else (None, False)
            if ok:
                steps.append(v)
            else:
                g = m.group(0)
                step_bad.append(g if len(g) <= 40 else g[:40] + f'…[{len(g)} 자]')
    e_min = int(min(exps)) if exps else 0
    t_, nb_t, _ex = _int_col([r[0] for r in rows])
    xyz = np.array([[_safe_float(x) for x in r[1:4]] for r in rows], np.float64)
    rr = np.array([_safe_float(r[4]) for r in rows], np.float64)
    return {'t': t_, 'xyz': xyz, 'r': rr,
            'half': 0.5 * 10.0 ** e_min, 'dec_exp': sorted(int(e) for e in exps), 'header': header, 'n': len(rows),
            'n_nonfinite': int(n_nf), 'n_int_bad': int(nb_t), 'n_nonpositive_r': int((np.isfinite(rr) & ~(rr > 0.0)).sum()),
            'n_format_bad': int(n_fmt), 'examples_format_bad': ex_fmt, 'n_lexical': int(n_lex), 'examples_lexical': ex_lex,
            'steps': steps, 'n_step_bad': len(step_bad), 'examples_step_bad': step_bad[:3]}


# ═════════════════════════ 관문 ═════════════════════════
def _check_type_map(type_map):
    if not isinstance(type_map, dict):
        raise TypeError('type_map 은 {덤프 형 정수: "AM_P" | "AM_S" | 다른 이름} dict — 기본값 없음 (침대마다 덤프 형 규약이 다르다 · 추측하지 않는다)')
    out = {}
    for k, v in type_map.items():
        if isinstance(k, bool) or not isinstance(k, (int, np.integer)) or not isinstance(v, str):
            raise TypeError(f'type_map 항목은 정수 → 문자열: {k!r} → {v!r}')
        out[int(k)] = v
    if not any(v in AM_KINDS for v in out.values()):
        raise ValueError(f'type_map 에 AM 종류 ({AM_KINDS}) 가 없다: {type_map!r}')
    return out


def _check_reuse(g):
    if g is None:
        return None
    if not isinstance(g, dict) or 'atom_step' not in g or 'contact_step' not in g:
        raise TypeError('geom_reuse 는 {"atom_step": int, "contact_step": int, "reason": str} — 두 step 기록 필수 (D19)')
    for k in ('atom_step', 'contact_step'):
        if isinstance(g[k], bool) or not isinstance(g[k], (int, np.integer)):
            raise TypeError(f'geom_reuse[{k!r}] 는 정수 step: {g[k]!r}')
    return {'atom_step': int(g['atom_step']), 'contact_step': int(g['contact_step']), 'reason': str(g.get('reason', ''))}


def _min_image(d, periodic, L):
    """축마다 최소 영상 (주기 축만) → (잔차, 정수 영상 k)."""
    k = np.zeros_like(d)
    for ax in range(3):
        if periodic[ax]:
            k[..., ax] = np.round(d[..., ax] / L[ax])
    return d - k * L, k


def _ids_index(ids):
    """id → 행 번호 조회 (없으면 −1)."""
    o = np.argsort(ids, kind='stable')
    s = ids[o]

    def look(q):
        q = np.asarray(q, np.int64)
        if not len(s):
            return np.full(len(q), -1, np.int64)
        p = np.minimum(np.searchsorted(s, q), len(s) - 1)
        return np.where(s[p] == q, o[p], -1)
    dup = s[1:][np.diff(s) == 0] if len(s) > 1 else s[:0]
    return look, dup


def _entrance(sc, A, Cd, add, um):
    """입구 검사 e1–e6 (RIMP-02 · 03 · RIMPR-01 · 02 · R01 · 03 · v5 같은 부류) — 걸린 사유를 `add` 로 더하고 요약 dict 를 돌려준다 (status PASS | REJECT).
    um = sim_to_um (scaffold µm 변환값 = 내보내는 c_um · r_um 의 유한 검사 · RIMPR-02).
    v5: 덤프 글자 어휘 = frame_layout (`atom_lexical` · `contact_lexical`) · scaffold ASCII 고정소수 · 주석 아닌 줄 어휘 = numeric_format
    (`scaffold_grammar` · `scaffold_lexical`) · scaffold 머리줄 step 선언 = int_token (`scaffold_step`) · 요약 `lexical` · `format.scaffold_bad`."""
    ea, ec = A['entrance'], Cd['entrance']
    n0 = [0]                                                   # 걸린 사유 수

    def _add(code, n, detail):
        n0[0] += 1
        add(code, 'entrance', n, detail)
    #  e1 — scaffold µm 변환 (×um) 뒤 비유한 (float64 로는 유한인 값 중 · 예: 10^306 sim × 1000 = inf) — RIMPR-02
    with np.errstate(over='ignore', invalid='ignore'):
        sx, srr = np.asarray(sc['xyz'], np.float64), np.asarray(sc['r'], np.float64)
        n_um = int((np.isfinite(sx) & ~np.isfinite(sx * um)).sum() + (np.isfinite(srr) & ~np.isfinite(srr * um)).sum())
    nf = {'scaffold': sc['n_nonfinite'], 'scaffold_um': n_um, 'atom': ea['n_nonfinite'], 'contact': ec['n_nonfinite'],
          'atom_box': ea['box_n_nonfinite'], 'contact_box': ec['box_n_nonfinite']}
    if sum(nf.values()):
        _add('nonfinite_value', sum(nf.values()), [f'{k} {v}' for k, v in nf.items() if v]
             + [str(x) for x in ea['examples_nonfinite'] + ec['examples_nonfinite']])
    npr = {'scaffold': sc['n_nonpositive_r'], 'atom': ea['n_nonpositive_radius']}
    if sum(npr.values()):
        _add('nonpositive_radius', sum(npr.values()), [f'{k} {v}' for k, v in npr.items() if v])
    ib = {'atom_step': int(not ea['step_int_ok']), 'contact_step': int(not ec['step_int_ok']),
          'atom_count': int(not ea['n_declared_int_ok']), 'contact_count': int(not ec['n_declared_int_ok']),
          'atom_id': ea['n_int_bad']['id'], 'atom_type': ea['n_int_bad']['type'],
          'contact_id1': ec['n_int_bad']['id1'], 'contact_id2': ec['n_int_bad']['id2'], 'scaffold_type': sc['n_int_bad'],
          'scaffold_step': sc['n_step_bad']}                   # scaffold 머리줄 step 선언 ASCII · int64 (v5)
    if sum(ib.values()):
        _add('int_token', sum(ib.values()), [f'{k} {v}' for k, v in ib.items() if v]
             + [f'step {ea["step_token"]!r}' if not ea['step_int_ok'] else '', f'step {ec["step_token"]!r}' if not ec['step_int_ok'] else '']
             + [repr(x) for x in ea['examples_int_bad'] + ec['examples_int_bad']]
             + [f'scaffold_step {x!r}' for x in sc['examples_step_bad']])
    shapes = {'atom': ea['box_shape'], 'contact': ec['box_shape']}
    if 'tilted' in shapes.values():
        _add('box_tilted', sum(1 for v in shapes.values() if v == 'tilted'), [f'{k} {v}' for k, v in shapes.items()])
    if 'malformed' in shapes.values():
        _add('box_format', sum(1 for v in shapes.values() if v == 'malformed'),
             [f'atom {w}' for w in ea['box_shape_why']] + [f'contact {w}' for w in ec['box_shape_why']])
    ng = {'atom': ea['n_not_g6'], 'contact': ec['n_not_g6'], 'atom_box': ea['box_n_not_g6'], 'contact_box': ec['box_n_not_g6']}
    sf = {'scaffold_grammar': sc['n_format_bad'], 'scaffold_lexical': sc['n_lexical']}   # scaffold ASCII 고정소수 · 주석 아닌 줄 어휘 (v5)
    if sum(ng.values()) + sum(sf.values()):
        _add('numeric_format', sum(ng.values()) + sum(sf.values()), [f'{k} {v}' for k, v in ng.items() if v] + [f'{k} {v}' for k, v in sf.items() if v]
             + [repr(x) for x in ea['examples_not_g6'] + ec['examples_not_g6'] + ea['box_examples_not_g6'] + ec['box_examples_not_g6']]
             + [repr(x) for x in sc['examples_format_bad']] + [f'scaffold {x}' for x in sc['examples_lexical']])
    #  e6 전수 소비 (RIMPR-01) — 열 수 다른 행 · 필수 열 중복 · 절 배치 (파서가 버리던 것) = 거부
    rw = {'atom': ea['n_rows_width_bad'], 'contact': ec['n_rows_width_bad']}
    if sum(rw.values()):
        _add('row_width', sum(rw.values()), [f'{k} {v}' for k, v in rw.items() if v]
             + [f'atom {x}' for x in ea['examples_width_bad']] + [f'contact {x}' for x in ec['examples_width_bad']])
    hd = {'atom': list(ea['header_duplicate']), 'contact': list(ec['header_duplicate'])}
    if any(hd.values()):
        _add('header_duplicate', sum(len(v) for v in hd.values()), [f'{k} {c}' for k, v in hd.items() for c in v])
    fl = {f'{nm}_{k}': int(v) for nm, e_ in (('atom', ea), ('contact', ec))
          for k, v in (('preamble_lines', e_['n_preamble_lines']), ('unknown_sections', e_['n_unknown_sections']),
                       ('duplicate_sections', len(e_['duplicate_sections'])), ('scalar_header_extra', len(e_['scalar_header_extra'])),
                       ('header_boundary', len(e_['header_boundary'])),     # 구역 이름 뒤 단어 경계 없음 (RIMPR-R01 · v5 = 공백 · 탭만)
                       ('lexical', e_['n_lexical']))}                       # 덤프 글자 어휘 (v5 · TAB · LF · CR · 0x20–0x7E 밖)
    if sum(fl.values()):
        _add('frame_layout', sum(fl.values()), [f'{k} {v}' for k, v in fl.items() if v]
             + [f'{nm} {x}' for nm, e_ in (('atom', ea), ('contact', ec)) for x in e_['examples_lexical']]
             + [f'{nm} {x!r}' for nm, e_ in (('atom', ea), ('contact', ec))
                for x in e_['unknown_sections'] + e_['duplicate_sections'] + e_['scalar_header_extra'] + e_['header_boundary']])
    return {'status': 'PASS' if not n0[0] else 'REJECT', 'rule': ENTRANCE_RULE,
            'n_nonfinite': int(sum(nf.values())), 'nonfinite': nf, 'n_nonpositive_radius': int(sum(npr.values())),
            'n_int_token_bad': int(sum(ib.values())), 'int_token_bad': ib,
            'n_rows_physical': {'atom': int(ea['n_rows_physical']), 'contact': int(ec['n_rows_physical'])},
            'n_row_width_bad': int(sum(rw.values())), 'row_width_bad': rw, 'header_duplicate': hd, 'frame_layout': fl,
            'box': shapes,
            'lexical': {'atom': int(ea['n_lexical']), 'contact': int(ec['n_lexical']), 'scaffold': int(sc['n_lexical']),
                        'rule': ('TAB · LF · CR · 출력 가능 ASCII (0x20–0x7E) 만 — 덤프 = 글 전체 (frame_layout) · scaffold = 주석 아닌 줄 '
                                 '(numeric_format · 주석 줄은 밖) · v5')},
            'format': {'rule': NUMERIC_FORMAT, 'atom_ok': ea['n_not_g6'] == 0 and ea['box_n_not_g6'] == 0,
                       'contact_ok': ec['n_not_g6'] == 0 and ec['box_n_not_g6'] == 0, 'n_not_g6': ng,
                       'scaffold_rule': SCAFFOLD_FORMAT, 'scaffold_ok': not sum(sf.values()), 'scaffold_bad': sf,
                       'area_helper_sigfig': int(H.AREA_CHECK_SIGFIG),
                       'meaning': ('덤프 = 6 유효숫자 %g 생산 포맷만 지원 — 면적 포괄 helper (봉인 · 고정 6 자리) 의 가정과 같다 · 다른 정밀도 · 혼합 = 거부 '
                                   '(기록 S 를 helper 에 넘기지 않는다 · RIMP-03) · scaffold 실수 열 = ASCII 고정소수 `[+-]?[0-9]+(.[0-9]+)?` 만 '
                                   '(생산 %.6f · v5)')}}


def _early_reject(rej, ent, sc, A, Cd, files, um, dilate_z, tmap):
    """입구 검사 실패 — 관문 계산 없이 REJECT 기록 (소비자가 읽는 키는 다 있다 · 값은 '계산 안 함')."""
    ns = int(len(sc['t']))
    z = np.zeros(0, np.int64)
    skip = '입구 검사 실패 — 관문 계산 안 함 (RIMP-02 · 03 · RIMPR-01 · 02 · R01 · 03 · v5 같은 부류)'
    with np.errstate(over='ignore', invalid='ignore'):        # 거부 기록의 입자 µm 값 (넘침 = 거부 사유 · 기록은 그대로 inf)
        c_um, r_um = sc['xyz'] * um, sc['r'] * um
    join = {'kind': JOIN_KIND, 'version': JOIN_VERSION, 'status': 'REJECT', 'rejections': rej, 'entrance': ent,
            'g_geo': {'skipped': skip, 'n_scaffold': ns},
            'g_frame': {'skipped': skip, 'atom_step': A['step'], 'contact_step': Cd['step'], 'atom_frames': A['n_frames'],
                        'contact_frames': Cd['n_frames'], 'atom_sigfig': A['sigfig'], 'contact_sigfig': Cd['sigfig']},
            'geom_reuse': None, 'scaffold_frame_claim': '주장 없음 — 입구 검사 실패',
            'files': files, 'steps': {'atom': A['step'], 'contact': Cd['step']}, 'sim_to_um': um, 'dilate_z': float(dilate_z),
            'type_map': {str(k): v for k, v in sorted(tmap.items())},
            'particles': {'c_um': c_um, 'r_um': r_um, 't': sc['t'].astype(np.int64)},
            'atom_id_of_row': np.full(ns, -1, np.int64),
            'dem_am_am': {'row_a': z, 'row_b': z.copy(), 'delta_um': np.zeros(0), 'area_um2': np.zeros(0), 'seam': np.zeros(0, bool),
                          'pflag': np.zeros(0)},
            'status_note': '입구 검사 실패 — 출처 증명 없음 · ①′ 정량 채택 · 생산 HOLD · 기구 · 시험 전용'}
    join['fp_particles'] = S3._iface_particles_fp(join['particles']['c_um'], join['particles']['r_um'], join['particles']['t'])
    join['fp_join'] = S3.iface_join_fp(join)
    return join


def am_iface_join(scaffold_csv, atom_dump, contact_dump, *, type_map, sim_to_um=SIM_TO_UM, geom_reuse=None, dilate_z=1.0):
    """G-geo · G-frame 조인 관문 → 조인 기록 dict (kind `am_iface_join` · status PASS | REJECT · 거부 사유 · 입구 검사 요약 (`entrance`) ·
    관문 요약 · 인증 입자 (µm) · fp_particles (= step3_sigma._iface_particles_fp) · DEM AM–AM 접촉 (scaffold 행 쌍) · 파일 sha256 · step · fp_join).

    type_map   {덤프 형: 'AM_P' | 'AM_S' | 다른 이름} — **필수** (real_14 = {1: AM_P, 2: AM_S, 3: SE} · case15 = {1: AM_P, 2: SE})
    geom_reuse 다른 step 기하 재사용 선언 {'atom_step', 'contact_step', 'reason'} (D19 · 기본 None = 같은 step 요구)
    dilate_z   raster 에 쓴 z 늘림 — ≠ 1 이면 거부 (N1)
    입구 검사 (e1–e6 · RIMP-02 · 03 · RIMPR-01 · 02) 가 하나라도 걸리면 관문 계산 없이 REJECT (사유만 · `g_geo` · `g_frame` = 'skipped')."""
    tmap = _check_type_map(type_map)
    reuse = _check_reuse(geom_reuse)
    um = float(sim_to_um)
    if not (np.isfinite(um) and um > 0.0):
        raise ValueError(f'sim_to_um 은 유한한 양수: {sim_to_um!r}')
    rej = []

    def add(code, gate, n, detail=None):
        rej.append({'code': code, 'gate': gate, 'n': int(n), 'detail': [x for x in (detail or []) if x != ''][:8], 'why': WHY.get(code, code)})

    sc = read_scaffold_csv(scaffold_csv)
    A = read_atom_dump_frame(atom_dump)
    Cd = read_contact_dump_frame(contact_dump)
    if float(dilate_z) != 1.0:
        add('dilate_z', 'N1', 1, [float(dilate_z)])
    ent = _entrance(sc, A, Cd, add, um)
    if ent['status'] != 'PASS':
        files = {'scaffold': _file_digest(scaffold_csv), 'atom': _file_digest(atom_dump), 'contact': _file_digest(contact_dump)}
        return _early_reject(rej, ent, sc, A, Cd, files, um, dilate_z, tmap)
    # ── G-frame ──────────────────────────────────────────────────────────────
    if A['n_frames'] != 1 or Cd['n_frames'] != 1:
        add('multi_frame', 'G-frame', 1, [A['n_frames'], Cd['n_frames']])
    gr = None
    if reuse is None:
        if A['step'] != Cd['step']:
            add('timestep_mismatch', 'G-frame', 1, [A['step'], Cd['step']])
    elif A['step'] == Cd['step']:
        add('geom_reuse_not_needed', 'G-frame', 1, [A['step']])
    elif (reuse['atom_step'], reuse['contact_step']) != (A['step'], Cd['step']):
        add('geom_reuse_mismatch', 'G-frame', 1, [reuse['atom_step'], reuse['contact_step'], A['step'], Cd['step']])
    else:
        gr = {'declared': reuse, 'observed': {'atom_step': A['step'], 'contact_step': Cd['step']}, 'status': 'accepted',
              'rule': 'D19 — 다른 step 기하 재사용 = 선언 + 두 step 기록일 때만 (위치 · 상자 · id · δ · A 관문은 그대로 다 통과해야 한다)'}
    #  f3 — 머리 · 경계 줄 **전 토큰** (옛 판은 플래그 끝 셋 · 경계 앞 두 토큰만 비교해 tilt 를 버렸다 · RIMP-02 · 기울어진 머리는 e4 가 이미 거부)
    box_equal = bool(A['entrance']['box_header'] == Cd['entrance']['box_header']
                     and A['entrance']['box_lines'] == Cd['entrance']['box_lines'])
    if not box_equal:
        add('box_mismatch', 'G-frame', 1, [A['box_flags'], Cd['box_flags']])
    if A['n_declared'] != A['n_rows'] or Cd['n_declared'] != Cd['n_rows']:
        add('count_mismatch', 'G-frame', 1, [A['n_declared'], A['n_rows'], Cd['n_declared'], Cd['n_rows']])
    look, dup = _ids_index(A['ids'])
    if len(dup):
        add('atom_id_duplicate', 'G-frame', len(dup), dup.tolist())
    ia, ib = look(Cd['id1']), look(Cd['id2'])
    orph = (ia < 0) | (ib < 0)
    if orph.any():
        add('orphan_id', 'G-frame', int(orph.sum()), np.flatnonzero(orph).tolist())
    periodic = [f == 'pp' for f in (A['box_flags'] or ('ff', 'ff', 'ff'))]
    L = A['box_hi'] - A['box_lo']
    ok = ~orph
    okn = np.flatnonzero(ok)
    pos_bad = np.zeros(len(ok), bool); shifted = np.zeros(len(ok), bool)
    max_pos_ratio = 0.0
    for pos, hpos, idx in ((Cd['pos1'], Cd['h_pos1'], ia), (Cd['pos2'], Cd['h_pos2'], ib)):
        X, hX = A['x'][idx[ok]], A['hx'][idx[ok]]
        res, k = _min_image(pos[ok] - X, periodic, L)
        tol = hpos[ok] + hX + 4.0 * _EPS * (np.abs(pos[ok]) + np.abs(X) + np.abs(k * L))
        pos_bad[okn[(np.abs(res) > tol).any(axis=1)]] = True
        shifted[okn[(k != 0).any(axis=1)]] = True
        if len(tol):
            max_pos_ratio = max(max_pos_ratio, float((np.abs(res) / tol).max()))
    if pos_bad.any():
        add('pos_mismatch', 'G-frame', int(pos_bad.sum()), np.flatnonzero(pos_bad).tolist())
    #  f6 δ 자기 일관
    iaz, ibz = np.maximum(ia, 0), np.maximum(ib, 0)
    r1 = np.where(ok, A['r'][iaz] if len(A['r']) else 0.0, np.nan); r2 = np.where(ok, A['r'][ibz] if len(A['r']) else 0.0, np.nan)
    hr1 = np.where(ok, A['hr'][iaz] if len(A['r']) else 0.0, 0.0); hr2 = np.where(ok, A['hr'][ibz] if len(A['r']) else 0.0, 0.0)
    with np.errstate(over='ignore', invalid='ignore'):        # 넘침 · inf − inf = 아래 유한 검사가 거부한다 (RIMPR-04 부분)
        dv, _k = _min_image(Cd['pos1'] - Cd['pos2'], periodic, L)
        dist = np.sqrt((dv * dv).sum(axis=1))
        wd = (np.sqrt(((Cd['h_pos1'] + Cd['h_pos2']) ** 2).sum(axis=1)) + hr1 + hr2 + Cd['h_delta']
              + 8.0 * _EPS * (np.abs(np.nan_to_num(r1)) + np.abs(np.nan_to_num(r2)) + dist + np.abs(Cd['delta'])))
        dd = np.abs(Cd['delta'] - (r1 + r2 - dist))
    dbad = ok & (dd > wd)
    if dbad.any():
        add('delta_pos_mismatch', 'G-frame', int(dbad.sum()), np.flatnonzero(dbad).tolist())
    #  RIMPR-04 (부분 · Codex 10-20 판정문 §4) — 입력이 유한이어도 제곱합이 넘치면 거리 · 허용폭 = inf → `inf > inf` = 거짓이라 위 비교가 조용히
    #  통과한다 (비-AM 두 구 x 1e160 반례) → 파생 거리 · 허용폭 · 차가 비유한인 행 = 거부 (고아 행 제외 — r1 · r2 = NaN 은 orphan_id 몫).
    #  안정한 hypot 재작성은 하지 않는다 (정량 채택 전 · 연기 조건 ④).
    dnf = ok & ~(np.isfinite(dist) & np.isfinite(wd) & np.isfinite(dd))
    if dnf.any():
        add('derived_nonfinite', 'G-frame', int(dnf.sum()), np.flatnonzero(dnf).tolist())
    nonpos = Cd['delta'] <= 0.0
    if nonpos.any():
        add('delta_nonpositive', 'G-frame', int(nonpos.sum()), np.flatnonzero(nonpos).tolist())
    g_frame = {'atom_step': A['step'], 'contact_step': Cd['step'], 'atom_frames': A['n_frames'], 'contact_frames': Cd['n_frames'],
               'box_equal': box_equal, 'box_flags': list(A['box_flags'] or ()), 'n_atoms': A['n_rows'], 'n_contact_rows': Cd['n_rows'],
               'n_orphan_rows': int(orph.sum()), 'n_pos_mismatch': int(pos_bad.sum()), 'max_pos_ratio': max_pos_ratio,
               'n_rows_image_shift': int(shifted.sum()), 'n_rows_image_shift_flag0': int((shifted & (Cd['pflag'] == 0.0)).sum()),
               'n_delta_pos_mismatch': int(dbad.sum()), 'max_delta_pos_ratio': float((dd[ok] / wd[ok]).max()) if ok.any() else None,
               'n_derived_nonfinite': int(dnf.sum()),
               'n_delta_nonpositive': int(nonpos.sum()), 'atom_sigfig': A['sigfig'], 'contact_sigfig': Cd['sigfig'],
               'rule': ('f1 프레임 각 1 · f2 TIMESTEP 같음 (선언된 재사용만 예외) · f3 상자 같음 (머리 · 경계 줄 전 토큰) · f4 id 유일 · 머리 수 = 행 수 · 고아 0 · '
                        'f5 pos = 원자 위치 (주기 축 정수 영상 · 토큰 반폭 `_half_ulp` 합) · f6 δ = r1 + r2 − |최소 영상 거리| (반폭 전파) · δ > 0 · '
                        'f6 거리 · 허용폭 · 차 유한 (RIMPR-04 부분)')}
    # ── G-geo ────────────────────────────────────────────────────────────────
    hs = float(sc['half'])
    st, sxyz, sr = sc['t'], sc['xyz'], sc['r']
    ns = len(st)
    if not np.isin(st, list(SCAFFOLD_TYPE)).all():
        add('scaffold_type_unknown', 'G-geo', int((~np.isin(st, list(SCAFFOLD_TYPE))).sum()))
    stepm = list(sc['steps'])                                   # ASCII · int64 step 선언만 (나머지는 입구 int_token · scaffold_step — v5)
    if stepm:
        if any(s_ != A['step'] for s_ in stepm):
            add('scaffold_step_mismatch', 'G-geo', 1, stepm + [A['step']])
        claim = 'G-frame 까지 — scaffold 머리줄의 step = 원자 덤프 step'
    else:
        claim = 'G-geo 만 — scaffold 머리줄에 원 덤프 step 이 없다 (v3 §6-3 · 기하 대응까지만 주장)'
    kind_of = np.array([tmap.get(int(t), '') for t in A['types']], dtype=str)
    am_idx = np.flatnonzero(np.isin(kind_of, AM_KINDS))
    nd = len(am_idx)
    Xd, hXd, rd, hrd = A['x'][am_idx], A['hx'][am_idx], A['r'][am_idx], A['hr'][am_idx]
    ncand = np.zeros(ns, np.int64); cand = np.zeros(ns, np.int64); pos_ratio = np.full(ns, np.nan)
    if nd:
        for c0 in range(0, ns, 256):
            sl = slice(c0, min(ns, c0 + 256))
            res, _kk = _min_image(sxyz[sl, None, :] - Xd[None, :, :], periodic, L)
            tol = hs + hXd[None, :, :] + 4.0 * _EPS * (np.abs(sxyz[sl, None, :]) + np.abs(Xd[None, :, :]) + 1.0)
            m = (np.abs(res) <= tol).all(axis=2)
            ncand[sl] = m.sum(axis=1)
            first = np.argmax(m, axis=1)
            cand[sl] = first
            rr = (np.abs(res) / tol).max(axis=2)
            pos_ratio[sl] = np.where(ncand[sl] == 1, rr[np.arange(rr.shape[0]), first], np.nan)
    unm, amb, one = ncand == 0, ncand > 1, ncand == 1
    if unm.any():
        add('scaffold_row_unmatched', 'G-geo', int(unm.sum()), np.flatnonzero(unm).tolist())
    if amb.any():
        add('scaffold_row_ambiguous', 'G-geo', int(amb.sum()), np.flatnonzero(amb).tolist())
    hits = np.bincount(cand[one], minlength=nd) if nd else np.zeros(0, np.int64)
    if nd and (hits == 0).any():
        add('dump_am_unmatched', 'G-geo', int((hits == 0).sum()), A['ids'][am_idx][hits == 0].tolist())
    if nd and (hits > 1).any():
        add('dump_am_multi', 'G-geo', int((hits > 1).sum()), A['ids'][am_idx][hits > 1].tolist())
    good = one & (hits[cand] == 1) if nd else np.zeros(ns, bool)
    tbad = np.zeros(ns, bool); rbad = np.zeros(ns, bool); rratio = np.full(ns, np.nan)
    if nd:
        tbad = one & np.array([SCAFFOLD_TYPE.get(int(st[i]), '?') != kind_of[am_idx[cand[i]]] for i in range(ns)], bool)
        rtol = hs + hrd[cand] + 4.0 * _EPS * (np.abs(sr) + np.abs(rd[cand]))
        rratio = np.where(one, np.abs(sr - rd[cand]) / rtol, np.nan)
        rbad = one & (rratio > 1.0)
    if tbad.any():
        add('type_mismatch', 'G-geo', int(tbad.sum()), np.flatnonzero(tbad).tolist())
    if rbad.any():
        add('radius_mismatch', 'G-geo', int(rbad.sum()), np.flatnonzero(rbad).tolist())
    atom_id_of_row = np.where(good, A['ids'][am_idx][cand] if nd else -1, -1).astype(np.int64)
    #  δ · 면적 · 접촉 집합 — AM–AM 접촉 행 (두 원자 모두 1:1 로 짝지어진 것)
    row_of_atom = np.full(len(A['ids']), -1, np.int64)
    if nd:
        row_of_atom[am_idx[cand[good]]] = np.flatnonzero(good)
    ra_ = np.where(ok, row_of_atom[iaz] if len(row_of_atom) else -1, -1)
    rb_ = np.where(ok, row_of_atom[ibz] if len(row_of_atom) else -1, -1)
    q = np.flatnonzero((ra_ >= 0) & (rb_ >= 0))
    a_, b_ = ra_[q], rb_[q]
    ea, eb = hs + A['hx'][ia[q]], hs + A['hx'][ib[q]]
    dvs, ks = _min_image(sxyz[a_] - sxyz[b_], periodic, L)
    ds = np.sqrt((dvs * dvs).sum(axis=1))
    dsc = sr[a_] + sr[b_] - ds
    wsc = (np.sqrt(((ea + eb) ** 2).sum(axis=1)) + (hs + A['hr'][ia[q]]) + (hs + A['hr'][ib[q]]) + Cd['h_delta'][q]
           + 8.0 * _EPS * (np.abs(sr[a_]) + np.abs(sr[b_]) + ds + np.abs(Cd['delta'][q])))
    dmis = np.abs(Cd['delta'][q] - dsc) > wsc
    if dmis.any():
        add('delta_scaffold_mismatch', 'G-geo', int(dmis.sum()), q[dmis].tolist())
    seam = (ks != 0).any(axis=1) if len(q) else np.zeros(0, bool)
    if len(q):
        _ac, _lo, _hi, _lb0, beyond, xd = H._contact_area_rows(A['r'][ia[q]], A['r'][ib[q]], Cd['delta'][q], Cd['area'][q])
    else:
        beyond, xd = np.zeros(0, bool), {'uncertified': np.zeros(0, bool), 'negative': np.zeros(0, bool)}
    if beyond.any():
        add('area_enclosure', 'G-geo', int(beyond.sum()), q[beyond].tolist())
    #  RIMP-02 — 진단 helper 가 비교에서 **뺀** 행 (음수 · 미인증) 을 인증으로 읽지 않는다: PASS = 전 AM–AM 행 인증
    neg_q = np.asarray(xd['negative'], bool)
    unc_q = np.asarray(xd['uncertified'], bool) & ~neg_q
    if neg_q.any():
        add('area_negative', 'G-geo', int(neg_q.sum()), q[neg_q].tolist())
    if unc_q.any():
        add('area_uncertified', 'G-geo', int(unc_q.sum()), q[unc_q].tolist())
    not_q = np.ones(len(Cd['area']), bool); not_q[q] = False
    n_neg_other = int((not_q & (Cd['area'] < 0.0)).sum())
    pa, pb = np.minimum(a_, b_), np.maximum(a_, b_)
    keyp = pa * max(ns, 1) + pb
    uk, cnt = np.unique(keyp, return_counts=True)
    if (cnt > 1).any():
        add('dem_duplicate_pair', 'G-geo', int((cnt > 1).sum()), uk[cnt > 1].tolist())
    dem_set = set(keyp[~seam].tolist())
    #  g4 — scaffold 확실한 접촉 (비주기 거리 · raster 가 보는 쌍) ⊆ 덤프 (짝지어진 행끼리만)
    n_cert, miss = 0, []
    if ns >= 2 and nd:
        from scipy.spatial import cKDTree
        e_row = np.where(good[:, None], hs + hXd[cand], np.inf)
        er_row = np.where(good, hs + hrd[cand], np.inf)
        for i, j in sorted(cKDTree(sxyz).query_pairs(2.0 * float(sr.max()) + 1e-9)):
            if not (good[i] and good[j]):
                continue
            d_ = float(np.sqrt(((sxyz[i] - sxyz[j]) ** 2).sum()))
            w_ = float(np.sqrt(((e_row[i] + e_row[j]) ** 2).sum()) + er_row[i] + er_row[j])
            if float(sr[i] + sr[j] - d_) > w_:
                n_cert += 1
                if (min(i, j) * ns + max(i, j)) not in dem_set:
                    miss.append((int(i), int(j)))
    if miss:
        add('dem_contact_missing', 'G-geo', len(miss), miss)
    e_max = hs + (hXd.max(axis=0) if nd else np.zeros(3))
    with np.errstate(over='ignore', invalid='ignore'):        # 넘침 = 아래 유한 검사가 거부한다 (RIMPR-04 부분)
        dbound = um * float(np.sqrt(((2.0 * e_max) ** 2).sum()) + 2.0 * (hs + (float(hrd.max()) if nd else 0.0)))
        delta_um, area_um2 = Cd['delta'][q] * um, Cd['area'][q] * um * um
    #  RIMPR-04 (부분) — 파생 δ 반올림 폭 (원장 delta_bound_um 후보 · 한-AM 좌표 ~1e160 = 제곱합 넘침) · 내보내는 AM–AM δ · 면적 µm 값 (sim_to_um 1e160 =
    #  ×um² 넘침) 이 비유한 = 거부 — inf 폭 · 면적을 인증된 값으로 발행하지 않는다 (후단 원장 검사에 기대지 않는다)
    geo_nf = [nm for nm, fin in (('delta_bound_um', bool(np.isfinite(dbound))), ('dem_am_am.delta_um', bool(np.isfinite(delta_um).all())),
                                 ('dem_am_am.area_um2', bool(np.isfinite(area_um2).all()))) if not fin]
    if geo_nf:
        add('derived_nonfinite', 'G-geo', len(geo_nf), geo_nf)
    g_geo = {'n_scaffold': int(ns), 'n_dump_am': int(nd), 'n_matched': int(good.sum()),
             'n_unmatched': int(unm.sum()), 'n_ambiguous': int(amb.sum()),
             'max_pos_ratio': (float(np.nanmax(pos_ratio)) if np.isfinite(pos_ratio).any() else None),
             'max_radius_ratio': (float(np.nanmax(rratio)) if np.isfinite(rratio).any() else None),
             'scaffold_half_box': hs, 'scaffold_dec_exp': sc['dec_exp'], 'dump_sigfig': A['sigfig'],
             'delta_bound_um': dbound,
             'delta_bound_rule': 'µm · √Σ(2·(h_s + max h_d))² + 2·(h_s + max h_r) — scaffold δ 의 참값 대비 상한 (원장 delta_bound_um 후보)',
             'derived_nonfinite': geo_nf,
             'n_dem_am_am': int(len(q)), 'n_dem_am_am_seam': int(seam.sum()),
             'n_delta_scaffold_mismatch': int(dmis.sum()),
             'max_delta_scaffold_ratio': (float((np.abs(Cd['delta'][q] - dsc) / wsc).max()) if len(q) else None),
             'n_area_tested': int((~xd['uncertified'] & ~xd['negative']).sum()), 'n_area_beyond': int(beyond.sum()),
             'n_area_uncertified': int(xd['uncertified'].sum()), 'n_area_negative': int(neg_q.sum()),
             'area_all_certified': bool(int((~xd['uncertified'] & ~xd['negative']).sum()) == int(len(q))),
             'n_area_negative_not_am_am': n_neg_other,
             'area_sigfig_assumed': int(H.AREA_CHECK_SIGFIG),
             'area_scope': ('조인이 인증하는 면적 = AM–AM 행 (두 원자 모두 scaffold 와 1:1) 뿐 — AM–SE · SE–SE 행의 c_cpl[22] 는 인증하지 않는다 '
                            '(음수 수만 기록 · n_area_negative_not_am_am)'),
             'n_scaffold_certain_pairs': int(n_cert), 'n_dem_contact_missing': int(len(miss)),
             'rule': ('g1 1:1 (축마다 |Δ| ≤ h_s + h_d · 주기 축 최소 영상 · 형 · 반경) · g2 δ_dump ↔ δ_scaffold · '
                      'g3 c_cpl[22] ↔ lens_geometry 포괄 (lhs_descriptor_harvest._contact_area_rows) · 음수 · 미인증 = 거부 (전 행 인증) · '
                      'g4 scaffold 확실한 접촉 ⊆ 덤프')}
    join = {'kind': JOIN_KIND, 'version': JOIN_VERSION, 'status': ('PASS' if not rej else 'REJECT'), 'rejections': rej,
            'entrance': ent,
            'g_geo': g_geo, 'g_frame': g_frame, 'geom_reuse': (gr if not rej else None),
            'scaffold_frame_claim': claim,
            'files': {'scaffold': _file_digest(scaffold_csv), 'atom': _file_digest(atom_dump), 'contact': _file_digest(contact_dump)},
            'steps': {'atom': A['step'], 'contact': Cd['step']}, 'sim_to_um': um, 'dilate_z': float(dilate_z),
            'type_map': {str(k): v for k, v in sorted(tmap.items())},
            'particles': {'c_um': sxyz * um, 'r_um': sr * um, 't': st.astype(np.int64)},
            'atom_id_of_row': atom_id_of_row,
            'dem_am_am': {'row_a': pa.astype(np.int64), 'row_b': pb.astype(np.int64), 'delta_um': delta_um,
                          'area_um2': area_um2, 'seam': seam.astype(bool), 'pflag': Cd['pflag'][q]},
            'status_note': '출처 증명만 — 덤프 경로의 부류 · 면적 (c_cpl[22]) 채택 아님 · ①′ 정량 채택 · 생산 HOLD · 기구 · 시험 전용'}
    join['fp_particles'] = S3._iface_particles_fp(join['particles']['c_um'], join['particles']['r_um'], join['particles']['t'])
    join['fp_join'] = S3.iface_join_fp(join)
    return join


def join_summary(join):
    """배열 (입자 · DEM 접촉 · id 사상) 을 뺀 요약 — JSON · 보고용."""
    return {k: v for k, v in join.items() if k not in ('particles', 'atom_id_of_row', 'dem_am_am')}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--scaffold', required=True)
    ap.add_argument('--atom', required=True)
    ap.add_argument('--contact', required=True)
    ap.add_argument('--type-map', required=True, help='예: 1:AM_P,2:AM_S,3:SE (덤프 형 → 이름 · 기본값 없음)')
    ap.add_argument('--json', default='', help='요약 JSON 출력 경로 (배열 제외)')
    a = ap.parse_args(argv)
    tmap = {int(k): v for k, v in (x.split(':') for x in a.type_map.split(','))}
    jn = am_iface_join(a.scaffold, a.atom, a.contact, type_map=tmap)
    txt = json.dumps(join_summary(jn), ensure_ascii=False, indent=1,
                     default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))
    if a.json:
        with open(a.json, 'w', encoding='utf-8') as fh:
            fh.write(txt + '\n')
    print(f"status {jn['status']} · 거부 {[x['code'] for x in jn['rejections']]}")
    return 0 if jn['status'] == 'PASS' else 3


if __name__ == '__main__':
    sys.exit(main())
