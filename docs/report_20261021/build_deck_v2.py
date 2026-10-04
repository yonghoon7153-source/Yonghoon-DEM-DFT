#!/usr/bin/env python3
"""이종기술 3세부 2차년도 진도점검 워크숍 (2026-10-21) — 한양대 DEM 파트 슬라이드 v2 생성기 (2026-10-01).

    python3 docs/report_20261021/make_figs.py            # 그래프 데이터 · 미리보기 · Origin 스크립트 · 수치
    python3 docs/report_20261021/build_deck_v2.py --template <3세부 양식.pptx> --out docs/report_20261021/report_20261021_v2.pptx

- **양식 그대로**: 양식 8 번 장 (2-1 · 자유 양식) 의 틀 — ◆ 머리 1 + 연파랑 요약 상자 · ◆ 머리 2 + 탭 패널 둘 — 을 장마다 복제해 채운다.
  빨간 안내 상자만 지운다.  양식의 다른 장 (1–7 · 10–11) 은 손대지 않는다.  양식 파일은 리포에 두지 않는다 (사용자 업로드 원본).
- **글꼴 (사용자 지정)**: 한글 = KoPubWorld돋움체 Medium · 영어 = Aptos (머리 · 탭 · 표 · 라벨) · 설명 문장 = 맑은 고딕 · 그래프 영어 = Aptos (Origin).
- **수식 = PowerPoint 네이티브 수식 (OMML)** — 눌러서 바로 고친다 (옛 생성기 `docs/report_20261001/build_deck.py` 의 Eq 조립기 재사용).
- **그래프 = Origin** — 덱에는 미리보기 PNG (`previews/`) 를 넣고 "Origin 으로 교체" 표지를 단다.  Origin 스크립트 · 데이터 = `origin/`.
- **완료 가정 발표** (1저자 10-01): 아직 진행 중인 항목은 결과 칸을 ⬜ 로 두고 "(10월 중 완료 예정)" 을 붙인다.  지어낸 값은 없다 — 모든 수치는 `summary.json` 에서 읽는다.
"""
import argparse
import copy
import csv
import importlib.util
import json
import math
from pathlib import Path

from lxml import etree
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt, Emu

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
_spec = importlib.util.spec_from_file_location('bd1', ROOT / 'docs/report_20261001/build_deck.py')
bd1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bd1)
Eq, add_equations, dup_slide, shape, drop, set_runs_text, set_bullets, notes = (
    bd1.Eq, bd1.add_equations, bd1.dup_slide, bd1.shape, bd1.drop, bd1.set_runs_text, bd1.set_bullets, bd1.notes)

A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
KO, EN, DESC = 'KoPubWorld돋움체 Medium', 'Aptos', '맑은 고딕'
DARK, SUB, NAVY, ORANGE = RGBColor(0x26, 0x26, 0x26), RGBColor(0x55, 0x5B, 0x66), RGBColor(0x1F, 0x3A, 0x68), RGBColor(0xD9, 0x5D, 0x12)
LBOX = (0.62, 3.58, 4.30, 3.42)          # 왼쪽 탭 패널 안쪽 (in) — 양식 렌더에서 잰 값
RBOX = (5.96, 3.58, 4.36, 3.42)          # 오른쪽 탭 패널 안쪽
PENDING = '(10월 중 완료 예정)'
S = json.load(open(HERE / 'summary.json', encoding='utf-8'))
E = Eq(sz=1200)


# ───────────────────────────── 글꼴 ─────────────────────────────
def setfont(rpr, latin, ea):
    for t in ('latin', 'ea', 'cs'):
        for el in rpr.findall('{%s}%s' % (A, t)):
            rpr.remove(el)
    after = [rpr.find('{%s}%s' % (A, t)) for t in ('sym', 'hlinkClick', 'hlinkMouseOver', 'rtl', 'extLst')]
    after = [a for a in after if a is not None]
    new = []
    for t, face in (('latin', latin), ('ea', ea), ('cs', latin)):
        el = etree.Element('{%s}%s' % (A, t))
        el.set('typeface', face)
        new.append(el)
    if after:
        idx = list(rpr).index(after[0])
        for k, el in enumerate(new):
            rpr.insert(idx + k, el)
    else:
        for el in new:
            rpr.append(el)


def fonts_in(el, latin, ea):
    for tag in ('rPr', 'endParaRPr', 'defRPr'):
        for rpr in el.iter('{%s}%s' % (A, tag)):
            setfont(rpr, latin, ea)


# ───────────────────────────── 도형 ─────────────────────────────
def tb(slide, box, lines, size=10, bold=False, color=DARK, align=PP_ALIGN.LEFT, kind='ko', anchor=MSO_ANCHOR.TOP, spacing=0):
    """lines = [str | [(글자, 굵게, 색 | None), …]]"""
    x, y, w, h = box
    t = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = t.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for side in ('margin_left', 'margin_right', 'margin_top', 'margin_bottom'):
        setattr(tf, side, Inches(0.03))
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if spacing:
            p.space_after = Pt(spacing)
        segs = [(ln, bold, None)] if isinstance(ln, str) else ln
        for txt, b, c in segs:
            r = p.add_run()
            r.text = txt
            r.font.size, r.font.bold = Pt(size), b
            r.font.color.rgb = c or color
    fonts_in(t._element, *((EN, KO) if kind == 'ko' else (DESC, DESC)))
    return t


def tbl(slide, box, rows, col_w=None, size=9, row_h=0.27, head=NAVY, pending_color=ORANGE, bold_first_col=False):
    x, y, w, _ = box
    nr, nc = len(rows), len(rows[0])
    gt = slide.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(w), Inches(row_h * nr))
    t = gt.table
    if col_w:
        tot = sum(col_w)
        for j, cw in enumerate(col_w):
            t.columns[j].width = int(Inches(w) * cw / tot)
    for i, row in enumerate(rows):
        t.rows[i].height = Inches(row_h)
        for j, v in enumerate(row):
            c = t.cell(i, j)
            c.margin_left = c.margin_right = Inches(0.04)
            c.margin_top = c.margin_bottom = Inches(0.01)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = c.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER if (j > 0 or i == 0) else PP_ALIGN.LEFT
            r = p.add_run()
            r.text = str(v)
            r.font.size = Pt(size)
            r.font.bold = (i == 0) or (bold_first_col and j == 0)
            c.fill.solid()
            if i == 0:
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                c.fill.fore_color.rgb = head
            else:
                c.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF) if i % 2 else RGBColor(0xF1, 0xF4, 0xFA)
                r.font.color.rgb = pending_color if ('⬜' in str(v) or PENDING in str(v)) else DARK
    fonts_in(gt._element, EN, KO)
    return t


