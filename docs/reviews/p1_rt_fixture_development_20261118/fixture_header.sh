#!/bin/bash
set -uo pipefail
die() { echo "STOP: $*" >&2; exit 2; }
say() { printf '%s\n' "$*"; }
[ "$#" = 0 ] && [ -n "$SLURM_JOB_ID" ] && [ "$SLURM_NTASKS" = 6 ] || die "one NP6 allocation required"
NP=6
PY=$(command -v python3) || die "python3"
MPIRUN=$(command -v mpirun) || die "mpirun"
MPIRUN_FLAGS="--oversubscribe --bind-to none"
[ -x "$LMP" ] || die "binary unavailable"
LMP_SHA=$(sha256sum -- "$LMP") || die "binary hash"
LMP_SHA=${LMP_SHA%% *}
[ "$LMP_SHA" = "@LMP_SHA@" ] || die "wrong binary"
SOURCE=$(cd "$(dirname "$0")/kit" && pwd) || die "input kit"
WORK_ROOT="$PWD/work"
mkdir -- "$WORK_ROOT" || die "work directory already exists"
KIT="$WORK_ROOT/kit"
cp -R -- "$SOURCE" "$KIT" || die "kit copy"
(cd "$KIT" && sha256sum -c RT_CANDIDATE_SHA256SUMS) || die "fixture inputs"
RUN="$WORK_ROOT/fixture"
mkdir -- "$RUN" || die "run directory"
h=$(sha256sum "$KIT/RT_CANDIDATE_SHA256SUMS") || die "fixture list"
printf '%s\n' "label=DEVELOPMENT_DATA_ONLY" "mode=rt_grammar" "job_dir=$RUN" "kit=$KIT" "sums_sha256=${h%% *}" "lmp_sha256=$LMP_SHA" "np=$NP" "job_id=$SLURM_JOB_ID" "start=$(date -u +%FT%TZ)" > "$RUN/run_manifest.txt" || die "manifest"
RT_GRAMMAR_ONLY=1
