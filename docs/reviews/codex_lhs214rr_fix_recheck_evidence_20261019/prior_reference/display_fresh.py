"""Independent fresh final-loader/Flask probes plus disclosed K1--K4 checks.

All writes are fixtures/evidence below this review. The source is imported intact.
Use display_run_command.py to supply the pinned Python/dependencies.
"""
import contextlib
import copy
import csv
import hashlib
from html.parser import HTMLParser
import io
import json
import math
import os
from pathlib import Path
import sys
import tarfile
import traceback

review = Path(__file__).resolve().parents[1]
tree = sys.argv[1] if len(sys.argv) > 1 else 'source'
root = review / tree
work = review / 'evidence' / ('display_fresh_work_' + tree)
work.mkdir(parents=True, exist_ok=True)
for key, name in (('WEBAPP_UPLOAD_FOLDER', 'uploads'), ('WEBAPP_RESULTS_FOLDER', 'results'),
                  ('WEBAPP_ARCHIVE_FOLDER', 'archive'), ('WEBAPP_MPM_LAB_FOLDER', 'mpm'), ('MPLCONFIGDIR', 'mpl')):
    os.environ[key] = str(work / name)
os.environ['SUPABASE_URL'] = os.environ['SUPABASE_KEY'] = ''
sys.path[:0] = [str(root / 'webapp'), str(root / 'scripts')]
quiet = io.StringIO()
with contextlib.redirect_stdout(quiet):
    import app
import tau_flux as tf
import pipeline_service as ps
import grade_engine as ge
app.app.config['TESTING'] = True

