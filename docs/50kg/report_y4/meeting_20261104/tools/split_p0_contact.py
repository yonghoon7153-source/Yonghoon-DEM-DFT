"""3장 오른쪽 접촉 모델 그림 (p0_contact_model_labeled) 을 네 조각으로 따로 그린다 — 1저자 11-02 "지배방정식 부분 그림 각각 독립적으로 떼서".
리포 생성기 (docs/50kg/report_y4/figs/make_fig_p0_dem_method.py) 의 panel_a–d · 저장 상태 JSON 을 읽기만 한다 (render_all 안 부름 = 리포 그림 안 덮어씀).
바꾸는 것 하나: 그림 안 한글 '미끄럼' → 'slip' (1저자 규칙 "그림 안 글 = 영문").
usage: python3 -I split_p0_contact.py <repo> <outdir>
출력: 조각 PNG 4 (300 dpi · 투명) + 합친 그림 (대조용) + layout.json (조각마다 합친 그림 안 위치 · in)
"""
import importlib.util
import json
import os
import sys

import numpy as np

REPO, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
gen_path = os.path.join(REPO, 'docs/50kg/report_y4/figs/make_fig_p0_dem_method.py')
spec = importlib.util.spec_from_file_location('p0gen', gen_path)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
state = json.load(open(g.STATE))
snaps, meta = state['snaps'], state['meta']
g.CTX.update(snaps=snaps, r=np.array(meta['r']), am=np.array(meta['am']))
I, J, FN, ANG = g.pick_pair(snaps, meta)
sn = snaps['compress']
g.CTX.update(x=np.array(sn['x']), py=sn['plate_y'], C=sn['contacts'], fmax=max(c[2] for c in sn['contacts']), I=I, J=J)

plt = g._mpl()
# 덱에 들어간 예전 그림은 Carlito 가 없는 환경에서 그려졌다 (글 = WenQuanYi · 수식 = DejaVu Sans 대체) — 같은 모양으로 맞춘다
plt.rcParams.update({'font.family': ['WenQuanYi Zen Hei', 'DejaVu Sans'], 'mathtext.it': 'DejaVu Sans:italic',
                     'mathtext.rm': 'DejaVu Sans', 'mathtext.bf': 'DejaVu Sans:bold'})
FW, FH = 4.50, 2.75
fig = plt.figure(figsize=(FW, FH), dpi=300)
axa = fig.add_axes([0.0, 0.30, 0.52, 0.70]); n, t = g.panel_a(axa, True)
axb = fig.add_axes([0.55, 0.36, 0.43, 0.60]); g.panel_b(axb, n, True)
axc = fig.add_axes([0.10, 0.06, 0.32, 0.22]); g.panel_c(axc, True)
axd = fig.add_axes([0.62, 0.06, 0.32, 0.22]); g.panel_d(axd, True)
kor = [tx for tx in axd.texts if tx.get_text() == '미끄럼']
assert len(kor) == 1, kor
kor[0].set_text('slip')
fig.savefig(os.path.join(OUT, 'p0_contact_model_labeled_slip.png'), dpi=300, transparent=True)

fig.canvas.draw()
rend = fig.canvas.get_renderer()
axes = {'a_particles': axa, 'b_contact': axb, 'c_normal': axc, 'd_tangential': axd}
layout = {}
PAD = 0.03
from matplotlib.transforms import Bbox
boxes = {}
for name, ax in axes.items():                     # 다 보이는 상태에서 먼저 잰다 (안 보이는 축은 tightbbox 가 None)
    bb = ax.get_tightbbox(rend).transformed(fig.dpi_scale_trans.inverted())
    boxes[name] = (max(bb.x0 - PAD, 0.0), max(bb.y0 - PAD, 0.0), min(bb.x1 + PAD, FW), min(bb.y1 + PAD, FH))
for name, ax in axes.items():
    x0, y0, x1, y1 = boxes[name]
    box = Bbox([[x0, y0], [x1, y1]])
    for other in axes.values():
        other.set_visible(other is ax)
    fig.savefig(os.path.join(OUT, f'p0_{name}.png'), dpi=300, transparent=True, bbox_inches=box, pad_inches=0)
    layout[name] = dict(x0=x0, y0=y0, x1=x1, y1=y1)
for other in axes.values():
    other.set_visible(True)
json.dump(dict(fig_w_in=FW, fig_h_in=FH, panels=layout, pair=[int(I), int(J)]), open(os.path.join(OUT, 'layout.json'), 'w'), indent=1)
print(json.dumps(layout, indent=0))
