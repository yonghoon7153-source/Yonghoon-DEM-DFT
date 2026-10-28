#!/bin/bash
# run_tests.sh — DEM1 도구(tool/th_grid.sh) 납품 전 테스트. 진짜 LIGGGHTS + Slurm 흉내. ✅/❌ 집계, 실패 0 이어야 납품.
#   bash run_tests.sh all        chain ops freeze qos paste (~15분, 2코어 기준)
#   bash run_tests.sh insert     실제 크기 삽입 6케이스 (계획 코어, 무거움 ~3분+)
#   bash run_tests.sh chain|ops|freeze|qos|paste
#   TOOL=다른/스크립트.sh 로 바꿔 테스트 가능 · LMP=/path/lmp_mpi · WORK=작업폴더
. "$(cd "$(dirname "$0")" && pwd)/kit_lib.sh"
setup_bin

t_chain(){ hdr "chain: 시간제한 12초로 여러 번 끊겨도 끝까지 · 이완 step 정확 · 남은 링크 자동 취소 · 잡 안 예약 env"
  local C=th3_85 S4 FE
  export MOCK_TLIMIT=12 MOCK_QOS_CAP=4; fresh chain $C
  chk "gen 표 (코어 합 60 / 60)" grepq "코어 합 60 / 60" $T/gen.out
  tg start > $T/start.out 2>&1; chk "start → 첫 링크 + 다음 링크" grepq "▶ $C: job" $T/start.out
  waitq 600; S4=$(s4 $C); FE=$(fe $C)
  chk "Finished" grepq "^====== $C Finished" "$(lastlog $C)"
  chk "링크 3개 이상 (시간제한에 끊겨 이어감)" [ "$(logs $C | wc -l)" -ge 3 ]
  chk "첫 링크 삽입은 z 분할 1x1x2" grepq "1 by 1 by 2 MPI processor grid" "$(logs $C | head -1)"
  chk "삽입 개수 확인 줄" grepq "삽입 .*개 (예상" "$(logs $C | head -1)"
  chk "본 런은 x·y 분할" grep -aqE "(2 by 1|1 by 2) by 1 MPI processor grid" "$(lastlog $C)"
  chk "ERROR 0" [ "$(errs $C)" = 0 ]
  chk "원자 수 하나로 일정" [ "$(natoms $C)" = 1 ]
  chk "PHASE 2 시작 3002" [ "$(s2 $C)" = 3002 ]
  chk "이완 1500 step 정확 (S4 $S4 → 끝 $FE)" [ "$((S4+1500))" = "$FE" ]
  chk "큐 비었음 (남은 링크 자동 취소)" qempty
  chk "잡 안에서 다음 링크 예약함" [ "$(sacct | grep -c '|in-job:')" -ge 1 ]
  chk "잡 안 예약 env: SLURM_CONF 유지 · SLURM_JOB_ID 지움" [ "$(sacct | awk -F'|' '$5 ~ /^in-job/ && ($6 != "conf" || $7 != "clean")' | wc -l)" = 0 ]
  cleanup; unset MOCK_TLIMIT; }

