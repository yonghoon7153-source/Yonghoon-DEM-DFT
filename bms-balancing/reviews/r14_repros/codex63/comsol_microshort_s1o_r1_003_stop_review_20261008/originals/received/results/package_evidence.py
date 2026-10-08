"""Data-only closeout; never imports candidates or runs test engines."""
import csv, hashlib, io, json, time, zipfile
from pathlib import Path
R=Path(__file__).resolve().parents[1]
S=R.parent
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(b): return hashlib.sha256(b).hexdigest()
def identity(p):
 p=Path(p); b=p.read_bytes(); return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
def write(name,obj):
 with (R/name).open('x',encoding='utf-8',newline='\n') as f: json.dump(obj,f,ensure_ascii=False,indent=2)
origin=read(R/'ORIGIN.json'); delivery=read(R/'DELIVERY_ORIGIN.json')
def elapsed(o): return time.perf_counter()-o['monotonic_ticks']/o['frequency']
def check_budget():
 if elapsed(origin)>1740 or elapsed(delivery)>280: raise RuntimeError('CLOSEOUT_RESERVE_LIMIT')
check_budget()
plan=read(R/'VALIDATION_PLAN_CORRECTED.json'); first=read(R/'FIRST_SEAL.json')
py=read(R/'results/PYTHON_RESULTS.json'); ps=read(R/'results/ps_first_failure.json')
py_session=read(R/'results/PYTHON_SESSION.json'); ps_session=read(R/'results/POWERSHELL_SESSION.json')
assert py['status']=='PASS' and py['count']==99 and py_session['rc']==0
assert ps['current_case']=='PARENT_R113' and ps['case_count']==28 and ps_session['rc']==1
assert ps['first_error']=='HARNESS_FIXTURE_OR_ASSERTION:R113_DOUBLE_AFTER_JSON_PARSE'
preserved=[]
for item in first['files']:
 now=identity(item['path']); same=now['bytes']==item['bytes'] and now['sha256']==item['sha256']
 preserved.append({'before':item,'after':now,'match':same})
write('SELECTED_SOURCES_AFTER.json',{'scope':'First-seal file set only; not whole PC','all_match':all(x['match'] for x in preserved),'items':preserved})
if not all(x['match'] for x in preserved): raise RuntimeError('FROZEN_FILE_CHANGED')
pymap={x['id']:x for x in py['cases']}; psmap={x['id']:x for x in ps['cases']}
rows=[]
for c in plan['cases']:
 cid=c['id']; x=pymap.get(cid) or psmap.get(cid)
 if x:
  status=x.get('status',x.get('result')); observed=x['observed']; stage=x.get('observed_stage')
  reached=x.get('reached_functions',x.get('target_reach',[])); reason=x.get('error')
 elif cid==ps['current_case']:
  status='HARNESS_FAILURE_BEFORE_TARGET'; observed=ps['first_error']; stage='fixture JSON transport type assertion'; reached=[]; reason=ps['first_error']
 else: status='NOT_RUN_AFTER_FIRST_FAILURE'; observed=None; stage=None; reached=[]; reason='First failure stop'
 rows.append({'id':cid,'input_id':c['input_id'],'engine':c['engine'],'expected':c['expected'],'expected_stage':c.get('expected_stage',c.get('required_reach')),'observed':observed,'observed_stage':stage,'reached_functions':reached,'positive_control_case_id':c['positive_control_case_id'],'status':status,'reason':reason})
assert len(rows)==130 and len({x['input_id'] for x in rows})==130
counts={k:sum(x['status']==k for x in rows) for k in ('PASS','HARNESS_FAILURE_BEFORE_TARGET','NOT_RUN_AFTER_FIRST_FAILURE')}
assert counts=={'PASS':127,'HARNESS_FAILURE_BEFORE_TARGET':1,'NOT_RUN_AFTER_FIRST_FAILURE':2}
write('CASE_RESULT_MAP.json',{'counts':counts,'cases':rows,'static_N4_separate':True,'no_assertion_double_count':True})
with (R/'CASE_RESULT_MAP.csv').open('x',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader()
 for row in rows:
  w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in row.items()})
