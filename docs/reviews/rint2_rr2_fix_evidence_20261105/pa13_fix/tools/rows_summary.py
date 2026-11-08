"""rows_dump 결과 JSON → 검사마다 행 수 · 실패 행 · 통과 행 (요약)."""
import json
import sys

d = json.load(open(sys.argv[1], encoding='utf-8'))
for k, v in d.items():
    det = v['detail']
    if not isinstance(det, dict):
        print(k, v['pass'], det)
        continue
    rows = det.get('rows', det.get('got', {}))
    bn = set(det.get('bad_names') or det.get('bad', {}))
    print(f'{k} pass={v["pass"]} rows={len(rows)} bad={len(bn)}')
    print('   통과 행:', [r for r in rows if r not in bn])
    print('   실패 행:', sorted(bn))
