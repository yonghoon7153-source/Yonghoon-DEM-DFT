"""Read-only review of supplied files; mutations/outputs stay in independent/.
No LIGGGHTS, MPI, SLURM, WSL or remote commands are executed.
"""
from pathlib import Path
import ast, hashlib, json, re, difflib, subprocess, sys, os, shutil, shlex

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'independent'; OUT.mkdir(exist_ok=True)
REPO=ROOT/'repo'; CASE='kg50_d07_b50'
TR=ROOT/'trial'/CASE
ATT=next(TR.glob('attempt_*'))
MAIN=REPO/'docs/data/kg50_decks_20261027_v3_b50'/CASE/f'input_{CASE}.liggghts'
RES=TR/f'input_{CASE}_r56.liggghts'; TEST=TR/f'input_{CASE}_r56t.liggghts'
TOOL=REPO/'scripts/resume_ckpt.sh'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,s): p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(s.encode('utf-8'))
def save(p,v):put(p,json.dumps(v,ensure_ascii=False,indent=2)+'\n')
checks=[]
def expect(name,actual,expected):
 checks.append({'name':name,'actual':actual,'expected':expected,'pass':actual==expected})

# Verify the supplied bytes against the remote fixed-pin Git blob identities.
inventory=json.loads((ROOT/'intake.json').read_text(encoding='utf-8'))
remote=json.loads((ROOT/'remote_meta.json').read_text(encoding='utf-8'))
for x in remote:
 assert x['status']=='fulfilled' and not x['value']['error'],x
 v=x['value']; blob=(REPO/v['path']).read_bytes()
 actual_blob=hashlib.sha1(b'blob '+str(len(blob)).encode()+b'\0'+blob).hexdigest()
 expect('remote_blob:'+v['path'],actual_blob,v['sha'])
manifest_count=0
for line in (ROOT/'MANIFEST.sha256').read_text(encoding='utf-8').splitlines():
 if not line.strip():continue
 expected,rel=line.split('  ',1)
 p=(ROOT/rel).resolve()
 assert p.is_relative_to(ROOT),rel
 assert sha(p)==expected,rel
 manifest_count+=1
expect('zip manifest',manifest_count,22)

# Extract the exact producer's Python heredoc; do not source the submit script.
txt=TOOL.read_text(encoding='utf-8')
code=txt.split("deckcheck(){ python3 - \"$@\" <<'PY'\n",1)[1].split('\nPY\n}',1)[0]
put(OUT/'deckcheck_exact.py',code+'\n')
defs=code.split('\nif len(sys.argv) == 3',1)[0]
dc={};exec(compile(defs,str(TOOL)+'#deckcheck','exec'),dc)
ck=f'restart_{CASE}/restart_settling_20001.bin'
def checkpair(a,b):
 p,n=dc['check'](str(a),str(b),ck,20001,str(TR))
 return {'problem_count':len(p),'problems':p,'notes':n}
base=checkpair(MAIN,RES);expect('actual_D07_static',base['problem_count'],0)
save(OUT/'actual_deckcheck.json',base)
trial_new=OUT/'trial_regenerated.liggghts'
rc=dc['cut_trial'](str(RES),'2000',str(trial_new))
expect('trial_cutter_rc',rc,0);expect('trial_exact_bytes',trial_new.read_bytes(),TEST.read_bytes())
# bytes are recorded by digest in the JSON, not as giant binary strings.
checks[-1]['actual']=sha(trial_new); checks[-1]['expected']=sha(TEST)
mutations={
 'gravity_res_only':('fix gravi all gravity 98.1','fix gravi all gravity 196.2'),
 'dt_res_only':('variable dt      equal 1.0e-6','variable dt      equal 2.0e-6'),
 'duration_res_only':('run 180000','run 190000'),
}
for name,(old,new) in mutations.items():
 s=RES.read_text(encoding='utf-8');assert s.count(old)==1
 p=OUT/(name+'.liggghts');put(p,s.replace(old,new));v=checkpair(MAIN,p)
 expect(name+'_rejected',v['problem_count']>0,True);save(OUT/(name+'.json'),v)
# Both source and generated deck changed before a new call: new trial remains identical.
am=OUT/'new_source_210001.liggghts'; ar=OUT/'new_resume_210001.liggghts'
put(am,MAIN.read_text(encoding='utf-8').replace('run 200000','run 210000',1))
put(ar,RES.read_text(encoding='utf-8').replace('run 180000','run 190000',1))
v=checkpair(am,ar);expect('new_call_duration_change_static_pass',v['problem_count'],0)
newtrial=OUT/'new_call_trial.liggghts';dc['cut_trial'](str(ar),'2000',str(newtrial))
expect('new_call_trial_unchanged',sha(newtrial),sha(TEST));save(OUT/'new_call_duration_change.json',v)

