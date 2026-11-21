#!/usr/bin/env bash
set -euo pipefail
umask 077
case $# in
  1) mode=run ;;
  2) [[ $2 = --preflight-only ]] || exit 2; mode=preflight ;;
  *) echo 'Usage: bash run_arm.sh ARM [--preflight-only]' >&2; exit 2 ;;
esac
self=$(cd -- "$(dirname -- "$0")" && pwd -P)
py="$HOME/.conda/envs/myenv/bin/python3"
printf '%s  %s\n' 561c350efec08f1712162c4d649f4b668bacceb68388e973efec964f0073cd92 "$py" | sha256sum --check --status -
exec "$py" -I -B "$self/ps73_node.py" "$mode" "$1"
