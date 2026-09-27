# ckpt_watch.sh — resume_ckpt.sh 로 이어받은 런 watch
#   bash ckpt_watch.sh r30 pse_r050_a pse_r075_a        (ROOT=… 로 루트 변경, 기본 ~/dem_test/lhs)
#   watch -n 30 bash ckpt_watch.sh r30 pse_r050_a pse_r075_a
L=${ROOT:-~/dem_test/lhs}; SFX=$1; shift; CASES="$*"
[ -n "$SFX" ] && [ -n "$CASES" ] || { echo "사용: bash ckpt_watch.sh <접미사 예: r30> <케이스…>"; exit 1; }
echo "── $SFX 재개 런 · $(date '+%m-%d %H:%M') ──"
printf "%-11s %-3s %-8s %-3s %-8s %-7s %-7s %-8s %-8s %-8s %s\n" case st elapsed ph step P_MPa P_1h step/h plate_z ckpt note
for C in $CASES; do
  W=$L/$C; N=${C}_$SFX; D=$W/input_${N}.liggghts
  read JI ST EL LF RS <<< "$(squeue -u $USER -h -n $N -o '%i %t %M %L %R' | head -1)"
  O=$(ls -t $L/logs/output_${N}_*.out 2>/dev/null | head -1)
  # step · 판 z : 이번 런이 쓴 mesh 덤프 (로그는 긴 run 도중 버퍼에 있어 늦게 보임)
  MS=$(find $W/post_$C -maxdepth 1 -name 'mesh_*.stl' -newer $W/run_${N}.sh -printf '%T@ %f\n' 2>/dev/null | sed -E 's/^([0-9]+)[.0-9]* mesh_([0-9]+)\.stl$/\2 \1/' | sort -n)
  S1=$(echo "$MS" | tail -1 | awk '{print $1}'); T1=$(echo "$MS" | tail -1 | awk '{print $2}')
  read S0 T0 <<< "$(echo "$MS" | awk -v t=$((T1-3600)) 'NF==2{d=$2-t; if(d<0)d=-d; if(b==""||d<b){b=d; s=$1; u=$2}} END{print s, u}')"
  RATE=$(awk -v a=$S0 -v b=$S1 -v c=$T0 -v d=$T1 'BEGIN{if(d-c>=600) printf "%d", (b-a)/(d-c)*3600; else print "-"}')
  PZ=$( [ -n "$S1" ] && awk '/vertex/{printf "%.5f", $4; exit}' $W/post_$C/mesh_$S1.stl || echo -)
  # 로그: 마지막 단계 · 마지막 thermo step · 압력
  PH=$(grep -a '^======' $O 2>/dev/null | grep -aoE 'PHASE [0-9]|Finished' | tail -1)
  read LS LP VS <<< "$(awk '/^ *Step +Atoms/{p=($NF=="pressMPa");c=0;for(i=1;i<=NF;i++)if($i=="CPU")c=i;q=1;next} q&&$1~/^[0-9]+$/{s=$1; if(p&&c>0&&$c+0>0){v=$NF;w=$1}} END{print s, v, w}' $O 2>/dev/null)"
  STEP=$S1; [ -n "$LS" ] && { [ -z "$STEP" ] || [ "$LS" -gt "$STEP" ]; } && STEP=$LS
  P1H=-; [ -n "${RATE//-/}" ] && [ -n "$VS" ] && P1H=$(awk -v t=$((VS-RATE)) '/^ *Step +Atoms/{p=($NF=="pressMPa");c=0;for(i=1;i<=NF;i++)if($i=="CPU")c=i;q=1;next} q&&p&&c>0&&$c+0>0&&$1~/^[0-9]+$/{d=$1-t; if(d<0)d=-d; if(b==""||d<b){b=d; v=$NF}} END{print (v==""?"-":v)}' $O)
  CK=$(ls $W/restart_$C/ 2>/dev/null | sed -nE 's/^restart_compress_([0-9]+)\.bin$/\1 &/p' | sort -n | tail -1 | cut -d' ' -f2)
  [ -z "$CK" ] && [ -s $W/restart_$C/restart_after_settling.bin ] && CK=restart_after_settling.bin
  TG=$(awk '$1=="variable" && $2=="target_press"{print $4}' $D)
  NOTE=""
  if [ -n "$ST" ]; then
    if [ "$ST" = PD ]; then NOTE="대기 $RS"
    elif [ "$PH" = "PHASE 2" ] && [ -n "${RATE//-/}" ]; then
      P2E=$(awk '/PHASE 2: STABILIZE/{p=1} p&&$1=="run"{print $2; exit}' $D); read M0 SS RR0 < $W/mode_$SFX.txt
      NOTE="P3 까지 $(awk -v r=$RATE -v e=$((SS+1+P2E)) -v s=$STEP 'BEGIN{if(e<=s) printf "곧"; else printf "~%.1fh", (e-s)/r}')"
    elif [ "$PH" = "PHASE 3" ] && [ -n "${P1H//-/}" ] && [ -n "$LP" ]; then
      NOTE=$(awk -v a=$P1H -v b=$LP -v g=$TG 'BEGIN{d=b-a; if(d>0) printf "%s MPa 까지 ~%.0fh (선형)", g, (g-b)/d; else print "압력 정체"}')
    elif [ "$PH" = "PHASE 4" ]; then NOTE="이완 중"; fi
  else
    SA=$(sacct -X -n -P --name=$N -S $(date -d "-7 days" +%F) -o JobID,State 2>/dev/null | tail -1 | awk -F"|" '{print $2" job "$1}')
    if [ "$PH" = Finished ]; then NOTE="✅ 완료 ${SA}"
    else NOTE="⛔ 꺼짐 ${SA:-큐에없음} — 재시작: $CK z=$PZ"; fi
    ST="-"
  fi
  f4(){ awk -v v="$1" 'BEGIN{if(v ~ /^[-+.0-9eE]+$/ && v ~ /[0-9]/) printf "%.4f", v; else print "-"}'; }
  CKS=$(echo "${CK:--}" | sed -E 's/^restart_compress_([0-9]+)\.bin$/\1/; s/^restart_after_settling\.bin$/settle/')
  printf "%-11s %-3s %-8s %-3s %-8s %-7s %-7s %-8s %-8s %-8s %s\n" $C "${ST:--}" "${EL:--}" "$(echo "${PH:--}" | sed 's/PHASE /P/; s/Finished/fin/')" "${STEP:--}" "$(f4 "$LP")" "$(f4 "$P1H")" "$RATE" "$PZ" "$CKS" "$NOTE"
done
echo "(step·z: 이번 런 mesh 덤프 · P: 로그의 정규 thermo, 늦게 써짐 · ckpt: 재시작점)"
