"""Run the unchanged resident SM function with a complete transport scaffold.
The ZIP omits legacy cohort JSON; numerical records and the ca_ext consumer are untouched.
"""
import contextlib,io
with contextlib.redirect_stdout(io.StringIO()): import probe_actual as P
import test_ca_ext_b6 as B
B.RC=P.RC;B.CW=P.CW
mm=P.manifest(*P.T._qd3_svx()[:3])
Es=lambda x:x['ca_ext']['cjunc']['evidence']
Es(mm)['fp']=dict(B.CJ_FP)
Es(mm)['receipts']['electronic_main']['fp_registry']=B.CJ_FP['registry']
Es(mm)['census']={}
B._sv_put(mm,P.V.sv_cf_record(B._sv_raw()))
assert B.RC.ca_ext_record_ok(mm)==(True,None)
B.t_sv_mismatch(mm,P.V.sv_cf_record,Es)
print(f'RESIDENT_SM_DIRECT: {B._ok} PASS, {len(B._fail)} FAIL')
assert not B._fail
