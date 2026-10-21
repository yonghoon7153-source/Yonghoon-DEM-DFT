#!/usr/bin/env python3
"""Check every number cited in the Codex verdict (and the brief) against OUR outputs (and Codex's JSONs).

'같음' = ours agrees with the printed value at its printed precision (|ours-printed| <= 0.5 unit of the last
printed digit, plus 1e-12 relative slack); booleans / labels / counts exact.
Usage: verdict_numbers.py <work W> <codex bundle X> <out.json> <out.md>
"""
import json, math, os, re, sys
from decimal import Decimal
import numpy as np

W, X, OUT_J, OUT_M = sys.argv[1:5]
R = os.path.join(W, '_repro_ours_20261021')
EV = os.path.join(W, 'part_b', 'evidence')
XE = os.path.join(X, 'part_b', 'evidence')


def L(p):
    return json.loads(open(p, 'rb').read().decode('utf-8-sig'))


ours = {'geo': L(f'{R}/geometry_probe_results.json'), 'reg': L(f'{R}/registration_probe_results.json'),
        'conv': L(f'{R}/convergence_probe_results.json'), 'search': L(f'{R}/search_cg_connected_results.json'),
        'ind': L(f'{EV}/independent_join_checks.json'), 'klm': L(f'{EV}/known_limit_and_mutant.json'),
        'struct': L(f'{EV}/structure_results.json'), 'num': L(f'{EV}/numeric_current.json'),
        'ovf': L(f'{EV}/numeric_overflow_replay_current.json')}
codex = {'geo': L(f'{X}/geometry/geometry_probe_results.json'), 'reg': L(f'{X}/registration/registration_probe_results.json'),
         'conv': L(f'{X}/geometry/convergence_probe_results.json'), 'search': L(f'{X}/geometry/search_cg_connected_results.json'),
         'ind': L(f'{XE}/independent_join_checks.json'), 'klm': L(f'{XE}/known_limit_and_mutant.json'),
         'struct': L(f'{XE}/structure_results.json'), 'num': L(f'{XE}/numeric_current.json'),
         'ovf': L(f'{XE}/numeric_overflow_replay_current.json')}


def logcount(name, pat=r'(\d+) PASS · (\d+) FAIL'):
    p = os.path.join(EV, name)
    t = open(p, 'rb').read().decode('utf-8', 'replace')
    m = re.findall(pat, t)
    return '%s/%d' % (m[-1][0], int(m[-1][0]) + int(m[-1][1])) if m else None


def harness_rc(name):
    return L(os.path.join(EV, name))['rc']


rows = []


def _numstr(x):
    if isinstance(x, bool):
        return None
    if isinstance(x, (int, float)):
        return repr(x)
    if isinstance(x, str):
        s = x.replace(',', '').replace('−', '-').strip()
        try:
            Decimal(s)
            return s
        except Exception:  # noqa
            return None
    return None


def agree(printed, value):
    ps = _numstr(printed)
    if ps is None or value is None or isinstance(value, (bool, str, list)):
        return printed == value
    d = Decimal(ps)
    exp = d.as_tuple().exponent
    half = Decimal(5) * Decimal(10) ** (exp - 1)
    return abs(Decimal(repr(float(value))) - d) <= half + abs(d) * Decimal('1e-12')


def add(item, printed, f, note=''):
    vals = {}
    for nm, src in (('ours', ours), ('codex', codex)):
        try:
            vals[nm] = f(src)
        except Exception as e:  # noqa
            vals[nm] = f'ERR {type(e).__name__}: {e}'
    ok_o = agree(printed, vals['ours']) if not str(vals['ours']).startswith('ERR') else False
    ok_c = agree(printed, vals['codex']) if not str(vals['codex']).startswith('ERR') else False
    rows.append({'item': item, 'printed': printed, 'ours': vals['ours'], 'codex_json': vals['codex'],
                 'ours_matches_printed': bool(ok_o), 'codex_json_matches_printed': bool(ok_c), 'note': note})


