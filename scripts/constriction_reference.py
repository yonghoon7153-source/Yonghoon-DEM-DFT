#!/usr/bin/env python3
"""AREA-09 STEP 4 — 협착저항의 **독립 기준해**.  ψ 를 어디에 두는가를 수치로 판정한다.

정본 계약 = `docs/area_contract_20260913.md` · 판정문 =
`docs/reviews/codex_verdict_area_contract_20260913.md` (AREA-09) · 원장 = `L2-01`.

★ 왜 (판정문 §3): *"독립 두 입자/neck 기준해·유효 영역·극한 검증: **없음**.
  16/49 비교는 수송 기준해가 아니다."*  그래서 세 공식 중 어느 것이 맞는지를
  **문헌 인용이 아니라 계산**으로 가른다.

경쟁하는 셋 (같은 기하, 같은 a/b):
    R_Holm   = 1 / (2 σ a)                반무한 반공간, flux tube 없음
    R_lit    = ψ(a/b) / (2 σ a)           ψ 를 **곱한다**
    R_code   = 1 / (2 σ a ψ(a/b))         우리 코드 (`network_conductivity.py:399`)
    ψ(s)     = (1 − s)^1.5,  s = a/b

⚠ **우리 파일 안에서 주석과 코드가 서로 다르다** — `network_conductivity.py:380` 의
   주석은 `R_constriction = (1 - a/r_min)^1.5 / (2a)` (= ψ 를 **곱함**) 인데
   `:399` 의 코드는 `1.0 / (... * 2 * a_eff * psi)` (= ψ 로 **나눔**) 이다.
   이 파일은 그 둘 중 어느 쪽이 맞는지를 가린다.

기준해: **축대칭 유한차분**으로 하나의 flux tube 를 푼다 —
반지름 b, 길이 2L 의 원기둥을 반지름 a 의 원판 구멍이 뚫린 절연 격막이 가운데서 막고,
양 끝면이 등전위, 옆면은 절연.  `∇·(σ∇φ) = 0` 을 (r, z) 격자에서 푼 뒤

    R_total = ΔV / I,   R_constriction = R_total − R_bulk

⇒ **협착 몫만** 남긴다.  이것이 세 공식이 예측하는 바로 그 양이다.
(직렬 분해 `R_total = 2L/(σπb²) + R_c` 는 flux-tube 유도 자신의 규약이다.)

⚠ 이 기준해가 **답하는 것**: 같은 flux-tube 기하에서 ψ 를 곱해야 하는가 나눠야 하는가,
   그리고 그 근사가 어느 s 까지 유효한가.
⚠ 이 기준해가 **답하지 않는 것**: 우리 침대의 A 가 그 원판이 맞는가 (그건 `AREA-03` ·
   `AREA-09` STEP 2 의 면적 계약 문제다).  여기서는 **A 가 주어졌다고 놓고** 저항식만 본다.
⚠ 구가 아니라 **원기둥**이다 — flux tube 가 문헌 유도의 기하이기 때문이다.  유한한 두 구의
   해가 필요하면 그것은 별도 (STEP 2 의 '접촉 연산자와 영역' 결정에 따라 달라진다).

★ 선형해는 **희소 직접 분해**다 (`scipy.sparse` + SuperLU) — 반복 허용오차가 값에 안
   들어간다.  초판은 Jacobi-CG 였고, **두 솔버가 6자리 이상 일치**한다 (예: nr=300 s=0.05
   에서 `R_c = 10.032023` 동일, nr=240 s=0.05 에서 `10.232813` 동일).  ⇒ 선형대수 쪽
   실수는 배제된다.  덤으로 74 s → 3.3 s.

★★ v1 의 결함 (기록으로 남긴다 — 규율 ②): conductance 세 개에서 축대칭 면적의 **2π 를
   통째로 빠뜨렸다**.  모든 저항이 일률적으로 2π 배 부풀어 검사 ③ 이 1.02 대신 **6.4295**
   를 냈고, 나는 그것을 "유한 tube 라서 Holm 에 안 붙는 것" 이라는 **물리 서술로 착각**할
   뻔했다.  일률 배수라 단조·수렴·극한 검사(① ② ④)는 **전부 초록이었다** = 규율 ⑤ 의
   false-green.  ⇒ 검사 ⓪ **정규화**(측정 R_bulk ↔ 해석 2L/(σπb²)) 를 상주시킨다.
   배수 검사만이 이것을 잡는다.

사용:
  python3 scripts/constriction_reference.py                  # 기본 스윕
  python3 scripts/constriction_reference.py --nr 400 --nz 800
  python3 scripts/constriction_reference.py --selftest
"""
from __future__ import annotations
import argparse
import math
import os
import sys

