"""Read-only production audit: process-local mutations and small CPU fixtures."""
from pathlib import Path
import sys, os, json, subprocess, tempfile, copy, contextlib, io
ROOT=Path(__file__).resolve().parents[1]
EVD=ROOT/'evidence_g1'
sys.path[:0]=[str(ROOT/'source/scripts'),str(ROOT.parent/'lhs_coverage_review_20260930/deps')]
os.environ['PYTHONUTF8']='1';os.environ['PYTHONIOENCODING']='utf-8';os.environ['PYTHONDONTWRITEBYTECODE']='1'
os.environ['PYTHONPATH']=os.pathsep.join(sys.path[:2])
sys.dont_write_bytecode=True
import numpy as np
import step3_sigma as S3
import run_contract as RC


def child(mode,argv):
    import mpm_webapp_payload as P
    orig=S3.solve_sigma_z
    count=0
    receipts=[]
    def wrapper(*args,**kwargs):
        nonlocal count
        count+=1
        old=S3.CG_MAXITER
        target={'wetted_unconverged':2,'bare_unconverged':3,'main_unconverged':1}.get(mode)
        if count==target:S3.CG_MAXITER=1
        try:r=orig(*args,**kwargs)
        finally:S3.CG_MAXITER=old
        receipts.append({'call':count,'sigma_eff':r.get('sigma_eff'),'cg_info':r.get('cg_info'),
                         'resid':r.get('resid'),'unconverged':r.get('unconverged'),'interface':r.get('interface')})
        return r
    S3.solve_sigma_z=wrapper
    sys.argv=[P.__file__,*argv]
    try:P.main()
    finally:(EVD/f'{mode}_solver_records.json').write_text(json.dumps(receipts,indent=2),encoding='utf-8')


def producer_probes():
    import check_method_discipline as CMD
    import test_rint_receipts as TR
    out=[]
    with tempfile.TemporaryDirectory(dir=EVD) as d:
        am,se,ph,fid,dia=CMD._smoke_fixture(d)
        base=['--scaffold',am,'--se',se,'--phase',ph,'--fibre',fid,'--fibre-dia',dia,
              '--n-vox',CMD._SMOKE_NVOX,'--step3-vox',CMD._SMOKE_VOX,
              '--no-pore','--no-thermal','--no-trackb','--no-field','--no-step4','--no-ion',
              '--step3-rint-e','AM_S|AM_S=0.001','AM_S|VGCF=0.002']
        for mode in ['normal','wetted_unconverged','bare_unconverged','main_unconverged']:
            p=EVD/f'{mode}.json'
            r=subprocess.run([sys.executable,__file__,'--child',mode,'--',*base,'--out',str(p)],
                             cwd=d,capture_output=True,text=True,encoding='utf-8',timeout=300)
            log=r.stdout+r.stderr
            (EVD/f'{mode}.log').write_text(log,encoding='utf-8')
            row={'mode':mode,'rc':r.returncode,'published':p.exists(),
                 'warning_present':'STEP3 CG not converged' in log}
            if p.exists():
                _,s,m=TR.load_manifest(p)
                row.update(sigma_e=s.get('sigma_e_eff_S_cm'),collector=s.get('collector_geometric'),
                           collector_status=(m.get('components') or {}).get('collector_geom'),
                           receipt_contract=RC.interface_record_ok(m),receipts=m.get('interface_receipts'))
                stamp=m.get('fibre_stamp') or 'point'
                ar=subprocess.run([sys.executable,str(ROOT/'source/scripts/sr01_stamp_compare.py'),
                                   '--check-arm',str(p),'--stamp',stamp],capture_output=True,text=True,encoding='utf-8',timeout=60,cwd=d)
                row['check_arm_rc']=ar.returncode
                (EVD/f'{mode}_check_arm.log').write_text(ar.stdout+ar.stderr,encoding='utf-8')
            out.append(row)
            print(json.dumps(row,ensure_ascii=False),flush=True)
    return out


