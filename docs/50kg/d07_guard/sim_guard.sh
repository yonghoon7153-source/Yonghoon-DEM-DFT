#!/bin/bash
# sim_guard.sh — d07_guard_block.txt 흉내 시험 (가짜 HOME · 가짜 scancel/squeue/sacct/sleep · LIGGGHTS 없음)
#   bash sim_guard.sh <block.txt> <real_receipt> <real_test_out> <orig_log> <scenario>
set -u
BLK=$1; REC=$2; TOUT=$3; OLOG=$4; SC=$5
SIM=$(mktemp -d); H=$SIM/home; B=$SIM/bin; mkdir -p $H/dem_test/logs $B
L=$H/dem_test; C=kg50_d07_b50; W=$L/$C
mkdir -p $L/$C.ins1 $W/attempt_r56_1030_140521_985018
cp $OLOG $L/$C.ins1/log.liggghts; cp $OLOG $W/log.liggghts.ins1
cp $REC $W/attempt_r56_1030_140521_985018/main_inputs.sha256; echo 333858 > $W/attempt_r56_1030_140521_985018/job_t.txt
[ "$SC" = cmpdiff ] && echo extra >> $W/log.liggghts.ins1
cat > $B/scancel <<'EOF'
#!/bin/bash
echo "$*" >> "$SIMDIR/scancel.log"; rm -f "$SIMDIR/running_$1"
EOF
cat > $B/squeue <<'EOF'
#!/bin/bash
j=""; while [ $# -gt 0 ]; do [ "$1" = -j ] && j=$2; shift; done
[ -n "$j" ] && [ -e "$SIMDIR/running_$j" ] && echo RUNNING; exit 0
EOF
cat > $B/sacct <<'EOF'
#!/bin/bash
echo "JobID State ExitCode Elapsed (흉내)"
EOF
cat > $B/sleep <<'EOF'
#!/bin/bash
/bin/sleep 0.05
EOF
chmod +x $B/*
export SIMDIR=$SIM
# 흉내 도구 (창 A): 작업 폴더 밀기 → 새 복사 → 새 시도 → 영수증 → 시험 job → 판정 → 본 job → 신원 줄 → 정착 끝 판 STL
tool(){
  for i in $(seq 1 200); do grep -q '이제 창 A' $SIM/out.txt 2>/dev/null && break; /bin/sleep 0.05; done
  grep -q '이제 창 A' $SIM/out.txt 2>/dev/null || return
  if [ "$SC" = nomove ]; then :; else mv $W $L/$C.prev_x; mkdir -p $W; cp $OLOG $W/log.liggghts.ins1; fi
  echo run > $W/run_${C}_r56.sh; /bin/sleep 1.1   # 러너 (판 STL 보다 오래됨)
  A=$W/attempt_r56_1030_160000_4242; mkdir -p $A; /bin/sleep 0.3
  if [ "$SC" = recdiff ]; then sed 's/^8e129f42/8e129f43/' $REC > $A/main_inputs.sha256; else cp $REC $A/main_inputs.sha256; fi
  [ "$SC" = twonew ] && mkdir -p $W/attempt_r56_1030_160001_9999
  echo 444444 > $A/job_t.txt; touch $SIM/running_444444; /bin/sleep 0.5
  if [ "$SC" = reject ]; then printf 'G0 1 G1 0 G2 1 G3 1\n결정: 본 제출 안 함 (G0–G3)\n' > $A/result.txt; return; fi
  rm -f $SIM/running_444444; echo 555555 > $A/main_job.txt; touch $SIM/running_555555
  printf 'G0 1 G1 1 G2 1 G3 1 · 시험 job 444444\n결정: 본 제출 job 555555\n' > $A/result.txt; /bin/sleep 0.5
  I=$(sed -n 1p $TOUT | sed 's#input_kg50_d07_b50_r56t.liggghts sha256=94db4187093b417468ac7a2da6a0b43e5312e04507539251be45cbe2b8011ea1#input_kg50_d07_b50_r56.liggghts sha256=8e129f421a8491975f83527f79c8418318b2af30baeedd7440cfcede2d45c5e5#')
  [ "$SC" = lmpdiff ] && I=${I/sha256=ee2d7726/sha256=ee2d7727}
  echo "$I" > $L/logs/output_${C}_r56_555555.out
  [ "$SC" = jobgone ] && { /bin/sleep 0.5; rm -f $SIM/running_555555; return; }
  /bin/sleep 1.2; mkdir -p $W/restart_$C $W/post_$C; head -c 1000 /dev/urandom > $W/restart_$C/restart_after_settling.bin
  printf 'solid plate\nfacet normal 0 0 -1\n' > $W/plate_$C.stl; /bin/sleep 0.4; echo 'endsolid plate' >> $W/plate_$C.stl
  touch $W/post_$C/mesh_200000.stl
}
[ "$SC" = early ] && mkdir -p $W/attempt_r56_1030_155959_1111
HOME=$H PATH=$B:$PATH bash $BLK > $SIM/install.txt 2>&1
tool & TP=$!
HOME=$H PATH=$B:$PATH timeout 60 bash $H/d07_guard.sh > $SIM/out.txt 2>&1; RC=$?
wait $TP 2>/dev/null
echo "    install: $(tail -n 1 $SIM/install.txt | cut -c1-60)"
echo "[$SC] rc=$RC · scancel: $(cat $SIM/scancel.log 2>/dev/null | tr '\n' ' ')"
cat $SIM/out.txt | sed "s/^/    /" | cut -c1-170
rm -rf $SIM
