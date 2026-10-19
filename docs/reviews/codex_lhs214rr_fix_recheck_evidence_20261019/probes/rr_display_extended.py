"""Independent loader + complete Flask page controls for R02/WEB09.

No builder monkeypatches; expected values derive from explicit fixture arithmetic.
All case files and page captures are below evidence/rr_display_extended_work.
"""
import contextlib
import copy
import csv
import hashlib
from html.parser import HTMLParser
import io
import json
import os
from pathlib import Path
import sys
import traceback

REVIEW = Path(__file__).resolve().parents[1]
TREE = sys.argv[1] if len(sys.argv)>1 else 'source'
ROOT = REVIEW/'source' if TREE=='source' else REVIEW.parent/'lhs214r_fix_recheck_20261017/source'
WORK = REVIEW/('evidence/rr_display_extended_'+TREE+'_work')
for key, name in (('WEBAPP_UPLOAD_FOLDER', 'uploads'), ('WEBAPP_RESULTS_FOLDER', 'results'),
                  ('WEBAPP_ARCHIVE_FOLDER', 'archive'), ('WEBAPP_MPM_LAB_FOLDER', 'mpm'), ('MPLCONFIGDIR', 'mpl')):
    os.environ[key] = str(WORK/name)
os.environ['SUPABASE_URL'] = os.environ['SUPABASE_KEY'] = ''
sys.path[:0] = [str(ROOT/'webapp'), str(ROOT/'scripts')]
QUIET = io.StringIO()
with contextlib.redirect_stdout(QUIET):
    import app
app.app.config['TESTING'] = True
app.app.config['PROPAGATE_EXCEPTIONS'] = False
CLIENT = app.app.test_client()

class Rows(HTMLParser):
    def __init__(self):
        super().__init__(); self.rows = []; self.row = self.cell = None
    def handle_starttag(self, tag, attrs):
        if tag == 'tr': self.row = []
        if tag == 'td' and self.row is not None: self.cell = []
    def handle_data(self, data):
        if self.cell is not None: self.cell.append(data)
    def handle_endtag(self, tag):
        if tag == 'td' and self.cell is not None:
            self.row.append(''.join(self.cell).strip()); self.cell = None
        if tag == 'tr' and self.row is not None:
            if self.row: self.rows.append(self.row)
            self.row = None

ION, RB, CF, SBI, AMP = ('σ_ionic (mS/cm)', 'R_brug (과대추정 배수)', 'Contact-free / Full',
                        'σ_brug / σ_ionic', 'σ_ionic ratio (physics/Hertzian)')
LABS = (ION, RB, CF, SBI, AMP)
DIAG = 'Independent diagnostic sentinel (outside ionic refresh)'
DIAGNOSTICS = ('Constriction 비율(%)', 'σ_electronic (mS/cm)', 'σ_thermal (mS/cm equiv)')
BASE = dict(sigma_full_mScm=.24, sigma_full_mScm_physics=.72,
    sigma_full_status='computed', sigma_full_status_physics='computed',
    network_solver_status='success', sigma_ratio=.24, sigma_grain_S_cm=.003, phi_se=.5,
    sigma_bulk_net_mScm=1., sigma_bulk_net_mScm_physics=1.,
    R_brug_over_full=7.2, R_brug_over_full_physics=2.4,
    bulk_resistance_fraction=.6, bulk_resistance_fraction_physics=.8,
    electronic_sigma_full_mScm=2., electronic_sigma_full_mScm_physics=3.,
    thermal_sigma_full_mScm=.3, thermal_sigma_full_mScm_physics=.45, tortuosity_mean=1.2)
FRESH = {ION: ['0.24', '0.72', '+200.0%'], RB: ['7.2×', '2.4×', '-66.7%'],
         CF: ['7.2×', '2.4×', '-66.7%'], SBI: ['3.0×', '1.0×', '-66.7%'],
         AMP: ['3.00×', '3.00×', '0%']}
OLD = {ION: ['17.0', '19.0', '+11.8%'], RB: ['31.0×','37.0×','+19.4%'],
       CF: ['31.0×','37.0×','+19.4%'], SBI: ['41.0×','43.0×','+4.9%'],
       AMP: ['1.12×','1.12×','0%']}

