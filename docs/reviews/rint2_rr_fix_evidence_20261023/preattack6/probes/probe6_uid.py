#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""사전 공격 6 회차 (10-30 · 대상 4c69070ad) — PC5-07 그룹 원 찾기의 "environ 을 못 읽는 같은 실 uid 프로세스 = 미확인" 실측 (실제 /proc · 실제
`run_in_group` · 실제 `--stage recover` · root 로 시작해 자식만 uid 65534 (nobody) 로 내린다 · 설치 · 시스템 설정 없음).

  sudo 없이 root 로:  python3 -I docs/reviews/rint2_rr_fix_evidence_20261023/preattack6/probes/probe6_uid.py

구경꾼 프로세스 (그룹과 무관 · 표지 env 없음) 두 꼴 — 사슬과 같은 실 uid (65534) 이고 environ 을 그 uid 가 못 읽는다:
  ssh 꼴  = root 프로세스가 setresuid(65534,65534,65534) (sshd 권한 분리 자식 `sshd: user@pts/N` · `@notty` 의 꼴 — 자격 바꿈 = dumpable 0)
  suid 꼴 = 실 uid 65534 · 유효 uid 0 (setuid-root 프로그램을 사용자가 띄운 꼴 — sudo · su · passwd · (옛) ping 의 프로세스 자격)
