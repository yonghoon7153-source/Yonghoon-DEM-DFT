"""ps45 다섯 조성 — 힘 · 응력 지표 그림 (발표 양식: 파랑 선 · 사각 점 · 7:3 빨강 · 점마다 값) + Origin 용 CSV (Long Name · Units · Comment 세 줄).
입력 = 망 배치 폴더 (network_cases.tsv + work/results/<id>/full_metrics.json).  값은 full_metrics 그대로 (새 계산 = 힘 몫 = 평균 × 개수 의 비뿐)."""
import csv, json, os, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ORDER = ['0:10', '3:7', '5:5', '7:3', '10:0']
PAIRS = [('AM_P_SE', 'PC–SE'), ('AM_S_SE', 'SC–SE'), ('SE_SE', 'SE–SE'), ('AM_P_AM_P', 'PC–PC'), ('AM_P_AM_S', 'PC–SC'), ('AM_S_AM_S', 'SC–SC')]
STAGES = [('intact', 'Intact'), ('microcrack', 'Microcrack'), ('multicrack', 'Multicrack'), ('fragmentation', 'Fragmentation'), ('pulverization', 'Pulverization')]


def load(batch):
    rows = list(csv.DictReader(open(os.path.join(batch, 'network_cases.tsv'), encoding='utf-8'), delimiter='\t'))
    out = {}
    for r in rows:
        p = os.path.join(batch, 'work', 'results', r['case_id'], 'full_metrics.json')
        if os.path.exists(p):
            out[r['P_S']] = json.load(open(p, encoding='utf-8'))
    return {k: out[k] for k in ORDER if k in out}


def fnum(v):
    try:
        x = float(v)
        return x if x == x else None
    except (TypeError, ValueError):
        return None


def panel(ax, xs, ys, label=None, color='#1f3fbf', marker='s', red=True, fmt='{:.2f}', dy=0.03, below=False):
    pts = [(i, y) for i, y in zip(range(len(xs)), ys) if y is not None]
    if not pts:
        return
    ax.plot([p[0] for p in pts], [p[1] for p in pts], '-', color=color, lw=1.2, marker=marker, ms=5, label=label, zorder=2)
    span = (max(p[1] for p in pts) - min(p[1] for p in pts)) or abs(pts[0][1]) or 1.0
    for i, y in pts:
        if red and xs[i] == '7:3':
            ax.plot([i], [y], marker, color='red', ms=5, zorder=3)
        ax.annotate(fmt.format(y), (i, y - dy * span if below else y + dy * span), ha='center',
                    va='top' if below else 'bottom', fontsize=8)


def style(ax, xs, ylabel):
    ax.set_xticks(range(len(xs)))
    ax.set_xticklabels(xs)
    ax.set_xlim(-0.5, len(xs) - 0.5)
    ax.set_xlabel('PC:SC (wt%)')
    ax.set_ylabel(ylabel)
    ax.tick_params(direction='in', top=True, right=True)
    for s in ax.spines.values():
        s.set_linewidth(1.0)


def write_csv(path, xs, cols):
    """cols = [(long name, units, comment, values)] — Origin 머리 세 줄 (Long Name · Units · Comment)"""
    with open(path, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['PC:SC'] + [c[0] for c in cols])
        w.writerow(['wt%'] + [c[1] for c in cols])
        w.writerow(['조성'] + [c[2] for c in cols])
        for i, x in enumerate(xs):
            w.writerow([x] + ['' if c[3][i] is None else repr(c[3][i]) for c in cols])


