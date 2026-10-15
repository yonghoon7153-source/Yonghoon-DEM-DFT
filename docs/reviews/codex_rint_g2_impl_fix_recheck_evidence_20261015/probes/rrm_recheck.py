"""Independent, read-only RRM closure probes for pinned 2026-10-15 snapshot."""
import contextlib
import copy
import importlib.util
import io
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
NEW = ROOT / 'rint_g2_impl_reverify_20261015'
sys.path[:0] = [str(NEW / 'source/scripts'),
               str(ROOT / 'gen2_network_reverify3_20261007/deps'),
               str(ROOT / 'lhs_coverage_review_20260930/deps')]
import numpy as np
import step3_sigma as S3
import rint_rrm_reference as RRM
import test_rint_g2_rrm as FIX
FIX.S3 = S3
FIX.RRM = RRM

def quiet(fn, *args, **kwargs):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*args, **kwargs)

def fp(q):
    q['fp_rows'] = S3._iface_rows_fp(q['axes'])
    return q

def trycall(fn):
    try:
        value = fn()
        return {'accepted': True, 'value': value}
    except Exception as e:
        return {'accepted': False, 'error': type(e).__name__ + ': ' + str(e)}

def result_fields(ans):
    return {k: ans.get(k) for k in ('sigma_eff', 'unconverged', 'resid')}

def baseline_and_old():
    path = ROOT / 'rint_g2_impl_review_20261014/probes/rrm_probe.py'
    # Import target modules first; old probe's path insertion cannot replace them.
    spec = importlib.util.spec_from_file_location('old_rrm_probe', path)
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    assert old.S3 is S3 and old.RRM is RRM
    assert pathlib.Path(RRM.__file__).is_relative_to(NEW / 'source')
    return {'rrm': old.rrm(), 'geometry': old.geometry(), 'areas': old.areas()}

