#!/bin/bash
# 목표량 증서 탐침 재실행 (93d93bc02) — 두 OpenBLAS 경로 (기본 SkylakeX · Haswell = Codex 경로)
cd "$(dirname "$0")"
export PRE_REPO=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a388f740a6ce4524d
echo "=== probe_cert_codex (default)"; timeout 600 python3 -I probe_cert_codex.py > /dev/null 2>cert_default.err; echo rc=$?
echo "=== probe_cert_codex (Haswell)"; OPENBLAS_CORETYPE=Haswell timeout 600 python3 -I probe_cert_codex.py > /dev/null 2>cert_haswell.err; echo rc=$?
echo "=== probe_limits (default)"; timeout 600 python3 -I probe_limits.py 2>&1 | tail -5; mv -f probe_limits.json probe_limits_default.json
echo "=== probe_limits (Haswell)"; OPENBLAS_CORETYPE=Haswell timeout 600 python3 -I probe_limits.py 2>&1 | tail -5; mv -f probe_limits.json probe_limits_Haswell.json
echo "=== probe_cert_liveness"; timeout 600 python3 -I probe_cert_liveness.py 2>&1 | tail -6
echo "=== probe_b01_mutation"; timeout 600 python3 -I probe_b01_mutation.py 2>&1 | tail -6
echo "=== show_cert"; python3 -I show_cert.py 2>&1 | tail -30
