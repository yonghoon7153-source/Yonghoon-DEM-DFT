"""Independent narrow ULPR probes. Synthetic control-flow fixtures, not DEM runs."""
from pathlib import Path
import sys,os,json,csv,hashlib,subprocess,copy,types,random,re
from fractions import Fraction
R=Path(__file__).resolve().parent;K=R/'repo/docs/data/ps45_unload_20261009';O=R/'evidence/independent';O.mkdir(parents=True,exist_ok=True);F=R/'tmp/probe';F.mkdir(parents=True,exist_ok=True)
sys.dont_write_bytecode=True;sys.path.insert(0,str(K));import ul_reader as u,make_unload_decks as mk
import tempfile
tempfile.tempdir=str(R/'tmp')
P=u.ul_lib.load_params();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old=types.ModuleType('old_reader');old.__file__=str(K/'ul_reader.py');exec(compile((R/'baseline/docs/data/ps45_unload_20261009/ul_reader.py').read_bytes(),old.__file__,'exec'),old.__dict__)
# Separate resident R39 run, no whole-repository claim.
r39=[]
def chk(label,test,extra=''):
 try:r39.append({'label':label,'pass':bool(test()),'error':None})
 except Exception as e:r39.append({'label':label,'pass':False,'error':repr(e)})
u._resume_integer_tests(chk,P);(O/'r39.json').write_text(json.dumps(r39,ensure_ascii=False,indent=2),encoding='utf8')
# Independent arithmetic oracle: decimal coefficient and base-ten exponent via Fraction, not Decimal/float round.
rng=random.Random(20261024);ar=[]
for i in range(500):
 digits=str(rng.randrange(0,10**rng.randrange(1,45)));cut=rng.randrange(len(digits)+1);e=rng.randrange(-48,49);s=('+' if i%3==0 else '')+(digits[:cut] or '0')+'.'+digits[cut:]+f'e{e:+d}'
 oracle=Fraction(int(digits),10**(len(digits)-cut))*Fraction(10**e if e>=0 else 1,10**(-e) if e<0 else 1)
 expect=int(oracle) if oracle.denominator==1 else None;got=u._resume_integer(s);ar.append({'token':s,'expected':expect,'actual':got,'pass':expect==got})
for s,expected in [('9007199254740993',9007199254740993),('9007199254740992.0000000001',None),('3e-1000000000',None),('0e1000000000',0),('1e309',None),('0'*4095+'3',3),('0'*4096+'3',None),('3\u00a0',None),('\u00a03',None),('٣',None),('３',None),('3_0',None),('-0',None),('3.0000000000000000000000001',None)]:
 got=u._resume_integer(s);ar.append({'token':s[:120],'length':len(s),'expected':expected,'actual':got,'pass':expected==got})
(O/'integer_oracle.json').write_text(json.dumps(ar,ensure_ascii=False,indent=2),encoding='utf8')
# A production-deck control-flow trace for all four legal boundaries, with physical observations mocked.
positive=[];fixtures={}
for kr in range(4):
 root=F/f'k{kr}';root.mkdir(exist_ok=True);ds,tr=u._ut_trace_arm(str(root),P,4);u._fake_restored(str(root),u.B73);u._w(str(root/u.B73/'ul_base.in'),'variable ul_S2max equal 1e-05\n');d=Path(ds);cols=P['records']['steps_cols'];row=dict(zip(cols,tr['steps'][kr]));sr=int(row['step']);plain=u.arm_verdict(str(d),u.B73,'UT',P,root=str(root))
 state={'ul_rstep':sr,'ul_k':kr,'ul_phase':0 if kr<2 else 1,'ul_modeB':int(kr>0),'ul_pz':float(row['plate_z']),'ul_lift':float(row['lift']),'ul_ncross':max(0,kr-2),'ul_xk':-1 if kr<2 else 2,'ul_lk0':11,'ul_Pbar':float(row['Pbar']),'ul_kind':row['kind']}
 def obs(k,w,phase,step):return {'P':{None:.16,0:.16,1:.0012,2:.0008,3:.0006,4:.0004}.get(k,.0002),'Kt':1e-7,'Kr':1e-8,'Kti':1e-7,'nc':1,'na':160417,'lk':11}
 trace=mk.deck_sim(mk.render(u.B73,'UT',P),obs,sr,state=state,cli={'ul_resume':'1'})
 for name in ['windows','steps','events']:
  cc=P['records'][name+'_cols'];ix=cc.index('step');rows=[x for x in tr[name] if int(x[ix])<=sr]+trace[name]
  (d/f'ul_{name}.csv').write_bytes((','.join(cc)+'\n'+''.join(','.join(x)+'\n' for x in rows)).encode())
 (d/'run_manifest.txt').write_bytes(f'bed={u.B73}\njob=UT\nresume=0\ngate=ALLOW\nstart=a1\nend=a1 fails=1 reader_rc=0\nresume=1\ngate=RESUME\nstart=a2\nresume_from={sr}\nstage=UT screen=screen_a2.txt rc=0 check=PASS\nreader_arm_rc=0\nend=a2 fails=0 reader_rc=0\n'.encode())
 sp=d/'restart'/f'state_unload_{sr}.in';sp.write_bytes(''.join(f'variable {k} {"string" if isinstance(v,str) else "equal"} {v}\n' for k,v in state.items()).encode())
 before={n:sha(d/n) for n in ['ul_events.csv','ul_windows.csv','ul_steps.csv']}
 p=subprocess.run([sys.executable,'-X','utf8','-B',str(K/'ul_reader.py'),'arm',str(root),u.B73,'UT'],capture_output=True,text=True,encoding='utf8',timeout=30)
 v=json.loads((d/'arm_verdict.json').read_text(encoding='utf8'));rr=u.read_run(str(d),P)
 positive.append(dict(kr=kr,sr=sr,auth=rr['resume_auth'],primary=v['primary_status'],rho=v['rho_pct'],baseline_primary=plain['primary_status'],baseline_rho=plain['rho_pct'],same=plain['rho_pct']==v['rho_pct'],mock_result=trace['result'],cli_rc=p.returncode,csv_unchanged=all(sha(d/n)==h for n,h in before.items())))
 fixtures[kr]=(root,d,sr,sp)
