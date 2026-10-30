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
10-28 밤 2 (독립 사전 공격 리뷰 · 고친 판 fb334928) — Y = 반례 A (준비 구간 변수 다시 정의 · 순서) · B (본 덱 체크포인트 run 꼬리 ·
run every 안 include) · C (시험 뒤 덱 · 러너 바뀜 · 실행 영수증) · D (본 sbatch 출력) · E (G3 유한 수) · F (케이스 이름 · 시도 기록 읽기) ·
시험 빈틈 셋 (재삽입 · G1 만 · G3 결손만 — 리뷰어 변이 py_reinsert · sh_g1 · sh_miss 가 살아남던 자리).
10-30 (Codex 재확인 KG50RF-02 · 원장 KG50R-F02 · 1저자 Q2 *"권고대로"*) — RB = 러너 결속: 검사한 덱 ↔ 잡이 실제로 읽는 덱.  가짜 sbatch 가
제출된 러너를 실제로 돌리고 (예전 = 제공 로그 복사만) 가짜 mpirun 이 cwd · 인자 · -in sha256 을 적는다 · 가짜 dem_restart.py 의 러너 = 실제
헬퍼 꼴 (--output · cd = 작업 폴더 실제 경로).  Codex 반례 (.bak · 다른 cd · 주석 속 정상 줄 · 둘째 MPI 실행) + 같은 부류는 sbatch 0 회 ·
실제 D2 헬퍼 러너 꼴 (ibb /home → /lustre 별칭) 은 시험 1 · 본 1 + 기록된 cwd · -in · 바이트 · 영수증 다섯 (재개 덱 · 러너 · 시험 덱 · 시험 러너 ·
체크포인트).  Codex 반례 폴더 (independent/launch/) 는 읽기만 — 같은 꼴을 여기서 만든다.
10-30 (독립 사전 공격 리뷰 · 도구 5f4ffb46 · P2 셋 · P3 일곱 · PA-01–10) — RB 에 더함: 잡이 실제로 읽는 바이트 (가짜 sbatch 가 러너를
SLURM 처럼 제출 때 사본으로 떠서 돌리고 · 잡 앞뒤 고리 FAKE_PRE_SPOOL · _PRE_TRIAL · _POST_TRIAL · _PRE_MAIN · _POST_MAIN) · 시험 로그
잡 안 덱 신원 관문 (-T · 본 흐름) · 잡 안 sha256 대조 (시험 · 본 잡 시작 전) · 멈춘 폴더 링크 · 환경 줄 음성 · -n · -x 시작 거부 · 잡 안 cd 실패 ·
BASH_ENV 의 mpirun 함수 · 경로 속 ERROR · runnerck 직접 호출 (RBU).  리뷰어 장면 (attack.py) 은 같은 꼴을 여기서 만든다.
10-30 (KG50R-F01 2 판 · 독립 사전 공격 R1–R8 · 1저자 "권고대로") — VP = 정적 대조의 남은 구멍: 상태 표 키 자리 치환 (R1) · 본 덱 체크포인트 앞
run every · partition 안 명령 (R2) · 줄 읽기 = LIGGGHTS file()/parse() (R3) · 준비 구간 print file 을 읽는 명령 (R4) · write_restart 체크포인트 앞
흐름 줄 (R5) · 판 메시 file 이름 = 펼친 이름 (R6) · 펼친 글 크기 상한 (R7) · group 값 대조 (R8).

  python3 scripts/test_resume_ckpt.py                 # 고친 스크립트 (기본)
  python3 scripts/test_resume_ckpt.py --only RB       # RB 묶음만 (변이 시험용)
  python3 scripts/test_resume_ckpt.py --only VP       # VP 묶음만 (변이 시험용)
  python3 scripts/test_resume_ckpt.py --script <경로>  # 다른 판 (고치기 전 판 실패 확인용)
  python3 scripts/test_resume_ckpt.py --compare-old <옛 판>
      # 장면마다 옛 판도 같은 입력으로 돌려 stdout · 보고 · 작업 폴더 파일 · 제출 여부를 대조 (임시 경로 · 날짜 시각만 맞춤 ·
      # 10-28 밤 새로 더한 줄 (표지 'KG50R' 가 든 줄) · 시도 폴더 · cut_*.txt 는 빼고 · 승인 인자 -A · -H 는 새 판에만)
      # → 묶음별 같음 / 다름 · 예전부터 있던 묶음 (K S D Q T N F C A P W) 에서 옛 판 · 새 판 둘 다 정상 (시험 · G0–G3 통과 / -C 통과)
      #   인 장면에 다름이 있으면 rc 1 · 새 묶음 (R G X L I Q9 Y) 의 다름 · 옛 판 정상인데 새 판이 거부한 장면은 목록으로 보고만
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
#   10-28 밤 2 (사전 공격 C · D): FAKE_EDIT_AFTER_TRIAL = 시험 제출 때 그 파일 (작업 폴더 재개 덱 · 러너) 끝에 주석 한 줄 ·
#   FAKE_SBATCH_MAIN_TEXT = 본 제출이 그 글을 내고 종료 코드 1 · FAKE_SBATCH_MAIN_SUFFIX = 본 job 번호 뒤에 그 꼬리 (--parsable 'id;cluster')
#   10-30 (KG50R-F02 · Codex KG50RF-02 · 1저자 Q2): 제출된 러너를 실제로 돈다 — 예전 = 제공 로그만 logs/ 로 복사 (러너가 어느 cwd · 어느 -in 을
#     읽는지 못 봤다).  SLURM 처럼 제출 폴더에서 bash <러너> · stdout+stderr = 러너의 #SBATCH --output (%j = job · 없으면 slurm-%j.out) ·
#     SLURM_JOB_ID · FAKE_JOB_KIND (trial · main) 를 넘긴다 · 러너 안 mpirun = 아래 가짜 mpirun (stub 폴더가 PATH 맨 앞).
#     제출 실패 (FAKE_SBATCH_MAIN_TEXT · _TRIAL_TEXT · _TRIAL_EMPTY) = 잡이 없으니 안 돈다 · 시험 로그 고정물 없음 (FAKE_TRIAL_LOG 빈 값) 인 시험 =
#     출력 파일을 안 만든 잡 (예전 S6 '시험 로그 없음' 장면 그대로).  FAKE_EDIT_GLOB = 시험 제출 때 그 글로브의 파일마다 끝에 주석 한 줄 ·
#     FAKE_DROP_LAST_GLOB = 시험 제출 때 그 글로브의 파일마다 마지막 줄 지움 (시도 폴더 영수증처럼 이름에 시각이 든 파일용)
#   10-30 (사전 공격 PA-01 · 02): 러너를 SLURM 처럼 제출 때 사본 ($CAPTURE.spool.<job>) 으로 떠서 그 사본을 돈다 (제출 뒤 러너 파일을 고쳐도
#     잡에 안 닿는다 · 덱 · 체크포인트를 고치면 닿는다).  고리 (sh -c '<글>' fake <러너> <종류> · $1 = 러너 · $2 = trial | main):
#     FAKE_PRE_SPOOL = 사본 뜨기 전 (러너 파일을 고치면 잡이 그 글을 돈다) · FAKE_PRE_TRIAL · FAKE_PRE_MAIN = 사본 뒤 · 잡 시작 전 (큐 대기) ·
#     FAKE_POST_TRIAL · FAKE_POST_MAIN = 잡 끝난 뒤
STUB_SBATCH = r'''#!/bin/sh
f=""; for a in "$@"; do f="$a"; done
b=$(basename "$f" .sh); n=${b#run_}
case "$b" in *t) kind=trial;; *) kind=main;; esac
if [ $kind = main ] && [ -n "$FAKE_SBATCH_MAIN_TEXT" ]; then echo "main $f" >> "$CAPTURE"; echo "$FAKE_SBATCH_MAIN_TEXT"; exit 1; fi
if [ $kind = trial ]; then
  echo "trial $f" >> "$CAPTURE"
  [ -n "$FAKE_TOUCH_HELPER" ] && echo "# 시험 제출 뒤 바뀜" >> "$FAKE_TOUCH_HELPER"
  [ -n "$FAKE_EDIT_AFTER_TRIAL" ] && echo "# 시험 제출 뒤 바뀜 (사전 공격 C)" >> "$FAKE_EDIT_AFTER_TRIAL"
  if [ -n "$FAKE_EDIT_GLOB" ]; then for p in $FAKE_EDIT_GLOB; do echo "# 시험 제출 뒤 바뀜 (10-30 KG50R-F02)" >> "$p"; done; fi
  if [ -n "$FAKE_DROP_LAST_GLOB" ]; then for p in $FAKE_DROP_LAST_GLOB; do sed -i '$d' "$p"; done; fi
  [ -n "$FAKE_SBATCH_TRIAL_EMPTY" ] && exit 0
  [ -n "$FAKE_SBATCH_TRIAL_TEXT" ] && { echo "$FAKE_SBATCH_TRIAL_TEXT"; exit 1; }
  j=$((7000 + $(grep -c '^trial' "$CAPTURE")))
else
  echo "main $f" >> "$CAPTURE"; j=$((9000 + $(grep -c '^main' "$CAPTURE")))
fi
if [ $kind = main ] || [ -n "$FAKE_TRIAL_LOG" ]; then
  o=$(sed -n 's/^#SBATCH --output=//p' "$f" | tail -1); [ -n "$o" ] || o="slurm-%j.out"
  o=$(printf '%s' "$o" | sed "s/%j/$j/g")
  [ -n "$FAKE_PRE_SPOOL" ] && sh -c "$FAKE_PRE_SPOOL" fake "$f" "$kind"
  sp="$CAPTURE.spool.$j"; cp "$f" "$sp"
  case $kind in trial) pre=$FAKE_PRE_TRIAL; post=$FAKE_POST_TRIAL;; *) pre=$FAKE_PRE_MAIN; post=$FAKE_POST_MAIN;; esac
  [ -n "$pre" ] && sh -c "$pre" fake "$f" "$kind"
  SLURM_JOB_ID=$j FAKE_JOB_KIND=$kind bash "$sp" > "$o" 2>&1 < /dev/null
  [ -n "$post" ] && sh -c "$post" fake "$f" "$kind"
  rm -f "$sp"
fi
if [ $kind = main ]; then echo "$j$FAKE_SBATCH_MAIN_SUFFIX"; else echo $j; fi
'''
# 10-30 (KG50R-F02): 가짜 mpirun — 실제 cwd (pwd -P) · 인자 하나하나 · -in 파일 sha256 (그 cwd 기준 · 없으면 MISSING) 을 $FAKE_MPIRUN_REC 에
#   한 묶음씩 (begin <종류> <job> … end) 적고, 시험 = 시험 로그 고정물 (FAKE_TRIAL_LOG) 을 stdout 으로 (가짜 sbatch 가 #SBATCH --output 으로 보낸다
#   = 도구가 읽는 logs/output_<C>_<SFX>t_<job>.out) · 본 = 표지 한 줄.  실제 LIGGGHTS · MPI 0
STUB_MPIRUN = r'''#!/bin/sh
in=""; prev=""
for a in "$@"; do [ "$prev" = "-in" ] && in="$a"; prev="$a"; done
{ printf 'begin %s %s\n' "${FAKE_JOB_KIND:-?}" "${SLURM_JOB_ID:-?}"
  printf 'cwd %s\n' "$(pwd -P)"
  for a in "$@"; do printf 'arg %s\n' "$a"; done
  if [ -n "$in" ] && [ -f "$in" ]; then printf 'in_sha256 %s\n' "$(sha256sum < "$in" | cut -c1-64)"; else printf 'in_sha256 MISSING\n'; fi
  printf 'end\n'; } >> "$FAKE_MPIRUN_REC"
if [ "$FAKE_JOB_KIND" = trial ]; then [ -n "$FAKE_TRIAL_LOG" ] && cat "$FAKE_TRIAL_LOG"; else echo "FAKE MAIN RUN (가짜 mpirun)"; fi
exit 0
'''
#   10-28 밤 2 (사전 공격 F): FAKE_RM_MODE = 그 작업 폴더의 시도 폴더 mode.txt 를 지운다 (둘째 고리가 읽기 전 · sacct 를 처음 부를 때)
STUB_SACCT = ('#!/bin/sh\n[ -n "$FAKE_RM_MODE" ] && rm -f "$FAKE_RM_MODE"/attempt_*/mode.txt\n'
              'printf "%s\\n" "$FAKE_SACCT"\nexit ${FAKE_SACCT_RC:-0}\n')
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
# 가짜 dem_restart.py 의 러너 (10-30 KG50R-F02) — 실제 dem_restart.py 꼴 (ibb D2 r4 · 09-27 r075 r30 러너: #SBATCH --output · cd = 작업 폴더
#   실제 경로 /lustre/… · 도구가 -n · -np 를 NP 로 고친다).  예전 가짜 러너 = cd $HOME/dem_test/<케이스> (가짜 루트의 작업 폴더가 아님 · --output 없음) —
#   러너를 실제로 돌리지 않던 때라 안 보였다 · 10-30 엄격 대조 (cd 실제 경로 = 작업 폴더) 에 맞게 바꿈.
#   {W} = 작업 폴더 실제 경로 · {CS} = <케이스>_<접미사> · {C} = 케이스 · {ROOT} = --root 그대로
RB_BASE = ('#!/bin/bash\n#SBATCH --job-name={CS}\n#SBATCH --output=logs/output_{CS}_%j.out\n#SBATCH -n 1\n'
           '#SBATCH --time=5-00:00:00\ncd {W}\nmpirun -np 1 lmp_mpi -in input_{CS}.liggghts\n')
#   FAKE_RUNNER = 그 파일 바이트 (위 자리표만 바꿈 · 줄 끝 · NUL · UTF-8 아닌 바이트 그대로) 를 러너로 (RB 묶음) · 없으면 RB_BASE
FAKE_DEM_RESTART = r'''#!/usr/bin/env python3
import os, shutil, sys
a = sys.argv
case, root, sfx = a[a.index('--case-list') + 1], a[a.index('--root') + 1], a[a.index('--suffix') + 1]
W = os.path.join(root, case)
if os.environ.get('FAKE_DEM_FAIL'):
    print('  제외: %s (가짜 · 체크포인트 없음)' % case)
    sys.exit(0)
shutil.copy(os.environ['FAKE_RES'], os.path.join(W, 'input_%s_%s.liggghts' % (case, sfx)))
t = __RB_BASE__.encode()
if os.environ.get('FAKE_RUNNER'):
    with open(os.environ['FAKE_RUNNER'], 'rb') as f:
        t = f.read()
for k, v in (('{W}', os.path.realpath(W)), ('{CS}', '%s_%s' % (case, sfx)), ('{C}', case), ('{ROOT}', root)):
    t = t.replace(k.encode(), v.encode())
with open(os.path.join(W, 'run_%s_%s.sh' % (case, sfx)), 'wb') as f:
    f.write(t)
print('  %s  %s  %s' % (case, os.environ.get('FAKE_MODE', 'settling'), os.environ.get('FAKE_CKPT', '')))
'''.replace('__RB_BASE__', repr(RB_BASE))
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
    if kind == 'p_ifprint':
        # 10-28 밤 2 (사전 공격 A · 순서 대조): 삽입 자기검사 블록은 본 덱에서 정착 단계 print 앞에 있다 — 그 자리 (본 덱 순서) 에 둔다
        #   (예전 = 첫 긴 run 바로 앞 = restart 50000 뒤 · 이제 순서 보존 부분열이 아니라 거부된다 · 이 시험의 몫 = if-print 시험 덱)
        return mutate(g, 'print "====== PHASE 1: SETTLING ======"\n', pre[kind] + 'print "====== PHASE 1: SETTLING ======"\n')
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
    #   10-30 (KG50R-F02): 러너 run_*.sh 도 뺀다 — 고친 판은 본 · 시험 러너를 도구 틀로 쓴다 (헬퍼 러너 sed 사본 아님 · 옛 판과 바이트가 다른 게 정상 ·
    #   러너 내용은 RB 묶음이 따로 본다)
    out = {}
    for rel, v in tree_sha(d).items():
        base = os.path.basename(rel)
        if rel.startswith('attempt_') or base.startswith('cut_') or (base.startswith('run_') and base.endswith('.sh')):
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
    # 10-30 (KG50R-F02): 러너를 실제로 돌리므로 가짜 mpirun · 아무것도 안 하는 conda · 빈 ~/.bashrc (실제 헬퍼 러너의 환경 줄 꼴)
    for name, body in (('sbatch', STUB_SBATCH), ('sacct', STUB_SACCT), ('squeue', STUB_SQUEUE), ('sleep', '#!/bin/sh\nexit 0\n'),
                       ('mpirun', STUB_MPIRUN), ('conda', '#!/bin/sh\nexit 0\n')):
        p = os.path.join(stub, name)
        with open(p, 'w') as f:
            f.write(body)
        os.chmod(p, 0o755)
    open(os.path.join(home, '.bashrc'), 'w').close()
    helper = os.path.join(home, 'dem_test', 'dem_restart.py')
    with open(helper, 'w') as f:
        f.write(fake)
    cap = os.path.join(tmp, 'capture.txt')
    open(cap, 'w').close()
    return dict(tmp=tmp, L=L, home=home, stub=stub, S=S, cap=cap, helper=helper)


def snap_reports(L):
    return {p: (os.stat(p).st_mtime_ns, os.stat(p).st_size) for p in glob.glob(os.path.join(L, 'resume_%s_*.md' % SFX))}


def mp_records(path):
    # 10-30 (KG50R-F02): 가짜 mpirun 기록 → [{kind · job · cwd · args · in_sha}] (begin <종류> <job> · cwd · arg … · in_sha256 · end)
    out, cur = [], None
    if not os.path.isfile(path):
        return out
    with open(path, encoding='utf-8', errors='replace') as f:
        lines = f.read().split('\n')
    for l in lines:
        if l.startswith('begin '):
            k = l.split(' ')
            cur = dict(kind=k[1], job=k[2] if len(k) > 2 else '', cwd=None, args=[], in_sha=None)
        elif cur is None:
            continue
        elif l.startswith('cwd '):
            cur['cwd'] = l[4:]
        elif l.startswith('arg '):
            cur['args'].append(l[4:])
        elif l.startswith('in_sha256 '):
            cur['in_sha'] = l[10:]
        elif l == 'end':
            out.append(cur)
            cur = None
    return out


