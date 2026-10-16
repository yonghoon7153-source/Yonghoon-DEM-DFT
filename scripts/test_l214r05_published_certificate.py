#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L214R-05 — 게시 (computed) 가지 수치 증서 결합 (`tau_flux._cert_published_problem` · `_cert_geometry` · `sigma0_binding_problems`) 의 비유한 재구성 반례 (상주 시험).

  python3 scripts/test_l214r05_published_certificate.py          # 종료코드 0 = 전부 PASS

근거 = L214R-01 수정 중 발견 (Codex 재검증 판정 `docs/reviews/codex_review_lhs214_fix_reverify_20261015.md` §2 반례 A 와 같은 `inf <= inf` 부류가 **게시 경로**에도 있다) ·
수정 계획 `docs/reviews/lhs214r_fix_plan_20261016.md` (1저자 10-16 — L214R-01 A 의 유한성 규칙을 게시 증서 경로로 넓힘 · Q3 = 권고대로).
L214R-01 의 모형 한계 경로 시험 = `scripts/test_l214r01_certificate.py` (이 시험은 그 파일을 고치지 않는다 · 그 시험은 그대로 통과해야 한다).

★ 시험 먼저 — 고치기 전 코드에서 반례 묶음이 빨갛다:
  · 게시 증서 재구성 q = (I_bottom/ΔV)·T/A 가 +∞ 로 넘치면 저장 σ_ratio 와의 대조가 `inf <= inf` 로 참 · 차원 σ 재구성 1000·σ₀·q · 그 허용 (`sigma_identity_tol` —
    저장 σ_dim 과 재구성 차원 σ 의 합) 도 넘치면 `x <= inf` 로 참 · 넘친 T/A 와의 G→q 대조도 `inf <= inf` · 0 으로 밑넘친 q 는 절대 반폭 5e-9 뒤에 숨는다
  · scale² (Python float 의 OverflowError) · 큰 JSON 정수 (10⁴⁰⁰ — float 로 못 옮김) = 사유가 아니라 예외
  A  게시 증서 반례 — 실제 생산자 정상 침대 (사슬 21 구 · 상자 1.5 — H0 · H12 · physics FULL computed · CF model_over_conduction · 협착-only computed /
     model_over_conduction) 의 증서만 바꾼다 (봉인된 기하 · 기록 값 · 다른 증서는 그대로):
     A1 전류 넘침 (Codex 반례 A 의 게시판) — I_bottom 1e308 · I_top −1e308 · sum_g 1e308 (게시 증서에는 없는 키 — 무시된다) · 마지막 pass 시도 전류도 맞춤 ·
        T 20 · A 2.25 → q_rec = (I_b·T)/A = +∞ · 저장 q 유한 그대로.  H0 FULL · physics FULL · H12 FULL · H0 CF (게시 model_over_conduction) ·
        physics 협착-only (게시 model_over_conduction) 다섯 자리
     A2 봉인 일관 T ≈ A ≈ 1e308 — 실행의 모든 증서 기하를 2¹⁰¹⁹ 배 (T/A = 20/2.25 비트 그대로 · 다른 증서 재구성 비트 그대로) + H0 FULL 전류 2 → (2·T)/A 넘침
     A3 봉인 일관 T/A 넘침 — 모든 증서 T 1e300 · A 1e−10 (g_to_q 그대로) → T/A = +∞ · 게시 증서 전부 q_rec = +∞
     A4 봉인 일관 scale 1e200 — 모든 증서 scale² = OverflowError (고치기 전: 증서 결합 · 세대 계약 · τ 행 · 기록 판정이 예외)
     A5 증서 하나 (증서 결합 관문) — T = A = 1e308 (Codex 모양 그대로) + 전류 2 · T/A 밑넘침 · q_rec 0 밑넘침 · d_rec 넘침 · 허용 넘침 · 큰 JSON 정수 일곱 칸
        (plate_z · box_x · scale · g_to_q · delta_V · I_bottom · sigma_bulk_S_cm) · ★ 10-16 L214R-07 — d_rec · 허용 넘침 두 레코드는 레코드 항등식도 넘쳐 0b 가 먼저
        non_finite 로 거부 (증서 경로 검사는 직접 호출로 본다 · `scripts/test_l214r06_same_class.py` B)
  C  대조 (그대로여야):
     C1 실제 생산자 정상 게시 레코드 — 상자 1.5 · 2.0 (CF computed) · SE+AM 침대 (전자 게시 증서) — 세 모드 소비자 전부 통과 · τ 값 = φ_mc/f 그대로
     C2 사다리 fallback 게시 레코드 — spsolve 증서 실패 → cg+jacobi · + cg+jacobi 미수렴 → gmres+ilu (모든 풀이)
     C3 숫자 없는 가지 (비관통 valid_zero) 정책 그대로 · C4 FULL 모형 한계 레코드 그대로 (전체 행렬 = test_l214r01_certificate)
     C5 이미 거부되던 변이는 거부 그대로 · C6 경계 · 상수 그대로 (q 반폭 5e-9 + 16ε · G→q 1e−12 · 큰 유한 기하 2¹⁰¹⁹ 은 넘침이 없으면 통과)
  D  관문 경계 (문서화 — 고치기 전 · 뒤 같다): 공용 기술 검사 0b (`ion_record_problem`) 는 증서를 읽지 않는다 (computed = 기록 값 · 두 표현 항등식만) ·
     게시 채널 판정 (`pipeline_service.channel_verdict`) · 내용 판정 (`network_content_verdict` — 모드 파일) 은 computed 채널의 **상태만** 본다 (RC6-02 · RC7-02 계약 ·
     증서를 읽지 않는다) → 반례를 받는다.  게시 결정은 내용 판정 ∧ 승격 전 기록 판정 (`network_record_verdict` — RGLR2-01 · webapp/app.py
     `_network_candidate_checks`) 이고 기록 판정이 세대 계약 (`network_generation_contract` → `certificate_binding_problems`) 을 부른다.
