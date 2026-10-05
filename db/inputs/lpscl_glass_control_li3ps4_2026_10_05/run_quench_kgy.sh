#!/usr/bin/env bash
# =============================================================================
# run_quench_kgy.sh — li2s 대조 계 a-Li₃PS₄ 유리 담금질 5 시드 (kgy)
#   카드 db/properties/lpscl_smallcell_glass_control_li3ps4_estimand_2026_10_05.json §1b · 결정 D-2026-10-05-lpscl-smallcell-glass-control-li3ps4
#   melt_quench_uma.py --system B --n_fu 15 --seed S --quench_rate 1e12 --melt_ps 100 --hold_ps 50 --dt_fs 2 --save_ps 1.0 --turbo
#   = A 의 담금질과 같은 인자 (lpscl_smallcell_uma_qe_force_estimand_2026_09_16.json '도구') · --system · --n_fu 만 다르다 (120 원자).
#   끝난 시드마다 --seed_gate 로 게이트 입력(원시·relax 두 판)을 남긴다 — 판정은 repo 에서 카드대로.
#
# 사용 (kgy · tmux 안 · 이 카드를 담은 커밋의 git worktree 에서):
#   SELFTEST=1 bash db/inputs/lpscl_glass_control_li3ps4_2026_10_05/run_quench_kgy.sh   # 가드 시험 (음성 포함 · UMA 안 부름)
#   DRY_RUN=1  bash db/inputs/lpscl_glass_control_li3ps4_2026_10_05/run_quench_kgy.sh   # 5 시드 셀·계획만 (임시 폴더 · UMA 안 부름)
#   bash db/inputs/lpscl_glass_control_li3ps4_2026_10_05/run_quench_kgy.sh              # 시드 1→5 차례로 (한 번에 하나)
# env: PY (/home/kgy/apps/miniforge3/envs/uma/bin/python · 절대경로 — base python 은 fairchem 이 없다)
#      RUN (~/work/runs/lpscl_glass_control_li3ps4_2026_10_05) · SEEDS ("1 2 3 4 5") · START_MAX_MIB (20000)
#      WAIT_MAX_S (21600 — GPU 가 비기를 기다리는 최대 시간) · DECISION (위 결정 ID — 원장에서 active 여야 시작한다)
#
# ⛔ 못 하는 것: 시드 게이트·T₅₀ 를 판정하지 않는다 (입력만 남긴다 · 판정은 repo) · 600 K MD 를 돌리지 않는다 ·
#   이미 결과가 있는 시드를 덮어쓰지 않는다 (건너뛴다) · 중간에 멈춘 시드 폴더를 보면 **멈춘다** (흔적을 지우지 않는다 —
#   다시 도는 것은 사람이 정하는 실행 복구다 · 카드 §7) · 다른 UMA 잡(cascade 등)을 건드리지 않는다.
# =============================================================================
set -uo pipefail
W=$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)
cd "$W" || { echo "⛔ $W 없음"; exit 1; }
CARD=db/properties/lpscl_smallcell_glass_control_li3ps4_estimand_2026_10_05.json
DECISION=${DECISION:-D-2026-10-05-lpscl-smallcell-glass-control-li3ps4}
PY=${PY:-/home/kgy/apps/miniforge3/envs/uma/bin/python}
RUN=${RUN:-$HOME/work/runs/lpscl_glass_control_li3ps4_2026_10_05}
SEEDS=${SEEDS:-"1 2 3 4 5"}
START_MAX_MIB=${START_MAX_MIB:-20000}
WAIT_MAX_S=${WAIT_MAX_S:-21600}
TAG=lpscl_glass_control_li3ps4_2026_10_05           # 잡 고유 인자 — pgrep 은 이것으로만 (공용 이름 금지)
ARGS=(--system B --n_fu 15 --quench_rate 1e12 --melt_ps 100 --hold_ps 50 --dt_fs 2 --save_ps 1.0 --turbo)
N_ATOMS_EXPECTED=120

