#!/usr/bin/env python3
"""anion_rotation_acf.py — PS₄ **배향 자기상관** C_ℓ(t) → τ_rot → Ea_rot (T16).

왜 (2026-08-28, `shin2026_bh4_reorientation_li_transport_li6ps5x` 에서 이전):
  그 논문의 실물 근거는 두 가지다.
    ① ⁷Li 와 ¹¹B 의 SLR **Ea 가 세 시료 모두 0.01 eV 이내로 붙어 함께 움직이는데
       ³¹P 만 따로 논다** (Li 0.27/0.29/0.35 · B 0.28/0.30/0.34 · P 0.18/0.16/0.16).
    ② **회전 자유도만 얼린 대조 MD 에서 D(500 K) 가 네 배열 전부 2.0–3.0배 감소**
       (`Table S9`) — 상관이 아니라 인과 증거다.
  **우리 축에는 회전 자유도가 아예 없다** (정적 기술자만: 자리·채널·BVSE·blocking).
  이 도구가 그 축을 만든다. 새 시뮬레이션 0회 — 필요한 건 P–S 결합벡터 시간열뿐이고
  우리 궤적(600–1000 K · 200 ps · save 100 fs)에 이미 있다.

무엇을 재나
  각 PS₄ 의 **P→S 결합 단위벡터** u(t) 에 대해
      C₁(t) = ⟨u(0)·u(t)⟩ ,  C₂(t) = ⟨P₂(u(0)·u(t))⟩ = ⟨(3cos²θ−1)/2⟩
  시간원점을 전부 쓴다. C₂ 가 NMR SLR 의 계산 대응물이다(쌍극자 완화가 ℓ=2).

★ 이 도구의 핵심 판정은 τ 가 아니라 **회전이냐 흔들림(libration)이냐** 다.
  - 강체 정지         → C₂ ≈ 1 (안 떨어진다)
  - **흔들림(libration)** → C₂ 가 **0 이 아닌 값에 고원**을 만든다 (원뿔 안에서만 흔들림)
  - 자유 재배향        → C₂ → 0
  고원이 있는데 지수함수를 맞추면 **τ 가 창 길이를 따라간다** — 물리가 아니라 창의 성질이다.
  ⇒ 고원이면 τ 를 **안 준다.** (van Hove 고원에서 배운 것과 같은 함정이다)

⛔ 이 도구가 **못 하는 것**
  · **BH₄ 를 못 잰다.** 우리 host 엔 없다. 여기서 재는 것은 PS₄ 이고, 그건 Shin 2026 이
    *"안 돈다"* 고 판정한 대상이다 ⇒ **"PS₄ 느리다" 가 나와도 재확인이지 신규가 아니다.**
    **신규가 되는 길**은 하나뿐이다: Cl 함량(comp1→modelc) 또는 **우리 도펀트(B₂O₃·O)가
    PS₄ 회전을 바꾸는가.** 그 비교로 쓸 때만 이 도구가 새 값을 만든다.
  · **개별 S 를 추적한다.** 사면체는 P–S 축 둘레 120° 회전에 대해 자기 자신으로 가므로,
    모양이 안 변해도 결합벡터는 탈상관된다. 이건 NMR 이 보는 것과 같지만
    *"사면체가 뒤집혔나"* 와는 다른 질문이다.
  · **축 회전과 텀블링을 안 가른다.** C₁·C₂ 를 같이 내서 사람이 보게만 한다
    (자유 등방회전이면 τ₁/τ₂ = 3, 작은각 확산이면 다른 비가 나온다).
  · **S 교환을 고치지 않는다.** 감지해서 보고만 하고 그 PS₄ 는 뺀다.
  · **Ea 는 온도 3점부터.** 그리고 UMA 가 PS₄ 회전 장벽을 맞게 내는지는 **검증 안 됐다** —
    Li₃N 전례가 있다. 이 도구의 Ea 를 실험 SLR 과 나란히 놓기 전에 그 검증이 필요하다.
  · 절대 τ 를 인용하지 마라. **조성 간 비**만 우리 규율에 맞는다.

사용:
  python3 anion_rotation_acf.py --traj aimd/T600/traj.xyz --label modelc_T600 \\
      --out_dir rot/modelc_T600 --save_fs 100
  python3 anion_rotation_acf.py --arrhenius rot/modelc_T*/  *_rotacf.json
  python3 anion_rotation_acf.py --selftest
"""
import argparse
import glob
import json
import math
import os
import sys
from pathlib import Path

