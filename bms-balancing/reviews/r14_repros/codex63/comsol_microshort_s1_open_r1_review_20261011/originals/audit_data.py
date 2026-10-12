"""Reviewer-owned data audit. Never import or execute submitted code."""
import ast
import collections
import difflib
import hashlib
import json
import pathlib
import zipfile
from decimal import Decimal

OUT = pathlib.Path(__file__).resolve().parent
R = OUT / 'received'
checks = []
def sha(b): return hashlib.sha256(b).hexdigest()
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def check(name, ok, detail=None): checks.append({'name':name,'matched':bool(ok),'detail':detail})
def rel(s):
    marker='/microshort_s1_open_connection_r1_20261010/'
    s=s.replace('\\','/')
    return s.split(marker,1)[1] if marker in s else s
def identity(row):
    p=R/rel(row['path'])
    if not p.is_file(): return False
    b=p.read_bytes()
    return len(b)==row['bytes'] and sha(b)==row['sha256']

manifest=read(R/'CODE_MANIFEST.json')
check('code_manifest_14',len(manifest['files'])==14 and all(identity(x) for x in manifest['files']))
binding=read(R/'REVISION_BINDING.json')
changed=[]
for x in binding['members']:
    old=(R/'basis/prior_preparation'/x['path']).read_bytes()
    new=(R/x['path']).read_bytes()
    check('revision:'+x['path'], len(old)==x['previous_bytes'] and sha(old)==x['previous_sha256'] and len(new)==x['current_bytes'] and sha(new)==x['current_sha256'] and (old!=new)==x['changed'])
    if old!=new: changed.append(x['path'])
check('only_expected_three_old_members_changed',changed==['candidate/resource_connection.py.inactive.txt','candidate/resource_connection.py.inactive.txt.diff.txt','LIMITED_VALIDATION_PLAN.json'],changed)

oldzip=pathlib.Path('C:/Users/Administrator/Downloads/COMSOL_MICROSHORT_S1_OPEN_CONNECTION_PREPARATION_20261009.zip')
if oldzip.exists():
    check('previous_zip_identity',oldzip.stat().st_size==1929576 and sha(oldzip.read_bytes())=='32cbb6ee5b8885a645da762154dab38d8f67ef4c7f97b5b4bc9c2ecd5fdd6f5c')
    with zipfile.ZipFile(oldzip) as z:
        entries=[x for x in z.infolist() if not x.is_dir()]
        check('basis_exact_original_80_members',len(entries)==80 and all((R/'basis/prior_preparation'/x.filename).read_bytes()==z.read(x) for x in entries))
else: check('previous_zip_local_available',False)
review=(R/'basis/REVIEW.zip').read_bytes()
check('previous_review_zip_identity',len(review)==1953422 and sha(review)=='f23d02b01b7a2ae96a2cfcf17009d73a2c47cddae7895c124aea6543b15bdd15')
with zipfile.ZipFile(R/'basis/REVIEW.zip') as z:
    check('review_text_original',z.read('REVIEW_KO.md')==(R/'basis/REVIEW_KO.md').read_bytes())

spans=read(R/'FUNCTION_SPANS.json')['spans']
for s in spans:
    b=(R/s['path']).read_bytes(); lines=b.splitlines(keepends=True)
    start=sum(map(len,lines[:s['first_line']-1]));end=sum(map(len,lines[:s['last_line']]))
    raw=b[start:end]
    normalized='\n'.join(raw.decode('utf-8').splitlines()).encode('utf-8')
    check('span:'+s['id'],len(b)==s['source_bytes'] and sha(b)==s['source_sha256'] and start==s['byte_start_inclusive'] and end==s['byte_end_exclusive'] and sha(raw)==s['raw_span_sha256'] and sha(normalized)==s['lf_no_final_lf_sha256'])
check('span_count',len(spans)==86,len(spans))

before=read(R/'evidence/SELECTED_SOURCES_BEFORE.json')
files=before['files']; bypath=collections.defaultdict(list)
for x in files: bypath[x['path'].replace('\\','/').casefold()].append((x['bytes'],x['sha256']))
check('preservation_count_and_duplicate_identity',len(files)==112 and len(bypath)==111 and all(len(set(v))==1 for v in bypath.values()),{'items':len(files),'unique_paths':len(bypath)})
for filename in ['SELECTED_SOURCES_AFTER_STATIC.json','SELECTED_SOURCES_AFTER_PREPACKAGE.json']:
    check('preservation_records:'+filename,read(R/'evidence'/filename)['files']==files)
