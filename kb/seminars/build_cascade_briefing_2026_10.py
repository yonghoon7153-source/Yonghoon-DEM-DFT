#!/usr/bin/env python3
"""Build the 2026-10-13 cascade progress-briefing deck by editing the user's 2026-08-18 deck.

Keeps the lab template (layout 2 header line, Hanyang logo, footer, slide numbers) by
duplicating slide 3 for new slides (pptx skill add_slide.py) and editing slide XML.

Usage: python3 build_deck.py <src.pptx> <out.pptx> <skill_dir> <extra_media_dir>
What this does NOT do: speaker notes; native charts (graphs are drawn in Origin from the
per-page CSVs); it does not check that numbers match the ledger (they were checked by hand).
"""
import os, re, shutil, subprocess, sys, zipfile
from xml.sax.saxutils import escape
from lxml import etree

SRC, OUT, SKILL, EXTRA = sys.argv[1:5]
WORK = os.path.join(os.path.dirname(os.path.abspath(OUT)), 'un_build')
NS = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
      'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
RELNS = 'http://schemas.openxmlformats.org/package/2006/relationships'
IMG_T = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image'
E = lambda inch: int(round(inch * 914400))

# ---------------------------------------------------------------- text helpers
FONT = ('<a:latin typeface="Calibri" panose="020F0502020204030204" pitchFamily="34" charset="0"/>'
        '<a:ea typeface="-윤고딕340" pitchFamily="18" charset="-127"/>'
        '<a:cs typeface="Calibri" panose="020F0502020204030204" pitchFamily="34" charset="0"/>')
INK, NAVY, RED, BLUE, MUTED, BUL = '1F2937', '1F497D', 'FF5050', '0070C0', '6B7280', 'A50021'


def col(c):
    if c == 'bg1':
        return '<a:schemeClr val="bg1"/>'
    if c == 'head':
        return '<a:schemeClr val="bg1"><a:lumMod val="75000"/><a:lumOff val="25000"/></a:schemeClr>'
    return f'<a:srgbClr val="{c}"/>'


TOK = re.compile(r'\[\[([rbBnmiuo_^]):(.*?)\]\]')


def runs(markup, sz=None, color='bg1', bold=False, italic=False):
    """[[r:red]] [[b:blue]] [[B:bold]] [[n:navy bold]] [[m:muted]] [[i:italic]] [[_:sub]] [[^:sup]]"""
    out, pos = [], 0
    segs = []
    for m in TOK.finditer(markup):
        if m.start() > pos:
            segs.append(('', markup[pos:m.start()]))
        segs.append((m.group(1), m.group(2)))
        pos = m.end()
    if pos < len(markup):
        segs.append(('', markup[pos:]))
    for k, t in segs:
        c, b, i, base = color, bold, italic, None
        if k == 'r': c = RED
        elif k == 'b': c = BLUE
        elif k == 'B': b = True
        elif k == 'n': c, b = NAVY, True
        elif k == 'm': c = MUTED
        elif k == 'i': i = True
        elif k == '_': base = '-25000'
        elif k == '^': base = '30000'
        a = ['kumimoji="1"', 'lang="en-US"', 'altLang="ko-KR"']
        if sz: a.append(f'sz="{sz}"')
        if b: a.append('b="1"')
        if i: a.append('i="1"')
        if base: a.append(f'baseline="{base}"')
        a.append('dirty="0"')
        out.append(f'<a:r><a:rPr {" ".join(a)}><a:solidFill>{col(c)}</a:solidFill>{FONT}</a:rPr>'
                   f'<a:t>{escape(t)}</a:t></a:r>')
    return ''.join(out)


def P(markup, kind='b', sz=1500, ln=150, algn=None, color=None, bold=False, italic=False,
      spcbef=0, spcaft=0):
    sp = ''
    if spcbef: sp += f'<a:spcBef><a:spcPts val="{spcbef}"/></a:spcBef>'
    if spcaft: sp += f'<a:spcAft><a:spcPts val="{spcaft}"/></a:spcAft>'
    lnx = f'<a:lnSpc><a:spcPct val="{ln * 1000}"/></a:lnSpc>'
    al = f' algn="{algn}"' if algn else ''
    if kind == 'h':   # original level-1 heading (dark-red square bullet)
        ppr = (f'<a:pPr marL="265113" indent="-265113" latinLnBrk="0"{al}>{lnx}{sp}'
               f'<a:buClr><a:srgbClr val="{BUL}"/></a:buClr><a:buSzPct val="75000"/>'
               '<a:buFont typeface="Wingdings" pitchFamily="2" charset="2"/><a:buChar char="n"/><a:defRPr/></a:pPr>')
        return f'<a:p>{ppr}{runs(markup, None, color or "head", bold, italic)}</a:p>'
    if kind == 'b':   # original level-2 bullet
        ppr = (f'<a:pPr marL="573750" indent="-285750" latinLnBrk="0"{al}>{lnx}{sp}'
               '<a:buClr><a:schemeClr val="bg1"/></a:buClr><a:buSzPct val="75000"/>'
               '<a:buFont typeface="Arial" panose="020B0604020202020204" pitchFamily="34" charset="0"/>'
               '<a:buChar char="•"/><a:defRPr/></a:pPr>')
        return f'<a:p>{ppr}{runs(markup, sz, color or "bg1", bold, italic)}</a:p>'
    if kind == 'cb':  # compact bullet for cards and boxes
        ppr = (f'<a:pPr marL="182880" indent="-182880" latinLnBrk="0"{al}>{lnx}{sp}'
               f'<a:buClr><a:srgbClr val="{color or INK}"/></a:buClr><a:buSzPct val="80000"/>'
               '<a:buFont typeface="Arial" panose="020B0604020202020204" pitchFamily="34" charset="0"/>'
               '<a:buChar char="•"/><a:defRPr/></a:pPr>')
        return f'<a:p>{ppr}{runs(markup, sz, color or INK, bold, italic)}</a:p>'
    ppr = f'<a:pPr marL="0" indent="0" latinLnBrk="0"{al}>{lnx}{sp}<a:buNone/><a:defRPr/></a:pPr>'
    return f'<a:p>{ppr}{runs(markup, sz, color or INK, bold, italic)}</a:p>'


class Ids:
    def __init__(self, start=200):
        self.n = start

    def __call__(self):
        self.n += 1
        return self.n


def body_pr(anchor='t', ins=(0.05, 0.03, 0.05, 0.03)):
    l, t, r, b = (E(v) for v in ins)
    return (f'<a:bodyPr wrap="square" lIns="{l}" tIns="{t}" rIns="{r}" bIns="{b}" rtlCol="0" anchor="{anchor}">'
            '<a:noAutofit/></a:bodyPr>')


