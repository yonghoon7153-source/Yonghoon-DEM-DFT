"""Small independent passive-network probes; no production file changes."""
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent / 'lhs_coverage_review_20260930' / 'deps'))
sys.path.insert(0, str(ROOT / 'source' / 'scripts'))
import numpy as np
from scipy.sparse import csr_matrix, diags
from scipy.sparse.linalg import cg
import step3_conv_cert as cert
import step3_sigma as s3


def solve_count(L, b, x0=None, rtol=1e-12):
    count = [0]
    def callback(x):
        count[0] += 1
    x, info = cg(L, b, x0=x0, rtol=rtol, atol=0.0,
                 M=diags(1.0 / L.diagonal()), maxiter=1000, callback=callback)
    return x, int(info), count[0]


def warm_candidate():
    # Positive resistors: bottom --1-- u --1-- v --1-- top;
    # bottom --1/G-- w is a valid one-plate dead-end component.
    G = 1e15
    L = csr_matrix([[2., -1., 0.], [-1., 2., 0.], [0., 0., G]])
    b = np.array([1., 0., G])
    p = np.array([.75, .25, 1.])
    bottom = np.array([0, 2]); gb = np.array([1., G])
    top = np.array([1]); gt = np.array([1.])
    resid = float(np.linalg.norm(L @ p-b) / np.linalg.norm(b))
    resolves = []
    def res(L, b, x0, rtol):
        x, info, it = solve_count(L, b, x0, rtol)
        resolves.append({'iterations': it, 'info': info, 'phi': x.tolist(), 'rtol': rtol})
        return x, info
    c = cert.certify(L, b, p, 0, resid, 1e-12, bottom, gb, top, gt, 1., res)
    first, info, iterations = solve_count(L, b)
    Ib, It = cert.plate_currents(first, bottom, gb, top, gt)
    return {'candidate_phi': p.tolist(), 'true_phi': [2/3, 1/3, 1],
            'true_conductance': 1/3, 'candidate_conductance': .25,
            'relative_error': -.25, 'residual_rel': resid,
            'candidate_energy': float((1-p[0])**2+(p[0]-p[1])**2+p[1]**2),
            'certificate': c, 'resolve': resolves,
            'zero_start': {'phi':first.tolist(), 'info':info, 'iterations':iterations,
                           'Ib':Ib, 'It':It, 'imbalance':abs(Ib-It)/abs(Ib)},
            'scope': 'Certificate sufficiency counterexample. First production zero-start CG does not produce this candidate; B correctly rejects its first iterate.'}


def valid_zero():
    # Each conductor reaches exactly one plate, and no through component exists.
    L = diags([1., 1.], format='csr')
    b = np.array([1., 0.]); p = b.copy()
    def res(L, b, x0, rtol):
        return s3._solve_cg(L, b, x0=x0, rtol=rtol)
    c = cert.certify(L, b, p, 0, 0., 1e-12,
                     np.array([0]), np.array([1.]), np.array([1]), np.array([1.]), 1., res)
    return {'exact_zero_certificate':c, 'scope':'Disconnected-terminal exact zero requires a separate topology certificate, not a relative-current/relative-sigma certificate.'}


