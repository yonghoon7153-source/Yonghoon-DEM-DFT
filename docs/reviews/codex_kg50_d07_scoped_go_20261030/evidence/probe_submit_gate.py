"""Execute only the pinned post-trial Bash gate, with fake queue/submit functions.
No real scheduler, MPI, LIGGGHTS or WSL. Checkpoint here is explicitly FAKE.
"""
from pathlib import Path
import hashlib,json,os,subprocess,shutil
R=Path(__file__).resolve().parent;O=R/'independent/gate_probe';O.mkdir(parents=True,exist_ok=True)
tool=R/'repo/scripts/resume_ckpt.sh';txt=tool.read_text(encoding='utf-8')
start=txt.index('  if [ $G0 = 1 ] && [ $G1 = 1 ] && [ $G2 = 1 ] && [ $G3 = 1 ]; then\n')
end=txt.index('\ndone\n',start)
block=txt[start:end] # verbatim production lines 2084--2112, no edits
(O/'gate_verbatim.sh').write_bytes((block+'\n').encode())
def sh(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pos(p):
 if os.name!='nt':return str(p.resolve())
 s=str(p.resolve()).replace('\\','/');return '/'+s[0].lower()+s[2:]
def quote(s):return "'"+str(s).replace("'","'\"'\"'")+"'"
base=R/'trial/kg50_d07_b50';rows=[]
for kind in ('baseline','changed_after_trial','new_call_unreviewed_duration'):
 d=O/kind;d.mkdir(exist_ok=True);ad=d/'attempt';ad.mkdir(exist_ok=True)
 for n in ('input_kg50_d07_b50_r56.liggghts','input_kg50_d07_b50_r56t.liggghts','run_kg50_d07_b50_r56.sh','run_kg50_d07_b50_r56t.sh'):
  (d/n).write_bytes((base/n).read_bytes())
 ck=d/'FAKE_checkpoint.bin';ck.write_bytes(b'FAKE CHECKPOINT - NO SIMULATION DATA\n')
 helper=d/'FAKE_helper.py';helper.write_bytes(b'# FAKE helper identity; never executed\n')
 main=d/'input_kg50_d07_b50_r56.liggghts';runner=d/'run_kg50_d07_b50_r56.sh'
 paths=[main,runner,d/'input_kg50_d07_b50_r56t.liggghts',d/'run_kg50_d07_b50_r56t.sh',ck]
 def receipt():return ''.join(sh(p)+'  '+pos(p)+'\n' for p in paths).encode()
 reviewed=hashlib.sha256(receipt()).hexdigest()
 if kind=='new_call_unreviewed_duration':
  old=sh(main);main.write_bytes(main.read_bytes().replace(b'run 180000',b'run 190000',1))
  runner.write_bytes(runner.read_bytes().replace(old.encode(),sh(main).encode()))
 rec=ad/'main_inputs.sha256';rec.write_bytes(receipt());mis=sh(rec)
 if kind=='changed_after_trial':main.write_bytes(main.read_bytes()+b'\n# after-trial edit\n')
 report=d/'report.md';report.write_bytes(b'')
 calls=d/'fake_sbatch_calls.txt';calls.write_bytes(b'')
 # Remove only our prior synthetic output, if reproducing in the same folder.
 prior=ad/'main_job.txt'
 if prior.exists():prior.unlink()
 settings={'W':pos(d),'AD':pos(ad),'REP':pos(report),'SELF':pos(tool),'HELPER':pos(helper),
  'APT':sh(tool),'APH':sh(helper),'MIS':mis,'C':'kg50_d07_b50','SFX':'r56','ATT':'attempt',
  'J':'333858','TONLY':'0','G0':'1','G1':'1','G2':'1','G3':'1','USER':'review_fixture',
  'CALLS':pos(calls),'REVIEWED_RECEIPT':reviewed,'ACK_REVIEWED_RECEIPT':'0'}
 head='#!/bin/bash\nset -u\nexport PATH=/usr/bin:/bin\n'
 head+='\n'.join(k+'='+quote(v) for k,v in settings.items())+'\n'
 head+='squeue(){ return 0; }\nqre(){ printf "%s" "$1"; }\nsbatch(){ printf "%s\\n" "$*" >> "$CALLS"; printf "900001\\n"; }\n'
 script=d/'safe_gate.sh';script.write_bytes((head+'for once in 1; do\n'+block+'\ndone\n').encode())
 bash=os.environ.get('REVIEW_BASH','C:/Program Files/Git/bin/bash.exe') if os.name=='nt' else '/bin/bash'
 p=subprocess.run([bash,'--noprofile','--norc',str(script)],cwd=d,capture_output=True,text=True,encoding='utf-8')
 (d/'stdout.txt').write_text(p.stdout+p.stderr,encoding='utf-8')
 n=len(calls.read_text().splitlines());expected=0 if kind=='changed_after_trial' else 1
 rows.append({'case':kind,'returncode':p.returncode,'fake_submit_calls':n,'expected':expected,
  'pass':p.returncode==0 and n==expected,'reviewed_receipt':reviewed,'new_call_receipt':mis,
  'same_as_reviewed':reviewed==mis,'human_ack':False,'trial_deck_same_as_zip':sh(paths[2])==sh(base/paths[2].name),
  'report':report.read_text(encoding='utf-8')})
(O/'results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(rows,ensure_ascii=False,indent=2))
raise SystemExit(any(not x['pass'] for x in rows))
