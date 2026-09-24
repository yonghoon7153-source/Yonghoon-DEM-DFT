"""Recipient-owned Gate 69 checks. Never runs scientific fits or changes target code."""
from __future__ import annotations
import copy, hashlib, importlib.util, json, os, pathlib, shutil, subprocess, sys, time, zipfile

HERE = pathlib.Path(__file__).resolve().parent
REPO = pathlib.Path('C:/Users/Administrator/Documents/Codex/g69_20260924')
DD = REPO / 'degradation-degeneracy'
HEAD = 'e6ddcd1efb7df4be69849a4fd5b59c43cccff873'
REQUEST_COMMIT = 'afab648'
BASE = 'a1979cdf5b9f04234b6a441150e161bd4f0a3ced'
SCOPE = ['src','tools','configs','scripts','run.sh','requirements*.txt']

def sha(b): return hashlib.sha256(b).hexdigest()
def dump(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
def git(*args): return subprocess.check_output(['git',*args], cwd=REPO)
def env(temp):
    temp.mkdir(exist_ok=False)
    e = os.environ.copy()
    e.update(TMP=str(temp),TEMP=str(temp),PYTHONUTF8='1',PYTHONIOENCODING='utf-8',
             PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
    for k in ('PYTEST_ADDOPTS','PYTEST_PLUGINS','PYTEST_CURRENT_TEST'): e.pop(k,None)
    return e
def run(name, argv, cwd=DD, environment=None, timeout=180):
    start=time.monotonic()
    r=subprocess.run(argv,cwd=cwd,env=environment,capture_output=True,timeout=timeout)
    (HERE/(name+'.stdout.bin')).write_bytes(r.stdout)
    (HERE/(name+'.stderr.bin')).write_bytes(r.stderr)
    row=dict(argv=list(map(str,argv)),cwd=str(cwd),rc=r.returncode,seconds=time.monotonic()-start,
             stdout_sha256=sha(r.stdout),stderr_sha256=sha(r.stderr))
    dump(HERE/(name+'.json'),row)
    print(json.dumps(row,ensure_ascii=True),flush=True)
    return r

def identity():
    request=pathlib.Path('C:/Users/Administrator/Downloads/GATE69_REQUEST.md').read_bytes()
    blob=git('show',f'{HEAD}:degradation-degeneracy/docs/22p_gap/GATE69_REQUEST.md')
    (HERE/'GATE69_REQUEST_RECEIVED.md').write_bytes(request)
    (HERE/'GATE69_REQUEST_GIT_BLOB.md').write_bytes(blob)
    row=dict(head=git('rev-parse','HEAD').decode().strip(),request_commit=git('rev-parse',REQUEST_COMMIT).decode().strip(),
             request_received_sha256=sha(request),request_blob_sha256=sha(blob),request_raw_equal=request==blob,
             request_normalized_equal=request.replace(b'\r\n',b'\n')==blob.replace(b'\r\n',b'\n'),
             status_before=git('status','--porcelain=v1').decode(),python=sys.version,executable=sys.executable)
    for key,args in {
        'request_to_head_dd':['diff','--name-status',REQUEST_COMMIT,HEAD,'--','degradation-degeneracy'],
        'base_to_head_dd':['diff','--name-status',BASE,HEAD,'--','degradation-degeneracy'],
        'scope_diff':['-C',str(DD),'diff','--name-status','743f65bead671bf353ce38027c2e8e457738ec08',HEAD,'--',*SCOPE],
        'scope_log':['-C',str(DD),'log','--oneline','743f65bead671bf353ce38027c2e8e457738ec08..'+HEAD,'--',*SCOPE],
        'history':['log','-12','--format=%H %s',HEAD],
    }.items():
        data=git(*args);(HERE/(key+'.txt')).write_bytes(data);row[key]=data.decode('utf-8')
    dump(HERE/'IDENTITY.json',row)
    run('source_digest',[sys.executable,'-X','utf8','-B','-c','from src.io import source_digest; print(source_digest())'])
    print(json.dumps({k:v for k,v in row.items() if k not in ('base_to_head_dd','history')},ensure_ascii=True),flush=True)

def tests():
    e=env(pathlib.Path('C:/Users/Administrator/Documents/Codex/g69tmp_01'))
    argv=[sys.executable,'-X','utf8','-B','-m','pytest',
          'tests/test_gate66_defensive.py','tests/test_gate67_defensive.py','tests/test_gate68_defensive.py',
          '--noconftest','-q','-p','no:cacheprovider','--basetemp='+str(pathlib.Path(e['TEMP'])/'outer'),
          '--junitxml='+str(HERE/'targeted.xml'),'--json-report','--json-report-file='+str(HERE/'targeted.pytest.json')]
    run('targeted',argv,environment=e,timeout=240)
    run('preimages',[sys.executable,'-X','utf8','-B','docs/22p_gap/mutation_replay.py','--check-preimages'],environment=e)

def boundaries():
    e=env(pathlib.Path('C:/Users/Administrator/Documents/Codex/g69tmp_02'));os.environ.update(e)
    sys.path.insert(0,str(DD/'tests'));import test_gate66_defensive as tm
    out=HERE/'boundaries';out.mkdir(exist_ok=False)
    results={};clean=None
    cases=[('clean',{},None),('nousersite',{'PYTHONNOUSERSITE':'1'},None),
           ('setup_only',{'PYTEST_ADDOPTS':'--setup-only'},None),
           ('collect_only',{'PYTEST_ADDOPTS':'--collect-only'},None),
           ('usage_error',{'PYTEST_ADDOPTS':'--g69-no-such-option'},None),
           ('inherited_setup_only',{},'--setup-only'),('disable_autoload',{'PYTEST_DISABLE_PLUGIN_AUTOLOAD':'1'},None)]
    for name,extra,ambient in cases:
        if ambient:os.environ['PYTEST_ADDOPTS']=ambient
        else:os.environ.pop('PYTEST_ADDOPTS',None)
        junit=out/(name+'.xml');start=time.monotonic();r=tm._premise_run(sys.executable,extra,junit)
        (out/(name+'.stdout.txt')).write_text(r.stdout,encoding='utf-8')
        (out/(name+'.stderr.txt')).write_text(r.stderr,encoding='utf-8')
        records=tm._phase_records(tm._phase_witness_path(junit)) if tm._phase_witness_path(junit).exists() else []
        row=dict(child_rc=r.returncode,seconds=time.monotonic()-start,records=records,
                 call_count=sum(x['when']=='call' for x in records))
        try:row.update(consumer='ACCEPTED',unmeasured=tm.assert_premise_actually_ran(r,junit))
        except Exception as exc:row.update(consumer='REJECTED',exception=type(exc).__name__,reason=str(exc))
        results[name]=row
        if name=='clean':clean=(r,junit,records)
        dump(out/'REAL_CHILD_RESULTS.json',results)
        print(name,row['child_rc'],row['call_count'],row['consumer'],flush=True)
    os.environ.pop('PYTEST_ADDOPTS',None)
    r,junit,recs=clean
    assert results['clean']['consumer']=='ACCEPTED'
    tests={}
    mutations={
        'missing_call':lambda rs:[x for x in rs if x['when']!='call'],
        'duplicate_call':lambda rs:rs+[copy.deepcopy(next(x for x in rs if x['when']=='call'))],
        'setup_failure':lambda rs:[dict(x,outcome='failed') if i==0 else x for i,x in enumerate(rs)],
        'teardown_failure':lambda rs:[dict(x,outcome='failed') if x['when']=='teardown' else x for x in rs],
        'wrong_node':lambda rs:[dict(x,nodeid='tests/alien.py::'+x['nodeid'].split('::')[1]) for x in rs],
        'bad_call_outcome':lambda rs:[dict(x,outcome='unknown') if x['when']=='call' else x for x in rs],
        'empty':lambda rs:[],
    }
    for name,mutate in mutations.items():
        dst=out/(name+'.xml');dst.write_bytes(junit.read_bytes())
        tm._phase_witness_path(dst).write_text(''.join(json.dumps(x)+'\n' for x in mutate(copy.deepcopy(recs))),encoding='utf-8')
        try:tests[name]=dict(consumer='ACCEPTED',unmeasured=tm.assert_premise_actually_ran(r,dst))
        except Exception as exc:tests[name]=dict(consumer='REJECTED',exception=type(exc).__name__,reason=str(exc))
    dump(out/'RECIPIENT_RECORD_CASES.json',tests)
    assert results['setup_only']['consumer']=='REJECTED' and results['setup_only']['call_count']==0
    assert all(x['consumer']=='REJECTED' for x in tests.values())

def mutation():
    e=env(pathlib.Path('C:/Users/Administrator/Documents/Codex/g69tmp_03'));os.environ.update(e)
    sys.path.insert(0,str(DD/'docs/22p_gap'));import mutation_replay as mr
    names=[x for x in mr.MUTANTS if x[0]=='the-premise-checks-the-call-phase-g68'];assert len(names)==1
    name,source,old,new,selector=names[0]
    # Full source tree copied by the registered sandbox builder. No original mutation.
    work=mr._make_sandbox();target=work/source.relative_to(DD);before=target.read_bytes()
    assert before.count(old.encode())==1
    out=HERE/'mutation';out.mkdir(exist_ok=False);rows={}
    for phase in ('baseline','mutant'):
        if phase=='mutant':target.write_bytes(before.replace(old.encode(),new.encode(),1))
        report=out/(phase+'.pytest.json')
        argv=[sys.executable,'-X','utf8','-B','-m','pytest','tests/test_gate68_defensive.py','--noconftest','-q',
              '-p','no:cacheprovider','-k',selector,'--json-report','--json-report-file='+str(report)]
        r=run('mutation/'+phase,argv,cwd=work,environment=e,timeout=180)
        data=json.loads(report.read_text(encoding='utf-8'))
        failed={x['nodeid']:x for x in data['tests'] if x['outcome']=='failed'}
        expected=mr.EXPECT[name]
        rows[phase]=dict(rc=r.returncode,summary=data['summary'],failed=list(failed),
            expected=expected,exact_failed_set=set(failed)==set(expected['fail']),
            call_only=all(x.get('call',{}).get('outcome')=='failed' and x.get('setup',{}).get('outcome')=='passed'
                          and x.get('teardown',{}).get('outcome')=='passed' for x in failed.values()),
            witnesses={n:expected['witness'][n] in str(x.get('call',{}).get('longrepr','')) for n,x in failed.items() if n in expected['witness']})
    dump(out/'RESULTS.json',dict(name=name,sandbox=str(work),rows=rows,original_unchanged=source.read_bytes()==before))
    print(json.dumps(rows,ensure_ascii=True),flush=True)

def manifests():
    results={}
    for gate,man in [(66,'MANIFEST.json'),(67,'REVIEW_MANIFEST.json'),(68,'MANIFEST.json')]:
        base=f'degradation-degeneracy/docs/22p_gap/gate{gate}_review/codex'
        mbytes=git('show',f'{HEAD}:{base}/{man}');m=json.loads(mbytes)
        entries=m.get('files') or next(v for v in m.values() if isinstance(v,list))
        rows=[]
        for entry in entries:
            p=entry.get('path') or entry.get('file');b=git('show',f'{HEAD}:{base}/{p}')
            prior=git('show',f'90c766f^:{base}/{p}')
            rows.append(dict(path=p,expected=entry['sha256'],git_sha256=sha(b),size=len(b),
                             match=sha(b)==entry['sha256'],prior_match=sha(prior)==entry['sha256']))
        zips=list((REPO/base).parent.glob('*.zip'));archives=[]
        for zp in zips:
            with zipfile.ZipFile(zp) as z:
                matches=[n for n in z.namelist() if n.split('/')[-1]==man]
                one=dict(name=zp.name,bytes=zp.stat().st_size,sha256=sha(zp.read_bytes()),crc_bad=z.testzip(),manifests=matches)
                if len(matches)==1:
                    zm=z.read(matches[0]);prefix=matches[0][:-len(man)];bad=[]
                    for e1 in entries:
                        pn=e1.get('path') or e1.get('file');zb=z.read(prefix+pn)
                        if sha(zb)!=e1['sha256']:bad.append(pn)
                    one.update(manifest_raw_equal=zm==mbytes,payload_mismatches=bad)
                archives.append(one)
        results[str(gate)]=dict(total=len(rows),match_count=sum(x['match'] for x in rows),prior_mismatch_count=sum(not x['prior_match'] for x in rows),rows=rows,archives=archives)
        dump(HERE/'GIT_BLOB_MANIFEST_CHECKS.json',results)
        print(gate,len(rows),sum(x['match'] for x in rows),'prior mismatches',sum(not x['prior_match'] for x in rows),flush=True)

if __name__=='__main__':globals()[sys.argv[1]]()
