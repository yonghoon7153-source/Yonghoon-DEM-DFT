#!/usr/bin/env python3
"""resume_ckpt.sh 시험 — 가짜 SLURM (sbatch · sacct · squeue · sleep) 과 가짜 dem_restart.py 로 스크립트 전체를 실제로 돌린다.

KG50-02 (실패한 재개 시험이 본 런으로 승격) · KG50-10 (재개 덱 ↔ 본 덱 정적 대조) · 1저자 10-26 *"50kg 권고대로해"* Q2.
반례 다섯 = Codex 판정문 docs/reviews/codex_kg50_decks_review_20261026/codex_review_kg50_decks_20261026.md §3 표 (step 1 재개 → 이번 덱의 step 20001 재개로 옮김).
-c (10-27 · 1저자 *"권고대로"*) — ibb 의 dem_restart.py 가 덱 머리 주석의 템플릿 이름 (real_4) 도 "다른 케이스명 혼입" 으로 거부했다
(kg50_d07_b40 r56).  가짜 dem_restart.py 엄격판 (FAKE_DEM_RESTART_STRICT) 이 그 검사를 흉내 낸다 (N1–N6b).
실제 LIGGGHTS · SLURM 호출 0 · 임시 폴더만 쓴다.

  python3 scripts/test_resume_ckpt.py                 # 고친 스크립트 (기본)
  python3 scripts/test_resume_ckpt.py --script <경로>  # 다른 판 (고치기 전 판 실패 확인용)
"""
import glob
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, 'scripts', 'resume_ckpt.sh')
MAIN = os.path.join(ROOT, 'docs/data/kg50_decks_20261026_v2/kg50_d07_b40/input_kg50_d07_b40.liggghts')
MAIN_INS = os.path.join(ROOT, 'docs/data/kg50_decks_20261026_v2/kg50_d07_b40/input_kg50_d07_b40_insert.liggghts')
R075 = os.path.join(ROOT, 'docs/data/pure_se_r075_20260927')
C, SUF, NP = 'kg50_d07_b40', 'ins1', 56
SFX = 'r%d' % NP
CKPT = 'restart_%s/restart_settling_20001.bin' % C
HDR = 'Step Atoms KinEng CPU'

