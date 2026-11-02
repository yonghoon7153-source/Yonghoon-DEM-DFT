"""진도점검 회의 덱 (2026.11.04) 양식으로 DEM 4장 — 업로드 덱의 제목 · 글 상자 (Rectangle 23) · 캡션 XML 을 복사해 글만 바꾼다.
python3 -I build_dem4.py <fmt.pptx> <out.pptx> <figdir> <plan3d.png> <contact.png>
"""
import copy
import sys

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Pt

IN, OUT, FIG, PLAN3D, CONTACT = sys.argv[1:6]
EMU = 914400
prs = Presentation(IN)
s8, s12 = prs.slides[7], prs.slides[11]


def shape(s, name):
    return next(sh for sh in s.shapes if sh.name == name)


T_TITLE = copy.deepcopy(shape(s12, 'TextBox 1')._element)
T_RECT = copy.deepcopy(shape(s8, 'Rectangle 23')._element)
T_CAP = copy.deepcopy(shape(s8, 'Text Box 36')._element)
p8 = shape(s8, 'Rectangle 23').text_frame.paragraphs
p12 = shape(s12, 'Rectangle 23').text_frame.paragraphs
P_HEAD, P_BUL, P_ARR = copy.deepcopy(p12[0]._p), copy.deepcopy(p12[1]._p), copy.deepcopy(p12[2]._p)
R_PLAIN = copy.deepcopy(p12[1].runs[0]._r)
R_BLUE = copy.deepcopy(p12[2].runs[1]._r)
R_RED = copy.deepcopy(p8[3].runs[1]._r)
LAYOUT = s12.slide_layout
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
_blips = P_HEAD.findall('.//' + qn('a:blip'))
BULLET_IMG = [s12.part.related_part(e.get(qn('r:embed'))) for e in _blips]

# 원래 17 장은 뺀다 (양식만 쓴다)
lst = prs.slides._sldIdLst
for sid in list(lst):
    prs.part.drop_rel(sid.rId)
    lst.remove(sid)


def run(proto, text):
    r = copy.deepcopy(proto)
    r.find(qn('a:t')).text = text
    return r


def para(proto, segs, lead=None):
    p = copy.deepcopy(proto)
    for r in p.findall(qn('a:r')) + p.findall(qn('a:br')):
        p.remove(r)
    end = p.find(qn('a:endParaRPr'))
    items = ([run(R_PLAIN, lead)] if lead else []) + [run({None: R_PLAIN, 'b': R_BLUE, 'r': R_RED}[c], t) for t, c in segs]
    for r in items:
        if end is not None:
            end.addprevious(r)
        else:
            p.append(r)
    return p


def head_para(text, s=None):
    p = copy.deepcopy(P_HEAD)
    for e, part in zip(p.findall('.//' + qn('a:blip')), BULLET_IMG):
        e.set(qn('r:embed'), s.part.relate_to(part, RT.IMAGE))
    rs = p.findall(qn('a:r'))
    rs[0].find(qn('a:t')).text = '  ' + text
    for r in rs[1:]:
        p.remove(r)
    return p


def next_id(s):
    return max([int(e.get('id')) for e in s.shapes._spTree.iter(qn('p:cNvPr'))] + [1]) + 1


def put(s, tmpl, name):
    el = copy.deepcopy(tmpl)
    nv = el.find('.//' + qn('p:cNvPr'))
    nv.set('id', str(next_id(s)))
    nv.set('name', name)
    s.shapes._spTree.append(el)
    return el


def xfrm(el, x, y, w=None, h=None):
    xf = el.find('.//' + qn('a:xfrm'))
    xf.find(qn('a:off')).set('x', str(int(x * EMU)))
    xf.find(qn('a:off')).set('y', str(int(y * EMU)))
    if w is not None:
        xf.find(qn('a:ext')).set('cx', str(int(w * EMU)))
    if h is not None:
        xf.find(qn('a:ext')).set('cy', str(int(h * EMU)))


