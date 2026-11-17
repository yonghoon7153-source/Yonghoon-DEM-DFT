#!/usr/bin/env python3
"""vuquoc1999_nfd_reproduce.py — Vu-Quoc & Zhang (1999) 탄소성 법선 접촉 (NFD) 모델 재구현 + 그림 판독.

카드: litdb/papers/vuquoc1999_elastoplastic_normal_contact_force_displacement_model.md
원문: L. Vu-Quoc, X. Zhang, "An elastoplastic contact force-displacement model in the normal direction:
      displacement-driven version", Proc. R. Soc. Lond. A 455 (1999) 4013-4044 (JSTOR 스캔판 · PDF 33 쪽 ·
      PDF 1 쪽 = JSTOR 표지 · PDF 쪽 p ↔ 인쇄 쪽 4011 + p).

무엇을 하나
  1) 모델 = 식 (3.7)-(3.22) + 알고리즘 3.2 / 3.3 (같은 구 두 개 꼴 · R · E · ν · σ_Y) 을 그대로 옮긴다.
     ⚠ 인쇄된 (3.17) 의 둘째 항은 (1/3)c1 (P)(P)^(-2/3) 로 P 가 한 번 더 붙어 있다 — (3.15) 를 미분하면
       (1/3)c1 P^(-2/3) 이다.  여기서는 미분대로 쓴다 (뉴턴 수렴 속도만 바뀌고 해는 같다).
     ⚠ C_a 의 단위는 원문에 'N m^-1' 로 인쇄 — 식 (2.5) 가 a^p (m) = C_a<P - P_Y> 이므로 m N^-1 로 읽는다.
  2) Thornton (1997) 모델을 원문이 쓴 꼴로: 구 ↔ 강체 평판 (R* = R · E* = E/(1-ν²)) · p_y = 1.61 σ_Y ·
     소성 가지 P = P_Y + π p_y R*(α − α_Y) · 제하 = 반지름 R_p* 의 Hertz.  ⚠ R_p* 식은 이 논문에 인쇄돼 있지
     않다 — Thornton & Ning (1998) 식 (28) (정본 카드 thorntonning1998_adhesive_elastoplastic_contact) 을 빌린다.
  3) §4 충돌 (식 4.1-4.7 · leap-frog · Δt 1.0e-6 s · 중력 없음) 을 돌려 원문 인쇄값과 맞춘다 (--selftest).
  4) --digitize <pdf> : 원 래스터 (600 dpi JBIG2) 에서 그림 20 표지 (범례 표지 틀 맞춤) · 그림 10 / 16 의 마지막
     하중 0 표지 · 그림 17 일점쇄선 · 그림 12 직선 높이를 읽어 CSV 로.  눈금 보정 값 (pt) 은 아래 CAL 에
     적었다 (틀 선 · 눈금 막대 위치를 원 래스터에서 잰 값).

usage
  python3 tools/litdb/vuquoc1999_nfd_reproduce.py --selftest
  python3 tools/litdb/vuquoc1999_nfd_reproduce.py --sweep                  # 충돌 0.02-0.20 m/s 표
  python3 tools/litdb/vuquoc1999_nfd_reproduce.py --digitize litdb/inbox/<pdf> --out litdb/figures/<slug>/digitized.csv

못 하는 것
  · FEA 를 다시 풀지 않는다 (ABAQUS 5.4 축대칭 · CAX6 2141 개) — FEA 값은 그림 판독뿐.
  · 재재하 (제하 뒤 다시 누름) 는 알고리즘 3.2 그대로 처녀 적재 식을 다시 쓴다 (원문에 재재하 가지 없음).
"""
import argparse
import csv
import math
import sys

# ---- 원문 §2 · §4 의 입력 (인쇄값) ----
R, E, NU, SY = 0.1, 7.0e10, 0.3, 1.0e8          # p.4021: R 0.1 m · E 70 GPa · ν 0.3 · σ_Y 100 MPa (알루미늄 합금)
AY = 1.61                                       # p.4031: A_Y(0.3) ≈ 1.61
CA, KC = 2.33e-7, 2.69e-4                       # p.4027 (C_a · 'N m^-1' 로 인쇄 → m/N) · p.4029 (K_c · N^-1)
RHO = 2.699e3                                   # p.4036: ρ (알루미늄) → m = 11.306 kg
M = RHO * 4.0 / 3.0 * math.pi * R ** 3          # (4.1)

