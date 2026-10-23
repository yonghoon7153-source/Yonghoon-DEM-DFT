#!/usr/bin/env python3
import importlib.util,json,math
from pathlib import Path
B=Path(__file__).resolve().parent

def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
old=load('old',B/'baseline/make_mixer_deck.py');new=load('new',B/'scripts/make_mixer_deck.py')
out={'kind':'synthetic arithmetic only; no simulation or fitted threshold'}
for label,g in [('old',old),('new',new)]:
 p=g.plan(100000,cgf=151.4)
 a=g.gm_arm({'AM_P':1e-200,'AM_S':1e-200,'SE':1},gamma_wall=.0256,bo_se=g.BO_BASE)
 m=g.ced_matrix_geomean(a,p['d'])
 def force(i,j):
  names=list(g.TYPES)+[g.WALL];ti,tj=names[i],names[j]
  return 4.5*math.pi**3*g.rstar_pair(ti,tj,p['d'])**2*m[i][j]**3/g.estar_pair(ti,tj,g.E_PHASE)**2
 out[label+'_underflow']={'AM_P_CED':m[0][0], 'Fpp_Fss':force(0,0)/force(2,2),'hand_ratio':9e-200}
# The ceiling scales as Bo^(2/3); evaluate declared inputs, do not choose a physical calibration.
g=new;caps=[]
for gen in ['gen1','lab20261014']:
 for bo in [637.32,850.0]:
  p=g.plan(100000,cgf=151.4,dens_gen=gen)
  a=g.gm_arm({'AM_P':1.,'AM_S':1.,'SE':1.},gamma_wall=g.gm_wall_from_ncm(1.),bo_se=bo,rho_uncoated_ncm=1.)
  try:
   m=g.ced_matrix_geomean(a,p['d'],dens=p['dens'])
   names=list(g.TYPES)+[g.WALL]
   rows=[(g.pair_overlap(m[i][j],ti,tj,p['d'],g.E_PHASE),ti,tj) for i,ti in enumerate(names) for j,tj in enumerate(names) if i<=j and (ti,tj)!=(g.WALL,g.WALL)]
   maximum=max(rows)
   caps.append({'dens_gen':gen,'bo':bo,'max_fraction':maximum[0],'pair':maximum[1:],'bo_at_static_1pct_by_power_law':bo*(.01/maximum[0])**1.5})
  except SystemExit as e:
   caps.append({'dens_gen':gen,'bo':bo,'rejected':str(e)})
out['MXD2_07_ceiling_diagnostic']=caps
(B/'analytic-results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
