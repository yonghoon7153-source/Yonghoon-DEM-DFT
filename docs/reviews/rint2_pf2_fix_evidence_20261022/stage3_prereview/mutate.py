import hashlib, json, os, subprocess, sys, time
M2 = sys.argv[1]; OUT = sys.argv[2]; only = sys.argv[3].split(',') if len(sys.argv) > 3 else None
SC = os.path.join(M2, 'scripts')
CMD = {
 'CH': ['scripts/test_rint_r_chain.py', '--only', 'B,D,G,U,V,N,C0,S0,M4'],
 'B6': ['scripts/test_ca_ext_b6.py', '--only', 'S'],
 'CJ': ['scripts/test_carbon_junction.py', '--only', 'QD2,QD,MUT-RCA2'],
}
MUTS = [
 ('R1', 'rint_r_chain.py', "        if there.get(nm) is not None and there[nm] != want:", "        if False:", 'CH'),
 ('R2', 'rint_r_chain.py', "    if r.get('plan_source') != S0_STAGE1_SOURCE:", "    if False:", 'CH'),
 ('R3', 'rint_r_chain.py', "        if not first and s.get('s0_reports') != s0reps:", "        if False:", 'CH'),
 ('R4', 'rint_r_chain.py', "        if not s0r_first and s.get('s0_reports') != s0r0:", "        if False:", 'CH'),
 ('R5', 'rint_r_chain.py', "    for k, nm in (('chain', '사슬'), ('runner', '러너')):", "    for k, nm in (('chain', '사슬'),):", 'CH'),
 ('R6', 'rint_r_chain.py', "    if now.get('head') != head:", "    if False:", 'CH'),
 ('R7', 'rint_r_chain.py', "    if files != r.get('files'):", "    if False:", 'CH'),
 ('R8', 'rint_r_chain.py', "parse_constant=_reject_constant, object_pairs_hook=_reject_dup)", "parse_constant=_reject_constant)", 'CH'),
 ('R9', 'rint_r_chain.py', "        elif lo_ok and hi_ok:\n            straddle.append(key)", "        elif lo_ok and hi_ok:\n            pass", 'CH'),
 ('R10', 'rint_r_chain.py', "(x == math.inf or (math.isfinite(x) and x > 0.0))", "(x == math.inf or math.isfinite(x))", 'CH'),
 ('R11', 'rint_r_chain.py', "    if code_key(s.get('code')) != code_key(code):              # ★ PF2 D", "    if False:              # ★ PF2 D", 'CH'),
 ('R12', 'rint_r_chain.py', "    if a.machine is not None and (a.stage == 'verdict' or not MACHINE_RE.fullmatch(a.machine)):", "    if a.machine is not None and (not MACHINE_RE.fullmatch(a.machine)):", 'CH'),
 ('R13', 'rint_r_chain.py', "    if r['plan_sha256'] != s0_sha:\n        return f'S0 단계 2", "    if False:\n        return f'S0 단계 2", 'CH'),
 ('R14', 'rint_r_chain.py', "        why = code_dirty_problem(s.get('code'))               # ★ PF2 D — 고쳐진 트리에서 돈 사다리", "        why = None               # ★ PF2 D — 고쳐진 트리에서 돈 사다리", 'CH'),
 ('V1', 'ca_ext_svcf.py', "    if (ust, ur, ul) != (sh, rh, lh):", "    if False:", 'B6'),
 ('V2', 'ca_ext_svcf.py', "    if not (hi == math.inf or hi >= lo * RATIO_FLOOR):", "    if False:", 'B6'),
 ('V3', 'ca_ext_svcf.py', "    if not r_ >= RATIO_FLOOR:", "    if False:", 'B6'),
 ('V4', 'ca_ext_svcf.py', "        if not (isinstance(gc, float) and not _is_bool(gc) and gc == 0.0):", "        if False:", 'B6'),
 ('V5', 'ca_ext_svcf.py', "    if form == 'inf' and lim == 'inf' and r_ is None:", "    if form == 'inf' and lim == 'inf':", 'B6'),
 ('V6', 'ca_ext_svcf.py', "        if (sh, rh, lh) != (rec.get('status'), rec.get('sv_counterfactual_ratio'), rec.get('ratio_limit')):", "        if False:", 'B6'),
 ('V7', 'ca_ext_svcf.py', "        if bad or cc.get('status') != CERT_OK_STATUS:", "        if cc.get('ok') is not True:", 'B6'),
 ('C1', 'carbon_junction.py', "            Ab, gb, cb, kb_ = _drop(Ab, gb, cb)", "            kb_ = 0", 'CJ'),
 ('C2', 'carbon_junction.py', "        if len(labels) != n_cen:", "        if False:", 'CJ'),
 ('C3', 'carbon_junction.py', "        if not np.all(pc[f:f + c] == x):", "        if False:", 'CJ'),
 ('C4', 'carbon_junction.py', "    rec['status_hi'] = up['status'] if up is not None else rec['status']", "    rec['status_hi'] = rec['status']", 'CJ'),
]
def run(cmd):
    t = time.time()
    p = subprocess.run([sys.executable, '-I'] + CMD[cmd], cwd=M2, capture_output=True, text=True,
                       env=dict(os.environ, OPENBLAS_NUM_THREADS='1'), timeout=1500)
    tail = [l for l in (p.stdout + p.stderr).splitlines() if 'FAIL' in l][:6]
    last = (p.stdout.strip().splitlines() or [''])[-1]
    return p.returncode, round(time.time() - t, 1), tail, last
res = {}
if only is None or 'BASE' in only:
    for c in CMD:
        res['BASE_' + c] = run(c); print('BASE', c, res['BASE_' + c][:2], res['BASE_' + c][3][:120], flush=True)
for tag, fn, old, new, cmd in MUTS:
    if only and tag not in only:
        continue
    p = os.path.join(SC, fn)
    src = open(p, encoding='utf-8').read()
    h0 = hashlib.sha256(src.encode()).hexdigest()
    n = src.count(old)
    if n != 1:
        res[tag] = ('BADMATCH', n); print(tag, 'BADMATCH', n, flush=True); continue
    open(p, 'w', encoding='utf-8').write(src.replace(old, new))
    try:
        rc, dt, tail, last = run(cmd)
    finally:
        open(p, 'w', encoding='utf-8').write(src)
        assert hashlib.sha256(open(p, encoding='utf-8').read().encode()).hexdigest() == h0
    verdict = 'CAUGHT' if rc != 0 else 'SURVIVED'
    res[tag] = (verdict, rc, dt, tail, last)
    print(tag, verdict, rc, dt, last[:100], '|', ' || '.join(x[:140] for x in tail[:3]), flush=True)
json.dump(res, open(OUT, 'w'), ensure_ascii=False, indent=1)
