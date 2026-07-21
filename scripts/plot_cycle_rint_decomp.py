#!/usr/bin/env python3
"""CYCLE-STEP3 R_int(N) 분해 그림 — 기계(접촉,모델) vs 화학(잔차,측정).

입력: cycle_rint_synthesis.py 산출 rint_decomp.json (primary=mono, secondary=bimodal).
출력: <out>.svg + <out>.png + <out>.csv (랩 규약 동시산출).  WSL에서 실행(matplotlib).

패널 A: 측정 R_int(N) 배율 + 모델 기계-몫 밴드(Holm↔CT) 겹침 (mono vs bimodal).
패널 B: N=100 기계 vs 화학 몫 분해 막대 (CT 대표 + 밴드 오차).
사용: python3 scripts/plot_cycle_rint_decomp.py --json rint_decomp.json --out rint_decomp_fig
"""
import argparse
import csv
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

C_MONO, C_BIM, C_MEAS = '#2c7fb8', '#d95f02', '#555555'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', default='rint_decomp.json')
    ap.add_argument('--out', default='rint_decomp_fig')
    a = ap.parse_args()
    d = json.load(open(a.json))
    res = d['results']
    meas = d['measured']
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.4))

    # ── Panel A: R_int(N) multiplier (measured total + model mechanical band) ──
    for tag, col, lab in (('primary', C_MONO, 'mono'), ('secondary', C_BIM, 'bimodal')):
        if tag not in res:
            continue
        rows = res[tag]['rows']
        N = [r['cycle'] for r in rows]
        holm = [r['rct_holm_rel'] for r in rows]
        ct = [r['rct_ct_rel'] for r in rows]
        ax[0].fill_between(N, ct, holm, color=col, alpha=0.20)
        ax[0].plot(N, ct, '-', color=col, lw=2, label=f'{lab} contact R ratio (CT-Holm band)')
    Nm = sorted(int(k) for k in meas['traj'])
    Rm = [meas['traj'][str(k)] if str(k) in meas['traj'] else meas['traj'][k] for k in Nm]
    ax[0].plot(Nm, Rm, 'ks--', lw=2, label=f'measured total R_int ({meas["source"].split("(")[0].strip()})')
    ax[0].set_xlabel('Cycle N'); ax[0].set_ylabel('R relative to pristine (x)')
    ax[0].set_title('A. Model contact-R ratio vs measured total R_int', fontsize=10)
    ax[0].legend(fontsize=7.5); ax[0].grid(alpha=0.3)

    # ── Panel B: N=100 mechanical vs chemical share (CT representative + band) ──
    tags = [(t, c, l) for t, c, l in (('primary', C_MONO, 'mono'), ('secondary', C_BIM, 'bimodal')) if t in res]
    x = np.arange(len(tags))
    mech, lo, hi = [], [], []
    for t, _, _ in tags:
        r = res[t]['rows'][-1]
        m = (r.get('mech_share_ct_nom') or 0.0) * 100
        mech.append(m)
        lo.append(m - (r.get('mech_share_lo') or 0.0) * 100)
        hi.append((r.get('mech_share_hi') or 0.0) * 100 - m)
    ax[1].bar(x, mech, 0.5, yerr=[lo, hi], capsize=6, color=[c for _, c, _ in tags],
              label='mechanical contact share (CT, band = law x f0)')
    ax[1].bar(x, [100 - m for m in mech], 0.5, bottom=mech, color='#bbbbbb', alpha=0.6,
              label='chemical share (measured residual)')
    for i, m in enumerate(mech):
        ax[1].text(i, m + 2, f'{m:.0f}%', ha='center', fontsize=9, fontweight='bold')
    ax[1].set_xticks(x); ax[1].set_xticklabels([l for _, _, l in tags])
    ax[1].set_ylabel('R_int(N=100) growth share (%)'); ax[1].set_ylim(0, 105)
    ax[1].set_title('B. Mechanical vs chemical @N=100 (measured = Yun 2.87x)', fontsize=10)
    ax[1].legend(fontsize=7.5, loc='center right')

    fig.suptitle('A10 CYCLE-STEP3 - R_int(N): mechanical (contact, DEM ledger) vs chemical (interphase, measured)',
                 fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(a.out + '.svg'); fig.savefig(a.out + '.png', dpi=150)
    # CSV (그림 원자료)
    with open(a.out + '.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['arch', 'cycle', 'rct_holm_rel', 'rct_ct_rel', 'R_int_rel_meas',
                    'mech_share_ct_nom', 'mech_share_lo', 'mech_share_hi', 'R_chem_rel'])
        for t, _, l in tags:
            for r in res[t]['rows']:
                w.writerow([l, r['cycle'], r['rct_holm_rel'], r['rct_ct_rel'], r['R_int_rel_meas'],
                            r.get('mech_share_ct_nom'), r.get('mech_share_lo'), r.get('mech_share_hi'),
                            r['R_chem_rel']])
    print(f'saved {a.out}.svg / .png / .csv')


if __name__ == '__main__':
    main()
