#!/usr/bin/env python3
"""Per-page Origin CSVs for the 2026-10-13 cascade progress briefing (one file per data graphic).

Writes db/properties/seminar_2026_10_13_cascade/pNN_*.csv + README.md. Page numbers follow
Research_Seminar_2026_10_13_cascade_progress.pptx (19 slides — the September-audit slide is page 11).
Coverage counts (p06, p07) are counted from the ledgers themselves, not typed in.

What it does NOT do: it does not digitize literature figures (Kang 2026, Sundar 2025, Jung 2026 —
literature values never sit beside ours); it does not export the bond-valence landscape (volumetric
.cube data); it cannot give the raw E–V points of the two DFT EOS curves (they were never copied into
the repo — eos.json only names container paths), so p09 holds the Birch–Murnaghan fit curves only.
It writes no transport value (no D, ratio or Ea) — p13 is run status and wall-clock cost only.
It does not decide which ledger is "the" species count — p07 lists each ledger with its own count.

  python3 kb/seminars/export_cascade_briefing_csvs_2026_10.py            # write
  python3 kb/seminars/export_cascade_briefing_csvs_2026_10.py --selftest
"""
import csv, json, os, re, sys

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


ANION_FAMILY = {'O': 'oxides', 'Cl': 'chlorides', 'S': 'sulfides', 'F': 'fluorides', 'Br': 'bromides', 'N': 'nitrides', 'I': 'iodides'}
MAIN_FAMILIES = ('multi_category_2026_05_26_v23', 'as2s3_recover')   # x = 0.25 set; dualx_v23 is a separate concentration set


def anion_family(formula):
    """Anion family of a binary precursor ('Al2O3' -> 'oxides'). Raises unless exactly one anion element."""
    an = {el for el in re.findall(r'[A-Z][a-z]?', formula) if el in ANION_FAMILY}
    if len(an) != 1:
        raise ValueError(f'{formula}: expected one anion element, found {sorted(an)}')
    return ANION_FAMILY[an.pop()]


def base(name):
    return name.replace('+Clrich', '')


def assert_subset(label, sp, allsp):
    """A ledger may hold fewer precursors than the 91, never an unknown one (that would be a naming split)."""
    extra = set(sp) - set(allsp)
    if extra:
        raise ValueError(f'{label}: species not in the 91 relaxed set: {sorted(extra)}')


def stage1_rows():
    with open(os.path.join(P, 'cascade_all_302_2026_08_25.csv'), encoding='utf-8') as f:
        return [r for r in csv.DictReader(f)]


def ledger_species():
    """Species set of every Stage-1 ledger, read from the ledger files (no typed-in counts)."""
    allr = stage1_rows()
    main = [r for r in allr if r['family'] in MAIN_FAMILIES]
    dualx = [r for r in allr if r['family'] == 'dualx_v23']
    esw = json.load(open(os.path.join(P, 'oxidation_stability_cascade_v3_pinned.json')))['results']
    jl = lambda f: [json.loads(x) for x in open(os.path.join(P, f), encoding='utf-8') if x.strip()]
    i90, ili, icb = jl('cascade_interface_90.jsonl'), jl('cascade_interface_li.jsonl'), jl('cascade_interface_carbon.jsonl')
    sep = rows_of(os.path.join(P, 'cascade_stability_axes.csv'))
    funnel = json.load(open(os.path.join(P, 'cascade_screening_funnel_v2.json')))['pool_names']
    return {
        'main': ({base(r['dopant']) for r in main}, len(main)),
        'annealed': ({base(r['dopant']) for r in main if r['anneal_converged'] == 'True'},
                     sum(r['anneal_converged'] == 'True' for r in main)),
        'dualx': ({base(r['dopant']) for r in dualx}, len(dualx)),
        'esw': ({v['dopant_base'] for v in esw.values() if v.get('dopant_base')}, len(esw)),
        'iface_cathode': ({r['species'] for r in i90}, len(i90)),
        'iface_li': ({r['species'] for r in ili}, len(ili)),
        'iface_carbon': ({r['species'] for r in icb}, len(icb)),
        'separate_phase': ({r[0] for r in sep[1:]}, len(sep) - 1),
        'gate_eval': (set(funnel), len(funnel)),
    }


