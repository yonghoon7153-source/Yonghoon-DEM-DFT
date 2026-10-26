# resume_ckpt.sh — 멈춘 LIGGGHTS 런을 최신 체크포인트에서 이어받아 N MPI 로 재제출 (복사 → 재개 덱 → 짧은 시험 → 대조 → 본 제출)
# 2026-09-27 pse_r050_a · pse_r075_a (15 → 30 MPI) 건에서 확정한 표준 절차.  사용 전 원 런 폴더를 <root>/<case>.<접미사> 로 옮겨 둔다.
#   bash resume_ckpt.sh -n 30 -s stop15_0927 pse_r050_a pse_r075_a
#   -n NP   본 런 MPI 수 (기본 30)          -s SUF  멈춘 폴더 접미사 (필수)      -r ROOT 케이스 루트 (기본 ~/dem_test/lhs)
#   -x SFX  새 파일 접미사 (기본 r<NP>)      -t N    시험 step (기본 2000)
NP=30; SUF=""; L=~/dem_test/lhs; SFX=""; TS=2000
while getopts "n:s:r:x:t:" o; do case $o in n) NP=$OPTARG;; s) SUF=$OPTARG;; r) L=$OPTARG;; x) SFX=$OPTARG;; t) TS=$OPTARG;; *) exit 1;; esac; done
shift $((OPTIND-1)); CASES="$*"; SFX=${SFX:-r$NP}
[ -n "$SUF" ] && [ -n "$CASES" ] || { echo "사용: bash resume_ckpt.sh -n 30 -s stop15_0927 <케이스…>"; exit 1; }
cd $L || exit 1; mkdir -p logs; STAMP=$(date +%m%d_%H%M); REP=$L/resume_${SFX}_$STAMP.md
tl(){ awk -v s="$1" '/^ *Step +Atoms/{n=split($0,h);next} n>0 && NF==n && $1~/^[0-9]+$/ && $1==s {o=""; for(i=1;i<=NF;i++){if(h[i]=="CPU"||h[i]=="pressMPa")continue; o=o" "h[i]"="$i}; r=o} END{print r}' "$2"; }
reg(){ awk '/^ *Step +Atoms/{n=split($0,h);c=0;for(i=1;i<=n;i++)if(h[i]=="CPU")c=i;next} n>0&&NF==n&&c>0&&$1~/^[0-9]+$/&&$c+0>0{print $1}' "$1"; }
tr2(){ awk -v s="$1" '/^ *Step +Atoms/{n=split($0,h);c=0;for(i=1;i<=n;i++)if(h[i]=="CPU")c=i;next} n>0&&NF==n&&c>0&&$1~/^[0-9]+$/&&$1==s&&$c+0>0{o="";for(i=1;i<=NF;i++){if(i==c)continue;o=o" "h[i]"="$i};r=o} END{print r}' "$2"; }
same(){ awk -v a="$1" -v b="$2" -v t="$3" 'BEGIN{na=split(a,x," ");nb=split(b,y," ");if(na<3||na-nb)exit 1;for(i=1;i<=na;i++){split(x[i],p,"=");split(y[i],q,"=");if(p[1]<q[1]||p[1]>q[1])exit 1;if(match(p[2],/^[-+]?[0-9.]+([eE][-+]?[0-9]+)?$/)==0||match(q[2],/^[-+]?[0-9.]+([eE][-+]?[0-9]+)?$/)==0)exit 1;if(p[1]=="Step"||p[1]=="Atoms"){if(p[2]+0<q[2]+0||p[2]+0>q[2]+0)exit 1;continue};d=p[2]-q[2];if(d<0)d=-d;m=p[2];if(m<0)m=-m;if(d>t*m&&d>1e-12)exit 1};exit 0}'; }
# 느슨한 역학 확인: 원자 수 같고, 압력 (있으면) 아니면 KE 가 5 % 안
sane(){ awk -v a="$1" -v b="$2" 'BEGIN{na=split(a,x," ");nb=split(b,y," ");if(na<3||na-nb)exit 1;k="";for(i=1;i<=na;i++){split(x[i],p,"=");split(y[i],q,"=");A[p[1]]=p[2];B[q[1]]=q[2]};if(A["Atoms"]+0<B["Atoms"]+0||A["Atoms"]+0>B["Atoms"]+0)exit 1;k=("pressMPa" in A && A["pressMPa"]+0>1e-6)?"pressMPa":"KinEng";if((k in A)==0)exit 1;d=A[k]-B[k];if(d<0)d=-d;m=A[k];if(m<0)m=-m;exit (d>0.05*m && d>1e-12)}'; }
sel(){ awk 'NR==9{n=0;split("id type x y z radius vx vy vz",w," ");for(k=1;k<=9;k++)for(i=3;i<=NF;i++)if($i==w[k]){n++;c[n]=i-2};next} NR>9{o=$c[1];for(k=2;k<=n;k++)o=o" "$c[k];print o}' "$1" | sort -n | md5sum | cut -c1-12; }
echo "# LIGGGHTS 체크포인트 재개 기록 — $SFX ($NP MPI) · $(date '+%F %H:%M')" > $REP
echo "명령: bash resume_ckpt.sh -n $NP -s $SUF -r $L -x $SFX -t $TS $CASES" >> $REP
for C in $CASES; do
  S=$L/$C.$SUF; W=$L/$C; X=$L/$C.prev_$STAMP; D=$W/input_${C}_$SFX.liggghts; RN=$W/run_${C}_$SFX.sh
  echo; echo "████ $C"
  [ -d $S ] || { echo "  ⛔ $S 없음 (원 런 폴더를 먼저 이 이름으로 옮겨 둘 것)"; continue; }
  PH=$(grep -a '^======' $S/log.liggghts | tail -1)
  LS=$(awk '/^ *Step +Atoms/{q=1;next} q&&$1~/^[0-9]+$/{s=$1} END{print s+0}' $S/log.liggghts)
  echo "  멈춘 곳: $PH | 로그 마지막 step $LS"
  echo "  restart_$C/ 최신: $(ls $S/restart_$C/ 2>/dev/null | sort -t_ -k3 -n | tail -3 | tr '\n' ' ')"
  ls $S/restart_forced_liggghts_* 2>/dev/null | sed 's#.*/#  (강제 restart, 안 씀: #; s/$/)/'
  if squeue -u $USER -h -o %j | grep -q "^$C"; then echo "  ⛔ $C 이름 잡이 큐에 있음 — 건너뜀"; continue; fi
  if [ -e $W ]; then
    [ -e $X ] && { echo "  ⛔ $X 이미 있음 — 건너뜀"; continue; }
    mv $W $X && echo "  같은 이름의 기존 폴더 → ${X##*/} (보존)"
  fi
  echo "  복사 중 ($(du -sh $S | cut -f1)) …"; cp -a $S $W || { echo "  ⛔ 복사 실패"; continue; }
  mv $W/log.liggghts $W/log.liggghts.$SUF
  python3 ~/dem_test/dem_restart.py --case-list $C --root $L --suffix $SFX --skip-sacct --no-relax-detect > $W/plan_$SFX.txt 2>&1
  P=$(grep -E "^ +$C +(compress|after_settling|settling) " $W/plan_$SFX.txt | sed 's/^ *//')
  [ -n "$P" ] || { echo "  ⛔ 재개 덱 못 만듦 (체크포인트 없음 → 처음부터밖에 없음 · 보고 후 승인):"; grep -A3 '제외' $W/plan_$SFX.txt; continue; }
  M=$(echo $P | awk '{print $2}'); RR=$(awk '$1=="read_restart"{print $2}' $D)
  S0=$(echo $RR | sed -nE 's/.*_([0-9]+)\.bin$/\1/p')
  [ -z "$S0" ] && S0=$(awk '/^ *Step +Atoms +c?_?zmax/{getline; print $1; exit}' $W/log.liggghts.$SUF)
  if [ "$M" = compress ]; then TP="없음 (메시 type 1 이 첫 run 전에 생김)"; else
    awk '$1=="fix" && ($2~/^pts[0-9]+$/ || $2=="pdd_mix")' $W/input_$C.liggghts > $W/tmpl_$SFX.txt
    grep -q '&$' $W/tmpl_$SFX.txt && { echo "  ⛔ 템플릿 줄이 여러 줄 — 손으로 봐야 함"; continue; }
    awk -v f=$W/tmpl_$SFX.txt '{print} $1=="read_restart"{while((getline l < f)>0) print l}' $D > $D.tmp && mv $D.tmp $D
    TP="$(awk '{print $2}' $W/tmpl_$SFX.txt | tr '\n' ' ')(원 덱 그대로 · 삽입 fix 는 없음)"; fi
  O=$W/old_post_after${S0}_$SUF; mkdir -p $O
  (cd $W/post_$C && ls | awk -v k=$S0 '{n=$0; sub(/.*_/,"",n); sub(/\..*/,"",n); if(n~/^[0-9]+$/ && n+0>k) print}' | xargs -r mv -t $O)
  echo "  계획: $P"
  echo "  read_restart $RR (step $S0) · 뒤 덤프 $(ls $O | wc -l)개 → ${O##*/} · 템플릿 재선언: $TP"
  echo "$TP" > $W/tp_$SFX.txt
  sed -i "s/^#SBATCH -n .*/#SBATCH -n $NP/; s/mpirun \(--oversubscribe \)\{0,1\}\(--bind-to none \)\{0,1\}-np [0-9]*/mpirun --oversubscribe --bind-to none -np $NP/" $RN
  awk -v t=$TS '{if($1=="run" && $2+0>1){n=$2+0; if(n>t)n=t; print "run " n; exit} print}' $D > $W/input_${C}_${SFX}t.liggghts
  sed -e "s/${C}_$SFX/${C}_${SFX}t/g" -e "s/^#SBATCH --time=.*/#SBATCH --time=01:00:00/" $RN > $W/run_${C}_${SFX}t.sh
  EX=$(comm -13 <(awk '$1=="fix"||$1=="dump"{print $1,$2}' $W/input_$C.liggghts | sort -u) <(awk '$1=="fix"||$1=="dump"{print $1,$2}' $D | sort -u) | tr '\n' ' ')
  OK=1
  [ -s $W/$RR ] || { OK=0; echo "  ✗ $RR 없음"; }
  [ -z "$EX" ] || { OK=0; echo "  ✗ 원 덱에 없는 fix/dump ID: $EX"; }
  { grep -qE "^#SBATCH -n $NP\$" $RN && grep -q -- "--oversubscribe --bind-to none -np $NP lmp_mpi" $RN && grep -q -- "-np $NP lmp_mpi -in input_${C}_${SFX}t.liggghts" $W/run_${C}_${SFX}t.sh; } || { OK=0; echo "  ✗ 러너 $NP"; }
  echo "  $(grep '^processors' $D) | $(grep -c . $W/input_${C}_${SFX}t.liggghts)줄 시험 덱 (마지막: $(tail -1 $W/input_${C}_${SFX}t.liggghts))"
  if [ $OK = 1 ]; then J=$(sbatch --parsable $W/run_${C}_${SFX}t.sh); echo $J > $W/job_${SFX}t.txt; echo "$M $S0 $RR" > $W/mode_$SFX.txt; echo "  ▶ 시험 job $J ($(tail -1 $W/input_${C}_${SFX}t.liggghts))"
  else echo "  ⛔ 시험 제출 안 함"; fi
