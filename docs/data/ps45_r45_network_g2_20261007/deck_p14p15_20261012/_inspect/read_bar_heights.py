"""Read-only: recover the plotted bar values of the four small deck charts (p14 Tortuosity / Coverage,
p15 sigma_Li+ / sigma_e-) from the PDF vector paths: y major-tick lines + their numeric labels give the
axis map, bar tops give the values.  Untrusted PDF -> run with python3 -I.  Prints JSON."""
import json
import sys
import fitz

pdf = sys.argv[1]
doc = fitz.open(pdf)
REG = {'p14_tortuosity': (13, (40, 365, 200, 525)), 'p14_coverage': (13, (200, 365, 362, 525)),
       'p15_sigma_li': (14, (565, 220, 740, 368)), 'p15_sigma_e': (14, (565, 368, 740, 525))}
BAR_FILLS = ['#FDE724', '#B4DD2B', '#6BCD58', '#35B778', '#1E9C88']


def hexc(c):
    return None if c is None else '#' + ''.join('%02X' % int(round(v * 255)) for v in c)


out = {}
for name, (pno, (x0, y0, x1, y1)) in REG.items():
    page = doc[pno]
    inside = lambda r: not (r.x1 < x0 or r.x0 > x1 or r.y1 < y0 or r.y0 > y1)
    drs = [d for d in page.get_drawings() if inside(d['rect'])]
    bars = sorted([d['rect'] for d in drs if hexc(d.get('fill')) in BAR_FILLS], key=lambda r: r.x0)
    bar_cols = [hexc(d.get('fill')) for d in sorted([d for d in drs if hexc(d.get('fill')) in BAR_FILLS], key=lambda d: d['rect'].x0)]
    # y-axis = the long vertical stroke; major ticks = 2.0 pt horizontal strokes ending on it
    vert = [d for d in drs if d['type'] == 's' and len(d['items']) == 1 and d['items'][0][0] == 'l'
            and abs(d['items'][0][1].x - d['items'][0][2].x) < 1e-3 and abs(d['items'][0][1].y - d['items'][0][2].y) > 50]
    ax_x = min(v['items'][0][1].x for v in vert)
    ticks = sorted({round(d['items'][0][1].y, 2) for d in drs if d['type'] == 's' and len(d['items']) == 1 and d['items'][0][0] == 'l'
                    and abs(d['items'][0][1].y - d['items'][0][2].y) < 1e-3
                    and 1.8 < abs(d['items'][0][1].x - d['items'][0][2].x) < 2.3
                    and abs(max(d['items'][0][1].x, d['items'][0][2].x) - ax_x) < 0.05})
    labels = []
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            for s in l['spans']:
                bx = fitz.Rect(s['bbox'])
                if inside(bx) and bx.x1 < ax_x and ax_x - bx.x1 < 8:
                    try:
                        labels.append((float(s['text']), (bx.y0 + bx.y1) / 2))
                    except ValueError:
                        pass
    pairs = []
    for ty in ticks:
        v, cy = min(labels, key=lambda t: abs(t[1] - ty))
        if abs(cy - ty) < 4:
            pairs.append((ty, v))
    (ya, va), (yb, vb) = pairs[0], pairs[-1]
    slope = (vb - va) / (yb - ya)
    val = lambda y: va + (y - ya) * slope
    resid = max(abs(val(ty) - v) for ty, v in pairs)
    out[name] = {'page': pno + 1, 'y_axis_x_pt': round(ax_x, 2), 'major_ticks': [v for _, v in sorted(pairs, key=lambda p: -p[0])],
                 'tick_fit_max_resid': round(resid, 6), 'bar_fill': bar_cols,
                 'bar_values': [round(val(r.y0), 4) for r in bars], 'bar_base_values': [round(val(r.y1), 4) for r in bars],
                 'bar_width_pt': round(bars[0].width, 3), 'bar_pitch_pt': round(bars[1].x0 - bars[0].x0, 3)}
print(json.dumps(out, ensure_ascii=False, indent=1))
