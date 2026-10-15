"""Independent L214 display probes: actual imports, loader, Flask route/template.

Only synthetic fixtures under evidence/display_work are written. No 214 batch.
"""
import argparse
import contextlib
import copy
import csv
import hashlib
import io
import json
import os
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser()
ap.add_argument('--tree', choices=('source', 'base'), default='source')
ap.add_argument('--producers', action='store_true')
args = ap.parse_args()
ROOT = HERE / args.tree
WORK = HERE / 'evidence' / 'display_work' / args.tree
WORK.mkdir(parents=True, exist_ok=True)
tempfile.tempdir = str(WORK)
for k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[k] = '1'
for k, name in [('WEBAPP_UPLOAD_FOLDER','uploads'), ('WEBAPP_RESULTS_FOLDER','results'),
                ('WEBAPP_ARCHIVE_FOLDER','archive'), ('WEBAPP_MPM_LAB_FOLDER','mpm')]:
    os.environ[k] = str(WORK / name)
os.environ['SUPABASE_URL'] = ''
os.environ['SUPABASE_KEY'] = ''
os.environ['MPLCONFIGDIR'] = str(WORK / 'mplconfig')
sys.path[:0] = [str(ROOT / 'webapp'), str(ROOT / 'scripts')]
capture = io.StringIO()
with contextlib.redirect_stdout(capture):
    import app
app.app.config['TESTING'] = True

class Rows(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.row = None
        self.cell = None
    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.row = []
        if tag == 'td' and self.row is not None:
            self.cell = []
    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)
    def handle_endtag(self, tag):
        if tag == 'td' and self.cell is not None:
            self.row.append(''.join(self.cell).strip())
            self.cell = None
        if tag == 'tr' and self.row is not None:
            if self.row:
                self.rows.append(self.row)
            self.row = None

NORMAL = dict(sigma_full_mScm=.6, sigma_full_mScm_physics=.9,
              sigma_full_status='computed', sigma_full_status_physics='computed',
              network_solver_status='success', sigma_ratio=.4, phi_se=.5,
              sigma_bulk_net_mScm=1., sigma_bulk_net_mScm_physics=1.,
              R_brug_over_full=2., R_brug_over_full_physics=1.4,
              bulk_resistance_fraction=.6, bulk_resistance_fraction_physics=.8,
              electronic_sigma_full_mScm=2., electronic_sigma_full_mScm_physics=3.,
              thermal_sigma_full_mScm=.3, thermal_sigma_full_mScm_physics=.45,
              tortuosity_mean=1.2)
LEGACY = [['── Network Solver (Hertzian DEM-native) ──',''],
          ['σ_ionic (mS/cm)',.6], ['R_brug (과대추정 배수)','2.0×'],
          ['Constriction 비율(%)',40.], ['σ_electronic (mS/cm)',2.],
          ['σ_thermal (mS/cm equiv)',.3], ['SE Volume Fraction',.5]]
LABELS = ('σ_ionic (mS/cm)', 'σ_electronic (mS/cm)', 'σ_thermal (mS/cm equiv)',
          'σ_ionic ratio (physics/Hertzian)', 'σ_brug / σ_ionic',
          'R_brug (과대추정 배수)', 'Contact-free / Full',
          'σ_ionic 망 상태 (생산자 sigma_full_status)')
def relevant(rows):
    wanted = set(LABELS) | {app._PAPER_LABEL_MAP.get(x, x) for x in LABELS}
    return [r for r in rows if r and (r[0] in wanted or 'handover status' in str(r[0]) or '인계 상태' in str(r[0]))]

def fixture(name, mx, csvrows):
    cid = 'display_' + name
    rd = Path(app.app.config['RESULTS_FOLDER']) / cid
    ud = Path(app.app.config['UPLOAD_FOLDER']) / cid
    rd.mkdir(parents=True, exist_ok=True)
    ud.mkdir(parents=True, exist_ok=True)
    (rd / 'full_metrics.json').write_text(json.dumps(mx), encoding='utf-8')
    (ud / 'meta.json').write_text(json.dumps({'name':cid, 'status':'done'}), encoding='utf-8')
    return cid, rd

def evaluate(name, mx, legacy, rd=None, cid=None):
    csvrows = copy.deepcopy(LEGACY if legacy else [['SE Volume Fraction',.5]])
    if legacy == 'split':
        csvrows += [['── Physics (Plastic film, Tabor+volume) ──',''],
                    ['σ_ionic [physics] (mS/cm)',.9],
                    ['σ_ionic ratio (physics/Hertzian)','1.50×']]
    if legacy == 'fourcol':
        csvrows = [[r[0],r[1],r[1],'0%'] for r in csvrows]
    if rd is None:
        cid, rd = fixture(name, mx, csvrows)
    else:
        rd = Path(rd)
    with (rd / 'network_summary.csv').open('w', encoding='utf-8', newline='') as f:
        wr = csv.writer(f); wr.writerow(['지표','H','P','Δ'] if legacy == 'fourcol' else ['지표','값']); wr.writerows(csvrows)
    raw = {'network_summary':{'data':copy.deepcopy(csvrows)}}
    app.transform_network_summary_4col(raw, copy.deepcopy(mx), {})
    tables, metrics, _ = app._load_case_tables(str(rd), {})
    # Full Jinja template with all ordinary context processors; no template extraction.
    if cid is None:
        with app.app.test_request_context('/single/display_probe'):
            html = app.render_template('single.html', case={'id':'display_probe','name':name},
                figures=[], report='', tables=tables, metrics=metrics, input_params={},
                archive_path='', mpm_metrics={}, trust_card=app._build_trust_card(metrics),
                lv=app._page_lv('single'))
        status = 'render_template'
    else:
        response = app.app.test_client().get('/single/' + cid)
        status = response.status_code
        html = response.get_data(as_text=True)
    parsed = Rows(); parsed.feed(html)
    target = HERE / 'evidence' / ('display_' + args.tree + '_' + name + '.html')
    if name in ('normal_new','normal_csv','hertz_null_new','hertz_null_csv',
                'physics_null_new','producer_ml_hertz_new','producer_ml_hertz_csv',
                'producer_ml_physics_split','producer_ml_physics_fourcol'):
        target.write_text(html, encoding='utf-8')
    return {'http_status':status, 'raw_rows':relevant(raw['network_summary']['data']),
            'loader_rows':relevant(tables['network_summary']['data']),
            'rendered_rows':relevant(parsed.rows),
            'all_loader_rows':tables['network_summary']['data']}