def p06():
    rs = rows_of(os.path.join(P, 'cascade_pool_accounting.csv'))
    head, body = rs[0], [r for r in rs[1:] if r[0] != 'TOTAL']
    i = {k: head.index(k) for k in head}
    led = ledger_species()
    relaxed, gate = led['main'][0], led['gate_eval'][0]
    planned = {r[i['anion_family']]: int(r[i['n_planned']]) for r in body}
    assert sum(planned.values()) == len(relaxed) == 91, (sum(planned.values()), len(relaxed))
    note = {'As2S3': 'relaxed in the August re-run (08-20~25, valence table fixed); not yet in the stability, interface or gate tables',
            'AlI3': 'relaxed; rank-1 configuration lacks elastic/EOS/bond-valence descriptors — using rank 2 is an open decision'}
    rows = []
    for fam, n_pl in planned.items():
        sp_rel = sorted(x for x in relaxed if anion_family(x) == fam)
        miss = [x for x in sp_rel if x not in gate]
        assert len(sp_rel) == n_pl, (fam, len(sp_rel), n_pl)
        rows.append([fam, n_pl, len(sp_rel), len(sp_rel) - len(miss), ' | '.join(miss), ' | '.join(note[x] for x in miss)])
    return write('p06_candidate_set_by_anion_family.csv',
                 ['Page 6 — candidate set by anion family (bar chart: n_planned vs n_relaxed vs n_gate_evaluation).',
                  'Sources: cascade_pool_accounting.csv (plan) · cascade_all_302_2026_08_25.csv main x = 0.25 set incl. the August re-run (relaxed) · '
                  'cascade_screening_funnel_v2.json pool_names (gate evaluation, diagnostic).',
                  'All 91 planned precursors are relaxed. The gate evaluation (89) predates the re-run; see p07 for every ledger.'],
                 ['anion_family', 'n_planned', 'n_relaxed', 'n_gate_evaluation', 'not_in_gate_evaluation', 'note'], rows)


def p07():
    led = ledger_species()
    allsp = led['main'][0]
    steps = [('main', '1-2', 'Site enumeration + MLIP relaxation (main batch + August re-run)', 'cascade_all_302_2026_08_25.csv (families v23 + as2s3_recover)', 'configurations'),
             ('annealed', '3', 'Short anneal 500 K / 50 ps (converged)', 'cascade_all_302_2026_08_25.csv anneal_converged', 'configurations'),
             ('esw', '6', 'Stability window (grand potential, corrected definition)', 'oxidation_stability_cascade_v3_pinned.json results', 'compositions'),
             ('iface_cathode', '7', 'Interface: doped composition vs LiCoO2 / LiNiO2 / LiMn2O4 (+ NCM811 and Li-metal subsets of 8)', 'cascade_interface_90.jsonl', 'reaction rows'),
             ('iface_li', '7', 'Interface: doped composition vs Li metal', 'cascade_interface_li.jsonl', 'reaction rows'),
             ('iface_carbon', '7', 'Interface: doped composition vs carbon', 'cascade_interface_carbon.jsonl', 'reaction rows'),
             ('separate_phase', '— (slide 10 text)', 'Precursor as a separate phase (coating view) vs H2O (H2S release), LiCoO2, Li6PS5Cl, Li metal, LiNiO2', 'cascade_stability_axes.csv', 'precursors'),
             ('gate_eval', '— (not on slides)', 'Literature-style gate funnel (diagnostic, unvalidated)', 'cascade_screening_funnel_v2.json pool_names', 'precursors'),
             ('dualx', '— (not on slides)', 'Concentration set x = 0.0625 / 0.25 in a 16 f.u. cell (exploratory, incomplete)', 'cascade_all_302_2026_08_25.csv family dualx_v23', 'configurations')]
    rows = []
    for key, row_no, what, src, unit in steps:
        sp, n = led[key]
        assert_subset(key, sp, allsp)
        rows.append([row_no, what, len(sp), n, unit, 'yes' if 'As2S3' in sp else 'no', 'yes' if 'AlI3' in sp else 'no', src])
    return write('p07_stage1_coverage_by_ledger.csv',
                 ['Page 7 — Stage-1 coverage: how many of the 91 precursors each ledger holds (table or bars: n_precursors per step).',
                  'Counted from the ledger files by this script. Stage 1 is exploratory data since 2026-09-19 (cascade_v23_demoted_2026_09_19.json).',
                  'Configurations are structures, not designs; all main-set configurations share one dopant level (labels x002/x005/x010 are not concentrations).'],
                 ['workflow_row', 'step_or_ledger', 'n_precursors', 'n_rows', 'row_unit', 'As2S3_included', 'AlI3_included', 'source'], rows)


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


