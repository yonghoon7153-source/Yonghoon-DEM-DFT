#!/bin/bash
# Re-run each committed generator version's own --selftest (with that commit's additives.py) to check the
# pass counts quoted in the commit messages.  usage: bash run_verify_counts.sh
V=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prereview_mixer_d2/verify
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
for d in e432ec015 f1d7d9271 42061a3f1 dd161fd3f cb5a6a445; do
  nice -n 19 python3 -I -B $V/$d/make_mixer_deck.py --selftest > $V/$d/selftest.txt 2>&1
  echo "$d rc=$? $(grep 'selftest:' $V/$d/selftest.txt | tail -1 | cut -c1-200)"
done
