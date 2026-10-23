#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② D — SV 반사실 대조의 **증거 꼴** (등록 R §5-6 SV 행 · Codex RCA-06 · 1저자 Q4 · 2026-10-21).

반사실 대조 = 같은 침대 · 같은 R_j 에서 SV 융합 면 (어느 면을 끊는지 = producer `carbon_junction.CjuncSolver.sv_counterfactual` 의 정의) 을
끊은 판을 한 번 더 풀어 단자 G 비 (`sv_counterfactual_ratio` = G_full/G_cut ≥ 1 · Rayleigh) 를 낸다.  문턱 (`SV_DEPENDENT`) = 사슬 계획
(`rint_r_chain` · 등록 R §5-6 · producer 는 비만 낸다 — 이 배선의 요청은 늘 `{'threshold': None}`).

이 모듈 = 그 원 기록의 **JSON 투영** (payload · 증거 `ca_ext.cjunc.evidence.solve.sv_counterfactual`) 과 **검증기** (`run_contract.ca_ext_record_ok`
가 접합 블록 검증 뒤 부른다).  접합 모듈 (A 소관) 밖에 둔다 — 그리고 **끊는 면의 정의에 기대지 않는다** (사전 리뷰 PRE-impl-04 · 코디네이터
10-21 Q-D): 읽는 칸 = 비 · 상태 · 표지 (· 종류는 'counterfactual…' 이기만 하면 아무 정의 · 정의별 수 칸 `n_*` 은 이름 그대로 옮긴다).
· 비 +∞ (위상 — 끊은 그래프에 관통 성분 없음) = JSON 비 null + `ratio_limit` 'inf' (극한 R_j 의 `R_j_ohm` null + `rj_limit` 'inf' 와 한 꼴)
· 비를 싣는 상태 = `RATIO_STATUSES` 둘뿐 — 그 밖의 상태 (미수렴 · 수치 실패 · 주 해 미수렴 · 앞으로 producer 가 더할 이름) = 비 없음 →
  사슬은 그 모서리를 `SV_UNCHECKED` 로 센다 (fail-closed · 모르는 상태를 '의존 없음' 으로 읽지 않는다)
★ 10-22 (사전 리뷰 2 회차 PRE2-impl-01 · 1저자 Q1 (다) · 등록 R §5-6 SV 행 개정) 괄호 칸 — 못 가른 덩어리 수 (`n_unsplit_bridging_components`) ·
  규칙 (`bracket_rule`) · 위 끝 상태 · 비 (`status_hi` · `sv_counterfactual_ratio_hi` · +∞ = null + `ratio_limit_hi` 'inf') · 위 끝 풀이 기록
  (`upper` · 아래 끝과 같은 꼴 · 덩어리 0 = None) → 검증기 (꼴 · 덩어리 수 ↔ 위 끝 기록 · 덩어리 0 = 위 = 아래 · 위 끝 칸 = 위 끝 풀이 기록) ·
  사슬 꼴 (아래 끝 · 위 끝 · 덩어리 수 — 위 끝 칸이 없는 옛 기록 = 위 끝 못 읽음 · fail-closed).  비 값의 대조 (G 비 · 아래 ≤ 위) = 다른 묶음
  → ★ PF2 E (10-22 · PRE2-impl-02) `_values_problem` — 비 = G_full/G_cut · 비 ≥ (1 − τ)/(1 + τ) · 증서 ok · computed ↔ G_cut 유한 양수 ·
  no_through ↔ G_cut 0 · 위 끝도 같은 규칙 · 괄호 아래 ≤ 위 (같은 증서 폭 여유) · 사슬 꼴은 유한 양수 · +∞ 만 읽는다.
★★ 10-23 (Codex 재검토 RCA2-01 · 04 · 1저자 Q1 (가) · author 10-23 ratified Q1-Q8) **증서 구간 판정** — 옛 판정은 풀이가 낸 비 하나 (nominal)
  를 문턱과 비교했다 (판정문 반례: nominal 10.291249475344962 < 문턱 10.291251705345072 인데 증서가 보장하는 참 비 구간 전체가 문턱 위).
  · 투영이 주 해 (`conv_cert_full`) · 끝마다 (`conv_cert`) 증서의 목표량 구간 (`target_lo` · `target_hi`) · 게시 판 전류 (`I_bot`) · 결합 칸을
    버리지 않는다 (`_cert_proj`) · 기록 지위 (`standing` — 증서 구간 = 증서를 켠 런 · 진단 = 증서 없는 런) · 판정 근거 칸
    `ratio_cert_interval` = [아래비, 위비] (`cert_interval` — 아래비 = Gfull_lo / Gcut_lower_hi (내림) · 위비 = Gfull_hi / Gcut_upper_lo (올림) ·
    정확 분수 · +∞ = 그 끝의 영값 위상 증서가 증명한 0 분모만 · 못 정하면 None · JSON 의 +∞ = 'inf').
  · 사슬 꼴 (`chain_view`) 이 같은 함수로 다시 센다 (`ratio_cert_lo` · `ratio_cert_hi` · nominal 비 = 기록만 · 판정에 쓰지 않는다).
  · 기록 계약 (`sv_cf_problem` — 실제 소비자 `run_contract.ca_ext_record_ok`): 증서 구간 기록의 비를 싣는 끝마다 현 증서 필수 (판 · 상태 ·
    ⓐ–ⓓ · 목표량 판 · 봉인) · 증서 ↔ 그 끝의 G (게시 판 전류 = G 정확히 · 목표량 구간을 같은 판정 함수 `step3_conv_cert.target_judge` 로
    다시 봄) · 분자 G_full = 주 해 증서 · 솔브 기록 `I_bot_code` · 결합 칸 = 주 해 증서 = 증거 `fp` (다른 회로 · 다른 런 증서 = 거부) ·
    괄호 규칙 = 등록된 값만 (`BRACKET_RULES`) · 수 칸 = 0 이상 정수 · int64 범위 · 제거 성분 수 = 못 가른 덩어리 수 · 제거 셀 수 ≥ 성분 수 ·
    실제 census (증거 `census`) 와 일관 (못 가른 ⊆ 다리 놓는 ⊆ 닿는 성분) · 진단 기록 = 증서 없음 (사슬은 R 판정 입력으로 받지 않는다 =
    SV_UNCHECKED) · 판정 근거 칸 = 기록의 증서에서 다시 센 값.
★ 10-23 (Codex 재검토 RCA2-06 F6 · author 10-23 ratified Q1-Q8) 위 끝 구조화 실패 `unsplit_census_mismatch` (census 의 못 가른 덩어리 수 ≠ 지문
  묶인 원장에서 다시 가른 수 · 위 끝을 풀지 않음 · fail-closed) = 끝-끝 보존 — 검증기가 그 꼴 (`_mismatch_problem`: 다시 가른 수 ≠ census 수 ·
  사유 · 풀이 칸 없음 · 위 끝 칸 = (상태, None, None)) 을 받는다 (옛 판 = 못 가른 덩어리 0 꼴을 '위 끝 기록' 으로 게시 거부 · 덩어리 > 0 꼴은
  꼴을 보지 않고 받음) → 사슬 = 위 끝 못 읽음 (SV_UNCHECKED · 사유에 상태 이름 · `rint_r_chain.sv_corner_label`).
