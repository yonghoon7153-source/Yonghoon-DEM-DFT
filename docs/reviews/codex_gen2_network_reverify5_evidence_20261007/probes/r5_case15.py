"""Case15 diagnostic and S0b probes; only isolated CPU/synthetic work.

Positive control uses the submitted case15 record plus real published synthetic
through/nonthrough/clamp folders. Production source and submitted data are read-only.
"""
from pathlib import Path
import contextlib, copy, gzip, hashlib, io, json, os, shutil, subprocess, sys, tempfile

R = Path(__file__).resolve().parents[1]
S, E = R / 'source', R / 'evidence'
T = Path(tempfile.mkdtemp(prefix='r5_case15_', dir=R / 'tmp'))
for key in ('TMP', 'TEMP', 'TMPDIR'):
    os.environ[key] = str(T)
tempfile.tempdir = str(T)
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
os.environ.update(SUPABASE_URL='', SUPABASE_KEY='', PYTHONDONTWRITEBYTECODE='1')
for key, tail in (('WEBAPP_UPLOAD_FOLDER', 'uploads'), ('WEBAPP_RESULTS_FOLDER', 'results'), ('WEBAPP_ARCHIVE_FOLDER', 'archive'), ('WEBAPP_MPM_LAB_FOLDER', 'mpm_lab')):
    p = T / tail
    p.mkdir()
    os.environ[key] = str(p)
sys.path[:0] = [str(S / 'scripts'), str(S / 'webapp')]
import wsl_network_smoke as smoke
import g2_network_reread as rr
import app
import pipeline_service as ps
import tau_flux as tf
import test_gen2_publication_handover as PH

submitted = json.loads((R / 'submitted/g2pre_smoke_839dbac6b_1007_2224/smoke_report.json').read_text(encoding='utf-8'))
c15 = submitted['reports']['case15_network']
summary = dict(source_sha='aa7ec7fe98e8684f1a2138665f9eba978366c229', observations={}, s0b={}, producer={})

def save(name, obj):
    (E / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2, default=str) + '\n', encoding='utf-8')

def evaluate(r):
    checks = smoke.evaluate({'case15_network': r}, {'case15_network': {'rc': 0}})
    return dict(n=len(checks), failures=[c for c in checks if c['verdict'] != 'PASS'], checks=checks)

summary['producer']['submitted_positive'] = evaluate(c15)
assert not summary['producer']['submitted_positive']['failures']
stage = T / 'raw_case15'
stage.mkdir()
bed = smoke.REFBEDS['case15']
raw_files = [(src, dst, key) for src, dst, key in bed['files'] if (bed['dir'] / src).is_file()]
for src, dst, key in raw_files:
    if src.endswith('.gz'):
        with gzip.open(bed['dir'] / src, 'rb') as fi, open(stage / dst, 'wb') as fo:
            shutil.copyfileobj(fi, fo)
    else:
        shutil.copy2(bed['dir'] / src, stage / dst)
raw = smoke.case15_channel_probe(stage, c15['type_map'])
raw['raw_sha256'] = {key: hashlib.sha256((stage / dst).read_bytes()).hexdigest() for _src, dst, key in raw_files}
want = smoke.refbed_sha_table(bed['dir'])
assert all(want[key] == digest for key, digest in raw['raw_sha256'].items())
raw['snapshot_missing_files'] = [src for src, dst, key in bed['files'] if not (bed['dir'] / src).is_file()]
save('r5_case15_raw.json', raw)
fresh = copy.deepcopy(c15)
fresh['negctl'] = raw
summary['producer']['independent_raw_positive'] = evaluate(fresh)
assert not summary['producer']['independent_raw_positive']['failures']
print('Raw six-channel positive: PASS', flush=True)

smroot = T / 'smoke_consumer'
results = smroot / 'work' / 'results'
results.mkdir(parents=True)
normal = {}
with contextlib.redirect_stdout(io.StringIO()):
    for bed in ('through', 'nonthrough', 'clamp'):
        d, status, failed, rid = PH._publish(app, 'baseline', bed=bed)
        assert status == 'done', (bed, status, failed)
        shutil.copytree(d, results / bed)
        normal[bed] = dict(stop_after='network', status=status)

base = dict(reports={**normal, 'case15_network': copy.deepcopy(fresh)},
            checks=smoke.evaluate({'case15_network': fresh}, {'case15_network': {'rc': 0}}), rc=0)

