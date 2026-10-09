"""Independent hashes/record arithmetic/source-text comparisons only; no candidate execution."""
from pathlib import Path
import hashlib, json, ast, difflib
from collections import Counter
from decimal import Decimal

ROOT=Path(__file__).resolve().parent
R=ROOT/'received'
def sha(b): return hashlib.sha256(b).hexdigest()
def obj(n): return json.loads((R/n).read_text(encoding='utf-8-sig'))
audit={}
for name,prefix in [('CODE_MANIFEST.json',''),('reference/r1/CODE_MANIFEST.json','reference/r1/')]:
    m=obj(name)
    for r in m['files']:
        b=(R/(prefix+r['path'])).read_bytes()
        assert len(b)==r['bytes'] and sha(b)==r['sha256'],r['path']
    audit[name]={'members_matched':len(m['files']),'sha256':sha((R/name).read_bytes())}
prior=(R/'reference/PRIOR_REVIEW.zip').read_bytes()
assert sha(prior)=='9524f8ce7e5cef2722675806a2d92ac69b27188012bf50c758de7a260dee1486'
base=(R/'reference/r1/candidate/variants/P0.java.inactive.txt').read_bytes()
new=(R/'candidate/P0.connection.java.inactive.txt').read_bytes()
insert_start=new.index(b'    // BEGIN S1 OPEN ADDITIVE HELPERS.')
insert_end=new.index(b'    public static void main(',insert_start)
insertion=new[insert_start:insert_end]
assert new[:insert_start]+new[insert_end:]==base
fragment=(R/'candidate/InstalledReadback.fragment.java.inactive.txt').read_bytes()
assert insertion.replace(b'\r\n',b'\n')==fragment.replace(b'\r\n',b'\n')+b'\n'
assert sha(insertion)==obj('evidence/JAVA_REVERSE_BINDING.json')['removed_insert_sha256']
audit['java']={'reverse_full_bytes_equal':True,'insert_bytes':len(insertion),'insert_sha256':sha(insertion),'fragment_relation':'CRLF-normalized fragment plus exactly one separator LF','runAll_count_unchanged':base.count(b'.runAll(')==new.count(b'.runAll('),'inactive_main_unchanged':b'public static void main(String[] args) throws Exception { denyS0Execution(); }' in new}
for f in ('raw_connection.py.inactive.txt','resource_connection.py.inactive.txt'):
    text=(R/'candidate'/f).read_text(encoding='utf8')
    ast.parse(text) # syntax tree only, not compiled/imported/evaluated
    diff=(R/'candidate'/(f+'.diff.txt')).read_text(encoding='utf8').splitlines()
    added=[line[1:] for line in diff if line.startswith('+') and not line.startswith('+++')]
    assert added==text.splitlines()
audit['new_python_ast_and_added_diff']='MATCHED_NO_EXECUTION'
for s in obj('FUNCTION_SPANS.json'):
    lines=(R/s['file']).read_text(encoding='utf8').splitlines()
    assert sha('\n'.join(lines[s['start_line']-1:s['end_line']]).encode())==s['span_sha256']
audit['function_spans_matched']=len(obj('FUNCTION_SPANS.json'))
def identities(rows):
    return {x['path'].replace('\\','/').casefold():(x['bytes'],x['sha256']) for x in rows}
before=obj('evidence/SELECTED_SOURCES_BEFORE.json')
after=obj('evidence/SELECTED_SOURCES_AFTER_STATIC.json')
prepack=obj('evidence/SELECTED_SOURCES_AFTER_PREPACKAGE.json')
assert len(identities(before))==len(before)==33
assert identities(before)==identities(after)==identities(prepack)
audit['selected_preservation']={'recorded_rows':33,'before_static_prepackage_identical_by_identity':True,'before_prepackage_bytes_identical':(R/'evidence/SELECTED_SOURCES_BEFORE.json').read_bytes()==(R/'evidence/SELECTED_SOURCES_AFTER_PREPACKAGE.json').read_bytes(),'remote_current_observation':False,'external_after_package_hash_reported_by_user':'eab7035bce73a5a141bce45e9635ddea267b7b48f48a798e523a59456cf6306c'}
st=obj('STATIC_CHECKS.json')
assert len(st['checks'])==st['check_count']==74 and all(x['matched'] is True for x in st['checks'])
audit['submitted_static_records']={'count':74,'all_matched_assertions':True,'not_functional_tests':True}
plan=obj('LIMITED_VALIDATION_PLAN.json'); cases=plan['cases']
assert len(cases)==len(set(x['id'] for x in cases))==50
assert len(set(x['group'] for x in cases))==8
assert Counter(x['engine'] for x in cases)==plan['counts']
for p in plan['source_pins']:
    rel=p['path'].split('/microshort_s1_open_connection_candidate_20261009/')[1]
    b=(R/rel).read_bytes(); assert len(b)==p['bytes'] and sha(b)==p['sha256']
audit['plan_structure']={'groups':8,'cases':50,'engines':dict(Counter(x['engine'] for x in cases)),'budget_sum':sum(v for k,v in plan['budget_proposal_s'].items() if k!='total'),'proposed_only':True,'note':'Matching counts and hashes does not establish branch reach or functional correctness.'}
origin=obj('ORIGIN.json'); phases=obj('PHASE_RECORDS.json')
freq=Decimal(origin['frequency']); t0=Decimal(origin['monotonic_ticks']); td=Decimal(phases['delivery']['start_ticks'])
for k in ('preparation','static'):
    p=phases[k]; assert (Decimal(p['end_ticks'])-Decimal(p['start_ticks']))/freq==Decimal(str(p['elapsed_s']))
audit['timing']={'phase_records_arithmetic_matched':True,'delivery_origin_offset_s':str((td-t0)/freq),'external_receipt_total_by_ticks_s':str((Decimal(20538587910868)-t0)/freq),'external_package_return_total_by_ticks_s':str((Decimal(20538588553653)-t0)/freq),'final_check_reported_s':'1684.9520819','post_check_write_reported_s':'1685.0463578','post_check_write_delivery_reported_s':'130.0137145','last_boundary':'After check-file write/readback; BEFORE check-file SHA computation and tool return (corrected user transcription).','complete_after_transcription_elapsed':'UNOBSERVED','user_external_records_original_bytes_received':False}
pasted=Path('C:/Users/Administrator/.codex/attachments/fc65cc7a-b5c9-4165-b359-750296bc1a0d/붙여넣은 텍스트.txt').read_bytes()
audit['pasted_report']={'bytes':len(pasted),'sha256':sha(pasted),'normalized_text_matches_packaged_report':pasted.decode('utf-8-sig').replace('\r\n','\n').strip()==(R/'REPORT_KO.md').read_text(encoding='utf-8-sig').replace('\r\n','\n').strip()}
audit['reviewer_actions']={'received_code_import_compile_execute':0,'submitted_tests':0,'COMSOL_JVM':0,'reviewer_owned_data_inspection_only':True}
(ROOT/'DATA_AUDIT.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(audit,ensure_ascii=False,indent=2))
