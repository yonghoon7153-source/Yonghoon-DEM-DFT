#!/usr/bin/env bash
# 캐스케이드 90종 vs **Li 금속 음극** — 닫힌계(0 V) 계면 반응.
#
# ⛔ 왜 앞 배치(run_cascade_interface_90.sh)와 따로인가
#    앞 배치는 Li 저장고를 연 grand-potential 이라 상대가 **순수 Li 면 정의가 안 된다**
#    (정규화 분모 0 → ZeroDivisionError, 2026-08-19 실측). Li 음극 쪽은 닫힌계로 잰다.
#    Sundar 2025 Fig.2 의 Li-anode 판이 정확히 이 계산이다.
#
# ⚠ **두 배치의 숫자를 같은 표에 섞지 말 것.** 전압축이 있는 값(양극 쪽)과
#    0 V 한 점(Li 쪽)은 다른 잣대다. 파일도 따로 둔다.
#
# 비용 — chemsys 가 (도펀트 + Li,P,S,Cl,O) 뿐이라 양극 쪽보다 작다. 쌍당 2~5초 예상,
#    90종이면 10분 안쪽. GPU 안 씀.
#
# RUN on gabia:  bash tools/oxidation/run_cascade_interface_li.sh
set -e
cd "$(dirname "$0")/../.."
: "${MP_API_KEY:?MP_API_KEY 가 환경에 있어야 한다}"

python3 tools/oxidation/interface_reactivity_v2.py --selftest

python3 tools/oxidation/interface_reactivity_v2.py \
  --batch_from --resume --closed \
  --cathodes "Li:Li_metal" \
  --out db/properties/cascade_interface_li.jsonl

echo "DONE -> db/properties/cascade_interface_li.jsonl (커밋해서 보내 주세요)"
