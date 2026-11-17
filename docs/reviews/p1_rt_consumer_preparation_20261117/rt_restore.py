"""Read-only legacy/RT adapter and optional explicit exclusive publication."""
import argparse,importlib.util,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import rt_contract as C
from rt_publish import publish_new

def legacy_reader(kit):
    kit=Path(kit).resolve()
    if not (kit/'ul_reader.py').is_file():raise ValueError('prepared kit required')
    sys.path.insert(0,str(kit))
    spec=importlib.util.spec_from_file_location('legacy_rt_consumer',kit/'ul_reader.py')
    old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old);return old

def restore(root,bed,job='RJ',hist=None,kit=None):
    kit=Path(kit or Path(__file__).resolve().parent)
    old=legacy_reader(kit);P=old.ul_lib.load_params(str(kit/'unload_params.json'))
    if bed not in C.GRIDS or job not in ('RJ','RJ2') or (job=='RJ2' and bed!='ps_10_0_r45'):raise ValueError('unsupported bed/job')
    baseline=old.restore_verdict(str(root),bed,job,str(hist) if hist else None,P)
    step=baseline['s0']
    try:source=C.select_source(root,bed,job,step,P['ext_10_0'],P['beds'][bed]['orig_log'])
    except (ValueError,TypeError):
        checks=dict(baseline['checks']);checks['G2c_cont']=checks.pop('G2c',{'status':'NOT_COMPUTED'})
        checks['source_selection']={'ok':False}
        if checks.get('syntax',{}).get('ok') is not True:status='SYNTAX_FAIL'
        elif (checks.get('g0',{}).get('ok') is not True or checks.get('pre_post',{}).get('equal') is False
              or any(checks.get(k,{}).get('status')=='FAIL' for k in ('G1','G2','mesh_md5','G3'))):status='VALUE_MISMATCH'
        else:status='UNCONFIRMED'
        return {'schema':'rt_restore_candidate_v1','restore_rule':'rev5_g2cp','status':status,
                'bed':bed,'job':job,'s0':step,'checks':checks,'operational_qualification':False,'certificate_published':False}
    return C.evaluate(Path(root)/bed/job,bed=bed,step=step,atoms=P['beds'][bed]['atoms'],
        reference_contact=source['contact'],grid_text=C.text(source['log']),grid=source['grid'],written_np=source['written_np'],
        legacy_checks=baseline['checks'],job_kind=job)

def job_restored(root,bed,job,kit=None):
    old=legacy_reader(kit or Path(__file__).resolve().parent)
    path=Path(root)/bed/job
    try:report=json.loads((path/'restore_verdict.json').read_bytes())
    except (OSError,ValueError):return False
    if not isinstance(report,dict) or report.get('schema')!='rt_restore_candidate_v1' or report.get('restore_rule')!='rev5_g2cp' or report.get('status')!='RESTORED':return False
    if report.get('bed')!=bed or report.get('job')!=job:return False
    ok,_,receipt=old._job_receipt(str(root),bed,job)
    return ok and all([line for line in receipt.splitlines() if line.startswith(key+'=')]==[key+'=PASS']
                      for key in ('grammar_prereq','rt_grammar_prereq'))

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('bed')
    p.add_argument('--job',default='RJ',choices=['RJ','RJ2']);p.add_argument('--kit',type=Path);p.add_argument('--hist',type=Path)
    p.add_argument('--publish-new',action='store_true');a=p.parse_args(argv)
    try:
        r=dict(restore(a.root,a.bed,a.job,a.hist,a.kit))
        if a.publish_new:
            r['certificate_published']=True
            publish_new(a.root/a.bed/a.job,r)
        print(json.dumps(r,ensure_ascii=False,allow_nan=False,indent=2,default=lambda x:sorted(x) if isinstance(x,set) else str(x)))
        return 0 if r['status']=='RESTORED' else 2
    except (OSError,ValueError,TypeError) as error:
        print('RT_READ_OR_PUBLISH_ERROR: '+type(error).__name__,file=sys.stderr);return 3
if __name__=='__main__':raise SystemExit(main())
