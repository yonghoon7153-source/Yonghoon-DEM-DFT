"""3장 오른쪽 합친 접촉 모델 그림 (Picture 4) → 네 조각 그림 (같은 배율 · 같은 배치 · 각각 따로 움직일 수 있게).
usage: python3 -I place_p0_panels.py in.pptx out.pptx <panel_dir>   (panel_dir = split_p0_contact.py 출력 · layout.json)
"""
import json
import os
import sys

from PIL import Image
from pptx import Presentation
from pptx.util import Emu

SRC, DST, PD = sys.argv[1:4]
IN = 914400
L = json.load(open(os.path.join(PD, 'layout.json')))
prs = Presentation(SRC)
s = prs.slides[2]
old = [sh for sh in s.shapes if sh.name == 'Picture 4' and sh.shape_type == 13]
assert len(old) == 1
pic = old[0]
assert pic.image.size == (1350, 825), pic.image.size              # 합친 그림 (4.50 × 2.75 in @300 dpi)
X, Y, W, H = pic.left, pic.top, pic.width, pic.height
sc = W / (L['fig_w_in'] * IN)
assert abs(H - L['fig_h_in'] * IN * sc) < 0.01 * IN, '가로세로비 다름'
pic._element.getparent().remove(pic._element)
names = {'a_particles': '접촉 모델 ① 입자 힘', 'b_contact': '접촉 모델 ② 접촉 요소',
         'c_normal': '접촉 모델 ③ 법선 힘', 'd_tangential': '접촉 모델 ④ 접선 힘'}
for key, nm in names.items():
    b = L['panels'][key]
    png = os.path.join(PD, f'p0_{key}.png')
    w_in, h_in = b['x1'] - b['x0'], b['y1'] - b['y0']
    px = Image.open(png).size
    assert abs(px[0] - w_in * 300) <= 2 and abs(px[1] - h_in * 300) <= 2, (key, px, w_in, h_in)
    left = X + int(b['x0'] * IN * sc)
    top = Y + int((L['fig_h_in'] - b['y1']) * IN * sc)
    p = s.shapes.add_picture(png, Emu(left), Emu(top), Emu(int(w_in * IN * sc)), Emu(int(h_in * IN * sc)))
    p.name = nm
    print(f'{nm}: x={left / IN:.2f} y={top / IN:.2f} w={w_in * sc:.2f} h={h_in * sc:.2f} in · {px[0]}×{px[1]} px')
prs.save(DST)
