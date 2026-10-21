#!/usr/bin/env python3
"""recheck 10-21 — mutation tests on the launcher D2 guards (run_all.sh · resume_all.sh) at 9412f384a.

Mutant root mutL/<name>/ = { scripts -> W/scripts (symlink) · dem_scripts/mixer_20260919 -> W/... (symlink) ·
dem_scripts/mixer_20260921/ = real copies, one file edited }.  Runs that root's test_launcher.sh (PYTHONDONTWRITEBYTECODE=1 ·
TMPDIR in scratch).  Records PASS/FAIL counts and the failing check names.
usage: python3 -I -B probe_launcher_mutations.py <W>
"""
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
W = sys.argv[1]
L21 = os.path.join(W, 'dem_scripts', 'mixer_20260921')
G_RA = """  if [[ "$nm" =~ ^(npprobe[1-9][0-9]*_)?GM(cc|cu|uc|uu)_ ]] || grep -qF '★ D2 결합 규칙 (기하평균' "$d/in.mixer"; then
    echo "· D2 결합 규칙 셀 건너뜀"""
MUT = [
    ('CONTROL', None, None, None),
    ('L1_run_all_no_header_grep', 'run_all.sh', G_RA,
     G_RA.replace(""" || grep -qF '★ D2 결합 규칙 (기하평균' "$d/in.mixer"; then""", "; then")),
    ('L2_run_all_no_name_guard', 'run_all.sh', G_RA,
     G_RA.replace("""[[ "$nm" =~ ^(npprobe[1-9][0-9]*_)?GM(cc|cu|uc|uu)_ ]] || grep""", "grep")),
    ('L3_resume_all_no_header_grep', 'resume_all.sh',
     """  if [[ "$nm" =~ ^(npprobe[1-9][0-9]*_)?GM(cc|cu|uc|uu)_ ]] || grep -qF '★ D2 결합 규칙 (기하평균' "$d/in.mixer"; then echo "· D2 결합 규칙 셀 — 재개 없음""",
     """  if [[ "$nm" =~ ^(npprobe[1-9][0-9]*_)?GM(cc|cu|uc|uu)_ ]]; then echo "· D2 결합 규칙 셀 — 재개 없음"""),
    ('L4_resume_all_no_name_guard', 'resume_all.sh',
     """  if [[ "$nm" =~ ^(npprobe[1-9][0-9]*_)?GM(cc|cu|uc|uu)_ ]] || grep -qF '★ D2 결합 규칙 (기하평균' "$d/in.mixer"; then echo "· D2 결합 규칙 셀 — 재개 없음""",
     """  if grep -qF '★ D2 결합 규칙 (기하평균' "$d/in.mixer"; then echo "· D2 결합 규칙 셀 — 재개 없음"""),
]
res = []
tmpd = os.path.join(HERE, 'tmp_launcher')
os.makedirs(tmpd, exist_ok=True)
for name, f, old, new in MUT:
    root = os.path.join(HERE, 'mutL', name)
    if os.path.isdir(root):
        shutil.rmtree(root)
    os.makedirs(os.path.join(root, 'dem_scripts'))
    os.symlink(os.path.join(W, 'scripts'), os.path.join(root, 'scripts'))
    os.symlink(os.path.join(W, 'dem_scripts', 'mixer_20260919'), os.path.join(root, 'dem_scripts', 'mixer_20260919'))
    shutil.copytree(L21, os.path.join(root, 'dem_scripts', 'mixer_20260921'))
    rec = dict(mutation=name)
    if f:
        p_ = os.path.join(root, 'dem_scripts', 'mixer_20260921', f)
        src = open(p_, encoding='utf-8').read()
        rec['occurrences'] = src.count(old)
        if rec['occurrences'] != 1:
            rec['status'] = 'NOT_APPLIED'
            res.append(rec)
            print(name, 'NOT APPLIED', rec['occurrences'])
            continue
        open(p_, 'w', encoding='utf-8').write(src.replace(old, new))
    p = subprocess.run(['bash', os.path.join(root, 'dem_scripts', 'mixer_20260921', 'test_launcher.sh')], capture_output=True, text=True,
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=tmpd, OPENBLAS_NUM_THREADS='1'), timeout=3000)
    out = p.stdout + p.stderr
    fails = [l.strip()[:140] for l in out.splitlines() if l.strip().startswith('✗')]
    tail = [l for l in out.splitlines() if 'test_launcher:' in l]
    rec.update(rc=p.returncode, n_fail=len(fails), fails=fails[:6], summary=tail[-1] if tail else out.strip().splitlines()[-1:])
    rec['status'] = 'CLEAN' if (name == 'CONTROL' and p.returncode == 0 and not fails) else (
        'KILLED' if (p.returncode != 0 or fails) else ('SURVIVED' if name != 'CONTROL' else 'DIRTY'))
    res.append(rec)
    print(f"{name:34s} {rec['status']:9s} rc={p.returncode} nfail={len(fails)} {rec['summary']} | {'; '.join(x[:60] for x in fails[:3])}")
    shutil.rmtree(root)
json.dump(res, open(os.path.join(HERE, 'probe_launcher_mutations.json'), 'w'), ensure_ascii=False, indent=1)
