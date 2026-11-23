#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""주간보고 생성 — 개요 (JSON) + 지난주 1저자 수정본 (PPTX 틀) → 교수님 보고 덱.

    python3 build_weekly.py --outline outline.json --template last_week.pptx --out this_week.pptx
    python3 build_weekly.py --selftest

틀 (지난주 1저자 수정본) 에서 쓰는 것:
  1 장 = 요약표 (연구주제 · 구분 · 전주 / 금주 · 연구 관련 · 기타)
  2 장 = 주간 업무 수행 (요일 표)
  3 장 = Part 표지 (그대로 둔다)
  4 장 = 내용 장의 제목 · 부제 · 아래 한 줄 (< … >) 모양을 빌린다 (4 장 이후는 지우고 새로 만든다)

내용 장은 참고 양식 (랩 주간보고) 꼴: 'N) 제목' → '(k) 부제' → 짧은 bullet (• · - · →)
→ 아래 (또는 오른쪽) 에 그림 · 표 · 그래프 → 맨 아래 한 줄 = 교수님이 가져갈 한 문장.
그림이 아직 없으면 빈칸 (점선 상자 · '그림 ①' · 무엇을 · 어디서) 을 둔다 — 1저자가 붙여 넣는다.
"""
from __future__ import annotations

import argparse
import copy
import json
import math
import os
import re
import sys

from lxml import etree
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION
from pptx.enum.dml import MSO_LINE
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

FONT = '맑은 고딕'
INK = RGBColor(0x26, 0x26, 0x26)
MUTED = RGBColor(0x6E, 0x6E, 0x6E)
EMPH = RGBColor(0x1F, 0x4E, 0x9A)      # ** 강조 ** = 남색 굵게
TODO = RGBColor(0xC0, 0x00, 0x00)      # [[ 1저자 작성 ]] = 빨강 굵게 (빈칸 표시)
SLOT_FILL = RGBColor(0xF2, 0xF2, 0xF2)
SLOT_LINE = RGBColor(0x9E, 0x9E, 0x9E)

SLIDE_W, SLIDE_H = 10.833, 7.5
BODY_X, BODY_W = 0.66, 9.55
FIG_BOTTOM = 6.40                      # 아래 한 줄 (< … >, 6.54) 위까지


# ── 글자 ────────────────────────────────────────────────────────────────────
def font(run, size, bold=False, color=INK):
    f = run.font
    f.size = Pt(size)
    f.bold = bold
    f.color.rgb = color
    f.name = FONT
    rPr = run._r.get_or_add_rPr()
    for tag in ('a:ea', 'a:cs'):
        el = rPr.find(qn(tag))
        if el is None:
            el = etree.SubElement(rPr, qn(tag))
        el.set('typeface', FONT)


_TOKEN = re.compile(r'(\*\*[^*]+\*\*|\[\[[^\]]+\]\])')


def rich(p, text, size, color=INK, bold=False):
    """'**강조**' = 남색 굵게 · '[[빈칸]]' = 빨강 굵게."""
    for part in _TOKEN.split(text):
        if not part:
            continue
        if part.startswith('**'):
            r = p.add_run(); r.text = part[2:-2]; font(r, size, True, EMPH)
        elif part.startswith('[['):
            r = p.add_run(); r.text = part[2:-2]; font(r, size, True, TODO)
        else:
            r = p.add_run(); r.text = part; font(r, size, bold, color)


def _bullet(p, kind):
    """kind: h = '1. 제목' 줄 · b = • · s = - · a = → · p = 글만."""
    pPr = p._p.get_or_add_pPr()
    for tag in ('a:buNone', 'a:buChar', 'a:buAutoNum', 'a:buFont'):
        for el in pPr.findall(qn(tag)):
            pPr.remove(el)
    marL, ind, ch = {'h': (0.0, 0.0, None), 'p': (0.0, 0.0, None),
                     'b': (0.22, -0.18, '•'), 's': (0.50, -0.17, '-'),
                     'a': (0.50, -0.22, '→')}[kind]
    pPr.set('marL', str(int(Inches(marL))))
    pPr.set('indent', str(int(Inches(ind))))
    if ch is None:
        etree.SubElement(pPr, qn('a:buNone'))
    else:
        bf = etree.SubElement(pPr, qn('a:buFont')); bf.set('typeface', 'Arial')
        bc = etree.SubElement(pPr, qn('a:buChar')); bc.set('char', ch)


def classify(line):
    for pre, kind in (('• ', 'b'), ('- ', 's'), ('→ ', 'a')):
        if line.startswith(pre):
            return kind, line[len(pre):]
    if re.match(r'^\d+\. ', line):
        return 'h', line
    return 'p', line


def _units(text):
    """한 줄 폭 어림 — 한글 · 전각 1, 그 밖 0.55."""
    t = re.sub(r'\*\*|\[\[|\]\]', '', text)
    return sum(1.0 if ord(c) > 0x2E7F else 0.55 for c in t)


def est_height(lines, size, width_in):
    per_line = width_in * 72.0 / (size * 1.0)              # 한글 한 자 ≈ size pt
    h = 0.0
    for ln in lines:
        kind, txt = classify(ln)
        w = width_in - (0.5 if kind in 's a' else 0.22 if kind == 'b' else 0)
        n = max(1, math.ceil(_units(txt) / (w * 72.0 / size)))
        h += n * size * 1.22 / 72.0 + (5 if kind in 'h b' else 2) / 72.0
    return h + 0.08


def text_lines(tf, lines, size):
    tf.word_wrap = True
    for m in ('margin_left', 'margin_right'):
        setattr(tf, m, Inches(0.03))
    tf.margin_top = tf.margin_bottom = Inches(0.02)
    first = True
    for ln in lines:
        kind, txt = classify(ln)
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_before = Pt(5 if kind in ('h', 'b') else 2)
        _bullet(p, kind)
        rich(p, txt, size, bold=(kind == 'h'))


def textbox(slide, x, y, w, h, lines, size, name=None, align=None):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if name:
        tb.name = name
    text_lines(tb.text_frame, lines, size)
    if align is not None:
        for p in tb.text_frame.paragraphs:
            p.alignment = align
    return tb


def replace_keep_style(shape, text):
    """틀 모양의 첫 run 모양을 그대로 두고 글만 바꾼다 (여러 줄 = '\\n')."""
    tf = shape.text_frame
    p0 = tf.paragraphs[0]
    r0 = p0.runs[0] if p0.runs else None
    rPr = copy.deepcopy(r0._r.find(qn('a:rPr'))) if r0 is not None and r0._r.find(qn('a:rPr')) is not None else None
    pPr = copy.deepcopy(p0._p.find(qn('a:pPr'))) if p0._p.find(qn('a:pPr')) is not None else None
    txBody = tf._txBody
    for p in txBody.findall(qn('a:p')):
        txBody.remove(p)
    for line in text.split('\n'):
        p = etree.SubElement(txBody, qn('a:p'))
        if pPr is not None:
            p.append(copy.deepcopy(pPr))
        r = etree.SubElement(p, qn('a:r'))
        if rPr is not None:
            r.append(copy.deepcopy(rPr))
        t = etree.SubElement(r, qn('a:t'))
        t.text = line


# ── 그림 · 빈칸 · 그래프 ────────────────────────────────────────────────────
def picture(slide, path, x, y, w, h):
    from PIL import Image
    with Image.open(path) as im:
        iw, ih = im.size
    s = min(w / iw, h / ih)
    pw, ph = iw * s, ih * s
    return slide.shapes.add_picture(path, Inches(x + (w - pw) / 2), Inches(y + (h - ph) / 2),
                                    Inches(pw), Inches(ph))


def slot(slide, x, y, w, h, label, desc, src):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.name = f'SLOT {label}'
    sh.fill.solid(); sh.fill.fore_color.rgb = SLOT_FILL
    sh.line.color.rgb = SLOT_LINE; sh.line.width = Pt(1.25); sh.line.dash_style = MSO_LINE.DASH
    sh.shadow.inherit = False
    tf = sh.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    for k, (t, size, bold, col) in enumerate(((label, 15, True, MUTED), (desc, 11.5, False, INK),
                                               ('넣을 것: ' + src, 9.5, False, MUTED))):
        p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.CENTER
        p.space_before = Pt(0 if k == 0 else 4)
        r = p.add_run(); r.text = t; font(r, size, bold, col)
    return sh


def chart(slide, spec, x, y, w, h):
    cd = CategoryChartData()
    cd.categories = spec['cats']
    for name, vals, _col in spec['series']:
        cd.add_series(name, vals)
    gf = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(x), Inches(y),
                                Inches(w), Inches(h), cd)
    ch = gf.chart
    ch.font.size = Pt(10); ch.font.name = FONT
    multi = len(spec['series']) > 1
    ch.has_legend = multi
    if multi:
        ch.legend.position = XL_LEGEND_POSITION.TOP
        ch.legend.include_in_layout = False
        ch.legend.font.size = Pt(9.5)
    plot = ch.plots[0]
    plot.gap_width = 70
    plot.overlap = -5
    for s, (_n, _v, col) in zip(plot.series, spec['series']):
        s.format.fill.solid(); s.format.fill.fore_color.rgb = RGBColor.from_string(col)
    plot.has_data_labels = True
    dl = plot.data_labels
    dl.number_format = spec.get('fmt', '0.00'); dl.number_format_is_linked = False
    dl.position = XL_LABEL_POSITION.OUTSIDE_END
    dl.font.size = Pt(9)
    va = ch.value_axis
    if 'ymin' in spec:
        va.minimum_scale = spec['ymin']
    if 'ymax' in spec:
        va.maximum_scale = spec['ymax']
    if 'ystep' in spec:
        va.major_unit = spec['ystep']
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = RGBColor(0xD9, 0xD9, 0xD9)
    va.tick_labels.number_format = spec.get('axfmt', spec.get('fmt', '0.00'))
    va.tick_labels.number_format_is_linked = False
    va.tick_labels.font.size = Pt(9.5)
    ch.category_axis.tick_labels.font.size = Pt(10)
    if spec.get('ytitle'):
        va.has_title = True
        tf = va.axis_title.text_frame
        tf.text = spec['ytitle']
        for r in tf.paragraphs[0].runs:
            font(r, 10, False, INK)
    return gf


def figure_row(slide, figs, x0, y0, width, y1, gap=0.25):
    """그림 칸을 한 줄로 — 칸 폭은 'w' (상대값) 비율."""
    ws = [f.get('w', 1.0) for f in figs]
    tot = sum(ws)
    avail = width - gap * (len(figs) - 1)
    x = x0
    for f, wr in zip(figs, ws):
        fw = avail * wr / tot
        cap_h = 0.30 if f.get('cap') else 0.0
        fh = max(0.6, y1 - y0 - cap_h)
        if 'img' in f:
            picture(slide, f['img'], x, y0, fw, fh)
        elif 'slot' in f:
            slot(slide, x, y0, fw, fh, f['slot'], f.get('desc', ''), f.get('src', ''))
        elif 'chart' in f:
            chart(slide, f['chart'], x, y0, fw, fh)
        if f.get('cap'):
            textbox(slide, x, y0 + fh + 0.02, fw, 0.28, [f['cap']], 10.5, align=PP_ALIGN.CENTER)
        x += fw + gap


# ── 장 만들기 ───────────────────────────────────────────────────────────────
def _find(slide, prefix):
    for sh in slide.shapes:
        if sh.name.startswith(prefix):
            return sh
    raise KeyError(prefix)


def content_slide(prs, tpl, spec):
    s = prs.slides.add_slide(tpl.slide_layout)
    for ph in list(s.placeholders):                      # 틀 배치의 빈 자리 표시는 쓰지 않는다
        ph._element.getparent().remove(ph._element)
    tree = s.shapes._spTree
    for name in ('Google Shape;202', 'Google Shape;201', 'TextBox 207'):
        el = copy.deepcopy(_find(tpl, name)._element)
        tree.append(el)
    replace_keep_style(_find(s, 'Google Shape;202'), spec['title'])
    replace_keep_style(_find(s, 'Google Shape;201'), spec.get('sub', ''))
    cap = _find(s, 'TextBox 207')
    if spec.get('caption'):
        replace_keep_style(cap, '< ' + spec['caption'] + ' >')
    else:
        cap._element.getparent().remove(cap._element)
    size = spec.get('size', 14)
    figs = spec.get('figs', [])
    pos = spec.get('fig_pos', 'bottom')
    y_body = 1.55
    if pos == 'right' and figs:
        tw = spec.get('text_w', 5.9)
        h = est_height(spec['bullets'], size, tw)
        textbox(s, BODY_X, y_body, tw, h, spec['bullets'], size, name='Body')
        fx = BODY_X + tw + 0.25
        figure_row(s, figs, fx, y_body + 0.05, BODY_X + BODY_W - fx, FIG_BOTTOM)
    else:
        h = est_height(spec['bullets'], size, BODY_W)
        textbox(s, BODY_X, y_body, BODY_W, h, spec['bullets'], size, name='Body')
        if figs:
            y0 = y_body + h + 0.12
            if FIG_BOTTOM - y0 < 1.6:
                raise SystemExit(f'⛔ "{spec["title"]}" 글이 길어 그림 칸이 {FIG_BOTTOM - y0:.2f} in — '
                                 'bullet 을 줄이거나 fig_pos=right')
            figure_row(s, figs, BODY_X, y0, BODY_W, FIG_BOTTOM)
    return s


def fill_cell(cell, lines, size):
    tf = cell.text_frame
    p0 = tf.paragraphs[0]
    pPr = copy.deepcopy(p0._p.find(qn('a:pPr'))) if p0._p.find(qn('a:pPr')) is not None else None
    txBody = tf._txBody
    for p in txBody.findall(qn('a:p')):
        txBody.remove(p)
    for ln in lines:
        p = etree.SubElement(txBody, qn('a:p'))
        if pPr is not None:
            p.append(copy.deepcopy(pPr))
    for p, ln in zip(tf.paragraphs, lines):
        _bullet(p, 'p')                                   # 틀 칸의 자동 번호 · 글머리 끄기 (번호는 글로 쓴다)
        bold = ln.startswith('## ')
        rich(p, ln[3:] if bold else ln, size, bold=bold)


def summary_slide(slide, o):
    t = [sh for sh in slide.shapes if sh.has_table][0].table
    replace_keep_style_cell(t.cell(0, 0), o['topic'])
    replace_keep_style_cell(t.cell(1, 1), f'전주 수행 업무 ({o["prev_period"]})')
    replace_keep_style_cell(t.cell(1, 2), f'금주 수행 업무 ({o["next_period"]})')
    sz = o.get('summary_size', 10)
    fill_cell(t.cell(2, 1), o['summary']['prev'], sz)
    fill_cell(t.cell(2, 2), o['summary']['next'], sz)
    fill_cell(t.cell(3, 1), o['summary']['etc_prev'], sz)
    fill_cell(t.cell(3, 2), o['summary']['etc_next'], sz)


def replace_keep_style_cell(cell, text):
    tf = cell.text_frame
    p0 = tf.paragraphs[0]
    runs = p0.runs
    if runs:
        runs[0].text = text
        for r in runs[1:]:
            r._r.getparent().remove(r._r)
        for p in tf.paragraphs[1:]:
            p._p.getparent().remove(p._p)
    else:
        rich(p0, text, 11)


def daily_slide(slide, o):
    t = [sh for sh in slide.shapes if sh.has_table][0].table
    for row in t.rows:                                    # 틀에서 합친 칸 (예: 토 · 일) 은 풀어서 하루씩 쓴다
        for c in row.cells:
            if c.is_merge_origin:
                c.split()
    sz = o.get('daily_size', 11)
    for i, (day, work, note) in enumerate(o['daily'], start=1):
        replace_keep_style_cell(t.cell(i, 0), day)
        c = t.cell(i, 1)
        fill_cell(c, [work], sz)
        if note:
            fill_cell(t.cell(i, 2), [note], sz)


def delete_slide(prs, idx):
    lst = prs.slides._sldIdLst
    sid = lst[idx]
    prs.part.drop_rel(sid.rId)
    lst.remove(sid)


def build(outline, template, out):
    o = json.load(open(outline, encoding='utf-8'))
    base = os.path.dirname(os.path.abspath(outline))
    prs = Presentation(template)
    tpl = prs.slides[3]
    summary_slide(prs.slides[0], o)
    daily_slide(prs.slides[1], o)
    if o.get('part_title'):
        replace_keep_style(_find(prs.slides[2], 'Google Shape;142'), o['part_title'])
    for spec in o['slides']:
        for f in spec.get('figs', []):
            if 'img' in f and not os.path.isabs(f['img']):
                f['img'] = os.path.join(base, f['img'])
        content_slide(prs, tpl, spec)
    n_tpl = len(prs.slides) - len(o['slides'])
    for idx in range(n_tpl - 1, 2, -1):                  # 틀의 4 장 이후 (지난주 내용) 지우기
        delete_slide(prs, idx)
    prs.save(out)
    return out


# ── 시험 ────────────────────────────────────────────────────────────────────
def _selftest():
    ok = 0
    assert classify('• 가')[0] == 'b'; ok += 1
    assert classify('- 가')[0] == 's'; ok += 1
    assert classify('→ 가')[0] == 'a'; ok += 1
    assert classify('1. 피드백')[0] == 'h'; ok += 1
    assert classify('그냥')[0] == 'p'; ok += 1
    assert abs(_units('가나') - 2.0) < 1e-9 and abs(_units('ab') - 1.1) < 1e-9; ok += 1
    assert est_height(['• ' + '가' * 200], 14, 9.5) > est_height(['• 가'], 14, 9.5); ok += 1
    assert _TOKEN.split('a **b** c [[d]]') == ['a ', '**b**', ' c ', '[[d]]', '']; ok += 1
    print(f'selftest {ok}/8 ✓')
    return 0


def main():
    ap = argparse.ArgumentParser(description='주간보고 생성 (개요 JSON + 지난주 수정본 틀)')
    ap.add_argument('--outline'); ap.add_argument('--template'); ap.add_argument('--out')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if not (a.outline and a.template and a.out):
        ap.error('--outline --template --out 셋 다 필요')
    print(build(a.outline, a.template, a.out))
    return 0


if __name__ == '__main__':
    sys.exit(main())
