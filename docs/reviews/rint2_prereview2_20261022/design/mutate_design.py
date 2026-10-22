"""Mutation tests on the registration-rule lines (4th edition) of the chain / S0 gate at 93d93bc02.

Each mutant = one exact string replacement (must occur exactly once) in one file of the worktree → run the owning test file →
record PASS count and failing check IDs → restore the original bytes (finally · sha256 check).
Run:  bash heavy.sh python3 -I mutate_design.py <worktree>      (writes mutate_design.json next to this file)
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import time

WT = sys.argv[1]
ONLY = sys.argv[2].split(',') if len(sys.argv) > 2 else None
CH = 'scripts/rint_r_chain.py'
S0 = 'scripts/ca_s0_census.py'
T_CH = 'scripts/test_rint_r_chain.py'
T_S0 = 'scripts/test_ca_s0_census.py'
MUT = [
    ('Ma_judge_set_NC_priority_off', CH, "        if 'NOT_COMPUTED' in bad:\n            return {'verdict': 'NOT_COMPUTED', 'state': 'calib'}\n",
     "        if False:\n            return {'verdict': 'NOT_COMPUTED', 'state': 'calib'}\n", T_CH),
    ('Mb_outside_band_ignores_e', CH, '    return s * (1.0 - e) >= X if lo else s * (1.0 + e) <= X\n', '    return s >= X if lo else s <= X\n', T_CH),
    ('Mc_edge_hit_ignores_e', CH, '    a, b = s * (1.0 - e), s * (1.0 + e)\n    if a <= T <= b:', '    a, b = s, s\n    if a <= T <= b:', T_CH),
    ('Md_end_origin_push_off', CH, "    lo = side == 'lo'\n    pushes, seen = 0, []\n", "    lo = side == 'lo'\n    return end, 0, []\n    pushes, seen = 0, []\n", T_CH),
    ('Me_states_differ_rule_off', CH, '    if states is not None and len(set(states)) > 1:\n        return False, sp\n',
     '    if False:\n        return False, sp\n', T_CH),
    ('Mf_W_pos_off', CH, '    W = W0 if (0.0 < W0 < math.inf) else (0.0 if w_pos is None else w_pos)\n', '    W = W0\n', T_CH),
    ('Mg_variant_NC_after_name', CH, "    if vJ['verdict'] == 'NOT_COMPUTED':\n        return (f'{V}_UNCHECKED', None,",
     "    if vJ['verdict'] == 'NOT_COMPUTED' and vJ['verdict'] == J['verdict']:\n        return (f'{V}_UNCHECKED', None,", T_CH),
    ('Mh_variant_own_origin_flag_off', CH, "    if 'CALIB_ORIGIN_SENSITIVE' in (vflags or ()):\n        return (f'{V}_UNCHECKED', False,",
     "    if False:\n        return (f'{V}_UNCHECKED', False,", T_CH),
    ('Mi_sentence_no_sens_suffix', CH, '    if sens_incomplete:\n        s += SENTENCE_JOIN + SENTENCE_SENS\n', '    if False:\n        s += SENTENCE_JOIN + SENTENCE_SENS\n', T_CH),
    ('Mj_sentence_no_point_suffix', CH, "    if state == 'point':\n        s += SENTENCE_JOIN + SENTENCE_POINT\n",
     "    if False:\n        s += SENTENCE_JOIN + SENTENCE_POINT\n", T_CH),
    ('Mk_sens_incomplete_never', CH, "                sens_incomplete = True                          # ⑰",
     "                sens_incomplete = False                         # ⑰", T_CH),
    ('Ml_grade_boundary_strict', CH, "    return 'PASS_INFORMATIVE' if W <= GRADE_INFORMATIVE_MAX else",
     "    return 'PASS_INFORMATIVE' if W < GRADE_INFORMATIVE_MAX else", T_CH),
    ('Mm_U_equals_E', CH, '    inU, inE = bool(in_law), lo <= x <= hi\n', '    inU, inE = lo <= x <= hi, lo <= x <= hi\n', T_CH),
    ('Mn_require_numbers_drop_scope', CH, "PLAN_REGISTERED_NUMBERS = ('max_ladder_points', 'calib_rj_ratio_max', 'sv_cf_threshold', 'sv_cf_scope')",
     "PLAN_REGISTERED_NUMBERS = ('max_ladder_points', 'calib_rj_ratio_max', 'sv_cf_threshold')", T_CH),
    ('Mn2_require_numbers_drop_scope_S0', CH, "PLAN_REGISTERED_NUMBERS = ('max_ladder_points', 'calib_rj_ratio_max', 'sv_cf_threshold', 'sv_cf_scope')",
     "PLAN_REGISTERED_NUMBERS = ('max_ladder_points', 'calib_rj_ratio_max', 'sv_cf_threshold')", T_S0),
    ('Mo_stage2_gate_no_numbers', S0, '            _rrc.require_plan_numbers(robj)\n', '            pass\n', T_S0),
    ('Mp_sv_on_in_variants', CH, "        scope = plan['sv_cf_scope'] if a.variant is None else None\n", "        scope = plan['sv_cf_scope']\n", T_CH),
    ('Mq_stop_at_e_lt_emin', CH, "            self.st['local_e_ge_emin'] = bool(e >= E_MIN)",
     "            self.st['local_e_ge_emin'] = bool(e >= E_MIN)\n            if e < E_MIN:\n                raise Stop('CALIB_UNIDENTIFIED', 'e < e_min')", T_CH),
    ('Mr_sv_threshold_ge', CH, '        elif threshold is not None and r_ > float(threshold):', '        elif threshold is not None and r_ >= float(threshold):', T_CH),
    ('Ms_variant_stop_rejects_all', CH, "    return s.get('status') == 'STOPPED' and s.get('variant') is None\n", "    return s.get('status') == 'STOPPED'\n", T_CH),
    ('Mt_end_candidate_unconfirmed', CH, '    end = cand if ok else lad._outer_neighbor(X, lo)\n', '    end = cand\n', T_CH),
    ('Mu_stage2_gate_no_tolff_cross', S0, "    if robj['tol_ff_um'] != plan['values_um']['tol_ff']:\n", "    if False:\n", T_S0),
    ('Mv_dbe_origin_threshold_0p2W', CH, 'ORIGIN_DBE_FRAC_W = 0.1 ', 'ORIGIN_DBE_FRAC_W = 0.2 ', T_CH),
    ('Mw_sbe_origin_0p04', CH, 'ORIGIN_SBE_MAX = 0.02 ', 'ORIGIN_SBE_MAX = 0.04 ', T_CH),
    ('Mx_plans_cross_rtol_off', CH, "    eqf('R 계획 step3_rtol ↔ §3-5 봉인 CERT_RTOL_MAX', plan.get('step3_rtol'), _cc.CERT_RTOL_MAX)\n", '', T_CH),
]
res = {}
for name, f, old, new, test in MUT:
    if ONLY and name not in ONLY:
        continue
    p = os.path.join(WT, f)
    orig = open(p, 'rb').read()
    txt = orig.decode('utf-8')
    n = txt.count(old)
    if n != 1:
        res[name] = {'error': f'old string occurs {n} times'}
        continue
    try:
        open(p, 'wb').write(txt.replace(old, new).encode('utf-8'))
        t0 = time.time()
        r = subprocess.run([sys.executable, os.path.join(WT, test)], cwd=WT, capture_output=True, text=True, timeout=1800)
        out = r.stdout + r.stderr
        fails = re.findall(r'^\s*FAIL\s+(\S+)', out, re.M)
        tail = [ln for ln in out.splitlines() if ln.strip()][-1:] if out else []
        res[name] = {'file': f, 'test': test, 'rc': r.returncode, 'caught': r.returncode != 0 or bool(fails),
                     'n_fail': len(fails), 'fail_ids': fails[:12], 'tail': tail, 'seconds': round(time.time() - t0, 1)}
    finally:
        open(p, 'wb').write(orig)
        assert hashlib.sha256(open(p, 'rb').read()).digest() == hashlib.sha256(orig).digest()
    print(name, json.dumps(res[name], ensure_ascii=False)[:300], flush=True)
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mutate_design.json')
prev = {}
if os.path.exists(path):
    prev = json.load(open(path, encoding='utf-8'))
prev.update(res)
json.dump(prev, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('DONE')
