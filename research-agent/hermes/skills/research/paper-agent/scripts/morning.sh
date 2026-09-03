#!/usr/bin/env bash
# Hermes/cron helper: build digest (dry-run) and print it so the agent can polish/deliver it.
set -euo pipefail
REPO="${RA_ROOT:-$(cd "$(dirname "$0")/../../../../.." && pwd)}"
cd "$REPO"
mkdir -p data/logs
ra morning --dry-run 2>&1 | tee -a data/logs/morning.log
DATE=$(TZ=Asia/Seoul date +%F)
echo "=== DIGEST vault/Digests/$DATE.md ==="
cat "vault/Digests/$DATE.md"
