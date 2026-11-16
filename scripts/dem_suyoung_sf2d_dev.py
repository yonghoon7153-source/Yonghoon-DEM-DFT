#!/usr/bin/env python3
"""Small CPU S/F development comparison; normalized units, not paper data.

Quadratic MLS/APIC transfer and corotated/log-strain plastic projection follow
the existing mpm2d_plastic.py development scheme. Both arms use this one kernel.
S has one nodal field. F has one per original disk, with support-node contact.
Contact uses mass-gradient normals and sequential inelastic Coulomb impulses.
Finite-grid early contact and multi-body order/residuals remain development
limitations: no calibrated material, convergence or unloading claim is made.
Only synthetic, procedurally generated disks are accepted; no raw-data loader.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import sys
import time

import numpy as np

FLOOR, LEFT, RIGHT, TOP0 = .16, .10, .90, .80
E, NU, YIELD, RHO = 1.0, .30, .02, 1.0
MU = E / (2 * (1 + NU))
LAM = E * NU / ((1 + NU) * (1 - 2 * NU))


def seed_disks(grid):
    """Same synthetic four-disk state for S and F; immutable disk IDs."""
    h = 1.0 / grid
    points, ids = [], []
    for pid, center in enumerate(((.34,.35),(.64,.35),(.34,.65),(.64,.65))):
        radius = .145
        k = math.ceil(radius / (h/2))
        for i in range(-k,k+1):
            for j in range(-k,k+1):
                offset = np.array([i,j]) * (h/2)
                if float(offset @ offset) <= radius**2:
                    points.append(np.array(center)+offset); ids.append(pid)
    return np.array(points,dtype=float),np.array(ids,dtype=int)


def stencil(x, grid):
    base = np.floor(x * grid - .5).astype(int)
    if np.any(base < 0) or np.any(base + 2 > grid):
        raise ValueError('material point left supported grid')
    f = x * grid - base
    weights = np.stack((.5*(1.5-f)**2, .75-(f-1)**2, .5*(f-.5)**2),axis=1)
    derivatives = np.stack((f-1.5, -2*(f-1), f-.5),axis=1)*grid
    nodes, w, grad, dpos = [], [], [], []
    for i in range(3):
        for j in range(3):
            ij=base+np.array([i,j])
            nodes.append(ij[:,0]*(grid+1)+ij[:,1])
            w.append(weights[:,i,0]*weights[:,j,1])
            grad.append(np.column_stack((derivatives[:,i,0]*weights[:,j,1],weights[:,i,0]*derivatives[:,j,1])))
            dpos.append(ij/grid-x)
    return np.stack(nodes,axis=1),np.stack(w,axis=1),np.stack(grad,axis=1),np.stack(dpos,axis=1)


def stress(F):
    U,s,Vh=np.linalg.svd(F)
    J=np.prod(s,axis=1)
    if np.any(np.linalg.det(F)<=0) or not np.isfinite(F).all():
        raise ValueError('inverted/nonfinite deformation')
    R=U@Vh
    return 2*MU*((F-R)@np.swapaxes(F,1,2)) + np.eye(2)[None,:,:]*(LAM*J*(J-1))[:,None,None]


def plastic_project(F):
    if not np.isfinite(F).all() or np.any(np.linalg.det(F)<=0):
        raise ValueError('inverted/nonfinite trial deformation')
    U,s,Vh=np.linalg.svd(F)
    if np.any(s<=1e-8) or np.any(s>=1e4): raise ValueError('singular/extreme deformation')
    strain=np.log(s); mean=strain.mean(axis=1,keepdims=True); dev=strain-mean
    norm=np.linalg.norm(dev,axis=1,keepdims=True)
    scale=np.minimum(1.0,(YIELD/(2*MU))/np.maximum(norm,1e-30))
    vals=np.exp(mean+dev*scale)
    return (U*vals[:,None,:])@Vh


def pair_impulse(ma,mb,va,vb,normal,friction):
    """Normal points a->b. Separating/tangent pairs get no normal impulse."""
    relative=va-vb; closing=np.sum(relative*normal,axis=1)
    inv=1/ma+1/mb
    jn=np.maximum(closing,0)/inv
    tangent=relative-closing[:,None]*normal
    speed=np.linalg.norm(tangent,axis=1)
    jt=np.minimum(friction*jn,speed/inv)
    impulse=jn[:,None]*normal+jt[:,None]*tangent/np.maximum(speed[:,None],1e-30)
    return va-impulse/ma[:,None],vb+impulse/mb[:,None],jn,jt


def contact(mass,velocity,gradient,centers,friction,sweeps=4):
    fields=len(mass); hits=0; degenerate=0
    if fields==1:return dict(pair_node_projections=0,degenerate_normals=0,residual_closing=0.0)
    threshold=1e-14*float(mass.max())
    pairs=[]
    for a in range(fields):
        for b in range(a+1,fields):
            ii=np.flatnonzero((mass[a]>threshold)&(mass[b]>threshold))
            if not len(ii):continue
            n=gradient[b,ii]/mass[b,ii,None]-gradient[a,ii]/mass[a,ii,None]
            norm=np.linalg.norm(n,axis=1)
            weak=norm<1e-12
            degenerate+=int(weak.sum())
            if weak.any():
                direction=centers[b]-centers[a]; dn=np.linalg.norm(direction)
                if dn<=1e-12:raise ValueError('undefined coincident-field contact normal')
                n[weak]=direction/dn;norm[weak]=1
            n/=norm[:,None]
            pairs.append((a,b,ii,n))
    for _ in range(sweeps):
        for a,b,ii,n in pairs:
            va,vb,jn,_=pair_impulse(mass[a,ii],mass[b,ii],velocity[a,ii],velocity[b,ii],n,friction)
            velocity[a,ii]=va;velocity[b,ii]=vb;hits+=int(np.count_nonzero(jn))
    residual=max((float(np.maximum(np.sum((velocity[a,ii]-velocity[b,ii])*n,axis=1),0).max()) for a,b,ii,n in pairs),default=0.0)
    return dict(pair_node_projections=hits,degenerate_normals=degenerate,residual_closing=residual)


def boundary(mass,velocity,coords,top,wall_v):
    active=mass>0
    topmask=active & (coords[None,:,1]>=top) & (velocity[:,:,1]>wall_v)
    impulse=float(np.sum(mass[topmask]*(velocity[:,:,1][topmask]-wall_v)))
    velocity[:,:,1][topmask]=wall_v
    for axis,position,side in ((1,FLOOR,-1),(0,LEFT,-1),(0,RIGHT,1)):
        outside=(coords[:,axis]<=position if side<0 else coords[:,axis]>=position)
        mask=active & outside[None,:] & (velocity[:,:,axis]*side>0)
        velocity[:,:,axis][mask]=0
    return impulse


def initial_state(grid):
    x,ids=seed_disks(grid)
    return dict(x=x,ids=ids,v=np.zeros_like(x),C=np.zeros((len(x),2,2)),F=np.tile(np.eye(2),(len(x),1,1)))


def step(state,arm,grid,dt,top,wall_v,friction):
    x,v,C,F,ids=(state[k] for k in ('x','v','C','F','ids'))
    field=np.zeros_like(ids) if arm=='S' else ids
    nfield=int(field.max())+1;nn=(grid+1)**2;vol=(.5/grid)**2;pm=RHO*vol
    nodes,w,grad,offset=stencil(x,grid)
    mass=np.zeros((nfield,nn));momentum=np.zeros((nfield,nn,2));gradient=np.zeros_like(momentum)
    affine=pm*C-dt*vol*4*grid**2*stress(F)
    for q in range(9):
        idx=(field,nodes[:,q]);wt=w[:,q]
        np.add.at(mass,idx,wt*pm)
        np.add.at(momentum,idx,wt[:,None]*(pm*v+np.einsum('nij,nj->ni',affine,offset[:,q])))
        np.add.at(gradient,idx,pm*grad[:,q])
    if not np.isclose(mass.sum(),pm*len(x),rtol=1e-12,atol=1e-15):raise ValueError('P2G mass mismatch')
    gv=np.divide(momentum,mass[:,:,None],out=np.zeros_like(momentum),where=mass[:,:,None]>0)
    ij=np.indices((grid+1,grid+1)).reshape(2,-1).T;coords=ij/grid
    impulse=boundary(mass,gv,coords,top,wall_v)
    centers=np.array([x[field==i].mean(axis=0) for i in range(nfield)])
    diagnostic=contact(mass,gv,gradient,centers,friction)
    impulse+=boundary(mass,gv,coords,top,wall_v)
    nv=np.zeros_like(v);nc=np.zeros_like(C)
    for q in range(9):
        vg=gv[field,nodes[:,q]];wt=w[:,q]
        nv+=wt[:,None]*vg
        nc+=4*grid**2*wt[:,None,None]*(vg[:,:,None]*offset[:,q,None,:])
    trial=(np.eye(2)[None,:,:]+dt*nc)@F
    nf=plastic_project(trial);nx=x+dt*nv
    if not np.isfinite(nx).all() or not np.isfinite(nv).all():raise ValueError('nonfinite material state')
    state.update(x=nx,v=nv,C=nc,F=nf)
    diagnostic.update(plate_pressure=impulse/(dt*(RIGHT-LEFT)),mass=float(mass.sum()),
                      kinetic_energy=float(.5*pm*np.sum(nv*nv)),material_points=len(x),fields=nfield,
                      reference_solid_area=vol*len(x),current_solid_area=float(vol*np.linalg.det(nf).sum()))
    return diagnostic


def run_arm(arm,grid,steps,dt,speed,friction,output,wall_limit):
    state=initial_state(grid);start=time.monotonic();records=[];tail=[];max_residual=0.0
    every=max(1,steps//50)
    with (output/(arm+'_trace.jsonl')).open('x',encoding='utf-8') as f:
        for i in range(1,steps+1):
            if time.monotonic()-start>wall_limit:raise TimeoutError('arm wall-clock budget')
            top=TOP0-speed*dt*i
            if top<=FLOOR+.25:raise ValueError('development piston travel bound')
            value=step(state,arm,grid,dt,top,-speed,friction)
            max_residual=max(max_residual,value['residual_closing'])
            if i>steps-max(1,steps//5):tail.append(value['plate_pressure'])
            if i==1 or i%every==0 or i==steps:
                row=dict(step=i,time_code=dt*i,top_code=top,**value)
                f.write(json.dumps(row,allow_nan=False)+'\n');f.flush();records.append(row)
    return dict(arm=arm,steps_completed=steps,seconds=time.monotonic()-start,
                end=records[-1],tail_mean_plate_pressure=float(np.mean(tail)),
                tail_window_steps=len(tail),max_contact_residual_closing=max_residual)


def ratio(s,f):
    return s/f if math.isfinite(s) and math.isfinite(f) and f>1e-12 else None


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--grid',type=int,default=32)
    ap.add_argument('--steps',type=int,default=1200)
    ap.add_argument('--dt',type=float,default=.0005)
    ap.add_argument('--wall-speed',type=float,default=.15)
    ap.add_argument('--friction',type=float,default=.20)
    ap.add_argument('--arm-seconds',type=float,default=600)
    args=ap.parse_args(argv)
    if not 16<=args.grid<=64 or not 1<=args.steps<=5000:ap.error('small CPU development bounds')
    if not all(math.isfinite(v) for v in (args.dt,args.wall_speed,args.friction,args.arm_seconds)):ap.error('finite parameters required')
    if not 0<args.dt<=.0005 or not 0<args.wall_speed<=.2 or not 0<=args.friction<=1 or not 1<=args.arm_seconds<=1800:ap.error('development parameter bound')
    if TOP0-args.steps*args.dt*args.wall_speed<=FLOOR+.25:ap.error('development travel bound')
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=False)
    src=Path(__file__).read_bytes();x,ids=seed_disks(args.grid)
    manifest=dict(label='DEVELOPMENT_DATA_ONLY',units='normalized 2D code units; not MPa',
        source_sha256=hashlib.sha256(src).hexdigest(),python=platform.python_version(),numpy=np.__version__,
        grid=args.grid,steps=args.steps,dt=args.dt,wall_speed=args.wall_speed,friction=args.friction,
        material=dict(E=E,nu=NU,yield_stress=YIELD,rho=RHO),arm_seconds=args.arm_seconds,
        initial_points=len(x),disk_count=int(ids.max())+1,
        initial_state_sha256=hashlib.sha256(x.astype('<f8').tobytes()+ids.astype('<i8').tobytes()).hexdigest(),
        threads={k:os.environ.get(k) for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS')},
        registered_conclusions_adoptable=False,physical_qualification=False,
        limitations=['support-node contact may occur before geometric contact','sequential multi-body projection has finite residual/order effects','small normalized development material; no physical calibration','no unloading or grid/dt convergence qualification'])
    (out/'INPUT.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    results={};status='INCOMPLETE';error=None
    try:
        for arm in ('S','F'):
            results[arm]=run_arm(arm,args.grid,args.steps,args.dt,args.wall_speed,args.friction,out,args.arm_seconds)
        status='DEVELOPMENT_COMPLETE'
    except Exception as exc:
        error=type(exc).__name__+': '+str(exc)
    peak=None
    try:
        import resource
        if sys.platform.startswith('linux'):peak=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)*1024
    except ImportError:pass
    q=ratio(results['S']['tail_mean_plate_pressure'],results['F']['tail_mean_plate_pressure']) if status=='DEVELOPMENT_COMPLETE' else None
    summary=dict(status=status,label='DEVELOPMENT_DATA_ONLY',arms=results,peak_process_rss_bytes=peak,
                 memory_scope='process high-water mark including both sequential arms; not per-arm incremental memory',
                 plate_stress_ratio_S_over_F=q,ratio_status='AVAILABLE' if q is not None else 'UNAVAILABLE_OR_ZERO_DENOMINATOR',
                 registered_conclusions_adoptable=False,error=error)
    (out/'SUMMARY.json').write_text(json.dumps(summary,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps(summary,allow_nan=False))
    return 0 if status=='DEVELOPMENT_COMPLETE' else 2


if __name__=='__main__':raise SystemExit(main())
