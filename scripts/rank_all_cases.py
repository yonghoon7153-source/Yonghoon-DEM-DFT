"""
rank_all_cases.py — Run grade_engine on every case in case_summary.csv
and produce a honest full ranking.

Output: docs/full_ranking.csv  +  console summary by capacity tier.
"""
import csv
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))

from grade_engine import build_overall_grade


def cast(v):
    """CSV string → Python primitive."""
    if v is None or v == '':
        return None
    try:
        f = float(v)
        # Keep as int if it looks like one
        return int(f) if f.is_integer() and abs(f) < 1e10 else f
    except (TypeError, ValueError):
        return v


def csv_row_to_metrics(row):
    """Translate CSV row (with fm__/ip__/meta__ prefixes) → grade_engine
    input dict.  Includes the synthetic _input_* / _meta_* keys so axes
    like Q_areal / bimodal / commercial composition resolve."""
    m = {}
    case_id = (row.get('meta__name') or row.get('case_id') or '').strip()
    scale = cast(row.get('meta__scale')) or 1000

    # Direct fm__ → metrics
    for k, v in row.items():
        if k.startswith('fm__'):
            m[k[4:]] = cast(v)

    # input_params via the same _input_* contract grade_engine expects
    ip = {}
    for k, v in row.items():
        if k.startswith('ip__'):
            ip[k[4:]] = cast(v)

    # AM:SE ratio
    ratio = ip.get('am_se_ratio') or m.get('am_se_ratio')
    if ratio:
        m['_input_am_se_ratio'] = str(ratio)

    # Box
    bx, by = ip.get('box_x'), ip.get('box_y')
    if bx is not None and by is not None:
        try:
            m['_input_box_x'] = float(bx) * float(scale)
            m['_input_box_y'] = float(by) * float(scale)
        except (TypeError, ValueError):
            pass

    # Radii (sim → μm)
    for src, dst in (('r_SE',   '_input_r_SE_um'),
                      ('r_AM_P', '_input_r_AM_P_um'),
                      ('r_AM_S', '_input_r_AM_S_um')):
        v = ip.get(src) or ip.get(src + '_sim')
        if v is not None:
            try:
                m[dst] = float(v) * float(scale)
            except (TypeError, ValueError):
                pass

    # Target pressure
    tp = ip.get('target_press_sim')
    if tp is not None:
        try:
            m['_input_target_press_MPa'] = float(tp) * 1000 if float(tp) < 10 else float(tp)
        except (TypeError, ValueError):
            pass

    # Meta (mode + ps_ratio for bimodal detection)
    m['_meta_mode'] = row.get('meta__mode') or None
    m['_meta_ps_ratio'] = row.get('meta__ps_ratio') or None

    return case_id, m


def tier_of(case_id: str) -> str:
    """Capacity tier from case_id."""
    if '1mAh' in case_id:        return '1mAh'
    if '6mAh' in case_id:        return '6mAh'
    if '8mAh' in case_id:        return '8mAh'
    if 'particulate' in case_id: return 'particulate'
    if case_id.startswith('input_S_'):   return 'S_series'
    return 'other'


