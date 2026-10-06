"""Read-only design review probes. No new production implementation or campaign."""
from pathlib import Path
import itertools, json, math, hashlib, sys
import numpy as np
import scipy

ROOT = Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'source'/'scripts'))
import step3_sigma as s3

def epsilon_tie_probe():
    eps=1e-6
    centers=np.array([[0.,0.,0.],[1.,0.,0.],[2.,0.,0.]])
    powers=np.array([-1+1.5*eps,-1+.75*eps,-1.])
    radii=np.sqrt((centers**2).sum(axis=1)-powers)
    powers=(centers**2).sum(axis=1)-radii**2
    def pick(i,j):
        if abs(powers[i]-powers[j]) <= eps:
            return min((i,j),key=lambda k:tuple(centers[k]))
        return i if powers[i]<powers[j] else j
    permutations=[]
    for perm in itertools.permutations(range(3)):
        winner=perm[0]
        for k in perm[1:]: winner=pick(winner,k)
        permutations.append({'input':perm,'winner':int(winner)})
    global_min=float(powers.min())
    band=[k for k in range(3) if powers[k]<=global_min+eps]
    global_winner=min(band,key=lambda k:tuple(centers[k]))
    set_rule_results=[]
    for perm in itertools.permutations(range(3)):
        pmin=min(powers[k] for k in perm)
        eligible=[k for k in perm if powers[k]<=pmin+eps]
        winner=min(eligible,key=lambda k:tuple(centers[k]))
        set_rule_results.append({'input':perm,'winner':int(winner)})
    same_center_radii=[1.,math.sqrt(1+.5*eps)]
    return {'epsilon_um2':eps,'centers_um':centers.tolist(),'radii_um':radii.tolist(),
        'power_um2':powers.tolist(),'pair_winners':{'0_vs_1':pick(0,1),'1_vs_2':pick(1,2),'2_vs_0':pick(2,0)},
        'sequential_results':permutations,'global_min_epsilon_band':band,'global_band_winner':int(global_winner),
        'set_rule_results':set_rule_results,
        'same_center_unequal_radii_um':same_center_radii,
        'same_center_power_difference':same_center_radii[1]**2-same_center_radii[0]**2}

def bridge_mid(c,r,perm):
    i,j=perm
    d=float(np.linalg.norm(c[i]-c[j]))
    return c[i]+(c[j]-c[i])*(r[i]+.5*(d-r[i]-r[j]))/max(d,1e-12)

