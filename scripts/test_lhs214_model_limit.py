#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LHS 214 망 단계 실패 — FULL 모형 한계 (수치 인증 성공 / 출력 채택 거부) 범주의 양성 · 음성 행렬 (`L214-01` · `L214-02`).

  python3 scripts/test_lhs214_model_limit.py [--selftest]

근거 = Codex 판정 `docs/reviews/codex_review_lhs214_failures_20261014.md` §2 (L214-01 · 02) · §4 A1 · A2 · 수정 계획 `docs/reviews/lhs214_fix_plan_20261014.md`
§1 · §3 A2 (1저자 10-14 비준 Q1–Q5 권고대로 — Q2 (가) 분류 = H0 · H12 · Physics 공통 · 단상 이온 · 전자 FULL 만 · 열 제외 · Q5 (가) 문턱 1.5 그대로 ·
수치 허용치 1e−6 · 사다리 · G > 0 · 병렬 상한 그대로).

★ 시험 먼저 — Codex 의 반례 (`probes/solver_probe.py` · `probes/consumer_contracts.py` — 실행하지 않았다 · 읽기만) 를 **우리 시험으로** 다시 만든다.
  고치기 전 코드에서 빨갛다 (FULL q > 1.5 가 `solve_failed` 로 뭉개짐 · plate_z = +∞ 가 같은 가드 사유 · 공용 판정 함수 없음 · 실패 레코드 검사 면제 상속).
  S  솔버 (실제 `solve_network` · 0–1–2 직렬 3 노드 회로 · R_total 0.25 둘 · 정확해 V = (1, 0.5, 0) · G = 2 · 전류 ±2 · Σg 8):
     q = 2 · 1.5 · 1.49999998 · 1.50000002 · 열 q = 2 (면제) · CF q 5 · 협착-only q 3.33 (값 유지 표지) · R_c = 0 · 비관통 · 경계 겹침 ·
     첫 단 예외 · 틀린 해 · 비유한 해 · 미수렴 · 0 전도 (병렬 상한) · plate_z = +∞ · NaN · 0 · 음수 · bool
  R  생산자 레코드 (실제 `_run_all_networks` · 사슬 침대 셋) — physics 만 · Hertz 주 타깃 · 전자 채널 모형 한계 · 전자 · 열 FULL 상태 · 사유 전파 ·
     생산자 → 소비자 같은 판정 (공용 판정 `tau_flux.full_model_limit_problem` · `pipeline_service.channel_verdict` · `ion_record_problem`)
  P  직렬화 레코드 위조 · 결손 (사유만 위조 · 증서 결손 · 남의 증서 · 틀린 q 재구성 · 문턱 이하 q · 남은 값 · 모르는 사유 · Codex C1 의 세 반례 ·
     세대 결손 · 열 · 관통 0 · 채널 상태 · 모드 · 단 기록 · 병렬 상한 · 정책 · 모형 한계 + 다른 채널 실패)
  T  τ 소비자 (`tau_flux.ion_columns`) — 정확한 사유 full_over_conduction · 값 빈칸 · 위조 = 기술 실패 · 띠 L1 우선 · 상태 판정 도우미
  D  실제 자료 — Codex 묶음의 lhsx_054 단독 진단 (tgz 안 JSON · 읽기만): 증서 수치 · q 재구성 1.5370331988867802 · 옛 레코드 = 계속 차단 (Q3 unknown)
  V  배포 빌더 (`lhs_release_build`) — 빈칸 뜻 NA_MODEL_LIMIT · 주 타깃 Hertz 모형 한계 = v1.3 HOLD · 관통 분류 · physics 부록 빈칸 일관성
⚠ 범위 — 분류 · 게시 · 인계 계약의 시험이다 (합성 회로 · 합성 사슬 — φ_SE > 1 인 합성 기하 포함).  물리 정확도 · 14 건의 원인 · 새 214 결과로 확대하지 않는다.
  실 생산자 CLI → 일반 · 정지 게시 → 다시 읽기 → 인계 → 배포 → 화면 끝-끝은 `webapp/test_network_handover_chain.py` ⑤.
