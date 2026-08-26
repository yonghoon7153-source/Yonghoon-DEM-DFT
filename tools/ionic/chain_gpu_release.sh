#!/usr/bin/env bash
# =============================================================================
# chain_gpu_release.sh — **GPU 가 비면** 후속 작업(QE 단일점 + Li 슬랩)을 착수.
#
# 왜 repo 로 옮겼나 — ~/chain_qe_slab.sh 로 임시 작성한 판본이 두 군데서 틀렸다.
#
#  (1) `tmux new -d -s chain2 "... > ~/logs/chain2.log 2>&1"` 인데 **~/logs 가 없었다.**
#      리다이렉트가 실패하면 셸이 즉시 죽고 tmux 세션도 같이 사라진다 — 조용히.
#      (증상: tmux ls 에 chain2 가 아예 없고 로그도 없음. "안 걸렸네"로 오해하기 딱 좋다.)
#      → 여기서는 로그 디렉터리를 **스크립트가 직접** 만든다.
#
#  (2) 대기 조건이 `pgrep -x pw.x` 였다. 이건 **CPU 빌드 pw.x 까지 문다.**
#      지금 gabia 에서 도는 ELF(CPU, k444)는 GPU 를 한 조각도 안 쓰는데,
#      그것 때문에 이 체인이 며칠씩 더 기다리게 된다.
#      → 이 체인이 기다려야 할 것은 **GPU 점유자**뿐이다:
#         · UMA MD (disorder_ensemble_diffusion / aimd_mlip)
#         · GPU 빌드 pw.x
#      실제 확인법도 같이 쓴다 — nvidia-smi 의 compute-apps 가 비면 그게 정답이다.
#
# 실행:
#   bash tools/ionic/chain_gpu_release.sh            # 포그라운드(테스트용)
#   tmux new -d -s chain2 'bash tools/ionic/chain_gpu_release.sh'   # 권장(로그는 자체 처리)
# =============================================================================
set -u
LOGDIR=${LOGDIR:-$HOME/logs}
mkdir -p "$LOGDIR"                       # ← (1) 즉사 방지
LOG=$LOGDIR/chain2.log
exec > >(tee -a "$LOG") 2>&1             # tmux 명령줄에 리다이렉트를 안 붙여도 되게

ts() { date '+%m-%d %H:%M:%S'; }

# 중복 실행 가드 (CLAUDE.md 공통 관례)
SELF=$(basename "$0")
# ⚠⚠ **pgrep 으로 세면 안 된다 (2026-08-03 실측 재발).** tmux 가 끼워 넣는 래퍼
#   (`sh -c 'bash ... | tee ...'`)까지 세기 때문에 세션이 하나도 없는데 -gt 1 이 참이 되어
#   **시작하자마자 죽는다.** 실제로 tmux ls 에 chain2 가 없는데 "이미 도는 ... 중단"만 찍혔다.
#   run_phaseB_slabfirst_gabia.sh 에서 같은 사고를 겪고 flock 으로 바꾼 그 함정이다.
LOCK=${LOCK:-/tmp/chain_gpu_release.lock}
exec 9>"$LOCK" || { echo "[$(ts)] 락 파일을 못 연다: $LOCK"; exit 1; }
if command -v flock >/dev/null 2>&1; then
  flock -n 9 || { echo "[$(ts)] 이미 도는 $SELF 가 있다 (flock $LOCK) — 중복 실행 중단"; exit 0; }
else
  echo "[$(ts)] flock 없음 — 중복 실행 가드 없이 진행한다"
fi

# ── GPU 점유자 판정 ──────────────────────────────────────────────────────
# ⚠ CPU 빌드 QE 는 **일부러 제외**한다 (위 (2)).
gpu_busy() {
  pgrep -f "disorder_ensemble_diffusion|aimd_mlip" >/dev/null && return 0
  pgrep -f "qe-.*-gpu/bin/pw\.x" >/dev/null && return 0
  # 최종 근거: 실제 VRAM 점유 프로세스가 있나
  local n
  # ⚠ `grep -c . || echo 0` 은 grep 이 0 을 찍고 **비영 종료**하면 "0\n0" 두 줄이 되어
  #   [ 에서 "integer expression expected" 로 터진다 (실측). 마지막 줄만 취해 한 줄로 만든다.
  n=$(nvidia-smi --query-compute-apps=pid --format=csv,noheader 2>/dev/null | grep -c . | tail -1)
  [ "${n:-0}" -gt 0 ] 2>/dev/null
}

echo "[$(ts)] chain 시작 — GPU 해방 대기 (CPU QE 는 무시)"
while gpu_busy; do
  HOLD=$(nvidia-smi --query-compute-apps=pid,used_memory --format=csv,noheader 2>/dev/null | tr '\n' ' ')
  CPUQE=$(pgrep -fc "qe-.*-cpu/bin/pw\.x" 2>/dev/null | tail -1); CPUQE=${CPUQE:-0}
  echo "[$(ts)] GPU 점유: ${HOLD:-?}  (무시 중인 CPU QE rank ${CPUQE}개) — 5분 뒤 재확인"
  sleep 300
done
echo "[$(ts)] GPU 해방 — 후속 착수"

# ── 후속 실행 ────────────────────────────────────────────────────────────
# ⭐ 2026-08-26 — `AFTER=` 로 **아무 명령이나** 예약할 수 있게 열었다.
#   종전에는 여기가 비어 있어서 이 체인이 "해방 시각 알림" 밖에 못 했다.
#   대기 로직(GPU 점유 판정 · CPU QE 제외 · flock · 로그디렉터리 자동생성)은
#   이미 실전에서 세 번 데어가며 다듬은 것이라 **그 자산을 살려 쓰는 게 맞다.**
#
#   예약:
#     tmux new -d -s chain2 'AFTER="bash tools/ionic/run_comp1_supercell.sh" \
#       V0XYZ=... LABEL=... bash tools/ionic/chain_gpu_release.sh'
#
# ⛔ 이 체인이 **못 하는 것**
#   · AFTER 명령의 성공을 보장하지 않는다 — 종료코드만 옮긴다.
#   · GPU 가 잠깐 비었다가 다른 사람이 채가는 경쟁은 못 막는다 (5분 폴링이다).
#   · AFTER 가 비어 있으면 **아무것도 실행하지 않고** 알림만 남긴다 (종전 동작).
echo "READY   at $(ts)"
if [ -n "${AFTER:-}" ]; then
  echo "[$(ts)] AFTER 실행: $AFTER"
  # ⚠ eval 이다 — 예약 문자열을 그대로 셸에 넘긴다. 신뢰하는 입력만 줄 것.
  eval "$AFTER"
  rc=$?
  echo "[$(ts)] AFTER 종료코드 $rc"
  exit $rc
fi
echo "AFTER 가 비어 있다 — 실행 없이 알림만 남긴다."
echo "다음 후보: ① mlip_committee.py 궤적 스냅샷 → QE 단일점 대조 (T1 절대 검증)"
echo "          ② Li‖LPSCl 슬랩 (T3 게이트, open_items 참조)"
