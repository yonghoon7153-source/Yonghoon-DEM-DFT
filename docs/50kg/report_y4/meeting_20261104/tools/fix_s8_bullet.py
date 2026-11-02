"""① 8장: 빨강 run 이 문단 첫 run 이 되어 글머리표 (•) 도 빨갛게 그려지는 것 고침 — 글머리 색을 같은 문단 일반 글 색으로 고정 (<a:buClr>)
② 4장 세 칸 그림 자리 글을 짧게 (좁은 칸에서 줄바꿈) — '웹앱 3D' / '기공 보기'
usage: python3 -I fix_s8_bullet.py in.pptx out.pptx
"""
import copy
import sys

from pptx import Presentation
from pptx.oxml.ns import qn

prs = Presentation(sys.argv[1])
s8 = prs.slides[7]
paras = [p for sh in s8.shapes if sh.name == 'Rectangle 23' for p in sh.text_frame.paragraphs
         if p.text.startswith('미립 전해질 이온전도도 감소 (0.45배)와 상쇄')]
assert len(paras) == 1
p = paras[0]
plain = [r for r in p.runs if r._r.find(qn('a:rPr')).find(qn('a:solidFill') + '/' + qn('a:srgbClr')) is None
         or r._r.find(qn('a:rPr')).find(qn('a:solidFill') + '/' + qn('a:srgbClr')).get('val') != 'FF5050']
assert plain, '일반 글 run 없음'
fill = plain[0]._r.find(qn('a:rPr')).find(qn('a:solidFill'))
assert fill is not None and len(fill) == 1
ppr = p._p.find(qn('a:pPr'))
assert ppr.find(qn('a:buClr')) is None and ppr.find(qn('a:buClrTx')) is None
bu = ppr.makeelement(qn('a:buClr'), {})
bu.append(copy.deepcopy(fill[0]))
after = [c for c in ppr if c.tag in (qn('a:lnSpc'), qn('a:spcBef'), qn('a:spcAft'))]
ppr.insert(list(ppr).index(after[-1]) + 1 if after else 0, bu)
print('① 8장 글머리 색 =', fill[0].tag.split('}')[1], dict(fill[0].attrib))

s4 = prs.slides[3]
n = 0
for sh in s4.shapes:
    if sh.name.startswith('3D 그림 자리 (웹앱) '):
        ts = sh._element.findall('.//' + qn('a:t'))
        assert [t.text for t in ts] == ['3D 그림 (웹앱)', '기공 (빈 공간) 보기']
        ts[0].text, ts[1].text = '웹앱 3D', '기공 보기'
        n += 1
assert n == 3
print('② 4장 칸 글', n)
prs.save(sys.argv[2])
