#!/usr/bin/env bash
# SR-01 — **σ_e 축 격자 수렴 시험** (SI 정정 [R2] 의 직접 근거).
#
# 왜: SI 는 "0.4-µm grid, a resolution **validated against measured ionic conductivities**"
#   라고 적는다.  그런데 래스터 규약 민감도는
#       이온  8 % (VGCF 1 wt%) ~ 21 % (2.97 wt%)      ← 거의 안 흔들리는 축
#       전자  48배                                     ← 주장이 걸린 축
#   즉 **민감하지 않은 채널로 검증하고 민감한 채널에 썼다.**  σ_e 축의 근거가 없다.
#
# 이 런: 같은 침대·같은 직경-보존 규약으로 **복셀만 줄여** σ_e 가 수렴하는지 본다.
#   직경-보존은 복셀에 맞춰 σ 를 다시 뽑으므로(σ_eff = σ_bulk·πd²/(4·vox²)) 격자를 바꿔도
#   **같은 물리를 겨냥한다** — 수렴하면 방법이 σ_e 축에서 검증된 것이고,
#   안 하면 그 사실이 SI 에 들어가야 할 한계다.
#     vox 0.4 → σ_VGCF 11.045   ·   vox 0.3 → σ_VGCF 19.635   ·   vox 0.25 → 28.274
#   ⚠ 계단 인자 k 는 격자에 거의 무관하다(방향의 성질, 실측 1.486) → 수렴을 가리지 않는다.
#   ⚠ 메모리: 셀 수 ∝ vox⁻³.  0.4→0.3 은 2.37배, 0.4→0.25 는 4.1배.  OOM 이면 그 사실이 결과다.
#
# 사용 (V100):
#   cd ~/sdcp
#   setsid nohup bash ~/dem-sk/scripts/sr01_grid_converge_e.sh kit_SBE 0.4 0.3 \
#     > grid_conv.log 2>&1 &
#   tail -f grid_conv.log
set -uo pipefail

KIT_IN="${1:-}"; shift || true
VOXES="${*:-0.4 0.3}"
[ -n "$KIT_IN" ] || { echo "사용: bash scripts/sr01_grid_converge_e.sh <KIT> [vox ...]"; exit 2; }
# ★ BRIDGE_UM 를 주면 AM 접촉 브리지 반경을 **물리 단위로 고정**한다 (CL-21 교란 분리).
#   기본(빈 값) = 현행 1.2·vox → 격자를 조이면 브리지도 같이 얇아져 탄소 효과와 섞인다.
#   예:  BRIDGE_UM=0.48 bash scripts/sr01_grid_converge_e.sh kit_SBE 0.4 0.3
BRIDGE_UM="${BRIDGE_UM:-}"
BR_FLAG=""; BR_TAG=""
if [ -n "$BRIDGE_UM" ]; then
  BR_FLAG=" --step3-bridge-um $BRIDGE_UM"; BR_TAG="b$(echo "$BRIDGE_UM" | tr -d '.')"
  echo "[gc] ★ 브리지 반경 **고정** $BRIDGE_UM µm — 격자와 무관하게 유지된다"
fi
KIT="$(cd "$KIT_IN" && pwd)"
SCR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -z "${VIRTUAL_ENV:-}" ] && [ -z "${MPM_NO_VENV:-}" ]; then
  for _v in "$SCR/../venv" "$SCR/../.venv" "$HOME/Yonghoon-DEM-DFT/venv"; do
    [ -f "$_v/bin/activate" ] && { . "$_v/bin/activate"; echo "[gc] venv $_v"; break; }
  done
fi

if [ -e "$KIT/latest_run" ]; then RUN="$(cd "$KIT/latest_run" && pwd)"
else
  CAND=""; N=0
  for d in "$KIT"/run_*; do [ -f "$d/se_dump.npy" ] || continue; CAND="$d"; N=$((N+1)); done
  [ "$N" = 1 ] || { echo "ABORT — 압밀된 런이 $N 개"; exit 1; }
  RUN="$(cd "$CAND" && pwd)"
fi
cd "$RUN"
echo "[gc] run: $RUN   vox 목록: $VOXES"

