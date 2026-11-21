#!/bin/bash
set -euo pipefail
umask 077
[[ $# == 2 && "$2" =~ ^[0-9a-f]{64}$ && ${SLURM_JOB_ID:-} =~ ^[1-9][0-9]*$ && ${SLURM_NTASKS:-} == 6 ]]
[[ -z ${SLURM_ARRAY_JOB_ID:-} && ${SLURM_JOB_NUM_NODES:-} == 1 && ${SLURM_CPUS_PER_TASK:-1} == 1 ]]
case "$1" in UB|UT|UC|UVa|UVb|UTc) ;; *) exit 2 ;; esac
ops="$HOME/ps73_dev_ops_20261121"
[[ ! -L "$ops" && ! -L "$ops/state" && ! -L "$ops/state/jobs" && ! -L "$ops/state/jobs/$1" ]]
[[ "$(pwd -P)" == "$(cd "$ops" && pwd -P)/state/jobs/$1" ]]
( cd "$ops" && printf '%s  SOURCE_SHA256SUMS\n' "$2" | sha256sum -c --status - && sha256sum -c --status SOURCE_SHA256SUMS )
unset BASH_ENV ENV PYTHONPATH PYTHONHOME
exec /bin/bash "$ops/run_arm.sh" "$1"
