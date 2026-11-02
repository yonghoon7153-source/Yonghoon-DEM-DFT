#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""변이 G04 (옆 거부 기록 파일 건너뜀 뺌) 가 PD12u 의 어느 줄에서 잡히나 — 시험 러너의 사유 글은 600 자에서 잘리므로 그 줄만 직접 센다 (값 · σ 없음).

  python3 check_g04_reason.py <원 트리> <임시 폴더 바탕>
"""
import json
import sys
import tempfile
import types
from pathlib import Path

WT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(WT / 'scripts'))
OLD = ("            if not Path(p).is_dir():\n                continue                                      # 옆 거부 기록 파일")
NEW = ("            if False:\n                continue                                      # 옆 거부 기록 파일")


def load(mutate):
    src = (WT / 'scripts' / 'rint_r_chain.py').read_text(encoding='utf-8')
    if mutate:
        assert src.count(OLD) == 1
        src = src.replace(OLD, NEW, 1)
    m = types.ModuleType('rint_r_chain_g04' if mutate else 'rint_r_chain_base')
    m.__file__ = str(WT / 'scripts' / 'rint_r_chain.py')
    exec(compile(src, m.__file__, 'exec'), m.__dict__)
    return m


root = Path(tempfile.mkdtemp(prefix='g04_', dir=sys.argv[2]))
side3 = root / 'side3' / 'attempt_3.rejected.json'
side3.parent.mkdir(parents=True)
side3.write_text('{}', encoding='utf-8')
st = {'entries': {3: {'target': 'ladder:P0', 'machine': 'kgy', 'resume_of': None}},
      'results': {3: {'status': 'stopped', 'side': 'post', 'folder': 'attempt_3'}}}
out = {}
for tag, mut in (('base', False), ('G04', True)):
    out[tag] = load(mut).found_attempts_problem(st, {3: [side3]})
print(json.dumps({k: (v[:160] if isinstance(v, str) else v) for k, v in out.items()}, ensure_ascii=False, indent=1))
