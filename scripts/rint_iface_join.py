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
scaffold 머리줄에 원 덤프 step 이 없으면 scaffold ↔ 덤프는 **G-geo 까지만** 주장한다 (v3 §6-3).  N1: dilate_z ≠ 1 = 거부 (기하가 DEM 이 아님).
입구 검사 (RIMP-02 · 03 · Codex 10-14 판정문 §3 · §4 · 1저자 Q2 (가) — 봉인 helper 는 그대로 · 이 소비자에서 엄격) — 관문 계산 **전**, 하나라도 걸리면
  REJECT (관문 계산 생략 · 사유만):
  e1  유한 — scaffold x y z r · 원자 x y z radius · 접촉 pos1 pos2 면적 δ 주기 플래그 · 상자 경계 (nan · inf · 못 읽는 토큰 = nonfinite_value)
  e2  양수 — scaffold r · 원자 radius > 0 (nonpositive_radius) · 상자 hi > lo (box_format)
  e3  정확 정수 — TIMESTEP · 머리 수 · 원자 id · type · 접촉 id1 · id2 · scaffold type 토큰 = 정수 문자열만 (`2060000.9` · `201.0` · `1e+06` = int_token ·
      `int(float(…))` 로 줄이지 않는다)
  e4  지원 상자 — 직교 `ITEM: BOX BOUNDS f1 f2 f3` (플래그 [pfsm]² · p 는 pp 만) + 경계 줄 셋 · 줄마다 토큰 둘.  기울어진 머리 (xy xz yz) = box_tilted (지원 밖 ·
      tilt 를 버리고 비교하지 않는다) · 그 밖 모양 = box_format.  상자 동일 (f3) = 머리 · 경계 줄 **전 토큰** 비교
  e5  형식 = **6 유효숫자 `%g` 생산 포맷만** (LIGGGHTS dump 기본 · 토큰 = '%g' % 값) — 다른 정밀도 · 끝 0 · 혼합 포맷 = numeric_format.  면적 포괄
      helper 는 고정 6 자리 (`lhs_descriptor_harvest.AREA_CHECK_SIGFIG`) 라 지원 형식을 그 가정과 같게 묶는다 (기록 S 를 helper 에 넘기지 않는다 · 봉인 무변경)
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
JOIN_VERSION = 'g_geo_g_frame_v2'           # v2 (RIMP-02 · 03) = 입구 검사 e1–e5 + AM–AM 면적 전 행 인증 · v1 (10-13) = 그 전
SIM_TO_UM = 1000.0              # LIGGGHTS 상자 단위 → µm (덱 머리 "Scale: r*1000" · real_14 README)
AM_KINDS = ('AM_P', 'AM_S')
SCAFFOLD_TYPE = {1: 'AM_P', 2: 'AM_S'}                         # scaffold CSV 규약 (머리줄 "AM_P=1,AM_S=2")
POS1 = ('c_cpl[1]', 'c_cpl[2]', 'c_cpl[3]')                    # pair/gran/local pos (덱 `compute … pair/gran/local pos id force …`)
POS2 = ('c_cpl[4]', 'c_cpl[5]', 'c_cpl[6]')
_EPS = float(np.finfo(np.float64).eps)
_STEP_RE = re.compile(r'(?:time)?step\s*[=:]?\s*(\d+)', re.I)
_INT_RE = re.compile(r'[+-]?\d+')                              # e3 정확 정수 토큰 (소수점 · 지수 · 밑줄 없음)
_BOX_FLAG_RE = re.compile(r'[pfsm]{2}')                        # e4 LAMMPS 경계 플래그 (축마다 lo · hi)
_TILT_TOKENS = ('xy', 'xz', 'yz')
NUMERIC_FORMAT = 'g6'                                          # e5 — 지원하는 유일한 실수 형식 (6 유효숫자 `%g` · LIGGGHTS dump 기본)
ENTRANCE_RULE = ('e1 유한 · e2 양수 (반경 · 상자 길이) · e3 정확 정수 (step · 머리 수 · id · type) · e4 직교 상자만 (기울어진 머리 = 거부) · '
                 'e5 6 유효숫자 %g 생산 포맷만 (다른 정밀도 · 혼합 = 거부) — 하나라도 걸리면 관문 계산 없이 REJECT (RIMP-02 · 03)')

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
    'nonfinite_value': 'e1 — 비유한 (nan · inf) 또는 못 읽는 수 토큰 (NaN 비교는 어떤 허용폭 검사도 실패시키지 않는다 — 입구에서 거부 · RIMP-02)',
    'nonpositive_radius': 'e2 — 반경 ≤ 0 (scaffold 또는 원자 덤프)',
    'int_token': 'e3 — 정수여야 할 토큰 (TIMESTEP · 머리 수 · id · type) 이 정확한 정수 문자열이 아니다 (int(float(…)) 로 줄이지 않는다 · RIMP-02)',
    'box_tilted': 'e4 — 기울어진 상자 머리 (xy xz yz) · 직교 상자만 지원 (tilt 를 버리고 비교하지 않는다 · RIMP-02)',
    'box_format': 'e4 — 상자 머리 · 경계 줄 모양이 직교 LAMMPS 꼴이 아니다 (플래그 셋 · 줄마다 토큰 둘 · hi > lo)',
    'numeric_format': 'e5 — 실수 토큰이 6 유효숫자 %g 생산 포맷이 아니다 (다른 정밀도 · 끝 0 · 혼합 · 면적 포괄 helper 의 고정 6 자리 가정 밖 · RIMP-03)',
    'area_negative': 'g3 — AM–AM 접촉의 c_cpl[22] 가 음수 (진단 helper 는 음수 행을 포괄 비교에서 뺀다 — 뺀 것을 인증으로 읽지 않는다 · RIMP-02)',
    'area_uncertified': 'g3 — AM–AM 접촉의 면적 포괄을 인증할 수 없다 (토큰 상자 위 거리 하한 ≤ 0 · 생산자 오차 상한 없음 — "포괄 밖 0" ≠ "전 행 인증" · RIMP-02)',
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
    """e3 — 정확한 정수 문자열이면 (int, True) · 아니면 (None, False).  `int(float(…))` 로 줄이지 않는다 (RIMP-02 · Codex `2060000.9`)."""
    if isinstance(tok, str) and _INT_RE.fullmatch(tok):
        return int(tok), True
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
    """e4 — 상자 머리 토큰 · 경계 줄 셋 → (모양 'orthogonal' | 'tilted' | 'malformed', 사유 목록)."""
    if any(t in _TILT_TOKENS for t in hdr_tok):
        return 'tilted', ['xy xz yz 머리 (삼사정계)']
    why = []
    if len(hdr_tok) != 3:
        why.append(f'플래그 수 {len(hdr_tok)} ≠ 3')
    for f in hdr_tok:
        if not _BOX_FLAG_RE.fullmatch(f) or (('p' in f) and f != 'pp'):
            why.append(f'플래그 {f!r}')
    for k, b in enumerate(lines3):
        if len(b) != 2:
            why.append(f'경계 줄 {k} 토큰 {len(b)} ≠ 2')
    return ('orthogonal' if not why else 'malformed'), why