import numpy as np
from scipy import sparse as _sparse
from scipy.sparse.linalg import spsolve as _spsolve

PSI_EXP = 1.5
LIT_VALID_MAX = 0.3          # (1−s)^1.5 근사의 통상 인용 상한 (0 < a/b ≤ 0.3)
BAND_EPS = 1e-9              # ⚠ P2-R2-03: a_eff = k·dr 가 0.30000000000000004 로 나와 s=0.3 이
                             #   '범위 밖' 으로 분류됐다.  구간 경계는 이 허용오차로 비교한다.
TWO_PI = 2.0 * math.pi


def psi(s: float) -> float:
    """flux-tube 보정 ψ(s) = (1 − s)^1.5,  s = a/b."""
    return max(1.0 - s, 0.0) ** PSI_EXP


def coef_ratio_min_over_series(sigma1, sigma2, a=None, b1=None, b2=None):
    """`AREA-11` 계수비 = (min(σ) 식) / (직렬 후보).

    **공통 b · 공통 ψ** 에서만 ψ 와 a 가 약분돼

        ratio = 2σ₁σ₂ / (σ_min·(σ₁+σ₂))  ∈ **[1, 2)**

    가 된다 (σ₁=σ₂ 면 정확히 1, σ₂/σ₁→∞ 에서 2 에 접근하되 **닿지 않는다**).
    `b₁≠b₂` 면 ψ₁≠ψ₂ 라 약분이 일어나지 않고 **구간이 깨진다** (검사 ⑩b 의 반례 0.855 < 1).

    `a`·`b1`·`b2` 를 주면 각자 ψ 를 써서 **약분 없이** 계산한다 (공유 b 는 `b_min`).
    ⛔ 이 함수를 σ 나 ψ 가 0 일 때 부르지 않는다 — 0/0 비는 보고하지 않는다 (`R3-05`).
    """
    if not (sigma1 > 0 and sigma2 > 0):
        raise ValueError('σ 는 양수여야 한다 — 0/0 비를 보고하지 않는다 (R3-05)')
    if a is None:                                  # 공통 b · 공통 ψ: 약분된 닫힌 꼴
        return 2.0 * sigma1 * sigma2 / (min(sigma1, sigma2) * (sigma1 + sigma2))
    if not (b1 and b2 and a > 0):
        raise ValueError('a·b1·b2 는 양수여야 한다')
    psi1, psi2 = psi(a / b1), psi(a / b2)
    psi_shared = psi(a / min(b1, b2))
    if psi1 <= 0 or psi2 <= 0 or psi_shared <= 0:
        raise ValueError('ψ = 0 에서는 비를 보고하지 않는다 (R3-05)')
    r_min = psi_shared / (2.0 * min(sigma1, sigma2) * a)
    r_ser = (psi1 / sigma1 + psi2 / sigma2) / (4.0 * a)
    return r_min / r_ser