out = {'tree':args.tree,'source_import':str(Path(app.__file__).resolve()),
       'scope':'actual app import, actual loader, Flask GET /single, full single.html render; synthetic fixtures',
       'cases':{}, 'producer_runs':{}, 'errors':{}}
cases = {'normal':copy.deepcopy(NORMAL)}
for kind, value in [('valid_zero_null',None),('valid_zero_numeric',0.)]:
    mx=copy.deepcopy(NORMAL)
    for suffix in ('','_physics'):
        for prefix in ('','electronic_','thermal_'):
            mx[prefix+'sigma_full_mScm'+suffix]=value
            mx[prefix+'sigma_full_status'+suffix]='valid_zero'
            mx[prefix+'sigma_full_reason'+suffix]='no_through_path'
        mx['R_brug_over_full'+suffix]=None
    cases[kind]=mx
for side in ('physics','hertz'):
    suffix = '_physics' if side == 'physics' else ''
    for variant in ('null','missing','zero','unknown_reason','unknown_state'):
        mx = copy.deepcopy(NORMAL)
        for base in ('sigma_full_mScm','electronic_sigma_full_mScm','thermal_sigma_full_mScm',
                     'R_brug_over_full'):
            key = base + suffix
            if variant == 'missing':
                mx.pop(key, None)
            else:
                mx[key] = 0. if variant == 'zero' else None
        for prefix in ('','electronic_','thermal_'):
            mx[prefix+'sigma_full_status'+suffix] = 'unknown' if variant == 'unknown_state' else 'not_computed'
            mx[prefix+'sigma_full_reason'+suffix] = 'unknown_reason' if variant == 'unknown_reason' else 'full_over_conduction'
        cases[side+'_'+variant] = mx
for case, mx in cases.items():
    for legacy,tag in ((False,'new'),(True,'csv'),('split','split'),('fourcol','fourcol')):
        name = case + '_' + tag
        try:
            with contextlib.redirect_stdout(capture):
                out['cases'][name] = evaluate(name, mx, legacy)
        except Exception as e:
            import traceback
            out['errors'][name] = traceback.format_exc()

if args.producers:
    import test_network_handover_chain as chain
    for bed, tm in [('ml_physics','1:SE'),('ml_hertz','1:SE'),('ml_el','1:SE,2:AM_P'),('nonthrough','1:SE')]:
        # Preexisting legacy display CSV is present BEFORE actual network publication.
        # The scientific rows are an explicit stale-file adversarial fixture, not
        # a claim that a historical real case carried these invented values.
        cid = 'display_producer_' + bed
        rd = Path(app.app.config['RESULTS_FOLDER'])/cid
        rd.mkdir(parents=True, exist_ok=True)
        # Every invocation gets a fresh scientific fixture under our evidence tree.
        rd = Path(tempfile.mkdtemp(prefix='producer_'+bed+'_', dir=WORK))
        with (rd/'network_summary.csv').open('w',encoding='utf-8',newline='') as f:
            wr=csv.writer(f); wr.writerow(['지표','값']); wr.writerows(LEGACY)
        csv_before = (rd/'network_summary.csv').read_bytes()
        with contextlib.redirect_stdout(capture):
            rd, state, failed, rid = chain._run_ml(app, bed, tm=tm, d=str(rd))
        mx = json.loads((Path(rd)/'full_metrics.json').read_text(encoding='utf-8'))
        out['producer_runs'][bed] = {'state':state,'failed':failed,'run_id':rid,
                                    'metrics':mx,'path':rd,
                                    'preexisting_csv_preserved':csv_before==(Path(rd)/'network_summary.csv').read_bytes(),
                                    'csv_sha256':hashlib.sha256(csv_before).hexdigest()}
        for legacy,tag in ((False,'new'),(True,'csv'),('split','split'),('fourcol','fourcol')):
            name = 'producer_'+bed+'_'+tag
            try:
                with contextlib.redirect_stdout(capture):
                    out['cases'][name] = evaluate(name, mx, legacy, rd=rd)
            except Exception:
                import traceback
                out['errors'][name] = traceback.format_exc()
out['stdout'] = capture.getvalue()
target = HERE/'evidence'/('display_'+args.tree+'.json')
target.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
print(json.dumps({'output':str(target),'cases':len(out['cases']), 'errors':{k:v.splitlines()[-1] for k,v in out['errors'].items()},
                  'producer_states':{k:v['state'] for k,v in out['producer_runs'].items()}},ensure_ascii=False))
