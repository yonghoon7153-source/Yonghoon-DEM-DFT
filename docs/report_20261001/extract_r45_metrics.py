#!/usr/bin/env python3
"""사양 5 조성 (r4.5 · 6 mAh/cm²) — 웹앱 full_metrics.json 에서 수송 · 구조 지표를 뽑는다 (보고 2-8 표용 · 읽기 전용).

    ~/Yonghoon-DEM-DFT/venv/bin/python3 ~/dem-web/docs/report_20261001/extract_r45_metrics.py [results 폴더]

기본 results 폴더 = ~/Yonghoon-DEM-DFT/webapp/results · 출력 = ~/r45_metrics_20260929.tsv (키 × 5 조성) + 화면.
키 이름을 가정하지 않는다 — 이름에 sigma · tortuos · porosity · coverage · cn · perc · thickness · active 가 든 숫자 키를 전부 싣는다.
"""
import json
import os
import re
import sys

ROOT = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else '~/Yonghoon-DEM-DFT/webapp/results')
CASES = [('10:0', '260922_222828_6e4ff6'), ('7:3', '260925_000559_082983'), ('5:5', '260925_000513_123978'),
         ('3:7', '260925_000448_bd85f9'), ('0:10', '260925_000001_0bee25')]
PAT = re.compile(r'(sigma|tortuos|porosity|coverage|_cn|perc|thickness|active)', re.I)
data = {}
for ps, cid in CASES:
    path = os.path.join(ROOT, cid, 'full_metrics.json')
    try:
        m = json.load(open(path, encoding='utf-8'))
    except Exception as e:  # 없는 케이스는 빈 열로 남긴다
        print(f'{ps} {cid} 읽기 실패: {e}')
        continue
    data[ps] = {k: v for k, v in m.items() if PAT.search(k) and isinstance(v, (int, float)) and not isinstance(v, bool)}
keys = sorted(set().union(*[d.keys() for d in data.values()])) if data else []
out = os.path.expanduser('~/r45_metrics_20260929.tsv')
with open(out, 'w', encoding='utf-8') as f:
    f.write('key\t' + '\t'.join(ps for ps, _ in CASES) + '\n')
    for k in keys:
        f.write(k + '\t' + '\t'.join(('%.6g' % data[ps][k]) if k in data.get(ps, {}) else '' for ps, _ in CASES) + '\n')
print(open(out, encoding='utf-8').read())
print(f'→ {out}  (케이스 {len(data)}/5 · 키 {len(keys)})')
