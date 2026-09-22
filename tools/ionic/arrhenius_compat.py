#!/usr/bin/env python3
"""arrhenius_compat.py — C3/C4/C5 를 **온도별 자격 시드 평균의 재표본**으로 잰다 (2판 · 회신 BL 반영).

왜 별도 도구인가 (사다리 ②③ 를 밟고 왔다)
  `build_final_conductivity.py` 는 b2o3/modelc D 값이 **하드코딩**된 일회용이고
  C3 의 재표본 절차가 없다. `msd_diffusive_check.py` 는 런 하나의 plateau 를
  보는 도구지 온도 3점을 잇지 않는다. 기존 도구에 플래그로 붙일 자리가 없다.

⛔ 초판(2026-09-08)이 틀린 것 — 회신 BL 결함 2
  초판은 "시드 하나 = 세 온도를 모두 돈 한 런 묶음" 이라며 **시드 번호를 묶어** 공동 재표본했다.
  드라이버는 온도마다 다른 RNG 를 쓴다 — `disorder_ensemble_diffusion.py:427`
  `seed=args.seed + 1000*ci + int(T)`. 같은 번호라는 것 외에 pairing 근거가 없고, 세 온도의
  반복은 **독립**이다. 그리고 초판은 온도마다 시드 수가 같아야 시작했다 — 09-01 개정 R1
  (온도별 2/3 자격)로 시드가 빠지면 아예 못 돌았다.

이 판이 재는 것 (lpsocl_box331_closure_conditions_2026_09_07.json C3·C4·C5 + 개정 2026-09-11)
  · 표본 단위 = **온도별 자격 시드의 D 평균**. 온도마다 시드를 복원추출해 평균을 만든다 (온도 간 독립).
  · **800 K 평균 하나를 두 구간 식에 함께 쓴다** — 두 구간 Ea 가 같은 800 K 값을 공유하는 상관은
    이것으로 살아난다 (회신 BG Q4 · BL 결함 2). 시드 번호 pairing 은 하지 않는다.
  · ΔEa = Ea(600–800) − Ea(800–1000) 를 **직접** 계산 → CI95 전체가 [−δ,+δ] 안이면 compatible,
    전체가 밖이면 incompatible, 경계와 겹치면 inconclusive(HOLD).
  · 같은 재표본에서 3점 무가중 ln D 적합의 Ea 분포도 낸다 → C5(CI95 폭 ≤ 해상도) · C4(leave-one-seed-out
    Ea 가 그 CI95 안).
  · 온도별 시드 수가 달라도 된다 (2·3·3 등). 온도마다 최소 `--min_per_T`(기본 2 = R1) 개.
    `null` 칸 = 자격 없는 런(no_value) — 제외하고 **목록에 남긴다**. 어느 런을 뺄지는 이 도구가 정하지 않는다.
  · 재표본은 난수 없이 **전수 열거**한다 (온도별 n^n 개 평균의 곱). 곱이 너무 크면 고정 시드 MC 로 떨어지고
    그 사실을 출력에 적는다.
  · 대조(⛔ 판정 아님): 800 K 를 두 구간에 **따로** 뽑은 분포. 공유 쪽 SD 가 **더 커야** 정상이다 —
    ΔEa 에서 ln D800 의 계수가 (c1+c2) 라 (c1+c2)² > c1²+c2². 대조가 같으면 공유를 안 살린 것이다.

⛔ 이 도구가 **못 하는 것**
  · D 를 계산하지 않는다 — `msd_diffusive_check.py --mto` 의 값을 받는다. MSD 규약(창 2–50 ps · MTO ·
    자유절편)을 여기서 다시 구현하지 않는다 (convention_check.py 가 감시하는 복제를 늘리지 않으려고).
  · plateau·홉·골격(C2·C2b·C6)을 판정하지 않는다 — 그건 앞 게이트다. 어느 런이 자격인지도 정하지 않는다.
  · δEa·해상도를 **정하지 않는다.** 카드에서 읽는다 (`--card`). 하드코딩 금지.
  · 온도가 3점이 아니면 시작하지 않는다 (2점이면 C3 가 성립하지 않는다 → no_value).
  · 시드 간 상관이 실제로 있는지 검정하지 못한다 — 독립을 **가정**한다 (드라이버 시드 구조가 근거).
  · n=2~3 의 재표본 꼬리가 거칠다는 사실을 고치지 못한다 — 그래서 민감도(LOO)를 같이 찍는다.

  python3 tools/ionic/arrhenius_compat.py --d d.json \
      --card db/properties/lpsocl_box331_closure_conditions_2026_09_07.json
  python3 tools/ionic/arrhenius_compat.py --selftest
"""
from __future__ import annotations
import argparse, itertools, json, math, pathlib, random, statistics, sys

KB = 8.617333262e-5          # eV/K
MAX_EXACT = 200_000          # 전수 열거 상한 (넘으면 고정 시드 MC)
MC_N = 20_000
MC_SEED = 20260911


