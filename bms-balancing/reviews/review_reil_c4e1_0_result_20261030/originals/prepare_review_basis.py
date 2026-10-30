"""Reviewer-owned exact-byte copies of prior static-review evidence."""
import ast, hashlib, json
from pathlib import Path
r=Path(__file__).resolve().parent
p=r.parent/'reil_c4e_e1_v5_prereview_20261030'/'source'
runner=ast.parse((r/'source/bms-balancing/evidence/reil_c4e1_0_20261030/00_step_runner.py').read_text(encoding='utf-8'))
fixed=ast.literal_eval(next(n.value for n in runner.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_FIXED' for t in n.targets)))
files=[x for x in fixed if (p/x).is_file()]
files += ['bms-balancing/docs/'+x for x in ['REIL_C4E1_LAUNCHER_DRAFT_v5_20261027.py.txt','REIL_C4E1_LAUNCHER_SKELETON_DRAFT_v5_20261027.py.txt','REIL_C4E1_LAUNCHER_CONTROLS_DRAFT_v5_20261027.py.txt','REIL_C4E1_RUNNER_CONTROLS_DRAFT_v3_20261027.py.txt','REIL_C4E1_STEP_RUNNER_DRAFT_v5_20261027.py.txt','REIL_C4E_E1_APPROVAL_REQUEST_v5_20261027.md']]
rows=[]
for path in sorted(set(files)):
    b=(p/path).read_bytes()
    dst=r/'basis/prior_v5/source'/path
    dst.parent.mkdir(parents=True,exist_ok=True)
    with dst.open('xb') as f:f.write(b)
    assert dst.read_bytes()==b
    rows.append({'relative_path':str(dst.relative_to(r)).replace('\\','/'),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'origin':'Prior v5 static review source capture; not a new target run'})
(r/'BASIS_COPY_IDENTITIES.json').write_text(json.dumps({'files':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'exact_copies':len(rows),'received_code_execution':0}))