def body(s, heading, bullets, arrows, h=1.75):
    el = put(s, T_RECT, 'Rectangle 23')
    tx = el.find('.//' + qn('p:txBody'))
    for p in tx.findall(qn('a:p')):
        tx.remove(p)
    tx.append(head_para(heading, s))
    for segs in bullets:
        tx.append(para(P_BUL, segs))
    for segs in arrows:
        tx.append(para(P_ARR, segs, lead='   → '))
    xfrm(el, 0.47, 1.15, 9.41, h)


def caption(s, text, y):
    el = put(s, T_CAP, 'Text Box 36')
    tx = el.find('.//' + qn('p:txBody'))
    ps = tx.findall(qn('a:p'))
    for p in ps[1:]:
        tx.remove(p)
    rs = ps[0].findall(qn('a:r'))
    rs[0].find(qn('a:t')).text = f'【 {text} 】'
    for r in rs[1:]:
        ps[0].remove(r)
    xfrm(el, 0.60, y, 8.80, 0.28)


def pic(s, path, x, y, w):
    from PIL import Image
    im = Image.open(path)
    h = w * im.size[1] / im.size[0]
    s.shapes.add_picture(path, Emu(int(x * EMU)), Emu(int(y * EMU)), Emu(int(w * EMU)), Emu(int(h * EMU)))
    return h


def slot(s, x, y, w, h, lines):
    sp = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Emu(int(x * EMU)), Emu(int(y * EMU)), Emu(int(w * EMU)), Emu(int(h * EMU)))
    sp.name = '3D 그림 자리 (웹앱)'
    sp.fill.solid()
    sp.fill.fore_color.rgb = RGBColor(0xF7, 0xF7, 0xF7)
    sp.line.color.rgb = RGBColor(0xA6, 0xA6, 0xA6)
    sp.line.width = Pt(1)
    ln = sp.line._get_or_add_ln()
    ln.append(ln.makeelement(qn('a:prstDash'), {'val': 'dash'}))
    sp.shadow.inherit = False
    tf = sp.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    for k, t in enumerate(lines):
        p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = t
        r.font.size = Pt(12 if k == 0 else 10.5)
        r.font.color.rgb = RGBColor(0x7F, 0x7F, 0x7F)
        r.font.name = 'KoPubWorld돋움체 Medium'
        rpr = r._r.get_or_add_rPr()
        rpr.append(rpr.makeelement(qn('a:ea'), {'typeface': 'KoPubWorld돋움체 Medium'}))


def new_slide(notes):
    s = prs.slides.add_slide(LAYOUT)
    for ph in list(s.placeholders):
        ph._element.getparent().remove(ph._element)
    put(s, T_TITLE, 'TextBox 1')
    s.notes_slide.notes_text_frame.text = notes
    return s


from pptx.util import Inches


def table(s, x, y, colw, rows, size=10.5):
    nr, nc = len(rows), len(rows[0])
    gf = s.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(sum(colw)), Inches(0.30 * nr))
    tb = gf.table
    tbPr = tb._tbl.tblPr
    for k in ('firstRow', 'bandRow'):
        tbPr.set(k, '0')
    for j, w in enumerate(colw):
        tb.columns[j].width = Inches(w)
    for i, row in enumerate(rows):
        tb.rows[i].height = Inches(0.30)
        for j, txt in enumerate(row):
            c = tb.cell(i, j)
            c.fill.solid()
            c.fill.fore_color.rgb = RGBColor(0xF2, 0xF2, 0xF2) if (i == 0 or j == 0) else RGBColor(0xFF, 0xFF, 0xFF)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = c.text_frame
            tf.paragraphs[0].alignment = PP_ALIGN.CENTER
            r = tf.paragraphs[0].add_run()
            r.text = txt
            r.font.size = Pt(size)
            r.font.color.rgb = RGBColor(0x26, 0x26, 0x26)
            r.font.name = 'KoPubWorld돋움체 Medium'
            rpr = r._r.get_or_add_rPr()
            rpr.append(rpr.makeelement(qn('a:ea'), {'typeface': 'KoPubWorld돋움체 Medium'}))
            tcPr = c._tc.get_or_add_tcPr()
            for tag in ('a:lnL', 'a:lnR', 'a:lnT', 'a:lnB'):
                ln = tcPr.makeelement(qn(tag), {'w': '6350'})
                sf = ln.makeelement(qn('a:solidFill'), {})
                sf.append(sf.makeelement(qn('a:srgbClr'), {'val': 'BFBFBF'}))
                ln.append(sf)
                tcPr.append(ln)


