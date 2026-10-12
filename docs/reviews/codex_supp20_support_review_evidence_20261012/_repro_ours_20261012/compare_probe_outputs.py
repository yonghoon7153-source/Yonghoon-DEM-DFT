"""Codex 탐침 출력 ↔ 우리 트리 재실행 출력 대조 (보충 20 지원 검토 · 10-12).

python3 -I compare_probe_outputs.py <Codex evidence 폴더> <우리 출력 폴더> <out.json> release_probe.json design_probe.json

JSON 을 평탄화해 키별로 비교한다.  같지 않은 값은 셋으로 나눈다:
  path   — 둘 다 문자열이고 작업 경로 (윈도 · /tmp · /home · 임시 폴더 이름) 가 들어 있음 = 환경 차이
  float  — 둘 다 실수 · 상대 차 ≤ 1e-12
  other  — 나머지 = 판정값 차이 (0 이어야 같은 판정)
"""
import json
import re
import sys

PATHY = re.compile(r'(/tmp/|/home/|[A-Za-z]:\\|\\\\|C:/|release_probe_|design_probe_|tmp[a-z0-9_]{6,})')


def flat(x, p=''):
    o = {}
    if isinstance(x, dict):
        for k, v in x.items():
            o.update(flat(v, f'{p}.{k}' if p else str(k)))
    elif isinstance(x, list):
        if not x:
            o[p] = []
        for i, v in enumerate(x):
            o.update(flat(v, f'{p}[{i}]'))
    else:
        o[p] = x
    return o


def main():
    codex, ours, out = sys.argv[1:4]
    names = sys.argv[4:]
    res = {}
    for name in names:
        a = flat(json.load(open(f'{codex}/{name}', encoding='utf-8')))
        b = flat(json.load(open(f'{ours}/{name}', encoding='utf-8')))
        ka, kb = set(a), set(b)
        cat = {'equal': 0, 'path': [], 'float': [], 'other': []}
        for k in sorted(ka & kb):
            va, vb = a[k], b[k]
            if va == vb and type(va) is type(vb):
                cat['equal'] += 1
            elif isinstance(va, str) and isinstance(vb, str) and (PATHY.search(va) or PATHY.search(vb)):
                cat['path'].append(k)
            elif isinstance(va, float) and isinstance(vb, float) and abs(va - vb) <= 1e-12 * max(1.0, abs(va)):
                cat['float'].append(k)
            else:
                cat['other'].append({'key': k, 'codex': str(va)[:200], 'ours': str(vb)[:200]})
        res[name] = {'keys_codex': len(ka), 'keys_ours': len(kb), 'only_codex': sorted(ka - kb), 'only_ours': sorted(kb - ka),
                     'equal': cat['equal'], 'path_only_diff': cat['path'], 'float_1e-12': cat['float'], 'judgment_diff': cat['other']}
        print(f"{name}: 키 Codex {len(ka)} · 우리 {len(kb)} · 한쪽만 {len(ka - kb)} / {len(kb - ka)} · 같음 {cat['equal']} · "
              f"경로 문자열만 {len(cat['path'])} · 실수 1e-12 {len(cat['float'])} · 판정값 차이 {len(cat['other'])}")
    json.dump(res, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)
    sys.exit(1 if any(r['judgment_diff'] or r['only_codex'] or r['only_ours'] for r in res.values()) else 0)


if __name__ == '__main__':
    main()
