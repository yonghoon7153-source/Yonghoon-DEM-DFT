> **받은 그대로 커밋** (2026-09-27 · 사용자 업로드 `resume_ckpt_handoff_20260927.md`, 선배 세션 작성).  §5 의 두 스크립트는 `scripts/resume_ckpt.sh` · `scripts/ckpt_watch.sh` 에 있다 (§5 코드 블록과 내용 일치 확인).  원장 `SELF-54` · 사전등록 `docs/reviews/pure_se_union_prereg_20260927.md` §6-0.

# LIGGGHTS 체크포인트 재개 — 표준 절차와 코드 (2026-09-27 확정)

**앞으로 멈춘 런이나 시간이 끝난 런을 이어 돌릴 때는 반드시 이 문서와 `resume_ckpt.sh`를 따른다.**
두 스크립트(`resume_ckpt.sh` · `ckpt_watch.sh`)를 `scripts/`에 넣고, 원장에 SELF 항목으로 기록해 줘.

## 0. 규칙 (원장에 그대로 기록)

1. 재개는 `scripts/resume_ckpt.sh`로만 한다.
   - 처음부터 다시 돌리는 건 체크포인트가 정말 없을 때만이다.
   - 그때도 먼저 보고하고 승인을 받는다.
2. 원 런 폴더는 먼저 `<케이스>.<접미사>`(예: `pse_r050_a.stop15_0927`)로 옮겨 둔다. 그 뒤로는 읽기만 한다.
3. 재개 확인 기준(G1 · G2 · G3, §3)은 바꾸지 않는다. 바꿔야 하면 근거를 들어 먼저 보고한다.
4. 지시문에는 소스나 로그로 확인한 사실만 쓴다. 이번 건 지시문의 두 전제가 틀렸다 (§1).

## 1. 이번 건 (pse_r050_a · pse_r075_a, 15 → 30 MPI)

### 무엇이 잘못됐나

- **처음부터 돌렸다.** 체크포인트를 확인하지 않고 INSERTING부터 새로 돌렸다 (job 232384 · 232385, 취소).
- **지시문 전제 ① — 틀림.** "체크포인트는 PHASE 3에서만 써진다"고 했다.
  - 실제 덱은 PHASE 1에서 `restart 50000 restart_<case>/restart_settling_*.bin`을 쓴다.
  - PHASE 1 끝에는 `restart_after_settling.bin`도 쓴다.
- **지시문 전제 ② — 불가능.** "재개 첫 thermo 줄의 압력이 원 로그와 맞아야 한다"고 했다.
  - LIGGGHTS는 run 시작(setup) 줄의 판 압력을 믿을 수 없게 찍는다.
  - 원 런에서도 loop 경계마다 약 1.5배로 튀었다 (원 로그 실측: 14002 정규 0.13241 → setup 0.19935).
  - read_restart 직후 setup 줄은 0이다.
  - 그래서 이 기준대로면 영원히 제출할 수 없다.

### 결과 (사전등록 기록용)

| | pse_r050_a (139,706개) | pse_r075_a (41,394개) |
|---|---|---|
| 멈춘 곳 | PHASE 2 (로그 끝 200002, `restart_settling_250000`까지 감) | PHASE 3 (로그 끝 1520002) |
| 재개 체크포인트 | after_settling (step 200001) | compress 1500000 |
| 시험 job | 233627 (ERROR 0) | 233642 (ERROR 0) |
| G1 재개 첫 줄 | step 200001 · 원자 139706 · zmax 0.050555745 — 원 로그와 같음 | step 1500000 · 원자 41394 · KE 2.628489e-06 — 같음 |
| G2 상태 덤프 | PLATE HEIGHT 줄 같음 | atom_1500000(위치·속도) · mesh_1500000 원 런과 같음 |
| G3 첫 정규 줄 | 원 로그에 PHASE 2 정규 줄이 없어 생략 (로그 버퍼, §3) | 아래 표 |
| 본 제출 | **job 233797** (30 MPI) | **job 233799** (30 MPI) |

r075의 G3 첫 정규 줄 비교 (참고용):

| step | 원 런 압력 (MPa) | 재개 압력 (MPa) | 차이 |
|---|---|---|---|
| 1501000 | 0.050278 | 0.050578 | 0.6 % |
| 1502000 | 0.050373 | 0.050711 | 0.7 % |

같은 구간의 KE는 약 8 % 차이였다.

**재개 후 확인:**
- r075의 판은 185,000 step 동안 0.00185 내려갔다. 0.01 m/s × dt 1e-6으로 계산한 값과 일치하므로 판 이동이 제대로 이어졌다.
- 속도는 r075가 약 116만 step/h, r050(PHASE 2)이 약 21만 step/h다.

**기록 파일과 이번에 쓴 스크립트:**
- ibb 기록 파일은 `~/dem_test/lhs/pse_resume30_0927.md`다.
- 이번에 실제로 쓴 스크립트는 둘이다.
  - `pse_resume30.sh`: G3를 1e-3으로 잡아서 막혔다.
  - `pse_confirm30.sh`: 덤프로 상태를 대조한 뒤 제출했다.
- 아래 `resume_ckpt.sh`는 두 스크립트를 합치고 기준을 바로잡은 완성본이다.

## 2. `resume_ckpt.sh`가 하는 일

1. **멈춘 곳 확인:** 마지막 `======` 단계, 로그 마지막 step, `restart_<case>/` 최신 파일, 강제 restart(`restart_forced_*`, 안 씀)를 본다.
2. **충돌 확인:** 같은 이름의 잡이 큐에 있으면 건너뛴다. 같은 이름의 폴더가 있으면 `<case>.prev_<시각>`으로 옮긴다 (보존).
3. **복사:** 멈춘 폴더를 `cp -a`로 복사하고, 원 로그는 `log.liggghts.<접미사>`로 바꿔 둔다.
4. **재개 덱·러너 생성:**
   - `~/dem_test/dem_restart.py --suffix r<NP> --skip-sacct --no-relax-detect`로 만든다.
   - 체크포인트 우선순위는 compress > after_settling > settling이다.
5. **템플릿 재선언 (비압축 모드만):**
   - after_settling · settling이면 원 덱의 `fix pts*` · `fix pdd_mix` 줄을 `read_restart` 바로 뒤에 다시 넣는다. 삽입 fix는 넣지 않는다.
   - 순수 SE는 판 메시(type 1)가 생기기 전 첫 run에서 type 1이 분포에만 있다.
   - 이 줄을 빼면 `ERROR: Atom types must start from 1 (properties.cpp:120)`로 죽는다 (목업 실측).
6. **옛 덤프 정리:** 체크포인트 step 뒤의 옛 덤프는 `old_post_after<step>_<접미사>/`로 옮긴다. 지우지 않는다.
7. **러너:**
   - `#SBATCH -n NP`와 `mpirun --oversubscribe --bind-to none -np NP`를 짝으로 맞춘다.
   - 제출은 루트에서 한다. `#SBATCH --output=logs/…`가 제출 폴더 기준이라, 거기 `logs/`가 있어야 한다.
8. **시험:**
   - 재개 후 첫 run(>1)을 2000 step으로 줄인 덱을 1시간 러너로 제출한다.
   - sacct가 종료를 보이고 squeue가 빌 때까지 기다린다.
9. **본 제출:** G1 · G2 · G3을 모두 통과해야 제출한다. 하나라도 실패하면 제출하지 않고 기록한 뒤 사람이 판단한다.

## 3. 확인 기준과 근거

- **G1 — 재개 첫 thermo 줄 (setup 줄)**
  - step과 원자 수는 정확히 같아야 한다.
  - CPU · 압력 열을 뺀 나머지(KE 또는 zmax)는 1e-6 안이어야 한다.
  - 압력을 빼는 이유는 §1 전제 ②와 같다.
- **G2 — 체크포인트 step의 상태를 덤프로 직접 대조**
  - 시험이 다시 쓴 파일만 인정한다.
  - `atom_<step>`: id · type · x · y · z · radius · v 열을 id로 정렬한 뒤 md5를 비교한다.
  - `mesh_<step>.stl`: md5를 비교한다.
  - after_settling은 `PLATE HEIGHT` 줄이 같아야 한다.
  - settling에서 해당 step의 덤프가 없으면 G1의 KE 일치로 대신한다.
- **G3 — 느슨한 역학 확인**
  - setup 뒤 첫 정규 thermo 줄에서 원자 수가 같고, 압력(0이면 KE)이 5 % 안이어야 한다.
  - 원 로그에 그 줄이 없으면 생략한다.
  - 느슨하게 두는 이유: MPI 분할 수가 바뀌면 합산 순서가 달라져 조밀한 충전층에서는 궤적이 금방 갈라진다.
    - r075 실측: 1000 step 뒤 압력 0.6 %, KE 8 % 차이.
    - 목업(2 → 4 코어): 3e-6 차이.
  - 궤적이 비트 단위로 같기를 요구하지 않는다. 사전등록 §3의 "물리 불변, 비트 동일 아님"과 같은 취지다.
- **로그 버퍼**
  - 긴 run 도중의 thermo 줄은 버퍼에 있다가 늦게 써지고, scancel되면 사라진다.
  - r050 원 로그는 200002에서 끝났지만 `restart_settling_250000`이 있었다.
  - 진행 확인은 mesh 덤프와 restart 파일로 한다. `ckpt_watch.sh`가 그렇게 본다.

