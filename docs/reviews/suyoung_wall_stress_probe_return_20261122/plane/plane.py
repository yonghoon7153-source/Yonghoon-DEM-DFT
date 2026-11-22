"""Zero-timestep constant-stress transfer for an artificial horizontal slab.

The foreground mask is selected with a uniform downward velocity on all
positive-mass nodes at or below the plane. It is frozen for each probe.
This is a kernel/support diagnostic, not an elastic equilibrium calculation.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
import math
from pathlib import Path

import numpy as np


LO = Q(3,20)
WIDTH = Q(1,4)
THICKNESS = Q(1,20)
DY = Q(1,640)
MATERIAL_SHA = "6e8073230f14142f3f802e1fed316bea22610502a98292e2ef794a123ea7e5f4"
GAPS = (Q(0),DY,2*DY,4*DY,6*DY)


def get_stencil(path):
    if hashlib.sha256(path.read_bytes()).hexdigest()!=MATERIAL_SHA:
        raise ValueError("WRONG_FIXED_MATERIAL")
    spec=importlib.util.spec_from_file_location("native_synthetic_slab_stencil",path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.stencil


def analytic(grid,gap):
    """Evaluate 40 sum_(j >= 0) integral_(grid*gap + j)^1.5 r B2(r) dr exactly.

    With y above an aligned plane only the plane and first subplane row
    contribute. Full lateral integration has sum(w_x)=1. The upper slab
    surface is beyond the 1.5-cell support so there is no upper term.
    """
    if gap < 0 or grid*THICKNESS < Q(3,2) or (LO*grid).denominator != 1:
        raise ValueError("SLAB_DOMAIN")
    def A(x): return Q(3,8)*x**2-x**4/4
    def B(x): return Q(9,16)*x**2-x**3/2+x**4/8
    def tail(z):
        half=Q(1,2); upper=Q(3,2)
        if z>=upper: return Q(0)
        if z>=half: return B(upper)-B(z)
        return A(half)-A(z) + B(upper)-B(half)
    return 40*(tail(grid*gap)+tail(grid*gap+1))


def sample_points(gap):
    """Eight lateral columns; two-point Gauss volume quadrature in each fixed layer."""
    count=int(THICKNESS/DY)
    # At the stated gaps all spline breaks lie on layer boundaries for both grids.
    x=.375+(np.arange(8)+.5)*(float(WIDTH)/8)
    centers=float(LO+gap)+(np.arange(count)+.5)*float(DY)
    radius=float(DY)/(2*math.sqrt(3))
    y=np.sort(np.r_[centers-radius,centers+radius])
    points=np.stack(np.meshgrid(x,y,indexing="ij"),axis=-1).reshape(-1,2)
    volume=np.full(len(points),float(WIDTH/8*DY/2))
    return points,volume


def transfer(stencil,cloud,grid):
    x,volume=cloud
    node,w,_,offset=stencil(x,grid)
    mass=np.bincount(node.ravel(),weights=(volume[:,None]*w).ravel(),minlength=(grid+1)**2)
    # Only for deciding the wall mask, a prescribed velocity of -1 everywhere gives v_y<0.
    y=(np.arange(len(mass))%(grid+1))/grid
    mask=(mass>0)&(y<=float(LO))
    eligible=mask[node]
    projected=(40*grid**2/float(WIDTH))*w*volume[:,None]
    # Compressive tau_yy=-1, symmetric positive unit shear tau_yx=1.
    normal=np.where(eligible,projected*(-offset[:,:,1]),0.)
    shear=np.where(eligible,projected*offset[:,:,0],0.)
    return dict(vertical_MPa=math.fsum(normal.ravel()),shear_MPa=math.fsum(shear.ravel()),
                selected_nodes=int(mask.sum()))


def run(path):
    stencil=get_stencil(path)
    rows=[]
    for gap in GAPS:
        cloud=sample_points(gap)
        values={}
        for grid in (80,160):
            answer=transfer(stencil,cloud,grid)
            expected=analytic(grid,gap)
            if abs(answer["vertical_MPa"]-float(expected))>1e-12 or abs(answer["shear_MPa"])>1e-12:
                raise ValueError("NATIVE_VERSUS_EXACT")
            values[grid]=dict(**answer,expected_fraction=str(expected))
        rows.append(dict(gap_box_units=str(gap),points=len(cloud[0]),grids=values,
                         coarse_minus_fine_MPa=values[80]["vertical_MPa"]-values[160]["vertical_MPa"]))
    return dict(label="SYNTHETIC_PLANAR_SUPPORT_ONLY",material_sha256=MATERIAL_SHA,
                wall=float(LO),slab_width=float(WIDTH),slab_thickness=float(THICKNESS),
                field_count=1,model_stress_to_MPa=10,model_steps=0,reference="exact_piecewise_cubic_integral",
                u6_qualification="HOLD",rows=rows)


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--material",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    result=run(args.material)
    with args.out.open("x",encoding="utf-8",newline="\n") as out:
        json.dump(result,out,indent=2,allow_nan=False)
        out.write("\n")
