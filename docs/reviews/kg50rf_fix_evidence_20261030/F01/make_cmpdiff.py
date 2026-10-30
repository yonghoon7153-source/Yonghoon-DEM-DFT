"""시험 파일 사본 — --compare-old 에서 V 밖 묶음의 '다름' 장면마다 옛 판 ↔ 새 판 출력 (out_n · rep_n) 차이 줄과 작업 폴더 지도 차이를 찍는다.
   python3 -I make_cmpdiff.py <scripts/test_resume_ckpt.py> <출력 .py> <리포 뿌리>"""
import sys

src, dst, repo = sys.argv[1:4]
t = open(src, encoding='utf-8').read()
helper = '''
def _cmpdiff(g, kind, new, old, keys):
    import difflib
    print('   ~~ 다름 %s %s · %s' % (g, kind, ', '.join(keys)))
    for k in ('out_n', 'rep_n'):
        if k in keys:
            d = [l for l in difflib.unified_diff(old[k].split('\\n'), new[k].split('\\n'), 'old', 'new', lineterm='', n=0)
                 if l[:1] in '+-' and l[:3] not in ('+++', '---')]
            print('      [%s] 다른 줄 %d' % (k, len(d)))
            for l in d[:10]:
                print('        ' + l[:240])
    if 'w_cmp' in keys:
        a, b = old['w_cmp'], new['w_cmp']
        for x in sorted(set(a) | set(b)):
            if a.get(x) != b.get(x):
                print('      [w_cmp] %s : 옛 %s ↔ 새 %s' % (x, str(a.get(x))[:60], str(b.get(x))[:60]))


def run_case(script, *a, **k):'''
a0 = '\ndef run_case(script, *a, **k):'
assert t.count(a0) == 1
t = t.replace(a0, helper, 1)
a1 = "        d = [x for x in ('trial', 'main', 'rc', 'out_n', 'rep_n', 'w_cmp', 's_same') if r[x] != o[x]]\n"
assert t.count(a1) == 1
t = t.replace(a1, a1 + "        if d and CMP['grp'] != 'V':\n            _cmpdiff(CMP['grp'], 'run', r, o, d)\n", 1)
a2 = "        o = deckcheck_only1(CMP['old'], main, res, ckpt, s0, workdir_files)\n"
assert t.count(a2) == 1
t = t.replace(a2, a2 + "        if CMP['grp'] != 'V' and (r[0] != o[0] or r[2] != o[2]):\n"
                       "            _cmpdiff(CMP['grp'], '-C %s' % os.path.basename(res), {'out_n': r[2]}, {'out_n': o[2]},"
                       " [x for x, y, z in (('rc', r[0], o[0]), ('out_n', r[2], o[2])) if y != z])\n", 1)
root_line = "ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n"
assert t.count(root_line) == 1
t = t.replace(root_line, 'ROOT = %r\n' % repo)
open(dst, 'w', encoding='utf-8').write(t)
print('사본:', dst)
