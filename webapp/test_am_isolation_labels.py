#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AM 고립 비율 (vulnerable) 표지 — 7c (1저자 10-01 *"ㄱㄱ 하자"* · J20-k 7c · J20-l) · 원장 LHS-23.

  python3 webapp/test_am_isolation_labels.py      # 종료코드 0 = PASS

`am_vulnerable_pct` · `AM_P_vulnerable_pct` · `AM_S_vulnerable_pct` 는 **SE 접촉이 0–1 개인 AM 의 비율** 이다
(`dem_analysis_core.calc_am_isolation_risk` — 접촉 개수만 센다 · coverage 를 읽지 않는다).  09-19 census 가 이것을
"coverage 문턱 기반" 으로 분류했고 (LHS-23) 웹앱 영문 라벨 · 쉬운 설명 · 피팅 보고서도 coverage 처럼 설명했다.
7c 에서 인계표에 싣는 날, 같은 묶음에서 웹앱 설명을 코드 정의에 맞춘다 (J20-l).

  [W] 웹앱 — 영문 라벨 (low-coverage 아님) · 역방향 라벨 맵 짝 · 쉬운 설명 (덮임이 아니라 닿은 개수) · 케이스 툴팁 한정어
  [R] 피팅 보고서 — v_AM 설명
"""
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


def section_w():
    print('[W] 웹앱 — 고립 비율은 접촉 개수 기준 (coverage 아님 · LHS-23)')
    import app as A
    en = getattr(A, 'EN_LABELS', None) or {}
    if not en:                                  # 이름이 달라도 찾는다 — 한국어 행 이름 → 영문 라벨 dict
        en = next((v for v in vars(A).values()
                   if isinstance(v, dict) and 'AM Vulnerable(%)' in v and isinstance(v.get('AM Vulnerable(%)'), str)), {})
    lab = en.get('AM Vulnerable(%)', '')
    chk('W1 영문 라벨 — "low-coverage" 아님 · SE 접촉 0–1 개로 정의',
        bool(lab) and 'coverage' not in lab.lower() and '0–1' in lab and 'contact' in lab.lower(), repr(lab))
    html = open(os.path.join(HERE, 'templates', 'single.html'), encoding='utf-8').read()
    chk('W2 single.html 역방향 라벨 맵이 새 영문 라벨을 AM Vulnerable(%) 로 되돌린다 · 옛 low-coverage 키는 없다',
        bool(lab) and f"'{lab}': 'AM Vulnerable(%)'" in html and 'low-coverage' not in html)
    plain = getattr(A, '_GRADE_PLAIN', {})
    t = plain.get('__vulnerable_pct', '')
    chk('W3 쉬운 설명 — 덮인 정도가 아니라 닿은 개수 (0–1 군데) · coverage 로 설명하지 않는다',
        bool(t) and '덮여' not in t and '0–1' in t and '닿' in t, t)
    b = _tip_block(html, 'AM Vulnerable(%)') or ''
    chk('W4 케이스 툴팁 — 접촉 개수 기준 · coverage 아님 한정어 (LHS-23)',
        'LHS-23' in b and '접촉 개수' in b and 'coverage' in b, b[:200])
    for key in ('  ├ AM_P Vulnerable(%)', '  └ AM_S Vulnerable(%)'):
        bb = _tip_block(html, key) or ''
        chk(f'W5 상별 툴팁에도 같은 한정어 — {key.strip()}', 'LHS-23' in bb and '접촉 개수' in bb, bb[:160])


def section_r():
    print('[R] 피팅 보고서 — v_AM 설명')
    src = open(os.path.join(SCRIPTS, 'generate_fitting_report.py'), encoding='utf-8').read()
    line = next((ln for ln in src.splitlines() if 'v_AM = AM_S_vulnerable_pct/100' in ln), '')
    chk('R1 v_AM 설명 — "coverage 낮아" 아님 · SE 접촉 0–1 개 (LHS-23)',
        bool(line) and 'coverage 낮아' not in line and '0–1' in line and 'LHS-23' in line, line)


def main():
    for fn in (section_w, section_r):
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
