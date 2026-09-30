#!/usr/bin/env python3
"""full_metrics.json 의 숫자를 숫자로 — 쓰기 (numpy → 파이썬) · 읽기 (옛 숫자 문자열 → 숫자) 를 한 곳에서.

2026-09-30 (웹앱 ② · 원장 LHS-24 (a)) — `analyze_contacts.save_results` 가 `json.dump(..., default=str)` 로 저장해
numpy 정수 (`am_am_n_contacts` — `sum(np.array) // 2`) 가 **문자열** ('412') 로 들어갔다.  숫자만 고르는 그룹 선택기
(`app.group_param_options`) · 그룹 그림 (`generate_comparison_plots._merged_params`) 이 그 열을 조용히 빼 먹었다.
  · 쓰기: `json_default` — numpy 스칼라 · 배열만 파이썬 값으로.  그 밖의 객체는 옛 동작 그대로 `str` (값을 잃지 않는다).
  · 읽기: `metric_number` — 이미 저장된 옛 케이스의 숫자 문자열도 숫자로 읽는다 (파일은 고치지 않는다).

  python3 scripts/metrics_json.py --selftest
"""
import math
import re
import sys

_NUM = re.compile(r'\s*[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?\s*')


def json_default(o):
    """`json.dump(..., default=json_default)` — numpy bool · 정수 · 실수 · 배열을 파이썬 값으로, 나머지는 `str(o)`."""
    try:
        import numpy as np
    except ImportError:                             # numpy 없는 환경 — 옛 동작
        return str(o)
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.floating):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    return str(o)


def metric_number(v):
    """비교 · 그림용 숫자 — int · float (bool 제외) 는 float 그대로 (옛 동작과 같다), 숫자 모양 문자열 ('412' · '1e-3') 은
    그 숫자로.  그 밖 ('7:3' · 'True' · 'nan' · 'mesh' · None) 은 None."""
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str) and _NUM.fullmatch(v):
        x = float(v)
        return x if math.isfinite(x) else None
    return None


def _selftest():
    import json
    fails = []

    def chk(name, ok, extra=''):
        print(('  ✓ ' if ok else '  ✗ ') + name + ('' if ok else f'  — {extra}'))
        if not ok:
            fails.append(name)

    try:
        import numpy as np
        s = json.dumps({'n': np.int64(412), 'b': np.bool_(True), 'f': np.float32(0.5), 'a': np.arange(3),
                        'x': 1.5, 'o': object.__name__}, default=json_default)
        back = json.loads(s)
        chk('① numpy int64 · bool_ · float32 · 배열 → 412 · true · 0.5 · [0, 1, 2] (문자열 아님)',
            back['n'] == 412 and isinstance(back['n'], int) and back['b'] is True and back['f'] == 0.5
            and back['a'] == [0, 1, 2], s)
    except ImportError:
        print('  (numpy 없음 — ① 건너뜀)')
    chk('② 알 수 없는 객체는 옛 동작 그대로 str', json_default({1}) == '{1}', json_default({1}))
    cases = {'412': 412.0, ' 1e-3 ': 1e-3, '-2.5': -2.5, 7: 7.0, 0.25: 0.25, True: None, 'True': None,
             '7:3': None, 'nan': None, 'inf': None, 'mesh': None, None: None, '': None}
    got = {repr(k): metric_number(k) for k in cases}
    chk('③ metric_number — 숫자 모양 문자열만 숫자 · bool · 비율 · nan · 이름은 None',
        all(got[repr(k)] == v for k, v in cases.items()), str(got))
    print(f'\n{3 - len(fails)}/3  ' + ('✓ 전부 통과' if not fails else f'✗ {len(fails)} 건 실패'))
    return 0 if not fails else 1


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(_selftest())
    print(__doc__)
