#!/usr/bin/env bash
# After the agent fills data/analysis/pending/*.json → import, rebuild vault, export litdb, commit.
set -euo pipefail
REPO="${RA_ROOT:-$(cd "$(dirname "$0")/../../../../.." && pwd)}"
cd "$REPO"
ra analyze --import-dir data/analysis/pending
ra vault && ra litdb
git add -A data vault && git commit -q -m "ra: analyses $(TZ=Asia/Seoul date +%F)" || true
ra status