static=read(R/'STATIC_CHECKS.json')
check('reported_static_records_consistent',static['count']==static['matched']==len(static['checks'])==151 and all(x['matched'] is True for x in static['checks']))

plan=read(R/'LIMITED_VALIDATION_PLAN.json');cases=plan['cases'];ids=[x['id'] for x in cases];positions={x:i for i,x in enumerate(ids)}
engines=collections.Counter(x['engine'] for x in cases);groups=collections.Counter(x['group'] for x in cases)
check('plan_counts',len(cases)==len(set(ids))==93 and len(groups)==9 and engines=={'Python':87,'Java_helper':6},dict(engines))
check('old_50_case_ids_retained',set(x['id'] for x in read(R/'basis/prior_preparation/LIMITED_VALIDATION_PLAN.json')['cases'])<=set(ids))
check('cases_are_not_executed',all(x['actual_execution']=='NOT_EXECUTED' for x in cases))
pins={}
for field in ['source_pins','existing_core_pins','contract_and_dependency_pins','source_byte_bindings']:
    pins[field]=len(plan[field]);check('plan_pin:'+field,all(identity(x) for x in plan[field]))
check('span_file_pin',identity(plan['dependency_span_file']))
ordering=[]
for c in cases:
    p=c['positive_control']
    if p not in positions or positions[p]>positions[c['id']]: ordering.append({'case':c['id'],'positive_control':p})
blocks=[]
for c in cases:
    if not blocks or blocks[-1]['engine']!=c['engine']: blocks.append({'engine':c['engine'],'ids':[]})
    blocks[-1]['ids'].append(c['id'])

source=R/'candidate/resource_connection.py.inactive.txt'
tree=ast.parse(source.read_text(encoding='utf-8-sig'),filename=source.name)
check('resource_ast_parse_only',isinstance(tree,ast.Module))
old=(R/'basis/prior_preparation/candidate/resource_connection.py.inactive.txt').read_text(encoding='utf-8-sig')
new=source.read_text(encoding='utf-8-sig')
submitted=(R/'candidate/resource_connection.py.inactive.txt.diff.txt').read_text(encoding='utf-8-sig')
expected=list(difflib.unified_diff(old.splitlines(keepends=True),new.splitlines(keepends=True)))
check('resource_minimal_diff_body',submitted.splitlines()[2:]==''.join(expected).splitlines()[2:])

origin=read(R/'ORIGIN.json');phases=read(R/'PHASE_RECORDS.json');freq=Decimal(origin['frequency'])
for name in ['correction','static','plan_reseal']:
    x=phases[name]; elapsed=Decimal(x['end_ticks']-x['start_ticks'])/freq
    check('phase_arithmetic:'+name,elapsed==Decimal(str(x['elapsed_s'])) and elapsed<=x['limit_s'])
for name,tick,overall,delivery in [('receipt',21956921264806,'854.6578693','82.061403'),('final_check',21957130249817,'875.5563704','102.9599041')]:
    check('chat_tick_arithmetic:'+name,Decimal(tick-origin['monotonic_ticks'])/freq==Decimal(overall) and Decimal(tick-phases['preservation_delivery']['start_ticks'])/freq==Decimal(delivery))

result={'method':'Data/byte/AST/text only; no received module import, function call, test, JVM, COMSOL or OS resource experiment',
 'checks':checks,'matched':sum(c['matched'] for c in checks),'total':len(checks),'failed':[c for c in checks if not c['matched']],
 'case_counts':{'groups':dict(groups),'engines':dict(engines),'unique':len(set(ids))},'plan_pin_counts':pins,
 'plan_order_observation':{'declared':plan['case_order'],'positive_after_dependent':ordering,'listed_engine_blocks':blocks,'scope':'Review observation, not a functional test'},
 'provenance_limit':'Preservation files and chat external returns are supplied records, not fresh remote filesystem or OS observations. Static reported 151 are not re-executed checks.'}
(OUT/'DATA_AUDIT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'matched':result['matched'],'total':result['total'],'failed':result['failed'],'engines':dict(engines),'positive_after_dependent':ordering},ensure_ascii=False))
