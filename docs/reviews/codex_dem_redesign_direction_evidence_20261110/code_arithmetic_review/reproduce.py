"""Read-only audit: no project imports, Taichi, simulation, or host interaction.
Independent algebra from pinned source; the source is only read/AST-parsed.
Run with the provided lhs28 venv Python. Outputs results.json alongside this file.
"""
from pathlib import Path
import ast
import hashlib
import json
import math
import numpy as np
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
REPO = HERE.parent / 'package' / 'repo'
out = {'scope': 'offline algebra and small synthetic geometry only', 'source_sha256': {}}
for relative in ['scripts/mpm3d_compaction.py', 'scripts/mpm_dem_match.py', 'scripts/dem3d_plastic.py']:
    raw = (REPO / relative).read_bytes()
    ast.parse(raw.decode('utf-8-sig'))
    out['source_sha256'][relative] = hashlib.sha256(raw).hexdigest()

def lame(E, nu):
    mu = E / (2*(1+nu))
    la = E*nu / ((1+nu)*(1-2*nu))
    return mu, la

def onset_3d(E, nu, yld, sign, epsilon=0):
    # F=diag(b,b,a); R=I; J=a*b*b.  For 3D dev log stretch,
    # ||dev(log F)|| = sqrt(2/3)*abs(log(a/b)).
    mu, la = lame(E, nu)
    ratio = math.exp(sign*math.sqrt(3/2)*(yld/(2*mu)-epsilon))
    def lateral_tau(b):
        J = ratio*b**3
        return 2*mu*b*(b-1) + la*J*(J-1)
    b = brentq(lateral_tau, 0.8, 1.3, xtol=1e-14)
    a = ratio*b
    J = a*b*b
    tau = 2*mu*a*(a-1)+la*J*(J-1)
    return {'axial_stretch':a, 'lateral_stretch':b, 'J':J,
            'tau_GPa':tau, 'cauchy_GPa':tau/J,
            'lateral_residual_GPa': lateral_tau(b)/J,
            'yield_norm':math.sqrt(2/3)*abs(math.log(a/b)),
            'mu_GPa':mu, 'lambda_GPa':la}

out['yield_3d']={}
for name,E,nu in [('soft',1.53,.49),('stiff',22.06,.36)]:
    out['yield_3d'][name]={}
    for lab,sign in [('compression',-1),('tension',1)]:
        v=onset_3d(E,nu,.30,sign)
        v['epsilon_1e_9_delta_GPa']=onset_3d(E,nu,.30,sign,1e-9)['cauchy_GPa']-v['cauchy_GPa']
        out['yield_3d'][name][lab]=v
out['small_strain_uniaxial_GPa']=math.sqrt(3/2)*.30
out['yield_2d_NZ22_MPa']={}
mu,la=lame(10,.45); sy=.4*math.sqrt(2/3)
for name,sgn in [('compression',-1),('tension',1)]:
    q=math.exp(sgn*math.sqrt(2)*sy/(2*mu))
    fun=lambda b:2*mu*b*(b-1)+la*q*b*b*(q*b*b-1)
    b=brentq(fun,.8,1.3,xtol=1e-14);a=q*b;J=a*b
    axial=(2*mu*a*(a-1)+la*J*(J-1))/J
    zz=la*(J-1)
    vm=math.sqrt((axial**2+zz**2+(zz-axial)**2)/2)
    out['yield_2d_NZ22_MPa'][name]={'code_threshold':sy,'axial_Cauchy':axial,'out_of_plane_Cauchy':zz,'3d_von_Mises':vm,'deviation_from_0_4':vm/.4-1}
out['elasticity']={}
for name,E,nu in [('soft',1.53,.49),('stiff',22.06,.36),('W1_stopped',24,.30),('W1_hit_1',1.35,.30),('W1_hit_2',1.53,.30)]:
    mu,la=lame(E,nu); K=la+2*mu/3; M=la+2*mu
    out['elasticity'][name]={'mu_GPa':mu,'K_GPa':K,'M_GPa':M,'cL_cS':math.sqrt(M/mu)}

