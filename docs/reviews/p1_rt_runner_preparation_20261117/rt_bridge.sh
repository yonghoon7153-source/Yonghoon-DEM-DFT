# >>> RT bridge
# Uses the original run_deck/note functions and its exact NP/LMP/EXTRA_VARS.
# The parent candidate remains closed until the rev5 reader is integrated.
rt_bridge_fail() {
  note "rt_binding_error=$1"
  FAILS=$((FAILS + 1)); PRE_OK=0
}
rt_pair_after_un() {
  local line first second
  if [ "$PRE_OK" != 1 ]; then
    note 'stage=RT1 skipped (preceding stage failure)'
    note 'stage=RT2 skipped (preceding stage failure)'
    return 0
  fi
  if ! run_deck "$JD/RT1" RT1 "$CKPT0" - 0; then
    PRE_OK=0; note 'stage=RT2 skipped (RT1 technical failure)'; return 0
  fi
  if [ "$(grep -c '^UL_RT_DONE bed=' "$JD/RT1/screen.txt")" != 1 ]; then
    rt_bridge_fail RT1_marker; note 'stage=RT2 skipped (RT1 marker missing or duplicated)'; return 0
  fi
  if [ ! -s "$JD/RT1/rt.bin" ]; then
    rt_bridge_fail RT1_binary_missing; note 'stage=RT2 skipped (RT1 binary missing)'; return 0
  fi
  if ! line=$(sha256sum -- "$JD/RT1/rt.bin"); then
    rt_bridge_fail RT1_hash_read; note 'stage=RT2 skipped (RT1 hash read failure)'; return 0
  fi
  first=${line%% *}
  if [[ ! "$first" =~ ^[0-9a-f]{64}$ ]]; then
    rt_bridge_fail RT1_hash_format; note 'stage=RT2 skipped (RT1 hash format)'; return 0
  fi
  note "rt1_bin=$JD/RT1/rt.bin sha256=$first"
  if ! line=$(sha256sum -- "$JD/RT1/rt.bin"); then
    rt_bridge_fail RT2_hash_read; note 'stage=RT2 skipped (RT2 hash read failure)'; return 0
  fi
  second=${line%% *}
  if [[ ! "$second" =~ ^[0-9a-f]{64}$ ]]; then
    rt_bridge_fail RT2_hash_format; note 'stage=RT2 skipped (RT2 hash format)'; return 0
  fi
  note "rt2_ckpt=$JD/RT1/rt.bin sha256=$second"
  if [ "$first" != "$second" ]; then
    rt_bridge_fail RT_hash_changed; note 'stage=RT2 skipped (RT binary changed)'; return 0
  fi
  if ! run_deck "$JD/RT2" RT2 "$JD/RT1/rt.bin" - 0; then PRE_OK=0; return 0; fi
  if [ "$(grep -c '^UL_RT_DONE bed=' "$JD/RT2/screen.txt")" != 1 ]; then rt_bridge_fail RT2_marker; fi
}
# <<< RT bridge
