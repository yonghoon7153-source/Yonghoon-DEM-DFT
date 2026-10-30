#!/bin/bash
# run_envs.sh <tag> <env,env,...> [extra args to test_resume_ckpt.py ...] — run_one.sh for each env in turn
W=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/f01r2
T=$1; ENVS=$2; shift 2
for e in ${ENVS//,/ }; do
  bash "$W/run_one.sh" "$T" "$e" "$@"
done
echo DONE