say() { echo "[$(date '+%F %T')] $*" | tee -a "${LOG:-/dev/null}"; }
decision_active() {   # $1 = 결정 ID · 원장(이 worktree)에서 active 면 0
  "$PY" - "$1" <<'PY'
import json, sys
d = json.load(open("db/governance/decisions.json"))
x = [e for e in d["decisions"] if e.get("id") == sys.argv[1]]
sys.exit(0 if x and x[0].get("decision_state") == "active" else 1)
PY
}
gpu_used() { if [ -n "${FAKE_GPU_USED:-}" ]; then echo "$FAKE_GPU_USED"; else nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | head -1 | tr -d ' '; fi; }
seed_state() {        # $1 = 시드 · done | partial | empty
  local d="$RUN/B/seed$1"
  if [ -e "$d/result.json" ]; then echo done
  elif [ -e "$d" ] && [ -n "$(ls -A "$d" 2>/dev/null)" ]; then echo partial
  else echo empty; fi
}
our_running() { for x in $(pgrep -f "$TAG/B" 2>/dev/null); do case "$(cat /proc/$x/comm 2>/dev/null)" in python*) echo "$x";; esac; done | head -1; }
dry_one() {           # $1 = 시드 · $2 = 출력 루트 (임시) → n_atoms 를 찍는다
  "$PY" tools/ionic/melt_quench_uma.py "${ARGS[@]}" --seed "$1" --out_root "$2" --dry_run 2>&1 | grep -E "원자|dry_run" | head -2
}

if [ "${SELFTEST:-0}" = 1 ]; then
  fails=0; ck() { if eval "$2"; then echo "  ✓ $1"; else echo "  ✗ $1"; fails=$((fails+1)); fi; }
  T=$(mktemp -d)
  ck "카드가 이 worktree 에 있다" "[ -f $CARD ]"
  ck "결정 $DECISION 이 원장에서 active" "decision_active $DECISION"
  ck "⛔음성 없는 결정 ID 는 active 가 아니다" "! decision_active D-0000-00-00-nope"
  ck "GPU 가드: 사용 1000 MiB 이면 시작 가능 (문턱 $START_MAX_MIB)" "[ \$(FAKE_GPU_USED=1000 gpu_used) -le $START_MAX_MIB ]"
  ck "⛔음성 GPU 가드: 사용 23000 MiB 이면 시작 안 함" "! [ \$(FAKE_GPU_USED=23000 gpu_used) -le $START_MAX_MIB ]"
  RUN0=$RUN; RUN=$T/run
  mkdir -p $RUN/B/seed2 $RUN/B/seed3; echo '{}' > $RUN/B/seed2/result.json; echo x > $RUN/B/seed3/plan.json
  ck "끝난 시드(result.json)는 done — 건너뛴다 (덮어쓰지 않는다)" "[ \$(seed_state 2) = done ]"
  ck "⛔음성 중간에 멈춘 시드 폴더는 partial — 멈춘다" "[ \$(seed_state 3) = partial ]"
  ck "빈 시드는 empty — 돈다" "[ \$(seed_state 1) = empty ]"
  RUN=$RUN0
  ck "인자: --system B · --n_fu 15 · 1e12 · turbo (A 와 같은 일정)" "[[ \" ${ARGS[*]} \" == *' --system B --n_fu 15 --quench_rate 1e12 --melt_ps 100 --hold_ps 50 --dt_fs 2 --save_ps 1.0 --turbo '* ]]"
  out=$(dry_one 1 "$T/dry")
  ck "실제 경로 dry_run: B seed1 = $N_ATOMS_EXPECTED 원자 (n_fu 기본 50 = 400 원자를 막는다)" "[[ \"$out\" == *\"$N_ATOMS_EXPECTED 원자\"* ]]"
  ck "⛔음성 n_fu 를 빼면 400 원자 — 이 시험이 그걸 잡는다" "[[ \"\$(\"$PY\" tools/ionic/melt_quench_uma.py --system B --seed 1 --quench_rate 1e12 --out_root $T/dry2 --dry_run 2>&1)\" != *\"$N_ATOMS_EXPECTED 원자\"* ]]"
  rm -rf "$T"
  echo "selftest $([ $fails = 0 ] && echo PASS || echo FAIL) ($fails 실패)"; [ $fails = 0 ]; exit $?
fi

