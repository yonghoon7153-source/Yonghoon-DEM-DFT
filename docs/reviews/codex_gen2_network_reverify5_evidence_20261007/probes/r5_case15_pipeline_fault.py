"""Actual frozen case15 CPU pipeline, with only network child spawn denied.

No DEM/MPM solver, production campaign, or source edits. Real staging/parser/
contact/coverage plus original smoke child/evaluator; injected PermissionError
at the network subprocess boundary. Independent raw six-channel probe runs.
"""
from pathlib import Path
import contextlib, io, json, os, sys, tempfile

R = Path(__file__).resolve().parents[1]
S, E = R/'source', R/'evidence'
T = Path(tempfile.mkdtemp(prefix='r5_case15_pipeline_', dir=R/'tmp'))
for key in ('TMP', 'TEMP', 'TMPDIR'):
    os.environ[key] = str(T)
tempfile.tempdir = str(T)
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
sys.path[:0] = [str(S/'scripts'), str(S/'webapp')]
import wsl_network_smoke as smoke
smoke._setup_child_env(T)
os.chdir(T/'work')
import pipeline_service as ps
actual = ps._RUNNER
calls = []
def deny_network(cmd, **kwargs):
    if len(cmd) > 1 and Path(cmd[1]).name == 'network_conductivity.py':
        calls.append([str(x) for x in cmd])
        raise PermissionError('r5_case15 injected solver executable denied')
    return actual(cmd, **kwargs)
ps._RUNNER = deny_network
capture = io.StringIO()
try:
    with contextlib.redirect_stdout(capture), contextlib.redirect_stderr(capture):
        rep = smoke.child_case(dict(root=str(T), id='case15_network', kind='case15', stop='network', negative_control=smoke.CASE15_NEGCTL['tag']))
finally:
    ps._RUNNER = actual
checks = smoke.evaluate({'case15_network': rep}, {'case15_network': {'rc': 0}})
doc = dict(source_sha='aa7ec7fe98e8684f1a2138665f9eba978366c229', root=str(T), denied_calls=calls, report=rep,
           checks=checks, failures=[c for c in checks if c['verdict'] != 'PASS'])
(E/'r5_case15_pipeline_fault.json').write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding='utf-8')
(E/'r5_case15_pipeline_fault.log').write_text(capture.getvalue(), encoding='utf-8')
print(json.dumps(dict(root=str(T), denied=len(calls), status=rep.get('status'), failed_stages=rep.get('failed_stages'),
                     checks=len(checks), fail=len(doc['failures']), failures=doc['failures']), ensure_ascii=False), flush=True)