"""
import contextlib
import copy
import io
import json
import math
import os
import sys
import tarfile
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
for _p in (HERE, os.path.join(ROOT, 'webapp')):
    if _p not in sys.path:
        sys.path.insert(0, _p)
EVIDENCE_TGZ = os.path.join(ROOT, 'docs', 'reviews', 'codex_lhs214_failures_review_evidence_20261014', 'submitted',
                            'lhs214_run_evidence_1014_1520.tgz')
DIAG = 'lhs214_run_evidence_1014_1520/diag_lhsx054/network_conductivity_physics.json'
ML = 'full_over_conduction'
CH_ML = 'model_limit'
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
    """묶음 하나가 예외로 죽어도 나머지를 센다 (고치기 전 코드 — 없는 함수 · 인자 = 그 묶음 FAIL)."""
    try:
        fn()
    except Exception as e:                                       # noqa: BLE001
        chk(f'{label} — 예외 없이 끝난다 ({type(e).__name__}: {e})', False)


def quiet(fn, *a, **kw):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*a, **kw)


def net3(plate_z=1.0, **kw):
    """Codex 3 노드 회로 — 0–1–2 직렬 · R_total 0.25 둘 · 바닥 {0} · 위 {2} · 단위 기하 (plate_z 1 → q = 2)."""
    n = {'nodes': {0, 1, 2}, 'bottom': {0}, 'top': {2}, 'scale': 1.0, 'plate_z': plate_z, 'box_x': 1.0, 'box_y': 1.0,
         'edges': [{'id1': a, 'id2': b, 'R_total': 0.25, 'R_bulk': 0.1, 'R_constriction': 0.15} for a, b in ((0, 1), (1, 2))]}
    n.update(kw)
    return n


def chain_bed(box, area=0.5, delta=0.2):
    A = {i: dict(type=1, x=0., y=0., z=float(z), radius=1.) for i, z in enumerate(range(21), 1)}
    C = [dict(id1=i, id2=i + 1, contact_area=area, delta=delta) for i in range(1, 21)]
    return A, C, 20.0, box


def se_am_ml_bed():
    """SE 사슬 (면적 0.1 · δ 0.05) + AM 사슬 (면적 1.0 · δ 0.3 · x 5) · 상자 1 × 1 — 전자 physics q 1.611 (모형 한계) · 이온 · 전자 H0 computed."""
    A = {i: dict(type=1, x=0., y=0., z=float(z), radius=1.) for i, z in enumerate(range(21), 1)}
    A.update({100 + k: dict(type=2, x=5., y=0., z=float(z), radius=1.) for k, z in enumerate(range(21))})
    C = [dict(id1=i, id2=i + 1, contact_area=0.1, delta=0.05) for i in range(1, 21)]
    C += [dict(id1=100 + k, id2=101 + k, contact_area=1.0, delta=0.3) for k in range(20)]
    return A, C, 20.0, 1.0


def produce(nc, bed, se=(1,), am=(), tm=None):
    """실 생산자 두 모드 (CLI 가 모드 파일 · dual 에 쓰는 바로 그 dict) — JSON 왕복 = 디스크 모양."""
    A, C, plate, box = bed
    tm = tm or {1: 'SE'}
    recs = {cm: quiet(nc._run_all_networks, A, C, list(se), list(am), tm, 1, plate, box, box, None, contact_mode=cm)
            for cm in ('hertzian', 'physics')}
    return json.loads(json.dumps(recs))


def ledger_of(bed):
    A, _C, plate, box = bed
    phi = sum(4.0 / 3.0 * math.pi * a['radius'] ** 3 for a in A.values() if a['type'] == 1) / (box * box * plate)
    return {'thickness_um': plate, 'thickness_mass_conserving_um': plate, 'phi_se_mass_conserving': phi}


def main(argv=None):
    import network_conductivity as nc
    import tau_flux as tf
    import pipeline_service as ps

    fml = getattr(tf, 'full_model_limit_problem', None)            # ★ 공용 판정 함수 (고치기 전 = 없음 → 그 시험 FAIL)
    mlc = getattr(nc, 'model_limit_certificate_problem', None)     # ★ 증서 수준 판정 (생산자 · 소비자 같은 함수)

    def rejects(rec, ch='ionic', mode='physics'):
        """공용 판정이 **거부**하는가 (사유 문자열) — 함수가 없으면 False (고치기 전 = FAIL)."""
        if fml is None:
            return False
        p = fml(rec, ch, mode)
        return isinstance(p, str) and bool(p)

    def accepts(rec, ch='ionic', mode='physics'):
        return fml is not None and fml(rec, ch, mode) is None

    # ══ S. 솔버 (실제 solve_network · 3 노드) ══════════════════════════════════════════════════════════════════════
    def sS():
        net = net3()
        r = quiet(nc.solve_network, net, mode='full')
        info = net['solve_info']['full']
        att = (info.get('attempts') or [{}])[-1]
        chk('S1a 실제 3 노드 q = 2 — 값은 그대로 거부 (None, None) · 수치 시도 pass · 증서 보존 (I_b 2 · I_t −2 · 두 잔차 0) · 내부 상태 over_conduction_guard',
            r == (None, None) and att.get('outcome') == 'pass' and info.get('I_bottom') == 2.0 and info.get('I_top') == -2.0
            and info.get('conservation_rel') == 0.0 and info.get('status') == 'over_conduction_guard', repr((r, info.get('status'), att)))
        chk('S1b ★ 진단 q 를 별도 키로 (값 칸이 아니라 증서) — q_withheld 2.0 (원 정밀도 · 반올림 없음) · 문턱 1.5 · Σg 8 · 정책 판 (옛: 없음)',
            info.get('q_withheld') == 2.0 and info.get('q_guard_max') == 1.5 and info.get('sum_g') == 8.0
            and isinstance(info.get('guard_policy'), str) and info.get('guard_policy') == getattr(nc, 'MODEL_LIMIT_POLICY', object()),
            repr({k: info.get(k) for k in ('q_withheld', 'q_guard_max', 'sum_g', 'guard_policy')}))
        try:
            st = nc._net_sigma_status(None, False, info, channel='ionic')
        except TypeError as e:
            st = f'TypeError {e}'
        chk(f"S1c ★ 생산자 상태 = ('not_computed', 'full_over_conduction') (옛: solve_failed 로 뭉갬 · L214-01) — {st!r}",
            st == ('not_computed', ML))
        chk('S1d ★ 증서 수준 판정 (생산자 · 소비자 같은 함수 model_limit_certificate_problem) = 통과 (solve_info · 결과 증서 둘 다)',
            mlc is not None and mlc(info) is None
            and mlc(nc.solve_certificate(info, {'channel': 'ionic', 'role': 'H0', 'contact_mode': 'hertzian', 'sigma_bulk_S_cm': 0.003})) is None)
        cert = nc.solve_certificate(info, {'channel': 'ionic', 'role': 'H0', 'contact_mode': 'hertzian', 'sigma_bulk_S_cm': 0.003})
        chk('S1e 결과 증서에 진단 q · 문턱 · Σg · 정책이 실린다 · 게시 증서 계약 (certificate_problem) 은 그대로 거부 (출력 채택 거부 = 게시할 값 없음)',
            cert.get('q_withheld') == 2.0 and cert.get('q_guard_max') == 1.5 and cert.get('sum_g') == 8.0
            and nc.certificate_problem(cert) is not None, repr({k: cert.get(k) for k in ('q_withheld', 'q_guard_max', 'sum_g', 'status')}))

        n15 = net3(plate_z=0.75)
        r15 = quiet(nc.solve_network, n15, mode='full')
        chk(f'S2a q = 1.5 정확히 → computed (2.0, 1.5) — 문턱은 엄격 > (그대로) {r15!r}',
            r15 == (2.0, 1.5) and n15['solve_info']['full'].get('status') == 'computed')
        nlo, nhi = net3(plate_z=0.75 - 1e-8), net3(plate_z=0.75 + 1e-8)
        rlo, rhi = quiet(nc.solve_network, nlo, mode='full'), quiet(nc.solve_network, nhi, mode='full')
        chk(f'S2b q = 1.49999998 → computed · q = 1.50000002 → 값 거부 ({rlo!r} · {rhi!r})',
            rlo[1] is not None and rlo[1] < 1.5 and rhi == (None, None))
        ihi = nhi['solve_info']['full']
        try:
            st_hi = nc._net_sigma_status(None, False, ihi, channel='ionic')
        except TypeError as e:
            st_hi = f'TypeError {e}'
        chk(f'S2c ★ 1.50000002 = 모형 한계 (원 정밀도의 q 로 분류 · 반올림한 1.50 으로 넣고 빼지 않는다) — {st_hi!r} · q_withheld {ihi.get("q_withheld")!r}',
            st_hi == ('not_computed', ML) and ihi.get('q_withheld') == 2.0 * (0.75 + 1e-8) / 1.0 and ihi.get('q_withheld') > 1.5)

        def ns(ch):
            try:
                return nc._net_sigma_status(None, False, info, channel=ch)
            except TypeError as e:
                return f'TypeError {e}'
        chk(f"S3a ★ 적용 범위 = 단상 이온 · 전자 FULL — 같은 q = 2 증서라도 채널 열 · 없음 = 모형 한계 아님 (solve_failed) · 전자 = 모형 한계 "
            f"({ns('thermal')!r} · {ns(None)!r} · {ns('electronic')!r})",
            ns('thermal') == ('not_computed', 'solve_failed') and ns(None) == ('not_computed', 'solve_failed')
            and ns('electronic') == ('not_computed', ML))
        nth = net3(is_thermal=True)
        rth = quiet(nc.solve_network, nth, mode='full')
        chk(f'S3b 열 FULL q = 2 → computed (열은 다상 정규화 · 병렬 상한 — 이 예외에 넣지 않는다 · 그대로) {rth!r}',
            rth == (2.0, 2.0) and nth['solve_info']['full'].get('status') == 'computed')

        ncf = net3()
        rcf = quiet(nc.solve_network, ncf, mode='bulk_only')
        ncn = net3()
        rcn = quiet(nc.solve_network, ncn, mode='constriction_only')
        chk(f'S4a CF q 5 · 협착-only q 3.33 → 값 유지 + model_over_conduction (기존 진단 정책 그대로 · 새 범주 아님) ({rcf!r} · {rcn!r})',
            rcf == (5.0, 5.0) and ncf['solve_info']['bulk_only'].get('status') == 'model_over_conduction'
            and rcn[1] is not None and abs(rcn[1] - 10.0 / 3.0) < 1e-12 and ncn['solve_info']['constriction_only'].get('status') == 'model_over_conduction'
            and nc._net_sigma_status(rcf[1], False, ncf['solve_info']['bulk_only']) == ('model_over_conduction', 'q_gt_1p5'))
        nz = net3()
        nz['edges'][0]['R_constriction'] = 0.0
        rz = quiet(nc.solve_network, nz, mode='constriction_only')
        chk('S4b 협착-only R_c = 0 → (None, None) · zero_resistance_requires_contraction (기존 정책 그대로)',
            rz == (None, None) and nz['solve_info']['constriction_only'].get('reason') == 'zero_resistance_requires_contraction')

        nnt = net3()
        nnt['top'] = {3}
        nnt['nodes'] = {0, 1, 2, 3}
        quiet(nc.solve_network, nnt, mode='full')
        try:
            st_nt = nc._net_sigma_status(None, True, nnt['solve_info']['full'], channel='ionic')
        except TypeError as e:
            st_nt = f'TypeError {e}'
        chk(f"S5a 비관통 → ('valid_zero', 'no_through_path') (그래프가 증명한 0 · 그대로 · 채널 이온이어도) {st_nt!r}",
            st_nt == ('valid_zero', 'no_through_path'))
        nov = net3()
        nov['top'] = {0}
        rov = quiet(nc.solve_network, nov, mode='full')
        iov = nov['solve_info']['full']
        try:
            st_ov = nc._net_sigma_status(None, False, iov, channel='ionic')
        except TypeError as e:
            st_ov = f'TypeError {e}'
        chk(f"S5b 경계 겹침 → (None, None) · not_computed boundary_overlap · 풀이 방법 없음 (모형 한계 아님) {st_ov!r}",
            rov == (None, None) and st_ov == ('not_computed', 'boundary_overlap') and iov.get('method') is None)

    _guard('S1–S5', sS)

    def sS6():
        import numpy as np

        def faulted(fault, net=None):
            net = net3() if net is None else net
            old = {k: getattr(nc, k) for k in ('spsolve', 'cg', 'gmres')}
            if fault == 'exception':
                def broken(*a, **k):
                    raise RuntimeError('주입: 첫 단 예외')
                nc.spsolve = broken
            elif fault in ('bad_certificate', 'nonfinite_vector'):
                v = 0.0 if fault == 'bad_certificate' else float('nan')
                nc.spsolve = lambda A, b: np.full(len(b), v)
                nc.cg = lambda A, b, **k: (np.full(len(b), v), 0)
                nc.gmres = lambda A, b, **k: (np.full(len(b), v), 0)
            elif fault == 'not_converged':
                nc.spsolve = lambda A, b: np.full(len(b), float('nan'))
                nc.cg = lambda A, b, **k: (np.zeros(len(b)), 1)
                nc.gmres = lambda A, b, **k: (np.zeros(len(b)), 1)
            try:
                r = quiet(nc.solve_network, net, mode='full')
            finally:
                for k, v in old.items():
                    setattr(nc, k, v)
            info = net['solve_info']['full']
            try:
                st = nc._net_sigma_status(r[0], False, info, channel='ionic')
            except TypeError as e:
                st = f'TypeError {e}'
            return r, info, st
        res = {f: faulted(f) for f in ('exception', 'bad_certificate', 'nonfinite_vector', 'not_converged')}
        zg = net3()
        for e in zg['edges']:
            e['R_total'] = float('inf')
        res['zero_conductance'] = faulted(None, zg)
        want = {'exception': ('not_computed', 'solve_failed'), 'bad_certificate': ('not_computed', 'current_conservation_failed'),
                'nonfinite_vector': ('not_computed', 'current_conservation_failed'), 'not_converged': ('not_computed', 'solve_failed'),
                'zero_conductance': ('not_computed', 'solve_failed')}
        got = {k: v[2] for k, v in res.items()}
        chk(f'S6a ★ 높은 q 그래프 + 앞 단계 실패 (첫 단 예외 · 틀린 해 · 비유한 해 · 미수렴 · 0 전도 병렬 상한) = 기술 실패 그대로 · 높은 q 로 구제하지 않는다 {got}',
            got == want and all(v[0] == (None, None) for v in res.values()))
        chk('S6b 그 실패 증서는 모형 한계 증서 판정도 거부한다 (model_limit_certificate_problem = 사유)',
            mlc is not None and all(isinstance(mlc(v[1]), str) and mlc(v[1]) for v in res.values()))

    _guard('S6', sS6)

    def sS7():
        def geo(**kw):
            n = net3(**kw)
            r = quiet(nc.solve_network, n, mode='full')
            info = n['solve_info']['full']
            try:
                st = nc._net_sigma_status(r[0], False, info, channel='ionic')
            except TypeError as e:
                st = f'TypeError {e}'
            return r, info, st
        rinf, iinf, sinf = geo(plate_z=float('inf'))
        chk(f"S7a ★ plate_z = +∞ (나머지는 같은 유효 회로) → 모형 한계가 아니다 — 입력 · 경계 검사 먼저 (not_computed invalid_geometry · 옛: 같은 "
            f"over_conduction_guard 사유 · L214-01) {sinf!r} · 내부 {iinf.get('status')!r}/{iinf.get('reason')!r}",
            rinf == (None, None) and sinf == ('not_computed', 'invalid_geometry') and iinf.get('reason') == 'invalid_geometry'
            and (mlc is not None and isinstance(mlc(iinf), str)))
        bad = {}
        for lab, kw in (('NaN', dict(plate_z=float('nan'))), ('0', dict(plate_z=0.0)), ('음수', dict(plate_z=-1.0)), ('bool', dict(box_x=True)),
                        ('문자열', dict(scale='1')), ('상자 ∞', dict(box_y=float('inf')))):
            r_, i_, s_ = geo(**kw)
            bad[lab] = (r_, s_)
        chk(f'S7b ★ plate_z NaN · 0 · 음수 · box bool · scale 문자열 · 상자 ∞ → (None, None) · not_computed invalid_geometry (NaN · ∞ · 타입을 수로 묵인하지 않는다) '
            f'{ {k: v[1] for k, v in bad.items()} }',
            all(v == ((None, None), ('not_computed', 'invalid_geometry')) for v in bad.values()))
        nn = net3(plate_z=float('inf'))
        nn['top'] = {3}
        nn['nodes'] = {0, 1, 2, 3}
        quiet(nc.solve_network, nn, mode='full')
        try:
            st = nc._net_sigma_status(None, True, nn['solve_info']['full'], channel='ionic')
        except TypeError as e:
            st = f'TypeError {e}'
        chk(f"S7c 비관통 + 무효 기하 → invalid_geometry (증명된 0 으로 읽지 않는다 · 입력 검사 먼저) {st!r}", st == ('not_computed', 'invalid_geometry'))

    _guard('S7', sS7)

    # ══ R. 생산자 레코드 (실제 _run_all_networks) ══════════════════════════════════════════════════════════════════
    B1, B2, B3 = chain_bed(1.0), chain_bed(0.7), se_am_ml_bed()
    recs = {}

    def sR():
        recs['B1'] = produce(nc, B1)
        recs['B2'] = produce(nc, B2)
        recs['B3'] = produce(nc, B3, se=(1,), am=(2,), tm={1: 'SE', 2: 'AM_P'})
        h, p = recs['B1']['hertzian'], recs['B1']['physics']
        h12 = h.get('hertz_h12') or {}
        cp = p.get('solve_certificate_full') or {}
        g = cp.get('geometry') or {}
        q_rec = (cp['I_bottom'] / cp['delta_V'] * (g['plate_z'] * g['scale']) / (g['box_x'] * g['box_y'] * g['scale'] ** 2)
                 if cp.get('I_bottom') is not None else None)
        chk(f"R1a ★ physics FULL 모형 한계 레코드 — σ · 차원 σ null · not_computed full_over_conduction · 이온 채널 model_limit (옛: solve_failed · failed) · "
            f"증서 q_withheld = I_b × T/A ({cp.get('q_withheld')!r} · 재구성 {q_rec!r})",
            p.get('sigma_full') is None and p.get('sigma_full_mScm') is None and p.get('sigma_full_status') == 'not_computed'
            and p.get('sigma_full_reason') == ML and p.get('ionic_status') == CH_ML
            and cp.get('status') == 'over_conduction_guard' and q_rec is not None and cp.get('q_withheld') == q_rec and q_rec > 1.5,
            repr({k: p.get(k) for k in ('sigma_full_status', 'sigma_full_reason', 'ionic_status')}))
        chk("R1b ★ FULL 유도값 없음 — CF/FULL · Bruggeman/FULL 비 없음 · 협착 전력 몫 None + 모형 한계 사유 (옛: 'FULL solve failed' 문구)",
            p.get('R_brug_over_full') is None and p.get('R_bruggeman_over_full') is None
            and p.get('constriction_power_share_ion_physics') is None
            and p.get('constriction_power_share_ion_physics_status') == getattr(nc, 'CPS_MODEL_LIMIT_STATUS', object()),
            repr({k: p.get(k) for k in ('R_brug_over_full', 'constriction_power_share_ion_physics_status')}))
        chk(f"R1c Hertz H0 · H12 = computed 그대로 (q {h.get('sigma_full')!r} · {h12.get('sigma_full')!r}) · CF · 협착-only 진단 = 기존 정책 · 열 FULL q > 1.5 = computed (면제)",
            h.get('sigma_full') == 0.79535562 and h.get('sigma_full_status') == 'computed' and h12.get('sigma_full') == 1.34224459
            and h12.get('sigma_full_status') == 'computed' and p.get('sigma_bulk_net_status') == 'model_over_conduction'
            and p.get('thermal_status') == 'computed' and (p.get('thermal_sigma_full') or 0) > 1.5)
        hh, h12b, pb = recs['B2']['hertzian'], recs['B2']['hertzian'].get('hertz_h12') or {}, recs['B2']['physics']
        chk('R2 ★ 주 타깃 Hertz H0 · H12 · physics 모두 모형 한계 (상자 0.7) — 셋 다 not_computed full_over_conduction · 이온 채널 model_limit (분류 = 모드 공통 · Q2 (가))',
            all(r_.get('sigma_full_status') == 'not_computed' and r_.get('sigma_full_reason') == ML and r_.get('ionic_status') == CH_ML
                for r_ in (hh, h12b, pb)),
            repr([(r_.get('sigma_full_reason'), r_.get('ionic_status')) for r_ in (hh, h12b, pb)]))
        e_h, e_p = recs['B3']['hertzian'], recs['B3']['physics']
        chk("R3a ★ 전자 FULL 모형 한계 (physics) — electronic_sigma_full_status · _reason 이 출력까지 전파 (옛: 키 없음 · Codex §2 끝 문단) · 전자 채널 model_limit · "
            "CF/FULL 전자 비 · 전력 몫 없음",
            e_p.get('electronic_sigma_full') is None and e_p.get('electronic_sigma_full_status') == 'not_computed'
            and e_p.get('electronic_sigma_full_reason') == ML and e_p.get('electronic_status') == CH_ML and e_p.get('electronic_R_brug') is None
            and e_p.get('constriction_power_share_el_physics') is None
            and e_p.get('constriction_power_share_el_physics_status') == getattr(nc, 'CPS_MODEL_LIMIT_STATUS', object())
            and (e_p.get('electronic_solve_certificate_full') or {}).get('q_withheld', 0) > 1.5,
            repr({k: e_p.get(k) for k in ('electronic_sigma_full_status', 'electronic_sigma_full_reason', 'electronic_status')}))
        chk('R3b 전자 · 열 FULL 상태 · 사유 전파 (정상) — Hertz 전자 computed · 열 computed · 이온 두 모드 computed (같은 침대)',
            e_h.get('electronic_sigma_full_status') == 'computed' and e_h.get('electronic_status') == 'computed'
            and e_h.get('thermal_sigma_full_status') == 'computed' and e_p.get('thermal_sigma_full_status') == 'computed'
            and e_h.get('sigma_full_status') == e_p.get('sigma_full_status') == 'computed')
        same = []
        if fml is not None:
            same = [fml(p, 'ionic', 'physics'), fml(hh, 'ionic', 'hertz'), fml(h12b, 'ionic', 'hertz_h12'), fml(pb, 'ionic', 'physics'),
                    fml(e_p, 'electronic', 'physics')]
        chk(f'R4a ★ 생산자 → 소비자 같은 판정 — 공용 판정 tau_flux.full_model_limit_problem = 통과 (B1 physics · B2 H0 · H12 · physics · B3 전자 physics) {same}',
            fml is not None and all(x is None for x in same))
        cv = [ps.channel_verdict(p, 'ionic', 'physics') if 'mode' in ps.channel_verdict.__code__.co_varnames else ('no-mode', ''),
              ps.channel_verdict(e_p, 'electronic', 'physics') if 'mode' in ps.channel_verdict.__code__.co_varnames else ('no-mode', '')]
        chk(f'R4b 게시 채널 판정 (pipeline_service.channel_verdict) = ok — 모형 한계 채널 (공용 판정으로 확인) · 옛: failed {[(v, w[:60]) for v, w in cv]}',
            all(v == 'ok' for v, _w in cv))
        chk('R4c ★ 공용 기술 검사 (ion_record_problem) = None (유효한 모형 한계 · 옛: solver_guard) · 세대 계약 g2 · 문제 0 · 증서 결합 [] (Codex C1 #3)',
            tf.ion_record_problem(p) is None and tf.ion_record_problem(hh) is None and tf.ion_record_problem(h12b) is None
            and tf.network_generation_contract(recs['B1']).get('generation') == 'g2' and not tf.network_generation_contract(recs['B1']).get('problems')
            and tf.network_generation_contract(recs['B2']).get('generation') == 'g2' and not tf.network_generation_contract(recs['B2']).get('problems')
            and tf.certificate_binding_problems('physics', p) == [],
            repr((tf.ion_record_problem(p), tf.generation_contract_text(tf.network_generation_contract(recs['B1']))[:200])))

    _guard('R', sR)

    # ══ P. 직렬화 레코드 위조 · 결손 (L214-01 · 02) ═════════════════════════════════════════════════════════════════
    def sP():
        if 'B1' not in recs:
            chk('P — 생산자 레코드가 없다 (R 실패)', False)
            return
        base = recs['B1']['physics']
        chk('P0 기준 레코드 (B1 physics) = 공용 판정 통과 (아래 변이는 이 레코드에서 한 곳씩만 바꾼다)', accepts(base))

        def mut(fn, src=None):
            m = copy.deepcopy(src if src is not None else base)
            fn(m)
            return m
        #  P1 사유만 위조 — 실제 옛 실패 레코드 (Codex 묶음 lhsx_054 단독 진단 · 옛 생산자) 의 사유 · 채널 상태 · 전력 몫 사유만 바꾼다
        old = None
        try:
            with tarfile.open(EVIDENCE_TGZ) as t:
                old = json.load(t.extractfile(DIAG))
        except (OSError, KeyError, ValueError) as e:
            chk(f'P1 실제 옛 레코드를 읽는다 ({type(e).__name__}: {e})', False)
        if old is not None:
            forged = copy.deepcopy(old)
            forged.update(sigma_full_reason=ML, ionic_status=CH_ML,
                          constriction_power_share_ion_physics_status=getattr(nc, 'CPS_MODEL_LIMIT_STATUS', 'x'))
            chk('P1 ★ 사유만 위조 (실제 옛 lhsx_054 레코드 · 증서는 옛 그대로 — q_withheld · 정책 없음) → 공용 판정 거부 · ion_record_problem 기술 실패 (invalid_input)',
                rejects(forged) and (tf.ion_record_problem(forged) or ('',))[0] == 'invalid_input', repr(tf.ion_record_problem(forged))[:200])
        cases = {
            'P2a 증서 결손 (키 삭제)': mut(lambda m: m.pop('solve_certificate_full')),
            'P2b 증서 None': mut(lambda m: m.update(solve_certificate_full=None)),
            'P2c 증서 객체 아님': mut(lambda m: m.update(solve_certificate_full='cert')),
            'P3a 남의 증서 — CF 증서를 FULL 자리에': mut(lambda m: m.update(solve_certificate_full=copy.deepcopy(base['solve_certificate_bulk_net']))),
            'P4a 틀린 q 재구성 — q_withheld ×1.01': mut(lambda m: m['solve_certificate_full'].update(
                q_withheld=(m['solve_certificate_full'].get('q_withheld') or 2.593468501694396) * 1.01)),
            'P5a q_withheld = 1.5 (문턱 · 엄격 > 아님)': mut(lambda m: m['solve_certificate_full'].update(q_withheld=1.5)),
            'P5b q_withheld bool': mut(lambda m: m['solve_certificate_full'].update(q_withheld=True)),
            'P5c q_withheld NaN': mut(lambda m: m['solve_certificate_full'].update(q_withheld=float('nan'))),
            'P5d q_withheld 문자열': mut(lambda m: m['solve_certificate_full'].update(q_withheld='2.59')),
            'P6a 남은 값 — sigma_full 숫자': mut(lambda m: m.update(sigma_full=2.59346850)),
            'P6b 남은 값 — sigma_full_mScm 숫자': mut(lambda m: m.update(sigma_full_mScm=7.780406)),
            'P6c 남은 유도값 — R_brug_over_full': mut(lambda m: m.update(R_brug_over_full=1.0)),
            'P6d 남은 유도값 — 전력 몫 숫자': mut(lambda m: m.update(constriction_power_share_ion_physics=0.3)),
            'P6e 전력 몫 사유 = 풀이 실패 문구': mut(lambda m: m.update(constriction_power_share_ion_physics_status=nc.CPS_SOLVE_FAILED_STATUS)),
            'P10a 상태 valid_zero 로 바꿈 (증서는 해를 주장)': mut(lambda m: m.update(sigma_full_status='valid_zero')),
            'P10b 상태 computed + 값 없음': mut(lambda m: m.update(sigma_full_status='computed')),
            'P12a 관통 분율 0': mut(lambda m: m.update(percolating_fraction=0.0)),
            'P12b 채널 상태 failed (모형 한계 가지인데)': mut(lambda m: m.update(ionic_status='failed')),
            'P14a 단 기록 위조 — 마지막 시도 certificate_failed': mut(lambda m: m['solve_certificate_full']['attempts'][-1].update(outcome='certificate_failed')),
            'P14b 단 기록 위조 — 마지막 시도 방법 다름': mut(lambda m: m['solve_certificate_full']['attempts'][-1].update(method='gmres+ilu')),
            'P14c 병렬 상한 — Σg < I_b/1.1': mut(lambda m: m['solve_certificate_full'].update(sum_g=m['solve_certificate_full']['I_bottom'] / 2)),
            'P14d 문턱 기록 위조 — q_guard_max 1.0': mut(lambda m: m['solve_certificate_full'].update(q_guard_max=1.0)),
            'P14e 정책 판 위조': mut(lambda m: m['solve_certificate_full'].update(guard_policy='any_q/v0')),
            'P14f 증서 사유 위조 (가드 사유가 아님)': mut(lambda m: m['solve_certificate_full'].update(reason='solve_failed')),
            'P14g 증서 가지 bulk_only': mut(lambda m: m['solve_certificate_full'].update(branch='bulk_only')),
            'P14h 증서 채널 thermal': mut(lambda m: m['solve_certificate_full'].update(channel='thermal')),
            'P14i 증서 σ₀ ≠ 부모 σ₀': mut(lambda m: m['solve_certificate_full'].update(sigma_bulk_S_cm=0.006)),
            'P14j ΔV 2': mut(lambda m: m['solve_certificate_full'].update(delta_V=2.0)),
            'P14k 기하 G→q 변이': mut(lambda m: m['solve_certificate_full'].update(g_to_q=m['solve_certificate_full']['g_to_q'] * 2)),
            'P14l 기하 plate_z +∞ (증서)': mut(lambda m: m['solve_certificate_full']['geometry'].update(plate_z=float('inf'))),
            'P14m 증서 상태 computed (가드 상태가 아님)': mut(lambda m: m['solve_certificate_full'].update(status='computed')),
        }

        def _scale_currents(m, f):
            c = m['solve_certificate_full']
            c['I_bottom'] *= f
            c['I_top'] *= f
            a = c['attempts'][-1]
            a['I_bottom'], a['I_top'] = c['I_bottom'], c['I_top']
        cases['P4b 틀린 q 재구성 — 전류 ×1.01 (보존은 맞춤 · q_withheld 그대로)'] = mut(lambda m: _scale_currents(m, 1.01))

        def _below(m):                                              # 일관되게 낮춘 위조 — q_rec = q_withheld = 1.4 (문턱 이하)
            c = m['solve_certificate_full']
            f = 1.4 / (c.get('q_withheld') or 2.593468501694396)
            _scale_currents(m, f)
            g = c['geometry']
            c['q_withheld'] = c['I_bottom'] / c['delta_V'] * (g['plate_z'] * g['scale']) / (g['box_x'] * g['box_y'] * g['scale'] ** 2)
        cases['P5e 일관된 문턱 이하 q (재구성 = 기록 = 1.4)'] = mut(_below)
        bad = sorted(k for k, m in cases.items() if not rejects(m))
        chk(f'P2–P14 ★ 위조 · 결손 {len(cases)} 가지 전부 공용 판정 거부 (함수가 없으면 전부 FAIL) — 통과해 버린 것 {bad}', fml is not None and not bad)
        leak = sorted(k for k, m in cases.items() if tf.ion_record_problem(m) is None)
        chk(f'P2–P14b 그 레코드들은 공용 기술 검사 (ion_record_problem) 에서도 기술 실패 — 새는 것 {leak}', not leak)
        if 'B2' in recs and 'B3' in recs:
            h0, h12 = recs['B2']['hertzian'], recs['B2']['hertzian'].get('hertz_h12') or {}
            m3b = mut(lambda m: m.update(solve_certificate_full=copy.deepcopy(h12['solve_certificate_full'])), src=h0)
            m3c = mut(lambda m: m.update(solve_certificate_full=copy.deepcopy(recs['B3']['physics']['electronic_solve_certificate_full'])))
            m3d = mut(lambda m: m.update(solve_certificate_full=copy.deepcopy(h0['solve_certificate_full'])), src=recs['B2']['physics'])
            chk('P3b–d ★ 남의 증서 — H12 FULL 증서를 H0 자리에 · 전자 증서를 이온 자리에 · H0 증서를 physics 자리에 → 거부',
                rejects(m3b, 'ionic', 'hertz') and rejects(m3c, 'ionic', 'physics') and rejects(m3d, 'ionic', 'physics'))
            chk('P13 ★ 모드 어긋남 — physics 레코드를 H0 자리 (hertz) 로 판정하면 거부 · H12 레코드를 주 Hertz 자리로 판정하면 거부',
                rejects(base, 'ionic', 'hertz') and rejects(h12, 'ionic', 'hertz'))
        m7 = mut(lambda m: m.update(sigma_full_reason='full_overconduction'))
        chk(f"P7 ★ 모르는 사유 (오타 full_overconduction) → 공용 기술 검사 solver_guard (기술 실패 · 모형 한계 범주가 아니다) {tf.ion_record_problem(m7)!r}",
            (tf.ion_record_problem(m7) or ('',))[0] == 'solver_guard')
        #  P8 — Codex C1 의 세 반례 (consumer_review.md · 판정문 §2 L214-02 표) 를 그대로
        c8a = mut(lambda m: (m['solve_certificate_bulk_net'].update(residual_rel=1.0), m.update(sigma_bulk_net_status='computed')))
        c8b = mut(lambda m: m.pop('bulk_model'))
        chk('P8a ★ CF 증서 residual_rel 1.0 (+ 상태 computed) → certificate_binding_problems 비지 않음 (옛: [] — 실패 레코드로 일찍 반환)',
            bool(tf.certificate_binding_problems('physics', c8a)), repr(tf.certificate_binding_problems('physics', c8a))[:200])
        chk('P8b ★ physics bulk_model 삭제 → _g2_mode_problems 비지 않음 (옛: [] — not_computed 실패 레코드의 표기 결손 면제 상속)',
            bool(tf._g2_mode_problems('physics', c8b)), repr(tf._g2_mode_problems('physics', c8b)))
        chk('P8c ★ 실제 FULL 수치 증서를 그대로 보존한 유효 모형 한계 → 증서 결합 [] (옛: "숫자 없는 가지인데 증서가 해를 주장" 충돌) · 공용 기술 검사 None',
            tf.certificate_binding_problems('physics', base) == [] and tf.ion_record_problem(base) is None)
        c9 = {k: mut(lambda m, k=k: m.pop(k)) for k in ('electrode_model', 'area_rule', 'psi_placement')}
        bad9 = [k for k, m in c9.items() if not tf.network_generation_contract({'hertzian': recs['B1']['hertzian'], 'physics': m}).get('problems')]
        chk(f'P9 ★ 세대 표기 결손 (전극 · 면적 규칙 · ψ) → 세대 계약 위반 (모형 한계 레코드는 실패 면제를 받지 않는다) — 통과해 버린 것 {bad9}', not bad9)
        th = mut(lambda m: m.update(thermal_status=CH_ML))
        cvm = 'mode' in ps.channel_verdict.__code__.co_varnames
        chk('P11 ★ 열 채널 model_limit 주장 → 게시 채널 판정 fail (열은 이 예외 밖 · 옛: unknown) · 공용 판정 (thermal) 거부',
            ps.channel_verdict({'thermal_status': CH_ML}, 'thermal')[0] == 'fail'
            and (ps.channel_verdict(th, 'thermal', 'physics')[0] if cvm else 'x') == 'fail' and rejects(base, 'thermal', 'physics'))
        #  P15 — 모형 한계 + 다른 채널 진짜 실패 (같은 레코드) → 다른 실패가 우선 (게시 내용 판정 = 모드 파일 · 채널 셋)
        d = tempfile.mkdtemp(prefix='l214_cv_')
        try:
            def _write(h_, p_):
                for n_, r_ in (('hertzian', h_), ('physics', p_)):
                    with open(os.path.join(d, f'network_conductivity_{n_}.json'), 'w') as f:
                        json.dump(r_, f)
                return ps.network_content_verdict(d)
            ok1, why1 = _write(recs['B1']['hertzian'], base)
            ok2, why2 = _write(recs['B1']['hertzian'], mut(lambda m: m.update(thermal_status='failed', thermal_status_reason='주입: 열 FULL 풀이 실패')))
            ok3, why3 = _write(recs['B1']['hertzian'], mut(lambda m: m['solve_certificate_full'].update(q_withheld=1.0)))
            chk(f'P15a ★ 유효 모형 한계 레코드 → 게시 내용 판정 ok (옛: physics.ionic=fail) — {why1[:160]}', ok1)
            chk(f'P15b 모형 한계 + 같은 레코드 열 채널 진짜 실패 → 내용 판정 실패 (진짜 실패 우선 · 기존 차단) — {why2[:160]}', not ok2 and 'thermal' in why2)
            chk(f'P15c 위조 증서 (q 1.0) 의 model_limit 채널 → 내용 판정 실패 — {why3[:160]}', not ok3 and 'ionic' in why3)
        finally:
            import shutil
            shutil.rmtree(d, ignore_errors=True)

    _guard('P', sP)

    # ══ T. τ 소비자 (ion_columns) ══════════════════════════════════════════════════════════════════════════════════
    def sT():
        if 'B1' not in recs:
            chk('T — 생산자 레코드가 없다', False)
            return
        row = tf.ion_columns(recs['B1'], ledger_of(B1), 100.0)
        chk(f"T1 ★ physics = NOT_COMPUTED · 사유 정확히 'full_over_conduction' (옛: solver_guard 로 뭉갬) · f · f_gap · tau2 · tau 빈칸 · Hertz OK · H12 OK · 세대 g2 "
            f"({row.get('ion_net_status_physics')!r} · {row.get('ion_net_status_reason_physics')!r} · H {row.get('ion_net_status_hertz')!r} · "
            f"H12 {row.get('ion_net_status_hertz_h12')!r})",
            row.get('ion_net_status_physics') == 'NOT_COMPUTED' and row.get('ion_net_status_reason_physics') == ML
            and all(row.get(k) is None for k in ('f_ion_physics', 'f_ion_physics_gap', 'tau2_ion_physics', 'tau_ion_physics'))
            and row.get('ion_net_status_hertz') == 'OK' and row.get('ion_net_status_hertz_h12') == 'OK' and row.get('ion_net_generation') == 'g2')
        row2 = tf.ion_columns(recs['B2'], ledger_of(B2), 100.0)
        chk('T2 ★ 주 타깃 Hertz 모형 한계 (B2) → hertz · H12 · physics 모두 NOT_COMPUTED full_over_conduction · 값 빈칸 (0 · 1.5 · physics 로 대체하지 않는다)',
            all(row2.get(f'ion_net_status_{m}') == 'NOT_COMPUTED' and row2.get(f'ion_net_status_reason_{m}') == ML and row2.get(f'f_ion_{m}') is None
                for m in ('hertz', 'hertz_h12', 'physics')),
            repr({m: (row2.get(f'ion_net_status_{m}'), row2.get(f'ion_net_status_reason_{m}')) for m in ('hertz', 'hertz_h12', 'physics')}))
        fd = copy.deepcopy(recs['B1'])
        fd['physics']['solve_certificate_full']['q_withheld'] = 1.0
        row3 = tf.ion_columns(fd, ledger_of(B1), 100.0)
        chk(f"T3 위조 (q 1.0) → physics NOT_COMPUTED invalid_input (기술 실패 · 모형 한계 사유 아님) {row3.get('ion_net_status_reason_physics')!r:.120}",
            row3.get('ion_net_status_physics') == 'NOT_COMPUTED' and tf.reason_code(row3.get('ion_net_status_reason_physics')) == 'invalid_input')
        bd = copy.deepcopy(recs['B1'])
        bd['physics']['boundary_rule'] = 'L1'
        row4 = tf.ion_columns(bd, ledger_of(B1), 100.0)
        chk(f"T4 띠 L1 우선 (과학적 HOLD 의 기존 순서 그대로) — 모형 한계 레코드라도 띠 규칙이 L0 아니면 BAND_FALLBACK {row4.get('ion_net_status_physics')!r}",
            row4.get('ion_net_status_physics') == 'BAND_FALLBACK')
        im = getattr(tf, 'is_model_limit_status', None)
        chk('T5 상태 판정 도우미 is_model_limit_status — (NOT_COMPUTED, full_over_conduction) 정확히만 · 세부 꼬리 · 다른 상태 · 다른 사유 = 아님',
            im is not None and im('NOT_COMPUTED', ML) and not im('NOT_COMPUTED', ML + ': x') and not im('OK', ML)
            and not im('NOT_COMPUTED', 'solver_guard') and not im('NOT_COMPUTED', None))
        pp = getattr(ps, 'NETWORK_POWER_MODEL_LIMIT_REASON', None)
        chk('T6 어휘 짝 — 정지 계약의 전력 몫 모형 한계 사유 = 생산자 문구 · 공용 사유 = 생산자 사유 · 채널 상태 = 생산자 상태 (갈라지면 정상 모형 한계가 failed)',
            pp is not None and pp == getattr(nc, 'CPS_MODEL_LIMIT_STATUS', None) and getattr(tf, 'MODEL_LIMIT_REASON', None) == getattr(nc, 'FULL_OVER_CONDUCTION_REASON', 0)
            and getattr(tf, 'CHANNEL_MODEL_LIMIT', None) == getattr(nc, 'CHANNEL_MODEL_LIMIT', 0) and CH_ML in nc.CHANNEL_STATES)

    _guard('T', sT)

    # ══ D. 실제 자료 — lhsx_054 단독 진단 (Codex 묶음 tgz · 읽기만) ═════════════════════════════════════════════════
    def sD():
        with tarfile.open(EVIDENCE_TGZ) as t:
            old = json.load(t.extractfile(DIAG))
        c = old['solve_certificate_full']
        g = c['geometry']
        #  솔버 순서 = solve_network 의 `sigma_ratio = G_eff * T_um / A_um2` ((I_b/ΔV)·T)/A — 가드가 실제로 1.5 와 비교한 수 ·
        #  Codex 판정문 §1-3 의 값 = I_b/ΔV × g_to_q (미리 나눈 T/A) — 같은 수의 다른 계산 순서 (마지막 자리 3 ulp)
        q = c['I_bottom'] / c['delta_V'] * (g['plate_z'] * g['scale']) / (g['box_x'] * g['box_y'] * g['scale'] ** 2)
        q_codex = c['I_bottom'] / c['delta_V'] * c['g_to_q']
        cons = abs(c['I_bottom'] + c['I_top']) / max(abs(c['I_bottom']), abs(c['I_top']))
        chk(f'D1 실제 증서 — 수치 인증 통과 (보존 {cons:.3g} · 내부 잔차 {c["residual_rel"]:.3g} ≤ 1e−6 · 마지막 시도 pass) · q 재구성 (솔버 순서) {q!r} · '
            f'Codex 값 (I_b × g_to_q) {q_codex!r} — 3 ulp 차 (계산 순서) · 둘 다 > 1.5',
            q == 1.5370331988867805 and q_codex == 1.5370331988867802 and abs(q - q_codex) <= 16 * sys.float_info.epsilon * q
            and cons <= 1e-6 and c['residual_rel'] <= 1e-6 and c['attempts'][-1]['outcome'] == 'pass' and c['status'] == 'over_conduction_guard')
        chk('D2 ★ 옛 레코드 (sigma_full_reason solve_failed · 옛 생산자) = 계속 차단 — 공용 기술 검사 solver_guard · 옛 증서는 모형 한계 증서 판정도 거부 '
            '(q_withheld · 정책 · Σg 없음 — 옛 13 건과 함께 unknown · 사후 재분류 금지 · Q3 (가))',
            (tf.ion_record_problem(old) or ('',))[0] == 'solver_guard' and mlc is not None and isinstance(mlc(c), str) and 'q_withheld' in mlc(c),
            repr((tf.ion_record_problem(old), mlc(c) if mlc else None)))

    _guard('D', sD)

    # ══ V. 배포 빌더 (lhs_release_build) ═══════════════════════════════════════════════════════════════════════════
    def sV():
        import lhs_release_build as LRB
        rp = {'case_id': 'synthetic_P', 'f_ion_physics': '', 'tau2_ion_physics': '', 'tau_ion_physics': '',
              'ion_net_status_physics': 'NOT_COMPUTED', 'ion_net_status_reason_physics': ML}
        rt = dict(rp, case_id='synthetic_T', ion_net_status_reason_physics='solver_guard')
        chk('V1 ★ 빈칸 뜻 — physics 모형 한계 = NA_MODEL_LIMIT (옛: 기술 실패 NOT_COMPUTED 로 표지) · 기술 실패 = NOT_COMPUTED 그대로 · 사전에 코드 있음',
            'NA_MODEL_LIMIT' in LRB.V13_BLANK_CODES and LRB.v13_blank_reason(rp, 'f_ion_physics') == 'NA_MODEL_LIMIT'
            and LRB.v13_blank_reason(rp, 'tau2_ion_physics') == 'NA_MODEL_LIMIT' and LRB.v13_blank_reason(rt, 'f_ion_physics') == 'NOT_COMPUTED'
            and LRB.v13_blank_reason(rp, 'ion_net_status_reason_physics') is None)
        cols = ['case_id', 'f_ion_physics', 'tau2_ion_physics', 'tau_ion_physics', 'ion_net_status_physics', 'ion_net_status_reason_physics']
        chk('V2 physics 부록 행 (모형 한계 · 값 빈칸 + 사유) = 빈칸 일관성 통과 · 같은 행에 값이 남으면 거부',
            LRB.v13_blank_problems([rp], cols) == [] and bool(LRB.v13_blank_problems([dict(rp, f_ion_physics='0.5')], cols)))
        #  ★ 10-16 L214R-02 — 지금 생성기 인계 행은 FULL 모형 한계 독립 표지 두 칸 (full_model_limit_hertz · _physics — 'True' · 'False') 을 늘 싣는다 ·
        #    관문은 그 칸이 없는 행을 fail-closed 로 거부한다 (test_l214r02 D4) → 이 행들도 그 칸을 단다 (값 = 그 행의 상태와 같은 사실)
        rh = {'case_id': 'synthetic_H0', 'ion_net_status_hertz': 'NOT_COMPUTED', 'ion_net_status_reason_hertz': ML, 'percolation_pct': '100.0',
              'full_model_limit_hertz': 'True', 'full_model_limit_physics': 'True'}
        rh_ok = {'case_id': 'synthetic_ok', 'ion_net_status_hertz': 'OK', 'ion_net_status_reason_hertz': '', 'percolation_pct': '100.0',
                 'ion_net_status_physics': 'NOT_COMPUTED', 'ion_net_status_reason_physics': ML,
                 'full_model_limit_hertz': 'False', 'full_model_limit_physics': 'True'}
        gate = getattr(LRB, 'v13_primary_model_limit_problems', None)
        chk('V3 ★ 주 타깃 Hertz (H0) 모형 한계 = v1.3 주 타깃 배포 HOLD (실행 가능한 관문 · Q2 (가)) · physics 만 모형 한계 = 통과 (부록 공란)',
            gate is not None and bool(gate([rh])) and gate([rh_ok]) == [] and 'HOLD' in ' '.join(gate([rh])))
        try:
            cls = LRB._v13_class(rh)
        except Exception as e:                                        # noqa: BLE001
            cls = f'{type(e).__name__}: {e}'
        chk(f"V4 관통 분류 — Hertz 모형 한계 행은 관통 (그래프 관통 · percolation 100) = '1' (옛: 빈칸 + NOT_COMPUTED — 기술 실패로 읽힘) {cls!r}",
            cls == ('1', ''))

    _guard('V', sV)

    print(f'\ntest_lhs214_model_limit: {_ok}/{_ok + len(_fail)} PASS' + (f'   FAILED: {_fail}' if _fail else ''))
    return 0 if not _fail else 1


if __name__ == '__main__':
    if '--selftest' in sys.argv or len(sys.argv) == 1:          # 등재 진입점 (docs/reviews/selftest_inventory.tsv · 드라이버 --run-fast)
        sys.exit(main(sys.argv[1:]))
    sys.stderr.write('사용: python3 scripts/test_lhs214_model_limit.py [--selftest]\n')
    sys.exit(2)
