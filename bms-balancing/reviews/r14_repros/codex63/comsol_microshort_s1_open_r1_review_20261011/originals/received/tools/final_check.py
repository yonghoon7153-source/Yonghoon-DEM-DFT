"""Read-back and provenance record only. No candidate or native execution."""
import pathlib,json,hashlib,time
R=pathlib.Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def info(p):
 b=p.read_bytes();return {'path':str(p).replace('\\','/'),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
o=read(R/'ORIGIN.json');ph=read(R/'PHASE_RECORDS.json');freq=o['frequency'];start=o['monotonic_ticks'];delivery=ph['preservation_delivery']['start_ticks']
receipt=read(R/'DELIVERY_RECEIPT.json');tool=read(R/'FINAL_PACKAGE_TOOL_RETURN.json')
assert tool['exit_code']==0 and tool['reported_output']['package']==receipt['package']
assert info(pathlib.Path(receipt['package']['path']))==receipt['package']
manifest=read(R/'CODE_MANIFEST.json')
for f in manifest['files']:
 got=info(R/f['path']);assert got['bytes']==f['bytes'] and got['sha256']==f['sha256']
before=read(R/'evidence/SELECTED_SOURCES_BEFORE.json')
for f in before['files']:
 got=info(pathlib.Path(f['path']));assert got['bytes']==f['bytes'] and got['sha256']==f['sha256']
tick=int(time.perf_counter()*freq)
result={'kind':'FINAL_SUBMISSION_CHECK','phase':'AFTER_PACKAGE_CODE_AND_ORIGINAL_READBACK_BEFORE_THIS_FILE_WRITE','snapshot_ticks':tick,'overall_s':(tick-start)/freq,'delivery_s':(tick-delivery)/freq,'within_limits':(tick-start)/freq<=2400 and (tick-delivery)/freq<=300,'source_items':len(before['files']),'unique_source_paths':before['unique_paths'],'all_selected_unchanged':True,'code_manifest':info(R/'CODE_MANIFEST.json'),'delivery_receipt':info(R/'DELIVERY_RECEIPT.json'),'package_tool_return':info(R/'FINAL_PACKAGE_TOOL_RETURN.json'),'package_matches_receipt_and_return':True,'functional_tests':0,'native_ready':False,'scope_limit':'This file cannot observe its own later write or external tool-return time; next stdout separately observes its write/read/hash.'}
assert result['within_limits']
p=R/'FINAL_SUBMISSION_CHECK.json';assert not p.exists();p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');assert read(p)==result
final_id=info(p);tick=int(time.perf_counter()*freq)
print(json.dumps({'kind':'FINAL_CHECK_TOOL_STDOUT','phase':'AFTER_FINAL_CHECK_WRITE_READBACK_AND_HASH_BEFORE_TOOL_RETURN','final_check':final_id,'overall_s':(tick-start)/freq,'delivery_s':(tick-delivery)/freq,'within_limits':(tick-start)/freq<=2400 and (tick-delivery)/freq<=300,'functional_tests':0,'native_ready':False},ensure_ascii=False))