# ── 분산비 판정 규칙 (회신 BU · 2026-09-22 1저자 합의) ────────────────────────
#: **무엇을 가르나.** 시드 간 Ea 산포가 *구조 무질서* 때문인지 *런 내부 통계* 때문인지.
#:   σ̄²_within = 시드별 부트스트랩 σ²(Ea) 의 **평균** (⛔ 중앙값 아님)
#:   s²_seed   = 시드별 Ea 의 표본분산
#:   R = s²_seed / σ̄²_within,  귀무(구조 산포 없음) 아래 **R ~ χ²_{n−1}/(n−1)**
#: ⛔ **폐기된 초안**: IQR/1.349 로 SD 를 만들어 비교하려 했다. 두 번 틀렸다 —
#:   ① n=5 에서 IQR 이 SD 보다 **더** 흔들린다(실측 0.573 vs 0.365)
#:   ② 1.349 는 **모집단** 상수다. n=5 표본 비는 1.053 이라 SD 를 **1.28 배 과대평가**한다.
#: ⚠ σ̄²_within 을 **오차 없는 상수**로 본다 — 부트스트랩 복제가 충분하다는 가정이다.
#:   복제가 적으면 R 의 분모도 흔들리므로 이 문턱이 낙관적이 된다.
VR_P_3SIGMA = 0.0013498980316301035   # 단측 1 − Φ(3)
VR_P_95 = 0.05
VR_MIN_SEEDS = 3                      # n=2 는 표본분산의 dof 가 1 — 판정하지 않는다
#: 회신 BU 본문은 검출한계를 *"σ_struct ≈ 2 σ_within"* 으로 적었다. 정확값은
#: `√(R_3σ − 1)` 이고 n=5 에서 **1.857** 이다 (E[R] = 1 + (σ_s/σ_w)²). 회신의 "≈2" 는
#: 반올림이고, 여기서는 **정확값을 계산해 적는다**.


def _gammainc_reg(s, x):
    """정규화 하부 불완전감마 `P(s, x)`. (scipy 없이 — 이 도구는 stdlib 전용이다)"""
    if s <= 0 or x < 0:
        return None
    if x == 0:
        return 0.0
    lead = math.exp(-x + s * math.log(x) - math.lgamma(s))
    if x < s + 1.0:                                   # 급수
        ap, total, d = s, 1.0 / s, 1.0 / s
        for _ in range(1000):
            ap += 1.0
            d *= x / ap
            total += d
            if abs(d) < abs(total) * 1e-16:
                break
        return total * lead
    tiny = 1e-300                                     # 연분수 (Q 쪽)
    b, c, d = x + 1.0 - s, 1.0 / tiny, 1.0 / (x + 1.0 - s)
    h = d
    for i in range(1, 1000):
        an = -i * (i - s)
        b += 2.0
        d = an * d + b
        if abs(d) < tiny:
            d = tiny
        c = b + an / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        de = d * c
        h *= de
        if abs(de - 1.0) < 1e-16:
            break
    return 1.0 - lead * h


def chi2_cdf(x, k):
    """χ²_k 누적분포. ⛔ `k` 는 양의 정수 자유도."""
    return _gammainc_reg(k / 2.0, x / 2.0)


def chi2_ppf(p, k):
    """χ²_k 분위수 (이분법). ⛔ 못 하는 것: `p` 가 0/1 이면 None — 무한대를 흉내내지 않는다."""
    if not (0.0 < p < 1.0) or k < 1:
        return None
    hi = max(10.0, 2.0 * k)
    for _ in range(80):
        if chi2_cdf(hi, k) >= p:
            break
        hi *= 2.0
    lo = 0.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if chi2_cdf(mid, k) < p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def variance_ratio_thresholds(n_seeds):
    """→ `{"dof", "R_3sigma", "R_95", "sd_ratio_3sigma", "sigma_struct_over_within_at_3sigma"}`"""
    k = int(n_seeds) - 1
    if k < 1:
        return None
    r3 = chi2_ppf(1.0 - VR_P_3SIGMA, k) / k
    r95 = chi2_ppf(1.0 - VR_P_95, k) / k
    return {"dof": k, "R_3sigma": r3, "R_95": r95,
            "sd_ratio_3sigma": math.sqrt(r3),
            "sigma_struct_over_within_at_3sigma": math.sqrt(max(r3 - 1.0, 0.0))}


