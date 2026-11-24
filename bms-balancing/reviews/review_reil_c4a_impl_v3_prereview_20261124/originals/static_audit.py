import ast,hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
src=root/'source/bms-balancing'
prior=root.parent/'reil_c4a_impl_v2_prereview_20261108'
old=(prior/'source/bms-balancing/docs/REIL_PREREQUISITES_STATUS_20261004.md').read_bytes()
new=(src/'docs/REIL_PREREQUISITES_STATUS_20261004.md').read_bytes()
rows=[]
for p in sorted((src/'tests').glob('test_reil_c4*.py')):
    t=ast.parse(p.read_text('utf-8'))
    for f in t.body:
        if not isinstance(f,(ast.FunctionDef,ast.AsyncFunctionDef)) or not f.name.startswith('test_'):continue
        calls=[]
        for n in ast.walk(f):
            if not isinstance(n,ast.Call):continue
            c=ast.unparse(n.func)
            if c.endswith(('supervise','run_phase_a','run_local','minimize','run_optimization','stage_a','start','kill','killpg','_launch','_pre','_tree','_git','Popen')) or c=='subprocess.run':
                calls.append({'line':n.lineno,'call':c})
        if calls:rows.append({'file':p.name,'test':f.name,'calls':calls})
out={'kind':'STATIC_TEXT_AST_READ_ONLY_AUDIT','ledger_previous_exact_prefix':new.startswith(old),'ledger_before_bytes':len(old),'ledger_after_bytes':len(new),'test_call_index':rows,'target_import':0,'target_execution':0,'pytest_collection':0,'note':'AST parsing indexes call spellings; not dynamic call counts or exhaustive proof of absence.'}
(root/'STATIC_AUDIT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'ledger_previous_exact_prefix':new.startswith(old),'indexed_tests':len(rows),'target_execution':0}))
for r in rows:
    if r['file']!='test_reil_c4e1_launch.py':print(r)