write('ENGINE_TOOL_RETURNS.json',{'source':'Later transcription of actual exec tool returns; not raw OS audit','python':{'completion_chunk':'596519','tool_exit_code':0,'tool_wait_wall_seconds':0.0000152,'engine_elapsed_s':169.2741394,'post_session_overall_snapshot_s':576.5540182,'within_limits':True},'powershell':{'completion_chunk':'003995','tool_exit_code':1,'tool_wait_wall_seconds':0.0000142,'engine_elapsed_s':30.3085736,'post_session_overall_snapshot_s':666.6853731,'within_limits':False,'reason':'EARLIER_ENGINE_FAILURE_PRESERVED'},'note':'Engine within_limits combines success and time conditions. PowerShell false is caused by rc1;30.309s is below300s. Poll wall times are not whole process time.'})
write('VALIDATION_CLOSEOUT.json',{'status':'INCOMPLETE_FIRST_UNEXPECTED_HARNESS_FAILURE','counts':counts,'python_session':py_session,'powershell_session':ps_session,'first_failure':ps['first_error'],'unexecuted':[x['id'] for x in rows if x['status']=='NOT_RUN_AFTER_FIRST_FAILURE'],'native_ready':False,'overall':'INCOMPLETE','normal_gate':'INCOMPLETE','production_modified':False,'functional_sessions':{'python':1,'Windows_PowerShell_5_1':1},'preparation_data_helpers':'Separate data-only Python preparation calls; not candidate validation sessions','prohibited_actual_calls':{'COMSOL':0,'JVM':0,'Java_compile':0,'native':0,'user_input_gate':0,'Job_control':0,'policy_changes':0},'no_fix_no_retest_after_failure':True,'fixture_failure_is_not_production_defect_proof':True,'overall_snapshot_s':elapsed(origin),'delivery_snapshot_s':elapsed(delivery),'snapshot_boundary':'before package and receipt writes'})
report='''# S1O-R1 R1_003 한정 검증 중지 결과

이번 결과는 **INCOMPLETE**입니다. Python 99사례는 전부 통과했고, PowerShell은 앞선 28사례 통과 후 PARENT_R113의 시험 입력 형식 확인에서 멈췄습니다. 127 PASS / 1 하네스 실패 / 2 미실행이며 전체 130사례 통과가 아닙니다.

첫 오류는 `HARNESS_FIXTURE_OR_ASSERTION:R113_DOUBLE_AFTER_JSON_PARSE`입니다. PowerShell 하네스 133행의 JSON 파싱 후 Double 형식 assertion에서 중단됐습니다. 해당 사례의 목표 생산 판정 함수에 도달하기 전이므로 생산 코드 결함이나 해당 음성 사례 PASS로 분류하지 않습니다. 실제 파싱 형식은 실패 기록에 없으므로 추측해 확정하지 않습니다. PARENT_R114·PARENT_R115는 실행하지 않았습니다.

사전 봉인 390.058414/720초, Python 실제 세션 169.274139/420초·rc0, PowerShell 실제 세션 30.308574/300초·rc1입니다. PowerShell 반환의 within_limits=false는 성공/예산 결합 판정이며 시간 상한 초과라는 뜻이 아닙니다. 최종 전달 시간은 ZIP 밖 DELIVERY_RECEIPT와 반환 후속 전사를 함께 확인해야 합니다.

사용자가 R1_003 새 위치를 승인한 뒤 새 원점으로 수행했습니다. 앞선 R1_001/R1_002 중지 기록은 보존했으며 재사용한 준비 자료를 이번에 새 기능 시험한 것으로 부풀리지 않았습니다. 이번 첫 시험 전에 INIT02 경계 입력을 target0.001/observed0.001000001로 정리하여 절대1e-9·상대1e-6 허용치를 유지했습니다. 생산 파일은 변경하지 않았습니다.

FIRST_SEAL은 생산 소스·엔진·130 입력 명세·하네스·추출 범위·명령을 결속합니다. Python 실제 분석 결과 및 context 10개를 PS_PRODUCER_SEAL로 추가 봉인한 뒤 PS가 읽었습니다. 원문 stdout/stderr, 외부 rc, 실패 스택, 사례별 이유·도달·미실행 목록과 선택 파일 전후 해시를 동봉합니다. 정적 N4 확인 1개는 기능 사례 수에 포함하지 않습니다.

최초 실패 후 수정·부분 재시험·추가 probe는 없었습니다. COMSOL/JVM/Java 컴파일/native/실제 입력·Job·정책 변경과 실제 승인 활성화도 없습니다. native_ready=false, 전체/정상 gate INCOMPLETE 및 기존 미확인 상태를 유지합니다.

다음 판단 대상은 PARENT_R113의 시험 입력 JSON 전달과 형식 assertion 한 곳입니다. 이미 통과한 결과의 재사용 여부와 이 실패 사례·후속 2개에 필요한 최소 검증 범위를 검토받을 수 있습니다. 이번 제출은 정정·재시험 또는 native 실행 승인이 아닙니다.
'''
with (R/'RESULT_KO.md').open('x',encoding='utf-8',newline='\n') as f: f.write(report)
check_budget()
name='COMSOL_MICROSHORT_S1O_R1_003_VALIDATION_STOP_20261008.zip'
excluded={name,'PACKAGE_MANIFEST.json','DELIVERY_RECEIPT.json','FINAL_PACKAGE_TOOL_RETURN.json','FINAL_SUBMISSION_CHECK.json'}
payload={}
for p in sorted(R.rglob('*')):
 if p.is_file() and '__pycache__' not in p.parts and p.name not in excluded:
  payload[p.relative_to(R).as_posix()]=p
