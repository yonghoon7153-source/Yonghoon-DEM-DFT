#!/usr/bin/env bash
# =============================================================================
# run_comp2_lobster_gabia.sh — comp2 v3 champion ICOHP via LOBSTER (lpsocl 방법).
#   all-PAW scf + nscf(nbnd 500, extended basis, ecut 70/560) -> LOBSTER 5.1.1 ICOHP.
#   cohpGenerator: Li-S, Li-Cl, Li-Br, P-S, S-S (build_lobster_paw_inputs.py에 Br 지원 추가).
#
# ⚠ pw.x라 UMA(MD)·elastic-pw.x와 GPU 경합 — 기본 wait(MD+elastic 끝난 뒤). COEXIST=1로 동시 시도
#   (근데 nbnd 500 nscf가 메모리 무거워 3-way는 OOM 위험 — 죽으면 resume-safe로 재실행).
# ⚠ LOBSTER는 crystal 좌표 요구 -> comp2_V0_v3_relaxed.xyz에서 crystal src_out 생성.
#
#   gabia(root): tmux new -s c2lob -d 'bash tools/elastic/run_comp2_lobster_gabia.sh > ~/comp2_lobster.log 2>&1'
# =============================================================================
set -u; set +H
REPO=${REPO:-$HOME/Yonghoon-DEM-DFT}; [ -d "$REPO" ] || REPO=$HOME/work/Yonghoon-DEM-DFT
RELWORK=${RELWORK:-/data/work/runs/comp2_relax}
WORK=${WORK:-/data/work/runs/comp2_lobster}; mkdir -p "$WORK/pseudo"
LOBSTER=/data/apps/lobster-5.1.1/lobster
UMA_PY=$(ls /data/apps/miniforge3/envs/uma/bin/python3 2>/dev/null || which python3)
XYZ=$REPO/db/structures/comp2_V0_v3_relaxed.xyz
[ -f "$RELWORK/relax.in" ] || { echo "ERROR: $RELWORK/relax.in 없음"; exit 1; }
[ -f "$XYZ" ] || { echo "ERROR: $XYZ 없음 (git pull)"; exit 1; }
[ "$(pgrep -fc run_comp2_lobster)" -le 2 ] || { echo "이미 실행중"; exit 1; }

# gabia QE-GPU env
HPCX=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi
export PATH=$HPCX/bin:$PATH
export LD_LIBRARY_PATH=$HPCX/lib:/data/apps/nvhpc/Linux_x86_64/24.11/compilers/lib:/usr/local/cuda-12.6/lib64:${LD_LIBRARY_PATH:-}
export OPAL_PREFIX=$HPCX OMP_NUM_THREADS=1 CUDA_VISIBLE_DEVICES=0 OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
QE=/data/apps/qe-7.4.1-gpu/bin; MPIRUN=$HPCX/bin/mpirun
ts(){ date +%H:%M:%S; }
wait_free_gpu(){
  if [ "${COEXIST:-0}" != 1 ]; then
    while pgrep -f 'disorder_ensemble|elastic_mlip|comp_phonon_uma|run_comp2_md|run_comp2_elastic_dft' >/dev/null 2>&1; do
      echo "[$(ts)] UMA(MD)/elastic 실행중 — pw.x 대기 (동시 원하면 COEXIST=1)"; sleep 300
    done
  fi
  local need=${1:-10000} free
  while :; do
    free=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits -i 0 2>/dev/null | head -1); [ -z "$free" ] && free=0
    [ "$free" -ge "$need" ] && { echo "[$(ts)] GPU free ${free} MiB >= ${need} — go"; return; }
    echo "[$(ts)] GPU free ${free} < ${need} — 대기"; sleep 60
  done
}
run_pw(){ grep -q "JOB DONE" "$2" 2>/dev/null && { echo "[$(ts)] $2 DONE — skip"; return 0; }
  wait_free_gpu "$3"; echo "[$(ts)] pw.x $1"
  "$MPIRUN" -np 1 "$QE/pw.x" -npool 1 -in "$1" > "$2" 2>&1
  grep -q "JOB DONE" "$2" && echo "[$(ts)] $1 OK" || { echo "[$(ts)] $1 FAIL:"; tail -12 "$2"; return 1; } }