FW = 4.30
XL, XR, YF = 0.55, 5.15, 3.15
CAP_Y = 6.45

# 1 — 요약
s = new_slide('DEM 해석 결과를 먼저 요약합니다. 고체전해질 입도만 다른 세 전극을 비교했고, 입도가 작을수록 기공도가 낮고 (22.4 → 19.6 → 18.1 %), '
              '활물질 하나에 닿는 전해질 접촉이 약 10배 늘며, 전해질 물성이 같다고 보면 정규화 유효 이온전도도가 2.4배가 됩니다. '
              '다만 미립 전해질의 이온전도도가 3 µm의 0.45배로 떨어져 (3차년도 펠릿) 1 µm 전극 전체로는 3 µm 전극과 거의 같은 수준, 손익분기 근처입니다.')
body(s, 'DEM 기반 고체전해질 입도별 복합양극 해석 결과 요약',
     [[('전해질 입도만 다른 복합양극 3종 (D50 3, 2, 1 µm) 비교', None)]],
     [[('미립화', 'b'), (': ', None), ('기공도 감소, 접촉 약 10배, 정규화 유효 이온전도도 2.4배', 'r')],
      [('전해질 이온전도도 감소 (0.45배)와 상쇄 → ', None), ('1 µm 손익분기 근처', 'b')]])
slot(s, XL, YF + 0.15, FW, 2.60, ['3D 그림 (웹앱)', '전해질 3, 2, 1 µm 복합양극 (이완 후)'])
table(s, XR, YF + 0.20, [1.60, 0.90, 0.90, 0.90],
      [['항목', '3 µm', '2 µm', '1 µm'],
       ['기공도 (%)', '22.4', '19.6', '18.1'],
       ['활물질–전해질 접촉 수', '10', '24', '100'],
       ['활물질 표면 피복률 (%)', '52.6', '54.2', '46.8'],
       ['정규화 유효 이온전도도 (3 µm = 1)', '1.0', '1.7', '2.4'],
       ['tortuosity', '13.6', '8.3', '6.0'],
       ['펠릿 이온전도도', '5.1', '—', '2.3']])
caption(s, '전해질 입도별 복합양극 미세구조 (왼쪽) 및 주요 해석 결과 (오른쪽)', CAP_Y)

# 2 — 배경
s = new_slide('50kg 과제의 방향은 전해질 미립화입니다. 전해질이 작아지면 같은 양으로도 활물질 표면에 더 많이 닿고 틈을 채울 수 있습니다. '
              '반면 3차년도 펠릿 측정에서 1 µm 전해질은 2.3 mS/cm로 3 µm (5.1)의 0.45배입니다. 구조 이득이 이 감소를 넘는지가 질문이고, 이번 해석은 구조 쪽을 DEM으로 정량화했습니다.')
body(s, '고체전해질 미립화 검토 배경',
     [[('미립 전해질: 활물질 표면 접촉 증가 및 충진에 따른 치밀화 기대', None)],
      [('미립화 시 전해질 이온전도도 감소 (3차년도 펠릿: 5.1 → 2.3 mS/cm)', None)]],
     [[('구조 이득', 'b'), ('과 ', None), ('이온전도도 감소', 'r'), ('의 상대 크기 확인 필요 → DEM 해석', None)]])
slot(s, XL, YF, FW, 2.70, ['그림 자리', '활물질 주변 전해질 배치 (3 µm vs 1 µm)'])
pic(s, f'{FIG}/d4_pellet_sigma.png', XR, YF, FW)
caption(s, '미립 전해질의 활물질 표면 접촉 (왼쪽) 및 입도별 전해질 펠릿 이온전도도 (오른쪽, 3차년도)', CAP_Y)

