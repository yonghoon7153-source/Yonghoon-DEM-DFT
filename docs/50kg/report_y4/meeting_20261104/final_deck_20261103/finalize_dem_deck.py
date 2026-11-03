"""1저자 덱 (50kg_report_DEM_slides_1.pptx) → DEM 장 (6–15) 최종 — 1저자 11-03:
'geometric tortuosity 안 넣고 수송 tortuosity 를 tortuosity 로만' · '사진 = 준 것 활용 또는 공백' · 'origin 값 표시' · '다 최종본으로'.
바꾸는 것만 바꾼다 (글 run 서식 그대로 · 그림 칸 = 비율 유지 가운데 맞춤 → 점선 칸 지움 · 빈 칸은 점선 그대로)."""
import io, re, sys, copy
from pathlib import Path
from pptx import Presentation
from pptx.util import Emu
from PIL import Image

SRC, OUT, CHARTS, IMGS, REPO, P06, D1FIG = (Path(a) for a in sys.argv[1:8])
FIG = REPO / 'docs/50kg/report_y4/meeting_20261104/figs'
prs = Presentation(str(SRC))
S = {i + 1: s for i, s in enumerate(prs.slides)}
log = []


def all_shapes(container):
    for sh in container.shapes:
        if sh.shape_type == 6:
            yield from all_shapes(sh)
        else:
            yield sh


def norm(t):
    return re.sub(r'\s+', ' ', t).strip()


def set_text_keep_first_run(sh, new):
    tf = sh.text_frame
    p0 = tf.paragraphs[0]
    runs = p0.runs
    assert runs, sh.name
    runs[0].text = new
    for r in runs[1:]:
        r._r.getparent().remove(r._r)
    for p in tf.paragraphs[1:]:
        p._p.getparent().remove(p._p)


def relabel(slide_no, old, new, expect):
    n = 0
    for sh in all_shapes(S[slide_no]):
        if sh.has_text_frame and norm(sh.text_frame.text) == old:
            set_text_keep_first_run(sh, new); n += 1
    assert n == expect, (slide_no, old, n)
    log.append(f's{slide_no}: "{old}" → "{new}" × {n}')


def revalue(slide_no, vals):
    boxes = [sh for sh in all_shapes(S[slide_no]) if sh.has_text_frame and re.fullmatch(r'\d\.\d\d', norm(sh.text_frame.text))]
    assert len(boxes) == 3, (slide_no, [b.text_frame.text for b in boxes])
    boxes.sort(key=lambda b: b.left)
    old = [norm(b.text_frame.text) for b in boxes]
    for b, v in zip(boxes, vals):
        set_text_keep_first_run(b, v)
    log.append(f's{slide_no}: 값 {old} → {vals}')


def drop_word_before(slide_no, word='수송 ', target='tortuosity'):
    """문단 run 들에 걸쳐 있어도 '수송 tortuosity' → 'tortuosity' (서식 그대로)."""
    n = 0
    for sh in all_shapes(S[slide_no]):
        if not sh.has_text_frame:
            continue
        for p in sh.text_frame.paragraphs:
            while True:
                runs = p.runs
                full = ''.join(r.text for r in runs)
                k = full.find(word + target)
                if k < 0:
                    break
                # word 의 글자 범위 [k, k+len(word)) 를 run 별로 지운다
                pos, lo, hi = 0, k, k + len(word)
                for r in runs:
                    a, b = pos, pos + len(r.text)
                    cut_a, cut_b = max(a, lo), min(b, hi)
                    if cut_a < cut_b:
                        r.text = r.text[:cut_a - a] + r.text[cut_b - a:]
                    pos = b
                n += 1
    log.append(f's{slide_no}: "{word}{target}" → "{target}" × {n}')
    return n