manifest=read(S/'CODE_MANIFEST.json')
payload['source/CODE_MANIFEST.json']=S/'CODE_MANIFEST.json'
for item in manifest['files']: payload['source/'+item['path']]=S/item['path']
assert len({n.casefold() for n in payload})==len(payload)
entries=[]
for n,p in payload.items():
 assert not n.startswith('/') and '..' not in n.split('/') and not p.is_symlink()
 x=identity(p); entries.append({'path':n,'bytes':x['bytes'],'sha256':x['sha256']})
pm={'schema':'PAYLOAD_MANIFEST_V1','self_excluded':True,'count':len(entries),'files':entries}
write('PACKAGE_MANIFEST.json',pm)
with zipfile.ZipFile(R/name,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,p in payload.items(): z.write(p,n)
 z.write(R/'PACKAGE_MANIFEST.json','PACKAGE_MANIFEST.json')
with zipfile.ZipFile(R/name) as z:
 assert z.testzip() is None
 assert set(z.namelist())==set(payload)|{'PACKAGE_MANIFEST.json'}
 for item in entries:
  b=z.read(item['path']); assert len(b)==item['bytes'] and sha(b)==item['sha256']
  assert not (z.getinfo(item['path']).external_attr>>16)&0o170000==0o120000
check_budget()
zipid=identity(R/name)
assert zipid['bytes']<=52428800
fixturebytes=sum(p.stat().st_size for p in R.rglob('*') if p.is_file())
assert fixturebytes<=1073741824
receipt={'kind':'DELIVERY_RECEIPT','recipient':None,'zip':zipid,'manifest':identity(R/'PACKAGE_MANIFEST.json'),'payload_count':len(entries),'verification':'exact set,size,SHA,CRC,casefold uniqueness,path and symlink checks','fixture_bytes':fixturebytes,'overall_snapshot_s':elapsed(origin),'overall_limit_s':1860,'delivery_snapshot_s':elapsed(delivery),'delivery_limit_s':300,'snapshot_boundary':'after ZIP reread/hash before receipt write and tool return','result':'INCOMPLETE_FIRST_UNEXPECTED_HARNESS_FAILURE','native_ready':False}
write('DELIVERY_RECEIPT.json',receipt)
assert read(R/'DELIVERY_RECEIPT.json')==receipt
final={'kind':'PACKAGE_FINAL_RETURN','zip':zipid,'receipt':identity(R/'DELIVERY_RECEIPT.json'),'result':receipt['result'],'counts':counts,'overall_snapshot_s':elapsed(origin),'delivery_snapshot_s':elapsed(delivery),'within_time_limits':elapsed(origin)<=1860 and elapsed(delivery)<=300,'snapshot_boundary':'after receipt reread; before this tool return','recipient':None}
print(json.dumps(final,ensure_ascii=False,separators=(',',':')))
