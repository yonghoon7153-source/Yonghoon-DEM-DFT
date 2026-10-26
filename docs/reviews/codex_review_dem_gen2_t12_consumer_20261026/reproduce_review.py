"""Replay this review from the packaged original blobs, offline, in a new result directory."""
from pathlib import Path
import argparse,subprocess,sys,os,json
R=Path(__file__).resolve().parent;p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();O=a.output.resolve();O.mkdir(parents=True,exist_ok=False);(R/'tmp').mkdir(exist_ok=True)
env=dict(os.environ,GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='safe.directory',GIT_CONFIG_VALUE_0=(R/'object_repo').as_posix(),GIT_NO_LAZY_FETCH='1',TEMP=str(R/'tmp'),TMP=str(R/'tmp'),TMPDIR=str(R/'tmp'));runs=[]
def run(name,args):
 cmd=[sys.executable,'-I','-X','utf8','-B']+list(map(str,args));p=subprocess.run(cmd,capture_output=True,env=env,timeout=180);(O/(name+'.stdout')).write_bytes(p.stdout);(O/(name+'.stderr')).write_bytes(p.stderr);runs.append({'name':name,'rc':p.returncode,'command':cmd});print(name,p.returncode,flush=True);assert p.returncode==0,name
run('object_database',[R/'build_object_repo.py']);run('provenance',[R/'audit_provenance.py'])
run('direct52',[R/'snapshot/scripts/test_dem_gen2_t12_consumer_contract.py','--repo',R/'object_repo','--json',O/'direct52.json'])
D=R/'snapshot/docs/reviews/dem_gen2_t12_consumer_contract_evidence_20261024/independent-ulpri'
for name,script in [('loader','reproduce_loader_checks.py'),('mutants','reproduce_consumer_mutants.py')]:run(name,[R/'run_harness_utf8.py',D/script,'--source',R/'snapshot','--repo',R/'object_repo','--output',O/name])
run('scope',[R/'probe_scope.py','--repo',R/'object_repo','--out',O/'scope']);run('promisor',[R/'probe_promisor.py','--out',O/'promisor'])
(O/'reproduction.json').write_text(json.dumps(runs,indent=2),encoding='utf8')
