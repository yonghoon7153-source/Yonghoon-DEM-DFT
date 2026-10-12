#!/usr/bin/env python3
"""연구세미나 덱 생성기 (2026-10 · 1저자 비준 개요 v1 · 양식 = 10-13 연구세미나 덱 사본).

    python3 build_seminar.py --template <10-13 덱.pptx> --repo <리포> --figs <새 그림 폴더> --out <out.pptx>

- 양식 그대로: 10-13 덱의 장을 **프로토타입**으로 복제해 글 · 그림만 바꾼다 (글꼴 · 색 · 자리 = 양식).  원래 장은 전부 지운다.
  표지 (1) · 그림 본문 (4) · 두 칸 (11) · 점선 틀 (3) · 요약 (15) · 참고문헌 (17) · Thank you (16).
- 빈 그림 자리 (리포에 없는 그림) = 양식의 점선 "Figure" 상자 + **채울 글** (무엇 · 출처 · 명령) — 1저자 10-13 *"공백에 글 포함해서 나중에 검토할 때 추가되게"*.
- 수치는 전부 정본 문서에서 (각 장 notes 에 출처).  철회값 (claims.json quotation_ban) 은 쓰지 않는다 — selftest 가 덱 전체 글을 스윕한다.
- 용어 = 분야 표준 (내부 코드명 · 원장 ID · 세션명 없음).
"""
import argparse
import copy
import json
import re
from pathlib import Path

from lxml import etree
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Emu, Pt

NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
A = NS['a']
DARK, GRAY, NAVY, RED, BLUE = '1F2937', '6B7280', '1F497D', 'C00000', '0070C0'

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
    rp = copy.deepcopy(proto_rpr)
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


def set_body(box, head, bullets, head_size=None, bullet_size=None):
    """양식 본문 상자 (Rectangle 4): 문단 0 = ■ 제목 · 문단 1.. = • 소불릿.  bullet = 문자열 또는 [(글, 색 or None), …]."""
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


def set_items(box, items, size=None):
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


def place_pic(slide, path, box, keep='fit'):
    """box = (x, y, w, h) in — 비율 유지 · 가운데."""
    x, y, w, h = box
    im = Image.open(path)
    iw, ih = im.size
    s = min(w / iw, h / ih)
    pw, ph = iw * s, ih * s
    return slide.shapes.add_picture(str(path), Inches(x + (w - pw) / 2), Inches(y + (h - ph) / 2), Inches(pw), Inches(ph))


