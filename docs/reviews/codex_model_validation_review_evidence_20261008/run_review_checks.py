"""Replay review arithmetic and postprocessor tests; never invokes a DEM engine."""
from pathlib import Path
import hashlib, importlib.metadata, json, os, subprocess, sys

ROOT=Path(__file__).resolve().parent
(ROOT/'tmp').mkdir(exist_ok=True)
(ROOT/'evidence').mkdir(exist_ok=True)
manifest=json.loads((ROOT/'source_manifest.json').read_text(encoding='utf8'))
for item in manifest:
    path=ROOT/'source'/item['path']
    b=path.read_bytes()
    assert hashlib.sha256(b).hexdigest()==item['sha256'],item['path']
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==item['sha'],item['path']
assert (ROOT/'submitted/codex_model_validation_request_20261008.md').read_bytes()==(ROOT/'source/docs/reviews/codex_model_validation_request_20261008.md').read_bytes()
extra=[('mv_softening_in.ps_7_3_r45_61ebd18.liggghts','52ed80f64bd82110a4dd9d3b1127b1d514807ba8'),
       ('mv_softening_normal_model_hooke_hysteresis_3d5c00f.h','3921ff5c767324e8825e76ff7528563e92e8efd7')]
for name,sha in extra:
    b=(ROOT/'evidence'/name).read_bytes()
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==sha,name
env=os.environ.copy()
env.update(PYTHONDONTWRITEBYTECODE='1',PYTHONIOENCODING='utf-8',PYTHONUTF8='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',TEMP=str(ROOT/'tmp'),TMP=str(ROOT/'tmp'))
scripts=['mv_anchor_porosity.py','mv_pressure_arithmetic.py','mv_softening_scaling.py','mv_softening_frozen_reweight.py','mv_stress_probe.py','mv_stress_core_probe.py']
runs=[]
for name in scripts:
    p=subprocess.run([sys.executable,'-B',str(ROOT/'probes'/name)],cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf8',errors='replace')
    (ROOT/'evidence'/f'{Path(name).stem}.stdout.txt').write_text(p.stdout,encoding='utf8')
    (ROOT/'evidence'/f'{Path(name).stem}.stderr.txt').write_text(p.stderr,encoding='utf8')
    runs.append(dict(probe=name,returncode=p.returncode,stdout=f'evidence/{Path(name).stem}.stdout.txt',stderr=f'evidence/{Path(name).stem}.stderr.txt'))
    if name in ('mv_pressure_arithmetic.py','mv_softening_frozen_reweight.py') and p.returncode==0:
        obj=json.loads(p.stdout)
        (ROOT/'evidence'/f'{Path(name).stem}_result.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
versions={}
for name in ('numpy','pandas','networkx'):
    try: versions[name]=importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError: versions[name]='not in base environment; see probe dependency path'
report=dict(pin='61ebd181b1ae5b47a76fe69d4400e4a3950dc8a3',source_files_verified=len(manifest),external_evidence_blobs_verified=len(extra),attachment_equals_pinned_request=True,python=sys.version,packages=versions,runs=runs,all_passed=all(r['returncode']==0 for r in runs),no_simulations=True)
(ROOT/'evidence/review_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(0 if report['all_passed'] else 1)
