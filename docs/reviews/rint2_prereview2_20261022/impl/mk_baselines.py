import json
import os
D = os.path.dirname(os.path.abspath(__file__))
ms = json.load(open(os.path.join(D, 'mutations.json'), encoding='utf-8'))
seen, out = [], []
for m in ms:
    k = tuple(m['cmd'])
    if k in seen or m['file'] == 'scripts/rint_r_chain.py':
        continue
    seen.append(k)
    out.append({'id': 'BASE_' + m['id'], 'file': m['file'], 'what': '기준선 (변이 없음)', 'old': m['old'], 'new': m['old'],
                'cmd': m['cmd'], 'expect': []})
json.dump(out, open(os.path.join(D, 'baselines.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(out), [o['id'] for o in out])
