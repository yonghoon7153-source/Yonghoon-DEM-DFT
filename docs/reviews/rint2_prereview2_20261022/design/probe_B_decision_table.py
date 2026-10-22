"""Probe B — decision-table closure (registration R §5-0 · §5-1 · §5-5 · §5-5b · §5-6 · §5-6a) vs the REAL chain at 93d93bc02.

Independent reference = my own reading of the registration text (no chain code reused for the reference).
Run:  python3 -I probe_B_decision_table.py <worktree>      (writes probe_B_decision_table.json · < 10 s)
"""
import itertools
import json
import math
import os
import random
import re
import sys

WT = sys.argv[1]
sys.path.insert(0, os.path.join(WT, 'scripts'))
import rint_r_chain as RR  # noqa: E402

REG = open(os.path.join(WT, 'docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md'), encoding='utf-8').read()
X = 4.68
G0 = math.log(4.68 / 1.8877)
OUT = {'judge': {}, 'sentence': {}, 'assemble': {}}


# ── independent reference of §5-0 / §5-1 / §5-5 (text) ──
def ref_judge(vals):
    by = {}
    for (c, law, rr), v in vals.items():
        by.setdefault(law, []).append(v)
    I = {law: (min(v), max(v)) for law, v in by.items()}
    allv = list(vals.values())
    lo, hi = min(allv), max(allv)
    inU = any(a <= X <= b for a, b in I.values())
    inE = lo <= X <= hi
    zero = lo == 0.0
    if zero:
        state, W = 'extended', math.inf
    elif lo == hi:
        state, W = 'point', 0.0
    else:
        state, W = 'positive', math.log(hi / lo)
    if inU:
        v = 'UNINFORMATIVE' if zero else ('PASS_INFORMATIVE' if W <= G0 / 2 else 'CONSISTENT_WEAK' if W <= G0 else 'UNINFORMATIVE')
    elif inE:
        v = 'GAP_ENVELOPE_ONLY'
    else:
        v = 'FAIL'
    return state, v, W


def mk(vals_by_law):
    out = {}
    for law, vs in vals_by_law.items():
        for (c, rr), v in zip(itertools.product(('0', '1'), ('R_j_lo', 'R_j0', 'R_j_hi')), vs):
            out[(c, law, rr)] = v
    return out


# (1) structured + random enumeration of judge
rng = random.Random(20261021)
cases, mism, outside_table = 0, [], []
specials = [0.0, X, X * (1 - 1e-15), X * (1 + 1e-15), 4.68 * math.exp(-G0 / 2), 4.68 * math.exp(G0 / 2), 1.0, 10.0, 3.0, 6.0]
for _ in range(20000):
    vb = {}
    for law in ('P0', 'P1'):
        kind = rng.random()
        if kind < 0.15:
            vs = [rng.choice(specials) for _ in range(6)]
        elif kind < 0.25:
            p = rng.choice(specials + [rng.uniform(1, 8)])
            vs = [p] * 6
        else:
            base = rng.uniform(1.0, 9.0)
            vs = [base * math.exp(rng.uniform(-0.6, 0.6)) for _ in range(6)]
            if rng.random() < 0.1:
                vs[rng.randrange(6)] = 0.0
        vb[law] = vs
    vals = mk(vb)
    J = RR.judge(vals)
    st, v, W = ref_judge(vals)
    cases += 1
    if (J['state'], J['verdict']) != (st, v) or not (J['W'] == W or (math.isinf(J['W']) and math.isinf(W)) or abs(J['W'] - W) < 1e-15):
        mism.append({'vals': {str(k): x for k, x in vals.items()}, 'chain': [J['state'], J['verdict'], J['W']], 'ref': [st, v, W]})
    if J['verdict'] not in RR.STATE_VERDICTS.get(J['state'], ()):
        outside_table.append([J['state'], J['verdict']])
OUT['judge'] = {'cases': cases, 'mismatches': len(mism), 'first': mism[:3], 'outside_STATE_VERDICTS': outside_table[:3]}

# exact boundary: W exactly G0/2 (registration "W ≤ 0.454" — rounded number vs exact G0/2)
lo = 3.0
for name, W_ in (('W=G0/2', G0 / 2), ('W=0.454 (rounded)', 0.454), ('W=0.4540 just above G0/2', G0 / 2 + 1e-12), ('W=G0', G0), ('W=0.908', 0.908)):
    J = RR.judge({('0', 'P0', 'R_j_lo'): 4.0, ('0', 'P0', 'R_j_hi'): 4.0 * math.exp(W_)})
    OUT['judge'][f'boundary {name}'] = [J['verdict'], J['W']]
