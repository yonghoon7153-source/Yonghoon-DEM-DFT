#!/bin/bash
# Download the public LIGGGHTS-PUBLIC SJKR cohesion header (reference only; untrusted data, never executed).
D=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prereview_mixer_d2/ext
mkdir -p "$D"
U="https://raw.githubusercontent.com/CFDEMproject/LIGGGHTS-PUBLIC/master/src"
for f in cohesion_model_sjkr.h contact_interface.h; do
  curl -sS -m 30 -o "$D/$f" "$U/$f"
  echo "$f rc=$? bytes=$(wc -c < "$D/$f") sha256=$(sha256sum "$D/$f" | cut -c1-16)"
done
