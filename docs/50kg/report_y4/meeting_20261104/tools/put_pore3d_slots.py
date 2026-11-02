"""4장 점선 자리 셋 ('3D 그림 자리 (웹앱) 3 µm' · 2 µm · 1 µm) 을 웹앱 기공 3D 그림으로 바꾼다 (1저자 11-02 "이렇게 넣어서 4pg 만들어줘").

usage: python3 -I put_pore3d_slots.py in.pptx out.pptx FIGDIR 3=img 2=img 1=img
  - 그림 = 웹앱 기공 보기 저장본 (RGBA · 바깥 alpha 0) — alpha 로 빈 여백을 잘라 PNG (투명 바탕 그대로) 로 FIGDIR 에 저장
  - 셋을 같은 높이로 (자리 안에 들어가는 가장 큰 공통 높이) · 자리 가운데 · 자리 도형은 지운다
  - 라벨 도형 ('3D 라벨 3 µm' …) 은 1저자 것 그대로 둔다 — 없으면 멈춘다
  - 자리가 정확히 하나씩 없으면 멈춘다 (두 번 돌리면 실패 = 이미 넣음)
"""
import os
import sys

import numpy as np
from PIL import Image
from pptx import Presentation

SLIDE = 4
SLOT = '3D 그림 자리 (웹앱) {} µm'
LABEL = '3D 라벨 {} µm'
IN_ = 914400


def crop_alpha(src, dst, thr=20, pad=14):
    im = Image.open(src).convert('RGBA')
    a = np.asarray(im)
    mask = a[..., 3] > thr
    cols = np.where(mask.any(axis=0))[0]
    rows = np.where(mask.any(axis=1))[0]
    if not len(cols):
        raise SystemExit(f'{src}: 보이는 픽셀 없음')
    x0, x1 = max(cols[0] - pad, 0), min(cols[-1] + pad, a.shape[1] - 1)
    y0, y1 = max(rows[0] - pad, 0), min(rows[-1] + pad, a.shape[0] - 1)
    out = im.crop((x0, y0, x1 + 1, y1 + 1))
    out.save(dst, 'PNG')
    return out.size, (x0, y0, x1, y1)


def main():
    src, dst, figdir = sys.argv[1:4]
    items = dict(a.split('=', 1) for a in sys.argv[4:])
    if sorted(items) != ['1', '2', '3']:
        raise SystemExit('그림 셋 = 3=… 2=… 1=… 이어야 한다')
    os.makedirs(figdir, exist_ok=True)
    prs = Presentation(src)
    s = prs.slides[SLIDE - 1]
    slots, crops = {}, {}
    for k in ('3', '2', '1'):
        hit = [sh for sh in s.shapes if sh.name == SLOT.format(k)]
        lab = [sh for sh in s.shapes if sh.name == LABEL.format(k)]
        if len(hit) != 1 or len(lab) != 1:
            raise SystemExit(f'{SLIDE}장 {k} µm: 자리 {len(hit)} · 라벨 {len(lab)} (각 1 이어야 한다)')
        slots[k] = hit[0]
        png = os.path.join(figdir, f'pore3d_{k}um.png')
        size, box = crop_alpha(items[k], png)
        crops[k] = (png, size)
        print(f'{k} µm: {os.path.basename(items[k])} crop {box} -> {size[0]}x{size[1]} px -> {png}')
    # 공통 높이 = 모든 자리에 들어가는 가장 큰 높이
    h_img = min(min(sl.height, int(sl.width * crops[k][1][1] / crops[k][1][0])) for k, sl in slots.items())
    for k, sl in slots.items():
        png, (pw, ph) = crops[k]
        w_img = int(h_img * pw / ph)
        x = sl.left + (sl.width - w_img) // 2
        y = sl.top + (sl.height - h_img) // 2
        pic = s.shapes.add_picture(png, x, y, width=w_img, height=h_img)
        pic.name = f'기공 3D {k} µm'
        sl._element.getparent().remove(sl._element)
        print(f'{k} µm: 그림 {x/IN_:.3f},{y/IN_:.3f} {w_img/IN_:.3f}x{h_img/IN_:.3f} in')
    prs.save(dst)


if __name__ == '__main__':
    main()
