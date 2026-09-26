"""Package reviewer artifacts; verify source preservation and reopened ZIP."""
from pathlib import Path, PurePosixPath
import datetime,hashlib,json,subprocess,zipfile,stat
O=Path(__file__).resolve().parent
W=Path('C:/Users/Administrator/Documents/Codex/g74_20260926')
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(n,v):
    with (O/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
before=json.loads((O/'SOURCE_BEFORE.json').read_bytes())
after={n:ident((W/n).read_bytes()) for n in before}
assert before==after
status=subprocess.check_output(['git','-C',str(W),'status','--porcelain=v1','-uall']).decode()
assert not status
head=subprocess.check_output(['git','-C',str(W),'rev-parse','HEAD']).decode().strip()
assert head=='a49a021833282e0bd04c4565591668dc323e9630'
write('PRESERVATION_AFTER.json',{'head':head,'checked_tracked_files':len(after),'changed':[],
 'all_bytes_sha_equal':True,'git_status':status,'scope':'This fixed review checkout, not remote host inventory/processes'})
source=Path('C:/Users/Administrator/Downloads/SEND_GATE74_2026-09-26.md')
dest=O/'receiver_inputs/SEND_GATE74_2026-09-26.md';dest.parent.mkdir(exist_ok=True);dest.write_bytes(source.read_bytes())
write('RECEIVER_INPUTS.json',{'path':str(source),'identity':ident(source.read_bytes()),'original_not_modified':True})
excluded={'MANIFEST.json','DELIVERY_RECEIPT.json','GATE74_REVIEW_20260926.zip'}
files={p.relative_to(O).as_posix():ident(p.read_bytes()) for p in sorted(O.rglob('*')) if p.is_file() and p.name not in excluded}
assert len(files)==len({n.casefold() for n in files})
for n in files:
    q=PurePosixPath(n);assert not q.is_absolute() and '..' not in q.parts and '\\' not in n
write('MANIFEST.json',{'format':'review-payload/v1','payload_count':len(files),'files':files})
zpath=O/'GATE74_REVIEW_20260926.zip'
with zipfile.ZipFile(zpath,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for n in sorted(files):z.write(O/n,n)
    z.write(O/'MANIFEST.json','MANIFEST.json')
with zipfile.ZipFile(zpath) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(set(z.namelist()))==len(files)+1
    assert set(z.namelist())==set(files)|{'MANIFEST.json'}
    assert z.read('MANIFEST.json')==(O/'MANIFEST.json').read_bytes()
    for n,v in files.items():
        assert ident(z.read(n))==v
        assert not stat.S_ISLNK(z.getinfo(n).external_attr>>16)
receipt={'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'scope':'Locally generated Gate74 reviewer package; source data already reviewed, no new scientific execution',
 'archive':{'path':str(zpath),**ident(zpath.read_bytes())},'payload_count':len(files),
 'entries_including_manifest':len(files)+1,'manifest':ident((O/'MANIFEST.json').read_bytes()),
 'exact_set_size_SHA_CRC_verified':True,'duplicate_case_path_link_checks':True,'preserved_checkout_files':len(after),
 'reviewer_project_imports':0,'reviewer_scientific_runs':0,'reviewer_restore_or_class_changes':0,
 'recipient':None}
write('DELIVERY_RECEIPT.json',receipt)
print(json.dumps(receipt,ensure_ascii=False))