def variance_ratio_verdict(ea_by_seed, sigma_within_by_seed):
    """**분산비 판정** — 시드 간 Ea 산포가 구조인가 통계인가 (회신 BU 규칙 그대로).

    `ea_by_seed` / `sigma_within_by_seed` = `{"s1": 0.31, …}` / `{"s1": 0.02, …}` [eV].
    두 딕셔너리의 **키가 같아야** 한다 — 하나라도 짝이 없으면 **판정하지 않는다**.

    ⛔⛔ **판정 보류가 기본값이다.** σ_within 이 하나라도 없거나(블록 plateau 미검출)
    0 이면 `R` 을 **계산하지 않고** None 으로 둔다. 있는 것만으로 비를 만들면 분모가 섞인다.
    ⛔ `R ≤ R_95` 를 *"통계로 설명된다"* 로 쓰지 않는다 — 검출한계를 같이 적는다
    (`detection_limit` 필드). n=5 의 검정력이 그 문장을 허락하지 않는다.

    ⛔ 이 함수가 **못 하는 것**
      · σ_within 을 **계산하지 않는다** — `msd_diffusive_check.joint_ea_bootstrap` 이 낸다.
      · 블록 길이가 전 시드에 같은지 **검사하지 못한다**(σ 만 받는다). 호출자가 보장한다.
      · 구조 산포가 *무엇 때문인지*(Cl/S 배열? 밀도?) 말하지 못한다. 있다/없다까지다.
    """
    seeds = sorted(ea_by_seed)
    n = len(seeds)
    th = variance_ratio_thresholds(n) or {}
    out = {"n_seeds": n, "seeds": seeds, "R": None, "s2_seed": None,
           "sigma2_within_mean": None, **th,
           "rule": "R = s²_seed / σ̄²_within ~ χ²_{n−1}/(n−1)  (회신 BU 2026-09-22)",
           "aggregation": "σ̄²_within 은 σ² 의 **평균**이다 (중앙값 아님)"}
    if n < VR_MIN_SEEDS:
        out["verdict"] = "판정보류_시드부족"
        out["why"] = f"시드 {n} 개 — {VR_MIN_SEEDS} 개 미만이면 표본분산을 판정에 쓰지 않는다."
        return out
    missing = [s for s in seeds
               if sigma_within_by_seed.get(s) is None or not sigma_within_by_seed.get(s, 0) > 0]
    if missing:
        out["verdict"] = "판정보류_σ_within_없음"
        out["missing_sigma_seeds"] = missing
        out["why"] = ("σ_within 을 **못 구한** 시드가 있다 " + str(missing) +
                      " — 블록 길이 plateau 가 안 나왔거나 부트스트랩을 안 돌렸다. "
                      "있는 것만으로 R 을 만들지 않는다 (분모가 섞인다).")
        return out
    s2 = statistics.variance([float(ea_by_seed[s]) for s in seeds])
    sw2 = sum(float(sigma_within_by_seed[s]) ** 2 for s in seeds) / n
    R = s2 / sw2
    out.update({"s2_seed": s2, "sigma2_within_mean": sw2, "R": R,
                "sd_seed_eV": math.sqrt(s2), "sd_within_eV": math.sqrt(sw2)})
    if R > th["R_3sigma"]:
        out["verdict"] = "구조_산포_있음"
        out["why"] = f"R = {R:.3f} > {th['R_3sigma']:.3f} (단측 p < {VR_P_3SIGMA:.5f})"
    elif R > th["R_95"]:
        out["verdict"] = "시사적_판정보류"
        out["why"] = (f"{th['R_95']:.3f} < R = {R:.3f} ≤ {th['R_3sigma']:.3f} — "
                      "95 % 는 넘고 3σ 는 못 넘는다.")
    else:
        out["verdict"] = "구조_산포_미검출"
        out["why"] = f"R = {R:.3f} ≤ {th['R_95']:.3f}"
        out["forbidden_phrasing"] = ("⛔ *\"시드 간 차이는 통계로 설명된다\"* 로 쓰지 않는다. "
                                     "**못 봤다**와 **없다**는 다르다.")
    out["detection_limit"] = {
        "sigma_struct_over_within": th["sigma_struct_over_within_at_3sigma"],
        "sd_seed_over_within": th["sd_ratio_3sigma"],
        "sigma_struct_eV_at_3sigma": (th["sigma_struct_over_within_at_3sigma"]
                                      * math.sqrt(sw2)) if sw2 else None,
        "note": ("E[R] = 1 + (σ_struct/σ_within)² 가 문턱에 닿는 지점 — **≈50 % 검정력**이지 "
                 "보장이 아니다. 회신 BU 본문의 '≈2 σ_within' 은 이 값의 반올림이다."),
    }
    return out


def ea_two_point(T1, D1, T2, D2):
    """두 온도 사이의 아레니우스 기울기 Ea [eV]. T1 < T2 를 가정하지 않는다."""
    if D1 <= 0 or D2 <= 0:
        raise ValueError("D 는 양수여야 한다")
    return KB * math.log(D2 / D1) / (1.0 / T1 - 1.0 / T2)


def delta_ea(D_by_T, temps):
    """ΔEa = Ea(T0–T1) − Ea(T1–T2). temps 는 오름차순 3개. D_by_T[T1] 이 **두 구간에 공유**된다."""
    t0, t1, t2 = temps
    return (ea_two_point(t0, D_by_T[t0], t1, D_by_T[t1])
            - ea_two_point(t1, D_by_T[t1], t2, D_by_T[t2]))


def ea_three_point(D_by_T, temps):
    """3점 **무가중** ln D vs 1/(k_B T) 최소제곱 기울기 → Ea [eV] (09-04 판정: 가중적합 안 한다)."""
    xs = [1.0 / (KB * T) for T in temps]
    ys = [math.log(D_by_T[T]) for T in temps]
    if any(D_by_T[T] <= 0 for T in temps):
        raise ValueError("D 는 양수여야 한다")
    xm, ym = statistics.fmean(xs), statistics.fmean(ys)
    sxx = sum((x - xm) ** 2 for x in xs)
    sxy = sum((x - xm) * (y - ym) for x, y in zip(xs, ys))
    return -sxy / sxx


def eligible_table(raw, min_per_T):
    """`null` 칸을 빼고 온도별 자격 시드만 남긴다. 부족하면 **시작하지 않는다**."""
    table, excluded = {}, []
    for T, cells in raw.items():
        keep = {}
        for s, v in cells.items():
            if v is None:
                excluded.append((T, s))
            else:
                keep[s] = float(v)
        table[T] = keep
    temps = tuple(sorted(table))
    if len(temps) != 3:
        raise SystemExit(f"⛔ 온도가 3점이어야 한다 — 받은 것: {temps}. "
                         "2점이면 C3(두 구간 비교)가 성립하지 않는다 → no_value 다.")
    short = {T: len(v) for T, v in table.items() if len(v) < min_per_T}
    if short:
        raise SystemExit(f"⛔ 자격 시드가 부족한 온도가 있다 {short} (최소 {min_per_T}/온도 — 09-01 개정 R1). "
                         "그 온도는 정의되지 않는다 → 3점이 못 되므로 no_value. 이 도구는 여기서 멈춘다.")
    return table, temps, excluded


def mean_resamples(vals):
    """n 개 값의 복원추출 전수 열거 → n**n 개 평균 (각각 등확률)."""
    vals = list(vals)
    n = len(vals)
    return [statistics.fmean(vals[i] for i in draw)
            for draw in itertools.product(range(n), repeat=n)]


