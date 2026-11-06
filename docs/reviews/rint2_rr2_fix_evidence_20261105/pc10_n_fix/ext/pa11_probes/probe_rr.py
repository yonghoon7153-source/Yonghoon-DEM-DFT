"""Pre-attack 11 probe (scratch only) — real CLI path (recover --ledger -> result line -> --add --resume) on a given tree.

usage: python3 -I probe_rr.py <tree> <out.json>
Each row = one hand-made attempt folder (git ledger entry 1, dead chain parent, post-result marker, one group record + log) whose
ladder_summary.json is replaced by `prep`.  Reports orphan_cause, result line (cause/resume_ok) and the resume rc.
"""
import sys, json, tempfile, shutil, io, contextlib, hashlib
from pathlib import Path

tree, outp = sys.argv[1], sys.argv[2]
sys.path.insert(0, tree + '/scripts')
import test_rint_r_chain as T          # noqa: E402
import rint_r_chain as RR              # noqa: E402
T.RR = RR
T.TD = tempfile.mkdtemp(prefix='pa11_rr_')

TB = T.RC02_LOG                          # Traceback KeyError (no resource words)
PLAIN = '[p2] run\n'
OOM = '[p2] run\n' + T.LG_OOM


def summ(code, runs, run='L01_floor'):
    def prep(f):
        s = {'tool': RR.TOOL, 'schema': RR.SCHEMA, 'stage': 'ladder', 'status': 'STOPPED', 'stop': {'code': code, 'run': run, 'reason': None},
             'runs': runs}
        RR.write_summary(Path(f) / 'ladder_summary.json', s)
    return prep


def rec(name='L01_floor', **kw):
    return dict({'name': name, 'outdir': f'{name}_arm1'}, **kw)


def extra_run(prev_name, log, end=None):
    """second (earlier) run: group records + log in the attempt folder."""
    def prep(f):
        T.pc_group(f, prev_name, end or {'cause': None, 'rc': 0}, log, t='2026-10-27T00:00:00Z')
    return prep


def both(*ps):
    def prep(f):
        for p in ps:
            p(f)
    return prep


