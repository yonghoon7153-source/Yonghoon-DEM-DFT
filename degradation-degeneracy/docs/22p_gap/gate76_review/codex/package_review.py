"""Reviewer delivery: preserve fixed checkout and verify the reopened ZIP."""
from pathlib import Path, PurePosixPath
import datetime, hashlib, json, stat, subprocess, zipfile
O=Path(__file__).resolve().parent
W=Path('C:/Users/Administrator/Documents/Codex/g76_20260927');D=W/'degradation-degeneracy'
H='b5e4eadea7794d157d961170247e49d2761bba26'
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(n,v):
    with (O/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
def git(*args):
    return subprocess.check_output(['git','-c','http.sslBackend=openssl','-c','credential.interactive=never','-C',str(W),*args])
before=json.loads((O/'SOURCE_BEFORE.json').read_bytes())
after={p:ident((W/p).read_bytes()) for p in before}
assert before==after
status=git('status','--porcelain=v1','-uall').decode();head=git('rev-parse','HEAD').decode().strip()
assert head==H and not status
write('PRESERVATION_AFTER.json',{'head':H,'checked_tracked_files':len(after),'changed':[],
 'all_bytes_size_sha_identical':True,'git_status':status,'scope':'This reviewer fixed checkout only; not remote host or process inventory'})
for name,a,b,path in [('G75_MUTATION_CHANGES','ef6689bbe296e545df57dc481e45ec98c2b9ea3b',H,'docs/22p_gap/mutation_replay.py'),
                      ('G75_TEST_EVOLUTION','10be3a69','23c361ed','tests/test_gate75_defensive.py')]:
    (O/(name+'.diff')).write_bytes(git('diff','--no-ext-diff',a,b,'--','degradation-degeneracy/'+path))
decision=json.loads((O/'DECISION.json').read_bytes());probes=json.loads((O/'DECISION_PROBES.json').read_bytes())
audit=json.loads((O/'DATA_AUDIT.json').read_bytes())
assert decision['head']==head==audit['head']==probes['head']
assert decision['source_digest']==audit['source_digest']=='1c67a748598baadb'
assert decision['isolated_unique_cases']==probes['case_count']==len(probes['cases'])==44
assert len({c['id'] for c in probes['cases']})==44
assert not decision['blocking_findings'] and not decision['new_execution_GO']
assert all(v.startswith('CLOSED_ACCEPTED') for v in decision['items'].values())
assert audit['registry_count']==369 and audit['tracked_files']==len(after)==2868
for name in ('GATE76_REVIEW_KO.md','CLAUDE_REPLY_GATE76.md','REVIEWER_CHECK_HISTORY.md'):
    text=(O/name).read_text(encoding='utf-8');assert '\ufffd' not in text
excluded={'MANIFEST.json','DELIVERY_RECEIPT.json','GATE76_REVIEW_20260927.zip'}
files={p.relative_to(O).as_posix():ident(p.read_bytes()) for p in sorted(O.rglob('*'))
       if p.is_file() and p.relative_to(O).as_posix() not in excluded}
assert len(files)==len({p.casefold() for p in files})
for p in files:
    q=PurePosixPath(p);assert not q.is_absolute() and '..' not in q.parts and '\\' not in p and ':' not in p
write('MANIFEST.json',{'format':'review-payload/v1','payload_count':len(files),'files':files})
zp=O/'GATE76_REVIEW_20260927.zip'
with zipfile.ZipFile(zp,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(files):z.write(O/p,p)
    z.write(O/'MANIFEST.json','MANIFEST.json')
with zipfile.ZipFile(zp) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(set(n.casefold() for n in z.namelist()))==len(files)+1
    assert set(z.namelist())==set(files)|{'MANIFEST.json'}
    assert z.read('MANIFEST.json')==(O/'MANIFEST.json').read_bytes()
    for p,v in files.items():
        assert ident(z.read(p))==v and not stat.S_ISLNK(z.getinfo(p).external_attr>>16)
receipt={'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'scope':'Locally generated Gate76 independent review; finite closure, not new execution authorization',
 'archive':{'path':str(zp),**ident(zp.read_bytes())},'payload_count':len(files),'entries_including_manifest':len(files)+1,
 'manifest':ident((O/'MANIFEST.json').read_bytes()),'exact_set_size_SHA_CRC_verified':True,
 'duplicate_case_path_link_checks':True,'preserved_checkout_files':len(after),'decision':decision['status'],
 'blocking_findings':0,'isolated_unique_cases':44,'new_execution_GO':False,
 'whole_subject_module_imports':0,'full_subject_suite_runs':0,'scientific_runs':0,
 'archive_restore_attach_projection_or_class_changes':0,'production_edits':0,
 'reviewer_owned_scripts_and_allowlisted_predicate_execution':True,'recipient':None}
write('DELIVERY_RECEIPT.json',receipt)
print(json.dumps(receipt,ensure_ascii=False))
