#!/usr/bin/env bash
# Hermes/cron helper: deterministic part of the NOON procedure.
set -euo pipefail
REPO="${RA_ROOT:-$(cd "$(dirname "$0")/../../../../.." && pwd)}"
cd "$REPO"
mkdir -p data/logs
ra noon "$@" 2>&1 | tee -a data/logs/noon.log
echo "pending analyses: $(ls data/analysis/pending/*.json 2>/dev/null | wc -l)"
