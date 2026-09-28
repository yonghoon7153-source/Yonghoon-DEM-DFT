"""Independent source-as-data checks, no candidate imports/functions/engines."""
from pathlib import Path
from decimal import Decimal
import ast,csv,hashlib,io,json,zipfile
O=Path(__file__).resolve().parent;R=O/'received'
def obj(n):return json.loads((R/n).read_bytes())
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(n,v):(O/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
manifest=obj('CODE_MANIFEST.json');c=obj('CONTRACT.json')
assert manifest['approved'] is manifest['usable'] is c['approved'] is c['usable'] is False
for r in manifest['files']:assert ident((R/r['file']).read_bytes())=={k:r[k] for k in ('bytes','sha256')}
assert c['candidate_java']['sha256']==ident((R/'src/Guard1198Candidate.java').read_bytes())['sha256']
ops=obj('TRANSFORM_RECORD.json')['operations']
candidate=(R/'src/Guard1198Candidate.java').read_text(encoding='utf-8');inverse=candidate
for op in reversed(ops):
    assert inverse.count(op['new'])==1,op['category']
    inverse=inverse.replace(op['new'],op['old'],1)
assert inverse.encode()==(R/'basis/00_ElectrolyteGuard300R320C16Trigger.java').read_bytes()
assert candidate.count('m.sol(sol).runAll();')==1 and 'comp1.x' not in candidate
assert 'loadCopy(' not in candidate and 'getPreference(' not in candidate
basis=obj('BASIS_MAP.json');basislocal=[]
for b in basis:
    assert ident((R/b['copy']).read_bytes())=={k:b['source'][k] for k in ('bytes','sha256')};basislocal.append(b['copy'])
assert obj('PRESERVATION_BEFORE.json')==obj('PRESERVATION_AFTER.json')
prior=[];unmatched=[];baseline=[]
with zipfile.ZipFile('C:/Users/Administrator/Downloads/COMSOL63_ELECTROLYTE_GUARD_HANDOFF.zip') as guard, zipfile.ZipFile('C:/Users/Administrator/Downloads/COMSOL63_B020_EVIDENCE_RECONCILIATION_REVIEW_20260927.zip') as b020:
    for b in basis:
        source=b['source']['path']; suffix='outputs/'+source.replace('\\','/').split('/outputs/',1)[1]
        matches=[]
        for label,z in [('guard',guard),('B020',b020)]:
            for n in z.namelist():
                if n==suffix or n.endswith('/'+suffix):
                    if z.read(n)==(R/b['copy']).read_bytes():matches.append({'archive':label,'member':n})
        (prior if matches else unmatched).append({'file':b['copy'],'matches':matches})
    for name,ref in c['baseline_files'].items():
        suffix='outputs/'+ref['path'].split('/outputs/',1)[1]
        n=next(n for n in b020.namelist() if n.endswith('/'+suffix))
        raw=b020.read(n);assert ident(raw)=={k:ref[k] for k in ('bytes','sha256')}
        baseline.append({'file':name,'identity':ident(raw),'archive_member':n})
        if name=='preflight_global.csv':
            records=list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig')))); times={Decimal(x['time_s']) for x in records}
            missing=[x for x in c['requested_times_s'] if Decimal(x) not in times]
            assert not missing and len(times)==987 and len(c['requested_times_s'])==187
            requested={'baseline_times':len(times),'requested_times':len(c['requested_times_s']),'missing':missing}
    # Read existing stop log to check syntax only; it is NOT a successful1198 test.
    logname='outputs/comsol63/.comsol-jobs/08e0fc5d41e147678f3940e98100ec12/batch.log'
    legacy_stop=[s for s in guard.read(logname).decode('utf-8-sig').splitlines() if 'Stop condition fulfilled' in s]

tree=ast.parse((R/'src/trigger_consumer.py').read_bytes())
entry=ast.parse((R/'src/candidate_entry.py').read_bytes())
an=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='analyze')
initial=an.body[0].value
initialkeys=[k.value for k in initial.keys]
try1=next(n for n in an.body if isinstance(n,ast.Try))
assert 'limited_result' not in initialkeys
assert any(isinstance(n,ast.Return) and isinstance(n.value,ast.Name) and n.value.id=='result' for h in try1.handlers for n in ast.walk(h))
entry_an=next(n for n in entry.body if isinstance(n,ast.FunctionDef) and n.name=='analyze')
save_line=next(n.lineno for n in ast.walk(entry_an) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='save')
subs=[n.lineno for n in ast.walk(entry_an) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id=='result' and isinstance(n.slice,ast.Constant) and n.slice.value=='limited_result']
pure_counterexample={'trigger':'INCOMPLETE','sampled_comparison':'INCOMPLETE','errors':[{'axis':'trigger','error':'NATIVE_STOP_REASON'}],'overall':'INCOMPLETE'}
try:pure_counterexample['limited_result']
except KeyError as e:counterexample_error=repr(e)
f={'id':'G1198-N1','source':'src/trigger_consumer.py','initial_keys':initialkeys,
   'early_return_line':next(n.lineno for h in try1.handlers for n in ast.walk(h) if isinstance(n,ast.Return)),
   'entry_save_line':save_line,'entry_limited_result_access_lines':subs,
   'reviewer_owned_schema_example':pure_counterexample,'ordinary_dict_result':counterexample_error,
   'limit':'Dictionary schema demonstration and static call-path analysis only. Candidate not imported or executed.'}
save('FAILURE_SCHEMA_EVIDENCE.json',f)
def numbered(name):
    lines=(R/name).read_text(encoding='utf-8').splitlines()
    return '\n'.join(f'{i}: {line}' for i,line in enumerate(lines,1))+'\n'
for n in ['src/trigger_consumer.py','src/candidate_entry.py','PARENT_COMMAND.ps1']:
    (O/(Path(n).name+'.numbered.txt')).write_text(numbered(n),encoding='utf-8')
save('DATA_STATIC_AUDIT.json',{'candidate_manifest':ident((R/'CODE_MANIFEST.json').read_bytes()),
 'code_files':len(manifest['files']),'transform_operations':len(ops),'inverse_original_bytes_equal':True,
 'one_static_runAll_no_loadCopy_getPreference_argmin':True,'basis_internal_matched':len(basislocal),
 'basis_prior_matched':prior,'basis_prior_unavailable':unmatched,'baseline_six_matches':baseline,
 'requested_times_direct_check':requested,'sender_selected_preservation_count':len(obj('PRESERVATION_BEFORE.json')),
 'sender_preservation_records_equal':True,'native_stop_syntax_prior':legacy_stop,
 'subject_import_or_execution':0,'resource_delivery_final_receipt':'not included in supplied ZIP; final sender delivery closure not independently established'})
print(json.dumps({'status':'DATA_STATIC_CHECKS_COMPLETE','transform_operations':len(ops),'basis_prior_matched':len(prior),
 'basis_prior_unavailable':len(unmatched),'baseline_matches':len(baseline),'error_schema_confirmed_statically':True}))