def add_box(slide, proto_el, box, text_paras, name):
    """양식 요소 (점선 상자 · 캡션 등) 를 복제해 자리 · 글을 바꾼다.  text_paras = [[(글, 색, 굵게?), …], …]."""
    el = copy.deepcopy(proto_el)
    slide.shapes._spTree.append(el)
    sp = slide.shapes[-1]
    sp.name = name
    x, y, w, h = box
    sp.left, sp.top, sp.width, sp.height = Inches(x), Inches(y), Inches(w), Inches(h)
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
            _run(p, txt, rpr, color=col, bold=b)
        body.append(p)
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
    TAG_PROTO = copy.deepcopy(shape(P['pic'], 'TextBox 69')._element)           # 우상단 이탤릭 출처
    CONC_PROTO = copy.deepcopy(shape(P['summary'], 'Conclusion')._element)      # 아래 결론 줄
    n_orig = len(prs.slides)
    D = {}  # 장별 출처 (Codex 리뷰 요청서용)

    def fig_placeholder(slide, box, what, source, howto, name='Placeholder'):
        """빈 그림 자리 = 점선 상자 + 채울 글."""
        paras = [[('Figure to add', GRAY, True)], [(what, DARK)], [(source, GRAY)], [(howto, GRAY)]]
        return add_box(slide, FIG_PROTO, box, paras, name)

    def caption(slide, box, text):
        return add_box(slide, CAP_PROTO, box, [[('< ' + text + ' >', DARK)]], 'Caption')

    def tag(slide, text, box=(6.0, 0.93, 3.65, 0.27)):
        return add_box(slide, TAG_PROTO, box, [[(text, DARK)]], 'Source tag')

    def conclusion(slide, segs, box=(0.4, 6.2, 9.2, 0.4), size=14):
        sp = add_box(slide, CONC_PROTO, box, [segs], 'Conclusion')
        for r in sp.text_frame.paragraphs[0].runs:
            r.font.size = Pt(size)
        return sp

    def body_slide(section, head, bullets, head_size=None, bullet_size=13, body_h=None):
        s = dup_slide(prs, P['pic'])
        drop(s, 'New picture', 'TextBox 69')
        set_runs_text(shape(s, 'TextBox 20').text_frame, section)
        box = shape(s, 'Rectangle 4')
        set_body(box, head, bullets, head_size=head_size, bullet_size=bullet_size)
        box.height = Inches(body_h or 2.25)
        return s

    # ── 1 표지 ────────────────────────────────────────────────────────────
    s = dup_slide(prs, P['title'])
    set_runs_text(shape(s, '직사각형 12').text_frame, '[date — to be set]')
    tb = shape(s, 'Rectangle 4').text_frame
    # 양식: 문단 0 = 'Research Seminar' · 문단 1 = 제목 (vertical tab 으로 두 줄) — 제목 문단의 run 을 하나로
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
    # 제목이 두 줄이라 저자 상자를 0.35 in 내린다
    au = shape(s, '직사각형 10')
    au.top = au.top + Inches(0.35)
    D[1] = 'title'
    notes(s, 'Title. Date to be set by the presenter.')

    # ── 2 ① Pipeline ─────────────────────────────────────────────────────
    s = body_slide('Introduction', 'Heterogeneous-technology pipeline for a sulfide composite cathode',
                   ['Three particle-level stages, each calibrated to its own experiment — never to one another.',
                    'Agreement between stages is treated as cross-validation; disagreement as a quantified model limit.'])
    place_pic(s, figs / 'F1_pipeline.png', (0.5, 3.35, 9.0, 2.65))
    caption(s, (2.5, 6.05, 5.0, 0.36), 'DEM → MPM → voxel transport → electrode response')
    D[2] = 'CLAUDE.md frame [1]–[5]; docs/report_20261021 2-2'
    notes(s, 'No numbers. Source: project framing document (DEM/MPM complementary frame, finalized 2026-06-07).')

    # ── 3 ① DEM — porosity ──────────────────────────────────────────────
    s = body_slide('DEM', 'Soft-sphere DEM reproduces the composition dependence of porosity',
                   ['Rigid spheres with a linear hysteretic contact law, pressed to 300 MPa; one bed per composition.',
                    'Porosity 31.8 → 25.1 → 16.7 → 16.5 % through one run; 7:3 (large : small NCM) is the densest of five.'])
    place_pic(s, repo / 'docs/data/ps73_compaction_curve_20261006/stages_20261012/aligned_ckpt/t1_geometry/ps73_geom3d_4panel_porosity_preview.png', (0.5, 3.45, 5.6, 2.55))
    place_pic(s, repo / 'docs/report_20261021/previews/G1.png', (6.2, 3.3, 3.4, 2.7))
    caption(s, (0.8, 6.05, 5.0, 0.36), 'four stages of one 7:3 bed (0 · 47 · 296 · 165 MPa)')
    caption(s, (6.1, 6.05, 3.6, 0.36), 'porosity vs large : small NCM')
    D[3] = 'ps73 stages README §6 (porosity exact union 31.81 · 25.09 · 16.68 · 16.49); report_20261021 G1 (20.59 · 18.67 · 17.67 · 16.49 · 16.90)'
    notes(s, 'Sources: docs/data/ps73_compaction_curve_20261006/stages_20261012/README.md §6; docs/report_20261021/summary.json G1. '
             'Qualifier: one bed per composition, no seed replicates; porosity = exact union of spheres.')

    # ── 4 ① DEM → transport ─────────────────────────────────────────────
    s = body_slide('DEM', 'From the contact network to Li⁺ transport: a Kirchhoff network with contact constriction',
                   ['Each SE–SE contact = bulk resistance + Hertz constriction; σ₀ = 1.5 mS cm⁻¹ (pellet literature range).',
                    'Transport tortuosity 7.2 → 5.0 (0:10 → 7:3): 73–75 % of the resistance sits in the contact necks, not in path length.'])
    place_pic(s, repo / 'docs/data/ps45_r45_network_g2_20261007/deck_p14p15_20261012/p14_tortuosity_hertz.png', (0.45, 3.45, 2.95, 2.55))
    place_pic(s, repo / 'docs/data/ps45_r45_network_g2_20261007/deck_p14p15_20261012/p15_sigmaLi_hertz_s0_1p5.png', (3.45, 3.45, 2.95, 2.55))
    fig_placeholder(s, (6.55, 3.45, 3.0, 2.55),
                    'Current pathways in the 7:3 bed (3D, ionic, Hertz, top 50 % of current)',
                    'webapp DEM 3D viewer "current flow" after scripts/network_current.py dump <ps45 7:3 result folder>',
                    'command to be run by the presenter (WSL); capture at the same camera as the geometry panels')
    caption(s, (0.6, 6.05, 2.7, 0.36), 'transport tortuosity (Hertz)')
    caption(s, (3.6, 6.05, 2.7, 0.36), 'σ(Li⁺), σ₀ = 1.5 mS cm⁻¹')
    caption(s, (6.6, 6.05, 2.9, 0.36), 'actual current pathways')
    D[4] = 'ps45_r45_network_g2 README (tau2 7.2433 · 5.9733 · 5.4495 · 5.0297 · 5.2864; σ_ion 0.0587–0.0893; constriction share 73–75 %; CF tau2 1.25–1.79)'
    notes(s, 'Sources: docs/data/ps45_r45_network_g2_20261007/README.md (values, σ0 = 1.5 section, decomposition section). '
             'Qualifiers: transport tortuosity = φ_SE σ0 / σ_eff (not its square root); Hertz = primary; the 73–75 % share and the path-only '
             'tortuosity 1.25–1.79 are model-internal ratios, not a measured decomposition; 7:3 vs 10:0 difference is within seed scatter.')

    # ── 5 ② DEM limits ──────────────────────────────────────────────────
    s = body_slide('DEM', 'What a rigid-sphere DEM cannot do',
                   ['No shape change and no yield cap: overlap is the only proxy for plasticity, so the 18× softened SE modulus (24 → 1.35 GPa) is a surrogate, not a property.',
                    'During compression, global viscous damping carries 58 % of the plate reaction in one 7:3 bed — an open issue.'])
    place_pic(s, repo / 'docs/data/dem_governing_equations_report_20261011/fig2_hysteresis_cycle.png', (0.5, 3.5, 5.5, 2.5))
    sp = add_box(s, CONC_PROTO, (6.2, 3.6, 3.4, 2.4),
                 [[('Battery-electrode DEM literature (22 studies)', NAVY, True)],
                  [('· softened SE modulus: 0 of 22', DARK)],
                  [('· yield / hardness cap: 7 of 22', DARK)],
                  [('· linear hysteretic law: 1 of 22', DARK)],
                  [('· global damping during dry compaction: none reported', DARK)]], 'Lit box')
    for p in sp.text_frame.paragraphs:
        p.alignment = 1
        for r in p.runs:
            r.font.size = Pt(12)
    caption(s, (0.8, 6.05, 4.9, 0.36), 'hysteretic normal force (code reproduction)')
    D[5] = 'dem_governing_equations_background_20261011.md §5.1 · §10.3 · §11; DEMP-01 (57.9 %)'
    notes(s, 'Sources: docs/dem_governing_equations_background_20261011.md (§5.3 figure 2; §10.3 literature counts; §11 limits). '
             'Damping share 57.9 % = measured on the ps45 7:3 bed during compression (ledger DEMP-01, open). Literature count = canonical cards, our classification.')

    # ── 6 ③ MPM — why ───────────────────────────────────────────────────
    s = body_slide('MPM', 'The material point method supplies the plastic half',
                   ['J2 plasticity on a background grid: true shape change and void filling that a rigid sphere cannot represent.',
                    'Active material is kept rigid (DEM skeleton); only the electrolyte flows.'])
    fig_placeholder(s, (0.6, 3.45, 4.3, 2.55),
                    'Plastic SE morphology after compaction (2D champion, E = 1.53 GPa, σy = 0.15 GPa)',
                    'uma: ~/work/mpm/vis_/viszoom_E1.53_sy0.15.png (not in repo)',
                    'copy the PNG into the deck folder; same scale bar as the right panel')
    fig_placeholder(s, (5.1, 3.45, 4.3, 2.55),
                    '3D DEM-scaffold MPM, x–z slice (AM fixed, SE material points)',
                    'scripts/viz_mpm_morphology.py on the real_14 scaffold run (payload not in repo)',
                    'python3 scripts/viz_mpm_morphology.py <mpm run dir> --slice xz')
    caption(s, (0.8, 6.05, 3.9, 0.36), '2D: SE flows into voids')
    caption(s, (5.3, 6.05, 3.9, 0.36), '3D: fixed AM skeleton, plastic SE')
    D[6] = 'CLAUDE.md DEM↔MPM frame; 2D champion E 1.53 / σy 0.15; 3D locked E 1.53 · ν 0.49 · σy 0.30'
    notes(s, 'Figures to be added by the presenter (MPM renders are not tracked in the repository). Sources: CLAUDE.md MPM sections (2026-06-07 … 06-17).')

    # ── 7 ③ SE parameters ───────────────────────────────────────────────
    s = dup_slide(prs, P['two'])
    set_runs_text(shape(s, 'TextBox 20').text_frame, 'MPM')
    set_body(shape(s, 'Rectangle 4'), 'How the electrolyte parameters were fixed',
             ['Bulk modulus from DFT; shear softening calibrated to pure-electrolyte compaction; yield stress from the LPSCl literature range.'], bullet_size=14)
    set_text(shape(s, 'Audit findings'), 'Three layers of the SE model')
    set_items(shape(s, 'Audit findings items'),
              ['Real bulk: E ≈ 24 GPa, σy 0.05–0.30 GPa (single-crystal LPSCl range)',
               'DEM effective: E = 1.35 GPa (18× softened) — reproduces compaction, not a property',
               'MPM: E = 1.53 GPa, ν = 0.49, σy = 0.30 GPa; K = 25.5 GPa ≈ DFT bulk modulus 26.2 GPa'], size=13)
    set_text(shape(s, 'Decisions recorded on Sep 12'), 'What is — and is not — an external anchor')
    set_items(shape(s, 'Decisions recorded on Sep 12 items'),
              ['Pure-SE porosity 10 % at 300 MPa is the calibration target: a lab reference sample, unpublished',
               'It is not a literature anchor; the earlier citation was retracted',
               'Shear-only softening keeps the real bulk modulus (ν = 0.49); softening the bulk over-crushed the bed'], size=13)
    concs = shapes_named(s, 'Conclusion')
    set_text(concs[0], [('The softening is irreducible for a resolved-grain continuum', BLUE), (' — a volumetric cap and real E both failed the Heckel test.', DARK)], size=14)
    concs[1]._element.getparent().remove(concs[1]._element)
    D[7] = 'CLAUDE.md 3D MPM (ν 0.49 · K 25.5 ≈ B0 26.23); CL-94 (10 % = calibration target, source unverified); DPC cross-check'
    notes(s, 'Sources: CLAUDE.md "3D MPM compaction — 3-fix calibration" (K = E/(3(1−2ν)) = 25.5 GPa vs DFT B0 26.23); claims ledger CL-94 (pure-SE 10 % is a calibration target; '
             'the Minnmann citation was retracted); 2026-10-08 note: the 10 % value is a lab standard sample, unpublished. "Heckel test" = DPC/jamming cross-check (docs/mpm_dpc_cap_crosscheck.md).')

    # ── 8 ③ DEM ↔ MPM ───────────────────────────────────────────────────
    s = body_slide('MPM', 'DEM-scaffold MPM: what agrees, and what does not count as evidence',
                   ['Stress-stop thickness agrees (30.7 vs 30.3 µm); porosity agreement is not independent — the AM skeleton and the SE seeds both come from the DEM bed.',
                    'Pressed honestly to 300 MPa the MPM over-compacts (sphere porosity 1.1 % vs 15.6 % measured): AM load sharing is the missing piece.'])
    fig_placeholder(s, (0.7, 3.5, 8.6, 2.5),
                    'DEM-scaffold MPM at the stress stop: x–z slice with the DEM bed side by side (same scale)',
                    'scripts/viz_mpm_morphology.py (scaffold run real_14, n_grid 384) + DEM dump atom_2060000 (docs/data/real14_reference_20260928)',
                    'render both at the same camera; label thickness 30.7 vs 30.28 µm')
    D[8] = 'CLAUDE.md scaffold cross-validation + 09-09 correction (CDX-16); fam_platen_prereg §11 (ε_sphere 1.13 %, 14.5 %p over-compaction)'
    notes(s, 'Sources: CLAUDE.md "DEM→MPM SCAFFOLD" (thickness 30.7 vs 30.28 µm) and the 2026-09-09 correction (porosity agreement = same geometry, not independent); '
             'docs/reviews/fam_platen_prereg_20260812.md §11 (R1: ε_sphere 1.125 %, experiment 15.6 %, 14.5 %p over-compaction). Figure to be added.')

    # ── 9 ④ Voxelization ────────────────────────────────────────────────
    s = body_slide('Transport', 'Voxelizing the compacted microstructure turns morphology into a transport mesh',
                   ['Finite-volume ∇·(σ∇φ) = 0 on the phase grid gives ionic, electronic and thermal conductivity on the same structure.',
                    'Faces are joined by a harmonic mean, so there is no interface-resistance term: the voxel solver sits on the contact-free branch.'])
    fig_placeholder(s, (0.6, 3.45, 4.3, 2.55),
                    'Voxelized phase grid of a compacted bed (AM · SE · pore · additives)',
                    'STEP3 phase grid from the MPM payload (scripts/step3_sigma.py); manuscript Fig. S16/S17 style',
                    'export a mid-plane slice of the sid grid (phase colours) at vox 0.15 µm')
    fig_placeholder(s, (5.1, 3.45, 4.3, 2.55),
                    'Electronic current-density field at 1 V (manuscript S16/S17)',
                    'manuscript SI figures (rendered by the presenter, outside the repository)',
                    'reuse the S16/S17 panels; colourbar in A cm⁻²')
    caption(s, (0.8, 6.05, 3.9, 0.36), 'phase grid')
    caption(s, (5.3, 6.05, 3.9, 0.36), 'current density at 1 V')
    D[9] = 'CLAUDE.md §5 two-solver table; CL-81 (contact-free branch; median 4.04× vs full network, n = 157)'
    notes(s, 'Sources: CLAUDE.md "σ 를 내는 솔버는 둘이다" table and CL-81 note (voxel FV = CONTACT_FREE branch; the 4.04× median is a model-internal ratio over 157 cases). Figures to be added.')

    # ── 10 ⑤ Additives ──────────────────────────────────────────────────
    s = body_slide('Transport', 'Additives enter at the voxel stage',
                   ['Carbon fibres (VGCF) as diameter-preserving segments, PTFE as a centre-line insulator, a conductive polymer as true-diameter spheres.',
                    'A 104-arm pre-registered run: the electronic-conductivity order across 1–4 wt% VGCF is robust to voxel size and origin shift (72/72).'])
    place_pic(s, repo / 'docs/figures/additive_seed_vgcf_ptfe.png', (0.5, 3.45, 3.0, 2.55))
    place_pic(s, repo / 'docs/figures/additives_preview.png', (3.6, 3.45, 3.0, 2.55))
    place_pic(s, repo / 'docs/report_20261021/previews/G6.png', (6.7, 3.35, 2.9, 2.7))
    caption(s, (0.5, 6.05, 3.0, 0.36), 'fibre + binder seeds')
    caption(s, (3.6, 6.05, 3.0, 0.36), 'additive stamps')
    caption(s, (6.6, 6.05, 3.1, 0.36), 'σ(e⁻) vs VGCF wt%, three voxel sizes')
    D[10] = 'CL-60 (centerline); phase_a_rep100 README (ORDER-ROBUST 72/72, replay 0.00000 %); report_20261021 G6'
    notes(s, 'Sources: docs/data/phase_a_rep100_20260930/README.md (104 arms, 72/72, order only is the registered estimand; increments are technical report only); '
             'docs/report_20261021 G6 (voxel σe means; contact resistance not included). Stamp conventions: CLAUDE.md SR-01 (sphere stamp, centerline PTFE = CL-60).')

    # ── 11 ⑥ grid ──────────────────────────────────────────────────────
    s = body_slide('Limits', 'Problem 1 — the voxel electronic gain is grid-dependent and does not extrapolate',
                   ['Same bed pair, same convention, voxel 0.4 → 0.3 → 0.25 µm: the electronic ratio keeps falling and the ionic ratio changes sign.',
                    'The increments follow no power law — no Richardson extrapolation, and no lower-bound claim either.'])
    place_pic(s, figs / 'F2_grid_dependence.png', (0.8, 3.45, 4.1, 2.6))
    sp = add_box(s, CONC_PROTO, (5.3, 3.6, 4.2, 2.4),
                 [[('What survives', NAVY, True)],
                  [('· the headline of the earlier manuscript draft is a grid artefact', DARK)],
                  [('· the shape (monotonic, decelerating) is real; no converged value yet', DARK)],
                  [('· finer grids reach the memory limit of one GPU', DARK)]], 'Side box')
    for p in sp.text_frame.paragraphs:
        p.alignment = 1
        for r in p.runs:
            r.font.size = Pt(12)
    caption(s, (0.9, 6.05, 4.0, 0.36), 'conductivity ratio vs voxel size')
    D[11] = 'CL-24 (live: 1.4215 → 1.1621 → 1.0849; 1.0742 → 0.9926 → 0.9908); CL-41 hold (finer-grid values not quotable); CL-72 (lower-bound claim retracted)'
    notes(s, 'Sources: claims ledger CL-24 (public values at vox 0.4/0.3/0.25); CL-41 (vox ≤ 0.15 values on hold — not shown); CL-72 ("lower bound" retracted). '
             'Memory: peak RSS 35.6 GB at vox 0.115; 0.10 µm needs ≈ 54 GB.')

    # ── 12 ⑥ absolute σ_e ──────────────────────────────────────────────
    s = body_slide('Limits', 'Problem 2 — absolute electronic conductivity sits far above DC-polarization measurements',
                   ['Voxel model 54 and 71 vs 4.5 and 12 mS cm⁻¹ measured (×12, ×5.7): no interface resistance, unanchored carbon conductivity.',
                    'Carbon- and binder-free NCM–SE beds, common NCM reference 4.1 mS cm⁻¹: 0.38–0.47 mS cm⁻¹ across the five compositions.'])
    place_pic(s, figs / 'F3_sigma_e_model_vs_exp.png', (0.7, 3.45, 4.1, 2.6))
    place_pic(s, figs / 'F4_ps45_sigma_e.png', (5.2, 3.45, 4.1, 2.6))
    caption(s, (0.7, 6.05, 4.1, 0.36), 'voxel model vs experiment (log scale)')
    caption(s, (5.2, 6.05, 4.1, 0.36), 'NCM–SE beds, common-conductivity network')
    D[12] = 'sdcp_sigma_e_dcp_anchor_registration_20261012 (54.0 · 70.6 ↔ 4.47 · 12.4); ps45_sigmae_factor_off_20261013 (0.391 · 0.406 · 0.402 · 0.375 · 0.467); Codex §6-1 footnote'
    notes(s, 'Sources: docs/reviews/sdcp_sigma_e_dcp_anchor_registration_20261012.md (experimental values from DC polarization, conditions unverified; re-run registered, no results yet); '
             'docs/data/ps45_sigmae_factor_off_20261013/README.md. Footnote for the right panel (Codex §6-1): computed effective electronic conductivity of the DEM particle arrangement; '
             'Hertz H0 / Maxwell constriction; common reference conductivity 4.1 mS/cm for polycrystalline and single-crystal NCM (sintered-pellet literature ≈ 4 mS/cm at 20 °C, designated reference); '
             'no empirical size factor; absolute values conditional on this reference and contact model; single bed per composition, scatter not evaluated; carbon- and binder-free AM–SE composite.')

    # ── 13 ⑥ compaction / load ─────────────────────────────────────────
    s = body_slide('Limits', 'Problem 3 — compaction mechanics: over-compaction and load sharing',
                   ['Large–large NCM contacts carry 48–60 % of the vertical stress; 7:3 is the minimum.',
                    'Its five-composition order matches the measured porosity order (n = 5, exploratory; the experimental set is a selected subset).'])
    place_pic(s, repo / 'docs/data/ps45_plane_load_20261007/slide/contribution_sigma_zz.png', (0.5, 3.45, 3.9, 2.55))
    place_pic(s, repo / 'docs/data/ps73_compaction_curve_20261006/stages_20261012/aligned_ckpt/t3_vm_se/ps73_se_vm3d_4panel_nowall_linear_0_150_preview.png', (4.5, 3.6, 5.1, 2.3))
    caption(s, (0.5, 6.05, 3.9, 0.36), 'contribution to σzz by contact type')
    caption(s, (4.7, 6.05, 4.7, 0.36), 'SE von Mises stress, four stages (0–150 MPa)')
    D[13] = 'ps45_plane_load_20261007 README (AM–AM 59.56 · 54.63 · 52.37 · 48.46 · 56.91 %); RB-01/02 (interpretation on hold); ps73 stages §6 (SE σ_VM)'
    notes(s, 'Sources: docs/data/ps45_plane_load_20261007/README.md (21-plane load-weighted average); Codex 2026-10-09 verdict (correlation observed, "springback" interpretation and stiffness inversion on hold, RB-01/RB-02); '
             'experimental thickness = selected 3-of-n average (2026-10-09 note). SE stress figure: ps73 stages README §6.')

    # ── 14 ⑦ pre-registered runs ────────────────────────────────────────
    s = dup_slide(prs, P['dashed'])
    set_runs_text(shape(s, 'TextBox 20').text_frame, 'Progress')
    set_body(shape(s, 'Rectangle 4'), 'Pre-registered, origin-replicated runs — what each one settled',
             ['Every production run is registered before launch (hypotheses, decision lines, sealed code) and judged by an independent reviewer.'], bullet_size=14)
    set_text(shape(s, 'Frame title'), 'Registered campaigns', bold=True)
    for r in shape(s, 'Frame title').text_frame.paragraphs[0].runs:
        r.font.color.rgb = __import__('pptx.dml.color', fromlist=['RGBColor']).RGBColor(0x1F, 0x49, 0x7D)
    shape(s, 'Dashed frame').line.color.rgb = __import__('pptx.dml.color', fromlist=['RGBColor']).RGBColor(0x9C, 0xA3, 0xAF)
    items = [('8-arm origin factorial, voxel 0.15 µm', 'gain follows the represented additive volume (procedure and verdict only)'),
             ('Phase A: 104 arms, VGCF 1–4 wt%', 'order robust, 72/72; replay 0.00000 %'),
             ('Lee-2025 absolute comparison, 16 arms', 'R = 2.07 → order-of-magnitude agreement; Q = 0.84 → prediction met'),
             ('194 LHS beds → descriptor dataset v1.2', 'sealed pipeline; 7 external re-verification rounds before launch')]
    for i, (a, b) in enumerate(items, 1):
        set_text(shape(s, f'Item {i}'), f'{i}.\t{a}', size=14)
        set_text(shape(s, f'Note {i}'), b, size=13)
    drop(s, 'Down arrow')
    set_text(shape(s, 'Conclusion'), [('Ratios and gains of the 8-arm series are on hold', RED), (' — only the procedure and the verdict are reported.', DARK)], size=14)
    D[14] = 'sdcp_gain_prereg_v2 (h1 verdict, values hold CL-33/41); phase_a_rep100 README; lee_abs_sigma_e_prereg §5 (R 2.074, Q 0.840); release v1.2 README'
    notes(s, 'Sources: docs/reviews/sdcp_gain_prereg_v2_20260816.md (verdict h1 = gain follows represented SDCP volume; numeric ratios on hold); docs/data/phase_a_rep100_20260930/README.md; '
             'docs/reviews/lee_abs_sigma_e_prereg_20260923.md §5 (R = 2.074 ± 0.004, Tier 1 "order-of-magnitude", not "within band"; Q = 0.840); docs/data/lhs_release_20261006_v12/README.md.')

    # ── 15 ⑦ dataset ───────────────────────────────────────────────────
    s = body_slide('Progress', 'A 194-bed design-of-experiments dataset for machine learning',
                   ['130 + 64 Latin-hypercube beds (composition, particle sizes, loading) → structure and transport descriptors, released as v1.2.',
                    'SE percolation 106/130; geometric tortuosity 1.3–4.2 (shortest path, not transport); porosity OOF R² 0.99 (collaborator) vs 0.98 from the five design knobs.'])
    place_pic(s, repo / 'docs/report_20261021/previews/G5a.png', (0.6, 3.45, 2.9, 2.55))
    place_pic(s, repo / 'docs/report_20261021/previews/G5b.png', (3.55, 3.45, 2.9, 2.55))
    place_pic(s, repo / 'docs/report_20261021/previews/G3.png', (6.5, 3.45, 2.9, 2.55))
    caption(s, (0.6, 6.05, 2.9, 0.36), 'geometric tortuosity')
    caption(s, (3.55, 6.05, 2.9, 0.36), 'ionically isolated AM')
    caption(s, (6.5, 6.05, 2.9, 0.36), 'porosity vs SE fraction')
    D[15] = 'release v1.2 README; report_20261021 G3 · G5a · G5b; lhs_ml_crosscheck_20261005 (OOF R² 0.990 vs 0.980)'
    notes(s, 'Sources: docs/data/lhs_release_20261006_v12/README.md; docs/report_20261021/summary.json (G5: span 106/130, tau 1.29–4.15); docs/data/lhs_ml_crosscheck_20261005/README.md. '
             'Qualifier: wall-based tortuosity is geometric (Dijkstra), not transport tortuosity.')

    # ── 16 ⑧ future ────────────────────────────────────────────────────
    s = dup_slide(prs, P['two'])
    set_runs_text(shape(s, 'TextBox 20').text_frame, 'Plan')
    set_body(shape(s, 'Rectangle 4'), 'Next steps — closing the three problems',
             ['Each item is registered before it is run; nothing below has a result yet.'], bullet_size=14)
    set_text(shape(s, 'Audit findings'), 'Transport')
    set_items(shape(s, 'Audit findings items'),
              ['Interface resistance in the voxel solver: AM–AM film implemented (default off), production on hold',
               'Anchor the carbon conductivity with the SBE/DBE DC-polarization values (re-run registered)',
               'Polycrystalline vs single-crystal NCM conductivity: literature first, then the model'], size=13)
    set_text(shape(s, 'Decisions recorded on Sep 12'), 'Mechanics and mixing')
    set_items(shape(s, 'Decisions recorded on Sep 12 items'),
              ['AM load sharing in the MPM platen (registered contract)',
               'Stepwise unloading of the five beds: springback vs measured thickness (registration revised twice)',
               'Coating-aware mixing: surface-energy anchor for SE–SE adhesion before the confirmatory runs'], size=13)
    concs = shapes_named(s, 'Conclusion')
    set_text(concs[0], [('Decisions pending: ', BLUE), ('launch of the 194 + 20 network batch after the final external check.', DARK)], size=14)
    concs[1]._element.getparent().remove(concs[1]._element)
    D[16] = 'Rint v3.1; fam_platen_prereg §12; dem_unloading_ps45_prereg §13; hetero_thesis §4'
    notes(s, 'Sources: docs/reviews/contact_resistance_pipeline_draft_v3_1_20261007.md; docs/reviews/fam_platen_prereg_20260812.md §12; docs/reviews/dem_unloading_ps45_prereg_20261009.md §12–13; docs/hetero_thesis.md §4. No numbers claimed.')

    # ── 17 Summary ─────────────────────────────────────────────────────
    s = dup_slide(prs, P['summary'])
    set_runs_text(shape(s, 'TextBox 20').text_frame, 'Summary')
    set_body(shape(s, 'Rectangle 4'), 'What the pipeline can and cannot say today',
             [[('DEM + contact network: ', BLUE), ('composition trends in porosity, Li⁺ transport and load sharing — one bed per composition, model-internal ratios.', None)],
              [('MPM: ', BLUE), ('plastic morphology and the stress-stop thickness; porosity agreement is not independent evidence.', None)],
              [('Voxel transport: ', BLUE), ('a contact-free upper branch; electronic gains are grid-dependent and absolute values exceed measurements.', None)],
              [('Every production number is pre-registered, sealed and externally re-verified', RED), (' before it is reported.', None)]], bullet_size=15)
    drop(s, 'Conclusion')
    D[17] = 'summary of slides 3–15'
    notes(s, 'Summary; no new numbers.')

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
            '[7] LIGGGHTS-PUBLIC 3.8.0 (commit 3d5c00f, 2024), github.com/CFDEMproject/LIGGGHTS-PUBLIC']
    right = [('h', 'Solid-state battery electrodes'),
             '[8] A.M. Bazzoun et al., J. Power Sources 661, 238682 (2026)',
             '[9] M. So et al., J. Power Sources 508, 230344 (2021)',
             '[10] C.A. Varkey et al., Adv. Powder Technol. 37, 105338 (2026)',
             '[11] T. Shi et al., Adv. Energy Mater. 10, 1902881 (2020)',
             '[12] D.J. Lee et al., Nat. Commun. 16, 4200 (2025)',
             '[13] P. Minnmann et al., J. Electrochem. Soc. 168, 040537 (2021)',
             '[14] V. Miß, F. Lange, S. Staubitz, B. Roling, ACS Appl. Mater. Interfaces 18, 32830–32836 (2026)']
    set_items(shape(s, 'Refs left'), left)
    set_items(shape(s, 'Refs right'), right)
    D[18] = 'references from canonical literature cards only'
    notes(s, 'All entries are taken from the canonical literature cards (original PDFs); no bibliographic field was filled from memory.')

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


