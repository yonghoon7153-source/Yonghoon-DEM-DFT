"""Package only reviewer-created artifacts; no subject program execution."""
from pathlib import Path, PurePosixPath
import hashlib,json,stat,subprocess,zipfile
from datetime import datetime,timezone
O=Path(__file__).resolve().parent
W=Path('C:/Users/Administrator/Documents/Codex/g79_20260928')
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(p,o):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
head=subprocess.check_output(['git','-C',str(W),'rev-parse','HEAD']).decode().strip()
status=subprocess.check_output(['git','-C',str(W),'status','--porcelain=v1','-uall']).decode()
assert head=='b0203d1090b2659c31f8eb6f55e5a144657e9052' and not status
before=json.loads((O/'SOURCE_BEFORE.json').read_text(encoding='utf-8'))
changed=[p for p,i in before.items() if ident((W/p).read_bytes())!=i]
assert not changed
write(O/'SOURCE_AFTER_CHECK.json',{'head':head,'git_status_clean':True,'files_compared':len(before),'changed':changed,
 'scope':'Tracked degradation-degeneracy bytes in isolated review checkout; no all-remote-state claim'})
decision=json.loads((O/'DECISION.json').read_text(encoding='utf-8'))
assert decision['P1_count']==0 and decision['P2_count']==1
assert decision['stage3_authorized'] is False and decision['execution_go']=='NOT_REQUESTED_NOT_GRANTED'
for p in O.rglob('*.json'):json.loads(p.read_text(encoding='utf-8'))
for n in ['REVIEW_KO.md','CLAUDE_REPLY.md']:
    text=(O/n).read_text(encoding='utf-8')
    assert '\ufffd' not in text and 'G79-N1' in text and 'G78-N1' in text and 'G78-N2' in text
payload={p.relative_to(O).as_posix():ident(p.read_bytes()) for p in sorted(O.rglob('*')) if p.is_file()}
assert 'MANIFEST.json' not in payload and not any(n.endswith('.zip') for n in payload)
write(O/'MANIFEST.json',{'schema':'review-payload-manifest/v1','scope':'Reviewer data/static evidence only; no execution authorization','files':payload})
zpath=O/'GATE79_REVIEW_20260928.zip'
with zipfile.ZipFile(zpath,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for n in [*payload,'MANIFEST.json']:z.write(O/n,n)
with zipfile.ZipFile(zpath) as z:
    names=z.namelist();assert set(names)==set(payload)|{'MANIFEST.json'}
    assert len(names)==len(set(n.casefold() for n in names)) and z.testzip() is None
    for n in names:
        p=PurePosixPath(n)
        assert not p.is_absolute() and '..' not in p.parts and '\\' not in n and ':' not in n
        assert not stat.S_ISLNK(z.getinfo(n).external_attr>>16)
        if n in payload:assert ident(z.read(n))==payload[n]
    assert z.read('MANIFEST.json')==(O/'MANIFEST.json').read_bytes()
receipt={'created_utc':datetime.now(timezone.utc).isoformat(),'package':{'file':zpath.name,**ident(zpath.read_bytes())},
 'payload_count':len(payload),'manifest':ident((O/'MANIFEST.json').read_bytes()),
 'exact_set_size_sha_crc_path_case_link_verified':True,'tracked_source_unchanged':len(before),
 'decision':decision['status'],'P1':0,'P2':1,'recipient':None,
 'scope':'Generation receipt, outside ZIP to avoid self-reference; not sender test execution or execution GO.'}
write(O/'DELIVERY_RECEIPT.json',receipt)
print(json.dumps({'status':'REVIEW_PACKAGE_VERIFIED',**receipt},ensure_ascii=False))
