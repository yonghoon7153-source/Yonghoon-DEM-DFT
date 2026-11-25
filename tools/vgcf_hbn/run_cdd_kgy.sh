#!/usr/bin/env bash
# =============================================================================
# run_cdd_kgy.sh — Li 결합 CDD (charge density difference) on kgy.
#   CDD = rho(Li+host) - rho(host) - rho(Li)   [같은 셀·같은 grid 3-SCF 차분]
# Liu2022(AMI 9,2200011) 그림 (f)(g) 대응 비교그림용. relaxed 구조에서 single-point.
#   대상 3종: Li_on_graphene(↔Li-Cu) / Li_on_hbn(↔Li-hBN) / Li_in_gallery_2L2L(↔샌드위치)
#
# 노랑=전자 축적(받개), 청록=결핍(Li+). VGCF가 전자받개(Cu역할) vs h-BN 수동캡 시각화.
#
# ⚠ GPU 필요 (pw.x). NEB 돌면 대기 내장 — 근데 CDD 빨리 원하면 NEB 잠깐 멈추고(resume-safe)
#   이거 먼저(~2h) 돌린 뒤 NEB 재개 권장. relaxed 좌표는 ~/work/vgcf_hbn/*.out에서.
#   cd ~/Yonghoon-DEM-DFT && git pull   # (or checkout tools/vgcf_hbn/)
#   tmux new -s vgcfcdd -d 'bash tools/vgcf_hbn/run_cdd_kgy.sh >> ~/work/vgcf_hbn/cdd_run.log 2>&1'
# =============================================================================
set -u; set +H
REPO=${REPO:-$HOME/Yonghoon-DEM-DFT}; [ -d "$REPO" ] || REPO=$HOME/work/Yonghoon-DEM-DFT
WORK=${WORK:-$HOME/work/vgcf_hbn}; CDD=$WORK/cdd; mkdir -p "$CDD"
CASES=${CASES:-"Li_on_graphene_2L Li_on_hbn_2L Li_in_gallery_2L2L"}
[ "$(pgrep -fc run_cdd_kgy.sh)" -le 3 ] || { echo "이미 실행중"; exit 1; }

# GPU 대기 (NEB/relax 뒤)
while pgrep -f 'pw\.x|neb\.x' >/dev/null 2>&1; do
  echo "[$(date +%H:%M:%S)] GPU 사용중(NEB?) — 5분 뒤 재확인 (빨리 원하면 NEB 멈추고 재시작)"; sleep 300
done
echo "[$(date +%H:%M:%S)] GPU free — CDD 시작"

# ---- qegpu env + pp.x ----
PW=${PW:-$(find "$HOME/apps" -maxdepth 4 -name pw.x -path "*qe*gpu*bin*" 2>/dev/null | head -1)}
PPX="$(dirname "$PW")/pp.x"; [ -x "$PPX" ] || { echo "ERROR: pp.x 없음"; exit 1; }
NV="$HOME/apps/nvhpc/Linux_x86_64/24.11"
HPCX="$(ls -d "$NV"/comm_libs/*/hpcx/hpcx-*/ompi 2>/dev/null | sort | tail -1)"
export OPAL_PREFIX="$HPCX" OMP_NUM_THREADS=1
export LD_LIBRARY_PATH="$NV/compilers/lib:$NV/cuda/12.6/lib64:$NV/math_libs/lib64:$HPCX/lib:${LD_LIBRARY_PATH:-}"
export PATH="$(dirname "$PW"):$HPCX/bin:$PATH"
MPIRUN="$HPCX/bin/mpirun"; PSE=$WORK/pseudo
echo "pw.x=$PW  pp.x=$PPX"

gen_scf() { python3 "$REPO/tools/vgcf_hbn/cdd_build.py" "$WORK" "$CDD" "$1" "$PSE"; }

run_scf() { # $1=dir $2=tag (complex|host|li). 입력 outdir=절대경로 -> pp.x 동일 경로.
  local d=$1 g=$2
  if ! grep -aq "JOB DONE" "$d/$g.out" 2>/dev/null; then
    echo "[$(date +%H:%M:%S)] pw.x $(basename $d)/$g"
    "$MPIRUN" -np 1 "$PW" -in "$d/$g.in" > "$d/$g.out" 2>&1
    grep -aq "JOB DONE" "$d/$g.out" || { echo "[$g] SCF FAIL:"; tail -10 "$d/$g.out"; return 1; }
  fi
  if [ ! -s "$d/${g}_rho.cube" ]; then
    cat > "$d/pp_$g.in" <<EOF
&INPUTPP
  prefix='$g', outdir='$d/tmp_$g', plot_num=0, filplot='$d/${g}_fp'
/
&PLOT
  iflag=3, output_format=6, fileout='$d/${g}_rho.cube'
/
EOF
    "$MPIRUN" -np 1 "$PPX" -in "$d/pp_$g.in" > "$d/pp_$g.out" 2>&1
    [ -s "$d/${g}_rho.cube" ] || { echo "[$g] pp.x FAIL:"; tail -8 "$d/pp_$g.out"; return 1; }
  fi
}

for c in $CASES; do
  d=$CDD/$c
  gen_scf "$c" || { echo "[$c] 입력생성 실패 skip"; continue; }
  run_scf "$d" complex && run_scf "$d" host && run_scf "$d" li || { echo "[$c] SCF 실패"; continue; }
  echo "[$(date +%H:%M:%S)] CDD 차분 $c"
  python3 "$REPO/tools/electronic/cube_diff.py" --mode cdd \
    --ab "$d/complex_rho.cube" --a "$d/host_rho.cube" --b "$d/li_rho.cube" \
    --out "$d/${c}_cdd.cube" && echo "[$c] -> $d/${c}_cdd.cube"
done

echo ""; echo "===== CDD cube (VESTA로 iso ~0.002~0.005 e/Bohr^3, 노랑+ 청록-) ====="
ls -la $CDD/*/*_cdd.cube 2>/dev/null
echo ">> cube 3개 가져오면 .vesta 페어 + 그림(노랑축적/청록결핍) 만들어줄게 (Liu f/g 대응)."
