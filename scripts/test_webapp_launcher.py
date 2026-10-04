#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""웹앱 런처 회귀 — **옛 인스턴스를 안 멈추면 새 코드가 영영 안 뜬다**.

★ 재현한 실사고 (2026-09-14):
  런처가 포트를 확인하지 않고 `python3 app.py` 를 또 띄웠다.  포트가 이미 물려 있으면 새
  프로세스는 bind 실패로 죽는데, 준비 검사가 `connect_ex('127.0.0.1',PORT)==0` 만 봐서
  **옛 프로세스 덕분에 즉시 통과**하고 `✓ PID …` 를 찍었다 = 거짓 초록.  사용자는
  "git pull 했고 런처가 ✓ 라는데 새 라우트가 404" 를 보게 된다 (worklog 페이지에서 실제 발생).
  ⇒ 포트 기준으로 **먼저 멈추고** 띄운다.  pid 파일은 낡을 수 있어 믿지 않는다.

★★ 재현한 실사고 (2026-10-04 · 원장 `SELF-83`):
  위 수리가 포트 주인을 **확인하지 않고** 껐다.  내가 1저자에게 다른 포트로 두 번째 인스턴스를 띄우는 명령을 줬는데,
  그 포트를 1저자의 **다른 웹 서비스**가 쓰고 있었고 런처가 그것을 꺼 버렸다.  게다가 `--bg` 의 로그 · pid 파일 이름이
  포트와 무관해 같은 데이터 폴더의 기존 인스턴스 로그를 덮을 수 있었다.
  ⇒ ⑤ DEM 웹앱 체크아웃에서 뜬 `app.py` 만 끈다 (cwd = <리포>/webapp · app.py · ../scripts/run_dem_webapp.sh) ·
    ⑦ 그 밖의 프로세스는 **끄지 않고 멈춘다** (--stop · 띄우기 둘 다) · ⑧ 로그 · pid 파일 = 포트별 (기본 포트 5002 만 옛 이름) ·
    ⑨ 실제 --bg 기동이 포트별 파일을 쓰고 옛 로그를 건드리지 않는다.
  ⚠ 이 시험은 **빈 포트만** 쓴다 (`_free_port`) — 실제로 쓰는 포트 (5002 등) 에 리스너를 띄우거나 --stop 하지 않는다.
    ⑧ 의 5002 는 `--print-paths` (경로만 찍고 끝 — 포트를 보지 않는다) 로만 잰다.

  python3 scripts/test_webapp_launcher.py
