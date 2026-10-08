"""Feed real case15 process-fault report through S0b with proven normal folders."""
from pathlib import Path
import contextlib, io, json, os, shutil, sys, tempfile
R = Path(__file__).resolve().parents[1]
S, E = R/'source', R/'evidence'
T = Path(tempfile.mkdtemp(prefix='r5_case15_fault_reread_', dir=R/'tmp'))
for key in ('TMP', 'TEMP', 'TMPDIR'):
    os.environ[key] = str(T)
tempfile.tempdir = str(T)
os.environ.update(SUPABASE_URL='', SUPABASE_KEY='', PYTHONDONTWRITEBYTECODE='1')
sys.path[:0] = [str(S/'scripts'), str(S/'webapp')]
import g2_network_reread as rr
positive = json.loads((E/'r5_case15_s0b_positive.json').read_text(encoding='utf-8'))
fault = json.loads((E/'r5_case15_pipeline_fault.json').read_text(encoding='utf-8'))
reports = {'case15_network': fault['report']}
for case in positive['cases']:
    assert all(c['ok'] for c in case['checks'])
    shutil.copytree(case['folder'], T/'work'/'results'/case['case'])
    reports[case['case']] = dict(stop_after='network', status='done')
(T/'smoke_report.json').write_text(json.dumps(dict(reports=reports, checks=fault['checks'], rc=0), ensure_ascii=False), encoding='utf-8')
out = E/'r5_case15_pipeline_fault_reread.json'
log = io.StringIO()
with contextlib.redirect_stdout(log):
    rc = rr.main(['--smoke-root', str(T), '--json', str(out)])
(E/'r5_case15_pipeline_fault_reread.log').write_text(log.getvalue(), encoding='utf-8')
print('Actual child-case PermissionError reread rc', rc)