for VOX in $VOXES; do
  TAG="gc$(echo "$VOX" | tr -d '.')${BR_TAG}"
  OUT="mpm_payload_${TAG}.json"
  if [ -s "$OUT" ]; then echo "[gc] SKIP (있음) $OUT"; continue; fi

  # ── 이 vox 에 맞는 직경-보존 σ 를 **다시** 뽑는다 (격자마다 다르다) ──────────────
  SIGMA=$(STEP3_VOX="$VOX" python3 - <<'PY'
import os, sys
import numpy as np
sys.path.insert(0, os.path.expanduser('~/dem-sk/scripts'))
import step3_sigma as s3                                        # noqa: E402
VOX, D_REF = float(os.environ['STEP3_VOX']), 0.15
dia, ph = np.load('fibre_dia.npy'), np.load('phase.npy')
st = s3.dia_stats_by_phase(dia, ph)
v = st.get(2)
if v is None or not v['uniform']:
    sys.stderr.write(f'ABORT — VGCF Ø 비균일/부재: {v}\n'); raise SystemExit(1)
se, pv = s3.diameter_preserving_sigma(100.0, dia[ph == 2], D_REF, VOX)
sys.stderr.write(f'  [gc] vox {VOX}: σ_VGCF 100 → {se:.6g} (factor {pv["factor"]})\n')
print(f'{se:.6g}')
PY
  ) || exit 1

  python3 "$SCR/sr01_stamp_compare.py" --extract-payload "$KIT/run_mpm.sh" \
          --stamp segment --extra-flags "--sigma-vgcf $SIGMA --step3-vox $VOX$BR_FLAG" \
          --tag "$TAG" --out-name "$OUT" > "_$TAG.sh" || exit 1
  { echo 'set -uo pipefail'; echo "KIT=\"$KIT\""; echo "SCR=\"$SCR\"";
    echo "PSIG=(${MPM_PERIODIC_SIGMA:+--periodic})"; cat "_$TAG.sh"; } > "$TAG.sh"
  rm -f "_$TAG.sh"
  grep -q -- "--step3-vox $VOX" "$TAG.sh" || { echo "ABORT — vox 미주입"; exit 1; }
  if [ -n "$BRIDGE_UM" ]; then
    grep -q -- "--step3-bridge-um $BRIDGE_UM" "$TAG.sh" || { echo "ABORT — 브리지 미주입"; exit 1; }
  fi
  grep -q -- "--sigma-vgcf $SIGMA" "$TAG.sh" || { echo "ABORT — σ 미주입"; exit 1; }
  echo "[gc] ── vox $VOX · σ_VGCF $SIGMA → $OUT"
  bash "$TAG.sh" || { echo "[gc] vox $VOX FAILED (OOM 이면 그 사실이 결과다 — 기록할 것)"; }
done

python3 - "$BR_TAG" $VOXES <<'PY'
import json, os, sys

BR = sys.argv[1]
rows = []
for v in sys.argv[2:]:
    f = f"mpm_payload_gc{v.replace('.', '')}{BR}.json"
    if not os.path.exists(f):
        rows.append((v, None, None, None, 'FAILED/OOM')); continue
    d = json.load(open(f))
    s = d.get('step3') or (d.get('mpm_metrics') or {}).get('step3') or {}
    sh = s.get('dissipation_share') or {}
    rows.append((v, s.get('sigma_e_eff_S_cm'), s.get('sigma_ion_eff_S_cm'),
                 s.get('n_dof'), {k: round(x, 3) for k, x in sh.items() if x and x > 0.01}))
print()
print('── σ_e 격자 수렴 (직경-보존 규약 고정) ──────────────────────')
for v, se, si, nd, sh in rows:
    print(f'  vox {v:>5}  σ_e {str(se):<12} σ_ion {str(si):<12} dof {str(nd):<10} share {sh}')
ok = [(float(v), se) for v, se, *_ in rows if isinstance(se, (int, float))]
if len(ok) >= 2:
    ok.sort(reverse=True)                       # 굵은 격자 → 고운 격자
    print()
    for (v0, s0), (v1, s1) in zip(ok, ok[1:]):
        print(f'  {v0} → {v1} µm:  σ_e {s0:.4g} → {s1:.4g}  = {(s1/s0 - 1)*100:+.1f} %')
    print()
    print('  판정 규약 (SI [R2] 용): |Δ| < 10 % 면 "σ_e 축에서 수렴" 으로 SI 에 쓸 수 있다.')
    print('           그 이상이면 **미수렴을 그대로 적고** σ_e 를 밴드로 보고해야 한다.')
    print('  ⚠ 이것은 격자 수렴만이다 — 계단 인자 k(1.486)와 σ 재척도는 두 격자에 공통이라')
    print('    상쇄되고, 이 시험은 그 규약이 **옳은지**는 묻지 않는다 (자기일관성만).')
PY