(O/'positive.json').write_text(json.dumps(positive,ensure_ascii=False,indent=2),encoding='utf8')
root,d,sr,sp=fixtures[3];ep=d/'ul_events.csv';mp=d/'run_manifest.txt';original={p:p.read_bytes() for p in [ep,mp,sp]};cases=[]
def reset():
 for p,b in original.items():p.write_bytes(b)
def event_edit(field,token,extra=False):
 rows=list(csv.DictReader(ep.read_text(encoding='utf8').splitlines()));ev=next(x for x in rows if x['event']=='RESUME')
 if extra: ev=dict(ev);rows.append(ev)
 ev[field]=token;cc=P['records']['events_cols'];ep.write_bytes((','.join(cc)+'\n'+''.join(','.join(row[c] for c in cc)+'\n' for row in rows)).encode())
def capture(name,expected,cli=True):
 before={n:sha(d/n) for n in ['ul_events.csv','ul_windows.csv','ul_steps.csv']};rr=u.read_run(str(d),P);baseline=old.read_run(str(d),P)
 if cli:
  p=subprocess.run([sys.executable,'-X','utf8','-B',str(K/'ul_reader.py'),'arm',str(root),u.B73,'UT'],capture_output=True,text=True,encoding='utf8',timeout=30)
  v=json.loads((d/'arm_verdict.json').read_text(encoding='utf8'));rc=p.returncode
 else:v=u.arm_verdict(str(d),u.B73,'UT',P,root=str(root));rc=None
 case={'name':name,'expected':expected,'auth':rr['resume_auth'],'baseline_auth':baseline['resume_auth'],'dropped':rr['n_superseded_rows'],'primary':v['primary_status'],'rho':v['rho_pct'],'problems':rr['problems'],'why':v['why'],'cli_rc':rc,'csv_unchanged':all(sha(d/n)==h for n,h in before.items())}
 case['satisfies']=bool(rr['resume_auth']) and v['primary_status']=='OK' if expected=='accept' else not rr['resume_auth'] and v['rho_pct'] is None and v['primary_status']=='UNIDENTIFIED' if expected=='reject' else None
 cases.append(case)
 # Keep altered input bytes and actual CLI result to replay each distinct case.
 sd=O/'cases'/name;sd.mkdir(parents=True,exist_ok=True)
 for p0 in [ep,mp,sp]: (sd/p0.name).write_bytes(p0.read_bytes())
 (sd/'arm_verdict.json').write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
 return case
for field in ['k','step']:
 val=3 if field=='k' else sr
 for idx,token in enumerate([f'{val}.0',f'{val}E0',f'{val}.0000000000000001','NaN','1e9999999','٣',f'{val}\u00a0','0'*4096+str(val)]):
  reset();event_edit(field,token);capture(f'event_{field}_{idx}','accept' if idx<2 else 'reject')
for key,val in [('ul_k',3),('ul_rstep',sr)]:
 for idx,token in enumerate([f'{val}.0',f'{val}E0',f'{val}.0000000000000001',f'{val}\u00a0']):
  reset();sp.write_bytes(original[sp].replace(f'variable {key} equal {val}\n'.encode(),f'variable {key} equal {token}\n'.encode()));capture(f'state_{key}_{idx}','accept' if idx<2 else 'reject')
 reset();sp.write_bytes(original[sp]+f'variable {key} equal {val}\n'.encode());capture(f'state_duplicate_{key}','reject')
for idx,append in enumerate([f'resume_from={sr}.0\n',f'\u2003resume_from={sr}\n',f'resume_from={sr}\u2028#tail\n','resume_from=\n',f'resume_from = {sr}.49\n',f'ignored=true\u2028resume_from={sr}.49\n']):
 reset();mp.write_bytes(original[mp]+append.encode());capture(f'manifest_{idx}','reject' if idx<4 else 'explore')
for idx,token in enumerate(['3.49', '3\u2028.49','3\x00','3\t4']):
 reset();event_edit('k',token,extra=True);capture(f'extra_bad_event_{idx}','reject')
# A RESUME identifier error must not disappear merely because the event label is noncanonical.
for idx,label in enumerate(['RESUME ',' RESUME','RESUME\u00a0','RESUME\t','resume','RESUME\x00','UNKNOWN']):
 reset();event_edit('event',label,extra=True)
 rows=ep.read_text(encoding='utf8');lines=rows.split('\n');lines[-2]=lines[-2].replace(',3,',',3.49,',1);ep.write_bytes('\n'.join(lines).encode());capture(f'event_label_{idx}','explore')
reset();capture('restored_positive','accept')
(O/'cli_cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2),encoding='utf8')
summary={'r39_pass':sum(x['pass'] for x in r39),'r39_total':len(r39),'arithmetic_pass':sum(x['pass'] for x in ar),'arithmetic_total':len(ar),'positive':positive,'cli_cases':len(cases),'contract_failures':[x for x in cases if x['satisfies'] is False],'explore':[x for x in cases if x['expected']=='explore']}
(O/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(summary,ensure_ascii=False,indent=2),flush=True)
