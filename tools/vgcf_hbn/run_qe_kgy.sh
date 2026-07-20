#!/usr/bin/env bash
# =============================================================================
# run_qe_kgy.sh — h-BN@VGCF Li-adsorption QE relaxations on kgy (QE-GPU).
#
# First calculation of the new project: does the h-BN|Li|VGCF sandwich anchor Li
# more strongly than the bare surfaces (Shi eq5 test; VGCF vs Cu/Li-metal bottom)?
# Params Shi-2017-matched (QE/PBE, PAW; we use D3-BJ). E_ads vs isolated Li atom.
#
#   cd ~/Yonghoon-DEM-DFT && git pull
#   tmux new -s vgcfqe -d 'bash tools/vgcf_hbn/run_qe_kgy.sh > ~/work/vgcf_hbn/run.log 2>&1'
#   tail -f ~/work/vgcf_hbn/run.log
# =============================================================================
set -u; set +H
REPO=${REPO:-$HOME/Yonghoon-DEM-DFT}; [ -d "$REPO" ] || REPO=$HOME/work/Yonghoon-DEM-DFT
WORK=${WORK:-$HOME/work/vgcf_hbn}
IN="$REPO/tools/vgcf_hbn/qe_inputs"
mkdir -p "$WORK"; cd "$WORK"

# ---- pseudos (PSlibrary PBE kjpaw PAW) ----
PSE=${PSE:-$WORK/pseudo}; mkdir -p "$PSE"
NEED="C.pbe-n-kjpaw_psl.1.0.0.UPF B.pbe-n-kjpaw_psl.1.0.0.UPF N.pbe-n-kjpaw_psl.1.0.0.UPF Li.pbe-s-kjpaw_psl.1.0.0.UPF"
BASE="https://pseudopotentials.quantum-espresso.org/upf_files"
missing=0
for p in $NEED; do
    [ -s "$PSE/$p" ] && continue
    f=$(find "$HOME" -name "$p" 2>/dev/null | head -1)
    if [ -n "$f" ]; then cp "$f" "$PSE/"; echo "[pseudo] $p <- $f"; continue; fi
    echo "[pseudo] wget $p"; wget -q "$BASE/$p" -O "$PSE/$p" 2>/dev/null
    [ -s "$PSE/$p" ] || { echo "  !! $p 확보 실패"; missing=1; }
done
if [ "$missing" = 1 ]; then
    echo "=== pseudo 부족 — kgy에 있는 UPF 목록(호환 대체 고르게) ==="
    find "$HOME" -name "*.UPF" 2>/dev/null | grep -iE "/(C|B|N|Li)[._]" | head -40
    echo ">>> 위 목록 붙여주면 대체 pseudo로 입력 갱신할게 (지금 중단)"; exit 1
fi
echo "[pseudo] OK: $(ls "$PSE" | tr '\n' ' ')"

# ---- qegpu env (drag 러너와 동일: NVHPC/HPC-X prepend) ----
PW=${PW:-$(find "$HOME/apps" -maxdepth 4 -name pw.x -path "*qe*gpu*bin*" 2>/dev/null | head -1)}
[ -n "$PW" ] || { echo "ERROR: pw.x(gpu) 못찾음"; exit 1; }
NV="$HOME/apps/nvhpc/Linux_x86_64/24.11"
HPCX="$(ls -d "$NV"/comm_libs/*/hpcx/hpcx-*/ompi 2>/dev/null | sort | tail -1)"
[ -n "$HPCX" ] || { echo "ERROR: hpcx 못찾음"; exit 1; }
export OPAL_PREFIX="$HPCX" OMP_NUM_THREADS=1
export LD_LIBRARY_PATH="$NV/compilers/lib:$NV/cuda/12.6/lib64:$NV/math_libs/lib64:$HPCX/lib:${LD_LIBRARY_PATH:-}"
export PATH="$(dirname "$PW"):$HPCX/bin:$PATH"
MPIRUN="$HPCX/bin/mpirun"
echo "pw.x=$PW"

# ---- run: cheap refs first (Li_atom validates env/pseudo), then the 6 slabs ----
ORDER=${ORDER:-"Li_atom graphene hbn Li_on_graphene Li_on_hbn bilayer Li_in_gallery"}
run_one() {
    local name=$1 f="$IN/$1.in" o="$WORK/$1.out"
    [ -f "$f" ] || { echo "[$name] 입력없음 skip"; return; }
    grep -aq "JOB DONE" "$o" 2>/dev/null && { echo "[$name] done skip"; return; }
    sed "s|\$PSEUDO_DIR|$PSE|g" "$f" > "$WORK/$name.in"
    echo "[$(date +%H:%M:%S)] pw.x $name (nat $(grep -c '^  [A-Z]' "$WORK/$name.in"))"
    "$MPIRUN" -np 1 "$PW" -in "$WORK/$name.in" > "$o" 2>&1
    if grep -aq "JOB DONE" "$o"; then
        echo "[$name] OK  E=$(grep -a '^!' "$o" | tail -1 | awk '{print $(NF-1)}') Ry"
    else echo "[$name] FAIL — tail:"; tail -18 "$o"; fi
}
for n in $ORDER; do run_one "$n"; done

echo; echo "===== E_ads = E(Li_on_X) - E(X) - E(Li_atom) ====="
python3 - "$WORK" <<'PY'
import re, sys, os
W = sys.argv[1]; Ry = 13.605693
def E(n):
    p = f"{W}/{n}.out"
    if not os.path.exists(p): return None
    m = re.findall(r"^!\s+total energy\s+=\s+(-\d+\.\d+)", open(p).read(), re.M)
    return float(m[-1]) if m else None
li = E("Li_atom")
rows = [("Li on VGCF(graphene)", "Li_on_graphene", "graphene"),
        ("Li on h-BN",           "Li_on_hbn",      "hbn"),
        ("Li in h-BN|VGCF gallery", "Li_in_gallery", "bilayer")]
vals = {}
for lab, cx, sub in rows:
    ec, es = E(cx), E(sub)
    if ec and es and li:
        v = (ec - es - li) * Ry; vals[lab] = v
        print(f"  {lab:26s} E_ads = {v:+.3f} eV")
    else:
        print(f"  {lab:26s} (미완)")
if len(vals) == 3:
    g = vals["Li on VGCF(graphene)"]; h = vals["Li on h-BN"]; s = vals["Li in h-BN|VGCF gallery"]
    print(f"  --- Shi eq5: gallery({s:+.3f}) vs graphene({g:+.3f})+hbn({h:+.3f}) 합({g+h:+.3f}) ---")
    print("  >>> gallery가 두 단일표면보다 더 음수면 VGCF가 Cu역할 = 샌드위치 성립.")
    print("      아니면 그 자체가 발견(VGCF != Cu). (절대값은 vs Li-atom; lithiophobicity는 vs bulk-Li -1.63 eV 변환)")
PY
echo ">> paste 해주면 db 등록 + 확산 NEB 다음 단계 설계"
