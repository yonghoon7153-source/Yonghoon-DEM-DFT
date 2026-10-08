"""One approved session. First unexpected result stops; no retry."""
import sys,os,ast,types,json,hashlib,time,traceback,copy,builtins
from pathlib import Path
from decimal import Decimal as D,localcontext
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shared_fixture as f
from control_cases import execute_control_case
from input_binding import VerificationProxy
ROOT=f.ROOT;SOURCE=f.SOURCE
PLAN=json.loads((ROOT/'VALIDATION_PLAN_CORRECTED.json').read_text(encoding='utf-8-sig'))
def block(*a,**k):raise RuntimeError('INERT_NATIVE_PROCESS_CONSOLE_JOB_BLOCK')
def audit(event,args):
 if event.startswith(('subprocess.','os.system','os.exec','os.spawn','ctypes.','socket.')):block()
sys.addaudithook(audit)
builtins.input=block;os.system=block
def load_exact(name):
 path=SOURCE/'candidate'/f'{name}.py.inactive.txt';text=path.read_text(encoding='utf-8-sig');tree=ast.parse(text)
 nodes=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.ClassDef,ast.FunctionDef))]
 allowed={'decimal','csv','hashlib','io','copy','json','math'}
 for n in nodes:
  if isinstance(n,ast.Import):assert all(a.name in allowed for a in n.names)
  if isinstance(n,ast.ImportFrom):assert n.module in allowed
 module=types.ModuleType('sealed_'+name);module.__dict__['__name__']='sealed_'+name
 exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),module.__dict__)
 return module
def compare_args(a,ref,spec):return(a,ref,spec['requests_current'],spec['requests_reference'],spec['common_requests'],spec['safe_end_s'])
def charge_case(cid,c,case):
 protect=cid in ('CHARGE_R109','CHARGE_R116')
 b,n,a,rb,s=f.base(protect)
 idx=-1
 if cid=='CHARGE02':
  for i in range(len(a['charge'])):
   for k in ('j','RN','RP','I'):a['charge'][i][k]=D(0)
   f.sync_li(a,i,'LiN',D(1));f.sync_li(a,i,'LiP',D(1))
 elif cid=='CHARGE03':rb['quadrature_bound_C_m2']=None
 elif cid=='CHARGE04':rb['quadrature_bound_C_m2']='1'
 elif cid=='CHARGE05':
  r=a['charge'][1];r.update(j=D('-1'),RN=D('-1'),RP=D('1'),I=D('-1'))
 elif cid=='CHARGE06':a['charge'][1]['RN']=D(99)
 elif cid=='CHARGE07':a['charge'][1]['I']=D(99)
 elif cid=='CHARGE08':
  f.sync_li(a,1,'LiN',D('1.00001'));f.sync_li(a,1,'LiP',D('.99999'))
 elif cid=='CHARGE09':
  # Last qP excess exceeds the solid balance tolerance, total Li compensated.
  r=a['charge'][-1];delta=D('.1')/f.F
  f.sync_li(a,-1,'LiP',r['LiP']+delta);f.sync_li(a,-1,'LiE',r['LiE']-delta)
 elif cid=='CHARGE10':
  r=a['charge'][-1];delta=D('.1')/f.F
  f.sync_li(a,-1,'LiN',r['LiN']-delta);f.sync_li(a,-1,'LiP',r['LiP']+delta)
 elif cid=='CHARGE11':a['charge'][1],a['charge'][2]=a['charge'][2],a['charge'][1]
 elif cid=='CHARGE12':f.sync_li(a,-1,'LiE',D('1.01'))
 elif cid=='CHARGE_R101':a['charge'].pop()
 elif cid=='CHARGE_R102':a['charge'].pop(1)
 elif cid=='CHARGE_R103':a['charge'][1]['time_s']+=D('.000001')
 elif cid=='CHARGE_R104':a['charge'][1]['LiN']+=D('.000001')
 elif cid=='CHARGE_R105':rb['charge_provenance']['global_identity']={**rb['charge_provenance']['global_identity'],'sha256':'b'*64}
 elif cid=='CHARGE_R106':del rb['charge_provenance']['native_grid_identity']
 elif cid=='CHARGE_R107':n['stored_times_s'][1]=str(D(n['stored_times_s'][1])+D('.000001'))
 elif cid=='CHARGE_R108':n['last_stored_s']='119.9'
 elif cid in ('CHARGE_R110','CHARGE_R111','CHARGE_R114'):
  ind=next(i for i,r in enumerate(a['charge']) if r['time_s']==D('100.001'))
  electrode='LiP' if cid=='CHARGE_R111' else 'LiN'
  reversal=D('.0002000001') if cid=='CHARGE_R114' else D('.00075')
  q=D('25.001')-reversal
  value=D(1)+(q/f.F if electrode=='LiP' else -q/f.F)
  old=a['charge'][ind][electrode];f.sync_li(a,ind,electrode,value)
  f.sync_li(a,ind,'LiE',a['charge'][ind]['LiE']-(value-old))
 elif cid in ('CHARGE_R112','CHARGE_R113'):
  r=D(case['pinned_scalar_fixture']['inventory_r_mol_m2']);a=f.data([D(0),D(1)],D(0))
  for i,(nn,pp) in enumerate(((D(0),r),(r,D(0)))):f.sync_li(a,i,'LiN',nn);f.sync_li(a,i,'LiP',pp)
  n.update(stored_times_s=['0','1'],last_stored_s='1');s['safe_end_s']='1'
  f.rebind(b,n,a,rb)
  args,kw=f.charge_args(a,n,rb,s,end='1');return c.charge_balance(*args,**kw),None
 elif cid=='CHARGE_R115':rb['charge_provenance']['normalized_units']['LiN']='mol'
 elif cid=='CHARGE_R116':s['safe_end_s']='90.1'
 elif cid=='CHARGE_R117':a['charge'].pop(0)
 if cid not in ('CHARGE_R105','CHARGE_R106'):f.rebind(b,n,a,rb)
 if cid in ('CHARGE01','CHARGE03') or cid.startswith('CHARGE_R1'):
  result=c.analyze(b,n,a,rb,s)
  return result,f.producer_context(b,n,s)
 args,kw=f.charge_args(a,n,rb,s);return c.charge_balance(*args,**kw),None
