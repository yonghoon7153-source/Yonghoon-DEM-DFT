#!/usr/bin/env bash
# (B)(A)(C) — MP 만 쓰는 싼 축 셋. 전부 새 DFT 0건, GPU 안 씀.
#   B  분해산물 밴드갭     — 계면 게이트의 자인된 약점("분해산물 전자전도도 미고려")을 메운다
#   A  안정성 3축 47→90종  — 이미 검증된 표의 커버리지 구멍 (hull · H2S · 계면 4상대)
#   C  전도조제 탄소 계면   — ASSB 실제 고장 모드 (litdb cho2024)
#
# RUN on gabia:  bash tools/oxidation/run_cascade_extras.sh
# ⚠ 앞 배치(interface_90 / interface_li)가 아직 돌고 있어도 된다 — 파일이 다 다르다.
#   다만 MP 속도 제한을 셋이 나눠 쓰니 진행바가 느려지면 하나씩 돌릴 것.
set -e
cd "$(dirname "$0")/../.."
: "${MP_API_KEY:?MP_API_KEY 가 환경에 있어야 한다}"

echo "════════ (B) 분해산물 밴드갭 ════════"
python3 tools/oxidation/sei_product_gaps.py --selftest
# 기존 47종 표의 반응식 + 지금 돌린 계면 배치의 반응식을 **다 모아서** 조회한다.
SRC=(db/properties/cascade_stability_axes.csv)
[ -f db/properties/cascade_interface_90.jsonl ] && SRC+=(db/properties/cascade_interface_90.jsonl)
[ -f db/properties/cascade_interface_li.jsonl ] && SRC+=(db/properties/cascade_interface_li.jsonl)
python3 tools/oxidation/sei_product_gaps.py \
  --from_reactions "${SRC[@]}" \
  --out db/properties/cascade_product_gaps.json

echo
echo "════════ (A) 안정성 3축 47 → 90종 ════════"
# 같은 CSV 에 이어 붙는다 — 기존 47행은 resume 이 건너뛴다.
python3 tools/cascade/stability_axes.py --run --pool v2

echo
echo "════════ (C) 전도조제 탄소 계면 ════════"
python3 tools/oxidation/interface_reactivity_v2.py \
  --batch_from --resume --closed \
  --cathodes "C:carbon" \
  --out db/properties/cascade_interface_carbon.jsonl

echo
echo "DONE — 커밋해서 보내 주세요:"
echo "  db/properties/cascade_product_gaps.json"
echo "  db/properties/cascade_stability_axes.csv   (47 → 90행)"
echo "  db/properties/cascade_interface_carbon.jsonl"
