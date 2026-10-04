import ast, hashlib, json, pathlib, re, difflib
p=pathlib.Path(__file__).with_name("RECEIVED_SNAPSHOT.json")
s=json.loads(p.read_text(encoding="utf-8"))
checks=[]
for path,d in s["files"].items():
 b=d["content"].encode("utf-8")
 got=hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
 checks.append({"path":path,"git_blob_match":got==d["sha"],"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()})
logs=[]
for e in s["evidence_manifest"]:
 path="degradation-degeneracy/docs/22p_gap/gate88_evidence/"+e["name"]
 d=next(x for x in checks if x["path"]==path)
 logs.append(dict(e,size_match=e["bytes"]==d["bytes"],sha_match=e["sha256"]==d["sha256"]))
pv=s["files"]["degradation-degeneracy/tools/preserve.py"]["content"]
tree=ast.parse(pv)
funcs={x.name:x for x in tree.body if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef))}
calls={}
for name in ["finalize_leg","resume_claim","_read_claim_record","_assert_external_input_binding","_claim_required_phases"]:
 f=funcs[name]
 calls[name]={"line":f.lineno,"end":f.end_lineno,"calls":[{"name":ast.unparse(n.func),"line":n.lineno} for n in ast.walk(f) if isinstance(n,ast.Call)]}
out={"method":"reviewer-owned static data reader only; received source parsed, not imported or executed","snapshot_blob_checks":checks,"log_checks":logs,"callgraph":calls,"all_git_blobs_match":all(x["git_blob_match"] for x in checks),"all_log_size_sha_match":all(x["size_match"] and x["sha_match"] for x in logs),"received_program_executions":0,"project_tests_executed":0}
scope=json.loads(p.with_name('RUN_SCOPE_SNAPSHOT.json').read_text(encoding='utf-8'))
prior=json.loads(p.with_name('PRIOR_REFERENCE.json').read_text(encoding='utf-8'))
h=hashlib.sha256()
scope_ids=[]
for path,d in sorted(scope['files'].items()):
 b=d['content'].encode('utf-8')
 h.update(path.removeprefix('degradation-degeneracy/').encode('utf-8')); h.update(b)
 gitsha=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 tree_sha=next(x['sha'] for x in scope['entries'] if x['path']==path)
 old_sha=next(x['sha'] for x in prior['entries'] if x['path']==path)
 scope_ids.append({'path':path,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob':gitsha,'blob_tree_match':gitsha==d['sha']==tree_sha,'unchanged_since_g87':gitsha==old_sha})
out['run_scope']={'digest':h.hexdigest()[:16],'count':len(scope_ids),'all_blobs_match':all(x['blob_tree_match'] for x in scope_ids),'files':scope_ids}
out['receipt_diffs']={}
for leg in ('paired_fixed5_v4','grid_fit_v5'):
 path='degradation-degeneracy/docs/22p_gap/receipts/'+leg+'.validate.yaml'
 old=prior['files'][path]['content']; new=s['files'][path]['content']
 hist=s['files']['degradation-degeneracy/docs/22p_gap/receipts/history/'+leg+'.validate.864edfb73b9695a1.yaml']['content']
 out['receipt_diffs'][leg]={'history_byte_identical':old==hist,'unified_diff':'\n'.join(difflib.unified_diff(old.splitlines(),new.splitlines(),fromfile='prior',tofile='current',lineterm=''))}
lp='degradation-degeneracy/docs/22p_gap/LEG_PRESERVATION.yaml'
out['ledger_diff']='\n'.join(difflib.unified_diff(prior['files'][lp]['content'].splitlines(),s['files'][lp]['content'].splitlines(),fromfile='g87',tofile='g88',lineterm=''))
invariants={}
for path,names in [('degradation-degeneracy/tools/preserve.py',['leg_run_spec','leg_run_spec_v3','stage3_axis_from_envelope','assert_run_is_authorized']),('degradation-degeneracy/src/fitting.py',['_assert_fit_authorized','_assert_fit_input_is_authorized','_stage3_preflight','_prepare_stage3','_run_fit_locked','stage3_context_from_plan'])]:
 a={n.name:n for n in ast.parse(prior['files'][path]['content']).body if isinstance(n,ast.FunctionDef)}
 b={n.name:n for n in ast.parse(s['files'][path]['content']).body if isinstance(n,ast.FunctionDef)}
 for name in names:
  invariants[path+':'+name]={'present':name in a and name in b,'ast_equal':name in a and name in b and ast.dump(a[name])==ast.dump(b[name])}
out['ast_invariants']=invariants
out['finalizer_binding_gap']={'evidence_kind':'static call and data flow; not an execution reproduction','helper_calls_in_finalizer':sum(x['name']=='_assert_external_input_binding' for x in calls['finalize_leg']['calls']),'helper_call_lines_in_source':[i for i,l in enumerate(pv.splitlines(),1) if '_assert_external_input_binding(' in l],'finalizer_input_package_comparison_lines':[9133,9134,9135,9136,9137,9138],'finalizer_copies_receipt_lines':[9174,9175,9176,9177]}
print(json.dumps(out,ensure_ascii=False))
