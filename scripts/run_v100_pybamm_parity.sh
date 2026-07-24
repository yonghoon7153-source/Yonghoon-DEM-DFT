#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════
# V100: STEP4-v2 ↔ PyBaMM DFN 패리티 런 (#5 — defense_review 잔여 1조각)
#   지금 도는 0.2C CCCV 런이 step4_*.npz 를 남기면 실행.
#   mpm_metrics.json 에서 σ_e/σ_ion/두께/SE분율을 자동 추출 → 균질-트윈 DFN 대조.
# 사용: bash scripts/run_v100_pybamm_parity.sh <run_dir>
#   <run_dir> = mpm_metrics.json + step4_*.npz 가 있는 폴더 (예: run_VGCF1_PTFE1_*/latest_run)
# 프로토콜(§4·frame[4]): 균일-구조 극한에서 voxel-v2 ≈ pybamm 수 % = 솔버 검증;
#   실제 침대와의 편차 = 미세구조 효과 정량.  cross-fit 금지 — 대조만.
# ══════════════════════════════════════════════════════════════════════════
set -euo pipefail
RUN_DIR="${1:?사용법: run_v100_pybamm_parity.sh <run_dir (mpm_metrics.json + step4_*.npz)>}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
M="$RUN_DIR/mpm_metrics.json"
[ -f "$M" ] || { echo "mpm_metrics.json 없음: $M"; exit 1; }
NPZ=$(ls "$RUN_DIR"/step4_*.npz 2>/dev/null | head -1)
[ -n "$NPZ" ] || { echo "step4_*.npz 없음 (STEP4 런 완료 후 실행): $RUN_DIR"; exit 1; }

read -r SIGE SIGI EPS TH AMF <<<"$(python3 - "$M" <<'PY'
import json, sys
m = json.load(open(sys.argv[1])); s3 = m.get('step3', m) or {}
sige = s3.get('sigma_e_eff_S_cm'); sigi = s3.get('sigma_ion_eff_S_cm')
th = m.get('thickness_um') or m.get('thickness_mpm_um')
# eps(pybamm 전해질상) = SE 부피분율(전극 기준) — SE/solid × (1−porosity) 재구성; 키 없으면 보수 기본
por = (m.get('porosity_mpm_pct') or m.get('porosity_settled_pct') or 0.0) / 100.0
se_sol = m.get('se_solid_frac') or m.get('se_over_solid') or 0.30      # 로그 "SE/solid" (없으면 0.30 기본)
if se_sol > 1: se_sol /= 100.0
eps = se_sol * (1.0 - por)
amf = (1.0 - se_sol) * (1.0 - por)                                     # AM 부피분율 (전극 기준, 근사)
assert sige and sigi and th, f'metrics 키 부족: sigma_e={sige} sigma_ion={sigi} th={th}'
print(f'{sige} {sigi} {eps:.4f} {th} {amf:.4f}')
PY
)"
echo "추출: σ_e=$SIGE S/cm · σ_ion=$SIGI S/cm · ε(SE상)=$EPS · 두께=$TH µm · AM분율=$AMF"
echo "⚠ ε/AM분율은 metrics 재구성(키 없으면 SE/solid=0.30 기본) — 로그의 'SE/solid' 실측과 다르면 --eps/--am-frac 수동 지정"

python3 "$ROOT/scripts/step4_pybamm_anchor.py" --compare "$NPZ" \
  --sigma-e-S-cm "$SIGE" --sigma-ion-S-cm "$SIGI" --eps "$EPS" \
  --thickness-um "$TH" --am-frac "$AMF" --r-um 2.0 \
  --out "$RUN_DIR/step4_pybamm_compare.npz"
echo "완료 → $RUN_DIR/step4_pybamm_compare.npz  (V(t) 대조 — 수 % 이내 = 솔버 검증, 편차 = 미세구조 몫)"