class Rows(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows, self.row, self.cell = [], None, None
    def handle_starttag(self, tag, attrs):
        if tag == 'tr': self.row = []
        if tag == 'td' and self.row is not None: self.cell = []
    def handle_data(self, data):
        if self.cell is not None: self.cell.append(data)
    def handle_endtag(self, tag):
        if tag == 'td' and self.cell is not None:
            self.row.append(''.join(self.cell).strip())
            self.cell = None
        if tag == 'tr' and self.row is not None:
            if self.row: self.rows.append(self.row)
            self.row = None

BASE = dict(sigma_full_mScm=.2, sigma_full_mScm_physics=.8,
    sigma_full_status='computed', sigma_full_status_physics='computed',
    network_solver_status='success', sigma_ratio=.4, phi_se=.5,
    sigma_bulk_net_mScm=1., sigma_bulk_net_mScm_physics=1.,
    R_brug_over_full=3., R_brug_over_full_physics=.75,
    bulk_resistance_fraction=.6, bulk_resistance_fraction_physics=.8,
    electronic_sigma_full_mScm=2., electronic_sigma_full_mScm_physics=3.,
    thermal_sigma_full_mScm=.3, thermal_sigma_full_mScm_physics=.45, tortuosity_mean=1.2)
LABELS = ('σ_ionic (mS/cm)', 'R_brug (과대추정 배수)', 'Contact-free / Full',
          'σ_brug / σ_ionic', 'σ_ionic ratio (physics/Hertzian)')
OLD = [['── Network Solver (Hertzian DEM-native) ──', '', '', ''],
       [LABELS[0], 17., 19., '+11.8%'], [LABELS[1], '31.0×', '37.0×', '+19.4%'],
       [LABELS[2], '31.0×', '37.0×', '+19.4%'], [LABELS[3], '41.0×', '43.0×', '+4.9%'],
       [LABELS[4], '1.12×', '1.12×', '0%'], ['SE Volume Fraction', .5, .5, '0%']]

def mapped(rows):
    return {str(r[0]): [str(x) for x in r[1:]] for r in rows if r}

def case(name, mx, layout='fourcol'):
    rd, ud = work/'results'/name, work/'uploads'/name
    rd.mkdir(parents=True, exist_ok=True); ud.mkdir(parents=True, exist_ok=True)
    (rd/'full_metrics.json').write_text(json.dumps(mx), encoding='utf-8')
    (ud/'meta.json').write_text(json.dumps(dict(name=name, status='done', scale=1)), encoding='utf-8')
    rows = copy.deepcopy(OLD)
    if layout == 'new': rows = [['SE Volume Fraction', .5]]
    elif layout in ('csv', 'split'):
        rows = [[r[0], r[1]] for r in rows if r[0] != LABELS[4]]
        if layout == 'split':
            rows += [['── Physics (Plastic film, Tabor+volume) ──', ''],
                     ['σ_ionic [physics] (mS/cm)', 19.], [LABELS[4], '1.12×']]
    with (rd/'network_summary.csv').open('w', encoding='utf-8', newline='') as f:
        wr = csv.writer(f); wr.writerow(['metric','H','P','delta'] if layout == 'fourcol' else ['metric','value']); wr.writerows(rows)
    sha = hashlib.sha256((rd/'network_summary.csv').read_bytes()).hexdigest()
    try:
        with contextlib.redirect_stdout(quiet):
            tables, met, _ = app._load_case_tables(str(rd), {})
            res = app.app.test_client().get('/single/' + name)
        html = res.get_data(as_text=True)
        parsed = Rows(); parsed.feed(html)
        got = dict(loader=mapped(tables['network_summary']['data']), rendered=mapped(parsed.rows),
                   status=res.status_code, csv_unchanged=sha==hashlib.sha256((rd/'network_summary.csv').read_bytes()).hexdigest())
        if name in ('missing_both_derived_fourcol', 'K1_tiny_sigma_fourcol', 'validzero_hertz_fourcol'):
            (review/'evidence'/f'display_fresh_{tree}_{name}.html').write_text(html, encoding='utf-8')
        return got
    except Exception as exc:
        return dict(error=f'{type(exc).__name__}: {exc}', traceback=traceback.format_exc())

out = dict(tree=tree, source_import=str(Path(app.__file__).resolve()), cases={}, checks=[], known={})
for layout in ('new', 'csv', 'split', 'fourcol'):
    out['cases']['normal_'+layout] = case('normal_'+layout, BASE, layout)
    for mode in ('hertz', 'physics', 'both'):
        mx = copy.deepcopy(BASE)
        for suffix in ('', '_physics') if mode == 'both' else (('',) if mode == 'hertz' else ('_physics',)):
            mx['sigma_full_mScm'+suffix] = None
            mx['R_brug_over_full'+suffix] = None
            mx['sigma_full_status'+suffix] = 'valid_zero'
            mx['sigma_full_reason'+suffix] = 'no_through_path'
        out['cases']['validzero_'+mode+'_'+layout] = case('validzero_'+mode+'_'+layout, mx, layout)

# Fresh edge: approved legacy retention applies, but the documented delta rule
# says old cells must not receive an apparently current comparison.
mx = {k:v for k,v in BASE.items() if not k.startswith('R_brug_over_full') and k != 'sigma_ratio' and 'status' not in k}
for layout in ('csv', 'split', 'fourcol'):
    out['cases']['missing_both_derived_'+layout] = case('missing_both_derived_'+layout, mx, layout)
mx = {k:v for k,v in BASE.items() if k != 'R_brug_over_full_physics'}
out['cases']['missing_one_derived_fourcol'] = case('missing_one_derived_fourcol', mx)

def call(fn, *a, **kw):
    try: return dict(value=fn(*a, **kw))
    except Exception as exc: return dict(error=f'{type(exc).__name__}: {exc}')

tiny = dict(BASE, sigma_full_mScm=1e-310)
out['known']['K1_tau2_from_metrics'] = call(tf.tau2_from_metrics, tiny)
out['known']['K1_tau2_value'] = call(tf.tau2_value, 1e308, 3., 1e-3)
out['known']['K1_grade_axis'] = call(ge._tau_axis, tiny, 'hertz')
grade = ge.build_overall_grade(tiny, corpus_rows=[])
out['known']['K1_grade_impact'] = dict(axes=[a for a in grade['axes'] if 'tau' in str(a['source_key'])], composite=grade['composite'])
out['cases']['K1_tiny_sigma_fourcol'] = case('K1_tiny_sigma_fourcol', tiny)
big = dict(BASE, temperature_provenance={'sigma_ion_T_factor':10**400})
out['known']['K2_tau2_from_metrics'] = call(tf.tau2_from_metrics, big)
out['known']['K4_stage_e_missing_keys'] = call(ps.stage_e_missing_keys, {'sigma_full_mScm_stage_e':10**400})

# K2 guard: point at a real small producer folder from the independent rerun,
# and modify only the full_metrics argument passed to the reader.
old = json.loads((review/'evidence/display_source.json').read_text(encoding='utf-8'))
prod = old['producer_runs']['ml_el']
fm = copy.deepcopy(prod['metrics'])
fm['temperature_provenance'] = {'sigma_ion_T_factor':10**400}
out['known']['K2_stop_verdict'] = call(ps.network_stop_verdict, prod['path'], prod['run_id'], fm=fm)

# K3: use an actual archived legacy nonthrough row as a fixture, without
# extracting or altering the historical archive.
# Historical fixture bytes are shared between the two code roots; the base
# package intentionally contains no docs/data archive.
archive = review/'source/docs/data/lhs_network194_11fcf91e8/handover_v12_20261006/net194_tau_sources_20261006.tar.gz'
with tarfile.open(archive) as tar:
    for member in tar.getmembers():
        if member.name.endswith('/network_conductivity_dual.json'):
            dual = json.load(tar.extractfile(member))
            if dual.get('hertzian', {}).get('sigma_full_status') == 'valid_zero':
                parent = member.name.rsplit('/', 1)[0]
                ledger = json.load(tar.extractfile(parent+'/full_metrics.json'))
                break
    else: raise RuntimeError('No archived legacy valid_zero fixture')
for rec in dual.values():
    if isinstance(rec, dict): rec['sigma_grain_S_cm'] = 1e306
out['known']['K3_source_member'] = member.name
out['known']['K3_ion_columns'] = call(tf.ion_columns, dual, ledger, 0)
paired = dict(ledger, sigma_grain_S_cm=1e306, temperature_provenance=dual['hertzian']['temperature_provenance'])
out['known']['K3_sigma0_problem'] = call(ps.network_sigma0_problem, dual, dual['hertzian'], paired)

def cells(v, label, where='rendered'):
    return v.get(where, {}).get(app._PAPER_LABEL_MAP.get(label, label))
for name, value in out['cases'].items():
    if name.startswith('normal_'):
        got = cells(value, LABELS[0])
        out['checks'].append(dict(case=name, check='current ionic sigma', got=got, want=['0.2','0.8','+300.0%'], passed=got==['0.2','0.8','+300.0%']))
    if name.startswith('missing_both_derived_'):
        for label in LABELS[1:4]:
            got = cells(value, label)
            out['checks'].append(dict(case=name, check='no delta when neither derived value current', label=label, got=got,
                passed=got is None or got[2]=='—'))
out['stdout'] = quiet.getvalue()
(review/'evidence'/f'display_fresh_{tree}.json').write_text(json.dumps(out, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
print(json.dumps(dict(cases=len(out['cases']), errors={n:v['error'] for n,v in out['cases'].items() if 'error' in v},
    checks=len(out['checks']), failed_checks=[c for c in out['checks'] if not c['passed']],
    known={k:v for k,v in out['known'].items() if k not in ('K3_ion_columns','K2_stop_verdict')}), ensure_ascii=False))
