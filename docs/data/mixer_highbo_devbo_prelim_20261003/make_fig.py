"""dev-bo 2 바퀴 M(t) · S²(t) 그림 — 이 폴더의 판독 JSON 만 읽는다 (DEV 자료 · n = 1 seed · 판정 아님).

  python3 docs/data/mixer_highbo_devbo_prelim_20261003/make_fig.py   → webapp/static/mixer/devbo_Mt_v12.png
"""
import json, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
D = os.path.join(ROOT, 'docs', 'data', 'mixer_highbo_devbo_prelim_20261003')
OUT = os.path.join(ROOT, 'webapp', 'static', 'mixer', 'devbo_Mt_v12.png')
CELLS = [('16x4', '16×16×4'), ('12x3', '12×12×3'), ('8x2', '8×8×2')]
STY = {'LC_ref_r2': ('#1f77b4', 'LC_ref_r2 (comparison partner)'), 'LH_ref_r2': ('#ff7f0e', 'LH (Bo_code 38.4)'),
       'LHx10_ref_r2': ('#2ca02c', 'LHx10 (Bo_code 384)'), 'LHx30_ref_r2': ('#d62728', 'LHx30 (Bo_code 1152)')}
fig, ax = plt.subplots(2, 3, figsize=(13, 7.2), sharex=True)
for j, (c, lab) in enumerate(CELLS):
    runs = json.load(open(os.path.join(D, f'devbo_c{c}.json')))
    for r in runs:
        n = os.path.basename(r['run']).replace('_s32452843', '')
        col, name = STY[n]
        rev = [w['rev'] for w in r['rows']]
        ax[0, j].plot(rev, [w['M'] for w in r['rows']], color=col, lw=1.0, label=name)
        ax[1, j].plot(rev, [w['s2'] for w in r['rows']], color=col, lw=1.0)
        ax[1, j].plot([0], [r['S0']], 'o', color=col, ms=4)
    ax[1, j].axhline(runs[0]['SR'], color='k', ls='--', lw=0.9, label='S_R² (E0 uniform ref)')
    for a in (ax[0, j], ax[1, j]):
        a.axvspan(1.0, 2.0, color='0.92', zorder=0)
    ax[0, j].axhline(0, color='0.4', lw=0.6); ax[0, j].axhline(1, color='0.4', lw=0.6, ls=':')
    ax[0, j].set_title(f'cells {lab} (n_min 20 · axis x)', fontsize=10)
    ax[1, j].set_xlabel('revolutions (shaded = registered bin 1)')
ax[0, 0].set_ylabel('Lacey M = (S0² − S²)/(S0² − S_R²)')
ax[1, 0].set_ylabel('cell variance S²  (dot = run\'s own t0 S0²)')
ax[0, 0].legend(fontsize=8, loc='lower right'); ax[1, 0].legend(fontsize=8, loc='upper right')
fig.suptitle('Mixer high-Bo stiffness axis · DEV seed 1 · dev-bo (2 turns) — DEV data, n = 1 seed, no pass line, NOT a verdict\n'
             'joint intervention B (AM–AM + AM–wall cohesion) · levels chosen after the dev-rot M was opened (post-hoc)', fontsize=10)
fig.tight_layout(rect=(0, 0, 1, 0.93))
fig.savefig(OUT, dpi=110)
print(OUT, os.path.getsize(OUT))
