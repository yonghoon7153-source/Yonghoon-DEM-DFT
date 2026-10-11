"""Read-only review arithmetic and an actual diagnostic-function call; no DEM run."""
from pathlib import Path
import importlib.util, json, math, hashlib, urllib.request
import numpy as np
R=Path(__file__).resolve().parents[1]
p=R/'source/scripts/plane_load_share.py'
s=importlib.util.spec_from_file_location('sealed_plane',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
# Five equal spheres in a vertical chain. Body weight is explicitly known;
# each inner particle has upward pair-force sum mg, hence total force zero.
n=5;radius=0.00051;density=2000.;g=9.81
weight=density*4*math.pi*radius**3/3*g
atoms=dict(id=np.arange(1,n+1),type=np.full(n,3),z=np.arange(.5,n,.1)[:n])
atoms['z']=(np.arange(n)+.5)*.001
atoms['radius']=np.full(n,radius)
# id1 lower, id2 upper. Lower receives negative z force.
edge_force=weight*np.array([14.,13.,12.,11.])
f=np.column_stack([np.zeros(4),np.zeros(4),-edge_force])
contacts=dict(id1=np.arange(1,5),id2=np.arange(2,6),f=f,fn=f)
res=m.compute(atoms,contacts,{3:'SE'},.005,(.05,.05,'input_params.json'),1000)
net=np.zeros((n,3));np.add.at(net,np.arange(4),f);np.add.at(net,np.arange(1,5),-f)
inner=(atoms['z']>=2*radius)&(atoms['z']<=.005-2*radius)
physical=net[inner].copy();physical[:,2]-=weight
body=dict(weight_N=weight,inner_ids=atoms['id'][inner].tolist(),pair_only_residual=res['balance_residual'],true_total_force_max_N=float(np.abs(physical).max()),S3_threshold=1e-3,S3_pass=res['balance_residual']<=1e-3,source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),comment='Exact static force balance; kinematic DEM simulation not performed')
# Net zero is not separation: two simultaneous compressive/tensile wall contacts.
separation=dict(wall_normal_forces_N=[1.,-1.],net_force_N=0.,contact_count=2,registered_P_nonpositive=True,actually_separated=False)
# R_M is saved AFTER crossing. A monotone branch is already below P_meas.
gravity_branch=dict(Pmeas_MPa=1.,primary_crossing_pressures_MPa=[1.2,.8],R_M_after_two_steps_MPa=.6,after_g_switch_MPa=.7,subsequent_lift_pressures_MPa=[.5,.3],bracket_exists=False,comment='Admissible counterexample values, not measured bed predictions')
# Quasi-static endpoint quadrature need not equal time-resolved moving-platen work.
A=2.5e-9;dh=1e-6
work=dict(area_m2=A,lift_m=dh,endpoint_pressures_Pa=[10e6,1e6],moving_pressure_Pa=10e6,endpoint_proxy_J=.5*(10e6+1e6)*A*dh,true_movement_work_J=10e6*A*dh,relative_underestimate=.45,comment='Illustrative force history: relaxation takes place at fixed height, not a simulation')
# Complete windows in R and k0.
windows=dict(R_steps=2000,W_steps=5000,complete_R_windows=2000//5000,k0_windows=2,available_adjacent_mean_differences=1,required_consecutive_drift_passes=2)
out=dict(S3_body_force=body,separation=separation,gravity_branch=gravity_branch,work=work,windows=windows)
dest=R/'evidence/counterexamples.json';dest.write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf8')
print(json.dumps(out,indent=2,ensure_ascii=False))
