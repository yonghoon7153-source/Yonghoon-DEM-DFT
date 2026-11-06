"""P8-01 — PC7-02 class through the AL07 exception (real chain path, fake runner).

Threat model = the one test PE02 itself uses (ledger clone reset before entry 1 + re-appended lines + one hand on the base folder).
PE02 keeps result line 1 "as is" (completed/stopped) and removes attempt.json -> now ATTEMPT_LEDGER_MISMATCH (fixed).
Here result line 1 is re-appended as a form-valid *rejected* line and an empty-ish attempt_1.rejected.json is placed next to the folder
(the AL07 shape) -> found_attempts_problem skips attempt_1 -> the seen-result attempt 1 disappears from every check -> attempt 2 adopted.

  python3 -I probe_p801_al07_exception.py <tree>
"""
import hashlib
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from probe_common import setup  # noqa: E402

RR, T = setup(sys.argv[1])


def hide(tag, d, n1, mode):
    lines = T.led_lines(d)
    e1 = [x for x in lines if x.get('kind') == 'entry' and x.get('n') == n1][0]
    r1 = [x for x in lines if x.get('kind') == 'result' and x.get('n') == n1][0]
    dr = T.led_reset_before(d, tag, f'rint-r attempt {n1} entry ')
    T.led_hand(dr, dict(e1, target='ladder:P0:FIBRE'), msg='entry 1 target only (probe)')
    if mode == 'as_is':
        T.led_hand(dr, r1, msg='result 1 as is (probe = PE02)')
    else:
        rej = {'kind': 'result', 'n': n1, 'status': 'rejected', 'stop': {'code': 'OUTDIR_NOT_EMPTY', 'run': None, 'reason': None},
               'side': 'pre', 'cause': 'presolve', 'resume_ok': False,
               'folder': (f'attempt_{n1}.rejected.json' if mode == 'rej_side' else f'attempt_{n1}'),
               'folder_sha256': hashlib.sha256(b'x').hexdigest(), 'by': 'chain', 'utc': r1['utc']}
        T.led_hand(dr, rej, msg='result 1 re-appended as rejected (probe)')
    return dr


def go():
    d, _rc, _so = T.led_new('P801')
    _r, n1, _s = T.led_add(d, 'ladder:P0')
    a = T.lad_att('P801', T.world('P801_a', dict(T.PW, faults=[{'do': 'illegal_driver_after_mark', 'match': {'rj': 'inf'}}])), d, n1)
    res1 = T.led_result(d, n1)
    rows = {'attempt1': {'rc': a['rc'], 'status': (a['sum'] or {}).get('status'), 'side': (res1 or {}).get('side'),
                         'result_status': (res1 or {}).get('status')}}
    for mode in ('as_is', 'rej_side', 'rej_infolder'):
        dr = hide(f'P801_{mode}', d, n1, mode)
        base = T.pc_copy_base(a['base'], f'P801_{mode}_base')
        (base / f'attempt_{n1}' / 'attempt.json').unlink()          # one hand on the folder (same as PE02 rm_attempt_json)
        if mode != 'as_is':
            (base / f'attempt_{n1}{RR.REJECTED_SIDE}').write_text('{}', encoding='utf-8')   # touch the AL07 side record
        add2 = T.led_add(dr, 'ladder:P0')
        b = T.lad_att(f'P801_{mode}_b', T.world(f'P801_{mode}_b'), dr, add2[1], base=base) if add2[1] else None
        v = T.ver_led(f'P801_{mode}_v', [b['out']], dr) if b else None
        vwhy = str((((v or {}).get('v') or {}).get('stop') or {}).get('cause'))
        _r3, n3, _s3 = T.led_add(dr, 'ladder:P1')
        c = T.lad_att(f'P801_{mode}_P1', T.world(f'P801_{mode}_c'), dr, n3, law='P1')
        _r4, n4, _s4 = T.led_add(dr, 'predict')
        wp = T.world(f'P801_{mode}_p')
        p = T.pred_att(f'P801_{mode}_pred', wp, dr, n4, [b['out'], c['out']]) if b else None
        rows[mode] = {'add2_rc': add2[0], 'b_status': ((b or {}).get('sum') or {}).get('status'),
                      'verdict_stop': T.stop_code(v) if v else None, 'verdict_names_attempt1': 'attempt_1' in vwhy,
                      'predict_stop': T.stop_code(p) if p else None, 'predict_status': ((p or {}).get('sum') or {}).get('status'),
                      'predict_runner_calls': T.n_calls(wp), 'ledger_tail': [x.get('kind') + ':' + str(x.get('n')) + ':' + str(x.get('status', ''))
                                                                            for x in T.led_lines(dr)]}
    return rows


rows = go()
print(json.dumps(rows, ensure_ascii=False, indent=1))
ok_control = rows['as_is']['verdict_stop'] == 'ATTEMPT_LEDGER_MISMATCH'
bypass = [m for m in ('rej_side', 'rej_infolder') if rows[m]['verdict_stop'] != 'ATTEMPT_LEDGER_MISMATCH']
print(f'\ncontrol (PE02 shape, result as-is) refused: {ok_control}')
print(f'bypass modes (verdict ledger check passed): {bypass}')