def main(batch, out):
    os.makedirs(out, exist_ok=True)
    d = load(batch)
    xs = list(d)
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10})
    made = []
    # ① 상별 평균 응력 비 (Love–Weber · 벽 제외 값이 있으면 그것)
    for tag, suf in (('all', ''), ('nowall', '_nowall')):
        ser = [(lab, [fnum(d[x].get(f'stress_ratio_{t}_lw{suf}')) if d[x].get('stress_lw_status') == 'OK' else None for x in xs])
               for t, lab in (('AM_P', 'PC'), ('AM_S', 'SC'), ('SE', 'SE'))]
        if not any(v is not None for _, vs in ser for v in vs):
            continue
        fig, ax = plt.subplots(figsize=(4.72, 3.54))
        for (lab, vs), (c, m, bl) in zip(ser, (('black', 's', True), ('gray', 'o', False), ('#1f3fbf', '^', False))):
            panel(ax, xs, vs, label=lab, color=c, marker=m, fmt='{:.2f}', below=bl)
        ax.axhline(1.0, color='0.6', lw=0.8, ls=':')
        style(ax, xs, 'Particle stress ratio (phase / all)')
        ax.legend(frameon=False, fontsize=8)
        fig.tight_layout(); p = os.path.join(out, f'stress_ratio_lw_{tag}.png'); fig.savefig(p, dpi=300); plt.close(fig); made.append(p)
        write_csv(os.path.join(out, f'stress_ratio_lw_{tag}.csv'), xs,
                  [(lab, '-', f'Love–Weber 입자 응력 상 평균 ÷ 전체 평균{" · 벽 접촉 입자 제외" if suf else ""} (모델 내부 · 응력 틀 미인증)', vs) for lab, vs in ser])
    # ② 접촉 쌍별 평균 법선력 (µN) + 힘 몫 (%)
    fn = [(lab, [fnum(d[x].get(f'fn_{k}_mean')) for x in xs]) for k, lab in PAIRS]
    cnt = [(lab, [fnum(d[x].get(f'area_{k}_n')) for x in xs]) for k, lab in PAIRS]
    fn = [s for s in fn if any(v is not None for v in s[1])]
    if fn:
        fig, ax = plt.subplots(figsize=(4.72, 3.54))
        cols = ['black', 'gray', '#1f3fbf', '#b5651d', '#2e8b57', '#8a2be2']
        for (lab, vs), c in zip(fn, cols):
            panel(ax, xs, vs, label=lab, color=c, red=False, fmt='{:.0f}')
        style(ax, xs, 'Mean normal contact force (µN)')
        ax.legend(frameon=False, fontsize=7, ncol=2)
        fig.tight_layout(); p = os.path.join(out, 'contact_force_mean.png'); fig.savefig(p, dpi=300); plt.close(fig); made.append(p)
        write_csv(os.path.join(out, 'contact_force_mean.csv'), xs, [(lab, 'µN', 'DEM 접촉 덤프 법선력 평균 (덱 축척 환산)', vs) for lab, vs in fn])
        share = {}
        for i, x in enumerate(xs):
            tot = sum((f[1][i] or 0) * (n[1][i] or 0) for f, n in zip([s for s in [(lab, [fnum(d[x2].get(f'fn_{k}_mean')) for x2 in xs]) for k, lab in PAIRS]],
                                                                          cnt))
            for (k, lab), (_, fv), (_, nv) in zip(PAIRS, [(lab, [fnum(d[x2].get(f'fn_{k}_mean')) for x2 in xs]) for k, lab in PAIRS], cnt):
                share.setdefault(lab, []).append(100 * fv[i] * nv[i] / tot if tot and fv[i] is not None and nv[i] is not None else None)
        groups = [('AM–AM', ['PC–PC', 'PC–SC', 'SC–SC']), ('AM–SE', ['PC–SE', 'SC–SE']), ('SE–SE', ['SE–SE'])]
        gs = [(g, [sum(share[m][i] for m in ms if share.get(m) and share[m][i] is not None) if any(share.get(m) and share[m][i] is not None for m in ms) else None
                   for i in range(len(xs))]) for g, ms in groups]
        fig, ax = plt.subplots(figsize=(4.72, 3.54))
        for (g, vs), (c, m, bl) in zip(gs, (('black', 's', True), ('gray', 'o', False), ('#1f3fbf', '^', True))):
            panel(ax, xs, vs, label=g, color=c, marker=m, fmt='{:.1f}', below=bl)
        style(ax, xs, 'Share of contact normal force (%)')
        ax.legend(frameon=False, fontsize=8)
        fig.tight_layout(); p = os.path.join(out, 'contact_force_share.png'); fig.savefig(p, dpi=300); plt.close(fig); made.append(p)
        write_csv(os.path.join(out, 'contact_force_share.csv'), xs, [(g, '%', '쌍 묶음의 (평균 법선력 × 접촉 수) ÷ 전체 — 판 하중 분담 아님', vs) for g, vs in gs])
    # ③ AM–AM 파괴 단계 (힘 기반 Auerbach) — 1저자 10-07: 발표에서 뺌 (--with-fracture 일 때만)
    st = [] if not WITH_FRACTURE else [(lab, [fnum(d[x].get(f'frac_{s}_force_pct')) for x in xs]) for s, lab in STAGES]
    if st and any(v is not None for _, vs in st for v in vs):
        fig, ax = plt.subplots(figsize=(4.72, 3.54))
        bottom = [0.0] * len(xs)
        colors = ['#cfd8ea', '#9fb3d9', '#5f7fc0', '#2a4f9e', '#0d2a66']
        for (lab, vs), c in zip(st, colors):
            vv = [v or 0.0 for v in vs]
            ax.bar(range(len(xs)), vv, bottom=bottom, color=c, label=lab, width=0.6, edgecolor='black', linewidth=0.5)
            bottom = [b + v for b, v in zip(bottom, vv)]
        style(ax, xs, 'AM–AM contacts (%)')
        ax.set_ylim(0, 100)
        ax.legend(frameon=False, fontsize=7, loc='upper left', bbox_to_anchor=(1.0, 1.0))
        fig.tight_layout(); p = os.path.join(out, 'am_am_fracture_stages.png'); fig.savefig(p, dpi=300); plt.close(fig); made.append(p)
        fi = [fnum(d[x].get('fracture_index_force')) for x in xs]
        write_csv(os.path.join(out, 'am_am_fracture_stages.csv'), xs,
                  [(lab, '%', 'F / P_c (Auerbach · K_IC PC 0.3 · SC 1.0 · A 200 — 상수 출처 미확인 · 조성 비교용)', vs) for lab, vs in st]
                  + [('Fracture index', '-', '(파편화 + 분쇄) / AM–AM 접촉', fi)])
    print('조성', xs)
    for p in made:
        print(' ', p)


WITH_FRACTURE = False
if __name__ == '__main__':
    WITH_FRACTURE = '--with-fracture' in sys.argv[3:]
    main(sys.argv[1], sys.argv[2])
