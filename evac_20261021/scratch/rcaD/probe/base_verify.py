"""Check that a scratch base copy (scripts/) is byte-identical to a commit's scripts/ tree (all tracked files)."""
import hashlib
import os
import subprocess
import sys

WT = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-afe53be7bdb176c82'
commit, base = sys.argv[1], sys.argv[2]
ls = subprocess.run(['git', '-C', WT, 'ls-tree', '-r', '--name-only', commit, 'scripts/'], capture_output=True, text=True, check=True)
names = [n for n in ls.stdout.splitlines() if n]
bad, missing = [], []
for n in names:
    blob = subprocess.run(['git', '-C', WT, 'show', f'{commit}:{n}'], capture_output=True, check=True).stdout
    p = os.path.join(base, n)
    if not os.path.exists(p):
        missing.append(n)
        continue
    if hashlib.sha256(open(p, 'rb').read()).hexdigest() != hashlib.sha256(blob).hexdigest():
        bad.append(n)
print(f'{commit}: tracked scripts/ files {len(names)} · missing {len(missing)} · differ {len(bad)}')
for n in (missing + bad)[:20]:
    print('   ', n)