t_ops(){ hdr "ops: cores · 중복 제출 · stop/resume"
  local C=th3_85 i O
  export MOCK_QOS_CAP=6 PSPEED=0.2; unset MOCK_TLIMIT; fresh ops $C
  tg start > /dev/null 2>&1; waitfor '[ "$(ck th3_85)" -ge 9000 ] 2>/dev/null' 300
  for i in 1 2 3 4 5; do O=$(TH_GUARD_S=0 tg cores $C:3 2>&1); echo "$O" | grep -q "▶ $C" && break; sleep 1; done
  chk "cores $C:3 → 최신 체크포인트에서 다시 제출" grepq "▶ $C" <(echo "$O")
  waitfor '[ -n "$(squeue -u x -h -t R -o %i)" ]' 60; sleep 10
  chk "새 잡 3코어 x·y" grep -aqE "(3 by 1|1 by 3) by 1 MPI processor grid" "$(lastlog $C)"
  ( cd $H/dem_test && sbatch --parsable $C/run_$C.sh > $T/dup.id ); sleep 8
  chk "사람이 러너를 또 sbatch → 나중 잡은 바로 끝" grepq "먼저 돌고 있음" "$H/dem_test/logs/output_${C}_$(cat $T/dup.id).out"
  chk "RUNNING 은 하나" [ "$(squeue -u x -h -t R -o %j | grep -c "^$C$")" = 1 ]
  tg stop $C > $T/stop.out 2>&1
  chk "stop → 큐 비움" qempty
  chk "stop → ⛔ 표시" grepq "사용자 stop" $H/.th_grid/$C.stop
  tg resume $C:2 > $T/resume.out 2>&1; waitq 600
  chk "resume → Finished" grepq "^====== $C Finished" "$(lastlog $C)"
  chk "resume 뒤 이완 정확" [ "$(( $(s4 $C) + 1500 ))" = "$(fe $C)" ]
  hdr "ops: LIGGGHTS ERROR → ⛔ + 다음 링크 취소"
  fresh ops2 $C; export INJECT_DIR=$T; sed -i "1a export PATH=$WORK/binw:\$PATH INJECT_DIR=$T" $H/.bashrc
  tg start > /dev/null 2>&1; waitfor '[ "$(ck th3_85)" -ge 6000 ] 2>/dev/null' 300; tg stop $C > /dev/null 2>&1
  touch $T/inject_error; tg resume $C > /dev/null 2>&1; waitq 120
  chk "ERROR → ⛔ 표시" grepq "LIGGGHTS 에러" $H/.th_grid/$C.stop
  chk "ERROR → 큐 비움 (다음 링크 취소)" qempty
  hdr "ops: 조용한 실패 반복 → 3링크째 진전 없음으로 멈춤"
  rm -f $T/inject_error; touch $T/inject_silent; tg resume $C > /dev/null 2>&1; waitq 240
  chk "진전 없음 ⛔" grepq "진전 없음" $H/.th_grid/$C.stop
  chk "큐 비움" qempty
  rm -f $T/inject_silent; unset INJECT_DIR
  hdr "ops: int32 가드 (삽입 개수 과장)"
  fresh ops3 $C; sed -i 's/^N_TOTAL=.*/N_TOTAL=200000000/' $H/dem_test/$C/th_case.txt
  chk "resume 거절" grepq "int32" <(tg resume $C 2>&1)
  chk "start 거절" grepq "int32" <(tg start 2>&1)
  chk "제출 안 됨" qempty
  cleanup; unset PSPEED; }

