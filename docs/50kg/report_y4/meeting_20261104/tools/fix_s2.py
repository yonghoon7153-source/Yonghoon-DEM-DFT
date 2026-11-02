"""진도점검 덱 2장 고침 (1저자 11-02 "2pg도 설명 및 수정할 부분 수정하고"):
  ① 펠릿 그림 = y축 σ 이탤릭판 (덱 다른 그림과 같은 대체 글꼴로 다시 만든 것) — 같은 그림 파트를 쓰는 7장도 같이 바뀜
  ② 캡션 (왼쪽) · (오른쪽) 빼기 — 1저자 "왼쪽 오른쪽 이렇게 캡션하지말고"
  ③ 그림 자리 = 3 µm · 1 µm 두 칸 + 아래 라벨 (1장 라벨 서식 그대로) — 웹앱 'AM 접촉 · Coverage 확대' 그림 붙일 자리
usage: python3 -I fix_s2.py in.pptx out.pptx new_pellet.png
"""
import copy
import io
import sys

from PIL import Image
from pptx import Presentation
from pptx.oxml.ns import qn

SRC, DST, PNG = sys.argv[1:4]
IN = 914400
OLD_CAP = '【 미립 전해질의 활물질 표면 접촉 (왼쪽) 및 입도별 전해질 펠릿 이온전도도 (오른쪽, 3차년도) 】'
NEW_CAP = '【 전해질 입도별 활물질 표면 접촉 및 펠릿 이온전도도 (3차년도) 】'
SLOT = '3D 그림 자리 (웹앱)'

prs = Presentation(SRC)
s1, s2 = prs.slides[0], prs.slides[1]

# ① 그림 파트 교체 (같은 크기 확인 · 쓰는 곳 출력)
pic = [sh for sh in s2.shapes if sh.name == 'Picture 4']
assert len(pic) == 1
part = s2.part.related_part(pic[0]._element.blipFill.blip.rEmbed)
users = [(n, sh.name) for n, s in enumerate(prs.slides, 1) for sh in s.shapes
         if sh.shape_type == 13 and s.part.related_part(sh._element.blipFill.blip.rEmbed) is part]
new = open(PNG, 'rb').read()
assert Image.open(io.BytesIO(new)).size == Image.open(io.BytesIO(part.blob)).size, '그림 픽셀 크기 다름'
part._blob = new
print('① 그림', part.partname, '쓰는 곳', users)

# ② 캡션
hits = [r for sh in s2.shapes if sh.has_text_frame for p in sh.text_frame.paragraphs for r in p.runs if r.text == OLD_CAP]
assert len(hits) == 1, f'캡션 run {len(hits)}'
hits[0].text = NEW_CAP
print('② 캡션', NEW_CAP)

# ③ 그림 자리 → 두 칸 + 라벨
slots = [sh for sh in s2.shapes if sh.name == SLOT]
assert len(slots) == 1
slot = slots[0]
X, Y, W, H = slot.left, slot.top, slot.width, slot.height
gap, lab_h = int(0.10 * IN), int(0.27 * IN)
cw, ch = (W - gap) // 2, H - lab_h - int(0.02 * IN)
tree = slot._element.getparent()
idx = tree.index(slot._element)
nid = max(int(e.get('id')) for e in tree.iter(qn('p:cNvPr'))) + 1
labs = [sh for sh in s1.shapes if sh.name == '3D 라벨 3 µm']
assert len(labs) == 1
for k, size in enumerate(('3 µm', '1 µm')):
    el = copy.deepcopy(slot._element)
    nv = el.find('.//' + qn('p:cNvPr'))
    nv.set('id', str(nid)); nv.set('name', f'{SLOT} {size}'); nid += 1
    el.find('.//' + qn('a:off')).set('x', str(X + k * (cw + gap)))
    el.find('.//' + qn('a:off')).set('y', str(Y))
    el.find('.//' + qn('a:ext')).set('cx', str(cw))
    el.find('.//' + qn('a:ext')).set('cy', str(ch))
    ts = el.findall('.//' + qn('a:t'))
    assert len(ts) == 2
    ts[0].text, ts[1].text = '3D 그림 (웹앱)', 'AM 접촉 · Coverage 확대'
    tree.insert(idx + 1 + 2 * k, el)
    lab = copy.deepcopy(labs[0]._element)
    nv = lab.find('.//' + qn('p:cNvPr'))
    nv.set('id', str(nid)); nv.set('name', f'3D 라벨 {size}'); nid += 1
    lab.find('.//' + qn('a:off')).set('x', str(X + k * (cw + gap)))
    lab.find('.//' + qn('a:off')).set('y', str(Y + ch + int(0.02 * IN)))
    lab.find('.//' + qn('a:ext')).set('cx', str(cw))
    lab.find('.//' + qn('a:ext')).set('cy', str(lab_h))
    ts = lab.findall('.//' + qn('a:t'))
    assert len(ts) == 1
    ts[0].text = size
    tree.insert(idx + 2 + 2 * k, lab)
tree.remove(slot._element)
print(f'③ 두 칸 {cw / IN:.2f} × {ch / IN:.2f} in · 라벨 높이 {lab_h / IN:.2f}')
prs.save(DST)
