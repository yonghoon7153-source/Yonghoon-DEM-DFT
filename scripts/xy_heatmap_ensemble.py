"""
xy_heatmap_ensemble.py — ensemble summary across all 86 cases.

Input: docs/data/xy_heatmap/<case>.json (per-case heatmap from
                                           extract_xy_fracture_heatmap.py)

Output:
  • docs/figures/xy_heatmap_ensemble.png  (3-panel paper figure):
      Panel 1: severe_frac_overall (%) vs case_id, grouped by tier
      Panel 2: tier별 평균 severe% map (tier 마다 1개 mean heatmap)
      Panel 3: AM_P-only mono vs bimodal vs AM_S-only mono 분포 비교
  • docs/data/xy_heatmap_summary.csv  (per-case scalar metrics)
"""
from __future__ import annotations
import csv
import json
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent

TIER_ORDER = ['1mAh', '6mAh', '8mAh', 'particulate', 'S']
TIER_COLOR = {'1mAh': '#1f77b4', '6mAh': '#ff7f0e',
              '8mAh': '#2ca02c', 'particulate': '#d62728',
              'S': '#9467bd'}


def tier_of(case_name: str) -> str:
    for t in TIER_ORDER:
        if t == 'S':
            if case_name.startswith('input_S_'): return 'S'
        elif t in case_name:
            return t
    return 'other'


def composition_class(ps_ratio: str) -> str:
    """mono AMP / mono AMS / bimodal / unknown"""
    if not ps_ratio or ':' not in str(ps_ratio):
        return 'unknown'
    try:
        a, b = (float(x) for x in str(ps_ratio).split(':')[:2])
    except (ValueError, IndexError):
        return 'unknown'
    if a > 0 and b == 0: return 'mono AM_P'
    if a == 0 and b > 0: return 'mono AM_S'
    if a > 0 and b > 0:  return 'bimodal'
    return 'unknown'


