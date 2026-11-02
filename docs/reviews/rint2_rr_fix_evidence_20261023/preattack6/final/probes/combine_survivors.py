#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""생존 변이를 한 사본에 함께 넣는다 (넓은 확인 = 전체 사슬 시험 · 끝-끝 한 번씩) — 합친 변이가 다 통과하면 하나씩도 통과로 본다 (서로 가리는 일은
드묾 · 추정).  RECOUNT_KEYS 변이 (M2a · b · c · e) 는 한 줄로 합친다 (= 살아남은 칸을 다 뺌).

  python3 combine_survivors.py <원 트리> <사본 트리> <id,id,…>
"""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
spec = importlib.util.spec_from_file_location('m6', HERE.parent / 'mutate_pc6.py')
M6 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M6)

wt, tree, ids = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3].split(',')
src = (wt / 'scripts' / 'rint_r_chain.py').read_text(encoding='utf-8')
allm = {m[0]: m for m in M6.load_pc5() + M6.NEW}
rk = [i for i in ids if i.startswith('M2')]
rest = [i for i in ids if not i.startswith('M2')]
out = src
if rk:
    drop = {'M2a': 'status', 'M2b': 'stop', 'M2c': 'side', 'M2d': 'cause', 'M2e': 'resume_ok'}
    keep = [k for k in ('status', 'stop', 'side', 'cause', 'resume_ok') if k not in {drop[i] for i in rk}]
    old = "RECOUNT_KEYS = ('status', 'stop', 'side', 'cause', 'resume_ok')"
    assert out.count(old) == 1
    out = out.replace(old, 'RECOUNT_KEYS = (' + ''.join(f"'{k}', " for k in keep) + ')', 1)
for i in rest:
    _mid, _why, o, n, _only, _int = allm[i]
    c = out.count(o)
    if c != 1:
        sys.exit(f'{i}: 옛 글 {c} 번 (합친 사본)')
    out = out.replace(o, n, 1)
import ast  # noqa: E402
ast.parse(out)
(tree / 'scripts' / 'rint_r_chain.py').write_text(out, encoding='utf-8')
print('combined', ids, 'RECOUNT_KEYS keep =', keep if rk else 'unchanged')
