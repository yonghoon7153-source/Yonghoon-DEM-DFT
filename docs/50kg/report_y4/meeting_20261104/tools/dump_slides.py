"""read-only: 장마다 도형 · 글 (색 · 이탤릭 · 첨자 표지) · 표 · 그림 (파트 · 픽셀) · 노트."""
import sys
from pptx import Presentation
from pptx.oxml.ns import qn
IN = 914400
prs = Presentation(sys.argv[1])
want = [int(x) for x in sys.argv[2].split(',')]
def tag(r):
    rpr = r._r.find(qn('a:rPr'))
    t = []
    if rpr is None:
        return ''
    c = rpr.find(qn('a:solidFill') + '/' + qn('a:srgbClr'))
    if c is not None and c.get('val') not in ('262626', '000000', '7F7F7F'):
        t.append(c.get('val'))
    if rpr.get('i') == '1': t.append('ital')
    if rpr.get('b') == '1': t.append('b')
    if rpr.get('baseline'): t.append('base' + rpr.get('baseline'))
    return f'[{",".join(t)}]' if t else ''
for n in want:
    s = prs.slides[n - 1]
    print(f'################ slide {n}')
    for sh in s.shapes:
        g = f'x={sh.left/IN:.2f} y={sh.top/IN:.2f} w={sh.width/IN:.2f} h={sh.height/IN:.2f}'
        if sh.shape_type == 13:
            print(f'## PIC {sh.name!r} {g} {s.part.related_part(sh._element.blipFill.blip.rEmbed).partname} px={sh.image.size}')
            continue
        print(f'## {sh.name!r} {g}')
        if sh.has_text_frame:
            for p in sh.text_frame.paragraphs:
                if p.runs:
                    print('   |', ''.join(r.text + tag(r) for r in p.runs))
        if getattr(sh, 'has_table', False) and sh.has_table:
            for row in sh.table.rows:
                print('   T', [c.text for c in row.cells])
    print('## NOTES:')
    for p in s.notes_slide.notes_text_frame.paragraphs:
        if p.text.strip():
            print('   ', p.text)
