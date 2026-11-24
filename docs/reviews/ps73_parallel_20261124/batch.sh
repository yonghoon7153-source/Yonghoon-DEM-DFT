#!/bin/bash
set -euo pipefail
umask 077
root=$1
arm=$2
segment=$3
manifest=$4
[[ $# -eq 4 && "$manifest" =~ ^[a-f0-9]{64}$ ]]
case "$arm" in UB|UT|UC|UVa) ;; *) exit 2;; esac
unset BASH_ENV ENV PYTHONHOME PYTHONPATH
[[ "$(pwd -P)" == "$segment" ]]
( cd "$root" && printf '%s  SOURCE_SHA256SUMS\n' "$manifest" | sha256sum -c --status - && sha256sum -c --status SOURCE_SHA256SUMS )
py="$HOME/.conda/envs/myenv/bin/python3"
printf '%s  %s\n' 561c350efec08f1712162c4d649f4b668bacceb68388e973efec964f0073cd92 "$py" | sha256sum -c --status -
exec "$py" -I -B "$root/site_ops.py" WORKER "$arm" "$segment"
