#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L214R-02 — 띠 폴백 (BAND_FALLBACK) 이 H0 FULL 모형 한계의 배포 HOLD 를 가리지 않게: FULL 모형 한계 **독립 표지** 두 칸 (시험 먼저).

  python3 scripts/test_l214r02_model_limit_flag.py

근거 = Codex 재검증 판정 `docs/reviews/codex_review_lhs214_fix_reverify_20261015.md` §3 (L214R-02) · §6 4 · 7 · 10 · §8 Q4 · §9-2 ·
수정 계획 `docs/reviews/lhs214r_fix_plan_20261016.md` (1저자 10-16 Q1–Q5 권고대로 — Q2 = 인계표 새 칸 `full_model_limit_hertz` · `full_model_limit_physics`
(참 / 거짓) · 배포 build · check 가 이 칸으로 H0 주 타깃 HOLD · ML 사용자도 공란 이유를 본다) · 탐침
`docs/reviews/codex_lhs214_fix_reverify_evidence_20261015/probes/l214_consumers.py` (기본 · --release — 실행하지 않았다 · 같은 꼴을 우리 시험으로 옮겼다).

★ 시험 먼저 — 고치기 전 코드에서 빨갛다: τ 상태 표시는 띠 폴백 우선 (L1 · L2 → BAND_FALLBACK · 사유 공란) 이고 배포 관문은 NOT_COMPUTED + full_over_conduction
  만 모형 한계로 읽어, L1 · L2 + H0 모형 한계 행이 27 파일로 배포되고 check 가 문제 0 을 낸다 (Codex 표).  L0 대조는 이미 HOLD.
  D  배포 관문 함수 (`lhs_release_build.v13_primary_model_limit_problems` — build · check 공용) — 표지 True + BAND_FALLBACK = HOLD · 표지 값 모름 · 열 없음 ·
     표지 ↔ 상태 모순 = 문제 · Physics · H12 만 모형 한계 = 문제 아님 (정책 그대로) · 이름 짝 · 모형 한계 집계 (상태 셈) 에서 빠지지 않는다
  A  실 생산자 레코드 (`network_conductivity._run_all_networks`) — 띠 L0 · L1 · L2 × 모형 한계 없음 · Physics 만 · H12 (+ Physics — Physics q 가 늘 더 크다) ·
     H0 (세 모드) = 12 침대: 옛 50 열 이름 · 자리 그대로 · 표지 둘은 끝 · τ 상태 표시 우선순위 그대로 · 표지 = 공용 판정 (`tau_flux.full_model_limit_problem`
     · 띠와 무관) · 위조 = False · 세대 무효 · 레코드 없음 = 빈칸 · 정상 행 값 그대로 (항등식 + 고치기 전 실측 기준값)
  B  실 사슬 — 생산자 CLI → 게시 (`app._network_and_stage_e` 정지 경로) → `load_tau_results` (P0–P4 · 기대 세대 g2) → `build_handover` 묶음 tau (12 침대):
     게시 done · 인계 칸 = `tau_flux.case_row` · 표지 칸 값 · 열 사전 · 관문 — H0 모형 한계 = HOLD (L0 · L1 · L2) · 나머지 9 = 통과
  C  실제 배포 빌더 (`build_v13(dry_run=False, diagnostic=False)` · `check_v13`) — Codex `--release` 꼴: 선택 행 = B 의 실 인계 칸 (실 K1–K7 · 실 τ 원천) ·
     나머지 행 · 감사 · 배치 기록 = `test_lhs_release_v13` 합성 픽스처 · τ 다시 읽기 비교 함수는 그대로 (원천 공급만 어댑터):
     L1 · L2 + H0 = 빌드 거부 (HOLD) · 진단 빌드 경고 · 배포 대조 문제 · 재적합 제외 사유에 모형 한계 원인 / L0 + H0 대조 = 거부 그대로 /
     L1 띠 폴백만 · L1 Physics 만 · L2 H12 = 만들고 대조 통과 · 배포 주 표 · Physics 부록에 표지 열 (가려진 Physics 모형 한계 = True · README 집계)
⚠ 범위 — 분류 · 게시 · 인계 · 배포 계약의 시험 (작은 합성 사슬 · 상자를 줄인 φ_SE > 1 합성 기하 포함 — 물리 침대 아님 · 발생률 · 물리 타당성 주장 아님).
  C 의 213 행 · 감사 · 배치 기록은 합성 — 실제 214 생산 배포 통과가 아니다.
