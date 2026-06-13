#!/usr/bin/env python3
"""Plot the 3D elasto-plastic DEM Furnas-dip sweep: porosity vs AM wt%, cap ON
(plastic) vs cap OFF (rigid), at the real 12:4:1 sizes, beta=0.40, E_AM=140,
measured by the bulk axial virial.  Reads docs/data/dem3d_dip_sweep.csv.

The verdict figure for "does real plasticity (with the contact-network jamming
the MPM lacks) erase the Furnas dip?"
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

ams = sorted(d['plastic'])
pl = [d['plastic'][a] for a in ams]
rg = [d['rigid'][a] for a in ams]
amin_pl = ams[pl.index(min(pl))]
amin_rg = ams[rg.index(min(rg))]

fig, ax = plt.subplots(figsize=(6.6, 4.8))
ax.plot(ams, rg, '-o', color='#5b6b7a', lw=2, ms=7, label='RIGID  (cap OFF, pure Hertz)')
ax.plot(ams, pl, '-o', color='#c0392b', lw=2.4, ms=8, label='PLASTIC  (cap ON, Thornton+lock)')
# shade the densification the plasticity adds
ax.fill_between(ams, pl, rg, color='#c0392b', alpha=0.10)
# mark the dips
ax.annotate(f'plastic dip\nAM{amin_pl}  {min(pl):.1f}%', xy=(amin_pl, min(pl)),
            xytext=(amin_pl - 13, min(pl) - 3.2), fontsize=9, color='#c0392b',
            arrowprops=dict(arrowstyle='->', color='#c0392b'))
ax.scatter([amin_pl], [min(pl)], s=140, facecolors='none', edgecolors='#c0392b', lw=2, zorder=5)

ax.set_xlabel('AM content (wt %)')
ax.set_ylabel('porosity  ε_sphere  (%)')
ax.set_title('3D elasto-plastic DEM — Furnas dip survives plasticity\n'
             '12:4:1, 300 MPa, bulk virial, real E (no softening)', fontsize=10.5)
ax.grid(alpha=0.3)
ax.legend(fontsize=9, loc='upper center')
ax.set_xticks(ams)
plt.tight_layout()
out = os.path.join(HERE, '..', 'docs', 'figures', 'dem3d_dip_sweep.png')
plt.savefig(out, dpi=130)
print(f"saved {out}")
print(f"plastic dip @ AM{amin_pl} ({min(pl):.1f}%), depth ~"
      f"{0.5 * (pl[0] + pl[-1]) - min(pl):.1f}%p;  rigid min @ AM{amin_rg} ({min(rg):.1f}%)")
print(f"plastic below rigid by {min(r - p for p, r in zip(pl, rg)):.1f}–"
      f"{max(r - p for p, r in zip(pl, rg)):.1f} %p (plasticity densifies)")
