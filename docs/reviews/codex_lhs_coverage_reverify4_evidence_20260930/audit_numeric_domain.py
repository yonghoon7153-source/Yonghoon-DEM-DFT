"""Document the finite/normal-intermediate precondition; deliberately outside LHS scale."""
import sys,json
from pathlib import Path
from decimal import Decimal as D,localcontext
E=Path(__file__).resolve().parent;C=E.parent/'candidate';W=E.parent.parent
sys.path[:0]=[str(C/'scripts'),str(W/'lhs_coverage_review_20260930/deps')]
import lhs_descriptor_harvest as h
PI=D('3.1415926535897932384626433832795028841971693993751058209749445923078164062862')
a=b=1e-100;d=1.9e-100
ap,dp=h.producer_area_binary64(a,b,d)
with localcontext() as ctx:
    ctx.prec=90
    aa,bb,dd=D(a),D(b),D(d);dl=aa+bb-dd
    ae=-PI/4*((dd-aa-bb)*(dd+aa-bb)*(dd-aa+bb)*(dd+aa+bb))/(dd*dd)
    vals=(dl,2*aa-dl,2*bb-dl,2*aa+2*bb-dl,dd)
    ee=h._producer_abs_error(*[(float(v),float(v)) for v in vals])
    r=dict(radii_sim=[a,b],distance_sim=d,producer_area_sim2=ap,exact_area_sim2=str(ae),E_sim2=ee,
        error_exceeds_E=abs(D(ap)-ae)>D(ee),limitation='Deliberately nonphysical LHS scale; underflow of intermediate product; not evidence of affected real beds')
(E/'numeric_domain_results.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
print(json.dumps(r,indent=2))
