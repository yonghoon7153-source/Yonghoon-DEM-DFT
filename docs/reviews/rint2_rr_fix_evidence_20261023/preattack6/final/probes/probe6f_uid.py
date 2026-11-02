#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""사전 공격 6 회차 마무리 (11-02) — PC6-01 넓히기 (실제 /proc · 실제 `run_in_group` · 실제 `--stage recover` · root 로 시작해 자식만 uid 65534 (nobody)
로 내린다 · 설치 · 시스템 설정 없음).  중간 보고 탐침 `../../probes/probe6_uid.py` 의 구경꾼 (setresuid = 자격 바꿈 = dumpable 0) 꼴을 그대로 쓴다.

  root 로:  python3 -I docs/reviews/rint2_rr_fix_evidence_20261023/preattack6/final/probes/probe6f_uid.py

R8a 잠깐 사는 구경꾼 — 러너 (bash sleep 2) 끝 무렵 (1.8 s) 에 생겨 0.7 s 만 사는 구경꾼 → 끝 기록 확인? · 러너 끝 → run_in_group 반환까지 걸린 시간
    (group_settle 은 대기 상한 GROUP_GONE_WAIT_S 안에서 다시 보지 않는다?) · 대조 = 구경꾼이 러너 끝 전에 사라짐
R8b "운영자 세션" — 사슬 (uid 65534) 을 런 도중 SIGKILL (러너 그룹 고아 · 끝 기록 없음) → 그 뒤 생긴 구경꾼 S (sshd 세션 꼴) 아래 자식 O (exec · dumpable)
    가 --stage recover → rc? · S 밖 프로세스의 recover (S 삶) → rc? · S 를 끝낸 뒤 recover → rc · 죽인 수
