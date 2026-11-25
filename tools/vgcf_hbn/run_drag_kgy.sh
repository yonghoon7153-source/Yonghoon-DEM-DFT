#!/usr/bin/env bash
# =============================================================================
# run_drag_kgy.sh — Li hollow->hollow barrier via constrained-drag (pw.x only).
# neb.x가 kgy QE-GPU 빌드에 없어 채택한 사내 검증 방법(Li3N 계열). 각 case의
# 7개 drag 이미지를 relax(Li x,y 고정)해 E(x) 프로파일 -> barrier = max-start.
#
# GPU 대기 내장 (vgcf2L/pw.x 뒤 자동). 검증 앵커: hBN 표면 Shi2017 = 0.10 eV.
#   cd ~/Yonghoon-DEM-DFT && git pull   # (or checkout tools/vgcf_hbn/)
#   tmux new -s vgcfdrag -d 'bash tools/vgcf_hbn/run_drag_kgy.sh >> ~/work/vgcf_hbn/drag_run.log 2>&1'
# =============================================================================
set -u; set +H
REPO=${REPO:-$HOME/Yonghoon-DEM-DFT}; [ -d "$REPO" ] || REPO=$HOME/work/Yonghoon-DEM-DFT
WORK=${WORK:-$HOME/work/vgcf_hbn}; DRAG=$WORK/drag; mkdir -p "$DRAG"
[ "$(pgrep -fc run_drag_kgy.sh)" -le 3 ] || { echo "이미 실행중 — 종료"; exit 1; }

# GPU 선점 대기
while pgrep -f 'pw\.x|neb\.x' >/dev/null 2>&1; do
  echo "[$(date +%H:%M:%S)] GPU 사용중 — 5분 뒤 재확인"; sleep 300
done
echo "[$(date +%H:%M:%S)] GPU free — drag 체인 시작"

# ---- qegpu env (run_qe_kgy.sh와 동일; neb.x 불필요) ----
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

CASES="Li_on_hbn Li_on_graphene Li_in_gallery Li_in_gallery_2L2L"
python3 "$REPO/tools/vgcf_hbn/drag_build_kgy.py"

for c in $CASES; do
  d=$DRAG/$c
  [ -d "$d" ] || { echo "[$c] 이미지없음 skip"; continue; }
  for f in "$d"/img*.in; do
    [ -f "$f" ] || continue
    o="${f%.in}.out"
    grep -aq "JOB DONE" "$o" 2>/dev/null && { echo "[$(basename "$d")/$(basename "$o")] done skip"; continue; }
    echo "[$(date +%H:%M:%S)] pw.x $c/$(basename "$f")"
    "$MPIRUN" -np 1 "$PW" -in "$f" > "$o" 2>&1
    grep -aq "JOB DONE" "$o" || { echo "[$c/$(basename "$f")] FAIL — tail:"; tail -8 "$o"; }
  done
done

echo ""; echo "===== drag barriers (E(x) − E(start)) ====="
python3 - "$DRAG" "$CASES" <<'PY'
import re, sys, os, glob
DRAG = sys.argv[1]; cases = sys.argv[2].split(); Ry = 13.605693
for c in cases:
    d = f"{DRAG}/{c}"
    outs = sorted(glob.glob(f"{d}/img*.out"), key=lambda p: int(re.search(r"img(\d+)", p).group(1)))
    Es = []
    for o in outs:
        m = re.findall(r"^!\s+total energy\s+=\s+(-\d+\.\d+)", open(o, errors="ignore").read(), re.M)
        Es.append(float(m[-1]) if m else None)
    if not Es or None in Es:
        print(f"  {c:22s} (미완 {sum(x is not None for x in Es)}/{len(outs)})"); continue
    e0 = Es[0]; prof = [(e - e0) * Ry for e in Es]
    bar = max(prof)
    print(f"  {c:22s} barrier = {bar:.3f} eV   프로파일(eV): " + " ".join(f"{p:+.3f}" for p in prof))
print("  기준: hBN 표면 Shi2017 0.10 / graphene 문헌 ~0.3 / gallery=신규(핵심).")
print("  >> 붙여주면 db 등록 + 균일분산 판정 (조건② 확산).")
PY
