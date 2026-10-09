"""Author-owned JSON/diff/identity preparation. Never loads candidate functions."""
from pathlib import Path
import json, hashlib, difflib, zipfile, stat
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT.parents[1]/'outputs/microshort_s1o_r1_20261008'
def ident(p):
    b=p.read_bytes();return {'path':p.as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(name,obj):
    p=ROOT/name;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n')
source_manifest=json.loads((SRC/'CODE_MANIFEST.json').read_bytes())
for e in source_manifest['files']:
    p=SRC/e['path'];b=p.read_bytes()
    assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256']
    dest=ROOT/'reference/r1'/e['path'];dest.parent.mkdir(parents=True,exist_ok=True)
    with dest.open('xb') as f:f.write(b)
with (ROOT/'reference/r1/CODE_MANIFEST.json').open('xb') as f:f.write((SRC/'CODE_MANIFEST.json').read_bytes())
supp=Path('C:/Users/BML/Desktop/COMSOL_MICROSHORT_S1O_R1_004_SUPPLEMENT_REVIEW_20261009.zip')
with zipfile.ZipFile(supp) as z:
    names=z.namelist();assert len(names)==len(set(n.casefold() for n in names))
    m=json.loads(z.read('REVIEW_MANIFEST.json'));assert set(names)=={'REVIEW_MANIFEST.json'}|{e['path'] for e in m['files']}
    for e in z.infolist():
        assert not e.is_dir() and not e.filename.startswith(('/','\\')) and '..' not in e.filename.replace('\\','/').split('/')
        assert stat.S_IFMT(e.external_attr>>16)!=stat.S_IFLNK
    for e in m['files']:
        b=z.read(e['path']);assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256']
    assert z.testzip() is None
save('evidence/INPUT_ARCHIVE_CHECK.json',{'archive':ident(supp),'payload':len(m['files']),'exact_set_size_sha_crc_path_link':'MATCHED','received_code_executed':False})
save('TOOL_OBSERVATIONS.json',{'observations':[
 {'kind':'input_arrival','detail':'Initial exact Desktop lookup absent; after attachment same absolute path matched expected SHA; no network/fallback.'},
 {'kind':'read_only_search_errors','chunks':['5a0a62','04c870','0b7838'],'detail':'Nonexistent guessed documentation/plan paths and unexpanded rg glob operands; later located real local paths. No fixed source identity mismatch, candidate test, or native call. Error output remains in conversation tool records.'},
 {'kind':'no_match_search','detail':'Some rg exit1 means no textual hit, not native failure.'}],
 'functional_test_first_failure':None,'functional_tests_run':0,'native_calls':0})
binding=json.loads((SRC/'contracts/EXECUTION_BINDING.json').read_bytes())
refs={e['path']:e for e in source_manifest['files']}
save('ACCEPTANCE_LINK.json',{'schema':'S1_OPEN_PREPARATION_RECEIPT_LINK','status':'LIMITED_VALIDATION_CLOSED_WITH_DOCUMENTED_SCOPE',
 'basis_manifest_sha256':ident(SRC/'CODE_MANIFEST.json')['sha256'],'source_member_count':21,
 'review_zip':ident(supp),'review_decision_identity':ident(ROOT/'reference/DECISION.json'),
 'new_preparation_authorized_by':'User pasted exact S1 OPEN scope and go-ahead in this chat; attachment arrival is evidence, not independent execution permission.',
 'historical_status_strings_unchanged':True,'native_ready':False,'approved':False,'usable':False,
 'past_614_480_scope':'Recorded snapshot only; subsequent check-write/tool-return total unobserved; not complete end-to-end budget PASS.'})
rawmap=[
 {'id':'stored_grid','producer':'s1OpenStoredGrid / EvalGlobal t innerinput=all','unit':'s','domain':'solution','consumer':'native.stored_times_s / Parent.Native.stored_times_s','status':'HELPER_UNCALLED; semantic native parser OPEN'},
 {'id':'initial','producer':'CDI type/properties + Time consistent + actual exact t0 values/profile','consumer':'readbacks.initial + initial_targets','status':'POST_CONSISTENCY_PROVENANCE_OPEN'},
 {'id':'coefficients','producer':'pcb1/pce1/pce2 properties + recursive/all FeatureInfo + actual evaluation','consumer':'readbacks.configured/consumed/coefficient_expected','status':'INSTALLED_VARIABLES_AND_VALUES_OPEN','installed_symbol':None,'mapping_sha256':None},
 {'id':'charge','producer':'preflight_global.csv + s1_leakage.csv + native complete grid','consumer':'data.charge + readbacks.charge_provenance','status':'BYTE_AND_NUMERIC_PROJECTION_CANDIDATE_ONLY'},
 {'id':'quadrature','producer':'independently reviewed uniform-all-prefix j/RN/-RP bound raw','consumer':'quadrature_bound_C_m2 + quadrature_provenance','status':'METHOD_OPEN','current_bound_C_m2':None},
 {'id':'request_guard','producer':'full configured vector + native reason/operator/guard last two actual states','consumer':'comparison_spec.safe_end_s and common_requests; native.guard_pair','status':'PREFIX_CANDIDATE; native reason/guard proof OPEN'},
 {'id':'os','producer':'held private Job/member handles -> counter snapshot -> projection','consumer':'control.assess_resources then advance_stop; Parent final boundary','status':'PURE_PROJECTION_ONLY; OS provider/cap/stop OPEN'}]
save('OPEN_CONNECTION_MAP.json',{'native_ready':False,'basis':ident(SRC/'CODE_MANIFEST.json'),'items':rawmap,
 'unresolved':['installed_post_consistency_t0','installed_effective_coefficient_mapping','raw_native_evidence_adapter','OS_resource_ownership_stop_adapters'],
 'equation_reference':'evidence/DOC_08.txt:101-143','time_reference':'evidence/DOC_02.txt:consistent and evidence/LOCAL_comsol_ref_solver.36.136.txt:137-143',
 'exact_native_argv':None,'exact_native_cwd':None,'new_native_paths':None,'parent_schema_publication':'OPEN: R1 manifest schema differs from unchanged V1 authorize_execution expected schema; do not normalize silently'})
osrows=[
 ('private Job/root','CreateJobObjectW/CreateProcessW/AssignProcessToJobObject/ResumeThread','winjob.py:30-41,124-132,190-208','SOURCE_DECLARATIONS_AND_PREVIOUS_PATH','member handles for all descendants, PID+creation, two membership bookends'),
 ('root identity','GetProcessTimes','winjob.py:38,203-204','SOURCE_DECLARATION','all-member creation FILETIME collection not implemented'),
 ('membership','QueryInformationJobObject class3','winjob.py:74-80','SOURCE_DECLARATION','capacity/race/error handling; no empty default'),
 ('RSS','WorkingSetSize via reviewed process counter API','not present in existing source','LOCAL_PRIMARY_API_ABI_OPEN','unique member totals, shared pages may count twice'),
 ('Job current commit','exact information class/counter unresolved','existing EXT PeakJobMemoryUsed is peak, not current','OPEN','not member sum and not peak replacement'),
 ('Job enforced commit cap','SetInformationJobObject + query/readback mapping unresolved','winjob.py:193-196 only sets kill-on-close','NOT_IMPLEMENTED','12GiB proposal unchanged; setting/readback failure blocks resume'),
 ('host commit','CommitLimit/CommitTotal/PageSize API candidate; exact primary doc needed','legacy GlobalMemoryStatusEx availPage unused for this meaning','OPEN','host available physical RAM is separate'),
 ('host RAM/disk','GlobalMemoryStatusEx availPhys/shutil.disk_usage','winjob.py:67-73','START_ONLY_SOURCE_PATH','periodic sampling/provider unimplemented'),
 ('owned output','bounded file tree metadata walk','new projection requires COMPLETE_NO_REPARSE_NO_UNKNOWN_FILE','COLLECTOR_OPEN','include staged/prefs/log/CSV/MPH/temp/evidence; original files excluded; no deletion'),
 ('cooperative stop','none verified','no matching stop/cancel callable confirmed in inspected SolverSequence/legacy source','UNVERIFIED','not inferred from getUBlock stop index or runFromTo fstopname'),
 ('forced termination','TerminateJobObject/kill-on-close','winjob.py:36,208-end','SOURCE_PATH_FORCE_ONLY','not graceful; separate decision if no cooperative API'),
 ('final boundary','Parent.S1FinalReturn','Parent.ps1.inactive.txt:339-end','UNCHANGED_ACCEPTED_PURE_LOGIC','actual child rc/clock/writer provider and external return capture remain needed')]
save('OS_API_MATRIX.json',{'observed_process_experiments':0,'new_os_calls_executed':0,'primary_windows_sdk_path_observed_absent':'C:/Program Files (x86)/Windows Kits/10/Include',
 'rows':[dict(zip(['metric','api_or_candidate','local_source','evidence_grade','remaining'],r)) for r in osrows],
 'resource_contract_unchanged':refs['contracts/RESOURCE_CONTRACT.json'],
 'force_only_approved':False,'hard_cap_removal_approved':False})
cases=[]
def group(g,fn,items,engine='Python'):
 for i,(label,expect,setup) in enumerate(items,1):
  cases.append({'id':f'{g}-{i:02d}','group':g,'engine':engine,'target_function':fn,
                'case':label,'expected_reason_or_result':expect,'fixture_rule':setup,
                'positive_control':f'{g}-01','reached_function_required':fn.split(' -> ')[-1],
                'unexpected_exception_is_pass':False})
group('C01','numeric_table',[
 ('valid bytes/units','parsed Decimal rows','small exact producer header plus data; identities computed before first test'),
 ('changed bytes','RAW_IDENTITY','hold expected hash; mutate one byte'),
 ('header mismatch','TABLE_HEADER_OR_UNITS','rehash fixture; change header only'),
 ('unit mismatch','TABLE_HEADER_OR_UNITS','raw units array differs; valid data'),
 ('ragged row','TABLE_WIDTH','rehash raw with extra cell'),
 ('NaN','DECIMAL_NONFINITE','rehash NaN cell; other fields valid'),
 ('header only','EMPTY_TABLE','nonzero header bytes; correct identity')])
group('C02','charge_projection',[
 ('normal full grid','exact eight fields','native/global/leak same >=3 times and duplicate RN/RP/j equal'),
 ('leak omits stored time','FULL_GRID_MISMATCH','native/global full; leak remove middle only'),
 ('duplicate current differs','DUPLICATE_CURRENT_DISAGREEMENT','valid grids; alter RN on leakage row'),
 ('repeated time','GRID_ORDER_OR_RANGE','repeat time in all three grids to reach order guard'),
 ('Double time transport','DECIMAL_TRANSPORT','native_grid one Python float; numeric tables valid'),
 ('time beyond end','GRID_ORDER_OR_RANGE','same full grids extend beyond unchanged configured end')])
group('C03','request_prefix',[
 ('normal all requests','normal complete prefix','fixed end and >1 request; full stored grid'),
 ('protective nonrequest stop','prefix ends <= t_minus; pair retained','last two states not both requested; stop strictly before end'),
 ('missing scheduled prefix','REQUEST_PREFIX_MISSING','remove request time from native but keep other times and endpoint'),
 ('t0 only safe prefix','PREFIX_EMPTY_OR_ZERO_ONLY','guard pair before first positive request; valid grids'),
 ('pair not last two','PROTECTIVE_PAIR','valid ordered times but pair t_minus not second last')])
group('C04','quadrature_projection',[
 ('absent bound','INCONCLUSIVE_NO_CERTIFIED_BOUND','proof=None; no bound promoted'),
 ('reviewed method and raw','BOUND_BYTES_LINKED_REQUIRES_METHOD_ACCEPTANCE','inert accepted method seal plus matching JSON payload/identity/grid/all prefixes'),
 ('unreviewed method','QUADRATURE_METHOD_OPEN','no accepted method hash'),
 ('wrong grid','QUADRATURE_GRID_OR_SCOPE','raw and proof both wrong grid, identities recomputed; avoid payload mismatch'),
 ('caller forges bound','QUADRATURE_PAYLOAD_BINDING','valid raw identity; caller proof.bound_C_m2 differs from raw')])
group('C05','require_installed_mapping / consumer_connection',[
 ('accepted inert seam','actual consumer.analyze reached; preserve its exact result','inert provider verifies supplied same run/manifest; real unchanged consumer with accepted fixture data, no native'),
 ('default provider','INSTALLED_PROOF_PROVIDER_OPEN','provider omitted; consumer not reached'),
 ('wrong provider run','INSTALLED_PROOF_REJECTED','inert proof uses wrong run; consumer not reached'),
 ('mapping absent','INSTALLED_MAPPING_OPEN','no reviewed mapping seal'),
 ('mapping dictionary mismatch','MAPPING_OBJECT_BINDING','raw mapping valid SHA; separately supplied dict modified'),
 ('mapping not observed','INSTALLED_OBSERVATION_OPEN','correct byte-bound JSON but status OPEN'),
 ('byte-bound inert mapping positive','same mapping returned','canonical raw JSON with exact inert reviewed hash, INDEPENDENTLY_ACCEPTED fixture-only status, engine/source identities; never production mapping')])
group('C06','project_owned_sample',[
 ('complete sampled transaction','sample and ownership projected','exact member PID+creation, root included once, current Job commit mapping pin nonnull'),
 ('root exited children live','sum children only','held root signaled true; member list includes owned children, not root'),
 ('duplicate member','MEMBER_DUPLICATE','repeat identical PID+creation on both membership bookends'),
 ('membership churn','MEMBERSHIP_CHURN_OR_EMPTY','change after member list'),
 ('commit mapping missing','JOB_COMMIT_MAPPING_OPEN','anchors accepted_commit_mapping_sha256=None'),
 ('missing counter','COUNTER_MISSING:volume_free_bytes','other fields valid; volume counter None'),
 ('reparse output','OUTPUT_SCOPE','output_walk_status not complete'),
 ('clock reverses','CLOCK_ORDER','sample end before start; other times finite')])
group('C07','resource_decision / stop_action_plan',[
 ('within limits','CONTINUE_WITHIN_SAMPLED_LIMITS','project C06 positive into actual control.assess_resources with unchanged contract'),
 ('RSS threshold exceeded','RESOURCE_THRESHOLD:job_rss_bytes','complete snapshot; RSS one byte above existing early threshold'),
 ('projection query fails','STOP_REQUIRED / OS_QUERY_FAILURE','raw.query_success=false; no zero substitution'),
 ('owned force plan','FORCED + execute_now=false','actual control.advance_stop STOP_REQUESTED, verified ownership, explicitly force-only inert permission; FORCE_OWNED_JOB_ONCE action; no OS call'),
 ('unsupported stop','STOP_METHOD_NOT_APPROVED','actual STOP_REQUESTED no verified cooperative/no force-only permission'),
 ('ownership lost','NO_KILL_WITHOUT_OWNERSHIP','event.ownership_verified=false; no OS calls')])
group('C08','s1OpenProperties / s1OpenConfiguredReadback / s1OpenStoredGrid',[
 ('typed property output','exact type/key/value table','extract actual new helpers; minimal PropFeature/Model stubs and old readSetting/table dependencies'),
 ('unknown value type','original IllegalArgumentException propagates','actual old readSetting default; no empty successful output'),
 ('recursive equation calls','3 features x 4 kinds, recursive/all','record actual helper call arguments on inert FeatureInfo'),
 ('stored zero semantics','STORED_ZERO_POST_CONSISTENCY_PROOF_OPEN','inert evaluate returns exact [0,positive,end]; no t0 proof tag generated'),
 ('nonzero first time','original TIME_ORIGIN propagates','use actual existing checkShape via inert evaluate dependency; do not reimplement shape check'),
 ('readback exception','first raw exception propagates','property getter throws fixed sentinel; later equation calls not reached')],engine='Java_helper')
engine_names={'Python':binding['engine_pins'][0]['path']}
# Select the Python pin by filename, independent of list order.
engine_names['Python']=next(e['path'] for e in binding['engine_pins'] if Path(e['path']).name.lower()=='python.exe')
oldcommands=json.loads((ROOT.parents[1]/'outputs/normal30_limited_validation_R1_20260928/COMMANDS.json').read_bytes())
engine_names['Java_compile']=oldcommands['Java_compile']['argv'][0]
engine_names['Java_helper']=oldcommands['Java_stub']['argv'][0]
engines={k:ident(Path(v)) for k,v in engine_names.items()}
fixture=ROOT/'proposed_changed_validation_001'
plan={'schema':'S1_OPEN_CHANGED_BRANCH_PLAN_V1','approved':False,'usable':False,'native_ready':False,
 'status':'PROPOSAL_ONLY_NOT_EXECUTED','groups':8,'unique_cases':len(cases),
 'counts':{k:sum(c['engine']==k for c in cases) for k in ('Python','Java_helper')},
 'engine_pins_current_file_reads_no_version_invocation':engines,
 'engine_selection_source':ident(ROOT.parents[1]/'outputs/normal30_limited_validation_R1_20260928/COMMANDS.json'),
 'fixture_proposed_only_not_created':fixture.as_posix(),
 'commands':{
  'Python':{'argv':[engines['Python']['path'],'-I','-S','-B','-X','utf8',(fixture/'run_python.py').as_posix()],'cwd':fixture.as_posix(),'max_sessions':1,'timeout_s':180},
  'Java_compile':{'argv':[engines['Java_compile']['path'],'-proc:none','-d',(fixture/'classes').as_posix(),(fixture/'OpenReadbackHarness.java').as_posix()],'cwd':fixture.as_posix(),'max_sessions':1,'timeout_s':90},
  'Java_helper':{'argv':[engines['Java_helper']['path'],'-cp',(fixture/'classes').as_posix(),'OpenReadbackHarness'],'cwd':fixture.as_posix(),'max_sessions':1,'timeout_s':60}},
 'budget_proposal_s':{'harness_seal':600,'Python':180,'Java_compile':90,'Java_helper':60,'preservation_delivery':300,'incomplete_closeout':120,'total':1350},
 'no_PS_session_reason':'No Parent changes or new Parent projection; existing PS acceptance reused. Future native->Parent adapter still OPEN and requires its own changed-path validation when implemented.',
 'requirements':['User separate approval before harness/test','Freeze exact source/engine/harness/input byte hashes and expected reasons/reach before first test','Block native/console/Job/file side effects before candidate load','Only exact new Java helpers plus necessary old pure dependencies; no COMSOL jars/full model','Actual consumer/control functions for integration; no lookalike replacement','Expected rejection is not unexpected failure; any unrelated earlier error is failure','First unexpected failure/time budget stop, preserve stderr/rc and unexecuted IDs; no edits/retry/probe/fallback','All results keep native_ready=false; installed/OS proof cannot come from fixtures'],
 'cases':cases,'source_pins':[ident(p) for p in sorted((ROOT/'candidate').glob('*.inactive.txt'))],
 'existing_core_pins':[refs[x] for x in ('candidate/consumer.py.inactive.txt','candidate/control.py.inactive.txt','candidate/Parent.ps1.inactive.txt')]}
save('LIMITED_VALIDATION_PLAN.json',plan)
for name in ('raw_connection.py.inactive.txt','resource_connection.py.inactive.txt'):
 text=(ROOT/'candidate'/name).read_text(encoding='utf-8')
 diff=''.join(difflib.unified_diff([],text.splitlines(True),fromfile='/dev/null',tofile='candidate/'+name))
 with (ROOT/'candidate'/(name+'.diff.txt')).open('x',encoding='utf-8',newline='') as f:f.write(diff)
save('NATIVE_CONNECTION_STATUS.json',{'native_ready':False,'approved':False,'usable':False,'actual_native_argv':None,'actual_native_cwd':None,
 'installed_provider':'UNAVAILABLE_DEFAULT','os_provider':'UNAVAILABLE_DEFAULT','actual_approval_paths_created':False,
 'previous_core_files_modified':0,'future_entrypoint_publication':'SEPARATE_IMPLEMENTATION_AND_VALIDATION_REQUIRED',
 'parent_schema_issue':'R1 manifest vs authorize_execution V1 gate unresolved for future publication; no silent rewrite',
 'quadrature_bound':None,'cooperative_stop':'UNVERIFIED','job_commit_hard_cap':'NOT_IMPLEMENTED',
 'functional_test_calls_this_task':0,'COMSOL_JVM_compile_solve_calls_this_task':0})
save('FIXED_IDENTITIES.json',{'accepted_manifest':ident(SRC/'CODE_MANIFEST.json'),'accepted_parent':ident(SRC/'candidate/Parent.ps1.inactive.txt'),
 'incoming_review':ident(supp),'approval_scope_document':ident(ROOT/'reference/NEXT_APPROVAL_DRAFT_KO.md'),
 'proposal_engines':engines,'before_selection_count':len(json.loads((ROOT/'evidence/SELECTED_SOURCES_BEFORE.json').read_bytes()))})
print(json.dumps({'new_validation_plan_only':True,'groups':8,'cases':len(cases),'engine_counts':plan['counts'],'functional_tests_run':0}))
