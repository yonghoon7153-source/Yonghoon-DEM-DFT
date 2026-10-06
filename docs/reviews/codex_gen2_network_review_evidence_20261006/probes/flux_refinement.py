from pathlib import Path
import sys,json,math
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'source/scripts'))
import constriction_reference as cr
rows=[]
for nr,nz in ((160,320),(300,600),(400,800),(600,1200)):
 d=cr.solve_flux_tube(.05,nr=nr,nz=nz,aspect=4.)
 s=d['s_eff'];psi=(1-s)**1.5;rm=psi/(2*s);rd=1/(2*s*psi)
 r=dict(nr=nr,nz=nz,s=s,R_fv=d['R_c'],mul=rm,div=rd,mul_better=abs(math.log(rm/d['R_c']))<abs(math.log(rd/d['R_c'])))
 rows.append(r);print(r,flush=True)
 (R/'evidence/flux_refinement.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
