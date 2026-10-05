#!/usr/bin/env bash
# =============================================================================
# run_quench_kgy.sh — li2s 대조 계 a-Li₃PS₄ 유리 담금질 5 시드 (kgy 기본 · MACHINE=gabia 면 탄성 옆 공존 모드)
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
# MACHINE=gabia (2026-10-05 · 사용자 'gabia에서 진행하자' · 공존 결정 EXCEPTION_ID 가 active 여야 시작) — 기본값이 바뀐다:
#   PY /data/apps/miniforge3/envs/uma/bin/python · RUN /data/work/runs/<TAG> · START_MAX_MIB 42500 · COEXIST=1
#   COEXIST=1 이면 담금질 python 을 뒤에서 돌리고 SAMPLE 초마다 가드를 본다 (값·의미 = glass_main_queue_gabia.sh 의 v2 예외):
#     ① GPU 합계 > TOTALCAP 46000 · ② 우리 PID 트리 > OURCAP 3500 MiB (WARM 300 s 뒤) · ③ host < HOSTFLOOR 8192 MiB
#     ④ 탄성 작업방(ELW) 최신 *.out 에 GPU 메모리 오류 (우리 시드 시작 뒤 새로 쓰인 부분만)
#     → **우리 담금질만** 죽이고 예외를 닫는다 (다음 시드를 안 띄운다 · 자동 재시작 없음 · 종료 코드 6 = ①–③ · 7 = ④).
#   시작 문턱: GPU 합계 ≤ START_MAX_MIB 그리고 host ≥ HOSTFLOOR + 4096. ELW 에 *.out 이 없으면 **시작하지 않는다** (④ 가 말없이 무력해진다).
#   점유 표본 (회신 CS Q-CS-1 · gabia 는 실측): PMON_S (60) 초마다 `nvidia-smi pmon -c 1 -s u` → logs/seed<S>_pmon.tsv
#     (시각 · 우리 PID 트리 sm % · 모든 잡 sm % 합). 장부의 점유 = Σ Δt × 우리/합 (합이 0 인 표본은 우리 몫 1 — 보수) · 원값을 남긴다.
#   로그·장부 이름은 기계별: run_quench_<MACHINE>.log · quench_<MACHINE>.tsv (kgy 는 종전 이름 그대로).
#
# ⛔ 못 하는 것: 시드 게이트·T₅₀ 를 판정하지 않는다 (입력만 남긴다 · 판정은 repo) · 600 K MD 를 돌리지 않는다 ·
#   이미 결과가 있는 시드를 덮어쓰지 않는다 (건너뛴다) · 중간에 멈춘 시드 폴더를 보면 **멈춘다** (흔적을 지우지 않는다 —
#   다시 도는 것은 사람이 정하는 실행 복구다 · 카드 §7) · 다른 UMA 잡(cascade 등)을 건드리지 않는다 ·
#   공존 모드에서도 탄성 pw.x·탄성 러너를 건드리지 않는다 (가드는 우리 담금질만 죽인다) · 표본 간격(SAMPLE)보다 빠른 VRAM 급등은 못 막는다 ·
#   점유 GPU-h 를 계산하지 않는다 (원값만 남긴다 · 장부는 repo 에서).
# =============================================================================
set -uo pipefail
W=$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)
cd "$W" || { echo "⛔ $W 없음"; exit 1; }
CARD=db/properties/lpscl_smallcell_glass_control_li3ps4_estimand_2026_10_05.json
DECISION=${DECISION:-D-2026-10-05-lpscl-smallcell-glass-control-li3ps4}
TAG=lpscl_glass_control_li3ps4_2026_10_05           # 이 카드의 실행 이름 (RUN 기본 폴더) — 살아 있는 잡은 our_running 이 --out_root 로 찾는다
MACHINE=${MACHINE:-kgy}
case "$MACHINE" in
  kgy)   PY=${PY:-/home/kgy/apps/miniforge3/envs/uma/bin/python}; RUN=${RUN:-$HOME/work/runs/$TAG}; START_MAX_MIB=${START_MAX_MIB:-20000}; COEXIST=${COEXIST:-0};;
  gabia) PY=${PY:-/data/apps/miniforge3/envs/uma/bin/python}; RUN=${RUN:-/data/work/runs/$TAG}; START_MAX_MIB=${START_MAX_MIB:-42500}; COEXIST=${COEXIST:-1};;
  *) echo "⛔ MACHINE=$MACHINE — kgy 또는 gabia"; exit 1;;
