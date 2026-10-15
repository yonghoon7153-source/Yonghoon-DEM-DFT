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


def _bins(td):
    """가짜 mpirun · lmp · pywrap — 글자가 늘 같다 (호출 기록 = 환경 MOCK_LOG) ⇒ 가짜 lmp 의 sha256 이 시험 폴더마다 같다
    (Q5 — 문법 fixture 런과 본 키트 런이 같은 바이너리여야 사전 점검을 통과한다).  가짜 lmp 는 이력 시험 덱 (in.hist_*) 이면 그 읽는 쪽 모의 단계로 간다."""
    b = os.path.join(td, 'bin')
    os.makedirs(b, exist_ok=True)
    with open(os.path.join(b, 'mpirun'), 'w') as f:
        f.write('#!/bin/bash\nflags=""; np=""\nwhile [ $# -gt 0 ]; do case "$1" in\n'
                '  --oversubscribe) flags="$flags o"; shift;; --bind-to) flags="$flags b:$2"; shift 2;; -np) np=$2; shift 2;;\n'
                '  *) break;; esac; done\n'
                'echo "np=$np flags=$flags" >> "${MOCK_LOG:-/dev/null}"\nMOCK_NP=$np exec "$@"\n')
    with open(os.path.join(b, 'lmp'), 'w') as f:
        f.write('#!/bin/bash\ndeck=""; args=""; out=""\nwhile [ $# -gt 0 ]; do case "$1" in -in) deck=$2; shift 2;; -log) shift 2;;\n'
                '  -var) args="$args $2=$3"; [ "$2" = out ] && out=$3; shift 3;; *) shift;; esac; done\n'
                'echo "lmp deck=$deck $args np=$MOCK_NP" >> "${MOCK_LOG:-/dev/null}"\n'
                '# 이력 시험 덱 (문법 fixture 양성 대조) = 그 읽는 쪽의 모의 단계\n'
                'case "$(basename "$deck")" in\n  in.hist_*)\n'
                '    echo "LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, git commit 3d5c00f)"\n'
                f'    exec {sys.executable} {os.path.join(HERE, "history_test", "read_history.py")} --mock-stage "$(basename "$out")" "$out";;\nesac\n'
                f'exec {sys.executable} {os.path.join(HERE, "ul_runner_test.py")} --mock-lmp "$deck" $args\n')
    with open(os.path.join(b, 'pywrap'), 'w') as f:   # 판독기 모의 (시험 쪽 감쌈 · 운영 코드에 우회 없음) — $3 = ul_reader 명령
        f.write('#!/bin/bash\ncmd="${3:-}"\n'
                'if [ -n "${MOCK_READER_FAIL:-}" ] && [ "$cmd" = "$MOCK_READER_FAIL" ]; then\n'
                '  echo "Traceback (most recent call last): [mock] 판독기 $cmd 프로그램 오류" >&2; exit 1; fi\n'
                'if [ -n "${MOCK_READER_FAIL_ONCE:-}" ] && [ "$cmd" = "$MOCK_READER_FAIL_ONCE" ] && [ ! -e "${MOCK_ONCE_FLAG:?}" ]; then\n'
                '  : > "$MOCK_ONCE_FLAG"; echo "Traceback (most recent call last): [mock] 판독기 $cmd 프로그램 오류 (첫 호출만)" >&2; exit 1; fi\n'
                f'{sys.executable} "$@"; r=$?\n'
                '# 모의 복원 판정 = RESTORED (모의 R · UN 은 관측 덤프를 다 흉내 내지 않는다 — 증서와 그 판독기 rc 0 을 러너가 그대로 기록하게)\n'
                'if [ "${MOCK_RESTORE_AS:-}" = RESTORED ] && [ "$cmd" = restore ]; then\n'
                f'  {sys.executable} -I -c \'import json,sys; p=sys.argv[1]; d=json.load(open(p)); d["status"]="RESTORED"; open(p,"w").write(json.dumps(d))\' '
                '"$4/$5/$7/restore_verdict.json" && r=0; fi\n'
                '# 결과 파일을 쓴 뒤 실패 (Codex actual_restore_cli_closed_stdout — 출력 flush 실패 rc 120)\n'
                'if [ -n "${MOCK_READER_FAIL_AFTER:-}" ] && [ "$cmd" = "$MOCK_READER_FAIL_AFTER" ]; then\n'
                '  echo "[mock] 판독기 $cmd — 결과 파일을 쓴 뒤 출력 실패 (rc 120)" >&2; exit 120; fi\n'
                'exit $r\n')
    for x in ('mpirun', 'lmp', 'pywrap'):
        os.chmod(os.path.join(b, x), 0o755)
    return b


_GV = {'path': None}   # Q5 — 이 시험 실행의 문법 fixture 양성 대조 판정 (selftest 처음에 한 번 만든다)


def _grammar_run(gdir):
    """Q5 양성 대조 — 지금 history_test 의 문법 fixture 러너 (run_history.sh --grammar-only) + 읽는 쪽 (read_history.py --grammar) 을
    본 키트 모의 시험과 같은 가짜 바이너리 (같은 sha256) 로 → (그 런의 grammar_verdict.json | None, rc, 화면)."""
    work = os.path.join(gdir, 'work')
    os.makedirs(work)
    b = _bins(gdir)
    env = dict(os.environ, WORK_ROOT=work, MPIRUN=os.path.join(b, 'mpirun'), LMP=os.path.join(b, 'lmp'), NP='6', NP_ALT='4',
               HIST_STAMP='20261014_000000', PY=sys.executable, ALLOW_CONCURRENT='1', ALLOW_OTHER_LMP='1', MOCK_LOG=os.path.join(gdir, 'calls.log'))
    for k in ('MOCK_FAIL_STAGE', 'MOCK_FAIL_AFTER_STAGE', 'HIST_KIT', 'KIT'):
        env.pop(k, None)
    p = subprocess.run(['bash', os.path.join(HERE, 'history_test', 'run_history.sh'), '--grammar-only'], env=env, capture_output=True, text=True,
                       timeout=900)
    hits = glob.glob(os.path.join(work, 'gram_*', 'grammar_verdict.json'))
    return (hits[0] if p.returncode == 0 and len(hits) == 1 else None), p.returncode, p.stdout + p.stderr