def consumer_case(cid,c,case):
 if cid.startswith('CHARGE'):return charge_case(cid,c,case)
 if cid.startswith('READ'):
  raw=b'time_s,value\n0,1\n1,2\n';head=['time_s','value'];units={'time_s':'s','value':'1'};idn=f.identity('simple.csv',raw)
  if cid=='READ01':
   b,n,a,rb,s=f.base();out=[];parsed={}
   for e in ('N','P'):
    rows=[r for t in [D(v) for v in f.REQUESTS] for r in a['profile_'+e][t]]
    header=list(rows[0]);raw=(',' .join(header)+'\n'+''.join(','.join(str(r[k]) for k in header)+'\n' for r in rows)).encode()
    u={'time_s':'s','coordinate_m':'m','domain_id':'1','x_surface':'1','x_particle_average':'1'}
    parsed[e]=c.read_csv_bytes(raw,header,f.identity(e+'.csv',raw),u,u)
   tr=c.timed_rows([{'time_s':D(t),'value':D(1)} for t in f.REQUESTS],'120')
   c.coverage(tr,tr,f.REQUESTS,f.REQUESTS,f.REQUESTS,'120')
   for e in ('N','P'):
    pp=c.profile_rows(parsed[e],{D(t) for t in f.REQUESTS},f.COORDS[e],1 if e=='N' else 3);out.append(len(pp))
   assert out==[255,255] and all(len(parsed[e])==255*241 for e in ('N','P'))
   return {'status':'RETURN_VALID_ROWS','rows_per_electrode':255*241,'profile_times':out},None
  if cid=='READ02':idn['sha256']='0'*64
  elif cid=='READ03':units={'time_s':'ms','value':'1'}
  elif cid=='READ04':head=['other','value']
  elif cid=='READ05':raw=b'time_s,value\n0\n';idn=f.identity('simple.csv',raw)
  elif cid=='READ06':raw=b'time_s,value\n0,NaN\n';idn=f.identity('simple.csv',raw)
  elif cid=='READ07':raw=b'time_s,value\n';idn=f.identity('simple.csv',raw)
  elif cid=='READ08':return c.timed_rows([{'time_s':D(0)},{'time_s':D(0)}],'1'),None
  elif cid=='READ09':return c.coverage([D(0)],[D(0),D(1)],['0','1'],['0','1'],['0','1'],'1'),None
  elif cid=='READ10':return c.coverage([D(0)],[D(0)],['0'],['0'],['0'],'1'),None
  elif cid in ('READ11','READ12'):
   a=f.data([D(0)]);rr=a['profile_N'][D(0)]
   if cid=='READ11':rr[0]['domain_id']=D(3)
   else:rr.pop()
   return c.profile_rows(rr,[D(0)],f.COORDS['N'],1),None
  return c.read_csv_bytes(raw,head,idn,units,{'time_s':'s','value':'1'}),None
 if cid.startswith('INIT'):
  ob,targets=f.init();conf,cons,expected=f.coeff()
  if cid=='INIT01':
   return c.compare_initialization_pair(ob,copy.deepcopy(ob),targets),None
  if cid=='INIT02':targets[0]['target']='0.001';ob['values']['inventory']['value']='0.001000001'
  elif cid=='INIT03':ob['values']['inventory']['value']='1.0000000011'
  elif cid=='INIT04':ob['time_s']='.1'
  elif cid=='INIT05':ob['provenance']={}
  elif cid=='INIT06':ob['values']['inventory']['unit']='mol'
  elif cid=='INIT07':conf['rtol']='1e-5'
  elif cid=='INIT08':cons['grade']='SETTINGS_ONLY'
  elif cid=='INIT10':cons['values']['rtol']['value']='2e-6'
  elif cid=='INIT11':
   right=copy.deepcopy(ob);ob['values']['inventory']['value']='.999999999';right['values']['inventory']['value']='1.000000001'
   return c.compare_initialization_pair(ob,right,targets),None
  elif cid=='INIT12':
   a=f.data([D(0)]);a['profile_N'][D(0)][0]['x_particle_average']+=D('.001')
   return c.initial_profile_uniformity(a['profile_N'][D(0)],a['profile_P'][D(0)],'.445','.581'),None
  if int(cid[4:])>=7:return c.verify_coefficient_evidence(conf,cons,expected),None
  return c.compare_initialization(ob,targets),None
 if cid.startswith('POLICY'):
  b,n,a,rb,s=f.base();ref=s['reference']
  if cid=='POLICY01':
   extra=f.data([D('100.001')])
   for key in ('global','N','P','profile_N','profile_P'):
    ref[key][D('100.001')]=extra[key][D('100.001')];ref[key]=dict(sorted(ref[key].items()))
  if cid in ('POLICY02','POLICY03'):
   delta=D('.001') if cid=='POLICY02' else D('.0010000000000000000001')
   for t in ref['P']:
    ref['P'][t]['phis_V']+=delta;ref['P'][t]['Eeq_V']+=delta
   return c.analyze(b,n,a,rb,s),f.producer_context(b,n,s)
  if cid in ('POLICY04','POLICY05'):
   delta=D('.0001') if cid=='POLICY04' else D('.000100000001')
   ref['profile_N'][D(120)][0]['x_surface']+=delta
  elif cid=='POLICY06':
   a['global'][D(120)]['Li_electrolyte_mol_m2']+=D('.001');return c.invariants(a['global'],a['N'],a['P']),None
  elif cid=='POLICY07':a['P'][D(120)]['phis_V']+=D('.000001');return c.invariants(a['global'],a['N'],a['P']),None
  elif cid=='POLICY08':ref['profile_N'][D(120)][0]['coordinate_m']+=D('.000001')
  return c.compare_policy(*compare_args(a,ref,s)),None
 if cid.startswith('PAIRED'):
  zero={D(0):D(0),D(2700):D(0),D(3600):D(0)};finite={D(0):D(0),D(2700):D('-.001'),D(3600):D('-.01')}
  if cid=='PAIRED02':finite={D(0):D(0),D(2700):D('-.0001'),D(3600):D('-.0002')}
  if cid=='PAIRED04':finite={D(0):D(0),D(2700):D('-.0005'),D(3600):D('-.001')}
  controls={'K':{'same_setting_pair':True,'validity':'VALID','nearzero_setting_without_sigma_sha256':f.H,'finite_setting_without_sigma_sha256':f.H,'nearzero':zero.copy(),'finite':finite.copy()}}
  validity={'evidence':'VALID','initialization':'PASS','effective_coefficients':'PASS','charge_conservation':'PASS','pair_initialization':'PASS','finite_direction':'CONSISTENT','nearzero_direction':'RESOLUTION_LIMITED','expected_k_settings':{'K':f.H}}
  if cid=='PAIRED03':controls['K']['finite']={D(0):D(0),D(2700):D('-.0001'),D(3600):D('-.02')}
  elif cid=='PAIRED05':controls={}
  elif cid=='PAIRED06':controls['K']['same_setting_pair']=False
  elif cid=='PAIRED07':finite.pop(D(2700))
  return c.paired_classification(zero,finite,controls,['K'],validity),None
 raise RuntimeError('UNMAPPED_CASE:'+cid)