def _scan_frame(path, count_item, rows_item):
    """마지막 프레임의 (step · 머리 수 · 상자 플래그 · 상자 토큰 · 열 머리 · 행) + 프레임 수 + 입구 검사 재료 (step · 머리 수 토큰 정수 여부 ·
    상자 머리 · 경계 줄 전 토큰 · 상자 모양).  정수가 아닌 step · 머리 수 = None (줄이지 않는다)."""
    with _open_text(path) as fh:
        lines = fh.read().splitlines()
    starts = [i for i, ln in enumerate(lines) if ln.startswith('ITEM: TIMESTEP')]
    if not starts:
        raise ValueError(f'{path}: `ITEM: TIMESTEP` 이 없다 — LIGGGHTS 덤프가 아니다')
    i = starts[-1]
    step_tok = (lines[i + 1].split() or [''])[0] if i + 1 < len(lines) else ''
    step, step_ok = _int_token(step_tok)
    n_decl, n_decl_ok, n_decl_tok = None, True, None
    flags, btok, bhdr, blines, hdr, rows = None, None, None, None, None, []
    i += 2
    while i < len(lines):
        ln = lines[i]
        if ln.startswith('ITEM: TIMESTEP'):
            break
        if ln.startswith(count_item):
            n_decl_tok = (lines[i + 1].split() or [''])[0] if i + 1 < len(lines) else ''
            n_decl, n_decl_ok = _int_token(n_decl_tok)
            i += 2
            continue
        if ln.startswith('ITEM: BOX BOUNDS'):
            bhdr = ln.replace('ITEM: BOX BOUNDS', '').split()
            flags = tuple(bhdr[-3:]) if len(bhdr) >= 3 else None
            blines = [lines[i + 1 + k].split() if i + 1 + k < len(lines) else [] for k in range(3)]
            btok = [tuple(b[:2]) for b in blines]
            i += 4
            continue
        if ln.startswith(rows_item):
            hdr = ln.replace(rows_item, '').split()
            i += 1
            while i < len(lines) and not lines[i].startswith('ITEM:'):
                v = lines[i].split()
                if len(v) == len(hdr):
                    rows.append(v)
                i += 1
            continue
        i += 1
    if hdr is None or btok is None:
        raise ValueError(f'{path}: `{rows_item}` 또는 `ITEM: BOX BOUNDS` 가 마지막 프레임에 없다')
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
                         'box_examples_not_g6': binfo['examples_not_g6']}}


