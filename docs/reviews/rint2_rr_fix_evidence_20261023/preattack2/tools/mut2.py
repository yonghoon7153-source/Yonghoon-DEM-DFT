"""Round-2 mutation sample: revert/neutralise ONE fixed line per mutant (copy of new_src/scripts + docs symlink), run resident
tests suite by suite (stop at the first suite that has a FAIL).  usage: python3 -I -B mut2.py [names...]  -> JSON on stdout."""
import json, os, re, shutil, subprocess, sys
W = os.environ['ATK_ROOT']  # 리뷰어 작업 폴더 (리포 반입 때 한 줄만 바꿈 · README)
SRC = os.path.join(W, 'new_src')
RUN = os.path.join(W, 'tools_r1', 'run.py')
SV, CJ, RC = 'scripts/ca_ext_svcf.py', 'scripts/carbon_junction.py', 'scripts/rint_r_chain.py'
M = {
    'C1-k<=c': (SV, '    if k > c:\n', '    if False:\n'),
    'C1-ku-in-[k,k+ne]': (SV, '        if not k <= ku <= k + ne:\n', '        if False:\n'),
    'C1-lo-k>0-L==M': (SV, '        if k > 0 and L == M:\n', '        if False:\n'),
    'C1-lo-k==0-L!=M': (SV, '        if k == 0 and L != M:\n', '        if False:\n'),
    'C1-up-reach>0-U==M': (SV, '        if reach_up > 0 and U == M:\n', '        if False:\n'),
    'C1-up-reach==0-U!=M': (SV, '        if reach_up == 0 and U != M:\n', '        if False:\n'),
    'C1-up-plate-diff==npc': (SV, '        if (M[2] + M[3]) - (U[2] + U[3]) != npc:\n', '        if False:\n'),
    'C1-(7)-upper-c==lower-c': (SV, '    if un is not None and not (_count_ok(un) and int(un) == c):\n', '    if False:\n'),
    'C1-lo-plates==M': (SV, '        if L[2:] != M[2:]:\n', '        if False:\n'),
    'C1-lo-c==0-L!=M': (SV, '        if c == 0 and L != M:\n', '        if False:\n'),
    'C1-up-cut0-U!=M': (SV, '        if cut_up == 0 and U != M:\n', '        if False:\n'),
    'C1-up<=lo': (SV, '            big = [names[i] for i in range(4) if U[i] > L[i]]\n', '            big = []\n'),
    'C1-up-ne0npc0-U!=L': (SV, '            if ne == 0 and npc == 0 and U != L:\n', '            if False:\n'),
    'C1-topo-off': (SV, '    return _topo_problem(rec)\n', '    return None\n'),
    'C1-proj-no-topo': (SV, "'fp_cjunc_registry', 'fp_cjunc_rows') + CERT_TOPO_KEYS\n", "'fp_cjunc_registry', 'fp_cjunc_rows')\n"),
    'C1-up<=M': (SV, '        big = [names[i] for i in range(4) if U[i] > M[i]]\n', '        big = []\n'),
    'C1-lo<=M': (SV, '        big = [names[i] for i in (0, 1) if L[i] > M[i]]\n', '        big = []\n'),
    'C5-kind-prefix': (SV, '    if not (isinstance(kd, str) and kd == SV_CF_KIND)', "    if not (isinstance(kd, str) and kd.startswith('counterfactual'))"),
    'C5-rule-off': (SV, '    if not (isinstance(ru, str) and ru == SV_CF_RULE):\n', '    if False:\n'),
    'C5-rule-not-projected': (SV, "_COPY = ('kind', 'rule', 'requested'", "_COPY = ('kind', 'requested'"),
    'P-parallel-filter-off': (CJ, '    if s.any():\n        live = ', '    if False:\n        live = '),
    'P-reach-filter-off': (CJ, '    return int(np.count_nonzero(reach[lab[gone[:, 0]]])) if len(gone) else 0\n', '    return int(len(gone))\n'),
    'P-upper-main-plates-off': (CJ, '            if n_rm_plate:', '            if False:'),
    'R-readrun-topo-off': (RC, '+ SVCF.BIND_FIELDS + SVCF.CERT_TOPO_KEYS\n', '+ SVCF.BIND_FIELDS\n'),
    'C3-origin-check-off': (RC, '                org = [(n, r_monotone_problem(p)) for n, p in origin_points(self, law, c)]\n', '                org = []\n'),
    'C3-origin8-not-recorded': (RC, "                        self.org[(c, law, rr)].update((f'origin8_a{i}', x) for i, x in enumerate(r8))\n",
                                '                        pass\n'),
    'C3-origin12-not-recorded': (RC, "                    self.org[(c, law, rr)] = dict([('corner_a0', a0r)] + [(f'origin_a{i}', x) for i, x in zip(ORIGIN_ARMS, r12)])\n",
                                 "                    self.org[(c, law, rr)] = {}\n"),
    'C4-old-band': (RC, '    k = Fraction(k)\n    return k * Fraction(lo), k * Fraction(hi)\n',
                    "    e = Fraction(arm_err(rec)); s = Fraction(float(rec['sigma']))\n    return s * (1 - e), s * (1 + e)\n"),
    'C4-band-collapse-lo': (RC, '    return k * Fraction(lo), k * Fraction(hi)\n', '    return k * Fraction(lo), k * Fraction(lo)\n'),
    'C4-touch=stop': (RC, '            if r1 < r2 and b1[1] < b2[0]:\n', '            if r1 < r2 and b1[1] <= b2[0]:\n'),
    'C4-no-field-check': (RC, '    if not (_num(lo) and _num(hi) and _num(k) and 0 < lo <= hi and k > 0):\n', '    if False:\n'),
    'C4-readrun-no-fields': (RC, "**({k: (cert or {}).get(k) for k in ('target_lo', 'target_hi', 'scale')} if reg != 'VALID_ZERO_TOPOLOGY' else",
                             "**({k: None for k in ('target_lo', 'target_hi', 'scale')} if reg != 'VALID_ZERO_TOPOLOGY' else"),
    'C2-M1-plain-div': (SV, '    q = Fraction(a) / Fraction(b)\n', '    return a / b\n    q = Fraction(a) / Fraction(b)\n'),
    'C2-M7-swapped': (SV, "    if up and fq < q:\n        f = math.nextafter(f, math.inf)\n    elif not up and fq > q:\n        f = math.nextafter(f, -math.inf)\n",
                      "    if (not up) and fq < q:\n        f = math.nextafter(f, math.inf)\n    elif up and fq > q:\n        f = math.nextafter(f, -math.inf)\n"),
    'C2-up-only-round': (SV, "    elif not up and fq > q:\n        f = math.nextafter(f, -math.inf)\n", "    elif False:\n        f = math.nextafter(f, -math.inf)\n"),
    'C2-lo-only-round': (SV, "    if up and fq < q:\n        f = math.nextafter(f, math.inf)\n", "    if False:\n        f = math.nextafter(f, math.inf)\n"),
    'C4-scale-ignored': (RC,'    k = Fraction(k)\n    return k * Fraction(lo), k * Fraction(hi)\n', '    k = Fraction(1)\n    return k * Fraction(lo), k * Fraction(hi)\n'),
}
SUITES = [('tcj', 'test_carbon_junction.py', ['--only', 'QD2,QD3,QD4,QD5,QD6,QD7']),
          ('trc', 'test_rint_r_chain.py', ['--only', 'U15,U16,U17,U19,U20,M49,M50,V28,V29,V30,V31,V32,V33,V34,V35']),
          ('b6S', 'test_ca_ext_b6.py', ['--only', 'S'])]