**검증:**
- 목업(LIGGGHTS-PUBLIC 3.8 MPI 빌드, 축소 순수 SE 덱)에서 compress · after_settling · settling 세 경로를 모두 끝까지 돌려 통과했다.
- 다음 경우에는 본 제출이 막히는 것도 확인했다:
  - 덤프가 불일치할 때
  - 시험이 덤프를 다시 쓰지 않았을 때
  - 원자 수가 다를 때
  - 압력 차이가 11 %일 때
  - `Ave neighs/atom` 같은 비-thermo 줄이 섞일 때
- mawk와 gawk에서 모두 동작한다. 붙여넣기용이라 `!`와 탭 문자를 쓰지 않았다.

## 4. 사용법

```bash
# 1) 원 런 폴더를 옮겨 둔다 (잡이 멈춘 뒤)
mv ~/dem_test/lhs/<case> ~/dem_test/lhs/<case>.stop15_$(date +%m%d)
# 2) 재개 (시험 → 대조 → 본 제출까지 자동). 창을 닫아도 계속 돈다
nohup bash ~/dem_test/scripts/resume_ckpt.sh -n 30 -s stop15_MMDD <case…> > ~/dem_test/resume.log 2>&1 &
tail -f ~/dem_test/resume.log
# 3) 감시
watch -n 30 bash ~/dem_test/scripts/ckpt_watch.sh r30 <case…>
```

## 5. 코드

### `scripts/resume_ckpt.sh`

```bash
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
```

### `scripts/ckpt_watch.sh`

```bash
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
```

## 6. 해 달라는 것

1. 위 두 스크립트를 `scripts/`에 넣고 커밋한다.
2. 원장에 SELF 항목으로 기록한다. 내용은 이번 실수(처음부터 돌림, 틀린 전제 두 개), 규칙(§0), 기준과 근거(§3)다.
3. 사전등록 기록에 §1의 결과 표(재개 step · 파일 · 명령 · job 번호 · 대조값)를 옮긴다.
4. 앞으로 재개 요청을 받으면 이 문서를 먼저 읽고 `resume_ckpt.sh`로만 진행한다.

## 2026-10-26 개정 — 본 제출 조건 · 재개 덱 정적 대조 (원장 KG50-02 · KG50-10 · 1저자 Q2 · `d1b34664c`)

- 본 제출 = **G0** ∧ G1 ∧ G2 ∧ G3.  G0 = 시험 job 이 sacct `COMPLETED` · ExitCode `0:0` · 시험 로그의 마지막 thermo step = S0 + 시험 run · 그 뒤 `Loop time of` · ERROR 0.  sacct 조회 실패 · 대기 (360 × 20 s) 초과 · 시험 로그 없음 = 제출 안 함.
- **G3 개정** — 원 로그의 비교 구간 (S0, 기대 끝] 정규 thermo 줄이 시험 로그에 하나라도 없으면 실패 (결손).  원 로그에 그 구간 줄이 없을 때만 생략.  첫 줄의 5 % 비교는 그대로 (Codex 판정문 §3 · 고치기 전에는 시험이 setup 줄만 쓰고 죽어도 "비교할 줄 없음" 으로 통과했다).
- **재개 덱 정적 대조** (시험 전 · 실패 = 시험도 안 냄 · 기록 `<작업 폴더>/deckcheck_<SFX>.txt`): 재삽입 fix 없음 · 물리 · 변수 줄 = 본 덱 줄 그대로 (판 메시 파일 이름만 예외 · 그 파일이 작업 폴더에 있을 때) · 재개 run 에서 살아 있는 fix · 쌍 · 이웃 · timestep = 본 덱 그 run 의 상태 · restart 명령 체크포인트는 남은 step (예: step 20001 재개 → 정착 끝 200001) · 재개 run 뒤 순서 (fix · unfix · run · restart · if) = 본 덱 그대로 · 쓰는 c_ · f_ 이름 정의.
- 큐 검사 = 이름 정확 일치 (C · C_ins · C_<SFX>[t] · C_r<N>[t]) · squeue 조회 실패 = 그 케이스 건너뜀.
- 새 선택: `-T` (시험만 · NP 실측) · `-C <본 덱> <재개 덱> <체크포인트> <S0> <작업 폴더>` (정적 대조만 · 손 확인).
- 시험 = `scripts/test_resume_ckpt.py` (가짜 SLURM · 가짜 dem_restart.py · 실제 09-27 r075 덱 쌍) · 게이트에 들어 있다.
- 한정: settling 모드 G2 는 여전히 G1 KE 일치로 대신한다 (step S0 원자 상태 해시 대조 없음) · after_settling 모드의 실제 dem_restart.py 산출은 대조해 본 적 없다.

## 2026-10-27 개정 — `-c` 주석 줄 빼기 (ibb kg50_d07_b40 r56 · 1저자 *"권고대로"*)

- 왜: ibb `dem_restart.py` 의 덱 검사가 **주석 속** 다른 케이스 이름도 거부한다 — `plan_r56.txt` = `kg50_d07_b40 덱 검증 실패: 다른 케이스명 혼입: ['real_4']` (덱 생성기 `scripts/make_se_size_decks.py` 가 덱 머리 줄 전체 주석 두 줄에 템플릿 이름 `real_4` 를 적는다 · `docs/data/kg50_decks_20261026_v2/` 덱 12 개 모두 그 두 줄뿐 · 비주석 줄엔 없다) → 재개 덱 못 만듦 · 시험 안 냄.
- `-c` = 복사 직후 · `dem_restart.py` 전에 **작업 사본** 의 맨 위 `input*.liggghts` 에서 줄 전체 주석 (첫 공백 아닌 글자 `#`) 만 뺀다 · 멈춘 폴더 (원본) 는 그대로 (임시 파일 → 검사 → `os.replace` = 새 파일 · 링크 대상도 안 건드림) · 빈 줄 · 인라인 주석 · 나머지 바이트 그대로.
- 검사 (덱마다 · 하나라도 실패 = 어느 덱도 안 바꾸고 ⛔ 건너뜀): 비주석 줄 sha256 전 = 후 · 새 파일에 줄 전체 주석 0 · LIGGGHTS 명령 (`&` 이어 붙이기 → 주석 제거 · 정적 대조와 같은 `deck()`) 전 = 후 — `&` 로 이어진 명령 안의 주석 줄 · `&` 로 끝나는 주석 줄은 빼면 명령이 바뀐다.  기록 = stdout · `<작업 폴더>/strip_<SFX>.txt` · 보고 케이스 절 (덱마다 뺀 줄 수 · sha256 전 = 후) · 명령 줄의 `-c`.
- 한계: 인라인 주석 (`fix … # … real_4`) 은 안 뺀다 → 거기 다른 케이스 이름이 있으면 여전히 거부된다 · 실제 `dem_restart.py` 가 어느 덱 · 어떤 이름 목록을 보는지 · 주석에 기대는 데가 있는지는 리포에 없어 모른다 (시험의 가짜 = 맨 위 `input*.liggghts` 전부 · 가정 · 단계 표지는 `print` 줄이라 안 빠진다).  시험 = `scripts/test_resume_ckpt.py` N1–N6b · `-c` 없으면 stdout · 보고 · 작업 폴더 파일이 고치기 전 판과 바이트 같다 (가짜 SLURM 장면 29 + `-C` 3 대조 · 날짜 · 시각만 맞춤).

## 2026-10-27 개정 2 — 재개 덱 첫 긴 run 1 step 고침 (ibb kg50_d2_b50 r4 · 1저자 Q1 (가) *"권고대로 해줘"* · 원장 KG50-17)

- 왜: ibb `dem_restart.py` 가 settling 체크포인트 재개 덱에 `run 179999` 를 냈다 (= 본 덱 그 run 길이 200000 − 체크포인트 step 20001).  본 덱 정착 run 은 삽입 `run 1` 뒤 step 1 에서 시작해 step 200001 에서 끝나므로 맞는 남은 step 은 180000 — 재개 끝이 1 step 짧다.  정적 대조가 설계대로 `남은 step 다름: 재개 끝 200000 ↔ 본 덱 그 run 끝 200001 ([run 179999])` 로 거부했고 시험을 내지 않았다 (10-27 21:10 · 원본 그대로).  원인 = 계산 꼴에서 추정 (그 도구 소스는 리포에 없다).
- 고침 = `dem_restart.py` 뒤 · 시험 덱을 만들기 전에 그 꼴 하나만: 정적 대조 문제가 그 `남은 step 다름` 하나 · 재개 덱 첫 긴 run 이 원 줄 한 줄짜리 숫자 run (`upto` 없음 · `&` 이어 붙임 아님) · 맞는 값 = 원래 + 1 일 때만 그 줄의 숫자를 바꾼다 (앞 공백 · 뒤 주석 · 나머지 바이트 그대로) → 다시 읽어 명령이 그 하나만 다르고 정적 대조 문제 0 일 때만 바꾼다 (임시 파일 → `os.replace`).  그 밖 (2 step 이상 차이 · 길어짐 · 다른 문제가 같이 있음 · `upto`) = 그대로 두고 정적 대조가 거부한다.  기록 = `<작업 폴더>/fixrun_<SFX>.txt` · stdout · 보고 줄.  `-C` (정적 대조만) 는 고치지 않는다.
- 시험 = `scripts/test_resume_ckpt.py` F1–F6 (고치기 전 49 PASS · 6 FAIL → 고친 뒤 55 PASS · 0 FAIL) · 변이 7 중 4 잡힘 · 3 생존 = 겹친 가드 (문제 여러 개 허용 → 다시 대조가 잡음 · 다시 대조 빼기 → 앞 조건이 이미 보장 · `&` 줄 검사 빼기 → 원 줄 정규식이 거부).
- ⚠ 10-27 같은 날 ibb `~/dem_test/scripts/resume_ckpt.sh` 가 09-27 판 (sha256 `bf82948e…` = `1b8ef7f67` · `-T` 없음 · KG50-02 고침 전) 이었다 — D2-50 첫 `-T` 시험이 `illegal option -- T` 로 멈췄다 (아무것도 안 함).  1저자가 옛 판을 `resume_ckpt.sh.bf82948e_0927` 로 보관하고 메인 판으로 바꿨다.  ⇒ **재개 전에 `sha256sum ~/dem_test/scripts/resume_ckpt.sh` 를 리포 판과 대조한다** (기대 값 = 그때의 README).

