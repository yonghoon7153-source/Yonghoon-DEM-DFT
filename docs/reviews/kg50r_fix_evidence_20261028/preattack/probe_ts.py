import os, sys
WT = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/kg50fix-1028'
sys.path.insert(0, os.path.join(WT, 'scripts'))
import test_resume_ckpt as T
for tool in sys.argv[1:]:
    for t in ('0', 'abc', '-5'):
        r = T.run_case1(tool, 'good', 'ok', extra=('-T', '-t', t))
        o = [l.strip() for l in r['out'].splitlines() if '⛔' in l or '✗' in l][:1]
        print('%-14s -t %-4s rc=%s trial=%d main=%d %s' % (os.path.basename(tool), t, r['rc'], r['ntrial'], r['nmain'], o))
