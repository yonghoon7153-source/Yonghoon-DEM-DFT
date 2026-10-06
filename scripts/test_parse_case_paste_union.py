#!/usr/bin/env python3
"""parse_case_paste ↔ 웹앱 '📋 전체 복사' 의 Coverage 행 — C2-⑥ (10-06 · 합집합 cap) 뒤에도 조용히 비지 않는가.

C2-⑥ 이 케이스 표의 Coverage AM_P 행 이름 뒤에 Physics 열 정의 (' · Physics 열 = 합집합 cap …') 를 붙이고, 옛 Physics v1
(합-클립) 값을 바로 아래 '└ Physics legacy 합-클립 …' 줄로 옮겼다.  옛 파서 정규식 (`… cov_AM_P \\(%\\)\\s*\\t`) 은 그 줄을
못 찾아 **dem_cov_amp_* 두 칸이 조용히 빈다** (규율 ⑤ — 부분집합 · 형식 사각의 false-green 과 같은 부류).
라벨 문자열은 webapp/app.py 원문에서 읽는다 (생산자 ↔ 소비자 묶기 — 웹앱 라벨이 바뀌면 이 시험이 먼저 깨진다).

  P1 옛 붙여넣기 (정의 없는 라벨 · 두 수)           → hertz · tabor (= 옛 Physics v1) · union 빈칸
  P2 새 붙여넣기 (합집합 라벨 + legacy 줄)          → hertz · union · tabor = legacy 줄 값
  P3 새 붙여넣기 · 옛 케이스 (합집합 '—' + legacy)   → union 빈칸 (0 아님) · tabor = legacy
  P4 합집합 라벨인데 legacy 줄이 없다                → tabor 빈칸 (합집합 값을 옛 칸에 넣지 않는다)
  P5 CSV 열 = 옛 열 순서 그대로 + 새 열은 맨 끝 (위치 소비자 보호)
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import parse_case_paste as P  # noqa: E402

_fails = []


def chk(name, cond):
    print(f"  {'✓' if cond else '✗'} {name}")
    if not cond:
        _fails.append(name)


def _app_labels():
    src = open(os.path.join(ROOT, 'webapp', 'app.py'), encoding='utf-8').read()
    m = re.search(r"'Coverage AM_P\(%\)':\s*'([^']*)'", src)
    l = re.search(r"^UNION_LEGACY_ROW_LABEL\s*=\s*'([^']*)'", src, re.M)
    assert m and l, 'webapp/app.py 에서 Coverage AM_P 라벨 · UNION_LEGACY_ROW_LABEL 을 못 찾았다'
    return m.group(1), l.group(1)


OLD_COLS = ['case', 'mAh', 'ps_label', 'p_frac', 'am_wt', 'dem_porosity_pct', 'mpm_porosity_pct',
            'dem_cov_amp_hertz', 'dem_cov_amp_tabor', 'mpm_cov_amp_plastic_tabor', 'mpm_cov_amp_rigid_tabor',
            'sigma_ionic_hertz_mScm', 'sigma_ionic_physics_mScm', 'thickness_um', 'fracture_severe_pct',
            'n_am', 'n_se', 'r_se', 'e_se']


def main():
    lab, leg = _app_labels()
    head = '# input_6mAh_test\n'
    old = head + 'Coverage of AM_P by SE, cov_AM_P (%)\t17.5\t43.9\t+150.9%\n'
    new = head + f'{lab}\t18.4\t39.7\t+116%\n    {leg}\t—\t48.3\t\n'
    new_oldcase = head + f'{lab}\t18.4\t—\t\n    {leg}\t—\t48.3\t\n'
    new_noleg = head + f'{lab}\t18.4\t39.7\t+116%\n'

    print('P1 옛 붙여넣기')
    d = P.parse(old)
    chk('P1 hertz 17.5 · tabor 43.9 · union 빈칸',
        (d.get('dem_cov_amp_hertz'), d.get('dem_cov_amp_tabor'), d.get('dem_cov_amp_physics_union')) == ('17.5', '43.9', ''))
    print('P2 새 붙여넣기 (합집합 + legacy)')
    d = P.parse(new)
    chk('P2 hertz 18.4 · union 39.7 · tabor = legacy 48.3',
        (d.get('dem_cov_amp_hertz'), d.get('dem_cov_amp_physics_union'), d.get('dem_cov_amp_tabor')) == ('18.4', '39.7', '48.3'))
    print('P3 새 붙여넣기 · 옛 케이스 (합집합 —)')
    d = P.parse(new_oldcase)
    chk('P3 union 빈칸 (0 · legacy 아님) · tabor = legacy 48.3 · hertz 18.4',
        (d.get('dem_cov_amp_physics_union'), d.get('dem_cov_amp_tabor'), d.get('dem_cov_amp_hertz')) == ('', '48.3', '18.4'))
    print('P4 합집합 라벨 · legacy 줄 없음')
    d = P.parse(new_noleg)
    chk('P4 tabor 빈칸 (합집합 값을 옛 칸에 넣지 않는다) · union 39.7',
        (d.get('dem_cov_amp_tabor'), d.get('dem_cov_amp_physics_union')) == ('', '39.7'))
    print('P5 CSV 열')
    chk('P5 옛 열 순서 그대로 + dem_cov_amp_physics_union 은 맨 끝',
        P.COLS[:len(OLD_COLS)] == OLD_COLS and P.COLS[len(OLD_COLS):] == ['dem_cov_amp_physics_union'])

    n = 5
    print(f'\n{n - len(_fails)}/{n} 통과')
    return 1 if _fails else 0


if __name__ == '__main__':
    sys.exit(main())
