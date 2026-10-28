import os, sys
WT = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/kg50fix-1028'
sys.path.insert(0, os.path.join(WT, 'scripts'))
import test_resume_ckpt as T
tool = sys.argv[1]
mb = open(T.MAIN, 'rb').read()
old = b'restart 50000 restart_kg50_d07_b40/restart_settling_*.bin\n'
i = mb.index(old)
j = mb.index(b'run 200000\n', i)
mb2 = mb[:j] + b'run 200000 every 1000 "velocity all set 0.0 0.0 0.0"\n' + mb[j + len(b'run 200000\n'):]
r = T.run_case1(tool, 'good', 'ok', main_bytes=mb2)
print('B_main_every e2e: rc=%s trial=%d main=%d' % (r['rc'], r['ntrial'], r['nmain']))
for l in r['rep'].splitlines():
    if '정적 대조' in l or '본 제출' in l: print('   ', l[:200])