reg = lambda s: s['reg']
cal = lambda s: s['reg']['calibration']
org = lambda s: s['reg']['origin']
cb = lambda s: s['reg']['contact_bias']
lg = lambda s: s['reg']['logic']
lr = lambda s: s['reg']['loading_rate']
# ---------------- RCA-01
add('RCA-01 마지막 이웃 R_lo [Ω]', '31622.7766', lambda s: cal(s)['last_bracket_Rj_ohm'][0])
add('RCA-01 마지막 이웃 R_hi [Ω]', '100000', lambda s: cal(s)['last_bracket_Rj_ohm'][1])
add('RCA-01 S(R_lo) [mS/cm]', '1.6518055793', lambda s: cal(s)['last_bracket_SBE_mScm'][0])
add('RCA-01 S(R_hi) [mS/cm]', '1.6163261981', lambda s: cal(s)['last_bracket_SBE_mScm'][1])
add('RCA-01 e', '0.01885983293', lambda s: cal(s)['e'])
add('RCA-01 e_min', '0.01737177928', lambda s: cal(s)['emin'])
add('RCA-01 세 자리 보정값 [Ω]', '64000', lambda s: cal(s)['rounded_Rj0_ohm'])
add('RCA-01 확인 S [mS/cm]', '1.6263191459', lambda s: cal(s)['confirmed_SBE_mScm'])
add('RCA-01 확인 S 목표 대비 [%]', '-0.2258193', lambda s: 100 * (cal(s)['confirmed_SBE_mScm'] / 1.63 - 1))
add('RCA-01 바닥 1.597 목표 대비 [%]', '2.0245399', lambda s: cal(s)['extrema_distance_pct_denominator_target'][0])
add('RCA-01 점 수 (≤12)', 8, lambda s: cal(s)['points_including_extrema_and_confirmation'])
add('RCA-01 등록 보간 R_lo [Ω]', '22387.5598', lambda s: cal(s)['draft_r_bounds'][0] * cal(s)['Rj_scale_ohm'])
add('RCA-01 등록 보간 R_hi [Ω]', '186736.3736', lambda s: cal(s)['draft_r_bounds'][1] * cal(s)['Rj_scale_ohm'])
add('RCA-01 실제 역상 R_lo [Ω]', '25493.9497', lambda s: cal(s)['true_r_bounds'][0] * cal(s)['Rj_scale_ohm'])
add('RCA-01 실제 역상 R_hi [Ω]', '5097624.1129', lambda s: cal(s)['true_r_bounds'][1] * cal(s)['Rj_scale_ohm'])
add('RCA-01 등록 양끝 S lo', '1.6698749769', lambda s: cal(s)['SBE_at_draft_bounds'][0])
add('RCA-01 등록 양끝 S hi', '1.6076118802', lambda s: cal(s)['SBE_at_draft_bounds'][1])
add('RCA-01 R_hi/R_lo 등록 (약)', '8.34', lambda s: cal(s)['draft_r_bounds'][1] / cal(s)['draft_r_bounds'][0])
add('RCA-01 R_hi/R_lo 실제', '199.9542703', lambda s: cal(s)['true_r_bound_ratio'])
add('RCA-01 등록 DBE lo', '3.2923382972', lambda s: cal(s)['draft_DBE_verdict']['lo'])
add('RCA-01 등록 DBE hi', '5.0075751200', lambda s: cal(s)['draft_DBE_verdict']['hi'])
add('RCA-01 실제 DBE lo', '3.0110192837', lambda s: cal(s)['exact_DBE_verdict']['lo'])
add('RCA-01 실제 DBE hi', '4.8071625344', lambda s: cal(s)['exact_DBE_verdict']['hi'])
add('RCA-01 W 등록', '0.419353749', lambda s: cal(s)['draft_DBE_verdict']['W'])
add('RCA-01 등급 등록', 'PASS_INFORMATIVE', lambda s: cal(s)['draft_DBE_verdict']['label'])
add('RCA-01 W 실제', '0.467828346', lambda s: cal(s)['exact_DBE_verdict']['W'])
add('RCA-01 등급 실제', 'CONSISTENT_WEAK', lambda s: cal(s)['exact_DBE_verdict']['label'])
# ---------------- RCA-02
add('RCA-02 중앙 r=1 전 origin [mS/cm]', '3.9290909091', lambda s: org(s)['centre_all_origins'][0])
add('RCA-02 중앙 origin log 산포', 0, lambda s: org(s)['centre_origin_log_range'] if org(s)['centre_origin_log_range'] < 1e-15 else 'nonzero')
add('RCA-02 arm0 lo', '3.4961904762', lambda s: org(s)['draft_verdict']['lo'])
add('RCA-02 arm0 hi', '4.6866666667', lambda s: org(s)['draft_verdict']['hi'])
add('RCA-02 W arm0', '0.2930476574', lambda s: org(s)['draft_verdict']['W'])
add('RCA-02 등급 arm0', 'PASS_INFORMATIVE', lambda s: org(s)['draft_verdict']['label'])
add('RCA-02 8팔 lo', '2.6628571429', lambda s: org(s)['true_eight_origin_verdict']['lo'])
add('RCA-02 8팔 hi', '6.1450000000', lambda s: org(s)['true_eight_origin_verdict']['hi'])
add('RCA-02 W 8팔', '0.8362390828', lambda s: org(s)['true_eight_origin_verdict']['W'])
add('RCA-02 등급 8팔', 'CONSISTENT_WEAK', lambda s: org(s)['true_eight_origin_verdict']['label'])
# ---------------- RCA-03
sf = lambda s: s['geo']['same_fid_same_cell']
add('RCA-03 (0,0,0) 지나는 선분 (첫·마지막)', [0, 4], lambda s: sf(s)['segments_visiting_target'])
add('RCA-03 가닥 중심선 거리 [µm]', '0.1838477631', lambda s: sf(s)['strand_separation_um'])


