"""Package this offline revision once, preserving originals; no candidate execution."""
import json,pathlib,hashlib,zipfile,time,stat
R=pathlib.Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def put(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(b):return hashlib.sha256(b).hexdigest()
def ident(p,relative=False):
 b=p.read_bytes();return {'path':str(p.relative_to(R) if relative else p).replace('\\','/'),'bytes':len(b),'sha256':sha(b)}
origin=read(R/'ORIGIN.json');freq=origin['frequency'];start=origin['monotonic_ticks'];tick=lambda:int(time.perf_counter()*freq)
zp=R/'COMSOL_MICROSHORT_S1_OPEN_CONNECTION_R1_20261010.zip'
assert not zp.exists() and not (R/'DELIVERY_RECEIPT.json').exists(),'PACKAGE_ALREADY_EXISTS'
ph=read(R/'PHASE_RECORDS.json');delivery=ph['plan_reseal']['end_ticks'];ph['preservation_delivery']={'start_ticks':delivery,'limit_s':300,'state':'IN_PROGRESS; final snapshots outside ZIP','origin_scope':'Immediately after plan/reseal; includes pre-package metadata/return transcription'};put(R/'PHASE_RECORDS.json',ph)
before=read(R/'evidence/SELECTED_SOURCES_BEFORE.json');after=[]
for f in before['files']:
 b=pathlib.Path(f['path']).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256'],'ORIGINAL_CHANGED:'+f['path'];after.append(f)
put(R/'evidence/SELECTED_SOURCES_AFTER_PREPACKAGE.json',{'files':after,'unique_paths':before['unique_paths']})
manifest=read(R/'CODE_MANIFEST.json')
for f in manifest['files']:assert ident(R/f['path'],True)==f,'CODE_CHANGED:'+f['path']
now=tick();put(R/'IN_PACKAGE_CLOSEOUT.json',{'phase':'AFTER_PREPACKAGE_ORIGINAL_HASHES_BEFORE_PACKAGE_WRITE','snapshot_ticks':now,'overall_s':(now-start)/freq,'delivery_s':(now-delivery)/freq,'originals_unchanged':True,'functional_tests':0,'native_ready':False,'actual_runtime_created':False,'post_package_evidence':'External DELIVERY_RECEIPT, FINAL_PACKAGE_TOOL_RETURN, FINAL_SUBMISSION_CHECK, FINAL_CHECK_TOOL_RETURN'})
excluded={'PACKAGE_MANIFEST.json',zp.name,'DELIVERY_RECEIPT.json','FINAL_PACKAGE_TOOL_RETURN.json','FINAL_SUBMISSION_CHECK.json','FINAL_CHECK_TOOL_RETURN.json','SELECTED_SOURCES_AFTER_PACKAGE.json'}
payload=[p for p in sorted(R.rglob('*')) if p.is_file() and p.relative_to(R).as_posix() not in excluded]
assert sum(p.stat().st_size for p in payload)<50*1024*1024,'SIZE_LIMIT'
pm={'schema':'OPEN_R1_STATIC_PACKAGE_V1','self_excluded':True,'payload_count':len(payload),'files':[ident(p,True) for p in payload]};put(R/'PACKAGE_MANIFEST.json',pm)
with zipfile.ZipFile(zp,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in payload+[R/'PACKAGE_MANIFEST.json']:z.write(p,str(p.relative_to(R)).replace('\\','/'))
with zipfile.ZipFile(zp) as z:
 names=z.namelist();assert set(names)=={f['path'] for f in pm['files']}|{'PACKAGE_MANIFEST.json'}
 assert len(names)==len(set(n.casefold() for n in names));assert z.testzip() is None
 for i in z.infolist():
  q=pathlib.PurePosixPath(i.filename);assert not q.is_absolute() and '..' not in q.parts and ':' not in i.filename and '\\' not in i.filename and not stat.S_ISLNK(i.external_attr>>16)
 for f in pm['files']:
  b=z.read(f['path']);assert len(b)==f['bytes'] and sha(b)==f['sha256']
for f in before['files']:
 b=pathlib.Path(f['path']).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256'],'AFTER_PACKAGE_ORIGINAL_CHANGED'
put(R/'SELECTED_SOURCES_AFTER_PACKAGE.json',{'files':after,'unique_paths':before['unique_paths']})
package=ident(zp);now=tick();receipt={'kind':'OFFLINE_REVISION_DELIVERY_RECEIPT','recipient':None,'package':package,'package_manifest':ident(R/'PACKAGE_MANIFEST.json'),'code_manifest':ident(R/'CODE_MANIFEST.json'),'payload_count':len(payload),'archive_verified':True,'original_preservation_items':len(after),'original_preservation_unique_paths':before['unique_paths'],'originals_unchanged':True,'phase':'AFTER_ZIP_READBACK_AND_HASH_BEFORE_RECEIPT_WRITE','snapshot_ticks':now,'overall_s':(now-start)/freq,'delivery_s':(now-delivery)/freq,'limits_s':{'total':2400,'delivery':300},'functional_tests':0,'native_calls':0,'native_ready':False}
assert receipt['overall_s']<=2400 and receipt['delivery_s']<=300,'BUDGET'
put(R/'DELIVERY_RECEIPT.json',receipt);assert read(R/'DELIVERY_RECEIPT.json')==receipt
receipt_id=ident(R/'DELIVERY_RECEIPT.json');now=tick();folderbytes=sum(p.stat().st_size for p in R.rglob('*') if p.is_file())
out={'kind':'OPEN_R1_PACKAGE_TOOL_STDOUT','phase':'AFTER_RECEIPT_READBACK_AND_HASH_BEFORE_TOOL_RETURN','package':package,'receipt':receipt_id,'overall_s':(now-start)/freq,'delivery_s':(now-delivery)/freq,'within_limits':(now-start)/freq<=2400 and (now-delivery)/freq<=300,'folder_bytes':folderbytes,'folder_limit_bytes':50*1024*1024,'functional_tests':0,'native_ready':False}
assert out['within_limits'] and folderbytes<=50*1024*1024
print(json.dumps(out,ensure_ascii=False))
