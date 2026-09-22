"""Analytical countermodels for R17 inferences; NOT real-data reproduction."""
import json, pathlib, sys
import numpy as np
from scipy.optimize import minimize

HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[1]/'work/r17-head/bms-balancing'
sys.path.insert(0,str(ROOT))
from bms_balancing.model import Objective
from bms_balancing import cycles, model

result={'scope':'Analytical synthetic countermodels; no real battery input or external fit results reproduced.'}
# Both models have positive definite Hessian 2 I and a unique minimizer.
# Changing gamma initialization/lower bound has no effect; changing model does.
fits=[]
for label,target in [('A',np.array([1.,0.,1.02,0.,.2407])),('B',np.array([1.,0.,.98,0.,.2240]))]:
    for g0,lower in [(.25,0.),(.02,.02)]:
        x0=np.array([1.,0.,1.,0.,g0])
        r=minimize(lambda p:float(np.sum((p-target)**2)),x0,
                   jac=lambda p:2*(p-target),method='L-BFGS-B',
                   bounds=[(.5,1.5),(-.2,.2),(.5,1.5),(-.2,.2),(lower,1.)],
                   options={'ftol':1e-15,'gtol':1e-12})
        assert r.success and np.max(np.abs(r.x-target))<1e-8
        fits.append(dict(model=label,gamma_initial=g0,gamma_lower=lower,
                         optimum=r.x.tolist(),hessian_eigenvalues=[2.]*5,
                         signed_ne_proxy=float(1-r.x[2])))
result['same_optimum_not_nonidentifiability']=fits
# Wider observed lower bounds do not order the unknown true spans.
result['lower_bound_order_counterexample']={
    'observed_A':2.439,'observed_B':7.099,'possible_true_A':20.,'possible_true_B':8.,
    'observed_B_over_A':7.099/2.439,'true_B_over_A':8/20,
    'all_lower_bound_inequalities_hold':2.439<=20 and 7.099<=8}
# Relative-to-minimum tolerance can grow when a conflicting nonnegative residual
# is added, even though objective curvature increases and the optimum is unique.
# JA=1+x^2; Jextra=100+(x-.1)^2; JB=101.005+2*(x-.05)^2.
tol=.01
result['relative_threshold_counterexample']={
    'A':{'minimum':1.,'curvature':2.,'exact_width':2*np.sqrt(.01)},
    'B':{'minimum':101.005,'curvature':4.,'exact_width':2*np.sqrt(101.005*.01/2)},
    'definition':'full width of J<=1.01*J_min',
    'reason':'Minimum-dependent threshold changes, not a calibrated confidence region.'}
# Independent chain-rule check of the target's actual E_cell/dv_cell methods.
# Analytic curves avoid interpolation/smoothing and real-data ambiguity.
class Half:
    E_PE=staticmethod(lambda x:3.+np.asarray(x)**2)
    dv_PE=staticmethod(lambda x:2*np.asarray(x))
class Blend:
    E=staticmethod(lambda x,g:.2+.3*np.asarray(x)**2)
    dv=staticmethod(lambda x,g:.6*np.asarray(x))
o=Objective.__new__(Objective);o.half=Half();o.blend=Blend()
p=np.array([.8,.1,1.2,-.1,.2]);x=np.linspace(.2,.6,101);h=1e-6
fd=(o.E_cell(p,x+h)-o.E_cell(p,x-h))/(2*h)
raw=o.dv_cell(p,x)
fixed=Half.dv_PE((x-p[1])/p[0])/p[0]-Blend.dv((x-p[3])/p[2],p[4])/p[2]
result['known_chain_rule_independent_check']={
    'legacy_max_abs_error':float(np.max(np.abs(fd-raw))),
    'corrected_formula_max_abs_error':float(np.max(np.abs(fd-fixed))),
    'not_new_finding':True,'not_author_200x_fit_reproduction':True}
assert np.max(np.abs(fd-raw))>.1 and np.max(np.abs(fd-fixed))<1e-8
# Invalid tolerance makes {J<=J_best*(1+tol)} empty. Actual implementation
# includes best anyway and returns measured zero-width, not failed/refused.
bp=(model.LB5+model.UB5)/2
width=cycles._width_fields(True,lambda p:1.,bp,1.,1.,bp,1.,-.5,0,0,model.LB5,lambda *a:None)
result['negative_tolerance_empty_set']={'objective_everywhere':1.,'limit':.5,'actual':width}
(HERE/'SCIENCE_REPRO_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