## 2026-10-28 개정 3 — G0 기대 끝 = 시험 덱 run 합 · write_restart · 루프 체크포인트 첫 긴 run 대조 (원장 KG50-18 · KG50-19 · 1저자 *"50kg 권고대로 해"* ④ ⑤)

- 왜 (Codex 재확인 요청서 `docs/reviews/codex_kg50_resume_tool_recheck_request_20261027.md` §4-1 · §4-2 · Q2 · Q3 · 둘 다 합성으로 본 것):
  - **KG50-18** — G0 기대 끝이 S0 + 시험 덱 **마지막** run 이었다.  after_settling 재개 덱은 체크포인트 (write_restart · step 200001) 뒤 첫 긴 run (안정화 `run 200000`) 앞에 판 높이 `run 1` 이 있어 시험 = `run 1` + `run 2000` → 끝 202002 ↔ 기대 202001 → 정상 시험도 G0 실패 (닫힌 실패 · after_settling 재개가 늘 막힘).  거꾸로 1 step 짧게 끝난 시험 (202001) 은 G0 을 지난다 (합성 시험 A3 · 고치기 전 판).
  - **KG50-19** — 정적 대조 D (남은 step) 는 restart 명령 체크포인트 · 그 run 앞 반복 없음 (= settling 꼴) 에서만 돌고 E (뒤 순서) 는 첫 긴 run **다음** 줄부터 본다 → write_restart · 압축 루프 체크포인트 재개 덱의 첫 긴 run 길이는 아무도 안 봤다 (`-C` 합성: 안정화 run 199999 · 100000 · 400000 · 09-27 r075 쌍 루프 `run 5000` → `run 4000` = 통과 · 노트 "남은 step 확인 해당 없음" · "확인 생략").
- 고침 (시험 덱 · 정적 대조 · G0 의 기대 끝만 · **G1–G3 그대로**):
  - **G0 기대 끝 = S0 + 시험 덱 read_restart 뒤 모든 run 합** (`deckcheck --trial-steps`).  run 꼴 = `run N` · 꼬리 `pre yes|no` · `post yes|no` 만.  합을 못 정하면 **시험을 내지 않는다**: read_restart ≠ 1 개 · 따옴표를 못 읽음 · 명령 이름에 변수 · `jump` · `next` · `include` · step 을 바꾸는 명령 (`reset_timestep` · `minimize` · `rerun` · `read_data` · `read_dump` · `clear` …) · `print` · `quit` 말고 다른 명령이 든 `if` · read_restart 앞 run · run 수가 숫자 아님 · 꼬리 `upto` · `every` · `start` · `stop` (그 밖 꼬리도) · 마지막 명령이 run 아님.  `label` 혼자는 지나간다 (압축 재개 시험 덱 = `label loop_press` 뒤 `run 2000` · 루프 jump 는 잘려 나가 없다) · `print` · `quit` 만 든 `if` (덱의 삽입 자기검사 꼴) 도 지나간다.
  - **정적 대조 첫 긴 run** (D 를 넓힘):
    - write_restart 체크포인트 (after_settling): 본 덱 그 줄 뒤 첫 긴 run 까지의 run · label 줄 = 재개 덱 read_restart 뒤 첫 긴 run 까지 — **글자 같아야** (`deck()` 정리 뒤 · v2 · v3 덱 = `[run 1] [run 200000]`).  그 사이 run 수가 변수 · 흐름 줄이면 정할 수 없음 = 거부.
    - 반복 안 restart 체크포인트 (압축 루프 — 그 run 앞에 label · jump · include · next · run 이 든 if · step 을 바꾸는 명령 · 변수 run 이 있어 남은 step 을 못 셈): 체크포인트 줄 뒤 루프 머리 `label X` 부터 첫 긴 run 까지 = 재개 덱 read_restart 뒤 첫 긴 run 까지 (r075 쌍 = `[label loop_press] [run 5000]`) · 본 덱 그 run 뒤 첫 흐름 줄이 `X` 로 돌아가는 jump (`jump SELF X` 또는 print · quit 과 그것만 든 if) 여야 · 루프 머리 없음 · 체크포인트 줄과 머리 사이나 머리 뒤에 변수 run · 흐름 줄 = 정할 수 없음 = 거부 (예전 = "확인 생략" 노트 · 통과).
    - settling 꼴 (그대로 + 한 줄): 재개 덱 첫 긴 run 앞에 run (`run 0` 말고) 이 있으면 거부 — G0 이 시험 덱 run 합을 보게 되면 그 run 으로 생긴 1 step 어긋남을 예전 G0 (마지막 run 만) 처럼 **우연히** 막지 못한다.  남은 step 셈도 label · jump 말고 include · next · run 이 든 if · step 을 바꾸는 명령이 있으면 "못 셈" 쪽 (위 루프 대조 · 루프 머리 없으면 거부) 으로 간다.
  - 그대로: `-C` 는 정적 대조만 (고치지 않음) · `--fix-run` (KG50-17) 은 정적 대조 문제가 `남은 step 다름` 하나일 때만 (새 문제 문구는 그 꼴이 아니라 고침이 안 돈다).
- 새로 보이는 줄 (run 이 하나뿐인 settling · 압축 재개 = 예전과 같은 줄 · 새 줄 없음):

```
# stdout (시험을 낼 때 · 시험 덱 run 이 둘 이상)
  · 시험 기대 끝 step = S0 + 시험 덱 read_restart 뒤 run 합 2001 ([run 1] [run 2000] · 10-28 KG50-18)
  ▶ 시험 job <J> (run 2000 · 기대 끝 step 202002)
# 보고 케이스 절 (같은 경우 · G0 줄 앞)
- 시험 기대 끝 step (10-28 · KG50-18): S0 200001 + 시험 덱 read_restart 뒤 run 합 2001 ([run 1] [run 2000]) = 202002
- G0 시험 정상 종료: 통과 — 상태 COMPLETED · ExitCode 0:0 · 마지막 step 202002 (기대 202002) · …
# stdout (시험 전 거부 · 이유는 위 목록 중 하나 · 그 뒤 "⛔ 시험 제출 안 함")
  ✗ 시험 기대 끝 step 을 못 정함 (10-28 KG50-18) — 흐름 명령 (jump · next · include): [jump SELF skip1]
# 정적 대조 (stdout · <작업 폴더>/deckcheck_<SFX>.txt · 보고에는 마지막 "재개 덱 정적 대조: …" 줄)
  · 첫 긴 run 같음 (write_restart 체크포인트 · 10-28 KG50-19): 본 덱 그 뒤 [run 1] [run 200000] = 재개 덱 read_restart 뒤
  ✗ 첫 긴 run 다름 (write_restart 체크포인트 · 10-28 KG50-19): 본 덱 그 뒤 [run 1] [run 200000] ↔ 재개 덱 read_restart 뒤 [run 1] [run 199999]
  · 루프 몸 run 같음 (반복 안 restart 체크포인트 · 10-28 KG50-19): 본 덱 [label loop_press] [run 5000] = 재개 덱 read_restart 뒤
  ✗ 루프 몸 run 다름 (반복 안 restart 체크포인트 · 10-28 KG50-19): 본 덱 [label loop_press] [run 5000] ↔ 재개 덱 read_restart 뒤 [label loop_press] [run 4000]
  ✗ 루프 몸 run 을 정할 수 없음 (반복 안 restart 체크포인트 · 10-28 KG50-19): 본 덱 [label loop_press] [run 5000] 뒤 첫 흐름 줄 없음 (그 label 로 돌아가는 jump 여야) — 손으로 확인
  ✗ 남은 step 을 정할 수 없음 (그 run 앞에 반복 · 흐름 · 변수 run · 체크포인트 뒤 루프 머리 label 없음 · 10-28 KG50-19) — 손으로 확인
  ✗ 첫 긴 run 길이를 정할 수 없음 (write_restart 체크포인트 · 10-28 KG50-19): 본 덱 그 뒤 run 수가 숫자가 아님 [run ${n1}] — 손으로 확인
  ✗ 재개 덱 첫 긴 run 앞에 run 이 있음 (restart 체크포인트 = 본 덱 그 run 도중 · 10-28 KG50-18): [run 1]
```

