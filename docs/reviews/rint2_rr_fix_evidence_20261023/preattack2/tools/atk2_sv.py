"""Pre-attack round 2: C1 (end certificate <-> cut graph) on REAL producer-path records (no source edits).
Prints one JSON object: attack -> {expected, contract, flags@t, interval ...}."""
import copy, json, math, os, sys
SRC = os.environ['RINT_REVIEW_SOURCE']
sys.path.insert(0, os.path.join(SRC, 'scripts'))
import numpy as np  # noqa: F401
import carbon_junction as CJ
import step3_sigma as S3
import ca_ext_svcf as SV
import rint_r_chain as RC
import test_carbon_junction as T
T.CJ, T.S3 = CJ, S3

out = {}


def ev_of(run):
    reg, pl, r, c = run
    return T._qd3_ev(reg, pl, r, c)


def flags(p, t):
    return RC.sv_assess({('1', 'P1', 'R_j0'): {'sv_cf': SV.chain_view(p)}}, t, 'R_j0')[0]


def prob(e):
    try:
        return SV.sv_cf_problem(e, True)
    except Exception as ex:  # noqa: BLE001
        return f'EXC {type(ex).__name__}: {ex}'


def topo(cc):
    return tuple((cc or {}).get(k) for k in SV.CERT_TOPO_KEYS) if isinstance(cc, dict) else None


def reint(s):
    lo, hi = SV.cert_interval(s)
    s['ratio_cert_interval'] = [SV._enc(lo), SV._enc(hi)]
    return lo, hi


def summ(e):
    s = e['solve']['sv_counterfactual']
    up = s.get('upper') if isinstance(s.get('upper'), dict) else None
    v = SV.chain_view(s)
    return {'nu': s.get('n_unsplit_bridging_components'), 'status': (s.get('status'), s.get('status_hi')),
            'c': s.get('n_sv_faces_cut'), 'k': s.get('n_reach_pairs_cut'),
            'up': None if up is None else {kk: up.get(kk) for kk in ('status', 'n_edges_cut', 'n_plate_couplings_cut', 'n_sv_faces_cut',
                                                                      'n_reach_pairs_cut')},
            'M': topo(s.get('conv_cert_full')), 'L': topo(s.get('conv_cert')), 'U': topo((up or {}).get('conv_cert')),
            'nominal': [v['ratio'], v['ratio_hi']], 'interval': [v['ratio_cert_lo'], v['ratio_cert_hi']]}


runs = {
    'SVX': lambda: T._qd3_svx(cert=True),
    'QD2-1': lambda: T._qd3_run([T.QD2_A1, T.QD2_B1], T.QD2_S1, T.QD2_N1),
    'QD2-2': lambda: T._qd3_run([T.QD2_A1, T.QD2_B1C], T.QD2_S1, T.QD2_N1),
    'QD2-3': lambda: T._qd3_run([T.QD2_A3, T.QD2_B3, T.QD2_C3], T.QD2_S3, T.QD2_N3),
    'QD4': lambda: T._qd3_run(T.QD4_POLYS, T.QD4_SDCP, T.QD4_N),
    'RAIL5': lambda: T._qd3_run(T.QD5_RAIL5, T.QD4_SDCP, T.QD5_RAIL5_N),
    'QDX': lambda: T._qd3_run(T.QDX_POLYS, T.QDX_SDCP, T.QDX_N),
    'QD11R': lambda: T._qd3_run(T.QD11R_POLYS, T.QD2_S11, T.QD11R_N),
    'FLOAT': lambda: T._qd3_run(T.QD7_FL_POLYS, T.QD7_FL_SDCP, T.QD7_FL_N),
    'PARc1': lambda: T._qd3_run(T.QD7_PAR_POLYS, T.QD7_PAR_SDCP, T.QD7_PAR_N, sdcp_mod={'c': 1.0}),
    'PARc0': lambda: T._qd3_run(T.QD7_PAR_POLYS, T.QD7_PAR_SDCP, T.QD7_PAR_N),
    'UFLOAT': lambda: T._qd3_run(T.QD7_UFL_POLYS, T.QD7_UFL_SDCP, T.QD7_UFL_N),
    'UPLATE': lambda: T._qd3_run(T.QD7_UPL_POLYS, T.QD7_UPL_SDCP, T.QD7_UPL_N),
}
EV = {}
for nm, mk in runs.items():
    e = ev_of(mk())
    EV[nm] = json.loads(json.dumps(e))
    out[f'B0 base {nm}'] = dict(summ(EV[nm]), contract=prob(EV[nm]))


