#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L214R-09 · 10 · 11 — 같은 부류 셋 (τ 출력의 유한성 · 온도 규약 재계산의 유한성 · 정지 계약 수 판정의 큰 JSON 정수) 반례 (상주 시험).

  python3 scripts/test_l214r09_same_class.py          # 종료코드 0 = 전부 PASS

근거 = L214R-06 · 07 · 08 수정 중 보고된 같은 부류 N1 · N2 · N3 (L214R-01 A · 05 · 07 · 08 의 규칙 — 비교 · 게시 **전에** 유한성 · 넘침 · 밑넘침 = 기술 실패 사유
(생산자 `network_conductivity.NON_FINITE_REASON` 꼬리표) · float 로 못 옮기는 큰 정수 = 유한 실수가 아니다 · 예외 아님 — 를 남은 자리로).  선행 시험
(`scripts/test_l214r06_same_class.py` · `test_l214r05_published_certificate.py` · `test_l214r01_certificate.py`) 은 고치지 않는다 (그대로 통과해야 한다).

★ 시험 먼저 — 고치기 전 코드에서 반례 묶음이 빨갛다:
  A  L214R-09 (N1) — τ 행 (`tau_flux.ion_columns` · 폴더 `case_row`) 이 게시하는 f · tau2 · tau 의 유한 양수를 보지 않는다 (값 상태 OK · MBCB 를 주기 전):
     (a) 진짜 194 v1.2 역사 레코드 (lhs00_000 · inferred_legacy · 증서 없음) 의 σ_ratio 1e−310 · σ_dim 1e−7 — 두 표현 항등식은 절대 반폭 5e−7 안이라 0b 통과 →
         f 9.6e−311 (밑정규) · tau2 = φ_mc/f = +∞ · 상태 OK (σ_ratio 5e−324 도 같다)
     (b) 장부 극값 — L_gap 1e308 + L_mc 1e−10 · L_mc 1e−310 → f = +∞ · tau2 = tau = 0 · 상태 MBCB / φ_mc 1e308 → H0 tau2 = +∞ · OK / L_gap 5e−324 → f 가 0 으로
         밑넘쳐 tau2 = φ_mc/0 = ZeroDivisionError (τ 행 · 폴더 행 · 다시 읽기 실행이 예외로 죽는다).  세대 2 레코드도 같다 (증서는 장부를 묶지 않는다) — 실제 웹
         게시 경로 (`app._network_and_stage_e` · 실 생산자 CLI) 로 만든 폴더에서 정지 계약 · 다시 읽기 K1–K7 · 인계 관문 H1 (P0–P4) 이 전부 받아들였다.
     ⚠ 각 값 **하나만** (L_gap 1e308 · L_mc 1e−10) 으로는 이 침대들에서 f · tau2 가 유한 양수다 (A0 — 둘이 함께일 때 넘친다) — 유한한 극값은 규칙 밖 (새 문턱 없음).
  B  L214R-10 (N2) — 온도 규약 대조 (`tau_flux.sigma0_convention_problem`) 가 다시 계산한 σ_grain · 배수의 유한성을 비교 전에 안 본다: T_C −272.15 · Ea −0.0613 eV →
     (T_ref/T)·exp(…) 가 예외 없이 +∞ → |σ₀ − ∞| ≤ 1e−12·∞ 가 참 → **어떤 σ₀ 든** None.  소비자 (σ₀ 결합 · 증서 결합 · 세대 계약 · τ 행 · 정지 계약 ⑧ ⑨ ·
     기록 판정 · 다시 읽기 K2 · K4) 가 전부 받아들였다.
  C  L214R-11 (N3) — 정지 계약 수 판정 (`pipeline_service._stop_num`) 이 JSON 정수 10⁴⁰⁰ 에 OverflowError (`math.isfinite`) → `network_stop_verdict` 전체가 예외 ·
     다시 읽기 K4 · 인계 P4 는 잡지만 사유 대신 예외 문구.  `_stop_num` 이 읽는 칸 전부 — 장부 넷 (L_gap · L_mc · φ_mc · calc_percolation) · full_metrics σ 둘 ·
     협착 전력 몫 둘 (full_metrics + 레코드 사본) · 띠 폭 둘 (레코드 사본) · 비관통 (valid_zero) · 모형 한계 가지의 calc_percolation.
  H  대조 (그대로여야): 실 생산자 정상 세대 2 레코드 (상자 1.5 · 2.0 · 1.0 모형 한계 · 비관통 — 세 모드 τ = 독립 식 φ_mc/(σ_ratio·L_gap/L_mc)) · 정직한 풀이
     실패 (solver_guard) · 진짜 194 v1.2 역사 레코드 폴더 행 전부 (고치기 전 코드에서 잰 지문 = 비트 같음 · 독립 식) · 실제 웹 게시 폴더 다섯 (관통 · 비관통 ·
     모형 한계 · 띠 L1 · 60 °C Arrhenius) 의 정지 계약 · 기록 판정 · 다시 읽기 · 폴더 행 · 생산자 온도 규약 (25 °C 상수 · Arrhenius 넷) = None · 유한한 어긋남의
     사유 문구 그대로 · `_stop_num` 의 보통 값 판정 그대로.
소비자 — τ 행 (`ion_columns` · `case_row`) · 정지 계약 (`pipeline_service.network_stop_verdict` ①–⑨) · 기록 판정 (`network_record_verdict`) · 다시 읽기
  (`g2_network_reread.run_smoke_or_dirs` — K1–K7 + H1 = 인계 출처 관문 `lhs_design_dataset.load_tau_results` P0–P4) · 배포 빈칸 규칙
  (`lhs_release_build.v13_blank_problems` · `_v13_class` — NOT_COMPUTED 를 사유 어휘와 무관하게 기술 실패로 분류하는가).
