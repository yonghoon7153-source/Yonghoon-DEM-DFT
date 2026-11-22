"""Independent read-only return diagnostic and compact synthetic checks; no time stepping."""
import csv
import hashlib
import importlib.util
import io
import itertools
import json
from pathlib import Path
import sys
import tarfile

import numpy as np


def curve(archive, key):
    with tarfile.open(archive, "r:gz") as tar:
        raw = tar.extractfile(key).read()
    cols = list(csv.DictReader(io.StringIO(raw.decode("ascii"))))
    step = np.array([int(r["step"]) for r in cols])
    h = np.array([float(r["height"]) for r in cols])
    x = h[0]-h
    p = np.array([float(r["bottom_pressure_E"])*10 for r in cols])
    assert np.array_equal(step,np.arange(len(step))) and (np.diff(x)>0).all()
    assert np.isfinite(p).all()
    return x, p


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def solve(module, pos, mass, vin, ids, order, mu):
    ids, order = np.array(ids), np.array(order)
    centers = np.empty_like(pos)
    centers[ids] = pos
    v = vin[order].copy()
    module.project_contacts(ids[order], np.zeros(len(pos), int), mass[order],
                            (pos*mass[:,None])[order], v, centers, mu)
    return v[np.argsort(order)]


def synthetic(folder):
    old = load("frozen_historical", folder/"scripts/suyoung_u6_first_dev.py")
    new = load("bounded_kernel", folder/"scripts/suyoung_multicontact_dev.py")
    pos = np.array([[-.3,.5],[.4,-.1],[.1,.9]])
    m = np.array([1.2,1.8,.7])
    v = np.array([[.71,-.15],[-.22,.47],[-.34,-.42]])
    def perms(kernel):
        return np.array([solve(kernel, pos,m,v,ids,np.roll(ids,1),.5)
                         for ids in itertools.permutations(range(3))])
    vo,vn = perms(old),perms(new)
    assert np.array_equal(vn,np.broadcast_to(vn[0],vn.shape))
    assert np.max(np.abs(vo-vo[0]))>1e-4
    assert np.max(np.abs((m@v)-(m@vn[0])))<1e-14
    assert np.sum(m[:,None]*vn[0]**2)<=np.sum(m[:,None]*v**2)
    count = 0
    for s in (0.,.3,-.3,1.5,-1.5,3.,-3.):
        # Positive normal, oblique coordinate axes, 2.0 closing speed,
        # Coulomb switch at |s|=1.0; analytic reduced mass impulses.
        n=np.array([.6,.8])
        t=np.array([-.8,.6])
        pos2=np.array([-n,n])
        m2=np.array([.5,2.])
        vin=np.array([2*n+s*t,np.zeros(2)])
        kick=.4*(2*n+np.clip(s,-1,1)*t)
        expected=vin+np.array([-kick/m2[0],kick/m2[1]])
        for ids in ((0,1),(1,0)):
            o=solve(old,pos2,m2,vin,ids,ids,.5)
            c=solve(new,pos2,m2,vin,ids,ids,.5)
            assert np.array_equal(o,c)
            np.testing.assert_allclose(c,expected,atol=2e-15,rtol=0)
            np.testing.assert_allclose(m2@c,m2@vin,atol=2e-15,rtol=0)
            assert np.sum(m2[:,None]*c**2)<=np.sum(m2[:,None]*vin**2)
            count+=1
    return dict(three_ids=6,old_max_velocity_shift=float(np.max(np.abs(vo-vo[0]))),
                new_max_velocity_shift=float(np.max(np.abs(vn-vn[0]))),two_body_cases=count)


def main(repo, wall, order, now, out):
    paths=[(wall,"run/arms/F8/trace.csv"),(order,"run/F8_RELABEL/trace.csv"),
           (now,"run/ORIGINAL/trace.csv"),(now,"run/REVERSED/trace.csv")]
    curves=[curve(a,b) for a,b in paths]
    end=min(x[-1] for x,_ in curves)
    union=np.unique(np.concatenate([x[x<=end] for x,_ in curves]))
    vals=[np.interp(union,x,p) for x,p in curves]
    pold,poldr,pnew,pnewr=vals
    assert len(union)==min(len(x) for x,_ in curves)
    assert all(np.array_equal(union,x[:len(union)]) for x,_ in curves)
    assert np.array_equal(curves[2][0],curves[3][0])
    diagnostic=dict(common_points=len(union),end=float(end),grid_sizes=[len(x) for x,_ in curves],
        common_old=float(np.max(np.abs(pold-poldr))),common_new=float(np.max(np.abs(pnew-pnewr))),
        model_change_o=float(np.max(np.abs(pold-pnew))),model_change_r=float(np.max(np.abs(poldr-pnewr))),
        new_full_pair=float(np.max(np.abs(curves[2][1]-curves[3][1]))),
        count_different_new_values=int(np.count_nonzero(curves[2][1]!=curves[3][1])),
        last_steps=[len(x)-1 for x,_ in curves])
    result={"archive_sha":hashlib.sha256(now.read_bytes()).hexdigest(),
            "four_common":diagnostic,"synthetic":synthetic(repo)}
    out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result))


if __name__=="__main__":
    main(*map(Path,sys.argv[1:]))
