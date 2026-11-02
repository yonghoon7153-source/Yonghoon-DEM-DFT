"""진도점검 덱 1장 글 고침 2 (1저자 11-02):
  ① 정의 괄호 = 기호 σ_eff/σ_0 — "한국어로만 하려고 하지말고 저 부분을 기호로 · eff/0"
     · σ = 이탤릭 (변수) · eff · 0 = 아래첨자 · 똑바로 — "italic 같은거 잘 지키고"
     · 그 구절 색 = 기본색 (1저자 저장본 그대로)
  ② '전해질 이온전도도 감소 (0.45배)와 상쇄' = 빨강 (FF5050) — "상쇄된건 안좋은거니까 빨간부분으로 하이라이트"
usage: python3 -I fix_s1_text2.py in.pptx out.pptx
대상 run 이 정확히 하나여야 한다 (아니면 멈춘다).
"""
import copy
import sys

from pptx import Presentation
from pptx.oxml.ns import qn

PRE1 = '기공도 감소, 접촉 약 10배, 정규화 유효 이온전도도 ('
SUF1 = ') 2.4배'
NEW1 = [(PRE1, None), ('σ', 'ital'), ('eff', 'sub'), ('/', None), ('σ', 'ital'), ('0', 'sub'), (SUF1, None)]
OLD2 = '   → 전해질 이온전도도 감소 (0.45배)와 상쇄 → '
NEW2 = [('   → ', None), ('전해질 이온전도도 감소 (0.45배)와 상쇄', 'red'), (' → ', None)]


def runs(slide):
    return [r for sh in slide.shapes if sh.has_text_frame for p in sh.text_frame.paragraphs for r in p.runs]


def one(hits, what):
    if len(hits) != 1:
        raise SystemExit(f'대상 run {len(hits)} 개: {what}')
    return hits[0]


def split_run(run, parts):
    r0 = run._r
    parent = r0.getparent()
    idx = parent.index(r0)
    for k, (text, kind) in enumerate(parts):
        r = copy.deepcopy(r0)
        rpr = r.find(qn('a:rPr'))
        for att in ('i', 'baseline'):
            if att in rpr.attrib:
                del rpr.attrib[att]
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
        r.find(qn('a:t')).text = text
        parent.insert(idx + k, r)
    parent.remove(r0)


def flags(r):
    rpr = r._r.find(qn('a:rPr'))
    out = []
    if rpr.get('i') == '1':
        out.append('ital')
    if rpr.get('baseline') == '-25000':
        out.append('sub')
    clr = rpr.find(qn('a:solidFill') + '/' + qn('a:srgbClr'))
    if clr is not None:
        out.append(clr.get('val'))
    return ','.join(out)


def main():
    prs = Presentation(sys.argv[1])
    s = prs.slides[0]
    r1 = one([r for r in runs(s) if r.text.startswith(PRE1) and r.text.endswith(SUF1)], PRE1)
    print('바꾸는 글:', repr(r1.text))
    split_run(r1, NEW1)
    split_run(one([r for r in runs(s) if r.text == OLD2], OLD2), NEW2)
    for sh in s.shapes:
        if sh.has_text_frame:
            for p in sh.text_frame.paragraphs:
                if '미립화' in p.text or '상쇄' in p.text:
                    print(' | '.join(f'{r.text!r}[{flags(r)}]' for r in p.runs))
    prs.save(sys.argv[2])


if __name__ == '__main__':
    main()
