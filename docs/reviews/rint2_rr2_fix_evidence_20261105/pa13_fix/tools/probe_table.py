"""사전 공격 13 탐침 다시 — 고치기 전 (before) · 뒤 (after) 출력에서 판정 칸만 뽑아 한 줄씩 (보고 표 원천 · 숫자 = 출력 그대로).
쓰임: python3 probe_table.py <probe_out 폴더>"""
import json
import sys
from pathlib import Path

D = Path(sys.argv[1])


def load(name, side):
    p = D / f'{name}_{side}.out'
    t = p.read_text(encoding='utf-8')
    if '[stderr]' in t:
        t = t.split('\n[stderr]\n')[0]
    try:
        return json.loads(t)
    except json.JSONDecodeError:                      # 탐침 p4 원판 = 출력 2000 자에서 자른다 → 머리 칸 (n · verified) 만 글에서
        import re
        return {'n': int(re.search(r'"n": (\d+)', t).group(1)), 'verified': int(re.search(r'"verified": (\d+)', t).group(1)),
                'bad': None, 'fail_kind_bad': None, 'truncated': True}


def kind(x):
    return x[0] if isinstance(x, list) else x


def p1(d):
    out = {'producer': kind(d['producer']['kind'])}
    for k in ('as_is', 'pad_none', 'pad_impossible', 'pad_legacy_state'):
        v = d[k]
        led = v['ledger[resume_ok, order_stop, recount]']
        out[k] = f"{kind(v['kind'])} · resume_ok {v['resume_ok']} · 원장 {led[1]}"
    return out


def p1b(d):
    return {k: f"resume_ok {v['result']['resume_ok']} · resume rc {v['resume_rc']} · 거부 {v['not_allowed']}" for k, v in d.items()}


def p2(d):
    e = d['edited']
    return {'attempt2_stop': d['attempt2_stop']['code'], 'real_result_line_2': d['real_result_line_2'],
            'edited': f"resume_ok {e['resume_ok']} · 사유 {'있음' if e['stop_record_problem'] else '없음'}",
            'edited_ledger': d['edited_ledger[resume_ok, order_stop, recount]'], 'attempt3_src_done': d['attempt3_src_done']}


def p2b(d):
    nr = d['next_resume_1_order_problem']
    return {'res1': d['res1']['resume_ok'], 'res2_from_edited': d['res2_from_edited']['resume_ok'],
            'next_resume_1': kind(nr) if nr else None, 'recount_2': d['recount_2'],
            'stop_record_problem_edited': '있음' if d['stop_record_problem_edited'] else '없음',
            'L02_same_as_attempt1': d['L02_payload_same_as_attempt1_leftover']}


def p2c(d):
    out = {}
    for k, v in d.items():
        if k == 'scen':
            out[k] = f"mm {v['mm_stop']} · l3 {v['l3_stop']}"
        elif k == 'LIMIT_resume_chain_recount':
            out[k] = (f"결과 줄 resume_ok {v['result_line_resume_ok_src_elsewhere']} · 같은 바탕 다시 셈 "
                      f"{'대조 실패' if v['recount_same_base_with_src'] else 'None'}")
        else:
            out[k] = f"{v['cause']} · resume_ok {v['resume_ok']} · 사유 {'있음' if v['reason'] else '없음'}"
    return out


def p3(d):
    return {'forms': d['forms'], 'n_bad': d['n_bad']}


def p4(d):
    if d.get('truncated'):
        return {'n': d['n'], 'verified': d['verified'], 'n_bad': '(출력 2000 자에서 잘림 · n − verified)', 'fail_kind_bad': '(잘림 · p4v 참조)'}
    return {'n': d['n'], 'verified': d['verified'], 'n_bad': len(d.get('bad') or []),
            'fail_kind_bad': d['fail_kind_bad'] if isinstance(d['fail_kind_bad'], int) else len(d['fail_kind_bad'])}


def p4v(d):
    return {k: {'n': v['n'], 'kinds': v['kinds'], 'fail_kind_bad': v['fail_kind_bad']} for k, v in d.items()}


def p5(d):
    return {'n_arm_records': d['n_arm_records'], 'n_rejected_by_proposal': d['n_rejected_by_proposal']}


def p5b(d):
    return {'fn': d['fn'], 'n_runs': d['n_runs'], 'n_arm_records': d['n_arm_records'], 'kinds': d['kinds'],
            'n_rejected': d['n_rejected'] if d['fn'] else 'N/A (함수 없음)'}


def p6(d):
    return {k: kind(v) for k, v in d.items()}


SPEC = [('p1_value_domain', p1), ('p1b_value_domain_cli', p1b), ('p2_resume_mismatch', p2), ('p2b_resume_mismatch_chain', p2b),
        ('p2c_resume_stronger', p2c), ('p3_honest_shapes_main_pred', p3), ('p3_honest_shapes_units_over', p3),
        ('p4_all_arm_forms', p4), ('p4v_all_arm_forms_values', p4v), ('p5_value_domain_honest_units', p5),
        ('p5b_value_domain_real_units', p5b), ('p6_struct_edges', p6)]
for name, f in SPEC:
    print(f'== {name}')
    b, a = f(load(name, 'before')), f(load(name, 'after'))
    for k in b:
        same = '' if b[k] != a.get(k) else '   (같음)'
        print(f'  {k}: {json.dumps(b[k], ensure_ascii=False)}  →  {json.dumps(a.get(k), ensure_ascii=False)}{same}')
py38 = D / 'p1_value_domain_after_py38.out'
if py38.exists():
    same = py38.read_bytes() == (D / 'p1_value_domain_after.out').read_bytes()
    print(f'== p1_value_domain after py3.8 = after py3.11 바이트 같음 {same}')
