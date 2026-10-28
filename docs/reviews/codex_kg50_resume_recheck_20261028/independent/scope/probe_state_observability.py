from pathlib import Path
import hashlib,json
out=Path(__file__).resolve().parent
# Synthetic kinematic counterexample only: not a DEM trajectory or physical run.
a=[dict(id=1,type=1,mass=1.0,radius=0.5,x=0.0,y=0.0,z=0.0,vx=1.0,vy=0.0,vz=0.0,omegax=0.0,omegay=0.0,omegaz=0.0),dict(id=2,type=2,mass=1.0,radius=0.5,x=1.0,y=0.0,z=0.0,vx=0.0,vy=1.0,vz=0.0,omegax=0.0,omegay=0.0,omegaz=0.0)]
b=[dict(p) for p in a]
b[0].update(x=100.0,vx=0.0,vy=1.0)
b[1].update(type=1,radius=0.7,vx=1.0,vy=0.0)
c=[dict(p) for p in a];c[0]['omegaz']=123.0
ke=lambda ps:sum(0.5*p['mass']*sum(p[k]**2 for k in ('vx','vy','vz')) for p in ps)
fields='id type x y z radius vx vy vz'.split()
project=lambda ps:[[p[k] for k in fields] for p in sorted(ps,key=lambda p:p['id'])]
r={'kind':'synthetic arithmetic and field projection, not LIGGGHTS execution','ke_not_state_identity':{'N_A':len(a),'N_B':len(b),'KE_A_J':ke(a),'KE_B_J':ke(b),'different_fields':['positions','velocity vectors','type','radius'],'equal_KE':ke(a)==ke(b),'identical_states':a==b},'current_sel_ignores_rotation':{'source':'scripts/resume_ckpt.sh:646','fields':fields,'omega_A':a[0]['omegaz'],'omega_C':c[0]['omegaz'],'equal_projected_atoms':project(a)==project(c),'equal_KE':ke(a)==ke(c)},'limits':['No inference about actual current KG50 particles or contact history','No DEM execution','Same-checkpoint two-reader agreement is an internal consistency check, not an independent pre-checkpoint physical-state comparison']}
assert r['ke_not_state_identity']['equal_KE'] and not r['ke_not_state_identity']['identical_states']
assert r['current_sel_ignores_rotation']['equal_projected_atoms']
(out/'state_observability.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(r,ensure_ascii=False,indent=2))