numpy 없이 뜬다 (`numbers` · `fractions` · 원 기록의 numpy 수도 받는다 · 검증기의 증서 대조만 `step3_conv_cert` 를 그 자리에서 부른다)."""
import math
import numbers
import sys
from fractions import Fraction

#: 비를 싣는 상태 → 비의 꼴 (finite = 유한 양수 · inf = +∞ · JSON null + 'inf')
RATIO_STATUSES = {'computed': 'finite', 'no_through_without_sv': 'inf'}
#: 지금 producer 가 내는 상태 낱말 (기록 · 문서용 — 검증기는 이 목록 밖 상태도 '비 없음' 이면 받는다 · 정의 무관)
KNOWN_STATUSES = ('computed', 'no_through_without_sv', 'unconverged', 'nonpositive_cut_current', 'nonpositive_full_current',
                  'main_unconverged', 'cjunc_electrode_short', 'all_floating_dropped', 'no_through_component',
                  'unsplit_census_mismatch')       # ★ 10-23 (RCA2-06 F6) = `UNSPLIT_MISMATCH` (위 끝 구조화 실패 · 검증기 `_mismatch_problem`)
KIND_PREFIX = 'counterfactual'
FLAGS = (None, 'SV_DEPENDENT')
#: ★ PF2 E (10-22 · 사전 리뷰 2 회차 PRE2-impl-02 · 결정 없음) — 기록 안 수의 다시 대조.  τ = 수렴 증서 ⓓ 의 보장 상대 오차
#   (= `step3_conv_cert.CERT_TARGET_TOL` · |G − G*| ≤ τ·G · 시험 S8o 가 대조 · 이 모듈은 numpy 없이 뜬다)
CERT_TARGET_TOL = 1.0e-4
#: 비 = G_full/G_cut 다시 셈 허용 (상대 · float 나눗셈 반올림 수준)
RATIO_REL_TOL = 1e-12
#: 증서 폭 꼴 여유 (새 숫자 없음) — 두 풀이가 각각 |G − G*| ≤ τ·G 면 참 비 ≥ 1 (Rayleigh) ⟹ 기록 비 ≥ (1 − τ)/(1 + τ) · 같은 G_full 의 두 끝
#   (괄호 위 = 덩어리를 더 뺀 판 · 참 G_cut,hi ≤ G_cut,lo) ⟹ 기록 위 ≥ 아래 × (1 − τ)/(1 + τ)
RATIO_FLOOR = (1.0 - CERT_TARGET_TOL) / (1.0 + CERT_TARGET_TOL)
CERT_OK_STATUS = 'POSITIVE_SOLVED'    # = `step3_conv_cert.STATUS_POSITIVE` (비를 낸 풀이 = 관통 성분이 있는 양의 해)
CERT_ZERO_STATUS = 'VALID_ZERO_TOPOLOGY'   # = `step3_conv_cert.STATUS_ZERO` (+∞ 의 분모 0 = 위상이 증명한 꼴)
#: ★ 10-23 (Codex 재검토 RCA2-01 · 04 · 1저자 Q1 (가)) 기록 지위 (= `carbon_junction.SV_CF_STANDING_*` · 시험이 대조) — 증서 구간 = 주 해 · 끝마다
#   수렴 증서를 실은 기록 (증서를 켠 런) · 진단 = 증서 없는 런의 기록 (사슬은 R 판정 입력으로 받지 않는다 → SV_UNCHECKED)
STANDING_CERTIFIED = 'certified_interval'
STANDING_DIAGNOSTIC = 'diagnostic_uncertified'
STANDINGS = (STANDING_CERTIFIED, STANDING_DIAGNOSTIC)
#: +∞ 끝 영값 위상 증서의 그래프 이름표 (= `carbon_junction.SV_CF_ZERO_GRAPH` · 시험이 대조 — 끊은 반사실 그래프가 증명한 0 · 다른 그래프의 0 = 거부)
ZERO_GRAPH_SV_CF = 'cjunc_sv_counterfactual'
#: 등록된 괄호 규칙 (= `carbon_junction.CJUNC_SV_CF_BRACKET_RULE` · 시험이 대조 · 등록 R §5-6 SV 행 · 이 밖의 낱말 = 거부)
BRACKET_RULES = ('lower_keep_unsplit_upper_remove_unsplit_sdcp_cells_v1',)
#: 위 끝 구조화 실패 (= `carbon_junction.SV_CF_UNSPLIT_MISMATCH` · 다시 가른 수 ≠ census 수 = 그 상태의 정의 · 제거 수 대조 밖 · 꼴 = `_mismatch_problem`)
UNSPLIT_MISMATCH = 'unsplit_census_mismatch'
#: ★ 10-23 (RCA2-06 F6) 구조화 실패 끝의 풀이 칸 — 풀지 않은 끝 = 전부 없다 (생산자 `carbon_junction._sv_cf_upper_unsolved` 정의: 비 · 표지 (투영) ·
#   G_cut · 잔차 · CG · 증서 · backend 는 None · 제거 셀 · 끊은 간선 · 판 결합 · SV 면 수는 푼 끝만 싣는다)
MISMATCH_EMPTY_KEYS = ('sv_counterfactual_ratio', 'ratio_limit', 'G_cut_code', 'resid', 'cg_info', 'conv_cert', 'backend_last_solve',
                       'n_cells_removed', 'n_edges_cut', 'n_plate_couplings_cut', 'n_sv_faces_cut')
#: 수 칸의 의미 범위 (0 이상 · int64 — 10**400 같은 값 = 거부 · RCA2-04)
COUNT_MAX = 2 ** 63 - 1
#: 증서 투영 칸 (★ 10-23 — 목표량 구간 · 게시 판 전류 · 영값 위상 칸 · 결합 칸까지 · 옛 판 = 판 · 상태 · ok · ⓐ–ⓓ 만 → 다른 회로 증서를 못 가렸다)
CERT_PROJ_KEYS = ('version', 'status', 'ok', 'pass_a', 'pass_b', 'pass_c', 'pass_d', 'I_bot', 'target_lo', 'target_hi',
                  'target_version', 'target_fp', 'target_tol', 'zero_source', 'zero_graph', 'reason', 'n_through_dof', 'sigma',
                  'bind_version', 'fp_sid', 'fp_sig', 'fp_face_plan', 'fp_cjunc_registry', 'fp_cjunc_rows')
_CERT_NUM_KEYS = frozenset(('I_bot', 'target_lo', 'target_hi', 'target_tol', 'n_through_dof', 'sigma'))
#: 증서 결합 칸 (= `step3_conv_cert.BIND_KEYS` + 판 · 끝마다 증서 = 주 해 증서와 같은 런 입력)
BIND_FIELDS = ('bind_version', 'fp_sid', 'fp_sig', 'fp_face_plan', 'fp_cjunc_registry', 'fp_cjunc_rows')
#: 실제 census 칸 (증거 `census` · 생산자 `carbon_junction._sv_split` 정의: 못 가른 ⊆ 다리 놓는 ⊆ 닿는 성분) · 기록이 옮겨 실은 census 사본
CENSUS_KEYS = ('n_unsplit_bridging_components', 'n_bridging_components', 'n_sdcp_components_touching')
CENSUS_COPY_KEYS = CENSUS_KEYS + ('n_sv_faces_kept_self',)
#: 투영이 옮기는 칸 (판정 · 기록) — 정의별 수 칸 (`n_*` · int) 은 이 목록 밖이어도 이름 그대로 옮긴다
_COPY = ('kind', 'requested', 'threshold', 'status', 'flag', 'cg_info')


def _is_bool(x):
    return isinstance(x, bool) or type(x).__name__ in ('bool_', 'bool')


def _fin_or_none(x):
    """유한 실수 → float · 그 밖 (bool · 수 아님 · NaN · ±inf) → None."""
    if _is_bool(x) or not isinstance(x, numbers.Real):
        return None
    v = float(x)
    return v if math.isfinite(v) else None


def _ratio_proj(r_):
    """비 → (투영 비, 표지) — +∞ = (None, 'inf') · 유한 = (float, None) · NaN · -inf · bool = (None, None) (그 상태의 꼴 검사가 거부한다) ·
    문자열 = 그대로 (검증기가 거부)."""
    if isinstance(r_, numbers.Real) and not _is_bool(r_) and math.isinf(float(r_)) and float(r_) > 0:
        return None, 'inf'
    if r_ is not None and not isinstance(r_, str):
        return _fin_or_none(r_), None
    return r_, None


def _num_proj(v):
    """증서의 수 칸 → JSON 투영 — 정수 = int · 유한 실수 = float · 비유한 = None · bool · 글자 · None = 그대로 (검증기 · 구간 함수가 거부)."""
    if _is_bool(v) or not isinstance(v, numbers.Real):
        return v
    if isinstance(v, numbers.Integral):
        return int(v)
    f = float(v)
    return f if math.isfinite(f) else None


def _cert_proj(cc):
    """수렴 증서 → 투영 (★ 10-23 · RCA2-01 · 04 — `CERT_PROJ_KEYS`: 판 · 상태 · ⓐ–ⓓ · 게시 판 전류 · 목표량 구간 · 목표량 판 · 봉인 · 영값 위상 칸 ·
    결합 칸) · dict 아닌 값 = 그대로 (None = 증서 없음 · 그 밖 = 검증기가 거부)."""
    if not isinstance(cc, dict):
        return cc
    return {k: (_num_proj(cc.get(k)) if k in _CERT_NUM_KEYS else cc.get(k)) for k in CERT_PROJ_KEYS}


def _enc(x):
    """구간 끝 → JSON (+∞ = 'inf' · 유한 float · None 그대로)."""
    return 'inf' if (isinstance(x, float) and x == math.inf) else x


def _end_proj(rec):
    """반사실 한 끝의 풀이 칸 → 투영 (비 · 표지 · G_cut · 잔차 · 증서 · backend · 정의별 수 칸) — 아래 끝 (기록 자신) · 위 끝 (`upper`) 같은 꼴.
    ★ 10-23 — 증서 = `_cert_proj` (목표량 구간 · 게시 판 전류 · 결합 칸을 버리지 않는다)."""
    r_, lim = _ratio_proj(rec.get('sv_counterfactual_ratio'))
    out = {'sv_counterfactual_ratio': r_, 'ratio_limit': lim, 'G_cut_code': _fin_or_none(rec.get('G_cut_code')),
           'resid': _fin_or_none(rec.get('resid'))}
    for k, v in rec.items():                       # 정의별 수 칸 (끊은 면 수 · 다리 놓는 SDCP 수 …) — 이름 그대로 · int 만
        if isinstance(k, str) and k.startswith('n_') and isinstance(v, numbers.Integral) and not _is_bool(v):
            out[k] = int(v)
    out['conv_cert'] = _cert_proj(rec.get('conv_cert'))
    bk = rec.get('backend_last_solve')
    out['backend_last_solve'] = ({k: bk.get(k) for k in ('used', 'requested', 'precond', 'fallback_reason')}
                                 if isinstance(bk, dict) else None)
    return out


def sv_cf_record(rec):
    """반사실 원 기록 → 증거 투영 (JSON 유한 · 판정 칸 · 사본 아님 — 원 기록의 값을 그대로 옮긴다).  ★ 10-22 괄호 칸 (규칙 · 위 끝 상태 · 비 ·
    위 끝 풀이 기록) 도 같은 꼴로 옮긴다 (원 기록에 없으면 None — 검증기가 거부 · 사슬 = 위 끝 못 읽음).
    ★ 10-23 (RCA2-01 · 04 · Q1 (가)) — 기록 지위 (`standing`) · 주 해 증서 (`conv_cert_full`) · 판정 근거 칸 `ratio_cert_interval` (= 이 투영에서
    `cert_interval` 로 센 [아래비, 위비] · +∞ = 'inf' · 못 정함 = None)."""
    if not isinstance(rec, dict):
        return None
    e = _end_proj(rec)
    out = {k: rec.get(k) for k in _COPY}
    out.update({'sv_counterfactual_ratio': e['sv_counterfactual_ratio'], 'ratio_limit': e['ratio_limit'],
                'G_full_code': _fin_or_none(rec.get('G_full_code')), 'G_cut_code': e['G_cut_code'], 'resid': e['resid']})
    out.update({k: v for k, v in e.items() if k.startswith('n_')})
    out['conv_cert'], out['backend_last_solve'] = e['conv_cert'], e['backend_last_solve']
    rh, lh = _ratio_proj(rec.get('sv_counterfactual_ratio_hi'))
    up = rec.get('upper')
    upp = None
    if isinstance(up, dict):
        upp = {'status': up.get('status'), 'cg_info': up.get('cg_info'), 'why': up.get('why')}
        upp.update(_end_proj(up))
    elif up is not None:
        upp = up                                   # dict 아닌 값 = 그대로 (검증기가 거부)
    out.update({'bracket_rule': rec.get('bracket_rule'), 'status_hi': rec.get('status_hi'), 'sv_counterfactual_ratio_hi': rh,
                'ratio_limit_hi': lh, 'upper': upp})
    out['standing'] = rec.get('standing')
    out['conv_cert_full'] = _cert_proj(rec.get('conv_cert_full'))
    lo, hi = cert_interval(out)
    out['ratio_cert_interval'] = [_enc(lo), _enc(hi)]
    return out


def request_problem(req):
    """요청 꼴 → 문제 | None — {'threshold': None | 유한 실수 ≥ 1} (producer `carbon_junction._sv_cf_request` 와 같은 정의역)."""
    if not isinstance(req, dict) or set(req) != {'threshold'}:
        return f"요청 꼴 {req!r} (= {{'threshold': None | 실수 ≥ 1}})"
    t = req['threshold']
    if t is None:
        return None
    if _is_bool(t) or not isinstance(t, numbers.Real) or not math.isfinite(float(t)) or float(t) < 1.0:
        return f'요청 문턱 {t!r} (유한 실수 ≥ 1 · 비 G_full/G_cut ≥ 1 = Rayleigh)'
    return None


def attach_evidence(ev, request):
    """payload — 접합 블록 증거 (`ca_ext_cjunc.payload_blocks` 의 evidence) 에 요청을 싣고, 솔브 요약이 옮긴 원 기록을 투영으로 바꾼다
    (끔 = 이 함수를 부르지 않는다 = 칸 없음 = 옛 바이트)."""
    ev['sv_counterfactual_request'] = dict(request)
    sol = ev.get('solve')
    if isinstance(sol, dict) and 'sv_counterfactual' in sol:
        sol['sv_counterfactual'] = sv_cf_record(sol['sv_counterfactual'])
    return ev


def sv_cf_problem(ev, solved):
    """증거의 SV 반사실 요청 ↔ 기록 → 문제 | None.  solved = 주 전자 솔브가 풀렸나 (접합 영수증 applied · absent_geometry).
    요청 없음 ⟹ 기록 없음 · 요청 + 풀림 ⟹ 기록 (종류 · 문턱 · 상태 ↔ 비 ↔ 표지) · 요청 + 조기 반환 ⟹ 기록 없음 (주 해가 없다)."""
    ev = ev if isinstance(ev, dict) else {}
    sol = ev.get('solve') if isinstance(ev.get('solve'), dict) else {}
    has_req, has_rec = 'sv_counterfactual_request' in ev, 'sv_counterfactual' in sol
    if not has_req:
        return 'sv_cf| 요청 없는 반사실 기록 (지금 요청한 런의 것이 아니다)' if has_rec else None
    req = ev['sv_counterfactual_request']
    why = request_problem(req)
    if why:
        return f'sv_cf| {why}'
    if not solved:
        return 'sv_cf| 주 솔브가 조기 반환했는데 반사실 기록이 있다 (주 해 없이 비를 낼 수 없다)' if has_rec else None
    rec = sol.get('sv_counterfactual')
    if not isinstance(rec, dict):
        return 'sv_cf| 요청했고 주 솔브가 풀렸는데 반사실 기록이 없다 (배선 누락)'
    kd = rec.get('kind')
    if not (isinstance(kd, str) and kd.startswith(KIND_PREFIX)) or rec.get('requested') is not True:
        return f'sv_cf| 기록 종류 {kd!r} · requested {rec.get("requested")!r} (반사실 기록이어야 · 정의는 producer 이름 그대로)'
    thr = req['threshold']
    if rec.get('threshold') != thr:
        return f'sv_cf| 기록 문턱 {rec.get("threshold")!r} ≠ 요청 {thr!r}'
    st = rec.get('status')
    if not (isinstance(st, str) and st):
        return f'sv_cf| 상태 {st!r} (비지 않은 낱말)'
    r_, lim, fl = rec.get('sv_counterfactual_ratio'), rec.get('ratio_limit'), rec.get('flag')
    form = RATIO_STATUSES.get(st)
    if form == 'finite':
        if _is_bool(r_) or not isinstance(r_, float) or not math.isfinite(r_) or not r_ > 0.0 or lim is not None:
            return f'sv_cf| {st} 인데 비 {r_!r} · 표지 {lim!r} (유한 양수 · 표지 없음)'
    elif form == 'inf':
        if r_ is not None or lim != 'inf':
            return f'sv_cf| {st} 인데 비 {r_!r} · 표지 {lim!r} (null · inf — 위상의 +∞)'
    elif r_ is not None or lim is not None:
        return f'sv_cf| {st} 인데 비 {r_!r} · 표지 {lim!r} (이 상태는 비를 싣지 않는다)'
    if fl not in FLAGS:
        return f'sv_cf| 모르는 표지 {fl!r}'
    #  producer 의 문턱 비교 (`carbon_junction` — 비 ≥ 문턱) 와 기록이 맞는가 (이 배선은 문턱 None → 표지 None 이어야)
    dep = thr is not None and (lim == 'inf' or (form == 'finite' and r_ >= float(thr)))
    if (fl == 'SV_DEPENDENT') != dep:
        return f'sv_cf| 표지 {fl!r} ↔ 문턱 {thr!r} · 비 {r_!r} · 표지 {lim!r} (문턱 판정과 기록이 갈렸다)'
    why = _bracket_problem(rec)
    if why:
        return why
    why = _values_problem(rec)
    if why:
        return why
    #  ★ 10-23 (Codex 재검토 RCA2-01 · 04 · 1저자 Q1 (가)) — 증서 (지위 · 끝마다 · 분자 · 결합) → 실제 census → 판정 근거 칸 (기록 안에서 먼저 ·
    #    증거 칸 (census · I_bot_code · fp) 대조는 그 뒤 — 기록 자신의 결함은 자기 사유로 거부된다)
    why = _cert_problem(rec, ev)
    if why:
        return why
    why = _census_problem(rec, ev)
    if why:
        return why
    return _interval_problem(rec)


def _form_problem(st, r_, lim, what):
    """상태 ↔ 비 ↔ 표지 꼴 (아래 끝 · 위 끝 같은 규칙) → 문제 | None."""
    form = RATIO_STATUSES.get(st)
    if form == 'finite':
        if _is_bool(r_) or not isinstance(r_, float) or not math.isfinite(r_) or not r_ > 0.0 or lim is not None:
            return f'sv_cf| {what} {st} 인데 비 {r_!r} · 표지 {lim!r} (유한 양수 · 표지 없음)'
    elif form == 'inf':
        if r_ is not None or lim != 'inf':
            return f'sv_cf| {what} {st} 인데 비 {r_!r} · 표지 {lim!r} (null · inf — 위상의 +∞)'
    elif r_ is not None or lim is not None:
        return f'sv_cf| {what} {st} 인데 비 {r_!r} · 표지 {lim!r} (이 상태는 비를 싣지 않는다)'
    return None


def _bracket_problem(rec):
    """★ 10-22 (PRE2-impl-01 · 02 · 1저자 Q1 (다)) 괄호 칸의 꼴 → 문제 | None — 못 가른 덩어리 수 = 0 이상 정수 · 규칙 = 비지 않은 낱말 ·
    위 끝 상태 ↔ 비 ↔ 표지 (아래 끝과 같은 규칙) · 덩어리 0 ⟹ 위 끝 풀이 기록 없음 · 위 = 아래 (상태 · 비 · 표지) · 덩어리 > 0 ⟹ 위 끝 풀이
    기록 (dict · 꼴) = 위 끝 칸.  비 값의 대조 (G 비 다시 셈 · 아래 ≤ 위) 는 이 함수 밖 (★ PF2 E `_values_problem`).
    ★ 10-23 (RCA2-06 F6) 예외 하나 — 위 끝 풀이 기록이 구조화 실패 (`UNSPLIT_MISMATCH` · census 수 ≠ 다시 가른 수) 면 덩어리 수 (0 · > 0) 와 무관하게
    그 꼴만 본다 (`_mismatch_problem` · 덩어리 0 인데 위 끝 기록이 있는 유일한 꼴 · 제거 수 대조 밖)."""
    nu = rec.get('n_unsplit_bridging_components')
    if not _count_ok(nu):
        return f'sv_cf| 못 가른 덩어리 수 {nu!r} (0 이상 정수 · int64 범위 — 의미 범위 · 괄호 판정 10-22 · 10-23 RCA2-04)'
    br = rec.get('bracket_rule')
    if not (isinstance(br, str) and br in BRACKET_RULES):
        return f'sv_cf| 괄호 규칙 {br!r} — 등록된 값만 {BRACKET_RULES} (10-23 RCA2-04 · 위 끝 칸 없는 옛 기록 = 거부)'
    sh, rh, lh = rec.get('status_hi'), rec.get('sv_counterfactual_ratio_hi'), rec.get('ratio_limit_hi')
    if not (isinstance(sh, str) and sh):
        return f'sv_cf| 위 끝 상태 {sh!r} (비지 않은 낱말)'
    why = _form_problem(sh, rh, lh, '위 끝')
    if why:
        return why
    up = rec.get('upper')
    if isinstance(up, dict) and up.get('status') == UNSPLIT_MISMATCH:
        return _mismatch_problem(rec, up, int(nu))
    if int(nu) == 0:
        if up is not None:
            return f'sv_cf| 못 가른 덩어리 0 인데 위 끝 풀이 기록 {type(up).__name__} (다시 풀지 않는다 · 위 = 아래)'
        if (sh, rh, lh) != (rec.get('status'), rec.get('sv_counterfactual_ratio'), rec.get('ratio_limit')):
            return (f'sv_cf| 못 가른 덩어리 0 인데 위 끝 ({sh!r}, {rh!r}, {lh!r}) ≠ 아래 끝 ({rec.get("status")!r}, '
                    f'{rec.get("sv_counterfactual_ratio")!r}, {rec.get("ratio_limit")!r}) (위 = 아래)')
        return None
    if not isinstance(up, dict):
        return f'sv_cf| 못 가른 덩어리 {nu} 인데 위 끝 풀이 기록 {up!r} (덩어리가 있으면 늘 두 번 푼다 · 값 봉인)'
    ust, ur, ul = up.get('status'), up.get('sv_counterfactual_ratio'), up.get('ratio_limit')
    if not (isinstance(ust, str) and ust):
        return f'sv_cf| 위 끝 풀이 기록 상태 {ust!r} (비지 않은 낱말)'
    why = _form_problem(ust, ur, ul, '위 끝 풀이 기록')
    if why:
        return why
    if (ust, ur, ul) != (sh, rh, lh):
        return f'sv_cf| 위 끝 칸 ({sh!r}, {rh!r}, {lh!r}) ≠ 위 끝 풀이 기록 ({ust!r}, {ur!r}, {ul!r})'
    return _removed_problem(up, int(nu))


def _mismatch_problem(rec, up, nu):
    """★ 10-23 (Codex 재검토 RCA2-06 F6 · author 10-23 ratified Q1-Q8) 위 끝 구조화 실패 `UNSPLIT_MISMATCH` → 문제 | None — 생산자 정의
    (`carbon_junction.sv_counterfactual`): census 의 못 가른 덩어리 수 nu ≠ 지문 묶인 원장에서 다시 가른 수 → 위 끝을 풀지 않는다 (fail-closed).
    받는 꼴 = 다시 가른 수 (`n_components_removed` · 0 이상 정수 · int64 범위) ≠ nu · 사유 (`why`) = 비지 않은 글 · 풀이 칸 (`MISMATCH_EMPTY_KEYS`)
    없음 · 위 끝 칸 (`status_hi` · 비 · 표지) = (상태, None, None).  받은 기록의 위 끝 = 비 없음 → 사슬 = 못 읽음 (SV_UNCHECKED · 사유에 상태 이름)."""
    nr = up.get('n_components_removed')
    if not _count_ok(nr) or int(nr) == nu:
        return (f'sv_cf| 위 끝 {UNSPLIT_MISMATCH} 인데 다시 가른 덩어리 수 {nr!r} (0 이상 정수 · int64 범위 · census 수 {nu} 와 달라야 — 그 상태의 '
                f'정의 · 10-23 RCA2-06)')
    why = up.get('why')
    if not (isinstance(why, str) and why.strip()):
        return f'sv_cf| 위 끝 {UNSPLIT_MISMATCH} 인데 사유 {why!r} (비지 않은 글 · 10-23 RCA2-06)'
    filled = [k for k in MISMATCH_EMPTY_KEYS if up.get(k) is not None]
    if filled:
        return f'sv_cf| 위 끝 {UNSPLIT_MISMATCH} 인데 풀이 칸 {filled} 이 있다 (풀지 않은 끝 · 10-23 RCA2-06)'
    hi = (rec.get('status_hi'), rec.get('sv_counterfactual_ratio_hi'), rec.get('ratio_limit_hi'))
    if hi != (UNSPLIT_MISMATCH, None, None):
        return f'sv_cf| 위 끝 풀이 기록 = {UNSPLIT_MISMATCH} 인데 위 끝 칸 {hi!r} (같은 상태 · 비 · 표지 없음 · 10-23 RCA2-06)'
    return None


def _count_ok(v):
    """수 칸의 의미 범위 (★ 10-23 · RCA2-04) — 0 이상 정수 (bool 아님) · int64 범위 (10**400 = 거부)."""
    return isinstance(v, numbers.Integral) and not _is_bool(v) and 0 <= int(v) <= COUNT_MAX


def _removed_problem(up, nu):
    """★ 10-23 (Codex 재검토 RCA2-04 · 생산자 정의 `carbon_junction.sv_counterfactual`) 위 끝 풀이 기록의 제거 수 → 문제 | None —
    제거 성분 수 = 못 가른 덩어리 수 (지문 묶인 원장에서 다시 가른 수 = census 수 · 다르면 `unsplit_census_mismatch` 꼴) · 제거 셀 수 = 그 성분의
    SDCP 셀 수 ≥ 성분 수 (성분마다 셀 ≥ 1 · 비를 싣는 끝은 필수) · 끊은 간선 · 판 결합 · SV 면 수 = 0 이상 정수 (있으면) · 전부 int64 범위."""
    nc = up.get('n_components_removed')
    if not _count_ok(nc) or int(nc) != nu:
        return f'sv_cf| 위 끝 제거 성분 수 {nc!r} ≠ 못 가른 덩어리 수 {nu} (생산자 정의 = 같다 · 0 이상 정수 · int64 범위 · 10-23 RCA2-04)'
    ncell = up.get('n_cells_removed')
    need = RATIO_STATUSES.get(up.get('status')) is not None
    if (ncell is not None or need) and (not _count_ok(ncell) or int(ncell) < nu):
        return (f'sv_cf| 위 끝 제거 셀 수 {ncell!r} (0 이상 정수 · int64 범위 · 제거 성분 수 {nu} 이상 — 성분마다 SDCP 셀 ≥ 1 · 비를 싣는 끝은 '
                f'필수 · 10-23 RCA2-04)')
    for k in ('n_edges_cut', 'n_plate_couplings_cut', 'n_sv_faces_cut'):
        if up.get(k) is not None and not _count_ok(up.get(k)):
            return f'sv_cf| 위 끝 {k} {up.get(k)!r} (0 이상 정수 · int64 범위 · 10-23 RCA2-04)'
    return None


def _pos_float(x):
    """유한 양의 float (bool · 정수 · 글자 · NaN · ±∞ · 0 · 음수 아님)."""
    return isinstance(x, float) and not _is_bool(x) and math.isfinite(x) and x > 0.0


def _end_values_problem(end, G_full, what):
    """★ PF2 E (10-22 · 사전 리뷰 2 회차 PRE2-impl-02 · 결정 없음) — 한 끝 (아래 = 기록 자신 · 위 = `upper`) 의 수 대조 → 문제 | None.
    computed = G_full · G_cut 유한 양수 · 비 = G_full/G_cut (상대 `RATIO_REL_TOL` · 그 값이 유한) · 비 ≥ `RATIO_FLOOR` (증서 폭 꼴) · 반사실 증서가
    있으면 ok · ⓐ–ⓓ 참 · POSITIVE_SOLVED (플래그를 믿지 않는다) · no_through_without_sv = G_cut 정확히 0 · G_full 유한 양수 (+∞ 의 분자) · 비를
    싣지 않는 상태 = 수 대조 없음 (사슬 = 못 읽음)."""
    st = end.get('status')
    form = RATIO_STATUSES.get(st)
    if form is None:
        return None
    if not _pos_float(G_full):
        return f'sv_cf| {what} {st} 인데 G_full {G_full!r} (유한 양수 — 비의 분자 · 주 해 단자 G)'
    gc = end.get('G_cut_code')
    if form == 'inf':
        if not (isinstance(gc, float) and not _is_bool(gc) and gc == 0.0):
            return f'sv_cf| {what} {st} 인데 G_cut {gc!r} (관통 없음 = 0.0)'
        return None
    if not _pos_float(gc):
        return f'sv_cf| {what} {st} 인데 G_cut {gc!r} (유한 양수 — 비의 분모)'
    r_ = end.get('sv_counterfactual_ratio')
    want = G_full / gc
    if not (math.isfinite(want) and abs(r_ - want) <= RATIO_REL_TOL * want):
        return f'sv_cf| {what} 비 {r_!r} ≠ G_full/G_cut {want!r} (상대 {RATIO_REL_TOL:g} · 기록 안 수가 서로 맞지 않는다)'
    if not r_ >= RATIO_FLOOR:
        return (f'sv_cf| {what} 비 {r_!r} < (1 − τ)/(1 + τ) = {RATIO_FLOOR!r} (τ = 증서 ⓓ 보장 상대 오차 {CERT_TARGET_TOL:g} · 끊기만 한 그래프의 '
                f'비 ≥ 1 = Rayleigh)')
    cc = end.get('conv_cert')
    if cc is not None:
        if not isinstance(cc, dict):
            return f'sv_cf| {what} 반사실 증서 꼴 {type(cc).__name__} (dict 이어야)'
        bad = [k for k in ('ok', 'pass_a', 'pass_b', 'pass_c', 'pass_d') if cc.get(k) is not True]
        if bad or cc.get('status') != CERT_OK_STATUS:
            return (f'sv_cf| {what} {st} 인데 반사실 증서 상태 {cc.get("status")!r} · 참이 아닌 칸 {bad} (ok · ⓐ–ⓓ 참 · {CERT_OK_STATUS} 이어야 · '
                    f'플래그를 믿지 않는다)')
    return None


def _values_problem(rec):
    """★ PF2 E — 아래 끝 · 위 끝 (못 가른 덩어리 > 0 이면 `upper`) 의 수 대조 + 괄호 아래 ≤ 위 (같은 증서 폭 여유 · 아래 +∞ ⟹ 위 +∞) → 문제 | None.
    꼴 검사 (`sv_cf_problem` · `_bracket_problem`) 를 지난 기록에만 (상태 ↔ 비 꼴 · 덩어리 0 ⟹ 위 = 아래 · 위 끝 칸 = 위 끝 풀이 기록)."""
    gf = rec.get('G_full_code')
    why = _end_values_problem(rec, gf, '아래 끝')
    if why:
        return why
    up = rec.get('upper')
    if isinstance(up, dict):
        why = _end_values_problem(up, gf, '위 끝')
        if why:
            return why
    lo = _end_view(rec.get('status'), rec.get('sv_counterfactual_ratio'), rec.get('ratio_limit'))
    hi = _end_view(rec.get('status_hi'), rec.get('sv_counterfactual_ratio_hi'), rec.get('ratio_limit_hi'))
    if lo is None or hi is None:
        return None
    if not (hi == math.inf or hi >= lo * RATIO_FLOOR):       # 아래 +∞ ⟹ lo × 여유 = +∞ ⟹ 위도 +∞ 이어야 (관통 없음이 되살아날 수 없다)
        return (f'sv_cf| 괄호 위 {hi!r} < 아래 {lo!r} × (1 − τ)/(1 + τ) (위 = 덩어리를 더 뺀 판 · 참 G_cut,hi ≤ G_cut,lo · 아래 +∞ 면 위도 +∞ · '
                f'증서 폭 여유 τ {CERT_TARGET_TOL:g} · Rayleigh)')
    return None


# ═════════════════════════ ★ 10-23 증서 구간 (Codex 재검토 RCA2-01 · 04 · 1저자 Q1 (가)) ═════════════════════════
def _hex32(v):
    return isinstance(v, str) and len(v) == 32 and all(ch in '0123456789abcdef' for ch in v)


def _ends(rec):
    """기록의 끝 [(이름, 끝)] — 아래 끝 = 기록 자신 · 위 끝 = `upper` 풀이 기록 (dict 일 때 · 못 가른 덩어리 0 = 아래 끝 그 자체)."""
    out = [('아래 끝', rec)]
    if isinstance(rec.get('upper'), dict):
        out.append(('위 끝', rec['upper']))
    return out


def _pos_cert_problem(cc, G, what, CC):
    """양의 해 증서 ↔ 그 끝의 G → 문제 | None — 현 판 (`CERT_VERSION`) · POSITIVE_SOLVED · ok · ⓐ–ⓓ 참 (bool) · 목표량 판 · 부동소수 규칙 · τ 봉인 ·
    게시 판 전류 = G (정확히 · 다른 회로의 증서 = 거부) · 목표량 구간을 그 G 로 같은 판정 함수 (`step3_conv_cert.target_judge`) 에 다시 넣어 통과."""
    if not isinstance(cc, dict):
        return (f'sv_cf| {what} 증서가 없다 ({type(cc).__name__}) — 증서 구간 기록의 비를 싣는 끝 = 현 증서 필수 (무증서 = 진단 기록만 · '
                f'10-23 RCA2-04)')
    if cc.get('version') != CC.CERT_VERSION:
        return f'sv_cf| {what} 증서 판 {cc.get("version")!r} ≠ 현 판 {CC.CERT_VERSION!r}'
    bad = [k for k in ('ok', 'pass_a', 'pass_b', 'pass_c', 'pass_d') if cc.get(k) is not True]
    if bad or cc.get('status') != CC.STATUS_POSITIVE:
        return f'sv_cf| {what} 증서 상태 {cc.get("status")!r} · 참이 아닌 칸 {bad} ({CC.STATUS_POSITIVE} · ok · ⓐ–ⓓ 참이어야)'
    for k, want in (('target_version', CC.TARGET_VERSION), ('target_fp', CC.TARGET_FP_RULE), ('target_tol', CC.CERT_TARGET_TOL)):
        if cc.get(k) != want:
            return f'sv_cf| {what} 증서 {k} = {cc.get(k)!r} ≠ 이 코드의 봉인 {want!r}'
    ib = cc.get('I_bot')
    if not (isinstance(ib, float) and not _is_bool(ib) and isinstance(G, float) and ib == G):
        return f'sv_cf| {what} 증서 게시 판 전류 {ib!r} ≠ 그 끝의 G {G!r} (정확히 같아야 — 다른 회로의 증서 · 10-23 RCA2-04)'
    jd = CC.target_judge(cc.get('target_lo'), cc.get('target_hi'), G)
    if jd.get('pass_d') is not True:
        return f'sv_cf| {what} 증서 목표량 구간을 그 끝의 G 로 다시 보면 실패 — {jd.get("target_why")}'
    return None


def _zero_cert_problem(cc, what, CC):
    """+∞ 끝 (관통 없음) 의 영값 위상 증서 → 문제 | None — 현 판 · VALID_ZERO_TOPOLOGY · ok True · 조기 반환 출처 · 영값 위상 사유 · 관통 dof 0 ·
    σ 정확히 0 (∞ = 위상이 증명한 0 분모만 · 10-23 RCA2-01)."""
    if not isinstance(cc, dict):
        return (f'sv_cf| {what} 관통 없음 (+∞) 인데 영값 위상 증서가 없다 ({type(cc).__name__}) — ∞ = 위상이 증명한 0 분모만 '
                f'(10-23 RCA2-01)')
    if cc.get('version') != CC.CERT_VERSION or cc.get('status') != CC.STATUS_ZERO or cc.get('ok') is not True:
        return (f'sv_cf| {what} 관통 없음 증서 판 {cc.get("version")!r} · 상태 {cc.get("status")!r} · ok {cc.get("ok")!r} '
                f'({CC.CERT_VERSION} · {CC.STATUS_ZERO} · True 이어야)')
    if (cc.get('zero_source') != 'early_return' or CC.classify_reason(cc.get('reason')) != CC.STATUS_ZERO
            or cc.get('zero_graph') != ZERO_GRAPH_SV_CF):
        return (f'sv_cf| {what} 관통 없음 증서 출처 {cc.get("zero_source")!r} · 사유 {cc.get("reason")!r} · 그래프 {cc.get("zero_graph")!r} '
                f'(조기 반환 · 영값 위상 사유 · 끊은 반사실 그래프 {ZERO_GRAPH_SV_CF!r} 이어야)')
    ntd, s = cc.get('n_through_dof'), cc.get('sigma')
    if not (type(ntd) is int and ntd == 0 and isinstance(s, float) and not _is_bool(s) and s == 0.0):   # noqa: E721
        return f'sv_cf| {what} 관통 없음 증서 관통 dof {ntd!r} · σ {s!r} (0 · 0.0 이어야)'
    return None


def _cert_problem(rec, ev):
    """★ 10-23 (Codex 재검토 RCA2-01 · 04 · 1저자 Q1 (가)) 기록 지위 · 증서 → 문제 | None.
    · 지위 ∈ `STANDINGS` · 진단 = 증서가 하나도 없다 (주 해 · 끝 — 실려 있으면 지위와 모순) · 사슬은 진단 기록을 R 판정 입력으로 받지 않는다
    · 증서 구간 + 비를 싣는 끝이 있다 → 분자 = 주 해 증서 (`conv_cert_full` · `_pos_cert_problem` · 게시 판 전류 = G_full = 솔브 기록
      `I_bot_code` · 결합 칸 = 판 · 격자 · σ 표 hex32 · 증거 `fp` 의 sid · registry · plan_rows) · 비를 싣는 끝마다 그 끝의 증서 (computed =
      양의 해 · 관통 없음 = 영값 위상) · 결합 칸 = 주 해 증서와 같다 (다른 런 · 다른 계획 증서 = 거부) · 비를 싣지 않는 끝 = 대조 없음."""
    st = rec.get('standing')
    if st not in STANDINGS:
        return f'sv_cf| 기록 지위 {st!r} (∈ {STANDINGS} · 10-23 RCA2-04 — 지위 칸 없는 옛 기록 = 거부)'
    ends = _ends(rec)
    full = rec.get('conv_cert_full')
    if st == STANDING_DIAGNOSTIC:
        bad = [w for w, e in ends if e.get('conv_cert') is not None] + (['주 해'] if full is not None else [])
        if bad:
            return f'sv_cf| 진단 기록 (증서 없는 런) 인데 증서가 실려 있다 ({bad}) — 지위 ↔ 증서 모순'
        return None
    if not any(RATIO_STATUSES.get(e.get('status')) for _w, e in ends):
        return None
    import step3_conv_cert as CC                   # 증서 정본 (판 · 상태 · 봉인 · 판정 함수) — 못 불러오면 계약이 unverifiable 로 거부
    G = rec.get('G_full_code')
    why = _pos_cert_problem(full, G, '주 해 (분자 G_full)', CC)
    if why:
        return why
    sol = ev.get('solve') if isinstance(ev.get('solve'), dict) else {}
    ib = sol.get('I_bot_code')
    if not (isinstance(ib, float) and not _is_bool(ib) and ib == G):
        return f'sv_cf| 분자 G_full {G!r} ≠ 솔브 기록 I_bot_code {ib!r} (그 런의 주 해 단자 전류와 정확히 같아야 · 10-23 RCA2-04)'
    if full.get('bind_version') != CC.BIND_VERSION or not _hex32(full.get('fp_sig')):
        return f'sv_cf| 주 해 증서 결합 판 {full.get("bind_version")!r} · σ 표 지문 {full.get("fp_sig")!r} ({CC.BIND_VERSION} · hex32 이어야)'
    fp = ev.get('fp') if isinstance(ev.get('fp'), dict) else {}
    for ck, ek in (('fp_sid', 'sid'), ('fp_cjunc_registry', 'registry'), ('fp_cjunc_rows', 'plan_rows')):
        if not (_hex32(full.get(ck)) and full.get(ck) == fp.get(ek)):
            return f'sv_cf| 주 해 증서 {ck} {full.get(ck)!r} ≠ 증거 fp.{ek} {fp.get(ek)!r} — 다른 런 · 다른 계획의 증서 (10-23 RCA2-04)'
    for w, e in ends:
        form = RATIO_STATUSES.get(e.get('status'))
        if form is None:
            continue
        cc = e.get('conv_cert')
        why = (_pos_cert_problem(cc, e.get('G_cut_code'), w, CC) if form == 'finite' else _zero_cert_problem(cc, w, CC))
        if why:
            return why
        diff = [k for k in BIND_FIELDS if cc.get(k) != full.get(k)]
        if diff:
            return f'sv_cf| {w} 증서 결합 칸 {diff} ≠ 주 해 증서 — 다른 런 · 다른 계획의 증서 (10-23 RCA2-04)'
    return None


def _census_problem(rec, ev):
    """★ 10-23 (Codex 재검토 RCA2-04) 실제 census (증거 `census` · 생산자가 원장에서 낸 값) ↔ 기록 → 문제 | None — 세 칸 = 0 이상 정수 · int64 ·
    못 가른 ≤ 다리 놓는 ≤ 닿는 성분 (생산자 정의 `carbon_junction._sv_split`) · 기록이 옮겨 실은 census 사본 (`CENSUS_COPY_KEYS`) = 실제 census."""
    cen = ev.get('census') if isinstance(ev, dict) else None
    if not isinstance(cen, dict):
        return 'sv_cf| 증거 census 가 없다 — 못 가른 덩어리 수 · 제거 수를 실제 census 와 대조할 수 없다 (10-23 RCA2-04)'
    for k in CENSUS_KEYS:
        if not _count_ok(cen.get(k)):
            return f'sv_cf| 증거 census {k} = {cen.get(k)!r} (0 이상 정수 · int64 범위)'
    nu, nb, nt = (int(cen[k]) for k in CENSUS_KEYS)
    if not nu <= nb <= nt:
        return (f'sv_cf| 증거 census 못 가른 {nu} ≤ 다리 놓는 {nb} ≤ 닿는 성분 {nt} 가 아니다 (생산자 정의 — 못 가른 덩어리 ⊆ 다리 놓는 성분 ⊆ '
                f'닿는 성분)')
    for k in CENSUS_COPY_KEYS:
        v = rec.get(k)
        if v is None and k != 'n_unsplit_bridging_components':
            continue
        w = cen.get(k)
        if not (_count_ok(v) and _count_ok(w) and int(v) == int(w)):
            return f'sv_cf| 기록 {k} {v!r} ≠ 증거 census {w!r} (기록의 census 사본 = 실제 census · 10-23 RCA2-04)'
    return None


def _interval_problem(rec):
    """★ 10-23 (RCA2-01) 판정 근거 칸 `ratio_cert_interval` = 이 기록의 증서에서 `cert_interval` 로 다시 센 값 (같은 꼴 · 같은 수 · +∞ = 'inf')."""
    lo, hi = cert_interval(rec)
    want = [_enc(lo), _enc(hi)]
    got = rec.get('ratio_cert_interval')
    if not (isinstance(got, list) and len(got) == 2 and all(type(a) is type(b) and a == b for a, b in zip(got, want))):   # noqa: E721
        return f'sv_cf| 증서 구간 비 칸 {got!r} ≠ 기록의 증서에서 다시 셈 {want!r} (판정 근거 칸 · 10-23 RCA2-01)'
    return None


def _pos_bracket(cc, G):
    """양의 해 증서 → (목표량 하한, 상한) | None — POSITIVE_SOLVED · ok · ⓐ–ⓓ 참 · 게시 판 전류 = 그 끝의 G (정확) · 0 < 하한 ≤ 상한 유한."""
    if not isinstance(cc, dict) or cc.get('status') != CERT_OK_STATUS:
        return None
    if any(cc.get(k) is not True for k in ('ok', 'pass_a', 'pass_b', 'pass_c', 'pass_d')):
        return None
    ib, a, b = cc.get('I_bot'), cc.get('target_lo'), cc.get('target_hi')
    if not (_pos_float(G) and _pos_float(ib) and ib == G and _pos_float(a) and _pos_float(b) and a <= b):
        return None
    return a, b


def _end_bracket(end):
    """한 끝 → (목표량 하한, 상한) (computed · 양의 해 증서) | 'zero' (관통 없음 · 영값 위상 증서 · G_cut 정확히 0 = 위상이 증명한 0) | None."""
    if not isinstance(end, dict):
        return None
    form = RATIO_STATUSES.get(end.get('status'))
    if form == 'finite':
        return _pos_bracket(end.get('conv_cert'), end.get('G_cut_code'))
    if form == 'inf':
        cc, gc = end.get('conv_cert'), end.get('G_cut_code')
        if (isinstance(cc, dict) and cc.get('status') == CERT_ZERO_STATUS and cc.get('ok') is True
                and cc.get('zero_source') == 'early_return' and cc.get('zero_graph') == ZERO_GRAPH_SV_CF
                and type(cc.get('n_through_dof')) is int and cc['n_through_dof'] == 0
                and isinstance(cc.get('sigma'), float) and cc['sigma'] == 0.0
                and isinstance(gc, float) and not _is_bool(gc) and gc == 0.0):   # noqa: E721
            return 'zero'
    return None


def _div_dir(a, b, up):
    """a / b (유한 양의 float 둘) 의 방향 반올림 — 아래 (up False) = 정확 몫 이하의 가장 큰 float · 위 = 정확 몫 이상의 가장 작은 float
    (정확 분수 — float 나눗셈의 반올림이 칼날에서 판정 쪽으로 기울지 않게) · 위 끝 넘침 = None (∞ = 위상만) · 아래 끝 넘침 = 가장 큰 유한 float."""
    q = Fraction(a) / Fraction(b)
    try:
        f = q.numerator / q.denominator            # int / int = 올바른 반올림 (가장 가까운 float)
    except OverflowError:
        return None if up else sys.float_info.max
    if not math.isfinite(f):
        return None if up else sys.float_info.max
    fq = Fraction(f)
    if up and fq < q:
        f = math.nextafter(f, math.inf)
    elif not up and fq > q:
        f = math.nextafter(f, -math.inf)
    if not math.isfinite(f):
        return None if up else sys.float_info.max
    return f


def cert_interval(rec):
    """★ 10-23 (Codex 재검토 RCA2-01 · 1저자 Q1 (가)) 증서 구간 비 → (아래비, 위비) — 판정 근거 (nominal 비 아님).
    아래비 = Gfull_lo / Gcut_lower_hi (내림) — 참 비 ≥ 아래 끝 참 비 ≥ 이 값 · 위비 = Gfull_hi / Gcut_upper_lo (올림) — 참 비 ≤ 위 끝 참 비 ≤ 이 값
    (Gfull = 주 해 증서 (`conv_cert_full`) · Gcut_lower = 아래 끝 증서 · Gcut_upper = 위 끝 (`upper`) 증서 · 못 가른 덩어리 0 = 아래 끝 그 자체).
    +∞ = 그 끝의 영값 위상 증서가 증명한 0 분모만 · None = 못 정함 (증서 구간 기록 아님 · 주 해 · 그 끝 증서가 없거나 묶이지 않음 · 비를 싣지
    않는 상태 · 위비 넘침).  넘어 온 값은 float · +∞ · None (JSON 'inf' 는 받지 않는다 — 투영 · 검증기가 다시 센다)."""
    if not isinstance(rec, dict) or rec.get('standing') != STANDING_CERTIFIED:
        return None, None
    full = _pos_bracket(rec.get('conv_cert_full'), rec.get('G_full_code'))
    if full is None:
        return None, None
    lo_end = _end_bracket(rec)
    up, nu = rec.get('upper'), rec.get('n_unsplit_bridging_components')
    if isinstance(up, dict):
        hi_end = _end_bracket(up)
    elif up is None and isinstance(nu, numbers.Integral) and not _is_bool(nu) and int(nu) == 0:
        hi_end = lo_end
    else:
        hi_end = None
    lo = math.inf if lo_end == 'zero' else (None if lo_end is None else _div_dir(full[0], lo_end[1], up=False))
    hi = math.inf if hi_end == 'zero' else (None if hi_end is None else _div_dir(full[1], hi_end[0], up=True))
    return lo, hi


def _end_view(st, r_, lim):
    """한 끝의 (상태, 비, 표지) → 사슬이 읽는 비 (float · +∞ · None = 못 읽음).  ★ PF2 E (10-22) — finite 꼴 = 유한 양의 float 만 ·
    inf 꼴 = 비 null + 표지 'inf' 만 (NaN · 음수 · 0 · ±∞ · bool · 수가 실린 inf 꼴 = 못 읽음 → 사슬 SV_UNCHECKED)."""
    form = RATIO_STATUSES.get(st)
    if form == 'finite' and _pos_float(r_):
        return r_
    if form == 'inf' and lim == 'inf' and r_ is None:
        return math.inf
    return None


def chain_view(rec):
    """사슬 (판정) 이 읽는 꼴 → {'status', 'ratio', 'status_hi', 'ratio_hi' (float · +∞ · None), 'n_unsplit', 'standing', 'ratio_cert_lo',
    'ratio_cert_hi'} — 비 · 상태 · 덩어리 수 · 지위 · 증서 구간 (정의 무관).  ★ 10-22 (Q1 (다)) ratio = 아래 끝 · ratio_hi = 위 끝 (못 가른
    덩어리를 통째로 뺀 판 · 덩어리 0 = 아래 끝과 같다) — 위 끝 칸이 없는 옛 기록 = 위 끝 None (못 읽음 · 사슬 = SV_UNCHECKED · fail-closed).
    ★ 10-23 (RCA2-01 · Q1 (가)) 판정 = `ratio_cert_lo` · `ratio_cert_hi` (`cert_interval` 로 이 자리에서 다시 센다 — 기록의 칸을 믿지 않는다) ·
    ratio · ratio_hi (nominal) = 기록 · 보고만 (판정에 쓰지 않는다)."""
    if not isinstance(rec, dict):
        return {'status': None, 'ratio': None, 'status_hi': None, 'ratio_hi': None, 'n_unsplit': None, 'standing': None,
                'ratio_cert_lo': None, 'ratio_cert_hi': None}
    st, sh = rec.get('status'), rec.get('status_hi')
    nu = rec.get('n_unsplit_bridging_components')
    lo, hi = cert_interval(rec)
    return {'status': st, 'ratio': _end_view(st, rec.get('sv_counterfactual_ratio'), rec.get('ratio_limit')),
            'status_hi': sh, 'ratio_hi': _end_view(sh, rec.get('sv_counterfactual_ratio_hi'), rec.get('ratio_limit_hi')),
            'n_unsplit': (int(nu) if isinstance(nu, numbers.Integral) and not _is_bool(nu) else None),
            'standing': rec.get('standing'), 'ratio_cert_lo': lo, 'ratio_cert_hi': hi}
