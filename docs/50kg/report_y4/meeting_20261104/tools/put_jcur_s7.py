"""7장 이온 전류 3D 자리 셋 → 웹앱 이온 전류 그림 하나 (1 µm · 1저자 11-02 웹앱 캡처 "이렇게함") + 컬러바.
  - 웹앱 설정 (1저자 화면): 이온 (SE–SE) · 전류 95 % (247626 개) · 주 갈래 · 굵기 ×1 · 선형 눈금 (이등분) · 위쪽 p50
  - 접촉 247,626 개 = 1 µm 침대만 가능 (SE–SE 접촉 ≈ 166,971 × 4.98 / 2 ≈ 4.2 × 10⁵ · 2 µm ≈ 4.2 × 10⁴)
  - 웹앱 색 위쪽 = 침대마다 백분위 (p50) → 세 침대를 나란히 두면 색 눈금이 서로 다르다 → 이종기술 덱처럼 대표 하나
  - 컬러바 = 웹앱 그림의 막대 + 눈금 숫자만 잘라 쓴다 (웹앱 제목 줄의 내부 용어는 화면에 안 둔다) · 제목 = 편집 가능한 글 상자
usage: python3 -I put_jcur_s7.py in.pptx out.pptx FIGDIR jcur3d.webp colorbar.webp TICKS SEL
  TICKS = 웹앱 컬러바 눈금 셋 (예: 0.022,0.17,0.31 — 편집 가능한 글로 단다 · 그림 속 숫자는 너무 작아 잘라 낸다) · SEL = all | 95 (웹앱 "전류" 칸)
"""
import os
import sys

import numpy as np
from PIL import Image
from pptx import Presentation
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

SRC, DST, FIG, J3D, JCB, TICKS, SEL = sys.argv[1:8]
TICKS = TICKS.split(',')
assert len(TICKS) == 3 and SEL in ('all', '95'), (TICKS, SEL)
FONT = 'KoPubWorld돋움체 Medium'
os.makedirs(FIG, exist_ok=True)


def crop_alpha(src, dst, pad=14):
    im = Image.open(src).convert('RGBA')
    a = np.asarray(im)
    m = a[..., 3] > 20
    cols, rows = np.where(m.any(0))[0], np.where(m.any(1))[0]
    box = (max(cols[0] - pad, 0), max(rows[0] - pad, 0), min(cols[-1] + pad, a.shape[1] - 1) + 1, min(rows[-1] + pad, a.shape[0] - 1) + 1)
    im.crop(box).save(dst, 'PNG')
    return Image.open(dst).size


def crop_bar(src, dst):
    """막대 (채도 높은 줄) 위아래 4 px 만 — 웹앱 제목 · 눈금 숫자 · 설명 글은 뺀다 (숫자는 편집 가능한 글로 다시 단다)."""
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
gone = [sh for sh in s.shapes if sh.name.startswith(('3D 그림 자리 (웹앱)', '3D 라벨'))]
if len(gone) != 6:
    raise SystemExit(f'7장 자리 · 라벨 {len(gone)} 개 (6 이어야 한다)')
for sh in gone:
    sh._element.getparent().remove(sh._element)
p3d = os.path.join(FIG, 'jcur3d_1um.png')
pcb = os.path.join(FIG, 'jcur_colorbar.png')
w3, h3 = crop_alpha(J3D, p3d)
wb, hb = crop_bar(JCB, pcb)
H = 2.45
W = H * w3 / h3
pic = s.shapes.add_picture(p3d, Inches(0.75), Inches(3.12), height=Inches(H))
pic.name = '이온 전류 3D 1 µm'
textbox(s, '이온 전류 3D 라벨', 0.75, 3.12 + H + 0.02, W, 0.27, [('1 µm', 'n')])
CBW = 2.35
cb = s.shapes.add_picture(pcb, Inches(2.45), Inches(4.20), width=Inches(CBW))
cb.name = '이온 전류 컬러바'
textbox(s, '이온 전류 컬러바 제목', 2.45, 3.88, CBW, 0.27, [('Li', 'n'), ('+', 'sup'), (' current density (A cm', 'n'), ('−2', 'sup'), (')', 'n')])
CBH = CBW * hb / wb
for k, (tx, al) in enumerate(zip(TICKS, (PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.RIGHT))):
    xk = 2.45 + (0, CBW / 2 - 0.4, CBW - 0.8)[k]
    textbox(s, f'이온 전류 컬러바 눈금 {k + 1}', xk, 4.20 + CBH + 0.03, 0.8, 0.22, [(tx, 'n')], size=10, align=al)
notes = [p for p in s.notes_slide.notes_text_frame.paragraphs if p.runs][0]
old = '3D 그림은 같은 계산의 이온 전류 밀도 분포입니다.'
r = [x for x in notes.runs if old in x.text]
if len(r) != 1:
    raise SystemExit('7장 노트 3D 문장 못 찾음')
sel_txt = '모든 전해질–전해질 접촉을 그렸습니다' if SEL == 'all' else '전류의 95 %를 나르는 접촉만 그렸습니다'
r[0].text = r[0].text.replace(old, f'3D 그림은 1 µm 전극에 1 V를 걸었을 때 전해질–전해질 접촉별 이온 전류 밀도이고, {sel_txt}.')
prs.save(DST)
print(f'3D {w3}x{h3} px → {W:.2f} x {H:.2f} in · 컬러바 {wb}x{hb} px → {CBW:.2f} x {CBW * hb / wb:.2f} in')