- 시험 = `scripts/test_resume_ckpt.py` 에 32 개 더함 (A 6 = after_settling 가짜 SLURM 장면 · P 13 = 시험 덱 run 합 거부 · 지나감 · W 13 = `-C` 첫 긴 run 대조) — 시험 먼저 커밋에서 고치기 전 판 (도구 sha256 `65f73b37…` = 10-27 개정 2 판) = 87 중 57 PASS · 30 FAIL (옛 55 전부 통과 · 새 32 중 지키는 시험 2 통과) → 고친 판 87 PASS · 0 FAIL.  Python 3.11.15 · 3.8.20 (시험 파일 · 도구 안 `python3` 둘 다) 판정 같음.  돌연변이 아홉 (고친 판에서 한 조각씩 끔 — D 의 흐름 셈 · 루프 머리 앞 대조 · 시험 덱 if 거부 · settling 앞 run · G0 합 · write 대조 · 루프 대조 · run 꼬리 이유 · 루프 jump 확인) = 아홉 다 잡힘.
- **settling 길 바이트 같음** = `python3 scripts/test_resume_ckpt.py --compare-old <고치기 전 판>` (장면마다 같은 입력으로 옛 판도 돌려 stdout · 보고 · 작업 폴더 모든 파일 · 시험 · 본 제출 여부를 바이트 대조 · 임시 경로 · 보고 머리 날짜 시각만 맞춤): settling 묶음 장면 45 (K 6 · S 7 · D 9 · Q 4 · T 1 · N 7 · F 11) **다름 0** — F 의 `-T` 장면 = ibb D2-50 `-T` 꼴 (dem_restart.py `run 179999` → 고침 `run 180000` · 기대 끝 22001) 포함 · Python 3.8 에서도 다름 0.  대조 도구 자체 = 같은 판끼리 장면 79 다름 0.  실제 09-27 r075 압축 쌍 (`-C`) = 판정 (종료 코드) 같음 · 노트 한 줄만 "남은 step 확인 생략" → "루프 몸 run 같음 ([label loop_press] [run 5000])".
- 이 개정 판 `scripts/resume_ckpt.sh` sha256 = `e59c43e6…` (10-27 개정 2 판 `65f73b37…` 에서 바뀜) — ibb 사본을 바꿀 때 대조한다.
- 한계:
  - after_settling · 압축 재개 덱 · 원 로그 · 시험 로그는 **합성**이다 (요청서 §4 의 구성 · 실제 dem_restart.py 산출 · ibb 시험 아님).  실제 dem_restart.py 가 after_settling 재개 덱의 판 높이 `run 1` · 안정화 run 을 어떻게 내는지 모른다 (소스가 리포에 없다).  글자 대조라 같은 뜻의 다른 표기 (`run 1 pre no` · 덧붙인 `run 0`) 도 거부한다 (닫힌 실패 · 손으로 본다).
  - 정적 대조는 체크포인트가 체크포인트 줄 뒤 **첫 긴 run** 에서 나왔다고 본다 (예전과 같은 가정) — 이완 run 중에 쓰인 `restart_compress_*` (`restart 0` 없는 덱 · KG50-11) · 루프 몸의 둘째 긴 run 도중 체크포인트는 가리지 못한다.  뒤에서 jump 하는 label 이 (루프 머리 말고) 재개 덱 첫 긴 run 앞에 있는지도 보지 않는다.
  - `&` 로 나뉜 run (시험 덱 자르기 awk 가 못 보는 꼴) 은 시험이 그 run 을 통째로 돈다 — 합은 맞게 세지만 시험이 1 시간을 넘기면 G0 (TIMEOUT) 이 막는다 (닫힌 실패).
  - 시험 전 거부 이유는 stdout (nohup 기록) 에만 나온다 — 보고 .md 의 케이스 절은 시험을 낸 케이스만 생긴다 (다른 시험 전 거부와 같은 자리 · 시험 N1 이 그 꼴을 지킨다).
  - settling 꼴의 새 거부는 그런 줄이 있는 덱에서만 결과가 바뀐다 — 본 덱 쪽 (include · next · run 이 든 if · step 을 바꾸는 명령) 은 v2 · v3 본 덱 · 09-27 r075 본 덱에 없다 (v2 · v3 의 삽입 자기검사 `if` 는 print · quit 만이라 지나간다 · 가짜 SLURM settling 장면이 모두 v2 본 덱으로 돈다).  재개 덱 쪽 (첫 긴 run 앞 run) 은 ibb D2-50 `-T` 가 기대 끝 22001 = S0 + 2000 으로 G0 을 지났으니 그 재개 덱에는 0 아닌 run 이 없었다 (추정 · 메인 세션 전달 · 그 덱은 리포에 없다).

## 2026-10-28 밤 개정 4 — 이번 호출 시험만 승격 · 전체 프로그램 대조 · 압축 체크포인트 거부 · 도구 신원 승인 · G0 마지막 줄 (원장 KG50R-01–05 · 07 · 1저자 *"50kg도 권고대로해"*)

