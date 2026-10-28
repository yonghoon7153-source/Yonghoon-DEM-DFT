import os, sys, subprocess, tempfile, shutil
WT = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/kg50fix-1028'
sys.path.insert(0, os.path.join(WT, 'scripts'))
import test_resume_ckpt as T
P = os.path.dirname(os.path.abspath(__file__))
MAIN = os.path.join(P, 'd2', 'input_kg50_d2_b50.liggghts')
CK = 'restart_kg50_d2_b50/restart_after_settling.bin'
g = T.res_after('good', main=MAIN, case='kg50_d2_b50', tmpl=True)
seg0 = 'print "====== RESTART SAVED ======"\n'
assert g.count(seg0) == 1
v = {'as_drop_seg0': g.replace(seg0, ''),
     # make the seg's first command a physics fix: insert into BOTH main and resume? no -> drop only from resume a fix that main has right after write_restart
     }
# variant where main's seg starts with a fix (main modified) and the resume omits it
M = open(MAIN, encoding='utf-8').read()
wr = 'write_restart restart_kg50_d2_b50/restart_after_settling.bin\n'
assert M.count(wr) == 1
M2 = M.replace(wr, wr + 'fix extra all viscous 0.7\n')
tools = {'new': os.path.join(WT, 'scripts/resume_ckpt.sh'), 'mut_qnone': os.path.join(P, 'mut/py_qnone.sh'), 'mut_reinsert': os.path.join(P, 'mut/py_reinsert.sh')}
cases = [('as_drop_seg0', MAIN, v['as_drop_seg0']), ('as_main_seg0_fix_missing_in_resume', None, g)]
for name, main, res in cases:
    d = tempfile.mkdtemp(prefix='pqn_', dir=P)
    try:
        if main is None:
            main = os.path.join(d, 'm.liggghts'); open(main, 'w').write(M2)
        r = os.path.join(d, 'r.liggghts'); open(r, 'w').write(res)
        wd = os.path.join(d, 'wd'); os.mkdir(wd)
        for tag, tool in tools.items():
            p = subprocess.run(['bash', tool, '-C', main, r, CK, '200001', wd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            out = p.stdout.decode()
            print('%-36s %-12s rc=%d %s' % (name, tag, p.returncode, out.strip().splitlines()[-1]))
            for l in [l for l in out.splitlines() if '✗' in l][:2]: print('       ' + l.strip()[:200])
    finally:
        shutil.rmtree(d, ignore_errors=True)
# reinsert essential role: main deck that does NOT unfix the insert fix; resume re-declares it verbatim
M3 = open(MAIN, encoding='utf-8').read()
assert M3.count('unfix ins_mix\n') == 1
M3 = M3.replace('unfix ins_mix\n', '')
R0 = open(os.path.join(P, 'd2', 'input_kg50_d2_b50_r4.liggghts'), encoding='utf-8').read()
ins = ('fix ins_mix all insert/pack seed 16900021 distributiontemplate pdd_mix &\n    maxattempt 3000 insert_every once overlapcheck yes all_in no &\n'
       '    vel constant 0.0 0.0 -0.5 &\n    region reg_mix &\n    volumefraction_region 0.321\n')
assert M3.count(ins) == 1
TM = 'fix pdd_mix all particledistribution/discrete 16800023 2 pts1 0.85 pts3 0.15\n'
R3 = R0.replace(TM, TM + 'region reg_mix block 0.0 0.05 0.0 0.05 0.005 0.322700 units box\n' + ins, 1)
d = tempfile.mkdtemp(prefix='pqn_', dir=P)
try:
    m = os.path.join(d, 'm.liggghts'); open(m, 'w').write(M3)
    r = os.path.join(d, 'r.liggghts'); open(r, 'w').write(R3)
    wd = os.path.join(d, 'wd'); os.mkdir(wd)
    for tag, tool in tools.items():
        p = subprocess.run(['bash', tool, '-C', m, r, 'restart_kg50_d2_b50/restart_settling_20001.bin', '20001', wd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = p.stdout.decode()
        print('%-36s %-12s rc=%d %s' % ('main_keeps_ins_resume_redeclares', tag, p.returncode, out.strip().splitlines()[-1]))
        for l in [l for l in out.splitlines() if '✗' in l][:2]: print('       ' + l.strip()[:200])
finally:
    shutil.rmtree(d, ignore_errors=True)