def series_merge():   # independent: 5 x 1 Ω series, nodes 0..5, merge nonconsecutive 1 and 4
    def solve(n, edges, a, b):
        Lm = np.zeros((n, n))
        for i, j, g in edges:
            Lm[i, i] += g; Lm[j, j] += g; Lm[i, j] -= g; Lm[j, i] -= g
        u = np.zeros(n); u[a] = 1.
        fr = [k for k in range(n) if k not in (a, b)]
        u[fr] = np.linalg.solve(Lm[np.ix_(fr, fr)], -Lm[fr, a])
        return 1. / float((Lm @ u)[a])
    full = solve(6, [(k, k + 1, 1.) for k in range(5)], 0, 5)
    mp = {0: 0, 1: 1, 2: 2, 3: 3, 4: 1, 5: 4}
    merged = solve(5, [(mp[k], mp[k + 1], 1.) for k in range(5)], 0, 4)
    return full, merged


_f, _m = series_merge()
rows.append({'item': 'RCA-03 R 직렬 5 → (cell,fid) 합침 2 [Ω] (우리 독립 계산)', 'printed': '5 → 2 · G 2.5배',
             'ours': f'{_f:.12g} → {_m:.12g} · G {_f / _m:.12g}배', 'codex_json': f"{codex['geo']['same_fid_same_cell']['finite_path_R_ohm']} → {codex['geo']['same_fid_same_cell']['collapsed_cell_fid_R_ohm']} (탐침 안 상수)",
             'ours_matches_printed': abs(_f - 5) < 1e-12 and abs(_m - 2) < 1e-12, 'codex_json_matches_printed': True,
             'note': '탐침 JSON 의 5/2/2.5 는 계산값이 아니라 상수 — 우리 쪽에서 직렬 망 해로 따로 확인'})
# ---------------- RCA-04
add('RCA-04 A0 선택 G [S]', '1', lambda s: s['geo']['port_tie']['port_near_terminal']['G_S'])
add('RCA-04 A1 선택 G [S]', '0.5', lambda s: s['geo']['port_tie']['port_after_reversal']['G_S'])
# ---------------- RCA-05
lc = lambda s, i: s['geo']['long_contact_lumping'][i]
add('RCA-05 분산 G [S]', '1.366013071895', lambda s: lc(s, 0)['G_distributed'])
add('RCA-05 왼쪽 집중 G [S]', '5.000000000000', lambda s: lc(s, 0)['G_lumped'])
add('RCA-05 중앙 집중 G [S]', '0.238095238095', lambda s: lc(s, 1)['G_lumped'])
add('RCA-05 왼쪽 집중 오차 [%]', '266.028708', lambda s: 100 * lc(s, 0)['relative_error'])
add('RCA-05 중앙 집중 오차 [%]', '-82.570062', lambda s: 100 * lc(s, 1)['relative_error'])
add("RCA-05 r' [Ω/µm]", '56.58842421', lambda s: s['geo']['transfer_length']['axial_ohm_per_um'])
for rj, v in (('10000.0', '5.1485'), ('1000000.0', '51.4851'), ('100000000.0', '514.8513')):
    add(f'RCA-05 λ (R_j={float(rj):.0e}) [µm]', v, lambda s, rj=rj: s['geo']['transfer_length']['lambda_um'][rj])
