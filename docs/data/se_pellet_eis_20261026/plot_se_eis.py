import csv, json, sys, os
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
D = sys.argv[1]
rd = json.load(open(os.path.join(D, 'readings.json')))
C = {'small': '#2a6fb0', 'big': '#c8553d'}
fig, ax = plt.subplots(1, 2, figsize=(10.5, 4.2), dpi=160)
for fn in sorted(rd):
    kind = 'small' if '_small_' in fn else 'big'; run = fn.split('_sym_')[1][:2]
    r = list(csv.DictReader(open(os.path.join(D, 'extracted', fn[:-4] + '.csv'))))
    f = np.array([float(x['freq_Hz']) for x in r]); re_ = np.array([float(x['ReZ_ohm']) for x in r]); nim = np.array([float(x['negImZ_ohm']) for x in r])
    ph = np.array([float(x['phase_deg']) for x in r]); ls = '-' if run == '01' else '--'
    R = rd[fn]['R_fit']['100Hz']['R_ohm']
    lab = f'SE {kind} #{run}  (R = {R:.1f} Ω)'
    ax[0].plot(re_, nim, ls, color=C[kind], lw=1.6, marker='o', ms=2.6, label=lab)
    ax[0].plot([R], [0], marker='|', ms=14, mew=2, color=C[kind])
    ax[1].semilogx(f, -ph, ls, color=C[kind], lw=1.6, label=f'SE {kind} #{run}')
ax[0].set_xlim(15, 75); ax[0].set_ylim(-30, 60); ax[0].set_aspect('equal'); ax[0].axhline(0, color='#888', lw=0.8)
ax[0].set_xlabel('Re(Z) / Ω'); ax[0].set_ylabel('−Im(Z) / Ω'); ax[0].set_title('Nyquist, high-frequency zoom (7 MHz →)', fontsize=10)
ax[0].grid(color='#ddd', lw=0.6); ax[0].legend(fontsize=7.5, frameon=False, loc='upper left', bbox_to_anchor=(1.02, 1.0))
ax[1].set_xlabel('Frequency / Hz'); ax[1].set_ylabel('−Phase / deg'); ax[1].set_ylim(-50, 90); ax[1].axhline(0, color='#888', lw=0.8)
ax[1].set_title('Phase (blocking tail: −phase → 90° = ideal)', fontsize=10); ax[1].grid(color='#ddd', lw=0.6); ax[1].legend(fontsize=7.5, frameon=False, loc='lower left')
for a in ax:
    for s in ('top', 'right'): a.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig(os.path.join(D, 'nyquist_hf_phase.png')); print('ok')