def mutations():
    sid, _, led = quiet(FIX.bed, FIX.A_C, FIX.A_R, FIX.A_T, FIX.A_LO, FIX.A_HI, FIX.A_VOX, FIX.A_BR)
    p = RRM.rrm_plan(led, FIX.RT, resolve_k=4.)
    kw = dict(z_bot_um=0., z_top_um=FIX.A_HI[2], return_field=True)
    muts = {}
    q = copy.deepcopy(FIX.with_rows(p, lambda ax, lin, cut: not cut))
    q['record']['iface_rrm']['resolve_k'] = 5.
    muts['removed_cut_k_5'] = q
    q = copy.deepcopy(FIX.with_rows(p, lambda ax, lin, cut: not cut))
    q['record']['iface_r_type_ohm_cm2'] = {}
    muts['removed_cut_rtable_empty'] = q
    q = copy.deepcopy(FIX.with_rows(p, lambda ax, lin, cut: False))
    q['record']['iface_rrm']['resolve_k'] = 5.
    q['record']['iface_rrm']['n_reference'] = 0
    q['record']['iface_rrm']['contacts'] = []
    q['realized'][:] = False
    muts['all_rows_empty_k_5'] = q
    q = copy.deepcopy(q)
    q['record']['iface_rrm']['resolve_k'] = 4.
    q['record']['iface_r_type_ohm_cm2'] = {}
    muts['all_rows_empty_rtable_empty'] = q
    for name, value in [('nan', np.nan), ('inf', np.inf), ('negative_inf', -np.inf), ('negative', -.001), ('zero_unregistered', 0.)]:
        q = copy.deepcopy(p)
        for a in q['axes']:
            a['rface'][~a['cut']] = value
        muts['film_' + name] = fp(q)
    for name, value in [('zero', 0.), ('negative', -1.), ('nan', np.nan), ('inf', np.inf), ('bool', True), ('string', 'oops')]:
        q = copy.deepcopy(p)
        q['record']['iface_rrm']['resolve_k'] = value
        muts['recipe_k_' + name] = q
    for key in ('iface_rrm', 'iface_r_type_ohm_cm2', 'iface_exception_law'):
        q = copy.deepcopy(p)
        q['record'].pop(key)
        muts['record_missing_' + key] = q
    for name, value in [('nan', np.nan), ('negative', -1.), ('inf', np.inf)]:
        q = copy.deepcopy(p)
        q['record']['iface_r_type_ohm_cm2'] = {'AM_S|AM_S': value}
        muts['recipe_r_' + name] = q
    q = copy.deepcopy(p)
    q['record']['iface_exception_law']['gap'] = 'silent_fallback'
    muts['recipe_law_unknown'] = q
    for key, value in [('rface', .001), ('ck', 21)]:
        q = copy.deepcopy(p)
        for a in q['axes']:
            a[key][a['cut']] = value
        muts['cut_' + key + '_nonzero'] = fp(q)
    q = copy.deepcopy(p)
    for a in q['axes']:
        a['cid'][~a['cut']] = 3
    muts['cid_outside'] = fp(q)

    out = {}
    original_planner = RRM.rrm_plan
    for name, q in muts.items():
        full = RRM.rrm_check(q, led)
        # Make replay tautologically pass to isolate checks 1-3 from planner replay.
        RRM.rrm_plan = lambda *a, _q=q, **k: _q
        try:
            independent = RRM.rrm_check(q, led)
        finally:
            RRM.rrm_plan = original_planner
        with FIX.direct_solver():
            wrapped = trycall(lambda q=q: result_fields(quiet(RRM.rrm_solve, sid, FIX.te(), FIX.A_VOX, q, led, **kw)))
        out[name] = {'full': full, 'independent_without_replay': independent, 'wrapper': wrapped}
        assert full and independent and not wrapped['accepted'], name

    rejected_plans = {}
    for name, table, k in [('unresolved', FIX.RT, 5.), ('missing_r', {}, 4.)]:
        q = RRM.rrm_plan(led, table, resolve_k=k)
        intact_check = RRM.rrm_check(q, led)
        wrapped = trycall(lambda q=q: quiet(RRM.rrm_solve, sid, FIX.te(), FIX.A_VOX, q, led, **kw))
        cleared = copy.deepcopy(q)
        cleared['rejections'] = []
        cleared['record']['iface_rejections'] = []
        rejected_plans[name] = {'intact_check': intact_check, 'intact_wrapper': wrapped,
                               'cleared_rejections_check': RRM.rrm_check(cleared, led)}
        assert not intact_check and not wrapped['accepted'] and rejected_plans[name]['cleared_rejections_check']

    zero = RRM.rrm_plan(led, {'AM_S|AM_S': 0.}, resolve_k=4.)
    with FIX.direct_solver():
        zero_solve = result_fields(quiet(RRM.rrm_solve, sid, FIX.te(), FIX.A_VOX, zero, led, **kw))
    return {'mutation_count': len(muts), 'mutations': out, 'excluded_plans': rejected_plans,
            'registered_zero': {'check': RRM.rrm_check(zero, led), 'solve': zero_solve},
            'generic_direct': direct_guard(sid, led, p, kw)}

def direct_guard(sid, led, p, kw):
    out = {}
    cnc = S3.am_iface_plan(led, FIX.RT)
    for family, original in [('rrm', p), ('cnc', cnc)]:
        rows = {}
        for name, value in [('normal', None), ('nan', np.nan), ('negative', -.001)]:
            q = copy.deepcopy(original)
            if value is not None:
                for a in q['axes']:
                    a['rface'][~a['cut']] = value
                fp(q)
            gate = trycall(lambda: S3.iface_require_quantitative(q, sid, FIX.te(), vox=FIX.A_VOX) is q)
            with FIX.direct_solver():
                solve = trycall(lambda: result_fields(quiet(S3.solve_sigma_z, sid, FIX.te(), FIX.A_VOX, iface=q, **kw)))
            rows[name] = {'gate': gate, 'solve': solve}
        out[family] = rows
    return out

