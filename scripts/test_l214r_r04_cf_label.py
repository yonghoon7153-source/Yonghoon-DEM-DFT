#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L214R-R04 (10-18 같은 부류 점검 · 1저자 10-19 Q1 *"q1 한다음에 하자"*) — 숫자를 싣는 이온 가지의 표지 (상태 · 사유) ↔ 증서 재구성 q (시험 먼저).

  python3 scripts/test_l214r_r04_cf_label.py          # 종료코드 0 = 전부 PASS

근거 = 수정 계획 `docs/reviews/lhs214rr_fix_plan_20261018.md` §5 · 원장 `L214R-R04`.  생산자 규칙 (`network_conductivity.solve_network` · `_net_sigma_status`):
CF (bulk_only) · 협착-only (constriction_only) — 반올림 전 q > 1.5 (엄격) 면 값 유지 + (model_over_conduction · q_gt_1p5) · 그 밖 (computed · None) /
FULL — 게시는 (computed · None) 만 (q > 1.5 = 보류 · L214R-R01).  증서 (solve_info) 의 상태 · 사유도 같다.

★ 시험 먼저 — 고치기 전 코드 (`f8871224b` · `b2681cfec`) 에서 빨갛다: 게시 증서 판정 (`tau_flux._cert_published_problem`) 은 숫자를 싣는 가지의 상태가 게시 상태
  둘 중 하나인지 · 증서 상태 = 가지 상태인지만 보고 q ↔ 표지를 대조하지 않았다 → 표지를 (증서와 함께) 바꾼 레코드를 받았다 (값 그대로 · 해석 표지만 반전).
  값은 거부하지 않는다 (Codex 재확인 판정 §1-4) — 표지가 생산자 규칙과 맞는가만 본다.
  R  레코드 단 — test_l214r02 의 12 침대 (띠 L0 · L1 · L2 · 실 생산자) × 세 모드: R0 원 레코드 [] / R1 CF · 협착-only model_over_conduction → computed
     (가지 상태 · 사유 · 증서 상태 · 사유) 거부 / R2 computed → model_over_conduction 거부 / R3 사유만 (가지 · 증서 각각) 바꿈 거부 / R4 FULL computed 의
     사유만 q_gt_1p5 로 (가지 · 증서 · 둘 다) 거부 / R5 세대 계약 invalid (그 모드 cert) / R6 τ 행 그 모드 NOT OK / R7 레코드 판정 (network_record_verdict) 거부
  E  경계 — 3 노드 실제 풀이 (bulk_only plate 0.3 · 협착-only 0.45 의 prev · eq · next) 의 생산자 표지 그대로 = 통과 · 표지만 반대로 = 거부
  C  대조 — 보류 FULL 복원 (L214R-R01) 은 R01 사유 하나 (표지 사유를 겹치지 않는다) · 원 레코드의 열 · 전자 채널 그대로 · FULL 상태를
     model_over_conduction 으로 바꾼 레코드 = 공용 기술 검사 (`ion_record_problem` — FULL 상태 계약) 가 이미 거부 (고치기 전에도 · 이 수정과 무관)
⚠ 범위 — 계약 시험 (합성 사슬 · 물리 침대 아님).  τ 인계 (FULL 만) 수치에는 원래 영향 없다 — 해석 표지 (배포 빈칸 뜻 · 화면 과전도 표지) 의 무결성.
  전자 · 열 채널의 CF 표지 = 이 검사 밖 (공용 증서 판정 = 이온 세 가지 · `tau_flux` 정책 절).