def replace_picture(slide_no, name, png):
    sh = next(s for s in all_shapes(S[slide_no]) if s.name == name and s.shape_type == 13)
    part, rid = S[slide_no].part.get_or_add_image_part(str(png))
    blip = sh._element.xpath('.//a:blip')[0]
    blip.set('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed', rid)
    log.append(f's{slide_no}: 그림 "{name}" ← {png.name}')


def fill_slot(slide_no, slot_name, img_path, tag):
    slide = S[slide_no]
    slot = next(s for s in all_shapes(slide) if s.name == slot_name)
    im = Image.open(img_path)
    if im.mode not in ('RGB', 'RGBA'):
        im = im.convert('RGBA')
    bb = im.getbbox() if im.mode == 'RGBA' else None
    if bb:
        im = im.crop(bb)
    buf = io.BytesIO(); im.save(buf, 'PNG'); buf.seek(0)
    pad = Emu(int(0.03 * 914400))
    W, H = slot.width - 2 * pad, slot.height - 2 * pad
    r = min(W / im.width, H / im.height)
    w, h = int(im.width * r), int(im.height * r)
    x = slot.left + (slot.width - w) // 2
    y = slot.top + (slot.height - h) // 2
    pic = slide.shapes.add_picture(buf, x, y, w, h)
    pic.name = tag
    slot._element.getparent().remove(slot._element)
    log.append(f's{slide_no}: {slot_name} ← {Path(img_path).name}')


def webp_png(p):
    out = Path(OUT).parent / (p.stem + '_conv.png')
    Image.open(p).save(out); return out


def set_notes(slide_no, text):
    ns = S[slide_no].notes_slide
    ns.notes_text_frame.text = text
    log.append(f's{slide_no}: 노트 갱신')


# ── 7장 (입도 · 구조 · 두께 · 기공)
relabel(7, 'Transport tortuosity', 'Tortuosity', 3)
drop_word_before(7)
set_notes(7, 'D_SE = 1 / 2 / 3 µm: 질량 보존 두께 124.57 / 126.83 / 131.50 µm, 기공도 18.1 / 19.6 / 22.4 %, '
             'tortuosity 6.00 / 8.26 / 13.63 (= φ_SE·σ₀/σ_eff · 이온 수송 · 제곱근 아님), 유효 이온전도도 0.070 / 0.050 / 0.029 mS/cm (σ₀ = 1.5 mS/cm 기준).\n'
             '경로 그림 = SE 망 경로 예시 (값은 그림이 아니라 전도도 해에서 나온 tortuosity).\n'
             '⚠ 질문 대비: 1 µm 는 압축 중 판 압력의 약 65 % 가 감쇠 항력 상당 — 1 µm 기공 · tortuosity 는 2 · 3 µm 와 같은 접촉망 응력에서 압밀된 값이 아님 (원장 KG50-20).\n'
             'Origin 자료: 시트 p07_thickness_DSE · p07_porosity_DSE.')

# ── 8장 (입도 · 미세구조 비교)
relabel(8, 'Geometric tortuosity', 'Tortuosity', 3)
revalue(8, ['6.00', '8.26', '13.63'])
r = {1: '29', 2: '27', 3: '28'}; pth = {1: '30', 2: '31', 3: '32'}; um = {1: 1, 2: 2, 3: 3}
for c in (1, 2, 3):
    fill_slot(8, f'Image slot Structure {c}', webp_png(IMGS / f'{r[c]}.webp'), f'Structure D{c}')
    fill_slot(8, f'Image slot Pore {c}', FIG / 'pore3d' / f'pore3d_{um[c]}um.png', f'Pore D{c}')
    fill_slot(8, f'Image slot Geometric tortuosity {c}', webp_png(IMGS / f'{pth[c]}.webp'), f'Tortuosity path D{c}')
