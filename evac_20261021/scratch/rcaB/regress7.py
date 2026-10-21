"""PRE-impl-07 round — run the regression list one at a time, each through the machine-wide lock (heavy.sh: flock · nice 19 ·
BLAS / OMP 1 thread); log each to its own file.

usage: python3 regress7.py <out dir> <tree>:<name> [<tree>:<name> ...]
<tree> = wt (the worktree) | fix (scratch copy b7fix = worktree scripts + the fixture patch) | pre (b7pre = pre-fix modules).
Writes <out>/<tree>_<name>.txt and appends `tree · name · rc · seconds (incl. lock wait) · last line` to <out>/summary.txt."""
import os
import subprocess
import sys
import time

SCR = '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad'
TREES = {'wt': '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a9a78b0be0713b231',
         'fix': SCR + '/rcaB/b7fix', 'pre': SCR + '/rcaB/b7pre'}
HEAVY = SCR + '/heavy.sh'
TESTS = {
    'target_fast': ['python3', 'scripts/test_step3_target_cert.py'],
    'target_long': ['python3', 'scripts/test_step3_target_cert.py', '--long'],
    'conv_cert': ['python3', 'scripts/test_step3_conv_cert.py'],
    's3_selftest': ['python3', 'scripts/step3_sigma.py', '--selftest'],
    's3_selftest_rint': ['python3', 'scripts/step3_sigma.py', '--selftest-rint'],
    'rc_selftest': ['python3', 'scripts/run_contract.py', '--selftest'],
    'ca_b6': ['python3', 'scripts/test_ca_ext_b6.py'],
    'ca_b6_old': ['python3', 'scripts/test_ca_ext_b6.py', '--old-scripts', SCR + '/rcaB/b7pre/scripts'],
    'rint_chain': ['python3', 'scripts/test_rint_r_chain.py'],
    'rint_chain_e2e': ['python3', 'scripts/test_rint_r_chain_e2e.py'],
    'ca_runner': ['python3', 'scripts/test_ca_ext_runner.py'],
    'ca_verdict': ['python3', 'scripts/test_ca_ext_verdict.py'],
    'ca_z3': ['python3', 'scripts/test_ca_ext_z3.py'],
    'payload_bitid': ['python3', SCR + '/rcaB/probe_payload_bitid.py', SCR + '/rcaB/b7pre', SCR + '/rcaB/b7fix'],
    'cmd_selftest': ['python3', 'scripts/check_method_discipline.py', '--selftest'],
    'cmd_noarg': ['python3', 'scripts/check_method_discipline.py'],
}
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
env = dict(os.environ)
env.pop('PYTHONPATH', None)
for item in sys.argv[2:]:
    tree, name = item.split(':', 1)
    cmd = ['bash', HEAVY] + TESTS[name]
    t0 = time.time()
    log = os.path.join(OUT, f'{tree}_{name}.txt')
    with open(log, 'w') as fh:
        rc = subprocess.run(cmd, cwd=TREES[tree], env=env, stdout=fh, stderr=subprocess.STDOUT).returncode
    dt = time.time() - t0
    lines = [x for x in open(log, encoding='utf-8', errors='replace').read().splitlines() if x.strip()]
    tail = lines[-1][:240] if lines else ''
    with open(os.path.join(OUT, 'summary.txt'), 'a') as fh:
        fh.write(f'{tree}\t{name}\trc={rc}\t{dt:.0f}s\t{tail}\n')
    print(f'{tree}:{name} rc={rc} {dt:.0f}s {tail}', flush=True)
print('ALL DONE', flush=True)