⚠ 범위 — 손상 · 위조 기록을 관문이 거르는가의 계약 시험이다 (합성 사슬 · 진짜 역사 레코드 · 실제 웹 게시 폴더에 합성 변이).  실제 침대 자료에서 난 일이 아니다.
"""
import contextlib
import copy
import hashlib
import io
import json
import math
import os
import shutil
import sys
import tarfile
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
for _p in (HERE, os.path.join(ROOT, 'webapp')):
    if _p not in sys.path:
        sys.path.insert(0, _p)

TAG = 'non_finite'
ML = 'full_over_conduction'
BIG_TXT = '1' + '0' * 400                                        # JSON 정수 10⁴⁰⁰ — float 로 못 옮긴다 (json.loads = int)
#: 진짜 194 v1.2 역사 레코드 폴더 행 (`tau_flux.case_row` 전부 · 케이스 이름순 · json sort_keys) 의 sha256 — **고치기 전 코드** (ad81c82a7) 에서 잰 값.
#:   고친 뒤에도 같아야 한다 (정상 행 비트 같음 · 194 = OK·OK 160 · NOT_PERCOLATING 24 · OK·MBCB 10 · 전부 inferred_legacy).
LEGACY194_ROWS_SHA256 = '739b98b1a9e5a85022a5a602c361623896918cbec2c5a1d0124870f5409f5580'
_ok, _fail = 0, []


def chk(name, cond, extra=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'   {str(extra)[:400]}' if extra else ''))


def _guard(label, fn):
    """묶음 하나가 예외로 죽어도 나머지를 센다 (고치기 전 코드 — 예외 = 그 묶음 FAIL)."""
    try:
        fn()
    except Exception as e:                                       # noqa: BLE001
        chk(f'{label} — 예외 없이 끝난다 ({type(e).__name__}: {e})', False)


def _call(fn, *a, **kw):
    """→ (값, None) | (None, '예외 이름: 내용') — 판정 함수가 사유 대신 예외를 내면 그것도 기록한다 (요구 = 사유)."""
    try:
        return fn(*a, **kw), None
    except Exception as e:                                       # noqa: BLE001
        return None, f'{type(e).__name__}: {e}'


def _big_text(obj):
    """'__L214R09_BIG__' 자리를 JSON 정수 10⁴⁰⁰ 으로 — 디스크 · 다시 읽기와 같은 모양 (json.loads = int)."""
    return json.dumps(obj).replace('"__L214R09_BIG__"', BIG_TXT)


BIG_MARK = '__L214R09_BIG__'


def main():
    import network_conductivity as nc
    import tau_flux as tf
    import pipeline_service as ps
    import se_material as sm
    import lhs_release_build as RB
    import g2_network_reread as GR
    #  실제 생산자 경로 = test_lhs214_model_limit 의 것 · 실제 웹 게시 경로의 침대 · 실 CLI 대역 = test_pipeline_provenance 의 것 · 진짜 역사 레코드 묶음 =
    #  test_gen2_role_contract 의 ARCHIVE (194 v1.2 배치 원천) — 복제하지 않는다 (규율 ①)
    from test_lhs214_model_limit import chain_bed, ledger_of, produce, quiet
    from test_gen2_role_contract import ARCHIVE
    import test_pipeline_provenance as TP
    with contextlib.redirect_stdout(io.StringIO()):
        import app                                               # Flask — 실제 웹 게시 경로 (`_network_and_stage_e`)

    tmp = tempfile.mkdtemp(prefix='l214r09_')
    MODES3 = ('hertz', 'hertz_h12', 'physics')
    SCRIPTS = os.path.join(ROOT, 'scripts')

    def rec_of(d, m):
        return tf.mode_record(d, m)

    def vals(row, m):
        return tuple(row.get(k) for k in (f'f_ion_{m}', f'f_ion_{m}_gap', f'tau2_ion_{m}', f'tau_ion_{m}'))

    def nonfinite_row(row, m):
        """그 모드 = NOT_COMPUTED · 사유 'invalid_input: non_finite …' (기술 실패 · 생산자 꼬리표) · 값 넷 빈칸."""
        return (isinstance(row, dict) and row.get(f'ion_net_status_{m}') == 'NOT_COMPUTED'
                and str(row.get(f'ion_net_status_reason_{m}')).startswith(f'invalid_input: {TAG}') and vals(row, m) == (None, None, None, None))

    def show(row, m):
        if not isinstance(row, dict):
            return row
        return (row.get(f'ion_net_status_{m}'), str(row.get(f'ion_net_status_reason_{m}'))[:70]) + vals(row, m)

    def oracle_ok(row, m, sf, led):
        """독립 식 — f = σ_ratio·L_gap/L_mc · tau2 = φ_mc/f · tau = √tau2 · 셋 다 유한 양수 · 상태 = tau2 < 1 이면 MBCB 아니면 OK."""
        f = sf * led['thickness_um'] / led['thickness_mass_conserving_um']
        t2 = led['phi_se_mass_conserving'] / f
        st = 'MODEL_BELOW_CONTINUUM_BOUND' if t2 < 1.0 else 'OK'
        return (row.get(f'ion_net_status_{m}') == st and vals(row, m) == (f, sf, t2, math.sqrt(t2))
                and all(math.isfinite(v) and v > 0 for v in (f, t2, math.sqrt(t2))))

    def jl(d, n):
        with open(os.path.join(d, n), encoding='utf-8') as fh:
            return json.load(fh)

    def jw(d, n, obj):
        with open(os.path.join(d, n), 'w', encoding='utf-8') as fh:
            fh.write(_big_text(obj))

    def web_bed(bed, **rk):
        """실제 웹 게시 경로 — 실 생산자 CLI (`TP._CLIRunner` — runpy) → `app._network_and_stage_e(stop_before_stage_e=True)` (내용 판정 · 기록 판정 · 정지 계약 ·
        도장 · 승격) → 게시된 케이스 폴더 · 상태 · 이번 실행 run id."""
        d = tempfile.mkdtemp(prefix=f'web_{bed}_', dir=tmp)
        a, c = TP._write_bed(d, bed)
        with open(os.path.join(d, 'full_metrics.json'), 'w') as f:
            json.dump(TP._bed_ledger(bed), f)
        with contextlib.redirect_stdout(io.StringIO()):
            stages, rid = app._network_and_stage_e(d, SCRIPTS, a, c, '1:SE', 1, [], runner=TP._CLIRunner(delegate=TP._fake_stage_e, **rk),
                                                   stop_before_stage_e=True)
        st, _failed = ps.summarize(stages)
        return d, st, rid

    def reread(d):
        """다시 읽기 (K1–K7 + H1 인계 출처 관문) → [(실패한 검사 이름, 세부)] — 실행 예외는 `_call` 이 잡는다 (고치기 전 = 그 자체가 결함)."""
        with contextlib.redirect_stdout(io.StringIO()):
            reps = GR.run_smoke_or_dirs([d], 'g2', out=lambda *a, **k: None)
        return [(c['name'], c['detail']) for c in reps[0]['checks'] if not c['ok']]

    NAMES = ('network_conductivity_dual.json', 'network_conductivity_hertzian.json', 'network_conductivity_physics.json', 'network_conductivity.json',
             'full_metrics.json')

    def snapshot(d):
        return {n: jl(d, n) for n in NAMES}

    def restore(d, snap):
        for n, o in snap.items():
            with open(os.path.join(d, n), 'w', encoding='utf-8') as fh:
                json.dump(o, fh)

    def mutate_copies(d, snap, h=None, p=None, fm=None):
        """폴더의 모든 사본을 한꺼번에 바꾼다 — h(레코드) = Hertz 레코드 (dual hertzian · 모드 파일 · legacy) · p(레코드) = physics (dual · 모드 파일) ·
        fm(dict) = full_metrics.  BIG_MARK 자리는 디스크에서 JSON 정수 10⁴⁰⁰."""
        for n, o in snap.items():
            o = copy.deepcopy(o)
            if n == 'network_conductivity_dual.json':
                if h:
                    h(o['hertzian'])
                if p:
                    p(o['physics'])
            elif n in ('network_conductivity_hertzian.json', 'network_conductivity.json'):
                if h:
                    h(o)
            elif n == 'network_conductivity_physics.json':
                if p:
                    p(o)
            elif n == 'full_metrics.json' and fm:
                fm(o)
            jw(d, n, o)

    def release_row(row):
        """배포 빈칸 규칙이 읽는 꼴 — 인계 칸 (`tau_flux._cell`) + case_id."""
        return dict({k: tf._cell(v) for k, v in row.items() if k != 'case'}, case_id=row.get('case', 'x'))

    REL_COLS = [f'{p}_{m}' for m in ('hertz', 'physics', 'hertz_h12') for p in ('f_ion', 'tau2_ion', 'tau_ion', 'ion_net_status_reason')]

    try:
        # ── 실 생산자 세대 2 침대 (test_l214r06 과 같은 침대) ─────────────────────────────────────────────────────────────────────
        B15 = chain_bed(1.5)
        L15 = ledger_of(B15)
        d15 = produce(nc, B15)
        B20 = chain_bed(2.0, area=3.2)
        L20 = ledger_of(B20)
        d20 = produce(nc, B20)
        B10 = chain_bed(1.0)
        L10 = ledger_of(B10)
        d10 = produce(nc, B10)
        _A, _C, _P, _X = chain_bed(1.5)
        Bnp = (_A, [c for c in _C if c['id1'] != 10], _P, _X)
        Lnp = ledger_of(Bnp)
        dnp = produce(nc, Bnp)

        # ══ H — 대조 (그대로여야) ════════════════════════════════════════════════════════════════════════════════════
        def sH():
            for lab, d, led in (('상자 1.5', d15, L15), ('상자 2.0 면적 3.2', d20, L20)):
                row = tf.ion_columns(d, led, 100.0)
                chk(f'H1 정상 세대 2 레코드 ({lab}) τ 세 모드 = 독립 식 φ_mc/(σ_ratio·L_gap/L_mc) · 유한 양수 · 상태 그대로 '
                    f'{[show(row, m)[:3] for m in MODES3]}',
                    all(oracle_ok(row, m, rec_of(d, m)['sigma_full'], led) for m in MODES3) and row.get(tf.ROW_GENERATION_COL) == 'g2')
            row = tf.ion_columns(d10, L10, 100.0)
            chk(f"H2 FULL 모형 한계 (상자 1.0 · physics) = NOT_COMPUTED full_over_conduction · 값 빈칸 · H0 · H12 = 독립 식 {[show(row, m)[:3] for m in MODES3]}",
                tf.is_model_limit_status(row.get('ion_net_status_physics'), row.get('ion_net_status_reason_physics'))
                and vals(row, 'physics') == (None, None, None, None)
                and all(oracle_ok(row, m, rec_of(d10, m)['sigma_full'], L10) for m in ('hertz', 'hertz_h12')))
            row = tf.ion_columns(dnp, Lnp, 0.0)
            chk(f'H3 정직한 비관통 (valid_zero) = NOT_PERCOLATING · f = f_gap = 0.0 · tau2 · tau 빈칸 (등록된 물리적 ∞ 표현) {[show(row, m) for m in MODES3]}',
                all(row.get(f'ion_net_status_{m}') == 'NOT_PERCOLATING' and vals(row, m) == (0.0, 0.0, None, None) for m in MODES3))
            #  정직한 풀이 실패 — 실제 생산자 사다리의 모든 단 실패 (spsolve 틀린 해 · cg · gmres 미수렴 주입) → solver_guard
            import numpy as np
            old = {k: getattr(nc, k) for k in ('spsolve', 'cg', 'gmres')}
            nc.spsolve = lambda A_, b_: np.zeros(len(b_))
            nc.cg = lambda A_, b_, **k_: (np.zeros(len(b_)), 1)
            nc.gmres = lambda A_, b_, **k_: (np.zeros(len(b_)), 1)
            try:
                dfail = produce(nc, B15)
            finally:
                for k, v in old.items():
                    setattr(nc, k, v)
            row = tf.ion_columns(dfail, L15, 100.0)
            chk(f"H4 정직한 풀이 실패 (모든 단 실패) = NOT_COMPUTED solver_guard · 값 빈칸 {show(row, 'hertz')}",
                (row.get('ion_net_status_hertz'), row.get('ion_net_status_reason_hertz')) == ('NOT_COMPUTED', 'solver_guard')
                and vals(row, 'hertz') == (None, None, None, None))
            #  _stop_num 의 보통 값 — 유한 실수만 참 (bool · 문자열 · None · NaN · ±∞ · numpy 아닌 꼴 = 거짓)
            table = ((1.0, True), (0, True), (-3, True), (2 ** 53, True), (1e308, True), (5e-324, True), (True, False), (False, False), ('1', False),
                     (None, False), (float('nan'), False), (float('inf'), False), (-float('inf'), False), ([1], False))
            got = [(v, _call(ps._stop_num, v)) for v, _w in table]
            chk(f'H5 정지 계약 수 판정 (_stop_num) 의 보통 값 그대로 {[(v, g) for v, (g, e) in got][:6]} …',
                all(e is None and g is w for (v, (g, e)), (_v, w) in zip(got, table)), got)

        _guard('H', sH)

        # ══ H — 진짜 194 v1.2 역사 레코드 (폴더 행 전부 · 비트 같음) ══════════════════════════════════════════════════════════════
        legacy_root = os.path.join(tmp, 'legacy194')

        def sHL():
            with tarfile.open(ARCHIVE) as t:
                for mem in t.getmembers():
                    parts = mem.name.split('/')
                    if mem.isfile() and len(parts) > 2 and parts[-1] in ('network_conductivity_dual.json', 'full_metrics.json', 'network_provenance.json'):
                        cd = os.path.join(legacy_root, parts[1])
                        os.makedirs(cd, exist_ok=True)
                        with t.extractfile(mem) as fh, open(os.path.join(cd, parts[-1]), 'wb') as out:
                            out.write(fh.read())
            cases = sorted(os.listdir(legacy_root))
            rows = [tf.case_row(os.path.join(legacy_root, c)) for c in cases]
            sha = hashlib.sha256(json.dumps(rows, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()
            chk(f'H6 ★ 진짜 194 역사 레코드 폴더 행 전부 = 고치기 전 코드의 지문 그대로 (비트 같음) — {len(rows)} 행 · {sha[:16]}…',
                len(rows) == 194 and sha == LEGACY194_ROWS_SHA256, sha)
            bad, n_val, n_np = [], 0, 0
            for c, row in zip(cases, rows):
                dual = jl(os.path.join(legacy_root, c), 'network_conductivity_dual.json')
                fm = jl(os.path.join(legacy_root, c), 'full_metrics.json')
                for m in ('hertz', 'physics'):
                    st = row.get(f'ion_net_status_{m}')
                    if st in ('OK', 'MODEL_BELOW_CONTINUUM_BOUND'):
                        n_val += 1
                        if not oracle_ok(row, m, rec_of(dual, m)['sigma_full'], fm):
                            bad.append((c, m))
                    elif st == 'NOT_PERCOLATING':
                        n_np += 1
                        if vals(row, m) != (0.0, 0.0, None, None):
                            bad.append((c, m))
                    else:
                        bad.append((c, m, st))
            chk(f'H7 194 역사 레코드 τ = 독립 식 (값 상태 {n_val} 칸) · 비관통 {n_np} 칸 = f 0.0 · tau2 빈칸 · 그 밖 상태 없음 — 어긋남 {bad[:4]}',
                not bad and n_val == 340 and n_np == 48)

        _guard('H legacy', sHL)

        # ══ H — 실제 웹 게시 폴더 다섯 (정지 계약 · 기록 판정 · 다시 읽기 · 폴더 행 그대로) ══════════════════════════════════════════
        web = {}

        def sHW():
            want = {'through': ('OK', 'OK', 'OK'), 'nonthrough': ('NOT_PERCOLATING',) * 3, 'ml_physics': ('OK', 'OK', 'NOT_COMPUTED'),
                    'band_l1': ('BAND_FALLBACK',) * 3, 'through_60C': ('OK', 'OK', 'OK')}
            for lab in want:
                bed, rk = ('through', dict(extra_argv=['--temp-c', '60'])) if lab == 'through_60C' else (lab, {})
                d, st, rid = web_bed(bed, **rk)
                web[lab] = (d, rid)
                sv, e1 = _call(ps.network_stop_verdict, d, rid)
                rv, e2 = _call(ps.network_record_verdict, d)
                rr, e3 = _call(reread, d)
                row = tf.case_row(d)
                sts = tuple(row.get(f'ion_net_status_{m}') for m in MODES3)
                chk(f'H8 웹 게시 폴더 [{lab}] = done · 정지 계약 (True, ok) · 기록 판정 통과 · 다시 읽기 실패 0 · τ 상태 {sts}',
                    st == 'done' and sv == (True, 'ok') and not e1 and not e2 and rv[0] is True and not e3 and rr == [] and sts == want[lab],
                    (st, sv, e1, rv, e2, e3, rr))
            r60 = jl(web['through_60C'][0], 'network_conductivity_dual.json')['hertzian']
            chk(f"H9 생산자 온도 규약 (60 °C Arrhenius · 웹 게시) — σ₀ {r60.get('sigma_grain_S_cm')!r} · 규약 대조 None",
                r60['temperature_provenance'].get('T_C') == 60.0 and tf.sigma0_convention_problem(r60) is None)

        _guard('H web', sHW)

        # ══ H — 온도 규약 대조의 정상 · 유한 어긋남 (그대로) ═════════════════════════════════════════════════════════════════════
        def sHT():
            A, C, plate, box = B15
            for tc, ea in ((None, None), (60.0, None), (60.0, 0.29), (-20.0, 0.46), (25.0, None)):
                rr = json.loads(json.dumps(quiet(nc._run_all_networks, A, C, [1], [], {1: 'SE'}, 1, plate, box, box, None, contact_mode='hertzian',
                                                 temp_c=tc, ea_ion_ev=ea)))
                p1, e1 = _call(tf.sigma0_convention_problem, rr)
                p2, e2 = _call(tf.sigma0_convention_problem, rr['hertz_h12'])
                chk(f"H10 생산자 온도 규약 (T_C {tc} · Ea {ea}) — σ₀ {rr['sigma_grain_S_cm']!r} · 배수 {rr['temperature_provenance']['sigma_ion_T_factor']!r} · "
                    f"H0 · H12 규약 대조 None", (p1, e1, p2, e2) == (None, None, None, None), (p1, e1, p2, e2))
            r = copy.deepcopy(d15['hertzian'])
            r['sigma_grain_S_cm'] = 0.006
            want = 'σ₀ ↔ 온도 규약 (G2RR2-04): σ₀ 0.006 S/cm ≠ 온도 규약 (T_C None · Ea None · T_ref 25.0) 의 σ_grain 0.003'
            got = tf.sigma0_convention_problem(r)
            chk(f'H11 유한 어긋남 (25 °C · σ₀ ×2) 의 사유 문구 그대로 — {got!r:.120}', got == want)
            r = copy.deepcopy(d15['hertzian'])
            r['temperature_provenance'] = dict(r['temperature_provenance'], T_C=-272.15, Ea_ion_eV=-0.07, T_dependence='ARRHENIUS')
            got = tf.sigma0_convention_problem(r)
            chk(f'H12 exp 자체가 넘치는 규약 (T_C −272.15 · Ea −0.07) = 기존 사유 그대로 (재계산 불가 · OverflowError 를 사유로) — {got!r:.120}',
                got == '온도 규약을 다시 계산할 수 없다 (OverflowError: math range error)')
            r = copy.deepcopy(d15['hertzian'])
            r['temperature_provenance'] = dict(r['temperature_provenance'], T_C=-272.15, Ea_ion_eV=0.07, T_dependence='ARRHENIUS')
            got, e = _call(tf.sigma0_convention_problem, r)
            chk(f'H13 배수가 0 으로 밑넘치는 규약 (T_C −272.15 · Ea +0.07) = 거부 (사유 · None 아님 · 예외 아님 — 고치기 전에도 거부) — {got!r:.120}',
                e is None and isinstance(got, str) and bool(got))

        _guard('H temp', sHT)

        # ══ A — L214R-09 (N1) τ 출력의 유한성 ═══════════════════════════════════════════════════════════════════════════════════
        def sA():
            for lab, led in (('L_gap 1e308 만', dict(L15, thickness_um=1e308)), ('L_mc 1e−10 만', dict(L15, thickness_mass_conserving_um=1e-10))):
                row, e = _call(tf.ion_columns, d15, led, 100.0)
                chk(f'A0 전제 [{lab}] — 유한한 극값 하나만으로는 f · tau2 · tau 가 유한 양수 · 값 상태 그대로 (새 범위 문턱 없음) {[show(row, m)[:4] for m in MODES3] if row else e}',
                    e is None and all(oracle_ok(row, m, rec_of(d15, m)['sigma_full'], led) for m in MODES3))
            cases = (('A1 L_gap 1e308 + L_mc 1e−10 (f = +∞ · tau2 = 0)', dict(L15, thickness_um=1e308, thickness_mass_conserving_um=1e-10), MODES3),
                     ('A2 L_mc 1e−310 (f = +∞ · tau2 = 0)', dict(L15, thickness_mass_conserving_um=1e-310), MODES3),
                     ('A3 L_gap 5e−324 (f 가 0 으로 밑넘침 — 고치기 전 ZeroDivisionError)', dict(L15, thickness_um=5e-324), MODES3),
                     ('A4 φ_mc 1e308 (H0 tau2 = +∞)', dict(L15, phi_se_mass_conserving=1e308), ('hertz',)))
            for lab, led, bad_modes in cases:
                row, e = _call(tf.ion_columns, d15, led, 100.0)
                chk(f'{lab} ★ 세대 2 실 생산자 레코드 τ 행 — {bad_modes} = NOT_COMPUTED invalid_input: {TAG} … · 값 빈칸 · 예외 아님 — '
                    f'{[show(row, m) for m in bad_modes] if row else e}', e is None and all(nonfinite_row(row, m) for m in bad_modes))
                if row and bad_modes == ('hertz',):
                    chk(f'{lab} · physics · H12 (유한) = 독립 식 그대로', all(oracle_ok(row, m, rec_of(d15, m)['sigma_full'], led) for m in ('physics', 'hertz_h12')))

        _guard('A', sA)

        # ══ A — 진짜 역사 레코드 (lhs00_000 · inferred_legacy) 폴더 행 ═════════════════════════════════════════════════════════════════
        def sAL():
            cd = os.path.join(legacy_root, 'lhs00_000')
            dp, fp = os.path.join(cd, 'network_conductivity_dual.json'), os.path.join(cd, 'full_metrics.json')
            dual0, fm0 = jl(cd, 'network_conductivity_dual.json'), jl(cd, 'full_metrics.json')
            row0 = tf.case_row(cd)
            chk(f"AL0 전제 — lhs00_000 = inferred_legacy · 증서 없음 · H0 OK (tau2 {row0.get('tau2_ion_hertz')!r}) · physics OK",
                row0.get('ion_net_generation') == 'inferred_legacy' and not any(k.startswith('solve_certificate') for k in dual0['hertzian'])
                and row0.get('ion_net_status_hertz') == 'OK' and row0.get('ion_net_status_physics') == 'OK')

            def run(dual=None, fm=None):
                with open(dp, 'w', encoding='utf-8') as fh:
                    json.dump(dual if dual is not None else dual0, fh)
                with open(fp, 'w', encoding='utf-8') as fh:
                    json.dump(fm if fm is not None else fm0, fh)
                return _call(tf.case_row, cd)

            for lab, q, sd in (('AL1 σ_ratio 1e−310 · σ_dim 1e−7 (Codex 모양 — 0b 통과 · 고치기 전 OK tau2 = +∞)', 1e-310, 1e-7),
                               ('AL2 σ_ratio 5e−324 · σ_dim 1e−7', 5e-324, 1e-7)):
                d = copy.deepcopy(dual0)
                d['hertzian'].update(sigma_full=q, sigma_full_mScm=sd)
                irp = tf.ion_record_problem(d['hertzian'])
                row, e = run(dual=d)
                chk(f"{lab} ★ 폴더 행 H0 = NOT_COMPUTED invalid_input: {TAG} … · 값 빈칸 · physics OK 그대로 — {show(row, 'hertz') if row else e} · 0b {irp!r:.40}",
                    e is None and nonfinite_row(row, 'hertz') and row.get('ion_net_status_physics') == 'OK'
                    and row.get('tau2_ion_physics') == row0.get('tau2_ion_physics'))
                o, e = _call(tf.ion_columns, d, fm0, fm0.get('percolation_pct'))
                chk(f'{lab} ★ τ 행 (ion_columns · 같은 입력) 도 같다', e is None and nonfinite_row(o, 'hertz') and o.get('ion_net_status_physics') == 'OK', e)
                if q == 1e-310 and row:
                    rr = release_row(row)
                    bp, e1 = _call(RB.v13_blank_problems, [rr], REL_COLS)
                    cl, e2 = _call(RB._v13_class, rr)
                    chk(f'{lab} ★ 배포 빈칸 규칙 — 값 칸 빈칸 = NOT_COMPUTED (사유 어휘 무관 · 새 코드 없음) · 문제 0 · 관통 분류 = ("", NOT_COMPUTED) — {bp or e1} · {cl or e2}',
                        e1 is None and bp == [] and e2 is None and cl == ('', 'NOT_COMPUTED')
                        and RB.v13_blank_reason(rr, 'tau2_ion_hertz') == 'NOT_COMPUTED')
            for lab, upd in (('AL3 장부 L_gap 1e308 + L_mc 1e−10', dict(thickness_um=1e308, thickness_mass_conserving_um=1e-10)),
                             ('AL4 장부 L_gap 5e−324 (고치기 전 ZeroDivisionError)', dict(thickness_um=5e-324))):
                row, e = run(fm=dict(fm0, **upd))
                chk(f"{lab} ★ 폴더 행 두 모드 = NOT_COMPUTED invalid_input: {TAG} … · 값 빈칸 · 예외 아님 — {[show(row, m) for m in ('hertz', 'physics')] if row else e}",
                    e is None and all(nonfinite_row(row, m) for m in ('hertz', 'physics')))
            row, e = run()
            chk('AL5 되돌린 역사 레코드 = 처음 행 그대로', e is None and row == row0)

        _guard('A legacy', sAL)

        # ══ A — 실제 웹 게시 폴더 (세대 2) 의 장부 극값 — 정지 계약 · 다시 읽기 · 인계 관문 ═══════════════════════════════════════════════
        def sAW():
            if 'through' not in web:
                chk('AW 웹 게시 폴더 (H8 이 만든다) 없음', False)
                return
            d, rid = web['through']
            snap = snapshot(d)
            for lab, upd in (('AW1 L_gap 1e308 + L_mc 1e−10', dict(thickness_um=1e308, thickness_mass_conserving_um=1e-10)),
                             ('AW2 L_mc 1e−310', dict(thickness_mass_conserving_um=1e-310)),
                             ('AW3 φ_mc 1e308 (H0 tau2 = +∞)', dict(phi_se_mass_conserving=1e308)),
                             ('AW4 L_gap 5e−324 (고치기 전 ZeroDivisionError)', dict(thickness_um=5e-324))):
                mutate_copies(d, snap, fm=lambda o, u=upd: o.update(u))
                sv, e = _call(ps.network_stop_verdict, d, rid)
                chk(f'{lab} ★ 정지 계약 = 거부 · 사유 ⑦ τ 인계 … {TAG} (예외 · 예외 문구 아님) — {e or str(sv)[:200]}',
                    e is None and sv[0] is False and '⑦ τ 인계 hertz: NOT_COMPUTED' in sv[1] and TAG in sv[1] and 'Error' not in sv[1])
                row, e = _call(tf.case_row, d)
                modes = ('hertz',) if 'φ_mc' in lab else MODES3
                chk(f'{lab} ★ 폴더 행 {modes} = NOT_COMPUTED invalid_input: {TAG} … · 값 빈칸 — {[show(row, m) for m in modes] if row else e}',
                    e is None and all(nonfinite_row(row, m) for m in modes))
                rr, e = _call(reread, d)
                names = sorted({n.split(' ')[0] for n, _x in (rr or [])})
                chk(f'{lab} ★ 다시 읽기 = 거부 (예외 없이 · K4 정지 계약 · K6 관통 일치 · H1 인계 출처 관문 P4 실패) — {e or names}',
                    e is None and {'K4', 'K6', 'H1'} <= set(names) and not any('Error' in str(x) for _n, x in rr))
                if row and lab.startswith('AW1'):
                    rrow = release_row(row)
                    bp, e1 = _call(RB.v13_blank_problems, [rrow], REL_COLS)
                    chk(f'{lab} ★ 배포 빈칸 규칙 — 세 모드 값 칸 = NOT_COMPUTED · 문제 0 (고치기 전: MBCB 인데 f = inf 문제) — {bp or e1}', e1 is None and bp == [])
            restore(d, snap)
            chk('AW5 되돌린 웹 게시 폴더 = 정지 계약 (True, ok)', ps.network_stop_verdict(d, rid) == (True, 'ok'))

        _guard('A web', sAW)

        # ══ B — L214R-10 (N2) 온도 규약 재계산의 유한성 ═════════════════════════════════════════════════════════════════════════
        def mut_prov(rec, **kw):
            if isinstance(rec, dict) and isinstance(rec.get('temperature_provenance'), dict):
                rec['temperature_provenance'] = dict(rec['temperature_provenance'], **kw)
            if isinstance(rec, dict) and isinstance(rec.get('hertz_h12'), dict):
                mut_prov(rec['hertz_h12'], **kw)

        N2 = dict(T_C=-272.15, Ea_ion_eV=-0.0613, T_dependence='ARRHENIUS')

        def sB():
            fac, e = _call(sm.arrhenius_sigma_factor, -272.15, -0.0613, 25.0)
            want, e2 = _call(sm.sigma_grain_S_cm, -272.15, -0.0613, 25.0)
            chk(f'B0 전제 — 규약 배수 (T_C −272.15 · Ea −0.0613) = {fac!r} · σ_grain = {want!r} (예외 없이 +∞ — (T_ref/T)·exp(…) 넘침)',
                e is None and e2 is None and fac == math.inf and want == math.inf)
            for lab, s0 in (('B1 σ₀ 그대로 (3e−3)', None), ('B2 σ₀ 123.0 (아무 값)', 123.0)):
                r = copy.deepcopy(d15['hertzian'])
                mut_prov(r, **N2)
                if s0 is not None:
                    r['sigma_grain_S_cm'] = s0
                p, e = _call(tf.sigma0_convention_problem, r)
                chk(f'{lab} ★ 규약 대조 = 사유 {TAG} … (None · 예외 아님) — {e or p!r:.160}', e is None and isinstance(p, str) and p.startswith(TAG))
            d = copy.deepcopy(d15)
            for m in ('hertzian', 'physics'):
                mut_prov(d[m], **N2)
            r = d['hertzian']
            sb, e = _call(tf.sigma0_binding_problems, r)
            chk(f'B3 ★ σ₀ 결합 (sigma0_binding_problems) = [{TAG} …] — {e or sb!r:.160}', e is None and any(str(x).startswith(TAG) for x in (sb or [])))
            for m in MODES3:
                cb, e = _call(tf.certificate_binding_problems, m, rec_of(d, m))
                chk(f'B4 ★ 증서 결합 ({m}) 에 규약 사유 {TAG} … — {e or cb!r:.140}', e is None and any(TAG in str(x) for x in (cb or [])))
            con, e = _call(tf.network_generation_contract, d)
            chk(f"B5 ★ 세대 계약 = invalid (cert 문제) — {e or (con or {}).get('generation')!r}",
                e is None and con.get('generation') == tf.NET_GEN_BAD and any(k == 'cert' and TAG in det for _m, k, det in con.get('problems', [])))
            row, e = _call(tf.ion_columns, d, L15, 100.0)
            chk(f'B6 ★ τ 행 세 모드 = NOT_COMPUTED invalid_input (세대 계약) · 값 빈칸 — {[show(row, m)[:2] for m in MODES3] if row else e}',
                e is None and all(row.get(f'ion_net_status_{m}') == 'NOT_COMPUTED' and str(row.get(f'ion_net_status_reason_{m}')).startswith('invalid_input')
                                  and vals(row, m) == (None, None, None, None) for m in MODES3))
            if 'through' not in web:
                chk('B7 웹 게시 폴더 (H8 이 만든다) 없음', False)
                return
            wd, rid = web['through']
            snap = snapshot(wd)
            mutate_copies(wd, snap, h=lambda o: mut_prov(o, **N2), p=lambda o: mut_prov(o, **N2),
                          fm=lambda o: o.update(temperature_provenance=dict(o['temperature_provenance'], **N2)))
            sv, e = _call(ps.network_stop_verdict, wd, rid)
            chk(f'B7 ★ 정지 계약 (모든 사본의 온도 규약을 같이 바꿈) = 거부 · ⑧ σ₀ 결합 사유 {TAG} … — {e or str(sv)[:220]}',
                e is None and sv[0] is False and '⑧ σ₀ 결합' in sv[1] and TAG in sv[1])
            s0p, e = _call(ps.network_sigma0_problem, jl(wd, 'network_conductivity_dual.json'), jl(wd, 'network_conductivity.json'), jl(wd, 'full_metrics.json'))
            chk(f'B8 ★ 정지 계약 ⑧ (network_sigma0_problem) = 사유 {TAG} … (빈 문자열 아님) — {e or s0p!r:.160}', e is None and TAG in str(s0p))
            rv, e = _call(ps.network_record_verdict, wd)
            chk(f'B9 ★ 기록 판정 (승격 전) = 거부 (세대 계약) — {e or str(rv)[:160]}', e is None and rv[0] is False and TAG in rv[1])
            rr, e = _call(reread, wd)
            names = sorted({n.split(' ')[0] for n, _x in (rr or [])})
            chk(f'B10 ★ 다시 읽기 = 거부 (K2 세대 계약 · K4 정지 계약) — {e or names}', e is None and {'K2', 'K4'} <= set(names))
            restore(wd, snap)
            chk('B11 되돌린 웹 게시 폴더 = 정지 계약 (True, ok)', ps.network_stop_verdict(wd, rid) == (True, 'ok'))

        _guard('B', sB)

        # ══ C — L214R-11 (N3) 정지 계약 수 판정의 큰 JSON 정수 ═══════════════════════════════════════════════════════════════════
        def sC():
            v, e = _call(ps._stop_num, 10 ** 400)
            chk(f'C0 ★ _stop_num(10⁴⁰⁰) = False (유한 실수가 아니다 · OverflowError 아님) — {e or v!r}', e is None and v is False)
            if not all(k in web for k in ('through', 'nonthrough', 'ml_physics')):
                chk('C 웹 게시 폴더 (H8 이 만든다) 없음', False)
                return

            def put(key):
                return lambda o: o.__setitem__(key, BIG_MARK)

            cases = [(f'C1 장부 {k}', 'through', dict(fm=put(k)), '⑦ τ 인계 장부')
                     for k in ('thickness_um', 'thickness_mass_conserving_um', 'phi_se_mass_conserving', 'percolation_pct')]
            cases += [('C2 full_metrics σ (sigma_full_mScm · H0)', 'through', dict(fm=put('sigma_full_mScm')), '③ hertzian: computed 인데 full_metrics sigma_full_mScm'),
                      ('C2 full_metrics σ (sigma_full_mScm_physics)', 'through', dict(fm=put('sigma_full_mScm_physics')),
                       '③ physics: computed 인데 full_metrics sigma_full_mScm_physics'),
                      ('C3 협착 전력 몫 (H0 · full_metrics + 레코드 사본)', 'through',
                       dict(fm=put('constriction_power_share_ion_hertz'), h=put('constriction_power_share_ion_hertz')), '④ constriction_power_share_ion_hertz'),
                      ('C3 협착 전력 몫 (physics · full_metrics + 레코드 사본)', 'through',
                       dict(fm=put('constriction_power_share_ion_physics'), p=put('constriction_power_share_ion_physics')),
                       '④ constriction_power_share_ion_physics'),
                      ('C4 띠 폭 (H0 레코드 사본)', 'through', dict(h=put('boundary_band_frac')), '⑤ hertzian: boundary_rule'),
                      ('C4 띠 폭 (physics 레코드 사본)', 'through', dict(p=put('boundary_band_frac')), '⑤ physics: boundary_rule'),
                      ('C5 비관통 (valid_zero) 의 calc_percolation', 'nonthrough', dict(fm=put('percolation_pct')),
                       '③ hertzian: valid_zero 인데 독립 calc_percolation'),
                      ('C6 FULL 모형 한계 가지 (physics) 의 calc_percolation', 'ml_physics', dict(fm=put('percolation_pct')),
                       '③ physics: FULL 모형 한계 (관통 해) 인데 독립 calc_percolation')]
            for lab, bed, kw, needle in cases:
                d, rid = web[bed]
                snap = snapshot(d)
                mutate_copies(d, snap, **kw)
                sv, e = _call(ps.network_stop_verdict, d, rid)
                chk(f'{lab} = 10⁴⁰⁰ ★ 정지 계약 = 거부 · 사유 "{needle}" (예외 · 예외 문구 아님) — {e or str(sv)[:200]}',
                    e is None and sv[0] is False and needle in sv[1] and 'Error' not in sv[1])
                if lab.startswith(('C1 장부 thickness_um', 'C3 협착 전력 몫 (H0', 'C4 띠 폭 (H0', 'C5')):
                    rr, e = _call(reread, d)
                    det = {n.split(' ')[0]: x for n, x in (rr or [])}
                    chk(f'{lab} = 10⁴⁰⁰ ★ 다시 읽기 K4 (정지 계약) · H1 (인계 P4) = 거부 · 세부가 사유 (OverflowError 문구 아님) — '
                        f'{e or {k: str(det.get(k))[:80] for k in ("K4", "H1")}}',
                        e is None and 'K4' in det and 'H1' in det and 'Overflow' not in det['K4'] and 'Overflow' not in det['H1'])
                rv, e = _call(ps.network_record_verdict, d)
                chk(f'{lab} = 10⁴⁰⁰ · 기록 판정 (이 칸을 읽지 않는다) = 예외 없이 끝난다', e is None and isinstance(rv, tuple), e)
                restore(d, snap)
            chk('C7 되돌린 웹 게시 폴더 셋 = 정지 계약 (True, ok)',
                all(ps.network_stop_verdict(*web[k]) == (True, 'ok') for k in ('through', 'nonthrough', 'ml_physics')))

        _guard('C', sC)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print(f'\ntest_l214r09_same_class: {_ok}/{_ok + len(_fail)} PASS' + (f'   FAILED: {len(_fail)}' if _fail else ''))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
