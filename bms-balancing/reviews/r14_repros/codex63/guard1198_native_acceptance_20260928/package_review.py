"""Package reviewer artifacts and selected unchanged evidence. No subject execution."""
from pathlib import Path
import hashlib,json,zipfile,stat
O=Path(__file__).resolve().parent;R=O/'received'
Z=Path('C:/Users/Administrator/Downloads/COMSOL63_GUARD1198_NATIVE_RESULT_FOR_REVIEW_20260928.zip')
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def dump(n,v):(O/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
before=json.loads((O/'SOURCE_BEFORE.json').read_bytes())
assert ident(Z.read_bytes())==before['input_zip']
for f in before['extracted']:assert ident((R/f['file']).read_bytes())=={k:f[k] for k in ('bytes','sha256')},f['file']
dump('SOURCE_AFTER_CHECK.json',{'input_zip_unchanged':True,'received_payloads_current_bytes_match':len(before['extracted']),'scope':'Local review input only; no remote/live preservation claim','COMSOL_JVM_solve_calls':0,'received_code_imports_or_executions':0})
selected=['REVIEW_REQUEST_KO.md','candidate/CODE_MANIFEST.json','candidate/CONTRACT.json','candidate/COMMAND_MAP.json','candidate/src/trigger_consumer.py','candidate/src/candidate_entry.py','candidate/PARENT_COMMAND.ps1','run/NATIVE_STATE.json','run/batch.log','run/tables/electrolyte_guard.csv','run/tables/guard_binding.csv','run/tables/axes_runtime_settings.csv','run/POLICY_BEFORE.json','run/CLASS_IDENTITY.json','run/OUTPUT_MPH_IDENTITY.json','run/compile_RETURN.json','run/batch_RETURN.json','run/compile_RESERVATION.json','run/batch_RESERVATION.json','parent/PARENT_START.json','parent/NATIVE_PARENT_RETURN.json','parent/ANALYSIS_PARENT_RETURN.json','parent/PARENT_LOCAL_DECISION.json','parent/FINAL_BOUNDARY.json','local/RESULT_OBSERVATION.json','authorization/guard1198_001.json','authorization/VALIDATION_RELEASE.json','authorization/USER_DECISION.txt','prior/validation_DELIVERY_RECEIPT.json','prior/preexec_DELIVERY_RECEIPT.json','EXCLUDED_FILES.json']
for name in selected:
    p=O/'reference'/'received'/name;p.parent.mkdir(parents=True,exist_ok=True);raw=(R/name).read_bytes()
    if p.exists():assert p.read_bytes()==raw
    else:p.write_bytes(raw)
files=[p for p in O.iterdir() if p.is_file() and p.suffix in ['.md','.json','.py'] and p.name not in ['REVIEW_PACKAGE_MANIFEST.json','DELIVERY_RECEIPT.json']]
files.extend(p for p in (O/'reference').rglob('*') if p.is_file())
assert all((O/n).exists() for n in ['REVIEW_KO.md','CLAUDE_AND_CODEX_REPLY_KO.md','NEXT_30S_PREPARATION_DIRECTIVE_KO.md','DECISION.json','NUMERIC_AUDIT.json','EVIDENCE_AUDIT.json'])
decision=json.loads((O/'DECISION.json').read_bytes());assert decision['native_30s_approved'] is False and not decision['blocking_findings_in_reviewed_scope']
for name in ['REVIEW_KO.md','CLAUDE_AND_CODEX_REPLY_KO.md','NEXT_30S_PREPARATION_DIRECTIVE_KO.md']:
    t=(O/name).read_text(encoding='utf-8');assert '\ufffd' not in t and '30' in t
manifest={'scope':'Recipient review of fixed native evidence; no future execution permission','files':[{'file':p.relative_to(O).as_posix(),**ident(p.read_bytes())} for p in sorted(files)]}
dump('REVIEW_PACKAGE_MANIFEST.json',manifest)
archive=O/'COMSOL63_GUARD1198_NATIVE_ACCEPTANCE_REVIEW_20260928.zip'
assert not archive.exists(),'Refuse to overwrite review delivery'
with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in files+[O/'REVIEW_PACKAGE_MANIFEST.json']:z.write(p,p.relative_to(O).as_posix())
with zipfile.ZipFile(archive) as z:
    ns=z.namelist();assert len(ns)==len(set(x.casefold() for x in ns))
    assert set(ns)=={x['file'] for x in manifest['files']}|{'REVIEW_PACKAGE_MANIFEST.json'}
    for f in manifest['files']:assert ident(z.read(f['file']))=={k:f[k] for k in ('bytes','sha256')}
    assert z.testzip() is None
    for i in z.infolist():assert '..' not in Path(i.filename).parts and ':' not in i.filename and not stat.S_ISLNK(i.external_attr>>16)
receipt={'scope':'Reviewer package generation, not remote native execution or receipt acceptance','zip':{'path':str(archive),**ident(archive.read_bytes())},'payloads':len(files),'manifest':ident((O/'REVIEW_PACKAGE_MANIFEST.json').read_bytes()),'exact_set_size_sha_crc_path_case_link_verified':True,'recipient':None,'native_30s_approved':False,'COMSOL_calls':0,'selected_input_preserved':True}
dump('DELIVERY_RECEIPT.json',receipt);print(json.dumps(receipt,ensure_ascii=False))
