#!/usr/bin/env bash
# comp2 anion-disorder ensemble monitor.  usage:
#   watch -n 30 bash tools/ionic/watch_comp2_disorder.sh
# (optional arg1 = out_root, arg2 = log path)
R=${1:-$HOME/work/runs/comp2_disorder}
LOG=${2:-$HOME/work/comp2_disorder.log}

echo "=== comp2 DISORDER ensemble   $(date '+%m-%d %H:%M') ==="
echo "GPU: $(nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader 2>/dev/null | head -1)"
if pgrep -af 'disorder_ensemble_diffusion\.py' 2>/dev/null | grep -q comp2_disorder; then
  echo "driver: ALIVE"
else
  echo "driver: (없음 — 완료 or 대기 or GPU-wait)"
fi
echo "----------------------------------------------------------"

# per config x T progress (msd.json = that T done)
shopt -s nullglob
found=0
for cd in "$R"/d*_cfg*; do
  [ -d "$cd" ] || continue
  found=1; nm=$(basename "$cd"); done=0; line="  $nm : "
  for T in 600 800 1000; do
    f="$cd/T$T/msd.json"
    if [ -f "$f" ]; then
      D=$(grep -ao '"D_Li_cm2_s":[^,}]*' "$f" 2>/dev/null | head -1 | grep -ao '[-0-9.eE]*$')
      line+="${T}K✓(${D:-?}) "; done=$((done+1))
    else
      line+="${T}K· "
    fi
  done
  line+="  [$done/3]"; echo "$line"
done
[ "$found" = 0 ] && echo "  (아직 config 디렉토리 없음 — equilib 중이거나 GPU 대기)"
echo "----------------------------------------------------------"

# config별 Ea + level 집계 (드라이버 stdout)
echo "[Ea] 드라이버 로그:"
grep -aE "cfg[0-9]+ Ea=|### d=|structure sanity|d=.*T=[0-9]+:" "$LOG" 2>/dev/null | tail -8
echo "..."
tail -2 "$LOG" 2>/dev/null
echo "----------------------------------------------------------"
echo "ordered baseline (비교): comp2 Ea 0.276±0.033  /  comp1 0.253  (disorder가 낮추면 가설 확증)"
