"""Independent CPU probes of pinned producer/consumer functions; no production edits."""
from pathlib import Path
import sys
import json
import contextlib
import io
import ast
import hashlib

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path[:0] = [str(ROOT / 'source/scripts'), str(ROOT.parent / 'lhs_coverage_review_20260930/deps')]
sys.dont_write_bytecode = True
import numpy as np
import step3_sigma as s3


def quiet(fn, *args, **kwargs):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*args, **kwargs)


def probe_pid():
    # Two AM spheres and a tangent carbon line with every input point outside AM,
    # passed through actual rasterize. Cell stamping overlaps the AM silhouette.
    vox = .2
    pts = np.c_[np.full(30, 2.181), np.full(30, 1.1), np.linspace(.05, 3.95, 30)]
    centers = np.array([[1.18,1.1,1.0],[1.18,1.1,3.0]])
    sid, pid = s3.rasterize(centers,
                          np.array([1.0,1.0]), np.array([2,2]),
                          pts, np.full(30,2), (0,0,0), (2.2,2.2,4), vox,
                          add_fid=np.zeros(30,dtype=int), bridge_um=.24)
    sig = s3.electronic_sigma_table(.01,.005,100,10,250)
    res = quiet(s3.solve_sigma_z, sid, sig, vox, return_field=True,z_bot_um=0,z_top_um=4)
    cleaned = np.where(np.isin(sid,[1,2]),pid,-1)
    je = s3.per_particle_current(res,sid,pid,sig,2)
    je_clean = s3.per_particle_current(res,sid,cleaned,sig,2)
    patches = s3.am_surface_patches(sid,pid,2)
    patches_clean = s3.am_surface_patches(sid,cleaned,2)
    # A separate AM/SE slab with carbon overwritten on AM: live reaction function.
    sr = np.ones((4,4,10),np.int8); sr[:,:,5:]=6
    pr = np.full(sr.shape,-1,np.int32); pr[:2,:,:5]=0; pr[2:,:,:5]=1
    sr[1,1,1:4]=3
    pc = np.where(np.isin(sr,[1,2]),pr,-1)
    si = s3.ionic_sigma_table(.003,.003)
    rx = quiet(s3.solve_reaction_current,sr,sig,si,pr,2,vox,.01,z_top_um=2,z_bot_um=0)
    rc = quiet(s3.solve_reaction_current,sr,sig,si,pc,2,vox,.01,z_top_um=2,z_bot_um=0)
    # One fully overwritten AM voxel column demonstrates no AM ownership remains.
    so = np.zeros((3,3,10),np.int8); so[1,1,:]=3
    po = np.full(so.shape,-1,np.int32); po[1,1,:]=0
    ro = quiet(s3.solve_sigma_z,so,sig,vox,return_field=True,z_bot_um=0,z_top_um=2)
    return {'raster_shape':list(sid.shape),
            'all_additive_input_points_outside_am':bool(np.all(np.linalg.norm(pts[:,None,:]-centers[None,:,:],axis=2)>1.0)),
            'carbon_cells':int((sid==3).sum()),
            'inherited_carbon_cells':int(((sid==3)&(pid>=0)).sum()),
            'je_inherited':je.tolist(),'je_am_masked':je_clean.tolist(),
            'je_ratio':(je/je_clean).tolist(),
            'patches_bitwise_unchanged':all(np.array_equal(patches[k],patches_clean[k]) for k in patches),
            'reaction_i_am':rx['i_am'].tolist(),
            'reaction_bitwise_unchanged':np.array_equal(rx['i_am'],rc['i_am']),
            'reaction_kcl':rx['kcl_err'],
            'no_remaining_am_cells':int(np.isin(so,[1,2]).sum()),
            'fully_overwritten_particle_proxy':s3.per_particle_current(ro,so,po,sig,1).tolist()}


