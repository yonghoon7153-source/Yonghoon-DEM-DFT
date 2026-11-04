"""P8-02 — PC7-04 class outside recover_group: an end record copied from another run (token/name differ from the launch record) but
*confirmed True*.  stage_recover never sends it to recover_group (todo = missing or unconfirmed end records only), so the PC7-04 token/name
check never runs; attempt_groups_problem / orphan_cause / ResumeRunner._src_done read the end record without comparing it to the launch.

Real path: ladder attempt, chain parent SIGKILL after the mark (runner group alive · PE01 shape) -> copy groups/L01_floor.end.json from
another completed attempt (partial copy = PC7-04's own precondition) -> --stage recover --out <attempt> --ledger <ledger>.
Control: same copied end record with confirmed False -> PC7-04 guard refuses (rc 3, no result line).

  python3 -I probe_p802_foreign_confirmed_end.py <tree>
"""
import json
import os
import shutil
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from probe_common import setup  # noqa: E402

RR, T = setup(sys.argv[1])


def donor():
    """a normal completed attempt somewhere else -> its groups/L01_floor.end.json (by chain · confirmed True · rc 0 · its own token)."""
    d, _rc, _so = T.led_new('P802_donor')
    _r, n, _s = T.led_add(d, 'ladder:P0')
    a = T.lad_att('P802_donor', T.world('P802_donor'), d, n)
    return a['out'] / 'groups' / 'L01_floor.end.json'


def scenario(tag, end_src, confirmed):
    d, _rc, _so = T.led_new(tag)
    _r, n1, _s = T.led_add(d, 'ladder:P0')
    b1 = Path(T.TD) / 'runs' / f'{tag}_b1'
    w = T.world(tag, dict(T.PW, faults=[{'do': 'msg_sleep_after_mark', 'msg': f'[p2] solving ({tag})', 's': 40.0, 'match': {'rj': 'inf'}}]))
    seen, f1, tok = T.pe_kill_after(tag, d, n1, b1, w, f'solving ({tag})')
    alive0 = T.gr_alive(tok) if tok else None
    end = json.loads(Path(end_src).read_text(encoding='utf-8'))
    end['confirmed'] = confirmed
    (f1 / 'groups' / 'L01_floor.end.json').write_text(json.dumps(end), encoding='utf-8')   # partial copy (another run's end record)
    launch = json.loads((f1 / 'groups' / 'L01_floor.launch.json').read_text(encoding='utf-8'))
    unit = {'attempt_groups_problem': RR.attempt_groups_problem(f1), 'orphan_cause': RR.orphan_cause(f1)}
    rc, so = T.call(['--stage', 'recover', '--out', str(f1), '--ledger', str(d)], w)
    alive1 = T.gr_alive(tok) if tok else None
    res = T.led_result(d, n1)
    out = {'seen_mark': seen, 'launch_token': launch.get('token'), 'end_token': end.get('token'), 'alive_before_recover': bool(alive0),
           'unit': unit, 'recover_rc': rc, 'result_line': ({k: res.get(k) for k in ('status', 'side', 'cause', 'resume_ok', 'by')} if isinstance(res, dict)
                                                           else res),
           'runner_group_alive_after_recover': bool(alive1), 'recover_tail': so.strip().splitlines()[-3:]}
    if isinstance(res, dict) and res.get('resume_ok'):
        rc_add, n2, so_add = T.led_add(d, 'ladder:P0', resume=n1)
        out['resume_add'] = (rc_add, n2)
    for pid in alive1 or []:                                    # clean up the orphan runner group (probe hygiene)
        try:
            os.kill(pid, 9)
        except OSError:
            pass
    return out


src = donor()
print('donor end record:', json.loads(src.read_text(encoding='utf-8')))
rows = {'control_unconfirmed': scenario('P802c', src, False), 'foreign_confirmed': scenario('P802f', src, True)}
print(json.dumps(rows, ensure_ascii=False, indent=1, default=str))
f = rows['foreign_confirmed']
print('\nHOLE' if (f['recover_rc'] == 0 and isinstance(f['result_line'], dict) and f['runner_group_alive_after_recover']) else '\nno hole',
      '— result line written while the runner group is alive:', f['runner_group_alive_after_recover'], '· result line', f['result_line'])
