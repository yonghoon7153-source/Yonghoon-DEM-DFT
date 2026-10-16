#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L214R-01 — FULL 모형 한계 수치 증서 (`network_conductivity.model_limit_certificate_problem`) 의 비유한 재구성 · 채택 단 모순 반례 (상주 시험).

  python3 scripts/test_l214r01_certificate.py          # 종료코드 0 = 전부 PASS

근거 = Codex 재검증 판정 `docs/reviews/codex_review_lhs214_fix_reverify_20261015.md` §2 (반례 A · B) · §6 행 2 · 9 · §9-1 ·
수정 계획 `docs/reviews/lhs214r_fix_plan_20261016.md` §1 L214R-01 A · B (1저자 비준 Q1 = 생산자 수용 상수를 그대로 · 새 문턱 없음).
반례 탐침 `docs/reviews/codex_lhs214_fix_reverify_evidence_20261015/probes/l214_numeric.py` 를 이 시험이 부르지는 않는다 (탐침은 리포 밖 고정 사본 배치를 전제) —
같은 변이를 우리 시험으로 다시 만든다.

★ 시험 먼저 — 고치기 전 코드에서 반례 묶음이 빨갛다 (q_rec = +∞ 를 `inf <= inf` 로 통과 · 넘친 T/A 와의 G→q 대조도 `inf <= inf` · 마지막 pass 시도의
  잔차 · 보존 · krylov_info · 예외를 안 본다 · scale² 넘침 · 큰 정수 = 사유가 아니라 예외).
  A  유한 입력의 중간 넘침 → 기술 실패 사유 (non_finite …) · 예외 아님
     A1 21 노드 생산자 physics 모형 한계 레코드 — 증서 전류 1e308 · −1e308 · Σg 1e308 (마지막 pass 시도 전류도 맞춤) · T 20 · A 1 → q_rec = (I_b·T)/A = +∞ ·
        저장 q 유한 그대로 (Codex 반례 A)
     A2 같은 레코드 — 실행의 모든 증서 기하를 T = 20·2¹⁰¹⁹ · A = 2¹⁰¹⁹ 로 (T/A = 20 정확히 그대로 · 봉인된 기하 · 다른 증서 재구성 그대로) · 모형 한계 증서 전류 2 ·
        q_withheld 40 (= 2·T/A 수학값 — 모든 입력 유한 · 서로 맞음) → 같은 순서의 (2·T)/A 가 넘친다 (Codex 'T = A = 1e308' 반례를 레코드 소비자까지)
     A3 3 노드 실제 풀이 증서 — T = A = 1e308 (Codex 반례 그대로) · scale 1e200 (scale² OverflowError) · T/A 넘침 (T 1e300 · A 1e−10) · T/A 밑넘침 ·
        큰 정수 (JSON 정수 10⁴⁰⁰ — 기하 · 전류 · q · Σg)
  B  채택 단 모순 — 같은 레코드의 마지막 pass 시도 한 칸만: residual_rel 1.0 · conservation_rel 1.0 · krylov_info 1 (Codex 반례 B — 레코드 소비자 전부) +
     residual_rel NaN · error 있음 · 문턱 안이지만 요약과 다른 잔차 · 직접해 단의 krylov_info 0 · Krylov 단 (cg+jacobi) 의 krylov_info None · False · 1 · −1
  C  대조 (그대로여야):
     C1 실제 생산자 정상 모형 한계 레코드 (`test_lhs214_model_limit` 의 생산자 경로) → 소비자 전부 통과 · 3 노드 실제 증서 (solve_info · 결과 증서)
     C2 사다리 fallback 성공 — 첫 단 spsolve 증서 실패 (주입) + cg+jacobi pass · spsolve 증서 실패 + Krylov 미수렴 (주입) + gmres+ilu pass (3 노드) ·
        레코드 단 (spsolve 증서 실패 주입 · 모든 풀이가 cg+jacobi 로) → 소비자 전부 통과 · 사다리 여섯 단 (none_free · spsolve · cg (자유 > 30,000) ·
        spsolve_fallback · cg+jacobi · gmres+ilu) 각각의 실제 모형 한계 증서 통과 (방법별 수렴 상태 규칙 = 생산자가 실제로 싣는 모양)
     C3 이미 거부되던 변이 (마지막 시도 outcome certificate_failed · 마지막 전류 다름) → 소비자 전부 거부 그대로
     C4 경계 그대로 — q = 1.5 정확 = computed · 다음 수 = 모형 한계 · q_withheld +16 ulp 통과 · +17 ulp 거부 (16ε) · 문턱 1.5 · 사다리 수용 상수 1e−6
