"""Pre-attack: SV certificate-interval judgment + record contract on the REAL producer path (no source edits).
Prints JSON lines: each attack = name, expected, actual."""
import contextlib, copy, io, json, math, os, sys
from fractions import Fraction as F
SRC = os.environ['RINT_REVIEW_SOURCE']
sys.path.insert(0, os.path.join(SRC, 'scripts'))
import numpy as np
import carbon_junction as CJ
import step3_sigma as S3
import ca_ext_svcf as SV
import rint_r_chain as RC
import run_contract as RCON
import test_carbon_junction as T
T.CJ, T.S3 = CJ, S3

out = {}


def ev_of(reg, pl, r, cf):
    return T._qd3_ev(reg, pl, r, cf)


def assess(view, thr):
    return RC.sv_assess({('1', 'P1', 'R_j0'): {'sv_cf': view}}, thr, 'R_j0')


def flags_of(rec_proj, thr):
    return assess(SV.chain_view(rec_proj), thr)[0]


def exact_interval(c, mc):
    """Independent exact recompute: lower = Gfull_lo/Gcut_lower_hi, upper = Gfull_hi/Gcut_upper_lo (Fractions)."""
    lo_c = c.get('conv_cert') or {}
    up = c.get('upper') if isinstance(c.get('upper'), dict) else None
    hi_c = (up or {}).get('conv_cert') if up is not None else lo_c
    fl, fh = F(mc['target_lo']), F(mc['target_hi'])
    lo = fl / F(lo_c['target_hi']) if lo_c.get('target_hi') else None
    hi = fh / F(hi_c['target_lo']) if (hi_c or {}).get('target_lo') else None
    return lo, hi


# ---------------------------------------------------------------- A1: real certified records accepted (liveness)
for nm, polys, sdcp, n in (('QD2-3 bracket (nu=1, finite upper)', [T.QD2_A3, T.QD2_B3, T.QD2_C3], T.QD2_S3, T.QD2_N3),
                           ('QD4 two comps (nu=2, inf upper)', T.QD4_POLYS, T.QD4_SDCP, T.QD4_N),
                           ('two comps + 5th rail (nu=2, finite upper)',
                            T.QD4_POLYS + [[(13.5, 1.5, 0.5), (13.5, 1.5, 8.5)]], T.QD4_SDCP, (15, 3, 9)),
                           ('QD2-1 reviewer (nu=1, inf upper)', [T.QD2_A1, T.QD2_B1], T.QD2_S1, T.QD2_N1),
                           ('QD2-2 (nu=0, inf lower)', [T.QD2_A1, T.QD2_B1C], T.QD2_S1, T.QD2_N1)):
    reg, pl, r, c = T._qd3_run(polys, sdcp, n)
    ev = ev_of(reg, pl, r, c)
    prob = SV.sv_cf_problem(ev, True)
    p = ev['solve']['sv_counterfactual']
    v = SV.chain_view(p)
    mc = (r or {}).get('conv_cert') or {}
    try:
        exlo, exhi = exact_interval(c, mc)
    except Exception as e:  # noqa
        exlo, exhi = f'{type(e).__name__}', None
    out['A1 ' + nm] = {'contract_problem': prob, 'standing': p.get('standing'), 'status': (p.get('status'), p.get('status_hi')),
                       'interval': [v.get('ratio_cert_lo'), v.get('ratio_cert_hi')],
                       'nominal': [v.get('ratio'), v.get('ratio_hi')],
                       'exact_lo<=got_lo': (None if not isinstance(exlo, F) or not isinstance(v.get('ratio_cert_lo'), float)
                                            else F(v['ratio_cert_lo']) <= exlo),
                       'got_hi>=exact_hi': (None if not isinstance(exhi, F) or not isinstance(v.get('ratio_cert_hi'), float)
                                            else F(v['ratio_cert_hi']) >= exhi)}

# ---------------------------------------------------------------- A2: same-run substitution (main cert as lower-end cert, nu=0)
reg, pl, r, c = T._qd3_svx(cert=True)
ev = ev_of(reg, pl, r, c)
base = json.loads(json.dumps(ev))
p0 = base['solve']['sv_counterfactual']
out['A2 base SVX'] = {'contract': SV.sv_cf_problem(base, True), 'flags@t=2': flags_of(p0, 2.0),
                      'interval': [SV.chain_view(p0)['ratio_cert_lo'], SV.chain_view(p0)['ratio_cert_hi']]}
