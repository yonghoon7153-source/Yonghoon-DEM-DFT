#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Codex 언로딩 개정 1 재검토 (10-12) — 우리 트리 재확인 (Codex 탐침을 import 하지 않는다).

    python3 -I -B <이 파일> <리포 루트> <출력 json>

하는 것 (DEM · 키트 실행 없음 · 표준 라이브러리 + git):
  ① 판정문이 인용한 등록 (REG) 줄이 우리 트리에서 그 내용인가 — 줄마다 낱말 대조
  ② 판정문의 산술을 우리 식으로 다시 (Fraction · statistics) — Codex 증거 JSON 값과 대조
  ③ 묶음 source_manifest 의 97 blob 이 우리 리포 핀의 같은 경로 blob 과 같은가
한정: 규칙의 합성 반례 재확인이다 — 언로딩 결과 · 키트 출력 아님.
"""
from __future__ import annotations

import hashlib
import json
import math
import statistics
import subprocess
import sys
from fractions import Fraction as F
from pathlib import Path

REG = 'docs/reviews/dem_unloading_ps45_prereg_20261009.md'
REQ = 'docs/reviews/codex_dem_unloading_prereg_rereview_request_20261011.md'
EVD = 'docs/reviews/codex_dem_unloading_prereg_rereview_evidence_20261012'
REG_SHA = '73bc55a5045b6c60377095b51558418757b3d41d694a608be5c25e505a69babd'
REQ_SHA = '92f9c5ee919fbec1bee304684b29e0be3f2d6d662795f58deb04f12f0a46363a'
H0 = F('111.052')          # 7:3 h0 (µm) — 판정문 · 등록
T = F('0.10')              # 허용 민감도 문턱 (%p)

#: (줄, 반드시 들어 있어야 할 낱말들, 판정문의 인용 이유)
LINE_CHECKS = [
    (275, ['두 단 더', 'R_M', '분리 상태'], 'ULR1-02 멈춤 = 첫 교차 뒤 두 단 · 분리 · 유지까지'),
    (288, ['창 10,000 step'], 'ULR1-04 옛 UT = 같은 시간 창 10,000'),
    (307, ['UT 를 멈춤 규칙까지 이어 돌린'], 'ULR1-05 ③ 옛 UT 연장 (§12-4 가 대체)'),
    (319, ['0.5 × P_meas × A', '상쇄 우세'], 'ULR1-03 상쇄 문턱'),
    (320, ['띠 > b'], 'ULR1-05 ① 비단조 판정이 b 를 부른다'),
    (332, ['≤ 0.002 µm / 창'], 'ULR1-04 S4 문턱'),
    (334, ['UNSTEADY'], 'ULR1-01 UNSTEADY 정의'),
    (335, ['미식별'], 'ULR1-01 끝점 비정상 = 미식별'),
    (336, ['TIMEOUT'], 'ULR1-02 TIMEOUT'),
    (337, ['마지막 정상 단 값', '하한'], 'ULR1-02 TIMEOUT = 하한 (조건 없음)'),
    (389, ['| UNSTEADY |', '미식별'], 'ULR1-01 상태표'),
    (390, ['| NOISE_FLOOR |', '3 σ_P'], 'ULR1-01 · Q2 σ_P'),
    (391, ['| TIMEOUT |', '하한'], 'ULR1-02 상태표 (대체 표지 없음)'),
    (392, ['| TECH |'], 'ULR1-01 TECH = 별도 범주'),
    (394, ['상쇄 우세'], 'ULR1-03 표지 (값과 함께)'),
    (413, ['b 밖'], 'ULR1-05 ① 보고 예문의 b'),
    (435, ['b = …'], 'ULR1-05 ① 보고 예문의 b'),
    (473, ['for A in UB UV UT UC'], 'ULR1-05 ② UV 동시 제출 예문'),
    (619, ['보간하지 않는다'], 'ULR1-01 결손 끝점 = 보간 안 함'),
    (625, ['물리 시간', '단일 튜플'], 'ULR1-04 물리 시간 = 튜플'),
    (627, ['1 MPa 끝점까지', '아니면 dt* = dt₀/2'], 'ULR1-01 · 05 ③ dt 먼저'),
    (629, ['팔 셋으로 끝난다'], 'ULR1-01 "팔 셋으로 끝난다" (유한 넷에서만 참)'),
    (633, ['≤ 0.10 | ≤ 0.10'], 'ULR1-01 결정표 1행'),
    (634, ['≤ 0.10 | > 0.10'], 'ULR1-01 결정표 2행'),
    (635, ['> 0.10 | ≤ 0.10', 'UT 팔'], 'ULR1-01 결정표 3행 · ULR1-05 ③'),
    (636, ['> 0.10 | > 0.10'], 'ULR1-01 결정표 4행'),
    (650, ['TENSION', 'SEPARATED', '두 창 연속'], 'ULR1-03 상태 전이'),
    (651, ['TENSION 으로 기록', 'h_surf 시작 = SEPARATED 첫 창'], 'ULR1-03 기록 · 첫 창'),
    (655, ['R_M = 첫 1 MPa 교차 뒤 두 단'], 'ULR1-02 분기 위치'),
    (660, ['창 W = 5,000 step'], 'ULR1-04 W 적용 범위 한정 없음'),
    (661, ['매 단 끝 contact'], 'ULR1-03 단 끝 벽 자료 하나'),
    (662, ['4–12 창'], 'ULR1-04 유지 예산'),
    (667, ['p99.9 방법', '빈 칸'], 'Q2 표면 관측자 = 열거만'),
    (678, ['3,660,000', '3,650,000', '3,662,000'], 'Q6 10:0 일정'),
]


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def rho(lift) -> F:
    """판 상승 (µm) → 회복 %  (h0 = 7:3)."""
    return F(100) * F(lift) / H0


def cross(l0, l1, p0, p1, pm=F(1)) -> F:
    """두 단 사이 1 MPa 선형 보간 상승."""
    l0, l1, p0, p1 = map(F, (l0, l1, p0, p1))
    return l0 + (pm - p0) * (l1 - l0) / (p1 - p0)


def select(d_dt, d_v):
    """REG:627–636 을 글자대로 — 값이 없으면 행이 없다."""
    if d_dt is None or d_v is None:
        return None
    if isinstance(d_dt, float) and math.isnan(d_dt) or isinstance(d_v, float) and math.isnan(d_v):
        return None
    if d_dt <= T:
        return 'UB' if d_v <= T else 'UV_dt0'
    return 'UT' if d_v <= T else 'UV_dt0_half'


def close(a: float, b: float, rel=1e-12) -> bool:
    return abs(a - b) <= rel * max(1.0, abs(a), abs(b))


def main(repo: Path, out: Path) -> int:
    res: dict = {'kind': 'our-tree recheck of codex 10-12 unloading re-review (no DEM · no kit · no codex import)'}
    reg_b = (repo / REG).read_bytes()
    req_b = (repo / REQ).read_bytes()
    lines = reg_b.decode('utf-8').split('\n')
    res['reg'] = {'sha256': sha256(reg_b), 'sha_matches_verdict': sha256(reg_b) == REG_SHA,
                  'lines': len(lines) - (1 if lines and lines[-1] == '' else 0)}
    res['request'] = {'sha256': sha256(req_b), 'sha_matches_verdict': sha256(req_b) == REQ_SHA}

    # ① 인용 줄 대조
    lc = []
    for n, toks, why in LINE_CHECKS:
        text = lines[n - 1]
        miss = [t for t in toks if t not in text]
        lc.append({'line': n, 'ok': not miss, 'missing': miss, 'why': why})
    # 결정표 앞뒤 (625–645) 에 결손 · 무효 끝점 처리 행이 없는지
    sel_block = '\n'.join(lines[624:645])
    res['line_checks'] = {'n': len(lc), 'ok': sum(x['ok'] for x in lc), 'rows': lc,
                          'decision_block_mentions_missing_or_invalid':
                              any(w in sel_block for w in ('결손', '무효', 'UNSTEADY', 'NOISE_FLOOR', 'SELECTION'))}

    # ② 산술 (우리 식)
    ev_state = json.loads((repo / EVD / 'evidence/state.json').read_text(encoding='utf-8-sig'))
    ev_obs = json.loads((repo / EVD / 'evidence/observers.json').read_text(encoding='utf-8-sig'))
    a = {}
    # ULR1-01 결정표
    rows = [(F('0.04'), F('0.04')), (F('0.04'), F('0.20')), (F('0.20'), F('0.04')), (F('0.20'), F('0.20')),
            (T, T), (None, F('0.04')), (F('0.04'), None), (float('nan'), F('0.04'))]
    show = lambda x: None if x is None else str(float(x))  # noqa: E731 — 표시용 (Fraction → 십진)
    a['ULR1_01_selector'] = [{'d_dt': show(x), 'd_v': show(y), 'row': select(x, y)} for x, y in rows]
    a['ULR1_01_codex_same'] = (
        [r['selected'] for r in ev_state['four_finite_rows']] == [select(x, y) for x, y in rows[:4]]
        and ev_state['equality_boundary']['selected'] == select(T, T)
        and all(u['selected'] == 'NO_REGISTERED_ROW' for u in ev_state['undefined_inputs'])
        and all(select(x, y) is None for x, y in rows[5:]))
    # ULR1-02 측정 뒤 TIMEOUT
    cl = cross('0.20', '0.25', '1.2', '0.8')
    rm, rl = rho(cl), rho('0.35')
    pmt = ev_state['post_measurement_timeout']
    a['ULR1_02'] = {'interp_lift_um': float(cl), 'rho_M_pct': float(rm), 'rho_last_pct': float(rl),
                    'false_lower_bound': rm < rl,
                    'codex_same': close(float(cl), pmt['interpolated_lift_um'])
                    and close(float(rm), pmt['valid_rho_percent'])
                    and close(float(rl), pmt['old_unconditional_timeout_claim_rho_greater_than_percent'])}
    # ULR1-03 양압 상쇄
    net = F('1.6') - F('0.6')
    a['ULR1_03'] = {'net_MPa': float(net), 'contact_by_650': net > 0,
                    'tension_by_319_651': F('0.6') >= F('0.5') * F(1)}
    # ULR1-04 창
    dt0, dth, w0 = F(1, 10**6), F(1, 2 * 10**6), 5000
    tw = dt0 * w0
    w_half = tw / dth
    s4 = F('0.002')
    v = F('0.6')
    a['ULR1_04'] = {'T_W_s': float(tw), 'W_half_dt_steps': int(w_half),
                    'hold_4_12_s_ub': [float(4 * tw), float(12 * tw)],
                    'literal_5000_at_half_dt_window_s': float(w0 * dth),
                    'surface_um_per_window_ub': float(v * tw), 'S4_fail_ub': v * tw > s4,
                    'surface_um_per_window_literal': float(v * w0 * dth), 'S4_fail_literal': v * w0 * dth > s4,
                    'codex_same': close(float(tw), ev_obs['windows']['baseline_T_W_s'])
                    and int(w_half) == ev_obs['windows']['half_dt_same_time_W_steps']
                    and close(float(v * tw), ev_obs['windows']['surface_change_base_um'])
                    and close(float(v * w0 * dth), ev_obs['windows']['surface_change_half_dt_fixed_5000_um'])}
    # ULR1-05 ① 비단조 b
    f1 = cross('1.00', '1.05', '1.2', '0.8')
    f2 = cross('1.10', '1.15', '1.3', '0.7')
    nb = ev_state['live_nonmonotone_b_reference']
    a['ULR1_05_nonmonotone'] = {'first_lift_um': float(f1), 'last_lift_um': float(f2),
                                'span_pp': float(rho(f2 - f1)),
                                'codex_same': close(float(rho(f2 - f1)), nb['span_pp'])
                                and close(float(rho(f1)), nb['first_crossing_rho_percent'])
                                and close(float(rho(f2)), nb['last_crossing_rho_percent'])}
    # Q2 S3 norm 순서
    fs, den = (1e-5, -1e-5), 1e-2
    a['Q2_S3'] = {'sum_norms': sum(abs(x) for x in fs) / den, 'norm_sum': abs(sum(fs)) / den,
                  'codex_same': close(sum(abs(x) for x in fs) / den, ev_obs['S3_norm_order']['sum_particle_norms_residual'])}
    # Q2 σ_P ddof
    smp = [0.67, 1.33] * 10
    sp, ss = statistics.pstdev(smp), statistics.stdev(smp)
    a['Q2_sigma_P'] = {'ddof0': sp, 'ddof1': ss, '3ddof0': 3 * sp, '3ddof1': 3 * ss,
                       'noise_floor_ddof0': 1 < 3 * sp, 'noise_floor_ddof1': 1 < 3 * ss,
                       'codex_same': close(sp, ev_obs['sigma_sample_rule']['population_sigma_MPa'])
                       and close(ss, ev_obs['sigma_sample_rule']['sample_sigma_MPa'])}
    # Q2 표면 관측자 — 빈 칸 · 분위수
    vals = sorted([100.0] * 99 + [200.0])
    idx = (len(vals) - 1) * 0.999
    lin = vals[math.floor(idx)] + (idx - math.floor(idx)) * (vals[math.ceil(idx)] - vals[math.floor(idx)])
    near = vals[math.ceil(0.999 * len(vals)) - 1]
    a['Q2_surface'] = {'omit_empty_mean': 99 * 100 / 99, 'zero_empty_mean': 99 * 100 / 100,
                       'p999_linear': lin, 'p999_nearest_rank': near,
                       'codex_same': close(lin, ev_obs['surface_quantile']['linear_um'])
                       and near == ev_obs['surface_quantile']['nearest_rank_um']}
    # Q3 세 팔 · 괄호
    wa = rho('0.20')
    a['Q3'] = {'A_width_pp': float(wa), 'max_bracket_abs_diff_pp': float(F('0.04') + wa),
               'select_1.00_1.04_1.20': select(abs(F('1.04') - F('1.00')), abs(F('1.20') - F('1.00'))),
               'unmeasured_corner_diff_pp': float(F('1.80') - F('1.20')),
               'codex_same': close(float(wa), ev_state['point_threshold_vs_bracket']['A_width_pp'])
               and close(float(F('0.04') + wa),
                         ev_state['point_threshold_vs_bracket']['possible_abs_difference_range_from_brackets_pp'][1])}
    # Q6 10:0 일정
    a['Q6'] = {'main_end': 3_600_000 + 60_000, 'S0p_mod_10000': 3_650_000 % 10_000,
               'main_end_mod_50000': 3_660_000 % 50_000, 'opt_end': 3_660_000 + 50_000,
               'S0pp_window_inside': 3_700_000 + 5_000 < 3_660_000 + 50_000,
               'R_continue_would_be': 3_602_000 + 60_000}
    res['arithmetic'] = a

    # ③ source blob 대조
    man = json.loads((repo / EVD / 'source_manifest.json').read_text(encoding='utf-8-sig'))
    same, diff = 0, []
    for e in man['files']:
        r = subprocess.run(['git', '-C', str(repo), 'rev-parse', f"{man['pin']}:{e['path']}"],
                           capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.strip() == e['blob_sha']:
            same += 1
        else:
            diff.append(e['path'])
    res['source_blobs'] = {'pin': man['pin'], 'files': len(man['files']), 'same': same, 'diff': diff}

    flags = [res['reg']['sha_matches_verdict'], res['request']['sha_matches_verdict'],
             res['line_checks']['ok'] == res['line_checks']['n'],
             not res['line_checks']['decision_block_mentions_missing_or_invalid'],
             same == len(man['files'])] + [v['codex_same'] for v in a.values() if isinstance(v, dict) and 'codex_same' in v] \
        + [a['ULR1_01_codex_same']]
    res['all_ok'] = all(flags)
    out.write_text(json.dumps(res, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'all_ok': res['all_ok'], 'line_checks': f"{res['line_checks']['ok']}/{res['line_checks']['n']}",
                      'source_blobs': f'{same}/{len(man["files"])}'}, ensure_ascii=False))
    return 0 if res['all_ok'] else 1


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1]).resolve(), Path(sys.argv[2])))
