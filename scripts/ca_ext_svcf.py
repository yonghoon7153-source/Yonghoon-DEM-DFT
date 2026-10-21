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


def sv_cf_record(rec):
    """반사실 원 기록 → 증거 투영 (JSON 유한 · 판정 칸 · 사본 아님 — 원 기록의 값을 그대로 옮긴다)."""
    if not isinstance(rec, dict):
        return None
    r_ = rec.get('sv_counterfactual_ratio')
    lim = None
    if isinstance(r_, numbers.Real) and not _is_bool(r_) and math.isinf(float(r_)) and float(r_) > 0:
        r_, lim = None, 'inf'
    elif r_ is not None and not isinstance(r_, str):
        r_ = _fin_or_none(r_)                      # NaN · -inf · bool = None (그 상태의 꼴 검사가 거부한다) · 문자열 = 그대로 (검증기가 거부)
    out = {k: rec.get(k) for k in _COPY}
    out.update({'sv_counterfactual_ratio': r_, 'ratio_limit': lim, 'G_full_code': _fin_or_none(rec.get('G_full_code')),
                'G_cut_code': _fin_or_none(rec.get('G_cut_code')), 'resid': _fin_or_none(rec.get('resid'))})
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
    return None


def chain_view(rec):
    """사슬 (판정) 이 읽는 꼴 → {'status', 'ratio' (float · +∞ · None)} — 비 · 상태만 (정의 무관)."""
    if not isinstance(rec, dict):
        return {'status': None, 'ratio': None}
    st = rec.get('status')
    form = RATIO_STATUSES.get(st)
    if form == 'finite' and isinstance(rec.get('sv_counterfactual_ratio'), float):
        return {'status': st, 'ratio': rec['sv_counterfactual_ratio']}
    if form == 'inf' and rec.get('ratio_limit') == 'inf':
        return {'status': st, 'ratio': math.inf}
    return {'status': st, 'ratio': None}
