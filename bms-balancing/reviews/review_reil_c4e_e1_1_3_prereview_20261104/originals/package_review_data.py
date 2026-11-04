"""Package verified review data only. Received sources are never imported/executed."""
import hashlib,json,stat,zipfile,zlib
from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
R=Path(__file__).resolve().parent
A=R/'REIL_C4E_E1_1_3_PREREVIEW_20261104.zip'
def sha(b):return hashlib.sha256(b).hexdigest()
def ident(p):
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
def writej(p,obj):
    b=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    with p.open('xb') as f:f.write(b)
    assert p.read_bytes()==b
    return ident(p)
i=json.loads((R/'SOURCE_IDENTITIES.json').read_bytes())
originals=[]
for row in i['attachments']:
    p=Path(row['path']); obs=ident(p)
    assert (obs['bytes'],obs['sha256'])==(row['bytes'],row['sha256'])
    assert p.read_bytes()==(R/'input'/p.name).read_bytes()==(R/'source/bms-balancing/docs'/p.name).read_bytes()
    originals.append(obs)
copies=[]
for row in i['connector_sources']+i['reused_sources']:
    p=R/'source'/row['path']; obs=ident(p)
    assert (obs['bytes'],obs['sha256'])==(row['bytes'],row['sha256'])
    copies.append({'path':'source/'+row['path'],'bytes':obs['bytes'],'sha256':obs['sha256']})
assert len(copies)==11 and len({r['path'] for r in copies})==11
writej(R/'SOURCE_PRESERVATION_CHECK.json',{'kind':'PREREVIEW_LOCAL_IDENTITY_RECHECK','utc':datetime.now(timezone.utc).isoformat(),'original_attachments':originals,'original_attachments_preserved':True,'reviewed_source_copies':copies,'scope':'Two local original attachments and 11 reviewed source paths; the attachments also occur among those source paths. Not 13 distinct remote originals or a remote runtime preservation audit.','received_program_execution':0})
d=json.loads((R/'REVIEW_DECISION.json').read_bytes())
assert d['decision']=='REVISION_REQUIRED_BEFORE_EXECUTION_APPROVAL' and len(d['findings'])==6
assert not d['readiness']['actual_execution_authorized_by_review']
assert json.loads((R/'HEAD_AT_CLOSE.json').read_bytes())['matches_reviewed_pin']
o=json.loads((R/'STATIC_SOURCE_OBSERVATIONS.json').read_bytes())
assert len(o['run_record_parts_keys'])==8 and len(o['judge_RUN_FILES'])==9 and o['received_program_execution']==0
excluded={A.name,'PACKAGE_MANIFEST.json','DELIVERY_RECEIPT.json','PACKAGE_TOOL_RETURN.json'}
payload={}
for p in sorted(R.rglob('*')):
    if not p.is_file():continue
    n=p.relative_to(R).as_posix()
    if n in excluded:continue
    q=PurePosixPath(n)
    assert not p.is_symlink() and not q.is_absolute() and all(s not in ('','.','..') for s in q.parts)
    assert ':' not in n and '\\' not in n
    payload[n]=p.read_bytes()
assert len({n.casefold() for n in payload})==len(payload)
manifest=writej(R/'PACKAGE_MANIFEST.json',{'kind':'STATIC_PREREVIEW_PACKAGE_MANIFEST','payload_count':len(payload),'manifest_self_excluded':True,'files':[{'path':n,'bytes':len(b),'sha256':sha(b)} for n,b in payload.items()],'scope':'Review evidence and reviewer data tools; received source copies and commands are not execution instructions.'})
sealed=dict(payload);sealed['PACKAGE_MANIFEST.json']=(R/'PACKAGE_MANIFEST.json').read_bytes()
with zipfile.ZipFile(A,'x',compression=zipfile.ZIP_DEFLATED) as z:
    for n,b in sealed.items():z.writestr(n,b)
with zipfile.ZipFile(A,'r') as z:
    info=z.infolist();assert len(info)==len(sealed) and {m.filename for m in info}==set(sealed)
    assert len({m.filename.casefold() for m in info})==len(info)
    for m in info:
        q=PurePosixPath(m.filename)
        assert not q.is_absolute() and all(s not in ('','.','..') for s in q.parts) and not stat.S_ISLNK(m.external_attr>>16)
        b=z.read(m.filename)
        assert b==sealed[m.filename] and m.file_size==len(b) and zlib.crc32(b)&0xffffffff==m.CRC
for r in originals:assert ident(Path(r['path']))==r
receipt=writej(R/'DELIVERY_RECEIPT.json',{'kind':'REIL_E113_PREREVIEW_DELIVERY_RECEIPT','recipient':None,'archive':ident(A),'manifest':manifest,'payload_count':len(payload),'entries':len(sealed),'verification':'Exact member set, safe unique relative paths, decompressed size/SHA256, non-link metadata and independently recomputed CRC32 matched.','decision':d['decision'],'findings':6,'small_schema_correction':'E113_PRE_C1','P2_02':'CLOSED_STATIC_CD_FAILURE_BRANCH','local_original_attachments_preserved':2,'reviewed_source_copies_matched':11,'received_program_execution':0,'probe_execution':0,'tests':0,'COMSOL':0,'actual_execution_authorized_by_review':False,'numeric_review_budget_seconds':None,'whole_review_elapsed_claim':None,'boundary':'After review archive readback and local attachment rehash; before receipt write/readback and tool return.'})
print(json.dumps({'kind':'REIL_E113_PREREVIEW_PACKAGE_RETURN','archive':ident(A),'receipt':receipt,'payload_count':len(payload),'entries':len(sealed),'decision':d['decision'],'findings':6,'P2_02':'CLOSED','received_program_execution':0,'probe_execution':0,'tests':0,'boundary':'After review ZIP and receipt write/readback; before actual tool return and its later transcription.'},ensure_ascii=False,indent=2))
