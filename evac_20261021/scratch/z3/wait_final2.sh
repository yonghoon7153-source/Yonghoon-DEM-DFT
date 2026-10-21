#!/bin/bash
# wait until the second final regression batch writes its done marker
Z3=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/z3
until [ -e "$Z3/final2.done" ]; do sleep 5; done
echo ready
