import sys, re
from pptx import Presentation
p = Presentation(sys.argv[1]); hits = []
for i, s in enumerate(p.slides, 1):
    txt = [sh.text_frame.text for sh in s.shapes if sh.has_text_frame] + [c.text for sh in s.shapes if getattr(sh, 'has_table', False) and sh.has_table for r in sh.table.rows for c in r.cells] + [s.notes_slide.notes_text_frame.text]
    for t in txt:
        for m in re.finditer(r'(?i)hertz|physics|union|수송 tortuosity|이온 이동 경로|156|재확인|빗금', t):
            hits.append((i, m.group(0)))
print('hits', hits)
