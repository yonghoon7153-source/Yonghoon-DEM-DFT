# -*- coding: utf-8 -*-
"""P9 — P8 의 짝: 정직 RESUME_MISMATCH 요약에서 재실행 런 기록의 이름만 바꿈 (L02_ceiling → L02_ceilingX · outdir 그에 맞춤 · resume.rerun 같이) + 멈춤 L03 런 전
   TIME_LIMIT + compared [] · assumed.  디스크: groups/L02_ceilingX.* · L02_ceilingX_arm1/ 없음 (실제 = L02_ceiling).  기대 ↔ 실제."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import h  # noqa: E402

T, RR = h.T, h.RR
NX = h.N2 + 'X'


def rename(s):
    T.rr4_tl(s)
    r = s['runs'][1]
    assert r['name'] == h.N2 and 'copied_from' not in r
    r.update(name=NX, outdir=NX + '_arm1')
    s['resume'].update(rerun=NX, compared=[], determinism='assumed')


def mk(tag):
    return T.rr4_edit(T.rr4_two(tag, 'changed-ceiling'), rename)


res = {'forged_rename': h.three('P9_rename', mk)}
res['accepted_all_three'] = h.accepted(res['forged_rename'])
atts = mk('P9_disk')
f2 = Path(atts[1][0])
res['disk'] = {'groups_' + NX: (f2 / 'groups' / f'{NX}.launch.json').exists(), 'folder_' + NX: (f2 / (NX + '_arm1')).exists(),
               'groups_' + h.N2: (f2 / 'groups' / f'{h.N2}.launch.json').exists()}
h.dump(Path(__file__).resolve().parent.parent / 'out' / 'p9_rename.json', res)
o = res['forged_rename']
print('accepted_all_three', res['accepted_all_three'], '| writer', o['writer'], '| places', o['places'], '| cli', o['cli'], '|', res['disk'])