PY = math.pi ** 3 * R ** 2 * (1 - NU ** 2) ** 2 * (AY * SY) ** 3 / (6 * E ** 2)     # (3.7)
AYR = (3 * PY * R * (1 - NU ** 2) / (4 * E)) ** (1 / 3)                              # (3.8) a_Y
ALY = AYR ** 2 / R                                                                   # (3.9) α_Y
C1 = (1 / CA) * (3 * R * (1 - NU ** 2) / (4 * E)) ** (1 / 3)                         # (3.14)


def a_e(P):                       # (1.7) Hertz 반지름 (같은 구 두 개)
    return (3 * P * R * (1 - NU ** 2) / (4 * E)) ** (1 / 3)


def c_r(P):                       # (3.6)
    return 1.0 + KC * max(P - PY, 0.0)


def resid(P, al):                 # (3.15)
    return (P - PY) + C1 * P ** (1 / 3) - (1 / CA) * (c_r(P) * R * al) ** 0.5


def dresid(P, al):                # (3.15) 의 미분 (인쇄 (3.17) 의 둘째 항 P 하나 덜어냄)
    return 1 + C1 / 3 * P ** (-2 / 3) - (1 / (2 * CA)) * KC * R ** 0.5 * al ** 0.5 / c_r(P) ** 0.5


def loading_force(al, guess=None, tol=0.005, maxit=60):
    """처녀 적재 가지: α ≤ α_Y → (3.10) Hertz · α > α_Y → (3.15) 뉴턴 (판정 = 상대 증분 ≤ 0.005, 식 4.8)."""
    if al <= ALY:
        return 4 * E * R ** 0.5 / (3 * (1 - NU ** 2)) * al ** 1.5, 0
    P = guess if (guess and guess > PY) else PY * (al / ALY)
    for it in range(1, maxit + 1):
        Pn = P - resid(P, al) / dresid(P, al)
        if Pn <= 0:
            Pn = 0.5 * P
        if abs(Pn - P) / Pn <= tol:
            return Pn, it
        P = Pn
    return P, maxit


def quasi_static(Pmax):
    """정적 한 주기 (P_max 까지 적재 → 0 까지 제하) 의 α_max · α_res (식 2.3 · 2.5 · 3.5 · 3.19)."""
    ae, ap = a_e(Pmax), CA * max(Pmax - PY, 0.0)
    al_max = (ae + ap) ** 2 / (c_r(Pmax) * R)
    al_res = al_max - ae ** 2 / (c_r(Pmax) * R)
    return dict(a_e=ae, a_p=ap, a_ep=ae + ap, C_R=c_r(Pmax), alpha_max=al_max, alpha_res=al_res)


class VZModel:
    """알고리즘 3.2 (변위 구동) — 입력 α_n · 출력 P_n."""

    def __init__(self):
        self.inc, self.prev, self.prev2, self.maxit = True, (0.0, 0.0), (0.0, 0.0), 0
        self.Pmax = self.alpha_max = self.alpha_res = None

    def force(self, al):
        (a1, P1), (a2, P2) = self.prev, self.prev2
        dal = al - a1
        if dal > 0:                                            # 줄 9-21 (재재하도 이 가지)
            self.inc = True
            guess = P1 + (P1 - P2) / (a1 - a2) * (al - a1) if a1 != a2 else None    # (3.18)
            P, it = loading_force(al, guess)
            self.maxit = max(self.maxit, it)
        elif dal < 0:                                          # 줄 22-33
            if self.inc:
                self.Pmax, self.alpha_max = P1, a1
                self.alpha_res = a1 - a_e(P1) ** 2 / (c_r(P1) * R)                   # (3.19)
                self.inc = False
            ae = (c_r(self.Pmax) * R * max(al - self.alpha_res, 0.0)) ** 0.5         # (3.21)
            P = 4 * E / (3 * R * (1 - NU ** 2)) * ae ** 3                            # (3.22)
        else:
            P = P1
        self.prev2, self.prev = self.prev, (al, P)
        return P