# ---------------- RCA-06
sv = lambda s: s['geo']['sv_dissipation_guard']
add('RCA-06 전체 G [S]', '0.00105238095238', lambda s: sv(s)['G_S'])
add('RCA-06 SV 경로 전류 몫 [%]', '90.49773756', lambda s: 100 * sv(s)['SV_terminal_current_fraction'])
add('RCA-06 SV 끊으면 G 감소 배수', '10.52380952', lambda s: sv(s)['G_ratio_to_SV_path_cut'])
add('RCA-06 P_SV [W]', '4.5351473923e-5', lambda s: sv(s)['P_W']['SV_SDCP'])
add('RCA-06 P_VV [W]', '1.0e-4', lambda s: sv(s)['P_W']['VV'])
add('RCA-06 가드 (P_SV ≥ P_VV)', False, lambda s: sv(s)['SV_DOMINANT_guard'])
# ---------------- RCA-07
c7 = lambda s: s['conv']['actual_production_cg_zero_resolve_iterations']
add('RCA-07 g 최대 (코드 단위)', '1270.447780941764', lambda s: max(max(c7(s)['conductance_chain']), c7(s)['dead_end_conductance']))
add('RCA-07 g 최소', '1.92731315261e-9', lambda s: min(c7(s)['conductance_chain']))
add('RCA-07 대비 g_max/g_min', '6.59e11', lambda s: max(max(c7(s)['conductance_chain']), c7(s)['dead_end_conductance']) / min(c7(s)['conductance_chain']))
add('RCA-07 정확 G', '1.6475350536519418e-9', lambda s: c7(s)['true_G'])
add('RCA-07 첫 CG 판 전류 G', '1.6472243400696000e-9', lambda s: c7(s)['reported_G'])
add('RCA-07 상대 오차', '-1.88593002409e-4', lambda s: c7(s)['relative_error'])
add('RCA-07 info', 0, lambda s: c7(s)['certificate']['info'])
add('RCA-07 첫 CG 반복', 10, lambda s: c7(s)['iterations_initial_then_resolve'][0])
add('RCA-07 전역 상대 잔차', '2.76138147391e-16', lambda s: c7(s)['certificate']['resid'])
add('RCA-07 판 전류 불균형 (< 1e-4)', '9.14779553358e-5', lambda s: c7(s)['certificate']['imbalance'])
add('RCA-07 이어 풀기 추가 반복', 0, lambda s: c7(s)['iterations_initial_then_resolve'][1])
add('RCA-07 이어 풀기 ΔG/G', 0, lambda s: c7(s)['certificate']['dsigma_rel'])
add('RCA-07 certify pass_a', True, lambda s: c7(s)['certificate']['pass_a'])
add('RCA-07 certify pass_b', True, lambda s: c7(s)['certificate']['pass_b'])
add('RCA-07 certify pass_c', True, lambda s: c7(s)['certificate']['pass_c'])
add('RCA-07 certify ok', True, lambda s: c7(s)['certificate']['ok'])
add('RCA-07 에너지 상한 U', '1.647535053652368e-9', lambda s: c7(s)['energy_upper_G'])
add('RCA-07 흐름 하한', '1.6475350536519418e-9', lambda s: c7(s)['feasible_flow_lower_G'])
add('RCA-07 상·하한 상대 폭', '2.58682e-13', lambda s: c7(s)['energy_rel_gap'])
cc = lambda s: s['conv']['actual_production_cg_connected']
add('RCA-07 보조(연결) 정확 G', '2.10862372514e-12', lambda s: cc(s)['true_G'])
add('RCA-07 보조(연결) 판독 G', '2.08956791085e-12', lambda s: cc(s)['reported_G'])
add('RCA-07 보조(연결) 오차 [%]', '-0.9037086166', lambda s: 100 * cc(s)['relative_error'])
add('RCA-07 보조(연결) 잔차', '5.28596e-17', lambda s: cc(s)['certificate']['resid'])
add('RCA-07 보조(연결) 판 불균형', '1.15636e-5', lambda s: cc(s)['certificate']['imbalance'])
add('RCA-07 보조(연결) 재풀이 반복', 0, lambda s: cc(s)['iterations_initial_then_resolve'][1])
add('RCA-07 보조(연결) certify ok', True, lambda s: cc(s)['certificate']['ok'])
add('RCA-07 보조(연결) 대비', '5.08e14', lambda s: max(max(cc(s)['conductance_chain']), cc(s)['dead_end_conductance'], cc(s)['stub_to_first_chain_conductance']) / min(min(cc(s)['conductance_chain']), cc(s)['stub_to_first_chain_conductance']))
add('RCA-07 정상 영값 pass_a/b/c', [True, False, False], lambda s: [s['conv']['valid_zero']['exact_zero_certificate'][k] for k in ('pass_a', 'pass_b', 'pass_c')])
add('RCA-07 검색 seed611 찾은 표본', 57686, lambda s: s['search']['found'][0]['sample'])
add('RCA-07 검색 찾은 표본 certify ok', True, lambda s: s['search']['found'][0]['certificate']['ok'])
# ---------------- RCA-08..13
add('RCA-08 envelope W', '0.3513978868', lambda s: lg(s)['scenario_hull_verdict']['W'])
add('RCA-08 envelope 등급', 'PASS_INFORMATIVE', lambda s: lg(s)['scenario_hull_verdict']['label'])
add('RCA-08 어느 P 구간도 목표 포함', False, lambda s: lg(s)['any_admissible_P_interval_contains_target'])
add('RCA-09 주 판정 W', '.1100008952', lambda s: lg(s)['same_model_primary_with_calibration_bounds']['W'])
add('RCA-09 주 판정 등급', 'PASS_INFORMATIVE', lambda s: lg(s)['same_model_primary_with_calibration_bounds']['label'])
add('RCA-09 중앙 네 점 W', '.0335226920', lambda s: lg(s)['same_model_noop_sensitivity_centres_only']['W'])
add('RCA-09 중앙 네 점 등급', 'FAIL', lambda s: lg(s)['same_model_noop_sensitivity_centres_only']['label'])
add('RCA-10 DIA_UNCHECKED 아래 PASS 문장 허용', False, lambda s: lg(s)['PASS_sentence_allowed_by_literal_7_1'])
s0 = lambda s: s['geo']['s0_resampling']
add('RCA-11 tol (간격 .10 / .02) [µm]', [0.05, 0.01], lambda s: [s0(s)[0]['tol_ff_um'], s0(s)[1]['tol_ff_um']])
add('RCA-11 등록 접합 있음 → 없음', [True, False], lambda s: [s0(s)[0]['register_contact'], s0(s)[1]['register_contact']])
add('RCA-12 Rc=1 Ω 문턱', '3.9967891509', lambda s: cb(s)['threshold'])
add('RCA-12 ±2% 할선 s', '2.9702538506', lambda s: cb(s)['local_pm2pct_secant_s'])
add('RCA-12 문서식 예측/측정', '1.1709917265', lambda s: cb(s)['registered_formula_prediction_over_measurement'])
add('RCA-12 정확 유한 이동', '0.4932649517', lambda s: cb(s)['exact_prediction_over_measurement'])
add('RCA-12 유한 구간 평균 s', '8.5926514778', lambda s: cb(s)['finite_range_s'])
add('RCA-12 SBE 실제 이동 [%] (약)', '16.62', lambda s: 100 * (cb(s)['SBE_true_mScm'] / 1.63 - 1))
rows.append({'item': 'RCA-13 τ_mono 단위 의존 (산술 · 탐침 없음)', 'printed': '0.5 거부 / 0.0005 허용',
             'ours': f'|1000−999.5| = {abs(1000-999.5):g} > 1e-3 ; |1−0.9995| = {abs(1-0.9995):.4g} < 1e-3',
             'codex_json': '— (탐침 없음)', 'ours_matches_printed': abs(1000 - 999.5) > 1e-3 and abs(1 - 0.9995) < 1e-3,
             'codex_json_matches_printed': None, 'note': '판정문 산술만 · 실행 탐침 없음'})
