"""Decode connector captures and preserve read-only review evidence; no target execution."""
import base64, hashlib, json
from pathlib import Path
R=Path(__file__).resolve().parent
P=R.parent/'reil_c4e_e1_1_3_scope_v3_review_20261104'
def sha(b): return hashlib.sha256(b).hexdigest()
def put(n,b):
    p=R/n; p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f: f.write(b)
    assert p.read_bytes()==b
def writej(n,d): put(n,(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
c=json.loads((R/'SOURCE_CAPTURE.json').read_bytes())
rows=[]; attachments=[]
for r in c['files']:
    b=base64.b64decode(r['content'])
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['sha']
    put('source/'+r['path'],b)
    rows.append({'path':r['path'],'bytes':len(b),'sha256':sha(b),'git_blob_sha1':r['sha'],'source':'Pinned GitHub connector base64; blob identity verified'})
    name=Path(r['path']).name
    if name in ['REIL_C4E_E1_1_3_APPROVAL_REQUEST_20261104.md','REIL_C4E_E1_1_3_PREREVIEW_SEND_20261104.md']:
        a=Path('C:/Users/Administrator/Downloads')/name; ab=a.read_bytes(); assert ab==b
        put('input/'+name,ab); attachments.append({'path':str(a),'bytes':len(ab),'sha256':sha(ab),'matches_pinned_source':True})
    if name!='REIL_PREREQUISITES_STATUS_20261004.md':
        put('numbered/'+name+'.lines.txt',('\n'.join(f'{i}: {s}' for i,s in enumerate(b.decode('utf-8').splitlines(),1))+'\n').encode('utf-8'))
cmp=json.loads((R/'COMPARE_FROM_SCOPE_V3.json').read_bytes())
assert cmp['status']=='ahead' and not cmp['too_large'] and len(cmp['files'])<300
changed={x['filename'] for x in cmp['files']}
old=json.loads((P/'SOURCE_IDENTITIES.json').read_bytes())
reused=[]
for rel in ['bms-balancing/scripts/reil_c4e1_launch.py','bms-balancing/scripts/reil_c4e_run.py','bms-balancing/docs/REIL_C4E_E1_0B_APPROVAL_REQUEST_20261030.md','bms-balancing/docs/REIL_C4E_E1_1_3_SCOPE_v3_20261104.md']:
    assert rel not in changed
    b=(P/'source'/rel).read_bytes()
    r=old['attachment'] if rel.endswith('SCOPE_v3_20261104.md') else next(x for x in old['reused_sources'] if x['path']==rel)
    assert sha(b)==r['sha256'] and len(b)==r['bytes']
    put('source/'+rel,b); reused.append({'path':rel,'bytes':len(b),'sha256':sha(b),'source':'Prior verified raw copy; unchanged path in complete pinned compare'})
for n in ['CODEX_REPLY_KO.txt','REVIEW_DECISION.json','SOURCE_IDENTITIES.json','DELIVERY_RECEIPT.json','PACKAGE_TOOL_RETURN.json']:
    put('basis/SCOPE_V3_'+n,(P/n).read_bytes())
writej('SOURCE_IDENTITIES.json',{'pin':c['pin'],'attachments':attachments,'connector_sources':rows,'reused_sources':reused,'received_program_execution':0,'probe_execution':0,'scope':'Static bytes/text; no remote runtime observation'})
print(json.dumps({'pin':c['pin'],'attachments':attachments,'new_sources':[{k:r[k] for k in ('path','bytes','sha256')} for r in rows],'reused_sources':len(reused)},ensure_ascii=False))
