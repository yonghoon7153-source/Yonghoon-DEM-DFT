"""Actual production solver on analytic networks. No solver mocking or campaign."""
from pathlib import Path
import sys,json,contextlib,io
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'source/scripts'))
import network_conductivity as nc
def e(i,j,g):return dict(id1=i,id2=j,R_total=1/g,R_bulk=1/g,R_constriction=0.)
def net(es):return dict(nodes=list({v for e in es for v in (e['id1'],e['id2'])}),edges=es,bottom={0},top={1},scale=1.,plate_z=1.,box_x=1000.,box_y=1000.)
out=[]
for high in (1e9,1e10,1.15e10,1.16e10,1.165e10,1.17e10,1.18e10,1.2e10,1.3e10,1.4e10,1.5e10,1e11,1e14):
 es=[e(0,2,high),e(0,3,1.),e(3,1,1.),e(0,4,1.),e(4,1,19.)]
 for i in range(5,30004):es.extend([e(0,i,1e-30),e(i,1,1e-30)])
 n=net(es);log=io.StringIO()
 with contextlib.redirect_stdout(log):G,q=nc.solve_network(n,return_field=False)
 info=n['solve_info']['full'];exact=.5+19/20
 out.append(dict(high=high,G=G,exact_G=exact,rel_error=None if G is None else G/exact-1,certificate=info,certificate_problem=nc.certificate_problem(info),log=log.getvalue()))
 print(high,G,'error',out[-1]['rel_error'],'method',info['method'],'cons',info['conservation_rel'],'res',info['residual_rel'],flush=True)
(R/'evidence/numerics.json').write_text(json.dumps(out,indent=2),encoding='utf8')
