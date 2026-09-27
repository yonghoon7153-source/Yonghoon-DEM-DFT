"""Reviewer-owned Gate77 closure of file preservation and delivery integrity."""
from pathlib import Path, PurePosixPath
import datetime, hashlib, json, stat, subprocess, zipfile
O=Path(__file__).resolve().parent
W=Path('C:/Users/Administrator/Documents/Codex/g77_20260927')
H='ebbcf04ed6cd4f5c2f71b4ebd28031c5fd441002'
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(n,v):
    if n=='PRESERVATION_AFTER.json' and (O/n).exists():
        assert json.loads((O/n).read_bytes())==v
        return
    with (O/n).open('x',encoding='utf-8',newline='\n') as f:
        json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
def git(*args):
    return subprocess.check_output(['git','-c','http.sslBackend=openssl','-c','credential.interactive=never','-C',str(W),*args])
before=json.loads((O/'SOURCE_BEFORE.json').read_bytes())
after={p:ident((W/p).read_bytes()) for p in before}
assert after==before
assert set(before)==set(p for p in git('ls-files','-z','--','degradation-degeneracy').decode().split('\0') if p)
status=git('status','--porcelain=v1','-uall').decode()
assert not status and git('rev-parse','HEAD').decode().strip()==H
write('PRESERVATION_AFTER.json',{'head':H,'checked_tracked_files':len(after),'changed':[],
 'bytes_size_sha_unchanged':True,'git_status':status,'scope':'Fixed reviewer checkout only, not remote host/process inventory'})
decision=json.loads((O/'DECISION.json').read_bytes())
audit=json.loads((O/'DATA_AUDIT.json').read_bytes())
assert decision['head']==audit['head']==H
assert decision['source_digest']==audit['source_digest']=='1c67a748598baadb'
assert len(after)==audit['tracked_files']==2958
assert audit['scope_files']==58 and audit['prior_package']['payload']==87
assert decision['execution_go'] is False and decision['prior_gate76_finite_scope_closed'] is True
assert [x['id'] for x in decision['findings']]==['G77-N1','G77-N2','G77-N3']
assert [x['priority'] for x in decision['findings']]==[1,1,2]
for n in ['README.md','REVIEW_KO.md','CLAUDE_REPLY.md']:
    t=(O/n).read_text(encoding='utf-8'); assert '\ufffd' not in t
    if n!='README.md':
        assert all(i in t for i in ['G77-N1','G77-N2','G77-N3'])
refs=O/'reference'
anchors=[('docs/22p_gap/GATE77_REQUEST.md',37,'실물 provider'),
 ('docs/22p_gap/GATE77_REQUEST.md',47,'완주'),
 ('docs/22p_gap/GATE77_REQUEST.md',54,'primary arm'),
 ('docs/22p_gap/GATE77_REQUEST.md',55,'pilot 전에 숫자'),
 ('docs/22p_gap/GATE77_REQUEST.md',57,'transition table'),
 ('docs/22p_gap/GATE77_REQUEST.md',65,'작고 독립'),
 ('src/fitting.py',288,'warm'),('src/fitting.py',430,'n_eval')]
for p,line,needle in anchors:
    assert needle in (refs/p).read_text(encoding='utf-8').splitlines()[line-1],(p,line)
write('REPORT_QA.json',{'head':H,'decision_report_scope_consistent':True,
 'finding_ids':['G77-N1','G77-N2','G77-N3'],'anchors_checked':[{'path':p,'line':n,'text':v} for p,n,v in anchors],
 'scientific_or_subject_test_execution':False,'encoding_replacement_chars':0})
name='GATE77_REVIEW_20260927.zip'
excluded={name,'MANIFEST.json','DELIVERY_RECEIPT.json'}
files={p.relative_to(O).as_posix():ident(p.read_bytes()) for p in sorted(O.rglob('*'))
       if p.is_file() and p.relative_to(O).as_posix() not in excluded}
assert len(files)==len({p.casefold() for p in files})
for p in files:
    q=PurePosixPath(p)
    assert not q.is_absolute() and '..' not in q.parts and '\\' not in p and ':' not in p
write('MANIFEST.json',{'format':'review-payload/v1','payload_count':len(files),'files':files})
zp=O/name
with zipfile.ZipFile(zp,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(files):z.write(O/p,p)
    z.write(O/'MANIFEST.json','MANIFEST.json')
with zipfile.ZipFile(zp) as z:
    assert z.testzip() is None
    ns=z.namelist();assert len(ns)==len(set(n.casefold() for n in ns))==len(files)+1
    assert set(ns)==set(files)|{'MANIFEST.json'}
    assert z.read('MANIFEST.json')==(O/'MANIFEST.json').read_bytes()
    for p,v in files.items():
        assert ident(z.read(p))==v and not stat.S_ISLNK(z.getinfo(p).external_attr>>16)
receipt={'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'scope':'Gate77 independent design/status review, no implementation or execution authorization',
 'archive':{'path':str(zp),**ident(zp.read_bytes())},'payload_count':len(files),'total_entries':len(files)+1,
 'manifest':ident((O/'MANIFEST.json').read_bytes()),'exact_set_size_SHA_CRC_verified':True,
 'duplicate_case_path_link_checks':True,'preserved_checkout_files':len(after),
 'findings':{'P1':2,'P2':1},'Gate76_finite_scope_closed_maintained':True,
 'subject_imports':0,'subject_suite_runs':0,'new_scientific_COMSOL_Java_runs':0,
 'restore_rescore_source_edits_projection_class_changes':0,'execution_go':False,'recipient':None}
write('DELIVERY_RECEIPT.json',receipt)
print(json.dumps(receipt,ensure_ascii=False))
