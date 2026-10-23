"""Round-2: nu -> 0 edit (drop the upper end) with / without the evidence census edit, fixed thresholds.  Prints JSON."""
import json, os, sys
SRC = os.environ['RINT_REVIEW_SOURCE']
sys.path.insert(0, os.path.join(SRC, 'scripts'))
import carbon_junction as CJ
import step3_sigma as S3
import ca_ext_svcf as SV
import rint_r_chain as RC
import test_carbon_junction as T
T.CJ, T.S3 = CJ, S3


def flags(p, t):
    return RC.sv_assess({('1', 'P1', 'R_j0'): {'sv_cf': SV.chain_view(p)}}, t, 'R_j0')[0]


def prob(e):
    try:
        return SV.sv_cf_problem(e, True)
    except Exception as ex:  # noqa: BLE001
        return f'EXC {type(ex).__name__}: {ex}'


runs = {'QD2-3': lambda: T._qd3_run([T.QD2_A3, T.QD2_B3, T.QD2_C3], T.QD2_S3, T.QD2_N3),
        'QDX': lambda: T._qd3_run(T.QDX_POLYS, T.QDX_SDCP, T.QDX_N),
        'RAIL5': lambda: T._qd3_run(T.QD5_RAIL5, T.QD4_SDCP, T.QD5_RAIL5_N),
        'QD2-1': lambda: T._qd3_run([T.QD2_A1, T.QD2_B1], T.QD2_S1, T.QD2_N1),
        'QD4': lambda: T._qd3_run(T.QD4_POLYS, T.QD4_SDCP, T.QD4_N)}
out = {}
for nm, mk in runs.items():
    base = json.loads(json.dumps(T._qd3_ev(*mk())))
    for census_too in (False, True):
        e = json.loads(json.dumps(base))
        s = e['solve']['sv_counterfactual']
        s['n_unsplit_bridging_components'] = 0
        if census_too:
            e['census']['n_unsplit_bridging_components'] = 0
        s['upper'] = None
        s['status_hi'], s['sv_counterfactual_ratio_hi'], s['ratio_limit_hi'] = s['status'], s['sv_counterfactual_ratio'], s['ratio_limit']
        lo, hi = SV.cert_interval(s)
        s['ratio_cert_interval'] = [SV._enc(lo), SV._enc(hi)]
        bv = SV.chain_view(base['solve']['sv_counterfactual'])
        t = 1.2 if nm != 'QDX' else 2.0
        out[f'{nm} census_edit={census_too}'] = {'contract': (prob(e) or 'None')[:160], 'base_iv': [bv['ratio_cert_lo'], bv['ratio_cert_hi']],
                                                 'new_iv': [lo, hi], 't': t, 'flags_base': flags(base['solve']['sv_counterfactual'], t),
                                                 'flags_attack': flags(s, t)}
print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
