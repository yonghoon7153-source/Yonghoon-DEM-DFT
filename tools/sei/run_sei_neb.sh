#!/usr/bin/env bash
# =============================================================================
# run_sei_neb.sh — SEI 3종의 CI-NEB 을 순차 실행한다 (Li₂S · Li₃P · Li₃PO₄ γ).
#
# ⚠ NEB 은 **이미지마다 SCF** 를 돌린다. 경로 스텝 하나에 (이미지−2) 번의 scf 가 들고
#   그게 수십 번 반복된다 — 갭 계산(scf 1회)의 100 배 급이다. 싼 것부터 순서를 잡는다:
#     li2s(23원자) → li3p(63) → li3po4g(127)
#   앞이 깨지면 뒤는 안 건다. 뒤로 갈수록 비싸므로 진단은 앞에서 끝내는 게 맞다.
#
# ⚠ pw.x 와 UMA 를 동시에 돌리지 않는다 (VRAM 47/48 GB 점유 사례) — nvidia-smi 가드.
#
#   bash tools/sei/run_sei_neb.sh              # 전부 (싼 것부터)
#   bash tools/sei/run_sei_neb.sh li2s         # 하나만
# =============================================================================
set -uo pipefail; set +H
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
WORK=${WORK:-/data/work/runs/sei_neb}
NEB=${NEB:-/data/apps/qe-7.4.1-gpu/bin/neb.x}
H_MPI=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi
MPIRUN=${MPIRUN:-$H_MPI/bin/mpirun}
export PATH=$H_MPI/bin:$PATH OPAL_PREFIX=$H_MPI OMP_NUM_THREADS=1 CUDA_VISIBLE_DEVICES=0
export OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
export LD_LIBRARY_PATH=$H_MPI/lib:/data/apps/nvhpc/Linux_x86_64/24.11/compilers/lib:/usr/local/cuda-12.6/lib64
ts(){ echo "[$(date +%H:%M:%S)] $*"; }

LOCK=/tmp/sei_neb.lock; exec 9>"$LOCK"
command -v flock >/dev/null && { flock -n 9 || { ts "⛔ 이미 돈다"; exit 0; }; }

# ⚠ UMA 가 GPU 를 쥐고 있으면 pw.x 가 OOM 으로 죽는다. 먼저 본다.
if command -v nvidia-smi >/dev/null; then
  used=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | head -1)
  if [ "${used:-0}" -gt 2000 ]; then
    ts "⛔ GPU 가 이미 ${used} MiB 쓰인다 (UMA?). 확인 후 다시 걸 것:"
    nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv
    exit 1
  fi
fi

# 싼 것부터 — 원자 수 순서를 코드에 박아 둔다(알파벳 순이면 li3po4g 가 먼저 온다)
ORDER=(li2s li3p li3po4g)
TARGETS=("$@"); [ ${#TARGETS[@]} -eq 0 ] && TARGETS=("${ORDER[@]}")

for t in "${TARGETS[@]}"; do
  d="$WORK/$t"
  [ -f "$d/neb.in" ] || { ts "⛔ 없음: $d/neb.in — build_neb_inputs.py 부터"; continue; }
  ts "═══ $t ═══"
  cd "$d" || continue
  if grep -aq "neb: convergence achieved" neb.out 2>/dev/null; then
    ts "  ✓ 이미 수렴 — 건너뜀"; cd - >/dev/null; continue
  fi
  # ⚠ neb.x 는 재시작 파일(prefix.path)이 있으면 이어서 돈다. 지우지 말 것.
  nat=$(grep -a -m1 "nat" neb.in | grep -oE "[0-9]+")
  ts "  ▶ neb.x (원자 ${nat:-?})  — 진행은 neb.out 의 'activation energy' 줄로 본다"
  $MPIRUN -np 1 --oversubscribe "$NEB" -inp neb.in > neb.out 2>&1
  if grep -aq "neb: convergence achieved" neb.out; then
    ts "  ✅ 수렴"
    grep -a "activation energy" neb.out | tail -2
  else
    ts "  ⚠ 미수렴 — 꼬리:"; tail -12 neb.out
    ts "     경로 스텝을 더 주려면 neb.in 의 nstep_path 를 늘리고 다시 걸면 이어서 돈다."
    ts "     ⛔ 여기서 멈춘다 — 뒤 계는 더 비싸므로 원인을 먼저 볼 것."
    cd - >/dev/null; break
  fi
  cd - >/dev/null
done

ts "═══ 결산 ═══"
python3 "$REPO/tools/sei/collect_neb.py" --work "$WORK" || true
