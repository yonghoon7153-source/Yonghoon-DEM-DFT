"""Real JSON -> unchanged loader -> full Flask response type/nullable controls."""
import contextlib
import copy
import csv
import hashlib
from html.parser import HTMLParser
import io
import json
import os
from pathlib import Path
import re
import sys
import traceback

REVIEW = Path(__file__).resolve().parents[1]
TREE = sys.argv[1]
ROOT = REVIEW / 'source' if TREE == 'source' else REVIEW.parent / 'lhs214rr_recheck_20261019/source'
WORK = REVIEW / ('evidence/s04_types_' + TREE + '_work')
for key, name in (('WEBAPP_UPLOAD_FOLDER', 'uploads'), ('WEBAPP_RESULTS_FOLDER', 'results'),
                  ('WEBAPP_ARCHIVE_FOLDER', 'archive'), ('WEBAPP_MPM_LAB_FOLDER', 'mpm'), ('MPLCONFIGDIR', 'mpl')):
    os.environ[key] = str(WORK / name)
os.environ['SUPABASE_URL'] = os.environ['SUPABASE_KEY'] = ''
sys.path[:0] = [str(ROOT / 'webapp'), str(ROOT / 'scripts')]
quiet = io.StringIO()
with contextlib.redirect_stdout(quiet):
    import app
app.app.config.update(TESTING=True, PROPAGATE_EXCEPTIONS=False)
client = app.app.test_client()
BASE = dict(sigma_full_mScm=.24, sigma_full_mScm_physics=.72,
    sigma_full_status='computed', sigma_full_status_physics='computed',
    network_solver_status='success', sigma_ratio=.24, sigma_grain_S_cm=.003, phi_se=.5,
    percolation_pct=100., sigma_bulk_net_mScm=1., sigma_bulk_net_mScm_physics=1.,
    R_brug_over_full=7.2, R_brug_over_full_physics=2.4, bulk_resistance_fraction=.6,
    bulk_resistance_fraction_physics=.8, electronic_sigma_full_mScm=2.,
    electronic_sigma_full_mScm_physics=3., thermal_sigma_full_mScm=.3,
    thermal_sigma_full_mScm_physics=.45, tortuosity_mean=1.2, tortuosity_recommended=1.2)
ROWS = [['── Network Solver (Hertzian DEM-native) ──', '', '', ''],
        ['σ_ionic (mS/cm)', '0.24', '0.72', '+200.0%'], ['SE Volume Fraction', '.5', '.5', '0%']]
LABELS = ('σ_brug/σ_grain (Bruggeman)', 'σ_brug / σ_ionic', 'σ_Bruggeman (mS/cm)')
MISSING = object()
TYPES = dict(missing=MISSING, null=None, zero=0, integer=1, finite=.24, false=False,
             true=True, nan=float('nan'), posinf=float('inf'), neginf=-float('inf'),
             numeric_string='0.24', array=[.24], mapping={'value': .24})
GROUPS = [('sigma_ratio',), ('phi_se',), ('tortuosity_recommended', 'tortuosity_mean'),
          ('percolation_pct',), ('sigma_full_mScm',), ('sigma_grain_S_cm',)]

def run(name, mutations):
    m = dict(BASE)
    for key, value in mutations.items():
        if value is MISSING:
            m.pop(key, None)
        else:
            m[key] = value
    rd, ud = WORK / 'results' / name, WORK / 'uploads' / name
    rd.mkdir(parents=True, exist_ok=True)
    ud.mkdir(parents=True, exist_ok=True)
    (rd / 'full_metrics.json').write_text(json.dumps(m), encoding='utf-8')
    (ud / 'meta.json').write_text(json.dumps(dict(name=name, status='done', scale=1)), encoding='utf-8')
    with (rd / 'network_summary.csv').open('w', encoding='utf-8', newline='') as f:
        wr = csv.writer(f)
        wr.writerow(['metric', 'H', 'P', 'delta'])
        wr.writerows(ROWS)
    hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in rd.iterdir() if p.is_file()}
    r = dict(mutations={k: '<MISSING>' if v is MISSING else v for k, v in mutations.items()})
    with contextlib.redirect_stdout(quiet):
        try:
            tables, effective, _ = app._load_case_tables(str(rd), {})
            r['loader_ok'] = True
            r['loader_rows'] = tables['network_summary']['data']
        except Exception:
            r['loader_ok'] = False
            r['loader_error'] = traceback.format_exc()
        response = client.get('/single/' + name)
    page = response.get_data(as_text=True)
    (WORK / (name + '.html')).write_text(page, encoding='utf-8')
    r['http'] = response.status_code
    r['inputs_unchanged'] = hashes == {n: hashlib.sha256((rd / n).read_bytes()).hexdigest() for n in hashes}
    r['tooltips'] = {}
    for label in LABELS:
        hit = re.search(r"  '" + re.escape(label) + r"': \{.*?\n  \}", page, re.S)
        r['tooltips'][label] = hit.group(0) if hit else None
    return r

cases = {'normal': run('normal', {})}
for keys in GROUPS:
    for tag, value in TYPES.items():
        name = keys[0] + '_' + tag
        cases[name] = run(name, dict.fromkeys(keys, value))
cases['sigma_ratio_null_nophi'] = run('sigma_ratio_null_nophi', {'sigma_ratio': None, 'phi_se': MISSING})
cases['sigma_ratio_absent_nophi'] = run('sigma_ratio_absent_nophi', {'sigma_ratio': MISSING, 'phi_se': MISSING})
flags = {tag: app.app.jinja_env.tests['number'](value) for tag, value in TYPES.items() if value is not MISSING}
out = dict(source=str(Path(app.__file__).resolve()), cases=cases, jinja_number=flags,
           note='NaN and infinities are Python JSON extensions, not strict JSON numbers. No builder/loader/template monkeypatch.', stdout=quiet.getvalue())
(REVIEW / ('evidence/s04_types_' + TREE + '.json')).write_text(json.dumps(out, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
print(json.dumps(dict(cases=len(cases), http200=sum(r['http'] == 200 for r in cases.values()),
                     http500=[k for k, r in cases.items() if r['http'] == 500], jinja_number=flags), ensure_ascii=False))