def _assemble(kz, nr, nz, dr, dz, rp, rm, sig_z):
    """축대칭 유한체적 conductance 를 조립한다 → (diag, Gr, Gz, Gb0, Gb1).

      z 면 면적 = π(rp²−rm²) = 2π·Az     r 면 면적 = 2π·rp·dz
    ⚠ **2π 를 빼먹으면 모든 저항이 일률적으로 2π 배 된다** (v1 결함).  검사 ⓪ 이 잡는다.
    `sig_z` = z 기둥별 σ (길이 nz).  z 면은 반 셀씩의 **직렬**(조화)로 잇는다 — 그래야
    **양쪽이 다른 재료**여도 맞는다 (검사 ⑧).
    """
    Az = (rp ** 2 - rm ** 2) / 2.0            # z 면 면적 / (2π)
    sig_z = np.asarray(sig_z, dtype=float)
    inv = 1.0 / sig_z
    Gr = TWO_PI * (rp[:-1, None] * dz / dr) * sig_z[None, :]        # (nr-1, nz)
    Gz = TWO_PI * Az[:, None] * kz / ((dz / 2.0) * (inv[:-1] + inv[1:]))[None, :]
    Gb0 = TWO_PI * Az * sig_z[0] / (dz / 2.0)
    Gb1 = TWO_PI * Az * sig_z[-1] / (dz / 2.0)

    diag = np.zeros((nr, nz))
    diag[:-1, :] += Gr; diag[1:, :] += Gr
    diag[:, :-1] += Gz; diag[:, 1:] += Gz
    diag[:, 0] += Gb0;  diag[:, -1] += Gb1
    return diag, Gr, Gz, Gb0, Gb1


def _solve(kz, nr, nz, dr, dz, rp, rm, sig_z):
    """SPD 라플라시안을 **희소 직접 분해**로 푼다 → (φ, I, rel_resid).

    φ 경계 = z 양끝 ∓0.5 (ΔV = 1).
    ★ 직접해다 — 반복 허용오차가 결과에 안 들어간다 (CG 판에서는 조임 정도가 값을
      흔들 수 있었다).  희소 행렬은 `scipy.sparse` 로 조립한다 (생산 솔버와 같은 의존).
    """
    diag, Gr, Gz, Gb0, Gb1 = _assemble(kz, nr, nz, dr, dz, rp, rm, sig_z)
    n = nr * nz
    idx = np.arange(n).reshape(nr, nz)

    rows = [idx.ravel()]
    cols = [idx.ravel()]
    vals = [diag.ravel()]
    # r 방향 (i ↔ i+1)
    a_, b_ = idx[:-1, :].ravel(), idx[1:, :].ravel()
    g = (-Gr).ravel()
    rows += [a_, b_]; cols += [b_, a_]; vals += [g, g]
    # z 방향 (j ↔ j+1)
    a_, b_ = idx[:, :-1].ravel(), idx[:, 1:].ravel()
    g = (-Gz).ravel()
    rows += [a_, b_]; cols += [b_, a_]; vals += [g, g]

    A = _sparse.coo_matrix((np.concatenate(vals),
                            (np.concatenate(rows), np.concatenate(cols))),
                           shape=(n, n)).tocsc()
    rhs = np.zeros((nr, nz))
    rhs[:, 0] = Gb0 * (-0.5)
    rhs[:, -1] = Gb1 * (+0.5)
    rhs = rhs.ravel()

    x = _spsolve(A, rhs)
    rel = float(np.linalg.norm(A @ x - rhs) / max(np.linalg.norm(rhs), 1e-300))
    X = x.reshape(nr, nz)
    I = float(np.sum(Gb0 * (X[:, 0] - (-0.5))))   # z=−L 경계로 들어오는 전류
    return X, I, rel


