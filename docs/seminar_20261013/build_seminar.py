#!/usr/bin/env python3
"""연구세미나 덱 생성기 v2 (2026-10-13 · Codex NO-GO 판정 반영 · 양식 = 10-13 연구세미나 덱 사본).

    python3 build_seminar.py --template <10-13 덱.pptx> --repo <리포> --figs <새 그림 폴더> --out <out.pptx>
    python3 build_seminar.py --selftest-only <deck.pptx> --repo <리포> --figs <그림 폴더>      # 검사만 (고치기 전 덱 = 실패해야 한다)

- 양식 그대로: 10-13 덱의 장을 **프로토타입**으로 복제해 글 · 그림만 바꾼다 (글꼴 · 색 · 자리 = 양식).  원래 장은 전부 지운다.
  표지 (1) · 그림 본문 (4) · 두 칸 (11) · 점선 틀 (3) · 요약 (15) · 참고문헌 (17) · Thank you (16).
- v2 (Codex 10-13 통합 판정 §9 좌표 · pt · 문구 · 1저자 Q1–Q6): ■ 제목 18 pt (상속) · 본문 15 pt (줄 간격 125 % · 문단 뒤 5 pt) ·
  캡션 12 pt · 그림 위로 · 자리 표시 = 한 줄 라벨 (명령은 notes) · hold 추론 · 전칭 보증 · 옛 30.7 비교 제거 · 참고문헌 [n] 연결.
- 수치는 전부 정본 문서에서 (각 장 notes 에 출처).  철회값 (claims.json quotation_ban) 은 쓰지 않는다 — selftest 가 덱 전체 글을 스윕한다.
- 용어 = 분야 표준 (내부 코드명 · 원장 ID · 세션명 없음).  tau2 의 이름 = transport tortuosity + 정의식 (1저자 10-05 규약).
"""
import argparse
import copy
import json
import re
from pathlib import Path

from lxml import etree
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Emu, Pt

NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
A = NS['a']
DARK, GRAY, NAVY, RED, BLUE = '1F2937', '6B7280', '1F497D', 'C00000', '0070C0'
BODY_PT, CAP_PT = 15, 12

# ───────────────────────────── 양식 복제 도우미 ─────────────────────────────

def dup_slide(prs, src):
    new = prs.slides.add_slide(src.slide_layout)
    for shp in list(new.shapes):
        shp._element.getparent().remove(shp._element)
    rid_map = {}
    for rid, rel in src.part.rels.items():
        if rel.reltype.endswith(('/slideLayout', '/notesSlide')):
            continue
        rid_map[rid] = (new.part.relate_to(rel.target_ref, rel.reltype, is_external=True) if rel.is_external
                        else new.part.relate_to(rel.target_part, rel.reltype))
    src_csld = src._element.find('{%s}cSld' % NS['p'])
    bg = src_csld.find('{%s}bg' % NS['p'])
    if bg is not None:
        new._element.find('{%s}cSld' % NS['p']).insert(0, copy.deepcopy(bg))
    for el in src.shapes._spTree.iterchildren():
        if el.tag.endswith(('}nvGrpSpPr', '}grpSpPr')):
            continue
        new.shapes._spTree.append(copy.deepcopy(el))
    for el in new.shapes._spTree.iter():
        for k in list(el.attrib):
            if k.startswith('{%s}' % NS['r']) and el.attrib[k] in rid_map:
                el.attrib[k] = rid_map[el.attrib[k]]
    return new


def shape(slide, name):
    for s in slide.shapes:
        if s.name == name:
            return s
    raise KeyError(name)


def shapes_named(slide, name):
    return [s for s in slide.shapes if s.name == name]


def drop(slide, *names):
    for n in names:
        for s in shapes_named(slide, n):
            s._element.getparent().remove(s._element)


def set_runs_text(tf, text):
    """첫 문단 · 첫 run 서식 유지 · 글자만."""
    p0 = tf.paragraphs[0]
    r0 = p0.runs[0]
    r0.text = text
    for r in p0.runs[1:]:
        r._r.getparent().remove(r._r)
    for p in tf.paragraphs[1:]:
        p._p.getparent().remove(p._p)


def _run(p, text, proto_rpr, color=None, bold=None, size=None):
    r = etree.SubElement(p, '{%s}r' % A)
    rp = copy.deepcopy(proto_rpr) if proto_rpr is not None else etree.Element('{%s}rPr' % A)
    if color:
        for sf in rp.findall('{%s}solidFill' % A):
            rp.remove(sf)
        sf = etree.Element('{%s}solidFill' % A)
        c = etree.SubElement(sf, '{%s}srgbClr' % A); c.set('val', color)
        rp.insert(0, sf)
    if bold is not None:
        rp.set('b', '1' if bold else '0')
    if size:
        rp.set('sz', str(int(size * 100)))
    r.append(rp)
    t = etree.SubElement(r, '{%s}t' % A); t.text = text
    return r


def _spacing(paragraph, line=None, before=None, after=None):
    if line is not None:
        paragraph.line_spacing = line
    if before is not None:
        paragraph.space_before = Pt(before)
    if after is not None:
        paragraph.space_after = Pt(after)


def set_body(box, head, bullets, head_size=None, bullet_size=BODY_PT, line=1.25, after=5):
    """양식 본문 상자 (Rectangle 4): 문단 0 = ■ 제목 (크기 상속 = 18 pt) · 문단 1.. = • 소불릿 (15 pt · 줄 간격 125 % · 문단 뒤 5 pt)."""
    tf = box.text_frame
    body = tf._txBody
    paras = tf.paragraphs
    p_head = copy.deepcopy(paras[0]._p)
    p_bul = copy.deepcopy(paras[1]._p) if len(paras) > 1 else copy.deepcopy(paras[0]._p)
    for p in list(paras):
        body.remove(p._p)
    def fill(p_proto, segs, size):
        p = copy.deepcopy(p_proto)
        runs = p.findall('{%s}r' % A)
        rpr = copy.deepcopy(runs[0].find('{%s}rPr' % A))
        for r in runs:
            p.remove(r)
        for e in p.findall('{%s}endParaRPr' % A):
            p.remove(e)
        for txt, col in segs:
            _run(p, txt, rpr, color=col, size=size)
        body.append(p)
    fill(p_head, [(head, None)], head_size)
    for b in bullets:
        segs = [(b, None)] if isinstance(b, str) else b
        fill(p_bul, segs, bullet_size)
    for p in tf.paragraphs[1:]:
        _spacing(p, line=line, after=after)


