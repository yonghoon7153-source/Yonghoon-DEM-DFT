#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L214R-06 · 07 · 08 — 같은 부류 셋 (게시 증서의 채택 단 · 두 σ 표현 항등식의 유한성 · float 로 못 옮기는 큰 JSON 정수) 반례 (상주 시험).

  python3 scripts/test_l214r06_same_class.py          # 종료코드 0 = 전부 PASS

근거 = 수정 계획 `docs/reviews/lhs214r_fix_plan_20261016.md` §4-2 (1저자 10-16 *"(가) 먼저 고치고 보내기"* — Q4 · Q5 · Q6 = 원장 `L214R-06` · `07` · `08`) ·
L214R-05 수정 중 보고된 같은 부류 (L214R-01 A · B 와 L214R-05 의 규칙을 남은 자리로).  선행 시험 = `scripts/test_l214r01_certificate.py` (모형 한계 증서) ·
`scripts/test_l214r05_published_certificate.py` (게시 증서 유한성) — 이 시험은 그 파일들을 고치지 않는다 (그대로 통과해야 한다).

★ 시험 먼저 — 고치기 전 코드에서 반례 묶음이 빨갛다:
  A  L214R-06 (Q4) — 게시 증서 경로 (`tau_flux._cert_published_problem` — 숫자를 싣는 이온 FULL · CF · 협착-only) 가 증서의 시도 기록 (`attempts`) 을 읽지
     않는다 → 정상 H0 레코드의 FULL 증서 마지막 시도 한 칸만 바꿔도 소비자 전부 통과 · τ OK: outcome certificate_failed · residual_rel 1.0 ·
     conservation_rel 1.0 · error · 다른 방법 · I_bottom ×2 (마지막 시도만) · 목록 [] · 키 삭제 · 직접해 단 krylov_info 1.  CF (computed · model_over_conduction) ·
     협착-only (computed · model_over_conduction) · H12 · physics FULL · fallback 증서의 마지막 시도도.  고친 뒤 = 모형 한계 증서 ③ 과 **같은 함수**
     (`network_conductivity.adopted_attempt_binding_problem`) 가 게시 증서에도 (모형 한계 증서 판정의 문구는 그대로).
  B  L214R-07 (Q5) — 공용 기술 검사 (`tau_flux.ion_record_problem`) 의 두 σ 표현 항등식이 비교 전에 유한성을 안 본다: σ_ratio 1e308 · σ_dim 1.0 (σ₀ 3e-3) →
     1000·σ₀·σ_ratio = +∞ · |차| = 허용 = +∞ · inf ≤ inf 통과 · 곱이 0 으로 밑넘치면 절대 반폭 5e-7 뒤에 숨는다.  세대 2 는 증서 결합이 따로 막지만 증서
     없는 옛 세대 레코드 (진짜 194 v1.2 역사 레코드 = inferred_legacy) 는 τ 행이 f_ion = ∞ · tau2 = 0 (MODEL_BELOW_CONTINUUM_BOUND · 값 유지)
  D  L214R-08 (Q6) — float 로 못 옮기는 큰 JSON 정수 (10⁴⁰⁰ — json.loads 가 int 로 준다) 가 사유 대신 OverflowError:
     (a) 숫자 없는 가지 증서 I_bottom (`_cert_unpublished_problem` — None = '해 주장 없음 = 받음' 인 자리 · 변환 불가 = 숫자가 실렸다 = 거부여야)
     (b) 전자 · 열 증서 σ_bulk (`sigma0_binding_problems`) · (c) 모형 한계 증서 σ_bulk (`full_model_limit_problem`) · (d) 레코드 값 (`ion_record_problem`) ·
     같은 소비 경로의 다른 자리 (온도 규약 T_C · 모형 한계 레코드 σ₀ · τ 장부 · 옛 세대 레코드 · 등급 τ getter)
  H  대조 (그대로여야): 실제 생산자 정상 게시 레코드 (상자 1.5 · 2.0) · 사다리 fallback 성공 (앞 단 실패 + 마지막 pass) · 정직한 실패 (비관통 valid_zero ·
     협착-only 0 저항 not_computed (I_bottom None) · FULL 모형 한계 · 모든 단 실패 = solver_guard) · 진짜 역사 레코드 τ 그대로 · 항등식 경계 · 생산자 증서
     모양 (해를 낸 모든 이온 증서 = 시도 목록이 비지 않고 마지막이 그 해의 pass 단)
소비자 (레코드 단 넷) — 0b∧증서 결합 (`certificate_binding_problems`) · 0b∧세대 계약 (`network_generation_contract` = 다시 읽기 K2 · 정지 계약 ⑨) ·
  게시 관문 (내용 판정 ∧ 기록 판정 — `pipeline_service.network_content_verdict` · `network_record_verdict`) · τ 행 (`ion_columns` · 폴더는 `case_row`).
  ⚠ 증서 결합 · 세대 계약은 **0b 위임**이다 (L214R-01 · 05 시험과 같은 합성 관문).  옛 세대 레코드는 게시 관문 대상이 아니다 (현행 생산물만 게시) —
    공용 기술 검사 · τ 행 · 폴더 행으로 본다 (인계 P4 의 정지 계약 ③ 도 같은 `ion_record_problem`).
