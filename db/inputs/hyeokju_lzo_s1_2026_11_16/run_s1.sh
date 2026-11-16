#!/usr/bin/env bash
# [혁주] 1 단계 열역학 — 카드 db/properties/hyeokju_lzo_stage1_reactivity_card_2026_11_16.json
# QE 가 아니다: MP 조회 + pymatgen 상도 (CPU · GPU 안 씀). gabia 에서 tmux 로 돈다.
#   ① 닫힌계 LPSCl · LZO × NCA721 · NCA811 (양극 Li 함량 y = 1.0 … 0.1) · kink 전부
#   ② 닫힌계 LPSCl × LZO · 앵커 LPSCl × LiCoO2 / Li0.5CoO2 (G2)
#   ③ 열린계 LPSCl · LZO × NCA721 · NCA811 (y = 1) · 2.5–5.0 V (vs Li/Li+) 0.1 V 간격
#   ④ 열린계 LPSCl × LZO · 같은 전압 격자
# 이 스크립트가 못 하는 것: 판독 · 그림 · 3.8/4.4 V 라벨 (혁주 자료 전에는 안 붙인다) · push (자격 증명은 사용자가)
set -euo pipefail
PY=${PY:-/data/apps/miniforge3/envs/uma/bin/python}
O=db/properties; D=2026_11_16; T=tools/oxidation/interface_reactivity_v2.py
CL=$O/hyeokju_lzo_s1_closed_$D.jsonl; OP=$O/hyeokju_lzo_s1_open_$D.jsonl
[ -n "${MP_API_KEY:-}" ] || { echo "⛔ MP_API_KEY 없음"; exit 2; }
for x in $(pgrep -f "hyeokju_lzo_s1_(closed|open)" || true); do
  case "$(cat /proc/$x/comm 2>/dev/null)" in python*) echo "⛔ 이미 도는 중 PID $x"; exit 3;; esac
done
RES=""
if [ -n "${RESUME:-}" ]; then RES="--resume"; else
  [ ! -e "$CL" ] && [ ! -e "$OP" ] || { echo "⛔ 결과 파일이 이미 있다 — 이어 돌리려면 RESUME=1"; exit 4; }
fi
CATS=()
for y in 1.0 0.9 0.8 0.7 0.6 0.5 0.4 0.3 0.2 0.1; do
  CATS+=("Li${y}Ni0.7Co0.2Al0.1O2:NCA721_y${y}" "Li${y}Ni0.8Co0.1Al0.1O2:NCA811_y${y}")
done
VS=$(LC_ALL=C seq 2.5 0.1 5.0)
echo "== 판 $(git rev-parse --short HEAD) · pymatgen $($PY -c 'import pymatgen.core as c; print(c.__version__)' 2>/dev/null || echo '?') · 시작 $(date '+%F %T')"
echo "== ① 닫힌계 LPSCl · LZO × NCA (y 격자 20) $(date '+%T')"
$PY $T --closed --record_kinks $RES --only "LPSCl:Li6PS5Cl" "LZO:Li2ZrO3" --cathodes "${CATS[@]}" --out $CL
echo "== ② 닫힌계 LPSCl × LZO · 앵커 LCO $(date '+%T')"
$PY $T --closed --record_kinks --resume --only "LPSCl:Li6PS5Cl" --cathodes "Li2ZrO3:LZO" "LiCoO2:LCO_full" "Li0.5CoO2:LCO_half" --out $CL
echo "== ③ 열린계 LPSCl · LZO × NCA721 · NCA811 $(date '+%T')"
$PY $T $RES --only "LPSCl:Li6PS5Cl" "LZO:Li2ZrO3" --cathodes "LiNi0.7Co0.2Al0.1O2:NCA721" "LiNi0.8Co0.1Al0.1O2:NCA811" --voltages $VS --out $OP
echo "== ④ 열린계 LPSCl × LZO $(date '+%T')"
$PY $T --resume --only "LPSCl:Li6PS5Cl" --cathodes "Li2ZrO3:LZO" --voltages $VS --out $OP
echo "== 줄 수 (기대: 닫힌계 43 · 열린계 5) $(wc -l < $CL) · $(wc -l < $OP)"
echo "✅ 끝 $(date '+%F %T')"
