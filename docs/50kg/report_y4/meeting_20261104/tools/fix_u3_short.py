"""5장 · 7장 긴 줄 줄이기 (렌더에서 두 줄로 넘어가 그림에 닿음) — 뜻 · 숫자 그대로.
usage: python3 -I fix_u3_short.py in.pptx out.pptx
"""
import sys
from pptx import Presentation
prs = Presentation(sys.argv[1])
E = [(5, '   → 활물질 표면 피복률은 증가하지 않음 (52.6 → 54.2 → 46.8 %) → ', '   → 피복률은 증가하지 않음 (52.6 → 54.2 → 46.8 %) → '),
     (5, '같은 표면을 다수의 작은 접촉으로 분할', '작은 접촉 여럿으로 분할'),
     (7, '1 µm 전극이 3 µm와 같아지는 조건: 미립 전해질 2.1 mS/cm (3 µm의 0.42배) ↔ 실측 2.3', '1 µm 전극이 3 µm와 같아지는 조건: 전해질 2.1 mS/cm (0.42배) ↔ 실측 2.3')]
for n, old, new in E:
    hit = [r for sh in prs.slides[n - 1].shapes if sh.name == 'Rectangle 23' for p in sh.text_frame.paragraphs for r in p.runs if r.text == old]
    if len(hit) != 1:
        raise SystemExit(f'{n}장 대상 {len(hit)}: {old!r}')
    hit[0].text = new
    print(f'{n}장: {new.strip()}')
prs.save(sys.argv[2])
