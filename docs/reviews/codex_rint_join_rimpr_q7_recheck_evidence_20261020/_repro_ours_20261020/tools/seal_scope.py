"""Seal-32 scope check from git name lists (read-only).

Usage: python3 -I seal_scope.py <worktree> <changed_between_pins.txt> <files_3b9d51789.txt> <files_2b9efa253.txt>
CODE_FILES = scripts/run_network_194_parallel.py constant (at the worktree = review-pin code);
NUMERIC_MODULES = scripts/seal_s3_prerun.py constant.
"""
import ast
import sys
import os

wt = sys.argv[1]


def const(rel, name):
    tree = ast.parse(open(os.path.join(wt, rel), encoding='utf-8').read())
    for n in tree.body:
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in n.targets):
            return list(ast.literal_eval(n.value))
    raise KeyError(name)


seal = const('scripts/run_network_194_parallel.py', 'CODE_FILES')
s3 = const('scripts/seal_s3_prerun.py', 'NUMERIC_MODULES')
read = lambda p: [l.strip() for l in open(p, encoding='utf-8') if l.strip()]
between, c1, c2 = (set(read(p)) for p in sys.argv[2:5])
print('CODE_FILES', len(seal), '| NUMERIC_MODULES', len(s3))
print('3b9d51789 files', sorted(c1))
print('2b9efa253 files', sorted(c2))
print('seal touched by 3b9d51789:', sorted(set(seal) & c1))
print('seal touched by 2b9efa253:', sorted(set(seal) & c2))
print('seal changed dcb97f1ed -> 2b9efa253:', sorted(set(seal) & between))
print('S3 numeric changed dcb97f1ed -> 2b9efa253:', sorted(set(s3) & between))
print('step3_sigma.py in seal?', 'scripts/step3_sigma.py' in seal)