STUB_SBATCH = r'''#!/bin/sh
f=""; for a in "$@"; do f="$a"; done
b=$(basename "$f" .sh); n=${b#run_}
case "$b" in
  *t) echo "trial $f" >> "$CAPTURE"; [ -n "$FAKE_TRIAL_LOG" ] && cp "$FAKE_TRIAL_LOG" "logs/output_${n}_7001.out"; echo 7001;;
  *) echo "main $f" >> "$CAPTURE"; echo 9001;;
esac
'''
STUB_SACCT = '#!/bin/sh\nprintf "%s\\n" "$FAKE_SACCT"\nexit ${FAKE_SACCT_RC:-0}\n'
STUB_SQUEUE = r'''#!/bin/sh
for a in "$@"; do [ "$a" = "-j" ] && exit 0; done
[ -n "$FAKE_SQUEUE" ] && printf '%s\n' "$FAKE_SQUEUE"
exit ${FAKE_SQUEUE_RC:-0}
'''
FAKE_DEM_RESTART = r'''#!/usr/bin/env python3
import os, shutil, sys
a = sys.argv
case, root, sfx = a[a.index('--case-list') + 1], a[a.index('--root') + 1], a[a.index('--suffix') + 1]
W = os.path.join(root, case)
shutil.copy(os.environ['FAKE_RES'], os.path.join(W, 'input_%s_%s.liggghts' % (case, sfx)))
with open(os.path.join(W, 'run_%s_%s.sh' % (case, sfx)), 'w') as f:
    f.write('#!/bin/bash\n#SBATCH --job-name=%s_%s\n#SBATCH -n 1\n#SBATCH --time=5-00:00:00\n'
            'cd $HOME/dem_test/%s\nmpirun -np 1 lmp_mpi -in input_%s_%s.liggghts\n' % (case, sfx, case, case, sfx))
print('  %s  %s  %s' % (case, os.environ.get('FAKE_MODE', 'settling'), os.environ.get('FAKE_CKPT', '')))
'''
# 엄격판 = ibb dem_restart.py 의 덱 검사 흉내 (10-27 실측 plan_r56.txt: "kg50_d07_b40 덱 검증 실패: 다른 케이스명 혼입: ['real_4']").
# 작업 폴더의 맨 위 input*.liggghts 어느 줄에든 (주석 줄 · 인라인 주석 포함) 다른 케이스 이름 (FAKE_FOREIGN) 이 있으면
# 재개 덱 · 러너 · 계획 줄 없이 끝낸다.  ⚠ 실제 도구가 어느 덱 · 어떤 이름 목록을 보는지는 리포에 없어 모른다 — 가정.
FAKE_NAME_CHECK = r'''names = [n for n in os.environ.get('FAKE_FOREIGN', 'real_4').split(',') if n]
found = sorted(set(n for p in glob.glob(os.path.join(W, 'input*.liggghts'))
                   for l in open(p, encoding='utf-8', errors='replace') for n in names if n in l))
if found:
    print('  %s 덱 검증 실패: 다른 케이스명 혼입: %r' % (case, found))
    sys.exit(0)
'''
assert FAKE_DEM_RESTART.count('import os, shutil, sys\n') == 1 and FAKE_DEM_RESTART.count('W = os.path.join(root, case)\n') == 1
FAKE_DEM_RESTART_STRICT = FAKE_DEM_RESTART.replace('import os, shutil, sys\n', 'import glob, os, shutil, sys\n').replace(
    'W = os.path.join(root, case)\n', 'W = os.path.join(root, case)\n' + FAKE_NAME_CHECK)
# 줄 전체 주석 (첫 공백 아닌 글자 '#') 한 줄 — 시험 쪽 기대값을 스크립트와 다른 방법 (정규식) 으로 셈
COMMENT_LINE = re.compile(rb'^[ \t\r\x0b\x0c]*#.*(?:\n|\Z)', re.M)


def strip_expect(data):
    """줄 전체 주석을 뺀 바이트 · 뺀 줄 수 · 남은 바이트 (= 비주석 줄) sha256."""
    out, n = COMMENT_LINE.subn(b'', data)
    return out, n, hashlib.sha256(out).hexdigest()


def bsub(data, old, new):
    assert data.count(old) == 1, old
    return data.replace(old, new)


def thermo(rows):
    return [HDR] + ['%8d %8d %14s %10s' % r for r in rows]