"""
import ast
import contextlib
import copy
import csv
import io
import json
import math
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
for _p in (str(HERE), str(ROOT / 'webapp')):
    if _p not in sys.path:
        sys.path.insert(0, _p)

ML = 'full_over_conduction'
FLAG = {'hertz': 'full_model_limit_hertz', 'physics': 'full_model_limit_physics'}
MODES = ('hertz', 'physics', 'hertz_h12')
DATE = '20991231'
_ok, _fail = 0, []


def chk(name, cond, extra=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'   {str(extra)[:500]}' if extra else ''))
    return cond


def _guard(label, fn):
    """묶음 하나가 예외로 죽어도 나머지를 센다 (고치기 전 코드 — 없는 이름 · 인자 = 그 묶음 FAIL)."""
    try:
        fn()
    except Exception as e:                                       # noqa: BLE001
        import traceback
        traceback.print_exc()
        chk(f'{label} — 예외 없이 끝난다 ({type(e).__name__}: {e})', False)


def quiet(fn, *a, **kw):
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return fn(*a, **kw)


#  ── 침대 (A · B 공용) ────────────────────────────────────────────────────────────────────────────────────────────────────────────────
#  L0 = 21 구 사슬 (반경 1 · z 0..20 · 판 20 · 면적 0.5 · δ 0.2 — test_pipeline_provenance 의 ml_physics · ml_hertz 와 같은 사슬) · L1 = band_l1 사슬
#  (반경 0.4 · 81 구 · z 0..40 간격 0.5 · 판 40) · L2 = band_l2 사슬 (21 구 · z 0..10 · 판 40) — 상자 변만 바꾼다 (q ∝ 1/상자 넓이 · 망 · 간선 그대로 ·
#  Codex 탐침은 band_l1 · band_l2 의 상자 0.1).  q (H0 · H12 · Physics) = 이 리포 생산자 실측 (10-16 · 고치기 전 코드):
#    L0 2.0 0.199 · 0.336 · 0.648 | 1.0 0.795 · 1.342 · 2.593 | 0.85 1.101 · 1.858 · 3.590 | 0.7 1.623 · 2.739 · 5.293
#    L1 10 0.0009 · 0.0011 · 0.0015 | 0.3 0.992 · 1.248 · 1.685 | 0.257 1.352 · 1.700 · 2.296 | 0.1 8.93 · 11.23 · 15.17
#    L2 10 0.0036 · 0.0045 · 0.0061 | 0.6 0.992 · 1.248 · 1.685 | 0.514 1.352 · 1.700 · 2.296 | 0.1 35.7 · 44.9 · 60.7
#  ⇒ 모형 한계 (q > 1.5) 모드: none = 없음 · phys = Physics · h12 = H12 + Physics · h0 = 세 모드.  ('H12 만' 은 없다 — Physics q 가 늘 더 크다.)
BEDS = {
    'L0_none': ('L0', (), 'l0', 2.0), 'L0_phys': ('L0', ('physics',), 'l0', 1.0),
    'L0_h12': ('L0', ('physics', 'hertz_h12'), 'l0', 0.85), 'L0_h0': ('L0', MODES, 'l0', 0.7),
    'L1_none': ('L1', (), 'l1', 10.0), 'L1_phys': ('L1', ('physics',), 'l1', 0.3),
    'L1_h12': ('L1', ('physics', 'hertz_h12'), 'l1', 0.257), 'L1_h0': ('L1', MODES, 'l1', 0.1),
    'L2_none': ('L2', (), 'l2', 10.0), 'L2_phys': ('L2', ('physics',), 'l2', 0.6),
    'L2_h12': ('L2', ('physics', 'hertz_h12'), 'l2', 0.514), 'L2_h0': ('L2', MODES, 'l2', 0.1),
}
H0_BEDS = ('L0_h0', 'L1_h0', 'L2_h0')

#: 고치기 전 τ 열 50 (모드 셋 × 15 + 공통 5 · 10-06 밤 판) — 이름 · 순서가 그대로 앞자리에 남아야 한다 (인계표 · 배포 열 순서 불변)
OLD50 = [c for m in MODES for c in (f'f_ion_{m}', f'f_ion_{m}_gap', f'tau2_ion_{m}', f'tau_ion_{m}', f'ion_net_status_{m}',
                                        f'ion_net_status_reason_{m}', f'ion_net_area_mode_{m}', f'ion_net_constriction_{m}', f'ion_net_psi_{m}',
                                        f'ion_net_area_rule_{m}', f'ion_net_electrode_{m}', f'ion_net_bulk_{m}', f'ion_net_band_rule_{m}',
                                        f'ion_net_band_frac_{m}', f'ion_net_basis_check_{m}')] + [
    'ion_sigma0_mScm', 'ion_sigma0_T_C', 'phi_basis', 'L_basis', 'ion_net_generation']

#: 고치기 전 코드 실측 (10-16 · `tau_flux.ion_columns` · repr) — 정상 행 값이 그대로인가 (상대 1e-9 — 플랫폼 사이 끝자리 차는 허용)
PRE_FIX = {
    'L0_none': {'f_ion_hertz': 0.19883891, 'f_ion_hertz_gap': 0.19883891, 'tau2_ion_hertz': 5.5298906474413245, 'tau_ion_hertz': 2.3515719524269985,
                'f_ion_physics': 0.64836713, 'tau2_ion_physics': 1.6958870644112192, 'tau_ion_physics': 1.3022622871031853,
                'f_ion_hertz_h12': 0.33556115, 'tau2_ion_hertz_h12': 3.276772143486895, 'tau_ion_hertz_h12': 1.8101856654738195,
                'ion_net_band_frac_hertz': 0.2, 'ion_sigma0_mScm': 3.0, 'ion_sigma0_T_C': 25.0},
    'L0_phys': {'f_ion_hertz': 0.79535562, 'tau2_ion_hertz': 5.529890786495868, 'tau_ion_hertz': 2.3515719819932936,
                'f_ion_hertz_h12': 1.34224459, 'tau2_ion_hertz_h12': 3.276772167899525},
    'L1_none': {'ion_net_band_frac_hertz': 0.3, 'ion_net_band_frac_physics': 0.3, 'ion_net_band_frac_hertz_h12': 0.3, 'ion_sigma0_mScm': 3.0},
}


def bed(name):
    """침대 → (atoms, contacts, plate_z, box) — test_pipeline_provenance._bed 와 같은 꼴."""
    _band, _ml, kind, box = BEDS[name]
    if kind == 'l0':
        A = {i: dict(type=1, x=0., y=0., z=float(z), radius=1.) for i, z in enumerate(range(21), 1)}
        C = [dict(id1=i, id2=i + 1, contact_area=0.5, delta=0.2) for i in range(1, 21)]
        return A, C, 20.0, box
    n = 81 if kind == 'l1' else 21
    A = {i: dict(type=1, x=0., y=0., z=0.5 * k, radius=0.4) for i, k in enumerate(range(n), 1)}
    C = [dict(id1=i, id2=i + 1, contact_area=0.1 * 0.16, delta=0.05 * 0.4) for i in range(1, n)]
    return A, C, 40.0, box


def produce(nc, b):
    """실 생산자 두 모드 (CLI 가 모드 파일 · dual 에 쓰는 바로 그 dict) — JSON 왕복 = 디스크 모양."""
    A, C, plate, box = b
    recs = {cm: quiet(nc._run_all_networks, A, C, [1], [], {1: 'SE'}, 1, plate, box, box, None, contact_mode=cm)
            for cm in ('hertzian', 'physics')}
    return json.loads(json.dumps(recs))


def ledger(dac, b):
    """접촉 분석 장부 (test_pipeline_provenance._bed_ledger 와 같은 식) — (장부, calc_percolation 의 percolation_pct)."""
    A, C, plate, box = b
    cp = quiet(dac.calc_percolation, A, C, [1], plate, box_x=box, box_y=box)
    phi = sum(4.0 / 3.0 * math.pi * a['radius'] ** 3 for a in A.values() if a['type'] == 1) / (box * box * plate)
    return {'thickness_um': plate, 'thickness_mass_conserving_um': plate, 'phi_se_mass_conserving': phi}, cp['percolation_pct']


def _close(a, b, rel=1e-9):
    return isinstance(a, float) and math.isfinite(a) and abs(a - b) <= rel * max(abs(a), abs(b), 1e-300)


# ══ D. 배포 관문 함수 (build · check 공용) ═══════════════════════════════════════════════════════════════════════════════════════════
def sec_D():
    import lhs_release_build as LRB
    import tau_flux as tf
    print('D  배포 관문 함수 — v13_primary_model_limit_problems (build_v13 · check_v13 같은 함수)')
    gate = LRB.v13_primary_model_limit_problems
    ok = {'case_id': 'd_ok', 'ion_net_status_hertz': 'OK', 'ion_net_status_reason_hertz': '', 'ion_net_status_physics': 'OK',
          'ion_net_status_reason_physics': '', FLAG['hertz']: 'False', FLAG['physics']: 'False'}
    g1 = gate([dict(ok, case_id='d_l1h0', ion_net_status_hertz='BAND_FALLBACK', ion_net_status_physics='BAND_FALLBACK',
                    **{FLAG['hertz']: 'True', FLAG['physics']: 'True'})])
    chk(f"D1 ★ 표지 full_model_limit_hertz = True + 상태 BAND_FALLBACK (사유 공란) → 주 타깃 HOLD (옛: 문제 0 — 상태만 읽었다) {g1}",
        bool(g1) and any('HOLD' in p and 'd_l1h0' in p for p in g1))
    chk('D2 정상 행 (표지 False · OK) → 문제 0 (정상 행 그대로)', gate([ok]) == [], gate([ok]))
    bad3 = {v: gate([dict(ok, **{FLAG['hertz']: v})]) for v in ('true', '', 'yes', '1', 'None')}
    chk(f'D3 ★ 표지 값 모름 (소문자 true · 빈칸 · yes · 1 · None) → 문제 (fail-closed — 판정할 수 없는 행을 통과시키지 않는다) {bad3}',
        all(p and any(FLAG['hertz'] in x for x in p) for p in bad3.values()))
    miss = {k: v for k, v in ok.items() if k != FLAG['hertz']}
    g4 = gate([miss])
    chk(f'D4 ★ 표지 열 없음 (옛 생성기 인계표) → 문제 (주 타깃 모형 한계 사실을 확인할 수 없다) {g4}', bool(g4) and any(FLAG['hertz'] in p for p in g4))
    g5 = gate([dict(ok, case_id='d_contra', ion_net_status_hertz='NOT_COMPUTED', ion_net_status_reason_hertz=ML)])
    chk(f'D5 ★ 표지 False ↔ 상태 NOT_COMPUTED full_over_conduction (모순) → HOLD (상태 기준 그대로) + 모순 보고 {g5}',
        any('HOLD' in p for p in g5) and any('모순' in p for p in g5))
    g5b = gate([dict(ok, case_id='d_contra2', **{FLAG['hertz']: 'True'})])
    chk(f'D5b 표지 True ↔ 상태 OK (값이 있는 FULL 과 모순) → HOLD + 모순 보고 {g5b}', any('HOLD' in p for p in g5b) and any('모순' in p for p in g5b))
    g6 = gate([dict(ok, case_id='d_phys', ion_net_status_physics='BAND_FALLBACK', **{FLAG['physics']: 'True'}),
               dict(ok, case_id='d_phys0', ion_net_status_physics='NOT_COMPUTED', ion_net_status_reason_physics=ML, **{FLAG['physics']: 'True'})])
    chk(f'D6 Physics 만 모형 한계 (표지 physics True · 띠 폴백 · L0 둘) → 문제 0 (Physics = opt-in 부록 정책 그대로 · 넓히지 않는다) {g6}', g6 == [])
    g7 = gate([dict(ok, case_id='d_h12', ion_net_status_hertz_h12='NOT_COMPUTED', ion_net_status_reason_hertz_h12=ML)])
    chk(f'D7 H12 만 모형 한계 → 문제 0 (H12 민감도 부록 정책 그대로 · H12 표지 열은 없다 — 1저자 Q2 두 칸) {g7}', g7 == [])
    g7b = gate([dict(ok, case_id='d_l0h0', ion_net_status_hertz='NOT_COMPUTED', ion_net_status_reason_hertz=ML, **{FLAG['hertz']: 'True'})])
    chk(f'D7b L0 대조 (상태 NOT_COMPUTED full_over_conduction · 표지 True) → HOLD 그대로 (모순 보고 없음) {g7b}',
        any('HOLD' in p and 'd_l0h0' in p for p in g7b) and not any('모순' in p for p in g7b))
    fl = getattr(LRB, 'V13_MODEL_LIMIT_FLAG', None)
    chk(f"D8 이름 짝 — 배포 빌더 V13_MODEL_LIMIT_FLAG = tau_flux.MODEL_LIMIT_FLAG_COL = {FLAG} · 직렬화 tau_flux._cell(True) = 'True' (인계표 값)",
        fl == FLAG and getattr(tf, 'MODEL_LIMIT_FLAG_COL', None) == FLAG and tf._cell(True) == 'True' and tf._cell(False) == 'False', (fl,))
    sc = LRB._v13_status_counts([dict(ok, ion_net_status_physics='BAND_FALLBACK', **{FLAG['physics']: 'True'}),
                                 dict(ok, case_id='d2', ion_net_status_physics='BAND_FALLBACK')], 'ion_net_status_physics')
    chk(f'D9 ★ 모형 한계 원인 집계 (Codex §6-10) — 띠 폴백에 가려진 Physics 모형 한계는 상태 셈에서 따로 (BAND_FALLBACK 순수와 섞지 않는다) {sc}',
        len(sc) == 2 and any(ML in k and k.startswith('BAND_FALLBACK') for k in sc) and sc.get('BAND_FALLBACK') == 1)
    mlf = getattr(LRB, 'v13_model_limit', None)
    chk('D10 모형 한계 판정 도우미 v13_model_limit — 상태 (NOT_COMPUTED full_over_conduction) 또는 표지 True · 그 밖 = 아님',
        callable(mlf) and mlf(dict(ok, ion_net_status_hertz='BAND_FALLBACK', **{FLAG['hertz']: 'True'}), 'hertz')
        and mlf(dict(ok, ion_net_status_hertz='NOT_COMPUTED', ion_net_status_reason_hertz=ML), 'hertz')
        and not mlf(ok, 'hertz') and not mlf(dict(ok, ion_net_status_hertz='BAND_FALLBACK'), 'hertz')
        and not mlf(dict(ok, **{FLAG['hertz']: 'true'}), 'hertz'))


# ══ A. 실 생산자 레코드 → τ 소비자 (ion_columns) ═══════════════════════════════════════════════════════════════════════════════════
def sec_A(state):
    import network_conductivity as nc
    import tau_flux as tf
    import dem_analysis_core as dac
    print('A  실 생산자 레코드 (12 침대 · 띠 L0 · L1 · L2 × 모형 한계 없음 · Physics · H12 · H0) → tau_flux.ion_columns')
    cols = tf.column_names()
    chk('A0 옛 τ 50 열의 이름 · 자리 그대로 (앞자리) — 인계표 · 배포의 옛 열 순서 불변', cols[:50] == OLD50, cols[:3])
    chk(f'A1 ★ 표지 두 칸 full_model_limit_hertz · full_model_limit_physics = τ 열 끝 (H12 표지 없음 — 1저자 Q2 두 칸) {cols[50:]}',
        cols[50:] == [FLAG['hertz'], FLAG['physics']])
    rows = {}
    for name in BEDS:
        b = bed(name)
        du = produce(nc, b)
        led, pp = ledger(dac, b)
        rows[name] = (du, tf.ion_columns(du, led, pp), led)
    state['A_rows'] = rows
    bad2 = {}
    for name, (du, row, _l) in rows.items():
        band, mls = BEDS[name][:2]
        for m in MODES:
            st = (row.get(f'ion_net_status_{m}'), row.get(f'ion_net_status_reason_{m}'))
            want = ('BAND_FALLBACK', '') if band != 'L0' else (('NOT_COMPUTED', ML) if m in mls else ('OK', ''))
            if st != want or row.get(f'ion_net_band_rule_{m}') != band:
                bad2[(name, m)] = (st, row.get(f'ion_net_band_rule_{m}'))
    chk('A2 τ 상태 표시 우선순위 그대로 — L0: 모형 한계 모드 NOT_COMPUTED full_over_conduction · 나머지 OK / L1 · L2: 세 모드 BAND_FALLBACK · 사유 공란 '
        '(띠 폴백 먼저 — Codex §6-7 표시 순서 수용) · 띠 규칙 칸 = 침대 띠', not bad2, bad2)
    bad3 = {}
    for name, (du, row, _l) in rows.items():
        mls = BEDS[name][1]
        for m, col in FLAG.items():
            if row.get(col, 'ABSENT') is not (m in mls):
                bad3[(name, m)] = row.get(col, 'ABSENT')
    chk('A3 ★ 표지 = 그 모드 FULL 모형 한계 사실 · 띠와 무관 — L1 · L2 + H0 = full_model_limit_hertz True (상태는 BAND_FALLBACK 인데도) · Physics · H12 (+Physics) '
        '= hertz False · physics True · 모형 한계 없음 = 둘 다 False (12 침대 × 두 모드)', not bad3, bad3)
    bad4 = {}
    for name, (du, row, _l) in rows.items():
        for m, col in FLAG.items():
            want = tf.full_model_limit_problem(tf.mode_record(du, m), 'ionic', m) is None
            if row.get(col, 'ABSENT') is not want:
                bad4[(name, m)] = (row.get(col, 'ABSENT'), want)
    chk('A4 표지 = 공용 판정 tau_flux.full_model_limit_problem (자리 모드) 그대로 — 새 판정을 만들지 않는다 (규율 ①)', not bad4, bad4)
    led1 = rows['L1_h0'][2]
    fq = copy.deepcopy(rows['L1_h0'][0])
    fq['hertzian']['solve_certificate_full']['q_withheld'] *= 1.01
    rq = tf.ion_columns(fq, led1, 100.0)
    fr = copy.deepcopy(rows['L1_none'][0])
    fr['hertzian'].update(sigma_full_status='not_computed', sigma_full_reason=ML)
    rr = tf.ion_columns(fr, rows['L1_none'][2], 100.0)
    chk(f"A5 위조 — L1 + H0 증서 q ×1.01 · 값이 남은 레코드에 사유만 full_over_conduction → 표지 False (모형 한계 아님) · 상태 NOT_COMPUTED invalid_input "
        f"(0b 공용 판정 — 띠 게이트 앞) ({rq.get(FLAG['hertz'], 'ABSENT')!r} · {rr.get(FLAG['hertz'], 'ABSENT')!r} · "
        f"{tf.reason_code(rq.get('ion_net_status_reason_hertz'))!r} · {tf.reason_code(rr.get('ion_net_status_reason_hertz'))!r})",
        rq.get(FLAG['hertz'], 'ABSENT') is False and rr.get(FLAG['hertz'], 'ABSENT') is False
        and tf.reason_code(rq.get('ion_net_status_reason_hertz')) == 'invalid_input' and tf.reason_code(rr.get('ion_net_status_reason_hertz')) == 'invalid_input')
    go = tf.generation_override(dict(rows['L1_h0'][1]), '합성 세대 무효 (시험)')
    chk('A6 케이스 폴더 세대 무효 (generation_override) → 표지 두 칸 빈칸 (None — 확정되지 않은 세대의 사실을 싣지 않는다) · 상태 generation_invalid',
        all(k in go and go[k] is None for k in FLAG.values()) and str(go.get('ion_net_status_reason_hertz', '')).startswith('generation_invalid'),
        {k: go.get(k, 'ABSENT') for k in FLAG.values()})
    rm = tf.ion_columns({'hertzian': rows['L0_none'][0]['hertzian']}, rows['L0_none'][2], 100.0)
    chk(f"A7 레코드 없는 모드 (physics 없음) → 그 표지 빈칸 (None) · 있는 모드 (hertz computed) = False "
        f"({rm.get(FLAG['physics'], 'ABSENT')!r} · {rm.get(FLAG['hertz'], 'ABSENT')!r})",
        FLAG['physics'] in rm and rm[FLAG['physics']] is None and rm.get(FLAG['hertz'], 'ABSENT') is False)
    bad8 = {}
    for name, (du, row, led) in rows.items():
        for m in MODES:
            if row.get(f'ion_net_status_{m}') not in ('OK', 'MODEL_BELOW_CONTINUUM_BOUND'):
                if any(row.get(k) is not None for k in (f'f_ion_{m}', f'tau2_ion_{m}', f'tau_ion_{m}')):
                    bad8[(name, m)] = '값이 남았다'
                continue
            q = tf.mode_record(du, m).get('sigma_full')
            f = q * led['thickness_um'] / led['thickness_mass_conserving_um']
            t2 = led['phi_se_mass_conserving'] / f
            if not (row[f'f_ion_{m}_gap'] == q and _close(row[f'f_ion_{m}'], f) and _close(row[f'tau2_ion_{m}'], t2)
                    and _close(row[f'tau_ion_{m}'], math.sqrt(t2))):
                bad8[(name, m)] = (row[f'f_ion_{m}'], f)
    for name, want in PRE_FIX.items():
        row = rows[name][1]
        for k, v in want.items():
            if not _close(row.get(k), v):
                bad8[(name, k)] = (row.get(k), v)
    chk('A8 정상 값 그대로 — 값 있는 모드: f_gap = σ_ratio · f = σ_ratio·L_gap/L_mc · T = φ_mc/f · √T (생산 식) · 값 없는 모드: f · T · √T 빈칸 · '
        '고치기 전 실측 기준값 (L0 모형 한계 없음 · L0 Physics 만의 H0 · H12 · L1 띠 폴백 띠 폭 · σ₀) 상대 1e-9 안', not bad8, bad8)


# ══ B. 실 사슬 — 생산자 CLI → 게시 → load_tau_results → build_handover ═══════════════════════════════════════════════════════════════
def sec_B(state, tmp):
    import app
    import pipeline_service as ps
    import tau_flux as tf
    import test_pipeline_provenance as TP
    import test_network_handover_chain as CH
    import lhs_design_dataset as LDD
    import lhs_webapp_batch as LWB
    import lhs_release_build as LRB
    print('B  실 사슬 (생산자 CLI → 정지 경로 게시 → load_tau_results P0–P4 · 기대 세대 g2 → build_handover 묶음 tau)')
    orig = TP._bed
    TP._bed = lambda n: bed(n) if n in BEDS else orig(n)
    runs = {}
    try:
        for name in BEDS:
            runs[name] = quiet(CH._run_ml, app, name)
            tmp.append(runs[name][0])
    finally:
        TP._bed = orig
    st = {k: v[1] for k, v in runs.items()}
    chk(f'B1 12 침대 게시 = done (L1 · L2 + 모형 한계 포함 — 진단 게시는 막지 않는다 · Codex §6-4) {st}', all(v == 'done' for v in st.values()))
    src = ROOT / 'docs/data/lhs_webapp_contact_d1ec42fba'
    st0 = json.loads((src / 'status.json').read_text(encoding='utf-8'))
    with (src / 'metrics_flat.csv').open(encoding='utf-8', newline='') as fh:
        flat = {r['case']: {k: v for k, v in r.items() if v != ''} for r in csv.DictReader(fh)}
    cands = sorted(c for c, s in st0['cases'].items() if s.get('status') == 'done' and float(flat.get(c, {}).get('percolation_pct') or 0) > 0)
    mapping = dict(zip(BEDS, cands))
    work = Path(tempfile.mkdtemp(prefix='l214r02_handover_'))
    tmp.append(str(work))
    results = work / 'results'
    results.mkdir()
    bstate = copy.deepcopy(st0)
    bstate.update(stop_after='network', cases={})
    brows = {}
    tie = tuple(ps.NETWORK_STOP_LEDGER_KEYS) + tuple(LDD.TAU_TIE_EXTRA)
    for name, cid in mapping.items():
        d_, s_, f_, rid_ = runs[name]
        shutil.copytree(d_, results / cid)
        bstate['cases'][cid] = dict(st0['cases'][cid], stop_after='network', status=s_, failed_stages=f_, network_run_id=rid_)
        fm_ = json.loads((results / cid / 'full_metrics.json').read_text(encoding='utf-8'))
        brows[cid] = dict(flat[cid], **{k: fm_[k] for k in tie if k in fm_})
    LWB.write_outputs(work / 'batch', bstate, brows)
    web = LDD.load_webapp(work / 'batch')
    tau = LDD.load_tau_results(results, web, expected_generation='g2')
    with (ROOT / LDD.DESCRIPTOR_FILL_EXPECTED['path']).open(encoding='utf-8-sig') as fh:
        design = [r for r in csv.DictReader(fh) if r['case_id'] in set(mapping.values())]
    hv = LDD.load_harvest(ROOT / 'docs/data/lhs_descriptors_cov_1e09f661d')
    un = LDD.load_union(ROOT / LDD.DEFAULT_UNION_TSV)
    hrows, hcols, hrep = LDD.build_handover(design, hv, union=un, webapp=web, webapp_groups='tau', tau=tau)
    by_id = {r['case_id']: r for r in hrows}
    hb = {name: by_id.get(cid, {}) for name, cid in mapping.items()}
    state.update(B_runs=runs, B_mapping=mapping, B_rows=hb, B_tau=tau, B_results=results, B_hcols=hcols)
    tcols = list(tf.column_names())
    want = {name: {c: tf._cell(v) for c, v in tf.case_row(str(results / cid)).items() if c in tcols} for name, cid in mapping.items()}
    badc = [name for name in BEDS if {c: hb[name].get(c) for c in tcols} != want[name]]
    chk(f"B2 인계 τ 칸 = tau_flux.case_row 그대로 (P0–P4 통과 · 출처 관문 {hrep.get('tau_checked')} 행) — 다른 침대 {badc}",
        not badc and hrep.get('tau_checked') == len(BEDS))
    bad3 = {}
    for name, r in hb.items():
        mls = BEDS[name][1]
        for m, col in FLAG.items():
            if r.get(col, 'ABSENT') != ('True' if m in mls else 'False'):
                bad3[(name, m)] = r.get(col, 'ABSENT')
    chk("B3 ★ 인계표 표지 칸 — H0 모형 한계 (L0 · L1 · L2) = full_model_limit_hertz 'True' · Physics 모형 한계 = full_model_limit_physics 'True' · 그 밖 'False' "
        "(띠 L1 · L2 의 BAND_FALLBACK 행에서도 사실이 남는다)", not bad3, bad3)
    bad4 = {name: (r.get('ion_net_status_hertz'), r.get('ion_net_status_reason_hertz')) for name, r in hb.items()
            if BEDS[name][0] != 'L0' and (r.get('ion_net_status_hertz'), r.get('ion_net_status_reason_hertz')) != ('BAND_FALLBACK', '')}
    chk('B4 인계 τ 상태 표시 그대로 — L1 · L2 행 = BAND_FALLBACK · 사유 공란 (표시 우선순위 유지 · 띠 폴백 행을 새로 막지 않는다)', not bad4, bad4)
    dct = {d['column']: d for d in LDD.column_dictionary(hcols, webapp=web)}
    bad5 = {c: dct.get(c, {}).get('meaning', 'ABSENT')[:80] for c in FLAG.values()
            if not (c in hcols and dct.get(c, {}).get('source') == 'tau_flux'
                    and all(k in dct[c].get('meaning', '') for k in ('True', 'False', 'BAND_FALLBACK', 'full_over_conduction', '띠')))}
    chk('B5 열 사전 — 표지 두 칸이 인계표 열에 있고 뜻 (원천 tau_flux · True / False · 띠와 무관 · BAND_FALLBACK 에 가려지는 사실 · full_over_conduction)',
        not bad5, bad5)
    gate = LRB.v13_primary_model_limit_problems
    bad6 = {}
    for name, r in hb.items():
        g = gate([r])
        hold = bool(g) and any('HOLD' in p for p in g)
        if hold != (name in H0_BEDS):
            bad6[name] = g[:1]
    chk('B6 ★ 배포 관문 (인계 행) — H0 모형 한계 = HOLD (L0 대조 · L1 · L2 — 옛: L1 · L2 는 문제 0) · Physics · H12 · 모형 한계 없음 · 띠 폴백만 = 통과 (9 행)',
        not bad6, bad6)


# ══ C. 실제 배포 빌더 (build_v13 · check_v13) ════════════════════════════════════════════════════════════════════════════════════════
C_TARGETS = (('L0_h0', True), ('L1_h0', True), ('L2_h0', True), ('L1_none', False), ('L1_phys', False), ('L2_h12', False))


def _release_helpers():
    """test_lhs_release_v13 의 합성 픽스처 (머리 ~ stage13 정의까지) — 그 파일을 고치지 않고 정의만 실행한다 (Codex --release 탐침과 같은 방식)."""
    helper = HERE / 'test_lhs_release_v13.py'
    tree = ast.parse(helper.read_text(encoding='utf-8'))
    end = next(i for i, n in enumerate(tree.body) if isinstance(n, ast.FunctionDef) and n.name == 'stage13')
    env = {'__file__': str(helper), '__name__': 'l214r02_release_fixture'}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(ast.Module(body=tree.body[:end + 1], type_ignores=[]), str(helper), 'exec'), env)
    return env


def sec_C(state, tmp):
    import tau_flux as tf
    import lhs_release_build as LRB
    import lhs_design_dataset as LDD
    import g2_network_reread as RR
    import pipeline_service as ps
    import logging
    logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)
    print('C  실제 배포 빌더 (build_v13 dry_run False · diagnostic False / check_v13) — 선택 행 = B 의 실 인계 칸 · 나머지 = 합성 픽스처')
    if 'B_rows' not in state:
        chk('C — B 의 실 인계 행이 없다 (B 실패)', False)
        return
    env = _release_helpers()
    mapping, hb, tau, results = state['B_mapping'], state['B_rows'], state['B_tau'], state['B_results']
    orig_rr = LRB.v13_reread_tau
    for name, hold in C_TARGETS:
        cid, target = mapping[name], hb[name]
        croot = Path(tempfile.mkdtemp(prefix=f'l214r02_rel_{name}_'))
        tmp.append(str(croot))

        def mutate(ds, head, rows, cid=cid, target=target):
            if ds == 'lhs':
                row = next(r for r in rows if r['case_id'] == cid)
                row.update({c: target[c] for c in tf.column_names()})
        handover = quiet(env['make_g2_handover_dir'], str(croot / 'handover'), mutate=mutate)
        batch = quiet(env['make_batch_root'], str(croot / 'batch'))
        gp = Path(batch) / 'reread.json'
        gate_rec = json.loads(gp.read_text(encoding='utf-8'))
        actual = RR.reread_case(results / cid, 'g2', ps, tf)                 # 선택 행의 실제 K1–K7 (실 생산자 게시 폴더)
        for r in gate_rec['cases']:
            if r['case'] == cid:
                r.update(checks=actual['checks'], statuses=actual['statuses'], row_cells=actual['row_cells'])
        gp.write_text(json.dumps(gate_rec, ensure_ascii=False), encoding='utf-8')
        verdict = croot / 'fixture_verdict.txt'
        verdict.write_text('TEST ONLY — 합성 픽스처 판정문 (배포 승인 아님)\n', encoding='utf-8')

        def rr_adapter(ds, batch_root, rows, expected, cid=cid):
            """τ 다시 읽기 — 비교 함수 (v13_reread_tau) 는 그대로 · 원천 공급만: 선택 행 = 실 load_tau_results 칸 · 나머지 = 인계표 칸 (합성)."""
            o_load, o_web = LDD.load_tau_results, LDD.load_webapp

            def provision(*a, **kw):
                cells = {r['case_id']: {'cells': {c: r.get(c, '') for c in tf.column_names()}} for r in rows}
                if ds == 'lhs':
                    cells[cid] = tau['cases'][cid]
                return {'schema': LDD.TAU_NET_SCHEMA, 'cases': cells}
            LDD.load_tau_results, LDD.load_webapp = provision, (lambda *a, **kw: {'stop_after': 'network'})
            try:
                return orig_rr(ds, batch_root, rows, expected)
            finally:
                LDD.load_tau_results, LDD.load_webapp = o_load, o_web
        LRB.v13_reread_tau = rr_adapter
        try:
            out = croot / 'release'
            try:
                rep = quiet(env['build13'], out_dir=str(out), handover_dir=handover, batch_root=batch, date=DATE, codex_verdict=str(verdict))
                err = ''
            except Exception as e:                                        # noqa: BLE001
                rep, err = None, f'{type(e).__name__}: {e}'
            if hold:
                chk(f'C1 {name} ★ 실제 빌드 (dry_run False · diagnostic False) → 거부 · 주 타깃 HOLD · 산출 폴더 없음 '
                    f'(옛: L1 · L2 는 27 파일 · 경고 0) — {err[:160] or "만들었다"}',
                    rep is None and 'ReleaseError' in err and '주 타깃 모형 한계' in err and 'HOLD' in err and not out.exists())
                outd = croot / 'release_diag'
                try:
                    repd = quiet(env['build13'], out_dir=str(outd), handover_dir=handover, batch_root=batch, date=DATE,
                                 codex_verdict=str(verdict), diagnostic=True)
                    errd = ''
                except Exception as e:                                    # noqa: BLE001
                    repd, errd = None, f'{type(e).__name__}: {e}'
                wd = (repd or {}).get('warnings') or []
                chk(f'C2 {name} 진단 빌드 (NOT FOR RELEASE) — 만들되 경고에 주 타깃 HOLD ({errd[:120] or len(wd)})',
                    repd is not None and any('주 타깃' in w and 'HOLD' in w and cid in w for w in wd))
                if repd is not None:
                    pc = LRB.check_v13(str(outd), handover)
                    chk(f'C3 {name} ★ 배포 대조 (check_v13 · 배포 모드) → 주 타깃 HOLD 문제 (옛: L1 · L2 는 진단 표지 차이만) {[p[:90] for p in pc][:3]}',
                        any('HOLD' in p and cid in p for p in pc))
                    sm = json.load(open(outd / 'lhs_v13_refit_porosity_sigma_cn_summary.json', encoding='utf-8'))
                    want_ex = 'NOT_COMPUTED:full_over_conduction' if name == 'L0_h0' else 'BAND_FALLBACK:full_over_conduction'
                    chk(f"C4 {name} 재적합 제외 사유 — 모형 한계 원인이 따로 남는다 (앞 상태가 덮어도 · Codex §6-10) {sm.get('excluded')}",
                        (sm.get('excluded') or {}).get(want_ex, 0) >= 1)
                else:
                    chk(f'C3 {name} 배포 대조 (진단 빌드 실패로 건너뜀)', False, errd)
                    chk(f'C4 {name} 재적합 제외 사유 (진단 빌드 실패로 건너뜀)', False, errd)
            else:
                pc = LRB.check_v13(str(out), handover) if rep is not None else ['(빌드 실패)']
                chk(f'C1 {name} 실제 빌드 → 만들고 check_v13 문제 0 (띠 폴백만 · Physics · H12 모형 한계는 배포 HOLD 아님 — 정책 그대로) '
                    f'{(err or str(pc))[:200]}', rep is not None and pc == [])
                if rep is not None:
                    mh, mr = env['_read_csv'](str(out / f'lhs_release_{DATE}_v13.csv'))
                    ph, pr = env['_read_csv'](str(out / f'lhs_release_{DATE}_v13_physics.csv'))
                    sel = next((r for r in pr if r.get('case_id') == cid), {})
                    want_p = 'True' if 'physics' in BEDS[name][1] else 'False'
                    chk(f"C2 {name} ★ 배포 표지 열 — 주 표 full_model_limit_hertz (전 행 False) · Physics 부록 full_model_limit_physics (선택 행 {want_p} · "
                        f"상태 칸 BAND_FALLBACK 그대로) ({sel.get(FLAG['physics'], 'ABSENT')!r} · {sel.get('ion_net_status_physics')!r})",
                        FLAG['hertz'] in mh and all(r[FLAG['hertz']] == 'False' for r in mr) and FLAG['physics'] in ph
                        and sel.get(FLAG['physics']) == want_p and sel.get('ion_net_status_physics') == 'BAND_FALLBACK')
                    if want_p == 'True':
                        rd = (out / 'README.md').read_text(encoding='utf-8')
                        chk(f'C3 {name} README 집계 — 띠 폴백에 가려진 Physics 모형 한계가 Physics 상태 셈 · 문단에 따로 (full_model_limit_physics · 빠지지 않는다)',
                            f'{FLAG["physics"]}' in rd and any(ML in ln and 'BAND_FALLBACK' in ln and FLAG['physics'] in ln for ln in rd.splitlines()))
        finally:
            LRB.v13_reread_tau = orig_rr


def main():
    tmp, state = [], {}
    try:
        _guard('D', sec_D)
        _guard('A', lambda: sec_A(state))
        _guard('B', lambda: sec_B(state, tmp))
        _guard('C', lambda: sec_C(state, tmp))
    finally:
        for d in tmp:
            shutil.rmtree(d, ignore_errors=True)
    print(f'\ntest_l214r02_model_limit_flag: {_ok}/{_ok + len(_fail)} PASS' + (f'   FAILED: {_fail}' if _fail else ''))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
