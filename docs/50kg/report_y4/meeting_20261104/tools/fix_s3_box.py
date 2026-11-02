"""3장 — 오른쪽 접촉 모델 그림 설명 상자 + 용어 'hysteretic spring' (1저자 11-02 '권고대로' = B 판).
  · 오른쪽 그림 넷 = 같은 배치 그대로 0.93 배 · 위 끝 3.05 in (상자 자리) · 왼쪽 그림 · 글머리 위치 · 캡션 그대로
  · 글머리 셋째 줄 '(이력 스프링, 마찰)' → '(hysteretic spring, 마찰)'
  · 상자 = 왼쪽 그림의 회색 이름 상자 색 (E7E7E7 · 테두리 · 그림자 없음) · 편집 가능한 글 (KoPub Medium 10 pt · 머리말 Bold · 변수 이탤릭 · 첨자)
usage: python3 -I fix_s3_box.py in.pptx out.pptx
"""
import copy
import sys

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR
from pptx.oxml.ns import qn
from pptx.util import Inches

prs = Presentation(sys.argv[1])
slide = prs.slides[2]
NAMES = ['접촉 모델 ① 입자 힘', '접촉 모델 ② 접촉 요소', '접촉 모델 ③ 법선 힘', '접촉 모델 ④ 접선 힘']
SCALE, TOP = 0.93, Inches(3.05)
BOX = dict(x=5.191, y=5.78, w=4.201, h=0.60)
LINES = [
    [('입자 운동: ', 'b'), ('접촉력 · 중력 (병진), 접선력 · 구름 저항 (회전)', 'n')],
    [('법선력: ', 'b'), ('hysteretic spring — 가압 ', 'n'), ('k', 'i'), ('1', 's'), (' / 제하 ', 'n'), ('k', 'i'), ('2', 's'),
     (', 잔류 겹침 ', 'n'), ('δ', 'i'), ('0', 's')],
    [('접선력: ', 'b'), ('스프링 ', 'n'), ('k', 'i'), ('t', 's'), (' + 마찰 (|', 'n'), ('F', 'i'), ('t', 's'), ('| ≤ ', 'n'),
     ('μF', 'i'), ('n', 's'), (', 도달 시 미끄러짐)', 'n')],
]
pics = {sh.name: sh for sh in slide.shapes if sh.name in NAMES}
if len(pics) != 4 or any(sh.name == '접촉 모델 설명 상자' for sh in slide.shapes):
    raise SystemExit(f'3장 대상 그림 {len(pics)} 개 · 또는 상자가 이미 있음')
ox0 = min(p.left for p in pics.values()); oy0 = min(p.top for p in pics.values())
ox1 = max(p.left + p.width for p in pics.values())
gx0 = int((ox0 + ox1) / 2 - (ox1 - ox0) * SCALE / 2)
for p in pics.values():
    l, t, w, h = p.left, p.top, p.width, p.height
    p.left = int(gx0 + (l - ox0) * SCALE); p.top = int(TOP + (t - oy0) * SCALE)
    p.width = int(w * SCALE); p.height = int(h * SCALE)
runs = [r for sh in slide.shapes if sh.name == 'Rectangle 23' for para in sh.text_frame.paragraphs for r in para.runs]
hit = [r for r in runs if '(이력 스프링, 마찰)' in r.text]
if len(hit) != 1:
    raise SystemExit(f'글머리 대상 run {len(hit)}')
hit[0].text = hit[0].text.replace('(이력 스프링, 마찰)', '(hysteretic spring, 마찰)')
tmpl = [r for r in runs if r.text.startswith('입자 생성')][0]._r.find(qn('a:rPr'))
box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(BOX['x']), Inches(BOX['y']), Inches(BOX['w']), Inches(BOX['h']))
box.name = '접촉 모델 설명 상자'
box.fill.solid(); box.fill.fore_color.rgb = RGBColor(0xE7, 0xE7, 0xE7)
box.line.fill.background()
box.shadow.inherit = False
st = box._element.find(qn('p:style'))
if st is not None:
    box._element.remove(st)
tf = box.text_frame
tf.word_wrap = True
tf.margin_left = tf.margin_right = Inches(0.08); tf.margin_top = tf.margin_bottom = Inches(0.03)
tf.vertical_anchor = MSO_ANCHOR.MIDDLE
body = tf._txBody
for p in list(body.findall(qn('a:p'))):
    body.remove(p)
for segs in LINES:
    p = body.makeelement(qn('a:p'), {})
    ppr = p.makeelement(qn('a:pPr'), {'algn': 'l'})
    ln = ppr.makeelement(qn('a:lnSpc'), {}); ln.append(ln.makeelement(qn('a:spcPct'), {'val': '100000'})); ppr.append(ln)
    p.append(ppr)
    for text, kind in segs:
        r = p.makeelement(qn('a:r'), {})
        rpr = copy.deepcopy(tmpl)
        rpr.set('sz', '1000'); rpr.set('lang', 'ko-KR')
        for a in ('i', 'b', 'baseline'):
            rpr.attrib.pop(a, None)
        if kind == 'b':
            rpr.set('b', '1')
            for tag in ('a:latin', 'a:ea'):
                rpr.find(qn(tag)).set('typeface', 'KoPubWorld돋움체 Bold')
        elif kind == 'i':
            rpr.set('i', '1')
        elif kind == 's':
            rpr.set('baseline', '-25000')
        r.append(rpr)
        t = r.makeelement(qn('a:t'), {}); t.text = text; r.append(t)
        p.append(r)
    body.append(p)
prs.save(sys.argv[2])
print('3장: 그림 넷 0.93 배 · 위 끝 3.05 in · 글머리 hysteretic spring · 설명 상자 세 줄')
