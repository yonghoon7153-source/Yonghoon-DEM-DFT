#!/bin/bash
set -euo pipefail
[[ $# == 3 && "$3" =~ ^[a-f0-9]{64}$ ]]
code=$1
seg=$2
# An allocation can start before sbatch returns to the coordinator.
for ((i=0; i<120; i++)); do
  [[ -f "$seg/ack.json" ]] && break
  sleep 1
done
[[ -f "$seg/ack.json" ]] || { echo 'MISSING_ACK_AT_START'; exit 2; }
cd -- "$seg"
exec bash "$code/batch.sh" "$code" UVa "$seg" "$3"
