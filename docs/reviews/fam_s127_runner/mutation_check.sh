#!/bin/bash
# mutation_check.sh — one deliberate defect per copy of run_s127.sh; the harness must FAIL on each.
set -u
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
SRC=$HERE/run_s127.sh
MD=$HERE/mutants; rm -rf "$MD"; mkdir -p "$MD"
n=0; caught=0; missed=()
mut() {  # name  sed-expression
  local name=$1 expr=$2 f="$MD/run_s127.sh"
  n=$((n + 1))
  sed -e "$expr" "$SRC" > "$f"
  if cmp -s "$SRC" "$f"; then echo "M$n $name: NOT APPLIED"; missed+=("$name (not applied)"); return; fi
  bash "$HERE/test_run_s127.sh" "$f" > "$MD/$name.log" 2>&1
  local rc=$? s; s=$(grep -E '^== SUMMARY' "$MD/$name.log")
  if [ "$rc" -ne 0 ]; then caught=$((caught + 1)); echo "M$n $name: caught · $s · first: $(grep -m1 '^  FAIL' "$MD/$name.log" | sed 's/^  FAIL //')"
  else missed+=("$name"); echo "M$n $name: MISSED · $s"; fi
}
mut amend_missing      's/--platen-mach 0\.0099999/--platen-mach 0.01/'
mut amend_on_confirm   '0,/--platen-mach 0\.01 /s//--platen-mach 0.0099999 /'
mut order_fa_fb        's/^ARMS=(confirm_fb corner_fb corner_fa corner_f0)/ARMS=(confirm_fb corner_fa corner_fb corner_f0)/'
mut f0_no_allow_flag   's/--am-load-frac 0 --allow-unconverged-servo/--am-load-frac 0/'
mut gate_skip_marker   's/  log_has "\$log" "\$MARKER" || why="\${why}no_converged_marker,"/  :/'
mut gate_skip_json     's/  \[ -s "\$json" \] || why="\${why}json_missing,"/  :/'
mut leak_tail_in_end   's/status=\$(status_word "\$log")"/status=$(status_word "$log") $(tail -n 1 "$log")"/'
mut free_le            's/\[ "\$GPU_F" -lt "\$GPU_FREE_MIN" \]/[ "$GPU_F" -le "$GPU_FREE_MIN" ]/'
mut header_deadline_le 's/\[ "\$now" -lt "\$DEADLINE_EPOCH" \] || refuse/[ "$now" -le "$DEADLINE_EPOCH" ] || refuse/'
mut corner_fail_stops  's/^    if \[ "\$kind" = confirm \]; then confirm_gate; fi/    if [ "$kind" = confirm ]; then confirm_gate; elif [ "$ARM_RC" -ne 0 ]; then exit 6; fi/'
mut hb_every_300       's/HB_S=600/HB_S=300/'
mut eta_no_x5          's/^PRINT_EVERY=5 /PRINT_EVERY=1 /'
mut no_kill            's/        kill -KILL "\$pid" 2> \/dev\/null/        :/'
mut no_stop_file_poll  's/    elif \[ -e "\$STOPF" \]; then stop=author/    elif false; then stop=author/'
mut start_line_first   's/^  header$/  say "§12-7 시작 $(now_h)"; header/'
mut py_check_first     's/^  # 1 봉인 표지$/  "$PY" -c "import sys" > \/dev\/null 2>\&1/'
mut skip_md5           's/  \[ "\$got" = "\$CODE_MD5" \] || refuse/  : || refuse/'
mut no_settle_pgrep    's/^  pgrep_clear || skip "\$arm" "\$PG_WHY"/  :/'
echo "== mutants: $n · caught $caught · missed ${#missed[@]} =="
[ "${#missed[@]}" -eq 0 ] || printf '  missed: %s\n' "${missed[@]}"
