"""display_source.json 의 rendered_rows 를 행 라벨 기준으로 고치기 전 · 후 대조 (읽기 전용 · 증거 정리용)."""
import json
import sys

pre = json.load(open(sys.argv[1], encoding='utf-8'))
post = json.load(open(sys.argv[2], encoding='utf-8'))
key = sys.argv[3] if len(sys.argv) > 3 else 'rendered_rows'


def short(lbl):
    return lbl.split(' — ')[0].split(',')[0][:38]


def cell(v):
    v = str(v)
    if v.startswith('— (모형 한계'):
        return '—(ML)'
    if v.startswith('미계산 — FULL 모형 한계'):
        return '미계산(ML)'
    return v[:28]


n_changed = 0
for c in sorted(pre['cases']):
    a = pre['cases'][c].get(key) or []
    b = post['cases'].get(c, {}).get(key) or []
    da = {r[0]: r[1:] for r in a}
    db = {r[0]: r[1:] for r in b}
    out = []
    for lbl in list(da) + [l for l in db if l not in da]:
        va, vb = da.get(lbl), db.get(lbl)
        if va != vb:
            out.append(f"    {short(lbl):38s} {' | '.join(cell(x) for x in (va or ['(없음)'])):60s} → {' | '.join(cell(x) for x in (vb or ['(없음)']))}")
    hs = (pre['cases'][c].get('http_status'), post['cases'].get(c, {}).get('http_status'))
    if out or hs[0] != hs[1]:
        n_changed += 1
        print(f'{c}  http {hs[0]}→{hs[1]}')
        print('\n'.join(out))
print('cases', len(pre['cases']), 'changed', n_changed)
