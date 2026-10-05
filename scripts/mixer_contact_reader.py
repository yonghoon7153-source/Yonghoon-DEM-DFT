#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""믹서 보조 판독기 — SE–SE 접촉 군집 (s1) · AM–SE 부착 (s2) (2026-10-05 · 사전등록 강성 축 §12-4).

    python3 scripts/mixer_contact_reader.py <런 디렉터리> [<런 디렉터리> ...] --json out.json
    python3 scripts/mixer_contact_reader.py --selftest
    python3 scripts/mixer_contact_reader.py --bench 100000          # 합성 10 만 입자 프레임 한 장의 시간 (기록용 · 판정 아님)

━━ 등록 (docs/reviews/mixer_highbo_stiffness_prereg_20260929.md §12-4 — 결과 전에 정의 · 바꾸지 않는다) ━━━━━━━━━━━━━━━━━
  (s1) SE–SE 접촉 군집 = 중심 거리 < r_i + r_j (겹침 > 0 = SJKR 점착이 작동하는 접촉) 인 SE–SE 쌍의 연결 성분.
       보고: 크기 ≥ 2 성분에 든 SE 분율 · 가장 큰 성분의 SE 분율 · 수 가중 평균 성분 크기 · 크기 히스토그램 (1 · 2 · 3–9 · 10–99 · ≥ 100).
  (s2) AM–SE 부착: AM 하나 이상과 겹친 SE 분율 · AM 하나당 붙은 SE 평균 (AM_P · AM_S 따로).
  프레임 = t₀ 과 bin 1 계획 프레임.  LC_ref_r2 · E0_ref 에도 같은 식으로.  판독기는 LU 의 M 열람 **전에** 구현 · 시험한다.
  반경 출처 = 덤프 열 `radius` (판독기 measure_mixing_index.py 와 같은 열) — 템플릿이 `radius constant` 라 상마다 하나
  (AM_P 6.813e-4 · AM_S 3.028e-4 · SE 7.57e-5 m = 계획 지름 / 2) — 그 일치를 먼저 대조하고 어긋나면 TECH.
  기술 실패는 TECH 로 기록하고, 새 결정 없이 다시 돌리지 않는다.

━━ 구현 규약 (등록 문구의 읽기 — 새 관측량을 만들지 않는다) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  · 접촉 판정 = LIGGGHTS pair gran 과 같은 식 `rsq < (r_i + r_j)²` — **엄격** (정확히 맞닿으면 접촉 아님 · 셀프테스트 ④).
  · 성분 = SE 전부를 마디로 (접촉 없는 SE = 크기 1 성분 — 히스토그램의 '1' 칸).
  · "수 가중 평균 성분 크기" = 성분마다 무게 1 (수평균) = N_SE / 성분 수 (크기 1 포함).
  · "크기 히스토그램" = 크기 구간별 **성분 수**.
  · "AM 하나 이상과 겹친 SE 분율" = 아무 AM (AM_P ∪ AM_S) 기준 + 상별 (AM_P · AM_S 따로) — 두 AM 에 닿은 SE 는 분율에서 한 번 ·
    "AM 하나당 붙은 SE" 에서는 AM 마다 한 번 (= 그 상 AM–SE 접촉 쌍 수 / 그 상 AM 수 · 셀프테스트 ⑤).
  · type → 상 = 그 런의 `deck_meta.json` (`types` · `radius_m` · `deck_sha256` = in.mixer) + in.mixer 템플릿 (`atom_type` · `radius constant`)
    — 하드코딩 · 추정 없음 (확립 못 하면 TECH).
  · 프레임 선택 = 판독기 measure_mixing_index.py 의 함수를 **가져다 쓴다** (deck_plan · _t0_exact · bin_window_files · frame_digest) —
    그 파일은 고치지 않는다 (sha256 이 발사 · 스모크 봉인에 들어 있다).  bin_window_files 의 격자 = 판독기 analyse 의 bin 격자
    (scripts/mixer_gate_reader_diff.py 가 차등 시험으로 상주 대조).  계획 t₀ 정확히 (없으면 앞 프레임으로 대신하지 않는다) ·
    bin 1 = 계획 덤프 격자 위 · 결손 · 같은 step 둘 · 격자 밖 · 헤더/스키마 불량 = TECH.  다른 bin 의 프레임은 열지 않는다 (⑱).
  · 회전 런 = 계획 2 바퀴 (bin 1 = 계획 마지막 bin) · E0 = 계획 회전 0 (`run 0`) → 자기 t₀ 만 (bin 1 = NOT_APPLICABLE).  그 밖 = TECH.
  · 원자 = t₀ 원자 수 = deck_meta n_atoms_planned (n_expected 파일이 있으면 그것과도) · bin 프레임의 (id, type) 집합 = t₀ 그대로.
  · SE 0 개 = UNDEFINED (분모 0 — 0 을 값처럼 내지 않는다) · 값 없음.
  · ⛔ M 없음 — Lacey M · 칸 분산 · 혼합 지수를 계산하지 않는다 (판독기의 칸 함수를 가져오지 않는다 · 셀프테스트 ⑰).
    이 판독기의 값은 M 과 따로 검증된다.

━━ 해상도 (보고 전용 · 정의 불변) — 덤프 좌표는 `%g` 6 유효숫자다 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  덱의 `dump dmp all custom … x y z … radius` 에 dump_modify format 이 없다 → LIGGGHTS 기본 `%g` (6 유효숫자 · 원장 SELF-63 이
  LHS 덤프에서 실측).  드럼 좌표 |x| ≈ 0.01 m 의 마지막 자리 = 1e-7 m (반폭 5e-8 m/좌표).  등록 판정 (덤프 값으로 rsq < Σr²) 은 그대로 하고,
  쌍마다 반올림 폭 (lhs_contact_audit v2 규칙: 유효숫자 S = max(관측, 6) · 값의 반폭 0.5·10^(e−S+1)) 으로 참 거리의 범위를 같이 적는다:
      확실 (lo) = 반올림 범위 안 어디서도 겹침  ⊆  등록  ⊆  가능 (hi) = 범위 안 어딘가에서 겹침.
  s1 · s2 의 스칼라는 접촉 집합에 단조 (간선을 더하면 줄지 않는다) 라 참 값은 [lo, hi] 안이다 (히스토그램 칸은 단조가 아니라 범위를 내지 않는다).
  ⚠ 겹침이 반올림 폭 (좌표 크기에 따라 반폭 5e-9 – 5e-8 m) 보다 작은 접촉은 덤프로 가를 수 없다 — 그 몫이 [lo, hi] 의 폭이다.
    참고 (어림 · 측정 아님): 등록 정적 평형 겹침 SE–SE ref ×20 (§12-3) = 0.055 · 0.114 % (LU212 · LU637 · r 7.57e-5 m 기준 ≈ 42 · 86 nm) ·
    점착이 약한 LC · E0 는 중력 하중 겹침이라 한 자릿수 이상 작다 (E0 soft 실측 중앙 δ/r_min 0.034 % · ×20 경화 Hertz 환산 20^(−2/3)
    → 수 nm).  ⇒ 같은 정의라도 덤프에서 가려지는 비율이 런마다 다를 수 있다 — 해석 전에 [lo, hi] 를 같이 본다.
  이 범위는 관측량이 아니라 등록 관측량의 **측정 해상도**다 (판정 · 관문 아님).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
import time

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree

_SCR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCR)
#  ★ 프레임 선택 = 판독기 그대로 (가져다 쓴다 · 고치지 않는다).  M 을 계산하는 함수 (cell_stats · analyse · bin_window_stats ·
#    e0_t0_stats · t0_floor) 는 가져오지 않는다 — 셀프테스트 ⑰ 이 가져오는 이름의 집합을 고정한다.
from measure_mixing_index import deck_plan, _t0_exact, bin_window_files, frame_digest   # noqa: E402
from measure_bed_aspect import frames, read_dump, validate_frame                       # noqa: E402