값 · σ 없음.  임시 폴더 = 작업 트리 안 `.pa6f_uid_<pid>` (uid 65534 가 쓸 수 있게 0777 · 끝에 지운다).
"""
import contextlib
import importlib.util
import io
import json
import os
import shutil
import signal
import sys
import time
from pathlib import Path

WT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(WT / 'scripts'))
import rint_r_chain as RR  # noqa: E402

_spec = importlib.util.spec_from_file_location('probe6_uid', Path(__file__).resolve().parents[2] / 'probes' / 'probe6_uid.py')
P6 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(P6)
UID = P6.UID


def out(tag, **kw):
    print(json.dumps(dict(probe=tag, **kw), ensure_ascii=False, sort_keys=True, default=str), flush=True)


def r8a(tmp):
    rows = {}
    for tag, at, life in (('alive_at_end', 1.8, 0.7), ('gone_before_end', 0.5, 0.3)):
        d = tmp / f'R8a_{tag}'
        d.mkdir()
        os.chmod(d, 0o777)
        r, w = os.pipe()
        pid = os.fork()
        if pid == 0:
            os.close(r)
            try:
                P6.drop('full')
                t0 = time.time()
                with open(d / 'log.txt', 'w', encoding='utf-8') as lf:
                    rc, cause, end = RR.run_in_group(['bash', '-c', 'sleep 2'], str(d), dict(os.environ), lf, 60, d / 'groups', 'L01_floor')
                res = {'rc': rc, 'cause': cause, 'confirmed': end.get('confirmed'), 'left': end.get('left'), 'seconds_total': round(time.time() - t0, 2)}
            except BaseException as e:               # noqa: BLE001
                res = {'error': f'{type(e).__name__}: {e}'}
            os.write(w, json.dumps(res, default=str).encode())
            os.close(w)
            os._exit(0)
        os.close(w)
        time.sleep(at)
        b = P6.bystander('full', life)
        buf = b''
        while True:
            x = os.read(r, 65536)
            if not x:
                break
            buf += x
        os.close(r)
        os.waitpid(pid, 0)
        res = json.loads(buf.decode() or '{}')
        time.sleep(life + 0.2)
        alive_after = Path('/proc', str(b)).exists() and (Path('/proc', str(b), 'stat').read_bytes().split(b') ')[1][:1] not in (b'Z', b'X'))
        P6.kill(b)
        rows[tag] = dict(res, bystander_start_s=at, bystander_life_s=life, bystander_alive_after=alive_after,
                         group_gone_wait_s=RR.GROUP_GONE_WAIT_S)
    out('R8a', rows=rows)


def _recover_rc(d):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = RR.main(['--stage', 'recover', '--out', str(d)])
    return {'rc': rc, 'tail': buf.getvalue().strip().splitlines()[-2:]}


SESSION_CHILD = r'''
import contextlib, io, json, sys
sys.path.insert(0, sys.argv[1])
import rint_r_chain as RR
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rc = RR.main(['--stage', 'recover', '--out', sys.argv[2]])
open(sys.argv[3], 'w').write(json.dumps({'rc': rc, 'tail': buf.getvalue().strip().splitlines()[-2:]}))
'''


def session_recover(d, res_path):
    """구경꾼 S (root fork → setresuid 65534 · dumpable 0 · sshd 세션 꼴) 를 띄우고 그 아래 자식 O (fork · exec python = dumpable) 가 recover → (S pid,
    O 결과)."""
    r, w = os.pipe()
    s = os.fork()
    if s == 0:
        os.close(r)
        try:
            env = {k: v for k, v in os.environ.items() if k != RR.GROUP_TOKEN_ENV}
            P6.drop('full')
            o = os.fork()
            if o == 0:
                os.execve(sys.executable, [sys.executable, '-I', '-c', SESSION_CHILD, str(WT / 'scripts'), str(d), str(res_path)], env)
            os.waitpid(o, 0)
            os.write(w, b'1')
            os.close(w)
            time.sleep(60)
        finally:
            os._exit(0)
    os.close(w)
    os.read(r, 1)
    os.close(r)
    return s, json.loads(Path(res_path).read_text(encoding='utf-8'))


def r8b(tmp):
    d = tmp / 'R8b'
    d.mkdir()
    os.chmod(d, 0o777)
    pid = os.fork()
    if pid == 0:
        try:
            P6.drop('full')
            with open(d / 'log.txt', 'w', encoding='utf-8') as lf:
                RR.run_in_group(['bash', '-c', 'sleep 30'], str(d), dict(os.environ), lf, 120, d / 'groups', 'L01_floor')
        finally:
            os._exit(0)
    lp = d / 'groups' / 'L01_floor.launch.json'
    t_end, tok = time.time() + 20, None
    while time.time() < t_end and tok is None:
        try:
            j = json.loads(lp.read_text(encoding='utf-8'))
            tok = j.get('token') if j.get('pid') else None
        except (OSError, ValueError):
            pass
        time.sleep(0.05)
    time.sleep(0.5)
    os.kill(pid, signal.SIGKILL)
    os.waitpid(pid, 0)
    time.sleep(0.3)
    res_path = tmp / 'R8b_session_recover.json'
    s, o_res = session_recover(d, res_path)
    outside = P6.in_child(lambda: _recover_rc(d))
    end_mid = json.loads((d / 'groups' / 'L01_floor.end.json').read_text(encoding='utf-8')) if (d / 'groups' / 'L01_floor.end.json').exists() else None
    P6.kill(s)
    after = P6.in_child(lambda: _recover_rc(d))
    end_fin = json.loads((d / 'groups' / 'L01_floor.end.json').read_text(encoding='utf-8')) if (d / 'groups' / 'L01_floor.end.json').exists() else None
    out('R8b', token_seen=tok is not None, recover_from_session_child=o_res, recover_outside_session_alive=outside,
        end_while_session={k: (end_mid or {}).get(k) for k in ('confirmed', 'by', 'why', 'killed')},
        recover_after_session_gone=after, end_final={k: (end_fin or {}).get(k) for k in ('confirmed', 'by', 'killed')})


def r8c(tmp):
    """가짜 /proc (사슬 PROC_DIR 자리 · uid 65534 로 셈) — 다른 사용자 (root) 프로세스의 stat · status 를 못 읽음 (hidepid=1 꼴 = 폴더는 보이고 안 파일은
    EACCES · 이 컨테이너에서 /proc 를 다시 걸지 않는다 = 꼴만) → group_members ?  대조 = 같은 표에서 stat 를 읽을 수 있음."""
    rows = {}
    for tag, mode in (('stat_unreadable', 0o000), ('stat_readable', 0o644)):
        fp = tmp / f'R8c_{tag}'
        p = fp / '900010'
        p.mkdir(parents=True)
        rest = ['S', '1', '900010', '900010', '0', '-1'] + ['0'] * 13 + ['100'] + ['0'] * 20
        (p / 'stat').write_text('900010 (other) ' + ' '.join(rest) + '\n', encoding='ascii')
        (p / 'status').write_text('Name:\tother\nUid:\t0\t0\t0\t0\n', encoding='ascii')
        (p / 'environ').write_bytes(b'A=1\0')
        for f in ('stat', 'status', 'environ'):
            os.chmod(p / f, mode)
        os.chmod(p, 0o755)
        os.chmod(fp, 0o755)

        def go(fp=fp):
            RR.PROC_DIR = str(fp)
            return {'m': RR.group_members('a' * 32, since=None)}
        rows[tag] = P6.in_child(go)['m']
    out('R8c', rows=rows)


if __name__ == '__main__':
    if os.getuid() != 0:
        print('root 로 돌린다 (자식만 uid 65534 로 내린다)')
        sys.exit(2)
    tmp = WT / f'.pa6f_uid_{os.getpid()}'
    tmp.mkdir()
    os.chmod(tmp, 0o777)
    only = set(sys.argv[1].split(',')) if len(sys.argv) > 1 else {'R8a', 'R8b', 'R8c'}
    try:
        out('env', python=sys.version.split()[0], suid_dumpable=Path('/proc/sys/fs/suid_dumpable').read_text().strip(), kernel=os.uname().release)
        for k, fn in (('R8a', r8a), ('R8b', r8b), ('R8c', r8c)):
            if k in only:
                fn(tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
