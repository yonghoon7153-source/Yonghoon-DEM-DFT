#!/usr/bin/env bash
# =============================================================================
# run_comp2_elastic_dft_gabia.sh — comp2 v3 champion DFT elastic (lpsocl suite와 동일 방법).
#   12 relaxed-ion strains (6 Voigt × ±0.005) -> full Cij -> VRH B/G/E.
#   recipe = comp2 DFT-relax와 동일(kjpaw 60/480, mv 0.01, k222). src = comp2_relax/relax.{in,out}.
#   build_elastic_strain_inputs.py -> 12 pw.x relax -> fit_elastic_cij_stress.py.  (lpsocl elastic stage 복제)
#
# ⚠ pw.x라 UMA(MD/elastic-mlip/phonon)와 GPU 동시 실행 금지(CLAUDE.md VRAM 규율).
#   -> wait_free_gpu가 UMA 프로세스 끝나길 대기. 즉 conductivity MD 끝난 뒤 자동 시작.
#   지금 걸어두면 대기하다 MD 종료 시 12 strain 순차 진행(~few h). 병렬로 당장 원하면 KISTI로.
#
#   gabia(root): tmux new -s c2eldft -d 'bash tools/elastic/run_comp2_elastic_dft_gabia.sh > ~/comp2_elastic_dft.log 2>&1'
# =============================================================================
set -u; set +H
REPO=${REPO:-$HOME/Yonghoon-DEM-DFT}; [ -d "$REPO" ] || REPO=$HOME/work/Yonghoon-DEM-DFT
RELWORK=${RELWORK:-/data/work/runs/comp2_relax}
WORK=${WORK:-/data/work/runs/comp2_elastic_dft}; mkdir -p "$WORK"
PSE=$RELWORK/pseudo
[ -f "$RELWORK/relax.out" ] || { echo "ERROR: $RELWORK/relax.out 없음 (comp2 relax 먼저)"; exit 1; }
[ "$(pgrep -fc run_comp2_elastic_dft)" -le 2 ] || { echo "이미 실행중"; exit 1; }

# gabia QE-GPU env (lpsocl suite와 동일)
HPCX=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi
export PATH=$HPCX/bin:$PATH
export LD_LIBRARY_PATH=$HPCX/lib:/data/apps/nvhpc/Linux_x86_64/24.11/compilers/lib:/usr/local/cuda-12.6/lib64:${LD_LIBRARY_PATH:-}
export OPAL_PREFIX=$HPCX OMP_NUM_THREADS=1 CUDA_VISIBLE_DEVICES=0 OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
QE=/data/apps/qe-7.4.1-gpu/bin; MPIRUN=$HPCX/bin/mpirun
ts(){ date +%H:%M:%S; }

wait_free_gpu(){   # UMA(pw.x+UMA 금지) 대기 후 VRAM 확인
  while pgrep -f 'disorder_ensemble|elastic_mlip|comp_phonon_uma' >/dev/null 2>&1; do
    echo "[$(ts)] UMA(MD 등) 실행중 — pw.x 공존 금지, 5분 대기"; sleep 300
  done
  local need=${1:-6000} free
  while :; do
    free=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits -i 0 2>/dev/null | head -1); [ -z "$free" ] && free=0
    [ "$free" -ge "$need" ] && { echo "[$(ts)] GPU free ${free} MiB >= ${need} — go"; return; }
    echo "[$(ts)] GPU free ${free} < ${need} — 대기"; sleep 60
  done
}
run_pw(){   # $1=in $2=out (skip if JOB DONE)
  grep -q "JOB DONE" "$2" 2>/dev/null && { echo "[$(ts)] $2 DONE — skip"; return 0; }
  wait_free_gpu 6000
  echo "[$(ts)] pw.x $1"
  "$MPIRUN" -np 1 "$QE/pw.x" -npool 1 -in "$1" > "$2" 2>&1
  grep -q "JOB DONE" "$2" && echo "[$(ts)] $1 OK" || { echo "[$(ts)] $1 FAIL:"; tail -12 "$2"; return 1; }
}

# ---- strain 입력 12개 생성 (comp2 relax를 src로, relaxed-ion, k222) ----
if [ ! -f "$WORK/strain_11_p.in" ]; then
  echo "[$(ts)] build 12 strain inputs (relaxed-ion, ±0.005, k222)"
  python3 "$REPO/tools/comp1_v3/build_elastic_strain_inputs.py" --relaxed_ion \
    --src_in "$RELWORK/relax.in" --src_out "$RELWORK/relax.out" \
    --strain 0.005 --workdir "$WORK" --prefix_base strain \
    --kpoints "2 2 2 0 0 0" || { echo "strain 생성 실패"; exit 1; }
fi
cd "$WORK"
TAGS="strain_11_p strain_11_m strain_22_p strain_22_m strain_33_p strain_33_m \
      strain_23_p strain_23_m strain_13_p strain_13_m strain_12_p strain_12_m"
for t in $TAGS; do
  sed -i "s|outdir *=.*|outdir='./tmp_$t'|; s|prefix *=.*|prefix='$t'|; s|pseudo_dir *=.*|pseudo_dir='$PSE'|" "$t.in"
done
for t in $TAGS; do run_pw "$t.in" "$t.out" || echo "  ($t FAIL — fit 전 재실행 필요)"; done

echo "[$(ts)] fit Cij -> VRH:"
python3 "$REPO/tools/modelc_v3/fit_elastic_cij_stress.py" --workdir "$WORK" --strain 0.005 \
  | tee "$WORK/elastic_fit.txt" || echo "fit FAIL (미완 strain 확인)"
echo ""; echo ">> elastic_fit.txt 붙여줘 — comp2.json elastic_dft_v3 등록 + comp1(E_VRH) 비교표(슬라이드 iii)."
