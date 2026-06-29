#!/usr/bin/env bash
# b2o3 UMA-MD 살아있는지 점검. SSH 끊겨도 setsid라 살아야 정상.
# 사용: bash tools/modelc_v3/watch_b2o3_md.sh   (gabia에서)
set +H
echo "════════ $(date '+%m-%d %H:%M')  b2o3 UMA-MD 상태 ════════"
echo "── MD 프로세스 (이게 핵심) ──"
if pgrep -af disorder_ensemble_diffusion.py; then
  echo "  ✅ MD 실행 중"
else
  echo "  ⛔ 실행 중인 MD 없음 (꺼짐 또는 미실행)"
fi
echo "── 출력/로그 위치 탐색 ──"
found=$(find /data/work /tmp -maxdepth 5 -path "*b2o3_md*" \
        \( -name "*.log" -o -name "ensemble_results.json" -o -name "msd.json" \) 2>/dev/null)
if [ -n "$found" ]; then
  echo "$found"
  L=$(echo "$found" | grep -m1 '\.log$')
  [ -n "$L" ] && { echo "── 로그 끝 12줄 ($L) ──"; tail -n 12 "$L"; }
  R=$(echo "$found" | grep -m1 ensemble_results.json)
  [ -n "$R" ] && { echo "── 완료 결과 헤드라인 ──"; grep -A20 '"headline"' "$R" 2>/dev/null | head -25; }
else
  echo "  (b2o3_md 출력 없음 — 아직 한 번도 안 떴을 수 있음)"
fi
echo "── GPU ──"
nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader 2>/dev/null | sed 's/^/  proc: /'
nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv,noheader 2>/dev/null | sed 's/^/  GPU: /'
echo "※ ⛔이면 영구 위치에서 재실행:"
echo "   cd /data/work && git clone --depth 1 -b claude/friendly-meitner-lldvar https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT b2o3md 2>/dev/null; cd b2o3md"
echo "   bash tools/modelc_v3/run_b2o3_md.sh /data/work/runs/b2o3_md cuda"
