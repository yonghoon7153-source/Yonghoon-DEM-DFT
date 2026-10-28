#!/usr/bin/env python3
"""resume_ckpt.sh 시험 — 가짜 SLURM (sbatch · sacct · squeue · sleep) 과 가짜 dem_restart.py 로 스크립트 전체를 실제로 돌린다.

KG50-02 (실패한 재개 시험이 본 런으로 승격) · KG50-10 (재개 덱 ↔ 본 덱 정적 대조) · 1저자 10-26 *"50kg 권고대로해"* Q2.
반례 다섯 = Codex 판정문 docs/reviews/codex_kg50_decks_review_20261026/codex_review_kg50_decks_20261026.md §3 표 (step 1 재개 → 이번 덱의 step 20001 재개로 옮김).
-c (10-27 · 1저자 *"권고대로"*) — ibb 의 dem_restart.py 가 덱 머리 주석의 템플릿 이름 (real_4) 도 "다른 케이스명 혼입" 으로 거부했다
(kg50_d07_b40 r56).  가짜 dem_restart.py 엄격판 (FAKE_DEM_RESTART_STRICT) 이 그 검사를 흉내 낸다 (N1–N6b).
KG50-18 · 19 (10-28 · Codex 재확인 요청서 docs/reviews/codex_kg50_resume_tool_recheck_request_20261027.md §4-1 · §4-2 ·
1저자 *"50kg 권고대로 해"* ④ ⑤) — A = after_settling 재개 (시험 = 판 높이 run 1 + 시험 run → G0 기대 끝 = S0 + 둘의 합) ·
P = 시험 덱 run 합을 못 정하는 꼴은 시험 전에 거부 · W = write_restart · 루프 체크포인트 재개 덱의 첫 긴 run 대조 (-C).
after_settling 재개 덱 · 로그는 합성이다 (실제 dem_restart.py 산출 · LIGGGHTS 로그 아님 — 요청서 §4 의 구성 그대로).
실제 LIGGGHTS · SLURM 호출 0 · 임시 폴더만 쓴다.
10-28 밤 (Codex 재검토 docs/reviews/codex_kg50_resume_recheck_20261028/ · 수정 계획 docs/50kg/kg50_resume_recheck_fix_plan_20261028.md ·
1저자 *"50kg도 권고대로해"* Q1–Q5 · 원장 KG50R-01–05 · 07) — R = 이번 호출이 낸 시험만 본 제출 (같은 작업 폴더를 남긴 채 두 번 호출 ·
Codex probe_stale_trial.py 두 장면을 옮김 — 승인값 · 가짜 dem_restart.py 를 준다 · 그 탐침 그대로는 -A · -H 가 없어 새 판의 승인 거부로
끝나 Q1 을 못 본다) · G = 전체 프로그램 대조 (Codex 덱 고정물을 그대로 읽어 -C · 원본 → 시험 덱 → 관문 사슬) · X = 압축 체크포인트 재개
거부 · L = G0 마지막 thermo 줄 · Loop step 수 (우리 재현 g0_lastrun/ 로그 포함) · I = 도구 신원 · 승인 · -T 본 제출 명령 (G0–G3 통과
케이스만) · Q9 = 시험 전 거부의 보고 케이스 절.  Codex 고정물은 읽기만 한다 (신뢰하지 않는 입력 · 실행 안 함).

  python3 scripts/test_resume_ckpt.py                 # 고친 스크립트 (기본)
  python3 scripts/test_resume_ckpt.py --script <경로>  # 다른 판 (고치기 전 판 실패 확인용)
  python3 scripts/test_resume_ckpt.py --compare-old <옛 판>
      # 장면마다 옛 판도 같은 입력으로 돌려 stdout · 보고 · 작업 폴더 파일 · 제출 여부를 대조 (임시 경로 · 날짜 시각만 맞춤 ·
      # 10-28 밤 새로 더한 줄 (표지 'KG50R' 가 든 줄) · 시도 폴더 · cut_*.txt 는 빼고 · 승인 인자 -A · -H 는 새 판에만)
      # → 묶음별 같음 / 다름 · 예전부터 있던 묶음 (K S D Q T N F C A P W) 에서 옛 판 · 새 판 둘 다 정상 (시험 · G0–G3 통과 / -C 통과)
      #   인 장면에 다름이 있으면 rc 1 · 새 묶음 (R G X L I Q9) 의 다름 · 옛 판 정상인데 새 판이 거부한 장면은 목록으로 보고만
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
# 10-28 KG50-18 · 19: after_settling (write_restart) 체크포인트 · v3 50×50 본 덱 (요청서 §4-2 의 -C 합성 자리)
CKPT_AS = 'restart_%s/restart_after_settling.bin' % C
C50 = 'kg50_d07_b50'
MAIN50 = os.path.join(ROOT, 'docs/data/kg50_decks_20261027_v3_b50/%s/input_%s.liggghts' % (C50, C50))
# --compare-old: 옛 판 경로 · 지금 묶음 이름 · 장면마다 (묶음, 설명, 다른 항목, 옛 판 정상 장면?)
CMP = {'old': None, 'grp': '', 'rows': []}
# 10-28 밤: Codex 재검토 고정물 (읽기만 · 실행 안 함) · 우리 재현 G0 로그
CODEX = os.path.join(ROOT, 'docs/reviews/codex_kg50_resume_recheck_20261028')
CX_DECK = os.path.join(CODEX, 'independent/deck')
CX_SCHED = os.path.join(CODEX, 'independent/scheduler')
G0_LOGS = os.path.join(CODEX, '_repro_ours_20261028/g0_lastrun')
Q3MSG = '압축 체크포인트 재개 = 지원 안 함 (KG50R-01 · 1저자 10-28 Q3 (가))'
# 고치기 전 판 (e59c43e6) 693 줄 시험 덱 절단기 — 정상 재개 덱에서 새 절단기 (--cut-trial) 와 바이트가 같아야
OLD_CUT = '{if($1=="run" && $2+0>1){n=$2+0; if(n>t)n=t; print "run " n; exit} print}'
NEW_MARK = 'KG50R'               # 10-28 밤 새로 더한 출력 줄의 표지 (--compare-old 가 빼고 대조)

# 가짜 sbatch — 시험 job = 7000 + (이 루트에서 낸 시험 수) · 본 job = 9000 + (본 제출 수) (두 번 호출에도 번호가 겹치지 않게)
#   FAKE_SBATCH_TRIAL_EMPTY = 시험 제출이 빈 출력 · FAKE_TOUCH_HELPER = 시험 제출 때 그 파일 (dem_restart.py) 에 한 줄 덧붙임
STUB_SBATCH = r'''#!/bin/sh
f=""; for a in "$@"; do f="$a"; done
b=$(basename "$f" .sh); n=${b#run_}
case "$b" in
  *t) echo "trial $f" >> "$CAPTURE"
      [ -n "$FAKE_TOUCH_HELPER" ] && echo "# 시험 제출 뒤 바뀜" >> "$FAKE_TOUCH_HELPER"
      [ -n "$FAKE_SBATCH_TRIAL_EMPTY" ] && exit 0
      [ -n "$FAKE_SBATCH_TRIAL_TEXT" ] && { echo "$FAKE_SBATCH_TRIAL_TEXT"; exit 1; }
      j=$((7000 + $(grep -c '^trial' "$CAPTURE")))
      [ -n "$FAKE_TRIAL_LOG" ] && cp "$FAKE_TRIAL_LOG" "logs/output_${n}_$j.out"; echo $j;;
  *) echo "main $f" >> "$CAPTURE"; echo $((9000 + $(grep -c '^main' "$CAPTURE")));;
esac
'''
STUB_SACCT = '#!/bin/sh\nprintf "%s\\n" "$FAKE_SACCT"\nexit ${FAKE_SACCT_RC:-0}\n'
# 가짜 squeue — 호출 번호를 센다 ($CAPTURE.sq · 호출마다 harness 가 지움) · FAKE_SQUEUE_SECOND 면 둘째 호출부터 FAKE_SQUEUE_2 · _RC_2 ·
#   -o '%i %j' 면 'id 이름' (줄에 칸 하나면 id 0) · 그 밖 (-o %j) 은 마지막 칸 (이름)
STUB_SQUEUE = r'''#!/bin/sh
fmt=""; prev=""
for a in "$@"; do [ "$a" = "-j" ] && exit 0; [ "$prev" = "-o" ] && fmt="$a"; prev="$a"; done
c=$(cat "$CAPTURE.sq" 2>/dev/null || echo 0); c=$((c+1)); echo $c > "$CAPTURE.sq"
out="$FAKE_SQUEUE"; rc=${FAKE_SQUEUE_RC:-0}
if [ "$c" -ge 2 ] && [ -n "$FAKE_SQUEUE_SECOND" ]; then out="$FAKE_SQUEUE_2"; rc=${FAKE_SQUEUE_RC_2:-0}; fi
[ -n "$out" ] && printf '%s\n' "$out" | awk -v f="$fmt" '{ if (f == "%i %j") { if (NF == 1) print "0", $1; else print } else print $NF }'
exit $rc
'''
FAKE_DEM_RESTART = r'''#!/usr/bin/env python3
import os, shutil, sys
a = sys.argv
case, root, sfx = a[a.index('--case-list') + 1], a[a.index('--root') + 1], a[a.index('--suffix') + 1]
W = os.path.join(root, case)
if os.environ.get('FAKE_DEM_FAIL'):
    print('  제외: %s (가짜 · 체크포인트 없음)' % case)
    sys.exit(0)
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


def block(hdr, rows):
    return [hdr] + ['  '.join('%8s' % v for v in r) for r in rows]


# after_settling 원 로그 (합성 · 요청서 §4-1): 정착 끝 200001 → write_restart → 판 높이 run 1 (c_zmax · 200001 · 200002) →
# 안정화 run 200000 중 230000 에서 멈춤 (Loop time 없음).  G2 = PLATE HEIGHT 줄 · G1 = step 200001 의 c_zmax 줄.
AS_ZH, AS_SH = 'Step Atoms c_zmax', 'Step Atoms KinEng CPU pressMPa'
AS_PLATE = '====== PLATE HEIGHT: 0.0605557 ======'
AS_ZROWS = [(200001, 312506, '0.0505557'), (200002, 312506, '0.0505557')]
AS_MID = ['====== SETTLING COMPLETE ======', '====== Z_MAX (center): 0.0505557 ======', AS_PLATE, '====== PHASE 2: STABILIZE ======']


def as_ke(k):
    return '%.4f' % (0.02 - (k - 200000) * 2e-7)


AS_LOG = '\n'.join(
    ['LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, compiled 2026-03-26-14:37:06 by yonghoon, git commit 3d5c00f)']
    + thermo([(0, 0, '0', '0'), (1, 312506, '0.11', '0.5')])
    + ['Loop time of 0.5 on 1 procs for 1 steps with 312506 atoms',
       '====== INSERTED 312506 / 312506 (floor 309380 = 99%) ======', '====== PHASE 1: SETTLING ======']
    + thermo([(1, 312506, '0.11', '0')] + [(k, 312506, '%.4f' % (0.1 - k * 4e-7), '%d' % (k // 100))
                                          for k in range(50000, 200001, 50000)] + [(200001, 312506, '0.0200', '2000.01')])
    + ['Loop time of 2000 on 1 procs for 200000 steps with 312506 atoms', '====== RESTART SAVED ======']
    + block(AS_ZH, AS_ZROWS) + ['Loop time of 0.01 on 1 procs for 1 steps with 312506 atoms'] + AS_MID
    + block(AS_SH, [(200002, 312506, '0.0200', '0', '0')]
            + [(k, 312506, as_ke(k), '%d' % ((k - 200000) // 100), '0') for k in range(201000, 230001, 1000)])
    + ['']) + '\n'


def as_trial(end=202002):
    """after_settling 시험 로그 (합성): run 1 (200001 → 200002) + run 2000 (→ end) + Loop time.  정상 끝 = 200001 + 1 + 2000."""
    rows = (['LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0)'] + block(AS_ZH, AS_ZROWS)
            + ['Loop time of 0.01 on 56 procs for 1 steps with 312506 atoms'] + AS_MID
            + block(AS_SH, [(200002, 312506, '0.0200', '0', '0')]
                    + [(k, 312506, as_ke(k), '%d' % ((k - 200000) // 1000), '0') for k in (201000, 202000)]
                    + [(end, 312506, as_ke(202000), '2.002', '0')])
            + ['Loop time of 2.002 on 56 procs for %d steps with 312506 atoms' % (end - 200002)])
    return '\n'.join(rows) + '\n'


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
    # 10-27 ibb kg50_d2_b50 r4 — 실제 dem_restart.py 의 settling 잔여 = 200000 − 20001 = 179999 (본 덱 정착 run 은 삽입 run 1 뒤
    # step 1 에서 시작 → 끝 200001 · 맞는 남은 step 180000).  F 꼴 = 고칠 수 있는 꼴 하나 + 고치면 안 되는 꼴들.
    if kind == 'steps_ibb':
        return mutate(g, 'run 180000\n', 'run 179999\n')
    if kind == 'steps_ibb_comment':
        return mutate(g, 'run 180000\n', '  run   179999   # settling 잔여\n')
    if kind == 'steps_minus2':
        return mutate(g, 'run 180000\n', 'run 179998\n')
    if kind == 'steps_plus1':
        return mutate(g, 'run 180000\n', 'run 180001\n')
    if kind == 'steps_ibb_extra':
        return mutate(g, 'run 180000\n', 'fix extra all viscous 0.1\nrun 179999\n')
    if kind == 'steps_ibb_amp':
        return mutate(g, 'run 180000\n', 'run &\n179999\n')
    if kind == 'steps_ibb_upto':
        return mutate(g, 'run 180000\n', 'run 200000 upto\n')
    # 10-28 KG50-18 — 시험 덱 (= 이 덱을 첫 긴 run 에서 자른 것) 의 run 합을 못 정하는 꼴 · 정하는 꼴 (첫 긴 run 앞에 한 줄 더)
    pre = {'p_if_run': 'if "1 > 0" then "run 100"\n', 'p_reset': 'reset_timestep 0\n',
           'p_jump': 'jump SELF skip1\nlabel skip1\n', 'p_include': 'include extra.in\n', 'p_upto': 'run 1 upto\n',
           'p_var': 'run ${n_settle}\n', 'p_every': 'run 1 every 1 NULL\n', 'p_run0': 'run 0 pre no post no\n',
           'p_run1': 'run 1\n', 'p_if_else': 'if "1 > 0" then "print a" else "run 100"\n', 'p_varcmd': '${cmdx} 100\n',
           'p_rr2': 'read_restart %s\n' % CKPT,
           'p_ifprint': ('variable n_ins equal count(all)\nif "${n_ins} < 309380" then &\n'
                         '    "print \'FATAL: partial insertion - bed composition differs (PS-01). aborting.\'" &\n'
                         '    "quit 1"\n')}
    if kind in pre:
        return mutate(g, 'run 180000\n', pre[kind] + 'run 180000\n')
    raise ValueError(kind)


def res_after(kind='good', main=MAIN, case=C, tmpl=False):
    """after_settling 재개 덱 (합성 · 요청서 §4-1 규칙): 본 덱에서 create_box · 템플릿 · 분포 · 삽입 블록 · 정착 run 200000 ·
    write_restart …after_settling 을 빼고 processors 뒤에 read_restart …/restart_after_settling.bin.
    tmpl = 도구가 비압축 재개에 하듯 read_restart 바로 뒤에 본 덱의 fix pts* · pdd_mix 줄 (요청서 §4-2 의 -C 합성 = 템플릿 줄 포함)."""
    with open(main, encoding='utf-8') as f:
        raw = f.readlines()
    tl = [l for l in raw if len(l.split()) >= 2 and l.split()[0] == 'fix' and re.match(r'^(pts[0-9]+|pdd_mix)$', l.split()[1])]
    out, skip, settle = [], False, False
    for l in raw:
        s = l.strip()
        if re.match(r'fix\s+(pts\d+|pdd_mix)\b', s) or s.startswith('create_box'):
            continue
        if re.match(r'fix\s+ins_mix\b', s):
            skip = True
        if 'PHASE 1: SETTLING' in s:
            skip, settle = False, True
        if skip:
            continue
        if settle and re.match(r'run\s+200000\b', s):
            settle = False
            continue
        if s.startswith('write_restart') and 'restart_after_settling.bin' in s:
            continue
        out.append(l)
        if s.startswith('processors'):
            out.append('read_restart restart_%s/restart_after_settling.bin\n' % case)
            if tmpl:
                out.extend(tl)
    g = ''.join(out)
    assert g.count('read_restart') == 1 and g.count('write_restart restart_%s/restart_after_settling.bin' % case) == 0
    if kind == 'good':
        return g
    if kind.startswith('stab'):  # 안정화 run 200000 (정착 run 을 뺀 뒤 첫 run 200000) 의 길이만
        return mutate(g, 'run 200000\n', 'run %s\n' % kind[4:])
    if kind == 'damp_settle':  # 안정화 감쇠를 정착 값 그대로 (요청서 §4-2 — 상태 C 가 잡는 꼴)
        return mutate(g, 'fix damp all viscous 0.5\n', 'fix damp all viscous 1.0e-5\n')
    raise ValueError(kind)


def with_tmpl(text):
    """도구가 settling 재개 덱에 하는 일 (read_restart 바로 뒤에 본 덱의 fix pts* · pdd_mix 줄) 을 시험 쪽에서 따로 계산."""
    tl = [l if l.endswith('\n') else l + '\n' for l in open(MAIN, encoding='utf-8')
          if len(l.split()) >= 2 and l.split()[0] == 'fix' and re.match(r'^(pts[0-9]+|pdd_mix)$', l.split()[1])]
    out = []
    for l in text.splitlines(keepends=True):
        out.append(l)
        if l.split()[:1] == ['read_restart']:
            out.extend(tl)
    return ''.join(out)


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


def norm(s, tmp):
    # --compare-old 대조용: 임시 폴더 경로 · 날짜 시각 (보고 머리 줄) 만 맞춘다 · 10-28 밤 새 줄 (표지 NEW_MARK) 은 뺀다
    s = '\n'.join(l for l in s.split('\n') if NEW_MARK not in l)
    return re.sub(r'[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}', '<날짜 시각>', s.replace(tmp, '<임시>'))


def tree_cmp(d, tmp):
    # --compare-old 대조용 작업 폴더 지도 — 10-28 밤 새 파일 (시도 폴더 attempt_* · cut_*.txt) 빼고 · .txt 는 새 줄 뺀 내용의 sha256
    out = {}
    for rel, v in tree_sha(d).items():
        if rel.startswith('attempt_') or os.path.basename(rel).startswith('cut_'):
            continue
        p = os.path.join(d, rel)
        if rel.endswith('.txt') and not os.path.islink(p):
            with open(p, encoding='utf-8', errors='replace') as f:
                v = hashlib.sha256(norm(f.read(), tmp).encode()).hexdigest()
        out[rel] = v
    return out


def sha256f(p):
    with open(p, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def supports_approval(script):
    # 10-28 밤 Q4 판 (-A · -H) 인가 — 옛 판에는 승인 인자를 주지 않는다 (getopts 가 모르는 선택으로 끝난다)
    with open(script, encoding='utf-8', errors='replace') as f:
        return 'A:H:' in f.read()


def run_case(script, *a, **k):
    r = run_case1(script, *a, **k)
    if CMP['old'] is not None:  # 같은 입력으로 옛 판도 돌려 대조 (판정은 지금 판 r 로만)
        o = run_case1(CMP['old'], *a, **k)
        d = [x for x in ('trial', 'main', 'rc', 'out_n', 'rep_n', 'w_cmp', 's_same') if r[x] != o[x]]
        desc = ' '.join(str(x) for x in a if x) + ''.join(' %s=%s' % (x, str(k[x]).replace('\n', '\\n')) for x in sorted(k)
                                                         if x in ('extra', 'sacct', 'squeue', 'mode', 'main_link'))
        if 'res_text' in k:
            desc += ' (합성 재개 덱)'
        # 정상 장면 = 시험을 내고 G0–G3 를 통과 (본 제출 · 또는 -T 의 '🧪 시험만' 줄) — 옛 판 · 새 판 각각
        #   ('시험만' 글자만 보면 안 된다 — 새 판의 시도 줄 "이번 호출이 낸 시험만 …" 에도 든다)
        CMP['rows'].append((CMP['grp'], 'run ' + desc.strip(), d, o['trial'] and (o['main'] or '🧪 시험만 (-T)' in o['rep']),
                            r['trial'] and (r['main'] or '🧪 시험만 (-T)' in r['rep'])))
    return r


def make_root(fake=FAKE_DEM_RESTART, main_bytes=None, more_decks=(), main_link=False, ckpt=CKPT, orig_log=ORIG_LOG):
    # 임시 루트 하나 — 멈춘 폴더 <C>.ins1 (본 덱 · 원 로그 · 체크포인트) · 가짜 SLURM · 가짜 dem_restart.py.  두 번 호출 시험은 이 루트를 그대로 쓴다.
    # fake · main_bytes (멈춘 폴더의 본 덱 내용) · more_decks ((이름, 바이트) — 멈춘 폴더에 더 넣을 덱) = 기본값이면 예전 그대로
    # main_link = 멈춘 폴더의 본 덱을 같은 폴더 main_real.liggghts 를 가리키는 절대 경로 링크로 (cp -a 뒤에도 원본을 가리킨다)
    tmp = tempfile.mkdtemp(prefix='rck_')
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
        f.write(orig_log)
    os.makedirs(os.path.dirname(os.path.join(S, ckpt)), exist_ok=True)
    with open(os.path.join(S, ckpt), 'wb') as f:
        f.write(b'\x00' * 64)
    for name, body in (('sbatch', STUB_SBATCH), ('sacct', STUB_SACCT), ('squeue', STUB_SQUEUE), ('sleep', '#!/bin/sh\nexit 0\n')):
        p = os.path.join(stub, name)
        with open(p, 'w') as f:
            f.write(body)
        os.chmod(p, 0o755)
    helper = os.path.join(home, 'dem_test', 'dem_restart.py')
    with open(helper, 'w') as f:
        f.write(fake)
    cap = os.path.join(tmp, 'capture.txt')
    open(cap, 'w').close()
    return dict(tmp=tmp, L=L, home=home, stub=stub, S=S, cap=cap, helper=helper)


def snap_reports(L):
    return {p: (os.stat(p).st_mtime_ns, os.stat(p).st_size) for p in glob.glob(os.path.join(L, 'resume_%s_*.md' % SFX))}


def invoke(ctx, script, res_text, trial_text, sacct='COMPLETED|0:0', sacct_rc=0, squeue='', squeue_rc=0, squeue2=None,
           squeue_rc2=0, extra=(), mode='settling', ckpt=CKPT, approve='auto', suf=SUF, env_more=None, cases=None):
    # 한 번 호출 — 이 호출에서 생긴 sbatch 호출 · 보고 · stdout · 작업 폴더 상태만 돌려준다
    # approve: 'auto' = 새 판 · -T 없음이면 실제 sha256 둘 (-A 이 스크립트 · -H 가짜 dem_restart.py) · None = 안 줌 ·
    #   'badA' · 'badH' = 하나만 틀린 값 · squeue2 = 둘째 squeue 호출부터 (본 제출 직전 다시 조회) 의 출력
    tmp, L, cap = ctx['tmp'], ctx['L'], ctx['cap']
    res = os.path.join(tmp, 'res.liggghts')
    with open(res, 'w', newline='') as f:
        f.write(res_text)
    tl = ''
    if trial_text is not None:
        tl = os.path.join(tmp, 'trial.out')
        with open(tl, 'w') as f:
            f.write(trial_text)
    env = dict(os.environ, HOME=ctx['home'], PATH=ctx['stub'] + ':' + os.environ['PATH'], USER='tester', CAPTURE=cap,
               FAKE_SACCT=sacct, FAKE_SACCT_RC=str(sacct_rc), FAKE_SQUEUE=squeue, FAKE_SQUEUE_RC=str(squeue_rc),
               FAKE_TRIAL_LOG=tl, FAKE_RES=res, FAKE_CKPT=ckpt, FAKE_MODE=mode)
    for x in ('FAKE_SQUEUE_SECOND', 'FAKE_SQUEUE_2', 'FAKE_SQUEUE_RC_2', 'FAKE_SBATCH_TRIAL_EMPTY', 'FAKE_SBATCH_TRIAL_TEXT',
              'FAKE_TOUCH_HELPER', 'FAKE_DEM_FAIL'):
        env.pop(x, None)
    if squeue2 is not None:
        env.update(FAKE_SQUEUE_SECOND='1', FAKE_SQUEUE_2=squeue2, FAKE_SQUEUE_RC_2=str(squeue_rc2))
    env.update(dict((k, v.replace('{helper}', ctx['helper'])) for k, v in (env_more or {}).items()))
    if os.path.exists(cap + '.sq'):
        os.remove(cap + '.sq')
    args = ['bash', script, '-n', str(NP), '-s', suf, '-r', L] + list(extra)
    if approve and supports_approval(script):
        ta, ha = sha256f(script), sha256f(ctx['helper'])
        if approve == 'auto' and '-T' not in extra:
            args += ['-A', ta, '-H', ha]
        elif approve == 'badA':
            args += ['-A', '0' * 64, '-H', ha]
        elif approve == 'badH':
            args += ['-A', ta, '-H', '0' * 64]
    elif approve in ('badA', 'badH'):
        args += ['-A', '0' * 64, '-H', '0' * 64]          # 옛 판 — 모르는 선택 (getopts 거부)
    args += [C] if cases is None else list(cases)
    S = os.path.join(L, '%s.%s' % (C, suf))
    with open(cap) as f:
        n0 = len(f.read().splitlines())
    reps0 = snap_reports(L)
    s_before = tree_sha(S)
    p = subprocess.run(args, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=600)
    s_after = tree_sha(S)
    with open(cap) as f:
        calls = f.read().splitlines()[n0:]
    reps1 = snap_reports(L)
    new = sorted((p2 for p2 in reps1 if reps0.get(p2) != reps1[p2]), key=lambda p2: reps1[p2][0])
    rep = open(new[-1], encoding='utf-8').read() if new else ''
    W = os.path.join(L, C)
    w_decks, att = {}, {}
    for q in glob.glob(os.path.join(W, 'input*.liggghts')):
        with open(q, 'rb') as f:
            w_decks[os.path.basename(q)] = f.read()
    for q in glob.glob(os.path.join(W, 'attempt_*', '**'), recursive=True):
        if os.path.isfile(q):
            with open(q, 'rb') as f:
                att[os.path.relpath(q, W)] = f.read().decode('utf-8', 'replace')
    plan = os.path.join(W, 'plan_%s.txt' % SFX)
    plan = open(plan, encoding='utf-8', errors='replace').read() if os.path.isfile(plan) else ''
    out = p.stdout.decode('utf-8', 'replace')
    return dict(trial=any(c.startswith('trial ') for c in calls), main=any(c.startswith('main ') for c in calls),
                ntrial=sum(c.startswith('trial ') for c in calls), nmain=sum(c.startswith('main ') for c in calls),
                calls=calls, rep=rep, out=out, rc=p.returncode, s_before=s_before, s_after=s_after, w_decks=w_decks,
                att=att, plan=plan, out_n=norm(out, tmp), rep_n=norm(rep, tmp),
                w_files=tree_sha(W) if os.path.isdir(W) else {}, w_cmp=tree_cmp(W, tmp) if os.path.isdir(W) else {},
                s_same=s_before == s_after, w_exists=os.path.isdir(W))


def run_case1(script, res_kind, trial, sacct='COMPLETED|0:0', sacct_rc=0, squeue='', squeue_rc=0, extra=(),
              fake=FAKE_DEM_RESTART, main_bytes=None, more_decks=(), main_link=False,
              res_text=None, trial_text=None, mode='settling', ckpt=CKPT, orig_log=ORIG_LOG, **more):
    # 10-28: res_text · trial_text = 재개 덱 · 시험 로그 내용을 바로 · mode · ckpt · orig_log = 가짜 dem_restart.py 계획 줄 · 체크포인트 · 원 로그
    # 10-28 밤: more = invoke 의 squeue2 · squeue_rc2 · approve · env_more · cases (새 시험만 씀)
    ctx = make_root(fake=fake, main_bytes=main_bytes, more_decks=more_decks, main_link=main_link, ckpt=ckpt, orig_log=orig_log)
    try:
        if trial_text is None and trial:
            trial_text = trial_log(trial)
        return invoke(ctx, script, res_variant(res_kind) if res_text is None else res_text, trial_text, sacct=sacct,
                      sacct_rc=sacct_rc, squeue=squeue, squeue_rc=squeue_rc, extra=extra, mode=mode, ckpt=ckpt, **more)
    finally:
        shutil.rmtree(ctx['tmp'], ignore_errors=True)


def deckcheck_only(script, main, res, ckpt, s0, workdir_files=()):
    r = deckcheck_only1(script, main, res, ckpt, s0, workdir_files)
    if CMP['old'] is not None:
        o = deckcheck_only1(CMP['old'], main, res, ckpt, s0, workdir_files)
        CMP['rows'].append((CMP['grp'], '-C %s %s %s' % (os.path.basename(res), ckpt, s0),
                            [x for x, y, z in (('rc', r[0], o[0]), ('out_n', r[2], o[2])) if y != z], o[0] == 0, r[0] == 0))
    return r[:2]


def deckcheck_only1(script, main, res, ckpt, s0, workdir_files=()):
    # (종료 코드 · stdout 그대로 (판정용) · 임시 경로 · 새 줄 뺀 것 (--compare-old 대조용))
    tmp = tempfile.mkdtemp(prefix='rckc_')
    try:
        for n in workdir_files:
            open(os.path.join(tmp, n), 'w').close()
        p = subprocess.run(['bash', script, '-C', main, res, ckpt, str(s0), tmp],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
        out = p.stdout.decode('utf-8', 'replace')
        return p.returncode, out.replace(tmp, '<임시>'), norm(out, tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def write_tmp(d, name, text):
    p = os.path.join(d, name)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(text)
    return p


def main():
    script = SCRIPT
    if '--script' in sys.argv:
        script = sys.argv[sys.argv.index('--script') + 1]
    if '--compare-old' in sys.argv:
        CMP['old'] = os.path.abspath(sys.argv[sys.argv.index('--compare-old') + 1])
    ok = fail = 0

    def grp(g):
        CMP['grp'] = g

    def chk(name, cond, detail=''):
        nonlocal ok, fail
        if cond:
            ok += 1
            print('PASS', name)
        else:
            fail += 1
            print('FAIL', name, '·', detail[-1500:].replace('\n', ' | '))

    # ── Codex §3 반례 다섯 (step 20001 재개로 옮김) ──
    grp('K')
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
    grp('S')
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
    grp('D')
    for kind, label in (('reinsert', '재삽입 fix'), ('damp_wrong', '정착 감쇠가 다른 단계 값 (0.5)'),
                        ('damp_missing', '정착 감쇠 fix 빠짐'), ('steps_wrong', '남은 정착 step 이 200000 (끝 220001)'),
                        ('extra_fix', '본 덱에 없는 fix'), ('var_changed', '판 속도 변수 0.02'),
                        ('tail_changed', '이완 run 100000 → 50000'), ('mesh_scale', '판 메시 줄이 파일 말고도 다름'),
                        ('compute_missing', '뒤에서 쓰는 compute zmax 정의 빠짐')):
        r = run_case(script, kind, 'ok')
        chk('D %s → 시험 · 본 제출 안 함' % label, not r['trial'] and not r['main'], r['out'])
    # ── 큐 이름 · -T ──
    grp('Q')
    r = run_case(script, 'good', 'ok', squeue='%s_ins' % C)
    chk('Q1 삽입 잡 (%s_ins) 이 큐에 있음 → 건너뜀' % C, not r['trial'] and not r['main'], r['out'])
    r = run_case(script, 'good', 'ok', squeue='%s_r56' % C)
    chk('Q2 같은 케이스 재개 잡 (%s_r56) 이 큐에 있음 → 건너뜀' % C, not r['trial'] and not r['main'], r['out'])
    r = run_case(script, 'good', 'ok', squeue='%sx\n%s_s2' % (C, C))
    chk('Q3 이름이 겹치기만 하는 다른 잡 → 막지 않음', r['trial'] and r['main'], r['rep'] + r['out'])
    r = run_case(script, 'good', 'ok', squeue_rc=1)
    chk('Q4 squeue 조회 실패 → 건너뜀', not r['trial'] and not r['main'], r['out'])
    grp('T')
    r = run_case(script, 'good', 'ok', extra=('-T',))
    chk('T1 -T 시험만 → 시험은 내고 본 제출 안 함', r['trial'] and not r['main'] and '시험만' in r['rep'], r['rep'] + r['out'])
    # ── -C: 실제 09-27 재개 덱 쌍 (dem_restart.py 산출 · 압축 단계) ──
    grp('C')
    m075 = os.path.join(R075, 'input_pse_r075_a.liggghts')
    r075 = os.path.join(R075, 'input_pse_r075_a_r30.liggghts')
    rc, out = deckcheck_only(script, m075, r075, 'restart_pse_r075_a/restart_compress_1500000.bin', 1500000,
                             ('plate_pse_r075_a_r30.stl',))
    # 10-28 밤 바꿈 (KG50R-01 · 1저자 Q3 (가)): 예전 기대 = 통과 — 그 쌍의 체크포인트 1,500,000 은 판정 1,500,002 의 2 step 앞 (위상 4,998) 인데
    #   재개 덱은 run 5000 을 새로 돌아 다음 판정이 1,505,000 (Codex §2 · 우리 r075_retro.md) → 압축 체크포인트 재개 = 거부가 기대값
    chk('C1 실제 09-27 쌍 (압축 재개) → 거부 (압축 체크포인트 재개 = 지원 안 함 · 그 밖 문제 0 · 10-28 밤 Q3 로 기대 바꿈)',
        rc != 0 and Q3MSG in out and '(문제 1)' in out, out)
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
    grp('N')
    with open(MAIN, 'rb') as f:
        mb = f.read()
    with open(MAIN_INS, 'rb') as f:
        ib = f.read()
    nm, ni = 'input_%s.liggghts' % C, 'input_%s_insert.liggghts' % C
    ins = ((ni, ib),)
    rej = "다른 케이스명 혼입: ['real_4']"
    r = run_case(script, 'good', 'ok', fake=FAKE_DEM_RESTART_STRICT, more_decks=ins)
    # 10-28 밤 바꿈 (Q9 · Codex Q9): 예전 기대 = 보고에 케이스 절 없음 (거부 이유는 nohup 화면에만) → 시험 전 거부도 케이스 절 (단계 · 이유 · 시도)
    chk('N1 덱 머리 주석에 템플릿 이름 real_4 · -c 없음 → 재개 덱 못 만듦 · 시험 · 본 제출 안 함 · 보고에 시험 전 거부 케이스 절 (단계 · 시도 · 10-28 밤 Q9 로 기대 바꿈)',
        rej in r['plan'] and '재개 덱 못 만듦' in r['out'] and not r['trial'] and not r['main']
        and ('## %s — 시험 전 거부' % C) in r['rep'] and '단계: 재개 덱 만들기 (dem_restart.py)' in r['rep']
        and re.search(r'시도 attempt_r56_[0-9_]+', r['rep']), r['plan'] + r['out'] + r['rep'])
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
    # ── F: 재개 덱 첫 긴 run 의 1 step 짧음 고침 (10-27 ibb kg50_d2_b50 r4 · 1저자 Q1 (가) "권고대로 해줘") ──
    #    dem_restart.py 가 run 179999 (끝 200000) 를 내는데 본 덱 정착 run 끝은 200001 → 도구가 그 한 줄만 180000 으로 고치고
    #    정적 대조를 처음부터 다시 통과할 때만 시험을 낸다.  그 밖의 차이 · 다른 문제가 같이 있으면 고치지 않는다 (정적 대조가 거부).
    grp('F')
    nr = 'input_%s_%s.liggghts' % (C, SFX)
    r = run_case(script, 'steps_ibb', 'ok', extra=('-T',))
    wd = r['w_decks'].get(nr, b'')
    chk('F1 dem_restart.py 의 run 179999 (끝 200000 ↔ 본 덱 200001) → 재개 덱 그 줄만 run 180000 · 정적 대조 통과 · 시험 냄 (-T · 본 제출 안 함)',
        r['trial'] and not r['main'] and b'\nrun 180000\n' in wd and b'179999' not in wd
        and '남은 step 같음: 끝 200001' in r['out'], r['out'])
    g = with_tmpl(res_variant('good')).encode()
    chk('F1b 고친 재개 덱 = 정상 재개 덱 (run 180000) 과 바이트 같음 — 다른 줄은 손대지 않음',
        wd == g, r['out'])
    chk('F1c 기록 = stdout · 보고 둘 다 고친 줄 (옛 run 179999 → 새 run 180000 · 본 덱 그 run 끝 200001 · 체크포인트 step 20001)',
        all(any(('run 179999' in l and 'run 180000' in l and '200001' in l and '20001' in l) for l in t.splitlines())
            for t in (r['out'], r['rep'])), r['out'] + r['rep'])
    chk('F1d 멈춘 폴더 (원본) 의 모든 파일 sha256 그대로', r['s_before'] == r['s_after'], r['out'])
    r = run_case(script, 'steps_ibb', 'ok')
    chk('F2 같은 꼴 · -T 없음 · 시험 정상 → 본 제출', r['trial'] and r['main'], r['out'] + r['rep'])
    r = run_case(script, 'steps_ibb_comment', 'ok', extra=('-T',))
    wd = r['w_decks'].get(nr, b'')
    chk('F3 앞 공백 · 뒤 주석이 있는 run 줄 → 숫자만 바뀜 (공백 · 주석 그대로) · 시험 냄',
        r['trial'] and b'\n  run   180000   # settling \xec\x9e\x94\xec\x97\xac\n' in wd and b'179999' not in wd, r['out'])
    for kind, label in (('steps_minus2', '2 step 짧음 (run 179998)'), ('steps_plus1', '1 step 김 (run 180001)'),
                        ('steps_ibb_extra', '1 step 짧음 + 본 덱에 없는 fix'), ('steps_ibb_amp', '1 step 짧음 · run 줄이 & 로 이어짐'),
                        ('steps_ibb_upto', 'run 200000 upto (끝 200000)'), ('steps_wrong', '남은 정착 step 200000 (끝 220001)')):
        r = run_case(script, kind, 'ok', extra=('-T',))
        orig = with_tmpl(res_variant(kind)).encode()
        chk('F4 %s → 고치지 않음 (재개 덱 바이트 그대로) · 정적 대조 실패 · 시험 · 본 제출 안 함' % label,
            not r['trial'] and not r['main'] and r['w_decks'].get(nr) == orig and '재개 덱 정적 대조: 실패' in r['out'], r['out'])
    r = run_case(script, 'good', 'ok', extra=('-T',))
    chk('F5 정상 재개 덱 (run 180000) → 고칠 것 없음 · 재개 덱 바이트 그대로 · 시험 냄',
        r['trial'] and r['w_decks'].get(nr) == with_tmpl(res_variant('good')).encode() and '고칠 것 없음' in r['out'], r['out'])
    tmp = tempfile.mkdtemp(prefix='rckf_')
    try:
        bad = os.path.join(tmp, 'res_ibb.liggghts')
        with open(bad, 'w', encoding='utf-8') as f:
            f.write(res_variant('steps_ibb'))
        rc, out = deckcheck_only(script, MAIN, bad, CKPT, 20001)
        chk('F6 -C (정적 대조만) 는 고치지 않는다 — run 179999 → 실패 · 남은 step 다름', rc != 0 and '남은 step 다름' in out, out)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    # ── A: after_settling 재개 (10-28 KG50-18 · 요청서 §4-1) — 시험 = 판 높이 run 1 + 시험 run 2000 → 끝 = S0 200001 + 2001 ──
    #    고치기 전 G0 기대 끝 = S0 + 마지막 run = 202001 → 정상 시험 (끝 202002) 도 G0 실패 · 1 step 짧게 멈춘 시험 (끝 202001) 은 통과
    grp('A')
    asx = dict(mode='after_settling', ckpt=CKPT_AS, orig_log=AS_LOG)
    r = run_case(script, None, None, res_text=res_after('good'), trial_text=as_trial(), extra=('-T',), **asx)
    chk('A1 after_settling 정상 재개 · -T → 정적 대조 통과 · 시험 냄 · G0 통과 (마지막 step 202002 = 기대 202002) · G1–G3 통과 · 본 제출 안 함',
        r['trial'] and not r['main'] and '시험만' in r['rep'] and 'G0 시험 정상 종료: 통과' in r['rep']
        and '마지막 step 202002 (기대 202002)' in r['rep'] and 'G2 체크포인트 상태 덤프 대조: 통과 —판 높이 같음' in r['rep']
        and re.search(r'G1 재개 첫 thermo \(step 200001,[^\n]*: 통과', r['rep']) and 'G3' in r['rep'] and '5 % 안' in r['rep'],
        r['rep'] + r['out'])
    chk('A1b 기대 끝 = S0 + 시험 덱 read_restart 뒤 run 합 — stdout 한 줄 + ▶ 줄 · 보고 한 줄 (run 이 둘 이상일 때만)',
        '시험 기대 끝 step = S0 + 시험 덱 read_restart 뒤 run 합 2001 ([run 1] [run 2000] · 10-28 KG50-18)' in r['out']
        and '▶ 시험 job 7001 (run 2000 · 기대 끝 step 202002)' in r['out']
        and '- 시험 기대 끝 step (10-28 · KG50-18): S0 200001 + 시험 덱 read_restart 뒤 run 합 2001 ([run 1] [run 2000]) = 202002'
        in r['rep'], r['out'] + r['rep'])
    chk('A1c 정적 대조 = write_restart 체크포인트의 첫 긴 run 대조 (본 덱 그 뒤 [run 1] [run 200000] = 재개 덱) 통과',
        '첫 긴 run 같음 (write_restart 체크포인트 · 10-28 KG50-19): 본 덱 그 뒤 [run 1] [run 200000] = 재개 덱 read_restart 뒤'
        in r['out'] and '재개 덱 정적 대조: 통과' in r['out'], r['out'])
    r = run_case(script, None, None, res_text=res_after('good'), trial_text=as_trial(), **asx)
    chk('A2 같은 장면 · -T 없음 → 본 제출', r['trial'] and r['main'], r['rep'] + r['out'])
    r = run_case(script, None, None, res_text=res_after('good'), trial_text=as_trial(202001), **asx)
    chk('A3 시험 로그가 1 step 짧게 끝남 (202001 · COMPLETED · Loop time 있음) → G0 실패 · 본 제출 안 함',
        r['trial'] and not r['main'] and 'G0 시험 정상 종료: 실패' in r['rep'] and '마지막 step 202001 (기대 202002)' in r['rep'],
        r['rep'] + r['out'])
    r = run_case(script, None, None, res_text=res_after('stab199999'), trial_text=as_trial(), extra=('-T',), **asx)
    chk('A4 재개 덱 안정화 run 199999 → 정적 대조 실패 (첫 긴 run 다름) · 시험 · 본 제출 안 함',
        not r['trial'] and not r['main'] and '첫 긴 run 다름 (write_restart 체크포인트' in r['out']
        and '[run 199999]' in r['out'], r['out'])
    # ── P: 시험 덱 run 합을 못 정하는 꼴 = 시험 전 거부 (10-28 KG50-18 · fail-closed) · settling 장면 · -T ──
    grp('P')
    for kind, frag, label in (('p_if_run', 'print · quit 말고 다른 명령이 든 if: [if "1 > 0" then "run 100"]', 'run 이 든 if'),
                              ('p_reset', 'step 을 바꾸는 명령: [reset_timestep 0]', 'reset_timestep'),
                              ('p_jump', '흐름 명령 (jump · next · include): [jump SELF skip1]', 'jump · label'),
                              ('p_include', '흐름 명령 (jump · next · include): [include extra.in]', 'include'),
                              ('p_upto', 'run 꼬리 upto: [run 1 upto]', 'run 1 upto'),
                              ('p_var', 'run 수가 숫자가 아님: [run ${n_settle}]', 'run 수가 변수'),
                              ('p_every', 'run 꼬리 every: [run 1 every 1 NULL]', 'run every'),
                              ('p_if_else', 'print · quit 말고 다른 명령이 든 if: [if "1 > 0" then "print a" else "run 100"]',
                               'else 에 run 이 든 if'),
                              ('p_varcmd', '명령 이름에 변수: [${cmdx} 100]', '이름이 변수인 명령'),
                              ('p_rr2', '시험 덱에 read_restart 가 2 개 (1 개여야)', '두 번째 read_restart')):
        r = run_case(script, kind, 'ok', extra=('-T',))
        chk('P %s 가 첫 긴 run 앞에 → 시험 기대 끝 step 을 못 정함 · 시험 · 본 제출 안 함' % label,
            not r['trial'] and not r['main'] and ('✗ 시험 기대 끝 step 을 못 정함 (10-28 KG50-18) — ' + frag) in r['out'], r['out'])
    r = run_case(script, 'p_run0', 'ok', extra=('-T',))
    # 10-28 밤 바꿈 (KG50R-03 · 1저자 Q2 (가)): 예전 기대 = 시험 냄 (합 2000) — 본 덱에 없는 run (run 0 도 setup 을 다시 돈다) 이 준비 구간에 있으면
    #   전체 프로그램 대조가 거부 (준비 구간 = 상태 명령 · 본 덱 체크포인트 앞에 글자 그대로 있는 print · if · group · shell mkdir 만)
    chk('P8 첫 긴 run 앞 run 0 pre no post no (본 덱에 없는 run) → 정적 대조 거부 (준비 구간 명령 허용 안 됨) · 시험 안 함 (10-28 밤 Q2 로 기대 바꿈)',
        not r['trial'] and not r['main'] and '재개 덱 준비 구간 명령 허용 안 됨' in r['out'] and '[run 0 pre no post no]' in r['out'],
        r['out'] + r['rep'])
    r = run_case(script, 'p_run1', 'ok', extra=('-T',))
    chk('P9 settling 재개 덱 첫 긴 run 앞에 run 1 (시험 합 2001 이면 G0 이 1 step 어긋남을 못 막는다) → 정적 대조 실패 · 시험 안 함',
        not r['trial'] and not r['main'] and '재개 덱 첫 긴 run 앞에 run 이 있음' in r['out'] and '[run 1]' in r['out'], r['out'])
    r = run_case(script, 'p_ifprint', 'ok', extra=('-T',))
    chk('P10 print · quit 만 든 if (삽입 자기검사 꼴 · & 이어 붙임) → 막지 않음 · 기대 22001 · G0 통과 · 시험 냄',
        r['trial'] and 'G0 시험 정상 종료: 통과' in r['rep'] and '마지막 step 22001 (기대 22001)' in r['rep']
        and '시험 기대 끝 step 을 못 정함' not in r['out'], r['out'] + r['rep'])
    # ── W: write_restart · 반복 안 restart 체크포인트 재개 덱의 첫 긴 run 대조 (10-28 KG50-19 · 요청서 §4-2 · -C) ──
    grp('W')
    rc, out = deckcheck_only(script, m075, r075, 'restart_pse_r075_a/restart_compress_1500000.bin', 1500000,
                             ('plate_pse_r075_a_r30.stl',))
    # 10-28 밤 바꿈 (KG50R-01 · Q3 (가)): 예전 기대 = 통과 · '루프 몸 run 같음' — 루프 몸 글자만 같고 위상 (판정까지 남은 2 step) 을 안 봤다
    chk('W0 실제 09-27 r075 압축 쌍 → 거부 (압축 체크포인트 재개 = 지원 안 함 · 10-28 밤 Q3 로 기대 바꿈)',
        rc != 0 and Q3MSG in out and '루프 몸 run 같음' not in out, out)
    tmp = tempfile.mkdtemp(prefix='rckw_')
    try:
        ck50 = 'restart_%s/restart_after_settling.bin' % C50
        rc, out = deckcheck_only(script, MAIN50, write_tmp(tmp, 'w1.liggghts', res_after('good', MAIN50, C50, tmpl=True)), ck50, 200001)
        chk('W1 v3 50×50 after_settling 재개 덱 (템플릿 줄 포함) → 통과 · 첫 긴 run 같음',
            rc == 0 and '첫 긴 run 같음 (write_restart 체크포인트' in out, out)
        for n in ('199999', '100000', '400000'):
            rc, out = deckcheck_only(script, MAIN50, write_tmp(tmp, 'w%s.liggghts' % n,
                                                                res_after('stab' + n, MAIN50, C50, tmpl=True)), ck50, 200001)
            chk('W2 같은 덱 · 안정화 run 200000 → %s → 실패 (첫 긴 run 다름)' % n,
                rc != 0 and '첫 긴 run 다름 (write_restart 체크포인트' in out and '[run %s]' % n in out, out)
        rc, out = deckcheck_only(script, MAIN50, write_tmp(tmp, 'w5.liggghts', res_after('damp_settle', MAIN50, C50, tmpl=True)),
                                 ck50, 200001)
        chk('W5 같은 덱 · 안정화 감쇠를 정착 값 그대로 → 실패 (재개 지점 상태 · 고치기 전에도 잡던 꼴)', rc != 0 and 'damp' in out, out)
        with open(r075, encoding='utf-8') as f:
            t075 = f.read()
        with open(m075, encoding='utf-8') as f:
            tm075 = f.read()
        rc, out = deckcheck_only(script, m075, write_tmp(tmp, 'w6.liggghts', mutate(t075, '    run 5000\n', '    run 4000\n')),
                                 'restart_pse_r075_a/restart_compress_1500000.bin', 1500000, ('plate_pse_r075_a_r30.stl',))
        # 10-28 밤 바꿈 (W6 · W7 · W10 · W12 — 압축 루프 체크포인트 = Q3 (가) 거부가 먼저 · 예전 기대 = '루프 몸 run 다름' · '정할 수 없음')
        chk('W6 r075 쌍 · 루프 몸 run 5000 → 4000 → 실패 (압축 체크포인트 거부 + 첫 긴 run 다름 · 10-28 밤 Q3 로 기대 바꿈)',
            rc != 0 and Q3MSG in out and '[run 4000]' in out, out)
        rc, out = deckcheck_only(script, m075, write_tmp(tmp, 'w7.liggghts', mutate(t075, 'label loop_press\n', '')),
                                 'restart_pse_r075_a/restart_compress_1500000.bin', 1500000, ('plate_pse_r075_a_r30.stl',))
        chk('W7 r075 쌍 · 재개 덱에서 label loop_press 빠짐 (본 런이 jump 에서 죽는 꼴) → 실패 (압축 체크포인트 거부 + jump 목적지 없음 · 10-28 밤 Q3 로 기대 바꿈)',
            rc != 0 and Q3MSG in out and 'jump 목적지 label loop_press 가 재개 덱에 없음' in out, out)
        with open(MAIN50, encoding='utf-8') as f:
            t50 = f.read()
        m8 = write_tmp(tmp, 'm8.liggghts', mutate(t50, 'run 1\nvariable z_max equal c_zmax\n',
                                                  'run ${n1}\nvariable z_max equal c_zmax\n'))
        rc, out = deckcheck_only(script, m8, write_tmp(tmp, 'w8.liggghts', res_after('good', m8, C50, tmpl=True)), ck50, 200001)
        chk('W8 본 덱 write_restart 뒤 run 수가 변수 (run ${n1}) · 재개 덱 같음 → 실패 (첫 긴 run 길이를 정할 수 없음)',
            rc != 0 and '첫 긴 run 길이를 정할 수 없음' in out, out)
        with open(MAIN, encoding='utf-8') as f:
            tm = f.read()
        m9 = write_tmp(tmp, 'm9.liggghts', mutate(tm, 'compute zmax all reduce max z\n', 'label dummy0\ncompute zmax all reduce max z\n'))
        rc, out = deckcheck_only(script, m9, write_tmp(tmp, 'w9.liggghts', res_variant('good')), CKPT, 20001)
        chk('W9 settling 체크포인트 앞에 label (남은 step 을 못 셈) · 체크포인트 뒤 루프 머리 없음 → 실패 (예전 = 확인 생략 · 통과)',
            rc != 0 and '남은 step 을 정할 수 없음' in out, out)
        ifj = '    if "${current_press} < ${target_press}" then "jump SELF loop_press"\n'
        m10 = write_tmp(tmp, 'm10.liggghts', mutate(tm075, ifj, ''))
        rc, out = deckcheck_only(script, m10, write_tmp(tmp, 'w10.liggghts', mutate(t075, ifj, '')),
                                 'restart_pse_r075_a/restart_compress_1500000.bin', 1500000, ('plate_pse_r075_a_r30.stl',))
        chk('W10 r075 쌍 · 본 덱 · 재개 덱 둘 다 루프 jump 빠짐 (label 뒤 run 이 루프가 아님) → 실패 (압축 체크포인트 거부 · 10-28 밤 Q3 로 기대 바꿈)',
            rc != 0 and Q3MSG in out, out)
        rst = 'restart 50000 restart_%s/restart_settling_*.bin\n' % C
        m11 = write_tmp(tmp, 'm11.liggghts', mutate(tm, rst, rst + 'include extra.in\n'))
        rc, out = deckcheck_only(script, m11, write_tmp(tmp, 'w11.liggghts', res_variant('good')), CKPT, 20001)
        chk('W11 settling 체크포인트 뒤 · 그 run 앞에 include (남은 step 을 못 셈 · 예전 = label · jump 만 봄) → 실패 (남은 step 을 정할 수 없음)',
            rc != 0 and '남은 step 을 정할 수 없음' in out, out)
        rcp = 'restart 50000 restart_pse_r075_a/restart_compress_*.bin\n'
        m12 = write_tmp(tmp, 'm12.liggghts', mutate(tm075, rcp, rcp + 'run ${nwarm}\n'))
        rc, out = deckcheck_only(script, m12, r075, 'restart_pse_r075_a/restart_compress_1500000.bin', 1500000,
                                 ('plate_pse_r075_a_r30.stl',))
        chk('W12 r075 본 덱 · 체크포인트 줄과 루프 머리 사이에 변수 run (체크포인트가 그 run 에서 나왔을 수 있음) → 실패 (압축 체크포인트 거부 · 10-28 밤 Q3 로 기대 바꿈)',
            rc != 0 and Q3MSG in out, out)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ═══ 10-28 밤 — Codex 재검토 KG50R-01–05 · 07 · 수정 계획 Q1–Q5 · Q9 (docs/50kg/kg50_resume_recheck_fix_plan_20261028.md) ═══
    good = res_variant('good')
    ok_log = trial_log('ok')
    # ── R: 이번 호출이 낸 시험만 본 제출 (KG50R-04 · Q1) ──
    grp('R')

    def codex_probe(scenario):
        # Codex independent/scheduler/probe_stale_trial.py 두 장면 그대로 — 작업 폴더에 옛 성공 시험 (job 7001 · mode · 원 로그 · 시험 로그 ·
        #   옛 러너 · 옛 기록) 이 남아 있고 이번 호출의 첫 squeue 가 그 케이스 잡을 돌려주거나 (busy_queue) 실패 (queue_query_failure).
        #   그 탐침은 ZIP 의 repo/ 옆에서만 돈다 → 같은 파일 · 같은 가짜 scheduler 를 여기서 만든다 (승인 인자는 새 판에 실제 값)
        ctx = make_root()
        try:
            L, W = ctx['L'], os.path.join(ctx['L'], C)
            os.makedirs(os.path.join(W, 'post_' + C))
            os.makedirs(os.path.join(L, 'logs'))
            log7 = os.path.join(L, 'logs', 'output_%s_%st_7001.out' % (C, SFX))
            files = {os.path.join(W, 'log.liggghts.' + SUF): ORIG_LOG, os.path.join(W, 'job_%st.txt' % SFX): '7001\n',
                     os.path.join(W, 'mode_%s.txt' % SFX): 'settling 20001 %s 22001\n' % CKPT, log7: ok_log,
                     os.path.join(W, 'run_%s_%s.sh' % (C, SFX)): '#!/bin/sh\n# old prior invocation runner; never execute\n'}
            for n in ('tp', 'fixrun', 'deckcheck'):
                files[os.path.join(W, '%s_%s.txt' % (n, SFX))] = 'OLD PREEXISTING ARTIFACT\n'
            for p, body in files.items():
                with open(p, 'w') as f:
                    f.write(body)
            w0, l0 = tree_sha(W), sha256f(log7)
            r = invoke(ctx, script, good, ok_log, **(dict(squeue=C) if scenario == 'busy_queue' else dict(squeue_rc=1)))
            return r, w0 == tree_sha(W) and l0 == sha256f(log7)
        finally:
            shutil.rmtree(ctx['tmp'], ignore_errors=True)

    for sc, stage in (('busy_queue', '단계: 큐 ·'), ('queue_query_failure', '단계: 큐 조회')):
        r, kept = codex_probe(sc)
        chk('R1 Codex probe_stale_trial %s — 옛 성공 시험 (job 7001) 이 남은 작업 폴더 · 이번 호출 큐 차단 → sbatch 0 회 (시험 · 본 제출 없음) · '
            '작업 폴더 · 옛 시험 로그 그대로 · 보고에 시험 전 거부 절 (KG50R-04)' % sc,
            r['calls'] == [] and kept and ('## %s — 시험 전 거부' % C) in r['rep'] and stage in r['rep'], r['out'] + r['rep'])

    def twice(first, second, family):
        # 같은 루트에서 두 번 호출 — family A = 작업 폴더를 그대로 둠 · B = 작업 폴더를 멈춘 폴더 <C>.stop2 로 옮김 (그 본 런이 멈춘 꼴 ·
        #   옛 job · mode 파일이 다음 재개의 작업 폴더로 같이 복사된다) · 둘째 호출 전 logs/ 의 옛 시험 로그 sha256 을 적어 둔다
        ctx = make_root()
        try:
            L = ctx['L']
            W = os.path.join(L, C)
            r1 = invoke(ctx, script, good, ok_log, **first)
            suf2 = SUF
            if family == 'B':
                os.rename(W, os.path.join(L, '%s.stop2' % C))
                with open(os.path.join(L, '%s.stop2' % C, 'log.liggghts'), 'w') as f:
                    f.write(ORIG_LOG)
                suf2 = 'stop2'
            keep = dict((p, sha256f(p)) for p in glob.glob(os.path.join(L, 'logs', '*')))
            w0 = tree_sha(W) if os.path.isdir(W) else None
            sec = dict(second)
            r2 = invoke(ctx, script, sec.pop('res_text', good), sec.pop('trial_text', ok_log), suf=suf2, **sec)
            prev = [d for d in os.listdir(L) if d.startswith(C + '.prev_')]
            pj = [open(os.path.join(L, d, 'job_%st.txt' % SFX)).read() for d in prev
                  if os.path.isfile(os.path.join(L, d, 'job_%st.txt' % SFX))]
            info = dict(r1=r1, logs_kept=all(os.path.isfile(p) and sha256f(p) == h for p, h in keep.items()) and len(keep) > 0,
                        w_same=(w0 == tree_sha(W)) if w0 is not None else None, prev_jobs=pj)
            return r2, info
        finally:
            shutil.rmtree(ctx['tmp'], ignore_errors=True)

    T1, FULL = dict(extra=('-T',)), dict()
    for tag, fam, first, second, want_t, want_m, frag in (
            ('R2 A · 큐에 그 케이스 잡', 'A', T1, dict(squeue=C), 0, 0, '단계: 큐 ·'),
            ('R3 A · 첫 squeue 조회 실패', 'A', T1, dict(squeue_rc=1), 0, 0, '단계: 큐 조회'),
            ('R4 B · 정적 거부 (정착 감쇠 0.5)', 'B', FULL, dict(res_text=res_variant('damp_wrong')), 0, 0, '단계: 정적 대조 · 시험 덱'),
            ('R5 B · 시험 sbatch 빈 출력', 'B', FULL, dict(env_more={'FAKE_SBATCH_TRIAL_EMPTY': '1'}), 1, 0, '단계: 시험 제출'),
            ('R6 B · dem_restart.py 계획 없음', 'B', FULL, dict(env_more={'FAKE_DEM_FAIL': '1'}), 0, 0, '단계: 재개 덱 만들기'),
            ('R7 A · 본 제출 직전 큐에 그 케이스 잡이 나타남', 'A', T1, dict(squeue2='5555 %s_%s' % (C, SFX)), 1, 0, '본 제출 직전 큐에 그 케이스 잡'),
            ('R8 A · 본 제출 직전 squeue 조회 실패', 'A', T1, dict(squeue2='', squeue_rc2=1), 1, 0, '본 제출 직전 squeue 조회 실패')):
        r, info = twice(first, second, fam)
        chk('%s → 이번 호출 새 본 제출 0 회 (시험 sbatch %d 회 · 옛 시험 job 7001 로 승격 안 함 · logs/ 옛 시험 로그 그대로 · KG50R-04)' % (tag, want_t),
            r['ntrial'] == want_t and r['nmain'] == want_m and info['logs_kept'] and frag in r['rep']
            and (fam == 'B' or r['ntrial'] > 0 or info['w_same']), r['out'] + r['rep'])
    r, info = twice(T1, {}, 'A')
    chk('R9 A · 정상 새 시도 → 시험 1 · 본 1 (새 시험 job 7002 로 승격) · 옛 작업 폴더는 <C>.prev_<시각> 로 (옛 job 7001 그대로)',
        r['ntrial'] == 1 and r['nmain'] == 1 and '- 시험: job 7002' in r['rep'] and info['prev_jobs'] == ['7001\n'] and info['logs_kept'],
        r['out'] + r['rep'])
    r, info = twice(FULL, {}, 'B')
    om = [k for k in r['att'] if '/old_markers/' in k]
    chk('R10 B · 정상 새 시도 → 시험 1 · 본 1 · 멈춘 폴더에서 같이 온 옛 job · mode 파일은 시도 폴더 old_markers/ 로 (내용 그대로 · 승격에 안 씀)',
        r['ntrial'] == 1 and r['nmain'] == 1 and r['s_same'] and info['logs_kept']
        and any(k.endswith('/old_markers/job_%st.txt' % SFX) and r['att'][k] == '7001\n' for k in om)
        and any(k.endswith('/old_markers/mode_%s.txt' % SFX) for k in om), r['out'] + r['rep'] + ' '.join(sorted(r['att'])))
    r = run_case(script, 'good', 'ok', squeue2='7001 %s_%st' % (C, SFX))
    chk('R11 본 제출 직전 큐에 이번 시험 job (7001) 만 → 빼고 봄 → 본 제출', r['trial'] and r['main'], r['out'] + r['rep'])
    r = run_case(script, 'good', 'ok', squeue2='7777 %s_%st' % (C, SFX))
    chk('R12 본 제출 직전 큐에 같은 이름 다른 시험 job (7777) → 본 제출 안 함 (KG50R-04)',
        r['trial'] and not r['main'] and '본 제출 직전 큐에 그 케이스 잡' in r['rep'], r['out'] + r['rep'])
    r = run_case(script, 'good', 'ok', cases=[C, C])
    chk('R13 같은 케이스를 목록에 두 번 → 시험 1 · 본 1 (두 번째는 시험 전 거부 · 예전 = 시험 2 · 본 2)',
        r['ntrial'] == 1 and r['nmain'] == 1 and '같은 케이스가 목록에 두 번' in r['out'], r['out'] + r['rep'])

    # ── G: 전체 프로그램 대조 (KG50R-02 · 03 · 05 · Q2 (가)) — Codex 덱 고정물 그대로 (-C) ──
    grp('G')
    tmp = tempfile.mkdtemp(prefix='rckg_')
    try:
        CKS, CKA = (CKPT, 20001), (CKPT_AS, 200001)
        for path, ck, want, frag in (
                (os.path.join(CX_DECK, 'baseline.liggghts'), CKS, 0, '통과'),
                (os.path.join(CX_SCHED, 'plain.liggghts'), CKS, 0, '통과'),
                (os.path.join(CX_DECK, 'after_settling_baseline.liggghts'), CKA, 0, '통과'),
                (os.path.join(CX_DECK, 'suffix_velocity.liggghts'), CKS, 1, '첫 긴 run 뒤 명령 다름'),
                (os.path.join(CX_DECK, 'suffix_density.liggghts'), CKS, 1, '첫 긴 run 뒤 명령 다름'),
                (os.path.join(CX_DECK, 'suffix_delete.liggghts'), CKS, 1, '첫 긴 run 뒤 명령 다름'),
                (os.path.join(CX_DECK, 'suffix_include.liggghts'), CKS, 1, '다룰 수 없는 구문 (재개 덱 · include'),
                (os.path.join(CX_DECK, 'velocity_after_first_long.liggghts'), CKS, 1, '첫 긴 run 뒤 명령 다름'),
                (os.path.join(CX_DECK, 'density_after_first_long.liggghts'), CKS, 1, '첫 긴 run 뒤 명령 다름'),
                (os.path.join(CX_DECK, 'delete_after_first_long.liggghts'), CKS, 1, '첫 긴 run 뒤 명령 다름'),
                (os.path.join(CX_DECK, 'include_after_first_long.liggghts'), CKS, 1, 'include'),
                (os.path.join(CX_DECK, 'first_run_every.liggghts'), CKS, 1, '첫 긴 run 꼴이 지원 밖'),
                (os.path.join(CX_DECK, 'first_run_pre_no.liggghts'), CKS, 1, '첫 긴 run 꼴이 지원 밖'),
                (os.path.join(CX_DECK, 'run_pre_no.liggghts'), CKS, 1, '첫 긴 run 꼴이 지원 밖'),
                (os.path.join(CX_DECK, 'run_post_no.liggghts'), CKS, 1, '첫 긴 run 꼴이 지원 밖'),
                (os.path.join(CX_DECK, 'first_run_upto_wrong.liggghts'), CKS, 1, '첫 긴 run 꼴이 지원 밖'),
                (os.path.join(CX_DECK, 'first_run_upto_right.liggghts'), CKS, 1, '첫 긴 run 꼴이 지원 밖'),
                (os.path.join(CX_DECK, 'run_upto_same_end.liggghts'), CKS, 1, '첫 긴 run 꼴이 지원 밖'),
                (os.path.join(CX_DECK, 'duplicate_loop_label.liggghts'), CKS, 1, 'label 이 겹침'),
                (os.path.join(CX_DECK, 'missing_target_variable.liggghts'), CKS, 1, '정의 전 변수를 씀'),
                (os.path.join(CX_DECK, 'duplicate_target_later.liggghts'), CKS, 1, '정의 전 변수를 씀'),
                (os.path.join(CX_DECK, 'missing_compute_control.liggghts'), CKS, 1, 'c_zmax'),
                (os.path.join(CX_DECK, 'missing_c_zmax_compute.liggghts'), CKS, 1, 'c_zmax'),
                (os.path.join(CX_DECK, 'changed_timestep_control.liggghts'), CKS, 1, '재개 지점 timestep 다름'),
                (os.path.join(CX_DECK, 'reorder_velocity_before_restart.liggghts'), CKS, 1, '준비 구간 명령 허용 안 됨'),
                (os.path.join(CX_DECK, 'rename_read_restart.liggghts'), CKS, 1, 'read_restart 가 체크포인트'),
                (os.path.join(CX_SCHED, 'continued_first_long_run.liggghts'), CKS, 1, '& 로 이어진 여러 줄'),
                (os.path.join(CX_DECK, 'after_settling_first_long_changed_300000.liggghts'), CKA, 1, '첫 긴 run 다름'),
                (os.path.join(CX_DECK, 'after_settling_damp_mismatch.liggghts'), CKA, 1, 'fix damp all viscous 1.0e-5')):
            rc, out = deckcheck_only(script, MAIN, path, ck[0], ck[1])
            chk('G1 -C Codex 고정물 %s → %s (%s)' % (os.path.relpath(path, CODEX), '통과' if want == 0 else '거부', frag),
                (rc == 0) == (want == 0) and frag in out, out)
        rc, out = deckcheck_only(script, os.path.join(R075, 'input_pse_r075_a.liggghts'), os.path.join(CX_DECK, 'loop_first_numeric_remaining2.liggghts'),
                                 'restart_pse_r075_a/restart_compress_1500000.bin', 1500000, ('plate_pse_r075_a_r30.stl',))
        chk('G2 -C Codex 고정물 loop_first_numeric_remaining2 (루프 첫 run 만 run 2) → 거부 (압축 체크포인트 · Codex: 완성된 고침 아님)',
            rc != 0 and Q3MSG in out, out)
        # 그 밖 같은 부류 (전체 프로그램 대조의 규칙마다 하나씩) — 합성 · 이 시험에서만
        for tag, text, frag in (
                ('준비 구간 velocity', good.replace('run 180000\n', 'velocity all set 0 0 0\nrun 180000\n'), '준비 구간 명령 허용 안 됨'),
                ('준비 구간 본 덱에 없는 print', good.replace('run 180000\n', 'print "hello"\nrun 180000\n'), '준비 구간 명령 허용 안 됨'),
                ('준비 구간 group region 꼴', good.replace('run 180000\n', 'group gx region reg_box\nrun 180000\n'), '준비 구간 명령 허용 안 됨'),
                ('준비 구간 shell rm', good.replace('run 180000\n', 'shell rm -rf post_kg50_d07_b40\nrun 180000\n'), '준비 구간 명령 허용 안 됨'),
                ('변수 꼴 index', good.replace('run 180000\n', 'variable zz index a b\nrun 180000\n'), '다룰 수 없는 변수 꼴 index'),
                ('준비 구간 변수 값 다름', re.sub(r'(?m)^(variable plate_margin equal) 0\.003', r'\1 0.004', good, count=1), '재개 지점 variable plate_margin 다름'),
                ('준비 구간 dump 더함', good.replace('run 180000\n', 'dump dx all custom 1000 x.dump id\nrun 180000\n'), '재개 지점 dump dx 는 재개 덱에만'),
                ('restart 설정 빠짐', re.sub(r'(?m)^restart 50000 [^\n]*\n', '', good, count=1), '재개 지점 restart 가 재개 덱에 없음'),
                ('jump 꼴 (다른 파일)', good.replace('run 180000\n', 'run 180000\njump other.in loop_press\n'), 'jump 꼴'),
                ('next', good.replace('run 180000\n', 'run 180000\nnext a\n'), '다룰 수 없는 구문 (재개 덱 · next'),
                ('if 안 include', good.replace('run 180000\n', 'run 180000\nif "1 > 0" then "include x.in"\n'), '다룰 수 없는 구문 (재개 덱 · include'),
                ('S0 가 그 run 범위 밖', None, '범위')):
            if text is None:
                rc, out = deckcheck_only(script, MAIN, write_tmp(tmp, 'g3s0.liggghts', good), CKPT, 200001)
            else:
                rc, out = deckcheck_only(script, MAIN, write_tmp(tmp, 'g3.liggghts', text), CKPT, 20001)
            chk('G3 -C 같은 부류 · %s → 거부 (%s)' % (tag, frag), rc != 0 and frag in out, out)
        with open(MAIN, encoding='utf-8') as f:
            tmn = f.read()
        mif = write_tmp(tmp, 'g3m.liggghts', mutate(tmn, 'compute zmax all reduce max z\n',
                                                    'if "1 > 0" then "fix extra all viscous 0.1"\ncompute zmax all reduce max z\n'))
        rc, out = deckcheck_only(script, mif, write_tmp(tmp, 'g3r.liggghts', good), CKPT, 20001)
        chk('G3 -C 같은 부류 · 본 덱 체크포인트 앞 if 가 fix 를 만든다 (그 시점 상태를 정할 수 없음) → 거부',
            rc != 0 and '본 덱 체크포인트 앞 if 에 print · quit · jump 말고 다른 명령' in out, out)
        # 허용 차이 목록 고정 (1저자 Q2 (가) · 지금 도구가 허용하던 것만): ① 첫 긴 run 남은 수 (F · K) ② 판 메시 fix 의 file 이름 (그 파일이
        #   작업 폴더에 있을 때만) ③ shell mkdir ↔ mkdir -p ④ 템플릿 fix 재선언 · 빠짐 (G1 scheduler/plain) ⑤ '선언하면 같아야' 상태 (compute ·
        #   변수 · dump · region · thermo) 의 빠짐 (G1 baseline = thermo · 삽입 검사 변수 없음) ⑥ 본 덱 체크포인트 앞에 글자 그대로 있는
        #   print · if (print · quit) · group type · shell mkdir (G1 baseline · P10)
        mstl = 'mesh/surface/stress file plate_%s.stl ' % C
        asr = mutate(res_after('good', tmpl=True), mstl, 'mesh/surface/stress file plate_%s_r56.stl ' % C)
        for tag, text, ck, files, want, frag in (
                ('② after_settling 판 fix 의 file 이름만 다름 · 파일 있음', asr, (CKPT_AS, 200001), ('plate_%s_r56.stl' % C,), 0, '판 메시 파일만 다름'),
                ('② 같은 꼴 · 파일 없음', asr, (CKPT_AS, 200001), (), 1, '판 메시 파일 plate_%s_r56.stl 가 작업 폴더에 없음' % C),
                ('③ shell mkdir → mkdir -p', mutate(good, 'shell mkdir restart_%s\n' % C, 'shell mkdir -p restart_%s\n' % C), (CKPT, 20001),
                 (), 0, '통과'),
                ('③ 같은 자리 다른 디렉터리', mutate(good, 'shell mkdir restart_%s\n' % C, 'shell mkdir -p restart_other\n'), (CKPT, 20001), (), 1,
                 '준비 구간 명령 허용 안 됨')):
            rc, out = deckcheck_only(script, MAIN, write_tmp(tmp, 'g6.liggghts', text), ck[0], ck[1], files)
            chk('G6 허용 차이 목록 %s → %s (%s)' % (tag, '통과' if want == 0 else '거부', frag), (rc == 0) == (want == 0) and frag in out, out)
        # 원본 → 시험 덱 → 관문 사슬 (가짜 SLURM · -T) — 시험 덱을 자르기 전에 거부되어야 (KG50R-02 · 05)
        for tag, text, frag in (
                ('첫 긴 run every', good.replace('run 180000\n', 'run 180000 every 1000 "velocity all set 1.0 0.0 0.0"\n'), '시험 덱을 못 만듦'),
                ('첫 긴 run & 이음 (Codex continued_first_long_run)', good.replace('run 180000\n', 'run &\n180000\n'), '시험 덱을 못 만듦'),
                ('첫 긴 run 뒤 velocity (Codex suffix_velocity)', good.replace('run 180000\n', 'run 180000\nvelocity all set 1.0 0.0 0.0\n'),
                 '첫 긴 run 뒤 명령 다름')):
            r = run_case(script, None, None, res_text=text, trial_text=ok_log, extra=('-T',))
            chk('G4 사슬 · %s → 시험 · 본 제출 안 함 (%s)' % (tag, frag),
                not r['trial'] and not r['main'] and frag in r['out'], r['out'])
        # 정상 재개 덱의 시험 덱 = 고치기 전 판 693 줄 awk 절단기와 바이트 같음 (줄 끝 주석 · & 이은 if · after_settling)
        nr, nt = 'input_%s_%s.liggghts' % (C, SFX), 'input_%s_%st.liggghts' % (C, SFX)
        for tag, kw in (('정상 settling', dict(res_text=good)),
                        ('run 줄 끝 주석 (F3 꼴 · 고친 뒤)', dict(res_text=res_variant('steps_ibb_comment'))),
                        ('& 이은 print · quit if (P10 꼴)', dict(res_text=res_variant('p_ifprint'))),
                        ('after_settling', dict(res_text=res_after('good'), mode='after_settling', ckpt=CKPT_AS, orig_log=AS_LOG))):
            r = run_case(script, None, None, trial_text=as_trial() if 'mode' in kw else ok_log, extra=('-T',), **kw)
            src = write_tmp(tmp, 'cutsrc.liggghts', '')
            with open(src, 'wb') as f:
                f.write(r['w_decks'].get(nr, b''))
            exp = subprocess.run(['awk', '-v', 't=2000', OLD_CUT, src], stdout=subprocess.PIPE).stdout
            chk('G5 %s → 시험 냄 · 시험 덱 = 고치기 전 awk 절단기 출력과 바이트 같음 (%d 바이트)' % (tag, len(exp)),
                r['trial'] and nt in r['w_decks'] and r['w_decks'][nt] == exp and len(exp) > 0, r['out'])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ── X: 압축 체크포인트 재개 = 거부 (KG50R-01 · KG50-19 · 1저자 10-28 Q3 (가)) ──
    grp('X')
    tmp = tempfile.mkdtemp(prefix='rckx_')
    try:
        with open(r075, encoding='utf-8') as f:
            t075 = f.read()
        for n, why in ((1500000, '판정 1,500,002 의 2 step 앞 (Codex §2)'), (1500002, '판정 step 그 자리'),
                       (1505000, '재개 판정 꼴 자리'), (3300000, '이완 중 restart_compress_* (KG50-11 · 이 덱엔 restart 0 없음)')):
            ck = 'restart_pse_r075_a/restart_compress_%d.bin' % n
            rc, out = deckcheck_only(script, m075, write_tmp(tmp, 'x%d.liggghts' % n, t075.replace('restart_compress_1500000.bin', 'restart_compress_%d.bin' % n)),
                                     ck, n, ('plate_pse_r075_a_r30.stl',))
            chk('X1 -C r075 압축 체크포인트 step %d (%s) → 거부 (%s)' % (n, why, Q3MSG), rc != 0 and Q3MSG in out, out)
        ck6 = 'restart_%s/restart_compress_600000.bin' % C
        rc, out = deckcheck_only(script, MAIN, write_tmp(tmp, 'x6.liggghts', good.replace(CKPT, ck6)), ck6, 600000)
        chk('X2 -C v2 본 덱 · 압축 체크포인트 이름 restart_compress_600000 → 거부 (압축 체크포인트 재개 = 지원 안 함)',
            rc != 0 and Q3MSG in out, out)
        r = run_case(script, 'good', 'ok', mode='compress', ckpt=ck6, extra=('-T',))
        chk('X3 본 흐름 · dem_restart.py 계획 = compress → 시험 · 본 제출 안 함 · stdout · 보고 케이스 절에 거부 (단계 · 이유 · 시도 · Q9)',
            not r['trial'] and not r['main'] and Q3MSG in r['out'] and '단계: 압축 체크포인트 (Q3)' in r['rep'] and Q3MSG in r['rep'],
            r['out'] + r['rep'])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ── L: G0 마지막 thermo 줄 · Loop step 수 (KG50R-07 · Q5) ──
    grp('L')
    with open(os.path.join(G0_LOGS, 'bad_final.log'), encoding='utf-8') as f:
        bad_final = f.read()
    with open(os.path.join(G0_LOGS, 'bad_late.log'), encoding='utf-8') as f:
        bad_late = f.read()
    r = run_case(script, None, None, res_text=good, trial_text=bad_final)
    chk('L1 우리 재현 bad_final.log (마지막 정상 줄 22000 뒤 한 토큰 "22001" · Loop for 1999 steps) → G0 실패 (마지막 step 22000) · 본 제출 안 함',
        r['trial'] and not r['main'] and 'G0 시험 정상 종료: 실패' in r['rep'] and '마지막 step 22000 (기대 22001)' in r['rep'], r['rep'])
    r = run_case(script, None, None, res_text=good, trial_text=bad_late, extra=('-T',))
    chk('L2 우리 재현 bad_late.log (22000 줄 Atoms 10 · KE 1e6 · 마지막 22001 줄 온전) → G0 통과 (마지막 줄만의 계약 · 22000 줄은 G3 첫 줄 '
        '수치 비교 밖 = 공개된 설계 · Codex Q6) — 범위 기록',
        r['trial'] and 'G0 시험 정상 종료: 통과' in r['rep'] and 'G3 원 로그 비교 구간 (step 21000 부터' in r['rep'], r['rep'])
    for tag, text in (('Loop for 1999 steps (마지막 run 2000)', ok_log.replace('for 2000 steps', 'for 1999 steps')),
                      ('마지막 줄 KE nan', '\n'.join(['LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0)'] + T_OK[:-2]
                                                    + ['%8d %8d %14s %10s' % (22001, 312506, 'nan', '2.001'), T_OK[-1]]) + '\n'),
                      ('마지막 줄 칸 3 (머리 4)', '\n'.join(['LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0)'] + T_OK[:-2]
                                                       + ['%8d %8d %14s' % (22001, 312506, '0.0902'), T_OK[-1]]) + '\n')):
        r = run_case(script, None, None, res_text=good, trial_text=text)
        chk('L3 %s → G0 실패 · 본 제출 안 함 (KG50R-07)' % tag,
            r['trial'] and not r['main'] and 'G0 시험 정상 종료: 실패' in r['rep'], r['rep'])

    # ── I: 도구 신원 · 본 제출 승인 (Codex Q7 · 1저자 Q4) ──
    grp('I')
    hsha, tsha = hashlib.sha256(FAKE_DEM_RESTART.encode()).hexdigest(), sha256f(script)
    for tag, ap in (('승인 인자 없음', None), ('-A 틀림', 'badA'), ('-H 틀림', 'badH')):
        r = run_case(script, 'good', 'ok', approve=ap)
        chk('I1 -T 없음 · %s → 아무것도 하지 않음 (작업 폴더 · 시험 · 본 제출 없음 · 실제 sha256 을 찍음)' % tag,
            not r['trial'] and not r['main'] and not r['w_exists'] and '⛔ 본 제출 승인 인자' in r['out'] and tsha in r['out'], r['out'])
    r = run_case(script, 'good', 'ok', extra=('-T',))
    mc = [l for l in r['rep'].splitlines() if l.startswith('- 본 제출 명령')]
    chk('I2 -T → 보고에 도구 sha256 둘 (resume_ckpt.sh · dem_restart.py) · 본 제출 명령 한 줄 (-T 없이 -A · -H 승인값)',
        r['trial'] and not r['main'] and ('resume_ckpt.sh sha256 %s' % tsha) in r['rep'] and ('dem_restart.py sha256 %s' % hsha) in r['rep']
        and len(mc) == 1 and mc[0].count('`') == 2 and mc[0].split('`')[1].endswith('-A %s -H %s %s' % (tsha, hsha, C))
        and ' -T' not in mc[0].split('`')[1], r['rep'])
    r = run_case(script, 'good', 'ok', env_more={'FAKE_TOUCH_HELPER': '{helper}'})
    chk('I3 시험 제출 뒤 dem_restart.py 가 바뀜 → 본 제출 직전 sha256 다시 대조 → 본 제출 안 함',
        r['trial'] and not r['main'] and '도구 sha256 이 승인값과 다름' in r['rep'], r['out'] + r['rep'])
    r = run_case(script, 'good', 'ok')
    a = dict((k.split('/', 1)[1], v) for k, v in r['att'].items() if '/' in k)
    chk('I4 정상 본 제출 → 시도 폴더에 도구 신원 · 시험 job · mode · 덱 · 러너 · 본 job (tool.txt · job_t.txt 7001 · main_job.txt 9001)',
        r['main'] and ('resume_ckpt.sh sha256 %s' % tsha) in a.get('tool.txt', '') and ('dem_restart.py sha256 %s' % hsha) in a.get('tool.txt', '')
        and a.get('job_t.txt') == '7001\n' and a.get('main_job.txt') == '9001\n' and a.get('mode.txt', '').startswith('settling 20001 ')
        and all(n in a for n in ('input_%s_%s.liggghts' % (C, SFX), 'input_%s_%st.liggghts' % (C, SFX), 'run_%s_%s.sh' % (C, SFX),
                                 'run_%s_%st.sh' % (C, SFX), 'deckcheck_%s.txt' % SFX, 'cut_%s.txt' % SFX, 'result.txt')),
        ' '.join(sorted(a)) + r['out'])
    # -T 의 본 제출 명령 = 이번 -T 에서 G0–G3 를 통과한 케이스만 — 거부 · 실패 뒤에 본 제출 명령 줄이 통과처럼 읽히지 않게
    def mcmd(rep):
        return [l for l in rep.splitlines() if l.startswith('- 본 제출 명령')]
    r = run_case(script, 'good', 'ok', squeue='%s_ins' % C, extra=('-T',))
    mc = mcmd(r['rep'])
    chk('I5 -T · 시험 전 거부 (큐) → 본 제출 명령 없음 (그 줄이 거부 케이스를 담지 않음)',
        not r['trial'] and len(mc) == 1 and mc[0].startswith('- 본 제출 명령 없음') and '`' not in mc[0] and C in mc[0], r['rep'])
    r = run_case(script, 'good', 'ok', sacct='COMPLETED|1:0', extra=('-T',))
    mc = mcmd(r['rep'])
    chk('I6 -T · 시험 G0 실패 → 본 제출 명령 없음',
        r['trial'] and not r['main'] and len(mc) == 1 and mc[0].startswith('- 본 제출 명령 없음') and '`' not in mc[0], r['rep'])
    r = run_case(script, 'good', 'ok', extra=('-T',), cases=[C, 'kg50_none'])
    mc = mcmd(r['rep'])
    chk('I7 -T · 두 케이스 중 하나만 G0–G3 통과 (다른 하나 = 멈춘 폴더 없음) → 본 제출 명령에 통과 케이스만 · 빠진 케이스 이름',
        r['ntrial'] == 1 and len(mc) == 1 and mc[0].count('`') == 2 and mc[0].split('`')[1].endswith('-A %s -H %s %s' % (tsha, hsha, C))
        and 'kg50_none' not in mc[0].split('`')[1] and '빠짐: kg50_none' in mc[0], r['rep'])

    # ── Q9: 시험 전 거부도 보고 케이스 절 (Codex Q9) ──
    grp('Q9')
    r = run_case(script, 'damp_wrong', 'ok')
    chk('Q9a 정적 대조 거부 → 보고 케이스 절 (단계 정적 대조 · 시험 덱 · 이유에 대조 문제 줄 · 시도)',
        ('## %s — 시험 전 거부' % C) in r['rep'] and '단계: 정적 대조 · 시험 덱' in r['rep'] and '재개 지점 fix damp 다름' in r['rep']
        and re.search(r'시도 attempt_r56_[0-9_]+', r['rep']), r['rep'])
    r = run_case(script, 'good', 'ok', squeue='%s_ins' % C)
    chk('Q9b 큐에 삽입 잡 → 보고 케이스 절 (단계: 큐)', ('## %s — 시험 전 거부' % C) in r['rep'] and '단계: 큐 ·' in r['rep'], r['rep'])
    r = run_case(script, 'good', 'ok', env_more={'FAKE_SBATCH_TRIAL_EMPTY': '1'})
    chk('Q9c 시험 sbatch 빈 출력 → 본 제출 안 함 · 보고 케이스 절 (단계: 시험 제출)',
        r['trial'] and not r['main'] and '단계: 시험 제출' in r['rep'], r['out'] + r['rep'])
    r = run_case(script, 'good', 'ok', env_more={'FAKE_SBATCH_TRIAL_TEXT': 'sbatch: error: Batch job submission failed: QOS limit'})
    chk('Q9d 시험 sbatch 가 job 번호 아닌 글 (종료 코드 1) → 시험 job 으로 안 받음 · 본 제출 안 함 · 보고 케이스 절 (단계: 시험 제출 · KG50R-04)',
        r['trial'] and not r['main'] and '단계: 시험 제출' in r['rep'] and 'QOS limit' in r['rep'], r['out'] + r['rep'])

    print('%d PASS · %d FAIL' % (ok, fail))
    if CMP['old'] is not None:
        print('── 옛 판 대조 (--compare-old %s · 판정은 지금 판으로만 · 새 줄 (표지 %s) · 시도 폴더 · cut_*.txt 빼고) — 장면 %d'
              % (CMP['old'], NEW_MARK, len(CMP['rows'])))
        tagn = {(True, True): ' (둘 다 정상)', (True, False): ' (옛 판 정상 · 새 판 거부)', (False, True): ' (새 판만 정상)', (False, False): ''}
        for g, desc, d, on, nn in CMP['rows']:
            print('  %s %s%s · %s%s' % ('같음' if not d else '다름', g, tagn[(on, nn)], desc, '' if not d else ' — ' + ', '.join(d)))
        groups = []
        for x in CMP['rows']:
            if x[0] not in groups:
                groups.append(x[0])
        for g in groups:
            rows = [x for x in CMP['rows'] if x[0] == g]
            print('  묶음 %s: 같음 %d / %d' % (g, len([x for x in rows if not x[2]]), len(rows)))
        # 굳은 조건 (rc 1) = 예전부터 있던 장면 묶음 (K S D Q T N F C A P W) 에서 둘 다 정상인데 다름 — 영향 없는 settling ·
        #   after_settling 정상 출력이 그대로인지.  10-28 밤 새 묶음 (R G X L I Q9) 은 새 행동을 시험하려고 만든 장면이라 보고만 한다
        old_g = ('K', 'S', 'D', 'Q', 'T', 'N', 'F', 'C', 'A', 'P', 'W')
        both = [x for x in CMP['rows'] if x[3] and x[4]]
        nd = [x for x in both if x[2] and x[0] in old_g]
        info = [x for x in both if x[2] and x[0] not in old_g]
        flip = [x for x in CMP['rows'] if x[3] and not x[4]]
        print('  둘 다 정상인 장면 (시험 · G0–G3 통과 / -C 통과) %d — 예전 묶음에서 다름 %d · 새 묶음에서 다름 %d (보고만: %s)'
              % (len(both), len(nd), len(info), ' | '.join('%s %s — %s' % (x[0], x[1], ', '.join(x[2])) for x in info) or '없음'))
        print('  옛 판 정상 · 새 판 거부 %d: %s' % (len(flip), ' | '.join('%s %s' % (x[0], x[1]) for x in flip) or '없음'))
        if nd:
            return 1
    return 0 if fail == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
