#!/usr/bin/env bash
# 기준선 — **도핑 안 한** 전해질을 같은 네 축에 태운다.
#
# 왜 필요한가 (2026-08-19) — 90종이 Li 음극과 −0.38~−0.66 으로 전부 반응하는데,
#   **도핑 안 한 LPSCl 도 Li 와 반응한다**(잘 알려진 사실). 기준선이 없으면
#   "도핑이 개선인가 악화인가" 를 말할 수 없다. 탄소·양극 축도 마찬가지다.
#   ⇒ 이 스크립트가 없으면 앞 배치의 모든 숫자가 **부호 없는 절대값**으로만 남는다.
#
# 두 기준선을 넣는다 — 우리 덱이 이 둘을 비교하므로:
#   LPSCl    = Li6PS5Cl        (comp1, 화학량론)
#   LPSCl1.6 = Li5.4PS4.4Cl1.6 (modelc, Cl-rich)
#
# RUN on gabia:  bash tools/oxidation/run_interface_baseline.sh   (1분 안쪽)
set -e
cd "$(dirname "$0")/../.."
: "${MP_API_KEY:?MP_API_KEY 가 환경에 있어야 한다}"
BASE=("LPSCl:Li6PS5Cl" "LPSCl1.6:Li5.4PS4.4Cl1.6")

echo "──── 양극 3종 × 5전압 (grand-potential) ────"
python3 tools/oxidation/interface_reactivity_v2.py \
  --only "${BASE[@]}" --resume \
  --cathodes "LiCoO2:LCO" "LiNiO2:LNO" "LiMn2O4:LMO" \
  --voltages 2.5 3.0 3.5 4.0 4.3 \
  --out db/properties/cascade_interface_baseline.jsonl

echo "──── Li 음극 + 탄소 (닫힌계 0 V) ────"
python3 tools/oxidation/interface_reactivity_v2.py \
  --only "${BASE[@]}" --resume --closed \
  --cathodes "Li:Li_metal" "C:carbon" \
  --out db/properties/cascade_interface_baseline_closed.jsonl

echo "DONE -> db/properties/cascade_interface_baseline{,_closed}.jsonl (커밋해서 보내 주세요)"