def main():
    in_dir = ROOT / 'docs' / 'data' / 'xy_heatmap'
    if not in_dir.is_dir():
        print(f'{in_dir} 없음 — extract_xy_fracture_heatmap.py 먼저 실행', file=sys.stderr)
        sys.exit(1)

    cases = []
    for jf in sorted(in_dir.glob('*.json')):
        try:
            d = json.loads(jf.read_text())
        except Exception:
            continue
        cases.append(d)
    if not cases:
        print('JSON 없음', file=sys.stderr); sys.exit(1)
    print(f'Loaded {len(cases)} cases')

    # ── Scalar summary CSV ─────────────────────────────────────────────
    summary_csv = ROOT / 'docs' / 'data' / 'xy_heatmap_summary.csv'
    with open(summary_csv, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=[
            'case_name', 'tier', 'mode', 'ps_ratio', 'composition',
            'box_x_um', 'box_y_um', 'n_severe', 'n_total_damaged',
            'severe_frac_overall_pct', 'n_reliable_bins', 'severe_pct_p95',
        ])
        w.writeheader()
        for d in cases:
            sev_arr = np.array([[np.nan if v is None else v for v in row]
                                for row in d['severe_pct_reliable']],
                                dtype=float)
            n_reliable = int(np.sum(~np.isnan(sev_arr)))
            valid = sev_arr[~np.isnan(sev_arr)]
            sev_p95 = round(float(np.percentile(valid, 95)), 1) if valid.size else 0.0
            w.writerow({
                'case_name':              d['case_name'],
                'tier':                   tier_of(d['case_name']),
                'mode':                   d.get('mode', ''),
                'ps_ratio':               d.get('am_se_ratio', ''),
                'composition':            composition_class(d.get('am_se_ratio', '')),
                'box_x_um':               d['box_x_um'],
                'box_y_um':               d['box_y_um'],
                'n_severe':               d['n_severe_contacts'],
                'n_total_damaged':        d['n_total_contacts'],
                'severe_frac_overall_pct': d['severe_frac_overall'],
                'n_reliable_bins':        n_reliable,
                'severe_pct_p95':         sev_p95,
            })
    print(f'CSV → {summary_csv}')

    # ── 3-panel ensemble figure ────────────────────────────────────────
    fig = plt.figure(figsize=(18, 10))
    gs  = fig.add_gridspec(2, 3, height_ratios=[1, 1.2], hspace=0.4, wspace=0.3)

    # Panel 1 (top, span 3 columns): severe_frac_overall vs case, by tier
    ax1 = fig.add_subplot(gs[0, :])
    # Group cases by tier, sort within tier
    grouped = {t: [] for t in TIER_ORDER}
    for d in cases:
        t = tier_of(d['case_name'])
        if t in grouped:
            grouped[t].append((d['case_name'], d['severe_frac_overall']))
    # x positions
    x = 0
    xticks, xlabels = [], []
    for t in TIER_ORDER:
        items = sorted(grouped[t], key=lambda x: -x[1])  # descending severe
        for name, sev in items:
            ax1.bar(x, sev, color=TIER_COLOR[t], width=0.85)
            if sev >= 25:  # annotate extreme cases
                short = name.replace('input_', '')
                ax1.text(x, sev + 1, short, rotation=90, ha='center',
                          va='bottom', fontsize=7, color='#333')
            x += 1
        x += 2   # gap between tiers
    # Tier labels at center of each group
    x = 0
    for t in TIER_ORDER:
        n = len(grouped[t])
        if n:
            ax1.text(x + n/2 - 0.5, -8, t, ha='center', fontsize=11,
                      color=TIER_COLOR[t], fontweight='bold')
            x += n + 2
    ax1.set_ylabel('Severe % overall', fontsize=11)
    ax1.set_title('Per-case severe% (frag + pulv), grouped by capacity tier '
                  '— sorted descending within tier',
                  fontsize=11)
    ax1.set_xticks([])
    ax1.set_ylim(-12, max(70, max(d['severe_frac_overall'] for d in cases) + 5))
    ax1.axhline(0, color='black', linewidth=0.5)
    # threshold lines
    for thr, lbl in [(3, 'workable <3%'), (10, 'risk >10%'), (25, 'failure >25%')]:
        ax1.axhline(thr, linestyle='--', color='gray', linewidth=0.7, alpha=0.6)
        ax1.text(ax1.get_xlim()[1] * 0.99, thr + 0.5, lbl,
                 ha='right', va='bottom', fontsize=8, color='#555',
                 alpha=0.8)
    ax1.grid(axis='y', alpha=0.3)

    # Panel 2 (bottom-left): composition class boxplot
    ax2 = fig.add_subplot(gs[1, 0])
    comp_groups = {'mono AM_P': [], 'bimodal': [], 'mono AM_S': []}
    for d in cases:
        c = composition_class(d.get('am_se_ratio', ''))
        if c in comp_groups:
            comp_groups[c].append(d['severe_frac_overall'])
    labels = list(comp_groups.keys())
    data = [comp_groups[k] for k in labels]
    bp = ax2.boxplot(data, labels=[f'{k}\n(n={len(v)})' for k, v in comp_groups.items()],
                      patch_artist=True, widths=0.55)
    colors = ['#dc2626', '#10b981', '#2563eb']
    for patch, c in zip(bp['boxes'], colors):
        patch.set_facecolor(c); patch.set_alpha(0.5)
    ax2.set_ylabel('Severe % overall', fontsize=10)
    ax2.set_title('Severe% by composition class', fontsize=10)
    ax2.grid(axis='y', alpha=0.3)
    ax2.axhline(10, linestyle='--', color='gray', linewidth=0.7)

    # Panel 3 (bottom-middle): tier vs severe% boxplot
    ax3 = fig.add_subplot(gs[1, 1])
    tier_groups = {t: [d['severe_frac_overall'] for d in cases
                       if tier_of(d['case_name']) == t]
                    for t in TIER_ORDER}
    labels = [f'{t}\n(n={len(v)})' for t, v in tier_groups.items() if v]
    data   = [v for v in tier_groups.values() if v]
    bp = ax3.boxplot(data, labels=labels, patch_artist=True, widths=0.55)
    for patch, t in zip(bp['boxes'],
                          [t for t in TIER_ORDER if tier_groups[t]]):
        patch.set_facecolor(TIER_COLOR[t]); patch.set_alpha(0.5)
    ax3.set_ylabel('Severe % overall', fontsize=10)
    ax3.set_title('Severe% by capacity tier', fontsize=10)
    ax3.grid(axis='y', alpha=0.3)

    # Panel 4 (bottom-right): RVE area vs severe% scatter
    ax4 = fig.add_subplot(gs[1, 2])
    for d in cases:
        t = tier_of(d['case_name'])
        rve_area = d['box_x_um'] * d['box_y_um']
        ax4.scatter(rve_area, d['severe_frac_overall'],
                    color=TIER_COLOR.get(t, '#888'), s=30, alpha=0.7)
    # tier legend
    for t in TIER_ORDER:
        if any(tier_of(d['case_name']) == t for d in cases):
            ax4.scatter([], [], color=TIER_COLOR[t], s=30, label=t)
    ax4.legend(loc='upper right', fontsize=8)
    ax4.set_xlabel('RVE cross-section area (μm²)', fontsize=10)
    ax4.set_ylabel('Severe % overall', fontsize=10)
    ax4.set_title('Finite-size effect — severe% vs RVE area', fontsize=10)
    ax4.set_xscale('log')
    ax4.grid(alpha=0.3)

    fig.suptitle(f'XY fracture heatmap ensemble — {len(cases)} cases',
                 fontsize=13, fontweight='bold', y=0.995)

    out_png = ROOT / 'docs' / 'figures' / 'xy_heatmap_ensemble.png'
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=130, bbox_inches='tight')
    plt.close(fig)
    print(f'PNG → {out_png}')

    # ── Console summary ────────────────────────────────────────────────
    print('\n' + '─' * 80)
    print('Composition class 통계:')
    print('─' * 80)
    for cls in ['mono AM_P', 'bimodal', 'mono AM_S']:
        vals = comp_groups[cls]
        if vals:
            print(f'  {cls:<12s} n={len(vals):>3}  '
                  f'mean={np.mean(vals):>5.1f}%  '
                  f'median={np.median(vals):>5.1f}%  '
                  f'max={max(vals):>5.1f}%')
    print('\nTier 통계:')
    print('─' * 80)
    for t in TIER_ORDER:
        vals = tier_groups[t]
        if vals:
            print(f'  {t:<12s} n={len(vals):>3}  '
                  f'mean={np.mean(vals):>5.1f}%  '
                  f'median={np.median(vals):>5.1f}%  '
                  f'max={max(vals):>5.1f}%')
    print('\nTop 5 worst cases (severe% 최고):')
    print('─' * 80)
    for d in sorted(cases, key=lambda x: -x['severe_frac_overall'])[:5]:
        print(f"  {d['case_name']:<35s} "
              f"sev={d['severe_frac_overall']:>5.1f}%  "
              f"mode={d.get('mode', ''):>9s}  "
              f"ps={d.get('am_se_ratio', '')}")


if __name__ == '__main__':
    main()