def sphere_template(diameter_cells):
    # Dimensionless radius=1; dx=2/diameter_cells; SE spacing=dx/2.
    spc=1/diameter_cells; k=int(1/spc)+1
    ax=np.arange(-k,k+1)*spc
    q=np.stack(np.meshgrid(ax,ax,ax,indexing='ij'),-1).reshape(-1,3)
    n=int(np.count_nonzero(np.sum(q*q,axis=1)<=1))
    return {'points':n,'relative_volume_error':n*spc**3/(4*math.pi/3)-1}

out['seed_template']={str(d):sphere_template(d) for d in [6,8,12,16]}
out['seed_template_around7']={str(d):sphere_template(d) for d in [6.95,7,7.05,7.1]}
out['seed_rounding_384']={'side_um_exact':50/.92,'side_um_rounded':54.3,
    'exact':sphere_template(384/(50/.92)), 'rounded':sphere_template(384/54.3),
    'note':'The discrete template jumps when the squared dimensionless radius crosses integer 50.'}
out['scaffold']={}
total=0
for phase,filename in [('AM','real14_am_scaffold.csv'),('SE','real14_se_scaffold.csv')]:
    a=np.loadtxt(REPO/'docs'/'data'/filename, delimiter=',',comments='#')
    vals,counts=np.unique(a[:,[0,4]],axis=0,return_counts=True)
    vol=float(np.sum(4*math.pi/3*(a[:,4]*1000)**3));total+=vol
    out['scaffold'][phase]={'count':len(a),'groups':[{'type':int(v[0]),'radius_um':v[1]*1000,'count':int(c)} for v,c in zip(vals,counts)],'volume_um3':vol}
out['scaffold']['kappa_SE']=out['scaffold']['SE']['volume_um3']/total
out['scaffold']['solid_fraction_at_50x50x30_3']=total/(50*50*30.3)
out['scaffold']['heights_from_exact_mass_um']={str(phi):total/(50*50*phi) for phi in [.6,.35]}

cap48=.85*49140*2**20
cap24=.85*24576*2**20
side=50/.92 # source scaffold SW=(.04,.96)
out['memory']={'cap48_GB':cap48/1e9,'cap24_GB':cap24/1e9,'grid_side_um':side,'rows':[]}
for ng in [384,435,512]:
    pin=sphere_template(ng/side)['points']; npoints=32832*pin
    for height_factor in [1,1.42]:
        nodes=ng**3*height_factor
        p=npoints*124; b=nodes*24; f=nodes*36
        out['memory']['rows'].append({'ng':ng,'height_factor':height_factor,'points_per_SE':pin,'particle_GB':p/1e9,'base_GB':b/1e9,'field_GB':f/1e9,'K48':math.floor((cap48-p-b)/f),'K24':math.floor((cap24-p-b)/f)})
out['memory']['height_reconstruction']={}
for label,h in [('memo_rounded',76),('mass_exact',total/(2500*.35))]:
    # Existing scaffold code FLOOR=.05, WALL0=am_top+.05, am_top=FLOOR+h/um_box.
    fac=max(1,(.05+h/side+.05+.02))
    row={'bed_height_um':h,'continuous_nz_factor_scaffold_convention':fac,'ng435_nz':math.ceil(fac*435),'K48_by_ng':{}}
    for ng in [384,435,512]:
        nodes=ng*ng*max(ng,math.ceil(fac*ng))
        p=32832*sphere_template(ng/side)['points']*124
        row['K48_by_ng'][str(ng)]=math.floor((cap48-p-nodes*24)/(nodes*36))
    out['memory']['height_reconstruction'][label]=row
out['memory']['dense_one_body_fields_TB']=32832*384**3*16/1e12

out['stage4_boxes']=[]
for L,H in [(25,15),(25,30),(50,30)]:
    volume=L*L*H*.88
    for cells in [8,12]:
        count=volume/(4*math.pi/3*.5**3)
        npoints=count*sphere_template(cells)['points']
        out['stage4_boxes'].append({'L_um':L,'H_um':H,'cells_per_diameter':cells,'SE_count':count,'points':npoints,'points_GB':npoints*124/1e9})

