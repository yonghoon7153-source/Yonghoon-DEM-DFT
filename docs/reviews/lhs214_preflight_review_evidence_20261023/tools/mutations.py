import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT=Path(os.environ.get('REPO_ROOT', Path(__file__).resolve().parents[4])).expanduser().resolve()
OUT=Path(os.environ.get('EVIDENCE_OUT', Path.cwd() / 'lhs214-reproduction')).expanduser().resolve()
OUT.mkdir(parents=True, exist_ok=True)
REAL=ROOT/'scripts/supp20_input_receipt.py'
source=REAL.read_text()
guards={
    'm1_leftover_pending':"if st_ == 'registered' and p_ is not None:",
    'm2_cross_document':'if (r_, p_) != b_:',
    'm3_base_problems':'if bp_:',
    'm4_undeclared':"if st_ == 'undeclared':",
}
summary={}
for name,old in guards.items():
    assert source.count(old)==1,(name,source.count(old))
    changed=source.replace(old,'if False and '+old[3:])
    path=OUT/(name+'.py')
    path.write_text(changed)
    # Execute the mutated module with its original path metadata. All source
    # writes stay in the review folder; the repository is never changed.
    program="import sys; from pathlib import Path; sys.path.insert(0,sys.argv[1]); ns={'__file__':sys.argv[2],'__name__':'independent_mutant'}; exec(compile(Path(sys.argv[3]).read_text(),sys.argv[2],'exec'),ns); raise SystemExit(ns['_selftest']())"
    start=time.monotonic()
    with (OUT/(name+'.log')).open('w') as log:
        run=subprocess.run([sys.executable,'-I','-c',program,str(ROOT/'scripts'),str(REAL),str(path)],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
    lines=(OUT/(name+'.log')).read_text().splitlines()
    failure=[s for s in lines if s.startswith('  FAIL')]
    summary[name]={'rc':run.returncode,'seconds':round(time.monotonic()-start,3),
                   'sha256':hashlib.sha256(changed.encode()).hexdigest(),'failures':failure,'last_lines':lines[-3:]}
    (OUT/'mutations.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(name,run.returncode,lines[-1],flush=True)
assert all(v['rc']==1 and len(v['failures'])==1 and 'S11g' in v['failures'][0] for v in summary.values()),summary
