#!/usr/bin/env python3
"""Per-page Origin CSVs for the 2026-10-13 cascade progress briefing (one file per data graphic).

Writes db/properties/seminar_2026_10_13_cascade/pNN_*.csv + README.md. Page numbers follow
Research_Seminar_2026_10_13_cascade_progress.pptx (18 slides).

What it does NOT do: it does not digitize literature figures (Kang 2026, Sundar 2025, Jung 2026 —
literature values never sit beside ours); it does not export the bond-valence landscape (volumetric
.cube data); it cannot give the raw E–V points of the two DFT EOS curves (they were never copied into
the repo — eos.json only names container paths), so p09 holds the Birch–Murnaghan fit curves only.
It writes no transport value (no D, ratio or Ea) — p12 is run status and wall-clock cost only.

  python3 kb/seminars/export_cascade_briefing_csvs_2026_10.py            # write
  python3 kb/seminars/export_cascade_briefing_csvs_2026_10.py --selftest
"""
import csv, json, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
P = os.path.join(ROOT, 'db', 'properties')
OUT = os.path.join(P, 'seminar_2026_10_13_cascade')
EV_PER_A3_PER_GPA = 1 / 160.21766208
AS_OF = '2026-10-12 10:04 KST (last runner watch)'


def rows_of(path):
    """CSV rows, skipping comment lines (first cell starting with '#')."""
    with open(path, encoding='utf-8') as f:
        return [r for r in csv.reader(f) if r and not r[0].lstrip('"').startswith('#')]


def comments_of(path):
    with open(path, encoding='utf-8') as f:
        return [line.rstrip('\n').strip('"').rstrip(',').rstrip('"') for line in f if line.lstrip('"').startswith('#')]


def write(name, header_lines, cols, rows):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), 'w', encoding='utf-8', newline='') as f:
        for h in header_lines:
            f.write(h if h.startswith('#') else '# ' + h)
            f.write('\n')
        w = csv.writer(f)
        w.writerow(cols)
        w.writerows(rows)
    return name


def bm3(v, v0, b0_gpa, bp):
    """Birch–Murnaghan 3rd-order E(V) − E0 (eV); V, V0 in Å³."""
    b0 = b0_gpa * EV_PER_A3_PER_GPA
    eta = (v0 / v) ** (2.0 / 3.0)
    return 9.0 * v0 * b0 / 16.0 * ((eta - 1) ** 3 * bp + (eta - 1) ** 2 * (6 - 4 * eta))


def p06():
    rs = rows_of(os.path.join(P, 'cascade_pool_accounting.csv'))
    head, body = rs[0], [r for r in rs[1:] if r[0] != 'TOTAL']
    i = {k: head.index(k) for k in head}
    rows = [[r[i['anion_family']], r[i['n_planned']], r[i['n_scored']], r[i['dropped_species']], r[i['drop_reason']]] for r in body]
    return write('p06_candidate_set_by_anion_family.csv',
                 ['Page 6 — candidate set by anion family (bar chart: n_planned vs n_computed).',
                  'Source: db/properties/cascade_pool_accounting.csv (91 planned → 89 computed).',
                  'not_computed: As2S3 = no valid configuration generated; AlI3 = descriptor set incomplete on its top row.'],
                 ['anion_family', 'n_planned', 'n_computed', 'not_computed_species', 'reason'], rows)


