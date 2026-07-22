#!/usr/bin/env bash
# =============================================================================
# run_b2o3_elastic_dft_gabia.sh — b2o3(128atom) DFT relaxed-ion elastic on gabia.
#   comp2/lpsocl 방법: 12 relaxed-ion strain (6 Voigt × ±0.01) → full 6×6 → VRH+Pugh/Debye.
#   ⚠ STRAIN=0.01 (b2o3 shear가 0.005서 국소최소 오염 이력 — kb/results/b2o3_elastic_analysis).
#   recipe = b2o3_paw_scf.in (ecut 60/480, mv 0.01, k 3 3 1, PAW Li-sl/P-n/B-n/S-nl/O-n/Cl-nl).
#   128원자 ecutrho480 → 48GB 필수(24GB는 cuFFT 터짐 확정). build_elastic가 angstrom→crystal 자동.
#
#   준비: ~/work/b2o3_elastic/b2o3_paw_scf.in (KISTI백업서 전송됨).
#   ★comp2 elastic 끝난 뒤 자동 시작(waiter). MD(UMA)와는 공존, 근데 b2o3 큼 → VRAM 감시.
#   gabia: tmux new -s b2oel -d 'bash tools/elastic/run_b2o3_elastic_dft_gabia.sh > ~/b2o3_elastic.log 2>&1'
# =============================================================================
set -u; set +H
REPO=${REPO:-$HOME/Yonghoon-DEM-DFT}; [ -d "$REPO" ] || REPO=$HOME/work/Yonghoon-DEM-DFT
WORK=${WORK:-$HOME/work/b2o3_elastic}
SRC=${SRC:-$WORK/b2o3_paw_scf.in}
STRUCT=${STRUCT:-$REPO/db/structures/b2o3_relaxV0.xyz}
STRAIN=${STRAIN:-0.01}
VRAM_NEED=${VRAM_NEED:-40000}
[ -f "$SRC" ] || { echo "ERROR: $SRC 없음 (KISTI백업 전송 먼저)"; exit 1; }
[ "$(pgrep -fc run_b2o3_elastic_dft)" -le 2 ] || { echo "이미 실행중"; exit 1; }

# gabia QE-GPU env
HPCX=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi
export PATH=$HPCX/bin:$PATH
export LD_LIBRARY_PATH=$HPCX/lib:/data/apps/nvhpc/Linux_x86_64/24.11/compilers/lib:/usr/local/cuda-12.6/lib64:${LD_LIBRARY_PATH:-}
export OPAL_PREFIX=$HPCX OMP_NUM_THREADS=1 CUDA_VISIBLE_DEVICES=0 OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
QE=/data/apps/qe-7.4.1-gpu/bin; MPIRUN=$HPCX/bin/mpirun
ts(){ date +%H:%M:%S; }

# ── comp2 elastic 끝날 때까지 대기 (2 pw.x elastic 동시 회피) ──
while pgrep -f run_comp2_elastic_dft >/dev/null 2>&1; do
  echo "[$(ts)] comp2 elastic 아직 도는중 — b2o3는 그 뒤. 5분 대기"; sleep 300
done
echo "[$(ts)] comp2 elastic 종료 감지 — b2o3 elastic 준비"

wait_vram(){ local free
  while :; do
    free=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits -i 0 2>/dev/null | head -1); [ -z "$free" ] && free=0
    [ "$free" -ge "$VRAM_NEED" ] && { echo "[$(ts)] VRAM free ${free} MiB >= ${VRAM_NEED} — go"; return; }
    echo "[$(ts)] VRAM ${free} < ${VRAM_NEED} 대기 (b2o3 128원자 큼; MD와 공존시 여유 필요)"; sleep 120
  done; }
run_pw(){ grep -q "JOB DONE" "$2" 2>/dev/null && { echo "[$(ts)] $2 DONE skip"; return 0; }
  wait_vram; echo "[$(ts)] pw.x $1"; "$MPIRUN" -np 1 "$QE/pw.x" -npool 1 -in "$1" > "$2" 2>&1
  grep -q "JOB DONE" "$2" && echo "[$(ts)] $1 OK" || { echo "[$(ts)] $1 FAIL(OOM/cuFFT?):"; tail -12 "$2"; return 1; } }

# ── pseudos (b2o3 확장 PAW 6종; find-or-wget) ──
PSE=$WORK/pseudo; mkdir -p "$PSE"
NEED="Li.pbe-sl-kjpaw_psl.1.0.0.UPF P.pbe-n-kjpaw_psl.1.0.0.UPF B.pbe-n-kjpaw_psl.1.0.0.UPF S.pbe-nl-kjpaw_psl.1.0.0.UPF O.pbe-n-kjpaw_psl.0.1.UPF Cl.pbe-nl-kjpaw_psl.1.0.0.UPF"
BASE="https://pseudopotentials.quantum-espresso.org/upf_files"
for p in $NEED; do
  [ -s "$PSE/$p" ] && continue
  f=$(find "$HOME" /data -name "$p" 2>/dev/null | head -1)
  if [ -n "$f" ]; then cp "$f" "$PSE/"; else wget -q "$BASE/$p" -O "$PSE/$p" || true; fi
  [ -s "$PSE/$p" ] || { echo "pseudo $p 확보 실패"; exit 1; }
done

# ── strain 12개 생성 (b2o3_paw_scf.in을 src_in·src_out; k 3 3 1) ──
if [ ! -f "$WORK/strain_11_p.in" ]; then
  echo "[$(ts)] build 12 strain (relaxed-ion, ±$STRAIN, k331)"
  python3 "$REPO/tools/comp1_v3/build_elastic_strain_inputs.py" --relaxed_ion \
    --src_in "$SRC" --src_out "$SRC" --strain "$STRAIN" --workdir "$WORK" \
    --prefix_base strain --kpoints "3 3 1 0 0 0" || { echo "strain 생성 실패"; exit 1; }
fi
cd "$WORK"
TAGS="strain_11_p strain_11_m strain_22_p strain_22_m strain_33_p strain_33_m \
      strain_23_p strain_23_m strain_13_p strain_13_m strain_12_p strain_12_m"
for t in $TAGS; do
  sed -i "s|outdir *=.*|outdir='./tmp_$t'|; s|prefix *=.*|prefix='$t'|; s|pseudo_dir *=.*|pseudo_dir='$PSE'|" "$t.in"
done
for t in $TAGS; do run_pw "$t.in" "$t.out" || echo "  ($t FAIL — fit 전 재실행 필요)"; done

echo "[$(ts)] fit Cij -> VRH (strain $STRAIN):"
python3 "$REPO/tools/modelc_v3/fit_elastic_cij_stress.py" --workdir "$WORK" --strain "$STRAIN" \
  --struct "$STRUCT" | tee "$WORK/elastic_fit.txt" || echo "fit FAIL (미완 strain 확인)"
echo ""; echo ">> elastic_fit.txt 붙여줘 — b2o3 VRH B/G/E + Pugh/Cauchy/경도/Debye 등록 (db/properties)."
