"""Scalar binary64 evaluation of the official add_pair expression; NOT a DEM run.

Source read 2026-09-30:
https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/master/src/compute_pair_gran_local.cpp
add_pair lines 509-531. No inference that this is the installed producer build.
"""
import sys, math, json
from pathlib import Path
E=Path(__file__).resolve().parent; C=E.parent/'candidate'; W=E.parent.parent
sys.path[:0]=[str(C/'scripts'),str(W/'lhs_coverage_review_20260930/deps')]
import numpy as np
import lhs_descriptor_harvest as h
import lens_geometry as lg
q=lambda x: float(format(x,'.6g'))
def emitted(radi,radj,dx):
    rsq=dx*dx+0.0*0.0+0.0*0.0
    r=math.sqrt(rsq)
    # Preserve C++ parenthesization and left-associative operations.
    a=-math.pi/4*((r-radi-radj)*(r+radi-radj)*(r-radi+radj)*(r+radi+radj))/rsq
    dl=radi+radj-r
    return a,dl
def case(a,b,d):
    raw,dl=emitted(a,b,d)
    ar,br,dlr,area=map(q,(a,b,dl,raw))
    lo,hi,lb,how=h._area_enclosure(np.array([ar]),np.array([br]),np.array([dlr]))
    diag=h.contact_area_check(np.array([1,2]),np.array(['AM','SE']),np.array([ar,br]),np.array([1]),np.array([2]),np.array([area]),np.array([dlr]),np.array([0]))
    return dict(radii_sim=[a,b],center_distance_sim=d,producer_expression_area=raw,producer_delta=dl,
        tokens=[ar,br,dlr,area],local_reconstruction=lg.intersection_disc_area(a,b,dl),
        cap_exact_equal_radius=math.pi*a*a if a==b else None,
        enclosure=dict(lo=float(lo[0]),hi=float(hi[0]),lb=bool(lb[0]),how=str(how[0])),
        diagnostic=diag)
R={}
for name, vals in {
    'normal':(.001,.001,.0019),
    'equal_deep_1e-12':(.001,.001,1e-15),
    'equal_deep_1e-13':(.001,.001,1e-16),
    'contained':(.002,.001,.0009),
    'no_contact':(.001,.001,.0021),
}.items(): R[name]=case(*vals)
(E/'producer_results.json').write_text(json.dumps(R,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:{**{a:b for a,b in v.items() if a!='diagnostic'},'diagnostic_all':v['diagnostic']['all']} for k,v in R.items()},ensure_ascii=False,indent=2))