def set_items(box, items, size=None, line=1.12, before=4):
    """두 칸 · 참고문헌 상자: 문단 틀 = 첫 문단 (불릿 있음) · 두 번째 문단 (있으면 소제목 꼴)."""
    tf = box.text_frame
    body = tf._txBody
    paras = tf.paragraphs
    protos = [copy.deepcopy(p._p) for p in paras]
    for p in list(paras):
        body.remove(p._p)
    for it in items:
        kind, segs = ('b', it) if isinstance(it, (str, list)) else it
        proto = protos[0] if kind == 'b' or len(protos) == 1 else protos[1]
        p = copy.deepcopy(proto)
        runs = p.findall('{%s}r' % A)
        rpr = copy.deepcopy(runs[0].find('{%s}rPr' % A))
        for r in runs:
            p.remove(r)
        for e in p.findall('{%s}endParaRPr' % A):
            p.remove(e)
        segs = [(segs, None)] if isinstance(segs, str) else segs
        for txt, col in segs:
            _run(p, txt, rpr, color=col, size=size)
        body.append(p)
    for p in tf.paragraphs:
        _spacing(p, line=line, before=before)


def set_text(box, segs, size=None, bold=None):
    tf = box.text_frame
    p0 = tf.paragraphs[0]
    runs = p0.runs
    rpr = copy.deepcopy(runs[0]._r.find('{%s}rPr' % A))
    for r in runs:
        p0._p.remove(r._r)
    for p in tf.paragraphs[1:]:
        p._p.getparent().remove(p._p)
    segs = [(segs, None)] if isinstance(segs, str) else segs
    for txt, col in segs:
        _run(p0._p, txt, rpr, color=col, size=size, bold=bold)


def place(sp, box):
    x, y, w, h = box
    sp.left, sp.top, sp.width, sp.height = Inches(x), Inches(y), Inches(w), Inches(h)


def place_pic(slide, path, box):
    """box = (x, y, w, h) in — 비율 유지 · 가운데."""
    x, y, w, h = box
    im = Image.open(path)
    iw, ih = im.size
    s = min(w / iw, h / ih)
    pw, ph = iw * s, ih * s
    return slide.shapes.add_picture(str(path), Inches(x + (w - pw) / 2), Inches(y + (h - ph) / 2), Inches(pw), Inches(ph))


def add_box(slide, proto_el, box, text_paras, name, size=None, line=None):
    """양식 요소 (점선 상자 · 캡션 등) 를 복제해 자리 · 글을 바꾼다.  text_paras = [[(글, 색, 굵게?), …], …]."""
    el = copy.deepcopy(proto_el)
    slide.shapes._spTree.append(el)
    sp = slide.shapes[-1]
    sp.name = name
    place(sp, box)
    tf = sp.text_frame
    body = tf._txBody
    paras = tf.paragraphs
    proto = copy.deepcopy(paras[0]._p)
    for p in list(paras):
        body.remove(p._p)
    for segs in text_paras:
        p = copy.deepcopy(proto)
        runs = p.findall('{%s}r' % A)
        rpr = copy.deepcopy(runs[0].find('{%s}rPr' % A)) if runs else None
        for r in runs:
            p.remove(r)
        for e in p.findall('{%s}endParaRPr' % A):
            p.remove(e)
        for seg in segs:
            txt, col, b = (seg + (None, None))[:3] if isinstance(seg, tuple) else (seg, None, None)
            _run(p, txt, rpr, color=col, bold=b, size=size)
        body.append(p)
    if line is not None:
        for p in tf.paragraphs:
            _spacing(p, line=line)
    return sp


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


# ───────────────────────────── 덱 내용 ─────────────────────────────

