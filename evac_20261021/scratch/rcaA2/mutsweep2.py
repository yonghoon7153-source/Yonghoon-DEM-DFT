"""One-line source mutants of the A2 implementation — each must make a named test fail (for the right reason).
Runs the worktree tests through drv.py with a temp impl dir (one file mutated).  Writes a JSON table."""
import json
import os
import shutil
import subprocess
import sys
import tempfile

D = '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaA2/'
IMPL = sys.argv[1] if len(sys.argv) > 1 else D + 'impl'
OUT = sys.argv[2] if len(sys.argv) > 2 else D + 'logs/mutsweep2.json'
CJ, CW, S0, S3 = 'carbon_junction.py', 'ca_ext_cjunc.py', 'ca_s0_census.py', 'step3_sigma.py'
MUTS = [('M10 자기 L_c = 두 쪽 선분 전부 짝 (접합 쌍 제한 끔)', 'carbon_junction.py', '        si = np.searchsorted(su, S); qi = np.searchsorted(qu, Q)\n', '        si = np.repeat(np.arange(len(su)), len(qu)); qi = np.tile(np.arange(len(qu)), len(su))\n', 'cj', 'KINK,RCA03,SELFD,REC,CEN'), ('M12 쌍 무리 고리 둘레 잇기 끔', 'carbon_junction.py', '                if rg:\n                    a_, b_ = a_ % n_, b_ % n_', '                if False:\n                    a_, b_ = a_ % n_, b_ % n_', 'cj', 'RING'), ('M19 자기 분산판 맞은편 = 짝 제한 끔', 'carbon_junction.py', '                    m_ = pb[pa == Xs[j]]\n', '                    m_ = pb\n', 'cj', 'SELFD,RCA03,KINK,RING,CEN'), ('M25 단계 2 --r-plan-path 필수 끔', 'ca_s0_census.py', '        if not threshold_commit or not plan_path or not r_plan_path:', '        if not threshold_commit or not plan_path:', 's0', 't_plan_commit'), ('M26 같은 셀 재방문 = 별칭 짝도 셈', 'carbon_junction.py', "                if pos['piece'][p] != pos['piece'][q] or int(pos['alias'][p]) == q or int(pos['alias'][q]) == p:", "                if pos['piece'][p] != pos['piece'][q]:", 'cj', 'RING'), ('M27 경로로만 = 경로 끊김 검사 끔', 'carbon_junction.py', "        if np.all(pos['live'][a0_:a1_ + 1]):", '        if True:', 'cj', 'CEN,KINK-R,RCA03,QD,QC')]


def run(tmpd, kind, tags):
    if kind == 'cj':
        cmd = [sys.executable, D + 'drv.py', '--impl', tmpd, '--', '--only', tags]
    else:
        cmd = [sys.executable, D + 'run_s0_groups.py', '--impl', tmpd] + tags.split(',')
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1')
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=900, env=env,
                       cwd='/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1ea4b71aa06a03ee')
    out = p.stdout + p.stderr
    fails = [ln.strip() for ln in out.splitlines() if ln.strip().startswith('FAIL ') or ln.strip().startswith('FAIL:')]
    summ = [ln for ln in out.splitlines() if 'PASS' in ln and ('test_carbon_junction:' in ln or ' FAIL' in ln)]
    return p.returncode, fails, (summ[-1] if summ else out[-300:])


rows = []
base = {}
for kind, tags in sorted({(m[4], m[5]) for m in MUTS}):
    base[(kind, tags)] = run(IMPL, kind, tags)
for nm, fn, old, new, kind, tags in MUTS:
    tmpd = tempfile.mkdtemp(prefix='a2mut_')
    try:
        for f in os.listdir(IMPL):
            if f.endswith('.py'):
                shutil.copy(os.path.join(IMPL, f), tmpd)
        src = open(os.path.join(tmpd, fn), encoding='utf-8').read()
        c = src.count(old)
        if c != 1:
            rows.append({'mutant': nm, 'file': fn, 'error': f'snippet count {c}'})
            print(nm, 'SNIPPET', c, flush=True)
            continue
        open(os.path.join(tmpd, fn), 'w', encoding='utf-8').write(src.replace(old, new))
        rc, fails, summ = run(tmpd, kind, tags)
        b = base[(kind, tags)]
        rows.append({'mutant': nm, 'file': fn, 'tests': tags, 'base_rc': b[0], 'base_summary': b[2], 'rc': rc, 'summary': summ,
                     'caught': rc != 0 and b[0] == 0, 'fails': fails[:6]})
        print(nm, '→', 'CAUGHT' if (rc != 0 and b[0] == 0) else 'NOT CAUGHT', '|', summ, flush=True)
    finally:
        shutil.rmtree(tmpd, ignore_errors=True)
json.dump({'impl': IMPL, 'base': {f'{k[0]}:{k[1]}': v[2] for k, v in base.items()}, 'rows': rows}, open(OUT, 'w'),
          ensure_ascii=False, indent=1)
print('wrote', OUT)