sub = json.loads(json.dumps(base))
s = sub['solve']['sv_counterfactual']
G = s['G_full_code']
s['G_cut_code'] = G
s['sv_counterfactual_ratio'] = G / G
s['sv_counterfactual_ratio_hi'] = G / G
s['conv_cert'] = dict(s['conv_cert_full'])
lo2, hi2 = SV.cert_interval(s)
s['ratio_cert_interval'] = [SV._enc(lo2), SV._enc(hi2)]
out['A2 main-cert-as-lower-end (consistent edit; true ratio ~10.29)'] = {
    'expected': 'reject (end cert certifies the full system, not the cut system)',
    'contract': SV.sv_cf_problem(sub, True), 'interval': [lo2, hi2], 'flags@t=2': flags_of(s, 2.0)}

# ---------------------------------------------------------------- A3: threshold knife edges on a real certified record
v = SV.chain_view(p0)
lo, hi = v['ratio_cert_lo'], v['ratio_cert_hi']
out['A3 knife'] = {'t=lo (equal)': assess(v, lo)[0], 't=hi (equal)': assess(v, hi)[0],
                   't=nextafter(lo,-inf)': assess(v, math.nextafter(lo, -math.inf))[0],
                   't=nextafter(hi,+inf)': assess(v, math.nextafter(hi, math.inf))[0],
                   't between': assess(v, 0.5 * (lo + hi))[0]}

# ---------------------------------------------------------------- A4: record-field type/encoding attacks (contract must reject with own sentence)
def mut(fn):
    e = json.loads(json.dumps(base))
    fn(e, e['solve']['sv_counterfactual'])
    try:
        return SV.sv_cf_problem(e, True)
    except Exception as ex:  # noqa
        return f'EXC {type(ex).__name__}: {ex}'


muts = {
    'standing trailing space': lambda e, s: s.update(standing='certified_interval '),
    'standing fullwidth/homoglyph': lambda e, s: s.update(standing='certified_іnterval'),
    'n_unsplit True': lambda e, s: s.update(n_unsplit_bridging_components=True),
    'n_unsplit 0.0': lambda e, s: s.update(n_unsplit_bridging_components=0.0),
    'census n_unsplit True': lambda e, s: e['census'].update(n_unsplit_bridging_components=True),
    'I_bot_code True-ish (1.0 if G==1)': lambda e, s: e['solve'].update(I_bot_code=str(s['G_full_code'])),
    'conv_cert_full target_lo string': lambda e, s: s['conv_cert_full'].update(target_lo=str(s['conv_cert_full']['target_lo'])),
    'end cert target_hi < target_lo': lambda e, s: s['conv_cert'].update(target_lo=s['conv_cert']['target_hi'],
                                                                           target_hi=s['conv_cert']['target_lo']),
    'end cert pass_d 1 (int not bool)': lambda e, s: s['conv_cert'].update(pass_d=1),
    'end cert ok "true"': lambda e, s: s['conv_cert'].update(ok='true'),
    'end cert target_tol 1e-3': lambda e, s: s['conv_cert'].update(target_tol=1e-3),
    'main cert bind_version other': lambda e, s: s['conv_cert_full'].update(bind_version='cert-bind-v0'),
    'end cert fp_face_plan differs': lambda e, s: s['conv_cert'].update(fp_face_plan='a' * 32),
    'ratio_cert_interval list of strings': lambda e, s: s.update(ratio_cert_interval=[str(x) for x in s['ratio_cert_interval']]),
    'ratio_cert_interval ints': lambda e, s: s.update(ratio_cert_interval=[int(x) if isinstance(x, float) else x for x in s['ratio_cert_interval']]),
    'G_full_code -0.0': lambda e, s: s.update(G_full_code=-0.0),
    'kind other counterfactual': lambda e, s: s.update(kind='counterfactual_cut_sv_faces_all'),
    'rule field changed': lambda e, s: s.update(rule='some_other_rule'),
}
out['A4 field attacks'] = {k: mut(f) for k, f in muts.items()}

# ---------------------------------------------------------------- A5: real consumer path run_contract.ca_ext_record_ok via a manifest wrapper
# (the evidence is wrapped like the payload; we only reuse the cjunc evidence validator chain)
print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
