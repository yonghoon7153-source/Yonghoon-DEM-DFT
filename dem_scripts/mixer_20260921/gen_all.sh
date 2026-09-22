#!/usr/bin/env bash
# 믹서 캠페인 덱 생성 — 원장 docs/session_20260921_mixer_decisions.md §10 (1저자 비준 2026-09-21)
# 6 팔 × 시드 가중 = 10 런: L0·LB1·LB2·LB3 (시드 1) + LC·LA (시드 3).  전부 층상 삽입.
# + 기준 런 3 (E0 균일·점착 0·회전 0, 캠페인 시드) — Lacey S_R² 기준 (리뷰 R-2).
# 사용:  bash dem_scripts/mixer_20260921/gen_all.sh            (리포 루트에서)
#        FORCE=1 … 로그가 있는(이미 돈) 디렉터리도 다시 만든다.  살아 있는 런은 FORCE 로도 안 건드린다.
#
# ★★ 2026-09-22 — **실행 중인 런의 덱을 제자리에서 덮어쓰지 않는다.**  LIGGGHTS 는 입력 파일을
#   **읽어 가며** 실행한다.  옛 판은 13 디렉터리를 무조건 다시 썼고(같은 inode 를 잘라 새로 씀), 09-21 에
#   먼저 띄운 `E0_s32452843` 이 옛 덱 6,917 B 를 다 실행한 뒤 EOF 자리에서 **새 덱의 6,917 번째 바이트부터**
#   (`… fx fy f|z radius`) 를 명령으로 읽어 `Unknown command: z radius` 로 죽었다.
#   ⇒ ⓐ `pid` 가 살아 있으면 건너뛴다 · 로그가 있으면 FORCE=1 없이 건너뛴다
#      ⓑ 덱은 `<dir>.new/` 에 만든 뒤 **`mv` 로 바꿔 넣는다** (rename = 새 inode ⇒ 실행 중인 프로세스는
#         옛 inode 를 끝까지 읽는다).  회귀: test_launcher.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
OUT="${OUT:-$ROOT/dem_scripts/mixer_20260921/runs}"
STL="${STL:-$ROOT/dem_scripts/mixer_20260919}"          # Drum/Front/Back.stl 출처
N_TOTAL="${N_TOTAL:-100000}"; CGF="${CGF:-151.4}"; REV="${REV:-8}"
mkdir -p "$OUT"
skipped=0; made=0
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
  #  ⓐ 가드 — 살아 있는 런은 절대, 이미 돈 런은 FORCE 없이는 건드리지 않는다
  if [ -f "$d/pid" ] && kill -0 "$(cat "$d/pid")" 2>/dev/null; then echo "· 실행 중 — 건너뜀: $d"; continue; fi
  if [ -f "$d/log.lmp" ] && [ "${FORCE:-0}" != 1 ]; then echo "· 로그 있음(이미 돈 런) — 건너뜀 (FORCE=1 로 다시 만듦): $d"; continue; fi
  #  ⓑ 새 디렉터리에 만들고 rename 으로 바꿔 넣는다
  rm -rf "$d.new"
  python3 "$ROOT/scripts/make_mixer_deck.py" --out "$d.new" --n-total "$N_TOTAL" --cgf "$CGF" \
      --arm "$arm" --seed "$seed" --revolutions "$rev" > "$d.gen.log" 2>&1 || { echo "⛔ $arm s$seed 생성 실패 — $d.gen.log"; exit 1; }
  cp "$STL"/Drum.stl "$STL"/Front.stl "$STL"/Back.stl "$d.new/"
  mkdir -p "$d"
  for f in in.mixer Drum.stl Front.stl Back.stl; do mv -f "$d.new/$f" "$d/$f"; done
  if [ -d "$d.new/data" ]; then rm -rf "$d/data"; mv "$d.new/data" "$d/data"; fi
  rm -rf "$d.new"
  #  ★ 후처리 계약 (리뷰 R-14): 기대 원자수 · 드럼 반경을 런 옆에 기록 — check_contact_validity --n-expected,
  #    measure_mixing_index --r-container 가 이것을 읽는다 (기본값에 기대지 않는다)
  grep -oE 'N=[0-9,]+' "$d.gen.log" | head -1 | tr -d 'N=,' > "$d/n_expected"
  grep -oE 'R +[0-9.]+ mm' "$d.gen.log" | head -1 | awk '{printf "%.6f\n", $2/1000}' > "$d/r_container"
  echo "✓ $(basename "$d")  rev=$rev  n=$(cat "$d/n_expected")  R=$(cat "$d/r_container") m  $(grep -m1 -oE 'Fr [0-9.]+' "$d.gen.log")"
done
echo "생성 완료 → $OUT  (런 수: $(ls -d "$OUT"/*_s*/ 2>/dev/null | wc -l))"