def p13():
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
    write('p13_md_campaign_runs.csv',
          [f'Page 13 — MLIP-MD run roster (40 runs = 10 start configurations × 2 precursors × 2 seeds), status as of {AS_OF}.',
           'Source: db/properties/cascade_v7_main_runlog_2026_10_07.json (per-run wall-clock GPU-hours of finished runs).',
           'NO transport values here (no D, ratio or Ea) — the ratio is analysed once, after all 40 runs.',
           'Run order assumption: seed 1 for A–J first (the 13th run was P1_Al2O3_G seed 1); queued order is not asserted.'],
          ['precursor', 'start_configuration', 'seed', 'status', 'wall_GPU_h'], rows)
    summ = [['runs', 12, 40, 'runs'],
            ['GPU-hours used (incl. 6.8444 for the run lost in the 10-12 reboot)', 101.10, 461.4, 'GPU-h (cap)']]
    return write('p13_md_campaign_progress.csv',
                 [f'Page 13 — progress bars, as of {AS_OF}. Update before the talk with the runner watch.',
                  'Source: cascade_v7_main_runlog_2026_10_07.json ✅_재개 (101.10) · decision D-2026-10-07-cascade-v7-main-round-cap (461.4).'],
                 ['metric', 'value', 'total', 'unit'], summ)


def p18():
    src = os.path.join(P, 'seminar_table_site_preference.csv')
    rs = rows_of(src)
    return write('p18_site_preference_vs_ionic_radius.csv',
                 ['Page 18 (backup) — site preference vs Shannon ionic radius (MLIP relative energies).',
                  'This is the June site-preference batch (antisite swap), NOT the Stage-1 cascade set whose x labels were all x = 0.25.',
                  'Source: db/properties/seminar_table_site_preference.csv — its notes, verbatim:']
                 + comments_of(src), rs[0], rs[1:])


# ---------------------------------------------------------------- deck figures (--figures)
# Preview figures for the slim deck, drawn from the CSVs above (house style, English labels).
# They are stand-ins until the Origin versions exist; p12 is a schematic and carries no data.
ASSETS = os.path.join(ROOT, 'kb', 'seminars', 'assets_2026_10_13')
ROSTER_STATUS = ('done', 'running', 'queued')


def structures_by_family():
    """Stage-1 main set (x = 0.25, incl. the August re-run): relaxed and annealed structures per anion family."""
    fam_rows = {}
    for r in stage1_rows():
        if r['family'] not in MAIN_FAMILIES:
            continue
        f = anion_family(base(r['dopant']))
        rel, ann = fam_rows.get(f, (0, 0))
        fam_rows[f] = (rel + 1, ann + (r['anneal_converged'] == 'True'))
    return fam_rows


def p07b():
    fam = structures_by_family()
    order = ['oxides', 'chlorides', 'sulfides', 'fluorides', 'bromides', 'nitrides', 'iodides']
    assert set(fam) == set(order), sorted(fam)
    rows = [[f, fam[f][0], fam[f][1]] for f in order]
    assert sum(r[1] for r in rows) == 3675 and sum(r[2] for r in rows) == 693, rows
    return write('p07_structures_by_anion_family.csv',
                 ['Page 7 (slim deck figure, left panel) — Stage-1 structures per anion family: relaxed vs annealed (500 K, 50 ps).',
                  'Source: cascade_all_302_2026_08_25.csv, main x = 0.25 set incl. the August re-run (families v23 + as2s3_recover).',
                  'Structures (configurations), not designs; all at one dopant level.'],
                 ['anion_family', 'n_relaxed_structures', 'n_annealed_structures'], rows)