- 왜: Codex 재검토 `docs/reviews/codex_kg50_resume_recheck_20261028/codex_review_kg50_resume_recheck_20261028.md` (리뷰 핀 `f118c1fd1` · 자동 본 제출 HOLD · P1 4 · P2 1 · P3 1) + 우리 재현 `docs/reviews/codex_kg50_resume_recheck_20261028/_repro_ours_20261028/README.md` (KG50R-04 를 Linux bash 로 실제로 돌려 두 장면 모두 본 제출 · G0 마지막 줄 = KG50R-07).  수정 계획 `docs/50kg/kg50_resume_recheck_fix_plan_20261028.md` — 1저자 10-28 밤 Q1 예 · Q2 (가) · Q3 (가) · Q4 예 · Q5 예 · Q6 (나) · Q7 예 · Q8 (가).
- 고침 (G1–G3 문턱 · `-T` 뜻 그대로):
  - **Q1 (KG50R-04 · KG50-02 · 14) 이번 호출이 낸 시험만 본 제출로.**  첫 고리에서 시험 sbatch 가 종료 코드 0 · 숫자 job 번호 (`--parsable` 의 `id` 또는 `id;cluster` → `id`) 를 돌려준 케이스만 메모리 목록에 넣고, 둘째 고리는 그 목록만 돈다 — 작업 폴더의 `job_<SFX>t.txt` · `mode_<SFX>.txt` 로 자격을 다시 만들지 않는다 (예전 = 큐 차단 · 정적 거부 뒤에도 옛 성공 시험으로 본 제출).
    - 시도 폴더 `<작업 폴더>/attempt_<SFX>_<MMDD_HHMMSS>_<PID>/` — `tool.txt` (두 도구 sha256 · 승인값 · 시도 · 케이스 · 멈춘 폴더 · NP · `-t` · 시험을 내면 모드 · S0 · 체크포인트 · 시험 덱 첫 긴 run · 예산 한 줄) · 시험을 내면 그 시험의 재개 덱 · 시험 덱 · 러너 둘 · plan · fixrun · deckcheck · cut · tp (· strip) 사본 · `job_t.txt` · `mode.txt` · `lastrun_n.txt` · `result.txt` (G0–G3 · 결정) · 본 제출이면 `main_job.txt` · 시험 전 거부면 `reject.txt`.
    - 멈춘 폴더에서 같이 복사된 옛 `job_*t.txt` · `mode_*.txt` 는 `<시도 폴더>/old_markers/` 로 옮긴다 (지우지 않는다 · 읽지 않는다).  예전 작업 폴더 (`<C>.prev_<시각>`) · `logs/` 의 옛 시험 로그는 손대지 않는다.  이번 시험의 `job_<SFX>t.txt` · `mode_<SFX>.txt` 는 예전처럼 작업 폴더에도 쓴다 (`ckpt_watch.sh` 가 읽는다 · 승격에는 안 쓴다).
    - 본 제출 바로 전 — `squeue -u $USER -h -o '%i %j'` 다시: 그 케이스 잡 (C · C_ins · C_<SFX>[t] · C_r<N>[t] · 이번 시험 job 번호는 뺀다) 이 있거나 조회 실패면 본 제출 안 함 · 두 도구 sha256 다시 (승인값과 다르면 안 함) · 이 시도의 `main_job.txt` 가 이미 있으면 안 함.
    - 같은 케이스 이름이 목록에 두 번이면 두 번째는 시험 전 거부 (예전 = 시험 2 · 본 2).
  - **Q2 (KG50R-02 · 03 · 05 · KG50-10 · 18) 정적 대조 = 전체 프로그램 대조** (규칙 원문 = 도구 안 `check()` 앞 머리 주석) — 재개 덱 = [준비 구간] + [본 덱 체크포인트 뒤 구간을 논리 명령 하나하나 그대로]:
    - 뒤 구간 — restart 체크포인트 = 본 덱 그 run (남은 step 만 다름 · ⚠ 10-28 밤 2 정정: 이 판은 그 run 의 꼬리 (every · pre · post · start · stop · upto) 를 안 봐 `run 200000 every 1000 "velocity …"` 본 덱에 `run 180000` 재개 덱이 통과했다 — 고친 판 = 꼬리가 있으면 거부 · 아래 개정 4b B) 부터 끝까지 · write_restart 체크포인트 = 그 줄 다음 명령부터 끝까지 (판 높이 `run 1` · 판 STL `print` · 판 fix · 첫 긴 run 까지 글자 그대로).  다르면 더함 · 빠짐 · 바뀜을 보인다 (difflib).
    - 준비 구간 — 상태 명령 (도구 `STATE_CMD`: fix · unfix · fix_modify · compute · uncompute · compute_modify · variable · dump · undump · dump_modify · region · thermo · thermo_style · thermo_modify · timestep · neighbor · neigh_modify · atom_style · atom_modify · units · boundary · newton · dimension · processors · soft_particles · communicate · comm_style · comm_modify · restart · pair_style · pair_coeff) 과, 본 덱 체크포인트 앞에 **글자 그대로** 있는 `print` · `if` (print · quit 만) · `group … type …` · `shell mkdir` 만.  그 밖 (velocity · set · delete_atoms · run · label · jump · create_box · 모르는 명령) = 거부.
    - 준비 구간이 만든 상태 = 본 덱 체크포인트 시점 상태 (⚠ 10-28 밤 2 정정: 이 판은 준비 구간 **끝**의 상태 표만 대조했다 — 변수를 바꿨다 되돌리면 (`variable dt equal 2.0e-6` · `timestep ${dt}` · `variable dt equal 1.0e-6`) 끝 표는 같은데 timestep 은 2 배인 덱이 통과했다 · 실제 D2 r4 덱에 두 줄을 더한 반례 · LIGGGHTS 는 `${x}` 를 그 자리에서 치환한다.  고친 판 = 상태 줄도 본 덱 체크포인트 앞에 글자 그대로 + 명령 순서 = 본 덱의 순서 보존 부분열 · 아래 개정 4b A).  꼭 있어야 (빠짐 = 거부): fix (템플릿 빼고) · fix_modify · 전역 설정 (timestep · neighbor · restart · pair_style …) · pair_coeff · *_modify.  선언하면 같아야 (빠짐 = 허용 · 쓰는 곳은 아래 참조 검사 · c_/f_ 검사): compute · 변수 · dump · region · thermo · 템플릿 fix.  재개 덱에만 있는 것 = 거부.
    - 변수 참조 (`${x}` · `$x` · `v_x`) = 그 앞에 정의 · label = 본 덱 · 재개 덱 각각 유일 · jump 목적지 = 재개 덱에 있고 본 덱 뒤 구간의 그 label · `include` · `next` · `jump SELF <label>` 말고 다른 jump · 이름이 변수인 명령 = 명령 자리에서 거부 (⚠ 10-28 밤 2 정정: '어디서든' 이 아니었다 — 이 판은 최상위 · `if` 안만 보고 `run … every M "…"` 안 명령은 못 봤다 · 고친 판 = run every 안까지 (개정 4b B) · LIGGGHTS 와 낱말 나누기가 다른 꼴 (NBSP · `&` 이음 · CR 만 쓴 덱) 은 여전히 못 본다 = 개정 4b 한계 I) · 본 덱 체크포인트 앞 `if` = print · quit · jump 만 · 변수 꼴 = equal · atom · string · delete 만 · read_restart = 1 개 · 그 파일 = 체크포인트 · restart 체크포인트 step 은 본 덱 그 run 범위 안.
    - 첫 긴 run = 꼬리 없는 `run N` 원 줄 한 줄 — `every` · `pre` · `post` · `start` · `stop` · **`upto`** · 변수 · `&` 이음 = 거부 (`upto` 는 지원하지 않기로 정했다 · 시험 G1).
    - **허용 차이 (목록 고정 · 시험)**: ① 첫 긴 run 남은 수 (restart 체크포인트 · 시험 F · K) ② 판 메시 fix 의 `file` 이름 (그 파일이 작업 폴더에 있을 때만 · G6 · C2) ③ `shell mkdir` ↔ `shell mkdir -p` (같은 디렉터리 · G6) ④ 템플릿 fix 재선언 · 빠짐 (G1 scheduler/plain) ⑤ '선언하면 같아야' 상태의 빠짐 (G1 baseline = thermo · 삽입 검사 변수 없음) ⑥ 본 덱 체크포인트 앞에 글자 그대로 있는 print · if · group type · shell mkdir (G1 baseline · P10).  그 밖의 더함 · 빠짐 · 바뀜 = 거부 (⚠ 10-28 밤 2 정정: 이 판에서는 끝 상태 표가 같은 다시 정의 · 준비 구간 명령 순서 바꿈 (fix 순서) 이 '바뀜' 으로 안 잡혔다 → 고친 판 = 개정 4b A · ② 는 그 파일이 **있는지만** 보고 내용 (판 높이) 은 안 본다 = 개정 4b 한계 J).
    - 시험 덱 = `deckcheck --cut-trial` (같은 논리 명령 파서) — 첫 긴 run 앞 원 줄 그대로 + `run min(N, -t)` · 자른 덱을 다시 읽어 명령 = 재개 덱 첫 긴 run 앞 명령 + 그 run 일 때만 쓴다 · 정상 재개 덱에서는 예전 awk 절단기 (`$1=="run" && $2+0>1` 에서 자름) 와 바이트 같다 (시험 G5).
    - 시험 예산 — 첫 긴 run 앞 run 합 + min(N, -t) = 시험 덱 run 합 (`--trial-steps`) · 마지막 run = `[run min(N, -t)]` · 아니면 시험 안 냄 · G0 기대 끝 = S0 + 그 합.  `-t` = 1 이상 정수.
  - **Q3 (KG50R-01 · KG50-19 · KG50-11) 압축 체크포인트 재개 = 거부** — `-C` (체크포인트 이름 `restart_compress_*` · 또는 본 덱 반복 (label · jump) 안 restart 체크포인트) · 본 흐름 (dem_restart.py 계획 = compress → 시험 전 거부).  문구 = `압축 체크포인트 재개 = 지원 안 함 (KG50R-01 · 1저자 10-28 Q3 (가))`.  이완 중 `restart_compress_*` 도 같은 길.  09-27 r075 실제 쌍 = 이제 거부 (예전 = 통과).
  - **Q4 (Codex Q7) 도구 신원** — 시작 때 이 스크립트 · `~/dem_test/dem_restart.py` sha256 을 stdout · 보고 머리 · 시도 폴더에.  본 제출 (`-T` 없음) = `-A <resume_ckpt.sh sha256>` · `-H <dem_restart.py sha256>` 이 실제 파일과 같을 때만 (둘 다 64 자 sha256 이 있어야) — 없거나 다르면 **아무것도 하지 않는다** (작업 폴더도 안 만든다 · rc 1) · 본 제출 바로 전 다시 대조.  `-T` = 기록만 + 보고 끝에 **본 제출 명령 한 줄 — 그 `-T` 에서 G0–G3 를 통과한 케이스만** (빠진 케이스는 이름만 · 통과한 케이스가 없으면 `본 제출 명령 없음`).
  - **Q5 (KG50R-07) G0** = 예전 조건 ∧ 마지막 thermo 줄이 최신 머리 (`Step Atoms …`) 아래 · 칸 수 = 머리 칸 수 · 모든 칸이 유한한 수 ∧ 마지막 `Loop time of … for N steps` 의 N = 시험 마지막 run.
  - **Q9** — 시험 전 거부 (같은 케이스 두 번 · 멈춘 폴더 없음 · 큐 조회 실패 · 큐 · 이전 폴더 · 복사 · 시도 폴더 · `-c` · dem_restart.py · 압축 · 템플릿 · 정적 대조 · 시험 덱 · 시험 제출) 도 보고에 케이스 절 `## <C> — 시험 전 거부 (10-28 Q9 · KG50R)` (단계 · 이유 · 시도).  stdout 의 거부 줄은 예전 글자 그대로.  (`docs/dem1/kg50_watch/kg50_watch.sh` 의 resume 열은 `## <C>` 절만 읽는다 — 시험 전 거부 절은 그 열에 안 잡히고 더 이른 보고의 판정이 보인다 · 예전에는 거부가 보고에 아예 없었다.)
  - **Q6 (나) · 한정** — 상태 대조 = G1 첫 줄 (원자 수 · KE 등 1e-6) 로 대신한다 · **원 런 상태 증명이 아니다** (체크포인트를 따로 읽어 시험 S0 상태와 대조하는 reader 는 만들지 않았다 · 1저자 10-28 Q6 (나) · 덱 명령으로 상태를 바꾸는 길은 위 Q2 가 막는다).
- 쓰는 법 (바뀜):

```bash
# ① 시험만 — 보고 머리 '도구 신원' 줄 = sha256 둘 · 보고 끝 '본 제출 명령' 줄 (G0–G3 통과 케이스만 · -T 없이 · -A · -H 승인값)
bash ~/dem_test/scripts/resume_ckpt.sh -T -n 56 -s ins1 -r ~/dem_test kg50_d07_b50
# ② 1저자가 sha256 두 값을 확인한 뒤 — 그 '본 제출 명령' 줄 그대로 (새 시험부터 다시 돌고 G0–G3 · 큐 · sha256 을 다시 본 뒤 본 제출)
bash /home/<사용자>/dem_test/scripts/resume_ckpt.sh -n 56 -s ins1 -r /home/<사용자>/dem_test -x r56 -t 2000 -A <resume_ckpt.sh sha256> -H <dem_restart.py sha256> kg50_d07_b50
```

