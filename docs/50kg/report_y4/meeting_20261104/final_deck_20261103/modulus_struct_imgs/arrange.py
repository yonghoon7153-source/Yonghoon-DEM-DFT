# Fill the 11 / 33 GPa columns of the modulus slide at the same scale as the 22 GPa pictures
# (same width = same scale, bottom-aligned) and swap the two D_SE charts for the E_SE charts,
# stacked to the frame height with their y axes aligned.
import re, sys, shutil, os
import numpy as np
from PIL import Image
S, U = sys.argv[1], sys.argv[2]
KEEP_CHARTS = '--keep-charts' in sys.argv[3:]   # 1저자 11-03: 두께 · 기공도 그래프는 1저자가 직접 바꿈
NEW, CH = S + '/arr_work/new', S + '/final_out/charts'
sx = open(U + '/ppt/slides/slide1.xml', encoding='utf-8').read()
EMU = 914400

def block(name, tag):
    m = re.search(r'<p:%s>(?:(?!</p:%s>).)*?name="%s".*?</p:%s>' % (tag, tag, re.escape(name), tag), sx, re.S)
    assert m, name
    return m

def geom(name, tag='sp'):
    b = block(name, tag).group(0)
    x, y, cx, cy = map(int, re.search(r'<a:off x="(-?\d+)" y="(-?\d+)"/>\s*<a:ext cx="(\d+)" cy="(\d+)"', b).groups())
    return x, y, cx, cy

lab = {11: geom('TextBox 7'), 22: geom('TextBox 18'), 33: geom('TextBox 9')}
tl = {11: geom('Transport tortuosity label 1'), 22: geom('Transport tortuosity label 2'), 33: geom('Transport tortuosity label 3')}
bed22, path22, frame = geom('Structure E22', 'pic'), geom('Tortuosity path E22', 'pic'), geom('직사각형 28')
bed_dx = bed22[0] - lab[22][0]
bed_w, bed_bot = bed22[2], bed22[1] + bed22[3]
path_w, path_bot = path22[2], path22[1] + path22[3]
assert abs((path22[0] + path22[2] / 2) - (tl[22][0] + tl[22][2] / 2)) < 0.02 * EMU   # 22 GPa path sits under its label

next_id = max(int(v) for v in re.findall(r'<p:cNvPr id="(\d+)"', sx)) + 1
rels_new, pics_cols, k = [], [], 11
def pic(name, descr, rid, x, y, cx, cy):
    global next_id
    s = ('<p:pic><p:nvPicPr><p:cNvPr id="%d" name="%s" descr="%s"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/>'
         '</p:cNvPicPr><p:nvPr/></p:nvPicPr><p:blipFill><a:blip r:embed="%s"/><a:stretch><a:fillRect/></a:stretch>'
         '</p:blipFill><p:spPr><a:xfrm><a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/></a:xfrm><a:prstGeom prst="rect">'
         '<a:avLst/></a:prstGeom></p:spPr></p:pic>') % (next_id, name, descr, rid, x, y, cx, cy)
    next_id += 1
    return s
def add_media(src):
    global k
    tgt = 'image%d.png' % k
    assert not os.path.exists(U + '/ppt/media/' + tgt)
    shutil.copy(src, U + '/ppt/media/' + tgt)
    rid = 'rId%d' % (k + 100)
    rels_new.append('<Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/%s"/>' % (rid, tgt))
    k += 1
    return rid
report = []
for e in (11, 33):
    bw, bh = Image.open('%s/bed_E%d.png' % (NEW, e)).size
    pw, ph = Image.open('%s/path_E%d.png' % (NEW, e)).size
    bx = lab[e][0] + bed_dx; bcy = round(bed_w * bh / bw); by = bed_bot - bcy
    pcx = tl[e][0] + tl[e][2] / 2; pcyy = round(path_w * ph / pw); py = path_bot - pcyy; px = round(pcx - path_w / 2)
    pics_cols.append(pic('Structure E%d' % e, 'E_SE %d GPa composite cathode structure (black = NCM, beige = SE)' % e,
                         add_media('%s/bed_E%d.png' % (NEW, e)), bx, by, bed_w, bcy))
    pics_cols.append(pic('Tortuosity path E%d' % e, 'E_SE %d GPa shortest ion path through SE' % e,
                         add_media('%s/path_E%d.png' % (NEW, e)), px, py, path_w, pcyy))
    report.append('E%d bed x=%.3f y=%.3f w=%.3f h=%.3f | path x=%.3f y=%.3f w=%.3f h=%.3f' % (
        e, bx / EMU, by / EMU, bed_w / EMU, bcy / EMU, px / EMU, py / EMU, path_w / EMU, pcyy / EMU))
report.append('E22 bed x=%.3f y=%.3f w=%.3f h=%.3f | path x=%.3f y=%.3f w=%.3f h=%.3f' % tuple(v / EMU for v in bed22 + path22))

