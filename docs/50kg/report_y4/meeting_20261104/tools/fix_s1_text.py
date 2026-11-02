"""진도점검 덱 1장 글 고침 (1저자 11-02):
  ① '정규화 유효 이온전도도' 정의를 괄호로 · ② 빨간색 남발 금지 → 이 줄의 빨강 (FF5050) 을 파랑 (0070C0) 으로
  ③ 캡션에서 '(왼쪽)' · '(오른쪽)' 빼기
usage: python3 -I fix_s1_text.py in.pptx out.pptx
고칠 글이 정확히 한 번 있어야 한다 (없거나 둘 이상이면 멈춘다).
"""
import sys

from pptx import Presentation

OLD_RUN = '기공도 감소, 접촉 약 10배, 정규화 유효 이온전도도 2.4배'
NEW_RUN = '기공도 감소, 접촉 약 10배, 정규화 유효 이온전도도 (전극 ÷ 전해질 이온전도도, 전해질 물성 동일 가정) 2.4배'
OLD_CAP = '전해질 입도별 복합양극 미세구조 (왼쪽) 및 주요 해석 결과 (오른쪽)'
NEW_CAP = '전해질 입도별 복합양극 미세구조 및 주요 해석 결과'


def runs_with(slide, text):
    out = []
    for sh in slide.shapes:
        if sh.has_text_frame:
            for par in sh.text_frame.paragraphs:
                out += [r for r in par.runs if text in r.text]
    return out


def main():
    prs = Presentation(sys.argv[1])
    s = prs.slides[0]
    hit = runs_with(s, OLD_RUN)
    if len(hit) != 1:
        raise SystemExit(f'① 대상 run {len(hit)} 개')
    r = hit[0]
    r.text = r.text.replace(OLD_RUN, NEW_RUN)
    clr = r._r.xpath('./a:rPr//a:srgbClr')
    if not clr or clr[0].get('val') != 'FF5050':
        raise SystemExit('② 빨강 run 아님')
    clr[0].set('val', '0070C0')
    cap = runs_with(s, OLD_CAP)
    if len(cap) != 1:
        raise SystemExit(f'③ 캡션 run {len(cap)} 개')
    cap[0].text = cap[0].text.replace(OLD_CAP, NEW_CAP)
    red_left = [x.text for sh in s.shapes if sh.has_text_frame for p in sh.text_frame.paragraphs for x in p.runs
                if 'FF5050' in x._r.xml]
    print('1장 남은 빨강 run:', red_left)
    prs.save(sys.argv[2])


if __name__ == '__main__':
    main()
