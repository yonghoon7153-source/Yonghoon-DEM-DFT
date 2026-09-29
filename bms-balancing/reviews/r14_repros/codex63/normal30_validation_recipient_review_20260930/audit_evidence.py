"""Static/data audit only; no imports/calls of submitted modules or engines."""
import ast
from collections import Counter
import difflib
import hashlib
import io
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parent
R = ROOT / 'received'
OLD = ROOT.parent / 'normal30_review_20260928' / 'received'
def read(n): return json.loads((R/n).read_bytes())
def sha(b): return hashlib.sha256(b).hexdigest()
checks = []
def check(name, ok, detail=None):
    checks.append(dict(check=name, passed=bool(ok), detail=detail))
def key(r): return (r['group'],r['case'])
with zipfile.ZipFile(R/'prior_attempt02/COMSOL63_NORMAL30_ATTEMPT02_PARTIAL_20260928.zip') as z:
    nested = {n:z.read(n) for n in z.namelist()}
files = {p.relative_to(R).as_posix():p.read_bytes() for p in R.rglob('*') if p.is_file()}
all_data = list(files.items())+ [('nested/'+n,b) for n,b in nested.items()]
cm = read('candidate_snapshot/CODE_MANIFEST.json')
mh = sha(files['candidate_snapshot/CODE_MANIFEST.json'])
seal1 = read('prior_attempt02/PRE_TEST_SEAL.json')
seal2 = read('PRE_TEST_SEAL.json')
for n in ['CODE_MANIFEST.json']+[v['file'] for v in cm['files']]:
    b = files['candidate_snapshot/'+n]
    for label,s in [('prior',seal1),('current',seal2)]:
        row=[r for r in s['files'] if r['path'].endswith('/normal30_limited_validation_R1_20260928/'+n)]
        check(label+'_seal:'+n, len(row)==1 and row[0]['bytes']==len(b) and row[0]['sha256']==sha(b))
    matching=[(p,v) for p,v in nested.items() if p.endswith('/'+n) or p==n]
    check('nested_candidate:'+n, any(v==b for p,v in matching), [p for p,v in matching])
for n in ('records/positive_result.json','records/protected_result.json'):
    check('reused_fixture:'+n, files[n]==nested[n])
    check('fixture_manifest:'+n, read(n)['code_manifest_sha256']==mh)
for n,b in files.items():
    if n.startswith('prior_attempt02/') and not n.endswith('.zip'):
        rel=n.removeprefix('prior_attempt02/')
        if rel == 'DELIVERY_RECEIPT.json':
            receipt=json.loads(b)
            archive=files['prior_attempt02/COMSOL63_NORMAL30_ATTEMPT02_PARTIAL_20260928.zip']
            check('prior_external_receipt_identity',receipt['zip']['sha256']==sha(archive) and receipt['zip']['bytes']==len(archive) and receipt['recipient'] is None)
            continue
        check('prior_copy:'+rel, nested.get(rel)==b)
py=read('prior_attempt02/records/PYTHON_RESULT.json')['results']
ps=read('records/PS_RESULT.json')['results']
combined=read('COMBINED_CASE_RESULTS.json')
jout=files['prior_attempt02/records/Java_stub_stdout.txt'].decode().splitlines()
jcases=[line.split()[0] for line in jout if line.endswith(' PASS')]
check('python_47_unique_pass',len(py)==len(set(map(key,py)))==47 and all(r['status']=='PASS' for r in py))
check('ps_56_unique_pass',len(ps)==len(set(map(key,ps)))==56 and all(r['status']=='PASS' for r in ps))
check('java_8_unique_pass',len(jcases)==len(set(jcases))==8 and 'JAVA_PASS 8' in jout)
check('ps_declared_case_set',set(map(key,ps))==set(map(key,read('CASE_MAP.json')['cases'])))
check('combined_113_unique',len(combined['cases'])==len(set(map(key,combined['cases'])))==113)
check('combined_17_groups',len({x['group'] for x in combined['cases']})==17)
for eng,rows in [('Python',py),('PS51',ps)]:
    check('combined_'+eng,set(map(key,rows))=={key(r) for r in combined['cases'] if r['engine']==eng})
