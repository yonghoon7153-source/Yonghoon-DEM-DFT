#!/usr/bin/env bash
# UNEXECUTED PLAN. User approval for staging + direct preflight is still pending.
# Refuses before any external command or write unless separately approved.
(
if [[ ${P1_STAGE_APPROVAL:-} != 'APPROVE_STAGING_AND_PREFLIGHT_ONLY' ]]; then
  printf 'REFUSED: staging/direct-preflight approval required; no changes made.\n' >&2
  exit 64
fi
set -euo pipefail
trap 'printf "STOPPED: preserve any partial directories; no cleanup/retry or RJ launch.\n" >&2' ERR
repo=/home/yonghoon/Yonghoon-DEM-DFT
new_src=/home/yonghoon/unload_src_4c29705fa1c4
work=/home/yonghoon/ps45_unload_20261009
pin=4c29705fa1c4ba94737a858b206fa4f4c5bb2bde
kit="$new_src/docs/data/ps45_unload_20261009"
py=/home/yonghoon/.conda/envs/myenv/bin/python3
mpi=/home/yonghoon/.conda/envs/myenv/bin/mpirun
lmp=/lustre/home/yonghoon/LIGGGHTS-PUBLIC/src/lmp_mpi
hist=/home/yonghoon/ps45_unload_hist_20261013/hist_20261014_094731/history_verdict.json
gram=/home/yonghoon/ps45_unload_hist_20261013/gram_20261015_030225/grammar_verdict.json
fail() { printf 'STOP: %s\n' "$*" >&2; exit 1; }
absent() { [[ ! -e "$1" && ! -L "$1" ]] || fail "occupied path (including dangling symlink): $1"; }
check_file() {
  local path=$1 expected_size=$2 expected_hash=$3 got_size got_line
  [[ -f "$path" ]] || fail "missing/nonregular: $path"
  got_size=$(stat -L --printf='%s' -- "$path")
  got_line=$(sha256sum -- "$path")
  [[ "$got_size" == "$expected_size" && "${got_line%% *}" == "$expected_hash" ]] || fail "identity mismatch: $path"
  printf 'IDENTITY_MATCH %s\n' "$path"
}
[[ $(hostname -s) == ibb-master && $(id -un) == yonghoon ]] || fail 'expected ibb-master/yonghoon'
[[ -d "$repo" && -x "$py" && -x "$mpi" && -x "$lmp" ]] || fail 'repository or designated commands unavailable'
absent "$new_src"
absent "$work"
# No inherited Git routing, implicit blob fetch or checkout hooks.
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_COMMON_DIR GIT_OBJECT_DIRECTORY GIT_ALTERNATE_OBJECT_DIRECTORIES
export GIT_OPTIONAL_LOCKS=0 GIT_NO_LAZY_FETCH=1
git_repo() { git --no-lazy-fetch -c core.hooksPath=/dev/null -c core.fsmonitor=false -C "$repo" "$@"; }
old_head=$(git_repo rev-parse HEAD)
old_status=$(git_repo status --porcelain=v1 --untracked-files=normal)
# Recheck prerequisite bytes before any planned filesystem creation.
check_file '/lustre/home/yonghoon/LIGGGHTS-PUBLIC/src/lmp_mpi' '9180024' 'ee2d77261bac9e7fa4e9311c8709e74bf7583a13225a5bc35a791bef9be60a3f'
check_file '/home/yonghoon/ps45_unload_hist_20261013/hist_20261014_094731/run_manifest.txt' '531' 'a2501b490899b8b19710847e3295db9d8c11bad9f97a1b4a303dbe1cd0f13fba'
check_file '/home/yonghoon/ps45_unload_hist_20261013/hist_20261014_094731/history_verdict.json' '3851' '313158c6696332cf7b7ad60e904e556db9a994bf41fd5bb1fc806f562eb72c55'
check_file '/home/yonghoon/ps45_unload_hist_20261013/gram_20261015_030225/run_manifest.txt' '541' '61b2af170303aa9a064e472ced438eeafc79b47064ae6c668fad7593303d3474'
check_file '/home/yonghoon/ps45_unload_hist_20261013/gram_20261015_030225/grammar_verdict.json' '1021' 'c19a5aa620bfc58d7593059f5d8c5a51012da7b6774ed2c54902dd7a02efcdbb'
check_file '/home/yonghoon/ps45_unload_hist_20261013/kit_20261015_030225/SHA256SUMS' '1344' '8ff722d24096c6bd929682842e3b93907951ad29943f180709c914404cdb928d'
check_file '/home/yonghoon/ps45_unload_hist_20261013/kit_20261015_030225/history_params.json' '8427' '7a5279f0119cbbc37a9c212593e256a03e417dc9a6af4f18a4f01bdc72404ff4'
check_file '/home/yonghoon/ps45_unload_hist_20261013/kit_20261015_030225/read_history.py' '79327' '70f741a9b8308fe33683de0f22872e2c44ce674dd6223cfce8c00e1a725b696c'
check_file '/home/yonghoon/dem_test/ps45/ps_7_3_r45/restart_ps_7_3_r45/restart_compress_3200000.bin' '81154383' '0aa6e41a2330ae7825a715b8d98da6b708c37cb4093d3ab0f8fe2c2653ca3730'
check_file '/home/yonghoon/dem_test/ps45/ps_7_3_r45/post_ps_7_3_r45/atom_3200000.liggghts' '21430748' '2da106f8470a60c7d3b85894025007d6a5decdffb249b22e0a2ce67d08bbdd9e'
check_file '/home/yonghoon/dem_test/ps45/ps_7_3_r45/post_ps_7_3_r45/contact_3200000.liggghts' '149687008' '53ae293b4586d091dfca58ab430c174f36b641dcd24678eb10d10fc3f416e65c'
check_file '/home/yonghoon/dem_test/ps45/ps_7_3_r45/post_ps_7_3_r45/mesh_3200000.stl' '349' 'c25296a6d4d6b185be3c1c0ff98543dbfdb710c281403111c7fae2b9bde2b820'
check_file '/home/yonghoon/dem_test/ps45/logs/output_ps_7_3_r45_r8_220537.out' '127049' '35e28690eb9b45c989d7526205a1b168b23041cd1cce6afb12a020deb5096c49'
check_file '/home/yonghoon/dem_test/ps45/ps_7_3_r45/input_ps_7_3_r45_r8.liggghts' '5916' '097658aa640f798b53da4c40a9d101632b8faaee6f80f4d1d2667591eef8d9cd'
# This explicit network fetch is part of the future approval scope.
git_repo fetch --no-tags origin refs/heads/codex/unloading-ulpri
[[ $(git_repo rev-parse FETCH_HEAD) == "$pin" ]] || fail 'remote branch tip is not the approved full pin'
# Both roots must remain absent. mkdir without -p claims each exclusively.
absent "$new_src"
absent "$work"
mkdir -- "$new_src"
git_repo worktree add --detach "$new_src" "$pin"
[[ $(git --no-lazy-fetch -C "$new_src" rev-parse HEAD) == "$pin" ]] || fail 'new worktree pin mismatch'
[[ $(git_repo rev-parse HEAD) == "$old_head" ]] || fail 'original checkout HEAD changed'
[[ $(git_repo status --porcelain=v1 --untracked-files=normal) == "$old_status" ]] || fail 'original checkout status changed'
check_file "$kit/SHA256SUMS" 7403 bb9f305f476815d7448ee5069ceb8fa3b9f138f3be1dc59703fcc8eec09c03bb
(cd -- "$kit" && sha256sum -c -- SHA256SUMS)
mkdir -- "$work"
mkdir -- "$work/ps_7_3_r45"
mkdir -- "$work/ps_7_3_r45/in"
copy_checked() {
  local src=$1 name=$2 size=$3 hash=$4 dest="$work/ps_7_3_r45/in/$2"
  check_file "$src" "$size" "$hash"
  absent "$dest"
  cp -n -- "$src" "$dest"
  # cp -n may skip and return success; do not infer copying from its rc alone.
  check_file "$dest" "$size" "$hash"
}
copy_checked '/home/yonghoon/dem_test/ps45/ps_7_3_r45/restart_ps_7_3_r45/restart_compress_3200000.bin' 'restart_compress_3200000.bin' '81154383' '0aa6e41a2330ae7825a715b8d98da6b708c37cb4093d3ab0f8fe2c2653ca3730'
copy_checked '/home/yonghoon/dem_test/ps45/ps_7_3_r45/post_ps_7_3_r45/atom_3200000.liggghts' 'atom_3200000.liggghts' '21430748' '2da106f8470a60c7d3b85894025007d6a5decdffb249b22e0a2ce67d08bbdd9e'
copy_checked '/home/yonghoon/dem_test/ps45/ps_7_3_r45/post_ps_7_3_r45/contact_3200000.liggghts' 'contact_3200000.liggghts' '149687008' '53ae293b4586d091dfca58ab430c174f36b641dcd24678eb10d10fc3f416e65c'
copy_checked '/home/yonghoon/dem_test/ps45/ps_7_3_r45/post_ps_7_3_r45/mesh_3200000.stl' 'mesh_3200000.stl' '349' 'c25296a6d4d6b185be3c1c0ff98543dbfdb710c281403111c7fae2b9bde2b820'
copy_checked '/home/yonghoon/dem_test/ps45/logs/output_ps_7_3_r45_r8_220537.out' 'output_ps_7_3_r45_r8_220537.out' '127049' '35e28690eb9b45c989d7526205a1b168b23041cd1cce6afb12a020deb5096c49'
copy_checked '/home/yonghoon/dem_test/ps45/ps_7_3_r45/input_ps_7_3_r45_r8.liggghts' 'input_ps_7_3_r45_r8.liggghts' '5916' '097658aa640f798b53da4c40a9d101632b8faaee6f80f4d1d2667591eef8d9cd'
# Verify the pinned kit again immediately before running its approved reader logic.
check_file "$kit/SHA256SUMS" 7403 bb9f305f476815d7448ee5069ceb8fa3b9f138f3be1dc59703fcc8eec09c03bb
(cd -- "$kit" && sha256sum -c -- SHA256SUMS)
# Direct entrypoint ONLY. Never invoke the sbatch wrapper, even in an allocation.
env -u BASH_ENV WORK_ROOT="$work" NP=6 LMP="$lmp" PY="$py" MPIRUN="$mpi"   MPIRUN_FLAGS='--oversubscribe --bind-to none' HIST_VERDICT="$hist" GRAMMAR_VERDICT="$gram"   RESUME=0 ALLOW_OTHER_LMP=0 ALLOW_CONCURRENT=0 UL_KIT=0   bash "$kit/run_unload.sh" ps_7_3_r45 RJ --preflight-only
[[ $(git_repo rev-parse HEAD) == "$old_head" ]] || fail 'original checkout HEAD changed'
[[ $(git_repo status --porcelain=v1 --untracked-files=normal) == "$old_status" ]] || fail 'original checkout status changed'
printf 'STAGING_AND_DIRECT_PREFLIGHT_FINISHED; physical RJ NOT_RUN. Stop here.\n'
)