def solve_flux_tube(s: float, nr: int = 300, nz: int = 600,
                    aspect: float = 4.0, sigma: float = 1.0,
                    sigma2: float | None = None):
    """축대칭 FD flux tube → dict(R_total, R_bulk, R_c, a_eff, s_eff, R_bulk_exact, ...).

    기하 (b = 1): 0 ≤ r ≤ 1, −L ≤ z ≤ +L.  z=±L 등전위(∓0.5), r=1 절연.
    z=0 평면에 **절연 격막**, r ≤ a 만 열림 (= 접촉 원판).

    ★ 구멍은 **격자 면에 스냅**한다 (`a_eff = k·dr`) — 그러지 않으면 a 의 이산화 오차가
      비 R_c/R_Holm(a) 에 1차로 그대로 들어온다.  보고·정규화는 전부 `a_eff` 기준.
    ★ `R_bulk` 는 **유도하지 않고 같은 솔버로 측정**한다 (격막 없는 런).  그래야 **bulk
      성분의** 이산화 오차가 상쇄되고 `R_c` 만 남는다.  ⚠ 구멍 가장자리의 이산화 오차는
      **상쇄되지 않는다** (P2-R2-04: s=.05 · nr120 에서 nz 240→480→960 에 R_c 10.312 → 9.912 →
      9.774 로 계속 움직인다).  정량 인용에는 a_eff 고정 r/z 독립 세분화 증거가 따로 필요하다.
      해석값과의 대조는 검사 ⓪ 이 따로 한다.
    """
    if not (0.0 < s < 1.0):
        raise ValueError(f's = a/b 는 (0,1) 이어야 한다: {s}')
    if nz % 2:
        #  ⚠ 홀수 nz 면 격막(jmid = nz//2 − 1)이 정확한 중간이 아니라 두 재료의 길이가 달라진다 —
        #    Codex 재현: nz=81, σ 1:8 에서 측정 R_bulk 가 R_bulk_exact 와 −0.9602194787 % 어긋남.
        raise ValueError(f'nz 는 짝수여야 한다 (격막이 정확한 중간에 오도록): {nz}')
    L = float(aspect)
    dr = 1.0 / nr
    dz = 2.0 * L / nz
    rp = (np.arange(nr) + 1.0) * dr
    rm = np.arange(nr) * dr

    k = int(round(s / dr))
    if k < 1:
        raise ValueError(f'구멍이 한 셀보다 작다 (s={s}, dr={dr:g}) — nr 을 올려라')
    if k >= nr:
        raise ValueError(f'구멍이 tube 전체다 (s={s}) — s < 1 − dr 이어야 한다')
    a_eff = k * dr

    kz_open = np.ones((nr, nz - 1))
    kz = kz_open.copy()
    jmid = nz // 2 - 1
    kz[k:, jmid] = 0.0

    s2 = float(sigma if sigma2 is None else sigma2)
    sig_z = np.where(np.arange(nz) <= jmid, float(sigma), s2)

    _, I, rel = _solve(kz, nr, nz, dr, dz, rp, rm, sig_z)
    _, I0, rel0 = _solve(kz_open, nr, nz, dr, dz, rp, rm, sig_z)
    R_tot = 1.0 / I
    R_bulk = 1.0 / I0
    return {
        'R_total': R_tot, 'R_bulk': R_bulk, 'R_c': R_tot - R_bulk,
        'a_eff': a_eff, 's_eff': a_eff,          # b = 1 이므로 s_eff = a_eff
        'R_bulk_exact': L / (math.pi * 1.0 ** 2) * (1.0 / sigma + 1.0 / s2),
        # 이종쌍 Holm = 두 반공간의 **직렬**:  (1/4a)(1/σ1 + 1/σ2)
        'R_Holm': (1.0 / (4.0 * a_eff)) * (1.0 / sigma + 1.0 / s2),
        'R_Holm_min': 1.0 / (2.0 * min(sigma, s2) * a_eff),   # 코드의 min(σ) 규약
        'sigma1': float(sigma), 'sigma2': s2,
        'rel_resid': max(rel, rel0), 'n_cells_across': k,
    }


