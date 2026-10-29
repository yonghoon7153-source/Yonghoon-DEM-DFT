"""Copy only deliverable-local inputs into a temporary sibling layout and rerun."""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]
temp=Path(tempfile.mkdtemp(prefix='portable_',dir=HERE)).resolve()
assert temp.is_relative_to(HERE.resolve()) and temp != HERE.resolve()
try:
    dst=temp/'independent'/'identity'
    dst.mkdir(parents=True)
    for name in ['metadata','sources','gate_inputs']:
        shutil.copytree(HERE/name,dst/name)
    shutil.copy2(HERE/'audit_identity.py',dst/'audit_identity.py')
    shutil.copytree(BASE/'repo',temp/'repo')
    run=subprocess.run([sys.executable,'-I','-X','utf8','-B',str(dst/'audit_identity.py')],cwd=temp,text=True,capture_output=True,encoding='utf-8')
    result={'returncode':run.returncode,'stdout':run.stdout,'stderr':run.stderr,'summary':json.loads((dst/'summary.json').read_text(encoding='utf-8')) if (dst/'summary.json').exists() else None,'external_prior_cache_used':False,'copied_inputs':['repo/','independent/identity/metadata/','independent/identity/sources/','independent/identity/gate_inputs/','independent/identity/audit_identity.py']}
    (HERE/'portable_result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    assert run.returncode==0
finally:
    assert temp.is_relative_to(HERE.resolve()) and temp.name.startswith('portable_') and temp != HERE.resolve()
    shutil.rmtree(temp)