def p08():
    rs = rows_of(os.path.join(P, 'seminar_table_site_grid.csv'))
    head = rs[0]
    anions = head[1:4]
    long, matrix = [], []
    total = None
    for r in rs[1:]:
        if r[0] == 'column_total':
            total = int(r[4])
            continue
        matrix.append([r[0]] + r[1:4])
        for a, n in zip(anions, r[1:4]):
            long.append([r[0], a, int(n)])
    assert total == sum(n for *_, n in long) == 3615, total
    for row in long:
        row.append(round(100 * row[2] / total, 1))
    write('p08_configurations_per_site_pair_long.csv',
          ['Page 8 — configurations generated per (cation site, anion site) pair; long format (Origin heat map: X, Y, Z).',
           'Source: db/properties/seminar_table_site_grid.csv (from cascade_v23_all.csv, 3,615 configurations).',
           'Counts are CONFIGURATIONS, not compounds; all at one dopant concentration. All nine pairs populated.'],
          ['cation_site', 'anion_site', 'n_configurations', 'percent_of_all'], long)
    return write('p08_configurations_per_site_pair_matrix.csv',
                 ['Page 8 — same counts as a 3x3 matrix (rows = cation site, columns = anion site).',
                  'Source: db/properties/seminar_table_site_grid.csv.'],
                 ['cation_site'] + anions, matrix)


def p09():
    e = {r['id']: r for r in json.load(open(os.path.join(P, 'eos.json')))['results']}
    sysd = [('Li6PS5Cl', e['comp1_v3'], 4, 960.0, 1085.0), ('Li5.4PS4.4Cl1.6', e['modelc_v3'], 5, 1140.0, 1285.0)]
    n = 200
    cols, data = [], []
    for lab, r, nfu, lo, hi in sysd:
        cols += [f'{lab}_V_cell_A3', f'{lab}_V_per_fu_A3', f'{lab}_dE_fit_eV_per_cell', f'{lab}_dE_fit_meV_per_atom']
        nat = {'Li6PS5Cl': 52, 'Li5.4PS4.4Cl1.6': 62}[lab]   # modelc_v3.json atoms 62 (5 f.u.)
        col = []
        for k in range(n):
            v = lo + (hi - lo) * k / (n - 1)
            de = bm3(v, r['V0_A3'], r['B0_GPa'], r['B0_prime'])
            col.append([round(v, 4), round(v / nfu, 4), round(de, 6), round(1000 * de / nat, 4)])
        data.append(col)
    rows = [a + b for a, b in zip(*data)]
    return write('p09_eos_bm3_fit_curves.csv',
                 ['Page 9 — DFT equation of state, Birch–Murnaghan (3rd order) FIT CURVES only, as E − E0.',
                  f"Li6PS5Cl (comp1_v3): V0 = {e['comp1_v3']['V0_A3']} Å³/cell (4 f.u.), B0 = {e['comp1_v3']['B0_GPa']} GPa, B0' = {e['comp1_v3']['B0_prime']}.",
                  f"Li5.4PS4.4Cl1.6 (modelc_v3): V0 = {e['modelc_v3']['V0_A3']} Å³/cell (5 f.u.), B0 = {e['modelc_v3']['B0_GPa']} GPa (B0' not quoted — ill-constrained).",
                  'Source: db/properties/eos.json results comp1_v3 / modelc_v3 (canonical_registry b0-dft-bm3-v1).',
                  'Raw E–V points (8 and 11 DFT points) are NOT in the repo — eos.json names container paths only; the slide keeps the original figure.',
                  'Compare volumes per f.u. only (HZ-eos-v0-extensive). Atoms per cell used for meV/atom: 52 and 62.'],
                 cols, rows)


