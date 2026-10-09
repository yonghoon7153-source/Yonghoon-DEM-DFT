"""Author-owned local packaging only; no candidate imports or native programs."""
from pathlib import Path
import json,hashlib,zipfile,time,datetime,sys
ROOT=Path(__file__).resolve().parents[1]
phase=json.loads((ROOT/'PHASE_RECORDS.json').read_bytes())
# On this Windows Python, perf_counter uses QPC, same frequency as Stopwatch.
# Values below are obtained via QueryPerformanceCounter directly to avoid a
# cross-runtime monotonic-origin assumption; this only reads a clock.
import ctypes
def tick():
 v=ctypes.c_longlong()
 if not ctypes.windll.kernel32.QueryPerformanceCounter(ctypes.byref(v)):raise RuntimeError('CLOCK_READ_FAILED')
 return v.value
def snapshot():
 t=tick();total=(t-phase['total_origin_ticks'])/phase['frequency'];delivery=(t-phase['delivery']['start_ticks'])/phase['frequency']
 if total>3600 or delivery>480:raise RuntimeError('DELIVERY_OR_TOTAL_BUDGET')
 size=sum(p.stat().st_size for p in ROOT.rglob('*') if p.is_file())
 if size>52428800:raise RuntimeError('FOLDER_SIZE_BUDGET')
 return {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'monotonic_ticks':t,'total_elapsed_s':total,'total_limit_s':3600,'delivery_elapsed_s':delivery,'delivery_limit_s':480,'folder_bytes':size,'folder_limit_bytes':52428800}
def ident(p):
 b=p.read_bytes();return {'path':p.as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(name,v):
 with (ROOT/name).open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
def preserve():
 before=json.loads((ROOT/'evidence/SELECTED_SOURCES_BEFORE.json').read_bytes());after=[]
 for e in before:
  got=ident(Path(e['path']))
  if got!=e:raise RuntimeError('SELECTED_PRESERVATION_MISMATCH:'+e['path'])
  after.append(got)
 return after
snapshot()
write('evidence/SELECTED_SOURCES_AFTER_PREPACKAGE.json',preserve())
write('IN_PACKAGE_CLOSEOUT.json',{'status':'OFFLINE_PREPARATION_SUBMITTED_WITH_FOUR_OPEN_ITEMS','native_ready':False,
 'approved':False,'usable':False,'static_checks':74,'functional_tests':0,'native_JVM_compile_solve':0,
 'preparation_s':phase['preparation']['elapsed_s'],'preparation_limit_s':2400,
 'static_s':phase['static']['elapsed_s'],'static_limit_s':600,
 'boundary':'BEFORE_PACKAGE_CREATION','snapshot':snapshot(),'recipient':None})
archive=ROOT/'COMSOL_MICROSHORT_S1_OPEN_CONNECTION_PREPARATION_20261009.zip'
if archive.exists():raise RuntimeError('PACKAGE_EXISTS_NO_OVERWRITE')
payload=sorted(p for p in ROOT.rglob('*') if p.is_file())
rows=[]
for p in payload:
 r=ident(p);r['path']=p.relative_to(ROOT).as_posix();rows.append(r)
write('PACKAGE_MANIFEST.json',{'self_excluded':True,'schema':'S1_OPEN_PREPARATION_PACKAGE_V1','payload_count':len(rows),'files':rows})
with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for r in rows:z.write(ROOT/r['path'],r['path'])
 z.write(ROOT/'PACKAGE_MANIFEST.json','PACKAGE_MANIFEST.json')
with zipfile.ZipFile(archive) as z:
 names=z.namelist()
 if len(names)!=len(set(n.casefold() for n in names)) or set(names)!={r['path'] for r in rows}|{'PACKAGE_MANIFEST.json'}:raise RuntimeError('ZIP_SET')
 for r in rows:
  b=z.read(r['path'])
  if len(b)!=r['bytes'] or hashlib.sha256(b).hexdigest()!=r['sha256']:raise RuntimeError('ZIP_PAYLOAD:'+r['path'])
 if z.testzip() is not None:raise RuntimeError('ZIP_CRC')
write('SELECTED_SOURCES_AFTER_PACKAGE.json',preserve())
receipt={'recipient':None,'kind':'NEW_OFFLINE_PREPARATION_DELIVERY_RECEIPT','archive':ident(archive),
 'package_manifest':ident(ROOT/'PACKAGE_MANIFEST.json'),'code_manifest':ident(ROOT/'CODE_MANIFEST.json'),
 'payload_count':len(rows),'entries':len(rows)+1,'zip_verification':'EXACT_SET_SIZE_SHA_CRC_MATCHED',
 'selected_preservation':ident(ROOT/'SELECTED_SOURCES_AFTER_PACKAGE.json'),'boundary':'AFTER_ZIP_REREAD_HASH_AND_SOURCE_RECHECK_BEFORE_RECEIPT_WRITE',
 'snapshot':snapshot(),'native_ready':False,'functional_tests_run':0}
write('DELIVERY_RECEIPT.json',receipt)
assert json.loads((ROOT/'DELIVERY_RECEIPT.json').read_bytes())==receipt
returned={'kind':'PACKAGE_COMPLETION','archive':ident(archive),'receipt':ident(ROOT/'DELIVERY_RECEIPT.json'),
 'boundary':'AFTER_RECEIPT_WRITE_READBACK_BEFORE_STDOUT_FILE_WRITE_AND_TOOL_RETURN',
 'snapshot':snapshot(),'native_ready':False,'overall':'INCOMPLETE','open_items':4}
write('PACKAGE_STDOUT.json',returned)
print(json.dumps(returned,ensure_ascii=False))
