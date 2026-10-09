"""Self-authored inert fixtures. Contains no candidate import or invocation."""
from decimal import Decimal as D, localcontext, getcontext
from pathlib import Path
import json, hashlib, copy, csv, io
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT.parent
getcontext().prec=50
F=D('96485.33212')
H='a'*64
POLICY=json.loads((SOURCE/'contracts/POLICY_VARIANTS.json').read_text(encoding='utf-8-sig'))
REQUESTS=POLICY['request_vectors']['sparse_0_120']['tokens_s']
COORDS={'N':[D('0.000052')*D(i)/D(240) for i in range(241)],'P':[D('.000077')+D('.000044')*D(i)/D(240) for i in range(241)]}
def identity(name,raw):
 return {'path':'fixture/'+name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def raw_json(obj):
 return json.dumps(obj,default=str,ensure_ascii=False,separators=(',',':')).encode()
def init():
 target=[{'name':'inventory','unit':'mol/m^2','target':'1','abs_tol':'1e-9','rel_tol':'1e-6'}]
 observed={'phase':'consistent_initialization','time_s':'0','provenance':{'stage':'POST_CONSISTENCY_BEFORE_POSITIVE_INTEGRATION','one_approved_solve':True,'raw_identity':'fixture','installed_mapping_sha256':H},'values':{'inventory':{'value':'1','unit':'mol/m^2'}}}
 return observed,target
def coeff():
 exp={'configured':{'rtol':'1e-6'},'consumed':{'rtol':{'value':'1e-6','abs_tol':'1e-15','unit':'1'}}}
 con={'grade':'INSTALLED_EQUATION_AND_NUMERICAL_READBACK','raw_identity':identity('coefficient_readback.json',b'{"rtol":"1e-6","unit":"1"}'),'mapping_sha256':H,'values':{'rtol':{'value':'1e-6','unit':'1'}}}
 return exp['configured'].copy(),con,exp
def data(times,j=D('.25001')):
 out={'global':{},'N':{},'P':{},'profile_N':{},'profile_P':{},'charge':[]}
 with localcontext() as c:
  c.prec=50
  for t in times:
   q=j*t;n=D(1)-q/F;p=D(1)+q/F
   out['global'][t]={'time_s':t,'Li_N_mol_m2':n,'Li_P_mol_m2':p,'Li_electrolyte_mol_m2':D(1)}
   for e,x,v in [('N',D('.445'),D(0)),('P',D('.581'),D(3))]:
    out[e][t]={'time_s':t,'phis_V':v,'Eeq_V':v,'etamid_V':D(0),'phil_V':D(0)}
    out['profile_'+e][t]=[{'time_s':t,'coordinate_m':xx,'domain_id':D(1 if e=='N' else 3),'x_surface':x,'x_particle_average':x} for xx in COORDS[e]]
   out['charge'].append({'time_s':t,'j':j,'RN':j,'RP':-j,'I':j,'LiN':n,'LiP':p,'LiE':D(1)})
 return out
def base(protect=False):
 times=sorted(set([D(t) for t in REQUESTS]+[D('.00015'),D('100.001')]))
 if protect:times=[t for t in times if t<=D(90)]+[D('90.1')]
 ref=data([D(t) for t in REQUESTS]);a=data(times)
 global_id=identity('global.json',raw_json(list(a['global'].values())))
 charge_id=identity('charge.json',raw_json(a['charge']))
 grid_id=identity('grid.json',raw_json([str(t) for t in times]))
 a['source_identities']={'global':global_id,'charge':charge_id}
 units={'time_s':'s','j':'A/m^2','RN':'A/m^2','RP':'A/m^2','I':'A','LiN':'mol/m^2','LiP':'mol/m^2','LiE':'mol/m^2'}
 binding={'run_id':'fixture_R1','variant_id':'P1','manifest_sha256':H,'end_s':'120','common_requested_times_s':REQUESTS}
 native={'raw_binding_validated':True,'child_rc':0,'fatal':False,'reason':'GUARD_STOP' if protect else 'NORMAL_END','last_stored_s':str(times[-1]),'stored_times_s':[str(t) for t in times],'stored_grid_identity':grid_id}
 if protect:native['guard_pair']={'t_minus':'90','t_plus':'90.1'}
 initial,targets=init();configured,consumed,expected=coeff()
 proof={'run_id':binding['run_id'],'manifest_sha256':H,'normalized_units':units,'global_li_unit':'mol/m^2','native_grid_identity':grid_id,'global_identity':global_id,'charge_identity':charge_id}
 rb={'source_evidence':[global_id,charge_id,grid_id],'units_status':'PASS','guard_status':'PASS','initial':initial,'initial_targets':targets,'xN_target':'.445','xP_target':'.581','configured':configured,'consumed':consumed,'coefficient_expected':expected,'charge_provenance':proof,'area_m2':'1','quadrature_bound_C_m2':'0','quadrature_provenance':{'uniform_over_all_prefixes':True,'integrands':['j','RN','-RP'],'bound_method_verified':True,'raw_identity':'synthetic_linear_exact','grid_sha256':grid_id['sha256']}}
 spec={'reference':ref,'requests_current':REQUESTS,'requests_reference':REQUESTS,'common_requests':REQUESTS,'safe_end_s':'90' if protect else '120'}
 return binding,native,a,rb,spec
def charge_args(a,n,rb,spec,end='120'):
 return (a['charge'],rb['area_m2'],rb.get('quadrature_bound_C_m2')),{'global_rows':a['global'],'native_times_s':n['stored_times_s'],'configured_end_s':end,'actual_end_s':n['last_stored_s'],'safe_end_s':spec['safe_end_s'],'native_reason':n['reason'],'source_binding':rb['charge_provenance']}
def sync_li(a,index,field,value):
 row=a['charge'][index];row[field]=value
 a['global'][row['time_s']][{'LiN':'Li_N_mol_m2','LiP':'Li_P_mol_m2','LiE':'Li_electrolyte_mol_m2'}[field]]=value
def rebind(b,n,a,rb):
 """Bind synthetic raw normalized inputs after intended value mutations."""
 gid=identity('global.json',raw_json(list(a['global'].values())))
 cid=identity('charge.json',raw_json(a['charge']))
 nid=identity('grid.json',raw_json(n['stored_times_s']))
 a['source_identities']={'global':gid,'charge':cid};n['stored_grid_identity']=nid
 rb['source_evidence']=[gid,cid,nid]
 rb['charge_provenance'].update(global_identity=gid,charge_identity=cid,native_grid_identity=nid)
 rb['quadrature_provenance']['grid_sha256']=nid['sha256']
def producer_context(binding,native,spec):
 expected={**binding,'required_count':len(REQUESTS),'phase_limits_s':{'native':7200,'analysis':900},'overall_limit_s':9000}
 n={'returned':True,'invocation_succeeded':True,'new_error':False,'within_limits':True,'rc':0,'exception':None,'fatal':False,'record_errors':[],'run_id':binding['run_id'],'variant_id':binding['variant_id'],'manifest_sha256':H,'elapsed_s':1,'stored_times_s':native['stored_times_s'],'final_time_s':native['last_stored_s'],'stored_grid_identity':native['stored_grid_identity'],'termination':'NORMAL_END_MATCHED' if native['reason']=='NORMAL_END' else 'PROTECTIVE_STOP_MATCHED','active_guards':[] if native['reason']=='NORMAL_END' else ['fixtureguard'],'stop_pair_status':'MATCHED_SAME_OPERATOR_UNITS_DOMAIN','no_post_stop_integration':True,'stop_reason':'fixture'}
 if 'guard_pair' in native:n['guard_pair']=native['guard_pair']
 return {'Expected':expected,'Native':n,'Analysis':{'rc':0,'returned':True,'record_errors':[],'elapsed_s':1},'Completion':{'preservation':'PASS','process_cleanup':'PASS','policy_preservation':'PASS','resource_recording':'PASS','overall_elapsed_s':2,'record_errors':[]}}