⚠ 범위 — 손상 · 위조 기록을 관문이 거르는가의 계약 시험이다 (합성 사슬 · 진짜 역사 레코드에 합성 변이).  실제 침대 자료에서 난 일이 아니다.
"""
import copy
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
FULL, CF, CO = 'solve_certificate_full', 'solve_certificate_bulk_net', 'solve_certificate_constr_net'
BIG_TXT = '1' + '0' * 400                                        # JSON 정수 10⁴⁰⁰ — float 로 못 옮긴다 (json.loads = int)
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


def with_big(dual, path):
    """dual 의 path (키 목록) 자리를 JSON 정수 10⁴⁰⁰ 으로 — **JSON 텍스트**에 400 자리 정수를 넣고 json.loads (디스크 · 다시 읽기와 같은 모양)."""
    d = copy.deepcopy(dual)
    o = d
    for k in path[:-1]:
        o = o[k]
    o[path[-1]] = '__L214R08_BIG__'
    out = json.loads(json.dumps(d).replace('"__L214R08_BIG__"', BIG_TXT))
    o = out
    for k in path[:-1]:
        o = o[k]
    assert isinstance(o[path[-1]], int) and o[path[-1]] == 10 ** 400
    return out


def main():
    import numpy as np
    import network_conductivity as nc
    import tau_flux as tf
    import pipeline_service as ps
    #  실제 생산자 경로 = test_lhs214_model_limit 의 것 그대로 (사슬 침대 · 두 모드 · JSON 왕복 = 디스크 모양) · 진짜 역사 레코드 묶음 = test_gen2_role_contract 의
    #  ARCHIVE (194 v1.2 배치 원천) — 복제하지 않는다 (규율 ①)
    from test_lhs214_model_limit import chain_bed, ledger_of, produce, se_am_ml_bed
    from test_gen2_role_contract import ARCHIVE

    tmp = tempfile.mkdtemp(prefix='l214r06_')
    case_dir = os.path.join(tmp, 'case')
    os.makedirs(case_dir)
    MODES3 = ('hertz', 'hertz_h12', 'physics')

    def rec_of(d, m):
        return tf.mode_record(d, m)

    def write_case(dual):
        """케이스 폴더 모양 (게시 관문이 읽는 사본 전부 — dual · legacy · 모드 파일 둘)."""
        for name, doc in (('network_conductivity_hertzian.json', dual['hertzian']), ('network_conductivity_physics.json', dual['physics']),
                          ('network_conductivity_dual.json', dual), ('network_conductivity.json', dual['hertzian'])):
            with open(os.path.join(case_dir, name), 'w') as f:
                json.dump(doc, f)

    def tau_default(st, rs):
        return st in ('OK', 'MODEL_BELOW_CONTINUUM_BOUND')

    def tau_np(st, rs):
        return st == 'NOT_PERCOLATING'

    def tau_ml(st, rs):
        return (st, rs) == ('NOT_COMPUTED', ML)

    def verdicts(dual, m, led, pp, tau_ok=tau_default):
        """dual + 시험 자리 m → {소비자: (받아들였나 True/False · 예외 · 모름이면 None, 세부)} — 받아들임 = 그 자리 레코드를 유효로 받았다."""
        rec = rec_of(dual, m)
        out = {}
        irp, e0 = _call(tf.ion_record_problem, rec)
        v, e = _call(tf.certificate_binding_problems, m, rec)
        out['0b∧증서 결합'] = (None if (e or e0) else (irp is None and v == []), e or e0 or (irp, v))
        v, e = _call(tf.network_generation_contract, dual)
        out['0b∧세대 계약 (K2)'] = (None if (e or e0) else (irp is None and v.get('generation') == 'g2' and not v.get('problems')),
                                e or e0 or (irp, (v or {}).get('generation'), (v or {}).get('problems')))
        write_case(dual)
        vc, ec = _call(ps.network_content_verdict, case_dir)
        vr, er = _call(ps.network_record_verdict, case_dir)
        out['게시 관문 (내용 ∧ 기록 판정)'] = (None if (ec or er) else (bool(vc[0]) and bool(vr[0])), ec or er or (vc, vr))
        v, e = _call(tf.ion_columns, dual, led, pp)
        if e:
            out['τ 행'] = (None, e)
        else:
            st, rs = v.get(f'ion_net_status_{m}'), v.get(f'ion_net_status_reason_{m}')
            rej = st == 'NOT_COMPUTED' and tf.reason_code(rs) == 'invalid_input'
            out['τ 행'] = (True if tau_ok(st, rs) else (False if rej else None), (st, rs))
        return out

    def expect(label, dual, m, accept, led, pp, tau_ok=tau_default):
        """네 소비자 각각 — accept=True 면 받아들여야 · False 면 예외 없이 거부해야."""
        for k, (acc, det) in verdicts(dual, m, led, pp, tau_ok).items():
            want = 'accept' if accept else 'reject'
            chk(f'{label} · {k} = {"통과" if accept else "거부"}', acc is accept, f'{want} 기대 · 얻음 {acc!r} · {det!r}')

    def cb_reason(label, dual, m, ck, needle):
        """증서 결합 사유에 그 증서 자리 + 기대 문구 · 예외 아님."""
        cb, e = _call(tf.certificate_binding_problems, m, rec_of(dual, m))
        hit = [p for p in (cb or []) if p.startswith(ck + ':') and needle in p]
        chk(f'{label} · 증서 결합 사유 = {ck}: … {needle} … (예외 아님) — {(e or (hit[0] if hit else cb))!r:.200}', e is None and bool(hit))

    def mut(fn, src):
        d = copy.deepcopy(src)
        fn(d)
        return d

    def patched(make, spsolve=False, cg=False, gmres=False):
        """첫 단 spsolve 가 틀린 해 (0 벡터 → 증서 실패) · cg · gmres 미수렴 (info 1) 주입 → 실제 생산자 사다리가 다음 단 · 끝까지 실패."""
        old = {k: getattr(nc, k) for k in ('spsolve', 'cg', 'gmres')}
        if spsolve:
            nc.spsolve = lambda A_, b_: np.zeros(len(b_))
        if cg:
            nc.cg = lambda A_, b_, **k_: (np.zeros(len(b_)), 1)
        if gmres:
            nc.gmres = lambda A_, b_, **k_: (np.zeros(len(b_)), 1)
        try:
            return make()
        finally:
            for k, v in old.items():
                setattr(nc, k, v)

    # ── 실제 생산자 침대 ─────────────────────────────────────────────────────────────────────────────────────────
    B15 = chain_bed(1.5)                                          # FULL computed 셋 · CF model_over_conduction 셋 · 협착-only H0 computed · physics model_over_conduction
    L15 = ledger_of(B15)
    d15 = produce(nc, B15)
    B20 = chain_bed(2.0, area=3.2)                                # FULL computed 셋 · CF computed 셋 · 협착-only H0 computed · physics · H12 = not_computed 0 저항 (I_bottom None)
    L20 = ledger_of(B20)
    d20 = produce(nc, B20)
    _A, _C, _P, _X = chain_bed(1.5)
    Bnp = (_A, [c for c in _C if c['id1'] != 10], _P, _X)          # 10–11 접촉 하나를 뺀 사슬 = 관통 성분 없음 (세 모드 valid_zero)
    Lnp = ledger_of(Bnp)
    dnp = produce(nc, Bnp)
    B10 = chain_bed(1.0)                                          # physics FULL 모형 한계 (H0 computed)
    L10 = ledger_of(B10)
    d10 = produce(nc, B10)
    fb = {}

    def honest_ionic_certs():
        """(이름, 증서) — 해를 낸 이온 증서 전부 (게시 상태 · 모형 한계 가드) — 실제 생산자 침대 + fallback 성공."""
        srcs = [('상자 1.5', d15), ('상자 2.0 면적 3.2', d20), ('상자 1.0 (모형 한계)', d10)] + [(f'fallback {k}', v) for k, v in fb.items()]
        for lab, d in srcs:
            for m in MODES3:
                for ck in (FULL, CF, CO):
                    c = rec_of(d, m).get(ck)
                    if isinstance(c, dict) and c.get('status') in ('computed', 'model_over_conduction', 'over_conduction_guard'):
                        yield f'{lab} · {m} · {ck}', c

    try:
        # ══ H — 대조 (그대로여야) ════════════════════════════════════════════════════════════════════════════════
        def sH():
            pre = (all(rec_of(d15, m)['sigma_full_status'] == 'computed' for m in MODES3)
                   and all(rec_of(d15, m)['sigma_bulk_net_status'] == 'model_over_conduction' for m in MODES3)
                   and rec_of(d15, 'hertz')['sigma_constr_net_status'] == 'computed' and rec_of(d15, 'physics')['sigma_constr_net_status'] == 'model_over_conduction')
            chk('H1a 전제 — 상자 1.5 = FULL computed 셋 · CF model_over_conduction 셋 · 협착-only H0 computed · physics model_over_conduction (전부 게시 증서)', pre)
            for m in MODES3:
                expect(f'H1b 정상 게시 레코드 (상자 1.5 · {m})', d15, m, True, L15, 100.0)
            row = tf.ion_columns(d15, L15, 100.0)
            phi = L15['phi_se_mass_conserving']
            want = {m: phi / (rec_of(d15, m)['sigma_full'] * L15['thickness_um'] / L15['thickness_mass_conserving_um']) for m in MODES3}
            chk(f"H1c τ 값 그대로 — tau2 = φ_mc/f 세 모드 {[(m, row.get(f'tau2_ion_{m}')) for m in MODES3]}",
                all(row.get(f'ion_net_status_{m}') == 'OK' and row.get(f'tau2_ion_{m}') == want[m] for m in MODES3))
            co = {m: (rec_of(d20, m)['sigma_constr_net_status'], rec_of(d20, m)['sigma_constr_net_reason'], rec_of(d20, m)[CO].get('I_bottom'),
                      rec_of(d20, m)[CO].get('reason')) for m in MODES3}
            chk(f'H2a 전제 — 상자 2.0 면적 3.2 = FULL · CF computed 셋 · 협착-only H0 computed · physics · H12 not_computed 0 저항 (증서 I_bottom None · 사유 같음) {co}',
                all(rec_of(d20, m)['sigma_full_status'] == 'computed' and rec_of(d20, m)['sigma_bulk_net_status'] == 'computed' for m in MODES3)
                and co['hertz'][0] == 'computed'
                and all(co[m] == ('not_computed', nc.ZERO_RESISTANCE_REASON, None, nc.ZERO_RESISTANCE_REASON) for m in ('physics', 'hertz_h12')))
            for m in MODES3:
                expect(f'H2b 정직한 실패 가지 (협착-only 0 저항 · I_bottom None) 를 싣은 정상 레코드 (상자 2.0 · {m})', d20, m, True, L20, 100.0)
            chk('H3a 전제 — 비관통 사슬 = 세 모드 valid_zero · FULL 증서 I_bottom None · 시도 []',
                all(rec_of(dnp, m)['sigma_full_status'] == 'valid_zero' for m in MODES3)
                and rec_of(dnp, 'hertz')[FULL].get('I_bottom') is None and rec_of(dnp, 'hertz')[FULL].get('attempts') == [])
            for m in MODES3:
                expect(f'H3b 정직한 비관통 레코드 (valid_zero · {m})', dnp, m, True, Lnp, 0.0, tau_np)
            chk('H4a 전제 — 상자 1.0 = physics FULL 모형 한계 · H0 computed', rec_of(d10, 'physics')['sigma_full_reason'] == ML
                and rec_of(d10, 'hertz')['sigma_full_status'] == 'computed')
            expect('H4b FULL 모형 한계 레코드 (physics)', d10, 'physics', True, L10, 100.0, tau_ml)
            expect('H4c FULL 모형 한계 레코드의 H0', d10, 'hertz', True, L10, 100.0)
            for lab, kw, want_atts in (('spsolve 증서 실패 → cg+jacobi', dict(spsolve=True), [('spsolve', 'certificate_failed'), ('cg+jacobi', 'pass')]),
                                       ('spsolve 증서 실패 → cg+jacobi 미수렴 → gmres+ilu', dict(spsolve=True, cg=True),
                                        [('spsolve', 'certificate_failed'), ('cg+jacobi', 'not_converged'), ('gmres+ilu', 'pass')])):
                d = patched(lambda: produce(nc, B15), **kw)
                fb[lab] = d
                atts = {ck: [(a.get('method'), a.get('outcome')) for a in rec_of(d, 'hertz')[ck].get('attempts') or []] for ck in (FULL, CF, CO)}
                chk(f'H5a 전제 [{lab}] — 게시 증서 셋의 시도 {atts[FULL]} (CF · 협착-only 같음) · σ_ratio = 기준 침대와 같다',
                    all(v == want_atts for v in atts.values()) and all(rec_of(d, m)['sigma_full'] == rec_of(d15, m)['sigma_full'] for m in MODES3))
                for m in MODES3:
                    expect(f'H5b ★ 정상 fallback 성공 (앞 단 실패 기록 + 마지막 pass) [{lab} · {m}]', d, m, True, L15, 100.0)
            dfail = patched(lambda: produce(nc, B15), spsolve=True, cg=True, gmres=True)
            r = rec_of(dfail, 'hertz')
            irp = tf.ion_record_problem(r)
            row = tf.ion_columns(dfail, L15, 100.0)
            chk(f"H6 정직한 풀이 실패 (모든 단 실패 → not_computed {r.get('sigma_full_reason')!r} · σ None · 증서 I_bottom None) → 분류 그대로 = 0b solver_guard · "
                f"τ NOT_COMPUTED solver_guard — {irp!r:.100} · {(row.get('ion_net_status_hertz'), row.get('ion_net_status_reason_hertz'))}",
                r.get('sigma_full_status') == 'not_computed' and r.get('sigma_full_reason') == nc.CURRENT_CONSERVATION_FAILED_REASON
                and r.get('sigma_full') is None and r[FULL].get('I_bottom') is None
                and isinstance(irp, tuple) and irp[0] == 'solver_guard'
                and (row.get('ion_net_status_hertz'), row.get('ion_net_status_reason_hertz')) == ('NOT_COMPUTED', 'solver_guard'))
            bad = []
            n = 0
            for lab, c in honest_ionic_certs():
                n += 1
                atts = c.get('attempts')
                last = atts[-1] if isinstance(atts, list) and atts and isinstance(atts[-1], dict) else None
                krylov_ok = (last is not None and ((last.get('krylov_info') == 0 and type(last.get('krylov_info')) is int)
                                                   if last.get('method') in ('cg', 'cg+jacobi', 'gmres+ilu') else last.get('krylov_info') is None))
                if not (last is not None and last.get('outcome') == 'pass' and last.get('method') == c.get('method') and last.get('error') is None
                        and last.get('I_bottom') == c.get('I_bottom') and last.get('I_top') == c.get('I_top')
                        and last.get('conservation_rel') == c.get('conservation_rel') and last.get('residual_rel') == c.get('residual_rel')
                        and krylov_ok and all(a.get('outcome') != 'pass' for a in atts[:-1])):
                    bad.append(lab)
            chk(f'H7 생산자 증서 모양 (독립 오라클) — 해를 낸 이온 증서 {n} 개 (게시 · 모형 한계 · fallback) 전부 시도 목록이 비지 않고 마지막 = 그 해의 pass 단 '
                f'(방법 · 두 전류 · 보존 · 내부 잔차 = 요약 · 예외 없음 · Krylov 단 krylov_info int 0 · 그 밖 None · 앞 단 pass 없음) — 어긋남 {bad}',
                n >= 30 and not bad)

        _guard('H', sH)

        # ══ A — L214R-06 (Q4) 게시 증서의 채택 단 ═════════════════════════════════════════════════════════════════════
        Q4 = (('outcome certificate_failed', lambda c: c['attempts'][-1].update(outcome='certificate_failed')),
              ('residual_rel 1.0', lambda c: c['attempts'][-1].update(residual_rel=1.0)),
              ('conservation_rel 1.0', lambda c: c['attempts'][-1].update(conservation_rel=1.0)),
              ("error 'RuntimeError: x'", lambda c: c['attempts'][-1].update(error='RuntimeError: x')),
              ('method 다름 (gmres+ilu)', lambda c: c['attempts'][-1].update(method='gmres+ilu')),
              ('I_bottom ×2 (마지막 시도만)', lambda c: c['attempts'][-1].update(I_bottom=c['attempts'][-1]['I_bottom'] * 2)),
              ('attempts []', lambda c: c.update(attempts=[])),
              ('attempts 키 삭제', lambda c: c.pop('attempts')),
              ('직접해 (spsolve) 단 krylov_info 1', lambda c: c['attempts'][-1].update(krylov_info=1)))

        def sA():
            fn = getattr(nc, 'adopted_attempt_binding_problem', None)
            certs = list(honest_ionic_certs())
            chk(f'A0a ★ 공용 함수 network_conductivity.adopted_attempt_binding_problem 이 있고 해를 낸 이온 증서 {len(certs)} 개 전부 통과 (정직한 증서를 막지 않는다)',
                fn is not None and len(certs) >= 30 and all(fn(c) is None for _l, c in certs),
                [l_ for l_, c in certs if fn is not None and fn(c) is not None][:4])
            for lab, f in Q4:
                d = mut(lambda d_, f_=f: f_(d_['hertzian'][FULL]), d15)
                c = d['hertzian'][FULL]
                chk(f'A1-0 전제 [{lab}] — 요약은 그대로 (수치 증서 통과 · certificate_problem None)', nc.certificate_problem(c) is None)
                if fn is not None:
                    p = fn(c)
                    chk(f'A1-1 ★ [{lab}] 공용 함수 = 사유 · 예외 아님 — {p!r:.160}', isinstance(p, str) and p.startswith('채택 단 기록'))
                else:
                    chk(f'A1-1 ★ [{lab}] 공용 함수 = 사유 (함수 없음)', False)
                expect(f'A1 ★ H0 FULL 마지막 시도 {lab}', d, 'hertz', False, L15, 100.0)
                cb_reason(f'A1 ★ H0 FULL 마지막 시도 {lab}', d, 'hertz', FULL, '채택 단 기록')
            sites = (('H0 CF (model_over_conduction) · outcome certificate_failed', d15, L15, 'hertz', CF, Q4[0][1]),
                     ('H0 CF (model_over_conduction) · attempts []', d15, L15, 'hertz', CF, Q4[6][1]),
                     ('H0 CF (computed · 상자 2.0) · residual_rel 1.0', d20, L20, 'hertz', CF, Q4[1][1]),
                     ('H0 CF (computed · 상자 2.0) · krylov_info 1', d20, L20, 'hertz', CF, Q4[8][1]),
                     ('H0 협착-only (computed) · error', d15, L15, 'hertz', CO, Q4[3][1]),
                     ('H0 협착-only (computed) · method 다름', d15, L15, 'hertz', CO, Q4[4][1]),
                     ('physics 협착-only (model_over_conduction) · I_bottom ×2 (마지막 시도만)', d15, L15, 'physics', CO, Q4[5][1]),
                     ('physics 협착-only (model_over_conduction) · attempts 키 삭제', d15, L15, 'physics', CO, Q4[7][1]),
                     ('H12 FULL · conservation_rel 1.0', d15, L15, 'hertz_h12', FULL, Q4[2][1]),
                     ('physics FULL · outcome certificate_failed', d15, L15, 'physics', FULL, Q4[0][1]))
            for lab, src, led, m, ck, f in sites:
                d = mut(lambda d_, m_=m, ck_=ck, f_=f: f_(rec_of(d_, m_)[ck_]), src)
                chk(f'A2-0 전제 [{lab}] — 게시 상태 {rec_of(d, m)[ck]["status"]!r} · 요약 수치 증서 통과',
                    rec_of(d, m)[ck]['status'] in tf.CERT_PUBLISHED_STATES and nc.certificate_problem(rec_of(d, m)[ck]) is None)
                expect(f'A2 ★ {lab}', d, m, False, led, 100.0)
                cb_reason(f'A2 ★ {lab}', d, m, ck, '채택 단 기록')
            src = fb.get('spsolve 증서 실패 → cg+jacobi')
            if src is None:
                chk('A3 fallback 레코드 (H5 가 만든다) 없음', False)
                return
            for lab, f in (('fallback 마지막 pass (cg+jacobi) 의 krylov_info 1', lambda c: c['attempts'][-1].update(krylov_info=1)),
                           ('fallback 마지막 pass 시도를 뺌 (앞 단 실패가 마지막)', lambda c: c.update(attempts=c['attempts'][:-1]))):
                d = mut(lambda d_, f_=f: f_(d_['hertzian'][FULL]), src)
                expect(f'A3 ★ {lab}', d, 'hertz', False, L15, 100.0)
                cb_reason(f'A3 ★ {lab}', d, 'hertz', FULL, '채택 단 기록')

        _guard('A', sA)

        # ══ A4 — 모형 한계 증서 판정의 채택 단 문구 그대로 (같은 함수로 옮겨도 출력 바이트 불변) ═══════════════════════════════════════
        def sA4():
            c0 = d10['physics'][FULL]
            chk('A4-0 전제 — 상자 1.0 physics FULL 모형 한계 증서 · 시도 [(spsolve, pass)]',
                [(a.get('method'), a.get('outcome')) for a in c0['attempts']] == [('spsolve', 'pass')] and nc.model_limit_certificate_problem(c0) is None)
            c = copy.deepcopy(c0)
            c['attempts'][-1]['outcome'] = 'certificate_failed'
            want = ("채택 단 기록 — 마지막 시도 {'method': 'spsolve', 'outcome': 'certificate_failed'} 가 증서 방법 'spsolve' · "
                    '두 전류와 같은 pass 단이 아니다 (앞 단계 실패를 높은 q 로 구제하지 않는다)')
            got = nc.model_limit_certificate_problem(c)
            chk(f'A4a 모형 한계 증서 — 마지막 시도 outcome certificate_failed 의 사유 문구 그대로 — {got!r:.200}', got == want)
            c = copy.deepcopy(c0)
            c['attempts'][-1]['error'] = 'RuntimeError: x'
            want = "채택 단 기록 — 마지막 pass 시도가 요약과 같은 해가 아니다: 예외 기록 'RuntimeError: x' 이 있는데 pass — 사다리는 예외 단을 채택하지 않는다"
            got = nc.model_limit_certificate_problem(c)
            chk(f'A4b 모형 한계 증서 — 마지막 pass 시도 error 의 사유 문구 그대로 — {got!r:.200}', got == want)
            c = copy.deepcopy(c0)
            c['attempts'] = []
            got = nc.model_limit_certificate_problem(c)
            chk(f'A4c 모형 한계 증서 — 시도 [] 의 사유 문구 그대로 — {got!r:.200}',
                got == "채택 단 기록 — 마지막 시도 None 가 증서 방법 'spsolve' · 두 전류와 같은 pass 단이 아니다 (앞 단계 실패를 높은 q 로 구제하지 않는다)")

        _guard('A4', sA4)

        # ══ B — L214R-07 (Q5) 두 σ 표현 항등식의 유한성 ═════════════════════════════════════════════════════════════════
        def nonfinite(irp):
            return isinstance(irp, tuple) and irp[0] == 'invalid_input' and str(irp[1]).startswith(TAG)

        def sB():
            s0 = d15['hertzian']['sigma_grain_S_cm']

            def g2(q, sd, s0_=None):
                def fn(d):
                    r = d['hertzian']
                    r['sigma_full'], r['sigma_full_mScm'] = q, sd
                    if s0_ is not None:
                        r['sigma_grain_S_cm'] = s0_
                return mut(fn, d15)
            cases = (('B1 σ_ratio 1e308 · σ_dim 1.0 (Codex Q5 모양)', g2(1e308, 1.0)),
                     ('B2 σ_ratio 1e308 · σ_dim = float 최대 (1000·σ₀·σ_ratio 3e308 의 가장 가까운 표현 — "맞춘" 넘침 짝)', g2(1e308, sys.float_info.max)),
                     ('B3 곱 0 밑넘침 — σ₀ 1e−300 · σ_ratio 1e−300 · σ_dim 4e−7 (절대 반폭 5e−7 뒤)', g2(1e-300, 4e-7, 1e-300)))
            chk(f'B0 전제 — B1 · B2: 곱 = +∞ · |차| = 허용 = +∞ (inf ≤ inf) · B3: 곱 = 0.0 · |차| 4e−7 ≤ 허용 (σ₀ {s0!r})',
                math.isinf(1000.0 * s0 * 1e308) and math.isinf(tf.sigma_identity_tol(s0, 1e308, 1.0))
                and math.isinf(tf.sigma_identity_tol(s0, 1e308, sys.float_info.max))
                and 1000.0 * 1e-300 * 1e-300 == 0.0 and 4e-7 <= tf.sigma_identity_tol(1e-300, 1e-300, 4e-7))
            for lab, d in cases:
                irp, e = _call(tf.ion_record_problem, d['hertzian'])
                chk(f'{lab} ★ 0b (ion_record_problem) = (invalid_input, {TAG} …) · 예외 아님 — {e or irp!r:.200}', e is None and nonfinite(irp))
                expect(lab, d, 'hertz', False, L15, 100.0)
                row, e = _call(tf.ion_columns, d, L15, 100.0)
                rs = (row or {}).get('ion_net_status_reason_hertz')
                chk(f'{lab} ★ τ 행 사유 = 0b 의 invalid_input: {TAG} … (증서 결합 전에 0b 가 잡는다) — {e or rs!r:.160}',
                    e is None and str(rs).startswith(f'invalid_input: {TAG}'))
            d = json.loads(json.dumps(d15).replace(f'"sigma_full_mScm": {d15["hertzian"]["sigma_full_mScm"]!r}', '"sigma_full_mScm": 3e308', 1))
            chk(f'B4 JSON 글자 3e308 = float inf (넘침은 JSON 에서 이미 inf) → 0b 거부 그대로 (유한 양수여야) — {tf.ion_record_problem(d["hertzian"])!r:.120}',
                math.isinf(d['hertzian']['sigma_full_mScm']) and tf.ion_record_problem(d['hertzian']) is not None)
            q0 = d15['hertzian']['sigma_full']
            tol0 = tf.sigma_identity_tol(s0, q0, 1000.0 * s0 * q0)

            def sd_at(f):
                return tf.ion_record_problem(dict(d15['hertzian'], sigma_full_mScm=1000.0 * s0 * q0 + f * tol0))
            chk(f'B5 항등식 경계 그대로 — σ_dim = 1000·σ₀·q ± 0.9·허용 통과 · +1.1·허용 거부 (불일치 문구) · 생산자 기록 통과 — {sd_at(1.1)!r:.120}',
                sd_at(0.9) is None and sd_at(-0.9) is None and isinstance(sd_at(1.1), tuple) and '두 σ 표현 불일치' in sd_at(1.1)[1]
                and tf.ion_record_problem(d15['hertzian']) is None)

        _guard('B', sB)

        # ══ B — 옛 세대 레코드 (진짜 194 v1.2 역사 레코드 · inferred_legacy · 증서 없음) ══════════════════════════════════════════
        legacy_dir = os.path.join(tmp, 'legacy', 'lhs00_000')

        def sBL():
            os.makedirs(legacy_dir)
            with tarfile.open(ARCHIVE) as t:
                for mem in t.getmembers():
                    parts = mem.name.split('/')
                    if mem.isfile() and len(parts) > 2 and parts[1] == 'lhs00_000' and parts[-1] in (
                            'network_conductivity_dual.json', 'full_metrics.json', 'network_provenance.json'):
                        with t.extractfile(mem) as fh, open(os.path.join(legacy_dir, parts[-1]), 'wb') as out:
                            out.write(fh.read())
            dp = os.path.join(legacy_dir, 'network_conductivity_dual.json')
            with open(dp, encoding='utf-8') as f:
                dual0 = json.load(f)
            with open(os.path.join(legacy_dir, 'full_metrics.json'), encoding='utf-8') as f:
                fm = json.load(f)
            row0 = tf.case_row(legacy_dir)
            h = dual0['hertzian']
            want = fm['phi_se_mass_conserving'] / (h['sigma_full'] * fm['thickness_um'] / fm['thickness_mass_conserving_um'])
            chk(f"BL0 진짜 역사 레코드 (lhs00_000) = inferred_legacy · 증서 없음 · H0 OK tau2 {row0.get('tau2_ion_hertz')!r} (= φ_mc/f 그대로) · physics OK",
                row0.get('ion_net_generation') == 'inferred_legacy' and not any(k.startswith('solve_certificate') for k in h)
                and row0.get('ion_net_status_hertz') == 'OK' and row0.get('tau2_ion_hertz') == want and row0.get('ion_net_status_physics') == 'OK')

            def run(fn):
                d = copy.deepcopy(dual0)
                fn(d['hertzian'])
                with open(dp, 'w', encoding='utf-8') as f:
                    json.dump(d, f)
                return d, tf.case_row(legacy_dir)
            for lab, fn in (('BL1 σ_ratio 1e308 (σ_dim 그대로 — 고치기 전 τ = f ∞ · tau2 0)', lambda r: r.update(sigma_full=1e308)),
                            ('BL2 σ_ratio 1e308 · σ_dim = float 최대 ("맞춘" 넘침 짝)', lambda r: r.update(sigma_full=1e308, sigma_full_mScm=sys.float_info.max))):
                d, row = run(fn)
                irp = tf.ion_record_problem(d['hertzian'])
                st, rs = row.get('ion_net_status_hertz'), row.get('ion_net_status_reason_hertz')
                chk(f"{lab} ★ 옛 세대 폴더 행 (case_row) = NOT_COMPUTED invalid_input: {TAG} … · f · tau2 빈칸 (OK · 하한 표지 · f ∞ · tau2 0 아님) — "
                    f"{(st, str(rs)[:90], row.get('f_ion_hertz'), row.get('tau2_ion_hertz'))}",
                    row.get('ion_net_generation') == 'inferred_legacy' and st == 'NOT_COMPUTED' and str(rs).startswith(f'invalid_input: {TAG}')
                    and row.get('f_ion_hertz') is None and row.get('tau2_ion_hertz') is None and nonfinite(irp))
                o = tf.ion_columns(d, fm, fm.get('percolation_pct'))
                chk(f'{lab} ★ τ 행 (ion_columns · 같은 입력) 도 같은 거부 · physics 는 OK 그대로',
                    o.get('ion_net_status_hertz') == 'NOT_COMPUTED' and str(o.get('ion_net_status_reason_hertz')).startswith(f'invalid_input: {TAG}')
                    and o.get('ion_net_status_physics') == 'OK')
            d = json.loads(json.dumps(dual0).replace(f'"sigma_full": {h["sigma_full"]!r}', f'"sigma_full": {BIG_TXT}', 1))
            with open(dp, 'w', encoding='utf-8') as f:
                json.dump(d, f)
            row, e = _call(tf.case_row, legacy_dir)
            chk(f'BL3 ★ (L214R-08 d) 옛 세대 레코드 σ_ratio = JSON 정수 10⁴⁰⁰ → 폴더 행 NOT_COMPUTED invalid_input · 예외 아님 — {e or (row or {}).get("ion_net_status_reason_hertz")!r:.140}',
                e is None and isinstance(d['hertzian']['sigma_full'], int) and row.get('ion_net_status_hertz') == 'NOT_COMPUTED'
                and tf.reason_code(row.get('ion_net_status_reason_hertz')) == 'invalid_input' and row.get('tau2_ion_hertz') is None)
            with open(dp, 'w', encoding='utf-8') as f:
                json.dump(dual0, f)
            chk('BL4 되돌린 역사 레코드 = 처음 행 그대로', tf.case_row(legacy_dir) == row0)

        _guard('B legacy', sBL)

        # ══ D — L214R-08 (Q6) float 로 못 옮기는 큰 JSON 정수 ═══════════════════════════════════════════════════════════
        def sD():
            # (a) 숫자 없는 가지 증서의 I_bottom — None 은 '해 주장 없음' · 변환 불가 정수는 숫자가 실린 것 (해 주장) → 거부
            for lab, src, led, pp, m, path, tau_ok in (
                    ('Da1 비관통 (valid_zero) H0 FULL 증서 I_bottom', dnp, Lnp, 0.0, 'hertz', ['hertzian', FULL, 'I_bottom'], tau_np),
                    ('Da2 협착-only 0 저항 (not_computed) physics 증서 I_bottom', d20, L20, 100.0, 'physics', ['physics', CO, 'I_bottom'], tau_default)):
                d = with_big(src, path)
                cb, e = _call(tf.certificate_binding_problems, m, rec_of(d, m))
                chk(f'{lab} = 10⁴⁰⁰ ★ 증서 결합 사유 (그 자리 · 예외 아님 · "없음" 으로 읽지 않는다) — {e or cb!r:.180}',
                    e is None and any(p.startswith(path[1] + ':') for p in (cb or [])))
                expect(f'{lab} = 10⁴⁰⁰ ★', d, m, False, led, pp, tau_ok)
            # (b) 전자 · 열 증서 σ_bulk
            dsa = produce(nc, (lambda b: (b[0], b[1], b[2], 1.5))(se_am_ml_bed()), se=(1,), am=(2,), tm={1: 'SE', 2: 'AM_P'})
            chk('Db0 전제 — SE+AM 침대 (상자 1.5) 에 전자 FULL 증서 (σ_bulk = SIGMA_AM_ELECTRONIC) · 세 모드 통과',
                (dsa['hertzian'].get('electronic_solve_certificate_full') or {}).get('sigma_bulk_S_cm') == nc.SIGMA_AM_ELECTRONIC
                and all(tf.certificate_binding_problems(m, rec_of(dsa, m)) == [] for m in MODES3))
            for lab, src, led, path in (('Db1 열 FULL 증서 σ_bulk (상자 1.5 · H0)', d15, L15, ['hertzian', 'thermal_solve_certificate_full', 'sigma_bulk_S_cm']),
                                        ('Db2 전자 FULL 증서 σ_bulk (SE+AM · H0)', dsa, ledger_of((lambda b: (b[0], b[1], b[2], 1.5))(se_am_ml_bed())),
                                         ['hertzian', 'electronic_solve_certificate_full', 'sigma_bulk_S_cm'])):
                d = with_big(src, path)
                v, e = _call(tf.sigma0_binding_problems, d['hertzian'])
                chk(f'{lab} = 10⁴⁰⁰ ★ σ₀ 결합 사유 (그 증서 자리 · 예외 아님) — {e or v!r:.160}',
                    e is None and any(p.startswith(path[1] + ':') for p in (v or [])))
                expect(f'{lab} = 10⁴⁰⁰ ★', d, 'hertz', False, led, 100.0)
            # (c) 모형 한계 증서 σ_bulk · 모형 한계 레코드의 σ₀
            for lab, path in (('Dc1 모형 한계 physics FULL 증서 σ_bulk', ['physics', FULL, 'sigma_bulk_S_cm']),
                              ('Dc2 모형 한계 physics 레코드 σ₀ (sigma_grain_S_cm)', ['physics', 'sigma_grain_S_cm'])):
                d = with_big(d10, path)
                mp, e = _call(tf.full_model_limit_problem, d['physics'], 'ionic', 'physics')
                irp, e2 = _call(tf.ion_record_problem, d['physics'])
                cv, e3 = _call(ps.channel_verdict, d['physics'], 'ionic', 'physics')
                chk(f'{lab} = 10⁴⁰⁰ ★ 공용 판정 사유 · 0b invalid_input · 채널 판정 fail (예외 문구 아님) — {e or mp!r:.120} · {e3 or cv!r:.100}',
                    e is None and isinstance(mp, str) and 'σ₀' in mp and e2 is None and isinstance(irp, tuple) and irp[0] == 'invalid_input'
                    and e3 is None and cv[0] == 'fail' and 'Error' not in str(cv[1]))
                expect(f'{lab} = 10⁴⁰⁰ ★', d, 'physics', False, L10, 100.0, tau_ml)
            # (d) 레코드 값 (공용 기술 검사)
            for lab, src, led, pp, path, tau_ok in (('Dd1 H0 σ_ratio (sigma_full)', d15, L15, 100.0, ['hertzian', 'sigma_full'], tau_default),
                                                    ('Dd2 H0 σ_dim (sigma_full_mScm)', d15, L15, 100.0, ['hertzian', 'sigma_full_mScm'], tau_default),
                                                    ('Dd3 H0 관통 분율', d15, L15, 100.0, ['hertzian', 'percolating_fraction'], tau_default),
                                                    ('Dd4 H0 σ₀ (sigma_grain_S_cm)', d15, L15, 100.0, ['hertzian', 'sigma_grain_S_cm'], tau_default),
                                                    ('Dd5 비관통 (valid_zero) H0 관통 분율', dnp, Lnp, 0.0, ['hertzian', 'percolating_fraction'], tau_np)):
                d = with_big(src, path)
                irp, e = _call(tf.ion_record_problem, d['hertzian'])
                chk(f'{lab} = 10⁴⁰⁰ ★ 0b = (invalid_input, 사유) · 예외 아님 — {e or irp!r:.140}',
                    e is None and isinstance(irp, tuple) and irp[0] == 'invalid_input')
                if path[-1] == 'percolating_fraction':
                    #  τ 행은 관통 분율을 0b 앞에서 읽는다 (입력 결손 게이트 0) → NOT_COMPUTED missing_input 도 거부 (예외 아님)
                    row, e = _call(tf.ion_columns, d, led, pp)
                    chk(f'{lab} = 10⁴⁰⁰ ★ τ 행 NOT_COMPUTED (예외 아님) — {e or (row or {}).get("ion_net_status_hertz")!r}',
                        e is None and row.get('ion_net_status_hertz') == 'NOT_COMPUTED' and row.get('tau2_ion_hertz') is None)
                    for k, (acc, det) in verdicts(d, 'hertz', led, pp, tau_ok).items():
                        if k != 'τ 행':
                            chk(f'{lab} = 10⁴⁰⁰ ★ · {k} = 거부', acc is False, det)
                else:
                    expect(f'{lab} = 10⁴⁰⁰ ★', d, 'hertz', False, led, pp, tau_ok)
            # 같은 소비 경로의 다른 자리 — 온도 규약 T_C · τ 장부 · 등급 τ getter
            d = with_big(d15, ['hertzian', 'temperature_provenance', 'T_C'])
            v, e = _call(tf.sigma0_convention_problem, d['hertzian'])
            chk(f'De1 H0 온도 규약 T_C = 10⁴⁰⁰ ★ 규약 사유 (유한 수가 아니다) · 예외 아님 — {e or v!r:.140}', e is None and isinstance(v, str) and 'T_C' in v)
            expect('De1 H0 온도 규약 T_C = 10⁴⁰⁰ ★', d, 'hertz', False, L15, 100.0)
            led_big = json.loads(json.dumps(dict(L15, thickness_um='__X__')).replace('"__X__"', BIG_TXT))
            row, e = _call(tf.ion_columns, d15, led_big, 100.0)
            chk(f'De2 τ 장부 thickness_um = 10⁴⁰⁰ ★ τ 행 세 모드 NOT_COMPUTED (입력 무효 · 값 빈칸) · 예외 아님 — {e or [(row or {}).get(f"ion_net_status_{m}") for m in MODES3]}',
                e is None and all(row.get(f'ion_net_status_{m}') == 'NOT_COMPUTED' and row.get(f'tau2_ion_{m}') is None for m in MODES3))
            met = json.loads(json.dumps({'phi_se': 0.3, 'sigma_full_mScm': '__X__'}).replace('"__X__"', BIG_TXT))
            v, e = _call(tf.tau2_from_metrics, met)
            chk(f'De3 등급 τ getter (tau2_from_metrics) σ = 10⁴⁰⁰ → tau2 None (값 없음) · 예외 아님 — {e or v!r:.80}',
                e is None and isinstance(v, tuple) and v[0] is None)

        _guard('D', sD)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print(f'\ntest_l214r06_same_class: {_ok}/{_ok + len(_fail)} PASS' + (f'   FAILED: {len(_fail)}' if _fail else ''))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
