from pathlib import Path
import sys,json,re,copy,subprocess,hashlib,math,itertools
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'snapshot/scripts';OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(S));import test_mixer_d2_consumers as t
records=[]
mutations={
 'normal':lambda s:s,
 'run_upto':lambda s:re.sub(r'(?m)^run (\d+)$',r'run \1 upto',s),
 'late_timestep':lambda s:re.sub(r'(?m)^timestep[^\n]*\n','',s)+re.search(r'(?m)^timestep[^\n]*',s).group(0)+'\n',
 'insert_start_late':lambda s:s.replace('insert_every once','insert_every once start 9000000'),
 'front_period':lambda s:re.sub(r'(fix mvF[^\n]* period )[^\s]+',r'\g<1>0.1',s),
 'exclude_SE_SE':lambda s:s.replace('neigh_modify    delay 0','neigh_modify    delay 0\nneigh_modify exclude type 3 3'),
 'friction_missing':lambda s:re.sub(r'(?m)^fix m4[^\n]*\n(?:    [^\n]*\n){4}','',s),
 'negative_control_bad_gravity':lambda s:s.replace('gravity 9.81','gravity 1.0'),
 'negative_control_remove_integrator':lambda s:re.sub(r'(?m)^fix integrS[^\n]*\n','',s),
}
for name,transform in mutations.items():
 a,am,_=t.fixture();b,bm,_=t.fixture(coated=True);a2=transform(a);b2=transform(b)
 if name!='normal':assert a!=a2 and b!=b2
 am2=t.rebound(a2,am);bm2=t.rebound(b2,bm)
 d=OUT/'cases'/name;d.mkdir(parents=True,exist_ok=True)
 for fn,val in [('old.in',a2),('new.in',b2)]: (d/fn).write_bytes(val.encode())
 for fn,val in [('old.meta.json',am2),('new.meta.json',bm2)]: (d/fn).write_text(json.dumps(val,ensure_ascii=False,indent=2),encoding='utf-8')
 values={'readback':t.rb.read_d2(a2,am2),'pair':t.dd.diff_d2_decks(a2,b2,am2,bm2),'plan':t.smoke.d2_plan_check(a2,am2)}
 expected='FAIL' if name.startswith('negative_control') else 'PASS'
 assert all(x['verdict']==expected for x in values.values())
 for key,x in values.items():(d/(key+'.json')).write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
 # Real CLI for each consumer, without running a simulator.
 cmds={
 'readback':[str(S/'mixer_deck_readback.py'),'--d2',str(d/'old.in'),str(d/'old.meta.json'),'--json',str(d/'readback.cli.json')],
 'pair':[str(S/'mixer_deck_diff.py'),str(d/'old.in'),str(d/'new.in'),'--allow','D2','--meta-ref',str(d/'old.meta.json'),'--meta-new',str(d/'new.meta.json'),'--json',str(d/'pair.cli.json')],
 'plan':[str(S/'mixer_smoke_blind.py'),'--d2-plan',str(d/'old.in'),'--d2-meta',str(d/'old.meta.json')]
 }
 rc={}
 for key,args in cmds.items():
  p=subprocess.run([sys.executable,'-I','-X','utf8','-B',*args],capture_output=True);(d/(key+'.log')).write_bytes(p.stdout+p.stderr);rc[key]=p.returncode
  assert p.returncode==(1 if expected=='FAIL' else 0),(name,key,p.stderr)
 records.append({'name':name,'verdicts':{k:v['verdict'] for k,v in values.items()},'cli_rc':rc,'execution_authorized':{k:v['execution_authorized'] for k,v in values.items()}})
