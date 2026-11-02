"""7장 이온 전류 3D 자리 셋 → 웹앱 이온 전류 그림 셋 (3 · 2 · 1 µm · 1저자 11-02 웹앱 캡처 · "전체가 나을듯") + 전극마다 컬러바.
  - 웹앱 설정 (1저자 화면): 이온 (SE–SE) · 전류 = 전체 · 주 갈래 · 굵기 ×1 · 선형 눈금 · 위쪽 p50
  - 웹앱 색 위쪽 = 침대마다 백분위 (p50) → 색 눈금이 전극마다 다르다 → 그림마다 자기 컬러바 · 눈금 (0 과 위쪽 끝)
  - 컬러바 = 웹앱 그림의 막대만 잘라 쓴다 (웹앱 제목 줄의 내부 용어 · 작은 숫자는 화면에 안 둔다) · 눈금 · 제목 = 편집 가능한 글 상자
  - 왼쪽 끝 눈금 = 0 (웹앱 최솟값 10⁻¹⁰–10⁻⁶ A cm⁻² = 위쪽 끝의 10⁻⁵ 미만 · 이 눈금에서 0 으로 반올림)
usage: python3 -I put_jcur_s7.py in.pptx out.pptx FIGDIR SEL 3d_3um cb_3um top_3um 3d_2um cb_2um top_2um 3d_1um cb_1um top_1um
  SEL = all | 95 (웹앱 "전류" 칸) · top = 웹앱 컬러바 오른쪽 끝 숫자 (예: 0.094)
"""
import os
import sys

import numpy as np
from PIL import Image
from pptx import Presentation
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

SRC, DST, FIG, SEL = sys.argv[1:5]
ARGS = sys.argv[5:]
assert SEL in ('all', '95') and len(ARGS) == 9, (SEL, ARGS)
BEDS = ('3', '2', '1')
PANEL = {b: ARGS[3 * k:3 * k + 3] for k, b in enumerate(BEDS)}
for b in BEDS:
    float(PANEL[b][2])
FONT = 'KoPubWorld돋움체 Medium'
HMAX, CBW = 2.20, 1.20
os.makedirs(FIG, exist_ok=True)
E = 914400


def crop_alpha(src, dst, pad=14):
    im = Image.open(src).convert('RGBA')
    a = np.asarray(im)
    m = a[..., 3] > 20
    if m.all():
        raise SystemExit(f'{src}: 배경이 투명하지 않다 (웹앱 PNG/WebP 투명 캡처여야 한다)')
    cols, rows = np.where(m.any(0))[0], np.where(m.any(1))[0]
    box = (max(cols[0] - pad, 0), max(rows[0] - pad, 0), min(cols[-1] + pad, a.shape[1] - 1) + 1, min(rows[-1] + pad, a.shape[0] - 1) + 1)
    im.crop(box).save(dst, 'PNG')
    return Image.open(dst).size


def crop_bar(src, dst):
    """막대 (채도 높은 줄) 위아래 4 px 만 — 웹앱 제목 · 눈금 숫자 · 설명 글은 뺀다."""
    a = np.asarray(Image.open(src).convert('RGB')).astype(int)
    sat = a.max(2) - a.min(2)
    bar = np.where((sat > 60).mean(1) > 0.3)[0]
    top, bot = bar.min(), bar.max()
    cols = np.where((sat[top:bot + 1] > 60).mean(0) > 0.3)[0]
    box = (max(cols[0] - 4, 0), top - 4, min(cols[-1] + 4, a.shape[1] - 1) + 1, bot + 5)
    Image.open(src).convert('RGB').crop(box).save(dst, 'PNG')
    return Image.open(dst).size


def textbox(s, name, x, y, w, h, segs, size=10.5, align=PP_ALIGN.CENTER):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tb.name = name
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = align
    for text, kind in segs:
        r = p.add_run()
        r.text = text
        r.font.size = Pt(size)
        rpr = r._r.get_or_add_rPr()
        if kind == 'sup':
            rpr.set('baseline', '30000')
        for tag in ('a:latin', 'a:ea', 'a:cs'):
            el = rpr.find(qn(tag))
            if el is None:
                el = rpr.makeelement(qn(tag), {})
                rpr.append(el)
            el.set('typeface', FONT)
    return tb


