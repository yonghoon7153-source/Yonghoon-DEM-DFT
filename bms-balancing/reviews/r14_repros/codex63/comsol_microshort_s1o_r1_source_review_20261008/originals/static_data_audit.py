"""Reviewer data and source-text comparisons only, not execution of candidate functions."""
from pathlib import Path
import ast,hashlib,json,collections
ROOT=Path(__file__).resolve().parent
R=ROOT/'received/main'
OLD=ROOT.parent/'microshort_s1o_preparation_review_20261007/received'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
changes=read(R/'CHANGED_FILES.json');checks=[]
for entry in changes:
    a=(OLD/entry['path']).read_bytes();b=(R/entry['path']).read_bytes()
    checks.append({'path':entry['path'],'old_matches':len(a)==entry['old_bytes'] and sha(a)==entry['old_sha256'],
                   'new_matches':len(b)==entry['new_bytes'] and sha(b)==entry['new_sha256']})
assert all(c['old_matches'] and c['new_matches'] for c in checks)
changed_names={e['path'] for e in changes}
cm=read(R/'CODE_MANIFEST.json');unchanged=[]
for entry in cm['files']:
    name=entry['path']
    if name in changed_names or name=='VALIDATION_PLAN_R1.json':continue
    assert (OLD/name).read_bytes()==(R/name).read_bytes(),name
    unchanged.append(name)
a=(OLD/'candidate/variants/P0.java.inactive.txt').read_bytes()
b=(R/'candidate/variants/P0.java.inactive.txt').read_bytes()
assert b.count(b'accepted tsteps storage')==1
assert b.replace(b'accepted tsteps storage',b'requested tlist storage')==a
def function_texts(path):
    text=path.read_text(encoding='utf8');lines=text.splitlines();tree=ast.parse(text)
    out={}
    for node in tree.body:
        if isinstance(node,(ast.FunctionDef,ast.ClassDef)):
            begin=min([node.lineno]+[d.lineno for d in getattr(node,'decorator_list',[])])
            out[node.name]='\n'.join(lines[begin-1:node.end_lineno])
    return out
old_functions=function_texts(OLD/'candidate/consumer.py.inactive.txt')
new_functions=function_texts(R/'candidate/consumer.py.inactive.txt')
assert old_functions.keys()==new_functions.keys()
changed_functions=[n for n in old_functions if old_functions[n]!=new_functions[n]]
plan=read(R/'VALIDATION_PLAN_R1.json');cases=plan['cases'];ids=[c['id'] for c in cases]
old_ids={c['id'] for c in read(R/'reference/ORIGINAL_VALIDATION_PLAN.json')['cases']}
assert len(ids)==len(set(ids))==130 and old_ids<=set(ids) and len(old_ids)==98
spans=[]
for entry in plan['extraction_spans']:
    lines=(R/entry['source']).read_text(encoding='utf8').splitlines()
    start,end=entry['start_line'],entry['end_line']
    data='\n'.join(lines[start-1:end]).encode('utf8')
    spans.append({'source':entry['source'],'name':entry['name'],'start_line':start,'end_line':end,
                  'valid_nonempty_range':1<=start<=end<=len(lines) and len(data)>0,
                  'computed_sha256':sha(data),'declared_sha256':entry['sha256'],'hash_matches':sha(data)==entry['sha256']})
parent_lines=(R/'candidate/Parent.ps1.inactive.txt').read_text(encoding='utf8').splitlines()
before=read(R/'ORIGINALS_BEFORE.json');after=read(R/'ORIGINALS_AFTER.json')
before_set={x['path']:(x['bytes'],x['sha256']) for x in before}
after_set={x['path']:(x['bytes'],x['sha256']) for x in after['files']}
assert len(before_set)==len(after_set)==116 and before_set==after_set
result={
 'scope':'Byte/text/JSON/AST syntax data inspection. Candidate functions and tests not run.',
 'changed_file_checks':checks,'unchanged_manifest_member_count':len(unchanged),'unchanged_members':unchanged,
 'P0_only_summary_literal_changed':True,'consumer_changed_functions':changed_functions,
 'cases':len(cases),'unique_ids':len(set(ids)),'old_ids_preserved':len(old_ids),'new_ids':sorted(set(ids)-old_ids),
 'engine_counts':dict(collections.Counter(c['engine'] for c in cases)),
 'group_counts':dict(collections.Counter(c['group'] for c in cases)),
 'extraction_spans':spans,'invalid_ranges':[e for e in spans if not e['valid_nonempty_range']],
 'actual_S1Sha_line23_normalized_no_final_LF_sha256':sha(parent_lines[22].encode('utf8')),
 'PARENT12':next(c for c in cases if c['id']=='PARENT12'),
 'final_return_cases':[{'id':c['id'],'expected_field_path':c.get('expected_field_path'),
                       'positive_control_case_id':c.get('positive_control_case_id')}
                      for c in cases if 'S1FinalReturn' in c['target_functions']],
 'preservation_record_set_equal_count':116,
 'preservation_scope':'Submitted before/after record comparison; not current execution-host observation',
 'directive_sha256':sha((R/'reference/R1_DIRECTIVE_v2_KO.md').read_bytes()),
}
with (ROOT/'STATIC_DATA_AUDIT.json').open('x',encoding='utf8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
print(json.dumps({k:v for k,v in result.items() if k not in ('extraction_spans','PARENT12','unchanged_members','changed_file_checks')},ensure_ascii=False))
