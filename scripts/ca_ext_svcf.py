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
  사슬 꼴 (아래 끝 · 위 끝 · 덩어리 수 — 위 끝 칸이 없는 옛 기록 = 위 끝 못 읽음 · fail-closed).  비 값의 대조 (G 비 · 아래 ≤ 위) = 다른 묶음.
numpy 없이 뜬다 (`numbers` · 원 기록의 numpy 수도 받는다)."""
import math
import numbers

#: 비를 싣는 상태 → 비의 꼴 (finite = 유한 양수 · inf = +∞ · JSON null + 'inf')
RATIO_STATUSES = {'computed': 'finite', 'no_through_without_sv': 'inf'}
#: 지금 producer 가 내는 상태 낱말 (기록 · 문서용 — 검증기는 이 목록 밖 상태도 '비 없음' 이면 받는다 · 정의 무관)
KNOWN_STATUSES = ('computed', 'no_through_without_sv', 'unconverged', 'nonpositive_cut_current', 'nonpositive_full_current',
                  'main_unconverged', 'cjunc_electrode_short', 'all_floating_dropped', 'no_through_component')
KIND_PREFIX = 'counterfactual'
FLAGS = (None, 'SV_DEPENDENT')
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


def _end_proj(rec):
    """반사실 한 끝의 풀이 칸 → 투영 (비 · 표지 · G_cut · 잔차 · 증서 · backend · 정의별 수 칸) — 아래 끝 (기록 자신) · 위 끝 (`upper`) 같은 꼴."""
    r_, lim = _ratio_proj(rec.get('sv_counterfactual_ratio'))
    out = {'sv_counterfactual_ratio': r_, 'ratio_limit': lim, 'G_cut_code': _fin_or_none(rec.get('G_cut_code')),
           'resid': _fin_or_none(rec.get('resid'))}
    for k, v in rec.items():                       # 정의별 수 칸 (끊은 면 수 · 다리 놓는 SDCP 수 …) — 이름 그대로 · int 만
        if isinstance(k, str) and k.startswith('n_') and isinstance(v, numbers.Integral) and not _is_bool(v):
            out[k] = int(v)
    cc = rec.get('conv_cert')
    out['conv_cert'] = ({k: cc.get(k) for k in ('version', 'status', 'ok', 'pass_a', 'pass_b', 'pass_c', 'pass_d')}
                        if isinstance(cc, dict) else None)
    bk = rec.get('backend_last_solve')
    out['backend_last_solve'] = ({k: bk.get(k) for k in ('used', 'requested', 'precond', 'fallback_reason')}
                                 if isinstance(bk, dict) else None)
    return out


def sv_cf_record(rec):
    """반사실 원 기록 → 증거 투영 (JSON 유한 · 판정 칸 · 사본 아님 — 원 기록의 값을 그대로 옮긴다).  ★ 10-22 괄호 칸 (규칙 · 위 끝 상태 · 비 ·
    위 끝 풀이 기록) 도 같은 꼴로 옮긴다 (원 기록에 없으면 None — 검증기가 거부 · 사슬 = 위 끝 못 읽음)."""
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
    return _bracket_problem(rec)


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
    기록 (dict · 꼴) = 위 끝 칸.  비 값의 대조 (G 비 다시 셈 · 아래 ≤ 위) 는 이 함수 밖 (다른 묶음)."""
    nu = rec.get('n_unsplit_bridging_components')
    if _is_bool(nu) or not isinstance(nu, numbers.Integral) or int(nu) < 0:
        return f'sv_cf| 못 가른 덩어리 수 {nu!r} (0 이상 정수 · 괄호 판정 · 10-22)'
    br = rec.get('bracket_rule')
    if not (isinstance(br, str) and br):
        return f'sv_cf| 괄호 규칙 {br!r} (비지 않은 낱말 · 위 끝 칸 없는 옛 기록 = 거부)'
    sh, rh, lh = rec.get('status_hi'), rec.get('sv_counterfactual_ratio_hi'), rec.get('ratio_limit_hi')
    if not (isinstance(sh, str) and sh):
        return f'sv_cf| 위 끝 상태 {sh!r} (비지 않은 낱말)'
    why = _form_problem(sh, rh, lh, '위 끝')
    if why:
        return why
    up = rec.get('upper')
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
    return None


def _end_view(st, r_, lim):
    """한 끝의 (상태, 비, 표지) → 사슬이 읽는 비 (float · +∞ · None = 못 읽음)."""
    form = RATIO_STATUSES.get(st)
    if form == 'finite' and isinstance(r_, float) and not _is_bool(r_):
        return r_
    if form == 'inf' and lim == 'inf':
        return math.inf
    return None


def chain_view(rec):
    """사슬 (판정) 이 읽는 꼴 → {'status', 'ratio', 'status_hi', 'ratio_hi' (float · +∞ · None), 'n_unsplit'} — 비 · 상태 · 덩어리 수만
    (정의 무관).  ★ 10-22 (Q1 (다)) ratio = 아래 끝 · ratio_hi = 위 끝 (못 가른 덩어리를 통째로 뺀 판 · 덩어리 0 = 아래 끝과 같다) — 위 끝
    칸이 없는 옛 기록 = 위 끝 None (못 읽음 · 사슬 = SV_UNCHECKED · fail-closed)."""
    if not isinstance(rec, dict):
        return {'status': None, 'ratio': None, 'status_hi': None, 'ratio_hi': None, 'n_unsplit': None}
    st, sh = rec.get('status'), rec.get('status_hi')
    nu = rec.get('n_unsplit_bridging_components')
    return {'status': st, 'ratio': _end_view(st, rec.get('sv_counterfactual_ratio'), rec.get('ratio_limit')),
            'status_hi': sh, 'ratio_hi': _end_view(sh, rec.get('sv_counterfactual_ratio_hi'), rec.get('ratio_limit_hi')),
            'n_unsplit': (int(nu) if isinstance(nu, numbers.Integral) and not _is_bool(nu) else None)}
