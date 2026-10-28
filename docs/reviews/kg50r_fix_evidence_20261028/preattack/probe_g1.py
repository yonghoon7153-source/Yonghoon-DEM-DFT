import os, sys
WT = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/kg50fix-1028'
sys.path.insert(0, os.path.join(WT, 'scripts'))
import test_resume_ckpt as T
rows = T.T_OK[:]
assert '0.1000' in rows[1]
rows[1] = rows[1].replace('0.1000', '0.1003')   # setup line at S0 differs by 0.3 % (G1 1e-6) -- 21000/22000/22001 untouched
txt = '\n'.join(['LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0)'] + rows) + '\n'
for tool in sys.argv[1:]:
    r = T.run_case1(tool, 'good', None, trial_text=txt)
    g = [l for l in r['rep'].splitlines() if l.startswith('- G1') or '본 제출' in l]
    print('%-40s trial=%d main=%d | %s' % (os.path.basename(tool), r['ntrial'], r['nmain'], ' / '.join(x[:90] for x in g[-3:])))
