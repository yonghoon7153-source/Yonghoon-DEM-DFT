"""Write a unified diff (a/ b/ labels) of selected files between the repo worktree and the scratch full copy.

usage: python3 make_patch.py <repo root> <copy root> <out patch> <rel path> [<rel path> ...]
"""
import difflib
import sys

repo, copy, out = sys.argv[1:4]
chunks = []
for rel in sys.argv[4:]:
    a = open(f'{repo}/{rel}', encoding='utf-8').read().splitlines(keepends=True)
    b = open(f'{copy}/{rel}', encoding='utf-8').read().splitlines(keepends=True)
    chunks.extend(difflib.unified_diff(a, b, fromfile=f'a/{rel}', tofile=f'b/{rel}'))
open(out, 'w', encoding='utf-8').writelines(chunks)
print(out, sum(1 for _ in chunks), 'lines')