[ -f "$CARD" ] || { echo "⛔ 카드가 이 worktree 에 없다 ($CARD)"; exit 1; }
"$PY" -c "import ase, numpy" 2>/dev/null || { echo "⛔ PY=$PY 에 ase/numpy 없음"; exit 1; }
decision_active "$DECISION" || { echo "⛔ 결정 $DECISION 이 원장에서 active 가 아니다 — 시작하지 않는다"; exit 1; }

if [ "${DRY_RUN:-0}" = 1 ]; then
  T=$(mktemp -d); echo "DRY_RUN · worktree $(git rev-parse --short=9 HEAD 2>/dev/null) · RUN $RUN · 시드 $SEEDS"
  for S in $SEEDS; do echo "  seed$S · 상태 $(seed_state $S) · $(dry_one $S "$T" | head -1)"; done
  echo "  GPU 사용 $(gpu_used) MiB (시작 문턱 ≤ $START_MAX_MIB) · 우리 잡 $(our_running || true)"
  rm -rf "$T"; exit 0
fi

"$PY" -c "import fairchem" 2>/dev/null || { echo "⛔ PY=$PY 에 fairchem 없음 (uma env 절대경로인지 본다)"; exit 1; }
[ -z "$(our_running)" ] || { echo "⛔ 같은 잡이 이미 돈다 (PID $(our_running)) — 두 번 띄우지 않는다"; exit 1; }
mkdir -p "$RUN/logs"; LOG=$RUN/run_quench_kgy.log; TSV=$RUN/quench_kgy.tsv
[ -f "$TSV" ] || printf 'seed\tstart\tend\twall_s\trc\n' > "$TSV"
say "START @ $(git rev-parse --short=9 HEAD) · 변경 $(git status --porcelain 2>/dev/null | wc -l) · RUN $RUN · 시드 $SEEDS · 인자 ${ARGS[*]}"
for S in $SEEDS; do
  st=$(seed_state "$S")
  if [ "$st" = done ]; then say "seed$S — 이미 끝남 (result.json) · 건너뛴다"; continue; fi
  if [ "$st" = partial ]; then say "⛔ seed$S — 결과 없이 폴더만 있다 (중간에 멈춤?) · 멈춘다 — 흔적을 보고 사람이 정한다"; exit 3; fi
  waited=0
  while [ "$(gpu_used)" -gt "$START_MAX_MIB" ]; do
    [ $waited -ge $WAIT_MAX_S ] && { say "⛔ GPU 사용 $(gpu_used) MiB > $START_MAX_MIB 가 ${WAIT_MAX_S}s 계속 — 멈춘다"; exit 4; }
    [ $((waited % 1800)) = 0 ] && say "GPU 사용 $(gpu_used) MiB > $START_MAX_MIB — 기다린다"
    sleep 60; waited=$((waited+60))
  done
  t0=$(date +%s); say "seed$S 시작 · GPU 사용 $(gpu_used) MiB"
  "$PY" tools/ionic/melt_quench_uma.py "${ARGS[@]}" --seed "$S" --out_root "$RUN" > "$RUN/logs/seed$S.log" 2>&1; rc=$?
  t1=$(date +%s); printf '%s\t%s\t%s\t%s\t%s\n' "$S" "$(date -d @$t0 '+%F %T')" "$(date -d @$t1 '+%F %T')" $((t1-t0)) $rc >> "$TSV"
  grep -aE "원자 · 셀|UMA inference mode" "$RUN/logs/seed$S.log" | head -2 | sed 's/^/   /' | tee -a "$LOG"
  if [ $rc != 0 ] || [ ! -e "$RUN/B/seed$S/result.json" ]; then say "⛔ seed$S rc $rc · result.json $( [ -e $RUN/B/seed$S/result.json ] && echo 있음 || echo 없음) — 뒤 시드를 돌리지 않는다"; exit 2; fi
  "$PY" tools/ionic/melt_quench_uma.py --seed_gate "$RUN/B/seed$S" > "$RUN/logs/seed${S}_gate.log" 2>&1
  say "seed$S 끝 · $((t1-t0)) s · 게이트 입력 rc $? (판정은 repo)"
done
say "✅ 끝 — 시드 $SEEDS · 다음: 회수(새 worktree) → repo 에서 시드 게이트 · T₅₀ 스캔 → 600 K 러너"
