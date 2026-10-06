from pathlib import Path
import sys,json,math,io,contextlib
R=Path(__file__).resolve().parents[1];sys.path[:0]=[str(R/'source/scripts'),str(R/'source/docs/data/gen2_design_20261006/c1')]
import network_conductivity as nc
import constriction_reference as cr
from fv_sphere_chain import sphere_chain_R
out={'flux_tube':[],'sphere_chain':[]}
for s in (.05,.1,.2,.3,.4,.5,.6,.7,.8,.9):
 d=cr.solve_flux_tube(s,nr=160,nz=320,aspect=4.)
 a=d['s_eff'];RH=1/(2*a);psi=(1-a)**1.5
 out['flux_tube'].append(dict(s=s,R_fv=d['R_c'],R_mul=psi*RH,R_div=RH/psi,mul_error=abs(math.log(psi*RH/d['R_c'])),div_error=abs(math.log(RH/psi/d['R_c']))))
for s in (.3,.45,.5,.7):
 h=math.sqrt(1-s*s);delta=2-2*h
 A={1:dict(type=1,x=0.,y=0.,z=0.,radius=1.),2:dict(type=1,x=0.,y=0.,z=2*h,radius=1.)}
 C=[dict(id1=1,id2=2,contact_area=math.pi*s*s,delta=delta)]
 with contextlib.redirect_stdout(io.StringIO()):
  n0=nc.build_network(A,C,[1],1.,10.,type_map={1:'SE'},box_x=10.,box_y=10.)
  n12=nc.build_network(A,C,[1],1.,10.,type_map={1:'SE'},box_x=10.,box_y=10.,hertz_constriction='mikic_psi_multiply',bulk_model='sphere_segment')
 vals=[sphere_chain_R(s,n)[0] for n in (100,200,400)]
 ex=2*vals[-1]-vals[-2];r0=n0['edges'][0]['R_total'];r12=n12['edges'][0]['R_total']
 row=dict(s=s,FV_R=vals,R_extrap=ex,R_H0=r0,R_H12=r12,conductance_H12_relative_error=ex/r12-1,true_conductance_between_models=min(1/r0,1/r12)<=1/ex<=max(1/r0,1/r12))
 out['sphere_chain'].append(row);print(row,flush=True)
out['multiply_better_all']=all(r['mul_error']<r['div_error'] for r in out['flux_tube'])
(R/'evidence/reference_checks.json').write_text(json.dumps(out,indent=2,default=lambda x:x.item()),encoding='utf8')
print('Multiply beats divide at all 10 reference points:',out['multiply_better_all'])
