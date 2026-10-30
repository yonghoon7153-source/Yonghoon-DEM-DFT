"""변이 사본 (mut/out) 을 되돌리면 지금 도구와 바이트 같은가 — 변이 시험이 고친 판 (커밋된 도구) 에서 돌았는지.
   python3 -I check_mutants_base.py <mutate_f01.py> <변이 출력 폴더> <도구>"""
import ast
import hashlib
import os
import sys

mf, outd, tool = sys.argv[1:4]
tree = ast.parse(open(mf, encoding='utf-8').read())
MUT = None
for node in tree.body:
    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'MUT' for t in node.targets):
        MUT = ast.literal_eval(node.value)
src = open(tool, encoding='utf-8').read()
print('도구 sha256', hashlib.sha256(src.encode('utf-8')).hexdigest())
ok = bad = 0
for mid, what, old, new in MUT:
    p = os.path.join(outd, 'resume_ckpt_%s.sh' % mid.replace('-', '_'))
    if not os.path.exists(p):
        print(mid, '사본 없음'); bad += 1
        continue
    m = open(p, encoding='utf-8').read()
    # 새 글이 사본에 여러 번 (다른 곳에 같은 글) — 자리마다 되돌려 보고 하나라도 도구와 같으면 같음
    same, i = False, m.find(new)
    while i >= 0 and not same:
        same = (m[:i] + old + m[i + len(new):]) == src and src.count(old) == 1
        i = m.find(new, i + 1)
    ok += same; bad += not same
    if not same:
        print(mid, '되돌려도 다름', m.count(new))
print('변이 사본 %d · 되돌리면 도구와 같음 %d · 다름 %d' % (len(MUT), ok, bad))
