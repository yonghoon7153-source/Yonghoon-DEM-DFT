"""M7 survivor effect: real certified records, threshold t = largest float <= exact upper quotient U."""
import json, math, os, sys
from fractions import Fraction as F
SRC = os.environ['RINT_REVIEW_SOURCE']
sys.path.insert(0, os.path.join(SRC, 'scripts'))
import carbon_junction as CJ
import step3_sigma as S3
import ca_ext_svcf as SV
import rint_r_chain as RC
import test_carbon_junction as T
T.CJ, T.S3 = CJ, S3
res = {'tree': SRC.rsplit('/', 1)[-1]}
for nm, mk in (('SVX nu=0', lambda: T._qd3_svx(cert=True)),
               ('QD2-3 nu=1 finite upper', lambda: T._qd3_run([T.QD2_A3, T.QD2_B3, T.QD2_C3], T.QD2_S3, T.QD2_N3))):
    reg, pl, r, c = mk()
    p = SV.sv_cf_record(c)
    full = p['conv_cert_full']
    up = p['upper'] if isinstance(p.get('upper'), dict) else p
    U = F(full['target_hi']) / F(up['conv_cert']['target_lo'])
    t = float(U)
    if F(t) > U:
        t = math.nextafter(t, -math.inf)
    v = SV.chain_view(p)
    f, d = RC.sv_assess({('1', 'P1', 'R_j0'): {'sv_cf': v}}, t, 'R_j0')
    res[nm] = {'exact_U_is_float': F(t) == U, 't (largest float <= U)': t, 'ratio_cert_hi': v['ratio_cert_hi'],
               'hi>=U': F(v['ratio_cert_hi']) >= U, 'flags@t': f}
print(json.dumps(res, indent=1))
