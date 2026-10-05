"""Actual network functions on a synthetic graph; no DEM/MPM campaign."""
from pathlib import Path
import sys,json,math,contextlib,io
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'source/scripts'))
import network_conductivity as nc
out=[]
for nz in (20,40,80):
 atoms={};idx={};nr=3;contacts=[]
 for z in range(nz):
  for y in range(nr):
   for x in range(nr):
    i=len(atoms)+1;idx[x,y,z]=i;atoms[i]=dict(type=1,x=2*x+1.,y=2*y+1.,z=2*z+1.,radius=1.)
 for (x,y,z),i in idx.items():
  for pos in (((x+1)%nr,y,z),(x,(y+1)%nr,z),(x,y,z+1)):
   if pos in idx:contacts.append(dict(id1=i,id2=idx[pos],contact_area=.01,delta=0.))
 # Positive contact_area just keeps identical adjacency. CF ignores area/Rc.
 log=io.StringIO()
 with contextlib.redirect_stdout(log):
  net=nc.build_network(atoms,contacts,[1],1.,2.*nz,box_x=2.*nr,box_y=2.*nr,type_map={1:'SE'})
  sol=nc.solve_network(net,mode='bulk_only')
 G,q=sol
 phi=math.pi/6;T=phi/q
 out.append(dict(nz=nz,nodes=len(atoms),edges=len(net['edges']),L=2*nz,boundary=net['boundary_rule'],G=G,q=q,phi=phi,T=T,analytic_centerplane_limit=2/3*(nz-1)/nz,log=log.getvalue()))
assert all(x['T']<1 for x in out)
(R/'evidence/bulk_counterexample.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps(out,indent=2))
