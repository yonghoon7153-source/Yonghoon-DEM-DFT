#!/usr/bin/env bash
# 0.2C 충전 스텝이 **완전히 저장된 뒤** 남은 스케줄을 멈춘다.
#   (지금 V100 에서 도는 킷은 옛 버전이라 STOP 센티널이 없다 — 그 대용)
#
# step4_dyn 저장 순서:  (1) 결과 npz  →  (2) chain state  →  (3) viz json
#   ⇒ viz json 이 뜨면 그 스텝 산출물은 **전부** 디스크에 있다.  그 뒤엔 아무 때나 죽여도 안전.
#
# 사용:  nohup bash stop_after_02c.sh <RUN_DIR> > stopwatch.log 2>&1 &
set -uo pipefail
RUN="${1:?사용: bash stop_after_02c.sh /path/to/run_dir}"
cd "$RUN" || exit 1
echo "[watch] $RUN — 0.2C 충전 완료 대기…  $(date)"
while :; do
  ls -1 step4_*viz*chg_c0.2*.json >/dev/null 2>&1 && break
  sleep 60
done
echo "[watch] ✓ 0.2C 산출물 완비 $(date) — 이제 무슨 일이 나도 안 사라짐:"
ls -1sh step4_*chg_c0.2*.npz step4_*viz*chg_c0.2*.json s4state_*.npz 2>/dev/null
# ── 안전 종료: pkill -f 는 **자기 자신·부모 셸까지 잡을 수 있다**(실측).  PID 를 골라 제외한다.
SELF="$$"; PARENT="$PPID"
victims=""
for pat in 'step4_dyn\.py' 'run_mpm\.sh'; do
  for p in $(pgrep -f "$pat" 2>/dev/null); do
    [ "$p" = "$SELF" ] && continue
    [ "$p" = "$PARENT" ] && continue
    victims="$victims $p"
  done
done
if [ -z "$victims" ]; then
  echo "[watch] 돌고 있는 런 없음 — 이미 끝났거나 다른 호스트."
else
  echo "[watch] 종료 대상 PID:$victims"
  ps -o pid=,cmd= -p $victims 2>/dev/null | sed 's/^/         /'
  kill $victims 2>/dev/null
  sleep 5
  still=$(for p in $victims; do kill -0 "$p" 2>/dev/null && echo "$p"; done)
  [ -n "$still" ] && { echo "[watch] 안 죽은 PID → KILL: $still"; kill -9 $still 2>/dev/null; }
fi
echo "[watch] 완료 $(date).  회수:  tar -czf ~/harvest_02c.tar.gz \\"
echo "          mpm_payload.json mpm_metrics.json mpm_input.json mpm_run.log \\"
echo "          step4_*chg_c0.2*.npz step4_*viz*chg_c0.2*.json s4state_*.npz"
