#!/usr/bin/env bash
# =============================================================================
# run_comp2_elastic_uspp_gabia.sh — comp2 elastic = comp1 완전복제.
#   USPP · ecut 52/520 · k444 · smearing mv 0.01 · relaxed-ion (comp1_v3 레시피 그대로).
#   comp2 v3 champion → USPP V0 relax → USPP k444 strain(±0.005) → full Cij → E/B/G_VRH.
#   pseudo: li/s/cl/br v1.4.uspp + P.pbe-n-rrkjus_psl (comp1 set + Br). /data/work/pseudo.
#   → comp1(E_VRH 22.06)과 pseudo·ecut·k·cubic-52·방법 완전 동일 = LPSCl vs LPSClBr 정당 비교.
#   ⚠ comp2 champion(PAW)은 phonon/LOBSTER/gap용으로 그대로 둠 — elastic만 USPP 분리(comp1도 동일 구조).
#   gabia(root): tmux new -s c2eluspp -d 'bash tools/elastic/run_comp2_elastic_uspp_gabia.sh > ~/comp2_elastic_uspp.log 2>&1'
# =============================================================================
set -u; set +H
REPO=${REPO:-$HOME/Yonghoon-DEM-DFT}; [ -d "$REPO" ] || REPO=$HOME/work/Yonghoon-DEM-DFT
WORK=${WORK:-/data/work/runs/comp2_elastic_uspp}; mkdir -p "$WORK"
STRUCT=${STRUCT:-$REPO/db/structures/comp2_V0_v3_relaxed.xyz}
STRAIN=${STRAIN:-0.005}
KLINE=${KLINE:-"4 4 4 0 0 0"}
[ -f "$STRUCT" ] || { echo "ERROR: $STRUCT 없음"; exit 1; }
[ "$(pgrep -fc run_comp2_elastic_uspp)" -le 2 ] || { echo "이미 실행중"; exit 1; }

# gabia QE-GPU env (lpsocl/comp2 suite와 동일)
HPCX=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi
export PATH=$HPCX/bin:$PATH
export LD_LIBRARY_PATH=$HPCX/lib:/data/apps/nvhpc/Linux_x86_64/24.11/compilers/lib:/usr/local/cuda-12.6/lib64:${LD_LIBRARY_PATH:-}
export OPAL_PREFIX=$HPCX OMP_NUM_THREADS=1 CUDA_VISIBLE_DEVICES=0 OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
QE=/data/apps/qe-7.4.1-gpu/bin; MPIRUN=$HPCX/bin/mpirun
ts(){ date +%H:%M:%S; }

wait_gpu(){ local free   # MD(UMA)와 공존; 52원자 소형이라 VRAM 여유만 확인
  while :; do
    free=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits -i 0 2>/dev/null | head -1); [ -z "$free" ] && free=0
    [ "$free" -ge 6000 ] && { echo "[$(ts)] GPU free ${free} MiB — go"; return; }
    echo "[$(ts)] GPU free ${free} < 6000 대기"; sleep 60
  done; }
run_pw(){ grep -q "JOB DONE" "$2" 2>/dev/null && { echo "[$(ts)] $2 DONE skip"; return 0; }
  wait_gpu; echo "[$(ts)] pw.x $1"
  "$MPIRUN" -np 1 "$QE/pw.x" -npool 1 -in "$1" > "$2" 2>&1
  grep -q "JOB DONE" "$2" && echo "[$(ts)] $1 OK" || { echo "[$(ts)] $1 FAIL:"; tail -12 "$2"; return 1; } }

# ── pseudo (comp1 USPP set + Br v1.4.uspp) — find-or-fail ──
PSE=$WORK/pseudo; mkdir -p "$PSE"
NEED="li_pbe_v1.4.uspp.F.UPF P.pbe-n-rrkjus_psl.1.0.0.UPF s_pbe_v1.4.uspp.F.UPF cl_pbe_v1.4.uspp.F.UPF br_pbe_v1.4.uspp.F.UPF"
for p in $NEED; do
  [ -s "$PSE/$p" ] && continue
  src=$(find /data/work/pseudo /data/work/bml/manuscript_support -name "$p" 2>/dev/null | head -1)
  [ -z "$src" ] && src=$(find /data/work/pseudo /data/work/bml -iname "${p%%.*}*uspp*" -o -iname "${p%%.*}*rrkjus*" 2>/dev/null | head -1)
  [ -n "$src" ] && { cp "$src" "$PSE/$p"; echo "  pseudo $p <- $src"; } || { echo "pseudo $p 못찾음"; exit 1; }
