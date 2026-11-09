# -*- coding: utf-8 -*-
"""고침 C — 생산자 길 원천 sha256 (바탕 ↔ 고친 판 같은지 · 이 고침은 검사 쪽만 바꾼다): ResumeRunner._src_done · run · _copy · Runner._execute · _prepare ·
run_in_group · stop_trace · run_traces · record_outdir · resume_leftovers (줄 조각 = `inspect.getsource` 같은 셈 · 들여쓰기 · 끝 줄바꿈 포함).
쓰임: python3 producer_sha.py <이름=rint_r_chain.py 경로> ..."""
import ast
import hashlib
import sys

WANT_CLS = {'ResumeRunner': ('_src_done', 'run', '_copy'), 'Runner': ('_execute', '_prepare')}
WANT_FN = ('run_in_group', 'stop_trace', 'run_traces', 'record_outdir', 'resume_leftovers', 'group_pair')
res = {}
for arg in sys.argv[1:]:
    label, path = arg.split('=', 1)
    src = open(path, encoding='utf-8').read()
    lines = src.splitlines(keepends=True)

    def seg(n):
        first = min([n.lineno] + [d.lineno for d in n.decorator_list])
        return hashlib.sha256(''.join(lines[first - 1:n.end_lineno]).encode('utf-8')).hexdigest()
    row = {}
    for n in ast.parse(src).body:
        if isinstance(n, ast.ClassDef) and n.name in WANT_CLS:
            for m in n.body:
                if isinstance(m, ast.FunctionDef) and m.name in WANT_CLS[n.name]:
                    row[f'{n.name}.{m.name}'] = seg(m)
        if isinstance(n, ast.FunctionDef) and n.name in WANT_FN:
            row[n.name] = seg(n)
    res[label] = row
labels = list(res)
names = sorted(set().union(*[set(r) for r in res.values()]))
same = 0
for nm in names:
    vals = [res[lb].get(nm) for lb in labels]
    eq = len(set(vals)) == 1 and vals[0] is not None
    same += eq
    print(f'{"같음" if eq else "다름"}  {nm}  ' + '  '.join(f'{lb} {(v or "-")[:16]}' for lb, v in zip(labels, vals)))
print(f'생산자 조각 {len(names)} 중 같음 {same}')