set_notes(8, 'D_SE = 1 / 2 / 3 µm: 활물질 (NCM) 1개당 전해질 접촉 수 99.7 / 24.1 / 10.3개, 기공도 18.1 / 19.6 / 22.4 %, '
             'tortuosity 6.00 / 8.26 / 13.63 (= φ_SE·σ₀/σ_eff · 이온 수송).\n'
             'Structure · Pore · Tortuosity 그림 = 웹앱 캡처 (경로 그림 = 예시 · 값은 전도도 해) · SE contacts per AM 칸 = 그림 대기 (1저자 웹앱 AM–SE 접촉 보기 캡처 · coverage 는 1저자 11-03 결정으로 뺌).')

# ── 9장 (입도 · 지표)
drop_word_before(9)
replace_picture(9, 'p09_tortuosity_DSE', CHARTS / 'p09_tortuosity_DSE.png')
set_notes(9, 'D_SE = 1 / 2 / 3 µm: 기공도 (시뮬레이션) 18.1 / 19.6 / 22.4 %, tortuosity 6.00 / 8.26 / 13.63 (수송 · φ_SE·σ₀/σ_eff), coverage 46.8 / 54.2 / 52.6 %.\n'
             'Origin 자료: 시트 p09_porosity_DSE · p09_tortuosity_DSE · p09_coverage_DSE.')

# 1저자 11-03 '피복률 저거는 안넣을듯 · AM–SE contacts 갯수로 넣을거같아' — 9장 coverage 막대 → NCM 1개당 SE 접촉 수 (같은 자리 · 같은 크기)
#   + 둘째 글머리 · 노트 (coverage 값 · 이유는 질문 대비로 노트에만) · 8장 Coverage 칸 이름 · 값 · 글머리도 같은 결정으로
replace_picture(9, 'p09_coverage_DSE', CHARTS / 'p09_contacts_DSE.png')
next(x for x in S[9].shapes if x.name == 'p09_coverage_DSE').name = 'p09_contacts_DSE'
_A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
_paras = [pp for x in all_shapes(S[9]) if x.has_text_frame for pp in x.text_frame.paragraphs]
_b1 = next(pp for pp in _paras if [r.text for r in pp.runs][:2] == ['입도 감소 시 ', '기공도 감소'])
_b2 = next(pp for pp in _paras if [r.text for r in pp.runs] == ['활물질 coverage는 2 µm에서 최대 (54.2 %), 1 µm에서 최소 (46.8 %)'])
_r0 = _b2.runs[0]
_r0.text = '활물질 1개당 전해질 '
_blue = copy.deepcopy(_b1.runs[1]._r); _r0._r.addnext(_blue)
_tail = copy.deepcopy(_r0._r); _blue.addnext(_tail)
_b2.runs[1].text = '접촉 수 증가'
_b2.runs[2].text = ' (10.3 → 99.7개)'
set_notes(9, 'D_SE = 1 / 2 / 3 µm: 기공도 (시뮬레이션) 18.1 / 19.6 / 22.4 %, tortuosity 6.00 / 8.26 / 13.63 (수송 · φ_SE·σ₀/σ_eff), '
             '활물질 (NCM) 1개당 전해질 접촉 수 99.7 / 24.1 / 10.3개 (평균).\n'
             '질문 대비 (화면에 안 씀): coverage 46.8 / 54.2 / 52.6 % 는 덱에서 뺐다 — 접촉 수는 약 10 배지만 접촉 하나 면적이 0.21 / 0.94 / 1.97 µm² 라 '
             '활물질당 접촉 면적 합은 21.0 / 22.6 / 20.3 µm² 로 비슷하다 (docs/50kg/report_y4/draft2/metrics_all.csv).\n'
             'Origin 자료: 시트 p09_porosity_DSE · p09_tortuosity_DSE · p09_contacts_DSE.')
log.append('s9: coverage 막대 → 접촉 수 막대 · 둘째 글머리 · 노트')
relabel(8, 'Coverage', 'SE contacts per AM', 3)
for _o, _n in (('46.8 %', '99.7'), ('54.2 %', '24.1'), ('52.6 %', '10.3')):
    relabel(8, _o, _n, 1)