prs = Presentation(SRC)
s = prs.slides[6]
slot = {}
for b in BEDS:
    sh = [x for x in s.shapes if x.name == f'3D 그림 자리 (웹앱) {b} µm']
    if len(sh) != 1:
        raise SystemExit(f'7장 {b} µm 자리 {len(sh)} 개')
    slot[b] = (sh[0].left / E, sh[0].top / E, sh[0].width / E)
gone = [x for x in s.shapes if x.name.startswith(('3D 그림 자리 (웹앱)', '3D 라벨'))]
if len(gone) != 6:
    raise SystemExit(f'7장 자리 · 라벨 {len(gone)} 개 (6 이어야 한다)')
for x in gone:
    x._element.getparent().remove(x._element)
size3d, sizecb = {}, {}
for b in BEDS:
    size3d[b] = crop_alpha(PANEL[b][0], os.path.join(FIG, f'jcur3d_{b}um.png'))
    sizecb[b] = crop_bar(PANEL[b][1], os.path.join(FIG, f'jcur_colorbar_{b}um.png'))
H = min([HMAX] + [slot[b][2] * size3d[b][1] / size3d[b][0] for b in BEDS])
y0 = slot['3'][1]
for b in BEDS:
    sx, _, sw = slot[b]
    w = H * size3d[b][0] / size3d[b][1]
    pic = s.shapes.add_picture(os.path.join(FIG, f'jcur3d_{b}um.png'), Inches(sx + (sw - w) / 2), Inches(y0), height=Inches(H))
    pic.name = f'이온 전류 3D {b} µm'
    yl = y0 + H + 0.03
    textbox(s, f'이온 전류 3D 라벨 {b} µm', sx, yl, sw, 0.22, [(f'{b} µm', 'n')])
    xc, yc = sx + (sw - CBW) / 2, yl + 0.25
    cb = s.shapes.add_picture(os.path.join(FIG, f'jcur_colorbar_{b}um.png'), Inches(xc), Inches(yc), width=Inches(CBW))
    cb.name = f'이온 전류 컬러바 {b} µm'
    cbh = CBW * sizecb[b][1] / sizecb[b][0]
    yt = yc + cbh + 0.02
    textbox(s, f'이온 전류 컬러바 눈금 {b} µm 왼쪽', xc - 0.05, yt, 0.5, 0.18, [('0', 'n')], size=9, align=PP_ALIGN.LEFT)
    textbox(s, f'이온 전류 컬러바 눈금 {b} µm 오른쪽', xc + CBW - 0.45, yt, 0.5, 0.18, [(PANEL[b][2], 'n')], size=9, align=PP_ALIGN.RIGHT)
x0, x1 = slot['3'][0], slot['1'][0] + slot['1'][2]
textbox(s, '이온 전류 컬러바 제목', x0, yt + 0.21, x1 - x0, 0.22,
        [('Li', 'n'), ('+', 'sup'), (' current density (A cm', 'n'), ('−2', 'sup'), (')', 'n')], size=10)
notes = [p for p in s.notes_slide.notes_text_frame.paragraphs if p.runs][0]
old = '3D 그림은 같은 계산의 이온 전류 밀도 분포입니다.'
r = [x for x in notes.runs if old in x.text]
if len(r) != 1:
    raise SystemExit('7장 노트 3D 문장 못 찾음')
sel_txt = '전류가 흐르는 접촉을 모두 그렸습니다' if SEL == 'all' else '전류의 95 %를 나르는 접촉만 그렸습니다'
new = (f'3D 그림은 세 전극에 각각 1 V를 걸었을 때 전해질–전해질 접촉별 이온 전류 밀도이고, {sel_txt}. '
       '색 막대 오른쪽 끝은 전극마다 접촉 전류 밀도의 중앙값입니다.')
r[0].text = r[0].text.replace(old, new)
prs.save(DST)
print(f'3D 높이 {H:.2f} in · ' + ' · '.join(f'{b} µm {size3d[b][0]}x{size3d[b][1]} px 컬러바 {sizecb[b][0]}x{sizecb[b][1]} px 위 {PANEL[b][2]}' for b in BEDS))
print(f'아래 끝 (제목) {yt + 0.21 + 0.22:.2f} in')