esac
SEEDS=${SEEDS:-"1 2 3 4 5"}
WAIT_MAX_S=${WAIT_MAX_S:-21600}
EXCEPTION_ID=${EXCEPTION_ID:-D-2026-10-05-gabia-uma-coexist-elastic-li2s-control}
TOTALCAP=${TOTALCAP:-46000}; OURCAP=${OURCAP:-3500}; WARM=${WARM:-300}; HOSTFLOOR=${HOSTFLOOR:-8192}
SAMPLE=${SAMPLE:-2}; KILL_GRACE=${KILL_GRACE:-10}; PMON_S=${PMON_S:-60}; ELW=${ELW:-/data/work/runs/elastic_modelc_2x}
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
# 담금질 python 의 명령줄에 실제로 있는 잡 고유 인자 = "--out_root $RUN" (끝 고정 · python 만). ⛔ 10-05 이전 판은 "$TAG/B" 로 찾았는데
#   그 문자열은 담금질 명령줄에 없고 (--seed_gate 호출에만 있다) — 같은 잡이 돌아도 못 찾았다 (selftest 가 안 봤다).
our_running() { for x in $(pgrep -f -- "--out_root $RUN( |\$)" 2>/dev/null); do case "$(cat /proc/$x/comm 2>/dev/null)" in python*) echo "$x";; esac; done | head -1; }
# ── 공존 가드 (MACHINE=gabia · 값·의미 = glass_main_queue_gabia.sh v2 예외 · 그 러너는 MD 드라이버 전용이라 담금질에 못 쓴다)
tree_pids() { echo "$1"; local c; for c in $(pgrep -P "$1" 2>/dev/null); do tree_pids "$c"; done; }
gpu_tree() { local apps s=0 p v; apps=$(nvidia-smi --query-compute-apps=pid,used_memory --format=csv,noheader,nounits 2>/dev/null)
  for p in $(tree_pids "$1"); do v=$(echo "$apps" | awk -F', *' -v p="$p" '$1==p{s+=$2} END{print s+0}'); s=$((s+v)); done; echo "$s"; }
host_mib() { if [ -n "${FAKE_HOST_MIB:-}" ]; then echo "$FAKE_HOST_MIB"; else awk '/MemAvailable/{printf "%d", $2/1024}' /proc/meminfo; fi; }
kill_tree() { local ps i=0; ps=$(tree_pids "$1"); kill -TERM $ps 2>/dev/null
  while [ "$i" -lt "$KILL_GRACE" ]; do kill -0 "$1" 2>/dev/null || break; sleep 1; i=$((i+1)); done
  kill -KILL $ps 2>/dev/null; return 0; }