# Independent logical command comparison (quote-aware, joins '&'; no producer parser).
def commands(p):
 rows=[];buf='';start=0
 for no,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
  q=None;s=''
  for c in line:
   if c=='#' and q is None:break
   s+=c
   if c==q:q=None
   elif c in '\"\'' and q is None:q=c
  s=s.strip()
  if not s:continue
  if not buf:start=no
  if s.endswith('&'):buf+=s[:-1].rstrip()+' ';continue
  rows.append((start,buf+s));buf=''
 assert not buf
 return rows
m=commands(MAIN);r=commands(RES)
mi=next(i for i,x in enumerate(m) if x[1]=='run 200000')
ri=next(i for i,x in enumerate(r) if x[1].startswith('run 180000'))
expect('tail_commands_equal',[shlex.split(s) for _,s in m[mi+1:]],[shlex.split(s) for _,s in r[ri+1:]])
checks[-1]['actual']=len(m[mi+1:]);checks[-1]['expected']=len(r[ri+1:])
expect('tail_command_count',len(r[ri+1:]),64)
for ident in ('pts1','pts2','pts3','pdd_mix'):
 a=[s for _,s in m if s.startswith('fix '+ident+' ')]
 b=[s for _,s in r if s.startswith('fix '+ident+' ')]
 expect('template:'+ident,a,b)
ins=MAIN.with_name(f'input_{CASE}_insert.liggghts')
expect('insert_prefix_166',MAIN.read_bytes().splitlines()[:166],ins.read_bytes().splitlines()[:166])
checks[-1]['actual']=hashlib.sha256(b'\n'.join(MAIN.read_bytes().splitlines()[:166])).hexdigest()
checks[-1]['expected']=hashlib.sha256(b'\n'.join(ins.read_bytes().splitlines()[:166])).hexdigest()
runrows=[];step=20001
for no,s in r[ri:]:
 if re.match(r'^run \d+$',s):
  n=int(s.split()[1]);runrows.append({'line':no,'command':s,'start':step,'end':step+n,'note':'first visit only; pressure loop not evaluated'});step+=n
save(OUT/'static_run_trace.json',{'warning':'static straight-line first visits, NOT a simulation','runs':runrows,'checkpoint_line':160,'terminal_after_checkpoint':False})

# Recompute hashes and actual trial log values, separating unavailable originals.
receipt=[]
for line in (ATT/'main_inputs.sha256').read_text().splitlines():
 h,path=line.split('  ',1);p=TR/Path(path).name
 if p.exists():expect('receipt:'+p.name,sha(p),h)
 receipt.append({'path':path,'expected':h,'local_sha256':sha(p) if p.exists() else None,'available':p.exists()})
save(OUT/'receipt_verification.json',receipt)
log=(ROOT/'trial/logs/output_kg50_d07_b50_r56t_333858.out').read_text(encoding='utf-8')
thermo=[]
for no,s in enumerate(log.splitlines(),1):
 w=s.split()
 if len(w)==4 and w[0].isdigit() and w[1]=='488291':thermo.append({'line':no,'step':int(w[0]),'atoms':int(w[1]),'KE':float(w[2]),'CPU':float(w[3])})
