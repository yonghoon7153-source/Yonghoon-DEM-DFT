import os
import sys
import tempfile
sys.path.insert(0, '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1a2386b8dc655b22/scripts')
import test_ca_ext_b6 as B6  # noqa: E402

td = tempfile.mkdtemp(prefix='dbgshift_', dir='/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/y2')
B6.make_fixture(td, sdcp=False)
for extra in (B6.OFF + B6.LEAN2 + ['--step3-origin-shift', '0', '0', '0.5'],
              B6.OFF + B6.LEAN2 + B6.CJ + ['--step3-rtol', '1e-12', '--step3-origin-shift', '0', '0', '0.5']):
    rc, log, d = B6.run_payload(td, extra, out='x.json')
    print('RC', rc)
    print('\n'.join(ln for ln in log.splitlines() if any(t in ln for t in ('REFUSED', 'ABORT', 'Error', 'error', 'CJUNC', 'reject', 'EVID', '거부', 'STEP3', 'exit'))) [-3000:])
    print('-----')