# 3 — 방법
s = new_slide('DEM으로 고체전해질 입도만 다른 세 전극을 같은 절차로 만들었습니다. 입자를 만들고 중력으로 쌓은 뒤 300 MPa까지 누르고, '
              '판을 고정해 이완시킨 상태를 비교합니다. 접촉력은 누를 때와 뗄 때 기울기가 다른 스프링과 마찰로 계산합니다. '
              '왼쪽 그림은 50kg 계획 단계의 예시이고, 오른쪽은 설명용 2D 모식입니다.')
body(s, 'DEM 기반 복합양극 미세구조 시뮬레이션',
     [[('전해질 입도만 변경 (D50 3, 2, 1 µm), NCM (6 µm) 85 wt% 고정', None)],
      [('입자 생성 → 중력 침강 → 300 MPa 가압 → 판 고정 이완 (LIGGGHTS)', None)]],
     [[('입자 간 접촉력', 'b'), (' (이력 스프링, 마찰) 기반 ', None), ('복합양극 구조 구현', 'b')]])
pic(s, PLAN3D, XL, YF + 0.25, FW)
pic(s, CONTACT, XR, YF, FW)
caption(s, 'DEM 해석 절차 (왼쪽, 50kg 계획 예시) 및 입자 접촉 모델 (오른쪽, 2D 모식)', CAP_Y)

# 4 — 기공도 (exact union)
s = new_slide('같은 300 MPa로 눌렀을 때 기공도는 3 µm 22.4 %, 2 µm 19.6 %, 1 µm 18.1 %로 입도가 작을수록 낮습니다. '
              '작은 전해질이 활물질 사이 틈을 채운 결과이고, 3 → 2 µm 차이는 두께 방향 모든 구간에서 같은 방향입니다.')
body(s, '고체전해질 미립화에 따른 복합양극 기공도 변화',
     [[('동일 조건 (300 MPa 가압 후 판 고정 이완)에서 전해질 입도별 구조 비교', None)]],
     [[('미립 전해질의 충진 효과', 'b'), ('로 ', None), ('기공도 감소', 'r'), (' (22.4 → 19.6 → 18.1 %)', None)],
      ])
slot(s, XL, YF, FW, 2.70, ['3D 그림 (웹앱)', '전해질 3, 2, 1 µm 복합양극 (이완 후)'])
pic(s, f'{FIG}/d4_porosity_plain.png', XR, YF, FW)
caption(s, '전해질 입도별 복합양극 미세구조 (왼쪽) 및 기공도 (오른쪽)', CAP_Y)

# 5 — 접촉
s = new_slide('활물질 하나에 닿은 전해질 입자는 3 µm 10개, 2 µm 24개, 1 µm 100개로 약 10배 늘어납니다. '
              '활물질 표면 피복률은 47–54 %로 비슷해, 같은 표면을 더 많은 작은 접촉으로 나눠 덮는 셈입니다.')
body(s, '고체전해질 미립화에 따른 활물질/전해질 접촉',
     [[('활물질 1개당 전해질 접촉 수 및 활물질 표면 피복률 분석', None)]],
     [[('전해질 미립화', 'b'), ('에 따른 ', None), ('활물질/전해질 접촉 약 10배 증가', 'r'), (' (10 → 24 → 100개)', None)],
      [('활물질 표면 피복률은 유사 (47–54 %) → ', None), ('같은 표면을 다수의 작은 접촉으로 분할', 'b')]])
pic(s, f'{FIG}/d4_contacts.png', XL, YF, FW)
pic(s, f'{FIG}/d4_coverage.png', XR, YF, FW)
caption(s, '전해질 입도별 활물질 1개당 전해질 접촉 수 (왼쪽) 및 활물질 표면 피복률 (오른쪽)', CAP_Y)

# 6 — 이온 이동 경로
s = new_slide('전해질 물성을 같게 두고 구조만 비교하면, 정규화 유효 이온전도도 (전극 유효 이온전도도 ÷ 전해질 이온전도도)는 2 µm에서 1.7배, 1 µm에서 2.4배가 됩니다. '
              '같은 계산에서 tortuosity는 13.6, 8.3, 6.0으로 줄어듭니다. 모든 활물질이 전해질 망에 연결되어 고립된 활물질은 없습니다.')