# ---------------- §4-1 , §5-2
ff = lambda s: s['geo']['face_false_zero']
add('§4-1 정확 α', '0.0134549613712', lambda s: ff(s)['exact_alpha'])
add('§4-1 K4', 0, lambda s: ff(s)['midpoint_alpha']['4'])
add('§4-1 K8', 0, lambda s: ff(s)['midpoint_alpha']['8'])
add('§4-1 K16', '.015625', lambda s: ff(s)['midpoint_alpha']['16'])
add('§4-1 K32', '.01171875', lambda s: ff(s)['midpoint_alpha']['32'])
add('§5-2 SE M [GPa]', '26.18456376', lambda s: lr(s)['SE_M_GPa'])
add('§5-2 VGCF100 M [GPa]', '134.61538462', lambda s: lr(s)['VGCF100_M_GPa'])
add('§5-2 CFL 구', '2.9722242377e-4', lambda s: lr(s)['old_cfl_cap'])
add('§5-2 CFL 신 = dt 신', '1.3108617603e-4', lambda s: lr(s)['new_cfl_cap'])
add('§5-2 dt 신 (코드 단위)', '.000131086176026', lambda s: lr(s)['new_dt'])
add('§5-2 실제 핀 스칼라 블록 dt (E=100)', '1.3108617603e-4', lambda s: lr(s)['actual_pinned_scalar_blocks'][1]['dt'])
add('§5-2 속도 비', '1.5257138934', lambda s: lr(s)['speed_factor'])
add('§5-2 P-Mach 신', '.4145364648', lambda s: lr(s)['P_Mach_old_new'][1])
add('§5-2 S-Mach 구', '1.9403261040', lambda s: lr(s)['S_Mach_old_new'][0])
add('§5-2 S-Mach 신', '2.9603824947', lambda s: lr(s)['S_Mach_old_new'][1])
add('§5-2 150 프레임 예산 신', '.7865170562', lambda s: lr(s)['150_frame_budget_time_old_new'][1])
add('§5-2 40 프레임 hold 신', '.2097378816', lambda s: lr(s)['40_frame_hold_time_old_new'][1])
# ---------------- Part B
st = lambda s: s['struct']
add('Part B 구조 탐침 건수', 144, lambda s: st(s)['summary']['n_cases'])
add('Part B 구조 기대 밖 통과/거부', [[], []], lambda s: [st(s)['summary']['unexpected_pass'], st(s)['summary']['unexpected_reject']])