def tb(i, name, x, y, w, h, paras, anchor='t', ins=(0.05, 0.03, 0.05, 0.03)):
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="{escape(name)}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{E(x)}" y="{E(y)}"/><a:ext cx="{E(w)}" cy="{E(h)}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
            f'<p:txBody>{body_pr(anchor, ins)}<a:lstStyle/>{paras}</p:txBody></p:sp>')


def box(i, name, x, y, w, h, fill=None, line=None, dash=False, paras='', anchor='t', geom='roundRect',
        adj=6000, ins=(0.1, 0.07, 0.1, 0.07), lw=12700):
    av = f'<a:avLst><a:gd name="adj" fmla="val {adj}"/></a:avLst>' if geom == 'roundRect' else '<a:avLst/>'
    fx = f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>' if fill else '<a:noFill/>'
    if line:
        lx = (f'<a:ln w="{lw}"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill>'
              + ('<a:prstDash val="dash"/>' if dash else '') + '</a:ln>')
    else:
        lx = '<a:ln><a:noFill/></a:ln>'
    tx = paras or '<a:p><a:endParaRPr lang="en-US" dirty="0"/></a:p>'
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="{escape(name)}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{E(x)}" y="{E(y)}"/><a:ext cx="{E(w)}" cy="{E(h)}"/></a:xfrm>'
            f'<a:prstGeom prst="{geom}">{av}</a:prstGeom>{fx}{lx}</p:spPr>'
            f'<p:txBody>{body_pr(anchor, ins)}<a:lstStyle/>{tx}</p:txBody></p:sp>')


def pic(i, name, rid, x, y, w, h, descr=''):
    return (f'<p:pic><p:nvPicPr><p:cNvPr id="{i}" name="{escape(name)}" descr="{escape(descr)}"/>'
            '<p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>'
            f'<p:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>'
            f'<p:spPr><a:xfrm><a:off x="{E(x)}" y="{E(y)}"/><a:ext cx="{E(w)}" cy="{E(h)}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')


BORDER = ''.join(f'<a:{s} w="12700" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:srgbClr val="C9D3E3"/></a:solidFill>'
                 '<a:prstDash val="solid"/><a:round/><a:headEnd type="none" w="med" len="med"/>'
                 '<a:tailEnd type="none" w="med" len="med"/></a:' + s + '>' for s in ('lnL', 'lnR', 'lnT', 'lnB'))


def table(i, name, x, y, colw, rows, rowh, sz=1200, fills=None, colors=None, aligns=None, hsz=None):
    grid = ''.join(f'<a:gridCol w="{E(w)}"/>' for w in colw)
    trs, tot = '', 0.0
    for ri, row in enumerate(rows):
        h = rowh[ri] if isinstance(rowh, (list, tuple)) else rowh
        tot += h
        tcs = ''
        for ci, cell in enumerate(row):
            head = ri == 0
            al = 'ctr' if head else (aligns[ci] if aligns else 'l')
            c = (colors or {}).get((ri, ci), INK)
            paras = ''.join(P(part, 'p', hsz or sz if head else sz, 100, al, c, bold=head)
                            for part in str(cell).split('\n'))
            f = (fills or {}).get((ri, ci))
            fx = f'<a:solidFill><a:srgbClr val="{f}"/></a:solidFill>' if f else ''
            tcs += (f'<a:tc><a:txBody><a:bodyPr/><a:lstStyle/>{paras}</a:txBody>'
                    f'<a:tcPr marL="{E(0.06)}" marR="{E(0.06)}" marT="{E(0.03)}" marB="{E(0.03)}" anchor="ctr">'
                    f'{BORDER}{fx}</a:tcPr></a:tc>')
        trs += f'<a:tr h="{E(h)}">{tcs}</a:tr>'
    return (f'<p:graphicFrame><p:nvGraphicFramePr><p:cNvPr id="{i}" name="{escape(name)}"/>'
            '<p:cNvGraphicFramePr><a:graphicFrameLocks noGrp="1"/></p:cNvGraphicFramePr><p:nvPr/></p:nvGraphicFramePr>'
            f'<p:xfrm><a:off x="{E(x)}" y="{E(y)}"/><a:ext cx="{E(sum(colw))}" cy="{E(tot)}"/></p:xfrm>'
            '<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/table"><a:tbl>'
            '<a:tblPr firstRow="1" bandRow="1"><a:tableStyleId>{3B4B98B0-60AC-42C2-AFA5-B58CD77FA1E5}</a:tableStyleId></a:tblPr>'
            f'<a:tblGrid>{grid}</a:tblGrid>{trs}</a:tbl></a:graphicData></a:graphic></p:graphicFrame>')


def arrow(i, x, y, w, h, fill='9CA3AF', geom='rightArrow'):
    return box(i, f'Arrow {i}', x, y, w, h, fill=fill, geom=geom, paras='<a:p><a:endParaRPr lang="en-US" dirty="0"/></a:p>')


# ---------------------------------------------------------------- package helpers
def sh(*a):
    r = subprocess.run(a, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f'{a} failed: {r.stdout}{r.stderr}')
    return r.stdout


def sp(path):
    return os.path.join(WORK, 'ppt', 'slides', path)


def load(name):
    return etree.parse(sp(name))


def save(tree, name):
    # no etree.cleanup_namespaces: it can drop prefixes used only inside mc:Ignorable values
    tree.write(sp(name), xml_declaration=True, encoding='UTF-8', standalone=True)


def tree_of(t):
    return t.getroot().find('.//p:cSld/p:spTree', NS)


def add(t, *xmls):
    st = tree_of(t)
    for x in xmls:
        wrap = etree.fromstring(f'<w xmlns:a="{NS["a"]}" xmlns:r="{NS["r"]}" xmlns:p="{NS["p"]}">{x}</w>')
        for el in wrap:
            st.append(el)


def shape_text(el):
    return ''.join(el.itertext())


def drop(t, pred):
    st = tree_of(t)
    n = 0
    for el in list(st):
        tag = etree.QName(el).localname
        if tag in ('sp', 'pic', 'graphicFrame', 'grpSp', 'cxnSp') and pred(el):
            st.remove(el)
            n += 1
    return n


def name_of(el):
    c = el.find('.//p:cNvPr', NS)
    return c.get('name') if c is not None else ''


def set_texts(t, mapping):
    """Replace whole <a:t> strings."""
    hits = 0
    for at in t.getroot().iter(f'{{{NS["a"]}}}t'):
        if at.text in mapping:
            at.text = mapping[at.text]
            hits += 1
    return hits