freeze(){ # K → 참조 런 파일을 step K 까지만 남긴 케이스 상태 (덱·러너는 gen 것 그대로)
  local K=$1 A=$H/dem_test/$C f s
  rm -rf $A/restart_$C $A/post_$C $A/plate_$C*.stl $A/input_${C}_rs*.liggghts $A/plan_* $H/.th_grid/$C.* $H/dem_test/logs/*
  cp -a $R/restart_$C $R/post_$C $A/; [ $K -ge 3002 ] && cp $R/plate_$C.stl $A/
  for f in $A/restart_$C/restart_*_*.bin $A/post_$C/*; do s=$(echo $f | sed -nE 's/.*_([0-9]+)\.(bin|stl|liggghts)$/\1/p'); [ -n "$s" ] && [ $s -gt $K ] && rm -f $f; done
  [ $K -lt 3001 ] && rm -f $A/restart_$C/restart_after_settling.bin
  awk -v k=$K '$1~/^[0-9]+$/ && NF>=3 && $1+0>k {exit} {print}' $R/log_ref.out > $H/dem_test/logs/output_${C}_400100.out; }
dryk(){ ( . <(head -n -1 $H/th_grid.sh); dry $C; echo "RC=$? MODE=$MODE CK=$CK · $INFO $ERRM" ); }

t_freeze(){ hdr "freeze: 끊김 없는 참조 런 → step K 에서 멈춘 상태 만들어 모드·남은 몫 · 잘린 체크포인트 · 로그 없음 · 잡 안 sbatch 막힘"
  local C=th3_85 S4R FER KC KR O L
  export MOCK_QOS_CAP=4; unset MOCK_TLIMIT PSPEED; fresh freeze $C
  R=$WORK/ref; rm -rf $R; mkdir -p $R; cp $H/dem_test/$C/input_$C.liggghts $R/
  ( cd $R && mpirun --oversubscribe --bind-to none -np 2 $LMP -in input_$C.liggghts > log_ref.out 2>&1 )
  S4R=$(awk '/^====== PHASE 4: RELAXATION ======$/{f=1;next} f && $1~/^[0-9]+$/ && NF>=4 {print $1; exit}' $R/log_ref.out); FER=$(awk '$1~/^[0-9]+$/ && NF>=4 {s=$1} END{print s}' $R/log_ref.out)
  chk "참조 런 Finished (S4 $S4R · 끝 $FER)" grepq "^====== $C Finished" $R/log_ref.out
  KC=$(( (S4R-1)/500*500 )); KR=$(( (S4R/500+1)*500 ))
  freeze 1;     O=$(dryk); echo "  K=1     $O" | cut -c1-150;   chk "K=1 → 체크포인트 없음 (삽입부터)" grepq "RC=2" <(echo "$O")
  freeze 1500;  O=$(dryk); echo "  K=1500  $O" | cut -c1-150;   chk "K=1500 → settling 남은 1501" grepq "MODE=settling CK=1500 .*PHASE 1 남은 1501" <(echo "$O")
  freeze 3001;  O=$(dryk); echo "  K=3001  $O" | cut -c1-150;   chk "K=3001 → after_settling" grepq "MODE=after_settling" <(echo "$O")
  freeze 4000;  O=$(dryk); echo "  K=4000  $O" | cut -c1-150;   chk "K=4000 → stabilize 남은 1002" grepq "MODE=stabilize CK=4000 .*PHASE 2 남은 1002" <(echo "$O")
  freeze 10000; O=$(dryk); echo "  K=10000 $O" | cut -c1-150;   chk "K=10000 → compress" grepq "MODE=compress CK=10000" <(echo "$O")
  freeze $KC;   O=$(dryk); echo "  K=$KC $O" | cut -c1-150;     chk "K=$KC (S4 직전) → compress" grepq "MODE=compress CK=$KC" <(echo "$O")
  freeze $KR;   O=$(dryk); echo "  K=$KR $O" | cut -c1-150;     chk "K=$KR (S4 직후) → relax 남은 $((1500-KR+S4R))" grepq "MODE=relax CK=$KR .*이완 남은 $((1500-KR+S4R))" <(echo "$O")
  freeze 10000; f=$H/dem_test/$C/restart_$C/restart_compress_10000.bin; truncate -s $(( $(stat -c %s $f) / 2 )) $f; O=$(dryk)
  chk "50% 잘린 최신 체크포인트 → 건너뛰고 9500" grepq "CK=9500 .*comp10000작음" <(echo "$O")
  freeze 10000; f=$H/dem_test/$C/restart_$C/restart_compress_10000.bin; s=$(stat -c %s $f); dd if=/dev/zero of=$f bs=1 count=70000 seek=$((s-70000)) conv=notrunc 2>/dev/null; O=$(dryk)
  chk "끝 64KB 가 0 → 건너뛰고 9500" grepq "CK=9500 .*comp10000빔" <(echo "$O")
  freeze $((KR+500)); rm -f $H/dem_test/logs/*; O=$(dryk)
  chk "이완 중인데 로그 없음 → 멈춤 (남은 몫 모름)" grepq "RC=1 .*PHASE 4 시작 step 을 못 찾음" <(echo "$O")
  hdr "freeze: 끝까지 — stabilize(4000) · relax($KR) · 80% 잘린 체크포인트(잡 안 rcheck)"
  freeze 4000; tg resume $C > /dev/null 2>&1; waitq 300; L=$(lastlog $C)
  chk "K=4000 → Finished · 이완 정확" [ "$(grep -ac "^====== $C Finished" $L)" = 1 -a "$(( $(s4 $C) + 1500 ))" = "$(fe $C)" ]
  freeze $KR; tg resume $C > /dev/null 2>&1; waitq 300
  chk "K=$KR → 이완만 남은 만큼 → 끝 step = 참조 $FER" [ "$(fe $C)" = "$FER" ]
  freeze 10000; f=$H/dem_test/$C/restart_$C/restart_compress_10000.bin; truncate -s $(( $(stat -c %s $f) * 8 / 10 )) $f
  tg resume $C > /dev/null 2>&1; waitq 300; L=$(lastlog $C)
  chk "80% 잘린 체크포인트 → 잡 안 1코어 read_restart 가 걸러냄" grepq "못 읽음" $L
  chk "못 읽은 목록에 기록" grepq "restart_compress_10000.bin" $H/.th_grid/$C.bad
  chk "이전 체크포인트(9500)로 끝까지" grepq "^====== $C Finished" $L
  hdr "freeze: 잡 안 sbatch 막힘 + 시간제한 8초 → 로그인에서 건 2링크까지만 + 경고, resume 하면 이어감"
  freeze 10000; export MOCK_SBATCH_FAIL_IN_JOB=1 MOCK_TLIMIT=8; tg resume $C > /dev/null 2>&1; waitq 120
  chk "다음 링크 예약 실패 경고" grep -aq "다음 링크 예약 실패" $(logs $C)
  chk "링크 2개로 멈춤 · 큐 비움" qempty
  chk "watch: 멈춤→resume" grepq "멈춤→resume" <(tg watch)
  unset MOCK_SBATCH_FAIL_IN_JOB MOCK_TLIMIT; tg resume $C > /dev/null 2>&1; waitq 300
  chk "resume → Finished" grepq "^====== $C Finished" "$(lastlog $C)"
  cleanup; }

t_qos(){ hdr "qos: 2케이스 · QoS 2코어(하나씩) · 시간제한 10초 → 번갈아 끊기며 둘 다 끝까지"
  local C
  export MOCK_TLIMIT=10 MOCK_QOS_CAP=2; fresh qos th3_85 th45_85
  tg start > $T/start.out 2>&1
  chk "QoS 상한으로 대기하는 잡 있음" grepq "QOSMaxCpuPerUserLimit" $T/start.out
  waitq 900
  for C in th3_85 th45_85; do
    chk "$C Finished" grepq "^====== $C Finished" "$(lastlog $C)"
    chk "$C ERROR 0 · 원자 수 일정" [ "$(errs $C)" = 0 -a "$(natoms $C)" = 1 ]
    chk "$C 이완 정확" [ "$(( $(s4 $C) + 1500 ))" = "$(fe $C)" ]
  done
  chk "큐 비었음" qempty
  cleanup; unset MOCK_TLIMIT; }

t_paste(){ hdr "paste: 블록 만들기 · 대화형 붙여넣기 왕복 · 1글자 깨짐 · CRLF · 실제 코어로 start"
  local BL=$WORK/paste_block.txt
  cp "$TOOL" $WORK/th_grid.sh; bash $KIT/../tool/make_block.sh $WORK/th_grid.sh "bash ~/th_grid.sh gen" > /dev/null; mv $WORK/th_grid_block.txt $BL
  [ -s $KIT/../tool/th_grid_block.txt ] && [ "$TOOL" = "$(cd $KIT/../tool && pwd)/th_grid.sh" ] && chk "make_block 결과 = tool/th_grid_block.txt" cmp -s $BL $KIT/../tool/th_grid_block.txt
  export MOCK_QOS_CAP=0; newhome paste; rm -f $H/th_grid.sh
  ( cd $H && timeout 120 bash --norc -i < $BL > $T/paste.out 2>&1 )
  chk "붙여넣기 왕복 = 원본" cmp -s $H/th_grid.sh "$TOOL"
  chk "gen 실행됨" grepq "코어 합 60 / 60" $T/paste.out
  tg start > $T/start.out 2>&1
  chk "start → 6케이스 x 2링크 = 12잡 (QoS 0 이라 대기)" [ "$(squeue -u x -h | wc -l)" = 12 ]
  scancel $(squeue -u x -h -o %i) 2>/dev/null; sleep 1
  newhome paste2; rm -f $H/th_grid.sh; sed '0,/^mt(){/s//mt (){/' $BL > $T/bad.txt
  ( cd $H && timeout 60 bash --norc -i < $T/bad.txt > $T/bad.out 2>&1 )
  chk "1글자 깨진 붙여넣기 → md5 게이트가 막음" grepq "붙여넣기가 깨짐 (md5 다름) — 아무것도 안 함" $T/bad.out
  chk "깨졌을 땐 아무것도 안 만듦" [ -z "$(ls $H/dem_test | grep '^th')" ]
  newhome paste3; rm -f $H/th_grid.sh; sed 's/$/\r/' $BL > $H/th_grid_block.txt
  ( cd $H && sed -i 's/\r$//' ~/th_grid_block.txt && bash ~/th_grid_block.txt > $T/crlf.out 2>&1 )
  chk "CRLF 로 깨진 파일도 sed 로 복구 → 원본과 같음" cmp -s $H/th_grid.sh "$TOOL"
  cleanup; }

t_insert(){ hdr "insert: 실제 크기 6케이스 삽입 (계획 코어 · z 분할) → 종류별 개수"
  local C N D P
  newhome insert; ( cd $H && bash ~/th_grid.sh gen > $T/gen.out 2>&1 )
  for C in th3_85 th3_80 th3_75 th45_85 th45_75 th9_80; do
    N=$(sed -nE 's/^#SBATCH +-n +([0-9]+).*/\1/p' $H/dem_test/$C/run_$C.sh); D=$T/ins_$C; mkdir -p $D; cp $H/dem_test/$C/input_${C}_ins.liggghts $D/
    echo 'write_dump all custom ins_types.txt id type radius x y z' >> $D/input_${C}_ins.liggghts
    ( cd $D && mpirun --oversubscribe --bind-to none -np $N $LMP -in input_${C}_ins.liggghts > log.out 2>&1 )
    P=$(python3 - $D/ins_types.txt $H/dem_test/th_manifest.csv $C <<'PY'
import sys, collections
L = open(sys.argv[1]).read().splitlines(); i = [k for k, x in enumerate(L) if x.startswith('ITEM: ATOMS')][0]
c = collections.Counter(x.split()[1] for x in L[i + 1:]); n = sum(c.values())
for l in open(sys.argv[2]).read().splitlines()[1:]:
    f = l.split(',')
    if f[0] == sys.argv[3]: e = [float(f[5]), float(f[6]), float(f[7]), float(f[8])]
ok = abs(c['1'] - e[0]) <= max(3, 0.03 * e[0]) and abs(c['2'] - e[1]) <= max(3, 0.01 * e[1]) and abs(c['3'] - e[2]) <= max(10, 0.001 * e[2]) and abs(n - e[3]) <= max(10, 0.001 * e[3])
print(('OK' if ok else 'BAD') + f' P {c["1"]}/{e[0]:.1f} S {c["2"]}/{e[1]:.1f} SE {c["3"]}/{e[2]:.0f} 합 {n}/{e[3]:.0f}')
PY
)
    chk "$C ${N}코어 $(grep -a 'processor grid' $D/log.out | head -1 | awk '{print $1"x"$3"x"$5}') · $P" [ "${P%% *}" = OK -a "$(grep -ac 'Less insertions' $D/log.out)" = 0 ]
  done
  cleanup; }

case "${1:-all}" in
  all) t_chain; t_ops; t_freeze; t_qos; t_paste;;
  chain) t_chain;; ops) t_ops;; freeze) t_freeze;; qos) t_qos;; paste) t_paste;; insert) t_insert;;
  *) sed -n '2,6p' "$0"; exit 1;;
esac
report