ARMS = [{'file': 'p2_SBE_vgcf100_a0.json', 'index': 0, 'sha256': 'a' * 64}]
ROWS = [
    #  ── S1 check stop (runner rc 0, chain-side read_run Stop) — single field edit stop.code -> GROUP_UNCONFIRMED
    ('S1_honest_check_GENERATION', {'by': 'chain', 'confirmed': True, 'cause': None, 'rc': 0}, PLAIN,
     summ('GENERATION', [rec(group_cause=None, rc=0, arms_read=ARMS, seconds=1.0)])),
    ('S1_forged_code_GU', {'by': 'chain', 'confirmed': True, 'cause': None, 'rc': 0}, PLAIN,
     summ('GROUP_UNCONFIRMED', [rec(group_cause=None, rc=0, arms_read=ARMS, seconds=1.0)])),
    ('S1_forged_code_GU_noarms', {'by': 'chain', 'confirmed': True, 'cause': None, 'rc': 0}, PLAIN,
     summ('GROUP_UNCONFIRMED', [rec(group_cause=None, rc=0, arms_read=[], seconds=1.0)])),
    #  ── S2 GU run record rc 1 -> 0 (single field) — end record says rc 1, Traceback log
    ('S2_honest_GU_rc1', {'by': 'chain', 'confirmed': True, 'cause': None, 'rc': 1}, TB,
     summ('GROUP_UNCONFIRMED', [rec(group_cause=None, rc=1)])),
    ('S2_forged_GU_rc0', {'by': 'chain', 'confirmed': True, 'cause': None, 'rc': 1}, TB,
     summ('GROUP_UNCONFIRMED', [rec(group_cause=None, rc=0)])),
    ('S2_honest_RUNNER_RC_rc1', {'by': 'chain', 'confirmed': True, 'cause': None, 'rc': 1}, TB,
     summ('RUNNER_RC', [rec(group_cause=None, rc=1)])),
    #  ── S3 duplicate run records (never written) — last one wins
    ('S3_dup_last_signal', {'by': 'chain', 'confirmed': True, 'cause': None, 'rc': 1}, TB,
     summ('RUNNER_RC', [rec(group_cause=None, rc=1), rec(group_cause='signal', rc=None)])),
    #  ── S4 GU stop.run -> earlier completed run (single field)
    ('S4_honest_GU_L01_rc1', {'by': 'chain', 'confirmed': True, 'cause': None, 'rc': 1}, TB,
     both(extra_run('L00_prev', PLAIN), summ('GROUP_UNCONFIRMED', [rec('L00_prev', group_cause=None, rc=0), rec(group_cause=None, rc=1)]))),
    ('S4_forged_GU_run_L00', {'by': 'chain', 'confirmed': True, 'cause': None, 'rc': 1}, TB,
     both(extra_run('L00_prev', PLAIN), summ('GROUP_UNCONFIRMED', [rec('L00_prev', group_cause=None, rc=0), rec(group_cause=None, rc=1)],
                                             run='L00_prev'))),
    #  ── S5 never-written extra fields on a killed:timeout record
    ('S5_TL_timeout_with_arms_copied', {'by': 'chain', 'confirmed': True, 'cause': 'timeout', 'rc': -9}, PLAIN,
     summ('TIME_LIMIT', [rec(group_cause='timeout', rc=None, arms_read=ARMS, copied_from=7, seconds=None)])),
    #  ── S6 rc key missing (documented limitation)
    ('S6_TL_timeout_no_rc_key', {'by': 'chain', 'confirmed': True, 'cause': 'timeout', 'rc': -9}, PLAIN,
     summ('TIME_LIMIT', [rec(group_cause='timeout')])),
    #  ── S7 orphan path: on-disk cause signal_after (never written by any producer since C2b)
    ('S7_orphan_honest_none_rc1', {'by': 'chain', 'confirmed': True, 'cause': None, 'rc': 1}, TB, None),
    ('S7_orphan_forged_signal_after_rc1', {'by': 'chain', 'confirmed': True, 'cause': 'signal_after', 'rc': 1}, TB, None),
    ('S7_orphan_forged_timeout_rc1', {'by': 'chain', 'confirmed': True, 'cause': 'timeout', 'rc': 1}, TB, None),
    #  ── S8 N1 / N2 sanity (CT04 shape) + 'killed' with rc key absent but group_cause None
    ('S8_N1_TL_gcNone_rc1', {'by': 'chain', 'confirmed': True, 'cause': None, 'rc': 1}, TB, summ('TIME_LIMIT', [rec(group_cause=None, rc=1)])),
    ('S8_N2_RR_timeout_rc1', {'by': 'chain', 'confirmed': True, 'cause': None, 'rc': 1}, TB, summ('RUNNER_RC', [rec(group_cause='timeout', rc=1)])),
    ('S8_N2_RR_signal_after_rc1', {'by': 'chain', 'confirmed': True, 'cause': None, 'rc': 1}, TB,
     summ('RUNNER_RC', [rec(group_cause='signal_after', rc=1)])),
    #  ── S9 TL + record {timeout,null} while the group end record says cause None rc 1 (3-field forgery = producer shape)
    ('S9_TL_timeout_null_vs_end_none_rc1', {'by': 'chain', 'confirmed': True, 'cause': None, 'rc': 1}, TB,
     summ('TIME_LIMIT', [rec(group_cause='timeout', rc=None)])),
]

out = {}
try:
    T.fixtures()
    for nm, end, log, prep in ROWS:
        try:
            r = T.rc_recover_resume(f'PA11_{nm}', end, log, prep=prep)
            out[nm] = {'orphan': r['orphan'], 'recover_rc': r['recover_rc'],
                       'result': {k: (r['result'] or {}).get(k) for k in ('status', 'cause', 'resume_ok')},
                       'resume_rc': r['resume_rc'], 'not_allowed': r['not_allowed']}
        except Exception as e:                                       # noqa: BLE001
            out[nm] = {'error': f'{type(e).__name__}: {e}'}
finally:
    shutil.rmtree(T.TD, ignore_errors=True)
Path(outp).write_text(json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')
for k, v in out.items():
    print(k, json.dumps(v, ensure_ascii=False))
