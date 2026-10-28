# kg50_watch.sh — 50kg/batch 4차년도 SE 입도 비교 2케이스 (ibb · 읽기 전용 감시): job · 남은시간 · 단계 · step · 압력 · 판 z · 속도 · ETA · 체크포인트 · 재개 보고 판정
#   watch -n 60 bash ~/kg50_watch.sh watch    감시 — squeue 한 번 + 파일 읽기만 (제출 · 취소 · 파일 쓰기 없음)
#   bash ~/kg50_watch.sh watch                한 번만 찍기
#   제출 · 재개는 이 도구가 하지 않는다 → ~/dem_test/scripts/resume_ckpt.sh (G0–G3) · 리포 docs/data/kg50_decks_20261027_v3_b50/README.md §3
#   폴더 = ~/dem_test/<C> (resume_ckpt.sh 작업 사본 · 삽입 중이면 원 폴더) 또는 ~/dem_test/<C>.ins1 만 (= 삽입 끝 · 재개 전)
#   resume 열 = ~/dem_test/resume_r*_*.md 중 '## <C>' 절이 있는 가장 최근 보고의 판정 (✅본제출 <job> · 🧪시험만 · ⛔ · -)
DT0=$HOME/dem_test
CASES="kg50_d07_b50 kg50_d2_b50"
HS_UM=101.98   # 고체 두께 µm — 두 케이스 같음 (리포 docs/data/kg50_decks_20261027_v3_b50/README.md §2 = 덱 머리 ⑤) · 덱 길이 = 이 값 x (덱 r_* 줄이 말하는 1 µm 의 덱 길이)
mt(){ stat -Lc %Y "$1" 2>/dev/null || echo 0; }
mz(){ awk '/vertex/{print $4; exit}' "$1" < /dev/null 2>/dev/null; }
logs_of(){ command ls -t $DT0/logs/output_$1_*.out 2>/dev/null; }
grid(){ grep -a 'processor grid' "$1" 2>/dev/null < /dev/null | tail -1 | awk '{print $1"x"$3"x"$5}'; }
lastmesh(){ command ls "$1/post_$2" 2>/dev/null | sed -nE 's/^mesh_([0-9]+)\.stl$/\1/p' | sort -n | tail -1; }
sq(){ local o i; for i in 1 2 3 4; do o=$(squeue -u $USER -h -o "%i %j %T %C %M %L %S %R" 2>/dev/null) && { printf '%s\n' "$o"; return 0; }; [ $i = 4 ] || sleep 3; done; return 1; }
thermo(){ awk '/^ *Step +Atoms/{p=($NF=="pressMPa");c=0;for(i=1;i<=NF;i++)if($i=="CPU")c=i;q=1;next} q&&$1~/^[0-9]+$/{s=$1; a=$2; if(p&&c>0&&$c+0>0)v=$NF} END{if(s=="")s="-"; if(a=="")a="-"; if(v=="")v="-"; print s, a, v}' "$1" < /dev/null 2>/dev/null; }
phase_start(){ local M=$1 L S; shift; for L in "$@"; do S=$(awk -v m="$M" '$0==m {f=1; next} f && $1~/^[0-9]+$/ && NF>=4 {print $1; exit}' "$L" < /dev/null 2>/dev/null); [ -n "$S" ] && { echo $S; return; }; done; }
fin(){ local L; for L in $(logs_of $1) "$2/log.liggghts"; do grep -aq '^====== Simulation Finished' "$L" < /dev/null 2>/dev/null && return 0; done; return 1; }
runsum(){ awk '$1=="run" && $2~/^[0-9]+$/ {s+=$2} END{if(s>0) print s}' "$1" < /dev/null 2>/dev/null; }
role(){ local s=${1#"$2"}; s=${s#_}; case "$s" in "") echo 돌고있음;; ins) echo "삽입 중";; r[0-9]*t) echo "시험 중 $s";; *) echo "돌고있음 $s";; esac; }   # 잡 이름 C · C_ins · C_r<N>t (시험) · C_r<N> (본런)
npr(){ local f; for f in $(command ls -t "$1"/run_$2_r*.sh 2>/dev/null); do case "$f" in *t.sh) continue;; esac; sed -nE 's/^#SBATCH +-n +([0-9]+).*/\1/p' "$f" < /dev/null 2>/dev/null | head -1; return; done; }
deckv(){ # 덱 → 목표압력|PHASE 4 표식 (print 글자 그대로)|이완 run|1 µm 의 덱 길이 (r_* 줄 값 ÷ 그 줄 주석의 r=… µm · 줄마다 같아야)|그 r_* 줄 수
  awk -F'"' '{ split($0, w, " ") }
    w[1]=="variable" && w[2]=="target_press" && w[3]=="equal" && tg=="" { tg=w[4] }
    w[1]=="print" && $2 ~ /PHASE 4/ && pm=="" { pm=$2; f=1; next }
    f && w[1]=="run" && w[2]+0>1 && rx=="" { rx=w[2]+0 }
    w[1]=="variable" && w[2] ~ /^r_/ && w[3]=="equal" { h=index($0,"#"); if(h>0){ c=substr($0,h); if(match(c,/r=[0-9.]+/)){ n=substr(c,RSTART+2,RLENGTH-2)+0; v=w[4]+0; if(n>0 && v>0){ u=v/n; k++; if(k==1) u0=u; d=u-u0; if(d<0) d=-d; if(d>1e-6*u0) bad=1 } } } }
    END{ uu=""; if(k>0 && bad+0==0) uu=sprintf("%g", u0); printf "%s|%s|%s|%s|%s\n", tg, pm, rx, uu, k+0 }' "$1" < /dev/null 2>/dev/null; }
verdict(){ # C → '판정|보고 이름' — 가장 최근 (mtime) ~/dem_test/resume_r*_*.md 중 '## C' 절이 있는 것의 끝 줄 · 없으면 '-|'
  local F V
  for F in $(command ls -t $DT0/resume_r*_*.md 2>/dev/null); do
    V=$(awk -v h="## $1" '$0==h {f=1; v="-"; next} /^## / {f=0} f && /^- ✅ 본 제출 job/ {v="✅본제출"; if(match($0,/job [0-9]+/)) v=v " " substr($0,RSTART+4,RLENGTH-4)} f && /^- 🧪 시험만/ {v="🧪시험만"} f && /^- ⛔/ {v="⛔"} END{print v}' "$F" < /dev/null 2>/dev/null)
    [ -n "$V" ] && { echo "$V|${F##*/}"; return; }
  done
  echo "-|"
}
padw(){ # 글자 S 를 화면 폭 W 칸까지 오른쪽 공백으로 (printf %-Ns 는 바이트를 세서 한글 · 이모지 열이 어긋남 → UTF-8 을 풀어 한글 · CJK · ✅ ⛔ 🧪 = 2칸)
  LC_ALL=C awk -v s="$1" -v w="$2" 'BEGIN{for(i=128;i<256;i++) o[sprintf("%c",i)]=i; n=length(s); d=0; i=1
    while(i<=n){c=substr(s,i,1); b=(c in o)?o[c]:0
      if(b<192){d++; i++}
      else if(b<224){d++; i+=2}
      else if(b<240){cp=(b-224)*4096+(o[substr(s,i+1,1)]-128)*64+(o[substr(s,i+2,1)]-128)
        if(cp==65039) z=0; else if((cp>=4352&&cp<=4447)||(cp>=11904&&cp<=42191)||(cp>=44032&&cp<=55203)||(cp>=63744&&cp<=64255)||(cp>=65280&&cp<=65376)||(cp>=65504&&cp<=65510)||cp==9989||cp==9940||cp==10060||cp==9203) z=2; else z=1
        d+=z; i+=3}
      else {d+=2; i+=4}}
    printf "%s", s; for(k=d;k<w;k++) printf " "}'; }
row(){ printf '%-12s %-8s %-10s %-10s %-3s %-6s %-9s %-8s %-7s %-7s %-9s %-5s %-7s %-6s %-17s %-8s ' "$@"; }

watch1(){
  local C W I D DK F LG J JN JS NP EL LEFT SS RX1 T0 NR R PDL PD PN PR P1x P2x P3x P4x P5x ROLE JL PL G PH LL LA LP LPD LS MS S1 Z LM RT TG P4M RX U UN HS ZH S4 P1 ETA CKP ER FA STT V VD VF NOW SQ SQOK HD FT
  NOW=$(date +%s); SQ=$(sq); SQOK=$?
  if [ $SQOK = 0 ]; then HD="내 코어 R $(printf '%s\n' "$SQ" | awk '$3=="RUNNING"{s+=$4} END{print s+0}') / 60 (대기 $(printf '%s\n' "$SQ" | awk '$3=="PENDING"{s+=$4} END{print s+0}'))"
  else HD="⚠ squeue 4번 실패 — 큐 상태 모름 (job · next · 상태 = ?)"; fi
  echo "══ 50kg SE 입도 2케이스 · $(date '+%m-%d %H:%M:%S') · $HD ══"
  row case job elapsed left np grid phase step atoms P_MPa plate_z z/hs kstep/h ETA ckpt next; padw 상태 26; echo " resume"
  FT=
  for C in $CASES; do
    W=$DT0/$C; I=$DT0/$C.ins1; D=; [ -d "$I" ] && D=$I; [ -d "$W" ] && D=$W
    DK=; for F in "$W/input_$C.liggghts" "$I/input_$C.liggghts"; do [ -s "$F" ] && { DK=$F; break; }; done
    IFS='|' read -r TG P4M RX U UN <<< "$(deckv "$DK")"
    R=; NR=0; PDL=
    if [ $SQOK = 0 ]; then
      R=$(printf '%s\n' "$SQ" | awk -v c=$C '($2==c || index($2,c"_")==1) && $3 ~ /^(RUNNING|CONFIGURING|COMPLETING|SUSPENDED)$/' | sort -n)
      NR=$(printf '%s\n' "$R" | grep -c .)
      R=$(printf '%s\n' "$R" | head -1)
      PDL=$(printf '%s\n' "$SQ" | awk -v c=$C '($2==c || index($2,c"_")==1) && $3=="PENDING"' | sort -n | head -1)
    fi
    read -r J JN JS NP EL LEFT SS RX1 <<< "$R"
    read -r PD PN P1x P2x P3x P4x P5x PR <<< "$PDL"
    ROLE=; JL=-; PL=-; [ $SQOK = 0 ] || { JL=?; PL=?; }
    if [ -n "$J" ]; then ROLE=$(role "$JN" $C); JL=$J; case "$ROLE" in 시험*) JL=${J}t;; esac; fi
    if [ -n "$PD" ]; then PL=$PD; case "$(role "$PN" $C)" in 시험*) PL=${PD}t;; esac; PR=${PR#(}; PR=${PR%)}; PR=$(printf '%s' "$PR" | cut -c1-26); [ -n "$NP" ] || NP=$P2x; fi
    LG=; T0=0
    if [ -n "$J" ]; then
      case "$SS" in *T*) T0=$(date -d "${SS/T/ }" +%s 2>/dev/null) || T0=0;; esac
      for F in "$DT0/logs/output_${JN}_$J.out" $(command ls $DT0/logs/output_*_$J.out 2>/dev/null); do [ -f "$F" ] && { LG=$F; break; }; done
      [ -z "$LG" ] && [ -f "$D/log.liggghts" ] && [ "$T0" -gt 0 ] && [ "$(mt "$D/log.liggghts")" -ge "$T0" ] && LG=$D/log.liggghts
    else
      LG=$(logs_of $C | head -1); [ -z "$LG" ] && [ -f "$D/log.liggghts" ] && LG=$D/log.liggghts
    fi
    G=$(grid "$LG")
    PH=$(grep -aE '^====== (PHASE [0-9]|INSERT|Simulation Finished)' "$LG" 2>/dev/null < /dev/null | tail -1)
    case "$PH" in *Finished*) PH=done;; *"PHASE 1"*) PH=P1-settle;; *"PHASE 2"*) PH=P2-stab;; *"PHASE 3"*) PH=P3-comp;; *"PHASE 4"*) PH=P4-relax;; *INSERT*) PH=insert;; *) PH=-;; esac
    read -r LL LA LP <<< "$(thermo "$LG")"; LL=${LL:--}; LA=${LA:--}; LP=${LP:--}
    LPD=$LP; [ "$LP" = - ] || LPD=$(awk -v p="$LP" 'BEGIN{printf "%.4f", p}')
    LS=$LL; [ "$LS" = - ] && LS=
    S1=; Z=; RT=-; ETA=-
    if [ -n "$J" ] && [ -n "$D" ] && [ "$T0" -gt 0 ]; then
      MS=$(find "$D/post_$C" -maxdepth 1 -name 'mesh_*.stl' -newermt "${SS/T/ }" -printf '%T@ %f\n' 2>/dev/null | awk '{f=$2; gsub(/[^0-9]/,"",f); split($1,t,"."); print f, t[1]}' | sort -n)
      [ -n "$MS" ] || MS=$(find "$D/restart_$C" -maxdepth 1 -name 'restart_*_*.bin' -newermt "${SS/T/ }" -printf '%T@ %f\n' 2>/dev/null | awk '{f=$2; gsub(/[^0-9]/,"",f); split($1,t,"."); print f, t[1]}' | sort -n)
      S1=$(printf '%s\n' "$MS" | awk 'NF==2{s=$1} END{print s}')
      [ -n "$S1" ] && { [ -z "$LS" ] || [ "$LS" -lt "$S1" ]; } && LS=$S1
      [ -n "$S1" ] && [ -s "$D/post_$C/mesh_$S1.stl" ] && Z=$(mz "$D/post_$C/mesh_$S1.stl")
      RT=$(printf '%s\n' "$MS" | awk -v now=$NOW 'NF==2 && $2>=now-3600 {n++; s[n]=$1; t[n]=$2} END{if(n>=2 && t[n]-t[1]>=600) printf "%.0f", (s[n]-s[1])*3.6/(t[n]-t[1]); else print "-"}')
      [ "$RT" = - ] && RT=$(printf '%s\n' "$MS" | awk 'NF==2{n++; s[n]=$1; t[n]=$2} END{if(n>=2 && t[n]-t[1]>=600) printf "%.0f", (s[n]-s[1])*3.6/(t[n]-t[1]); else print "-"}')
      [ "$RT" = - ] && [ -n "$LG" ] && RT=$(awk '/^ *Step +Atoms/{c=0;for(i=1;i<=NF;i++)if($i=="CPU")c=i;n=0;next} c>0&&$1~/^[0-9]+$/&&$c+0>0{n++; if(n==1){s0=$1;c0=$c}; s1=$1;c1=$c} END{if(n>=2 && c1-c0>=60) printf "%.0f", (s1-s0)*3.6/(c1-c0); else print "-"}' "$LG" < /dev/null 2>/dev/null)   # 덤프가 모자라면 (긴 P1) 로그 마지막 run 의 CPU 열 (= 그 run 의 경과 초)
      if [ "$PH" = P3-comp ] && [ -n "${LP#-}" ] && [ -n "${LL#-}" ] && [ -n "${RT#-}" ] && [ "$RT" -gt 0 ] && [ -n "$TG" ]; then
        P1=$(awk -v t=$(( LL - RT*1000 )) '/^ *Step +Atoms/{p=($NF=="pressMPa");c=0;for(i=1;i<=NF;i++)if($i=="CPU")c=i;q=1;next} /^====== PHASE 3/{r=1} r&&q&&p&&c>0&&$c+0>0&&$1~/^[0-9]+$/{d=$1-t; if(d<0)d=-d; if(b==""||d<b){b=d; s=$1; v=$NF}} END{if(s=="") print "- -"; else print s, v}' "$LG" < /dev/null 2>/dev/null)
        ETA=$(awk -v sa="${P1% *}" -v a="${P1#* }" -v sb=$LL -v b="$LP" -v g="$TG" -v r=$RT 'BEGIN{if(sa=="" || sa=="-" || sb-sa<=0){print "-"; exit}; k=(b-a)/(sb-sa)*r*1000; if(k<=0){print "-"; exit}; x=(g-b)/k; if(x<0) x=0; printf "%.0fh", x}')
      fi
      if [ "$PH" = P4-relax ] && [ -n "${RT#-}" ] && [ "$RT" -gt 0 ] && [ -n "$P4M" ] && [ -n "$RX" ]; then
        S4=$(phase_start "$P4M" "$LG" $(logs_of $C))
        [ -n "$S4" ] && ETA=$(awk -v a=$S4 -v x=$RX -v s=${LS:-0} -v r=$RT 'BEGIN{y=(a+x-s)/1000/r; printf "%.1fh", (y>0)?y:0}')
      fi
    fi
    [ -z "$Z" ] && [ -n "$D" ] && LM=$(lastmesh "$D" $C) && [ -n "$LM" ] && Z=$(mz "$D/post_$C/mesh_$LM.stl")
    HS=; [ -n "$U" ] && HS=$(awk -v h=$HS_UM -v u="$U" 'BEGIN{printf "%.6g", h*u}')
    ZH=-; [ -n "$Z" ] && [ -n "$HS" ] && ZH=$(awk -v z="$Z" -v h="$HS" 'BEGIN{if(h+0>0) printf "%.2f", z/h; else print "-"}')
    [ -n "$NP" ] || NP=$(npr "$D" $C)
    CKP=; [ -n "$D" ] && CKP=$(command ls -t "$D/restart_$C" 2>/dev/null | grep -E '^restart_(settling|compress)_[0-9]+\.bin$|^restart_(after_settling|end)\.bin$' | head -1 | sed -E 's/^restart_//; s/\.bin$//')
    ER=$(grep -acE '^ERROR( on proc [0-9]+)?:' "$LG" 2>/dev/null < /dev/null); FA=$(grep -ac '^FATAL' "$LG" 2>/dev/null < /dev/null)
    if [ $SQOK = 1 ]; then STT="?큐조회실패"
    elif [ -n "$J" ]; then STT=$ROLE; [ "$JS" = RUNNING ] || STT="$STT ($JS)"; [ -z "$LG" ] && STT="$STT ⚠로그없음"; [ "$NR" -gt 1 ] && STT="$STT ⚠R$NR"
    elif [ -n "$PD" ]; then STT="대기 $PR"
    elif fin $C "$D"; then STT="✅끝"
    elif [ -d "$W" ] && [ -d "$I" ]; then case "${LG##*/}" in output_${C}_r*t_*.out) STT="시험 끝 · 본 제출 전";; *) STT="멈춤 (큐 없음)";; esac
    elif [ -d "$W" ]; then
      if [ "$LL" = "$(runsum "$W/input_${C}_insert.liggghts")" ] && grep -aq '^====== INSERTED' "$LG" < /dev/null 2>/dev/null; then STT="삽입 끝 · 재개 전"; else STT="멈춤 (큐 없음)"; fi
    elif [ -d "$I" ]; then STT="삽입 끝 · 재개 전"
    else STT="폴더 없음"; fi
    [ "${ER:-0}" -gt 0 ] && STT="$STT ERR$ER"; [ "${FA:-0}" -gt 0 ] && STT="$STT FATAL"
    V=$(verdict $C); VD=${V%%|*}; VF=${V#*|}
    row $C "$JL" "${EL:--}" "${LEFT:--}" "${NP:--}" "${G:--}" "$PH" "${LS:--}" "$LA" "$LPD" "${Z:--}" "$ZH" "$RT" "$ETA" "${CKP:--}" "$PL"; padw "$STT" 26; echo " $VD"
    F=없음; [ -n "$DK" ] && F="~/${DK#$HOME/}"
    FT="$FT
($C 덱 값: 목표 ${TG:-?} · 이완 run ${RX:-?} · 1 µm = ${U:-?} 덱 길이 (r_* 줄 ${UN:-0}개) → 고체 두께 ${HS:-?} · 덱 $F · resume ← ${VF:-없음})"
  done
  echo "(job 뒤 t = 시험 잡 · next = 대기 잡 (50kg 은 다음 링크 없음) · step: 이번 잡 mesh 덤프·로그 중 앞선 값 · P_MPa: 덱 thermo pressMPa (sim 값 · 덱 target_press 와 같은 단위) · z/hs: 판 z / 고체 두께 101.98 µm (덱 길이)"
  echo " kstep/h: 이번 잡 mesh 덤프 mtime (없으면 restart · 그것도 모자라면 로그 CPU 열) · ETA: P3 = 이번 잡 P3 의 최근 1시간 압력 기울기로 목표까지 선형 · P4 = 이완 남은 step)"
  printf '%s\n' "$FT" | sed '/^$/d'
}

main(){ case "$1" in
  watch) watch1;;
  *) sed -n '1,6p' "$0";;
esac; }
main "$@"; exit $?
