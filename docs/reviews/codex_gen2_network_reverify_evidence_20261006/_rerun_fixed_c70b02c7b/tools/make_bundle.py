"""Assemble the scratch bundle: <base>/bundle/{source (HEAD export), probes (Codex probe copies), evidence, tmp} + <base>/cwd.

usage: python3 -I make_bundle.py <base_dir> <head.tar> <probes_dir> <head_sha>
"""
import shutil
import sys
import tarfile
from pathlib import Path

base, tar_p, probes_src, head = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
b = base / 'bundle'
src = b / 'source'
for d in (src, b / 'probes', b / 'evidence', b / 'tmp', base / 'cwd'):
    d.mkdir(parents=True, exist_ok=True)
with tarfile.open(tar_p) as t:
    t.extractall(src, filter='data')
for p in sorted(probes_src.glob('*.py')):
    shutil.copyfile(p, b / 'probes' / p.name)
(b / 'SOURCE_HEAD.txt').write_text(head + '\n', encoding='utf-8')
n = sum(1 for _ in src.rglob('*') if _.is_file())
print('bundle', b, 'files', n, 'probes', sorted(p.name for p in (b / 'probes').glob('*.py')))