- 새로 보이는 줄 (가짜 SLURM 시험 장면 · v2 kg50_d07_b40 본 덱 · 경로 · sha256 · 시각만 줄임 · 새 줄에는 표지 `KG50R` 가 든다 — `--compare-old` 가 그 줄을 빼고 옛 판과 대조):

```
도구 신원 (10-28 Q4 · Codex Q7 · KG50R): resume_ckpt.sh sha256 <64> (<경로>) · dem_restart.py sha256 <64> (<경로>) · 시도 attempt_r56_1028_105629_16673
  · 시험 덱 (10-28 KG50R-02 · 05 · 같은 논리 명령 파서): 재개 덱 첫 긴 run [run 180000] (원 줄 129) → [run 2000] · 시험 예산 = 첫 긴 run 앞 run 합 0 + 2000
  · 첫 긴 run 뒤 명령 같음 (10-28 KG50R-03 · 명령 하나하나 64 개)
  · 재개 지점 상태 대조 (10-28 KG50R-03): 본 덱 48 항목 · 재개 덱 43 항목 · 재개 덱이 다시 선언하지 않음 (선언하면 같아야 하는 것 · 쓰는 곳은 참조 검사): thermo · thermo_style · variable n_am_ins · variable n_ins · variable n_se_ins
# -C 거부 예 (Codex suffix_velocity · 09-27 r075 압축 쌍)
  ✗ 첫 긴 run 뒤 명령 다름 (10-28 KG50R-03 · 명령 하나하나): 본 덱 64 개 ↔ 재개 덱 65 개 — 재개 덱에만 [velocity all set 1.0 0.0 0.0]
  ✗ 압축 체크포인트 재개 = 지원 안 함 (KG50R-01 · 1저자 10-28 Q3 (가)) — 체크포인트 restart_compress_1500000.bin (이름 restart_compress_*)
# 보고
- 도구 신원 (…): … · 승인 -A <64> · -H <64> (실제와 같음)                      ← -T 이면 "승인 -A 없음 · -H 없음 (없음 · 다름)"
- 시도 (10-28 KG50R-04): attempt_r56_… — 이번 호출이 낸 시험만 본 제출 대상 (작업 폴더의 옛 job · mode 파일은 읽지 않는다)
## kg50_d07_b40
- 시도 (10-28 KG50R-04): attempt_r56_… · 이번 호출이 낸 시험 job 7001 만 승격 대상 (기록 <작업 폴더>/attempt_r56_…)
- G0 마지막 줄 · Loop (10-28 KG50R-07): 마지막 thermo 줄 = 최신 머리 아래 · 칸 수 같음 · 모든 칸 유한 수 (step 22001 · 줄 6) · 'Loop time … for 2000 steps' ↔ 시험 마지막 run 2000 — 같음
- 본 제출 직전 다시 확인 (10-28 KG50R-04 · Q4): 큐에 그 케이스 잡 없음 (이번 시험 7001 뺌) · 도구 sha256 = 승인값
- ⛔ 본 제출 안 함 (10-28 KG50R-04) — 본 제출 직전 큐에 그 케이스 잡: kg50_d07_b40_r4 (이번 시험 7001 은 뺌)
## kg50_d07_b40 — 시험 전 거부 (10-28 Q9 · KG50R)
- ⛔ 시험 전 거부 (KG50R) — 단계: 큐 · 이유: kg50_d07_b40 의 잡 (kg50_d07_b40 · kg50_d07_b40_ins · kg50_d07_b40_r56[t] · kg50_d07_b40_r<N>[t]) 이 큐에 있음 — 건너뜀 · 시도 attempt_r56_… · 시험 · 본 제출 없음
- 본 제출 명령 (10-28 Q4 · KG50R · -T 를 뺀 같은 명령 + 승인값 · G0–G3 통과 케이스만 · 새 시험부터 다시): `bash <경로>/resume_ckpt.sh -n 56 -s ins1 -r <루트> -x r56 -t 2000 -A <64> -H <64> kg50_d07_b40`
- 본 제출 명령 없음 (10-28 Q4 · KG50R) — 이번 -T 에서 G0–G3 를 통과한 케이스가 없다 (거부 · 실패: kg50_d07_b40)
# 승인값이 없거나 다르면 (stdout · 아무것도 안 함 · rc 1)
⛔ 본 제출 승인 인자 (-A resume_ckpt.sh sha256 · -H dem_restart.py sha256) 가 없거나 실제 파일과 다름 — 아무것도 하지 않음 (10-28 Q4 · Codex Q7 · KG50R)
```

- 시험 = `scripts/test_resume_ckpt.py` 179 개 (옛 87 + 새 92 = R 14 · G 54 · X 6 · L 5 · I 9 · Q9 4) — 시험 먼저 커밋에서 고치기 전 판 (`e59c43e6…`) = 179 중 97 PASS · 82 FAIL (옛 87 중 기대를 바꾼 8 실패 · 79 통과 / 새 92 중 74 실패 · 18 통과 = 대조군 · 예전에도 거부하던 꼴 · 시험 덱 바이트 같음 · bad_late 기록) → 고친 판 179 PASS · 0 FAIL.  Python 3.11.15 · 3.8.20 (시험 파일 · 도구 안 `python3` 둘 다) 판정 같음 · 실행 ≈ 90 s (게이트 단계 주석의 "≈ 9 s" 는 옛 값).
  - R = 같은 루트 두 번 호출 (A 작업 폴더 남김 · B 옛 작업 폴더를 멈춘 폴더로 다시 이름) · Codex `probe_stale_trial.py` 두 장면 (busy_queue · queue_query_failure) 은 승인값 · 가짜 dem_restart.py 를 주어 옮겼다 — 그 탐침 그대로는 `-A` · `-H` 가 없어 새 판의 승인 거부로 끝나 Q1 을 못 본다.  G = Codex 덱 고정물 그대로 `-C` 29 · 같은 부류 13 · 허용 차이 4 · 사슬 3 · 옛 awk 절단기와 바이트 4 · 루프 1.
  - 기대를 바꾼 옛 시험 8: C1 · W0 (09-27 r075 압축 쌍 통과 → 거부 · Q3) · W6 · W7 · W10 · W12 (루프 몸 문구 → 압축 거부 · Q3) · P8 (`run 0 pre no post no` 받음 → 준비 구간 거부 · Q2) · N1 (보고 케이스 절 없음 → 있음 · Q9).
  - **옛 판 대조** (`--compare-old <e59c43e6 판>` · stdout · 보고 · 작업 폴더 파일 · 시험 · 본 제출 여부 · 새 줄 (표지 `KG50R`) · 시도 폴더 · `cut_*.txt` 빼고): 예전부터 있던 묶음 (K S D Q T N F C A P W) 의 둘 다 정상 장면 (시험 · G0–G3 통과 / `-C` 통과) **다름 0** = settling · after_settling 정상 길 출력 그대로 · Python 3.8 도.  새 묶음의 둘 다 정상 장면 다름 3 = 보고만 (R13 같은 케이스 두 번 · G6 ② 판 메시 노트 줄 문구 · I7 빠진 케이스의 시험 전 거부 절이 남긴 빈 줄).  옛 판 정상 · 새 판 거부 43 (C · W 의 r075 압축 쌍 · P8 · R12 · G 29 · X 4 · L 4 · I 2).
  - 돌연변이 28 (고친 판에서 관문 하나씩 끔) = 26 잡힘 · 생존 2 = 자른 시험 덱 다시 읽기 대조 · 셸 시험 예산 대조 — 절단기 · `--trial-steps` 가 맞는 한 닿지 않는 방어 (서로 같은 꼴을 막는다).
  - `docs/dem1/kg50_watch/test_kg50_watch.sh` (도구 글자 대조 · 보고 꼴) = ✅ 165 · ❌ 0.