def replace_body(t, paras, x=0.61, y=1.0, w=8.84, h=0.5):
    """Remove the original body 'Rectangle 4' and put a fresh one with the same bullet styles."""
    drop(t, lambda el: name_of(el) == 'Rectangle 4')
    add(t, tb(150, 'Rectangle 4', x, y, w, h, paras))


def header(t, text):
    hit = 0
    for at in t.getroot().iter(f'{{{NS["a"]}}}t'):
        if at.text in ('Introduction', 'Results &amp; Discussion', 'Results & Discussion'):
            at.text = text
            hit += 1
    assert hit == 1, f'header not found ({hit})'


def rels_path(name):
    return sp(os.path.join('_rels', name + '.rels'))


def rel_add(name, target):
    rt = etree.parse(rels_path(name))
    root = rt.getroot()
    ids = {r.get('Id') for r in root}
    n = 1
    while f'rId{n}' in ids:
        n += 1
    el = etree.SubElement(root, f'{{{RELNS}}}Relationship')
    el.set('Id', f'rId{n}'); el.set('Type', IMG_T); el.set('Target', target)
    rt.write(rels_path(name), xml_declaration=True, encoding='UTF-8', standalone=True)
    return f'rId{n}'


def rel_target(name, rid):
    for r in etree.parse(rels_path(name)).getroot():
        if r.get('Id') == rid:
            return r.get('Target')


def rels_prune(name):
    """Drop image relationships the slide no longer references."""
    used = set(re.findall(r'r:(?:embed|link|id)="(rId\d+)"', open(sp(name), encoding='utf-8').read()))
    rt = etree.parse(rels_path(name))
    for r in list(rt.getroot()):
        if r.get('Type') == IMG_T and r.get('Id') not in used:
            rt.getroot().remove(r)
    rt.write(rels_path(name), xml_declaration=True, encoding='UTF-8', standalone=True)


def refs_line(i, text, y=6.45, h=0.42, x=0.55, w=8.9, sz=1000):
    return tb(i, 'References', x, y, w, h, P(text, 'p', sz, 100, color=MUTED, italic=True))


def heading(i, text, y=0.98, h=0.48):
    return tb(i, 'Rectangle 4', 0.61, y, 8.84, h, P(text, 'h', ln=100))


# ---------------------------------------------------------------- build
shutil.rmtree(WORK, ignore_errors=True)
zipfile.ZipFile(SRC).extractall(WORK)

NEW_KEYS = ['prev', 'overview', 'workflow', 'stability', 'md_setup', 'md_status', 'next', 'summary', 'refs']
new = {}
for k in NEW_KEYS:
    out = sh('python3', os.path.join(SKILL, 'scripts', 'add_slide.py'), WORK, 'slide3.xml')
    m = re.search(r'(slide\d+\.xml)', out.split('Created')[-1])
    new[k] = m.group(1)
print('new slides:', new)

shutil.copy(os.path.join(EXTRA, 'jung2026_fig5b.png'), os.path.join(WORK, 'ppt', 'media', 'jung2026_fig5b.png'))


def fresh(key, hdr):
    """New slide (copy of slide 3): keep the header, drop body/ref/picture."""
    name = new[key]
    t = load(name)
    header(t, hdr)
    drop(t, lambda el: name_of(el) in ('Rectangle 4', 'TextBox 69') or etree.QName(el).localname == 'pic')
    return name, t


ids = Ids()

# ---- 1 title
t = load('slide1.xml')
assert set_texts(t, {'August 18, 2026': 'October 13, 2026',
                     'Technical Report on DFT Screening:': 'Progress Report on DFT/MLIP Screening:'}) == 2
save(t, 'slide1.xml')