def reread(label, doc):
    smoke.write_json(smroot / 'smoke_report.json', doc)
    jp = E / f'r5_case15_s0b_{label}.json'
    log = io.StringIO()
    with contextlib.redirect_stdout(log):
        rc = rr.main(['--smoke-root', str(smroot), '--json', str(jp)])
    j = json.loads(jp.read_text(encoding='utf-8'))
    d = dict(rc=rc, n_fail=j['n_fail'], meta=j['meta'], normal=[{'case': c['case'], 'failures': [x['name'] for x in c['checks'] if not x['ok']]} for c in j['cases']])
    summary['s0b'][label] = d
    print(label, rc, j['n_fail'], flush=True)
    return d

assert reread('positive', base)['rc'] == 0

for label in ('marker_missing', 'marker_unknown', 'checks_missing', 'checks_three', 'check_fail', 'one_check_repeated_four', 'negctl_missing', 'tau_numeric', 'ionic_residual_bad', 'raw_sha_fail', 'unexpected_failure_record'):
    doc = copy.deepcopy(base)
    r = doc['reports']['case15_network']
    negchecks = [c for c in doc['checks'] if '[음성 대조]' in c['name']]
    if label == 'marker_missing':
        r.pop('negative_control')
    elif label == 'marker_unknown':
        r['negative_control'] = 'unregistered_future_control'
    elif label == 'checks_missing':
        doc['checks'] = []
    elif label == 'checks_three':
        doc['checks'] = negchecks[:3]
    elif label == 'check_fail':
        negchecks[-1]['verdict'] = 'FAIL'
    elif label == 'one_check_repeated_four':
        doc['checks'] = [copy.deepcopy(negchecks[0]) for _ in range(4)]
    elif label == 'negctl_missing':
        r.pop('negctl')
    elif label == 'tau_numeric':
        r['tau']['tau_ion_hertz'] = 1.0
    elif label == 'ionic_residual_bad':
        r['negctl']['channels']['ionic_physics']['residual_rel'] = 0.1
    elif label == 'raw_sha_fail':
        r['raw_sha_ok'] = False
        doc['checks'] = smoke.evaluate({'case15_network': r}, {'case15_network': {'rc': 0}})
        doc['rc'] = 1
    elif label == 'unexpected_failure_record':
        r['attempt']['reason'] = 'PermissionError: solver executable denied'
        for step in r['stages']:
            if step['step'] == smoke.CASE15_NEGCTL['solver_step']:
                step.update(rc=1, err='PermissionError: solver executable denied')
        doc['checks'] = smoke.evaluate({'case15_network': r}, {'case15_network': {'rc': 0}})
    reread(label, doc)
    summary['producer'][label] = evaluate(r)

# Actual pipeline stage execution failure through the real failure-publication
# path, with a synthetic CSV fixture and independently recomputed frozen raw
# case15 diagnostic. This is not a re-run of the real DEM pipeline.
faultdir = T / 'results' / 'case15_network'
faultdir.mkdir()
atoms, contacts = PH.TP._write_bed(str(faultdir), 'through')
log = []
def failing_runner(cmd, **kwargs):
    return subprocess.CompletedProcess(cmd, 2, '', 'PermissionError: solver executable denied')
stages, rid = app._network_and_stage_e(str(faultdir), str(S/'scripts'), atoms, contacts, '1:SE', 1, log, runner=failing_runner, stop_before_stage_e=True)
status, failed = ps.summarize(stages)
out = dict(status=status, success=status=='done', failed_stages=[s['step'] for s in failed], network_run_id=rid, log=log)
r = copy.deepcopy(fresh)
r.update(smoke.collect(app, ps, tf, 'case15_network', out, 0))
summary['producer']['real_failure_path_synthetic_input'] = evaluate(r)
summary['observations']['real_failure_path'] = dict(status=status, failed=failed, stages=stages, attempt=r['attempt'], tau=r['tau'], caveat='Synthetic CSV stage fixture; raw case15 probe is independent, from pinned raw data.')
doc = copy.deepcopy(base)
doc['reports']['case15_network'] = r
doc['checks'] = summary['producer']['real_failure_path_synthetic_input']['checks']
reread('real_failure_path_synthetic_input', doc)
save('r5_case15_results.json', summary)
print('Evidence saved:', E / 'r5_case15_results.json', flush=True)
