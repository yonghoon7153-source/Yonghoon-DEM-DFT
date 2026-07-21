#!/usr/bin/env bash
# =============================================================================
# run_phaseB_refine_gabia.sh — DFT+U refine of SDCP LiNiO2 binding at the
# IMAGE-CLEAN UMA preferred poses (c40 tall-vacuum re-screen champions):
#   doped   = sulfonate_down_r90   (image-clean champion, -4.203 UMA)
#   neutral = chelation_r0         (neutral champion,       -2.673 UMA)
#
# WHY: the vertical protocol FORCED doped into the neutral pose -> biased ("약화").
# This scores each state in its OWN preferred, image-clean pose (the standard
# way). Verdict = E_bind(doped) - E_bind(neutral); SLAB CANCELS, so 2 complexes +
# 2 gas refs already give it (slab only for the absolute E_bind).
#
#   cd ~/Yonghoon-DEM-DFT && git pull   # (or checkout the 3 files)
#   tmux new -s pbrefine -d 'bash tools/sdcp/run_phaseB_refine_gabia.sh > \
#       /data/work/runs/sdcp_linio2_binding/pbrefine.log 2>&1'
# ⚠ pw.x -- run only when NO UMA/pw.x is on the GPU (VRAM). ~하루(복합체 2개가 heavy).
#
# OOM FIX (2026-07-21): c40 dense-FFT grid > 48GB VRAM -> "cufftPlanMany failed"
# killed slab+both complexes at scf#3 (mol boxes fine). DFT only needs the poses,
# not the UMA tall vacuum -> shrink c to zmax(molecule)+10A (~31) + david_ndim 2.
# =============================================================================
set -u; set +H
BASE=/data/work/runs/sdcp_linio2_binding
REPO=${REPO:-$HOME/Yonghoon-DEM-DFT}; [ -d "$REPO" ] || REPO=$HOME/work/Yonghoon-DEM-DFT
OUT=$BASE/phaseB_v7c_refine
SCAN=$BASE/phaseA_v7c_tallvac
UMA_PY=$(ls /data/apps/miniforge3/envs/uma/bin/python3 2>/dev/null || which python3)
echo "REPO=$REPO  UMA_PY=$UMA_PY"

# ---- 0) shrink cell: c40 -> zmax(pose)+10A (VRAM fits; image gap still >=10A) ----
mkdir -p "$OUT"
"$UMA_PY" - "$REPO/db/structures/sdcp_phaseB_slab_c40.vasp" "$SCAN" "$OUT" <<'PYC' || exit 1
import sys, math
vasp, scan, out = sys.argv[1:4]
zmax = 0.0
for tag in ("complex_doped_sulfonate_down_r90", "complex_neutral_chelation_r0"):
    ls = open(f"{scan}/{tag}.xyz").read().split("\n")
    zs = [float(l.split()[3]) for l in ls[2:2 + int(ls[0])]]
    zmax = max(zmax, max(zs))
c_new = max(math.ceil(zmax + 10.0), 29)          # >=10A molecule-top -> image-slab gap
lines = open(vasp).read().splitlines()
assert "Cartesian" in lines[7], "expect Cartesian POSCAR"
lines[4] = f"      0.000000000000     0.000000000000    {c_new:.9f}"
open(f"{out}/slab_cshrink.vasp", "w").write("\n".join(lines) + "\n")
print(f"[cell] pose zmax={zmax:.2f} A -> c={c_new} A (was 40; grid -{(1-c_new/40)*100:.0f}%)  -> slab_cshrink.vasp")
PYC

# ---- 1) generate 5 SCF inputs (uma python = ASE) at the new poses + shrunk slab ----
"$UMA_PY" "$REPO/tools/sdcp/phaseB_v7c_dft_binding.py" \
  --slab "$OUT/slab_cshrink.vasp" \
  --complex_doped   "$SCAN/complex_doped_sulfonate_down_r90.xyz" \
  --complex_neutral "$SCAN/complex_neutral_chelation_r0.xyz" \
  --mol_doped   "$BASE/inputs/sdcp_v7c/sdcp_v7c_doped.xyz" \
  --mol_neutral "$BASE/inputs/sdcp_v7c/sdcp_v7c_neutral.xyz" \
  --ref_scf     "$BASE/reference_dft_v2/scf_u62.in" \
  --afm_mode inplane --mol_vacuum 8 --pseudo_dir /data/work/pseudo \
  --out "$OUT" || { echo "입력생성 실패 (scf_u62.in / 자세 xyz 경로 확인)"; exit 1; }