def bridge_mask_counterexample():
    # Geometric boundary test: a voxel center on a bridge sphere, outside the
    # AM spheres. Small offsets of the geometric input explore floating rounding.
    h=.1; lo=np.zeros(3); hi=np.full(3,2.6); q=np.array([10,10,10]); target=(q+.5)*h
    radii=np.array([.5,.75]); types=np.array([2,1]); delta=.02
    tries=0
    for b in (.24,.25,.20,.30):
        for dz in (.005,.01,.015,.02,.025,.03):
            mid=target-np.array([math.sqrt(b*b-dz*dz),0.,dz])
            for dxulp in range(-6,7):
                x=mid[0]
                for _ in range(abs(dxulp)):
                    x=np.nextafter(x, -np.inf if dxulp<0 else np.inf)
                c=np.array([[x,mid[1],mid[2]-radii[0]+delta/2],
                            [x,mid[1],mid[2]+radii[1]-delta/2]])
                m0=bridge_mid(c,radii,[0,1]);m1=bridge_mid(c,radii,[1,0])
                # Exact arithmetic sequence from _ball's cell predicate.
                d0=float(np.sum((q+.5-m0/h)**2));d1=float(np.sum((q+.5-m1/h)**2));r2=(b/h)**2
                tries+=1
                if (d0<=r2)==(d1<=r2): continue
                if np.any(((c-target)**2).sum(axis=1)<=radii**2):continue
                grids=[]
                for perm in ([0,1],[1,0]):
                    sid,_=s3.rasterize(c[perm],radii[perm],types[perm],None,None,lo,hi,h,bridge_um=b)
                    grids.append(sid)
                masks=[np.isin(g,[1,2]) for g in grids]
                different=np.argwhere(masks[0]!=masks[1])
                if len(different):
                    return {'found':True,'search_trials':tries,'centers_um':c.tolist(),'radii_um':radii.tolist(),
                        'types':types.tolist(),'vox_um':h,'bridge_um':b,'box_lo_um':lo.tolist(),'box_hi_um':hi.tolist(),
                        'bridge_center_forward_um':m0.tolist(),'bridge_center_reverse_um':m1.tolist(),
                        'target_ijk':q.tolist(),'target_center_um':target.tolist(),
                        'squared_grid_distance':[d0,d1],'squared_bridge_radius_grid':r2,
                        'changed_AM_mask_cells':len(different),'changed_ijk':different.tolist(),
                        'AM_mask_count':[int(m.sum()) for m in masks],
                        'sid_at_changed':[[int(g[tuple(k)]) for k in different] for g in grids]}
    # Non-axis-aligned bridge and arbitrary radii expose cancellation that the
    # first axis-aligned set did not. Radius is pinned to a cell-center boundary.
    rng=np.random.default_rng(20261007)
    q=np.array([15,15,15]);target=(q+.5)*h;hi=np.full(3,3.2)
    for _ in range(2000):
        u=rng.normal(size=3);u/=np.linalg.norm(u)
        v=rng.normal(size=3);v-=v.dot(u)*u;v/=np.linalg.norm(v)
        dz=.005;nominal_b=.24
        mid=target-math.sqrt(nominal_b**2-dz**2)*v-dz*u
        radii=rng.uniform(.4,.9,size=2);delta=.005
        c=np.array([mid-u*(radii[0]-delta/2),mid+u*(radii[1]-delta/2)])
        m0=bridge_mid(c,radii,[0,1]);m1=bridge_mid(c,radii,[1,0])
        d0=float(np.sum((q+.5-m0/h)**2));d1=float(np.sum((q+.5-m1/h)**2))
        if d0==d1:continue
        for b in (h*math.sqrt(d0),h*math.sqrt(d1),
                  np.nextafter(h*math.sqrt(d0),-np.inf),np.nextafter(h*math.sqrt(d0),np.inf)):
            tries+=1;r2=(b/h)**2
            if (d0<=r2)==(d1<=r2):continue
            if np.any(((c-target)**2).sum(axis=1)<=radii**2):continue
            grids=[]
            for perm in ([0,1],[1,0]):
                sid,_=s3.rasterize(c[perm],radii[perm],types[perm],None,None,lo,hi,h,bridge_um=b)
                grids.append(sid)
            masks=[np.isin(g,[1,2]) for g in grids]
            different=np.argwhere(masks[0]!=masks[1])
            if len(different):
                return {'found':True,'search_trials':tries,'search_seed':20261007,
                    'centers_um':c.tolist(),'radii_um':radii.tolist(),'types':types.tolist(),
                    'vox_um':h,'bridge_um':b,'box_lo_um':lo.tolist(),'box_hi_um':hi.tolist(),
                    'bridge_center_forward_um':m0.tolist(),'bridge_center_reverse_um':m1.tolist(),
                    'target_ijk':q.tolist(),'target_center_um':target.tolist(),
                    'squared_grid_distance':[d0,d1],'squared_bridge_radius_grid':r2,
                    'changed_AM_mask_cells':len(different),'changed_ijk':different.tolist(),
                    'AM_mask_count':[int(m.sum()) for m in masks],
                    'sid_at_changed':[[int(g[tuple(k)]) for k in different] for g in grids]}
    return {'found':False,'search_trials':tries}

def sphere_probes():
    ki,km,r_over_a=10.,1.,1.
    keq=ki/(1+r_over_a*ki);beta=(keq-km)/(keq+2*km);mut_beta=(ki-km)/(ki+2*km)
    a,E,L=1.,1.,5.;f=(a/L)**3
    A=E*(1-beta*f)/(1-mut_beta*f)
    B=A*mut_beta*a**3
    phi_bc=-E*L*(1-beta*f)
    wrong_boundary=-A*L+B/L**2
    interior_r=2.
    true_phi=-E*interior_r+E*beta*a**3/interior_r**2
    wrong_phi=-A*interior_r+B/interior_r**2
    annulus_r=np.array([2.,3.,4.])
    annulus_phi=-A*annulus_r+B/annulus_r**2
    fit_A,fit_B=np.linalg.lstsq(np.column_stack((-annulus_r,1/annulus_r**2)),annulus_phi,rcond=None)[0]
    inferred_from_boundary=(1+wrong_boundary/(E*L))/f
    response=(1+2*beta*f)/(1-beta*f)
    return {'sigma_i':ki,'sigma_m':km,'r_over_a':r_over_a,'sigma_eq':keq,'beta':beta,
        'film_deleted_beta':mut_beta,'a':a,'L':L,'wrong_remote_coefficient_A':A,'wrong_dipole_B':B,
        'prescribed_boundary_phi':phi_bc,'wrong_solution_boundary_phi':wrong_boundary,
        'beta_inferred_from_prescribed_boundary':inferred_from_boundary,
        'annulus_r':annulus_r.tolist(),'annulus_phi':annulus_phi.tolist(),
        'annulus_fit_A':float(fit_A),'annulus_fit_B':float(fit_B),
        'beta_from_independent_two_parameter_annulus_fit':float(fit_B/(fit_A*a**3)),
        'r_inner_observation':interior_r,'correct_phi_inner':true_phi,'film_deleted_phi_inner':wrong_phi,
        'linear_outer_sphere_keff_over_km':response,
        'normalized_response':(response-1)/f,'analytic_normalized_response':3*beta/(1-beta*f),
        'l_ge_2_exact_continuum_coefficient':0.}

