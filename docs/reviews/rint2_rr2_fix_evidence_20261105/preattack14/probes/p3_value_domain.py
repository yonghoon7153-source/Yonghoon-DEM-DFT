"""P2-2 value-domain edges — arms_read_kind / arm_public_value_problem on a judged-complete arm (ct06_pub) + summary JSON path + recover CLI path."""
import copy, json, math
from pathlib import Path
from lib import RR, T, row

base = T.ct06_pub(0)
Z = dict(state='zero', err_rel=0.0, cert_pass=[None, None, None, None], cg_info=None, cg_resid=None, imbalance=None)
cases = [
    ('pid_bare_dash', dict(protocol_id='p3ca-'), 'producer = p3ca-<16 hex>'),
    ('pid_zwsp', dict(protocol_id='p3ca-​'), 'producer = p3ca-<16 hex>'),
    ('pid_space', dict(protocol_id='p3ca- '), 'producer = p3ca-<16 hex>'),
    ('pid_newline', dict(protocol_id='p3ca-0123456789abcdef\n'), 'producer = p3ca-<16 hex>'),
    ('sid_space', dict(sid_fp=' '), 'producer = 32 hex (_grid_fp)'),
    ('sid_nul', dict(sid_fp='\x00'), 'producer = 32 hex'),
    ('err_pos_half', dict(err_rel=0.5), 'positive ⓓ pass ⇒ err ≤ 1e-4'),
    ('err_pos_1e300', dict(err_rel=1e300), 'positive ⓓ pass ⇒ err ≤ 1e-4'),
    ('err_neg_zero', dict(err_rel=-0.0), 'trivial'),
    ('cgit_huge', dict(cg_iters=10 ** 30), 'producer may write (payload int)'),
    ('zero_cp_all_true', dict(Z, cert_pass=[True] * 4), 'declared (zero cert_pass not fixed)'),
    ('zero_cginfo_7', dict(Z, cg_info=7, cg_resid=-5.0), 'declared (zero cg_* not fixed)'),
    ('pos_resid_bigint', dict(cg_resid=10 ** 400), 'JSON int · conv_ok math.isfinite OverflowError?'),
    ('pos_resid_negbigint', dict(cg_resid=-(10 ** 400)), 'JSON int'),
    ('pos_cginfo_bigint', dict(cg_info=10 ** 400), 'cg_info != 0 -> unconv'),
    ('index_true', dict(index=True), 'bool index'),
    ('state_ws', dict(state='positive '), 'ws'),
]
print('honest base:', RR.arms_read_kind([base], T.rr3_prior([base])))
for nm, kw, note in cases:
    a = dict(base, **kw)
    rec = T.rr3_prior([a])
    try:
        k = RR.arms_read_kind(rec['arms_read'], rec)
    except Exception as e:      # noqa: BLE001
        k = ('EXC', f'{type(e).__name__}: {str(e)[:80]}')
    print(f'  {nm:22s} {str(k)[:120]:122s} [{note}]')

# JSON path: 1e400 literal parses to inf through _json_strict (parse_constant only sees NaN/Infinity tokens)
print('\n_json_strict(1e400) ->', RR._json_strict(b'{"x": 1e400}'))

# result_fields / summary path with a forged prior run whose arms_read has cg_resid 10**400 (positive) — honest file_ids + pads
folder = T.rr3_folder('PA14_big')
a = dict(base, cg_resid=10 ** 400)
s = T.rr3_summ('TIME_LIMIT', T.RR3_L2, [T.rr3_prior([a])])
print('\nresult_fields with cg_resid=10**400:', row(folder, s))
# written + read back through the real summary reader (strict JSON) → recount
(folder / 'ladder_summary.json').write_bytes(RR.canon_bytes(s))
try:
    print('result_recount:', RR.result_recount(folder))
except Exception as e:      # noqa: BLE001
    print('result_recount EXC', type(e).__name__, str(e)[:100])

# recover --ledger CLI path (real git ledger · rc_recover_resume) — does recover crash (traceback) or count bad?
name = T.ct06_pub(0)['file']
ar = [dict(T.ct06_pub(0), cg_resid=10 ** 400)]
try:
    out = T.rc_recover_resume('PA14_big_cli', T.CHAIN_OK0, T.LG_PLAIN, prep=T.rr3_cli_prep(ar, {name: T.RR3_PAYLOAD}))
    print('recover cli:', str(out)[:300])
except Exception as e:      # noqa: BLE001
    print('recover cli EXC', type(e).__name__, str(e)[:160])
