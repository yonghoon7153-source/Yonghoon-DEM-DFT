"""Read immutable records and compute timing relationships; no candidate execution."""
from pathlib import Path
import hashlib,json
from decimal import Decimal as D

ROOT=Path(__file__).resolve().parent
PREV=ROOT.parent/'microshort_s1o_r1_004_review_20261009'
INPUTS={
 'FINAL_SUBMISSION_CHECK.json':('afd5989d84b78413d6613207c80dfe7eae8d4a8fb3f7374a02c02a9431d18261',395),
 'COMSOL_MICROSHORT_S1O_R1_004_REVIEW_REPLY_SEND_20261009.md':('8acc72ad4baf0b21786cd81fb6e1a62430b4cf0bae9de289ea875555a7026ddb',6501)}
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'),parse_float=D)
final_path=Path('C:/Users/Administrator/Downloads/FINAL_SUBMISSION_CHECK.json')
request_path=Path('C:/Users/Administrator/Downloads/COMSOL_MICROSHORT_S1O_R1_004_REVIEW_REPLY_SEND_20261009.md')
final=read(final_path)
assert len(final_path.read_bytes())==395 and sha(final_path.read_bytes())==INPUTS[final_path.name][0]
assert len(request_path.read_bytes())==6501 and sha(request_path.read_bytes())==INPUTS[request_path.name][0]
prior_receipt=read(PREV/'REVIEW_DELIVERY_RECEIPT.json')
prior_zip=PREV/'COMSOL_MICROSHORT_S1O_R1_004_VALIDATION_REVIEW_20261009.zip'
assert len(prior_zip.read_bytes())==prior_receipt['zip']['bytes'] and sha(prior_zip.read_bytes())==prior_receipt['zip']['sha256']
origin=read(PREV/'received/ORIGIN.json'); delivery=read(PREV/'received/DELIVERY_ORIGIN.json'); close=read(PREV/'received/VALIDATION_CLOSEOUT.json')
offset=D(delivery['monotonic_ticks']-origin['monotonic_ticks'])/D(origin['frequency'])
rows=[
 {'name':'ZIP_CLOSEOUT','overall':close['overall_snapshot_s'],'delivery':close['delivery_snapshot_s'],'origin':'archive original; pre packaging'},
 {'name':'RECEIPT','overall':D('569.9025540000293'),'delivery':D('116.78792289993726'),'origin':'prior user-pasted receipt; original file not received'},
 {'name':'PACKAGE_RETURN','overall':D('569.9144170000218'),'delivery':D('116.79978640004992'),'origin':'prior user-pasted eb8612 return transcription'},
 {'name':'FINAL_SUBMISSION_CHECK','overall':final['overall_snapshot_s'],'delivery':final['delivery_snapshot_s'],'origin':'new original file; before check write and final tool return'}]
assert final['frozen_files']==246 and final['all_unchanged'] and final['package_tool_return_matches_zip_and_receipt']
assert final['overall_limit_s']==1200 and final['delivery_limit_s']==240 and final['native_ready'] is False
assert all(r['overall']<1200 and r['delivery']<240 for r in rows)
assert all(rows[i+1]['overall']>rows[i]['overall'] and rows[i+1]['delivery']>rows[i]['delivery'] for i in range(3))
for r in rows:
    r['separate_snapshot_offset_difference_s']=r['overall']-r['delivery']-offset
    r['within_declared_snapshot_limits']=True
result={'kind':'SUPPLEMENT_RECORD_REVIEW','inputs':[{'path':str(p),'bytes':len(p.read_bytes()),'sha256':sha(p.read_bytes())} for p in (final_path,request_path)],
 'previous_review_archive':prior_receipt['zip'],'timing_rows':rows,'delivery_origin_after_overall_origin_s':offset,
 'final_snapshot_margin_overall_s':D(1200)-final['overall_snapshot_s'],'final_snapshot_margin_delivery_s':D(240)-final['delivery_snapshot_s'],
 'additional_elapsed_after_package_snapshot_s':final['overall_snapshot_s']-rows[2]['overall'],
 'after_check_write_and_final_return_elapsed':'UNOBSERVED_NOT_INFERRED',
 'snapshot_status':'WITHIN_LIMITS_AT_RECORDED_BOUNDARY','submission_file_bytes_sha':'MATCHED',
 'preservation_at_latest_snapshot':'PRODUCER_AGGREGATE_ASSERTION_NOT_NEW_RECIPIENT_PER_FILE_MEASUREMENT',
 'received_code_executions':0,'COMSOL_calls':0}
with (ROOT/'SUPPLEMENT_CHECK.json').open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2,default=str)
print(json.dumps(result,ensure_ascii=False,default=str))