_r8 = [r for x in all_shapes(S[8]) if x.has_text_frame for pp in x.text_frame.paragraphs for r in pp.runs
       if r.text == '구조, coverage, 기공 및 이온 이동 경로']
assert len(_r8) == 1, len(_r8)
_r8[0].text = '구조, 활물질–전해질 접촉, 기공 및 이온 이동 경로'
log.append('s8: Coverage 칸 → SE contacts per AM (그림 칸 = 공백 · 1저자 웹앱 캡처 자리) · 글머리')

# ── 10장 (입도 · 이온전도도) — 글 그대로 · 노트에 Origin
old10 = S[10].notes_slide.notes_text_frame.text
set_notes(10, old10.rstrip() + '\nOrigin 자료: 시트 p11_sigma_DSE.')

# 1저자 11-03 '이 페이지에 이것들 잘 넣어봐' · '저 컬러바를 좀 조정해야될거 같은데' — 10장 이온 전류 3D 셋 = 11-02 웹앱 캡처 (figs/jcur · MANIFEST).
# 웹앱 색 위쪽 = 전극마다 접촉 전류 밀도 중앙값 (p50) → 세 그림이 같은 절대 눈금이 아니다 → 공동 컬러바 = 중앙값으로 나눈 값 (0 – 1) + 그림 아래 그 전극의 중앙값.
import json as _json
JC = FIG / 'jcur'
_man = _json.loads((JC / 'src' / 'MANIFEST.json').read_text(encoding='utf-8'))['beds']
MED = {c: _man[f'D{c}']['colorbar_ticks_A_cm2'][-1] for c in (1, 2, 3)}       # 위쪽 끝 = 중앙값 (0.22 · 0.14 · 0.094)
NCC = {c: _man[f'D{c}']['current_carrying_contacts'] for c in (1, 2, 3)}
for c in (1, 2, 3):
    fill_slot(10, f'Image slot current density {c}', JC / f'jcur3d_{c}um.png', f'Ion current D{c}')
s10 = S[10]
_lab = next(x for x in s10.shapes if x.name == 'Colorbar label')
_runs = _lab.text_frame.paragraphs[0].runs
assert [r.text for r in _runs][:2] == ['[ Li', '+'], [r.text for r in _runs]
_runs[2].text = ' current density / median ]'
for _r in _runs[3:]:
    _r._r.getparent().remove(_r._r)
_mn = next(x for x in s10.shapes if x.name == 'Colorbar min')
_mx = next(x for x in s10.shapes if x.name == 'Colorbar max (edit)')
_p = _mx.text_frame.paragraphs[0]._p
_p.insert(len(_p) - 1, copy.deepcopy(_mn.text_frame.paragraphs[0].runs[0]._r))
_mx.text_frame.paragraphs[0].runs[0].text = '1'
_mx.name = 'Colorbar max'
_ids = [int(e.get('id')) for e in s10.shapes._spTree.iter() if e.tag.endswith('}cNvPr')]
_pics = {c: next(x for x in s10.shapes if x.name == f'Ion current D{c}') for c in (1, 2, 3)}
_y = max(p.top + p.height for p in _pics.values()) + Emu(int(0.05 * 914400))
for c in (1, 2, 3):
    _el = copy.deepcopy(_mn._element)
    _mn._element.addnext(_el)
    _cnv = _el.xpath('./p:nvSpPr/p:cNvPr')[0]
    _cnv.set('id', str(max(_ids) + c)); _cnv.set('name', f'Median label {c}')
    _sh = next(x for x in s10.shapes if x._element is _el)
    _sh.left, _sh.width = _pics[c].left - Emu(int(0.2 * 914400)), _pics[c].width + Emu(int(0.4 * 914400))
    _sh.top, _sh.height = _y, Emu(int(0.2 * 914400))
    _r0 = _sh.text_frame.paragraphs[0].runs[0]
    _r0.text = f'median {MED[c]} A cm'
    _r1 = copy.deepcopy(_r0._r); _r0._r.addnext(_r1)
    _sh.text_frame.paragraphs[0].runs[1].text = '−2'
    _r1.find('{http://schemas.openxmlformats.org/drawingml/2006/main}rPr').set('baseline', '30000')
