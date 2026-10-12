"""Own metadata/hash/text sealer. Does not import or call candidate code."""
import json,pathlib,hashlib,difflib,time
R=pathlib.Path(__file__).resolve().parents[1];B=R/'basis/prior_preparation'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def put(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def info(p):
 b=p.read_bytes();return {'path':str(p.relative_to(R)).replace('\\','/'),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
plan=read(R/'LIMITED_VALIDATION_PLAN.json');cases=plan['cases'];ids={c['id']:c for c in cases}
assert len(ids)==len(cases)>50
assert len({c['group'] for c in cases})==plan['groups']
assert plan['unique_cases']==len(cases)
for engine,count in plan['counts'].items():assert sum(c['engine']==engine for c in cases)==count
assert all(c['positive_control'] in ids for c in cases)
for id in ['C04-03','C04-04','C04-05']:assert ids[id]['positive_control']=='C04-02'
for id in ['C07-05','C07-06']:assert ids[id]['positive_control']=='C07-04'
assert ids['C08-05']['positive_control']=='C08-04'
assert plan['approved'] is False and plan['usable'] is False and plan['native_ready'] is False
plan['source_byte_bindings']= [info(R/'candidate/resource_connection.py.inactive.txt'),info(R/'candidate/raw_connection.py.inactive.txt'),info(R/'candidate/InstalledReadback.fragment.java.inactive.txt'),info(B/'reference/r1/candidate/control.py.inactive.txt'),info(B/'reference/r1/candidate/consumer.py.inactive.txt'),info(B/'reference/r1/candidate/variants/P0.java.inactive.txt')]
plan['dependency_span_file']=info(R/'FUNCTION_SPANS.json')
plan['execution_status']='NOT_RUN; requires separate user approval and first-test harness/fixture/engine seal'
put(R/'LIMITED_VALIDATION_PLAN.json',plan)
old=(B/'LIMITED_VALIDATION_PLAN.json').read_text();new=(R/'LIMITED_VALIDATION_PLAN.json').read_text()
(R/'LIMITED_VALIDATION_PLAN.diff.txt').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='prior_preparation/LIMITED_VALIDATION_PLAN.json',tofile='OPEN_R1/LIMITED_VALIDATION_PLAN.json')),encoding='utf-8',newline='')
oldmanifest=read(B/'CODE_MANIFEST.json');members=[]
for f in oldmanifest['files']:
 current=info(R/f['path']);members.append({'path':f['path'],'previous_bytes':f['bytes'],'previous_sha256':f['sha256'],'current_bytes':current['bytes'],'current_sha256':current['sha256'],'changed':current['sha256']!=f['sha256']})
assert {x['path'] for x in members if x['changed']}=={'candidate/resource_connection.py.inactive.txt','candidate/resource_connection.py.inactive.txt.diff.txt','LIMITED_VALIDATION_PLAN.json'}
binding={'scope':'OPEN-R1 N1 N2 N3 only; inactive','previous_code_manifest':info(B/'CODE_MANIFEST.json'),'members':members,'source_locations':{'new_candidate':'candidate/','unchanged_accepted_r1':'basis/prior_preparation/reference/r1/','unchanged_historical_74_static_checks':'basis/prior_preparation/STATIC_CHECKS.json','review':'basis/REVIEW.zip'},'runtime_paths_created':False,'native_argv':None,'native_cwd':None,'native_approval_paths':None}
put(R/'REVISION_BINDING.json',binding)
sealed=[R/f['path'] for f in oldmanifest['files']]+[R/'RESOURCE_CLOCK_CONTRACT.json',R/'FUNCTION_SPANS.json',R/'REVISION_BINDING.json']
manifest={'schema':'S1_OPEN_CONNECTION_R1_INACTIVE_V1','approved':False,'usable':False,'native_ready':False,'basis_manifest_sha256':'4ce5c08dbde5153027819b5a651e3995ec82417b4429b9bb0f789082b440f5da','previous_connection_manifest_sha256':sha(B/'CODE_MANIFEST.json'),'self_excluded':True,'files':[info(p) for p in sealed]}
put(R/'CODE_MANIFEST.json',manifest)
static=read(R/'STATIC_CHECKS.json');before=read(R/'evidence/SELECTED_SOURCES_BEFORE.json')
decision={'scope':'STATIC_OFFLINE_CORRECTION_AND_RESEAL_ONLY','status':'OPEN_R1_STATIC_CORRECTION_SUBMITTED_NOT_FUNCTIONALLY_VALIDATED','findings':{'OPEN-R1-N1':{'status':'fixed','basis':'Frozen start context + scalar anchors; raw identity/origin exact binding; elapsed only context; see FUNCTION_SPANS'},'OPEN-R1-N2':{'status':'fixed','basis':'Item type/keys/identity type checked before access, typed rejection before assessor'},'OPEN-R1-N3':{'status':'fixed','basis':'Updated reason/output/reach/positive controls and added N1/N2 cases; not executed'}},'functional_validation':'NOT_RUN','proposed_groups':plan['groups'],'proposed_cases':plan['unique_cases'],'proposed_counts':plan['counts'],'native_ready':False,'approved':False,'usable':False,'overall':'INCOMPLETE','normal_gate':'INCOMPLETE','effective_policy':'UNVERIFIED','actual_cores':'UNVERIFIED','open_items':read(R/'OPEN_CONNECTION_MAP.json')['unresolved'],'candidate_imports_or_function_calls':0,'functional_test_sessions':0,'Java_compile_JVM_COMSOL_calls':0,'OS_collector_process_Job_experiments':0,'actual_approval_release_runtime_token_created':False,'static_checks':{'matched':static['matched'],'count':static['count'],'meaning':'Own data/text/AST/hash checks, not functional tests'},'preservation_items':len(before['files']),'preservation_unique_paths':before['unique_paths'],'code_manifest_sha256':sha(R/'CODE_MANIFEST.json'),'tool_error_disclosure':'See TOOL_OBSERVATIONS; own bootstrap path error, no candidate test failure.','after_submission':'STOP; no proposed validation/native execution'}
put(R/'DECISION.json',decision)
put(R/'evidence/PLAN_SEAL_CHECK.json',{'unique_ids':len(ids),'positive_controls_resolve':True,'N3_positive_links_correct':True,'old_case_ids_preserved':set(c['id'] for c in read(B/'LIMITED_VALIDATION_PLAN.json')['cases'])<=set(ids),'only_three_previous_members_changed':True,'scope':'JSON/hash/text assertions only; no functional cases executed'})
ph=read(R/'PHASE_RECORDS.json');tick=int(time.perf_counter()*10000000);ph['plan_reseal'].update(end_ticks=tick,elapsed_s=(tick-ph['plan_reseal']['start_ticks'])/10000000)
assert ph['plan_reseal']['elapsed_s']<=ph['plan_reseal']['limit_s'],'PLAN_RESEAL_BUDGET'
put(R/'PHASE_RECORDS.json',ph)
print(json.dumps({'code_manifest_sha256':sha(R/'CODE_MANIFEST.json'),'sealed_members':len(sealed),'groups':plan['groups'],'cases':len(cases),'counts':plan['counts'],'plan_reseal_elapsed_s':ph['plan_reseal']['elapsed_s'],'functional_tests':0}))
