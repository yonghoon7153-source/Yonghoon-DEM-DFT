"""ps45 다섯 조성 — 이온 · 전자전도도 (Tabor = Physics 모드 · 세대 2 망 FULL) 발표 양식 그림 + Origin CSV.  값 = network_cases.tsv 그대로."""
import csv, os, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ORDER = ['0:10', '3:7', '5:5', '7:3', '10:0']


def draw(xs, vs, ylabel, path, fmt):
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10})
    fig, ax = plt.subplots(figsize=(4.72, 3.54))
    span = (max(vs) - min(vs)) or 1.0
    ax.plot(range(len(xs)), vs, '-', color='#1f3fbf', lw=1.2, marker='s', ms=5, zorder=2)
    for i, y in enumerate(vs):
        if xs[i] == '7:3':
            ax.plot([i], [y], 's', color='red', ms=5, zorder=3)
        ax.annotate(fmt.format(y), (i, y + 0.03 * span), ha='center', va='bottom', fontsize=8)
    ax.set_xticks(range(len(xs))); ax.set_xticklabels(xs); ax.set_xlim(-0.5, len(xs) - 0.5); ax.margins(y=0.14)
    ax.set_xlabel('PC:SC (wt%)'); ax.set_ylabel(ylabel)
    ax.tick_params(direction='in', top=True, right=True)
    fig.tight_layout(); fig.savefig(path, dpi=300); plt.close(fig)


def main(tsv, out):
    os.makedirs(out, exist_ok=True)
    rows = {r['P_S']: r for r in csv.DictReader(open(tsv, encoding='utf-8'), delimiter='\t')}
    xs = [x for x in ORDER if x in rows]
    for x in xs:
        r = rows[x]
        assert r.get('psi_placement_physics') == 'multiply' and r['sigma_full_status_physics'] == 'computed' and r['electronic_status_physics'] == 'computed', (x, r.get('sigma_full_status_physics'), r.get('electronic_status_physics'))
    si = [float(rows[x]['sigma_full_mScm_physics']) for x in xs]
    se = [float(rows[x]['electronic_sigma_full_mScm_physics']) for x in xs]
    draw(xs, si, 'Ionic conductivity (mS/cm)', os.path.join(out, 'sigma_ion_tabor.png'), '{:.3f}')
    draw(xs, se, 'Electronic conductivity (mS/cm)', os.path.join(out, 'sigma_e_tabor.png'), '{:.2f}')
    with open(os.path.join(out, 'sigma_tabor_g2.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['PC:SC', 'Ionic conductivity (Tabor)', 'Electronic conductivity (Tabor)'])
        w.writerow(['wt%', 'mS/cm', 'mS/cm'])
        w.writerow(['조성', 'sigma_full_mScm_physics · 망 FULL · SE σ₀ 3.0 mS/cm (펠릿값)', 'electronic_sigma_full_mScm_physics · 망 FULL (Stage E 파괴 보정 전) · AM 입자 σ 입력 50 mS/cm (CL-92: 측정 NCM811 의 약 10 배) · 탄소 첨가제 없음'])
        for x, a, b in zip(xs, si, se):
            w.writerow([x, repr(a), repr(b)])
    print('σ_ion', [round(v, 4) for v in si]); print('σ_e', [round(v, 3) for v in se])


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
