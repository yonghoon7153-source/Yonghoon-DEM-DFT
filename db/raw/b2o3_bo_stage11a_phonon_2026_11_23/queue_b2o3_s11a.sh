#!/bin/bash
# b2o3_s11a — run_uma_kgy.sh 가 2026-11-22 22:01:09 에 썼다
LOG=/data/work/runs/b2o3_bo_2026_11_09/s11a_relax.log; WAIT_FOR=''; SUMS=/data/work/runs/b2o3_bo_2026_11_09/queue_b2o3_s11a.sha256
if [ -n "$WAIT_FOR" ]; then while tmux has-session -t "$WAIT_FOR" 2>/dev/null; do sleep 60; done; fi
while :; do read -r U T < <(nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader,nounits | head -1 | tr -d ","); F=$((T-U)); [ "$F" -ge 4000 ] && break; echo "$(date "+%F %T") VRAM 여유 $F < 4000 — 대기" >> "$LOG"; sleep 120; done
if ! sha256sum -c --quiet "$SUMS" >> "$LOG" 2>&1; then echo "$(date "+%F %T") ⛔ 입력 · 소스가 제출 뒤 바뀌었다 — 발사 안 함 (종료 12)" >> "$LOG"; exit 12; fi
echo "$(date "+%F %T") 시작 (입력 · 소스 해시 재대조 통과)" >> "$LOG"
cd /data/work/runs/b2o3_bo_2026_11_09/src && PYTHONUNBUFFERED=1 /data/apps/miniforge3/envs/uma/bin/python tools/doping/run_anneal.py --xyz /data/work/runs/b2o3_bo_2026_11_09/s8_anneal/cfg0015_E-2254.436_O-bo4/post_relax.xyz /data/work/runs/b2o3_bo_2026_11_09/s8_anneal/cfg0019_E-2254.209_O-bo4/post_relax.xyz /data/work/runs/b2o3_bo_2026_11_09/s8_anneal/cfg0040_E-2252.241_O-bo4/post_relax.xyz --out /data/work/runs/b2o3_bo_2026_11_09/s11a_relax --temperature 500 --time_ps 0 --seed 20261109 --relax_fmax 0.01 --purpose b2o3_bo/stage11a_phonon_relax --device cuda >> "$LOG" 2>&1
run_rc=$?
echo "$(date "+%F %T") 끝 run_rc=$run_rc" >> "$LOG"
cd /data/work/runs/b2o3_bo_2026_11_09/src && /data/apps/miniforge3/envs/uma/bin/python tools/doping/run_anneal.py --check_results /data/work/runs/b2o3_bo_2026_11_09/s11a_relax/anneal_results.json --expect_n 3 --expect_time_ps 0 --expect_temperature 500 --expect_purpose b2o3_bo/stage11a_phonon_relax >> "$LOG" 2>&1
check_rc=$?
echo "$(date "+%F %T") 결과 검사 check_rc=$check_rc (0 = 요청한 시간 · 온도 · 개수 · 결과 파일 해시가 기록과 같다)" >> "$LOG"
if [ "$run_rc" -ne 0 ]; then exit "$run_rc"; fi
if [ "$check_rc" -ne 0 ]; then exit 13; fi
exit 0
