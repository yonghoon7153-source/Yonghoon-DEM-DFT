"""ps45 다섯 조성 — 수송 tortuosity (tau2 = φ_SE·σ₀/σ_ion · 제곱근 아님) · 세대 2 망 (Tabor = Physics 모드 · Hertz = 주 값) — 발표 양식 그림 + Origin CSV.
입력 = webapp_network_batch 출력 폴더의 network_cases.tsv (값 그대로 · 새 계산 없음)."""
import csv, os, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ORDER = ['0:10', '3:7', '5:5', '7:3', '10:0']


def main(tsv, out):
    os.makedirs(out, exist_ok=True)
    rows = {r['P_S']: r for r in csv.DictReader(open(tsv, encoding='utf-8'), delimiter='\t')}
    xs = [x for x in ORDER if x in rows]
    for x in xs:
        assert rows[x]['ion_net_status_hertz'] == 'OK' and rows[x]['ion_net_status_physics'] == 'OK', x
        assert rows[x].get('psi_placement_physics') == 'multiply', x          # 세대 2 (ψ 곱셈) 만
    th = [float(rows[x]['tau2_ion_hertz']) for x in xs]
    tp = [float(rows[x]['tau2_ion_physics']) for x in xs]
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10})

    def draw(series, name, ylabel):
        fig, ax = plt.subplots(figsize=(4.72, 3.54))
        allv = [v for _, v, _, _ in series for v in v]
        span = (max(allv) - min(allv)) or 1.0
        for lab, vs, c, below in series:
            ax.plot(range(len(xs)), vs, '-', color=c, lw=1.2, marker='s', ms=5, label=lab, zorder=2)
            for i, y in enumerate(vs):
                if xs[i] == '7:3':
                    ax.plot([i], [y], 's', color='red', ms=5, zorder=3)
                ax.annotate(f'{y:.2f}', (i, y - 0.03 * span if below else y + 0.03 * span), ha='center', va='top' if below else 'bottom', fontsize=8)
        ax.set_xticks(range(len(xs))); ax.set_xticklabels(xs); ax.set_xlim(-0.5, len(xs) - 0.5); ax.margins(y=0.14)
        ax.set_xlabel('PC:SC (wt%)'); ax.set_ylabel(ylabel)
        ax.tick_params(direction='in', top=True, right=True)
        if len(series) > 1:
            ax.legend(frameon=False, fontsize=8)
        fig.tight_layout(); p = os.path.join(out, name + '.png'); fig.savefig(p, dpi=300); plt.close(fig)
        return p

    made = [draw([('Tabor', tp, '#1f3fbf', False)], 'transport_tortuosity_tabor', 'Transport tortuosity'),
            draw([('Hertz', th, '#1f3fbf', False), ('Tabor', tp, '#e07b00', True)], 'transport_tortuosity_hertz_tabor', 'Transport tortuosity')]
    with open(os.path.join(out, 'transport_tortuosity_g2.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['PC:SC', 'Transport tortuosity (Tabor)', 'Transport tortuosity (Hertz)'])
        w.writerow(['wt%', '-', '-'])
        w.writerow(['조성', 'tau2_ion_physics = φ_SE·σ₀/σ_ion (제곱근 아님) · 세대 2 망 (ψ 곱셈 · g2 면적)', 'tau2_ion_hertz (주 값 · 세대 1 과 상대 1e-6 안)'])
        for x, a, b in zip(xs, tp, th):
            w.writerow([x, repr(a), repr(b)])
    print('조성', xs); print('Tabor', [round(v, 3) for v in tp]); print('Hertz', [round(v, 3) for v in th])
    for p in made:
        print(' ', p)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
