"""Independent signed-row, affine, no-cross-body and periodic stress checks."""
import argparse
import importlib.util
import json
from pathlib import Path
from time import perf_counter

import numpy as np


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem,path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reference_cloud(material, grid, x, ids, volumes, N=None):
    keys,w,_,r = material.stencil(x, grid)
    if N is not None:
        keys = N(keys)
    key,inv = np.unique((keys + (grid+1)**2*ids[:,None]).ravel(),return_inverse=True)
    slots = inv.reshape(w.shape)
    mass = np.bincount(slots.ravel(),weights=(volumes[:,None]*w).ravel())
    return key,w,r,slots,mass


def basic(floor, candidate, material, cells, sign):
    grid,plane,dt = 10*cells,.35,.001
    pitch = .5/grid
    # Deliberately one-sided reference support plus a second particle with identical coordinates.
    d = np.array([[-.45,.56],[.41,.65],[-.37,1.28],[.44,1.31]])*pitch
    s0 = np.array([[.5,plane]])
    x = np.tile(s0+d,(2,1))
    ids = np.repeat([0,1],4)
    keys,w,r,slots,mass = reference_cloud(material,grid,x,ids,np.full(8,.125))
    b = candidate.build_boundary(floor,x,ids,s0.copy(),np.array([0]),pitch)
    wall = b.bind(x,w,r,slots,grid,plane,dt)
    N = np.bincount(wall.slots[0],weights=wall.coefficients[0],minlength=len(mass))
    xy = np.stack(np.divmod(keys%((grid+1)**2),grid+1),axis=1)/grid
    expected = np.sum(N)
    np.testing.assert_allclose(expected,1.,atol=2e-14,rtol=0)
    np.testing.assert_allclose(N @ xy, s0[0],atol=2e-14,rtol=0)
    np.testing.assert_array_equal(N[keys//((grid+1)**2)==1],0.)
    assert np.min(N)<0., "fixture should cover signed APIC weights"
    B = np.array([[.31,-.84],[.21,-.37]])
    gv = (xy-s0)@B.T + np.array([.35,sign*.2])
    gv[keys//((grid+1)**2)==1] += 8.
    vfree = gv.copy()
    before = N @ vfree[:,1]
    inv = float(np.sum(N[mass>0]**2/mass[mass>0]))
    prediction = max(0.,-before)/inv
    J = wall.project(mass,gv)
    np.testing.assert_allclose(J,prediction,atol=3e-13,rtol=1e-12)
    dp = np.sum(.125*np.einsum("pq,pqi->pi",w,(gv-vfree)[slots]),axis=0)
    np.testing.assert_allclose(dp,[0,J],atol=2e-14)
    np.testing.assert_array_equal(gv[keys//((grid+1)**2)==1],vfree[keys//((grid+1)**2)==1])
    E0 = float(mass @ np.sum(vfree**2,axis=1))/2
    E1 = float(mass @ np.sum(gv**2,axis=1))/2
    assert E1<=E0+1e-13
    vf = N @ gv
    target = s0[0]+dt*vf
    wall.transport(gv)
    np.testing.assert_allclose(b.positions[0],target,atol=2e-15)
    return dict(cells=cells,direction=sign,J=J,analytic_J=prediction,min_combined_weight=float(min(N)),
                marker_x_error=float(np.linalg.norm(N@xy-s0[0])),G2P_impulse_error=float(max(abs(dp-[0,J]))),
                energy_decrease=E0-E1)


def deformed_and_support(floor,candidate,material):
    c,dt=80,.001
    pitch=.5/c
    ref=np.array([[.5,.35]])
    local=pitch*np.array([[-.5,.25],[.5,.25],[-.5,1.25],[.5,1.25]])
    X=ref+local
    A=np.array([[1.1,.23],[-.14,.94]])
    b=np.array([-.045,.085])
    x=X@A.T+b
    expected_marker=ref@A.T+b
    projected_rows=[]
    for order in ([0,1,2,3],[3,1,0,2],[2,0,3,1]):
        order=np.array(order)
        g=candidate.build_boundary(floor,X[order],np.zeros(4,int),ref.copy(),np.zeros(1,int),pitch)
        g.positions[:]=expected_marker
        keys,w,r,slots,m=reference_cloud(material,c,x[order],np.zeros(4,int),np.full(4,.25))
        row=g.bind(x[order],w,r,slots,c,float(expected_marker[0,1]),dt)
        N=np.bincount(row.slots[0],weights=row.coefficients[0],minlength=len(keys))
        coords=np.stack(np.divmod(keys,c+1),axis=1)/c
        G=np.array([[-.02,.08],[.05,-.07]])
        velocities=coords@G.T+np.array([.08,-.3])
        marker_velocity=N@velocities
        np.testing.assert_allclose(marker_velocity,(expected_marker@G.T)[0]+[.08,-.3],rtol=0.,atol=2e-14)
        J=row.project(m,velocities)
        assert J>0.
        projected_rows.append(np.r_[marker_velocity,J,N])
    for v in projected_rows[1:]:
        np.testing.assert_allclose(v,projected_rows[0],rtol=2e-13,atol=3e-14)
    rejected=0
    for remote in (np.array([[.6,.35]]), np.array([[.48,.35]])):
        try:
            candidate.build_boundary(floor,X,np.zeros(4,int),remote.copy(),np.zeros(1,int),pitch)
        except ValueError:
            rejected+=1
    assert rejected==2
    return dict(finite_support_rejections=rejected,permutations=3,wall_J=projected_rows[0][2],
                max_permutation_error=max(float(max(abs(a-projected_rows[0]))) for a in projected_rows[1:]))


def slab_run(floor,candidate,material,flat,grid,slope):
    x,volume,depth,owners = flat.slab()
    period = round(flat.WIDTH*grid)
    def transform(nodes):
        ix,iy = np.divmod(nodes,grid+1)
        return ((ix-round(.3*grid)) % period)*(grid+1)+iy
    ids=np.zeros(len(x),dtype=int)
    key,w,r,slots,mass=reference_cloud(material,grid,x,ids,volume,transform)
    # Keep the original periodic slab's unique P2G masses. Neighbor-search copies across
    # the seam carry the same grid rows and have no independent mass.
    xx = np.concatenate([x+np.array([shift,0.]) for shift in (-flat.WIDTH,0.,flat.WIDTH)])
    idxx = np.tile(ids,3)
    b = candidate.build_boundary(floor,xx,idxx,x[owners].copy(),np.zeros(len(owners),int),.5/grid)
    wall=b.bind(xx,np.tile(w,(3,1)),np.tile(r,(3,1,1)),np.tile(slots,(3,1)),grid,flat.FLOOR,flat.DT)
    P=4*grid**2*flat.DT*volume[:,None]*(1+slope*depth[:,None])*w*r[:,:,1]
    p=np.bincount(slots.ravel(),weights=P.ravel(),minlength=len(key))
    v=np.zeros((len(key),2))
    np.divide(p,mass,out=v[:,1],where=mass>0)
    old=v.copy()
    J=wall.project(mass,v)
    np.testing.assert_allclose(mass@(v-old)[:,1],J,atol=2e-12)
    dp_g2p=float(volume @ np.sum(w*(v-old)[slots,1],axis=1))
    np.testing.assert_allclose(dp_g2p,J,atol=2e-12)
    return dict(grid=grid,slope=slope,parent_analytic_MPa=flat.exact(grid,slope),
                weighted_MPa=10*J/(flat.WIDTH*flat.DT),G2P_impulse_error=abs(dp_g2p-J))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("setting2_root",type=Path);p.add_argument("candidate",type=Path);p.add_argument("out",type=Path)
    p.add_argument("--slab-source",type=Path)
    args=p.parse_args()
    prefix=args.setting2_root/"history/old_full/prefix"
    floor=load(prefix/"docs/reviews/suyoung_floor_contact_20261123/material_floor.py")
    candidate=load(args.candidate)
    material=load(prefix/"scripts/dem_suyoung_sf2d_dev.py")
    flatpath=args.slab_source or prefix/"docs/reviews/suyoung_floor_contact_20261123/flat_stress_check.py"
    if not flatpath.is_file():
        raise ValueError("provide the pinned flat_stress_check.py with --slab-source")
    import hashlib
    if hashlib.sha256(flatpath.read_bytes()).hexdigest()!="7cbdc4dec11ffcd3308f6e17a1d45313116182be6af49df67586bdf8d829bce6":
        raise ValueError("wrong source for periodic flat and depth-gradient quadrature")
    flat=load(flatpath)
    start=perf_counter()
    basic_results=[basic(floor,candidate,material,n,s) for n in (8,12,16,24) for s in (-1.,1.)]
    slab_results=[slab_run(floor,candidate,material,flat,n,k) for n in (80,160) for k in (0.,12.)]
    result=dict(basic=basic_results, slab=slab_results,deformed=deformed_and_support(floor,candidate,material),
                candidate_sha256=hashlib.sha256(args.candidate.read_bytes()).hexdigest(),elapsed_s=perf_counter()-start)
    with args.out.open("x",encoding="utf-8") as stream:
        json.dump(result,stream,indent=2);stream.write("\n")


if __name__=="__main__":
    main()
