"""New bounded supplementary evidence packaging only, no candidate calls."""
from pathlib import Path
import json,hashlib,zipfile,time,datetime
OUT=Path(__file__).resolve().parents[1]
def read(n):return json.loads((OUT/n).read_text(encoding='utf-8-sig'))
def save(n,x):(OUT/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(b):return hashlib.sha256(b).hexdigest()
def ident(n):
    b=(OUT/n).read_bytes();return {'path':n,'bytes':len(b),'sha256':sha(b)}
o=read('ORIGIN.json');start=o['monotonic_ticks']/o['frequency'];events=read('PHASE_EVENTS.json');delivery=events[-1]
def observe():
    x=time.perf_counter()-start
    assert delivery['phase']=='delivery' and x<=2700 and x-delivery['start_elapsed_s']<=300
    return x
observe()
after=read('ORIGINALS_AFTER.json')
for row in after['files']:
    p=Path(row['path']);b=p.read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256']
save('POST_PACKAGE_ORIGINALS_CHECK.json',{'scope':'After main ZIP creation and returned-output transcription; before supplement packaging','selected_count':len(after['files']),'originals_after_identity':ident('ORIGINALS_AFTER.json'),'all_unchanged':True,'snapshot_elapsed_s':observe()})
main=read('FINAL_PACKAGE_TOOL_RETURN.json')
assert main['provenance']=='FOLLOWUP_TRANSCRIPTION_OF_ACTUAL_TOOL_RETURN' and main['tool_result']['exit_code']==0
stdout=json.loads(main['tool_result']['output'].strip())
assert stdout['zip']==ident(stdout['zip']['path'])
names=['TIMING.json','DELIVERY_RECEIPT.json','FINAL_PACKAGE_TOOL_RETURN.json','POST_PACKAGE_ORIGINALS_CHECK.json']
manifest={'kind':'R1_DELIVERY_SUPPLEMENT','self_excluded':True,'files':[ident(n) for n in names],'main_zip':stdout['zip'],'functional_validation':'NOT_RUN'}
manifestbytes=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
target=OUT/'COMSOL_MICROSHORT_S1O_R1_DELIVERY_SUPPLEMENT_20261008.zip';assert not target.exists()
with zipfile.ZipFile(target,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for n in names:z.write(OUT/n,n)
    z.writestr('MANIFEST.json',manifestbytes)
with zipfile.ZipFile(target) as z:
    assert z.testzip() is None and set(z.namelist())==set(names+['MANIFEST.json']) and len(z.namelist())==5
    for r in manifest['files']:
        b=z.read(r['path']);assert len(b)==r['bytes'] and sha(b)==r['sha256']
supplement=ident(target.name);snap=observe()
completed=[dict(p) for p in events]
completed[-1].update({'end_elapsed_s':snap,'duration_s':snap-delivery['start_elapsed_s'],'within_limit':True,'boundary':'after supplementary ZIP reread/hash, before closeout write and tool return'})
closeout={'kind':'R1_SUPPLEMENT_CLOSEOUT','zip':supplement,'main_zip':stdout['zip'],'snapshot_elapsed_s':snap,'total_limit_s':2700,'delivery_elapsed_s':snap-delivery['start_elapsed_s'],'delivery_limit_s':300,'phase_events':completed,'within_limits':True,'recipient':None,'scope':'Snapshot after supplement CRC/member hashes and ZIP SHA; before this closeout write/tool return, not independent OS audit. Tool wall time must not be added to elapsed snapshot.','functional_validation':'NOT_RUN','native_ready':False}
save('SUPPLEMENT_CLOSEOUT.json',closeout)
assert read('SUPPLEMENT_CLOSEOUT.json')==closeout
last=observe()
print(json.dumps({'kind':'R1_SUPPLEMENT_FINAL_RETURN','zip':supplement,'closeout':ident('SUPPLEMENT_CLOSEOUT.json'),'snapshot_elapsed_s':last,'total_limit_s':2700,'delivery_elapsed_s':last-delivery['start_elapsed_s'],'delivery_limit_s':300,'within_limits':True,'scope':'after supplementary package+closeout reread, BEFORE tool return','functional_validation':'NOT_RUN','native_ready':False},ensure_ascii=False))