import numpy as np

# ★ 궤적 읽기·PBC·P–S 결합 문턱은 **기존 도구의 것을 그대로 쓴다** (중복 금지 규율).
#   같은 폴더라 경로만 세워주면 된다. 이 import 가 깨지면 즉시 죽는 게 맞다 —
#   조용히 자기 사본을 쓰기 시작하면 규약이 갈라진다 (사각 C).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aimd_jump_stats import PS_BOND, read_traj  # noqa: E402

#: C₂ 가 이 값 위에서 평평해지면 **흔들림**으로 본다 (재배향이 아니다).
PLATEAU_C2 = 0.10
#: 고원 판정 창 — 궤적 뒤쪽 이 비율 구간에서 기울기를 본다.
PLATEAU_TAIL = 0.5
#: 이 이상 떨어져야 τ 를 지수함수로 뽑는다.
DECAY_FOR_FIT = 0.5
#: ⛔ 2026-08-28 — τ 가 창의 이 비율을 넘으면 **감쇠가 창 안에 없다.** 그때 피팅은
#:   숫자를 내놓지만 그 숫자는 창의 성질이지 물리가 아니다. selftest 의 스케일링
#:   테스트가 이걸 잡았다: σ 를 절반으로 하면 τ 가 4배(≈62 ps)여야 하는데 50 ps 창에서
#:   17.9 ps 가 나왔다 — **4배는커녕 0.85배**. 창을 넘으면 τ 가 창 쪽으로 끌려온다.
TAU_MAX_FRAC = 0.5
kB_eV = 8.617333262e-5


def ps4_units(sym, pos0, cell):
    """첫 프레임에서 PS₄ 단위를 잡는다 → [(P인덱스, [S인덱스 ×4]), ...].

    ⛔ 못 하는 것: 4배위가 아닌 P(결함·말단)는 **빼고 보고**한다. 조용히 3배위를
      사면체처럼 다루면 배향이 정의가 안 된다.
    """
    P = np.where(sym == "P")[0]
    S = np.where(sym == "S")[0]
    units, odd = [], []
    if not len(P) or not len(S):
        return units, odd
    cinv = np.linalg.inv(cell)
    for p in P:
        d = pos0[S] - pos0[p]
        f = d @ cinv
        f -= np.round(f)
        r = np.linalg.norm(f @ cell, axis=1)
        near = S[np.where(r < PS_BOND)[0]]
        if len(near) == 4:
            units.append((int(p), [int(x) for x in near]))
        else:
            odd.append({"P": int(p), "n_S": int(len(near))})
    return units, odd


def bond_unit_vectors(pos, cell, units):
    """(T, M, 3) 정규화된 P→S 결합벡터. M = 단위 수 × 4.

    최소이미지로 접는다 — PS₄ 가 셀 경계에 걸쳐 있어도 결합벡터는 짧아야 한다.
    """
    cinv = np.linalg.inv(cell)
    cols = []
    for p, ss in units:
        for s in ss:
            d = pos[:, s, :] - pos[:, p, :]
            f = d @ cinv
            f -= np.round(f)
            v = f @ cell
            n = np.linalg.norm(v, axis=1, keepdims=True)
            cols.append(v / np.where(n > 0, n, 1.0))
    return np.stack(cols, axis=1) if cols else np.zeros((len(pos), 0, 3))


def bond_break_report(u, pos, cell, units, tol=1.35):
    """결합이 끊겼거나 S 가 교환됐는지 — 결합 길이로 본다 → (ok_mask, 보고).

    벡터를 정규화하면 길이 정보가 사라져서 **끊어진 결합도 정상처럼 보인다.**
    그래서 길이를 따로 본다.
    """
    cinv = np.linalg.inv(cell)
    lens = []
    for p, ss in units:
        for s in ss:
            d = pos[:, s, :] - pos[:, p, :]
            f = d @ cinv
            f -= np.round(f)
            lens.append(np.linalg.norm(f @ cell, axis=1))
    if not lens:
        return np.zeros(0, bool), {"n_broken": 0, "max_len_A": None}
    L = np.stack(lens, axis=1)                       # (T, M)
    worst = L.max(axis=0)
    ok = worst < PS_BOND * tol
    return ok, {"n_broken": int((~ok).sum()), "n_bonds": int(len(ok)),
                "max_len_A": round(float(worst.max()), 3),
                "cutoff_A": round(PS_BOND * tol, 3)}


