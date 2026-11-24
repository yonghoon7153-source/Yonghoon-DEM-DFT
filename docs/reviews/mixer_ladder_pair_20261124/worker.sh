#!/usr/bin/env bash
set -eo pipefail
umask 077
if [ "$1" = GO_MIXER_LADDER_020_050_ONCE ]; then
  trap 'rc=$?; printf "%s\n" "$rc" >dispatch.rc.tmp; mv -- dispatch.rc.tmp dispatch.rc' EXIT
fi
source "$HOME/.bashrc" || true
conda activate myenv || exit 3
set -u
python3 -I -B -u ladder.py "$@"