SCHEMA = 'mixer_contact_reader/1'
REGISTERED = 'docs/reviews/mixer_highbo_stiffness_prereg_20260929.md §12-4'
REG_BIN = 1                      # "등록 2 바퀴 bin 1"
REG_REVS = 2                     # 회전 런 = 2 바퀴 계획 (bin 1 = 계획 마지막 bin) · E0 = 회전 0
PHASES = ('AM_P', 'AM_S', 'SE')
AM_PHASES = ('AM_P', 'AM_S')
#: 크기 히스토그램 칸 (이름 · 최소 · 최대 — None = 위 열림) — 등록 그대로 1 · 2 · 3–9 · 10–99 · ≥ 100
SIZE_BINS = (('1', 1, 1), ('2', 2, 2), ('3-9', 3, 9), ('10-99', 10, 99), ('>=100', 100, None))
#: 유효숫자 바닥 = LIGGGHTS 기본 `%g` — 관측 최대 자릿수는 형식 정밀도의 **하한**이라 (끝 0 이 지워진다) 그대로 쓰면 폭이 헐거워진다.
#:   lhs_contact_audit.SIGFIG_FLOOR 와 같은 규칙 (S = max(관측, 6) · SELF-63).
SIGFIG_FLOOR = 6
#: 부동소수로 가릴 수 있는 자릿수 상한 — 이 위면 13 으로 둔다 (참 정밀도 ≥ 13 이면 폭이 커지는 쪽 = 보수)
SIGFIG_MAX_TEST = 12
DECK_META_SCHEMA = 'mixer_deck_meta/1'
S1_KEYS = ('se_frac_in_clusters', 'largest_frac', 'mean_size_number')
S2_KEYS = ('se_attached_any_frac', 'se_attached_frac_AM_P', 'se_attached_frac_AM_S', 'se_per_am_AM_P', 'se_per_am_AM_S')
#: 판독기 (measure_mixing_index) 에서 가져와도 되는 이름 = 프레임 선택뿐 (셀프테스트 ⑰)
FRAME_TOOL_NAMES = frozenset({'deck_plan', '_t0_exact', 'bin_window_files', 'frame_digest'})
FRAME_TOOL_REQUIRED = frozenset({'deck_plan', '_t0_exact', 'bin_window_files'})
#: 결과에 나오면 안 되는 키 — M · 칸 분산 (판독기의 출력 이름)
M_KEYS = frozenset({'M', 'S0', 'SR', 'S0_all', 'SR_all', 'M_final', 'M_mean', 'M_all', 'M_t0', 's2'})
RESOLUTION_NOTE = ('프레임마다 resolution = 보고 전용 — 덤프 좌표 (%g) 반올림 안의 참 값 범위 (확실 lo ⊆ 등록 ⊆ 가능 hi) · '
                   '정의 · 판정 · 관문 아님 (§12-4 정의 불변)')


class Tech(Exception):
    """기술 실패 — 값 없이 TECH 로 기록한다 (사유 목록)."""

    def __init__(self, reasons):
        self.reasons = [reasons] if isinstance(reasons, str) else [str(r_) for r_ in reasons]
        super().__init__(' · '.join(self.reasons))


class Undefined(Exception):
    """정의 불가 (SE 0 개) — 0 을 값처럼 내지 않는다."""


def _sha_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def _frame_tools_sha():
    """가져다 쓰는 프레임 선택 코드의 sha256 (판독기 · 덤프 읽기) — 실제로 import 된 파일."""
    return {os.path.basename(sys.modules[f.__module__].__file__): _sha_file(sys.modules[f.__module__].__file__)
            for f in (deck_plan, read_dump)}


def _pos_int(v):
    return isinstance(v, int) and not isinstance(v, bool) and v > 0


def _real_pos(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) and v > 0


# ═════════════════════════════ 해상도 — 덤프 자릿수 ═════════════════════════════
def sigfigs_effective(V):
    """찍힌 값들의 유효숫자 S = max(관측 최대, 6).  토큰 대신 부동소수로 가린다 — 값 v 가 S 자리 십진수로 정확한가
    (float(토큰) 은 그 십진수에 가장 가까운 double 이라 S ≤ 12 에서는 v·10^(S−1−e) 가 정수에서 1e-3 안).  S > 12 → 13 (보수)."""
    v = np.abs(np.asarray(V, dtype=float).ravel())
    v = v[np.isfinite(v) & (v > 0)]
    if v.size == 0:
        return SIGFIG_FLOOR
    e = np.floor(np.log10(v) + 1e-12)
    for S in range(SIGFIG_FLOOR, SIGFIG_MAX_TEST + 1):
        sc = v * 10.0 ** (S - 1 - e)
        if np.all(np.abs(sc - np.round(sc)) <= 1e-3):
            return S
    return SIGFIG_MAX_TEST + 1


def half_width(V, S):
    """값 → 반올림 반폭 0.5·10^(e − S + 1) (e = 십진 지수) · 0 → 0.  lhs_contact_audit._half_ulp 의 벡터판
    (S = 파일 전체 유효숫자 — 토큰 자신의 자릿수가 아니다: `%g` 는 끝 0 을 지운다).  e 에 +1e-12 = 10 의 거듭제곱에서 큰 쪽 (보수)."""
    V = np.abs(np.asarray(V, dtype=float))
    out = np.zeros_like(V)
    nz = V > 0
    out[nz] = 0.5 * 10.0 ** (np.floor(np.log10(V[nz]) + 1e-12) - S + 1)
    return out


def classify_pairs(P, R, h, hr, ia, ib):
    """쌍 (ia, ib) → (reg, lo, hi) 불리언 배열.

      reg  등록 판정 = rsq < (r_i + r_j)² (LIGGGHTS pair gran 과 같은 엄격 부등식 · 덤프 값 그대로)
      lo   확실 — 좌표 반올림 범위 안 어디서도 참 거리 < Σr      (d + P + Q < Σr − 반경 폭)
      hi   가능 — 범위 안 어딘가에서 참 거리 < Σr               (d − P < Σr + 반경 폭)
    P = Σ_k |n_k|·w_k (w = 두 입자 좌표 반폭의 합) · Q = ‖w‖²/(2d) — d_참 ∈ [d − P, d + P + Q] 는 엄밀하다
    (아래: ‖u+Δ‖ ≥ n·(u+Δ) ≥ d − P · 위: √(1+x) ≤ 1 + x/2).  lo ⊆ reg ⊆ hi 를 구성으로 보장한다 (경계 반올림까지)."""
    u = P[ib] - P[ia]
    rsq = np.einsum('ij,ij->i', u, u)
    rs = R[ia] + R[ib]
    reg = rsq < rs * rs
    d = np.sqrt(rsq)
    w = h[ia] + h[ib]
    wn = np.sqrt(np.einsum('ij,ij->i', w, w))
    pos = d > 0
    dd = np.where(pos, d, 1.0)
    proj = np.einsum('ij,ij->i', np.abs(u), w) / dd
    upper = np.where(pos, d + proj + wn * wn / (2.0 * dd), wn)
    lower = np.where(pos, d - proj, 0.0)
    rr = hr[ia] + hr[ib]
    return reg, reg & (upper < rs - rr), reg | (lower < rs + rr)


# ═════════════════════════════ 대응 · 프레임 ═════════════════════════════
_RE_TPL = re.compile(r'^\s*fix\s+\S+\s+all\s+particletemplate/sphere\s+\d+\s+atom_type\s+(\d+)\b(.*)$', re.M)


