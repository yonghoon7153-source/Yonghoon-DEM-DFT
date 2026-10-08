"""New offline packaging/preservation tool. No source execution or native call."""
from pathlib import Path
import json,hashlib,zipfile,time,datetime,sys
OUT=Path(__file__).resolve().parents[1]
def read(n):return json.loads((OUT/n).read_text(encoding='utf-8-sig'))
def save(n,o):(OUT/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def digest(b):return hashlib.sha256(b).hexdigest()
def identity(p):
    b=p.read_bytes();return {'path':p.relative_to(OUT).as_posix(),'bytes':len(b),'sha256':digest(b)}
origin=read('ORIGIN.json');origin_s=origin['monotonic_ticks']/origin['frequency']
events=read('PHASE_EVENTS.json');delivery=events[-1]
assert delivery['phase']=='delivery'
def elapsed():return time.perf_counter()-origin_s
def within():
    now=elapsed()
    if now>2700 or now-delivery['start_elapsed_s']>300:raise RuntimeError('PREPARATION_DELIVERY_BUDGET')
    return now
within()
for row in read('CODE_MANIFEST.json')['files']:
    now=identity(OUT/row['path']);assert now==row,('CODE_SEAL_CHANGED',row['path'])
originals=read('ORIGINALS_BEFORE.json');after=[]
for row in originals:
    p=Path(row['path']);raw=p.read_bytes()
    assert len(raw)==row['bytes'] and digest(raw)==row['sha256'],('ORIGINAL_CHANGED',str(p))
    after.append(dict(row))
save('ORIGINALS_AFTER.json',{'observation':'After corrections/static/plan sealing; before delivery ZIP creation','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':after,'count':len(after),'all_equal':True,'scope':'116 files selected from original prepared folder only; not whole PC/MPH/prefs'})
inp=read('INPUT_IDENTITY.json')
for key in ('review_zip','base_zip'):
    row=inp[key];raw=Path(row['path']).read_bytes();assert digest(raw)==row['sha256']
timing={'origin':origin,'phase_events':events,'snapshot_elapsed_s':within(),'scope':'PRE_PACKAGE snapshot; current source/plan sealing complete, delivery still open','parallel_work_accounting':'Phase wall-time counted once, no addition of worker times; plan drafting overlapped correction/static while final seal/reporting is plan_seal','total_limit_s':2700,'all_completed_phases_within_limit':all(p.get('within_limit',True) for p in events)}
save('TIMING_PRE_PACKAGE.json',timing)
zipname='COMSOL_MICROSHORT_S1O_R1_OFFLINE_CORRECTIONS_20261008.zip'
target=OUT/zipname;assert not target.exists()
excluded={'PACKAGE_MANIFEST.json','TIMING.json','DELIVERY_RECEIPT.json','FINAL_PACKAGE_TOOL_RETURN.json','SUPPLEMENT_CLOSEOUT.json','SUPPLEMENT_FINAL_TOOL_RETURN.json'}
payload=sorted([p for p in OUT.rglob('*') if p.is_file() and p.name not in excluded and p.suffix!='.zip'],key=lambda p:p.relative_to(OUT).as_posix())
rows=[identity(p) for p in payload]
names=[r['path'] for r in rows];assert len(names)==len(set(n.lower() for n in names))
save('PACKAGE_MANIFEST.json',{'kind':'S1O_R1_PREPARATION_PACKAGE','self_excluded':True,'code_manifest_sha256':digest((OUT/'CODE_MANIFEST.json').read_bytes()),'functional_validation':'NOT_RUN','files':rows})
with zipfile.ZipFile(target,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in payload+[OUT/'PACKAGE_MANIFEST.json']:
        z.write(p,p.relative_to(OUT).as_posix())
with zipfile.ZipFile(target) as z:
    assert z.testzip() is None
    assert set(z.namelist())==set(names+['PACKAGE_MANIFEST.json'])
    assert len(z.namelist())==len(names)+1
    for r in rows:
        b=z.read(r['path']);assert len(b)==r['bytes'] and digest(b)==r['sha256']
    for n in z.namelist():
        assert not n.startswith(('/','\\')) and '..' not in n.replace('\\','/').split('/') and ':' not in n
        assert (z.getinfo(n).external_attr>>16)&0o170000 !=0o120000
ident=identity(target)
# New source copies cannot be mutated between the seal and package publication.
for row in read('CODE_MANIFEST.json')['files']:assert identity(OUT/row['path'])==row
post=within()
timing.update({'snapshot_elapsed_s':post,'delivery_elapsed_s':post-delivery['start_elapsed_s'],'scope':'POST_PACKAGE: ZIP created, reread, CRC/member hashes and ZIP SHA verified; BEFORE writing this TIMING/receipt and BEFORE tool return. Following transcription is separate.','zip':ident,'within_limits':True})
save('TIMING.json',timing)
receipt={'kind':'R1_PACKAGE_DELIVERY_RECEIPT','recipient':None,'zip':ident,'payload_count':len(rows),'entries':len(rows)+1,'package_manifest_sha256':digest((OUT/'PACKAGE_MANIFEST.json').read_bytes()),'code_manifest_sha256':digest((OUT/'CODE_MANIFEST.json').read_bytes()),'timing_identity':identity(OUT/'TIMING.json'),'snapshot_elapsed_s':post,'total_limit_s':2700,'functional_validation':'NOT_RUN','native_ready':False,'tool_return':'Generated after this tool returns, in FINAL_PACKAGE_TOOL_RETURN.json; later transcription, not self-observed OS evidence.'}
save('DELIVERY_RECEIPT.json',receipt)
assert read('DELIVERY_RECEIPT.json')==receipt
last=within()
print(json.dumps({'kind':'R1_PACKAGE_FINAL_RETURN','status':'OFFLINE_PREPARATION_DELIVERED_PENDING_REVIEW','zip':ident,'payload_count':len(rows),'entries':len(rows)+1,'code_manifest_sha256':receipt['code_manifest_sha256'],'snapshot_elapsed_s':last,'total_limit_s':2700,'delivery_elapsed_s':last-delivery['start_elapsed_s'],'observation_scope':'AFTER ZIP/receipt/TIMING write and reread, BEFORE tool return; not end-to-end OS audit','functional_validation':'NOT_RUN','native_ready':False},ensure_ascii=False))