def two_d(N,dmin,dmax,phi0,phif,nu,mach,cells):
    # Equal area-fraction per diameter bin => number PDF proportional to d^-2.
    mean_d2=dmin*dmax
    area=N*math.pi/4*mean_d2
    L=math.sqrt(area/phi0);dx=dmin/cells
    pts=area/(dx/2)**2
    nodes=(L/dx)**2
    # dt=.3*dx/cL; V=mach*cS; final h=initial h*phi0/phif.
    cp_cs=math.sqrt(2*(1-nu)/(1-2*nu))
    steps=L*(1-phi0/phif)/dx * cp_cs/(.3*mach)
    return {'L':L,'nodes':nodes,'points':pts,'steps_to_phif':steps,'particle_steps':pts*steps}
out['two_d_scale']={}
for c in [8,12,16,24]:
    out['two_d_scale'][f'3a_{c}']=two_d(300,2,4,.78,.95,.45,.034,c)
    out['two_d_scale'][f'3b_{c}']=two_d(500,.8,1.2,.70,.97,.49,.05,c)
out['run_count']={'3a':3*3*3,'3b_k1':3*3*3,'3b_k02_core':3*3*3,'3b_k02_report_A_mu0':3,'3c':2*2*3,'base_total':96,
                  'two_eligible_benchmarks_extend24_add':2*3*3,'all_eligible_extend24_total':114,
                  'note':'Memo line 348 permits 24-cell extension for 3a and 3b kappa=1 only. A(mu0) omission subtracts 3.'}
updates=9*sum(out['two_d_scale'][f'{suite}_{c}']['particle_steps'] for suite in ['3a','3b'] for c in [8,12,16])
out['cpu_budget']={'illustrative_3a_plus_3b_k1_particle_updates_to_assumed_final_phi':updates,
    'million_particle_updates_per_second_for_7_days':updates/(7*86400*1e6),
    'million_particle_updates_per_second_for_14_days':updates/(14*86400*1e6),
    'limits':'Excludes kappa=.2,3c,unit tests,retries,contact solving,colouring and convergence overhead; no measured throughput, no runtime guarantee.'}

# Three minimal offline counterexamples, no model advancement.
out['synthetic']={
    'frozen_AM':{'grid_mass':1,'vz_before':-1,'vz_after':0,'constraint_impulse_on_grid':1,'reaction_impulse_on_AM':-1},
    'platen_downward':{'v_wall':-1,'v_grid_before':-2,'bilateral_after':-1,'unilateral_after':-2,'bilateral_wall_impulse':-1,'unilateral_wall_impulse':0},
    'relative_displacement':{'initial_support_gap_cells':1.5,'budget_per_body_cells':1,'relative_closure_cells':2,'one_budget_graph_has_edge':False,'support_collision_possible':True}
}
# Nearest-centre ownership is not a conservative occupancy oracle. With three
# coincident equal spheres, every original body has exactly the same support;
# deterministic nearest-ID tie breaking can retain only ID 0. This is a logical
# counterexample, not an assertion about measured real_14 overlap severity.
out['synthetic']['nearest_reassignment']={'original_bodies_at_each_support_node':[0,1,2],'nearest_tie_owner':[0],'K_clique_original':3,'K_after_reassignment':1,'real14_measurement':False}

# Safely extract only the pure scalar reference function (no module import or
# top-level evaluation). Its Taichi counterpart was checked textually.
tree=ast.parse((REPO/'scripts/dem3d_plastic.py').read_text(encoding='utf-8-sig'))
fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='f_load_numpy')
isolated=ast.Module(body=[fn],type_ignores=[]); env={'math':math}
exec(compile(ast.fix_missing_locations(isolated),'<AST:f_load_numpy>','exec'),env)
R=.25; Estar=24/(2*(1-.3**2)); py=3*.15;dy=R*(math.pi*py/(2*Estar))**2; delta=.2*R
forces={str(beta):env['f_load_numpy'](delta,R,Estar,py,dy,beta,8) for beta in [.06,.30]}
out['dem_lock_counterexample']={'Rstar_um':R,'Estar_GPa':Estar,'sigma_y_GPa':.15,'py_GPa':py,'delta_um':delta,'dy_um':dy,'forces_GPa_um2_by_beta':forces,'force_ratio':forces['0.06']/forces['0.3'],'warning':'Synthetic monotonic contact only; neither parameter is newly selected or recommended.'}
(HERE/'results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:out[k] for k in ['yield_3d','scaffold','memory','run_count']},ensure_ascii=False,indent=2))