def phase_map(run_dir):
    """deck_meta.json (types · radius_m · deck_sha256) + in.mixer 템플릿 → dict(phases={상: {type, radius_m}}, …).
    확립 못 하면 Tech — 하드코딩 · 추정으로 메우지 않는다."""
    deck = os.path.join(run_dir, 'in.mixer')
    meta_p = os.path.join(run_dir, 'deck_meta.json')
    if not os.path.isfile(deck):
        raise Tech(f'{run_dir}: in.mixer 없음')
    if not os.path.isfile(meta_p):
        raise Tech('deck_meta.json 없음 — type → 상 대응 · 계획 반경을 확립할 수 없다 (하드코딩 · 추정으로 메우지 않는다)')
    try:
        with open(meta_p, encoding='utf-8') as f:
            meta = json.load(f)
    except (OSError, ValueError) as e:
        raise Tech(f'deck_meta.json 을 읽을 수 없다: {e}')
    if not isinstance(meta, dict) or meta.get('schema') != DECK_META_SCHEMA:
        raise Tech(f'deck_meta.json schema ≠ {DECK_META_SCHEMA}')
    deck_sha = _sha_file(deck)
    if meta.get('deck_sha256') != deck_sha:
        raise Tech(f'deck_meta.deck_sha256 ≠ in.mixer sha256 ({deck_sha[:16]}…) — 이 런의 메타가 아니다')
    types, radii = meta.get('types'), meta.get('radius_m')
    if not isinstance(types, dict) or not isinstance(radii, dict):
        raise Tech('deck_meta.json 에 types · radius_m 표가 없다')
    errs, ph = [], {}
    for p in PHASES:
        keys = [k for k, v in types.items() if v == p]
        if len(keys) != 1:
            errs.append(f'deck_meta.types 에서 {p} 의 type 이 {len(keys)} 개 {sorted(keys)} — 정확히 하나여야 한다')
            continue
        k = keys[0]
        if not (isinstance(k, str) and k.isdigit() and str(int(k)) == k and int(k) >= 1):
            errs.append(f'deck_meta.types 의 키 {k!r} ({p}) 가 양의 정수 type 이 아니다')
            continue
        r = radii.get(p)
        if not _real_pos(r):
            errs.append(f'deck_meta.radius_m[{p}] = {r!r} — 유한 양수가 아니다')
            continue
        ph[p] = dict(type=int(k), radius_m=float(r))
    if errs:
        raise Tech(errs)
    with open(deck, encoding='utf-8', errors='replace') as f:
        txt = f.read()
    tpl = {}
    for m in _RE_TPL.finditer(txt):
        t = int(m.group(1))
        mr = re.search(r'\bradius\s+constant\s+(\S+)', m.group(2))
        if not mr:
            errs.append(f'in.mixer 템플릿 atom_type {t} 의 반경이 constant 가 아니다 — 상마다 반경 하나라는 전제 (§12-4) 가 서지 않는다')
            continue
        try:
            rv = float(mr.group(1))
        except ValueError:
            errs.append(f'in.mixer 템플릿 atom_type {t} 반경 {mr.group(1)!r} 이 수가 아니다')
            continue
        if t in tpl:
            errs.append(f'in.mixer 에 atom_type {t} 템플릿이 둘 이상')
            continue
        tpl[t] = rv
    want = {v['type']: p for p, v in ph.items()}
    if set(tpl) != set(want):
        errs.append(f'in.mixer 템플릿 atom_type {sorted(tpl)} ≠ deck_meta 상 type {sorted(want)}')
    for t, p in sorted(want.items()):
        if t in tpl and tpl[t] != ph[p]['radius_m']:
            errs.append(f'{p} (type {t}) 계획 반경 불일치 — deck_meta radius_m {ph[p]["radius_m"]!r} · in.mixer 템플릿 {tpl[t]!r}')
    n_plan, revs, steps = meta.get('n_atoms_planned'), meta.get('revolutions'), meta.get('steps')
    if not _pos_int(n_plan):
        errs.append(f'deck_meta.n_atoms_planned = {n_plan!r} — 양의 정수가 아니다')
    if not (isinstance(revs, int) and not isinstance(revs, bool) and revs >= 0):
        errs.append(f'deck_meta.revolutions = {revs!r} — 0 이상 정수가 아니다')
    if not (isinstance(steps, dict) and _pos_int(steps.get('t0_planned')) and _pos_int(steps.get('dump_every'))):
        errs.append('deck_meta.steps 에 t0_planned · dump_every (양의 정수) 가 없다')
    n_exp = None
    ne_p = os.path.join(run_dir, 'n_expected')
    if os.path.isfile(ne_p):
        with open(ne_p, encoding='utf-8') as f:
            raw = f.read().strip()
        if not raw.isdigit():
            errs.append(f'n_expected 파일 {raw!r} 이 정수가 아니다')
        else:
            n_exp = int(raw)
            if _pos_int(n_plan) and n_exp != n_plan:
                errs.append(f'n_expected {n_exp} ≠ deck_meta n_atoms_planned {n_plan}')
    if errs:
        raise Tech(errs)
    return dict(phases=ph, deck_sha256=deck_sha, deck_meta_sha256=_sha_file(meta_p), n_planned=int(n_plan), revolutions=int(revs),
                meta_steps=dict(t0_planned=int(steps['t0_planned']), dump_every=int(steps['dump_every'])),
                arm=meta.get('arm'), seed=meta.get('seed'), n_expected_file=n_exp)


def frame_plan(run_dir, pm):
    """판독기 (measure_mixing_index) 와 같은 프레임 선택 → dict(mode, plan, n_revs, t0_step, t0_path, bin_steps, bin_paths).
    순서 = 판독기 bin_window_stats 와 같다: 계획 t₀ (정확히 · 검사) → bin 1 창 입력 집합 (결손 · 같은 step 둘 · 격자 밖 → 프레임을 열지 않고 TECH)
    → 프레임마다 형식 검사는 읽기 직전 (analyse_run).  읽는 파일 = 계획 t₀ · bin 1 계획 격자뿐 (다른 bin 은 열지 않는다).  못 서면 Tech."""
    try:
        plan = deck_plan(os.path.join(run_dir, 'in.mixer'))
    except (ValueError, AttributeError, OSError, ZeroDivisionError) as e:
        raise Tech(f'덱 계획을 읽을 수 없다 (deck_plan): {e}')
    spr, de = plan['steps_per_rev'], plan['dump_every']
    n_revs = int(round(plan['steps_run'] / spr)) if spr > 0 else -1
    if plan['steps_run'] == 0:
        mode = 't0_only'
        if pm['revolutions'] != 0:
            raise Tech(f'덱은 회전 0 (run 0) 인데 deck_meta.revolutions = {pm["revolutions"]}')
    elif n_revs == REG_REVS:
        mode = 'rot2'
        if pm['revolutions'] != REG_REVS:
            raise Tech(f'덱은 {REG_REVS} 바퀴인데 deck_meta.revolutions = {pm["revolutions"]}')
    else:
        raise Tech(f'계획 {n_revs} 바퀴 — 등록 (§12-4) 은 2 바퀴 계획의 bin 1 (회전 런) 또는 회전 0 (E0 · t₀ 만) 이다')
    post = os.path.join(run_dir, 'post')
    fr = frames(post) if os.path.isdir(post) else []
    try:
        t0, p0 = _t0_exact(fr, plan, run_dir, '평가 런')
    except SystemExit as e:                                      # 판독기는 거부를 SystemExit 로 낸다 — 여기서는 TECH
        raise Tech(str(e))
    ms = pm['meta_steps']
    if ms['t0_planned'] != t0 or ms['dump_every'] != de:
        raise Tech(f'deck_meta.steps (t0_planned {ms["t0_planned"]} · dump_every {ms["dump_every"]}) ≠ 덱 계획 (t₀ {t0} · 덤프 {de})')
    bin_steps, bin_paths = [], []
    if mode == 'rot2':
        w = bin_window_files(post, t0, spr, de, plan['steps_total'], (REG_BIN,))
        lat = sorted(w['lattice'])
        if not lat:
            raise Tech(f'bin {REG_BIN} 의 계획 덤프 격자가 비었다')
        probs = []
        if w['miss']:
            probs.append(f'bin {REG_BIN} 결손 {len(w["miss"])}/{len(lat)} 프레임 (step {w["miss"][:4]}'
                         f'{"…" if len(w["miss"]) > 4 else ""}) — 미완주이거나 덤프가 빠졌다')
        if w['dup']:
            probs.append(f'bin {REG_BIN} 에 같은 step 의 덤프가 둘 이상 (step {w["dup"][:4]}) — 어느 것이 참인지 모른다')
        if w['off']:
            probs.append(f'bin {REG_BIN} 에 계획 덤프 격자 밖 step {w["off"][:4]} (t₀ {t0} + k·{de})')
        if probs:
            raise Tech(probs)
        bin_steps = [int(s_) for s_ in lat]
        bin_paths = [w['cur'][s_][0] for s_ in lat]
    return dict(mode=mode, plan=plan, n_revs=n_revs, t0_step=int(t0), t0_path=p0, bin_steps=bin_steps, bin_paths=bin_paths)


# ═════════════════════════════ 관측량 ═════════════════════════════
def _s1(n_se, ei, ej):
    """SE–SE 접촉 간선 → 등록 s1 (군집 SE 분율 · 가장 큰 성분 분율 · 수평균 크기 · 성분 수 히스토그램)."""
    if len(ei):
        g = coo_matrix((np.ones(len(ei), dtype=np.int8), (ei, ej)), shape=(n_se, n_se))
        nc, lab = connected_components(g, directed=False)
    else:
        nc, lab = n_se, np.arange(n_se)
    sizes = np.bincount(lab, minlength=nc)
    hist = {}
    for name, lo_, hi_ in SIZE_BINS:
        m = sizes >= lo_ if hi_ is None else (sizes >= lo_) & (sizes <= hi_)
        hist[name] = int(m.sum())
    return dict(se_frac_in_clusters=float(sizes[sizes >= 2].sum()) / n_se, largest_frac=float(sizes.max()) / n_se,
                mean_size_number=float(n_se) / float(nc), n_components=int(nc), largest_size=int(sizes.max()), hist_components=hist)


def _s2(n_se, n_am, cross):
    """AM–SE 접촉 (상마다 SE 색인 배열 — 쌍마다 하나) → 등록 s2.  AM 이 없는 상의 'AM 당' = None (0/0)."""
    any_ = np.zeros(n_se, dtype=bool)
    out = {}
    for p in AM_PHASES:
        js = cross[p]
        att = np.zeros(n_se, dtype=bool)
        att[js] = True
        any_ |= att
        out[f'se_attached_frac_{p}'] = float(att.sum()) / n_se
        out[f'se_per_am_{p}'] = float(len(js)) / n_am[p] if n_am[p] > 0 else None
    out['se_attached_any_frac'] = float(any_.sum()) / n_se
    return {k: out[k] for k in S2_KEYS}


