# 영률 이온전도도 장 (템플릿 15장) = 입도 장 (10장 · 1저자 5쪽) 과 같은 방법: 이온 전류 3D 셋 (11-03 웹앱 캡처) + 공동 컬러바
# (중앙값으로 나눈 값 0 – 1) + 그림 아래 그 전극의 중앙값 (웹앱 컬러바 위쪽 = p50).  한 장짜리 PPTX 로 낸다.
import sys, io, copy
import numpy as np
from PIL import Image
from pptx import Presentation
from pptx.util import Emu
DECK, OUT, IMGDIR = sys.argv[1], sys.argv[2], sys.argv[3]
BEDS = {1: ('11', 'E11.webp', '0.13', 41165), 2: ('22', 'E22.webp', '0.14', 39402), 3: ('33', 'E33.webp', '0.15', 38063)}
prs = Presentation(DECK)
s = prs.slides[14]
assert 'modulus' in s.shapes[1].text_frame.text and s.notes_slide.notes_text_frame.text.startswith('유효 이온전도도 0.0544')
def crop_png(p):
    im = Image.open(p).convert('RGBA'); a = np.asarray(im)
    ink = (a[..., 3] > 128) & (a[..., :3].min(-1) < 235); ys, xs = np.where(ink); pad = 6
    im = im.crop((max(xs.min() - pad, 0), max(ys.min() - pad, 0), min(xs.max() + 1 + pad, im.width), min(ys.max() + 1 + pad, im.height)))
    bg = Image.new('RGBA', im.size, (255, 255, 255, 255)); bg.alpha_composite(im); im = bg.convert('RGB')   # 투명 배경 → 흰색 (5쪽 그림과 같은 바탕)
    buf = io.BytesIO(); im.save(buf, 'PNG'); buf.seek(0); return buf, im.size
pics = {}
for c, (g, fn, med, ncc) in BEDS.items():
    slot = next(x for x in s.shapes if x.name == 'Image slot current density %d' % c)
    buf, (iw, ih) = crop_png(IMGDIR + '/' + fn)
    pad = Emu(int(0.03 * 914400)); W, H = slot.width - 2 * pad, slot.height - 2 * pad
    r = min(W / iw, H / ih); w, h = int(iw * r), int(ih * r)
    pic = s.shapes.add_picture(buf, slot.left + (slot.width - w) // 2, slot.top + (slot.height - h) // 2, w, h)
    pic.name = 'Ion current E%s' % g; pics[c] = pic
    slot._element.getparent().remove(slot._element)
lab = next(x for x in s.shapes if x.name == 'Colorbar label')
runs = lab.text_frame.paragraphs[0].runs
assert [r.text for r in runs][:2] == ['[ Li', '+'], [r.text for r in runs]
runs[2].text = ' current density / median ]'
for r_ in runs[3:]: r_._r.getparent().remove(r_._r)
mn = next(x for x in s.shapes if x.name == 'Colorbar min'); mx = next(x for x in s.shapes if x.name == 'Colorbar max (edit)')
p_ = mx.text_frame.paragraphs[0]._p
p_.insert(len(p_) - 1, copy.deepcopy(mn.text_frame.paragraphs[0].runs[0]._r))
mx.text_frame.paragraphs[0].runs[0].text = '1'; mx.name = 'Colorbar max'
ids = [int(e.get('id')) for e in s.shapes._spTree.iter() if e.tag.endswith('}cNvPr')]
y = max(p.top + p.height for p in pics.values()) + Emu(int(0.05 * 914400))
for c, (g, fn, med, ncc) in BEDS.items():
    el = copy.deepcopy(mn._element); mn._element.addnext(el)
    cnv = el.xpath('./p:nvSpPr/p:cNvPr')[0]; cnv.set('id', str(max(ids) + c)); cnv.set('name', 'Median label %d' % c)
    sh = next(x for x in s.shapes if x._element is el)
    sh.left, sh.width = pics[c].left - Emu(int(0.2 * 914400)), pics[c].width + Emu(int(0.4 * 914400))
    sh.top, sh.height = y, Emu(int(0.2 * 914400))
    r0 = sh.text_frame.paragraphs[0].runs[0]; r0.text = 'median %s A cm' % med
    r1 = copy.deepcopy(r0._r); r0._r.addnext(r1)
    sh.text_frame.paragraphs[0].runs[1].text = '−2'
    r1.find('{http://schemas.openxmlformats.org/drawingml/2006/main}rPr').set('baseline', '30000')
old = s.notes_slide.notes_text_frame.text
s.notes_slide.notes_text_frame.text = (
    '3D = 세 전극에 각각 1 V 를 걸었을 때 전해질–전해질 접촉의 Li⁺ 전류 밀도 (Hertz 접촉 · 전류가 흐르는 접촉 전부 = '
    '11 GPa 41165 · 22 GPa 39402 · 33 GPa 38063 개 · 11-03 웹앱 캡처 · 22 GPa = D_SE 2 µm 와 같은 침대).\n'
    '색 = 각 전극의 접촉 전류 밀도를 그 전극의 중앙값으로 나눈 값 (웹앱 색 위쪽 = 전극마다 중앙값이라 세 그림에 공통 절대 눈금이 없다) · '
    '중앙값 0.13 / 0.14 / 0.15 A cm⁻² = 그림 아래.\n' + old.rstrip())
# 이 장만 남긴다
sld = prs.slides._sldIdLst
for i, sid in reversed(list(enumerate(list(sld)))):
    if i != 14:
        prs.part.drop_rel(sid.rId); sld.remove(sid)
prs.save(OUT)
print('saved', OUT, 'slides', len(prs.slides))
