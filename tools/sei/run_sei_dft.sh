#!/usr/bin/env bash
# =============================================================================
# run_sei_dft.sh — SEI 상들의 갭 + DOS/PDOS 체인을 순차 실행한다.
#   ① vc-relax → ② scf → ③ nscf(fixed, 갭) → ④ nscf(dos) → ⑤ dos.x → ⑥ projwfc.x
#
# ⚠ 갭은 ③의 **고유값**으로만 낸다. DOS 문턱 판독 금지(~0.3 eV 과소, CLAUDE.md 규율).
# ⚠ 계가 3–32 원자라 SDCP 슬랩과 달리 메모리 문제가 없다. GPU 하나로 순차면 충분하다.
#
#   bash tools/sei/run_sei_dft.sh            # 전부
#   bash tools/sei/run_sei_dft.sh li2o_mp-1960   # 하나만
# =============================================================================
set -uo pipefail; set +H
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
WORK=${WORK:-/data/work/runs/sei_dft}
QE=${QE:-/data/apps/qe-7.4.1-gpu/bin/pw.x}
DOSX=${DOSX:-/data/apps/qe-7.4.1-gpu/bin/dos.x}
PROJ=${PROJ:-/data/apps/qe-7.4.1-gpu/bin/projwfc.x}
H_MPI=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi
MPIRUN=${MPIRUN:-$H_MPI/bin/mpirun}
export PATH=$H_MPI/bin:$PATH OPAL_PREFIX=$H_MPI OMP_NUM_THREADS=1 CUDA_VISIBLE_DEVICES=0
export OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
export LD_LIBRARY_PATH=$H_MPI/lib:/data/apps/nvhpc/Linux_x86_64/24.11/compilers/lib:/usr/local/cuda-12.6/lib64
ts(){ echo "[$(date +%H:%M:%S)] $*"; }

LOCK=/tmp/sei_dft.lock; exec 9>"$LOCK"
command -v flock >/dev/null && { flock -n 9 || { ts "⛔ 이미 돈다"; exit 0; }; }

TARGETS=("$@"); [ ${#TARGETS[@]} -eq 0 ] && TARGETS=($(ls "$WORK"))

for t in "${TARGETS[@]}"; do
  d="$WORK/$t"; [ -d "$d" ] || { ts "⛔ 없음: $d"; continue; }
  ts "═══ $t ═══"
  cd "$d" || continue

  run(){  # $1=입력 $2=출력 $3=실행파일
    local in=$1 out=$2 exe=${3:-$QE}
    grep -aq "JOB DONE" "$out" 2>/dev/null && { ts "  ✓ $in 이미 완료"; return 0; }
    ts "  ▶ $in"
    $MPIRUN -np 1 --oversubscribe "$exe" -in "$in" > "$out" 2>&1
    if grep -aq "JOB DONE" "$out"; then return 0; fi
    ts "  ✗ $in 실패 — 꼬리:"; tail -6 "$out"; return 1
  }

  run 01_vcrelax.in 01_vcrelax.out || continue
  # ⚠ vc-relax 의 최종 좌표·셀을 scf 이후 입력에 반영해야 한다.
  #   QE 는 vc-relax 뒤 'Begin final coordinates' 블록을 찍는다 — 그걸 스플라이스한다.
  python3 "$REPO/tools/sei/splice_relaxed.py" --out 01_vcrelax.out \
      --targets 02_scf.in 03_nscf_gap.in 04_nscf_dos.in || { ts "  ✗ 기하 승계 실패"; continue; }

  run 02_scf.in 02_scf.out || continue
  run 03_nscf_gap.in 03_nscf_gap.out || continue
  python3 "$REPO/tools/sei/extract_gap.py" --nscf 03_nscf_gap.out --tag "$t" \
      --json "$d/gap.json" || ts "  ⚠ 갭 추출 실패"

  run 04_nscf_dos.in 04_nscf_dos.out || continue
  run 05_dos.in 05_dos.out "$DOSX" || true
  run 06_projwfc.in 06_projwfc.out "$PROJ" || true
  fails=0
  [ -s "$d/gap.json" ] || { ts "  ⚠ gap.json 없음 — 갭 추출 실패"; fails=$((fails+1)); }
  ls "$d"/*.pdos_atm* >/dev/null 2>&1 || { ts "  ⚠ PDOS 없음 — projwfc 실패"; fails=$((fails+1)); }
  [ "$fails" = 0 ] && ts "  ✅ 완료 → $d" || ts "  ⚠ $fails 개 산출 누락 (위 참조) → $d"
  cd - >/dev/null
done

ts "═══ 결산 ═══"
python3 - "$WORK" <<'PYS'
import glob, json, os, sys
w = sys.argv[1]
rows = []
for j in sorted(glob.glob(os.path.join(w, "*", "gap.json"))):
    d = json.load(open(j)); rows.append(d)
if not rows:
    print("  (아직 gap.json 이 없다)"); raise SystemExit
print(f"  {'상':26s} {'VBM':>8s} {'CBM':>8s} {'gap(eV)':>9s}  판정")
for d in rows:
    print(f"  {d['tag']:26s} {d['vbm']:8.3f} {d['cbm']:8.3f} {d['gap']:9.3f}  {d['verdict']}")
print("\n  ⚠ PBE 갭은 이 계열에서 30-50% 과소평가된다 — 실험값과 나란히 놓지 말 것.")
print("  ⚠ 갭은 fixed-occ nscf 고유값이다. DOS 문턱 판독 금지.")
PYS