HDR = ('_rows_no_boundary', '_box_no_boundary', '_rows_repeated_marker', '_box_repeated_marker', '_rows_marker_at_end')


def hdr10(s):
    rs = [r for r in st(s)['results'] if str(r.get('case', '')).endswith(HDR)]
    return [len(rs), sum(r['status'] == 'REJECT' for r in rs), sum(r.get('prior', {}).get('status') == 'PASS' for r in rs)]


add('Part B 헤더 공격 건수 · 현행 REJECT · 이전(dcb97f1ed) PASS', [10, 10, 10], hdr10,
    note='structure_probe 의 새 헤더 공격 10 건 (atom/contact × 5) · 2b9efa253 판 확인은 별도 탐침')


def prior_false_pass_all(s):
    return sum(1 for r in st(s)['results'] if r.get('prior', {}).get('status') == 'PASS'
               and r.get('expected') == 'reject' and r.get('status') != 'PASS')


add('Part B (참고) 이전 판 PASS → 현행 REJECT 전체', 17, prior_false_pass_all, note='헤더 10 + 10-15 보존 반례 7')
nc = lambda s: s['num']['cases']
add('Part B 수치 탐침 건수', 113, lambda s: len(nc(s)))
add('Part B 수치 PASS', 8, lambda s: sum(v.get('status') == 'PASS' for v in nc(s).values()))
add('Part B 수치 REJECT', 105, lambda s: sum(v.get('status') == 'REJECT' for v in nc(s).values()))
add('Part B 수치 예외', 0, lambda s: sum('exception' in v for v in nc(s).values()))
ind = lambda s: s['ind']['summary']
add('Part B 독립 입력 건수', 62, lambda s: ind(s)['n'])
add('Part B 독립 PASS', 32, lambda s: ind(s)['new_pass'])
add('Part B 독립 REJECT', 30, lambda s: ind(s)['new_reject'])
add('Part B 독립 기대 밖', [], lambda s: ind(s)['unexpected'])
add('Part B 독립 PASS 중 공개 F1 잔여', 8, lambda s: sum(1 for r in s['ind']['cases'] if r['known_residual'] and r['current'].get('status') == 'PASS'))
real = lambda s, n: [r for r in s['ind']['real'] if r['name'] == n][0]
add('Part B real14 입자 (scaffold/dump/matched)', [457, 457, 457], lambda s: [real(s, 'real14')['counts'][k] for k in ('n_scaffold', 'n_dump_am', 'n_matched')])
add('Part B real14 AM–AM 접촉', 660, lambda s: real(s, 'real14')['counts']['n_dem_am_am'])
add('Part B case15 입자', [104, 104, 104], lambda s: [real(s, 'case15')['counts'][k] for k in ('n_scaffold', 'n_dump_am', 'n_matched')])
add('Part B case15 AM–AM 접촉', 119, lambda s: real(s, 'case15')['counts']['n_dem_am_am'])
add('Part B real14 구/신 배열 전부 같음', True, lambda s: all(real(s, 'real14')['equal'].values()))
add('Part B case15 구/신 배열 전부 같음', True, lambda s: all(real(s, 'case15')['equal'].values()))


