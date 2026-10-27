"""One-off: upload the six kg50 D3 beds through the REAL webapp /upload route (Flask test client), isolated folders.
Usage: python3 -I upload_cases.py <worktree> <input dir> <web dir>"""
import glob
import json
import os
import sys

WT, IN, WEB = sys.argv[1], sys.argv[2], sys.argv[3]
for k, sub in (('WEBAPP_UPLOAD_FOLDER', 'uploads'), ('WEBAPP_RESULTS_FOLDER', 'results'),
               ('WEBAPP_ARCHIVE_FOLDER', 'archive'), ('WEBAPP_MPM_LAB_FOLDER', 'mpm_lab')):
    os.environ[k] = os.path.join(WEB, sub)
    os.makedirs(os.environ[k], exist_ok=True)
os.environ['SUPABASE_URL'] = ''
os.environ['SUPABASE_KEY'] = ''
sys.path.insert(0, os.path.join(WT, 'scripts'))
sys.path.insert(0, os.path.join(WT, 'webapp'))
os.chdir(os.path.join(WT, 'webapp'))
import app as A  # noqa: E402

assert A.app.config['UPLOAD_FOLDER'] == os.environ['WEBAPP_UPLOAD_FOLDER'], A.app.config['UPLOAD_FOLDER']
c = A.app.test_client()
NAMES = ['kg50_d3_b40_s1', 'kg50_d3_b40_s2', 'kg50_d3_b40_s3', 'kg50_d3_b50_s1', 'kg50_d3_b50_s2', 'kg50_d3_b50_s3']
for n in NAMES:
    d = os.path.join(IN, n)
    files = [os.path.join(d, f'input_{n}.liggghts')] + sorted(glob.glob(os.path.join(d, f'post_{n}', '*_end_*')))
    assert len(files) == 4, files
    data = {'case_name': n, 'mode': 'auto', 'type_map': '', 'ps_ratio': 'P only', 'scale': '1000',
            'files': [(open(f, 'rb'), os.path.basename(f)) for f in files]}
    r = c.post('/upload', data=data, content_type='multipart/form-data')
    print(n, r.status_code, r.get_data(as_text=True)[:200].replace('\n', ' '))
for m in sorted(glob.glob(os.path.join(os.environ['WEBAPP_UPLOAD_FOLDER'], '*', 'meta.json'))):
    j = json.load(open(m))
    print(os.path.basename(os.path.dirname(m)), j.get('name'), j.get('mode'), j.get('type_map'), j.get('type_map_resolved'),
          j.get('ps_ratio'), j.get('scale'), j.get('files'))
