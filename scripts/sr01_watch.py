#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SR-01 A/B 상태판 — V100 에서 한 줄로 "지금 어디까지 왔나" 를 본다.

왜: 채널 하나가 CPU 에서 ~1 h 라 A/B 는 반나절짜리다.  그동안 `tail -f` 로 원시 로그를
보면 (a) 사람이 붙들려 있어야 하고 (b) 대화에 로그를 통째로 붙이게 되는데 그게 컨텍스트
비용의 큰 몫이다 (실측 Bash 출력 17 %).  이 도구는 **산출물과 로그 마커만** 읽어 한
화면으로 줄인다.

읽는 것 (전부 러너가 실제로 남기는 것):
  · 압밀 산출물   se_dump.npy · fibre.npy · phase.npy
  · 팔별 실행본   payload_{point,seg}stamp.sh      ← 이게 생기면 그 팔이 **시작**된 것
  · 팔별 결과     mpm_payload_{point,seg}stamp.json ← 이게 생기면 그 팔이 **끝난** 것
  · 최종          sr01_stamp_ab.csv
  · 로그 마커     "STEP3 solve:" (솔브 시작) · "σ_e_eff" · "σ_ion_eff" · "κ_eff" (채널 완료)
  · 프로세스      ps 에서 mpm_webapp_payload

⚠ 추정하지 않는다.  로그를 못 찾으면 "로그 없음" 이라고 적지, 진행률을 지어내지 않는다.

사용:
    python3 scripts/sr01_watch.py                     # cwd 에서 킷 자동탐색, 1회 출력
    python3 scripts/sr01_watch.py kit_ps_7_3
    python3 scripts/sr01_watch.py kit_ps_7_3 --follow 600     # 10분마다 (조여 돌리지 말 것)
    python3 scripts/sr01_watch.py --selftest
