"""사전 공격 10 회차 리뷰어 탐침 결과 — 리뷰어 기록 (고친 판 f5b00a838 = probe_*_new.json) ↔ 이 고침 뒤 다시 돌린 결과 (probe_*_after.json) 의 행 차이.
  python3 -I diff_rows.py <리뷰어 기록 json> <다시 돌린 json> [<출력 json>]"""
import json
import sys

a = json.load(open(sys.argv[1], encoding='utf-8'))
b = json.load(open(sys.argv[2], encoding='utf-8'))


def rows(d):
    r = d.get('rows', d)
    out = {}
    for k, v in r.items():
        if isinstance(v, dict) and k in ('L_run_log_text', 'SU_read'):
            for kk, vv in v.items():
                out[f'{k}/{kk}'] = vv
        else:
            out[k] = v
    return out


ra, rb = rows(a), rows(b)
diff = {k: {'reviewer_fixed_version': ra.get(k), 'after_this_fix': rb.get(k)} for k in sorted(set(ra) | set(rb)) if ra.get(k) != rb.get(k)}
res = {'n_rows': len(set(ra) | set(rb)), 'n_diff': len(diff), 'diff': diff}
txt = json.dumps(res, ensure_ascii=False, indent=1)
if len(sys.argv) > 3:
    open(sys.argv[3], 'w', encoding='utf-8').write(txt + '\n')
print(txt)