def p10():
    v = json.load(open(os.path.join(P, 'oxidation_stability_cascade_v3_pinned.json')))
    hs = v['hosts_by_phase_set']
    vals = {(h['ocv_self_decomposition_V'], h['oxidation_limit_V'], h['window_V']) for h in hs.values()}
    assert len(vals) == 1, f'host window differs across phase sets: {sorted(vals)[:4]}'
    ocv, ox, win = vals.pop()
    h = next(iter(hs.values()))
    rows = [['lower bound (decomposition without Li exchange)', ocv, h.get('ocv_rxn', '')],
            ['upper bound (oxidation onset, Li release)', ox, h.get('oxidation_onset_rxn', '')],
            ['stable window width', win, 'upper − lower']]
    seg = [['Li uptake (display range)', 1.4, ocv], ['no Li exchange', ocv, ox], ['Li release (display range)', ox, 2.5]]
    write('p10_stability_window_host_segments.csv',
          ['Page 10 — schematic bar segments; 1.4 and 2.5 V are display limits, not data.'],
          ['segment', 'V_start_vs_Li', 'V_end_vs_Li'], seg)
    return write('p10_stability_window_host.csv',
                 [f'Page 10 — Li6PS5Cl host (Li24P4S20Cl4) stability window, grand-potential phase diagram, Materials Project phases (0 K), identical in all {len(hs)} phase sets.',
                  'Source: db/properties/oxidation_stability_cascade_v3_pinned.json hosts_by_phase_set (corrected definition 2026-09-22 / 10-01).',
                  'Corrected definition: window = oxidation limit − decomposition-without-Li-exchange voltage. The legacy (wider) window is NOT in this file.'],
                 ['quantity', 'voltage_V_vs_Li', 'reaction'], rows)


def p12():
    rl = json.load(open(os.path.join(P, 'cascade_v7_main_runlog_2026_10_07.json')))
    blk = rl['⛔_kgy_재부팅_2026_10_12']
    cost = blk['런별_단가_GPU_h']
    assert len(cost) == 12, len(cost)
    prec = {'P1': 'Al2O3-derived', 'P2': 'Al2S3-derived'}
    rows = []
    for seed in (1, 2):
        for parent in 'ABCDEFGHIJ':
            for p_ in ('P1_Al2O3', 'P2_Al2S3'):
                key = f'{p_}_{parent}'
                if seed == 1 and key in cost:
                    st, gh = 'done', cost[key]
                elif seed == 1 and key == 'P1_Al2O3_G':
                    st, gh = 'running (restarted after reboot)', ''
                else:
                    st, gh = 'queued', ''
                rows.append([prec[p_[:2]], parent, seed, st, gh])
    assert sum(r[3] == 'done' for r in rows) == 12 and len(rows) == 40
    write('p12_md_campaign_runs.csv',
          [f'Page 12 — MLIP-MD run roster (40 runs = 10 start configurations × 2 precursors × 2 seeds), status as of {AS_OF}.',
           'Source: db/properties/cascade_v7_main_runlog_2026_10_07.json (per-run wall-clock GPU-hours of finished runs).',
           'NO transport values here (no D, ratio or Ea) — the ratio is analysed once, after all 40 runs.',
           'Run order assumption: seed 1 for A–J first (the 13th run was P1_Al2O3_G seed 1); queued order is not asserted.'],
          ['precursor', 'start_configuration', 'seed', 'status', 'wall_GPU_h'], rows)
    summ = [['runs', 12, 40, 'runs'],
            ['GPU-hours used (incl. 6.8444 for the run lost in the 10-12 reboot)', 101.10, 461.4, 'GPU-h (cap)']]
    return write('p12_md_campaign_progress.csv',
                 [f'Page 12 — progress bars, as of {AS_OF}. Update before the talk with the runner watch.',
                  'Source: cascade_v7_main_runlog_2026_10_07.json ✅_재개 (101.10) · decision D-2026-10-07-cascade-v7-main-round-cap (461.4).'],
                 ['metric', 'value', 'total', 'unit'], summ)


def p17():
    src = os.path.join(P, 'seminar_table_site_preference.csv')
    rs = rows_of(src)
    return write('p17_site_preference_vs_ionic_radius.csv',
                 ['Page 17 (backup) — site preference vs Shannon ionic radius (MLIP relative energies).',
                  'Source: db/properties/seminar_table_site_preference.csv — its notes, verbatim:']
                 + comments_of(src), rs[0], rs[1:])


