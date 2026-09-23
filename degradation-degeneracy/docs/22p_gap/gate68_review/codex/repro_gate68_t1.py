"""Real child pytest: --setup-only vs genuine calls. No target edits."""
import argparse, importlib.util, json, os, pathlib, sys
p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);a=p.parse_args()
HERE=pathlib.Path(__file__).resolve().parent
out=HERE/'t1_setup_only';out.mkdir(exist_ok=False)
temp=pathlib.Path('C:/Users/Administrator/Documents/Codex/g68_20260924_setup')
temp.mkdir(exist_ok=False);os.environ.update(TMP=str(temp),TEMP=str(temp),PYTHONUTF8='1',PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1')
spec=importlib.util.spec_from_file_location('reviewed_gate66',a.repo/'tests/test_gate66_defensive.py')
tm=importlib.util.module_from_spec(spec);spec.loader.exec_module(tm)
rows=[]
for name,option in [('control',''),('collect_only','--collect-only'),('setup_only','--setup-only')]:
    junit=out/(name+'.xml');jreport=out/(name+'.pytest.json')
    opts=option+' --json-report --json-report-file="'+jreport.as_posix()+'"'
    q=tm._premise_run(sys.executable,{'PYTEST_ADDOPTS':opts},junit)
    (out/(name+'.stdout.txt')).write_text(q.stdout,encoding='utf-8')
    (out/(name+'.stderr.txt')).write_text(q.stderr,encoding='utf-8')
    try:
        unmeasured=tm.assert_premise_actually_ran(q,junit); verdict={'accepted':True,'unmeasured':unmeasured}
    except Exception as e:verdict={'accepted':False,'error':type(e).__name__,'message':str(e)}
    j=json.loads(jreport.read_text(encoding='utf-8')) if jreport.exists() else {}
    row=dict(case=name,actual_argv=q.args,rc=q.returncode,consumer=verdict,
             junit_outcomes=tm._premise_outcomes(junit) if junit.exists() else None,
             json_summary=j.get('summary'),
             phases=[{'nodeid':t['nodeid'],'outcome':t['outcome'],'phases':{k:t[k].get('outcome') for k in ('setup','call','teardown') if k in t}} for t in j.get('tests',[])])
    rows.append(row);print(json.dumps(row,ensure_ascii=True),flush=True)
(out/'RESULTS.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