expect('trial_thermo_steps',[x['step'] for x in thermo],[20001,21000,22000,22001])
expect('trial_errors',len(re.findall(r'^.*ERROR.*$',log,re.M)),0)
expect('trial_np_grid',re.search(r'  (\d+) by (\d+) by (\d+) MPI',log).groups(),('8','7','1'))
loop=re.search(r'Loop time of ([\d.]+) on (\d+) procs for (\d+) steps with (\d+) atoms',log)
expect('loop_evidence',loop.groups(),('211.783','56','2000','488291'))
lid=[l for l in log.splitlines() if l.startswith('LMP_IDENTITY ')]
expect('identity_line_count',len(lid),1)
expect('trial_deck_identity',re.search(r' deck=\S+ sha256=([a-f0-9]{64})',lid[0]).group(1),sha(TEST))
save(OUT/'trial_log_recomputed.json',{'thermo':thermo,'loop':loop.groups(),'identity':lid,'original_log_in_initial_bundle':False,'sacct_raw_in_bundle':False})
original=ROOT/'input/kg50_d07_b50_ins1_log.liggghts'
if original.exists():
 def thermos(p):
  out=[];head=None
  for no,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
   w=line.split()
   if len(w)>=2 and w[:2]==['Step','Atoms']:head=w;continue
   if head and len(w)==len(head) and w[0].isdigit():
    try:v=dict(zip(head,map(float,w)))
    except ValueError:continue
    out.append({'line':no,**v})
  return out
 old=thermos(original);new=thermos(ROOT/'trial/logs/output_kg50_d07_b50_r56t_333858.out')
 a={int(x['Step']):x for x in old};b={int(x['Step']):x for x in new}
 rows=[]
 for step in (20001,21000,22000):
  aa,bb=a[step],b[step];rel=abs(aa['KinEng']-bb['KinEng'])/abs(aa['KinEng'])
  expect('raw_log_atoms:'+str(step),aa['Atoms'],bb['Atoms'])
  expect('raw_log_KE:'+str(step),rel,0.0)
  rows.append({'step':step,'original_line':aa['line'],'trial_line':bb['line'],'atoms':int(aa['Atoms']),'original_KE':aa['KinEng'],'trial_KE':bb['KinEng'],'relative_difference':rel})
 expected_steps=sorted({int(x['Step']) for x in old if 20001<x['Step']<=22001 and x.get('CPU',0)>0})
 expect('G3_source_comparison_steps',expected_steps,[21000,22000])
 expect('G3_missing_comparison_rows',[s for s in expected_steps if s not in b],[])
 save(OUT/'original_log_recomputed.json',{'original_sha256':sha(original),'pairs':rows,
  'comparison_steps':expected_steps,'G1':True,'G3':True,'also_compared_22000_KE':True,
  'KE_unit':'J under LIGGGHTS units si, simulation-scaled energy, not real-pellet energy',
  'server_original_copy_cmp_verified':False,'scope':'user-provided raw log; server-copy identity beyond attached bytes not attested by this review'})

# Re-render both original runners using the exact producer function, supplied hashes.
rc_code=txt.split("runnerck(){ python3 -I - \"$@\" <<'PY'\n",1)[1].split('\nPY\n}',1)[0]
rn={};exec(compile(rc_code.split('\ntry:\n    sys.exit(main())',1)[0],str(TOOL)+'#runnerck','exec'),rn)
wr='/lustre/home/yonghoon/dem_test/'+CASE
helper=(ATT/f'helper_run_{CASE}_r56.sh.orig').read_text().splitlines()
sb={}
for line in helper:
 for key,_ in rn['KEYS']:
  if line.startswith('#SBATCH '+key):sb[key]=line[len('#SBATCH '+key):]
sb['-n ']='56'
env=[s for s in helper if rn['ENVL'].fullmatch(s)]
info={'sb':sb,'env':env,'ab':{'재개 덱':wr+'/'+RES.name,'시험 덱':wr+'/'+TEST.name},'sha':{'재개 덱':sha(RES),'시험 덱':sha(TEST),'체크포인트':receipt[-1]['expected']},'ckp':receipt[-1]['path']}
for trial in (False,True):
 name=f'run_{CASE}_r56'+('t' if trial else '')+'.sh'
 rendered=rn['render'](CASE,'r56','56',wr,info,trial).encode()
 expect('render_exact:'+name,hashlib.sha256(rendered).hexdigest(),sha(TR/name))

# Recompute the author's normalized D2 comparison. Read-only input; output elsewhere.
p=subprocess.run([sys.executable,'-I','-X','utf8','-B',str(ROOT/'evidence/compare_transform.py'),str(REPO),str(ROOT/'trial'),str(OUT/'transform')],capture_output=True,text=True,encoding='utf-8')
put(OUT/'transform_stdout.txt',p.stdout+p.stderr);expect('author_compare_rc',p.returncode,0)
for name in ('diff_D07.txt','diff_D2.txt','transform_compare.json'):
 # The author's write_text uses platform newlines. Compare textual results,
 # keeping input provenance checks strictly byte-based above.
 expect('author_compare_LF:'+name,hashlib.sha256((OUT/'transform'/name).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),sha(ROOT/'evidence'/name))
save(OUT/'checks.json',checks)
bad=[x for x in checks if not x['pass']]
print(json.dumps({'checks':len(checks),'passed':len(checks)-len(bad),'failed':bad,'scope':'static/source/hash/log readback only; no solver or scheduler'},ensure_ascii=False,indent=2))
sys.exit(bool(bad))
