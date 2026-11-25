#!/usr/bin/env bash
# =============================================================================
# run_comp2_phonon_gabia.sh — DFT-relaxed comp2 champion의 UMA Γ-phonon "한번 더".
#
# V0는 -45.8i 안장이었음 -> v3 followmin을 DFT-relax(고정셀, PS4 유지) 한 뒤
# 진짜 최소인지 재확인. comp_phonon_uma.py 재사용 = -45.8i 찾은 그 프로토콜(직접 비교).
# 그 툴은 입력을 UMA로 gentle-relax(RMSD 보고) 후 Γ 유한차분 -> DFT/UMA 기하 불일치 자동 처리.
#
# 게이트: relaxed 구조(comp2_V0_v3_relaxed.xyz)는 relax가 PS4 4배위 검증 통과 시에만 저장됨.
#   -> 그 파일 대기. relax 끝났는데 파일 없으면 = 골격 깨짐/실패 -> phonon 취소.
#
#   gabia(uma): tmux new -s c2phon -d 'bash tools/electronic/run_comp2_phonon_gabia.sh > ~/comp2_phonon.log 2>&1'
#   (relax와 동시에 걸어도 됨 — relaxed 구조 나올 때까지 대기하다 자동 시작)
# =============================================================================
set -u; set +H
REPO=${REPO:-$HOME/Yonghoon-DEM-DFT}; [ -d "$REPO" ] || REPO=$HOME/work/Yonghoon-DEM-DFT
RELWORK=${RELWORK:-/data/work/runs/comp2_relax}
REL=$RELWORK/comp2_V0_v3_relaxed.xyz
OUT=${OUT:-/data/work/runs/comp2_phonon_v3}
DEVICE=${DEVICE:-cuda}
UMA_PY=$(ls /data/apps/miniforge3/envs/uma/bin/python3 2>/dev/null || which python3)
cd "$REPO"
[ "$(pgrep -fc run_comp2_phonon_gabia)" -le 2 ] || { echo "이미 실행중"; exit 1; }

# relaxed 구조 대기 (relax 완료+PS4 통과 시 생성). 실패/골격깨짐이면 파일 안 생김 -> 감지.
while [ ! -f "$REL" ]; do
  if ! pgrep -f run_comp2_relax_gabia >/dev/null 2>&1; then
    echo "!! relax 끝났는데 $REL 없음 = PS4 골격 깨졌거나 relax 실패 -> phonon 취소."
    grep -aA10 "골격 검증" "$HOME/comp2_relax.log" 2>/dev/null | tail -12
    exit 1
  fi
  echo "[$(date +%H:%M:%S)] relax 진행중 — relaxed 구조 대기 (2분 후 재확인)"; sleep 120
done
echo "[$(date +%H:%M:%S)] relaxed 구조 확보: $REL"

# GPU 대기 (relax pw.x 잔여). relax 끝났으면 보통 바로 통과.
while [ "${SKIP_WAIT:-0}" != 1 ] && pgrep -f 'pw\.x' >/dev/null 2>&1; do
  echo "[$(date +%H:%M:%S)] pw.x 아직 있음 — 1분 후 재확인 (GPU 비었으면 SKIP_WAIT=1)"; sleep 60
done
echo "[$(date +%H:%M:%S)] UMA Γ-phonon 시작 (device=$DEVICE, comp_phonon_uma 프로토콜)"

"$UMA_PY" tools/electronic/comp_phonon_uma.py \
  --structure "$REL" --label comp2_v3_relaxed \
  --out "$OUT" --device "$DEVICE" \
  --fmax_relax 0.005 --delta 0.01 --imag_tol_cm1 20 \
  --uma_model uma-s-1p1 --uma_task omat
rc=$?
echo ""
if [ "$rc" = 0 ]; then
  echo ">> 판정(STABLE/SOFT) + 최저 모드 + UMA-relax RMSD 붙여줘."
  echo "   STABLE(허수 없음) = champion 자격 완성(안장 해소 확인). SOFT면 DFT ph.x(Γ) 에스컬레이션 논의."
else
  echo "!! phonon 실행 오류(rc=$rc) — 위 tail 확인 (device cpu로 재시도 가능: DEVICE=cpu)"
fi
