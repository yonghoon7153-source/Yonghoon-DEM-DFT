"""Linux-only follow-up candidate. NOT EXECUTED by this Windows review.

Use fresh temporary files; no production edits or scientific solves.
Checks whether the committed controls detect a constant-True token probe.
"""
from pathlib import Path
import argparse, json, sys, tempfile

p=argparse.ArgumentParser()
p.add_argument('--repo',type=Path,required=True)
a=p.parse_args()
if sys.platform != 'linux':
    raise SystemExit('NOT RUN: Linux fcntl required; no substitute lock implementation is used')
import fcntl
root=a.repo.resolve()
sys.path[:0]=[str(root),str(root/'tests'),str(root/'docs/22p_gap')]
import test_gate63_defensive as g63
import test_gate64_defensive as g64
import src.io as io

# Baseline: same token, same inode, held then explicitly unlocked before release.
base=Path(tempfile.mkdtemp(prefix='gate65_e2_followup_'))
tok=io.acquire_run_lock(base/'token-control','.fit.lock')
try:
    held=g63._kernel_lock_held(tok)
    fcntl.flock(tok.fd,fcntl.LOCK_UN)
    unheld=g63._kernel_lock_held(tok)
    assert (held,unheld)==(True,False),(held,unheld)
finally:
    io.release_run_lock(tok)

def controls(label):
    result={}
    for module,fn in ((g63,'test_the_kernel_lock_probe_itself_is_not_vacuous'),
                      (g64,'test_the_kernel_lock_probe_control_actually_runs_both_directions')):
        d=base/(label+'_'+fn)
        d.mkdir()
        try:
            getattr(module,fn)(d)
            result[fn]='PASS'
        except AssertionError as e:
            result[fn]='FAIL: '+str(e)
    return result

baseline=controls('baseline')
old=g63._kernel_lock_held
try:
    g63._kernel_lock_held=lambda tok: True
    mutated=controls('constant_true_token_probe')
finally:
    g63._kernel_lock_held=old
print(json.dumps({'artifact_class':'unexecuted follow-up until run on Linux',
                  'same_token_baseline':[held,unheld],
                  'baseline':baseline,'mutated':mutated,'temporary_root':str(base)},indent=2))