def mapped(rows):
    out = {}
    for row in rows:
        if row:
            out.setdefault(str(row[0]).strip(), []).append([str(x) for x in row[1:]])
    return out

def layout_rows(layout):
    rows = [['── Network Solver (Hertzian DEM-native) ──', '', '', '']]
    rows += [[lab, *OLD[lab]] for lab in LABS]
    rows += [[DIAG, '123.0', '456.0', '+270.7%'],
             [DIAGNOSTICS[0], '77.0', '88.0', '+14.3%'],
             [DIAGNOSTICS[1], '77.0', '88.0', '+14.3%'],
             [DIAGNOSTICS[2], '77.0', '88.0', '+14.3%'],
             ['SE Volume Fraction', '.5', '.5', '0%']]
    if layout == 'new':
        return ['metric', 'value'], [['SE Volume Fraction', '.5'], [DIAG, '123.0']]
    if layout == 'fourcol': return ['metric','H','P','delta'], rows
    rows = [[r[0], r[1]] for r in rows if r[0] != AMP]
    if layout == 'split':
        rows += [['── Physics (Plastic film, Tabor+volume) ──',''],
                 ['σ_ionic [physics] (mS/cm)', '19.0'], [AMP,'1.12×']]
    return ['metric','value'], rows

def run_case(name, metrics, layout, capture=False):
    rd, ud = WORK/'results'/name, WORK/'uploads'/name
    rd.mkdir(parents=True, exist_ok=True); ud.mkdir(parents=True, exist_ok=True)
    (rd/'full_metrics.json').write_text(json.dumps(metrics), encoding='utf-8')
    (ud/'meta.json').write_text(json.dumps(dict(name=name, status='done', scale=1)), encoding='utf-8')
    head, rows = layout_rows(layout)
    with (rd/'network_summary.csv').open('w', encoding='utf-8', newline='') as f:
        wr = csv.writer(f); wr.writerow(head); wr.writerows(rows)
    before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in rd.iterdir() if p.is_file()}
    try:
        with contextlib.redirect_stdout(QUIET):
            tables, effective, _ = app._load_case_tables(str(rd), {})
            response = CLIENT.get('/single/' + name)
        page = response.get_data(as_text=True)
        parser = Rows(); parser.feed(page)
        after = {n: hashlib.sha256((rd/n).read_bytes()).hexdigest() for n in before}
        result = dict(loader=mapped(tables['network_summary']['data']), route=mapped(parser.rows),
                      http=response.status_code, input_unchanged=before==after, effective_metrics=effective)
        if capture: (WORK/(name+'.html')).write_text(page, encoding='utf-8')
        return result
    except Exception:
        return {'exception': traceback.format_exc()}

def get_cell(result, where, lab):
    return result.get(where, {}).get(app._PAPER_LABEL_MAP.get(lab,lab))

def accepted(m, side):
    sx = '' if side == 0 else '_physics'
    return m.get('sigma_full_status'+sx) in (None,'computed') and isinstance(m.get('sigma_full_mScm'+sx),(float,int)) and m['sigma_full_mScm'+sx]>0

def expected(m, layout, lab):
    ok = [accepted(m, side) for side in (0,1)]
    if lab == AMP: return FRESH[lab] if all(ok) else ['—']*3
    vals = []
    for side in (0,1):
        sx = '' if side == 0 else '_physics'
        if not ok[side]:
            vals.append(app.MODEL_LIMIT_CELL if m.get('sigma_full_reason'+sx)=='full_over_conduction' else '—')
            continue
        has_current = lab==ION or (m.get('R_brug_over_full'+sx) is not None if lab in (RB,CF) else bool(m.get('sigma_ratio')))
        if has_current:
            vals.append(FRESH[lab][side])
        elif layout == 'new':
            vals.append('—')
        elif lab == RB and side==1 and layout!='fourcol':
            vals.append('—')
        else:
            vals.append(OLD[lab][side if layout=='fourcol' else 0])
    fresh = all(ok) and (lab==ION or (all(m.get('R_brug_over_full'+sx) is not None for sx in ('','_physics')) if lab in (RB,CF) else bool(m.get('sigma_ratio'))))
    return vals + [FRESH[lab][2] if fresh else '—']