body(s, '고체전해질 미립화에 따른 정규화 유효 이온전도도 및 tortuosity',
     [[('전해질 물성 동일 가정 하 정규화 유효 이온전도도 (전극 ÷ 전해질 이온전도도) 분석', None)]],
     [[('전해질 미립화', 'b'), ('에 따른 ', None), ('정규화 유효 이온전도도 1.7배 (2 µm), 2.4배 (1 µm)', 'r')],
      [('tortuosity 감소', 'r'), (' (13.6 → 8.3 → 6.0), 전 활물질 전해질 망 연결', None)]])
pic(s, f'{FIG}/d4_ion_path.png', XL, YF, FW)
pic(s, f'{FIG}/d4_tortuosity.png', XR, YF, FW)
caption(s, '전해질 입도별 정규화 유효 이온전도도 (왼쪽, 3 µm 대비) 및 tortuosity (오른쪽)', CAP_Y)

# 7 — 손익분기
s = new_slide('미립화에는 대가가 있습니다. 3차년도 펠릿 측정에서 1 µm 전해질은 2.3 mS/cm로 3 µm (5.1)의 0.45배입니다. '
              '정규화 유효 이온전도도 2.4배와 곱하면 1 µm 전극의 유효 이온전도도는 3 µm 전극의 약 1.1배, 손익분기 근처입니다. '
              '1 µm 전극이 앞서려면 미립 전해질 이온전도도가 3 µm 전해질의 0.42배 (2.1 mS/cm) 이상이어야 합니다.\n'
              '※ 이 덱 8쪽 새 측정 (small/large) 으로 보면 LPSC1.0 1.51/2.63 = 0.57배 (우위 범위), LPSC1.5 2.98/7.84 = 0.38배 (열위 범위) — small = 1 µm, large = 3 µm 대응 확인 뒤 슬라이드 반영 여부 결정.')
body(s, '미립화 구조 이득과 전해질 이온전도도 감소의 손익분기',
     [[('정규화 유효 이온전도도 2.4배 × 전해질 이온전도도 0.45배 ≈ 1.1배', None)],
      [('1 µm 전극 우위 조건: 미립 전해질 ≥ 2.1 mS/cm (3 µm의 0.42배)', None)]],
     [[('미립화 이득은 ', None), ('미립 전해질의 이온전도도 유지', 'b'), ('에 의존', None)]])
pic(s, f'{FIG}/d4_pellet_sigma.png', XL, YF, FW)
pic(s, f'{FIG}/d4_breakeven1.png', XR, YF, FW)
caption(s, '입도별 전해질 펠릿 이온전도도 (왼쪽, 3차년도) 및 3 µm 전극과 같아지는 전해질 이온전도도 (오른쪽, ◆ 실측)', CAP_Y)

# 8 — 결론 · 계획
s = new_slide('정리하면, 전해질 미립화는 전극 구조를 분명히 좋게 만들지만, 미립 전해질의 이온전도도 감소와 거의 상쇄됩니다. '
              '계산에서 이온 전달 저항의 약 4분의 3이 전해질끼리 맞닿은 접촉부에 몰려 있어 접촉 상태도 다음 과제입니다. '
              '다음 단계는 입도별 반복 계산, 2 µm 펠릿 측정, 그리고 이 구조로 3차원 전기화학 시뮬레이션입니다.')
body(s, 'DEM 해석 결론 및 향후 계획',
     [[('결론: 전해질 미립화에 따른 구조 개선 (기공도 감소, 접촉 약 10배, 정규화 유효 이온전도도 2.4배) 확인', None)],
      [('미립 전해질 이온전도도 감소 (0.45배)와 상쇄되어 1 µm 전극은 손익분기 근처', None)],
      [('이온 전달 저항의 약 3/4이 전해질–전해질 접촉부에 집중', None)]],
     [[('향후: ', None), ('입도별 반복 계산', 'b'), (', 2 µm 펠릿 이온전도도 측정', None)],
      [('DEM 구조 기반 ', None), ('3차원 전기화학 시뮬레이션', 'b'), (' (방전 용량 비교)', None)]], h=3.2)

prs.save(OUT)
print('ok', OUT, len(prs.slides))
