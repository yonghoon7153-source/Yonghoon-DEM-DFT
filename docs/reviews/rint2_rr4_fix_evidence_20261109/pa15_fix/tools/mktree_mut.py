# -*- coding: utf-8 -*-
"""변이 사본 트리 — argv[2] (MUT) 에 바탕 트리 argv[1] 의 맨 위 항목 링크 (scripts 뺌) + 고친 판 scripts 사본 (argv[3]/scripts · 시험 · 사슬 = 고친 판 그대로)."""
import os
import shutil
import sys
from pathlib import Path

base, mut, fixed = Path(sys.argv[1]).resolve(), Path(sys.argv[2]), Path(sys.argv[3]).resolve()
if mut.exists():
    shutil.rmtree(mut)
mut.mkdir(parents=True)
for p in sorted(base.iterdir()):
    if p.name == 'scripts':
        continue
    os.symlink(str(p), str(mut / p.name))
shutil.copytree(fixed / 'scripts', mut / 'scripts', symlinks=True, ignore=shutil.ignore_patterns('__pycache__'))
print('ok', mut, len(list(mut.iterdir())))
