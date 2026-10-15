#!/usr/bin/env python3
"""Per-page Origin CSVs for the 2026-10-13 cascade progress briefing (one file per data graphic).

Writes db/properties/seminar_2026_10_13_cascade/pNN_*.csv + README.md. Page numbers follow
Research_Seminar_2026_10_13_cascade_progress.pptx as it was on 10-13 (19 slides — the audit was page 11). Since 10-14 the
audit is slide 8 and the three slides after it moved down one: p08 = slide 9 · p09 = slide 10 · p10 = slide 11 (file names kept).
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


ESW_ADDENDUM = 'oxidation_stability_cascade_as2s3_addendum_2026_10_13.json'


def ledger_species():
    """Species set of every Stage-1 ledger, read from the ledger files (no typed-in counts)."""
    allr = stage1_rows()
    main = [r for r in allr if r['family'] in MAIN_FAMILIES]
    dualx = [r for r in allr if r['family'] == 'dualx_v23']
    esw = json.load(open(os.path.join(P, 'oxidation_stability_cascade_v3_pinned.json')))['results']
    # 2026-10-14: As2S3 went into a separate addendum (same tool, same MP db 2026.04.13, host re-measured in its phase set);
    # v3_pinned stays untouched. The addendum is part of the ledger now — a missing file is an error, not a zero.
    esw_add = {k: v for k, v in json.load(open(os.path.join(P, ESW_ADDENDUM)))['results'].items()
               if not k.startswith('__HOST__')}
    jl = lambda f: [json.loads(x) for x in open(os.path.join(P, f), encoding='utf-8') if x.strip()]
    i90, ili, icb = jl('cascade_interface_90.jsonl'), jl('cascade_interface_li.jsonl'), jl('cascade_interface_carbon.jsonl')
    sep = rows_of(os.path.join(P, 'cascade_stability_axes.csv'))
    funnel = json.load(open(os.path.join(P, 'cascade_screening_funnel_v2.json')))['pool_names']
    return {
        'main': ({base(r['dopant']) for r in main}, len(main)),
        'annealed': ({base(r['dopant']) for r in main if r['anneal_converged'] == 'True'},
                     sum(r['anneal_converged'] == 'True' for r in main)),
        'dualx': ({base(r['dopant']) for r in dualx}, len(dualx)),
        'esw': ({v['dopant_base'] for v in esw.values() if v.get('dopant_base')} | {base(v['dopant']) for v in esw_add.values()},
                len(esw) + len(esw_add)),
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
    note = {'As2S3': 'relaxed in the August re-run (08-20~25, valence table fixed); added to the stability-window and interface tables on 2026-10-14; not in the gate table',
            'AlI3': 'relaxed; rank-1 configuration lacks elastic/EOS/bond-valence descriptors — rank 2 is not used (user 2026-10-14); the rank-1 descriptors wait for a free GPU'}
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
             ('esw', '6', 'Stability window (grand potential, corrected definition)', 'oxidation_stability_cascade_v3_pinned.json results + ' + ESW_ADDENDUM + ' (As2S3, 2026-10-14)', 'compositions'),
             ('iface_cathode', '7', 'Interface: doped composition vs LiCoO2 / LiNiO2 / LiMn2O4 (+ NCM811 and Li-metal subsets of 8)', 'cascade_interface_90.jsonl', 'reaction rows'),
             ('iface_li', '7', 'Interface: doped composition vs Li metal', 'cascade_interface_li.jsonl', 'reaction rows'),
             ('iface_carbon', '7', 'Interface: doped composition vs carbon', 'cascade_interface_carbon.jsonl', 'reaction rows'),
             ('separate_phase', '— (slide 10 text)', 'Precursor as a separate phase (coating view) vs H2O (H2S release), LiCoO2, Li6PS5Cl, Li metal, LiNiO2', 'cascade_stability_axes.csv', 'precursors'),
             ('gate_eval', '— (not on slides)', 'Literature-style threshold table (diagnostic, unvalidated)', 'cascade_screening_funnel_v2.json pool_names', 'precursors'),
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


# ---- p07c: the Stage-1 composite score re-run once with all 91 precursors (user 10-14: "틀린거라도 랭킹 한번 추가해서" ·
#      "점수표 관련해서는 틀린 내용이라는걸 나중에 얘기할거니까 인용해도 될듯"). The August table (cascade_v23_ranked_v2.csv)
#      holds 89: As2S3 and AlI3 came in the August re-run, after the score was made. Method unchanged — the same tool is
#      re-run, and it must first reproduce the August table byte for byte from the August inputs (else the method drifted).
SCORE_TOOL = os.path.join(ROOT, 'tools', 'figures', 'plot_cascade_insights.py')
SCORE_ADDED = ('As2S3', 'AlI3')


def _score_rows(path):
    r = rows_of(path)
    return [dict(zip(r[0], x)) for x in r[1:]]


def _run_score_tool(champ, esw, ranked, figdir):
    import subprocess
    env = dict(os.environ, CASCADE_CHAMP=champ, CASCADE_ESW=esw, CASCADE_RANKED=ranked, CASCADE_FIGDIR=figdir, MPLBACKEND='Agg')
    subprocess.run([sys.executable, SCORE_TOOL], cwd=ROOT, env=env, check=True, capture_output=True)
    return _score_rows(ranked)


def as2s3_legacy_esw(path=None):
    """As2S3 row in the OLD window definition of the v2 table: from the 10-14 addendum's legacy fields
    (first_reduction_plateau_V = old lower limit · legacy_window_V = ox − that), picked by the v2 rule
    (rebuild_pool_inputs.build_esw_csv: highest oxidation onset among plain rows, first row on a tie)."""
    res = json.load(open(path or os.path.join(P, ESW_ADDENDUM)))['results']
    best = None
    for k, v in res.items():
        if v.get('dopant') != 'As2S3' or v.get('composition_family') != 'plain' or v.get('oxidation_limit_V') is None:
            continue
        if best is None or v['oxidation_limit_V'] > best[1]['oxidation_limit_V']:
            best = (k, v)
    if best is None:
        raise ValueError('As2S3: no plain row with an oxidation limit in ' + ESW_ADDENDUM)
    k, v = best
    ox, red, win = v['oxidation_limit_V'], v['first_reduction_plateau_V'], v['legacy_window_V_2026_09_22']
    if abs((ox - red) - win) > 1e-3:
        raise ValueError(f'As2S3 {k}: legacy window {win} != ox − first plateau {ox - red:.3f}')
    return k, ox, red, v.get('ocv_self_decomposition_V'), win


def spearman(x, y):
    def rk(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        out = [0] * len(v)
        for r_, i in enumerate(order):
            out[i] = r_ + 1
        return out
    a, b, n = rk(x), rk(y), len(x)
    return 1 - 6 * sum((p - q) ** 2 for p, q in zip(a, b)) / (n * (n * n - 1))


def p07c():
    import tempfile
    tmp = tempfile.mkdtemp(prefix='score91_')
    v2c, v2e = os.path.join(P, 'cascade_v23_champions_v2.csv'), os.path.join(P, 'oxidation_stability_cascade_v2.csv')
    aug_path = os.path.join(P, 'cascade_v23_ranked_v2.csv')
    body = lambda p: [l for l in open(p, encoding='utf-8') if not l.lstrip('"').startswith('#')]
    _run_score_tool(v2c, v2e, os.path.join(tmp, 'repro89.csv'), tmp)
    if body(os.path.join(tmp, 'repro89.csv')) != body(aug_path):
        raise AssertionError('the score tool no longer reproduces cascade_v23_ranked_v2.csv from its inputs — method drifted')
    with open(v2c, encoding='utf-8') as f:
        champ = list(csv.DictReader(f))
    cols = list(champ[0].keys())
    master1 = [r for r in stage1_rows() if r['family'] in MAIN_FAMILIES and str(r.get('rank_combined', '')).strip() == '1']
    # how far the August champion rows are from today's master rank-1 rows (reported, not refreshed — refreshing them
    # would make a different ranking, not "the August ranking with the two missing ones added")
    def num(s, nd):
        try:
            return round(float(s), nd)
        except (TypeError, ValueError):
            return None
    # rounded numbers, not string prefixes: the two files print the same value with different digits ('40.831' · '40.83098')
    key = lambda r: (num(r.get('elastic_E_young_GPa'), 2), num(r.get('rerank_de_post_anneal'), 3))
    ca, ma = {}, {}
    for r in champ:
        ca.setdefault(base(r['dopant']), set()).add(key(r))
    for r in master1:
        ma.setdefault(base(r['dopant']), set()).add(key(r))
    n_diff = sum(1 for d in ca if d not in SCORE_ADDED and ca[d] != ma.get(d))
    n_cmp = sum(1 for d in ca if d not in SCORE_ADDED)
    keep = [r for r in champ if base(r['dopant']) not in SCORE_ADDED]
    add = []
    for r in master1:
        if base(r['dopant']) in SCORE_ADDED:
            o = {c: r.get(c, '') for c in cols}
            o['_dir'] = r['name']
            add.append(o)
    cc = os.path.join(tmp, 'champ91.csv')
    with open(cc, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(keep + add)
    k, ox, red, ocv, win = as2s3_legacy_esw()
    ce = os.path.join(tmp, 'esw91.csv')
    with open(ce, 'w', encoding='utf-8') as f:
        f.write(open(v2e, encoding='utf-8').read().rstrip('\n') + '\n')
        f.write(f'As2S3,S,3,TM,{ox},{red},{"" if ocv is None else ocv},{win},,added 2026-10-14 from {ESW_ADDENDUM} legacy fields ({k})\n')
    rows = _run_score_tool(cc, ce, os.path.join(tmp, 'ranked91.csv'), tmp)
    got = {r['dopant'] for r in rows}
    if len(rows) != 91 or not set(SCORE_ADDED) <= got:
        raise AssertionError(f'expected 91 precursors incl. {SCORE_ADDED}, got {len(rows)}')
    aug = {r['dopant']: int(r['rank']) for r in _score_rows(aug_path)}
    common = [r['dopant'] for r in rows if r['dopant'] in aug]
    new = {r['dopant']: int(r['rank']) for r in rows}
    rho = spearman([aug[d] for d in common], [new[d] for d in common])
    top15 = [r['dopant'] for r in rows[:15]] == sorted(aug, key=aug.get)[:15]
    n_add = {sp: sum(1 for r in add if base(r['dopant']) == sp) for sp in SCORE_ADDED}
    out = [[r['rank'], r['dopant'], anion_family(r['dopant']), r['score'], r['de'], r['ox_V'], r['red_V'], r['E_GPa'], r['pugh'],
            r['pareto'], aug.get(r['dopant'], ''), 'yes' if r['dopant'] in SCORE_ADDED else ''] for r in rows]
    return write('p07_stage1_composite_score_91.csv',
                 ['Page 7 — Stage-1 composite score, the August method re-run on 2026-10-14 with all 91 precursors. Exploratory and flawed:',
                  'the September audit (slide 8 since 10-14) found it unusable as a ranking. Never cite a rank as a result.',
                  'Method unchanged: tools/figures/plot_cascade_insights.py, score = 0.30 ox + 0.25 stable (de) + 0.20 soft (E) + 0.15 ductile (pugh)',
                  '+ 0.10 window, min-max over the pool. This script first re-runs it on the August inputs and checks that it reproduces',
                  'cascade_v23_ranked_v2.csv (89) byte for byte.',
                  f'Added: As2S3 and AlI3 (August re-run) with their rank_combined == 1 rows from cascade_all_302 (As2S3 {n_add["As2S3"]}, AlI3 {n_add["AlI3"]};',
                  f'AlI3 had empty rows in the August champion table). As2S3 window from {ESW_ADDENDUM} legacy fields ({k}, old definition,',
                  'MP 2026.04.13); AlI3 was already in the August window table.',
                  f'The other 89 keep their August inputs: Spearman {rho:.4f} against the August ranks; top 15 {"unchanged" if top15 else "CHANGED"}.',
                  f'Not refreshed: the master rank-1 rows differ from the August champion rows for {n_diff} of {n_cmp} precursors.',
                  'Known flaws: de is a per-atom energy against the host with no reference for the added elements (composition-dependent);',
                  'elastic and bond-valence descriptors spread as much within a precursor as between precursors; hand-set weights;',
                  'min-max scaling shifts with the pool; the window is the old definition. anion_family is from the formula.'],
                 ['rank_91', 'precursor', 'anion_family', 'score', 'de_eV_per_atom', 'ox_V', 'red_V_old_definition', 'E_GPa', 'pugh',
                  'pareto', 'rank_aug89', 'added_2026_10_14'], out)


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


def anneal_rows(rows):
    """Main-batch structures that finished the short anneal → [(precursor, configuration, ΔE meV per supercell)].
    The dual-concentration set is a different experiment and stays out; a finished row without ΔE is an error, not a
    zero (an empty cell drawn as 0 would read as 'the anneal changed nothing')."""
    out = []
    for r in rows:
        if r['family'] not in MAIN_FAMILIES or r['anneal_converged'] != 'True':
            continue
        if not str(r.get('anneal_delta_E_meV', '')).strip():
            raise ValueError(f"{r['name']}: anneal_converged but no anneal_delta_E_meV")
        out.append((base(r['dopant']), r['name'], float(r['anneal_delta_E_meV'])))
    return out


def p08b():
    """Slide 9 (slim deck, user 10-15 'recommendation'): the short anneal's energy change, one row per annealed
    structure. Replaces the August Step-5 histogram (n 681, before the August re-run) — 693 is the count on slide 7."""
    a = anneal_rows(stage1_rows())
    dE = sorted(x for *_, x in a)
    n, neg = len(dE), sum(x < 0 for x in dE)
    med = (dE[(n - 1) // 2] + dE[n // 2]) / 2
    write('p08_anneal_energy_change.csv',
          ['Page 9 (slim deck) — energy change from the short anneal (500 K, 50 ps, then relaxed again); one row per structure.',
           f'Source: cascade_all_302_2026_08_25.csv · main batch ({" + ".join(MAIN_FAMILIES)}) · anneal_converged True → '
           f'n = {n} structures, {len({p for p, *_ in a})} precursors.',
           f'Lower after the anneal: {neg} of {n} · median {med:.1f} meV per supercell (4 formula units) — NOT per atom.',
           'UMA (MLIP) energies of the same structure before and after the anneal: no reference term enters.',
           "Exploratory (Stage 1). The August deck showed n 681 (before the August re-run) and 'the top ten did not change' — withdrawn.",
           'Origin: Plot > Statistical > Histogram, Bin Size 50, Begin -1250, End 0 (do not pre-bin).'],
          ['precursor', 'configuration', 'anneal_delta_E_meV_per_supercell'], [[p, c, f'{x:.3f}'] for p, c, x in a])
    return 'p08_anneal_energy_change.csv'


def anneal_origin_tables(rows):
    """p08_anneal_energy_change.csv rows (header first) → (median meV, Origin rows, 50 meV bin rows).
    Refuses a different header, a count other than the deck's 693, a value ≥ 0 (the deck says all 693 went lower) and a
    value outside −1250 … 0 (it would fall out of the bins). ⛔ Says nothing about why one structure dropped more."""
    head, body = rows[0], rows[1:]
    if head != ['precursor', 'configuration', 'anneal_delta_E_meV_per_supercell']:
        raise ValueError(f'unexpected header {head}')
    dE = [float(r[2]) for r in body]
    if len(dE) != 693 or max(dE) >= 0 or min(dE) < -1250:
        raise ValueError(f'n {len(dE)} · max {max(dE)} · min {min(dE)} — not the 693 lowered structures in −1250 … 0')
    s = sorted(dE)
    med = (s[(len(s) - 1) // 2] + s[len(s) // 2]) / 2
    edges = [-1250 + 50 * k for k in range(26)]
    counts = [sum(edges[k] <= x < edges[k + 1] for x in dE) for k in range(25)]
    if sum(counts) != len(dE):
        raise ValueError('a value fell between the bins')
    data = [[f'{x:.3f}', f'{x / 1000:.6f}', r[0], r[1]] for r, x in zip(body, dE)]
    bins = [[edges[k], edges[k + 1], edges[k] + 25, counts[k]] for k in range(25)]
    return med, data, bins


def p08b_origin():
    """User 10-15 ('csv 를 새롭게 · median 값이랑'): the 693 rows of p08_anneal_energy_change.csv for an Origin
    histogram like the August one, in meV and eV per 52-atom cell (the source column says 'supercell' = the
    4-formula-unit conventional cell), with the median in the header; plus the 50 meV bins for a column plot."""
    med, data, bins = anneal_origin_tables(rows_of(os.path.join(OUT, 'p08_anneal_energy_change.csv')))
    n = len(data)
    common = [f'n = {n} structures (main batch, short anneal 500 K / 50 ps, then relaxed again) · all {n} went lower.',
              f'Median ΔE = {med:.1f} meV = {med / 1000:.2f} eV per 52-atom cell (4 formula units) — NOT per atom.',
              f'Range {min(float(r[0]) for r in data):.1f} … {max(float(r[0]) for r in data):.1f} meV. Exploratory (Stage 1).',
              'Cell = the 52-atom conventional cell; the source CSV calls it "supercell". Same rows as p08_anneal_energy_change.csv.']
    write('p08_anneal_energy_change_origin.csv',
          ['Page 10 (user deck) — short-anneal energy change, one row per structure, for an Origin histogram.'] + common +
          ['Origin: select column A > Plot > Statistical > Histogram · Bin Size 50 · Begin -1250 · End 0 (do not pre-bin).',
           f'X axis -1250 … 0, title "energy change (meV per 52-atom cell)" · Y title "structures" · median line at X = {med:.1f}.'],
          ['dE_meV_per_52atom_cell', 'dE_eV_per_52atom_cell', 'precursor', 'configuration'], data)
    write('p08_anneal_energy_change_bins_origin.csv',
          ['Page 10 (user deck) — the same 693 values counted in 50 meV bins [left, right) — for a column plot.'] + common +
          ['Origin: X = bin_center_meV, Y = n_structures, Plot > Column/Bar, gap 0. The counts sum to n.'],
          ['bin_left_meV', 'bin_right_meV', 'bin_center_meV', 'n_structures'], bins)
    return 'p08_anneal_energy_change_origin.csv'


SITE_CODE_ROWS = {'Li_24g': 'Li 24g', 'P_4b': 'P 4b (framework)', 'Li_48h': 'Li 48h'}
SITE_CODE_COLS = {'S_4a': 'free sulfide', 'S_16e': 'sulfur in the PS₄ corner', 'Cl_4d': 'halide site'}


def p08_3675():
    """User 10-15 ('추가해서 만드는건 안되는거야?'): the site-pair table over all 3,675 relaxed structures of slide 7 —
    the main batch (3,615) plus the August re-run (60 = As₂S₃ 45 new + AlI₃ 15 re-runs of configurations already in the
    main batch, same names). Counts STRUCTURES (runs), like slide 7 — not distinct configurations (3,660)."""
    rows = [r for r in stage1_rows() if r['family'] in MAIN_FAMILIES]
    grid = {(c, a): 0 for c in SITE_CODE_ROWS for a in SITE_CODE_COLS}
    for r in rows:
        k = (r['cation_site'], r['anion_site'])
        if k not in grid:
            raise ValueError(f"{r['name']}: site pair {k} outside the 3 × 3 table")
        grid[k] += 1
    total = sum(grid.values())
    if total != 3675:
        raise ValueError(f'{total} structures, not the 3,675 of slide 7')
    names = [r['name'] for r in rows]
    dup = len(names) - len(set(names))
    head = ['Page 10 (user deck) — structures per (cation site, anion site) over all 3,675 relaxed structures of slide 7.',
            'Source: cascade_all_302_2026_08_25.csv families multi_category_2026_05_26_v23 (3,615) + as2s3_recover (60).',
            f'Counts STRUCTURES (relaxation runs), as slide 7 does: {dup} AlI3 re-runs share names with main-batch rows '
            f'(distinct configurations {total - dup}).']
    write('p08_structures_per_site_pair_3675_long.csv', head,
          ['cation_site', 'anion_site', 'n_structures', 'percent_of_all'],
          [[SITE_CODE_ROWS[c], SITE_CODE_COLS[a], grid[(c, a)], round(100 * grid[(c, a)] / total, 1)] for c in SITE_CODE_ROWS for a in SITE_CODE_COLS])
    return write('p08_structures_per_site_pair_3675_matrix.csv', head + ['Same counts as a 3x3 matrix (rows = cation site, columns = anion site).'],
                 ['cation_site'] + list(SITE_CODE_COLS.values()),
                 [[SITE_CODE_ROWS[c]] + [grid[(c, a)] for a in SITE_CODE_COLS] for c in SITE_CODE_ROWS])


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


def host_window_edges(hosts):
    """(lower, upper, width, earlier_lower, earlier_width) of the host window — the same in every phase set.
    The earlier lower limit (ledger `first_reduction_plateau_V`, the edge until the 2026-09-22 correction) must lie
    below the corrected edge, inside the Li-uptake range; if it does not, the ledger changed and so did page 12's story.
    ⛔ Cannot: tell whether the earlier value was ever a window edge for any other composition — host only."""
    vals = {(h['ocv_self_decomposition_V'], h['oxidation_limit_V'], h['window_V'],
             h['first_reduction_plateau_V'], h['legacy_window_V_2026_09_22']) for h in hosts.values()}
    if len(vals) != 1:
        raise ValueError(f'host window differs across phase sets: {sorted(vals)[:4]}')
    lo, ox, win, old, old_win = vals.pop()
    if not old < lo < ox or abs(ox - lo - win) > 0.002 or abs(ox - old - old_win) > 0.002:
        raise ValueError(f'host window edges inconsistent: {(lo, ox, win, old, old_win)}')
    return lo, ox, win, old, old_win


def p10():
    v = json.load(open(os.path.join(P, 'oxidation_stability_cascade_v3_pinned.json')))
    hs = v['hosts_by_phase_set']
    ocv, ox, win, old, old_win = host_window_edges(hs)
    write('p10_stability_window_host_legacy.csv',
          ['Page 12 (user deck) — the EARLIER lower limit of the host window, kept only to show what the 2026-09-22 correction changed.',
           'It is the voltage of a Li-uptake step (ledger first_reduction_plateau_V), not a window edge; earlier width = upper − this.',
           'Source: db/properties/oxidation_stability_cascade_v3_pinned.json hosts_by_phase_set (identical in all phase sets).'],
          ['quantity', 'voltage_V_vs_Li'],
          [['earlier lower limit (a Li-uptake step; the edge until 2026-09-22)', old], ['earlier window width', old_win]])
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


def origin_rich(formula):
    """Sc2O3 → Sc\\-(2)O\\-(3) (Origin rich-text subscript). Only digits after an element symbol are subscripts."""
    if not re.fullmatch(r'([A-Z][a-z]?\d*)+', formula):
        raise ValueError(f'not a plain formula: {formula!r}')
    return re.sub(r'(?<=[A-Za-z])(\d+)', r'\\-(\1)', formula)


def p07d(n=10):
    # p07d (user 10-15: "이거 origin으로 그리게 csv"): the top 10 of p07_stage1_composite_score_91.csv exactly as the slim
    # slide draws it — read from that file (no second score run), rows in Origin's plotting order.
    sc = rows_of(os.path.join(OUT, 'p07_stage1_composite_score_91.csv'))
    ix = {k: sc[0].index(k) for k in sc[0]}
    top = sc[1:n + 1]
    if [int(r[ix['rank_91']]) for r in top] != list(range(1, n + 1)):
        raise ValueError('p07_stage1_composite_score_91.csv is not in rank order')
    out = []
    for r in reversed(top):                       # rank 10 first: Origin's horizontal bars put row 1 at the bottom
        rank, sp, s = int(r[ix['rank_91']]), r[ix['precursor']], float(r[ix['score']])
        out.append([n + 1 - rank, rank, sp, f'{rank}. {sp}', f'{rank}. {origin_rich(sp)}', r[ix['score']], f'{s:.2f}'])
    return write('p07_stage1_composite_score_top10_origin.csv',
                 [f'Page 7 — slim slide, right: Stage-1 composite score, top {n} of 91 (copied from p07_stage1_composite_score_91.csv).',
                  'Exploratory and flawed: the September audit (slide 8) found this score unusable as a ranking. Never cite a rank as a result.',
                  f'Rows run from rank {n} to rank 1: Origin draws row 1 of a horizontal bar plot at the bottom, so rank 1 ends up on top.',
                  'Plot: Bar (horizontal), X = tick_label_origin_richtext (or tick_label_plain), Y = composite_score.',
                  'Axis as on the slide: 0 to 1.0, ticks 0 / 0.5 / 1.0, title "composite score (first attempt)".',
                  'Bars: fill #bdbdbd, black edge 0.8 pt. Value labels: value_label_2dp (2 decimals, as on the slide; score keeps 3).',
                  'tick_label_origin_richtext uses Origin escapes (\\-(2) = subscript); if the axis shows the backslashes, use tick_label_plain.'],
                 ['bar_position_bottom_to_top', 'rank_91', 'precursor', 'tick_label_plain', 'tick_label_origin_richtext',
                  'composite_score', 'value_label_2dp'], out)


SITE_PAIR_ROWS = {'Li 24g': 'Li 24g', 'P 4b (framework)': 'P 4b', 'Li 48h': 'Li 48h'}
SITE_PAIR_COLS = {'free sulfide': 'S 4a\n(free S$^{2{-}}$)', 'sulfur in the PS₄ corner': 'S 16e\n(in PS₄)', 'halide site': 'Cl 4d'}
P08_USER_SLOTS = {'heatmap': (4.6, 3.3), 'hist': (3.3, 1.7)}   # user's slim page 10 (10-15) — the hand-edited deck


def site_pair_matrix(rows, total=3615):
    """p08 matrix CSV rows (header first) → (row labels, column labels, counts) in field terms (Wyckoff site names).
    Refuses anything but the 3 × 3 table with the declared total (3,615 main batch, or 3,675 with the August re-run)
    and every pair populated — a partial or relabelled table must not be drawn as if it were the whole batch."""
    head, body = rows[0], rows[1:]
    if head[0] != 'cation_site' or head[1:4] != list(SITE_PAIR_COLS) or [r[0] for r in body] != list(SITE_PAIR_ROWS):
        raise ValueError(f'unexpected site-pair table: {head} / {[r[0] for r in body]}')
    counts = [[int(x) for x in r[1:4]] for r in body]
    if sum(map(sum, counts)) != total or min(map(min, counts)) <= 0:
        raise ValueError(f'site-pair total {sum(map(sum, counts))} != {total} or an empty pair')
    return [SITE_PAIR_ROWS[r[0]] for r in body], [SITE_PAIR_COLS[c] for c in head[1:4]], counts


def _plt():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family': 'Liberation Sans', 'font.size': 10, 'axes.labelsize': 10.5,
                         'mathtext.default': 'regular'})   # S$^{2-}$: Liberation Sans has no U+207B
    return plt


def draw_site_pair_heatmap(out, w=4.6, h=3.3, src='p08_configurations_per_site_pair_matrix.csv', total=3615):
    """Configurations per (cation, anion) substitution-site pair with field labels (user 10-15: 'field terms'; the
    August image17 said 'where the dopant metal went'). Drawn at the slot size, counts on the cells, no colour bar.
    ⛔ Does not show the 60 structures of the August re-run — they are not in the main-batch table."""
    plt = _plt()
    rl, cl, m = site_pair_matrix(rows_of(os.path.join(OUT, src)), total)
    tot, vmax = sum(map(sum, m)), max(map(max, m))
    fig, ax = plt.subplots(figsize=(w, h))
    ax.imshow(m, cmap='Blues', vmin=0, vmax=vmax * 1.05, aspect='auto')
    for i, row in enumerate(m):
        for j, n in enumerate(row):
            c = 'white' if n > 0.55 * vmax else '#1f2937'
            ax.text(j, i - 0.13, f'{n:,}', ha='center', va='center', fontsize=12, fontweight='bold', color=c)
            ax.text(j, i + 0.22, f'{100 * n / tot:.0f} %', ha='center', va='center', fontsize=9, color=c)
    ax.set_xticks(range(len(cl)), cl, fontsize=10)
    ax.set_yticks(range(len(rl)), rl, fontsize=10)
    ax.set_xticks([k + 0.5 for k in range(len(cl) - 1)], minor=True)
    ax.set_yticks([k + 0.5 for k in range(len(rl) - 1)], minor=True)
    ax.grid(which='minor', color='white', linewidth=2.5)
    ax.tick_params(which='both', length=0)
    for sp_ in ax.spines.values():
        sp_.set_visible(False)
    ax.set_xlabel('Anion substitution site')
    ax.set_ylabel('Cation substitution site')
    fig.tight_layout()
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


def draw_host_window(out, w=4.4, h=1.9, earlier=False):
    """Host Li6PS5Cl stability window on a voltage axis — corrected definition (no Li exchange between the
    decomposition-without-Li-exchange voltage and the oxidation onset). earlier=True widens the axis to 1.1 V and
    marks the earlier lower limit as a grey dotted line (user page 12, 10-15 'fit the story': the page says why the
    91 windows were recomputed). ⛔ Cannot: draw the earlier window as a window — only its lower edge, which sits in
    the Li-uptake range."""
    plt = _plt()
    seg = rows_of(os.path.join(OUT, 'p10_stability_window_host_segments.csv'))[1:]
    lo, hi = float(seg[1][1]), float(seg[1][2])
    x0 = 1.4
    if earlier:
        old = float(rows_of(os.path.join(OUT, 'p10_stability_window_host_legacy.csv'))[1][1])
        if not old < lo:
            raise ValueError(f'earlier lower limit {old} is not below the corrected edge {lo}')
        x0 = 1.1
    plt.rcParams.update({'font.size': 10, 'axes.labelsize': 10.5})
    fig, ax = plt.subplots(figsize=(w, h))
    ax.axvspan(lo, hi, color='#d9d9d9')
    for v in (lo, hi):
        ax.axvline(v, color='black', ls='--', lw=1)
        ax.text(v, 1.03, f'{v:.3f} V', ha='center', va='bottom', fontsize=9)
    if earlier:
        ax.axvline(old, color='#6b7280', ls=':', lw=1.4)
        ax.text(old, 1.03, f'{old:.3f} V', ha='center', va='bottom', fontsize=9, color='#6b7280')
        ax.text(old + 0.02, 0.14, 'earlier lower limit', ha='left', va='center', fontsize=8, color='#6b7280')
    ax.text(((old if earlier else x0) + lo) / 2, 0.5, 'Li uptake', ha='center', va='center', fontsize=9)
    ax.text((lo + hi) / 2, 0.5, 'no Li\nexchange', ha='center', va='center', fontsize=9)
    ax.text((hi + 2.5) / 2, 0.5, 'Li release', ha='center', va='center', fontsize=9)
    ax.set_xlim(x0, 2.5)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xlabel('voltage vs Li/Li$^+$ (V)')
    origin_axes(ax)
    ax.tick_params(left=False, right=False)
    fig.tight_layout()
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


def draw_anneal_hist(out, w=3.1, h=1.75, median=False, style='plain'):
    """The short anneal's energy change (693 structures), plain grey bars, 50 meV bins like the August Origin recipe.
    The cell is the 52-atom conventional cell (4 formula units) — the CSV column still says 'per supercell' (10-15: the
    axis says '52-atom cell'; the CSV is not rewritten here). `median` draws a dashed line at the median.
    style='origin' copies the look of the user's August Origin histogram (purple bars, framed axes) — same 693 rows;
    the August image itself is n 681 (before the August re-run) and must not stand in for this one."""
    plt = _plt()
    dE = [float(r[2]) for r in rows_of(os.path.join(OUT, 'p08_anneal_energy_change.csv'))[1:]]
    fig, ax = plt.subplots(figsize=(w, h))
    origin = style == 'origin'
    ax.hist(dE, bins=[-1250 + 50 * k for k in range(26)], color='#c084fc' if origin else '#bdbdbd',
            edgecolor='#6b21a8' if origin else 'black', linewidth=0.6 if origin else 0.8)
    if median:
        s = sorted(dE)
        med = (s[(len(s) - 1) // 2] + s[len(s) // 2]) / 2
        ax.axvline(med, color='#2563eb', linestyle='--', linewidth=1.0)
        ax.text(med - 20, ax.get_ylim()[1] * 0.97, 'median', color='#2563eb', fontsize=8.5, va='top', ha='right')
    ax.set_xlim(-1250, 0)
    ax.set_xticks([-1200, -900, -600, -300, 0])
    ax.set_xlabel('energy change (meV per 52-atom cell)', fontsize=9.5)
    ax.set_ylabel('structures', fontsize=9.5)
    if origin:
        ax.set_yticks([0, 50, 100, 150])
        origin_axes(ax)
        ax.tick_params(labelsize=9)
    else:
        plain_axes(ax, 9)
    fig.tight_layout()
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


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
             ('Literature-style threshold table', 'literature thresholds')]   # user 10-13: no 'gate' on the slides
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

    # p07c: Stage-1 composite score (August method, all 91) — top 10, drawn at its slide size (3.4 × 3.7 in, the height of
    # the pipeline box beside it) so a 12 pt label here is 12 pt on the slide. Plain grey bars: nothing is highlighted —
    # the next slides say why this score cannot rank precursors (user 10-14: shown, then called wrong).
    sc = rows_of(os.path.join(OUT, 'p07_stage1_composite_score_91.csv'))
    ix = {k: sc[0].index(k) for k in sc[0]}
    top = sc[1:11]
    sub = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')
    fig, ax = plt.subplots(figsize=(3.4, 3.7))
    ys = list(range(len(top)))[::-1]
    vals = [float(r[ix['score']]) for r in top]
    ax.barh(ys, vals, 0.62, color=GREY, edgecolor='black', linewidth=0.8)
    for y, v in zip(ys, vals):
        ax.text(v + 0.015, y, f'{v:.2f}', va='center', fontsize=11)
    ax.set_yticks(ys, [f"{r[ix['rank_91']]}. {r[ix['precursor']].translate(sub)}" for r in top], fontsize=12)
    ax.set_xlim(0, 1.0)
    ax.set_xticks([0, 0.5, 1.0])
    ax.set_xlabel('composite score (first attempt)', fontsize=11)   # 10-15: slide heading says 'first attempt'
    plain_axes(ax, 11)
    ax.tick_params(axis='y', length=0)
    save(fig, 'fig_p07_stage1_score_top10.png')

    # p08b: the short anneal's energy change (slide 9, under the anneal schematic) — drawn at its slot size (3.1 in)
    made.append(draw_anneal_hist(os.path.join(ASSETS, 'fig_p08_anneal_energy_hist.png')))
    # p08c (10-15): the site-pair heat map redrawn with field labels (the decks still embed the August image17)
    made.append(draw_site_pair_heatmap(os.path.join(ASSETS, 'fig_p08_site_pair_heatmap.png')))

    # p10: host stability window on a voltage axis (+ the user's page-12 version with the earlier lower limit)
    made.append(draw_host_window(os.path.join(ASSETS, 'fig_p10_host_window.png')))
    made.append(draw_host_window(os.path.join(ASSETS, 'fig_p10_host_window_earlier_limit.png'), earlier=True))

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
**Since 2026-10-14 the audit is slide 8** (right after the Stage-1 pipeline and its score) and the three slides that were
8–10 moved down one: `p08_*` = slide 9 · `p09_*` = slide 10 · `p10_*` = slide 11 (file names kept — they are paths).
Made by `kb/seminars/export_cascade_briefing_csvs_2026_10.py` — rerun it after the source files change.
Every CSV starts with `#` comment lines (source, units, cautions); Origin: Import → skip comment lines.
2026-10-12 update: the September-audit slide became page 11, so the MD-status CSV is now p13 and the
site-preference backup p18 (old p12 / p17 files are removed by the script). p06 and p07 count from the ledgers.

| page | slide | CSV | what to plot |
|---|---|---|---|
| 6 | Candidate set | `p06_candidate_set_by_anion_family.csv` | bars: n_planned vs n_relaxed vs n_gate_evaluation per anion family |
| 7 | Stage-1 coverage | `p07_stage1_coverage_by_ledger.csv` · `p07_structures_by_anion_family.csv` | not drawn on the slim deck since 2026-10-14 (the slide shows the five-step pipeline box; the full deck keeps the step table) — kept for questions and Origin (As2S3 / AlI3 flags) |
| 7 | Stage-1 composite score | `p07_stage1_composite_score_91.csv` | horizontal bars, top 10 of 91 (slim deck, beside the pipeline box) — the August method re-run on 10-14 with As2S3 and AlI3 added; exploratory and flawed (the audit, slide 8, says why); never cite a rank as a result |
| 7 | Stage-1 composite score, Origin copy (10-15) | `p07_stage1_composite_score_top10_origin.csv` | the slide's ten bars only, copied from the 91 file · rows in Origin plotting order (rank 10 → 1, so rank 1 is on top) · tick labels plain and Origin rich text (`\\-(2)` subscripts) · value labels at 2 decimals as on the slide · same caution |
| 8 | Configuration sampling | `p08_configurations_per_site_pair_long.csv` · `_matrix.csv` | heat map: cation site × anion site → configurations (main batch 3,615) |
| 8 | Short anneal (slim slide 9, 10-15) | `p08_anneal_energy_change.csv` | histogram: ΔE per structure (meV per supercell · 693 · bin 50 · −1250 … 0) — replaces the August Step-5 histogram (681) |
| 8 | Site pairs over all 3,675 (user page 10, 10-15) | `p08_structures_per_site_pair_3675_long.csv` · `…_3675_matrix.csv` | structures per (cation site, anion site), main batch + August re-run · counts runs like slide 7 (15 AlI₃ re-runs share names; 3,660 distinct) |
| 8 | Short anneal, Origin layout (user page 10, 10-15) | `p08_anneal_energy_change_origin.csv` · `p08_anneal_energy_change_bins_origin.csv` | same 693 values in meV and eV per 52-atom cell, median in the header · 50 meV bins (sum = 693) for a column plot |
| 9 | DFT EOS | `p09_eos_bm3_fit_curves.csv` | lines: E − E0 vs V per f.u. (fit curves; raw points not in repo) |
| 10 | Stability window | `p10_stability_window_host.csv` · `p10_stability_window_host_segments.csv` · `p10_stability_window_host_legacy.csv` | bar segments on a voltage axis (host Li6PS5Cl); the legacy file is the earlier lower limit (a Li-uptake step, edge until 2026-09-22) for the user's page 12 — not a window edge |
| 13 | MD status | `p13_md_campaign_progress.csv` · `p13_md_campaign_runs.csv` | progress bars; run roster (status, wall-clock GPU-h) |
| 18 | Backup: site preference | `p18_site_preference_vs_ionic_radius.csv` | ΔE vs Shannon radius, three loadings per element (June batch, not Stage 1) |

Slim-deck figures (`--figures`) in `kb/seminars/assets_2026_10_13/`: plain previews drawn from the CSVs here (`fig_p07_stage1_score_top10.png` — on the slim deck since 10-14 · `fig_p07_stage1_coverage.png` · `fig_p10_host_window.png` · `fig_p13_run_roster.png`; p07 is drawn at the size it takes on the slide, so its font sizes are the slide's — since 10-13 p06 shows the 08-18 family table (four columns, the third now 'anion vs host') instead, and `fig_p06_candidates_by_family.png` stays only as an Origin option) — replace them with the Origin versions — and literature figures cropped from the litdb crops as the reason for a method choice (`lit_schwietert2021_fig1.png` p10 · `lit_he2018_fig3.png` p12 · `lit_phuthi2026_fig1a.png` p14; never redrawn, never on the same plot as our numbers; `lit_jung2026_sio2_fig3d.png` left p06 on 10-13 and stays only as a crop).

Pages without a CSV:
- 2 (previous DFT work): figure boxes left empty on purpose — fill per tile on request.
- 3, 11, 14, 15 (cards) · 5, 12 (tables, text in the slide) · 1, 16, 17 (title, thanks, references).
- 4 (Kang 2026), 10 right (Sundar 2025 Fig. 2), 13 right (Jung 2026 Fig. 5b): literature figures — not digitized; literature values never go on the same plot as ours.
- 19 (bond-valence landscape): volumetric data (.cube) — not converted.

Value discipline: no transport value (D, ratio, Ea) is in any file here; the stability window is the corrected definition only;
B0 values are canonical DFT (compare per f.u. only); Stage-1 counts are exploratory-data coverage, not a ranking.
"""


