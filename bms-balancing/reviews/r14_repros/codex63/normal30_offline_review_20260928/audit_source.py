"""Static reviewer checks only: byte comparison, JSON, AST-as-data, arithmetic.
Does not import/compile/execute any received candidate or test harness.
"""
import ast, hashlib, json, pathlib, re
from decimal import Decimal as D
ROOT=pathlib.Path(__file__).resolve().parent
R=ROOT/'received'
PRIOR=ROOT.parent/'guard1198_native_review_20260928'/'received'
def h(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_bytes())
def save(n,o):(ROOT/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
out={'scope':'static byte/JSON/AST and mathematical witness; no target execution','checks':{}}
def ck(name,v):
    out['checks'][name]=bool(v)
    assert v,name
cm=read(R/'CODE_MANIFEST.json');c=read(R/'CONTRACT.json');oldc=read(R/'basis/CONTRACT.json')
for item in read(R/'basis/CODE_MANIFEST.json')['files']:
    name=item['file']
    ck('prior_received_identity:'+name,(R/'basis'/name).read_bytes()==(PRIOR/'candidate'/name).read_bytes())
old=(R/'basis/src/Guard1198Candidate.java').read_bytes();new=(R/'src/Normal30Candidate.java').read_bytes();inverse=new
reps=read(R/'JAVA_ALLOWED_REPLACEMENTS.json')
for r in reversed(reps):
    ck('replacement_count:'+r['category'],inverse.count(r['after'].encode())==r['occurrences'])
    inverse=inverse.replace(r['after'].encode(),r['before'].encode())
ck('whole_java_inverse_exact',inverse==old)
out['java']={'source_sha256':h(new),'basis_sha256':h(old),'inverse_sha256':h(inverse),'replacement_rows':len(reps),'literal_occurrences':sum(x['occurrences'] for x in reps)}
times=re.findall(rb'set\("tlist","([^"]+)"\)',new);ck('single_tlist',len(times)==1)
tokens=times[0].decode().split();expected_extension=[format(D(i)/D(10),'f') for i in range(51,301)]
ck('java_contract_tlist',tokens==c['requested_times_s'])
ck('old187_prefix',len(oldc['requested_times_s'])==187 and tokens[:187]==oldc['requested_times_s']==c['baseline_requested_times_s'])
ck('new250_exact_times',[D(x) for x in tokens[187:]]==[D(x) for x in expected_extension])
ck('437_unique_increasing',len(tokens)==437 and all(D(a)<D(b) for a,b in zip(tokens,tokens[1:])))
out['time_counts']={'original':187,'added':250,'total':437}
for key in ('baseline_files','coordinates','external_source_pins','legacy_gate','legacy_contract','legacy_inner_manifest','limits','guard_expression','domains','lagrange_order','storestopcondsol'):
    ck('unchanged:'+key,c[key]==oldc[key])
ck('threshold_zero',D(c['threshold_mol_m3'])==0)
ck('end30',D(c['maximum_physical_s'])==30)
ck('one_runall_no_loadcopy',new.count(b'.runAll(')==1 and b'loadCopy(' not in new)
ck('budget_sum',sum(v for k,v in c['budgets_seconds'].items() if k!='overall')==c['budgets_seconds']['overall']==5100)
mapping=read(R/'COMMAND_MAP.json');fields=read(R/'NATIVE_APPROVAL_FIELD_SPEC.json')
for phase in ('compile','batch'):
    ck('mapped_argv:'+phase,mapping['native'][phase]['argv']==c['commands'][phase]==fields['required_future_fields']['commands'][phase])
    ck('mapped_cwd:'+phase,mapping['native'][phase]['cwd']==c['run_root'])
for action in ('execute','analyze'):
    x=mapping[action]
    ck('python_argv:'+action,x['executable']==c['python']['path'] and x['cwd']==c['cwd'] and x['argv']==['-I','-S','-B','-X','utf8',c['root']+'/src/candidate_entry.py',action,'--approval',c['approval_path'],'--manifest-sha',h((R/'CODE_MANIFEST.json').read_bytes())])
def functions(p):
    raw=p.read_text(encoding='utf-8');tree=ast.parse(raw)
    return {n.name:ast.get_source_segment(raw,n) for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
for file,base in [('candidate_entry.py','candidate_entry.py'),('diagnostic_consumer.py','trigger_consumer.py')]:
    a=functions(R/'src'/file);b=functions(R/'basis/src'/base)
    out.setdefault('function_diff',{})[file]={'unchanged':[k for k in a if k in b and a[k]==b[k]],'changed':[k for k in a if k in b and a[k]!=b[k]],'added':[k for k in a if k not in b],'removed':[k for k in b if k not in a]}
ck('incomplete_schemas_same',functions(R/'src/candidate_entry.py')['incomplete_result']==functions(R/'src/diagnostic_consumer.py')['incomplete_result'])
ps=(R/'PARENT_COMMAND.ps1').read_text();ops=(R/'basis/PARENT_COMMAND.ps1').read_text()
for start,end in [('function BSave','function BInvoke'),('function BInvoke','function GDecision')]:
    ck('parent_unchanged:'+start,ps[ps.index(start):ps.index(end)]==ops[ops.index(start):ops.index(end)])
before=read(R/'PRESERVATION_BEFORE.json');after=read(R/'PRESERVATION_AFTER.json')
bm={r['path']:(r['bytes'],r['sha256']) for r in before};am={r['path']:(r['bytes'],r['sha256']) for r in after}
ck('38_preserved_in_sender_records',len(before)==len(bm)==38 and all(am.get(k)==v for k,v in bm.items()))
out['preservation']={'before_count':len(before),'after_count':len(after),'before_subset_equal':True,'remote_current_files_directly_observed':False}
plan=read(R/'LIMITED_VALIDATION_PLAN.json');ids=[case['id'] for group in plan['groups'] for case in group['cases']]
ck('plan_counts',len(plan['groups'])==plan['logical_groups']==17 and len(ids)==len(set(ids))==plan['listed_case_specs']==53)
out['plans']={'groups':17,'listed_cases':53,'functional_execution':False,'engines':plan['sessions']}
save('STATIC_REVIEW_AUDIT.json',out)
w={'scope':'Reviewer arithmetic counterexamples, not execution of received functions',
   'N30_N1':{'reference_N':'1','reference_P':'1','reference_electrolyte':'1','current_N':'1.0000005','current_P':'0.9999995','current_electrolyte':'1','total_difference':'0','each_changed_absolute_difference':'0.0000005','each_changed_relative_difference':'0.0000005','candidate_relative_1e6_check':True,'retained_absolute_1e9_check':False,'not_actual_COMSOL_data':True},
   'N30_N2':{'scenario':'Successful FINAL_BOUNDARY BSave/BRef takes time across limit; no I/O exception','before_write_overall_seconds':'5099.9','after_write_snapshot_seconds':'5100.1','before_write_within_limits':True,'candidate_final_print_reuses_before_write_flag':True,'post_write_acceptance_should_be':False,'actual_elapsed_measurement':False}}
save('STATIC_COUNTEREXAMPLES.json',w)
print(json.dumps({'static_checks':len(out['checks']),'all_static_checks_pass':all(out['checks'].values()),'function_diff':out['function_diff'],'preservation':out['preservation'],'target_execution':0},ensure_ascii=False))
