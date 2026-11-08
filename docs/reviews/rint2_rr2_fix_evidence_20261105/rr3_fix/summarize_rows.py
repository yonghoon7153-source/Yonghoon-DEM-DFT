"""dump_rr3.py 의 JSON → 행동 칸 요약 (재실행 자격 · 사유 · 분류 · 원장) — python3 summarize_rows.py <rows.json>."""
import json
import sys

d = json.load(open(sys.argv[1], encoding='utf-8'))
print('chain sha256', d.get('_chain_sha256'), '· test sha256', d.get('_test_sha256'))
for cid in ('CT06', 'PC12C', 'RR3A', 'RR3B', 'RR3C', 'RR3D', 'RR3E', 'RR3P'):
    v = d.get(cid)
    if v is None:
        continue
    w = v['why']
    n = w.get('n') if isinstance(w, dict) else None
    nb = w.get('n_bad') if isinstance(w, dict) else None
    print(f'{cid}: {"PASS" if v["ok"] else "FAIL"} · 행 {n} · 실패 {nb}')
c = (d.get('RR3C') or {}).get('why') or {}
rows = c.get('rows') or {} if isinstance(c, dict) else {}
if rows:
    neg = {k: r for k, r in rows.items() if k.startswith('n_')}
    print(f'RR3C 음성 {len(neg)} 중 자격 True =', sorted(k for k, r in neg.items() if r[1] is True))
    print(f'RR3C 음성 {len(neg)} 중 자격 False =', sorted(k for k, r in neg.items() if r[1] is not True))
    print('RR3C 정직 · 대조 행 [원인, 자격, 사유 있음, 분류] =', {k: r for k, r in rows.items() if not k.startswith('n_') and k != 'fixture_keys'})
    print('RR3C 음성 행 분류 =', {k: r[3] for k, r in neg.items()})
    print('RR3C fixture_keys =', rows.get('fixture_keys'))
for cid in ('RR3A', 'RR3B', 'RR3D'):
    w = (d.get(cid) or {}).get('why') or {}
    if isinstance(w, dict) and 'rows' in w:
        print(cid, 'rows =', json.dumps(w['rows'], ensure_ascii=False))
w = (d.get('RR3E') or {}).get('why') or {}
if isinstance(w, dict):
    print('RR3E got [recover rc, 자격, resume rc, RESUME_NOT_ALLOWED] =', w.get('got'))
w = (d.get('RR3P') or {}).get('why')
print('RR3P =', json.dumps(w, ensure_ascii=False))