def _draws(per_T_means, temps, extra_800=False):
    """온도별 평균 목록의 곱을 낸다 — 전수(≤ MAX_EXACT) 또는 고정 시드 MC. → (draw 목록, 방식 문자열)"""
    lists = [per_T_means[T] for T in temps]
    if extra_800:
        lists.append(per_T_means[temps[1]])       # 800 K 를 한 번 더 (대조용 독립 뽑기)
    n_total = 1
    for L in lists:
        n_total *= len(L)
    if n_total <= MAX_EXACT:
        return list(itertools.product(*lists)), f"전수 열거 {n_total}개"
    rng = random.Random(MC_SEED)
    return [tuple(rng.choice(L) for L in lists) for _ in range(MC_N)], \
        f"고정 시드 MC {MC_N}개 (전수 {n_total}개는 상한 {MAX_EXACT} 초과)"


def resample_stats(table, temps):
    """핵심. 온도별 평균 재표본 → ΔEa(공유 800 K) · Ea3(3점) 분포와 대조(독립 800 K) SD."""
    means = {T: mean_resamples(table[T].values()) for T in temps}
    draws, how = _draws(means, temps)
    dEa, Ea3 = [], []
    for d in draws:
        D = dict(zip(temps, d))
        dEa.append(delta_ea(D, temps))
        Ea3.append(ea_three_point(D, temps))
    draws_c, how_c = _draws(means, temps, extra_800=True)
    t0, t1, t2 = temps
    dEa_c = [ea_two_point(t0, a, t1, b) - ea_two_point(t1, b2, t2, c)
             for a, b, c, b2 in draws_c]
    return {"means_per_T": {T: len(means[T]) for T in temps}, "how": how,
            "dEa": dEa, "Ea3": Ea3,
            "contrast_indep800": {"how": how_c, "sd": statistics.pstdev(dEa_c),
                                  "min": min(dEa_c), "max": max(dEa_c)}}


def percentile(vals, q):
    """백분위 (선형 보간). numpy 없이 — 이 도구는 stdlib 만 쓴다."""
    v = sorted(vals)
    if len(v) == 1:
        return v[0]
    k = (len(v) - 1) * q
    lo = math.floor(k); hi = math.ceil(k)
    return v[lo] if lo == hi else v[lo] + (v[hi] - v[lo]) * (k - lo)


def verdict(ci_lo, ci_hi, delta):
    """C3 ③④⑤ 를 그대로 옮긴다. 문턱은 호출부가 카드에서 읽어 넘긴다."""
    if ci_lo >= -delta and ci_hi <= delta:
        return "compatible", "CI 전체가 허용영역 [−δ, +δ] 안"
    if ci_lo > delta or ci_hi < -delta:
        return "incompatible", "CI 전체가 허용영역 밖 — 곡률 주장 가능"
    return "inconclusive", "CI 가 허용영역 경계와 겹친다 → HOLD (⛔ '양립하지 않는다' 가 아니라 '판정하지 못했다')"


def read_thresholds_from_card(path):
    """⛔ δEa 와 해상도를 카드에서 **읽는다**. 도구가 정하지 않는다."""
    d = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    c = d["2_닫힘_조건"]
    c3 = c["C3_아레니우스_양립_재설계_2026_09_07"]
    c5 = c["C5_정밀도_해상도_2026_09_07_복원"]
    return {"delta_eV": float(c3["봉인_허용차_δEa_eV"]), "res_eV": float(c5["봉인_해상도_eV"]),
            "ratified": c3.get("✅_비준", "")}


def analyse(table, temps, delta, res):
    rs = resample_stats(table, temps)
    dEa, Ea3 = rs["dEa"], rs["Ea3"]
    lo, hi = percentile(dEa, 0.025), percentile(dEa, 0.975)
    v, why = verdict(lo, hi, delta)
    full = {T: statistics.fmean(table[T].values()) for T in temps}
    point = delta_ea(full, temps)
    e_lo, e_hi = percentile(Ea3, 0.025), percentile(Ea3, 0.975)
    width = e_hi - e_lo
    loo = {}
    for T in temps:
        for s in table[T]:
            if len(table[T]) < 2:
                continue                       # 하나 남으면 평균이 아니다 — 민감도로도 안 찍는다
            keep = {TT: (statistics.fmean(vv for ss, vv in table[TT].items() if not (TT == T and ss == s)))
                    for TT in temps}
            loo[f"−{T}K/{s}"] = {"Ea3_eV": ea_three_point(keep, temps), "dEa_eV": delta_ea(keep, temps)}
    c4_ok = all(e_lo <= x["Ea3_eV"] <= e_hi for x in loo.values()) if loo else None
    sd_shared = statistics.pstdev(dEa)
    return {
        "temps": list(temps), "seeds_per_T": {T: sorted(table[T]) for T in temps},
        "표본_단위": "온도별 자격 시드 D 의 평균 — 온도 간 독립 재표본, 800 K 평균 하나를 두 구간에 공유 (시드 번호 pairing 없음)",
        "delta_eV": delta, "resolution_eV": res,
        "D_mean_per_T": full,
        "C3": {"dEa_point_eV": point, "resample": rs["how"], "n": len(dEa),
               "CI95": [lo, hi], "min": min(dEa), "max": max(dEa), "median": statistics.median(dEa),
               "sd": sd_shared, "verdict": v, "why": why},
        "Ea3": {"point_eV": ea_three_point(full, temps), "CI95": [e_lo, e_hi], "width_eV": width,
                "C5_within_resolution": width <= res},
        "C4_leave_one_seed_out": {"per_drop": loo, "all_inside_Ea3_CI95": c4_ok},
        "대조_판정아님": {"indep800_sd": rs["contrast_indep800"]["sd"], "shared800_sd": sd_shared,
                       "공유가_더_넓다": sd_shared > rs["contrast_indep800"]["sd"],
                       "⛔": "800 K 를 두 구간에 따로 뽑은 대조다. 공유 쪽 SD 가 커야 상관을 살린 것이다. 판정에 쓰지 않는다"},
        "⛔_LOO_는_불확도가_아니다": "민감도 진단이다. 독립 반복으로 읽지 않는다",
    }