class ThorntonModel:
    """Thornton (1997) — 원문 그림 3 · 4 · 식 (1.11) · (1.12) 가 쓰는 꼴 (구 ↔ 강체 평판)."""

    def __init__(self):
        self.Es, self.py = E / (1 - NU ** 2), AY * SY
        self.inc, self.prev = True, (0.0, 0.0)
        self.alpha_res = None

    def loading(self, al):
        if al <= ALY:
            return 4 / 3 * self.Es * R ** 0.5 * al ** 1.5
        return PY + math.pi * self.py * R * (al - ALY)

    def unloading_setup(self, Ps, al_max):          # Thornton & Ning (1998) 식 (28) — 이 논문에 인쇄 안 됨
        self.Rp = (4 * self.Es / (3 * Ps)) * ((2 * Ps + PY) / (2 * math.pi * self.py)) ** 1.5
        self.alpha_res = al_max - (3 * Ps / (4 * self.Es * self.Rp ** 0.5)) ** (2 / 3)

    def force(self, al):
        a1, P1 = self.prev
        if al - a1 >= 0 and self.inc:
            P = self.loading(al)
        else:
            if self.inc:
                self.inc = False
                self.unloading_setup(P1, a1)
            P = 4 / 3 * self.Es * self.Rp ** 0.5 * max(al - self.alpha_res, 0.0) ** 1.5
        self.prev = (al, P)
        return P


def v_yield():                                     # (1.12) 구 ↔ 강체 평판 (R* = R · E* = E/(1-ν²) · m* = m)
    return 3.194 * ((AY * SY) ** 5 * R ** 3 / ((E / (1 - NU ** 2)) ** 4 * M)) ** 0.5


def e_thornton_111(vin):                           # (1.11)
    x = v_yield() / vin
    return ((6 / 5 * math.sqrt(3)) * (1 - x * x / 6)) ** 0.5 * (x / (x + 2 * math.sqrt(1.2 - 0.2 * x * x))) ** 0.25


def collide(model, vin, dt=1.0e-6):
    """§4(a): 중심-평판 거리 x · v_{1/2} = v_in · (4.2)-(4.5) · P 가 0 으로 떨어지면 분리 (p.4037)."""
    x, v, t, t0, Pmax, almax = R, -vin, 0.0, None, 0.0, 0.0
    last = None
    for _ in range(10 ** 6):
        x += v * dt
        t += dt
        al = R - x
        P = model.force(al) if al > 0 else 0.0
        if al > 0 and t0 is None:
            t0 = t
        if t0 is not None and (al <= 0 or (P <= 0.0 and not getattr(model, 'inc', True))):
            break
        v += (P / M) * dt
        Pmax, almax, last = max(Pmax, P), max(almax, al), t
    return dict(vout=v, e=v / vin, Pmax=Pmax, alpha_max=almax, tau=(last - t0) if last else None,
                alpha_res=model.alpha_res, newton_max=getattr(model, 'maxit', None))


def sweep():
    rows = []
    for k in range(1, 11):
        vin = round(0.02 * k, 2)
        a, b = collide(VZModel(), vin), collide(ThorntonModel(), vin)
        rows.append(dict(v_in=vin, v_in_over_vY=vin / v_yield(),
                         vz_e=a['e'], vz_vout=a['vout'], vz_Pmax_N=a['Pmax'], vz_Pmax_over_PY=a['Pmax'] / PY,
                         vz_alpha_max_m=a['alpha_max'], vz_alpha_res_m=a['alpha_res'], vz_tau_s=a['tau'],
                         vz_newton_max=a['newton_max'],
                         th_e=b['e'], th_e_eq111=e_thornton_111(vin), th_Pmax_N=b['Pmax'],
                         th_alpha_max_m=b['alpha_max'], th_alpha_res_m=b['alpha_res'], th_tau_s=b['tau']))
    return rows