def frame_quantities(D, pm):
    """한 프레임 (read_dump 결과) → dict(n, s1_se_clusters, s2_am_se_attach, pairs, resolution) — 키 이름에 등록 꼬리표 (s1 · s2) 를 붙인다 (판독기의 칸 분산 키 `s2` 와 섞이지 않게 · ⑰).  type · 반경 대조 실패 = Tech · SE 0 = Undefined."""
    t = np.asarray(D['type']).astype(np.int64)
    type_of = {v['type']: p for p, v in pm['phases'].items()}
    extra = sorted(set(np.unique(t).tolist()) - set(type_of))
    if extra:
        raise Tech(f'덤프에 계획 밖 type {extra} (deck_meta 상 type {sorted(type_of)}) — 상을 정할 수 없다')
    r = np.asarray(D['radius'], dtype=float)
    S_r = sigfigs_effective(r)
    hr = half_width(r, S_r)
    for p, v in pm['phases'].items():
        m = t == v['type']
        if m.any():
            bad = np.abs(r[m] - v['radius_m']) > hr[m] + 1e-12 * v['radius_m']
            if bad.any():
                raise Tech(f'{p} (type {v["type"]}) 덤프 반경 ≠ 계획 {v["radius_m"]!r} — {int(bad.sum())} 개 '
                           f'(예: {r[m][bad][:3].tolist()}) · radius constant 템플릿이면 상마다 하나여야 한다')
    P = np.column_stack([D['x'], D['y'], D['z']]).astype(float)
    S_xyz = sigfigs_effective(P)
    h = half_width(P, S_xyz)
    idx = {p: np.flatnonzero(t == v['type']) for p, v in pm['phases'].items()}
    n = {p: int(len(ix)) for p, ix in idx.items()}
    if n['SE'] == 0:
        raise Undefined('SE 0 개 — s1 · s2 의 분모가 0 이라 정의할 수 없다 (0 을 값처럼 내지 않는다)')
    #  후보 반경 = Σr + 반경 폭 둘 + 좌표 폭 상한 (2·√3·h_max) — '가능' 쌍까지 빠짐없이 (등록 쌍 ⊆ 가능 ⊆ 후보)
    pad = (2.0 * float(hr.max()) + 2.0 * math.sqrt(3.0) * float(h.max())) * (1.0 + 1e-9) + 1e-15
    ise = idx['SE']
    Pse, Rse, hse, hrse = P[ise], r[ise], h[ise], hr[ise]
    tree_se = cKDTree(Pse)
    pr = tree_se.query_pairs(2.0 * float(Rse.max()) + pad, output_type='ndarray') if n['SE'] > 1 else np.zeros((0, 2), np.int64)
    ia, ib = pr[:, 0].astype(np.int64), pr[:, 1].astype(np.int64)
    reg, lo, hi = classify_pairs(Pse, Rse, hse, hrse, ia, ib)
    s1 = {side: _s1(n['SE'], ia[m_], ib[m_]) for side, m_ in (('reg', reg), ('lo', lo), ('hi', hi))}
    pairs = {side: {'SE-SE': int(m_.sum())} for side, m_ in (('reg', reg), ('lo', lo), ('hi', hi))}
    cross = {'reg': {}, 'lo': {}, 'hi': {}}
    for p in AM_PHASES:
        ix = idx[p]
        if not len(ix):
            for side in cross:
                cross[side][p] = np.zeros(0, np.int64)
                pairs[side][f'{p}-SE'] = 0
            continue
        lists = cKDTree(P[ix]).query_ball_tree(tree_se, float(r[ix].max()) + float(Rse.max()) + pad)
        ja = np.repeat(np.arange(len(ix), dtype=np.int64), [len(l_) for l_ in lists])
        js = np.fromiter((j_ for l_ in lists for j_ in l_), dtype=np.int64, count=int(len(ja)))
        #  두 집합을 한 배열로 (AM 먼저 · SE 는 len(ix) 만큼 민다) → 같은 판정 함수
        Pc, Rc = np.vstack([P[ix], Pse]), np.concatenate([r[ix], Rse])
        hc, hrc = np.vstack([h[ix], hse]), np.concatenate([hr[ix], hrse])
        c_reg, c_lo, c_hi = classify_pairs(Pc, Rc, hc, hrc, ja, js + len(ix))
        for side, m_ in (('reg', c_reg), ('lo', c_lo), ('hi', c_hi)):
            cross[side][p] = js[m_]
            pairs[side][f'{p}-SE'] = int(m_.sum())
    s2 = {side: _s2(n['SE'], n, cross[side]) for side in cross}
    head = {side: {**{k: s1[side][k] for k in S1_KEYS}, **s2[side]} for side in ('lo', 'hi')}
    return dict(n={p: n[p] for p in PHASES}, s1_se_clusters=s1['reg'], s2_am_se_attach=s2['reg'], pairs=pairs['reg'],
                resolution=dict(sigfigs_xyz=int(S_xyz), sigfigs_radius=int(S_r), half_width_max_m=float(h.max()),
                                pairs_lo=pairs['lo'], pairs_hi=pairs['hi'], lo=head['lo'], hi=head['hi']))


def _flat(row):
    """프레임 행 → bin 평균 · SD 에 쓰는 평평한 dict (등록 스칼라 · 히스토그램 칸 · 접촉 수 · 해상도 lo/hi)."""
    f = {k: row['s1_se_clusters'][k] for k in S1_KEYS}
    f.update({f'hist.{name}': row['s1_se_clusters']['hist_components'][name] for name, _, _ in SIZE_BINS})
    f.update({k: row['s2_am_se_attach'][k] for k in S2_KEYS})
    f.update(n_components=row['s1_se_clusters']['n_components'], largest_size=row['s1_se_clusters']['largest_size'])
    f.update({f'pairs.{k}': v for k, v in row['pairs'].items()})
    for side in ('lo', 'hi'):
        f.update({f'{side}.{k}': row['resolution'][side][k] for k in S1_KEYS + S2_KEYS})
    return f


def bin_summary(rows, steps):
    """bin 1 프레임 행 → 평균 · SD (ddof 1 · 한 프레임이면 0 — 판독기 by_rev 와 같은 규약).  None 이 낀 키는 None."""
    flats = [_flat(r_) for r_ in rows]
    mean, sd = {}, {}
    for k in flats[0]:
        v = [f_[k] for f_ in flats]
        if any(x is None for x in v):
            mean[k] = sd[k] = None
            continue
        a = np.asarray(v, dtype=float)
        mean[k] = float(a.mean())
        sd[k] = float(a.std(ddof=1)) if len(a) > 1 else 0.0
    return dict(status='OK', bin=REG_BIN, n=len(rows), steps=[int(s_) for s_ in steps], mean=mean, sd=sd, frames=rows,
                sd_note='± = bin 안 프레임 SD (ddof 1) — seed 불확실성이 아니다 (§12-4)')