OUT['judge']['G0_exact'] = G0
OUT['judge']['G0/2_exact'] = G0 / 2

# (2) decide_sentence against the §5-5b table text parsed from the registration document
tab = REG.split('5-5b. 결정표', 1)[1].split('- 한 레코드에 칸 하나', 1)[0]
rows = [r for r in tab.splitlines() if r.startswith('| `')]
def italics(cell):
    return re.findall(r'\*"(.+?)"\*', cell)
doc_cells = {}
for r in rows:
    cells = [c.strip() for c in r.strip().strip('|').split('|')]
    name = cells[0].split('`')[1]
    doc_cells[name] = {'left': italics(cells[1]), 'right': italics(cells[2]), 'raw_left': cells[1], 'raw_right': cells[2]}
PASS_Q = REG.split('> SBE 측정 한 점으로', 1)[1].split('\n', 1)[0]
PASS_Q = 'SBE 측정 한 점으로' + PASS_Q
sent_bad = []
blk_sets = [[], ['FIBRE_UNCHECKED'], ['SV_UNCHECKED', 'CALIB_ORIGIN_SENSITIVE'], ['GRID_SENSITIVE', 'GRID_SENSITIVE']]
for state, vs in RR.STATE_VERDICTS.items():
    for v in sorted(vs):
        for b in blk_sets:
            for sens in (False, True):
                s = RR.decide_sentence(state, v, b, sens)
                # reference
                if v in ('NOT_COMPUTED',) or v.startswith('CALIB_'):
                    want = 'NC' if v == 'NOT_COMPUTED' else 'CALIB'
                    ok = (s == RR.SENTENCE_NC) if v == 'NOT_COMPUTED' else (s == RR.SENTENCE_CALIB)
                else:
                    bl = sorted(set(b))
                    lst = ' · '.join(bl)
                    if v == 'PASS_INFORMATIVE':
                        base = PASS_Q if not bl else f'계산기 판정 이름 `PASS_INFORMATIVE` · 차단 표지 {lst} — 판정 문장 보류'
                    else:
                        left = {'CONSISTENT_WEAK': '넓은 시나리오 구간 안에 들었다', 'UNINFORMATIVE': '예측 주장 없음 (구간이 현 세대 빗나감보다 넓다)',
                                'GAP_ENVELOPE_ONLY': '어느 법칙의 허용집합에도 포함되지 않았으나 전체 envelope 에는 포함 · P 는 두 끝만 등록했다 (사이 감쇠는 모형 밖)',
                                'FAIL': '빗나감 d · d/G0 · 방향 · §8 보고 (해석 금지 §8)'}[v]
                        base = left if not bl else f'{left} (차단 표지 {lst})'
                    if state == 'point':
                        base += ' · 점 구간'
                    if sens:
                        base += ' · 감도 미완료'
                    ok = s == base
                    want = base
                if not ok:
                    sent_bad.append({'state': state, 'v': v, 'b': b, 'sens': sens, 'chain': s, 'ref': want})
# pairs outside the table must raise
raised = []
for state in ('positive', 'point', 'extended', 'calib', 'bogus'):
    for v in RR.GRADES + RR.CALIB_ORDER + ('BOGUS',):
        if state in RR.STATE_VERDICTS and v in RR.STATE_VERDICTS[state]:
            continue
        try:
            RR.decide_sentence(state, v, [], False)
            raised.append((state, v, 'NO_RAISE'))
        except (ValueError, KeyError) as e:
            pass
OUT['sentence'] = {'n_bad': len(sent_bad), 'first_bad': sent_bad[:4], 'out_of_table_not_raising': raised[:5],
                   'doc_PASS_quote_eq_chain': PASS_Q.strip() == RR.SENTENCE_PASS,
                   'doc_cells_italics': {k: v['left'] + v['right'] for k, v in doc_cells.items()}}

