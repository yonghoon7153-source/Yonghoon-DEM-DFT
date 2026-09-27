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
