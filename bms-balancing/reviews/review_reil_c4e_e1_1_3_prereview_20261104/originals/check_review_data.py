"""Text/AST/identity inspection, not importing or running received programs."""
import ast,base64,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(b)
    assert p.read_bytes()==b
c=json.loads((R/'MONITOR_SOURCE_CAPTURE.json').read_bytes()); b=base64.b64decode(c['content'])
assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==c['sha']
assert c['pin']=='26a6c3a49b5c0a9044535ccdd62a8ffa5ed05cdd'
rel='bms-balancing/scripts/reil_c4_monitor.py'
put(R/'source'/rel,b)
put(R/'numbered/reil_c4_monitor.py.lines.txt',('\n'.join(f'{i}: {s}' for i,s in enumerate(b.decode('utf-8').splitlines(),1))+'\n').encode('utf-8'))
sources=json.loads((R/'SOURCE_IDENTITIES.json').read_bytes())
sources['connector_sources'].append({'path':rel,'bytes':len(b),'sha256':sha(b),'git_blob_sha1':c['sha'],'source':'Pinned GitHub connector base64; supplemental final_record text; blob identity verified'})
(R/'SOURCE_IDENTITIES.json').write_bytes((json.dumps(sources,ensure_ascii=False,indent=2)+'\n').encode())
doc=R/'source/bms-balancing/docs'
parsed=[]
for name in ['REIL_C4E1_E113_OUTER_DRAFT_20261104.py.txt','REIL_C4E1_E113_JUDGE_DRAFT_20261104.py.txt','REIL_C4E1_E113_END_WRITER_DRAFT_20261104.py.txt']:
    p=doc/name;raw=p.read_bytes(); t=ast.parse(raw,filename=name)
    parsed.append({'file':name,'bytes':len(raw),'sha256':sha(raw),'AST_parse':'OK','functions':[n.name for n in t.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]})
jt=ast.parse((doc/'REIL_C4E1_E113_JUDGE_DRAFT_20261104.py.txt').read_bytes())
jnode=next(n for n in jt.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='RUN_FILES' for t in n.targets))
judge_files=[n.value for n in jnode.value.elts]
rt=ast.parse((R/'source/bms-balancing/scripts/reil_c4e_run.py').read_bytes())
fn=next(n for n in rt.body if isinstance(n,ast.FunctionDef) and n.name=='record_parts')
ret=next(n for n in fn.body if isinstance(n,ast.Return))
run_files=[k.value for k in ret.value.keys]
out={'kind':'STATIC_REVIEW_TEXT_AST_IDENTITIES','received_program_execution':0,'probe_execution':0,'drafts':parsed,'run_record_parts_keys':run_files,'judge_RUN_FILES':judge_files,'extra_required_by_judge':sorted(set(judge_files)-set(run_files)),'scope':'AST reads syntax and literal names only. No target function/module execution, test, dynamic counterexample or functional pass claim. final_record behavior separately read as source.'}
put(R/'STATIC_SOURCE_OBSERVATIONS.json',(json.dumps(out,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({'AST_parsed':len(parsed),'run_part_count':len(run_files),'judge_count':len(judge_files),'extra_required_by_judge':out['extra_required_by_judge'],'monitor_bytes':len(b),'monitor_sha256':sha(b),'target_execution':0}))