done
echo "[$(ts)] pseudo 5종 확보 (USPP: li/s/cl/br v1.4.uspp + P rrkjus)"

# ── comp2 v3 champion(xyz) → USPP V0 relax 입력 (comp1 레시피: 52/520, k444, smearing mv 0.01) ──
if [ ! -f "$WORK/V0_relax.in" ]; then
  echo "[$(ts)] V0_relax.in 생성 (ase, comp1 레시피)"
  python3 - "$STRUCT" "$PSE" "$WORK" << 'PY'
import sys, numpy as np
from ase.io import read, write
struct, pse, work = sys.argv[1], sys.argv[2], sys.argv[3]
a = read(struct)
pseudos = {"Li":"li_pbe_v1.4.uspp.F.UPF","P":"P.pbe-n-rrkjus_psl.1.0.0.UPF",
           "S":"s_pbe_v1.4.uspp.F.UPF","Cl":"cl_pbe_v1.4.uspp.F.UPF","Br":"br_pbe_v1.4.uspp.F.UPF"}
inp = {"control":{"calculation":"relax","restart_mode":"from_scratch","tprnfor":True,"tstress":True,
                  "etot_conv_thr":1e-6,"forc_conv_thr":1e-4,"pseudo_dir":pse,"outdir":"./tmp_v0","prefix":"c2v0"},
       "system":{"ecutwfc":52,"ecutrho":520,"occupations":"smearing","smearing":"mv","degauss":0.01},
       "electrons":{"conv_thr":1e-8,"mixing_beta":0.3},"ions":{"ion_dynamics":"bfgs"}}
write(work+"/V0_relax.in", a, format="espresso-in", input_data=inp,
      pseudopotentials=pseudos, kpts=(4,4,4))
print("V0_relax.in:", len(a), "atoms, V=%.2f A^3" % abs(np.linalg.det(a.cell)))
PY
fi

# ── V0 relax (USPP) ──
cd "$WORK"
run_pw V0_relax.in V0_relax.out || { echo "V0 relax FAIL — tail:"; tail -20 V0_relax.out; exit 1; }

# ── 12 strain 생성 (relaxed-ion, USPP, k444, ±STRAIN) ──
if [ ! -f "$WORK/strain_11_p.in" ]; then
  echo "[$(ts)] build 12 strain (relaxed-ion, ±$STRAIN, k444, USPP)"
  python3 "$REPO/tools/comp1_v3/build_elastic_strain_inputs.py" --relaxed_ion \
    --src_in "$WORK/V0_relax.in" --src_out "$WORK/V0_relax.out" \
    --strain "$STRAIN" --workdir "$WORK" --prefix_base strain \
    --kpoints "$KLINE" || { echo "strain 생성 실패"; exit 1; }
fi
TAGS="strain_11_p strain_11_m strain_22_p strain_22_m strain_33_p strain_33_m \
      strain_23_p strain_23_m strain_13_p strain_13_m strain_12_p strain_12_m"
for t in $TAGS; do
  sed -i "s|outdir *=.*|outdir='./tmp_$t'|; s|prefix *=.*|prefix='$t'|; s|pseudo_dir *=.*|pseudo_dir='$PSE'|" "$t.in"
done
for t in $TAGS; do run_pw "$t.in" "$t.out" || echo "  ($t FAIL — fit 전 재실행 필요)"; done

# ── fit ──
echo "[$(ts)] fit Cij -> VRH (USPP·52/520·k444 = comp1 완전복제):"
python3 "$REPO/tools/modelc_v3/fit_elastic_cij_stress.py" --workdir "$WORK" --strain "$STRAIN" \
  --struct "$STRUCT" | tee "$WORK/elastic_fit.txt" || echo "fit FAIL (미완 strain 확인)"
echo ""; echo ">> elastic_fit.txt 붙여줘 — comp2 E_VRH vs comp1 22.06 (같은 USPP·52/520·k444·cubic-52)."
