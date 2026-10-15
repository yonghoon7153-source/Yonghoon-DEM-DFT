"""Render check of a deck PDF (LibreOffice + Carlito) from word boxes (`pdftotext -bbox`, poppler) — read-only.

python3 -I render_check_v33.py <deck.pdf> <out.json>

R1 pages = 18
R2 no two word boxes overlap by more than 2 pt in both directions on any page (text colliding with text).  pdftotext
   boxes are font line boxes (ascent + descent), not ink, so smaller touches are listed separately as `touches` and
   do not fail (v3.2 baseline: one 0.7 pt touch on page 3 — the subscript of the copied "m_i g" label vs the caption
   line "Forces on particle i", force diagram unchanged since v3.2).  Pictures and the equation fallback images carry
   no words, so text-on-picture is checked by eye and by the generator's zone checks.
R3 every word inside the page
R4 page 3: the source-line words end above the title words (two-line source line, SEM32-01)
R5 page 15: flow boxes read left → right as insertion · stabilization · compression · servo · relaxation · unloading · platen removal
R6 changed wording present / old wording absent in the rendered text (pages 3 · 7 · 11 · 15)
"""
import json
import re
import subprocess
import sys
import tempfile
from html import unescape
from pathlib import Path

pdf, out = Path(sys.argv[1]), Path(sys.argv[2])
with tempfile.TemporaryDirectory() as d:
    html = Path(d, 'bbox.html')
    subprocess.run(['pdftotext', '-bbox', str(pdf), str(html)], check=True)
    src = html.read_text(encoding='utf-8')

pages = []
for pm in re.finditer(r'<page width="([\d.]+)" height="([\d.]+)">(.*?)</page>', src, flags=re.S):
    w, h, body = float(pm.group(1)), float(pm.group(2)), pm.group(3)
    words = [dict(x0=float(a), y0=float(b), x1=float(c), y1=float(e), t=unescape(t))
             for a, b, c, e, t in re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', body)]
    pages.append(dict(w=w, h=h, words=words))

res = dict(pdf=pdf.name, pages=len(pages), checks=[])


def add(name, ok, detail=''):
    res['checks'].append(dict(check=name, ok=bool(ok), detail=detail if not ok else ''))


add('R1 pages = 18', len(pages) == 18, str(len(pages)))
LIMIT = 2.0
overl, touch, outside = [], [], []
for i, pg in enumerate(pages, 1):
    ws = pg['words']
    for a in ws:
        if a['x0'] < -0.5 or a['y0'] < -0.5 or a['x1'] > pg['w'] + 0.5 or a['y1'] > pg['h'] + 0.5:
            outside.append((i, a['t']))
    for k in range(len(ws)):
        a = ws[k]
        for b in ws[k + 1:]:
            dx = min(a['x1'], b['x1']) - max(a['x0'], b['x0'])
            dy = min(a['y1'], b['y1']) - max(a['y0'], b['y0'])
            if dx > 0 and dy > 0:
                (overl if dx > LIMIT and dy > LIMIT else touch).append((i, a['t'], b['t'], round(dx, 1), round(dy, 1)))
add('R2 no word boxes overlapping by more than 2 pt (all pages)', not overl, str(overl[:20]))
res['touches_le_2pt'] = touch
add('R3 all words inside the page', not outside, str(outside[:20]))


def text_of(i):
    return ' '.join(w['t'] for w in pages[i - 1]['words']) if len(pages) >= i else ''


if len(pages) >= 15:
    p3 = pages[2]['words']
    src_w = [w for w in p3 if w['y0'] < 90 and w['x0'] > 150]                 # 위 띠 오른쪽 (줄 아래 · 제목 위) — 출처 줄
    title = [w for w in p3 if w['t'] in ('DEM', 'governing') and 90 <= w['y0'] < 140]
    ok = bool(src_w) and bool(title) and max(w['y1'] for w in src_w) < min(w['y0'] for w in title)
    add('R4 page 3: source line ends above the title', ok,
        f"source y1 {max((w['y1'] for w in src_w), default=None)} title y0 {min((w['y0'] for w in title), default=None)}")
    res['page3_source_words'] = ' '.join(w['t'] for w in sorted(src_w, key=lambda w: (round(w['y0']), w['x0'])))
    p15 = pages[14]['words']
    flow_y = [w['y0'] for w in p15 if w['t'] == 'insertion']
    row = sorted([w for w in p15 if flow_y and abs(w['y0'] - flow_y[0]) < 14], key=lambda w: w['x0'])
    seq = [w['t'] for w in row]
    order = ['insertion', 'stabilization', 'compression', 'servo', 'relaxation', 'unloading', 'platen']
    pos = [seq.index(x) if x in seq else -1 for x in order]
    add('R5 page 15: flow order … relaxation → unloading → platen removal', -1 not in pos and pos == sorted(pos), str(seq))
    res['page15_flow_row'] = seq

PRESENT = {3: ['representative equations based on', 'small-overlap approximation'], 7: ['(nominal stopping pressure; see Problem 4)'],
           11: ['combined follow-up protocol', 'model-internal diagnostic', 'registered prediction band'], 15: ['to be redone']}
ABSENT = ['implemented equations', 'until the open checks pass', 'Heckel analysis redone']
for i, ps in PRESENT.items():
    t = text_of(i)
    miss = [p for p in ps if p not in t]
    add(f'R6 page {i}: new wording rendered', not miss, str(miss))
allt = ' '.join(text_of(i) for i in range(1, len(pages) + 1))
add('R6 old wording absent from the rendered text', not [a for a in ABSENT if a in allt], str([a for a in ABSENT if a in allt]))
res['failed'] = sum(1 for c in res['checks'] if not c['ok'])
res['total'] = len(res['checks'])
out.write_text(json.dumps(res, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print(f"render checks: {res['total']} · failed {res['failed']}")
for c in res['checks']:
    if not c['ok']:
        print('  ✗', c['check'], c['detail'][:160])
