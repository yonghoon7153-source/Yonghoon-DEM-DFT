#!/usr/bin/env bash
# F6: stale autocrlf clone (checked out before .gitattributes existed, 274f1f8^) moved to 1049894 vs fresh clone at 1049894
S="$(cd "$(dirname "$0")" && pwd)"; REPO=/home/user/Yonghoon-DEM-DFT
rm -rf "$S/crlf_stale" "$S/crlf_fresh"
git clone -q --shared --no-checkout "$REPO" "$S/crlf_stale"; git -C "$S/crlf_stale" config core.autocrlf true
git -C "$S/crlf_stale" checkout -q 274f1f8^ && git -C "$S/crlf_stale" checkout -q 1049894
echo "## stale clone (274f1f8^ -> 1049894, autocrlf=true):"; git -C "$S/crlf_stale" ls-files --eol bms-balancing/matlab/tests/run_all.sh bms-balancing/scripts/run_states.sh bms-balancing/.gitattributes
echo "git status --short:"; git -C "$S/crlf_stale" status --short | head -3; echo "(end status)"
echo "bash run_all.sh:"; (cd "$S/crlf_stale/bms-balancing" && timeout 120 bash matlab/tests/run_all.sh 2>&1 | head -4; echo "rc=${PIPESTATUS[0]}")
echo "## after git add --renormalize . && git checkout -- . (fix hint):"; (cd "$S/crlf_stale" && git add --renormalize . && git checkout -- . && git ls-files --eol bms-balancing/matlab/tests/run_all.sh && git status --short | head -2)
echo "## fresh clone at 1049894 with autocrlf=true (R6_REQUEST §0 documented path):"
git clone -q --shared --no-checkout "$REPO" "$S/crlf_fresh"; git -C "$S/crlf_fresh" config core.autocrlf true; git -C "$S/crlf_fresh" checkout -q 1049894
git -C "$S/crlf_fresh" ls-files --eol bms-balancing/matlab/tests/run_all.sh
echo "R6_REQUEST.md:24:"; sed -n 24p "$S/wt/bms-balancing/reviews/R6_REQUEST.md"; grep -c renormalize "$S/wt/bms-balancing/reviews/R6_REQUEST.md" "$S/wt/bms-balancing/README.md"