소비자 (레코드 단 아홉) — 증서 판정 · 생산자 상태 (`_net_sigma_status` — 같은 증서 판정) · 공용 판정 (`full_model_limit_problem`) · 0b (`ion_record_problem`) ·
  0b∧증서 결합 (`certificate_binding_problems`) · 0b∧세대 계약 (`network_generation_contract` = 다시 읽기 K2) · 채널 판정 (`channel_verdict`) ·
  내용 판정 (`network_content_verdict` — 모드 파일) · τ 행 (`ion_columns`).
  ⚠ 증서 결합 · 세대 계약은 **0b 위임**이다 — `certificate_binding_problems` 는 공용 기술 검사 (`ion_record_problem`) 가 거부한 레코드에 [] 를 돌려주는 계약
    (그 docstring: 모든 소비처가 0b 로 먼저 거부한다) · 세대 계약은 표기 + 그 결합 (Codex 판정 §6 행 6 이 K2 의 0b 위임에 동의 — K4 · K6 · P4 가 붙는 경로) →
    둘은 0b 와의 **합성 관문**으로 판정한다 (고치기 전: 합성 관문도 받아들인다 = 반례가 산다).
⚠ 범위 — 합성 회로 · 합성 사슬 (φ_SE > 1 인 합성 기하 포함) 위의 계약 시험이다.  실제 침대에서 1e308 전류가 난다는 주장이 아니다.
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

ML = 'full_over_conduction'
TAG = 'non_finite'
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
    """→ (값, None) | (None, '예외 이름: 내용') — 판정 함수가 사유 대신 예외를 내면 그것도 기록한다 (A 의 요구 = 사유)."""
    try:
        return fn(*a, **kw), None
    except Exception as e:                                       # noqa: BLE001
        return None, f'{type(e).__name__}: {e}'


