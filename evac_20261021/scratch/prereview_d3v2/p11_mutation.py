#!/usr/bin/env python3
"""PRE-D3V2 탐침 11 — 규칙 검사 C01–C17 의 변이 시험.  v2 규칙 (RulesV2) 을 한 자리씩 설계 v2 문장과 다르게 만든 변이체로
해당 검사를 다시 돌린다.  변이체가 여전히 (잡음 · 대조 통과) 면 '생존' = 그 검사는 그 자리를 시험하지 않는다.

재실행: python3 -I p11_mutation.py      (몬테카를로 검사 C04 · C14 를 포함 — 수 분)
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pcommon  # noqa: E402

c = pcommon.load_checks()
V2 = c.RulesV2


def mut(name, **methods):
    return type(name, (V2,), dict(methods, name='v2'))


def b_no_tol(self, x1, w1, x2, w2, ratios, tol):          # 허용 비교를 뺌 (dr > 0 이면 확인)
    dr = abs(ratios[0] - ratios[1])
    dmin = (w1 + w2) / dr if dr > 0 else float('inf')
    if abs(x1 - x2) > w1 + w2:
        return dict(status='F5', certifies_friction=False, dmin=dmin)
    if dr > 0:
        return dict(status='통과', certifies_friction=True, dmin=dmin)
    return dict(status='일치 미검사', certifies_friction=False, dmin=dmin)


def b_half(self, x1, w1, x2, w2, ratios, tol):            # 검출 한계 식에서 w2 를 뺌
    dr = abs(ratios[0] - ratios[1])
    dmin = w1 / dr if dr > 0 else float('inf')
    if abs(x1 - x2) > w1 + w2:
        return dict(status='F5', certifies_friction=False, dmin=dmin)
    if dmin <= tol:
        return dict(status='통과', certifies_friction=True, dmin=dmin)
    return dict(status='일치 미검사', certifies_friction=False, dmin=dmin)


def acc_half_interp(self, xs, I, u, mm, u_exp, nu=None, t_exp=2.0, interp=True, **kw):   # 보간 오차 ½ |ΔI|
    if any(v is None for v in u):
        return None
    tD = 2.0 if nu is None else c.t975(nu)
    segs = []
    for k in range(len(xs) - 1):
        uc = max(u[k], u[k + 1])
        band = math.sqrt((t_exp * u_exp) ** 2 + (tD * uc) ** 2) + (0.5 * abs(I[k + 1] - I[k]) if interp else 0.0)
        s = c.seg_within(xs[k], xs[k + 1], I[k], I[k + 1], mm, band)
        if s:
            segs.append(s)
    comps = c.merge(segs)
    return dict(comps=comps, side=None if comps else c.side_of(xs, I, mm))


def acc_t2(self, xs, I, u, mm, u_exp, nu=None, t_exp=2.0, interp=True, **kw):            # t(ν) 대신 2
    return V2.accept(self, xs, I, u, mm, u_exp, nu=None, t_exp=t_exp, interp=interp)


def acc_min_u(self, xs, I, u, mm, u_exp, nu=None, t_exp=2.0, interp=True, **kw):         # u_칸 = 두 끝 중 작은 쪽
    if any(v is None for v in u):
        return None
    tD = 2.0 if nu is None else c.t975(nu)
    segs = []
    for k in range(len(xs) - 1):
        uc = min(u[k], u[k + 1])
        band = math.sqrt((t_exp * u_exp) ** 2 + (tD * uc) ** 2) + (abs(I[k + 1] - I[k]) if interp else 0.0)
        s = c.seg_within(xs[k], xs[k + 1], I[k], I[k + 1], mm, band)
        if s:
            segs.append(s)
    comps = c.merge(segs)
    return dict(comps=comps, side=None if comps else c.side_of(xs, I, mm))


def anchor_largest(self, A1, A2):                          # F9 대신 가장 큰 성분을 앵커
    for A, nm in ((A1, 'T1'), (A2, 'T2')):
        if not A['comps']:
            return dict(status='F10', side=f'{nm} {A.get("side") or "?"}')
    C = c.intersect(A1['comps'], A2['comps'])
    if not C:
        return dict(status='F5')
    a, b = max(C, key=lambda p: p[1] - p[0])
    return dict(status='anchor', x=0.5 * (a + b), comps=C)


def u_no_sqrt(self, seeds_by_level):                       # u = s_pool (√n 나눗셈 뺌)
    u, how = V2.u_dem(self, seeds_by_level)
    multi = [v for v in seeds_by_level if len(v) >= 2]
    if not multi:
        return u, how
    return [x * math.sqrt(len(v)) if x is not None else None for x, v in zip(u, seeds_by_level)], how


def t2_resid_only(self, xs_pts, ys_pts, d, wrap_frac):     # 벽 두름 기준 뺌
    ang, rms = c.line_fit(xs_pts, ys_pts)
    return dict(status='관측 불가' if rms > self.EPS_FIT_D * d else '각', angle=ang)


def t2_wrap_only(self, xs_pts, ys_pts, d, wrap_frac):      # 잔차 기준 뺌
    ang, rms = c.line_fit(xs_pts, ys_pts)
    return dict(status='관측 불가' if wrap_frac > self.F_WRAP else '각', angle=ang)


def transfer_bogus(self):                                  # 구간 표지만 · 내용 없음
    return dict(value='center', interval=True, G='?', convention='?')


def order_no_key(self, seq):                               # 열쇠 커밋 제약 뺌
    idx = {e: i for i, e in enumerate(seq)}
    need = ('S3a_commit', 'measure_start', 'measure_end', 'raw_push_enc', 'S3b_commit', 'curve_seal', 'raw_open')
    if any(e not in idx for e in need):
        return False
    ok = (idx['S3a_commit'] < idx['measure_start'] < idx['measure_end'] < idx['raw_push_enc'] < idx['raw_open']
          and idx['S3b_commit'] < idx['curve_seal'] < idx['raw_open'])
    if 'raw_push_plain' in idx:
        ok = ok and idx['raw_push_plain'] > idx['raw_open']
    return ok


def order_no_s3b(self, seq):                               # S3b < 봉인 제약 뺌
    idx = {e: i for i, e in enumerate(seq)}
    need = ('S3a_commit', 'measure_start', 'raw_open')
    if any(e not in idx for e in need):
        return False
    ok = idx['S3a_commit'] < idx['measure_start'] < idx['raw_open']
    if 'raw_push_plain' in idx and 'curve_seal' in idx:
        ok = ok and idx['raw_push_plain'] > idx['curve_seal']
    return ok


def include_no_support(self, run, supported):              # 검사기 지원 여부 뺌
    return run['overlap'] is not None and run['overlap'] <= 1.0


def deck_bogus(self):                                      # 상 셋 · 드럼 표지만 (AM 개수 · 물성 블록 무관)
    return dict(phases=('AM_P', 'AM_S', 'SE'), drum='anything')


def f3_no_sat(self, xs, I, f, mm, band, ceiling):          # '위 포화' 갈래 뺌
    if mm > max(I) + band:
        return dict(status='확장', level=c.EXT_FACTOR * ceiling)
    return V2.f3(self, xs, I, f, mm, band, ceiling)


def f3_ext_at_ceiling(self, xs, I, f, mm, band, ceiling):  # 위 확장 = 천장 그대로 (0.95 대신 1.0)
    r = V2.f3(self, xs, I, f, mm, band, ceiling)
    if r['status'] == '확장' and mm > max(I):
        r = dict(status='확장', level=ceiling)
    return r


def uexp_t2(self, days, u_read):                           # t(날 − 1) 대신 2
    dm = [sum(dd) / len(dd) for dd in days]
    nd = len(dm)
    return sum(dm) / nd, math.sqrt((2.0 * c.sd(dm) / math.sqrt(nd)) ** 2 + (2.0 * u_read) ** 2)


def defs_bogus(self):                                      # 정의 = 자리 표지만
    return {k: 'x' for k in c.RulesV1().definitions()}


MUTANTS = [
    ('M01a 허용 비교 뺌 (dr>0 이면 확인)', 'C01', mut('M01a', b_check=b_no_tol)),
    ('M01b 검출 한계 식 w₂ 뺌', 'C01', mut('M01b', b_check=b_half)),
    ('M02a 보간 오차 ½|ΔI|', 'C02', mut('M02a', accept=acc_half_interp)),
    ('M02b 세분 안 함 (R_MAX 0)', 'C02', mut('M02b', R_MAX=0)),
    ('M02c u_칸 = 작은 쪽', 'C02', mut('M02c', accept=acc_min_u)),
    ('M03a F9 대신 가장 큰 성분 앵커', 'C03', mut('M03a', anchor=anchor_largest)),
    ('M04a t(ν) 대신 2', 'C04', mut('M04a', accept=acc_t2)),
    ('M04b u = s_pool (√n 뺌)', 'C04', mut('M04b', u_dem=u_no_sqrt)),
    ('M06a 벽 두름 기준 뺌', 'C06', mut('M06a', t2_angle=t2_resid_only)),
    ('M06b 맞춤 잔차 기준 뺌', 'C06', mut('M06b', t2_angle=t2_wrap_only)),
    ('M07a 이전 명세 = 표지만', 'C07', mut('M07a', transfer=transfer_bogus)),
    ('M08a 열쇠 커밋 제약 뺌', 'C08', mut('M08a', order_ok=order_no_key)),
    ('M08b S3b · 봉인 제약 뺌', 'C08', mut('M08b', order_ok=order_no_s3b)),
    ('M10a 검사기 지원 여부 뺌', 'C10', mut('M10a', include_run=include_no_support)),
    ('M11a 시험 덱 = 표지만', 'C11', mut('M11a', test_deck=deck_bogus)),
    ('M13a 위 포화 갈래 뺌', 'C13', mut('M13a', f3=f3_no_sat)),
    ('M13b 위 확장 = 천장 그대로', 'C13', mut('M13b', f3=f3_ext_at_ceiling)),
    ('M14a t(날−1) 대신 2', 'C14', mut('M14a', u_exp_band=uexp_t2)),
    ('M17a 정의 = 자리 표지만', 'C17', mut('M17a', definitions=defs_bogus)),
]
fn = dict(c.CHECKS)
rows = []
for label, cid, M in MUTANTS:
    caught, ok, det = fn[cid](M())
    rows.append(dict(mutant=label, check=cid, caught=caught, control_ok=ok, survives=bool(caught and ok), detail=det))
    print(f"{'생존' if caught and ok else '잡힘'} · {cid} · {label} — {det[:160]}")
pcommon.dump('p11_mutation.json', rows)
print(f"\n생존 {sum(r['survives'] for r in rows)} / {len(rows)}")
