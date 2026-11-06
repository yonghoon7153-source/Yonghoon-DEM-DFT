#  11-06 메모리 재기 감시 셸 (`docs/reviews/rint2_s0_mem_probe_20261106/` 묶음의 run.sh) 그대로 — 감싸개만 probe2.py (후보 검색 기록을 남김).
#  usage: bash run2.sh <L = 기록 폴더 (probe2.py 를 여기 둔다)> <W = 새 핀 작업 트리> <O = 새 출력 폴더 (없던 경로)>
L=$1; W=$2; O=$3; cd $L
$HOME/dem-venv/bin/python3 $L/probe2.py $L/stacks.txt $W/scripts/ca_s0_census.py --stage 1 --kit $HOME/sdcp/kit_SBE_vgcf100 --out $O > $L/run.log 2>&1 &
PID=$!; T0=$(date +%s); NEXT=8
AV=$(awk '/^MemAvailable/{print int($2/1048576)}' /proc/meminfo); CAP=$((AV-6)); [ $CAP -gt 46 ] && CAP=46
echo "pid=$PID cap_gb=$CAP" > $L/rss.log
while kill -0 $PID 2>/dev/null; do
  R=$(awk '/^VmRSS/{print $2}' /proc/$PID/status 2>/dev/null); R=${R:-0}; G=$((R/1048576)); T=$(( $(date +%s)-T0 ))
  echo "$T $R" >> $L/rss.log
  if [ $T -ge 20 ] && { [ $((T % 60)) -lt 5 ] || [ $G -ge $NEXT ]; }; then kill -USR1 $PID 2>/dev/null; echo "$T $G" >> $L/dumps.txt; [ $G -ge $NEXT ] && NEXT=$((G+4)); fi
  if [ $G -ge $CAP ]; then echo "$T CAP_TERM $G" >> $L/rss.log; kill -USR1 $PID 2>/dev/null; sleep 3; kill -TERM $PID 2>/dev/null; break; fi
  sleep 5
done
wait $PID; echo "rc=$?" >> $L/rss.log
