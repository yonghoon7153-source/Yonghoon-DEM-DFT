#!/usr/bin/env python3
"""Probe for Q9 design rev 2 (9a72d65c6) §3-2 lazy unit check + §3-5 adoption vs the one-machine chain.

A unit = (c, law, R) = corner run (first) + origin run (second) on one machine.  Adoption (§3-5) = first COMPLETED attempt in
ledger order, all earlier attempts must be pre-result; a post-result stop before it → "그 단위의 결과 = 그 멈춤".
Lazy check (§3-2) = adoption is decided when the recompute FIRST requests a run of that unit.

The chain world raises each stop at the run where it happened.  The literal merge raises a unit's stop at the unit's first request.
Both use the REAL Predict (current order; no overflow here, so current = new order per S0 of order_probe).
"""
import json
import sys

sys.path.insert(0, sys.argv[1])
import rint_r_chain as C  # noqa: E402
sys.path.insert(0, sys.argv[2])
from order_probe_lib import LAD, arm, base_arm0  # noqa: E402


def unit_of(role, law, c, rr):
    if role == 'sbe_noop':
        return f'noop_{law}'
    if role in ('corner', 'origin'):
        return f'u_c{c}_{law}_{rr}'
    return f'x_{law}_c{c}_{rr}'


# attempts[unit] = list of attempts; attempt = {'end': 'complete'} | {'end': 'stop', 'at': role, 'code': ..., 'payload': bool}
ATTEMPTS = {
    'u_c0_P0_R_j0': [{'end': 'stop', 'at': 'origin', 'code': 'NOT_COMPUTED', 'payload': True}],     # corner R01 ok, origin R02 → NOT_COMPUTED
    'u_c1_P1_R_j_hi': [{'end': 'stop', 'at': 'corner', 'code': 'ARM_CONTRACT', 'payload': True}],   # corner R01 → contract defect
}


def chain_fetch_factory(log):
    def fetch(kit, role, law, c, rj, arms, sv_cf=False):
        rr = {v: k for k, v in LAD[law].items() if k != 'r0_sigma'}[rj]
        log.append((role, law, c, rr))
        u = unit_of(role, law, c, rr)
        for a in ATTEMPTS.get(u, []):
            if a['end'] == 'stop' and a['at'] == role:
                raise C.Stop(a['code'], f'{u} {role}', f'req{len(log)}')
        a0 = base_arm0()[(c, law, rr)] if role != 'sbe_noop' else LAD[law]['r0_sigma']
        if role == 'sbe_noop':
            return [arm(a0)]
        return [arm(a0)] if role == 'corner' else [arm(a0), arm(a0)]
    return fetch


def merge_fetch_factory(log, unused):
    adopted = {}

    def fetch(kit, role, law, c, rj, arms, sv_cf=False):
        rr = {v: k for k, v in LAD[law].items() if k != 'r0_sigma'}[rj]
        log.append((role, law, c, rr))
        u = unit_of(role, law, c, rr)
        if u not in adopted:                                   # §3-2 lazy: decide adoption at the unit's FIRST request
            res = 'complete'
            for a in ATTEMPTS.get(u, [{'end': 'complete'}]):
                if a['end'] == 'complete':
                    res = 'complete'
                    break
                pre = not a['payload']                          # §3-5 rev 2: pre-result = no payload + runner stop record
                if pre:
                    continue
                res = a                                         # post-result stop first → "그 단위의 결과 = 그 멈춤"
                break
            adopted[u] = res
        if adopted[u] != 'complete':
            a = adopted[u]
            raise C.Stop(a['code'], f'unit {u} result = its stop (adoption at first request)', f'req{len(log)}')
        a0 = base_arm0()[(c, law, rr)] if role != 'sbe_noop' else LAD[law]['r0_sigma']
        if role == 'sbe_noop':
            return [arm(a0)]
        return [arm(a0)] if role == 'corner' else [arm(a0), arm(a0)]
    return fetch


def run(fetch):
    pr = C.Predict(fetch, LAD, None, sv_scope=None)
    try:
        pr.run()
        return 'PREDICTED', None, None
    except C.Stop as e:
        return (e.code if e.code in C.PREDICT_OUTCOMES else 'STOPPED'), e.code, e.run


lc, lm = [], []
rc = run(chain_fetch_factory(lc))
rm = run(merge_fetch_factory(lm, None))
units_never_requested_in_merge = sorted({unit_of(*x) for x in lc} - {unit_of(*x) for x in lm})
res = {'chain': {'status': rc[0], 'stop': rc[1], 'at': rc[2], 'runs': len(lc)},
       'merge_literal': {'status': rm[0], 'stop': rm[1], 'at': rm[2], 'runs': len(lm)},
       'units_requested_by_chain_not_by_merge': units_never_requested_in_merge}
print(json.dumps(res, ensure_ascii=False, indent=1))