def dbound(s, name):
    r = [x for x in st(s)['results'] if x.get('case') == name][0]
    return r['g_geo']['delta_bound_um']


add('Part B delta_bound_um real14', '0.002915255888325765', lambda s: dbound(s, 'real14'))
add('Part B delta_bound_um case15', '0.002915255888325765', lambda s: dbound(s, 'case15'))
add('Part B wd-only 현행', 'REJECT', lambda s: s['klm']['wd_only_current']['status'])
add('Part B wd-only 현행 사유', ['derived_nonfinite'], lambda s: s['klm']['wd_only_current']['codes'])
add('Part B wd-only 변이', 'PASS', lambda s: s['klm']['wd_only_mutant']['status'])
add('Part B underflow 5e-324 상태', 'PASS', lambda s: s['klm']['known_underflow']['status'])
add('Part B underflow r_um / area', [[0.0, 0.0], [0.0]], lambda s: [s['klm']['known_underflow']['r_um'], s['klm']['known_underflow']['area_um2']])
add('Part B 기본 1000 delta_bound_um', '2.732324012649634e-5', lambda s: s['klm']['normal']['delta_bound_um'])
add('Part B 개행 CRCRLF 수 (RINT2-B-01)', 2, lambda s: s['klm']['newline_fixture']['crcrlf_count'], note='Linux 에서 0 = 재현 안 됨 (예상대로)')
# test counts from our logs only (Codex values in text)
for item, printed, log, cdx in [
    ('Part B 현행 시험 원문 (우리 Linux)', '324/324', 'test_rint2rev_repro_test_rint_g2_join.py_testsfrom_rint2rev_repro.log', 'Windows 320/324'),
    ('Part B 현행 시험 + LF 작성기', '324/324', 'test_rint2rev_repro_test_rint_g2_join.py_testsfrom_rint2rev_repro_lf_adapter.log', '324/324'),
    ('Part B 이전 138 시험 → 현행 모듈', '138/138', 'test_rint2rev_repro_test_rint_g2_join.py_testsfrom_oldtest_2b9efa253.log', '138/138'),
    ('Part B 현행 324 시험 → 2b9efa253 모듈', '179/324', 'test_oldsrc_2b9efa253_test_rint_g2_join.py_testsfrom_rint2rev_repro_lf_adapter.log', '179/324'),
    ('Part B am_iface', '136/136', 'test_rint2rev_repro_test_rint_g2_am_iface.py_testsfrom_rint2rev_repro.log', '136/136'),
    ('Part B rrm', '55/55', 'test_rint2rev_repro_test_rint_g2_rrm.py_testsfrom_rint2rev_repro.log', '55/55'),
    ('Part B t4', '8/8', 'test_rint2rev_repro_test_rint_t4_census.py_testsfrom_rint2rev_repro.log', '8/8'),
    ('Part B t43', '6/6', 'test_rint2rev_repro_test_rint_t43_order.py_testsfrom_rint2rev_repro.log', '6/6'),
    ('Part B t2', '23/23', 'test_rint2rev_repro_test_rint_t2_dev.py_testsfrom_rint2rev_repro.log', '23/23')]:
    v = logcount(log)
    rows.append({'item': item, 'printed': printed, 'ours': v, 'codex_json': cdx, 'ours_matches_printed': v == printed,
                 'codex_json_matches_printed': cdx == printed, 'note': ''})
