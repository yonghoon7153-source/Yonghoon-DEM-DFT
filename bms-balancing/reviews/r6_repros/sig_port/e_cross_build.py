import sys, json, hashlib, pathlib, numpy as np, scipy
sys.path.insert(0, "/home/user/Yonghoon-DEM-DFT/bms-balancing")
from bms_balancing import verify
from bms_balancing.model import LB5, UB5
from scipy.optimize import minimize
root = pathlib.Path(sys.argv[1])
o = verify.build(root, "GITT", "100", "Li", w_dqdv=0.0, scale_seed=0)
print(f"numpy {np.__version__} scipy {scipy.__version__}")
print("scales    :", {k: float(v).hex() for k, v in o.scales.items()})
print("eps_rel   :", {k: f"{v['eps_rel']:.17g}" for k, v in o.scale_audit.items()})
P = np.array(verify.DD_EVAL_P, dtype=float)
vals = [o(q) for q in P]
print("obj(P)    :", hashlib.sha256(np.array(vals).tobytes()).hexdigest()[:16], [f"{v:.17g}" for v in vals[:2]])
start = LB5 + 0.5 * (UB5 - LB5)
r = minimize(o, start, method="L-BFGS-B", bounds=list(zip(LB5, UB5)), options={"maxiter": 400, "ftol": 1e-12})
print("L-BFGS-B  :", "nit", r.nit, "fun", f"{r.fun:.17g}", "x", [f"{x:.10g}" for x in r.x])
