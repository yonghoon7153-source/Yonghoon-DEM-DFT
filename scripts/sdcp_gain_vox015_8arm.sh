#!/usr/bin/env bash
# ★ 사전등록 v2 판별 런 — `docs/reviews/sdcp_gain_prereg_v2_20260816.md`
#
#   SBE / DBE 를 **vox 0.15 µm** 에서 **origin 8 팔 factorial** 로 푼다.
#   h0 (이득은 물리)        → σ_e 비 ≥ 1.05
#   h1 (SDCP 부피 인공물)  → σ_e 비 = 1.015
#   분해능 0.02 · 8 팔 표준오차 4.3σ (prereg §4)
#
# ⚠ 이 스크립트는 **판정을 하지 않는다** — 16 개 값을 전부 뽑아 JSON 으로 남긴다.
#   판정은 prereg §5 순서대로 `--verdict` 로 따로 돈다 (결과를 보고 창을 옮길 수 없게).
#
# ⚠ 고정해야 하는 것 (prereg §5): 브리지 반경을 **명시**한다.  기본 1.2·vox 는 격자마다
#   달라져 CL-22 의 결함을 반복한다.  vox 0.15 기본이면 0.18 µm — 여기서는 세 격자 비교에
#   쓴 값과 같은 **물리 단위**로 못 박는다.
#
# 사용 (원격 GPU 호스트):
#   . ~/dem-venv/bin/activate
#   cd ~/sdcp
#   setsid nohup bash ~/dem-sk/scripts/sdcp_gain_vox015_8arm.sh > p2.log 2>&1 &
#   tail -f p2.log
#   # 팔 하나만 시험:  ARMS=1 bash ~/dem-sk/scripts/sdcp_gain_vox015_8arm.sh
set -uo pipefail

VOX="${VOX:-0.15}"
BRIDGE_UM="${BRIDGE_UM:-0.48}"          # prereg §5 — 격자와 무관하게 고정
ARMS="${ARMS:-8}"
SCR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTDIR="${OUTDIR:-$PWD/prereg_v2_vox${VOX/./}}"
mkdir -p "$OUTDIR"

if [ -z "${VIRTUAL_ENV:-}" ] && [ -z "${MPM_NO_VENV:-}" ]; then
  for _v in "$HOME/dem-venv" "$SCR/../venv" "$SCR/../.venv"; do
    [ -f "$_v/bin/activate" ] && { . "$_v/bin/activate"; echo "[p2] venv $_v"; break; }
  done
fi

# ── 게이트: prereg 와 코드가 실제로 준비됐는지 (fail-closed) ─────────────────────────
PREREG="$SCR/../docs/reviews/sdcp_gain_prereg_v2_20260816.md"
[ -f "$PREREG" ] || { echo "ABORT — 사전등록 파일이 없다: $PREREG"; exit 2; }
python3 -c "
import sys; sys.path.insert(0,'$SCR')
import argparse, importlib.util as iu
spec = iu.spec_from_file_location('m','$SCR/mpm_webapp_payload.py')
src = open('$SCR/mpm_webapp_payload.py', encoding='utf-8').read()
assert '--step3-origin-shift' in src, 'origin 이동 CLI 가 없다 — 8 팔을 돌릴 수 없다'
print('  [p2] origin 이동 CLI 확인')
" || exit 2
PYTHONUTF8=1 python3 "$SCR/check_method_discipline.py" >/dev/null 2>&1 \
  || { echo "ABORT — 방법론 규율 검사 실패.  먼저 통과시킬 것"; exit 2; }
echo "[p2] 규율 검사 통과"
#  ★ 미정의 이름 게이트 (실사고 2026-08-16): 판별 런이 SE 점 6,792 만 개를 읽은 **뒤**
#    `NameError: _zt3` 로 죽었다.  런이 실제로 쓰는 파일만 정적으로 먼저 본다.
PYTHONUTF8=1 python3 "$SCR/check_undefined_names.py" \
  "$SCR/mpm_webapp_payload.py" "$SCR/step3_sigma.py" "$SCR/viz_mpm_continuum.py" \
  "$SCR/additives.py" "$SCR/sr01_stamp_compare.py" >/dev/null 2>&1 \
  || { echo "ABORT — 미정의 이름 발견.  다음으로 확인:"; \
       PYTHONUTF8=1 python3 "$SCR/check_undefined_names.py" \
         "$SCR/mpm_webapp_payload.py" "$SCR/step3_sigma.py" "$SCR/viz_mpm_continuum.py" \
         "$SCR/additives.py" "$SCR/sr01_stamp_compare.py"; exit 2; }
echo "[p2] 미정의 이름 없음 (런 경로 5 파일)"

# ── 8 팔 = {0, vox/2}³ ─────────────────────────────────────────────────────────────
H=$(python3 -c "print(f'{$VOX/2:.6f}')")
SHIFTS=()
for X in 0 "$H"; do for Y in 0 "$H"; do for Z in 0 "$H"; do
  SHIFTS+=("$X $Y $Z")
done; done; done

