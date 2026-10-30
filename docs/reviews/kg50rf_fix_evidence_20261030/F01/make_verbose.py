"""V 만 사본 → 장면마다 결과 줄을 찍는 사본 (-C = rc · 판정 줄 · KG50R-F01 문제 수 / 본 흐름 = 시험 · 본 제출 · 정적 대조 줄).
   python3 -I make_verbose.py <test_vonly.py> <출력 .py>"""
import sys

src, dst = sys.argv[1:3]
t = open(src, encoding='utf-8').read()
a = "    r = deckcheck_only1(script, main, res, ckpt, s0, workdir_files)\n"
b = ("    r = deckcheck_only1(script, main, res, ckpt, s0, workdir_files)\n"
     "    _ls = r[1].splitlines()\n"
     "    print('  [-C] rc=%d · %s · KG50R-F01 문제 %d' % (r[0], (_ls[-1].strip() if _ls else ''),"
     " sum(1 for _l in _ls if _l.startswith('  ✗ ') and 'KG50R-F01' in _l)))\n")
assert t.count(a) == 1
t = t.replace(a, b)
c = "    r = run_case1(script, *a, **k)\n"
d = ("    r = run_case1(script, *a, **k)\n"
     "    _st = [x.strip() for x in r['out'].splitlines() if '재개 덱 정적 대조:' in x]\n"
     "    print('  [흐름] 시험 %d · 본 %d · %s' % (r['ntrial'], r['nmain'], (_st[-1] if _st else '정적 대조 줄 없음')))\n")
assert t.count(c) == 1
t = t.replace(c, d)
open(dst, 'w', encoding='utf-8').write(t)
print('verbose 사본:', dst)
