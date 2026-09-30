#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""② 퍼콜레이션 표지 — 인계 (1저자 10-01 *"퍼콜레이션은 그렇게 가고"* · J20-b · J20-l) · 원장 LHS-19 · LHS-20.

  python3 webapp/test_percolation_labels.py      # 종료코드 0 = PASS

인계표에 ② 퍼콜레이션 열을 싣는 날, 같은 묶음에서 웹앱 설명을 코드 정의 (`calc_percolation` · `calc_ionic_active_am`) 와 J20-b F3
한정어에 맞춘다: 성분 수는 외톨이 SE 를 포함하고 문턱 10 은 출처 없는 상수 · 관통률은 밴드 규칙의 그래프 관통 (솔버 전류 관통과 다름) ·
top-reachable 은 위 밴드의 외톨이도 세며 관통률의 **상위집합** · 이온 활성 AM 은 top-reachable SE 와의 접촉 유무만 본다 (coverage 무관).

  [W] 웹앱 — 영문 라벨 둘 · 역방향 라벨 맵 짝 · 케이스 툴팁 넷
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'scripts'))

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
    print('[W] 웹앱 — 퍼콜레이션 표지 (F3 · LHS-19 · LHS-20)')
    import app as A
    en = next((v for v in vars(A).values()
               if isinstance(v, dict) and isinstance(v.get('SE Cluster 수'), str) and isinstance(v.get('Ionic Active AM(%)'), str)), {})
    lc, li = en.get('SE Cluster 수', ''), en.get('Ionic Active AM(%)', '')
    chk('W1 영문 라벨 SE Cluster 수 — "percolating" 이 아니다 (전체 성분 · 외톨이 포함)',
        bool(lc) and 'percolating' not in lc.lower() and 'isolated' in lc.lower(), repr(lc))
    chk('W2 영문 라벨 Ionic Active AM — top-reachable SE 와의 접촉 (SE 에 닿기만 한 것이 아니다)',
        bool(li) and 'top-reachable' in li.lower(), repr(li))
    html = open(os.path.join(HERE, 'templates', 'single.html'), encoding='utf-8').read()
    chk('W3 역방향 라벨 맵이 새 영문 라벨 둘을 되돌린다 · 옛 키 없음',
        f"'{lc}': 'SE Cluster 수'" in html and f"'{li}': 'Ionic Active AM(%)'" in html
        and 'SE percolating clusters (n≥10 / total)' not in html and 'Ionically-active AM, SE-touching (%)' not in html)
    b = _tip_block(html, 'SE Cluster 수') or ''
    chk('W4 SE Cluster 수 툴팁 — 외톨이 SE 포함 · 문턱 10 은 출처 없는 상수 (LHS-19)',
        '외톨이' in b and '출처 없는' in b and 'LHS-19' in b, b[:200])
    b = _tip_block(html, 'SE Percolation(%)') or ''
    chk('W5 SE Percolation 툴팁 — 밴드 규칙의 그래프 관통 · 솔버 (전류) 관통과 다름 · 0 % = 관통 성분 없음 (LHS-19 · J20-b)',
        '밴드' in b and '솔버' in b and '0 %' in b and 'LHS-19' in b, b[:200])
    b = _tip_block(html, 'Top Reachable(%)') or ''
    chk('W6 Top Reachable 툴팁 — 외톨이도 센다 (LHS-19) · 관통률의 상위집합 (dead-end = 차이) · 옛 거꾸로 된 문장 없음',
        '외톨이' in b and 'LHS-19' in b and 'f_SE^sep < SE percolation (%) 만큼이' not in b and '− SE percolation' in b, b[:240])
    b = _tip_block(html, 'Ionic Active AM(%)') or ''
    chk('W7 Ionic Active AM 툴팁 — 접촉 유무만 · coverage 무관 (LHS-20) · 위 밴드 외톨이 SE 도 센다',
        'coverage' in b and 'LHS-20' in b and '외톨이' in b, b[:200])


def main():
    try:
        section_w()
    except Exception as e:  # 예외도 실패로 센다
        import traceback
        traceback.print_exc()
        _fail.append(f'section_w 예외 {type(e).__name__}: {e}')
    print(f'\n{_ok} PASS · {len(_fail)} FAIL')
    if _fail:
        for f in _fail:
            print('  -', f)
        sys.exit(1)


if __name__ == '__main__':
    main()