def sweep(ss, nr, nz, aspect, sigma=1.0):
    print(f'축대칭 FD flux tube — nr={nr} nz={nz} aspect(L/b)={aspect} σ={sigma}')
    print('  (a 는 격자 면에 스냅된 a_eff 로 보고·정규화한다)')
    print()
    print(f'{"a/b(요청)":>10} {"a_eff":>8} {"셀":>4} {"R_c(수치)":>12} {"R_Holm":>10} '
          f'{"ψ·R_H":>10} {"R_H/ψ":>11} | {"c/Holm":>8} {"c/(ψ·R_H)":>10} {"c/(R_H/ψ)":>10}')
    rows = []
    for s in ss:
        d = solve_flux_tube(s, nr=nr, nz=nz, aspect=aspect, sigma=sigma)
        se, R_c, R_H = d['s_eff'], d['R_c'], d['R_Holm']
        ps = psi(se)
        R_lit = ps * R_H
        R_code = R_H / ps if ps > 0 else float('inf')
        rows.append(dict(d, psi=ps, R_lit=R_lit, R_code=R_code,
                         ratio_holm=R_c / R_H, ratio_lit=R_c / R_lit,
                         ratio_code=R_c / R_code if math.isfinite(R_code) else 0.0))
        mark = '' if se <= LIT_VALID_MAX + BAND_EPS else '  ⚠(1−s)^1.5 통상 인용범위 밖'
        print(f'{s:10.3f} {se:8.4f} {d["n_cells_across"]:4d} {R_c:12.6f} {R_H:10.6f} '
              f'{R_lit:10.6f} {R_code:11.6f} | {R_c/R_H:8.4f} {R_c/R_lit:10.4f} '
              f'{(R_c/R_code if math.isfinite(R_code) else 0.0):10.4f}{mark}')
    return rows


def _verdict(rows):
    """어느 배치가 수치해에 더 가까운가 — **구간을 나눠** 말한다 (평균 하나로 뭉개지 않는다)."""
    print()
    print('판정 (|ln 비| 가 작을수록 가깝다 — 1.0 이 완전 일치):')
    print(f'{"구간":>22} {"n":>3} {"ψ 를 곱함":>12} {"ψ 로 나눔":>12} {"보정 없음":>12}')
    bands = [('s ≤ 0.3 (통상 인용범위)', lambda r: r['s_eff'] <= LIT_VALID_MAX + BAND_EPS),
             ('s > 0.3 (범위 밖)',       lambda r: r['s_eff'] > LIT_VALID_MAX + BAND_EPS)]
    for name, sel in bands:
        sub = [r for r in rows if sel(r)]
        if not sub:
            continue
        def gm(key):
            v = [abs(math.log(r[key])) for r in sub if r[key] > 0]
            return math.exp(sum(v) / len(v)) if v else float('nan')
        print(f'{name:>22} {len(sub):3d} {gm("ratio_lit"):12.4f} '
              f'{gm("ratio_code"):12.4f} {gm("ratio_holm"):12.4f}')


