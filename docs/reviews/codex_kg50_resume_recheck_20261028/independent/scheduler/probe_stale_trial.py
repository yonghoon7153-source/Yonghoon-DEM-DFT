from pathlib import Path
import os,sys,importlib.util,json,subprocess,hashlib,shutil
R=Path(__file__).resolve().parents[2];out=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('author_test',R/'repo/scripts/test_resume_ckpt.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
script=R/'repo/scripts/resume_ckpt.sh';bash=Path('C:/Program Files/Git/bin/bash.exe') if os.name=='nt' else Path(shutil.which('bash') or '/bin/bash')
def pos(p):
 s=Path(p).resolve().as_posix();return '/'+s[0].lower()+s[2:] if os.name=='nt' else s
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(s.encode('utf-8'));os.chmod(p,0o755)
results=[]
for scenario in ['busy_queue','queue_query_failure']:
 root=out/scenario;root.mkdir(exist_ok=True);work=root/m.C;stopped=root/(m.C+'.'+m.SUF);bindir=root/'fakebin';bindir.mkdir(exist_ok=True)
 for p in [work,stopped,root/'logs',work/('post_'+m.C),stopped/('post_'+m.C)]:p.mkdir(exist_ok=True)
 write(stopped/'log.liggghts',m.ORIG_LOG);write(work/('log.liggghts.'+m.SUF),m.ORIG_LOG)
 write(work/('job_'+m.SFX+'t.txt'),'7001\n')
 write(work/('mode_'+m.SFX+'.txt'),'settling 20001 '+m.CKPT+' 22001\n')
 write(root/'logs'/('output_'+m.C+'_'+m.SFX+'t_7001.out'),m.trial_log('ok'))
 for name in ['tp_'+m.SFX+'.txt','fixrun_'+m.SFX+'.txt','deckcheck_'+m.SFX+'.txt']:write(work/name,'OLD PREEXISTING ARTIFACT\n')
 write(work/('run_'+m.C+'_'+m.SFX+'.sh'),'#!/bin/sh\n# old prior invocation runner; never execute\n')
 capture=root/'sbatch_calls.txt';capture.write_text('',encoding='utf-8')
 write(bindir/'sbatch','#!/bin/sh\nprintf "%s\\n" "$*" >> "'+pos(capture)+'"\necho 9001\n')
 write(bindir/'sacct','#!/bin/sh\nprintf "COMPLETED|0:0\\n"\n')
 sq='#!/bin/sh\nfor a in "$@"; do [ "$a" = "-j" ] && exit 0; done\n'
 sq+=('echo '+m.C+'\nexit 0\n') if scenario=='busy_queue' else 'exit 1\n'
 write(bindir/'squeue',sq);write(bindir/'sleep','#!/bin/sh\nexit 0\n')
 wrapper=root/'run_probe.sh';write(wrapper,'#!/bin/bash\nexport PATH="'+pos(bindir)+':/usr/bin:/bin"\nexport USER=synthetic-review\nbash "'+pos(script)+'" -n 56 -s '+m.SUF+' -r "'+pos(root)+'" '+m.C+'\n')
 p=subprocess.run([str(bash),pos(wrapper)],capture_output=True,timeout=30)
 (root/'stdout.log').write_bytes(p.stdout);(root/'stderr.log').write_bytes(p.stderr)
 calls=capture.read_text();res={'scenario':scenario,'returncode':p.returncode,'sbatch_calls':calls.splitlines(),'trial_submitted_in_this_invocation':False,'preexisting_trial_job':7001,'main_submitted':bool(calls),'stdout':p.stdout.decode('utf-8',errors='replace')}
 res['execution_status']='NOT_EXECUTED_BASH_RUNTIME_BLOCKED' if p.returncode==3221225794 else 'EXECUTED'
 results.append(res)
 print(json.dumps({k:v for k,v in res.items() if k!='stdout'},ensure_ascii=False))
 if res['execution_status']=='EXECUTED':
  assert calls and ('_r56.sh' in calls) and ('_r56t.sh' not in calls)
  assert '건너뜀' in res['stdout'] and '본 제출 job 9001' in res['stdout']
(out/'stale_trial_results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
