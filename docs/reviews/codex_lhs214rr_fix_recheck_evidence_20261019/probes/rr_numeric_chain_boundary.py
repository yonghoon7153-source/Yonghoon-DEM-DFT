"""Diagnose the submitted boundary fixture's platform sensitivity without editing it.

Select nearby box_y inputs from the measured solver current, then re-run the real
producer. E_Q and all five submitted section-E assertions remain unchanged.
"""
from pathlib import Path
import contextlib
import io
import json
import math
import os
import platform
import sys

ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT.parent
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
os.environ['TMP']=os.environ['TEMP']=str(ROOT/'tmp')
sys.path[:0]=[str(ROOT/'source/scripts'),str(ROOT/'source/webapp'),str(WORK/'lhs_coverage_review_20260930/deps'),str(WORK/'gen2_network_reverify3_20261007/deps')]
import network_conductivity as nc
import tau_flux as tf
import test_l214r_r01_restored_full as submitted
from test_lhs214_model_limit import chain_bed
import numpy
import scipy

def quiet(fn,*a,**kw):
    with contextlib.redirect_stdout(io.StringIO()):return fn(*a,**kw)

search=[]
for area_offset in range(33):
    area=submitted.E_AREA+area_offset*1e-12
    A,C,plate,_=chain_bed(1.,area=area)
    base=quiet(nc._run_all_networks,A,C,[1],[],{1:'SE'},1,plate,submitted.E_BX,submitted.E_BY['eq'],None,contact_mode='hertzian')
    cert=base['solve_certificate_full']
    ib=cert['I_bottom']
    if area_offset==0:original_ib=ib
    bx_candidates=[submitted.E_BX,math.nextafter(submitted.E_BX,math.inf),math.nextafter(submitted.E_BX,0.)]
    chosen={}
    for bx in bx_candidates:
        center=(ib*plate)/(bx*1.5)
        candidates=[center]
        up=down=center
        for _ in range(32):
            up=math.nextafter(up,math.inf);down=math.nextafter(down,0.)
            candidates.extend((up,down))
        chosen={}
        for k,q in submitted.E_Q.items():
            for by in candidates:
                if (ib/1.)*plate/(bx*by*1**2)==q:
                    chosen[k]=by;break
        if len(chosen)==3:break
    search.append(dict(area=area,I_bottom=ib,found=list(chosen)))
    if len(chosen)==3:break
assert len(chosen)==3,chosen
out=dict(python=sys.version,platform=platform.platform(),numpy=numpy.__version__,scipy=scipy.__version__,
         source_area=submitted.E_AREA,source_box_x=submitted.E_BX,source_box_y=dict(submitted.E_BY),measured_original_I_bottom=original_ib,
         measured_original_eq_q=original_ib*plate/(submitted.E_BX*submitted.E_BY['eq']),
         nearest_search_center=center,calibrated_area=area,calibrated_I_bottom=ib,calibrated_box_x=bx,calibrated_box_y=chosen,
         expected_q=submitted.E_Q,search=search,cases={})
for label,by in chosen.items():
    du=quiet(lambda:{cm:nc._run_all_networks(A,C,[1],[],{1:'SE'},1,plate,bx,by,None,contact_mode=cm) for cm in ('hertzian','physics')})
    du=json.loads(json.dumps(du));r=du['hertzian'];c=r['solve_certificate_full']
    T,Ar,_=nc._geometry_TA(c['geometry']);raw=(c['I_bottom']/c['delta_V'])*T/Ar
    ledger=dict(thickness_um=plate,thickness_mass_conserving_um=plate,phi_se_mass_conserving=sum(4/3*math.pi*a['radius']**3 for a in A.values())/(bx*by*plate))
    row=tf.ion_columns(du,ledger,100.)
    out['cases'][label]=dict(raw_q=raw,saved_q=r['sigma_full'],status=r['sigma_full_status'],reason=r['sigma_full_reason'],
                             binding=tf.certificate_binding_problems('hertz',r),tau_status=row['ion_net_status_hertz'],
                             certificate=c)
    assert raw==submitted.E_Q[label],(label,raw)
# A derived run; original test was already recorded failing and is not relabelled.
submitted.E_BY=dict(chosen)
submitted.E_BX=bx
submitted.E_AREA=area
log=io.StringIO()
with contextlib.redirect_stdout(log):submitted.sec_E({})
out['derived_E_assertions']={'passed':submitted._ok,'failed':submitted._fail}
(ROOT/'evidence/rr_numeric_chain_boundary.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
(ROOT/'evidence/rr_numeric_chain_boundary.log').write_text(log.getvalue(),encoding='utf8')
print(json.dumps({k:out[k] for k in ('source_area','source_box_x','source_box_y','measured_original_I_bottom','measured_original_eq_q','calibrated_area','calibrated_box_x','calibrated_box_y','expected_q','derived_E_assertions')},ensure_ascii=False))
sys.exit(bool(submitted._fail))