def build(template, repo, figs, out):
    repo = Path(repo); figs = Path(figs)
    prs = Presentation(template)
    P = {k: prs.slides[i - 1] for k, i in dict(title=1, tiles=2, dashed=3, pic=4, two=11, summary=15, thanks=16, refs=17).items()}
    FIG_PROTO = copy.deepcopy(shape(P['tiles'], 'Tile 1 figure')._element)      # 점선 "Figure" 상자
    CAP_PROTO = copy.deepcopy(shape(P['tiles'], 'Tile 1 caption')._element)     # < 캡션 >
    CONC_PROTO = copy.deepcopy(shape(P['summary'], 'Conclusion')._element)      # 결론 줄 · 글 상자 원형
    n_orig = len(prs.slides)
    D = {}  # 장별 출처 (Codex 검토용)

    def fig_placeholder(slide, box, what, name='Placeholder'):
        """빈 그림 자리 = 점선 상자 + 한 줄 라벨 (제작 명령은 notes).  1저자 10-13 Q3 (가)."""
        return add_box(slide, FIG_PROTO, box, [[('Figure pending: ' + what, GRAY)]], name, size=CAP_PT, line=1.15)

    def caption(slide, box, paras):
        paras = [paras] if isinstance(paras, str) else paras
        return add_box(slide, CAP_PROTO, box, [[('< ' + t + ' >', DARK)] for t in paras], 'Caption', size=CAP_PT, line=1.1)

    def textbox(slide, box, paras, name, size=14, line=1.15):
        return add_box(slide, CONC_PROTO, box, paras, name, size=size, line=line)

    def body_slide(section, head, bullets, body_box=(0.61, 1.08, 8.84, 1.75)):
        s = dup_slide(prs, P['pic'])
        drop(s, 'New picture', 'TextBox 69')
        set_runs_text(shape(s, 'TextBox 20').text_frame, section)
        box = shape(s, 'Rectangle 4')
        set_body(box, head, bullets)
        place(box, body_box)
        return s

    def two_column(section, head, bullet, left_title, left_items, right_title, right_items, bottom=None, bottom_box=(0.55, 5.75, 8.90, 0.65)):
        s = dup_slide(prs, P['two'])
        set_runs_text(shape(s, 'TextBox 20').text_frame, section)
        set_body(shape(s, 'Rectangle 4'), head, [bullet])
        place(shape(s, 'Rectangle 4'), (0.61, 1.08, 8.84, 1.05))
        lt, li = shape(s, 'Audit findings'), shape(s, 'Audit findings items')
        rt, ri = shape(s, 'Decisions recorded on Sep 12'), shape(s, 'Decisions recorded on Sep 12 items')
        set_text(lt, left_title, size=15); place(lt, (0.55, 2.20, 4.25, 0.36))
        set_text(rt, right_title, size=15); place(rt, (5.05, 2.20, 4.40, 0.36))
        set_items(li, left_items, size=BODY_PT); place(li, (0.55, 2.66, 4.25, 2.75))
        set_items(ri, right_items, size=BODY_PT); place(ri, (5.05, 2.66, 4.40, 2.75))
        concs = shapes_named(s, 'Conclusion')
        if bottom:
            set_text(concs[0], bottom, size=14); place(concs[0], bottom_box)
        else:
            concs[0]._element.getparent().remove(concs[0]._element)
        concs[1]._element.getparent().remove(concs[1]._element)
        return s

    # ── 1 표지 ────────────────────────────────────────────────────────────
    s = dup_slide(prs, P['title'])
    set_runs_text(shape(s, '직사각형 12').text_frame, '[date — to be set]')
    tb = shape(s, 'Rectangle 4').text_frame
    p1 = tb.paragraphs[1]
    r0 = p1.runs[0]
    r0.text = 'Particle-resolved multiscale simulation of sulfide all-solid-state composite cathodes:'
    rpr = copy.deepcopy(r0._r.find('{%s}rPr' % A))
    for r in p1.runs[1:]:
        r._r.getparent().remove(r._r)
    for br in p1._p.findall('{%s}br' % A):
        p1._p.remove(br)
    br = etree.SubElement(p1._p, '{%s}br' % A)
    if rpr is not None:
        br.append(copy.deepcopy(rpr))
    _run(p1._p, 'from powder packing to transport', rpr)
    # 저자 블록 (Codex P1): 제목이 두 줄이라 그림 (y 3.84) 과 겹치던 것 → 세 줄 · 16/14/14 pt · 행 간격 18 pt · 여백 0
    au = shape(s, '직사각형 10')
    place(au, (0.68, 2.98, 8.40, 0.75))
    atf = au.text_frame
    atf.margin_top = atf.margin_bottom = 0
    for p in list(atf.paragraphs):
        if not p.text.strip():
            p._p.getparent().remove(p._p)
    for i, p in enumerate(atf.paragraphs):
        for r in p.runs:
            r.font.size = Pt(16 if i == 0 else 14)
        p.line_spacing = Pt(18); p.space_before = Pt(0); p.space_after = Pt(0)
    D[1] = 'title'
    notes(s, 'Title. Date to be set by the presenter.')

    # ── 2 ① Pipeline ─────────────────────────────────────────────────────
    s = body_slide('Introduction', 'A coupled DEM–MPM–transport workflow',
                   ['Each stage has specific calibration targets and unresolved validation tasks.',
                    'Agreement between models sharing inputs is a consistency check, not independent validation.'])
    place_pic(s, figs / 'F1_pipeline.png', (0.77, 3.00, 8.46, 3.15))
    caption(s, (1.00, 6.28, 8.00, 0.36), 'DEM packing → plastic compaction → voxel transport → electrode response')
    D[2] = 'CLAUDE.md frame [1]–[5]; Codex 10-13 SEM-01 wording'
    notes(s, 'No numbers. Calibration targets per stage: DEM — compaction experiments; MPM — pure-electrolyte compaction (lab reference sample, unpublished); '
             'voxel transport — comparison with conductivity measurements (not yet matched). Agreement between stages that share inputs is a consistency check (SEM-01).')

    # ── 3 ① DEM — porosity ──────────────────────────────────────────────
    s = body_slide('DEM', 'Composition-dependent porosity in five simulated beds',
                   ['Soft-sphere DEM with a linear hysteretic contact law, pressed to 300 MPa; one bed per composition, no seed replicates.',
                    'One 7:3 bed: porosity 31.8 → 25.1 → 16.7 → 16.5 % (final state relaxed at fixed platen); 7:3 (large : small NCM) is the lowest of the five beds.'])
    place_pic(s, repo / 'docs/data/ps73_compaction_curve_20261006/stages_20261012/aligned_ckpt/t1_geometry/ps73_geom3d_4panel_porosity_preview.png', (0.45, 2.95, 5.75, 3.05))
    place_pic(s, repo / 'docs/report_20261021/previews/G1.png', (6.30, 2.90, 3.35, 3.10))
    caption(s, (0.55, 6.10, 5.55, 0.40), 'Four stages of one 7:3 bed: 0 · 47 · 296 · 165 MPa (last = relaxed)')
    caption(s, (6.20, 6.10, 3.50, 0.40), 'Porosity vs large : small NCM (one bed each)')
    D[3] = 'ps73 stages README §6 (porosity exact union 31.81 · 25.09 · 16.68 · 16.49); report_20261021 G1 (20.59 · 18.67 · 17.67 · 16.49 · 16.90)'
    notes(s, 'Sources: docs/data/ps73_compaction_curve_20261006/stages_20261012/README.md §6; docs/report_20261021/summary.json G1. '
             'Qualifiers: one bed per composition, no seed replicates; porosity = exact union of spheres; "lowest of five" is a statement about these five single beds, '
             'not an optimum ratio; the 165 MPa panel is the relaxed state at fixed platen, not an unloaded state.')

    # ── 4 ① DEM → transport ─────────────────────────────────────────────
    s = body_slide('DEM', 'From the contact network to Li⁺ transport',
                   ['Kirchhoff network: each SE–SE contact = bulk resistance + Holm/Maxwell constriction using Hertz contact radii; σ₀ = 1.5 mS cm⁻¹ [8].',
                    'Transport tortuosity T = φ_SE σ₀ / σ_eff: 7.2 → 5.0 (0:10 → 7:3). Contact constriction accounts for 73–75 % of Joule dissipation in this network model.'],
                   body_box=(0.61, 1.08, 8.84, 2.05))
    place_pic(s, repo / 'docs/data/ps45_r45_network_g2_20261007/deck_p14p15_20261012/p14_tortuosity_hertz.png', (0.45, 3.20, 2.95, 2.80))
    place_pic(s, repo / 'docs/data/ps45_r45_network_g2_20261007/deck_p14p15_20261012/p15_sigmaLi_hertz_s0_1p5.png', (3.45, 3.20, 2.95, 2.80))
    fig_placeholder(s, (6.55, 3.20, 3.0, 2.80), 'current pathways in the 7:3 bed (ionic, Hertz; top 50 % of current)')
    caption(s, (0.45, 6.10, 2.95, 0.55), ['Transport tortuosity (Hertz)', 'truncated y-axis — compare values'])
    caption(s, (3.45, 6.10, 2.95, 0.55), ['σ(Li⁺), σ₀ = 1.5 mS cm⁻¹', 'truncated y-axis — compare values'])
    caption(s, (6.55, 6.10, 3.0, 0.40), 'Current pathways (figure pending)')
    D[4] = 'ps45_r45_network_g2 README (tau2 7.2433 · 5.9733 · 5.4495 · 5.0297 · 5.2864; σ_ion 0.0587–0.0893; constriction share 73–75 %; CF tau2 1.25–1.79)'
    notes(s, 'Sources: docs/data/ps45_r45_network_g2_20261007/README.md (values, σ0 = 1.5 section, decomposition section). '
             'Qualifiers: transport tortuosity T = φ_SE σ0 / σ_eff (the literature "tortuosity factor"; not its square root); Hertz H0 = primary; '
             'the 73–75 % share = ΣI²R(constriction) / ΣI²R(total) of the same FULL network solution — a model-internal ratio, not evidence that contact necks explain 75 % of a real electrode. '
             'No seed replicates for these five beds; the 7:3 vs 10:0 difference is not resolved. '
             'Pending figure: scripts/network_current.py dump <7:3 result folder> → webapp DEM 3D viewer "current flow" (same bed, same H0/FULL ionic solution, 1 V, '
             'colour = j = |I|/A; "top 50 % of current" = edges carrying the top half of the current share, not the top half by count). [8] = Bazzoun 2026 (same network approach).')

    # ── 5 ② DEM limits ──────────────────────────────────────────────────
    s = body_slide('DEM', 'What a fixed-shape soft-sphere DEM cannot do',
                   ['No shape change and no yield cap: overlap is the only plasticity proxy; the softened SE modulus (1.35 vs ≈ 22 GPa) is an effective parameter, not a property [1, 7].',
                    'In one 7:3 bed, global viscous damping carries 58 % of the plate reaction during compression — an open issue.'],
                   body_box=(0.61, 1.08, 8.84, 1.85))
    place_pic(s, repo / 'docs/data/dem_governing_equations_report_20261011/fig2_hysteresis_cycle.png', (0.45, 3.05, 5.60, 2.95))
    textbox(s, (6.25, 3.25, 3.35, 2.55),
            [[('Selected literature survey', NAVY, True)], [('(22 studies; author classification)', GRAY)],
             [('· softened SE modulus: 0/22', DARK)], [('· yield or hardness cap: 7/22', DARK)],
             [('· linear hysteretic law: 1/22', DARK)], [('· global damping, dry compaction: none', DARK)]], 'Lit box', size=12, line=1.15)
    caption(s, (0.55, 6.10, 5.40, 0.40), 'Contact-law illustration from the implementation [1, 7]')
    D[5] = 'dem_governing_equations_background_20261011.md §5.1 · §10.3 · §11; DEMP-01 (57.9 %)'
    notes(s, 'Sources: docs/dem_governing_equations_background_20261011.md (§5.3 figure 2; §10.3 literature counts; §11 limits). '
             'Damping share 57.9 % = measured on one 7:3 bed during compression (ledger DEMP-01, open). Literature count = selected canonical cards, our classification; not a systematic review. '
             'Bulk modulus reference ≈ 22 GPa = our DFT E_VRH 22.06 GPa (literature DEM input 22.1 GPa, Bazzoun 2026 [8]); the glass-electrolyte value 24 GPa (Sakuda 2013 [15]) is a different material system. '
             'The statement is about this implementation (fixed spherical shapes, hooke/hysteresis), not about DEM in general.')

    # ── 6 ③ MPM — why ───────────────────────────────────────────────────
    s = body_slide('MPM', 'The material point method supplies the plastic half',
                   ['J2 plasticity on a background grid: shape change and void filling that a fixed-shape sphere cannot represent.',
                    'Active material is kept rigid (DEM skeleton); only the electrolyte flows. 2D: E = 1.53 GPa, σy = 0.15 GPa; 3D: E = 1.53 GPa, ν = 0.49, σy = 0.30 GPa.'])
    fig_placeholder(s, (0.60, 3.00, 4.30, 3.00), 'plastic SE morphology after compaction (2D)')
    fig_placeholder(s, (5.10, 3.00, 4.30, 3.00), '3D DEM-scaffold MPM, x–z slice (AM fixed, SE material points)')
    caption(s, (0.60, 6.10, 4.30, 0.40), '2D: SE flows into voids (figure pending)')
    caption(s, (5.10, 6.10, 4.30, 0.40), '3D: fixed AM skeleton, plastic SE (figure pending)')
    D[6] = 'CLAUDE.md DEM↔MPM frame; 2D champion E 1.53 / σy 0.15; 3D locked E 1.53 · ν 0.49 · σy 0.30'
    notes(s, 'Figures to be added by the presenter (MPM renders are not tracked in the repository). Left: 2D morphology image (file outside the repository; state the 2D conditions and add a length scale). '
             'Right: python3 scripts/viz_mpm_morphology.py --se <SE material points .npy> --scaffold <AM scaffold .csv> --y 0.5 --out morphology.png (actual files required; '
             'the earlier "--slice xz" form does not match the parser). Do not present either image as an independent validation of the other. Sources: CLAUDE.md MPM sections (2026-06-07 … 06-17).')

    # ── 7 ③ SE parameters ───────────────────────────────────────────────
    s = two_column('MPM', 'Effective material inputs and their status',
                   'Bulk modulus from DFT; shear softening and yield stress from a pure-electrolyte calibration sweep.',
                   'Effective material inputs',
                   ['Bulk LPSCl: E ≈ 22 GPa (DFT; DEM input 22.1 GPa [8]); σy 0.05–0.30 GPa',
                    'DEM effective: E = 1.35 GPa — reproduces compaction, not a property',
                    'MPM: E = 1.53 GPa, ν = 0.49, σy = 0.30 GPa; K = 25.5 ≈ DFT 26.2 GPa'],
                   'Calibration target and limits',
                   ['Calibration target: pure-SE porosity 10 % at 300 MPa (lab reference sample, unpublished)',
                    'Not a literature anchor; the earlier attribution was withdrawn',
                    'Shear-only softening keeps the real bulk modulus (ν = 0.49)'],
                   bottom=[('Tested alternatives (volumetric cap, real E) did not remove the need for effective parameters.', BLUE)])
    D[7] = 'CLAUDE.md 3D MPM (ν 0.49 · K 25.5 ≈ B0 26.23); DFT E_VRH 22.06; Bazzoun 2026 E_SE 22.1; CL-94 (10 % = calibration target, source unverified); DPC cross-check'
    notes(s, 'Sources: CLAUDE.md "3D MPM compaction — 3-fix calibration" (K = E/(3(1−2ν)) = 25.5 GPa vs DFT B0 26.23); our DFT E_VRH 22.06 GPa; Bazzoun 2026 [8] uses E_SE = 22.1 GPa for Li6PS5Cl; '
             'the sulfide-glass value 24 GPa (75Li2S·25P2S5, Sakuda 2013 [15]) is a different material system and is not used on the slide. '
             'σy = 0.30 GPa was selected in the pure-SE calibration sweep (0.15 → 5.6 %, 0.20 → 6.7 %, 0.25 → 9.0 %, 0.30 → 10.0 %), inside the literature range. '
             'Claims ledger CL-94: the pure-SE 10 % value is a calibration target (lab standard sample, unpublished); our earlier literature attribution was withdrawn. '
             '"Tested alternatives" = DPC volumetric cap and real-E runs (docs/mpm_dpc_cap_crosscheck.md); the statement is limited to the tested models.')

    # ── 8 ③ DEM ↔ MPM ───────────────────────────────────────────────────
    s = body_slide('MPM', 'Compaction agreement depends on initialization and loading protocol',
                   ['Historical and current scaffold calculations differ in electrolyte initialization and loading protocol; they are not one validation series.',
                    'AM load sharing remains a candidate explanation for over-compaction; the final hypothesis verdict is pending.'], body_box=(0.61, 1.08, 8.84, 2.20))
    textbox(s, (0.61, 3.50, 8.84, 2.40),
            [[('Scaffold calculations (AM skeleton from the DEM bed)', NAVY, True)],
             [('· Earlier: cell-filled SE, bidirectional servo — historical, not a DEM-seeded validation', DARK)],
             [('· Current registered runs: DEM-seeded SE, fixed-platen hold — f = 0 completed; f(a) execution failed', DARK)],
             [('· AM-load-sharing hypothesis: verdict pending', DARK)]], 'Status box', size=14, line=1.2)
    for p_ in shape(s, 'Status box').text_frame.paragraphs:
        p_.alignment = 1   # left
    D[8] = 'CLAUDE.md scaffold sections + 09-09 correction (CDX-16); fam_platen_prereg §11 · §12-6-2 (f = 0 completed, f(a) EXECUTION_FAILED, verdict unassigned); Codex SEM-02 minimal wording'
    notes(s, 'Sources: CLAUDE.md "DEM→MPM SCAFFOLD" and the 2026-09-09 correction (porosity agreement = same geometry, not independent); docs/mpm3d_calibration.md (earlier cell-filled SE, servo); '
             'docs/reviews/fam_platen_prereg_20260812.md §11 (R1 over-compaction) and §12-6-2 (f = 0 completed with I0 false; f(a) EXECUTION_FAILED; four-cell verdict unassigned). '
             'The earlier thickness agreement (30.7 vs 30.28 µm) is not shown: it comes from a different initialization and loading protocol and cannot serve as the validation value of the DEM-seeded runs (SEM-02). '
             'No figure: a side-by-side comparison requires the same initialization, loading history and state.')

    # ── 9 ④ Voxelization ────────────────────────────────────────────────
    s = body_slide('Transport', 'Voxelizing the compacted microstructure into a transport mesh',
                   ['Finite-volume conservation on the phase grid gives electrical (σ, φ) and thermal (κ, T) transport on the same structure.',
                    'Faces are joined by a harmonic mean with no interface-resistance term: an ideal-interface voxel model — an upper bound only within the same geometry, properties and boundaries.'],
                   body_box=(0.61, 1.08, 8.84, 2.20))
    fig_placeholder(s, (0.60, 3.40, 4.30, 2.60), 'voxelized phase grid of a compacted bed (mid-plane slice; AM · SE · pore · additives)')
    fig_placeholder(s, (5.10, 3.40, 4.30, 2.60), 'electronic current-density field at 1 V')
    caption(s, (0.60, 6.10, 4.30, 0.40), 'Phase grid (figure pending)')
    caption(s, (5.10, 6.10, 4.30, 0.40), 'Current density at 1 V (figure pending)')
    D[9] = 'CLAUDE.md §5 two-solver table; CL-81 (ideal-interface / contact-free branch; 4.04× median is model-internal)'
    notes(s, 'Sources: CLAUDE.md "σ 를 내는 솔버는 둘이다" table and CL-81. The voxel solver has no interface-resistance term by default (the film mechanism exists but is off): '
             'this makes it an ideal-interface model and an upper bound only for the same geometry, phase properties and boundary conditions — not a physical upper bound; '
             'geometric necks still cost resistance inside the voxel grid. The 4.04× (contact-free / full network, n = 157) is a ratio inside the contact-network model. '
             'Pending figures: STEP3 phase grid (full sid grid, origin, voxel size, phase mapping, electrode rule, run hash) and the 1 V current-density field of the same solution (A cm⁻²).')

    # ── 10 ⑤ Additives ──────────────────────────────────────────────────
    s = body_slide('Transport', 'Additive geometry used in transport rasterization',
                   ['Carbon fibres (VGCF) as diameter-preserving segments, PTFE as a centre-line insulator, a conductive polymer as true-diameter spheres.',
                    'Pre-registered 104-arm study: the electronic-conductivity order across 1–4 wt% VGCF holds across the tested voxel sizes and grid-origin offsets (72/72).'],
                   body_box=(0.61, 1.08, 8.84, 2.05))
    place_pic(s, repo / 'docs/figures/additive_seed_vgcf_ptfe.png', (0.45, 3.25, 2.75, 2.75))
    place_pic(s, repo / 'docs/figures/additives_preview.png', (3.30, 3.25, 2.75, 2.75))
    place_pic(s, repo / 'docs/report_20261021/previews/G6.png', (6.15, 3.05, 3.50, 3.05))
    caption(s, (0.45, 6.10, 2.75, 0.55), ['Additive seeding illustration', 'not a production stamp'])
    caption(s, (3.30, 6.10, 2.75, 0.55), ['Synthetic morphology example', 'not a production stamp'])
    caption(s, (6.15, 6.10, 3.50, 0.55), ['σ(e⁻) vs VGCF wt% at three voxel sizes', 'campaign values; contact resistance not included'])
    D[10] = 'CL-60 (centerline); phase_a_rep100 README (ORDER-ROBUST 72/72, replay 0.00000 %); report_20261021 G6'
    notes(s, 'Sources: docs/data/phase_a_rep100_20260930/README.md (104 arms, 72/72 adjacent-composition comparisons with no threshold violation; order only is the registered estimand; '
             'increments are technical report only; replay difference 0.00000 %); docs/report_20261021 G6 (voxel σe means; contact resistance not included). '
             'Left and centre panels are illustrations (seeding schematic; synthetic preview that includes additive types not used in Phase A) — they do not demonstrate the fidelity of the production VGCF/PTFE stamps. '
             'Stamp conventions: CLAUDE.md SR-01 (sphere stamp, centerline PTFE = CL-60).')

    # ── 11 ⑥ grid ──────────────────────────────────────────────────────
    s = body_slide('Limits', 'Problem 1: Grid dependence',
                   ['The electronic ratio decreases across the three tested voxel spacings (0.4, 0.3, 0.25 µm); the ionic ratio crosses 1.',
                    'Grid convergence has not been established.'])
    place_pic(s, figs / 'F2_grid_dependence.png', (0.65, 2.85, 5.20, 3.15))
    textbox(s, (6.05, 3.05, 3.30, 1.40), [[('No converged conductivity ratio is reported.', DARK)]], 'Side box', size=15, line=1.2)
    caption(s, (0.65, 6.10, 5.20, 0.55), ['Conductivity ratio, with / without conductive polymer, vs voxel size', 'same bed pair and convention'])
    D[11] = 'CL-24 (live: 1.4215 → 1.1621 → 1.0849; 1.0742 → 0.9926 → 0.9908); CL-41 hold (finer-grid values not quotable); CL-72 (lower-bound claim retracted); Codex SEM-03'
    notes(s, 'Sources: claims ledger CL-24 (public values at vox 0.4/0.3/0.25); CL-41 (vox ≤ 0.15 values on hold — not shown); CL-72 ("lower bound" retracted). '
             'The three public points admit an exact power-law fit (three points, three parameters), so no statement about power laws or extrapolation is made from them (SEM-03); '
             'the earlier manuscript headline at 0.4 µm is superseded. Finer grids reach the memory limit of one GPU (peak RSS 35.6 GB at vox 0.115; 0.10 µm ≈ 54 GB).')

    # ── 12 ⑥ absolute σ_e ──────────────────────────────────────────────
    s = body_slide('Limits', 'Problem 2: Absolute electronic conductivity',
                   ['Voxel predictions exceed the available DC-polarization estimates; measurement conditions remain unverified.',
                    'The NCM–SE comparison uses a common reference conductivity and a specified contact model.'])
    place_pic(s, figs / 'F3_sigma_e_model_vs_exp.png', (0.60, 2.95, 4.35, 3.00))
    place_pic(s, figs / 'F4_ps45_sigma_e.png', (5.10, 2.95, 4.35, 3.00))
    caption(s, (0.60, 6.10, 4.35, 0.65), ['Model and DC-polarization estimates — log scale', 'conditions not yet matched'])
    caption(s, (5.10, 6.10, 4.35, 0.65), ['Carbon- and binder-free NCM–SE beds; Hertz H0 contacts', 'common NCM reference 4.1 mS cm⁻¹ [16]; empirical size factor off; one bed per composition'])
    D[12] = 'sdcp_sigma_e_dcp_anchor_registration_20261012 (54.0 · 70.6 ↔ 4.47 · 12.4); ps45_sigmae_factor_off_20261013 (0.391 · 0.406 · 0.402 · 0.375 · 0.467); Codex §6-1 footnote; Wang 2018 (NMC811 4.1e-3 S/cm)'
    notes(s, 'Sources: docs/reviews/sdcp_sigma_e_dcp_anchor_registration_20261012.md (DC-polarization values 4.47 and 12.4 mS/cm, measurement conditions unverified; model 54.0 and 70.6; re-run registered, no results yet); '
             'docs/data/ps45_sigmae_factor_off_20261013/README.md (0.391 · 0.406 · 0.402 · 0.375 · 0.467 mS/cm; raw minimum 0.3747). Footnote for the right panel (Codex §6-1): computed effective electronic conductivity of the '
             'DEM particle arrangement; Hertz H0 / Holm–Maxwell constriction; common reference conductivity 4.1 mS/cm for polycrystalline and single-crystal NCM (Wang 2018 [16], SPS pellet NMC811 at 20 °C, designated reference); '
             'no empirical size factor; absolute values conditional on this reference and contact model; single bed per composition, scatter not evaluated; carbon- and binder-free AM–SE composite.')

    # ── 13 ⑥ compaction / load ─────────────────────────────────────────
    s = body_slide('Limits', 'Problem 3: Load sharing during compaction',
                   ['NCM–NCM contacts contribute 48–60 % of vertical stress after relaxation at fixed platen position; 7:3 is the minimum.',
                    'The porosity ranking agrees for the selected five compositions (exploratory comparison, n = 5).'])
    place_pic(s, repo / 'docs/data/ps45_plane_load_20261007/slide/contribution_sigma_zz.png', (0.50, 2.95, 4.25, 3.00))
    place_pic(s, repo / 'docs/data/ps73_compaction_curve_20261006/stages_20261012/aligned_ckpt/t3_vm_se/ps73_se_vm3d_4panel_nowall_linear_0_150_preview.png', (4.95, 3.10, 4.65, 2.80))
    caption(s, (0.50, 6.03, 4.25, 0.58), ['Contribution to σ_zz by contact type', '21 planes, load-weighted; relaxed at fixed platen'])
    caption(s, (4.95, 6.03, 4.65, 0.58), ['SE von Mises stress, four stages', '0–150 MPa; wall SE excluded'])
    D[13] = 'ps45_plane_load_20261007 (AM–AM 59.56 · 54.63 · 52.37 · 48.46 · 56.91 %, all NCM–NCM contacts; mean plane load 158–175 MPa); RB-01/02 (interpretation on hold); ps73 stages §6 (SE σ_VM)'
    notes(s, 'Sources: docs/data/ps45_plane_load_20261007/ps45_v2/plane_load.json (21-plane load-weighted AM–AM share: 59.56 · 54.63 · 52.37 · 48.46 · 56.91 % for 0:10 → 10:0; '
             'all NCM–NCM contacts, not large–large — the 0:10 bed has no large particles); state = relaxed at fixed platen (mean plane load 158–175 MPa, not the 300 MPa peak). '
             'Codex 2026-10-09 verdict: correlation observed; "springback" interpretation and stiffness inversion on hold (RB-01/RB-02); experimental thickness = selected 3-of-n average. '
             'SE stress figure: ps73 stages README §6 (wall SE excluded, linear 0–150 MPa).')

    # ── 14 ⑦ registered studies ─────────────────────────────────────────
    s = dup_slide(prs, P['dashed'])
    set_runs_text(shape(s, 'TextBox 20').text_frame, 'Progress')
    set_body(shape(s, 'Rectangle 4'), 'Registered studies and current status',
             ['Registered before launch, reviewed externally; the table shows the ledger state, not result claims.'])
    place(shape(s, 'Rectangle 4'), (0.61, 1.08, 8.84, 1.05))
    set_text(shape(s, 'Frame title'), 'Study status', size=15, bold=True)
    for r in shape(s, 'Frame title').text_frame.paragraphs[0].runs:
        r.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
    place(shape(s, 'Dashed frame'), (0.55, 2.40, 8.90, 3.25))
    shape(s, 'Dashed frame').line.color.rgb = RGBColor(0x9C, 0xA3, 0xAF)
    # 다섯째 행 = 넷째 행 복제
    for nm in ('Item', 'Note'):
        el = copy.deepcopy(shape(s, f'{nm} 4')._element)
        s.shapes._spTree.append(el)
        s.shapes[-1].name = f'{nm} 5'
    rows = [('Historical eight-origin study', 'Conductivity estimates and inference remain on hold'),
            ('VGCF ordering study (104 arms)', 'Ordering holds across tested grids and offsets (72/72)'),
            ('Absolute-conductivity comparison [12]', 'R = 2.07 (Tier 1); Q = 0.84'),
            ('194-bed dataset v1.2', 'Released for conditional use as model descriptors'),
            ('Updated transport software', 'Seven reviews completed; production remains pending')]
    ys = (2.72, 3.26, 3.80, 4.34, 4.88)
    for i, ((a, b), y) in enumerate(zip(rows, ys), 1):
        set_text(shape(s, f'Item {i}'), f'{i}.\t{a}', size=14); place(shape(s, f'Item {i}'), (0.80, y, 3.75, 0.48))
        set_text(shape(s, f'Note {i}'), b, size=14); place(shape(s, f'Note {i}'), (4.75, y, 4.55, 0.48))
    drop(s, 'Down arrow')
    set_text(shape(s, 'Conclusion'), [('R: model / literature conductivity. Q: conductivity retained after PTFE treatment (registered model-sensitivity prediction).', DARK)], size=12)
    place(shape(s, 'Conclusion'), (0.80, 5.85, 8.60, 0.58))
    D[14] = 'sdcp_gain_prereg_v2 (inference on hold: CL-33/34/41); phase_a_rep100 README; lee_abs_sigma_e_prereg §5 (R 2.074, Q 0.840); release v1.2 README; codex gen-2 reverify 7 (software GO, production pending); Codex SEM-05/06'
    notes(s, 'Sources: docs/reviews/sdcp_gain_prereg_v2_20260816.md — the eight-origin (voxel 0.15 µm) study: numerical ratios and the h1 inference are on hold in the claims ledger (CL-33/34/41), so no result is reported; '
             'docs/data/phase_a_rep100_20260930/README.md (104 arms; 72/72; replay 0.00000 %); docs/reviews/lee_abs_sigma_e_prereg_20260923.md §5 (R = 2.074 ± 0.004, Tier 1 "order-of-magnitude", not "within band"; '
             'Q = 0.840 = registered model-sensitivity prediction met, not an experimental hit; comparison with Lee 2025 [12]); docs/data/lhs_release_20261006_v12/README.md (v1.2 released for conditional use as model descriptors); '
             'docs/reviews/codex_review_gen2_network_reverify7_20261012.md (seven software re-verification rounds completed; the updated 194-bed production run, v1.3 and the 20-bed extension are not yet launched or approved). '
             '"Origin" = voxel-grid origin offsets of the same bed, not independent replicate beds.')

    # ── 15 ⑦ dataset ───────────────────────────────────────────────────
    s = body_slide('Progress', 'A 194-bed design-of-experiments dataset for machine learning',
                   ['130 + 64 Latin-hypercube beds (composition, particle sizes) → structure and transport descriptors, released as v1.2 (conditional use as model descriptors).',
                    'SE percolation 106/130; geometric shortest-path tortuosity 1.3–4.2 (percolating beds; not transport tortuosity).'], body_box=(0.61, 1.08, 8.84, 2.05))
    place_pic(s, repo / 'docs/report_20261021/previews/G5a.png', (0.55, 3.35, 4.30, 2.65))
    place_pic(s, repo / 'docs/report_20261021/previews/G3.png', (5.05, 3.35, 4.30, 2.65))
    caption(s, (0.55, 6.10, 4.30, 0.55), ['Geometric tortuosity vs SE fraction (130 beds)', '× = no percolating SE path (24 beds)'])
    caption(s, (5.05, 6.10, 4.30, 0.55), ['Porosity vs SE fraction', '130 + 64 beds'])
    D[15] = 'release v1.2 README; report_20261021 G3 · G5a (G5b moved to notes); lhs_ml_crosscheck_20261005 (notes only, no comparison claim)'
    notes(s, 'Sources: docs/data/lhs_release_20261006_v12/README.md (130 × 132 and 64 × 131; physical-target HOLD 59/130 and 62/64 — released as model descriptors, not validated physical targets); '
             'docs/report_20261021/summary.json (G5: span 106/130; finite geometric tortuosity 1.29–4.15 over the 130-bed set; G5b = ionically isolated AM, not shown). '
             'Loading is not a free design axis (derived from thickness and composition). The collaborator porosity model (OOF R² 0.99) and our five-knob fit (0.98) use unverified and different CV protocols; no comparison is claimed.')

    # ── 16 ⑧ future ────────────────────────────────────────────────────
    s = two_column('Plan', 'Tests for unresolved model limits',
                   'Grid sensitivity remains unresolved. Diagnostic results exist, while final hypothesis verdicts remain pending.',
                   'Electronic transport',
                   ['Interface resistance: film model implemented, production on hold',
                    'Carbon conductivity: comparison with DC polarization',
                    'NCM conductivity: literature-based input review'],
                   'Compaction and mixing',
                   ['AM load sharing: final hypothesis verdict pending',
                    'Unloading: springback and measured thickness',
                    'Mixing: an adhesion parameter for SE–SE contacts'],
                   bottom=[('Pending: ', BLUE), ('separate launch approvals for the updated 194-bed run and the 20-bed extension.', DARK)])
    D[16] = 'Rint v3.1; fam_platen_prereg §12; dem_unloading_ps45_prereg §13; hetero_thesis §4; gen-2 reverify 7 (launch approval separate)'
    notes(s, 'Sources: docs/reviews/contact_resistance_pipeline_draft_v3_1_20261007.md; docs/reviews/fam_platen_prereg_20260812.md §12; docs/reviews/dem_unloading_ps45_prereg_20261009.md §12–13; docs/hetero_thesis.md §4. '
             'Grid sensitivity: no new grid campaign is promised here. The updated 194-bed production run and the 20-bed extension have separate launch approvals pending (software review complete).')

    # ── 17 Summary ─────────────────────────────────────────────────────
    s = dup_slide(prs, P['summary'])
    set_runs_text(shape(s, 'TextBox 20').text_frame, 'Summary')
    set_body(shape(s, 'Rectangle 4'), 'Current findings and limitations',
             [[('DEM and contact networks: ', BLUE), ('composition trends from one bed per composition', None)],
              [('MPM: ', BLUE), ('plastic deformation, with compaction agreement dependent on initialization and loading protocol', None)],
              [('Voxel transport: ', BLUE), ('ideal-interface calculations with grid dependence and unresolved absolute conductivity', None)],
              [('Final model-validation verdicts remain pending', None)]], line=1.3, after=8)
    place(shape(s, 'Rectangle 4'), (0.61, 1.08, 8.84, 3.75))
    drop(s, 'Conclusion')
    D[17] = 'summary of slides 3–16 (Codex SEM-01/06 wording)'
    notes(s, 'Summary; no new numbers. No universal guarantee about registration or verification is claimed (SEM-06).')

    # ── 18 References ──────────────────────────────────────────────────
    s = dup_slide(prs, P['refs'])
    set_runs_text(shape(s, 'TextBox 20').text_frame, 'References')
    left = [('h', 'Contact mechanics and DEM'),
            '[1] S. Luding, Granul. Matter 10, 235–246 (2008)',
            '[2] C. Thornton, Z. Ning, Powder Technol. 99, 154–162 (1998)',
            '[3] M. Paulick, M. Morgeneyer, A. Kwade, Powder Technol. 283, 66–76 (2015)',
            '[4] C.J. Coetzee, Powder Technol. 310, 104–142 (2017)',
            '[5] K. Giannis et al., Granul. Matter 23, 17 (2021)',
            '[6] W. Zunker, K. Kamrin, J. Mech. Phys. Solids 183, 105492 (2024)',
            '[7] LIGGGHTS-PUBLIC 3.8.0 (commit 3d5c00f, 2024), github.com/CFDEMproject/LIGGGHTS-PUBLIC',
            '[15] A. Sakuda, A. Hayashi, M. Tatsumisago, Sci. Rep. 3, 2261 (2013)']
    right = [('h', 'Solid-state battery electrodes'),
             '[8] A.M. Bazzoun et al., J. Power Sources 661, 238682 (2026)',
             '[9] M. So et al., J. Power Sources 508, 230344 (2021)',
             '[10] C.A. Varkey et al., Adv. Powder Technol. 37, 105338 (2026)',
             '[11] T. Shi et al., Adv. Energy Mater. 10, 1902881 (2020)',
             '[12] D.J. Lee et al., Nat. Commun. 16, 4200 (2025)',
             '[13] P. Minnmann et al., J. Electrochem. Soc. 168, 040537 (2021)',
             '[14] V. Miß, F. Lange, S. Staubitz, B. Roling, ACS Appl. Mater. Interfaces 18, 32830–32836 (2026)',
             '[16] S. Wang, M. Yan, Y. Li, C. Vinado, J. Yang, J. Power Sources 393, 75–82 (2018)']
    set_items(shape(s, 'Refs left'), left, size=12, line=1.1, before=3)
    set_items(shape(s, 'Refs right'), right, size=12, line=1.1, before=3)
    place(shape(s, 'Refs left'), (0.50, 1.00, 4.45, 5.85))
    place(shape(s, 'Refs right'), (5.05, 1.00, 4.45, 5.85))
    D[18] = 'references from canonical literature cards only (+ [15] sakuda2013_sulfide_mechanical_property, [16] wang2018_lco_nmc_electronic_ionic_conductivity_vs_ni)'
    notes(s, 'All entries are taken from the canonical literature cards (original PDFs); no bibliographic field was filled from memory. '
             'The constriction law (Holm/Maxwell) and the MLS-MPM numerical method have no canonical card yet and are cited as the models used, without a bibliographic entry.')

    # ── 19 Thank you ──────────────────────────────────────────────────
    s = dup_slide(prs, P['thanks'])
    D[19] = 'closing'

    # 원래 장 삭제 (프로토타입 포함)
    sldIdLst = prs.slides._sldIdLst
    ids = list(sldIdLst)[:n_orig]
    for sld in ids:
        rId = sld.get('{%s}id' % NS['r'])
        prs.part.drop_rel(rId)
        sldIdLst.remove(sld)
    prs.save(out)
    Path(str(out) + '.sources.json').write_text(json.dumps(D, ensure_ascii=False, indent=1), encoding='utf-8')
    return D