ORIG_LOG = '\n'.join(
    ['LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, compiled 2026-03-26-14:37:06 by yonghoon, git commit 3d5c00f)']
    + thermo([(0, 0, '0', '0'), (1, 312506, '0.11', '0.5')])
    + ['Loop time of 0.5 on 1 procs for 1 steps with 312506 atoms',
       '====== INSERTED 312506 / 312506 (floor 309380 = 99%) ======', '====== PHASE 1: SETTLING ======']
    + thermo([(1, 312506, '0.11', '0')] + [(k, 312506, '%.4f' % (0.2 - k * 5e-6), '%d' % (k // 100))
                                          for k in range(1000, 20001, 1000)] + [(20001, 312506, '0.1000', '200.01')])
    + ['Loop time of 200 on 1 procs for 20000 steps with 312506 atoms']
    + thermo([(20001, 312506, '0.1000', '0'), (21000, 312506, '0.0950', '10'), (22000, 312506, '0.0900', '20'),
              (23000, 312506, '0.0850', '30'), (23001, 312506, '0.0850', '30.01')])
    + ['Loop time of 30 on 1 procs for 3000 steps with 312506 atoms', '']) + '\n'

T_OK = thermo([(20001, 312506, '0.1000', '0'), (21000, 312506, '0.0955', '1'), (22000, 312506, '0.0902', '2'),
               (22001, 312506, '0.0902', '2.001')]) + ['Loop time of 2.001 on 56 procs for 2000 steps with 312506 atoms']


def trial_log(kind):
    if kind == 'ok':
        rows = T_OK
    elif kind == 'setup_only':
        rows = T_OK[:2] + ['MPI process exited on signal 11']
    elif kind == 'after_first':
        rows = T_OK[:3] + ['MPI process exited on signal 11']
    elif kind == 'ke_tampered':
        rows = [r.replace('0.0955', '0.1910') for r in T_OK]
    elif kind == 'error':
        rows = T_OK[:2] + ['ERROR: test failure (fix_insert_pack.cpp:42)']
    elif kind == 'truncated':
        rows = T_OK[:3]
    elif kind == 'sparse':  # 원 로그의 21000 줄이 시험에 없다 (thermo 간격이 다른 시험)
        rows = [T_OK[0], T_OK[1], T_OK[3], T_OK[4], T_OK[5]]
    elif kind == 'no_loop':
        rows = T_OK[:-1]
    elif kind == 'warning_mid':  # 실행 중간의 WARNING 줄 — 정상 시험을 실패로 보지 않는다
        rows = T_OK[:3] + ['WARNING: Fix mesh: Mesh contains highly skewed element (fix_mesh.cpp:300)'] + T_OK[3:]
    else:
        raise ValueError(kind)
    return '\n'.join(['LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0)'] + rows) + '\n'


def res_good():
    out, skip, settle = [], False, False
    with open(MAIN, encoding='utf-8') as f:
        for raw in f:
            s = raw.strip()
            if re.match(r'fix\s+(pts\d+|pdd_mix)\b', s) or s.startswith('create_box'):
                continue
            if re.match(r'fix\s+ins_mix\b', s):
                skip = True
            if 'PHASE 1: SETTLING' in s:
                skip = False
            if skip:
                continue
            out.append(raw)
            if s.startswith('processors'):
                out.append('read_restart %s\n' % CKPT)
            if 'PHASE 1: SETTLING' in s:
                settle = True
            if settle and re.match(r'run\s+200000\b', s):
                out[-1] = 'run 180000\n'
                settle = False
    return ''.join(out)


def mutate(text, old, new, count=1):
    assert old in text, old
    return text.replace(old, new, count)


def res_variant(kind):
    g = res_good()
    if kind == 'good':
        return g
    if kind == 'reinsert':  # 본 덱의 삽입 fix 문장 전체 ('&' 로 이어진 줄까지) 를 read_restart 뒤에 그대로
        raw, take = [], False
        for l in open(MAIN, encoding='utf-8'):
            take = take or bool(re.match(r'\s*fix\s+ins_mix\b', l))
            if take:
                raw.append(l)
                if not l.rstrip().endswith('&'):
                    break
        return mutate(g, 'read_restart %s\n' % CKPT, 'read_restart %s\n%s' % (CKPT, ''.join(raw)))
    if kind == 'damp_wrong':
        return mutate(g, 'fix damp all viscous 1.0e-5', 'fix damp all viscous 0.5')
    if kind == 'damp_missing':
        return mutate(g, 'fix damp all viscous 1.0e-5\n', '')
    if kind == 'steps_wrong':
        return mutate(g, 'run 180000\n', 'run 200000\n')
    if kind == 'extra_fix':
        return mutate(g, 'run 180000\n', 'fix extra all viscous 0.1\nrun 180000\n')
    if kind == 'var_changed':
        return re.sub(r'(variable\s+press_speed\s+equal\s+)\S+', r'\g<1>0.02', g, count=1)
    if kind == 'tail_changed':
        return re.sub(r'\nrun 100000\n', '\nrun 50000\n', g, count=1)
    if kind == 'mesh_scale':
        return mutate(g, 'reference_point 0 0 0', 'reference_point 0 0 0 scale 2.0')
    if kind == 'compute_missing':
        return re.sub(r'\ncompute\s+zmax\b[^\n]*\n', '\n', g, count=1)
    raise ValueError(kind)


def tree_sha(d):
    """폴더 안 모든 파일 → sha256 (상대 경로 기준) · 심볼릭 링크는 'link:' + 가리키는 경로."""
    out = {}
    for base, _, files in os.walk(d):
        for n in files:
            p = os.path.join(base, n)
            if os.path.islink(p):
                out[os.path.relpath(p, d)] = 'link:' + os.readlink(p)
                continue
            with open(p, 'rb') as f:
                out[os.path.relpath(p, d)] = hashlib.sha256(f.read()).hexdigest()
    return out


def run_case(script, res_kind, trial, sacct='COMPLETED|0:0', sacct_rc=0, squeue='', squeue_rc=0, extra=(),
             fake=FAKE_DEM_RESTART, main_bytes=None, more_decks=(), main_link=False):
    # fake · main_bytes (멈춘 폴더의 본 덱 내용) · more_decks ((이름, 바이트) — 멈춘 폴더에 더 넣을 덱) = 기본값이면 예전 그대로
    # main_link = 멈춘 폴더의 본 덱을 같은 폴더 main_real.liggghts 를 가리키는 절대 경로 링크로 (cp -a 뒤에도 원본을 가리킨다)
    tmp = tempfile.mkdtemp(prefix='rck_')
    try:
        L, home, stub = (os.path.join(tmp, x) for x in ('root', 'home', 'bin'))
        S = os.path.join(L, '%s.%s' % (C, SUF))
        for d in (os.path.join(S, 'restart_' + C), os.path.join(S, 'post_' + C), os.path.join(home, 'dem_test'), stub):
            os.makedirs(d)
        tgt = os.path.join(S, 'main_real.liggghts' if main_link else 'input_%s.liggghts' % C)
        if main_bytes is None:
            shutil.copy(MAIN, tgt)
        else:
            with open(tgt, 'wb') as f:
                f.write(main_bytes)
        if main_link:
            os.symlink(tgt, os.path.join(S, 'input_%s.liggghts' % C))
        for name, body in more_decks:
            with open(os.path.join(S, name), 'wb') as f:
                f.write(body)
        with open(os.path.join(S, 'log.liggghts'), 'w') as f:
            f.write(ORIG_LOG)
        with open(os.path.join(S, CKPT), 'wb') as f:
            f.write(b'\x00' * 64)
        for name, body in (('sbatch', STUB_SBATCH), ('sacct', STUB_SACCT), ('squeue', STUB_SQUEUE), ('sleep', '#!/bin/sh\nexit 0\n')):
            p = os.path.join(stub, name)
            with open(p, 'w') as f:
                f.write(body)
            os.chmod(p, 0o755)
        with open(os.path.join(home, 'dem_test', 'dem_restart.py'), 'w') as f:
            f.write(fake)
        res = os.path.join(tmp, 'res.liggghts')
        with open(res, 'w') as f:
            f.write(res_variant(res_kind))
        tl = ''
        if trial:
            tl = os.path.join(tmp, 'trial.out')
            with open(tl, 'w') as f:
                f.write(trial_log(trial))
        cap = os.path.join(tmp, 'capture.txt')
        open(cap, 'w').close()
        env = dict(os.environ, HOME=home, PATH=stub + ':' + os.environ['PATH'], USER='tester', CAPTURE=cap,
                   FAKE_SACCT=sacct, FAKE_SACCT_RC=str(sacct_rc), FAKE_SQUEUE=squeue, FAKE_SQUEUE_RC=str(squeue_rc),
                   FAKE_TRIAL_LOG=tl, FAKE_RES=res, FAKE_CKPT=CKPT)
        s_before = tree_sha(S)
        p = subprocess.run(['bash', script, '-n', str(NP), '-s', SUF, '-r', L] + list(extra) + [C],
                           env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=600)
        s_after = tree_sha(S)
        with open(cap) as f:
            calls = f.read().split()
        reps = glob.glob(os.path.join(L, 'resume_%s_*.md' % SFX))
        rep = open(reps[0], encoding='utf-8').read() if reps else ''
        W = os.path.join(L, C)
        w_decks = {}
        for q in glob.glob(os.path.join(W, 'input*.liggghts')):
            with open(q, 'rb') as f:
                w_decks[os.path.basename(q)] = f.read()
        plan = os.path.join(W, 'plan_%s.txt' % SFX)
        plan = open(plan, encoding='utf-8', errors='replace').read() if os.path.isfile(plan) else ''
        return dict(trial='trial' in calls, main='main' in calls, rep=rep,
                    out=p.stdout.decode('utf-8', 'replace'), rc=p.returncode,
                    s_before=s_before, s_after=s_after, w_decks=w_decks, plan=plan)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def deckcheck_only(script, main, res, ckpt, s0, workdir_files=()):
    tmp = tempfile.mkdtemp(prefix='rckc_')
    try:
        for n in workdir_files:
            open(os.path.join(tmp, n), 'w').close()
        p = subprocess.run(['bash', script, '-C', main, res, ckpt, str(s0), tmp],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
        return p.returncode, p.stdout.decode('utf-8', 'replace')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    script = SCRIPT
    if '--script' in sys.argv:
        script = sys.argv[sys.argv.index('--script') + 1]
    ok = fail = 0

    def chk(name, cond, detail=''):
        nonlocal ok, fail
        if cond:
            ok += 1
            print('PASS', name)
        else:
            fail += 1
            print('FAIL', name, '·', detail[-1500:].replace('\n', ' | '))

    # ── Codex §3 반례 다섯 (step 20001 재개로 옮김) ──
    r = run_case(script, 'good', 'ok')
    chk('K1 정상 완료 → 본 제출', r['trial'] and r['main'], r['rep'] + r['out'])
    chk('K1b 보고에 G0 통과 줄', 'G0' in r['rep'] and '통과' in r['rep'], r['rep'])
    r = run_case(script, 'good', 'setup_only', sacct='FAILED|0:11')
    chk('K2 FAILED · setup 줄만 → 본 제출 안 함', r['trial'] and not r['main'], r['rep'] + r['out'])
    r = run_case(script, 'good', 'after_first', sacct='FAILED|0:11')
    chk('K3 FAILED · 21000 뒤 중단 → 본 제출 안 함', r['trial'] and not r['main'], r['rep'] + r['out'])
    r = run_case(script, 'good', 'ke_tampered')
    chk('K4 정상 완료 · 21000 KE 변조 → 본 제출 안 함', r['trial'] and not r['main'], r['rep'] + r['out'])
    r = run_case(script, 'good', 'error', sacct='FAILED|1:0')
    chk('K5 ERROR 줄 → 본 제출 안 함', r['trial'] and not r['main'], r['rep'] + r['out'])
    r = run_case(script, 'good', 'warning_mid')
    chk('K6 정상 완료 · 중간 WARNING 줄 → 본 제출', r['trial'] and r['main'], r['rep'] + r['out'])
    # ── 상태 · 끝 · 조회 (Codex 처방) ──
    r = run_case(script, 'good', 'ok', sacct='COMPLETED|1:0')
    chk('S1 COMPLETED 인데 ExitCode 1:0 → 본 제출 안 함', not r['main'], r['rep'] + r['out'])
    r = run_case(script, 'good', 'truncated')
    chk('S2 COMPLETED 인데 끝 step 21000 (기대 22001) → 본 제출 안 함', not r['main'], r['rep'] + r['out'])
    r = run_case(script, 'good', 'no_loop')
    chk('S3 끝 step 맞지만 Loop time 없음 → 본 제출 안 함', not r['main'], r['rep'] + r['out'])
    r = run_case(script, 'good', 'ok', sacct='', sacct_rc=1)
    chk('S4 sacct 조회 실패 → 본 제출 안 함', not r['main'], r['rep'] + r['out'])
    r = run_case(script, 'good', 'ok', sacct='RUNNING|0:0')
    chk('S5 끝나지 않음 (대기 시간 초과) → 본 제출 안 함', not r['main'], r['rep'] + r['out'])
    r = run_case(script, 'good', None, sacct='COMPLETED|0:0')
    chk('S6 시험 로그 없음 → 본 제출 안 함', not r['main'], r['rep'] + r['out'])
    r = run_case(script, 'good', 'sparse')
    chk('S7 원 로그의 비교 줄 (21000) 이 시험에 없음 → 본 제출 안 함', not r['main'], r['rep'] + r['out'])
    # ── 재개 덱 정적 대조 (KG50-10) — 실패면 시험도 안 낸다 ──
    for kind, label in (('reinsert', '재삽입 fix'), ('damp_wrong', '정착 감쇠가 다른 단계 값 (0.5)'),
                        ('damp_missing', '정착 감쇠 fix 빠짐'), ('steps_wrong', '남은 정착 step 이 200000 (끝 220001)'),
                        ('extra_fix', '본 덱에 없는 fix'), ('var_changed', '판 속도 변수 0.02'),
                        ('tail_changed', '이완 run 100000 → 50000'), ('mesh_scale', '판 메시 줄이 파일 말고도 다름'),
                        ('compute_missing', '뒤에서 쓰는 compute zmax 정의 빠짐')):
        r = run_case(script, kind, 'ok')
        chk('D %s → 시험 · 본 제출 안 함' % label, not r['trial'] and not r['main'], r['out'])
    # ── 큐 이름 · -T ──
    r = run_case(script, 'good', 'ok', squeue='%s_ins' % C)
    chk('Q1 삽입 잡 (%s_ins) 이 큐에 있음 → 건너뜀' % C, not r['trial'] and not r['main'], r['out'])
    r = run_case(script, 'good', 'ok', squeue='%s_r56' % C)
    chk('Q2 같은 케이스 재개 잡 (%s_r56) 이 큐에 있음 → 건너뜀' % C, not r['trial'] and not r['main'], r['out'])
    r = run_case(script, 'good', 'ok', squeue='%sx\n%s_s2' % (C, C))
    chk('Q3 이름이 겹치기만 하는 다른 잡 → 막지 않음', r['trial'] and r['main'], r['rep'] + r['out'])
    r = run_case(script, 'good', 'ok', squeue_rc=1)
    chk('Q4 squeue 조회 실패 → 건너뜀', not r['trial'] and not r['main'], r['out'])
    r = run_case(script, 'good', 'ok', extra=('-T',))
    chk('T1 -T 시험만 → 시험은 내고 본 제출 안 함', r['trial'] and not r['main'] and '시험만' in r['rep'], r['rep'] + r['out'])
    # ── -C: 실제 09-27 재개 덱 쌍 (dem_restart.py 산출 · 압축 단계) ──
    m075 = os.path.join(R075, 'input_pse_r075_a.liggghts')
    r075 = os.path.join(R075, 'input_pse_r075_a_r30.liggghts')
    rc, out = deckcheck_only(script, m075, r075, 'restart_pse_r075_a/restart_compress_1500000.bin', 1500000,
                             ('plate_pse_r075_a_r30.stl',))
    chk('C1 실제 09-27 쌍 (압축 재개) → 통과', rc == 0 and '통과' in out, out)
    rc, out = deckcheck_only(script, m075, r075, 'restart_pse_r075_a/restart_compress_1500000.bin', 1500000)
    chk('C2 같은 쌍 · 새 판 메시 파일 없음 → 실패', rc != 0 and '판 메시 파일' in out, out)
    tmp = tempfile.mkdtemp(prefix='rckm_')
    try:
        bad = os.path.join(tmp, 'bad.liggghts')
        with open(r075, encoding='utf-8') as f:
            txt = f.read()
        with open(bad, 'w', encoding='utf-8') as f:
            f.write(txt.replace('fix damp all viscous 0.5', 'fix damp all viscous 0.05', 1))
        rc, out = deckcheck_only(script, m075, bad, 'restart_pse_r075_a/restart_compress_1500000.bin', 1500000,
                                 ('plate_pse_r075_a_r30.stl',))
        chk('C3 같은 쌍 · 압축 감쇠 0.05 로 바꿈 → 실패', rc != 0 and 'damp' in out, out)
        rc, out = deckcheck_only(script, m075, r075, 'restart_pse_r075_a/restart_foo_1500000.bin', 1500000,
                                 ('plate_pse_r075_a_r30.stl',))
        chk('C4 체크포인트 이름이 본 덱의 restart 줄과 안 맞음 → 실패', rc != 0 and '체크포인트' in out, out)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    # ── -c: 작업 사본 덱의 줄 전체 주석 빼기 (10-27 ibb · dem_restart.py 가 덱 머리 주석의 템플릿 이름 real_4 도 거부) ──
    with open(MAIN, 'rb') as f:
        mb = f.read()
    with open(MAIN_INS, 'rb') as f:
        ib = f.read()
    nm, ni = 'input_%s.liggghts' % C, 'input_%s_insert.liggghts' % C
    ins = ((ni, ib),)
    rej = "다른 케이스명 혼입: ['real_4']"
    r = run_case(script, 'good', 'ok', fake=FAKE_DEM_RESTART_STRICT, more_decks=ins)
    chk('N1 덱 머리 주석에 템플릿 이름 real_4 · -c 없음 → 재개 덱 못 만듦 · 시험 · 본 제출 안 함 · 보고에 케이스 절 없음 (ibb 10-27 재현)',
        rej in r['plan'] and '재개 덱 못 만듦' in r['out'] and not r['trial'] and not r['main']
        and ('## %s' % C) not in r['rep'], r['plan'] + r['out'] + r['rep'])
    r = run_case(script, 'good', 'ok', fake=FAKE_DEM_RESTART_STRICT, more_decks=ins, extra=('-c',))
    em, nmc, hm = strip_expect(mb)
    ei, nic, hi = strip_expect(ib)

    def has(text, name, n, h):
        # 그 덱 이름의 한 줄에 뺀 줄 수와 비주석 줄 sha256 (전 = 후) 가 같이 있다
        return any(name + ':' in l and ('주석 %d 줄 뺌' % n) in l and ('sha256 전 %s = 후 %s' % (h, h)) in l
                   for l in text.splitlines())
    cmd = next((l for l in r['rep'].splitlines() if l.startswith('명령:')), '')
    chk('N2 -c → 작업 사본 덱 둘의 줄 전체 주석만 빠짐 (시험 쪽 정규식 계산과 바이트 같음) → 재개 덱 · 시험 · 본 제출',
        r['trial'] and r['main'] and nmc > 0 and nic > 0 and r['w_decks'].get(nm) == em and r['w_decks'].get(ni) == ei
        and b'real_4' not in em + ei, r['out'] + r['rep'])
    chk('N2b 기록 = stdout · 보고 둘 다 덱마다 뺀 줄 수 · 비주석 줄 sha256 전 = 후 · 보고 명령 줄에 -c',
        ' -c ' in cmd and has(r['out'], nm, nmc, hm) and has(r['out'], ni, nic, hi)
        and has(r['rep'], nm, nmc, hm) and has(r['rep'], ni, nic, hi), r['out'] + r['rep'])
    chk('N3 -c 뒤 멈춘 폴더 (원본) 의 모든 파일 sha256 그대로 · 작업 사본 덱만 바뀜',
        r['s_before'] == r['s_after'] and r['s_after'].get(nm) == hashlib.sha256(mb).hexdigest()
        and r['s_after'].get(ni) == hashlib.sha256(ib).hexdigest() and r['w_decks'].get(nm) == em, r['out'])
    r = run_case(script, 'good', 'ok', fake=FAKE_DEM_RESTART_STRICT, more_decks=ins, extra=('-c',), main_link=True)
    chk('N3b 멈춘 폴더 본 덱 = 멈춘 폴더 안 파일로 가는 절대 경로 링크 (cp -a 뒤 작업 사본도 원본을 가리킴) · -c → 원본 · 링크 그대로 · 작업 사본만 새 파일',
        r['trial'] and r['main'] and r['s_before'] == r['s_after'] and r['s_after'].get('main_real.liggghts') == hashlib.sha256(mb).hexdigest()
        and r['s_after'].get(nm, '').startswith('link:') and r['w_decks'].get(nm) == em, r['out'])
    il =b'fix m2 all property/global poissonsRatio peratomtype 0.25 0.25 0.30'
    mi = bsub(mb, il + b'\n', il + b'   # note real_4\n')
    r = run_case(script, 'good', 'ok', fake=FAKE_DEM_RESTART_STRICT, main_bytes=mi, more_decks=ins, extra=('-c',))
    chk('N4 -c 는 인라인 주석을 안 뺀다 (한계) — fix 줄 뒤 "# note real_4" 는 남고 줄 전체 주석만 빠짐 → 여전히 거부 · 시험 안 함',
        r['w_decks'].get(nm) == strip_expect(mi)[0] and (il + b'   # note real_4\n') in r['w_decks'].get(nm, b'')
        and rej in r['plan'] and '재개 덱 못 만듦' in r['out'] and not r['trial'] and not r['main'], r['plan'] + r['out'])
    r = run_case(script, 'good', 'ok', fake=FAKE_DEM_RESTART_STRICT, main_bytes=em, extra=('-c',))
    chk('N5 -c · 줄 전체 주석 없는 덱 → 0 줄 뺌 · 덱 그대로 · 재개 덱 · 시험 · 본 제출',
        r['trial'] and r['main'] and r['w_decks'].get(nm) == em and has(r['rep'], nm, 0, hashlib.sha256(em).hexdigest()),
        r['out'] + r['rep'])
    # LIGGGHTS 는 '&' 로 다음 줄을 붙인 뒤 주석을 지운다 — 이어 붙이기 안의 주석 줄 · '&' 로 끝나는 주석 줄은 빼면 명령이 바뀐다
    m3 = b'fix m3 all property/global coefficientRestitution peratomtypepair 3 &\n'
    m1 = b'fix m1 all property/global youngsModulus'
    for tag, bad in (('N6 이어 붙이기 (&) 안의 주석 줄', bsub(mb, m3, m3 + '# 반발 계수 (real_4 와 같음)\n'.encode())),
                     ('N6b & 로 끝나는 주석 줄 (다음 fix 줄을 삼킨다)', bsub(mb, m1, '# real_4 와 같음 &\n'.encode() + m1))):
        r = run_case(script, 'good', 'ok', fake=FAKE_DEM_RESTART_STRICT, main_bytes=bad, more_decks=ins, extra=('-c',))
        chk('%s · -c → 빼면 LIGGGHTS 명령이 바뀜 → ⛔ 건너뜀 (dem_restart.py · 시험 · 본 제출 안 함) · 작업 사본 덱 둘 다 그대로' % tag,
            '⛔ 주석 줄 빼기' in r['out'] and r['plan'] == '' and not r['trial'] and not r['main']
            and r['w_decks'].get(nm) == bad and r['w_decks'].get(ni) == ib, r['out'])
    print('%d PASS · %d FAIL' % (ok, fail))
    return 0 if fail == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
