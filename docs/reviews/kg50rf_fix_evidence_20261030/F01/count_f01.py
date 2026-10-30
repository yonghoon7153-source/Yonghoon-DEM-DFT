"""V 밖 '다름' -C 장면 (W9 · G duplicate_loop_label · Y ya · ya3 · y3bad) — 옛 판 ↔ 새 판 문제 수와 새 판의 KG50R-F01 줄 수.
   python3 -I count_f01.py <작업 트리> <옛 판> <임시 폴더 위>"""
import os
import sys
import tempfile

REPO, OLD, TMPD = sys.argv[1:4]
sys.path.insert(0, os.path.join(REPO, 'scripts'))
import test_resume_ckpt as T  # noqa: E402

NEW = os.path.join(REPO, 'scripts/resume_ckpt.sh')
tmp = tempfile.mkdtemp(prefix='cf01_', dir=TMPD)
mtxt = open(T.MAIN, encoding='utf-8').read()
good = T.res_good()
RRL = 'read_restart %s\n' % T.CKPT
DT1, DT2, TS1 = 'variable dt      equal 1.0e-6\n', 'variable dt      equal 2.0e-6\n', 'timestep        ${dt}\n'
scenes = [
    ('W9', T.write_tmp(tmp, 'm9.liggghts', T.mutate(mtxt, 'compute zmax all reduce max z\n', 'label dummy0\ncompute zmax all reduce max z\n')),
     T.write_tmp(tmp, 'w9.liggghts', T.res_variant('good')), T.CKPT, 20001),
    ('G duplicate_loop_label', T.MAIN, os.path.join(T.CX_DECK, 'duplicate_loop_label.liggghts'), T.CKPT, 20001),
    ('Y1 ya (a1)', T.MAIN, T.write_tmp(tmp, 'ya.liggghts', good.replace(RRL, RRL + DT2 + TS1 + DT1)), T.CKPT, 20001),
]
for tag, m, r, ck, s0 in scenes:
    o = T.deckcheck_only1(OLD, m, r, ck, s0)
    n = T.deckcheck_only1(NEW, m, r, ck, s0)
    ol = [l for l in o[1].splitlines() if l.startswith('  ✗ ')]
    nl = [l for l in n[1].splitlines() if l.startswith('  ✗ ')]
    print('%-26s 옛 rc %d 문제 %d · 새 rc %d 문제 %d · 새 판 KG50R-F01 줄 %d · 옛 문제 줄이 새 판에 그대로 %d/%d' % (
        tag, o[0], len(ol), n[0], len(nl), sum('KG50R-F01' in l for l in nl), sum(l in nl for l in ol), len(ol)))
