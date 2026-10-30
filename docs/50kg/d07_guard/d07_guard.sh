# d07_guard.sh — D0.7-50 본 제출 지킴이 (Codex 10-30 한 건 GO §6 ① ② ④ ⑤) · 창 B 에서 먼저 실행
#   nohup bash ~/d07_guard.sh > ~/d07_guard.log 2>&1 &  → tail -f ~/d07_guard.log 에 '이제 창 A' 가 뜨면 창 A 에서 본 명령
#   ① 원 로그 원본 ↔ 도구 사본 sha256 · cmp   ② 새 시도 영수증 = 29ff619a… (다르면 그 시험 job 만 취소)
#   ④ 본 job LMP_IDENTITY = lmp_mpi · 덱 · 체크포인트 승인값 (다르면 본 job 취소)
#   ⑤ 판 STL 이 다 써지면 (= after_settling 다 씀 · 200001) 본 job 정지 (등록 Q6) · 창을 닫으면 ⑤ 는 안 함
#   취소는 이 시도 폴더의 job 번호만 · 끝나면 화면을 통째로 복사해 Claude 에 붙여 넣기
L=$HOME/dem_test; C=kg50_d07_b50; W=$L/$C
OKR=29ff619a666f29131a9d582f27e555590316e8516dcf9d0a7d2af01715bde6fa
OKL=ee2d77261bac9e7fa4e9311c8709e74bf7583a13225a5bc35a791bef9be60a3f
OKD=8e129f421a8491975f83527f79c8418318b2af30baeedd7440cfcede2d45c5e5
OKK=aa833368651d9bf811c7b39331149ca939bfedf1bbe0511e2d66bf329fde15a8
isnum(){ case "$1" in ''|*[^0-9]*) return 1;; esac; return 0; }
echo "== $(date '+%F %T') D0.7 지킴이 =="
echo "① 원 로그 원본 ↔ 도구 사본 (Codex 가 받은 사본 = b1b298bb…6657f5 · 13475 B)"
sha256sum $W.ins1/log.liggghts $W/log.liggghts.ins1
ls -l $W.ins1/log.liggghts $W/log.liggghts.ins1 | awk '{print "   " $5 " B " $NF}'
if cmp -s $W.ins1/log.liggghts $W/log.liggghts.ins1; then echo "   cmp 같음"
else echo "   ⛔ cmp 다름 — 창 A 실행하지 말고 Claude 에게"; exit 1; fi
OLD=" "; for d in $W/attempt_r56_*; do [ -d "$d" ] && OLD="$OLD${d##*/} "; done
echo "② 기존 시도:$OLD(안 읽음)"
[ "$OLD" = " attempt_r56_1030_140521_985018 " ] || { echo "   ⛔ 기존 시도가 예상 (-T 시도 attempt_r56_1030_140521_985018 하나) 과 다름 — 창 A 를 이미 돌렸으면 Ctrl-C · Claude 에게"; exit 1; }
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
if [ "$H" = "$OKR" ]; then echo "   ✅ 영수증 = 승인값 29ff619a…"
else
  echo "   ⛔ 영수증이 승인값과 다름 — 시험 job $J 취소 (본 제출로 못 넘어감)"
  if isnum "$J"; then scancel $J; else echo "   job 번호 꼴 아님 — 창 A 를 Ctrl-C"; fi
  exit 1
fi
echo "③ 시험 · 도구 판정 기다림 (G0–G3 · 4–6 분)"
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
case "$I" in *"restart_settling_20001.bin sha256=$OKK"*) K=$((K+1));; esac
echo "   $I"
grep -q '^LMP_IDENTITY_MISMATCH' $O && K=0
if [ $K = 3 ]; then echo "   ✅ 본 job 신원 = 승인값 셋 (lmp_mpi · 덱 · 체크포인트)"
else echo "   ⛔ 본 job 신원 $K/3 — 본 job $JM 취소"; scancel $JM; exit 1; fi
P=$W/plate_$C.stl; R=$W/restart_$C/restart_after_settling.bin
echo "⑤ 정착 180,000 step (시험 속도로 약 5.3 시간 · 추정) — 판 STL 이 다 써지면 본 job $JM 정지 · $(date '+%F %T') 시작"
while :; do
  if [ -n "$(find $P -newer $W/run_${C}_r56.sh 2>/dev/null)" ] && grep -q '^endsolid plate' $P 2>/dev/null; then break; fi
  squeue -h -j $JM -o %T 2>/dev/null | grep -q . || { sleep 60; squeue -h -j $JM -o %T 2>/dev/null | grep -q . || { echo "   ⛔ 본 job $JM 이 큐에 없음 ($(date '+%F %T')) — 판 STL 전 · Claude 에게"; exit 1; }; }
  sleep 120
done
echo "   🟢 $(date '+%F %T') after_settling 다 씀 · 판 STL 생김 — 본 job $JM 정지 (등록 Q6)"
scancel $JM
sleep 60
sha256sum $R; ls -l $R | awk '{print "   " $5 " B"}'
ls $W/restart_$C/ | tail -n 4
echo "   본 job 출력 $O · 마지막 thermo 줄: $(awk 'NF>=4 && $1~/^[0-9]+$/ && $2~/^[0-9]+$/ {r=$0} END{print r}' $O)"
sacct -j $JM -X -o JobID,State,ExitCode,Elapsed 2>/dev/null
echo "   마지막 mesh 덤프: $(ls $W/post_$C/ 2>/dev/null | grep -E '^mesh_[0-9]+\.stl$' | sort -t_ -k2 -n | tail -1)"
echo "== 끝 · 이 화면 전체를 Claude 에 =="