"""
import contextlib
import copy
import io
import math
import sys
import tempfile
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
for _p in (str(HERE), str(ROOT / 'webapp')):
    if _p not in sys.path:
        sys.path.insert(0, _p)

MOC, QG = 'model_over_conduction', 'q_gt_1p5'
MODES = ('hertz', 'physics', 'hertz_h12')
VALUE_OK = ('OK', 'MODEL_BELOW_CONTINUUM_BOUND')
_ok, _fail = 0, []


def chk(name, cond, extra=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'   {str(extra)[:500]}' if extra else ''))


def quiet(fn, *a, **kw):
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return fn(*a, **kw)


def mode_rec(dual, m):
    return dual['physics'] if m == 'physics' else (dual['hertzian'] if m == 'hertz' else dual['hertzian']['hertz_h12'])


def relabel(rec, sk, rk, ck, to, branch_reason=True, cert_reason=True):
    """표지 바꿈 — 가지 상태 · 증서 상태는 늘 · 사유는 인자대로 (to 의 생산자 사유)."""
    rsn = QG if to == MOC else None
    rec[sk] = to
    rec[ck]['status'] = to
    if branch_reason:
        rec[rk] = rsn
    if cert_reason:
        rec[ck]['reason'] = rsn


def slot(probs, ck):
    return [p for p in probs if p.startswith(ck)]


def main():
    import network_conductivity as nc
    import tau_flux as tf
    import pipeline_service as ps
    import dem_analysis_core as dac
    from test_l214r02_model_limit_flag import BEDS, bed, produce, ledger
    from test_l214r_r01_restored_full import write_record_folder, restore
    tmp = Path(tempfile.mkdtemp(prefix='l214rr04_'))
    try:
        print('R  레코드 단 — 12 침대 × 세 모드 (실 생산자)')
        duals = {}
        for name in BEDS:
            b = bed(name)
            led, pp = ledger(dac, b)
            duals[name] = (quiet(produce, nc, b), led, pp)
        bad0, seen = {}, {'moc': 0, 'computed': 0, 'full': 0}
        flips = []                                               # (name, m, branch, sk, rk, ck, from)
        for name, (du, _l, _p) in duals.items():
            for m in MODES:
                r = mode_rec(du, m)
                pr = tf.certificate_binding_problems(m, r)
                if pr:
                    bad0[(name, m)] = pr[:1]
                for branch, qk, dk, sk, rk, ck in tf.CERT_BRANCH_KEYS:
                    st = r.get(sk)
                    if st not in tf.CERT_PUBLISHED_STATES:
                        continue
                    if branch == 'full':
                        seen['full'] += 1
                    else:
                        seen['moc' if st == MOC else 'computed'] += 1
                    flips.append((name, m, branch, sk, rk, ck, st))
        chk(f'R0 원 레코드 = 생산자 출력 그대로 통과 (결합 []) · 게시 가지 FULL computed {seen["full"]} · CF / 협착-only model_over_conduction {seen["moc"]} · '
            f'computed {seen["computed"]}', not bad0 and seen['moc'] >= 20 and seen['computed'] >= 20 and seen['full'] >= 12, bad0)
        acc = {'R1': {}, 'R2': {}, 'R3': {}, 'R4': {}, 'R5': {}, 'R6': {}, 'R7': {}, 'C3': {}}
        n_r7 = 0
        for i, (name, m, branch, sk, rk, ck, st) in enumerate(flips):
            du0, led, pp = duals[name]
            if branch == 'full':                                 # R4 (사유만) · C3 (상태 바꿈 = 기존 기술 검사)
                for which in ('branch', 'cert', 'both'):
                    d4 = copy.deepcopy(du0)
                    r4 = mode_rec(d4, m)
                    if which in ('branch', 'both'):
                        r4[rk] = QG
                    if which in ('cert', 'both'):
                        r4[ck]['reason'] = QG
                    if not slot(tf.certificate_binding_problems(m, r4), ck):
                        acc['R4'][(name, m, which)] = '수용'
                dc = copy.deepcopy(du0)
                relabel(mode_rec(dc, m), sk, rk, ck, MOC)
                row = tf.ion_columns(dc, led, pp)
                if tf.ion_record_problem(mode_rec(dc, m)) is None or row.get(f'ion_net_status_{m}') in VALUE_OK:
                    acc['C3'][(name, m)] = (tf.ion_record_problem(mode_rec(dc, m)), row.get(f'ion_net_status_{m}'))
                continue
            to = 'computed' if st == MOC else MOC
            key = (name, m, branch)
            d2 = copy.deepcopy(du0)
            relabel(mode_rec(d2, m), sk, rk, ck, to)
            probs = slot(tf.certificate_binding_problems(m, mode_rec(d2, m)), ck)
            tag = 'R1' if st == MOC else 'R2'
            if not probs:
                acc[tag][key] = mode_rec(du0, m).get('sigma_bulk_net' if branch == 'bulk_only' else 'sigma_constr_net')
            con = tf.network_generation_contract(d2)
            if not (con.get('generation') == 'invalid' and any(mm == m and kind == 'cert' for mm, kind, _d in con.get('problems') or [])):
                acc['R5'][key] = (con.get('generation'), [(mm, kind) for mm, kind, _d in con.get('problems') or []])
            row = tf.ion_columns(d2, led, pp)
            if row.get(f'ion_net_status_{m}') in VALUE_OK:
                acc['R6'][key] = row.get(f'ion_net_status_{m}')
            if i % 5 == 0:                                       # 레코드 판정 (네 사본 · 파일 쓰기) — 다섯 중 하나 (침대 · 모드 · 가지 종류에 걸친다)
                n_r7 += 1
                ok_r, why_r = ps.network_record_verdict(str(write_record_folder(tmp / f'r{i}', d2)))
                if ok_r or 'L214R-R04' not in why_r:
                    acc['R7'][key] = (ok_r, why_r[:160])
            for which in ('branch', 'cert'):                     # R3 — 사유만 (가지 또는 증서) 를 반대 표지의 사유로
                d3 = copy.deepcopy(du0)
                r3 = mode_rec(d3, m)
                wrong = None if st == MOC else QG
                if which == 'branch':
                    r3[rk] = wrong
                else:
                    r3[ck]['reason'] = wrong
                if not slot(tf.certificate_binding_problems(m, r3), ck):
                    acc['R3'][key + (which,)] = (st, wrong)
        n_full = sum(1 for f in flips if f[2] == 'full')
        chk(f'R1 ★ model_over_conduction (raw q > 1.5) → computed (가지 · 증서 상태 · 사유) → 거부 (옛: 51 수용) — 수용 {len(acc["R1"])}', not acc['R1'], acc['R1'])
        chk(f'R2 ★ computed (raw q ≤ 1.5) → model_over_conduction → 거부 (옛: 21 수용) — 수용 {len(acc["R2"])}', not acc['R2'], acc['R2'])
        chk(f'R3 ★ 사유만 반대 표지의 사유로 (가지 사유 · 증서 사유 각각 — 상태 그대로) → 거부 — 수용 {len(acc["R3"])}', not acc['R3'], acc['R3'])
        chk(f'R4 ★ FULL computed ({n_full} 가지) 의 사유만 q_gt_1p5 로 (가지 · 증서 · 둘 다 — 생산자 FULL 게시 = computed · 사유 없음) → 거부 (옛: 수용) — '
            f'수용 {len(acc["R4"])}', n_full >= 12 and not acc['R4'], acc['R4'])
        chk('R5 ★ 표지 바꾼 레코드 → 세대 계약 invalid · 그 모드에 cert 문제 (정지 계약 ⑨ · 다시 읽기 K2 · 인계 · 배포가 부르는 같은 함수)', not acc['R5'], acc['R5'])
        chk('R6 ★ τ 행 (ion_columns) — 그 모드 NOT OK (세대 invalid → 값 공란)', not acc['R6'], acc['R6'])
        chk(f'R7 ★ 레코드 판정 (network_record_verdict — 네 사본 · 세대 계약 · {n_r7} 레코드) 거부 · 사유에 L214R-R04', n_r7 >= 10 and not acc['R7'], acc['R7'])
        state_c3 = acc['C3']

        print('E  경계 (3 노드 실제 풀이 · 함수 단 — 결합 정보를 붙여 게시 증서 판정에 직접)')
        from test_lhs214_model_limit import net3
        res = {}
        for mode, base in (('bulk_only', 0.3), ('constriction_only', 0.45)):
            rk = tf.CERT_BRANCH_REASON_KEY[mode] if hasattr(tf, 'CERT_BRANCH_REASON_KEY') else {b: r_ for b, _q, _d, _s, r_, _c in tf.CERT_BRANCH_KEYS}[mode]
            for lab, pz in (('prev', math.nextafter(base, 0.0)), ('eq', base), ('next', math.nextafter(base, 1.0))):
                n = net3(plate_z=pz)
                g, q = quiet(nc.solve_network, n, mode=mode)
                cert = copy.deepcopy(n['solve_info'][mode])
                st, rsn = cert['status'], cert.get('reason')
                cert.update(channel='ionic', role='H0', contact_mode='hertzian', sigma_bulk_S_cm=.003)
                args = ('hertz', mode)
                ok_ = tf._cert_published_problem(*args, {'sigma_grain_S_cm': .003, rk: rsn}, round(q, 8), round(q * .003 * 1000, 6), st, cert)
                flip = 'computed' if st == MOC else MOC
                frs = QG if flip == MOC else None
                cert2 = dict(cert, status=flip, reason=frs)
                bad_ = tf._cert_published_problem(*args, {'sigma_grain_S_cm': .003, rk: frs}, round(q, 8), round(q * .003 * 1000, 6), flip, cert2)
                res[(mode, lab)] = (q, st, rsn, ok_, bad_)
        chk(f'E1 ★ 생산자 표지 그대로 = 통과 (raw q 1.5 = computed · 다음 수 1.5000000000000002 = model_over_conduction) · 표지만 반대로 = 거부 '
            f'{ {k: (v[0], v[1], v[3] is None, isinstance(v[4], str)) for k, v in res.items()} }',
            all(v[3] is None and isinstance(v[4], str) and 'L214R-R04' in v[4] for v in res.values())
            and all(res[(md, 'next')][1] == MOC and res[(md, 'next')][2] == QG and res[(md, 'eq')][1] == 'computed' and res[(md, 'eq')][2] is None
                    for md in ('bulk_only', 'constriction_only'))
            and all(res[(md, 'next')][0] == math.nextafter(1.5, 2.0) and res[(md, 'eq')][0] == 1.5 for md in ('bulk_only', 'constriction_only')))

        print('C  대조')
        withheld = [(n_, m) for n_, (du, _l, _p) in duals.items() for m in MODES
                    if mode_rec(du, m).get('sigma_full_status') == 'not_computed' and mode_rec(du, m).get('sigma_full_reason') == 'full_over_conduction']
        bad1 = {}
        for n_, m in withheld:
            dw = copy.deepcopy(duals[n_][0])
            restore(mode_rec(dw, m), m)
            fp = slot(tf.certificate_binding_problems(m, mode_rec(dw, m)), 'solve_certificate_full')
            if not (len(fp) == 1 and nc.MODEL_LIMIT_POLICY in fp[0] and 'L214R-R04' not in fp[0]):
                bad1[(n_, m)] = [p[:200] for p in fp]
        chk(f'C1 보류 FULL 복원 ({len(withheld)} 칸 · L214R-R01) → R01 사유 하나 (생산자 정책) · 표지 사유를 겹치지 않는다', len(withheld) == 18 and not bad1, bad1)
        bad2 = {}
        for n_, (du, _l, _p) in duals.items():
            for m in ('hertz', 'physics'):
                r = mode_rec(du, m)
                for ch in ('electronic', 'thermal'):
                    v = ps.channel_verdict(r, ch, m)
                    if v[0] not in ('ok', 'not_percolating', 'valid_zero') and not str(v[0]).startswith('ok'):
                        bad2[(n_, m, ch)] = v
        chk('C2 원 레코드의 전자 · 열 채널 판정 그대로 (이 검사 밖 — 이온 세 가지만)', not bad2, bad2)
        chk(f'C3 FULL 상태를 model_over_conduction 으로 바꿈 ({n_full} 가지) → 공용 기술 검사 거부 · τ 행 NOT OK (고치기 전에도 · 그대로)', not state_c3, state_c3)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f'\ntest_l214r_r04_cf_label: {_ok}/{_ok + len(_fail)} PASS' + (f'   FAILED: {_fail}' if _fail else ''))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
