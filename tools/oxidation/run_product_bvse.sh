#!/usr/bin/env bash
# 분해산물이 Li 를 통과시키는지 — BVSE (계면 판정의 세 번째 조각)
# RUN on gabia:  bash tools/oxidation/run_product_bvse.sh
set -e
cd "$(dirname "$0")/../.."
: "${MP_API_KEY:?MP_API_KEY 가 환경에 있어야 한다}"
python3 tools/oxidation/product_bvse.py --selftest
echo "──── 시범 5종 (한 종에 몇 초인지 본다) ────"
python3 tools/oxidation/product_bvse.py --limit 5
echo "──── 전수 78종 ────"
python3 tools/oxidation/product_bvse.py
echo "DONE -> db/properties/cascade_product_bvse.json (커밋해서 보내 주세요)"
