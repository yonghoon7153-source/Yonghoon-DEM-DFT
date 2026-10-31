# d07_guard_v2.sh — D0.7-50 이어 돌리기 (정착 끝 restart_after_settling.bin → 안정화 · 압축 · 이완 · 끝) 지킴이 · 창 B 에서 먼저 실행
#   nohup bash ~/d07_guard_v2.sh > ~/d07_guard_v2.log 2>&1 &  → tail -f ~/d07_guard_v2.log 에 '이제 창 A' 가 뜨면 창 A 에서 본 명령
#   지키는 범위 = 제출 단계뿐 (영수증 · 신원 · 처음 5 분):
#     ① 원 로그 원본 (멈춘 폴더 kg50_d07_b50.main1031) ↔ 도구 사본 sha256 · cmp
#     ② 기존 시도 폴더 집합 · -T 시도 영수증 ↔ 승인값 (영수증 sha256 · 덱 줄 · 체크포인트 줄) · 새 시도 영수증 = 승인값 (다르면 그 시험 job 만 취소)
#     ④ 본 job LMP_IDENTITY = lmp_mpi · 덱 · 체크포인트 (restart_after_settling.bin) 승인값 (다르면 본 job 취소) · 신원 줄 5 분 뒤 상태 RUNNING 확인 한 번
#   지키지 않는 것 = 그 뒤 런 전체 (안정화 · 압축 정지 판정 · 이완 · 끝 · 물리) — 끝에 읽기 전용 확인 명령 줄을 찍고 나간다 (오래 지켜보지 않는다)
#   v1 (10-30 · 정착까지) 의 ⑤ (판 STL = 정착 끝에서 정지) 는 없다 — 이어 돌리기는 끝까지 둔다
#   NP 접미사 r56 고정 (본 명령 = -n 56 · 기본 -x r56): 시도 폴더 attempt_r56_* · 덱 input_kg50_d07_b50_r56.liggghts · 출력 logs/output_kg50_d07_b50_r56_<job>.out
#   기존 시도 = 정확히 두 폴더 (집합 비교 · 순서 무관): INHERIT = 멈춘 폴더 main1031 에 들어 있던 10-30 본 호출 시도 (도구가 cp -a 로 같이 복사)
#     + OLDATT = 10-31 -T 시도.  새 시도 = 이 둘이 아닌 폴더 — 본 호출이 작업 폴더를 밀고 멈춘 폴더를 다시 복사해 INHERIT 가 다시 생겨도 새 시도로 치지 않는다
#   취소는 이 시도 폴더의 job 번호만 · 끝나면 화면을 통째로 복사해 Claude 에 붙여 넣기
#   승인값 네 자리 (OLDATT · OKR · OKL · OKD) = 10-31 -T 보고에서 채움 · Codex GO 판정문의 값과 같아야 한다 — 채우기 전에는 아무것도 안 한다
L=$HOME/dem_test; C=kg50_d07_b50; SUF=main1031; W=$L/$C
INHERIT=attempt_r56_1030_152123_2568313
OLDATT=__FILL_T_ATTEMPT__
OKR=__FILL_RECEIPT_SHA256__
OKL=__FILL_LMP_SHA256__
OKD=__FILL_DECK_SHA256__
OKK=45a838c18d19e3c1399a97f5948d52ad0995490f6a55040e6a6ffec8fecd2d70
isnum(){ case "$1" in ''|*[^0-9]*) return 1;; esac; return 0; }
is64(){ case "$1" in *[^0-9a-f]*) return 1;; esac; [ ${#1} = 64 ]; }
echo "== $(date '+%F %T') D0.7 이어 돌리기 지킴이 (v2 · 제출 단계만) =="
[[ "$OLDATT" =~ ^attempt_r56_[0-9]{4}_[0-9]{6}_[0-9]+$ ]] || { echo "⛔ 승인값이 비었거나 꼴이 아니다 (OLDATT [$OLDATT]) — Claude 에게"; exit 1; }
for v in "$OKR" "$OKL" "$OKD" "$OKK"; do is64 "$v" || { echo "⛔ 승인값이 비었거나 꼴이 아니다 [$v] — Claude 에게"; exit 1; }; done
echo "① 원 로그 원본 ↔ 도구 사본"
sha256sum $W.$SUF/log.liggghts $W/log.liggghts.$SUF
ls -l $W.$SUF/log.liggghts $W/log.liggghts.$SUF | awk '{print "   " $5 " B " $NF}'
if cmp -s $W.$SUF/log.liggghts $W/log.liggghts.$SUF; then echo "   cmp 같음"
else echo "   ⛔ cmp 다름 — 창 A 실행하지 말고 Claude 에게"; exit 1; fi
KNOWN=" $INHERIT $OLDATT "; OLD=" "; NS=0
for d in $W/attempt_r56_*; do [ -d "$d" ] || continue; b=${d##*/}; OLD="$OLD$b "; case "$KNOWN" in *" $b "*) NS=$((NS+1));; *) NS=99;; esac; done
echo "② 기존 시도:$OLD(안 읽음 · 예상 = 물려받은 $INHERIT + -T $OLDATT · 순서 무관)"
[ $NS = 2 ] || { echo "   ⛔ 기존 시도 집합이 예상 (위 두 폴더 · 그 밖 없음) 과 다름 — 창 A 를 이미 돌렸으면 Ctrl-C · Claude 에게"; exit 1; }
TR=$W/$OLDATT/main_inputs.sha256; HT=$(sha256sum < $TR 2>/dev/null | cut -c1-64); R1=$(sed -n 1p $TR 2>/dev/null); R5=$(sed -n 5p $TR 2>/dev/null); T3=0
[ "$HT" = "$OKR" ] && T3=$((T3+1))
case "$R1" in "$OKD  /"*"/$C/input_${C}_r56.liggghts") T3=$((T3+1));; esac
case "$R5" in "$OKK  /"*"/$C/restart_$C/restart_after_settling.bin") T3=$((T3+1));; esac
echo "   -T 시도 영수증 sha256 ${HT:-없음} · 1 줄 (덱) ${R1:0:12}… · 5 줄 (체크포인트) ${R5:0:12}…"
[ $T3 = 3 ] || { echo "   ⛔ -T 시도 영수증이 승인값 (영수증 ${OKR:0:8}… · 덱 ${OKD:0:8}… · 체크포인트 ${OKK:0:8}…) 과 $T3/3 — 창 A 실행하지 말고 Claude 에게"; exit 1; }
echo "   ✅ -T 시도 영수증 = 승인값 셋 (영수증 sha256 · 덱 줄 · 체크포인트 줄)"
echo "   ▶ 이제 창 A 에서 본 명령"
n=0
while :; do
  NEW=""
  for d in $W/attempt_r56_*; do b=${d##*/}; case "$KNOWN" in *" $b "*) ;; *) [ -d "$d" ] && NEW="$NEW $b";; esac; done
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
while :; do grep -q '^LMP_IDENTITY ' $O 2>/dev/null && break; sleep 15; done
sleep 15   # 신원 줄이 다 써진 뒤 읽는다 (바로 뒤 줄 = LIGGGHTS 머리 또는 MISMATCH)
I=$(grep -m1 '^LMP_IDENTITY ' $O); K=0
case "$I" in *" sha256=$OKL deck=/"*) K=$((K+1));; esac
case "$I" in *" deck=/"*"/$C/input_${C}_r56.liggghts sha256=$OKD checkpoint=/"*) K=$((K+1));; esac
case "$I" in *" checkpoint=/"*"/$C/restart_$C/restart_after_settling.bin sha256=$OKK") K=$((K+1));; esac
echo "   $I"
grep -q '^LMP_IDENTITY_MISMATCH' $O && { echo "   $(grep -m1 '^LMP_IDENTITY_MISMATCH' $O | cut -c1-300)"; K=0; }
if [ $K = 3 ]; then echo "   ✅ 본 job 신원 = 승인값 셋 (lmp_mpi · 덱 · 체크포인트)"
else echo "   ⛔ 본 job 신원 $K/3 — 본 job $JM 취소"; scancel $JM; exit 1; fi
sleep 300
QS=$(squeue -h -j $JM -o %T 2>/dev/null | head -n 1)
[ "$QS" = RUNNING ] || { sleep 60; QS=$(squeue -h -j $JM -o %T 2>/dev/null | head -n 1); }
if [ "$QS" = RUNNING ]; then
  echo "   🟢 $(date '+%F %T') 본 job $JM 상태 RUNNING (신원 줄 5 분 뒤) — 출력 $O"
else
  echo "   ⛔ $(date '+%F %T') 본 job $JM 상태 [${QS:-큐에 없음}] — 신원 줄 5 분 뒤 RUNNING 아님 · 출력 끝 줄을 Claude 에게"; tail -n 5 $O 2>/dev/null
  echo "   확인 (읽기 전용): sacct -j $JM -X -o JobID,State,ExitCode,Elapsed"; exit 1
fi
echo "   지킴이는 여기까지 = 제출 단계 (① 원 로그 · ② 시도 · 영수증 · ④ 신원 · 처음 5 분) — 그 뒤 런 (안정화 · 압축 · 이완 · 끝) 은 지키지 않는다"
echo "   확인 (읽기 전용 · 아무 때나 한 번씩): squeue -j $JM -o '%.10i %.9T %.10M %R' ; tail -n 3 $O ; sacct -j $JM -X -o JobID,State,ExitCode,Elapsed"
echo "== 끝 · 이 화면 전체를 Claude 에 =="