def analyse_run(run_dir, progress=False):
    """한 런 → 결과 dict (status OK · TECH · UNDEFINED).  TECH · UNDEFINED 면 값 (t0 · bin) 없음."""
    t_all = time.time()
    res = dict(schema=SCHEMA, registered=REGISTERED, run=os.path.basename(os.path.normpath(run_dir)), run_dir=os.path.abspath(run_dir),
               status=None, reasons=[], mode=None, phases=None, plan=None, t0=None, bin=None, resolution_note=RESOLUTION_NOTE,
               provenance=dict(reader_sha256=_sha_file(os.path.abspath(__file__)), frame_tools_sha256=_frame_tools_sha(),
                               deck_sha256=None, deck_meta_sha256=None, launch_record_sha256=None, dumps=[], dumps_digest=None),
               timing=None)
    rows, t_plan = [], 0.0
    try:
        pm = phase_map(run_dir)
        res['phases'] = {p: dict(v) for p, v in pm['phases'].items()}
        res['provenance'].update(deck_sha256=pm['deck_sha256'], deck_meta_sha256=pm['deck_meta_sha256'])
        lr = os.path.join(run_dir, 'launch_record.json')
        if os.path.isfile(lr):
            res['provenance']['launch_record_sha256'] = _sha_file(lr)
        t1 = time.time()
        fp = frame_plan(run_dir, pm)
        t_plan = time.time() - t1
        pl = fp['plan']
        res['mode'] = fp['mode']
        res['plan'] = dict(t0_step=fp['t0_step'], n_revs=fp['n_revs'], steps_per_rev=pl['steps_per_rev'], dump_every=pl['dump_every'],
                           steps_total=pl['steps_total'], n_atoms_planned=pm['n_planned'], arm=pm['arm'], seed=pm['seed'],
                           bin=REG_BIN if fp['mode'] == 'rot2' else None, bin_steps=fp['bin_steps'])
        ref = None
        todo = [(fp['t0_step'], fp['t0_path'])] + list(zip(fp['bin_steps'], fp['bin_paths']))
        for k_, (st, pth) in enumerate(todo):
            ta = time.time()
            sha = _sha_file(pth)
            pr_ = validate_frame(pth)                            # 판독기와 같은 형식 검사 (헤더 · 스키마 · id 유일 · 유한 좌표 · 양의 반경)
            if pr_:
                raise Tech(f'step {st}: 프레임 검사 (헤더 · 스키마) 실패 {pr_[:3]}')
            D = read_dump(pth)
            if _sha_file(pth) != sha:                            # 검사 · 읽기 사이에 바뀐 파일 (아직 쓰는 중인 런 등) — 섞인 값을 내지 않는다
                raise Tech(f'step {st}: 덤프가 읽는 사이에 바뀌었다 ({os.path.basename(pth)}) — 완주 뒤 다시')
            tb = time.time()
            ids = np.asarray(D['id']).astype(np.int64)
            typ = np.asarray(D['type']).astype(np.int64)
            o = np.argsort(ids, kind='stable')
            if ref is None:
                if len(ids) != pm['n_planned']:
                    raise Tech(f't₀ (step {st}) 원자 수 {len(ids)} ≠ deck_meta n_atoms_planned {pm["n_planned"]}')
                ref = (ids[o], typ[o])
            elif len(ids) != len(ref[0]) or not np.array_equal(ids[o], ref[0]) or not np.array_equal(typ[o], ref[1]):
                raise Tech(f'step {st}: 원자 집합 (id · type) 이 t₀ 과 다르다 — {len(ids)} 개 vs t₀ {len(ref[0])} 개 '
                           '(잃은 · 늘어난 · type 이 바뀐 원자)')
            try:
                q = frame_quantities(D, pm)
            except Tech as e:
                raise Tech([f'step {st}: {r_}' for r_ in e.reasons])
            except Undefined as e:
                raise Undefined(f'step {st}: {e}')
            tc = time.time()
            rows.append(dict(step=int(st), rev=float((st - fp['t0_step']) / pl['steps_per_rev']), file=os.path.basename(pth), sha256=sha,
                             **q, seconds=dict(read=tb - ta, compute=tc - tb)))
            res['provenance']['dumps'].append([int(st), os.path.basename(pth), sha])
            if progress and (k_ % 10 == 0 or k_ == len(todo) - 1):
                print(f'   … {res["run"]} 프레임 {k_ + 1}/{len(todo)} (step {st}) · 누적 {time.time() - t_all:.1f} s', file=sys.stderr)
        res['provenance']['dumps_digest'] = frame_digest(res['provenance']['dumps'])
        res['t0'] = rows[0]
        if fp['mode'] == 'rot2':
            res['bin'] = bin_summary(rows[1:], fp['bin_steps'])
        else:
            res['bin'] = dict(status='NOT_APPLICABLE', bin=REG_BIN,
                              reason='계획 회전 0 (E0 = 정지 · 균일 삽입 기준) — bin 1 이 없다 · 자기 t₀ 만 (§12-4 "E0 에도 같은 식으로")')
        res['status'] = 'OK'
    except Tech as e:
        res.update(status='TECH', reasons=e.reasons, t0=None, bin=None)
    except Undefined as e:
        res.update(status='UNDEFINED', reasons=[str(e)], t0=None, bin=None)
    if res['status'] != 'OK':                                    # 값이 없으면 부분 덤프 목록도 남기지 않는다
        res['provenance'].update(dumps=[], dumps_digest=None)
    res['timing'] = dict(total_s=time.time() - t_all, plan_validate_s=t_plan, frames_read=len(rows),
                         read_s=float(sum(r_['seconds']['read'] for r_ in rows)), compute_s=float(sum(r_['seconds']['compute'] for r_ in rows)))
    return res


def _fmt(v, f='.4f'):
    return '—' if v is None else format(v, f)


def report(res):
    print(f"{res['run']} · {res['status']}" + (f" · {res['mode']}" if res.get('mode') else ''))
    if res['status'] != 'OK':
        for r_ in res['reasons']:
            print(f'   ⚠ {r_}')
        return
    t0 = res['t0']
    print(f"   t₀ step {t0['step']} · SE {t0['n']['SE']} · AM_P {t0['n']['AM_P']} · AM_S {t0['n']['AM_S']}")

    def lines(tag, g):
        print(f"   (s1) {tag}  군집 SE 분율 {_fmt(g('se_frac_in_clusters'))} · 가장 큰 성분 {_fmt(g('largest_frac'))} · "
              f"수평균 크기 {_fmt(g('mean_size_number'), '.3f')}")
        print(f"   (s2) {tag}  아무 AM 에 붙은 SE {_fmt(g('se_attached_any_frac'))} · AM_P {_fmt(g('se_attached_frac_AM_P'))} · "
              f"AM_S {_fmt(g('se_attached_frac_AM_S'))} · AM 당 SE  AM_P {_fmt(g('se_per_am_AM_P'), '.2f')} · AM_S {_fmt(g('se_per_am_AM_S'), '.2f')}")
    lines('t₀   ', lambda k: t0['s1_se_clusters'][k] if k in t0['s1_se_clusters'] else t0['s2_am_se_attach'][k])
    print(f"        t₀ 성분 수 히스토그램 {t0['s1_se_clusters']['hist_components']} · 접촉 쌍 {t0['pairs']}")
    b = res['bin']
    if b.get('status') == 'OK':
        lines(f'bin {b["bin"]}', lambda k: b['mean'][k])
        print(f"        bin {b['bin']} = {b['n']} 프레임 (step {b['steps'][0]}–{b['steps'][-1]}) 평균 · SD: "
              + ' · '.join(f'{k} {_fmt(b["sd"][k])}' for k in S1_KEYS + S2_KEYS))
    else:
        print(f"   bin {b['bin']}: {b['status']} — {b.get('reason', '')}")
    rz = t0['resolution']
    print(f"   해상도 (보고 전용 · t₀): 좌표 유효숫자 {rz['sigfigs_xyz']} · 반폭 최대 {rz['half_width_max_m']:.3g} m · "
          f"SE–SE 접촉 확실/등록/가능 {rz['pairs_lo']['SE-SE']}/{t0['pairs']['SE-SE']}/{rz['pairs_hi']['SE-SE']} · "
          f"군집 SE 분율 [{_fmt(rz['lo']['se_frac_in_clusters'])}, {_fmt(rz['hi']['se_frac_in_clusters'])}]")
    tm = res['timing']
    print(f"   시간 {tm['total_s']:.1f} s (계획 · 검사 {tm['plan_validate_s']:.1f} · 읽기 {tm['read_s']:.1f} · 계산 {tm['compute_s']:.1f} · "
          f"프레임 {tm['frames_read']})")


def _json_clean(o):
    """numpy → 파이썬 · 비유한 float 은 ValueError (엄격 JSON — NaN 을 값처럼 내지 않는다)."""
    if isinstance(o, dict):
        return {str(k): _json_clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_json_clean(v) for v in o]
    if isinstance(o, (np.bool_, bool)):
        return bool(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating, float)):
        if not math.isfinite(float(o)):
            raise ValueError(f'비유한 값 {o!r} — 엄격 JSON 에 넣지 않는다')
        return float(o)
    return o


def dumps_strict(obj):
    return json.dumps(_json_clean(obj), ensure_ascii=False, indent=1, allow_nan=False)


# ═════════════════════════════ 합성 고정구 (셀프테스트 · 벤치) ═════════════════════════════
_R_PLAN = {'AM_P': 0.0006813, 'AM_S': 0.0003028, 'SE': 7.57e-05}     # 캠페인 덱의 radius constant (계획 지름 / 2)


def _synthetic_deck(revs, tpl_se='7.57e-05'):
    """판독기 deck_plan 이 읽는 최소 덱 — 정착 125 ×2 · 덤프 50 · 바퀴 160 step (주기 0.16 s / dt 1e-3) ⇒ t₀ 250 ·
    2 바퀴면 bin 0 = 250 · 300 · 350 · 400 / bin 1 = 450 · 500 · 550 (실제 캠페인처럼 바퀴가 덤프 간격의 배수가 아니다)."""
    return ('# 합성 덱 (mixer_contact_reader 셀프테스트)\n'
            'fix pt1 all particletemplate/sphere 10487 atom_type 1 density constant 4800 radius constant 0.0006813\n'
            'fix pt2 all particletemplate/sphere 11887 atom_type 2 density constant 4800 radius constant 0.0003028\n'
            f'fix pt3 all particletemplate/sphere 13901 atom_type 3 density constant 2000 radius constant {tpl_se}\n'
            'timestep 1e-3\nrun 1\n'
            'dump dmp all custom 50 post/mix_*.liggghts id type x y z vx vy vz fx fy fz radius\n'
            'run 125\nrun 125\n'
            'fix mvD all move/mesh mesh Drum rotate origin 0 0 0 axis 1. 0. 0. period 0.16\n'
            f'run {320 if revs == 2 else (480 if revs == 3 else 0)}\n')


