"""Run the regression list one at a time (nice 19 · BLAS 1 thread) from the worktree; log each to its own file.

usage: python3 regress.py <worktree> <out dir> <name> [<name> ...]   (names from TESTS below, in the given order)
Writes <out>/<name>.txt (full output) and appends a summary line to <out>/summary.txt: name · rc · seconds · last line.
"""
import os
import subprocess
import sys
import time

WT, OUT = sys.argv[1], sys.argv[2]
S1_OLD = '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/s1/old/scripts'
B47 = '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaB/base47/scripts'
TESTS = {
    'target_fast': ['python3', 'scripts/test_step3_target_cert.py'],
    'target_long': ['python3', 'scripts/test_step3_target_cert.py', '--long'],
    'conv_cert_full': ['python3', 'scripts/test_step3_conv_cert.py'],
    's3_selftest': ['python3', 'scripts/step3_sigma.py', '--selftest'],
    's3_selftest_rint': ['python3', 'scripts/step3_sigma.py', '--selftest-rint'],
    'rc_selftest': ['python3', 'scripts/run_contract.py', '--selftest'],
    'join': ['python3', 'scripts/test_rint_g2_join.py'],
    'face_alpha': ['python3', 'scripts/test_ptfe_face_alpha.py', '--old-scripts', S1_OLD],
    'carbon_junction': ['python3', 'scripts/test_carbon_junction.py'],
    'ca_b6': ['python3', 'scripts/test_ca_ext_b6.py'],
    'ca_b6_old': ['python3', 'scripts/test_ca_ext_b6.py', '--old-scripts', B47],
    'ca_z3_old': ['python3', 'scripts/test_ca_ext_z3.py', '--old-scripts', B47],
    'ca_runner': ['python3', 'scripts/test_ca_ext_runner.py'],
    'ca_verdict': ['python3', 'scripts/test_ca_ext_verdict.py'],
    'ca_z1': ['python3', 'scripts/test_ca_ext_z1.py'],
    'rint_chain': ['python3', 'scripts/test_rint_r_chain.py'],
    'ca_z3': ['python3', 'scripts/test_ca_ext_z3.py'],
    'rint_chain_e2e': ['python3', 'scripts/test_rint_r_chain_e2e.py'],
    'cmd_selftest': ['python3', 'scripts/check_method_discipline.py', '--selftest'],
    'cmd_noarg': ['python3', 'scripts/check_method_discipline.py'],
}
env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')
env.pop('PYTHONPATH', None)
os.makedirs(OUT, exist_ok=True)
for name in sys.argv[3:]:
    cmd = ['nice', '-n', '19'] + TESTS[name]
    t0 = time.time()
    with open(os.path.join(OUT, name + '.txt'), 'w') as fh:
        rc = subprocess.run(cmd, cwd=WT, env=env, stdout=fh, stderr=subprocess.STDOUT).returncode
    dt = time.time() - t0
    lines = [x for x in open(os.path.join(OUT, name + '.txt'), encoding='utf-8', errors='replace').read().splitlines() if x.strip()]
    tail = lines[-1][:220] if lines else ''
    with open(os.path.join(OUT, 'summary.txt'), 'a') as fh:
        fh.write(f'{name}\trc={rc}\t{dt:.0f}s\t{tail}\n')
    print(f'{name} rc={rc} {dt:.0f}s {tail}', flush=True)