# ---- PAW pseudos (extended variants; find-or-wget) ----
PSE=$WORK/pseudo
NEED="Li.pbe-sl-kjpaw_psl.1.0.0.UPF P.pbe-n-kjpaw_psl.1.0.0.UPF S.pbe-nl-kjpaw_psl.1.0.0.UPF Cl.pbe-nl-kjpaw_psl.1.0.0.UPF Br.pbe-n-kjpaw_psl.1.0.0.UPF"
BASE="https://pseudopotentials.quantum-espresso.org/upf_files"
for p in $NEED; do
  [ -s "$PSE/$p" ] && continue
  f=$(find "$HOME" /data -name "$p" 2>/dev/null | head -1)
  if [ -n "$f" ]; then cp "$f" "$PSE/"; echo "[pseudo] $p <- $f"
  else echo "[pseudo] wget $p"; wget -q "$BASE/$p" -O "$PSE/$p" || true
    [ -s "$PSE/$p" ] || { echo "!! $p 확보 실패 (인터넷/프록시)"; exit 1; }; fi
done

# ---- crystal 좌표 src_out 생성 (빌더가 crystal 요구; relax.out은 angstrom) ----
CRYSOUT=$WORK/relaxed_crystal.out
if [ ! -f "$CRYSOUT" ]; then
"$UMA_PY" - "$XYZ" "$CRYSOUT" <<'PY'
import sys, re, numpy as np
xyz, out = sys.argv[1], sys.argv[2]
L = open(xyz).read().splitlines(); nat = int(L[0])
A = np.array([float(x) for x in re.search(r'Lattice="([^"]+)"', L[1]).group(1).split()]).reshape(3,3)
inv = np.linalg.inv(A)
lines = ["ATOMIC_POSITIONS (crystal)"]
for ln in L[2:2+nat]:
    p = ln.split(); s = p[0]; c = np.array([float(x) for x in p[1:4]]); f = c @ inv; f -= np.floor(f)
    lines.append(f"{s:2s} {f[0]:.10f} {f[1]:.10f} {f[2]:.10f}")
open(out, "w").write("\n".join(lines) + "\n")
print(f"crystal src_out -> {out} ({nat} atoms)")
PY
fi

# ---- lobster 입력 (scf/nscf/lobsterin) 생성 ----
if [ ! -f "$WORK/lobster_scf.in" ]; then
  python3 "$REPO/tools/comp1_v3/build_lobster_paw_inputs.py" \
    --src_in "$RELWORK/relax.in" --src_out "$CRYSOUT" \
    --workdir "$WORK" --pseudo_dir "$PSE" --nbnd 500 \
    --kpoints "2 2 2 0 0 0" --ecutwfc 70 --ecutrho 560 || exit 1
fi
grep -q "Li type Br" "$WORK/lobsterin" && echo "[ok] lobsterin에 Li-Br cohpGenerator 포함" || echo "[warn] Li-Br 없음 — 확인 필요"

cd "$WORK"
run_pw lobster_scf.in lobster_scf.out 10000 || exit 1
run_pw lobster_nscf.in lobster_nscf.out 12000 || exit 1
ln -sfn tmp_V0_lobster_scf/V0_lobster_scf.save ./V0_lobster_scf.save 2>/dev/null || true
[ -f lobster_scf.in.orig ] || cp lobster_scf.in lobster_scf.in.orig
cp lobster_nscf.in lobster_scf.in   # LOBSTER는 *scf.in을 QE입력으로 읽음 -> nscf 내용으로 교체

if [ -s ICOHPLIST.lobster ]; then echo "ICOHPLIST 있음 — skip"
else
  export OMP_NUM_THREADS=8; echo "[$(ts)] LOBSTER start (OMP=8, CPU — GPU 안 씀)"
  "$LOBSTER" > lobster_run.out 2>&1; export OMP_NUM_THREADS=1
  echo "==== charge spilling (b2o3 1.19%였음; <5%면 OK) ===="; grep -iE "charge spilling" lobster_run.out | head -4
  echo "==== ICOHPLIST head ===="; head -25 ICOHPLIST.lobster 2>/dev/null || tail -15 lobster_run.out
fi
cp lobster_scf.in.orig lobster_scf.in   # 원복
echo ""; echo ">> ICOHPLIST.lobster + charge spilling 붙여줘 — Li-S/Li-Cl/Li-Br ICOHP 평균 → comp2.json 등록 + comp1 비교(슬라이드 v)."