# (3) assemble enumeration — §5-6 ② ③ ④ ⑤ and ⑰
CAL = {'P0': 'CALIBRATED', 'P1': 'CALIBRATED'}
base_vals = mk({'P0': [4.40e-3, 4.45e-3, 4.50e-3, 4.42e-3, 4.47e-3, 4.52e-3], 'P1': [4.55e-3, 4.60e-3, 4.65e-3, 4.57e-3, 4.62e-3, 4.80e-3]})
main = {'statuses': CAL, 'vals': base_vals, 'flags': []}
Jm = RR.judge_set(CAL, base_vals)
var_kinds = {
    'none': None,
    'same': {'statuses': CAL, 'vals': base_vals, 'flags': []},
    'same+originflag': {'statuses': CAL, 'vals': base_vals, 'flags': ['CALIB_ORIGIN_SENSITIVE']},
    'nc_predict': {'statuses': CAL, 'vals': None, 'flags': []},
    'nc_ladder': {'statuses': {'P0': 'NOT_COMPUTED', 'P1': 'CALIBRATED'}, 'vals': None, 'flags': []},
    'calib_edge': {'statuses': {'P0': 'CALIB_EDGE', 'P1': 'CALIBRATED'}, 'vals': None, 'flags': []},
    'diff_fail': {'statuses': CAL, 'vals': {k: v * 0.5 for k, v in base_vals.items()}, 'flags': []},
    'diff_fail+originflag': {'statuses': CAL, 'vals': {k: v * 0.5 for k, v in base_vals.items()}, 'flags': ['CALIB_ORIGIN_SENSITIVE']},
}
want_flag = {'none': 'UNCHECKED', 'same': None, 'same+originflag': 'UNCHECKED', 'nc_predict': 'UNCHECKED', 'nc_ladder': 'UNCHECKED',
             'calib_edge': 'SENSITIVE', 'diff_fail': 'SENSITIVE', 'diff_fail+originflag': 'SENSITIVE'}
abad = []
n = 0
for combo in itertools.product(var_kinds, repeat=4):
    variants = {V: var_kinds[k] for V, k in zip(RR.VARIANTS, combo)}
    for svf in ([], ['SV_UNCHECKED'], ['SV_DEPENDENT']):
        pub, res = RR.assemble(main, variants, (svf, {'threshold': 1.5, 'scope': 'R_j0', 'corners': {'x': 1}, 'unreadable': [], 'dependent': []}))
        n += 1
        exp_flags = set(svf)
        sens = False
        for V, k in zip(RR.VARIANTS, combo):
            wf = want_flag[k]
            if k == 'none':
                sens = True
            if wf:
                exp_flags.add(f'{V}_{wf}')
        exp_block = sorted(exp_flags)
        if pub['flags'] != exp_block or pub['blocking_flags'] != exp_block or pub['sensitivity_incomplete'] is not sens \
                or pub['sentence_allowed'] != (Jm['verdict'] == 'PASS_INFORMATIVE' and not exp_block) or 'CALIB_ORIGIN_SENSITIVE' in pub['flags']:
            abad.append({'combo': combo, 'sv': svf, 'got': [pub['flags'], pub['sensitivity_incomplete'], pub['sentence_allowed']],
                         'want': [exp_block, sens]})
OUT['assemble'] = {'main_verdict': Jm['verdict'], 'main_W': Jm['W'], 'combos': n, 'bad': len(abad), 'first_bad': abad[:3]}

# (3b) main calib with a CALIB_ORIGIN_SENSITIVE from the other law — §10-2 ㉙
pub, _ = RR.assemble({'statuses': {'P0': 'CALIB_EDGE', 'P1': 'CALIBRATED'}, 'vals': None, 'flags': ['CALIB_ORIGIN_SENSITIVE']}, {}, None)
OUT['assemble']['calib_with_origin_flag'] = {k: pub[k] for k in ('verdict', 'flags', 'blocking_flags', 'sentence', 'sensitivity_incomplete')}
pub, _ = RR.assemble({'statuses': {'P0': 'NOT_COMPUTED', 'P1': 'CALIB_EDGE'}, 'vals': None, 'flags': []}, {}, None)
OUT['assemble']['nc_vs_edge'] = pub['verdict']

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe_B_decision_table.json')
with open(path, 'w', encoding='utf-8') as f:
    json.dump(OUT, f, ensure_ascii=False, indent=1, default=str)
print(json.dumps({k: (v if k != 'sentence' else {kk: vv for kk, vv in v.items() if kk != 'doc_cells_italics'}) for k, v in OUT.items()},
                 ensure_ascii=False, default=str)[:4000])
