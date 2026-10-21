"""Mutation table — run each M check of test_rint_r_chain and print why the target check failed (right reason?)."""
import shutil
import sys
import tempfile

sys.path.insert(0, '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-afe53be7bdb176c82/scripts')
import test_rint_r_chain as T
import rint_r_chain as RR

T.RR = RR
T.TD = tempfile.mkdtemp(prefix='mutwhy_')
try:
    T.fixtures()
    sel = sys.argv[1].split(',') if len(sys.argv) > 1 else None
    for cid, title, fn in T.CHECKS:
        if not cid.startswith('M') or (sel and cid not in sel):
            continue
        res, why = fn()
        print(f'{cid} caught={res} :: {str(why)[:420]}')
finally:
    shutil.rmtree(T.TD, ignore_errors=True)
