"""Four registered mutations, portable supplemental evidence; NOT official Linux replay."""
import hashlib,json,os,pathlib,subprocess,sys,tempfile,time
from run_checks import HERE,dump
root=pathlib.Path('C:/Users/Administrator/Documents/Codex/r68_20260924/degradation-degeneracy')
temp=pathlib.Path('C:/Users/Administrator/Documents/Codex/g68_20260924_m1');temp.mkdir(exist_ok=False)
os.environ.update(TMP=str(temp),TEMP=str(temp),PYTHONUTF8='1',PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1')
out=HERE/'gate_mutations';out.mkdir(exist_ok=False)
sys.path.insert(0,str(root/'docs/22p_gap'));import mutation_replay as mr
names={'usercustomize-follows-the-startup-activation-g64','the-premise-uses-a-controlled-env-g66',
       'zip-bytes-come-from-the-archive-member-g67','the-premise-checks-the-child-actually-ran-g67'}
summary=[]
for name,source,old,new,selector in mr.MUTANTS:
    if name not in names:continue
    work=mr._make_sandbox();path=work/source.relative_to(root);before=path.read_bytes()
    assert before.count(old.encode())==1
    phases={}
    for phase in ('baseline','mutant'):
        if phase=='mutant':path.write_bytes(before.replace(old.encode(),new.encode(),1))
        report=out/(name+'.'+phase+'.json')
        cmd=[sys.executable,'-X','utf8','-B','-m','pytest','tests/test_gate64_defensive.py','tests/test_gate65_defensive.py','tests/test_gate66_defensive.py','tests/test_gate67_defensive.py','--noconftest','-q','-p','no:cacheprovider','-k',selector,'--json-report','--json-report-file='+str(report)]
        t=time.monotonic();r=subprocess.run(cmd,cwd=work,env=os.environ.copy(),capture_output=True,timeout=120)
        (out/(name+'.'+phase+'.stdout.bin')).write_bytes(r.stdout);(out/(name+'.'+phase+'.stderr.bin')).write_bytes(r.stderr)
        data=json.loads(report.read_text(encoding='utf-8')) if report.exists() else {}
        failed={x['nodeid']:x for x in data.get('tests',[]) if x['outcome']=='failed'};expected=mr.EXPECT[name]
        phases[phase]=dict(argv=cmd,rc=r.returncode,seconds=time.monotonic()-t,summary=data.get('summary'),
            failures=list(failed),exact_set=set(failed)==set(expected['fail']),
            call_only=all(x.get('call',{}).get('outcome')=='failed' and x.get('setup',{}).get('outcome')=='passed' and x.get('teardown',{}).get('outcome')=='passed' for x in failed.values()),
            witness={node:expected['witness'][node] in str(x.get('call',{}).get('longrepr','')) for node,x in failed.items() if node in expected['witness']})
    row=dict(name=name,work=str(work),preimage_sha=hashlib.sha256(before).hexdigest(),phases=phases,target_unchanged=source.read_bytes()==before,expected=expected)
    summary.append(row);dump(out/'RESULTS.json',summary);print(json.dumps(row,ensure_ascii=True),flush=True)
assert len(summary)==4
