#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEM 언로딩 키트 K3 — 러너 모의 시험 (가짜 mpirun · 가짜 lmp · 임시 키트 사본).  LIGGGHTS 없음 · 네트워크 없음.

    python3 ul_runner_test.py --selftest

임시 키트 = 이 폴더의 SHA256SUMS 목록 그대로 복사 → 표의 in/ 해시만 가짜 원 파일 해시로 바꾸고 SHA256SUMS 를 다시 쓴다 (운영 코드에 우회 없음).
가짜 lmp = 덱 머리의 "# DEM 언로딩 키트 — <침대> · <종류>" 를 읽어 그 종류가 쓰는 꼴의 산출물을 만든다 (ul_reader 합성기).
"""
from __future__ import annotations

import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ul_lib  # noqa: E402

B73 = 'ps_7_3_r45'


def _sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def _kit_copy(dst, P_patch):
    """SHA256SUMS 목록대로 복사 → 표 patch → SHA256SUMS 다시."""
    lines = [ln for ln in open(os.path.join(HERE, 'SHA256SUMS'), encoding='utf-8').read().splitlines() if ln.strip()]
    for ln in lines:
        rel = ln.split(None, 1)[1].strip()
        os.makedirs(os.path.dirname(os.path.join(dst, rel)) or dst, exist_ok=True)
        shutil.copy2(os.path.join(HERE, rel), os.path.join(dst, rel))
    P = json.load(open(os.path.join(dst, 'unload_params.json'), encoding='utf-8'))
    P_patch(P)
    with open(os.path.join(dst, 'unload_params.json'), 'w', encoding='utf-8') as f:
        json.dump(P, f, ensure_ascii=False, indent=1)
        f.write('\n')
    with open(os.path.join(dst, 'SHA256SUMS'), 'w', encoding='utf-8') as f:
        for ln in lines:
            rel = ln.split(None, 1)[1].strip()
            f.write(f'{_sha(os.path.join(dst, rel))}  {rel}\n')
    return dst


def _bins(td, log):
    b = os.path.join(td, 'bin')
    os.makedirs(b, exist_ok=True)
    with open(os.path.join(b, 'mpirun'), 'w') as f:
        f.write('#!/bin/bash\nflags=""; np=""\nwhile [ $# -gt 0 ]; do case "$1" in\n'
                '  --oversubscribe) flags="$flags o"; shift;; --bind-to) flags="$flags b:$2"; shift 2;; -np) np=$2; shift 2;;\n'
                '  *) break;; esac; done\n'
                f'echo "np=$np flags=$flags" >> {log}\nMOCK_NP=$np exec "$@"\n')
    with open(os.path.join(b, 'lmp'), 'w') as f:
        f.write('#!/bin/bash\ndeck=""; args=""\nwhile [ $# -gt 0 ]; do case "$1" in -in) deck=$2; shift 2;; -log) shift 2;;\n'
                '  -var) args="$args $2=$3"; shift 3;; *) shift;; esac; done\n'
                f'echo "lmp deck=$deck $args np=$MOCK_NP" >> {log}\n'
                f'exec {sys.executable} {os.path.join(HERE, "ul_runner_test.py")} --mock-lmp "$deck" $args\n')
    for x in ('mpirun', 'lmp'):
        os.chmod(os.path.join(b, x), 0o755)
    return b


def mock_lmp(deck, kv):
    """가짜 LIGGGHTS — 덱 종류별 산출물 (화면 · 기록 · restart 자리)."""
    import ul_reader as R
    P = ul_lib.load_params()
    head = open(deck, encoding='utf-8').read().splitlines()[1]
    m = re.match(r'# DEM 언로딩 키트 — (\S+) · (\S+) — ', head)
    bed, kind = m.group(1), m.group(2)
    out = kv['out']
    procs = int(os.environ.get('MOCK_PROCS') or os.environ.get('MOCK_NP') or 6)
    print('LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, git commit 3d5c00f)')
    if os.environ.get('MOCK_FAIL_KIND') == kind:
        print('ERROR: mock failure (모의 — 이 종류는 실패한다)')
        return 1
    if kind == 'R':
        open(os.path.join(out, 'un_diag.bin'), 'w').write('x')
        print('UL_R_START\nUL_R_SETUP_DONE\nUL_R_END\nUL_R_DONE')
    elif kind in ('UNread', 'UK', 'UC', 'Ut0', 'EXT', 'EXT2') or kind.startswith('G_'):
        if kind == 'UK':
            open(os.path.join(out, 'ul_windows.csv'), 'w').write(','.join(P['records']['windows_cols']) + '\n' + '\n'.join(
                f'UK,{bed},0,{w},4,{3200000 + 5000 * w},0.111052,0,0.16,2e-07,{r},0,-1,-1,-1,400,160417,11,2e-07'
                for w, r in ((1, 3e-8), (2, 1e-8), (3, 2e-8))) + '\n')
        if kind in ('EXT', 'EXT2'):
            os.makedirs(os.path.join(out, 'restart'), exist_ok=True)
            for s in (3650000, 3660000) if kind == 'EXT' else (3700000, 3710000):
                open(os.path.join(out, 'restart', f'restart_ext_{s}.bin'), 'w').write('x')
        print(f'UL_SUMMARY arm={kind} bed={bed} result=DONE')
    else:
        rho = {'U_UB': 1.0, 'UT': 1.2, 'U_UVa': 1.03, 'U_UVb': 1.22, 'U_UT3': 1.22}.get(kind, 1.0)
        h0um = P['beds'][bed]['h0'] * 1000.0
        mid = rho / 100.0 * h0um
        job = os.path.basename(out)
        W, dt = (10000, 5e-7) if kind in ('UT', 'U_UVb', 'U_UT3') else (5000, 1e-6)
        if kv.get('ul_resume') == '1':
            open(os.path.join(out, 'ul_events.csv'), 'a').write('RESUME,9,0,0,0,state\nPOST_DONE,9,0,0,0,w4\n')
            open(os.path.join(out, 'ul_summary.txt'), 'w').write(f'result=DONE\narm={kind}\nbed={bed}\n')
            print('UL_RESUME')
        else:
            root = os.path.dirname(os.path.dirname(out))
            R._mk_arm(root, bed, job, {'W': W, 'dt': dt, 'steps': R._ladder([mid - 0.025, mid + 0.025, mid + 0.075, mid + 0.125], [1.2, 0.8, 0.6, 0.4]),
                                       'events': [('CROSS', 1, 'first'), ('RM', 3, 'ncross2')],
                                       'summary': None if os.environ.get('MOCK_TIMEOUT_KIND') == kind else 'DONE'}, P)
            os.makedirs(os.path.join(out, 'restart'), exist_ok=True)
            for s in (3215000, 3240000, 3260000):
                open(os.path.join(out, 'restart', f'restart_unload_{s}.bin'), 'w').write('x')
                open(os.path.join(out, 'restart', f'state_unload_{s}.in'), 'w').write(f'variable ul_rstep equal {s}\n')
            open(os.path.join(out, 'restart', 'restart_RM_3240000.bin'), 'w').write('x')
            open(os.path.join(out, 'restart', 'state_RM_3240000.in'), 'w').write('variable ul_rstep equal 3240000\n')
        print(f'UL_SUMMARY arm={kind} bed={bed} result=DONE')
    print(f'Loop time of 1.0 on {procs} procs for 5000 steps with 160417 atoms')
    return 0


def _env(td, kit, extra=None):
    env = dict(os.environ, WORK_ROOT=os.path.join(td, 'work'), MPIRUN=os.path.join(td, 'bin', 'mpirun'), LMP=os.path.join(td, 'bin', 'lmp'), NP='6',
               PY=sys.executable, ALLOW_CONCURRENT='1', ALLOW_OTHER_LMP='1', UL_STAMP='20261013_000000')
    for k in ('MOCK_PROCS', 'MOCK_FAIL_KIND', 'RESUME', 'SLURM_JOB_ID', 'SLURM_NTASKS', 'MOCK_TIMEOUT_KIND'):
        env.pop(k, None)
    env.update(extra or {})
    return env


def _run(td, kit, bed, job, extra=None, args=()):
    p = subprocess.run(['bash', os.path.join(kit, 'run_unload.sh'), bed, job] + list(args), env=_env(td, kit, extra),
                       capture_output=True, text=True, timeout=600)
    return p.returncode, p.stdout + p.stderr


def _calls(log):
    return open(log).read().splitlines() if os.path.exists(log) else []


def _setup(td):
    """임시 키트 · 작업 폴더 · 가짜 원 파일 (in/) · 가짜 바이너리."""
    work = os.path.join(td, 'work')
    os.makedirs(work)
    P = ul_lib.load_params()
    fake = {}
    for bed in (B73, 'ps_3_7_r45'):
        ind = os.path.join(work, bed, 'in')
        os.makedirs(ind)
        B = P['beds'][bed]
        for key, rec in B['in_files'].items():
            p = os.path.join(ind, rec['file'])
            if key == 'atom':   # S0 프레임 = 진짜 덤프 꼴 (판독기 S3 · 표면 고정 집합이 읽는다)
                import ul_reader as R
                atoms = R._chain_atoms([1, 2, 3, 4, 5], B['h0'])
                ul_lib.write_custom(p, B['s0'], ['id', 'type', 'x', 'y', 'z', 'radius', 'vx', 'vy', 'vz'],
                                    [{c: a[c] for c in ('id', 'type', 'x', 'y', 'z', 'radius', 'vx', 'vy', 'vz')} for a in atoms])
            else:
                open(p, 'w').write(f'fake {bed} {key}\n')
            fake[(bed, key)] = _sha(p)
        open(os.path.join(ind, B['orig_log']), 'w').write('log\n')
        open(os.path.join(ind, B['last_deck']), 'w').write(ul_lib.r8_text(P))

    def patch(Pj):
        for (bed, key), sh in fake.items():
            Pj['beds'][bed]['in_files'][key]['sha256'] = sh
    kit = _kit_copy(os.path.join(td, 'kit'), patch)
    log = os.path.join(td, 'calls.log')
    _bins(td, log)
    return kit, work, log


def selftest() -> int:
    fails = []

    def chk(name, cond, detail=''):
        try:
            ok = bool(cond() if callable(cond) else cond)
        except Exception as e:  # noqa: BLE001 — 빈 구현 · 예외도 실패
            ok, detail = False, f'{type(e).__name__}: {e}'
        print(('  ✓ ' if ok else '  ✗ ') + name + ('' if ok else f'  — {detail}'))
        if not ok:
            fails.append(name)

    if not (os.path.exists(os.path.join(HERE, 'run_unload.sh')) and os.path.exists(os.path.join(HERE, 'SHA256SUMS'))):
        for n in ('M1', 'M2', 'M3', 'M4a', 'M4b', 'M5', 'M6', 'M7a', 'M7b', 'M8', 'M9', 'M10'):
            chk(f'{n} (러너 · 봉인 SHA256SUMS 없음 — 시험 먼저)', False)
        print(f'selftest: FAIL ({len(fails)} 실패)')
        return 1
    td = tempfile.mkdtemp(prefix='ul_runner_mock_')
    try:
        kit, work, log = _setup(td)
        rc, out = subprocess.run(['bash', os.path.join(kit, 'run_unload_ibb.sbatch'), kit, B73, 'RJ'], env=_env(td, kit), capture_output=True,
                                 text=True, timeout=300).returncode, ''
        chk('M1 sbatch 래퍼를 SLURM 밖에서 = 사전 점검만 (런 없음 · rc 0)', lambda: rc == 0 and not _calls(log))
        rc, out = subprocess.run(['bash', os.path.join(kit, 'run_unload_ibb.sbatch'), kit, B73, 'RJ'],
                                 env=_env(td, kit, {'SLURM_JOB_ID': '1', 'SLURM_NTASKS': '4'}), capture_output=True, text=True, timeout=300).returncode, ''
        chk('M2 SLURM_NTASKS 4 ≠ NP 6 → 멈춤 (#SBATCH -n 6 ↔ -np 6 짝이 깨짐 · 런 없음)', lambda: rc == 3 and not _calls(log))
        open(os.path.join(kit, 'decks', B73, 'in.R.liggghts'), 'a').write('# 손으로 고침\n')
        rc, out = _run(td, kit, B73, 'RJ')
        chk('M3 키트 덱을 손으로 고치면 SHA256SUMS 대조에서 멈춘다 (런 없음)', lambda: rc != 0 and 'SHA256SUMS' in out and not _calls(log))
        shutil.rmtree(kit)
        kit, work2, log = _setup(os.path.join(td, 'b'))
        rc, out = _run(os.path.join(td, 'b'), kit, B73, 'RJ')
        lmp = [c for c in _calls(log) if c.startswith('lmp ')]
        kinds = [re.search(r'out=\S+/RJ/(\w+)', c).group(1) for c in lmp]
        chk('M4 RJ (7:3) = Ut0 → R → UN → UK 차례 · 모두 -np 6 · --oversubscribe --bind-to none · G0 (원 마지막 조각 덱) 기록 · 복원 판정 JSON · 보고 묶음 + sha256',
            lambda: kinds == ['Ut0', 'R', 'UN', 'UK'] and all(c.endswith('np=6') for c in lmp)
            and all(c == 'np=6 flags= o b:none' for c in _calls(log) if c.startswith('np='))
            and os.path.exists(os.path.join(work2, B73, 'RJ', 'g0.json')) and os.path.exists(os.path.join(work2, B73, 'RJ', 'restore_verdict.json'))
            and glob.glob(os.path.join(work2, B73, 'RJ.report.tgz')) and 'sha256' in out)
        chk('M4 RJ 의 UN 은 R 의 진단 restart (un_diag.bin) 를 읽는다 · 처음 상태 파일 = 빈 파일 · ul_resume 0',
            lambda: 'ckpt=' + os.path.join(work2, B73, 'RJ', 'R', 'un_diag.bin') in lmp[2] and 'ul_resume=0' in lmp[1]
            and open(re.search(r'ul_state=(\S+)', lmp[1]).group(1)).read().startswith('#'))
        rc, out = _run(os.path.join(td, 'b'), kit, B73, 'UVa')
        chk('M5 UVa 를 UB · UT 판독 전에 내면 관문이 거부 (lmp 호출 없음 · 동시 UV 제출 없음)', lambda: rc != 0 and 'REFUSE' in out
            and not any('/UVa' in c for c in _calls(log)))
        ul = os.path.join(work2, B73)
        open(os.path.join(ul, 'RJ', 'restore_verdict.json'), 'w').write(json.dumps({'status': 'RESTORED'}))
        rc, out = _run(os.path.join(td, 'b'), kit, B73, 'UB')
        ub = [c for c in _calls(log) if '/UB ' in c + ' ' and c.startswith('lmp ')]
        chk('M6 UB: 원 체크포인트 · 빈 상태 파일 · KE 기준 파일 (kebase) · arm_verdict.json · selection.json',
            lambda: rc == 0 and ub and 'ul_resume=0' in ub[0] and 'ckpt=' + os.path.join(ul, 'in', 'restart_compress_3200000.bin') in ub[0]
            and os.path.exists(os.path.join(ul, 'UB', 'arm_verdict.json')) and os.path.exists(os.path.join(ul, 'selection.json'))
            and os.path.exists(os.path.join(ul, 'ul_base.in')))
        rc, out = _run(os.path.join(td, 'b'), kit, B73, 'UB', {'RESUME': '1'})
        ub = [c for c in _calls(log) if '/UB ' in c + ' ' and c.startswith('lmp ')]
        chk('M7 이어 돌림 한 번: 마지막 restart_unload_3260000 + 짝 상태 파일 · ul_resume 1 · 화면 screen_a2',
            lambda: rc == 0 and len(ub) == 2 and 'restart_unload_3260000.bin' in ub[1] and 'state_unload_3260000.in' in ub[1]
            and 'ul_resume=1' in ub[1] and os.path.exists(os.path.join(ul, 'UB', 'screen_a2.txt')))
        rc, out = _run(os.path.join(td, 'b'), kit, B73, 'UB', {'RESUME': '1'})
        chk('M7 두 번째 이어 돌림 = 거부 (등록 범위 한 번 · §13-1)', lambda: rc != 0 and len([c for c in _calls(log) if '/UB ' in c + ' ' and c.startswith('lmp ')]) == 2)
        rc, out = _run(os.path.join(td, 'b'), kit, B73, 'UT', {'MOCK_PROCS': '4'})
        chk('M8 화면 "Loop time … on 4 procs" (≠ NP 6) = 기술 실패 (rc ≠ 0 · run_check FAIL)',
            lambda: rc != 0 and 'FAIL' in open(os.path.join(ul, 'UT', 'run_check.txt')).read())
        shutil.rmtree(os.path.join(ul, 'UT'))
        rc, out = _run(os.path.join(td, 'b'), kit, B73, 'UT')
        rc2, out2 = _run(os.path.join(td, 'b'), kit, B73, 'UVb')
        rc3, out3 = _run(os.path.join(td, 'b'), kit, B73, 'UTc')
        utc = [c for c in _calls(log) if '/UTc ' in c + ' ' and c.startswith('lmp ')]
        chk('M9 UT (δ_dt 0.2) → UVb 허용 → 튜플 t3 → UTc = U_UT3 덱을 UT 의 R_M restart · 상태에서 ul_resume 1 · UT 기록 이어 받음',
            lambda: rc == 0 and rc2 == 0 and rc3 == 0 and utc and 'restart_RM_3240000.bin' in utc[0] and 'state_RM_3240000.in' in utc[0]
            and 'ul_resume=1' in utc[0] and open(os.path.join(ul, 'UTc', 'deck.txt')).read().strip() == 'in.U_UT3.liggghts'
            and open(os.path.join(ul, 'UTc', 'ul_steps.csv')).read().count('\n') >= 5)
        rc, out = _run(os.path.join(td, 'b'), kit, 'ps_3_7_r45', 'UB')
        chk('M10 다른 침대: 복원 전 거부 (최종 튜플이 있어도)', lambda: rc != 0 and 'REFUSE' in out)
    finally:
        shutil.rmtree(td, ignore_errors=True)
    print(f'selftest: {"PASS" if not fails else "FAIL"} ({len(fails)} 실패)')
    return 1 if fails else 0


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv[:1] == ['--selftest']:
        return selftest()
    if argv[:1] == ['--mock-lmp']:
        kv = dict(x.split('=', 1) for x in argv[2:] if '=' in x)
        return mock_lmp(argv[1], kv)
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main())
