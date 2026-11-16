#!/usr/bin/env python3
"""Author-run ibb E0 controller. Existing approved submit/job-start bytes are unchanged.

Exactly one E0 attempt. No cancellation, requeue, resume, reservation release or
next-wave action. --collect can only inspect/collect the existing attempt.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import runpy
import shutil
import subprocess
import sys
import tarfile
import time

CASE='PRECAL_E0'
F8='docs/reviews/mixer_first8_launch_preparation_20261106'
WALLTIME='1-00:00:00'
FREE_BYTES=32193231348
FREE_INODES=1261
MAX_BYTES=29266573952
WATCH_LIMIT_SECONDS=90000  # Controller only; Slurm walltime remains 24 h.
ACTIVE={'RUNNING','PENDING','CONFIGURING','COMPLETING','SUSPENDED','RESIZING','REQUEUED','REQUEUE_FED','SIGNALING','STAGE_OUT'}
TERMINAL={'COMPLETED','FAILED','CANCELLED','TIMEOUT','OUT_OF_MEMORY','NODE_FAIL','PREEMPTED','BOOT_FAIL','DEADLINE','REVOKED','SPECIAL_EXIT'}

def need(ok,why):
    if not ok:raise ValueError(why)

def sha(p):
    p=Path(p);before=p.stat();h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    after=p.stat()
    need((before.st_size,before.st_mtime_ns,before.st_ino)==(after.st_size,after.st_mtime_ns,after.st_ino),'file changed while hashing')
    return h.hexdigest()

def put(p,v):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf-8') as f:
        json.dump(v,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')

def read(p):return json.loads(Path(p).read_bytes())
def ref(p):return {'path':str(Path(p).resolve()),'sha256':sha(p)}
def safe_rel(s):
    p=PurePosixPath(s)
    need(not p.is_absolute() and '..' not in p.parts and '\\' not in s and p.parts,'unsafe relative path')
    return p

def queue_counts(text):
    cpus=first8=0
    for line in text.splitlines():
        if not line.strip():continue
        row=line.split('|');need(len(row)==7 and row[3].isdigit(),'unparsed squeue row')
        need(row[2] in ACTIVE,'unknown live scheduler state')
        cpus+=int(row[3])
        first8+=int('PRECAL_' in row[6] or row[1].lower().startswith(('first8','precal','mixer_e0')))
    return cpus,first8

def storage_ok(df,di,ost):
    def available(text):
        rows=[l.split() for l in text.splitlines()[1:] if l.strip()]
        need(len(rows)==1 and len(rows[0])>=6 and rows[0][3].isdigit(),'df not parsed')
        return int(rows[0][3])
    b,i=available(df),available(di)
    vals=[]
    for line in ost.splitlines():
        if 'OST' not in line:continue
        c=line.split();need(len(c)>=5 and c[3].isdigit(),'OST row not parsed');vals.append(int(c[3])*1024)
    need(vals and b>=FREE_BYTES and min(vals)>=FREE_BYTES and i>=FREE_INODES,'storage/OST floor not met or unknown')
    return dict(disk_budget_verified=True,inode_budget_verified=True,free_bytes=b,free_inodes=i,minimum_ost_free_bytes=min(vals),user_quota_limit='UNKNOWN')

def wall_seconds(token):
    if token in ('INFINITE','UNLIMITED'):return float('inf')
    days,clock=(token.split('-',1) if '-' in token else ('0',token))
    parts=clock.split(':');need(days.isdigit() and len(parts)==3 and all(x.isdigit() for x in parts),'unknown wall limit')
    return int(days)*86400+int(parts[0])*3600+int(parts[1])*60+int(parts[2])

def scheduler_ok(qos,assoc,partition,user):
    rows=[l.split('|') for l in qos.splitlines() if l.strip()]
    need(len(rows)==1 and rows[0][0]=='cpu-60' and re.search(r'(^|,)cpu=60(,|$)',rows[0][1]),'QoS CPU60 not confirmed')
    eligible=[l.split('|') for l in assoc.splitlines() if l.strip()]
    need(any(len(r)>=3 and r[0]==user and 'cpu-60' in r[1].split(',') and wall_seconds(r[2])>=86400 for r in eligible),'association/time not confirmed')
    p=dict(re.findall(r'(\w+)=([^\s]+)',partition))
    need(p.get('State')=='UP' and wall_seconds(p.get('MaxTime',''))>=86400,'partition/time not confirmed')

def package_rows(prefix,meta,reference):
    need(sha(meta)==reference['json_sha256_or_reason'],'conda metadata identity')
    names=read(meta)['files'];expected=reference['files']
    need(len(names)==len(expected),'conda file count')
    rows=[];mismatch=[]
    for index,(name,want) in enumerate(zip(names,expected),1):
        need(index==want[0],'reference package order')
        p=prefix/safe_rel(name);kind='l' if p.is_symlink() else 'f'
        raw=p.resolve(strict=True);st=raw.stat();digest=sha(raw)
        row=dict(index=index,path=name,kind=kind,bytes=st.st_size,mtime=st.st_mtime,sha256=digest,expected_sha256=want[6])
        rows.append(row)
        if kind!=want[1] or st.st_size!=int(want[4]) or digest!=want[6]:mismatch.append(row)
    return rows,mismatch

def progress(state,status,now,steps,start):
    maximum=max(steps) if steps else None
    if maximum is not None and maximum!=state.get('max_step'):
        state.update(max_step=maximum,first_seen=now)
    anchor=state.get('first_seen',start)
    return status=='RUNNING' and anchor is not None and now-anchor>1800

def log_flags(text):
    flags=dict(error=0,quota=0,nonfinite=0,lost=0,last_step=None,last_atoms=None,initial_atoms=None)
    active=False
    for line in text.splitlines():
        flags['error']+=int(line.startswith('ERROR'))
        flags['quota']+=int('disk quota exceeded' in line.lower())
        c=line.split()
        if c[:2]==['Step','Atoms']:active=True;continue
        if line.startswith('Loop time'):active=False;continue
        if not active or len(c)!=5 or re.fullmatch(r'\d+',c[0]) is None:continue
        try:values=[float(v) for v in c]
        except ValueError:continue
        if not all(math.isfinite(v) for v in values):flags['nonfinite']+=1
        step=int(c[0])
        if not math.isfinite(values[1]) or not values[1].is_integer():continue
        atoms=int(values[1]);flags.update(last_step=step,last_atoms=atoms)
        if step==1 and flags['initial_atoms'] is None:flags['initial_atoms']=atoms
        if flags['initial_atoms'] is not None and atoms<flags['initial_atoms']:flags['lost']+=1
    return flags

def terminal(text,jid):
    rows=[l.split('|') for l in text.splitlines() if l.split('|')[0]==jid]
    if len(rows)!=1 or len(rows[0])<3:return None
    r=rows[0];state=r[1].split()[0].rstrip('+')
    return dict(job_id=jid,state=state,exit_code=r[2],raw=r) if len(r)>=3 and state in TERMINAL else None

def policy(install,authority_sha):
    return dict(schema='mixer_first8_campaign/1',campaign_id='mixer_precal_first8_20261106',execution_authorized=True,install_root=install,max_concurrency=1,np=20,cpu_cap=60,author_go_sha256=authority_sha)

def author_scope(root,manifest):
    go=read(root/'control/author_go.json')
    need(go.get('schema')=='mixer_e0_author_go/1' and go.get('execution_authorized') is True
         and go.get('author_action')=='GO_E0_ONCE' and go.get('allowed_to_submit')==[CASE]
         and go.get('label')=='DEVELOPMENT_DATA_ONLY','explicit author E0 GO missing')
    need(go.get('approved_B_manifest_sha256')==sha(root/'B_manifest.json')
         and go.get('approved_reseal_return_sha256')==manifest.get('approved_return_sha256')
         and go.get('pilot_controller_sha256')==sha(__file__),'author GO source binding')
    return go

def inventory(root):
    result=[]
    for p in sorted(root.rglob('*')):
        need(not p.is_symlink(),'linked collection member')
        if p.is_file():
            st=p.stat();result.append(dict(path=p.relative_to(root).as_posix(),bytes=st.st_size,mtime=st.st_mtime,sha256=sha(p)))
        else:need(p.is_dir(),'nonregular collection member')
    return result

def command(argv,timeout=60):
    r=subprocess.run(list(map(str,argv)),stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding='utf-8',errors='replace',timeout=timeout)
    return r

def capture(folder,label,argv,timeout=60):
    start=time.time();r=command(argv,timeout)
    folder.mkdir(parents=True,exist_ok=True)
    out=folder/(label+'.stdout');err=folder/(label+'.stderr')
    out.write_text(r.stdout,encoding='utf-8');err.write_text(r.stderr,encoding='utf-8')
    rec=dict(argv=list(map(str,argv)),rc=r.returncode,captured_unix=start,finished_unix=time.time(),stdout=ref(out),stderr=ref(err))
    put(folder/(label+'.receipt.json'),rec)
    need(r.returncode==0,'command failed: '+label)
    return r.stdout,rec

def runtime(root,binary,mpi,prefix,label):
    expected=read(root/'control/runtime_reference.json');folder=root/'evidence'/label
    ldd,_=capture(folder,'ldd',['ldd',str(binary)])
    paths={}
    for line in ldd.splitlines():
        c=line.split()
        if not c or c[0]=='linux-vdso.so.1':continue
        if len(c)>=3 and c[1]=='=>' and c[2].startswith('/'):paths[c[0]]=Path(c[2])
        elif c[0].startswith('/'):paths[Path(c[0]).name]=Path(c[0])
        else:raise ValueError('unresolved ldd entry')
    errors=[];rows=[]
    need(set(paths)==set(expected['libraries']),'linked library set changed')
    for name,p in [('binary',binary),('mpi',mpi),*sorted(paths.items())]:
        want=expected.get(name+'_sha256',expected['libraries'].get(name));real=p.resolve(strict=True)
        row=dict(name=name,path=str(real),sha256=sha(real),expected_sha256=want,mtime=real.stat().st_mtime)
        rows.append(row)
        if row['sha256']!=want:errors.append(row)
    packages=[]
    for pkg in expected['packages']:
        rows2,bad=package_rows(prefix,prefix/'conda-meta'/pkg['json'],pkg)
        packages.append(dict(name=pkg['name'],files=rows2));errors.extend(bad)
    report=dict(collected_unix=time.time(),matches=not errors,linked=rows,packages=packages,mismatches=errors)
    put(folder/'runtime.json',report)
    return report

def preflight(root,binary,mpi,prefix):
    r=runtime(root,binary,mpi,prefix,'runtime_pre');need(r['matches'],'runtime identity mismatch')
    user=os.environ['USER'];folder=root/'evidence/scheduler_pre'
    qos,_=capture(folder,'qos',['sacctmgr','-n','-P','show','qos','cpu-60','format=Name,MaxTRESPU'])
    assoc,_=capture(folder,'assoc',['sacctmgr','-n','-P','show','assoc','user='+user,'format=User,QOS,MaxWall'])
    part,_=capture(folder,'partition',['scontrol','show','partition','cpu','-o'])
    scheduler_ok(qos,assoc,part,user)
    folder=root/'evidence/live_preflight_0';first=time.time();raw={};receipts={}
    calls=[('queue',['squeue','-h','-u',user,'-o','%i|%j|%T|%C|%q|%P|%Z']),('df',['df','-PB1',str(root)]),('inode',['df','-Pi',str(root)]),('ost',['lfs','df',str(root)]),('quota',['lfs','quota','-u',user,str(root)])]
    for name,argv in calls:raw[name],receipts[name]=capture(folder,name,argv,10)
    need(time.time()-first<=10,'preflight ten-second window exceeded; no automatic retry')
    used,first8=queue_counts(raw['queue']);storage=storage_ok(raw['df'],raw['inode'],raw['ost'])
    need(used+20<=60 and first8==0,'CPU/concurrency budget')
    need(not re.search(r'\d+\*',raw['quota']),'quota exceeded marker')
    live=dict(observed_unix=first,qos='cpu-60',partition='cpu',qos_verified=True,d07_finished=True,
              d07_basis='author-accepted historical completion: job 338349; baseline_table section 0-A',
              paths_verified=True,reserved_cpus=used,running_first8=first8,qualification_accepted=False,
              cpu_count_rule='all listed active user jobs, including pending/completing, conservatively summed',raw_outputs=receipts,**storage)
    put(root/'evidence/live_preflight.json',live)
    return live

def verify_deployment(root):
    b=root/'B';manifest=read(root/'B_manifest.json')
    want={r['path'] for r in manifest['files']};actual={p.relative_to(b).as_posix() for p in b.rglob('*') if p.is_file()}
    need(actual==want,'B deployment member set')
    need(not any(p.is_symlink() for p in b.rglob('*')),'B link')
    for r in manifest['files']:
        p=b/safe_rel(r['path']);need(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'B deployment hash')
    ab=read(root/'control/AB_RECEIPT.json')
    need(ab['status']=='AB_READY_FOR_AUTHOR_REVIEW' and len(ab['checks'])==12 and all(r['rc']==r['expected_rc'] for r in ab['checks']),'AB receipt')
    need(ab['source_pin']==manifest['source_pin'],'AB pin')
    return manifest

def prepare_approval(root,manifest,binary,mpi):
    b=root/'B';here=b/F8
    need(read(here/'source_seal.json')['source_pin']==manifest['source_pin'],'B source pin differs')
    case=here/'cases'/CASE;case.mkdir(parents=True)
    for name in ('in.mixer','deck_meta.json','Drum.stl','Front.stl','Back.stl'):shutil.copyfile(here/'planned_assets'/CASE/name,case/name)
    folder=here/'approvals'/CASE;folder.mkdir(parents=True)
    authority=root/'control/author_go.json';go=read(authority)
    need(go['allowed_to_submit']==[CASE] and go['execution_authorized'] is True,'author scope')
    put(here/'campaign_policy.json',policy(str(here),sha(authority)))
    put(folder/'policy.json',dict(execution_authorized=True,policy_id='E0_PILOT_ONE_20261116',allowed_to_submit=[CASE]))
    put(folder/'qualification.json',dict(gate='QUALIFICATION_PILOT_GO',purpose='first E0 qualification pilot after approved AB; completed physical qualification NOT claimed',registration='mixer_e0_pilot_registration_20261113/registration_candidate.md',actual_qualification_accepted=False))
    put(folder/'mxd2r_disposition.json',dict(scope='E0 only',basis='author authorizes qualification pilot; R01 limited acceptance retained; other MXD2R and next wave not closed',next_wave_authorized=False))
    c=dict(schema='mixer_first8_execution_approval/1',execution_authorized=True,gate='QUALIFICATION_PILOT_GO',case=CASE,np=20,case_dir=str(case),
           author_choices_confirmed=True,approved_concurrency=1,wave_release=[CASE],runner_reviewed=True,walltime_approved=True,
           source_root=str(b),source_pin=manifest['source_pin'],minimum_free_bytes=FREE_BYTES,minimum_free_inodes=FREE_INODES,
           author_go=ref(authority),campaign_policy=ref(here/'campaign_policy.json'),binary=ref(binary),mpi_launcher=ref(mpi),
           qualification=ref(folder/'qualification.json'),mxd2r_disposition=ref(folder/'mxd2r_disposition.json'),policy=ref(folder/'policy.json'),live_preflight=ref(root/'evidence/live_preflight.json'))
    python=Path(sys.executable).resolve(strict=True)
    c['runner_bindings']=dict(python=str(python),job_start=str(here/'job_start.py.txt'),stdout=str(case/'slurm.stdout'),stderr=str(case/'slurm.stderr'),walltime=WALLTIME)
    ap=folder/'approval.json';ns=runpy.run_path(str(here/'submit_one.py.txt'))
    runner=folder/'runner.sbatch';runner.write_text(ns['canonical_runner'](c,str(ap)),encoding='utf-8');c['runner']=ref(runner)
    paths=[b/safe_rel(r['path']) for r in manifest['files']]+[p for p in case.iterdir() if p.is_file()]+[python,Path(__file__).resolve(),root/'control/runtime_reference.json',root/'control/AB_RECEIPT.json',root/'B_manifest.json']
    rows={str(p.resolve()):ref(p) for p in paths};put(folder/'source_manifest.json',{'files':list(rows.values())});c['source_manifest']=ref(folder/'source_manifest.json')
    put(ap,c);return ap,case

def watch_row(root,case,jid,status,state):
    now=time.time();post=case/'post';steps=[];size=0;latest=None;count=0
    for name in ('post','restart'):
        folder=case/name
        if not folder.exists():continue
        for p in folder.iterdir():
            need(p.is_file() and not p.is_symlink(),'unrecognized output entry')
            st=p.stat();size+=st.st_size
            if name=='post':
                count+=1;latest=max(latest or st.st_mtime,st.st_mtime)
                hit=re.fullmatch(r'mix_(\d+)\.liggghts',p.name)
                if hit:steps.append(int(hit[1]))
    start=read(case/'job_start.json')['start_unix'] if (case/'job_start.json').exists() else None
    flags={}
    for name in ('log.liggghts','simulator.stdout','simulator.stderr'):
        p=case/name;flags[name]=log_flags(p.read_text(encoding='utf-8',errors='replace') if p.exists() else '')
    v=os.statvfs(case);free=v.f_bavail*v.f_frsize
    quota=command(['lfs','quota','-u',os.environ['USER'],str(root)],30)
    reasons=[]
    if free<FREE_BYTES:reasons.append('S2')
    if size>MAX_BYTES:reasons.append('S4')
    if progress(state,status,now,steps,start):reasons.append('S5')
    if any(r['error'] or r['nonfinite'] or r['lost'] for r in flags.values()):reasons.append('S6')
    if re.search(r'\d+\*',quota.stdout) or any(r['quota'] for r in flags.values()):reasons.append('S8')
    row=dict(unix=now,utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(now)),job=jid,state=status,max_step=max(steps) if steps else None,
             step_first_seen=state.get('first_seen'),post_latest_mtime=latest,post_files=count,post_restart_bytes=size,case_entries=sum(1 for _ in case.rglob('*')),
             free_bytes=free,free_inodes=v.f_favail,logs=flags,quota_rc=quota.returncode,quota_stdout=quota.stdout,quota_stderr=quota.stderr,stop_recommendations=reasons,automatic_cancel=False)
    with (root/'evidence/watch.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(row)+'\n')
    print('WATCH '+json.dumps({k:row[k] for k in ('utc','state','max_step','post_files','post_restart_bytes','stop_recommendations')}),flush=True)
    if reasons:print('STOP_RECOMMENDED '+','.join(reasons)+'; author command: scancel '+jid,flush=True)

def wait_job(root,case,jid):
    state={};last_watch=0;last_status=None;missing_since=None;monitor_start=time.monotonic()
    while True:
        need(time.monotonic()-monitor_start<=WATCH_LIMIT_SECONDS,'monitor budget reached; job not cancelled; author reconciliation required')
        q=command(['squeue','-h','-j',jid,'-o','%i|%T'],30);need(q.returncode==0,'squeue watch failed; no cancellation or retry')
        rows=[l.split('|') for l in q.stdout.splitlines() if l.strip()]
        need(all(len(r)==2 and r[0]==jid for r in rows),'unexpected job query')
        status=rows[0][1] if rows else 'ABSENT'
        if status!=last_status:print('JOB_STATE '+jid+' '+status,flush=True);last_status=status
        if not rows:
            text,rec=capture(root/'evidence'/('sacct_%d'%time.time_ns()),'sacct',['sacct','-n','-P','-j',jid,'--format=JobIDRaw,State,ExitCode,Elapsed,AllocCPUS,NNodes,MaxRSS'])
            terminal_row=terminal(text,jid)
            if terminal_row:
                watch_row(root,case,jid,terminal_row['state'],state)
                put(root/'evidence/scheduler_terminal.json',terminal_row)
                return terminal_row
            missing_since=missing_since or time.monotonic()
            need(time.monotonic()-missing_since<300,'terminal state unknown; preserve and use collection-only after reconciliation')
        else:missing_since=None
        if time.time()-last_watch>=600:
            watch_row(root,case,jid,status,state);last_watch=time.time()
        time.sleep(30)

def full_collection(root,case,manifest):
    rows=inventory(case);put(root/'evidence/case_inventory.json',{'files':rows,'count':len(rows),'source_mtimes':True})
    out=root/'returns';out.mkdir(exist_ok=True);tarpath=out/'e0_full_result.tar.gz';need(not tarpath.exists(),'collection already exists; no overwrite')
    v=os.statvfs(out);need(v.f_bavail*v.f_frsize>=sum(r['bytes'] for r in rows)+256*1024*1024,'collection free space')
    with tarfile.open(tarpath,'w:gz',compresslevel=1) as t:
        for r in rows:t.add(case/r['path'],arcname='run/'+r['path'],recursive=False)
        for r in manifest['files']:t.add(root/'B'/r['path'],arcname='source/'+r['path'],recursive=False)
        t.add(root/'evidence',arcname='evidence')
        t.add(root/'control',arcname='control')
    after=inventory(case);need(after==rows,'case changed during collection')
    return ref(tarpath)

def report_archive(root):
    out=root/'returns';out.mkdir(exist_ok=True);p=out/'e0_report.tar.gz';need(not p.exists(),'report already exists; no overwrite')
    with tarfile.open(p,'w:gz') as t:
        for folder in ('evidence','control'):
            if (root/folder).exists():t.add(root/folder,arcname=folder)
        case=root/'B'/F8/'cases'/CASE
        if case.exists():
            for x in case.iterdir():
                if x.is_file() and not x.is_symlink():t.add(x,arcname='run/'+x.name,recursive=False)
        admission=root/'B'/F8/'admission'
        if admission.exists():t.add(admission,arcname='admission')
        approvals=root/'B'/F8/'approvals'
        if approvals.exists():t.add(approvals,arcname='approvals')
    return ref(p)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,required=True);ap.add_argument('--binary',type=Path,required=True)
    ap.add_argument('--mpi',type=Path,required=True);ap.add_argument('--env-prefix',type=Path,required=True)
    ap.add_argument('--collect',action='store_true');a=ap.parse_args()
    root=a.root.resolve(strict=True);binary=a.binary.resolve(strict=True);mpi=a.mpi.resolve(strict=True);prefix=a.env_prefix.resolve(strict=True)
    need(sys.platform.startswith('linux'),'author Linux host only')
    need(not any(k.startswith(('SBATCH_','SLURM_','SALLOC_','SRUN_')) for k in os.environ),'inherited scheduler options/allocation')
    env={k:os.environ[k] for k in ('PATH','HOME','USER','LOGNAME','LANG','LC_ALL','TMPDIR') if k in os.environ}
    os.environ.clear();os.environ.update(env)
    (root/'evidence').mkdir(exist_ok=True);final=dict(scope='E0_ONLY',label='DEVELOPMENT_DATA_ONLY',physical_qualification_accepted=False,automatic_retry=False);rc=2
    try:
        manifest=read(root/'B_manifest.json');case=root/'B'/F8/'cases'/CASE
        author_scope(root,manifest)
        if not a.collect:
            verify_deployment(root)
            preflight(root,binary,mpi,prefix)
            approval,case=prepare_approval(root,manifest,binary,mpi)
            r=command([sys.executable,'-I','-X','utf8','-B',str(root/'B'/F8/'submit_one.py.txt'),str(approval)],90)
            (root/'evidence/submit.stdout').write_text(r.stdout,encoding='utf-8');(root/'evidence/submit.stderr').write_text(r.stderr,encoding='utf-8')
            put(root/'evidence/submission_timing.json',dict(submit_rc=r.returncode,received_unix=time.time()))
            print('SUBMIT_RC='+str(r.returncode),flush=True);print(r.stdout+r.stderr,flush=True)
            need(r.returncode==0,'submission rejected/ambiguous; never resubmit')
        receipt=read(case/'submission.receipt.json');need(receipt['state']=='SUBMITTED' and str(receipt['job_id']).isdigit(),'no confirmed job')
        jid=str(receipt['job_id']);final['job_id']=jid
        print('JOB_ID='+jid+'; exact author stop command: scancel '+jid,flush=True)
        terminal_row=wait_job(root,case,jid)
        try:post=runtime(root,binary,mpi,prefix,'runtime_T9');final['runtime_post_matches']=post['matches']
        except Exception as e:final['runtime_post_matches']=None;final['runtime_post_error']=str(e)
        end=read(case/'job_end.json') if (case/'job_end.json').is_file() else None
        final.update(scheduler=terminal_row,runner_rc=end.get('returncode') if end else None,job_end_present=end is not None)
        print('RUNNER_RC='+str(final['runner_rc'])+' SCHEDULER_STATE='+terminal_row['state'],flush=True)
        final['full_archive']=full_collection(root,case,manifest)
        final['state']='COLLECTED_REQUIRES_QUALIFICATION'
        rc=0 if final['runner_rc']==0 and terminal_row['state']=='COMPLETED' and terminal_row['exit_code']=='0:0' else 1
    except Exception as e:
        final.update(state='INCOMPLETE',error=str(e));print('STOP: '+str(e),flush=True)
    finally:
        put(root/'evidence'/('controller_%d.json'%time.time_ns()),final)
        report=report_archive(root)
        lines=[report]+([final['full_archive']] if final.get('full_archive') else [])
        with (root/'returns/SHA256SUMS').open('x',encoding='ascii') as f:
            for item in lines:f.write(item['sha256']+'  '+Path(item['path']).name+'\n')
        print('COLLECTION_RC='+str(rc)+' REPORT='+report['sha256'],flush=True)
    return rc

if __name__=='__main__':raise SystemExit(main())
