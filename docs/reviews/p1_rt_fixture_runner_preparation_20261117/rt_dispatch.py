"""Candidate dispatch: rev5 restoration/gates and RT prereqs; never launch."""
import argparse,importlib.util,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
CP=HERE if (HERE/'rt_restore.py').is_file() else HERE.parent/'p1_rt_consumer_preparation_20261117'
sys.path.insert(0,str(CP))
import rt_restore as R
import rt_fixture_prereq as F

def orig_grid(root,bed,job,kit):
    """Read only original log/deck or the ONE selected EXT screen."""
    result={'ok':False,'status':'NOT_COMPUTED','operational_go':False}
    try:
        if bed not in R.C.GRIDS or job not in ('RJ','RJ2'):raise ValueError('bed/job')
        root=Path(root);old=R.legacy_reader(kit);P=old.ul_lib.load_params(str(Path(kit)/'unload_params.json'))
        B=P['beds'][bed]
        if job=='RJ':
            step=P['ext_10_0']['start_step'] if bed=='ps_10_0_r45' else B['s0']
        else:
            dec=json.loads((root/bed/'s0_decision.json').read_bytes())
            if not isinstance(dec,dict) or dec.get('status')!='PASS' or type(dec.get('s0')) is not int:raise ValueError('selected S0')
            step=dec['s0']
        source=R.C.select_source(root,bed,job,step,P['ext_10_0'],B['orig_log'])
        text=Path(source['log']).read_text(encoding='utf8')
        if job=='RJ':
            name=B['last_deck']
            if not isinstance(name,str) or Path(name).name!=name:raise ValueError('original deck basename')
            text+='\n'+(root/bed/'in'/name).read_text(encoding='utf8')
        evidence=R.C.N.grid_evidence(text,source['grid'],source['written_np'])
        result.update(evidence,ok=evidence['status']=='PASS',step=step)
    except (OSError,ValueError,TypeError,KeyError,UnicodeError) as e:
        result['reason']=type(e).__name__
    return result

def main(argv=None,*,kit=None):
    argv=list(sys.argv[1:] if argv is None else argv);kit=Path(kit or HERE)
    if not argv:raise ValueError('command required')
    cmd=argv[0]
    if cmd=='restore':
        return R.main(argv[1:]+['--kit',str(kit)])
    if cmd=='rt_grammar':
        p=argparse.ArgumentParser();p.add_argument('verdict',type=Path);p.add_argument('--lmp-sha',required=True)
        a=p.parse_args(argv[1:])
        try:
            identities=json.loads((kit/'RT_FIXTURE_CANDIDATE_IDENTITIES.json').read_bytes())
            result=F.check(a.verdict,a.lmp_sha,identities)
        except (OSError,ValueError,TypeError) as e:result={'ok':False,'operational_go':False,'error':type(e).__name__}
        print(json.dumps(result,ensure_ascii=False,allow_nan=False))
        return 0 if result['ok'] else 2
    if cmd=='orig_grid':
        if len(argv)!=4:raise ValueError('orig_grid ROOT BED JOB')
        r=orig_grid(*argv[1:],kit);print(json.dumps(r));return 0 if r['ok'] else 2
    # Only the certificate consumer changes; other historical functions remain.
    old=R.legacy_reader(kit)
    def restored(root,bed,job):
        ok=R.job_restored(root,bed,job,kit)
        return ok,'rev5 certificate + complete receipt + both grammar prerequisites'
    old._job_restored=restored
    return old.main(argv)
if __name__=='__main__':
    try:raise SystemExit(main())
    except (OSError,ValueError,TypeError) as e:
        print('RT_DISPATCH_ERROR: '+type(e).__name__,file=sys.stderr);raise SystemExit(3)
