"""Pre-attack 11 probe 2 (scratch only) — summary nested-field types (N4 class on the summary path) and outdir redirect vs check trace.

usage: python3 -I probe_rr2.py <tree> <out.json>
"""
import sys, json, tempfile, shutil
from pathlib import Path

tree, outp = sys.argv[1], sys.argv[2]
sys.path.insert(0, tree + '/scripts')
import test_rint_r_chain as T          # noqa: E402
import rint_r_chain as RR              # noqa: E402
T.RR = RR
T.TD = tempfile.mkdtemp(prefix='pa11_rr2_')
TB = T.RC02_LOG
OOM = '[p2] run\n' + T.LG_OOM


def raw_summary(obj):
    def prep(f):
        (Path(f) / 'ladder_summary.json').write_text(json.dumps(obj), encoding='utf-8')
    return prep


def with_trace(prep):
    def p(f):
        u = Path(f) / 'L01_floor_arm1' / '.unchecked'
        u.mkdir(parents=True, exist_ok=True)
        (u / 'p2_SBE_vgcf100_a0.json').write_text('{}\n', encoding='utf-8')      # runner-side check-failure payload = check trace
        prep(f)
    return p


def S(stop, runs):
    return {'tool': RR.TOOL, 'schema': RR.SCHEMA, 'stage': 'ladder', 'status': 'STOPPED', 'stop': stop, 'runs': runs}


STOP = {'code': 'RUNNER_RC', 'run': 'L01_floor', 'reason': None}
END1 = {'by': 'chain', 'confirmed': True, 'cause': None, 'rc': 1}
ROWS = [
    ('N4s_runs_list_of_int', END1, TB, raw_summary(S(STOP, [1]))),
    ('N4s_runs_str', END1, TB, raw_summary(S(STOP, 'abc'))),
    ('N4s_stop_str', END1, TB, raw_summary(S('x', []))),
    ('N4s_stop_list', END1, TB, raw_summary(S([1], []))),
    ('N4s_outdir_dict', END1, TB, raw_summary(S(STOP, [{'name': 'L01_floor', 'outdir': {'a': 1}, 'group_cause': None, 'rc': 1}]))),
    ('N4s_outdir_int', END1, TB, raw_summary(S(STOP, [{'name': 'L01_floor', 'outdir': 5, 'group_cause': None, 'rc': 1}]))),
    ('N4s_runs_dict', END1, TB, raw_summary(S(STOP, {'name': 'L01_floor'}))),
    #  check trace guard: honest (outdir = producer name) vs single-field outdir edit (never written: outdir not prefixed by run name)
    ('TR_honest_oom_trace', END1, OOM, with_trace(raw_summary(S(STOP, [{'name': 'L01_floor', 'outdir': 'L01_floor_arm1', 'group_cause': None,
                                                                          'rc': 1}])))),
    ('TR_forged_outdir_oom_trace', END1, OOM, with_trace(raw_summary(S(STOP, [{'name': 'L01_floor', 'outdir': 'nowhere', 'group_cause': None,
                                                                                 'rc': 1}])))),
]

out = {}
try:
    T.fixtures()
    for nm, end, log, prep in ROWS:
        try:
            r = T.rc_recover_resume(f'PA11b_{nm}', end, log, prep=prep)
            out[nm] = {'orphan': r['orphan'], 'recover_rc': r['recover_rc'],
                       'result': {k: (r['result'] or {}).get(k) for k in ('status', 'cause', 'resume_ok')} if isinstance(r['result'], dict) else r['result'],
                       'resume_rc': r['resume_rc'], 'tail': r.get('tail')}
        except Exception as e:                                       # noqa: BLE001
            import traceback
            tb = traceback.format_exc().strip().splitlines()
            out[nm] = {'error': f'{type(e).__name__}: {e}', 'where': [x.strip() for x in tb[-6:]]}
finally:
    shutil.rmtree(T.TD, ignore_errors=True)
Path(outp).write_text(json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')
for k, v in out.items():
    print(k, json.dumps(v, ensure_ascii=False)[:400])
