"""Finalize review artifacts, verify preserved checkout and reopen delivery ZIP."""
from pathlib import Path, PurePosixPath
import datetime,hashlib,json,subprocess,zipfile,stat
O=Path(__file__).resolve().parent
W=Path('C:/Users/Administrator/Documents/Codex/g75_20260927');D=W/'degradation-degeneracy'
H='ef6689bbe296e545df57dc481e45ec98c2b9ea3b'
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(n,v):
    with (O/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
before=json.loads((O/'SOURCE_BEFORE.json').read_bytes())
after={p:ident((W/p).read_bytes()) for p in before}
assert before==after
status=subprocess.check_output(['git','-C',str(W),'status','--porcelain=v1','-uall']).decode()
head=subprocess.check_output(['git','-C',str(W),'rev-parse','HEAD']).decode().strip()
assert head==H and not status
write('PRESERVATION_AFTER.json',{'head':H,'checked_tracked_files':len(after),'changed':[],
 'all_bytes_size_sha_identical':True,'git_status':status,'scope':'This reviewer fixed checkout only, not remote host/process inventory'})
for name in ('STAGE3_CONTRACT.md',):
    target=O/'reference/docs/22p_gap'/name;target.write_bytes((D/'docs/22p_gap'/name).read_bytes())
source=Path('C:/Users/Administrator/Downloads/SEND_GATE75_2026-09-26.md')
target=O/'receiver_inputs'/source.name;target.parent.mkdir(exist_ok=True);target.write_bytes(source.read_bytes())
write('RECEIVER_INPUTS.json',{'path':str(source),'identity':ident(source.read_bytes()),'original_modified':False})
decision=json.loads((O/'DECISION.json').read_bytes())
probes=json.loads((O/'DECISION_PROBES.json').read_bytes())
assert decision['head']==head and probes['case_count']==23
assert len([f for f in decision['findings'] if f['priority']==1])==1
assert len([f for f in decision['findings'] if f['priority']==2])==2
shell=json.loads((O/'SHELL_BOUNDARY_CHECK.json').read_bytes())
assert len(shell['results'])==2 and all(x['actual_shell_exit_code']==0 and not x['stderr'] for x in shell['results'])
excluded={'MANIFEST.json','DELIVERY_RECEIPT.json','GATE75_REVIEW_20260927.zip'}
files={p.relative_to(O).as_posix():ident(p.read_bytes()) for p in sorted(O.rglob('*'))
       if p.is_file() and p.relative_to(O).as_posix() not in excluded}
assert len(files)==len({p.casefold() for p in files})
for p in files:
    q=PurePosixPath(p);assert not q.is_absolute() and '..' not in q.parts and '\\' not in p
write('MANIFEST.json',{'format':'review-payload/v1','payload_count':len(files),'files':files})
zp=O/'GATE75_REVIEW_20260927.zip'
with zipfile.ZipFile(zp,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(files):z.write(O/p,p)
    z.write(O/'MANIFEST.json','MANIFEST.json')
with zipfile.ZipFile(zp) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(set(z.namelist()))==len(files)+1
    assert set(z.namelist())==set(files)|{'MANIFEST.json'}
    assert z.read('MANIFEST.json')==(O/'MANIFEST.json').read_bytes()
    for p,v in files.items():
        assert ident(z.read(p))==v
        assert not stat.S_ISLNK(z.getinfo(p).external_attr>>16)
receipt={'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'scope':'Locally generated Gate75 independent reviewer package; no execution authorization',
 'archive':{'path':str(zp),**ident(zp.read_bytes())},'payload_count':len(files),'entries_including_manifest':len(files)+1,
 'manifest':ident((O/'MANIFEST.json').read_bytes()),'exact_set_size_SHA_CRC_verified':True,
 'duplicate_case_path_link_checks':True,'preserved_checkout_files':len(after),'decision':decision['status'],
 'priorities':{'P1':1,'P2':2},'isolated_unique_cases':23,'shell_rechecks':2,
 'whole_subject_module_imports':0,'full_subject_suite_runs':0,'scientific_runs':0,
 'archive_restore_attach_projection_or_class_changes':0,'production_edits':0,
 'reviewer_owned_scripts_and_allowlisted_predicate_execution':True,'recipient':None}
write('DELIVERY_RECEIPT.json',receipt)
print(json.dumps(receipt,ensure_ascii=False))
