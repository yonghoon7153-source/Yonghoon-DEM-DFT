#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""사전 공격 5 회차 (묶음 C · 10-28) — 실경로 탐침 (사슬 `rint_r_chain.main` · 실제 bash 러너 꼴 · 가짜 payload · 실제 프로세스 그룹 · 실제 git 원장).

시험 틀 = `scripts/test_rint_r_chain.py` 의 고정물 · 가짜 러너를 **그대로** 불러 쓴다 (시험 파일은 고치지 않는다).  가짜 러너 원문에 고장 하나만 더한다
(`msg_after_mark` = 첫 풀이 끝 표지 뒤 주어진 한 줄을 찍고 rc 1 — 이 탐침 프로세스 안의 사본에만).

  python3 docs/reviews/rint2_rr_fix_evidence_20261023/preattack5/probe_real.py <임시 폴더 바탕> [R1,R2,R3,R4]

R1 원장 끝 결과 줄 바꿔치기 (git reset · merge -s ours) → 재실행 자격 없는 시도 (runner_rc) 를 resource 로 → --add --resume 받음 → 재실행 → 판정 원장 대조 통과
R2 자원 낱말 — device-side assert · misaligned · launch failed · invalid value (cupy 꼴) = resource · --add --resume 받음 (실경로)
R3 사슬 프로세스의 Stop 아닌 예외 (팔 읽기 중) → 요약 없음 → recover = interrupted · parent_dead · 재실행 자격 True → --add --resume 받음
R4 같은 바탕 폴더의 나중 시도 하나 (다른 대상 · 풀기 전 거부) → 앞 원장 판정의 --reverify = REVERIFY_DIFF (판정 입력은 그대로)
값 · σ 를 찍지 않는다 (가짜 σ 도 화면에 없음).
"""
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

WT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(WT / 'scripts'))
import rint_r_chain as RR  # noqa: E402
import test_rint_r_chain as TM  # noqa: E402

BASE = Path(sys.argv[1] if len(sys.argv) > 1 else tempfile.gettempdir()).resolve()
BASE.mkdir(parents=True, exist_ok=True)
ONLY = set(sys.argv[2].split(',')) if len(sys.argv) > 2 else {'R1', 'R2', 'R3', 'R4'}


def out(tag, **kw):
    print(json.dumps(dict(probe=tag, **kw), ensure_ascii=False, sort_keys=True, default=str), flush=True)


def setup():
    TM.RR = RR
    TM.TD = tempfile.mkdtemp(prefix='pa5_real_', dir=str(BASE))
    anchor = "        if hit('sleep_after_mark'):"
    assert TM.FAKE_SRC.count(anchor) == 1
    TM.FAKE_SRC = TM.FAKE_SRC.replace(anchor, "        if hit('msg_after_mark'):\n            print(hit('msg_after_mark').get('msg'))\n"
                                              "            sys.exit(1)\n"
                                              "        if hit('msg_sleep_after_mark'):\n"
                                              "            print(hit('msg_sleep_after_mark').get('msg'), flush=True)\n"
                                              "            time.sleep(float(hit('msg_sleep_after_mark').get('s', 8.0)))\n"
                                              "            sys.exit(1)\n" + anchor, 1)
    TM.fixtures()


def plan_obj():
    return dict(TM.FX['plan_obj'])


def is_anc(repo, a, b):
    return subprocess.run(['git', '-C', str(repo), 'merge-base', '--is-ancestor', a, b], capture_output=True).returncode == 0


# ───────────────────────── R1 ─────────────────────────
def r1():
    d, _rc, _so = TM.led_new('R1')
    _rc1, n1, _s1 = TM.led_add(d, 'ladder:P0')
    a = TM.lad_att('R1', TM.world('R1_a', dict(TM.PW, faults=[{'do': 'illegal_after_mark', 'match': {'rj': 'inf'}}])), d, n1)
    res1 = TM.led_result(d, 1)
    honest_commit = TM.git_(d, 'rev-parse', 'HEAD')
    # (가) 정직한 원장 — 재실행 거부 (AL19b 와 같음)
    dh = TM.led_clone(d, 'R1_honest')
    rc_h, _nh, so_h = TM.led_add(dh, 'ladder:P0', resume=1)
    # (나) -s ours 꼴 (곁가지에 바꾼 결과 줄 · 본가지를 merge -s ours 로 붙인 커밋으로 본가지를 옮김) — 정직한 결과 줄 커밋은 조상으로 남는다
    ds = TM.led_clone(d, 'R1_ours')
    main = TM.git_(ds, 'rev-parse', '--abbrev-ref', 'HEAD')
    TM.git_(ds, 'checkout', '-q', '-b', 'side', 'HEAD~1')
    TM.led_hand(ds, dict(res1, cause='resource', resume_ok=True), msg='forged result on side (probe)')
    TM.git_(ds, 'merge', '-q', '-s', 'ours', '--no-edit', main)
    merged = TM.git_(ds, 'rev-parse', 'HEAD')
    TM.git_(ds, 'checkout', '-q', main)
    TM.git_(ds, 'reset', '-q', '--hard', merged)
    st_s = RR.ledger_parse(RR.ledger_now(ds)[1])
    e2 = dict(st_s['entries'][1], n=2, resume_of=1)
    ours = {'history_problem': RR.ledger_history_problem(ds, RR.ledger_head(ds)), 'honest_result_commit_is_ancestor': is_anc(ds, honest_commit, merged),
            'order_problem_for_resume_entry': RR.attempt_order_problem(st_s, e2, plan_obj())}
    # (다) 끝 커밋 바꿔치기 (git reset --hard HEAD~1 + 바꾼 결과 줄) — 실제 --add · 재실행 시도 · 판정까지
    TM.git_(d, 'reset', '-q', '--hard', 'HEAD~1')
    TM.led_hand(d, dict(res1, cause='resource', resume_ok=True), msg='forged tip (probe)')
    hist = RR.ledger_history_problem(d, RR.ledger_head(d))
    rc2, n2, so2 = TM.led_add(d, 'ladder:P0', resume=1)
    b = TM.lad_att('R1', TM.world('R1_b'), d, n2, base=a['base']) if n2 else None
    lv = None
    try:
        pub = RR.ledger_verdict_check([b['out']], d)
        lv = {'ok': True, 'targets': pub['targets']}
    except RR.Stop as e:
        lv = {'ok': False, 'stop': e.code, 'cause': str(e.cause)[:200]}
    v = TM.ver_led('R1_v', [b['out']], d) if b else None
    out('R1', honest_result={k: res1.get(k) for k in ('status', 'side', 'cause', 'resume_ok', 'folder_sha256')},
        honest_resume_add_rc=rc_h, honest_refused=('RESUME_NOT_ALLOWED' in so_h),
        s_ours=ours,
        tip_reset={'history_problem': hist, 'resume_add_rc': rc2, 'resume_n': n2,
                   'resume_attempt': (b and {'rc': b['rc'], 'status': (b['sum'] or {}).get('status'), 'resume': (b['sum'] or {}).get('resume')}),
                   'ledger_verdict_check': lv,
                   'verdict_stop_code': (v and TM.stop_code(v)), 'verdict_stop_is_ledger_stop': (v and TM.stop_code(v) in TM.LEDGER_STOPS)})


# ───────────────────────── R2 ─────────────────────────
R2_MSGS = {
    'assert': 'cupy_backends.cuda.api.runtime.CUDARuntimeError: cudaErrorAssert: device-side assert triggered',
    'misaligned': 'cupy_backends.cuda.api.driver.CUDADriverError: CUDA_ERROR_MISALIGNED_ADDRESS: misaligned address',
    'launch_failed': 'cupy_backends.cuda.api.driver.CUDADriverError: CUDA_ERROR_LAUNCH_FAILED: unspecified launch failure',
    'invalid_value': 'cupy_backends.cuda.api.runtime.CUDARuntimeError: cudaErrorInvalidValue: invalid argument',
    'illegal_address (대조)': 'cupy_backends.cuda.api.driver.CUDADriverError: CUDA_ERROR_ILLEGAL_ADDRESS: an illegal memory access was encountered',
}


def r2():
    for k, msg in R2_MSGS.items():
        tag = 'R2_' + k.split()[0]
        d, _rc, _so = TM.led_new(tag)
        _rc1, n1, _s1 = TM.led_add(d, 'ladder:P0')
        a = TM.lad_att(tag, TM.world(tag + '_a', dict(TM.PW, faults=[{'do': 'msg_after_mark', 'msg': msg, 'match': {'rj': 'inf'}}])), d, n1)
        res1 = TM.led_result(d, 1) or {}
        rc_add, n2, so_add = TM.led_add(d, 'ladder:P0', resume=1)
        done = None
        if k == 'assert' and n2:
            b = TM.lad_att(tag, TM.world(tag + '_b'), d, n2, base=a['base'])
            done = {'rc': b['rc'], 'status': (b['sum'] or {}).get('status')}
        out('R2', case=k, stop=TM.stop_code(a), cause=res1.get('cause'), side=res1.get('side'), resume_ok=res1.get('resume_ok'),
            resume_add_rc=rc_add, resume_refused=('RESUME_NOT_ALLOWED' in so_add), resume_attempt=done)


# ───────────────────────── R3 ─────────────────────────
def r3():
    d, _rc, _so = TM.led_new('R3')
    _rc1, n1, _s1 = TM.led_add(d, 'ladder:P0')
    orig = RR.read_run
    calls = []

    def boom(*a, **k):
        calls.append(1)
        raise KeyError('probe: chain defect while reading arm (Stop 아닌 예외)')
    RR.read_run = boom
    exc = None
    try:
        TM.lad_att('R3', TM.world('R3_a'), d, n1)
    except KeyError as e:
        exc = repr(e)[:120]
    finally:
        RR.read_run = orig
    f = Path(TM.TD) / 'runs' / 'R3' / 'attempt_1'
    has_summary = (f / 'ladder_summary.json').exists()
    marks = sorted(p.name for p in f.rglob('*.first_result.json'))
    before = TM.led_result(d, 1)
    rc_rec, so_rec = TM.call(['--stage', 'recover', '--out', str(f), '--ledger', str(d)])
    res1 = TM.led_result(d, 1) or {}
    rc_add, n2, so_add = TM.led_add(d, 'ladder:P0', resume=1)
    out('R3', exception=exc, read_run_calls=len(calls), summary_written=has_summary, first_result_marks=len(marks), result_before_recover=before,
        recover_rc=rc_rec, result={k: res1.get(k) for k in ('status', 'side', 'cause', 'resume_ok', 'by')}, resume_add_rc=rc_add, resume_n=n2)


# ───────────────────────── R4 ─────────────────────────
def r4():
    r = TM.s_led_main()
    d, v = r['d'], r['v']
    rc_same, so_same = TM.call(['--stage', 'verdict', '--reverify', str(v['out']), '--root', str(TM.FX['root'])])
    _rc4, n4, s4 = TM.led_add(d, 'ladder:P0:FIBRE')                       # 다른 대상 (감도 사다리) — 항목만
    x = TM.lad_att('LM_P0', TM.world('R4_x'), d, n4, base=r['l0']['base'])   # 변이 인자 없이 = 풀기 전 거부 (같은 바탕 폴더에 attempt_<n4>)
    rc_diff, so_diff = TM.call(['--stage', 'verdict', '--reverify', str(v['out']), '--root', str(TM.FX['root'])])
    import re
    m = re.search(r'멈춤 ([A-Z_]+)', so_diff)
    pub0 = json.loads((Path(v['out']) / 'verdict.json').read_text(encoding='utf-8'))
    lin = pub0.get('ledger_input') or {}
    try:
        RR.ledger_verdict_check(pub0.get('input_dirs') or [], lin.get('path'), lin.get('attempt_dirs') or (), lin.get('commit'))
        why = 'ledger_verdict_check (원 판정 커밋) 통과'
    except RR.Stop as e:
        why = f'{e.code}: {str(e.cause)[:200]}'
    out('R4', verdict_rc=v['rc'], reverify_before_rc=rc_same, reverify_before_same=('REVERIFY_SAME' in so_same), later_attempt_n=n4,
        later_attempt_rc=x['rc'], later_attempt_rejected=(Path(r['l0']['base']) / f'attempt_{n4}' / 'rejected.json').exists(),
        reverify_after_rc=rc_diff, reverify_after_diff=('REVERIFY_DIFF' in so_diff), reverify_stop=(m.group(1) if m else None), why=why)


# ───────────────────────── R5 재실행 시도가 단계 안 관문 (풀기 전) 에서 멈춤 = 재실행 사슬 끝 ─────────────────────────
def r5():
    out_rows = {}
    for tag, kw in (('maxhours_typo', {'max_hours': '3'}), ('machine_typo (대조 · 풀기 전 대조 = 거부 기록)', {'machine': 'gabia'})):
        t = 'R5_' + tag.split()[0]
        d, _rc, _so = TM.led_new(t)
        _rc1, n1, _s1 = TM.led_add(d, 'ladder:P0')
        a = TM.lad_att(t, TM.world(t + '_a', dict(TM.PW, faults=[{'do': 'oom_after_mark', 'match': {'rj': 'inf'}}])), d, n1)
        r1_ = TM.led_result(d, 1) or {}
        _rc2, n2, _s2 = TM.led_add(d, 'ladder:P0', resume=1)
        b = TM.lad_att(t, TM.world(t + '_b'), d, n2, base=a['base'], **kw)       # 실수 하나 (시간 상한 · 기계) — 결과 전
        r2_ = TM.led_result(d, n2) or {}
        rc3, n3, so3 = TM.led_add(d, 'ladder:P0', resume=1)                       # 바른 인자로 다시 재실행하려 함
        c = TM.lad_att(t, TM.world(t + '_c'), d, n3, base=a['base']) if n3 else None
        out_rows[tag] = {'first': {k: r1_.get(k) for k in ('status', 'side', 'cause', 'resume_ok')},
                         'resume_with_typo': {'stop': TM.stop_code(b), 'result': {k: r2_.get(k) for k in ('status', 'side', 'cause', 'resume_ok')}},
                         'second_resume_add_rc': rc3, 'second_resume_refused': ('RESUME_NOT_ALLOWED' in so3),
                         'second_resume_status': (c and (c['sum'] or {}).get('status'))}
    out('R5', **out_rows)


# ───────────────────────── R6 코드 결함 꼴 오류를 본 뒤 사슬 부모를 SIGKILL → recover = parent_dead · 재실행 자격 ─────────────────────────
def r6():
    import os
    import signal as _sig
    msg = 'cupy_backends.cuda.api.driver.CUDADriverError: CUDA_ERROR_ILLEGAL_ADDRESS: an illegal memory access was encountered'
    d, _rc, _so = TM.led_new('R6')
    _rc1, n1, _s1 = TM.led_add(d, 'ladder:P0')
    base = Path(TM.TD) / 'runs' / 'R6'
    w = TM.world('R6_a', dict(TM.PW, faults=[{'do': 'msg_sleep_after_mark', 'msg': msg, 's': 8.0, 'match': {'rj': 'inf'}}]))
    pr = TM.gr_spawn_chain('R6', TM.ladder_argv(base) + ['--ledger', str(d), '--attempt', str(n1)], w)
    logp = base / f'attempt_{n1}' / 'logs' / 'L01_floor.log'
    t_end, seen = time.time() + 30, False
    while time.time() < t_end and not seen:
        try:
            seen = 'CUDA_ERROR_ILLEGAL_ADDRESS' in logp.read_text(encoding='utf-8', errors='replace')
        except OSError:
            pass
        time.sleep(0.05)
    os.kill(pr.pid, _sig.SIGKILL)                         # 운영자가 런 로그의 코드 결함 꼴 오류를 본 뒤 사슬 부모를 끈다
    pr.wait()
    before = TM.led_result(d, 1)
    rc_rec, _so_rec = TM.call(['--stage', 'recover', '--out', str(base / f'attempt_{n1}'), '--ledger', str(d)])
    res1 = TM.led_result(d, 1) or {}
    rc_add, n2, so_add = TM.led_add(d, 'ladder:P0', resume=1)
    b = TM.lad_att('R6', TM.world('R6_b'), d, n2, base=base) if n2 else None
    out('R6', error_seen_in_log=seen, result_before_recover=before, recover_rc=rc_rec,
        result={k: res1.get(k) for k in ('status', 'side', 'cause', 'resume_ok', 'by')}, resume_add_rc=rc_add,
        resume_refused=('RESUME_NOT_ALLOWED' in so_add), resume_status=(b and (b['sum'] or {}).get('status')))


if __name__ == '__main__':
    t0 = time.time()
    setup()
    for nm, fn in (('R1', r1), ('R2', r2), ('R3', r3), ('R4', r4), ('R5', r5), ('R6', r6)):
        if nm in ONLY:
            try:
                fn()
            except Exception as ex:                               # noqa: BLE001
                import traceback
                out(nm, error=f'{type(ex).__name__}: {ex}', tb=traceback.format_exc().splitlines()[-4:])
    out('done', seconds=round(time.time() - t0, 1), td=TM.TD)
