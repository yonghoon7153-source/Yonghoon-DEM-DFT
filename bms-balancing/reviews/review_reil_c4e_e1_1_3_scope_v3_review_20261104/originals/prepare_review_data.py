"""Static bytes/text preparation only; never execute received source or commands."""
import base64, difflib, hashlib, json
from pathlib import Path
R = Path(__file__).resolve().parent
P = R.parent / 'reil_c4e_e1_1_3_scope_v2_review_20261104'
A = Path('C:/Users/Administrator/Downloads/REIL_C4E_E1_1_3_SCOPE_v3_20261104.md')
def sha(b): return hashlib.sha256(b).hexdigest()
def put(n,b):
    p=R/n; p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f: f.write(b)
    assert p.read_bytes()==b
def writej(n,d): put(n,(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
c=json.loads((R/'SOURCE_CAPTURE.json').read_bytes())
b=base64.b64decode(c['content'])
assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==c['sha']
ab=A.read_bytes(); assert ab==b
put('input/'+A.name,ab)
put('source/bms-balancing/docs/'+A.name,b)
put('input/SCOPE_V3_NUMBERED.txt',('\n'.join(f'{i}: {s}' for i,s in enumerate(b.decode('utf-8').splitlines(),1))+'\n').encode('utf-8'))
cmp=json.loads((R/'COMPARE_FROM_V2.json').read_bytes())
assert cmp['status']=='ahead' and cmp['total_commits']==3 and len(cmp['files'])<300 and not cmp['too_large']
assert cmp['base']=='c54217a8e5f9ab53713f0c5ce26de0937935f040'
assert cmp['head']=='2621b4b21f138005c4d74b3b9f4b146c2ace7928'
changed={x['filename'] for x in cmp['files']}
prev=json.loads((P/'SOURCE_IDENTITIES.json').read_bytes())
rows=[]
for rel in ['bms-balancing/scripts/reil_c4e1_launch.py','bms-balancing/scripts/reil_c4e_run.py','bms-balancing/docs/REIL_C4E_E1_0B_APPROVAL_REQUEST_20261030.md','bms-balancing/docs/REIL_C4E_E1_1_3_SCOPE_20261104.md','bms-balancing/docs/REIL_C4E_E1_1_3_SCOPE_v2_20261104.md']:
    assert rel not in changed
    raw=(P/'source'/rel).read_bytes()
    row=prev['attachment'] if rel.endswith('SCOPE_v2_20261104.md') else next(x for x in prev['reused_sources'] if x['path']==rel)
    assert len(raw)==row['bytes'] and sha(raw)==row['sha256']
    put('source/'+rel,raw)
    rows.append({'path':rel,'bytes':len(raw),'sha256':sha(raw),'provenance':'Prior reviewed raw copy; same path unchanged in complete pinned comparison from v2.'})
for n in ['CODEX_REPLY_KO.txt','REVIEW_DECISION.json','SOURCE_IDENTITIES.json','DELIVERY_RECEIPT.json','PACKAGE_TOOL_RETURN.json']:
    put('basis/V2_'+n,(P/n).read_bytes())
old=(P/'input/REIL_C4E_E1_1_3_SCOPE_v2_20261104.md').read_text(encoding='utf-8').splitlines()
put('V2_TO_V3_TEXT_DIFF.txt',('\n'.join(difflib.unified_diff(old,b.decode('utf-8').splitlines(),fromfile='v2',tofile='v3',lineterm=''))+'\n').encode('utf-8'))
writej('SOURCE_IDENTITIES.json',{'pin':cmp['head'],'attachment':{'path':str(A),'bytes':len(ab),'sha256':sha(ab)},'repository_blob_sha1':c['sha'],'attachment_equals_pinned_repository_bytes':True,'reused_sources':rows,'received_program_execution':0,'probe_execution':0,'scope':'Static local attachment and saved source identity / complete pinned commit difference only. No remote runtime observation.'})
print(json.dumps({'attachment_bytes':len(ab),'attachment_sha256':sha(ab),'attachment_equals_pinned_repo':True,'unchanged_source_paths':len(rows),'received_program_execution':0}))
