"""Verify delivered relative paths by replaying in a fresh extraction directory."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,tempfile,zipfile,shutil
R=Path(__file__).resolve().parent
zpath=R.parent/'codex_rint_g2_impl_fix_recheck_20261015.zip'
target=Path(tempfile.mkdtemp(prefix='rint_recheck_',dir=R/'tmp'))
with zipfile.ZipFile(zpath) as z:
    for name in z.namelist():
        q=(target/name).resolve()
        assert q.is_relative_to(target.resolve()),name
        p=Path('\\\\?\\'+str(q)) if os.name=='nt' else q
        p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(name))
    manifest=json.loads(z.read('PACKAGE_MANIFEST.json'))
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
# This Python runtime keeps third-party SciPy in the workspace's dependency cache.
# Expose only those libraries, never the original reviewed source paths.
env['PYTHONPATH']=os.pathsep.join([str(R.parent/'lhs_coverage_review_20260930/deps'),
                                str(R.parent/'gen2_network_reverify3_20261007/deps')])
for suffix in ('json','log'):
    prior=R/'evidence'/('package_portability.'+suffix)
    backup=R/'evidence'/('package_portability_initial_missing_scipy.'+suffix)
    if prior.exists() and not backup.exists():shutil.copyfile(prior,backup)
cmd=[sys.executable,'-X','utf8','-B',str(target/R.name/'reproduce.py')]
p=subprocess.run(cmd,cwd=target,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=900)
(R/'evidence/package_portability.log').write_bytes(p.stdout)
out={'extraction_root':str(target),'zip_sha256_tested':hashlib.sha256(zpath.read_bytes()).hexdigest(),
     'command':cmd,'rc':p.returncode,'member_hashes_prechecked':len(manifest['files']),
     'third_party_only_pythonpath':env['PYTHONPATH'],
     'stdout_sha256':hashlib.sha256(p.stdout).hexdigest()}
(R/'evidence/package_portability.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps(out,indent=2));print(p.stdout.decode('utf8'))
sys.exit(p.returncode)
