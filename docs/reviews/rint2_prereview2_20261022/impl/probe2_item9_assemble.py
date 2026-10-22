# -*- coding: utf-8 -*-
"""탐침 2-9 (항목 9 · §5-6 ③ ② ④ · §5-5b) — 순수 함수 `rint_r_chain.assemble` 에 변이 혼합을 넣는다.
기대 (등록 R 4판 §5-6 ①–⑤ · §5-5b 결정표 · ⑰): 멈춘 변이 = <V>_UNCHECKED · 다른 이름 = <V>_SENSITIVE · 같은 이름 + 자기 CALIB_ORIGIN_SENSITIVE =
<V>_UNCHECKED · 안 돌림 = <V>_UNCHECKED + 감도 미완료 · 주 판정 이름 · 상태는 그대로 · PASS 문장 막힘."""
import json
import os
import sys
REPO = os.environ.get('PRE_REPO')
sys.path.insert(0, os.path.join(REPO, 'scripts'))
import rint_r_chain as R   # noqa: E402

LAWS, CS, RR = R.LAWS, R.CS, R.RJ_ROLES


def vals_of(lo, hi):
    """12 모서리 — 법칙 P0 = [lo, m] · P1 = [m, hi] 가 붙어 U = E = [lo, hi] (S/cm)."""
    m = (lo * hi) ** 0.5
    out = {}
    for law in LAWS:
        a, b = (lo, m) if law == 'P0' else (m, hi)
        for i, rr in enumerate(RR):
            for c in CS:
                out[(c, law, rr)] = a + (b - a) * (i / 2.0)
    return out


CAL = {'P0': 'CALIBRATED', 'P1': 'CALIBRATED'}
PASS_V = vals_of(4.0e-3, 5.0e-3)            # W = ln 1.25 = 0.223 → PASS (4.68 안)
FAIL_V = vals_of(1.0e-3, 1.2e-3)            # 4.68 밖 → FAIL
sv_none = ([], {'threshold': 2.0, 'scope': 'R_j0', 'corners': {'c0_P0_R_j0': {}}, 'unreadable': [], 'dependent': []})
cases = {
    'A 멈춤 FIBRE · 다른 이름 UNREG · 같은 GRID · 안 돌림 SVORDER': {
        'FIBRE': {'statuses': {'P0': 'NOT_COMPUTED', 'P1': 'CALIBRATED'}, 'vals': None, 'flags': []},
        'UNREG': {'statuses': CAL, 'vals': FAIL_V, 'flags': []},
        'GRID': {'statuses': CAL, 'vals': PASS_V, 'flags': []}},
    'B 넷 다 멈춤 (돌렸는데 결과 없음)': {V: {'statuses': {'P0': 'NOT_COMPUTED', 'P1': 'NOT_COMPUTED'}, 'vals': None, 'flags': []}
                                    for V in R.VARIANTS},
    'C 넷 다 같은 이름 · GRID 만 자기 CALIB_ORIGIN_SENSITIVE': {
        **{V: {'statuses': CAL, 'vals': PASS_V, 'flags': []} for V in R.VARIANTS},
        'GRID': {'statuses': CAL, 'vals': PASS_V, 'flags': ['CALIB_ORIGIN_SENSITIVE']}},
    'D 넷 다 같은 이름 · 표지 없음 (차단 0 이어야 · SV 없음)': {V: {'statuses': CAL, 'vals': PASS_V, 'flags': []} for V in R.VARIANTS},
    'E 변이 CALIB_EDGE (보정 결과 이름) · 나머지 같음': {
        **{V: {'statuses': CAL, 'vals': PASS_V, 'flags': []} for V in R.VARIANTS},
        'FIBRE': {'statuses': {'P0': 'CALIB_EDGE', 'P1': 'CALIBRATED'}, 'vals': None, 'flags': []}},
}
out = {}
for nm, var in cases.items():
    pub, res = R.assemble({'statuses': CAL, 'vals': PASS_V, 'flags': []}, var, sv_none)
    out[nm] = {k: pub[k] for k in ('verdict', 'state', 'flags', 'blocking_flags', 'sensitivity_incomplete', 'sentence_allowed', 'sentence')}
    out[nm]['variants'] = {V: (v.get('flag'), v.get('verdict')) for V, v in pub['variants'].items()}
    print(nm)
    for k, v in out[nm].items():
        print('   ', k, '=', v)
# 주 판정 멈춤 = 판정 전체 NOT_COMPUTED (verdict_compute 의 INPUT_STAGE_STOPPED → _stopped_pub)
st = {'status': 'STOPPED', 'variant': None, 'stop': {'code': 'RUNNER_RC'}}
out['main_stopped_rejects'] = R.stopped_stage_rejects_verdict(st)
out['variant_stopped_is_variant'] = R.variant_stage_stopped(dict(st, variant='GRID'))
pub = R._stopped_pub(R.Stop('INPUT_STAGE_STOPPED', 'x'), [], None)
out['main_stopped_pub'] = {k: pub[k] for k in ('verdict', 'state', 'sentence_allowed', 'sentence')}
print('main stopped', out['main_stopped_rejects'], out['variant_stopped_is_variant'], out['main_stopped_pub'])
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe2_item9_assemble.json'), 'w'), ensure_ascii=False,
          indent=1, default=str)
