# 24 real-deck pairs = 12 kg50 main decks (docs/data/kg50_decks_2026102[67]_*) × (settling · after_settling) — the review's a04_regress.py
#   settling resume = main minus create_box/templates/insertion block, read_restart restart_settling_20001.bin + templates after processors,
#   PHASE 1 run 200000 → 180000 · after_settling resume = test_resume_ckpt.res_after('good', main, case, tmpl=True)
#   usage: python3 -I real24.py <worktree> <tool> [<tool2> …]   → per tool: rc per pair · problem lines when rc != 0 · total
import glob, hashlib, os, re, shutil, subprocess, sys, tempfile
WT = os.path.abspath(sys.argv[1])
TOOLS = [os.path.abspath(x) for x in sys.argv[2:]]
TMP = '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/f01r2/tmp'
sys.path.insert(0, os.path.join(WT, 'scripts'))
import test_resume_ckpt as T  # noqa: E402


def tmpl_lines(raw):
    return [l for l in raw if len(l.split()) >= 2 and l.split()[0] == 'fix' and re.match(r'^(pts[0-9]+|pdd_mix)$', l.split()[1])]


def settle_resume(main, case):
    raw = open(main, encoding='utf-8').readlines()
    tl = tmpl_lines(raw)
    out, skip, settle = [], False, False
    for l in raw:
        s = l.strip()
        if re.match(r'fix\s+(pts\d+|pdd_mix)\b', s) or s.startswith('create_box'):
            continue
        if re.match(r'fix\s+ins_mix\b', s):
            skip = True
        if 'PHASE 1: SETTLING' in s:
            skip = False
        if skip:
            continue
        out.append(l)
        if s.startswith('processors'):
            out.append('read_restart restart_%s/restart_settling_20001.bin\n' % case)
            out.extend(tl)
        if 'PHASE 1: SETTLING' in s:
            settle = True
        if settle and re.match(r'run\s+200000\b', s):
            out[-1] = 'run 180000\n'
            settle = False
    return ''.join(out)


def runC(tool, mt, rt, ck, s0):
    d = tempfile.mkdtemp(prefix='r24_', dir=TMP)
    try:
        mp, rp = os.path.join(d, 'm.liggghts'), os.path.join(d, 'r.liggghts')
        for p, t in ((mp, mt), (rp, rt)):
            with open(p, 'w', encoding='utf-8', newline='') as f:
                f.write(t)
        p = subprocess.run(['bash', tool, '-C', mp, rp, ck, str(s0), d], capture_output=True, text=True, cwd=d)
        return p.returncode, p.stdout + p.stderr
    finally:
        shutil.rmtree(d, ignore_errors=True)


os.makedirs(TMP, exist_ok=True)
mains = [m for m in sorted(glob.glob(os.path.join(WT, 'docs/data/kg50_decks_2026102[67]_*/kg50_*/input_kg50_*.liggghts')))
         if not m.endswith('_insert.liggghts')]
for tool in TOOLS:
    print('tool %s sha256 %s' % (tool, hashlib.sha256(open(tool, 'rb').read()).hexdigest()))
    n = ok = 0
    for m in mains:
        case = os.path.basename(m)[len('input_'):-len('.liggghts')]
        mt = open(m, encoding='utf-8').read()
        for kind, rt, ck, s0 in (('settling', settle_resume(m, case), 'restart_%s/restart_settling_20001.bin' % case, 20001),
                                 ('after_settling', T.res_after('good', m, case, tmpl=True), 'restart_%s/restart_after_settling.bin' % case, 200001)):
            rc, out = runC(tool, mt, rt, ck, s0)
            n += 1
            ok += rc == 0
            last = [l for l in out.splitlines() if '재개 덱 정적 대조:' in l]
            rec = [l.strip() for l in out.splitlines() if '그 자리 치환 대조' in l]
            print('  %-55s %-15s rc=%d  %s  %s' % (os.path.relpath(m, WT), kind, rc, last[-1].strip() if last else '?', rec[0][:90] if rec else ''))
            if rc != 0:
                for l in out.splitlines():
                    if l.startswith('  ✗'):
                        print('      ' + l[:250])
    print('  합: %d 쌍 · rc 0 = %d' % (n, ok))
