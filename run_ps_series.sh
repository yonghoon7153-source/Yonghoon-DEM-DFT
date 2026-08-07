#!/bin/bash
# P:S 5종 직렬 — 0.2C(step4_dyn) 종료를 스스로 기다렸다 시작.  one GPU = one run.
KITS=(kit_ps_10_0 kit_ps_7_3 kit_ps_5_5 kit_ps_3_7 kit_ps_0_10)
echo "[series] step4_dyn(0.2C) 종료 대기…  $(date)"
while pgrep -f step4_dyn.py >/dev/null; do sleep 300; done
echo "[series] GPU 비었음 — 시작  $(date)"
for k in "${KITS[@]}"; do
  echo "[series] ▶ $k  $(date)"
  bash "$k/run_mpm.sh"
  # run_mpm.sh 는 self-detach 후 즉시 리턴 — 실제 MPM 프로세스가 뜰 때까지 대기 (최대 10분)
  started=0
  for i in $(seq 60); do
    pgrep -f mpm3d_compaction.py >/dev/null && { started=1; break; }; sleep 10
  done
  [ "$started" = 1 ] || { echo "[series] ✗ $k MPM 미기동 — $k/run_*/mpm_run.log 확인 후 재개"; exit 1; }
  while pgrep -f mpm3d_compaction.py >/dev/null; do sleep 60; done
  echo "[series] ✓ $k 완료  $(date)"
done
echo "[series] 5/5 전부 완료  $(date)  — 각 kit_ps_*/latest_run/mpm_payload.json 을 웹앱 ③ 업로드"