README = """# Origin CSVs — Research Seminar 2026-10-13 (cascade progress briefing)

Deck: `kb/seminars/Research_Seminar_2026_10_13_cascade_progress.pptx` (18 slides).
Made by `kb/seminars/export_cascade_briefing_csvs_2026_10.py` — rerun it after the source files change.
Every CSV starts with `#` comment lines (source, units, cautions); Origin: Import → skip comment lines.

| page | slide | CSV | what to plot |
|---|---|---|---|
| 6 | Candidate set | `p06_candidate_set_by_anion_family.csv` | bars: n_planned vs n_computed per anion family |
| 8 | Configuration sampling | `p08_configurations_per_site_pair_long.csv` · `_matrix.csv` | heat map: cation site × anion site → configurations |
| 9 | DFT EOS | `p09_eos_bm3_fit_curves.csv` | lines: E − E0 vs V per f.u. (fit curves; raw points not in repo) |
| 10 | Stability window | `p10_stability_window_host.csv` · `p10_stability_window_host_segments.csv` | bar segments on a voltage axis (host Li6PS5Cl) |
| 12 | MD status | `p12_md_campaign_progress.csv` · `p12_md_campaign_runs.csv` | progress bars; run roster (status, wall-clock GPU-h) |
| 17 | Backup: site preference | `p17_site_preference_vs_ionic_radius.csv` | ΔE vs Shannon radius, three loadings per element |

Pages without a CSV:
- 2 (previous DFT work): figure boxes left empty on purpose — fill per tile on request.
- 3, 7, 11, 13, 14 (cards and tables), 5–6 tables (text in the slide).
- 4 (Kang 2026), 10 right (Sundar 2025 Fig. 2), 12 right (Jung 2026 Fig. 5b): literature figures — not digitized; literature values never go on the same plot as ours.
- 18 (bond-valence landscape): volumetric data (.cube) — not converted.

Value discipline: no transport value (D, ratio, Ea) is in any file here; the stability window is the corrected definition only;
B0 values are canonical DFT (compare per f.u. only).
"""


def main():
    made = [p06(), p08(), p09(), p10(), p12(), p17()]
    with open(os.path.join(OUT, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(README)
    print('wrote', len(os.listdir(OUT)), 'files to', os.path.relpath(OUT, ROOT))


def selftest():
    ok = 0
    # positive: BM3 has its minimum at V0 and is zero there
    assert abs(bm3(1016.62, 1016.62, 26.233, 4.171)) < 1e-12; ok += 1
    assert bm3(990.0, 1016.62, 26.233, 4.171) > 0 and bm3(1050.0, 1016.62, 26.233, 4.171) > 0; ok += 1
    # curvature check: B0 = V d2E/dV2 at V0 (finite difference) reproduces the input within 0.5 %
    h, v0 = 0.05, 1016.62
    d2 = (bm3(v0 + h, v0, 26.233, 4.171) - 2 * bm3(v0, v0, 26.233, 4.171) + bm3(v0 - h, v0, 26.233, 4.171)) / h ** 2
    assert abs(v0 * d2 / EV_PER_A3_PER_GPA - 26.233) / 26.233 < 0.005; ok += 1
    # negative: a wrong unit (GPa used as eV/Å³) must fail the same curvature check
    d2_bad = (bm3(v0 + h, v0, 26.233 / EV_PER_A3_PER_GPA, 4.171) - 2 * 0 + bm3(v0 - h, v0, 26.233 / EV_PER_A3_PER_GPA, 4.171)) / h ** 2
    assert abs(v0 * d2_bad / EV_PER_A3_PER_GPA - 26.233) / 26.233 > 0.5; ok += 1
    # negative: comment-skipping reader must not return '#' rows
    import tempfile
    with tempfile.NamedTemporaryFile('w', suffix='.csv', delete=False) as t:
        t.write('"# note",,\na,b\n1,2\n')
    assert rows_of(t.name) == [['a', 'b'], ['1', '2']]; ok += 1
    os.unlink(t.name)
    print(f'selftest PASS ({ok})')


if __name__ == '__main__':
    selftest() if '--selftest' in sys.argv else main()