def probe_joule():
    vox=.5; r=.01
    sid=np.ones((4,4,10),np.int8); sid[:,:,5:]=3
    sig=np.zeros(10); sig[[1,3]]=1
    kw=dict(return_field=True,z_bot_um=0,z_top_um=5)
    off=quiet(s3.solve_sigma_z,sid,sig,vox,**kw)
    on=quiet(s3.solve_sigma_z,sid,sig,vox,rint={(1,3):r},**kw)
    jo=s3.joule_hotspot(off,sid,sig,vox,(1,3)); jn=s3.joule_hotspot(on,sid,sig,vox,(1,3))
    shares=s3.phase_current_share(on,sid,sig)
    # Compare normalized spatial pattern, exactly as payload's field normalization.
    qon=jn['q']/jn['q_p99_8']; qoff=jo['q']/jo['q_p99_8']
    return {'sigma_off':off['sigma_eff'],'sigma_on':on['sigma_eff'],
            'interface_share_solver':shares[-1],'interface_share_series_formula':r/(r+5e-4),
            'faces':on['interface']['n_faces_rint'],
            'joule_normalized_max_abs_delta_on_off':float(np.max(np.abs(qon-qoff))),
            'hot_frac_50_on':jn['hot_frac_50'],'hot_frac_50_off':jo['hot_frac_50'],
            'conc_ratio_on':jn['conc_ratio'],'conc_ratio_off':jo['conc_ratio'],
            'joule_return_keys':sorted(jn)}


def probe_context():
    vox=.5
    sid=np.ones((3,3,10),np.int8); sid[:,:,5:]=3
    sig=np.zeros(10); sig[[1,3]]=1
    res=quiet(s3.solve_sigma_z,sid,sig,vox,return_field=True,z_bot_um=0,z_top_um=5,rint={(1,3):.01})
    alternate=np.ones_like(sid)  # Same sigma everywhere: sid mismatch is sole change.
    ja=s3._voxel_jmag(res['phi'],res['cond'],s3.sigma_field(sig,sid),rint_ctx=s3.rint_ctx_from(res,sid))
    jb=s3._voxel_jmag(res['phi'],res['cond'],s3.sigma_field(sig,alternate),rint_ctx=s3.rint_ctx_from(res,alternate))
    a=s3.phase_current_share(res,sid,sig); b=s3.phase_current_share(res,alternate,sig)
    # Solve stores the passed pid by reference. Mutation corrupts the same-sid context too.
    same=np.ones((3,3,10),np.int8); pid=np.zeros(same.shape,np.int32); pid[:,:,5:]=1
    rs=quiet(s3.solve_sigma_z,same,sig,vox,return_field=True,z_bot_um=0,z_top_um=5,rint={(1,1):.01},pid=pid)
    share_before=s3.phase_current_share(rs,same,sig)[-1]
    pid[:]=0
    share_after=s3.phase_current_share(rs,same,sig)[-1]
    return {'caller_sid_mismatch_rejected':False,
            'correct_interface_share':a[-1],'wrong_interface_share':b[-1],
            'jmax_correct':float(ja.max()),'jmax_wrong':float(jb.max()),'jmax_wrong_over_correct':float(jb.max()/ja.max()),
            'pid_alias_is_original':rs['_rint'][1] is pid,
            'pid_mutation_share_before':share_before,'pid_mutation_share_after':share_after,
            'saved_interface_faces_after_pid_mutation':rs['interface']['n_faces_rint']}


