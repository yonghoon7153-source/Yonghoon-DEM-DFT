"""Reviewer-owned AST/hash/copy checks; never imports received code."""
import ast,hashlib,json,shutil
from pathlib import Path
R=Path(__file__).resolve().parent
W=R.parent
OLD=W/'reil_c4e1_0_result_review_20261030'/'source'
D=R/'source'/'bms-balancing'/'docs'
def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def ident(p):
    b=p.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def tree(p): return ast.parse(p.read_text(encoding='utf-8-sig'))
def literal(t,name):
    return ast.literal_eval(next(n.value for n in t.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id==name for x in n.targets)))
def nodekey(n,i):
    if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)): return n.name
    if isinstance(n,ast.Assign): return 'assign:'+','.join(ast.unparse(t) for t in n.targets)
    if isinstance(n,(ast.Import,ast.ImportFrom)): return 'import:'+ast.dump(n,include_attributes=False)
    if isinstance(n,ast.Expr) and isinstance(n.value,ast.Constant) and isinstance(n.value.value,str): return 'docstring'
    if isinstance(n,ast.If): return 'if:'+ast.unparse(n.test)
    return type(n).__name__+':'+str(i)
def diff(a,b):
    def nodes(p):
        out={}; occurrences={}
        for i,n in enumerate(tree(p).body):
            key=nodekey(n,i)
            occurrences[key]=occurrences.get(key,0)+1
            if occurrences[key]>1: key+=' #'+str(occurrences[key])
            out[key]=ast.dump(n,include_attributes=False)
        return out
    aa=nodes(a)
    bb=nodes(b)
    same=[k for k in aa.keys()&bb.keys() if aa[k]==bb[k]]
    return {'same_including_main_if':len(same),'same_excluding_if':len([k for k in same if not k.startswith('if:')]),
      'changed':[k for k in aa.keys()&bb.keys() if aa[k]!=bb[k]],'added':sorted(bb.keys()-aa.keys()),'removed':sorted(aa.keys()-bb.keys())}
compare=load(R/'COMPARE_FROM_E1_0.json')
changed={x['filename'] for x in compare['files']}
assert compare['status']=='ahead' and compare['behind_by']==0 and len(changed)<300
drafts=['REIL_C4E1_LAUNCHER_DRAFT_v6_20261030.py.txt','REIL_C4E1_LAUNCHER_CONTROLS_DRAFT_v6_20261030.py.txt',
'REIL_C4E1_RUNNER_CONTROLS_DRAFT_v4_20261030.py.txt','REIL_C4E1_STEP_RUNNER_DRAFT_v6_20261030.py.txt','REIL_C4E1_0B_END_WRITER_DRAFT_20261030.py.txt']
for n in drafts:tree(D/n)
runner=tree(D/drafts[3])
fixed=literal(runner,'_FIXED'); old_launch=literal(runner,'RED_LAUNCH'); new_launch=literal(runner,'IMPL')
launchpath=literal(runner,'LAUNCH')
override={'bms-balancing/tests/test_reil_c4e1_launch.py':D/drafts[1],'bms-balancing/tests/test_reil_c4e1_runner.py':D/drafts[2]}
seal=[]
current=[]
for p,e in {launchpath:old_launch,**fixed}.items():
    if p in override: src=override[p]
    else:
        assert p not in changed
        src=OLD/p
        dest=R/'basis'/'unchanged_at_pin'/p
        dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(src,dest)
        current.append({'path':p,'captured':dest.relative_to(R).as_posix(),**ident(dest),'basis_commit':compare['base'],'current_unchanged_by_complete_compare':True})
    assert ident(src)==e,(p,ident(src),e)
    seal.append({'path':p,'expected':e,'match':True,'source':src.relative_to(W).as_posix()})
