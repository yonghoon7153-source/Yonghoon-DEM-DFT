#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CF/FULL ('R_brug') 라벨 회귀 — L2-07 의 웹앱 · 코드 문구 반영 (1저자 비준 10-02 · J20-l).

  python3 webapp/test_cf_full_labels.py      # 종료코드 0 = PASS

  `R_brug_over_full` 은 이름과 달리 Bruggeman 이 아니라 **CONTACT_FREE / FULL** (접촉 저항을 뺀 네트워크 σ ÷ 전체 네트워크 σ) 이다
  (`scripts/network_conductivity.py` L2-07 주석).  진짜 Bruggeman ÷ network 비는 `R_bruggeman_over_full` · 웹앱 'σ_brug / σ_ionic' 행이고
  케이스마다 다르다 (1 보다 작을 수도 있다 — Codex 4 구 반례 0.28).

  [A] `calc_effective_conductivity` docstring 이 "network solver 대비 3-10× 과대" 를 주장하지 않는다 · 비는 케이스마다라고 적는다
  [B] 그룹 그림 `plot_r_brug_comparison` — 범례 · y 축 · 제목에 Bruggeman 과대추정 문구가 없고 CF/FULL 로 적는다 ·
      y = 1 문구가 'Bruggeman = exact' 가 아니다
  [C] 그림 목록 (`PLOT_REGISTRY`) 제목 · 설명이 'Bruggeman 과대추정' 이 아니라 CF/FULL (L2-07) 이다
  [D] 그룹 화면 체크박스 이름이 'R_brug' 가 아니라 접촉 배수 (CF/FULL) 다 (그림 키 r_brug_comparison 은 그대로)
"""
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRIPTS = os.path.join(ROOT, 'scripts')
sys.path.insert(0, HERE)
sys.path.insert(0, SCRIPTS)

_ok, _fail = 0, []


def chk(name, cond, extra=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f' — {extra}' if extra else ''))
    return bool(cond)


print('[A] calc_effective_conductivity docstring')
import dem_analysis_core as dac  # noqa: E402
doc = dac.calc_effective_conductivity.__doc__ or ''
chk('A1 "3-10× 과대" 주장이 없다', not re.search(r'overestimates by 3', doc), doc.strip()[:160])
chk('A2 비는 케이스마다 (σ_brug / σ_ionic) · CF/FULL (L2-07) 을 적는다', 'σ_brug / σ_ionic' in doc and 'CF/FULL' in doc and 'L2-07' in doc)

print('[B] 그룹 그림 plot_r_brug_comparison')
import matplotlib  # noqa: E402
matplotlib.use('Agg')
import generate_comparison_plots as gcp  # noqa: E402
captured = []
_orig_save = gcp._save
gcp._save = lambda fig, outdir, name: (captured.append(fig), os.path.join(outdir, name))[1]
try:
    data = [{'R_brug_over_full': 4.0, 'electronic_R_brug': 2.0, 'thermal_R_brug': 1.5},
            {'R_brug_over_full': 6.0, 'electronic_R_brug': 3.0, 'thermal_R_brug': 1.2}]
    with tempfile.TemporaryDirectory() as td:
        gcp.plot_r_brug_comparison(data, ['c1', 'c2'], td)
finally:
    gcp._save = _orig_save
chk('B0 그림이 그려진다', len(captured) == 1)
if captured:
    ax = captured[0].axes[0]
    leg = [t.get_text() for t in (ax.get_legend().get_texts() if ax.get_legend() else [])]
    texts = [t.get_text() for t in ax.texts]
    title, ylab = ax.get_title(), ax.get_ylabel()
    blob = ' '.join(leg + texts + [title, ylab])
    chk('B1 범례 = CF/FULL (R_brug 아님)', leg and all('CF/FULL' in s for s in leg) and not any('R_brug' in s for s in leg), str(leg))
    chk('B2 y = 1 문구가 "Bruggeman = exact" 가 아니다', 'Bruggeman = exact' not in texts, str(texts))
    chk('B3 제목 · y 축에 Bruggeman 과대추정 문구가 없다',
        'Overestimat' not in blob and 'overestimat' not in blob, f'{title!r} / {ylab!r}')
    chk('B4 y 축 = CF/FULL', 'CF/FULL' in ylab, ylab)
    chk('B5 제목에 Bruggeman 이 아니라는 표지 (L2-07)', 'not Bruggeman' in title and 'L2-07' in title, title)

print('[C] PLOT_REGISTRY')
reg = gcp.PLOT_REGISTRY['r_brug_comparison']
chk('C1 제목 = CF/FULL', 'CF/FULL' in reg['title'] and 'R_brug' not in reg['title'], reg['title'])
chk('C2 설명이 Bruggeman 과대추정이 아니다 · L2-07 · 진짜 비 안내', 'Bruggeman 과대추정' not in reg['description']
    and 'L2-07' in reg['description'] and 'σ_brug / σ_ionic' in reg['description'], reg['description'][:120])

print('[D] group.html 체크박스')
html = open(os.path.join(HERE, 'templates', 'group.html'), encoding='utf-8').read()
m = re.search(r'value="r_brug_comparison">\s*([^<]+)<', html)
lab = m.group(1).strip() if m else ''
chk('D1 체크박스 이름 = 접촉 배수 (CF/FULL)', 'CF/FULL' in lab and 'R_brug' not in lab, lab)

print(f'\n{_ok} PASS · {len(_fail)} FAIL')
sys.exit(1 if _fail else 0)
