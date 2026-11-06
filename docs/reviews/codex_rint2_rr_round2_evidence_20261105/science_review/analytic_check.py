"""Independent normalized midpoint-TLM check; no production geometry or research run.

Unit choices: r1=r2=1, lambda=1, Delta=d, L=m*d, g=1/2.
The closed form follows the second-difference equation for rail voltage difference.
No imports from the supplied repo, so missing production dependencies are not masked.
"""
import json
import math
import platform
import numpy as np
import scipy
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve


def circuit(m, d):
    # m midpoint rail nodes each, source and drain have half-cell lead resistance.
    src, sink = 2*m, 2*m+1
    edges = [(src, 0, 2/d), (2*m-1, sink, 2/d)]
    edges += [(i, i+1, 1/d) for i in range(m-1)]
    edges += [(m+i, m+i+1, 1/d) for i in range(m-1)]
    edges += [(i, m+i, d/2) for i in range(m)]
    row, col, val = [], [], []
    for i, j, g in edges:
        row.extend((i,j,i,j)); col.extend((i,j,j,i)); val.extend((g,g,-g,-g))
    lap = coo_matrix((val,(row,col)), shape=(2*m+2,2*m+2)).tocsr()
    v = np.zeros(2*m+2); v[src] = 1
    v[:2*m] = spsolve(lap[:2*m,:2*m], -lap[:2*m,src].toarray().ravel())
    return 1/float((lap@v)[src])


def closed(m, d):
    theta = 2*math.asinh(d/2)
    return m*d/2 + (d/2)/math.tanh(theta/2)/math.tanh(m*theta/2)


def continuum(m, d):
    return m*d/2 + 1/math.tanh(m*d/2)


def tolerance(m, d):
    return 1.5*(d*d/8 + d/(3*m))


out = {"environment": {"python":platform.python_version(), "numpy":np.__version__, "scipy":scipy.__version__},
       "scope":"independent normalized circuit only; no production-kit data or production modules",
       "cases":[]}
for m,d in ((50,.2),(30,.2),(60,.1),(30,.02),(2,.2),(30,math.sqrt(.4))):
    c,dc,ct = circuit(m,d),closed(m,d),continuum(m,d)
    out["cases"].append({"m":m,"d_over_lambda":d,"q":m*d,"circuit":c,"discrete_closed":dc,
      "continuum":ct,"circuit_closed_rel":abs(c-dc)/dc,"analytic_error":abs(dc-ct),
      "tolerance":tolerance(m,d),"error_tolerance_ratio":abs(dc-ct)/tolerance(m,d)})
# This sweep assesses the stated allowance, not a proof nor a production test.
worst = (-1,None)
for m in range(1,1001):
    for d in np.geomspace(.001,math.sqrt(.4),151):
        ratio=abs(closed(m,float(d))-continuum(m,float(d)))/tolerance(m,float(d))
        if ratio>worst[0]: worst=(ratio,{"m":m,"d_over_lambda":float(d)})
out["tolerance_sweep"]={"n_cases":151000,"max_error_tolerance_ratio":worst[0],"at":worst[1]}
errors=[abs(closed(m,d)-continuum(m,d))/continuum(m,d) for m,d in ((30,.2),(60,.1))]
out["second_order_error_ratio"]=errors[0]/errors[1]
out["saturation_junction_part_ratio"]=(closed(50,.2)-5)/(closed(30,.2)-3)
out["assertions"]={"circuit_closed":max(x["circuit_closed_rel"] for x in out["cases"])<1e-11,
 "six_cases_within_allowance":all(x["error_tolerance_ratio"]<=1 for x in out["cases"]),
 "sweep_within_allowance":worst[0]<=1,"second_order":3.6<out["second_order_error_ratio"]<4.4}
print(json.dumps(out,indent=2))
assert all(out["assertions"].values())
