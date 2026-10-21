#!/usr/bin/env python3
"""Compare a scripts/ copy with blobs at given commits (sha256 prefix per file)."""
import hashlib
import os
import subprocess
import sys

WT = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1a2386b8dc655b22'
copy = sys.argv[1]
revs = sys.argv[2].split(',')
files = sys.argv[3].split(',')


def h(b):
    return hashlib.sha256(b).hexdigest()[:12]


for f in files:
    p = os.path.join(copy, f)
    row = [f, 'copy=' + (h(open(p, 'rb').read()) if os.path.exists(p) else 'absent')]
    for r in revs:
        try:
            b = subprocess.run(['git', '-C', WT, 'show', f'{r}:scripts/{f}'], capture_output=True, check=True).stdout
            row.append(f'{r}={h(b)}')
        except subprocess.CalledProcessError:
            row.append(f'{r}=absent')
    print(' '.join(row))