set_notes(10, ('3D = 세 전극에 각각 1 V 를 걸었을 때 전해질–전해질 접촉의 Li⁺ 전류 밀도 (Hertz 접촉 · 전류가 흐르는 접촉 전부 = '
               f'1 µm {NCC[1]} · 2 µm {NCC[2]} · 3 µm {NCC[3]} 개 · 11-02 웹앱 캡처).\n'
               '색 = 각 전극의 접촉 전류 밀도를 그 전극의 중앙값으로 나눈 값 (웹앱 색 위쪽 = 전극마다 중앙값이라 세 그림에 공통 절대 눈금이 없다) · '
               f'중앙값 {MED[1]} / {MED[2]} / {MED[3]} A cm⁻² = 그림 아래.\n') + old10.rstrip() + '\nOrigin 자료: 시트 p11_sigma_DSE.')
log.append('s10: 이온 전류 3D 셋 + 공동 컬러바 (중앙값으로 나눈 값 0 – 1) + 그림 아래 중앙값')

# ── 11장 (영률 · 구조 · 두께 · 기공)
relabel(11, 'Transport tortuosity', 'Tortuosity', 3)
fill_slot(11, 'Image slot E22', webp_png(IMGS / '27.webp'), 'Structure E22')   # 22 GPa = D_SE 2 µm 와 같은 침대 · 11 · 33 GPa = 공백
# 1저자 11-03 '여기에 tortuosity도 넣어주고' — 7장처럼 경로 그림 (값 아래) · 22 GPa = 31 (2 µm 같은 침대) · 11 · 33 GPa = 점선 칸
labs = sorted([sh for sh in all_shapes(S[11]) if sh.has_text_frame and norm(sh.text_frame.text) == 'Tortuosity'], key=lambda b: b.left)
vals = sorted([sh for sh in all_shapes(S[11]) if sh.has_text_frame and re.fullmatch(r'\d\.\d\d', norm(sh.text_frame.text))], key=lambda b: b.left)
assert len(labs) == 3 and len(vals) == 3
tmpl = next(sh for sh in all_shapes(S[11]) if sh.name == 'Image slot E11')
PW, PH = Emu(int(0.76 * 914400)), Emu(int(1.38 * 914400))
for c, (lab, val) in enumerate(zip(labs, vals), start=1):
    cx = lab.left + lab.width // 2
    x, y = cx - PW // 2, val.top + val.height + Emu(int(0.06 * 914400))
    el = copy.deepcopy(tmpl._element)
    el.xpath('.//p:cNvPr')[0].set('name', f'Image slot path {c}')
    el.xpath('.//p:cNvPr')[0].set('id', str(5000 + c))
    off, ext = el.xpath('.//a:off')[0], el.xpath('.//a:ext')[0]
    off.set('x', str(int(x))); off.set('y', str(int(y))); ext.set('cx', str(int(PW))); ext.set('cy', str(int(PH)))
    tmpl._element.getparent().append(el)
fill_slot(11, 'Image slot path 2', webp_png(IMGS / '31.webp'), 'Tortuosity path E22')
log.append('s11: tortuosity 경로 칸 셋 (22 GPa = 31 · 11 · 33 GPa = 점선)')
drop_word_before(11)
set_notes(11, 'E_SE = 11 / 22 / 33 GPa (22 GPa 의 ×0.5 / ×1 / ×1.5), DEM 유효 입력 0.675 · 1.35 · 2.025 GPa.\n'
              '질량 보존 두께 123.61 / 126.83 / 129.39 µm, 기공도 17.5 / 19.6 / 21.2 %, tortuosity 7.80 / 8.26 / 9.05 (= φ_SE·σ₀/σ_eff · 이온 수송).\n'
              '22 GPa 구조 그림 = D_SE 2 µm 와 같은 침대 · 11 · 33 GPa 그림 = 대기.\n'
              'Origin 자료: 시트 p12_thickness_ESE · p12_porosity_ESE.')