def main():
    csv_path = ROOT / 'docs' / 'case_summary.csv'
    if not csv_path.exists():
        print(f'{csv_path} not found', file=sys.stderr)
        sys.exit(1)

    with open(csv_path) as f:
        rows = list(csv.DictReader(f))
    print(f'Loaded {len(rows)} cases from {csv_path}')

    corpus_csv = str(ROOT / 'docs' / 'data' / 'se_diagnostics_82.csv')
    if not os.path.exists(corpus_csv):
        corpus_csv = None
        print('  (no corpus CSV — cut_fraction / bn_below_frac axes will be N/A)')

    results = []
    for row in rows:
        case_id, m = csv_row_to_metrics(row)
        if not case_id:
            continue
        try:
            r = build_overall_grade(m, corpus_csv, se_aux=None,
                                    case_id=case_id)
        except Exception as e:
            print(f'  [{case_id}] FAILED: {type(e).__name__}: {e}')
            continue
        comp = r['composite']
        results.append({
            'rank':         0,   # filled after sort
            'case_id':      case_id,
            'score':        comp['score'],
            'grade':        comp['grade'],
            'n_axes':       comp['n_axes'],
            'n_total':      comp['n_total'],
            'is_unit_cell': comp.get('is_unit_cell', False),
            'base_case':    comp.get('base_case', case_id),
            'mode':         row.get('meta__mode', ''),
            'am_se':        m.get('am_se_ratio', ''),
            'thickness':    m.get('thickness_um'),
            'porosity':     m.get('porosity'),
            'sigma_ionic':  m.get('sigma_full_mScm_stage_e_physics')
                            or m.get('sigma_full_mScm_physics'),
            'asr_ionic':    None,
            'Q_grav':       None,
            'Q_vol':        None,
            'wt_am':        None,
            # category scores
            **{f'cat_{c}': s for c, s in r['category_scores'].items()},
        })
        # Pull a few axis values
        for ax in r['axes']:
            if 'ASR_ionic' in ax['label'] and ax['value'] is not None:
                results[-1]['asr_ionic'] = round(ax['value'], 1)
            if 'Q_gravimetric' in ax['label'] and ax['value'] is not None:
                results[-1]['Q_grav'] = round(ax['value'], 1)
            if 'Q_volumetric' in ax['label'] and ax['value'] is not None:
                results[-1]['Q_vol'] = round(ax['value'], 1)
            if ax['label'].startswith('wt_AM') and ax['value'] is not None:
                results[-1]['wt_am'] = round(ax['value'], 1)

    # Assign capacity tier
    for r in results:
        r['tier'] = tier_of(r['case_id'])

    # Cross-tier (overall) ranking
    results.sort(key=lambda r: r['score'] if r['score'] is not None else -1,
                  reverse=True)
    for i, r in enumerate(results, 1):
        r['rank_overall'] = i

    # Within-tier ranking (fair comparison)
    for tier in {r['tier'] for r in results}:
        tier_rs = [r for r in results if r['tier'] == tier]
        tier_rs.sort(key=lambda r: r['score'] if r['score'] is not None else -1,
                      reverse=True)
        for i, r in enumerate(tier_rs, 1):
            r['rank_in_tier'] = i
            r['tier_size'] = len(tier_rs)

    # Keep `rank` alias = within-tier rank (the fairer one)
    for r in results:
        r['rank'] = r.get('rank_in_tier', 0)

    # Write CSV
    out_csv = ROOT / 'docs' / 'full_ranking.csv'
    keys = ['rank_overall', 'rank_in_tier', 'tier', 'tier_size',
            'case_id', 'score', 'grade', 'n_axes', 'n_total',
            'is_unit_cell', 'mode', 'am_se', 'wt_am',
            'thickness', 'porosity', 'sigma_ionic', 'asr_ionic',
            'Q_grav', 'Q_vol', 'base_case']
    keys += sorted([k for k in results[0].keys() if k.startswith('cat_')])
    with open(out_csv, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=keys, extrasaction='ignore')
        w.writeheader()
        for r in results:
            w.writerow(r)
    print(f'\nFull ranking → {out_csv} ({len(results)} cases)')

    # Per-tier 순위 (fair comparison — 같은 capacity 안에서)
    tier_order = ['6mAh', '8mAh', '1mAh', 'particulate', 'S_series', 'other']
    print('\n' + '═' * 100)
    print('  TIER 별 ranking (★ 권장: 면용량이 같은 case끼리 비교가 공정)')
    print('═' * 100)
    for tier in tier_order:
        tier_rs = sorted(
            [r for r in results if r['tier'] == tier],
            key=lambda r: r['rank_in_tier'])
        if not tier_rs:
            continue
        print(f"\n── {tier} (n={len(tier_rs)}) ──")
        print(f"  {'#':>2}  {'case_id':<35}  {'grade':>4}  {'score':>6}  "
              f"{'mode':>9}  {'AM:SE':>8}  {'wt%':>5}  {'T(μm)':>6}  "
              f"{'σ_i':>6}  {'ASR':>6}  {'Q_v':>5}")
        for r in tier_rs:
            uc = ' 🧫' if r['is_unit_cell'] else ''
            print(f"  {r['rank_in_tier']:>2}  {r['case_id'][:35]:<35}  "
                  f"{r['grade']:>4}  {r['score']:>6.1f}  {r['mode']:>9}  "
                  f"{str(r['am_se'])[:8]:>8}  {(r['wt_am'] or 0):>5.1f}  "
                  f"{(r['thickness'] or 0):>6.1f}  "
                  f"{(r['sigma_ionic'] or 0):>6.3f}  "
                  f"{(r['asr_ionic'] or 0):>6.1f}  "
                  f"{(r['Q_vol'] or 0):>5.0f}{uc}")

    # Sanity checks
    print('\n' + '─' * 100)
    print('SANITY CHECKS')
    print('─' * 100)
    # 1. Bimodal commercial (82:18) cases should mostly be top half
    commercial = [r for r in results if r.get('wt_am') and 78 <= r['wt_am'] <= 88]
    print(f'  Commercial composition (78-88% AM): {len(commercial)} cases, '
          f'median rank #{sorted(r["rank"] for r in commercial)[len(commercial)//2] if commercial else "—"}')
    # 2. SE-rich (62:38) should be lower
    se_rich = [r for r in results if r.get('wt_am') and r['wt_am'] < 70]
    print(f'  SE-rich (<70% AM): {len(se_rich)} cases, '
          f'median rank #{sorted(r["rank"] for r in se_rich)[len(se_rich)//2] if se_rich else "—"}')
    # 3. Mono cathodes
    mono = [r for r in results if r['mode'] == 'standard']
    bimodal = [r for r in results if r['mode'] == 'bimodal']
    if mono and bimodal:
        med_m = sorted(r['score'] for r in mono if r['score'])[len(mono)//2]
        med_b = sorted(r['score'] for r in bimodal if r['score'])[len(bimodal)//2]
        print(f'  bimodal (n={len(bimodal)}) median score: {med_b:.1f}')
        print(f'  mono    (n={len(mono)})    median score: {med_m:.1f}')


if __name__ == '__main__':
    main()
