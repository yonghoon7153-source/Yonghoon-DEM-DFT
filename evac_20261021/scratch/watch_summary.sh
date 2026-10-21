#!/usr/bin/env bash
# Emit each new line of the heavy-regression summary; exit when DONE appears.
F=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/heavy/summary.txt
seen=0
while true; do
  if [ -f "$F" ]; then
    total=$(wc -l < "$F")
    if [ "$total" -gt "$seen" ]; then
      sed -n "$((seen + 1)),${total}p" "$F"
      seen=$total
    fi
    if grep -q '^DONE' "$F"; then
      exit 0
    fi
  fi
  sleep 15
done
