from pathlib import Path
import sys,json,copy,ast
R=Path(__file__).resolve().parents[1];K=R/'source/docs/data/ps45_unload_20261009';sys.path.insert(0,str(K))
import ul_reader as u,ul_lib as l,ul_s3 as s,ul_observers as o
P=l.load_params();E=R/'evidence/observer_cases';E.mkdir(parents=True,exist_ok=True)
out={}
spec={'W':5000,'dt':1e-6,'steps':u._ladder([.20,.25,.30,.35],[1.2,.8,.6,.4]),'summary':'TIMEOUT'}
root=E/'malformed';d=Path(u._mk_arm(str(root),u.B73,'UB',spec,P))
before=u.arm_verdict(str(d),u.B73,'UB',P,root=str(root))
run=u.read_run(str(d),P);target=run['steps'][2];step=target['step'];a=d/'dump'/f'atom_{step}.dump'
txt=a.read_text();lines=txt.splitlines();ix=next(i for i,x in enumerate(lines) if x.startswith('ITEM: ATOMS'))
rows=[x.split() for x in lines[ix+1:]];cols=lines[ix].split()[2:];fz=cols.index('fz')
rows[0][fz]='0.001'
bad='\n'.join(lines[:ix+1]+[' '.join(x) for x in rows])+'\n';a.write_text(bad,encoding='utf8')
badver=u.arm_verdict(str(d),u.B73,'UB',P,root=str(root))
rows[0][fz]='nan';a.write_text('\n'.join(lines[:ix+1]+[' '.join(x) for x in rows])+'\n',encoding='utf8')
parsed=l.read_dump(str(a),'custom');nanver=u.arm_verdict(str(d),u.B73,'UB',P,root=str(root))
out['nonfinite_atom_salvaged']={'before':before,'finite_bad_force':badver,'parsed':parsed,'nan_result':nanver,'s3':u._s3_at(str(d),step,target['plate_z'],{1,2,3,4,5})}
assert before['primary_status']=='OK' and badver['primary_status']=='UNIDENTIFIED' and not parsed['ok'] and nanver['primary_status']=='OK'
# The timestamp written INSIDE a wall file must equal its named window, not just be parseable.
# Restore the original valid atom bytes so the time mutation is independent of NaN.
a.write_text(txt,encoding='utf8')
w=d/'dump'/f'wall_{step}.dump';wl=w.read_text().splitlines();wl[1]=str(step-100000);w.write_text('\n'.join(wl)+'\n',encoding='utf8')
out['wrong_wall_timestamp']={'file_step':step-100000,'requested_step':step,'rows_accepted':u._wall_rows(str(w)),'verdict':u.arm_verdict(str(d),u.B73,'UB',P,root=str(root))}
assert out['wrong_wall_timestamp']['verdict']['primary_status']=='OK'
wl[1]=str(step);w.write_text('\n'.join(wl)+'\n',encoding='utf8')
for frame in [a,d/'dump'/f'contact_{step}.dump']:
    lines=frame.read_text().splitlines();lines[1]=str(step-100000);frame.write_text('\n'.join(lines)+'\n',encoding='utf8')
out['wrong_atom_contact_timestamps']=u._s3_at(str(d),step,target['plate_z'],{1,2,3,4,5})
assert out['wrong_atom_contact_timestamps']['status']=='PASS'
# C4 explicitly freezes THREE complete UK windows. One finite row is accepted.
base=E/'one_uk';p=base/u.B73/'RJ/UK/ul_windows.csv';p.parent.mkdir(parents=True,exist_ok=True)
cs=P['records']['windows_cols'];row={x:'0' for x in cs};row['ke_rot_avg']='1e-3';row['step']='1';row['w']='1'
p.write_text(','.join(cs)+'\n'+','.join(row[x] for x in cs)+'\n',encoding='utf8')
out['one_uk_row']=u.kebase(str(base),u.B73,P,write=False)
assert out['one_uk_row']['s2_limit'] is not None
# The actual low-gravity total force must use low-gravity normalization if C2 means m*g.
A=[{'id':1,'z':.001,'radius':.0005,'mass':1e-6,'fx':0.,'fy':0.,'fz':-1e-6*9.81e-6}]
out['gravity_floor']={'g_default':s.s3_residual(A,[],{1},.1,atom_step=1,contact_step=1),'g_actual':s.s3_residual(A,[],{1},.1,atom_step=1,contact_step=1,g=9.81e-6)}
# C_all is required to be invariant, but helper is computed from the current radii/set.
A=[{'id':i,'z':.001,'radius':.0005} for i in range(1,6)]
out['fixed_volume']={'full':o.eps_sphere(A,{1,2,3,4,5},.0025,.1),'lost_one':o.eps_sphere(A[:-1],{1,2,3,4,5},.0025,.1)}
out['observer_production_calls']={name:[] for name in ['eps_sphere','w_proxy']}
for path in K.glob('*.py'):
    tree=ast.parse(path.read_text(encoding='utf8'))
    for node in ast.walk(tree):
        if isinstance(node,ast.Call):
            name=getattr(node.func,'attr',getattr(node.func,'id',None))
            if name in out['observer_production_calls']:out['observer_production_calls'][name].append({'file':path.name,'line':node.lineno})
(R/'evidence/observer_adversarial.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'malformed_input':{'before':before['primary_status'],'bad_force':badver['primary_status'],'nan':nanver['primary_status'],'parser_ok':parsed['ok'],'rho':nanver['rho_pct']},'wrong_wall_step_accepted':out['wrong_wall_timestamp']['rows_accepted'] is not None,'one_uk_s2':out['one_uk_row']['s2_limit'],'gravity_floor':out['gravity_floor'],'calls':out['observer_production_calls']},ensure_ascii=False,indent=2))
