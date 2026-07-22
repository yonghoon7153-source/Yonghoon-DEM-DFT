#!/usr/bin/env bash
# =============================================================================
# run_comp2_elastic_gabia.sh — comp2 v3 champion 600K MLIP snapshot elastic.
#   comp1(LPSCl)과 동일 방법("600K_snapshot_x5")으로 공정 비교 (comp1 E_VRH=29.1 GPa).
#   프로토콜: 600K MD(equilib 10 + prod 20 ps) -> 5 snapshot -> 각 FIRE quench +
#            6 Voigt strain ±0.005 relaxed-ion -> 6x6 Cij stress-strain -> VRH ± std.
#   elastic_mlip_600K.py 재사용 (완전 파라미터화). ~3-6 h (A6000).
#
# conductivity MD와 GPU 공존 가능(둘 다 UMA, VRAM 각 ~1-2GB; MD는 seed 고정이라
# GPU 공유해도 결과 bit-identical). GPU 이슈 보이면 DEVICE=cpu로.
#
#   gabia(uma): tmux new -s c2elastic -d 'bash tools/elastic/run_comp2_elastic_gabia.sh > ~/comp2_elastic.log 2>&1'
# =============================================================================
set -u; set +H
REPO=${REPO:-$HOME/Yonghoon-DEM-DFT}; [ -d "$REPO" ] || REPO=$HOME/work/Yonghoon-DEM-DFT
cd "$REPO"
unset LD_LIBRARY_PATH OPAL_PREFIX 2>/dev/null || true   # QE env 잔재가 torch 오염 (MD 러너와 동일)
PY=$(ls /data/apps/miniforge3/envs/uma/bin/python3 2>/dev/null || which python3)
STRUCT=${STRUCT:-$REPO/db/structures/comp2_V0_v3_relaxed.xyz}
OUT=${OUT:-/data/work/runs/comp2_elastic_v3}
DEVICE=${DEVICE:-cuda}
[ "$(pgrep -fc run_comp2_elastic_gabia)" -le 2 ] || { echo "이미 실행중"; exit 1; }
test -f "$STRUCT" || { echo "MISSING $STRUCT — git pull 먼저"; exit 1; }
echo "comp2 v3 elastic (600K snapshot x5, relaxed-ion) — device=$DEVICE"
echo "  struct=$STRUCT  out=$OUT  PY=$PY"

"$PY" tools/modelc_v3/elastic_mlip_600K.py \
  --v0_xyz "$STRUCT" --out_dir "$OUT" \
  --T_K 600 --equilib_ps 10 --prod_ps 20 --n_snapshots 5 \
  --timestep_fs 2.0 --friction 0.02 \
  --strain 0.005 --quench_fmax 0.01 \
  --uma_model uma-s-1p1 --uma_task omat --device "$DEVICE"
rc=$?
echo ""
if [ "$rc" = 0 ]; then
  echo ">> out JSON: $OUT (Cij 6x6 + VRH B/G/E ± std). 붙여주면:"
  echo "   comp2.json elastic_mlip_600K_v3 등록 + comp1(E_VRH 29.1) 비교표 (슬라이드 iii)."
else
  echo "!! 오류(rc=$rc) — GPU 충돌이면 DEVICE=cpu로 재시도. tail 확인."
fi
