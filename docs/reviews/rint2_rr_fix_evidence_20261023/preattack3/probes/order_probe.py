#!/usr/bin/env python3
"""Probe for Q9 design rev 2 (9a72d65c6) — order / priority / lazy-merge claims.

Uses the REAL rint_r_chain.Predict (current order) and a simulated "new order" (§2 ①–④ of the design)
built only from the real helper functions (dbe_origin_ok, origin_points, r_monotone_problem, arm_band,
_r_monotone).  No solver, no runner.  Fake arm records only.

Usage: python3 -I order_probe.py <tree>/scripts
"""
import json
import sys

sys.path.insert(0, sys.argv[1])
import rint_r_chain as C  # noqa: E402

LAD = {law: {'R_j0': '1000000.0', 'R_j_lo': '500000.0', 'R_j_hi': '2000000.0', 'r0_sigma': 1.0e-3} for law in C.LAWS}
E = 1e-6


def arm(sig, state='positive'):
    return {'sigma': sig, 'state': state, 'err_rel': E, 'target_lo': sig * (1 - E), 'target_hi': sig * (1 + E), 'scale': 1.0,
            'n_sdcp_near': 0, 'sv_cf': None}


class World:
    """arm0 table + over corners + injected stops.  stops[(role, law, c, rr)] = code (raised as Stop when that run is requested)."""

    def __init__(self, arm0, over=(), stops=None):
        self.arm0, self.over, self.stops = arm0, set(over), dict(stops or {})
        self.log = []

    def fetch(self, kit, role, law, c, rj, arms, sv_cf=False):
        rr = {v: k for k, v in LAD[law].items() if k != 'r0_sigma'}[rj]
        self.log.append((role, law, c, rr))
        code = self.stops.get((role, law, c, rr))
        if code:
            raise C.Stop(code, f'injected at {role} {law} c{c} {rr}', f'run{len(self.log)}')
        if role == 'sbe_noop':
            return [dict(arm(LAD[law]['r0_sigma']))]
        a0 = self.arm0[(c, law, rr)]
        if role == 'corner':
            return [arm(a0)]
        if role == 'origin':
            f = 1.05 if (law, c) in self.over else 1.0
            return [arm(a0 * f), arm(a0)]
        if role == 'origin8':
            f = 1.05 if (law, c) in self.over else 1.0
            return [arm(a0)] + [arm(a0 * f)] + [arm(a0)] * 6
        raise AssertionError(role)


def run_current(world):
    pr = C.Predict(world.fetch, LAD, None, sv_scope=None)
    try:
        pr.run()
        st = ('PREDICTED', None, None)
    except C.Stop as e:
        st = (e.code if e.code in C.PREDICT_OUTCOMES else 'STOPPED', e.code, e.cause)
    return st, list(world.log), pr


