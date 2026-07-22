#!/usr/bin/env python3
"""STEP4 R_int 사다리 비교 — 여러 step4 npz(같은 전극·rate, 다른 집전체 R_int)를 한 그림에.

풀셀 축(R_int Phase 2): 같은 베드/그리드에 R_int만 바꾼 단일변수 실험 → delivered vs R_int.
V_term = V_cell − I·R_int → R_int↑ 시 CC 조기종료·용량 압축.  전극-내부(R_int=0)가 상한.

입력: --npz PATH:LABEL:RINT  (여러 개).  각 npz는 step4_dyn 산출 (충전 CCCV 또는 방전).
출력: <out>.svg + .png + .csv (곡선 + delivered%/R_int 요약; 랩 규약 동시산출).

사용 예 (5점 사다리 {DBE 0/10/12, SBE 0/18}):
  python3 scripts/step4_rint_ladder.py \
    --npz DBE0.npz:DBE\ R0:0 --npz DBE10.npz:DBE\ R10\ C-SUS:10 --npz DBE12.npz:DBE\ R12\ bareAl:12 \
    --npz SBE0.npz:SBE\ R0:0 --npz SBE18.npz:SBE\ R18\ bareAl:18 --out rint_ladder
"""
import argparse
import csv
import json

import numpy as np


def load(path):
    d = np.load(path, allow_pickle=False)
    meta = json.loads(str(d['params_json']))
    x0, x100 = meta['x0'], meta['x100']
    charge = bool(meta.get('cv_hold') or meta.get('c_rate') and meta.get('x_init', x0) == x100)
    xm = d['x_mean']
    win = abs(x100 - x0)
    # 충전=(x100−x̄)/win, 방전=(x̄−x0)/win → 진행 SOC 분율
    xi = meta.get('x_init', x100 if meta.get('cv_hold') else x0)
    q = np.abs(xm - xi) / win * 100.0                        # SOC-창 진행 %
    return dict(path=path, Vt=d['V_terminal'], Vc=d['V'], I=d['I'], t=d['t'], q=q,
                x_mean=xm, delivered=float(d['q_frac_at_cutoff']) * 100.0,
                end=str(d['end_reason']) if 'end_reason' in d else meta.get('end_reason', '?'),
                rint=meta.get('r_int_ohm_cm2', 0.0), c_rate=meta.get('c_rate'),
                charge=bool(meta.get('cv_hold')), v_min=meta.get('v_min'), v_max=meta.get('v_max'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--npz', action='append', required=True,
                    help='PATH:LABEL:RINT (여러 번); RINT는 라벨/정렬용 (npz meta 우선)')
    ap.add_argument('--out', default='rint_ladder')
    ap.add_argument('--title', default='STEP4 R_int ladder (full-cell axis)')
    a = ap.parse_args()
    items = []
    for spec in a.npz:
        parts = spec.split(':')
        path, label = parts[0], (parts[1] if len(parts) > 1 else parts[0])
        rint_hint = float(parts[2]) if len(parts) > 2 and parts[2] else None
        r = load(path)
        r['label'] = label
        if rint_hint is not None and abs(r['rint'] - rint_hint) > 0.5:
            print(f'  ⚠ {label}: npz R_int={r["rint"]} ≠ 라벨 힌트 {rint_hint} (npz 값 사용)', flush=True)
        items.append(r)
    items.sort(key=lambda r: (r['label'].split()[0], r['rint']))   # 전극군 → R_int

    # 요약 출력 + CSV
    print(f'{"label":24s} {"R_int":>6s} {"end":>10s} {"delivered%":>11s} {"Vterm0":>8s}')
    for r in items:
        print(f'{r["label"]:24s} {r["rint"]:6.0f} {r["end"]:>10s} {r["delivered"]:11.1f} '
              f'{r["Vt"][0]:8.3f}')
    with open(a.out + '.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['label', 'R_int_ohm_cm2', 'end_reason', 'delivered_pct', 'Vterm_start',
                    'c_rate', 'charge'])
        for r in items:
            w.writerow([r['label'], r['rint'], r['end'], round(r['delivered'], 2),
                        round(float(r['Vt'][0]), 4), r['c_rate'], r['charge']])

    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        print(f'saved {a.out}.csv (matplotlib 없음 — 그림 스킵)')
        return
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.4))
    groups = sorted(set(r['label'].split()[0] for r in items))
    _tab = plt.get_cmap('tab10')
    cmap = {g: _tab(i) for i, g in enumerate(groups)}
    for r in items:
        g = r['label'].split()[0]
        ls = '-' if r['rint'] == 0 else ('--' if r['rint'] < 15 else ':')
        ax[0].plot(r['q'], r['Vt'], ls, color=cmap[g], lw=1.8, label=f'{r["label"]} ({r["delivered"]:.1f}%)')
    ax[0].set_xlabel('SOC window progress (%)'); ax[0].set_ylabel('Terminal voltage (V)')
    ax[0].set_title('A. V_terminal curves (R_int series)', fontsize=10)
    ax[0].legend(fontsize=7); ax[0].grid(alpha=0.3)
    # 패널 B: delivered vs R_int (전극군별)
    for g in groups:
        gs = sorted([r for r in items if r['label'].split()[0] == g], key=lambda r: r['rint'])
        ax[1].plot([r['rint'] for r in gs], [r['delivered'] for r in gs], 'o-',
                   color=cmap[g], lw=1.8, ms=7, label=g)
        for r in gs:
            ax[1].annotate(f'{r["delivered"]:.1f}', (r['rint'], r['delivered']),
                           fontsize=7, va='bottom', ha='center')
    ax[1].set_xlabel('R_int (Ohm cm2)'); ax[1].set_ylabel('Delivered / charged (% of window)')
    ax[1].set_title('B. Capacity vs interface resistance', fontsize=10)
    ax[1].legend(fontsize=8); ax[1].grid(alpha=0.3)
    fig.suptitle(a.title, fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(a.out + '.svg'); fig.savefig(a.out + '.png', dpi=150)
    print(f'saved {a.out}.svg / .png / .csv')


if __name__ == '__main__':
    main()