소비자 (레코드 단 넷) — 0b∧증서 결합 (`certificate_binding_problems`) · 0b∧세대 계약 (`network_generation_contract` = 다시 읽기 K2 · 정지 계약 ⑨) ·
  게시 관문 (내용 판정 ∧ 기록 판정 — dual · legacy · 모드 파일) · τ 행 (`ion_columns`).
  ⚠ 증서 결합 · 세대 계약은 **0b 위임**이다 — `certificate_binding_problems` 는 공용 기술 검사가 거부한 레코드에 [] 를 돌려주는 계약 (그 docstring) · 세대 계약은
    표기 + 그 결합 → 둘은 0b 와의 **합성 관문**으로 판정한다 (고치기 전: 합성 관문도 받아들인다 = 반례가 산다).
⚠ 범위 — 합성 사슬 · 합성 증서 위의 계약 시험이다.  실제 침대에서 1e308 전류가 난다는 주장이 아니다.  채택 단 (마지막 pass 시도 ↔ 요약) 결합은 게시 경로에서
  이 항목 범위 밖이다 (L214R-01 B 는 모형 한계 증서만) — 여기서 시험하지 않는다.
"""
import copy
import json
import math
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
for _p in (HERE, os.path.join(ROOT, 'webapp')):
    if _p not in sys.path:
        sys.path.insert(0, _p)

TAG = 'non_finite'
ML = 'full_over_conduction'
FULL, CF, CO = 'solve_certificate_full', 'solve_certificate_bulk_net', 'solve_certificate_constr_net'
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


def main():
    import numpy as np
    import network_conductivity as nc
    import tau_flux as tf
    import pipeline_service as ps
    #  실제 생산자 경로 = test_lhs214_model_limit 의 것 그대로 (사슬 침대 · 두 모드 · JSON 왕복 = 디스크 모양) — 복제하지 않는다 (규율 ①)
    from test_lhs214_model_limit import chain_bed, ledger_of, produce, se_am_ml_bed

    B15 = chain_bed(1.5)
    LED = ledger_of(B15)
    dual0 = produce(nc, B15)
    tmp = tempfile.mkdtemp(prefix='l214r05_')
    RECK = {'hertz': lambda d: d['hertzian'], 'hertz_h12': lambda d: d['hertzian']['hertz_h12'], 'physics': lambda d: d['physics']}
    MODES3 = ('hertz', 'hertz_h12', 'physics')
    CMODE = {'hertz': 'hertz', 'hertz_h12': 'hertz', 'physics': 'physics'}

    def write_case(dual):
        """케이스 폴더 모양 (게시 관문이 읽는 사본 전부 — dual · legacy · 모드 파일 둘)."""
        for name, doc in (('network_conductivity_hertzian.json', dual['hertzian']), ('network_conductivity_physics.json', dual['physics']),
                          ('network_conductivity_dual.json', dual), ('network_conductivity.json', dual['hertzian'])):
            with open(os.path.join(tmp, name), 'w') as f:
                json.dump(doc, f)

    # ── 소비자 넷 (레코드 단) ─────────────────────────────────────────────────────────────────────────────────────
    def verdicts(dual, m='hertz', led=LED, pp=100.0):
        """dual + 시험 자리 m → {소비자: (받아들였나 True/False · 예외 · 모름이면 None, 세부)}.
        받아들임 = 그 소비자가 그 자리 레코드 (게시 가지 · 증서) 를 유효로 받았다 (반례 = 거부여야 · 대조 = 받아야)."""
        rec = RECK[m](dual)
        out = {}
        irp, e0 = _call(tf.ion_record_problem, rec)
        v, e = _call(tf.certificate_binding_problems, m, rec)
        out['0b∧증서 결합'] = (None if (e or e0) else (irp is None and v == []), e or e0 or (irp, v))
        v, e = _call(tf.network_generation_contract, dual)
        out['0b∧세대 계약 (K2)'] = (None if (e or e0) else (irp is None and v.get('generation') == 'g2' and not v.get('problems')),
                                e or e0 or (irp, (v or {}).get('generation'), (v or {}).get('problems')))
        write_case(dual)
        vc, ec = _call(ps.network_content_verdict, tmp)
        vr, er = _call(ps.network_record_verdict, tmp)
        out['게시 관문 (내용 ∧ 기록 판정)'] = (None if (ec or er) else (bool(vc[0]) and bool(vr[0])), ec or er or (vc, vr))
        v, e = _call(tf.ion_columns, dual, led, pp)
        if e:
            out['τ 행'] = (None, e)
        else:
            st, rs = v.get(f'ion_net_status_{m}'), v.get(f'ion_net_status_reason_{m}')
            acc = st in ('OK', 'MODEL_BELOW_CONTINUUM_BOUND')
            rej = st == 'NOT_COMPUTED' and tf.reason_code(rs) == 'invalid_input'
            out['τ 행'] = (True if acc else (False if rej else None), (st, rs))
        return out

    def expect(label, dual, m, accept, **kw):
        """네 소비자 각각 — accept=True 면 받아들여야 · False 면 예외 없이 거부해야."""
        for k, (acc, det) in verdicts(dual, m, **kw).items():
            want = 'accept' if accept else 'reject'
            chk(f'{label} · {k} = {"통과" if accept else "거부"}', acc is accept, f'{want} 기대 · 얻음 {acc!r} · {det!r}')

    def tagged(label, dual, m, ck):
        """증서 결합 사유에 그 증서 자리 + 생산자 비유한 꼬리표 (NON_FINITE_REASON) · 예외 아님."""
        cb, e = _call(tf.certificate_binding_problems, m, RECK[m](dual))
        hit = [p for p in (cb or []) if p.startswith(ck + ':') and TAG in p]
        chk(f'{label} · 증서 결합 사유 = {ck}: {TAG} … (예외 아님) — {(e or (hit[0] if hit else cb))!r:.220}', e is None and bool(hit))

    def mut(fn, src=None):
        d = copy.deepcopy(src if src is not None else dual0)
        fn(d)
        return d

    def cert(d, m='hertz', ck=FULL):
        return RECK[m](d)[ck]

    def all_certs(dual):
        """한 실행의 모든 증서 (H0 · H12 · physics × 이온 · 전자 · 열 × 세 가지) — 봉인된 기하 대조 (`_cert_geometry_problems`) 와 같은 범위."""
        h = dual.get('hertzian') or {}
        for rec in (h, h.get('hertz_h12'), dual.get('physics')):
            if not isinstance(rec, dict):
                continue
            for pre in ('',) + tf.CHANNEL_PREFIXES:
                for k in nc.SOLVE_CERTIFICATE_KEYS:
                    c = rec.get(pre + k)
                    if isinstance(c, dict) and 'geometry' in c:
                        yield c

    def q_rec_of(c):
        """같은 식 · 같은 순서의 재구성 (생산자 σ 환산 · 소비자 대조와 같다)."""
        g = c['geometry']
        return (c['I_bottom'] / c['delta_V']) * (g['plate_z'] * g['scale']) / (g['box_x'] * g['box_y'] * g['scale'] ** 2)

    def set_currents(c, ib):
        c.update(I_bottom=ib, I_top=-ib)
        c['attempts'][-1].update(I_bottom=ib, I_top=-ib)            # 마지막 pass 시도 전류도 맞춘다 (채택 단 대조가 있어도 걸리지 않게)

    try:
        # ══ C1 대조 — 실제 생산자 정상 게시 레코드 ════════════════════════════════════════════════════════════════
        def sC1():
            h, h12, p = dual0['hertzian'], dual0['hertzian']['hertz_h12'], dual0['physics']
            chk(f"C1a 기준 = 실제 생산자 정상 침대 (상자 1.5) — FULL computed (q {h['sigma_full']!r} · {h12['sigma_full']!r} · {p['sigma_full']!r}) · CF "
                f"{[r_['sigma_bulk_net_status'] for r_ in (h, h12, p)]} · 협착-only {[r_['sigma_constr_net_status'] for r_ in (h, h12, p)]} · σ₀ {h['sigma_grain_S_cm']!r}",
                all(r_['sigma_full_status'] == 'computed' and r_[FULL]['status'] == 'computed' for r_ in (h, h12, p))
                and all(r_['sigma_bulk_net_status'] == 'model_over_conduction' for r_ in (h, h12, p))
                and p['sigma_constr_net_status'] == 'model_over_conduction' and h['sigma_constr_net_status'] == 'computed')
            for m in MODES3:
                expect(f'C1b 정상 게시 레코드 (상자 1.5 · {m})', dual0, m, True)
            row = tf.ion_columns(dual0, LED, 100.0)
            phi = LED['phi_se_mass_conserving']
            want = {m: phi / (RECK[m](dual0)['sigma_full'] * LED['thickness_um'] / LED['thickness_mass_conserving_um']) for m in MODES3}
            chk(f"C1c τ 값 그대로 — tau2 = φ_mc/f (f = σ_ratio·L_gap/L_mc) 세 모드 {[(m, row.get(f'tau2_ion_{m}')) for m in MODES3]}",
                all(row.get(f'ion_net_status_{m}') == 'OK' and row.get(f'tau2_ion_{m}') == want[m] for m in MODES3))
            for lab, bed, kw in (('상자 2.0 (CF computed)', chain_bed(2.0), {}),
                                 ('SE+AM 침대 상자 1.5 (전자 게시 증서)', (lambda b: (b[0], b[1], b[2], 1.5))(se_am_ml_bed()),
                                  dict(se=(1,), am=(2,), tm={1: 'SE', 2: 'AM_P'}))):
                d = produce(nc, bed, **kw)
                pre = (all(RECK[m](d)['sigma_full_status'] == 'computed' for m in MODES3)
                       and (lab.startswith('상자 2.0') and d['hertzian']['sigma_bulk_net_status'] == 'computed'
                            or lab.startswith('SE+AM') and (d['physics'].get('electronic_solve_certificate_full') or {}).get('status') == 'computed'))
                chk(f'C1d 전제 — {lab} 세 모드 FULL computed', pre)
                for m in MODES3:
                    expect(f'C1e 정상 게시 레코드 ({lab} · {m})', d, m, True, led=ledger_of(bed))

        _guard('C1', sC1)

        # ══ A1 — 게시 증서 전류 넘침 (Codex 반례 A 의 게시판) ═══════════════════════════════════════════════════════
        def sA1():
            sites = (('hertz', FULL, 'H0 FULL (Codex 반례 A 모양)'), ('physics', FULL, 'physics FULL'), ('hertz_h12', FULL, 'H12 FULL'),
                     ('hertz', CF, 'H0 CF (게시 model_over_conduction)'), ('physics', CO, 'physics 협착-only (게시 model_over_conduction)'))
            for m, ck, lab in sites:
                def a1(d, m_=m, ck_=ck):
                    c = cert(d, m_, ck_)
                    set_currents(c, 1e308)
                    c['sum_g'] = 1e308
                d = mut(a1)
                c = cert(d, m, ck)
                rec = RECK[m](d)
                qk = {FULL: 'sigma_full', CF: 'sigma_bulk_net', CO: 'sigma_constr_net'}[ck]
                chk(f'A1a 전제 [{lab}] — 게시 상태 {c["status"]!r} · 수치 증서 통과 (보존 0 · 잔차 그대로) · 기하 T 20 · A 2.25 유한 · 같은 순서 재구성 = +∞ · '
                    f'저장 σ_ratio {rec[qk]!r} 유한',
                    c['status'] in tf.CERT_PUBLISHED_STATES and nc.certificate_problem(c) is None and math.isinf(q_rec_of(c))
                    and math.isfinite(rec[qk]) and c['geometry'] == {'plate_z': 20.0, 'box_x': 1.5, 'box_y': 1.5, 'scale': 1})
                expect(f'A1b ★ 전류 1e308 넘침 [{lab}]', d, m, False)
                tagged(f'A1c ★ [{lab}]', d, m, ck)

        _guard('A1', sA1)

        # ══ A2 · A3 · A4 — 봉인 일관 기하 넘침 (실행의 모든 증서 · 세대 계약 · 기록 판정까지) ═══════════════════════════════════════
        G2 = {'plate_z': 20.0 * 2.0 ** 1019, 'box_x': 1.5 * 2.0 ** 509, 'box_y': 1.5 * 2.0 ** 510, 'scale': 1}

        def sA234():
            def a2(d):
                for c in all_certs(d):
                    c['geometry'] = dict(G2)
                set_currents(cert(d), 2.0)
            d2 = mut(a2)
            T, A = G2['plate_z'] * G2['scale'], G2['box_x'] * G2['box_y'] * G2['scale'] ** 2
            others = [c for c in all_certs(d2) if c is not cert(d2) and c.get('I_bottom') is not None]
            chk('A2a 전제 — T = 20·2¹⁰¹⁹ · A = 2.25·2¹⁰¹⁹ 유한 · T/A = g_to_q 비트 그대로 · 다른 증서 재구성 = 원래 재구성 비트 그대로 · H0 FULL (2·T)/A = +∞',
                math.isfinite(T) and math.isfinite(A) and T / A == cert(dual0)['g_to_q'] == cert(d2)['g_to_q']
                and all(q_rec_of(c) == (c['I_bottom'] / c['delta_V']) * 20.0 / 2.25 for c in others) and math.isinf(q_rec_of(cert(d2))))
            expect('A2b ★ 봉인 일관 T ≈ A ≈ 1e308 + H0 FULL 전류 2', d2, 'hertz', False)
            tagged('A2c ★', d2, 'hertz', FULL)

            def a3(d):
                for c in all_certs(d):
                    c['geometry'] = {'plate_z': 1e300, 'box_x': 1e-5, 'box_y': 1e-5, 'scale': 1}
            d3 = mut(a3)
            pub = [c for c in all_certs(d3) if c.get('status') in tf.CERT_PUBLISHED_STATES]
            chk('A3a 전제 — 모든 증서 T 1e300 · A 1e−10 (둘 다 유한 양수 · g_to_q 그대로 8.89) · T/A = +∞ · 게시 증서 전부 같은 순서 재구성 +∞',
                math.isinf(1e300 / (1e-5 * 1e-5)) and len(pub) >= 9 and all(math.isinf(q_rec_of(c)) for c in pub)
                and all(c['g_to_q'] == cert(dual0)['g_to_q'] for c in all_certs(d3)))
            for m in MODES3:
                expect(f'A3b ★ 봉인 일관 T/A 넘침 · {m}', d3, m, False)
                tagged(f'A3c ★ T/A 넘침 · {m}', d3, m, FULL)

            def a4(d):
                for c in all_certs(d):
                    c['geometry'] = dict(c['geometry'], scale=1e200)
            d4 = mut(a4)
            chk('A4a 전제 — scale 1e200 은 유한 · Python float 의 scale ** 2 = OverflowError (곱 · 나눗셈은 inf)',
                _call(lambda: 1e200 ** 2)[1] is not None and _call(lambda: 1e200 ** 2)[1].startswith('OverflowError'))
            for m in MODES3:
                expect(f'A4b ★ 봉인 일관 scale 1e200 (scale² OverflowError) · {m}', d4, m, False)
                tagged(f'A4c ★ scale² 넘침 · {m}', d4, m, FULL)

        _guard('A2–A4', sA234)

        # ══ A5 — 증서 하나 (증서 결합 관문 · 세대 계약 이후 소비자는 예외 없이 거부) ═══════════════════════════════════════
        def sA5():
            s0 = dual0['hertzian']['sigma_grain_S_cm']

            def one_geo(c, geo, ib=None):
                c['geometry'] = dict(geo)
                g = c['geometry']
                c['g_to_q'] = (g['plate_z'] * g['scale']) / (g['box_x'] * g['box_y'] * g['scale'] ** 2)
                if ib is not None:
                    set_currents(c, ib)

            def a5a(d):                                   # Codex 'T = A = 1e308' 모양 그대로 (T/A = 1 유한) + 전류 2 → (2·T)/A 넘침
                one_geo(cert(d), {'plate_z': 1e308, 'box_x': 1e154, 'box_y': 1e154, 'scale': 1}, 2.0)

            def a5b(d):                                   # T/A 밑넘침 (T 1e−300 · A 1e100 → 0) — g_to_q 는 원래 값 그대로
                cert(d)['geometry'] = {'plate_z': 1e-300, 'box_x': 1e50, 'box_y': 1e50, 'scale': 1}

            def a5c(d):                                   # q_rec 0 밑넘침 — T 1e−300 · A 1 · 전류 1e−30 · 기록 q 1e−9 (두 표현 항등식 맞춤)
                one_geo(cert(d), {'plate_z': 1e-300, 'box_x': 1.0, 'box_y': 1.0, 'scale': 1}, 1e-30)
                r = d['hertzian']
                r['sigma_full'] = 1e-9
                r['sigma_full_mScm'] = 1000.0 * s0 * 1e-9

            def a5d(d):                                   # d_rec 넘침 — T = A = 1 · 전류 = 기록 q = 1e308 (q 재구성 유한 · 1000·σ₀·q = +∞)
                one_geo(cert(d), {'plate_z': 1.0, 'box_x': 1.0, 'box_y': 1.0, 'scale': 1}, 1e308)
                r = d['hertzian']
                r['sigma_full'] = 1e308
                r['sigma_full_mScm'] = 1.0

            def a5e(d):                                   # 허용 넘침 — T = A = 1 · 전류 = 기록 q = 3e307 · 기록 σ_dim 1.7e308 (재구성 차원 σ 9e307 유한 · 허용 = +∞)
                one_geo(cert(d), {'plate_z': 1.0, 'box_x': 1.0, 'box_y': 1.0, 'scale': 1}, 3e307)
                r = d['hertzian']
                r['sigma_full'] = 3e307
                r['sigma_full_mScm'] = 1.7e308

            cases = (('A5a T = A = 1e308 (Codex 모양) + 전류 2', a5a), ('A5b T/A 밑넘침 (T 1e−300 · A 1e100)', a5b),
                     ('A5c q_rec 0 밑넘침 (절대 반폭 5e-9 뒤에 숨음)', a5c), ('A5d 차원 σ 재구성 1000·σ₀·q 넘침', a5d),
                     ('A5e 차원 σ 허용 넘침 (σ_dim + 1000·σ₀·q)', a5e))
            dd = {lab: mut(fn) for lab, fn in cases}
            c_a, c_c, c_d, c_e = (cert(dd[k]) for k in (cases[0][0], cases[2][0], cases[3][0], cases[4][0]))
            #  ★ 10-16 L214R-07 — A5d · A5e 레코드는 레코드 자신의 두 표현 항등식도 넘친다 (1000·σ₀·σ_ratio = +∞ · 허용 = +∞) → 공용 기술 검사 0b 가 먼저
            #    non_finite 로 거부한다 (옛 판: 0b 가 inf ≤ inf 로 통과 · 증서 결합만 막았다 — 그 구멍이 L214R-07).  증서 결합은 0b 위임이라 [] → 증서 경로의
            #    유한성 검사 (`_cert_published_problem`) 는 직접 불러 그대로 본다 (이중 방어 · 문구 그대로)
            chk('A5-0 전제 — 넷 다 수치 증서 통과 · A5a 재구성 +∞ · A5c 재구성 0.0 · A5d 재구성 = 기록 q 유한 · 1000·σ₀·q = +∞ · A5e 재구성 = 기록 q · '
                '1000·σ₀·q 유한 · 허용 = +∞ · A5c 기록은 0b 통과 (증서 결합만 막을 수 있다) · A5d · A5e 기록은 0b 가 non_finite 로 먼저 거부 (L214R-07)',
                all(nc.certificate_problem(c) is None for c in (c_a, c_c, c_d, c_e))
                and math.isinf(q_rec_of(c_a)) and q_rec_of(c_c) == 0.0
                and q_rec_of(c_d) == 1e308 and math.isinf(1000.0 * s0 * 1e308)
                and q_rec_of(c_e) == 3e307 and math.isfinite(1000.0 * s0 * 3e307) and math.isinf(tf.sigma_identity_tol(s0, 3e307, 1.7e308))
                and tf.ion_record_problem(dd[cases[2][0]]['hertzian']) is None
                and all(str((tf.ion_record_problem(dd[cases[i][0]]['hertzian']) or ('', ''))[1]).startswith(TAG) for i in (3, 4)))
            for lab, _fn in cases:
                d = dd[lab]
                v = verdicts(d, 'hertz')
                acc, det = v.pop('0b∧증서 결합')
                chk(f'{lab} ★ 0b∧증서 결합 = 거부 (예외 아님)', acc is False, det)
                if lab in (cases[3][0], cases[4][0]):
                    r = d['hertzian']
                    irp = tf.ion_record_problem(r)
                    cp, ce = _call(tf._cert_published_problem, 'hertz', 'full', r, r['sigma_full'], r['sigma_full_mScm'], r['sigma_full_status'], cert(d))
                    chk(f'{lab} ★ 0b 사유 = {TAG} … (L214R-07 — 레코드 항등식) · 증서 경로 직접 = {TAG} … (예외 아님) — {irp!r:.120} · {ce or cp!r:.120}',
                        isinstance(irp, tuple) and str(irp[1]).startswith(TAG) and ce is None and isinstance(cp, str) and TAG in cp)
                else:
                    tagged(f'{lab} ★', d, 'hertz', FULL)
                chk(f'{lab} · 세대 계약 · 게시 관문 · τ 행 = 예외 없이 거부 {[(k, a) for k, (a, _x) in v.items()]}',
                    all(a is False for a, _x in v.values()), v)

            big = 10 ** 400
            huge = {'기하 plate_z': lambda c: c['geometry'].update(plate_z=big), '기하 box_x': lambda c: c['geometry'].update(box_x=big),
                    '기하 scale': lambda c: c['geometry'].update(scale=big), 'g_to_q': lambda c: c.update(g_to_q=big),
                    'delta_V': lambda c: c.update(delta_V=big), 'I_bottom': lambda c: c.update(I_bottom=big),
                    'sigma_bulk_S_cm': lambda c: c.update(sigma_bulk_S_cm=big)}
            got = {}
            for lab, fn in huge.items():
                d = json.loads(json.dumps(mut(lambda d_, f=fn: f(cert(d_)))))     # JSON 정수 10⁴⁰⁰ 그대로 (표준 JSON 이 싣는 값)
                got[lab] = (verdicts(d, 'hertz'), d)
            for lab, (v, _d) in got.items():
                chk(f'A5f ★ 큰 JSON 정수 (10⁴⁰⁰ — float 로 못 옮김) H0 FULL 증서 {lab} → 네 소비자 예외 없이 거부 {[(k, a) for k, (a, _x) in v.items()]}',
                    all(a is False for a, _x in v.values()), {k: str(x)[:120] for k, (a, x) in v.items() if a is not False})

        _guard('A5', sA5)

        # ══ C2 — 사다리 fallback 게시 레코드 (앞 단 실패 기록 + 마지막 pass) 는 통과 그대로 ══════════════════════════════════════
        def faulted(make, bad_cg=False):
            """첫 단 spsolve 가 틀린 해 (0 벡터 → 증서 실패) · bad_cg 면 cg 도 미수렴 (info 1) → 실제 생산자 사다리가 다음 단으로 간다."""
            old = {k: getattr(nc, k) for k in ('spsolve', 'cg')}
            nc.spsolve = lambda A_, b_: np.zeros(len(b_))
            if bad_cg:
                nc.cg = lambda A_, b_, **k_: (np.zeros(len(b_)), 1)
            try:
                return make()
            finally:
                for k, v in old.items():
                    setattr(nc, k, v)

        def sC2():
            for lab, bad_cg, want in (('spsolve 증서 실패 → cg+jacobi', False, [('spsolve', 'certificate_failed'), ('cg+jacobi', 'pass')]),
                                      ('spsolve 증서 실패 → cg+jacobi 미수렴 → gmres+ilu', True,
                                       [('spsolve', 'certificate_failed'), ('cg+jacobi', 'not_converged'), ('gmres+ilu', 'pass')])):
                d = faulted(lambda: produce(nc, B15), bad_cg)
                atts = [(a.get('method'), a.get('outcome')) for a in cert(d).get('attempts') or []]
                chk(f'C2a 전제 [{lab}] — H0 FULL 게시 증서 시도 {atts} · 세 모드 computed · σ_ratio = 기준 침대와 같다',
                    atts == want and all(RECK[m](d)['sigma_full'] == RECK[m](dual0)['sigma_full'] for m in MODES3))
                for m in MODES3:
                    expect(f'C2b fallback 게시 레코드 [{lab} · {m}]', d, m, True)

        _guard('C2', sC2)

        # ══ C3 · C4 — 숫자 없는 가지 정책 · FULL 모형 한계 레코드 그대로 ══════════════════════════════════════════════════════
        def sC34():
            A, C, plate, box = chain_bed(1.5)
            Bnp = (A, [c for c in C if c['id1'] != 10], plate, box)              # 10–11 접촉 하나를 뺀 사슬 = 관통 성분 없음
            dnp = produce(nc, Bnp)
            row = tf.ion_columns(dnp, ledger_of(Bnp), 0.0)
            con = tf.network_generation_contract(dnp)
            write_case(dnp)
            chk('C3 숫자 없는 가지 (비관통) — 세 모드 valid_zero · 증서 결합 [] · 세대 g2 · τ NOT_PERCOLATING · 게시 관문 통과 (기존 정책 그대로)',
                all(RECK[m](dnp)['sigma_full_status'] == 'valid_zero' and tf.certificate_binding_problems(m, RECK[m](dnp)) == [] for m in MODES3)
                and con['generation'] == 'g2' and not con['problems']
                and all(row.get(f'ion_net_status_{m}') == 'NOT_PERCOLATING' for m in MODES3)
                and ps.network_content_verdict(tmp)[0] and ps.network_record_verdict(tmp)[0],
                [(m, RECK[m](dnp)['sigma_full_status'], row.get(f'ion_net_status_{m}')) for m in MODES3])
            B1 = chain_bed(1.0)
            d1 = produce(nc, B1)
            row = tf.ion_columns(d1, ledger_of(B1), 100.0)
            write_case(d1)
            chk('C4 FULL 모형 한계 레코드 (상자 1.0 · physics) — 증서 결합 [] 세 모드 · 세대 g2 · τ H0 OK · physics NOT_COMPUTED full_over_conduction · 게시 관문 통과',
                d1['physics']['sigma_full_reason'] == ML and all(tf.certificate_binding_problems(m, RECK[m](d1)) == [] for m in MODES3)
                and tf.network_generation_contract(d1)['generation'] == 'g2' and not tf.network_generation_contract(d1)['problems']
                and row.get('ion_net_status_hertz') == 'OK' and (row.get('ion_net_status_physics'), row.get('ion_net_status_reason_physics')) == ('NOT_COMPUTED', ML)
                and ps.network_content_verdict(tmp)[0] and ps.network_record_verdict(tmp)[0],
                (row.get('ion_net_status_physics'), row.get('ion_net_status_reason_physics')))

        _guard('C3–C4', sC34)

        # ══ C5 — 이미 거부되던 변이는 거부 그대로 ═════════════════════════════════════════════════════════════════════
        def sC5():
            def numbers_only(d):
                for m in ('hertz', 'physics'):
                    r = RECK[m](d)
                    r['sigma_full'] = round(r['sigma_full'] * 1.25, 8)
                    r['sigma_full_mScm'] = round(r['sigma_full'] * r['sigma_grain_S_cm'] * 1000, 6)     # 두 표현 항등식은 맞춘다 (0b 통과)
            muts = {'H0 FULL 전류 ×1.01 (시도 맞춤)': lambda d: set_currents(cert(d), cert(d)['I_bottom'] * 1.01),
                    'H0 FULL ΔV 2': lambda d: cert(d).update(delta_V=2.0),
                    'H0 FULL 보존 실패 (I_top 0)': lambda d: cert(d).update(I_top=0.0, conservation_rel=1.0),
                    'H0 FULL g_to_q ×2': lambda d: cert(d).update(g_to_q=cert(d)['g_to_q'] * 2),
                    'H0 CF 증서 삭제 (숫자 실림)': lambda d: d['hertzian'].pop(CF),
                    '숫자만 ×1.25 (항등식 맞춤 · 두 모드)': numbers_only}
            for lab, fn in muts.items():
                v = verdicts(mut(fn), 'hertz')
                chk(f'C5 이미 거부 — {lab} → 0b∧증서 결합 · 0b∧세대 계약 · 게시 관문 · τ 행 거부 그대로 {[(k, a) for k, (a, _x) in v.items()]}',
                    all(a is False for a, _x in v.values()), {k: str(x)[:120] for k, (a, x) in v.items() if a is not False})
            why = tf.certificate_binding_problems('hertz', mut(numbers_only)['hertzian'])
            chk(f'C5 숫자만 변이의 사유 = 재구성 (문구 그대로) — {why!r:.160}', any('재구성' in p for p in why))

        _guard('C5', sC5)

        # ══ C6 — 경계 · 상수 그대로 ══════════════════════════════════════════════════════════════════════════════════
        def sC6():
            c0 = cert(dual0)
            q0 = q_rec_of(c0)
            s0 = dual0['hertzian']['sigma_grain_S_cm']

            def q_at(f):
                def fn(d):
                    r = d['hertzian']
                    r['sigma_full'] = q0 + f * tf.SIGMA_RATIO_ROUND_HALF
                    r['sigma_full_mScm'] = 1000.0 * s0 * r['sigma_full']
                return tf.certificate_binding_problems('hertz', mut(fn)['hertzian'])
            chk(f'C6a 발행 σ_ratio = 재구성 q ± 0.9·5e-9 통과 · +1.1·5e-9 · −1.1·5e-9 거부 (저장 반폭 그대로 · 재구성 문구) — {q_at(1.1)!r:.120}',
                q_at(0.9) == [] and q_at(-0.9) == [] and any('재구성' in p for p in q_at(1.1)) and any('재구성' in p for p in q_at(-1.1)))

            def g_at(f):
                return tf.certificate_binding_problems('hertz', mut(lambda d: cert(d).update(g_to_q=cert(d)['g_to_q'] * (1.0 + f)))['hertzian'])
            chk(f'C6b G→q 상대 0.9e−12 통과 · 1.1e−12 거부 (CERT_G2Q_REL_TOL 그대로) — {g_at(1.1e-12)!r:.120}',
                g_at(0.9e-12) == [] and g_at(-0.9e-12) == [] and any('G→q' in p for p in g_at(1.1e-12)))

            def big_finite(d):
                for c in all_certs(d):
                    c['geometry'] = dict(G2)
            dbf = mut(big_finite)
            chk('C6c 전제 — 큰 유한 기하 (모든 증서 2¹⁰¹⁹ 배 · 전류 그대로) 는 재구성이 넘치지 않는다 (게시 증서 전부 q_rec = 원래 재구성 비트 그대로)',
                all(q_rec_of(c) == (c['I_bottom'] / c['delta_V']) * 20.0 / 2.25 for c in all_certs(dbf) if c.get('status') in tf.CERT_PUBLISHED_STATES))
            for m in MODES3:
                expect(f'C6d 큰 유한 기하 (넘침 없음) · {m}', dbf, m, True)
            chk('C6e 상수 그대로 — σ_ratio 반폭 5e-9 · σ_dim 반폭 5e-7 · 16ε · G→q 1e−12 · ΔV 1',
                tf.SIGMA_RATIO_ROUND_HALF == 5e-9 and tf.SIGMA_DIM_ROUND_HALF == 5e-7 and tf._ID_FP == 16 * sys.float_info.epsilon
                and tf.CERT_G2Q_REL_TOL == 1e-12 and tf.CERT_DELTA_V == 1.0)

        _guard('C6', sC6)

        # ══ D — 관문 경계 (문서화 · 고치기 전 · 뒤 같다) ═══════════════════════════════════════════════════════════════
        def sD():
            d = mut(lambda d_: set_currents(cert(d_), 1e308))
            rec = d['hertzian']
            write_case(d)
            cv, cc = ps.channel_verdict(rec, 'ionic', CMODE['hertz']), ps.network_content_verdict(tmp)
            chk(f'D1 0b (ion_record_problem) 는 증서를 읽지 않는다 — computed 레코드의 기록 값 · 두 표현 항등식만 (A1 H0 FULL 반례에 None) · 증서 결합 · 세대 계약이 '
                f'0b 위임 뒤 증서를 본다 — {tf.ion_record_problem(rec)!r}', tf.ion_record_problem(rec) is None)
            chk(f'D2 게시 채널 판정 · 내용 판정 (모드 파일) 은 computed 채널의 상태만 본다 (RC6-02 · RC7-02 — 증서를 읽지 않는다) → A1 반례에 ok — {cv!r} · {cc!r}',
                cv[0] == 'ok' and cc[0] is True)

        _guard('D', sD)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print(f'\ntest_l214r05_published_certificate: {_ok}/{_ok + len(_fail)} PASS' + (f'   FAILED: {len(_fail)}' if _fail else ''))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
