"""ResumeRunner._src_done 원천 sha256 — 바탕 · 고친 판 같은지 (한정: 재실행 러너의 복사 판단 그대로) · 셈 = `inspect.getsource` 와 같은 줄 조각 (들여쓰기 ·
끝 줄바꿈 포함 · 시험 RR4E 의 RR4_SRC_DONE_SHA 와 같은 셈).  쓰임: python3 src_done_sha.py <이름=rint_r_chain.py 경로> ..."""
import ast
import hashlib
import sys

for arg in sys.argv[1:]:
    label, path = arg.split('=', 1)
    src = open(path, encoding='utf-8').read()
    lines = src.splitlines(keepends=True)
    for n in ast.parse(src).body:
        if isinstance(n, ast.ClassDef) and n.name == 'ResumeRunner':
            for m in n.body:
                if isinstance(m, ast.FunctionDef) and m.name == '_src_done':
                    first = min([m.lineno] + [d.lineno for d in m.decorator_list])
                    seg = ''.join(lines[first - 1:m.end_lineno])
                    print(hashlib.sha256(seg.encode('utf-8')).hexdigest(), f'ResumeRunner._src_done {first}–{m.end_lineno}', label)
