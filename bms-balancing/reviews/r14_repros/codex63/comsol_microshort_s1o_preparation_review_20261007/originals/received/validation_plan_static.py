"""New text-only plan author. It never runs planned test cases or candidates."""
import pathlib,json,hashlib,datetime
R=pathlib.Path(__file__).resolve().parent
groups={
'AUTH':('control.py.inactive.txt','authorize_execution',[
 ('complete future fixture only','AUTHORIZED_ONE_RUN'),('missing approval','SEPARATE_NATIVE_APPROVAL_REQUIRED'),('wrong source bytes','SOURCE_IDENTITY'),
 ('wrong engine pin','ENGINE_OR_DEPENDENCY_IDENTITY'),('wrong validation binding','VALIDATION_ACCEPTANCE_BINDING'),('wrong sigma/run unit','APPROVED_RUN_UNIT_MISMATCH'),
 ('extra solve count','CALL_COUNTS_NOT_APPROVED'),('changed cwd/argv','COMMAND_OR_CWD_MISMATCH'),('existing runtime path','PATH_OR_CONCURRENT_WORK'),
 ('policy changed or elevated','POLICY_OR_PRIVILEGE_MISMATCH'),('prior attempt exists','NO_RETRY_EXISTING_ATTEMPT'),('current native_ready false','OFFLINE_NATIVE_NOT_READY'),
 ('native command null','NATIVE_COMMANDS_UNRESOLVED'),('native paths null','NATIVE_PATHS_UNRESOLVED'),('current policy pin null','CURRENT_POLICY_PIN_UNRESOLVED')]),
'READ':('consumer.py.inactive.txt','read_csv_bytes/timed_rows/coverage/profile_rows',[
 ('valid raw CSV+units then exact profile','RETURN_VALID_ROWS'),('raw SHA mismatch','CSV_IDENTITY'),('unit mismatch','UNIT_EVIDENCE'),('wrong header','CSV_HEADER'),
 ('short row','CSV_WIDTH'),('NaN numeric','NONFINITE'),('empty numeric CSV','EMPTY_CSV'),('duplicate time','DUPLICATE_OR_UNORDERED_TIME'),
 ('required positive time missing','REQUIRED_TIME_MISSING'),('empty/t0-only comparison','EMPTY_OR_ZERO_ONLY_COMPARISON'),('wrong coordinate/domain','COORDINATE_DOMAIN'),('missing profile row','PROFILE_MISSING')]),
'INIT':('consumer.py.inactive.txt','compare_initialization/verify_coefficient_evidence',[
 ('all initial targets exact','PASS'),('exact absolute and relative boundaries','PASS'),('inventory boundary excess','INITIAL_INVENTORY_OR_COMPOSITION'),
 ('first positive sample substituted for0','INITIAL_TIME_NOT_EXACT_ZERO'),('no postconsistency proof','INITIAL_PROVENANCE_OR_TARGETS'),
 ('initial wrong unit','INITIAL_UNIT'),('configured coefficient mismatch','COEFFICIENT_SETTINGS'),('settings only consumption claim','EFFECTIVE_COEFFICIENT_OPEN'),
 ('matched installed mapping fixture','PASS'),('actual coefficient exceeds fixed tolerance','COEFFICIENT_CONSUMPTION'),
 ('both valid individual initialstates butpairdifferenceexceeds','PAIR_INITIAL_STATE_MISMATCH'),('particleaverage nonuniformatoneinitialcoordinate','INITIAL_PROFILE_NONUNIFORM')]),
'POLICY':('consumer.py.inactive.txt','compare_policy/invariants',[
 ('255 exact requests and extra common states','WITHIN_LIMITS_THIS_WINDOW'),('voltage exactly1mV','WITHIN_LIMITS_THIS_WINDOW'),
 ('voltage above1mV valid native','EXCEEDS_LIMITS'),('surface exactly1e-4','WITHIN_LIMITS_THIS_WINDOW'),('surface above1e-4','EXCEEDS_LIMITS'),
 ('individual Li drift above1e-6','LI_DRIFT'),('decomposition above1e-8','VOLTAGE_IDENTITY'),('matched count but wrong coordinate','COORDINATE_DOMAIN')]),
'CHARGE':('consumer.py.inactive.txt','charge_balance',[
 ('resolved balanced series with adequate bound','CONSISTENT'),('nearzero signal includingt0','INCONCLUSIVE'),('unknown quadrature bound','INCONCLUSIVE'),
 ('bound above quarter allocation','INCONCLUSIVE'),('reverse current beyonddeadband','REVERSE_CURRENT'),('RN/RP inconsistency','REACTION_CURRENT_BALANCE'),
 ('I vsA*j mismatch','CURRENT_AREA_CONVERSION'),('reverse Li transfer beyonddeadband','REVERSE_LI_TRANSFER'),('qN-qP exceeds','SOLID_TRANSFER_BALANCE'),
 ('integral residual plus bound exceeds fixedlimit','INTEGRATED_CHARGE_BALANCE'),('reordered integral time','CHARGE_TIME'),('totalLi drift','LI_DRIFT')]),
'PAIRED':('consumer.py.inactive.txt','paired_classification',[
 ('D,S strictly above5E andabsolute thresholds','DISTINGUISHABLE_AT_REST'),('smallD/S smallE','NOT_DISTINGUISHABLE_WITHIN_T'),
 ('large numerical sensitivity masks signal','INCONCLUSIVE'),('D equalspositive threshold','INCONCLUSIVE'),('one Kaxis missing','K_INCOMPLETE'),
 ('same-sigma pairing false','UNMATCHED_K_PAIR'),('2700endpoint missing','PAIRED_ENDPOINT_MISSING')]),
'RESOURCE':('control.py.inactive.txt','assess_resources/advance_stop/execute_once',[
 ('fresh measuredownedjob belowthresholds','CONTINUE_WITHIN_SAMPLED_LIMITS'),('counter absent','STOP_REQUIRED'),('counterNaN','STOP_REQUIRED'),
 ('ownership missing','STOP_REQUIRED'),('doublecount aggregation','STOP_REQUIRED'),('memory exceeds early stop','STOP_REQUIRED'),('sample gap too long','STOP_REQUIRED'),
 ('wall entersstopreserve','STOP_REQUIRED'),('supported cooperative request','WAITING_COOPERATIVE'),('unsupportedwithoutforceapproval','UNRESOLVED'),
 ('unsupportedexplicitforceapproved','FORCE_PENDING'),('cooperativewaitexpires','FORCE_PENDING'),('force succeeded not yetverified','VERIFY_PENDING'),
 ('remaining member after force','UNRESOLVED'),('verified emptyjob androot exit','TERMINATED_VERIFIED'),('authorizationdeny before spy firstsideeffect','OFFLINE_NATIVE_NOT_READY')]),
'PARENT':('Parent.ps1.inactive.txt','S1NativeAxis/S1Fields/S1Decision/S1FinalReturn',[
 ('actual Python valid result +complete native evidence','AWAITING_S1_LIMITED_EXTERNAL_REVIEW'),('actual Python valid numericalexceedance','AWAITING_S1_LIMITED_EXTERNAL_REVIEW'),
 ('actual Python protective stop','PROTECTIVE_STOP_INCOMPLETE'),('childrc wrongtype/nonzero','NATIVE_INVOCATION_OR_FATAL'),('rc0fatal','NATIVE_INVOCATION_OR_FATAL'),
 ('missing nestedfield','INCOMPLETE'),('forgedcomparison summary','COMPARISON_SUMMARY_CONTRADICTION'),('init/configonly success claim','INITIALIZATION_OR_ACTUAL_COEFFICIENT_UNVERIFIED'),
 ('record writer throws','INCOMPLETE'),('postwrite totaloverrun','INCOMPLETE'),('postwrite deliveryoverrun','INCOMPLETE'),('postwrite exact limits andsuccess','AWAITING_S1_LIMITED_EXTERNAL_REVIEW'),
 ('Expected missing positiveend/requestcount','EXPECTED_REQUIRED_FIELDS'),('chargeINCONCLUSIVE producer cannotbe promoted','INCOMPLETE'),
 ('initial_profile evidence missing','EVIDENCE_AXIS_MISSING:initial_profile'),('negative deliveryelapsed fromfuturestart','INCOMPLETE')])}