def _write_frame(path, atoms, step, fmt='g'):
    """[id, type, x, y, z, r] 목록 → LIGGGHTS 평문 덤프 (캠페인 덱의 열 순서 · 좌표 `%g` = LIGGGHTS 기본)."""
    with open(path, 'w') as f:
        f.write(f'ITEM: TIMESTEP\n{step}\nITEM: NUMBER OF ATOMS\n{len(atoms)}\nITEM: BOX BOUNDS ff ff ff\n'
                '-0.015 0.015\n-0.015 0.015\n-0.015 0.015\nITEM: ATOMS id type x y z vx vy vz fx fy fz radius\n')
        f.write(''.join(f'{int(i)} {int(t)} {x:{fmt}} {y:{fmt}} {z:{fmt}} 0 0 0 0 0 0 {r:g}\n' for i, t, x, y, z, r in atoms))


def _make_synthetic_run(root, name, frames_cfg, revs=2, meta_patch=None, tpl_se='7.57e-05', n_planned=None):
    """합성 셀 (in.mixer · deck_meta.json · post/) — frames_cfg = {step: [[id, type, x, y, z, r], …]} (셀프테스트 · 벤치 전용)."""
    d = os.path.join(root, name)
    os.makedirs(os.path.join(d, 'post'))
    deck = _synthetic_deck(revs, tpl_se)
    with open(os.path.join(d, 'in.mixer'), 'w') as f:
        f.write(deck)
    n0 = len(next(iter(frames_cfg.values())))
    meta = dict(schema=DECK_META_SCHEMA, deck_sha256=hashlib.sha256(deck.encode()).hexdigest(),
                types={'1': 'AM_P', '2': 'AM_S', '3': 'SE', '4': 'WALL'}, radius_m=dict(_R_PLAN),
                n_atoms_planned=n0 if n_planned is None else n_planned, revolutions=revs,
                steps=dict(t0_planned=250, dump_every=50))
    if meta_patch:
        meta_patch(meta)
    with open(os.path.join(d, 'deck_meta.json'), 'w') as f:
        json.dump(meta, f)
    for st, atoms in frames_cfg.items():
        _write_frame(os.path.join(d, 'post', f'mix_{st}.liggghts'), atoms, st)
    return d


