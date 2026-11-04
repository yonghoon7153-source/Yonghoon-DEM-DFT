"""Review-data packaging only; no received source, shell probe or target import."""
import hashlib, json, stat, zipfile, zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
R=Path(__file__).resolve().parent
A=R/'REIL_C4E_E1_1_3_SCOPE_V3_REVIEW_20261104.zip'
def sha(b): return hashlib.sha256(b).hexdigest()
def ident(p):
    b=p.read_bytes(); return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
def writej(p,obj):
    b=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    with p.open('xb') as f: f.write(b)
    assert p.read_bytes()==b
    return ident(p)
i=json.loads((R/'SOURCE_IDENTITIES.json').read_bytes())
original=Path(i['attachment']['path'])
observed=ident(original)
assert (observed['bytes'],observed['sha256'])==(i['attachment']['bytes'],i['attachment']['sha256'])
assert original.read_bytes()==(R/'input'/original.name).read_bytes()==(R/'source/bms-balancing/docs'/original.name).read_bytes()
copies=[]
for row in i['reused_sources']:
    p=R/'source'/row['path']; r=ident(p)
    assert (r['bytes'],r['sha256'])==(row['bytes'],row['sha256'])
    assert p.read_bytes()==(R.parent/'reil_c4e_e1_1_3_scope_v2_review_20261104/source'/row['path']).read_bytes()
    copies.append({'path':'source/'+row['path'],'bytes':r['bytes'],'sha256':r['sha256'],'matches_prior_review_copy':True})
writej(R/'SOURCE_PRESERVATION_CHECK.json',{'kind':'REVIEW_SOURCE_IDENTITY_RECHECK','utc':datetime.now(timezone.utc).isoformat(),'original_attachment':observed,'original_attachment_matches_intake':True,'fixed_source_copies':copies,'original_attachment_count':1,'fixed_source_copy_count':len(copies),'scope':'One local original attachment and five previously reviewed raw source copies; not a remote runtime or whole-filesystem audit.','received_program_execution':0})
d=json.loads((R/'REVIEW_DECISION.json').read_bytes())
assert d['closures']['P2_01']=='CLOSED'
assert all(d['closures'][f'N2_F{n}']=='DOCUMENT_CORRECTION_CLOSED' for n in (1,2,3))
assert d['p1_document_direction_acceptable'] and not d['p1_drafting_blocked'] and not d['p2_immediate_probe_ready']
assert not d['probe_authorized'] and not d['actual_execution_authorized'] and not d['user_choices_recorded']
assert json.loads((R/'HEAD_AT_CLOSE.json').read_bytes())['matches_reviewed_pin']
exclude={A.name,'PACKAGE_MANIFEST.json','DELIVERY_RECEIPT.json','PACKAGE_TOOL_RETURN.json'}
payload={}
for p in sorted(R.rglob('*')):
    if not p.is_file(): continue
    name=p.relative_to(R).as_posix()
    if name in exclude: continue
    q=PurePosixPath(name)
    assert not p.is_symlink() and not q.is_absolute() and all(s not in ('','.','..') for s in q.parts)
    assert ':' not in name and '\\' not in name
    payload[name]=p.read_bytes()
assert len({s.casefold() for s in payload})==len(payload)
rows=[{'path':n,'bytes':len(b),'sha256':sha(b)} for n,b in payload.items()]
manifest=writej(R/'PACKAGE_MANIFEST.json',{'kind':'REVIEW_PACKAGE_MANIFEST','payload_count':len(rows),'manifest_self_excluded':True,'files':rows,'scope':'Static review and review-data tools; received source copies are evidence, not execution authorization.'})
sealed=dict(payload); sealed['PACKAGE_MANIFEST.json']=(R/'PACKAGE_MANIFEST.json').read_bytes()
with zipfile.ZipFile(A,'x',compression=zipfile.ZIP_DEFLATED) as z:
    for n,b in sealed.items(): z.writestr(n,b)
with zipfile.ZipFile(A,'r') as z:
    info=z.infolist()
    assert len(info)==len(sealed) and {m.filename for m in info}==set(sealed)
    assert len({m.filename.casefold() for m in info})==len(info)
    for m in info:
        q=PurePosixPath(m.filename)
        assert not q.is_absolute() and all(s not in ('','.','..') for s in q.parts)
        assert not stat.S_ISLNK(m.external_attr>>16)
        b=z.read(m.filename)
        assert b==sealed[m.filename] and m.file_size==len(b) and (zlib.crc32(b)&0xffffffff)==m.CRC
assert original.read_bytes()==(R/'input'/original.name).read_bytes()
receipt=writej(R/'DELIVERY_RECEIPT.json',{'kind':'REIL_SCOPE_V3_REVIEW_DELIVERY_RECEIPT','recipient':None,'archive':ident(A),'manifest':manifest,'payload_count':len(payload),'entries':len(sealed),'verification':'Exact set, safe unique relative paths, decompressed size/SHA256, link metadata and independently recomputed CRC32 matched.','original_attachment_preserved':True,'fixed_source_copies_matched':len(copies),'decision':d['decision'],'closures':d['closures'],'p1_document_direction_acceptable':True,'p2_immediate_probe_ready':False,'user_choices_recorded':False,'received_program_execution':0,'probe_execution':0,'actual_E1_execution_authorized':False,'numeric_review_budget_seconds':None,'whole_work_elapsed_claim':None,'boundary':'After review ZIP readback and original attachment rehash; before receipt write/readback and tool return.'})
print(json.dumps({'kind':'REIL_SCOPE_V3_REVIEW_PACKAGE_RETURN','archive':ident(A),'receipt':receipt,'payload_count':len(payload),'entries':len(sealed),'decision':d['decision'],'old_P2_01_F1_F2_F3_closed':True,'p1_document_direction_acceptable':True,'p2_immediate_probe_ready':False,'received_program_execution':0,'probe_execution':0,'boundary':'After review ZIP/receipt write and readback; before actual tool return and its later transcription.'},ensure_ascii=False,indent=2))
