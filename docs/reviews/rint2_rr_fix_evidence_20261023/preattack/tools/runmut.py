"""Run selected resident tests against each mutant tree; report pass/fail counts (subprocess per test file)."""
import os, re, subprocess, sys, json
A = os.environ['ATK_ROOT']  # 리뷰어 작업 폴더 (new_src · old_src · mut · logs · tmp · tools) — 리포 사본에서 바꾼 줄
RUN = os.path.join(A, 'tools', 'run.py')
env = dict(os.environ, TMPDIR=os.path.join(A, 'tmp'))
TESTS = [('tcj', 'test_carbon_junction.py', ['--only', 'QD2,QD3,QD4']),
         ('trc', 'test_rint_r_chain.py', ['--only', 'U15,U16,U17,V28,V29,V30,V31']),
         ('b6S', 'test_ca_ext_b6.py', ['--only', 'S'])]
muts = sys.argv[1:]
res = {}
for m in muts:
    tree = os.path.join(A, 'mut', m) if m != 'BASE' else os.path.join(A, 'new_src')
    res[m] = {}
    for tag, f, args in TESTS:
        log = os.path.join(A, 'logs', f'mut_{m}_{tag}.log')
        with open(log, 'w') as fh:
            r = subprocess.run([sys.executable, '-I', '-B', RUN, '-', os.path.join(tree, 'scripts', f)] + args, stdout=fh,
                               stderr=subprocess.STDOUT, env=env, timeout=3600)
        txt = open(log, encoding='utf-8', errors='replace').read()
        fails = [ln.strip()[:160] for ln in txt.splitlines() if re.match(r'\s*(FAIL|  -)', ln)]
        tail = [ln for ln in txt.splitlines() if 'PASS' in ln and ('/' in ln or '·' in ln)][-1:] if txt else []
        summ = [ln for ln in txt.splitlines() if re.search(r'(\d+/\d+ PASS|\d+ PASS · \d+ FAIL)', ln)]
        res[m][tag] = {'rc': r.returncode, 'summary': summ[-1:] , 'fails': fails[:12]}
print(json.dumps(res, ensure_ascii=False, indent=1))
