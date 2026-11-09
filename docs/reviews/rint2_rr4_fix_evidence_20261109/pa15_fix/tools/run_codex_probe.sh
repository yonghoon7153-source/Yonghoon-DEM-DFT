#!/usr/bin/env bash
# Codex 회차 ④ 재개 탐침 무변경 재실행 — 쓰임: bash run_codex_probe.sh <탐침 풂 폴더 (그 아래 resume_attack/probe_resume_independent.py · sha256 83622e5a…)> <코드 트리> <TMPDIR>
# 탐침 파일은 리포에 넣지 않는다 (회차 ④ 반입 규칙 그대로 · 받은 ZIP 안 이름 · sha256 만)
set -u
P=${1:?탐침 풂 폴더}
export RINT_REVIEW_REPO=${2:?코드 트리}
export TMPDIR=${3:?TMPDIR}
cd "$P" || exit 9
sha256sum resume_attack/probe_resume_independent.py
sha256sum "$RINT_REVIEW_REPO/scripts/rint_r_chain.py"
python3 -I -X utf8 -B resume_attack/probe_resume_independent.py
echo "rc=$?"