def main():
    import numpy as np
    import network_conductivity as nc
    import tau_flux as tf
    import pipeline_service as ps
    #  실제 생산자 경로 = test_lhs214_model_limit 의 것 그대로 (사슬 침대 · 두 모드 · JSON 왕복 = 디스크 모양 · 3 노드 회로) — 복제하지 않는다 (규율 ①)
    from test_lhs214_model_limit import chain_bed, ledger_of, net3, produce, quiet

    B1 = chain_bed(1.0)
    LED = ledger_of(B1)
    dual0 = produce(nc, B1)
    tmp = tempfile.mkdtemp(prefix='l214r01_')

    # ── 소비자 아홉 (레코드 단) ─────────────────────────────────────────────────────────────────────────────────────
    def verdicts(dual):
        """dual (hertzian · physics — physics 가 시험 레코드) → {소비자: (받아들였나 True/False · 예외면 None, 세부)}.
        받아들임 = 그 소비자가 physics 이온 FULL 의 모형 한계 주장을 유효로 받았다 (반례 = 거부여야 · 대조 = 받아야)."""
        rec = dual['physics']
        cert = rec.get('solve_certificate_full')
        out = {}
        v, e = _call(nc.model_limit_certificate_problem, cert)
        out['증서'] = (None if e else v is None, e or v)
        v, e = _call(nc._net_sigma_status, None, False, cert, channel='ionic')
        out['생산자 상태'] = (None if e else v == ('not_computed', ML), e or v)
        v, e = _call(tf.full_model_limit_problem, rec, 'ionic', 'physics')
        out['공용 판정'] = (None if e else v is None, e or v)
        irp, e0 = _call(tf.ion_record_problem, rec)
        out['0b'] = (None if e0 else irp is None, e0 or irp)
        v, e = _call(tf.certificate_binding_problems, 'physics', rec)
        out['0b∧증서 결합'] = (None if (e or e0) else (irp is None and v == []), e or e0 or (irp, v))
        v, e = _call(tf.network_generation_contract, dual)
        out['0b∧세대 계약 (K2)'] = (None if (e or e0) else (irp is None and v.get('generation') == 'g2' and not v.get('problems')),
                                e or e0 or (irp, (v or {}).get('generation'), (v or {}).get('problems')))
        v, e = _call(ps.channel_verdict, rec, 'ionic', 'physics')
        out['채널 판정'] = (None if e else v[0] == 'ok', e or v)
        for n_, r_ in (('hertzian', dual['hertzian']), ('physics', rec)):
            with open(os.path.join(tmp, f'network_conductivity_{n_}.json'), 'w') as f:
                json.dump(r_, f)
        v, e = _call(ps.network_content_verdict, tmp)
        out['내용 판정'] = (None if e else bool(v[0]), e or v)
        v, e = _call(tf.ion_columns, dual, LED, 100.0)
        if e:
            out['τ 행'] = (None, e)
        else:
            st, rs = v.get('ion_net_status_physics'), v.get('ion_net_status_reason_physics')
            acc = st == 'NOT_COMPUTED' and rs == ML
            rej = st == 'NOT_COMPUTED' and tf.reason_code(rs) == 'invalid_input'
            out['τ 행'] = (True if acc else (False if rej else None), (st, rs))
        return out

    def expect(label, dual, accept):
        """아홉 소비자 각각 — accept=True 면 받아들여야 · False 면 예외 없이 거부해야."""
        for k, (acc, det) in verdicts(dual).items():
            want = 'accept' if accept else 'reject'
            chk(f'{label} · {k} = {"통과" if accept else "거부"}', acc is accept, f'{want} 기대 · 얻음 {acc!r} · {det!r}')

    def mut(fn, src=None):
        d = copy.deepcopy(src if src is not None else dual0)
        fn(d)
        return d

    def fcert(d):
        return d['physics']['solve_certificate_full']

    def all_certs(dual):
        """한 실행의 모든 증서 (Hertz · H12 · physics × 이온 · 전자 · 열 × 세 가지) — 봉인된 기하 대조 (`_cert_geometry_problems`) 와 같은 범위."""
        h = dual.get('hertzian') or {}
        for rec in (h, h.get('hertz_h12'), dual.get('physics')):
            if not isinstance(rec, dict):
                continue
            for pre in ('',) + tf.CHANNEL_PREFIXES:
                for k in nc.SOLVE_CERTIFICATE_KEYS:
                    c = rec.get(pre + k)
                    if isinstance(c, dict) and 'geometry' in c:
                        yield c

    try:
        # ══ C1 대조 — 실제 생산자 정상 모형 한계 레코드 ══════════════════════════════════════════════════════════
        def sC1():
            c0 = fcert(dual0)
            chk(f"C1a 기준 레코드 = 실제 생산자 physics FULL 모형 한계 (q_withheld {c0.get('q_withheld')!r} · 방법 {c0.get('method')!r} · 시도 "
                f"{[(a.get('method'), a.get('outcome')) for a in c0.get('attempts') or []]})",
                dual0['physics'].get('sigma_full_reason') == ML and c0.get('status') == 'over_conduction_guard' and c0.get('q_withheld', 0) > 1.5)
            expect('C1b 정상 모형 한계 레코드', dual0, True)
            net = net3()
            quiet(nc.solve_network, net, mode='full')
            info = net['solve_info']['full']
            cert = nc.solve_certificate(info, {'channel': 'ionic', 'role': 'H0', 'contact_mode': 'hertzian', 'sigma_bulk_S_cm': 0.003})
            chk('C1c 3 노드 실제 증서 (q = 2) — solve_info · 결과 증서 둘 다 증서 판정 통과 · 생산자 상태 = 모형 한계',
                nc.model_limit_certificate_problem(info) is None and nc.model_limit_certificate_problem(cert) is None
                and nc._net_sigma_status(None, False, info, channel='ionic') == ('not_computed', ML))

        _guard('C1', sC1)

        # ══ A1 · A2 — 유한 입력의 중간 넘침 (레코드 소비자 전부) ══════════════════════════════════════════════════════
        def sA12():
            def a1(d):
                c = fcert(d)
                c.update(I_bottom=1e308, I_top=-1e308, sum_g=1e308)
                c['attempts'][-1].update(I_bottom=1e308, I_top=-1e308)
            d1 = mut(a1)
            g = fcert(d1)['geometry']
            chk('A1a 전제 — 기하 T 20 · A 1 (유한) · 같은 순서 재구성 (I_b/ΔV)·T/A 가 +∞ 로 넘친다 · 저장 q 는 유한 그대로',
                g['plate_z'] * g['scale'] == 20.0 and g['box_x'] * g['box_y'] * g['scale'] ** 2 == 1.0
                and math.isinf((1e308 / 1.0) * 20.0 / 1.0) and math.isfinite(fcert(d1)['q_withheld']))
            p1, e1 = _call(nc.model_limit_certificate_problem, fcert(d1))
            chk(f'A1b ★ 증서 판정 = 기술 실패 사유 ({TAG} …) · 예외 아님 — {e1 or p1!r:.200}',
                e1 is None and isinstance(p1, str) and p1.startswith(TAG))
            expect('A1c ★ 전류 1e308 넘침 레코드', d1, False)

            G = {'plate_z': 20.0 * 2.0 ** 1019, 'box_x': 2.0 ** 509, 'box_y': 2.0 ** 510, 'scale': 1.0}

            def a2(d):
                for c in all_certs(d):
                    c['geometry'] = dict(G)
                c = fcert(d)
                c.update(I_bottom=2.0, I_top=-2.0, conservation_rel=0.0, q_withheld=40.0)
                c['attempts'][-1].update(I_bottom=2.0, I_top=-2.0, conservation_rel=0.0)
            d2 = mut(a2)
            T, A = G['plate_z'] * G['scale'], G['box_x'] * G['box_y'] * G['scale'] ** 2
            chk('A2a 전제 — T = 20·2¹⁰¹⁹ · A = 2¹⁰¹⁹ 유한 · T/A = 20 정확히 (g_to_q 그대로) · 다른 증서 전류 < 0.4 (넘치지 않음) · 모형 한계 증서 (2·T)/A = +∞ ·'
                f' 수학값 2·20 = 40 = 저장 q · Σg {fcert(d2)["sum_g"]!r} ≥ 2/1.1',
                math.isfinite(T) and math.isfinite(A) and T / A == 20.0 and fcert(d2)['g_to_q'] == 20.0
                and all(c.get('I_bottom') is None or c['I_bottom'] < 0.4 for c in all_certs(dual0))
                and math.isinf((2.0 / 1.0) * T / A) and fcert(d2)['sum_g'] * 1.1 >= 2.0)
            p2, e2 = _call(nc.model_limit_certificate_problem, fcert(d2))
            chk(f'A2b ★ 증서 판정 = 기술 실패 사유 ({TAG} …) · 예외 아님 — {e2 or p2!r:.200}',
                e2 is None and isinstance(p2, str) and p2.startswith(TAG))
            expect('A2c ★ 봉인된 기하 T · A ≈ 1e308 넘침 레코드', d2, False)

        _guard('A1–A2', sA12)

        # ══ A3 — 3 노드 실제 풀이 증서의 넘침 · 밑넘침 · 큰 정수 (증서 판정 · 생산자 상태) ══════════════════════════════════
        def sA3():
            net = net3()
            quiet(nc.solve_network, net, mode='full')
            info = net['solve_info']['full']
            base = json.loads(json.dumps(nc.solve_certificate(info, {'channel': 'ionic', 'role': 'H0', 'contact_mode': 'hertzian',
                                                                      'sigma_bulk_S_cm': 0.003})))
            cases = {
                'A3a T = A = 1e308 (plate_z 1e308 · 상자 1e154 × 1e154 · T/A = 1 그대로 — Codex 반례)': dict(plate_z=1e308, box_x=1e154, box_y=1e154),
                'A3b scale 1e200 (scale² = Python float OverflowError)': dict(scale=1e200),
                'A3c T/A 넘침 (T 1e300 · A 1e−10 — 둘 다 유한 양수 · g_to_q 1 그대로)': dict(plate_z=1e300, box_x=1e-5, box_y=1e-5),
                'A3d T/A 밑넘침 (T 1e−300 · A 1e100 → 0)': dict(plate_z=1e-300, box_x=1e50, box_y=1e50),
            }
            for label, geo in cases.items():
                for form, src in (('solve_info', info), ('결과 증서', base)):
                    c = copy.deepcopy(src)
                    c['geometry'].update(geo)
                    p, e = _call(nc.model_limit_certificate_problem, c)
                    s, es = _call(nc._net_sigma_status, None, False, c, channel='ionic')
                    chk(f'{label} [{form}] ★ 증서 판정 = {TAG} 사유 · 예외 아님 · 생산자 상태 ≠ 모형 한계 — {e or p!r:.160} · {es or s!r}',
                        e is None and isinstance(p, str) and p.startswith(TAG) and es is None and s != ('not_computed', ML))
            big = 10 ** 400
            huge = {'기하 plate_z': lambda c: c['geometry'].update(plate_z=big), '기하 scale': lambda c: c['geometry'].update(scale=big),
                    'I_bottom': lambda c: c.update(I_bottom=big), 'q_withheld': lambda c: c.update(q_withheld=big),
                    'sum_g': lambda c: c.update(sum_g=big)}
            got = {}
            for label, fn in huge.items():
                c = json.loads(json.dumps(base))
                fn(c)
                c = json.loads(json.dumps(c))                     # JSON 정수 10⁴⁰⁰ 그대로 (표준 JSON 이 싣는 값)
                got[label] = _call(nc.model_limit_certificate_problem, c)
            chk(f'A3e ★ 큰 정수 (JSON 10⁴⁰⁰ — float 로 못 옮김) 다섯 칸 → 증서 판정 = 사유 · 예외 아님 (기준 3 노드 증서는 통과) '
                f'{ {k: str(e or p)[:70] for k, (p, e) in got.items()} }',
                nc.model_limit_certificate_problem(base) is None
                and all(e is None and isinstance(p, str) and bool(p) for p, e in got.values()))

        _guard('A3', sA3)

        # ══ B — 채택 단 (마지막 pass 시도) ↔ 요약 결합 ═══════════════════════════════════════════════════════════════
        def sB():
            for key, val in (('residual_rel', 1.0), ('conservation_rel', 1.0), ('krylov_info', 1)):
                d = mut(lambda d_, k=key, v=val: fcert(d_)['attempts'][-1].update({k: v}))
                p, e = _call(nc.model_limit_certificate_problem, fcert(d))
                chk(f'B1 ★ 마지막 pass 시도 {key} = {val!r} (요약은 정상) → 증서 판정 사유 · 예외 아님 — {e or p!r:.200}',
                    e is None and isinstance(p, str) and bool(p))
                expect(f'B2 ★ 마지막 시도 {key} {val!r} 레코드', d, False)
            res0 = fcert(dual0)['residual_rel']
            extra = {'residual_rel NaN': lambda d_: fcert(d_)['attempts'][-1].update(residual_rel=float('nan')),
                     'error 있음 (pass 인데 예외 기록)': lambda d_: fcert(d_)['attempts'][-1].update(error='RuntimeError: 주입'),
                     'residual_rel 9e−7 (문턱 안 · 요약과 다름)': lambda d_: fcert(d_)['attempts'][-1].update(residual_rel=9e-7),
                     '직접해 (spsolve) 의 krylov_info 0 (사다리는 직접해에 싣지 않는다)': lambda d_: fcert(d_)['attempts'][-1].update(krylov_info=0)}
            chk(f'B3 전제 — 기준 요약 잔차 {res0!r} ≠ 9e−7 · 마지막 시도 = spsolve pass · krylov_info None',
                res0 != 9e-7 and fcert(dual0)['attempts'][-1]['method'] == 'spsolve' and fcert(dual0)['attempts'][-1]['krylov_info'] is None)
            for label, fn in extra.items():
                d = mut(fn)
                p, e = _call(nc.model_limit_certificate_problem, fcert(d))
                ok_c, why_c = verdicts(d)['내용 판정']
                chk(f'B4 ★ 마지막 시도 {label} → 증서 판정 사유 · 내용 판정 (모드 파일) 거부 — {e or p!r:.140} · {why_c!r:.80}',
                    e is None and isinstance(p, str) and bool(p) and ok_c is False)

        _guard('B', sB)

        # ══ C2 — 사다리 fallback 성공 (앞 단 실패 + 마지막 pass) 은 통과 그대로 · Krylov 단의 수렴 상태 결합 ══════════════════════════
        def faulted(make_net, bad_cg=False):
            """첫 단 spsolve 가 틀린 해 (0 벡터 → 증서 실패) · bad_cg 면 cg 도 미수렴 (info 1) → 실제 생산자 사다리가 다음 단으로 간다."""
            old = {k: getattr(nc, k) for k in ('spsolve', 'cg')}
            nc.spsolve = lambda A_, b_: np.zeros(len(b_))
            if bad_cg:
                nc.cg = lambda A_, b_, **k_: (np.zeros(len(b_)), 1)
            try:
                return make_net()
            finally:
                for k, v in old.items():
                    setattr(nc, k, v)

        def run3():
            """3 노드 회로를 실제 solve_network 로 풀고 망 dict 를 돌려준다 (solve_info 가 실린다)."""
            n = net3()
            quiet(nc.solve_network, n, mode='full')
            return n

        dual_fb = {}

        def sC2():
            for label, bad_cg, want in (('C2a spsolve 증서 실패 → cg+jacobi pass', False, ['spsolve', 'cg+jacobi']),
                                        ('C2b spsolve 증서 실패 → cg+jacobi 미수렴 → gmres+ilu pass', True, ['spsolve', 'cg+jacobi', 'gmres+ilu'])):
                info = faulted(run3, bad_cg)['solve_info']['full']
                atts = info.get('attempts') or []
                cert = json.loads(json.dumps(nc.solve_certificate(info, {'channel': 'ionic', 'role': 'H0', 'contact_mode': 'hertzian',
                                                                          'sigma_bulk_S_cm': 0.003})))
                chk(f"{label} (3 노드 · 실제 사다리) — 시도 {[(a.get('method'), a.get('outcome'), a.get('krylov_info')) for a in atts]} · "
                    '마지막 Krylov pass 의 krylov_info = 0 (int) · 증서 판정 통과 (solve_info · 결과 증서) · 생산자 상태 = 모형 한계',
                    [a.get('method') for a in atts] == want and atts[-1].get('outcome') == 'pass' and atts[-1].get('krylov_info') == 0
                    and type(atts[-1].get('krylov_info')) is int and all(a.get('outcome') != 'pass' for a in atts[:-1])
                    and nc.model_limit_certificate_problem(info) is None and nc.model_limit_certificate_problem(cert) is None
                    and nc._net_sigma_status(None, False, info, channel='ionic') == ('not_computed', ML))
            dual_fb['d'] = faulted(lambda: produce(nc, B1))
            cf = fcert(dual_fb['d'])
            chk(f"C2c 레코드 단 fallback (모든 풀이가 spsolve 증서 실패 → cg+jacobi) — physics FULL 시도 "
                f"{[(a.get('method'), a.get('outcome'), a.get('krylov_info')) for a in cf.get('attempts') or []]} · q_withheld {cf.get('q_withheld')!r}",
                [(a.get('method'), a.get('outcome')) for a in cf.get('attempts') or []] == [('spsolve', 'certificate_failed'), ('cg+jacobi', 'pass')]
                and cf.get('method') == 'cg+jacobi' and cf.get('q_withheld', 0) > 1.5)
            expect('C2d ★ fallback 성공 레코드 (앞 단 실패 기록 + 마지막 pass)', dual_fb['d'], True)
            got = {}
            for label, val in (('None', None), ('False', False), ('1', 1), ('-1', -1)):
                d = mut(lambda d_, v=val: fcert(d_)['attempts'][-1].update(krylov_info=v), src=dual_fb['d'])
                got[label] = _call(nc.model_limit_certificate_problem, fcert(d))
            chk(f'C2e ★ Krylov 단 (cg+jacobi) pass 의 krylov_info None · False · 1 · −1 → 증서 판정 사유 · 예외 아님 (사다리: Krylov 단은 늘 int 를 싣고 0 이 '
                f'아니면 not_converged — 수렴 상태 없음 · bool · 미수렴) {[(k, str(e or p)[:50]) for k, (p, e) in got.items()]}',
                all(e is None and isinstance(p, str) and bool(p) for p, e in got.values()))

            #  C2f — 사다리 여섯 단 전부 실제 생산자 출력으로: 방법별 수렴 상태 규칙 (Krylov 단 = int 0 · 그 밖 = None) 이 생산자가 실제로 싣는 모양과 같은가
            def wide(n_free=30005):                            # 자유 노드마다 두 전극에 직접 — L_ff 대각 (첫 단 cg 가 바로 수렴) · G = n/2 · T/A 1e−4 → q 1.50025
                ed = []
                for k in range(n_free):
                    ed += [{'id1': 0, 'id2': 2 + k, 'R_total': 1.0, 'R_bulk': 0.4, 'R_constriction': 0.6},
                           {'id1': 2 + k, 'id2': 1, 'R_total': 1.0, 'R_bulk': 0.4, 'R_constriction': 0.6}]
                return {'nodes': set(range(n_free + 2)), 'bottom': {0}, 'top': {1}, 'scale': 1.0, 'plate_z': 1.0, 'box_x': 100.0, 'box_y': 100.0,
                        'edges': ed}

            def direct_pair():                                 # 자유 노드 0 — 바닥 · 위 띠가 한 간선 (none_free) · G 4 · q 4
                return {'nodes': {0, 1}, 'bottom': {0}, 'top': {1}, 'scale': 1.0, 'plate_z': 1.0, 'box_x': 1.0, 'box_y': 1.0,
                        'edges': [{'id1': 0, 'id2': 1, 'R_total': 0.25, 'R_bulk': 0.1, 'R_constriction': 0.15}]}

            def solved(make, cg_fail=False):
                old = nc.cg
                if cg_fail:                                    # 첫 단 cg 미수렴 (주입) → spsolve_fallback (자유 ≤ 250,000)
                    nc.cg = lambda A_, b_, **k_: (np.zeros(len(b_)), 1)
                try:
                    n = make()
                    quiet(nc.solve_network, n, mode='full')
                finally:
                    nc.cg = old
                return n['solve_info']['full']
            runs = {'none_free': solved(direct_pair), 'spsolve': solved(net3), 'cg': solved(wide),
                    'spsolve_fallback': solved(wide, cg_fail=True),
                    'cg+jacobi': faulted(run3)['solve_info']['full'], 'gmres+ilu': faulted(run3, True)['solve_info']['full']}
            shape = {m: (i.get('method'), (i.get('attempts') or [{}])[-1].get('krylov_info'), i.get('status')) for m, i in runs.items()}
            okm = {m: nc.model_limit_certificate_problem(i) is None and nc.model_limit_certificate_problem(json.loads(json.dumps(
                       nc.solve_certificate(i, {'channel': 'ionic', 'role': 'H0', 'contact_mode': 'hertzian', 'sigma_bulk_S_cm': 0.003})))) is None
                   for m, i in runs.items()}
            chk(f'C2f ★ 사다리 여섯 단 (none_free · spsolve · cg · spsolve_fallback · cg+jacobi · gmres+ilu) 의 실제 모형 한계 증서 — 채택 방법 = 그 단 · Krylov 단 '
                f'krylov_info int 0 · 그 밖 None · 증서 판정 통과 (solve_info · 결과 증서) {shape} · {okm}',
                set(runs) == set(nc.DIRICHLET_METHODS) and all(shape[m][0] == m and shape[m][2] == 'over_conduction_guard' for m in runs)
                and all((type(shape[m][1]) is int and shape[m][1] == 0) if m in ('cg', 'cg+jacobi', 'gmres+ilu') else shape[m][1] is None for m in runs)
                and all(okm.values()))

        _guard('C2', sC2)

        # ══ C3 — 이미 거부되던 변이는 거부 그대로 ═════════════════════════════════════════════════════════════════════
        def sC3():
            d = mut(lambda d_: fcert(d_)['attempts'][-1].update(outcome='certificate_failed'))
            expect('C3a 마지막 시도 outcome certificate_failed', d, False)
            d = mut(lambda d_: fcert(d_)['attempts'][-1].update(I_bottom=fcert(d_)['attempts'][-1]['I_bottom'] * 1.01))
            expect('C3b 마지막 시도 전류 다름 (I_bottom ×1.01)', d, False)

        _guard('C3', sC3)

        # ══ C4 — 경계 · 상수 그대로 ══════════════════════════════════════════════════════════════════════════════════
        def sC4():
            n15 = net3(plate_z=0.75)
            r15 = quiet(nc.solve_network, n15, mode='full')
            nup = net3(plate_z=math.nextafter(0.75, math.inf))
            rup = quiet(nc.solve_network, nup, mode='full')
            iup = nup['solve_info']['full']
            chk(f'C4a q = 1.5 정확 → computed {r15!r} (가드 아님 · 증서 판정 거부) · 다음 수 q {iup.get("q_withheld")!r} → 값 거부 · 모형 한계 (원 정밀도 엄격 >)',
                r15 == (2.0, 1.5) and isinstance(nc.model_limit_certificate_problem(n15['solve_info']['full']), str)
                and rup == (None, None) and iup.get('q_withheld') > 1.5 and nc.model_limit_certificate_problem(iup) is None
                and nc._net_sigma_status(None, False, iup, channel='ionic') == ('not_computed', ML))
            net = net3()
            quiet(nc.solve_network, net, mode='full')
            info = net['solve_info']['full']

            def ulp(k):
                c = copy.deepcopy(info)
                for _ in range(k):
                    c['q_withheld'] = math.nextafter(c['q_withheld'], math.inf)
                return nc.model_limit_certificate_problem(c)
            chk(f'C4b q_withheld +16 ulp 통과 · +17 ulp 거부 (같은 식 · 같은 순서 재구성 · 16ε 그대로) — {ulp(17)!r:.120}',
                ulp(16) is None and isinstance(ulp(17), str) and 'q_withheld' in ulp(17))
            chk('C4c 상수 그대로 — FULL_Q_GUARD_MAX 1.5 · 사다리 수용 상수 (보존 · 내부 잔차) 1e−6 · q 재구성 허용 16ε',
                nc.FULL_Q_GUARD_MAX == 1.5 and nc.DIRICHLET_CONSERVATION_REL_MAX == 1e-6 and nc.DIRICHLET_RESIDUAL_REL_MAX == 1e-6
                and nc._Q_REC_REL_TOL == 16 * sys.float_info.epsilon)

        _guard('C4', sC4)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print(f'\ntest_l214r01_certificate: {_ok}/{_ok + len(_fail)} PASS' + (f'   FAILED: {len(_fail)}' if _fail else ''))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
