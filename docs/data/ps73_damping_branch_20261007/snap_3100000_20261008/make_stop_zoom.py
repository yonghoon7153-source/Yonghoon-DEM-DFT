"""판 압력 — 300 MPa 도달 (판 정지) 전후 확대 그림.  값 = ps73 압축 곡선 그대로 (docs/data/ps73_compaction_curve_20261006/curve/pressure.csv ·
열 step, phase, segment, pressure_mpa · 계산 없음).  시간 = step × 1e-6 s (그 곡선 폴더와 같은 환산).
주석 숫자 (300.95 · 204.6 · 165.3 MPa) = 같은 CSV 의 3,125,000 · 3,126,000 행과 이완 끝값 (README 표) — 손으로 적은 값이라 CSV 를 바꾸면 같이 본다.
다시 만들기: python3 make_stop_zoom.py <pressure.csv> <출력 폴더>"""
import csv
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

src, out = sys.argv[1], sys.argv[2]
rows = [r for r in csv.reader(open(src, encoding='utf-8'))][1:]
t, p = [], []
for r in rows:
    try:
        s = int(r[0]); v = float(r[3])
    except (ValueError, IndexError):
        continue
    if 3_095_000 <= s <= 3_225_000:
        t.append(s * 1e-6); p.append(v)
plt.rcParams.update({'font.family': 'Liberation Sans', 'font.size': 9, 'axes.linewidth': 1.0, 'xtick.direction': 'in', 'ytick.direction': 'in',
                     'xtick.top': True, 'ytick.right': True})
fig, ax = plt.subplots(figsize=(5.2, 3.0), dpi=220)
ax.plot(t, p, '-', color='#000000', lw=1.1)
ax.axvline(3.125, ls=':', color='#e00000', lw=1.0)
ax.annotate('300 MPa reached\n(plate stops, damping 0.5 → 1e-5)', (3.125, 300.95), xytext=(3.137, 285), fontsize=7, color='#e00000',
            arrowprops=dict(arrowstyle='->', color='#e00000', lw=0.8))
ax.annotate('1,000 steps later: 205 MPa', (3.126, 204.6), xytext=(3.140, 235), fontsize=7, color='#404040',
            arrowprops=dict(arrowstyle='->', color='#404040', lw=0.8))
ax.axhline(165.3, ls='--', color='#7f7f7f', lw=0.9)
ax.text(3.224, 168, 'relaxed: 165 MPa', ha='right', va='bottom', fontsize=7, color='#404040')
ax.set_xlim(3.095, 3.225); ax.set_ylim(0, 330)
ax.set_xlabel('Simulation time (s)'); ax.set_ylabel('Plate pressure (MPa)')
fig.tight_layout(); fig.savefig(f'{out}/ps73_stop_zoom.png', dpi=220); fig.savefig(f'{out}/ps73_stop_zoom.svg')
print('ok', len(t))
