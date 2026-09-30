#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""경로 기준 고립 AM (= 100 − 이온 활성) 과 그 분해 표지 — LHS 인계 v1.1 ①② (1저자 비준 10-01 · J20-l).

  python3 webapp/test_ionic_isolation_labels.py      # 종료코드 0 = PASS

인계표 v1.1 이 `am_ionic_isolated_pct` (= 100 − ionic_active_pct) 와 그 분해 (`ionic_dead_pct` = SE 는 닿았지만 그 SE 가 위 띠
(분리막 쪽) 로 안 이어짐 · `ionic_no_se_pct` = SE 접촉 0) 를 싣는 날, 웹앱도 **같은 이름 · 같은 정의 · 같은 한정어**로 보여 준다.
두 "고립" 을 섞지 않는 것이 요점이다 — `am_vulnerable_pct` 는 고립 **위험** (SE 접촉 0–1 개 · 접촉 개수) 이고, 경로 기준 고립은
이온이 실제로 못 가는 AM 이다 (접촉이 둘 이상인데 고립일 수도, 하나뿐인데 활성일 수도 있다).

  [W] 웹앱 — 영문 라벨 · 역방향 라벨 맵 · 케이스 툴팁 · 표 순서 · 옛 케이스 보정 (분해 키가 없던 세대) · 그룹 비교 · MD 보고서 · 쉬운 설명
  [B] 표 재구성기 (rebuild_tables_from_metrics) — 같은 줄 · 같은 키
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRIPTS = os.path.join(ROOT, 'scripts')
sys.path.insert(0, HERE)
sys.path.insert(0, SCRIPTS)

_ok, _fail = 0, []

