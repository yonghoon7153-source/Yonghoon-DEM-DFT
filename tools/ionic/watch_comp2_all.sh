#!/usr/bin/env bash
# comp2 COMBINED monitor: ELASTIC (USPP k444) + DISORDER-MD ensemble in one view.
#   watch -n 30 bash tools/ionic/watch_comp2_all.sh
# env: EL=elastic dir, DIS=disorder out_root, LOG=disorder log
EL=${EL:-/data/work/runs/comp2_elastic_uspp}
DIS=${DIS:-$HOME/work/runs/comp2_disorder}
LOG=${LOG:-$HOME/work/comp2_disorder.log}
now=$(date +%s)

echo "=== comp2 monitor: ELASTIC + DISORDER-MD   $(date '+%m-%d %H:%M') ==="
echo "GPU: $(nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader 2>/dev/null | head -1)"
for p in $(pgrep -f 'pw\.x' 2>/dev/null); do
  echo "   ├ pw.x pid$p  cwd=$(readlink /proc/$p/cwd 2>/dev/null | sed 's#.*/##')"
done
echo "----------------------------------------------------------------------"

# ---------- ELASTIC ----------
echo "[ELASTIC] comp2 USPP k444"
ndone=0
for s in 11 22 33 23 13 12; do for pm in m p; do
  f="$EL/strain_${s}_${pm}.out"; nm="strain_${s}_${pm}"
  if [ ! -f "$f" ]; then echo "  $nm   ·대기"; continue; fi
  it=$(grep -ac "iteration #" "$f" 2>/dev/null)
  if grep -qa "JOB DONE" "$f" 2>/dev/null; then
    echo "  $nm   ✓DONE ($it it)"; ndone=$((ndone+1))
  else
    mt=$(stat -c %Y "$f" 2>/dev/null || echo "$now"); age=$(( (now - mt)/60 ))
    if [ "$age" -lt 3 ]; then echo "  $nm   ▶도는중 (it $it)"
    else echo "  $nm   ⚠미완·비활성 (it $it · ${age}m)"; fi
  fi
done; done
echo "  진행: $ndone/12 DONE"
echo "----------------------------------------------------------------------"

# ---------- DISORDER MD ----------
echo "[DISORDER MD] comp2 anion-disorder ensemble (Cl/Br<->S2-)"
if pgrep -af 'disorder_ensemble_diffusion\.py' 2>/dev/null | grep -q comp2_disorder; then
  echo "  driver: ALIVE"
else
  echo "  driver: (없음 — GPU-wait / 완료 / 미시작)"
fi
shopt -s nullglob; found=0
for cd in "$DIS"/d*_cfg*; do
  [ -d "$cd" ] || continue; found=1; nm=$(basename "$cd"); done=0; line="  $nm : "
  for T in 600 800 1000; do
    if [ -f "$cd/T$T/msd.json" ]; then line+="${T}K✓ "; done=$((done+1)); else line+="${T}K· "; fi
  done
  line+=" [$done/3]"; echo "$line"
done
[ "$found" = 0 ] && echo "  (config 없음 — equilib 중이거나 GPU 대기)"
grep -aE "cfg[0-9]+ Ea=|### d=|structure sanity" "$LOG" 2>/dev/null | tail -4
tail -1 "$LOG" 2>/dev/null
echo "----------------------------------------------------------------------"
echo "baseline: comp2 ordered Ea 0.276±0.033 | comp1 0.253  (disorder가 낮추면 가설 확증)"
