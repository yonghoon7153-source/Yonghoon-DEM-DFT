"""Reviewer orchestration. No production edits or long scientific runs."""
import argparse, hashlib, json, os, pathlib, shutil, subprocess, sys, time
HERE = pathlib.Path(__file__).resolve().parent
WS = HERE.parents[1]
REPO = WS / 'work/r17-gate68-a1979cdf'
BMS = REPO / 'bms-balancing'
DD = REPO / 'degradation-degeneracy'
ENV = dict(os.environ, PYTHONUTF8='1', PYTHONIOENCODING='utf-8',
           PYTHONDONTWRITEBYTECODE='1', OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
def dump(p, x):
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
def run(name, cmd, cwd, timeout=300):
    begin=time.monotonic()
    try:
        p=subprocess.run(list(map(str,cmd)),cwd=cwd,env=ENV,capture_output=True,timeout=timeout)
        rc=p.returncode; out=p.stdout; err=p.stderr; expired=False
    except subprocess.TimeoutExpired as e:
        rc=None;out=e.stdout or b'';err=e.stderr or b'';expired=True
    (HERE/(name+'.stdout.bin')).write_bytes(out)
    (HERE/(name+'.stderr.bin')).write_bytes(err)
    x=dict(argv=list(map(str,cmd)),cwd=str(cwd),rc=rc,timeout=expired,seconds=time.monotonic()-begin,
           stdout_sha256=hashlib.sha256(out).hexdigest(),stderr_sha256=hashlib.sha256(err).hexdigest())
    dump(HERE/(name+'.json'),x)
    print(json.dumps(x,ensure_ascii=True),flush=True)
    print(out.decode('utf-8','replace')[-2000:]); print(err.decode('utf-8','replace')[-1000:])
    return x
def old_copy(src, dst):
    dst.parent.mkdir(parents=True,exist_ok=True)
    if not dst.exists():shutil.copyfile(src,dst)
    assert src.read_bytes()==dst.read_bytes()
    return dst
def main():
    global REPO, BMS, DD
    a=argparse.ArgumentParser(); a.add_argument('part',choices=['identity','fast','producer','bms-targeted','gate-targeted','gate-boundaries','gate-inherited','gate-preimages','source-digest'])
    a.add_argument('--temp',type=pathlib.Path)
    a.add_argument('--repo',type=pathlib.Path)
    opts=a.parse_args();part=opts.part
    if opts.repo:
        REPO=opts.repo.resolve();BMS=REPO/'bms-balancing';DD=REPO/'degradation-degeneracy'
    if opts.temp:
        opts.temp.mkdir(parents=True,exist_ok=False)
        ENV.update(TMP=str(opts.temp.resolve()),TEMP=str(opts.temp.resolve()))
    py=[sys.executable,'-X','utf8','-B']
    if part=='identity':
        for label,args in {
            'head':['rev-parse','HEAD'], 'status_before':['status','--porcelain'],
            'r17_response_delta':['diff','fcb54da3','HEAD','--','bms-balancing/bms_balancing','bms-balancing/reviews'],
            'r17_all_delta':['diff','--stat','fcb54da3','HEAD','--','bms-balancing'],
            'gate_send_delta':['diff','a31be7a9','HEAD','--','degradation-degeneracy'],
            'gate_changed':['diff','--stat','cdc49e91','HEAD','--','degradation-degeneracy'],
            'r17_code_diff':['diff','e834b01e','HEAD','--','bms-balancing/scripts/gc_partial.py','bms-balancing/scripts/width_report.py','bms-balancing/scripts/verify_run_receipt.py','bms-balancing/bms_balancing/schema.py','bms-balancing/bms_balancing/verify.py'],
            'gate_code_diff':['diff','cdc49e91','HEAD','--','degradation-degeneracy/docs/22p_gap/mutation_replay.py','degradation-degeneracy/tests/test_gate66_defensive.py','degradation-degeneracy/tests/test_gate67_defensive.py'],
        }.items():run(label,['git',*args],REPO)
        run('run_scope_log',['git','log','-1','--format=%H','--','src','tools','configs','scripts','run.sh','requirements*.txt'],DD)
        run('source_digest',py+['-c','from src.io import source_digest; print(source_digest())'],DD)
    elif part in ('fast','producer'):
        script=old_copy(WS/'outputs/r17_followup3_e834b01/repro_followup3.py',HERE/'r17_repros/repro_followup3.py')
        run('r17_'+part,py+[script,'--target',BMS,'--part',part],HERE,600)
    elif part=='bms-targeted':
        run('r17_targeted',py+['-m','pytest','tests/test_r17_followup3.py','-q','-p','no:cacheprovider','-k','fu3_14 or fu3_15 or fu3_16 or fu3_17 or fu3_18 or fu3_19 or fu3_20 or fu3_21 or fu3_22','--junitxml='+str(HERE/'r17_targeted.xml'),'--basetemp='+str(HERE/'bms_tmp')],BMS,180)
    elif part=='gate-targeted':
        # Linux conftest /proc+fcntl is not available here. Explicitly limited portable test scope.
        label='gate_targeted_isolated' if opts.temp else 'gate_targeted'
        run(label,py+['-m','pytest','tests/test_gate67_defensive.py','tests/test_gate66_defensive.py','tests/test_gate65_defensive.py','tests/test_gate64_defensive.py','--noconftest','-q','-p','no:cacheprovider','-k','not kernel_lock_probe_control_actually','--junitxml='+str(HERE/(label+'.xml')),'--basetemp='+str((opts.temp/'outer') if opts.temp else HERE/'gate_tmp')],DD,240)
    elif part in ('gate-boundaries','gate-inherited'):
        name='repro_boundaries.py' if part=='gate-boundaries' else 'repro_premise_no_execution.py'
        script=old_copy(WS/'outputs/gate67_review_20260922'/name,HERE/name)
        label=part+('_short' if opts.repo else '')
        run(label,py+[script,'--repo',DD,'--out',HERE/label],HERE,300)
    elif part=='source-digest':
        run('source_digest_gate_env',py+['-c','from src.io import source_digest; print(source_digest())'],DD)
    else:
        run('gate_preimages',py+['docs/22p_gap/mutation_replay.py','--check-preimages'],DD,180)
if __name__=='__main__':main()