# ───────────────────────────── selftest ─────────────────────────────
def _selftest():                                            # noqa: C901
    import ast
    import builtins
    import tempfile
    ok, fail = 0, []

    def chk(name, fn):
        nonlocal ok
        try:
            cond = bool(fn())
        except Exception as e:                              # noqa: BLE001 — 스텁 · 결함이 예외로 터져도 FAIL 로 센다
            print(f'        ({type(e).__name__}: {str(e)[:160]})')
            cond = False
        if cond:
            ok += 1
        else:
            fail.append(name)
        print(('  PASS  ' if cond else '  FAIL  ') + name)

    R = _R_PLAN
    RS = 2 * R['SE']                                               # SE–SE Σr = 1.514e-4
    A = 0.9 * RS                                                   # 접촉 간격 (겹침 0.1·Σr = 1.5e-5 m ≫ 덤프 반올림)
    XS1 = R['AM_P'] + R['AM_S'] + 1.4e-4                           # AM_S#1 중심 x (두 AM 표면 사이 틈 1.4e-4 < SE 지름)

    def base_atoms():
        """알려진 답의 배치 C0 — [id, type, x, y, z, r] (무리끼리 ≥ 2 mm 떨어져 서로 안 닿는다)."""
        L = [[1, 3, 0.0, 0.002, 0.004]]                                          # G1 홑 SE
        L += [[2 + k, 3, k * A, 0.004, 0.004] for k in range(3)]                 # G2 사슬 3 (끝끼리 2A > Σr)
        L += [[5 + k, 3, k * A, 0.006, 0.004] for k in range(2)]                 # G3a 덩어리 2
        L += [[7 + k, 3, k * A, 0.008, 0.004] for k in range(4)]                 # G3b 덩어리 4
        L += [[11, 3, 0.0, 0.010, 0.004], [12, 3, 0.0001514, 0.010, 0.004]]      # G4 정확히 맞닿음 (d == Σr)
        L += [[101, 1, 0.0, -0.004, 0.004], [102, 2, XS1, -0.004, 0.004],         # AM_P#1 · AM_S#1
              [103, 1, 0.0, -0.008, 0.004]]                                       # AM_P#2 (붙은 SE 없음)
        L += [[13, 3, R['AM_P'] + 7e-5, -0.004, 0.004],                          # SE_y — AM_P#1 · AM_S#1 둘 다
              [14, 3, -(R['AM_P'] + 7e-5), -0.004, 0.004],                       # SE_x — AM_P#1 만
              [15, 3, XS1 + R['AM_S'] + 7e-5, -0.004, 0.004],                    # SE_z — AM_S#1 만
              [16, 3, XS1, -0.004, 0.004 + R['AM_S'] + 7e-5]]                    # SE_w — AM_S#1 만
        rr = {1: R['AM_P'], 2: R['AM_S'], 3: R['SE']}
        return [a + [rr[a[1]]] for a in L]

    def c1_atoms():
        """C1 = C0 에서 G2 의 b–c 고리를 끊고 (id 4 를 1e-4 밀기) SE_z 를 AM_S 에서 떼었다 (2e-4)."""
        L = base_atoms()
        for a in L:
            if a[0] == 4:
                a[2] += 1e-4
            if a[0] == 15:
                a[2] += 2e-4
        return L

    ROT = (250, 300, 350, 400, 450, 500, 550)

    def std_frames():
        return {s: (c1_atoms() if s == 500 else base_atoms()) for s in ROT}

    #  손 계산 답 (16 SE · AM_P 2 · AM_S 1)
    EXP0 = dict(se_frac_in_clusters=9 / 16, largest_frac=4 / 16, mean_size_number=16 / 10,
                hist={'1': 7, '2': 1, '3-9': 2, '10-99': 0, '>=100': 0},
                se_attached_any_frac=4 / 16, se_attached_frac_AM_P=2 / 16, se_attached_frac_AM_S=3 / 16,
                se_per_am_AM_P=1.0, se_per_am_AM_S=3.0, n_se_se=6, n_P=2, n_S=3)
    EXP1 = dict(se_frac_in_clusters=8 / 16, largest_frac=4 / 16, mean_size_number=16 / 11,
                hist={'1': 8, '2': 2, '3-9': 1, '10-99': 0, '>=100': 0},
                se_attached_any_frac=3 / 16, se_attached_frac_AM_P=2 / 16, se_attached_frac_AM_S=2 / 16,
                se_per_am_AM_P=1.0, se_per_am_AM_S=2.0, n_se_se=5, n_P=2, n_S=2)

    def close(a, b, tol=1e-12):
        return a is not None and b is not None and abs(float(a) - float(b)) <= tol

    def vals_ok(fr, E):
        s1, s2 = fr['s1_se_clusters'], fr['s2_am_se_attach']
        return (all(close(s1[k], E[k]) for k in S1_KEYS) and s1['hist_components'] == E['hist']
                and all(close(s2[k], E[k]) for k in S2_KEYS)
                and fr['pairs'] == {'SE-SE': E['n_se_se'], 'AM_P-SE': E['n_P'], 'AM_S-SE': E['n_S']})

    def no_values(res):
        return res.get('t0') is None and res.get('bin') is None

    def keys_rec(o):
        if isinstance(o, dict):
            for k, v in o.items():
                yield k
                yield from keys_rec(v)
        elif isinstance(o, list):
            for v in o:
                yield from keys_rec(v)

    with tempfile.TemporaryDirectory() as td:
        def mk(name, revs=2, frames_cfg=None, **kw):
            fc = frames_cfg if frames_cfg is not None else (std_frames() if revs else {200: base_atoms(), 250: base_atoms()})
            return _make_synthetic_run(td, name, revs=revs, frames_cfg=fc, **kw)

        def tech_dir(d_, why):
            r_ = analyse_run(d_)
            return r_['status'] == 'TECH' and no_values(r_) and any(why in s_ for s_ in r_['reasons'])

        def tech_case(name, why, **kw):
            return tech_dir(mk(name, **kw), why)

        #  ⓪ 고정구 자체의 판별력 — 정확히 맞닿은 쌍이 부동소수로 **정확히** Σr 이고 (엄격 · 비엄격이 갈린다) 접촉 간격이 Σr 안이다
        chk('⓪ 고정구: 7.57e-05 + 7.57e-05 == 1.514e-4 · 제곱도 같다 (비엄격 ≤ 면 G4 가 접촉으로 들어온다) · 0.9·Σr < Σr < 2·0.9·Σr',
            lambda: (R['SE'] + R['SE'] == float('0.0001514') and (RS * RS) == float('0.0001514') ** 2 and A < RS < 2 * A))

        run = mk('LU212_ref_r2_s1')
        opened = []
        _open = builtins.open

        def _spy(p, *a, **k):
            if isinstance(p, str) and os.sep + 'post' + os.sep in p:
                opened.append(os.path.basename(p))
            return _open(p, *a, **k)
        builtins.open = _spy
        try:
            res = analyse_run(run)
        finally:
            builtins.open = _open
        t0r = (res or {}).get('t0') or {}
        b = (res or {}).get('bin') or {}
        fr_ = b.get('frames') or []
        chk('① 정상 2 바퀴 런 → OK · mode rot2 · t₀ step 250 · bin 1 = [450, 500, 550] (판독기 bin_window_files 격자)',
            lambda: res['status'] == 'OK' and res['mode'] == 'rot2' and t0r['step'] == 250 and b['steps'] == [450, 500, 550])
        chk('② (s1) 홑 SE = 크기 1 성분 · 끝끼리 안 닿는 사슬 3 = 한 성분 — t₀ 성분 수 10 · 크기 1 성분 7',
            lambda: t0r['s1_se_clusters']['n_components'] == 10 and t0r['s1_se_clusters']['hist_components']['1'] == 7
            and t0r['s1_se_clusters']['hist_components']['3-9'] == 2)
        chk('③ (s1) 떨어진 두 덩어리 (2 · 4) = 두 성분 — 군집 SE 분율 9/16 · 가장 큰 성분 4/16 · 수평균 크기 16/10 · 히스토그램',
            lambda: vals_ok(t0r, EXP0))
        chk('④ ★ 정확히 맞닿은 쌍 (d == r_i + r_j) 은 접촉이 아니다 (엄격 부등식) — G4 = 홑 둘 · SE–SE 접촉 6',
            lambda: t0r['pairs']['SE-SE'] == 6 and t0r['s1_se_clusters']['hist_components']['2'] == 1)
        chk('⑤ (s2) 두 AM 에 닿은 SE 는 분율에서 한 번 (아무 AM 4/16) · AM 당 수에서 두 번 (쌍 AM_P 2 + AM_S 3)',
            lambda: close(t0r['s2_am_se_attach']['se_attached_any_frac'], 4 / 16) and t0r['pairs']['AM_P-SE'] + t0r['pairs']['AM_S-SE'] == 5)
        chk('⑥ (s2) AM_P · AM_S 따로 — AM_P 분율 2/16 · AM 당 1.0 / AM_S 3/16 · 3.0',
            lambda: close(t0r['s2_am_se_attach']['se_attached_frac_AM_P'], 2 / 16) and close(t0r['s2_am_se_attach']['se_per_am_AM_P'], 1.0)
            and close(t0r['s2_am_se_attach']['se_attached_frac_AM_S'], 3 / 16) and close(t0r['s2_am_se_attach']['se_per_am_AM_S'], 3.0))
        chk('⑦ bin 1 프레임별 값 (C0 · C1 · C0) · 평균 · SD (ddof 1) = 손 계산',
            lambda: (len(fr_) == 3 and vals_ok(fr_[0], EXP0) and vals_ok(fr_[1], EXP1) and vals_ok(fr_[2], EXP0)
                     and b['n'] == 3
                     and all(close(b['mean'][k], np.mean([EXP0[k], EXP1[k], EXP0[k]])) for k in S1_KEYS + S2_KEYS)
                     and all(close(b['sd'][k], np.std([EXP0[k], EXP1[k], EXP0[k]], ddof=1)) for k in S1_KEYS + S2_KEYS)
                     and close(b['mean']['hist.1'], (7 + 8 + 7) / 3)))

        r8 = analyse_run(mk('E0_ref_s1', revs=0))
        chk('⑧ E0 (회전 0) = 자기 t₀ (250) 만 · bin 1 = NOT_APPLICABLE (TECH 아님) · 값 = C0',
            lambda: r8['status'] == 'OK' and r8['mode'] == 't0_only' and r8['t0']['step'] == 250
            and r8['bin']['status'] == 'NOT_APPLICABLE' and vals_ok(r8['t0'], EXP0))

        def _no_se(m):
            m['types'] = {'1': 'AM_P', '2': 'AM_S', '3': 'AM_S', '4': 'WALL'}
        chk('⑨ type → 상 대응 불일치 (deck_meta 에 SE 없음 · AM_S 둘) → TECH · 값 없음',
            lambda: tech_case('map_bad', 'SE 의 type', meta_patch=_no_se))
        fc = {s: base_atoms() + [[999, 4, 0.0, 0.0, 0.0, R['SE']]] for s in ROT}
        chk('⑨b 덤프에 계획 밖 type (4 = 벽 · 모든 프레임) → TECH', lambda: tech_case('type4', '계획 밖 type', frames_cfg=fc))
        r9c = mk('meta_gone')
        os.remove(os.path.join(r9c, 'deck_meta.json'))
        chk('⑨c deck_meta.json 없음 → TECH (type 을 추정으로 메우지 않는다)', lambda: tech_dir(r9c, 'deck_meta.json 없음'))

        def _bad_sha(m):
            m['deck_sha256'] = '0' * 64
        chk('⑨d deck_meta.deck_sha256 ≠ in.mixer → TECH (이 런의 메타가 아니다)',
            lambda: tech_case('meta_sha', 'deck_sha256', meta_patch=_bad_sha))

        fc = std_frames()
        fc[500] = [a[:5] + [7.6e-05 if a[1] == 3 else a[5]] for a in c1_atoms()]
        chk('⑩ 반경 불일치 — bin 프레임 하나의 SE 반경 7.6e-05 ≠ 계획 7.57e-05 → TECH',
            lambda: tech_case('rad_bad', '덤프 반경 ≠ 계획', frames_cfg=fc))
        chk('⑩b in.mixer 템플릿 반경 (7.6e-05) ≠ deck_meta radius_m → TECH', lambda: tech_case('tpl_bad', '템플릿', tpl_se='7.6e-05'))

        r11 = mk('miss500')
        os.remove(os.path.join(r11, 'post', 'mix_500.liggghts'))
        r11b = mk('miss_t0')
        os.remove(os.path.join(r11b, 'post', 'mix_250.liggghts'))
        chk('⑪ 계획 프레임 결손 — bin 1 의 500 없음 → TECH · 계획 t₀ 250 없음 → TECH (앞 프레임으로 대신하지 않는다)',
            lambda: tech_dir(r11, '결손') and tech_dir(r11b, '계획 t₀'))

        fc = std_frames()
        fc[450] = [[2 if a[0] == 3 else a[0]] + a[1:] for a in base_atoms()]
        chk('⑫ 원자 id 중복 (bin 프레임) → TECH', lambda: tech_case('dup_id', 'id 중복', frames_cfg=fc))
        r12b = mk('dup_step')
        _write_frame(os.path.join(r12b, 'post', 'copy_500.txt'), c1_atoms(), 500)
        chk('⑫b 같은 step (500) 의 덤프 둘 → TECH (어느 것이 참인지 모른다)', lambda: tech_dir(r12b, '둘 이상'))

        fc = std_frames()
        fc[550] = [a[:2] + [float('nan')] + a[3:] if a[0] == 7 else a for a in base_atoms()]
        chk('⑬ NaN 좌표 (bin 프레임) → TECH', lambda: tech_case('nan_x', '비유한', frames_cfg=fc))

        fc = std_frames()
        fc[500] = [a for a in c1_atoms() if a[0] != 16]
        chk('⑭ 원자 집합이 t₀ 과 다르다 (bin 프레임에서 SE 하나 사라짐) → TECH', lambda: tech_case('lost', '원자 집합', frames_cfg=fc))
        chk('⑭b t₀ 원자 수 (21) ≠ deck_meta n_atoms_planned (100000) → TECH',
            lambda: tech_case('n_plan', 'n_atoms_planned', n_planned=100000))

        am_only = [a for a in base_atoms() if a[1] != 3]
        r15 = analyse_run(mk('no_se', frames_cfg={s: am_only for s in ROT}))
        chk('⑮ SE 0 개 → UNDEFINED (정의 불가 · 예외 없음) · 값 None — 0 을 값처럼 내지 않는다',
            lambda: r15['status'] == 'UNDEFINED' and no_values(r15) and bool(r15['reasons']) and dumps_strict(r15))

        chk('⑯ 계획 바퀴 수가 0 · 2 가 아니면 (3 바퀴 덱) → TECH (등록 = 2 바퀴 계획의 bin 1)',
            lambda: tech_case('three_revs', '바퀴', revs=3, frames_cfg={s: base_atoms() for s in range(250, 731, 50)}))

        def _imports():
            tree = ast.parse(open(os.path.abspath(__file__), encoding='utf-8').read())
            got = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module == 'measure_mixing_index':
                    got |= {a.name for a in node.names}
                if isinstance(node, ast.Import) and any(a.name == 'measure_mixing_index' for a in node.names):
                    got.add('*')                                                # 모듈 통째 — 무엇이든 부를 수 있다 → 거부
            return got
        chk('⑰ M 없음 — 판독기에서 가져오는 이름 = 프레임 선택뿐 (deck_plan · _t0_exact · bin_window_files ⊆ 가져온 것 ⊆ 허용) · '
            '결과 키에 M · S0 · SR · s2 (칸 분산) 없음',
            lambda: (FRAME_TOOL_REQUIRED <= _imports() <= FRAME_TOOL_NAMES
                     and not (set(keys_rec(res)) & M_KEYS) and not (set(keys_rec(r8)) & M_KEYS)))
        chk('⑱ 연 덤프 = 계획 t₀ + bin 1 정확히 — bin 0 (300 · 350 · 400) 은 열지 않는다',
            lambda: set(opened) == {'mix_250.liggghts', 'mix_450.liggghts', 'mix_500.liggghts', 'mix_550.liggghts'})

        rz = t0r.get('resolution') or {}
        chk('⑲ 해상도 (보고 전용) — 확실 ⊆ 등록 ⊆ 가능 · 정확히 맞닿은 G4 는 가능에만 (SE–SE 6 · 6 · 7) · 가능 쪽 군집 분율 11/16 · '
            '확실 쪽 = 등록 값',
            lambda: (rz['pairs_lo']['SE-SE'] == 6 and rz['pairs_hi']['SE-SE'] == 7
                     and close(rz['hi']['se_frac_in_clusters'], 11 / 16) and close(rz['lo']['se_frac_in_clusters'], 9 / 16)
                     and all(rz['lo'][k] <= t0r['s1_se_clusters'][k] + 1e-15 <= rz['hi'][k] + 2e-15 for k in S1_KEYS)
                     and all(rz['lo'][k] <= t0r['s2_am_se_attach'][k] + 1e-15 <= rz['hi'][k] + 2e-15 for k in S2_KEYS)))
        v6 = np.array([0.0304637, 0.005, -0.0123456, 3.34479e-06, 0.0])
        v9 = np.array([0.0304637123, 0.00512345678, -0.0123456789])
        chk('⑲b 유효숫자 = max(관측, 6) — %g 값 → 6 · %.9g 값 → 9 · 반폭(0.005, 6) = 5e-9 · 반폭(0.0304637, 6) = 5e-8 · 0 → 0 '
            '(lhs_contact_audit v2 규칙 · SELF-63)',
            lambda: (sigfigs_effective(v6) == 6 and sigfigs_effective(v9) == 9
                     and np.allclose(half_width(v6, 6), [5e-8, 5e-9, 5e-8, 5e-12, 0.0], rtol=1e-12, atol=0)))
        chk('⑳ 엄격 JSON (allow_nan=False) · 출처 — 판독기 sha256 · 덱 · 메타 sha256 · 덤프 4 장 (step · 이름 · sha256) · 묶음 sha256',
            lambda: (json.loads(dumps_strict(res))['provenance']['reader_sha256'] == _sha_file(os.path.abspath(__file__))
                     and res['provenance']['deck_sha256'] == _sha_file(os.path.join(run, 'in.mixer'))
                     and res['provenance']['deck_meta_sha256'] == _sha_file(os.path.join(run, 'deck_meta.json'))
                     and [d_[0] for d_ in res['provenance']['dumps']] == [250, 450, 500, 550]
                     and res['provenance']['dumps'][0][2] == _sha_file(os.path.join(run, 'post', 'mix_250.liggghts'))
                     and len(res['provenance']['dumps_digest']) == 64))
        rt = analyse_run(r11)
        chk('⑳b TECH 결과도 엄격 JSON · 사유 문자열 · 값 없음 (t₀ · bin None)',
            lambda: rt['status'] == 'TECH' and no_values(json.loads(dumps_strict(rt))) and all(isinstance(s, str) for s in rt['reasons']))

        #  ㉑ 검사 · 읽기 사이에 덤프가 바뀌면 (아직 쓰는 중인 런) 섞인 값을 내지 않는다 — read_dump 직전에 파일 끝에 한 줄을 붙인다
        r21 = mk('changing')
        g_ = globals()
        _rd = g_['read_dump']

        def _rd_touch(path):
            if path.endswith('mix_500.liggghts'):
                with _open(path, 'a') as fh:
                    fh.write('\n')
            return _rd(path)
        g_['read_dump'] = _rd_touch
        try:
            ok21 = tech_dir(r21, '바뀌었다')
        finally:
            g_['read_dump'] = _rd
        chk('㉑ 형식 검사 뒤 · 읽기 사이에 덤프가 바뀌면 → TECH (sha256 앞뒤 대조 · 섞인 값 없음)', lambda: ok21)

    print(f'\nmixer_contact_reader selftest: {ok}/{ok + len(fail)} PASS' + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


def bench(n, seed=7):
    """합성 N 입자 한 프레임 (E0 형 · t₀ 만) 의 판독 시간 — 캠페인 비 (AM_P 176 · AM_S 859 / 10 만) · SE 는 간격 0.98·2r 격자
    (이웃마다 겹침 3 µm = 실제 침대의 접촉 수 규모) · 좌표 `%g`.  판정 아님 (기록용)."""
    import tempfile
    rng = np.random.default_rng(seed)
    nP, nS = max(1, round(n * 176 / 100000)), max(1, round(n * 859 / 100000))
    nE = n - nP - nS
    a = 0.98 * 2 * _R_PLAN['SE']
    m = int(np.ceil(nE ** (1.0 / 3.0)))
    g = np.stack(np.meshgrid(np.arange(m), np.arange(m), np.arange(m), indexing='ij'), -1).reshape(-1, 3)[:nE]
    Pse = (g - m / 2.0) * a + np.array([0.0, 0.0, -0.006]) + rng.normal(0.0, 2e-8, (nE, 3))
    Pam = rng.uniform(Pse.min(0), Pse.max(0), (nP + nS, 3))
    atoms = [[k + 1, 1 if k < nP else 2, *Pam[k], _R_PLAN['AM_P'] if k < nP else _R_PLAN['AM_S']] for k in range(nP + nS)]
    atoms += [[nP + nS + k + 1, 3, *Pse[k], _R_PLAN['SE']] for k in range(nE)]
    with tempfile.TemporaryDirectory() as td:
        tw = time.time()
        d = _make_synthetic_run(td, 'bench_E0', revs=0, frames_cfg={250: atoms})
        tw = time.time() - tw
        res = analyse_run(d)
    if res['status'] != 'OK':
        print(f'bench: {res["status"]} {res["reasons"]}')
        return res
    t0 = res['t0']
    tm = res['timing']
    per = tm['plan_validate_s'] + tm['read_s'] + tm['compute_s']
    print(f'bench N={n:,} (AM_P {nP} · AM_S {nS} · SE {nE}) · 덤프 쓰기 {tw:.2f} s (판독 밖)')
    print(f'   판독 전체 {tm["total_s"]:.2f} s = 계획 · t₀ 검사 (판독기 _t0_exact) {tm["plan_validate_s"]:.2f} · sha256 앞뒤 + 형식 검사 + read_dump {tm["read_s"]:.2f} · '
          f'계산 (KD 트리 · 판정 셋 · 성분 셋) {tm["compute_s"]:.2f}')
    print(f'   접촉 쌍 등록 {t0["pairs"]} · SE–SE 확실/가능 {t0["resolution"]["pairs_lo"]["SE-SE"]}/{t0["resolution"]["pairs_hi"]["SE-SE"]} · '
          f'군집 SE 분율 {t0["s1_se_clusters"]["se_frac_in_clusters"]:.4f}')
    print(f'   2 바퀴 런 (t₀ + bin 1 100 프레임 = 101 장) 환산 ≈ {101 * per / 60:.1f} 분 (프레임당 {per:.2f} s)')
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description='믹서 보조 판독기 — SE–SE 접촉 군집 · AM–SE 부착 (사전등록 강성 축 §12-4 · M 계산 없음)')
    ap.add_argument('runs', nargs='*', help='런 디렉터리 (in.mixer · deck_meta.json · post/)')
    ap.add_argument('--json', help='결과 JSON 경로 (엄격 JSON · allow_nan=False)')
    ap.add_argument('--selftest', action='store_true', help='합성 덤프 고정구 셀프테스트')
    ap.add_argument('--bench', type=int, metavar='N', help='합성 N 입자 프레임 한 장의 읽기 · 계산 시간 (기록용 · 판정 아님)')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    if a.bench:
        res = bench(a.bench)
        return 0 if res.get('status') == 'OK' else 1
    if not a.runs:
        ap.error('런 디렉터리가 필요하다')
    out = []
    for d in a.runs:
        r_ = analyse_run(d, progress=True)
        report(r_)
        out.append(r_)
    if a.json:
        with open(a.json, 'w', encoding='utf-8') as f:
            f.write(dumps_strict(dict(schema=SCHEMA, registered=REGISTERED, argv=list(sys.argv), runs=out)))
        print(f'→ {a.json}')
    return 0 if all(r_['status'] == 'OK' for r_ in out) else 1


if __name__ == '__main__':
    raise SystemExit(main())