def probe_reaction_scope():
    # Two independent transport/BV paths. Only path 0 has an AM|VGCF boundary.
    sid=np.zeros((5,3,12),np.int8)
    for x in (1,3):
        sid[x,1,:6]=1; sid[x,1,6:]=6
    sid[1,1,:4]=3
    pid=np.full(sid.shape,-1,np.int32); pid[1,1,:6]=0; pid[3,1,:6]=1
    se=np.zeros(10); se[[1,3]]=1
    si=np.zeros(10); si[6]=1
    vox=.5; gct=1.; r=.01
    rx=quiet(s3.solve_reaction_current,sid,se,si,pid,2,vox,gct,z_bot_um=0,z_top_um=6)
    # Actual current for no film verifies resistor-chain oracle: two half-cell plate
    # edges (1 each), 10 internal edges (2 each), BV edge (1): R0=23.
    resistance_off=2*(.5/vox)+10/vox+1/gct
    resistance_film=r*1e4/vox**2
    oracle=np.array([1/(resistance_off+resistance_film),1/resistance_off])
    return {'actual_rxn_currents':rx['i_am'].tolist(),'actual_rxn_normalized':(rx['i_am']/rx['i_am'].mean()).tolist(),
            'oracle_off_current':1/resistance_off,'oracle_with_film_currents':oracle.tolist(),
            'oracle_with_film_normalized':(oracle/oracle.mean()).tolist(),
            'film_path_reaction_suppression_pct':100*(1-oracle[0]/rx['i_am'][0]),
            'current_function_has_rint_parameter':'rint' in __import__('inspect').signature(s3.solve_reaction_current).parameters}


def probe_serialization():
    # Parse and execute the actual producer's np.savez_compressed expression with
    # a capturing callable. This obtains real stored kwargs, not a copied schema.
    tree=ast.parse((ROOT/'source/scripts/mpm_webapp_payload.py').read_text(encoding='utf-8'))
    call=next(n for n in ast.walk(tree) if isinstance(n,ast.Call) and
              isinstance(n.func,ast.Attribute) and n.func.attr=='savez_compressed' and n.lineno==2771)
    from types import SimpleNamespace
    captured={}
    class NP:
        def __getattr__(self,n): return getattr(np,n)
        def savez_compressed(self,*a,**k): captured.update(k)
    env={'np':NP(),'a':SimpleNamespace(save_step4_grid='not_written.npz',step3_vox=.5,periodic=False,
                                     _rint_e={(1,3):.01},_rint_i=None),
         'sid3':np.ones((3,3,10)),'pid3':np.zeros((3,3,10)),'_zt3':5.,
         '_sig3':np.ones(10),'_sig3i':np.ones(10),'_osh':np.zeros(3),'r':np.ones(2),
         'UM':1.,'json':json,'_temp_prov':{},'_tkw':{}}
    eval(compile(ast.Expression(call),'<actual_save_expression>','eval'),env)
    return {'actual_save_line':call.lineno,'stored_keys':sorted(captured),
            'contains_interface_or_rint':any('rint' in k or 'interface' in k or 'iface' in k for k in captured)}


def probe_zero_api():
    sig=np.zeros(10);sig[1]=.01;sig[3]=100
    sid=np.ones((3,3,10),np.int8);sid[:,:,5:]=3
    a=quiet(s3.solve_sigma_z,sid,sig,.5,return_field=True,z_bot_um=0,z_top_um=5)
    b=quiet(s3.solve_sigma_z,sid,sig,.5,return_field=True,z_bot_um=0,z_top_um=5,rint={(1,3):0.})
    sa=s3.phase_current_share(a,sid,sig);sb=s3.phase_current_share(b,sid,sig)
    api=s3._check_rint_table({(1.7,3):True})
    return {'zero_sigma_bitwise_equal':a['sigma_eff'].hex()==b['sigma_eff'].hex(),
            'zero_phi_bitwise_equal':np.array_equal(a['phi'],b['phi']),
            'shares_off':sa,'shares_zero':sb,
            'max_share_delta':max(abs(sa[k]-sb[k]) for k in sa),
            'coerced_noninteger_bool':str(api),
            'unknown_sid_accepted':str(s3._check_rint_table({(0,3):1.}))}


if __name__=='__main__':
    out={'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
         (ROOT/'source/scripts').glob('*.py') if p.name in ('step3_sigma.py','mpm_webapp_payload.py','step4_dyn.py')},
         'pid':probe_pid(),'joule':probe_joule(),'context':probe_context(),
         'reaction_scope':probe_reaction_scope(),'serialization':probe_serialization(),'zero_api':probe_zero_api()}
    report=json.dumps(out,indent=2)
    (HERE/'consumer_results.json').write_text(report,encoding='utf-8')
    print(report)
