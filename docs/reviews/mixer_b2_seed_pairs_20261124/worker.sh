#!/bin/bash
set -eo pipefail
umask 077
source "$HOME/.bashrc" || true
conda activate myenv || exit 3
set -u
exec python3 -I -B -u repeat.py "$@"