# ───────────────────────────── 검사 ─────────────────────────────

FOOT = {'HANYANG UNIVERSITY', 'Battery Materials Lab.'}
#: Codex 10-13 가 지적한 문구 — 어느 장 본문 · notes 에도 남으면 안 된다 (SEM-01~06 · 11 · 14)
FORBIDDEN = ['Large–large', 'large–large', 'follow no power law', 'changes sign', 'never to one another', 'cross-validation',
             'was retracted', 'Every production number', 'nothing below has a result', '30.7', 'Pressed honestly', 'contact-free branch',
             'Hertz constriction', 'single-crystal LPSCl', 'irreducible', 'closing the three problems', 'gain follows the represented']
INTERNAL = r'\b(?:CL-\d+|SELF-\d+|SEM-\d+|G2RR\d*-\d+|RGL[R0-9]*-\d+|UL-\d+|DEMP-\d+|RB-\d+|MV-\d+|PS45E-\d+|stoic-knuth|pqwtv8|kgy|ibb|uma|WSL)\b'


def deck_text(path):
    prs = Presentation(path)
    out = []
    for s in prs.slides:
        for sh in s.shapes:
            if sh.has_text_frame:
                out.append(sh.text_frame.text)
        if s.has_notes_slide:
            out.append(s.notes_slide.notes_text_frame.text)
    return '\n'.join(out)


