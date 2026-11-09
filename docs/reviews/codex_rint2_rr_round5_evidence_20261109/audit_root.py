"""Read-only package/remote identity, prior-source and mutation-record audit.
No production tests or engine invoked. Only M56 helper/candidate regression execute.
"""
from pathlib import Path
import ast, collections, hashlib, importlib.util, json, os, sys
ROOT=Path(__file__).resolve().parent
REPO=ROOT/'package/repo'
OUT=ROOT/'root_audit'; OUT.mkdir(exist_ok=True)
trees=json.loads((ROOT/'remote/selective_trees.json').read_text(encoding='utf-8'))
lookup={'/'.join(filter(None,[t['prefix'],i['path']])):i['sha'] for t in trees for i in t['tree'] if i['type']=='blob'}
data=json.loads((ROOT/'input_verification.json').read_text(encoding='utf-8'))
blobs=[{'path':x['path'][5:],'local_git_blob':x['git_blob'],'remote_git_blob':lookup.get(x['path'][5:]),'match':x['git_blob']==lookup.get(x['path'][5:])} for x in data['rows'] if x['path'].startswith('repo/')]
res={'pin':'abf0911ebc994167ac50132c78207c6c8d4421f1','checked':len(blobs),'match':sum(x['match'] for x in blobs),'differences':[x for x in blobs if not x['match']],'rows':blobs}
(ROOT/'remote/blob_comparison.json').write_text(json.dumps(res,indent=2)+'\n',encoding='utf-8')
assert len(blobs)==806 and all(x['match'] for x in blobs)
old=Path(os.environ.get('RR4_REPO',str(ROOT/'baseline/repo' if (ROOT/'baseline/repo').is_dir() else ROOT.parent/'rint2_rr_round4_review_20261109/package/repo')))
src=(REPO/'scripts/rint_r_chain.py').read_text(encoding='utf-8')
scriptdiff=[]
for p in sorted(p for p in (REPO/'scripts').iterdir() if p.is_file()):
    prev=old/'scripts'/p.name
    scriptdiff.append({'file':p.name,'old_present':prev.is_file(),'byte_equal':prev.is_file() and p.read_bytes()==prev.read_bytes()})
def functions(text):
    return {n.name:ast.get_source_segment(text,n) for n in ast.walk(ast.parse(text)) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
oldsrc=(old/'scripts/rint_r_chain.py').read_text(encoding='utf-8')
fnew,fold=functions(src),functions(oldsrc)
producer_names=['_src_done','run','_copy','_execute','_prepare','run_in_group','stop_trace','run_traces','record_outdir','resume_leftovers','group_pair']
# Distinguish repeated names by AST node list, never last-match silently.
def candidates(text,name):
    return [ast.get_source_segment(text,n) for n in ast.walk(ast.parse(text)) if isinstance(n,ast.FunctionDef) and n.name==name]
producer=[]
for n in producer_names:
    a,b=candidates(oldsrc,n),candidates(src,n)
    producer.append({'name':n,'old_count':len(a),'new_count':len(b),'all_same':a==b})
fix=REPO/'docs/reviews/rint2_rr4_fix_evidence_20261109'
j=json.loads((fix/'pa15_fix/logs/mutation_final.json').read_text(encoding='utf-8'))
muts=[x for x in j if x['id']!='NOMUT']
print('mutation row keys',list(muts[0]))
statuses=collections.Counter(x.get('status',x.get('kind',x.get('state'))) for x in muts)
# Preserve original records; count whatever exact field is actually present.
audit={'source_28':scriptdiff,'producer11':producer,'mutation_counts':dict(statuses),'mutation_records':muts}
(OUT/'static_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sys.path.insert(0,str(REPO/'scripts')); sys.dont_write_bytecode=True
import rint_r_chain as rr
root=OUT/'m56_synthetic';root.mkdir(exist_ok=True)
(root/'attempt_1').write_text('not a directory\n',encoding='utf-8')
(root/'attempt_1.rejected.json').write_text('{}\n',encoding='utf-8')
s={'resume':{'from':1,'copied':[],'rerun':'R','compared':[],'determinism':'assumed'},'runs':[{'name':'R','outdir':'R_arm1','arms':1,'arm_list':None}]}
fn=fnew['resume_rerun_problem']; before='    if not src.is_dir():'; after='    if not src.exists():'
assert fn.count(before)==1
ns=dict(rr.__dict__);exec(compile(fn.replace(before,after),'<historical-M56>','exec'),ns)
actual=rr.resume_rerun_problem(s,root/'attempt_2','TIME_LIMIT','NEXT')
mutant=ns['resume_rerun_problem'](s,root/'attempt_2','TIME_LIMIT','NEXT')
m56={'current':actual,'historical_mutant':mutant,'distinguished':isinstance(actual,str) and mutant is None,'scope':'Direct helper. No filesystem mock. Not a full-CLI exploit.'}
(OUT/'m56_result.json').write_text(json.dumps(m56,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert m56['distinguished']
spec=importlib.util.spec_from_file_location('review_test_rint_r_chain',REPO/'scripts/test_rint_r_chain.py')
tt=importlib.util.module_from_spec(spec);spec.loader.exec_module(tt);tt.RR=rr
rr4c=[]
for variant,func in [('candidate',rr.resume_rerun_problem),('M56',ns['resume_rerun_problem'])]:
    scratch=OUT/('rr4c_'+variant);scratch.mkdir(exist_ok=True)
    # Each replay has a separate path; no package state is altered.
    import tempfile
    tt.TD=tempfile.mkdtemp(prefix='run_',dir=scratch)
    previous=rr.resume_rerun_problem;rr.resume_rerun_problem=func
    try: outcome=tt.t_RR4C()
    finally: rr.resume_rerun_problem=previous
    rr4c.append({'variant':variant,'ok':outcome[0],'result':outcome[1]})
(OUT/'rr4c_direct.json').write_text(json.dumps(rr4c,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert rr4c[0]['ok'] and not rr4c[1]['ok']
print(json.dumps({'remote':{'checked':806,'match':806},'source_28_unchanged':sum(x['byte_equal'] for x in scriptdiff),'source_28_changed':[x['file'] for x in scriptdiff if not x['byte_equal']],'producer':producer,'M56':m56,'mutants':len(muts),'statuses':dict(statuses)},ensure_ascii=False,indent=2))

