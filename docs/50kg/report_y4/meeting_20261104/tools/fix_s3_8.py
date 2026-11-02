"""진도점검 덱 3–8장 고침 (1저자 11-02 "2pg- 끝페이지까지도 다시한번 확인하고 진행해봐") — 1장 · 2장에서 정한 규칙을 나머지 장에 그대로:
  · 캡션 (왼쪽) · (오른쪽) 빼기 (다른 한정어는 둠)                         — "왼쪽 오른쪽 이렇게 캡션하지말고"
  · 좋은 결과의 빨강 → 같은 문단 일반 글 색 (빨강 = 나쁜 것만)              — 1장 1저자 저장본 · "빨간색 남발하지마" · "상쇄된건 안좋은거니까 빨간부분"
  · 8장 '감소와 상쇄' = 빨강 (1장과 같은 문장)
  · 6장 정의 괄호 = 기호 σ_eff/σ_0 (σ 이탤릭 · eff · 0 아래첨자)          — "eff/0 이거써서" · "italic 같은거 잘 지키고"
  · 4장 '동일 조건' → '같은 절차' (화면 · 노트) — 초안 3 하지 않을 말 '모든 조건이 같다' · '300 MPa 상태'
  · 4장 그림 자리 = 3 · 2 · 1 µm 세 칸 + 라벨 (1장과 같은 서식)
  · 6장 노트 = 8장 결론 '저항 약 3/4' 의 근거 한 줄 (constriction_power_share_ion_hertz 0.710 · 0.715 · 0.742)
usage: python3 -I fix_s3_8.py in.pptx out.pptx
고칠 글이 정확히 하나여야 한다 (아니면 멈춘다).
"""
import copy
import sys

from pptx import Presentation
from pptx.oxml.ns import qn

SRC, DST = sys.argv[1:3]
IN = 914400
prs = Presentation(SRC)
S = {n: prs.slides[n - 1] for n in range(1, len(prs.slides) + 1)}
log = []


def runs(slide):
    out = []
    for sh in slide.shapes:
        if sh.has_text_frame:
            for p in sh.text_frame.paragraphs:
                out += [(p, r) for r in p.runs]
    return out


def one(slide, text, sub=False):
    hits = [(p, r) for p, r in runs(slide) if (text in r.text if sub else r.text == text)]
    if len(hits) != 1:
        raise SystemExit(f'대상 run {len(hits)} 개: {text[:40]}')
    return hits[0]


def color_of(r):
    rpr = r._r.find(qn('a:rPr'))
    c = rpr.find(qn('a:solidFill') + '/' + qn('a:srgbClr')) if rpr is not None else None
    return c.get('val') if c is not None else None


def to_plain(slide, text):
    p, r = one(slide, text)
    assert color_of(r) == 'FF5050', f'빨강 아님: {text}'
    plain = [x for x in p.runs if color_of(x) not in ('FF5050', '0070C0')]
    assert plain, f'같은 문단 일반 글 없음: {text}'
    rpr = r._r.find(qn('a:rPr'))
    for f in rpr.findall(qn('a:solidFill')):
        rpr.remove(f)
    src = plain[0]._r.find(qn('a:rPr')).find(qn('a:solidFill'))
    if src is not None:
        ln = rpr.find(qn('a:ln'))
        rpr.insert(0 if ln is None else list(rpr).index(ln) + 1, copy.deepcopy(src))
    log.append(f'빨강 → 일반: {text}')


def split(slide, text, parts):
    p, r = one(slide, text)
    r0 = r._r
    parent = r0.getparent()
    idx = parent.index(r0)
    for k, (t, kind) in enumerate(parts):
        rr = copy.deepcopy(r0)
        rpr = rr.find(qn('a:rPr'))
        for att in ('i', 'baseline'):
            rpr.attrib.pop(att, None)
        if kind == 'sub':
            rpr.set('baseline', '-25000')
        elif kind == 'ital':
            rpr.set('i', '1')
        elif kind == 'red':
            for f in rpr.findall(qn('a:solidFill')):
                rpr.remove(f)
            fill = rpr.makeelement(qn('a:solidFill'), {})
            fill.append(fill.makeelement(qn('a:srgbClr'), {'val': 'FF5050'}))
            ln = rpr.find(qn('a:ln'))
            rpr.insert(0 if ln is None else list(rpr).index(ln) + 1, fill)
        rr.find(qn('a:t')).text = t
        parent.insert(idx + k, rr)
    parent.remove(r0)
    log.append(f'나눔: {text[:30]}… → {[t for t, _ in parts]}')


def replace(slide, old, new):
    p, r = one(slide, old)
    r.text = new
    log.append(f'글: {old[:34]}… → {new[:34]}…')


def notes_replace(slide, old, new):
    hits = [r for p in slide.notes_slide.notes_text_frame.paragraphs for r in p.runs if old in r.text]
    if len(hits) != 1:
        raise SystemExit(f'노트 대상 {len(hits)} 개: {old}')
    hits[0].text = hits[0].text.replace(old, new)
    log.append(f'노트: {old} → {new}')


def notes_append(slide, sentence):
    ps = [p for p in slide.notes_slide.notes_text_frame.paragraphs if p.runs]
    r = ps[0].runs[-1]
    assert sentence not in r.text
    r.text = r.text.rstrip() + ' ' + sentence
    log.append(f'노트 +: {sentence[:40]}…')


# 3장 — 캡션 (한정어 '50kg 계획 예시' · '2D 모식' 은 둠: 초안 3 하지 않을 말 "왼쪽 3D 그림 = 이번 침대" · "오른쪽 = 우리 계산 결과")
replace(S[3], '【 DEM 해석 절차 (왼쪽, 50kg 계획 예시) 및 입자 접촉 모델 (오른쪽, 2D 모식) 】',
        '【 DEM 해석 절차 (50kg 계획 예시) 및 입자 접촉 모델 (2D 모식) 】')
