"""rows_dump 결과 JSON → 검사마다 통과 · 행 수 · 실패 행 · 행 상태 (RR4A = accepted / rejected<표지>) 요약.  쓰임: python3 rows_summary.py <rows json>"""
import json
import sys

d = json.load(open(sys.argv[1], encoding='utf-8'))
for k, v in d.items():
    det = v['detail']
    if not isinstance(det, dict):
        print(f'{k} pass={v["pass"]} {str(det)[:300]}')
        continue
    rows = det.get('rows', det.get('got', {}))
    bn = sorted(det.get('bad_names') or det.get('bad', {}) or [])
    print(f'{k} pass={v["pass"]} rows={len(rows) if isinstance(rows, dict) else "-"} bad={len(bn)}')
    if isinstance(rows, dict):
        for r, val in rows.items():
            if isinstance(val, dict) and ('state' in val or 'behaviour_ok' in val):
                print(f'   {r}: state={val.get("state", "-")} behaviour_ok={val.get("behaviour_ok")} recount_ok={val.get("recount_ok")} '
                      f'cli={str(val.get("cli"))[:160]} places={str(val.get("places"))[:160]}')
            else:
                print(f'   {r}: {str(val)[:220]}')
    if bn:
        print('   실패 행:', bn)
