"""Read-only RIMP-01 closure probes; outputs are review artifacts only.

Loads both snapshots but does not run their CLIs or write to them.  The old
boundary-control AFTER is compared with the fixed harness unmodified solve.
Independent exact-linear layers use analytic gradient/current, not the new
boundary resistance formula, to check the assembled boundary row sums.
"""
import contextlib
import importlib.util
import io
import json
import math
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'rint_g2_impl_reverify_20261015'
sys.path[:0] = [str(BASE / 'source/scripts'),
               str(ROOT / 'lhs_coverage_review_20260930/deps'),
               str(ROOT / 'gen2_network_reverify3_20261007/deps')]
import numpy as np
import scipy
import rint_t2_dev as T2


def module_at(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def solve_capture(m, n=16, L=1.6, law='axis'):
    original = T2.spsolve
    saved = {}
    def spy(a, b):
        saved['a'], saved['b'] = a, b
        p = original(a, b)
        saved['p'] = p.reshape(n, n)
        return p
    T2.spsolve = spy
    try:
        out = T2.mms_solve(m, n, L, law)
    finally:
        T2.spsolve = original
    saved['exact'] = out.pop('phi_exact')
    return out, saved


def old_counterexamples():
    old_probe = module_at('boundary_old_probe', ROOT / 'rint_g2_impl_review_20261014/probes/rrm_probe.py')
    old_t2 = module_at('boundary_old_t2', ROOT / 'rint_g2_impl_review_20261014/source/scripts/rint_t2_dev.py')
    old_probe.T2 = old_t2
    result = []
    for th, n, law, off in [(15,64,'axis',0.), (30,16,'axis',0.),
                            (45,128,'axis',0.), (45,128,'axis',.001),
                            (15,64,'L1',0.)]:
        old = old_probe.boundary_control(th,n,law,off)
        m = T2.Mms(2,3,2,5,1e-5,th,offset_um=off)
        fixed, _ = solve_capture(m,n,1.6,law)
        delta = {k:fixed[k]-old['after'][k] for k in ('err_max','err_l2')}
        result.append({'theta':th,'n':n,'law':law,'offset_um':off,
                       'old_before':old['before'], 'old_after':old['after'],
                       'fixed_unmodified':fixed, 'fixed_minus_old_after':delta,
                       'old_boundary_adjustments':old['boundary_adjustments']})
    return result


def boundary_geometry(m,n,L):
    h=L/n; xc=-L/2+(np.arange(n)+.5)*h
    X,Y=np.meshgrid(xc,xc,indexing='ij'); U,_=m.uv(X,Y)
    spec = [(0,-1,np.zeros(n,int),np.arange(n),np.full(n,-L/2),xc),
            (0,1,np.full(n,n-1),np.arange(n),np.full(n,L/2),xc),
            (1,-1,np.arange(n),np.zeros(n,int),xc,np.full(n,-L/2)),
            (1,1,np.arange(n),np.full(n,n-1),xc,np.full(n,L/2))]
    return h,xc,X,Y,U,spec


def analytic_linear_oracle(m,n=16,L=1.6,law='axis'):
    """For beta=0, cross-boundary conductance from analytic current/delta phi.

    With axis law, exact normal directional current into each cell is
    sigma(region)*dphi/du*n_axis*outward_sign. Multiplying h^2 and dividing by
    phi(face)-phi(cell) determines its conductance independently of d_c/d_f.
    Internal cross faces are absent in the tested layers/corners.
    """
    out,save=solve_capture(m,n,L,law)
    h,xc,X,Y,U,spec=boundary_geometry(m,n,L)
    expect_diag=np.zeros((n,n)); expect_rhs=np.zeros((n,n)); records=[]
    crossing_by_cell={}
    for axis,sign,ii,jj,fx,fy in spec:
        uf,_=m.uv(fx,fy); pc=m.phi(X[ii,jj],Y[ii,jj]); pf=m.phi(fx,fy)
        crossing=(uf>=0)!=(U[ii,jj]>=0)
        # sigma * directional derivative is s1*alpha*n_axis in either region.
        exact_current=h*h*m.s1*m.alpha*m.n[axis]*sign
        for t,(i,j) in enumerate(zip(ii,jj)):
            sc=m.s2 if U[i,j]>=0 else m.s1
            dp=float(pf[t]-pc[t])
            # Tangential boundary direction has zero current and delta phi.
            g=exact_current/dp if abs(dp)>1e-13 else 2*sc*h
            expect_diag[i,j]+=g; expect_rhs[i,j]+=g*pf[t]
            if crossing[t]:
                key=str((int(i),int(j)))
                crossing_by_cell[key]=crossing_by_cell.get(key,0)+1
                records.append({'cell':[int(i),int(j)],'axis':axis,
                                'outward_sign':sign,'u_cell':float(U[i,j]),
                                'u_face':float(uf[t]),'analytic_g':float(g)})
    got_diag=np.asarray(save['a'].sum(axis=1)).ravel().reshape(n,n)
    got_rhs=save['b'].reshape(n,n)
    residual=save['a']@save['exact'].ravel()-save['b']
    out.update(analytic_boundary_diag_max_abs=float(np.max(abs(got_diag-expect_diag))),
               analytic_boundary_rhs_max_abs=float(np.max(abs(got_rhs-expect_rhs))),
               exact_solution_residual_max=float(np.max(abs(residual))),
               boundary_crossing_by_cell=crossing_by_cell,
               crossing_records=records)
    return out


def analytic_layers():
    out=[]
    # Axis exact normal vectors avoid trig endpoint/tie roundoff here.
    for theta,normal in [(0,(1.,0.)), (90,(0.,1.)), (180,(-1.,0.)), (270,(0.,-1.))]:
        for off in (-.78,.78,-.8,.8):
            for r in (0.,1e-5):
                m=T2.Mms(2,0,2,5,r,theta,offset_um=off)
                m.n=np.array(normal); m.t=np.array([-normal[1],normal[0]])
                rec=analytic_linear_oracle(m)
                rec['layer_kind']='boundary_only_or_endpoint'
                out.append(rec)
    return out


def analytic_corners():
    out=[]
    for theta in (30,45,60,120,135,150,210,225,240,300,315,330):
        for sign in (-1,1):
            m=T2.Mms(2,0,2,5,1e-5,theta)
            # All cell centres on one side; two outward faces of one corner
            # lie on the other side. Internal film count must remain zero.
            m.offset_um=sign*(.75*sum(abs(m.n))+.025*min(abs(m.n)))
            out.append(analytic_linear_oracle(m))
    return out


def tie_diagnostic():
    out=[]; base_phase=None; base_phi=None; base_nontie=None
    for off in (0.,-1e-14,1e-14,-1e-13,1e-13,-1e-11,1e-11,.001):
        m=T2.Mms(2,3,2,5,1e-5,45,offset_um=off)
        rec,save=solve_capture(m,128)
        _,_,X,Y,U,_=boundary_geometry(m,128,1.6)
        phase=U>=0
        if base_phase is None:
            base_phase=phase; base_phi=save['p']; base_nontie=abs(U)>=1e-12
        rec['phase_changes_from_unshifted']=int(np.count_nonzero(phase!=base_phase))
        rec['solution_max_change_from_unshifted']=float(np.max(abs(save['p']-base_phi)))
        rec['non_tie_solution_max_change_from_unshifted']=float(np.max(abs(save['p']-base_phi)[base_nontie]))
        rec['non_tie_err_max']=float(np.max(abs(save['p']-save['exact'])[base_nontie]))
        rec['exact_u_zero_count']=int(np.count_nonzero(U==0))
        rec['near_tie_reg2_count']=int(np.count_nonzero((abs(U)<1e-12)&phase))
        out.append(rec)
    return out


def author_test():
    mod=module_at('boundary_author_test',BASE/'source/scripts/test_rint_t2_dev.py')
    capture=io.StringIO()
    with contextlib.redirect_stdout(capture):
        mod.main()
    return {'stdout':capture.getvalue(),'pass_count':mod._ok,'failures':mod._fail}


if __name__=='__main__':
    report={'pin':'dcb97f1ed942f622d9189eee1a1e9432dc05a655',
            'environment':{'python':sys.version,'numpy':np.__version__,
                           'scipy':scipy.__version__,'OMP_NUM_THREADS':os.environ.get('OMP_NUM_THREADS'),
                           'OPENBLAS_NUM_THREADS':os.environ.get('OPENBLAS_NUM_THREADS')},
            'loaded_fixed_source':str(Path(T2.__file__).resolve()),
            'author_test':author_test(),
            'old_counterexamples':old_counterexamples(),
            'analytic_layers':analytic_layers(),
            'analytic_corners':analytic_corners(),
            'tie_diagnostic':tie_diagnostic()}
    path=BASE/'evidence/boundary_recheck.json'
    path.write_text(json.dumps(report,indent=2,ensure_ascii=False,default=lambda x:x.item() if isinstance(x,np.generic) else str(x))+'\n',encoding='utf-8')
    print(json.dumps({'output':str(path),'author_tests':[report['author_test']['pass_count'],len(report['author_test']['failures'])],
                      'counterexamples':[{k:r[k] for k in ['theta','n','law','offset_um','fixed_minus_old_after']} for r in report['old_counterexamples']],
                      'layer_count':len(report['analytic_layers']),
                      'layer_max_err':max(r['err_max'] for r in report['analytic_layers']),
                      'corner_count':len(report['analytic_corners']),
                      'corner_max_err':max(r['err_max'] for r in report['analytic_corners']),
                      'tie_diagnostic':report['tie_diagnostic']},indent=2,ensure_ascii=False))
