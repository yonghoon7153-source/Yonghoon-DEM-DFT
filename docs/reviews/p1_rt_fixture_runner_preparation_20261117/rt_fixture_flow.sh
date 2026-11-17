# >>> RT fixture flow
if [ "$RT_GRAMMAR_ONLY" = 1 ]; then
  rt_hash() {
    local line
    line=$(sha256sum -- "$1") || return 1
    RT_HASH=${line%% *}
    [[ "$RT_HASH" =~ ^[0-9a-f]{64}$ ]]
  }
  PRC=0; run_stage P in.hist_producer.liggghts "$NP" - || PRC=$?
  FIX="$RUN/P/fixture.bin"
  if [ "$PRC" = 0 ] && [ -s "$FIX" ]; then
    TRC=0; run_stage RT1 in.hist_rt1.liggghts "$NP" "$FIX" || TRC=$?
    EXPECT_MARK=$("$PY" -I -c 'import json,sys;d=json.load(open(sys.argv[1]));print("UL_RT_DONE bed="+d["ul_bed"]+" step="+str(d["ul_s0"]))' "$KIT/rt_fixture_contract.json") || die "RT contract read"
    if [ "$TRC" = 0 ] && [ -s "$RUN/RT1/rt.bin" ] && [ "$(grep -Fxc "$EXPECT_MARK" "$RUN/RT1/screen.out")" = 1 ]; then
      if rt_hash "$RUN/RT1/rt.bin"; then
        FIRST_HASH=$RT_HASH
        echo "rt1_bin=$RUN/RT1/rt.bin sha256=$FIRST_HASH" >> "$RUN/run_manifest.txt" || die "RT1 binding write"
        if rt_hash "$RUN/RT1/rt.bin" && [ "$FIRST_HASH" = "$RT_HASH" ]; then
          echo "rt2_ckpt=$RUN/RT1/rt.bin sha256=$RT_HASH" >> "$RUN/run_manifest.txt" || die "RT2 binding write"
          run_stage RT2 in.hist_rt2.liggghts "$NP" "$RUN/RT1/rt.bin"
        else
          say "RT2 skipped: hash read/change"
        fi
      else
        say "RT2 skipped: RT1 hash read"
      fi
    else
      say "RT2 skipped: RT1 rc/marker/binary"
    fi
  else
    say "RT1/RT2 skipped: P rc/binary"
  fi
  echo "end=$(date -Iseconds)" >> "$RUN/run_manifest.txt" || die "fixture end write"
  # RUN is new; never replace an existing verdict.
  (set -o noclobber; "$PY" -I "$KIT/read_rt_grammar.py" "$RUN" > "$RUN/rt_grammar_verdict.json")
  VRC=$?
  [ -f "$RUN/rt_grammar_verdict.json" ] && cat "$RUN/rt_grammar_verdict.json"
  REP="$RUN.report.tgz"
  [ ! -e "$REP" ] && [ ! -L "$REP" ] || die "report already exists"
  (cd "$WORK_ROOT" && tar -czf "$REP" "$(basename "$RUN")" "$(basename "$KIT")") || die "fixture archive failed"
  sha256sum -- "$REP" || die "fixture archive hash failed"
  say "RT_FIXTURE_READER_RC=$VRC (candidate only; no physical qualification)"
  exit "$VRC"
fi
# <<< RT fixture flow
