#!/usr/bin/env bash
# =============================================================================
# run_neb_kgy.sh — CI-NEB Li hollow->hollow hops on kgy (h-BN surf / VGCF surf /
# gallery). 조건 ②(확산): h-BN 0.10 eV(Shi 검증) / graphene ~0.3 eV(문헌 기준선) /
# gallery = 신규 핵심값.
#
# GPU 선점 대기 내장 — vgcf2L 체인이 아직 돌고 있어도 지금 걸어놓으면 끝난 뒤 시작.
#   cd ~/Yonghoon-DEM-DFT && git pull   # (or checkout tools/vgcf_hbn/)
#   tmux new -s vgcfneb -d 'bash tools/vgcf_hbn/run_neb_kgy.sh > ~/work/vgcf_hbn/neb_run.log 2>&1'
# =============================================================================
set -u; set +H
REPO=${REPO:-$HOME/Yonghoon-DEM-DFT}; [ -d "$REPO" ] || REPO=$HOME/work/Yonghoon-DEM-DFT
WORK=${WORK:-$HOME/work/vgcf_hbn}; NEB=$WORK/neb; mkdir -p "$NEB"

# 중복실행 가드
[ "$(pgrep -fc run_neb_kgy.sh)" -le 3 ] || { echo "이미 실행중 — 종료"; exit 1; }

# GPU 선점 대기 (vgcf2L 등 기존 pw.x/neb.x)
while pgrep -f 'pw\.x|neb\.x' >/dev/null 2>&1; do
  echo "[$(date +%H:%M:%S)] GPU 사용중(pw.x/neb.x) — 5분 뒤 재확인"; sleep 300
done
echo "[$(date +%H:%M:%S)] GPU free — NEB 체인 시작"

# ---- qegpu env (run_qe_kgy.sh와 동일) ----
PW=${PW:-$(find "$HOME/apps" -maxdepth 4 -name pw.x -path "*qe*gpu*bin*" 2>/dev/null | head -1)}
[ -n "$PW" ] || { echo "ERROR: pw.x(gpu) 못찾음"; exit 1; }
NEBX="$(dirname "$PW")/neb.x"
[ -x "$NEBX" ] || { echo "ERROR: neb.x 없음 ($NEBX) — QE 빌드에 NEB 패키지 필요"; exit 1; }
NV="$HOME/apps/nvhpc/Linux_x86_64/24.11"
HPCX="$(ls -d "$NV"/comm_libs/*/hpcx/hpcx-*/ompi 2>/dev/null | sort | tail -1)"
[ -n "$HPCX" ] || { echo "ERROR: hpcx 못찾음"; exit 1; }
export OPAL_PREFIX="$HPCX" OMP_NUM_THREADS=1
export LD_LIBRARY_PATH="$NV/compilers/lib:$NV/cuda/12.6/lib64:$NV/math_libs/lib64:$HPCX/lib:${LD_LIBRARY_PATH:-}"
export PATH="$(dirname "$PW"):$HPCX/bin:$PATH"
MPIRUN="$HPCX/bin/mpirun"
echo "pw.x=$PW"; echo "neb.x=$NEBX"

CASES="Li_on_hbn Li_on_graphene Li_in_gallery Li_in_gallery_2L2L"

# ---- pass 1: endpoint-B 입력 생성 + relax (Li +2.46A, 기판 dimple 재형성) ----
python3 "$REPO/tools/vgcf_hbn/neb_build_kgy.py"
cd "$NEB"
for c in $CASES; do
  f=$NEB/${c}_nebB.in o=$NEB/${c}_nebB.out
  [ -f "$f" ] || { echo "[$c] endpoint-B 입력없음 skip"; continue; }
  grep -aq "JOB DONE" "$o" 2>/dev/null && { echo "[$c] endpoint-B done skip"; continue; }
  echo "[$(date +%H:%M:%S)] pw.x ${c}_nebB (relax)"
  "$MPIRUN" -np 1 "$PW" -in "$f" > "$o" 2>&1
  grep -aq "JOB DONE" "$o" && echo "[$c] endpoint-B OK" \
    || { echo "[$c] endpoint-B FAIL — tail:"; tail -12 "$o"; }
done

# ---- pass 2: NEB 입력 생성 + neb.x (endpoint 짝 완성된 케이스만) ----
python3 "$REPO/tools/vgcf_hbn/neb_build_kgy.py"
for c in $CASES; do
  d=$NEB/$c
  [ -f "$d/neb.in" ] || { echo "[$c] neb 입력없음 (endpoint 실패?) skip"; continue; }
  grep -aiq "convergence achieved" "$d/neb.out" 2>/dev/null && { echo "[$c] NEB done skip"; continue; }
  ls "$d"/*.path >/dev/null 2>&1 && sed -i "s/'from_scratch'/'restart'/" "$d/neb.in"
  echo "[$(date +%H:%M:%S)] neb.x $c (7 images)"
  ( cd "$d" && "$MPIRUN" -np 1 "$NEBX" -inp neb.in > neb.out 2>&1 )
  ea=$(grep -a "activation energy (->)" "$d/neb.out" | tail -1)
  if [ -n "$ea" ]; then echo "[$c] $ea"; else echo "[$c] 결과줄 없음 — tail:"; tail -12 "$d/neb.out"; fi
done

echo ""; echo "===== NEB barriers (forward) ====="
for c in $CASES; do
  ea=$(grep -a "activation energy (->)" "$NEB/$c/neb.out" 2>/dev/null | tail -1 | awk '{print $(NF-1)}')
  echo "  $c : ${ea:-대기} eV"
done
echo ">> 기준: h-BN 표면 Shi2017 0.10 eV / graphene 문헌 ~0.3 eV / gallery=신규(핵심값)."
echo ">> 붙여주면 db 등록 + 균일분산 판정."