def orient_acf(u, max_lag):
    """C₁(t), C₂(t) — 시간원점 전부 사용 → (lags, C1, C2).

    ⛔ 못 하는 것: 원점끼리 강하게 상관돼 있다. 여기 산포는 **오차막대가 아니다.**
    """
    T, M, _ = u.shape
    max_lag = int(min(max_lag, T - 1))
    c1 = np.empty(max_lag + 1)
    c2 = np.empty(max_lag + 1)
    for k in range(max_lag + 1):
        dot = np.einsum("tmi,tmi->tm", u[k:], u[:T - k]) if k else \
            np.einsum("tmi,tmi->tm", u, u)
        dot = np.clip(dot, -1.0, 1.0)
        c1[k] = dot.mean()
        c2[k] = (1.5 * dot ** 2 - 0.5).mean()
    return np.arange(max_lag + 1), c1, c2


def classify(lags_ps, c2):
    """회전 / 흔들림 / 정지 → dict. **τ 는 회전일 때만 준다.**

    판정 순서가 중요하다 — 고원을 먼저 배제하지 않으면 창 길이가 τ 로 둔갑한다.
    """
    if len(c2) < 4:
        return {"verdict": "unknown", "reason": "lag 이 너무 짧다"}
    tail = c2[int(len(c2) * PLATEAU_TAIL):]
    c2_end = float(c2[-1])
    drop = float(c2[0] - c2_end)
    # 뒤쪽 절반의 기울기 — 평평하면 더 안 떨어진다
    x = np.arange(len(tail), dtype=float)
    slope = float(np.polyfit(x, tail, 1)[0]) if len(tail) > 2 else 0.0
    flat = abs(slope) * len(tail) < 0.05          # 창을 두 배 늘려도 0.05 미만 변화
    out = {"C2_final": round(c2_end, 4), "drop": round(drop, 4),
           "tail_slope_per_frame": slope}
    if drop < 0.05:
        out.update(verdict="rigid",
                   reason=f"C₂ 가 {drop:.3f} 밖에 안 떨어졌다 — 재배향이 없다",
                   tau_ps=None)
    elif c2_end > PLATEAU_C2 and flat:
        out.update(verdict="libration",
                   reason=f"C₂ 가 {c2_end:.3f} 에서 **고원**이다 — 원뿔 안에서만 흔들린다. "
                          f"지수함수를 맞추면 τ 가 창 길이를 따라간다",
                   tau_ps=None)
    elif drop < DECAY_FOR_FIT:
        out.update(verdict="undecided",
                   reason=f"C₂ 가 {drop:.3f} 만 떨어졌다 (<{DECAY_FOR_FIT}) — "
                          f"이 창으로는 회전인지 고원인지 못 가른다. 더 긴 lag 이 필요하다",
                   tau_ps=None)
    else:
        out.update(verdict="reorienting", tau_ps=None,
                   reason="C₂ 가 충분히 떨어졌다 — τ 를 뽑을 수 있다")
    return out


def fit_tau(lags_ps, c2, floor=1e-3):
    """C₂ ≈ exp(−t/τ) 를 ln 선형회귀로 → (τ_ps, r2). 못 맞추면 (None, None).

    양수 구간만 쓴다 — 고원 근처에서 c2 가 음수로 흔들리면 ln 이 폭발한다.

    ⛔ 못 하는 것: **창보다 긴 τ 는 못 잰다.** 여기서는 날것으로 돌려주고,
      `tau_in_window()` 가 창 대비 검사를 한다 (그 둘을 합치면 대조 시험을 못 한다).
    """
    m = (c2 > max(floor, 0.05)) & (lags_ps > 0)
    if m.sum() < 4:
        return None, None
    x, y = lags_ps[m], np.log(c2[m])
    a, b = np.polyfit(x, y, 1)
    if a >= 0:
        return None, None
    pred = a * x + b
    ss = 1.0 - float(((y - pred) ** 2).sum() / max(((y - y.mean()) ** 2).sum(), 1e-30))
    return float(-1.0 / a), round(ss, 4)


