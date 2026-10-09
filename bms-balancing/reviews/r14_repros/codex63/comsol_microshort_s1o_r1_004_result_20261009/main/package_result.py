"""Data-only preservation and delivery. No candidate import or test invocation."""
import json,hashlib,time,zipfile,csv
from pathlib import Path
R=Path(__file__).resolve().parent;S=R.parent;OLD=S/'future_validation_fixture_R1_003'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
def ident(p):
 p=Path(p);b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
def write(n,o):
 with (R/n).open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2)
origin=read(R/'ORIGIN.json');delivery=read(R/'DELIVERY_ORIGIN.json')
def elapsed(o):return time.perf_counter()-o['monotonic_ticks']/o['frequency']
def budget():
 assert elapsed(origin)<1140 and elapsed(delivery)<220,'DELIVERY_RESERVE'
budget()
py=read(R/'results/PYTHON_RESULTS.json');ps=read(R/'results/ps_results.json')
assert py['status']=='PASS' and py['count']==4 and ps['status']=='PASS' and ps['case_count']==3
assert [x['id'] for x in ps['cases']]==['PARENT_R115','PARENT_R113','PARENT_R114']
for x in ps['cases']:assert x['result']=='PASS' and x['reason_matches'] and x['reach_matches'] and x['extra_assertions']
transport=ps['cases'][1]['json_transport'];assert transport['cast_clr_type']=='System.Double' and transport['other_leaves_unchanged']
assert ps['cases'][1]['raw_return']['reason']=='DECIMAL_TRANSPORT_PRECISION' and ps['cases'][1]['raw_return']['stage']=='comparison_numerics'
assert ps['cases'][2]['raw_return']['reason']=='COMPARISON_SUMMARY_CONTRADICTION' and ps['cases'][2]['raw_return']['stage']=='fields'
sessions={x:read(R/f'results/{x}_SESSION.json') for x in ('PYTHON','POWERSHELL')}
assert all(x['rc']==0 and x['within_limits'] and not x['timed_out'] for x in sessions.values())
seal=read(R/'FIRST_SEAL.json');after=[]
for p in seal['files']:
 now=ident(p['path']);same=now['bytes']==p['bytes'] and now['sha256']==p['sha256'];after.append({'before':p,'after':now,'match':same})
assert all(x['match'] for x in after)
write('SELECTED_SOURCES_AFTER.json',{'scope':'Current first seal including prior123 and archive lineage, engines, dependencies, new harness and reused producer bytes','all_match':True,'count':len(after),'items':after})
oldpy=read(OLD/'results/PYTHON_RESULTS.json');oldps=read(OLD/'results/ps_first_failure.json');oldplan=read(OLD/'VALIDATION_PLAN_CORRECTED.json');old_cases={x['id']:x for x in oldplan['cases']}
rows=[]
for x in oldpy['cases']+oldps['cases']:
 cid=x['id'];rows.append({'id':cid,'category':'ORIGINAL_REUSED','status':'PASS','source':'R1_003','expected':old_cases[cid]['expected'],'observed':x['observed'],'reached':x.get('reached_functions',x.get('target_reach')),'read_control_supplement':cid in [f'READ{i:02d}' for i in range(2,13)]})