def cp(nm):
    return json.loads(json.dumps(EV[nm]))


# ---- X1: A2 (round-1 edit set, NO count edits) on every computed-lower record: lower <- main cert, G_cut = G_full, ratio 1
def swap_lower_main(e):
    s = e['solve']['sv_counterfactual']
    G = s['G_full_code']
    s['G_cut_code'] = G
    s['sv_counterfactual_ratio'] = G / G
    s['conv_cert'] = copy.deepcopy(s['conv_cert_full'])
    if s.get('upper') is None:
        s['sv_counterfactual_ratio_hi'] = G / G
    reint(s)
    return e


for nm in EV:
    if EV[nm]['solve']['sv_counterfactual'].get('status') != 'computed':
        continue
    e = swap_lower_main(cp(nm))
    s = e['solve']['sv_counterfactual']
    base_iv = summ(EV[nm])['interval']
    t_mid = None
    if isinstance(base_iv[0], float) and base_iv[0] > 1.0 + 1e-9:
        t_mid = 0.5 * (1.0 + base_iv[0])
    out[f'X1 A2 (no count edit) lower<-main [{nm}]'] = {
        'expected': 'reject (end cert certifies main graph) unless honestly same graph & same G',
        'contract': prob(e), 'base_interval': base_iv, 'new_interval': summ(e)['interval'],
        't_between_1_and_base_lo': t_mid,
        'flags_base@t': None if t_mid is None else flags(EV[nm]['solve']['sv_counterfactual'], t_mid),
        'flags_attack@t': None if t_mid is None else flags(s, t_mid)}


# ---- X2: upper <- main cert with NO count edits (records with an upper computed end)
def swap_upper_main(e):
    s = e['solve']['sv_counterfactual']
    G = s['G_full_code']
    up = s['upper']
    up['G_cut_code'] = G
    up['sv_counterfactual_ratio'] = G / G
    up['conv_cert'] = copy.deepcopy(s['conv_cert_full'])
    s['sv_counterfactual_ratio_hi'] = G / G
    reint(s)
    return e


for nm in EV:
    up = EV[nm]['solve']['sv_counterfactual'].get('upper')
    if not (isinstance(up, dict) and up.get('status') == 'computed'):
        continue
    e = swap_upper_main(cp(nm))
    out[f'X2 upper<-main (no count edit) [{nm}]'] = {'contract': prob(e), 'base': summ(EV[nm])['interval'], 'new': summ(e)['interval']}


# ---- X3: lower <- upper cert (lower end certifies the upper graph) — not in the known list (known = upper <- lower)
def swap_lower_upper(e):
    s = e['solve']['sv_counterfactual']
    up = s['upper']
    s['G_cut_code'] = up['G_cut_code']
    s['sv_counterfactual_ratio'] = up['sv_counterfactual_ratio']
    s['conv_cert'] = copy.deepcopy(up['conv_cert'])
    thr = e['sv_counterfactual_request']['threshold']
    reint(s)
    return e


for nm in EV:
    up = EV[nm]['solve']['sv_counterfactual'].get('upper')
    if not (isinstance(up, dict) and up.get('status') == 'computed' and EV[nm]['solve']['sv_counterfactual'].get('status') == 'computed'):
        continue
    e = swap_lower_upper(cp(nm))
    out[f'X3 lower<-upper cert (no count edit) [{nm}]'] = {
        'expected': 'reject (lower end cert certifies the upper graph)', 'contract': prob(e),
        'base': summ(EV[nm])['interval'], 'new': summ(e)['interval'], 'k_ku_ne_npc': (EV[nm]['solve']['sv_counterfactual'].get('n_reach_pairs_cut'),
                                                                                         up.get('n_reach_pairs_cut'), up.get('n_edges_cut'),
                                                                                         up.get('n_plate_couplings_cut'))}


# ---- X4: new-field form attacks (lower / upper) on computed records — must be rejected (own sentence)
BADS = {'True': True, 'False': False, '-1': -1, '1.0': 1.0, '"1"': '1', 'None': None, '2**63': 2 ** 63, 'NaN': float('nan'),
        'inf': float('inf'), '[1]': [1], '"0"': '0', '0.0': 0.0}


