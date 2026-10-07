"""발표 5 쪽 3열 판 — Particle stress ratio (PC · SC · SE ≈ 1 점선) · Contact force share (%) — 그림 + Origin CSV (값 = 기록 CSV 그대로)."""
import csv, os, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)


def read(name):
    rows = list(csv.reader(open(os.path.join(src, name), encoding='utf-8')))
    head, data = rows[0], rows[3:]
    xs = [r[0] for r in data]
    cols = {h: [float(r[i]) if r[i] else None for r in data] for i, h in enumerate(head) if i}
    return xs, cols


def fig(xs, series, ylabel, path, fmt, ref=None):
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11})
    f, ax = plt.subplots(figsize=(4.72, 3.54))
    vals = [v for _, vs, *_ in series for v in vs if v is not None]
    span = (max(vals) - min(vals)) or 1.0
    def place(si, i, v, below):          # 같은 x 의 다른 선과 가까우면 위 · 아래로 갈라 놓는다 (값 글자 겹침 방지)
        near = [o[1][i] for k, o in enumerate(series) if k != si and o[1][i] is not None and abs(o[1][i] - v) < 0.12 * span]
        return below if not near else v < max(near)
    for si, (lab, vs, col, mk, below) in enumerate(series):
        pts = [(i, v) for i, v in enumerate(vs) if v is not None]
        ax.plot([p[0] for p in pts], [p[1] for p in pts], '-', color=col, lw=1.3, marker=mk, ms=5.5, label=lab, zorder=2)
        for i, v in pts:
            if xs[i] == '7:3':
                ax.plot([i], [v], mk, color='red', ms=5.5, zorder=3)
            bl = place(si, i, v, below)
            ax.annotate(fmt.format(v), (i, v - 0.035 * span if bl else v + 0.035 * span), ha='center', va='top' if bl else 'bottom', fontsize=8.5)
    if ref is not None:
        ax.axhline(ref[0], color='0.45', lw=1.0, ls=':', zorder=1)
        ax.annotate(ref[1], (len(xs) - 0.55, ref[0]), ha='right', va='bottom', fontsize=8.5, color='0.35')
    ax.set_xticks(range(len(xs))); ax.set_xticklabels(xs); ax.set_xlim(-0.5, len(xs) - 0.5); ax.margins(y=0.15)
    ax.set_xlabel('PC:SC (wt%)'); ax.set_ylabel(ylabel)
    ax.tick_params(direction='in', top=True, right=True)
    ax.legend(frameon=False, fontsize=9, loc='upper left')
    f.tight_layout(); f.savefig(path, dpi=300); plt.close(f)


def write(path, xs, cols):
    with open(path, 'w', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh, lineterminator='\n')
        w.writerow(['PC:SC'] + [c[0] for c in cols]); w.writerow(['wt%'] + [c[1] for c in cols]); w.writerow(['조성'] + [c[2] for c in cols])
        for i, x in enumerate(xs):
            w.writerow([x] + ['' if c[3][i] is None else f'{c[3][i]:.4f}' for c in cols])


xs, s = read('stress_ratio_lw_all.csv')
fig(xs, [('PC', s['PC'], 'black', 's', True), ('SC', s['SC'], 'gray', 'o', False)], 'Particle stress ratio', os.path.join(out, 'particle_stress_ratio.png'), '{:.2f}',
    ref=(1.0, 'SE ≈ 1'))
write(os.path.join(out, 'particle_stress_ratio.csv'), xs, [
    ('PC', '-', '상 평균 입자 응력 (Love–Weber · von Mises) ÷ 전체 입자 평균 · 모델 내부 비교 (응력 기준틀 미인증)', s['PC']),
    ('SC', '-', '같음', s['SC']), ('SE', '-', '같음 (입자 수 대부분 = SE ⇒ ≈ 1 · 그림에는 점선)', s['SE'])])
xs, c = read('contact_force_share.csv')
fig(xs, [('AM–AM', c['AM–AM'], 'black', 's', True), ('AM–SE', c['AM–SE'], 'gray', 'o', False), ('SE–SE', c['SE–SE'], '#1f3fbf', '^', True)],
    'Force contribution (%)', os.path.join(out, 'force_contribution.png'), '{:.1f}')
write(os.path.join(out, 'force_contribution.csv'), xs, [
    ('AM–AM', '%', '쌍 묶음의 (평균 법선력 × 접촉 수) ÷ 전체 — 판 하중 분담 아님', c['AM–AM']),
    ('AM–SE', '%', '같음', c['AM–SE']), ('SE–SE', '%', '같음', c['SE–SE'])])
print(open(os.path.join(out, 'particle_stress_ratio.csv'), encoding='utf-8').read()); print(open(os.path.join(out, 'force_contribution.csv'), encoding='utf-8').read())