PARENT = 'Ionic Isolated AM(%)'
DEAD = '  ├ Isolated: SE not linked(%)'
NOSE = '  └ Isolated: no SE contact(%)'


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
    print('[W] 웹앱 — 경로 기준 고립 = 100 − 활성 · 분해 (단절 · 무접촉) · 고립 위험과 다른 양')
    import app as A
    en = next((v for v in vars(A).values()
               if isinstance(v, dict) and 'AM Vulnerable(%)' in v and isinstance(v.get('AM Vulnerable(%)'), str)), {})
    lp, ld, ln = en.get(PARENT, ''), en.get(DEAD, ''), en.get(NOSE, '')
    chk('W1 영문 라벨 — 경로 기준 · 100 − active (접촉 개수 기준의 vulnerable 과 다른 말) · coverage 없음',
        bool(lp) and 'path' in lp.lower() and '100 − active' in lp and 'vulnerab' not in lp.lower() and 'coverage' not in lp.lower(), repr(lp))
    chk('W2 영문 라벨 — 분해 두 줄 (SE 는 닿았지만 분리막 쪽으로 안 이어짐 · SE 접촉 0) · 트리 기호 유지',
        ld.lstrip().startswith('├') and 'separator' in ld and 'SE' in ld
        and ln.lstrip().startswith('└') and 'no SE contact' in ln, f'{ld!r} · {ln!r}')
    html = open(os.path.join(HERE, 'templates', 'single.html'), encoding='utf-8').read()
    chk('W3 single.html 역방향 라벨 맵 — 세 영문 라벨을 내부 이름으로 되돌린다',
        all(lab and f"'{lab}': '{key}'" in html for lab, key in ((lp, PARENT), (ld, DEAD), (ln, NOSE))))   # 자식 줄은 앞 공백까지 (기존 규약)
    b = _tip_block(html, PARENT) or ''
    chk('W4 케이스 툴팁 (부모) — 경로 기준 · = 100 − Ionic Active = 단절 + 무접촉 · 고립 위험 (AM Vulnerable · 접촉 0–1 개) 과 다르다',
        '경로 기준' in b and '100 −' in b and '단절' in b and '무접촉' in b and '고립 위험' in b and 'AM Vulnerable' in b, b[:240])
    bd, bn = _tip_block(html, DEAD) or '', _tip_block(html, NOSE) or ''
    chk('W5 케이스 툴팁 (분해) — 단절 = SE 는 닿았지만 위 띠 (분리막 쪽) 로 안 이어짐 · 무접촉 = SE 접촉 0',
        '닿았지만' in bd and '분리막' in bd and 'SE 접촉 0' in bn, f'{bd[:160]} · {bn[:160]}')
    #  표 순서 = normalize_network_summary_layout 안의 지역 목록 _CANONICAL_ROW_ORDER (Pass F) — 소스에서 그대로 읽는다
    import ast
    order = None
    for node in ast.walk(ast.parse(open(os.path.join(HERE, 'app.py'), encoding='utf-8').read())):
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == '_CANONICAL_ROW_ORDER' for t in node.targets):
            order = ast.literal_eval(node.value)
    ok6 = False
    if order:
        o = list(order)
        i = o.index('Ionic Active AM(%)')
        ok6 = o[i + 1:i + 4] == [PARENT, DEAD.strip(), NOSE.strip()] and o.index('AM Vulnerable(%)') == i + 4
    chk('W6 표 순서 — 활성 → 경로 기준 고립 → 단절 → 무접촉 → 고립 위험 (AM Vulnerable)', ok6,
        str(order[order.index('Ionic Active AM(%)'):order.index('Ionic Active AM(%)') + 6]) if order else '순서 목록 없음')

    #  옛 세대 케이스 (분해 키 없음) — 부모 줄은 활성에서 유도 · 분해 두 줄은 '—' (측정 안 한 것을 0 으로 채우지 않는다)
    tables = {'network_summary': {'data': [['── 활성도 ──', '', '', ''],
                                           ['Ionic Active AM(%)', '97.5', '97.5', '0%'],
                                           ['AM Vulnerable(%)', '1.0', '1.0', '0%']]}}
    A.normalize_network_summary_layout(tables, {'ionic_active_pct': 97.5})
    rows = {r[0].strip(): r for r in tables['network_summary']['data'] if r and isinstance(r[0], str)}
    labs = [r[0].strip() for r in tables['network_summary']['data'] if r and isinstance(r[0], str)]
    ok7 = (PARENT in rows and rows[PARENT][1] in ('2.5', 2.5) and rows.get(DEAD.strip(), [None, None])[1] == '—'
           and rows.get(NOSE.strip(), [None, None])[1] == '—'
           and labs.index(PARENT) == labs.index('Ionic Active AM(%)') + 1)
    chk('W7 옛 세대 케이스 — 부모 줄 = 100 − 활성 (2.5) 을 활성 바로 뒤에 · 분해 두 줄은 — (0 으로 안 채움)', ok7,
        str([r for r in tables['network_summary']['data']]))
    #  새 세대 — 분해 키가 있으면 값으로
    tables2 = {'network_summary': {'data': [['Ionic Active AM(%)', '60.0', '60.0', '0%'],
                                            ['AM Vulnerable(%)', '1.0', '1.0', '0%']]}}
    A.normalize_network_summary_layout(tables2, {'ionic_active_pct': 60.0, 'am_ionic_isolated_pct': 40.0,
                                                 'ionic_dead_pct': 30.0, 'ionic_no_se_pct': 10.0})
    rows2 = {r[0].strip(): r for r in tables2['network_summary']['data'] if r and isinstance(r[0], str)}
    chk('W8 분해 키가 있는 케이스 (표에 줄이 없던 옛 CSV) — 부모 40.0 · 단절 30.0 · 무접촉 10.0',
        rows2.get(PARENT, [None, None])[1] in ('40.0', 40.0) and rows2.get(DEAD.strip(), [None, None])[1] in ('30.0', 30.0)
        and rows2.get(NOSE.strip(), [None, None])[1] in ('10.0', 10.0), str(tables2['network_summary']['data']))

    params = getattr(A, 'GROUP_PARAMS', None) or next(
        (v for v in vars(A).values() if isinstance(v, list) and any(isinstance(x, tuple) and len(x) == 4
                                                                  and x[2] == 'ionic_active_pct' for x in v)), [])
    keys = [x[2] for x in params if isinstance(x, tuple) and len(x) == 4]
    names = {x[2]: x[0] for x in params if isinstance(x, tuple) and len(x) == 4}
    chk('W9 그룹 비교 — 경로 기준 고립 · 단절 · 무접촉 열 (활성 바로 뒤) · 셋 다 낮을수록 좋음 (같은 철자)',
        keys[keys.index('ionic_active_pct') + 1:keys.index('ionic_active_pct') + 4]
        == ['am_ionic_isolated_pct', 'ionic_dead_pct', 'ionic_no_se_pct']
        and all(names[k] in A.GROUP_LOWER_BETTER for k in ('am_ionic_isolated_pct', 'ionic_dead_pct', 'ionic_no_se_pct')),
        str(keys[keys.index('ionic_active_pct'):keys.index('ionic_active_pct') + 4]) if 'ionic_active_pct' in keys else '활성 열 없음')
    src = open(os.path.join(HERE, 'app.py'), encoding='utf-8').read()
    chk('W10 그룹 비교의 옛 세대 보정 — am_ionic_isolated_pct 가 없으면 100 − ionic_active_pct 로 채운다 (분해 두 열은 비워 둔다)',
        "metrics.setdefault('am_ionic_isolated_pct'" in src or "metrics['am_ionic_isolated_pct'] = " in src)
    md = next((ln for ln in src.splitlines() if 'Ionically-isolated AM' in ln and '| ' in ln and 'am_ionic_isolated_pct' in ln), '')
    chk('W11 MD 보고서 — 경로 기준 고립 줄 (= 100 − active) · 고립 위험과 구분', bool(md) and '100 − active' in md, md)
    plain = getattr(A, '_GRADE_PLAIN', {}).get('ionic_active_pct', '')
    chk('W12 쉬운 설명 (ionic_active_pct) — 이온이 못 가는 활물질 = 100 − 이 값 · 닿은 개수로 보는 "고립 위험" 과 다르다',
        '100 −' in plain and '고립 위험' in plain, plain)


def section_b():
    print('[B] 표 재구성기 — 같은 줄 · 같은 키')
    import rebuild_tables_from_metrics as RB
    net = [x for x in RB._NET if x[1]]
    labs = [x[0] for x in net]
    i = labs.index('Ionic Active AM(%)') if 'Ionic Active AM(%)' in labs else -1
    got = [(x[0], x[1]) for x in net[i + 1:i + 4]] if i >= 0 else []
    chk('B1 _NET — 활성 뒤에 (부모 · am_ionic_isolated_pct) · (단절 · ionic_dead_pct) · (무접촉 · ionic_no_se_pct)',
        got == [(PARENT, ('am_ionic_isolated_pct',)), (DEAD, ('ionic_dead_pct',)), (NOSE, ('ionic_no_se_pct',))], str(got))


def main():
    for fn in (section_w, section_b):
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
