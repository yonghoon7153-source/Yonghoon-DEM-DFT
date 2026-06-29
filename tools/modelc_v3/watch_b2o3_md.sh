#!/usr/bin/env bash
# b2o3 UMA-MD 라이브 점검. 1회 출력 (반복하려면: watch -n 30 bash <이 파일>).
# 각 온도(600/800/1000K)는 equilib 5 + prod 50 = 55 ps에서 끝, msd.json 기록.
set +H
R="${1:-/data/work/runs/b2o3_md}"
echo "════ $(date '+%m-%d %H:%M:%S')  b2o3 UMA-MD  ($R) ════"
if P=$(pgrep -f disorder_ensemble_diffusion.py); then
  echo "✅ MD 실행중 PID=$P  경과 $(ps -o etime= -p $P 2>/dev/null | tr -d ' ')"
else
  echo "⛔ 실행 중 MD 없음 (끝났거나 죽음)"
fi
echo "── T별 상태 (600→800→1000) ──"
for t in 600 800 1000; do
  j="$R/d0.00_cfg0/T$t/msd.json"; m="$R/d0.00_cfg0/T$t/md.log"
  if [ -f "$j" ]; then
    python3 -c "import json;v=json.load(open('$j')).get('D_Li_cm2_s');print('  T$t  ✓ 완료   D_Li = %s'%(('%.3e cm2/s'%v) if v else 'n/a'))"
  elif [ -f "$m" ]; then
    l=$(tail -1 "$m"); echo "  T$t  ▶ 진행중  ~$(echo "$l"|awk '{print $1}')/55 ps  ($(echo "$l"|awk '{print $NF}') K)"
  else
    echo "  T$t  · 대기"
  fi
done
if [ -f "$R/ensemble_results.json" ]; then
  echo "── 완료 헤드라인 (Ea/D0) ──"
  grep -A8 '"headline"' "$R/ensemble_results.json" 2>/dev/null | head -10 | sed 's/^/  /'
fi
echo "── 메인 로그 끝 3줄 ──"; tail -n 3 "$R/b2o3_md.log" 2>/dev/null | sed 's/^/  /'
echo "── GPU ──"; nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv,noheader 2>/dev/null | sed 's/^/  /'
