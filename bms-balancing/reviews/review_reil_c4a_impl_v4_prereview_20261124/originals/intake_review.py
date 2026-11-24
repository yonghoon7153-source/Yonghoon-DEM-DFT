import base64,difflib,hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
prior=root.parent/'reil_c4a_v3_review_20261124'
def sha(b):return hashlib.sha256(b).hexdigest()
rows=[]
for r in json.loads((root/'capture/FETCHED_BASE64.json').read_text('utf-8')):
 assert r['status']=='fulfilled'
 v=r['value']; s=v['result']['structuredContent']; b=base64.b64decode(''.join(s['content'].split()),validate=True)
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==s['sha']
 p=root/'input'/Path(v['path']).name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 rows.append({'repository_path':v['path'],'local_path':p.relative_to(root).as_posix(),'bytes':len(b),'sha256':sha(b),'git_blob_sha':s['sha']})
attach=Path('C:/Users/Administrator/Downloads/REIL_C4A_v4_SEND_READY.txt');b=attach.read_bytes();(root/'input'/attach.name).write_bytes(b)
rows.append({'local_original_path':str(attach),'local_path':'input/'+attach.name,'bytes':len(b),'sha256':sha(b)})
v3=(root/'input/REIL_C4A_IMPL_REQUEST_v3_20261124.md').read_bytes();assert v3==(prior/'input/REIL_C4A_IMPL_REQUEST_v3_20261124.md').read_bytes()
v4=(root/'input/REIL_C4A_IMPL_REQUEST_v4_20261124.md').read_bytes();assert len(v4)==105784 and sha(v4)=='85e148b41840a0d3d98eb08ec0adae7e8b39f64bc5d3c44d2165723b9da74db2'
old=(prior/'source/bms-balancing/docs/REIL_PREREQUISITES_STATUS_20261004.md').read_bytes();new=(root/'input/REIL_PREREQUISITES_STATUS_20261004.md').read_bytes()
a=v3.decode().splitlines(keepends=True);b=v4.decode().splitlines(keepends=True)
ops=[{'kind':tag,'v3_lines':[i+1,j],'v4_lines':[k+1,l],'before':''.join(a[i:j]),'after':''.join(b[k:l])} for tag,i,j,k,l in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes() if tag!='equal']
(root/'V3_V4_DIFF.txt').write_text(''.join(difflib.unified_diff(a,b,fromfile='v3',tofile='v4')),encoding='utf-8')
(root/'CHANGE_MAP.json').write_text(json.dumps(ops,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
out={'kind':'V4_STATIC_INTAKE','files':rows,'v3_preserved':True,'ledger_prior_exact_prefix':new.startswith(old),'changed_hunks':len(ops),'line_ending_normalization':False,'target_execution':0,'pytest_collection':0}
(root/'INTAKE.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k!='files'},ensure_ascii=False))
print((root/'V3_V4_DIFF.txt').read_text('utf-8'))
