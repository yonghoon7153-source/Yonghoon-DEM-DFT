# R 사다리 감시 (읽기만 · σ 를 열지 않는다 — 파일 수 · 프로세스 · GPU 만) · 쓰는 법: watch -n 60 bash ~/rwatch.sh <P0|P1> <시도 번호>
L=$1; N=$2; D=$HOME/sdcp/ca1_ladder_$L; A=$D/attempt_$N; G=$HOME/sdcp/ca1_logs/ladder_${L}_a$N.log
date '+%m-%d %H:%M:%S'
echo "사슬 $(pgrep -f "^[^ ]*python[0-9.]* [^ ]*rint_r_chain[.]py --stage ladder --law $L" | wc -l) 개 · 원장 자리: $(ls -d $HOME/sdcp/ca1_ledger $HOME/sdcp/ca1_ledger.parked 2>/dev/null | xargs -r -n1 basename | tr '\n' ' ')"
echo "런 폴더 $(find "$D" -mindepth 1 -maxdepth 3 -type d -name 'L[0-9]*' 2>/dev/null | wc -l) · 끝난 팔 JSON $(find "$D" -maxdepth 4 -name 'p2_*.json' 2>/dev/null | wc -l) · launch $(ls "$A/groups" 2>/dev/null | grep -c 'launch.json$') · 요약 $([ -f "$A/ladder_summary.json" ] && echo '있음 (사다리 끝)' || echo 없음)"
echo "사슬 로그 마지막 고침 $(stat -c '%y' "$G" 2>/dev/null | cut -c1-19) · $(wc -l < "$G" 2>/dev/null) 줄"
nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total,temperature.gpu --format=csv,noheader
nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader
