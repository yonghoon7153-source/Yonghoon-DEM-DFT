"""Read the bounded step-145 capture. No dynamics, field imports or time advances."""
import argparse
from decimal import Decimal, localcontext
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np


def dec(x):
    return Decimal.from_float(float(x))


def evaluate_impulse(node, impulses):
    """Re-evaluate frozen binary64 coefficients in 70-digit decimal arithmetic."""
    with localcontext() as ctx:
        ctx.prec = 70
        m = [dec(x) for x in node["mass"]]
        v0 = [[dec(x) for x in row] for row in node["incoming"]]
        v = [row.copy() for row in v0]
        mu = dec(node["mu"])
        normals = [[dec(x) for x in row] for row in node["normal"]]
        qn = [dec(x) for x in impulses[0::2]]
        qt = [dec(x) for x in impulses[1::2]]
        pairs = list(zip(node["left"], node["right"]))
        for p, (i, j) in enumerate(pairs):
            # Reproduce the binary64 reduced mass used by the pinned kernel,
            # then freeze it with the normal and scaled impulses.
            reduced = dec(1.0/(1.0/float(m[i]) + 1.0/float(m[j])))
            nx, ny = normals[p]
            kick = [reduced*(qn[p]*nx - qt[p]*ny), reduced*(qn[p]*ny + qt[p]*nx)]
            for d in (0, 1):
                v[i][d] -= kick[d]/m[i]
                v[j][d] += kick[d]/m[j]
        errors = []
        for p, (i, j) in enumerate(pairs):
            dx, dy = (v[i][d] - v[j][d] for d in (0, 1))
            nx, ny = normals[p]
            closing, slip = dx*nx + dy*ny, -dx*ny + dy*nx
            dn = max(-qn[p], closing)
            lim = mu*(qn[p] + dn)
            dt = max(-lim-qt[p], min(lim-qt[p], slip))
            errors.append(max(abs(dn), abs(dt)))
        def energy(vel):
            return sum(m[i]*sum((vel[i][d]-v0[0][d])**2 for d in (0,1)) for i in range(len(m)))
        e0 = energy(v0)
        speed_tol = dec(node["speed_tol"])
        return {"residual": float(max(errors)), "worst_pair": int(np.argmax(errors)),
                "energy_bound_satisfied": energy(v) <= e0 + dec(1e-11)*e0 + sum(m)*speed_tol**2}


def look_for_witness(node):
    """Try all face labels through four fields, stop at first strict residual witness."""
    m, vin = np.array(node["mass"]), np.array(node["incoming"])
    count = len(node["left"])
    if len(m) > 4:
        return {"status": "SKIPPED_MORE_THAN_FOUR_FIELDS", "examined": 0}
    normals = np.array(node["normal"])
    pairs = list(zip(node["left"], node["right"]))
    g = np.zeros((2*count, 2*len(m)))
    for p, (i,j) in enumerate(pairs):
        nx, ny = normals[p]
        axes = np.array([[nx,ny],[-ny,nx]])
        g[2*p:2*p+2,2*i:2*i+2] = -axes
        g[2*p:2*p+2,2*j:2*j+2] = axes
    reduced = np.array([1.0/(1.0/m[i]+1.0/m[j]) for i,j in pairs])
    response = ((g / np.repeat(m,2)) @ g.T) * np.repeat(reduced,2)
    # Subtract common translation before forming the right-hand side.
    rhs0 = -(g @ (vin-vin[0]).ravel())
    mu, tol = node["mu"], node["speed_tol"]
    modes = ("open", "stick", "plus", "minus") if mu else ("open", "normal")
    skipped = 0
    for examined, face in enumerate(itertools.product(modes, repeat=count), 1):
        a = np.eye(2*count)
        rhs = np.zeros(2*count)
        for p,state in enumerate(face):
            if state == "open":
                continue
            n = 2*p
            a[n], rhs[n] = response[n], rhs0[n]
            if state == "stick":
                a[n+1], rhs[n+1] = response[n+1], rhs0[n+1]
            elif state in ("plus","minus"):
                a[n+1,n] = mu if state == "minus" else -mu
        q, _, rank, _ = np.linalg.lstsq(a,rhs,rcond=None)
        if rank < len(q):
            skipped += 1  # Only one representative of this null space was tried.
        if np.max(np.abs(a@q-rhs)) > 100.0*tol:
            continue
        # Screen obvious cone failures cheaply; the accepted witness always
        # passes the original tolerance under the independent Decimal check.
        if min(q[::2]) < -100.0*tol or max(np.abs(q[1::2])-mu*q[::2]) > 100.0*tol:
            continue
        check = evaluate_impulse(node,q)
        if check["residual"] <= tol and check["energy_bound_satisfied"]:
            return {"status": "WITNESS_AT_ORIGINAL_TOLERANCE", "examined":examined,
                    "modes":list(face),"scaled_impulses_nt":q.tolist(),
                    "decimal_residual":check["residual"],"rank_deficient_seen":skipped}
    return {"status":"NO_VERIFIED_REPRESENTATIVE","examined":examined,"rank_deficient_seen":skipped}


def analyze(node):
    m, v = np.asarray(node["mass"],float), np.asarray(node["incoming"],float)
    pair_indices = list(itertools.combinations(range(len(m)), 2))
    pairs = list(zip(node["left"], node["right"], strict=True))
    p = len(pairs)
    normal = np.asarray(node["normal"],float)
    qn, qt, c, s = (np.asarray(node[k],float) for k in ("jn_scaled","jt_scaled","closing","slip"))
    mu, tol = node["mu"], node["speed_tol"]
    if (len(m)<3 or v.shape!=(len(m),2) or pairs!=pair_indices or
            normal.shape!=(p,2) or any(a.shape!=(p,) for a in (qn,qt,c,s)) or
            not all(np.isfinite(a).all() for a in (m,v,normal,qn,qt,c,s)) or
            min(m)<=0 or np.max(abs(np.linalg.norm(normal,axis=1)-1))>1e-12 or
            not np.isfinite(mu) or mu<0 or not np.isfinite(tol) or tol<=0):
        raise ValueError("Invalid captured nodal input")
    dn = np.maximum(-qn,c)
    dt = np.clip(s,(-mu*qn-qt)-mu*dn,(mu*qn-qt)+mu*dn)
    reported = node["residual"]
    native = float(np.max(np.maximum(abs(dn),abs(dt))))
    if not np.isclose(native,reported,rtol=1e-12,atol=tol*1e-6):
        raise ValueError("Mismatch between captured native residual and pair values")
    terminal = evaluate_impulse(node,np.column_stack((qn,qt)).ravel())
    return {"node_id":node["node_id"],"fields":len(m),"mass_ratio":float(max(m)/min(m)),
            "speed_tol":tol,"iteration":node["iteration"],"native_ratio":native/tol,
            "decimal_ratio_same_terminal_impulses":terminal["residual"]/tol,
            "terminal_residual_survives_decimal_check":terminal["residual"]>tol,
            "witness":look_for_witness(node)}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--nodes", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()
    raw = args.nodes.read_bytes()
    capture = json.loads(raw)
    if (capture.get("protocol")!="F8-original-stop145-nodes-v1" or
            capture.get("step")!=145 or capture.get("mapping")!="ORIGINAL" or not capture.get("nodes")):
        raise ValueError("Unexpected failure capture")
    report = {"scope":"captured terminal iterate and alternate face witnesses on frozen nodes only",
              "capture_sha256":hashlib.sha256(raw).hexdigest(), "nodes":[analyze(n) for n in capture["nodes"]]}
    with args.out.open("x",encoding="ascii",newline="\n") as out:
        out.write(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print("ANALYZED_FROZEN_NODES",len(report["nodes"]))


if __name__ == "__main__":
    main()
