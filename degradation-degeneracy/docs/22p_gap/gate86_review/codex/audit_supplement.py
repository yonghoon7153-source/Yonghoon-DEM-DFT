"""Read-only review of appended fixed-commit log evidence; no submitted scripts run."""
import hashlib
import json
import re
from pathlib import Path

H=Path(__file__).resolve().parent
E=H/'supplement_evidence'
R=H/'supplement_reference'
REF='92c50f9035db79143f7f5aca65072b3adffdee26'
HEAD='27bfeed68ea516e5c5a50f2475c8cc2b4f80ff3b'
checks=[]
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(b): return hashlib.sha256(b).hexdigest()
def check(n,v):
    checks.append({'check':n,'pass':bool(v)})
    assert v,n
def rows(t): return {r[0]:(int(r[1]),r[2]) for r in re.findall(r'\| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|',t)}
files={}
for p in sorted(E.glob('*.json')):
    d=read(p)
    if 'sha' not in d: continue
    b=d['content'].encode('utf-8')
    blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    check('Git blob '+p.name,blob==d['sha'])
    check('Fixed ref '+p.name,'/'+REF+'/' in d['display_url'])
    R.mkdir(exist_ok=True)
    name=p.name[:-5]
    (R/name).write_bytes(b)
    files[name]={'bytes':len(b),'sha256':sha(b),'git_blob_sha1':blob,'url':d['display_url']}
table=rows((R/'README.md').read_text(encoding='utf-8'))
oldtable=rows((H/'reference/docs/22p_gap/gate86_evidence/README.md').read_text(encoding='utf-8'))
check('17 payload rows',len(table)==17)
for k,v in oldtable.items(): check('Prior identity retained '+k,table[k]==v)
for k,v in table.items():
    if k.startswith('request_commit_27bfeed6/'):
        n=Path(k).name
        check('Size '+n,files[n]['bytes']==v[0])
        check('Full SHA '+n,files[n]['sha256']==v[1])
c=read(E/'COMPARE.json')
check('Single forward evidence commit',c['behind_by']==0 and c['ahead_by']==1 and not c.get('too_large'))
check('Only evidence tree changed',all(x['filename'].startswith('degradation-degeneracy/docs/22p_gap/gate86_evidence/') for x in c['files']))
log=(R/'g86_send.log').read_text(encoding='utf-8')
test=(R/'g86_send_pytest.txt').read_text(encoding='utf-8')
smoke=(R/'g86_send_smoke.txt').read_text(encoding='utf-8')
check('Same clean head before/after',all(s in log for s in ['START_HEAD='+HEAD+' status=0','END_HEAD='+HEAD+' status=0']))
check('Outer rc retained',all(s in log for s in ['pytest rc=0','smoke rc=0 168s']))
check('Current digest observed','source_digest f1f4378f46610f08' in log)
check('Full test result','2046 passed, 1 xfailed in 3543.27s' in log and '2046 passed, 1 xfailed in 3543.27s' in test)
check('No failed summary',not re.search(r'\d+ failed|^FAILED ',test,re.M))
check('Expected xfail name','test_staging_an_input_outside_the_repo_is_still_unsupported' in test)
check('Smoke completion text','pipeline smoke 통과' in smoke)
first=(R/'g86_send.interrupted.log').read_text(encoding='utf-8')
check('First interrupted attempt start only',len(first.splitlines())==1 and '22:32:40Z' in first)
obj={'pass':True,'checks':checks,'files':files,'source_commit':REF,'execution_head':HEAD,'received_scripts_executed':0,'last_full_suite':'SOURCE_RAW_LOG_VERIFIED_NOT_REEXECUTED','pytest':{'passed':2046,'xfailed':1,'failed':0,'seconds':3543.27,'rc':0},'smoke':{'rc':0,'seconds':168},'limits':['First interrupted pytest partial output was overwritten per README. Only its start marker survives.','Runtime source logs are sender evidence, not independent remote OS observation.','352 full mutation replay remains at 0be169b1; no claim of full replay at 27bfeed6.']}
(H/'SUPPLEMENT_AUDIT.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'FINAL_SOURCE_LOGS_VERIFIED','checks':len(checks),'files':len(files),'payloads_added':5,'pytest_passed':2046,'received_code_executions':0}))
