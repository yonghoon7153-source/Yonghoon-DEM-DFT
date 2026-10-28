# kit_lib.sh — DEM1 테스트 공용 (목업 홈 + Slurm 흉내 + 진짜 LIGGGHTS). 테스트 전용 · 샌드박스에서만 (pkill -x lmp_mpi/mpirun 씀 — IBB 에서 돌리지 말 것)
KIT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
TOOL=${TOOL:-$KIT/../tool/th_grid.sh}; TOOL=$(cd "$(dirname "$TOOL")" && pwd)/$(basename "$TOOL")
WORK=${WORK:-$KIT/work}; B=$WORK/bin
LMP=${LMP:-$(command -v lmp_mpi 2>/dev/null)}; [ -x "$LMP" ] || LMP=$HOME/lig/LIGGGHTS-PUBLIC/src/lmp_novtk
[ -x "$LMP" ] || { echo "⛔ LIGGGHTS 실행파일 없음 — LMP=/path/lmp 로 주거나 bash $KIT/build_liggghts.sh"; exit 1; }
PASS=0; FAIL=0; FAILS=
setup_bin(){ rm -rf $B $WORK/binw; mkdir -p $B $WORK/binw
  cp $KIT/slurm.py $B/slurm.py; chmod +x $B/slurm.py; for c in squeue sbatch scancel scontrol sacct; do ln -sf slurm.py $B/$c; done
  ln -sf "$LMP" $B/lmp_mpi; printf '#!/bin/bash\nexit 0\n' > $B/conda; chmod +x $B/conda
  sed "s#@REAL@#$LMP#" $KIT/lmp_wrap.sh > $WORK/binw/lmp_mpi; chmod +x $WORK/binw/lmp_mpi; }
export USER=yonghoon MOCK_REQUIRE_CONF=1 OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1 OMPI_MCA_rmaps_base_oversubscribe=1
export PATH=$B:/usr/local/bin:/usr/bin:/bin
hdr(){ echo; echo "################ $*"; }
ok(){ echo "  ✅ $*"; PASS=$((PASS+1)); }
ng(){ echo "  ❌ $*"; FAIL=$((FAIL+1)); FAILS="$FAILS
   - $*"; }
chk(){ local d=$1; shift; if "$@" > /dev/null 2>&1; then ok "$d"; else ng "$d"; fi; }
report(){ echo; echo "════ 결과: ✅ $PASS · ❌ $FAIL ════"; [ $FAIL = 0 ] || { echo "실패:$FAILS"; return 1; }; }
cleanup(){ [ -n "$T" ] && [ -d $T/state ] && touch $T/state/daemon.stop; pkill -x lmp_mpi 2>/dev/null; pkill -x mpirun 2>/dev/null; sleep 1; }
newhome(){ # 이름 → 빈 목업 홈 + Slurm 흉내 데몬 (QoS·시간제한은 MOCK_QOS_CAP·MOCK_TLIMIT)
  cleanup; T=$WORK/$1; H=$T/home; rm -rf $T; mkdir -p $T/state $H/dem_test/a6_p08
  export HOME=$H MOCK_SLURM_STATE=$T/state
  printf 'export PATH=%s:/usr/local/bin:/usr/bin:/bin\nexport OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1 OMPI_MCA_rmaps_base_oversubscribe=1 OMPI_MCA_ras=^slurm OMPI_MCA_plm=^slurm\n' $B > $H/.bashrc
  printf '#!/bin/bash\n#SBATCH --job-name=a6_p08\n#SBATCH --output=logs/output_%%x_%%j.out\n#SBATCH -n 20\n\nsource ~/.bashrc\nconda activate myenv\nexport OMP_NUM_THREADS=1\ncd ~/dem_test/a6_p08\nmpirun --oversubscribe --bind-to none -np 20 lmp_mpi -in input_a6_p08.liggghts\n' > $H/dem_test/a6_p08/run_a6_p08.sh
  cp "$TOOL" $H/th_grid.sh
  ( cd $T && nohup python3 $B/slurm.py _daemon > $T/daemon.log 2>&1 & ); }
fresh(){ # 이름 케이스… → newhome + 진짜 gen + 남길 케이스만 + 덱 축소(상자 0.02·H 0.03·run 짧게) + 코어 NPT(기본 2)
  local n=$1 C; shift; newhome $n
  ( cd $H && bash ~/th_grid.sh gen > $T/gen.out 2>&1 )
  for C in th3_85 th3_80 th3_75 th45_85 th45_75 th9_80; do case " $* " in *" $C "*) ;; *) rm -rf $H/dem_test/$C;; esac; done
  for C in "$@"; do ( cd $H/dem_test/$C && python3 $KIT/mkdeck_th.py ${PSPEED:-0.5} input_$C.liggghts input_${C}_ins.liggghts > /dev/null ) && sed -i -E "s/^(#SBATCH +-n +)[0-9]+/\1${NPT:-2}/" $H/dem_test/$C/run_$C.sh; done; }
tg(){ ( cd $H && bash ~/th_grid.sh "$@" ); }
qempty(){ [ -z "$(squeue -u x -h -o %i)" ]; }
waitq(){ local i; for i in $(seq 1 ${1:-600}); do qempty && return 0; sleep 1; done; echo "  (큐가 ${1:-600}초 안에 안 비었음)"; return 1; }
waitfor(){ local i; for i in $(seq 1 ${2:-600}); do eval "$1" && return 0; sleep 1; done; echo "  (시간초과: $1)"; return 1; }
logs(){ ls -tr $H/dem_test/logs/output_$1_*.out 2>/dev/null; }
lastlog(){ ls -t $H/dem_test/logs/output_$1_*.out 2>/dev/null | head -1; }
ck(){ ls $H/dem_test/$1/restart_$1 2>/dev/null | sed -nE 's/^restart_compress_([0-9]+)\.bin$/\1/p' | sort -n | tail -1; }
s2(){ cat $(logs $1) /dev/null | awk '/^====== PHASE 2: STABILIZE ======$/{f=1;next} f && $1~/^[0-9]+$/ && NF>=4 {print $1; exit}'; }
s4(){ local L S; for L in $(ls -t $H/dem_test/logs/output_$1_*.out 2>/dev/null); do S=$(awk '/^====== PHASE 4: RELAXATION ======$/{f=1;next} f && $1~/^[0-9]+$/ && NF>=4 {print $1; exit}' $L); [ -n "$S" ] && { echo $S; return; }; done; }
fe(){ awk '$1~/^[0-9]+$/ && NF>=4 {s=$1} END{print s}' $(lastlog $1); }
natoms(){ cat $(logs $1) /dev/null | awk '$1~/^[0-9]+$/ && $2~/^[0-9]+$/ && NF>=3 && $2>0 {a[$2]=1} END{n=0; for(k in a) n++; print n}'; }
errs(){ cat $(logs $1) /dev/null | grep -acE '^ERROR( on proc [0-9]+)?:'; }
grepq(){ grep -aq -- "$1" "$2"; }