def slide_stats(prs):
    """장별 (본문 단어 수 (자리 표시 제외) · 본문 bullet pt 집합 · 캡션 pt 최소)."""
    out = []
    for s in prs.slides:
        words, bullet_pt, cap_pt = 0, set(), []
        for sh in s.shapes:
            if not sh.has_text_frame:
                continue
            t = sh.text_frame.text.strip()
            if not t or t in FOOT or re.fullmatch(r'\d+', t):
                continue
            if sh.name != 'Placeholder':
                words += len(t.split())
            if sh.name == 'Rectangle 4':
                for p in sh.text_frame.paragraphs[1:]:
                    for r in p.runs:
                        if r.font.size:
                            bullet_pt.add(r.font.size.pt)
            if sh.name in ('Caption', 'Placeholder'):
                for p in sh.text_frame.paragraphs:
                    for r in p.runs:
                        if r.font.size:
                            cap_pt.append(r.font.size.pt)
        out.append((words, bullet_pt, min(cap_pt) if cap_pt else None))
    return out


def selftest(out, repo, figs=None, word_cap=100, wide_cap=120, wide=(7, 14, 16)):
    txt = deck_text(out)
    ban = json.loads((Path(repo) / 'docs/reviews/claims.json').read_text(encoding='utf-8')).get('quotation_ban', [])
    pats = [q.get('pattern') if isinstance(q, dict) else q for q in ban]
    hits = [p for p in pats if p and p in txt]
    assert not hits, f'banned strings in deck: {hits}'
    prs = Presentation(out)
    slide_txt = '\n'.join(sh.text_frame.text for s in prs.slides for sh in s.shapes if sh.has_text_frame)
    leak = re.findall(INTERNAL, slide_txt)
    assert not leak, f'internal identifiers on slides: {leak}'
    bad = [f for f in FORBIDDEN if f in slide_txt]   # 슬라이드 본문 기준 (notes 는 '무엇을 안 보이는지' 를 설명해도 된다)
    assert not bad, f'phrases flagged by the Codex review still present: {bad}'
    n = len(prs.slides)
    assert n == 19, n
    stats = slide_stats(prs)
    heavy = [(i, w) for i, (w, _, _) in enumerate(stats, 1) if 2 <= i <= 17 and w > (wide_cap if i in wide else word_cap)]
    assert not heavy, f'slides over {word_cap}/{wide_cap} words (placeholders excluded): {heavy}'
    small = [(i, bp) for i, (_, bp, _) in enumerate(stats, 1) if bp and min(bp) < BODY_PT]
    assert not small, f'body bullets below {BODY_PT} pt: {small}'
    cap_small = [(i, c) for i, (_, _, c) in enumerate(stats, 1) if c is not None and c < CAP_PT]
    assert not cap_small, f'captions below {CAP_PT} pt: {cap_small}'
    if figs:
        svg = (Path(figs) / 'F4_ps45_sigma_e.svg').read_text(encoding='utf-8')
        labels = [k for k in ('0:10', '3:7', '5:5', '7:3', '10:0') if k in svg]
        assert len(labels) == 5, f'F4 composition labels present in svg: {labels}'
    print(f'selftest ok — {n} slides · banned 0 · internal 0 · flagged phrases 0 · max words {max(w for w, _, _ in stats[1:17])} · bullets ≥ {BODY_PT} pt · captions ≥ {CAP_PT} pt')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--template')
    ap.add_argument('--repo', required=True)
    ap.add_argument('--figs', required=True)
    ap.add_argument('--out')
    ap.add_argument('--selftest-only', help='기존 덱 검사만 (생성 없음)')
    a = ap.parse_args()
    if a.selftest_only:
        selftest(a.selftest_only, a.repo, a.figs)
        return
    build(a.template, a.repo, a.figs, a.out)
    selftest(a.out, a.repo, a.figs)
    print('written', a.out)


if __name__ == '__main__':
    main()
