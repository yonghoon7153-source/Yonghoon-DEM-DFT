#!/usr/bin/env python3
"""Figure 1(b) — network-solver schematic as an EDITABLE .pptx.

Geometry comes from scripts/network_schematic_data.py (shared with the
matplotlib preview) so the .pptx matches the PNG exactly.  Every particle
is a real PowerPoint OVAL; every resistor is a real zigzag FREEFORM line.
Edge colors are computed from endpoint phases (yellow SE-SE / blue AM-SE /
red AM-AM) so they cannot be wrong.  Edit any shape by hand in PowerPoint.

Run:  python3 scripts/make_network_pptx.py
Out:  docs/figures/network_solver_schematic.pptx
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

from network_schematic_data import build, spring

def C(h): return RGBColor.from_string(h)
C_SE, C_SE_E = C('F6C623'), C('C08A0A')
C_AM, C_AM_E = C('9B9B9B'), C('3F3F3F')
E_SESE, E_AMSE, E_AMAM = C('F3BF1E'), C('3F7FD0'), C('E22B2B')
BB_Y, BB_R = C('F5A800'), C('EE1111')
SUS_FC, SUS_EC = C('E8807F'), C('C64A4A')
BULK_FC, BULK_EC = C('E8D3A0'), C('B89030')

D = build()
nodes = D['nodes']; edges = D['edges']
se_chain = D['se_chain']; am_chain = D['am_chain']
cc = D['consts']
X0, X1 = cc['X0'], cc['X1']
SUS_Y, BULK_Y = cc['SUS_Y'], cc['BULK_Y']

# ── data-coord → slide inches (equal x/y scale → circles stay round) ──
S = 0.62
MX, MY = 0.35, 0.30
def sx(x): return MX + x * S
def sy(y): return MY + (11 - y) * S
EMU = 914400
def E(inch): return Emu(int(round(inch * EMU)))

prs = Presentation()
prs.slide_width = Inches(13.33); prs.slide_height = Inches(7.5)
slide = prs.slides.add_slide(prs.slide_layouts[6])
shapes = slide.shapes

def add_bar(y_top, y_bot, fc, ec):
    sh = shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                          E(sx(X0-0.2)), E(sy(y_top)),
                          E((X1-X0+0.4)*S), E((y_top-y_bot)*S))
    sh.fill.solid(); sh.fill.fore_color.rgb = fc
    sh.line.color.rgb = ec; sh.line.width = Pt(1.5); sh.shadow.inherit = False
add_bar(SUS_Y+0.9, SUS_Y, SUS_FC, SUS_EC)
add_bar(BULK_Y, BULK_Y-0.9, BULK_FC, BULK_EC)

def add_spring(pts, color, width_pt):
    flat = [(E(sx(px)), E(sy(py))) for (px, py) in pts]
    fb = shapes.build_freeform(flat[0][0], flat[0][1], scale=1.0)
    fb.add_line_segments(flat[1:], close=False)
    sh = fb.convert_to_shape()
    sh.fill.background(); sh.line.color.rgb = color
    sh.line.width = Pt(width_pt); sh.shadow.inherit = False

for a, b in edges['AM-AM']: add_spring(spring((a[0],a[1]),(b[0],b[1])), E_AMAM, 1.6)
for a, b in edges['AM-SE']: add_spring(spring((a[0],a[1]),(b[0],b[1])), E_AMSE, 1.5)
for a, b in edges['SE-SE']: add_spring(spring((a[0],a[1]),(b[0],b[1])), E_SESE, 1.4)

for chain, col in [(se_chain, BB_Y), (am_chain, BB_R)]:
    for m in range(len(chain)-1):
        add_spring(spring(chain[m], chain[m+1]), col, 3.4)

def add_node(x, y, ph, r, bb):
    fc, ec = (C_SE, C_SE_E) if ph == 'SE' else (C_AM, C_AM_E)
    d = E(2*r*S)
    sh = shapes.add_shape(MSO_SHAPE.OVAL, E(sx(x)-r*S), E(sy(y)-r*S), d, d)
    sh.fill.solid(); sh.fill.fore_color.rgb = fc
    sh.line.color.rgb = ec; sh.line.width = Pt(1.6 if bb else 1.0); sh.shadow.inherit = False
for (x, y, ph, r, bb) in nodes: add_node(x, y, ph, r, bb)

def add_X(xc, yc, color, half=0.28):
    for p, q in [((xc-half, yc-half), (xc+half, yc+half)),
                 ((xc-half, yc+half), (xc+half, yc-half))]:
        add_spring([p, q], color, 4.0)
sx_, sy_ = se_chain[-1]; add_X(sx_, sy_+0.75, BB_Y)
ax_, ay_ = am_chain[-1]; add_X(ax_, ay_-0.75, BB_R)

# ── legend ──
LX, LY, LW, LH = 9.0, 0.5, 4.0, 6.6
box = shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(LX), Inches(LY), Inches(LW), Inches(LH))
box.fill.solid(); box.fill.fore_color.rgb = C('FFFFFF')
box.line.color.rgb = C('333333'); box.line.width = Pt(1.4); box.shadow.inherit = False

def txt(x, y, s, size=12, bold=False):
    tb = shapes.add_textbox(Inches(x), Inches(y), Inches(3.6), Inches(0.35))
    p = tb.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
    run = p.add_run(); run.text = s
    run.font.size = Pt(size); run.font.bold = bold; run.font.color.rgb = C('222222')

def leg_oval(x, y, fc, ec, d=0.26):
    sh = shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
    sh.fill.solid(); sh.fill.fore_color.rgb = fc
    sh.line.color.rgb = ec; sh.line.width = Pt(1.2); sh.shadow.inherit = False

def leg_zig(x, y, color, w=2.0):
    pts = [(x, y), (x+0.12, y-0.07), (x+0.24, y+0.07), (x+0.36, y-0.07), (x+0.48, y+0.07), (x+0.60, y)]
    flat = [(E(px), E(py)) for (px, py) in pts]
    fb = shapes.build_freeform(flat[0][0], flat[0][1], scale=1.0)
    fb.add_line_segments(flat[1:], close=False)
    sh = fb.convert_to_shape(); sh.fill.background()
    sh.line.color.rgb = color; sh.line.width = Pt(w); sh.shadow.inherit = False

txt(LX+0.25, LY+0.15, 'NODES', 13, True)
leg_oval(LX+0.35, LY+0.65, C_SE, C_SE_E);       txt(LX+0.9, LY+0.62, 'yellow = SE (ionic, majority matrix)', 11)
leg_oval(LX+0.32, LY+1.12, C_AM, C_AM_E, 0.33); txt(LX+0.9, LY+1.12, 'gray = AM (electronic, minority islands)', 11)
txt(LX+0.25, LY+1.75, 'CONTACTS (resistors)', 13, True)
leg_zig(LX+0.35, LY+2.30, E_SESE); txt(LX+1.15, LY+2.18, 'yellow = SE-SE', 11)
leg_zig(LX+0.35, LY+2.72, E_AMSE); txt(LX+1.15, LY+2.60, 'blue  = AM-SE', 11)
leg_zig(LX+0.35, LY+3.14, E_AMAM); txt(LX+1.15, LY+3.02, 'red   = AM-AM', 11)
txt(LX+0.25, LY+3.75, 'BACKBONES', 13, True)
leg_zig(LX+0.35, LY+4.30, BB_Y, 3.0); txt(LX+1.15, LY+4.18, 'yellow → bulk (Li+ path); X = no SE to SUS', 10)
leg_zig(LX+0.35, LY+4.78, BB_R, 3.0); txt(LX+1.15, LY+4.66, 'red → SUS (e- path); X = no AM to bulk', 10)

import os; os.makedirs('docs/figures', exist_ok=True)
out = 'docs/figures/network_solver_schematic.pptx'
prs.save(out)
print(f"saved: {out}  nodes={len(nodes)} AM-AM={len(edges['AM-AM'])} "
      f"AM-SE={len(edges['AM-SE'])} SE-SE={len(edges['SE-SE'])}")