# ---- 2 previous DFT work (figure boxes left empty on purpose)
name, t = fresh('prev', 'Background')
add(t, heading(ids(), 'DFT simulations so far — the experience behind this screening'))
tiles = [
    ('Li₆PS₅Cl baseline', 'Band gap (fixed-occupation NSCF), EOS, elastic constants — reference for every doped model'),
    ('Nd/O co-doping (Nd₂O₃)', 'Band edges (Nd 5d vs 4f), −ICOHP bonding, cathode-interface (CEI) models — with the experimental team'),
    ('B₂O₃ and O doping', 'Equation of state, bond-valence Li pathways, MLIP-MD Li transport (multi-seed, relative)'),
    ('h-BN on carbon fiber', 'Li adsorption and migration (NEB) on h-BN-coated VGCF; layer-number (confinement) effect'),
    ('Li₃N (SEI component)', 'Li migration barriers (NEB); universal MLIP found biased for Li₃N → DFT only'),
    ('Li₂S (SEI component)', 'Li-vacancy migration barrier (NEB, charged cell) and supercell-size convergence'),
    ('Interfacial adhesion', 'Work of adhesion of SE|SE and SE|graphite interfaces (slab DFT, MLIP cross-check) → contact input for DEM'),
    ('Binder adsorption (SDCP)', 'Spin-state-resolved adsorption of a binder molecule on LiNiO₂ surfaces'),
]
TW, TH, GX, GY = 2.16, 2.4, 0.12, 0.1
for k, (ti, tx) in enumerate(tiles):
    x = 0.5 + (k % 4) * (TW + GX)
    y = 1.5 + (k // 4) * (TH + GY)
    add(t,
        box(ids(), f'Tile {k + 1}', x, y, TW, TH, fill='F5F7FA', adj=5000),
        tb(ids(), f'Tile {k + 1} title', x + 0.06, y + 0.04, TW - 0.12, 0.44,
           P(ti, 'p', 1150, 100, color=NAVY, bold=True), anchor='ctr'),
        box(ids(), f'Tile {k + 1} figure', x + 0.1, y + 0.5, TW - 0.2, 1.12, fill='FFFFFF', line='9CA3AF',
            dash=True, geom='rect', paras=P('Figure', 'p', 1000, 100, 'ctr', MUTED), anchor='ctr'),
        tb(ids(), f'Tile {k + 1} text', x + 0.06, y + 1.66, TW - 0.12, 0.72, P(tx, 'p', 950, 100, color=INK)))
add(t, tb(ids(), 'Carried over', 0.5, 6.45, 9.0, 0.42,
          P('[[B:Carried into this work:]] DFT EOS/elastic · band-edge analysis · bond-valence maps · MLIP-MD protocol '
            '(multi-seed, relative) · NEB · grand-potential stability · interface energetics', 'p', 1100, 100, color=BLUE)))
save(t, name)

# ---- 3 overview
name, t = fresh('overview', 'Overview')
add(t, heading(ids(), 'This work: purpose, what has run, what comes next'))
cards = [
    ('Purpose', 'FDF1F1', BUL, [('p', 'Select dopant precursors for Li₆PS₅Cl that raise electrochemical and mechanical stability without slowing Li-ion transport.'),
                                ('p', 'Let the computation make the selection, with the selection rule stated in advance.')]),
    ('Completed', 'EEF3FA', NAVY, [('cb', 'Site enumeration + MLIP relaxation: 89 of 91 precursors (3,615 configurations)'),
                                   ('cb', 'DFT equation of state of the reference compositions'),
                                   ('cb', 'Stability windows recomputed with one consistent definition')]),
    ('Running', 'E8F4FB', BLUE, [('cb', 'MLIP-MD Li diffusivity: Al₂O₃- vs Al₂S₃-derived doping (12 of 40 runs)'),
                                 ('cb', 'DFT elastic constants of the reference compositions')]),
    ('Next', 'F3F4F6', '374151', [('cb', 'Interfacial reaction products with ground-state reference phases'),
                                  ('cb', 'Selection rule fixed before combining descriptors'),
                                  ('cb', 'Shortlist → DFT validation → experiments')]),
]
for k, (ti, fill, tc, items) in enumerate(cards):
    x = 0.55 + (k % 2) * 4.52
    y = 1.55 + (k // 2) * 2.4
    paras = P(ti, 'p', 1600, 100, color=tc, bold=True, spcaft=600) + ''.join(
        P(s, kind, 1300, 110, color=INK, spcaft=400) for kind, s in items)
    add(t, box(ids(), f'Card {ti}', x, y, 4.38, 2.25, fill=fill, paras=paras, ins=(0.16, 0.12, 0.16, 0.1)))
add(t, tb(ids(), 'Status note', 0.55, 6.38, 8.9, 0.4,
          P('At this stage the screening descriptors are used for exploration; [[B:no dopant ranking is claimed.]]',
            'p', 1300, 100, color=BLUE)))
save(t, name)

# ---- 5 prior screens (orig slide 7)
t = load('slide7.xml')
replace_body(t, P('Prior work: what dopant screens vary', 'h', ln=130)
             + P('Earlier screens place one element on a site, or screen hostless compounds.', 'b', ln=130)
             + P('Here a [[b:precursor compound]] fills one cation and one anion site at once.', 'b', ln=130),
             y=1.08, h=1.45)
drop(t, lambda el: etree.QName(el).localname == 'grpSp' or name_of(el) == 'TextBox 3')   # images + captions; 4-line refs box
add(t, tb(ids(), 'References top', 4.6, 0.93, 4.9, 0.42,
          P('Chem. Mater. 27, 4040 (2015) · Adv. Energy Mater. 14, 2304025 (2024)', 'p', 950, 100, 'r', MUTED, italic=True)
          + P('J. Mater. Chem. A 12, 7272 (2024) · Joule 3, 1252 (2019)', 'p', 950, 100, 'r', MUTED, italic=True)))
assert set_texts(t, {'47': '89'}) == 1          # cell runs: '47' ' (' '91' ' planned)'
tbl = t.getroot().find('.//p:graphicFrame', NS)
cell_hits = 0
for tc in tbl.iter(f'{{{NS["a"]}}}tc'):
    txt = shape_text(tc)
    if txt.startswith('Included'):  # runs: 'I' 'ncluded' '(reported as sensitivity, ' 'not a gate)'
        ps = tc.findall('.//a:p', NS)
        first = ps[0]
        for extra in ps[1:]:
            extra.getparent().remove(extra)
        rs = first.findall('a:r', NS)
        rs[0].find('a:t', NS).text = 'DFT reference + MLIP descriptor (not a gate)'
        for r in rs[1:]:
            first.remove(r)
        cell_hits += 1
assert cell_hits == 1, cell_hits
tbl.find('.//p:xfrm/a:off', NS).set('y', str(E(2.62)))
add(t, tb(ids(), 'Related screens', 0.6, 4.88, 8.85, 1.5,
          P('Related screens', 'p', 1300, 115, color=NAVY, bold=True)
          + P('Holistic screening of Li-ion conductors (Sendek 2017) and high-throughput MD (Kahle 2020)', 'cb', 1250, 115)
          + P('Dual-dopant screening of LGPS-type conductors (Jung 2026) · ML interface-stability screening (Park 2026)', 'cb', 1250, 115)
          + P('Site-resolved dopant defect thermodynamics in argyrodites (Muy 2025)', 'cb', 1250, 115)),
    refs_line(ids(), 'Energy Environ. Sci. 10, 306 (2017) · Energy Environ. Sci. 13, 928 (2020) · eTransportation 28, 100570 (2026) · '
                     'Adv. Sci. 2026, e76305 · Chem. Mater. 37, 2395 (2025)'))
save(t, 'slide7.xml')

# ---- 6 candidate set (orig slide 8)
t = load('slide8.xml')
header(t, 'Approach')
replace_body(t, P('Candidate set: 91 precursor compounds in seven anion families', 'h', ln=130)
             + P('Cations +1 to +6, anions O²⁻ to I⁻; only existing compounds are used.', 'b', ln=130)
             + P('89 of 91 computed (As₂S₃: no valid configuration; AlI₃: incomplete).', 'b', ln=130),
             y=1.08, h=1.4)
gf = t.getroot().find('.//p:graphicFrame', NS)
gf.find('.//p:xfrm/a:off', NS).set('y', str(E(2.5)))
for rp in gf.iter(f'{{{NS["a"]}}}rPr', f'{{{NS["a"]}}}endParaRPr'):
    if rp.get('sz'):
        rp.set('sz', '1300')
for tr in gf.iter(f'{{{NS["a"]}}}tr'):
    tr.set('h', str(E(0.36)))
add(t, refs_line(ids(), 'Precursor-derived co-doping of argyrodites: CuCl — Taklu, Nano Energy 90, 106542 (2021) · '
                        'MgF₂ — Liu, Angew. Chem. Int. Ed. 62, e202302655 (2023) · ZnO — Jang, J. Alloys Compd. 957, 170273 (2023) · '
                        'La₂O₃ — Yang, Electrochim. Acta 535, 146619 (2025) · Nd₂O₃ — Xu, Nano Energy 157, 112246 (2026)',
                 y=5.72, h=0.8, sz=950))
save(t, 'slide8.xml')

# ---- 7 workflow table
name, t = fresh('workflow', 'Approach')
add(t, heading(ids(), 'Simulation workflow and status'))
DONE, RECO, RUN, PLAN = ('E8F3EA', '1B5E20'), ('FFF4E0', '8A5A00'), ('DCEBF8', '0B5394'), ('EFEFEF', '4B5563')
rows = [['#', 'Step', 'Method', 'Scale', 'Status'],
        ['1', 'Site enumeration', 'Charge-balanced placement of the precursor cation and anion on the Li, P, S and Cl sublattices', '91 precursors', 'Done'],
        ['2', 'Relaxation', 'Universal MLIP (UMA), FIRE optimizer', '3,615 configurations', 'Done'],
        ['3', 'Short anneal', 'MLIP-MD at 500 K for 50 ps, then re-relaxation', '681 configurations', 'Done'],
        ['4', 'Li-site landscape', 'Bond-valence site energy (softBV)', 'per precursor', 'Done (structural proxy)'],
        ['5', 'EOS / elastic constants', 'DFT (Quantum ESPRESSO): Birch–Murnaghan fit; finite strains with ionic relaxation', 'reference compositions', 'EOS done · C[[_:ij]] running'],
        ['6', 'Stability window', 'Grand-potential phase diagram from Materials Project phases (0 K)', '89 compositions', 'Recomputed'],
        ['7', 'Interfacial reactivity', 'Pseudo-binary reaction energy vs Li metal, LiCoO₂, LiMn₂O₄', '90 compounds', 'Re-evaluation planned'],
        ['8', 'Li transport', 'MLIP-MD (NVT); MSD → Li diffusivity ratio between two precursors', '40 runs', 'Running (12/40)']]
st = {1: DONE, 2: DONE, 3: DONE, 4: DONE, 5: RUN, 6: RECO, 7: PLAN, 8: RUN}
fills = {(r, 4): st[r][0] for r in st}
colors = {(r, 4): st[r][1] for r in st}
add(t, table(ids(), 'Workflow table', 0.45, 1.52, [0.35, 1.7, 3.75, 1.75, 1.55], rows,
             [0.38] + [0.52] * 8, sz=1150, hsz=1250, fills=fills, colors=colors,
             aligns=['ctr', 'l', 'l', 'l', 'ctr']),
    tb(ids(), 'Abbreviations', 0.45, 6.18, 9.1, 0.6,
       P('MLIP: machine-learning interatomic potential (UMA, a universal model) · MSD: mean squared displacement · '
         'EOS: equation of state · all configurations at one dopant concentration', 'p', 1050, 105, color=MUTED)))
save(t, name)

# ---- 8 configuration sampling (orig slide 11)
t = load('slide11.xml')
header(t, 'Approach')
grp = t.getroot().find('.//p:grpSp', NS)
emf_rid, emf_ext = None, None
for p_ in grp.iter(f'{{{NS["p"]}}}pic'):
    rid = p_.find('.//a:blip', NS).get(f'{{{NS["r"]}}}embed')
    if rel_target('slide11.xml', rid).endswith('image17.png'):   # the site-pair heatmap (the EMF is the bar chart)
        ext = p_.find('.//a:xfrm/a:ext', NS)
        emf_rid, emf_ext = rid, (int(ext.get('cx')), int(ext.get('cy')))
assert emf_rid, 'site-pair heatmap (image17.png) not found'
drop(t, lambda el: etree.QName(el).localname == 'grpSp' or name_of(el) in ('TextBox 8', 'TextBox 9'))
replace_body(t, P('Configuration sampling and MLIP relaxation', 'h', ln=130)
             + P('No site was assumed: every charge-balanced placement was [[b:built and relaxed]].', 'b', ln=130)
             + P('A short anneal (500 K, 50 ps) moves each structure out of its local minimum.', 'b', ln=130),
             y=1.08, h=1.4)
rid23 = rel_add('slide11.xml', '../media/image23.png')
hw = 4.6
hh = hw * emf_ext[1] / emf_ext[0]
add(t, pic(ids(), 'Site-pair heatmap', emf_rid, 0.5, 2.6, hw, hh, 'Configurations per cation-anion site pair'),
    tb(ids(), 'Caption left', 0.5, 2.62 + hh, hw, 0.32,
       P('< configurations per cation–anion site pair (3,615 in total) >', 'p', 1150, 100, 'ctr')),
    pic(ids(), 'Anneal schematic', rid23, 5.55, 2.6, 3.6, 3.6 * 1197 / 1623, 'What a short anneal does'),
    tb(ids(), 'Caption right', 5.45, 2.62 + 3.6 * 1197 / 1623, 3.9, 0.32,
       P('< what the short anneal does >', 'p', 1150, 100, 'ctr')),
    tb(ids(), 'Bottom note', 0.55, 6.2, 8.9, 0.6,
       P('Configurations of the same precursor can differ as much as different precursors for some descriptors '
         '→ [[B:descriptors are used for exploration, not for ranking.]]', 'p', 1250, 105, color=BLUE)))
save(t, 'slide11.xml')

# ---- 9 DFT reference (orig slide 16)
t = load('slide16.xml')
header(t, 'Approach')
replace_body(t, P('DFT reference calculations: equation of state and elastic constants', 'h')
             + P('B₀ and equilibrium volume from a [[b:Birch–Murnaghan]] equation-of-state fit.', 'b', ln=130)
             + P('Elastic constants (C[[_:ij]]) from finite strains are running on GPU.', 'b', ln=130),
             y=1.08, h=1.5)
assert set_texts(t, {'※ these two curves are DFT; the screening ran on the machine-learned potential with FIRE relaxation':
                     '※ DFT (Quantum ESPRESSO); the screening itself used the MLIP'}) == 1
add(t, refs_line(ids(), 'Deng, J. Electrochem. Soc. 163, A67 (2016) · Torii, J. Phys. Chem. C 129, 17882 (2025)',
                 y=6.1, h=0.3))
save(t, 'slide16.xml')

# ---- 10 stability window + interface
name, t = fresh('stability', 'Approach')
add(t, heading(ids(), 'Electrochemical stability window and interfacial reactivity'))
add(t, tb(ids(), 'Window bullets', 0.55, 1.5, 4.55, 2.55,
          P('Grand-potential phase diagram: the Li chemical potential is scanned as a voltage (0 K, bulk thermodynamics).', 'cb', 1250, 110, spcaft=500)
          + P('Stable window = voltage range where the composition decomposes [[b:without Li exchange]]; if no such range exists, no stable window.', 'cb', 1250, 110, spcaft=500)
          + P('Recomputed for all 89 compositions with this definition (Sep–Oct); the earlier definition overestimated window widths.', 'cb', 1250, 110)))
x0, x1, v0, v1 = 0.75, 4.85, 1.4, 2.5
X = lambda v: x0 + (v - v0) * (x1 - x0) / (v1 - v0)
add(t,
    tb(ids(), 'Schematic title', 0.6, 4.08, 4.4, 0.3, P('Example: Li₆PS₅Cl host (MP phases, 0 K)', 'p', 1100, 100, color=INK, bold=True)),
    tb(ids(), 'Window label', (X(1.717) + X(2.140)) / 2 - 1.1, 4.42, 2.2, 0.28, P('stable window 0.423 V', 'p', 1050, 100, 'ctr', '1B5E20', bold=True)),
    box(ids(), 'Reduction zone', X(1.4), 4.72, X(1.717) - X(1.4), 0.42, fill='FBE3E3', geom='rect', anchor='ctr',
        paras=P('Li uptake', 'p', 1000, 100, 'ctr', '7F1D1D')),
    box(ids(), 'Window zone', X(1.717), 4.72, X(2.140) - X(1.717), 0.42, fill='DFF2E3', geom='rect', anchor='ctr',
        paras=P('no Li exchange', 'p', 1000, 100, 'ctr', '1B5E20')),
    box(ids(), 'Oxidation zone', X(2.140), 4.72, X(2.5) - X(2.140), 0.42, fill='FBE3E3', geom='rect', anchor='ctr',
        paras=P('Li release', 'p', 1000, 100, 'ctr', '7F1D1D')),
    tb(ids(), 'Tick low', X(1.717) - 0.45, 5.16, 0.9, 0.26, P('1.717 V', 'p', 1000, 100, 'ctr')),
    tb(ids(), 'Tick high', X(2.140) - 0.45, 5.16, 0.9, 0.26, P('2.140 V', 'p', 1000, 100, 'ctr')),
    tb(ids(), 'Axis label', 0.75, 5.42, 4.1, 0.26, P('voltage vs Li/Li⁺ →', 'p', 1000, 100, 'ctr', MUTED)),
    tb(ids(), 'Reactions', 0.6, 5.7, 4.5, 0.55,
       P('Inside the window: Li₆PS₅Cl → Li₃PS₄ + Li₂S + LiCl (no Li exchange); above 2.140 V: oxidation with Li release',
         'p', 950, 100, color=MUTED)))
rid31 = rel_add(name, '../media/image31.png')
add(t, pic(ids(), 'Sundar 2025 Fig 2', rid31, 5.3, 1.55, 4.15, 4.15 * 805 / 2118, 'Coating reaction energy at four interfaces'),
    tb(ids(), 'Caption right', 5.3, 3.17, 4.15, 0.3, P('< coating reaction energy at four interfaces >', 'p', 1100, 100, 'ctr')),
    tb(ids(), 'Credit right', 5.3, 3.43, 4.15, 0.28, P('Reproduced from Sundar et al., Adv. Sci. 12, e13191 (2025)', 'p', 950, 100, 'ctr', MUTED, italic=True)),
    tb(ids(), 'Interface bullets', 5.3, 3.85, 4.15, 2.2,
       P('Interfacial reactivity uses the same phase data: reaction energy of each dopant phase against Li₆PS₅Cl, Li metal and cathode materials.', 'cb', 1250, 110, spcaft=500)
       + P('Our reaction-product analysis is being [[b:redone with ground-state reference phases]] (E[[_:hull]] = 0).', 'cb', 1250, 110)),
    refs_line(ids(), 'Zhu, ACS Appl. Mater. Interfaces 7, 23685 (2015) · Richards, Chem. Mater. 28, 266 (2016) · '
                     'Xiao, Nat. Rev. Mater. 5, 105 (2020) · Schwietert, Nat. Mater. 19, 428 (2020)', y=6.4))
save(t, name)

# ---- 11 MD setup
name, t = fresh('md_setup', 'Progress')
add(t, heading(ids(), 'Li transport by MLIP molecular dynamics: setup'))
add(t, tb(ids(), 'Setup bullets', 0.55, 1.5, 4.6, 2.9,
          P('[[B:Question]]: does the precursor anion (Al₂O₃ vs Al₂S₃) change Li diffusivity in Al-doped Li₆PS₅Cl?', 'cb', 1250, 110, spcaft=600)
          + P('[[B:Reported quantity]]: ratio of Li tracer diffusivities from MSD slopes — relative, not an absolute conductivity.', 'cb', 1250, 110, spcaft=600)
          + P('[[B:Analysis plan fixed before the runs]]: diffusive-regime checks, then an equivalence test (margin ±ln 1.5) on the log-ratio.', 'cb', 1250, 110)),
    box(ids(), 'Recipe A', 0.6, 4.5, 2.1, 0.95, fill='EEF3FA', anchor='ctr',
        paras=P('Al₂O₃-derived', 'p', 1200, 100, 'ctr', NAVY, bold=True) + P('2 Al + 3 O + 4 Li vacancies', 'p', 1050, 100, 'ctr')),
    box(ids(), 'Recipe B', 2.95, 4.5, 2.1, 0.95, fill='F3F4F6', anchor='ctr',
        paras=P('Al₂S₃-derived', 'p', 1200, 100, 'ctr', '374151', bold=True) + P('2 Al + 4 Li vacancies (S unchanged)', 'p', 1050, 100, 'ctr')),
    tb(ids(), 'Recipe note', 0.6, 5.52, 4.45, 0.75,
       P('Same host configuration and cell volume — only the precursor anion differs', 'p', 1050, 105, 'ctr', MUTED)
       + P('→ D(Al₂O₃) / D(Al₂S₃)', 'p', 1300, 110, 'ctr', BLUE, bold=True)))
rows = [['Setting', 'Value'],
        ['Potential', 'UMA (universal MLIP)'],
        ['Ensemble', 'NVT, Langevin thermostat'],
        ['Temperature', '1000 K (selected in a pilot)'],
        ['Run length', '400 ps production; MSD fit 2–50 ps'],
        ['Cell', '204 atoms, common volume (edge ≈ 1.6 nm)'],
        ['Sampling', '10 start configurations × 2 precursors × 2 seeds = 40 runs'],
        ['Diffusive-regime checks', 'sub-window MSD slope ratio 0.8–1.2 · D spread ≤ 10 % · ≥ 50 Li hops · framework intact']]
add(t, table(ids(), 'Settings table', 5.3, 1.5, [1.4, 2.75], rows, [0.34, 0.42, 0.42, 0.42, 0.5, 0.5, 0.6, 0.8],
             sz=1100, hsz=1200, aligns=['l', 'l']),
    refs_line(ids(), 'Kahle, Energy Environ. Sci. 13, 928 (2020) · He, npj Comput. Mater. 4, 18 (2018) · '
                     'Wood et al. (UMA), arXiv:2506.23971 (2026)'))
save(t, name)

# ---- 12 MD status + limits
name, t = fresh('md_status', 'Progress')
add(t, heading(ids(), 'Li transport: temperature choice, status and limits'))
add(t, tb(ids(), 'Status bullets', 0.55, 1.5, 4.75, 3.1,
          P('[[B:600 K pilot]] (40 runs, 200 ps): Li hopped (~4,000 hops per run) but the MSD never became linear over 2–100 ps → no diffusivity reported (UMA, this cell and volume).', 'cb', 1200, 108, spcaft=500)
          + P('[[B:Temperature]] then chosen by a predefined pilot: 800 K failed and 1000 K passed the diffusive-regime checks.', 'cb', 1200, 108, spcaft=500)
          + P('[[B:Limits]]: the ~1.6-nm cell is below the ~2-nm bulk minimum suggested for MLIP transport, and rankings at high T need not hold at room temperature → relative, condition-specific result.', 'cb', 1200, 108)))
bx, bw = 1.6, 2.6
add(t,
    box(ids(), 'Status panel', 0.55, 4.7, 4.75, 1.6, fill='F5F7FA', adj=4000),
    tb(ids(), 'Status title', 0.7, 4.76, 4.4, 0.3, P('Status (Oct 12)', 'p', 1200, 100, color=NAVY, bold=True)),
    tb(ids(), 'Bar1 label', 0.7, 5.1, 0.9, 0.26, P('Runs', 'p', 1050, 100)),
    box(ids(), 'Bar1 bg', bx, 5.13, bw, 0.2, fill='E5E7EB', geom='rect'),
    box(ids(), 'Bar1 fg', bx, 5.13, bw * 12 / 40, 0.2, fill=BLUE, geom='rect'),
    tb(ids(), 'Bar1 value', bx + bw + 0.05, 5.08, 1.05, 0.28, P('12 / 40', 'p', 1050, 100, color=INK, bold=True)),
    tb(ids(), 'Bar2 label', 0.7, 5.45, 0.9, 0.26, P('GPU-hours', 'p', 1050, 100)),
    box(ids(), 'Bar2 bg', bx, 5.48, bw, 0.2, fill='E5E7EB', geom='rect'),
    box(ids(), 'Bar2 fg', bx, 5.48, bw * 101.1 / 461.4, 0.2, fill=BLUE, geom='rect'),
    tb(ids(), 'Bar2 value', bx + bw + 0.05, 5.43, 1.05, 0.28, P('101 / 461', 'p', 1050, 100, color=INK, bold=True)),
    tb(ids(), 'Status text', 0.7, 5.78, 4.5, 0.5,
       P('Completion expected around Oct 21; the ratio is analysed once, after all 40 runs.', 'p', 1050, 105, color=INK)))
ridj = rel_add(name, '../media/jung2026_fig5b.png')
jw = 3.95
add(t, pic(ids(), 'Jung 2026 Fig 5b', ridj, 5.45, 1.5, jw, jw * 635 / 715, 'Li diffusivity vs 1000/T, Jung 2026 Fig. 5b'),
    tb(ids(), 'Caption right', 5.4, 1.52 + jw * 635 / 715, 4.05, 0.55,
       P('< Li diffusivity vs 1000/T in four LGPS-type compounds: the ordering changes between 700 and 1300 K >', 'p', 1050, 100, 'ctr')),
    tb(ids(), 'Credit right', 5.4, 2.07 + jw * 635 / 715, 4.05, 0.28,
       P('Reproduced from Jung et al., eTransportation 28, 100570 (2026), Fig. 5b', 'p', 950, 100, 'ctr', MUTED, italic=True)),
    refs_line(ids(), 'Phuthi et al., Chem. Mater. (2026), Perspective · Jung et al., eTransportation 28, 100570 (2026)', y=6.42))
save(t, name)

# ---- 13 next steps
name, t = fresh('next', 'Plan')
add(t, heading(ids(), 'Next steps and purpose'))
plan = [('Now → late Oct', BLUE, 1.55, 0.95,
         P('Finish the 40 MD runs and analyse once with the predefined criteria. The follow-up for each outcome '
           '(difference · equivalent · inconclusive · criteria not met) is written down before the analysis.', 'p', 1250, 110)),
        ('Next 1–2 months', NAVY, 2.62, 1.2,
         P('Interfacial reaction products with ground-state reference phases', 'cb', 1250, 110)
         + P('Stability-window table with the corrected definition', 'cb', 1250, 110)
         + P('DFT elastic constants of the reference compositions', 'cb', 1250, 110)),
        ('Then', BUL, 3.94, 0.95,
         P('Selection rule fixed before combining descriptors → shortlist → DFT validation → synthesis and testing with the experimental team.', 'p', 1250, 110)),
        ('Method upgrades', MUTED, 5.01, 0.95,
         P('Larger cells (≥ 2 nm) and longer runs (≥ 0.3 ns) · fine-tuned MLIP · ensemble uncertainty · '
           'dopant concentration from charge-neutral defect thermodynamics', 'p', 1250, 110))]
for lab, c, y, h, paras in plan:
    add(t, box(ids(), f'Label {lab}', 0.55, y, 1.75, h, fill=c, anchor='ctr', paras=P(lab, 'p', 1250, 100, 'ctr', 'FFFFFF', bold=True)),
        box(ids(), f'Content {lab}', 2.4, y, 7.05, h, fill='F5F7FA', anchor='ctr', paras=paras, ins=(0.15, 0.06, 0.15, 0.06)))
add(t, tb(ids(), 'Goal', 0.55, 6.08, 8.9, 0.36,
          P('Goal: a screen that [[B:selects]] the precursor, with the selection rule stated in advance.',
            'p', 1250, 100, color=BLUE)),
    refs_line(ids(), 'Phuthi, Chem. Mater. (2026) · Muy, Chem. Mater. 37, 2395 (2025) · Alghamdi, J. Phys. Energy 8, 025013 (2026) · '
                     'Grasselli, Digital Discovery 4, 2654 (2025)', y=6.52, h=0.36, sz=900))
save(t, name)

# ---- 14 summary
name, t = fresh('summary', 'Summary')
cols3 = [('Done', 'E8F3EA', '1B5E20', ['91 precursors enumerated; 89 relaxed with an MLIP (3,615 configurations)',
                                      'DFT equation of state of the reference compositions',
                                      'Stability windows recomputed with one consistent definition']),
         ('Running', 'E3EEF9', '0B5394', ['MLIP-MD Li diffusivity ratio, Al₂O₃ vs Al₂S₃ (40 runs; ~Oct 21)',
                                         'DFT elastic constants']),
         ('Next', 'F3F4F6', '374151', ['Interfacial reaction products with ground-state phases',
                                      'Selection rule fixed in advance → shortlist → DFT → experiment'])]
for k, (ti, fill, tc, items) in enumerate(cols3):
    paras = P(ti, 'p', 1800, 100, color=tc, bold=True, spcaft=900) + ''.join(P(s, 'cb', 1400, 115, spcaft=700) for s in items)
    add(t, box(ids(), f'Summary {ti}', 0.55 + k * 3.07, 1.15, 2.9, 4.35, fill=fill, paras=paras, ins=(0.16, 0.14, 0.16, 0.1)))
add(t, tb(ids(), 'Bottom line', 0.55, 5.75, 8.9, 0.55,
          P('No dopant ranking is claimed yet — [[B:the screen proposes, predefined tests decide.]]', 'p', 1500, 100, color=BLUE)))
save(t, name)

# ---- 16 references (backup)
name, t = fresh('refs', 'References')
L = [('[[B:Motivation and screening]]', None),
     ('Kang et al., Chem. Commun. 62, 10277 (2026)', 1), ('Xiao et al., Joule 3, 1252 (2019)', 1),
     ('Kahle et al., Energy Environ. Sci. 13, 928 (2020)', 1), ('Sendek et al., Energy Environ. Sci. 10, 306 (2017)', 1),
     ('Miara et al., Chem. Mater. 27, 4040 (2015)', 1), ('Anderson et al., Adv. Energy Mater. 14, 2304025 (2024)', 1),
     ('Lee et al., J. Mater. Chem. A 12, 7272 (2024)', 1), ('Jung et al., eTransportation 28, 100570 (2026)', 1),
     ('Park et al., Adv. Sci. 2026, e76305', 1), ('Muy et al., Chem. Mater. 37, 2395 (2025)', 1),
     ('[[B:Precursor-derived co-doping]]', None),
     ('Taklu et al., Nano Energy 90, 106542 (2021)', 1), ('Liu et al., Angew. Chem. Int. Ed. 62, e202302655 (2023)', 1),
     ('Jang et al., J. Alloys Compd. 957, 170273 (2023)', 1), ('Yang et al., Electrochim. Acta 535, 146619 (2025)', 1),
     ('Xu et al., Nano Energy 157, 112246 (2026)', 1)]
R = [('[[B:Methods]]', None),
     ('Wood et al. (UMA), arXiv:2506.23971 (2026)', 1), ('Rao et al., Phys. Status Solidi A 208, 1804 (2011)', 1),
     ('Deng et al., J. Electrochem. Soc. 163, A67 (2016)', 1), ('Torii et al., J. Phys. Chem. C 129, 17882 (2025)', 1),
     ('Zhu et al., ACS Appl. Mater. Interfaces 7, 23685 (2015)', 1), ('Richards et al., Chem. Mater. 28, 266 (2016)', 1),
     ('Xiao et al., Nat. Rev. Mater. 5, 105 (2020)', 1), ('Schwietert et al., Nat. Mater. 19, 428 (2020)', 1),
     ('Sundar et al., Adv. Sci. 12, e13191 (2025)', 1),
     ('[[B:Transport statistics and limits]]', None),
     ('He et al., npj Comput. Mater. 4, 18 (2018)', 1), ('Phuthi et al., Chem. Mater. (2026), Perspective', 1),
     ('Marcolongo et al., Phys. Rev. Materials 1, 025402 (2017)', 1), ('Alghamdi et al., J. Phys. Energy 8, 025013 (2026)', 1),
     ('Grasselli et al., Digital Discovery 4, 2654 (2025)', 1)]
num = [0]


def ref_paras(lst):
    out = ''
    for txt, k in lst:
        if k is None:
            out += P(txt, 'p', 1100, 100, color=NAVY, spcbef=500, spcaft=150)
        else:
            num[0] += 1
            out += P(f'[{num[0]}] {txt}', 'p', 1000, 100, color=INK, spcaft=80)
    return out


add(t, tb(ids(), 'Refs left', 0.5, 1.0, 4.45, 5.85, ref_paras(L)),
    tb(ids(), 'Refs right', 5.05, 1.0, 4.45, 5.85, ref_paras(R)))
save(t, name)

# ---- backups (orig 10, 15)
t = load('slide10.xml')
header(t, 'Backup')
replace_body(t, P('Site preference vs ionic radius (MLIP relative energies)', 'h', ln=120)
             + P('A precursor fills one cation and one anion site; every charge-balancing placement is a new structure.', 'b', ln=120),
             y=1.08, h=1.2)
save(t, 'slide10.xml')
t = load('slide15.xml')
header(t, 'Backup')
replace_body(t, P('Bond-valence Li landscape (method illustration)', 'h', ln=120)
             + P('Low bond-valence site energy marks Li-accessible regions — a structural proxy, not a diffusion coefficient.', 'b', ln=120),
             y=1.08, h=1.2)
save(t, 'slide15.xml')

# ---- order, prune, pack
order = ['slide1.xml', new['prev'], new['overview'], 'slide3.xml', 'slide7.xml', 'slide8.xml', new['workflow'],
         'slide11.xml', 'slide16.xml', new['stability'], new['md_setup'], new['md_status'], new['next'],
         new['summary'], 'slide19.xml', new['refs'], 'slide10.xml', 'slide15.xml']
pres_p = os.path.join(WORK, 'ppt', 'presentation.xml')
rels_p = os.path.join(WORK, 'ppt', '_rels', 'presentation.xml.rels')
rmap = {r.get('Target').split('/')[-1]: r.get('Id') for r in etree.parse(rels_p).getroot()
        if r.get('Target', '').startswith('slides/')}
pt = etree.parse(pres_p)
lst = pt.getroot().find('p:sldIdLst', NS)
by_rid = {el.get(f'{{{NS["r"]}}}id'): el for el in lst}
for el in list(lst):
    lst.remove(el)
for s in order:
    lst.append(by_rid[rmap[s]])
pt.write(pres_p, xml_declaration=True, encoding='UTF-8', standalone=True)
for s in order:
    rels_prune(s)
print(sh('python3', os.path.join(SKILL, 'scripts', 'clean.py'), WORK)[-400:])
if os.path.exists(OUT):
    os.remove(OUT)
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    ct = os.path.join(WORK, '[Content_Types].xml')
    z.write(ct, '[Content_Types].xml')
    for root, _, files in os.walk(WORK):
        for f in files:
            full = os.path.join(root, f)
            arc = os.path.relpath(full, WORK)
            if arc != '[Content_Types].xml':
                z.write(full, arc)
print('wrote', OUT, 'slides', len(order))
