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

# ① 시범 3종 — 한 쌍에 몇 초/몇 분인지 먼저 잰다. 여기서 느리면 ②를 나눠 돌린다.
python3 tools/oxidation/interface_reactivity_v2.py \
  --batch_from --limit 3 --resume \
  --cathodes "LiCoO2:LCO" "LiNi0.8Co0.1Mn0.1O2:NCM811" "Li:Li_metal" \
  --voltages 2.5 3.0 3.5 4.0 4.3 \
  --out db/properties/cascade_interface_90.jsonl

echo
echo "=== 시범 3종 끝. 위 초 단위를 보고 전체를 돌린다 ==="
python3 tools/oxidation/interface_reactivity_v2.py \
  --batch_from --resume \
  --cathodes "LiCoO2:LCO" "LiNi0.8Co0.1Mn0.1O2:NCM811" "Li:Li_metal" \
  --voltages 2.5 3.0 3.5 4.0 4.3 \
  --out db/properties/cascade_interface_90.jsonl

echo "DONE -> db/properties/cascade_interface_90.jsonl (커밋해서 보내 주세요)"
