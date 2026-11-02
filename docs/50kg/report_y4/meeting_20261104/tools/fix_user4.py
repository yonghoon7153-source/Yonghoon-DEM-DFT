"""1저자 11-02 수정본 (u6 · 3장 불릿을 직접 고친 판) 위의 단위 오타 하나 — '300 Mpa' → '300 MPa'.
  · 1저자가 다시 친 불릿 ('LIGGGHTS 해석: … → 입자 간 접촉력 (hysteretic spring, 마찰)으로 복합양극 구조 구현') · 패널 ② 위치는 그대로 둔다.
  · 'M' · 'p' · 'a' 가 따로 된 세 run 중 가운데 'p' 만 'P' 로 (서식 그대로).
usage: python3 -I fix_user4.py in.pptx out.pptx
"""
import sys

from pptx import Presentation

prs = Presentation(sys.argv[1])
s = prs.slides[2]
hits = []
for sh in s.shapes:
    if sh.name != 'Rectangle 23' or not sh.has_text_frame:
        continue
    for p in sh.text_frame.paragraphs:
        rs = p.runs
        for i in range(1, len(rs) - 2):
            if rs[i - 1].text.endswith('300 ') and [rs[i].text, rs[i + 1].text, rs[i + 2].text] == ['M', 'p', 'a']:
                hits.append(rs[i + 1])
if len(hits) != 1:
    raise SystemExit(f'3장 "300 Mpa" run 묶음 {len(hits)} 개 (1 이어야 한다)')
hits[0].text = 'P'
prs.save(sys.argv[2])
print("3장: '300 Mpa' → '300 MPa'")
