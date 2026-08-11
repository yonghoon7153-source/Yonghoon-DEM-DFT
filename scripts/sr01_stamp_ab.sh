#!/usr/bin/env bash
# SR-01 (option 2) — 같은 압밀 베드 위에서 STEP3 탄소 래스터만 바꿔 **Δσ_e 를 실측**한다.
#
#   arm A = 점 스탬프 (현행 기본값)   → run_mpm.sh 가 이미 만든 mpm_payload.json
#   arm B = 선분 스탬프 (--step3-fibre-stamp segment) → mpm_payload_segstamp.json
#
# 압밀(STEP1)은 **다시 돌지 않는다** — 두 팔이 같은 se_dump.npy/fibre.npy 를 읽으므로
# 베드·섬유 시딩·난수가 바이트로 동일하고, 차이는 오직 래스터화뿐이다 (공통모드 완전 상쇄).
# 그래서 이 A/B 는 SR-01 이 묻는 것("스탬프 아티팩트가 σ_e 를 얼마나 움직이나")에
# 정확히 답한다 — 다른 어떤 것도 변하지 않기 때문이다.
#
# 사용:
#   bash scripts/sr01_stamp_ab.sh <KIT_DIR>            # latest_run 을 자동으로 씀
#   bash scripts/sr01_stamp_ab.sh <KIT_DIR> <RUN_DIR>  # 런 폴더를 직접 지정
#
# 예 (V100):
#   cd ~/Yonghoon-DEM-DFT/se_curve
#   bash ~/Yonghoon-DEM-DFT/scripts/sr01_stamp_ab.sh kit_ps_7_3
set -uo pipefail

KIT_IN="${1:-}"
if [ -z "$KIT_IN" ]; then
  echo "사용: bash scripts/sr01_stamp_ab.sh <KIT_DIR> [RUN_DIR]"; exit 2
fi
KIT="$(cd "$KIT_IN" && pwd)" || { echo "ABORT — 킷 폴더 없음: $KIT_IN"; exit 1; }
RUN="${2:-$KIT/latest_run}"
[ -e "$RUN" ] || { echo "ABORT — 런 폴더가 없습니다: $RUN"; \
                   echo "        먼저 압밀을 돌리세요:  bash $KIT/run_mpm.sh   (~2h)"; exit 1; }
RUN="$(cd "$RUN" && pwd)"
SCR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── venv (run_mpm.sh 와 같은 규약) ──
if [ -z "${VIRTUAL_ENV:-}" ] && [ -z "${MPM_NO_VENV:-}" ]; then
  for _v in "$SCR/../venv" "$SCR/../.venv" "$HOME/Yonghoon-DEM-DFT/venv"; do
    [ -f "$_v/bin/activate" ] && { . "$_v/bin/activate"; echo "[venv] $_v"; break; }
  done
fi

# ── arm A 확인.  없으면 여기서 멈춘다 (압밀 없이 payload 만 돌리면 STALE se_dump 를 읽는다) ──
if [ ! -f "$RUN/mpm_payload.json" ]; then
  echo "ABORT — arm A 산출물이 없습니다: $RUN/mpm_payload.json"
  echo "        run_mpm.sh 가 정상 종료했는지 확인하세요 (mpm_done.marker)."
  exit 1
fi
for f in se_dump.npy fibre.npy; do
  [ -f "$RUN/$f" ] || { echo "ABORT — $RUN/$f 가 없습니다 — 선분 스탬프는 --fibre 없이는 못 돕니다."; exit 1; }
done

# ── run_mpm.sh 에서 payload 호출부를 그대로 뽑아 --out 과 스탬프만 바꾼다 ──
#   (run_mpm.sh 자신이 실패 안내에서 권하는 패턴.  케이스별 플래그가 많아 손으로 옮기면 틀린다.)
cd "$RUN"
sed -n '/mpm_webapp_payload/,/--out mpm_payload.json/p' "$KIT/run_mpm.sh" > _payload_block.sh
grep -q 'mpm_webapp_payload' _payload_block.sh || { echo "ABORT — run_mpm.sh 에서 payload 호출부를 못 찾음"; exit 1; }
sed -i 's|--out mpm_payload.json|--step3-fibre-stamp segment --out mpm_payload_segstamp.json|' _payload_block.sh
grep -q 'step3-fibre-stamp segment' _payload_block.sh || { echo "ABORT — --out 치환 실패"; exit 1; }
{ echo 'set -uo pipefail'; echo "KIT=\"$KIT\""; echo "SCR=\"$SCR\""; cat _payload_block.sh; } > payload_segstamp.sh

echo "[sr01] arm B (선분 스탬프) 시작 — $RUN/mpm_payload_segstamp.json"
echo "[sr01]   압밀은 다시 안 돕니다 (같은 se_dump.npy/fibre.npy = 공통모드 상쇄)."
bash payload_segstamp.sh || { echo "[sr01] arm B FAILED — 위 트레이스"; exit 1; }

echo
python3 "$SCR/sr01_stamp_compare.py" "$RUN/mpm_payload.json" "$RUN/mpm_payload_segstamp.json" \
        --label "$(basename "$KIT")" --csv "$RUN/sr01_stamp_ab.csv"
echo
echo "[sr01] 회수할 것: $RUN/sr01_stamp_ab.csv  +  mpm_payload{,_segstamp}.json"