def api_probes():
    import rint03_je_compare as C
    from scipy.stats import spearmanr
    sid=np.ones((3,3,10),np.int8);sid[:,:,5:]=3
    sig=np.zeros(10);sig[[1,3]]=1
    with contextlib.redirect_stdout(io.StringIO()):
        r=S3.solve_sigma_z(sid,sig,.5,return_field=True,z_top_um=5,z_bot_um=0,rint={(1,3):.01})
    def rejected(fn):
        try:fn();return False
        except ValueError:return True
    checks={'sid_mismatch_rejected':rejected(lambda:S3.phase_current_share(r,np.ones_like(sid),sig)),
            'sigma_mismatch_rejected':rejected(lambda:S3.joule_hotspot(r,sid,sig*2,.5,(1,3)))}
    tb={'AM_S|VGCF':.01}
    m={'interface_rint_e_ohm_cm2':tb,'interface_rint_i_ohm_cm2':None,
       'interface_model':S3.INTERFACE_MODEL_VERSION,'component_plan':{'collector':True,'ionic':False},
       'interface_receipts':{'electronic_main':RC.interface_receipt(r,tb),
                             'electronic_wetted':RC.interface_receipt(r,tb),
                             'electronic_bare':RC.interface_receipt(r,tb),'ionic':{'status':'not_requested'}}}
    checks['base_receipt_valid']=RC.interface_record_ok(m)
    bad=copy.deepcopy(m);bad['interface_receipts']['electronic_wetted'].update(status='failed',why='injected_failure',n_faces_rint=0,faces_by_pair={},solved=False)
    checks['failed_receipt_with_successful_result_contract']=RC.interface_record_ok(bad)
    checks['spearman_ties']={'a':[1,1,2],'b':[1,2,2], 'actual':C._spearman(np.array([1,1,2]),np.array([1,2,2])),
                              'tie_aware_reference':float(spearmanr([1,1,2],[1,2,2]).statistic)}
    checks['spearman_all_zero']={'actual':C._spearman(np.zeros(5),np.zeros(5)),'reference':'undefined (constant rank)'}
    # Prior independent counterexample rebuilt against the new production code.
    vox=.2
    pts=np.c_[np.full(30,2.181),np.full(30,1.1),np.linspace(.05,3.95,30)]
    centers=np.array([[1.18,1.1,1.0],[1.18,1.1,3.0]])
    ss,pp=S3.rasterize(centers,np.ones(2),np.array([2,2]),pts,np.full(30,2),
                       (0,0,0),(2.2,2.2,4),vox,add_fid=np.zeros(30,dtype=int),bridge_um=.24)
    st=S3.electronic_sigma_table(.01,.005,100,10,250)
    with contextlib.redirect_stdout(io.StringIO()):
        rr=S3.solve_sigma_z(ss,st,vox,return_field=True,z_bot_um=0,z_top_um=4)
    jj=C.face_current_proxy(rr,ss,st)
    old,_=C.masked_mean(jj,pp,pp>=0,2)
    new=S3.per_particle_current(rr,ss,pp,st,2)
    checks['tangent_raster_ownership']={'input_points_outside_am':bool(np.all(np.linalg.norm(pts[:,None,:]-centers[None,:,:],axis=2)>1)),
             'old_je':old.tolist(),'new_actual_je':new.tolist(),'old_over_new':(old/new).tolist(),
             'new_matches_explicit_am_mask':bool(np.array_equal(new,C.masked_mean(jj,pp,(pp>=0)&np.isin(ss,[1,2]),2)[0]))}
    # Warning omission alone is weaker than a finite residual contract.
    original=S3._solve_cg
    try:
        S3._solve_cg=lambda L,b:(np.full(len(b),np.nan),0)
        capture=io.StringIO()
        with contextlib.redirect_stdout(capture):
            rn=S3.solve_sigma_z(sid,sig,.5,return_field=True,z_top_um=5,z_bot_um=0)
    finally:S3._solve_cg=original
    checks['nonfinite_residual_warning']={'warning_emitted':'STEP3 CG not converged' in capture.getvalue(),
              'unconverged':rn['unconverged'],'resid_finite':bool(np.isfinite(rn['resid'])),
              'note':'Process-local injected NaN CG result; not evidence the three historical realbed solves had NaNs.'}
    return checks


if __name__=='__main__':
    if '--child' in sys.argv:
        child(sys.argv[2],sys.argv[sys.argv.index('--')+1:])
    else:
        ans={'api':api_probes(),'producer':producer_probes()}
        (EVD/'adversarial_results.json').write_text(json.dumps(ans,ensure_ascii=False,indent=2),encoding='utf-8')
        print(json.dumps(ans['api'],ensure_ascii=False,indent=2))
