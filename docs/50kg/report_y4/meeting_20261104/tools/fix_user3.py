"""1저자 11-02 최신 덱 (그림 붙인 판) 위에 사전 공격 A 묶음 적용 — 1저자 "여기에서 계속 진행해주고".
  · 1저자가 직접 고친 것 (µ · mS cm⁻¹ · 2장 그림 · 불릿 1 · 2 · 3장 그림 위치) 은 손대지 않는다.
  · 2장 = 1저자 최종 (11-02 화면 "2page는 이게 최종이야") — 올린 판과 다른 곳은 캡션의 '펠릿' → 'pellet' 하나뿐이라 그것만 고친다.
  · 보류 표지 · 실행 이력 같은 주의 문구는 넣지 않는다 (1저자 11-02 — 요청서에만).
usage: python3 -I fix_user3.py in.pptx out.pptx
"""
import copy
import sys

from pptx import Presentation
from pptx.oxml.ns import qn

prs = Presentation(sys.argv[1])
S = prs.slides
log = []


def runs(n, shape='Rectangle 23'):
    return [r for sh in S[n - 1].shapes if sh.name == shape and sh.has_text_frame for p in sh.text_frame.paragraphs for r in p.runs]


def set_run(n, old, new, sub=False, shape='Rectangle 23'):
    hit = [r for r in runs(n, shape) if (old in r.text if sub else r.text == old)]
    if len(hit) != 1:
        raise SystemExit(f'{n}장 대상 run {len(hit)} 개: {old!r}')
    hit[0].text = hit[0].text.replace(old, new) if sub else new
    log.append(f'{n}장: {old[:28]!r} → {new[:28]!r}')


def notes(n, old, new):
    hit = [r for p in S[n - 1].notes_slide.notes_text_frame.paragraphs for r in p.runs if old in r.text]
    if len(hit) != 1:
        raise SystemExit(f'{n}장 노트 대상 {len(hit)}: {old!r}')
    hit[0].text = hit[0].text.replace(old, new)
    log.append(f'{n}장 노트: {old[:24]!r} → {new[:24]!r}')


def notes_append(n, sentence):
    ps = [p for p in S[n - 1].notes_slide.notes_text_frame.paragraphs if p.runs]
    r = ps[0].runs[-1]
    r.text = r.text.rstrip() + ' ' + sentence
    log.append(f'{n}장 노트 +: {sentence[:30]!r}')


def italic_sub_d50(n):
    """'D50' → D (이탤릭) + 50 (아래첨자) — 그 run 을 셋으로 나눈다."""
    hit = [r for r in runs(n) if 'D50' in r.text]
    if len(hit) != 1:
        raise SystemExit(f'{n}장 D50 run {len(hit)}')
    r0 = hit[0]._r
    pre, post = hit[0].text.split('D50', 1)
    parent, idx = r0.getparent(), r0.getparent().index(r0)
    for k, (t, kind) in enumerate([(pre, None), ('D', 'i'), ('50', 'sub'), (post, None)]):
        rr = copy.deepcopy(r0)
        rpr = rr.find(qn('a:rPr'))
        rpr.attrib.pop('i', None); rpr.attrib.pop('baseline', None)
        if kind == 'i':
            rpr.set('i', '1')
        if kind == 'sub':
            rpr.set('baseline', '-25000')
        rr.find(qn('a:t')).text = t
        parent.insert(idx + k, rr)
    parent.remove(r0)
    log.append(f'{n}장: D50 → D(이탤릭) 50(아래첨자)')


# 1장
set_run(1, '접촉 약 10배', '접촉 수 약 10배', sub=True)
italic_sub_d50(1)
# 2장 = 1저자 최종 (11-02 화면) — 결론 줄 ('→ 구조 이득과 이온전도도 감소의 상대 크기 확인 필요 → DEM 해석') 은
#       올린 판 그대로 둔다 (이전 판의 '(DEM)' · '(실측)의 상대 크기 비교' 고침은 뺌).  캡션 한 낱말만 화면대로.
set_run(2, '펠릿 이온전도도', 'pellet 이온전도도', sub=True, shape='Text Box 36')
# 3장
italic_sub_d50(3)
# 4장 — 원인 단정 빼기
set_run(4, '미립 전해질의 충진 효과', '전해질 미립화')
set_run(4, '로 기공도 감소 (22.4 → 19.6 → 18.1 %)', '에 따라 기공도 감소 (22.4 → 19.6 → 18.1 %)')
notes(4, '작은 전해질이 활물질 사이 틈을 채운 결과이고', '작은 전해질이 활물질 사이 틈을 채우는 방향과 맞고')
# 5장
set_run(5, '에 따른 활물질/전해질 접촉 약 10배 증가 (10 → 24 → 100개)', '에 따른 활물질/전해질 접촉 수 약 10배 증가 (10 → 24 → 100개)')
set_run(5, '   → 활물질 표면 피복률은 유사 (47–54 %) → ', '   → 활물질 표면 피복률은 증가하지 않음 (52.6 → 54.2 → 46.8 %) → ')
notes(5, '활물질 표면 피복률은 47–54 %로 비슷해, 같은 표면을', '활물질 표면 피복률은 52.6, 54.2, 46.8 %로 늘지 않아, 비슷한 표면을')
# 6장 노트 — tortuosity 정의 (발표자 답변용)
notes_append(6, 'tortuosity는 전해질 부피 분율을 정규화 유효 이온전도도로 나눈 값이고, 경로 길이의 비가 아닙니다.')
# 7장
set_run(7, '1 µm 전극 우위 조건: 미립 전해질 ≥ 2.1 mS/cm (3 µm의 0.42배)', '1 µm 전극이 3 µm와 같아지는 조건: 미립 전해질 2.1 mS/cm (3 µm의 0.42배) ↔ 실측 2.3')
notes(7, '1 µm 전극이 앞서려면 미립 전해질 이온전도도가 3 µm 전해질의 0.42배 (2.1 mS/cm) 이상이어야 합니다.',
      '1 µm 전극이 3 µm 전극과 같아지려면 미립 전해질 이온전도도가 3 µm 전해질의 0.42배 (2.1 mS/cm)여야 하고, 실측 2.3은 그보다 조금 높습니다. 펠릿 값에는 입계와 입자 접촉 저항이 들어 있어, 정규화 유효 이온전도도와 곱한 1.1배는 조건부 추정입니다.')
notes(7, '※ 이 덱 8쪽 새 측정 (small/large) 으로 보면', '※ 진도점검 회의 자료 8쪽의 새 펠릿 측정 (small/large) 으로 보면')
# 8장
set_run(8, '결론: 전해질 미립화에 따른 구조 개선 (기공도 감소, 접촉 약 10배, 정규화 유효 이온전도도 2.4배) 확인',
        '결론: 전해질 미립화에 따른 구조 개선 (기공도 감소, 접촉 수 약 10배, 정규화 유효 이온전도도 2.4배) 관측')
set_run(8, '이온 전달 저항의 약 3/4이 전해질–전해질 접촉부에 집중', '이온 전달 저항의 71–74 %가 전해질–전해질 접촉부에 집중')
notes(8, '전극 구조를 분명히 좋게 만들지만', '전극 구조를 좋게 만들지만')
notes(8, '이온 전달 저항의 약 4분의 3이', '이온 전달 저항의 71–74 %가')
prs.save(sys.argv[2])
print('\n'.join(log))