def run_new(world):
    """§2 new order: ① origin samples all (law → c) ② early monotone (existing points) ③ origin8 (law → c) ④ final _r_monotone."""
    pr = C.Predict(world.fetch, LAD, None, sv_scope=None)
    early = []
    try:
        # — identical prefix (no-op · corners · same_p · W0) — copy of Predict.run lines
        for law in C.LAWS:
            r = pr.fetch(C.SBE_KIT, 'sbe_noop', law, '1', LAD[law]['R_j0'], 1)[0]
            ok = r['sigma'] == LAD[law]['r0_sigma'] and r['n_sdcp_near'] == 0
            pr.checks['sbe_noop'].append({'law': law, 'ok': ok})
            if not ok:
                raise C.Stop('SAME_P_CONSISTENCY', 'noop')
        for law in C.LAWS:
            for rr in C.RJ_ROLES:
                for c in C.CS:
                    pr.vals[(c, law, rr)] = pr.fetch(C.DBE_KIT, 'corner', law, c, LAD[law][rr], 1, False)[0]
                d = C.ln_diff(pr.vals[('0', law, rr)]['sigma'], pr.vals[('1', law, rr)]['sigma'])
                ok = d >= -C.TAU_MONO
                pr.checks['same_p'].append({'law': law, 'rj_role': rr, 'ok': ok})
                if not ok:
                    raise C.Stop('SAME_P_CONSISTENCY', 'same_p')
        W0 = C.ln_spread([v['sigma'] for v in pr.vals.values()])
        Wp = C.w_pos_of([v['sigma'] for v in pr.vals.values()])
        pr.sealed['W0'], pr.sealed['W_pos'] = W0, Wp
        # ① origin samples all
        overc = []
        for law in C.LAWS:
            for c in C.CS:
                ent = {'c': c, 'law': law, 'status': 'pass', 'arm_list': list(C.ORIGIN_ARMS), 'per_R': {}, 'states_differ': []}
                over = False
                for rr in C.ORIGIN_CHECK_ROLES:
                    a0r = pr.vals[(c, law, rr)]
                    r12 = pr.fetch(C.DBE_KIT, 'origin', law, c, LAD[law][rr], C.ORIGIN_ARMS)
                    pr.org[(c, law, rr)] = dict([('corner_a0', a0r)] + [(f'origin_a{i}', x) for i, x in zip(C.ORIGIN_ARMS, r12)])
                    vv = [a0r['sigma']] + [x['sigma'] for x in r12]
                    sts = [a0r.get('state', 'positive')] + [x.get('state', 'positive') for x in r12]
                    ok, sp = C.dbe_origin_ok(vv, W0, states=sts, w_pos=Wp)
                    ent['per_R'][rr] = 'pass' if ok else 'over'
                    over = over or not ok
                if over:
                    ent['status'] = 'adjusted'
                    overc.append((law, c))
                pr.origin.append(ent)
        # ② early monotone (existing points only — §3-2: non-over corner estimator (arm0) + every corner's corner_a0/a1/a2)
        for law in C.LAWS:
            for c in C.CS:
                if (law, c) not in overc:
                    pts = [(C.rj_float(LAD[law][rr]), rr, C.arm_band(pr.vals[(c, law, rr)])) for rr in C.RJ_ROLES]
                    bad = C.r_monotone_problem(pts)
                    early.append({'law': law, 'c': c, 'what': 'arm0', 'ok': bad is None})
                    if bad is not None:
                        raise C.Stop('R_MONOTONE_VIOLATION', f'early {law} c{c} estimator {bad}')
                for n, p in C.origin_points(pr, law, c):
                    bad = C.r_monotone_problem(p)
                    early.append({'law': law, 'c': c, 'what': n, 'ok': bad is None})
                    if bad is not None:
                        raise C.Stop('R_MONOTONE_VIOLATION', f'early {law} c{c} origin {n} {bad}')
        # ③ origin8 for over corners (law → c)
        for (law, c) in overc:
            for rr in C.RJ_ROLES:
                r8 = pr.fetch(C.DBE_KIT, 'origin8', law, c, LAD[law][rr], 8)
                pr.adj[(c, law, rr)] = C.mean_ext([x['sigma'] for x in r8])
                pr.adj_band[(c, law, rr)] = C.mean_band(r8)
                pr.org[(c, law, rr)].update((f'origin8_a{i}', x) for i, x in enumerate(r8))
        # ④ final monotone (unchanged)
        pr._r_monotone()
        st = ('PREDICTED', None, None)
    except C.Stop as e:
        st = (e.code if e.code in C.PREDICT_OUTCOMES else 'STOPPED', e.code, e.cause)
    return st, list(world.log), pr, early


def base_arm0(nonmono_p0c1=False):
    t = {('0', 'P0', 'R_j_lo'): 4.40e-3, ('0', 'P0', 'R_j0'): 4.35e-3, ('0', 'P0', 'R_j_hi'): 4.30e-3,
         ('1', 'P0', 'R_j_lo'): 4.62e-3, ('1', 'P0', 'R_j0'): 4.60e-3, ('1', 'P0', 'R_j_hi'): 4.45e-3,
         ('0', 'P1', 'R_j_lo'): 4.10e-3, ('0', 'P1', 'R_j0'): 4.05e-3, ('0', 'P1', 'R_j_hi'): 4.00e-3,
         ('1', 'P1', 'R_j_lo'): 4.20e-3, ('1', 'P1', 'R_j0'): 4.15e-3, ('1', 'P1', 'R_j_hi'): 4.10e-3}
    if nonmono_p0c1:
        t[('1', 'P0', 'R_j_lo')] = 4.50e-3          # R_lo σ < R_0 σ (4.60) → R monotone contradiction (bands ±1e-6)
    return t


