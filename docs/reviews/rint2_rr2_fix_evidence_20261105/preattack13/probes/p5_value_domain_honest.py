"""P5 — 제안 고침 (ARM_PUBLIC 값 꼴 = read_run 이 쓰는 값 범위) 이 정직 기록을 거부하지 않는지: 정직 요약 (사다리 · 예측 · 단위 · 합치기 · 넘침) 의
verified 기록 전부에 제안 술어를 적용 · 관측 값 꼴 표."""
import json, math, sys
from collections import Counter, defaultdict
from common import RR, T, setup_fixtures

def proposed_problem(a):
    st = a.get('state')
    if st not in ('positive', 'zero'):
        return f'state {st!r}'
    pid = a.get('protocol_id')
    if not (type(pid) is str and pid.startswith(RR.RC.CA_EXT_PREFIX + '-')):
        return f'protocol_id {pid!r}'
    if not (type(a.get('sid_fp')) is str and a['sid_fp']):
        return 'sid_fp'
    cp = a.get('cert_pass')
    if not (type(cp) is list and len(cp) == 4 and all(x is None or type(x) is bool for x in cp)):
        return f'cert_pass {cp!r}'
    e = a.get('err_rel')
    if not (type(e) is float and math.isfinite(e) and e >= 0.0) or (st == 'zero' and e != 0.0):
        return f'err_rel {e!r}'
    for k in ('cg_iters', 'resolve_iters'):
        v = a.get(k)
        if not (v is None or type(v) is int):
            return f'{k} {v!r}'
    if st == 'positive' and cp != [True, True, True, True]:
        return f'positive cert_pass {cp!r}'
    return None

def main():
    setup_fixtures()
    types = defaultdict(Counter)
    bad, n = [], 0
    sums = []
    for law in ('P0', 'P1'):
        sums.append((f'lad_{law}', T.s_main(law).get('sum')))
    sums.append(('pred', T.s_main_predict().get('sum')))
    if 'units' in sys.argv[1:]:
        r = T.s_units_main()
        for nm, atts in r['units'].items():
            for a in atts:
                if a: sums.append((f'unit:{nm}', a.get('sum')))
        sums.append(('merge', (r.get('m') or {}).get('sum')))
        r2 = T.s_units_over()
        for k in ('m2', 'one'):
            sums.append((f'over:{k}', (r2.get(k) or {}).get('sum')))
    for lab, s in sums:
        for r in (s or {}).get('runs') or []:
            if RR.arms_read_kind(r.get('arms_read'), r)[0] != 'verified':
                continue
            for a in r['arms_read']:
                n += 1
                for k in RR.ARM_PUBLIC:
                    v = a.get(k)
                    types[k][type(v).__name__ if k not in ('state', 'sv_cf_status') else repr(v)] += 1
                why = proposed_problem(a)
                if why:
                    bad.append((lab, r.get('name'), why))
    print(json.dumps({'n_arm_records': n, 'n_rejected_by_proposal': len(bad), 'bad': bad[:10],
                      'observed_types': {k: dict(v) for k, v in types.items()}}, ensure_ascii=False, indent=1))

if __name__ == '__main__':
    main()
