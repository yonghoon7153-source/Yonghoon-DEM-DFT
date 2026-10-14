"""Offline adversarial RRM / MMS probes, source snapshot read only."""
import contextlib
import copy
import io
import json
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'rint_g2_impl_review_20261014/source/scripts'),
               str(ROOT / 'gen2_network_reverify3_20261007/deps'),
               str(ROOT / 'lhs_coverage_review_20260930/deps')]
import numpy as np
from scipy.integrate import quad
import step3_sigma as S3
import rint_rrm_reference as RRM
import rint_t2_dev as T2
import test_rint_g2_rrm as FIX
FIX.S3 = S3
FIX.RRM = RRM

def quiet(fn, *args, **kwargs):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*args, **kwargs)

def areas():
    rng = np.random.default_rng(20261014)
    worst = [0, None]
    for i in range(1000):
        a = 10**rng.uniform(-2, 1)
        bounds = rng.uniform(-1.4, 1.4, 4) * a
        x0, x1 = sorted(bounds[:2]); y0, y1 = sorted(bounds[2:])
        lo, hi = max(x0, -a), min(x1, a)
        if hi <= lo:
            ref = 0.
        else:
            f = lambda x: max(0., min(y1, math.sqrt(max(a*a-x*x, 0.))) - max(y0, -math.sqrt(max(a*a-x*x, 0.))))
            points = [s*math.sqrt(a*a-y*y) for y in [y0, y1] if abs(y) < a for s in [-1, 1]]
            points = [p for p in points if lo < p < hi]
            ref = quad(f, lo, hi, points=points, epsabs=1e-12*a*a, epsrel=1e-12)[0]
        got = RRM.disc_rect_area(0, 0, a, x0, x1, y0, y1)
        err = abs(got-ref)/(a*a)
        if err > worst[0]: worst = [err, [a, x0, x1, y0, y1, got, ref]]
    return {'samples': 1000, 'max_abs_error_over_a2': worst}

def rrm():
    sid, _, led = quiet(FIX.bed, FIX.A_C, FIX.A_R, FIX.A_T, FIX.A_LO, FIX.A_HI, FIX.A_VOX, FIX.A_BR)
    p = RRM.rrm_plan(led, FIX.RT, resolve_k=4.)
    out = {'base': p['record']['iface_rrm']['contacts'][0],
           'row_counts': {key:p[key] for key in ['n_film_rows','n_cut_rows']}}
    with FIX.direct_solver():
        ans = quiet(RRM.rrm_solve, sid, FIX.te(), FIX.A_VOX, p, led, z_bot_um=0, z_top_um=FIX.A_HI[2], return_field=True)
    out['base_solve'] = {key:ans.get(key) for key in ['sigma_eff','unconverged','resid']}
    out['stored_summary'] = p['record']['iface_contact_ledger']
    out['actual_G_S'] = S3.iface_plan_film_G_S(p).tolist()
    mutations = {}
    mut = FIX.with_rows(p, lambda ax, lin, cut: not cut)
    mutations['cut_rows_removed'] = mut
    q = copy.deepcopy(mut); q['record']['iface_rrm']['resolve_k'] = 5.
    mutations['cut_rows_removed_k_changed'] = q
    q = copy.deepcopy(mut); q['record']['iface_r_type_ohm_cm2'] = {}
    mutations['cut_rows_removed_rtable_removed'] = q
    q = copy.deepcopy(p)
    for ax in q['axes']:
        ax['rface'][~ax['cut']] = np.nan
    q['fp_rows'] = S3._iface_rows_fp(q['axes'])
    mutations['nan_rface'] = q
    out['mutation_checks'] = {}
    for tag, q in mutations.items():
        rec = {'rrm_check': RRM.rrm_check(q, led)}
        try:
            S3.iface_require_quantitative(q, sid, FIX.te())
            rec['production_gate'] = 'accept'
        except Exception as e:
            rec['production_gate'] = type(e).__name__+': '+str(e)
        if tag in ['cut_rows_removed_k_changed', 'cut_rows_removed_rtable_removed', 'nan_rface']:
            try:
                with FIX.direct_solver():
                    ans = quiet(RRM.rrm_solve, sid, FIX.te(), FIX.A_VOX, q, led, z_bot_um=0, z_top_um=FIX.A_HI[2], return_field=True)
                rec['rrm_solve'] = {k: ans.get(k) for k in ['sigma_eff','unconverged','resid']}
            except Exception as e:
                rec['rrm_solve'] = type(e).__name__+': '+str(e)
        out['mutation_checks'][tag] = rec
    return out

