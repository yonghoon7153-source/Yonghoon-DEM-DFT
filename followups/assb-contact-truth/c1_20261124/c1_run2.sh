#!/usr/bin/env bash
# C1 2 차 격자 순서 (설계서 §5-9 · §8-5) — 단계마다 run_step.sh 기록 · rc ≠ 0 이면 그 자리에서 멈춘다 (§5-8).
# 사용: c1_run2.sh   (환경: C1 · C1_DIR · C1_RUN · C1_COPY · C1_REPO · PY · C1_T0)
set -u
: "${C1:?}" "${C1_DIR:?}" "${C1_RUN:?}" "${C1_COPY:?}" "${C1_REPO:?}" "${PY:?}" "${C1_T0:?}"
OUTROOT=${C1_OUTROOT:-$C1/out2}; OUT=$OUTROOT/grid; SPK=$OUTROOT/spikes; CSV=${C1_CSV:-$C1_DIR/run2_tables}
mkdir -p "$OUT" "$CSV"
G="$PY -I $C1_DIR/c1_grid.py"; A="$PY -I $C1_DIR/c1_analyze.py"
log() { echo "$(date -u +%H:%M:%SZ) $*" | tee -a "$C1_RUN/steps.txt"; }
one() { local n=$1; shift; "$C1_DIR/run_step.sh" "$n" "$@"; local rc=$?; log "$n rc=$rc"; return $rc; }
par() { # 병렬 단계: 이름접두 · 명령 줄들 (이름|명령)
  local pids=() names=() rc=0
  while IFS='|' read -r n cmd; do [ -z "$n" ] && continue; "$C1_DIR/run_step.sh" "$n" $cmd & pids+=($!); names+=("$n"); done
  for i in "${!pids[@]}"; do wait "${pids[$i]}"; local r=$?; log "${names[$i]} rc=$r"; [ $r -ne 0 ] && rc=$r; done
  return $rc
}
left_min() { $PY -I -c "import datetime as d,time;t0=d.datetime.strptime('$C1_T0','%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=d.timezone.utc).timestamp();print(int((t0+4*3600-time.time())//60))"; }
log "start · budget left $(left_min) min"
one 20_conv $G conv --out $OUT --spk $SPK || { log "STOP at 20_conv"; exit 3; }
par <<P || { log "STOP at 21_c1a"; exit 3; }
21_c1a_G05_Wa10|$G c1a --out $OUT --spk $SPK --shape G05 --Wa 10
21_c1a_G05_Wa0.1|$G c1a --out $OUT --spk $SPK --shape G05 --Wa 0.1
21_c1a_G2_Wa10|$G c1a --out $OUT --spk $SPK --shape G2 --Wa 10
21_c1a_G2_Wa0.1|$G c1a --out $OUT --spk $SPK --shape G2 --Wa 0.1
P
one 22_failcheck $A failcheck --out $OUT --spk $SPK || { log "STOP at 22_failcheck (rule 6)"; exit 3; }
one 23_dc $G dc --out $OUT --spk $SPK || { log "STOP at 23_dc"; exit 3; }
par <<P || { log "STOP at 24_c1b"; exit 3; }
24_c1b_Wa10|$G c1b --out $OUT --spk $SPK --Wa 10
24_c1b_Wa0.1|$G c1b --out $OUT --spk $SPK --Wa 0.1
P
one 25_failcheck $A failcheck --out $OUT --spk $SPK || { log "STOP at 25_failcheck (rule 6)"; exit 3; }
L=$(left_min); log "budget left $L min before AD (D3: AD only if ≥ 90 min)"
if [ "$L" -ge 90 ]; then
  par <<P || log "AD c1a rc≠0 (선택 팔 — 기록)"
26_ad_c1a_G05_Wa10|$G ad_c1a --out $OUT --spk $SPK --shape G05 --Wa 10
26_ad_c1a_G05_Wa0.1|$G ad_c1a --out $OUT --spk $SPK --shape G05 --Wa 0.1
26_ad_c1a_G2_Wa10|$G ad_c1a --out $OUT --spk $SPK --shape G2 --Wa 10
26_ad_c1a_G2_Wa0.1|$G ad_c1a --out $OUT --spk $SPK --shape G2 --Wa 0.1
P
  one 27_ad_dc $G ad_dc --out $OUT --spk $SPK || log "AD dc rc≠0"
  par <<P || log "AD c1b rc≠0"
28_ad_c1b_Wa10|$G ad_c1b --out $OUT --spk $SPK --Wa 10
28_ad_c1b_Wa0.1|$G ad_c1b --out $OUT --spk $SPK --Wa 0.1
P
  AD=1
else
  AD=0; log "AD skipped (budget)"
fi
one 30_analyze_c1a $A c1a --out $OUT --spk $SPK --csv $CSV || log "30 rc≠0"
one 31_analyze_c1b $A c1b --out $OUT --spk $SPK --csv $CSV || log "31 rc≠0"
[ "$AD" = 1 ] && { one 32_analyze_ad $A ad --out $OUT --spk $SPK --csv $CSV || log "32 rc≠0"; }
log "done · budget left $(left_min) min"