def _gram_variant(gv, dst, kind):
    """문법 fixture 판정 런 폴더 사본 + 반례 하나 (Q5 음성) — run_dir 은 새 자리로 (그 반례만 남게) · kit 은 원 자리 그대로 (run_manifest kit=)."""
    src = os.path.dirname(gv)
    nd = os.path.join(dst, os.path.basename(src))
    shutil.copytree(src, nd)
    vp = os.path.join(nd, 'grammar_verdict.json')
    v = json.load(open(vp, encoding='utf-8'))
    v['run_dir'] = nd
    if kind == 'status_fail':
        v.update(status='FAIL', exit_code=2)
    if kind == 'deck':
        open(os.path.join(nd, 'GA', 'in.hist_grammar.liggghts'), 'a').write('# 손으로 고침\n')
    if kind == 'lmp':
        mp = os.path.join(nd, 'run_manifest.txt')
        mtext = re.sub(r'^lmp_sha256=.*$', 'lmp_sha256=' + 'f' * 64, open(mp).read(), flags=re.M)
        open(mp, 'w').write(mtext)
    open(vp, 'w', encoding='utf-8').write(json.dumps(v, ensure_ascii=False, indent=2))
    return vp


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
    crash = os.environ.get('MOCK_CRASH_KIND') == kind   # 기계 실패 모의 — 기록 · 단 끝 restart 는 남기고 요약 · Loop time 없이 rc 1
    if kind == 'R':
        open(os.path.join(out, 'un_diag.bin'), 'w').write('x')
        print('UL_R_START\nUL_R_SETUP_DONE\nUL_R_END\nUL_R_DONE')
    elif kind == 'UNread':
        print('UL_UN_START\nUL_UN_DONE')
    elif kind in ('UK', 'UC', 'Ut0', 'EXT', 'EXT2') or kind.startswith('G_'):
        if kind == 'UK':   # 덱 in.UK 꼴 그대로 — S0 무이동 세 창 (step = S0 + w · W0 · 판 = h0) · 사건 START · NOMOVE_DONE · 요약 DONE (ULKR-09)
            B, W0 = P['beds'][bed], P['windows']['W0']
            s0 = int(kv.get('ul_s0') or B['s0'])
            rows = [(w, s0 + W0 * w, r) for w, r in ((1, 3e-8), (2, 1e-8), (3, 2e-8))]
            if os.environ.get('MOCK_UK_ONEROW'):   # Codex one_uk_row — step 1 · w 1 · 회전 0.001 J 한 줄 (불완전 UK)
                rows = [(1, 1, 0.001)]
            open(os.path.join(out, 'ul_windows.csv'), 'w').write(','.join(P['records']['windows_cols']) + '\n' + '\n'.join(
                f'UK,{bed},0,{w},4,{s},{B["h0"]},0,0.16,2e-07,{r},0,-1,-1,-1,400,160417,11,2e-07' for w, s, r in rows) + '\n')
            open(os.path.join(out, 'ul_events.csv'), 'w').write(','.join(P['records']['events_cols']) + f'\nSTART,0,{s0},{B["h0"]},0,s0\n'
                                                                 f'NOMOVE_DONE,0,{s0 + 3 * W0},{B["h0"]},0,w3\n')
            open(os.path.join(out, 'ul_summary.txt'), 'w').write(f'result=DONE\narm=UK\nbed={bed}\n')
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
        if os.environ.get('MOCK_ROLLBACK_KIND') == kind:   # ULKRR-02 러너 수준 양성 대조 — 기계 실패 + 이어 돌림 (남긴 줄 · 덱 꼴 그대로)
            return _mock_rollback(out, bed, job, kind, P, W, dt, mid, kv)
        if kv.get('ul_resume') == '1':
            st = open(kv['ul_state']).read() if os.path.exists(kv.get('ul_state', '')) else ''
            m, mk = re.search(r'variable ul_rstep equal (\d+)', st), re.search(r'variable ul_k equal (\d+)', st)
            rs, kr = (m.group(1) if m else '0'), (mk.group(1) if mk else '9')
            open(os.path.join(out, 'ul_events.csv'), 'a').write(f'RESUME,{kr},{rs},0,0,state\nPOST_DONE,{kr},{rs},0,0,w4\n')
            open(os.path.join(out, 'ul_summary.txt'), 'w').write(f'result=DONE\narm={kind}\nbed={bed}\n')
            print('UL_RESUME')
        else:
            root = os.path.dirname(os.path.dirname(out))
            # 덱 꼴 그대로: 교차 k 2 · 확인 k 3 · 4 → R_M (restart_RM_<그 step> + state_RM_<그 step> — _mk_arm) · UT 는 R_M 에서 멈춤 (RM_STOP)
            ev = [('CROSS', 2, 'first'), ('RM', 4, 'ncross2')] + ([('RM_STOP', 4, 'UT')] if kind == 'UT' else [])
            done = None if (os.environ.get('MOCK_TIMEOUT_KIND') == kind or crash) else ('RM_STOP' if kind == 'UT' else 'DONE')
            R._mk_arm(root, bed, job, {'W': W, 'dt': dt, 'steps': R._ladder([mid - 0.025, mid + 0.025, mid + 0.075, mid + 0.125], [1.2, 0.8, 0.6, 0.4]),
                                       'events': ev, 'summary': done}, P)
            os.makedirs(os.path.join(out, 'restart'), exist_ok=True)
            for s in (3215000, 3240000, 3260000):
                open(os.path.join(out, 'restart', f'restart_unload_{s}.bin'), 'w').write('x')
                open(os.path.join(out, 'restart', f'state_unload_{s}.in'), 'w').write(f'variable ul_rstep equal {s}\n')
        if crash:
            print('[mock] 기계 실패 — 요약 · Loop time 없이 끝')
            return 1
        print(f'UL_SUMMARY arm={kind} bed={bed} result=DONE')
    print(f'Loop time of 1.0 on {procs} procs for 5000 steps with 160417 atoms')
    return 0


