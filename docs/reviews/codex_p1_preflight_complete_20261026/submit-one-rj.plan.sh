#!/usr/bin/env bash
# UNEXECUTED physical-RJ submission plan; approval is separate from preflight.
(
if [[ ${P1_RJ_APPROVAL:-} != 'APPROVE_ONE_PS73_RJ_SUBMISSION' ]]; then
  printf 'REFUSED: one physical RJ submission requires explicit approval.\n' >&2
  exit 64
fi
set -euo pipefail
trap 'printf "STOPPED: preserve submission receipt; do not resubmit, retry or delete on uncertainty.\n" >&2' ERR
src=/home/yonghoon/unload_src_4c29705fa1c4
kit="$src/docs/data/ps45_unload_20261009"
work=/home/yonghoon/ps45_unload_20261009
receipt="$work/submission_ps73_RJ_20261026_once"
pin=4c29705fa1c4ba94737a858b206fa4f4c5bb2bde
py=/home/yonghoon/.conda/envs/myenv/bin/python3
mpi=/home/yonghoon/.conda/envs/myenv/bin/mpirun
lmp=/lustre/home/yonghoon/LIGGGHTS-PUBLIC/src/lmp_mpi
hist=/home/yonghoon/ps45_unload_hist_20261013/hist_20261014_094731/history_verdict.json
gram=/home/yonghoon/ps45_unload_hist_20261013/gram_20261015_030225/grammar_verdict.json
fail() { printf 'STOP: %s\n' "$*" >&2; exit 1; }
absent() { [[ ! -e "$1" && ! -L "$1" ]] || fail "occupied path: $1"; }
check_file() {
  local path=$1 size=$2 hash=$3 got_size got_hash
  [[ -f "$path" ]] || fail "missing/nonregular: $path"
  got_size=$(stat -L --printf='%s' -- "$path")
  got_hash=$(sha256sum -- "$path")
  [[ "$got_size" == "$size" && "${got_hash%% *}" == "$hash" ]] || fail "identity mismatch: $path"
}
[[ $(hostname -s) == ibb-master && $(id -un) == yonghoon ]] || fail 'expected ibb-master/yonghoon'
[[ -z ${SLURM_JOB_ID:-} ]] || fail 'submit from login session, not nested allocation'
[[ -d "$work" && -x "$py" && -x "$mpi" && -x "$lmp" ]] || fail 'required setup missing'
command -v sbatch
absent "$receipt"
shopt -s nullglob
for previous in "$work/ps_7_3_r45/"RJ*; do
  absent "$previous" # Any previous RJ-prefixed entry requires manual review.
done
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_COMMON_DIR GIT_OBJECT_DIRECTORY GIT_ALTERNATE_OBJECT_DIRECTORIES
[[ $(GIT_OPTIONAL_LOCKS=0 GIT_NO_LAZY_FETCH=1 git --no-lazy-fetch -C "$src" rev-parse HEAD) == "$pin" ]] || fail 'working checkout pin mismatch'
check_file "$kit/SHA256SUMS" 7403 bb9f305f476815d7448ee5069ceb8fa3b9f138f3be1dc59703fcc8eec09c03bb
(cd -- "$kit" && sha256sum -c -- SHA256SUMS)
check_file '/lustre/home/yonghoon/LIGGGHTS-PUBLIC/src/lmp_mpi' 9180024 'ee2d77261bac9e7fa4e9311c8709e74bf7583a13225a5bc35a791bef9be60a3f'
check_file '/home/yonghoon/ps45_unload_hist_20261013/hist_20261014_094731/run_manifest.txt' 531 'a2501b490899b8b19710847e3295db9d8c11bad9f97a1b4a303dbe1cd0f13fba'
check_file '/home/yonghoon/ps45_unload_hist_20261013/hist_20261014_094731/history_verdict.json' 3851 '313158c6696332cf7b7ad60e904e556db9a994bf41fd5bb1fc806f562eb72c55'
check_file '/home/yonghoon/ps45_unload_hist_20261013/gram_20261015_030225/run_manifest.txt' 541 '61b2af170303aa9a064e472ced438eeafc79b47064ae6c668fad7593303d3474'
check_file '/home/yonghoon/ps45_unload_hist_20261013/gram_20261015_030225/grammar_verdict.json' 1021 'c19a5aa620bfc58d7593059f5d8c5a51012da7b6774ed2c54902dd7a02efcdbb'
check_file '/home/yonghoon/ps45_unload_hist_20261013/kit_20261015_030225/SHA256SUMS' 1344 '8ff722d24096c6bd929682842e3b93907951ad29943f180709c914404cdb928d'
check_file '/home/yonghoon/ps45_unload_hist_20261013/kit_20261015_030225/history_params.json' 8427 '7a5279f0119cbbc37a9c212593e256a03e417dc9a6af4f18a4f01bdc72404ff4'
check_file '/home/yonghoon/ps45_unload_hist_20261013/kit_20261015_030225/read_history.py' 79327 '70f741a9b8308fe33683de0f22872e2c44ce674dd6223cfce8c00e1a725b696c'
check_file "$work/ps_7_3_r45/in/restart_compress_3200000.bin" 81154383 '0aa6e41a2330ae7825a715b8d98da6b708c37cb4093d3ab0f8fe2c2653ca3730'
check_file "$work/ps_7_3_r45/in/atom_3200000.liggghts" 21430748 '2da106f8470a60c7d3b85894025007d6a5decdffb249b22e0a2ce67d08bbdd9e'
check_file "$work/ps_7_3_r45/in/contact_3200000.liggghts" 149687008 '53ae293b4586d091dfca58ab430c174f36b641dcd24678eb10d10fc3f416e65c'
check_file "$work/ps_7_3_r45/in/mesh_3200000.stl" 349 'c25296a6d4d6b185be3c1c0ff98543dbfdb710c281403111c7fae2b9bde2b820'
check_file "$work/ps_7_3_r45/in/output_ps_7_3_r45_r8_220537.out" 127049 '35e28690eb9b45c989d7526205a1b168b23041cd1cce6afb12a020deb5096c49'
check_file "$work/ps_7_3_r45/in/input_ps_7_3_r45_r8.liggghts" 5916 '097658aa640f798b53da4c40a9d101632b8faaee6f80f4d1d2667591eef8d9cd'
# Atomic one-submission marker OUTSIDE the bed/RJ.* prior-attempt namespace.
# No -p: a prior receipt, including an interrupted/uncertain attempt, blocks reuse.
mkdir -- "$receipt"
printf 'pin=%s\nphysical_job=ps_7_3_r45/RJ\nmax_walltime=5-00:00:00\n' "$pin" > "$receipt/context.txt"
TZ=Asia/Seoul date -Iseconds > "$receipt/requested-at.txt"
printf 'SUBMISSION_STARTED; outcome may be uncertain until receipt inspected\n' > "$receipt/state.txt"
# Neutralize inherited scheduler option variables, including job-array settings.
for setting in ${!SBATCH_@}; do unset "$setting"; done
# Exactly one sbatch call. Never bash the wrapper on the login node.
# The sealed wrapper itself sets ALLOW_CONCURRENT=1 inside the allocation.
if env -u BASH_ENV WORK_ROOT="$work" NP=6 LMP="$lmp" PY="$py" MPIRUN="$mpi"     MPIRUN_FLAGS='--oversubscribe --bind-to none' HIST_VERDICT="$hist" GRAMMAR_VERDICT="$gram"     RESUME=0 UL_KIT=0 ALLOW_OTHER_LMP=0 ALLOW_CONCURRENT=0     sbatch --parsable --no-requeue --partition=cpu --qos=cpu-60 --ntasks=6 --time=5-00:00:00     --job-name=p1_ps73_RJ --chdir="$work" --export=ALL     --output="$receipt/slurm-%j.stdout" --error="$receipt/slurm-%j.stderr"     "$kit/run_unload_ibb.sbatch" "$kit" ps_7_3_r45 RJ     > "$receipt/sbatch.stdout" 2> "$receipt/sbatch.stderr"; then
  submit_rc=0
else
  submit_rc=$?
fi
printf '%s\n' "$submit_rc" > "$receipt/sbatch.rc"
cat -- "$receipt/sbatch.stdout" "$receipt/sbatch.stderr"
answer=$(cat -- "$receipt/sbatch.stdout")
if [[ "$submit_rc" != 0 || ! "$answer" =~ ^[1-9][0-9]*(\;[A-Za-z0-9_.-]+)?$ ]]; then
  printf 'SUBMISSION_UNCERTAIN; preserve all files; no automatic retry\n' > "$receipt/state.txt"
  fail 'submission outcome uncertain; do not submit again'
fi
printf '%s\n' "$answer" > "$receipt/job-id.txt"
printf 'SUBMISSION_ACCEPTED_ONLY; execution/completion not established\n' > "$receipt/state.txt"
printf 'Submitted exactly once: %s; receipt=%s. No retry/requeue/downstream submission.\n' "$answer" "$receipt"
)
