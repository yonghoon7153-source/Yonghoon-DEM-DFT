"""Read-only: dump vector drawings + text spans inside the chart regions of pages 14/15 (untrusted PDF; python3 -I)."""
import sys, os
import fitz
pdf, outdir = sys.argv[1], sys.argv[2]
doc = fitz.open(pdf)
REG = {  # page index -> {name: rect (pt)}
    13: {'tort': fitz.Rect(40, 365, 195, 525), 'cov': fitz.Rect(200, 365, 360, 525)},
    14: {'sion': fitz.Rect(565, 220, 735, 378), 'se': fitz.Rect(565, 378, 735, 525)},
}
def col(c):
    if c is None: return None
    return '#%02X%02X%02X' % tuple(int(round(v * 255)) for v in c)
for pno, regs in REG.items():
    page = doc[pno]
    dr = page.get_drawings()
    words = page.get_text('dict')
    for name, R in regs.items():
        print(f'===== page {pno+1} {name} {R}')
        pix = page.get_pixmap(dpi=600, clip=R)
        pix.save(os.path.join(outdir, f'crop_p{pno+1}_{name}_600dpi.png'))
        for d in dr:
            r = d['rect']
            if not R.intersects(r) or not (R.contains(r) or (r.width < 1 or r.height < 1) and R.intersects(r)):
                continue
            items = d['items']
            kinds = ''.join(it[0] for it in items)
            print(f"  {d.get('type')} fill={col(d.get('fill'))} stroke={col(d.get('color'))} w={d.get('width')} op_f={d.get('fill_opacity')} op_s={d.get('stroke_opacity')} "
                  f"rect=({r.x0:.2f},{r.y0:.2f},{r.x1:.2f},{r.y1:.2f}) items={kinds[:12]} dash={d.get('dashes')} cap={d.get('lineCap')}")
        for b in words['blocks']:
            for l in b.get('lines', []):
                for s in l['spans']:
                    sr = fitz.Rect(s['bbox'])
                    if R.intersects(sr):
                        print(f"  TEXT {s['text']!r} font={s['font']} size={s['size']:.2f} color=#{s['color']:06X} flags={s['flags']} bbox=({sr.x0:.1f},{sr.y0:.1f},{sr.x1:.1f},{sr.y1:.1f}) origin={tuple(round(v,1) for v in s['origin'])}")
