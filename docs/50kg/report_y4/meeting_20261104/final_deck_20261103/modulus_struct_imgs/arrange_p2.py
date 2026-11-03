# Modulus slide (1저자 6쪽) laid out exactly like the size slide (1저자 2쪽 = template slide 7):
# frame · column labels · tortuosity labels/values · legend · caption take slide-7 geometry; pictures take
# the D1/D2/D3 picture centres with one common width (same scale) and one bottom line; charts = page-2
# Origin boxes (6.98 / 2.94 · 7.11 / 4.79 in) with the page-2-style E_SE PNGs.
import re, sys, shutil, os, zipfile
from PIL import Image
S, U, DECK = sys.argv[1], sys.argv[2], sys.argv[3]
NEW, P2C = S + '/arr_work/new', S + '/arr_work/p2charts'
EMU = 914400
s7 = zipfile.ZipFile(DECK).read('ppt/slides/slide7.xml').decode('utf-8')
sx = open(U + '/ppt/slides/slide1.xml', encoding='utf-8').read()
def find(x, name, tag):
    m = re.search(r'<p:%s>(?:(?!</p:%s>).)*?name="%s".*?</p:%s>' % (tag, tag, re.escape(name), tag), x, re.S)
    assert m, (name, tag); return m
GRE = r'<a:off x="(-?\d+)" y="(-?\d+)"/>\s*<a:ext cx="(\d+)" cy="(\d+)"/>'
def geom(x, name, tag='sp'):
    return tuple(map(int, re.search(GRE, find(x, name, tag).group(0)).groups()))
def set_geom(name, tag, g, keep_ext=False):
    global sx
    m = find(sx, name, tag); b = m.group(0)
    def rep(mm):
        cx, cy = (mm.group(3), mm.group(4)) if keep_ext else (g[2], g[3])
        return '<a:off x="%d" y="%d"/><a:ext cx="%s" cy="%s"/>' % (g[0], g[1], cx, cy)
    b2 = re.sub(GRE, rep, b, count=1)
    sx = sx[:m.start()] + b2 + sx[m.end():]
def edit_block(name, tag, fn):
    global sx
    m = find(sx, name, tag); sx = sx[:m.start()] + fn(m.group(0)) + sx[m.end():]
T = {k: geom(s7, v) for k, v in dict(frame='직사각형 261', l1='TextBox 12', l2='TextBox 14', l3='TextBox 13',
     t1='TextBox 15', t2='TextBox 17', t3='TextBox 18', v1='TextBox 16', v2='TextBox 19', v3='TextBox 20', cap='Text Box 36').items()}
T['leg'] = geom(s7, '그룹 260', 'grpSp')
R = {i: geom(s7, 'Size render D%d' % i, 'pic') for i in (1, 2, 3)}
P = {i: geom(s7, 'Size path D%d' % i, 'pic') for i in (1, 2, 3)}
OLE = {}
for g in re.finditer(r'<p:graphicFrame>.*?</p:graphicFrame>', sx, re.S):
    b = g.group(0)
    if 'presentationml/2006/ole' in b:
        nm = re.search(r'<p:cNvPr [^>]*name="([^"]*)"', b).group(1)
        OLE[nm] = tuple(map(int, re.search(r'<p:xfrm><a:off x="(-?\d+)" y="(-?\d+)"/><a:ext cx="(\d+)" cy="(\d+)"/>', b).groups()))
assert set(OLE) == {'개체 1', '개체 2'}, OLE
rep = []
# frame · labels · tortuosity labels/values · legend · caption
set_geom('직사각형 28', 'sp', T['frame'])
for nm, k in (('TextBox 7', 'l1'), ('TextBox 18', 'l2'), ('TextBox 9', 'l3')):
    set_geom(nm, 'sp', T[k])
    edit_block(nm, 'sp', lambda b: b.replace('rtlCol="0">', 'rtlCol="0" anchor="ctr">', 1) if 'anchor=' not in b.split('</a:bodyPr>')[0][:400] else b)
for i in (1, 2, 3):
    set_geom('Transport tortuosity label %d' % i, 'sp', T['t%d' % i])
    set_geom('Transport tortuosity value %d' % i, 'sp', T['v%d' % i])
    edit_block('Transport tortuosity value %d' % i, 'sp', lambda b: re.sub(r'(<a:pPr[^>]*?)algn="ctr"', r'\1algn="l"', b, count=1))
set_geom('그룹 23', 'grpSp', T['leg'], keep_ext=True)
set_geom('Text Box 36', 'sp', T['cap'])
# pictures: common width = D2 width (E22 bed is the D_SE 2 µm bed); centres = D1/D2/D3 centres; one bottom line
bed_w, path_w = R[2][2], P[2][2]
bed_bot, path_bot = R[2][1] + R[2][3], P[2][1] + P[2][3]
def place(img, i, w, bot, ref):
    pw, ph = Image.open(img).size
    h = round(w * ph / pw); cx = ref[i][0] + ref[i][2] / 2
    return round(cx - w / 2), bot - h, w, h
media = {11: (NEW + '/bed_E11.png', NEW + '/path_E11.png'), 33: (NEW + '/bed_E33.png', NEW + '/path_E33.png')}
col = {11: 1, 22: 2, 33: 3}
next_id = max(int(v) for v in re.findall(r'<p:cNvPr id="(\d+)"', sx)) + 1
rels_new, k = [], 11
def add_media(src):
    global k
    tgt = 'image%d.png' % k; assert not os.path.exists(U + '/ppt/media/' + tgt)
    shutil.copy(src, U + '/ppt/media/' + tgt); rid = 'rId%d' % (k + 100)
    rels_new.append('<Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/%s"/>' % (rid, tgt))
    k += 1; return rid
