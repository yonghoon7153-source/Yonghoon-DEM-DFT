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
