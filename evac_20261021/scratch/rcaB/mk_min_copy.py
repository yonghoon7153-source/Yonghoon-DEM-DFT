"""Minimal scratch copy of the worktree for running the repo tests outside it (disk-light: docs/data = symlink).

usage: python3 mk_min_copy.py <worktree> <dest>
Copies scripts/ (no __pycache__), symlinks docs/data, copies the registration R draft the chain test reads."""
import os
import shutil
import sys

wt, dest = sys.argv[1], sys.argv[2]
if os.path.exists(dest):
    shutil.rmtree(dest)
os.makedirs(os.path.join(dest, 'docs', 'reviews'))
shutil.copytree(os.path.join(wt, 'scripts'), os.path.join(dest, 'scripts'), ignore=shutil.ignore_patterns('__pycache__'))
os.symlink(os.path.join(wt, 'docs', 'data'), os.path.join(dest, 'docs', 'data'))
for rel in ('docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md',):
    shutil.copy2(os.path.join(wt, rel), os.path.join(dest, rel))
print('ok', dest)