assert ident(D/drafts[0])==new_launch
seal.append({'path':launchpath,'phase':'GREEN','expected':new_launch,'match':True,'source':drafts[0]})
copy_more=['bms-balancing/tests/test_reil_c4e1_launch.py','bms-balancing/tests/test_reil_c4e1_runner.py','bms-balancing/evidence/reil_c4e1_0_20261030/00_step_runner.py']
for p in copy_more:
    assert p not in changed
    dest=R/'basis'/'unchanged_at_pin'/p
    dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(OLD/p,dest)
    current.append({'path':p,'captured':dest.relative_to(R).as_posix(),**ident(dest),'basis_commit':compare['base'],'current_unchanged_by_complete_compare':True})
prior=R/'basis'/'prior_review'
prior.mkdir(parents=True,exist_ok=True)
for n in ['CODEX_REPLY_KO.txt','REVIEW_DECISION.json','PROPOSED_RED_CRITERIA_KO.txt']:
    shutil.copyfile(OLD.parent/n,prior/n)
pairs=[(OLD/'bms-balancing/scripts/reil_c4e1_launch.py',D/drafts[0]),
(OLD/'bms-balancing/tests/test_reil_c4e1_launch.py',D/drafts[1]),
(OLD/'bms-balancing/evidence/reil_c4e1_0_20261030/00_step_runner.py',D/drafts[3]),
(OLD/'bms-balancing/tests/test_reil_c4e1_runner.py',D/drafts[2])]
diffs={b.name:diff(a,b) for a,b in pairs}
counts={str(p.relative_to(R)) if p.is_relative_to(R) else p.name:sum(isinstance(n,ast.FunctionDef) and n.name.startswith('test_') for n in tree(p).body)
for p in [OLD/'bms-balancing/tests/test_reil_c4e.py',OLD/'bms-balancing/tests/test_reil_c4e_fix.py',D/drafts[1],D/drafts[2]]}
assert list(counts.values())==[21,6,33,11]
attachment=[]
for n in ['REIL_C4E_E1_0B_APPROVAL_REQUEST_20261030.md','REIL_C4E_E1_0B_PREREVIEW_SEND_20261030.md']:
    p=Path('C:/Users/Administrator/Downloads')/n
    dest=R/'basis'/'attachments'/n;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
    assert p.read_bytes()==(D/n).read_bytes()
    attachment.append({'path':str(p),'same_bytes_at_pinned_commit':True,**ident(p)})
writer=tree(D/drafts[4])
imports=[ast.unparse(n) for n in writer.body if isinstance(n,(ast.Import,ast.ImportFrom))]
status_old=(OLD/'bms-balancing/docs/REIL_PREREQUISITES_STATUS_20261004.md').read_bytes()
status_new=(D/'REIL_PREREQUISITES_STATUS_20261004.md').read_bytes()
out={'kind':'E1_0B_REVIEWER_STATIC_DATA_AUDIT','pinned_commit':compare['head'],
'attachments':attachment,'draft_AST_parse_count':5,'drafts':[{ 'file':n,**ident(D/n)} for n in drafts],
'fixed_seal_rows':seal,'fixed_seal_match_count':len(seal),'local_current_counterparts':current,
'unchanged_scope':'Git comparison of immutable commits + previously captured exact bytes; no remote working-tree observation',
'top_level_AST_comparison':diffs,'test_function_counts':counts,'planned_GREEN_total':sum(counts.values()),
'writer_imports':imports,'prior_status_prefix_preserved':status_new.startswith(status_old),
'start_sha_literal_count':10,'start_sha_written_description_count':11,
'functional_tests':0,'received_code_execution':0,'target_imports':0,'Git_fixture_or_probe':0}
(R/'STATIC_AUDIT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'seal_rows':len(seal),'GREEN_functions':sum(counts.values()),'current_counterparts':len(current),'attachments_same_bytes':True,'AST_comparison':diffs,'status_prefix_unchanged':out['prior_status_prefix_preserved'],'target_execution':0},ensure_ascii=False))