def geometry():
    result = []
    for target_axis in range(3):
        order=[i for i in range(3) if i != target_axis]
        order.insert(target_axis,2)
        # Put original z in target axis, original x/y in remaining axes.
        order=[0,1,2] if target_axis==2 else ([2,0,1] if target_axis==0 else [0,2,1])
        c = FIX.B_C[:,order]
        lo=np.asarray(FIX.B_LO)[order]; hi=np.asarray(FIX.B_HI)[order]
        sid,_,led = quiet(FIX.bed,c,FIX.B_R,FIX.B_T,lo,hi,.1,.7)
        p=RRM.rrm_plan(led,FIX.RT,resolve_k=4.)
        rec=p['record']['iface_rrm']['contacts'][0]
        result.append({'rotation_axis':target_axis,'rejections':p['rejections'],'check':RRM.rrm_check(p,led),'contact':rec})
    sid,_,led0=quiet(FIX.bed,FIX.A_C,FIX.A_R,FIX.A_T,FIX.A_LO,FIX.A_HI,.1,.7)
    carbon_sid=sid.copy()
    # Replace left half of each AM cell with a carbon material label.
    carbon_sid[:10,:,:][np.isin(carbon_sid[:10,:,:],(1,2))] = 3
    led=S3.am_iface_ledger(FIX.A_C,FIX.A_R,FIX.A_T,carbon_sid,sid,FIX.A_LO,.1,delta_bound_um=0.,bridge_um=.7)
    p=RRM.rrm_plan(led,FIX.RT,resolve_k=4.)
    result.append({'carbon_half':True,'check':RRM.rrm_check(p,led),'contact':p['record']['iface_rrm']['contacts'][0],
                   'row_counts':{key:p[key] for key in ['n_film_rows','n_cut_rows']},
                   'CNC_summary_film_G_S_total':p['record']['iface_contact_ledger']['film_G_S_total'],
                   'actual_G_S':S3.iface_plan_film_G_S(p).tolist()})
    return result

def mms():
    saved = T2.spsolve
    out = []
    for theta, n in [(0, 16), (15, 64), (30, 16), (45, 16), (45, 128)]:
        holder = {}
        def solver(a, b):
            p = saved(a, b); holder['p'] = p; return p
        T2.spsolve = solver
        m = T2.Mms(2, 3, 2, 5, 1e-5, theta)
        ans = T2.mms_solve(m, n, 1.6, 'axis')
        T2.spsolve = saved
        h = 1.6/n
        xc = -0.8 + (np.arange(n)+.5)*h
        x,y = np.meshgrid(xc,xc,indexing='ij')
        u,v = m.uv(x,y)
        err = holder['p'].reshape(n,n) - ans.pop('phi_exact')
        idx = tuple(np.unravel_index(np.argmax(np.abs(err)), err.shape))
        tie = abs(u) < 1e-12
        bc_cross = []
        for ii,jj,fx,fy in [(np.zeros(n,int),np.arange(n),np.full(n,-.8),xc), (np.full(n,n-1),np.arange(n),np.full(n,.8),xc),
                            (np.arange(n),np.zeros(n,int),xc,np.full(n,-.8)), (np.arange(n),np.full(n,n-1),xc,np.full(n,.8))]:
            ub,_ = m.uv(fx,fy)
            for t in np.flatnonzero((ub>=0) != (u[ii,jj]>=0)):
                bc_cross.append({'ij':[int(ii[t]),int(jj[t])], 'cell_u':float(u[ii[t],jj[t]]), 'face_u':float(ub[t]),'error':float(err[ii[t],jj[t]])})
        ans.update(max_ij=idx, max_u=float(u[idx]), max_v=float(v[idx]), signed_max_error=float(err[idx]),
                   tie_count=int(tie.sum()), non_tie_err_max=float(np.max(np.abs(err[~tie]))),
                   non_tie_err_l2=float(np.sqrt(np.mean(err[~tie]**2))), boundary_segment_crosses=bc_cross)
        out.append(ans)
    return out