def roster_matrix(rows):
    """40-run roster -> {(row_label, start_configuration): status}. Raises on an unknown status or a duplicate cell."""
    grid = {}
    for prec, parent, seed, status, _ in rows:
        if status.split(' ')[0] not in ROSTER_STATUS:
            raise ValueError(f'unknown run status: {status!r}')
        key = (f"{'Al₂O₃' if prec.startswith('Al2O3') else 'Al₂S₃'} · seed {seed}", parent)
        if key in grid:
            raise ValueError(f'duplicate roster cell: {key}')
        grid[key] = status.split(' ')[0]
    return grid


# Literature figures used on the slim deck as the reason for a method choice — cropped from the litdb
# figure crops (litdb/figures/<slug>/), never redrawn and never mixed with our numbers.
LIT_CROPS = [  # (slug, file, crop box in px or None, output name, why)
    ('jung2026_sio2_cosubstitution_mechanical_argyrodite', 'fig_3.png', (40, 585, 2170, 1140), 'lit_jung2026_sio2_fig3d.png',
     'p06: one precursor (SiO2) co-substitution, cycling over 500 cycles'),
    ('schwietert2021_intrinsic_vs_decomposition_window_sse', 'fig_1.png', None, 'lit_schwietert2021_fig1.png',
     'p10: decomposition vs intrinsic stability window'),
    ('he2018_statistical_variances_diffusional_aimd', 'fig_3.png', (200, 0, 1990, 704), 'lit_he2018_fig3.png',
     'p12: MSD spread over ten independent AIMD runs of one structure'),
    ('phuthi2026_mlip_ssb_perspective', 'fig_1.png', (150, 0, 1065, 765), 'lit_phuthi2026_fig1a.png',
     'p14: length and time scales needed for bulk ion transport'),
]


def lit_crops():
    from PIL import Image
    made = []
    for slug, fname, box_, out, _ in LIT_CROPS:
        im = Image.open(os.path.join(ROOT, 'litdb', 'figures', slug, fname))
        if box_:
            x0, y0, x1, y1 = box_
            if not (0 <= x0 < x1 <= im.width and 0 <= y0 < y1 <= im.height):
                raise ValueError(f'{slug}/{fname}: crop {box_} outside {im.size}')
            im = im.crop(box_)
        dst = os.path.join(ASSETS, out)
        im.save(dst)
        made.append(dst)
    return made


def origin_axes(ax, frame=True):
    """Plain Origin-like axes: black frame, inward ticks on all sides (the user's Origin graphs replace these)."""
    for sp_ in ax.spines.values():
        sp_.set_visible(frame)
        sp_.set_color('black')
        sp_.set_linewidth(1.0)
    ax.tick_params(direction='in', top=frame, right=frame, colors='black', length=4, width=1, labelsize=9.5)
    return ax


def plain_axes(ax, size=11):
    """Left and bottom axes only (house style: no top/right frame — CW P1 read the four-sided frame as a matplotlib
    default), inward ticks; for the bar previews drawn at slide size."""
    for k in ('top', 'right'):
        ax.spines[k].set_visible(False)
    for k in ('left', 'bottom'):
        ax.spines[k].set_color('black')
        ax.spines[k].set_linewidth(1.0)
    ax.tick_params(direction='in', colors='black', length=4, width=1, labelsize=size)
    return ax