def _selftest():
    ok = bad = 0
    def chk(c, m):
        nonlocal ok, bad
        print(("  ⭕ " if c else "  ⛔ ") + m); ok += c; bad += (not c)

    T = (600, 800, 1000)
    Ea, D0 = 0.30, 1e-3
    D = {t: D0 * math.exp(-Ea / (KB * t)) for t in T}
    chk(abs(delta_ea(D, T)) < 1e-9, "직선 아레니우스면 ΔEa = 0")
    chk(abs(ea_two_point(600, D[600], 800, D[800]) - Ea) < 1e-9, "두점 Ea 가 참값을 준다")
    chk(abs(ea_three_point(D, T) - Ea) < 1e-9, "3점 무가중 적합 Ea 가 참값을 준다")
    Dc = dict(D); Dc[800] = D[800] * 1.30
    chk(delta_ea(Dc, T) > 0, "800 K 가 높으면 ΔEa > 0 (저온구간 Ea 가 크다)")
    Dc2 = dict(D); Dc2[800] = D[800] * 0.70
    chk(delta_ea(Dc2, T) < 0, "800 K 가 낮으면 ΔEa < 0")

    # ── 시드 산포 0 이면 분포 폭 0 (양성) ─────────────────────────────────
    tab0 = {t: {"s2": D[t], "s3": D[t], "s4": D[t]} for t in T}
    r0 = analyse(tab0, T, 0.05, 0.05)
    chk(abs(r0["C3"]["CI95"][1] - r0["C3"]["CI95"][0]) < 1e-12 and r0["Ea3"]["width_eV"] < 1e-12,
        "시드 산포 0 → ΔEa·Ea3 CI 폭 0")
    chk(r0["C3"]["n"] == 27 ** 3 and "전수" in r0["C3"]["resample"], "3·3·3 시드는 전수 열거 27³ = 19683")

    # ── ⭐ 공유 800 K vs 독립 800 K — 공유 쪽 SD 가 **커야** 한다 ────────────
    #    ΔEa 에서 ln D800 의 계수는 (c1+c2) 다. 따로 뽑으면 c1²+c2² 만 남는다.
    #    잘못 짜서 800 K 를 두 번 뽑으면 둘이 같아진다 → 그것이 음성이다.
    bias = {"s2": 0.80, "s3": 1.00, "s4": 1.25}
    tab = {t: {s: D[t] * b for s, b in bias.items()} for t in T}
    r = analyse(tab, T, 0.05, 0.05)
    c1 = KB / (1 / 600 - 1 / 800); c2 = KB / (1 / 800 - 1 / 1000)
    sd_ln = statistics.pstdev([math.log(m) for m in mean_resamples(tab[800].values())])
    pred_ratio = (c1 + c2) / math.sqrt(c1 ** 2 + c2 ** 2)
    ratio = r["대조_판정아님"]["shared800_sd"] / r["대조_판정아님"]["indep800_sd"]
    chk(r["대조_판정아님"]["공유가_더_넓다"], "⭕양성: 공유 800 K 분포 SD > 독립 800 K 대조 SD")
    chk(ratio > 1.05, f"⛔음성: 공유/독립 SD 비 {ratio:.3f} — 1 에 가까우면 800 K 를 두 번 뽑은 것이다")
    chk(sd_ln > 0 and abs(ratio - pred_ratio) / pred_ratio < 0.35,
        f"해석 일관: 600·1000 산포를 합친 비 {ratio:.3f} 는 순수 800 K 예측 {pred_ratio:.3f} 근처에 있다")

    # ── 온도별 시드 수가 달라도 돈다 (2·3·3) · null 은 제외하고 남긴다 ──────
    raw = {"600": {"s2": D[600] * 0.9, "s3": D[600] * 1.1, "s4": None},
           "800": {"s2": D[800] * 0.95, "s3": D[800], "s4": D[800] * 1.05},
           "1000": {"s2": D[1000], "s3": D[1000] * 1.02, "s4": D[1000] * 0.98}}
    raw_i = {int(k): v for k, v in raw.items()}
    tb, tp, ex = eligible_table(raw_i, 2)
    chk(ex == [(600, "s4")] and len(tb[600]) == 2 and len(tb[800]) == 3, "null 칸은 제외 목록에 남고 나머지로 간다")
    r2 = analyse(tb, tp, 0.05, 0.05)
    chk(r2["C3"]["n"] == 4 * 27 * 27, "2·3·3 시드 → 전수 4·27·27 = 2916 (온도별 n^n 의 곱)")
    chk(len(r2["C4_leave_one_seed_out"]["per_drop"]) == 8, "LOO 는 온도별 시드마다 (2+3+3 = 8)")

    # ── 음성: 온도 하나가 1 시드면 시작하지 않는다 ───────────────────────
    raw_bad = {600: {"s2": D[600], "s3": None, "s4": None}, 800: raw_i[800], 1000: raw_i[1000]}
    try:
        eligible_table(raw_bad, 2); ok_short = False
    except SystemExit as e:
        ok_short = "부족" in str(e)
    chk(ok_short, "⛔음성: 자격 시드 1개인 온도 → SystemExit (조용히 1시드 평균으로 가지 않는다)")
    try:
        eligible_table({600: raw_i[600], 800: raw_i[800]}, 2); ok_two = False
    except SystemExit as e:
        ok_two = "3점" in str(e)
    chk(ok_two, "⛔음성: 온도 2점 → SystemExit (2점이면 C3 가 없다)")
    try:
        ea_two_point(600, 0.0, 800, 1e-5); ok_zero = False
    except ValueError:
        ok_zero = True
    chk(ok_zero, "⛔음성: D ≤ 0 을 거부한다 (log 가 조용히 -inf 가 되지 않는다)")

    # ── 판정 경계 ────────────────────────────────────────────────────────
    chk(verdict(-0.01, 0.02, 0.05)[0] == "compatible", "CI 가 허용영역 안 → compatible")
    chk(verdict(0.08, 0.12, 0.05)[0] == "incompatible", "CI 가 허용영역 밖 → incompatible")
    chk(verdict(-0.02, 0.09, 0.05)[0] == "inconclusive", "⛔음성: 경계와 겹치면 HOLD — 판정하지 않는다")
    chk("판정하지 못했다" in verdict(-0.02, 0.09, 0.05)[1], "inconclusive 문구가 '양립하지 않는다' 로 새지 않는다")

    # ── C5·C4 배선 ───────────────────────────────────────────────────────
    chk(r2["Ea3"]["C5_within_resolution"] == (r2["Ea3"]["width_eV"] <= 0.05), "C5 = Ea3 CI95 폭 ≤ 해상도")
    rr = analyse(tb, tp, 0.05, 1e-6)
    chk(rr["Ea3"]["C5_within_resolution"] is False, "⛔음성: 해상도를 1 µeV 로 주면 C5 불충족이 난다")
    chk(r0["C4_leave_one_seed_out"]["all_inside_Ea3_CI95"] is True, "산포 0 이면 LOO 가 전부 CI 안 (C4 통과)")

    # ── MC 대체 경로: 재현 가능 ──────────────────────────────────────────
    big = {t: {f"s{i}": D[t] * (1 + 0.05 * (i - 3)) for i in range(1, 7)} for t in T}   # 6·6·6 → 6^18
    rb1 = analyse(big, T, 0.05, 0.05); rb2 = analyse(big, T, 0.05, 0.05)
    chk("MC" in rb1["C3"]["resample"] and rb1["C3"]["CI95"] == rb2["C3"]["CI95"],
        "전수 상한 초과 → 고정 시드 MC, 두 번 돌려도 같은 CI")

    # ── ⛔ 2026-09-15: **정본 입력 형식을 읽는가** ────────────────────────
    #   db/properties/lpsocl_box331_c3_input_d_2026_09_11.json 은 `_출처`·`_단위` 를
    #   달고 있는데 로더가 `int('_출처')` 로 죽었다. 도구가 자기 정본을 못 읽었다.
    import tempfile as _tf, os as _os
    _dd = {"_출처": "이 키 때문에 죽으면 안 된다", "_단위": "cm^2/s",
           **{str(t): {f"s{i}": D[t] for i in (2, 3, 4)} for t in T}}
    _fd, _p = _tf.mkstemp(suffix=".json"); _os.close(_fd)
    pathlib.Path(_p).write_text(json.dumps(_dd, ensure_ascii=False), encoding="utf-8")
    try:
        _raw = json.loads(pathlib.Path(_p).read_text(encoding="utf-8"))
        _raw = {int(k): dict(v) for k, v in _raw.items() if not str(k).startswith("_")}
        chk(set(_raw) == set(T), "⛔음성: `_출처`·`_단위` 가 있어도 정본 d.json 을 읽는다 (메타키 건너뜀)")
    except ValueError as _e:
        chk(False, f"⛔음성 실패: 정본 형식에서 죽었다 — {_e}")
    finally:
        _os.unlink(_p)
    _raw2 = {int(k): dict(v) for k, v in {"_x": {}, "600": {"s2": 1.0}}.items()
             if not str(k).startswith("_")}
    chk(600 in _raw2 and len(_raw2) == 1, "⛔음성: 메타키만 건너뛰고 온도키는 남긴다")

    # ── 분산비 판정 규칙 (회신 BU) ─────────────────────────────────────
    chk(abs(chi2_ppf(1 - VR_P_3SIGMA, 4) - 17.800) < 5e-3
        and abs(chi2_ppf(0.95, 4) - 9.488) < 5e-3,
        "χ² 분위수가 회신 BU 의 값을 재현한다 (χ²₄: 3σ 17.800 · 95 % 9.488)")
    _t5 = variance_ratio_thresholds(5)
    chk(abs(_t5["R_3sigma"] - 4.450) < 5e-3 and abs(_t5["R_95"] - 2.372) < 5e-3
        and abs(_t5["sd_ratio_3sigma"] - 2.110) < 5e-3,
        "n=5 문턱: R 4.450 / 2.372 · SD 비 2.110 (회신 BU 표와 일치)")
    chk(abs(_t5["sigma_struct_over_within_at_3sigma"] - 1.857) < 5e-3,
        "검출한계 정확값 1.857 σ_within — 회신의 '≈2' 는 반올림이다")
    try:
        from scipy import stats as _st
        chk(abs(chi2_ppf(1 - VR_P_3SIGMA, 4) - _st.chi2.ppf(1 - VR_P_3SIGMA, 4)) < 1e-6
            and abs(chi2_cdf(9.488, 4) - _st.chi2.cdf(9.488, 4)) < 1e-10
            and abs(chi2_cdf(0.7, 9) - _st.chi2.cdf(0.7, 9)) < 1e-12,
            "⛔음성: 손으로 쓴 χ² 가 scipy 와 급수·연분수 **양쪽 가지**에서 일치한다")
    except ImportError:
        print("  … scipy 없음 — 교차검증 건너뜀 (stdlib 구현은 그대로 쓴다)")
    chk(chi2_ppf(0.0, 4) is None and chi2_ppf(1.0, 4) is None and chi2_ppf(0.5, 0) is None,
        "⛔음성: p 가 0/1 이거나 dof < 1 이면 None (무한대를 흉내내지 않는다)")

    _ea = {"s1": 0.20, "s2": 0.25, "s3": 0.30, "s4": 0.35, "s5": 0.40}   # SD = 0.0791
    _v = variance_ratio_verdict(_ea, {k: 0.02 for k in _ea})             # R ≈ 15.6
    chk(_v["verdict"] == "구조_산포_있음" and _v["R"] > _t5["R_3sigma"],
        "시드 SD 가 런 내부의 4 배면 **구조 산포 있음**")
    _v2 = variance_ratio_verdict(_ea, {k: 0.055 for k in _ea})           # R ≈ 2.07
    chk(_v2["verdict"] == "구조_산포_미검출" and "forbidden_phrasing" in _v2
        and _v2["detection_limit"]["sigma_struct_eV_at_3sigma"] > 0,
        "미검출이면 **금지 문구**와 **검출한계**를 같이 낸다")
    _v3 = variance_ratio_verdict(_ea, {k: 0.043 for k in _ea})           # R ≈ 3.38
    chk(_v3["verdict"] == "시사적_판정보류",
        "95 % 는 넘고 3σ 는 못 넘으면 **시사적, 판정 보류**")
    chk(variance_ratio_verdict({"s1": 0.2, "s2": 0.3},
                               {"s1": 0.01, "s2": 0.01})["verdict"] == "판정보류_시드부족",
        "⛔음성: 시드 2 개면 판정하지 않는다")
    _vm = variance_ratio_verdict(_ea, {"s1": 0.02, "s2": 0.02, "s3": None,
                                       "s4": 0.02, "s5": 0.02})
    chk(_vm["verdict"] == "판정보류_σ_within_없음" and _vm["R"] is None
        and _vm["missing_sigma_seeds"] == ["s3"],
        "⛔음성: σ_within 이 하나라도 없으면 **R 을 아예 안 만든다** (있는 것만으로 안 낸다)")
    chk(variance_ratio_verdict(_ea, {k: 0.0 for k in _ea})["R"] is None,
        "⛔음성: σ_within 이 0 이면 나눗셈을 시도하지 않는다")
    #: ⛔음성 — 평균이냐 중앙값이냐가 **판정을 바꾼다**. 규칙은 평균이다.
    _ea3 = {"s1": 0.28, "s2": 0.30, "s3": 0.32}                # s²_seed = 4.0e-4
    _sg3 = {"s1": 0.01, "s2": 0.01, "s3": 0.10}                # 평균 σ² 3.4e-3 · 중앙값 1e-4
    _vx = variance_ratio_verdict(_ea3, _sg3)
    chk(abs(_vx["sigma2_within_mean"] - 3.4e-3) < 1e-12
        and _vx["verdict"] == "구조_산포_미검출",
        "⛔음성: σ² 의 **평균**을 쓴다 — 중앙값을 썼다면 R=4.0 으로 '시사적' 이 됐다")

    print(f"selftest: ⭕ {ok} · ⛔ {bad}")
    return 0 if bad == 0 else 1