def boundary_control(theta, n, law='axis', offset=0.):
    """Change only boundary series conductance when its half-cell crosses u=0.

    Exact crossing fraction is linear in u; resistance integrates two bulk
    lengths and adds the SAME candidate film law used on interior faces.
    All interior entries, exact Dirichlet values and error targets stay fixed.
    This isolates the unaccounted boundary film, not a validated tilted method.
    """
    class ShiftMms(T2.Mms):
        def uv(self, x, y):
            u, v = super().uv(x,y)
            return u-offset, v
    m = ShiftMms(2,3,2,5,1e-5,theta)
    saved = T2.spsolve
    h = 1.6/n
    xc = -.8 + (np.arange(n)+.5)*h
    x,y = np.meshgrid(xc,xc,indexing='ij')
    u,_ = m.uv(x,y)
    holder = {}
    def plain(a,b):
        p = saved(a,b); holder['p']=p; return p
    T2.spsolve = plain
    before = T2.mms_solve(m,n,1.6,law)
    before.pop('phi_exact')
    adjustments=[]
    def fixed(a,b):
        diag = a.diagonal().copy(); b=b.copy()
        for axis,ii,jj,fx,fy in [(0,np.zeros(n,int),np.arange(n),np.full(n,-.8),xc),
                                   (0,np.full(n,n-1),np.arange(n),np.full(n,.8),xc),
                                   (1,np.arange(n),np.zeros(n,int),xc,np.full(n,-.8)),
                                   (1,np.arange(n),np.full(n,n-1),xc,np.full(n,.8))]:
            ub,_ = m.uv(fx,fy)
            cross = (ub>=0) != (u[ii,jj]>=0)
            bc_phi = m.phi(fx,fy)
            for t in np.flatnonzero(cross):
                i,j=int(ii[t]),int(jj[t]); q=i*n+j
                uc = float(u[i,j]); uf = float(ub[t])
                sc = m.s2 if uc>=0 else m.s1
                sf = m.s2 if uf>=0 else m.s1
                d1 = .5*h*abs(uc)/(abs(uc)+abs(uf)); d2=.5*h-d1
                old = 2*sc*h
                new = h*h/(d1/sc + d2/sf + 1e4*T2._face_rface(m,axis,law))
                diag[q] += new-old
                b[q] += (new-old)*bc_phi[t]
                adjustments.append({'ij':[i,j],'axis':axis,'u_cell':uc,'u_boundary':uf,
                                    'd_cell':d1,'d_boundary':d2,'g_old':old,'g_new':new})
        a=a.copy(); a.setdiag(diag)
        p=saved(a,b); holder['p']=p; return p
    T2.spsolve=fixed
    try:
        after=T2.mms_solve(m,n,1.6,law)
    finally:
        T2.spsolve=saved
    ex=after.pop('phi_exact')
    err=holder['p'].reshape(n,n)-ex
    after['max_ij']=tuple(np.unravel_index(np.argmax(abs(err)),err.shape))
    return {'theta':theta,'n':n,'law':law,'normal_offset_um':offset,'tie_count':int((abs(u)<1e-12).sum()),'before':before,'after':after,'boundary_adjustments':adjustments}

if __name__ == '__main__':
    result = {'areas': areas(), 'rrm': rrm(), 'geometry':geometry(),'mms': mms(),
              'boundary_controls':[boundary_control(th,n,law,off) for th,n,law,off in
                                   [(15,64,'axis',0.),(30,16,'axis',0.),(45,128,'axis',0.),
                                    (45,128,'axis',.001),(15,64,'L1',0.)]]}
    print(json.dumps(result, indent=2, ensure_ascii=False, default=lambda x: x.item() if isinstance(x, np.generic) else str(x)))
