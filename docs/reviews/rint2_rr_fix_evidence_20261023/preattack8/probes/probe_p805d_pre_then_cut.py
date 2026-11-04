"""P8-05d — consequence of P8-05 (a): the premature 'pre' result line lets a later folder cut-back pass the verdict.

1. chain alive · presolve slowed 20 s · recover --ledger writes 'interrupted · pre' (P8-05 a)
2. the live chain finishes CALIBRATED in attempt_1 (its own result line refused)
3. --add + attempt 2 (new, not a resume) in the same base -> runs (presolve does not re-count earlier non-resume attempts)
4. verdict on attempt 2 -> expected stop (attempt_1 folder sha != its result line)
5. cut attempt_1 back to attempt.json only (one hand: delete the produced files) -> verdict again

  python3 -I probe_p805d_pre_then_cut.py <tree>
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

d, _rc, _so = T.led_new('P805d')
_r, n1, _s = T.led_add(d, 'ladder:P0')
b1 = Path(T.TD) / 'runs' / 'P805d_b1'
w = T.world('P805d')
pr = T.gr_spawn_chain('P805d', T.ladder_argv(b1) + ['--ledger', str(d), '--attempt', str(n1)], w, driver=DRV, dname='p805d_driver.py')
t_end = time.time() + 60
while time.time() < t_end and not any(x.get('kind') == 'start' for x in T.led_lines(d)):
    time.sleep(0.1)
f1 = b1 / f'attempt_{n1}'
files_at_recover = sorted(str(p.relative_to(f1)) for p in f1.rglob('*') if p.is_file())
alive = pr.poll() is None
rc_r, _so_r = T.call(['--stage', 'recover', '--out', str(f1), '--ledger', str(d)], w)
r1 = T.led_result(d, n1)
rc_chain = pr.wait(timeout=600)
s1 = T.u_json(f1 / 'ladder_summary.json')
_r2, n2, _s2 = T.led_add(d, 'ladder:P0')
b = T.lad_att('P805d_2', T.world('P805d_2'), d, n2, base=b1)
v1 = T.ver_led('P805d_v1', [b['out']], d)
for p in sorted(f1.iterdir()):                                              # one hand: delete what the live chain produced
    if p.name != 'attempt.json':
        shutil.rmtree(p) if p.is_dir() else p.unlink()
v2 = T.ver_led('P805d_v2', [b['out']], d)
out = {'chain_alive_at_recover': alive, 'files_at_recover': files_at_recover, 'recover_rc': rc_r,
       'result_1': {k: (r1 or {}).get(k) for k in ('status', 'side', 'cause', 'resume_ok')}, 'attempt1_chain_rc': rc_chain,
       'attempt1_summary_status': (s1 or {}).get('status'), 'attempt1_runner_calls': T.n_calls(w),
       'attempt2': {'n': n2, 'rc': b['rc'], 'status': (b['sum'] or {}).get('status')},
       'verdict_before_cut': {'stop': T.stop_code(v1), 'cause': str((((v1.get('v') or {}).get('stop')) or {}).get('cause'))[:200]},
       'verdict_after_cut': {'stop': T.stop_code(v2), 'cause': str((((v2.get('v') or {}).get('stop')) or {}).get('cause'))[:200],
                             'adopted': ((v2.get('v') or {}).get('ledger') or {}).get('targets')}}
print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
