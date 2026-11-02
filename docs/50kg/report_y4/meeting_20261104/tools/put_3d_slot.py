"""점선 자리 '3D 그림 자리 (웹앱)' 를 웹앱 3D 그림 셋으로 바꾼다 (진도점검 덱 · 1저자 11-02 "이걸로 넣고").

usage: python3 -I put_3d_slot.py in.pptx out.pptx SLIDE_NO FIGDIR LABEL1=img1 LABEL2=img2 LABEL3=img3
  - 그림 순서 = 왼쪽부터 (규칙: 3 → 2 → 1 µm)
  - 흰 여백을 잘라 PNG 로 FIGDIR 에 저장 · 셋을 같은 높이로 · 아래 라벨 (KoPubWorld돋움체 Medium 10.5 pt)
  - 점선 자리는 지운다 (자리 크기 · 위치 = 그림 영역)
"""
import os
import sys

import numpy as np
from PIL import Image
from pptx import Presentation
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Pt

SLOT = '3D 그림 자리 (웹앱)'
FONT = 'KoPubWorld돋움체 Medium'
IN_ = 914400


def crop_white(src, dst, thr=235, frac=0.004, pad=14):
    """빈 여백을 잘라낸다 — 투명 배경 (웹앱 저장본 = RGBA, 바깥 alpha 0) 이면 alpha 로, 아니면 흰색 기준."""
    im = Image.open(src)
    if im.mode in ('RGBA', 'LA') or 'transparency' in im.info:
        im = im.convert('RGBA')
        a = np.asarray(im)
        mask = a[..., 3] > 20
    else:
        im = im.convert('RGB')
        a = np.asarray(im)
        mask = a.min(axis=2) < thr
    cols = np.where(mask.mean(axis=0) > frac)[0]
    rows = np.where(mask.mean(axis=1) > frac)[0]
    x0, x1 = max(cols[0] - pad, 0), min(cols[-1] + pad, a.shape[1] - 1)
    y0, y1 = max(rows[0] - pad, 0), min(rows[-1] + pad, a.shape[0] - 1)
    out = im.crop((x0, y0, x1 + 1, y1 + 1))
    out.save(dst, 'PNG')
    return out.size, (x0, y0, x1, y1)


def set_font(run, name, size_pt):
    run.font.size = Pt(size_pt)
    rpr = run._r.get_or_add_rPr()
    for tag in ('a:latin', 'a:ea', 'a:cs'):
        el = rpr.find(qn(tag))
        if el is None:
            el = rpr.makeelement(qn(tag), {})
            rpr.append(el)
        el.set('typeface', name)


def main():
    src, dst, slide_no, figdir = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
    items = [a.split('=', 1) for a in sys.argv[5:]]
    os.makedirs(figdir, exist_ok=True)
    prs = Presentation(src)
    s = prs.slides[slide_no - 1]
    slots = [sh for sh in s.shapes if sh.name == SLOT]
    if len(slots) != 1:
        raise SystemExit(f'slide {slide_no}: 점선 자리 {len(slots)} 개 (1 이어야 한다)')
    slot = slots[0]
    X, Y, W, H = slot.left, slot.top, slot.width, slot.height
    slot._element.getparent().remove(slot._element)

    crops = []
    for k, (label, path) in enumerate(items, 1):
        png = os.path.join(figdir, f'3d_s{slide_no}_{k}.png')
        size, box = crop_white(path, png)
        crops.append((label, png, size, box))
        print(f'{label}: {os.path.basename(path)} crop {box} -> {size[0]}x{size[1]} px')

    gap = int(0.10 * IN_)
    label_h = int(0.27 * IN_)
    col_w = (W - gap * (len(crops) - 1)) // len(crops)
    area_h = H - label_h
    h_img = min([area_h] + [int(col_w * sz[1] / sz[0]) for _, _, sz, _ in crops])
    y_img = Y + (area_h - h_img) // 2
    for k, (label, png, sz, _) in enumerate(crops):
        w_img = int(h_img * sz[0] / sz[1])
        x_col = X + k * (col_w + gap)
        pic = s.shapes.add_picture(png, x_col + (col_w - w_img) // 2, y_img, width=w_img, height=h_img)
        pic.name = f'3D 그림 {label}'
        tb = s.shapes.add_textbox(x_col, y_img + h_img + int(0.02 * IN_), col_w, label_h)
        tb.name = f'3D 라벨 {label}'
        tf = tb.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = label
        set_font(r, FONT, 10.5)
    print(f'slot {X/IN_:.2f},{Y/IN_:.2f} {W/IN_:.2f}x{H/IN_:.2f} in · image h {h_img/IN_:.2f} in · col {col_w/IN_:.2f} in')
    prs.save(dst)


if __name__ == '__main__':
    main()
