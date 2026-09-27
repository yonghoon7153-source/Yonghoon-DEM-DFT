"""Reviewer-owned preservation and reopened-ZIP verification for Gate78."""
from pathlib import Path, PurePosixPath
import datetime, hashlib, json, stat, subprocess, zipfile
O=Path(__file__).resolve().parent
W=Path('C:/Users/Administrator/Documents/Codex/g78_20260927')
H='720f0a0e466afb595fbd73a50f89416898cc927c'
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(n,v):
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
decision=json.loads((O/'DECISION.json').read_bytes())
audit=json.loads((O/'DATA_AUDIT.json').read_bytes())
arithmetic=json.loads((O/'DESIGN_ARITHMETIC.json').read_bytes())
assert decision['head']==audit['head']==arithmetic['head']==H
assert decision['source_digest']==audit['source_digest']=='1c67a748598baadb'
assert len(after)==audit['tracked_files']==2995
assert audit['scope_files']==58 and audit['prior_review_package']['payload']==34
assert decision['execution_GO'] is False and decision['prior_gate76_finite_closure_maintained'] is True
assert [x['id'] for x in decision['findings']]==['G78-N1','G78-N2']
assert [x['priority'] for x in decision['findings']]==[1,1]
assert len(arithmetic['single_pair_state_table'])==arithmetic['state_table_count']==9
assert arithmetic['missing_sensitivity_counterexample']['missing_as_fail_delta_full_planned_denominator']=='-1/40'
assert arithmetic['missing_sensitivity_counterexample']['sharp_full_planned_upper']=='1/40'
assert arithmetic['pairing_counterexample']['correct_n']==2
assert arithmetic['pairing_counterexample']['incorrect_n']==4
for n in ['README.md','REVIEW_KO.md','CLAUDE_REPLY.md']:
    t=(O/n).read_text(encoding='utf-8');assert '\ufffd' not in t
    if n!='README.md':assert all(i in t for i in ['G78-N1','G78-N2'])
anchors=[('docs/22p_gap/GATE78_REQUEST.md',58,'pairing key'),
 ('docs/22p_gap/GATE78_REQUEST.md',60,'pair_group_id'),
 ('docs/22p_gap/GATE78_REQUEST.md',62,'complete-pair'),
 ('docs/22p_gap/GATE78_REQUEST.md',63,'Δ_worst'),
 ('docs/22p_gap/GATE78_REQUEST.md',111,'사용자 승인'),
 ('docs/22p_gap/GATE78_REQUEST.md',115,'복원'),
 ('docs/22p_gap/GATE78_REQUEST.md',116,'명시 포함')]
for p,line,needle in anchors:
    assert needle in (O/'reference'/p).read_text(encoding='utf-8').splitlines()[line-1],(p,line)
write('PRESERVATION_AFTER.json',{'head':H,'checked_tracked_files':len(after),'changed':[],
 'bytes_size_sha_unchanged':True,'git_status':status,
 'scope':'Fixed reviewer checkout only, not the source host or remote process/storage inventory'})
write('REPORT_QA.json',{'head':H,'decision_report_data_consistent':True,
 'residual_ids':['G78-N1','G78-N2'],'anchors_checked':[{'path':p,'line':n,'text':t} for p,n,t in anchors],
 'algebra_state_rows':9,'provided_program_execution':False,'encoding_replacement_chars':0})
name='GATE78_REVIEW_20260927.zip'
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
 'scope':'Gate78 independent design/status review; conditional scope fitness, not execution authorization',
 'archive':{'path':str(zp),**ident(zp.read_bytes())},'payload_count':len(files),'total_entries':len(files)+1,
 'manifest':ident((O/'MANIFEST.json').read_bytes()),'exact_set_size_SHA_CRC_verified':True,
 'duplicate_case_path_link_checks':True,'preserved_checkout_files':len(after),
 'closed_design_corrections':['G77-N1','G77-N3'],'residual_findings':{'P1':2,'P2':0},
 'Gate76_closure_maintained':True,'subject_imports':0,'provided_suite_runs':0,
 'scientific_COMSOL_Java_runs':0,'restore_rescore_production_edits':0,
 'reviewer_own_fabricated_algebra_only':True,'execution_GO':False,'recipient':None}
write('DELIVERY_RECEIPT.json',receipt)
print(json.dumps(receipt,ensure_ascii=False))