for item, js in [('Part B step3 --selftest rc', 'test_rint2rev_repro_step3_sigma.py_testsfrom_rint2rev_repro_selftest.json'),
                 ('Part B step3 --selftest-rint rc', 'test_rint2rev_repro_step3_sigma.py_testsfrom_rint2rev_repro_selftest-rint.json'),
                 ('Part B rint_t41_census --selftest rc', 'test_rint2rev_repro_rint_t41_census.py_testsfrom_rint2rev_repro_selftest.json'),
                 ('Part B structure_minimal_replay rc (관문 발화 = 1)', 'probe_rint2rev_repro_structure_minimal_replay.py.json')]:
    rc = harness_rc(js)
    want = 1 if 'minimal' in js else 0
    rows.append({'item': item, 'printed': want, 'ours': rc, 'codex_json': want, 'ours_matches_printed': rc == want,
                 'codex_json_matches_printed': True, 'note': ''})

# ---------------- extra: same Codex probes run on the 2b9efa253 module tree (isolated harness copy part_b_old2b9/)
OLD_EV = os.path.join(W, 'part_b_old2b9', 'evidence')
if os.path.isdir(OLD_EV):
    os_ = L(os.path.join(OLD_EV, 'structure_results.json'))
    on = L(os.path.join(OLD_EV, 'numeric_current.json'))['cases']
    cn = ours['num']['cases']
    up = os_['summary']['unexpected_pass']
    rows.append({'item': '(추가) 2b9efa253 판 구조 탐침: 기대 밖 PASS = 헤더 공격', 'printed': '10 (이전 header 거짓 통과)',
                 'ours': f"{len(up)} = {sorted(up) == sorted(c for c in up if c.endswith(HDR))} (전부 헤더 공격)",
                 'codex_json': '— (판정문 서술)', 'ours_matches_printed': len(up) == 10 and all(c.endswith(HDR) for c in up),
                 'codex_json_matches_printed': None, 'note': 'Codex 구조 탐침을 2b9efa253 모듈 8 + 같은 자료로 실행'})
    p15 = sum(v.get('status') == 'PASS' for v in on.values()); r98 = sum(v.get('status') == 'REJECT' for v in on.values())
    rows.append({'item': '(추가) 2b9efa253 판 수치 탐침 PASS/REJECT', 'printed': '15/98', 'ours': f'{p15}/{r98}',
                 'codex_json': '— (판정문 서술)', 'ours_matches_printed': (p15, r98) == (15, 98), 'codex_json_matches_printed': None, 'note': ''})
    flip = [k for k in on if on[k].get('status') == 'PASS' and cn.get(k, {}).get('status') != 'PASS']
    nu = sum('unicode' in k for k in flip); nov = sum(cn[k].get('codes') == ['derived_nonfinite'] for k in flip)
    rows.append({'item': '(추가) PASS→REJECT 전환 = unicode + overflow', 'printed': '1 + 6', 'ours': f'{nu} + {nov} (총 {len(flip)})',
                 'codex_json': '— (판정문 서술)', 'ours_matches_printed': (nu, nov, len(flip)) == (1, 6, 7), 'codex_json_matches_printed': None, 'note': ''})

json.dump(rows, open(OUT_J, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
n_ok = sum(1 for r in rows if r['ours_matches_printed'])
bad = [r for r in rows if not r['ours_matches_printed']]
with open(OUT_M, 'w', encoding='utf-8') as f:
    f.write('| 항목 | 판정문 값 | 우리 값 | Codex JSON | 우리=판정문 |\n|---|---|---|---|---|\n')
    for r in rows:
        o = r['ours'] if not isinstance(r['ours'], float) else f"{r['ours']:.15g}"
        c = r['codex_json'] if not isinstance(r['codex_json'], float) else f"{r['codex_json']:.15g}"
        f.write(f"| {r['item']} | {r['printed']} | {o} | {c} | {'같음' if r['ours_matches_printed'] else '**다름**'} |\n")
print(f'items {len(rows)} · ours=printed {n_ok} · differ {len(bad)}')
for r in bad:
    print('  DIFF', r['item'], '| printed', r['printed'], '| ours', r['ours'], '| codex', r['codex_json'], '| codex=printed', r['codex_json_matches_printed'])
cm = [r for r in rows if r['codex_json_matches_printed'] is False]
print('codex JSON not matching printed:', [(r['item'], r['printed'], r['codex_json']) for r in cm])
