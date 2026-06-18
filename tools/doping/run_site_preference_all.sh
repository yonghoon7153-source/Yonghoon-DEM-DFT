#!/usr/bin/env bash
# Site-preference (antisite swap, same-composition, all-UMA) over EVERY dopant
# already processed by the 273-cascade.
#
# RESUMABLE: any system whose  $OUT/<sys>/site_pref.json  already exists is
# SKIPPED, so re-running only does the new ones.  Use  --force  to redo all.
#
# Run on gabia / kserver116 (UMA env active):
#     bash tools/doping/run_site_preference_all.sh            # do pending only
#     bash tools/doping/run_site_preference_all.sh --force    # redo everything
#     CAS=/path OUT=/path DEVICE=cuda FMAX=0.05 bash run_site_preference_all.sh
#
# Outputs: $OUT/<sys>/site_pref.json (+ M_at_P.xyz, M_at_Li.xyz, relax logs)
#          $OUT/master_<date>.log    + a final summary table.
set -u
CAS="${CAS:-/data/work/runs/multi_category_2026_05_26_v23}"
OUT="${OUT:-/data/work/runs/site_preference}"
DEVICE="${DEVICE:-cuda}"
FMAX="${FMAX:-0.05}"
STEPS="${STEPS:-300}"
FORCE="${1:-}"
HERE="$(cd "$(dirname "$0")" && pwd)"
PY="$HERE/site_preference_swap.py"

mkdir -p "$OUT"
LOG="$OUT/master_$(date +%m%d_%H%M).log"
echo "=== site-preference batch  $(date) ===" | tee "$LOG"
echo "CAS=$CAS  OUT=$OUT  DEVICE=$DEVICE  FMAX=$FMAX  FORCE=${FORCE:-no}" | tee -a "$LOG"

shopt -s nullglob
n_skip=0; n_run=0; n_fail=0
for d in "$CAS"/*_x0*/; do
  sys="$(basename "$d")"
  [ "$sys" = "_master_logs" ] && continue
  res="$OUT/$sys/site_pref.json"

  if [ -f "$res" ] && [ "$FORCE" != "--force" ]; then
    echo "skip(done) $sys" | tee -a "$LOG"; n_skip=$((n_skip+1)); continue
  fi

  xyz="$(python3 "$PY" --find_champion --sys "$sys" --cas "$CAS" 2>/dev/null)"
  if [ -z "$xyz" ] || [ ! -f "$xyz" ]; then
    echo "no-champion  $sys" | tee -a "$LOG"; n_fail=$((n_fail+1)); continue
  fi

  echo ">>> RUN $sys" | tee -a "$LOG"
  if python3 "$PY" --sys "$sys" --xyz "$xyz" --out "$OUT/$sys" \
        --device "$DEVICE" --fmax "$FMAX" --steps "$STEPS" >>"$LOG" 2>&1; then
    n_run=$((n_run+1))
    python3 - "$res" <<'PY' | tee -a "$LOG"
import json,sys
d=json.load(open(sys.argv[1]))
if d.get("status")=="ok":
    print(f"   {d['sys']} {d['dopant']}: dE={d['dE_per_dopant_eV']:+.3f} eV/dopant -> {d['preferred_site']}")
else:
    print(f"   {d['sys']}: {d.get('status')} ({d.get('reason','')[:60]})")
PY
  else
    echo "FAIL $sys" | tee -a "$LOG"; n_fail=$((n_fail+1))
  fi
done

echo "=== done: run=$n_run skip=$n_skip fail/no-champ=$n_fail ===" | tee -a "$LOG"
echo | tee -a "$LOG"
python3 "$PY" --summary --out "$OUT" | tee -a "$LOG"
echo "(full log: $LOG)"