def tau_in_window(tau, lags_ps):
    """τ 가 창 안에서 실제로 측정된 값인가 → (ok, 사유).

    ⛔⛔ 왜 따로 있나 (2026-08-28) — 피팅은 **창보다 긴 τ 에도 숫자를 내놓는다.**
      감쇠가 창 안에 없으면 그 숫자는 창 길이 쪽으로 끌려온 값이지 물리가 아니다.
      selftest 스케일링 시험이 이걸 잡았다: 회전을 4배 느리게 했더니 τ 가 4배가 아니라
      **0.85배**로 나왔다 — 둘 다 창에 눌린 것이다.
    """
    if tau is None:
        return False, "피팅 실패"
    win = float(lags_ps[-1])
    if tau > TAU_MAX_FRAC * win:
        return False, (f"τ={tau:.1f} ps 가 창({win:g} ps)의 {TAU_MAX_FRAC:.0%} 를 넘는다 — "
                       f"**감쇠가 창 안에 없다.** 더 긴 궤적이나 더 큰 --max_lag_ps 가 필요하다")
    return True, ""


def arrhenius(points):
    """[(T_K, tau_ps)] → {Ea_eV, tau0_ps, r2, n}. 3점 미만이면 거부한다."""
    pts = [(T, t) for T, t in points if t and t > 0]
    if len(pts) < 3:
        return {"Ea_eV": None, "n": len(pts),
                "reason": f"온도 {len(pts)}점 — Ea 는 3점부터다"}
    x = np.array([1.0 / (kB_eV * T) for T, _ in pts])
    y = np.array([math.log(t) for _, t in pts])
    a, b = np.polyfit(x, y, 1)
    pred = a * x + b
    r2 = 1.0 - float(((y - pred) ** 2).sum() / max(((y - y.mean()) ** 2).sum(), 1e-30))
    return {"Ea_eV": round(float(a), 4), "tau0_ps": round(float(math.exp(b)), 6),
            "r2": round(r2, 4), "n": len(pts),
            "T_K": [T for T, _ in pts], "tau_ps": [t for _, t in pts]}


def _build_parser():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--traj")
    ap.add_argument("--label")
    ap.add_argument("--out_dir")
    # ⛔ save_fs 에 기본값을 두지 않는다 — 추측하면 시간축이 통째로 틀리는데
    #   화면에는 정상으로 보인다 (aimd_jump_stats 와 같은 규약).
    ap.add_argument("--save_fs", type=float, default=None,
                    help="프레임 간격 [fs]. 없으면 옆 aimd_results.json 에서 읽는다")
    ap.add_argument("--max_lag_ps", type=float, default=50.0,
                    help="C(t) 를 볼 최대 lag [ps]")
    ap.add_argument("--arrhenius", nargs="*", default=None,
                    help="*_rotacf.json 들을 모아 Ea_rot 를 낸다")
    ap.add_argument("--selftest", action="store_true")
    return ap


