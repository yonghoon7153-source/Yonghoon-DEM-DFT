#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""생존 변이 셋 (M2e · M2c · M9) 의 뜻 — 같은 프로세스 안에서 사슬 모듈 값 · 함수만 바꿔 (사슬 파일은 고치지 않는다) 실경로 (사슬 main · 시험 틀 고정물 ·
가짜 러너 · 실제 git 원장) 를 지금 사슬 (none) · 변이 (그 이름) 두 번 돌린다.  판정은 재실행 시도 폴더가 있는 바탕 (복사본) 을 넣는다 (probe6f_m2e 의 R11 은
원 바탕만 넣어 "폴더 없음" 으로 멈췄다 — 그 판정은 원장 대조의 뜻이 아니었다).

  python3 -I docs/reviews/rint2_rr_fix_evidence_20261023/preattack6/final/probes/probe6f_mut_paths.py <임시 폴더 바탕> [M2e,M2c,M9]

M2e  원 시도 결과 뒤 · 원인 resource · 자격 False (검사 실패 흔적) → 끝 줄 resume_ok 만 True (reset + 손 줄) → --add --resume 1 · 재실행 · 판정
M2c  원 시도 OOM (자격) → 재실행 2 = 잘못된 주소 (runner_rc · 자격 False · 결과 뒤) → 끝 줄 (항목 2) 의 side 만 pre → --add --resume 1 (= 항목 3) · 판정
M9   같은 사슬 → 끝 줄 (항목 2) 의 cause · resume_ok 를 resource · True 로 → --add --resume 1 (= 항목 3) · 판정
값 · σ 를 찍지 않는다.
"""
import importlib.util
import inspect
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve()
_argv = sys.argv[:]
spec = importlib.util.spec_from_file_location('probe6f_real', HERE.parent / 'probe6f_real.py')
P = importlib.util.module_from_spec(spec)
sys.argv = [_argv[0], _argv[1] if len(_argv) > 1 else '/tmp', 'none']
spec.loader.exec_module(P)
ONLY = set(_argv[2].split(',')) if len(_argv) > 2 else {'M2e', 'M2c', 'M9'}
RR, TM = P.RR, P.TM
KEYS0 = RR.RECOUNT_KEYS
RCP0 = RR.resume_chain_problem
OLD_M9 = "and k < n and (k == orig or x['resume_of'] == orig)]:"


def m9_fn():
    src = inspect.getsource(RCP0)
    assert src.count(OLD_M9) == 1, 'M9 옛 글'
    ns = {}
    exec(compile(src.replace(OLD_M9, 'and k < n and k == orig]:'), '<m9>', 'exec'), RR.__dict__, ns)
    return ns['resume_chain_problem']


def mutate(which):
    RR.RECOUNT_KEYS = KEYS0
    RR.resume_chain_problem = RCP0
    if which == 'M2e':
        RR.RECOUNT_KEYS = tuple(k for k in KEYS0 if k != 'resume_ok')
    elif which == 'M2c':
        RR.RECOUNT_KEYS = tuple(k for k in KEYS0 if k != 'side')
    elif which == 'M9':
        RR.resume_chain_problem = m9_fn()


def forge(tag, d, n, changes):
    res = TM.led_result(d, n)
    dr = TM.led_clone(d, tag + '_forged')
    TM.git_(dr, 'reset', '-q', '--hard', 'HEAD~1')
    TM.led_hand(dr, dict(res, **changes), msg='탐침 — 끝 결과 줄 칸 바꿈')
    return dr, res


def fields(r):
    return {k: (r or {}).get(k) for k in ('status', 'side', 'cause', 'resume_ok')}


def tail(dr, base, n_orig, mode, tag):
    """변이 (mode) 를 건 채: --add --resume n_orig → 재실행 시도 (복사한 바탕) → 판정 (그 바탕의 재실행 시도 폴더) → 칸."""
    mutate(mode)
    try:
        add = TM.led_add(dr, 'ladder:P0', resume=n_orig)
        w = TM.world(tag + '_r')
        c = TM.lad_att(tag + '_r', w, dr, add[1], base=base) if add[1] else None
        rj = (c['out'] / 'rejected.json') if c else None
        rec = json.loads(rj.read_text(encoding='utf-8')) if rj is not None and rj.exists() else {}
        vin = c['out'] if c else base / f'attempt_{n_orig}'
        v = TM.ver_led(tag + '_v', [vin], dr)
        ad = RR.adoption(RR.ledger_parse(TM.led_raw(dr)), 'ladder:P0')
    finally:
        mutate('none')
    return {'mode': mode, 'recount_keys': list(KEYS0 if mode not in ('M2e', 'M2c') else
                                               [k for k in KEYS0 if k != {'M2e': 'resume_ok', 'M2c': 'side'}[mode]]),
            'add_resume_rc': add[0], 'add_n': add[1], 'resume_attempt_rc': (c or {}).get('rc'), 'runner_calls': TM.n_calls(w),
            'resume_stop': TM.stop_code(c) if c else None, 'rejected_code': rec.get('code'), 'rejected_cause': str(rec.get('cause'))[:220],
            'ledger_adoption_after': {'chain': ad['chain'], 'effective': ad['effective'], 'problems': [p[0] for p in ad['problems']]},
            'verdict_stop': TM.stop_code(v), 'verdict_why': str((((v or {}).get('v') or {}).get('stop') or {}).get('cause'))[:260]}


def sc_m2e(mode):
    tag = f'MPe_{mode}'
    d, _rc, _so = TM.led_new(tag)
    _r, n1, _s = TM.led_add(d, 'ladder:P0')
    a = TM.lad_att(tag, TM.world(tag + '_a', dict(TM.PW, faults=[{'do': 'unchecked_fail', 'oom': True, 'match': {'rj': 'inf'}}])), d, n1)
    dr, r1 = forge(tag, d, n1, {'resume_ok': True})
    base = TM.pc_copy_base(a['base'], tag + '_base')
    return dict(honest_1=fields(r1), forged='항목 1 resume_ok → True', **tail(dr, base, n1, mode, tag))


def chain2(tag):
    d, _rc, _so = TM.led_new(tag)
    _r, n1, _s = TM.led_add(d, 'ladder:P0')
    a = TM.lad_att(tag, TM.world(tag + '_a', dict(TM.PW, faults=[{'do': 'oom_after_mark', 'match': {'rj': 'inf'}}])), d, n1)
    _r, n2, _s = TM.led_add(d, 'ladder:P0', resume=n1)
    TM.lad_att(tag + '_b', TM.world(tag + '_b', dict(TM.PW, faults=[{'do': 'illegal_driver_after_mark', 'match': {'rj': 'inf'}}])), d, n2,
               base=a['base'])
    return d, n1, n2, a


def sc_m2c(mode):
    tag = f'MPc_{mode}'
    d, n1, n2, a = chain2(tag)
    r1 = TM.led_result(d, n1)
    dr, r2 = forge(tag, d, n2, {'side': 'pre'})
    base = TM.pc_copy_base(a['base'], tag + '_base')
    return dict(honest_1=fields(r1), honest_2=fields(r2), forged='항목 2 side → pre', **tail(dr, base, n1, mode, tag))


def sc_m9(mode):
    tag = f'MP9_{mode}'
    d, n1, n2, a = chain2(tag)
    r1 = TM.led_result(d, n1)
    dr, r2 = forge(tag, d, n2, {'cause': 'resource', 'resume_ok': True})
    base = TM.pc_copy_base(a['base'], tag + '_base')
    return dict(honest_1=fields(r1), honest_2=fields(r2), forged='항목 2 cause → resource · resume_ok → True', **tail(dr, base, n1, mode, tag))


if __name__ == '__main__':
    P.setup()
    P.out('env', python=sys.version.split()[0], td=TM.TD, recount_keys=list(KEYS0))
    for k, fn in (('M2e', sc_m2e), ('M2c', sc_m2c), ('M9', sc_m9)):
        if k not in ONLY:
            continue
        for mode in ('none', k):
            t0 = time.time()
            try:
                P.out(k, **fn(mode))
            except Exception as e:                       # noqa: BLE001 — 탐침 실패 = 기록
                import traceback
                P.out(k, mode=mode, error=f'{type(e).__name__}: {e}', tb=traceback.format_exc()[-1500:])
            P.out(k + '_t', mode=mode, seconds=round(time.time() - t0, 1))
