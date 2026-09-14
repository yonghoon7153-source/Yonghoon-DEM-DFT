#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""웹앱 런처 회귀 — **옛 인스턴스를 안 멈추면 새 코드가 영영 안 뜬다**.

★ 재현한 실사고 (2026-09-14):
  런처가 포트를 확인하지 않고 `python3 app.py` 를 또 띄웠다.  포트가 이미 물려 있으면 새
  프로세스는 bind 실패로 죽는데, 준비 검사가 `connect_ex('127.0.0.1',PORT)==0` 만 봐서
  **옛 프로세스 덕분에 즉시 통과**하고 `✓ PID …` 를 찍었다 = 거짓 초록.  사용자는
  "git pull 했고 런처가 ✓ 라는데 새 라우트가 404" 를 보게 된다 (worklog 페이지에서 실제 발생).
  ⇒ 포트 기준으로 **먼저 멈추고** 띄운다.  pid 파일은 낡을 수 있어 믿지 않는다.

  python3 scripts/test_webapp_launcher.py
"""
import os
import socket
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAUNCHER = os.path.join(ROOT, 'scripts', 'run_dem_webapp.sh')

_ok, _fail = 0, []


def chk(name, cond, detail=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}' + (f'   {detail}' if detail else ''))
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'   {detail}' if detail else ''))


def _free_port():
    s = socket.socket()
    s.bind(('127.0.0.1', 0))
    p = s.getsockname()[1]
    s.close()
    return p


def _listening(port):
    s = socket.socket()
    s.settimeout(0.3)
    try:
        return s.connect_ex(('127.0.0.1', port)) == 0
    finally:
        s.close()


def _have_port_tool():
    for cmd in (['ss', '-ltn'], ['lsof', '-v']):
        try:
            subprocess.run(cmd, capture_output=True, timeout=5)
            return True
        except (OSError, subprocess.SubprocessError):
            continue
    return False


def main():
    src = open(LAUNCHER, encoding='utf-8').read()

    # ══ 소스 핀 — 고친 구조가 지워지면 즉시 빨간불 ══
    chk('① 띄우기 직전에 옛 인스턴스를 멈춘다 (_stop_port || exit 1)',
        '_stop_port || exit 1' in src)
    chk('② 준비 루프가 우리 PID 사망 시 즉시 탈출한다 (남의 포트로 통과 금지)',
        'kill -0 "$PID" 2>/dev/null || break' in src)
    chk('③ 포트 소유자를 pid 파일이 아니라 ss/lsof 로 찾는다',
        '_port_pid()' in src and 'ss -ltnp' in src and 'lsof -ti' in src)
    chk('④ --stop 단독 모드가 있다', '--stop) STOP=1' in src and 'if [ "$STOP" = 1 ]' in src)

    # ══ 실동작 — 점유된 포트를 실제로 비우는가 ══
    if not _have_port_tool():
        print('  SKIP  ⑤⑥ 실동작 (ss/lsof 둘 다 없음 — 소스 핀만 검사)')
    else:
        port = _free_port()
        dummy = subprocess.Popen(
            [sys.executable, '-c',
             'import socket,time\n'
             's=socket.socket()\n'
             's.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)\n'
             f's.bind(("127.0.0.1",{port}))\n'
             's.listen(5)\n'
             'time.sleep(120)\n'],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            for _ in range(40):
                if _listening(port):
                    break
                time.sleep(0.1)
            chk('⑤a 더미 리스너가 포트를 점유했다', _listening(port), f'port={port}')

            env = dict(os.environ, PORT=str(port))
            r = subprocess.run(['bash', LAUNCHER, '--stop'], cwd=ROOT, env=env,
                               capture_output=True, text=True, timeout=60)
            freed = not _listening(port)
            chk('⑤ --stop 이 점유된 포트를 실제로 비운다',
                r.returncode == 0 and freed,
                f'rc={r.returncode} freed={freed} · {r.stdout.strip().splitlines()[-1:] }')
            chk('⑤b 점유 프로세스가 종료됐다', dummy.poll() is not None)
        finally:
            if dummy.poll() is None:
                dummy.kill()
                dummy.wait(timeout=10)

        port2 = _free_port()
        env2 = dict(os.environ, PORT=str(port2))
        r2 = subprocess.run(['bash', LAUNCHER, '--stop'], cwd=ROOT, env=env2,
                            capture_output=True, text=True, timeout=60)
        chk('⑥ 빈 포트에 --stop 은 성공적 no-op', r2.returncode == 0,
            f'rc={r2.returncode}')

    print('webapp launcher SELFTEST', 'PASS' if not _fail else 'FAIL ' + repr(_fail))
    return 0 if not _fail else 1


if __name__ == '__main__':
    raise SystemExit(main())
