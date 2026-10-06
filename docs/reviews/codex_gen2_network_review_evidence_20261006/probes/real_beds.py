"""Pinned raw DEM dumps, independent loader; graph solves only, not DEM/MPM."""
from pathlib import Path
import gzip,sys,json,io,contextlib,math,time
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'source/scripts'))
import network_conductivity as nc
def load(p,tag):
 with gzip.open(p,'rt') as f:
  for line in f:
   if line.startswith(tag):
    head=line[len(tag):].split();break
  return [dict(zip(head,x.split())) for x in f if x.strip() and not x.startswith('ITEM')]
out={}
for name,folder,suffix,tm,plate,box in [('real14','real14_reference_20260928','2060000',{1:'AM_P',2:'AM_S',3:'SE'},.0302845,.05),('case15','case15_corner_20261001','v4_1710000',{1:'AM_P',2:'SE'},.0191455,.1)]:
 root=R/'source/docs/data'/folder
 A={int(r['id']):dict(type=int(r['type']),**{k:float(r[k]) for k in ('x','y','z','radius')}) for r in load(root/('atom_'+suffix+'.liggghts.gz'),'ITEM: ATOMS')}
 C=[dict(id1=int(float(r['c_cpl[7]'])),id2=int(float(r['c_cpl[8]'])),contact_area=float(r['c_cpl[22]']),delta=float(r['c_cpl[23]'])) for r in load(root/('contact_'+suffix+'.liggghts.gz'),'ITEM: ENTRIES')]
 se=[k for k,v in tm.items() if v=='SE'];arms={};log=io.StringIO()
 for arm,opts in [('H0',{}),('g1_mul',dict(contact_mode='physics',area_rule='physics_g1')),('g2',dict(contact_mode='physics')),('H12',dict(hertz_constriction='mikic_psi_multiply',bulk_model='sphere_segment'))]:
  with contextlib.redirect_stdout(log):
   n=nc.build_network(A,C,se,1000.,plate,box_x=box,box_y=box,type_map=tm,**opts)
   solves={mode:nc.solve_network(n,mode=mode) for mode in ('full','bulk_only','constriction_only')}
  info=n['solve_info'];bal={m:abs(v['I_bottom']+v['I_top'])/max(abs(v['I_bottom']),abs(v['I_top']),1e-300) if v['I_bottom'] is not None else None for m,v in info.items()}
  arms[arm]=dict(solves=solves,solve_info=info,relative_current_imbalance=bal,edges=len(n['edges']),nodes=len(n['nodes']),clamp=n['n_clamp_zero'],floor=n['n_floor_only'],binding=n['area_binding_counts_physics'],resistance_range=[min(e['R_total'] for e in n['edges']),max(e['R_total'] for e in n['edges'])])
  print(name,arm,solves,bal,flush=True)
 out[name]=dict(atoms=len(A),contacts=len(C),arms=arms)
 (R/'evidence'/('real_'+name+'.log')).write_text(log.getvalue(),encoding='utf8')
 (R/'evidence/real_beds.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf8')