- 이 개정 판 `scripts/resume_ckpt.sh` sha256 = `fb334928ff0c524e240f3166fea40245d298a40b9245a26fd720352e7b106f07` (10-28 개정 3 판 `e59c43e6…` 에서 바뀜) — ibb 사본을 바꿀 때 대조하고, 본 제출 `-A` 값이 된다.
- 한계:
  - ~~**게이트 단계 둘이 이 판에서 실패한다**~~ → ✅ 10-28 밤 해소 (1저자 Q5-S1 = 등록 §12-4 개정 · 생성기 고침 · Q5 selftest `PASS (151/151)` · `PASS (98/98)` · 증거 `docs/reviews/kg50r_fix_evidence_20261028/`) — 아래는 고치기 전 기록:  — `scripts/kg50_q5_branches.py --selftest` = `FAIL (61/84)` · `scripts/kg50_q5_verdict.py --selftest` = `FAIL (6/21)` (통과 / 센 수 · 예외로 뒤 묶음이 끊겨 센 수도 준다 · 옛 판 `PASS (150/150)` · `PASS (98/98)`).  Q5 등록 `docs/50kg/kg50_q5_dt_damping_registration_draft_20261027.md` §8-1 (비준) 이 옛 판 `-C` 의 문제 한 줄 `재개 지점 뒤 순서 줄 수 다름: 본 덱 12 ↔ 재개 덱 0` 을 글자로 고정했고 생성기가 그 줄을 대조한다.  이 판은 W1 가지 A · F · A3 · F3 덱에 문제 셋을 낸다 — ⓐ `체크포인트 뒤 ~ 첫 긴 run 앞 명령 다름 … 본 덱 35 개 ↔ 재개 덱 37 개 — 재개 덱에만 [dump dq5a …] [dump dq5c …]` ⓑ `첫 긴 run 뒤 명령 다름 … 본 덱 27 개 ↔ 재개 덱 2 개 — 바뀜 [print "====== PHASE 3 …"] [dump dmp_atom …] → [undump dq5a] [undump dq5c]` ⓒ `재개 지점 restart 다름: 본 덱 [restart 50000 restart_<case>/restart_settling_*.bin] ↔ 재개 덱 [restart 0]` = 등록된 가지 바꿈 (§4-5 덤프 · W1 끝 · 165 행 `restart 0`) 그대로.  W2 (§12-2 초안) 는 압축 체크포인트라 Q3 거부 줄이 앞에 든다.  ⬜ 등록 · 생성기 처리 = 1저자 (이 판에서 정하지 않았다).
  - 덱 · 로그는 가짜 SLURM 시험 장면이다 (v2 본 덱 · 합성 재개 덱 · Codex 고정물 · 09-27 r075 실제 쌍) — 실제 ibb `dem_restart.py` 의 settling · after_settling 재개 덱 · 실제 LIGGGHTS 로그로 이 판을 돌린 적 없다.  새 대조는 예전보다 엄격하다 → 실제 덱에 시험 고정물에 없는 줄 (재개 덱에만 있는 명령 · 같은 뜻의 다른 표기) 이 있으면 시험 전 거부로 멈춘다 (닫힌 실패 · 손으로 본다).  특히 10-27 개정 2 의 첫 긴 run 1 step 고침은 정적 대조 문제가 `남은 step 다름` **하나**일 때만 돈다 → 실제 D2 재개 덱에서 다른 문제가 같이 나오면 고침이 안 돌고 시험을 내지 않는다.
  - awk — mawk 1.3.4 · GNU Awk 5.2.1 (10-28 밤 메인 재실행 · Ubuntu noble 패키지를 스크래치에 풀어 PATH 앞에만 · 시스템 awk 그대로) 둘 다 `179 PASS · 0 FAIL` (`docs/reviews/kg50r_fix_evidence_20261028/`) · ibb 의 실제 gawk 판으로는 아직 안 돌림 (새 awk 는 POSIX 범위: split · match · substr · ERE).
  - CRLF 재개 덱 — `-C` 는 읽지만 본 흐름의 체크포인트 줄 추출 (셸) 은 예전처럼 CR 이 남아 진행하지 못한다 (옛 판 · 새 판 같음).
  - region · group 이름을 쓰는 곳의 정의 대조는 없다 (변수 참조 · c_ · f_ 만) · 첫 긴 run 의 `upto` 는 지원하지 않는다 (거부).

## 2026-10-28 밤 2 개정 4b — 독립 사전 공격 A–F 고침 (준비 구간 글자 · 순서 · 체크포인트 run 꼬리 · 실행 영수증 · 본 sbatch 출력 · G3 유한 수 · 케이스 이름 · 원장 KG50P-01–06)

- 왜: 개정 4 판 (`fb334928…`) 을 고친 사람 설명 없이 diff 만 본 독립 사전 공격 리뷰 — 원장 KG50P-01–10 (P1 1 · P2 1 · P3 8 · 증거 `preattack/` 는 메인 통합 트리에 반입).  A–F (KG50P-01–06) = 이 개정에서 고침 (시험 먼저 · 고치기 전 판에서 옳은 이유로 실패 확인) · G–J (KG50P-07–10) = 고치지 않고 아래 한계에 적음 (KG50P-10 의 '준비 구간 fix 순서 바꿈' 은 A 로 닫힘).
- 고침 (G1–G3 문턱 · `-T` 뜻 · 허용 차이 목록 ①–⑥ 그대로):
  - **A (KG50P-01 · P1 · KG50R-03 부류 회귀)** 준비 구간 (read_restart · 템플릿 fix 빼고) = 본 덱 체크포인트 앞 명령의 **순서 보존 부분열**.  상태 명령 줄은 본 덱 체크포인트 앞에 글자 그대로 있어야 하고 (② 판 메시 `file` 이름 · ③ `mkdir` ↔ `mkdir -p` 는 같은 명령으로 본다) · 명령 순서 (상태 + 동작) 가 본 덱과 같아야 한다 (같은 변수를 두 번 정의하면 본 덱과 같은 순서 · 같은 정의일 때만 통과 — 시험 Y3 대조군).  새 문구 둘: `재개 덱 준비 구간 상태 명령이 본 덱 체크포인트 앞에 글자 그대로 없음 (10-28 사전 공격 A · …): [줄]` · `재개 덱 준비 구간 명령 순서가 본 덱 체크포인트 앞 순서와 다름 (10-28 사전 공격 A · …): [줄] 는 본 덱에서 [줄] 보다 앞에만 있다`.  본 흐름도 같다 (D2 r4 꼴 → 시험 0 · 본 0 · Y6).
    - ⚠ 상태 줄 하나가 본 덱 끝 상태와 다르면 끝 상태 대조 줄 (`재개 지점 … 다름`) 과 이 '글자 그대로 없음' 줄이 **같이** 나온다 (같은 차이 두 줄 · 판정은 같은 거부) — Q5 W1 가지가 그렇다 (아래 Q5).
    - 09-27 r075 실제 압축 쌍 (시험 C1) — dem_restart.py 의 compress 재개 덱은 끝 상태 fix (`integr` · `gravi 9.81` · `damp 0.5`) 를 판 메시 fix 앞에 둔다 (본 덱 = 판 메시 fix 뒤 Phase 2) → 압축 거부 줄에 순서 줄 `[fix top_mesh … plate_pse_r075_a_r30.stl …] 는 본 덱에서 [fix damp all viscous 0.5] 보다 앞에만 있다` 가 더해진다 (시험 기대 = 문제 2).  settling 재개 (D2 r4) 는 통과 · 실제 dem_restart.py **after_settling** 재개 덱은 리포에 없어 새 순서 규칙으로 돌려 보지 못했다 (체크포인트 앞 상태가 Phase 1 fix 뿐이라 같은 순서일 것 = 추정).  시험 P10 · G5 의 합성 `if … print` 블록은 본 덱 순서 자리 (PHASE 1 print 앞) 로 옮겼다 (시험 뜻 그대로).
  - **B (KG50P-02 · P2)** restart 체크포인트가 든 본 덱 run 에 꼬리 (every · pre · post · start · stop · upto …) 가 있으면 거부 (`본 덱 체크포인트 run 에 꼬리가 있음 (… 10-28 사전 공격 B …): [run …]`) — 재개 덱 첫 긴 run 은 꼬리 없는 `run N` 한 줄이라 같은 동작을 낼 수 없다.  다룰 수 없는 구문 검사 (include · next · jump · 이름 변수) 가 `run … every M "명령" …` 안 명령까지 본다 (Y7c).
  - **C (KG50P-03 · P3 · Codex §10-5)** 실행 영수증 — 시험을 내면 시도 폴더 `main_inputs.sha256` (작업 폴더 재개 덱 · 러너) 와 `tool.txt` 의 재개 덱 · 러너 · 시험 덱 · 시험 러너 · 체크포인트 sha256 · `lmp_mpi` 경로 + sha256 (이 셸 PATH 에서 찾은 것 · 잡 환경은 다를 수 있다 · 없으면 `없음`).  본 제출 바로 전 `sha256sum -c` — 다르면 본 제출 안 함 (`작업 폴더 재개 덱 · 러너가 시험 때와 다름 (sha256 ≠ …/main_inputs.sha256 · 10-28 사전 공격 C)`).
  - **D (KG50P-04)** 본 sbatch 출력 = 시험 (Q9d) 과 같은 규칙: 종료 코드 0 · `id` 또는 `id;cluster` (→ `id`) — 아니면 ✅ 줄을 안 찍고 `⛔ 본 제출 실패 (sbatch 종료 코드 … · 출력 […] · job 번호 꼴 아님 · 10-28 사전 공격 D — 큐를 손으로 확인)` · `result.txt` 에 적고 `main_job.txt` 는 안 쓴다.
  - **E (KG50P-05)** G3 `sane()` — 비교 칸이 전부 유한한 수 (정규식 · `nan` · `NaN` · `+nan` · `-nan` · `inf` · `-inf` · `Infinity` 어느 철자든 거부) · 두 줄의 칸 이름 · 순서가 같아야 · 판정 (원자 수 · KE 또는 압력 5 %) 은 예전 그대로.  mawk · gawk 같은 판정 (예전: mawk 는 `nan` 을 통과시켜 본 제출 · gawk 는 `nan` 을 0 으로 읽어 막고 `±nan` 은 통과).  보고 G3 줄 = `비교 칸이 유한한 수가 아님 · 칸 이름 다름 (10-28 사전 공격 E)`.
  - **F (KG50P-06)** 케이스 이름 = `^[A-Za-z0-9_][A-Za-z0-9_.-]*$` 만 (/ · 공백 · `.` · `..` · 글로브 글자 = 시험 전 거부 `케이스 이름` · 새 폴더 없음) · 케이스 목록 = 인자 하나하나 (낱말 나누기 · 글로브 없이) — 이 규칙에서는 서로 다른 두 철자가 같은 폴더를 가리킬 수 없다 (`C ./C` → `./C` 시험 전 거부 · 같은 이름 두 번 = 예전 Q9 규칙).  둘째 고리에서 시도 기록 (`mode.txt` · `lastrun_n.txt`) 을 못 읽거나 숫자 칸이 숫자가 아니면 그 케이스 본 제출 안 함 (`- ⛔ 본 제출 안 함 — 시도 폴더 기록 (mode.txt · lastrun_n.txt) 을 못 읽음 (10-28 사전 공격 F …)` · 예전 = 첫 고리 값이 남아 그 값으로 판정).
  - 도구 머리 주석 (규칙 원문) 의 깨진 보장 문장 셋 (뒤 구간 꼬리 · 상태 = 끝 표뿐 · include 자리) 을 고치고, 위 개정 4 본문 넷 (뒤 구간 · 상태 · include '어디서든' · 허용 차이 '그 밖 = 거부') 에 ⚠ 정정 표지를 달았다.