for x in ps['cases']:rows.append({'id':x['id'],'category':'ORIGINAL_NEWLY_SATISFIED','status':x['result'],'source':'R1_004','expected':x['expected'],'observed':x['observed'],'reached':x['target_reach']})
assert len(rows)==130 and len({x['id'] for x in rows})==130
write('ORIGINAL130_COVERAGE_MAP.json',{'original_reused':127,'original_newly_satisfied':3,'original_target_total':130,'auxiliary_positive_new':4,'not_one_130_case_session':True,'prior_R1_003_status_unchanged':'INCOMPLETE','cases':rows,'auxiliary_cases':py['cases']})
write('VALIDATION_CLOSEOUT.json',{'status':'LIMITED_SUBSET_VALIDATION_PASS_AWAITING_EXTERNAL_REVIEW','new_cases':7,'new_python_positive':4,'new_ps_original_cases':3,'prior127_reused':True,'prior003_failure_preserved':True,'original130_coverage':'127 reused +3 newly satisfied;4 auxiliary separately','preseal_s':seal['preseal_elapsed_s'],'preseal_limit_s':600,'sessions':sessions,'transport_observation':transport,'production_edits':0,'automatic_retries':0,'native_ready':False,'overall':'INCOMPLETE','normal_gate':'INCOMPLETE','installed_t0_coefficients_native_raw_OS_adapters':'OPEN','actual_COMSOL_JVM_Java_compile_native_input_Job_policy_calls':0,'engine_processes':'One functional Python session and one PS5.1 session; separate data-only preparation/packaging Python calls are not functional tests','overall_snapshot_s':elapsed(origin),'delivery_snapshot_s':elapsed(delivery),'boundary':'before packaging'})
report=f'''# S1O-R1 R1_004 잔여 검증 결과 — 2026-10-09

**새 7개 입력 한정 검증 PASS, 독립 수신 검토 대기입니다.** 실제 COMSOL 또는 microshort 계산은 하지 않았습니다.

집계는 원 127개 재사용 + 원 미완 PARENT_R115/R113/R114 3개 신규 충족이며, Python 보조 양성 4개는 별도입니다. 130개를 한 번에 재시험했다고 표현하지 않습니다. R1_003의 INCOMPLETE·첫 실패와 기존 원본은 그대로입니다.

Python READ_CTRL_CSV/TIME/COVERAGE/PROFILE은 각각 실제 생산 함수에 한 번 진입하여 정확한 정상 반환을 확인했습니다. 동일 기본 입력에서 선언한 변이만 적용한 데이터가 기존 READ02–12의 canonical 입력 해시와 모두 같았습니다. READ05–07은 raw와 identity의 복수 변이, READ10은 다섯 벡터의1 제거로 명시했습니다. 기존 음성함수는 재시험하지 않았습니다.

PowerShell 순서는 R115 → R113 → R114입니다. R115는 기존 POLICY02 문자열값의 정상 판정 및 WITHIN_LIMITS_THIS_WINDOW, R113은 DECIMAL_TRANSPORT_PRECISION/comparison_numerics, R114는 COMPARISON_SUMMARY_CONTRADICTION/fields를 실제 S1Decision·하위 함수에서 확인했습니다. 임의 조기 오류를 PASS로 세지 않았습니다.

R113 JSON 파서의 실제 형식은 **{transport['parsed_clr_type']}**, 값은 {transport['parsed_value']}였습니다. 유한한0.001인지 확인한 뒤 fixture의 해당 leaf만 **{transport['cast_clr_type']}**로 명시 변환했습니다. Double64비트는 {transport['double_bits_hex']}이며 나머지 leaf는 동일합니다. 파서가 Double을 만들었다고 주장하지 않습니다. 실제 원문 producer를 재생성하지 않았고 원 JSON/context10개를 동일 바이트로 연결했습니다. R114 양성 대조 PARENT02는 같은 소스·엔진·POLICY03·원 반환/도달 기록으로 재사용했으며 새로 호출하지 않았습니다.

사전 봉인 {seal['preseal_elapsed_s']:.6f}/600초, Python {sessions['PYTHON']['elapsed_s']:.6f}/120초·rc0, PS5.1 {sessions['POWERSHELL']['elapsed_s']:.6f}/180초·rc0입니다. 최종 전달 시간은 ZIP 밖 영수증과 마지막 포장 도구 반환을 함께 확인하세요. 내부 snapshot과 tool wall time은 합산하지 않습니다.

생산 소스 변경0, 재시도0입니다. 원 R1_003 ZIP153payload 대조와 원 봉인123개를 포함한 현재 봉인 {len(after)}개 파일의 전후 식별이 일치합니다. 서로 다른 집합을 합쳐 고유 원본 수로 주장하지 않습니다. 기존 결과 ZIP은 reference에 원바이트로 포함했습니다.

native_ready=false, 전체/정상 gate INCOMPLETE, 설치본t0·계수·native/raw/OS 어댑터 OPEN을 유지합니다. 이번 결과는 실제 S1-P 또는 후속 COMSOL 실행 승인이 아닙니다. 제출 후 중지합니다.
'''
with (R/'RESULT_KO.md').open('x',encoding='utf-8') as f:f.write(report)
budget()
name='COMSOL_MICROSHORT_S1O_R1_004_VALIDATION_RESULT_20261009.zip'
exclude={name,'PACKAGE_MANIFEST.json','DELIVERY_RECEIPT.json','FINAL_PACKAGE_TOOL_RETURN.json','FINAL_SUBMISSION_CHECK.json'}
files={p.relative_to(R).as_posix():p for p in R.rglob('*') if p.is_file() and p.name not in exclude and '__pycache__' not in p.parts}
assert len(files)==len({n.casefold() for n in files})
items=[]
for n,p in sorted(files.items()):
 assert '..' not in n.split('/') and not n.startswith('/') and not p.is_symlink()
 x=ident(p);items.append({'path':n,'bytes':x['bytes'],'sha256':x['sha256']})
write('PACKAGE_MANIFEST.json',{'self_excluded':True,'payload_count':len(items),'files':items})
with zipfile.ZipFile(R/name,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,p in sorted(files.items()):z.write(p,n)
 z.write(R/'PACKAGE_MANIFEST.json','PACKAGE_MANIFEST.json')
with zipfile.ZipFile(R/name) as z:
 assert z.testzip() is None and set(z.namelist())==set(files)|{'PACKAGE_MANIFEST.json'}
 for x in items:
  b=z.read(x['path']);assert len(b)==x['bytes'] and sha(b)==x['sha256']
budget()
zipid=ident(R/name);assert zipid['bytes']<=50*1024**2
fixturebytes=sum(p.stat().st_size for p in R.rglob('*') if p.is_file());assert fixturebytes<=1024**3
receipt={'kind':'DELIVERY_RECEIPT','recipient':None,'zip':zipid,'manifest':ident(R/'PACKAGE_MANIFEST.json'),'payload_count':len(items),'fixture_bytes':fixturebytes,'verification':'exact set,size,SHA,CRC,casefold/path/symlink checks','result':'LIMITED_SUBSET_VALIDATION_PASS_AWAITING_EXTERNAL_REVIEW','overall_snapshot_s':elapsed(origin),'overall_limit_s':1200,'delivery_snapshot_s':elapsed(delivery),'delivery_limit_s':240,'boundary':'after zip reread/hash before receipt write and tool return','native_ready':False}
write('DELIVERY_RECEIPT.json',receipt);assert read(R/'DELIVERY_RECEIPT.json')==receipt
print(json.dumps({'kind':'PACKAGE_FINAL_RETURN','zip':zipid,'receipt':ident(R/'DELIVERY_RECEIPT.json'),'result':receipt['result'],'new_pass':7,'prior_reused':127,'overall_snapshot_s':elapsed(origin),'delivery_snapshot_s':elapsed(delivery),'within_time_limits':elapsed(origin)<=1200 and elapsed(delivery)<=240,'boundary':'after receipt reread before tool return','native_ready':False},separators=(',',':')))