check('combined_java',set(jcases)=={r['case'] for r in combined['cases'] if r['engine']=='Java'})
check('two_static_checks',sum(r['status']=='PASS_STATIC_DATA' for r in combined['cases'])==2)
for phase in ('Python','Java_compile','Java_stub'):
    h=read('prior_attempt02/records/HOST_'+phase+'.json')
    check('host_rc_'+phase,h['returncode']==0 and h['timeout'] is False)
    for stream in ('stdout','stderr'):
        b=nested['records/'+phase+'_'+stream+'.txt']
        check(phase+'_'+stream+'_identity',len(b)==h[stream+'_bytes'] and sha(b)==h[stream+'_sha256'])
ph=read('records/HOST_PS51.json')
check('ps_host_rc',ph['returncode']==0 and ph['timeout'] is False and ph['exception'] is None and ph['elapsed_seconds']<=90)
for st in ('stdout','stderr'):
    b=files['records/PS51_'+st+'.txt'];r=ph[st]
    check('ps_'+st+'_identity',sha(b)==r['sha256'] and len(b)==r['bytes'])
tr=read('records/TOOL_RETURN_TRANSCRIPTION.json')['completion']
check('ps_outer_transcript',tr['exit_code']==0 and json.loads(tr['output'].splitlines()[0])==ph)
parent=files['candidate_snapshot/PARENT_COMMAND.ps1'].decode().replace('\r\n','\n')
ext=read('records/PS_EXTRACTED.json')
for r in ext:
    src=r['source'].replace('\r\n','\n')
    lines='\n'.join(parent.splitlines()[r['start']-1:r['end']])
    check('exact_extraction:'+r['name'],src in lines)
java=files['candidate_snapshot/src/Normal30Candidate.java'].decode().replace('\r\n','\n')
h=read('prior_attempt02/tests/JAVA_SOURCE_BINDING.json')
helper=h['helper']
check('java_helper_exact',helper in java and helper in files['prior_attempt02/tests/ShapeHarness.java'].decode().replace('\r\n','\n') and sha(helper.encode())==h['helper_sha256'])
c=read('candidate_snapshot/CONTRACT.json')
check('java_tlist_437',re.findall(r'\.set\("tlist","([^"]+)"\)',java)[0].split()==c['requested_times_s'] and len(c['requested_times_s'])==437)
check('java_threshold_0_runall1','m.param().set("ce_stop_threshold","0[mol/m^3]");' in java and java.count('.runAll();')==1)
check('initial_li_contract',c['limits']['initial_Li_absolute_mol_m2']=='1e-9' and c['limits']['relative_Li']=='0.000001')
# Independent comparison against the previously received normal30 preparation.
diffs=[]
for n in ('src/Normal30Candidate.java','src/candidate_entry.py','src/diagnostic_consumer.py','PARENT_COMMAND.ps1','CONTRACT.json'):
    old=OLD/n
    if not old.exists():
        check('prior_review_available:'+n,False);continue
    b=files['candidate_snapshot/'+n];a=old.read_bytes()
    if n in ('src/Normal30Candidate.java','src/candidate_entry.py'):
        check('original_byte_identical:'+n,a==b)
    diffs+=list(difflib.unified_diff(a.decode().replace('\r\n','\n').splitlines(True),b.decode().replace('\r\n','\n').splitlines(True),fromfile='previous/'+n,tofile='candidate/'+n))