run_arm() {   # $1=kit dir  $2="sx sy sz"  $3=tag
  local KIT="$1" SH="$2" TAG="$3"
  local RUN OUT
  if [ -e "$KIT/latest_run" ]; then RUN="$(cd "$KIT/latest_run" && pwd)"
  else
    RUN=""; for d in "$KIT"/run_*; do [ -f "$d/se_dump.npy" ] && RUN="$(cd "$d" && pwd)"; done
  fi
  [ -n "$RUN" ] || { echo "[p2] ABORT — $KIT 압밀 런 없음"; return 1; }
  OUT="$OUTDIR/${TAG}.json"
  [ -s "$OUT" ] && { echo "[p2] SKIP (있음) $TAG"; return 0; }

  # 이 vox 의 직경-보존 σ_VGCF 를 다시 뽑는다 (격자마다 다르다 — 기존 러너와 같은 규약)
  local SIGMA
  #  ⚠ 2026-08-16 실사고: `P2_SCR` 를 이 heredoc 에 안 넘겨 KeyError 로 전 팔이 실패했다.
  #    (fail-closed 는 작동했다 — 쓰레기 대신 0 팔을 냈다.)  두 변수를 **여기서** 넘긴다.
  SIGMA=$(cd "$RUN" && P2_SCR="$SCR" STEP3_VOX="$VOX" python3 - <<'PY'
import os, sys
import numpy as np
sys.path.insert(0, os.environ['P2_SCR'])
import step3_sigma as s3
VOX, D_REF = float(os.environ['STEP3_VOX']), 0.15
dia, ph = np.load('fibre_dia.npy'), np.load('phase.npy')
st = s3.dia_stats_by_phase(dia, ph)
v = st.get(2)
if v is None or not v['uniform']:
    sys.stderr.write(f'ABORT — VGCF Ø 비균일/부재: {v}\n'); raise SystemExit(1)
se, pv = s3.diameter_preserving_sigma(100.0, dia[ph == 2], D_REF, VOX)
sys.stderr.write(f'  [p2] vox {VOX}: σ_VGCF 100 → {se:.6g}\n')
print(f'{se:.6g}')
PY
  ) || return 1

  ( cd "$RUN" && P2_SCR="$SCR" python3 "$SCR/sr01_stamp_compare.py" \
      --extract-payload "$KIT/run_mpm.sh" --stamp segment \
      --extra-flags "--sigma-vgcf $SIGMA --step3-vox $VOX --step3-bridge-um $BRIDGE_UM --step3-origin-shift $SH" \
      --tag "$TAG" --out-name "$(basename "$OUT")" > "_$TAG.sh" ) || return 1
  { echo 'set -uo pipefail'; echo "KIT=\"$KIT\""; echo "SCR=\"$SCR\"";
    echo "PSIG=(${MPM_PERIODIC_SIGMA:+--periodic})"; cat "$RUN/_$TAG.sh"; } > "$RUN/$TAG.sh"
  rm -f "$RUN/_$TAG.sh"
  # ★ fail-closed — 세 인자가 **실제로** 주입됐는지 확인 (조용히 빠지면 팔이 오염된다)
  for NEEDLE in "--step3-vox $VOX" "--step3-origin-shift $SH" "--step3-bridge-um $BRIDGE_UM"; do
    grep -q -- "$NEEDLE" "$RUN/$TAG.sh" || { echo "[p2] ABORT — 미주입: $NEEDLE"; return 1; }
  done
  echo "[p2] ── $TAG  shift=($SH)  σ_VGCF=$SIGMA"
  ( cd "$RUN" && bash "$TAG.sh" ) || { echo "[p2] $TAG FAILED"; return 1; }
  [ -s "$RUN/$(basename "$OUT")" ] && mv "$RUN/$(basename "$OUT")" "$OUT"
}

echo "[p2] vox $VOX · 브리지 $BRIDGE_UM µm 고정 · $ARMS 팔 · out $OUTDIR"
i=0
for SH in "${SHIFTS[@]}"; do
  [ "$i" -ge "$ARMS" ] && break
  for K in kit_SBE kit_DBE; do
    [ -d "$K" ] || { echo "[p2] ABORT — $K 없음 (~/sdcp 에서 돌릴 것)"; exit 2; }
    #  ★ fail-fast — 한 팔이 실패하면 **전체를 멈춘다**.  실패한 팔을 빼고 계속하면
    #    팔 수가 달라져 앙상블이 오염된다 (판정기가 HOLD 를 내겠지만 GPU 시간을 버린다).
    if ! run_arm "$(cd "$K" && pwd)" "$SH" "p2_${K#kit_}_a${i}"; then
      echo "[p2] ABORT — 팔 p2_${K#kit_}_a${i} 실패.  원인을 고치고 다시 돌릴 것"
      echo "     (이미 끝난 팔은 $OUTDIR 에 남아 있어 다음 실행에서 SKIP 된다)"
      exit 1
    fi
  done
  i=$((i+1))
done

echo
echo "[p2] 수집 — 판정은 하지 않는다 (prereg §5 순서로 따로)"
python3 "$SCR/sdcp_gain_verdict.py" --dir "$OUTDIR" --collect-only
