"""Pre-attack 11 probe 3 (scratch only) — rejected.json dropped into an attempt folder that already ran (post-result marker + stage summary)
before recover writes its result line: is it read as rejected / pre (skipped by adoption) and does --add then accept a fresh attempt?

usage: python3 -I probe_rej.py <tree> <out.json>
"""
import sys, json, tempfile, shutil
from pathlib import Path

tree, outp = sys.argv[1], sys.argv[2]
sys.path.insert(0, tree + '/scripts')
import test_rint_r_chain as T          # noqa: E402
import rint_r_chain as RR              # noqa: E402
T.RR = RR
T.TD = tempfile.mkdtemp(prefix='pa11_rej_')


def run(tag, rej_body):
    d, _rc, _so = T.led_new(tag)
    _r, n1, _s = T.led_add(d, 'ladder:P0')
    f = T.rc_att_folder(tag, d, n1, {'by': 'chain', 'cause': None, 'rc': 0, 'confirmed': True}, '[p2] run\n')
    s = {'tool': RR.TOOL, 'schema': RR.SCHEMA, 'stage': 'ladder', 'status': 'STOPPED', 'stop': {'code': 'GENERATION', 'run': 'L01_floor', 'reason': None},
         'runs': [{'name': 'L01_floor', 'outdir': 'L01_floor_arm1', 'group_cause': None, 'rc': 0, 'arms_read': []}]}
    RR.write_summary(f / 'ladder_summary.json', s)
    if rej_body is not None:
        (f / RR.REJECTED_FILE).write_bytes(rej_body)
    side = RR.folder_side(f)
    rc_rec, so_rec = T.call(['--stage', 'recover', '--out', str(f), '--ledger', str(d)])
    r1 = T.led_result(d, n1) or {}
    try:
        rec = RR.result_recount(f)
        recount = {k: rec.get(k) for k in ('status', 'side', 'cause', 'resume_ok')}
    except RR.Stop as e:
        recount = f'Stop {e.code}'
    rc_add, n2, so_add = T.led_add(d, 'ladder:P0')                 # fresh attempt (not a resume) for the same target
    st = RR.ledger_parse(T.led_raw(d))
    ad = RR.adoption(st, 'ladder:P0')
    return {'folder_side': side, 'recover_rc': rc_rec, 'result': {k: r1.get(k) for k in ('status', 'side', 'cause', 'resume_ok')},
            'recount': recount, 'add_fresh_rc': rc_add, 'add_fresh_n': n2, 'add_tail': so_add.strip().splitlines()[-1:] if so_add else None,
            'adoption': {k: ad.get(k) for k in ('adopted', 'chain', 'effective', 'problems')}}


out = {}
try:
    T.fixtures()
    out['honest_no_rejected'] = run('PA11r_honest', None)
    out['forged_rejected_empty_obj'] = run('PA11r_forged', b'{}\n')
    out['forged_rejected_full_keys'] = run('PA11r_forged2', json.dumps({'schema': 'rint-r-rejected-v1', 'n': 1, 'code': 'OUTDIR_NOT_EMPTY', 'cause': 'x',
                                                                         'ledger_commit': 'a' * 40, 'utc': '2026-11-06T00:00:00Z'}).encode())
finally:
    shutil.rmtree(T.TD, ignore_errors=True)
Path(outp).write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print(json.dumps(out, ensure_ascii=False, indent=1))
