# >>> RT prerequisites
rt_prerequisites() {
  case "$JOB" in RJ|RJ2) ;; *) return 0;; esac
  [ -n "${RT_GRAMMAR_VERDICT:-}" ] || die "RT_GRAMMAR_VERDICT missing; no run"
  local out rc hash_line verdict_hash
  out=$("$PY" -I "$KIT/rt_dispatch.py" rt_grammar "$RT_GRAMMAR_VERDICT" --lmp-sha "$LMP_SHA"); rc=$?
  echo "$out"
  [ "$rc" = 0 ] || die "RT fixture provenance/raw reread refused; no run"
  out=$("$PY" -I "$KIT/rt_dispatch.py" orig_grid "$WORK_ROOT" "$BED" "$JOB"); rc=$?
  echo "$out"
  [ "$rc" = 0 ] || die "Original writer grid/deck refused; no run"
  hash_line=$(sha256sum -- "$RT_GRAMMAR_VERDICT") || die "RT verdict hash read failed; no run"
  verdict_hash=${hash_line%% *}
  [[ "$verdict_hash" =~ ^[0-9a-f]{64}$ ]] || die "RT verdict hash format; no run"
  GRAMMAR_REC+=("rt_grammar_prereq=PASS" "rt_grammar_verdict=$RT_GRAMMAR_VERDICT"
               "rt_grammar_verdict_sha256=$verdict_hash"
               "orig_grid_prereq=PASS")
}
# <<< RT prerequisites