- 시험 빈틈 셋 (리뷰어 돌연변이 생존 · 시험만 더함): Y16 = 본 덱이 삽입 fix 를 unfix 안 하고 재개 덱이 그 줄을 본 덱 순서 자리에 다시 선언 → 거부 (py_reinsert) · Y17 = 시험 setup 줄 KE 0.1000 → 0.1003 (G1 만 실패) → 본 0 (sh_g1) · Y18 = 시험 로그에서 22000 줄 하나만 빠짐 → G3 결손 → 본 0 (sh_miss).
- 시험 = `scripts/test_resume_ckpt.py` 216 개 (개정 4 의 179 + 묶음 Y 37).  시험 먼저 커밋의 시험 파일로 고치기 전 판 (`fb334928…`) = Python 3.11.15 + mawk 1.3.4: 186 PASS · 30 FAIL · 3.11 + GNU Awk 5.2.1 (스크래치에 푼 패키지 · PATH 앞에만 · 시스템 awk 그대로): 189 · 27 (gawk 는 E 의 `nan` · `NaN` · 원 로그 nan 을 0 으로 읽어 막는다) · 3.8.20 (`-I`) + mawk: 186 · 30 — 실패는 전부 묶음 Y (옛 179 통과).  고침 커밋에서 C1 기대를 바꾼 뒤의 최종 시험 파일로는 185 · 31 · 188 · 28 · 185 · 31 (C1 하나 더) → 고친 판 216 PASS · 0 FAIL (세 환경 모두 · ≈ 90 s).
  - 옛 판 대조 (`--compare-old <e59c43e6 판>`): 예전부터 있던 묶음 (K S D Q T N F C A P W) 의 둘 다 정상 장면 **다름 0** · 새 묶음의 둘 다 정상 장면 다름 5 = 보고만 (R13 · G6 ② · I7 = 개정 4 때 셋 + Y10 · Y10b 본 sbatch 출력 줄) · 옛 판 정상 · 새 판 거부 56 (개정 4 때 43 + 묶음 Y).
  - 돌연변이 (이 판에서 관문 하나씩 끔) 43 = 개정 4 의 28 + 새 관문 12 (A 글자 · 순서 · 부르기 · B 꼬리 · run every · C sha256 대조 · 영수증 · D sbatch 꼴 · E 유한 수 · F 이름 · 배열 · 시도 기록 읽기) + 리뷰어 빈틈 3 → 잡힘 41 · 생존 2 = 개정 4 때와 같은 둘 (자른 시험 덱 다시 읽기 대조 · 셸 시험 예산 대조 — 절단기 · `--trial-steps` 가 맞는 한 닿지 않는 이중 방어).  A 의 두 반쪽은 D2 r4 꼴을 서로 겹쳐 막고 (글자만 끄면 순서가 · 순서만 끄면 글자가 잡는다) 각자만 잡는 시험이 있다 (글자 = Y1 · Y2 · Y5 · 순서 = C1 · Y3b · Y4).
  - 리뷰어 돌연변이 (`fb334928…` 판 · 59 개) = 잡힘 40 · 생존 19 (시험 빈틈 3 + 이중 방어 16 · 리뷰어 집계 · 다시 돌리지 않음) → 빈틈 3 (py_reinsert · sh_g1 · sh_miss) 을 이 판에서 같은 꼴로 끄면 새 시험 Y16 · Y17 · Y18 이 잡는다 (위 V1–V3).
  - `docs/dem1/kg50_watch/test_kg50_watch.sh` = ✅ 165 · ❌ 0 (mawk · gawk 5.2.1).
  - 실제 D2 덱 (ibb 328599 의 받은 r4 · 본 덱 `input_kg50_d2_b50.liggghts`): `-C` r4 (`run 180000`) = 통과 (문제 0) · 157 행 `run 179999` 사본 = 문제 하나 `남은 step 다름: 재개 끝 200000 ↔ 본 덱 그 run 끝 200001 ([run 179999])` · `--fix-run` 결과 = 받은 r4 와 바이트 같음 · `--cut-trial` (2000) = 받은 r4t 와 바이트 같음 (`180000 2000 0 157`) · `--trial-steps` = `2000 1 [run 2000]` · 리뷰어 반례 A (r4 + 변수 바꿨다 되돌림) = 문제 둘 (글자 · 순서) · B (본 덱 `run 200000 every 1000 "velocity …"`) = 꼬리 거부.
- Q5 (메인 통합 트리 HEAD 를 임시 worktree 로 꺼내 이 판 도구만 넣고 돌림 · Q5 파일 안 고침 · 끝나고 지움):
  - W2 A · F = 등록 §12-4 넷과 같음.
  - W1 A · F · A3 = 문제 **넷** — 등록 셋의 3 번째 자리에 새 줄 `재개 덱 준비 구간 상태 명령이 본 덱 체크포인트 앞에 글자 그대로 없음 (10-28 사전 공격 A · LIGGGHTS 는 ${x} 를 그 자리에서 치환한다 — 끝 상태만 같아서는 안 된다): [restart 0]` (등록된 가지 바꿈 165 행 `restart 0` · 4 번째 줄 `재개 지점 restart 다름` 과 같은 차이) · F3 = A3 덱 그대로라 돌리지 않음.  ⇒ `scripts/kg50_q5_branches.py --selftest` = `FAIL (81/97)` · `scripts/kg50_q5_verdict.py --selftest` = `FAIL (6/21)` (같은 트리에 `fb334928…` 판 = `PASS (151/151)` · `PASS (98/98)`).  ⬜ 등록 §12-4 W1 을 넷으로 고칠지 · 도구가 끝 상태 대조와 같은 차이를 한 줄로 줄일지 = 1저자 (이 판에서 정하지 않았다).
- 이 개정 판 `scripts/resume_ckpt.sh` sha256 = `77c242375c4093023e609703ef471c64c2370d374e7533824412d96da5b1b9f8` (개정 4 판 `fb334928…` 에서 바뀜) — ibb 사본을 바꿀 때 대조하고, 본 제출 `-A` 값이 된다.
- 한계 (사전 공격 G–J · 이 판에서 고치지 않음):
  - **G (KG50P-07)** 큐 이름 검사 = `C` · `C_ins` · `C_<이번 SFX>[t]` · `C_r<N>[t]` 만 — 앞 호출이 다른 `-x foo` 였으면 그 `C_foo` 잡을 못 본다 (같은 케이스 본 런 둘 가능 · 고치기 전 판도 같음) → 본 제출 전 `squeue` 를 손으로도 본다.
  - **H (KG50P-08)** 체크포인트 대조 = 파일 이름 (basename) 만 — `-C` 에 다른 케이스 폴더의 같은 이름 체크포인트 (`../kg50_d07_b50/restart_kg50_d07_b50/restart_settling_20001.bin`) 와 그 줄을 쓴 재개 덱을 주면 통과한다 (이 판에서 실측 · 문제 0).  본 흐름은 도구가 그 케이스 폴더에서 체크포인트를 고르고 G1 (원자 수 · KE) 이 잡는다.
  - **I (KG50P-09)** 낱말 나누기가 LIGGGHTS 와 다르다 — NBSP · `viscous&` 뒤 줄바꿈 `1.0e-5` (`&` 이음) · CR 만 쓴 덱은 `-C` 통과 · LIGGGHTS 쪽이 오류로 멈추거나 아무것도 안 해 시험 덱 자르기 · G0 가 막는다 (닫힌 실패 · 손으로 본다).
  - **J (KG50P-10)** 허용 차이 ② (판 메시 `file` 이름) = 그 파일이 있는지만 · 내용 (판 높이) 은 안 본다 (after_settling 은 G2 의 `PLATE HEIGHT` 줄이 본다).  KG50P-10 의 '준비 구간 fix 순서 바꿈 통과' 는 A 로 닫혔다 (Y4).
  - 개정 4 한계 (실제 ibb 덱 · 로그로 안 돌림 · CRLF · region · group · `upto`) 그대로.  awk = mawk 1.3.4 · GNU Awk 5.2.1 (스크래치 패키지) 로 돌림 · ibb 의 실제 gawk 판으로는 아직.