def main():
    if '--fig-p08' in sys.argv:   # hand-edited deck (user's page 10): the two figures at its slot sizes, nothing else
        d = sys.argv[sys.argv.index('--fig-p08') + 1]
        os.makedirs(d, exist_ok=True)
        print(draw_site_pair_heatmap(os.path.join(d, 'fig_p08_site_pair_heatmap.png'), *P08_USER_SLOTS['heatmap']))
        print(draw_site_pair_heatmap(os.path.join(d, 'fig_p08_site_pair_heatmap_3675.png'), *P08_USER_SLOTS['heatmap'],
                                     src='p08_structures_per_site_pair_3675_matrix.csv', total=3675))
        print(draw_anneal_hist(os.path.join(d, 'fig_p08_anneal_energy_hist.png'), *P08_USER_SLOTS['hist'], median=True))
        print(draw_anneal_hist(os.path.join(d, 'fig_p08_anneal_energy_hist_origin.png'), *P08_USER_SLOTS['hist'],
                               median=True, style='origin'))
        return
    if '--fig-p10' in sys.argv:   # hand-edited deck (user's page 12): host window with the earlier lower limit
        d = sys.argv[sys.argv.index('--fig-p10') + 1]
        os.makedirs(d, exist_ok=True)
        print(draw_host_window(os.path.join(d, 'fig_p10_host_window_earlier_limit.png'), earlier=True))
        return
    for old in ('p12_md_campaign_runs.csv', 'p12_md_campaign_progress.csv', 'p17_site_preference_vs_ionic_radius.csv'):
        if os.path.exists(os.path.join(OUT, old)):      # renamed when the audit slide became page 11
            os.remove(os.path.join(OUT, old))
    made = [p06(), p07(), p07b(), p07c(), p07d(), p08(), p08_3675(), p08b(), p08b_origin(), p09(), p10(), p13(), p18()]
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
    # Spearman: identical order 1, reversed −1
    assert spearman([1, 2, 3, 4], [10, 20, 30, 40]) == 1 and spearman([1, 2, 3, 4], [4, 3, 2, 1]) == -1; ok += 1
    # As2S3 legacy window: the real addendum passes; a copy whose legacy window != ox − first plateau must be refused
    k_, ox_, red_, _, win_ = as2s3_legacy_esw()
    assert abs((ox_ - red_) - win_) < 1e-3; ok += 1
    bad = json.load(open(os.path.join(P, ESW_ADDENDUM)))
    for v in bad['results'].values():
        if v.get('dopant') == 'As2S3' and v.get('legacy_window_V_2026_09_22') is not None:
            v['legacy_window_V_2026_09_22'] += 0.1
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as t2:
        json.dump(bad, t2)
    try:
        as2s3_legacy_esw(t2.name)
    except ValueError:
        ok += 1
    else:
        raise AssertionError('as2s3_legacy_esw accepted an inconsistent legacy window')
    os.unlink(t2.name)
    # negative: a ledger species outside the 91 (e.g. a renamed 'As2S3_recov') must be refused
    try:
        assert_subset('test', {'As2S3_recov', 'Al2O3'}, {'Al2O3', 'As2S3'})
    except ValueError:
        ok += 1
    else:
        raise AssertionError('assert_subset accepted an unknown species')
    assert_subset('test', {'Al2O3'}, {'Al2O3', 'As2S3'}); ok += 1
    # anneal rows: main batch only, finished only; a finished row without ΔE is refused (not drawn as 0)
    fam = MAIN_FAMILIES[0]
    rr = [{'family': fam, 'anneal_converged': 'True', 'anneal_delta_E_meV': '-800.5', 'dopant': 'Al2O3', 'name': 'a'},
          {'family': 'dualx_v23', 'anneal_converged': 'True', 'anneal_delta_E_meV': '-700', 'dopant': 'Al2O3', 'name': 'b'},
          {'family': fam, 'anneal_converged': '', 'anneal_delta_E_meV': '', 'dopant': 'Al2O3', 'name': 'c'}]
    assert anneal_rows(rr) == [('Al2O3', 'a', -800.5)]; ok += 1
    try:
        anneal_rows(rr + [{'family': fam, 'anneal_converged': 'True', 'anneal_delta_E_meV': ' ', 'dopant': 'X', 'name': 'd'}])
    except ValueError:
        ok += 1
    else:
        raise AssertionError('anneal_rows drew a finished row without ΔE')
    assert len(anneal_rows(stage1_rows())) == 693; ok += 1        # the count on slide 7 (pipeline box)
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
    # p07d: Origin subscripts — positive, then a non-formula must be refused (not passed through half-converted)
    assert origin_rich('Sc2O3') == 'Sc\\-(2)O\\-(3)' and origin_rich('WO3') == 'WO\\-(3)' and origin_rich('LiCl') == 'LiCl'; ok += 1
    for bad in ('Sc₂O₃', '1. Sc2O3', 'sc2o3'):
        try:
            origin_rich(bad)
        except ValueError:
            ok += 1
        else:
            raise AssertionError(f'origin_rich accepted {bad!r}')
    # p07d: rows reversed for Origin (rank 1 last = top bar); a 91 file out of rank order must be refused
    global OUT
    saved_out, tmpd = OUT, tempfile.mkdtemp(prefix='p07d_')
    try:
        OUT = tmpd
        hdr = 'rank_91,precursor,anion_family,score\n'
        open(os.path.join(tmpd, 'p07_stage1_composite_score_91.csv'), 'w').write('# x\n' + hdr + '1,Sc2O3,oxides,0.828\n2,Cr2O3,oxides,0.822\n3,Y2O3,oxides,0.694\n')
        p07d(3)
        got = rows_of(os.path.join(tmpd, 'p07_stage1_composite_score_top10_origin.csv'))
        assert [r[1] for r in got[1:]] == ['3', '2', '1'] and got[1][0] == '1' and got[3][4] == '1. Sc\\-(2)O\\-(3)' and got[1][6] == '0.69'; ok += 1
        open(os.path.join(tmpd, 'p07_stage1_composite_score_91.csv'), 'w').write(hdr + '2,Cr2O3,oxides,0.822\n1,Sc2O3,oxides,0.828\n3,Y2O3,oxides,0.694\n')
        try:
            p07d(3)
        except ValueError:
            ok += 1
        else:
            raise AssertionError('p07d accepted a 91 file out of rank order')
    finally:
        OUT = saved_out
    # site-pair table: the real matrix passes (3 × 3, 3,615); a changed count or a relabelled column is refused
    real = rows_of(os.path.join(OUT, 'p08_configurations_per_site_pair_matrix.csv'))
    rl, cl, m = site_pair_matrix(real)
    assert len(rl) == len(cl) == 3 and sum(map(sum, m)) == 3615; ok += 1
    for bad in ([real[0]] + [real[1][:1] + ['1049'] + real[1][2:]] + real[2:],
                [real[0][:1] + ['free S'] + real[0][2:]] + real[1:]):
        try:
            site_pair_matrix(bad)
        except ValueError:
            ok += 1
        else:
            raise AssertionError('site_pair_matrix accepted a broken table')
    m3675 = rows_of(os.path.join(OUT, 'p08_structures_per_site_pair_3675_matrix.csv'))
    assert sum(map(sum, site_pair_matrix(m3675, 3675)[2])) == 3675; ok += 1
    try:
        site_pair_matrix(m3675)          # the 3,675 table must not pass as the 3,615 main batch
    except ValueError:
        ok += 1
    else:
        raise AssertionError('site_pair_matrix accepted the 3,675 table as the 3,615 main batch')
    # host window (user page 12): the ledger's edges pass; hosts that differ, or an earlier limit that is not below
    # the corrected edge (the page's whole story), are refused
    hosts = json.load(open(os.path.join(P, 'oxidation_stability_cascade_v3_pinned.json')))['hosts_by_phase_set']
    lo_, ox_, win_, old_, oldw_ = host_window_edges(hosts)
    assert (lo_, ox_, old_) == (1.717, 2.14, 1.242) and abs(win_ - 0.423) < 1e-9 and abs(oldw_ - 0.898) < 1e-9; ok += 1
    k0 = next(iter(hosts))
    one = {k: dict(v) for k, v in hosts.items()}
    one[k0]['window_V'] = 0.5
    above = {k: dict(v, first_reduction_plateau_V=1.8, legacy_window_V_2026_09_22=0.34) for k, v in hosts.items()}
    for bad in (one, above):
        try:
            host_window_edges(bad)
        except ValueError:
            ok += 1
        else:
            raise AssertionError('host_window_edges accepted a broken host set')
    leg = rows_of(os.path.join(OUT, 'p10_stability_window_host_legacy.csv'))
    assert float(leg[1][1]) == old_ and float(leg[2][1]) == oldw_; ok += 1
    real_a = rows_of(os.path.join(OUT, 'p08_anneal_energy_change.csv'))
    med_, data_, bins_ = anneal_origin_tables(real_a)
    assert len(data_) == 693 and sum(b[3] for b in bins_) == 693 and -820 < med_ < -800; ok += 1
    for bad in ([real_a[0]] + [real_a[1][:2] + ['12.0']] + real_a[2:],
                [['precursor', 'configuration', 'dE']] + real_a[1:]):
        try:
            anneal_origin_tables(bad)
        except ValueError:
            ok += 1
        else:
            raise AssertionError('anneal_origin_tables accepted a broken table')
    print(f'selftest PASS ({ok})')


if __name__ == '__main__':
    selftest() if '--selftest' in sys.argv else main()