def identity(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
py=pathlib.Path('C:/Users/BML/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe')
ps=pathlib.Path('C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe')
targets={
 'AUTH':['authorize_execution']*15,
 'READ':['read_csv_bytes']*7+['timed_rows','coverage','coverage','profile_rows','profile_rows'],
 'INIT':['compare_initialization']*6+['verify_coefficient_evidence']*4+['compare_initialization_pair','initial_profile_uniformity'],
 'POLICY':['compare_policy']*5+['invariants','invariants','compare_policy'],
 'CHARGE':['charge_balance']*12,
 'PAIRED':['paired_classification']*7,
 'RESOURCE':['assess_resources']*8+['advance_stop']*7+['execute_once'],
 'PARENT':['S1Decision']*3+['S1NativeAxis']*2+['S1Fields']*3+['S1FinalReturn']*4+['S1Decision','S1Decision','S1Fields','S1FinalReturn']}
cases=[]
for group,(file,functions,items) in groups.items():
 for i,(mutation,expected) in enumerate(items,1):
  cases.append(dict(id=f'{group}{i:02d}',engine='Windows PowerShell5.1' if group=='PARENT' else 'Python',source='candidate/'+file,
    target_functions=[targets[group][i-1]],fixture_mutation=mutation,expected=expected,
    required_reach=targets[group][i-1],reach_rule='Harness must prove this exact real function was reached; exact first reason/status must match. An earlier rejection or arbitrary exception is FAIL.',
    positive_control='Same valid sealed fixture with only stated mutation removed; controls shared rather than counted twice',
    first_unexpected_failure='preserve source seal/rawstdout/stderr/rc/firsterror; do not retry or run following engine'))
fixture=R/'future_validation_fixture_001'
record=dict(kind='S1O_CHANGED_BRANCH_VALIDATION_PROPOSAL_NOT_EXECUTED',approved=False,native_ready=False,
 utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),groups=len(groups),unique_cases=len(cases),inputs=len(cases),
 counts={'Python':sum(c['engine']=='Python' for c in cases),'PowerShell5.1':sum(c['engine']=='Windows PowerShell5.1' for c in cases)},
 engines=[identity(py),identity(ps)],engine_version_process_probe=False,
 budgets_s=dict(harness_seal=600,python=300,powershell=180,preservation_delivery=300,incomplete_closeout=120,overall=1500),
 storage=dict(max_fixture_GiB=1,max_delivery_MiB=50,start_free_GiB=2,profile_rows='at least255*241*2 with derivative mutants; no originalMPH orlargeCSV copies'),
 sessions=dict(Python=1,PowerShell=1,Java_compile=0,JVM=0,COMSOL=0),
 prospective_fixture_root=str(fixture),fixture_created=False,
 commands=[dict(argv=[str(py),'-I',str(fixture/'harness.py')],cwd=str(fixture)),dict(argv=[str(ps),'-NoLogo','-NoProfile','-File',str(fixture/'harness.ps1')],cwd=str(fixture))],
 source_bindings=[identity(R/'candidate'/f) for f in ('consumer.py.inactive.txt','control.py.inactive.txt','Parent.ps1.inactive.txt')],
 source_loading='Future approved harness loads exact content below inactive suffix; AST/extract ranges and terminalguard exclusions sealed BEFORE any import. No production/native adapters; spy inert adapters before candidate load.',
 powershell_extraction='LF normalization only if recorded; exact functions from function start to final closing brace; trailing LF excluded. Bothrawfilesha and extractedspansha/line bounds sealed. Parse/extract only futureapprovedharness, notcurrentexecution.',
 python_ps_connection='Python persists actual analyze results; same raw bytes and SHA consumed by PowerShell. Do not replace producer by hand-written summary.',
 cases=cases,
 unresolved_preseal=['Fixture generator/harness bytes and exact targetfunction for compound function names are not yet authored. Required in approved600sseal BEFORE tests; if cannotfinish stop withouttest.','Current inactive manifest cannot authorize native; positive authorization fixture is fixture-only with structurallycompletechanged fields, neverstored atrealapprovalpaths.','No native API/readback orOSresourceadapter is tested. Implementing those later changesmanifest and requires specific validation.'])