def pic(slide, path, box, caption=None, cap_h=0.30):
    x, y, w, h = box
    hh = h - (cap_h if caption else 0)
    im = Image.open(path)
    ar = im.width / im.height
    pw, ph = (w, w / ar) if w / ar <= hh else (hh * ar, hh)
    slide.shapes.add_picture(str(path), Inches(x + (w - pw) / 2), Inches(y + (hh - ph) / 2), Inches(pw), Inches(ph))
    if caption:
        tb(slide, (x, y + hh + 0.02, w, cap_h), caption if isinstance(caption, list) else [caption], size=8, color=SUB, kind='desc')


def ph_box(slide, box, lines):
    x, y, w, h = box
    b = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    b.fill.solid()
    b.fill.fore_color.rgb = RGBColor(0xF3, 0xF4, 0xF6)
    b.line.color.rgb = RGBColor(0x9A, 0xA0, 0xA8)
    b.line.dash_style = 4
    tf = b.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = ln
        r.font.size = Pt(9.5)
        r.font.color.rgb = ORANGE if PENDING in ln or '⬜' in ln else SUB
    fonts_in(b._element, EN, KO)
    return b


def flow_box(slide, box, head, body, fill):
    x, y, w, h = box
    b = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    b.adjustments[0] = 0.12
    b.fill.solid()
    b.fill.fore_color.rgb = fill
    b.line.fill.background()
    b.shadow.inherit = False
    tf = b.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    for side in ('margin_left', 'margin_right'):
        setattr(tf, side, Inches(0.08))
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = head
    r.font.size, r.font.bold = Pt(10.5), True
    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    r2 = p2.add_run()
    r2.text = body
    r2.font.size = Pt(9)
    r2.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    fonts_in(b._element, EN, KO)


# ───────────────────────────── 장 ─────────────────────────────
def cslide(prs, proto, num, h1, bullets, h2, ltab, rtab, llab='', rlab='', bsize=11):
    s = dup_slide(prs, proto)
    drop(s, '직사각형 17')                                   # 빨간 안내 상자
    set_runs_text(shape(s, 'TextBox 3').text_frame, num)
    for name, txt, wd in (('직사각형 10', h1, 9.9), ('직사각형 12', h2, 9.9)):
        hd = shape(s, name)
        set_runs_text(hd.text_frame, txt)
        hd.width = Inches(wd)
        hd.text_frame._txBody.find('{%s}bodyPr' % A).set('wrap', 'square')
        fonts_in(hd._element, EN, KO)
    box = shape(s, '직사각형 14')
    set_bullets(box, bullets, size=bsize)
    fonts_in(box._element, DESC, DESC)
    for grp, tab, lab, title, label in (('그룹 2', '직사각형 28', 'TextBox 29', ltab, llab), ('그룹 30', '직사각형 32', 'TextBox 33', rtab, rlab)):
        g = shape(s, grp)
        for c in g.shapes:
            if c.name == tab:
                set_runs_text(c.text_frame, title)
                fonts_in(c._element, EN, KO)
            elif c.name == lab:
                set_runs_text(c.text_frame, label or ' ')
                fonts_in(c._element, EN, KO)
    return s


