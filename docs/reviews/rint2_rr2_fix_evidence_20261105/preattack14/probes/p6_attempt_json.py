"""Declared-limitation check: forged attempt.json resume_of (1 → null) + summary resume null + stop TIME_LIMIT/L03 (honest RESUME_MISMATCH mm).
   Result line (recover, same function) → --add --resume order (attempt_order_problem) → presolve chain recount (resume_chain_problem) →
   verdict-side found_attempts_problem.  Is the declared mitigation ('원장 항목 대조 = found_attempts_problem') present at the resume decision points?"""
import copy, json
from pathlib import Path
from lib import RR, T, row

sc = T.scen('PA13', T.pa13_scen)
mm = sc['mm']['b']['sum']


def ledger(f2, s2):
    f1 = f2.parent / 'attempt_1'
    s1 = json.loads((f1 / 'ladder_summary.json').read_text(encoding='utf-8'))
    (f2 / 'ladder_summary.json').write_bytes(RR.canon_bytes(s2))
    head = {'kind': 'header', 'schema': RR.LEDGER_SCHEMA, 'plan_sha256': 'b' * 64, 'utc': 'synthetic'}
    ent1 = {'kind': 'entry', 'n': 1, 'target': 'ladder:P0', 'machine': 'synthetic', 'resume_of': None, 'plan_sha256': 'b' * 64,
            'code_key_sha256': 'c' * 64, 'env': {}, 'bed': {}, 'utc': 'synthetic'}
    ent2 = dict(ent1, n=2, resume_of=1)

    def start(n, f):
        return {'kind': 'start', 'n': n, 'base': str(f.parent.resolve()), 'folder': f.name, 'host': {'machine_id': None, 'boot_id': None, 'pidns': None},
                'utc': 'synthetic', 'chain_pid': 1, 'chain_start': None}
    res1 = RR.attempt_result_line(1, f1, s1, 'recover')
    res2 = RR.attempt_result_line(2, f2, s2, 'recover')
    st = RR.ledger_parse(''.join(RR.ledger_line(x) for x in (head, ent1, start(1, f1), res1, ent2, start(2, f2), res2)).encode('utf-8'))
    e3 = dict(ent1, n=3, resume_of=1)
    order = RR.attempt_order_problem(st, e3, {'exec_policy': {'max_attempts': 3}})
    try:
        chain = RR.resume_chain_problem(st, e3, 3, f2.parent)
    except Exception as ex:     # noqa: BLE001
        chain = f'EXC {type(ex).__name__}: {ex}'
    fa = RR.found_attempts_problem(st, {1: [f1], 2: [f2]})
    return {'res2': {k: res2[k] for k in ('cause', 'resume_ok', 'stop')}, 'order(--add --resume)': order, 'presolve chain recount': chain,
            'verdict found_attempts_problem': (fa or '')[:140] or None}


TL = T.pa13_stop('TIME_LIMIT', 'L03_point')
for nm, edits, attjson in (('honest_mm', [], None),
                           ('forge_stop_resume_null', [TL, T.pa13_set_resume(None)], None),
                           ('forge_stop_resume_null_attjson_null', [TL, T.pa13_set_resume(None)], {'resume_of': None})):
    f2 = T.pa13_folder(sc['mm'], 'p6_' + nm)
    if attjson:
        T.pa13_att(f2, **attjson)
        # keep canonical attempt.json bytes form (read_attempt = strict JSON · keys)
    s2 = T.pa13_ed(mm, *edits)
    print(nm)
    for k, v in ledger(f2, s2).items():
        print(f'   {k}: {str(v)[:200]}')
