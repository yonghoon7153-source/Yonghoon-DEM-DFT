#!/bin/bash
# pp_elf_cdd_kisti.sh — b2o3 ELF (plot_num=8) + CDD densities (rho_scf, rho_atomic)
# on KISTI, REUSING the existing champion SCF save (tmp/b2o3.save). No new expensive SCF.
#
#   sbatch tools/electronic/pp_elf_cdd_kisti.sh
# Produces (in /scratch/x3430a02/kgy/b2o3_eos):
#   b2o3_elf.cube          ELF (slide-19 style, free-S lone pair / B-S,P-O covalency)
#   b2o3_rho_scf.cube      SCF valence density   } CDD = rho_scf - rho_atomic
#   b2o3_rho_atomic.cube   atomic superposition  }  (run tools/electronic/cube_diff.py)
#
#SBATCH -J llm_finetuning_ppb2o3
#SBATCH -p amd_a100nv_8
#SBATCH -N 1
#SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:1
#SBATCH --time=02:00:00
#SBATCH --comment pytorch
#SBATCH -o logs/ppb2o3_%j.out
#SBATCH -e logs/ppb2o3_%j.err
set +H
cd "${SLURM_SUBMIT_DIR:-/scratch/x3430a02/kgy/b2o3_eos}"; mkdir -p logs
source /scratch/x3430a02/mjs0000/miniforge3/etc/profile.d/conda.sh 2>/dev/null || true
conda activate uma 2>/dev/null || true
GPU=/scratch/x3430a02/kgy/apps/qe-gpu/bin        # pw.x (GPU, for the quick atomic SCF)
CPU=/scratch/x3430a02/kgy/apps/qe-cpu/bin        # pp.x (CPU build = reliable post-proc)
echo ">> start $(date +%H:%M:%S)  cwd=$(pwd)"
test -d ./tmp/b2o3.save || { echo "ERROR: ./tmp/b2o3.save 없음 (SCF save 경로 확인)"; exit 1; }

# ---- 1) ELF (plot_num=8) — reuse the SCF wavefunctions in tmp/b2o3.save ----
cat > pp_elf.in <<'EOF'
&INPUTPP
  prefix='b2o3', outdir='./tmp', plot_num=8, filplot='b2o3_elf'
/
&PLOT
  iflag=3, output_format=6, fileout='b2o3_elf.cube'
/
EOF
echo ">> ELF pp.x $(date +%H:%M:%S)"
mpirun -np 8 "$CPU/pp.x" -in pp_elf.in > pp_elf.out 2>&1
echo "   ELF: $(ls -la b2o3_elf.cube 2>/dev/null || echo FAIL) ; tail: $(tail -2 pp_elf.out | tr '\n' ' ')"

# ---- 2) SCF valence density (plot_num=0) for CDD ----
cat > pp_rho.in <<'EOF'
&INPUTPP
  prefix='b2o3', outdir='./tmp', plot_num=0, filplot='b2o3_rho'
/
&PLOT
  iflag=3, output_format=6, fileout='b2o3_rho_scf.cube'
/
EOF
echo ">> rho_scf pp.x $(date +%H:%M:%S)"
mpirun -np 8 "$CPU/pp.x" -in pp_rho.in > pp_rho.out 2>&1

# ---- 3) atomic-superposition density (mixing_beta=0) for CDD -> tmp_atomic ----
#     copy the champion SCF input, freeze density at the free-atom superposition.
test -f b2o3_scf.in || { echo "b2o3_scf.in 없음 (STEP3 skip; CDD atomic 못 만듦)"; exit 0; }
python3 - <<'PY'
import re
s = open("b2o3_scf.in").read()
s = re.sub(r"outdir\s*=\s*'[^']*'", "outdir='./tmp_atomic'", s)
if re.search(r"mixing_beta\s*=", s): s = re.sub(r"mixing_beta\s*=\s*[0-9.eEdD+\-]+", "mixing_beta=0.0", s)
else: s = re.sub(r"(&electrons[^\n]*\n)", r"\1  mixing_beta=0.0,\n", s, count=1, flags=re.I)
if re.search(r"electron_maxstep\s*=", s): s = re.sub(r"electron_maxstep\s*=\s*[0-9]+", "electron_maxstep=1", s)
else: s = re.sub(r"(&electrons[^\n]*\n)", r"\1  electron_maxstep=1,\n", s, count=1, flags=re.I)
open("b2o3_scf_atomic.in","w").write(s); print("-> b2o3_scf_atomic.in (mixing_beta=0, maxstep=1, outdir=tmp_atomic)")
PY
echo ">> atomic SCF (GPU) $(date +%H:%M:%S)"
mpirun -np 1 "$GPU/pw.x" -npool 1 -in b2o3_scf_atomic.in > scf_atomic.out 2>&1
grep -qiE "JOB DONE|convergence NOT" scf_atomic.out || { echo "atomic SCF 이상 — tail:"; tail -8 scf_atomic.out; }
cat > pp_atomic.in <<'EOF'
&INPUTPP
  prefix='b2o3', outdir='./tmp_atomic', plot_num=0, filplot='b2o3_rho_at'
/
&PLOT
  iflag=3, output_format=6, fileout='b2o3_rho_atomic.cube'
/
EOF
echo ">> rho_atomic pp.x $(date +%H:%M:%S)"
mpirun -np 8 "$CPU/pp.x" -in pp_atomic.in > pp_atomic.out 2>&1

echo ">> DONE $(date +%H:%M:%S)"
ls -la b2o3_elf.cube b2o3_rho_scf.cube b2o3_rho_atomic.cube 2>/dev/null
echo "CDD 다음: python3 tools/electronic/cube_diff.py (b2o3_rho_scf.cube - b2o3_rho_atomic.cube)"
