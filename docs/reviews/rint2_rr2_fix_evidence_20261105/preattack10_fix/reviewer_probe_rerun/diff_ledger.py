"""사전 공격 10 회차 리뷰어 실경로 탐침 (probe_ledger.py) — 리뷰어 기록 ↔ 이 고침 뒤 다시 돌린 결과 (줄마다 결과 줄 원인 · 자격 · --add --resume rc).
  python3 -I diff_ledger.py <리뷰어 기록 json> <다시 돌린 json> [<출력 json>]"""
import json
import sys

a = json.load(open(sys.argv[1], encoding='utf-8'))['rows']
b = json.load(open(sys.argv[2], encoding='utf-8'))['rows']


def view(r):
    return {'orphan': r.get('orphan'), 'recover_rc': r.get('recover_rc'), 'cause': (r.get('result') or {}).get('cause'),
            'resume_ok': (r.get('result') or {}).get('resume_ok'), 'resume_rc': r.get('resume_rc'), 'not_allowed': r.get('not_allowed'),
            'ledger_same': r.get('ledger_same')}


res = {k: {'reviewer_fixed_version': view(a[k]), 'after_this_fix': view(b[k]), 'same': view(a[k]) == view(b[k])} for k in sorted(set(a) | set(b))}
txt = json.dumps(res, ensure_ascii=False, indent=1)
if len(sys.argv) > 3:
    open(sys.argv[3], 'w', encoding='utf-8').write(txt + '\n')
for k, v in res.items():
    print(k.ljust(36), 'same' if v['same'] else 'DIFF', v['reviewer_fixed_version']['resume_rc'], '->', v['after_this_fix']['resume_rc'],
          v['after_this_fix']['cause'])