# big cells: halve Davidson workspace (memory knob, physics-invariant; mol boxes fine as-is)
for j in slab complex_doped complex_neutral; do
  grep -aq diago_david_ndim "$OUT/$j/scf.in" || \
    sed -i '/&ELECTRONS/a\    diago_david_ndim = 2' "$OUT/$j/scf.in"
done
echo "[mem] diago_david_ndim=2 in slab/complex_doped/complex_neutral"

# ---- 2) qegpu env (vertical 러너와 동일) ----
HPCX=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi
export PATH=$HPCX/bin:$PATH
export LD_LIBRARY_PATH=$HPCX/lib:/data/apps/nvhpc/Linux_x86_64/24.11/compilers/lib:/usr/local/cuda-12.6/lib64:${LD_LIBRARY_PATH:-}
export OPAL_PREFIX=$HPCX OMP_NUM_THREADS=1 CUDA_VISIBLE_DEVICES=0
export OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
QE=/data/apps/qe-7.4.1-gpu/bin/pw.x
MPIRUN=$HPCX/bin/mpirun

run_one() {
  local d=$OUT/$1
  grep -aq "JOB DONE" "$d/scf.out" 2>/dev/null && { echo "[$1] done — skip"; return; }
  echo "[$(date +%H:%M:%S)] pw.x $1 (nat $(grep -a 'nat' "$d/scf.in"|head -1|grep -ao '[0-9]*'))"
  cd "$d" && "$MPIRUN" -np 1 "$QE" -npool 1 -in scf.in > scf.out 2>&1
  grep -aq "JOB DONE" "$d/scf.out" && echo "[$1] OK  E=$(grep -a '^!' "$d/scf.out"|tail -1|awk '{print $(NF-1)}')" \
    || echo "[$1] plateau/미수렴 (last-E 채택)"
}
# 복합체 먼저 (verdict 핵심) -> gas -> slab (verdict엔 slab 불필요, 절대값용)
for j in complex_doped complex_neutral mol_doped mol_neutral slab; do run_one "$j"; done

# ---- 3) harvest + verdict (slab-free) ----
echo ""; echo "===== VERDICT ====="
python3 - <<PYH
import re
Ry=13.605693
def E(p):
    try:
        t=open(f"$OUT/{p}/scf.out").read()
        m=re.findall(r"^!\s+total energy\s+=\s+(-\d+\.\d+)",t,re.M) or re.findall(r"total energy\s+=\s+(-\d+\.\d+)",t)
        return float(m[-1]) if m else None
    except FileNotFoundError: return None
e={k:E(k) for k in ["slab","complex_doped","complex_neutral","mol_doped","mol_neutral"]}
print("harvest (Ry):", {k:(round(v,5) if v else None) for k,v in e.items()})
need=["complex_doped","complex_neutral","mol_doped","mol_neutral"]
if all(e[k] is not None for k in need):
    d=(e["complex_doped"]-e["mol_doped"]-e["complex_neutral"]+e["mol_neutral"])*Ry
    print(f"VERDICT  Delta = E_bind(doped,sulfonate) - E_bind(neutral,chelation) = {d:+.3f} eV")
    print(f"  => {'도핑이 결합 강화 (UMA 방향 DFT 확정)' if d<0 else '도핑이 결합 약화'}")
    if e["slab"] is not None:
        ebd=(e["complex_doped"]-e["slab"]-e["mol_doped"])*Ry
        ebn=(e["complex_neutral"]-e["slab"]-e["mol_neutral"])*Ry
        print(f"  절대값: E_bind(doped,sulfonate)={ebd:+.3f} | E_bind(neutral,chelation)={ebn:+.3f} eV")
else:
    print("복합체/가스 일부 미완 — 붙여주면 verdict 계산")
PYH
echo ">> refine DONE (verdict 위)"