EL_F=""; EL_OFF=0
el_latest() { ls -t "$ELW"/*.out 2>/dev/null | head -1; }
el_mark() { EL_F=$(el_latest); EL_OFF=0; [ -n "$EL_F" ] && EL_OFF=$(stat -c %s "$EL_F"); return 0; }
el_gpu_error() { local f; f=$(el_latest); [ -z "$f" ] && return 1
  [ "$f" != "$EL_F" ] && { EL_F=$f; EL_OFF=0; }
  # ⛔ pipefail 이 켜져 있다 — `tail | grep -q` 면 grep 이 먼저 끝날 때 tail 이 SIGPIPE(141)로 죽어 '못 찾음' 으로 읽힌다 → 프로세스 치환
  grep -aqiE "out of memory|ALLOC_FAILED|cudaErrorMemoryAllocation" < <(tail -c +$((EL_OFF + 1)) "$f" 2>/dev/null); }
coexist_can_start() { [ "$(gpu_used)" -le "$START_MAX_MIB" ] && [ "$(host_mib)" -ge $((HOSTFLOOR + 4096)) ]; }
pmon_sample() {       # $1 = 우리 PID → "시각<TAB>우리 sm<TAB>모든 잡 sm 합" (pmon 을 못 읽으면 NA)
  local t out pids; t=$(date '+%F %T')
  out=$(nvidia-smi pmon -c 1 -s u 2>/dev/null) || { printf '%s\tNA\tNA\n' "$t"; return; }
  pids=" $(tree_pids "$1" | tr '\n' ' ') "
  echo "$out" | awk -v pids="$pids" -v t="$t" '!/^#/ && NF>=4 { sm=($4 ~ /^[0-9]+$/) ? $4 : 0; all+=sm; if (index(pids, " "$2" ")) ours+=sm } END { printf "%s\t%d\t%d\n", t, ours+0, all+0 }'
}
run_seed_coexist() {  # $1 = 시드 · $2 = 로그 → 0 = 담금질이 스스로 끝남 (rc 는 QRC) · 6 = 가드 ①–③ · 7 = 가드 ④
  local S=$1 lg=$2 QP t_s now last=0 tot ours host why="" pm="$RUN/logs/seed${1}_pmon.tsv"
  [ -f "$pm" ] || printf 'time\tsm_ours\tsm_all\n' > "$pm"
  el_mark
  if [ -n "${QCMD_OVERRIDE:-}" ]; then bash -c "$QCMD_OVERRIDE" > "$lg" 2>&1 & QP=$!
  else "$PY" tools/ionic/melt_quench_uma.py "${ARGS[@]}" --seed "$S" --out_root "$RUN" > "$lg" 2>&1 & QP=$!; fi
  QPID=$QP; t_s=$(date +%s)
  while kill -0 "$QP" 2>/dev/null; do
    now=$(date +%s); tot=$(gpu_used); ours=$(gpu_tree "$QP"); host=$(host_mib); why=""
    [ "$tot" -gt "$TOTALCAP" ] && why="① GPU 합계 $tot > $TOTALCAP MiB"
    [ -z "$why" ] && [ $((now - t_s)) -ge "$WARM" ] && [ "$ours" -gt "$OURCAP" ] && why="② 우리 담금질 $ours > $OURCAP MiB"
    [ -z "$why" ] && [ "$host" -lt "$HOSTFLOOR" ] && why="③ host $host < $HOSTFLOOR MiB"
    [ -z "$why" ] && el_gpu_error && why="④ 탄성 $(basename "$EL_F") 에 GPU 메모리 오류"
    if [ -n "$why" ]; then
      say "⛔ 가드 $why — 우리 담금질만 죽인다 (PID $QP · 탄성은 안 건드린다) · 예외를 닫는다"
      kill_tree "$QP"; wait "$QP" 2>/dev/null; QRC=137
      case "$why" in ④*) return 7;; *) return 6;; esac
    fi
    if [ $((now - last)) -ge "$PMON_S" ]; then pmon_sample "$QP" >> "$pm"; last=$now; fi
    sleep "$SAMPLE"
  done
  wait "$QP"; QRC=$?; return 0
}
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
  # 중복 가드 — 실제 담금질 호출과 같은 모양의 명령줄로 (python 은 잠만 잔다 · 시험 RUN 은 임시 폴더라 실제 잡과 안 겹친다)
  # 출력은 /dev/null — 안 그러면 남은 sleep 이 호출부 파이프(| tail 등)를 60 초 붙잡는다
  "$PY" -c "import time; time.sleep(60)" tools/ionic/melt_quench_uma.py "${ARGS[@]}" --seed 1 --out_root "$RUN" >/dev/null 2>&1 & P_OK=$!
  "$PY" -c "import time; time.sleep(60)" tools/ionic/melt_quench_uma.py --seed_gate "$RUN/B/seed1" >/dev/null 2>&1 & P_GATE=$!
  "$PY" -c "import time; time.sleep(60)" tools/ionic/melt_quench_uma.py "${ARGS[@]}" --seed 1 --out_root "${RUN}_other" >/dev/null 2>&1 & P_OTHER=$!
  bash -c "sleep 60; :" x tools/ionic/melt_quench_uma.py --out_root "$RUN" >/dev/null 2>&1 & P_SH=$!   # 명령 둘 — 하나면 bash 가 sleep 으로 exec 해서 인자가 사라진다
  sleep 1
  ck "중복 가드: 같은 RUN 의 담금질 python 을 찾는다 (PID 일치)" "[ \"\$(our_running)\" = $P_OK ]"
  kill $P_OK; wait $P_OK 2>/dev/null
  ck "⛔음성 중복 가드: 게이트 호출 · 다른 RUN · python 이 아닌 프로세스는 잡이 아니다" "[ -z \"\$(our_running)\" ]"
  pkill -P $P_SH 2>/dev/null; kill $P_GATE $P_OTHER $P_SH 2>/dev/null; wait $P_GATE $P_OTHER $P_SH 2>/dev/null   # bash 의 자식 sleep 은 부모 PID 로
  RUN=$RUN0
  ck "인자: --system B · --n_fu 15 · 1e12 · turbo (A 와 같은 일정)" "[[ \" ${ARGS[*]} \" == *' --system B --n_fu 15 --quench_rate 1e12 --melt_ps 100 --hold_ps 50 --dt_fs 2 --save_ps 1.0 --turbo '* ]]"
  out=$(dry_one 1 "$T/dry")
  ck "실제 경로 dry_run: B seed1 = $N_ATOMS_EXPECTED 원자 (n_fu 기본 50 = 400 원자를 막는다)" "[[ \"$out\" == *\"$N_ATOMS_EXPECTED 원자\"* ]]"
  ck "⛔음성 n_fu 를 빼면 400 원자 — 이 시험이 그걸 잡는다" "[[ \"\$(\"$PY\" tools/ionic/melt_quench_uma.py --system B --seed 1 --quench_rate 1e12 --out_root $T/dry2 --dry_run 2>&1)\" != *\"$N_ATOMS_EXPECTED 원자\"* ]]"
  # ── 공존 모드 (MACHINE=gabia) — 가짜 nvidia-smi · 가짜 담금질 (잠자는 bash) · 실제 함수 그대로 · 음성 포함
  FB=$T/fbin; mkdir -p "$FB" "$T/el" "$T/run2/logs"; echo 30000 > "$T/tot"; : > "$T/apps"
  cat > "$FB/nvidia-smi" <<FAKESMI
#!/bin/bash
live(){ while IFS= read -r l; do p=\${l%%,*}; [ -n "\$p" ] && kill -0 "\$p" 2>/dev/null && echo "\$l"; done < "$T/apps"; }
case "\$*" in
  *query-gpu=memory.used*) echo \$(( \$(cat "$T/tot") + \$(live | awk -F', *' '{s+=\$2} END{print s+0}') ));;
  *query-compute-apps*) live | awk -F', *' '{print \$1", "\$2}';;
  *pmon*) [ -e "$T/pmon_fail" ] && exit 1
          echo "# gpu         pid  type    sm   mem   enc   dec   command"; echo "# Idx           #   C/G     %     %     %     %   name"
          echo "    0      999999     C    90    40     -     -   pw.x"; live | awk -F', *' '{printf "    0 %s C %s 1 - - python\n", \$1, \$3}';;
esac
FAKESMI
  chmod +x "$FB/nvidia-smi"
  qs(){ echo "echo \$\$, ${2:-1500}, 7 >> $T/apps; sleep $1"; }       # 가짜 담금질: 자기 PID·VRAM·sm 을 가짜 표에 적고 잔다
  co(){ : > "$T/apps"; ( PATH="$FB:$PATH"; RUN=$T/run2; ELW=$T/el; SAMPLE=0.2; PMON_S=0; KILL_GRACE=2; WARM=300; OURCAP=3500
        TOTALCAP=46000; HOSTFLOOR=8192; FAKE_HOST_MIB=50000; eval "$1"; run_seed_coexist 9 "$T/run2/logs/co.log"; r=$?; echo "$QPID" > "$T/qpid"; exit $r ); }
  dead(){ sleep 0.3; ! kill -0 "$(cat "$T/qpid")" 2>/dev/null; }
  echo "old: CUDA error: out of memory" > "$T/el/strain_x.out"           # 우리 시작 **전** 오류 — ④ 가 잡으면 안 된다
  QCMD_OVERRIDE=$(qs 1.5); co ""; r=$?
  ck "공존 ⓪ 정상: 가드가 안 걸리면 담금질이 스스로 끝난다 (반환 0)" "[ $r = 0 ]"
  ck "공존 ⓪ 점유 표본: 우리 sm 7 · 합 97 이 pmon 장부에 찍힌다" "awk -F'\t' 'NR>1 && \$2==7 && \$3==97{f=1} END{exit !f}' $T/run2/logs/seed9_pmon.tsv"
  ck "⛔음성 공존 ④: 우리 시작 전에 있던 탄성 오류 줄은 잡지 않는다 (위 ⓪ 이 0)" "[ $r = 0 ]"
  echo 47000 > "$T/tot"; QCMD_OVERRIDE=$(qs 20); co ""; r=$?
  ck "⛔ 공존 ① GPU 합계 > 46000 → 우리 담금질만 죽이고 6" "[ $r = 6 ] && dead"; echo 30000 > "$T/tot"
  QCMD_OVERRIDE=$(qs 20 4000); co "WARM=0"; r=$?
  ck "⛔ 공존 ② 우리 > 3500 MiB (WARM 뒤) → 6" "[ $r = 6 ] && dead"
  QCMD_OVERRIDE=$(qs 1 4000); co ""; r=$?
  ck "⛔음성 공존 ②: WARM 300 s 전에는 우리 VRAM 으로 죽이지 않는다 (0)" "[ $r = 0 ]"
  QCMD_OVERRIDE=$(qs 20); co "FAKE_HOST_MIB=4000"; r=$?
  ck "⛔ 공존 ③ host < 8192 MiB → 6" "[ $r = 6 ] && dead"
  QCMD_OVERRIDE="echo \$\$, 1500, 7 >> $T/apps; sleep 0.5; { echo 'CUDA error: out of memory'; head -c 2000000 /dev/zero | tr '\\0' x; } >> $T/el/strain_x.out; sleep 20"
  co ""; r=$?
  ck "⛔ 공존 ④ 시작 뒤 탄성 *.out 에 GPU 메모리 오류 (뒤에 2 MB 더 · pipefail SIGPIPE 함정) → 7" "[ $r = 7 ] && dead"
  ck "공존 시작 조건: 합계 40000 · host 50000 → 시작" "( echo 40000 > $T/tot; PATH=$FB:\$PATH; START_MAX_MIB=42500; FAKE_HOST_MIB=50000; coexist_can_start )"
  ck "⛔음성 공존 시작 조건: 합계 43000 > 42500 → 기다린다" "! ( echo 43000 > $T/tot; PATH=$FB:\$PATH; START_MAX_MIB=42500; FAKE_HOST_MIB=50000; coexist_can_start )"
  ck "⛔음성 공존 시작 조건: host 10000 < 8192 + 4096 → 기다린다" "! ( echo 30000 > $T/tot; PATH=$FB:\$PATH; START_MAX_MIB=42500; FAKE_HOST_MIB=10000; coexist_can_start )"
  touch "$T/pmon_fail"
  ck "⛔음성 pmon 을 못 읽으면 NA (0 으로 적지 않는다)" "( PATH=$FB:\$PATH; pmon_sample \$\$ ) | grep -q 'NA	NA'"
  rm -f "$T/pmon_fail"
  out=$(SELFTEST=0 DRY_RUN=1 MACHINE=gabia PY="$PY" RUN=$T/run3 EXCEPTION_ID=$DECISION ELW=$T/none bash "${BASH_SOURCE[0]}" 2>&1); r=$?
  ck "⛔ 공존: 탄성 작업방에 *.out 이 없으면 시작하지 않는다 (가드 ④ 무력 방지 · 실제 경로)" "[ $r = 1 ] && [[ \"\$out\" == *'말없이 무력'* ]]"
  out=$(SELFTEST=0 DRY_RUN=1 MACHINE=gabia PY="$PY" RUN=$T/run3 EXCEPTION_ID=D-0000-00-00-nope ELW=$T/el bash "${BASH_SOURCE[0]}" 2>&1); r=$?
  ck "⛔ 공존: 공존 결정이 active 가 아니면 시작하지 않는다 (실제 경로)" "[ $r = 1 ] && [[ \"\$out\" == *'공존 결정'* ]]"
  [ -n "$T" ] && [ -d "$T/fbin" ] && pkill -f -- "$T/apps" 2>/dev/null
  rm -rf "$T"
  echo "selftest $([ $fails = 0 ] && echo PASS || echo FAIL) ($fails 실패)"; [ $fails = 0 ]; exit $?
fi

[ -f "$CARD" ] || { echo "⛔ 카드가 이 worktree 에 없다 ($CARD)"; exit 1; }
"$PY" -c "import ase, numpy" 2>/dev/null || { echo "⛔ PY=$PY 에 ase/numpy 없음"; exit 1; }
decision_active "$DECISION" || { echo "⛔ 결정 $DECISION 이 원장에서 active 가 아니다 — 시작하지 않는다"; exit 1; }
if [ "$COEXIST" = 1 ]; then
  decision_active "$EXCEPTION_ID" || { echo "⛔ 공존 결정 $EXCEPTION_ID 이 원장에서 active 가 아니다 — 탄성 GPU pw.x 옆 UMA 는 active 결정만 (시작하지 않는다)"; exit 1; }
  [ -n "$(el_latest)" ] || { echo "⛔ ELW=$ELW 에 *.out 이 없다 — 가드 ④ 가 말없이 무력해진다 (탄성 작업방을 맞게 준다 · 시작하지 않는다)"; exit 1; }
fi

if [ "${DRY_RUN:-0}" = 1 ]; then
  T=$(mktemp -d); echo "DRY_RUN · 기계 $MACHINE · 공존 $COEXIST · worktree $(git rev-parse --short=9 HEAD 2>/dev/null) · RUN $RUN · 시드 $SEEDS"
  for S in $SEEDS; do echo "  seed$S · 상태 $(seed_state $S) · $(dry_one $S "$T" | head -1)"; done
  echo "  GPU 사용 $(gpu_used) MiB (시작 문턱 ≤ $START_MAX_MIB) · 우리 잡 $(our_running || true)"
  if [ "$COEXIST" = 1 ]; then
    f=$(el_latest); echo "  공존 결정 $EXCEPTION_ID — active · 탄성 최신 $(basename "$f") ($(stat -c %s "$f") B · $(date -r "$f" '+%F %T'))"
    echo "  host $(host_mib) MiB (시작 ≥ $((HOSTFLOOR + 4096))) · 지금 시작 $(coexist_can_start && echo 가능 || echo '대기 (조건 미달)') · 가드 ① $TOTALCAP · ② $OURCAP (WARM $WARM s) · ③ $HOSTFLOOR · ④ $ELW"
    echo "  pmon 표본 (시각 · 우리 · 합): $(pmon_sample $$ | tr '\t' ' ')"
  fi
  rm -rf "$T"; exit 0
fi

"$PY" -c "import fairchem" 2>/dev/null || { echo "⛔ PY=$PY 에 fairchem 없음 (uma env 절대경로인지 본다)"; exit 1; }
[ -z "$(our_running)" ] || { echo "⛔ 같은 잡이 이미 돈다 (PID $(our_running)) — 두 번 띄우지 않는다"; exit 1; }
mkdir -p "$RUN/logs"; LOG=$RUN/run_quench_$MACHINE.log; TSV=$RUN/quench_$MACHINE.tsv
exec 9>"$RUN/.lock"; flock -n 9 || { echo "⛔ 이 RUN 에 러너가 이미 돈다 ($RUN/.lock) — 두 번 띄우지 않는다"; exit 1; }
[ -f "$TSV" ] || printf 'seed\tstart\tend\twall_s\trc\n' > "$TSV"
say "START @ $(git rev-parse --short=9 HEAD) · 변경 $(git status --porcelain 2>/dev/null | wc -l) · 기계 $MACHINE · 공존 $COEXIST$( [ "$COEXIST" = 1 ] && echo " ($EXCEPTION_ID · 가드 $TOTALCAP/$OURCAP/$HOSTFLOOR · ELW $ELW)") · RUN $RUN · 시드 $SEEDS · 인자 ${ARGS[*]}"
for S in $SEEDS; do
  st=$(seed_state "$S")
  if [ "$st" = done ]; then say "seed$S — 이미 끝남 (result.json) · 건너뛴다"; continue; fi
  if [ "$st" = partial ]; then say "⛔ seed$S — 결과 없이 폴더만 있다 (중간에 멈춤?) · 멈춘다 — 흔적을 보고 사람이 정한다"; exit 3; fi
  waited=0
  while { [ "$COEXIST" = 1 ] && ! coexist_can_start; } || { [ "$COEXIST" != 1 ] && [ "$(gpu_used)" -gt "$START_MAX_MIB" ]; }; do
    [ $waited -ge $WAIT_MAX_S ] && { say "⛔ 시작 조건 (GPU $(gpu_used) ≤ $START_MAX_MIB$( [ "$COEXIST" = 1 ] && echo " · host $(host_mib) ≥ $((HOSTFLOOR + 4096))")) 이 ${WAIT_MAX_S}s 안 채워졌다 — 멈춘다"; exit 4; }
    [ $((waited % 1800)) = 0 ] && say "시작 조건 대기 — GPU $(gpu_used) MiB (≤ $START_MAX_MIB)$( [ "$COEXIST" = 1 ] && echo " · host $(host_mib) MiB")"
    sleep 60; waited=$((waited+60))
  done
  t0=$(date +%s); say "seed$S 시작 · GPU 사용 $(gpu_used) MiB$( [ "$COEXIST" = 1 ] && echo " · host $(host_mib) MiB · 공존 가드 켬")"
  g=0
  if [ "$COEXIST" = 1 ]; then run_seed_coexist "$S" "$RUN/logs/seed$S.log"; g=$?; rc=$QRC
  else "$PY" tools/ionic/melt_quench_uma.py "${ARGS[@]}" --seed "$S" --out_root "$RUN" > "$RUN/logs/seed$S.log" 2>&1; rc=$?; fi
  t1=$(date +%s); printf '%s\t%s\t%s\t%s\t%s\n' "$S" "$(date -d @$t0 '+%F %T')" "$(date -d @$t1 '+%F %T')" $((t1-t0)) $rc >> "$TSV"
  grep -aE "원자 · 셀|UMA inference mode" "$RUN/logs/seed$S.log" | head -2 | sed 's/^/   /' | tee -a "$LOG"
  if [ "$g" != 0 ]; then say "⛔ seed$S — 공존 가드로 멈춤 (종료 코드 $g · 예외 닫힘) · 뒤 시드를 돌리지 않는다 · 시드 폴더는 흔적으로 남긴다 (다시 도는 것은 사람이 정하는 실행 복구)"; exit "$g"; fi
  if [ $rc != 0 ] || [ ! -e "$RUN/B/seed$S/result.json" ]; then say "⛔ seed$S rc $rc · result.json $( [ -e $RUN/B/seed$S/result.json ] && echo 있음 || echo 없음) — 뒤 시드를 돌리지 않는다"; exit 2; fi
  "$PY" tools/ionic/melt_quench_uma.py --seed_gate "$RUN/B/seed$S" > "$RUN/logs/seed${S}_gate.log" 2>&1
  say "seed$S 끝 · $((t1-t0)) s · 게이트 입력 rc $? (판정은 repo)"
done
say "✅ 끝 — 시드 $SEEDS · 다음: 회수(새 worktree) → repo 에서 시드 게이트 · T₅₀ 스캔 → 600 K 러너"