def summaries_and_boundary():
    sid, pid, led = quiet(FIX.bed, FIX.A_C, FIX.A_R, FIX.A_T, FIX.A_LO, FIX.A_HI, FIX.A_VOX, FIX.A_BR)
    csid = sid.copy()
    csid[:10, :, :][np.isin(csid[:10, :, :], (1, 2))] = 3
    lc = S3.am_iface_ledger(FIX.A_C, FIX.A_R, FIX.A_T, csid, sid, FIX.A_LO, FIX.A_VOX,
                            delta_bound_um=0., bridge_um=FIX.A_BR)
    out = {}
    for tag, s, l in [('baseline', sid, led), ('carbon_half', csid, lc)]:
        p = RRM.rrm_plan(l, FIX.RT, resolve_k=4.)
        with FIX.direct_solver():
            ans = quiet(RRM.rrm_solve, s, FIX.te(), FIX.A_VOX, p, l,
                        z_bot_um=0., z_top_um=FIX.A_HI[2], return_field=True)
        share, total = S3.phase_current_share(ans, s, FIX.te(), return_total=True)
        currents = S3.per_particle_current(ans, s, pid, FIX.te(), 2)
        summary = p['record']['iface_contact_ledger']
        cncs = p['record']['iface_cnc_comparison']['iface_contact_ledger']
        out[tag] = {'summary': summary, 'solve_summary': ans['iface']['iface_contact_ledger'],
                    'cnc_summary': cncs, 'rface_c': p['rface_c'], 'carbon_cover': p['carbon_cover'],
                    'iface_carbon_cover_status': p['record']['iface_carbon_cover_status'],
                    'realized': p['realized'].tolist(), 'row_G': S3.iface_plan_film_G_S(p).tolist(),
                    'record_json_serializable': trycall(lambda: bool(json.dumps(ans['iface']))),
                    'phase_current_share': share, 'phase_share_sum': float(sum(share.values())),
                    'dissipation_total': total, 'per_particle_current': currents.tolist(),
                    'solve': result_fields(ans)}
        assert set(summary['film_G_S_total']) == {'rrm'}
        assert set(summary['rface_ohm_cm2']) == {'rrm'}
        assert summary['film_G_S_total']['rrm'] == sum(out[tag]['row_G'])
        assert set(cncs['film_G_S_total']) == {'remove_area', 'renormalize'}
        assert p['rface_c'] is None and p['carbon_cover'] is None

    a = RRM.contact_disc(FIX.A_C[0], FIX.A_R[0], FIX.A_C[1], FIX.A_R[1])['a']
    edge = a / FIX.A_VOX
    boundary = {}
    for label, k in [('below', edge * (1.-1e-12)), ('at', edge), ('above', edge * (1.+1e-12))]:
        p = RRM.rrm_plan(led, FIX.RT, resolve_k=k)
        check = RRM.rrm_check(p, led)
        solver_calls = []
        original_solver = S3.solve_sigma_z
        def guard_only(*a, **kw):
            solver_calls.append(True)
            S3.iface_require_quantitative(kw['iface'], a[0], a[1], vox=a[2])
            return 'guard accepted'
        S3.solve_sigma_z = guard_only
        try:
            gate = trycall(lambda: RRM.rrm_solve(sid, FIX.te(), FIX.A_VOX, p, led))
        finally:
            S3.solve_sigma_z = original_solver
        boundary[label] = {'k': k, 'a': a, 'k_h': k * FIX.A_VOX, 'check': check,
                           'rejections': p['rejections'], 'film': p['n_film_rows'], 'cut': p['n_cut_rows'],
                           'wrapper_guard': gate}
    tsid, _, tl = quiet(FIX.bed, FIX.T_C, FIX.T_R, FIX.T_T, FIX.T_LO, FIX.T_HI, .1, .24)
    tp = RRM.rrm_plan(tl, FIX.RT, resolve_k=4.)
    tc = copy.deepcopy(tp)
    tc['rejections'] = []
    tc['record']['iface_rejections'] = []
    original_planner = RRM.rrm_plan
    RRM.rrm_plan = lambda *a, **kw: tc
    try:
        independent = RRM.rrm_check(tc, tl)
    finally:
        RRM.rrm_plan = original_planner
    boundary['tilt_rejection_removed'] = {'intact': RRM.rrm_check(tp, tl), 'rejections': tp['rejections'],
                                         'cleared': RRM.rrm_check(tc, tl), 'without_replay': independent}
    assert independent
    return {'summaries': out, 'eligibility_boundary': boundary}

if __name__ == '__main__':
    result = {'module_files': {'step3': S3.__file__, 'rrm': RRM.__file__},
              'original_probes': baseline_and_old(), 'expanded': mutations(),
              'summary_and_boundary': summaries_and_boundary()}
    print(json.dumps(result, indent=2, ensure_ascii=False, default=lambda x: x.item() if isinstance(x, np.generic) else str(x)))