def _mock_rollback(out, bed, job, kind, P, W, dt, mid, kv):
    """ULKRR-02 러너 수준 양성 대조 — 기계 실패 + 이어 돌림을 덱 꼴 그대로 (같은 사다리를 임시 폴더에 _mk_arm 으로 만든 뒤 나눠 쓴다):
    첫 시도 (ul_resume 0) = 단 1 끝 (s_r) 까지의 기록 · 덤프 + 단 2 의 창 둘 · 단 줄 하나 · 사건 하나 (P 9.999 — 끊긴 시도가 남긴 줄) ·
      restart_unload_<s_r> + state_unload_<s_r> (ul_rstep s_r · ul_k 1) → 요약 없이 rc 1 (기계 실패).
    두 번째 시도 (ul_resume 1 · 러너가 준 상태 파일) = RESUME (상태 파일의 k · step) + s_r 뒤 기록 · 덤프 · R_M · 요약 · 화면 → rc 0."""
    import tempfile
    import ul_reader as R
    Rc = P['records']
    with tempfile.TemporaryDirectory() as tmp:
        ev = [('CROSS', 2, 'first'), ('RM', 4, 'ncross2')] + ([('RM_STOP', 4, 'UT')] if kind == 'UT' else [])
        full = R._mk_arm(tmp, bed, job, {'W': W, 'dt': dt, 'steps': R._ladder([mid - 0.025, mid + 0.025, mid + 0.075, mid + 0.125], [1.2, 0.8, 0.6, 0.4]),
                                         'events': ev, 'summary': 'RM_STOP' if kind == 'UT' else 'DONE'}, P)

        def rows(name):
            return [ln.split(',') for ln in open(os.path.join(full, name)).read().splitlines()[1:] if ln.strip()]
        Wr, Sr, Er = rows('ul_windows.csv'), rows('ul_steps.csv'), rows('ul_events.csv')
        wc, sc, ec = Rc['windows_cols'], Rc['steps_cols'], Rc['events_cols']
        k1 = next(r for r in Sr if int(r[sc.index('k')]) == 1)
        sr = int(k1[sc.index('step')])

        def put(name, cols, rows_, append):
            with open(os.path.join(out, name), 'a' if append else 'w') as f:
                f.write(('' if append else ','.join(cols) + '\n') + ''.join(','.join(r) + '\n' for r in rows_))

        def copy_dumps(keep):
            os.makedirs(os.path.join(out, 'dump'), exist_ok=True)
            for nm in os.listdir(os.path.join(full, 'dump')):
                if keep(int(re.search(r'_(\d+)\.', nm).group(1))):
                    shutil.copy(os.path.join(full, 'dump', nm), os.path.join(out, 'dump', nm))
        blocks, cur = [], []
        for ln in open(os.path.join(full, 'screen.txt')).read().splitlines()[1:]:
            if ln.strip().startswith('Step') and cur:
                blocks.append(cur)
                cur = []
            cur.append(ln)
        blocks.append(cur)
        blocks = [(int(b[1].split()[0]), b) for b in blocks if len(b) > 1 and b[0].strip().startswith('Step')]
        if kv.get('ul_resume') != '1':
            iP, iS = wc.index('Ps_avg'), sc.index('Pbar')
            put('ul_windows.csv', wc, [r for r in Wr if int(r[wc.index('step')]) <= sr]
                + [r[:iP] + ['9.999'] + r[iP + 1:] for r in Wr if int(r[wc.index('k')]) == 2][:2], False)
            put('ul_steps.csv', sc, [r for r in Sr if int(r[sc.index('step')]) <= sr]
                + [r[:iS] + ['9.999'] + r[iS + 1:] for r in Sr if int(r[sc.index('k')]) == 2][:1], False)
            put('ul_events.csv', ec, [r for r in Er if int(r[ec.index('step')]) <= sr] + [r for r in Er if int(r[ec.index('step')]) > sr][:1], False)
            copy_dumps(lambda s: s <= sr)
            os.makedirs(os.path.join(out, 'restart'), exist_ok=True)
            open(os.path.join(out, 'restart', f'restart_unload_{sr}.bin'), 'w').write('x')
            open(os.path.join(out, 'restart', f'state_unload_{sr}.in'), 'w').write(
                f'variable ul_rstep equal {sr}\nvariable ul_k equal 1\nvariable ul_phase equal 0\nvariable ul_modeB equal 1\n')
            for s0, b in blocks:
                if s0 < sr:
                    print('\n'.join(b))
            print('[mock] 기계 실패 — 단 2 창 둘 · 단 줄 하나를 남기고 요약 · Loop time 없이 끝')
            return 1
        st = open(kv['ul_state']).read()
        rs, kr = (int(re.search(rf'variable {n} equal (\d+)', st).group(1)) for n in ('ul_rstep', 'ul_k'))
        put('ul_events.csv', ec, [['RESUME', str(kr), str(rs), k1[sc.index('plate_z')], k1[sc.index('lift')], 'state']]
            + [r for r in Er if int(r[ec.index('step')]) > rs], True)
        put('ul_windows.csv', wc, [r for r in Wr if int(r[wc.index('step')]) > rs], True)
        put('ul_steps.csv', sc, [r for r in Sr if int(r[sc.index('step')]) > rs], True)
        copy_dumps(lambda s: s > rs)
        for nm in os.listdir(os.path.join(full, 'restart')):
            shutil.copy(os.path.join(full, 'restart', nm), os.path.join(out, 'restart', nm))
        shutil.copy(os.path.join(full, 'ul_summary.txt'), os.path.join(out, 'ul_summary.txt'))
        print(f'UL_RESUME arm={job} bed={bed} step={rs} k={kr}')
        for s0, b in blocks:
            if s0 >= rs:
                print('\n'.join(b))
        print(f'UL_SUMMARY arm={job} bed={bed} result={"RM_STOP" if kind == "UT" else "DONE"}')
    return 0


def _env(td, kit, extra=None):
    """러너 환경 — 가짜 바이너리 · 호출 기록 (MOCK_LOG) · 문법 fixture 양성 판정 (GRAMMAR_VERDICT · Q5) · extra 의 값 None = 그 변수 없음."""
    env = dict(os.environ, WORK_ROOT=os.path.join(td, 'work'), MPIRUN=os.path.join(td, 'bin', 'mpirun'), LMP=os.path.join(td, 'bin', 'lmp'), NP='6',
               PY=sys.executable, ALLOW_CONCURRENT='1', ALLOW_OTHER_LMP='1', UL_STAMP='20261013_000000', MOCK_LOG=os.path.join(td, 'calls.log'))
    for k in ('MOCK_PROCS', 'MOCK_FAIL_KIND', 'RESUME', 'SLURM_JOB_ID', 'SLURM_NTASKS', 'MOCK_TIMEOUT_KIND', 'MOCK_CRASH_KIND', 'MOCK_READER_FAIL',
              'MOCK_UK_ONEROW', 'MOCK_READER_FAIL_ONCE', 'MOCK_ONCE_FLAG', 'MOCK_READER_FAIL_AFTER', 'MOCK_RESTORE_AS', 'MOCK_ROLLBACK_KIND',
              'GRAMMAR_VERDICT', 'HIST_VERDICT'):
        env.pop(k, None)
    if _GV['path']:
        env['GRAMMAR_VERDICT'] = _GV['path']
    for k, v in (extra or {}).items():
        if v is None:
            env.pop(k, None)
        else:
            env[k] = v
    return env


def _run(td, kit, bed, job, extra=None, args=()):
    p = subprocess.run(['bash', os.path.join(kit, 'run_unload.sh'), bed, job] + list(args), env=_env(td, kit, extra),
                       capture_output=True, text=True, timeout=600)
    return p.returncode, p.stdout + p.stderr


def _calls(log):
    return open(log).read().splitlines() if os.path.exists(log) else []


def _lmp(log, job):
    """가짜 lmp 호출 중 그 잡 폴더 (-var out …/<잡>) 의 것."""
    return [c for c in _calls(log) if c.startswith('lmp ') and re.search(rf'\bout=\S*/{re.escape(job)}(\s|$)', c)]


def _read(p):
    return open(p, encoding='utf-8', errors='replace').read() if os.path.exists(p) else ''


def _sha_or_none(p):
    return _sha(p) if os.path.exists(p) else None


def P_bed(bed):
    return ul_lib.load_params()['beds'][bed]


