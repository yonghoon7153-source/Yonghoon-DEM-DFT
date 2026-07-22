#!/usr/bin/env python3
"""CYCLE-STEP4 retention 그림 — retention_transport(N) + assumed-form 밴드 + 외삽 음영.

입력: cycle_retention.py 산출 JSON (하나 이상; 시나리오별).  출력: <out>.svg+.png+.csv (랩 규약).
★정직 표기: 곡선 = R_int(N)-기원 몫만(전극 동결); 밴드 = R_int(N) assumed-form; 외삽 구간 음영
(사다리 측정범위 밖 = 신뢰 낮음, 고-R_int STEP4 필요).  논문용 영문 라벨(폰트 무관).

사용: python3 scripts/plot_cycle_retention.py --json ret_dbe.json --json ret_sbe.json --out cycle_retention_fig
"""
import argparse
import csv
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

COLORS = ['#d95f02', '#2c7fb8', '#1b9e77', '#7570b3']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', action='append', required=True, help='cycle_retention JSON (여러 번)')
    ap.add_argument('--out', default='cycle_retention_fig')
    ap.add_argument('--logx', action='store_true', help='N 로그축 (0은 0.5로 대체 표시)')
    a = ap.parse_args()
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    all_rows = []
    for i, jp in enumerate(a.json):
        d = json.load(open(jp))
        c = COLORS[i % len(COLORS)]
        rows = d['rows']
        N = np.array([r['cycle'] for r in rows], float)
        Nx = np.where(N < 1, 0.5, N) if a.logx else N
        ret = np.array([r['retention_transport_pct'] for r in rows])
        lo = np.array([r['retention_lo'] for r in rows])
        hi = np.array([r['retention_hi'] for r in rows])
        ext = np.array([r['extrapolated'] for r in rows])
        lab = f'{d["electrode"].upper()} (scen {d["scenario"]}, R_int {d["R0"]:.0f}→{d["Rc"]:.0f})'
        ax.fill_between(Nx, lo, hi, color=c, alpha=0.15)
        ax.plot(Nx, ret, '-', color=c, lw=2, label=lab)
        # 외삽 구간(사다리 밖) = 점선 오버레이 + 첫 외삽점 표식
        if ext.any():
            k = int(np.argmax(ext))                        # 첫 외삽 사이클
            ax.plot(Nx[k:], ret[k:], ':', color=c, lw=2.4)
            ax.axvspan(Nx[k], Nx[-1], color=c, alpha=0.04)
            ax.annotate(f'ladder max {max(d["ladder"], key=float) if False else d["ladder_range"][1]:.0f}Ω\n→ extrapolated',
                        (Nx[k], ret[k]), xytext=(6, -2), textcoords='offset points',
                        fontsize=6.5, color=c, va='top')
        for r in rows:
            all_rows.append(dict(scenario=d['scenario'], electrode=d['electrode'], **r))
    ax.axhline(100, ls='-', color='gray', lw=0.6, alpha=0.5)
    if a.logx:
        ax.set_xscale('log')
    ax.set_xlabel('Cycle N'); ax.set_ylabel('Transport-origin retention (%)  = delivered@R(N)/delivered@R(0)')
    ax.set_title('CYCLE-STEP4 — R_int(N)-origin retention share (solid=measured-range, dotted=extrapolated)',
                 fontsize=9.5)
    ax.grid(alpha=0.3); ax.legend(fontsize=8, loc='lower left')
    fig.text(0.5, 0.005, 'transport(R_int) share only; measured retention − this = electrode/chemistry '
             'degradation (A10). Band = R_int(N) assumed-form. R_int = user-lab Fig.6e pristine (approx.)',
             ha='center', fontsize=6.5, color='#555')
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    fig.savefig(a.out + '.svg'); fig.savefig(a.out + '.png', dpi=150)
    with open(a.out + '.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(all_rows[0].keys()))
        w.writeheader(); w.writerows(all_rows)
    print(f'saved {a.out}.svg / .png / .csv')


if __name__ == '__main__':
    main()