def selftest():
    ok = True

    def chk(name, val, ref, tol):
        nonlocal ok
        good = abs(val - ref) <= tol
        ok &= good
        print(f"  {'⭕' if good else '❌'} {name}: {val:.6g} (원문 {ref:g} ± {tol:g})")

    print('selftest — 원문 인쇄값 재현 (카드 §3 · §4)')
    chk('P_Y (3.7) [N] p.4021', PY, 36.4, 0.1)
    chk('m (4.1) [kg] p.4036', M, 11.306, 0.002)
    chk('v_Y (1.12) [m/s] p.4040', v_yield(), 1.67e-3, 0.005e-3)
    a, b = collide(VZModel(), 0.04), collide(ThorntonModel(), 0.04)
    chk('v_in 0.04: 이 모델 v_out [m/s] 그림 19a', a['vout'], 0.0304, 0.0003)
    chk('v_in 0.04: 이 모델 e 그림 19b', a['e'], 0.7587, 0.002)
    chk('v_in 0.04: 이 모델 P_max [N] p.4038', a['Pmax'], 1435, 10)
    chk('v_in 0.04: 이 모델 τ [s] p.4038', a['tau'], 1.00e-3, 0.02e-3)
    chk('v_in 0.04: Thornton e p.4038', b['e'], 0.5331, 0.002)
    chk('v_in 0.04: Thornton P_max [N] p.4038', b['Pmax'], 957, 5)
    chk('v_in 0.04: Thornton τ [s] p.4038', b['tau'], 1.20e-3, 0.03e-3)
    chk('Thornton 모의 e = 식 (1.11) (p.4038) @0.04', b['e'], e_thornton_111(0.04), 0.001)
    P, _ = loading_force(1.56e-5)
    chk('변위 구동 α 1.56e-5 m: 이 모델 P [N] p.4034', P, 1495, 3)
    chk('변위 구동 α 1.56e-5 m: Thornton P [N] p.4034', ThorntonModel().loading(1.56e-5), 770.5, 2)
    chk('변위 구동 α 1.14e-5 m: Thornton P [N] p.4035', ThorntonModel().loading(1.14e-5), 559.6, 2)
    nmax = max(r['vz_newton_max'] for r in sweep())
    chk('뉴턴 반복 최대 (0.02-0.20 m/s) p.4038 "two"', nmax, 2, 0)
    print('selftest:', 'PASS' if ok else 'FAIL')
    return ok


# ---- 그림 판독 (원 래스터 600 dpi · pt 좌표) ----
CAL = {
    # 그림 20 (PDF 30 쪽): 틀 = 원 래스터에서 가장 긴 가로 · 세로 선 · 눈금 = 틀 안쪽 막대 위치
    '20a': dict(x0=107.65, x1=425.4, v0=0.0, v1=0.2, y0=279.9, y1=98.7, w0=0.01, w1=0.10),
    '20b': dict(x0=107.9, x1=425.9, v0=0.0, v1=120.0, y0=517.6, y1=336.3, w0=0.3, w1=0.9),
    # 그림 10 (PDF 13 쪽): 눈금 0.4e-5 = 220.2 pt · 0.8e-5 = 287.2 pt · P = 0 틀 292.9 pt
    '10': dict(x0=153.2, dx_per=33.5 / 0.2e-5, yframe=292.9),
    # 그림 16 (PDF 23 쪽): 눈금 0.4e-5 = 184.1 · 0.8e-5 = 260.5 pt · P 0 = 319.2 · 1500 N = 78.6 pt
    '16': dict(x0=107.6, dx_per=38.25 / 0.2e-5, yP0=319.2, yP1500=78.6),
    # 그림 17 (PDF 24 쪽): 0 = 268.3 · 0.5e-3 = 206.0 · 1e-3 = 143.7 · 1.5e-3 = 81.3 pt (점선 격자)
    '17': dict(y0=268.3, per=62.3 / 0.5e-3),
    # 그림 12 (PDF 15 쪽): a^p = 0 선 241.8 pt · 눈금 간격 26.82 pt · 라벨 '4×10^-4' (+4 칸) · '−2×10^-4' (−2 칸)
    #   · '2×10^-4' (+1 칸 — 다른 두 라벨과 어긋남) → 1 칸 = 1e-4 m 로 읽는다
    '12': dict(y0=241.8, per=26.82 / 1.0e-4, x0=119.2, x1=423.6),
    # 그림 11 (PDF 14 쪽 · 기울기 없음): r = 0 틀 127.78 pt · 눈금 0.2e-3 m 간격 32.72 pt (160.50 · 193.20 · 225.90 ·
    #   258.66 pt) · p = 0 틀 312.90 pt · 2e8 눈금 235.62 pt (1e8 = 38.64 pt) — 확인: Hertz 곡선의 p = 0 점이 식 (1.7)
    #   0.787 · 0.992 · 1.135e-3 m 와 ±0.002e-3 안 (아래 'Hertz check' 행)
    '11': dict(x0=127.78, per=32.72 / 0.2e-3, y0=312.90, ppy=38.64 / 1.0e8),
}
# ⚠ 스캔 기울기: PDF 11 · 13 · 15 · 23 쪽은 세로선이 기울어 있다 (틀 세로선 dx/dy ≈ −0.0085 ~ −0.0130 · 가로선은 거의
#   수평 = 가로 방향 전단) → x 를 읽을 때는 그 높이의 보정이 필요하다.  P = 0 틀 위 표지 (그림 10 · 16) 는 아래 눈금으로
#   보정했으니 그대로 · 그림 10 의 α_max 점선은 선을 맞춰 아래 틀 높이 (292.9 pt) 에서 읽는다.  14 · 24 · 30 쪽은 기울기 없음.