done
echo; echo "── 시험 잡 끝날 때까지 대기 (끝나면 대조 → 맞으면 본 제출)"
for C in $CASES; do
  W=$L/$C; S=$L/$C.$SUF; [ -f $W/job_${SFX}t.txt ] || continue; J=$(cat $W/job_${SFX}t.txt)
  for i in $(seq 360); do
    sacct -n -X -j $J -o State 2>/dev/null | grep -qE 'COMPLETED|FAILED|CANCELLED|TIMEOUT|OUT_OF|NODE_FAIL' && [ -z "$(squeue -h -j $J 2>/dev/null)" ] && break; sleep 20
  done
  read M S0 RR < $W/mode_$SFX.txt
  T=$(ls logs/output_${C}_${SFX}t_$J.out 2>/dev/null); T=${T:-/dev/null}; E=$(grep -ac ERROR $T)
  F=$(awk '/^ *Step +Atoms/{q=1;next} q&&$1~/^[0-9]+$/{print $1; exit}' $T)
  a=$(tl "$F" $W/log.liggghts.$SUF); b=$(tl "$F" $T)
  G1=0; [ -n "$F" ] && [ "$F" = "$S0" ] && [ "$E" = 0 ] && same "$a" "$b" 1e-6 && G1=1
  # G2: 체크포인트 step 의 상태를 덤프로 직접 대조 (시험이 다시 쓴 파일만 인정)
  G2=1; G2T=""
  if [ "$M" = after_settling ]; then
    x=$(grep -a '^====== PLATE HEIGHT' $W/log.liggghts.$SUF | tail -1); y=$(grep -a '^====== PLATE HEIGHT' $T | tail -1)
    [ -n "$x" ] && [ "$x" = "$y" ] && G2T="판 높이 같음 ($x)" || { G2=0; G2T="판 높이 다름/없음: 원 [$x] · 재개 [$y]"; }
  else
    nc=0
    for f in atom_$S0.liggghts mesh_$S0.stl; do
      o=$S/post_$C/$f; n=$W/post_$C/$f; [ -s $o ] || continue
      if [ -s $n ] && [ $n -nt $W/input_${C}_${SFX}t.liggghts ]; then
        case $f in atom*) u=$(sel $o); v=$(sel $n);; *) u=$(md5sum < $o | cut -c1-12); v=$(md5sum < $n | cut -c1-12);; esac
        nc=$((nc+1)); [ "$u" = "$v" ] && G2T="$G2T $f 같음 ·" || { G2=0; G2T="$G2T $f 다름 ·"; }
      else G2=0; G2T="$G2T $f 시험이 다시 안 씀 ·"; fi
    done
    [ $nc = 0 ] && [ "$M" = compress ] && { G2=0; G2T="$G2T 체크포인트 step 덤프 없음 — 손으로 확인"; }
    [ $nc = 0 ] && [ "$M" = settling ] && G2T="$G2T 체크포인트 step 덤프 없음 (G1 의 KE 일치로 대신)"
  fi
  # G3: 첫 정규 thermo (setup 줄 뒤) — 원자 수 + 압력 (없으면 KE) 5 % 안.  원 로그에 없으면 생략
  F2=$(comm -12 <(reg $T | sort -u) <(reg $W/log.liggghts.$SUF | sort -u) | sort -n | awk -v s="$F" '$1~/^[0-9]+$/ && $1+0>s+0{print;exit}')
  a2=$(tr2 "$F2" $W/log.liggghts.$SUF); b2=$(tr2 "$F2" $T)
  if [ -z "$F2" ]; then G3=1; G3T="원 로그에 비교할 정규 줄 없음 → 생략"; elif sane "$a2" "$b2"; then G3=1; G3T="5 % 안"; else G3=0; G3T="5 % 넘음"; fi
  [ -f $W/log.liggghts ] && mv $W/log.liggghts $W/log.liggghts.${SFX}t
  { echo; echo "## $C"
    echo "- 멈춘 폴더: ${C}.$SUF (손대지 않음) · 멈춘 곳 $(grep -a '^======' $S/log.liggghts | tail -1)"
    echo "- 작업 폴더: $W (= 멈춘 폴더 cp -a) · 원 로그 → log.liggghts.$SUF · 체크포인트 뒤 덤프 → old_post_after${S0}_$SUF/"
    echo "- 재개: $M 체크포인트 \`read_restart $RR\` (step $S0) · 덱 input_${C}_$SFX.liggghts · 러너 run_${C}_$SFX.sh (#SBATCH -n $NP · mpirun --oversubscribe --bind-to none -np $NP)"
    echo "- 템플릿 재선언: $(cat $W/tp_$SFX.txt)"
    echo "- 시험: job $J · input_${C}_${SFX}t.liggghts · ${T##*/} · ERROR $E"
    echo "- G1 재개 첫 thermo (step $F, setup 줄, CPU·압력 열 제외, 1e-6): $([ $G1 = 1 ] && echo 통과 || echo 실패)"; echo "    원 로그 :$a"; echo "    재개    :$b"
    echo "- G2 체크포인트 상태 덤프 대조: $([ $G2 = 1 ] && echo 통과 || echo 실패) —$G2T"
    echo "- G3 첫 정규 thermo (step ${F2:--}, 참고용 느슨한 확인): $G3T"; echo "    원 로그 :$a2"; echo "    재개    :$b2"
  } >> $REP
  if [ $G1 = 1 ] && [ $G2 = 1 ] && [ $G3 = 1 ]; then
    JM=$(sbatch --parsable $W/run_${C}_$SFX.sh); echo "- ✅ 본 제출 job $JM (run_${C}_$SFX.sh, 제출 폴더 $L)" >> $REP
  else echo "- ⛔ 본 제출 안 함 — 위 G1/G2/G3 확인 후 사람이 판단" >> $REP; fi
done
cat $REP; echo; squeue -u $USER -o "%.10i %.20j %.8T %.4C %.10M %R"
