#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""사전 공격 6 회차 (10-30 · 대상 4c69070ad) — 실경로 탐침 (사슬 `rint_r_chain.main` · 가짜 러너 (bash + 파이썬) · 실제 프로세스 그룹 · 실제 git 원장).

시험 틀 = `scripts/test_rint_r_chain.py` 의 고정물 · 가짜 러너를 **그대로** 불러 쓴다 (시험 파일 · 사슬은 고치지 않는다 · 가짜 러너의 기존 고장
`msg_sleep_after_mark` · `msg_after_mark` 만 쓴다).

  python3 -I docs/reviews/rint2_rr_fix_evidence_20261023/preattack6/probes/probe6_real.py <임시 폴더 바탕> [R1,R1c,R2,R3,R4]

R1  표지 뒤 러너 로그 = cupy 꼴 CUDA_ERROR_LAUNCH_FAILED (1저자 Q2 = 자동 재실행 없음 부류) → 사슬 부모 SIGKILL → recover --ledger →
    결과 줄 원인 · 재실행 자격 → --add --resume 1 → 재실행 시도 → 채택 사슬 · 원장 판정 대조
R1c 대조 — 같은 줄 · 사슬 산 채 러너 rc 1 (PC04 와 같은 꼴) → runner_rc · --add --resume 거부
R2  같은 줄 뒤 사슬이 SIGTERM (기다림 중) → 결과 줄 원인 · 재실행 자격 → --add --resume
R3  운영자 중단 신호 셋 (러너 기다림 중 · 로그 = 보통 줄) — SIGINT (Ctrl-C) · SIGTERM · SIGKILL → (recover) 결과 줄 원인 · 재실행 자격
R4  원장 덧붙임 중 신호 (git commit 직전) — SIGTERM · SIGHUP · SIGKILL · SIGINT → 원장 작업 파일 · 다음 --add (등록 R §10-5 아 ⑧
    "git add · commit 실패 (index.lock · 신호) = 작업 파일 · 색인을 읽은 판으로 되돌린다")