def read_atom_dump_frame(path):
    """원자 덤프 마지막 프레임 — id · type · x (N, 3) · r · 토큰 반폭 (hx · hr) · 파일 유효숫자 · step · 프레임 수 · 상자 · 입구 검사 재료
    (`entrance` — 비유한 · %g 아님 · 정수 아님 · 반경 ≤ 0 · 상자 모양)."""
    F = _scan_frame(path, 'ITEM: NUMBER OF ATOMS', 'ITEM: ATOMS')
    hdr, rows = F.pop('header'), F.pop('rows')
    need = ('id', 'type', 'x', 'y', 'z', 'radius')
    miss = [c for c in need if c not in hdr]
    if miss:
        raise ValueError(f'{path}: 원자 덤프에 열 {miss} 이 없다 (있는 열: {hdr})')
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
    `n_nonfinite` · type 정수 아님 = `n_int_bad` · r ≤ 0 = `n_nonpositive_r` — 입구 검사 e1–e3 이 거부한다 · 예외로 멈추지 않는다)."""
    header, rows = [], []
    with _open_text(path) as fh:
        for ln in fh:
            s = ln.strip()
            if not s:
                continue
            if s.startswith('#'):
                header.append(s)
                continue
            rows.append([x.strip() for x in s.split(',')])
    if not rows or any(len(r) != 5 for r in rows):
        raise ValueError(f'{path}: scaffold 행은 type,x,y,z,r 다섯 열이어야 한다')
    exps, n_nf = set(), 0
    for r in rows:
        for t in r[1:]:
            try:
                d = decimal.Decimal(t)
            except decimal.InvalidOperation:
                d = None
            if d is not None and d.is_finite():
                exps.add(int(d.as_tuple().exponent))
            else:
                n_nf += 1
    e_min = int(min(exps)) if exps else 0
    t_, nb_t, _ex = _int_col([r[0] for r in rows])
    xyz = np.array([[_safe_float(x) for x in r[1:4]] for r in rows], np.float64)
    rr = np.array([_safe_float(r[4]) for r in rows], np.float64)
    return {'t': t_, 'xyz': xyz, 'r': rr,
            'half': 0.5 * 10.0 ** e_min, 'dec_exp': sorted(int(e) for e in exps), 'header': header, 'n': len(rows),
            'n_nonfinite': int(n_nf), 'n_int_bad': int(nb_t), 'n_nonpositive_r': int((np.isfinite(rr) & ~(rr > 0.0)).sum())}


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


def _entrance(sc, A, Cd, add):
    """입구 검사 e1–e5 (RIMP-02 · 03) — 걸린 사유를 `add` 로 더하고 요약 dict 를 돌려준다 (status PASS | REJECT)."""
    ea, ec = A['entrance'], Cd['entrance']
    n0 = [0]                                                   # 걸린 사유 수

    def _add(code, n, detail):
        n0[0] += 1
        add(code, 'entrance', n, detail)
    nf = {'scaffold': sc['n_nonfinite'], 'atom': ea['n_nonfinite'], 'contact': ec['n_nonfinite'],
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
          'contact_id1': ec['n_int_bad']['id1'], 'contact_id2': ec['n_int_bad']['id2'], 'scaffold_type': sc['n_int_bad']}
    if sum(ib.values()):
        _add('int_token', sum(ib.values()), [f'{k} {v}' for k, v in ib.items() if v]
             + [f'step {ea["step_token"]!r}' if not ea['step_int_ok'] else '', f'step {ec["step_token"]!r}' if not ec['step_int_ok'] else '']
             + [repr(x) for x in ea['examples_int_bad'] + ec['examples_int_bad']])
    shapes = {'atom': ea['box_shape'], 'contact': ec['box_shape']}
    if 'tilted' in shapes.values():
        _add('box_tilted', sum(1 for v in shapes.values() if v == 'tilted'), [f'{k} {v}' for k, v in shapes.items()])
    if 'malformed' in shapes.values():
        _add('box_format', sum(1 for v in shapes.values() if v == 'malformed'),
             [f'atom {w}' for w in ea['box_shape_why']] + [f'contact {w}' for w in ec['box_shape_why']])
    ng = {'atom': ea['n_not_g6'], 'contact': ec['n_not_g6'], 'atom_box': ea['box_n_not_g6'], 'contact_box': ec['box_n_not_g6']}
    if sum(ng.values()):
        _add('numeric_format', sum(ng.values()), [f'{k} {v}' for k, v in ng.items() if v]
             + [repr(x) for x in ea['examples_not_g6'] + ec['examples_not_g6'] + ea['box_examples_not_g6'] + ec['box_examples_not_g6']])
    return {'status': 'PASS' if not n0[0] else 'REJECT', 'rule': ENTRANCE_RULE,
            'n_nonfinite': int(sum(nf.values())), 'nonfinite': nf, 'n_nonpositive_radius': int(sum(npr.values())),
            'n_int_token_bad': int(sum(ib.values())), 'int_token_bad': ib,
            'box': shapes,
            'format': {'rule': NUMERIC_FORMAT, 'atom_ok': ea['n_not_g6'] == 0 and ea['box_n_not_g6'] == 0,
                       'contact_ok': ec['n_not_g6'] == 0 and ec['box_n_not_g6'] == 0, 'n_not_g6': ng,
                       'area_helper_sigfig': int(H.AREA_CHECK_SIGFIG),
                       'meaning': ('6 유효숫자 %g 생산 포맷만 지원 — 면적 포괄 helper (봉인 · 고정 6 자리) 의 가정과 같다 · 다른 정밀도 · 혼합 = 거부 '
                                   '(기록 S 를 helper 에 넘기지 않는다 · RIMP-03)')}}


def _early_reject(rej, ent, sc, A, Cd, files, um, dilate_z, tmap):
    """입구 검사 실패 — 관문 계산 없이 REJECT 기록 (소비자가 읽는 키는 다 있다 · 값은 '계산 안 함')."""
    ns = int(len(sc['t']))
    z = np.zeros(0, np.int64)
    skip = '입구 검사 실패 — 관문 계산 안 함 (RIMP-02 · 03)'
    join = {'kind': JOIN_KIND, 'version': JOIN_VERSION, 'status': 'REJECT', 'rejections': rej, 'entrance': ent,
            'g_geo': {'skipped': skip, 'n_scaffold': ns},
            'g_frame': {'skipped': skip, 'atom_step': A['step'], 'contact_step': Cd['step'], 'atom_frames': A['n_frames'],
                        'contact_frames': Cd['n_frames'], 'atom_sigfig': A['sigfig'], 'contact_sigfig': Cd['sigfig']},
            'geom_reuse': None, 'scaffold_frame_claim': '주장 없음 — 입구 검사 실패',
            'files': files, 'steps': {'atom': A['step'], 'contact': Cd['step']}, 'sim_to_um': um, 'dilate_z': float(dilate_z),
            'type_map': {str(k): v for k, v in sorted(tmap.items())},
            'particles': {'c_um': sc['xyz'] * um, 'r_um': sc['r'] * um, 't': sc['t'].astype(np.int64)},
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
    입구 검사 (e1–e5 · RIMP-02 · 03) 가 하나라도 걸리면 관문 계산 없이 REJECT (사유만 · `g_geo` · `g_frame` = 'skipped')."""
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
    ent = _entrance(sc, A, Cd, add)
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
    dv, _k = _min_image(Cd['pos1'] - Cd['pos2'], periodic, L)
    dist = np.sqrt((dv * dv).sum(axis=1))
    wd = (np.sqrt(((Cd['h_pos1'] + Cd['h_pos2']) ** 2).sum(axis=1)) + hr1 + hr2 + Cd['h_delta']
          + 8.0 * _EPS * (np.abs(np.nan_to_num(r1)) + np.abs(np.nan_to_num(r2)) + dist + np.abs(Cd['delta'])))
    dd = np.abs(Cd['delta'] - (r1 + r2 - dist))
    dbad = ok & (dd > wd)
    if dbad.any():
        add('delta_pos_mismatch', 'G-frame', int(dbad.sum()), np.flatnonzero(dbad).tolist())
    nonpos = Cd['delta'] <= 0.0
    if nonpos.any():
        add('delta_nonpositive', 'G-frame', int(nonpos.sum()), np.flatnonzero(nonpos).tolist())
    g_frame = {'atom_step': A['step'], 'contact_step': Cd['step'], 'atom_frames': A['n_frames'], 'contact_frames': Cd['n_frames'],
               'box_equal': box_equal, 'box_flags': list(A['box_flags'] or ()), 'n_atoms': A['n_rows'], 'n_contact_rows': Cd['n_rows'],
               'n_orphan_rows': int(orph.sum()), 'n_pos_mismatch': int(pos_bad.sum()), 'max_pos_ratio': max_pos_ratio,
               'n_rows_image_shift': int(shifted.sum()), 'n_rows_image_shift_flag0': int((shifted & (Cd['pflag'] == 0.0)).sum()),
               'n_delta_pos_mismatch': int(dbad.sum()), 'max_delta_pos_ratio': float((dd[ok] / wd[ok]).max()) if ok.any() else None,
               'n_delta_nonpositive': int(nonpos.sum()), 'atom_sigfig': A['sigfig'], 'contact_sigfig': Cd['sigfig'],
               'rule': ('f1 프레임 각 1 · f2 TIMESTEP 같음 (선언된 재사용만 예외) · f3 상자 같음 (머리 · 경계 줄 전 토큰) · f4 id 유일 · 머리 수 = 행 수 · 고아 0 · '
                        'f5 pos = 원자 위치 (주기 축 정수 영상 · 토큰 반폭 `_half_ulp` 합) · f6 δ = r1 + r2 − |최소 영상 거리| (반폭 전파) · δ > 0')}
    # ── G-geo ────────────────────────────────────────────────────────────────
    hs = float(sc['half'])
    st, sxyz, sr = sc['t'], sc['xyz'], sc['r']
    ns = len(st)
    if not np.isin(st, list(SCAFFOLD_TYPE)).all():
        add('scaffold_type_unknown', 'G-geo', int((~np.isin(st, list(SCAFFOLD_TYPE))).sum()))
    stepm = [int(m.group(1)) for h_ in sc['header'] for m in _STEP_RE.finditer(h_)]
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
    dbound = um * float(np.sqrt(((2.0 * e_max) ** 2).sum()) + 2.0 * (hs + (float(hrd.max()) if nd else 0.0)))
    g_geo = {'n_scaffold': int(ns), 'n_dump_am': int(nd), 'n_matched': int(good.sum()),
             'n_unmatched': int(unm.sum()), 'n_ambiguous': int(amb.sum()),
             'max_pos_ratio': (float(np.nanmax(pos_ratio)) if np.isfinite(pos_ratio).any() else None),
             'max_radius_ratio': (float(np.nanmax(rratio)) if np.isfinite(rratio).any() else None),
             'scaffold_half_box': hs, 'scaffold_dec_exp': sc['dec_exp'], 'dump_sigfig': A['sigfig'],
             'delta_bound_um': dbound,
             'delta_bound_rule': 'µm · √Σ(2·(h_s + max h_d))² + 2·(h_s + max h_r) — scaffold δ 의 참값 대비 상한 (원장 delta_bound_um 후보)',
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
            'dem_am_am': {'row_a': pa.astype(np.int64), 'row_b': pb.astype(np.int64), 'delta_um': Cd['delta'][q] * um,
                          'area_um2': Cd['area'][q] * um * um, 'seam': seam.astype(bool), 'pflag': Cd['pflag'][q]},
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
