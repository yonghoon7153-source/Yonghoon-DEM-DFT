import os, sys
WT = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/kg50fix-1028'
sys.path.insert(0, os.path.join(WT, 'scripts'))
import test_resume_ckpt as T
rows = [r for r in T.T_OK if not r.lstrip().startswith('22000 ')]
assert len(rows) == len(T.T_OK) - 1
txt = '\n'.join(['LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0)'] + rows) + '\n'
for tool in sys.argv[1:]:
    r = T.run_case1(tool, 'good', None, trial_text=txt)
    g = [l for l in r['rep'].splitlines() if l.startswith('- G3') or '본 제출' in l]
    print('%-22s trial=%d main=%d | %s' % (os.path.basename(tool), r['ntrial'], r['nmain'], ' / '.join(x[:100] for x in g[-2:])))