def main() -> int:
    ap = argparse.ArgumentParser(description='협착저항 독립 기준해 (AREA-09 STEP 4)')
    ap.add_argument('--nr', type=int, default=300)
    ap.add_argument('--nz', type=int, default=600)
    ap.add_argument('--aspect', type=float, default=4.0)
    ap.add_argument('--sigma', type=float, default=1.0)
    ap.add_argument('--s', default='0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    ss = [float(x) for x in a.s.split(',')]
    rows = sweep(ss, a.nr, a.nz, a.aspect, a.sigma)
    _verdict(rows)
    print()
    print('⚠ 이 표가 답하는 것 — 같은 flux-tube 기하에서 **ψ 를 곱하는가 나누는가**.')
    print('⚠ 답하지 않는 것 — 우리 침대의 A 가 그 원판이 맞는가 (AREA-03 · STEP 2 소관).')
    print('⚠ 원기둥 flux tube 다.  유한한 두 구의 해가 필요하면 별도다.')
    print('⚠ 격자 하나의 표다.  인용 전에 --nr 을 올려 수렴을 확인할 것 (검사 ④).')
    return 0


def _selftest() -> int:
    """기준해가 **알려진 극한**을 재현하는가.  대조 없이 표만 내지 않는다."""
    ok = True

    def chk(name, cond, extra=''):
        nonlocal ok
        print(('  ✓ ' if cond else '  ✗ ') + name + (f'   {extra}' if extra else ''))
        ok = ok and bool(cond)

    print('협착 기준해 (AREA-09 STEP 4)')

    # ⓪ 정규화 — 측정 R_bulk 가 해석 2L/(σπb²) 와 같은가.
    #    ★ v1 은 conductance 의 2π 를 빼먹어 모든 저항이 2π 배였는데 ① ② ④ 는 전부
    #      초록이었다 (일률 배수라 극한·단조·수렴이 안 깨진다).  **이 검사만이 잡는다.**
    d = solve_flux_tube(0.3, nr=80, nz=160, aspect=2.0)
    e = abs(d['R_bulk'] - d['R_bulk_exact']) / d['R_bulk_exact']
    chk('⓪ 정규화: 측정 R_bulk = 해석 2L/(σπb²) (오차 < 1e-6)', e < 1e-6,
        f'{d["R_bulk"]:.9f} vs {d["R_bulk_exact"]:.9f} (rel {e:.2e})')

    # ⓪b σ 스케일링 — R ∝ 1/σ
    d2 = solve_flux_tube(0.3, nr=80, nz=160, aspect=2.0, sigma=4.0)
    chk('⓪b σ 스케일: σ ×4 → R_c ÷4', abs(d2['R_c'] * 4.0 / d['R_c'] - 1.0) < 1e-8,
        f'{d["R_c"]:.8f} → {d2["R_c"]:.8f}')

    # ① s → 1 (격막이 사라짐) 이면 협착 몫 → 0
    d = solve_flux_tube(0.99, nr=200, nz=200, aspect=2.0)
    chk('① s→1 (막힘 없음) 이면 협착 몫 ≈ 0', abs(d['R_c']) < 0.02 * d['R_bulk'],
        f'R_c={d["R_c"]:.6g} · R_bulk={d["R_bulk"]:.6g}')

    # ② 단조: 구멍이 작아지면 협착 저항이 커진다
    vals = [solve_flux_tube(s, nr=80, nz=160, aspect=2.0)['R_c'] for s in (0.2, 0.4, 0.6)]
    chk('② 단조: a 가 커지면 협착 저항이 **작아진다**',
        vals[0] > vals[1] > vals[2], f'{[round(v, 4) for v in vals]}')

    # ③ 작은 s 에서 Holm 스케일 1/(2σa) 에 접근 — **규모·정규화 smoke** 다.
    #    ⚠ 이 검사는 **어느 ψ 배치도 전제하지 않는다** — s→0 에서 ψ→1 이라 세 공식이
    #      전부 Holm 으로 모인다.  판정은 sweep 이 하고 여기는 솔버만 본다.
    #    ⚠⚠ P2-R2-04: 밴드 0.7~1.3 은 **20 % 국소 오류를 통과시킨다** (Codex 변이: s=.05 의
    #      R_c ×1.20 → 비 1.2279, 여전히 PASS; ×1.30 → 1.3303 은 FAIL).  2π 배수는 잡지만
    #      수 % 정확도는 **보증하지 않는다** — 그 보증은 별도 세분화 증거의 몫이다.
    d = solve_flux_tube(0.05, nr=240, nz=480, aspect=4.0)
    ratio = d['R_c'] / d['R_Holm']
    chk('③ [smoke] 작은 s 에서 R_c/R_Holm 이 1 근처 (0.7~1.3; ×1.2 오류는 못 잡는다)',
        0.7 < ratio < 1.3, f'{ratio:.4f}')

    # ④ 격자 수렴 — 해상도를 올려도 값이 크게 안 움직인다
    a1 = solve_flux_tube(0.3, nr=120, nz=240, aspect=3.0)['R_c']
    a2 = solve_flux_tube(0.3, nr=240, nz=480, aspect=3.0)['R_c']
    chk('④ 격자 수렴: nr 120 → 240 에서 협착 몫 변화 < 5 %',
        abs(a2 - a1) / max(abs(a1), 1e-30) < 0.05, f'{a1:.5f} → {a2:.5f}')

    # ⑤ 종횡비 무관 — 협착 몫은 tube 길이에 안 걸려야 한다 (bulk 만 걸린다)
    b1 = solve_flux_tube(0.3, nr=120, nz=240, aspect=2.0)['R_c']
    b2 = solve_flux_tube(0.3, nr=120, nz=480, aspect=4.0)['R_c']
    chk('⑤ 종횡비 무관: L/b 2 → 4 에서 협착 몫 변화 < 3 %',
        abs(b2 - b1) / max(abs(b1), 1e-30) < 0.03, f'{b1:.5f} → {b2:.5f}')

    # ⑥ 대조: ψ 를 곱한 것과 나눈 것이 **실제로 다르다** (검사가 무의미하지 않다)
    s = 0.3
    R_H = 1.0 / (2 * s)
    chk('⑥ 대조: ψ·R_H 와 R_H/ψ 가 s=0.3 에서 2배 이상 다르다',
        (R_H / psi(s)) / (psi(s) * R_H) > 2.0,
        f'비 = {(R_H / psi(s)) / (psi(s) * R_H):.4f}')

    # ⑧ **이종 재료쌍** — 두 반공간의 직렬인가, `min(σ)` 인가 (`AREA-11`)
    #    코드는 `min(σ1,σ2)` 를 쓴다 (`network_conductivity.py:390`).  참값이 직렬
    #    `(1/4a)(1/σ1+1/σ2)` 이면 코드는 최대 **2배** 과대평가다.
    d = solve_flux_tube(0.1, nr=200, nz=400, aspect=3.0, sigma=1.0, sigma2=8.0)
    r_ser = d['R_c'] / (psi(d['s_eff']) * d['R_Holm'])
    r_min = d['R_c'] / (psi(d['s_eff']) * d['R_Holm_min'])
    chk('⑧ 이종쌍(σ 1:8): 수치해가 **직렬** ψ(1/4a)(1/σ1+1/σ2) 에 붙는다',
        abs(r_ser - 1.0) < 0.10 and abs(r_min - 1.0) > 0.25,
        f'직렬비 {r_ser:.4f} · min(σ)비 {r_min:.4f} · **min식/수치해 {1/r_min:.4f}배** '
        f'(⚠ 직렬비/min비 = 16/9 는 수치해가 소거되는 계수비라 독립 증거가 아니다 — P2-R2-07)')
    # ⑧b 짝수 nz 요구 — 홀수면 거부한다 (부록 P2-R2-04)
    try:
        solve_flux_tube(0.3, nr=40, nz=81, aspect=2.0); odd_ok = False
    except ValueError:
        odd_ok = True
    chk('⑧b 홀수 nz 는 거부 (격막이 중간에 안 온다 — Codex: −0.96 % R_bulk 어긋남)', odd_ok)
    # ⑧c s=0.3 이 인용 구간 **안**에 분류된다 (P2-R2-03: 0.30000000000000004 가 밖으로 갔었다)
    d3 = solve_flux_tube(0.3, nr=300, nz=600, aspect=2.0)
    chk('⑧c s=0.3 요청이 s≤0.3 구간에 들어간다 (a_eff 부동소수 반올림 허용)',
        d3['s_eff'] <= LIT_VALID_MAX + BAND_EPS, f"s_eff={d3['s_eff']!r}")

    # ⑨ 동종쌍에서는 두 규약이 **같다** (⑧ 이 σ 비대칭만 잡는지 확인)
    d = solve_flux_tube(0.1, nr=200, nz=400, aspect=3.0, sigma=1.0, sigma2=1.0)
    chk('⑨ 동종쌍(σ 1:1): 직렬식과 min(σ)식이 동일',
        abs(d['R_Holm'] - d['R_Holm_min']) < 1e-12,
        f'{d["R_Holm"]:.10f} vs {d["R_Holm_min"]:.10f}')

    # ⑩ **`AREA-11` 계수비의 정의역** (`R3-05`) — `[1, 2)` 는 **공통 b · 공통 ψ** 에서만이다.
    #    3라운드가 잡은 것: 계약 v3 는 `b₁≠b₂` 까지 바꾸는 처방에 그 구간을 그대로 적었는데,
    #    ψ 가 약분되지 않으면 비가 **1 밑으로도 간다**.  문구에서만 한정하면 또 새어나가므로
    #    (규율 ④) 반례를 여기서 못박는다.
    import random as _rnd
    _rnd.seed(20260914)
    _in_band = []
    for _ in range(200):
        s1 = 10.0 ** _rnd.uniform(-3, 3)
        s2 = 10.0 ** _rnd.uniform(-3, 3)
        _in_band.append(1.0 - 1e-12 <= coef_ratio_min_over_series(s1, s2) < 2.0)
    _eq = coef_ratio_min_over_series(7.0, 7.0)
    _extreme = coef_ratio_min_over_series(1.0, 1e12)
    chk('⑩ 공통 b·공통 ψ 면 계수비 ∈ [1,2) — 동종 = 정확히 1 · 극단쌍도 2 를 안 넘는다',
        all(_in_band) and abs(_eq - 1.0) < 1e-12 and 1.99 < _extreme < 2.0,
        f'무작위 200쌍 전부 구간 안 · 동종 {_eq!r} · 1:1e12 {_extreme:.12f}')
    # ⑩b **반례** — b₁≠b₂ 면 ψ 가 약분되지 않아 비가 1 **밑**으로 간다 (판정문 §5.2)
    _cx = coef_ratio_min_over_series(1.0, 1.0, a=0.3, b1=1.0, b2=2.0)
    chk('⑩b 반례: a=.3 · b 1:2 · σ 1:1 → 비 0.8554… < 1 (구간이 깨진다)',
        abs(_cx - 0.8554035700220194) < 1e-12 and _cx < 1.0, f'{_cx!r}')
    # ⑩c ψ=0 · σ=0 에서는 비를 **보고하지 않는다** (0/0 을 숫자로 만들지 않는다)
    _refused = 0
    for _kw in ({'sigma1': 0.0, 'sigma2': 1.0},
                {'sigma1': 1.0, 'sigma2': 1.0, 'a': 1.0, 'b1': 1.0, 'b2': 2.0}):
        try:
            coef_ratio_min_over_series(**_kw)
        except ValueError:
            _refused += 1
    chk('⑩c σ=0 · ψ=0 (a=b) 은 거부한다 — 0/0 비를 보고하지 않는다', _refused == 2,
        f'거부 {_refused}/2')
    # ⑩d **계약이 그 한정을 실제로 담고 있다** — 문구만 문서에 두면 낡는다 (규율 ④).
    _ct = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       'docs', 'area_contract_20260913.md')
    _txt = open(_ct, encoding='utf-8').read() if os.path.exists(_ct) else ''
    _need = ['공통 b · 공통 ψ', '[1, 2)', '별도 기하 시험', '0.855']
    _miss = [t for t in _need if t not in _txt]
    chk('⑩d 계약 §5-v4 E 가 한정(공통 b·공통 ψ · 별도 기하 시험 · 반례 0.855)을 담는다',
        not _miss, f'빠진 문구: {_miss}')

    # ⑦ 대조: 2π 를 일부러 빼면 ⓪ 이 **반드시** 빨간불이 된다 (판별력 증명)
    import types
    src = open(__file__, encoding='utf-8').read().replace(
        'TWO_PI = 2.0 * math.pi', 'TWO_PI = 1.0', 1)
    mod = types.ModuleType('_cr_mutant')
    mod.__file__ = __file__
    exec(compile(src, __file__, 'exec'), mod.__dict__)
    dm = mod.solve_flux_tube(0.3, nr=60, nz=120, aspect=2.0)
    em = abs(dm['R_bulk'] - dm['R_bulk_exact']) / dm['R_bulk_exact']
    chk('⑦ 판별력: 2π 를 빼면 ⓪ 이 빨간불 (v1 결함 재현)', em > 1e-6,
        f'변이 rel = {em:.4f} (≈ 2π−1 = {TWO_PI - 1:.4f})')

    print('협착 기준해 SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