def _setup(td, beds=(B73, 'ps_3_7_r45')):
    """임시 키트 · 작업 폴더 · 가짜 원 파일 (in/) · 가짜 바이너리."""
    work = os.path.join(td, 'work')
    os.makedirs(work)
    P = ul_lib.load_params()
    fake = {}
    for bed in beds:
        ind = os.path.join(work, bed, 'in')
        os.makedirs(ind)
        B = P['beds'][bed]
        for key, rec in B['in_files'].items():
            p = os.path.join(ind, rec['file'])
            if key == 'atom':   # S0 프레임 = 진짜 덤프 꼴 (판독기 S3 · 표면 고정 집합이 읽는다 · 10:0 = 원 3,600,000)
                import ul_reader as R
                atoms = R._chain_atoms([1, 2, 3, 4, 5], B['h0'])
                ul_lib.write_custom(p, B['s0'] or P['ext_10_0']['start_step'], ['id', 'type', 'x', 'y', 'z', 'radius', 'vx', 'vy', 'vz'],
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
    log = os.path.join(td, 'calls.log')   # = _env 의 MOCK_LOG
    _bins(td)
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
        for n in ('M1', 'M2', 'M3', 'M4a', 'M4b', 'M4c', 'M5', 'M6', 'M7a', 'M7b', 'M7c', 'M8', 'M9', 'M10', 'M11', 'M12', 'M13', 'M14', 'M15',
                  'M16', 'M17', 'M18', 'M19'):
            chk(f'{n} (러너 · 봉인 SHA256SUMS 없음 — 시험 먼저)', False)
        print(f'selftest: FAIL ({len(fails)} 실패)')
        return 1
    td = tempfile.mkdtemp(prefix='ul_runner_mock_')
    try:
        gv, grc, gout = _grammar_run(os.path.join(td, 'gram'))
        _GV['path'] = gv
        chk('M22 (준비) Q5 문법 fixture 양성 대조 런 — 지금 history_test 러너 (--grammar-only) + 읽는 쪽 · 본 키트 모의와 같은 가짜 바이너리 → grammar_verdict PASS · rc 0',
            lambda: grc == 0 and gv is not None and json.load(open(gv, encoding='utf-8')).get('status') == 'PASS', gout[-400:])
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
        restored = {'PY': os.path.join(td, 'b', 'bin', 'pywrap'), 'MOCK_RESTORE_AS': 'RESTORED'}   # 모의 복원 판정 = RESTORED (판독기 rc 0 그대로 기록)
        rc, out = _run(os.path.join(td, 'b'), kit, B73, 'RJ', restored)
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
        man_rj = _read(os.path.join(work2, B73, 'RJ', 'run_manifest.txt'))
        chk('M4 ULKR-11 RJ 잡 기록에 단계마다 기술 rc (G0 · Ut0 · R · UNread · UK) · 판독기 rc (restore · kebase) · 끝 줄',
            lambda: all(re.search(rf'^stage={s}( |$).*\brc=0\b', man_rj, re.M) for s in ('G0', 'Ut0', 'R', 'UNread', 'UK'))
            and re.search(r'^reader_restore_rc=\d+$', man_rj, re.M) and re.search(r'^reader_kebase_rc=0$', man_rj, re.M)
            and re.search(r'^end=.* fails=0 ', man_rj, re.M))
        ul = os.path.join(work2, B73)
        open(os.path.join(ul, 'RJ', 'restore_verdict.json'), 'w').write(json.dumps({'status': 'RESTORED'}))
        rc, out = _run(os.path.join(td, 'b'), kit, B73, 'UB')
        ub = _lmp(log, 'UB')
        chk('M6 UB: 원 체크포인트 · 빈 상태 파일 · KE 기준 파일 (kebase) · arm_verdict.json · selection.json · 관문 ALLOW 기록 · 판독기 rc 0',
            lambda: rc == 0 and ub and 'ul_resume=0' in ub[0] and 'ckpt=' + os.path.join(ul, 'in', 'restart_compress_3200000.bin') in ub[0]
            and os.path.exists(os.path.join(ul, 'UB', 'arm_verdict.json')) and os.path.exists(os.path.join(ul, 'selection.json'))
            and os.path.exists(os.path.join(ul, 'ul_base.in')) and re.search(r'^gate=ALLOW$', _read(os.path.join(ul, 'UB', 'run_manifest.txt')), re.M)
            and re.search(r'^reader_arm_rc=0$', _read(os.path.join(ul, 'UB', 'run_manifest.txt')), re.M))
        rc, out = _run(os.path.join(td, 'b'), kit, B73, 'UB', {'RESUME': '1'})
        chk('M7a ULKR-06 첫 시도가 덱 요약 (ul_summary.txt) 까지 끝난 팔 = 이어 돌림 거부 (기계 실패가 아니다 · lmp 호출 없음)',
            lambda: rc != 0 and 'ul_summary' in out and len(_lmp(log, 'UB')) == 1 and not os.path.exists(os.path.join(ul, 'UB', 'screen_a2.txt')))
        rc, out = _run(os.path.join(td, 'b'), kit, B73, 'UT', {'MOCK_CRASH_KIND': 'UT'})
        first = {n: _sha_or_none(os.path.join(ul, 'UT', n)) for n in ('screen.txt', 'deck.liggghts')}
        rc2, out2 = _run(os.path.join(td, 'b'), kit, B73, 'UT', {'RESUME': '1'})
        ut = _lmp(log, 'UT')
        man_ut = _read(os.path.join(ul, 'UT', 'run_manifest.txt'))
        chk('M7 이어 돌림 한 번 (첫 시도 = 기계 실패 · 요약 없음): 마지막 restart_unload_3260000 + 짝 상태 파일 · ul_resume 1 · 화면 screen_a2 · '
            '첫 시도 화면 · 덱 사본 덮어쓰지 않음 · 잡 기록 덧붙임 (resume=0 · resume=1 둘 다)',
            lambda: rc != 0 and rc2 == 0 and len(ut) == 2 and 'restart_unload_3260000.bin' in ut[1] and 'state_unload_3260000.in' in ut[1]
            and 'ul_resume=1' in ut[1] and os.path.exists(os.path.join(ul, 'UT', 'screen_a2.txt')) and all(first.values())
            and all(_sha_or_none(os.path.join(ul, 'UT', n)) == h for n, h in first.items())
            and re.search(r'^resume=0$', man_ut, re.M) and re.search(r'^resume=1$', man_ut, re.M))
        rc, out = _run(os.path.join(td, 'b'), kit, B73, 'UT', {'RESUME': '1'})
        chk('M7 두 번째 이어 돌림 = 거부 (등록 범위 한 번 · §13-1 · 개정 3 §14-4)', lambda: rc != 0 and len(_lmp(log, 'UT')) == 2)
        shutil.copytree(os.path.join(ul, 'UB'), os.path.join(ul, 'UVa'))   # 관문을 거치지 않은 폴더 (같은 꼴 · 같은 덱 사본 · 요약 없음)
        mp = os.path.join(ul, 'UVa', 'run_manifest.txt')
        mtext = _read(mp).replace('job=UB', 'job=UVa').replace('gate=ALLOW\n', '')
        open(mp, 'w').write(mtext)
        os.remove(os.path.join(ul, 'UVa', 'ul_summary.txt'))
        shutil.copy(os.path.join(kit, 'decks', B73, 'in.U_UVa.liggghts'), os.path.join(ul, 'UVa', 'deck.liggghts'))
        open(os.path.join(ul, 'UVa', 'deck.txt'), 'w').write('in.U_UVa.liggghts\n')
        rc, out = _run(os.path.join(td, 'b'), kit, B73, 'UVa', {'RESUME': '1'})
        chk('M14 ULKR-06 같은 승인 팔의 기술 재개인지 검증 — 첫 시도 기록에 관문 ALLOW 가 없는 폴더 = 이어 돌림 거부 (관문 건너뛰기 없음 · lmp 호출 없음)',
            lambda: 'job=UVa' in mtext and rc != 0 and '관문 ALLOW' in out and not _lmp(log, 'UVa'))
        shutil.rmtree(os.path.join(ul, 'UVa'))
        rc, out = _run(os.path.join(td, 'b'), kit, B73, 'UC', {'MOCK_PROCS': '4'})
        chk('M8 화면 "Loop time … on 4 procs" (≠ NP 6) = 기술 실패 (rc ≠ 0 · run_check FAIL · 잡 기록 stage 줄)',
            lambda: rc != 0 and 'FAIL' in open(os.path.join(ul, 'UC', 'run_check.txt')).read()
            and re.search(r'^stage=UC .*rc=0 check=.*procs', _read(os.path.join(ul, 'UC', 'run_manifest.txt')), re.M))
        shutil.rmtree(os.path.join(ul, 'UT'))
        rc, out = _run(os.path.join(td, 'b'), kit, B73, 'UT')
        rc2, out2 = _run(os.path.join(td, 'b'), kit, B73, 'UVb')
        rc3, out3 = _run(os.path.join(td, 'b'), kit, B73, 'UTc')
        utc = _lmp(log, 'UTc')
        rm_ut = [ln.split(',') for ln in _read(os.path.join(ul, 'UT', 'ul_events.csv')).splitlines() if ln.startswith('RM,')]
        rms = rm_ut[0][2] if rm_ut else 'none'
        man_c = _read(os.path.join(ul, 'UTc', 'run_manifest.txt'))
        sums_c = _read(os.path.join(ul, 'UTc', 'parent_UT.sha256'))
        chk('M9 UT (δ_dt 0.2 · R_M 에서 멈춤) → UVb 허용 → 튜플 t3 → UTc = U_UT3 덱을 UT 의 R_M restart · 상태에서 ul_resume 1',
            lambda: rc == 0 and rc2 == 0 and rc3 == 0 and utc and f'restart_RM_{rms}.bin' in utc[0] and f'state_RM_{rms}.in' in utc[0]
            and 'ul_resume=1' in utc[0] and open(os.path.join(ul, 'UTc', 'deck.txt')).read().strip() == 'in.U_UT3.liggghts')
        chk('M9 ULKR-03 UTc 는 UT 기록 · 덤프를 복사하지 않는다 — 기록 CSV = 머리만 (+ 덱이 쓴 이어 돌림 줄) · run_manifest = continues=UT · parent_dir · rm_step · '
            'parent_sums (+ 그 sha256) · parent_UT.sha256 = UT 기록 · 덤프 sha256',
            lambda: _read(os.path.join(ul, 'UTc', 'ul_steps.csv')).count('\n') == 1 and _read(os.path.join(ul, 'UTc', 'ul_windows.csv')).count('\n') == 1
            and re.search(r'^continues=UT$', man_c, re.M) and re.search(rf'^parent_dir={re.escape(os.path.join(ul, "UT"))}$', man_c, re.M)
            and re.search(rf'^rm_step={rms}$', man_c, re.M) and re.search(r'^parent_sums=parent_UT\.sha256$', man_c, re.M)
            and re.search(rf'^parent_sums_sha256={_sha(os.path.join(ul, "UTc", "parent_UT.sha256"))}$', man_c, re.M)
            and re.search(r'  ul_windows\.csv$', sums_c, re.M) and re.search(r'  dump/atom_\d+\.dump$', sums_c, re.M)
            and not os.listdir(os.path.join(ul, 'UTc', 'dump')))
        rep = subprocess.run([sys.executable, '-I', os.path.join(kit, 'ul_reader.py'), 'report', work2], capture_output=True, text=True, timeout=300)
        r73 = (json.load(open(os.path.join(work2, 'report.json'))).get('beds') or {}).get(B73) or {} if rep.returncode == 0 else {}
        chk('M9 ULKR-03 최종 report (t3) = UT 주 값 (OK · UT 폴더 판독) + UTc 보조 (부모 해시 대조 · 이어 돌림 OK)',
            lambda: r73.get('primary_status') == 'OK' and r73.get('job') == 'UT+UTc'
            and ((r73.get('utc') or {}).get('continuation') or {}).get('status') == 'OK' and (r73.get('utc') or {}).get('primary_status') == 'OK')
        rc, out = _run(os.path.join(td, 'b'), kit, 'ps_3_7_r45', 'UB')
        chk('M10 다른 침대: 복원 전 거부 (최종 튜플이 있어도)', lambda: rc != 0 and 'REFUSE' in out)
        # ── ULKR-06 미지원 JOB 의 RESUME = 거부 (분명한 사유 · 기록 보존 · lmp 호출 없음) ──
        snap = {n: _sha_or_none(os.path.join(ul, 'UTc', n)) for n in ('screen.txt', 'run_manifest.txt', 'ul_events.csv')}
        n_utc = len(_lmp(log, 'UTc'))
        rc, out = _run(os.path.join(td, 'b'), kit, B73, 'UTc', {'RESUME': '1'})
        chk('M11 ULKR-06 RESUME UTc = 거부 ("RESUME 거부" · 개정 3 §14-4) · lmp 호출 없음 · UTc 화면 · 기록 그대로 · screen_a2 없음',
            lambda: rc != 0 and 'RESUME 거부' in out and len(_lmp(log, 'UTc')) == n_utc and not os.path.exists(os.path.join(ul, 'UTc', 'screen_a2.txt'))
            and all(_sha_or_none(os.path.join(ul, 'UTc', n)) == h for n, h in snap.items()))
        rc, out = _run(os.path.join(td, 'b'), kit, B73, 'G_UT3')
        n_g = len(_lmp(log, 'G_UT3'))
        gsnap = _sha_or_none(os.path.join(ul, 'G_UT3', 'screen.txt'))
        rc2, out2 = _run(os.path.join(td, 'b'), kit, B73, 'G_UT3', {'RESUME': '1'})
        chk('M12 ULKR-06 RESUME G_UT3 = 거부 · 첫 시도 화면 그대로 · lmp 호출 늘지 않음 (원 팔 R_M 에서 다시 시작하지 않는다)',
            lambda: rc == 0 and n_g == 1 and rc2 != 0 and 'RESUME 거부' in out2 and len(_lmp(log, 'G_UT3')) == 1
            and gsnap and _sha_or_none(os.path.join(ul, 'G_UT3', 'screen.txt')) == gsnap)
        n_all = len(_calls(log))
        res = [_run(os.path.join(td, 'b'), kit, b, j, {'RESUME': '1'}) for b, j in ((B73, 'RJ'), ('ps_10_0_r45', 'EXT'), ('ps_10_0_r45', 'RJ2'))]
        chk('M13 ULKR-06 RESUME RJ · EXT · RJ2 = 거부 (사유 · 다시 = 새 시도 안내) · 어떤 lmp · mpirun 호출도 없음',
            lambda: all(r != 0 and 'RESUME 거부' in o and '새 시도' in o for r, o in res) and len(_calls(log)) == n_all)
        # ── ULKR-11 G0 · Ut0 기술 실패 = R 을 돌리지 않는다 · 판독기 프로그램 오류 ↔ 정상 미식별 ──
        kit_c, work_c, log_c = _setup(os.path.join(td, 'c'))
        ld = os.path.join(work_c, B73, 'in', P_bed(B73)['last_deck'])
        open(ld, 'w').write(_read(ld).replace('pair_style gran model hooke/hysteresis', 'pair_style gran model hooke'))
        rc, out = _run(os.path.join(td, 'c'), kit_c, B73, 'RJ')
        man_c = _read(os.path.join(work_c, B73, 'RJ', 'run_manifest.txt'))
        chk('M15 ULKR-11 G0 실패 (원 마지막 조각 덱 ≠ 언로딩 머리) = Ut0 · R · UN · UK 를 돌리지 않는다 · 잡 기록 stage=G0 rc≠0 · 복원 증서 RESTORED 아님 · rc ≠ 0',
            lambda: rc != 0 and not [c for c in _calls(log_c) if c.startswith('lmp ')] and re.search(r'^stage=G0 rc=[1-9]', man_c, re.M)
            and (json.load(open(os.path.join(work_c, B73, 'RJ', 'restore_verdict.json'))).get('status') != 'RESTORED'))
        kit_d, work_d, log_d = _setup(os.path.join(td, 'd'))
        rc, out = _run(os.path.join(td, 'd'), kit_d, B73, 'RJ', {'MOCK_FAIL_KIND': 'Ut0'})
        kinds_d = [re.search(r'out=\S+/RJ/(\w+)', c).group(1) for c in _calls(log_d) if c.startswith('lmp ')]
        chk('M16 ULKR-11 7:3 Ut0 기술 실패 = R · UN · UK 를 돌리지 않는다 (lmp 호출 = Ut0 하나) · 잡 기록 stage=Ut0 rc≠0 · rc ≠ 0',
            lambda: rc != 0 and kinds_d == ['Ut0'] and re.search(r'^stage=Ut0 .*rc=[1-9]', _read(os.path.join(work_d, B73, 'RJ', 'run_manifest.txt')), re.M))
        kit_e, work_e, log_e = _setup(os.path.join(td, 'e'))
        rc0, _o = _run(os.path.join(td, 'e'), kit_e, B73, 'RJ', {'PY': os.path.join(td, 'e', 'bin', 'pywrap'), 'MOCK_RESTORE_AS': 'RESTORED'})
        open(os.path.join(work_e, B73, 'RJ', 'restore_verdict.json'), 'w').write(json.dumps({'status': 'RESTORED'}))
        rc, out = _run(os.path.join(td, 'e'), kit_e, B73, 'UB', {'PY': os.path.join(td, 'e', 'bin', 'pywrap'), 'MOCK_READER_FAIL': 'arm'})
        man_e = _read(os.path.join(work_e, B73, 'UB', 'run_manifest.txt'))
        rcu, outu = _run(os.path.join(td, 'e'), kit_e, B73, 'UC')
        man_u = _read(os.path.join(work_e, B73, 'UC', 'run_manifest.txt'))
        chk('M17 ULKR-11 판독기 프로그램 오류 (arm rc 1) = 잡 기록 reader_arm_rc=1 · 러너 rc ≠ 0 (LMP 는 성공) ↔ 정상 미식별 (UC 빈 기록 · JSON) = reader_arm_rc=0 · rc 0',
            lambda: rc != 0 and re.search(r'^reader_arm_rc=1$', man_e, re.M) and re.search(r'^stage=U_UB .*rc=0 check=PASS', man_e, re.M)
            and rcu == 0 and re.search(r'^reader_arm_rc=0$', man_u, re.M)
            and json.load(open(os.path.join(work_e, B73, 'UC', 'arm_verdict.json'))).get('primary_status') != 'OK')
        # ── ULKR-09 불완전 UK (Codex one_uk_row) = KE 기준 파일 미발행 → S2 를 쓰는 다음 팔 관문 거부 ──
        kit_f, work_f, log_f = _setup(os.path.join(td, 'f'))
        rc, out = _run(os.path.join(td, 'f'), kit_f, B73, 'RJ', {'MOCK_UK_ONEROW': '1'})
        man_f = _read(os.path.join(work_f, B73, 'RJ', 'run_manifest.txt'))
        open(os.path.join(work_f, B73, 'RJ', 'restore_verdict.json'), 'w').write(json.dumps({'status': 'RESTORED'}))
        rc2, out2 = _run(os.path.join(td, 'f'), kit_f, B73, 'UB')
        chk('M18 ULKR-09 UK 한 줄 (step 1 · w 1 · 회전 0.001 J) = kebase rc 2 · ul_base.in 없음 · 잡 기록 reader_kebase_rc=2 · 러너 rc ≠ 0 → UB 관문 거부 (lmp 호출 없음)',
            lambda: rc != 0 and re.search(r'^stage=UK .*rc=0 check=PASS', man_f, re.M) and re.search(r'^reader_kebase_rc=2$', man_f, re.M)
            and not os.path.exists(os.path.join(work_f, B73, 'ul_base.in')) and rc2 != 0 and 'REFUSE' in out2 and not _lmp(log_f, 'UB'))
        # ── ULKR-12 경량 보고 묶음 — 판정에 쓴 결정 파일을 함께 (RJ · RJ2 = ul_base.in · 7:3 = selection.json · EXT = EXT2 · s0_decision.json) ──
        import tarfile
        kit_g, work_g, log_g = _setup(os.path.join(td, 'g'), beds=(B73, 'ps_10_0_r45'))
        tg = os.path.join(td, 'g')

        def members(bed, job):
            p = os.path.join(work_g, bed, f'{job}.report.tgz')
            return set(tarfile.open(p).getnames()) if os.path.exists(p) else set()
        rc_rj, out_rj = _run(tg, kit_g, B73, 'RJ', {'PY': os.path.join(tg, 'bin', 'pywrap'), 'MOCK_RESTORE_AS': 'RESTORED'})
        open(os.path.join(work_g, B73, 'RJ', 'restore_verdict.json'), 'w').write(json.dumps({'status': 'RESTORED'}))
        rc_ub, out_ub = _run(tg, kit_g, B73, 'UB')
        for f, t in (('restore_verdict.json', json.dumps({'status': 'RESTORED'})),
                     ('run_manifest.txt', 'bed=ps_10_0_r45\njob=RJ\nresume=0\ngrammar_prereq=PASS\nend=x fails=0 reader_rc=0\n')):
            os.makedirs(os.path.join(work_g, 'ps_10_0_r45', 'RJ'), exist_ok=True)
            open(os.path.join(work_g, 'ps_10_0_r45', 'RJ', f), 'w').write(t)
        rc_ext, out_ext = _run(tg, kit_g, 'ps_10_0_r45', 'EXT')
        m_rj, m_ub, m_ext = members(B73, 'RJ'), members(B73, 'UB'), members('ps_10_0_r45', 'EXT')
        chk('M19 ULKR-12 경량 묶음에 판정 결정 파일: RJ (7:3) = ul_base.in · UB (7:3) = selection.json · EXT = EXT2/ · s0_decision.json · '
            '보낼 것 줄 = "모든 관측을 다시 검증하는 원천 아님"',
            lambda: 'ul_base.in' in m_rj and any(n.startswith('RJ/') for n in m_rj) and 'selection.json' in m_ub
            and any(n.startswith('EXT2/') for n in m_ext) and 's0_decision.json' in m_ext and any(n.startswith('EXT/') for n in m_ext)
            and '다시 검증하는 원천 아님' in out_ub and not [n for n in m_ext if n.endswith('.bin')])
        # ── ULKRR-03 판독기가 결과 파일을 쓴 뒤 실패 (rc 120) = 다음 팔 관문 거부 (fails=0 이어도) · 판독 오류를 rc 0 으로 삼키지 않는다 ──
        res3 = {}
        for name in ('restore', 'kebase'):
            tx = os.path.join(td, f'e_{name}')
            kx, wx, lx = _setup(tx)
            rcx, _o = _run(tx, kx, B73, 'RJ', {'PY': os.path.join(tx, 'bin', 'pywrap'), 'MOCK_RESTORE_AS': 'RESTORED', 'MOCK_READER_FAIL_AFTER': name})
            vp = os.path.join(wx, B73, 'RJ', 'restore_verdict.json')
            stx = json.load(open(vp)).get('status') if os.path.exists(vp) else None
            rcu, outu = _run(tx, kx, B73, 'UB')
            res3[name] = (rcx, stx, _read(os.path.join(wx, B73, 'RJ', 'run_manifest.txt')), os.path.exists(os.path.join(wx, B73, 'ul_base.in')), rcu, outu,
                          _lmp(lx, 'UB'))
        chk('M20 ULKRR-03 restore 가 RESTORED 증서를 쓴 뒤 rc 120 → 잡 기록 reader_restore_rc=120 · 끝 줄 fails=0 reader_rc=120 · 러너 rc ≠ 0 → UB 관문 거부 (lmp 호출 없음)',
            lambda: (lambda r: r[0] != 0 and r[1] == 'RESTORED' and re.search(r'^reader_restore_rc=120$', r[2], re.M)
                     and re.search(r'^end=.* fails=0 reader_rc=120$', r[2], re.M) and r[4] != 0 and 'REFUSE' in r[5] and not r[6])(res3['restore']))
        chk('M20 ULKRR-03 kebase 가 기준 파일 ul_base.in 을 쓴 뒤 rc 120 → 잡 기록 reader_kebase_rc=120 · 끝 줄 fails=0 reader_rc=2 → UB 관문 거부 (lmp 호출 없음)',
            lambda: (lambda r: r[0] != 0 and r[1] == 'RESTORED' and r[3] and re.search(r'^reader_kebase_rc=120$', r[2], re.M)
                     and re.search(r'^end=.* fails=0 reader_rc=2$', r[2], re.M) and r[4] != 0 and 'REFUSE' in r[5] and not r[6])(res3['kebase']))
        # ── Q4 (다) EXT — 등록된 연장 요청 (s0p rc 2) 만 EXT2 · 그 밖 비영 rc (판독기 프로그램 오류) = 멈춤 · RRC 보존 ──
        tk = os.path.join(td, 'k')
        kit_k, work_k, log_k = _setup(tk, beds=(B73, 'ps_10_0_r45'))
        for f, t in (('restore_verdict.json', json.dumps({'status': 'RESTORED'})),
                     ('run_manifest.txt', 'bed=ps_10_0_r45\njob=RJ\nresume=0\ngrammar_prereq=PASS\nend=x fails=0 reader_rc=0\n')):
            os.makedirs(os.path.join(work_k, 'ps_10_0_r45', 'RJ'), exist_ok=True)
            open(os.path.join(work_k, 'ps_10_0_r45', 'RJ', f), 'w').write(t)
        rc_k, out_k = _run(tk, kit_k, 'ps_10_0_r45', 'EXT', {'PY': os.path.join(tk, 'bin', 'pywrap'), 'MOCK_READER_FAIL_ONCE': 's0p',
                                                              'MOCK_ONCE_FLAG': os.path.join(tk, 'once.flag')})
        man_k = _read(os.path.join(work_k, 'ps_10_0_r45', 'EXT', 'run_manifest.txt'))
        chk('M21 Q4 (다) EXT 첫 s0p 가 판독기 프로그램 오류 (rc 1 — 등록된 연장 요청 rc 2 아님) → EXT2 를 돌리지 않는다 · reader_s0p_rc=1 한 번 · 끝 줄 reader_rc=1 '
            '(0 으로 되돌리지 않는다) · 러너 rc ≠ 0',
            lambda: rc_k != 0 and _lmp(log_k, 'EXT') and not _lmp(log_k, 'EXT2') and man_k.count('reader_s0p_rc=') == 1
            and re.search(r'^reader_s0p_rc=1$', man_k, re.M) and re.search(r'^end=.* reader_rc=1$', man_k, re.M), man_k[-300:])
        chk('M21 대조: 정상 EXT (s0p rc 2 = S0′ 미달 · 등록된 연장 요청) → EXT2 를 돌린다 (M19 의 같은 러너 · EXT2 lmp 호출)',
            lambda: bool(_lmp(log_g, 'EXT2')) and re.search(r'^reader_s0p_rc=2$', _read(os.path.join(work_g, 'ps_10_0_r45', 'EXT', 'run_manifest.txt')), re.M))
        # ── Q5 문법 fixture PASS = R · EXT 전 사전 점검 (LIGGGHTS 전 거부 · 1저자 10-14 강제) ──
        th = os.path.join(td, 'h')
        kit_h, work_h, log_h = _setup(th, beds=(B73, 'ps_10_0_r45'))
        res5 = {}
        for name in ('none', 'status_fail', 'deck', 'lmp'):
            gx = None if name == 'none' else (_gram_variant(gv, os.path.join(td, f'gv_{name}'), name) if gv else os.path.join(td, 'nope.json'))
            n0 = len(_calls(log_h))
            rcx, outx = _run(th, kit_h, B73, 'RJ', {'GRAMMAR_VERDICT': gx})
            res5[name] = (rcx, '문법 fixture' in outx, len(_calls(log_h)) - n0, os.path.isdir(os.path.join(work_h, B73, 'RJ')))
            shutil.rmtree(os.path.join(work_h, B73, 'RJ'), ignore_errors=True)
        chk('M22 Q5 RJ (본 R) — 문법 fixture 판정 없음 · FAIL · 덱 사본 sha256 다름 · LMP sha256 다름 = 사전 점검 거부 (LIGGGHTS · mpirun 호출 0 · RJ 폴더 없음)',
            lambda: all(r[0] != 0 and r[1] and r[2] == 0 and not r[3] for r in res5.values()), str(res5))
        n0 = len(_calls(log_h))
        rc_e5, out_e5 = _run(th, kit_h, 'ps_10_0_r45', 'EXT', {'GRAMMAR_VERDICT': None})
        chk('M22 Q5 EXT (10:0 이완 연장) — 문법 fixture 판정 없음 = 사전 점검 거부 (관문보다 먼저 · LIGGGHTS 호출 0 · EXT 폴더 없음)',
            lambda: rc_e5 != 0 and '문법 fixture' in out_e5 and len(_calls(log_h)) == n0 and not os.path.isdir(os.path.join(work_h, 'ps_10_0_r45', 'EXT')))
        rc_p5, out_p5 = _run(th, kit_h, B73, 'RJ', {'GRAMMAR_VERDICT': None}, args=('--preflight-only',))
        chk('M22 Q5 --preflight-only 도 같은 검사 (제출 전 사전 점검에서 먼저 보인다)', lambda: rc_p5 != 0 and '문법 fixture' in out_p5)
        rc_o5, out_o5 = _run(th, kit_h, B73, 'RJ')
        man_h = _read(os.path.join(work_h, B73, 'RJ', 'run_manifest.txt'))
        chk('M22 Q5 양성: 지금 history_test 러너 · 읽는 쪽이 낸 PASS 판정 (같은 가짜 바이너리) → 사전 점검 통과 → RJ 진행 (LIGGGHTS 호출) · '
            '잡 기록 grammar_prereq=PASS · 판정 경로 · sha256',
            lambda: bool(_lmp(log_h, 'Ut0')) and re.search(r'^grammar_prereq=PASS$', man_h, re.M) and re.search(r'^grammar_verdict_sha256=[0-9a-f]{64}$', man_h, re.M)
            and re.search(r'^grammar_verdict=\S+grammar_verdict\.json$', man_h, re.M), man_h[:600])
        # ── ULKRR-02 러너 수준 양성 대조 — 기계 실패 뒤 RESUME=1 (러너 resume_from · 덱 RESUME = 상태 파일 k) → 남긴 줄을 버리고 주 값 OK · 다음 관문 ──
        ti = os.path.join(td, 'i')
        kit_i, work_i, log_i = _setup(ti)
        _run(ti, kit_i, B73, 'RJ', {'PY': os.path.join(ti, 'bin', 'pywrap'), 'MOCK_RESTORE_AS': 'RESTORED'})
        rc_b, _o = _run(ti, kit_i, B73, 'UB')
        rc_1, _o = _run(ti, kit_i, B73, 'UT', {'MOCK_ROLLBACK_KIND': 'UT'})
        rc_2, out_2 = _run(ti, kit_i, B73, 'UT', {'MOCK_ROLLBACK_KIND': 'UT', 'RESUME': '1'})
        avp = os.path.join(work_i, B73, 'UT', 'arm_verdict.json')
        av = json.load(open(avp)) if os.path.exists(avp) else {}
        man_i = _read(os.path.join(work_i, B73, 'UT', 'run_manifest.txt'))
        g5 = subprocess.run([sys.executable, '-I', os.path.join(kit_i, 'ul_reader.py'), 'gate', work_i, B73, 'UVb'], capture_output=True, text=True, timeout=300)
        chk('M23 ULKRR-02 러너 수준 양성 대조 — UT 기계 실패 (단 1 끝 restart 뒤 단 2 창 둘 · 단 줄 · 사건을 남기고 rc 1) → RESUME=1 (러너 resume_from = 그 restart step · '
            '덱 RESUME = 상태 파일 k 1) → 판독기가 남긴 줄 3 을 버림 · UT 주 값 OK · δ_dt 0.2 → UVb 관문 ALLOW',
            lambda: rc_b == 0 and rc_1 != 0 and rc_2 == 0 and av.get('primary_status') == 'OK' and av.get('n_superseded_rows') == 3
            and re.search(r'^resume_from=\d+$', man_i, re.M) and g5.returncode == 0 and 'ALLOW' in g5.stdout,
            f'{rc_b} {rc_1} {rc_2} {av.get("primary_status")} {av.get("n_superseded_rows")} {av.get("why")} {g5.stdout.strip()}')
        # ── Q6 UC = fresh-attempt-only · 새 폴더 = 새 시도 (앞 시도 보존 · 잡 기록에 남긴다 — 재시도 한도 · 결과 선택을 초기화하지 않는다) ──
        rc_uc, _o = _run(ti, kit_i, B73, 'UC')
        uc = os.path.join(work_i, B73, 'UC')
        snap_uc = {n: _sha_or_none(os.path.join(uc, n)) for n in ('run_manifest.txt', 'screen.txt')}
        n_uc = len(_lmp(log_i, 'UC'))
        rc_ur, out_ur = _run(ti, kit_i, B73, 'UC', {'RESUME': '1'})
        chk('M24 Q6 RESUME UC = 거부 ("fresh-attempt-only" · 새 시도 안내) · lmp 호출 없음 · UC 기록 · 화면 그대로 (앞에서 거부)',
            lambda: rc_uc == 0 and rc_ur != 0 and 'fresh-attempt-only' in out_ur and len(_lmp(log_i, 'UC')) == n_uc
            and all(h and _sha_or_none(os.path.join(uc, n)) == h for n, h in snap_uc.items()))
        os.rename(uc, uc + '.try1')
        rc_uf, out_uf = _run(ti, kit_i, B73, 'UC')
        chk('M24 Q6 새 폴더 = 새 시도 — 앞 시도 폴더 UC.try1 보존 · 새 잡 기록에 prior_attempts=UC.try1 (러너가 남긴다 · 한도 판단 = 1저자)',
            lambda: rc_uf == 0 and os.path.isdir(uc + '.try1') and re.search(r'^prior_attempts=UC\.try1$', _read(os.path.join(uc, 'run_manifest.txt')), re.M))
        # ── Q3 (1저자 10-15 · Codex 수정 재확인 Q4) — M22 양성과 같은 PASS 판정 JSON 그대로 · 그 런 GA 화면에 ERROR 를 덧붙이면 (원자료 ≠ 판정) 사전 점검이
        #    승인된 판독기로 다시 읽어 RJ 의 LIGGGHTS 전에 멈춘다 (마지막 시험 — 같은 문법 런을 쓰는 앞 시험 뒤에 고친다) ──
        tk = os.path.join(td, 'q3')
        kit_k, work_k, log_k = _setup(tk)
        ga_scr = os.path.join(os.path.dirname(gv), 'GA', 'screen.out') if gv else os.path.join(td, 'nope', 'screen.out')
        if os.path.exists(ga_scr):
            with open(ga_scr, 'a', encoding='utf-8') as f:
                f.write('ERROR: injected raw error after the PASS verdict (Q3 시험)\n')
        n0 = len(_calls(log_k))
        rc_q3, out_q3 = _run(tk, kit_k, B73, 'RJ')
        chk('M25 Q3 문법 판정 JSON (PASS) 그대로 · 그 런 GA 화면 끝에 ERROR 덧붙임 (Codex raw_ga_error_cached_pass) → 사전 점검이 원자료 재판독에서 거부 · '
            'LIGGGHTS · mpirun 호출 0 · RJ 폴더 없음 (옛 판 = RJ 진행)',
            lambda: os.path.exists(ga_scr) and rc_q3 != 0 and '문법 fixture' in out_q3 and '재판독' in out_q3 and len(_calls(log_k)) == n0
            and not os.path.isdir(os.path.join(work_k, B73, 'RJ')), out_q3[-600:])
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
