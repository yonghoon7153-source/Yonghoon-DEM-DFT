#!/usr/bin/env python3
"""Run the repo's quotation-ban sweep on the changed files only (same function as check_review_findings --ban-sweep)."""
import os
import sys

ROOT = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-aa282bca507003e72'
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import check_review_findings as C  # noqa: E402

files = [os.path.join(ROOT, p) for p in sys.argv[1:]]
probs, n, nb = C.ban_sweep(ROOT, files=files)
print('files', n, 'bans', nb, 'problems', len(probs))
for p in probs:
    print(p)
sys.exit(1 if probs else 0)
