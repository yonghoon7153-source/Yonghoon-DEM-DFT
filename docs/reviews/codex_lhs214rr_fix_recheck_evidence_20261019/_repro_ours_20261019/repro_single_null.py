"""읽기 전용 파생 — Codex L214RR2-04 (과거 sigma_ratio null → /single 500) 를 우리 트리 웹앱에서 (Flask test client · 작업 폴더 = 인자).
python3 -B repro_single_null.py <우리 트리> <작업 폴더> <out.json>"""
import contextlib
import csv
import io
import json
import os
import sys
from pathlib import Path
TREE, WORK, OUT = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3])
for key, name in (('WEBAPP_UPLOAD_FOLDER', 'uploads'), ('WEBAPP_RESULTS_FOLDER', 'results'), ('WEBAPP_ARCHIVE_FOLDER', 'archive'),
                  ('WEBAPP_MPM_LAB_FOLDER', 'mpm'), ('MPLCONFIGDIR', 'mpl')):
    os.environ[key] = str(WORK / name)
os.environ['SUPABASE_URL'] = os.environ['SUPABASE_KEY'] = ''
sys.path[:0] = [str(TREE / 'webapp'), str(TREE / 'scripts')]
sys.dont_write_bytecode = True
with contextlib.redirect_stdout(io.StringIO()):
    import app  # noqa: E402
app.app.config['TESTING'] = True
app.app.config['PROPAGATE_EXCEPTIONS'] = False
C = app.app.test_client()
BASE = dict(sigma_full_mScm=.24, sigma_full_mScm_physics=.72, sigma_full_status='computed', sigma_full_status_physics='computed',
            network_solver_status='success', sigma_ratio=.24, sigma_grain_S_cm=.003, phi_se=.5, sigma_bulk_net_mScm=1., sigma_bulk_net_mScm_physics=1.,
            R_brug_over_full=7.2, R_brug_over_full_physics=2.4, bulk_resistance_fraction=.6, bulk_resistance_fraction_physics=.8,
            electronic_sigma_full_mScm=2., electronic_sigma_full_mScm_physics=3., thermal_sigma_full_mScm=.3, thermal_sigma_full_mScm_physics=.45,
            tortuosity_mean=1.2)
ROWS = [['── Network Solver (Hertzian DEM-native) ──', '', '', ''], ['σ_ionic (mS/cm)', '17.0', '19.0', '+11.8%'], ['SE Volume Fraction', '.5', '.5', '0%']]


def case(name, mut):
    m = dict(BASE)
    for k, v in mut.items():
        if v == '__drop__':
            m.pop(k, None)
        else:
            m[k] = v
    rd, ud = WORK / 'results' / name, WORK / 'uploads' / name
    rd.mkdir(parents=True, exist_ok=True)
    ud.mkdir(parents=True, exist_ok=True)
    (rd / 'full_metrics.json').write_text(json.dumps(m), encoding='utf-8')
    (ud / 'meta.json').write_text(json.dumps(dict(name=name, status='done', scale=1)), encoding='utf-8')
    with (rd / 'network_summary.csv').open('w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['metric', 'H', 'P', 'delta'])
        w.writerows(ROWS)
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        r = C.get('/single/' + name)
    return r.status_code


res = {'normal': case('s04_normal', {}), 'sigma_ratio_null': case('s04_sr_null', {'sigma_ratio': None}),
       'sigma_ratio_absent': case('s04_sr_absent', {'sigma_ratio': '__drop__'}),
       'sigma_ratio_null_no_phi': case('s04_sr_null_nophi', {'sigma_ratio': None, 'phi_se': '__drop__'}),
       'R_brug_null': case('s04_rb_null', {'R_brug_over_full': None})}
OUT.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(res))
