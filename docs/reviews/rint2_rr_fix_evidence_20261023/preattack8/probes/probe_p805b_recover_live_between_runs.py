"""P8-05b — same window between two runs: run 1 ended (end record by chain · confirmed True), run 2 not launched yet (chain reading run 1's
arms).  recover --ledger then sees every group confirmed and writes a result line (post · resume_ok True) for a live chain.

Driver = real chain; read_run wrapped with a 15 s sleep on its first call (stands in for a slow arm read / certificate check).

  python3 -I probe_p805b_recover_live_between_runs.py <tree>
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
_orig = RR.read_run
_n = [0]
def slow(*a, **k):
    _n[0] += 1
    if _n[0] == 1:
        time.sleep(15.0)
    return _orig(*a, **k)
RR.read_run = slow
sys.exit(RR.main(cfg['argv']))
'''

d, _rc, _so = T.led_new('P805b')
_r, n1, _s = T.led_add(d, 'ladder:P0')
b1 = Path(T.TD) / 'runs' / 'P805b_b1'
w = T.world('P805b')
pr = T.gr_spawn_chain('P805b', T.ladder_argv(b1) + ['--ledger', str(d), '--attempt', str(n1)], w, driver=DRV, dname='p805b_driver.py')
f1 = b1 / f'attempt_{n1}'
ep = f1 / 'groups' / 'L01_floor.end.json'
t_end = time.time() + 120
while time.time() < t_end and not ep.is_file():
    time.sleep(0.05)
time.sleep(0.5)
alive_at_recover = pr.poll() is None
groups_at_recover = sorted(p.name for p in (f1 / 'groups').glob('*')) if (f1 / 'groups').is_dir() else []
rc_r, so_r = T.call(['--stage', 'recover', '--out', str(f1), '--ledger', str(d)], w)
res = T.led_result(d, n1)
add2 = T.led_add(d, 'ladder:P0', resume=n1)
rc_chain = pr.wait(timeout=600)
summ = T.u_json(f1 / 'ladder_summary.json')
out = {'chain_alive_when_recover_ran': alive_at_recover, 'group_records_when_recover_ran': groups_at_recover, 'recover_rc': rc_r,
       'result_line': ({k: res.get(k) for k in ('status', 'side', 'cause', 'resume_ok', 'by')} if isinstance(res, dict) else res),
       'resume_add_while_chain_alive': (add2[0], add2[1]), 'recover_tail': so_r.strip().splitlines()[-2:], 'chain_rc': rc_chain,
       'chain_summary_status': (summ or {}).get('status'), 'runner_calls': T.n_calls(w),
       'ledger_kinds': [f"{x.get('kind')}:{x.get('n')}:{x.get('status', '')}:{x.get('side', '')}" for x in T.led_lines(d)]}
print(json.dumps(out, ensure_ascii=False, indent=1))
