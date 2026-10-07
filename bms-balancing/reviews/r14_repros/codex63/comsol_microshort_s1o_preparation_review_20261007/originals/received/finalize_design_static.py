"""New static metadata author; no candidate import/call or synthetic cases."""
import pathlib,json,hashlib,datetime,ast
R=pathlib.Path(__file__).resolve().parent
def read(n):return json.loads((R/n).read_bytes())
def put(n,v):(R/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def identity(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
plan=read('VALIDATION_PLAN.json')
binding=read('contracts/EXECUTION_BINDING.json')
binding['current_validation_engine_observation']={'source':'VALIDATION_PLAN.json','scope':'Python and PS executable bytes read for future validation only; no engine version/native probe','engines':plan['engines']}
binding['engine_pin_scope']+=' Current validation-only Python/PS byte identities are separately attached below; native current COMSOL and policy observations remain OPEN.'
binding['open_blockers']=[x.replace('PowerShell size and all current engine/dependency/policy identities not re-observed','Native current COMSOL engine/dependency/policy identities not re-observed; validation-only PS/Python byte observations do not clear this blocker') for x in binding['open_blockers']]
put('contracts/EXECUTION_BINDING.json',binding)
link={
 'kind':'OFFLINE_SOURCE_TO_CONTRACT_LINK_MAP','functional_tests':0,
 'consumer_inputs':{
  'read_csv_bytes':'raw bytes identity+exactheader+configured/evaluatedunit record; normalized Decimal rows',
  'compare_initialization':'INITIALIZATION.consumer_projection.targets; postconsistency exact0 proof',
  'initial_profile_uniformity':'validated profile_rows geometry,241each,t0; xN/xP fromINITIALIZATION',
  'compare_initialization_pair':'run cohort same registered concentration andinventory; required beforepairedclassification',
  'verify_coefficient_evidence':'COEFFICIENT_READBACK adapter_projection OPEN; no installedvariablemapping invented',
  'charge_balance':'CHARGE_BALANCE time_s/j/RN/RP/I/LiN/LiP/LiE; rawboundprovenance required in analyze',
  'compare_policy':'POLICY_VARIANTS selectedvariant requests; exactlyregistered255grid plus separate fullintersection',
  'paired_classification':'K_DESIGN futurefrozenK hashes projectedintoexpected_k_settings; nativecohortassemblerOPEN',
  'analyze':'normalizednativeproof/readbacks/data/safe_end from future immutable rawadapter; adapter OPEN'},
 'parent':'S1Fields/S1Decision consume actual analyze output; S1FinalReturn uses inertwriter/clock in futurevalidation',
 'control':'authorize_execution before adapter firstsideeffect; execute_once default adapter raises; native_readyfalse',
 'not_provided':['installed COMSOL readback mapping','native raw log/schema normalization adapter','OSresource sampler/hardJobcommit adapter','executable native commands/approval paths/currentprefs','future validation harness/fixtures'],
 'precision':'consumer Decimal50; parent double schema/check projection is not an independent arbitraryprecisionrecalculation. Futureboundaryfixtures must examine conversion and rejectcontradictions; no claimexactdecimalprooffromPS.'}
put('SOURCE_CONTRACT_LINKS.json',link)
paths=sorted([p for p in (R/'candidate').rglob('*') if p.is_file()]+list((R/'contracts').glob('*.json'))+[R/'VALIDATION_PLAN.json',R/'SOURCE_CONTRACT_LINKS.json'])
manifest=dict(schema='S1O_CODE_MANIFEST_V1',approved=False,usable=False,native_ready=False,status='OFFLINE_SOURCE_CONTRACTS_UNTESTED_WITH_OPEN_NATIVE_ADAPTERS',self_excluded=True,files=[identity(p) for p in paths])
put('CODE_MANIFEST.json',manifest)
sha=hashlib.sha256((R/'CODE_MANIFEST.json').read_bytes()).hexdigest()
decision=dict(s1o_status='PREPARED_WITH_EXPLICIT_OPEN_NATIVE_BLOCKERS',source_written=True,functional_validation='NOT_EXECUTED',native_ready=False,approved=False,usable=False,code_manifest_sha256=sha,
 items=[{'id':1,'status':'partial','artifact':'contracts/INITIALIZATION.json','open':'installed CDI type and postconsistency exactt0 extraction'},
 {'id':2,'status':'partial','artifact':'contracts/COEFFICIENT_READBACK.json','open':'installed coefficient/equation mapping and actualconsumption'},
 {'id':3,'status':'partial','artifact':'contracts/EXECUTION_BINDING.json','open':'native/readback/ownedruntime adapter, exactnativeargv/path/prefs'},
 {'id':4,'status':'done','artifact':'contracts/POLICY_VARIANTS.json','meaning':'offline variants/diff/consumer; untested'},
 {'id':5,'status':'done','artifact':'contracts/K_DESIGN.json','meaning':'unapproved fixeddesign/count/reduction rules'},
 {'id':6,'status':'done','artifact':'contracts/CHARGE_BALANCE.json','meaning':'offline thresholds/units/deadband; actualquadratureboundOPEN'},
 {'id':7,'status':'partial','artifact':'contracts/RESOURCE_CONTRACT.json','open':'OSsampler/Jobhardlimit/stopadapter andsupportedcooperative method'},
 {'id':8,'status':'done','artifact':'contracts/COST_MODEL.json','meaning':'unapproved pilotmeasurement andcostformulas; nofinite-sigma observedcost'}],
 reviewer_execution={'COMSOL':0,'JVM':0,'compile':0,'solve':0,'native_gate':0,'received_or_candidate_program_import_execution':0,'synthetic_validation_cases':0,'policy_changes':0,'MPH_access_or_change':0,'new_static_text_hash_arithmetic_and_packaging_scripts':'yes; source/outputprovided'},
 next_validation={'groups':plan['groups'],'cases':plan['unique_cases'],'counts':plan['counts'],'proposed_overall_limit_s':1500,'approved':False},
 offline_time_usage={'origin':'START.json','writing':'WRITING_CLOSEOUT.json','static':'STATIC_PHASE_CLOSEOUT.json','final_phase_summaries':'TIMING.json','package_end_snapshot':'DELIVERY_RECEIPT.json outsideZIP; do notaddtoolwalltoelapsed','pre_origin_intake':'separatelydisclosed; totalendtoendbeforeoriginnotmeasured'},
 legacy={'overall_normal_gate':'INCOMPLETE','effective_policy':'UNVERIFIED','actual_cores':'UNVERIFIED','native_acceptances_reopened':False,'receipt_recipient_unchanged':True},
 stop='Submit offline artifacts. Do not execute proposed validation or P/M/N without separate approval; current native-ready false has unresolved implementation prerequisites.')
put('DECISION.json',decision)
put('STATIC_TOOL_RETURNS.json',{'source':'assistant-preserved toolresults, not independent OS audit','records':[
 {'chunk':'bafcb3','rc':0,'wall_seconds':6.2901304,'kind':'new intake script','payload':38,'entries':39},
 {'chunk':'a2f4e0','rc':0,'wall_seconds':6.2309766,'kind':'selectedoriginalread/copy','files':10},
 {'chunk':'e0be9f','rc':0,'wall_seconds':6.216782,'kind':'inactive literalvariants','reverse_equal':True},
 {'chunk':'04b177','rc':0,'wall_seconds':6.1951533,'kind':'planwriter only','groups':8,'cases':98},
 {'chunk':'f8e273','rc':0,'wall_seconds':6.721909,'kind':'bundledPSparser dataread','errors':[]},
 {'chunk':'3a3906','rc':1,'wall_seconds':6.2442399,'kind':'newstatictoolpathkeyerror','full_error':'audit_history/FIRST_STATIC_ERROR.json'},
 {'chunk':'8a8ab2','rc':0,'wall_seconds':6.2275637,'kind':'correctednewstatictool','static_checks':156}],
 'agent_records':'physics/POLICY ownstaticscripts and outputs included underanalysis/root; snapshotsbeforefinalintegrationnotfinalcodepins'})
print(json.dumps(dict(code_files=len(paths),code_manifest_sha256=sha,native_ready=False,done=4,partial=4,validation_cases=plan['unique_cases'])))