def invoke(ctx, script, res_text, trial_text, sacct='COMPLETED|0:0', sacct_rc=0, squeue='', squeue_rc=0, squeue2=None,
           squeue_rc2=0, extra=(), mode='settling', ckpt=CKPT, approve='auto', suf=SUF, env_more=None, cases=None, root=None):
    # 한 번 호출 — 이 호출에서 생긴 sbatch 호출 · 보고 · stdout · 작업 폴더 상태만 돌려준다
    # approve: 'auto' = 새 판 · -T 없음이면 실제 sha256 둘 (-A 이 스크립트 · -H 가짜 dem_restart.py) · None = 안 줌 ·
    #   'badA' · 'badH' = 하나만 틀린 값 · squeue2 = 둘째 squeue 호출부터 (본 제출 직전 다시 조회) 의 출력
    # 10-30 (KG50R-F02): root = -r 에 줄 경로 (기본 루트 L · RB 묶음의 별칭 링크) · env_more 값의 {L} = 루트 · mp = 이 호출의 가짜 mpirun 기록
    #   10-30 (사전 공격): env_more 값의 {TMP} = 이 루트의 임시 폴더 · 넘겨받은 환경의 BASH_ENV · ENV · BASH_FUNC_* (내보낸 함수) · 새 고리 변수는 지운다
    tmp, L, cap = ctx['tmp'], ctx['L'], ctx['cap']
    res = os.path.join(tmp, 'res.liggghts')
    with open(res, 'w', newline='') as f:
        f.write(res_text)
    tl = ''
    if trial_text is not None:
        tl = os.path.join(tmp, 'trial.out')
        with open(tl, 'w') as f:
            f.write(trial_text)
    mprec = cap + '.mp'
    env = dict(os.environ, HOME=ctx['home'], PATH=ctx['stub'] + ':' + os.environ['PATH'], USER='tester', CAPTURE=cap,
               FAKE_SACCT=sacct, FAKE_SACCT_RC=str(sacct_rc), FAKE_SQUEUE=squeue, FAKE_SQUEUE_RC=str(squeue_rc),
               FAKE_TRIAL_LOG=tl, FAKE_RES=res, FAKE_CKPT=ckpt, FAKE_MODE=mode, FAKE_MPIRUN_REC=mprec)
    for x in ('FAKE_SQUEUE_SECOND', 'FAKE_SQUEUE_2', 'FAKE_SQUEUE_RC_2', 'FAKE_SBATCH_TRIAL_EMPTY', 'FAKE_SBATCH_TRIAL_TEXT',
              'FAKE_TOUCH_HELPER', 'FAKE_DEM_FAIL', 'FAKE_EDIT_AFTER_TRIAL', 'FAKE_SBATCH_MAIN_TEXT', 'FAKE_SBATCH_MAIN_SUFFIX',
              'FAKE_RM_MODE', 'FAKE_RUNNER', 'FAKE_EDIT_GLOB', 'FAKE_DROP_LAST_GLOB', 'SLURM_JOB_ID', 'FAKE_JOB_KIND',
              'FAKE_PRE_SPOOL', 'FAKE_PRE_TRIAL', 'FAKE_POST_TRIAL', 'FAKE_PRE_MAIN', 'FAKE_POST_MAIN', 'BASH_ENV', 'ENV'):
        env.pop(x, None)
    for x in [k for k in env if k.startswith('BASH_FUNC_')]:
        env.pop(x)
    if squeue2 is not None:
        env.update(FAKE_SQUEUE_SECOND='1', FAKE_SQUEUE_2=squeue2, FAKE_SQUEUE_RC_2=str(squeue_rc2))
    env.update(dict((k, v.replace('{helper}', ctx['helper']).replace('{L}', L).replace('{TMP}', tmp)) for k, v in (env_more or {}).items()))
    for p in (cap + '.sq', mprec):
        if os.path.exists(p):
            os.remove(p)
    args = ['bash', script, '-n', str(NP), '-s', suf, '-r', L if root is None else root] + list(extra)
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
                s_same=s_before == s_after, w_exists=os.path.isdir(W), mp=mp_records(mprec))


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


# ═══ RB: 러너 결속 (10-30 KG50R-F02 · Codex KG50RF-02 P1 · 1저자 Q2 "권고대로") ═══
#   검사한 덱 ↔ 잡이 실제로 읽는 덱.  헬퍼 러너 (dem_restart.py 산출) 를 줄마다 엄격 대조 — 받는 꼴 밖이면 시험 전 거부 (sbatch 0 회) ·
#   통과면 본 · 시험 러너 = 도구 틀 (cd "작업 폴더 실제 경로" · -in "검사한 덱 절대 경로" · 실행 줄 하나 · LMP_IDENTITY 기록 줄) ·
#   실행 입력 영수증 다섯 (재개 덱 · 러너 · 시험 덱 · 시험 러너 · 체크포인트) + 영수증 파일 자체 (이 호출 메모리 sha256) 를 본 제출 바로 전 다시.
#   가짜 sbatch 가 제출된 러너를 실제로 돌리고 가짜 mpirun 이 cwd · 인자 · -in sha256 을 적는다 (실제 LIGGGHTS · SLURM 0).
#   ibb 꼴 (-r /home/yonghoon/dem_test · 헬퍼 cd /lustre/home/…) = 루트 별칭 링크.  Codex 반례 폴더 (independent/launch/) 는 읽기만 — 같은 꼴을 여기서 만든다.
CS = '%s_%s' % (C, SFX)
D2RUN = os.path.join(ROOT, 'docs/data/kg50_resume_tests_20261027/d2_main_1028_0942/run_kg50_d2_b50_r4.sh')
#   10-30 (사전 공격 PA-01 · 02 · 08 · 09): 틀 = cd "…" || exit 1 · 잡 시작 때 덱 · 체크포인트 sha256 (ds · ks) · 신원 줄 하나 (lmp_mpi = 기록만 ·
#     덱 = 시험 로그에서 G0 관문 · 체크포인트 = 기록만) · 검사한 sha256 과 다르면 LMP_IDENTITY_MISMATCH 한 줄 + exit 1 (mpirun 안 함) · command mpirun
RB_DS = 'ds=$(sha256sum 2>/dev/null < "%s" | cut -c1-64); ks=$(sha256sum 2>/dev/null < "%s" | cut -c1-64)'
RB_IDENT = ('echo "LMP_IDENTITY (10-30 KG50R-F02): lmp_mpi=$(command -v lmp_mpi || echo none) '
            'sha256=$(sha256sum 2>/dev/null < "$(command -v lmp_mpi)" | cut -c1-64) deck=%s sha256=$ds checkpoint=%s sha256=$ks"')
RB_CHECK = ('[ "$ds" = "%s" ] && [ "$ks" = "%s" ] || { echo "LMP_IDENTITY_MISMATCH (10-30 KG50R-F02): deck %s sha256 $ds (checked %s) '
            'checkpoint %s sha256 $ks (checked %s) - mpirun not started"; exit 1; }')
RB_ID_PRE = 'LMP_IDENTITY (10-30 KG50R-F02): lmp_mpi='


def sha(b):
    # 10-30 (사전 공격 PA-10): None (파일 없음) = 실제 sha256 과 같을 수 없는 표지 — 예전 = TypeError 로 RB 묶음 전체가 죽어 실패 줄이 안 남았다
    return hashlib.sha256(b).hexdigest() if b is not None else '<없음>'


def rb_expect(name, wr, sb, env, trial, dsha, ksha):
    """시험 쪽에서 따로 쓴 기대 러너 바이트 — 도구 틀과 같아야.  name = <C>_<SFX>[t] · sb = (qos, partition, time) · env = 환경 줄 (순서 그대로) ·
    dsha · ksha = 검사한 덱 (본 = 재개 덱 · 시험 = 시험 덱) · 체크포인트 sha256."""
    qos, part, tm = sb
    deck, ckp = '%s/input_%s.liggghts' % (wr, name), '%s/%s' % (wr, CKPT)
    out = ['#!/bin/bash', '#SBATCH --job-name=' + name, '#SBATCH --output=logs/output_%s_%%j.out' % name]
    if qos:
        out.append('#SBATCH --qos=' + qos)
    if part:
        out.append('#SBATCH --partition=' + part)
    out += ['#SBATCH -n %d' % NP, '#SBATCH --time=' + ('01:00:00' if trial else tm)]
    if env:
        out += [''] + list(env)
    out += ['', 'cd "%s" || exit 1' % wr, RB_DS % (deck, ckp), RB_IDENT % (deck, ckp), RB_CHECK % (dsha, ksha, deck, dsha, ckp, ksha),
            'command mpirun --oversubscribe --bind-to none -np %d lmp_mpi -in "%s"' % (NP, deck)]
    return ('\n'.join(out) + '\n').encode()


def runnerck_code(script):
    """도구 안 runnerck 파이썬 (heredoc 그대로) — RBU 직접 호출용 · 못 찾으면 None."""
    with open(script, encoding='utf-8') as f:
        src = f.read()
    head = "runnerck(){ python3 -I - \"$@\" <<'PY'\n"
    if head not in src:
        return None
    a = src.index(head) + len(head)
    return src[a:src.index('\nPY\n}', a)] + '\n'