# 4장
replace(S[4], '동일 조건 (300 MPa 가압 후 판 고정 이완)에서 전해질 입도별 구조 비교',
        '같은 절차 (300 MPa 가압 후 판 고정 이완)로 만든 전해질 입도별 구조 비교')
to_plain(S[4], '기공도 감소')
replace(S[4], '【 전해질 입도별 복합양극 미세구조 (왼쪽) 및 기공도 (오른쪽) 】', '【 전해질 입도별 복합양극 미세구조 및 기공도 】')
notes_replace(S[4], '같은 300 MPa로 눌렀을 때 기공도는', '같은 절차로 300 MPa까지 누른 뒤 기공도는')
# 5장
to_plain(S[5], '활물질/전해질 접촉 약 10배 증가')
replace(S[5], '【 전해질 입도별 활물질 1개당 전해질 접촉 수 (왼쪽) 및 활물질 표면 피복률 (오른쪽) 】',
        '【 전해질 입도별 활물질 1개당 전해질 접촉 수 및 활물질 표면 피복률 】')
# 6장
split(S[6], '전해질 물성 동일 가정 하 정규화 유효 이온전도도 (전극 ÷ 전해질 이온전도도) 분석',
      [('전해질 물성 동일 가정 하 정규화 유효 이온전도도 (', None), ('σ', 'ital'), ('eff', 'sub'), ('/', None),
       ('σ', 'ital'), ('0', 'sub'), (') 분석', None)])
to_plain(S[6], '정규화 유효 이온전도도 1.7배 (2 µm), 2.4배 (1 µm)')
to_plain(S[6], 'tortuosity 감소')
replace(S[6], '【 전해질 입도별 정규화 유효 이온전도도 (왼쪽, 3 µm 대비) 및 tortuosity (오른쪽) 】',
        '【 전해질 입도별 정규화 유효 이온전도도 (3 µm 대비) 및 tortuosity 】')
notes_append(S[6], '같은 계산에서 이온 전달 저항의 71–74 %는 전해질끼리 맞닿은 접촉부에서 생깁니다.')
# 7장
replace(S[7], '【 입도별 전해질 펠릿 이온전도도 (왼쪽, 3차년도) 및 3 µm 전극과 같아지는 전해질 이온전도도 (오른쪽, ◆ 실측) 】',
        '【 입도별 전해질 펠릿 이온전도도 (3차년도) 및 3 µm 전극과 같아지는 전해질 이온전도도 (◆ 실측) 】')
# 8장 — 1장과 같은 문장 = 같은 강조
split(S[8], '미립 전해질 이온전도도 감소 (0.45배)와 상쇄되어 1 µm 전극은 손익분기 근처',
      [('미립 전해질 이온전도도 감소 (0.45배)와 상쇄', 'red'), ('되어 1 µm 전극은 손익분기 근처', None)])

# 4장 그림 자리 → 세 칸 + 라벨 (1장 그림 · 라벨 배치와 같은 간격)
s4, s1 = S[4], S[1]
slots = [sh for sh in s4.shapes if sh.name == '3D 그림 자리 (웹앱)']
assert len(slots) == 1
slot = slots[0]
X, Y, W, H = slot.left, slot.top, slot.width, slot.height
gap, lab_h = int(0.10 * IN), int(0.27 * IN)
cw, ch = (W - 2 * gap) // 3, H - lab_h - int(0.02 * IN)
tree = slot._element.getparent()
idx = tree.index(slot._element)
nid = max(int(e.get('id')) for e in tree.iter(qn('p:cNvPr'))) + 1
lab_proto = [sh for sh in s1.shapes if sh.name == '3D 라벨 3 µm']
assert len(lab_proto) == 1
for k, size in enumerate(('3 µm', '2 µm', '1 µm')):
    el = copy.deepcopy(slot._element)
    nv = el.find('.//' + qn('p:cNvPr'))
    nv.set('id', str(nid)); nv.set('name', f'3D 그림 자리 (웹앱) {size}'); nid += 1
    el.find('.//' + qn('a:off')).set('x', str(X + k * (cw + gap)))
    el.find('.//' + qn('a:off')).set('y', str(Y))
    el.find('.//' + qn('a:ext')).set('cx', str(cw))
    el.find('.//' + qn('a:ext')).set('cy', str(ch))
    ts = el.findall('.//' + qn('a:t'))
    assert len(ts) == 2
    ts[0].text, ts[1].text = '3D 그림 (웹앱)', '기공 (빈 공간) 보기'
    tree.insert(idx + 1 + 2 * k, el)
    lab = copy.deepcopy(lab_proto[0]._element)
    nv = lab.find('.//' + qn('p:cNvPr'))
    nv.set('id', str(nid)); nv.set('name', f'3D 라벨 {size}'); nid += 1
    lab.find('.//' + qn('a:off')).set('x', str(X + k * (cw + gap)))
    lab.find('.//' + qn('a:off')).set('y', str(Y + ch + int(0.02 * IN)))
    lab.find('.//' + qn('a:ext')).set('cx', str(cw))
    lab.find('.//' + qn('a:ext')).set('cy', str(lab_h))
    t = lab.findall('.//' + qn('a:t'))
    assert len(t) == 1
    t[0].text = size
    tree.insert(idx + 2 + 2 * k, lab)
tree.remove(slot._element)
log.append(f'4장 그림 자리 → 세 칸 {cw / IN:.2f} × {ch / IN:.2f} in + 라벨')

prs.save(DST)
print('\n'.join(log))