def digitize(pdf, out):
    import numpy as np
    import pymupdf as fitz
    from scipy import ndimage
    from scipy.signal import fftconvolve
    doc = fitz.open(pdf)

    def raster(p):
        pg = doc[p - 1]
        xref = max(pg.get_images(full=True), key=lambda im: im[2] * im[3])[0]
        pix = fitz.Pixmap(doc, xref)
        if pix.n != 1:
            pix = fitz.Pixmap(fitz.csGRAY, pix)
        a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w)
        return (a < 128).astype(np.float32), pix.w / pg.get_image_rects(xref)[0].width

    rows = []
    ink, S = raster(30)

    def px(v):
        return int(round(v * S))

    def tmpl(xc, yc, half):
        t = ink[px(yc - half):px(yc + half), px(xc - half):px(xc + half)]
        r, c = np.where(t.any(1))[0], np.where(t.any(0))[0]
        return t[r[0]:r[-1] + 1, c[0]:c[-1] + 1]

    circ, plus = tmpl(324.3, 235.5, 3.4), tmpl(324.3, 245.8, 3.2)    # 그림 20a 범례 표지

    def locate(t, xc, ylo, yhi, xw=2.5):
        th, tw = t.shape
        y0, y1, x0, x1 = px(ylo), px(yhi), px(xc - xw) - tw, px(xc + xw) + tw
        win = ink[y0:y1, x0:x1]
        corr = fftconvolve(win, (t - t.mean())[::-1, ::-1], mode='same')
        cx = win.shape[1] // 2
        band = corr[:, max(0, cx - px(xw)):cx + px(xw)]
        iy, ix = np.unravel_index(np.argmax(band), band.shape)
        return (y0 + iy) / S, (x0 + max(0, cx - px(xw)) + ix) / S

    for panel, ylo, yhi, xs in (('20a', 99.5, 279.0, [round(0.02 * k, 2) for k in range(1, 11)]),
                                ('20b', 337.0, 517.0, [12 * k for k in range(1, 11)])):
        c = CAL[panel]
        for xv in xs:
            xc = c['x0'] + (xv - c['v0']) / (c['v1'] - c['v0']) * (c['x1'] - c['x0'])
            for series, t in (('present model (o)', circ), ('Thornton 1997 (+)', plus)):
                yc, xf = locate(t, xc, ylo, yhi)
                yv = c['w0'] + (c['y0'] - yc) / (c['y0'] - c['y1']) * (c['w1'] - c['w0'])
                rows.append(dict(figure='Fig 20' + panel[-1], series=series,
                                 x_label='v_in (m/s)' if panel == '20a' else 'v_in/v_Y',
                                 x_value=xv, y_label='v_out (-m/s)' if panel == '20a' else 'e',
                                 y_value=round(yv, 4), x_pt=round(xf, 2), y_pt=round(yc, 2),
                                 method='template match (legend marker) on native 600 dpi raster; frame/tick calibration',
                                 note='printed check: 0.04 m/s -> v_out 0.0304 / 0.0214; e 0.7587 / 0.5331'))

    def on_axis(p, yframe, x0, x1, half=3.2):
        a, S2 = raster(p)
        Y0, Y1 = int((yframe - half) * S2), int((yframe + half) * S2)
        sub = a[Y0:Y1, int(x0 * S2):int(x1 * S2)] > 0
        sub[sub.mean(axis=1) > 0.6, :] = False                 # 틀 가로선 지움
        lab, n = ndimage.label(sub, structure=np.ones((3, 3)))
        out = []
        for i in range(1, n + 1):
            ys, xs = np.where(lab == i)
            if len(ys) >= 25:
                out.append((x0 + xs.mean() / S2, (Y0 + ys.min()) / S2, (Y0 + ys.max() + 1) / S2))
        return out

    c10 = CAL['10']
    for name, (xlo, xhi) in (('ABC (o)', (184, 190.5)), ('ADE (x)', (226, 233)), ('AFG (+)', (269, 275))):
        blobs = [b for b in on_axis(13, c10['yframe'], xlo, xhi) if b[2] > c10['yframe'] + 0.8]   # 틀 아래로 나온 조각만
        if blobs:
            xc = sum(b[0] for b in blobs) / len(blobs)
            rows.append(dict(figure='Fig 10', series='FEA ' + name + ' last point (P = 0)', x_label='alpha (m)',
                             x_value=round((xc - c10['x0']) / c10['dx_per'], 9), y_label='P (N)', y_value=0,
                             x_pt=round(xc, 2), y_pt=c10['yframe'],
                             method='marker piece below the P=0 frame line (frame rows removed) = marker centred on P = 0; centroid x',
                             note='residual normal displacement of the FEA unloading (not printed in the text)'))
    c16 = CAL['16']
    blobs = [b for b in on_axis(23, c16['yP0'], 241, 245.5) if b[2] > c16['yP0'] + 0.8]
    if blobs:
        xc = sum(b[0] for b in blobs) / len(blobs)
        rows.append(dict(figure='Fig 16', series='FEA (elasto-plastic) last point (P = 0)', x_label='alpha (m)',
                         x_value=round((xc - c16['x0']) / c16['dx_per'], 9), y_label='P (N)', y_value=0,
                         x_pt=round(xc, 2), y_pt=c16['yP0'], method='same as Fig 10 on-axis marker',
                         note='same FEA run as Fig 10 AFG; model curve ends here at P ~ 30-35 N'))
    # 그림 10 α_max 점선 (세로) — 띠마다 잉크 x 중심 → 직선 맞춤 → 아래 틀 (P = 0 · 292.9 pt) 높이에서 읽음
    a13, S13 = raster(13)

    def dotted_x_at(xseed, ya, yb, yat, half=2.0):
        P = []
        for y in np.arange(ya, yb, 6.0):
            Y0, Y1 = int(y * S13), int((y + 6) * S13)
            X0, X1 = int((xseed - half) * S13), int((xseed + half) * S13)
            cols = (a13[Y0:Y1, X0:X1] > 0).sum(axis=0)
            if cols.sum() >= 6:
                P.append((y + 3.0, (np.arange(X0, X1) * cols).sum() / cols.sum() / S13))
        P = np.array(P)
        m, c = np.polyfit(P[:, 0], P[:, 1], 1)
        return m * yat + c, m, len(P)

    for name, xs, ya, yb, printed in (('ABC', 267.3, 215, 290, None), ('ADE', 344.9, 140, 290, 1.14e-5),
                                      ('AFG', 415.5, 85, 290, 1.56e-5)):
        xb, m, n = dotted_x_at(xs, ya, yb, c10['yframe'])
        chk = 'printed alpha_max %.3g m (p.4034-4035) -> check' % printed if printed else 'alpha_max of ABC is not printed'
        rows.append(dict(figure='Fig 10', series='FEA ' + name + ' alpha_max (dotted vertical line)', x_label='alpha (m)',
                         x_value=round((xb - c10['x0']) / c10['dx_per'], 9), y_label='P (N)', y_value=0,
                         x_pt=round(xb, 2), y_pt=c10['yframe'],
                         method='ink x-centroid of the dotted vertical line in 6 pt bands, straight-line fit (slope %.4f), '
                                'evaluated at the P = 0 frame row (page 13 scan is sheared: frame dx/dy -0.0123)' % m,
                         note=chk + ('; with the frame shear slope forced: ~6.77e-6' if name == 'ABC' else '')))
    # 그림 11 (PDF 14 쪽) 접촉 반지름 = 마지막 p > 0 절점 ↔ 첫 p = 0 절점 (표지 중심 · 틀 줄 지움) + Hertz 확인
    a14, S14 = raster(14)
    c11 = CAL['11']

    def centroid(arr, Sx, xc, yc, half, drop_y=None):
        Y0, Y1 = int((yc - half) * Sx), int((yc + half) * Sx)
        X0, X1 = int((xc - half) * Sx), int((xc + half) * Sx)
        sub = arr[Y0:Y1, X0:X1] > 0
        if drop_y is not None:
            r0, r1 = int((drop_y - 0.45) * Sx) - Y0, int((drop_y + 0.45) * Sx) - Y0
            sub[max(0, r0):max(0, r1), :] = False
        ys, xs = np.nonzero(sub)
        return X0 / Sx + xs.mean() / Sx, Y0 / Sx + ys.mean() / Sx

    for name, P_N, last, first in (('ABC', 500, (272.64, 277.73), (278.36, 312.66)),
                                   ('ADE', 1000, (326.17, 273.44), (332.76, 313.06)),
                                   ('AFG', 1500, (364.92, 253.10), (372.65, 312.91))):
        for tag, (xc, yc), drop in (('last node with p > 0', last, None), ('first node with p = 0', first, c11['y0'])):
            cx, cy = centroid(a14, S14, xc, yc, 2.9, drop)
            rv = (cx - c11['x0']) / c11['per']
            pv = max(0.0, (c11['y0'] - cy) / c11['ppy']) if drop is None else 0.0
            rows.append(dict(figure='Fig 11', series='FEA %s (P = %d N) %s' % (name, P_N, tag), x_label='r (m)',
                             x_value=round(rv, 7), y_label='p (N/m2)', y_value=round(pv, -5),
                             x_pt=round(cx, 2), y_pt=round(cy, 2),
                             method='marker ink centroid in a 5.8 pt window (frame rows removed for p = 0 markers); '
                                    'frame/tick calibration (page 14 not sheared)',
                             note='FEA contact radius lies between the two nodes; mean pressure P/(pi a^2) from this interval'))
    for P_N, xs in ((500, 256.4), (1000, 289.9), (1500, 313.4)):
        Y = c11['y0'] - 3.6
        X0, X1 = int((xs - 1.5) * S14), int((xs + 1.5) * S14)
        cols = (a14[int(Y * S14), X0:X1] > 0)
        xh = (np.arange(X0, X1)[cols]).mean() / S14
        rows.append(dict(figure='Fig 11', series='Hertz check (solid line, P = %d N)' % P_N, x_label='r (m)',
                         x_value=round((xh - c11['x0']) / c11['per'], 7), y_label='p (N/m2)', y_value='~0',
                         x_pt=round(xh, 2), y_pt=round(Y, 2),
                         method='solid Hertz curve column 3.6 pt above the p = 0 frame',
                         note='calibration check vs eq (1.7): %.4e m' % a_e(P_N)))
    # 그림 12 FEA 제하 점 (∘) — 제하 중 a^p 가 고정인지 (식 2.5 · 3.20) 보는 판독
    a15, S15 = raster(15)
    c12 = CAL['12']
    for tag, (xc, yc), half in (('unloading (o) + loading (+) cluster at P ~ 1460-1500 N', (421.5, 156.0), 3.6),
                                ('unloading (o) peak', (251.88, 125.16), 2.9), ('unloading (o) peak', (271.55, 125.37), 2.9),
                                ('unloading (o) last point', (122.43, 184.97), 2.9)):
        cx, cy = centroid(a15, S15, xc, yc, half)
        Pv = (cx - c12['x0']) / (c12['x1'] - c12['x0']) * 1500
        rows.append(dict(figure='Fig 12', series='FEA ' + tag, x_label='P (N)', x_value=round(Pv, 0),
                         y_label='a^p (m)', y_value=round((c12['y0'] - cy) / c12['per'], 7), x_pt=round(cx, 2), y_pt=round(cy, 2),
                         method='marker ink centroid (window %.1f pt); 1 tick = 1e-4 m (two of three labels); '
                                'page 15 sheared (vertical frame dx/dy -0.012, horizontal lines level) -> P +-5 N' % (2 * half),
                         note='eq (2.5)/(3.20) holds a^p fixed at C_a(P_max - P_Y) = 3.41e-4 m during unloading'))
    # 그림 17 일점쇄선 (제하 중 고정된 a^p) · 그림 12 직선 (모델 적재 a^p) · 점선 (모델 제하 a^p)
    a17, S17 = raster(24)
    band = a17[int(200 * S17):int(260 * S17), int(200 * S17):int(390 * S17)]
    yy = 200 + np.argmax(band.mean(axis=1) * (band.mean(axis=1) < 0.3)) / S17
    rows.append(dict(figure='Fig 17', series='a^p during unloading (dash-dot)', x_label='P (N)', x_value='0-1500',
                     y_label='a^p (m)', y_value=round((CAL['17']['y0'] - yy) / CAL['17']['per'], 7), x_pt='', y_pt=round(yy, 2),
                     method='row of max partial ink coverage (dash-dot line) between 200-260 pt; grid-line calibration',
                     note='eq (2.5) with printed C_a: 2.33e-7 x (1500 - 36.45) = 3.41e-4 m'))
    a12, S12 = raster(15)
    c12 = CAL['12']
    for series, ypt in (('model unloading a^p (dashed)', 142.5),):
        rows.append(dict(figure='Fig 12', series=series, x_label='P (N)', x_value='0-1500', y_label='a^p (m)',
                         y_value=round((c12['y0'] - ypt) / c12['per'], 7), x_pt='', y_pt=ypt,
                         method='dashed-line row (31 % ink coverage) at 142.5 pt; 1 tick = 1e-4 m (two of three labels)',
                         note='~8 % above eq (2.5) with printed C_a (3.41e-4) -- Fig 12 tick labels are inconsistent'))
    for xpt, ypt in ((200, 218.0), (300, 185.1), (350, 168.6), (380, 158.8), (400, 152.3)):
        Pv = (xpt - c12['x0']) / (c12['x1'] - c12['x0']) * 1500
        rows.append(dict(figure='Fig 12', series='model loading a^p (solid line)', x_label='P (N)', x_value=round(Pv, 1),
                         y_label='a^p (m)', y_value=round((c12['y0'] - ypt) / c12['per'], 7), x_pt=xpt, y_pt=ypt,
                         method='solid line row in a single raster column (1 tick = 1e-4 m)',
                         note='slope of these points ~2.5e-7 m/N vs printed C_a 2.33e-7'))
    with open(out, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['figure', 'series', 'x_label', 'x_value', 'y_label', 'y_value',
                                          'x_pt', 'y_pt', 'method', 'note'])
        w.writeheader()
        w.writerows(rows)
    print(f'{len(rows)} rows -> {out}')


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--sweep', action='store_true')
    ap.add_argument('--digitize', metavar='PDF')
    ap.add_argument('--out', default='digitized.csv')
    a = ap.parse_args()
    if a.selftest:
        sys.exit(0 if selftest() else 1)
    if a.sweep:
        for r in sweep():
            print({k: (round(v, 6) if isinstance(v, float) else v) for k, v in r.items()})
        for P in (500, 1000, 1500):
            print(P, {k: round(v, 9) for k, v in quasi_static(P).items()})
    if a.digitize:
        digitize(a.digitize, a.out)
    if not (a.selftest or a.sweep or a.digitize):
        ap.print_help()


if __name__ == '__main__':
    main()
