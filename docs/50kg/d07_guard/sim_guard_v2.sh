#!/bin/bash
# sim_guard_v2.sh — d07_guard_v2.sh 흉내 시험 (가짜 HOME · 가짜 scancel/squeue/sacct/sleep · LIGGGHTS · SLURM 없음)
#   bash sim_guard_v2.sh <guard_v2.sh (승인값 채운 판 또는 채우기 전 판)> <scenario> [fill]
#   fill = 승인값 네 자리를 흉내 값으로 채워서 돌린다 (채우기 전 판의 구조 시험) · 없으면 주어진 판 그대로 (채운 판 시험)
#   장면: happy · recdiff · lmpdiff · reject · cmpdiff · twonew · early · jobgone · unfilled
set -u
GRD=$1; SC=$2; FILL=${3:-}
SIM=$(mktemp -d); H=$SIM/home; B=$SIM/bin; mkdir -p $H/dem_test/logs $B
L=$H/dem_test; C=kg50_d07_b50; SUF=main1031; W=$L/$C
OLDATT=attempt_r56_1031_220500_1111
printf 'aaaa  input_kg50_d07_b50_r56.liggghts\nbbbb  restart_after_settling.bin\n' > $SIM/rec.txt
REC_SHA=$(sha256sum < $SIM/rec.txt | cut -c1-64)
LMP=$(printf lmp | sha256sum | cut -c1-64); DECK=$(printf deck | sha256sum | cut -c1-64)
CKP=45a838c18d19e3c1399a97f5948d52ad0995490f6a55040e6a6ffec8fecd2d70
if [ -n "$FILL" ] && [ "$SC" != unfilled ]; then
  sed -e "s/__FILL_T_ATTEMPT__/$OLDATT/" -e "s/__FILL_RECEIPT_SHA256__/$REC_SHA/" -e "s/__FILL_LMP_SHA256__/$LMP/" -e "s/__FILL_DECK_SHA256__/$DECK/" $GRD > $H/d07_guard_v2.sh
else cp $GRD $H/d07_guard_v2.sh; fi
mkdir -p $L/$C.$SUF $W/$OLDATT
printf 'LIGGGHTS log (흉내)\n  200002   488285\n' > $L/$C.$SUF/log.liggghts; cp $L/$C.$SUF/log.liggghts $W/log.liggghts.$SUF
cp $SIM/rec.txt $W/$OLDATT/main_inputs.sha256; echo 333999 > $W/$OLDATT/job_t.txt
[ "$SC" = cmpdiff ] && echo extra >> $W/log.liggghts.$SUF
cat > $B/scancel <<'EOF'
#!/bin/bash
echo "$*" >> "$SIMDIR/scancel.log"; rm -f "$SIMDIR/running_$1"
EOF
cat > $B/squeue <<'EOF'
#!/bin/bash
j=""; while [ $# -gt 0 ]; do [ "$1" = -j ] && j=$2; shift; done
[ -n "$j" ] && [ -e "$SIMDIR/running_$j" ] && echo RUNNING; exit 0
EOF
cat > $B/sleep <<'EOF'
#!/bin/bash
/bin/sleep 0.05
EOF
chmod +x $B/*
export SIMDIR=$SIM
# 흉내 도구 (창 A): 새 시도 → 영수증 → 시험 job → 판정 → 본 job → 신원 줄 (정착 끝 체크포인트) — 판 STL 은 보지 않는다
tool(){
  for i in $(seq 1 200); do grep -q '이제 창 A' $SIM/out.txt 2>/dev/null && break; /bin/sleep 0.05; done
  grep -q '이제 창 A' $SIM/out.txt 2>/dev/null || return
  A=$W/attempt_r56_1031_230000_4242; mkdir -p $A; /bin/sleep 0.3
  if [ "$SC" = recdiff ]; then sed 's/^aaaa/aaab/' $SIM/rec.txt > $A/main_inputs.sha256; else cp $SIM/rec.txt $A/main_inputs.sha256; fi
  [ "$SC" = twonew ] && mkdir -p $W/attempt_r56_1031_230001_9999
  echo 444444 > $A/job_t.txt; touch $SIM/running_444444; /bin/sleep 0.5
  if [ "$SC" = reject ]; then printf 'G0 1 G1 0 G2 1 G3 1\n결정: 본 제출 안 함 (G0–G3)\n' > $A/result.txt; return; fi
  rm -f $SIM/running_444444; echo 555555 > $A/main_job.txt; touch $SIM/running_555555
  printf 'G0 1 G1 1 G2 1 G3 1 · 시험 job 444444\n결정: 본 제출 job 555555\n' > $A/result.txt; /bin/sleep 0.5
  I="LMP_IDENTITY lmp_mpi sha256=$LMP input_kg50_d07_b50_r56.liggghts sha256=$DECK restart_after_settling.bin sha256=$CKP"
  [ "$SC" = lmpdiff ] && I=${I/sha256=$LMP/sha256=0$LMP}
  [ "$SC" = jobgone ] && rm -f $SIM/running_555555   # 신원 줄 전에 큐에서 사라짐 (흉내 sleep 이 0.05 s 라 순서를 고정)
  echo "$I" > $L/logs/output_${C}_r56_555555.out
  return 0
}
[ "$SC" = early ] && mkdir -p $W/attempt_r56_1031_225959_7777
tool & TP=$!
HOME=$H PATH=$B:$PATH timeout 60 bash $H/d07_guard_v2.sh > $SIM/out.txt 2>&1; RC=$?
wait $TP 2>/dev/null
echo "[$SC] rc=$RC · scancel: $(cat $SIM/scancel.log 2>/dev/null | tr '\n' ' ')"
sed 's/^/    /' $SIM/out.txt | cut -c1-170
rm -rf $SIM
