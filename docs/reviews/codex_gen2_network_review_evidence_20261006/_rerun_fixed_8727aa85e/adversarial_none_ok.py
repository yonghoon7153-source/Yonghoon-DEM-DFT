"""Independent synthetic probes using pinned production functions. No DEM campaign."""
from pathlib import Path
import sys, json, math, copy, contextlib, io
R=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(R/'source/scripts'),str(R/'source/webapp')]
import numpy as np
import network_conductivity as nc
import tau_flux as tf
import pipeline_service as ps
def quiet(fn,*a,**kw):
 with contextlib.redirect_stdout(io.StringIO()): return fn(*a,**kw)
def e(i,j,g):
 return dict(id1=i,id2=j,R_total=1/g,R_bulk=1/g,R_constriction=0.)
def net(edges):
 return dict(nodes=list({v for x in edges for v in (x['id1'],x['id2'])}),edges=edges,bottom={0},top={1},scale=1.,plate_z=1.,box_x=1000.,box_y=1000.)
out={}
# A resistor to each electrode for every free node: exact G=sum(gB*gT/(gB+gT)).
# One high-conductance dead end loads rhs norm but carries zero current.
cg=[]
for high in (1e6,1e8,1e10,1e12,1e14):
 edges=[e(0,2,high)]
 for i in range(3,30004): edges += [e(0,i,1.),e(i,1,1.)]
 n=net(edges);G,q=quiet(nc.solve_network,n)
 info=n['solve_info']['full'];exact=30001/2
 cg.append(dict(high=high,G=G,q=q,exact_G=exact,rel_error=(G/exact-1) if G is not None else None,info=info))
out['cg_dead_end']=cg
direct=[]
for high in (1e6,1e8,1e10,1e12,1e14,1e15,1e16):
 n=net([e(0,2,high),e(2,1,1.)]);G,q=quiet(nc.solve_network,n)
 exact=high/(1+high)
 direct.append(dict(high=high,G=G,exact_G=exact,rel_error=G/exact-1 if G else None,info=n['solve_info']['full']))
out['direct']=direct
# Produce the baseline through the actual builder and solve wrappers.
A={i:dict(type=1,x=0.,y=0.,z=float(i),radius=1.) for i in range(21)}
C=[dict(id1=i,id2=i+1,contact_area=.01,delta=.05) for i in range(20)]
base={cm:quiet(nc._run_all_networks,A,C,[1],[],{1:'SE'},1.,20.,10.,10.,None,contact_mode=cm) for cm in ('hertzian','physics')}
phi=21*4/3*math.pi/2000
ledger=dict(thickness_um=20.,thickness_mass_conserving_um=20.,phi_se_mass_conserving=phi)
def observe(du):
 row=tf.ion_columns(du,ledger,100.)
 return dict(statuses={m:row['ion_net_status_'+m] for m in tf.MODES},tau2={m:row['tau2_ion_'+m] for m in tf.MODES},axes=tf.generation_axes(row),stop9=ps.network_generation2_problems(du,row,tf),row=row)
out['baseline']=observe(base)
mut=[]
for label,target,key,val in [
 ('H0 bulk relabelled sphere_segment','hertzian','bulk_model','sphere_segment'),
 ('H0 constriction relabelled Mikic','hertzian','resistance_model','mikic'),
 ('unknown electrode all','all','electrode_model','DIRICHLET_TYPO'),
 ('unknown area','physics','area_rule','physics_g9'),
 ('unknown psi','physics','psi_placement','multiply_TYPO'),
 ('missing psi','physics','psi_placement',None),
 ('missing area','physics','area_rule',None),
 ('physics bulk relabelled sphere_segment','physics','bulk_model','sphere_segment')]:
 du=copy.deepcopy(base)
 targets=[du['hertzian'],du['physics'],du['hertzian']['hertz_h12']] if target=='all' else [du[target]]
 for x in targets:
  if val is None: x.pop(key,None)
  else:x[key]=val
 o=observe(du);o['mixed_with_baseline']=tf.generation_mixing_problem([out['baseline']['row'],o['row']]);o['label']=label;mut.append(o)
out['generation_mutants']=mut
# Known Rc=0 opening vs analytic contraction, no ambiguity about missing data.
es=[dict(id1=0,id2=2,R_total=2.,R_bulk=2.,R_constriction=0.),dict(id1=2,id2=1,R_total=3.,R_bulk=2.,R_constriction=1.),dict(id1=0,id2=1,R_total=12.,R_bulk=2.,R_constriction=10.)]
n=net(es);G,q=quiet(nc.solve_network,n,mode='constriction_only')
out['zero_Rc']=dict(G=G,correct_contracted_G=1.1,rel_error=(None if G is None else G/1.1-1),info=n['solve_info']['constriction_only'])
(R/'evidence').mkdir(exist_ok=True)
(R/'evidence/adversarial.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf8')
print(json.dumps({k:v for k,v in out.items() if k not in ('baseline','generation_mutants')},indent=2))
for m in mut:print(m['label'],m['statuses'],'stop9=',m['stop9'],'mixed=',m['mixed_with_baseline'])
