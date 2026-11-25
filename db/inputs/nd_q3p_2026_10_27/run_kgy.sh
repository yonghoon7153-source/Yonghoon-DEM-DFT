#!/usr/bin/env bash
# run_kgy.sh — Nd Q3′ SCF launcher on kgy (card nd_q3p_same_cell_card_2026_10_27 · D-2026-10-27-nd-q3p-same-cell proposed,
#   user execution approval 10-27). Copies the repo inputs to R, sets up pseudos (setup_pseudo_kgy.sh), DRY_RUNs the
#   existing point runner (tools/doping/run_force_check_scf.sh: ldd-derived MPI, uniform-settings check, completion =
#   converged + forces (+ stress)), then starts tmux ndq3p: Bader root, then ELF root only if the NC set matched.
#   Beside cascade v7 — the point runner yields (MIN_FREE_MIB) instead of starting when VRAM is short.
# Env: W (worktree, required) · R (/home/kgy/work/runs/nd_q3p_1027 — must match pseudo_dir in the elf inputs) · PWX · MIN_FREE_MIB
#   START_AFTER_FILE · START_AFTER_TMUX (10-30): checks and DRY_RUN now, SCFs only after that file exists OR that tmux
#   session is gone (poll START_POLL_S 300 · give up after START_WAIT_S 7 d → exit 4 in start_wait.log, nothing started).
#   Why: the 3090 cannot hold two large pw.x (CEI MnP2O6 13.8 GB + this ≈ 10 GB) and the MIN_FREE_MIB check only sees
#   the moment it starts — a neighbour that grows later still dies (run_sei_dft.sh says the same).
# Exit: 0 launched · 2 refused (tmux exists, inputs differ from repo, dry run failed) · 3 PAW mismatch
# Cannot: post-process (Bader / ELF) — that is the next block after the SCFs finish. Cannot see a neighbour's future
#   VRAM growth — the start condition is the guard for that, not MIN_FREE_MIB.
set -u
W=${W:?W (worktree) is required}; R=${R:-/home/kgy/work/runs/nd_q3p_1027}
PWX=${PWX:-/home/kgy/apps/qe-7.4.1-gpu/bin/pw.x}; MINF=${MIN_FREE_MIB:-16000}
D=$W/db/inputs/nd_q3p_2026_10_27; FC=$W/tools/doping/run_force_check_scf.sh
tmux has-session -t ndq3p 2>/dev/null && { echo "⛔ tmux ndq3p 가 이미 있다 — 중복 실행하지 않는다"; exit 2; }
[ "$R" = /home/kgy/work/runs/nd_q3p_1027 ] || echo "⚠ R=$R — elf 입력의 pseudo_dir 는 /home/kgy/work/runs/nd_q3p_1027/pseudo_nc 다"
mkdir -p "$R"
for k in bader elf; do [ -d "$R/$k" ] || cp -r "$D/$k" "$R/"; done
for f in bader/MP_07 bader/MLi_04 elf/MP_07 elf/MLi_04; do
  cmp -s "$D/$f/scf.in" "$R/$f/scf.in" || { echo "⛔ $R/$f/scf.in 이 저장소 판과 다르다 — 옛 입력이 남았다. 시작하지 않는다"; exit 2; }
done
W=$W NC_DIR=$R/pseudo_nc bash "$D/setup_pseudo_kgy.sh"; prc=$?
[ "$prc" = 3 ] && exit 3
ROOTS=bader; [ -f "$R/pseudo_nc/.md5_ok" ] && ROOTS="bader elf"
for k in $ROOTS; do
  DRY_RUN=1 PWX=$PWX bash "$FC" "$R/$k" > "$R/dry_$k.log" 2>&1; rc=$?
  tail -4 "$R/dry_$k.log" | cut -c1-150
  [ "$rc" = 0 ] || { echo "⛔ $k DRY_RUN 끝 코드 $rc — 시작하지 않는다 ($R/dry_$k.log)"; exit 2; }
done
nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader 2>/dev/null
CMD="PWX=$PWX MIN_FREE_MIB=$MINF bash $FC $R/bader > $R/bader_run.log 2>&1"
[ "$ROOTS" = "bader elf" ] && CMD="$CMD; PWX=$PWX MIN_FREE_MIB=$MINF bash $FC $R/elf > $R/elf_run.log 2>&1"
SAF=${START_AFTER_FILE:-}; SAT=${START_AFTER_TMUX:-}; SWS=${START_WAIT_S:-604800}; SPS=${START_POLL_S:-300}; WAITMSG=""
if [ -n "$SAF$SAT" ]; then
  cat > "$R/start_wait.sh" <<EOF
#!/usr/bin/env bash
# run_kgy.sh 가 만든 시작 대기 (계산 설정은 안 바꾼다) — 파일 '${SAF}' 이 생기거나 tmux '${SAT}' 가 끝나면 0
w=0; echo "[\$(date '+%F %T')] ⏳ 시작 조건 기다림 — 파일 ${SAF:-없음} · tmux ${SAT:-없음} 끝 (최대 ${SWS}s)"
while :; do
  if [ -n "${SAF}" ] && [ -e "${SAF}" ]; then echo "[\$(date '+%F %T')] ▶ 파일이 생겼다 — 시작"; exit 0; fi
  if [ -n "${SAT}" ] && ! tmux has-session -t "${SAT}" 2>/dev/null; then echo "[\$(date '+%F %T')] ▶ tmux ${SAT} 끝 — 시작"; exit 0; fi
  [ \$w -ge ${SWS} ] && { echo "[\$(date '+%F %T')] ⛔ ${SWS}s 안에 조건이 안 됐다 — 시작하지 않는다"; exit 4; }
  sleep ${SPS}; w=\$((w + ${SPS}))
done
EOF
  CMD="bash $R/start_wait.sh > $R/start_wait.log 2>&1 && { $CMD; }"
  WAITMSG=" · 시작 조건 대기 ($R/start_wait.log)"
fi
tmux new -d -s ndq3p "$CMD" || { echo "⛔ tmux 시작 실패"; exit 2; }
echo "▶ tmux ndq3p $(date '+%F %T') · $ROOTS · HEAD $(git -C "$W" rev-parse --short HEAD)$WAITMSG"
