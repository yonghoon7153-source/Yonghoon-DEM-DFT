#!/usr/bin/env bash
# run_kgy.sh — Nd Q3′ SCF launcher on kgy (card nd_q3p_same_cell_card_2026_10_27 · D-2026-10-27-nd-q3p-same-cell proposed,
#   user execution approval 10-27). Copies the repo inputs to R, sets up pseudos (setup_pseudo_kgy.sh), DRY_RUNs the
#   existing point runner (tools/doping/run_force_check_scf.sh: ldd-derived MPI, uniform-settings check, completion =
#   converged + forces (+ stress)), then starts tmux ndq3p: Bader root, then ELF root only if the NC set matched.
#   Beside cascade v7 — the point runner yields (MIN_FREE_MIB) instead of starting when VRAM is short.
# Env: W (worktree, required) · R (/home/kgy/work/runs/nd_q3p_1027 — must match pseudo_dir in the elf inputs) · PWX · MIN_FREE_MIB
# Exit: 0 launched · 2 refused (tmux exists, inputs differ from repo, dry run failed) · 3 PAW mismatch
# Cannot: post-process (Bader / ELF) — that is the next block after the SCFs finish.
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
tmux new -d -s ndq3p "$CMD" || { echo "⛔ tmux 시작 실패"; exit 2; }
echo "▶ tmux ndq3p $(date '+%F %T') · $ROOTS · HEAD $(git -C "$W" rev-parse --short HEAD)"