# ── 12장 (영률 · 미세구조 비교) — 22 GPa = D_SE 2 µm 와 같은 침대 → 그 그림 · 11 · 33 GPa 칸 = 공백
relabel(12, 'Geometric tortuosity', 'Tortuosity', 3)
revalue(12, ['7.80', '8.26', '9.05'])
fill_slot(12, 'Image slot Structure 2', webp_png(IMGS / '27.webp'), 'Structure E22')
fill_slot(12, 'Image slot Pore 2', FIG / 'pore3d' / 'pore3d_2um.png', 'Pore E22')
fill_slot(12, 'Image slot Geometric tortuosity 2', webp_png(IMGS / '31.webp'), 'Tortuosity path E22')
set_notes(12, 'E_SE = 11 / 22 / 33 GPa (DEM 유효 입력 0.675 · 1.35 · 2.025 GPa): coverage 61.3 / 54.2 / 48.1 %, 기공도 17.5 / 19.6 / 21.2 %, '
              'tortuosity 7.80 / 8.26 / 9.05 (= φ_SE·σ₀/σ_eff · 이온 수송).\n'
              '22 GPa 칸 그림 = D_SE 2 µm 와 같은 침대 · 11 · 33 GPa 그림 = 대기 (웹앱 캡처).')

# ── 13장 (영률 · 지표)
drop_word_before(13)
replace_picture(13, 'p14_tortuosity_ESE', CHARTS / 'p14_tortuosity_ESE.png')
set_notes(13, 'E_SE = 11 / 22 / 33 GPa: 기공도 (시뮬레이션) 17.5 / 19.6 / 21.2 %, tortuosity 7.80 / 8.26 / 9.05 (수송 · φ_SE·σ₀/σ_eff), coverage 61.3 / 54.2 / 48.1 %.\n'
              'Origin 자료: 시트 p14_porosity_ESE · p14_tortuosity_ESE · p14_coverage_ESE.')

# ── 14장 (영률 · 응력 지도)
SM = FIG / 'stress_maps'
for c, g in ((1, '11'), (2, '22'), (3, '33')):
    fill_slot(14, f'Image slot NCM {c}', SM / f'modulus_{g}GPa_NCM.png', f'Stress NCM E{g}')
    fill_slot(14, f'Image slot SE {c}', SM / f'modulus_{g}GPa_SE.png', f'Stress SE E{g}')
set_notes(14, '이완 후 von Mises 응력 중앙값 (Love–Weber · 벽 · 판 접촉 입자 제외): 활물질 352.75 / 334.85 / 325.98 MPa, 고체전해질 84.73 / 125.96 / 151.51 MPa.\n'
              '이완 끝 가압판 압력 278.46 / 279.79 / 280.14 MPa (E_SE = 11 / 22 / 33 GPa).\n'
              '그림 = 판 · 바닥 접촉 입자 뺌 · 색 NCM 0–600 · SE 0–300 MPa 고정 (선형 jet) · 웹앱 3D 뷰어와 같은 렌더.\n'
              'Origin 자료: 시트 p14_stress_ESE.')

# ── 15장 (영률 · 이온전도도)
old15 = S[15].notes_slide.notes_text_frame.text
set_notes(15, old15.rstrip() + '\nOrigin 자료: 시트 p16_sigma_ESE.')

