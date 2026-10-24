#!/usr/bin/env python3
"""Round-4 probe — what a 'signal 9' attempt leaves behind with the CURRENT runner shape.

Mimics `scripts/sdcp_gain_vox015_8arm.sh` run_arm (4040e4388 lines 691–890): the payload process runs inside `( cd "$RUN" && bash arm.sh )`,
writes `$RUN/<out>.part` → `os.replace` → `$RUN/<out>` (= the kit run folder, OUTSIDE the attempt folder), then the runner runs the check and
only then `mv "$FRESH" "$OUT"` into OUTDIR (inside the attempt folder).  The chain calls `subprocess.run(['bash', runner], timeout=left)`
(`rint_r_chain.Runner.run`), whose timeout path sends SIGKILL to the bash PID only.

Two cases (no GPU · a 2 s sleep stands in for the solve):
  T  chain TIME_LIMIT: subprocess.run(timeout=0.5) → bash killed (rc of the child seen by the parent = -9) → does the payload still appear in $RUN?
  K  operator `kill -9 <runner bash pid>` during the solve → same question.
Expectation by the design's L119 rule: attempt folder has no p2_*.json and the recorded cause is 'signal 9' → 결과 전.
"""
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

root = Path(tempfile.mkdtemp(prefix='orphan_probe_', dir=sys.argv[1] if len(sys.argv) > 1 else None))
RUN = root / 'kit' / 'run_0001'
RUN.mkdir(parents=True)
ATT = root / 'attempt_U_1'
OUTDIR = ATT / 'P01_corner_arm1'
OUTDIR.mkdir(parents=True)
(RUN / 'arm.sh').write_text(
    'python3 -c "import time, json, os; time.sleep(2.0); '
    "open('p2_DBE_a0.json.part','w').write(json.dumps({'step3': {'sigma_e_eff_S_cm': 0.004680000001}})); "
    "os.replace('p2_DBE_a0.json.part', 'p2_DBE_a0.json')\"\n")
runner = root / 'runner.sh'
runner.write_text(f'set -uo pipefail\n( cd "{RUN}" && bash arm.sh ) || exit 1\n'
                  f'python3 -c "import time; time.sleep(0.2)"   # stands in for --check-arm\n'
                  f'mv "{RUN}/p2_DBE_a0.json" "{OUTDIR}/p2_DBE_a0.json"\n')


def state():
    return {'attempt_folder_payloads': sorted(str(p.relative_to(ATT)) for p in ATT.rglob('p2_*.json')),
            'kit_run_folder_payloads': sorted(p.name for p in RUN.glob('p2_*'))}


res = {}
# T — chain timeout path
t0 = time.time()
try:
    subprocess.run(['bash', str(runner)], timeout=0.5)
    res['T'] = {'timeout': False}
except subprocess.TimeoutExpired:
    res['T'] = {'timeout': True, 'seconds_to_return': round(time.time() - t0, 2), 'right_after': state()}
time.sleep(3.0)
res['T']['after_3s'] = state()
for p in RUN.glob('p2_*'):
    p.unlink()
# K — operator kill -9 on the runner bash
pr = subprocess.Popen(['bash', str(runner)])
time.sleep(0.5)
os.kill(pr.pid, signal.SIGKILL)
rc = pr.wait()
res['K'] = {'returncode_seen_by_chain': rc, 'right_after': state()}
time.sleep(3.0)
res['K']['after_3s'] = state()
res['tmp'] = str(root)
print(json.dumps(res, ensure_ascii=False, indent=1))
