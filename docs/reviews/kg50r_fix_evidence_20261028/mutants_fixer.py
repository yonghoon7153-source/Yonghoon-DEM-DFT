#!/usr/bin/env python3
"""새 관문 하나씩 끈 변이 판 → scripts/test_resume_ckpt.py --script <변이> → 실패한 시험 이름.  (작업 트리 · scratchpad 만)"""
import concurrent.futures as cf
import os
import re
import subprocess
import sys

WT = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/kg50fix-1028'
SP = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(SP, 'final_tool2.sh')
TEST = os.path.join(WT, 'scripts/test_resume_ckpt.py')

M = [
    ('M1 Q1 둘째 고리 = 작업 폴더 job 파일 (예전)',
     'for ENT in $SUBMITTED; do\n  C=${ENT%|*}; J=${ENT##*|}; W=$L/$C; S=$L/$C.$SUF; AD=$W/$ATT\n',
     'for C in $CASES; do\n  W=$L/$C; S=$L/$C.$SUF; [ -f $W/job_${SFX}t.txt ] || continue; J=$(cat $W/job_${SFX}t.txt); '
     'AD=$(ls -d $W/attempt_*/ 2>/dev/null | tail -1); AD=${AD%/}; { [ -n "$AD" ] && [ -f $AD/mode.txt ]; } || '
     '{ AD=$W/attempt_mut; mkdir -p $AD; cp $W/mode_$SFX.txt $AD/mode.txt; echo 2000 > $AD/lastrun_n.txt; }\n'),
    ('M2 Q1 본 제출 직전 squeue 다시 조회 끔',
     'QL2=$(squeue -u $USER -h -o \'%i %j\' 2>/dev/null) || BLK="본 제출 직전 squeue 조회 실패 (돌고 있는지 모른다)"',
     'QL2=""'),
    ('M3 Q1 다시 조회에서 이번 시험 job 빼기 끔',
     "awk -v j=\"$J\" 'NF>=2 && $1!=j {print $2}'", "awk 'NF>=2 {print $2}'"),
    ('M4 Q1 시험 sbatch 종료 코드 · job 번호 꼴 검사 끔',
     'if [ $JR = 0 ] && [[ "$J" =~ ^([0-9]+)(;[^[:space:]]*)?$ ]]; then J=${BASH_REMATCH[1]}',
     'if [ -n "$J" ]; then :'),
    ('M5 Q1 같은 케이스 두 번 막기 끔',
     'case "$SEEN" in *" $C "*) rej', 'case "$SEEN" in *" $C ZZ"*) rej'),
    ('M6 Q1 옛 job · mode 파일 old_markers 옮기기 끔',
     'OM=$(ls -d $W/job_*t.txt $W/mode_*.txt 2>/dev/null | tr \'\\n\' \' \')', 'OM=""'),
    ('M7 Q2 첫 긴 run 뒤 명령 대조 끔',
     "    seq_cmp(M[im + 1:], R[ir + 1:], W, notes, probs, '첫 긴 run 뒤 명령')\n", ''),
    ('M8 Q2 준비 구간 명령 종류 검사 끔',
     "def setup_check(Rs, Mp, probs):\n", "def setup_check(Rs, Mp, probs):\n    return\n"),
    ('M9 Q2 재개 지점 상태 대조 끔',
     "def state_cmp(stM, stR, W, notes, probs):\n", "def state_cmp(stM, stR, W, notes, probs):\n    return\n"),
    ('M10 Q2 변수 참조 검사 끔',
     "def var_refs(R, probs):\n", "def var_refs(R, probs):\n    return\n"),
    ('M11 Q2 label · jump 검사 끔',
     "def label_check(M, R, pM, probs):\n", "def label_check(M, R, pM, probs):\n    return\n"),
    ('M12 Q2 다룰 수 없는 구문 검사 끔',
     "def unsupported(l):\n", "def unsupported(l):\n    return ''\n"),
    ('M13 Q2 첫 긴 run 꼴 검사 끔',
     "def first_run_form(res, R, ir):\n", "def first_run_form(res, R, ir):\n    return ''\n"),
    ('M14 Q2 자른 시험 덱 명령 = 재개 덱 앞 + run 대조 끔',
     "        if deck(t) != R[:ir] + ['run %d' % tn]:\n", "        if False:\n"),
    ('M15 Q2 시험 예산 대조 (shell) 끔',
     '    if [ "$CPS" = - ] || [ "$NT" != $((CPS + CTN)) ] || [[ "$TDS" != *"[run $CTN]" ]]; then\n', '    if false; then\n'),
    ('M16 Q2 read_restart = 체크포인트 검사 끔',
     "    if len(rw) != 2 or os.path.normpath(rw[1]) != os.path.normpath(ckpt):\n", "    if False:\n"),
    ('M17 Q2 체크포인트 step 범위 검사 끔',
     "            if not step0 < s0 < step:\n", "            if False:\n"),
    ('M18 Q2 본 덱 체크포인트 앞 if 검사 끔',
     "def mprefix_check(Mp, probs):\n", "def mprefix_check(Mp, probs):\n    return\n"),
    ('M19 Q2 변수 꼴 (equal · atom · string · delete 만) 검사 끔',
     "            elif w[2] in VAR_OK:\n", "            elif True:\n"),
    ('M20 Q3 -C 압축 체크포인트 거부 끔',
     "        if base.startswith('restart_compress_') or (not known and labs):\n", "        if False:\n"),
    ('M21 Q3 본 흐름 계획 compress 거부 끔',
     '  [ "$M" = compress ] && { rej', '  [ "$M" = compressZZ ] && { rej'),
    ('M22 Q4 시작 때 승인 인자 대조 끔',
     'if [ $TONLY = 0 ] && ! {', 'if false && ! {'),
    ('M23 Q4 본 제출 직전 sha256 다시 대조 끔',
     '[ -z "$BLK" ] && { [ "$T2" != "$APT" ] || [ "$H2" != "$APH" ]; } && BLK=', '[ -z "$BLK" ] && false && BLK='),
    ('M24 Q5 마지막 줄 칸 수 · 유한 수 검사 끔 (예전 lastrun 꼴)',
     'q&&NF==n&&$1~/^[0-9]+$/{ok=1;for(i=1;i<=NF;i++)if(!fin($i)){ok=0;break};if(ok){s=$1;ln=NR}}',
     'q&&$1~/^[0-9]+$/{s=$1;ln=NR}'),
    ('M25 Q5 Loop for N steps = 마지막 run 검사 끔',
     ' && [ "$LPN" = "$LN" ] && [ "$E" = 0 ]', ' && [ "$E" = 0 ]'),
    ('M26 Q9 시험 전 거부 보고 케이스 절 끔',
     '  echo "- ⛔ 시험 전 거부 (KG50R) — 단계', '  : "- ⛔ 시험 전 거부 (KG50R) — 단계'),
    ('M27 Q4 -T 본 제출 명령 = 통과 케이스 있을 때만 끔 (늘 찍음)',
     '  if [ -n "$TPASS" ]; then echo "- 본 제출 명령 (', '  if true; then echo "- 본 제출 명령 ('),
    ('M28 Q4 -T 본 제출 명령 = 통과 케이스만 끔 (전 케이스)',
     '-H ${HSHA:-없음}$TPASS\\`', '-H ${HSHA:-없음} $CASES\\`'),
]


def run(m):
    name, old, new = m
    with open(SRC, encoding='utf-8') as f:
        src = f.read()
    n = src.count(old)
    if n != 1:
        return name, 'BAD (자리 %d 곳)' % n, []
    p = os.path.join(SP, 'mut_%s.sh' % re.sub(r'[^0-9A-Za-z]', '', name.split()[0]))
    with open(p, 'w', encoding='utf-8') as f:
        f.write(src.replace(old, new))
    r = subprocess.run([sys.executable, TEST, '--script', p], cwd=WT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1800)
    out = r.stdout.decode('utf-8', 'replace')
    fails = [l[5:].split(' ')[0] for l in out.splitlines() if l.startswith('FAIL ')]
    last = [l for l in out.splitlines() if 'PASS ·' in l]
    return name, last[-1] if last else out[-300:], fails


if __name__ == '__main__':
    with cf.ThreadPoolExecutor(max_workers=int(os.environ.get('NJ', '4'))) as ex:
        for name, summ, fails in ex.map(run, M):
            print('%s | %s | 실패: %s' % (name, summ, ' '.join(fails) if fails else '(없음 · 살아남음)'), flush=True)
