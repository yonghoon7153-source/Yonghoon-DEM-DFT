#!/usr/bin/env bash
# Read-only inventory; no reader, MPI, LMP, preflight or job is executed.
# Optional existing paths only: P1_KIT_DIR, P1_REPO_DIR, P1_WORK_ROOT.
(
set +e
set -u
export LC_ALL=C
matched=0; missing=0; mismatched=0; unknown=0
inspect_file() {
  local path=$1 expected_size=$2 expected_hash=$3 actual_size actual_line actual_hash
  printf '\nFILE %s\n' "$path"
  if [[ ! -f "$path" ]]; then
    printf 'MISSING_OR_NOT_REGULAR\n'; missing=$((missing+1)); return
  fi
  if actual_size=$(stat -L --printf='%s' -- "$path"); then
    printf 'size=%s stat_rc=0\n' "$actual_size"
  else
    printf 'STAT_ERROR rc=%s\n' "$?"; unknown=$((unknown+1)); return
  fi
  if actual_line=$(sha256sum -- "$path"); then
    actual_hash=${actual_line%% *}
    printf 'sha256=%s sha256sum_rc=0\n' "$actual_hash"
  else
    printf 'HASH_ERROR rc=%s\n' "$?"; unknown=$((unknown+1)); return
  fi
  if [[ "$actual_size" == "$expected_size" && "$actual_hash" == "$expected_hash" ]]; then
    printf 'MATCH_HISTORICAL_IDENTITY\n'; matched=$((matched+1))
  else
    printf 'MISMATCH expected_size=%s expected_sha256=%s\n' "$expected_size" "$expected_hash"
    mismatched=$((mismatched+1))
  fi
}
list_dir() {
  printf '\nDIRECTORY %s\n' "$1"
  if [[ -d "$1" ]]; then
    if ls -ld -- "$1" && ls -1A -- "$1"; then :
    else printf 'LIST_ERROR rc=%s\n' "$?"; unknown=$((unknown+1)); fi
  else printf 'MISSING_DIRECTORY\n'; missing=$((missing+1)); fi
}
printf 'INVENTORY_START\n'
if hostname; then :; else printf 'HOST_ERROR rc=%s\n' "$?"; unknown=$((unknown+1)); fi
if id -un; then :; else printf 'USER_ERROR rc=%s\n' "$?"; unknown=$((unknown+1)); fi
if TZ=Asia/Seoul date '+%Y-%m-%d %H:%M:%S %Z'; then :
else printf 'DATE_ERROR rc=%s\n' "$?"; unknown=$((unknown+1)); fi
for tool in python3 mpirun; do
  printf 'COMMAND_PATH %s ' "$tool"
  if command -v "$tool"; then :
  else printf 'UNAVAILABLE\n'; unknown=$((unknown+1)); fi
done
printf 'NP_EXPECTED=6; MPI behavior not tested\n'
inspect_file '/lustre/home/yonghoon/LIGGGHTS-PUBLIC/src/lmp_mpi' '9180024' 'ee2d77261bac9e7fa4e9311c8709e74bf7583a13225a5bc35a791bef9be60a3f'
inspect_file '/home/yonghoon/ps45_unload_hist_20261013/hist_20261014_094731/run_manifest.txt' '531' 'a2501b490899b8b19710847e3295db9d8c11bad9f97a1b4a303dbe1cd0f13fba'
inspect_file '/home/yonghoon/ps45_unload_hist_20261013/hist_20261014_094731/history_verdict.json' '3851' '313158c6696332cf7b7ad60e904e556db9a994bf41fd5bb1fc806f562eb72c55'
inspect_file '/home/yonghoon/ps45_unload_hist_20261013/gram_20261015_030225/run_manifest.txt' '541' '61b2af170303aa9a064e472ced438eeafc79b47064ae6c668fad7593303d3474'
inspect_file '/home/yonghoon/ps45_unload_hist_20261013/gram_20261015_030225/grammar_verdict.json' '1021' 'c19a5aa620bfc58d7593059f5d8c5a51012da7b6774ed2c54902dd7a02efcdbb'
inspect_file '/home/yonghoon/ps45_unload_hist_20261013/kit_20261015_030225/SHA256SUMS' '1344' '8ff722d24096c6bd929682842e3b93907951ad29943f180709c914404cdb928d'
inspect_file '/home/yonghoon/ps45_unload_hist_20261013/kit_20261015_030225/history_params.json' '8427' '7a5279f0119cbbc37a9c212593e256a03e417dc9a6af4f18a4f01bdc72404ff4'
inspect_file '/home/yonghoon/ps45_unload_hist_20261013/kit_20261015_030225/read_history.py' '79327' '70f741a9b8308fe33683de0f22872e2c44ce674dd6223cfce8c00e1a725b696c'
if [[ -x /lustre/home/yonghoon/LIGGGHTS-PUBLIC/src/lmp_mpi ]]; then
  printf 'LMP_EXECUTABLE_BIT=yes (not executed)\n'
else printf 'LMP_EXECUTABLE_BIT=no\n'; unknown=$((unknown+1)); fi
list_dir '/home/yonghoon/ps45_unload_hist_20261013/gram_20261015_030225'
list_dir '/home/yonghoon/ps45_unload_hist_20261013/gram_20261015_030225/P'
list_dir '/home/yonghoon/ps45_unload_hist_20261013/gram_20261015_030225/GA'
list_dir '/home/yonghoon/ps45_unload_hist_20261013/gram_20261015_030225/GB'
work=${P1_WORK_ROOT:-/home/yonghoon/ps45_unload_20261009}
list_dir "$work"
list_dir "$work/ps_7_3_r45/in"
# Check staged paths only; links may refer to the same original file.
inspect_file "$work/ps_7_3_r45/in/restart_compress_3200000.bin" '81154383' '0aa6e41a2330ae7825a715b8d98da6b708c37cb4093d3ab0f8fe2c2653ca3730'
inspect_file "$work/ps_7_3_r45/in/atom_3200000.liggghts" '21430748' '2da106f8470a60c7d3b85894025007d6a5decdffb249b22e0a2ce67d08bbdd9e'
inspect_file "$work/ps_7_3_r45/in/contact_3200000.liggghts" '149687008' '53ae293b4586d091dfca58ab430c174f36b641dcd24678eb10d10fc3f416e65c'
inspect_file "$work/ps_7_3_r45/in/mesh_3200000.stl" '349' 'c25296a6d4d6b185be3c1c0ff98543dbfdb710c281403111c7fae2b9bde2b820'
inspect_file "$work/ps_7_3_r45/in/output_ps_7_3_r45_r8_220537.out" '127049' '35e28690eb9b45c989d7526205a1b168b23041cd1cce6afb12a020deb5096c49'
inspect_file "$work/ps_7_3_r45/in/input_ps_7_3_r45_r8.liggghts" '5916' '097658aa640f798b53da4c40a9d101632b8faaee6f80f4d1d2667591eef8d9cd'
printf '\nPRIOR_RJ_NAMES (bounded to existing bed directory)\n'
shopt -s nullglob
prior=("$work/ps_7_3_r45/"RJ*)
if (( ${#prior[@]} )); then
  for item in "${prior[@]}"; do
    if ls -ld -- "$item"; then :; else printf 'LIST_ERROR rc=%s\n' "$?"; unknown=$((unknown+1)); fi
  done
else printf 'NO_RJ_PREFIX_ENTRIES_OBSERVED\n'; fi
repo=${P1_REPO_DIR:-/home/yonghoon/Yonghoon-DEM-DFT}
if [[ -d "$repo" ]]; then
  printf '\nREPOSITORY_CANDIDATE %s (not kit selection)\n' "$repo"
  if GIT_OPTIONAL_LOCKS=0 GIT_NO_LAZY_FETCH=1 git --no-lazy-fetch -c core.fsmonitor=false -C "$repo" worktree list --porcelain; then :
  else printf 'WORKTREE_QUERY_ERROR rc=%s (no fetch attempted)\n' "$?"; unknown=$((unknown+1)); fi
else printf '\nREPOSITORY_PATH_MISSING_OR_UNKNOWN\n'; unknown=$((unknown+1)); fi
if [[ -n ${P1_KIT_DIR:-} ]]; then
  printf '\nEXPLICIT_KIT %s\n' "$P1_KIT_DIR"
  if manifest_line=$(sha256sum -- "$P1_KIT_DIR/SHA256SUMS"); then
    manifest_hash=${manifest_line%% *}
    printf 'manifest_sha256=%s\n' "$manifest_hash"
    if [[ "$manifest_hash" == 'bb9f305f476815d7448ee5069ceb8fa3b9f138f3be1dc59703fcc8eec09c03bb' ]]; then
      printf 'ACCEPTED_4C_MANIFEST_MATCH; checking listed file bytes only\n'
      if (cd -- "$P1_KIT_DIR" && sha256sum -c -- SHA256SUMS); then
        printf 'KIT_LISTED_BYTES_MATCH (not execution qualification)\n'
      else printf 'KIT_CONTENT_CHECK_ERROR rc=%s\n' "$?"; mismatched=$((mismatched+1)); fi
    else
      printf 'KIT_MANIFEST_MISMATCH; listed paths NOT followed\n'; mismatched=$((mismatched+1))
    fi
  else printf 'KIT_MANIFEST_UNREADABLE rc=%s\n' "$?"; unknown=$((unknown+1)); fi
else printf '\nKIT_UNCONFIRMED: path unknown (not auto-selected)\n'; unknown=$((unknown+1)); fi
printf 'INVENTORY_ONLY: no overall READY/GO, preflight, restoration or simulation verdict\n'
if TZ=Asia/Seoul date '+%Y-%m-%d %H:%M:%S %Z'; then :
else printf 'DATE_ERROR rc=%s\n' "$?"; unknown=$((unknown+1)); fi
printf '\nOBSERVATION_COUNTS match=%s missing=%s mismatch=%s unknown=%s\n' "$matched" "$missing" "$mismatched" "$unknown"
inventory_rc=0
if (( missing + mismatched + unknown > 0 )); then inventory_rc=2; fi
printf 'inventory_rc=%s (inventory only, never READY/GO)\n' "$inventory_rc"
exit "$inventory_rc"
)