def setk(e, where, v, delete=False):
    s = e['solve']['sv_counterfactual']
    tgt = s if where == 'lower' else s['upper']
    if delete:
        tgt.pop('n_reach_pairs_cut', None)
    else:
        tgt['n_reach_pairs_cut'] = v
    return e


for nm in ('QD2-3', 'QDX', 'SVX'):
    res = {}
    for where in ('lower', 'upper'):
        if where == 'upper' and not isinstance(EV[nm]['solve']['sv_counterfactual'].get('upper'), dict):
            continue
        for bn, bv in BADS.items():
            res[f'{where} {bn}'] = prob(setk(cp(nm), where, bv))
        res[f'{where} <missing>'] = prob(setk(cp(nm), where, None, delete=True))
    out[f'X4 form attacks [{nm}]'] = {k: (v[:110] if isinstance(v, str) else v) for k, v in res.items()}

# ---- X5: form/relation attacks on records WITHOUT a computed end (both inf / upper inf)
res = {}
for bn, bv in BADS.items():
    res[f'QD2-2 (inf/inf) lower {bn}'] = prob(setk(cp('QD2-2'), 'lower', bv))
    res[f'QD2-2 (inf/inf) upper? {bn}'] = None
res['QD2-2 lower <missing>'] = prob(setk(cp('QD2-2'), 'lower', None, delete=True))
res['QD2-2 lower 10**6 (> n_sv_faces_cut)'] = prob(setk(cp('QD2-2'), 'lower', 10 ** 6))
for nm in ('QD4', 'QD2-1'):
    s0 = EV[nm]['solve']['sv_counterfactual']
    up0 = s0.get('upper') or {}
    res[f'{nm} base (k, ku, ne)'] = (s0.get('n_reach_pairs_cut'), up0.get('n_reach_pairs_cut'), up0.get('n_edges_cut'))
    e = cp(nm)
    e['solve']['sv_counterfactual']['upper']['n_reach_pairs_cut'] = 0   # violate ku >= k if k > 0, or ku <= k + ne
    res[f'{nm} upper(+inf) ku := 0'] = prob(e)
    e = cp(nm)
    e['solve']['sv_counterfactual']['upper']['n_reach_pairs_cut'] = 10 ** 6
    res[f'{nm} upper(+inf) ku := 10**6 (> k + ne)'] = prob(e)
    e = cp(nm)
    e['solve']['sv_counterfactual']['n_reach_pairs_cut'] = 10 ** 6
    res[f'{nm} lower k := 10**6 (> n_sv_faces_cut)'] = prob(e)
out['X5 relation/form on records with no computed end or +inf upper'] = res

# ---- X6: nu -> 0 consistent edit (record + evidence census): drop the upper end, hi := lower-end bound
res = {}
for nm in ('QD2-3', 'QDX', 'RAIL5', 'QD2-1', 'QD4'):
    e = cp(nm)
    s = e['solve']['sv_counterfactual']
    s['n_unsplit_bridging_components'] = 0
    e['census']['n_unsplit_bridging_components'] = 0
    s['upper'] = None
    s['status_hi'] = s['status']
    s['sv_counterfactual_ratio_hi'] = s['sv_counterfactual_ratio']
    s['ratio_limit_hi'] = s['ratio_limit']
    lo, hi = reint(s)
    base_iv = summ(EV[nm])['interval']
    t = None
    if isinstance(hi, float) and isinstance(base_iv[1], float) and base_iv[1] > hi:
        t = 0.5 * (hi + base_iv[1])
    elif isinstance(hi, float) and base_iv[1] == math.inf:
        t = hi * 1.5
    res[nm] = {'contract': prob(e), 'base_interval': base_iv, 'new_interval': [lo, hi], 't': t,
               'flags_base@t': None if t is None else flags(EV[nm]['solve']['sv_counterfactual'], t),
               'flags_attack@t': None if t is None else flags(s, t)}
out['X6 nu->0 (record + census) drops upper end'] = res

# ---- X7: remove upper n_sv_faces_cut (allowed 'if present'), then lower c := 0 with lower <- main (a) on QDX: does ⑦ still bind?
e = cp('QDX')
s = e['solve']['sv_counterfactual']
s['upper'].pop('n_sv_faces_cut', None)
swap_lower_main(e)
s['n_sv_faces_cut'] = 0
s['n_reach_pairs_cut'] = 0
out['X7 QDX upper n_sv_faces_cut deleted + (a) lower<-main c=k=0'] = {'contract': prob(e), 'interval': summ(e)['interval']}

print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