def group_rb(script, chk, grp):
    grp('RB')
    good = res_variant('good')
    ok_log = trial_log('ok')
    nd, nt, rm, rt = 'input_%s.liggghts' % CS, 'input_%st.liggghts' % CS, 'run_%s.sh' % CS, 'run_%st.sh' % CS
    F02 = 'KG50R-F02'
    g_deck = with_tmpl(good)          # 도구가 만든 재개 덱 (템플릿 재선언 뒤) = 정적 대조가 읽는 덱
    g_trial = subprocess.run(['awk', '-v', 't=2000', OLD_CUT], input=g_deck.encode(), stdout=subprocess.PIPE).stdout   # 시험 덱 (G5 와 같은 절단)
    assert g_deck.count('run 180000\n') == 1 and g_trial.endswith(b'\nrun 2000\n')
    VEL = 'velocity all set 1.0 0.0 0.0\n'
    bak_main = g_deck.replace('run 180000\n', 'run 180000\n' + VEL).encode()     # Codex: 첫 긴 run 뒤 물리 명령 하나 (시험 구간 밖)
    bak_trial2 = g_trial.replace(b'\nrun 2000\n', ('\n' + VEL + 'run 2000\n').encode())

    def rb(runner=None, more_decks=(), extra=(), env_more=None, alias=None, real_name=None, prep=None):
        # alias 'r' = -r 루트 별칭 링크 · 헬퍼 cd = 실제 경로 (ibb: -r /home/yonghoon/dem_test · cd /lustre/home/…) · 'cd' = -r 실제 루트 ·
        #   러너 글의 {ALIAS} = 별칭 링크 · real_name = 실제 루트 폴더 이름 (ctx 루트 L 은 그 폴더를 가리키는 링크가 된다)
        #   10-30 (사전 공격): prep(ctx) = 호출 전 루트 손질 · extra 의 {TMP} = 임시 폴더 · tmp_files = 호출 뒤 임시 폴더 목록 · mlog = 본 잡 로그
        ctx = make_root(more_decks=more_decks)
        try:
            tmp, L = ctx['tmp'], ctx['L']
            if real_name:
                real = os.path.join(tmp, real_name)
                os.rename(L, real)
                os.symlink(real, L)
            al = os.path.join(tmp, 'alias')
            if alias:
                os.symlink(L, al)
            em = dict(env_more or {})
            if runner is not None:
                p = os.path.join(tmp, 'runner.tmpl')
                data = runner if isinstance(runner, bytes) else runner.encode()
                with open(p, 'wb') as f:
                    f.write(data.replace(b'{ALIAS}', al.encode()))
                em['FAKE_RUNNER'] = p
            if prep:
                prep(ctx)
            r = invoke(ctx, script, good, ok_log, extra=tuple(x.replace('{TMP}', tmp) for x in extra), env_more=em,
                       root=al if alias == 'r' else None)
            r['tmp_files'] = sorted(os.listdir(tmp))
            if not r['rep']:      # -x · -n 으로 접미사가 바뀐 장면 — 보고 이름 resume_<접미사>_* (새 루트라 하나뿐)
                reps = sorted(glob.glob(os.path.join(L, 'resume_*.md')))
                r['rep'] = open(reps[-1], encoding='utf-8', errors='replace').read() if reps else ''
            W = os.path.join(L, C)
            r['wr'] = os.path.realpath(W)
            r['files'] = {}
            for n in (nd, nt, rm, rt):
                q = os.path.join(W, n)
                r['files'][n] = open(q, 'rb').read() if os.path.isfile(q) else None
            q = os.path.join(L, 'logs', 'output_%st_7001.out' % CS)
            r['tlog'] = open(q, encoding='utf-8', errors='replace').read() if os.path.isfile(q) else ''
            q = os.path.join(L, 'logs', 'output_%s_9001.out' % CS)
            r['mlog'] = open(q, encoding='utf-8', errors='replace').read() if os.path.isfile(q) else ''
            q = os.path.join(W, CKPT)
            r['ck_sha'] = sha256f(q) if os.path.isfile(q) else ''
            r['alias'] = al
            return r
        finally:
            shutil.rmtree(ctx['tmp'], ignore_errors=True)

    def ran(r):
        # 실패 기록 끝 (잘려도 남게) — 실제로 낸 sbatch · 돈 잡마다 cwd · -in · 읽은 바이트 sha256 앞 12 자 ↔ 검사한 덱 · 시험 덱
        hd, ht = (sha(r['files'][n])[:12] if r['files'].get(n) else '-' for n in (nd, nt))
        js = ['%s:%s cwd=%s -in=%s sha=%s' % (x['kind'], x['job'], x['cwd'], x['args'][-1] if x['args'] else '-', (x['in_sha'] or '-')[:12])
              for x in r['mp']]
        return ' ‖ sbatch=%s ‖ 돈 잡=%s ‖ 검사한 재개 덱 %s · 시험 덱 %s' % ([c.split(' ')[0] for c in r['calls']], js, hd, ht)

    STAGE = '단계: 정적 대조 · 시험 덱 · 러너 · 이유: 시험 제출 안 함 · 헬퍼 러너 엄격 대조 실패 (10-30 KG50R-F02'

    def neg(tag, r, phrase):
        # 거부 자리 = 정적 대조 · 시험 덱 · 러너 관문 (ng) — 실행 영수증 단계에서 우연히 막힌 것 (시험 러너를 안 써서) 과 가른다
        chk('RB%s → 시험 전 거부 · sbatch 0 회 (시험 · 본 없음 · mpirun 0) · %s 이유 [%s] · 보고 시험 전 거부 절 (러너 관문)' % (tag, F02, phrase),
            r['calls'] == [] and r['mp'] == [] and F02 in r['out'] and phrase in r['out']
            and ('## %s — 시험 전 거부' % C) in r['rep'] and STAGE in r['rep'] and phrase in r['rep'], r['out'][-500:] + r['rep'][-300:] + ran(r))

    def startrej(tag, r, phrase):
        # 10-30 (사전 공격 PA-06 · 07): -n · -x = 쓰기 전 (cd · 보고 · 작업 폴더 · sed 전) 시작 거부 — 종료 코드 1 · 아무것도 안 만듦
        chk('RB%s → 시작 거부 (종료 코드 1 · sbatch 0 · mpirun 0 · 보고 없음 · 작업 폴더 없음 · 멈춘 폴더 그대로) · 이유 [%s]' % (tag, phrase),
            r['rc'] == 1 and r['calls'] == [] and r['mp'] == [] and phrase in r['out'] and not r['rep'] and not r['w_exists'] and r['s_same'],
            'rc=%s w_exists=%s s_same=%s ' % (r['rc'], r['w_exists'], r['s_same']) + r['out'][-600:] + ran(r))

    # ── 음성: 받는 꼴 밖의 헬퍼 러너 = 시험 전 거부 (Codex KG50RF-02 반례 넷 + 같은 부류) ──
    B, MP, CD, T5 = RB_BASE, 'mpirun -np 1 lmp_mpi -in input_{CS}.liggghts\n', 'cd {W}\n', '#SBATCH --time=5-00:00:00\n'

    def sub(old, new):
        assert B.count(old) == 1, old
        return B.replace(old, new)
    bakrun = sub(MP, 'mpirun -np 1 lmp_mpi -in input_{CS}.liggghts.bak\n')
    bakmsg = 'MPI 실행 줄 -in [%s.bak] ≠ 검사한 재개 덱 [%s]' % (nd, nd)
    for tag, runner, decks, phrase in (
            ('1 Codex .bak — 본 러너 -in …%s.bak · 본 .bak 덱 = 첫 긴 run 뒤 velocity · 시험 .bak 덱 = 검사한 시험 덱과 바이트 같음' % nd,
             bakrun, ((nd + '.bak', bak_main), (nt + '.bak', g_trial)), bakmsg),
            ('2 .bak 가 시험 쪽에만 닿음 — 작업 폴더에 시험 .bak 덱만 (검사한 시험 덱과 다름 · 본 .bak 없음)', bakrun, ((nt + '.bak', bak_trial2),), bakmsg),
            ('3 cd = 멈춘 폴더 (작업 폴더 아님)', sub(CD, 'cd {ROOT}/%s.%s\n' % (C, SUF)), (), 'cd 실제 경로 ['),
            ('4 주석 속 정상 mpirun 줄 + 다른 실제 줄 (처음부터 덱 input_<C>.liggghts)',
             sub(MP, '# ' + MP + 'mpirun -np 1 lmp_mpi -in input_{C}.liggghts\n'), (), '주석 줄'),
            ('4b 주석 줄 하나 (나머지 정상)', sub(CD, '# resume runner\n' + CD), (), '주석 줄'),
            ('5 MPI 실행 줄 두 번 (같은 줄)', sub(MP, MP + MP), (), 'MPI 실행 줄이 두 번'),
            ('6 다른 명령 줄 (cp 처음부터 덱 → 재개 덱)', sub(MP, 'cp input_{C}.liggghts input_{CS}.liggghts\n' + MP), (), '허용 목록에 없는 명령 줄'),
            ('7a MPI 실행 줄 ; 이음', sub(MP, MP[:-1] + '; mpirun -np 1 lmp_mpi -in input_{C}.liggghts\n'), (), '셸 연결 · 치환 · 리디렉션 글자가 든 MPI 실행 줄'),
            ('7b MPI 실행 줄 && 이음', sub(MP, MP[:-1] + ' && cp input_{C}.liggghts input_{CS}.liggghts\n'), (), '셸 연결 · 치환 · 리디렉션 글자가 든 MPI 실행 줄'),
            ('8 cd 없음', sub(CD, ''), (), 'cd 줄 없음'),
            ('9 cd 두 번', sub(CD, CD + 'cd {ROOT}\n'), (), 'cd 가 두 번'),
            ('9b cd 두 번 (둘 다 작업 폴더)', sub(CD, CD + CD), (), 'cd 가 두 번'),
            ('25 MPI 실행 줄 없음', sub(MP, ''), (), 'MPI 실행 줄 없음'),
            ('26 NUL 바이트', B + '\x00\n', (), 'NUL 글자'),
            ('27 UTF-8 아닌 바이트', B.encode() + b'\xff\n', (), 'UTF-8 이 아님'),
            # 도구의 -n · -np 고침 (sed) 이 엄격 대조 전에 어긋남을 지우면 안 된다 — 예전 sed = '#SBATCH -n ' 로 시작하는 줄 전체 · 줄 어디든
            #   'mpirun … -np [숫자 0 개 이상]' 을 고쳐 아래 셋이 정상 꼴로 바뀌었다 (그 자리는 시도 폴더 원본에만 남았다)
            ('28 #SBATCH -n 줄에 다른 지시가 붙음 (-n 1 --nodes=2)', sub('#SBATCH -n 1\n', '#SBATCH -n 1 --nodes=2\n'), (), '#SBATCH -n 값'),
            ('29 MPI 실행 줄 -np 숫자 없음', sub(MP, 'mpirun -np  lmp_mpi -in input_{CS}.liggghts\n'), (), 'MPI 실행 줄이 정해진 꼴이 아님'),
            ('30 #SBATCH -n 값이 숫자 아님', sub('#SBATCH -n 1\n', '#SBATCH -n x\n'), (), '#SBATCH -n 값'),
            ('10 -n 어긋남 (#SBATCH -n 1 뒤 --ntasks=8 · SLURM 은 뒤 지시 = 8 작업)', sub('#SBATCH -n 1\n', '#SBATCH -n 1\n#SBATCH --ntasks=8\n'), (),
             '작업 수 · 노드 지시'),
            ('11 같은 #SBATCH 키 두 번 (--time)', sub(T5, T5 + '#SBATCH --time=00:10:00\n'), (), '#SBATCH --time= 가 두 번'),
            ('12 #SBATCH 가 명령 줄 뒤 (SLURM 이 안 읽는 자리)', sub(T5, T5 + 'source ~/.bashrc\n#SBATCH --qos=cpu-60\n'), (), '#SBATCH 줄이 명령 줄 뒤'),
            ('13 환경 줄이 cd 뒤', sub(CD, CD + 'export OMP_NUM_THREADS=1\n'), (), '환경 줄이 cd 뒤'),
            ('14 cd 경로에 .. 마디 (실제 경로는 작업 폴더와 같음)', sub(CD, 'cd {W}/../{C}\n'), (), 'cd 경로가 안전한 절대 경로가 아님'),
            ('15 MPI 실행 줄이 cd 앞', sub(CD + MP, MP + CD), (), 'MPI 실행 줄이 cd 앞'),
            ('16 CRLF 줄 끝', B.replace('\n', '\r\n'), (), 'CR 글자'),
            ('17 --job-name 다름 (큐 검사 이름 밖)', sub('#SBATCH --job-name={CS}\n', '#SBATCH --job-name=other_job\n'), (), '#SBATCH --job-name= 값'),
            ('18 --output 다름 (도구가 읽는 시험 로그 자리 밖)', sub('#SBATCH --output=logs/output_{CS}_%j.out\n', '#SBATCH --output=out.log\n'), (),
             '#SBATCH --output= 값'),
            ('20 --qos 값에 공백', sub(T5, T5 + '#SBATCH --qos=cpu-60 bad\n'), (), '안전한 낱말이 아님'),
            ('22 첫 줄 #!/bin/sh', sub('#!/bin/bash\n', '#!/bin/sh\n'), (), '첫 줄이 #!/bin/bash 가 아님'),
            ('23 --time 없음', sub(T5, ''), (), '#SBATCH --time= 줄 없음'),
            # 10-30 (사전 공격 변이 R17): 꼭 있어야 하는 키 --output 이 빠짐 (예전 시험 = --time 만 봤다)
            ('33 --output 없음', sub('#SBATCH --output=logs/output_{CS}_%j.out\n', ''), (), '#SBATCH --output= 줄 없음'),
            # 10-30 (사전 공격): 쉼표로 나눈 낱낱이 선택 꼴 (--exclusive) — 낱말 글자만 보면 통과하던 꼴
            ('34 --qos 값 쉼표 뒤 낱낱이 선택 꼴 (cpu-60,--exclusive)', sub(T5, T5 + '#SBATCH --qos=cpu-60,--exclusive\n'), (), '안전한 낱말이 아님')):
        neg(tag, rb(runner, decks), phrase)
    neg('19 작업 폴더 실제 경로에 $ (루트 = 그 폴더를 가리키는 링크 · 헬퍼 cd = 링크 경로 · 러너 cd "…" 안에서 펼쳐질 글자)',
        rb(sub(CD, 'cd {ROOT}/{C}\n'), real_name='ro$x'), '작업 폴더 실제 경로 [')
    # 10-30 (사전 공격 PA-06 · 07): -n · -x 는 쓰기 전 시작 거부 (예전 = 루프 안 runnerck 가 거부 · 그 전에 -n 이 sed 에 · -x 가 경로에 들어갔다)
    startrej('21 NP 0 (-n 0)', rb(extra=('-n', '0')), '⛔ -n 0 — ')
    startrej('24 접미사에 $ (-x r5$x · 덱 · 러너 이름에 그대로)', rb(extra=('-x', 'r5$x')), '⛔ -x r5$x — ')

    # ── 10-30 (사전 공격 PA-04): 환경 줄 허용 목록 음성 — 셋 꼴 (source ~/.bashrc · conda activate <이름> · export <넷>_NUM_THREADS=1) 밖 ──
    #   (리뷰어 변이 E1 export 아무거나 · E2 conda activate 아무 글 · E3 source 아무 파일 이 살아남던 자리 · conda 이름 첫 글자 = A-Z a-z 0-9 _)
    for tag, line in (
            ('32a 환경 줄 뒤 다른 명령 (export … ; mpirun …)', 'export OMP_NUM_THREADS=1; mpirun -np 1 lmp_mpi -in input_{C}.liggghts'),
            ('32b export PATH', 'export PATH=/evil/bin'),
            ('32c export LD_PRELOAD', 'export LD_PRELOAD=/x/evil.so'),
            ('32d export OMP_NUM_THREADS=2 (값 = 1 만)', 'export OMP_NUM_THREADS=2'),
            ('32e source 다른 파일', 'source /tmp/x'),
            ('32f . ~/.bashrc (점 꼴)', '. ~/.bashrc'),
            ('32g conda activate 뒤 ; 이음', 'conda activate myenv; mpirun -np 1 lmp_mpi -in input_{C}.liggghts'),
            ('32h conda activate . (현재 폴더 = 제출 폴더 환경)', 'conda activate .'),
            ('32i conda activate ..', 'conda activate ..'),
            ('32j conda activate -h (선택 꼴)', 'conda activate -h')):
        neg(tag, rb(sub(CD, line + '\n' + CD)), '[%s] — 받는 꼴이 아닌 환경 줄' % line.replace('{C}', C))
    # 환경 줄 꼴이 아닌 다른 명령 줄의 리디렉션 = 셸 글자 문구 (변이 M16b — 그 문구 가지를 끄면 '허용 목록에 없는 명령 줄' 로 떨어진다)
    neg('37 cd 앞 다른 명령 줄에 리디렉션 (ls > /tmp/x)', rb(sub(CD, 'ls > /tmp/x\n' + CD)), '[ls > /tmp/x] — 셸 연결 · 치환 · 리디렉션 글자 (')

    # ── 양성: 실제 D2 헬퍼 러너 꼴 (ibb run_kg50_d2_b50_r4.sh) · -r = 루트 별칭 링크 · 헬퍼 cd = 실제 경로 (ibb /home → /lustre 꼴) ──
    with open(D2RUN, encoding='utf-8') as f:
        d2 = f.read()
    d2cd = 'cd /lustre/home/yonghoon/dem_test/kg50_d2_b50\n'
    assert d2.count(d2cd) == 1 and d2.count('kg50_d2_b50_r4') == 3 and d2.count('kg50_d2_b50') == 4
    d2t = d2.replace(d2cd, 'cd {W}\n').replace('kg50_d2_b50_r4', '{CS}')
    assert 'kg50_d2_b50' not in d2t
    d2env = ('source ~/.bashrc', 'conda activate myenv', 'export OMP_NUM_THREADS=1', 'export MKL_NUM_THREADS=1',
             'export OPENBLAS_NUM_THREADS=1', 'export NUMEXPR_NUM_THREADS=1')

    def idl(log):
        # 로그의 신원 줄 (^LMP_IDENTITY  — 끝에 빈칸 · _MISMATCH 줄은 아님)
        return [l for l in log.split('\n') if l.startswith('LMP_IDENTITY ')]

    def pos(tag, r, sbv, env, helper_bytes):
        # 10-30 (사전 공격 PA-10): 파일이 없거나 기록이 비어도 그 칸만 실패 (sha(None) · 빈 목록 · 예전 = TypeError 로 묶음 전체가 죽었다)
        wr = r['wr']
        mt = [x for x in r['mp'] if x['kind'] == 'trial']
        mm = [x for x in r['mp'] if x['kind'] == 'main']
        fd, ft, fm, fr = (r['files'].get(n) for n in (nd, nt, rm, rt))
        ck = r['ck_sha']
        ckp = '%s/%s' % (wr, CKPT)

        def want(name):
            return ['--oversubscribe', '--bind-to', 'none', '-np', str(NP), 'lmp_mpi', '-in', '%s/input_%s.liggghts' % (wr, name)]
        chk('RB%s a → 시험 1 · 본 1 · 러너가 실제로 돈 기록 둘 (시험 7001 → 본 9001)' % tag,
            r['ntrial'] == 1 and r['nmain'] == 1 and [(x['kind'], x['job']) for x in r['mp']] == [('trial', '7001'), ('main', '9001')],
            r['out'] + r['rep'] + ' mp=%s' % r['mp'])
        chk('RB%s b → 시험 잡: cwd = 작업 폴더 실제 경로 · 인자 = mpirun … -in <작업 폴더 실제 경로>/%s · 읽은 바이트 = 검사한 시험 덱' % (tag, nt),
            len(mt) == 1 and mt[0]['cwd'] == wr and mt[0]['args'] == want(CS + 't') and ft == g_trial and mt[0]['in_sha'] == sha(ft),
            'mp=%s wr=%s' % (mt, wr))
        chk('RB%s c → 본 잡: cwd = 작업 폴더 실제 경로 · 인자 = mpirun … -in <작업 폴더 실제 경로>/%s · 읽은 바이트 = 검사한 재개 덱' % (tag, nd),
            len(mm) == 1 and mm[0]['cwd'] == wr and mm[0]['args'] == want(CS) and fd == g_deck.encode() and mm[0]['in_sha'] == sha(fd),
            'mp=%s wr=%s' % (mm, wr))
        chk('RB%s d → 본 · 시험 러너 = 도구 틀 (시험 쪽에서 따로 쓴 기대 바이트와 같음 · 환경 줄 순서 · qos · partition · 시험 --time=01:00:00 · '
            'cd … || exit 1 · 잡 안 sha256 대조 · command mpirun)' % tag,
            fm == rb_expect(CS, wr, sbv, env, False, sha(fd), ck) and fr == rb_expect(CS + 't', wr, sbv, env, True, sha(ft), ck),
            '%r\n%r' % (fm, fr))
        rc_ = next((v for k, v in r['att'].items() if k.endswith('/main_inputs.sha256')), '')
        exp = ''.join('%s  %s\n' % (h, p) for h, p in ((sha(fd), wr + '/' + nd), (sha(fm), wr + '/' + rm), (sha(ft), wr + '/' + nt),
                                                       (sha(fr), wr + '/' + rt), (r['ck_sha'], wr + '/' + CKPT)))
        chk('RB%s e → 실행 입력 영수증 = 다섯 (재개 덱 · 러너 · 시험 덱 · 시험 러너 · 체크포인트) · 러너가 읽는 절대 경로 · 실제 sha256' % tag,
            rc_ == exp and len(r['ck_sha']) == 64, '%r\n%r' % (rc_, exp))
        orig = next((v for k, v in r['att'].items() if k.endswith('/helper_run_%s.sh.orig' % CS)), None)
        chk('RB%s f → 시도 폴더에 헬퍼 러너 원본 바이트 (-n · -np 고치기 전) · 보고에 러너 대조 통과 줄 · 잡 안 신원 줄' % tag,
            orig == helper_bytes.decode() and '헬퍼 러너 엄격 대조 통과' in r['rep'] and F02 in r['rep'] and 'LMP_IDENTITY' in r['rep'],
            '%r\n%s' % (orig, r['rep']))
        # lmp_mpi 칸 (잡 안 PATH 의 것 · 기록만) 은 기계마다 다르다 — 머리 · 꼬리 (덱 · 체크포인트) 로 대조
        want_t = ' deck=%s/%s sha256=%s checkpoint=%s sha256=%s' % (wr, nt, sha(ft), ckp, ck)
        want_m = ' deck=%s/%s sha256=%s checkpoint=%s sha256=%s' % (wr, nd, sha(fd), ckp, ck)

        def one(log, tail):
            ls = idl(log)
            return len(ls) == 1 and ls[0].startswith(RB_ID_PRE) and ls[0].endswith(tail) and 'LMP_IDENTITY_MISMATCH' not in log
        chk('RB%s g → 시험 로그 신원 줄 = 하나 · 덱 = 검사한 시험 덱 경로 · sha256 · 체크포인트 경로 · sha256 (잡 시작 때 읽은 바이트) · 대조 다름 줄 없음' % tag,
            one(r['tlog'], want_t), '%r ‖ %r' % (want_t, r['tlog'][:700]))
        chk('RB%s h → 보고에 G0 잡 안 덱 신원 관문 통과 줄 (10-30 KG50R-F02 · 덱 경로 · sha256 = 영수증의 시험 덱)' % tag,
            ('- G0 잡 안 덱 신원 (10-30 KG50R-F02 · 관문): 통과 — 같음 (덱 %s/%s sha256 %s' % (wr, nt, sha(ft))) in r['rep'],
            r['rep'][-1500:])
        chk('RB%s i → 본 잡 로그 신원 줄 = 하나 · 덱 = 검사한 재개 덱 경로 · sha256 · 대조 다름 줄 없음 (도구는 본 잡 출력을 안 읽는다 — 잡 로그에만)' % tag,
            one(r['mlog'], want_m), '%r ‖ %r' % (want_m, r['mlog'][:700]))

    r = rb(d2t, alias='r')
    pos('P1 실제 D2 헬퍼 러너 꼴 · ibb 꼴 별칭 (-r 별칭 · cd 실제 경로)', r, ('cpu-60', 'cpu', '5-00:00:00'), d2env,
        d2t.replace('{W}', r['wr']).replace('{CS}', CS).encode())
    rp2 = sub(CD, 'cd {ALIAS}/{C}\n')
    r = rb(rp2, alias='cd')
    pos('P2 기본 헬퍼 러너 꼴 · 반대 별칭 (-r 실제 루트 · cd 별칭 경로)', r, (None, None, '5-00:00:00'), (),
        rp2.replace('{ALIAS}', r['alias']).replace('{CS}', CS).replace('{C}', C).encode())

    # ── 10-30 (사전 공격 PA-01 · 02): 잡이 실제로 읽는 바이트 — 영수증 뒤 · 잡 시작 전 (큐 대기) 바뀐 덱 · 체크포인트 · 신원 줄 관문 ──
    #   (리뷰어 장면 T_swap · swap_restore · main_toctou 그대로 + 체크포인트 · 신원 줄 개수 · 경로)
    WJ = '{L}/%s' % C
    VEL_T = "sed -i 's/^run 2000$/velocity all set 1.0 0.0 0.0\\nrun 2000/' %s/%s" % (WJ, nt)
    GI_F = '- G0 잡 안 덱 신원 (10-30 KG50R-F02 · 관문): 실패 — '
    G0_F = '- G0 시험 정상 종료: 실패'

    def nomp(r, kind):
        return [x for x in r['mp'] if x['kind'] == kind] == []
    r = rb(extra=('-T',), env_more={'FAKE_PRE_TRIAL': VEL_T})
    chk('RB40 PA-01 -T · 시험 덱이 영수증 뒤 · 시험 잡 시작 전에 바뀜 (되돌리지 않음) → 잡 안 sha256 대조가 mpirun 을 막음 · G0 실패 (잡 안 덱 신원 = '
        '영수증과 다름) · 시험만 통과 줄 · 본 제출 명령 없음',
        r['ntrial'] == 1 and r['nmain'] == 0 and nomp(r, 'trial') and 'LMP_IDENTITY_MISMATCH' in r['tlog'] and G0_F in r['rep']
        and (GI_F + '덱 sha256 [') in r['rep'] and '≠ 영수증의 시험 덱 sha256 [' in r['rep'] and '🧪 시험만' not in r['rep']
        and '본 제출 명령 없음' in r['rep'], r['rep'][-1200:] + ran(r))
    r = rb(env_more={'FAKE_PRE_TRIAL': 'cp %s/%s {TMP}/keep_t.bin && %s' % (WJ, nt, VEL_T), 'FAKE_POST_TRIAL': 'cp {TMP}/keep_t.bin %s/%s' % (WJ, nt)})
    chk('RB41 PA-01 시험 덱이 시험 잡 동안만 바뀌고 잡 뒤 되돌아옴 (본 제출 직전 영수증 대조는 원래 바이트를 본다) → 잡 안 대조가 mpirun 을 막음 · '
        'G0 실패 (잡 안 덱 신원 다름) · 본 제출 0',
        r['ntrial'] == 1 and r['nmain'] == 0 and nomp(r, 'trial') and 'LMP_IDENTITY_MISMATCH' in r['tlog'] and G0_F in r['rep']
        and (GI_F + '덱 sha256 [') in r['rep'] and '⛔ 본 제출 안 함' in r['rep'], r['rep'][-1200:] + ran(r))
    r = rb(env_more={'FAKE_PRE_TRIAL': 'cp %s/%s {TMP}/keep_k.bin && printf x >> %s/%s' % (WJ, CKPT, WJ, CKPT),
                     'FAKE_POST_TRIAL': 'cp {TMP}/keep_k.bin %s/%s' % (WJ, CKPT)})
    chk('RB42 PA-02 체크포인트가 시험 잡 동안만 바뀌고 되돌아옴 → 잡 안 sha256 대조가 mpirun 을 막음 · 보고에 그 줄 · G0 실패 · 본 제출 0 '
        '(신원 줄 관문 = 덱만 · 체크포인트 = 잡 안 대조)',
        r['ntrial'] == 1 and r['nmain'] == 0 and nomp(r, 'trial') and 'LMP_IDENTITY_MISMATCH' in r['tlog']
        and '- ⛔ 잡 안 sha256 대조 다름 — mpirun 안 함 (10-30 KG50R-F02): LMP_IDENTITY_MISMATCH' in r['rep'] and G0_F in r['rep']
        and '⛔ 본 제출 안 함' in r['rep'], r['rep'][-1200:] + ran(r))
    r = rb(env_more={'FAKE_PRE_MAIN': "printf 'velocity all set 1.0 0.0 0.0\\n' >> %s/%s" % (WJ, nd)})
    chk('RB43 PA-02 본 제출 직전 대조 · 본 sbatch 뒤 · 본 잡 시작 전 (큐 대기) 재개 덱이 바뀜 → 본 잡 안 sha256 대조가 mpirun 을 막음 '
        '(도구는 본 잡 출력을 읽지 않는다 — 본 잡 로그에 LMP_IDENTITY_MISMATCH)',
        r['ntrial'] == 1 and r['nmain'] == 1 and not nomp(r, 'trial') and nomp(r, 'main') and 'LMP_IDENTITY_MISMATCH' in r['mlog'],
        r['mlog'][-600:] + ran(r))
    r = rb(extra=('-T',), env_more={'FAKE_PRE_SPOOL': '''[ "$2" = trial ] && sed -i '/^echo "LMP_IDENTITY/p' "$1"'''})
    mt = [x for x in r['mp'] if x['kind'] == 'trial']
    chk('RB44 PA-01 -T · 시험 러너가 sbatch 가 읽기 전에 바뀜 (신원 줄 두 번 · 덱 바이트는 그대로 · mpirun 은 돎) → G0 실패 (신원 줄 2 개) · 시험만 통과 줄 없음',
        r['ntrial'] == 1 and r['nmain'] == 0 and len(mt) == 1 and mt[0]['in_sha'] == sha(r['files'].get(nt)) and len(idl(r['tlog'])) == 2
        and G0_F in r['rep'] and (GI_F + 'LMP_IDENTITY 줄 2 개') in r['rep'] and '🧪 시험만' not in r['rep'], r['rep'][-1200:] + ran(r))
    r = rb(extra=('-T',), env_more={'FAKE_PRE_SPOOL': r'''[ "$2" = trial ] && sed -i 's#\(deck=[^ ]*\)t\.liggghts #\1.liggghts #' "$1"'''})
    mt = [x for x in r['mp'] if x['kind'] == 'trial']
    chk('RB44b PA-01 -T · 시험 러너 신원 줄의 덱 경로만 재개 덱으로 바뀜 (sha256 · mpirun 은 시험 덱 그대로) → G0 실패 (덱 경로 ≠ 검사한 시험 덱) · 시험만 통과 줄 없음',
        r['ntrial'] == 1 and r['nmain'] == 0 and len(mt) == 1 and mt[0]['in_sha'] == sha(r['files'].get(nt)) and G0_F in r['rep']
        and (GI_F + '덱 경로 [%s/%s] ≠ 검사한 시험 덱 [%s/%s]' % (r['wr'], nd, r['wr'], nt)) in r['rep'] and '🧪 시험만' not in r['rep'],
        r['rep'][-1200:] + ran(r))

    # ── 10-30 (사전 공격 PA-09 · 08): 제출 환경 (sbatch 기본 = 환경 전부 넘김) 의 BASH_ENV — mpirun 함수 · cd 실패 흉내 ──
    #   (내보낸 함수 BASH_FUNC_mpirun%% 는 이 가짜 sbatch (dash) 가 넘기지 못해 여기서 못 본다 — bash 의 함수 찾기는 출처와 같다 · README)
    def benv(ctx):
        other = os.path.join(ctx['tmp'], 'other.liggghts')
        with open(other, 'w') as f:
            f.write('# not the checked deck\nrun 1\n')
        with open(os.path.join(ctx['tmp'], 'benv.sh'), 'w') as f:
            f.write('mpirun() { set -- "${@:1:$(($#-1))}" %s; command mpirun "$@"; }\n' % other)
    r = rb(env_more={'BASH_ENV': '{TMP}/benv.sh'}, prep=benv)
    mt, mm = ([x for x in r['mp'] if x['kind'] == k] for k in ('trial', 'main'))
    chk('RB45 PA-09 BASH_ENV 가 mpirun 함수를 정의 (마지막 인자를 다른 덱으로 바꿔 부름) → 러너 = command mpirun → 시험 · 본 잡 다 검사한 덱 경로 · 바이트',
        r['ntrial'] == 1 and r['nmain'] == 1 and len(mt) == 1 and len(mm) == 1
        and mt[0]['args'][-1:] == ['%s/%s' % (r['wr'], nt)] and mt[0]['in_sha'] == sha(r['files'].get(nt))
        and mm[0]['args'][-1:] == ['%s/%s' % (r['wr'], nd)] and mm[0]['in_sha'] == sha(r['files'].get(nd)), r['rep'][-600:] + ran(r))

    def cdenv(ctx):
        with open(os.path.join(ctx['tmp'], 'cdenv.sh'), 'w') as f:
            f.write('if [ -n "$SLURM_JOB_ID" ]; then cd() { return 1; }; fi\n')
    r = rb(env_more={'BASH_ENV': '{TMP}/cdenv.sh'}, prep=cdenv)
    chk('RB46 PA-08 잡 안 cd 실패 (잡에서만 cd 가 1 을 돌려주는 BASH_ENV) → cd "…" || exit 1 → mpirun 안 돎 (시험 · 본) · G0 실패 · 본 제출 0',
        r['ntrial'] == 1 and r['nmain'] == 0 and r['mp'] == [] and G0_F in r['rep'], r['rep'][-900:] + ran(r))

    # ── 10-30 (사전 공격 PA-05): 실제 경로에 ERROR (신원 줄이 덱 · 체크포인트 경로를 적는다) — 예전 = ERROR 셈에 걸려 G0 · G1 실패 (회귀) ──
    r = rb(real_name='ERRORS_root')
    chk('RB47 PA-05 실제 루트 폴더 이름에 ERROR → ERROR 셈에서 신원 줄을 뺀다 → 시험 ERROR 0 · G0 · G1 통과 · 본 제출 1',
        r['ntrial'] == 1 and r['nmain'] == 1 and ' · ERROR 0\n' in r['rep'] and '- G0 시험 정상 종료: 통과' in r['rep']
        and '1e-6): 통과' in r['rep'] and 'ERRORS_root' in r['wr'], r['rep'][-900:] + ran(r))

    # ── 10-30 (사전 공격 PA-03): 멈춘 폴더가 심볼릭 링크 — cp -a 가 링크를 그대로 복사해 작업 폴더 = 원 런 폴더 (원인은 F02 전부터) ──
    def slink(ctx):
        S = ctx['S']
        real = os.path.join(ctx['tmp'], 'elsewhere', os.path.basename(S))
        os.makedirs(os.path.dirname(real))
        os.rename(S, real)
        os.symlink(real, S)
    r = rb(prep=slink)
    chk('RB48 PA-03 멈춘 폴더 = 다른 곳 실제 폴더를 가리키는 링크 → 복사 · 쓰기 전에 거부 (단계 멈춘 폴더) · sbatch 0 · 원 런 폴더 그대로 · 작업 폴더 안 만듦',
        r['calls'] == [] and r['mp'] == [] and r['s_same'] and not r['w_exists'] and '심볼릭 링크' in r['out']
        and ('## %s — 시험 전 거부' % C) in r['rep'] and '단계: 멈춘 폴더 · ' in r['rep'],
        's_same=%s w_exists=%s ' % (r['s_same'], r['w_exists']) + r['out'][-700:] + ran(r))

    # ── 10-30 (사전 공격 PA-07 · 06): -n 이 sed 프로그램에 · -x 가 덱 · 러너 경로에 들어가기 전 시작 거부 ──
    #   (리뷰어 attack.py np_sed 의 꼬리 ';s/^/' 는 e 명령의 sh 가 구문 오류로 멈춰 표지를 못 만든다 — 실측 · 꼬리 ' #' (나머지 = sh 주석) 은 만든다)
    r = rb(extra=('-x', SFX, '-n', '56/;e touch {TMP}/SED_E_RAN #'))
    startrej('49 PA-07 -n 에 sed 명령 (56/;e touch … #) — 리뷰어 np_sed · sed_e_probe', r, '⛔ -n 56/;e touch ')
    chk('RB49b PA-07 → GNU sed e 명령이 안 돎 (표지 파일 SED_E_RAN 없음)', 'SED_E_RAN' not in r['tmp_files'], repr(r['tmp_files']))
    evil = g_deck.replace('run 180000\n', 'run 180000\n' + VEL).encode()

    def sfx_prep(ctx):
        # 리뷰어 sfx_slash 장면 그대로: -x r56/x → 검사 = $W/input_<C>_r56/x.liggghts · 러너 -in = <작업 폴더>/x.liggghts (다른 파일)
        S, L = ctx['S'], ctx['L']
        for dname in ('input_%s_r56' % C, 'run_%s_r56' % C, 'plan_r56', 'tmpl_r56', 'tp_r56', 'fixrun_r56', 'cut_r56',
                      'deckcheck_r56', 'job_r56', 'mode_r56', 'attempt_r56'):
            os.makedirs(os.path.join(S, dname))
        for n, body in (('x.liggghts', evil), ('xt.liggghts', g_trial), ('x.sh', b'#!/bin/bash\n'), ('xt.sh', b'#!/bin/bash\n')):
            with open(os.path.join(S, n), 'wb') as f:
                f.write(body)
        os.makedirs(os.path.join(L, 'logs', 'output_%s_r56' % C))
        os.makedirs(os.path.join(L, 'resume_r56'))
    r = rb(RB_BASE.replace('-in input_{CS}.liggghts', '-in x.liggghts'), extra=('-x', 'r56/x'), prep=sfx_prep)
    startrej('50 PA-06 -x r56/x (덱 경로 ↔ 러너 -in 이름이 갈린다 · 리뷰어 sfx_slash 준비 그대로)', r, '⛔ -x r56/x — ')

    # ── 10-30 (사전 공격 변이 R7 · R8): runnerck 쓰기 오류 (종료 코드 2) = 거부 · 멈춘 폴더에서 온 옛 시험 러너는 대조 전에 지운다 ──
    def tr_dir(ctx):
        os.makedirs(os.path.join(ctx['S'], rt))
    r = rb(prep=tr_dir)
    STAGE2 = '단계: 정적 대조 · 시험 덱 · 러너 · 이유: 시험 제출 안 함 · 헬퍼 러너 대조 · 러너 쓰기 오류 (10-30 KG50R-F02'
    chk('RB35 시험 러너 자리에 폴더 (멈춘 폴더에서 복사됨 → runnerck 가 시험 러너를 못 씀 · 종료 코드 2) → 러너 관문에서 거부 (실행 영수증 단계 아님) · sbatch 0 · '
        '작업 폴더에 러너 임시 파일 (.tmp) 안 남음',
        r['calls'] == [] and r['mp'] == [] and '러너 쓰기 오류' in r['out'] and STAGE2 in r['rep'] and not any('.tmp' in k for k in r['w_files']),
        r['out'][-500:] + r['rep'][-400:] + ran(r) + ' w_files=%s' % sorted(r['w_files'])[:40])

    def tr_stale(ctx):
        with open(os.path.join(ctx['S'], rt), 'w') as f:
            f.write('#!/bin/bash\n# 옛 시도의 시험 러너\nmpirun -np 1 lmp_mpi -in input_%s.liggghts\n' % C)
    r = rb(sub(CD, ''), prep=tr_stale)
    neg('36 멈춘 폴더에서 온 옛 시험 러너 + 거부되는 헬퍼 러너 (cd 없음)', r, 'cd 줄 없음')
    chk('RB36b → 작업 폴더에 옛 시험 러너가 안 남음 (대조 전에 지운다 · 이번 호출이 쓰지 않은 시험 러너를 남기지 않는다)', r['files'].get(rt) is None,
        repr(r['files'].get(rt))[:300])

    # ── 10-30 (사전 공격 변이 R3 · 체크포인트 인자): runnerck 직접 — 인자 계약 (도구 흐름에서는 WR = cd -P 실제 경로라 안 갈린다) ──
    code = runnerck_code(script)
    ut = tempfile.mkdtemp(prefix='rcku_')
    try:
        uw = os.path.join(ut, 'root', C)
        os.makedirs(os.path.join(uw, 'restart_' + C))
        uwr = os.path.realpath(uw)
        ud, utd, uck = (os.path.join(uw, n) for n in (nd, nt, CKPT))
        for p, body in ((ud, g_deck.encode()), (utd, g_trial), (uck, b'\x00' * 64)):
            with open(p, 'wb') as f:
                f.write(body)
        urn = os.path.join(ut, 'helper.sh')
        with open(urn, 'w') as f:      # 도구가 -n · -np 를 고친 뒤 꼴 (runnerck 는 그 뒤에 불린다)
            f.write('#!/bin/bash\n#SBATCH --job-name=%s\n#SBATCH --output=logs/output_%s_%%j.out\n#SBATCH -n %d\n#SBATCH --time=5-00:00:00\n'
                    'cd %s\nmpirun --oversubscribe --bind-to none -np %d lmp_mpi -in %s\n' % (CS, CS, NP, uwr, NP, nd))
        uom, uot = os.path.join(uw, rm), os.path.join(uw, rt)

        def rck(wr=uwr, ckp=uck, np_=str(NP), deck=ud):
            for p in (uom, uot):
                if os.path.exists(p):
                    os.remove(p)
            if code is None:
                return None, '도구 안에 runnerck 없음'
            p = subprocess.run(['python3', '-I', '-', urn, C, SFX, np_, uw, wr, deck, utd, uom, uot, ckp], input=code.encode(),
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
            return p.returncode, p.stdout.decode('utf-8', 'replace')
        rc, out = rck()
        chk('RBU1 runnerck 직접 · 정상 인자 11 (헬퍼 러너 · C · SFX · NP · 작업 폴더 · 실제 경로 · 재개 덱 · 시험 덱 · 두 러너 · 체크포인트) → 0 · 두 러너 씀',
            rc == 0 and os.path.isfile(uom) and os.path.isfile(uot), '%s %s' % (rc, out))
        rc, out = rck(wr=ut)
        chk('RBU2 runnerck 직접 · 실제 경로 인자 ≠ 작업 폴더의 실제 경로 → 1 · 러너 안 씀', rc == 1 and '실제 경로를 못 얻음' in out
            and not os.path.exists(uom) and not os.path.exists(uot), '%s %s' % (rc, out))
        rc, out = rck(ckp=os.path.join(uw, 'restart_' + C, 'none.bin'))
        chk('RBU3 runnerck 직접 · 체크포인트 없음 → 1 · 러너 안 씀', rc == 1 and '체크포인트 [' in out and '못 읽음' in out
            and not os.path.exists(uom), '%s %s' % (rc, out))
        bad = os.path.join(uw, 'restart_' + C, 'c$x.bin')
        with open(bad, 'wb') as f:
            f.write(b'\x00')
        rc, out = rck(ckp=bad)
        chk('RBU4 runnerck 직접 · 체크포인트 경로에 $ (러너의 "…" 안에서 펼쳐질 글자) → 1 · 러너 안 씀', rc == 1 and '체크포인트 절대 경로 [' in out
            and not os.path.exists(uom), '%s %s' % (rc, out))
        # 도구 흐름에서는 시작 거부 (-n · -x · 케이스 이름 규칙) 가 먼저 막는 runnerck 의 겹 방어 둘 (변이 M23 · M26)
        rc, out = rck(np_='0')
        chk('RBU5 runnerck 직접 · NP 0 → 1 · 러너 안 씀 (도구 흐름은 -n 시작 거부가 먼저)', rc == 1 and 'NP [0]' in out and not os.path.exists(uom),
            '%s %s' % (rc, out))
        rc, out = rck(deck=os.path.join(uw, 'input_r$x.liggghts'))
        chk('RBU6 runnerck 직접 · 재개 덱 이름에 $ → 1 · 러너 안 씀 (도구 흐름은 -x · 케이스 이름 규칙이 먼저)', rc == 1 and '재개 덱 절대 경로 [' in out
            and not os.path.exists(uom), '%s %s' % (rc, out))
    finally:
        shutil.rmtree(ut, ignore_errors=True)

    # ── 영수증: 시험 뒤 다섯 실행 입력 중 하나 · 영수증 파일 자체가 바뀌면 본 제출 안 함 (시험은 낸다) ──
    TDP, TRP, CKP = '{L}/%s/%s' % (C, nt), '{L}/%s/%s' % (C, rt), '{L}/%s/%s' % (C, CKPT)
    RCG = '{L}/%s/attempt_*/main_inputs.sha256' % C
    #   10-30 (사전 공격 PA-02): 시험 덱 · 체크포인트를 잡 시작 전에 고치면 이제 잡 안 sha256 대조가 먼저 막는다 (RB41 · RB42) → R1 · R3 은
    #     잡 끝난 뒤 (FAKE_POST_TRIAL) 고쳐 본 제출 직전 영수증 대조를 따로 본다 · 러너 (R2) 는 사본이 돌므로 제출 때 고쳐도 잡과 무관
    for tag, em, phrase in (
            ('R1 시험 잡 뒤 시험 덱이 바뀜', {'FAKE_POST_TRIAL': 'echo "# 시험 잡 뒤 바뀜 (10-30 KG50R-F02)" >> ' + TDP}, nt + ': FAILED'),
            ('R2 시험 제출 뒤 시험 러너가 바뀜', {'FAKE_EDIT_AFTER_TRIAL': TRP}, rt + ': FAILED'),
            ('R3 시험 잡 뒤 체크포인트가 바뀜', {'FAKE_POST_TRIAL': 'printf x >> ' + CKP}, CKPT.split('/')[-1] + ': FAILED'),
            ('R4 시험 제출 뒤 영수증 파일 끝에 줄 하나 (sha256sum -c 는 그대로 통과하는 꼴)', {'FAKE_EDIT_GLOB': RCG}, '실행 입력 영수증'),
            ('R5 시험 제출 뒤 영수증 마지막 줄 (체크포인트) 지움 (sha256sum -c 는 남은 넷만 보고 통과하는 꼴)', {'FAKE_DROP_LAST_GLOB': RCG},
             '실행 입력 영수증')):
        r = rb(env_more=em)
        chk('RB%s → 시험 1 · 본 제출 0 · 보고에 그 사유 (%s · %s)' % (tag, F02, phrase),
            r['ntrial'] == 1 and r['nmain'] == 0 and '⛔ 본 제출 안 함' in r['rep'] and F02 in r['rep'] and phrase in r['rep'],
            r['rep'][-700:] + ran(r))


# ═══ VP: 10-30 (KG50R-F01 2 판 · 독립 사전 공격 R1–R8 · 1저자 "권고대로") — 정적 대조 (-C) 의 남은 구멍 ═══
#   R1 상태 표 키 = 치환 전 글자 (fix gx${n} 둘이 한 키 · unfix ${u} 가 아무것도 안 지움) · R2 본 덱 체크포인트 앞 run every · partition 안
#   상태 명령 · R3 줄 읽기 ↔ LIGGGHTS file()/parse() (#\r · & + NBSP · variab&↵le · 제어 글자 · 주석 밖 비 ASCII · 주석 따옴표 규칙) ·
#   R4 준비 구간 print file/append 로 쓴 파일을 읽음 · R5 write_restart 체크포인트 앞 label · jump · clear · python · R6 판 메시 file 이름
#   있는지 = 펼친 이름 · R7 펼친 글 크기 상한 (지수 폭발) · R8 group 그 자리 치환 값 대조 (변이 M16 이 살아남던 자리).
#   리뷰어 장면 (스크래치 f01rev/a0*.py · 덱) 은 같은 꼴을 여기서 만든다 (받은 D2 덱 · v3 50×50 · 합성 write_restart 덱).
F01P = 'KG50R-F01 · 사전 공격'


def run_deckcheck_limited(script, main_text, res_text, ckpt, s0, workdir_files=(), limit=60):
    """-C 를 새 세션으로 돌리고 limit 초 넘으면 프로세스 묶음 전체를 끝낸다 (R7 — 고치기 전 판은 몇 분 · 손자 python 이 남지 않게).
    → (종료 코드 · stdout · 걸린 초 · 시간 초과?)"""
    import signal
    import time
    tmp = tempfile.mkdtemp(prefix='rckvp7_')
    try:
        mp, rp = os.path.join(tmp, 'm.liggghts'), os.path.join(tmp, 'r.liggghts')
        for p, t in ((mp, main_text), (rp, res_text)):
            with open(p, 'w', encoding='utf-8', newline='') as f:
                f.write(t)
        wd = os.path.join(tmp, 'w')
        os.makedirs(wd)
        for n in workdir_files:
            open(os.path.join(wd, n), 'w').close()
        t0 = time.time()
        p = subprocess.Popen(['bash', script, '-C', mp, rp, ckpt, str(s0), wd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             start_new_session=True)
        try:
            out, _ = p.communicate(timeout=limit)
            return p.returncode, out.decode('utf-8', 'replace'), time.time() - t0, False
        except subprocess.TimeoutExpired:
            try:
                os.killpg(p.pid, signal.SIGKILL)
            except OSError:
                pass
            p.communicate()
            return -9, '', time.time() - t0, True
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def group_vp(script, chk, grp):
    grp('VP')
    tmp = tempfile.mkdtemp(prefix='rckvp_')
    try:
        D2D = os.path.join(ROOT, 'docs/data/kg50_resume_tests_20261027/d2_main_1028_0942')
        with open(os.path.join(D2D, 'input_kg50_d2_b50.liggghts'), encoding='utf-8') as f:
            d2m = f.read()
        with open(os.path.join(D2D, 'input_kg50_d2_b50_r4.liggghts'), encoding='utf-8') as f:
            d2r = f.read()
        D2K = ('restart_kg50_d2_b50/restart_settling_20001.bin', 20001)
        FG = 'fix gravi all gravity 98.1 vector 0.0 0.0 -1.0\n'
        GX = 'fix gx all gravity 98.1 vector 0.0 0.0 -1.0\n'
        GP = 'fix gravi all gravity ${g_probe} vector 0.0 0.0 -1.0\n'
        DMP = FG + 'fix damp all viscous 1.0e-5\n'
        INS1, NI = 'run 1\nunfix ins_mix\n', 'variable n_ins equal count(all)\n'
        PLATE = 'plate_kg50_d2_b50.stl'
        for t, n in ((FG, 1), (DMP, 1), (NI, 1), ('top_mesh all mesh/surface/stress file %s ' % PLATE, 1)):
            assert d2m.count(t) == n and d2r.count(t) == n, t
        assert d2m.count(INS1) == 1 and d2r.count(INS1) == 0 and d2m.count('fix ins_mix all insert/pack') == 1

        def d2(mrep, rrep, old=FG):
            return d2m.replace(old, mrep), d2r.replace(old, rrep)
        with open(MAIN50, encoding='utf-8') as f:
            t50 = f.read()
        r50 = res_after('good', MAIN50, C50, tmpl=True)
        CK50 = ('restart_%s/restart_after_settling.bin' % C50, 200001)
        AS50 = dict(mode='after_settling', orig_log=AS_LOG)
        FI = 'fix integr all nve/sphere\n'
        assert t50.count(FI) == 1 and r50.count(FI) == 1
        # 합성 write_restart 덱 (변수 없음 — 변수 표 (KG50R-F01 1 판) 가 못 보는 꼴 · 리뷰어 A7s · C1)
        SR = 'units si\nread_restart restart_after_settling.bin\n' + GX + FI + 'run 1\nrun 50\n'
        SK = ('restart_after_settling.bin', 100)

        def sm(pre, post=''):
            return 'units si\n' + pre + GX + post + FI + 'run 100\nwrite_restart restart_after_settling.bin\nrun 1\nrun 50\n'
        STL = ''.join('print "%s" %s w.stl screen no\n' % (t, 'file' if k == 0 else 'append') for k, t in enumerate(
            ('solid w', 'facet normal 0 0 -1', 'outer loop', 'vertex 0.0 0.0 ${pz}', 'vertex 0.05 0.05 ${pz}', 'vertex 0.05 0.0 ${pz}',
             'endloop', 'endfacet', 'endsolid w')))
        MF = 'fix wm all mesh/surface file w.stl type 1 scale 1.0\n'

        def chain(depth, vref):
            # R7: a_k = a_(k-1) + a_(k-1) — ${} (정의 때 치환 · 펼친 글이 매 단 두 배) · v_ (쓸 때 계산 · 펼치기가 매 단 두 갈래)
            c = 'variable a0 equal 1.0\n' + ''.join('variable a%d equal %s+%s\n' % ((k,) + (vref % (k - 1),) * 2) for k in range(1, depth + 1))
            return FG + c + 'fix gx all gravity ${a%d} vector 0.0 0.0 -1.0\n' % depth

        # (꼬리표 · R · (본 덱, 재개 덱) · (체크포인트, S0) · 작업 폴더 빈 파일 · 꼭 있어야 할 문제 줄 조각 (KG50R-F01 든 문제 줄 · 다 있어야) ·
        #   본 흐름 (-T) 도 돌릴 꾸밈 (None = -C 만))
        neg = [
            ('VP1a R1 본 덱 fix gx${n} 둘 (n 1 → 2 = gx1 · gx2) · 재개 덱 fix gx${n} 하나 (n 2) — 키가 치환 전 글자라 한 키로 접힘',
             d2(FG + 'variable n equal 1\nfix gx${n} all gravity 98.1 vector 0.0 0.0 -1.0\nvariable n equal 2\n'
                'fix gx${n} all gravity 98.1 vector 0.0 0.0 -1.0\n', FG + 'variable n equal 2\nfix gx${n} all gravity 98.1 vector 0.0 0.0 -1.0\n'),
             D2K, (), ['사전 공격 R1', '키 자리', 'gx${n}'], None),
            ('VP1b R1 본 덱 fix gx · variable u string gx · unfix ${u} · 재개 덱 fix gx 만 (unfix ${u} 가 아무것도 안 지움)',
             d2(FG + GX + 'variable u string gx\nunfix ${u}\n', FG + GX), D2K, (), ['사전 공격 R1', '키 자리', '${u}'], None),
            ('VP1c R1 본 덱 variable u string damp · unfix ${u} (생산 감쇠 fix 를 지움) · 재개 덱 그대로 (감쇠 있음)',
             (d2m.replace(DMP, DMP + 'variable u string damp\nunfix ${u}\n'), d2r), D2K, (), ['사전 공격 R1', '키 자리', 'unfix ${u}'], {}),
            ('VP1d R1 v3 after_settling — 본 덱 fix gx${n} 둘 · 재개 덱 하나',
             (t50.replace(FI, FI + 'variable n equal 1\nfix gx${n} all gravity 98.1 vector 0.0 0.0 -1.0\nvariable n equal 2\n'
                          'fix gx${n} all gravity 98.1 vector 0.0 0.0 -1.0\n'),
              r50.replace(FI, FI + 'variable n equal 2\nfix gx${n} all gravity 98.1 vector 0.0 0.0 -1.0\n')), CK50, (),
             ['사전 공격 R1', '키 자리', 'gx${n}'], None),
            ('VP1e R1 v3 after_settling — 본 덱 unfix ${u} (u = gx) · 재개 덱 fix gx 남김',
             (t50.replace(FI, FI + GX + 'variable u string gx\nunfix ${u}\n'), r50.replace(FI, FI + GX)), CK50, (),
             ['사전 공격 R1', '키 자리', '${u}'], None),
            ('VP1f R1 fix 스타일 자리 ${s} (s = insert/pack · 재삽입 판별이 치환 전 글자를 봄 · 두 덱 같은 글자)',
             d2(FG + 'variable s string insert/pack\nfix ins2 all ${s} seed 123457 distributiontemplate pdd_mix\n',
                FG + 'variable s string insert/pack\nfix ins2 all ${s} seed 123457 distributiontemplate pdd_mix\n'), D2K, (),
             ['사전 공격 R1', '키 자리', '${s}'], None),
            ('VP1g R1 region 이름 자리 ${r} (두 덱 같은 글자)',
             d2(FG + 'variable r string rb\nregion ${r} block 0 1 0 1 0 1 units box\n', FG + 'variable r string rb\nregion ${r} block 0 1 0 1 0 1 units box\n'),
             D2K, (), ['사전 공격 R1', '키 자리', '${r}'], None),
            ('VP1h R1 pair_coeff 형 자리 ${t} (두 덱 같은 글자)',
             d2(FG + 'variable t equal 1\npair_coeff ${t} ${t}\n', FG + 'variable t equal 1\npair_coeff ${t} ${t}\n'), D2K, (),
             ['사전 공격 R1', '키 자리', '${t}'], None),
            ('VP2a R2 본 덱 삽입 run 1 every 1 "fix gx …" (재개 덱에 gx 없음 · if 안 같은 명령은 이미 거부)',
             (d2m.replace(INS1, 'run 1 every 1 "%s"\nunfix ins_mix\n' % GX.strip()), d2r), D2K, (), ['사전 공격 R2', 'run every', 'fix gx'], {}),
            ('VP2b R2 본 덱 fix gy (삽입 앞) · 삽입 run 1 every 1 "unfix gy" · 재개 덱 fix gy 남김',
             (d2m.replace('fix ins_mix all insert/pack', 'fix gy all gravity 98.1 vector 0.0 0.0 -1.0\nfix ins_mix all insert/pack', 1)
              .replace(INS1, 'run 1 every 1 "unfix gy"\nunfix ins_mix\n'), d2r.replace(NI, 'fix gy all gravity 98.1 vector 0.0 0.0 -1.0\n' + NI)),
             D2K, (), ['사전 공격 R2', 'run every', 'unfix gy'], None),
            ('VP2c R2 본 덱 삽입 run 1 every 1 "timestep 2.0e-6" (재개 덱 timestep ${dt} = 1e-6)',
             (d2m.replace(INS1, 'run 1 every 1 "timestep 2.0e-6"\nunfix ins_mix\n'), d2r), D2K, (), ['사전 공격 R2', 'run every', 'timestep'], None),
            ('VP2d R2 본 덱 체크포인트 앞 partition yes 1 fix gx … (파티션 하나 = 실행)',
             (d2m.replace(INS1, INS1 + 'partition yes 1 ' + GX), d2r), D2K, (), ['사전 공격 R2', 'partition'], None),
            ('VP2e R2 본 덱 삽입 run 1 every 1 "jump SELF nowhere" (run every · partition 안 jump 도 거부 — restart 체크포인트 남은 step 셈이 못 봄)',
             (d2m.replace(INS1, 'run 1 every 1 "jump SELF nowhere"\nunfix ins_mix\n'), d2r), D2K, (), ['사전 공격 R2', 'run every', 'jump'], None),
            ('VP3a R3 재개 덱 "#\\rvariable g_probe equal 196.2" (LIGGGHTS = 주석 한 줄 · 예전 도구 = 정의) → 제어 글자 거부',
             (d2m.replace(FG, 'variable g_probe equal 98.1\nvariable g_probe equal 196.2\n' + GP + 'variable g_probe equal 98.1\n'),
              d2r.replace(FG, 'variable g_probe equal 98.1\n#\rvariable g_probe equal 196.2\n' + GP + 'variable g_probe equal 98.1\n')), D2K, (),
             ['사전 공격 R3', '제어 글자'], {}),
            ('VP3b R3 재개 덱 "# note &<NBSP>" 다음 줄 variable g_probe equal 196.2 (LIGGGHTS = 안 이음 → 정의가 돈다 · 예전 = 주석에 붙임)',
             (d2m.replace(FG, 'variable g_probe equal 98.1\n' + GP), d2r.replace(FG, 'variable g_probe equal 98.1\n# note & \nvariable g_probe equal 196.2\n' + GP)),
             D2K, (), ['196.2'], {}),
            ('VP3c R3 본 덱 "variab&" ↵ "le g_probe equal 196.2" (LIGGGHTS = variable · 사이 공백 없음 · 예전 = "variab le")',
             (d2m.replace(FG, 'variable g_probe equal 98.1\nvariab&\nle g_probe equal 196.2\n' + GP + 'variable g_probe equal 98.1\n'),
              d2r.replace(FG, 'variable g_probe equal 98.1\n' + GP + 'variable g_probe equal 98.1\n')), D2K, (), ['그 자리 치환 값이 본 덱과 다름', '196.2'], {}),
            ('VP3d R3 두 덱 fix gravi 의 낱말 사이 NBSP (98.1<NBSP>vector · LIGGGHTS 는 한 낱말 · 예전 도구 = 공백)',
             d2(FG.replace(' vector', ' vector'), FG.replace(' vector', ' vector')), D2K, (), ['사전 공격 R3', '주석 밖 비 ASCII'], None),
            ('VP3e R3 두 덱 fix gravi 의 낱말 사이 \\f (제어 글자)', d2(FG.replace(' vector', '\x0cvector'), FG.replace(' vector', '\x0cvector')), D2K, (),
             ['사전 공격 R3', '제어 글자'], None),
            ('VP3f R3 재개 덱 주석 안 NUL (제어 글자 · 주석 안이어도)', (d2m, d2r.replace(FG, FG + '# nul \x00 here\n')), D2K, (), ['사전 공격 R3', '제어 글자'], None),
            ("VP3g R3 두 덱 print 'q\"x' # 한글 (LIGGGHTS 주석 규칙 = 따옴표가 바뀜 → # 뒤도 명령 · 예전 = 주석으로 뺌)",
             d2(FG + "print 'q\"x' # 한글\n", FG + "print 'q\"x' # 한글\n"), D2K, (), ['사전 공격 R3', '주석 밖 비 ASCII'], None),
            ('VP4a R4 준비 구간 print file/append w.stl (${pz} · 본 덱 0.2 ↔ 재개 덱 0.5) → 준비 구간 fix mesh/surface file w.stl 이 읽음',
             d2(FG + 'variable pz equal 0.5\nvariable pz equal 0.2\n' + STL + 'variable pz equal 0.5\n' + MF,
                FG + 'variable pz equal 0.5\n' + STL + 'variable pz equal 0.5\n' + MF), D2K, (), ['사전 공격 R4', 'w.stl'], {}),
            ('VP4b R4 준비 구간 print file %s (두 덱 같은 글자) → 뒤 구간 fix top_mesh 가 그 파일을 읽음' % PLATE,
             d2(FG + 'print "solid x" file %s screen no\n' % PLATE, FG + 'print "solid x" file %s screen no\n' % PLATE), D2K, (),
             ['사전 공격 R4', PLATE], None),
            ('VP5a R5 합성 write_restart — 본 덱 체크포인트 앞 jump SELF sk 가 fix gx 를 건너뜀 · 재개 덱 fix gx (변수 없음)',
             (sm('jump SELF sk\n', 'label sk\n'), SR), SK, (), ['사전 공격 R5', 'jump SELF sk'], None),
            ('VP5b R5 합성 write_restart — 본 덱 체크포인트 앞 clear (fix gx 를 지움) · 재개 덱 fix gx',
             (sm('', 'clear\nunits si\n'), SR), SK, (), ['사전 공격 R5', 'clear'], None),
            ('VP5c R5 합성 write_restart — 본 덱 체크포인트 앞 label 하나 (쓰이지 않아도 · 보수 쪽)', (sm('label l0\n'), SR), SK, (),
             ['사전 공격 R5', 'label l0'], None),
            ('VP5d R5 합성 write_restart — 본 덱 체크포인트 앞 if 안 jump (겹친 흐름 줄)', (sm('if "1 > 2" then "jump SELF nowhere"\n'), SR), SK, (),
             ['사전 공격 R5', 'jump SELF nowhere'], None),
            ('VP5e R5 합성 write_restart — 본 덱 체크포인트 앞 python (상태를 바꿀 수 있다)', (sm('python pf source here "pass"\n'), SR), SK, (),
             ['사전 공격 R5', 'python'], None),
            ('VP5f R5 v3 after_settling — 본 덱 jump SELF skipx 가 fix gx 를 건너뜀 · 재개 덱 fix gx',
             (t50.replace(FI, FI + 'jump SELF skipx\n' + GX + 'label skipx\n'), r50.replace(FI, FI + GX)), CK50, (), ['사전 공격 R5', 'jump SELF skipx'], None),
            ('VP6b R6 판 메시 fix file ${mf} ↔ ${mf}_r4 (펼치면 wall_kg50.stl_r4) — 작업 폴더에 치환 전 이름 "${mf}_r4" 만 있음',
             d2(FG + 'variable mf string wall_kg50.stl\nfix wmesh all mesh/surface file ${mf} type 1 scale 1.0\n',
                FG + 'variable mf string wall_kg50.stl\nfix wmesh all mesh/surface file ${mf}_r4 type 1 scale 1.0\n'), D2K, ('${mf}_r4',),
             ['wall_kg50.stl_r4', '작업 폴더에 없음'], None),
            ('VP2f R2 두 덱 끝 partition yes 1 include extra.in (partition 안 include · next = 다룰 수 없는 구문 — run every · if 안과 같은 길)',
             (d2m + 'partition yes 1 include extra.in\n', d2r + 'partition yes 1 include extra.in\n'), D2K, (), ['다룰 수 없는 구문', 'include'], None),
            ('VP4c R4 준비 구간 print file ${pf} (pf = w.stl · 이름에 그 자리 치환 = 정할 수 없음) → 준비 구간 fix mesh/surface file w.stl',
             d2(FG + 'variable pf string w.stl\nprint "solid w" file ${pf} screen no\n' + MF, FG + 'variable pf string w.stl\nprint "solid w" file ${pf} screen no\n' + MF),
             D2K, (), ['사전 공격 R4', '${pf}'], None),
            ('VP6c R6 판 메시 fix file w${k}.stl ↔ w${k}_r4.stl (k = equal 4 · 펼친 이름에 equal 값) — 작업 폴더에 치환 전 이름 "w${k}_r4.stl" 만 있음',
             d2(FG + 'variable k equal 4\nfix wmesh all mesh/surface file w${k}.stl type 1 scale 1.0\n',
                FG + 'variable k equal 4\nfix wmesh all mesh/surface file w${k}_r4.stl type 1 scale 1.0\n'), D2K, ('w${k}_r4.stl',),
             ['사전 공격 R6', '펼칠 수 없음'], None),
            ('VP6d R6 뒤 구간 판 메시 fix top_mesh file ${pf} ↔ ${pf}_r4 (pf = %s) — 작업 폴더에 치환 전 이름 "${pf}_r4" 만 있음' % PLATE,
             (d2m.replace(FG, FG + 'variable pf string %s\n' % PLATE).replace('top_mesh all mesh/surface/stress file %s ' % PLATE,
                                                                             'top_mesh all mesh/surface/stress file ${pf} '),
              d2r.replace(FG, FG + 'variable pf string %s\n' % PLATE).replace('top_mesh all mesh/surface/stress file %s ' % PLATE,
                                                                             'top_mesh all mesh/surface/stress file ${pf}_r4 ')), D2K, ('${pf}_r4',),
             ['사전 공격 R6', '뒤 구간'], None),
            ('VP8 R8 group gsel type ${t} — 본 덱 t 1 → 3 → group → 1 · 재개 덱 3 을 뺌 (변이 M16 = group 을 값 대조에서 빼면 통과하던 자리)',
             d2(FG + 'variable t equal 1\nvariable t equal 3\ngroup gsel type ${t}\nvariable t equal 1\n',
                FG + 'variable t equal 1\ngroup gsel type ${t}\nvariable t equal 1\n'), D2K, (), ['그 자리 치환 값이 본 덱과 다름', '${t}'], None),
        ]
        for tag, (mt, rt), ck, wfiles, frags, flow in neg:
            mp = os.path.join(tmp, 'vpm.liggghts')
            with open(mp, 'w', encoding='utf-8', newline='') as f:
                f.write(mt)
            rp = os.path.join(tmp, 'vpr.liggghts')
            with open(rp, 'w', encoding='utf-8', newline='') as f:
                f.write(rt)
            rc, out = deckcheck_only(script, mp, rp, ck[0], ck[1], wfiles)
            bad = [l for l in out.splitlines() if l.startswith('  ✗ ')]
            chk('%s → -C 거부 (%s)' % (tag, ' · '.join(frags)), rc != 0 and bad and all(any(x in l for l in bad) for x in frags), out)
            if flow is not None:
                r = run_case(script, None, None, res_text=rt, trial_text=trial_log('ok'), main_bytes=mt.encode('utf-8'), ckpt=ck[0],
                             extra=('-T',), **flow)
                chk('%s → 본 흐름 (-T) 시험 0 · 본 0 (정적 대조 실패)' % tag,
                    not r['trial'] and not r['main'] and '✗ 재개 덱 정적 대조 실패' in r['out'], r['out'])
        # 양성 · 대조군 — 고친 판이 정상 덱을 막지 않음 (VP6a 는 고치기 전 판이 치환 전 이름으로 찾아 거짓 거부)
        pos = [
            ('VP2z R2 대조군 — 본 덱 삽입 run 1 every 1 "print \'every ok\'" (print 만)',
             (d2m.replace(INS1, 'run 1 every 1 "print \'every ok\'"\nunfix ins_mix\n'), d2r), D2K, (), '그 자리 치환 대조'),
            ('VP3z R3 대조군 — 두 덱 fix gravi 줄 끝 한글 주석', d2(FG.replace('\n', '   # 중력 · 한글 주석\n'), FG.replace('\n', '   # 중력 · 한글 주석\n')),
             D2K, (), '그 자리 치환 대조'),
            ('VP4z R4 대조군 — 두 덱 준비 구간 print file note.txt (읽는 명령 없음)',
             d2(FG + 'print "note" file note.txt screen no\n', FG + 'print "note" file note.txt screen no\n'), D2K, (), '그 자리 치환 대조'),
            ('VP5z R5 대조군 — 합성 write_restart (흐름 줄 없음)', (sm(''), SR), SK, (), '재개 지점 상태 대조'),
            ('VP6a R6 판 메시 fix file ${mf} ↔ ${mf}_r4 — 작업 폴더에 펼친 이름 wall_kg50.stl_r4 만 있음 (고치기 전 판 = 치환 전 이름으로 찾아 거짓 거부)',
             d2(FG + 'variable mf string wall_kg50.stl\nfix wmesh all mesh/surface file ${mf} type 1 scale 1.0\n',
                FG + 'variable mf string wall_kg50.stl\nfix wmesh all mesh/surface file ${mf}_r4 type 1 scale 1.0\n'), D2K, ('wall_kg50.stl_r4',),
             '판 메시 파일만 다름 (재개 지점 fix wmesh): wall_kg50.stl_r4'),
            ('VP7z R7 대조군 — ${} 사슬 6 단 (두 덱 같음)', d2(chain(6, '${a%d}'), chain(6, '${a%d}')), D2K, (), '그 자리 치환 대조'),
            ('VP8z R8 대조군 — group gsel type ${t} (두 덱 같은 값)',
             d2(FG + 'variable t equal 1\ngroup gsel type ${t}\n', FG + 'variable t equal 1\ngroup gsel type ${t}\n'), D2K, (), '그 자리 치환 대조'),
        ]
        for tag, (mt, rt), ck, wfiles, frag in pos:
            mp = os.path.join(tmp, 'vpm.liggghts')
            with open(mp, 'w', encoding='utf-8', newline='') as f:
                f.write(mt)
            rp = os.path.join(tmp, 'vpr.liggghts')
            with open(rp, 'w', encoding='utf-8', newline='') as f:
                f.write(rt)
            rc, out = deckcheck_only(script, mp, rp, ck[0], ck[1], wfiles)
            chk('%s → -C 통과 (문제 0 · %s)' % (tag, frag), rc == 0 and '통과 (문제 0)' in out and frag in out, out)
        # R7 — 펼친 글 크기 상한: 깊은 사슬은 짧은 시간에 닫힌 실패 (고치기 전 판 = ${} 20 단 316 s (리뷰어 실측) · v_ 24 단은 그보다 훨씬 김)
        SCH = FG + 'variable a0 string ab\n' + ''.join('variable a%d string ${a%d}${a%d}\n' % (k, k - 1, k - 1) for k in range(1, 21)) + \
            'fix gx all gravity ${a20} vector 0.0 0.0 -1.0\n'
        for tag, sch in (('${} 사슬 20 단 (정의 때 치환 · 글이 매 단 두 배)', chain(20, '${a%d}')), ('v_ 사슬 24 단 (쓸 때 계산 · 매 단 두 갈래)', chain(24, 'v_a%d')),
                         ('string ${}${} 사슬 20 단 (string 글이 매 단 두 배 · 2 MB)', SCH)):
            mt, rt = d2(sch, sch)
            rc, out, sec, to = run_deckcheck_limited(script, mt, rt, D2K[0], D2K[1], limit=60)
            bad = [l for l in out.splitlines() if l.startswith('  ✗ ')]
            chk('VP7 R7 %s → 60 초 안에 -C 거부 (사전 공격 R7 · 자를 넘음)' % tag,
                not to and rc != 0 and any('사전 공격 R7' in l and '자를 넘음' in l for l in bad),
                '%.1f 초%s · rc %d · ' % (sec, ' · 시간 초과 (프로세스 묶음 끝냄)' if to else '', rc) + out[-1300:])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


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

    # 10-30 (KG50R-F02): --only RB = 러너 결속 묶음만 (변이 시험용 · 다른 묶음 안 돎)
    if '--only' in sys.argv and sys.argv[sys.argv.index('--only') + 1] == 'RB':
        group_rb(script, chk, grp)
        print('%d PASS · %d FAIL' % (ok, fail))
        return 0 if fail == 0 else 1
    # 10-30 (KG50R-F01 2 판): --only VP = 사전 공격 R1–R8 묶음만 (변이 시험용)
    if '--only' in sys.argv and sys.argv[sys.argv.index('--only') + 1] == 'VP':
        group_vp(script, chk, grp)
        print('%d PASS · %d FAIL' % (ok, fail))
        return 0 if fail == 0 else 1

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
    # 10-28 밤 2 바꿈 (사전 공격 A): 그 쌍의 재개 덱 (dem_restart.py 실제 산출) 은 Phase 2 상태 fix (integr · gravi 9.81 · damp 0.5) 를 판 메시
    #   fix 앞에 둔다 (본 덱 = 판 메시 fix 뒤에 gravi · damp 다시 정의) → 준비 구간 순서 문제 하나가 더 나온다 (문제 1 → 2)
    chk('C1 실제 09-27 쌍 (압축 재개) → 거부 (압축 체크포인트 재개 = 지원 안 함 + 준비 구간 순서 · 10-28 밤 Q3 · 밤 2 A 로 기대 바꿈)',
        rc != 0 and Q3MSG in out and '(문제 2)' in out and '[fix top_mesh all mesh/surface/stress file plate_pse_r075_a_r30.stl' in out
        and '순서가 본 덱 체크포인트 앞 순서와 다름' in out, out)
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

    # ── Y: 10-28 밤 2 — 독립 사전 공격 리뷰 (고친 판 fb334928) 의 반례 A–F + 시험 빈틈 셋 (반례 폴더는 스크래치 · 여기는 v2 고정물로 같은 꼴) ──
    #   A 준비 구간에서 변수를 바꿨다 되돌림 (LIGGGHTS 는 ${dt} 를 그 자리에서 치환 · 끝 상태 대조만으로는 같아 보인다) · 순서 · B 본 덱
    #   체크포인트 run 꼬리 · C 시험 뒤 작업 폴더 덱 · 러너 바뀜 · 실행 영수증 · D 본 sbatch 출력 · E G3 유한 수 · F 케이스 이름 · 시도 기록
    #   빈틈 = 재삽입 (본 덱이 삽입 fix 를 unfix 안 함) · G1 만 실패 · G3 결손만 — 그 관문 하나만 막는 입력
    grp('Y')
    tmp = tempfile.mkdtemp(prefix='rcky_')
    try:
        good = res_good()
        with open(MAIN, encoding='utf-8') as f:
            mtxt = f.read()
        RRL = 'read_restart %s\n' % CKPT
        DT1, DT2, TS1 = 'variable dt      equal 1.0e-6\n', 'variable dt      equal 2.0e-6\n', 'timestep        ${dt}\n'
        assert good.count(RRL) == 1 and good.count(DT1) == 1 and good.count(TS1) == 1 and mtxt.count(DT1) == 1 and mtxt.count(TS1) == 1
        a1 = good.replace(RRL, RRL + DT2 + TS1 + DT1)
        a2 = good.replace(DT1, DT2).replace(TS1, TS1 + DT1)      # 실제 D2 r4 반례 꼴 (47 줄 2.0e-6 · timestep 뒤 1.0e-6)
        for tag, text in (('read_restart 뒤 dt 2e-6 · timestep · dt 1e-6', a1), ('dt 정의 2e-6 · timestep 뒤 1e-6 (D2 r4 반례 꼴)', a2)):
            rc, out = deckcheck_only(script, MAIN, write_tmp(tmp, 'ya.liggghts', text), CKPT, 20001)
            chk('Y1 -C 준비 구간 변수 다시 정의 · %s → 거부 (글자 그대로 · 사전 공격 A)' % tag, rc != 0 and '글자 그대로 없음' in out, out)
        asr = res_after('good', tmpl=True)
        RRA = 'read_restart restart_%s/restart_after_settling.bin\n' % C
        rc, out = deckcheck_only(script, MAIN, write_tmp(tmp, 'ya3.liggghts', asr.replace(RRA, RRA + DT2 + TS1 + DT1)), CKPT_AS, 200001)
        chk('Y2 -C after_settling 준비 구간 dt 바꿈 · timestep · 되돌림 → 거부 (사전 공격 A)', rc != 0 and '글자 그대로 없음' in out, out)
        # 순서 — 줄은 전부 본 덱에 있고 끝 상태도 같은데 즉시 치환 자리가 다르다 (본 덱: dt 1e-6 → timestep → dt 2e-6 = 실제 dt 1e-6)
        m3 = write_tmp(tmp, 'y3m.liggghts', mtxt.replace(TS1, TS1 + DT2))
        rc, out = deckcheck_only(script, m3, write_tmp(tmp, 'y3ok.liggghts', good.replace(TS1, TS1 + DT2)), CKPT, 20001)
        chk('Y3 -C 본 덱이 dt 를 두 번 정의 · 재개 덱이 같은 순서 → 통과 (대조군)', rc == 0, out)
        rc, out = deckcheck_only(script, m3, write_tmp(tmp, 'y3bad.liggghts', good.replace(TS1, DT2 + TS1)), CKPT, 20001)
        chk('Y3b -C 같은 줄 · dt 2e-6 이 timestep 앞 (실제 dt 2 배 · 끝 상태는 같다) → 거부 (순서 · 사전 공격 A)',
            rc != 0 and '순서가 본 덱 체크포인트 앞 순서와 다름' in out and '글자 그대로 없음' not in out, out)
        FI, FG = 'fix integr all nve/sphere\n', 'fix gravi all gravity 98.1 vector 0.0 0.0 -1.0\n'
        assert good.count(FI + FG) == 1
        rc, out = deckcheck_only(script, MAIN, write_tmp(tmp, 'y4.liggghts', good.replace(FI + FG, FG + FI)), CKPT, 20001)
        chk('Y4 -C 준비 구간 fix 순서 바꿈 (gravity ↔ nve/sphere · 줄은 같다) → 거부 (순서 · 사전 공격 J 가 A 로 닫힘)',
            rc != 0 and '순서가 본 덱 체크포인트 앞 순서와 다름' in out, out)
        rc, out = deckcheck_only(script, MAIN, write_tmp(tmp, 'y5.liggghts', good.replace(DT1, 'variable dt      equal 3.0e-6\n' + DT1)), CKPT, 20001)
        chk('Y5 -C 준비 구간에 본 덱에 없는 상태 줄 (쓰기 전에 되돌림 · 끝 상태 같음) → 거부 (글자 그대로 · 사전 공격 A)',
            rc != 0 and '글자 그대로 없음' in out, out)
        r = run_case(script, None, 'ok', res_text=a2)
        chk('Y6 본 흐름 · 준비 구간 dt 바꿈 (D2 r4 반례 꼴) → 시험 0 · 본 0 (사전 공격 A)', r['ntrial'] == 0 and r['nmain'] == 0, r['out'])
        # B — 본 덱 체크포인트 run 의 꼬리 (재개 덱 첫 긴 run 은 꼬리 없는 한 줄이라 같은 동작을 못 낸다)
        RUN0 = 'run 200000\n'
        i0 = mtxt.index('restart 50000 restart_%s/restart_settling_*.bin\n' % C)
        j0 = mtxt.index(RUN0, i0)

        def mtail(t):
            return mtxt[:j0] + t + mtxt[j0 + len(RUN0):]
        for tag, tl in (('every velocity', 'run 200000 every 1000 "velocity all set 0.0 0.0 0.0"\n'),
                        ('every include', 'run 200000 every 1000 "include extra.in"\n'),
                        ('pre no post no', 'run 200000 pre no post no\n'), ('upto', 'run 200001 upto\n')):
            rc, out = deckcheck_only(script, write_tmp(tmp, 'y7m.liggghts', mtail(tl)), write_tmp(tmp, 'y7r.liggghts', good), CKPT, 20001)
            chk('Y7 -C 본 덱 체크포인트 run 꼬리 (%s) → 거부 (사전 공격 B)' % tag, rc != 0 and '본 덱 체크포인트 run 에 꼬리' in out, out)
        rc, out = deckcheck_only(script, write_tmp(tmp, 'y7im.liggghts', mtxt.replace('run 100000\n', 'run 100000 every 1000 "include extra.in"\n', 1)),
                                 write_tmp(tmp, 'y7ir.liggghts', good.replace('run 100000\n', 'run 100000 every 1000 "include extra.in"\n', 1)), CKPT, 20001)
        chk('Y7c -C 뒤 구간 run every 안 include (두 덱 같은 줄) → 거부 (다룰 수 없는 구문 · run every 안까지)',
            rc != 0 and '다룰 수 없는 구문' in out and 'include' in out, out)
        r = run_case(script, 'good', 'ok', main_bytes=mtail('run 200000 every 1000 "velocity all set 0.0 0.0 0.0"\n').encode())
        chk('Y7b 본 흐름 · 본 덱 체크포인트 run every → 시험 0 · 본 0 (사전 공격 B)', r['ntrial'] == 0 and r['nmain'] == 0, r['out'])
        # C — 시험 뒤 작업 폴더의 재개 덱 · 러너가 바뀜 → 본 제출 직전 sha256 대조 · 실행 영수증
        for tag, tgt in (('재개 덱', 'input_%s_%s.liggghts' % (C, SFX)), ('러너', 'run_%s_%s.sh' % (C, SFX))):
            ctx = make_root()
            try:
                r = invoke(ctx, script, good, trial_log('ok'), env_more={'FAKE_EDIT_AFTER_TRIAL': os.path.join(ctx['L'], C, tgt)})
            finally:
                shutil.rmtree(ctx['tmp'], ignore_errors=True)
            chk('Y8 시험 제출 뒤 작업 폴더 %s 가 바뀜 → 본 제출 직전 sha256 ≠ 시험 때 기록 → 본 제출 안 함 (사전 공격 C)' % tag,
                r['trial'] and not r['main'] and '시험 때와 다름' in r['rep'], r['out'] + r['rep'])
        ctx = make_root()
        try:
            lmp = os.path.join(ctx['stub'], 'lmp_mpi')
            with open(lmp, 'w') as f:
                f.write('#!/bin/sh\nexit 0\n')
            os.chmod(lmp, 0o755)
            ck_sha, lmp_sha = sha256f(os.path.join(ctx['S'], CKPT)), sha256f(lmp)
            r = invoke(ctx, script, good, trial_log('ok'))
        finally:
            shutil.rmtree(ctx['tmp'], ignore_errors=True)
        tt = next((v for k, v in r['att'].items() if k.endswith('/tool.txt')), '')
        chk('Y9 시도 폴더 tool.txt = 재개 덱 · 러너 · 체크포인트 sha256 · lmp_mpi 경로 · sha256 (실행 영수증 · 사전 공격 C · Codex §10-5)',
            r['main'] and ('체크포인트 %s sha256 %s' % (CKPT, ck_sha)) in tt and ('lmp_mpi %s sha256 %s' % (lmp, lmp_sha)) in tt
            and '재개 덱 sha256 ' in tt and '러너 sha256 ' in tt, tt + r['rep'])
        # D — 본 sbatch 출력 (시험 쪽 Q9d 와 같은 규칙)
        r = run_case(script, 'good', 'ok', env_more={'FAKE_SBATCH_MAIN_TEXT': 'sbatch: error: QOSMaxSubmitJobPerUserLimit'})
        a = dict((k.split('/', 1)[1], v) for k, v in r['att'].items() if '/' in k)
        chk('Y10 본 sbatch 가 job 번호 아닌 글 (종료 코드 1) → ✅ 안 찍음 · ⛔ 본 제출 실패 · main_job.txt 없음 (사전 공격 D)',
            r['main'] and '✅ 본 제출 job' not in r['rep'] and '⛔ 본 제출 실패' in r['rep'] and 'QOSMaxSubmitJobPerUserLimit' in r['rep']
            and 'main_job.txt' not in a and '본 제출 실패' in a.get('result.txt', ''), r['rep'] + ' '.join(sorted(a)))
        r = run_case(script, 'good', 'ok', env_more={'FAKE_SBATCH_MAIN_SUFFIX': ';clusterA'})
        a = dict((k.split('/', 1)[1], v) for k, v in r['att'].items() if '/' in k)
        chk('Y10b 본 sbatch --parsable 의 id;cluster → job 번호만 (✅ 9001 · main_job.txt 9001)',
            '✅ 본 제출 job 9001 (' in r['rep'] and a.get('main_job.txt') == '9001\n', r['rep'] + ' '.join(sorted(a)))
        # E — G3 비교 줄의 유한 수 (mawk · gawk 같은 판정 · nan · inf 어느 철자든)
        for tok in ('nan', 'NaN', '+nan', '-nan', 'inf', '-inf', 'Infinity'):
            rows = T_OK[:]
            assert '0.0955' in rows[2]
            rows[2] = rows[2].replace('0.0955', '%6s' % tok)
            r = run_case(script, 'good', None, trial_text='\n'.join(['LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0)'] + rows) + '\n')
            chk('Y11 시험 21000 줄 KE = %s (G3 비교 줄) → 본 제출 안 함 (사전 공격 E)' % tok, r['trial'] and not r['main'], r['rep'])
        orig = ORIG_LOG.replace('   21000   312506         0.0950', '   21000   312506            nan')
        assert orig != ORIG_LOG
        r = run_case(script, 'good', 'ok', orig_log=orig)
        chk('Y12 원 로그 21000 줄 KE = nan → 본 제출 안 함 (사전 공격 E)', r['trial'] and not r['main'], r['rep'])
        # F — 케이스 이름 (두 철자 · 위험한 이름) · 둘째 고리의 시도 기록 읽기
        ctx = make_root()
        try:
            r = invoke(ctx, script, good, trial_log('ok'), cases=[C, './' + C])
            prev = glob.glob(os.path.join(ctx['L'], C + '.prev_*')) + glob.glob(os.path.join(ctx['L'], '.', C + '.prev_*'))
        finally:
            shutil.rmtree(ctx['tmp'], ignore_errors=True)
        chk('Y13 케이스 두 철자 (C · ./C) → 둘째 시험 전 거부 (케이스 이름) · 시험 1 · 본 1 · 첫 작업 폴더가 prev 로 안 밀림 (사전 공격 F)',
            r['ntrial'] == 1 and r['nmain'] == 1 and not prev and ('## ./%s — 시험 전 거부' % C) in r['rep'] and '케이스 이름' in r['rep'],
            r['out'] + r['rep'] + ' prev=%s' % prev)
        for bad in ('.', '..', 'a/b', 'a*', 'a b'):
            ctx = make_root()
            try:
                before = sorted(os.listdir(ctx['L']))
                r = invoke(ctx, script, good, trial_log('ok'), cases=[bad])
                after = sorted(os.listdir(ctx['L']))
            finally:
                shutil.rmtree(ctx['tmp'], ignore_errors=True)
            made = [x for x in after if x not in before and not x.startswith('resume_') and x != 'logs']
            chk('Y14 케이스 이름 [%s] → 시험 전 거부 (케이스 이름) · 새 폴더 없음 (사전 공격 F)' % bad,
                r['ntrial'] == 0 and r['nmain'] == 0 and not made and '케이스 이름' in r['out'], r['out'] + ' made=%s' % made)
        ctx = make_root()
        try:
            r = invoke(ctx, script, good, trial_log('ok'), env_more={'FAKE_RM_MODE': os.path.join(ctx['L'], C)})
        finally:
            shutil.rmtree(ctx['tmp'], ignore_errors=True)
        chk('Y15 둘째 고리에서 시도 폴더 mode.txt 를 못 읽음 → 그 케이스 본 제출 안 함 · 보고에 그 사유 (사전 공격 F)',
            r['trial'] and not r['main'] and '시도 폴더 기록' in r['rep'] and '못 읽음' in r['rep'], r['out'] + r['rep'])
        # 시험 빈틈 셋 (리뷰어 변이 생존 py_reinsert · sh_g1 · sh_miss) — 그 관문 하나만 막는 입력
        UNF = 'unfix ins_mix\n'
        assert mtxt.count(UNF) == 1
        raw, take = [], False
        for l in mtxt.splitlines(keepends=True):
            take = take or bool(re.match(r'\s*fix\s+ins_mix\b', l))
            if take:
                raw.append(l)
                if not l.rstrip().endswith('&'):
                    break
        PH1 = 'print "====== PHASE 1: SETTLING ======"\n'
        assert good.count(PH1) == 1 and raw
        rc, out = deckcheck_only(script, write_tmp(tmp, 'y16m.liggghts', mtxt.replace(UNF, '')),
                                 write_tmp(tmp, 'y16r.liggghts', good.replace(PH1, ''.join(raw) + PH1)), CKPT, 20001)
        chk('Y16 본 덱이 삽입 fix 를 unfix 안 함 · 재개 덱이 그 줄을 본 덱 순서 자리에 다시 선언 → 거부 (재삽입 · 그 문제 하나 · 빈틈 py_reinsert)',
            rc != 0 and '재삽입' in out and '(문제 1)' in out, out)
        rows = T_OK[:]
        assert '0.1000' in rows[1]
        rows[1] = rows[1].replace('0.1000', '0.1003')
        r = run_case(script, 'good', None, trial_text='\n'.join(['LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0)'] + rows) + '\n')
        chk('Y17 시험 setup 줄 KE 0.1000 → 0.1003 (G1 만 실패 · G0 · G3 통과) → 본 제출 안 함 (빈틈 sh_g1)',
            r['trial'] and not r['main'] and '- G0 시험 정상 종료: 통과' in r['rep'] and '1e-6): 실패' in r['rep'] and '5 % 안' in r['rep'], r['rep'])
        rows = [x for x in T_OK if not x.lstrip().startswith('22000 ')]
        assert len(rows) == len(T_OK) - 1
        r = run_case(script, 'good', None, trial_text='\n'.join(['LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0)'] + rows) + '\n')
        chk('Y18 시험 로그에서 22000 줄 하나만 빠짐 (G0 · G1 · G3 첫 줄 통과) → G3 결손 → 본 제출 안 함 (빈틈 sh_miss)',
            r['trial'] and not r['main'] and '결손' in r['rep'] and '- G0 시험 정상 종료: 통과' in r['rep'], r['rep'])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ── V: 10-30 (KG50R-F01 · Codex KG50RF-01 · P1 · 1저자 Q1 "권고대로") 준비 구간이 그 자리에서 쓰는 변수 값 ──
    #   LIGGGHTS 는 ${x} · $x (따옴표 밖) 를 그 줄을 읽을 때 x 의 그때 값으로 바꾸고 equal 수식의 v_x 는 쓸 때 계산한다 (고정판
    #   doc/variable.txt).  순서 보존 부분열 · 끝 상태 글자만으로는 중간 정의를 뺀 덱 · 실행 상태에 따라 바뀌는 equal 수식을 못 막았다.
    #   반례 = Codex 넷 (받은 D2 덱 파생 둘 · 합성 둘 — 리포 D2 덱 · 이 시험 안 글자로 다시 만든다 · 합성 둘은 Codex 파일과 바이트 같음) +
    #   같은 부류 (사슬 · 한 글자 $g · 템플릿 반지름 · $(...) · 같은 글자 정의가 본 덱에 둘 · 본 덱 앞 구간 반복 · } 없음 · string).
    #   음성 = -C 거부 (문제에 KG50R-F01) + 본 흐름 (-T) 시험 0 · 양성 = 받은 D2 덱 · 보관 after_settling · v3 · 안전한 생략 · 상수 사슬 통과
    grp('V')
    tmp = tempfile.mkdtemp(prefix='rckv_')
    try:
        D2D = os.path.join(ROOT, 'docs/data/kg50_resume_tests_20261027/d2_main_1028_0942')
        with open(os.path.join(D2D, 'input_kg50_d2_b50.liggghts'), encoding='utf-8') as f:
            d2m = f.read()
        with open(os.path.join(D2D, 'input_kg50_d2_b50_r4.liggghts'), encoding='utf-8') as f:
            d2r = f.read()
        D2CK, D2S0 = 'restart_kg50_d2_b50/restart_settling_20001.bin', 20001
        FG = 'fix gravi all gravity 98.1 vector 0.0 0.0 -1.0\n'
        GP = 'fix gravi all gravity ${g_probe} vector 0.0 0.0 -1.0\n'
        TSD = 'timestep        ${dt}\n'
        RAS = 'variable r_AM_S  equal 2.0e-3'
        NI = 'variable n_ins equal count(all)\n'
        assert d2m.count(FG) == 1 and d2r.count(FG) == 1 and d2m.count(TSD) == 1 and d2r.count(TSD) == 1
        assert d2m.count(RAS) == 1 and d2r.count(RAS) == 1 and d2m.count(NI) == 1 and d2r.count(NI) == 1
        PMG, INS1 = 'variable plate_margin equal 0.003\n', 'run 1\nunfix ins_mix\n'
        assert d2m.count(PMG) == 1 and d2r.count(PMG) == 1 and d2m.count(INS1) == 1 and d2r.count(INS1) == 0

        def gv(*xs):
            # 'FIX' = fix gravi … ${g_probe} 한 줄 · 그 밖 = variable g_probe equal <값>
            return ''.join(GP if x == 'FIX' else 'variable g_probe equal %s\n' % x for x in xs)

        def d2(mrep, rrep, old=FG):
            return d2m.replace(old, mrep), d2r.replace(old, rrep)
        # Codex 합성 둘 (independent/program/cases/{drop_intermediate_variable_definition, runtime_dependent_eager_variable} — CRLF 그대로)
        TDROP_M = ('units si\r\nvariable dt equal 1e-6\r\nvariable dt equal 2e-6\r\ntimestep ${dt}\r\nvariable dt equal 1e-6\r\n'
                   'restart 10 restart_settling_*.bin\r\nrun 100\r\nprint "done"\r\n')
        TDROP_R = ('units si\r\nread_restart restart_settling_50.bin\r\nvariable dt equal 1e-6\r\ntimestep ${dt}\r\nvariable dt equal 1e-6\r\n'
                   'restart 10 restart_settling_*.bin\r\nrun 50\r\nprint "done"\r\n')
        TEAG_M = 'units si\r\nvariable dt equal 1e-6*(step+1)\r\ntimestep ${dt}\r\nrestart 10 restart_settling_*.bin\r\nrun 100\r\nprint "done"\r\n'
        TEAG_R = ('units si\r\nread_restart restart_settling_50.bin\r\nvariable dt equal 1e-6*(step+1)\r\ntimestep ${dt}\r\n'
                  'restart 10 restart_settling_*.bin\r\nrun 50\r\nprint "done"\r\n')
        TOK_M, TOK_R = TDROP_M.replace('variable dt equal 2e-6\r\n', ''), TDROP_R
        TCK = ('restart_settling_50.bin', 50)
        # v3 50×50 after_settling (write_restart 체크포인트) — 본 덱 앞 구간에 반복 (label · if jump): 첫 바퀴 timestep ${dt} = 1e-6 →
        #   dt 2e-6 · n0 = 1 → jump → 둘째 바퀴 timestep 2e-6 · n0 = 2 → 나감 (본 덱 timestep = 2e-6 · 줄 순서로만 읽으면 1e-6) ·
        #   재개 덱 = 반복 줄 없이 같은 줄 (V14 · 그 자리 값을 줄 순서로 못 정하는 본 덱 = 닫힌 실패)
        with open(MAIN50, encoding='utf-8') as f:
            t50 = f.read()
        assert t50.count(TSD) == 1
        m14 = t50.replace(TSD, 'variable n0 equal 0\nlabel pre0\n' + TSD + 'variable dt      equal 2.0e-6\nvariable n0 equal ${n0}+1\n'
                          'if "${n0} < 2" then "jump SELF pre0"\n')
        r14 = res_after('good', MAIN50, C50, tmpl=True)
        assert r14.count(TSD) == 1
        r14 = r14.replace(TSD, TSD + 'variable dt      equal 2.0e-6\n')
        CK50 = ('restart_%s/restart_after_settling.bin' % C50, 200001)
        AS50 = dict(mode='after_settling', orig_log=AS_LOG)
        D2K = (D2CK, D2S0)
        neg = [
            ('V2 Codex d2_drop_intermediate_variable_definition (g 98.1 → 196.2 → fix ${g_probe} → 98.1 · 재개 덱이 196.2 만 뺌)',
             d2(gv('98.1', '196.2', 'FIX', '98.1'), gv('98.1', 'FIX', '98.1')), D2K, {},
             ['그 자리 치환 값이 본 덱과 다름', '${g_probe}', '196.2', '98.1']),
            ('V3 Codex d2_runtime_dependent_eager_variable (두 덱 같은 g = 98.1*(step+1) · fix ${g_probe})',
             d2(gv('98.1*(step+1)', 'FIX'), gv('98.1*(step+1)', 'FIX')), D2K, {}, ['실행 상태에 따라 바뀜', '${g_probe}', 'step']),
            ('V4 Codex 합성 drop_intermediate_variable_definition (dt 1e-6 → 2e-6 → timestep ${dt} → 1e-6 · 2e-6 만 뺌)',
             (TDROP_M, TDROP_R), TCK, {}, ['그 자리 치환 값이 본 덱과 다름', '${dt}', '2e-6', '1e-6']),
            ('V5 Codex 합성 runtime_dependent_eager_variable (두 덱 같은 dt = 1e-6*(step+1) · timestep ${dt})',
             (TEAG_M, TEAG_R), TCK, {}, ['실행 상태에 따라 바뀜', '${dt}', 'step']),
            ('V6 사슬 — b = ${a}*2 정의 앞 a 중간 정의 (98.1) 를 뺌 · fix 가 v_b 로 씀',
             d2('variable a_g equal 49.05\nvariable a_g equal 98.1\nvariable b_g equal ${a_g}*2\nvariable a_g equal 49.05\n'
                'fix gravi all gravity v_b_g vector 0.0 0.0 -1.0\n',
                'variable a_g equal 49.05\nvariable b_g equal ${a_g}*2\nvariable a_g equal 49.05\n'
                'fix gravi all gravity v_b_g vector 0.0 0.0 -1.0\n'), D2K, {}, ['그 자리 치환 값이 본 덱과 다름', '${a_g}', '98.1', '49.05']),
            ('V7 한 글자 $g — g 98.1 → 196.2 → fix $g → 98.1 · 196.2 만 뺌',
             d2('variable g equal 98.1\nvariable g equal 196.2\nfix gravi all gravity $g vector 0.0 0.0 -1.0\nvariable g equal 98.1\n',
                'variable g equal 98.1\nfix gravi all gravity $g vector 0.0 0.0 -1.0\nvariable g equal 98.1\n'), D2K, {},
             ['그 자리 치환 값이 본 덱과 다름', '$g', '196.2']),
            ('V8 템플릿 fix 반지름 ${r_AM_S} = 실행 상태 수식 2.0e-3*(1+step) (두 덱 같은 글자)',
             d2(RAS + '*(1+step)', RAS + '*(1+step)', RAS), D2K, {}, ['실행 상태에 따라 바뀜', '${r_AM_S}', 'pts2']),
            ('V9 $(...) 그 자리 식 — timestep $(v_dt) (두 덱 같은 글자)',
             d2('timestep        $(v_dt)\n', 'timestep        $(v_dt)\n', TSD), D2K, {}, ['펼칠 수 없음', '$(v_dt)', '그 자리 식 = 지원 안 함']),
            ('V12 같은 글자 fix 가 본 덱에 둘 — 재개 덱 fix 는 앞 것 자리 (g 98.1) 에 맞춰지고 본 덱 끝 상태 = 뒤 것 (g 196.2)',
             d2(gv('98.1', 'FIX', '196.2', 'FIX', '98.1'), gv('98.1', 'FIX', '98.1')), D2K, {},
             ['그 자리 치환을 펼치면', '재개 지점 fix gravi', '196.2']),
            ('V13 같은 글자 b = ${a}*2 정의가 본 덱에 둘 — 끝 상태 b = 뒤 것 (a 98.1) ↔ 재개 덱 (a 49.05)',
             d2('variable a_g equal 49.05\nvariable b_g equal ${a_g}*2\nvariable a_g equal 98.1\nvariable b_g equal ${a_g}*2\n'
                'variable a_g equal 49.05\nfix gravi all gravity v_b_g vector 0.0 0.0 -1.0\n',
                'variable a_g equal 49.05\nvariable b_g equal ${a_g}*2\nvariable a_g equal 49.05\n'
                'fix gravi all gravity v_b_g vector 0.0 0.0 -1.0\n'), D2K, {}, ['그 자리 치환을 펼치면', '재개 지점 variable b_g', '98.1']),
            ('V14 v3 after_settling — 본 덱 체크포인트 앞에 반복 (label · if jump) · 준비 구간 timestep ${dt} (줄 순서로만 읽으면 같다)',
             (m14, r14), CK50, AS50, ['펼칠 수 없음', '흐름 줄', '${dt}']),
            ('V15 ${ 닫는 } 없음 — timestep ${dt (두 덱 같은 글자)',
             d2('timestep        ${dt\n', 'timestep        ${dt\n', TSD), D2K, {}, ['펼칠 수 없음', '${dt']),
            ('V16 string 변수 = 정의 때 실행 상태 값 (variable s_ins string ${n_ins} · n_ins = count(all) · 두 덱 같은 글자)',
             d2(NI + 'variable s_ins string ${n_ins}\n', NI + 'variable s_ins string ${n_ins}\n', NI), D2K, {},
             ['실행 상태에 따라 바뀜', '${n_ins}', 'count']),
            ('V20 string 값에 공백 (variable g_s string "98.1 vector 0.0 0.0 -1.0" · fix gravity ${g_s} — 치환 뒤 낱말이 갈림 · 닫힌 실패)',
             d2('variable g_s string "98.1 vector 0.0 0.0 -1.0"\nfix gravi all gravity ${g_s}\n',
                'variable g_s string "98.1 vector 0.0 0.0 -1.0"\nfix gravi all gravity ${g_s}\n'), D2K, {}, ['펼칠 수 없음', '공백']),
            ('V21 v_ 로 쓰는 string 값이 수 글 아님 (g_s string abc · g = v_g_s*2 · 닫힌 실패)',
             d2('variable g_s string abc\nvariable g_probe equal v_g_s*2\n' + GP, 'variable g_s string abc\nvariable g_probe equal v_g_s*2\n' + GP),
             D2K, {}, ['펼칠 수 없음', 'v_g_s']),
            ('V22 atom 변수를 ${} 로 씀 (닫힌 실패)',
             d2('variable g_probe atom 98.1\n' + GP, 'variable g_probe atom 98.1\n' + GP), D2K, {}, ['펼칠 수 없음', 'atom']),
            ('V23 PI (등록 상수 목록 밖 · 닫힌 실패)', d2(gv('98.1+0*PI', 'FIX'), gv('98.1+0*PI', 'FIX')), D2K, {}, ['실행 상태에 따라 바뀜', 'PI']),
            ('V24 논리 연산자 || (등록 상수 목록 밖 · 닫힌 실패)', d2(gv('98.1*(1||0)', 'FIX'), gv('98.1*(1||0)', 'FIX')), D2K, {},
             ['실행 상태에 따라 바뀜', '논리 연산자']),
            ('V25 본 덱 체크포인트 앞 run every 안 variable (삽입 run 1 끝에 g = 196.2 · 재개 덱에는 그 run 이 없다 · 줄 순서로만 읽으면 98.1)',
             (d2m.replace(PMG, PMG + 'variable g_probe equal 98.1\n').replace(INS1, 'run 1 every 1 "variable g_probe equal 196.2"\nunfix ins_mix\n')
              .replace(FG, GP), d2r.replace(PMG, PMG + 'variable g_probe equal 98.1\n').replace(FG, GP)), D2K, {},
             ['펼칠 수 없음', 'run 1 every 1']),
            ('V26 판 메시 fix (file 이름만 다름 허용) 가 본 덱에 둘 · 끝 상태 = 뒤 것 (scale ${msc} = 2.0) ↔ 재개 덱 (1.0)',
             d2('variable msc equal 1.0\nfix wmesh all mesh/surface file wall_kg50.stl type 1 scale ${msc}\nvariable msc equal 2.0\n'
                'fix wmesh all mesh/surface file wall_kg50.stl type 1 scale ${msc}\nvariable msc equal 1.0\n' + FG,
                'variable msc equal 1.0\nfix wmesh all mesh/surface file wall_kg50_r4.stl type 1 scale ${msc}\nvariable msc equal 1.0\n' + FG),
             D2K, {'more_decks': (('wall_kg50_r4.stl', b'solid w\nendsolid w\n'),)}, ['판 메시 fix 에 그 자리 치환', 'wall_kg50_r4.stl']),
            ('V28 v3 after_settling — 본 덱 체크포인트 앞 python 줄 (변수를 바꿀 수 있다 · 재개 덱에는 없음) · 준비 구간 timestep ${dt}',
             (t50.replace(TSD, 'python pyx file pyx.py\n' + TSD), res_after('good', MAIN50, C50, tmpl=True)), CK50, AS50,
             ['펼칠 수 없음', 'python pyx']),
            ('V29 본 덱 체크포인트 앞 variable ${vn} equal 196.2 (이름 자리 치환 = g_probe 를 바꿈 · 재개 덱에는 없음 · 줄 순서로만 읽으면 98.1)',
             (d2m.replace(PMG, PMG + 'variable vn string g_probe\nvariable g_probe equal 98.1\nvariable ${vn} equal 196.2\n').replace(FG, GP),
              d2r.replace(PMG, PMG + 'variable vn string g_probe\nvariable g_probe equal 98.1\n').replace(FG, GP)), D2K, {},
             ['펼칠 수 없음', '이름 · 꼴 자리']),
            ('V32 $ 뒤 이름 글자 아님 — fix gravity 98.1$- (두 덱 같은 글자 · 닫힌 실패)',
             d2('fix gravi all gravity 98.1$- vector 0.0 0.0 -1.0\n', 'fix gravi all gravity 98.1$- vector 0.0 0.0 -1.0\n'), D2K, {},
             ['펼칠 수 없음', '$-']),
            ('V34 v3 after_settling — 본 덱 체크포인트 앞 partition yes 1 variable dt equal 2.0e-6 (파티션 하나 = 실행 · 재개 덱에는 없음)',
             (t50.replace(TSD, 'partition yes 1 variable dt equal 2.0e-6\n' + TSD), res_after('good', MAIN50, C50, tmpl=True)), CK50, AS50,
             ['펼칠 수 없음', 'partition yes 1']),
            ('V35 본 덱 삽입 run 1 every 1 안 if 안 variable g_probe 196.2 (겹친 명령 · 재개 덱에는 그 run 이 없다)',
             (d2m.replace(PMG, PMG + 'variable g_probe equal 98.1\n')
              .replace(INS1, 'run 1 every 1 "if \'1 > 0\' then \'variable g_probe equal 196.2\'"\nunfix ins_mix\n').replace(FG, GP),
              d2r.replace(PMG, PMG + 'variable g_probe equal 98.1\n').replace(FG, GP)), D2K, {}, ['펼칠 수 없음', 'run 1 every 1']),
            ('V36 본 덱 삽입 run 1 every 1 "variable dt equal 2.0e-6" (마지막 쓰는 자리 뒤 · 끝 상태 dt = 2e-6 ↔ 재개 덱 1e-6 · 뒤 구간이 ${dt} 를 쓰면 다름)',
             (d2m.replace(INS1, 'run 1 every 1 "variable dt equal 2.0e-6"\nunfix ins_mix\n'), d2r), D2K, {},
             ['재개 지점 variable dt 다름', '끝 상태 변수 표']),
            # 아래 넷 = LIGGGHTS 자신도 오류로 끝내는 꼴 — 정적 대조가 닫힌 쪽 (KG50R-F01 문제 줄) 으로 끝나는지 (도구 오류 · 다른 까닭이 아니라)
            ('V37 순환 참조 (g = v_g+1 · fix ${g_probe} · 두 덱 같은 글자)', d2(gv('v_g_probe+1', 'FIX'), gv('v_g_probe+1', 'FIX')), D2K, {},
             ['펼칠 수 없음', '순환 참조']),
            ('V38 v_x[i] (atom 변수 원자 하나 값 · g = v_a_v[1] · 두 덱 같은 글자)',
             d2('variable a_v atom x\nvariable g_probe equal v_a_v[1]\n' + GP, 'variable a_v atom x\nvariable g_probe equal v_a_v[1]\n' + GP), D2K, {},
             ['펼칠 수 없음', '원자 하나']),
            ('V39 string 을 equal 로 다시 정의 (LIGGGHTS 오류 꼴 · 두 덱 같은 글자)',
             d2('variable g_probe string 98.1\nvariable g_probe equal 196.2\n' + GP, 'variable g_probe string 98.1\nvariable g_probe equal 196.2\n' + GP),
             D2K, {}, ['펼칠 수 없음', '다른 꼴']),
            ('V40 equal 정의 인자 둘 (variable g_probe equal 98.1 2 · LIGGGHTS 오류 꼴 · 두 덱 같은 글자)',
             d2('variable g_probe equal 98.1 2\n' + GP, 'variable g_probe equal 98.1 2\n' + GP), D2K, {}, ['펼칠 수 없음', '인자가 2 개']),
        ]
        for tag, (mt, rt), ck, kw, frags in neg:
            mp = os.path.join(tmp, 'vm.liggghts')
            with open(mp, 'w', encoding='utf-8', newline='') as f:
                f.write(mt)
            rp = os.path.join(tmp, 'vr.liggghts')
            with open(rp, 'w', encoding='utf-8', newline='') as f:
                f.write(rt)
            rc, out = deckcheck_only(script, mp, rp, ck[0], ck[1], tuple(n for n, _ in kw.get('more_decks', ())))
            bad = [l for l in out.splitlines() if l.startswith('  ✗ ') and 'KG50R-F01' in l]
            chk('%s → -C 거부 (KG50R-F01 문제 · %s)' % (tag, ' · '.join(frags)),
                rc != 0 and bad and all(any(x in l for l in bad) for x in frags), out)
            # 본 흐름 = LF 사본 (셸 awk 가 CRLF 덱의 read_restart 경로 끝 \r 을 남겨 체크포인트를 못 찾는다 — 이번 범위 밖 · -C 는 CRLF 그대로)
            r = run_case(script, None, None, res_text=rt.replace('\r\n', '\n'), trial_text=ok_log,
                         main_bytes=mt.replace('\r\n', '\n').encode('utf-8'), ckpt=ck[0], extra=('-T',), **kw)
            chk('%s → 본 흐름 (-T) 시험 0 · 본 0 (정적 대조 실패 · KG50R-F01)' % tag,
                not r['trial'] and not r['main'] and '✗ 재개 덱 정적 대조 실패' in r['out'] and 'KG50R-F01' in r['out'], r['out'])
        with open(os.path.join(CX_DECK, 'after_settling_baseline.liggghts'), encoding='utf-8') as f:
            asbt = f.read()
        with open(MAIN, encoding='utf-8') as f:
            tmain = f.read()
        pos = [
            ('V1 받은 D2 덱 그대로 (timestep ${dt} · 템플릿 반지름 셋 = 상수 · print · if 의 ${n_ins} = 값 대조 밖)', (d2m, d2r), D2K,
             '그 자리 치환 대조 (10-30 KG50R-F01): 명령 4 개 · 치환 4 곳'),
            ('V1b 보관 after_settling 기준선 (Codex archived_after_settling_baseline = 리포 고정물 · 판 높이 블록 = write_restart 뒤 구간)',
             (tmain, asbt), (CKPT_AS, 200001), '그 자리 치환 대조 (10-30 KG50R-F01): 명령 4 개 · 치환 4 곳'),
            ('V1c v3 50×50 after_settling (템플릿 줄 포함)', (t50, res_after('good', MAIN50, C50, tmpl=True)), CK50,
             '그 자리 치환 대조 (10-30 KG50R-F01): 명령 4 개 · 치환 4 곳'),
            ('V1d Codex 합성 대조군 (dt 1e-6 한 번 · timestep ${dt})', (TOK_M, TOK_R), TCK, '그 자리 치환 대조 (10-30 KG50R-F01): 명령 1 개 · 치환 1 곳'),
            ('V10 안전한 생략 (쓰기 전에 덮인 정의 196.2 만 뺌)', d2(gv('196.2', '98.1', 'FIX'), gv('98.1', 'FIX')), D2K, '명령 5 개 · 치환 5 곳'),
            ('V11 상수 사슬 (a 49.05 · b = ${a}*2 · fix v_b · 두 덱 같음)',
             d2('variable a_g equal 49.05\nvariable b_g equal ${a_g}*2\nfix gravi all gravity v_b_g vector 0.0 0.0 -1.0\n',
                'variable a_g equal 49.05\nvariable b_g equal ${a_g}*2\nfix gravi all gravity v_b_g vector 0.0 0.0 -1.0\n'), D2K,
             '명령 5 개 · 치환 5 곳'),
            ('V17 string 상수 글 (variable g_s string 98.1 · fix ${g_s})',
             d2('variable g_s string 98.1\nfix gravi all gravity ${g_s} vector 0.0 0.0 -1.0\n',
                'variable g_s string 98.1\nfix gravi all gravity ${g_s} vector 0.0 0.0 -1.0\n'), D2K, '명령 5 개 · 치환 5 곳'),
            ('V18 따옴표 안 ${dt} (그 자리 치환 아님 · 두 덱 같은 글자 · 쓰지 않음)',
             d2(NI + 'variable dq equal "${dt}*2"\n', NI + 'variable dq equal "${dt}*2"\n', NI), D2K, '명령 4 개 · 치환 4 곳'),
            ('V19 정해진 수학 함수 · 비교 연산자 (g = sqrt(9623.61)*(2>=1) · fix ${g_probe} · 두 덱 같음)',
             d2(gv('sqrt(9623.61)*(2>=1)', 'FIX'), gv('sqrt(9623.61)*(2>=1)', 'FIX')), D2K, '명령 5 개 · 치환 5 곳'),
            ('V30 v_ 로 쓰는 string 수 글 (g_s string 98.1 · g = v_g_s*1 · fix ${g_probe})',
             d2('variable g_s string 98.1\nvariable g_probe equal v_g_s*1\n' + GP, 'variable g_s string 98.1\nvariable g_probe equal v_g_s*1\n' + GP),
             D2K, '명령 5 개 · 치환 5 곳'),
            ('V31 v_ 로 쓰는 string = 정의 때 넣은 equal 값 (a 98.1 · s = ${a} · g = v_s*1 · fix ${g_probe})',
             d2('variable a_g equal 98.1\nvariable g_s string ${a_g}\nvariable g_probe equal v_g_s*1\n' + GP,
                'variable a_g equal 98.1\nvariable g_s string ${a_g}\nvariable g_probe equal v_g_s*1\n' + GP), D2K, '명령 6 개 · 치환 6 곳'),
            ('V33 string = 띄어 쓴 equal 값 (a "49.05 * 2" · s = ${a} · fix ${g_s} — LIGGGHTS 가 넣는 것은 수 98.1)',
             d2('variable a_g equal "49.05 * 2"\nvariable g_s string ${a_g}\nfix gravi all gravity ${g_s} vector 0.0 0.0 -1.0\n',
                'variable a_g equal "49.05 * 2"\nvariable g_s string ${a_g}\nfix gravi all gravity ${g_s} vector 0.0 0.0 -1.0\n'), D2K,
             '명령 6 개 · 치환 6 곳'),
            ('V27 판 메시 fix 하나 (scale ${msc} = 1.0 상수 · 재개 덱 file 이름만 다름 · 파일 있음)',
             d2('variable msc equal 1.0\nfix wmesh all mesh/surface file wall_kg50.stl type 1 scale ${msc}\n' + FG,
                'variable msc equal 1.0\nfix wmesh all mesh/surface file wall_kg50_r4.stl type 1 scale ${msc}\n' + FG), D2K,
             '명령 5 개 · 치환 5 곳', ('wall_kg50_r4.stl',)),
        ]
        for row in pos:
            tag, (mt, rt), ck, frag = row[:4]
            mp = os.path.join(tmp, 'vm.liggghts')
            with open(mp, 'w', encoding='utf-8', newline='') as f:
                f.write(mt)
            rp = os.path.join(tmp, 'vr.liggghts')
            with open(rp, 'w', encoding='utf-8', newline='') as f:
                f.write(rt)
            rc, out = deckcheck_only(script, mp, rp, ck[0], ck[1], row[4] if len(row) > 4 else ())
            chk('%s → -C 통과 (문제 0 · %s)' % (tag, frag), rc == 0 and '통과 (문제 0)' in out and frag in out, out)
        # 본 흐름 대조군 — 음성 장면과 같은 덱 묶음 · 같은 꾸밈 (체크포인트 · 원 로그) 에서 정적 대조 통과 · 시험 냄 (음성의 시험 0 = 값 대조 때문)
        for tag, (mt, rt), ck, kw in (('V1e 받은 D2 덱 그대로', (d2m, d2r), D2K, {}),
                                      ('V1f Codex 합성 대조군', (TOK_M, TOK_R), TCK, {}),
                                      ('V1g v3 after_settling 그대로', (t50, res_after('good', MAIN50, C50, tmpl=True)), CK50, AS50)):
            r = run_case(script, None, None, res_text=rt.replace('\r\n', '\n'), trial_text=ok_log,
                         main_bytes=mt.replace('\r\n', '\n').encode('utf-8'), ckpt=ck[0], extra=('-T',), **kw)
            chk('%s · 본 흐름 (-T) → 정적 대조 통과 · 시험 냄 (값 대조가 정상 덱을 막지 않음 · 음성 장면의 대조군)' % tag,
                r['trial'] and not r['main'] and '재개 덱 정적 대조: 통과' in r['out'], r['out'])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    # ── VP: 정적 대조 남은 구멍 (10-30 KG50R-F01 2 판 · 사전 공격 R1–R8) — 위 group_vp ──
    group_vp(script, chk, grp)
    # ── RB: 러너 결속 (10-30 KG50R-F02) — 위 group_rb ──
    group_rb(script, chk, grp)

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
        #   after_settling 정상 출력이 그대로인지.  10-28 밤 새 묶음 (R G X L I Q9 Y) 은 새 행동을 시험하려고 만든 장면이라 보고만 한다
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