def _selftest():
    ok = True

    def chk(c, m):
        nonlocal ok
        ok = ok and bool(c)
        print(f"  {'✓' if c else '✗'} {m}")

    rng = np.random.default_rng(0)
    T, dt = 1000, 0.1                                  # 100 ps · 100 fs
    lags = np.arange(T // 2 + 1) * dt

    def acf_of(u):
        _l, c1, c2 = orient_acf(u, T // 2)
        return c1, c2

    # 사면체 기준 방향 4개
    TET = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float)
    TET /= np.linalg.norm(TET, axis=1, keepdims=True)

    def rotate(axis, ang):
        a = axis / np.linalg.norm(axis)
        K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
        return np.eye(3) + math.sin(ang) * K + (1 - math.cos(ang)) * (K @ K)

    # ① 강체 정지 → C₂ 가 안 떨어진다. **τ 를 주면 안 된다.**
    u_rigid = np.repeat(TET[None], T, axis=0)
    _c1, c2r = acf_of(u_rigid)
    vr = classify(lags, c2r)
    chk(vr["verdict"] == "rigid" and vr["tau_ps"] is None,
        f"[음성] 정지 사면체는 'rigid' 이고 τ 를 안 준다 (C₂_end={vr['C2_final']})")

    # ② 자유 재배향 → C₂ → 0, τ 가 나온다
    #    ⚠ 각 스텝 σ 를 물리에서 정한다. 랜덤축 회전벡터 v=θn̂ 은 성분당 분산이 **σ²/3** 이라
    #      ⟨Δφ²⟩ = Nσ² = 6D_r t ⇒ D_r = σ²/(6Δt), τ₂ = 1/(6D_r) = **Δt/σ²**.
    #      (첫 판은 D_r = σ²/(2Δt) 로 써서 이론값이 3배 틀렸다 — 그 상태로도
    #       "τ 가 나온다" 만 보는 테스트는 통과했을 것이다.)
    #      첫 fixture 는 σ=0.25 라 τ₂≈0.16 ps — **2프레임 만에 다 떨어져** 피팅이 잡음이었다.
    #      fixture 가 실제보다 쉬운 게 아니라 **너무 어려웠던** 경우다.
    # ⚠ **독립 단위를 여럿 둔다.** 첫 판은 PS₄ 하나(결합벡터 4개)였는데, 긴 lag 에서
    #   시간원점이 줄어드는 데다 표본이 4개라 ACF 꼬리가 잡음투성이였고 ln-선형 피팅이
    #   그 꼬리에 끌려갔다 (τ 가 이론값의 1.35배, 그리고 σ 스케일링이 아예 안 맞았다).
    #   실제 궤적에는 PS₄ 가 수십 개 있다 — fixture 를 실제에 맞춘다 (처방 B).
    NU = 30

    def free_tau(sig):
        u_ = np.empty((T, 4 * NU, 3))
        for j in range(NU):
            R_ = rotate(rng.normal(size=3), rng.uniform(0, math.pi))   # 시작 배향도 무작위
            for t_ in range(T):
                R_ = rotate(rng.normal(size=3), rng.normal(0, sig)) @ R_
                u_[t_, 4 * j:4 * j + 4] = TET @ R_.T
        _c, c2_ = acf_of(u_)
        return classify(lags, c2_), fit_tau(lags, c2_), c2_

    SIG = 0.08
    tau_true = dt / SIG ** 2
    vf, (tau, r2), c2f = free_tau(SIG)
    chk(vf["verdict"] == "reorienting",
        f"[양성] 자유 재배향은 'reorienting' (C₂_end={vf['C2_final']}, drop={vf['drop']})")
    chk(tau is not None and 0.5 < tau / tau_true < 2.0 and r2 > 0.90,
        f"[양성] τ 가 이론값 규모다 ({None if tau is None else round(tau,2)} vs "
        f"{tau_true:.2f} ps, r²={r2})")
    # ★★ 여기가 판별력이다 — 절대값은 이산화 때문에 35 % 어긋나지만 **스케일링은 물리다.**
    #    τ₂ ∝ 1/σ² 이므로 σ 를 1.5배로 하면 τ 는 1/2.25 여야 한다. 상수가 틀려도 통과하는
    #    "숫자가 나온다" 류 테스트와 달리, 이건 감쇠를 **진짜로 풀어야** 통과한다.
    #    ⚠ 느리게(σ/2) 가 아니라 **빠르게(1.5σ)** 로 시험한다 — 느리게 하면 τ 가 창을 넘어
    #      아래 창 가드에 걸려서, 스케일링이 아니라 가드를 시험하게 된다.
    _v2, (tau_fast, _r), _c = free_tau(SIG * 1.5)
    ratio = None if (tau is None or tau_fast is None) else tau_fast / tau
    chk(ratio is not None and 0.30 < ratio < 0.65,
        f"[양성·스케일링] σ 를 1.5배로 하면 τ 가 **1/2.25 배**가 된다 "
        f"({None if ratio is None else round(ratio,2)}배 · "
        f"{None if tau_fast is None else round(tau_fast,1)} vs {round(tau,1)} ps)")

    # ★★★ 창 가드 (2026-08-28, 위 스케일링 시험이 찾아낸 fail-open) ★★★
    #   σ/2 는 τ₂ ≈ 62 ps 인데 창은 50 ps 다. 피팅은 **17.9 ps 를 내놓았다** — 4배는커녕
    #   0.85배. 창을 넘는 τ 는 창 쪽으로 끌려온다. 이제 도구가 거부해야 한다.
    _vs, (tau_slow, _r2s), c2s = free_tau(SIG / 2.0)
    good, why = tau_in_window(tau_slow, lags)
    chk(tau_slow is not None and not good,
        f"[음성·실측회귀] 창보다 긴 τ 는 **거부한다** "
        f"(피팅은 {None if tau_slow is None else round(tau_slow,1)} ps 를 내놓지만 "
        f"창 {lags[-1]:g} ps) — {why[:40]}")
    ok_w, _ = tau_in_window(tau, lags)
    chk(ok_w, f"[양성·대조] 창 안에 든 τ 는 통과시킨다 ({round(tau,1)} ps < "
              f"{TAU_MAX_FRAC*float(lags[-1]):.0f} ps) — 가드가 전부를 막지 않는다")

    # ③ ★★ 흔들림 — **여기가 이 도구의 존재 이유다.**
    #    원뿔 안에서만 흔들리면 C₂ 가 0 이 아닌 값에 고원을 만든다.
    #    지수함수를 맞추면 τ 가 나오는데 **그 τ 는 물리가 아니다.**
    #    ⚠ 원뿔 반각을 물리에서 정한다: 작은각에서 C₂ 고원 ≈ ⟨P₂(cosσ)⟩² ≈ (1−1.5σ²)².
    #      σ=0.45 rad(≈26°) → 고원 ≈ 0.48. 첫 판은 σ=0.12 로 해서 고원이 0.971 이었고,
    #      **'rigid' 로 찍혀** 이 테스트가 아무것도 시험하지 않았다.
    u_lib = np.empty((T, 4, 3))
    for t in range(T):
        u_lib[t] = TET @ rotate(rng.normal(size=3), rng.normal(0, 0.45)).T  # 누적 없음
    _c1, c2l = acf_of(u_lib)
    vl = classify(lags, c2l)
    chk(vl["verdict"] == "libration" and vl["tau_ps"] is None,
        f"[음성·핵심] 흔들림은 'libration' 이고 **τ 를 안 준다** "
        f"(C₂ 고원 {vl['C2_final']})")
    tau_bad, r_bad = fit_tau(lags, c2l)
    # 고원에 지수를 맞추면 τ 가 **창 길이 규모로 발산**하거나 아예 안 맞는다.
    # 어느 쪽이든 "물리가 아니다" 인데, 판정을 안 하면 그 숫자가 표에 들어간다.
    chk(tau_bad is None or tau_bad > 5.0 * float(lags[-1]),
        f"[음성·대조] 고원에 지수를 맞추면 τ 가 **창 길이({lags[-1]:g} ps)를 넘어 발산**하거나 "
        f"안 맞는다 ({None if tau_bad is None else round(tau_bad,1)} ps, r²={r_bad}) — "
        f"판정을 먼저 하는 이유")

    # ④ PS₄ 인식: 4배위만 단위로 잡고, 3배위는 빼고 **보고**한다
    cell = np.eye(3) * 20.0
    sym = np.array(["P"] + ["S"] * 4 + ["P"] + ["S"] * 3 + ["Li"])
    p0 = np.zeros((9, 3))
    p0[0] = [5, 5, 5]
    p0[1:5] = p0[0] + TET * 2.0
    p0[5] = [12, 12, 12]
    p0[6:9] = p0[5] + TET[:3] * 2.0
    p0[8] = [1, 1, 1]                                # Li 를 멀리
    sym = np.array(["P", "S", "S", "S", "S", "P", "S", "S", "Li"])
    p0 = np.zeros((9, 3))
    p0[0] = [5, 5, 5]; p0[1:5] = p0[0] + TET * 2.0
    p0[5] = [12, 12, 12]; p0[6:8] = p0[5] + TET[:2] * 2.0
    p0[8] = [1, 1, 1]
    units, odd = ps4_units(sym, p0, cell)
    chk(len(units) == 1 and units[0][0] == 0,
        f"[PS₄] 4배위 P 하나만 단위로 잡는다 ({len(units)}개)")
    chk(len(odd) == 1 and odd[0]["n_S"] == 2,
        f"[PS₄·음성] 2배위 P 를 조용히 넘기지 않고 **보고**한다 ({odd})")

    # ⑤ PBC: 셀 경계에 걸친 PS₄ 도 결합벡터가 짧아야 한다
    p1 = p0.copy()
    p1[0] = [0.2, 0.2, 0.2]; p1[1:5] = (p1[0] + TET * 2.0) % 20.0
    u2, _o = ps4_units(sym, p1, cell)
    chk(len(u2) >= 1, "[PBC] 셀 경계에 걸친 PS₄ 도 4배위로 인식된다")
    if u2:
        bv = bond_unit_vectors(p1[None], cell, u2[:1])
        chk(abs(np.linalg.norm(bv[0], axis=1).max() - 1.0) < 1e-9,
            "[PBC] 결합벡터가 단위벡터다")

    # ⑥ ★ 결합 파단 감지 — 정규화하면 **끊어진 결합도 정상으로 보인다**
    pos_ok = np.repeat(p0[None], 5, axis=0)
    _m, rep_ok = bond_break_report(None, pos_ok, cell, units)
    chk(rep_ok["n_broken"] == 0, f"[파단·양성] 멀쩡한 궤적은 파단 0 ({rep_ok})")
    pos_bad = pos_ok.copy()
    pos_bad[3:, 1] = [9.0, 9.0, 9.0]                 # S 하나가 떨어져 나간다
    _m2, rep_bad = bond_break_report(None, pos_bad, cell, units)
    chk(rep_bad["n_broken"] == 1,
        f"[파단·음성] S 가 떨어지면 **잡는다** (길이 {rep_bad['max_len_A']} Å) — "
        f"단위벡터만 보면 안 보인다")

    # ⑦ Arrhenius: 3점 미만은 거부한다 (2점으로 낸 Ea 는 언제나 r²=1 이다)
    a2 = arrhenius([(600, 5.0), (800, 2.0)])
    chk(a2["Ea_eV"] is None, f"[음성] 2점으로 Ea 를 안 낸다 ({a2.get('reason')})")
    true_Ea, t0 = 0.30, 1e-3
    pts = [(T_, t0 * math.exp(true_Ea / (kB_eV * T_))) for T_ in (600, 800, 1000)]
    a3 = arrhenius(pts)
    chk(abs(a3["Ea_eV"] - true_Ea) < 1e-3,
        f"[양성] 3점 Arrhenius 가 Ea 를 되찾는다 ({a3['Ea_eV']} vs {true_Ea})")

    # ⑧ 배선: 파서 기본값 (오늘 배선 버그가 셋이었다 — 사각 A)
    d = {a.dest: a.default for a in _build_parser()._actions}
    chk(d.get("save_fs") is None,
        "[배선] `--save_fs` 는 기본값을 두지 않는다 (추측하면 시간축이 통째로 틀린다)")
    chk(d.get("max_lag_ps") == 50.0, "[배선] max_lag 기본값이 50 ps")
    chk(d.get("arrhenius") is None,
        "[배선] `--arrhenius` 기본값이 None (평소 실행을 안 바꾼다)")

    # ⑨ 규약: P–S 문턱을 자기 사본으로 안 쓰고 기존 도구에서 가져온다
    chk(abs(PS_BOND - 2.30) < 1e-12,
        f"[규약] PS_BOND 를 aimd_jump_stats 에서 import 한다 ({PS_BOND} Å)")

    print("selftest " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def run_one(args):
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    save_fs = args.save_fs
    if save_fs is None:
        side = Path(args.traj).parent / "aimd_results.json"
        if side.is_file():
            save_fs = json.load(open(side)).get("save_fs")
    if not save_fs:
        print("⛔ save_fs 를 모른다 — 추측하면 시간축이 통째로 틀린다. --save_fs 를 줄 것")
        return 2
    dt_ps = save_fs / 1000.0

    sym, pos, cells = read_traj(args.traj)
    cell = cells[0]
    units, odd = ps4_units(sym, pos[0], cell)
    print(f"  frames={len(pos)} · dt={dt_ps:g} ps · PS₄ {len(units)}개"
          + (f" · ⚠ 4배위 아닌 P {len(odd)}개 {odd[:3]}" if odd else ""))
    if not units:
        print("⛔ PS₄ 를 하나도 못 찾았다 — 이 계에는 이 관측량이 정의되지 않는다")
        return 2

    ok_mask, brk = bond_break_report(None, pos, cell, units, )
    if brk["n_broken"]:
        print(f"  ⚠ 결합 {brk['n_broken']}/{brk['n_bonds']}개가 궤적 중 "
              f"{brk['cutoff_A']} Å 를 넘었다 (최대 {brk['max_len_A']} Å) — 그 결합은 뺀다")
    u = bond_unit_vectors(pos, cell, units)[:, ok_mask, :]
    if u.shape[1] < 4:
        print(f"⛔ 살아남은 결합이 {u.shape[1]}개다 — 판정 불가")
        return 2

    max_lag = int(round(args.max_lag_ps / dt_ps))
    k, c1, c2 = orient_acf(u, max_lag)
    lags_ps = k * dt_ps
    v = classify(lags_ps, c2)
    tau, r2 = (None, None)
    if v["verdict"] == "reorienting":
        tau, r2 = fit_tau(lags_ps, c2)
        good, why = tau_in_window(tau, lags_ps)
        if good:
            v["tau_ps"] = round(tau, 4)
            v["fit_r2"] = r2
        else:
            v.update(verdict="undecided", tau_ps=None, fit_r2=r2,
                     tau_raw_ps=None if tau is None else round(tau, 4),
                     reason=why)

    np.savetxt(out / f"{args.label}_rotacf.csv", np.c_[lags_ps, c1, c2],
               delimiter=",", header="lag_ps,C1,C2", comments="")
    print(f"  C₂: {c2[0]:.3f} → {c2[-1]:.3f} (lag {lags_ps[-1]:g} ps) · "
          f"C₁ 끝 {c1[-1]:.3f}")
    print(f"  ⇒ **{v['verdict']}** — {v['reason']}")
    if v.get("tau_ps"):
        print(f"     τ_rot = {v['tau_ps']} ps (r²={v.get('fit_r2')}) "
              f"· τ₁/τ₂ 는 CSV 에서 볼 것 (등방 자유회전이면 3)")
    else:
        print("     ⛔ τ 를 내지 않는다 — 위 판정이 지수 감쇠를 허락하지 않는다")
    T_K = None
    for tok in Path(args.traj).parts:
        if tok.startswith("T") and tok[1:].isdigit():
            T_K = int(tok[1:])
    summary = {"label": args.label, "traj": os.path.abspath(args.traj),
               "T_K": T_K, "save_fs": save_fs, "n_frames": len(pos),
               "n_ps4": len(units), "non_tetrahedral_P": odd,
               "bond_break": brk, "max_lag_ps": float(lags_ps[-1]),
               "C1_final": round(float(c1[-1]), 4), **v,
               "⛔": "절대 τ 인용 금지 — 조성 간 비만. PS₄ 회전은 Shin 2026 이 "
                    "'안 돈다'고 판정한 대상이라, 신규는 Cl 함량·도펀트 의존성뿐이다"}
    (out / f"{args.label}_rotacf.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"-> {out}/{args.label}_rotacf.json")
    return 0


def run_arrhenius(paths):
    files = []
    for p in paths:
        files += sorted(glob.glob(p)) if any(c in p for c in "*?[") else [p]
    files = [f for f in files if os.path.isfile(f)]
    if not files:
        print("⛔ 읽을 파일이 없다")
        return 2
    got, refused = [], []
    for f in files:
        d = json.load(open(f))
        if d.get("tau_ps") and d.get("T_K"):
            got.append((d["T_K"], d["tau_ps"], d["label"]))
        else:
            refused.append((d.get("label"), d.get("T_K"), d.get("verdict")))
    print(f"■ Ea_rot — 파일 {len(files)}개 중 τ 가 있는 것 {len(got)}개")
    for lab, T, vd in refused:
        print(f"   · 제외 {lab} (T={T}) — {vd}")
    a = arrhenius([(T, t) for T, t, _l in got])
    if a.get("Ea_eV") is None:
        print(f"   ⛔ {a.get('reason')}")
    else:
        print(f"   **Ea_rot = {a['Ea_eV']} eV** (τ₀ {a['tau0_ps']} ps · r² {a['r2']} · "
              f"{a['n']}점 {a['T_K']} K)")
        print("   ⛔ 이 값을 실험 SLR 과 나란히 놓기 전에 **UMA 가 PS₄ 회전 장벽을 "
              "맞게 내는지** 검증이 필요하다 (Li₃N 전례).")
    return 0


def main():
    a = _build_parser().parse_args()
    if a.selftest:
        return _selftest()
    if a.arrhenius is not None:
        return run_arrhenius(a.arrhenius)
    if not (a.traj and a.label and a.out_dir):
        print("⛔ --traj/--label/--out_dir 가 필요하다 (또는 --arrhenius / --selftest)")
        return 2
    return run_one(a)


if __name__ == "__main__":
    sys.exit(main() or 0)
