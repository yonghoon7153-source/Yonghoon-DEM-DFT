# Page-2 (1저자 Origin) chart boxes redrawn as PNG: same box size, same plot area, fonts ≈ 9 / 11 pt,
# same axis ranges as page 2 (thickness 115–135 · porosity 15–24), x label on both, open frame (11-03 standard).
import sys
from pathlib import Path
sys.path.insert(0, '/home/user/Yonghoon-DEM-DFT/docs/50kg/report_y4/tmpl_202611')
import build_tmpl_dem as m
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
m.mpl_setup()
plt.rcParams.update({'axes.linewidth': 0.8, 'xtick.major.width': 0.8, 'ytick.major.width': 0.8,
                     'ytick.minor.width': 0.6, 'xtick.major.size': 3.5, 'ytick.major.size': 3.5, 'ytick.minor.size': 2.0})
FT, FL = 9, 11
def chart(path, size, box, cats, vals, lo, hi, ticks, minor, ylabel, xlabel, ctop, cbot, cstub, stub, ylab_x, xlab_y):
    fw, fh = size; l, r, t, b = box; W, H = fw - l - r, fh - t - b; gap = 0.03
    fig = plt.figure(figsize=(fw, fh), dpi=300)
    axb = fig.add_axes([l / fw, b / fh, W / fw, stub / fh])
    axt = fig.add_axes([l / fw, (b + stub + gap) / fh, W / fw, (H - stub - gap) / fh])
    xs = np.arange(1, len(cats) + 1); bw = 0.6
    for x, v in zip(xs, vals):
        m._grad_bar(axt, x, bw, lo, v, cbot, ctop)
        axb.add_patch(Rectangle((x - bw / 2, 0), bw, 1, facecolor=cstub, lw=0, zorder=2))
    for ax in (axt, axb):
        ax.set_xlim(0.4, len(cats) + 0.6)
        ax.spines['right'].set_visible(False)
    axt.set_ylim(lo, hi); axb.set_ylim(0, 1)
    axt.spines['bottom'].set_visible(False); axt.spines['top'].set_visible(False); axb.spines['top'].set_visible(False)
    axt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    axt.set_yticks(ticks); axt.set_yticks(minor, minor=True)
    axt.tick_params(axis='y', which='both', right=False, labelsize=FT, pad=2)
    axb.set_yticks([0.0]); axb.set_yticklabels(['0'])
    axb.tick_params(axis='y', which='both', right=False, labelsize=FT, pad=2)
    axb.set_xticks(xs); axb.set_xticklabels(cats)
    axb.tick_params(axis='x', which='both', top=False, labelsize=FT, pad=2)
    y_lo, y_hi = (b + stub) / fh, (b + stub + gap) / fh; dx, dy = 0.04 / fw, 0.025 / fh
    for yy in (y_lo, y_hi):
        fig.add_artist(Line2D([l / fw - dx, l / fw + dx], [yy - dy, yy + dy], transform=fig.transFigure, color='black', lw=0.8))
    fig.text(ylab_x / fw, (b + H / 2) / fh, ylabel, rotation=90, ha='center', va='center', fontsize=FL)
    fig.text((l + W / 2) / fw, xlab_y / fh, xlabel, ha='center', va='center', fontsize=FL)
    fig.savefig(path, dpi=300, transparent=True); plt.close(fig)
TH_SIZE, TH_BOX = (2.290, 1.850), (0.49, 0.03, 0.09, 0.44)     # 2쪽 두께 Origin 칸 · 그림 영역 (스크린샷 120 px/in 판독)
PO_SIZE, PO_BOX = (2.160, 1.790), (0.37, 0.03, 0.08, 0.43)     # 2쪽 기공도 Origin 칸
for sec, tag in ((m.SIZE, 'DSE'), (m.MOD, 'ESE')):
    xl = m.xlabel_math(sec)
    chart(out / ('p2s_thickness_%s.png' % tag), TH_SIZE, TH_BOX, sec['cats'], sec['thickness'], 115, 135,
          [115, 120, 125, 130, 135], [117.5, 122.5, 127.5, 132.5], 'Thickness (µm)', xl,
          m.BLUE_TOP, m.BLUE_BOT, m.BLUE_STUB, 0.12, 0.10, 0.115)
    chart(out / ('p2s_porosity_%s.png' % tag), PO_SIZE, PO_BOX, sec['cats'], sec['porosity'], 15, 24,
          [16, 20, 24], [18, 22], 'Porosity (%)', xl, m.PINK_TOP, m.PINK_BOT, m.PINK_STUB, 0.07, 0.07, 0.13)
print(sorted(p.name for p in out.glob('p2s_*.png')))