def fixed_bridge_boundary_probe():
    # Recheck the boundary issue at exactly the usual float literal bridge=.24.
    base=np.array([[1.9748831001799216,1.879129304578067,1.7896943576126298],
                   [1.0611990064053254,.8549090548944595,1.7364778658264648]])
    radii=np.array([.534836145277679,.8437277367739292]);types=np.array([2,1])
    h=.1;b=.24;q=np.array([15,15,15]);lo=np.zeros(3);hi=np.full(3,3.2)
    for axis in range(3):
        for shift in range(-40,41):
            c=base.copy()
            for _ in range(abs(shift)):
                c[:,axis]=np.nextafter(c[:,axis],-np.inf if shift<0 else np.inf)
            mids=[bridge_mid(c,radii,p) for p in ([0,1],[1,0])]
            ds=[float(np.sum((q+.5-m/h)**2)) for m in mids];rr=(b/h)**2
            if (ds[0]<=rr)==(ds[1]<=rr):continue
            grids=[]
            for perm in ([0,1],[1,0]):
                sid,_=s3.rasterize(c[perm],radii[perm],types[perm],None,None,lo,hi,h,bridge_um=b)
                grids.append(sid)
            masks=[np.isin(g,[1,2]) for g in grids];changed=np.argwhere(masks[0]!=masks[1])
            if len(changed):
                return {'found':True,'centers_um':c.tolist(),'radii_um':radii.tolist(),'types':types.tolist(),
                    'vox_um':h,'bridge_um':b,'box_lo_um':lo.tolist(),'box_hi_um':hi.tolist(),
                    'bridge_centers_um':[m.tolist() for m in mids],
                    'target_center_um':((q+.5)*h).tolist(),'squared_grid_distances':ds,
                    'squared_bridge_radius_grid':rr,'changed_AM_mask_cells':len(changed),
                    'changed_ijk':changed.tolist(),'AM_mask_counts':[int(m.sum()) for m in masks],
                    'sid_at_changed':[[int(g[tuple(k)]) for k in changed] for g in grids]}
    return {'found':False}

def carbon_probe():
    # Two terminal nodes: the contact consists of two parallel 2-ohm films.
    # Surviving film is 2 or 1 ohm; independent legacy carbon branch is 0.02 ohm.
    bypass=.02
    def parallel(a,b): return 1/(1/a+1/b)
    return {'N0':2,'Nsurv':1,'fraction_surviving':.5,
        'pure_film_remove_R_ohm':2.,'pure_film_renormalize_R_ohm':1.,
        'carbon_bypass_R_ohm':bypass,
        'full_remove_R_ohm':parallel(2.,bypass),'full_renormalize_R_ohm':parallel(1.,bypass),
        'current_fraction_carbon_remove':(1/bypass)/(1/bypass+1/2),
        'film_log_sensitivity_remove':(1/2)/(1/bypass+1/2),
        'Nsurv_zero_with_carbon_R_ohm':bypass}

def occlusion_rounding_estimate():
    # Independent count of axis-aligned mask convention; this checks an
    # interpretation, not a hypothetical production v3 implementation.
    return {'quantity':'Nsurv/N0 is support-face fraction, not measured physical exposed area',
            'N0_zero_policy_required':True,'surv_subset_of_pre_additive_support_required':True}

def main():
    manifest=json.loads((ROOT/'source_manifest.json').read_text(encoding='utf8'))
    verified=[]
    for row in manifest['files']:
        b=(ROOT/'source'/row['path']).read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        assert blob==row['git_blob'],(row['path'],blob,row['git_blob'])
        verified.append(dict(row,sha256=hashlib.sha256(b).hexdigest()))
    out={'pin':manifest['pin'],'source_verification':verified,
         'environment':{'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__},
         'epsilon_tie':epsilon_tie_probe(),'legacy_AM_mask_permutation':bridge_mask_counterexample(),
         'fixed_bridge_AM_mask_permutation':fixed_bridge_boundary_probe(),
         'sphere_bc':sphere_probes(),'carbon_bypass':carbon_probe(),
         'occlusion_scope':occlusion_rounding_estimate()}
    assert len({x['winner'] for x in out['epsilon_tie']['sequential_results']})>1
    assert {x['winner'] for x in out['epsilon_tie']['set_rule_results']} == {1}
    fixed=out['fixed_bridge_AM_mask_permutation']
    assert fixed['found'] and fixed['changed_AM_mask_cells']==1
    assert fixed['bridge_um']==.24 and fixed['AM_mask_counts']==[3170,3171]
    sp=out['sphere_bc'];assert abs(sp['normalized_response']-sp['analytic_normalized_response'])<1e-12
    assert abs(sp['beta_inferred_from_prescribed_boundary']-sp['beta'])<1e-12
    (ROOT/'evidence_v3.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
