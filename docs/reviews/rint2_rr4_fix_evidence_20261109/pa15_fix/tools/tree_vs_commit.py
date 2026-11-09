# -*- coding: utf-8 -*-
"""바탕 트리 사본 ↔ 커밋 대조 — 커밋의 scripts/ · webapp/ 모든 파일 git blob 해시 ↔ 사본 파일 git blob 해시 (sha1 "blob <n>\\0" + 바이트).
쓰임: python3 tree_vs_commit.py <git 작업 트리> <커밋> <사본 뿌리> [뺄 경로 …] → 같음 · 다름 · 없음 수 (뺄 경로 = 시험 먼저에서 넣은 새 시험 파일)."""
import hashlib
import subprocess
import sys
from pathlib import Path

repo, commit, copy = sys.argv[1], sys.argv[2], Path(sys.argv[3])
skip = set(sys.argv[4:])
out = subprocess.run(['git', 'ls-tree', '-r', commit, '--', 'scripts', 'webapp'], cwd=repo, capture_output=True, text=True, check=True).stdout
same = diff = miss = 0
bad = []
for line in out.splitlines():
    meta, path = line.split('\t', 1)
    mode, typ, sha = meta.split()
    if typ != 'blob' or path in skip:
        continue
    p = copy / path
    if mode == '120000':
        ok = p.is_symlink()
    elif not p.is_file():
        miss += 1
        bad.append(('없음', path))
        continue
    else:
        b = p.read_bytes()
        ok = hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest() == sha
    if ok:
        same += 1
    else:
        diff += 1
        bad.append(('다름', path))
print(f'{commit} scripts+webapp 대조: 같음 {same} · 다름 {diff} · 없음 {miss} · 뺌 {sorted(skip)}')
for k, p in bad[:20]:
    print(' ', k, p)