def main():
    ap = argparse.ArgumentParser(description="C3/C4/C5 — 온도별 자격 시드 평균의 재표본 (800 K 공유)")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--d", help='D 표 JSON: {"600":{"s2":1.2e-5,"s4":null,...},"800":{...},"1000":{...}} [cm^2/s]. null = 자격 없는 런')
    ap.add_argument("--card", help="δEa·해상도를 읽을 닫힘조건 카드 (하드코딩 금지)")
    ap.add_argument("--delta", type=float, help="⚠ 카드가 없을 때만. 쓰면 화면에 경고를 찍는다")
    ap.add_argument("--resolution", type=float, help="⚠ 카드가 없을 때만 (C5 해상도)")
    ap.add_argument("--min_per_T", type=int, default=2,
                    help="온도별 최소 자격 시드 수 (기본 2 = 09-01 개정 R1 '3시드 중 2개 이상')")
    ap.add_argument("--out", help="결과 JSON 경로")
    ap.add_argument("--vr", metavar="JSON",
                    help='**분산비 판정**(회신 BU): {"Ea_eV":{"s1":0.31,…},'
                         '"sigma_Ea_eV":{"s1":0.02,…}} — 시드 간 산포가 구조인가 통계인가. '
                         'σ 는 msd_diffusive_check.py --ea_boot 이 낸다.')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    if a.vr:
        raw = json.loads(pathlib.Path(a.vr).read_text(encoding="utf-8"))
        ea = {k: v for k, v in (raw.get("Ea_eV") or {}).items() if not str(k).startswith("_")}
        sg = {k: v for k, v in (raw.get("sigma_Ea_eV") or {}).items() if not str(k).startswith("_")}
        if not ea:
            raise SystemExit("⛔ --vr JSON 에 `Ea_eV` 가 없다.")
        extra = sorted(set(sg) - set(ea))
        if extra:
            print(f"⚠ σ 에만 있는 시드 {extra} — 무시한다 (Ea 가 기준이다)")
        v = variance_ratio_verdict(ea, sg)
        print(f"\n시드 {v['n_seeds']} 개 {v['seeds']} · dof {v.get('dof')}")
        if v["R"] is None:
            print(f"  ★ 판정: **{v['verdict']}** — {v['why']}")
        else:
            print(f"  s_seed   = {v['sd_seed_eV']:.5f} eV   (표본 SD)")
            print(f"  σ̄_within = {v['sd_within_eV']:.5f} eV   (σ² 의 **평균**의 제곱근)")
            print(f"  R = {v['R']:.3f}   문턱 3σ {v['R_3sigma']:.3f} · 95 % {v['R_95']:.3f}")
            print(f"\n  ★ 판정: **{v['verdict']}** — {v['why']}")
            dl = v["detection_limit"]
            print(f"  검출한계: σ_struct ≳ {dl['sigma_struct_over_within']:.3f} σ_within"
                  f" = {dl['sigma_struct_eV_at_3sigma']:.5f} eV  ({dl['note'].split('—')[1].strip()})")
            if "forbidden_phrasing" in v:
                print("  " + v["forbidden_phrasing"])
        if a.out:
            pathlib.Path(a.out).write_text(json.dumps(v, ensure_ascii=False, indent=1) + "\n")
            print(f"\n-> {a.out}")
        raise SystemExit(0)
    if not a.d:
        ap.error("--d 또는 --vr 이 필요하다 (--selftest 제외)")

    raw = json.loads(pathlib.Path(a.d).read_text(encoding="utf-8"))
    # ⛔ 2026-09-15 — `_` 로 시작하는 메타키(`_출처`·`_단위`)를 건너뛴다.
    #   **정본 입력 파일이 바로 그 키를 갖고 있는데** 도구가 `int('_출처')` 로 죽었다
    #   (`db/properties/lpsocl_box331_c3_input_d_2026_09_11.json`). 도구가 자기 정본
    #   형식을 못 읽은 것이다 — 출처를 지우고 돌리라는 뜻이 되어 계보가 끊긴다.
    raw = {int(k): dict(v) for k, v in raw.items() if not str(k).startswith("_")}
    table, temps, excluded = eligible_table(raw, a.min_per_T)

    if a.card:
        th = read_thresholds_from_card(a.card)
        delta, res = th["delta_eV"], th["res_eV"]
        print(f"δEa = {delta} eV · 해상도 = {res} eV  ← 카드에서 읽음 ({pathlib.Path(a.card).name})")
        if th["ratified"]:
            print(f"  비준: {th['ratified'][:80]}")
    elif a.delta is not None and a.resolution is not None:
        delta, res = a.delta, a.resolution
        print(f"⚠ δEa = {delta} · 해상도 = {res} eV — **카드가 아니라 명령줄에서** 받았다. 판정 기록에 쓰지 말 것.")
    else:
        raise SystemExit("⛔ --card 또는 (--delta 와 --resolution) 이 필요하다. 문턱을 도구가 정하지 않는다.")

    r = analyse(table, temps, delta, res)
    r["excluded_cells_null"] = [f"{T}K/{s}" for T, s in excluded]
    c3, e3 = r["C3"], r["Ea3"]
    print(f"\n온도 {temps} · 자격 시드 {r['seeds_per_T']}"
          + (f" · 제외(null) {r['excluded_cells_null']}" if excluded else ""))
    print(f"  ΔEa (점추정)      = {c3['dEa_point_eV']:+.4f} eV")
    print(f"  재표본 {c3['resample']} · CI95 = [{c3['CI95'][0]:+.4f}, {c3['CI95'][1]:+.4f}] eV"
          f"  (범위 [{c3['min']:+.4f}, {c3['max']:+.4f}])")
    print(f"  허용영역          = [{-delta:+.4f}, {+delta:+.4f}] eV")
    print(f"\n  ★ C3 판정: **{c3['verdict']}**  — {c3['why']}")
    if c3["verdict"] == "inconclusive":
        print("     ⇒ C3 불충족 → **HOLD**. 값은 있으나 정밀도가 모자란 것이지 값이 없는 게 아니다.")
    print(f"  Ea(3점) = {e3['point_eV']:.4f} eV · CI95 [{e3['CI95'][0]:.4f}, {e3['CI95'][1]:.4f}] · 폭 {e3['width_eV']:.4f} eV"
          f" → C5 {'충족' if e3['C5_within_resolution'] else '불충족(HOLD)'} (해상도 {res})")
    c4 = r["C4_leave_one_seed_out"]
    print(f"  C4 leave-one-seed-out Ea 전부 CI95 안: {c4['all_inside_Ea3_CI95']}")
    for k, v in c4["per_drop"].items():
        print(f"    {k}: Ea3 {v['Ea3_eV']:.4f} · ΔEa {v['dEa_eV']:+.4f} eV")
    cc = r["대조_판정아님"]
    print(f"  대조(판정 아님): 공유 800 K SD {cc['shared800_sd']:.4f} vs 독립 800 K SD {cc['indep800_sd']:.4f}"
          f" → 공유가 더 넓다: {cc['공유가_더_넓다']}")
    if a.out:
        pathlib.Path(a.out).write_text(json.dumps(r, ensure_ascii=False, indent=1) + "\n")
        print(f"\n-> {a.out}")


if __name__ == "__main__":
    main()
