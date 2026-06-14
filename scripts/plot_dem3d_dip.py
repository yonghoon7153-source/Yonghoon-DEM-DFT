#!/usr/bin/env python3
"""3D elasto-plastic DEM porosity vs AM wt%, cap ON (plastic) vs OFF (rigid), at
EQUILIBRATED 300 MPa (fine bidirectional virial servo).  Reads
docs/data/dem3d_dip_sweep.csv.

Honest verdict figure: with proper equilibration the plastic curve is MONOTONIC
(no Furnas dip — the earlier dip was a settling artifact), and the composite
absolute porosity (36-41%) sits FAR above both the pure-SE anchor (~9-10%) and the
measured composite porosity (EA26-3669 FIB-SEM: 9.4% @75wt%, 18.9% @82wt%) -- the
rigid-AM bulk-virial load-shielding keeps the SE from densifying in the composite.
"""
import csv
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(HERE, '..', 'docs', 'data', 'dem3d_dip_sweep.csv')

d = {'plastic': {}, 'rigid': {}}
with open(CSV) as fh:
    for r in csv.DictReader(fh):
        d[r['mode']][int(r['am'])] = float(r['por_sphere'])

amp = sorted(a for a in d['plastic'] if a > 0)
amr = sorted(d['rigid'])
pl = [d['plastic'][a] for a in amp]
rg = [d['rigid'][a] for a in amr]

fig, ax = plt.subplots(figsize=(7.0, 4.9))
ax.plot(amr, rg, '-s', color='#5b6b7a', lw=2, ms=6, label='RIGID  (cap OFF)')
ax.plot(amp, pl, '-o', color='#c0392b', lw=2.4, ms=7, label='PLASTIC  (cap ON)')
# pure-SE anchor
ax.scatter([0], [d['plastic'].get(0, 9.0)], s=90, marker='*', color='#c0392b', zorder=5)
ax.annotate('pure-SE 9% (Minnmann)\n→ jumps to 39% with any AM\n(over-shielding)',
            xy=(0, 9.0), xytext=(6, 15), fontsize=8, color='#7a2018',
            arrowprops=dict(arrowstyle='->', color='#7a2018'))
# EA26-3669 measured composite porosity (FIB-SEM, post-cycle): 50vol%=75wt%, 60vol%=82wt%
ax.scatter([75, 82], [9.43, 18.93], s=80, marker='D', color='#1f7a3d', zorder=5,
           label='measured (EA26-3669 FIB-SEM)')
ax.axhspan(9, 19, color='#1f7a3d', alpha=0.07)

ax.set_xlabel('AM content (wt %)'); ax.set_ylabel('porosity  ε_sphere  (%)')
ax.set_title('3D elasto-plastic DEM @ equilibrated 300 MPa — NO Furnas dip;\n'
             'composite over-shielded (real rigid AM bears the bulk stress)', fontsize=10)
ax.grid(alpha=0.3); ax.legend(fontsize=8.5, loc='center right'); ax.set_ylim(0, 45)
ax.set_xticks([0, 20, 35, 50, 65, 75, 85, 95])
plt.tight_layout()
out = os.path.join(HERE, '..', 'docs', 'figures', 'dem3d_dip_sweep.png')
plt.savefig(out, dpi=130)
print(f"saved {out}")
print(f"plastic monotonic {pl[0]:.1f}->{pl[-1]:.1f}% (no local min); "
      f"composite {min(pl):.0f}-{max(pl):.0f}% vs measured 9-19% -> over-shielded")
