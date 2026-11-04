import base64, fnmatch, hashlib, json, shutil
from pathlib import Path
ROOT=Path(__file__).parent
PREV=ROOT.parent/'reil_c4e1_0b_a2_result_review_20261104'
attachment=Path('C:/Users/Administrator/Downloads/REIL_C4E_E1_1_3_SCOPE_20261104.md')
def digest(b):return hashlib.sha256(b).hexdigest()
def info(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':digest(b)}
def writej(name,x):(ROOT/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
cap=json.loads((ROOT/'SOURCE_CAPTURE.json').read_text(encoding='utf-8'))
rows=[]
for r in cap['files']:
 b=base64.b64decode(r['content']);blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 assert blob==r['sha'],r['path']
 p=ROOT/'source'/r['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 rows.append({'path':r['path'],'bytes':len(b),'sha256':digest(b),'git_blob_sha1':blob,'source':'fresh connector read at '+cap['pin']})
attachment_before=info(attachment)
p=ROOT/'input'/attachment.name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(attachment,p)
assert p.read_bytes()==(ROOT/'source/bms-balancing/docs'/attachment.name).read_bytes(),'Attachment differs from pinned repo'
compare=json.loads((ROOT/'COMPARE_FROM_A2_REVIEW.json').read_text(encoding='utf-8'))
changed={r['filename'] for r in compare['files']}
assert compare['status']=='ahead' and compare['total_commits']==4
oldids=json.loads((PREV/'SOURCE_IDENTITIES.json').read_text(encoding='utf-8'))
oldlookup={r['path']:r for r in oldids['fetched']}
additional=json.loads((PREV/'ADDITIONAL_IDENTITIES.json').read_text(encoding='utf-8'))
oldlookup.update({r['path']:r for r in additional['fetched']})
selected=[
 'bms-balancing/scripts/reil_c4e_run.py',
 'bms-balancing/docs/REIL_C4E_E1_0B_APPROVAL_REQUEST_20261030.md',
 'bms-balancing/evidence/reil_c4e1_0b_a2_20261104/00_start.txt',
 'bms-balancing/evidence/reil_c4e1_0b_a2_20261104/03_end.json'
]
for rel in selected:
 src=PREV/'source'/rel;b=src.read_bytes();old=oldlookup[rel]
 assert len(b)==old['bytes'] and digest(b)==old['sha256']
 assert rel not in changed
 p=ROOT/'source'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 rows.append({'path':rel,'bytes':len(b),'sha256':digest(b),'source':'prior pinned raw copy; unchanged path in complete compare '+compare['base']+'..'+compare['head']})
for n in ['CODEX_REPLY_KO.txt','REVIEW_DECISION.json']:
 p=ROOT/'basis'/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(PREV/n,p)
ex=json.loads((ROOT/'STATUS_EXCERPT_CAPTURE.json').read_text(encoding='utf-8'))
(ROOT/'source/STATUS_101_EXCERPT.txt').write_text(ex['content'],encoding='utf-8')
prior_launcher=(PREV/'source/bms-balancing/scripts/reil_c4e1_launch.py').read_bytes()
new_launcher=(ROOT/'source/bms-balancing/scripts/reil_c4e1_launch.py').read_bytes()
assert prior_launcher==new_launcher
scope=(ROOT/'input'/attachment.name).read_text(encoding='utf-8').splitlines()
(ROOT/'input/SCOPE_NUMBERED.txt').write_text('\n'.join(f'{i}: {line}' for i,line in enumerate(scope,1))+'\n',encoding='utf-8')
writej('SOURCE_IDENTITIES.json',{'pin':cap['pin'],'attachment':attachment_before,'attachment_equals_pinned_repository_bytes':True,'sources':rows,'fresh_launcher_equals_previously_accepted_v6':True,'status_excerpt_note':'API excerpt lines 2917–2960, not a raw full-file copy; reported git blob identity is retained only in STATUS_EXCERPT_CAPTURE.json.'})
writej('STATIC_LINKAGE.json',{
 'kind':'RECIPIENT_SCOPE_STATIC_DATA_REVIEW',
 'pin':cap['pin'],
 'attachment_matches_repository':True,
 'launcher_v6_unchanged':True,
 'unchanged_reused_paths':selected,
 'preserved_existing_evidence':'evidence/reil_c4e1_0b_a2_20261104',
 'broad_glob_matches_preserved_a2':fnmatch.fnmatchcase('evidence/reil_c4e1_0b_a2_20261104','evidence/reil_c4e1_*'),
 'configured_timeout_sums':{'identity':60+60+4*60+20,'fetch':300+4*60+60+4*60+20},
 'timeout_sum_is_proven_wall_clock_bound':False,
 'target_imports':0,'received_program_execution':0,'test_execution':0,'detach_probe_execution':0,
 'production_or_authoring_repository_mutations':0,
 'attachment_preserved':info(attachment)==attachment_before,
 'scope':'Text, raw hashes, comparison metadata and arithmetic only; no independent observation of remote runtime state.'
})
print(json.dumps({'scope_lines':len(scope),'source_files':len(rows),'attachment':attachment_before,'launcher_sha256':digest(new_launcher),'static_linkage':'MATCH'},ensure_ascii=False))

