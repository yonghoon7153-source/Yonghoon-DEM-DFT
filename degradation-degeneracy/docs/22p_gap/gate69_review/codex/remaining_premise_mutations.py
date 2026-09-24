"""Portable local mutation controls for the three older premise mutations.
Not the official Linux replay certificate; original source stays untouched.
"""
import hashlib,json,os,pathlib,sys
from review_checks import HERE,DD,env,run,dump
e=env(pathlib.Path('C:/Users/Administrator/Documents/Codex/g69tmp_04'));os.environ.update(e)
sys.path.insert(0,str(DD/'docs/22p_gap'));import mutation_replay as mr
names={'the-fixture-measures-its-premise-g65','the-premise-uses-a-controlled-env-g66',
       'the-premise-checks-the-child-actually-ran-g67'}
out=HERE/'older_premise_mutations';out.mkdir(exist_ok=False)
results=[]
for name,source,old,new,selector in mr.MUTANTS:
    if name not in names:continue
    work=mr._make_sandbox();p=work/source.relative_to(DD);before=p.read_bytes()
    assert before.count(old.encode())==1
    row=dict(name=name,sandbox=str(work),source_sha256=hashlib.sha256(before).hexdigest(),phases={})
    for phase in ('baseline','mutant'):
        if phase=='mutant':p.write_bytes(before.replace(old.encode(),new.encode(),1))
        report=out/(name+'.'+phase+'.pytest.json')
        argv=[sys.executable,'-X','utf8','-B','-m','pytest','tests/test_gate65_defensive.py',
              'tests/test_gate66_defensive.py','tests/test_gate67_defensive.py','tests/test_gate68_defensive.py',
              '--noconftest','-q','-p','no:cacheprovider','-k',selector,
              '--json-report','--json-report-file='+str(report)]
        r=run('older_premise_mutations/'+name+'.'+phase,argv,cwd=work,environment=e,timeout=120)
        data=json.loads(report.read_text(encoding='utf-8'));expected=mr.EXPECT[name]
        failed={x['nodeid']:x for x in data['tests'] if x['outcome']=='failed'}
        row['phases'][phase]=dict(rc=r.returncode,summary=data['summary'],expected=expected,failed=list(failed),
            exact_failed_set=set(failed)==set(expected['fail']),
            call_only=all(x.get('call',{}).get('outcome')=='failed' and x.get('setup',{}).get('outcome')=='passed'
                          and x.get('teardown',{}).get('outcome')=='passed' for x in failed.values()),
            witnesses={n:expected['witness'][n] in str(x.get('call',{}).get('longrepr','')) for n,x in failed.items() if n in expected['witness']})
    row['original_unchanged']=source.read_bytes()==before;results.append(row)
    dump(out/'RESULTS.json',results)
    print(name,row['phases']['mutant']['exact_failed_set'],row['phases']['mutant']['witnesses'],flush=True)
assert len(results)==3