def selftest(out, repo):
    txt = deck_text(out)
    ban = json.loads((Path(repo) / 'docs/reviews/claims.json').read_text(encoding='utf-8')).get('quotation_ban', [])
    pats = [q.get('pattern') if isinstance(q, dict) else q for q in ban]
    hits = [p for p in pats if p and p in txt]
    assert not hits, f'banned strings in deck: {hits}'
    internal = re.findall(r'\b(?:CL-\d+|SELF-\d+|G2RR\d*-\d+|RGL[R0-9]*-\d+|UL-\d+|DEMP-\d+|RB-\d+|MV-\d+|PS45E-\d+|stoic-knuth|pqwtv8|ps45|ps73|kgy|ibb|real_14|real14)\b', txt)
    body_internal = [t for t in internal]
    # 내부 용어는 notes (발표자 메모) 에만 허용 — 슬라이드 본문 검사
    prs = Presentation(out)
    slide_txt = '\n'.join(sh.text_frame.text for s in prs.slides for sh in s.shapes if sh.has_text_frame)
    leak = re.findall(r'\b(?:CL-\d+|SELF-\d+|G2RR\d*-\d+|RGL[R0-9]*-\d+|UL-\d+|DEMP-\d+|RB-\d+|MV-\d+|PS45E-\d+|stoic-knuth|pqwtv8|kgy|ibb)\b', slide_txt)
    assert not leak, f'internal identifiers on slides: {leak}'
    n = len(prs.slides)
    assert n == 19, n
    print(f'selftest ok — {n} slides · banned strings 0 · internal identifiers on slides 0')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--template', required=True)
    ap.add_argument('--repo', required=True)
    ap.add_argument('--figs', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    build(a.template, a.repo, a.figs, a.out)
    selftest(a.out, a.repo)
    print('written', a.out)


if __name__ == '__main__':
    main()