def actual_production_cg(small=False, bridge_factor=None):
    """Fixed independent counterexample found by bounded seed-611 passive-chain search."""
    k = np.array([0.03542843081279895,21.113990671509995,0.20370714955448593,
        0.000808971961390796,0.06976120349186236,1.6912757790891766,
        0.021238765753829096,0.0007609288395839504,0.20701635367585214,
        0.004052240218237343,31752.40122359974,0.00015528936294781815,
        2.8720471611538324e-05,0.33794145566284794,0.035436507440546515,
        5.089363857396167,0.0020462968348843712,4.924555717512331,
        0.10125977682414762,1.3150225184986553,1.1619900367249028,
        9.217092548952976e-05,3.113347553856885e-05,225.4217993099028])
    G = 6507979.172281959
    if small:
        k=np.array([3.9749047010591427,0.006535081136400995,0.003293084534476289,
            22992.948551542082,0.00035278660732561336,0.0004798389751913557,
            1339.2933113393337,70807.2008252101,0.4385075410195556,
            3.1577098692370925e-05,84788.55607773518])
        G=20815016.44294986
        # Exact power-of-two scaling preserves floating arithmetic and keeps max g near fibre plate g.
        k=k/16384; G=G/16384
    if small == 'connected':
        k=np.array([0.1036251621769631,77264.71177376187,115.83302628384007,
            188.05389893808805,15.658598399603378,7.184589096729567e-05,0.004872796993466964])
        G=36509171569.75918
        bridge_factor=0.0009451405762888877/float(k.min())
        k=k/(2**25); G=G/(2**25)
    n = len(k)-1
    a = np.zeros((n+1,n+1)); b = np.zeros(n+1)
    a[0,0]=k[0]; a[n-1,n-1]=k[-1]; a[n,n]=G; b[0]=k[0]; b[n]=G
    for i in range(n-1):
        a[i,i]+=k[i+1]; a[i+1,i+1]+=k[i+1]
        a[i,i+1]-=k[i+1]; a[i+1,i]-=k[i+1]
    eps=0. if bridge_factor is None else float(k.min()*bridge_factor)
    if eps:
        a[n,n]+=eps; a[0,0]+=eps
        a[n,0]-=eps; a[0,n]-=eps
    L=csr_matrix(a)
    s3.GPU_SOLVE=False; s3.AMG_SOLVE=False; s3.CG_MAXITER=1000
    count=[0]; real_cg=s3.cg
    def counting(*args,**kwargs):
        start=count[0]
        def cb(x): count[0]+=1
        kwargs['callback']=cb
        result=real_cg(*args,**kwargs)
        iterations.append(count[0]-start)
        return result
    iterations=[]; s3.cg=counting
    try:
        phi,info=s3._solve_cg(L,b,rtol=1e-12)
        resid=float(np.linalg.norm(L@phi-b)/np.linalg.norm(b))
        c=cert.certify(L,b,phi,int(info),resid,1e-12,
            np.array([0,n]),np.array([k[0],G]),np.array([n-1]),np.array([k[-1]]),1.,
            lambda LL,bb,xx,rt:s3._solve_cg(LL,bb,x0=xx,rtol=rt))
    finally:
        s3.cg=real_cg
    k_eff=k.copy()
    k_eff[0]+=G*eps/(G+eps)
    true=1/np.sum(1/k_eff)
    path=np.r_[1.,phi[:n],0.]
    energy=float(np.sum(k*np.diff(path)**2)+G*(1-phi[n])**2+eps*(phi[n]-phi[0])**2)
    flow_resistance=float(np.sum(1/k_eff)) # exactly feasible unit series/split flow
    return {'description':f'All conductances positive. {n} internal chain nodes plus one bottom stub. Exact analytic reference; first solution is actual production zero-start Jacobi CG, not fabricated.',
            'conductance_chain':k.tolist(),'dead_end_conductance':G,
            'stub_to_first_chain_conductance':eps,'all_nodes_in_through_component':bool(eps),
            'true_G':float(true),'reported_G':c['sigma'],
            'relative_error':float(c['sigma']/true-1),
            'resolve_relative_error':float(c['sigma_resolve']/true-1),
            'iterations_initial_then_resolve':iterations,'certificate':c,
            'energy_upper_G':energy,'feasible_flow_lower_G':1/flow_resistance,
            'energy_rel_gap':float(energy/true-1)}


if __name__ == '__main__':
    out = {'warm_candidate':warm_candidate(), 'valid_zero':valid_zero(),
           'actual_production_cg':actual_production_cg(),
           'actual_production_cg_zero_resolve_iterations':actual_production_cg(small=True)}
    out['actual_production_cg_connected']=actual_production_cg(small='connected')
    print(json.dumps(out, ensure_ascii=False, indent=2))
    (ROOT / 'geometry' / 'convergence_probe_results.json').write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
