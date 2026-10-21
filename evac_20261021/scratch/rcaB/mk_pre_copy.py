"""Make a scratch copy of the worktree (scripts + docs/data needed) where the three fixed modules are the base commit's versions.

usage: python3 mk_pre_copy.py <worktree> <dest> <base commit> <module> [<module> ...]
The test files and every other module stay as in the worktree (so the CURRENT tests run against the PRE-fix modules)."""
import os
import shutil
import subprocess
import sys

wt, dest, base = sys.argv[1], sys.argv[2], sys.argv[3]
mods = sys.argv[4:]
if os.path.exists(dest):
    shutil.rmtree(dest)
os.makedirs(dest)
shutil.copytree(os.path.join(wt, 'scripts'), os.path.join(dest, 'scripts'),
                ignore=shutil.ignore_patterns('__pycache__'))
for sub in ('docs/data',):
    src = os.path.join(wt, sub)
    if os.path.isdir(src):
        shutil.copytree(src, os.path.join(dest, sub), ignore=shutil.ignore_patterns('__pycache__'))
for m in mods:
    blob = subprocess.run(['git', '-C', wt, 'show', f'{base}:scripts/{m}'], capture_output=True, check=True).stdout
    with open(os.path.join(dest, 'scripts', m), 'wb') as fh:
        fh.write(blob)
# the tests' base comparison (git show <commit>:<path>) needs objects only: a fresh repository whose object store borrows the
# worktree's (alternates — read only · no shared index / HEAD / refs)
cd = subprocess.run(['git', '-C', wt, 'rev-parse', '--git-common-dir'], capture_output=True, check=True, text=True).stdout.strip()
if not os.path.isabs(cd):
    cd = os.path.normpath(os.path.join(wt, cd))
subprocess.run(['git', 'init', '-q', dest], check=True)
with open(os.path.join(dest, '.git', 'objects', 'info', 'alternates'), 'w') as fh:
    fh.write(os.path.join(cd, 'objects') + '\n')
print('ok', dest, mods)
