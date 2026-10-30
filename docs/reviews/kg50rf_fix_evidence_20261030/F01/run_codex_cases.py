"""Codex KG50RF-01 사례 폴더 여섯 (읽기만) 에 resume_ckpt.sh -C — 사례 · rc · 문제 줄 (KG50R-F01) · 마지막 줄.
   python3 -I run_codex_cases.py <도구> <사례 폴더 위> <작업 폴더>"""
import os
import subprocess
import sys

tool, base, work = sys.argv[1:4]
CASES = (('d2_drop_intermediate_variable_definition', 'restart_kg50_d2_b50/restart_settling_20001.bin', 20001),
         ('d2_runtime_dependent_eager_variable', 'restart_kg50_d2_b50/restart_settling_20001.bin', 20001),
         ('drop_intermediate_variable_definition', 'restart_settling_50.bin', 50),
         ('runtime_dependent_eager_variable', 'restart_settling_50.bin', 50),
         ('d2_received_baseline', 'restart_kg50_d2_b50/restart_settling_20001.bin', 20001),
         ('archived_after_settling_baseline', 'restart_kg50_d07_b40/restart_after_settling.bin', 200001))
os.makedirs(work, exist_ok=True)
for name, ck, s0 in CASES:
    d = os.path.join(base, name)
    p = subprocess.run(['bash', tool, '-C', os.path.join(d, 'main.liggghts'), os.path.join(d, 'resume.liggghts'), ck, str(s0), work],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
    out = p.stdout.decode('utf-8', 'replace').splitlines()
    print('== %s  rc=%d  %s' % (name, p.returncode, out[-1].strip() if out else ''))
    for l in out:
        if 'KG50R-F01' in l:
            print('   ' + l.strip()[:400])
