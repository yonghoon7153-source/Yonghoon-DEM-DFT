#!/usr/bin/env python3
"""Parse a webapp '📋 전체 복사 (AI용)' button paste → append/update a row in the 3D collection CSV.

The paste = the full text the dashboard copy button produces (case header + 입자 정보 +
네트워크 지표 + 취성 파괴 + MPM 결과 파라미터).  De-dupes by case name.

  python3 scripts/parse_case_paste.py <paste.txt> [--csv docs/data/case_3d_collection.csv]
"""
import argparse
import csv
import os
import re

COLS = ['case', 'mAh', 'ps_label', 'p_frac', 'am_wt', 'dem_porosity_pct', 'mpm_porosity_pct',
        'dem_cov_amp_hertz', 'dem_cov_amp_tabor', 'mpm_cov_amp_plastic_tabor', 'mpm_cov_amp_rigid_tabor',
        'sigma_ionic_hertz_mScm', 'sigma_ionic_physics_mScm', 'thickness_um', 'fracture_severe_pct',
        'n_am', 'n_se', 'r_se', 'e_se',
        #  ★ 10-06 (C2-⑥ · LHS-25) — 합집합 cap Physics 피복은 새 칸 (맨 끝 · 옛 열 위치 그대로).  dem_cov_amp_tabor = 옛 뜻 (합-클립) 유지.
        'dem_cov_amp_physics_union']


def _g(pat, txt, grp=1, flags=0):
    m = re.search(pat, txt, flags)
    return m.group(grp) if m else ''


def _num(s):
    """표 칸 → 숫자 문자열 · 숫자가 아니면 ('—' · '' · 사유) 빈칸 (0 으로 바꾸지 않는다)."""
    s = (s or '').strip()
    return s if re.fullmatch(r'\d+(?:\.\d+)?', s) else ''


def parse(txt):
    d = {c: '' for c in COLS}
    d['case'] = _g(r'#\s*(input_\S+)', txt)
    d['mAh'] = _g(r'(\d+)\s*mAh', d['case']) or _g(r'(\d+)\s*mAh', txt)
    d['ps_label'] = _g(r'P:S\s*=\s*(\d+:\d+)', txt)
    if d['ps_label']:
        p, q = (float(x) for x in d['ps_label'].split(':'))
        d['p_frac'] = f'{p / (p + q):.3f}'
    d['am_wt'] = _g(r'AM:SE\s*=\s*(\d+(?:\.\d+)?)\s*:', txt)
    d['dem_porosity_pct'] = _g(r'Porosity\s*ε\s*\(%\)\s*\t([\d.]+)', txt)
    d['thickness_um'] = _g(r'Electrode thickness T \(μm\)\s*\t([\d.]+)', txt)
    #  ★ 10-06 (C2-⑥ · LHS-25) — 웹앱이 이 행 이름 뒤에 Physics 열 정의 (' · Physics 열 = 합집합 cap …') 를 붙이고 옛 Physics v1
    #    (합-클립) 값을 바로 아래 '└ Physics legacy 합-클립' 줄로 옮겼다.  옛 정규식은 그 줄을 못 찾아 두 칸이 조용히 비었다
    #    (scripts/test_parse_case_paste_union.py).  합집합 → dem_cov_amp_physics_union · 옛 칸 = legacy 줄 (없으면 빈칸 — 합집합 값을 넣지 않는다).
    m = re.search(r'Coverage of AM_P by SE, cov_AM_P \(%\)([^\t\n]*)\t([^\t\n]*)\t([^\t\n]*)', txt)
    if m:
        d['dem_cov_amp_hertz'] = _num(m.group(2))
        if '합집합' in m.group(1):
            d['dem_cov_amp_physics_union'] = _num(m.group(3))
            rest = txt[m.end():]
            nxt = rest.split('\n', 2)[1] if rest.count('\n') >= 1 else ''
            lm = re.match(r'\s*└ Physics legacy 합-클립[^\t\n]*\t[^\t\n]*\t([^\t\n]*)', nxt)
            d['dem_cov_amp_tabor'] = _num(lm.group(1)) if lm else ''
        else:
            d['dem_cov_amp_tabor'] = _num(m.group(3))
    m = re.search(r'σ_ionic — full network solver \(mS/cm\)\s*\t([\d.]+)\t([\d.]+)', txt)
    if m:
        d['sigma_ionic_hertz_mScm'], d['sigma_ionic_physics_mScm'] = m.group(1), m.group(2)
    d['mpm_porosity_pct'] = _g(r'공극률 \(porosity\)\s*\t([\d.]+)', txt)
    m = re.search(r'coverage AM_P.*?\t\s*\d+\s*/\s*(\d+)\s*%\s*\(강체\s*\d+/(\d+)\)', txt)
    if m:
        d['mpm_cov_amp_plastic_tabor'], d['mpm_cov_amp_rigid_tabor'] = m.group(1), m.group(2)
    m = re.search(r'Severe\s*%\s*\t([\d.]+)\t([\d.]+)', txt)            # δ-based \t Force-based(★)
    d['fracture_severe_pct'] = m.group(2) if m else _g(r'Severe\s*%\s*\t([\d.]+)', txt)
    namp = _g(r'\bAM_P\s*\t(\d+)\t', txt)
    nams = _g(r'\bAM_S\s*\t(\d+)\t', txt)
    n_am = (int(namp) if namp else 0) + (int(nams) if nams else 0)
    d['n_am'] = str(n_am) if n_am else ''
    d['n_se'] = _g(r'\bSE\s*\t(\d+)\t', txt)
    d['r_se'] = _g(r'\bSE\s*\t\d+\s*\t([\d.]+)', txt)      # SE radius (µm) from particle table — variant axis
    d['e_se'] = _g(r'E_SE:\s*([\d.]+)', txt)               # DEM E_SE (GPa) from header — variant axis
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('paste')
    ap.add_argument('--csv', default='docs/data/case_3d_collection.csv')
    a = ap.parse_args()
    d = parse(open(a.paste, encoding='utf-8').read())
    if not d['case']:
        raise SystemExit('no case name (# input_...) found — is this a copy-button paste?')
    rows = [r for r in csv.DictReader(open(a.csv))] if os.path.exists(a.csv) else []
    rows = [r for r in rows if r.get('case') != d['case']]          # de-dupe
    os.makedirs(os.path.dirname(a.csv) or '.', exist_ok=True)
    with open(a.csv, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, '') for c in COLS})
        w.writerow(d)
    print(f"+ {d['case']}: DEM={d['dem_porosity_pct']}% MPM={d['mpm_porosity_pct']}% "
          f"AM={d['am_wt']}wt P:S={d['ps_label']} frac_severe={d['fracture_severe_pct']}% "
          f"→ {a.csv} ({len(rows) + 1} cases)")


if __name__ == '__main__':
    main()