"""
import os
import shutil
import socket
import subprocess
import sys
import tempfile
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
    chk('⑩ 끄기 전에 주인을 확인한다 (_is_dem_webapp · 실패면 멈춤)', '_is_dem_webapp' in src and 'DEM 웹앱이 아닌' in src)

    # ══ ⑧ 포트별 로그 · pid 경로 (포트를 보지 않는 --print-paths) ══
    with tempfile.TemporaryDirectory() as data:
        def paths(port):
            r = subprocess.run(['bash', LAUNCHER, '--print-paths'], cwd=ROOT,
                               env=dict(os.environ, PORT=str(port), DEM_WEB_DATA=data),
                               capture_output=True, text=True, timeout=60)
            kv = dict(ln.split('=', 1) for ln in r.stdout.splitlines() if ln.startswith(('LOG=', 'PID=')))
            return r.returncode, kv
        rc0, kv0 = paths(5002)
        pX = _free_port()
        rcX, kvX = paths(pX)
        chk('⑧a 기본 포트 5002 = 옛 이름 (dem_webapp.log · .pid — 1저자 습관 · alias 유지)',
            rc0 == 0 and kv0.get('LOG') == os.path.join(data, 'webapp', 'dem_webapp.log')
            and kv0.get('PID') == os.path.join(data, 'webapp', 'dem_webapp.pid'), f'rc={rc0} {kv0}')
        chk('⑧b 다른 포트 = 포트 꼬리 (dem_webapp_<포트>.log · .pid — 같은 데이터 폴더의 두 인스턴스가 서로 덮지 않는다)',
            rcX == 0 and kvX.get('LOG') == os.path.join(data, 'webapp', f'dem_webapp_{pX}.log')
            and kvX.get('PID') == os.path.join(data, 'webapp', f'dem_webapp_{pX}.pid'), f'rc={rcX} {kvX}')

    if not _have_port_tool():
        print('  SKIP  ⑤⑥⑦⑨ 실동작 (ss/lsof 둘 다 없음 — 소스 핀 · 경로만 검사)')
    else:
        procs = []
        tmp = tempfile.mkdtemp(prefix='dem_launcher_test_')
        try:
            # 가짜 DEM 체크아웃 = <tmp>/fake/{webapp/app.py, scripts/run_dem_webapp.sh (이 런처의 사본)}
            fake = os.path.join(tmp, 'fake')
            os.makedirs(os.path.join(fake, 'webapp'))
            os.makedirs(os.path.join(fake, 'scripts'))
            shutil.copy(LAUNCHER, os.path.join(fake, 'scripts', 'run_dem_webapp.sh'))
            with open(os.path.join(fake, 'webapp', 'app.py'), 'w') as f:
                f.write('import os, socket, time\n'
                        'if __name__ == "__main__":\n'
                        '    s = socket.socket(); s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)\n'
                        '    s.bind(("127.0.0.1", int(os.environ["PORT"]))); s.listen(5)\n'
                        '    print("fake dem app up", flush=True); time.sleep(120)\n')
            fake_launcher = os.path.join(fake, 'scripts', 'run_dem_webapp.sh')

            def listener(port, cwd, argv):
                p = subprocess.Popen(argv, cwd=cwd, env=dict(os.environ, PORT=str(port)),
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                procs.append(p)
                for _ in range(50):
                    if _listening(port):
                        break
                    time.sleep(0.1)
                return p

            # ⑤ DEM 웹앱 (가짜 체크아웃에서 뜬 app.py) → --stop 이 비운다
            p5 = _free_port()
            d5 = listener(p5, os.path.join(fake, 'webapp'), [sys.executable, 'app.py'])
            chk('⑤a DEM 웹앱 더미가 포트를 점유했다', _listening(p5), f'port={p5}')
            r = subprocess.run(['bash', LAUNCHER, '--stop'], cwd=ROOT, env=dict(os.environ, PORT=str(p5)),
                               capture_output=True, text=True, timeout=60)
            freed = not _listening(p5)
            chk('⑤ --stop 이 DEM 웹앱이 쥔 포트를 비운다', r.returncode == 0 and freed,
                f'rc={r.returncode} freed={freed} · {r.stdout.strip().splitlines()[-1:]}')
            time.sleep(0.3)
            chk('⑤b DEM 웹앱 더미가 종료됐다', d5.poll() is not None)

            # ⑦ DEM 웹앱이 아닌 프로세스 (다른 서비스 흉내 — cwd 에 app.py · ../scripts/run_dem_webapp.sh 없음) → 끄지 않는다
            other = os.path.join(tmp, 'other_service')
            os.makedirs(other)
            p7 = _free_port()
            d7 = listener(p7, other, [sys.executable, '-c',
                                      'import os,socket,time\n'
                                      's=socket.socket(); s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)\n'
                                      's.bind(("127.0.0.1", int(os.environ["PORT"]))); s.listen(5); time.sleep(120)\n'])
            chk('⑦a 다른 서비스 더미가 포트를 점유했다', _listening(p7), f'port={p7}')
            r7 = subprocess.run(['bash', LAUNCHER, '--stop'], cwd=ROOT, env=dict(os.environ, PORT=str(p7)),
                                capture_output=True, text=True, timeout=60)
            chk('⑦ --stop 이 DEM 웹앱이 아닌 프로세스를 끄지 않고 멈춘다 (rc ≠ 0 · 그 프로세스 살아 있음 · 사유 출력)',
                r7.returncode != 0 and d7.poll() is None and _listening(p7) and 'DEM 웹앱이 아닌' in r7.stdout,
                f'rc={r7.returncode} alive={d7.poll() is None} · {r7.stdout.strip().splitlines()[-1:]}')
            data7 = os.path.join(tmp, 'data7')
            os.makedirs(data7)
            r7b = subprocess.run(['bash', fake_launcher, '--no-pull', '--bg'], cwd=tmp,
                                 env=dict(os.environ, PORT=str(p7), DEM_WEB_DATA=data7, DEM_WEB_VENV='/nonexistent'),
                                 capture_output=True, text=True, timeout=90)
            chk('⑦b 띄우기도 그 포트를 빼앗지 않는다 (rc ≠ 0 · 다른 서비스 살아 있음)',
                r7b.returncode != 0 and d7.poll() is None and _listening(p7),
                f'rc={r7b.returncode} · {r7b.stdout.strip().splitlines()[-2:]}')

            # ⑨ 실제 --bg 기동 (가짜 체크아웃 · 빈 포트) → 포트별 파일 · 옛 로그 그대로 → --stop 으로 정리
            data9 = os.path.join(tmp, 'data9')
            os.makedirs(os.path.join(data9, 'webapp'))
            old_log = os.path.join(data9, 'webapp', 'dem_webapp.log')
            with open(old_log, 'w') as f:
                f.write('기존 인스턴스 로그 — 덮이면 안 된다\n')
            p9 = _free_port()
            r9 = subprocess.run(['bash', fake_launcher, '--no-pull', '--bg'], cwd=tmp,
                                env=dict(os.environ, PORT=str(p9), DEM_WEB_DATA=data9, DEM_WEB_VENV='/nonexistent'),
                                capture_output=True, text=True, timeout=90)
            log9 = os.path.join(data9, 'webapp', f'dem_webapp_{p9}.log')
            pid9 = os.path.join(data9, 'webapp', f'dem_webapp_{p9}.pid')
            chk('⑨a --bg 기동이 포트별 로그 · pid 를 쓴다', r9.returncode == 0 and os.path.isfile(log9) and os.path.isfile(pid9)
                and _listening(p9), f'rc={r9.returncode} · {r9.stdout.strip().splitlines()[-3:]}')
            chk('⑨b 옛 이름 로그 (dem_webapp.log) 는 그대로', open(old_log).read() == '기존 인스턴스 로그 — 덮이면 안 된다\n')
            r9s = subprocess.run(['bash', fake_launcher, '--stop'], cwd=tmp, env=dict(os.environ, PORT=str(p9)),
                                 capture_output=True, text=True, timeout=60)
            chk('⑨c 그 인스턴스는 DEM 웹앱으로 알아보고 --stop 이 비운다', r9s.returncode == 0 and not _listening(p9),
                f'rc={r9s.returncode} · {r9s.stdout.strip().splitlines()[-1:]}')
            if os.path.isfile(pid9):
                try:
                    os.kill(int(open(pid9).read().strip()), 9)
                except (OSError, ValueError):
                    pass

            # ⑥ 빈 포트에 --stop 은 성공적 no-op
            r6 = subprocess.run(['bash', LAUNCHER, '--stop'], cwd=ROOT, env=dict(os.environ, PORT=str(_free_port())),
                                capture_output=True, text=True, timeout=60)
            chk('⑥ 빈 포트에 --stop 은 성공적 no-op', r6.returncode == 0, f'rc={r6.returncode}')
        finally:
            for p in procs:
                if p.poll() is None:
                    p.kill()
                    try:
                        p.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        pass
            shutil.rmtree(tmp, ignore_errors=True)

    print('webapp launcher SELFTEST', 'PASS' if not _fail else 'FAIL ' + repr(_fail))
    return 0 if not _fail else 1


if __name__ == '__main__':
    raise SystemExit(main())
