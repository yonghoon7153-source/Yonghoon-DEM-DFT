#!/usr/bin/env python3
"""full_metrics.json 의 숫자를 숫자로 — 쓰기 (numpy → 파이썬) · 읽기 (옛 숫자 문자열 → 숫자) 를 한 곳에서.

2026-09-30 (웹앱 ② · 원장 LHS-24 (a)) — `analyze_contacts.save_results` 가 `json.dump(..., default=str)` 로 저장해
numpy 정수 (`am_am_n_contacts` — `sum(np.array) // 2`) 가 **문자열** ('412') 로 들어갔다.  숫자만 고르는 그룹 선택기
(`app.group_param_options`) · 그룹 그림 (`generate_comparison_plots._merged_params`) 이 그 열을 조용히 빼 먹었다.
  · 쓰기: `json_default` — numpy 스칼라 · 배열만 파이썬 값으로.  그 밖의 객체는 옛 동작 그대로 `str` (값을 잃지 않는다).
  · 읽기: `metric_number` — 이미 저장된 옛 케이스의 숫자 문자열도 숫자로 읽는다 (파일은 고치지 않는다).

2026-10-05 (원장 LHS-33 · 좁은 개정 · 1저자 비준 · Codex 재검증 Q7) — 옛 σ_VM 열 (`stress_cv` · `stress_ratio_<상>` ·
`stress_z_layer_cv`) 의 **상태 계약** 도 여기 한 곳에 둔다 (생산자 dem_analysis_core · analyze_contacts · 표 재생성 · 등급 · 그룹 그림 ·
웹앱이 같은 상수 · 같은 읽기를 쓴다).  옛 판은 무효 · 미정의 입력을 0 으로 저장했다 (등급 축 '기계적 안정성' 의 거짓 최고 등급).
  · 새 세대 (`stress_cv_contract` = v2-invalid-null): 정상 = 옛 정의 · 수치 · 키 그대로 + `stress_cv_status` = computed ·
    무효/미정의 = 값 None (null) + `stress_cv_status` (unavailable_no_c_strs · invalid_input · undefined_zero_mean) + `stress_cv_reason`.
  · 옛 세대 (상태 키 없음): 저장된 숫자를 그대로 읽는다 — 역사 파일은 바꾸지 않는다 (그 안의 0 이 거짓 0 인지는 구별할 수 없다).

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


# ── LHS-33 옛 σ_VM 열 상태 계약 (좁은 개정 · 1저자 비준 10-05 · Codex 재검증 Q7) ─────────────────────────────────────────
STRESS_CV_CONTRACT = 'v2-invalid-null'
STRESS_CV_COMPUTED = 'computed'
STRESS_CV_STATUSES = (STRESS_CV_COMPUTED, 'unavailable_no_c_strs', 'invalid_input', 'undefined_zero_mean')
#: 표 칸의 짧은 사유 ('— (…)') — 그룹 표 · 내보내기.  긴 사유는 full_metrics 의 stress_cv_reason (생산자가 쓴다).
STRESS_CV_STATUS_KO = {
    'unavailable_no_c_strs': 'c_strs 없음',            # 원자 덤프에 c_strs[1–3] 세 열이 다 없다 (옛 덱 · 손 픽스처)
    'invalid_input': '입력 무효',                       # 열 일부만 · 칸 비유한 · 파싱 실패 · 반경 무효 · 원자 0 · σ_VM 넘침
    'undefined_zero_mean': '평균 0 · 미정의',           # 평균 σ_VM = 0 (무하중 · 전 입자 정수압) → CV · 상 비 = 0/0
}
#: 케이스 표 상태 줄 — analyze_contacts (network_summary.csv) · 표 재생성 · 웹앱 정렬 표 · 툴팁이 같은 철자
STRESS_CV_STATUS_ROW = 'Stress CV 상태 (50/50 · LHS-33)'
#: 옛 네 열 (그룹 표 · 보고서) — 상 비는 LW 열 (`_lw` · `_lw_nowall`) 과 다른 키
STRESS_OLD_KEYS = ('stress_cv', 'stress_ratio_AM_P', 'stress_ratio_AM_S', 'stress_ratio_SE')


def stress_cv_status(metrics):
    """옛 σ_VM 열의 상태 — 'computed' · 무효 상태 이름 · None (옛 세대 = 상태 키 없음)."""
    s = (metrics or {}).get('stress_cv_status')
    return s if isinstance(s, str) and s else None


def stress_metric_value(metrics, key='stress_cv'):
    """옛 σ_VM 열 (stress_cv · stress_ratio_<상>) 값 — 상태가 computed 가 아니면 None (저장된 0 도 읽지 않는다 · 0 으로 채우지 않는다).
    옛 세대 (상태 키 없음) 는 저장된 숫자 그대로 (역사 파일 불변).  숫자가 아니거나 비유한이면 None."""
    st = stress_cv_status(metrics)
    if st is not None and st != STRESS_CV_COMPUTED:
        return None
    return metric_number((metrics or {}).get(key))


def stress_cv_reason(metrics):
    """빈칸의 이유 '상태 — 사유' (computed · 옛 세대면 None)."""
    st = stress_cv_status(metrics)
    if st is None or st == STRESS_CV_COMPUTED:
        return None
    why = (metrics or {}).get('stress_cv_reason')
    return f'{st} — {why}' if why else st


def stress_cv_blank(metrics):
    """표 칸 '— (짧은 사유)' (computed · 옛 세대면 None)."""
    st = stress_cv_status(metrics)
    if st is None or st == STRESS_CV_COMPUTED:
        return None
    return f'— ({STRESS_CV_STATUS_KO.get(st, st)})'


def stress_cv_group_cells(metrics):
    """그룹 비교 표 — 무효 · 미정의면 옛 네 열을 '— (짧은 사유)' 로 (None 이 'None' 으로 보이지 않게 · 0 아님).  있는 상 비 키만 바꾸고
    없는 상의 키는 만들지 않는다.  computed · 옛 세대는 그대로.  metrics 를 고쳐서 돌려준다 (웹앱 `_group_am_am_mean_na` 와 같은 꼴)."""
    b = stress_cv_blank(metrics)
    if b is not None:
        for k in STRESS_OLD_KEYS:
            if k == 'stress_cv' or k in metrics:
                metrics[k] = b
    return metrics


def stress_cv_report_line(metrics):
    """보고서 (Physics Derivations) — 무효 · 미정의면 한 줄 ('—' + 상태 — 사유) · computed · 옛 세대면 None (옛 줄을 그대로 쓴다)."""
    r = stress_cv_reason(metrics)
    if r is None:
        return None
    return (f'- **Stress CV (LIGGGHTS stress/atom 50/50 분할 · 대각)**: — ({r} · 0 으로 채우지 않음 · '
            f'등급 안 매김 · LHS-33 · 계약 {STRESS_CV_CONTRACT})')


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
