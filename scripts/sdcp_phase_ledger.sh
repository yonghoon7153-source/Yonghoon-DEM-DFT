#!/usr/bin/env bash
# ★ 상별 부피 원장 + 우선순위 결함 크기 — **솔브 없이, 순수 CPU** (심층 리뷰 ③ 제안)
#
# 두 가지를 한 번에 닫는다:
#   ① **CL-34 상계** — "구 스탬프가 SDCP 로 덮은 셀 중 원래 PTFE/SWCNT 였던 것" 을 직접 센다.
#      결함판(SDCP 가 그 둘을 덮음) vs 수정판(양보함) 의 차이가 곧 결함의 크기다.
#      ⇒ GPU 대조 팔 (~1.5 h) 없이 몇 분에 끝난다.
#   ② **상별 부피 원장** (GPU 3건 중 ②) — `count(sid)·vox³` 를 레시피와 대조.
#      CL-25 의 "SDCP 4.53×" 는 **단입자 산술**이라 셀 충돌·상 overwrite 를 안 본다.
#      이 원장이 실침대의 **진짜** 배수를 준다.
#
# ⚠ 솔브를 안 하므로 GPU 를 안 쓴다 — 돌고 있는 구-스탬프 런과 자원 충돌 없음
#   (RAM 은 격자 하나치 ~13 GB 를 잠깐 쓴다; 62 GB 호스트면 여유).
#
# 사용 (원격, ~/sdcp 에서):
#   . ~/dem-venv/bin/activate
#   bash ~/dem-sk/scripts/sdcp_phase_ledger.sh            # vox 0.15 (판별 런과 같은 격자)
#   VOXES="0.4 0.3 0.25 0.15" bash ~/dem-sk/scripts/sdcp_phase_ledger.sh   # 격자 스윕
set -uo pipefail

VOXES="${VOXES:-0.15}"
BRIDGE_UM="${BRIDGE_UM:-0.48}"
SDCP_D="${SDCP_D:-0.30}"
SCR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTDIR="${OUTDIR:-$PWD/phase_ledger}"
mkdir -p "$OUTDIR"

if [ -z "${VIRTUAL_ENV:-}" ]; then
  for _v in "$HOME/dem-venv" "$SCR/../venv"; do
    [ -f "$_v/bin/activate" ] && { . "$_v/bin/activate"; break; }
  done
fi
grep -q -- '--step3-rasterize-only' "$SCR/mpm_webapp_payload.py" \
  || { echo "ABORT — rasterize-only 플래그가 없다 (git pull 했나?)"; exit 2; }

run_one() {   # $1=kit  $2=vox  $3=sphere_d("" 면 점 스탬프)
  local K="$1" VOX="$2" SD="$3"
  local KIT RUN TAG SDF
  KIT="$(cd "$K" && pwd)"
  if [ -e "$KIT/latest_run" ]; then RUN="$(cd "$KIT/latest_run" && pwd)"
  else RUN=""; for d in "$KIT"/run_*; do [ -f "$d/se_dump.npy" ] && RUN="$(cd "$d" && pwd)"; done; fi
  [ -n "$RUN" ] || { echo "  ABORT — $K 압밀 런 없음"; return 1; }
  SDF=""; TAG="${K#kit_}_v${VOX/./}_pt"
  [ -n "$SD" ] && { SDF=" --step3-sdcp-sphere-d $SD"; TAG="${K#kit_}_v${VOX/./}_sph"; }
  local OUT="$OUTDIR/ledger_${TAG}.json"
  [ -s "$OUT" ] && { echo "  SKIP $TAG"; return 0; }

  local SIGMA
  SIGMA=$(cd "$RUN" && P2_SCR="$SCR" STEP3_VOX="$VOX" python3 - <<'PY'
import os, sys
import numpy as np
sys.path.insert(0, os.environ['P2_SCR'])
import step3_sigma as s3
dia, ph = np.load('fibre_dia.npy'), np.load('phase.npy')
se, _ = s3.diameter_preserving_sigma(100.0, dia[ph == 2], 0.15, float(os.environ['STEP3_VOX']))
print(f'{se:.6g}')
PY
  ) || return 1

  ( cd "$RUN" && P2_SCR="$SCR" python3 "$SCR/sr01_stamp_compare.py" \
      --extract-payload "$KIT/run_mpm.sh" --stamp segment \
      --extra-flags "--sigma-vgcf $SIGMA --step3-vox $VOX --step3-bridge-um $BRIDGE_UM --step3-rasterize-only $OUT$SDF" \
      --tag "L$TAG" --out-name "unused_$TAG.json" > "_L$TAG.sh" ) || return 1
  { echo 'set -uo pipefail'; echo "KIT=\"$KIT\""; echo "SCR=\"$SCR\""; echo 'PSIG=()';
    cat "$RUN/_L$TAG.sh"; } > "$RUN/L$TAG.sh"
  rm -f "$RUN/_L$TAG.sh"
  grep -q -- "--step3-rasterize-only" "$RUN/L$TAG.sh" || { echo "  ABORT — 플래그 미주입"; return 1; }
  echo "  ── $TAG"
  ( cd "$RUN" && bash "L$TAG.sh" ) || return 1
}

for VOX in $VOXES; do
  echo "══ vox $VOX ══════════════════════════════════════════"
  for K in kit_SBE kit_DBE; do
    [ -d "$K" ] || { echo "  ABORT — $K 없음 (~/sdcp 에서 돌릴 것)"; exit 2; }
    run_one "$K" "$VOX" ""                                  # 점 스탬프 (생산 규약)
    #  구 스탬프는 d/vox ≥ 2 에서만 (게이트가 거부한다)
    if python3 -c "import sys; sys.exit(0 if $SDCP_D/$VOX >= 2.0 else 1)"; then
      run_one "$K" "$VOX" "$SDCP_D"
    else
      echo "  (구 스탬프 건너뜀 — d/vox = $(python3 -c "print(f'{$SDCP_D/$VOX:.2f}')") < 2)"
    fi
  done
done

echo
echo "══ 종합 ═════════════════════════════════════════════════"
python3 "$SCR/sdcp_phase_ledger_report.py" --dir "$OUTDIR"