def show(name, cur, new):
    (sc, lc, _), (sn, ln, _, early) = cur, new
    print(f'== {name}')
    print(f'   current : status={sc[0]:<12} stop={sc[1]!s:<22} runs={len(lc)}')
    print(f'   new     : status={sn[0]:<12} stop={sn[1]!s:<22} runs={len(ln)}  early_checks={len(early)}')
    same_seq = lc == ln
    print(f'   same request sequence: {same_seq}  · same outcome: {sc[:2] == sn[:2]}')
    return {'name': name, 'current': {'status': sc[0], 'stop': sc[1], 'runs': len(lc)},
            'new': {'status': sn[0], 'stop': sn[1], 'runs': len(ln), 'early_checks': len(early)},
            'same_sequence': same_seq, 'same_outcome': sc[:2] == sn[:2]}


out = []
# S0 — no overflow, all fine → identical
out.append(show('S0 no-overflow all-pass', run_current(World(base_arm0())), run_new(World(base_arm0()))))
# S0b — no overflow, arm0 monotone contradiction in (P0,c1) → same stop, same runs; checks['r_monotone'] content differs
cur = run_current(World(base_arm0(True)))
new = run_new(World(base_arm0(True)))
r = show('S0b no-overflow monotone-contradiction', cur, new)
r['current_checks_r_monotone'] = cur[2].checks['r_monotone']
r['new_checks_r_monotone'] = new[2].checks['r_monotone']
print('   current checks[r_monotone] =', cur[2].checks['r_monotone'])
print('   new     checks[r_monotone] =', new[2].checks['r_monotone'], '(early check recorded elsewhere)')
out.append(r)
# S1 (documented §4) — (P0,c0) over, its first origin8 run NOT_COMPUTED; (P0,c1) non-over arm0 monotone contradiction
w = dict(over={('P0', '0')}, stops={('origin8', 'P0', '0', 'R_j_lo'): 'NOT_COMPUTED'})
out.append(show('S1 origin8 NOT_COMPUTED vs early monotone', run_current(World(base_arm0(True), **w)),
                run_new(World(base_arm0(True), **w))))
# S2 (not in §4/§7) — (P0,c0) over, origin8 NOT_COMPUTED; (P1,c1) origin sample run = ARM_CONTRACT (defect)
w = dict(over={('P0', '0')}, stops={('origin8', 'P0', '0', 'R_j_lo'): 'NOT_COMPUTED', ('origin', 'P1', '1', 'R_j_lo'): 'ARM_CONTRACT'})
out.append(show('S2 origin8 NOT_COMPUTED vs later origin-sample defect', run_current(World(base_arm0(), **w)),
                run_new(World(base_arm0(), **w))))
# S2r — swapped: origin8 (P0,c0) = ARM_CONTRACT (defect) · (P1,c1) origin sample = NOT_COMPUTED
w = dict(over={('P0', '0')}, stops={('origin8', 'P0', '0', 'R_j_lo'): 'ARM_CONTRACT', ('origin', 'P1', '1', 'R_j_lo'): 'NOT_COMPUTED'})
out.append(show('S2r origin8 defect vs later origin-sample NOT_COMPUTED', run_current(World(base_arm0(), **w)),
                run_new(World(base_arm0(), **w))))
# S3 — overflow, no stops → same outcome, different request order
w = dict(over={('P0', '0')})
out.append(show('S3 overflow all-pass', run_current(World(base_arm0(), **w)), run_new(World(base_arm0(), **w))))

print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
