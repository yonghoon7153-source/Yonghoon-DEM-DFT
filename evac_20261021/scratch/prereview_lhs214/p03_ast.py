#!/usr/bin/env python3
"""P03 — 영수증 도구 최상위 문 AST 비교 (옛 판 a76f59d0d · a69963967 ↔ fe23f2b83 · HEAD) + sha256 + _selftest 밖 바이트.
재실행: python3 -I p03_ast.py <worktree>"""
import ast, hashlib, json, subprocess, sys
WT = sys.argv[1] if len(sys.argv) > 1 else '.'
F = 'scripts/supp20_input_receipt.py'


def show(rev):
    return subprocess.run(['git', 'show', f'{rev}:{F}'], cwd=WT, capture_output=True, check=True).stdout


def top(src):
    t = ast.parse(src)
    out = []
    for n in t.body:
        name = getattr(n, 'name', None) or (n.targets[0].id if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) else type(n).__name__)
        out.append((name, ast.dump(n, include_attributes=False)))
    return out


res = {}
revs = ['a76f59d0d16c58b2f7816d67a3432f94367e46f0', 'a6996396774064fa159d360da0e1d26877b66c33', 'fe23f2b839f0a49adb077348fec6d4c85443b62a',
        '7f99be67c7bd66416e2b125e62cba50ca6f8a03a', '34713ac9650ece7c8d59b7c4d9a2aefccee693ea']
srcs = {r: show(r) for r in revs}
for r, b in srcs.items():
    res[r[:9]] = dict(sha256=hashlib.sha256(b).hexdigest(), n_top=len(ast.parse(b).body))
old, new = top(srcs[revs[1]]), top(srcs[revs[3]])
res['n_top_old_new'] = [len(old), len(new)]
res['names_equal'] = [a[0] for a in old] == [b[0] for b in new]
res['changed_top'] = [a[0] for a, b in zip(old, new) if a[1] != b[1]]
# 바이트 비교: _selftest 정의의 줄 범위 밖이 같은가 (줄 이동 감안 — _selftest 앞 · 뒤 글)
def split_around(b):
    s = b.decode('utf-8')
    t = ast.parse(s)
    fn = [n for n in t.body if isinstance(n, ast.FunctionDef) and n.name == '_selftest'][0]
    lines = s.split('\n')
    return '\n'.join(lines[:fn.lineno - 1]), '\n'.join(lines[fn.end_lineno:])
pre_o, post_o = split_around(srcs[revs[1]])
pre_n, post_n = split_around(srcs[revs[3]])
res['bytes_before_selftest_equal'] = pre_o == pre_n
res['bytes_after_selftest_equal'] = post_o == post_n
res['a76f_vs_a699_same_bytes'] = srcs[revs[0]] == srcs[revs[1]]
res['34713_vs_a699_same_bytes'] = srcs[revs[4]] == srcs[revs[1]]
res['fe23_vs_head_same_bytes'] = srcs[revs[2]] == srcs[revs[3]]
print(json.dumps(res, indent=1))