def pic(name, descr, rid, g):
    global next_id
    s = ('<p:pic><p:nvPicPr><p:cNvPr id="%d" name="%s" descr="%s"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/>'
         '</p:cNvPicPr><p:nvPr/></p:nvPicPr><p:blipFill><a:blip r:embed="%s"/><a:stretch><a:fillRect/></a:stretch>'
         '</p:blipFill><p:spPr><a:xfrm><a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/></a:xfrm><a:prstGeom prst="rect">'
         '<a:avLst/></a:prstGeom></p:spPr></p:pic>') % ((next_id, name, descr, rid) + tuple(g))
    next_id += 1; return s
# E22 pictures already in the slide: same rule (image size from their media)
r = open(U + '/ppt/slides/_rels/slide1.xml.rels', encoding='utf-8').read()
def media_of(name):
    rid = re.search(r'<a:blip r:embed="([^"]+)"', find(sx, name, 'pic').group(0)).group(1)
    return U + '/ppt/' + re.search(r'Id="%s"[^>]*Target="\.\./([^"]+)"' % rid, r).group(1)
g = place(media_of('Structure E22'), 2, bed_w, bed_bot, R); set_geom('Structure E22', 'pic', g); rep.append(('E22 bed', g))
g = place(media_of('Tortuosity path E22'), 2, path_w, path_bot, P); set_geom('Tortuosity path E22', 'pic', g); rep.append(('E22 path', g))
new_pics = []
for e in (11, 33):
    g = place(media[e][0], col[e], bed_w, bed_bot, R); rep.append(('E%d bed' % e, g))
    new_pics.append(pic('Structure E%d' % e, 'E_SE %d GPa composite cathode structure (black = NCM, beige = SE)' % e, add_media(media[e][0]), g))
    g = place(media[e][1], col[e], path_w, path_bot, P); rep.append(('E%d path' % e, g))
    new_pics.append(pic('Tortuosity path E%d' % e, 'E_SE %d GPa shortest ion path through SE' % e, add_media(media[e][1]), g))
first = None
for nm in ('Image slot E11', 'Image slot path 1', 'Image slot E33', 'Image slot path 3'):
    m = find(sx, nm, 'sp'); first = m.start() if first is None else min(first, m.start()); sx = sx[:m.start()] + sx[m.end():]
sx = sx[:first] + ''.join(new_pics) + sx[first:]
# charts: page-2-style E_SE PNGs into the page-2 Origin boxes
gfs = [m for m in re.finditer(r'<p:graphicFrame>.*?</p:graphicFrame>', sx, re.S) if 'presentationml/2006/ole' in m.group(0)]
pos = gfs[0].start()
for gg in reversed(gfs): sx = sx[:gg.start()] + sx[gg.end():]
charts = (pic('Thickness vs E_SE', 'Thickness (um) at E_SE 11 / 22 / 33 GPa: 123.6 / 126.8 / 129.4', add_media(P2C + '/p2s_thickness_ESE.png'), OLE['개체 2']) +
          pic('Porosity vs E_SE', 'Porosity (%) at E_SE 11 / 22 / 33 GPa: 17.5 / 19.6 / 21.2', add_media(P2C + '/p2s_porosity_ESE.png'), OLE['개체 1']))
sx = sx[:pos] + charts + sx[pos:]
assert 'graphicFrame' not in sx and 'oleObj' not in sx
open(U + '/ppt/slides/slide1.xml', 'w', encoding='utf-8').write(sx)
for rid in ('rId7', 'rId8', 'rId9', 'rId10'):
    assert ('r:id="%s"' % rid) not in sx and ('r:embed="%s"' % rid) not in sx
    r, n = re.subn(r'<Relationship Id="%s"[^>]*/>' % rid, '', r); assert n == 1
open(U + '/ppt/slides/_rels/slide1.xml.rels', 'w', encoding='utf-8').write(r.replace('</Relationships>', ''.join(rels_new) + '</Relationships>'))
npth = U + '/ppt/notesSlides/notesSlide1.xml'; n = open(npth, encoding='utf-8').read()
old = '22 GPa 구조 그림 = D_SE 2 µm 와 같은 침대 · 11 · 33 GPa 그림 = 대기.'
new = ('그림 · 글자 자리 = 입도 장 (2쪽) 과 같음 · 구조 · 경로 그림 = 세 칸 같은 가로 폭 (같은 배율) · 아래 맞춤 → 높이 차 = 두께 차. '
       '22 GPa = D_SE 2 µm 와 같은 침대. 11 · 33 GPa 구조 그림 = 22 GPa 그림 (밝기 +20 % · 대비 +20 %) 과 같은 색감. '
       '그래프 = 입도 장과 같은 칸 크기 · 축 범위 (두께 115–135 µm · 기공도 15–24 %).')
assert n.count(old) == 1; open(npth, 'w', encoding='utf-8').write(n.replace(old, new))
for nm, g in rep: print('%-9s x=%.3f y=%.3f w=%.3f h=%.3f bottom=%.3f' % ((nm,) + tuple(v / EMU for v in g) + ((g[1] + g[3]) / EMU,)))
print('charts', {k_: tuple(round(v / EMU, 3) for v in g_) for k_, g_ in OLE.items()})
