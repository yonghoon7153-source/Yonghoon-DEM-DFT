"""Probe C — registration R §10 stop "단계마다 코드 (사슬 · 러너) 가 다르다 (CODE_PIN_MISMATCH)" vs the chain's actual check.

Uses the repository's own fake-runner harness (scripts/test_rint_r_chain.py: fixtures · s_main · s_main_predict · verdict) at 93d93bc02.
(1) clean tree: ladders P0 · P1 + main predict + main verdict  → V1
(2) the verdict process then runs DIFFERENT code with the SAME git HEAD:
    (a) the file scripts/rint_r_chain.py gets one appended comment line (working tree dirty · git_identity dirty True)
    (b) the in-memory grade threshold GRADE_INFORMATIVE_MAX is changed (a 'local edit' of the grading rule)
    → verdict V2 on the same stage folders.  Does the chain stop (CODE_PIN_MISMATCH) or publish?
The file is restored in `finally` (byte-identical check printed).
Run:  python3 -I probe_C_code_pin.py <worktree>      (writes probe_C_code_pin.json · ~30 s)
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

WT = sys.argv[1]
sys.path.insert(0, os.path.join(WT, 'scripts'))
import rint_r_chain as RR  # noqa: E402
import test_rint_r_chain as TM  # noqa: E402

CHAIN = os.path.join(WT, 'scripts', 'rint_r_chain.py')
orig = open(CHAIN, 'rb').read()
OUT = {}
TM.RR = RR
TM.TD = tempfile.mkdtemp(prefix='probeC_')
try:
    TM.fixtures()
    v1 = TM.s_verdict_main()
    OUT['V1_clean'] = {'rc': v1['rc'], 'verdict': (v1['v'] or {}).get('verdict'), 'flags': (v1['v'] or {}).get('flags'),
                       'W': (v1['r'] or {}).get('W')}
    lsum = TM.s_main('P0')['sum']
    OUT['ladder_code_record'] = lsum['code']['chain']
    # (2a) dirty working tree, same HEAD
    with open(CHAIN, 'ab') as f:
        f.write(b'\n# probe C: local edit (same HEAD, dirty tree)\n')
    OUT['git_identity_now'] = RR.git_identity(CHAIN)
    # (2b) local edit of the grading threshold in the verdict process
    old = RR.GRADE_INFORMATIVE_MAX
    RR.GRADE_INFORMATIVE_MAX = 0.05
    v2 = TM.verdict('ver_main_dirty', TM.main_dirs())
    RR.GRADE_INFORMATIVE_MAX = old
    OUT['V2_dirty_same_HEAD'] = {'rc': v2['rc'], 'verdict': (v2['v'] or {}).get('verdict'), 'stop': (v2['v'] or {}).get('stop'),
                                 'W': (v2['r'] or {}).get('W'), 'flags': (v2['v'] or {}).get('flags')}
    OUT['same_code(head equal, dirty differs)'] = RR.same_code({'head': 'H', 'dirty': False}, {'head': 'H', 'dirty': True})
finally:
    open(CHAIN, 'wb').write(orig)
    OUT['restored_byte_identical'] = hashlib.sha256(open(CHAIN, 'rb').read()).hexdigest() == hashlib.sha256(orig).hexdigest()
    shutil.rmtree(TM.TD, ignore_errors=True)
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe_C_code_pin.json')
json.dump(OUT, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
print(json.dumps(OUT, ensure_ascii=False, indent=1, default=str)[:3000])
