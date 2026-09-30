#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""coverage 인계 범위 · physics 포화 표지 — J20-m (1저자 10-01 *"그렇게 하자"*) · 원장 LHS-25 · SELF-74.

  python3 webapp/test_coverage_handover_scope.py      # 종료코드 0 = PASS

결정: LHS 인계 디스크립터의 피복률 = **기하면적 열만** (LIGGGHTS c_cpl[22] 기하 교차 원판 · 이름만 hertz · L1-04).
physics v1 · v2 는 인계하지 않는다 — 접촉마다 추정한 소성 면적을 **표면 한도 없이** 더해 SE 가 많은 침대에서
100 % 에 붙고 (5번 배치: v1 ≥ 99 % 침대 LHS 29/130 · lhsx 62/64), v2 는 같은 원인으로 AM–AM 쪽 분모가 무너진다
(18 침대 빈칸 · 기하면적으로는 AM 1,320,178 개 중 0).  physics 는 망 전도도 · 등급 · 웹앱에서 **바꾸지 않는다** — 그쪽 쓰임새
(σ_ionic T1 의 면적 선택 포함) 는 코드 함수 검토 전이라 이 결정이 닫지 않는다 (1저자 10-01 *"이걸로 닫지 말고 아직"*).

  [C] 웹앱 표지 — 케이스 툴팁 (Coverage AM_P · AM_S · AM) 에 포화 · 인계 제외 한정어 · ③ 이후 낡은 문장
      ("v2 는 아직 표시하지 않는다") 제거 · v2 절 머리 · v2 행 툴팁 · 쉬운 설명 (포화 · "가장 믿을 만한" 철회)
  [K] 코드 · 데이터 — v2 분모 무효를 "이웃 AM 과 깊이 겹친 입자" 로 설명하던 주석 정정 (SELF-74) ·
      커밋된 인계표에 physics 열이 없다 (σ · 등급 쪽 physics 사용은 이 결정 밖 — 열림)
"""
import csv
import os
import re
import sys

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


def _tip_block(src, key):
    """METRIC_TIPS 안의 한 항목 `'key': { … }` 본문 (중괄호 균형) — 없으면 None."""
    i = src.find(f"'{key}': {{")
    if i < 0:
        return None
    j = src.index('{', i)
    depth = 0
    for k in range(j, len(src)):
        c = src[k]
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return src[j:k + 1]
    return None


def section_c():
    print('[C] 웹앱 표지 — 포화 · 인계 제외 (J20-m · LHS-25)')
    html = open(os.path.join(HERE, 'templates', 'single.html'), encoding='utf-8').read()
    for key in ('Coverage AM_P(%)', 'Coverage AM_S(%)', 'Coverage AM(%)'):
        b = _tip_block(html, key) or ''
        chk(f'C1 {key} 툴팁 = Physics 계열 포화 · 인계 제외 한정어 (포화 · LHS-25 · J20-m)',
            '포화' in b and 'LHS-25' in b and 'J20-m' in b, b[:200])
    chk('C2 ③ 이후 낡은 문장 ("v2 … 아직 표시하지 않는다") 없음', '아직 표시하지 않는다' not in html)
    import app as A
    tables = {'network_summary': {'columns': ['지표', 'H', 'P', 'Δ'], 'data': []}}
    A.inject_physics_v2_rows(tables, {'coverage_AM_mean_physics_v2': 41.0, 'coverage_AM_P_mean_physics_v2': 38.0,
                                      'coverage_AM_S_mean_physics_v2': 44.0})
    rows = [r[0] for r in tables['network_summary']['data']]
    hdr = next((r for r in rows if r.strip().startswith('──')), '')
    chk('C3 v2 절 머리 = 후보 · 미검증 + 포화 · 인계 제외 (LHS-25)',
        '후보' in hdr and '미검증' in hdr and '포화' in hdr and '인계 제외' in hdr and 'LHS-25' in hdr, hdr)
    v2_labels = [r.strip() for r in rows if 'physics v2' in r and not r.strip().startswith('──')]
    chk('C4a v2 행 셋 (AM · AM_P · AM_S)', len(v2_labels) == 3, repr(v2_labels))
    for lab in v2_labels:
        b = _tip_block(html, lab) or ''
        chk(f'C4 v2 행 툴팁 있음 · 분모 무효 · 포화 · LHS-25 — {lab}',
            '분모' in b and '포화' in b and 'LHS-25' in b, b[:160] if b else '툴팁 없음')
    plain = getattr(A, '_GRADE_PLAIN', {})
    for key in ('coverage_AM_P_mean_physics', 'coverage_AM_S_mean_physics'):
        t = plain.get(key, '')
        chk(f'C5 쉬운 설명 {key} — SE 가 많으면 100 % 에 붙는다 (포화)', '100 %' in t and '포화' in t, t)
    t_r = plain.get('coverage_AM_mean_physics_rough', '')
    chk('C6 쉬운 설명 B3 — "가장 믿을 만한" 철회 (인용 뿌리 감사 E7 · MI-5 와 같은 계열)',
        bool(t_r) and '가장 믿을 만한' not in t_r, t_r)


def section_k():
    print('[K] 코드 · 데이터 — 주석 정정 (SELF-74) · 인계표에 physics 없음')
    src = open(os.path.join(SCRIPTS, 'coverage_physics_vs_hertzian.py'), encoding='utf-8').read()
    chk('K1 v2 분모 무효를 "이웃 AM 과 깊이 겹친 입자" 로 설명하지 않는다 (SELF-74)',
        '이웃 AM 과 깊이 겹친 입자' not in src)
    chk('K2 대신 원인 = 접촉별 추정 면적 합에 표면 한도가 없다 (LHS-25) 를 적는다',
        '표면 한도' in src and 'LHS-25' in src)
    #  (σ · 등급에서 physics 를 어떻게 쓸지는 이 결정이 닫지 않는다 — σ_ionic T1 의 면적 선택은 코드 함수 검토 전 ·
    #   1저자 10-01 "이걸로 닫지 말고 아직".  그래서 등급 축 · σ 채널을 고정하는 시험을 두지 않는다.)
    for rel in ('docs/data/lhs_handover_20260930.csv', 'docs/data/lhsx_handover_20260930.csv'):
        p = os.path.join(ROOT, rel)
        with open(p, encoding='utf-8', newline='') as fh:
            head = next(csv.reader(fh))
        phys = [c for c in head if 'physics' in c.lower()]
        geo = [c for c in head if re.fullmatch(r'coverage_AM_(P|S|total)_hertz_pct', c)]
        chk(f'K4 {os.path.basename(rel)} — physics 열 없음 · 기하면적 피복 셋 있음', not phys and len(geo) == 3,
            f'physics={phys} geo={geo}')


def main():
    for fn in (section_c, section_k):
        try:
            fn()
        except Exception as e:  # 한 절의 예외가 다른 절을 가리지 않게
            import traceback
            traceback.print_exc()
            _fail.append(f'{fn.__name__} 예외 {type(e).__name__}: {e}')
    print(f'\n{_ok} PASS · {len(_fail)} FAIL')
    if _fail:
        for f in _fail:
            print('  -', f)
        sys.exit(1)


if __name__ == '__main__':
    main()
