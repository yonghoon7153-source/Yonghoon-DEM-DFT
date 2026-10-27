"""One-off: run the webapp's own run_pipeline (stop_after='network', figures/auto_db off — same call convention as
scripts/webapp_network_batch.py) on the six uploaded kg50 D3 cases in the isolated web dir.
Usage: python3 -P run_cases.py <worktree> <web dir>"""
import glob
import json
import os
import sys
import time

WT, WEB = sys.argv[1], sys.argv[2]
for k, sub in (('WEBAPP_UPLOAD_FOLDER', 'uploads'), ('WEBAPP_RESULTS_FOLDER', 'results'),
               ('WEBAPP_ARCHIVE_FOLDER', 'archive'), ('WEBAPP_MPM_LAB_FOLDER', 'mpm_lab')):
    os.environ[k] = os.path.join(WEB, sub)
os.environ['SUPABASE_URL'] = ''
os.environ['SUPABASE_KEY'] = ''
sys.path.insert(0, os.path.join(WT, 'scripts'))
sys.path.insert(0, os.path.join(WT, 'webapp'))
os.chdir(os.path.join(WT, 'webapp'))
import app as A  # noqa: E402

assert A.app.config['RESULTS_FOLDER'] == os.environ['WEBAPP_RESULTS_FOLDER']
for m in sorted(glob.glob(os.path.join(os.environ['WEBAPP_UPLOAD_FOLDER'], '*', 'meta.json'))):
    cid = os.path.basename(os.path.dirname(m))
    meta = json.load(open(m))
    t0 = time.time()
    with A.app.app_context():
        r = A.run_pipeline(cid, meta['mode'], meta['type_map'], int(meta.get('scale', 1000)),
                           figures=False, auto_db=False, stop_after='network')
    rd = os.path.join(os.environ['WEBAPP_RESULTS_FOLDER'], cid)
    have = sorted(f for f in ('full_metrics.json', 'network_conductivity_dual.json', 'network_provenance.json')
                  if os.path.exists(os.path.join(rd, f)))
    keys = list(r.keys())[:8] if isinstance(r, dict) else type(r).__name__
    err = r.get('error') if isinstance(r, dict) else None
    print(f'{meta["name"]} {cid} {time.time() - t0:.0f}s error={err!r} keys={keys} files={have}', flush=True)
