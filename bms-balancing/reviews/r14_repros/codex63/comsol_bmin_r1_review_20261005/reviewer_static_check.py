"""Reviewer-owned source-text/data audit; never loads received code as a module or program."""
import hashlib, json, re, zipfile
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
ref = json.loads((HERE/'REFERENCE_TEXT.json').read_text(encoding='utf-8'))
prior = json.loads((HERE/'PRIOR_REFERENCE_TEXT.json').read_text(encoding='utf-8'))
tree = json.loads((HERE/'GIT_TREE.json').read_text(encoding='utf-8'))
files = {r['path']:r for r in ref['files']}
additional = json.loads((HERE/'ADDITIONAL_REFERENCE_TEXT.json').read_text(encoding='utf-8'))
files.update({r['path']:r for r in additional['files']})
old = {r['path']:r for r in prior['files']}
base = 'bms-balancing/comsol_candidates/bmin_particle640_r1_20261005/'
v1 = 'bms-balancing/comsol_candidates/bmin_particle640_20261004/'
def raw(p): return files[base+p]['content'].encode('utf-8')
def oldraw(p): return old[v1+p]['content'].encode('utf-8')
def sha(b): return hashlib.sha256(b).hexdigest()
def identity(b): return {'bytes':len(b),'sha256':sha(b)}
def obj(p): return json.loads(raw(p))
out = {'scope':'Static source text / JSON / hash / archived log checks only. Candidate functions and submitted tools were NOT imported, parsed as code, compiled, or executed.', 'commit':ref['commit']}
out['connector_blobs'] = []
for path,r in files.items():
    b=r['content'].encode('utf-8')
    blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    out['connector_blobs'].append({'path':path,**identity(b),'git_blob':blob,'match':blob==r['sha']})
manifest=obj('candidate/CODE_MANIFEST.json')
out['manifest'] = identity(raw('candidate/CODE_MANIFEST.json'))
out['manifest_matches_claim'] = out['manifest']['sha256']=='9dcb47f0ec3ec346b491d90c2836e3b30f54eb88fd5e4fbd216fc34782275cdb'
out['manifest_files']=[{'file':r['file'],'match':identity(raw('candidate/'+r['file']))=={'bytes':r['bytes'],'sha256':r['sha256']}} for r in manifest['files']]
out['byte_identical']={p:raw('candidate/'+p)==oldraw('candidate/'+p) for p in ['src/Bmin640Candidate.java','src/candidate_entry.py']}
lit=obj('R1_LITERAL_CHANGES.json')['PARENT_COMMAND.ps1']
current=raw('candidate/PARENT_COMMAND.ps1').decode().replace('\r\n','\n')
original=oldraw('candidate/PARENT_COMMAND.ps1').decode().replace('\r\n','\n')
occurrences=[]
for r in lit:
    n=current.count(r['after']);assert n==r['count'],(r,n)
    current=current.replace(r['after'],r['before']);occurrences.append(n)
a=current.index('function GNativeAxis(');b=current.index('\ntry {\n',a)+1
x=original.index('function GFields(');y=original.index('\ntry {\n',x)+1
current=current[:a]+original[x:y]+current[b:]
parent_restored=current.replace('\n','\r\n').encode()
c=raw('candidate/src/diagnostic_consumer.py');o=oldraw('candidate/src/diagnostic_consumer.py')
consumer_restored=c[:c.index(b'def mesh_evidence(')]+o[o.index(b'def mesh_evidence('):]
out['reverse']={'parent_exact_v1':parent_restored==oldraw('candidate/PARENT_COMMAND.ps1'),'parent_inverse_occurrences':occurrences,'consumer_exact_v1':consumer_restored==o}
contract=obj('candidate/CONTRACT.json');oldcontract=json.loads(oldraw('candidate/CONTRACT.json'))
out['contract_changed_top_keys']=[k for k in set(contract)|set(oldcontract) if contract.get(k)!=oldcontract.get(k)]
out['dof_status']={'before':oldcontract['expected_transient_dof'],'after':contract['expected_transient_dof']}
contract['expected_transient_dof']['status']=oldcontract['expected_transient_dof']['status']
out['contract_inverse_exact_object']=contract==oldcontract
before=sha(oldraw('candidate/CODE_MANIFEST.json'));after=sha(raw('candidate/CODE_MANIFEST.json'))
out['binding_only_manifest_change']={p:oldraw('candidate/'+p).replace(before.encode(),after.encode())==raw('candidate/'+p) for p in ['COMMAND_MAP.json','NATIVE_APPROVAL_FIELD_SPEC.json']}
tree_by={x['path']:x for x in tree['tree']}
out['prior_selected_tree_preservation']=[{'path':p,'same_blob':tree_by.get(p,{}).get('sha')==r['sha']} for p,r in old.items() if p.startswith(v1)]
plan=obj('LIMITED_VALIDATION_PLAN.json');ids=[c['id'] for g in plan['groups'] for c in g['cases']]
out['plan']={'groups':len(plan['groups']),'case_ids':len(ids),'unique_ids':len(set(ids)),'by_group':{g['id']:len(g['cases']) for g in plan['groups']},'budget_sum':sum(v for k,v in plan['budget_seconds'].items() if k!='overall'),'overall':plan['budget_seconds']['overall'],'manifest_matches':plan['manifest_sha256']==after,'all_cases_unexecuted_by_reviewer':True}
prec='0.001000000000000000000000000001'
out['precision_literal']={'text':prec,'decimal_places':len(prec.split('.')[1]),'significant_digits':len(Decimal(prec).as_tuple().digits),'greater_than_limit_exactly':Decimal(prec)>Decimal('0.001'),'powershell_not_executed':True}
archive=Path('C:/Users/Administrator/Downloads/COMSOL63_NORMAL480_NATIVE_RESULT_20261001.zip')
with archive.open('rb') as f: archive_sha=hashlib.file_digest(f,'sha256').hexdigest()
out['normal480_archive']={'file':str(archive),'bytes':archive.stat().st_size,'sha256':archive_sha}
assert archive_sha=='e991ab4c918f6576b18d6225a86ed41759ab6ee726dd6543b9a9158e581cbc30'
with zipfile.ZipFile(archive) as z:
    names=[n for n in z.namelist() if n.endswith('/batch.log') or n=='batch.log']
    out['batch_members']=names
    assert len(names)==1,names
    batchraw=z.read(names[0]);batch=batchraw.decode('utf-8-sig')
    out['batch_log_identity']={'member':names[0],**identity(batchraw)}