# Independent arithmetic and phase/count controls on alternative input tuples.
normal=[]
for phases,generation,rho,stiff,layered in itertools.product([('AM_P','AM_S','SE'),('AM_P','SE')],['gen1','lab20261014'],[.2,1.,2.],[1.,20.],[True,False]):
 a,am,_=t.fixture(phases=phases,generation=generation,rho=rho,stiff=stiff,layered=layered,n=90007,cgf=135,bo=1.1,seed=49979687)
 b,bm,_=t.fixture(phases=phases,generation=generation,rho=rho,stiff=stiff,layered=layered,n=90007,cgf=135,bo=1.1,seed=49979687,coated=True)
 rr=t.rb.read_d2(a,am);pair=t.dd.diff_d2_decks(a,b,am,bm);assert rr['verdict']==pair['verdict']=='PASS'
 raw=t.rb.read_deck(a);se=len(phases);rad=raw['templates'][se]['radius'];dens=raw['templates'][se]['density'];E=raw['E'][se-1];nu=raw['nu'][se-1];es=E/(2*(1-nu*nu));rs=rad/2;ced=raw['ced'][se,se]
 A=4/3*es*math.sqrt(rs);B=2*math.pi*rs*ced;bo=(B**3/A**2)/(4/3*math.pi*rad**3*dens*9.81)
 assert abs(bo/1.1-1)<2e-5
 weights={'AM_P':56,'AM_S':24,'SE':18};d0={'gen1':{'AM':4800,'SE':2000},'lab20261014':{'AM':4850,'SE':1640}}[generation]
 nr=[weights[p]/(d0['SE' if p=='SE' else 'AM']*({'AM_P':9,'AM_S':4,'SE':1}[p]**3)) for p in phases];ind=[round(90007*x/sum(nr)) for x in nr]
 assert list(rr['expected_counts'].values())==ind
 normal.append({'phases':phases,'generation':generation,'rho':rho,'stiff':stiff,'layered':layered,'counts':ind,'Bo_SE_independent':bo})
# Byte binding through all three CLI entry points: CRLF physical bytes, unchanged LF metadata.
bytecases=[]
for meta_kind in ['lf_metadata','crlf_metadata']:
 d=OUT/'cases'/('crlf_'+meta_kind);d.mkdir(parents=True,exist_ok=True);a,am,_=t.fixture();b,bm,_=t.fixture(coated=True)
 for name,text,meta in [('old',a,am),('new',b,bm)]:
  raw=text.replace('\n','\r\n').encode();(d/(name+'.in')).write_bytes(raw)
  if meta_kind=='crlf_metadata':meta['deck_sha256']=hashlib.sha256(raw).hexdigest();meta['deck_bytes']=len(raw)
  (d/(name+'.meta.json')).write_text(json.dumps(meta),encoding='utf-8')
 commands=[['mixer_deck_readback.py','--d2',str(d/'old.in'),str(d/'old.meta.json')],['mixer_deck_diff.py',str(d/'old.in'),str(d/'new.in'),'--allow','D2','--meta-ref',str(d/'old.meta.json'),'--meta-new',str(d/'new.meta.json')],['mixer_smoke_blind.py','--d2-plan',str(d/'old.in'),'--d2-meta',str(d/'old.meta.json')]]
 rc=[]
 for idx,args in enumerate(commands):
  p=subprocess.run([sys.executable,'-I','-X','utf8','-B',str(S/args[0]),*args[1:]],capture_output=True);(d/(str(idx)+'.log')).write_bytes(p.stdout+p.stderr);rc.append(p.returncode)
 assert rc==([0,0,0] if meta_kind=='lf_metadata' else [1,1,1]),rc
 bytecases.append({'metadata':meta_kind,'cli_rc':rc,'physical_sha256':hashlib.sha256((d/'old.in').read_bytes()).hexdigest(),'physical_bytes':(d/'old.in').stat().st_size,'metadata_sha256':json.loads((d/'old.meta.json').read_bytes())['deck_sha256']})
# Exact command-semantics calculation, not simulated dynamics.
a,am,_=t.fixture();F=am['steps']['fill'];N=am['steps']['run'];dt=am['dt']['deck_s'];period=am['period_s']
calc={'registered_steps':[1,F,F,N],'relative_final_step':1+2*F+N,'upto_increments':[1,F-1,0,N-F],'upto_final_step':N,'registered_rotation_seconds':N*dt,'upto_rotation_seconds':(N-F)*dt,'registered_revs':N*dt/period,'upto_revs':(N-F)*dt/period,'front_period_seconds':.1,'drum_period_seconds':period,'front_revs_if_changed':N*dt/.1,'insert_start':9000000,'insA_removed_at':1+F,'insB_removed_at':1+2*F}
result={'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in S.glob('*.py')},'cases':records,'normal_arithmetic_cases':normal,'byte_cases':bytecases,'command_semantics':calc,'physical_runs':0}
(OUT/'independent_results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'cases':len(records),'normal_arithmetic':len(normal),'byte_cases':bytecases,'command_semantics':calc},ensure_ascii=False))
