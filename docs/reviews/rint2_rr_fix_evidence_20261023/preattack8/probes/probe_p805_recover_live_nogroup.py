"""P8-05 — recover closes an attempt whose chain is alive, in the window after the start record and before the first group launch record.

recover_group refuses a live chain (chain_parent_alive) but it is only reached through groups/*.launch.json.  Between attempt_open's start
record and the first runner launch (presolve checks · S0 report checks · bed re-hash) the attempt folder has attempt.json only, so
stage_recover has no group to look at and recover_ledger writes a result line (interrupted · pre) for a live attempt.  The start record now
holds base + host but no chain pid, so the new PC7-01 record does not help this check.

Driver = real chain in its own process; only attempt_presolve_problem is wrapped with a 20 s sleep (stands in for a slow presolve / bed hash).

  python3 -I probe_p805_recover_live_nogroup.py <tree>
"""
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from probe_common import setup  # noqa: E402

RR, T = setup(sys.argv[1])

DRV = r'''
import json, os, sys, time
from pathlib import Path
cfg = json.load(open(sys.argv[1], encoding='utf-8'))
sys.path.insert(0, cfg['scripts'])
import rint_r_chain as RR
RR.HERE = Path(cfg['here'])
os.environ.update(cfg['env'])
_orig = RR.attempt_presolve_problem
def slow(*a, **k):
    time.sleep(20.0)
    return _orig(*a, **k)
RR.attempt_presolve_problem = slow
sys.exit(RR.main(cfg['argv']))
'''

d, _rc, _so = T.led_new('P805')
_r, n1, _s = T.led_add(d, 'ladder:P0')
b1 = Path(T.TD) / 'runs' / 'P805_b1'
w = T.world('P805')
pr = T.gr_spawn_chain('P805', T.ladder_argv(b1) + ['--ledger', str(d), '--attempt', str(n1)], w, driver=DRV, dname='p805_driver.py')
t_end = time.time() + 60
while time.time() < t_end and not any(x.get('kind') == 'start' for x in T.led_lines(d)):
    time.sleep(0.1)
f1 = b1 / f'attempt_{n1}'
alive_at_recover = pr.poll() is None
groups_at_recover = sorted(p.name for p in (f1 / 'groups').glob('*')) if (f1 / 'groups').is_dir() else []
rc_r, so_r = T.call(['--stage', 'recover', '--out', str(f1), '--ledger', str(d)], w)
res_after_recover = T.led_result(d, n1)
rc_chain = pr.wait(timeout=600)
log = (Path(T.TD) / 'P805_chain.log').read_text(encoding='utf-8', errors='replace')
summ = T.u_json(f1 / 'ladder_summary.json')
out = {'chain_alive_when_recover_ran': alive_at_recover, 'group_records_when_recover_ran': groups_at_recover, 'recover_rc': rc_r,
       'result_line_after_recover': ({k: res_after_recover.get(k) for k in ('status', 'side', 'cause', 'resume_ok', 'by')}
                                     if isinstance(res_after_recover, dict) else res_after_recover),
       'recover_tail': so_r.strip().splitlines()[-2:], 'chain_rc': rc_chain, 'chain_summary_status': (summ or {}).get('status'),
       'runner_calls': T.n_calls(w), 'folder_side_now': RR.folder_side(f1),
       'ledger_kinds': [f"{x.get('kind')}:{x.get('n')}:{x.get('status', '')}:{x.get('side', '')}" for x in T.led_lines(d)],
       'chain_log_tail': log.strip().splitlines()[-3:]}
add2 = T.led_add(d, 'ladder:P0')
out['next_add_rc'] = add2[0]
print(json.dumps(out, ensure_ascii=False, indent=1))