# drop the four dashed slots; put the new pictures where the first slot was (same z-order)
first = None
for nm in ('Image slot E11', 'Image slot path 1', 'Image slot E33', 'Image slot path 3'):
    m = block(nm, 'sp'); first = m.start() if first is None else min(first, m.start())
    sx = sx[:m.start()] + sx[m.end():]
sx = sx[:first] + ''.join(pics_cols) + sx[first:]

# charts: E_SE thickness (top) + porosity (bottom), same scale, stacked to the frame height, y axes aligned
def axis_px(p):
    g = np.asarray(Image.open(p).convert('L')) < 110
    best, bx_ = 0, 0
    for x in range(g.shape[1] // 2):
        col = g[:, x]; run = cur = 0
        for v in col:
            cur = cur + 1 if v else 0; run = max(run, cur)
        if run > best: best, bx_ = run, x
    return bx_
th, po = CH + '/p12_thickness_ESE.png', CH + '/p12_porosity_ESE.png'
(tw, thh), (pw_, phh) = Image.open(th).size, Image.open(po).size
if not KEEP_CHARTS:
    dpi = 300.0
    fx, fy, fcx, fcy = frame
    s = 1.0                                           # native size = same as the template deck (slide 11: 2.29 x 1.604 / 2.213 x 1.846 in)
    def abox(p):
        a = np.asarray(Image.open(p).convert('RGBA'))[..., 3] > 8
        ys, xs = np.where(a); return ys.min(), ys.max() + 1
    ax_t, ax_p = axis_px(th), axis_px(po)
    t_cx, t_cy = round(tw / dpi * EMU), round(thh / dpi * EMU)
    p_cx, p_cy = round(pw_ / dpi * EMU), round(phh / dpi * EMU)
    x0 = round(7.042 * EMU)                           # template x of the thickness chart
    xp = x0 + round((ax_t - ax_p) / dpi * EMU)        # porosity shifted so the two y axes line up
    t_top, _ = abox(th); _, p_bot = abox(po)
    yt = fy - round(t_top / dpi * EMU)                # visible top of thickness chart = frame top
    yp = (fy + fcy) - round(p_bot / dpi * EMU)        # visible bottom of porosity chart = frame bottom
    charts = (pic('Thickness vs E_SE', 'Thickness (um) at E_SE 11 / 22 / 33 GPa: 123.6 / 126.8 / 129.4', add_media(th), x0, yt, t_cx, t_cy) +
              pic('Porosity vs E_SE', 'Porosity (%) at E_SE 11 / 22 / 33 GPa: 17.5 / 19.6 / 21.2', add_media(po), xp, yp, p_cx, p_cy))
    report.append('charts axis px t=%d p=%d | thick x=%.3f y=%.3f w=%.3f h=%.3f (bottom %.3f) | poro x=%.3f y=%.3f w=%.3f h=%.3f | frame y %.3f-%.3f' % (
        ax_t, ax_p, x0 / EMU, yt / EMU, t_cx / EMU, t_cy / EMU, (yt + t_cy) / EMU, xp / EMU, yp / EMU, p_cx / EMU, p_cy / EMU, fy / EMU, (fy + fcy) / EMU))
    gfs = [m for m in re.finditer(r'<p:graphicFrame>.*?</p:graphicFrame>', sx, re.S) if 'presentationml/2006/ole' in m.group(0)]
    assert len(gfs) == 2, len(gfs)
    pos = gfs[0].start()
    for g in reversed(gfs): sx = sx[:g.start()] + sx[g.end():]
    sx = sx[:pos] + charts + sx[pos:]
    assert 'graphicFrame' not in sx and 'oleObj' not in sx
open(U + '/ppt/slides/slide1.xml', 'w', encoding='utf-8').write(sx)

rp = U + '/ppt/slides/_rels/slide1.xml.rels'
r = open(rp, encoding='utf-8').read()
for rid in (() if KEEP_CHARTS else ('rId7', 'rId8', 'rId9', 'rId10')):
    assert ('r:id="%s"' % rid) not in sx and ('r:embed="%s"' % rid) not in sx
    r, n = re.subn(r'<Relationship Id="%s"[^>]*/>' % rid, '', r); assert n == 1
r = r.replace('</Relationships>', ''.join(rels_new) + '</Relationships>')
open(rp, 'w', encoding='utf-8').write(r)

npth = U + '/ppt/notesSlides/notesSlide1.xml'
n = open(npth, encoding='utf-8').read()
old = '22 GPa 구조 그림 = D_SE 2 µm 와 같은 침대 · 11 · 33 GPa 그림 = 대기.'
new = ('구조 · 경로 그림 = 세 칸 같은 가로 폭 (같은 배율) · 아래 맞춤 → 높이 차 = 두께 차. 22 GPa = D_SE 2 µm 와 같은 침대. '
       '11 · 33 GPa 구조 그림 = 22 GPa 그림 (밝기 +20 % · 대비 +20 %) 과 같은 색감으로 맞춤.')
assert n.count(old) == 1
n = n.replace(old, new)
open(npth, 'w', encoding='utf-8').write(n)
print('\n'.join(report))
