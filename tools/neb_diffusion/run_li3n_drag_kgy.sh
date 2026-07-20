#!/usr/bin/env bash
# =============================================================================
# run_li3n_drag_kgy.sh — Li3N drag points p5..p8 on kgy (offload from KISTI).
#
# KISTI chain was slow between 4h segments; kgy is free and ALREADY proven on
# 136-atom Li3N DFT (E_ads p0_min4/saddle3). Runs the constrained-relax drag
# inputs with the qegpu (NVHPC HPC-X) env -- same fix as the b2o3 elastic runner
# (uma env GNU libgomp / unset both crash pw.x; NVHPC libs must be prepended).
#
# Prereqs in $WORK ($HOME/work/li3n_drag):
#   drag_p5.in..drag_p8.in  (from KISTI /scratch/.../li3n_drag_dft, scp'd)
#   pseudo/{li_pbe_v1.4.uspp.F.UPF, N.pbe-n-radius_5.UPF}
#
#   cd ~/Yonghoon-DEM-DFT && git pull
#   tmux new -s li3ndrag -d 'bash tools/neb_diffusion/run_li3n_drag_kgy.sh > ~/work/li3n_drag/run.log 2>&1'
# Points to run via POINTS env (default "5 6 7 8"). Sequential on 1 GPU.
#
# WAIT_FOR (optional): block until $WORK/$WAIT_FOR has "JOB DONE" before starting.
# Used to CHAIN p4 after the running p5-p8 chain finishes, in a separate tmux, so
# the live chain is untouched (GPU-free guard also prevents any overlap):
#   tmux new -s li3np4 -d 'WAIT_FOR=drag_p8.out POINTS=4 bash tools/neb_diffusion/run_li3n_drag_kgy.sh > ~/work/li3n_drag/run_p4.log 2>&1'
# =============================================================================
set -u; set +H
WORK=${WORK:-$HOME/work/li3n_drag}
POINTS=${POINTS:-"5 6 7 8"}
cd "$WORK" || { echo "ERROR: $WORK 없음 (KISTI 전송 먼저)"; exit 1; }

PW=${PW:-$(find "$HOME/apps" -maxdepth 4 -name pw.x -path "*qe*gpu*bin*" 2>/dev/null | head -1)}
[ -n "$PW" ] || { echo "ERROR: pw.x(gpu) 못 찾음"; exit 1; }

# ★ qegpu env (b2o3 러너와 동일): NVHPC libgomp/CUDA/math + HPC-X ompi 를 앞에 prepend
NV="$HOME/apps/nvhpc/Linux_x86_64/24.11"
HPCX="$(ls -d "$NV"/comm_libs/*/hpcx/hpcx-*/ompi 2>/dev/null | sort | tail -1)"
[ -n "$HPCX" ] || { echo "ERROR: hpcx ompi 못 찾음"; exit 1; }
export OPAL_PREFIX="$HPCX" OMP_NUM_THREADS=1
export LD_LIBRARY_PATH="$NV/compilers/lib:$NV/cuda/12.6/lib64:$NV/math_libs/lib64:$HPCX/lib:${LD_LIBRARY_PATH:-}"
export PATH="$(dirname "$PW"):$HPCX/bin:$NV/compilers/bin:$PATH"
MPIRUN="$HPCX/bin/mpirun"
echo "pw.x=$PW  mpirun=$MPIRUN"

# pseudo_dir 을 kgy 로컬로 교정 (입력은 KISTI 절대경로를 가리킴)
PSE="$WORK/pseudo"
[ -d "$PSE" ] || { echo "ERROR: $PSE 없음"; exit 1; }
for p in $POINTS; do
    f=drag_p${p}.in
    [ -f "$f" ] || { echo "[$p] $f 없음 — skip"; continue; }
    sed -i "s|pseudo_dir *=.*|pseudo_dir = '$PSE'|" "$f"
done

E0=""
run_one() {
    local p=$1 f=drag_p${p}.in o=drag_p${p}.out
    if grep -aq "JOB DONE" "$o" 2>/dev/null; then echo "[$p] already done — skip"; return; fi
    # GPU 여유 대기 (타 프로세스 대비)
    while :; do
        free=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits -i 0 2>/dev/null|head -1)
        [ "${free:-0}" -ge 8000 ] && break
        echo "[$(date +%H:%M:%S)] GPU free ${free} < 8000 — wait"; sleep 60
    done
    echo "[$(date +%H:%M:%S)] pw.x drag_p$p (nat 136, relax)"
    "$MPIRUN" -np 1 "$PW" -npool 1 -in "$f" > "$o" 2>&1
    if grep -aq "JOB DONE" "$o"; then
        E=$(grep -a "^!" "$o"|tail -1|awk '{print $(NF-1)}')
        echo "[$p] OK  E=$E Ry"
    else
        echo "[$p] FAIL — tail:"; tail -12 "$o"
    fi
}

# --- optional chain gate: wait for another point to finish (p8 끝나고 p4 이어서) ---
if [ -n "${WAIT_FOR:-}" ]; then
    echo "[$(date +%H:%M:%S)] WAIT_FOR=$WAIT_FOR — 완료(JOB DONE) 대기…"
    while ! grep -aq "JOB DONE" "$WORK/$WAIT_FOR" 2>/dev/null; do sleep 120; done
    echo "[$(date +%H:%M:%S)] $WAIT_FOR 완료 감지 — POINTS='$POINTS' 시작"
fi

for p in $POINTS; do run_one "$p"; done

echo ""; echo "===== drag p5-p8 프로파일 (kgy) ====="
for p in $POINTS; do
    o=drag_p${p}.out
    grep -aq "JOB DONE" "$o" 2>/dev/null && \
      echo "  p$p  $(grep -a '^!' "$o"|tail -1|awk '{print $(NF-1)}') Ry" || echo "  p$p  (미완)"
done
echo "KISTI p0=-2176.45100463 기준 meV 변환은 붙여넣으면 처리 (프로파일 합산)"