(ROOT/'INDEPENDENT_SOURCE_DIFF.patch').write_text(''.join(diffs),encoding='utf-8')
# Verify branch evidence against the actual stored fixture outputs.
obs={x['name']:x for x in read('records/PS_RESULT.json')['observations']}
branch_summary=[]
for name in ('overall','delivery','pre_over','body','exact_overall','exact_delivery','valid'):
    b=read('ps_fixture/'+name+'/FINAL_BOUNDARY.json')
    lines=files['ps_fixture/'+name+'/FINAL_CONSOLE.txt'].decode().splitlines()
    final=json.loads(next(x for x in lines if 'USER_PARENT_FINAL_RETURN' in x))
    check('raw_fixture_observation:'+name,b==obs[name]['boundary'] and final==obs[name]['final'])
    expected=final['snapshot_seconds']<=5100 and final['delivery_elapsed_seconds']<=300 and b['within_limits']
    check('post_budget_recomputed:'+name,final['within_limits']==expected)
    if name in ('overall','delivery'):
        check('late_overrun_overrides:'+name,b['within_limits'] is True and final['within_limits'] is False and final['limited']=='INCOMPLETE')
    branch_summary.append(dict(name=name,pre_within=b['within_limits'],post_within=final['within_limits'],post_limited=final['limited'],overall=final['snapshot_seconds'],delivery=final['delivery_elapsed_seconds']))
for name in ('writer','transcript','last_return'):
    raw=files['ps_fixture/'+name+'/FINAL_CONSOLE.txt'].decode()
    check('missing_final_return:'+name,'USER_PARENT_FINAL_RETURN' not in raw)
check('native_not_approved',combined['native30_approved'] is False and cm['approved'] is False and cm['usable'] is False)
before=read('PRESERVATION_BEFORE.json');after=read('PRESERVATION_AFTER.json')
check('preservation_records_equal',before==after)
# Avoid interpreting sender-only paths as locally observed remote files.
preserved=before if isinstance(before,list) else before.get('files',[])
present=[];not_present=[]
for r in preserved:
    found=[p for p,b in all_data if len(b)==r['bytes'] and sha(b)==r['sha256']]
    (present if found else not_present).append(dict(path=r['path'],included_matching_bytes=found))
for r in read('FINAL_SOURCE_BINDING.json')['files']:
    check('reported_final_binding:'+r['expected']['path'],r['actual']==r['expected'] and r['matches'] is True)
# Structural parse is never execution of Python.
for n in ('candidate_snapshot/src/diagnostic_consumer.py','candidate_snapshot/src/candidate_entry.py','prior_attempt02/tests/run_python.py'):
    ast.parse(files[n].decode());check('ast_parse:'+n,True)
old_contract=json.loads((OLD/'CONTRACT.json').read_bytes())
def differences(a,b,p=''):
    if type(a)!=type(b):return [p]
    if isinstance(a,dict):
        return sum((differences(a.get(k),b.get(k),p+'/'+k) for k in sorted(set(a)|set(b))),[])
    if isinstance(a,list):
        if len(a)!=len(b):return [p]
        return sum((differences(x,y,p+'/'+str(i)) for i,(x,y) in enumerate(zip(a,b))),[])
    return [] if a==b else [p]
report=dict(scope='Recipient data/static comparison; target tests/native code never executed',checks=checks,
    passed=sum(x['passed'] for x in checks),failed=[x for x in checks if not x['passed']],
    functional_counts={'Python':len(py),'Java':len(jcases),'PS51':len(ps)},static_checks=2,finalizer_branches=branch_summary,
    candidate_manifest_sha256=mh,contract_changed_paths=differences(old_contract,c),
    sender_preservation_count=len(preserved),preservation_included=present,preservation_not_included=not_present,
    limitations=['No independent native test rerun','Sender host returns are serialized evidence, not recipient remote observation',
    'Current delivery receipt and outer closeout return not included in the received archive'])
(ROOT/'EVIDENCE_AUDIT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:report[k] for k in ('passed','failed','functional_counts','static_checks','finalizer_branches','contract_changed_paths','sender_preservation_count')},ensure_ascii=False,indent=2))
