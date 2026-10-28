from pathlib import Path
import sys,subprocess,importlib.util,json,re
out=Path(__file__).resolve().parent;root=out.parents[1];script=root/'repo/scripts/resume_ckpt.sh'
raw=script.read_text(encoding='utf-8');embedded=raw.split("<<'PY'\n",1)[1].split('\nPY\n',1)[0]
ep=out/'exact_embedded_gate.py';ep.write_text(embedded,encoding='utf-8')
spec=importlib.util.spec_from_file_location('author_test',root/'repo/scripts/test_resume_ckpt.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
# This construction is explicitly a narrow static transcription of awk :693, NOT executed GNU awk.
def slice_numeric_run(text,ts=2000):
 out=[]
 for line in text.splitlines():
  w=line.split()
  if len(w)>=2 and w[0]=='run':
   mat=re.match(r'^[+-]?(?:\d+(?:\.\d*)?|\.\d+)',w[1]);n=float(mat.group()) if mat else 0
   if n>1:out.append('run '+str(int(min(n,ts))));break
  out.append(line)
 return '\n'.join(out)+'\n'
records=[]
for name,body in [('plain',m.res_good()),('continued_first_long_run',m.res_good().replace('run 180000\n','run &\n180000\n',1))]:
 p=out/(name+'.liggghts');p.write_text(body,encoding='utf-8');t=out/(name+'_trial.liggghts');t.write_text(slice_numeric_run(body),encoding='utf-8')
 c=subprocess.run([sys.executable,'-I','-X','utf8','-B',str(ep),m.MAIN,str(p),m.CKPT,'20001',str(out)],capture_output=True,text=True)
 r=subprocess.run([sys.executable,'-I','-X','utf8','-B',str(ep),'--trial-steps',str(t)],capture_output=True,text=True)
 record={'case':name,'static_check_rc':c.returncode,'static_check_stdout':c.stdout,'trial_steps_rc':r.returncode,'trial_steps_stdout':r.stdout,'trial_construction':'Static transcription of awk :693; actual GNU awk could not start in sandbox','g0_expected_final_step':20001+int(r.stdout.split()[0]) if r.returncode==0 else None}
 records.append(record);print(json.dumps(record,ensure_ascii=False))
 assert c.returncode==0 and r.returncode==0
assert records[0]['g0_expected_final_step']==22001 and records[1]['g0_expected_final_step']==202002
(out/'trial_steps_results.json').write_text(json.dumps(records,indent=2,ensure_ascii=False),encoding='utf-8')