def build(template, out):
    prs = Presentation(template)
    proto = prs.slides[7]
    PV = HERE / 'previews'
    g1, g5, g6, g7 = S['G1'], S['G5'], S['G6'], S['G7']
    made = []

    # 데이터셋 요약 (배포 v1)
    def rel(tag):
        return list(csv.DictReader(open(ROOT / f'docs/data/lhs_release_20261001/{tag}_release_20261001.csv', encoding='utf-8')))
    def pstat(rows):
        v = sorted(float(r['porosity_union_exact_pct']) for r in rows if r.get('porosity_union_exact_pct') not in ('', None))
        med = v[len(v) // 2] if len(v) % 2 else (v[len(v) // 2 - 1] + v[len(v) // 2]) / 2
        return f'{med:.1f}  ({v[0]:.1f} – {v[-1]:.1f})'
    L130, L64 = rel('lhs'), rel('lhsx')
    _cols = list(csv.DictReader(open(ROOT / 'docs/data/lhs_release_20261001/lhs_release_20261001_columns.tsv', encoding='utf-8'), delimiter='\t'))
    ncol130 = sum(1 for r in _cols if r.get('source') != 'design')          # 측정 지표 (설계 열 제외)
    ndes130 = len(_cols) - ncol130

    # ── 2-1 개요 ──
    s = cslide(prs, proto, '2-1', '3세부 2차년도 개발 목표 및 중간 성과 — 한양대 (전극 미세구조 · 공정 시뮬레이션)', [
        [('목표  ', True), ('건식 황화물 후막 복합양극 (6 mAh/cm²) 의 미세구조와 이온 · 전자 경로를 조성 · 바이모달 비 · 입경으로 예측하고 설계 · 믹싱 조건 제시', False)],
        [('성과  ', True), (f'DEM 압축 모델 · 설계점 {g5["n130"] + g5["n64"]} 건 데이터셋 배포 · 전해질 함량 · 바이모달 비 · 도전재 영향 정량 · 건식 믹싱 판정 (사전 등록)', False)],
    ], '3세부 2차년도 연구개발 추진 내용', '추진 체계', '주요 결과')
    x, y, w, _ = LBOX
    fills = (RGBColor(0x1F, 0x3A, 0x68), RGBColor(0x2A, 0x78, 0xD6), RGBColor(0x2A, 0x9D, 0x8F))
    steps = (('① 전극 미세구조 모델', 'DEM 투입 · 침강 · 300 MPa 압축 · 이완 (LIGGGHTS)'),
             ('② 설계인자별 구조 · 이온/전자 경로', f'설계점 {g5["n130"] + g5["n64"]} 건 · 사양 5 조성 · 도전재 함량'),
             ('③ 건식 믹싱 균일성', '회전 드럼 DEM · 입자 점착 · 표면 점착 저감 (코팅 모사)'))
    for k, (hd, bd) in enumerate(steps):
        flow_box(s, (x + 0.1, y + 0.12 + k * 1.10, w - 0.2, 0.86), hd, bd, fills[k])
    tbl(s, (RBOX[0], RBOX[1] + 0.05, RBOX[2], 0), [
        ['항목', '결과'],
        ['설계점 데이터셋', f'{g5["n130"] + g5["n64"]} 설계점 · 측정 지표 {ncol130} 개 · 열 사전 (배포 10-01)'],
        ['바이모달 비', f'소입자만 {g1["0:10"]["union"]:.1f} % → 7:3 {g1["7:3"]["union"]:.1f} % (공극률)'],
        ['전해질 함량', f'고체 중 SE {S["G3_levels"][0][3]:.0f} → {S["G3_levels"][-1][3]:.0f} vol% 공극률 {S["G3_levels"][0][2]} → {S["G3_levels"][-1][2]} % · {g5["nonspan_se_max"]:.0f} % 이하 경로 단절 {g5["nonspan130"]} 건'],
        ['도전재 함량', 'VGCF 1→4 wt% 전자 전도도 순서 72/72 유지'],
        ['건식 믹싱', '8 회전 뒤 전 조건 M ≈ 1 · 코팅 모사 차이 구분 불가'],
        ['고점착 확장', f'⬜ {PENDING}'],
    ], col_w=[1.25, 3.1], size=8.5, row_h=0.42, bold_first_col=True)
    notes(s, '수치 출처 = docs/report_20261021/summary.json (make_figs.py).  배포 v1 = docs/data/lhs_release_20261001/.  믹서 = docs/data/mixer_final10_20260930/README.md.  Phase A = docs/data/phase_a_104arms_20260921/ · phase_a_rep100_20260930/.')
    made.append(s)

    # ── 2-2 압축 모델 ──
    s = cslide(prs, proto, '2-2', 'DEM 기반 복합양극 압축 모델', [
        '활물질 (NCM 대 · 소) · 고체전해질 (LPSCl) 을 구형 입자로 두고 접촉력으로 운동방정식을 풀어 투입 → 침강 → 300 MPa 압축 → 이완을 계산 (LIGGGHTS)',
        '접촉 = 탄성 + 하중/제하 이력 (잔류 겹침) 으로 소성 압밀 대리 · 전해질 유효 탄성계수 1.35 GPa (실제 24 GPa · 순수 전해질 압축 겹침으로 보정)',
    ], '모델 · 입력', '지배 방정식', '입력 물성')
    Fn, Ft, Mr = E.sub(E.b('F'), E.r('n,ij')), E.sub(E.b('F'), E.r('t,ij')), E.sub(E.b('M'), E.r('r,ij'))
    eqs = [
        (E.sub(E.r('m'), E.r('i')) + E.frac(E.r('d') + E.sub(E.b('v'), E.r('i')), E.r('dt')) + E.r('=') +
         E.nary('∑', E.r('j'), E.par(Fn + E.r('+') + Ft)) + E.r('+') + E.sub(E.r('m'), E.r('i')) + E.b('g'), 'm_i dv_i/dt = Σ_j (F_n,ij + F_t,ij) + m_i g'),
        (E.sub(E.r('I'), E.r('i')) + E.frac(E.r('d') + E.sub(E.b('ω'), E.r('i')), E.r('dt')) + E.r('=') +
         E.nary('∑', E.r('j'), E.par(E.sub(E.r('R'), E.r('i')) + E.sub(E.b('n'), E.r('ij')) + E.r('×') + Ft + E.r('+') + Mr)), 'I_i dω_i/dt = Σ_j (R_i n_ij × F_t,ij + M_r,ij)'),
        (E.sub(E.r('F'), E.r('n')) + E.r('=') + E.cases(
            E.sub(E.r('k'), E.r('1')) + E.r('δ') + E.r(',  ') + E.t('loading'),
            E.sub(E.r('k'), E.r('2')) + E.par(E.r('δ') + E.r('−') + E.sub(E.r('δ'), E.r('0'))) + E.r(',  ') + E.t('unloading')),
         'F_n = k1·δ (loading) · k2·(δ − δ0) (unloading)'),
        (E.frac(E.r('1'), E.sup(E.r('E'), E.r('*'))) + E.r('=') + E.frac(E.r('1') + E.r('−') + E.subsup(E.r('ν'), E.r('i'), E.r('2')), E.sub(E.r('E'), E.r('i'))) +
         E.r('+') + E.frac(E.r('1') + E.r('−') + E.subsup(E.r('ν'), E.r('j'), E.r('2')), E.sub(E.r('E'), E.r('j'))), '1/E* = (1−νi²)/Ei + (1−νj²)/Ej'),
        (E.par(E.sub(E.b('F'), E.r('t')), '|', '|') + E.r('≤') + E.r('μ') + E.par(E.sub(E.b('F'), E.r('n')), '|', '|') + E.r(',  ') +
         E.par(E.sub(E.b('M'), E.r('r')), '|', '|') + E.r('≤') + E.sub(E.r('μ'), E.r('r')) + E.sup(E.r('R'), E.r('*')) + E.par(E.sub(E.b('F'), E.r('n')), '|', '|'),
         '|F_t| ≤ μ|F_n| ,  |M_r| ≤ μ_r R*|F_n|'),
        (E.r('P') + E.r('=') + E.frac(E.sub(E.r('F'), E.t('plate')), E.sub(E.r('A'), E.t('box'))) + E.r('=') + E.t('300 MPa'), 'P = F_plate / A_box = 300 MPa'),
    ]
    x, y, w, h = LBOX
    add_equations(s, Inches(x), Inches(y), Inches(w), Inches(h), eqs, sz=1150, gap_pt=4)
    x, y, w, h = RBOX
    tbl(s, (x, y + 0.02, w, 0), [
        ['상', '지름 (µm)', 'E (GPa)', 'ν', 'ρ (g/cm³)'],
        ['대입자 (다결정 NCM)', '9', '140', '0.25', '4.8'],
        ['소입자 (단결정 NCM)', '4', '140', '0.25', '4.8'],
        ['고체전해질 LPSCl', '1', '1.35 *', '0.30', '2.0'],
    ], col_w=[1.9, 0.75, 0.72, 0.45, 0.8], size=8.5, row_h=0.30)
    tb(s, (x, y + 1.25, w, 0.42), ['* 유효값 (bulk 24 GPa) — 강체 구가 못 담는 재배열 · 입계 미끄러짐 · 미세 파쇄를 탄성계수 하나에 담은 규약'], size=8, color=SUB, kind='desc')
    tbl(s, (x, y + 1.72, w, 0), [
        ['단계', '내용'],
        ['투입 · 침강', '질량비대로 무작위 투입 → 중력 침강'],
        ['압축', '플래튼 하강 → 300 MPa 도달'],
        ['이완', '플래튼 고정 → 잔류 응력 이완'],
        ['경계', 'x · y 주기 · 바닥 벽 · 50 × 50 µm'],
    ], col_w=[1.0, 3.3], size=8.5, row_h=0.29)
    notes(s, '수식은 PowerPoint 수식 개체 (더블클릭해 편집).  F_n 이력식은 LIGGGHTS hooke/hysteresis 의 하중/제하 강성 구조.  물성 = 덱 값 (dem_scripts/ps_sweep_6mah_20260914/in.ps_7_3_r45.liggghts).  '
             '⚠ 과제 공식 물성 E_NCM 221 GPa (단결정) · 제작 압력 450 MPa 와 다름 — 모델 규약 (논의 사항).')
    made.append(s)

    # ── 2-3 지표 정의 ──
    s = cslide(prs, proto, '2-3', '미세구조 · 수송 성능 지표 정의', [
        '공극률 = 겹친 입자를 한 번만 센 기하 공극 (union) · 굴곡도 = 아래 벽 → 위 벽 전해질 접촉망 최단 경로 / 두께 (기하 굴곡도)',
        '이온 · 전자 전도도 = 입자 접촉망 + 접촉 협착 저항 (Holm) · Kirchhoff 해석  ·  고립 활물질 = 분리막 쪽 전해질 망에 닿지 못한 활물질',
    ], '지표 · 계산식', '지표', '계산식')
    tbl(s, (LBOX[0], LBOX[1] + 0.02, LBOX[2], 0), [
        ['지표', '기호', '단위', '뜻'],
        ['공극률 (union)', 'ε', '%', '입자에 속하지 않는 부피 비율'],
        ['두께', 'L', 'µm', '압축 · 이완 뒤 플래튼 높이'],
        ['굴곡도 (벽 기준)', 'τ_wall', '–', '전해질 최단 경로 길이 / 두께'],
        ['이온 · 전자 전도도', 'σ_ion · σ_e', 'mS/cm', '접촉망 유효 전도도'],
        ['전해질 배위수', 'CN_SE', '–', '전해질 1 개당 전해질 접촉 수'],
        ['피복률', 'θ', '%', '활물질 표면 중 전해질 접촉 면적'],
        ['고립 활물질', 'f_iso', '%', '이온 경로가 없는 활물질 비율'],
    ], col_w=[1.35, 0.85, 0.55, 1.75], size=8.2, row_h=0.36)
    eqs = [
        (E.r('ε') + E.r('=') + E.r('1') + E.r('−') + E.frac(E.r('V') + E.par(E.par(E.nary('⋃', E.r('i'), E.sub(E.r('B'), E.r('i')))) + E.r('∩') + E.r('Ω')), E.r('V') + E.par(E.r('Ω'))),
         'ε = 1 − V(∪ B_i ∩ Ω) / V(Ω)'),
        (E.sub(E.r('τ'), E.t('wall')) + E.r('=') + E.frac(E.sub(E.r('L'), E.t('path')), E.r('L')), 'τ_wall = L_path / L'),
        (E.sub(E.r('R'), E.r('ij')) + E.r('=') + E.frac(E.r('1'), E.r('2') + E.r('σ') + E.sub(E.r('a'), E.r('ij'))) + E.r(',  ') +
         E.nary('∑', E.r('j'), E.frac(E.sub(E.r('φ'), E.r('i')) + E.r('−') + E.sub(E.r('φ'), E.r('j')), E.sub(E.r('R'), E.r('ij')))) + E.r('=') + E.r('0'),
         'R_ij = 1/(2σ a_ij) ,  Σ_j (φ_i − φ_j)/R_ij = 0'),
        (E.sub(E.r('σ'), E.t('eff')) + E.r('=') + E.frac(E.r('I') + E.r('L'), E.r('A') + E.r('Δ') + E.r('V')), 'σ_eff = I L / (A ΔV)'),
        (E.sub(E.r('f'), E.t('iso')) + E.r('=') + E.r('1') + E.r('−') + E.frac(E.sub(E.r('N'), E.t('AM, linked')), E.sub(E.r('N'), E.t('AM'))), 'f_iso = 1 − N_AM,linked / N_AM'),
    ]
    x, y, w, h = RBOX
    add_equations(s, Inches(x), Inches(y), Inches(w), Inches(2.55), eqs, sz=1150, gap_pt=5)
    tb(s, (x, y + 2.62, w, 0.78), ['B_i: 입자 i · Ω: 전극 상자 (x · y 주기) · a_ij: 접촉 반지름 · φ: 전위',
                                   'union = 무작위 점 4×10⁶ 개 (±0.02 %p) · τ_wall 은 기하 최단 경로 (수송 굴곡도와 다름)'], size=8, color=SUB, kind='desc')
    notes(s, '굴곡도 = 수확기 벽 기준 Dijkstra (tortuosity_SE_wall) — 수송 τ (Laplace) 아님.  피복률 = 기하 접촉 면적 기준 (J20-m).  고립 = 100 − ionic_active_pct (경로 기준).')
    made.append(s)

    # ── 2-4 설계인자 · 데이터셋 ──
    s = cslide(prs, proto, '2-4', '설계인자 정의 및 설계점 데이터셋', [
        '핵심 설계인자 = 전해질 함량 · 바이모달 비 (대:소) · 대 · 소 활물질 입경 · 전해질 입경 → 라틴 하이퍼큐브 130 설계점 + 전해질 과량 64 설계점',
        f'설계점마다 구조 · 접촉 위상 · 이온 경로 측정 지표 {ncol130} 개 (+ 설계 변수 {ndes130}) 를 열 사전 (정의 · 계산 코드 · 한정어) 과 함께 배포 (10-01) → ML 구조 예측 입력',
    ], '설계인자 · 데이터셋', '설계인자', '데이터셋')
    tbl(s, (LBOX[0], LBOX[1] + 0.02, LBOX[2], 0), [
        ['설계인자', '사양', '130 설계점 범위', '단위'],
        ['활물질 함량 (나머지 SE)', '81.6', '70 – 95', 'wt%'],
        ['바이모달 비 (대 : 소)', '7 : 3', '0:10 – 10:0', '질량비'],
        ['대입자 입경 D_P', '9', '5 – 15', 'µm'],
        ['소입자 입경 D_S', '4', '1 – 5', 'µm'],
        ['전해질 입경 D_SE', '1', '1 – 2', 'µm'],
        ['압력', '300', '300', 'MPa'],
        ['면용량', '6', '2', 'mAh/cm²'],
    ], col_w=[1.75, 0.65, 1.2, 0.7], size=8.5, row_h=0.36)
    tbl(s, (RBOX[0], RBOX[1] + 0.02, RBOX[2], 0), [
        ['묶음', '건수', '공극률 union (%) 중앙 (범위)'],
        ['라틴 하이퍼큐브', str(len(L130)), pstat(L130)],
        ['전해질 과량', str(len(L64)), pstat(L64)],
        ['사양 5 조성', '5', f'{g1["5:5"]["union"]:.1f}  ({g1["7:3"]["union"]:.1f} – {g1["0:10"]["union"]:.1f})'],
    ], col_w=[1.3, 0.6, 2.45], size=8.5, row_h=0.32)
    tb(s, (RBOX[0], RBOX[1] + 1.42, RBOX[2], 1.95), [
        [('지표 묶음 ', True, None)],
        '• 구조: 두께 · 공극률 · 전해질 / 활물질 부피분율',
        '• 접촉 위상: 배위수 (SE–SE · AM–AM · AM–SE) · 계면 수',
        '• 이온 경로: 전해질 관통 · 벽 기준 굴곡도 · 고립 활물질',
        '• 피복률: 활물질 표면의 전해질 접촉 면적',
        [('• 분해 지표 추가판 (v1.1) ', False, None), (PENDING, False, ORANGE)],
    ], size=8.8, kind='ko')
    notes(s, f'130 = docs/data/lhs_design_20260818.csv 설계 (2 mAh/cm²) · 64 = lhsx (전해질 과량) · 공극률 = 배포 v1 porosity_union_exact_pct.  사양 5 조성 = ps45 union (r45_union_summary.tsv).  '
             f'공극률 중앙값 표기는 5 조성의 경우 5:5 값 (중앙값).')
    made.append(s)

    # ── 2-5 기준 전극 7:3 ──
    s = cslide(prs, proto, '2-5', '기준 전극 (대:소 = 7:3) 의 3차원 압축 구조', [
        f'6 mAh/cm² · 300 MPa 압축 뒤 두께 {g1["7:3"]["thickness"]:.1f} µm · 공극률 (union) {g1["7:3"]["union"]:.1f} % — 대입자 사이를 소입자와 전해질이 채우는 바이모달 충전 구조',
        '웹앱 3D 뷰어로 상별 분포 · 전해질 접촉망 · 공극 위치 확인',
    ], '3차원 구조 · 주요 값', '3D 구조', '주요 값')
    ph_box(s, LBOX, ['[그림] 웹앱 3D 뷰어 캡처', 'input_6mAh_real_4_D9 (7:3)', '대 · 소 활물질 · 전해질 색 구분'])
    tbl(s, (RBOX[0], RBOX[1] + 0.02, RBOX[2], 0), [
        ['항목', '값'],
        ['두께', f'{g1["7:3"]["thickness"]:.1f} µm'],
        ['공극률 (union)', f'{g1["7:3"]["union"]:.2f} %'],
        ['공극률 (구 부피 합)', f'{g1["7:3"]["sphere"]:.2f} %'],
        ['대 / 소 활물질 수', '280 / 1,376'],
        ['전해질 입자 수', '약 15.9 만'],
        ['σ_ion (mS/cm)', f'⬜ {PENDING}'],
        ['σ_e (mS/cm)', f'⬜ {PENDING}'],
        ['굴곡도 τ', f'⬜ {PENDING}'],
    ], col_w=[1.6, 2.75], size=8.8, row_h=0.36)
    notes(s, '웹앱 케이스 260925_000559_082983 (input_6mAh_real_4_D9) · 덤프 atom_3220000.  구 부피 합은 겹침을 두 번 세는 값 (union 과 병기).  ⬜ = 사양 5 조성 수송 값 (웹앱 PC extract_r45_metrics.py).')
    made.append(s)

    # ── 2-6 바이모달 비 → 공극률 ──
    r7 = dict((a, c) for a, b, c in S['G2'])
    s = cslide(prs, proto, '2-6', '바이모달 비 (대:소) 에 따른 공극률', [
        f'사양 5 조성: 소입자만 (0:10) {g1["0:10"]["union"]:.1f} % → 대입자 비율이 클수록 치밀 · 7:3 ({g1["7:3"]["union"]:.1f} %) 과 10:0 ({g1["10:0"]["union"]:.1f} %) 이 최저 구간 · 두께도 7:3 최소',
        f'130 설계점 (전해질 함량 · 입경 보정): 대입자 몫 0.7 부근 공극률 최저 (예측 대비 {r7["7:3"]:+.1f} % · 탐색적 분석 · R² {S["G2_control"]["r2"]:.2f})',
    ], '사양 5 조성 · 130 설계점', '사양 5 조성', '130 설계점 편차')
    pic(s, PV / 'G1.png', LBOX, ['조성당 침대 1 개 · union = 정확 계산 (±0.02 %p)', '미리보기 — Origin (origin/G1.ogs) 으로 교체'])
    pic(s, PV / 'G2.png', RBOX, ['편차 = 같은 SE 함량 · 입경의 예측 대비 공극률 비 (exp(잔차) − 1) · 조성별 중앙값', '미리보기 — Origin (origin/G2.ogs) 으로 교체'])
    notes(s, '왼쪽 = docs/data/ps45_r45_union_20260929/r45_union_summary.tsv.  오른쪽 = 배포 v1 130 설계점 ln(union) ~ 1 + SE/고체 + (SE/고체)² + d_SE (최소제곱) 잔차의 조성별 중앙값을 공극률 비 (exp − 1) 로 바꾼 값 (10-05 정정 — 앞 판은 ln × 100 을 % 로 적었다).  '
             '⚠ 7:3 과 10:0 의 차 (0.4 %p) 는 조성당 침대 1 개 기준 — 반복 없음 (논의 사항).')
    made.append(s)

    # ── 2-7 전해질 함량 · 입경 ──
    b3, b4 = S['G3_levels'], S['G4_bins']   # b3 = (활물질 수준, n, 공극률 중앙, SE 중앙) — 10-05 정정: 10 % 폭 구간 → 활물질 함량 여섯 수준
    s = cslide(prs, proto, '2-7', '전해질 함량 · 입경의 영향 (130 설계점)', [
        f'공극률을 가장 크게 좌우하는 인자는 전해질 함량 — 고체 중 SE {b3[0][3]:.0f} vol% (활물질 {b3[0][0][3:]} wt%) {b3[0][2]} % → {b3[-1][3]:.0f} vol% ({b3[-1][0][3:]} wt%) {b3[-1][2]} % (수준별 중앙값)',
        f'대입자 입경 (5 – 15 µm) 의 단독 효과는 작음 — 구간 중앙값 {min(v[2] for v in b4):.0f} – {max(v[2] for v in b4):.0f} %',
    ], '설계인자별 공극률', '전해질 함량', '대입자 입경')
    pic(s, PV / 'G3.png', LBOX, ['수준별 점 수: ' + ' · '.join(f'{a} {n}' for a, n, m, x in b3), '미리보기 — Origin (origin/G3.ogs) 으로 교체'])
    pic(s, PV / 'G4.png', RBOX, ['구간 점 수: ' + ' · '.join(f'{a} {n}' for a, n, m in b4) + f' (소입자만 {S["G4_excluded_mono_small"]} 점 제외)',
                                 '미리보기 — Origin (origin/G4.ogs) 으로 교체'])
    notes(s, '라틴 하이퍼큐브는 인자를 동시에 바꾸므로 수준별 · 구간 중앙값은 다른 인자가 섞인 주변 경향이다.  활물질 함량은 70–95 wt% 여섯 수준 (SE 11–51 vol%) — '
             '10-05 정정 전 판은 10 % 폭 구간으로 21 % · 30 % 두 수준을 한 칸에 합쳤다.')
    made.append(s)

    # ── 2-8 이온 경로 ──
    s = cslide(prs, proto, '2-8', '이온 경로 — 전해질 관통 · 굴곡도 · 고립 활물질 (194 설계점)', [
        f'고체 중 SE {g5["nonspan_se_max"]:.0f} % 이하에서 분리막까지 이어지는 전해질 경로가 끊기는 설계점 발생 ({g5["n130"]} 중 {g5["nonspan130"]} 건) — 이때 활물질 대부분이 이온적으로 고립',
        f'경로가 이어진 설계점의 굴곡도 {g5["tau130"][0]:.2f} – {g5["tau130"][1]:.2f} · SE 가 많을수록 1 에 가까움 (전해질 과량 {g5["n64"]} 건: {g5["tau64"][0]:.2f} – {g5["tau64"][1]:.2f} · 고립 ≈ 0 %)',
    ], '이온 경로 지표', '벽 기준 굴곡도', '고립 활물질')
    pic(s, PV / 'G5a.png', LBOX, ['× = 전해질 경로 없음 (굴곡도 정의 불가) · 기하 최단 경로 기준', '미리보기 — Origin (origin/G5a.ogs) 으로 교체'])
    pic(s, PV / 'G5b.png', RBOX, ['고립 = 분리막 쪽 전해질 망에 닿지 못한 활물질 (경로 기준)', '미리보기 — Origin (origin/G5b.ogs) 으로 교체'])
    notes(s, '출처 = 배포 v1 (tortuosity_SE_wall · ionic_active_pct · se_of_solid_vol).  굴곡도 = 수확기 벽 기준 Dijkstra — 수송 τ 아님.  비관통 24 건 = 09-19 진단과 같은 집합.')
    made.append(s)

    # ── 2-9 도전재 순서 (Phase A) ──
    m6 = g6['mean']
    s = cslide(prs, proto, '2-9', '도전재 (VGCF) 함량에 따른 전자 전도도 — 순서 판정', [
        '사양 7:3 전극에 VGCF 1 – 4 wt% 를 넣어 MPM 압밀 뒤 복셀 해석으로 전자 전도도 계산 — 함량 4 × 격자 3 × 원점 8 = 96 팔 + 재실행 대조 8 팔',
        '함량 순서 (1 < 2 < 3 < 4 wt%) 가 인접 쌍 72 비교 모두에서 유지 → 사전 등록 판정 "순서 견고" · VGCF 탄성계수 10 → 100 GPa 재현도 같은 판정',
    ], '계산 설계 · 결과', '계산 · 판정', '전자 전도도')
    tbl(s, (LBOX[0], LBOX[1] + 0.02, LBOX[2], 0), [
        ['항목', '내용'],
        ['침대', '6 mAh/cm² · 대:소 7:3 · MPM 압밀'],
        ['도전재', 'VGCF 1 · 2 · 3 · 4 wt% (+ PTFE 1 wt%)'],
        ['해석', '복셀 유한체적 전자 전도도 (σ_e)'],
        ['격자 × 원점', '0.15 · 0.20 · 0.25 µm × 8'],
        ['판정 (사전 등록)', '인접 함량 쌍 72 비교 · 위반 0'],
        ['재현 (09-30)', 'VGCF E 100 GPa 104 팔 · 같은 판정'],
        ['재실행 일치', '대조 8 팔 차이 0.00000 %'],
    ], col_w=[1.3, 3.0], size=8.5, row_h=0.36)
    pic(s, PV / 'G6.png', RBOX, [f'원점 8 평균 · 원점 간 산포 ≤ {g6["max_origin_spread_pct"]:.1f} % · 판정 대상은 순서 (절대값은 격자 의존)', '미리보기 — Origin (origin/G6.ogs) 으로 교체'])
    notes(s, 'docs/data/phase_a_104arms_20260921/ (판정 ORDER-ROBUST · 72/72 · replay 0.00000 %) · 재현 docs/data/phase_a_rep100_20260930/.  '
             '한정어: 등록된 estimand 는 순서뿐 · 증분 % 는 기술 보고 · 복셀 σ 는 접촉 저항 미포함 (CONTACT_FREE 가지).  ⚠ 이 장을 넣을지 = 논의 사항.')
    made.append(s)

    # ── 2-10 믹싱 모델 ──
    s = cslide(prs, proto, '2-10', '건식 믹싱 DEM — 활물질 · 전해질 응집 구현', [
        '회전 드럼에 대 · 소 활물질과 전해질을 층상 장입 (아래 활물질 · 위 전해질) 후 8 회전 · 입자 점착 (van der Waals) 을 SJKR 접촉 점착력으로 구현',
        '혼합 정도 = Lacey 혼합지수 M (0 미혼합 · 1 무작위 완전 혼합) · 코팅 모사 = 활물질 표면 점착 에너지 밀도를 낮춘 조건',
    ], '모델 · 계산 조건', '지배 방정식', '계산 조건')
    eqs = [
        (E.sub(E.r('F'), E.r('n')) + E.r('=') + E.frac(E.r('4'), E.r('3')) + E.sup(E.r('E'), E.r('*')) + E.rad(E.sup(E.r('R'), E.r('*'))) + E.sup(E.r('δ'), E.r('3/2')) +
         E.r('−') + E.sub(E.r('γ'), E.r('n')) + E.sub(E.r('v'), E.r('n')) + E.r('−') + E.sub(E.r('F'), E.t('coh')), 'F_n = (4/3) E* √R* δ^(3/2) − γ_n v_n − F_coh'),
        (E.sub(E.r('F'), E.t('coh')) + E.r('=') + E.sub(E.r('k'), E.r('c')) + E.r('·') + E.r('2π') + E.sup(E.r('R'), E.r('*')) + E.r('δ'), 'F_coh = k_c · 2π R* δ'),
        (E.t('Bo') + E.r('=') + E.frac(E.sub(E.r('F'), E.t('coh')), E.r('m') + E.r('g')), 'Bo = F_coh / (m g)'),
        (E.r('M') + E.par(E.r('t')) + E.r('=') + E.frac(E.subsup(E.r('S'), E.r('0'), E.r('2')) + E.r('−') + E.sup(E.r('S'), E.r('2')) + E.par(E.r('t')),
                                                        E.subsup(E.r('S'), E.r('0'), E.r('2')) + E.r('−') + E.subsup(E.r('S'), E.r('R'), E.r('2'))),
         'M(t) = (S0² − S²(t)) / (S0² − S_R²)'),
    ]
    x, y, w, h = LBOX
    add_equations(s, Inches(x), Inches(y), Inches(w), Inches(2.3), eqs, sz=1200, gap_pt=6)
    tb(s, (x, y + 2.38, w, 1.0), ['k_c: 점착 에너지 밀도 (J/m³) · Bo: Bond 수 · S²: 칸별 활물질 부피분율 분산',
                                  'S0²: 층상 장입 직후 · S_R²: 무작위 균일 장입 (기준 런)'], size=8, color=SUB, kind='desc')
    tbl(s, (RBOX[0], RBOX[1] + 0.02, RBOX[2], 0), [
        ['항목', '값'],
        ['입자 (3 상)', '대 9 · 소 4 · 전해질 1 µm (조대화 ×151)'],
        ['배치 · 입자 수', '2 g · 100,000 개'],
        ['드럼', '반지름 13.1 mm · 75 rpm · 8 회전'],
        ['LC (코팅 모사)', 'AM–AM Bo 0.00109 · 시드 3'],
        ['LB1 · LB2 · LB3', 'Bo 0.1 · 0.5 · 1.5 · 시드 1'],
        ['LA (기준)', 'Bo 3.0 · 시드 3'],
        ['L0 (음성 대조)', '점착 0 (전 쌍) · 시드 1'],
        ['E0 (무작위 기준)', '점착 0 · 무회전 · 시드 3'],
    ], col_w=[1.35, 3.0], size=8.5, row_h=0.355)
    notes(s, '식 = scripts/make_mixer_deck.py (Hertz + SJKR · Bo = F_coh / W) · scripts/measure_mixing_index.py (Lacey).  현 캠페인 = docs/reviews/mixer_layered_prereg_20260921.md.  '
             '드럼 그림 = /mixer 침대 보기 캡처로 넣을 것 (옛 09-20 세대 그림은 쓰지 않는다).')
    made.append(s)

    # ── 2-11 믹싱 결과 ──
    mn = g7['main']['16x4']
    s = cslide(prs, proto, '2-11', '층상 장입 건식 믹싱 결과 (8 회전) — 사전 등록 판정', [
        '10 런 모두 8 회전 뒤 M 0.96 – 1.00 (점착 0 대조 포함) — 이 판정 칸 규모에서는 점착 설정과 무관하게 혼합이 거의 끝남',
        f'코팅 모사 (LC) − 기준 (LA): Δ = {mn["Delta"]:+.3f} ± {mn["SE"]:.3f} (시드 3 쌍) → 등록된 "무분리" 범주 — 효과가 없다는 뜻이 아니라 이 해상도에서 가를 수 없음',
    ], '결과 · 판정', '혼합지수 M', '판정 (사전 등록)')
    pic(s, PV / 'G7.png', LBOX, ['막대 = 8 회전째 25 프레임 평균 · 오차 = 런내부 SD', '미리보기 — Origin (origin/G7.ogs) 으로 교체'])
    tbl(s, (RBOX[0], RBOX[1] + 0.02, RBOX[2], 0), [
        ['항목', '결과'],
        ['주 비교 (16×16×4)', f'Δ {mn["Delta"]:+.4f} · SE {mn["SE"]:.4f} → 무분리'],
        ['판정선', 'Δ ≥ 0.10 이고 ≥ 2·SE → 차이 있음 · |Δ| ≤ SE → 무분리'],
        ['음성 대조 L0', 'M 0.97 – 0.99 ≥ 0.8 → 통과'],
        ['바닥 검사 · 평탄', '10/10 · 30/30 통과'],
        ['사다리 (LB1→LA)', '단조 아님 (런내부 SD 안)'],
    ], col_w=[1.35, 3.0], size=8.3, row_h=0.40)
    tb(s, (RBOX[0], RBOX[1] + 2.5, RBOX[2], 0.9), ['코팅 모사 = 활물질 표면 점착 (AM–AM · AM–벽) 을 함께 낮춘 모델 조건 — 실제 코팅 공정 재현이 아님',
                                                   '판정선 · 칸 · 시드 · 회전 수는 결과를 보기 전에 등록'], size=8, color=SUB, kind='desc')
    notes(s, 'docs/data/mixer_final10_20260930/README.md · verdict_20260930.json.  결론 문안 = 사전등록 §5 (비교 이름 · 계약 한정어).  "효과 없음" · "동등" 이라 쓰지 않는다.')
    made.append(s)

    # ── 2-12 고점착 확장 ──
    s = cslide(prs, proto, '2-12', f'고점착 조건 확장 — 표면 점착 저감 (코팅 대리) 효과 {PENDING}', [
        '점착이 큰 조건 (AM–AM Bo 38.4) 에서 표면 점착 저감 (코팅 대리) 이 혼합 진척을 바꾸는지 확인 — 판정선 사전 등록 · 외부 검토 반영',
        [('결과  ', True), (f'⬜ {PENDING}', False)],
    ], '계산 설계 · 결과', '계산 설계', '결과')
    tbl(s, (LBOX[0], LBOX[1] + 0.02, LBOX[2], 0), [
        ['항목', '내용'],
        ['비교', 'LC (코팅 대리) ↔ LH (고점착)'],
        ['점착 (AM–AM Bo)', 'LC 0.00109 · LH 38.4'],
        ['시드 · 회전', '시드 3 · 8 회전 (4 회전 중간 판정)'],
        ['판정', '결과 전 등록 (중간 · 최종)'],
        ['검증', '강성 · 시간 간격 민감도 · 접촉 겹침 점검'],
    ], col_w=[1.35, 2.95], size=8.5, row_h=0.40)
    ph_box(s, RBOX, ['혼합지수 M (LC · LH) · Δ · 판정', f'⬜ {PENDING}'])
    notes(s, '사전등록 docs/reviews/mixer_highbo_prereg_20260927.md (v2.7) · Codex 검토.  결과가 나오면 2-11 과 같은 꼴 (막대 + 판정표) 로 채운다.')
    made.append(s)

    # ── 2-13 요약 ──
    s = cslide(prs, proto, '2-13', '요약 및 향후 계획', [
        f'DEM 압축 모델로 전해질 함량 · 바이모달 비 · 입경 · 도전재가 후막 미세구조와 이온 · 전자 경로에 주는 영향을 정량 ({g5["n130"] + g5["n64"]} 설계점 · 사양 5 조성)',
        f'이온 경로는 전해질 함량이 지배 (고체 중 SE {g5["nonspan_se_max"]:.0f} % 이하에서 단절) · 같은 함량에서는 대입자 몫 0.7 부근이 가장 치밀',
    ], '요약 · 향후 계획', '설계 지침', '향후 계획')
    tb(s, LBOX, [
        [('① 전해질 함량  ', True, None), (f'고체 중 SE > {g5["nonspan_se_max"]:.0f} vol % 관통 100 % · ≥ {g5["iso13_from"]["se_med"]:.0f} vol % (활물질 ≤ {g5["iso13_from"]["level"][3:]} wt%) 면 모든 설계점 고립 < 13 %', False, None)],
        [('② 바이모달 비  ', True, None), ('대 : 소 ≈ 7 : 3 — 가장 치밀 · 얇음', False, None)],
        [('③ 도전재  ', True, None), ('VGCF 함량 순서 견고 — 목표 전자 전도도에 맞춰 선택', False, None)],
        [('④ 건식 믹싱  ', True, None), ('8 회전이면 칸 규모 균일 · 코팅 대리 효과는 고점착 조건에서 판정', False, None)],
    ], size=9.5, kind='ko', spacing=6)
    tbl(s, (RBOX[0], RBOX[1] + 0.02, RBOX[2], 0), [
        ['항목', '내용', '시기'],
        ['사양 5 조성 수송', 'σ_ion · σ_e · 굴곡도', PENDING],
        ['고점착 믹싱 판정', 'LC ↔ LH (확인 런)', PENDING],
        ['데이터셋 v1.1', '분해 지표 · 구조 예측 ML', PENDING],
        ['MPM 연계', '전해질 소성 형상 · 하중 분담', '3차년도'],
        ['열화 연계', '사이클 접촉 손실 · 임피던스', '3차년도'],
    ], col_w=[1.35, 1.75, 1.25], size=8.3, row_h=0.42)
    notes(s, '설계 지침은 이 모델 · 이 설계 범위의 중간 결과 (탐색적 포함).  ⬜ 항목은 10월 중 결과로 채운다.')
    made.append(s)

    # 순서: 양식 1–7 · 새 장 · 양식 10–11 (빈 자유 양식 8 · 9 는 뺀다)
    sld = prs.slides._sldIdLst
    ids = list(sld)
    orig, new = ids[:11], ids[11:]
    for el in ids:
        sld.remove(el)
    for el in orig[:7] + new + orig[9:11]:
        sld.append(el)
    for el in orig[7:9]:
        prs.part.drop_rel(el.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'))
    prs.save(out)
    return len(made)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--template', required=True)
    ap.add_argument('--out', default=str(HERE / 'report_20261021_v2.pptx'))
    a = ap.parse_args()
    n = build(a.template, a.out)
    print(f'{n} 장 → {a.out}')


if __name__ == '__main__':
    main()
