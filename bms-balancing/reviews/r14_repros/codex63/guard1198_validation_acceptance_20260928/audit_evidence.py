"""Read-only subject evidence comparisons; no candidate/test code execution."""
from pathlib import Path
import json, hashlib, collections, difflib, zipfile, ast
O=Path(__file__).resolve().parent; R=O/'received'; P=O.parent/'guard1198_review_20260928'/'received'
def read(n): return json.loads((R/n).read_bytes())
def ident(b): return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def norm(b): return b.decode('utf-8-sig').replace('\r\r\n','\n').replace('\r\n','\n')
def dump(n,v): (O/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
m=read('candidate/CODE_MANIFEST.json'); mh=ident((R/'candidate/CODE_MANIFEST.json').read_bytes())['sha256']
assert m['approved'] is False and m['usable'] is False
for f in m['files']: assert ident((R/'candidate'/f['file']).read_bytes())=={k:f[k] for k in ('bytes','sha256')}
pre=read('PRE_TEST_SEAL.json'); post=read('FINAL_SOURCE_BINDING.json')
assert pre['files']==post['files'] and pre['source_manifest_sha256']==mh
checked=[]; not_included=[]
for f in pre['files']:
    path=f['path']; local=None
    if '/guard1198_limited_validation_R1_20260928/' in path: local=R/'candidate'/path.split('/guard1198_limited_validation_R1_20260928/')[1]
    elif '/guard1198_validation_attempt_04_20260928/' in path: local=R/path.split('/guard1198_validation_attempt_04_20260928/')[1]
    else:
        bases={'/gate/c2_entry.py':'05_c2_entry.py','/gate/C2_CONTRACT.json':'06_C2_CONTRACT.json','/src/launcher.py':'16_launcher.py'}
        for suffix,base in bases.items():
            if path.endswith(suffix): local=P/'basis'/base
    if local is not None:
        assert ident(local.read_bytes())=={k:f[k] for k in ('bytes','sha256')},path
        checked.append(path)
    else:not_included.append(path)
assert read('PRESERVATION_BEFORE.json')==read('PRESERVATION_AFTER.json')
case=read('CASE_MAP.json')['cases']; results=read('RESULTS.json')
key=lambda x:(x['group'],x['case'])
assert len(case)==len(set(map(key,case)))==78
assert len(results['results'])==len(set(map(key,results['results'])))==78
assert set(map(key,case))==set(map(key,results['results']))
assert all(x['status']=='PASS' for x in results['results'])
assert len({x['group'] for x in case})==26
actual=read('records/PYTHON_RESULT.json')['results']+read('records/PS_RESULT.json')['results']
assert len(actual)==len(set(map(key,actual)))==65
assert {key(x) for x in actual}=={key(x) for x in case if not x['group'].startswith('J')}
assert all(x['status']=='PASS' for x in actual)
returns={k:read('records/'+n) for k,n in [('python','PYTHON_TOOL_RETURN.json'),('java_compile','JAVA_COMPILE_TOOL_RETURN.json'),('java_stub','JAVA_STUB_TOOL_RETURN.json'),('powershell','POWERSHELL_TOOL_RETURN.json')]}
assert all(x['exit_code']==0 for x in returns.values())
assert json.loads(returns['python']['output'])['subcases']==30
assert returns['powershell']['output'].strip()=='PS_PASS subcases=35'
assert [x for x in returns['java_stub']['output'].splitlines() if '|PASS' in x]==['J%02d|PASS'%i for i in range(1,7)]
java=(R/'candidate/src/Guard1198Candidate.java').read_text('utf-8-sig')
harness=(R/'tests/GuardHarness.java').read_text('utf-8-sig')
binding=read('tests/JAVA_SOURCE_BINDING.json')
assert binding['source_sha256']==ident((R/'candidate/src/Guard1198Candidate.java').read_bytes())['sha256']
for x in binding['extractions']:
    text=java[x['source_start']:x['source_end']]
    assert ident(text.encode())['sha256']==x['source_text_sha256'],x['name']
    assert text in harness,x['name']
parent=(R/'candidate/PARENT_COMMAND.ps1').read_bytes().decode('utf-8-sig')
ps=read('records/PS_EXTRACTED.json')
assert {x['name'] for x in ps}=={'BSave','BInvoke','GDecision'}
for x in ps: assert x['source'] in parent,x['name']
pybinding=read('tests/PYTHON_BODY_BINDING.json')
launcher=(P/'basis/16_launcher.py').read_text('utf-8-sig')
nodes=ast.parse(launcher).body
attest=next(x for x in nodes if isinstance(x,ast.FunctionDef) and x.name=='timed_attest')
text=ast.get_source_segment(launcher,attest)
assert text==pybinding['timed_attest_source']
assert ident(text.encode())['sha256']==pybinding['timed_attest_sha256']
# Exact reference identity and CRLF-normalized display diff are separate.
cor=read('CORRECTION.json'); hb=(R/'tests/run_python.py').read_bytes()
assert ident(hb.replace(b'\r\n',b'\n'))['sha256']==cor['after_harness_sha256']
with zipfile.ZipFile(R/'history/COMSOL63_GUARD1198_LIMITED_TEST3_FAILURE_20260928.zip') as h:
    previous=h.read('tests/run_python.py')
    assert ident(previous)['sha256']==cor['before_harness_sha256']
    previous_results=json.loads(h.read('RESULTS.json'))
    (O/'HARNESS_NORMALIZED.diff').write_text(''.join(difflib.unified_diff(norm(previous).splitlines(True),norm(hb).splitlines(True),fromfile='attempt03 (newline normalized)',tofile='attempt04 (newline normalized)')),encoding='utf-8')
diff=[]
for n in ['src/trigger_consumer.py','src/candidate_entry.py','PARENT_COMMAND.ps1','CONTRACT.json']:
    diff.extend(difflib.unified_diff(norm((P/n).read_bytes()).splitlines(True),norm((R/'candidate'/n).read_bytes()).splitlines(True),fromfile='original/'+n,tofile='R1/'+n))
(O/'CANDIDATE_NORMALIZED.diff').write_text(''.join(diff),encoding='utf-8')
contract=read('candidate/CONTRACT.json'); commands=read('candidate/COMMAND_MAP.json')
assert commands['manifest_sha256']==mh
for phase in ('compile','batch'):
    assert commands['native'][phase]['argv']==contract['commands'][phase]
    assert commands['native'][phase]['cwd']==contract['run_root']
assert commands['execute']['cwd']==commands['analyze']['cwd']==contract['cwd']
summary={
 'scope':'Data/static source-binding review, not a rerun',
 'code_manifest_sha256':mh,'code_files_verified':len(m['files']),
 'pre_post_seal_entries':len(pre['files']),'directly_matched_received_or_prior_source_pins':checked,
 'engine_files_not_directly_received_or_remote_remeasured':not_included,
 'case_map_unique_subcases':78,'unique_groups':26,
 'engines':{'Python':{'groups':14,'subcases':30},'Java_stub':{'groups':6,'subcases':13,'basis':'Sequential assertions plus 6 completion markers; not 13 independent stdout records'},'PS51':{'groups':6,'subcases':35}},
 'python_ps65_case_records_exact_set_all_pass':True,'java_9_extracted_bodies_match_source_and_harness':True,
 'ps_3_extracted_functions_match_parent':True,'legacy_timed_attest_body_matches':True,
 'tool_returns':{k:{j:v[j] for j in ('chunk_id','exit_code','wall_time_seconds')} for k,v in returns.items()},
 'harness_raw_identity':ident(hb),'correction_after_hash_is_LF_normalized_not_raw':cor['after_harness_sha256'],
 'prior_result_status':{k:v for k,v in previous_results.items() if k in ('status','subcases','logical_groups')},
 'preservation_before_after_entries_equal':len(read('PRESERVATION_BEFORE.json')),
 'current_contract_command_map_match':True,
 'subject_executions':0,'native_1198_approved':False,
 'delivery_final_receipt_in_zip':False,
 'time_limit':'PACKAGING_BOUNDARY is before ZIP construction; final delivery budget closure not independently established from this ZIP alone'
}
dump('EVIDENCE_AUDIT.json',summary)
print(json.dumps(summary,ensure_ascii=False))