env = dict(os.environ, TMPDIR=os.path.join(W, 'tmp'))
names = sys.argv[1:] or list(M)
res = {}
for nm in names:
    rel, old, new = M[nm]
    dst = os.path.join(W, 'mut', nm)
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(dst)
    shutil.copytree(os.path.join(SRC, 'scripts'), os.path.join(dst, 'scripts'))
    os.symlink(os.path.realpath(os.path.join(SRC, 'docs')), os.path.join(dst, 'docs'))
    p = os.path.join(dst, rel)
    t = open(p, encoding='utf-8').read()
    if t.count(old) != 1:
        res[nm] = {'error': f'pattern count {t.count(old)}'}
        shutil.rmtree(dst)
        continue
    open(p, 'w', encoding='utf-8').write(t.replace(old, new))
    res[nm] = {}
    for tag, f, args in SUITES:
        log = os.path.join(W, 'logs', f'mut2_{re.sub(r"[^A-Za-z0-9_.-]", "_", nm)}_{tag}.log')
        with open(log, 'w') as fh:
            r = subprocess.run([sys.executable, '-I', '-B', RUN, '-', os.path.join(dst, 'scripts', f)] + args, stdout=fh,
                               stderr=subprocess.STDOUT, env=env, timeout=1800)
        txt = open(log, encoding='utf-8', errors='replace').read()
        fails = [ln.strip()[:150] for ln in txt.splitlines() if re.match(r'\s*FAIL', ln)]
        summ = [ln.strip() for ln in txt.splitlines() if re.search(r'(\d+/\d+ PASS|\d+ PASS · \d+ FAIL|PASS \()', ln)]
        res[nm][tag] = {'rc': r.returncode, 'summary': summ[-1:], 'fails': fails[:4]}
        if r.returncode != 0 or fails:
            break
    shutil.rmtree(dst)
    print(nm, json.dumps(res[nm], ensure_ascii=False)[:400], flush=True, file=sys.stderr)
print(json.dumps(res, ensure_ascii=False, indent=1))
