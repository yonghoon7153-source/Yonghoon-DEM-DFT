"""Check the scratch copies before the regression runs.

b7pre: the three fixed modules = base commit blobs; everything else in scripts/ = worktree (so the current tests run against pre-fix code).
b7fix: scripts/ = worktree except the two fixture files (patched).
usage: python3 verify_copies.py <worktree> <b7pre> <b7fix> <base commit>"""
import filecmp
import os
import subprocess
import sys

wt, pre, fix, base = sys.argv[1:5]
MODS = ('run_contract.py', 'step3_conv_cert.py', 'step3_sigma.py')
PATCHED = ('test_ca_ext_b6.py', 'test_rint_r_chain.py')
for m in MODS:
    blob = subprocess.run(['git', '-C', wt, 'show', f'{base}:scripts/{m}'], capture_output=True, check=True).stdout
    same = open(os.path.join(pre, 'scripts', m), 'rb').read() == blob
    print(f'b7pre {m} == {base}: {same}')


def walk(root):
    out = set()
    for d, dirs, files in os.walk(os.path.join(root, 'scripts')):
        dirs[:] = [x for x in dirs if x != '__pycache__']
        for f in files:
            if f.endswith('.pyc'):
                continue
            out.add(os.path.relpath(os.path.join(d, f), root))
    return out


wts = walk(wt)
for name, root, allowed in (('b7pre', pre, set('scripts/' + m for m in MODS)), ('b7fix', fix, set('scripts/' + p for p in PATCHED))):
    other = walk(root)
    missing = sorted(wts - other)
    extra = sorted(other - wts)
    diff = sorted(p for p in wts & other if not filecmp.cmp(os.path.join(wt, p), os.path.join(root, p), shallow=False))
    print(f'{name}: missing {len(missing)} {missing[:5]} · extra {len(extra)} {extra[:5]} · differ {diff}')
    print(f'{name}: differ set == expected {sorted(allowed)}: {set(diff) == allowed}')
for name, root in (('b7pre', pre), ('b7fix', fix)):
    dd = os.path.join(root, 'docs', 'data')
    print(f'{name} docs/data: islink={os.path.islink(dd)} -> {os.readlink(dd) if os.path.islink(dd) else "(dir)"}')
r = subprocess.run(['git', '-C', pre, 'cat-file', '-t', base], capture_output=True, text=True)
print('b7pre git object', base, '->', r.stdout.strip() or r.stderr.strip())