opening=list(re.finditer(r'^<---- Time-Dependent Solver.*$',batch,re.M))
closing=list(re.finditer(r'^----- Time-Dependent Solver.*-+>\s*$',batch,re.M))
assert len(opening)==len(closing)==1
start=opening[0].end();end=closing[0].start()
mentions=[(i+1,x) for i,x in enumerate(batch.splitlines()) if 'Number of degrees of freedom' in x]
inside=[x for x in batch[start:end].splitlines() if 'Number of degrees of freedom' in x]
pattern=r'Number of degrees of freedom solved for: (\d+) \(plus (\d+) internal DOFs\)\.'
out['normal480_dof']={'opening':opening[0].group().strip(),'closing':closing[0].group().strip(),'all_mentions':mentions,'transient_mentions':inside,'transient_regex_matches':re.findall(pattern,'\n'.join(inside))}
# A small, reviewer-owned data-only string model of the submitted line-count/search rule.
# This is NOT a call to mesh_evidence and is NOT a production functional test.
examples={
 'valid':'Number of degrees of freedom solved for: 79485 (plus 12 internal DOFs).',
 'two_lines':'Number of degrees of freedom solved for: 79485 (plus 12 internal DOFs).\nNumber of degrees of freedom solved for: 156925 (plus 12 internal DOFs).',
 'two_same_line':'Number of degrees of freedom solved for: 79485 (plus 12 internal DOFs). Number of degrees of freedom solved for: 156925 (plus 12 internal DOFs).',
 'valid_then_malformed_same_line':'Number of degrees of freedom solved for: 79485 (plus 12 internal DOFs). Number of degrees of freedom solved for: ???',
 'zero':'Number of degrees of freedom solved for: 0 (plus 12 internal DOFs).',
 'missing_internal':'Number of degrees of freedom solved for: 79485.'}
out['static_string_cases']=[]
for name,s in examples.items():
    lines=[x for x in s.splitlines() if 'Number of degrees of freedom' in x]
    hits=re.findall(pattern,s);h=re.search(pattern,lines[0]) if len(lines)==1 else None
    branch='COUNT' if len(lines)!=1 else 'FORMAT' if h is None else 'VALUE' if int(h.group(1))<=0 else 'ACCEPTS_FIRST_MATCH'
    out['static_string_cases'].append({'id':name,'text':s,'matching_lines':len(lines),'valid_occurrences':len(hits),'statically_predicted_branch':branch})
assert all(x['match'] for x in out['connector_blobs'])
assert all(x['match'] for x in out['manifest_files'])
assert all(out['byte_identical'].values()) and out['reverse']['parent_exact_v1'] and out['reverse']['consumer_exact_v1']
assert all(x['same_blob'] for x in out['prior_selected_tree_preservation'])
(HERE/'INDEPENDENT_STATIC_AUDIT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:out[k] for k in ['manifest','reverse','contract_inverse_exact_object','plan','precision_literal','normal480_dof','static_string_cases']},ensure_ascii=False))
