#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""#29 v2 — Joule 발열 hot-spot → 열화 공간 재분배기 (Eₐ-free, 끝점 보존).

문헌조사(2026-07-23): LPSCl 분해-율 Arrhenius Eₐ는 **문헌에 없음**(전도/계면 Eₐ는 틀린 양) →
절대 Arrhenius 곱은 날조 불가.  자기발열은 물리적 유의(~5-30K, Ayyaswamy AEM2026).
→ 정직한 v2 = **끝점-보존 공간 재분배기**: STEP5 스칼라 총 열화 증분 ΔR_total(이미 실측 끝점에
앵커, 자기발열 포함)을 Joule 발열밀도 q 로 **가중 분배** → 어디서 R_int이 빨리 자라나(공간).

    ΔR_local = ΔR_total · q^p / Σ(q^p)          (Σ ΔR_local = ΔR_total = 끝점 보존)

★Arrhenius 곱 아님(끝점 위에 얹으면 실셀 자기발열 이중계산) — **분배**만.  p = 집중 지수
(p=1 자연=열화∝국소발열 / p>1 = ASSUMED 스윕, 문헌 앵커 아님).  q 는 #29 v1 joule_hotspot 출력.
"""
from __future__ import annotations

import numpy as np


def redistribute(q, dR_total: float, focus_p: float = 1.0):
    """Joule 발열밀도 q(per-voxel/region 배열) 로 스칼라 ΔR_total 을 끝점-보존 분배.
    반환: ΔR_local 배열, **항상 Σ = ΔR_total** (끝점 보존).  q≡0(비퍼콜=발열없음)/수치붕괴 →
    균일 분배(ΔR_total/n)로 보존 유지(비퍼콜 셀도 화학열화는 균일; zeros 반환=보존위반 금지).
    ★q^p 가중 — p=1 권장(열화∝발열), p>1 = 집중 ASSUMED 스윕(Eₐ 아님)."""
    q = np.asarray(q, dtype=np.float64)
    valid = np.isfinite(q) & (q > 0.0)
    q = np.where(valid, q, 0.0)
    p = max(0.0, float(focus_p))
    w = np.where(valid, q ** p, 0.0)          # ★리뷰#5: invalid(q≤0/비유한)는 ALL p에서 0 (p=0의 0**0=1 재진입 방지)
    s = float(w.sum())
    n = q.size
    # ★리뷰#3/#7: q≡0(비퍼콜=발열없음, 화학열화는 여전) 또는 수치붕괴(s=inf/NaN, 극단 p) → 균일 분배로
    #   끝점 보존(Σ=dR_total).  zeros 반환은 Σ=0≠dR_total 로 보존 위반이라 금지.
    if n == 0:
        return np.zeros(0)
    if not np.isfinite(s) or s <= 0.0:
        return np.full(n, float(dR_total) / n)
    return float(dR_total) * w / s


def redistribute_summary(q, dR_total: float, focus_p: float = 1.0) -> dict:
    """재분배 요약: ΔR_local 최대/평균/집중도(총합 50% 담는 상위분율) + 보존 확인."""
    dR = redistribute(q, dR_total, focus_p)
    n = int(dR.size)
    tot = float(dR.sum())
    pos = dR[dR > 0]
    hot50 = 0.0
    if pos.size:
        srt = np.sort(pos)[::-1]; cum = np.cumsum(srt)
        hot50 = float((np.searchsorted(cum, 0.5 * cum[-1]) + 1) / pos.size)
    return {'dR_total_in': float(dR_total), 'dR_total_out': tot,
            'preserved': bool(abs(tot - float(dR_total)) < 1e-9 * max(1.0, abs(float(dR_total)))),
            'dR_local_max': float(dR.max()) if n else 0.0,
            'dR_local_mean': float(dR.mean()) if n else 0.0,
            'conc_ratio': float(dR.max() / max(dR.mean(), 1e-30)) if n else 0.0,
            'hot_frac_50': hot50, 'n': n, 'focus_p': p if (p := max(0.0, float(focus_p))) else 0.0}


# ─────────────────────────── self-test ───────────────────────────
def _selftest() -> int:
    fails = []
    rng = np.random.default_rng(0)
    q = rng.random(1000) ** 3                                   # skewed (hot-spot 유사)
    dR = 42.0
    # 1) 끝점 보존 (Σ = dR_total) — p=1
    d1 = redistribute(q, dR, 1.0)
    if abs(d1.sum() - dR) > 1e-9:
        fails.append(f'p=1 보존 실패 Σ={d1.sum()}')
    # 2) 끝점 보존 — p=2 (집중해도 Σ 불변)
    d2 = redistribute(q, dR, 2.0)
    if abs(d2.sum() - dR) > 1e-9:
        fails.append(f'p=2 보존 실패 Σ={d2.sum()}')
    # 3) p>1 이 더 집중 (max/mean 증가 = hot voxel에 더 몰림)
    c1 = d1.max() / d1.mean(); c2 = d2.max() / d2.mean()
    if not (c2 > c1):
        fails.append(f'p=2 집중도 {c2:.2f} !> p=1 {c1:.2f}')
    # 4) 발열 없음(q≡0) → 균일 분배로 끝점 보존 (리뷰#3: zeros 아님, Σ=dR)
    d0 = redistribute(np.zeros(10), dR)
    if abs(d0.sum() - dR) > 1e-9 or not np.allclose(d0, dR / 10.0):
        fails.append(f'q≡0 균일보존 실패 Σ={d0.sum()}')
    # 5) 균일 q → 균등 분배 (dR/n)
    du = redistribute(np.ones(10), dR, 1.0)
    if not np.allclose(du, dR / 10.0):
        fails.append('균일 q 균등분배 실패')
    # 6) 음수/비유한 q 안전 (제거 후 분배, 보존) — p=1 AND p=0 (리뷰#5: p=0 재진입 방지)
    qm = q.copy(); qm[0] = -1.0; qm[1] = np.inf; qm[2] = np.nan
    for pp in (1.0, 0.0):
        dm = redistribute(qm, dR, pp)
        if abs(dm.sum() - dR) > 1e-9 or dm[0] != 0 or dm[1] != 0 or dm[2] != 0:
            fails.append(f'p={pp} 음수/비유한 처리 실패 (Σ={dm.sum()}, dm[:3]={dm[:3]})')
    # 6b) 극단 p 수치붕괴 → 균일 폴백(보존) (리뷰#7)
    de = redistribute(q, dR, 1e4)
    if abs(de.sum() - dR) > 1e-6:
        fails.append(f'극단 p 보존 실패 Σ={de.sum()}')
    # 7) summary 보존 플래그
    s = redistribute_summary(q, dR, 1.5)
    if not s['preserved'] or not (0 < s['hot_frac_50'] <= 1):
        fails.append(f'summary 이상 {s}')
    print('selftest OK' if not fails else 'selftest FAIL: ' + '; '.join(fails))
    if not fails:
        print(f"  p=1 conc {c1:.1f}× → p=2 conc {c2:.1f}× (집중), 끝점 {dR} 보존, hot_frac_50 {s['hot_frac_50']:.3f}")
    return 1 if fails else 0


if __name__ == '__main__':
    import sys
    raise SystemExit(_selftest())
