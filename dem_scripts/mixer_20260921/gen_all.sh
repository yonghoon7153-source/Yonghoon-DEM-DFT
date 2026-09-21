#!/usr/bin/env bash
# 믹서 캠페인 덱 생성 — 원장 docs/session_20260921_mixer_decisions.md §10 (1저자 비준 2026-09-21)
# 6 팔 × 시드 가중 = 10 런: L0·LB1·LB2·LB3 (시드 1) + LC·LA (시드 3).  전부 층상 삽입.
# + 기준 런 3 (E0 균일·점착 0·회전 0, 캠페인 시드) — Lacey S_R² 기준 (리뷰 R-2).
# 사용:  bash dem_scripts/mixer_20260921/gen_all.sh            (리포 루트에서)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
OUT="${OUT:-$ROOT/dem_scripts/mixer_20260921/runs}"
STL="${STL:-$ROOT/dem_scripts/mixer_20260919}"          # Drum/Front/Back.stl 출처
N_TOTAL="${N_TOTAL:-100000}"; CGF="${CGF:-151.4}"; REV="${REV:-8}"
mkdir -p "$OUT"
python3 - "$ROOT" <<'PY' | while read -r arm seed rev; do
import sys; sys.path.insert(0, sys.argv[1] + '/scripts')
import importlib.util
spec = importlib.util.spec_from_file_location('m', sys.argv[1] + '/scripts/make_mixer_deck.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for arm, seed in m.CAMPAIGN:            # 측정 런 10 개 (REV 바퀴)
    print(arm, seed, 'REV')
for arm, seed, rev in m.REFERENCE:      # 기준 런 3 개 (회전 0 — measure_mixing_index --ref 상대)
    print(arm, seed, rev)
PY
  [ "$rev" = REV ] && rev="$REV"
  d="$OUT/${arm}_s${seed}"
  python3 "$ROOT/scripts/make_mixer_deck.py" --out "$d" --n-total "$N_TOTAL" --cgf "$CGF" \
      --arm "$arm" --seed "$seed" --revolutions "$rev" > "$d.gen.log" 2>&1 || { echo "⛔ $arm s$seed 생성 실패 — $d.gen.log"; exit 1; }
  cp "$STL"/Drum.stl "$STL"/Front.stl "$STL"/Back.stl "$d/"
  #  ★ 후처리 계약 (리뷰 R-14): 기대 원자수 · 드럼 반경을 런 옆에 기록 — check_contact_validity --n-expected,
  #    measure_mixing_index --r-container 가 이것을 읽는다 (기본값에 기대지 않는다)
  grep -oE 'N=[0-9,]+' "$d.gen.log" | head -1 | tr -d 'N=,' > "$d/n_expected"
  grep -oE 'R +[0-9.]+ mm' "$d.gen.log" | head -1 | awk '{printf "%.6f\n", $2/1000}' > "$d/r_container"
  echo "✓ $(basename "$d")  rev=$rev  n=$(cat "$d/n_expected")  R=$(cat "$d/r_container") m  $(grep -m1 -oE 'Fr [0-9.]+' "$d.gen.log")"
done
echo "생성 완료 → $OUT  (런 수: $(ls -d "$OUT"/*_s*/ | wc -l))"
