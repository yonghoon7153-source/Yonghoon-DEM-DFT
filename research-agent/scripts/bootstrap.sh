#!/usr/bin/env bash
# 최초 설치 + bootstrap 데이터로 파이프라인 검증 (LLM/메일 없이 동작)
set -euo pipefail
cd "$(dirname "$0")/.."
pip install -e ".[dev]" -q
python -m pytest -q
ra status
[ -f data/inbox/manual/done/bootstrap_2026-09-03.json ] || ra ingest --json data/inbox/manual/done/bootstrap_2026-09-03.json 2>/dev/null || true
ra triage --no-enrich
ra analyze --import-dir data/analysis/results
ra vault && ra litdb
ra morning --dry-run
echo "OK — open vault/ in Obsidian (00_MOC/Research Agent Home.md)"
