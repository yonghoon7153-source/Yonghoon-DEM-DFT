"""List the sealed CODE_FILES of run_network_194_parallel.py and whether any touched file is among them.

usage: python3 sealed_check.py <repo root> <touched rel path> ...
"""
import ast
import sys

root = sys.argv[1]
src = open(f'{root}/scripts/run_network_194_parallel.py', encoding='utf-8').read()
files = None
for node in ast.walk(ast.parse(src)):
    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'CODE_FILES' for t in node.targets):
        try:
            files = ast.literal_eval(node.value)
        except ValueError:
            files = None
print('CODE_FILES', len(files) if files else files)
names = {str(f).split('/')[-1] for f in (files or [])}
print('touched ∩ sealed:', [m for m in sys.argv[2:] if m.split('/')[-1] in names])
