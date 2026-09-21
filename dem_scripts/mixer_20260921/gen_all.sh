#!/usr/bin/env bash
# 믹서 캠페인 덱 생성 — 원장 docs/session_20260921_mixer_decisions.md §10 (1저자 비준 2026-09-21)
# 6 팔 × 시드 가중 = 10 런: L0·LB1·LB2·LB3 (시드 1) + LC·LA (시드 3).  전부 층상 삽입.
# 사용:  bash dem_scripts/mixer_20260921/gen_all.sh            (리포 루트에서)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
OUT="${OUT:-$ROOT/dem_scripts/mixer_20260921/runs}"
STL="${STL:-$ROOT/dem_scripts/mixer_20260919}"          # Drum/Front/Back.stl 출처
N_TOTAL="${N_TOTAL:-100000}"; CGF="${CGF:-151.4}"; REV="${REV:-8}"
mkdir -p "$OUT"
python3 - "$ROOT" <<'PY' | while read -r arm seed; do
import sys; sys.path.insert(0, sys.argv[1] + '/scripts')
import importlib.util
spec = importlib.util.spec_from_file_location('m', sys.argv[1] + '/scripts/make_mixer_deck.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for arm, seed in m.CAMPAIGN:
    print(arm, seed)
PY
  d="$OUT/${arm}_s${seed}"
  python3 "$ROOT/scripts/make_mixer_deck.py" --out "$d" --n-total "$N_TOTAL" --cgf "$CGF" \
      --arm "$arm" --seed "$seed" --revolutions "$REV" > "$d.gen.log" 2>&1 || { echo "⛔ $arm s$seed 생성 실패 — $d.gen.log"; exit 1; }
  cp "$STL"/Drum.stl "$STL"/Front.stl "$STL"/Back.stl "$d/"
  echo "✓ $d  ($(grep -m1 'rpm 에서 Fr' "$d.gen.log" | sed 's/^ *//'))"
done
echo "생성 완료 → $OUT  (런 수: $(ls -d "$OUT"/*_s*/ | wc -l))"
