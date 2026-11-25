#!/usr/bin/env bash
# =============================================================================
# chain_after_c1long.sh — kgy: comp1 1600 ps 가 끝나면 **자동으로** 6점 아레니우스 착수
#
# 왜 사슬로 거나
#   지금 kgy GPU 는 comp1 1600 ps 한 판이 잡고 있다(T600/800/1000 순차, 남은 ~2일).
#   그게 끝나는 시각을 사람이 지켜보고 있을 수 없고, 비어 있는 GPU 를 놀리기도 아깝다.
#   → 완료 조건을 걸어 두고 자동으로 다음 작업을 띄운다.
#
# 완료 판정 = comp1_seeds_p1600 아래 msd.json 이 **3개**(T600/800/1000) 생기는 것.
#   ⚠ 프로세스 생존으로 판정하지 않는다 — 죽어도 '없음'이 되어 사슬이 잘못 출발한다.
#     산출물의 존재로만 판정한다.
#
#   cd ~/Yonghoon-DEM-DFT && conda activate uma
#   tmux new -s arrchain -d 'bash tools/ionic/chain_after_c1long.sh 2>&1 | tee -a ~/logs/arrchain.log'
#
# ⚠ kgy 는 우리 브랜치가 아니다(claude/stoic-knuth-NObVQ). 이 스크립트와
#   run_arrhenius_6pt.sh · md_temperature_feasibility.py 를 먼저 가져와야 한다:
#     git fetch origin claude/friendly-meitner-lldvar && \
#     git checkout FETCH_HEAD -- tools/ionic/ db/structures/
# =============================================================================
set -uo pipefail; set +H
REPO="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$REPO"
unset LD_LIBRARY_PATH OPAL_PREFIX 2>/dev/null || true
LONG=${LONG:-$HOME/work/runs/comp1_seeds_p1600}
NEED=${NEED:-3}                       # T600/800/1000
POLL=${POLL:-600}                     # 10 분마다 확인
MAXWAIT=${MAXWAIT:-345600}            # 4일이면 포기하고 알린다
mkdir -p "$HOME/logs"

LOCK=${LOCK:-/tmp/arrchain.lock}
exec 9>"$LOCK" || { echo "⛔ 락 파일을 못 연다"; exit 1; }
command -v flock >/dev/null 2>&1 && { flock -n 9 || { echo "⛔ 이미 돈다 — 중단"; exit 0; }; }

ts(){ echo "[$(date +%m-%d\ %H:%M:%S)] $*"; }
count(){ ls "$LONG"/s*/d*_cfg*/T*/msd.json 2>/dev/null | wc -l; }

ts "사슬 시작 — comp1 1600 ps 완료 대기 (현재 $(count)/$NEED)"
WAITED=0
while [ "$(count)" -lt "$NEED" ]; do
  if [ "$WAITED" -ge "$MAXWAIT" ]; then
    ts "⛔ ${MAXWAIT}초 기다렸는데 안 끝났다 ($(count)/$NEED) — 사슬 중단. 손으로 확인할 것."
    exit 1
  fi
  # GPU 가 비었는데 산출물도 안 늘면 앞 작업이 죽은 것이다. 그건 사슬이 아니라 사람이 볼 일.
  sleep "$POLL"; WAITED=$((WAITED + POLL))
  [ $((WAITED % 3600)) -lt "$POLL" ] && ts "  대기 중 $(count)/$NEED · $((WAITED/3600))h 경과"
done

ts "✓ comp1 1600 ps 완료 ($(count)/$NEED) — 6점 아레니우스 착수"
# ⚠ 앞 작업이 GPU 메모리를 놓을 때까지 잠깐 둔다. 바로 붙이면 OOM 이 난다.
sleep 120
bash "$REPO/tools/ionic/run_arrhenius_6pt.sh"
ts "═══ 사슬 끝 ═══"
