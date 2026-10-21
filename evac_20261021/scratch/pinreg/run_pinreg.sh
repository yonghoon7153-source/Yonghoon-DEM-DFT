#!/bin/bash
# Rint Part B numbers at the review pin 5dc6f7f0b (main tree, clean) — request doc lines "⬜ 메인이 리뷰 핀에서 다시 돌려"
cd /home/user/Yonghoon-DEM-DFT || exit 9
D=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/pinreg
echo "HEAD $(git rev-parse --short HEAD) dirty=$(git status --porcelain | wc -l)"
run() { local name="$1"; shift; local t0=$(date +%s); timeout 3600 "$@" > $D/$name.log 2>&1; local rc=$?; echo "$name rc=$rc t=$(( $(date +%s)-t0 ))s :: $(tail -n 2 $D/$name.log | tr '\n' ' ' | cut -c1-200)"; }
run join python3 -B scripts/test_rint_g2_join.py
run join138 python3 -B $D/fake/scripts/test_join_138.py
run am_iface python3 -B scripts/test_rint_g2_am_iface.py
run rrm python3 -B scripts/test_rint_g2_rrm.py
run t4census python3 -B scripts/test_rint_t4_census.py
run t43 python3 -B scripts/test_rint_t43_order.py
run t2dev python3 -B scripts/test_rint_t2_dev.py
run t41 python3 -B scripts/rint_t41_census.py --selftest
echo DONE
