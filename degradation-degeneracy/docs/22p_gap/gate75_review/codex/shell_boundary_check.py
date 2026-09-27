"""Repeat only the two reviewer shell boundary fixtures with Git utilities on PATH.
No production script or archive operations execute.
"""
from pathlib import Path
import json,os,subprocess
O=Path(__file__).resolve().parent
env=dict(os.environ)
env['PATH']='C:/Program Files/Git/usr/bin;C:/Program Files/Git/bin;'+env.get('PATH','')
results=[]
for rc in (0,17):
    p=O/'fixtures02'/f'boundary_rc{rc}.sh'
    cp=subprocess.run(['C:/Program Files/Git/bin/bash.exe','--noprofile','--norc',p.as_posix()],
        cwd=p.parent,env=env,capture_output=True,timeout=20)
    record={'injected_index_command_rc':rc,'actual_shell_exit_code':cp.returncode,
        'stdout':cp.stdout.decode('utf-8','replace'),'stderr':cp.stderr.decode('utf-8','replace')}
    results.append(record)
    assert cp.returncode==0 and not cp.stderr,record
out={'scope':'Same reviewer boundary fixtures; only process-local PATH corrected, no subject script executed',
     'results':results,'whole_archive_executions':0,'subject_files_changed':0}
with (O/'SHELL_BOUNDARY_CHECK.json').open('x',encoding='utf-8') as f:json.dump(out,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps(out,ensure_ascii=False))