def figures():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch, Rectangle
    plt.rcParams.update({'font.family': 'Liberation Sans', 'font.size': 10, 'axes.labelsize': 10.5})
    os.makedirs(ASSETS, exist_ok=True)
    made = []
    GREY, DARK = '#bdbdbd', '#404040'

    def save(fig, name):
        out = os.path.join(ASSETS, name)
        fig.tight_layout()
        fig.savefig(out, dpi=300)
        plt.close(fig)
        made.append(out)

    # p06: precursors per anion family — horizontal bars drawn at the slide size (3.65 × 2.9 in), so a 13 pt label
    # here is 13 pt on the slide (CW P1: names were tilted and small); family order kept top → bottom
    fam6 = rows_of(os.path.join(OUT, 'p06_candidate_set_by_anion_family.csv'))[1:]
    fig, ax = plt.subplots(figsize=(3.65, 2.9))
    ys = list(range(len(fam6)))[::-1]
    vals = [int(r[1]) for r in fam6]
    ax.barh(ys, vals, 0.62, color=GREY, edgecolor='black', linewidth=0.8)
    for y, v in zip(ys, vals):
        ax.text(v + 0.8, y, str(v), va='center', fontsize=14)
    ax.set_yticks(ys, [r[0] for r in fam6], fontsize=13)
    ax.set_xlim(0, max(vals) * 1.2)
    ax.set_xlabel('precursors', fontsize=12)
    plain_axes(ax)
    ax.tick_params(axis='y', length=0)
    save(fig, 'fig_p06_candidates_by_family.png')

    # p07: precursors held by each Stage-1 table — one panel at the slide size (8.0 × 3.05 in; CW P1: the per-family
    # structure counts repeated p06 and are now a line of text; their CSV stays for Origin)
    cov = rows_of(os.path.join(OUT, 'p07_stage1_coverage_by_ledger.csv'))
    head = cov[0]
    i = {k: head.index(k) for k in head}
    keep = [r for r in cov[1:] if not r[i['step_or_ledger']].startswith('Concentration set')]
    short = [('Site enumeration', 'relaxed'), ('Short anneal', 'annealed'), ('Stability window', 'stability window'),
             ('Interface: doped composition vs LiCoO2', 'interface vs cathodes'), ('Interface: doped composition vs Li metal', 'interface vs Li'),
             ('Interface: doped composition vs carbon', 'interface vs C'), ('Precursor as a separate phase', 'separate phase'),
             ('Literature-style gate funnel', 'gate funnel')]
    lab = [next(v for k, v in short if r[i['step_or_ledger']].startswith(k)) for r in keep]
    n = [int(r[i['n_precursors']]) for r in keep]
    miss = [', '.join(sp for sp, col in (('As$_2$S$_3$', 'As2S3_included'), ('AlI$_3$', 'AlI3_included')) if r[i[col]] == 'no') for r in keep]
    fig, ax = plt.subplots(figsize=(8.0, 3.05))
    ys = list(range(len(lab)))[::-1]
    ax.barh(ys, n, 0.62, color=GREY, edgecolor='black', linewidth=0.8)
    for y, v, m in zip(ys, n, miss):
        ax.text(v + 1.5, y, f'{v}', va='center', fontsize=14)
        if m:
            ax.text(v + 9, y, f'(no {m})', va='center', fontsize=12.5, color='#4b5563')
    ax.set_yticks(ys, lab, fontsize=14)
    ax.set_xlim(0, 150)
    ax.set_xticks([0, 30, 60, 91])
    ax.set_xlabel('precursors (of 91)', fontsize=13)
    plain_axes(ax, 12)
    ax.spines['bottom'].set_bounds(0, 91)        # the axis stops at 91; the room to its right is for the notes
    ax.tick_params(axis='y', length=0)
    save(fig, 'fig_p07_stage1_coverage.png')

    # p10: host stability window on a voltage axis
    seg = rows_of(os.path.join(OUT, 'p10_stability_window_host_segments.csv'))[1:]
    lo, hi = float(seg[1][1]), float(seg[1][2])
    fig, ax = plt.subplots(figsize=(4.4, 1.9))
    ax.axvspan(lo, hi, color='#d9d9d9')
    for v in (lo, hi):
        ax.axvline(v, color='black', ls='--', lw=1)
        ax.text(v, 1.03, f'{v:.3f} V', ha='center', va='bottom', fontsize=9)
    ax.text((1.4 + lo) / 2, 0.5, 'Li uptake', ha='center', va='center', fontsize=9)
    ax.text((lo + hi) / 2, 0.5, 'no Li\nexchange', ha='center', va='center', fontsize=9)
    ax.text((hi + 2.5) / 2, 0.5, 'Li release', ha='center', va='center', fontsize=9)
    ax.set_xlim(1.4, 2.5)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xlabel('voltage vs Li/Li$^+$ (V)')
    origin_axes(ax)
    ax.tick_params(left=False, right=False)
    save(fig, 'fig_p10_host_window.png')

    # p13: 40-run roster status
    runs = rows_of(os.path.join(OUT, 'p13_md_campaign_runs.csv'))[1:]
    grid = roster_matrix(runs)
    rows_ = ['Al₂O₃ · seed 1', 'Al₂S₃ · seed 1', 'Al₂O₃ · seed 2', 'Al₂S₃ · seed 2']
    cols = list('ABCDEFGHIJ')
    style = {'done': ('black', 'black'), 'running': ('#9e9e9e', 'black'), 'queued': ('white', '#9e9e9e')}
    fig, ax = plt.subplots(figsize=(4.4, 2.25))
    for yi, rname in enumerate(rows_):
        for xi, c in enumerate(cols):
            fc, ec = style[grid[(rname, c)]]
            ax.add_patch(Rectangle((xi + 0.12, 3 - yi + 0.14), 0.76, 0.72, facecolor=fc, edgecolor=ec, linewidth=0.8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.set_xticks([k + 0.5 for k in range(10)], cols)
    ax.set_yticks([3.5 - k for k in range(4)], rows_, fontsize=9)
    ax.set_xlabel('start configuration')
    origin_axes(ax)
    ax.tick_params(length=0)
    counts = {k: sum(v == k for v in grid.values()) for k in ROSTER_STATUS}
    ax.legend(handles=[Patch(facecolor=style[k][0], edgecolor=style[k][1], label=f'{k} ({counts[k]})') for k in ROSTER_STATUS],
              frameon=False, fontsize=8.5, ncol=3, loc='lower center', bbox_to_anchor=(0.45, 1.0))
    save(fig, 'fig_p13_run_roster.png')

    for stale in ('fig_p12_msd_check_schematic.png',        # replaced by He et al. 2018 Fig. 3 (lit_he2018_fig3.png)
                  'fig_p07_stage1_scale_coverage.png'):     # two panels → fig_p07_stage1_coverage.png (CW, 10-13)
        if os.path.exists(os.path.join(ASSETS, stale)):
            os.remove(os.path.join(ASSETS, stale))
    return made + lit_crops()

README = """# Origin CSVs — Research Seminar 2026-10-13 (cascade progress briefing)

Decks: `kb/seminars/Research_Seminar_2026_10_13_cascade_progress.pptx` (19 slides) and the lean variant
`…_progress_lean.pptx` (same 19 slides, same order, same page numbers — every CSV below fits both).
Made by `kb/seminars/export_cascade_briefing_csvs_2026_10.py` — rerun it after the source files change.
Every CSV starts with `#` comment lines (source, units, cautions); Origin: Import → skip comment lines.
2026-10-12 update: the September-audit slide became page 11, so the MD-status CSV is now p13 and the
site-preference backup p18 (old p12 / p17 files are removed by the script). p06 and p07 count from the ledgers.

| page | slide | CSV | what to plot |
|---|---|---|---|
| 6 | Candidate set | `p06_candidate_set_by_anion_family.csv` | bars: n_planned vs n_relaxed vs n_gate_evaluation per anion family |
| 7 | Stage-1 coverage | `p07_stage1_coverage_by_ledger.csv` · `p07_structures_by_anion_family.csv` | bars: precursors held by each Stage-1 table (As2S3 / AlI3 flags); the per-family structure counts (relaxed 3,675 vs annealed 693) are a text line on the slim deck since 10-13 |
| 8 | Configuration sampling | `p08_configurations_per_site_pair_long.csv` · `_matrix.csv` | heat map: cation site × anion site → configurations (main batch 3,615) |
| 9 | DFT EOS | `p09_eos_bm3_fit_curves.csv` | lines: E − E0 vs V per f.u. (fit curves; raw points not in repo) |
| 10 | Stability window | `p10_stability_window_host.csv` · `p10_stability_window_host_segments.csv` | bar segments on a voltage axis (host Li6PS5Cl) |
| 13 | MD status | `p13_md_campaign_progress.csv` · `p13_md_campaign_runs.csv` | progress bars; run roster (status, wall-clock GPU-h) |
| 18 | Backup: site preference | `p18_site_preference_vs_ionic_radius.csv` | ΔE vs Shannon radius, three loadings per element (June batch, not Stage 1) |

Slim-deck figures (`--figures`) in `kb/seminars/assets_2026_10_13/`: plain previews drawn from the CSVs here (`fig_p07_stage1_coverage.png` · `fig_p10_host_window.png` · `fig_p13_run_roster.png`; p07 is drawn at the size it takes on the slide, so its font sizes are the slide's — since 10-13 p06 shows the 08-18 family table instead, and `fig_p06_candidates_by_family.png` stays only as an Origin option) — replace them with the Origin versions — and literature figures cropped from the litdb crops as the reason for a method choice (`lit_jung2026_sio2_fig3d.png` p06 · `lit_schwietert2021_fig1.png` p10 · `lit_he2018_fig3.png` p12 · `lit_phuthi2026_fig1a.png` p14; never redrawn, never on the same plot as our numbers).

Pages without a CSV:
- 2 (previous DFT work): figure boxes left empty on purpose — fill per tile on request.
- 3, 11, 14, 15 (cards) · 5, 12 (tables, text in the slide) · 1, 16, 17 (title, thanks, references).
- 4 (Kang 2026), 10 right (Sundar 2025 Fig. 2), 13 right (Jung 2026 Fig. 5b): literature figures — not digitized; literature values never go on the same plot as ours.
- 19 (bond-valence landscape): volumetric data (.cube) — not converted.

Value discipline: no transport value (D, ratio, Ea) is in any file here; the stability window is the corrected definition only;
B0 values are canonical DFT (compare per f.u. only); Stage-1 counts are exploratory-data coverage, not a ranking.
"""


def main():
    for old in ('p12_md_campaign_runs.csv', 'p12_md_campaign_progress.csv', 'p17_site_preference_vs_ionic_radius.csv'):
        if os.path.exists(os.path.join(OUT, old)):      # renamed when the audit slide became page 11
            os.remove(os.path.join(OUT, old))
    made = [p06(), p07(), p07b(), p08(), p09(), p10(), p13(), p18()]
    with open(os.path.join(OUT, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(README)
    print('wrote', len(os.listdir(OUT)), 'files to', os.path.relpath(OUT, ROOT))
    if '--figures' in sys.argv:
        for f in figures():
            print('figure', os.path.relpath(f, ROOT))


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
    # anion family: positive and negative paths
    assert anion_family('Al2O3') == 'oxides' and anion_family('Ca3N2') == 'nitrides' and anion_family('LiCl') == 'chlorides'; ok += 1
    for bad in ('LiClO4', 'NaK'):          # two anions / no anion must be refused, not guessed
        try:
            anion_family(bad)
        except ValueError:
            ok += 1
        else:
            raise AssertionError(f'anion_family accepted {bad}')
    # negative: a ledger species outside the 91 (e.g. a renamed 'As2S3_recov') must be refused
    try:
        assert_subset('test', {'As2S3_recov', 'Al2O3'}, {'Al2O3', 'As2S3'})
    except ValueError:
        ok += 1
    else:
        raise AssertionError('assert_subset accepted an unknown species')
    assert_subset('test', {'Al2O3'}, {'Al2O3', 'As2S3'}); ok += 1
    # roster grid: positive, then an unknown status and a duplicate cell must be refused
    good = [['Al2O3-derived', 'A', '1', 'done', '5.9'], ['Al2S3-derived', 'A', '1', 'running (restarted)', '']]
    assert roster_matrix(good) == {('Al₂O₃ · seed 1', 'A'): 'done', ('Al₂S₃ · seed 1', 'A'): 'running'}; ok += 1
    for bad in ([['Al2O3-derived', 'A', '1', 'finished', '']], good + [['Al2O3-derived', 'A', '1', 'queued', '']]):
        try:
            roster_matrix(bad)
        except ValueError:
            ok += 1
        else:
            raise AssertionError(f'roster_matrix accepted {bad}')
    # negative: a literature crop box outside the image must be refused
    saved = LIT_CROPS[:]
    try:
        LIT_CROPS[:] = [('he2018_statistical_variances_diffusional_aimd', 'fig_3.png', (0, 0, 99999, 10), 'x.png', '')]
        try:
            lit_crops()
        except ValueError:
            ok += 1
        else:
            raise AssertionError('lit_crops accepted a box outside the image')
    finally:
        LIT_CROPS[:] = saved
    print(f'selftest PASS ({ok})')


if __name__ == '__main__':
    selftest() if '--selftest' in sys.argv else main()
