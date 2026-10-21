#!/bin/bash
cd /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rint2rev_repro/source || exit 9
for cfg in "SkylakeX 4" "Haswell 4" "Sandybridge 1" "Nehalem 1"; do
  set -- $cfg
  log=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rint2rev_repro/_env_codex/cert_table_${1}_t$2.log
  OPENBLAS_CORETYPE=$1 OPENBLAS_NUM_THREADS=$2 OMP_NUM_THREADS=$2 MKL_NUM_THREADS=$2 nice -n 19 timeout 1500 python3 -I -X utf8 -B scripts/step3_conv_cert.py --table > $log 2>&1
  echo "$1 t$2 rc=$? $(grep -o "'interval': ([^)]*)" $log)"
done
