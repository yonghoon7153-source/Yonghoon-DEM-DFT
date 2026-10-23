"""Round-2 C5: kind / rule / requested form attacks on a real certified record (SVX).  Prints JSON."""
import json, os, sys
SRC = os.environ['RINT_REVIEW_SOURCE']
sys.path.insert(0, os.path.join(SRC, 'scripts'))
import carbon_junction as CJ
import step3_sigma as S3
import ca_ext_svcf as SV
import test_carbon_junction as T
T.CJ, T.S3 = CJ, S3

base = json.loads(json.dumps(T._qd3_ev(*T._qd3_svx(cert=True))))


def prob(e):
    try:
        return SV.sv_cf_problem(e, True)
    except Exception as ex:  # noqa: BLE001
        return f'EXC {type(ex).__name__}: {ex}'


K, R = SV.SV_CF_KIND, SV.SV_CF_RULE
cases = {
    'kind old name counterfactual_cut_sv_faces': {'kind': 'counterfactual_cut_sv_faces'},
    'kind trailing space': {'kind': K + ' '},
    'kind upper-case': {'kind': K.upper()},
    'kind None': {'kind': None},
    'kind missing': '__del__kind',
    'kind fullwidth-ish (Cyrillic a)': {'kind': K.replace('a', 'а', 1)},
    'rule None': {'rule': None},
    'rule missing': '__del__rule',
    'rule trailing newline': {'rule': R + '\n'},
    'rule list': {'rule': [R]},
    'rule = kind': {'rule': K},
    'requested 1 (int)': {'requested': 1},
    'requested "true"': {'requested': 'true'},
    'producer constants equal verifier constants': None,
}
out = {}
for nm, upd in cases.items():
    if upd is None:
        out[nm] = [CJ.CJUNC_SV_CF_KIND == K, CJ.CJUNC_SV_CF_RULE == R]
        continue
    e = json.loads(json.dumps(base))
    s = e['solve']['sv_counterfactual']
    if isinstance(upd, str):
        s.pop(upd.split('__del__')[1], None)
    else:
        s.update(upd)
    w = prob(e)
    out[nm] = (w or 'None')[:140]
out['base'] = prob(base)
print(json.dumps(out, ensure_ascii=False, indent=1))
