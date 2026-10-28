#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""사전 공격 5 회차 (묶음 C · 10-28) — 단위 탐침 (가짜 러너 없음 · 실제 사슬 함수 · 작은 손계산 반례).

  python3 docs/reviews/rint2_rr_fix_evidence_20261023/preattack5/probe_unit.py <임시 폴더>

U1 stop_cause / attempt_result_line — 자원 낱말 표 (RESOURCE_WORDS) 의 일반 클래스 이름 (CUDARuntimeError · CUDADriverError) · LAUNCH_FAILED
U2 recover_group — 같은 machine_id · 다른 boot_id = '재부팅 확인' (살아 있는 표지 프로세스를 그대로 두고 confirmed True)
U3 group_members — 지도자 스레드가 끝난 프로세스 (상태 Z · 다른 스레드는 삶) 를 그룹 원으로 세지 않는다 → run_in_group 확인 True 뒤 늦은 파일
U4 ledger_append — 두 프로세스 동시 덧붙이기 (잠금 없음)
U5 attempt_result_line(s=None) — 단계 요약 없음 = 원인 parent_dead (사슬 예외와 구분 못 함)
값 · σ 없음.  결과 = JSON 한 줄씩 화면.
"""
import json
import multiprocessing as mp
import os
import signal
import subprocess
import sys
import time
import uuid
from pathlib import Path

WT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(WT / 'scripts'))
import rint_r_chain as RR  # noqa: E402

TMP = Path(sys.argv[1] if len(sys.argv) > 1 else '/tmp/pa5_unit').resolve()
TMP.mkdir(parents=True, exist_ok=True)


def out(tag, **kw):
    print(json.dumps(dict(probe=tag, **kw), ensure_ascii=False, sort_keys=True), flush=True)


# ───────────────────────── U1 자원 낱말 ─────────────────────────
def u1():
    msgs = {
        'illegal_address_driver (10-28 고침 · 대조)': 'cupy_backends.cuda.api.driver.CUDADriverError: CUDA_ERROR_ILLEGAL_ADDRESS: an illegal memory access was encountered',
        'device_side_assert_runtime': 'cupy_backends.cuda.api.runtime.CUDARuntimeError: cudaErrorAssert: device-side assert triggered',
        'misaligned_address_driver': 'cupy_backends.cuda.api.driver.CUDADriverError: CUDA_ERROR_MISALIGNED_ADDRESS: misaligned address',
        'illegal_instruction_driver': 'cupy_backends.cuda.api.driver.CUDADriverError: CUDA_ERROR_ILLEGAL_INSTRUCTION: an illegal instruction was encountered',
        'launch_failed_driver': 'cupy_backends.cuda.api.driver.CUDADriverError: CUDA_ERROR_LAUNCH_FAILED: unspecified launch failure',
        'invalid_value_runtime': 'cupy_backends.cuda.api.runtime.CUDARuntimeError: cudaErrorInvalidValue: invalid argument',
        'python_bug (대조)': 'Traceback (most recent call last):\nKeyError: \'sigma\'',
    }
    for nm, msg in msgs.items():
        f = TMP / 'u1' / nm.split()[0] / 'attempt_1'
        (f / 'L01_floor_arm1' / '.unchecked').mkdir(parents=True, exist_ok=True)
        (f / 'L01_floor_arm1' / '.unchecked' / 'p2_SBE_vgcf100_a0.json.first_result.json').write_text('{}\n')   # 표지만 (payload 없음 · 결과 뒤)
        (f / 'logs').mkdir(exist_ok=True)
        (f / 'logs' / 'L01_floor.log').write_text('[p2] run\n' + msg + '\n')
        s = {'status': 'STOPPED', 'stop': {'code': 'RUNNER_RC', 'run': 'L01_floor', 'reason': None},
             'runs': [{'name': 'L01_floor', 'outdir': 'L01_floor_arm1', 'rc': 1, 'group_cause': None}]}
        r = RR.attempt_result_line(1, f, s, 'chain')
        out('U1', case=nm, cause=r['cause'], side=r['side'], resume_ok=r['resume_ok'])


# ───────────────────────── U2 recover_group machine_id ─────────────────────────
def u2():
    tok = os.urandom(16).hex()
    env = dict(os.environ, **{RR.GROUP_TOKEN_ENV: tok})
    p = subprocess.Popen(['sleep', '20'], env=env, start_new_session=True)
    try:
        me = RR.host_ident()
        gdir = TMP / 'u2' / 'groups'
        gdir.mkdir(parents=True, exist_ok=True)
        host = dict(me, boot_id=str(uuid.uuid4()))                 # 같은 machine_id · 다른 boot_id (복제 이미지 · 같은 이미지의 다른 컨테이너 흉내)
        lp = gdir / 'L01_floor.launch.json'
        RR.write_json_atomic(lp, {'schema': RR.GROUP_SCHEMA, 'name': 'L01_floor', 'token': tok, 'pid': p.pid, 'pgid': p.pid, 'argv': ['bash'],
                                  'host': host, 'started_utc': RR._utc(), 'by': 'chain', 'chain_pid': 1})
        members_before = RR.group_members(tok)
        end = RR.recover_group(lp, me)
        alive = p.poll() is None
        out('U2', machine_id_same=host['machine_id'] == me['machine_id'], boot_differs=True, members_before=members_before,
            confirmed=end['confirmed'], why=end['why'], killed=end['killed'], token_process_still_alive=alive)
    finally:
        p.kill()
        p.wait()


# ───────────────────────── U3 지도자 스레드가 끝난 프로세스 ─────────────────────────
U3_CHILD = r'''
import ctypes, os, sys, threading, time
late = sys.argv[1]
def w():
    time.sleep(2.0)
    open(late, "w").write("late %d\n" % os.getpid())
threading.Thread(target=w).start()
time.sleep(0.2)
ctypes.CDLL(None).pthread_exit(None)          # 주 스레드만 끝남 (프로세스는 다른 스레드로 산다)
'''


def u3():
    d = TMP / 'u3'
    d.mkdir(parents=True, exist_ok=True)
    child = d / 'child.py'
    child.write_text(U3_CHILD)
    late = d / 'late.txt'
    runner = d / 'runner.sh'
    runner.write_text(f'#!/bin/bash\n"{sys.executable}" -I "{child}" "{late}" &\nsleep 0.6\nexit 0\n')   # 러너는 rc 0 으로 끝난다
    with open(d / 'log.txt', 'w') as lf:
        rc, cause, end = RR.run_in_group(['bash', str(runner)], str(d), dict(os.environ), lf, 30, d / 'groups', 'U3')
    t_end = time.time()
    time.sleep(3.0)
    out('U3', rc=rc, cause=cause, confirmed=end['confirmed'], left=end['left'], killed=end['killed'],
        late_file_after_confirmed=late.exists(), late_mtime_after_end=(late.exists() and late.stat().st_mtime > t_end))


# ───────────────────────── U4 동시 덧붙이기 ─────────────────────────
def _u4_worker(repo, barrier, q, who):
    try:
        head, raw = RR.ledger_now(repo)
        st = RR.ledger_parse(raw)
        e = {'kind': 'entry', 'n': len(st['entries']) + 1, 'target': 'ladder:P0' if who == 0 else 'ladder:P1', 'machine': f'm{who}',
             'resume_of': None, 'plan_sha256': st['header']['plan_sha256'], 'code_key_sha256': 'c' * 64, 'env': {}, 'bed': {}, 'utc': 'x'}
        barrier.wait()
        c = RR.ledger_append(repo, e, f'entry by {who}', expect=raw)
        q.put((who, 'ok', c))
    except RR.Stop as ex:
        q.put((who, 'stop', f'{ex.code}: {str(ex.cause)[:120]}'))
    except Exception as ex:                                       # noqa: BLE001
        q.put((who, 'exc', f'{type(ex).__name__}: {ex}'))


def u4(trials=12):
    stats = {'both_ok': 0, 'one_ok': 0, 'none_ok': 0, 'ledger_unparseable_after': 0, 'stop_but_line_committed': 0}
    examples = []
    for t in range(trials):
        repo = TMP / 'u4' / f'r{t}'
        repo.mkdir(parents=True, exist_ok=True)
        subprocess.run(['git', 'init', '-q', str(repo)], check=True)
        head = {'kind': 'header', 'schema': RR.LEDGER_SCHEMA, 'plan_sha256': 'a' * 64, 'utc': 'x'}
        (repo / RR.LEDGER_FILE).write_text(RR.ledger_line(head))
        RR.ledger_git(repo, 'add', '--', RR.LEDGER_FILE)
        RR.ledger_git(repo, 'commit', '-q', '-m', 'init', '--', RR.LEDGER_FILE)
        barrier, q = mp.Barrier(2), mp.Queue()
        ps = [mp.Process(target=_u4_worker, args=(repo, barrier, q, w)) for w in (0, 1)]
        for p in ps:
            p.start()
        for p in ps:
            p.join(60)
        res = sorted(q.get() for _ in ps)
        n_ok = sum(1 for r in res if r[1] == 'ok')
        stats[{2: 'both_ok', 1: 'one_ok', 0: 'none_ok'}[n_ok]] += 1
        raw = RR.ledger_git(repo, 'show', f'HEAD:{RR.LEDGER_FILE}').stdout
        try:
            st = RR.ledger_parse(raw)
            committed = sorted(e['machine'] for e in st['entries'].values())
            parse = 'ok'
        except RR.Stop as ex:
            committed, parse = None, f'{ex.code}: {str(ex.cause)[:100]}'
            stats['ledger_unparseable_after'] += 1
        for who, kind, _x in res:
            if kind != 'ok' and committed is not None and f'm{who}' in committed:
                stats['stop_but_line_committed'] += 1
        if len(examples) < 3 and (parse != 'ok' or n_ok != 1 or stats['stop_but_line_committed']):
            examples.append({'trial': t, 'workers': res, 'parse': parse, 'committed_machines': committed,
                             'head_lines': raw.decode('utf-8', 'replace').count('\n')})
    out('U4', trials=trials, **stats, examples=examples)


# ───────────────────────── U5 요약 없는 시도 = parent_dead ─────────────────────────
def u5():
    f = TMP / 'u5' / 'attempt_1'
    (f / 'L01_floor_arm1' / '.unchecked').mkdir(parents=True, exist_ok=True)
    (f / 'L01_floor_arm1' / '.unchecked' / 'p2_SBE_vgcf100_a0.json.first_result.json').write_text('{}\n')
    r = RR.attempt_result_line(1, f, None, 'recover')
    out('U5', status=r['status'], cause=r['cause'], side=r['side'], resume_ok=r['resume_ok'],
        note='요약 없음 (부모 SIGKILL 이든 사슬 프로세스의 Stop 아닌 예외든 같은 줄)')


# ───────────────────────── U6 사슬 부모가 살아 있는데 recover ─────────────────────────
U6_CHAIN = r'''
import os, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import rint_r_chain as RR
d = Path(sys.argv[2])
with open(d / 'log.txt', 'w') as lf:
    rc, cause, end = RR.run_in_group(['bash', '-c', 'sleep 15'], str(d), dict(os.environ), lf, 60, d / 'groups', 'L01_floor')
print('CHAIN_SAW rc=%r cause=%r confirmed=%r by=%r' % (rc, cause, end['confirmed'], end['by']), flush=True)
'''


def u6():
    d = TMP / 'u6'
    (d / 'groups').mkdir(parents=True, exist_ok=True)
    (d / 'chain.py').write_text(U6_CHAIN)
    p = subprocess.Popen([sys.executable, '-I', str(d / 'chain.py'), str(WT / 'scripts'), str(d)], stdout=subprocess.PIPE, text=True)
    lp = d / 'groups' / 'L01_floor.launch.json'
    t_end = time.time() + 20
    while time.time() < t_end:
        try:
            if json.loads(lp.read_text()).get('pid'):
                break
        except (OSError, ValueError):
            pass
        time.sleep(0.05)
    time.sleep(0.5)
    chain_pid = json.loads(lp.read_text()).get('chain_pid')
    chain_alive_at_recover = p.poll() is None
    import contextlib
    import io
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = RR.main(['--stage', 'recover', '--out', str(d)])
    end_by_recover = json.loads((d / 'groups' / 'L01_floor.end.json').read_text())
    chain_out = p.communicate(timeout=90)[0].strip()
    end_final = json.loads((d / 'groups' / 'L01_floor.end.json').read_text())
    out('U6', chain_pid_recorded=chain_pid == p.pid, chain_alive_at_recover=chain_alive_at_recover, recover_rc=rc,
        recover_end={k: end_by_recover.get(k) for k in ('by', 'cause', 'confirmed', 'killed')}, chain_saw=chain_out,
        end_final={k: end_final.get(k) for k in ('by', 'cause', 'rc', 'confirmed')})


# ───────────────────────── U7 덧붙임 뒤 커밋 실패 = 커밋 안 된 줄이 남는다 ─────────────────────────
def u7():
    repo = TMP / 'u7' / 'r'
    repo.mkdir(parents=True, exist_ok=True)
    subprocess.run(['git', 'init', '-q', str(repo)], check=True)
    head = {'kind': 'header', 'schema': RR.LEDGER_SCHEMA, 'plan_sha256': 'a' * 64, 'utc': 'x'}
    (repo / RR.LEDGER_FILE).write_text(RR.ledger_line(head))
    RR.ledger_git(repo, 'add', '--', RR.LEDGER_FILE)
    RR.ledger_git(repo, 'commit', '-q', '-m', 'init', '--', RR.LEDGER_FILE)
    e = {'kind': 'entry', 'n': 1, 'target': 'ladder:P0', 'machine': 'kgy', 'resume_of': None, 'plan_sha256': 'a' * 64,
         'code_key_sha256': 'c' * 64, 'env': {}, 'bed': {}, 'utc': 'x'}
    lock = repo / '.git' / 'index.lock'
    lock.write_text('')                                         # 다른 git 프로세스가 잡은 꼴 (동시 사용 · 끊긴 git)
    try:
        RR.ledger_append(repo, e, 'entry (probe)')
        first = 'ok'
    except RR.Stop as ex:
        first = f'{ex.code}: {str(ex.cause)[:90]}'
    lock.unlink()
    dirty = RR.ledger_git(repo, 'status', '--porcelain').stdout.decode().strip()
    try:
        RR.ledger_now(repo)
        after = 'ok'
    except RR.Stop as ex:
        after = f'{ex.code}: {str(ex.cause)[:90]}'
    out('U7', append_with_lock=first, working_tree_after=dirty, next_ledger_read=after)


# ───────────────────────── U8 시간 초과 때 payload 원자적 쓰기 (.part) 가 남은 꼴 = '검사 실패 흔적' ─────────────────────────
def u8():
    rows = []
    for nm, files in (('marker_only (대조)', ['p2_SBE_vgcf100_a0.json.first_result.json']),
                      ('part_file (쓰는 중 죽음)', ['p2_SBE_vgcf100_a0.json.first_result.json', 'p2_SBE_vgcf100_a0.json.part']),
                      ('payload_before_runner_check (검사 전 죽음)', ['p2_SBE_vgcf100_a0.json.first_result.json', 'p2_SBE_vgcf100_a0.json'])):
        f = TMP / 'u8' / nm.split()[0] / 'attempt_1'
        u = f / 'L01_floor_arm1' / '.unchecked'
        u.mkdir(parents=True, exist_ok=True)
        for x in files:
            (u / x).write_text('{}\n')
        s = {'status': 'STOPPED', 'stop': {'code': 'TIME_LIMIT', 'run': 'L01_floor', 'reason': None},
             'runs': [{'name': 'L01_floor', 'outdir': 'L01_floor_arm1', 'rc': None, 'group_cause': 'timeout'}]}
        r = RR.attempt_result_line(1, f, s, 'chain')
        rows.append({'case': nm, 'cause': r['cause'], 'side': r['side'], 'resume_ok': r['resume_ok']})
    out('U8', rows=rows)


if __name__ == '__main__':
    only = set(sys.argv[2].split(',')) if len(sys.argv) > 2 else {'U1', 'U2', 'U3', 'U4', 'U5', 'U6', 'U7', 'U8'}
    for nm, fn in (('U1', u1), ('U2', u2), ('U3', u3), ('U4', u4), ('U5', u5), ('U6', u6), ('U7', u7), ('U8', u8)):
        if nm in only:
            try:
                fn()
            except Exception as ex:                               # noqa: BLE001
                out(nm, error=f'{type(ex).__name__}: {ex}')