U1 group_members (실 /proc · uid 65534 로 셈) — 구경꾼이 그룹 시작 뒤에 생김 · 그 전에 생김 · 없음
U2 run_in_group (uid 65534 · 러너 = bash sleep 4 · rc 0) 도중 1.5 s 에 구경꾼이 생김 → 끝 기록 확인 · 남음 · 원인 · rc / 대조 = 구경꾼 없음
U3 U2 의 단계 폴더에 --stage recover (uid 65534 · 사슬 부모 = 죽음) — 구경꾼이 살아 있을 때 · 죽인 뒤
값 · σ 없음.  임시 폴더 = 작업 트리 안 `.pa6_uid_<pid>` (uid 65534 가 쓸 수 있게 0777 · 끝에 지운다).
"""
import json
import os
import shutil
import signal
import sys
import time
from pathlib import Path

WT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(WT / 'scripts'))
import rint_r_chain as RR  # noqa: E402

UID = 65534
CLK = os.sysconf('SC_CLK_TCK')


def out(tag, **kw):
    print(json.dumps(dict(probe=tag, **kw), ensure_ascii=False, sort_keys=True, default=str), flush=True)


def drop(kind='full'):
    os.setgroups([])
    os.setresgid(UID, UID, UID)
    if kind == 'full':
        os.setresuid(UID, UID, UID)
    else:                                            # suid 꼴 — 실 uid = 사용자 · 유효 · 저장 uid = root
        os.setresuid(UID, 0, 0)


AGENT = ('import ctypes, os, sys, time\n'
         'ctypes.CDLL(None).prctl(4, 0, 0, 0, 0)\n'          # PR_SET_DUMPABLE = 4 · 0 (ssh-agent · gpg-agent 가 하는 것)
         'os.write(int(sys.argv[1]), b"1"); os.close(int(sys.argv[1]))\n'
         'time.sleep(float(sys.argv[2]))\n')


def bystander(kind, secs):
    """구경꾼 (fork · 표지 env 없음 · secs 초 산다) → pid.  kind = full (ssh 꼴) · suid (setuid 꼴) · agent (uid 65534 로 exec 한 뒤
    prctl(PR_SET_DUMPABLE, 0) — ssh-agent 꼴)."""
    r, w = os.pipe()
    pid = os.fork()
    if pid == 0:
        os.close(r)
        try:
            env = {k: v for k, v in os.environ.items() if k != RR.GROUP_TOKEN_ENV}
            os.environ.clear()
            os.environ.update(env)
            if kind == 'agent':
                drop('full')
                os.set_inheritable(w, True)
                os.execv(sys.executable, [sys.executable, '-I', '-c', AGENT, str(w), str(secs)])
            drop(kind)
            os.write(w, b'1')
        finally:
            os.close(w)
        time.sleep(secs)
        os._exit(0)
    os.close(w)
    os.read(r, 1)
    os.close(r)
    return pid


def in_child(fn):
    """uid 65534 자식에서 fn() → JSON 결과 (파이프)."""
    r, w = os.pipe()
    pid = os.fork()
    if pid == 0:
        os.close(r)
        try:
            drop('full')
            res = fn()
        except BaseException as e:                   # noqa: BLE001
            res = {'error': f'{type(e).__name__}: {e}'}
        os.write(w, json.dumps(res, default=str).encode())
        os.close(w)
        os._exit(0)
    os.close(w)
    buf = b''
    while True:
        b = os.read(r, 65536)
        if not b:
            break
        buf += b
    os.close(r)
    os.waitpid(pid, 0)
    return json.loads(buf.decode() or '{}')


def kill(pid):
    try:
        os.kill(pid, signal.SIGKILL)
        os.waitpid(pid, 0)
    except (ProcessLookupError, ChildProcessError):
        pass


def u1():
    tok = os.urandom(16).hex()
    rows = {}
    since_before = RR.boot_ticks() - 2 * CLK
    for kind in ('full', 'suid', 'agent'):
        time.sleep(0.05)
        b = bystander(kind, 8)
        st = (Path('/proc') / str(b) / 'status').read_text().splitlines()
        uid_line = [x for x in st if x.startswith('Uid:')][0].split()[1:]
        rd = in_child(lambda: {'read': _try_read(b)})
        rows[kind] = {'bystander_uids(r,e,s,fs)': uid_line, 'uid65534_reads_its_environ': rd.get('read'),
                      'group_members_since_before': in_child(lambda: {'m': RR.group_members(tok, since=since_before)})['m'],
                      'group_members_since_after': in_child(lambda: {'m': RR.group_members(tok, since=RR.boot_ticks() + CLK)})['m']}
        kill(b)
    rows['no_bystander'] = in_child(lambda: {'m': RR.group_members(tok, since=since_before)})['m']
    out('U1', rows=rows)


def _try_read(pid):
    try:
        (Path('/proc') / str(pid) / 'environ').read_bytes()
        return 'ok'
    except OSError as e:
        return f'{type(e).__name__} errno {e.errno}'


def run_group(d, name, with_bystander, kind='full'):
    """uid 65534 자식이 run_in_group (bash sleep 4) · 부모 (root) 가 1.5 s 에 구경꾼을 띄운다 → (결과, 구경꾼 pid | None)."""
    r, w = os.pipe()
    pid = os.fork()
    if pid == 0:
        os.close(r)
        try:
            drop('full')
            with open(d / f'{name}.log', 'w', encoding='utf-8') as lf:
                rc, cause, end = RR.run_in_group(['bash', '-c', 'sleep 4'], str(d), dict(os.environ), lf, 60, d / 'groups', name)
            res = {'rc': rc, 'cause': cause, 'confirmed': end.get('confirmed'), 'left': end.get('left'), 'killed': end.get('killed')}
        except BaseException as e:                   # noqa: BLE001
            res = {'error': f'{type(e).__name__}: {e}'}
        os.write(w, json.dumps(res, default=str).encode())
        os.close(w)
        os._exit(0)
    os.close(w)
    b = None
    if with_bystander:
        time.sleep(1.5)
        b = bystander(kind, 40)
    buf = b''
    while True:
        x = os.read(r, 65536)
        if not x:
            break
        buf += x
    os.close(r)
    os.waitpid(pid, 0)
    return json.loads(buf.decode() or '{}'), b


def u2_u3(tmp):
    rows = {}
    for kind in ('full', 'suid'):
        d = tmp / f'U2_{kind}'
        d.mkdir()
        os.chmod(d, 0o777)
        res, b = run_group(d, 'L01_floor', True, kind)
        end_disk = json.loads((d / 'groups' / 'L01_floor.end.json').read_text(encoding='utf-8'))
        rec_alive = in_child(lambda: _recover(d))
        end_after = json.loads((d / 'groups' / 'L01_floor.end.json').read_text(encoding='utf-8'))
        kill(b)
        rec_dead = in_child(lambda: _recover(d))
        end_final = json.loads((d / 'groups' / 'L01_floor.end.json').read_text(encoding='utf-8'))
        rows[kind] = {'run_in_group': res, 'end_on_disk': {k: end_disk.get(k) for k in ('rc', 'cause', 'confirmed', 'left', 'by')},
                      'recover_while_bystander_alive': rec_alive, 'end_after_recover1': {k: end_after.get(k) for k in ('confirmed', 'by', 'why')},
                      'recover_after_bystander_killed': rec_dead, 'end_final': {k: end_final.get(k) for k in ('confirmed', 'by')}}
    d = tmp / 'U2_control'
    d.mkdir()
    os.chmod(d, 0o777)
    res, _b = run_group(d, 'L01_floor', False)
    rows['control_no_bystander'] = {'run_in_group': res}
    out('U2_U3', rows=rows)


def _recover(d):
    import contextlib
    import io
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = RR.main(['--stage', 'recover', '--out', str(d)])
    return {'rc': rc, 'tail': buf.getvalue().strip().splitlines()[-2:]}


if __name__ == '__main__':
    if os.getuid() != 0:
        print('root 로 돌린다 (자식만 uid 65534 로 내린다)')
        sys.exit(2)
    tmp = WT / f'.pa6_uid_{os.getpid()}'
    tmp.mkdir()
    os.chmod(tmp, 0o777)
    try:
        out('env', python=sys.version.split()[0], suid_dumpable=Path('/proc/sys/fs/suid_dumpable').read_text().strip(),
            kernel=os.uname().release)
        u1()
        u2_u3(tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
