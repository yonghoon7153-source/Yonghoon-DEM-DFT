from pathlib import Path
import subprocess, os, json, hashlib, datetime, shutil
R=Path(__file__).resolve().parent
PY='C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
env=dict(os.environ,PYTHONPATH=os.pathsep.join([str(R/'source/scripts'),str(R.parent/'lhs_coverage_review_20260930/deps'),str(R.parent/'gen2_network_reverify3_20261007/deps')]),PYTHONDONTWRITEBYTECODE='1',PYTHONIOENCODING='utf-8',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',TEMP=str(R/'tmp'),TMP=str(R/'tmp'),TMPDIR=str(R/'tmp'))
(R/'source_prior').mkdir(exist_ok=True)
shutil.copyfile(R.parent/'rint_g2_v3_review_20261007/source/scripts/step3_sigma.py',R/'source_prior/step3_sigma.py')
shutil.copyfile('C:/Users/Administrator/.codex/attachments/a714cbf3-213a-4f24-8add-c897f202923d/붙여넣은 텍스트.txt',R/'submitted/user_request.txt')
jobs=[['probes/windows_telemetry_bootstrap.py','test_rint_t4_census.py'],['probes/windows_telemetry_bootstrap.py','test_rint_t43_order.py'],['probes/rrm_probe.py'],['probes/join_synthetic.py'],['probes/owner_vox_mismatch.py'],['probes/off_compatibility.py']]
out=[]
for j in jobs:
    p=subprocess.run([PY,'-X','utf8','-B',*j],cwd=R,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240)
    tag='_'.join(Path(x).stem for x in j)
    log=R/'evidence'/('rerun_'+tag+'.log');log.write_bytes(p.stdout)
    out.append(dict(command=j,rc=p.returncode,log=log.name,log_sha256=hashlib.sha256(p.stdout).hexdigest()))
    print(tag,p.returncode,flush=True)
(R/'evidence/root_reruns.json').write_text(json.dumps(out,indent=2),encoding='utf8')
mf=json.loads((R/'source_manifest.json').read_text(encoding='utf8'))
bad=[]
for f in mf['files']:
    if hashlib.sha256((R/'source'/f['path']).read_bytes()).hexdigest()!=f['sha256']:bad.append(f['path'])
meta={'pin':mf['pin'],'branch':'claude/stoic-knuth-NObVQ','pin_authorization':'User approved fetching and pinning the latest commit on 2026-10-14','verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_files':len(mf['files']),'source_mismatches':bad,'git_mutations':False,'production_simulations':False,'offline_small_fv_fixtures':True,'windows_resource_shim':'RSS telemetry only, ru_maxrss=NaN; source unmodified'}
(R/'evidence/review_metadata.json').write_text(json.dumps(meta,indent=2),encoding='utf8')
print(json.dumps(meta))
assert not bad and all(x['rc']==0 for x in out)