def get_field(obj,path):
 path=path.replace('result.','',1).replace('return_value.','',1)
 for part in path.split('.'):
  if '[' in part:
   key,index=part[:-1].split('[');obj=obj[key][int(index)]
  else:obj=obj[part]
 return obj
def main():
 start=time.monotonic();c=load_exact('consumer');ctl=load_exact('control');results=[]
 seals={x['id']:x for x in json.loads((ROOT/'CONSUMER_INPUT_IDENTITIES.json').read_text())}
 controls=json.loads((ROOT/'fixture_inputs/CONTROL_INPUTS.json').read_text())
 if isinstance(controls,list):controls={x['id']:x for x in controls}
 target_names={n.name for name in ('consumer','control') for n in ast.parse((SOURCE/'candidate'/f'{name}.py.inactive.txt').read_text()).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}-{'number','require','decimal_context','reject','canonical_hash','finite_number','is_sha','require_refs'}
 (ROOT/'results/producers').mkdir(exist_ok=False)
 for case in [x for x in PLAN['cases'] if x['engine']=='Python']:
  cid=case['id'];reach=[];counts={};returned=[];context=None;out=None;reason=None;stage=None;error=None;proxy=None
  def trace(frame,event,arg):
   if event in ('call','return') and frame.f_code.co_filename.endswith('.inactive.txt'):
    name=frame.f_code.co_name
    if name in target_names:
     if event=='call':
      counts[name]=counts.get(name,0)+1
      if name not in reach:reach.append(name)
     else:returned.append(name)
  try:
   if cid.startswith(('AUTH','RESOURCE')):
    sys.setprofile(trace)
    try:wrapper=execute_control_case(cid,ctl,controls[cid])
    finally:sys.setprofile(None)
    out=wrapper.get('return_value');reason=wrapper['observed'];stage=wrapper['stage']
   else:
    proxy=VerificationProxy(c,seals[cid]['calls'],profile=trace);out,context=consumer_case(cid,proxy,case)
    if proxy.index!=len(seals[cid]['calls']):raise RuntimeError('FIXTURE_INPUT_INVOCATIONS_MISSING')
   if reason is not None:pass
   elif isinstance(out,dict) and out.get('errors'):reason=out['errors'][0]['reason'];stage=out['errors'][0].get('stage')
   elif cid=='CHARGE_R109':reason=out['native_completion']
   elif cid.startswith('CHARGE') and 'charge_budget' in out:reason=out['charge_budget']['status']
   elif cid in ('POLICY02','POLICY03'):reason=out['comparison']
   else:reason=out.get('status') if isinstance(out,dict) else None
   if stage is None:
    stage='analyze' if 'analyze' in returned else (returned[-1] if returned else None)
    if cid in ('CHARGE_R112','CHARGE_R113') and stage=='charge_balance':stage+=' return'
  except (c.EvidenceError,ctl.ContractError) as exc:reason=exc.reason;stage=exc.stage;error={'reason':reason,'stage':stage,'details':getattr(exc,'details',None)}
  except Exception as exc:reason='UNEXPECTED_HARNESS_EXCEPTION';error={'type':type(exc).__name__,'message':str(exc),'traceback':traceback.format_exc()}
  finally:sys.setprofile(None)
  required=case['target_functions']
  okay=reason==case['expected'] and all(x in reach for x in required)
  if case.get('expected_stage') is not None:okay=okay and stage==case['expected_stage']
  if cid=='INIT01':okay=okay and counts.get('compare_initialization_pair')==1 and counts.get('compare_initialization')==2
  if cid=='READ01':okay=okay and all(counts.get(k)==v for k,v in {'read_csv_bytes':2,'timed_rows':1,'coverage':1,'profile_rows':2}.items())
  if cid in ('AUTH01','RESOURCE16'):okay=okay and counts.get('execute_once')==1 and counts.get('authorize_execution')==1
  for field,value in case.get('additional_expected_fields',{}).items():
   try:okay=okay and get_field(out,field)==value
   except (KeyError,TypeError,IndexError):okay=False
  if case.get('expected_first_violation'):
   got=(out or {}).get('charge_budget',{}).get('interval_direction',{}).get('first_violation',{}) or {}
   okay=okay and all(got.get(k)==v for k,v in case['expected_first_violation'].items())
  if case.get('expected_interval_sign') and out:okay=okay and out['records'][-1]['interval_sign']==case['expected_interval_sign']
  if cid=='PAIRED04' and out:okay=okay and all(D(out[k])==D(v) for k,v in {'D_V':'.001','S_V_per_h':'.002','E_D_V':'0','E_S_V_per_h':'0'}.items())
  elapsed=time.monotonic()-start
  if elapsed>420:okay=False;error={'reason':'PYTHON_BUDGET_EXCEEDED'}
  record={'id':cid,'input_id':case['input_id'],'expected':case['expected'],'observed':reason,'expected_stage':case.get('expected_stage'),'observed_stage':stage,'reached_functions':reach,'function_call_counts':counts,'status':'PASS' if okay else 'FAIL','error':error,'elapsed_total_s':elapsed}
  if cid.startswith(('AUTH','RESOURCE')) and error is None:record['control_observation']=wrapper
  results.append(record)
  if context and cid in ('CHARGE01','CHARGE03','CHARGE_R109','POLICY02','POLICY03'):
   raw=f.raw_json(out);path=ROOT/'results/producers'/f'{cid}.json';path.write_bytes(raw)
   context['producer_sha256']=hashlib.sha256(raw).hexdigest();context['producer_bytes']=len(raw)
   (ROOT/'results/producers'/f'{cid}.context.json').write_bytes(f.raw_json(context))
  (ROOT/'results/PYTHON_RESULTS.json').write_bytes(f.raw_json({'status':'RUNNING' if okay else 'FAIL','cases':results,'unexecuted':[x['id'] for x in PLAN['cases'] if x['engine']=='Python' and x['id'] not in {r['id'] for r in results}]}))
  print(json.dumps(record,default=str),flush=True)
  if not okay:return 1
 (ROOT/'results/PYTHON_RESULTS.json').write_bytes(f.raw_json({'status':'PASS','count':len(results),'cases':results,'elapsed_s':time.monotonic()-start,'unexecuted':[]}))
 return 0
if __name__=='__main__':raise SystemExit(main())