(R/'VALIDATION_PLAN.json').write_text(json.dumps(record,indent=2,ensure_ascii=False),encoding='utf-8')
lines=['# S1-O 변경부 한정 검증안 — 미승인·미실행','',f"새 순수 소비/제어/부모 함수 **{len(groups)}군·{len(cases)}개 고유 사례**만 제안한다. Python {record['counts']['Python']} + PowerShell {record['counts']['PowerShell5.1']}. 사례 수는 assertion 수가 아니다.",'',
'Python 1세션 300초, 일반 Windows PowerShell5.1 NoProfile 1세션 180초. 봉인600 + 보존/전달300 + 미완기록120을 포함해 전체1,500초. fixture≤1GiB, 기록≤50MiB, 시작여유≥2GiB. Java/JVM/COMSOL0. 이 값은 별도 사용자 승인 제안이다.','',
'실제 실행 전 하네스·fixture·추출 범위/해시·엔진 현재 바이트·정확 argv/cwd·각 입력 기대 이유와 도달함수를 봉인한다. 범위를 바꾸지 않고 구체화한다. 계획 JSON의 복합 함수 목록은 하네스에서 실제 도달할 한 경로로 정해야 하며 뜻밖의 앞단 거부를 목표 PASS로 세지 않는다. 받은/생산 코드를 현재 import하지 않았다.','',
'합성의 양성 fixture는 설치본의 사실을 대신하지 않는다. 현재 native_ready=false를 true로 바꾸는 운영승인 파일을 만들지 않는다. native/콘솔/Job/프로세스 진입은 대상 로드 전에 inert로 막는다. 실제 Python analyze 산출물을 PS S1Decision에 그대로 연결한다. 후보 및 이전 source는 수정하지 않는다. 첫 예상 밖 실패/시간/크기 초과에서 후속 엔진을 멈추며 자동 수정·재시험·probe·다른 셸·정책 변경은 없다.','',
'| ID | 실제 대상 | 입력/목표 | 기대 결과 |','|---|---|---|---|']
for c in cases:lines.append(f"| {c['id']} | {' / '.join(c['target_functions'])} | {c['fixture_mutation']} | {c['expected']} |")
lines +=['','## 다음 승인 제안','',
f"> 고정 S1-O source의 {len(groups)}군·{len(cases)}사례 변경부 검증 1건만 승인합니다. 제시된 엔진·세션·1,500초·디스크 한도 안에서 먼저 하네스를 봉인하고 첫 예상 밖 실패에서 멈추세요. 실제 COMSOL·JVM·compile·gate·정책·native 승인/release/runtime/token 생성은 제외합니다. 결과 제출 뒤 멈추세요.",'',
'이 문구는 채택 전 비활성 초안이다. 검증 결과 수용과 설치본 초기화/계수·OS자원 어댑터의 OPEN 종결 뒤에만 새 실행본과 자원 조건을 명시한 S1-P 승인문을 확정할 수 있다. 검증 통과로 P/M/N을 자동 승인하지 않는다. 전체 세부 식별·명령은 VALIDATION_PLAN.json을 따른다.']
(R/'VALIDATION_PLAN_KO.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps(dict(kind=record['kind'],groups=len(groups),cases=len(cases),counts=record['counts'],tests_executed=0)))
