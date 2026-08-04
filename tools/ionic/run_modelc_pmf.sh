#!/usr/bin/env bash
# run_modelc_pmf.sh — LPSCl1.6 의 **MD Li-밀도 PMF** 경로/장벽 그림 (2026-08-05)
#
# 왜 modelc 인가: β 게이트를 통과한 유일한 계다 (600/800/1000 K 3시드 0.87/0.93/0.92,
#   600 K 이온당 홉 13.9회). comp1 은 6/6 케이지라 PMF 도 표집 상한이 된다(open_items #9).
#
# 하는 일
#   1) 600 K 궤적(가능하면 시드 여러 개) → li_density_cube.py 로 Li 밀도 cube
#      ⚠ 궤적에 프레임이 없으면(--save_traj 없이 돈 런) 이 스크립트가 짧게 재실행한다.
#   2) pmf_path_profile.py 로 F = -kT ln(rho/rho_max) → 침투 문턱 F* · 최소경로 ·
#      구간별 장벽 (BV 판과 **같은 관례**라 나란히 비교 가능)
#   3) 회수할 것만 남긴다: PNG · CSV 2개 · npz (cube 는 수십 MB라 서버에 둠)
#
# 안전: 순수 CPU 분석(2단계)이지만 1단계 MD 는 GPU 를 쓴다 → pw.x 와 동시 실행 금지.
#   nvidia-smi 로 확인 후 실행할 것 (CLAUDE.md 규율).
#
#   bash tools/ionic/run_modelc_pmf.sh              # 600 K
#   TEMP=800 bash tools/ionic/run_modelc_pmf.sh     # 온도 의존성 보고 싶으면
set -u
REPO=${REPO:-$HOME/Yonghoon-DEM-DFT}; [ -d "$REPO" ] || REPO=$HOME/work/Yonghoon-DEM-DFT
cd "$REPO" || exit 1
TEMP=${TEMP:-600}
OUT=${OUT:-runs/modelc_pmf_T$TEMP}
DEV=${DEV:-cuda}
XYZ=${XYZ:-db/structures/modelc_V0_k663.xyz}
PY=${PY:-python3}
PROD_PS=${PROD_PS:-200}
NSEED=${NSEED:-3}

if pgrep -f "pmf_path_profile.py" >/dev/null 2>&1; then
  echo "⛔ 이미 실행 중 — 중복 방지"; exit 1
fi
[ -f "$XYZ" ] || { echo "⛔ $XYZ 없음 — git pull 먼저"; exit 1; }
mkdir -p "$OUT"

echo "── 0) 도구 최신화 ──"
git fetch origin claude/friendly-meitner-lldvar 2>&1 | tail -2
git checkout FETCH_HEAD -- tools/ionic/pmf_path_profile.py tools/ionic/li_density_cube.py \
                           tools/figures/fig_bv_path_profile.py \
                           tools/figures/fig_bv_path_annotated.py || exit 1
git --no-pager log -1 --format="  도구 커밋 %h %s" FETCH_HEAD

echo "── 1) $TEMP K 궤적 찾기 (프레임이 저장된 것만) ──"
if [ -n "${TRAJ_GLOB:-}" ]; then          # 직접 지정 (로컬 백업·다른 경로)
  mapfile -t TRAJS < <(ls -1 $TRAJ_GLOB 2>/dev/null | head -"$NSEED")
else
  mapfile -t TRAJS < <(find runs "$OUT" -name traj.xyz -path "*T${TEMP}*" 2>/dev/null \
                       | grep -a -i "modelc\|lpscl1.6\|lpscl16" | head -"$NSEED")
fi
echo "  찾은 궤적 ${#TRAJS[@]}개:"; printf '   %s\n' "${TRAJS[@]:-(없음)}"

if [ "${#TRAJS[@]}" -eq 0 ]; then
  # ⚠⚠ 2026-08-05: 예전 판은 여기서 **자동으로 GPU MD 를 시작**했다. Arrhenius 런이
  #   --save_traj 없이 돌아 프레임이 없는 게 정상이라 이 분기가 거의 항상 타는데,
  #   pw.x 와 VRAM 이 겹치면 사고다 (CLAUDE.md: pw.x 와 UMA 동시 실행 금지).
  #   → **명시적 옵트인(ALLOW_MD=1)** 없이는 여기서 멈춘다.
  USED=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | head -1)
  echo "  → 저장된 프레임이 없다 (Arrhenius 런은 --save_traj 없이 돈다 = 정상)."
  echo "     현재 VRAM 사용 ${USED} MiB"
  if [ "${ALLOW_MD:-0}" != "1" ]; then
    echo "  ⛔ MD 재실행은 옵트인이다. GPU 가 한가한 걸 확인한 뒤:"
    echo "       ALLOW_MD=1 bash tools/ionic/run_modelc_pmf.sh"
    echo "     또는 이미 있는 궤적을 직접 지정:"
    echo "       TRAJ_GLOB='/path/to/T600/traj.xyz' bash tools/ionic/run_modelc_pmf.sh"
    exit 2
  fi
  if [ "${USED:-0}" -gt 2000 ]; then
    echo "  ⚠ VRAM 이 이미 ${USED} MiB 점유 중이다 — pw.x 확인 후 진행할 것 (10초 대기)"
    sleep 10
  fi
  echo "  → $TEMP K 를 --save_traj 로 재실행 (GPU, ~20-40분)"
  unset LD_LIBRARY_PATH OPAL_PREFIX 2>/dev/null || true
  $PY tools/modelc_v3/disorder_ensemble_diffusion.py \
      --v0_xyz "$XYZ" --label modelc --out_root "$OUT" \
      --disorder_levels 0.0 --n_configs 1 \
      --temperatures "$TEMP" --equilib_ps 5 --prod_ps "$PROD_PS" \
      --save_traj --device "$DEV" 2>&1 | tail -12
  mapfile -t TRAJS < <(find "$OUT" -name traj.xyz -path "*T${TEMP}*" 2>/dev/null | head -"$NSEED")
  [ "${#TRAJS[@]}" -gt 0 ] || { echo "⛔ 궤적 생성 실패"; exit 1; }
fi

echo "── 2) Li 밀도 cube (시드별) ──"
CUBEARGS=()
for i in "${!TRAJS[@]}"; do
  C="$OUT/modelc_s$((i+1))_T${TEMP}_Li.cube"
  if [ ! -s "$C" ]; then
    $PY tools/ionic/li_density_cube.py --traj "${TRAJS[$i]}" --out "$C" \
        --skip 100 --spacing 0.2 --sigma_A 0.4 2>&1 | tail -3
  else
    echo "  (있음) $C"
  fi
  CUBEARGS+=(--cube "$C")
done

echo "── 3) PMF 경로·구간 장벽 ──"
$PY tools/ionic/pmf_path_profile.py "${CUBEARGS[@]}" \
    --T "$TEMP" --tag "modelc_T${TEMP}" --label "LPSCl1.6" --out_dir "$OUT" 2>&1 | tail -30

echo
echo "── 산출 ──"; ls -la "$OUT" | grep -a -E "png|csv|npz"
echo
echo "회수 (로컬에서):"
echo "  scp root@121.78.116.27:'$REPO/$OUT/modelc_T${TEMP}_pmf_*' ."
echo "  → PNG(프로파일) · CSV 2개(프로파일·구간) · npz(경로+구조; 3D 렌더는 로컬에서)"
echo "cube 는 서버에 둔다 (수십 MB): $OUT/*.cube"