# ── 남은 'Geometric' · 'Transport tortuosity' · '기하 tortuosity' 가 DEM 장 화면 글에 있으면 멈춤
bad = []
for i in range(4, 16):
    for sh in all_shapes(S[i]):
        if sh.has_text_frame:
            t = sh.text_frame.text
            if re.search(r'Geometric|Transport\s*tortuosity|기하 tortuosity|수송 tortuosity', t):
                bad.append((i, sh.name, t[:60]))
assert not bad, bad
def replace_slide_from(src_path, pos):
    src = Presentation(str(src_path)).slides[0]
    old = prs.slides[pos - 1]
    new = prs.slides.add_slide(old.slide_layout)
    for sh in list(new.shapes):
        sh._element.getparent().remove(sh._element)
    R = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
    for el in src.shapes._spTree.iterchildren():
        if el.tag.endswith('}nvGrpSpPr') or el.tag.endswith('}grpSpPr'):
            continue
        e2 = copy.deepcopy(el)
        for node in e2.iter():
            for att in (R + 'embed', R + 'link'):
                rid = node.get(att)
                if rid:
                    part = src.part.related_part(rid)
                    _, nrid = new.part.get_or_add_image_part(io.BytesIO(part.blob))
                    node.set(att, nrid)
        new.shapes._spTree.append(e2)
    if src.has_notes_slide:
        new.notes_slide.notes_text_frame.text = src.notes_slide.notes_text_frame.text
    lst = prs.slides._sldIdLst
    ids = list(lst)
    new_id, old_id = ids[-1], ids[pos - 1]
    lst.remove(new_id); lst.insert(pos - 1, new_id)
    prs.part.drop_rel(old_id.rId); lst.remove(old_id)
    log.append(f's{pos}: 1저자 한 장 덱 ({src_path.name}) 으로 바꿔 끼움')
    return prs.slides[pos - 1]


# 1저자 11-03 표준 (위 · 오른쪽 축선 없음) — 덱의 막대 그림 전부를 같은 값 · 같은 크기의 열린 틀 판으로
for _no, _names in ((7, ('kg50t_p07_thickness_DSE', 'kg50t_p07_porosity_DSE')), (9, ('p09_porosity_DSE', 'p09_contacts_DSE')),
                    (10, ('p11_sigma_DSE',)), (11, ('kg50t_p12_thickness_ESE', 'kg50t_p12_porosity_ESE')),
                    (13, ('p14_porosity_ESE', 'p14_coverage_ESE')), (15, ('p16_sigma_ESE',))):
    for _n in _names:
        replace_picture(_no, _n, CHARTS / (_n.replace('kg50t_', '') + '.png'))
s6 = replace_slide_from(P06, 6)
# 1저자 11-03 '우측, 위측 테두리는 없애줘 그게 우리 표준이야' — 압밀 곡선 = 위 · 오른쪽 축선 없는 판 (make_fig_d1_ms.py 기본)
_pic = next(sh for sh in s6.shapes if sh.shape_type == 13 and sh.name == 'D1 compaction curves')
_, _rid = s6.part.get_or_add_image_part(str(D1FIG))
_pic._element.xpath('.//a:blip')[0].set('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed', _rid)
log.append(f's6: 압밀 곡선 ← {D1FIG.name} (위 · 오른쪽 축선 없음)')
s6.notes_slide.notes_text_frame.text = s6.notes_slide.notes_text_frame.text.rstrip() + ('\n'
    '⚠ 질문 대비 (화면에 안 씀): 1 µm 는 압축 중 판 압력의 약 65 % 가 감쇠 항력 상당 (R_drag 0.647 · 접촉망 평균 응력 158 MPa · 2 µm 0.074 · 3 µm 0.026) — 판 정지 뒤 압력 하락 원인은 확정 아님 (원장 KG50-20).\n'
    'Origin 자료: 50kg_DEM_origin_data.xlsx 시트 p06_D1_compaction (시간 · 두께 · 압력 · 가압판 속도).')
prs.save(str(OUT))
print('\n'.join(log))
print('saved', OUT)
