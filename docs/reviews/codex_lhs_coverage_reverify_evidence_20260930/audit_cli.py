import sys,os,json,subprocess
from pathlib import Path
E=Path(__file__).resolve().parent
ROOT=E.parent/'lhs_coverage_review_20260930';C=Path(os.environ.get('LHS_REVIEW_REPO',ROOT/'candidate'))
sys.path[:0]=[str(C/'scripts'),str(ROOT/'deps')]
import coverage_physics_vs_hertzian as cv
base=E/'cli_fixtures';base.mkdir(exist_ok=True)
env=dict(os.environ,PYTHONPATH=str(ROOT/'deps'),PYTHONUTF8='1',PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1',
         WEBAPP_RESULTS_FOLDER=str(base/'empty_results'),WEBAPP_ARCHIVE_FOLDER=str(base/'archive'),WEBAPP_UPLOAD_FOLDER=str(base/'uploads'))
for k in ['WEBAPP_RESULTS_FOLDER','WEBAPP_ARCHIVE_FOLDER','WEBAPP_UPLOAD_FOLDER']:Path(env[k]).mkdir(exist_ok=True)
script=str(C/'scripts/coverage_physics_vs_hertzian.py')
R={}
def run(args):
    out=subprocess.run([sys.executable,script,*args],env=env,cwd=base,capture_output=True,encoding='utf-8')
    return {'rc':out.returncode,'stdout':out.stdout,'stderr':out.stderr}
d,_,_=cv._selftest_fixture(base/'archive/category/nested')
R['nested_archive_all']=run(['--all'])
R['nested_archive_all']['v2_written']='coverage_status_physics_v2' in json.loads((d/'full_metrics.json').read_text())
env['WEBAPP_RESULTS_FOLDER']=str(base/'results')
d,_,_=cv._selftest_fixture(base/'results/external')
R['external_case_id']=run(['external'])
R['external_case_id']['v2_written']='coverage_status_physics_v2' in json.loads((d/'full_metrics.json').read_text())
d,_,_=cv._selftest_fixture(base/'results/bad_json')
(d/'full_metrics.json').write_text('{not json')
R['bad_json_case_dir']=run(['--case-dir',str(d)])
R['bad_json_case_dir']['final_metrics_text']=(d/'full_metrics.json').read_text()
(E/'cli_results.json').write_text(json.dumps(R,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(R,ensure_ascii=False,indent=2))
