#!/usr/bin/env python3
"""φ(z) 두께방향 전위 프로파일 플롯 — Oh 2025 (MSE R 164, 100970) Fig 4e 문법.

payload json의 step3.phi_profile(신형 payload — mpm_webapp_payload가 ΔV=1V 전도 솔브에서
층별 전도-복셀 평균 φ를 export)을 읽어, 정규화 두께 vs 전위를 그린다:
  • 전자망 (정본 집전체) — 실선
  • 전자망 (bare 집전체) — 점선: 집전체 계면(z=0) 강하 = 그들 primer 그림의 우리판
  • 이온망 — 별도 패널 (--ionic)

사용:  python3 scripts/step3_phi_profile_plot.py PAYLOAD[:LABEL] [PAYLOAD2[:LABEL2] …]
           [--out step3_phi_profile] [--ionic]
표기 규약: 우리 솔브는 바닥판(집전체) φ=1, 꼭대기 φ=0.  Oh Fig4e와 시각 정합을 위해
x축 = z/L (0=집전체), y축 = φ 그대로 (그들은 상판 1V — 방향만 거울, 물리 동일).
png+svg+csv 동시 산출 (랩 규약).
"""
import argparse
import csv
import json
import os
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('payloads', nargs='+', help='mpm_payload.json[:LABEL] …')
    ap.add_argument('--out', default='step3_phi_profile')
    ap.add_argument('--ionic', action='store_true', help='이온망 패널 추가 (2패널)')
    a = ap.parse_args()

    series = []
    for tok in a.payloads:
        path, _, lab = tok.partition(':')
        lab = lab or os.path.basename(path).replace('.json', '')
        d = json.load(open(path))
        s3 = (d.get('mpm_metrics') or {}).get('step3') or d.get('step3') or {}
        pp = s3.get('phi_profile')
        if not pp or 'electronic' not in pp:
            print(f'⚠ {path}: phi_profile 없음 — 신형 payload로 재생성 필요 '
                  f'(payload-only 재실행이면 압밀 불필요)', file=sys.stderr)
            continue
        series.append((lab, pp))
        ne = len(pp['electronic']['z_um'])
        print(f'  {lab}: 전자 {ne}층'
              + (f' · bare {len(pp["electronic_bare"]["z_um"])}층' if pp.get('electronic_bare') else '')
              + (f' · 이온 {len(pp["ionic"]["z_um"])}층' if pp.get('ionic') else ''))
    if not series:
        raise SystemExit('플롯할 시리즈 없음')

    with open(a.out + '.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['label', 'network', 'z_um', 'z_over_L', 'phi_V_at_dV1V'])
        for lab, pp in series:
            for net in ('electronic', 'electronic_bare', 'ionic'):
                if not pp.get(net):
                    continue
                zs, ps = pp[net]['z_um'], pp[net]['phi']
                L = max(zs) if zs else 1.0
                for z, p in zip(zs, ps):
                    w.writerow([lab, net, z, f'{z / L:.4f}', p])

    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        print(f'matplotlib 없음 → CSV만 저장: {a.out}.csv')
        return
    ncol = 2 if a.ionic else 1
    fig, axs = plt.subplots(1, ncol, figsize=(4.6 * ncol, 3.5), dpi=300, squeeze=False)
    colors = ['#1f6fb2', '#d1495b', '#2e8b57', '#e0a100']
    axE = axs[0][0]
    for i, (lab, pp) in enumerate(series):
        c = colors[i % len(colors)]
        zs, ps = pp['electronic']['z_um'], pp['electronic']['phi']
        L = max(zs)
        axE.plot([z / L for z in zs], ps, '-', lw=1.7, color=c, label=lab)
        if pp.get('electronic_bare'):
            zb, pb = pp['electronic_bare']['z_um'], pp['electronic_bare']['phi']
            axE.plot([z / L for z in zb], pb, '--', lw=1.2, color=c, alpha=0.75,
                     label=f'{lab} (bare collector)')
    axE.set_xlabel('Normalized thickness z/L (0 = collector)')
    axE.set_ylabel('Electric potential (V, at ΔV = 1 V)')
    axE.legend(frameon=False, fontsize=8)
    if a.ionic:
        axI = axs[0][1]
        for i, (lab, pp) in enumerate(series):
            if not pp.get('ionic'):
                continue
            zs, ps = pp['ionic']['z_um'], pp['ionic']['phi']
            L = max(zs)
            axI.plot([z / L for z in zs], ps, '-', lw=1.7, color=colors[i % len(colors)], label=lab)
        axI.set_xlabel('Normalized thickness z/L')
        axI.set_ylabel('Ionic potential (V, at ΔV = 1 V)')
        axI.legend(frameon=False, fontsize=8)
    for ax in fig.axes:
        for s in ('top', 'right'):
            ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(a.out + '.png')
    fig.savefig(a.out + '.svg')
    print(f'saved {a.out}.png / .svg / .csv')


if __name__ == '__main__':
    main()
