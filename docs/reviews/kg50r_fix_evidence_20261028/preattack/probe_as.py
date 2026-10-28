import os, sys, subprocess, tempfile, shutil
WT = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/kg50fix-1028'
sys.path.insert(0, os.path.join(WT, 'scripts'))
import test_resume_ckpt as T
P = os.path.dirname(os.path.abspath(__file__))
MAIN = os.path.join(P, 'd2', 'input_kg50_d2_b50.liggghts')
CK = 'restart_kg50_d2_b50/restart_after_settling.bin'
tools = {'new': os.path.join(WT, 'scripts/resume_ckpt.sh'), 'old': os.path.join(P, 'resume_ckpt_old.sh')}
g = T.res_after('good', main=MAIN, case='kg50_d2_b50', tmpl=True)
anchor = 'read_restart restart_kg50_d2_b50/restart_after_settling.bin\n'
assert g.count(anchor) == 1
TM = 'fix pdd_mix all particledistribution/discrete 16800023 2 pts1 0.85 pts3 0.15\n'
assert g.count(TM) == 1, g.count(TM)
var = {
 'as_good': g,
 'as_dt_redef': g.replace(anchor, anchor + 'variable dt      equal 2.0e-6\ntimestep        ${dt}\nvariable dt      equal 1.0e-6\n'),
 'as_seg_velocity': g.replace('print "====== PHASE 2: STABILIZE ======"\n', 'velocity all set 0.0 0.0 0.0\nprint "====== PHASE 2: STABILIZE ======"\n'),
 'as_seg_run1_to_2': g.replace('\nrun 1\n', '\nrun 2\n', 1),
}
for name, txt in var.items():
    for tag, tool in tools.items():
        d = tempfile.mkdtemp(prefix='pas_', dir=P)
        try:
            r = os.path.join(d, 'res.liggghts'); open(r, 'w').write(txt)
            wd = os.path.join(d, 'wd'); os.mkdir(wd)
            p = subprocess.run(['bash', tool, '-C', MAIN, r, CK, '200001', wd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            out = p.stdout.decode()
            pr = [l.strip() for l in out.splitlines() if '✗' in l]
            print('%-18s %s rc=%d %s' % (name, tag, p.returncode, out.strip().splitlines()[-1]))
            for l in pr[:3]: print('      ' + l[:200])
        finally:
            shutil.rmtree(d, ignore_errors=True)
