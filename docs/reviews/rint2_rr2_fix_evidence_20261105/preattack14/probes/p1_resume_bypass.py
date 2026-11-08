"""P2-1 bypass search — honest producer summaries (mm = RESUME_MISMATCH · l3 = eligible after rerun · rr = eligible in rerun) + 1–4 field edits."""
import copy
from lib import RR, T, row

sc = T.scen('PA13', T.pa13_scen)
mm, l3, rr = (sc[k]['b']['sum'] for k in ('mm', 'l3', 'rr'))
print('honest resume blocks:')
for k in ('mm', 'l3', 'rr'):
    s = sc[k]['b']['sum']
    print(' ', k, (s.get('stop') or {}).get('code'), (s.get('stop') or {}).get('run'), s.get('resume'), [r.get('name') for r in s['runs']])


def ed(s0, *fns):
    s = copy.deepcopy(s0)
    for f in fns:
        f(s)
    return s


def stop(code=None, run=None):
    def f(s):
        if code is not None:
            s['stop']['code'] = code
        if run is not None:
            s['stop']['run'] = run
    return f


def rs(**kw):
    def f(s):
        s['resume'].update(kw)
    return f


def rsdel(k):
    def f(s):
        s['resume'].pop(k)
    return f


def runk(name, **kw):
    def f(s):
        [r for r in s['runs'] if r.get('name') == name][0].update(kw)
    return f


def same(v):
    def f(s):
        s['resume']['compared'] = [dict(x, same=v) for x in s['resume']['compared']]
    return f


rerun_mm = mm['resume']['rerun']
TL = stop('TIME_LIMIT', 'L03_point')
rows = [
    # (name, scen, src, summary, note)  note = producer-possible?
    ('A1_l3_resume_extra_key', 'l3', 'keep', ed(l3, rs(extra=1)), 'never written (extra key)'),
    ('A2_rr_del_determinism', 'rr', 'keep', ed(rr, rsdel('determinism')), 'never written (key missing)'),
    ('A3_rr_del_compared', 'rr', 'keep', ed(rr, rsdel('compared')), 'never written'),
    ('A4_rr_resume_extra_key', 'rr', 'keep', ed(rr, rs(extra=[1])), 'never written (extra key)'),
    ('A5_l3_det_compared_cmp_order_dup', 'l3', 'keep', ed(l3, lambda s: s['resume']['compared'].append(dict(s['resume']['compared'][0]))), 'never written'),
    ('B1_mm_TL_sameTrue', 'mm', 'keep', ed(mm, TL, same(True)), 'forgery 3 fields'),
    ('B2_mm_GU_code_only', 'mm', 'keep', ed(mm, stop('GROUP_UNCONFIRMED')), 'forgery 1 field'),
    ('B3_mm_GU_cmp_empty_det_none', 'mm', 'keep', ed(mm, stop('GROUP_UNCONFIRMED'), rs(compared=[], determinism=None)), 'forgery 3 fields'),
    ('B4_mm_GU_cmp_empty_det_none_armsread_empty', 'mm', 'keep',
     ed(mm, stop('GROUP_UNCONFIRMED'), rs(compared=[], determinism=None), runk(rerun_mm, arms_read=[])), 'forgery 4 fields'),
    ('B5_mm_TL_run_rerun_cmp_empty', 'mm', 'keep', ed(mm, stop('TIME_LIMIT'), rs(compared=[], determinism=None)), 'forgery 3 fields'),
    ('B6_mm_TL_rerun_to_L03', 'mm', 'keep', ed(mm, TL, rs(rerun='L03_point', compared=[], determinism=None)), 'forgery 4 fields'),
    ('C1_mm_TL_sameTrue_nosrc', 'mm', 'drop', ed(mm, TL, same(True)), 'declared limitation (src elsewhere)'),
    ('C2_mm_TL_assumed_nosrc', 'mm', 'drop', ed(mm, TL, rs(compared=[], determinism='assumed')), 'declared limitation (src elsewhere)'),
    ('E1_mm_TL_sameNone_nosrc', 'mm', 'drop', ed(mm, TL, same(None)), 'never written'),
    ('E2_mm_TL_sameStrTrue_nosrc', 'mm', 'drop', ed(mm, TL, same('true')), 'never written'),
    ('E3_mm_TL_same0_nosrc', 'mm', 'drop', ed(mm, TL, same(0)), 'never written'),
    ('F1_l3_from_float', 'l3', 'keep', ed(l3, rs(**{'from': 1.0})), 'never written'),
    ('F2_l3_from_str', 'l3', 'keep', ed(l3, rs(**{'from': '1'})), 'never written'),
    ('F3_l3_rerun_int', 'l3', 'keep', ed(l3, rs(rerun=2)), 'never written'),
    ('F4_l3_copiedfrom_true', 'l3', 'keep', ed(l3, runk('L01_floor', copied_from=True)), 'never written (bool copied_from)'),
    ('F5_l3_copiedfrom_true_from_true', 'l3', 'keep', ed(l3, runk('L01_floor', copied_from=True), rs(**{'from': True})), 'never written'),
    ('G1_rr_compared_None', 'rr', 'keep', ed(rr, rs(compared=None)), 'never written'),
    ('G2_l3_cmp_file_traversal_nosrc', 'l3', 'drop', ed(l3, lambda s: s['resume']['compared'].__setitem__(0, {'file': '../../x', 'same': True})), 'declared (nosrc)'),
    ('H_honest_mm', 'mm', 'keep', mm, 'honest'),
    ('H_honest_l3', 'l3', 'keep', l3, 'honest'),
    ('H_honest_rr', 'rr', 'keep', rr, 'honest'),
]
acc = []
for nm, k, src, s, note in rows:
    f = T.pa13_folder(sc[k], 'p1_' + nm, src)
    r = row(f, s)
    flag = (isinstance(r, list) and r[1] is True)
    print(f'{nm:48s} {src:4s} {str(r)[:170]}   [{note}]')
    if flag and not nm.startswith('H_'):
        acc.append((nm, note))
print('\nACCEPTED (resume_ok True) non-honest:', acc)
