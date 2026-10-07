"""New S1-O packaging of offline artifacts only; does not run any payload."""
import pathlib,json,hashlib,zipfile,time,datetime,stat
R=pathlib.Path(__file__).resolve().parent
def load(n):return json.loads((R/n).read_bytes())
def write(n,v):(R/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def identity(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
start=load('START.json'); timing=load('TIMING.json')
origin=start['monotonic_ticks']/start['frequency']
elapsed=lambda:time.perf_counter()-origin
assert timing['within_phase_limits'] is True
assert elapsed()<3600 and elapsed()-timing['delivery_start_elapsed_s']<240,'insufficient closeout reserve'
zipname='COMSOL_MICROSHORT_S1O_OFFLINE_PREPARATION_20261007.zip'
assert not (R/zipname).exists() and not (R/'MANIFEST.json').exists()
returns=load('STATIC_TOOL_RETURNS.json')
returns['records'] += [dict(chunk='352741',rc=0,wall_seconds=6.2832159,kind='finalpost-editstatic',checks=181),dict(chunk='7a7caf',rc=0,wall_seconds=6.7014814,kind='finalbundledPSparse',errors=[])]
write('STATIC_TOOL_RETURNS.json',returns)
exclude={'MANIFEST.json',zipname,'DELIVERY_RECEIPT.json','FINAL_PACKAGE_TOOL_RETURN.json','LAST_RETURN_SOURCE_NOTE.json'}
files=sorted(p for p in R.rglob('*') if p.is_file() and p.relative_to(R).as_posix() not in exclude)
entries=[]
for p in files:
 assert not p.is_symlink()
 i=identity(p);i['path']=p.relative_to(R).as_posix();entries.append(i)
write('MANIFEST.json',dict(kind='S1O_OFFLINE_DELIVERY_MANIFEST',self_excluded=True,payload_count=len(entries),files=entries))
with zipfile.ZipFile(R/zipname,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files+[R/'MANIFEST.json']: z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(R/zipname) as z:
 names=z.namelist();assert len(names)==len(set(n.casefold() for n in names))
 assert set(names)=={x['path'] for x in entries}|{'MANIFEST.json'}
 for zi in z.infolist():
  p=pathlib.PurePosixPath(zi.filename)
  assert not p.is_absolute() and '..' not in p.parts and ':' not in zi.filename and '\\' not in zi.filename and not stat.S_ISLNK(zi.external_attr>>16)
 for f in entries:
  b=z.read(f['path']);assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'],f['path']
 assert z.read('MANIFEST.json')==(R/'MANIFEST.json').read_bytes()
originals=load('SELECTED_ORIGINALS_BEFORE.json')['files']
inputs=load('INPUTS_BEFORE.json')['inputs']
assert [identity(pathlib.Path(x['path'])) for x in originals]==originals
assert [identity(pathlib.Path(x['path'])) for x in inputs]==inputs
snapshot=elapsed();delivery=snapshot-timing['delivery_start_elapsed_s']
assert snapshot<=3600 and delivery<=300
receipt=dict(kind='S1O_DELIVERY_RECEIPT',recipient=None,package=identity(R/zipname),payload_count=len(entries),zip_entries=len(names),
 manifest=identity(R/'MANIFEST.json'),code_manifest=identity(R/'CODE_MANIFEST.json'),crc_sha_path_exact_set=True,
 selected_originals_after_pack_unchanged=True,selected_original_count=len(originals),input_attachment_count=len(inputs),
 total_elapsed_snapshot_s=snapshot,delivery_elapsed_snapshot_s=delivery,limits_s={'overall':3600,'delivery':300},
 observation='after ZIP close/readback/allpayloadCRC+SHA andselectedoriginalhash checks; before receipt write andtoolreturn',
 pre_origin_intake='separate disclosed initialread, not included in this monotonicelapsed',
 native_ready=False,COMSOL=0,JVM=0,compile=0,solve=0,synthetic_tests=0)
write('DELIVERY_RECEIPT.json',receipt)
assert load('DELIVERY_RECEIPT.json')==receipt
final_snapshot=elapsed()
print(json.dumps(dict(kind='S1O_PACKAGE_COMPLETE',package=receipt['package'],payload_count=len(entries),entries=len(names),
 code_manifest_sha256=receipt['code_manifest']['sha256'],receipt=identity(R/'DELIVERY_RECEIPT.json'),
 final_snapshot_s=final_snapshot,delivery_snapshot_s=final_snapshot-timing['delivery_start_elapsed_s'],
 snapshot_scope='after receipt write/readback and before this tool return; not an OS process exit observation',
 native_ready=False,COMSOL=0,synthetic_tests=0),ensure_ascii=False))
