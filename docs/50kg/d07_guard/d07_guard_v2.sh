# d07_guard_v2.sh — D0.7-50 이어 돌리기 (정착 끝 restart_after_settling.bin → 안정화 · 압축 · 이완 · 끝) 지킴이 · 창 B 에서 먼저 실행
#   nohup bash ~/d07_guard_v2.sh > ~/d07_guard_v2.log 2>&1 &  → tail -f ~/d07_guard_v2.log 에 '이제 창 A' 가 뜨면 창 A 에서 본 명령
#   v1 (10-30 · 정착까지 한 건) 과 같은 손 확인 ① ② ④ · v1 의 ⑤ (판 STL = 정착 끝에서 정지) 는 없다 — 이어 돌리기는 끝까지 둔다
#   ① 원 로그 원본 (멈춘 폴더 kg50_d07_b50.main1031) ↔ 도구 사본 sha256 · cmp   ② 새 시도 영수증 = 승인값 (다르면 그 시험 job 만 취소)
#   ④ 본 job LMP_IDENTITY = lmp_mpi · 덱 · 체크포인트 (restart_after_settling.bin) 승인값 (다르면 본 job 취소) · 5 분 뒤 큐에 있는지 한 번 더
#   취소는 이 시도 폴더의 job 번호만 · 끝나면 화면을 통째로 복사해 Claude 에 붙여 넣기
#   승인값 네 자리 (OLDATT · OKR · OKD · OKL) = 10-31 -T 보고에서 채움 · Codex GO 판정문의 값과 같아야 한다 — 채우기 전에는 아무것도 안 한다
L=$HOME/dem_test; C=kg50_d07_b50; SUF=main1031; W=$L/$C
OLDATT=__FILL_T_ATTEMPT__
OKR=__FILL_RECEIPT_SHA256__
OKL=__FILL_LMP_SHA256__
OKD=__FILL_DECK_SHA256__
OKK=45a838c18d19e3c1399a97f5948d52ad0995490f6a55040e6a6ffec8fecd2d70
isnum(){ case "$1" in ''|*[^0-9]*) return 1;; esac; return 0; }
is64(){ case "$1" in *[^0-9a-f]*) return 1;; esac; [ ${#1} = 64 ]; }
echo "== $(date '+%F %T') D0.7 이어 돌리기 지킴이 (v2) =="
case "$OLDATT" in attempt_r56_*) ;; *) echo "⛔ 승인값이 비었다 (OLDATT) — Claude 에게"; exit 1;; esac
for v in "$OKR" "$OKL" "$OKD" "$OKK"; do is64 "$v" || { echo "⛔ 승인값이 비었거나 꼴이 아니다 [$v] — Claude 에게"; exit 1; }; done
echo "① 원 로그 원본 ↔ 도구 사본"
sha256sum $W.$SUF/log.liggghts $W/log.liggghts.$SUF
ls -l $W.$SUF/log.liggghts $W/log.liggghts.$SUF | awk '{print "   " $5 " B " $NF}'
if cmp -s $W.$SUF/log.liggghts $W/log.liggghts.$SUF; then echo "   cmp 같음"
else echo "   ⛔ cmp 다름 — 창 A 실행하지 말고 Claude 에게"; exit 1; fi
OLD=" "; for d in $W/attempt_r56_*; do [ -d "$d" ] && OLD="$OLD${d##*/} "; done
echo "② 기존 시도:$OLD(안 읽음)"
[ "$OLD" = " $OLDATT " ] || { echo "   ⛔ 기존 시도가 예상 (-T 시도 $OLDATT 하나) 과 다름 — 창 A 를 이미 돌렸으면 Ctrl-C · Claude 에게"; exit 1; }
echo "   ▶ 이제 창 A 에서 본 명령"
n=0
while :; do
  NEW=""
  for d in $W/attempt_r56_*; do b=${d##*/}; case "$OLD" in *" $b "*) ;; *) [ -d "$d" ] && NEW="$NEW $b";; esac; done
  set -- $NEW
  [ $# -gt 1 ] && { echo "   ⛔ 새 시도 폴더가 $# 개 ($NEW) — 창 A Ctrl-C 하고 Claude 에게"; exit 1; }
  [ $# = 1 ] && [ -s "$W/$1/job_t.txt" ] && break
  n=$((n+1)); [ $n -gt 1200 ] && { echo "   ⏹ 1시간 동안 새 시험 없음 — 창 A 확인"; exit 1; }
  sleep 3
done
A=$1; J=$(cat $W/$A/job_t.txt); H=$(sha256sum < $W/$A/main_inputs.sha256 | cut -c1-64)
echo "   새 시도 $A · 시험 job $J · 영수증 sha256 $H"
if [ "$H" = "$OKR" ]; then echo "   ✅ 영수증 = 승인값 ${OKR:0:8}…"
else
  echo "   ⛔ 영수증이 승인값과 다름 — 시험 job $J 취소 (본 제출로 못 넘어감)"
  if isnum "$J"; then scancel $J; else echo "   job 번호 꼴 아님 — 창 A 를 Ctrl-C"; fi
  exit 1
fi
echo "③ 시험 · 도구 판정 기다림 (G0–G3)"
while :; do grep -q '^결정' $W/$A/result.txt 2>/dev/null && break; sleep 10; done
sed -n '1,3p' $W/$A/result.txt
[ -s $W/$A/main_job.txt ] || { echo "   본 job 없음 — 위 줄을 Claude 에게"; exit 0; }
JM=$(cat $W/$A/main_job.txt); O=$L/logs/output_${C}_r56_$JM.out
isnum "$JM" || { echo "   ⛔ 본 job 번호 꼴 아님 [$JM] — Claude 에게"; exit 1; }
echo "④ 본 job $JM — 시작 (LMP_IDENTITY 줄) 기다림"
while :; do grep -q '^LMP_IDENTITY' $O 2>/dev/null && break; sleep 15; done
I=$(grep -m1 '^LMP_IDENTITY' $O); K=0
case "$I" in *"sha256=$OKL"*) K=$((K+1));; esac
case "$I" in *"input_${C}_r56.liggghts sha256=$OKD"*) K=$((K+1));; esac
case "$I" in *"restart_after_settling.bin sha256=$OKK"*) K=$((K+1));; esac
echo "   $I"
grep -q '^LMP_IDENTITY_MISMATCH' $O && K=0
if [ $K = 3 ]; then echo "   ✅ 본 job 신원 = 승인값 셋 (lmp_mpi · 덱 · 체크포인트)"
else echo "   ⛔ 본 job 신원 $K/3 — 본 job $JM 취소"; scancel $JM; exit 1; fi
sleep 300
if squeue -h -j $JM -o %T 2>/dev/null | grep -q .; then
  echo "   🟢 $(date '+%F %T') 본 job $JM 큐에 있음 ($(squeue -h -j $JM -o %T 2>/dev/null)) — 끝까지 둔다 · 출력 $O"
else
  echo "   ⛔ $(date '+%F %T') 본 job $JM 이 5 분 안에 큐에서 사라짐 — 출력 끝 줄을 Claude 에게"; tail -n 5 $O 2>/dev/null; exit 1
fi
echo "== 끝 · 이 화면 전체를 Claude 에 =="
