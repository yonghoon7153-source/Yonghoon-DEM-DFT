#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""⑤⑥⑦ 인계 한정어 — 웹앱 같은 묶음 (J20-s · 1저자 비준 10-04 · J20-l: 생성기 열 사전과 같은 정의 · 이름 · 한정어).

  A  F1 근접쌍 CN 툴팁 — 10 nm = 출처 없는 모델 상수 (옛 문구 "Tabor plastic film 의 typical lateral spread 거리" 는 근거 없음) · 항등식 · 오타
  B  경로 접촉 면적 (Path Hop Area · Bottleneck) — 선별 표본 통계 (덩어리마다 고른 경로 30 개) · 인계 제외 (LHS-32) · 케이스 · 그룹 툴팁
  C  파괴 (Severe % · fracture_index) — LHS-31 한정 (마지막 프레임 힘 → 손상 하한 · 벽 · 판 접촉 제외 · K_IC_P 0.3 = 소결 펠릿값) · 쉬운 설명
  D  면적 — F2 eff_area 식 (2 × area_SE_SE_total / (N_SE · 4π r_SE²)) · A_dem_geometric (c_cpl[22] 교차원 · Hertz πR*δ 의 ≈ 2 배)

  python3 webapp/test_s567_labels.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
_ok, _fail = 0, []


def chk(name, cond, why=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'  ({why})' if why else ''))


def _read(rel):
    with open(os.path.join(ROOT, rel), encoding='utf-8') as f:
        return f.read()


def _block(src, key, n=900):
    i = src.find(key)
    return src[i:i + n] if i >= 0 else ''


def main():
    single = _read('webapp/templates/single.html')
    group = _read('webapp/templates/group.html')
    app = _read('webapp/app.py')

    print('A  F1')
    f1 = _block(single, "'SE-SE CN (plastic-augmented) [F1]': {")
    f1x = _block(single, "'(F1 extra near-contact pairs)': {")
    chk('A1 F1 툴팁 — 10 nm = 출처 없는 모델 상수 · J20-s · 항등식 2 × n_extra / N_SE', '출처 없는 모델 상수' in f1 and 'J20-s' in f1
        and '2 × n_extra / N_SE' in f1, f1[:200])
    chk('A2 근접쌍 개수 툴팁 — 근거 없는 "Tabor plastic film 의 typical lateral spread 거리" 서술 없음 · 출처 없는 모델 상수',
        'typical lateral spread' not in single and '출처 없는 모델 상수' in f1x, f1x[:200])
    chk('A3 오타 "near-miss pair 도 carbon:" 없음', 'pair 도 carbon:' not in single)

    print('B  경로 접촉 면적')
    for key in ("'Path Hop Area mean(μm²)': {", "'Path Bottleneck(μm²)': {"):
        b = _block(single, key, 700)
        chk(f'B1 케이스 툴팁 {key[1:12]}… — 선별 표본 · LHS-32 · 인계 제외', '선별 표본' in b and 'LHS-32' in b and '인계' in b, b[:160])
    for key in ("'Hop Area': '", "'Bottleneck': '"):
        b = _block(group, key, 500)
        chk(f'B2 그룹 툴팁 {key[1:10]}… — 선별 표본 · LHS-32', '선별 표본' in b and 'LHS-32' in b, b[:160])

    print('C  파괴')
    for key in ("'Severe %': {", "'fracture_index (severe/total)': {"):
        b = _block(single, key, 900)
        chk(f'C1 케이스 툴팁 {key[1:16]}… — LHS-31 · 마지막 프레임 · 하한 · 벽 · K_IC_P 0.3', all(w in b for w in ('LHS-31', '마지막 프레임', '하한',
            '벽', 'K_IC_P 0.3')), b[:160])
    for key in ("'fracture_index_force': '", "'__frac_severe_force_pct': '"):
        b = _block(app, key, 500)
        chk(f'C2 쉬운 설명 {key[1:24]}… — 마지막 순간의 힘 · 실제보다 작게 (하한)', '마지막' in b and '하한' in b, b[:160])

    print('D  면적')
    f2 = _block(single, "'SE-SE CN (area-weighted)    [F2]': {")
    chk('D1 F2 eff_area 툴팁 — 2 × area_SE_SE_total / (N_SE · 4π r_SE²) · A_dem_geometric · ≈ 2 배', '2 × area_SE_SE_total' in f2
        and 'A_dem_geometric' in f2 and '≈ 2 배' in f2, f2[:200])
    am = _block(group, "'AM-AM Mean Area': '", 500)
    chk('D2 그룹 AM-AM Mean Area — A_dem_geometric · c_cpl[22] 교차원 · ≈ 2 배', 'A_dem_geometric' in am and '≈ 2 배' in am, am[:200])

    print(f'\n{_ok}/{_ok + len(_fail)} PASS' + ('' if not _fail else '  — FAIL: ' + ' · '.join(_fail)))
    return 1 if _fail else 0


if __name__ == '__main__':
    sys.exit(main())
