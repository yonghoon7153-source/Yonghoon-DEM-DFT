"""진도점검 덱 2장 글 고침 (1저자 11-02 "2장 권고대로 진행하고"):
  불릿 1 '활물질 표면 접촉 증가' → '활물질–전해질 접촉 수 증가' (5장 = 접촉 수 10배 · 피복률 증가 없음)
  불릿 2 '전해질 이온전도도 감소 (3차년도 펠릿: …)' → '전해질 펠릿 이온전도도 감소 (3차년도: …)' (펠릿 값 = 입계 · 접촉 · 기공 섞인 값)
  결론 줄 '…의 상대 크기 확인 필요 → DEM 해석' → '구조 이득 (DEM)과 이온전도도 감소 (실측)의 상대 크기 비교' (DEM = 구조 쪽만)
  노트 '활물질 표면에 더 많이 닿고' → '활물질에 닿는 접촉이 많아지고' (불릿 1 과 맞춤)
usage: python3 -I fix_s2_text.py in.pptx out.pptx
"""
import sys

from pptx import Presentation

prs = Presentation(sys.argv[1])
s = prs.slides[1]
EDITS = [('미립 전해질: 활물질 표면 접촉 증가 및 충진에 따른 치밀화 기대', '미립 전해질: 활물질–전해질 접촉 수 증가 및 충진에 따른 치밀화 기대'),
         ('미립화 시 전해질 이온전도도 감소 (3차년도 펠릿: 5.1 → 2.3 mS/cm)', '미립화 시 전해질 펠릿 이온전도도 감소 (3차년도: 5.1 → 2.3 mS/cm)'),
         ('과 ', ' (DEM)과 '),
         ('의 상대 크기 확인 필요 → DEM 해석', ' (실측)의 상대 크기 비교')]
runs = [r for sh in s.shapes if sh.name == 'Rectangle 23' for p in sh.text_frame.paragraphs for r in p.runs]
for old, new in EDITS:
    hit = [r for r in runs if r.text == old]
    if len(hit) != 1:
        raise SystemExit(f'대상 run {len(hit)} 개: {old!r}')
    hit[0].text = new
nr = [r for p in s.notes_slide.notes_text_frame.paragraphs for r in p.runs if '활물질 표면에 더 많이 닿고' in r.text]
if len(nr) != 1:
    raise SystemExit(f'노트 대상 {len(nr)}')
nr[0].text = nr[0].text.replace('활물질 표면에 더 많이 닿고', '활물질에 닿는 접촉이 많아지고')
for sh in s.shapes:
    if sh.name == 'Rectangle 23':
        for p in sh.text_frame.paragraphs:
            print('  |', p.text)
print('  노트:', s.notes_slide.notes_text_frame.text)
prs.save(sys.argv[2])