variants = {'fresh': copy.deepcopy(BASE), 'legacy': {k:v for k,v in BASE.items() if 'status' not in k}}
for action in ('absent','null'):
    for side in ('h','p','both'):
        m = copy.deepcopy(BASE)
        for sx in (('',) if side=='h' else ('_physics',) if side=='p' else ('','_physics')):
            key = 'R_brug_over_full'+sx
            if action=='absent': m.pop(key)
            else: m[key]=None
        variants['rbrug_'+action+'_'+side] = m
    for group in ('brug','all_derived'):
        m = copy.deepcopy(BASE)
        keys = ['sigma_ratio'] + (['R_brug_over_full','R_brug_over_full_physics'] if group=='all_derived' else [])
        for key in keys:
            if action=='absent': m.pop(key)
            else: m[key]=None
        variants[group+'_'+action]=m
for kind in ('brug_null','all_derived_null'):
    variants[kind+'_no_phi'] = {k:v for k,v in variants[kind].items() if k!='phi_se'}
for status, value, reason in (('valid_zero',None,'no_through_path'), ('valid_zero',0.,'no_through_path'),
                            ('not_computed',None,'full_over_conduction'), ('not_computed',.24,'full_over_conduction'),
                            ('not_computed',None,'solve_failed'), ('unknown',None,None)):
    for side in ('h','p','both'):
        m=copy.deepcopy(BASE)
        for sx in (('',) if side=='h' else ('_physics',) if side=='p' else ('','_physics')):
            m.update({'sigma_full_status'+sx:status, 'sigma_full_mScm'+sx:value, 'sigma_full_reason'+sx:reason})
        variants[f'{status}_{value}_{reason}_{side}'] = m

results, checks = {}, []
for kind, m in variants.items():
    for layout in ('new','csv','split','fourcol'):
        name=kind+'_'+layout
        r=run_case(name,m,layout,capture=(kind in ('all_derived_null','valid_zero_0.0_no_through_path_both','not_computed_None_full_over_conduction_p') and layout=='fourcol'))
        results[name]=r
        checks.append(dict(case=name,check='HTTP200 and unchanged source inputs',passed=r.get('http')==200 and r.get('input_unchanged') is True))
        if 'exception' in r: continue
        for where in ('loader','route'):
            if where=='route' and r.get('http')!=200: continue
            for lab in LABS:
                got=get_cell(r,where,lab)
                want=expected(m,layout,lab)
                # The existing new-table route emits no ionic block if Hertz is unavailable,
                # and omits optional SBI when sigma_ratio is absent. Historical CSV retains rows.
                absent_ok = layout=='new' and (not accepted(m,0) or (lab==SBI and not m.get('sigma_ratio')) or (lab==CF and not m.get('R_brug_over_full')))
                passed = got == [want] or (absent_ok and got is None)
                checks.append(dict(case=name,where=where,lab=lab,got=got,want=[want],absent_ok=absent_ok,passed=passed))
            sentinel = ['123.0','456.0','+270.7%'] if layout=='fourcol' else ['123.0','123.0','0%']
            checks.append(dict(case=name,where=where,check='unknown diagnostic untouched',got=get_cell(r,where,DIAG),want=[sentinel],passed=get_cell(r,where,DIAG)==[sentinel]))
            for lab,want in zip(DIAGNOSTICS, (['40.0','20.0','-50.0%'],['2.00','3.00','+50.0%'],['0.300','0.450','+50.0%'])):
                got=get_cell(r,where,lab)
                passed=got==[want] or (layout=='new' and not accepted(m,0) and lab==DIAGNOSTICS[0] and got is None)
                checks.append(dict(case=name,where=where,check='nonionic/diagnostic control',lab=lab,got=got,want=[want],passed=passed))

out=dict(source=str(Path(app.__file__).resolve()), cases=results,checks=checks,
         failures=[c for c in checks if not c['passed']],stdout=QUIET.getvalue())
(REVIEW/('evidence/rr_display_extended_'+TREE+'.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
print(json.dumps(dict(cases=len(results),checks=len(checks),failed=len(out['failures']),failures=out['failures'][:12]),ensure_ascii=False))
sys.exit(bool(out['failures']))