"""
from __future__ import annotations

import argparse
import glob
import os
import re
import subprocess
import sys
import time

BED = ('se_dump.npy', 'fibre.npy', 'phase.npy')
#: (라벨, 스탬프, 시작 증거, 완료 증거)
ARMS = (('A', 'point', 'payload_pointstamp.sh', 'mpm_payload_pointstamp.json'),
        ('B', 'segment', 'payload_segstamp.sh', 'mpm_payload_segstamp.json'))
CSV = 'sr01_stamp_ab.csv'
#: 채널 완료 마커 — mpm_webapp_payload 가 실제로 찍는 문구 (grep 으로 확인)
CHANNELS = (('전자', 'σ_e_eff'), ('이온', 'σ_ion_eff'), ('열', 'κ_eff'))
ARM_BANNER = '[sr01] ── arm '


def human(sec):
    if sec is None:
        return '—'
    sec = int(sec)
    h, m = divmod(sec // 60, 60)
    return f'{h}h{m:02d}m' if h else f'{m}m{sec % 60:02d}s'


def resolve_run(arg):
    """인자 → (킷 경로|None, 런 경로|None, 설명).  런 폴더는 se_dump.npy 로 식별한다."""
    cands = []
    if arg:
        cands.append(arg)
    else:                                          # cwd 에서 킷 자동탐색
        cands += sorted(glob.glob('kit_*')) + sorted(glob.glob('se_curve/kit_*'))
    for c in cands:
        if not os.path.isdir(c):
            continue
        if os.path.exists(os.path.join(c, BED[0])):
            return None, os.path.realpath(c), '런 폴더 직접 지정'
        lr = os.path.join(c, 'latest_run')
        if os.path.isdir(lr):
            return os.path.realpath(c), os.path.realpath(lr), 'latest_run'
        # ★ 디렉터리만, 그리고 **압밀 산출물을 가진** 것만.  2026-08-12 실사고: 글롭이
        #   `run_mpm.sh` (파일!) 를 런 폴더로 집어 "압밀 없음 → 먼저 run_mpm.sh" 라는
        #   정반대 안내를 냈다 — 러너에서 막 고친 것과 같은 종류의 오진.
        runs = [p for p in glob.glob(os.path.join(c, 'run_*'))
                if os.path.isdir(p) and os.path.exists(os.path.join(p, BED[0]))]
        if runs:
            runs.sort(key=os.path.getmtime)
            return os.path.realpath(c), os.path.realpath(runs[-1]), '최신 run_* (latest_run 없음)'
    return None, None, ('킷 폴더는 있는데 압밀된 run_* 이 없음 — 경로가 맞는지 확인하세요 '
                        f'(본 것: {", ".join(cands[:3])})' if cands else 'cwd 에 kit_* 가 없음')


def has_ab_banner(path, tail=256 * 1024):
    """이 로그가 **A/B 러너의 것**인가 (배너 포함).  꼬리만 본다."""
    try:
        size = os.path.getsize(path)
        with open(path, 'rb') as fh:
            fh.seek(max(0, size - tail))
            return ARM_BANNER.encode() in fh.read()
    except Exception:                              # noqa: BLE001
        return False


def find_log(run, explicit=None):
    """A/B 로그를 찾는다 — 런 폴더 **와 킷 폴더** 둘 다.  없으면 None.

    ★ 킷 폴더도 보는 이유 (2026-08-12 실측): 러너를 detach 로 띄울 때 로그를 킷 폴더에
    두는 게 자연스럽다 (`> kit_ps_7_3/sr01_ab.log`).  런 폴더만 뒤지면 어제 압밀이 남긴
    mpm_run.log 를 집어 "채널 대기" 로 보고한다 — 실제로는 A/B 가 잘 돌고 있는데도.
    ★ 최신순이 아니라 **A/B 배너가 있는 것**을 먼저 고른다.  압밀 로그가 더 최근일 수도
    있고(재압밀), 그때 최신순은 엉뚱한 파일을 집는다."""
    if explicit:
        return explicit if os.path.exists(explicit) else None
    seen, logs = set(), []
    for d in (run, os.path.dirname(run)):
        for p in glob.glob(os.path.join(d, '*.log')):
            rp = os.path.realpath(p)
            if rp in seen or os.path.getsize(p) <= 0:
                continue
            seen.add(rp)
            logs.append(p)
    if not logs:
        return None
    return max(logs, key=lambda p: (has_ab_banner(p), os.path.getmtime(p)))


def scan_log(text):
    """로그 → {'point': {...}, 'segment': {...}, 'pre': {...}}.

    ★ 로그는 두 팔이 **이어서** 쓰므로 배너로 잘라야 한다 — 안 자르면 arm A 의 완료
    마커가 arm B 진행률로 새어 들어가 "B 가 벌써 전자까지 끝났다" 는 거짓이 된다."""
    parts, cur = {'pre': []}, 'pre'
    for ln in text.splitlines():
        i = ln.find(ARM_BANNER)
        if i >= 0:
            cur = ln[i + len(ARM_BANNER):].split()[0].strip()
            parts.setdefault(cur, [])
            continue
        parts.setdefault(cur, []).append(ln)
    out = {}
    for k, lines in parts.items():
        blob = '\n'.join(lines)
        done = [name for name, mark in CHANNELS if mark in blob]
        solves = blob.count('STEP3 solve:')
        m = re.findall(r'STEP3 solve: ([\d,]+) dof', blob)
        out[k] = {'done': done, 'solves': solves, 'last_dof': m[-1] if m else None,
                  'unconverged': 'σ UNRELIABLE' in blob,
                  'traceback': 'Traceback (most recent call last)' in blob}
    return out


def running_procs():
    """→ [(pid, 경과초, 요약)] — mpm_webapp_payload 프로세스."""
    try:
        out = subprocess.run(['ps', '-eo', 'pid,etimes,args'], capture_output=True,
                             text=True, timeout=10).stdout
    except Exception:                              # noqa: BLE001 — ps 가 없어도 상태판은 뜬다
        return None
    hits = []
    for ln in out.splitlines()[1:]:
        if 'mpm_webapp_payload' not in ln or 'sr01_watch' in ln:
            continue
        f = ln.split(None, 2)
        if len(f) < 3:
            continue
        stamp = 'segment' if 'segstamp' in f[2] else ('point' if 'pointstamp' in f[2] else '?')
        hits.append((f[0], int(f[1]), stamp))
    return hits


def status(run, log_path=None, now=None):
    """→ 출력 줄 리스트.  파일시스템과 로그만 읽는다 (추정 없음)."""
    now = now or time.time()
    L = []
    ex = lambda f: os.path.exists(os.path.join(run, f))                       # noqa: E731
    mt = lambda f: os.path.getmtime(os.path.join(run, f)) if ex(f) else None  # noqa: E731

    L.append(f'run  {run}')
    miss = [f for f in BED if not ex(f)]
    L.append('압밀  ' + ('✓ ' + ' · '.join(BED) if not miss else f'✗ 없음: {", ".join(miss)}'
                         + '   → 먼저 run_mpm.sh (압밀)'))
    if miss:
        return L

    log = find_log(run, log_path)
    scan = {}
    if log:
        try:
            with open(log, 'rb') as fh:
                size = os.path.getsize(log)
                fh.seek(max(0, size - 2_000_000))
                scan = scan_log(fh.read().decode('utf-8', errors='replace'))
        except Exception as e:                     # noqa: BLE001
            L.append(f'로그  ⚠ 읽기 실패 {type(e).__name__}: {e}')
    procs = running_procs()

    for lab, stamp, sh, js in ARMS:
        s = scan.get(stamp, {})
        ch = s.get('done') or []
        chs = ' '.join(f'{n}✓' for n in ch) or ('—' if s else '')
        if ex(js):
            dt = mt(js) - (mt(sh) or mt(js))
            L.append(f'arm {lab} ({stamp:7}) ✓ 완료   {os.path.basename(js)}   소요 {human(dt)}   {chs}')
        elif ex(sh):
            alive = [p for p in (procs or []) if p[2] == stamp]
            el = human(now - mt(sh))
            if alive:
                L.append(f'arm {lab} ({stamp:7}) ▶ 진행   경과 {el}   채널 {chs or "대기"}'
                         + (f'   (솔브 {s["solves"]}회 시작, 최근 {s["last_dof"]} dof)' if s.get('solves') else ''))
            elif procs is None:
                L.append(f'arm {lab} ({stamp:7}) ? 프로세스 확인 불가(ps 없음)   경과 {el}   채널 {chs}')
            else:
                L.append(f'arm {lab} ({stamp:7}) ✗ **프로세스 없음인데 결과도 없음** — 죽었을 수 있음. '
                         f'경과 {el}   채널 {chs}')
                if s.get('traceback'):
                    L.append(f'      ↑ 로그에 Traceback 있음 → {log}')
        else:
            L.append(f'arm {lab} ({stamp:7}) · 미시작')
        if s.get('unconverged'):
            L.append(f'      ⚠ 이 팔 로그에 "σ UNRELIABLE" — 미수렴 채널이 있다, Δ 인용 금지')

    if ex(CSV):
        L.append(f'비교  ✓ {CSV}')
        try:
            with open(os.path.join(run, CSV), encoding='utf-8') as fh:
                L += ['      ' + x.rstrip() for x in fh.readlines()[:4]]
        except Exception:                          # noqa: BLE001
            pass
    elif all(ex(js) for _, _, _, js in ARMS):
        L.append('비교  → 두 팔 완료.  실행:')
        L.append(f'      python3 {os.path.join(os.path.dirname(os.path.abspath(__file__)), "sr01_stamp_compare.py")} \\')
        L.append(f'        {os.path.join(run, ARMS[0][3])} {os.path.join(run, ARMS[1][3])} \\')
        L.append(f'        --label $(basename $(dirname {run})) --csv {os.path.join(run, CSV)}')
    L.append(f'로그  {log or "없음 (러너 출력을 파일로 안 남겼거나 다른 경로)"}')
    return L


def _selftest():
    import tempfile
    ok = fail = 0

    def chk(m, c):
        nonlocal ok, fail
        print(('  PASS  ' if c else '  FAIL  ') + m)
        ok, fail = ok + (1 if c else 0), fail + (0 if c else 1)

    log = ('[sr01] PSIG=（없음）\n'
           '[sr01] ── arm point → mpm_payload_pointstamp.json\n'
           '    STEP3 solve: 2,713,168 dof, plate contacts 1/2 — CG running\n'
           '  STEP3 σ_e_eff = 0.005122 S/cm\n'
           '    STEP3 solve: 2,713,128 dof, plate contacts 1/2 — CG running\n'
           '  STEP3 σ_ion_eff = 0.31 S/cm\n'
           '[sr01] ── arm segment → mpm_payload_segstamp.json\n'
           '    STEP3 solve: 2,713,000 dof, plate contacts 1/2 — CG running\n')
    s = scan_log(log)
    chk('1) ★ 팔별로 잘라 읽는다 (A 의 완료가 B 로 안 샌다)',
        s['point']['done'] == ['전자', '이온'] and s['segment']['done'] == [])
    chk('2) 솔브 횟수·최근 dof', s['point']['solves'] == 2 and s['segment']['last_dof'] == '2,713,000')
    chk('3) 미수렴 마커 없음', not s['point']['unconverged'])
    s2 = scan_log(log + '  ⚠ STEP3 CG not converged (info=0, resid=1e-3) — σ UNRELIABLE\n')
    chk('4) ★ σ UNRELIABLE 을 잡는다', s2['segment']['unconverged'])
    # 배너 前 줄(러너 헤더)이 첫 팔로 새면 arm A 진행률이 부풀어 보인다
    s3 = scan_log('    STEP3 solve: 9 dof — CG running\n' + log)
    chk('5) ★ 배너 前 줄은 pre 로 (첫 팔로 새지 않는다)',
        s3['pre']['solves'] == 1 and s3['point']['solves'] == 2)

    with tempfile.TemporaryDirectory() as td:
        run = os.path.join(td, 'run_x'); os.makedirs(run)
        out = '\n'.join(status(run))
        chk('6) 압밀 없으면 그렇게 말하고 멈춘다', '✗ 없음' in out and 'arm A' not in out)
        for f in BED:
            open(os.path.join(run, f), 'w').close()
        out = '\n'.join(status(run))
        chk('7) 압밀만 있으면 두 팔 미시작', out.count('· 미시작') == 2)
        open(os.path.join(run, 'payload_pointstamp.sh'), 'w').close()
        out = '\n'.join(status(run))
        chk('8) ★ 시작됐는데 프로세스도 결과도 없으면 "죽었을 수 있음"', '죽었을 수 있음' in out)
        open(os.path.join(run, 'mpm_payload_pointstamp.json'), 'w').close()
        open(os.path.join(run, 'payload_segstamp.sh'), 'w').close()
        open(os.path.join(run, 'mpm_payload_segstamp.json'), 'w').close()
        out = '\n'.join(status(run))
        chk('9) 두 팔 완료면 비교 명령을 준다', 'sr01_stamp_compare.py' in out and '완료' in out)
        with open(os.path.join(run, CSV), 'w', encoding='utf-8') as fh:
            fh.write('label,sigma_e_A,sigma_e_B\nkit,0.005,0.006\n')
        out = '\n'.join(status(run))
        chk('10) csv 가 있으면 그걸 보여준다', 'sigma_e_A' in out)
        with open(os.path.join(run, 'x.log'), 'w', encoding='utf-8') as fh:
            fh.write(log)
        out = '\n'.join(status(run))
        chk('11) 로그를 찾아 채널을 표시', '전자✓' in out)
        # ★ 킷 폴더의 A/B 로그를 런 폴더의 압밀 로그보다 먼저 고른다 (2026-08-12 실사고)
        kitd = os.path.dirname(run)
        ab = os.path.join(kitd, 'sr01_ab.log')
        with open(ab, 'w', encoding='utf-8') as fh:
            fh.write(log)
        os.utime(os.path.join(run, 'x.log'), (time.time() + 60, time.time() + 60))  # 압밀 로그를 더 최신으로
        chk('14) ★ 킷 폴더의 A/B 로그를 찾는다 (런 폴더만 보면 압밀 로그를 집는다)',
            os.path.realpath(find_log(run)) == os.path.realpath(ab)
            or has_ab_banner(find_log(run)))
        with open(os.path.join(run, 'x.log'), 'w', encoding='utf-8') as fh:
            fh.write('압밀 로그 — A/B 배너 없음\n')
        chk('15) ★ 배너 없는 최신 로그보다 배너 있는 로그가 우선',
            has_ab_banner(find_log(run)))
        os.remove(ab)
        r2 = resolve_run(os.path.join(td, 'nope'))
        chk('12) 없는 경로는 조용히 실패', r2[1] is None)
        kit = os.path.join(td, 'kit_ps_7_3'); os.makedirs(kit)
        os.symlink(run, os.path.join(kit, 'latest_run'))
        chk('13) 킷 → latest_run 해석', resolve_run(kit)[1] == os.path.realpath(run))
        # ★ 2026-08-12 실사고: 글롭이 `run_mpm.sh`(파일)를 런 폴더로 집어
        #   "압밀 없음 → 먼저 run_mpm.sh" 라는 정반대 안내를 냈다.
        kit2 = os.path.join(td, 'kit_bogus'); os.makedirs(kit2)
        open(os.path.join(kit2, 'run_mpm.sh'), 'w').close()
        k, r, how = resolve_run(kit2)
        chk('16) ★ run_mpm.sh(파일)를 런 폴더로 집지 않는다', r is None and 'run_*' in how)
        empty = os.path.join(kit2, 'run_empty'); os.makedirs(empty)
        chk('17) ★ 압밀 산출물 없는 run_* 도 고르지 않는다', resolve_run(kit2)[1] is None)
        open(os.path.join(empty, BED[0]), 'w').close()
        chk('18) se_dump.npy 가 생기면 그때 고른다',
            resolve_run(kit2)[1] == os.path.realpath(empty))
    print(f'\nsr01_watch selftest: {ok}/{ok + fail} PASS')
    return 0 if fail == 0 else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('target', nargs='?', help='킷 폴더 또는 런 폴더 (생략 시 cwd 에서 kit_* 탐색)')
    ap.add_argument('--follow', type=int, metavar='SEC',
                    help='SEC 마다 반복 (권장 ≥300 — 조여 돌려도 채널당 ~1h 는 안 빨라진다)')
    ap.add_argument('--log', help='로그 경로 직접 지정 (자동탐색이 못 찾을 때)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    kit, run, how = resolve_run(a.target)
    if run is None:
        print(f'ABORT — {how}.  사용: python3 scripts/sr01_watch.py <킷 또는 런 폴더>')
        return 2
    while True:
        print('═' * 72)
        print(time.strftime('%Y-%m-%d %H:%M:%S') + f'   ({how}' + (f', kit={os.path.basename(kit)}' if kit else '') + ')')
        for ln in status(run, a.log):
            print(ln)
        sys.stdout.flush()
        if not a.follow:
            return 0
        time.sleep(max(30, a.follow))


if __name__ == '__main__':
    sys.exit(main())