값 · σ 를 찍지 않는다.
"""
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

WT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(WT / 'scripts'))
import rint_r_chain as RR  # noqa: E402
import test_rint_r_chain as TM  # noqa: E402

BASE = Path(sys.argv[1] if len(sys.argv) > 1 else tempfile.gettempdir()).resolve()
BASE.mkdir(parents=True, exist_ok=True)
ONLY = set(sys.argv[2].split(',')) if len(sys.argv) > 2 else {'R1', 'R1c', 'R2', 'R3', 'R4'}
LAUNCH = 'cupy_backends.cuda.api.driver.CUDADriverError: CUDA_ERROR_LAUNCH_FAILED: unspecified launch failure'
PLAIN = '[p2] solving (probe · 보통 줄)'

#: SIGINT 를 파이썬 기본 처리 (KeyboardInterrupt) 로 둔 사슬 구동기 — 터미널에서 돌린 사슬과 같은 꼴 (배경 작업이 SIGINT 를 물려받아 무시하는 일을 없앤다)
DRIVER = r'''
import json, os, signal, sys
from pathlib import Path
signal.signal(signal.SIGINT, signal.default_int_handler)
cfg = json.load(open(sys.argv[1], encoding='utf-8'))
sys.path.insert(0, cfg['scripts'])
import rint_r_chain as RR
RR.HERE = Path(cfg['here'])
os.environ.update(cfg['env'])
sys.exit(RR.main(cfg['argv']))
'''


def out(tag, **kw):
    print(json.dumps(dict(probe=tag, **kw), ensure_ascii=False, sort_keys=True, default=str), flush=True)


def setup():
    TM.RR = RR
    TM.TD = tempfile.mkdtemp(prefix='pa6_real_', dir=str(BASE))
    TM.fixtures()


def spawn(tag, argv, wpath):
    drv = Path(TM.TD) / 'pa6_driver.py'
    if not drv.exists():
        drv.write_text(DRIVER, encoding='utf-8')
    cfg = Path(TM.TD) / f'{tag}_cfg.json'
    cfg.write_text(json.dumps({'scripts': str(WT / 'scripts'), 'here': str(RR.HERE), 'env': {'FAKE_WORLD': str(wpath)},
                               'argv': [str(a) for a in argv]}), encoding='utf-8')
    log = open(Path(TM.TD) / f'{tag}_chain.log', 'w', encoding='utf-8')
    return subprocess.Popen([sys.executable, '-I', str(drv), str(cfg)], stdout=log, stderr=subprocess.STDOUT, start_new_session=True)


def wait_text(p, needle, t=30.0):
    t_end = time.time() + t
    while time.time() < t_end:
        try:
            if needle in Path(p).read_text(encoding='utf-8', errors='replace'):
                return True
        except OSError:
            pass
        time.sleep(0.05)
    return False


def kill_after(tag, msg, sig, s=8.0):
    """사다리 시도 하나를 따로 프로세스로 · 표지 뒤 msg 를 찍고 s 초 자는 러너 · 그 줄을 본 뒤 사슬 부모에 sig → (원장, 번호, 바탕, 사슬 rc, 그 줄 봄)."""
    d, _rc, _so = TM.led_new(tag)
    _r, n1, _s = TM.led_add(d, 'ladder:P0')
    base = Path(TM.TD) / 'runs' / tag
    w = TM.world(tag, dict(TM.PW, faults=[{'do': 'msg_sleep_after_mark', 'msg': msg, 's': s, 'match': {'rj': 'inf'}}]))
    pr = spawn(tag, TM.ladder_argv(base) + ['--ledger', str(d), '--attempt', str(n1)], w)
    seen = wait_text(base / f'attempt_{n1}' / 'logs' / 'L01_floor.log', 'CUDA_ERROR_LAUNCH_FAILED' if 'LAUNCH' in msg else 'solving (probe')
    time.sleep(0.2)
    os.kill(pr.pid, sig)
    try:
        rc = pr.wait(timeout=90)
    except subprocess.TimeoutExpired:
        os.kill(pr.pid, signal.SIGKILL)
        rc = pr.wait()
    return d, n1, base, rc, seen, w


def r1():
    d, n1, base, rc, seen, w = kill_after('R1', LAUNCH, signal.SIGKILL)
    before = TM.led_result(d, n1)
    rc_rec, so_rec = TM.call(['--stage', 'recover', '--out', str(base / f'attempt_{n1}'), '--ledger', str(d)], w)
    r1_ = TM.pc_res(d, n1)
    rc_add, n2, so_add = TM.led_add(d, 'ladder:P0', resume=n1)
    b = TM.lad_att('R1', TM.world('R1_b'), d, n2, base=base) if n2 else None
    ad = RR.adoption(RR.ledger_parse(TM.led_raw(d)), 'ladder:P0')
    v = TM.ver_led('R1_v', [b['out']], d) if b else None
    out('R1', seen=seen, chain_rc=rc, result_before_recover=before, recover_rc=rc_rec, result=r1_, add_resume_rc=rc_add,
        add_tail=so_add.strip().splitlines()[-1][:160] if so_add else None, resume_rc=(b or {}).get('rc'),
        resume_status=((b or {}).get('sum') or {}).get('status'), chain=ad.get('chain'), effective=ad.get('effective'),
        verdict_stop=(TM.stop_code(v) if v else None), verdict_ledger_stop=(TM.stop_code(v) in TM.LEDGER_STOPS) if v else None)


def r1c():
    d, _rc, _so = TM.led_new('R1c')
    _r, n1, _s = TM.led_add(d, 'ladder:P0')
    a = TM.lad_att('R1c', TM.world('R1c', dict(TM.PW, faults=[{'do': 'msg_after_mark', 'msg': LAUNCH, 'match': {'rj': 'inf'}}])), d, n1)
    rc_add, n2, so_add = TM.led_add(d, 'ladder:P0', resume=n1)
    out('R1c', stop=TM.stop_code(a), result=TM.pc_res(d, n1), add_resume_rc=rc_add, refused='RESUME_NOT_ALLOWED' in so_add)


def r2():
    import threading
    d, _rc, _so = TM.led_new('R2')
    _r, n1, _s = TM.led_add(d, 'ladder:P0')
    logp = Path(TM.TD) / 'runs' / 'R2' / f'attempt_{n1}' / 'logs' / 'L01_floor.log'

    def fire():
        wait_text(logp, 'CUDA_ERROR_LAUNCH_FAILED', 15.0)
        time.sleep(0.2)
        os.kill(os.getpid(), signal.SIGTERM)
    th = threading.Thread(target=fire)
    th.start()
    a = TM.lad_att('R2', TM.world('R2_a', dict(TM.PW, faults=[{'do': 'msg_sleep_after_mark', 'msg': LAUNCH, 's': 8.0, 'match': {'rj': 'inf'}}])), d, n1)
    th.join()
    rc_add, n2, so_add = TM.led_add(d, 'ladder:P0', resume=n1)
    out('R2', stop=TM.stop_code(a), result=TM.pc_res(d, n1), add_resume_rc=rc_add,
        add_tail=so_add.strip().splitlines()[-1][:160] if so_add else None)


def r3():
    rows = {}
    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGKILL):
        tag = f'R3_{sig.name}'
        d, n1, base, rc, seen, w = kill_after(tag, PLAIN, sig)
        before = TM.led_result(d, n1)
        rec = None
        if before is None:
            rec = TM.call(['--stage', 'recover', '--out', str(base / f'attempt_{n1}'), '--ledger', str(d)], w)[0]
        rc_add, _n2, so_add = TM.led_add(d, 'ladder:P0', resume=n1)
        rows[sig.name] = {'seen': seen, 'chain_rc': rc, 'result_by_chain': before is not None, 'recover_rc': rec, 'result': TM.pc_res(d, n1),
                          'add_resume_rc': rc_add}
    out('R3', rows=rows)


CHILD = r'''
import json, os, signal, sys, time
from pathlib import Path
cfg = json.load(open(sys.argv[1], encoding='utf-8'))
sys.path.insert(0, cfg['scripts'])
import rint_r_chain as RR
RR.HERE = Path(cfg['here'])
signal.signal(signal.SIGINT, signal.default_int_handler)
sig = getattr(signal, cfg['sig'])
orig = RR.ledger_git
def g(repo, *args, check=True):
    if args and args[0] == 'commit':
        os.kill(os.getpid(), sig)
        time.sleep(2.0)
    return orig(repo, *args, check=check)
RR.ledger_git = g
sys.exit(RR.main(cfg['argv']))
'''


def r4():
    rows = {}
    drv = Path(TM.TD) / 'pa6_r4_child.py'
    drv.write_text(CHILD, encoding='utf-8')
    for sg in ('SIGTERM', 'SIGHUP', 'SIGKILL', 'SIGINT'):
        d, _rc, _so = TM.led_new(f'R4_{sg}')
        argv = ['--stage', 'ledger', '--ledger', str(d), '--add', '--ledger-target', 'ladder:P0', '--machine', TM.MACH, '--plan', str(TM.FX['plan']),
                '--runner', str(TM.FX['runner']), '--root', str(TM.FX['root'])]
        cfg = Path(TM.TD) / f'R4_{sg}.json'
        cfg.write_text(json.dumps({'scripts': str(WT / 'scripts'), 'here': str(RR.HERE), 'sig': sg, 'argv': argv}), encoding='utf-8')
        p = subprocess.run([sys.executable, '-I', str(drv), str(cfg)], capture_output=True, text=True, timeout=120)
        porcelain = TM.git_(d, 'status', '--porcelain')
        rows_tail = (p.stdout.strip().splitlines() or [''])[-1][:140]
        try:
            RR.ledger_now(d)
            now = 'ok'
        except RR.Stop as e:
            now = f'{e.code}: {e.cause[:90]}'
        rc_add, n_add, so_add = TM.led_add(d, 'ladder:P0')
        rows[sg] = {'child_rc': p.returncode, 'child_tail': rows_tail, 'git_status_porcelain': porcelain, 'ledger_now': now, 'next_add_rc': rc_add,
                    'next_add_n': n_add,
                    'next_add_tail': (so_add.strip().splitlines() or [''])[-1][:140]}
    out('R4', rows=rows)


if __name__ == '__main__':
    setup()
    out('env', python=sys.version.split()[0], td=TM.TD)
    for k, fn in (('R1', r1), ('R1c', r1c), ('R2', r2), ('R3', r3), ('R4', r4)):
        if k in ONLY:
            t0 = time.time()
            try:
                fn()
            except Exception as e:                       # noqa: BLE001 — 탐침 실패 = 기록
                import traceback
                out(k, error=f'{type(e).__name__}: {e}', tb=traceback.format_exc()[-1500:])
            out(k + '_t', seconds=round(time.time() - t0, 1))
