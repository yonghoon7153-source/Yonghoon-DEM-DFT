#!/usr/bin/env bash
# 캐스케이드 90종 x {LiCoO2, NCM811, Li metal} 계면 반응성 (전압 분해).
#
# 왜 이게 싼가 — 새 DFT 를 한 건도 안 돌린다. MP 의 GGA/GGA+U 에너지를 받아
#   pymatgen GrandPotentialInterfacialReactivity 로 두 상을 x:1-x 로 섞어
#   가장 발열이 큰 조합을 찾는다 (Richards/Ong 2016). Sundar 2025 Fig.2 와 같은
#   알고리즘이고, 우리는 거기에 **전압축(mu_Li)** 까지 얹은 판이다.
#
# ⛔ 90종을 한 chemsys 에 넣으면 안 된다 — 원소 합집합이 44개라 끝나지 않는다.
#    종마다 (Li,P,S,Cl,O + 도펀트 + 상대물질) 로 따로 돈다. 그래서 오래 걸린다.
#
# 비용 — MP 질의가 병목이지 물리가 아니다. 종·상대 한 쌍에 수십 초~수 분.
#    270 쌍이면 몇 시간. JSONL 이라 **중간에 끊고 --resume 로 이어붙일 수 있다.**
#
# RUN on gabia (MP_API_KEY 가 이미 환경에 있음):  bash run_cascade_interface_90.sh
set -e
cd "$(dirname "$0")/../.."
: "${MP_API_KEY:?MP_API_KEY 가 환경에 있어야 한다 (gabia 는 이미 설정됨)}"

python3 tools/oxidation/interface_reactivity_v2.py --selftest

# ⛔ 상대는 **전이금속 하나짜리**로 (2026-08-19 실측 정정)
#    · NCM811 은 Ni·Co·Mn 셋을 얹어 chemsys 가 10원소가 되고 **17종에서 MP 가 거절**한다
#      (`MPRestError: Please specify fewer elements`). LiCoO2·LiNiO2·LiMn2O4 로 나눈다
#      — 이러면 전 종이 6~8원소라 통과하고, 한 쌍에 12~16초다(NCM811 은 72~78초였다).
#    · **Li 금속은 여기서 못 잰다.** Li 저장고를 연 grand-potential 은 상대가 순수 Li 면
#      정규화 분모가 0 이라 ZeroDivisionError 다. Li 음극 쪽은 **닫힌계(0 V)** 로 따로.
#      (도구가 이제 돌기 전에 막고 이유를 JSONL 에 남긴다.)
CATHODES=("LiCoO2:LCO" "LiNiO2:LNO" "LiMn2O4:LMO")

# ① 시범 3종 — 한 쌍에 몇 초인지 먼저 잰다.
python3 tools/oxidation/interface_reactivity_v2.py \
  --batch_from --limit 3 --resume \
  --cathodes "${CATHODES[@]}" \
  --voltages 2.5 3.0 3.5 4.0 4.3 \
  --out db/properties/cascade_interface_90.jsonl

echo
echo "=== 시범 3종 끝. 전체 90종 x 3 상대 = 270 쌍 (~15초/쌍 → 1시간 남짓) ==="
python3 tools/oxidation/interface_reactivity_v2.py \
  --batch_from --resume \
  --cathodes "${CATHODES[@]}" \
  --voltages 2.5 3.0 3.5 4.0 4.3 \
  --out db/properties/cascade_interface_90.jsonl

echo "DONE -> db/properties/cascade_interface_90.jsonl (커밋해서 보내 주세요)"
