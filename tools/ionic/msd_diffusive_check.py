#!/usr/bin/env python3
"""msd_diffusive_check.py — MSD 가 **진짜 확산 영역**인지 판정한다 (인용 게이트).

왜 필요한가
  D 는 MSD 를 `fit_window_ps` 에서 직선 맞춤해 얻는데, 그 창이 확산 영역이 아니면
  **케이지 진동·드리프트를 확산으로 오독**한다. 실측 두 건:
    · comp2 disorder d=0.5 — 600 K D 가 1.4~2.3e-05 cm²/s (comp1 의 1000 K 값과 동급),
      D(1000)/D(600) 가 1.98~5.6 밖에 안 됨 (0.276 eV 면 8.5 배 기대)
    · comp1 seed3 — D(600) 1.36e-06 ≈ D(800) 1.37e-06 (비 1.007). 물리적으로 불가능.
  둘 다 "Ea 를 냈다"까지는 갔지만 **그 Ea 를 인용하면 안 되는** 상태였다.

판정 (2026-08-30 개정, 회신 AK)
  판정축은 **`D_inc` plateau · 창 안정성 · 실제 독립 hop 수** 세 가지다.
    `D_inc(t1,t2) = [MSD(t2)−MSD(t1)] / [6(t2−t1)]`
  상수 절편은 여기서 **대수적으로 소거**되므로, 케이지 절편이면 창을 옮겨도 평평하고
  진짜 `t^α` 면 계속 움직인다. 실패는 **두 층으로** 나눠 낸다:
    `no-value`  값이 **정의되지 않음** (궤적 무결성 실패 · plateau 부재)
    `HOLD`      값은 있으나 **정밀도 부족** (홉 부족 등)
  ⇒ 처방이 갈린다: 앞은 프로토콜을 고치고, 뒤는 시드·길이를 늘린다.

⛔⛔ **β = 0.80 하드게이트는 폐기됐다** (kb/concepts/beta-gate.md §7-5 2026-08-26 ·
  §7-8b 회신 F 2026-08-27): *"β=1 은 물리, 0.8 은 폐기 수순. β 는 이제 **경보**지
  판정이 아니다."* 우리 운영점에서 고정문턱 0.8 은 **50 % 거짓탈락률**을 보였다.
  β 는 표에 남기고 경보로만 쓴다.
  ⚠ 이 도구는 카드가 폐기된 뒤에도 **나흘간 옛 문턱을 강제**했고, 그 사이 회신 AK 가
    그걸 착수 근거로 다시 인용했다. **판정을 바꿀 때 그 판정을 구현한 도구를 같이 고친다.**

⚠ **MSD 절대 크기**도 본다: 창 끝의 MSD 가 이웃 Li–Li 거리² (~3 Å² 정도) 보다 작으면
  이온이 자기 자리를 못 벗어난 것이라 통계가 없다.

  python3 tools/ionic/msd_diffusive_check.py --glob '~/work/runs/comp2_disorder_relaxed/d*_cfg*/T*/msd.json'
  python3 tools/ionic/msd_diffusive_check.py --glob '~/work/runs/comp1_seeds/s*/d*_cfg*/T*/msd.json'
"""
import argparse
import glob as _glob
import json
import math
import os
import pathlib
import sys

BETA_OK = (0.80, 1.20)
MSD_MIN_A2 = 3.0            # 창 끝 MSD 하한 — 이보다 작으면 자리 이탈을 못 한 것
D_HOP_A = 3.0               # 이웃 Li 자리 간격 [Å] — hops_per_ion.py 와 같은 규약
# β 추정기 잡음 반폭 (귀무 5% 분위 ≈ 중앙값 − 0.12; Li 27개·STO·창 2–50 실측,
# tools/ionic/beta_null_test.py --hop_sweep → db/properties/beta_gate_null_vs_hops_*.csv).
# Li 가 더 많은 셀에서는 보수적(과대)이다 — 잡음은 ~1/√n_Li 로 준다.
BETA_NOISE_5PCT = 0.12


def _covers(t, hi):
    """t 가 hi 까지 실제로 도달하는가 (마지막 간격 하나만큼의 여유 허용).

    ⛔⛔ 2026-08-29 (회신 S) — **이 검사가 없었다.** `lin_fit`/`d_incremental` 은
      `lo <= x <= hi` 로 거른 뒤 점이 3개 이상이기만 하면 맞춤을 돌려줬다.
      그래서 곡선이 100 ps 에서 끝나는데 창 `50–200` 을 요청하면 **50–100 을 맞춰 놓고
      라벨은 50–200** 이 붙었다. MTO 는 최대 lag 를 T/2 로 자르므로 200 ps 생산런의
      최대 lag 가 100 ps 다 — 즉 이건 예외가 아니라 **200 ps 런의 기본 상황**이었다.
      못 잰 것은 통과가 아니다 (이 파일 1502행 주석의 같은 원칙).
    """
    if not t:
        return False
    tmax = max(t)
    if tmax >= hi:
        return True
    if len(t) < 2:
        return False
    dts = sorted(b - a for a, b in zip(t[:-1], t[1:]) if b > a)
    step = dts[len(dts) // 2] if dts else 0.0
    return tmax >= hi - step


def lin_fit(t, y, lo, hi):
    """[lo,hi] 에서 MSD = c + m·t 를 자유 절편으로 맞춘다. (m, c, R²) 또는 None.

    ⛔ 곡선이 hi 까지 안 닿으면 **None** 이다 (회신 S). 잘린 창을 요청한 라벨로
      돌려주면 서로 다른 창이 같은 값이 되고 그게 측정처럼 읽힌다.

    ★★ 2026-08-11 — **이 절편이 β 게이트의 정체다.**
      고체 MSD 는 어느 계든 `MSD(t) = C + 6Dt` 꼴이다 (C = 케이지 진폭 + ballistic 잔재).
      C > 0 이면 log-log 기울기 β 는 **자동으로 1 아래**로 내려간다 — 확산이 아니어서가
      아니라 절편이 있어서다. 실측(db/properties/msd_3sys_200ps_origin.csv):

        계·온도              절편 c    c/MSD@50    β      비고
        B2O3 600 K           1.704 Å²   5.1 %     0.806
        LPSCl1.6 600 K       2.336      7.6 %     0.868
        **LPSOCl 600 K**     4.035     18.2 %     0.615   ← 게이트 탈락
        LPSCl1.6 1000 K      1.952      1.4 %     0.924

      β 가 c/MSD@50 에 거의 단조로 붙어 있고, **탈락한 곡선들의 직선 적합 R² 가
      0.971–0.996** 이다 — MSD 가 직선이 아니어서 탈락한 게 아니다.
      β=0.76 을 만드는 데 필요한 절편은 항상 창끝 MSD 의 ~7.4 % 다(크기 무관).

      ⇒ **게이트 β<0.8 은 사실상 "절편이 창끝 MSD 의 ~6 % 를 넘는가" 를 재고 있다.**
        그건 물리 판정이 아니라 **암묵적 표본 크기 요구**다. 그리고 D 는 이미
        **자유 절편 직선 맞춤**의 기울기에서 나오므로 절편에 영향받지 않는다.

      판별법: 창을 뒤로 밀면서 절편을 본다.
        · 절편이 **상수**·기울기 불변·β 가 1 로 올라감 → 케이지 절편. **D 인용 가능**
        · 절편이 **커지고** 기울기가 떨어지며 β 가 모든 창에서 그대로 → 진짜 sub-diffusion
    """
    if not _covers(t, hi):
        return None
    pts = [(a, b) for a, b in zip(t, y) if lo <= a <= hi]
    if len(pts) < 3:
        return None
    n = len(pts)
    sx = sum(p[0] for p in pts); sy = sum(p[1] for p in pts)
    sxx = sum(p[0] ** 2 for p in pts); sxy = sum(p[0] * p[1] for p in pts)
    den = n * sxx - sx * sx
    if abs(den) < 1e-30:
        return None
    m = (n * sxy - sx * sy) / den
    c = (sy - m * sx) / n
    ybar = sy / n
    ss = sum((c + m * x - yy) ** 2 for x, yy in pts)
    st = sum((yy - ybar) ** 2 for _, yy in pts)
    return m, c, (1.0 - ss / st if st > 1e-30 else float("nan"))


def d_incremental(t, y, lo, hi):
    """구간 증분 확산계수 `D_inc = [MSD(t2)−MSD(t1)] / [6(t2−t1)]` [Å²/ps]. 점 부족이면 None.

    **왜 이게 c 행보다 낫나** (2026-08-27, Codex 회신 F 권고를 받아들인 것):
      자유절편 `c` 는 관측 범위 **밖인 t=0 으로의 외삽**이고 `c`–`m` 오차가 강하게 얽혀
      있어서, 늦은 창에서 c 가 음수로 튀거나(실측: modelc/T700 −4.68 Å²) 요동만으로도
      "커진다/작아진다" 가 뒤집힌다. 반면 **차분은 상수 절편을 대수적으로 소거한다**:
        MSD = c + 6Dt  →  MSD(t2) − MSD(t1) = 6D(t2 − t1)   (c 가 사라진다)
      그래서 케이지 절편이면 창을 옮겨도 D_inc 가 **평평**하고, 진짜 t^α 면
      `D_inc ∝ t^(α−1)` 로 계속 움직인다. **케이지 vs 멱함수를 c 보다 곧게 가른다.**

    ⛔ 이 함수가 못 하는 것:
      · **느린 전이 vs 진짜 멱함수는 여전히 못 가른다.** 둘 다 D_inc 가 움직인다 —
        가르려면 더 긴 궤적에서 plateau 도달 여부를 봐야 한다.
      · 오차막대를 안 준다. 끝점 두 개만 쓰므로 잡음에 그대로 노출된다
        (실무 확정은 block/seed bootstrap CI 로 — 아직 미구현).
      · lag 이 궤적 길이에 가까우면 MSD(t2) 자체가 시간원점 부족으로 못 믿는다.
    """
    if not _covers(t, hi):     # 회신 S — 잘린 창을 요청 라벨로 돌려주지 않는다
        return None
    pts = [(a, b) for a, b in zip(t, y) if lo <= a <= hi]
    if len(pts) < 3 or pts[-1][0] - pts[0][0] <= 0:
        return None
    return (pts[-1][1] - pts[0][1]) / (6.0 * (pts[-1][0] - pts[0][0]))



# ── D_inc plateau 판정 (2026-08-30, 회신 AK) ─────────────────────────────────
#: ⛔⛔ **β=0.80 은 판정이 아니다.** kb/concepts/beta-gate.md §7-5(2026-08-26)·
#:   §7-8b(회신 F, 2026-08-27)에서 폐기됐다 — *"β=1 은 물리, 0.8 은 폐기 수순.
#:   β 는 이제 **경보**지 판정이 아니다."*
#:   그런데 **이 도구는 안 고쳐졌다.** 그래서 2026-08-30 회신 AK 를 쓸 때 폐기된 문턱을
#:   착수 근거로 다시 인용했다 (kb/methodology/selftest_blind_spots_2026_08_28.md 사각 D
#:   의 변형 — 판정은 읽었는데 **도구에 안 내려왔다**).
#:   ⇒ 판정축은 `D_inc` plateau · 창 안정성 · 실제 독립 hop 수다. 아래가 그 구현이다.

#: plateau 로 볼 D_inc 상대 산포 상한. 회신 F 의 "상수 절편이면 창과 무관하게 참값" 에서
#: 온 것이고, 실측 보정값이 아니다 — **문턱을 바꾸면 여기 사유를 적는다.**
DINC_PLATEAU_TOL = 0.10
#: plateau 판정에 최소 몇 개의 창이 필요한가. 두 개로는 '추세' 와 '평평' 을 못 가른다.
DINC_MIN_WINDOWS = 3
#: 이온당 실제 독립 hop 수 하한 — 이보다 적으면 값은 있어도 **정밀도 부족(HOLD)** 이다.
HOPS_MIN_PER_ION = 3.0

#: 사전 고정 보조 창 [ps] — 결과를 보고 고르지 않는다 (회신 AK Q4).
#:   200 ps 생산런의 MTO 최대 lag 는 100 ps 라 100 을 넘는 창은 `_covers` 가 알아서 뺀다.
DINC_WINDOWS = ((2, 50), (10, 50), (25, 100), (50, 100))

#: 실패 코드 — **두 층을 합치지 않는다** (회신 AK Q5).
#:   no_value = 값이 **정의되지 않음** · hold = 값은 있으나 **정밀도 부족**
NO_VALUE = "no_value"
HOLD = "hold"
CITABLE = "citable"


def dinc_plateau(t, y, windows=DINC_WINDOWS, tol=DINC_PLATEAU_TOL):
    """`D_inc` 가 창을 옮겨도 평평한가. → dict

    돌려주는 것: `{"per_window": {(lo,hi): D_inc}, "n": 잰 창 수, "spread": 상대산포,
                  "status": "plateau"|"drifting"|"insufficient", "trend": 부호}`
    상대산포 = (max−min)/|median| — 상수 절편이면 창을 옮겨도 소거되므로 0 에 가깝다.

    ⛔ 이 함수가 못 하는 것
      · **느린 전이 vs 진짜 멱함수를 못 가른다** (`d_incremental` 의 한계 그대로).
      · 오차막대가 없다 — 끝점 두 개만 쓰므로 잡음에 노출된다. `spread` 를
        오차막대로 쓰면 안 된다.
      · 창 목록을 자기가 고르지 않는다. 결과를 보고 창을 고르면 판정이 아니다.
    """
    per = {}
    for lo, hi in windows:
        v = d_incremental(t, y, lo, hi)
        if v is not None and v > 0:
            per[(lo, hi)] = v
    if len(per) < DINC_MIN_WINDOWS:
        return {"per_window": per, "n": len(per), "spread": None,
                "status": "insufficient", "trend": None}
    vals = [per[k] for k in sorted(per)]
    # 🔴 내부리뷰 AX P1-2 (2026-09-04) — 짝수 개일 때 `sorted[n//2]` 는 **위쪽 중앙값**이라
    #   진짜 median 보다 크고, med 가 크면 spread 가 작게 나와 **통과 쪽으로 편향**된다.
    #   실측: [0.122,0.117,0.107,0.100] → 옛 0.117 vs 진짜 0.112 (spread 18.8% → 19.6%).
    #   창이 3개일 때는 정확해서 지금까지 안 드러났고, 생산길이를 늘려 4창이 되는
    #   순간 드러난다. 그래서 400 ps 런 **전에** 고친다.
    _sv = sorted(vals)
    _n = len(_sv)
    med = _sv[_n // 2] if _n % 2 else (_sv[_n // 2 - 1] + _sv[_n // 2]) / 2.0
    spread = (max(vals) - min(vals)) / abs(med) if med else None
    trend = (vals[-1] - vals[0]) / abs(med) if med else None
    return {"per_window": per, "n": len(per), "spread": spread,
            "status": ("plateau" if spread is not None and spread <= tol else "drifting"),
            "trend": trend}


def hops_per_ion_msd(y, d_hop=D_HOP_A):
    """MSD 최댓값에서 읽는 **이온당 유효(독립) 홉 수**. `MSD_max / d²` = f·n (f = 상관계수 ≤ 1).

    ⛔ 2026-09-11 정정 — 옛 판은 이것을 '상한' 이라 불렀는데 방향이 반대다. 되돌아오는 홉은 MSD 를
       **줄이므로** MSD/d² 는 실제 이벤트 수 n 의 **하한**이고, '통계가 충분한가' 에 맞는 양은 바로 이
       유효 홉 수다. 실측(LPSOCl 3×3×1 400 ps): 궤적 계수 20–94/이온 vs MSD/d² 15.5–68, f ≈ 0.67–0.75
       (db/properties/lpsocl_box331_c2b_hops_2026_09_11.json). 실제 이벤트를 세는 것은
       `tools/ionic/aimd_jump_stats.py` (inter-cage) 다 — C2b 판정은 그쪽 계수로 한다 (개정안 A5).
    """
    return (max(y) / d_hop ** 2) if y else None


#: ── He 2018 오차식 + 로그정규 + 블록 부트스트랩 (2026-09-22, 회신 BT) ───────────
#:
#: ⛔⛔ **이 절의 존재 이유는 "He 식을 쓰자" 가 아니라 "He 식만 쓰지 말자" 다.**
#:   회신 BS §6 에서 내가 **적합 창끝 MSD 를 궤적 전체 공식에 넣어** N_eff 를 8 배
#:   과소평가했고(BT 에서 철회), 그 과정에서 세 가지가 드러났다:
#:     ① He 식은 **lag 창을 제한한 적합에 대해 검증된 적이 없다** — 궤적이 길어지면
#:        정밀도가 좋아지는데 식에 그게 안 들어간다.
#:     ② He 코드의 `absolute_sigma=True` 는 **적합 잔차를 전혀 안 본다** — 점이 선에서
#:        2.5σ 벗어나도 ± 가 안 커진다(그들 `Fig. S5a` 실측).
#:     ③ D 의 표본분포는 **정규가 아니라 오른쪽 치우침**이다(그들 `Fig. S2` 실독).
#:   ⇒ **런 내부 오차의 정본은 블록 부트스트랩**이고 He 식은 **귀무모형**이다.
HE2018_A_RSD = 3.43          # RSD = A/√N_eff + B  (He 2018 식 9)
HE2018_B_RSD = 0.04          #   ⚠ B 는 Fig. 4a (N_eff ≤ 265) 적합의 **외삽**이다 —
                             #      그 논문에 RSD < 0.10 인 실측이 하나도 없다.
RSD_SYMMETRIC_MAX = 0.30     # 이보다 크면 대칭 ± 를 **출력하지 않는다** (아래 참조)


def he2018_neff(n_li, msd_max_a2, a=D_HOP_A):
    """He 2018 식 (8): `N_eff = n_Li · max(MSD) / a²`.

    ⛔⛔ **`max(MSD)` 는 궤적 전체 최대다 — 적합 창끝 값이 아니다.** 회신 BT 에서
    내가 정확히 그 둘을 헷갈렸다. `msd.json` 은 2026-09-22 부터 두 값을
    `msd_max_A2` / `msd_at_fit_window_end_A2` 로 **따로** 적는다.
    """
    if not n_li or msd_max_a2 is None or msd_max_a2 <= 0:
        return None
    return float(n_li) * float(msd_max_a2) / float(a) ** 2


def he2018_rsd(n_eff):
    """He 2018 식 (9). ⛔ **귀무모형이다** — 런 내부 오차의 정본이 아니다(위 주석)."""
    if not n_eff or n_eff <= 0:
        return None
    return HE2018_A_RSD / math.sqrt(n_eff) + HE2018_B_RSD


def lognormal_from_rsd(rsd):
    """RSD → 로그정규 파라미터. → dict(s, lo68, hi68, median_over_mean) (평균=1 단위).

    왜 로그정규인가: `he2018` `Fig. S2` 실독에서 D 표본분포가 **오른쪽으로 치우쳐**
    있었다(우/좌 꼬리 비 1.86 / 1.38, N_eff 커지면 감소, 최빈/평균이 예측과 정합).
    ⚠ **증명은 아니다** — 논문이 표본 수도 왜도도 안 준다. **방향은 확정, 분포형은
    '정합' 까지**다. 그래서 이 값은 **부트스트랩이 없을 때의 대용**이고, 있으면 그쪽이 이긴다.

    ⛔ 이 함수가 **못 하는 것**: 실제 분포가 감마·와이블이면 꼬리가 다르다. 구간을
    '정확' 하다고 읽지 마라 — **대칭 ± 보다 낫다** 까지다.
    """
    if not rsd or rsd <= 0:
        return None
    s = math.sqrt(math.log(1.0 + rsd ** 2))        # shape
    mu = -0.5 * s ** 2                              # 평균 1 이 되게
    return {"s": s,
            "lo68": math.exp(mu - s), "hi68": math.exp(mu + s),
            "median_over_mean": math.exp(mu)}


def _resample_D(A, t, m, starts, block, n_o, rng):
    """블록 재표본 **한 번** → D [cm²/s]. (`block_bootstrap_D` 와 3 온도 동시판이 **공유**한다)

    떼어 놓은 이유는 복제 방지다 — 같은 재표본 규약이 두 군데에 있으면 한쪽만 고쳐진다.
    """
    import numpy as _np
    n_blk = int(math.ceil(n_o / block))
    pick = rng.integers(0, len(starts), size=n_blk)
    idx = _np.concatenate([_np.arange(starts[k], min(starts[k] + block, n_o))
                           for k in pick])[:n_o]
    sl = _np.polyfit(t[m], A[idx].mean(axis=0)[m], 1)[0]
    return sl / 6.0 * 1e-4


def block_bootstrap_D(msd_per_origin, t_ps, lo, hi, block, n_boot=400, seed=0):
    """시간원점 **블록** 부트스트랩으로 런 내부 σ(D) 를 **실측**한다.

    `msd_per_origin` = (n_origin, n_lag) 배열 — 원점마다의 MSD(τ) 곡선.
    원점을 길이 `block` 의 **연속 덩이**로 잘라 복원추출하고, 덩이 평균 곡선을
    창 [lo, hi] 에서 다시 적합해 D 분포를 만든다.

    왜 블록인가: 이웃 원점은 **상관**돼 있다. 낱개로 뽑으면 상관을 무시해 σ 를
    과소평가한다. 덩이로 뽑으면 덩이 안 상관이 보존된다.

    ⛔ 이 함수가 **못 하는 것**
      · **`block` 을 스스로 못 정한다.** 상관시간에 걸리므로 **궤적을 보고** 정해야
        한다 — 회신 BT 에서 *"결과 전에 못 박는 항목"* 으로 명시했다. 호출자가 준다.
      · 분포형을 가정하지 않는 대신 **원점 수가 적으면 그대로 흔들린다.**
      · 시드 간(구조) 산포는 안 잰다 — 그건 시드 5 개의 IQR 이다. **직교하는 양**이다.
    """
    import numpy as _np
    A = _np.asarray(msd_per_origin, float)
    if A.ndim != 2 or A.shape[0] < 2:
        return None
    t = _np.asarray(t_ps, float)
    m = (t >= lo) & (t <= hi)
    if m.sum() < 3:
        return None
    n_o = A.shape[0]
    block = max(1, min(int(block), n_o))
    starts = _np.arange(0, n_o, block)
    rng = _np.random.default_rng(seed)
    Ds = [_resample_D(A, t, m, starts, block, n_o, rng) for _ in range(int(n_boot))]
    Ds = _np.asarray(Ds, float)
    mean = float(Ds.mean())
    return {"sigma_D": float(Ds.std(ddof=1)),
            "rsd": float(Ds.std(ddof=1) / abs(mean)) if mean else None,
            "lo68": float(_np.percentile(Ds, 15.865)),
            "hi68": float(_np.percentile(Ds, 84.135)),
            "median_over_mean": float(_np.median(Ds) / mean) if mean else None,
            "n_boot": int(n_boot), "block": block, "n_origin": n_o}


def _resample_beta(A, t, lo, hi, starts, block, n_o, rng):
    """블록 재표본 한 번 → β (창 [lo,hi] 의 log-log 기울기). `_resample_D` 와 같은 재표본 규약."""
    import numpy as _np
    n_blk = int(math.ceil(n_o / block))
    pick = rng.integers(0, len(starts), size=n_blk)
    idx = _np.concatenate([_np.arange(starts[k], min(starts[k] + block, n_o))
                           for k in pick])[:n_o]
    return loglog_slope(t, A[idx].mean(axis=0), lo, hi)


def block_bootstrap_beta(msd_per_origin, t_ps, lo, hi, block, n_boot=400, seed=0):
    """시간원점 **블록** 부트스트랩으로 **β** 의 런 내부 σ 를 실측한다 (회신 CC Q8-① · 2026-09-26).

    회신 CC: *"β 0.805 는 문턱에서 0.6 % 떨어져 있을 뿐 — 불확도가 없으면 통과가 아니라 반올림이다.
    시간원점 블록으로 β 의 오차를 내서 0.805 ± x 로 적고, 그 폭이 0.005 를 넘으면 '경계, 구분 불가' 로."*
    재표본 규약은 `block_bootstrap_D` 와 같고(덩이 복원추출 → 덩이 평균 곡선), 적합만 log-log 기울기다.

    ⛔ 이 함수가 **못 하는 것**
      · `block` 을 스스로 못 정한다 — plateau 규칙(`choose_block_plateau`)으로 호출자가 고른다.
      · 카드의 β* 가 **단일 원점(STO) 곡선**이면 이 σ 는 그 추정자의 σ 가 아니다 — 공통원점 행렬(MTO 추정자)의
        σ 다. 단일 원점의 산포는 원점 평균의 산포보다 **작지 않으므로**, 이 σ 는 STO β 불확도의 **하한**으로 읽는다.
      · 게이트를 판정하지 않는다 — 숫자(β̂ · σ · 68 % 구간)만 낸다.
    """
    import numpy as _np
    A = _np.asarray(msd_per_origin, float)
    if A.ndim != 2 or A.shape[0] < 2:
        return None
    t = _np.asarray(t_ps, float)
    if ((t >= lo) & (t <= hi)).sum() < 3:
        return None
    n_o = A.shape[0]
    block = max(1, min(int(block), n_o))
    starts = _np.arange(0, n_o, block)
    rng = _np.random.default_rng(seed)
    b_point = loglog_slope(t, A.mean(axis=0), lo, hi)
    bs = [_resample_beta(A, t, lo, hi, starts, block, n_o, rng) for _ in range(int(n_boot))]
    bs = _np.asarray([b for b in bs if b is not None], float)
    if len(bs) < 2 or b_point is None:
        return None
    return {"beta_matrix_mean": float(b_point), "sigma_beta": float(bs.std(ddof=1)),
            "lo68": float(_np.percentile(bs, 15.865)), "hi68": float(_np.percentile(bs, 84.135)),
            "median": float(_np.median(bs)), "n_boot_used": int(len(bs)), "n_boot": int(n_boot),
            "block": block, "n_origin": n_o, "window_ps": [float(lo), float(hi)]}


# ── 블록 길이 선택 · 3 온도 **동시** 부트스트랩 (회신 BU · 2026-09-22 합의) ───────
#: 회신 BU 에서 1저자와 합의해 **결과를 보기 전에** 박은 것 셋을 코드로 내린다.
#:   ① 블록 길이 `b` 를 고르는 **규칙** — σ(b) 가 plateau 에 드는 최소 b
#:   ② **세 온도를 한 번의 재표본에서 동시에** 뽑아 Ea 를 **직접** 적합
#:   ③ 아레니우스 `reduced χ²` 를 한 열로 기록 (dof = 1 — **약한 지표**)
#: ②가 핵심이다. 온도별 D 를 먼저 내고 ± 를 전파하면 그 단계에서 **대칭 가정**이
#: 슬그머니 들어온다 — D 표본분포는 오른쪽으로 치우쳐 있다(he2018 `Fig. S2` 실독).
#: 직접 적합은 그 우회를 없앤다.
KB_EV = 8.617333262e-5       # eV/K
BLOCK_PLATEAU_TOL = 0.05     # 연속 상대변화 문턱. ⚠ **우리가 정한 값**이다 —
                             #    회신 BU 에 "더 나은 기준이 있으면 그쪽을 따른다" 고 적었다.
BLOCK_PLATEAU_RUN = 3        # "연속 세 b"


def ea_from_lnD(temps_K, lnD):
    """무가중 아레니우스 적합. → (Ea_eV, lnD0, [잔차…])

    `ln D = ln D0 − Ea/(kT)` 를 `x = 1/(kT)` 직선으로 푼다 ⇒ 기울기 = −Ea.

    ⛔ **가중하지 않는다.** 가중하려면 σ(ln D) 가 있어야 하는데 그건 이 적합을 B 회
    반복해야 나온다(순환). 가중판이 필요하면 부트스트랩이 끝난 뒤 **밖에서** 한다.
    """
    n = len(temps_K)
    if n < 2 or len(lnD) != n:
        return None
    x = [1.0 / (KB_EV * float(T)) for T in temps_K]
    mx = sum(x) / n
    my = sum(lnD) / n
    sxx = sum((xi - mx) ** 2 for xi in x)
    if sxx <= 0:
        return None
    slope = sum((xi - mx) * (yi - my) for xi, yi in zip(x, lnD)) / sxx
    icpt = my - slope * mx
    resid = [yi - (icpt + slope * xi) for xi, yi in zip(x, lnD)]
    return -slope, icpt, resid


def reduced_chi2(resid, sigmas, n_par=2):
    """`χ²_red = Σ(r/σ)² / (n − n_par)`. → float 또는 None

    ⚠ **dof = 1 이다** (3 점 · 2 모수). 회신 BU: *"약한 지표"* — **거친 이상**(온도 역전
    같은 것)만 잡는다. 그래도 찍는 이유는 he2018 `Fig. S5a` 의 역전을 드러내는 것이
    정확히 이 열이기 때문이다.

    ⛔ 이 함수가 **못 하는 것**: σ 가 틀리면 χ²_red 도 같이 틀린다 — σ 의 타당성을
    검증하지 않는다. σ 는 **같은 부트스트랩**에서 온 값이어야 한다.
    """
    dof = len(resid) - int(n_par)
    if dof < 1 or len(sigmas) != len(resid):
        return None
    if any((s is None or s <= 0) for s in sigmas):
        return None
    return sum((r / s) ** 2 for r, s in zip(resid, sigmas)) / dof


def joint_ea_bootstrap(runs, lo, hi, block, n_boot=400, seed=0):
    """**세 온도를 한 재표본에서 동시에** 뽑아 Ea 를 직접 적합한다 (회신 BU 합의).

    `runs` = `[{"T_K": 600.0, "msd_per_origin": (n_o, n_lag), "t_ps": (n_lag,)}, …]`

    한 복제(replicate)에서 **온도마다 독립으로** 블록을 뽑아 D 를 셋 만들고, 그 자리에서
    3 점 아레니우스를 적합해 Ea 하나를 얻는다. 이걸 `n_boot` 회 반복해 **Ea 분포**를 낸다.

    온도 간 draw 가 독립인 근거: 드라이버가 온도마다 다른 RNG 를 쓴다
    (`disorder_ensemble_diffusion.py:427` — `seed = args.seed + 1000*ci + int(T)`).
    같은 시드 번호라는 것 외에 pairing 근거가 없다 (`arrhenius_compat.py` 초판이 틀린 지점).

    ⛔ 이 함수가 **못 하는 것**
      · `block` 을 **스스로 못 정한다** — `choose_block_plateau()` 로 먼저 고른다.
        그리고 고른 b 는 **전 시드·전 온도에 하나로 고정**해야 한다(R 의 분모가 섞인다).
      · 온도가 2 개면 Ea 는 나오지만 `χ²_red` 는 **못 낸다**(dof = 0) — None 으로 적는다.
      · 시드 간(구조) 산포는 안 잰다. 그건 `arrhenius_compat.py --vr` 의 분자다.
      · 궤적이 실제로 확산적인지 판정하지 않는다 — 앞 게이트(C1·plateau)가 할 일이다.
    """
    import numpy as _np
    if not runs or len(runs) < 2:
        return None
    temps, prep, point_lnD = [], [], []
    for r in runs:
        A = _np.asarray(r["msd_per_origin"], float)
        t = _np.asarray(r["t_ps"], float)
        if A.ndim != 2 or A.shape[0] < 2:
            return None
        m = (t >= lo) & (t <= hi)
        if m.sum() < 3:
            return None
        n_o = A.shape[0]
        b = max(1, min(int(block), n_o))
        #: 점추정은 **정본 MTO 곡선**(`mean_curve`)에서 낸다 — 부트스트랩 행렬은 공통
        #: 원점 집합이라 짧은 lag 의 원점 수가 정본보다 적다(아래 `msd_per_origin_from_traj`
        #: 의 "못 하는 것" 참조). σ 만 그 행렬에서 내고, **값은 정본이 이긴다.**
        base = _np.asarray(r["mean_curve"], float) if r.get("mean_curve") is not None \
            else A.mean(axis=0)
        if base.shape != t.shape:
            return None
        D0 = _np.polyfit(t[m], base[m], 1)[0] / 6.0 * 1e-4
        if D0 <= 0:
            return None
        temps.append(float(r["T_K"]))
        point_lnD.append(math.log(D0))
        prep.append((A, t, m, _np.arange(0, n_o, b), b, n_o))
    rng = _np.random.default_rng(seed)
    Ea_s, lnD_s = [], []
    for _ in range(int(n_boot)):
        row = []
        for (A, t, m, starts, b, n_o) in prep:
            D = _resample_D(A, t, m, starts, b, n_o, rng)
            if D <= 0:
                row = None
                break
            row.append(math.log(D))
        if row is None:
            continue
        fit = ea_from_lnD(temps, row)
        if fit is None:
            continue
        Ea_s.append(fit[0])
        lnD_s.append(row)
    if len(Ea_s) < 2:
        return None
    Ea_s = _np.asarray(Ea_s, float)
    L = _np.asarray(lnD_s, float)
    sig_lnD = [float(L[:, i].std(ddof=1)) for i in range(L.shape[1])]
    pfit = ea_from_lnD(temps, point_lnD)
    rc_point = reduced_chi2(pfit[2], sig_lnD) if pfit else None
    rc_boot = [reduced_chi2(ea_from_lnD(temps, list(row))[2], sig_lnD) for row in L]
    rc_boot = [v for v in rc_boot if v is not None]
    return {
        "Ea_eV": float(pfit[0]) if pfit else None,
        "Ea_boot_mean_eV": float(Ea_s.mean()),
        "Ea_boot_median_eV": float(_np.median(Ea_s)),
        "Ea_sigma_eV": float(Ea_s.std(ddof=1)),
        "Ea_lo68_eV": float(_np.percentile(Ea_s, 15.865)),
        "Ea_hi68_eV": float(_np.percentile(Ea_s, 84.135)),
        "temps_K": temps,
        "lnD_point": point_lnD,
        "sigma_lnD_by_T": sig_lnD,
        "red_chi2_point": rc_point,
        "red_chi2_boot_median": float(_np.median(rc_boot)) if rc_boot else None,
        "dof": len(temps) - 2,
        "red_chi2_note": ("dof = %d. ⚠ **약한 지표** — 거친 이상(온도 역전)만 잡는다."
                          % (len(temps) - 2)),
        "n_boot_used": int(len(Ea_s)), "n_boot_asked": int(n_boot),
        "block": int(block), "window_ps": [float(lo), float(hi)],
        "design": "세 온도 **동시 재표본 → Ea 직접 적합** (회신 BU). "
                  "온도별 D 를 먼저 내고 ± 를 전파하지 **않는다** (대칭 가정 유입 방지).",
    }


def block_sigma_curve(sigma_of_block, blocks):
    """블록 사다리마다 σ 를 재서 곡선으로. → `[(b, σ), …]` (σ 가 None 인 b 는 뺀다)

    `sigma_of_block(b) -> float|None` 를 받는다 — σ(D) 든 σ(Ea) 든 **같은 규칙**을 쓴다.
    회신 BU 의 규칙은 **σ(Ea)** 에 대한 것이다(그게 판정의 분모라서). σ(D) 는 진단용이다.
    """
    out = []
    for b in blocks:
        try:
            s = sigma_of_block(int(b))
        except Exception:
            s = None
        if s is not None and s > 0:
            out.append((int(b), float(s)))
    return out


def choose_block_plateau(curve, tol=BLOCK_PLATEAU_TOL, run=BLOCK_PLATEAU_RUN, n_boot=None):
    """σ(b) 곡선에서 **plateau 에 드는 최소 b** 를 고른다 (회신 BU · 결과 보기 전 확정).

    plateau 판정: **연속 `run` 개의 b** 에서 σ 의 **이웃 간 상대변화가 모두 ≤ `tol`**.
    (`run = 3` 이면 상대변화는 2 개다 — 회신 문구 *"연속 세 b"* 의 문자 그대로다.
     "3 개의 변화" 로 읽는 판도 가능해서 `run` 을 인자로 뒀다. 고른 판을 기록에 남긴다.)

    → `{"block": b|None, "sigma": σ|None, "curve": [...], "why": "...", "rule": {...}}`

    ⛔⛔ **plateau 가 없으면 b 를 고르지 않는다.** `block=None` 을 돌려주고 호출자는
    σ_within 을 *"못 구했다"* 로 적고 **판정을 보류**한다. 아무 b 나 골라 숫자를 만들지 않는다.

    ⛔⛔ **규칙이 성립하는 범위에 두 가지 가드가 있다 (2026-09-22 실측으로 찾았다).**
      ① **몬테카를로 바닥.** 부트스트랩 SD 자체의 MC 오차는 대략 `σ/√(2B)` 다.
         `tol` 이 그 바닥에 가까우면 **잡음이 규칙을 통과시킨다.** 합성 궤적 실측:
         같은 곡선에서 `B=150` 이면 `b=12`, `B=3000` 이면 `b=7` 을 골랐다 —
         **복제 수가 답을 바꿨다.** ⇒ `n_boot` 을 주면 `tol ≥ 3/√(2B)` 를 요구하고,
         모자라면 **고르지 않는다**(필요한 B 를 같이 알려 준다).
      ② **사다리 간격.** 상대변화는 이웃 b 의 **간격에 비례**한다. 성긴 사다리는 변화를
         부풀리고 촘촘한 사다리는 줄인다 — 천천히 오르기만 하는 곡선도 사다리를 촘촘히
         하면 언젠가 통과한다.

    ⭐ **개정 2026-09-22 — 판정량을 `b 당` 으로 정규화한다** (가드 ② 를 대체한다).

        rel_per_b = |σ(b_{j+1}) − σ(b_j)| / σ(b_j) / (b_{j+1} − b_j)

      ⇒ 문턱 `tol` 은 그대로 5 % 이고, 이제 **"b 1 칸당 5 %"** 를 뜻한다.
      **왜 이게 안전한가**: `Δb == 1` 이면 `rel_per_b == rel` 이라 **원 규칙과 수식이 같다.**
      합의한 규칙은 *"b 를 1 부터 키우며"* = 연속 정수이므로, **원 규칙이 맞게 돌던 경우의
      답은 하나도 안 바뀐다.** 성긴 사다리에서만 달라진다 — 거기가 원래 틀리던 자리다.
      종전 가드 ② 는 그 자리에서 **기권**했는데, 정규화하면 **판정할 수 있으므로**
      기권 대신 **`confirm_at_spacing_1` 주의**를 단다(국소 선형성 가정이 남아 있어서다).
      ⚠ 이건 **규칙 개정**이라 원장에 적는다 — 조용히 바꾸지 않는다.

      가드 ① 은 그대로다 — MC 바닥은 사다리 간격과 **무관한 별개 문제**다.

    ⛔ 이 함수가 **못 하는 것**: 곡선이 단조 증가만 하는 **원인**(상관시간이 창보다 긴가?)
    을 말하지 못한다. 못 골랐다는 사실만 말한다.
    """
    c = sorted(curve, key=lambda p: p[0])
    rule = {"tol": float(tol), "run": int(run),
            "definition": "연속 run 개 b 의 이웃 간 상대변화(**b 당 정규화**)가 모두 ≤ tol",
            "normalization": "rel_per_b = |Δσ|/σ/Δb  (개정 2026-09-22)",
            "equivalent_when": "Δb == 1 이면 원 규칙과 **수식이 동일**하다 — "
                               "연속 정수 사다리의 답은 안 바뀐다",
            "guards": ["MC 바닥 tol ≥ 3/√(2B)"]}
    base = {"block": None, "sigma": None, "curve": c, "rule": rule}
    if n_boot:
        floor = 1.0 / math.sqrt(2.0 * float(n_boot))
        rule["mc_floor"] = floor
        if tol < 3.0 * floor:
            need = int(math.ceil(0.5 * (3.0 / tol) ** 2))
            return {**base,
                    "why": f"복제가 모자란다 — σ 의 MC 오차 ≈ {floor:.3f} 이고 "
                           f"tol {tol} 은 그 3 배({3 * floor:.3f}) 미만이다. "
                           f"**잡음이 규칙을 통과시킨다.** B ≥ {need} 로 올리고 다시 재라. "
                           "b 를 고르지 않는다."}
    if len(c) < run:
        return {**base,
                "why": f"곡선의 점이 {len(c)} 개 — 연속 {run} 개를 볼 수 없다. "
                       "**b 를 고르지 않는다**(판정 보류)."}
    def _per_b(j):
        """이웃 한 쌍의 **b 당** 상대변화. Δb == 1 이면 원 규칙의 값과 같다."""
        db = c[j + 1][0] - c[j][0]
        if db <= 0:                       # b 가 중복이거나 거꾸로면 판정 불가
            return None
        return abs(c[j + 1][1] - c[j][1]) / c[j][1] / db

    for i in range(len(c) - run + 1):
        pers = [_per_b(j) for j in range(i, i + run - 1)]
        if any(p is None for p in pers):
            continue
        if not all(p <= tol for p in pers):
            continue
        gaps = [c[j + 1][0] - c[j][0] for j in range(i, i + run - 1)]
        rels = [abs(c[j + 1][1] - c[j][1]) / c[j][1] for j in range(i, i + run - 1)]
        out = {"block": c[i][0], "sigma": c[i][1], "curve": c, "rule": rule,
               "rel_per_b": pers, "rel_changes": rels, "gaps": gaps,
               "why": f"b = {c[i][0]} 부터 연속 {run} 점의 **b 당** 상대변화가 "
                      f"{max(pers):.3f} ≤ {tol} — plateau 최소 b."}
        if any(g != 1 for g in gaps):
            out["confirm_at_spacing_1"] = (
                f"사다리 간격이 {gaps} 다. b 당 정규화로 **판정은 했지만**, 정규화는 "
                f"그 구간에서 σ(b) 가 국소적으로 선형이라고 **가정**한다. "
                f"b = {c[i][0]} 부근을 **1 간격으로 다시 재서 확인해라.**")
            out["why"] += "  ⚠ 사다리가 성기다 — `confirm_at_spacing_1` 참조."
        return out
    cand = [p for p in (_per_b(j) for j in range(len(c) - 1)) if p is not None]
    if not cand:
        return {**base, "why": "b 사다리가 단조 증가가 아니다(중복·역순) — 판정 불가."}
    best = min(cand)
    return {**base,
            "why": f"plateau 없음 — 최선의 이웃 **b 당** 상대변화가 {best:.3f} > {tol}. "
                   "**b 를 고르지 않는다.** σ_within 은 '못 구했다' 로 적고 판정을 보류한다."}


def rsd_report(rec, block=None, boot=None):
    """한 런의 오차 열들을 만든다. → dict

    ⛔⛔ **RSD > RSD_SYMMETRIC_MAX 이면 대칭 `±` 를 내지 않는다.**
      회신 BT 검산: 평균=1 단위에서 대칭 2σ 가 RSD 0.5 에서 `[0.000, 2.000]`,
      0.9 에서 **`[−0.800, 2.800]` = 음수**가 된다. 확산계수에 음수 구간을 찍는 것은
      틀린 정도가 아니라 **말이 안 된다.** 그 구간은 로그정규/부트스트랩으로만 낸다.
    """
    n_li = rec.get("n_Li")
    msd_max = rec.get("msd_max_A2")
    if msd_max is None:                      # 2026-09-22 이전 기록 — 배열에서 되살린다
        y = rec.get("msd_Li_A2") or []
        msd_max = max(y) if y else None
    a = rec.get("site_distance_A", D_HOP_A)
    neff = he2018_neff(n_li, msd_max, a)
    rsd = he2018_rsd(neff)
    out = {"n_Li": n_li, "msd_max_A2": msd_max, "site_distance_A": a,
           "n_eff_he2018": neff, "rsd_he2018": rsd,
           "rsd_he2018_note": "귀무모형. ⛔ lag 창을 제한한 적합에 대해 **미검증**"
                              " (회신 BT §6-e). 런 내부 오차의 정본은 부트스트랩이다."}
    if rsd:
        ln = lognormal_from_rsd(rsd)
        out.update({"s_lognorm": ln["s"], "D_lo68_rel": ln["lo68"],
                    "D_hi68_rel": ln["hi68"], "median_over_mean": ln["median_over_mean"]})
        out["symmetric_pm_allowed"] = bool(rsd <= RSD_SYMMETRIC_MAX)
        if rsd > RSD_SYMMETRIC_MAX:
            out["symmetric_pm_blocked_why"] = (
                f"RSD {rsd:.3f} > {RSD_SYMMETRIC_MAX} — 대칭 ± 는 2σ 에서 음수로 간다. "
                "비대칭 구간(로그정규 또는 부트스트랩)만 쓴다.")
    out["sigma_boot"] = boot if boot else None
    if boot is None:
        out["sigma_boot_why"] = (
            "원점별 MSD 곡선이 없어 **못 구했다** (구했는데 0 이 아니다). "
            "`--from_traj` 로 궤적을 주면 잰다. block 은 상관시간에 걸리므로 호출자가 준다.")
    return out


def run_verdict(t, y, beta=None, windows=DINC_WINDOWS):
    """한 런의 판정. → (code, 사유들)  code ∈ {no_value, hold, citable}

    판정축 (회신 AK Q4·Q5):
      no_value — 궤적 무결성 실패 · 안정된 `D_inc` plateau 부재
      hold     — 실제 독립 hop 부족
      citable  — 위 둘 다 아님

    ⛔ **β 는 판정에 안 들어간다.** 경보로 기록만 한다 (kb/concepts/beta-gate.md §7-5).
    ⛔ 이 함수가 못 하는 것: 상·확산기전이 온도마다 섞였는지는 **한 런만 봐서 못 본다**
       (그건 Arrhenius 단계의 판정이다) · 프로토콜 일치도 여기서 안 본다.
    """
    why = []
    if not t or not y:
        return NO_VALUE, ["궤적 없음 — MSD 배열이 비었다"]
    pl = dinc_plateau(t, y, windows)
    if pl["status"] == "insufficient":
        return NO_VALUE, [f"D_inc 를 잰 창이 {pl['n']}개 — plateau 판정 불가 "
                          f"(최소 {DINC_MIN_WINDOWS}개)"]
    if pl["status"] == "drifting":
        why.append(f"D_inc 가 창 따라 움직인다 (상대산포 {pl['spread']:.0%} "
                   f"> {DINC_PLATEAU_TOL:.0%}, 추세 {pl['trend']:+.0%})")
        return NO_VALUE, why
    n_hop = hops_per_ion_msd(y)
    if n_hop is not None and n_hop < HOPS_MIN_PER_ION:
        return HOLD, [f"홉 {n_hop:.1f}/이온 < {HOPS_MIN_PER_ION} (유효 홉 f·n, 이벤트 수의 하한) — "
                      f"값은 있으나 정밀도 부족"]
    return CITABLE, [f"D_inc plateau (산포 {pl['spread']:.0%}) · 홉 "
                     + (f"{n_hop:.1f}/이온" if n_hop is not None else "—")]

# ── 집계 자격 (2026-09-13, 회신 BQ-6 P0-1·P0-2) ─────────────────────────────
#: 부창 선형성 — 2–50 ps 를 셋으로 나눠 각 기울기 / 전체 기울기 (v4 카드 규칙)
SUB_WINDOWS = ((2, 18), (18, 34), (34, 50))
SUB_RATIO_OK = (0.80, 1.20)
#: 선언한 변위 사건 수 하한 (런당). ⚠ '독립성이 입증된 사건' 이 아니라 **선언한 변위 사건**
#:   (|r_i(t) − r_i(t_ref)| > 2.5 Å 첫 발생 → 1, t_ref 갱신) 이다 — 시간원점 중복만 피한다.
EVENTS_MIN_PER_RUN = 50


def sub_window_ratios(t, y, lo=2.0, hi=50.0, subs=SUB_WINDOWS):
    """부창 기울기 / 전체창 기울기. 어느 창이든 못 맞추면 **None** (검사 불가 — 통과 아님)."""
    full = lin_fit(t, y, lo, hi)
    if full is None or abs(full[0]) < 1e-30:
        return None
    out = []
    for a, b in subs:
        f = lin_fit(t, y, a, b)
        if f is None:
            return None
        out.append(f[0] / full[0])
    return out


def aggregation_eligible(t, y, events_per_run, windows=DINC_WINDOWS,
                         subs=SUB_WINDOWS, ratio_ok=SUB_RATIO_OK, events_min=EVENTS_MIN_PER_RUN):
    """한 런이 **집계에 들어갈 자격**이 있는가 → (bool, 사유들, 세부). ⛔ `run_verdict` 의 CITABLE 하나를
    전체 통과로 승격하지 않는다 (회신 BQ-6 P0-2).

    자격 = ① `run_verdict` ≠ NO_VALUE (D_inc plateau)
        ∧ ② 부창 기울기 비 셋이 전부 [0.8, 1.2] (`sub_window_ratios`) — run_verdict 는 이걸 **안 본다**.
            리뷰어 합성 사례: D_inc 창 끝점만 지키고 중간을 흔들면 plateau 산포 0 · CITABLE 인데
            부창 비는 전부 기준 밖이었다.
        ∧ ③ 선언한 변위 사건 수 ≥ events_min — 호출자가 궤적에서 센 값을 **넘겨야** 한다.
            None 이면 '검사 불가' 이고 **통과가 아니다**.
    ⛔ `hops_per_ion_msd` (max MSD / d²) 는 **자격에 안 들어간다.** 그것은 MSD 규모의 운영 경보다 —
       절편만 27 Å² 올려도 1.1 → 4.1 로 바뀐다 (리뷰어 합성 사례 ①). 실제 홉·독립 표본수·정밀도의
       증거로 쓰지 않는다. 결과에는 `msd_magnitude_alarm` 으로만 남긴다.
    ⛔ 못 하는 것: 사건의 통계적 독립성을 보증하지 않는다 · 상·기전 혼합은 못 본다 · 평형 표집을 증명하지 않는다.
    """
    code, why = run_verdict(t, y, windows=windows)
    reasons, ok = list(why), True
    if code == NO_VALUE:
        ok = False
    ratios = sub_window_ratios(t, y, subs=subs)
    if ratios is None:
        ok = False
        reasons.append("부창 기울기 비 검사 불가 (창을 못 맞춤) — 통과 아님")
    else:
        bad = [f"{a}-{b}: {r:.3f}" for (a, b), r in zip(subs, ratios) if not (ratio_ok[0] <= r <= ratio_ok[1])]
        if bad:
            ok = False
            reasons.append("부창 기울기 비 기준 밖 " + ", ".join(bad) + f" (허용 {ratio_ok})")
    if events_per_run is None:
        ok = False
        reasons.append("선언한 변위 사건 수가 없다 — 검사 불가 (통과 아님)")
    elif events_per_run < events_min:
        ok = False
        reasons.append(f"선언한 변위 사건 {events_per_run} < {events_min}/런")
    n_hop = hops_per_ion_msd(y)
    return ok, reasons, {"run_verdict": code, "sub_window_ratios": ratios, "events_per_run": events_per_run,
                         "msd_magnitude_alarm": (n_hop is not None and n_hop < HOPS_MIN_PER_ION),
                         "msd_magnitude_value": n_hop,
                         "⛔": "msd_magnitude_* 는 경보다. 자격 판정에 쓰이지 않았다"}


def framework_alarm(json_path, save_fs=None):
    """골격 이동 **경보** — `framework_com_split` 의 얇은 껍질. → dict(state ∈ unavailable · framework_static · ok · alarm)

    ⛔ 범위 (회신 BQ-6 P1): 원소 수 < FRAMEWORK_MIN_N(8) 인 종은 판정 평균에서 **빠진다** (Al₂·O₃ 는 안 본다) ·
       첫 프레임 대비 마지막 프레임 MSD 다 (시간원점 평균·2–50 ps 창이 아니다) · 전역 COM 하나만 뺀다.
       전체 비-Li 연결성·이동을 인증하지 않는다. 결합 재배열을 확정하지 않는다.
    ⛔ `framework_com_split` 이 None 이면 **'경보 없음' 이 아니라 '검사 불가'(unavailable)** 다.
    """
    r = framework_com_split(json_path, save_fs=save_fs)
    if r is None:
        return {"state": "unavailable", "why": "궤적/분해 도구 없음 또는 판정 가능한 종(n≥8) 없음 — 검사 불가",
                "excluded_species_note": f"n < {FRAMEWORK_MIN_N} 인 종은 판정에서 빠진다 (예: Al₂·O₃)"}
    v = r.get("verdict")
    state = ("framework_static" if v == "framework_static" else
             "alarm" if v in ("rearrangement", "mixed") else "ok")
    return {"state": state, **r, "excluded_species_note": f"n < {FRAMEWORK_MIN_N} 인 종은 판정에서 빠진다 (예: Al₂·O₃)",
            "measure": "첫↔마지막 프레임 MSD (원자수 가중), 전역 COM 제거 — 시간원점 평균 아님"}


def loglog_slope(t, y, lo, hi):
    """[lo,hi] ps 구간의 log-log 기울기. 점이 3개 미만이면 None."""
    pts = [(math.log(a), math.log(b)) for a, b in zip(t, y)
           if lo <= a <= hi and a > 0 and b > 0]
    if len(pts) < 3:
        return None
    n = len(pts)
    sx = sum(p[0] for p in pts); sy = sum(p[1] for p in pts)
    sxx = sum(p[0] ** 2 for p in pts); sxy = sum(p[0] * p[1] for p in pts)
    den = n * sxx - sx * sx
    return (n * sxy - sx * sy) / den if abs(den) > 1e-30 else None


def _curve(d, mto=False, path=None, rebuild=False):
    """(t, y) 회수. --mto 면 msd_Li_A2_mto/times_ps_mto 를 쓴다.

    ⚠ MTO 가 없는 옛 런에서 조용히 STO 로 후퇴하지 않는다 — 어느 곡선을 본 것인지
      모르면 판정을 못 쓴다. 없으면 (None, None) 을 돌려 그 런을 건너뛰게 한다.
    """
    if mto:
        y = d.get("msd_Li_A2_mto")
        if not y and rebuild and path:
            # ⛔ 조용히 STO 로 후퇴하지 않는다 — **되살리기를 시도**하고, 실패하면
            #   여전히 (None, None) 이다. 어느 곡선을 봤는지 모르면 판정을 못 쓴다.
            got = mto_from_traj(path, d.get("save_fs") or d.get("dt_save_fs"))
            if got:
                d.update(got)
                y = d.get("msd_Li_A2_mto")
        return (d.get("times_ps_mto") or d.get("times_ps"), y) if y else (None, None)
    return d.get("times_ps"), d.get("msd_Li_A2")



# ── 골격(비-Li) MSD ───────────────────────────────────────────────────────
# 왜 (2026-08-19): Zhang npj 2026 이 **MACE-MP-0 이 LGPS 골격을 1050–1500 K 에서
#   인위적으로 녹인다**는 걸 잡고 샘플링 온도를 1050 K 로 낮췄다.
#   우리 아레니우스 상한 1000 K 가 **그 선 바로 아래**다 → 우리 궤적도 확인해야 한다.
#   골격이 녹으면 Li 의 "확산"은 확산이 아니라 **구조 붕괴**이고, 그 D·Ea 는 못 쓴다.
# 판정선: 골격 MSD 가 Li MSD 의 이 비율을 넘으면 의심. Li 가 케이지 안에서만 떨 때
#   골격도 같이 떠는 것은 정상이므로 **비**로 본다 (절대값은 온도에 따라 변한다).
#
# ⛔⛔ 2026-08-20 실측으로 **비(ratio) 단독 판정을 폐기했다.** 세 방향으로 다 틀렸다:
#   ① 놓침 — b2o3 T800 은 B 의 **β = 1.44**, T1000 은 O 의 **β = 0.91** 인데 비가 각각
#     0.092 / 0.084 로 문턱 0.10 아래여서 **"⭕ rigid" 로 통과**했다.
#   ② 헛경보 — b2o3 T400/T500 의 "⚠ mobile" 은 **분모 인공물**이다. 저온이라 Li MSD 가
#     7–22 Å² 로 작아 비가 자동으로 부푼다(골격 절대 MSD 는 온도에 둔한 진동값).
#   ③ ★ **표본 크기를 안 봤다** — 이게 제일 컸다. b2o3 는 `Li58B2P8S41Cl16O3` 라
#     **B 가 2개, O 가 3개**다. 2개짜리 평균에서 B 하나가 한 번 뛰면 MSD 가 계단이 되고
#     그 구간 로그기울기는 1 을 훌쩍 넘는다 — `kb/concepts/beta-gate.md` 의
#     "β>1.2 = 드리프트 **또는 단일 대형 사건**" 중 후자다. 실제로 '최악 원소' 로 뽑힌 게
#     계속 B·O 였고, modelc 에서 뽑힌 Cl·S 는 16·41개였다.
#     (COM 표류는 원인이 아니다 — ASE Langevin 은 `fixcm=True` 가 기본이고
#      `kb/reports/paper_first_author_requests_2026_08.md` 에서 이미 배제됐다.)
# ⇒ **β 가 1차 판별자**(진동이면 MSD 가 평평해 β≈0, 자리를 뜨면 β→1)이고,
#   **표본이 부족한 원소는 아예 판정에서 뺀다.** 비는 2차 정보로만 남긴다.
FRAMEWORK_BETA_RIGID = 0.30    # 이 아래 = 진동 (실측: modelc 5온도 −0.08~0.13)
FRAMEWORK_BETA_MELT = 0.60     # 이 위 = 확산/구조붕괴
FRAMEWORK_MIN_N = 8            # 이보다 적은 원소는 평균이 의미 없다 → 판정 제외(보고는 한다)
FRAMEWORK_WARN_RATIO = 0.10    # 2차 — β 가 애매할 때만 본다
FRAMEWORK_FAIL_RATIO = 0.25
LI = "Li"
# 종별 MSD 가 들어 있을 수 있는 자리 (런 세대마다 다르다)
ELEM_MSD_PATHS = (("msd_per_elem_A2",), ("msd_data", "msd_per_elem_A2"),
                  ("msd_A2_per_elem",), ("msd_data", "msd_A2_per_elem"))


def _elem_msd(d):
    """종별 MSD 딕셔너리 {원소: [MSD…]} 를 찾는다. 없으면 None.

    ⚠ **없을 때 조용히 빈 값을 돌려주지 않는다.** 호출자가 '골격이 안 녹았다'로
      오독하면 이 검사는 없는 것만 못하다 — 없으면 None 이고 그 런은 '판정 불가'다.
    """
    for path in ELEM_MSD_PATHS:
        cur = d
        for k in path:
            cur = cur.get(k) if isinstance(cur, dict) else None
            if cur is None:
                break
        if isinstance(cur, dict) and cur:
            return cur
    return None


def tau_int_geyer(series, d_origin_ps):
    """적분상관시간 `τ_int` 와 block 하한을 낸다 (Geyer initial-monotone 절단).

    **정의를 여기 한 곳에 못 박는다** (2026-08-27, 교차리뷰 H):

        g       = 1 + 2·Σ_k ρ(k)          (자기상관 합 — statistical inefficiency)
        τ_int   = (Δo / 2) · g            (Δo = 시간원점 간격 [ps])

    ⚠⚠ **이 정의에서 `2·τ_int` 는 이미 `g·Δo` 다.** 회신 H 원문:
        *"이 정의에서는 기존 식의 `2τ_int` 가 이미 `g·Δo` 다. factor 2 를 다시 곱하면 안 된다."*
      그래서 block 하한은 `max(t₂_max, g·Δo)` 이지 `max(t₂_max, 2·τ_int·2)` 가 아니다.
      이 함수가 **`block_min_ps` 를 직접 돌려주는 이유**가 그것이다 — 호출자가 2 를
      다시 곱할 여지를 없앤다.

    절단 (회신 H 권고 순서 2): Geyer **initial-positive + monotone** —
      인접 두 항의 합 `Γ_m = ρ(2m)+ρ(2m+1)` 이 양수인 동안만 더하고, 단조 감소하도록 깎는다.
      back-jump 의 **음의 자기상관** 때문에 signed 합이 작아질 수 있는데, 그때도
      기억 꼬리는 길 수 있으므로 `memory_horizon_ps`(ρ 가 마지막으로 |ρ|>0.05 인 lag)를
      **같이** 돌려준다. 회신 H: *"실제 block 하한은 2τ_int 하나보다 ACF 의 memory horizon
      과 SE plateau 를 같이 봐야 한다."*

    ⛔ 이 함수가 못 하는 것:
      · **SE plateau 검사를 대신하지 않는다.** block 크기를 b·1.5b·2b 로 바꿔가며 SE 가
        평평해지는지는 호출자가 따로 봐야 한다.
      · 시드 경계를 넘어 이어붙이면 안 된다 — **시드마다 따로** 부르는 것이 전제다.
      · 표본이 짧으면 τ 가 과소평가된다. `n_eff` 를 같이 보고 8–10 미만이면 쓰지 말 것.
    """
    n = len(series)
    if n < 16:
        return None
    mean = sum(series) / n
    dev = [x - mean for x in series]
    var = sum(d * d for d in dev) / n
    if var <= 0:
        return None

    def rho(k):
        return sum(dev[i] * dev[i + k] for i in range(n - k)) / ((n - k) * var)

    # Geyer initial-positive: Γ_m = ρ(2m)+ρ(2m+1) 이 양수인 동안
    gammas, m = [], 0
    while 2 * m + 1 < n - 1:
        G = rho(2 * m) + rho(2 * m + 1)
        if m > 0 and G <= 0:
            break
        gammas.append(G)
        m += 1
        if m > n // 4:
            break
    if not gammas:
        return None
    # initial-monotone: 단조 비증가로 깎는다
    for i in range(1, len(gammas)):
        gammas[i] = min(gammas[i], gammas[i - 1])
    g = 2.0 * sum(gammas) - rho(0)          # = 1 + 2Σρ(k)  (ρ(0)=1)
    g = max(g, 1.0)                          # 반상관이 심해도 1 미만으로 내리지 않는다
    horizon = 0
    for k in range(1, min(n - 1, n // 2)):
        if abs(rho(k)) > 0.05:
            horizon = k
    return {
        "g": g,
        "tau_int_ps": (d_origin_ps / 2.0) * g,
        "block_min_ps": g * d_origin_ps,     # ★ = 2·τ_int. 호출자가 2 를 또 곱하지 말 것
        "memory_horizon_ps": horizon * d_origin_ps,
        "n_origin": n,
        "n_eff": n / g,
    }


def cell_axis_info(cell):
    """셀에서 **수직폭·종횡비·비직교성**을 낸다. `(widths, aspect, max_offdiag, angles_deg)`.

    ⚠ 수직폭은 `|a|` 가 아니라 **`V/|b×c|`** 다 — 유한크기를 정하는 것은 그쪽이다.
      실측(lpsocl V0): `|c| = 35.17 Å` 인데 수직폭은 28.83 Å.
    """
    import numpy as _np
    C = _np.asarray(cell, dtype=float)
    V = abs(_np.linalg.det(C))
    if V <= 0:
        return None
    w = [V / _np.linalg.norm(_np.cross(C[(k + 1) % 3], C[(k + 2) % 3])) for k in range(3)]
    off = max(abs(C[i][j]) for i in range(3) for j in range(3) if i != j)
    ang = []
    for i, j in ((0, 1), (0, 2), (1, 2)):
        cs = float(_np.dot(C[i], C[j]) / (_np.linalg.norm(C[i]) * _np.linalg.norm(C[j])))
        ang.append(_np.degrees(_np.arccos(max(-1.0, min(1.0, cs)))))
    return w, max(w) / min(w), off, ang


def directional_msd_tensor(traj_path, save_fs=100.0, species="Li",
                           prefix_ps=None, max_lag_frac=0.5, n_origin=200,
                           basis="cartesian"):
    """`traj.xyz` 에서 **확산텐서** `M_αβ(t) = ⟨Δr_α Δr_β⟩` 를 낸다 (다중 시간원점).

    왜 (2026-08-27, 교차리뷰 G/H): 우리 3×3×1 은 **이방 복제**라 scalar `L` 도 `m/6` 도
      자동으로 정당화되지 않는다. *"수송이 등방인지 방향별 MSD 로 먼저 확인해야 한다."*
      ⚠ 회신 H 정정: 이방계에서도 총 MSD 기울기 `m/6` 은 **수학적으로 `Tr(D)/3`** 이다.
        틀린 계산이 아니라 **"등방 D" 가 아니라 trace-average 라고 불러야** 하는 문제다.

    반환 `(t_ps, M)` — `M[a][b]` 가 각각 길이 len(t_ps) 인 리스트.
      `D_αβ = ½ · dM_αβ/dt`  (성분당 1차원이므로 **분모가 6 이 아니라 2** 다)

    ⛔ 이 함수가 못 하는 것:
      · **unwrap 을 하지 않는다.** wrap 된 궤적은 **거부**한다(한 프레임 최대 변위가
        셀 최소폭의 절반을 넘으면 None + 이유 출력). 실측 계기: kgy `EN_0717/licube` 가
        D = 3×10⁶ Å²/ps 를 냈다 — 실제 Li(~0.1)의 **10⁷ 배**. 눈에 띄어서 잡혔지만
        일부만 접힌 궤적은 **그럴듯한 숫자로 통과**하므로 도구가 막아야 한다.
      · **골격 drift 를 제거하지 않는다** — 호출자가 `framework_com_split()` 등으로 먼저
        보정해야 한다. Langevin `fixcm=True` 라 전체 CoM 은 고정이지만 **골격 기준**
        drift 는 따로다.
      · 오차막대를 안 준다. block/seed bootstrap 은 별도다 (τ_int 가 필요).
      · 비직교 셀에서 결정축 회전을 안 한다 — Cartesian 성분 그대로다.
        회신 H: *"비직교 셀이면 fractional 성분을 그대로 쓰지 말고 orthonormal Cartesian
        텐서를 계산한 뒤 결정축으로 회전해야 한다."* 우리 셀이 직교인지 호출자가 확인할 것.
    """
    try:
        import numpy as _np
        from ase.io import read as _read
    except ImportError as e:
        print(f"   ⛔ {type(e).__name__}: {e} — `conda activate uma` 필요")
        return None
    tp = pathlib.Path(traj_path)
    if not tp.exists():
        return None
    frames = _read(str(tp), ":")
    if not frames:
        return None
    dt = save_fs / 1000.0                                   # ps
    if prefix_ps:                                           # 누적 prefix 분석 (회신 G 권고 ①)
        keep = int(prefix_ps / dt) + 1
        # ⛔⛔ 2026-08-29 (회신 S) — **파이썬 슬라이스가 조용히 잘렸다.** `frames[:keep]` 은
        #   keep 이 프레임 수보다 커도 에러 없이 **전체**를 돌려준다. 그래서 60 ps 궤적에
        #   `--prefixes 70,150,200,400,800` 을 주면 60 ps 값 하나가 **다섯 개의 다른 라벨로**
        #   찍혔다 (실측 kgy `lpsocl_md/licube`: 0.0704/0.0733/0.0388 이 5행 전부 동일).
        #   같은 숫자가 반복되는 것이 유일한 단서였고, 그건 우연히 눈에 띈 것이지 검사가 아니다.
        #   ⇒ 요청한 prefix 를 궤적이 못 덮으면 **숫자를 내지 않는다.**
        if keep > len(frames):
            return {"__short__": (len(frames) - 1) * dt, "__requested__": float(prefix_ps)}
        frames = frames[:keep]
        if len(frames) < 20:
            return None
    idx = [i for i, s in enumerate(frames[0].get_chemical_symbols()) if s == species]
    if not idx:
        return None
    pos = _np.array([f.get_positions()[idx] for f in frames])   # (nframe, nion, 3)
    nf = len(pos)

    # ⛔⛔ 2026-08-27 — **wrap 된 궤적을 잡는다.** 실측(kgy `EN_0717/licube`):
    #   D 가 3×10⁶ Å²/ps 로 나왔다. 실제 Li 는 ~0.1 이라 **10⁷ 배**다. 확산이 아니라
    #   좌표가 주기상자로 접혀서 원자가 매 프레임 상자를 가로지른 것으로 읽힌 것이다.
    #   저 값은 커서 눈에 띄었지만, 일부만 접힌 궤적은 **그럴듯한 숫자로 통과**한다.
    #   → 한 프레임 최대 변위를 셀 최소폭의 절반과 비교한다. 넘으면 물리가 아니다.
    try:
        cell = _np.array(frames[0].get_cell())
        vol = abs(_np.linalg.det(cell))
        widths = [vol / _np.linalg.norm(_np.cross(cell[(k + 1) % 3], cell[(k + 2) % 3]))
                  for k in range(3)] if vol > 0 else []
        half_min = 0.5 * min(widths) if widths else None
    except Exception:
        half_min = None
    if half_min and nf > 1:
        step_max = float(_np.abs(_np.diff(pos, axis=0)).max())
        if step_max > half_min:
            print(f"   ⛔ **{tp.parent.name}: 좌표가 wrap 돼 있다** — 한 프레임 최대 변위 "
                  f"{step_max:.1f} Å > 셀 최소폭의 절반 {half_min:.1f} Å.\n"
                  f"      MSD 를 이 좌표로 재면 확산이 아니라 **상자 가로지르기**를 잰다. "
                  f"unwrap 한 궤적이 필요하다 — 여기서 숫자를 내지 않는다.")
            return None
    max_lag = max(3, int(nf * max_lag_frac))
    # 시간원점을 균등 추출 — 전부 쓰면 O(nf²) 라 800 ps 에서 느리다
    origins = _np.unique(_np.linspace(0, nf - max_lag - 1,
                                      min(n_origin, nf - max_lag), dtype=int))
    if len(origins) < 2:
        return None
    # ⛔⛔ 2026-08-27 — **결정축 투영.** 교차리뷰 G 가 요구한 것이고, 없으면 판독이 안 된다:
    #   *"비직교 셀이면 fractional 성분을 그대로 쓰지 말고 orthonormal Cartesian 텐서를
    #     계산한 뒤 결정축으로 회전해야 한다."*
    #   실측 계기: lpsocl V0 의 비대각이 **3.48 Å** 라 Cartesian z 가 결정축 c 가 아니다.
    #   그런데 우리가 `Dzz` 를 "복제 안 한 c 축" 으로 읽었다 — **근거 없는 독해**였다.
    #   ⚠ 비직교 셀에서 â·b̂·ĉ 는 서로 직교하지 않으므로 이 성분들은 **적절한 텐서 분해가
    #     아니다.** "a 방향으로의 평균제곱변위" 라는 뜻이고, 그게 복제 방향과 짝지어 볼 때
    #     필요한 것이다. 각도를 같이 찍어 얼마나 기울었는지 보이게 한다.
    #   ⚠⚠ **왜 â·b̂·ĉ 가 아니라 역격자 방향인가** (2026-08-27, 설계 결정):
    #     비직교에서 `Δr·â` 는 공변 성분이고 `â` 로 전개한 반변 계수와 **다른 양**이다.
    #     둘 다 정의는 되지만, **유한크기가 제약하는 것은 셀 벽까지의 수직 거리**이고
    #     그 방향은 `b×c` (수직폭 `V/|b×c|` 와 짝) 다. 그래서 정규화한 **역격자 방향**
    #     `b̂×c`, `ĉ×a`, `â×b` 로 투영한다 — 각 성분이 자기 수직폭과 정확히 짝지어진다.
    #     (직교 셀에서는 셋이 x·y·z 와 같아지므로 기존 결과와 어긋나지 않는다.)
    P = None
    if basis == "crystal":
        try:
            C = _np.array(frames[0].get_cell(), dtype=float)
            rec = _np.array([_np.cross(C[(k + 1) % 3], C[(k + 2) % 3]) for k in range(3)])
            P = _np.array([r / _np.linalg.norm(r) for r in rec])
        except Exception:
            print("   ⚠ 셀을 못 읽어 결정축 투영을 건너뛴다 — Cartesian 으로 낸다")
            P = None

    lags = _np.arange(1, max_lag)
    M = _np.zeros((3, 3, len(lags)))
    for k, L in enumerate(lags):
        d = pos[origins + L] - pos[origins]                 # (norig, nion, 3)
        d = d.reshape(-1, 3)
        if P is not None:
            d = d @ P.T                                     # 결정축 방향 성분
        M[:, :, k] = (d[:, :, None] * d[:, None, :]).mean(axis=0)
    return (lags * dt).tolist(), [[M[a][b].tolist() for b in range(3)] for a in range(3)]


def cmd_directional(a):
    """`--directional` — 확산텐서와 누적 prefix 표. 형상 비교(2×2×2 vs 3×3×1)의 도구다.

    ⛔ 못 하는 것: 두 런을 **자동으로 판정하지 않는다.** 숫자를 나란히 놓을 뿐이고,
      허용폭 안인지 밖인지는 사람이 사전 등록한 기준으로 정한다 (회신 H: p-value 아닌
      사전 허용폭). 오차막대도 없다 — block/seed bootstrap 은 τ_int 확정 후.
    """
    import glob as _g
    pre = [float(x) for x in a.prefixes.split(",") if x.strip()] or [None]
    paths = sorted(_g.glob(os.path.expanduser(a.glob)))
    if not paths:
        print(f"⛔ glob 이 아무것도 못 잡았다: {a.glob}")
        return 2
    print("방향별 확산텐서 — D_αβ = ½·dM_αβ/dt  (성분당 1차원이라 분모가 **2**)")
    print("⚠ 이방계에서도 총 MSD 기울기 m/6 은 Tr(D)/3 이다 — 'trace-average' 이지 "
          "'등방 D' 가 아니다 (회신 H 정정).")
    _cry = getattr(a, "crystal_axes", False)
    if _cry:
        print("★ **결정축 투영** (â·b̂·ĉ) — 열 이름 Dxx/Dyy/Dzz 를 **Daa/Dbb/Dcc 로 읽는다**")
        print("  ⚠ 비직교 셀에서 â·b̂·ĉ 는 서로 직교하지 않는다 — 적절한 텐서 분해가 아니라 "
              "'그 방향으로의 평균제곱변위' 다. 아래 셀 줄의 각도를 같이 볼 것.")
    print(f"{'case':30s} {'prefix':>8s} {'Dxx':>9s} {'Dyy':>9s} {'Dzz':>9s} "
          f"{'Tr/3':>9s} {'이방비':>7s}  비대각 최대")
    n_done = 0
    for p in paths:
        d = pathlib.Path(p)
        traj = d / "traj.xyz" if d.is_dir() else d.parent / "traj.xyz"
        if not traj.exists():
            print(f"{str(d)[-30:]:30s} {'—':>8s}  ⛔ traj.xyz 없음")
            continue
        sf = 100.0
        mj = traj.parent / "msd.json"
        if mj.exists():
            try:
                sf = json.load(open(mj)).get("save_fs") or 100.0
            except Exception:
                pass
        # ★ 셀 정보를 먼저 찍는다 — 어느 축이 짧고 어디를 복제했는지 화면에서 보여야
        #   `Dcc 가 낮다` 를 "복제 안 한 축" 과 짝지을 수 있다. 2026-08-27 에 우리가
        #   **c 를 짧은 축으로 착각**했다 (실제로는 수직폭 28.83 Å 로 제일 긴 축이었다).
        try:
            from ase.io import read as _rd
            _ci = cell_axis_info(_rd(str(traj), "0").get_cell())
            if _ci:
                _w, _asp, _off, _ang = _ci
                print(f"   셀 수직폭 a/b/c = {_w[0]:.2f}/{_w[1]:.2f}/{_w[2]:.2f} Å · "
                      f"최소 {min(_w):.2f} · **종횡비 {_asp:.2f}** · "
                      f"각도 {_ang[0]:.1f}/{_ang[1]:.1f}/{_ang[2]:.1f}° · "
                      f"비대각 {_off:.2f} Å"
                      + ("" if _off < 1e-6 else "  ⚠ **비직교** — Cartesian 축이 결정축이 아니다"))
        except Exception:
            pass
        for pp in pre:
            got = directional_msd_tensor(traj, save_fs=sf, prefix_ps=pp,
                                         basis="crystal" if _cry else "cartesian")
            if got is None:
                print(f"{str(traj.parent)[-30:]:30s} {(pp or 'all'):>8} "
                      f" ⛔ 프레임 부족 — 이 prefix 는 아직 못 잰다")
                continue
            if isinstance(got, dict) and "__short__" in got:
                # 회신 S — 요청 prefix 를 궤적이 못 덮는다. 잘린 값을 그 라벨로 내보내면
                # 서로 다른 prefix 행이 **같은 숫자**가 되고 그게 측정처럼 읽힌다.
                print(f"{str(traj.parent)[-30:]:30s} {(pp or 'all'):>8} "
                      f" ⛔ 궤적이 {got['__short__']:.1f} ps 뿐 — prefix "
                      f"{got['__requested__']:.0f} ps 를 못 덮는다 (잘린 값을 내지 않는다)")
                continue
            t, M = got
            lo, hi = a.window
            sel = [i for i, x in enumerate(t) if lo <= x <= hi]
            if len(sel) < 3:
                print(f"{str(traj.parent)[-30:]:30s} {(pp or 'all'):>8} "
                      f" ⛔ 창 {lo}-{hi} 에 점이 3개 미만")
                continue
            def _slope(series):
                xs = [t[i] for i in sel]; ys = [series[i] for i in sel]
                n = len(xs); sx = sum(xs); sy = sum(ys)
                sxx = sum(x * x for x in xs); sxy = sum(x * y for x, y in zip(xs, ys))
                den = n * sxx - sx * sx
                return (n * sxy - sx * sy) / den / 2.0 if abs(den) > 1e-30 else float("nan")
            Dd = [_slope(M[k][k]) for k in range(3)]
            off = max(abs(_slope(M[i][j])) for i, j in ((0, 1), (0, 2), (1, 2)))
            tr = sum(Dd) / 3.0
            aniso = max(Dd) / min(Dd) if min(Dd) > 0 else float("nan")
            print(f"{str(traj.parent)[-30:]:30s} {(pp or 'all'):>8} "
                  f"{Dd[0]:9.4f} {Dd[1]:9.4f} {Dd[2]:9.4f} {tr:9.4f} {aniso:7.2f}  {off:.4f}")
            n_done += 1
    if not n_done:
        print("⛔ **아무것도 재지 못했다** — 통과가 아니다.")
        return 3
    print()
    print("  판독: `이방비` = max/min 대각성분. 1 에 가까우면 등방이다.")
    print("  ⚠ 비대각이 0 과 양립하는지 봐야 한다 — 크면 결정축이 Cartesian 과 안 맞는 것이다.")
    print("  ⛔ 두 셀을 비교할 때는 **같은 물리 방향끼리** 본다. 그리고 x·y 를 늘린 뒤")
    print("     Dzz 가 변하는 것은 오류가 아니라 **방향 간 동역학 결합**의 정보다 (회신 H).")
    return 0


def resolve_save_fs(json_path, save_fs=None):
    """프레임 간격을 정한다 → (값, 가정했나, 출처문구).

    ⛔⛔ 2026-09-10 — 종전엔 호출자가 안 주면 **곧바로 100 fs 를 가정**했다.
      그런데 드라이버(disorder_ensemble_diffusion.py:264)가 `msd.json` **옆에**
      `aimd_results.json` 을 쓰고 거기에 `save_fs` 가 들어 있다. 답이 같은 폴더에
      있는데 가정한 것이다.
      이게 왜 중요한가: 시간축이 바뀌면 창 2–50 ps 가 **다른 프레임 구간**을
      집으므로 β 가 달라진다 (일정 배율이라 기울기가 불변인 게 아니다 — 창이
      프레임을 고른다). b2o3 셀확장 카드(2026-09-07)의 §무효조건에
      *"save_fs 가정과 실행 인자가 어긋난다"* 가 명시돼 있어, 가정으로 낸 β 는
      그 조항에 걸린다.

    이 함수가 못 하는 것: sidecar 가 **실행 인자와 일치하는지**는 확인 못 한다.
      드라이버가 쓴 값을 그대로 믿는다 (드라이버가 argparse 값을 그대로 쓴다).
    """
    if save_fs is not None:
        return float(save_fs), False, "호출자 지정"
    side = pathlib.Path(json_path).parent / "aimd_results.json"
    if side.exists():
        try:
            got = json.load(open(side)).get("save_fs")
        except (OSError, ValueError):
            got = None
        if got:
            return float(got), False, f"{side.name}"
    return 100.0, True, None


def elem_msd_from_traj(json_path, save_fs=None, cache=True):
    """`msd.json` 옆의 `traj.xyz` 에서 **종별 MSD 를 다시 계산**한다. 없으면 None.

    왜 (2026-08-20 실측): 캠페인이 쓰는 `msd.json` 은 **Li 만** 저장한다. 31런을 검사했더니
    31런 전부 종별 MSD 가 없었고, `aimd_results.json` 은 94 바이트짜리 빈 파일이었다.
    그런데 `--save_traj` 로 남긴 `traj.xyz` 가 10런에 살아 있다 — 거기서 뽑으면 **재계산 0**이다.

    산식은 `tools/modelc_v3/aimd_mlip.py:compute_msd_per_element` 를 **그대로 빌려 쓴다**
    (복사하면 규약이 갈라진다 — convention_check 대상).

    ⚠ 시간축은 `save_fs`(프레임 간격) 가 정해준다. json 에 있으면 그걸 쓰고, 없으면
      **캠페인 기본 100 fs 를 가정하고 그 사실을 찍는다** — 조용히 가정하지 않는다.
    """
    import importlib.util
    jp = pathlib.Path(json_path)
    traj = jp.parent / "traj.xyz"
    if not traj.exists():
        print(f"   · {jp.parent.name}: traj.xyz 가 없다 — 골격 검사 원리적 불가")
        return None
    save_fs, assumed, sf_src = resolve_save_fs(jp, save_fs)
    src = pathlib.Path(__file__).resolve().parents[1] / "modelc_v3" / "aimd_mlip.py"
    if not src.exists():
        print(f"   ⛔ {src} 가 없다 — 산식을 빌려올 곳이 없다")
        return None
    spec = importlib.util.spec_from_file_location("_aimd", src)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except BaseException as e:
        # ⛔ 여기서 조용히 None 을 돌려주면 화면에는 "종별 MSD 없음" 으로만 보인다.
        #   실제 원인은 대개 **환경**이다 — ase 가 이 conda 환경에 없는 것.
        #   kgy (base) 에서 실측(2026-08-26): traj.xyz 가 14 MB 로 멀쩡히 있는데
        #   10/10 이 "종별 MSD 없음" 으로 떨어졌고 이유가 어디에도 안 나왔다.
        print(f"   ⛔ aimd_mlip 을 못 읽었다: {type(e).__name__}: {e}")
        if isinstance(e, (ImportError, ModuleNotFoundError)):
            print(f"      → 환경 문제다. `conda activate uma` 로 ase 가 있는 환경에서 다시.")
        return None
    print(f"   … {traj.parent.name}/traj.xyz 에서 종별 MSD 계산"
          + (f" (save_fs={save_fs:g} fs **가정** — 옆에 aimd_results.json 이 없거나"
             f" 그 안에 save_fs 가 없다. 카드 무효조건 대상이다)"
             if assumed else f" (save_fs={save_fs:g} fs · {sf_src})"))
    try:
        out = mod.compute_msd_per_element(traj, dt_save_fs=save_fs)
    except BaseException as e:
        print(f"   ⚠ 실패: {type(e).__name__} {e}")
        return None
    if cache:
        # 118 MB 를 매번 다시 읽지 않도록 json 에 되써 둔다 (다음 실행은 즉시)
        try:
            d = json.load(open(jp))
            d["msd_per_elem_A2"] = out["msd_per_elem_A2"]
            d["n_atoms_per_elem"] = out.get("n_atoms_per_elem", {})
            d.setdefault("times_ps", out["times_ps"])
            d["_elem_msd_source"] = (f"recomputed from traj.xyz (save_fs={save_fs:g} fs, "
                                     f"{'ASSUMED' if assumed else sf_src})")
            json.dump(d, open(jp, "w"))
            print(f"   … {jp.name} 에 저장 (다음부터는 즉시)")
        except (OSError, ValueError) as e:
            print(f"   ⚠ 되쓰기 실패({type(e).__name__}) — 이번만 쓰고 버린다")
    return out


def mto_from_traj(json_path, save_fs=None, cache=True):
    """`msd.json` 옆의 `traj.xyz` 에서 **MTO 곡선을 다시 만든다.** 없으면 None.

    왜 (2026-08-25): 700/900 K 신규 21런은 `times_ps_mto`/`msd_Li_A2_mto` 가 없다
      (그 캠페인이 MTO 저장 전에 돌았다). 그래서 `--mto` 판정이 21/36 에서 막혔고,
      **세 계 공통 온도 집합**을 못 정해 1저자 요청 1·2 가 통째로 멈춰 있다.
      단일 시간원점(STO) 은 27 Li × 1 원점이라 빠른 채널을 잡은 몇 이온이 곡선을
      지배한다 — 그게 MTO 와 STO 가 순위를 뒤집은 원인이다(2026-08-25 실측).
      궤적이 남아 있으면 **MD 재계산 0** 으로 되살릴 수 있다.

    산식은 `tools/modelc_v3/disorder_ensemble_diffusion.py:msd_multi_origin` 을
    **그대로 빌려 쓴다** — 복사하면 규약이 갈라진다(convention_check 대상).

    ⚠ 시간축은 `save_fs`(프레임 간격)가 정한다. json 에 있으면 그걸 쓰고 없으면
      캠페인 기본 100 fs 를 **가정하고 그 사실을 찍는다** — 조용히 가정하지 않는다.
    ⛔ 이 함수가 못 하는 것: 궤적이 없는 런은 **원리적으로 복구 불가**다(새로 돌려야 한다).
      그리고 MTO 를 만든다고 β 가 좋아진다는 보장은 없다 — 추정자를 바꾸는 것뿐이다.
    """
    import importlib.util
    jp = pathlib.Path(json_path)
    traj = jp.parent / "traj.xyz"
    if not traj.exists():
        return None
    assumed = save_fs is None
    if assumed:
        save_fs = 100.0
    src = pathlib.Path(__file__).resolve().parents[1] / "modelc_v3" / "disorder_ensemble_diffusion.py"
    if not src.exists():
        return None
    spec = importlib.util.spec_from_file_location("_ded", src)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except BaseException:
        return None
    try:
        frames = _ase_read(traj, ":")
    except BaseException as e:
        print(f"   ⚠ traj 읽기 실패: {type(e).__name__} {e}")
        return None
    if not frames or len(frames) < 8:
        return None
    import numpy as _np
    sym = frames[0].get_chemical_symbols()
    li = [i for i, s in enumerate(sym) if s == "Li"]
    if not li:
        print("   ⚠ traj 에 Li 가 없다")
        return None
    cart = _np.array([f.get_positions() for f in frames])
    print(f"   … {traj.parent.name}/traj.xyz 에서 MTO 재생성 "
          f"({len(frames)} 프레임 · Li {len(li)}"
          + (f" · save_fs={save_fs:g} fs **가정**)" if assumed else f" · save_fs={save_fs:g} fs)"))
    try:
        tau, msd_mto, norig = mod.msd_multi_origin(cart[:, li], save_fs / 1000.0)
    except BaseException as e:
        print(f"   ⚠ 실패: {type(e).__name__} {e}")
        return None
    if not msd_mto:
        return None
    out = {"times_ps_mto": list(tau), "msd_Li_A2_mto": list(msd_mto),
           "n_origins_mto": list(norig)}
    if cache:
        try:
            d = json.load(open(jp))
            d.update(out)
            d["_mto_source"] = (f"recomputed from traj.xyz (save_fs={save_fs:g} fs"
                                + (", ASSUMED" if assumed else "") + ")")
            json.dump(d, open(jp, "w"))
            print(f"   … {jp.name} 에 저장 (다음부터는 즉시)")
        except (OSError, ValueError) as e:
            print(f"   ⚠ 되쓰기 실패({type(e).__name__}) — 이번만 쓰고 버린다")
    return out


def msd_per_origin_from_traj(json_path, save_fs=None, n_lag=150):
    """`traj.xyz` 에서 **원점별** MSD 곡선 행렬을 만든다 → 블록 부트스트랩의 입력.

    → `{"t_ps": (n_lag,), "msd_per_origin": (n_origin, n_lag), "n_origin": …,
        "lag_max": …, "save_fs": …, "save_fs_assumed": bool}`  또는 None

    **왜 필요한가.** `block_bootstrap_D`/`joint_ea_bootstrap` 이 재표본하는 단위는
    *시간 원점*인데, 정본 MTO 경로(`msd_multi_origin`)는 원점을 **이미 평균해서** 준다.
    그래서 2026-09-22 까지 부트스트랩은 **입력 생산자가 없는 선언**이었다 — 이 함수가
    그 배선이다.

    ⛔⛔ **이 곡선의 평균은 정본 MTO 곡선과 같지 않다.**
      `msd_multi_origin` 은 lag 마다 쓸 수 있는 원점을 **전부**(nt−L 개) 쓴다 — 짧은 lag
      일수록 원점이 많다. 재표본은 **교환가능한 단위**가 있어야 하므로 여기서는 모든 lag 를
      덮는 **공통 원점 집합**(`t0 < nt − lag_max`)만 쓴다. ⇒ 짧은 lag 의 표본이 정본보다
      적고, 평균 곡선이 미세하게 다르다.
      **그래서 이 행렬은 σ 전용이다.** D·Ea 의 **값**은 정본 곡선에서 내고
      (`joint_ea_bootstrap(runs=[{… "mean_curve": 정본곡선}])`), 여기서는 **산포만** 가져온다.

    ⛔ 이 함수가 **못 하는 것**
      · 궤적이 없으면 아무것도 못 한다 (원리적 복구 불가 — 새로 돌려야 한다).
      · `save_fs` 를 못 읽으면 캠페인 기본 100 fs 를 **가정하고 그 사실을 돌려준다**
        (`save_fs_assumed=True`). 조용히 가정하지 않는다.
      · 원점 사이 상관을 **고치지 않는다** — 그건 블록 길이가 할 일이다.
      · 드리프트를 빼지 않는다 (정본 경로와 같은 규약: 빼지 않는다).
    """
    import numpy as _np
    jp = pathlib.Path(json_path)
    traj = jp.parent / "traj.xyz"
    if not traj.exists():
        return None
    assumed = save_fs is None
    if assumed:
        save_fs = 100.0
    try:
        frames = _ase_read(traj, ":")
    except BaseException as e:
        print(f"   ⚠ traj 읽기 실패: {type(e).__name__} {e}")
        return None
    if not frames or len(frames) < 8:
        return None
    sym = frames[0].get_chemical_symbols()
    li = [i for i, s in enumerate(sym) if s == "Li"]
    if not li:
        print("   ⚠ traj 에 Li 가 없다")
        return None
    cart = _np.array([f.get_positions() for f in frames])[:, li]
    nt = cart.shape[0]
    lag_max = max(2, nt // 2)
    #: lag 격자는 `msd_multi_origin` 과 **같은 식**이다 — 시간축이 정본과 어긋나면
    #: 점추정(정본 곡선)과 σ(이 행렬)를 같은 창에서 못 쓴다.
    lags = _np.unique(_np.linspace(1, lag_max, min(int(n_lag), lag_max)).astype(int))
    n_o = nt - int(lags[-1])
    if n_o < 2:
        return None
    M = _np.empty((n_o, len(lags)), float)
    for j, L in enumerate(lags):
        d = cart[int(L):int(L) + n_o] - cart[:n_o]      # (n_o, n_Li, 3)
        M[:, j] = (d ** 2).sum(-1).mean(axis=1)
    return {"t_ps": [float(L) * save_fs / 1000.0 for L in lags],
            "msd_per_origin": M, "n_origin": int(n_o), "lag_max": int(lags[-1]),
            "save_fs": float(save_fs), "save_fs_assumed": bool(assumed),
            "note": "공통 원점 집합. 평균 곡선은 정본 MTO 와 **다르다** — σ 전용."}


def _ase_read(path, index=":"):
    """ase.io.read 를 **한 곳에서만** 부른다. 실패하면 이유를 말하고 예외를 낸다.

    ⛔⛔ 2026-09-07 — `_read` 가 `directional_msd_tensor`/`n_per_elem_from_traj` **안의
      지역 import** 였는데 `mto_from_traj`(L740)와 `haven_from_traj` 가 그 이름을 그냥
      불렀다. 파이썬 지역 import 는 전역 이름을 만들지 않으므로 **NameError** 다.
      · `haven_from_traj` 는 첫 실행에서 바로 드러났고,
      · `mto_from_traj` 는 `except BaseException` 이 삼켜 *"traj 읽기 실패"* 로만 찍혔다
        ⇒ **`--rebuild_mto` 가 조용히 전부 실패하고 있었다.** 예외를 넓게 잡으면
        "궤적이 없다" 와 "코드가 틀렸다" 가 같은 문장이 된다.
    """
    try:
        from ase.io import read as _r
    except ImportError as e:
        raise RuntimeError(f"ase 를 못 불러온다 ({e}) — `conda activate uma` 필요") from e
    return _r(str(path), index=index)


def haven_curves(cart_li, dt_ps, cart_ref=None, n_lag=150):
    """tracer MSD 와 **집단(전하)좌표 MSD** 를 같은 시간원점 집합에서 함께 낸다.

    반환 `(tau_ps, msd_tracer, msd_charge, n_origins)` — 둘 다 Å², 다중 시간원점.

        MSD*(τ)      = <|Δr_i(τ)|²>_{i, t0}                    ← 지금 쓰는 양
        MSD_σ(τ)     = <|Σ_i Δr_i(τ)|²>_{t0} / N               ← 집단좌표

    Haven 비  `H_R ≡ D*/D_σ` 이고, Nernst–Einstein 은 `σ = n q² D_σ /(k_B T)` 다.
    우리는 D* 를 대입해 왔으므로 `σ_NE = H_R × σ_true` — **H_R<1 이면 과소**다.

    ⚠ **드리프트 기준은 골격(비-Li)이다 — 전 원자 COM 이 아니다.**
      ⛔⛔ 첫 판은 전 원자 COM 을 뺐다. 그런데 Li 가 전 원자의 **44–45 %**(modelc 27/62 ·
      b2o3 58/128)라 전 원자 COM 안에 Li 집단좌표가 그만큼 들어 있고, 그걸 빼면
      **재려는 신호를 스스로 지운다.** 합성시험 ⑥ 에서 `cart_all = cart_li` 로 주니
      `Σ Δr ≡ 0` 이 되어 H_R 이 발산했다 — 극단 사례지만 실물에서도 같은 방향으로
      **H_R 을 체계적으로 과대**하게 만든다.
      전하 수송은 **고정 골격에 대한 Li 의 운동**이므로 기준은 비-Li COM 이다.
      `cart_ref` 를 안 주면 빼지 않고 **그 사실을 반환값에 표시**한다(조용히 넘기지 않는다).

    ⛔ 이 함수가 **못 하는 것**
      · `H_R` 을 정확히 주지 못한다. 집단좌표는 **표본이 하나**라(이온 N개 평균이 아니다)
        같은 궤적에서 D* 보다 훨씬 잡음이 크다. 200 ps·Li 27–58 개면 30–50 % 오차를 각오한다.
        방향(H_R ≷ 1)은 가릴 수 있고, 세 자리 숫자는 못 낸다.
      · 전하가 Li 만이라고 본다 (골격 이온의 반대 흐름을 안 센다).
      · 이건 **새 보고량**이다 — 값으로 쓰려면 estimand 카드·문턱 선등록이 먼저다.
    """
    import numpy as _np
    a = _np.asarray(cart_li, dtype=float)
    nt, N = a.shape[0], a.shape[1]
    if nt < 8 or N < 1:
        return [], [], [], []
    if cart_ref is not None:
        ref = _np.asarray(cart_ref, dtype=float)
        if ref.ndim != 3 or ref.shape[0] != nt or ref.shape[1] < 1:
            raise ValueError(f"cart_ref 모양이 안 맞는다: {ref.shape} vs Li {a.shape}")
        a = a - ref.mean(axis=1)[:, None, :]      # 골격 COM 기준 상대변위
    lag_max = max(2, nt // 2)
    lags = _np.unique(_np.linspace(1, lag_max, min(n_lag, lag_max)).astype(int))
    tau, mt, mc, nor = [], [], [], []
    tot = a.sum(axis=1)                                            # (nt, 3) 집단좌표
    for L in lags:
        d = a[L:] - a[:-L]                                         # (n0, N, 3)
        dt_ = tot[L:] - tot[:-L]                                   # (n0, 3)
        tau.append(float(L * dt_ps))
        mt.append(float((d ** 2).sum(axis=2).mean()))
        mc.append(float((dt_ ** 2).sum(axis=1).mean() / N))
        nor.append(int(d.shape[0]))
    return tau, mt, mc, nor


def haven_from_traj(json_path, save_fs=None, lo=2.0, hi=50.0):
    """`traj.xyz` 에서 **Haven 비를 직접 잰다.** 궤적이 없으면 None.

    왜 (2026-09-07): 우리는 σ 를 `H_R=1` 로 환산해 왔고, 그 값을 "상한" 이라고 적어 왔다.
      **부호가 틀렸다** — `H_R<1` 이면 NE 는 과소다(kb/concepts/md.md §6 정정).
      문헌값(Adeli 0.23)을 빌려 쓸 수도 있지만, 그건 다른 조성·다른 방법의 소환값이다.
      궤적이 있으면 **우리 계에서 직접 잴 수 있고 MD 재계산이 0** 이다.

    적합 창·자유절편은 D 규약을 그대로 따른다 (`lin_fit`, 기본 2–50 ps).
    ⛔ 못 하는 것은 `haven_curves` 의 docstring 참조 — 특히 **정밀도**.
    """
    jp = pathlib.Path(json_path)
    traj = jp.parent / "traj.xyz"
    if not traj.exists():
        print(f"   · {jp.parent.name}: traj.xyz 가 없다 — Haven 측정 원리적 불가")
        return None
    assumed = save_fs is None
    if assumed:
        save_fs = 100.0
    try:
        frames = _ase_read(traj, ":")
    except BaseException as e:                                     # noqa: BLE001
        print(f"   ⚠ traj 읽기 실패: {type(e).__name__} {e}")
        return None
    if not frames or len(frames) < 8:
        return None
    import numpy as _np
    sym = frames[0].get_chemical_symbols()
    li = [i for i, s in enumerate(sym) if s == "Li"]
    if not li:
        print("   ⚠ traj 에 Li 가 없다")
        return None
    cart = _np.array([f.get_positions() for f in frames])
    fw = [i for i, s_ in enumerate(sym) if s_ != "Li"]
    # ⛔ 기준은 **골격(비-Li)** COM 이다. 전 원자 COM 을 쓰면 Li(전 원자의 ~45 %)의
    #   집단좌표를 스스로 빼서 H_R 을 체계적으로 과대하게 만든다 (합성시험 ⑥).
    tau, mt, mc, nor = haven_curves(cart[:, li], save_fs / 1000.0,
                                    cart_ref=cart[:, fw] if fw else None)
    if not tau:
        return None
    st = lin_fit(tau, mt, lo, hi)
    sc = lin_fit(tau, mc, lo, hi)
    if not st or not sc or st[0] is None or sc[0] is None:
        print(f"   ⚠ {jp.parent.name}: {lo}–{hi} ps 창에 점이 모자라 적합 불가")
        return None
    d_star = st[0] / 6.0 * 1e-16 / 1e-12                           # Å²/ps → cm²/s
    d_sig = sc[0] / 6.0 * 1e-16 / 1e-12
    # ⛔ D_σ 가 잡음 바닥이면 H_R 은 **큰 수가 아니라 정의되지 않는다.**
    #   여기서 큰 유한값을 뱉으면 그게 측정처럼 읽힌다 (합성시험 ③ 이 잡은 실패).
    hr, hr_note = None, None
    if d_sig <= 0:
        hr_note = "D_σ ≤ 0 (잡음 바닥) — H_R 정의되지 않음. NE 는 과대 쪽이나 배수는 무계"
    elif sc[2] is not None and sc[2] < 0.5:
        hr_note = f"D_σ 적합 R²={sc[2]:.2f} < 0.5 — 집단좌표가 확산영역에 없다. H_R 보류"
    else:
        hr = d_star / d_sig
    print(f"   … {traj.parent.name}: Li {len(li)} · {len(frames)} 프레임"
          + (f" · save_fs={save_fs:g} fs **가정**" if assumed else f" · save_fs={save_fs:g} fs"))
    print(f"      D* = {d_star:.3e} · D_sigma = {d_sig:.3e} cm²/s"
          + (f" · H_R = {hr:.3f}" if hr else f" · H_R **미정** — {hr_note}"))
    return {"window_ps": [lo, hi], "n_Li": len(li), "n_frames": len(frames),
            "D_star_cm2_s": d_star, "D_sigma_cm2_s": d_sig, "haven_ratio": hr,
            "haven_undefined_why": hr_note,
            "R2_tracer": st[2], "R2_charge": sc[2],
            "drift_reference": ("framework(non-Li) COM" if fw else "없음 — 비-Li 원자가 0"),
            "save_fs_assumed": assumed,
            "⚠": ("집단좌표는 표본이 하나라 D* 보다 잡음이 훨씬 크다 — 방향 판별용이지 "
                  "세 자리 숫자가 아니다. 값으로 쓰려면 estimand 카드·문턱 선등록이 먼저다.")}


def n_per_elem_from_traj(json_path):
    """traj.xyz **첫 프레임만** 읽어 원소별 원자수를 센다. 없으면 None.

    왜 따로 두나: 2026-08-20 에 `--from_traj` 로 캐시해 둔 json 들은 `n_atoms_per_elem`
    이전 판이라 개수가 없다. 개수가 없으면 표본 부족 원소를 못 걸러내는데,
    그걸 위해 118 MB 궤적을 통째로 다시 읽을 이유는 없다 — 첫 프레임이면 충분하다.
    """
    traj = pathlib.Path(json_path).parent / "traj.xyz"
    if not traj.exists():
        return None
    try:
        from ase.io import read as _read
        at = _read(str(traj), index=0)
    except BaseException:
        return None
    syms = at.get_chemical_symbols()
    return {e: syms.count(e) for e in sorted(set(syms))}


# ══ 골격 흐름(drift) vs 재배열(rearrangement) 판별 — 2026-08-25 ════════════
#   골격 β 가 높다고 곧바로 'Li D 폐기' 가 아니다. 골격이 **통째로 흐르는 것**이면
#   공동계(co-moving frame)에서 Li 확산을 구제할 수 있고, **자리 재배열**이면 못 한다.
#   판정 기준은 **결과를 보기 전에** 고정한다:
DRIFT_KEEP = 0.30      # COM 제거 후 골격 MSD 가 원래의 30 % 이하 → 흐름 지배 = 구제 가능
DRIFT_LOST = 0.70      # 70 % 이상 남으면 재배열 = 구제 불가
#: ⛔⛔ 2026-08-28 실측 — 위 두 문턱은 **비율**이라 골격이 거의 안 움직일 때 뜻을 잃는다.
#:   골격이 진동만 하면(MSD 0.3–1 Å²) COM 을 빼도 바뀌는 게 없어 kept ≈ 1.0 이 되고,
#:   그러면 **rigid 한 골격이 "재배열 — 구제 불가"** 로 찍힌다. 실제로 modelc 9개 중 8개가
#:   그렇게 나왔다 — 같은 실행의 골격 β 검사는 **9/9 rigid** 라고 했는데도.
#:   ⇒ '흐름이냐 재배열이냐' 는 **골격이 실제로 움직일 때만** 성립하는 질문이다.
#:   오늘 아침 스칼라 일치도에서 고친 것과 같은 종류(절대 바닥 없는 백분율)다.
DRIFT_MIN_MSD = 2.0    # 골격 MSD [Å²] 가 이 밑이면 진동이다 — 판정하지 않는다 (RMS 1.4 Å)


def framework_com_split(json_path, save_fs=None):
    """골격 MSD 를 **전역 흐름분과 내부 재배열분으로 가른다** (재계산 0, 궤적만 있으면 됨).

    돌려주는 값: None 또는
      {'frame_total','frame_internal','kept_frac','li_total','li_internal','verdict'}
      (MSD 는 창 끝 값 Å², kept_frac = internal/total)

    ⛔ 이 함수가 못 하는 것
      · 국소 재배열을 지우지 못한다. COM 은 **전역 1개**라 골격 절반이 왼쪽·절반이
        오른쪽으로 가면 COM 은 0 이고 내부 MSD 는 그대로 남는다 — 그게 노림수다.
      · '구제 가능' 이 곧 '값 인용 가능' 은 아니다. 공동계 Li D 를 **다시 게이트에
        통과시켜야** 한다 (β·케이지 검사를 새로).
    """
    import importlib.util
    jp = pathlib.Path(json_path)
    traj = jp.parent / "traj.xyz"
    if not traj.exists():
        return None
    src = pathlib.Path(__file__).resolve().parents[1] / "modelc_v3" / "aimd_mlip.py"
    if not src.exists():
        return None
    spec = importlib.util.spec_from_file_location("_aimd", src)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
        raw = mod.compute_msd_per_element(traj, dt_save_fs=save_fs or 100.0)
        com = mod.compute_msd_per_element(traj, dt_save_fs=save_fs or 100.0,
                                          com_exclude=LI)
    except BaseException as e:
        print(f"   ⚠ COM 분해 실패: {type(e).__name__} {e}")
        return None

    def _frame_end(o):
        m, n = o["msd_per_elem_A2"], o.get("n_atoms_per_elem", {})
        els = [e for e in m if e != LI and n.get(e, 0) >= FRAMEWORK_MIN_N]
        if not els:
            return None
        # 원자수 가중 평균 — 종마다 개수가 달라 단순평균은 소수 종에 끌려간다
        tot = sum(n[e] for e in els)
        return sum(m[e][-1] * n[e] for e in els) / tot

    ft, fi = _frame_end(raw), _frame_end(com)
    if ft is None or fi is None or ft <= 0:
        return None
    kept = fi / ft
    if ft < DRIFT_MIN_MSD:
        v = "framework_static"        # 판정 자체가 성립 안 한다 (위 DRIFT_MIN_MSD 주석)
    else:
        v = ("drift_dominated" if kept <= DRIFT_KEEP else
             "rearrangement" if kept >= DRIFT_LOST else "mixed")
    return {"frame_total": ft, "frame_internal": fi, "kept_frac": kept,
            "li_total": raw["msd_per_elem_A2"][LI][-1],
            "li_internal": com["msd_per_elem_A2"][LI][-1],
            "verdict": v}


# ══ 결합S vs 자유S 분리 β (2026-08-25 — b2o3 서술③ 판정) ═══════════════════
#   b2o3 골격 검사에서 worst 가 S(41)·Cl(16) 로 나왔지만, S 41개 중 29개는
#   폴리음이온(PS₄·BS₃·PS₂O₂) 안의 **결합S** 고 12개만 **자유S** 다. 결합 검사
#   (b2o3_all_bond_lengths --traj)는 공유결합이 9/9 불변임을 이미 보였다 —
#   그러면 움직인 것은 자유 음이온 부격자여야 한다. 여기서 그걸 β 로 가른다.
#
#   판정 기준 (**데이터 보기 전 고정**):
#     bonded-S β < 0.30 이고 (free-S β ≥ 0.30 또는 Cl β ≥ 0.30)
#         → free_anion_sublattice_mobile  (서술③ 확정)
#     bonded-S β ≥ 0.30 → polyanion_frame_mobile  (서술③ 기각 — 골격 자체가 움직임)
#     둘 다 < 0.30     → inconsistent  (앞선 원소별 검사와 모순 — 재조사)
#
#   ⛔ 이 검사가 못 하는 것: 분류는 **첫 프레임** 결합 기준이다. 런 도중 결합이
#     바뀌면 그 원자는 잘못 분류된다 — 단, 결합 불변(9/9)이 먼저 확인된 계에서만
#     쓰라는 전제가 그래서 있다. 새 조성에 쓰려면 결합 검사부터 통과시킬 것.
SPLIT_RIGID = 0.30

# ── 단위별 판정 (2026-08-25, **데이터 보기 전 고정**) ────────────────────────
#   질문: b2o3 가 넣은 BS₃ 가 유동화의 원인인가, 호스트 PS₄ 자체가 무른가.
#   ⚠ 절대 β 는 온도마다 달라 계 간 비교가 안 된다. **같은 런 안의 비**로 본다.
UNIT_RATIO_HI = 2.0     # BS₃ MSD / PS₄ MSD ≥ 2.0 → BS₃ 가 유의하게 더 움직임
UNIT_RATIO_LO = 1.25    # ≤ 1.25 → 사실상 같이 움직임 (호스트 전체가 무름)
#   판정:
#     BS3_driven      : ratio ≥ 2.0  AND  PS4_unit β < 0.30   → 도핑 단위가 원인
#     host_wide       : ratio ≤ 1.25 AND  PS4_unit β ≥ 0.30   → 호스트 전체가 무름
#                                                                (UMA 아티팩트 쪽 무게↑)
#     both_mobile     : ratio ≥ 2.0  AND  PS4_unit β ≥ 0.30   → BS₃ 가 더 심하나 호스트도 움직임
#     inconclusive    : 그 외

_BOND_TOOL = pathlib.Path(__file__).resolve().parents[1] / "comp1_v3" / "b2o3_all_bond_lengths.py"


def unit_verdict(ratio, ps4_beta):
    """BS₃/PS₄ 비와 PS₄ β 에서 판정 하나를 낸다. **순수 함수** — selftest 대상.

    ⛔ 못 하는 것: 표본 수(n)·MSD 부호 검사는 호출부가 한다. 여기 오는 건
      이미 걸러진 값이다. ps4_beta 가 None(β 미산출)이면 판정하지 않는다 —
      '비만 크다' 로 BS3_driven 을 주면 호스트도 같이 뛰는 경우를 놓친다.
    """
    if ratio is None or ps4_beta is None:
        return "inconclusive"
    if ratio >= UNIT_RATIO_HI and ps4_beta < SPLIT_RIGID:
        return "BS3_driven"
    if ratio <= UNIT_RATIO_LO and ps4_beta >= SPLIT_RIGID:
        return "host_wide"
    if ratio >= UNIT_RATIO_HI and ps4_beta >= SPLIT_RIGID:
        return "both_mobile"
    return "inconclusive"


def _load_bond_tool():
    import importlib.util
    spec = importlib.util.spec_from_file_location("_bt", _BOND_TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def classify_sulfur(syms, cart, cell):
    """첫 프레임에서 S 를 결합S(P/B 결합창 안) / 자유S 로 가른다.

    결합창·최소이미지는 b2o3_all_bond_lengths 의 것을 **그대로 빌려 쓴다**
    (복사하면 규약이 갈라진다 — convention_check 대상).
    """
    bt = _load_bond_tool()
    import numpy as np
    syms = np.array(syms)
    D = bt.min_image_D(np.asarray(cart), np.asarray(cell))
    s_idx = [i for i, s in enumerate(syms) if s == "S"]
    cations = {"P": bt.DECOMP_WINDOWS[("P", "S")], "B": bt.DECOMP_WINDOWS[("B", "S")]}
    bonded, free, on_p, on_b = [], [], [], []
    for i in s_idx:
        host = None
        for cat, (lo, hi) in cations.items():
            for j in [k for k, s in enumerate(syms) if s == cat]:
                if lo <= D[i, j] <= hi:
                    host = cat
                    break
            if host:
                break
        if host is None:
            free.append(i)
        else:
            bonded.append(i)
            (on_p if host == "P" else on_b).append(i)
    P = [i for i, s in enumerate(syms) if s == "P"]
    B = [i for i, s in enumerate(syms) if s == "B"]
    # ★ 2026-08-25 — **단위(unit) 단위 그룹**. 원자별로는 B 가 n=2 라 컷오프(8) 아래여서
    #   판정에서 빠졌다. 그런데 결합 검사가 B–S 6→6 불변을 보였으므로 B 와 그 S 3개는
    #   **한 몸**이다 ⇒ BS₃ 단위(B 2 + S 6 = 8원자)를 하나의 그룹으로 보면 컷오프를 만족한다.
    #   이 그룹이 "b2o3 가 넣은 것이 움직이나(BS₃) vs 호스트가 무르나(PS₄)" 를 가른다.
    return {"bonded_S": bonded, "free_S": free,
            "S_on_P": on_p, "S_on_B": on_b,
            "PS4_unit": sorted(P + on_p), "BS3_unit": sorted(B + on_b),
            "Cl": [i for i, s in enumerate(syms) if s == "Cl"],
            "P": P, "B": B,
            "O": [i for i, s in enumerate(syms) if s == "O"]}


def framework_split(json_path, lo, hi, save_fs=None):
    """traj 에서 결합S/자유S/Cl 별 β → 서술③ 판정. → dict | None."""
    import importlib.util
    jp = pathlib.Path(json_path)
    traj = jp.parent / "traj.xyz"
    if not traj.exists():
        return None
    src = pathlib.Path(__file__).resolve().parents[1] / "modelc_v3" / "aimd_mlip.py"
    spec = importlib.util.spec_from_file_location("_aimd", src)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
        from ase.io import read as _aseread
        f0 = _aseread(str(traj), index=0)
    except BaseException as e:
        print(f"   ⚠ 로드 실패: {type(e).__name__} {e}")
        return None
    groups = classify_sulfur(f0.get_chemical_symbols(), f0.get_positions(),
                             f0.cell.array)
    out = mod.compute_msd_per_element(traj, dt_save_fs=save_fs or 100.0,
                                      groups=groups)
    tps = out["times_ps"]
    res = {}
    for g, idxs in groups.items():
        y = out["msd_per_group_A2"].get(g)
        if y is None:
            continue
        res[g] = {"n": len(idxs), "beta": loglog_slope(tps, y, lo, hi),
                  "msd_end_A2": round(y[-1], 2),
                  "judged": len(idxs) >= FRAMEWORK_MIN_N}
    bs, fs, cl = res.get("bonded_S"), res.get("free_S"), res.get("Cl")

    def _b(x):
        return x["beta"] if (x and x["judged"] and x["beta"] is not None) else None
    v = "insufficient"
    if _b(bs) is not None:
        if _b(bs) >= SPLIT_RIGID:
            v = "polyanion_frame_mobile"
        elif any(b is not None and b >= SPLIT_RIGID for b in (_b(fs), _b(cl))):
            v = "free_anion_sublattice_mobile"
        elif all(b is not None and b < SPLIT_RIGID for b in (_b(fs), _b(cl))):
            v = "inconsistent_with_elementwise"

    # ── 단위 판정: BS₃ vs PS₄ (사전 등록 기준) ──────────────────────────────
    ps4, bs3 = res.get("PS4_unit"), res.get("BS3_unit")
    unit = {"verdict": "no_BS3"}
    if ps4 and bs3 and bs3["n"] >= FRAMEWORK_MIN_N and ps4["msd_end_A2"] > 0:
        ratio = bs3["msd_end_A2"] / ps4["msd_end_A2"]
        pb = _b(ps4)
        uv = unit_verdict(ratio, pb)
        unit = {"verdict": uv, "ratio_BS3_over_PS4": round(ratio, 2),
                "PS4_beta": pb, "BS3_beta": _b(bs3),
                "PS4_msd_end": ps4["msd_end_A2"], "BS3_msd_end": bs3["msd_end_A2"],
                "n_PS4": ps4["n"], "n_BS3": bs3["n"]}
    return {"groups": res, "verdict": v, "unit": unit,
            "li_msd_end": out["msd_per_elem_A2"]["Li"][-1]}


def framework_check(d, lo, hi):
    """골격(비-Li) 원소가 확산하고 있나.

    돌려주는 값: None(종별 MSD 없음) 또는
      {'t_end','li','frame':{el:{'msd_end','ratio','beta'}}, 'worst_el','worst_ratio','verdict'}

    이 함수가 **못 하는 것**: 종별 MSD 가 없으면 아무 말도 못 한다(None).
      궤적에서 뽑는 것은 `elem_msd_from_traj()` 가 하고, 호출자가 `--from_traj` 로 켠다.
      **traj.xyz 도 없는 런은 원리적으로 판정 불가**다 — 새로 돌려야 한다.
    """
    em = _elem_msd(d)
    if not em:
        return None
    t = d.get("times_ps") or (d.get("msd_data") or {}).get("times_ps")
    if not t or LI not in em:
        return None
    npe = (d.get("n_atoms_per_elem")
           or (d.get("msd_data") or {}).get("n_atoms_per_elem") or {})
    t = list(t)
    # 창 끝(hi) 에 가장 가까운 표본
    k = min(range(len(t)), key=lambda i: abs(t[i] - hi))
    li_end = float(em[LI][k])
    frame, judged, thin = {}, [], []
    for el, y in em.items():
        if el == LI:
            continue
        end = float(y[k])
        n = int(npe.get(el, 0))
        rec = {"msd_end_A2": end, "n_atoms": n or None,
               "ratio_to_Li": (end / li_end if li_end > 0 else float("inf")),
               "beta": loglog_slope(t, y, lo, hi)}
        frame[el] = rec
        # 표본이 적으면 **판정에 넣지 않는다**. 개수를 모르면(옛 파일) 일단 판정에 넣되
        # 그 사실을 남긴다 — 조용히 빼면 "본 적 없는 원소"가 생긴다.
        (thin if (n and n < FRAMEWORK_MIN_N) else judged).append(el)
    if not frame:
        return None
    if not judged:
        v, worst_el = "sample_too_thin", None
    else:
        # ⛔⛔ 2026-08-20 (codex 리뷰) — **대표 원소 하나만 판정하던 것을 폐기한다.**
        #   앞 판은 β 를 0.05 로 양자화해 '최악' 원소를 고른 뒤 **그 원소만** 판정했다.
        #   그러면 양자화가 같은 통에 넣은 원소끼리 비(ratio) 로 대표가 갈리고,
        #   진짜로 fail 인 원소가 판정에서 빠진다. codex 반례를 그대로 재현했다:
        #       P β=0.610 ratio=0.010   (β ≥ 0.60 ⇒ melting)
        #       S β=0.590 ratio=0.020   ← 양자화가 같은 통, 비가 커서 대표로 뽑힘
        #       판정 = mobile   ⛔ P 가 판정에서 빠졌다
        #   ⇒ **원소마다 severity 를 내고 전체 max 로 판정한다.** 대표 표시는 그 뒤 문제다.
        def _sev(e):
            b, r = frame[e]["beta"], frame[e]["ratio_to_Li"]
            if b is None:
                return 0
            if b >= FRAMEWORK_BETA_MELT or r >= FRAMEWORK_FAIL_RATIO:
                return 2
            if b >= FRAMEWORK_BETA_RIGID or r >= FRAMEWORK_WARN_RATIO:
                return 1
            return 0
        sev = {e: _sev(e) for e in judged}
        top = max(sev.values())
        v = {0: "framework_rigid", 1: "framework_mobile", 2: "framework_melting"}[top]
        # 대표는 **표시용**이고 판정과 분리돼 있다. 고르는 규칙이 경우마다 다르다:
        #   · fail 이 있으면(top≥1) **유발 원소 중 β 최대** — 무엇이 판정을 만들었나를 보여준다.
        #   · 전부 rigid 면 β 는 1e-15 급 부동소수 잡음이라 **비(ratio) 로 고른다.**
        #     (β 로 고르면 잡음이 대표를 정한다 — selftest 가 그걸 잡았다.)
        drivers = [e for e in judged if sev[e] == top]
        if top >= 1:
            worst_el = max(drivers, key=lambda e: (frame[e]["beta"] if frame[e]["beta"] is not None
                                                   else -9.0, frame[e]["ratio_to_Li"]))
        else:
            worst_el = max(judged, key=lambda e: frame[e]["ratio_to_Li"])
            drivers = []          # rigid 면 유발 원소가 없다
        if all(frame[e]["beta"] is None for e in judged):
            v, worst_el = "sample_too_thin", None
    if judged and worst_el is not None:
        for e in judged:
            frame[e]["severity"] = _sev(e)
        frame_fail = [e for e in judged if frame[e].get("severity", 0) >= 1]
    else:
        frame_fail = []
    return {"t_end_ps": t[k], "li_msd_end_A2": li_end, "frame": frame,
            "judged": judged, "thin": thin, "drivers": frame_fail,
            "worst_el": worst_el, "verdict": v,
            "worst_ratio": (frame[worst_el]["ratio_to_Li"] if worst_el else None)}


def thin_note(r):
    """판정에서 뺀 원소를 화면 문구로. 없으면 빈 문자열.

    ⛔⛔ 2026-09-10 — 호출부가 `r["frame"].get("_thin")` 을 봤다. `frame` 은
      원소기호로 키가 잡힌 사전이라 `_thin` 은 **영원히 None** 이다 ⇒ 제외 원소가
      화면에 **한 번도 안 찍혔다**. framework_check 는 `thin` 을 제대로 돌려주고
      selftest 도 그 반환값을 검사해 통과하고 있었다 — 함수는 맞고 **화면만
      거짓말**이었다. 그래서 표기를 함수로 빼서 selftest 가 화면 문구를 직접 본다.

      대가가 실제로 있었다: b2o3 소형셀(128원자)에서 B(2)·O(3)이 조용히 빠져
      기준선 0.47–0.79 가 {Cl,P,S} 의 max 였는데, 2×2×1(512원자)에서 B(8)·O(12)가
      판정에 들어와 **다른 원소집합의 max** 가 됐다. 화면이 제외를 찍었다면
      그 차이를 그때 봤다.
    """
    thin = r.get("thin") or []
    parts = [f"{e}({r['frame'][e].get('n_atoms')},β{r['frame'][e]['beta']:.2f})"
             for e in thin
             if e in r.get("frame", {}) and r["frame"][e].get("beta") is not None]
    return "  [판정제외 " + ",".join(parts) + "]" if parts else ""


def framework_elem_table(r):
    """원소별 한 줄 (판정에 들어간 것/뺀 것을 나눠서). --framework_elems 용.

    이 함수가 못 하는 것: 부분집합의 max 를 **판정으로 바꾸지 않는다.**
      봉인된 보고량은 판정 대상 전체의 max 다 — 여기 표는 *무엇이 그 max 를
      만들었나* 를 보여줄 뿐이다.
    """
    rows, judged = [], set(r.get("judged") or [])
    for e in sorted(r.get("frame", {})):
        rec = r["frame"][e]
        b = rec.get("beta")
        rows.append("      {:<3s} n={:<4s} β={:>6s}  ratio={:>7s}  {}".format(
            e, str(rec.get("n_atoms") or "?"),
            "—" if b is None else f"{b:.2f}",
            "—" if rec.get("ratio_to_Li") is None else f"{rec['ratio_to_Li']:.3f}",
            ("판정" if e in judged else "제외(표본부족)")
            + (f" sev={rec['severity']}" if "severity" in rec else "")))
    return rows


def framework_verdict_text(v):
    return {
        "sample_too_thin": ("⚠ **표본 부족 — 판정 못 한다.** 골격 원소가 전부 "
                            f"{FRAMEWORK_MIN_N}개 미만이라 MSD 평균이 단일 사건에 휘둘린다"),
        "framework_rigid": "⭕ 골격 고정 — Li 만 움직인다. D/Ea 를 쓸 수 있다",
        "framework_mobile": ("⚠ 골격이 따라 움직인다 (0.30≤β<0.60) — Li 확산에 구조 이완이 "
                             "섞였다. 같은 온도의 다른 조성과 β 를 나란히 볼 것 "
                             "(실측 2026-08-25 멀티시드: modelc 600/800/1000 K "
                             "= -0.01 / 0.03·-0.05·-0.01 / 0.27·0.04·0.01 로 7/7 rigid, "
                             "b2o3 는 800 부터 0.51·0.79·0.54 — **b2o3 고유**. "
                             "⛔ 옛 주석의 '0.03/0.08 vs 0.59/0.63' 은 single-seed legacy 라 "
                             "canonical_registry 2026-08-20a 가 철회한 값이었다)"),
        "framework_melting": ("⛔ **골격이 확산 쪽으로 간다** (β≥0.60). Li 'D' 에 구조 완화가 "
                              "섞였다 — 그 온도 점은 아레니우스에서 빼거나 단서를 달 것. "
                              "⚠ β≈1 의 완전 융해와는 다르다: 0.6~0.9 는 '기어가는(creep)' "
                              "구간이다. Zhang npj 2026 의 MACE-MP-0 LGPS 융해와 같은 축이되 "
                              "강도는 약하다"),
    }.get(v, "판정 불가")


def selftest():
    """판정 로직 검증. **음성 경로가 핵심이다** — 못 잰 것을 통과로 읽지 않는지.

    이 selftest 가 생긴 이유(2026-08-17): lpsocl 작은 셀 3런이 MSD 배열 없이
    β 세 칸 전부 '—' 였는데 마지막 줄이 `✅ 3개 전부 확산 영역 — D/Ea 인용 가능`
    이었다. 양성만 보는 검사는 이걸 못 잡는다.
    """
    import io as _io
    import json as _json
    import contextlib as _ctx
    import tempfile as _tf
    n_ok = n_bad = 0

    def chk(cond, msg):
        nonlocal n_ok, n_bad
        if cond:
            n_ok += 1
            print(f"  ✓ {msg}")
        else:
            n_bad += 1
            print(f"  ✗ {msg}")

    # ── 집계 자격 (회신 BQ-6) — 리뷰어 합성 사례 두 개를 그대로 시험으로 ────────
    _t = [float(i) for i in range(1, 101)]
    _y1 = [0.1 * x for x in _t]; _y2 = [27 + 0.1 * x for x in _t]
    _e1 = aggregation_eligible(_t, _y1, 60); _e2 = aggregation_eligible(_t, _y2, 60)
    chk(run_verdict(_t, _y1)[0] == HOLD and run_verdict(_t, _y2)[0] == CITABLE,
        "[재현 BQ-6 ①] 절편 27 Å² 만 다른 두 곡선에서 run_verdict 가 hold ↔ citable 로 갈린다 (MSD 대용값 1.1 → 4.1)")
    chk(_e1[0] == _e2[0] and _e1[2]["msd_magnitude_alarm"] != _e2[2]["msd_magnitude_alarm"],
        "[음성 BQ-6 P0-1] 집계 자격은 절편에 **안 갈린다** — MSD 대용값은 경보로만 남고 자격을 안 정한다")
    _yp = [30 + 0.5 * x for x in _t]
    # 섭동은 2–50 ps 안에서만, D_inc 창 끝점 2·10·25·50 에서 0 (창 밖 100 도 건드리지 않는다)
    #   ⚠ 첫 판은 전 구간 5차식을 전역 최대로 정규화해서 2–50 안 진폭이 거의 0 이었다 → 시험이 초록 (헛것)
    def _bump(x):
        if not (2.0 <= x <= 50.0):
            return 0.0
        return (x - 2.0) * (x - 10.0) * (x - 25.0) * (x - 50.0)
    _m = max(abs(_bump(x)) for x in _t)
    _yq = [yy + 12.0 * _bump(x) / _m for yy, x in zip(_yp, _t)]
    _pl = dinc_plateau(_t, _yq); _rv = run_verdict(_t, _yq)[0]; _rat = sub_window_ratios(_t, _yq)
    _eq = aggregation_eligible(_t, _yq, 60)
    chk(_pl["status"] == "plateau" and _pl["spread"] < 1e-9 and _rv == CITABLE,
        "[재현 BQ-6 ②] D_inc 창 끝점만 지키고 중간을 흔들면 plateau 산포 0 · run_verdict CITABLE")
    chk(_rat is not None and any(not (0.8 <= r <= 1.2) for r in _rat) and _eq[0] is False
        and any("부창" in s for s in _eq[1]),
        "[음성 BQ-6 P0-2] 그 곡선은 부창 기울기 비가 기준 밖이고 **집계 자격이 없다** — CITABLE 하나가 통과로 승격되지 않는다")
    chk(aggregation_eligible(_t, _yp, 60)[0] is True,
        "[양성] 직선 + 사건 60 → 자격 있음")
    _en = aggregation_eligible(_t, _yp, None)
    chk(_en[0] is False and any("검사 불가" in s for s in _en[1]),
        "[음성] 사건 수 None 은 '검사 불가' 이지 통과가 아니다")
    chk(aggregation_eligible(_t, _yp, 49)[0] is False,
        "[음성] 선언 사건 49 < 50 → 자격 없음")
    _yd = [0.5 * x + 0.02 * x * x for x in _t]
    chk(run_verdict(_t, _yd)[0] == NO_VALUE and aggregation_eligible(_t, _yd, 60)[0] is False,
        "[음성] D_inc 가 움직이면(NO_VALUE) 사건이 충분해도 자격 없음")
    _fa = framework_alarm("/nonexistent/dir/msd.json")
    chk(_fa["state"] == "unavailable" and _fa["state"] != "ok",
        "[음성 BQ-6 P1] 골격 분해가 None 이면 'unavailable' — '경보 없음(ok)' 으로 읽지 않는다")

    def run(files_json, *argv):
        """임시 msd.json 들을 만들고 main() 을 돌려 **출력 전체**를 돌려준다."""
        d = _tf.mkdtemp()
        for i, obj in enumerate(files_json):
            sub = pathlib.Path(d) / f"T600_s{i}" / "cfg"
            sub.mkdir(parents=True)
            (sub / "msd.json").write_text(_json.dumps(obj), encoding="utf-8")
        buf = _io.StringIO()
        old = sys.argv
        sys.argv = ["x", "--glob", f"{d}/*/**/msd.json", *argv]
        try:
            with _ctx.redirect_stdout(buf):
                main()
        finally:
            sys.argv = old
        return buf.getvalue()

    # 이상적인 확산 곡선 MSD = 6Dt (β = 1)
    t = [round(0.5 * k, 2) for k in range(1, 201)]          # 0.5 … 100 ps
    lin = {"times_ps": t, "msd_Li_A2": [0.7 * u for u in t], "D_Li_cm2_s": 1.2e-5}
    # 상수 절편: MSD = c + m t (β < 1 이지만 **D 는 무사하다** — 절편이 D_inc 에서 소거된다)
    cage = {"times_ps": t, "msd_Li_A2": [12.0 + 0.7 * u for u in t], "D_Li_cm2_s": 1.2e-5}
    # 진짜 sub-diffusion: MSD = A t^0.6 — D_inc 가 창 따라 **계속 떨어진다**
    subdiff = {"times_ps": t, "msd_Li_A2": [5.0 * u ** 0.6 for u in t], "D_Li_cm2_s": 1.2e-5}
    # plateau 는 오는데 **홉이 모자란** 곡선 — 값은 정의되지만 정밀도가 부족(HOLD)
    thin = {"times_ps": t, "msd_Li_A2": [0.1 * u for u in t], "D_Li_cm2_s": 1.2e-6}
    # ⛔ 문제의 모양: D 는 있는데 MSD 배열이 없다
    nomsd = {"D_Li_cm2_s": 7.4e-6}

    out = run([lin, lin])
    chk("✅ 2개 전부 D_inc plateau" in out, "[양성] 확산 곡선 2개 → ✅")

    # STO 는 있는데 MTO 만 없는 것 — 처방이 정반대라 문구가 갈려야 한다
    stoonly = {"times_ps": t, "msd_Li_A2": [0.7 * u for u in t], "D_Li_cm2_s": 7.4e-6}

    out = run([nomsd, nomsd, nomsd])
    chk("✅" not in out,
        "[음성·핵심] MSD 배열이 없으면 ✅ 를 찍지 않는다 (fail-open 회귀)")
    chk("아무것도 판정하지 않았다" in out,
        "[음성] 전부 못 쟀으면 그렇게 말한다")
    chk("3/3" in out, "[음성] 못 잰 개수를 센다")

    out = run([lin, nomsd])
    chk("✅" not in out, "[음성] 하나만 못 재도 ✅ 로 뭉개지 않는다")
    chk("1/2" in out, "[음성] 섞여 있으면 못 잰 쪽만 센다")

    out = run([stoonly, stoonly], "--mto")
    chk("MTO 곡선 없음" in out,
        "[음성] STO 만 있는데 --mto 를 주면 **그렇게** 말한다 (‘배열 없음’ 아님)")
    chk("--mto` 를 빼면" in out or "--mto" in out,
        "[음성] 다음에 뭘 하면 되는지 알려준다")
    chk("✅" not in out, "[음성] MTO 못 재고 ✅ 로 넘어가지 않는다")
    out = run([stoonly, stoonly])
    chk("✅ 2개 전부 D_inc plateau" in out,
        "[양성] 같은 파일을 --mto 없이 주면 **바로 잰다** (재계산 불필요 확인)")

    # ── ⛔ 회신 AK (2026-08-30) — **β 는 판정이 아니다.** 아래 세 건이 그 회귀시험이다.
    #    kb/concepts/beta-gate.md §7-5 가 2026-08-26 에 β=0.8 을 폐기했는데 이 도구는
    #    나흘간 그대로였고, 그래서 회신 AK 가 폐기된 문턱을 착수 근거로 다시 인용했다.
    out = run([cage, cage])
    chk("✅ 2개 전부 D_inc plateau" in out,
        "[양성·핵심회귀] **상수 절편은 인용 가능하다** — β<1 이어도 D_inc 에서 절편이 "
        "소거된다 (옛 판은 여기서 '인용 금지' 를 찍었다)")
    chk("no-value" not in out,
        "[음성·핵심회귀] 상수 절편을 no-value 로 부르지 않는다")
    out = run([subdiff, subdiff])
    chk("no-value" in out and "D_inc 가 창 따라 움직인다" in out,
        "[음성] 진짜 t^0.6 은 D_inc 가 움직여 **no-value** 다 (β 가 아니라 이게 판정축)")
    chk("✅" not in out, "[음성] sub-diffusion 인데 ✅ 가 같이 찍히지 않는다")
    out = run([thin, thin])
    chk("HOLD" in out and "홉" in out,
        "[음성] plateau 는 왔는데 홉이 모자라면 **HOLD** (정의 실패가 아니다)")
    chk("no-value" not in out,
        "[음성·핵심] HOLD 를 no-value 와 **같은 코드로 합치지 않는다** (처방이 갈린다)")
    chk("✅" not in out, "[음성] HOLD 인데 ✅ 로 넘어가지 않는다")

    # ── 골격(비-Li) 검사 ───────────────────────────────────────────────
    tt = [i * 0.5 for i in range(1, 121)]                       # 0.5 … 60 ps
    def _lin(slope):  return [slope * x for x in tt]
    rigid = {"times_ps": tt, "msd_Li_A2": _lin(1.0),
             "msd_per_elem_A2": {"Li": _lin(1.0), "P": [0.4] * len(tt),
                                 "S": [0.5] * len(tt), "Cl": [0.9] * len(tt)}}
    melting = {"times_ps": tt, "msd_Li_A2": _lin(1.0),
               "msd_per_elem_A2": {"Li": _lin(1.0), "P": _lin(0.02),
                                   "S": _lin(0.05), "Cl": _lin(0.4)}}
    noelem = {"times_ps": tt, "msd_Li_A2": _lin(1.0)}
    nested = {"msd_data": {"times_ps": tt,
                           "msd_per_elem_A2": {"Li": _lin(1.0), "P": [0.3] * len(tt)}}}

    r = framework_check(rigid, 2.0, 50.0)
    chk(r and r["verdict"] == "framework_rigid",
        f"[양성] 평평한 골격은 rigid (worst {r['worst_ratio']:.3f})" if r else "[양성] rigid")
    chk(r and r["worst_el"] == "Cl", "[양성] 가장 큰 골격 원소를 집어낸다 (Cl)")

    m = framework_check(melting, 2.0, 50.0)
    # ★★ codex 반례 회귀시험 (2026-08-20) — **대표 원소만 판정하면 여기서 깨진다.**
    #   양자화가 같은 통에 넣은 두 원소 중 비가 큰 쪽이 대표로 뽑히고, 진짜 fail 인
    #   쪽(P β=0.61)이 판정에서 빠졌다. 이제 전 원소 severity 의 max 로 판정한다.
    _pw = lambda b, a50: [a50 * (x / 50.0) ** b for x in tt]
    cx = {"times_ps": tt, "msd_Li_A2": _lin(1.0),
          "msd_per_elem_A2": {"Li": _lin(1.0), "P": _pw(0.61, 0.5), "S": _pw(0.59, 1.0)},
          "n_atoms_per_elem": {"Li": 24, "P": 8, "S": 41}}
    rcx = framework_check(cx, 2.0, 50.0)
    chk(rcx["verdict"] == "framework_melting",
        f"[음성] ★ codex 반례 — P(β0.61) 가 대표가 아니어도 melting 으로 잡는다 "
        f"(대표 {rcx['worst_el']}, 유발 {rcx['drivers']})")
    chk("P" in rcx["drivers"], "[음성] 판정을 유발한 원소를 drivers 로 보고한다")
    # 비만으로도 fail 이 잡혀야 한다 (β 가 낮아도)
    rr = framework_check({"times_ps": tt, "msd_Li_A2": _lin(1.0),
                          "msd_per_elem_A2": {"Li": _lin(1.0), "S": _pw(0.05, 15.0)},
                          "n_atoms_per_elem": {"Li": 24, "S": 41}}, 2.0, 50.0)
    chk(rr["verdict"] == "framework_melting",
        "[음성] β 가 낮아도 비가 크면 잡는다 (두 축 OR)")

    chk(m and m["verdict"] == "framework_melting",
        f"[음성①] 골격이 선형으로 자라면 melting (worst {m['worst_ratio']:.2f})" if m else "[음성①]")
    chk(m and m["frame"]["Cl"]["beta"] is not None and m["frame"]["Cl"]["beta"] > 0.8,
        "[음성①] 녹는 골격의 β 가 1 근처로 잡힌다")

    # ★★ 표본 크기 — b2o3 의 B 2개 / O 3개가 '최악 원소' 로 뽑히던 실측 결함
    thin_case = {"times_ps": tt, "msd_Li_A2": _lin(1.0),
                 "msd_per_elem_A2": {"Li": _lin(1.0), "B": _lin(0.5),   # 2개, 마구 뜀
                                     "S": [0.5] * len(tt)},            # 41개, 평평
                 "n_atoms_per_elem": {"Li": 58, "B": 2, "S": 41}}
    tc = framework_check(thin_case, 2.0, 50.0)
    chk(tc and tc["worst_el"] == "S",
        "[음성⑤] ★ 2개짜리 B 가 급등해도 **판정은 41개짜리 S 로** 한다 (표본 부족 제외)")
    chk(tc and tc["verdict"] == "framework_rigid",
        "[음성⑤] 그래서 판정은 rigid — 단일 대형 사건에 안 휘둘린다")
    chk(tc and "B" in (tc.get("thin") or []),
        "[양성] 제외한 원소는 thin 에 남겨 보고한다 (조용히 버리지 않는다)")
    # ⛔⛔ 2026-09-10 회귀 — 위 검사는 **반환값**만 봤다. 화면은 죽은 조회
    #   (`r["frame"]["_thin"]`)를 써서 제외 원소를 한 번도 안 찍었다.
    #   함수가 맞아도 화면이 거짓말하면 사람은 화면을 인용한다 ⇒ 문구를 직접 본다.
    chk("B(2" in thin_note(tc), "[음성] 화면 문구에 제외 원소가 **실제로** 나온다")
    chk(thin_note({"thin": [], "frame": {}}) == "",
        "[음성] 제외가 없으면 빈 문구 (없는 괄호를 만들지 않는다)")
    chk(thin_note({"frame": {"B": {"n_atoms": 2, "beta": None}}, "thin": ["B"]}) == "",
        "[음성] β 를 못 잰 원소는 문구에 넣지 않는다")
    chk(thin_note({"frame": {}, "thin": ["Zz"]}) == "",
        "[음성] frame 에 없는 원소 이름에 KeyError 로 죽지 않는다")
    _rows = framework_elem_table(tc)
    chk(any(r.strip().startswith("B ") and "제외(표본부족)" in r for r in _rows),
        "[양성] 원소표가 B 를 '제외(표본부족)' 로 찍는다")
    chk(any(r.strip().startswith("S ") and "판정" in r and "제외" not in r for r in _rows),
        "[양성] 원소표가 S 를 '판정' 으로 찍는다")
    chk(tc and "B" in tc["frame"],
        "[양성] 제외해도 frame 에는 값이 남는다 (참고로 볼 수 있어야 한다)")
    allthin = {"times_ps": tt, "msd_Li_A2": _lin(1.0),
               "msd_per_elem_A2": {"Li": _lin(1.0), "B": _lin(0.5)},
               "n_atoms_per_elem": {"Li": 58, "B": 2}}
    at = framework_check(allthin, 2.0, 50.0)
    chk(at and at["verdict"] == "sample_too_thin",
        "[음성⑥] 판정 가능한 원소가 하나도 없으면 'sample_too_thin' — rigid 로 넘어가지 않는다")
    chk("표본 부족" in framework_verdict_text("sample_too_thin"),
        "[양성] sample_too_thin 문구가 있다")

    chk(framework_check(noelem, 2.0, 50.0) is None,
        "[음성②] **종별 MSD 가 없으면 None** — '골격 안 녹았다'로 넘어가지 않는다")
    chk(framework_check(nested, 2.0, 50.0) is not None,
        "[양성] msd_data 안에 중첩돼 있어도 찾는다 (런 세대 차이)")
    chk(framework_check({"times_ps": tt, "msd_per_elem_A2": {"P": [0.3] * len(tt)}},
                        2.0, 50.0) is None,
        "[음성③] Li 가 없으면 비를 못 내므로 None")
    # ⚠ 문구를 바꾸면 여기가 깨져야 한다 — 2026-08-20 에 "녹고 있다" → "확산 쪽으로 간다"
    #   로 고치면서 이 검사를 안 고쳐 selftest 가 깨진 채로 커밋됐다.
    #   문구 전체가 아니라 **판정 키가 다 문구를 갖는지**를 본다(문구 수정에 안 부서지게).
    _keys = ("framework_rigid", "framework_mobile", "framework_melting", "sample_too_thin")
    chk(all(framework_verdict_text(k) != "판정 불가" and len(framework_verdict_text(k)) > 10
            for k in _keys),
        "[양성] 판정 키 4개가 전부 문구를 갖는다")
    chk("판정 불가" == framework_verdict_text("무엇"),
        "[음성④] 모르는 판정은 '판정 불가' 로 떨어진다")

    # ── --rebuild_mto (2026-08-25) ──────────────────────────────────────────
    #   ⛔ 음성 먼저: **궤적이 없으면 되살릴 수 없다.** None 을 돌려야지 조용히
    #     STO 로 후퇴하면 어느 곡선을 본 건지 모르게 된다 — 이 축의 핵심 규율이다.
    import tempfile as _tf
    with _tf.TemporaryDirectory() as _td:
        _p = os.path.join(_td, "msd.json")
        json.dump({"times_ps": [1, 2, 3], "msd_Li_A2": [1, 2, 3]}, open(_p, "w"))
        chk(mto_from_traj(_p) is None, "[음성] traj.xyz 가 없으면 MTO 재생성은 None")
        _d = json.load(open(_p))
        chk(_curve(_d, mto=True, path=_p, rebuild=True) == (None, None),
            "[음성] rebuild 를 켜도 궤적이 없으면 STO 로 후퇴하지 않는다")
        json.dump({"times_ps_mto": [1, 2], "msd_Li_A2_mto": [5, 6]}, open(_p, "w"))
        _d = json.load(open(_p))
        chk(_curve(_d, mto=True, path=_p, rebuild=True)[1] == [5, 6],
            "[양성] MTO 가 있으면 그대로 쓴다 (재생성 안 함)")

    # ── 결합S/자유S 분류 규약 (2026-08-25 — framework_split) ────────────────
    import numpy as _np
    _syms = ["P", "S", "S", "Cl"]
    _cart = _np.array([[5.0, 5, 5], [7.05, 5, 5], [10.0, 5, 5], [15.0, 5, 5]])
    _g = classify_sulfur(_syms, _cart, _np.eye(3) * 30)
    chk(1 in _g["bonded_S"] and 1 not in _g["free_S"],
        "분류: P 에서 2.05 Å 의 S 는 결합S (b2o3_all_bond_lengths 의 P–S 창 재사용)")
    chk(2 in _g["free_S"], "[음성] 분류: P 에서 5 Å 의 S 는 자유S — 결합을 지어내지 않는다")
    chk(_g["Cl"] == [3], "분류: Cl 은 항상 자유 음이온 그룹")
    # 주기경계 — 셀 반대편이라도 최소이미지로 결합이면 결합S
    _g2 = classify_sulfur(["P", "S"], _np.array([[0.5, 5, 5], [28.45, 5, 5]]),
                          _np.eye(3) * 30)
    chk(1 in _g2["bonded_S"], "[음성] 주기경계 건너 2.05 Å 도 결합S (최소이미지)")

    # ── 단위 그룹: BS₃ / PS₄ (2026-08-25) ──────────────────────────────────
    #   B 는 홀로 n=2 라 컷오프(8) 아래다. 단위로 묶어야 판정 가능해진다.
    _syms3 = ["P", "S", "S", "S", "S", "B", "S", "S", "S", "Cl"]
    _c3 = _np.array([[5., 5, 5], [7.05, 5, 5], [5, 7.05, 5], [5, 5, 7.05], [2.95, 5, 5],
                     [15., 5, 5], [16.8, 5, 5], [15, 6.8, 5], [15, 5, 6.8], [25., 5, 5]])
    _g3 = classify_sulfur(_syms3, _c3, _np.eye(3) * 30)
    chk(_g3["S_on_B"] == [6, 7, 8] and _g3["S_on_P"] == [1, 2, 3, 4],
        "단위: S 를 P 쪽/B 쪽으로 가른다 (같은 S 를 양쪽에 넣지 않는다)")
    chk(_g3["BS3_unit"] == [5, 6, 7, 8] and _g3["PS4_unit"] == [0, 1, 2, 3, 4],
        "단위: BS₃ = B + B결합S, PS₄ = P + P결합S")
    chk(not (set(_g3["BS3_unit"]) & set(_g3["PS4_unit"])),
        "[음성] 단위: 두 단위가 원자를 공유하지 않는다 (공유하면 비가 자기상관)")
    chk(9 not in _g3["BS3_unit"] and 9 not in _g3["PS4_unit"],
        "[음성] 단위: Cl 은 어느 단위에도 안 들어간다")
    # 사전 등록 판정 — 네 갈래 전부 (양성 2 · 음성 2)
    chk(unit_verdict(5.0, 0.10) == "BS3_driven",
        "판정: 비 큼 + PS₄ 굳음 → BS3_driven (도핑 단위가 원인)")
    chk(unit_verdict(1.0, 0.90) == "host_wide",
        "판정: 비 ~1 + PS₄ 도 움직임 → host_wide (계 전체가 무름)")
    chk(unit_verdict(5.0, 0.90) == "both_mobile",
        "[음성] 비만 크다고 BS3_driven 이 되지 않는다 — PS₄ 가 움직이면 both_mobile")
    chk(unit_verdict(1.6, 0.10) == "inconclusive",
        "[음성] 회색지대(1.25<비<2.0)는 판정 안 한다 — 사전 등록 문턱을 사후에 늘리지 않는다")
    chk(unit_verdict(5.0, None) == "inconclusive",
        "[음성] PS₄ β 가 없으면 판정 없음 — 비만으로 결론 내지 않는다")
    chk(unit_verdict(None, 0.10) == "inconclusive",
        "[음성] 비가 없으면 판정 없음")

    # ── D_inc — 절편 없는 축 (2026-08-27, Codex 회신 F) ──────────────────────
    _t = [i * 0.1 for i in range(1, 1001)]                      # 0.1–100 ps
    _cage = [3.0 + 0.6 * x for x in _t]                         # MSD = c + 6Dt, D=0.1
    d1 = d_incremental(_t, _cage, 2, 50); d2 = d_incremental(_t, _cage, 50, 100)
    chk(d1 is not None and d2 is not None and abs(d1 - 0.1) < 1e-6 and abs(d2 - 0.1) < 1e-6,
        "[양성] 상수 절편이면 D_inc 가 창과 무관하게 참값(0.1)이다 — c 가 소거된다")
    _b = [loglog_slope(_t, _cage, lo, hi) for lo, hi in ((2, 50), (50, 100))]
    chk(_b[0] is not None and _b[0] < 0.95 and d1 is not None and abs(d1 - 0.1) < 1e-6,
        "[음성] **같은 곡선에서 β 는 0.95 밑으로 떨어지는데 D_inc 는 정확하다** — "
        "β 가 낮다고 D 가 틀린 게 아니다(게이트 폐기의 근거)")
    _sub = [1.5 * (x ** 0.6) for x in _t]                        # 진짜 t^0.6
    s1 = d_incremental(_t, _sub, 2, 50); s2 = d_incremental(_t, _sub, 50, 100)
    chk(s1 is not None and s2 is not None and s2 < 0.75 * s1,
        "[음성] 진짜 t^0.6 이면 D_inc 가 창 따라 **떨어진다** — 케이지와 갈린다")
    chk(d_incremental([1.0, 2.0], [1.0, 2.0], 0, 100) is None,
        "[음성] 점이 3개 미만이면 None — 두 점으로 기울기를 만들지 않는다")
    chk(d_incremental(_t, _cage, 200, 300) is None,
        "[음성] 창이 궤적 밖이면 None — 빈 구간에서 0 을 반환하지 않는다")

    # ── 회신 S P0 — **부분적으로만 덮이는 창** (종전 fail-open) ────────────────
    #   곡선이 100 ps 에서 끝나는데 창 50–200 을 요청하면 예전에는 50–100 을 맞춰
    #   놓고 라벨만 50–200 을 붙였다. MTO 는 최대 lag 를 T/2 로 자르므로 200 ps
    #   생산런의 최대 lag 가 100 ps 다 — 예외가 아니라 **기본 상황**이었다.
    _t100 = [0.5 * k for k in range(1, 201)]                     # 0.5 … 100.0 ps
    _lin100 = [0.7 * x for x in _t100]
    chk(lin_fit(_t100, _lin100, 50, 200) is None,
        "[음성 S] 곡선이 100 ps 인데 창 50–200 → lin_fit None (잘린 창을 그 라벨로 안 준다)")
    chk(d_incremental(_t100, _lin100, 50, 200) is None,
        "[음성 S] 같은 상황에서 d_incremental 도 None")
    _ok = lin_fit(_t100, _lin100, 50, 100)
    chk(_ok is not None and abs(_ok[0] - 0.7) < 1e-6,
        "[양성 S] 창이 실제로 덮이면(50–100) 그대로 맞춘다 — 정상까지 막지 않는다")
    chk(lin_fit(_t100, _lin100, 2, 100.4) is not None,
        "[양성 S] hi 가 마지막 점을 간격 하나만큼 넘어서는 것은 허용 (격자 끝 반올림)")
    chk(lin_fit(_t100, _lin100, 2, 130) is None,
        "[음성 S] 간격 하나를 넘게 모자라면 거부한다")

    # ── τ_int (2026-08-27, 교차리뷰 H) ───────────────────────────────────────
    try:
        import numpy as _np
        _r = _np.random.default_rng(11)

        def _ar1(phi, n=8000):
            x = _np.zeros(n)
            for i in range(1, n):
                x[i] = phi * x[i - 1] + _r.normal(0, 1)
            return x.tolist()

        for _phi in (0.0, 0.6, 0.8):
            _th = (1 + _phi) / (1 - _phi)          # AR(1) 이론 g
            _t = tau_int_geyer(_ar1(_phi), 1.0)
            chk(_t and abs(_t["g"] - _th) < max(0.3, 0.35 * _th),
                f"[양성] AR(1) φ={_phi} 의 g 를 회수한다 ({_t['g']:.2f} vs 이론 {_th:.2f})")
        _t = tau_int_geyer(_ar1(0.8), 1.0)
        chk(abs(_t["block_min_ps"] - 2 * _t["tau_int_ps"]) < 1e-9,
            "[음성] ⚠**factor-2 함정** — block_min_ps 가 이미 2·τ_int 다. "
            "호출자가 2 를 또 곱할 여지를 함수가 없앤다 (회신 H 경고)")
        _t = tau_int_geyer(_ar1(-0.7), 1.0)
        chk(_t["g"] <= 1.01 and _t["memory_horizon_ps"] > 10,
            f"[음성] **반상관에서 g 만 보면 놓친다** — g={_t['g']:.2f}(바닥)인데 "
            f"memory_horizon={_t['memory_horizon_ps']:.0f} ps 다 (back-jump 사례)")
        chk(tau_int_geyer([1, 2, 3], 1.0) is None,
            "[음성] 표본 16개 미만이면 None — 짧은 계열에서 τ 를 지어내지 않는다")
        chk(tau_int_geyer([5.0] * 100, 1.0) is None,
            "[음성] 분산 0 이면 None — 상수열에서 0 으로 나누지 않는다")
    except ImportError:
        print("  · (numpy 없음 — τ_int selftest 건너뜀)")

    # ── 방향별 확산텐서 (2026-08-27, 교차리뷰 G/H) ──────────────────────────
    chk(directional_msd_tensor("/does/not/exist/traj.xyz") is None,
        "[음성] 궤적 파일이 없으면 None — 빈 텐서를 만들지 않는다")
    try:
        import numpy as _np
        from ase import Atoms as _At
        from ase.io import write as _w
        import tempfile as _tf
        _rng = _np.random.default_rng(3)
        _d = pathlib.Path(_tf.mkdtemp())
        # 축별 D 를 다르게 준 브라운 운동 — 축당 분산 2·D·t 이므로 slope/2 = D
        _D = _np.array([0.40, 0.40, 0.10]); _n, _ni, _dt = 400, 40, 0.1
        _p = _np.cumsum(_rng.normal(0, 1, (_n, _ni, 3)) * _np.sqrt(2 * _D * _dt), axis=0)
        _w(str(_d / "traj.xyz"),
           [_At("Li" * _ni, positions=q, cell=[40, 40, 40], pbc=True) for q in _p])
        _got = directional_msd_tensor(_d / "traj.xyz", save_fs=100.0)
        chk(_got is not None, "[양성] 궤적에서 텐서를 낸다")
        if _got:
            _t, _M = _got
            def _sl(s):
                _i = [k for k, x in enumerate(_t) if 2 <= x <= 15]
                _x = [_t[k] for k in _i]; _y = [s[k] for k in _i]
                _N = len(_x); _sx = sum(_x); _sy = sum(_y)
                return ((_N * sum(p * q for p, q in zip(_x, _y)) - _sx * _sy)
                        / (_N * sum(p * p for p in _x) - _sx * _sx) / 2.0)
            _dd = [_sl(_M[k][k]) for k in range(3)]
            chk(all(abs(_dd[k] - _D[k]) < 0.5 * _D[k] for k in range(3)),
                f"[양성] 축별 D 를 50 % 안에서 회수한다 ({_dd[0]:.2f}/{_dd[1]:.2f}/{_dd[2]:.2f} "
                f"vs 참값 0.40/0.40/0.10)")
            chk(_dd[0] / _dd[2] > 2.0,
                "[음성] **이방을 등방으로 뭉개지 않는다** — z 가 x 보다 확실히 작다")
            _off = max(abs(_sl(_M[i][j])) for i, j in ((0, 1), (0, 2), (1, 2)))
            chk(_off < 0.3 * max(_dd),
                "[음성] 축이 독립이면 비대각이 대각보다 훨씬 작다 — 상관을 지어내지 않는다")
        # ★ wrap 거부 — kgy EN_0717/licube 가 D=3e6 Å²/ps 를 낸 실측이 계기다
        _pw = _p % 40.0                                     # 주기상자로 접는다
        _w(str(_d / "wrapped.xyz"),
           [_At("Li" * _ni, positions=q, cell=[40, 40, 40], pbc=True) for q in _pw])
        chk(directional_msd_tensor(_d / "wrapped.xyz", save_fs=100.0) is None,
            "[음성] ⛔**wrap 된 궤적을 거부한다** — 상자 가로지르기를 확산으로 재지 않는다 "
            "(EN_0717/licube 가 3e6 Å²/ps 를 냈던 그 상황)")
        chk(directional_msd_tensor(_d / "traj.xyz", save_fs=100.0) is not None,
            "[양성] 같은 궤적의 **unwrap 판은 그대로 통과**한다 — 정상까지 막지 않는다")
        chk(directional_msd_tensor(_d / "traj.xyz", save_fs=100.0, prefix_ps=0.5) is None,
            "[음성] prefix 가 너무 짧으면 None — 프레임 20개 미만은 재지 않는다")
        # 회신 S P0 — 궤적보다 긴 prefix. `frames[:keep]` 이 조용히 전체를 돌려줘서
        #   서로 다른 prefix 행이 **같은 값**으로 찍혔다 (실측 kgy lpsocl_md/licube 5행 동일).
        _short = directional_msd_tensor(_d / "traj.xyz", save_fs=100.0, prefix_ps=1e6)
        chk(isinstance(_short, dict) and "__short__" in _short,
            "[음성 S] 궤적보다 긴 prefix → 잘린 값 대신 __short__ 표식 "
            f"(실제 {_short.get('__short__', float('nan')):.2f} ps)")
        _full = directional_msd_tensor(_d / "traj.xyz", save_fs=100.0, prefix_ps=None)
        chk(_full is not None and not isinstance(_full, dict),
            "[양성 S] prefix 없이는 그대로 잰다 — 정상 경로를 막지 않는다")
        chk(directional_msd_tensor(_d / "traj.xyz", save_fs=100.0, species="Xx") is None,
            "[음성] 없는 원소를 달라면 None — 빈 배열로 0 을 반환하지 않는다")

        # ── 결정축 투영 (비직교) ─────────────────────────────────────────
        # ⚠ **크기가 아니라 성질**을 검사한다. 60이온·600프레임에서 D 는 15–30 % 흔들려
        #   숫자 일치로 검사하면 잡음에 걸려 깨진다. 견고한 것은 ① 등방은 어느 기저에서도
        #   등방 ② 억제한 방향이 억제된 칸으로 나온다 ③ 직교 셀에서는 두 기저가 같다.
        _Cn = _np.array([[20., 0., 0.], [0., 20., 0.], [10., 0., 30.]])   # 비직교
        _ci = cell_axis_info(_Cn)
        chk(_ci and _ci[2] > 1.0,
            f"[양성] cell_axis_info 가 비직교를 잡는다 (비대각 {_ci[2]:.1f} Å)")
        chk(_ci and abs(_ci[0][2] - 30.0) < 1e-6,
            "[양성] 수직폭을 |c| 가 아니라 V/|a×b| 로 낸다 — 유한크기를 정하는 쪽이다")

        def _mk(path, supp):
            _s = _r.normal(0, 1, (600, 60, 3)) * _np.sqrt(2 * 0.30 * 0.1)
            if supp is not None:                      # 역격자 세 번째 방향만 억제
                _rc = _np.cross(_Cn[0], _Cn[1]); _k = _rc / _np.linalg.norm(_rc)
                _s = _s + (supp - 1.0) * _np.outer(_s @ _k, _k).reshape(_s.shape)
            _w(str(path), [_At("Li" * 60, positions=q, cell=_Cn, pbc=True)
                           for q in _np.cumsum(_s, axis=0)])

        def _ratio(path, cry):
            _g = directional_msd_tensor(path, save_fs=100.0,
                                        basis="crystal" if cry else "cartesian")
            _t2, _M2 = _g
            _i = [k for k, x in enumerate(_t2) if 2 <= x <= 20]
            def _sl(s):
                _x = [_t2[k] for k in _i]; _y = [s[k] for k in _i]; _N = len(_x)
                _sx = sum(_x)
                return ((_N * sum(p * q for p, q in zip(_x, _y)) - _sx * sum(_y))
                        / (_N * sum(p * p for p in _x) - _sx * _sx) / 2.0)
            _dd = [_sl(_M2[k][k]) for k in range(3)]
            return max(_dd) / min(_dd), _dd

        _mk(_d / "iso.xyz", None)
        _mk(_d / "slow.xyz", 0.5)                     # 그 방향 D 를 1/4 로
        for _cry in (False, True):
            _ri, _ = _ratio(_d / "iso.xyz", _cry)
            chk(_ri < 1.5, f"[양성] 등방은 {'결정축' if _cry else 'Cartesian'} 기저에서도 "
                           f"등방이다 (비 {_ri:.2f})")
            _rs, _ds = _ratio(_d / "slow.xyz", _cry)
            chk(_rs > 2.5, f"[음성] 한 방향만 억제하면 **뭉개지 않고 잡아낸다** "
                           f"({'결정축' if _cry else 'Cartesian'} 비 {_rs:.2f})")
            chk(_ds.index(min(_ds)) == 2,
                f"[음성] 억제한 방향이 **맞는 칸**에 나온다 (3번째, "
                f"{'결정축' if _cry else 'Cartesian'})")
        import shutil as _sh; _sh.rmtree(_d, ignore_errors=True)
    except ImportError:
        print("  · (ase/numpy 없음 — 방향별 텐서 selftest 건너뜀)")


    # ★★ 실측회귀 (2026-08-28) — kept_frac 은 **비율**이라 골격이 안 움직이면 뜻을 잃는다.
    #   modelc 9개 중 8개가 골격 β 로는 rigid(−0.05~0.27)인데 이 검사에서
    #   "재배열 — 구제 불가" 로 찍혔다. **같은 실행의 두 검사가 정반대**를 말한 것이 신호였다.
    def _drift(ft, fi):
        kept = fi / ft
        if ft < DRIFT_MIN_MSD:
            return "framework_static"
        return ("drift_dominated" if kept <= DRIFT_KEEP else
                "rearrangement" if kept >= DRIFT_LOST else "mixed")
    chk(_drift(0.4, 0.4) == "framework_static",
        "[골격COM·실측회귀] 골격 MSD 0.4 Å²(진동)은 **판정 안 함** — 옛 판은 '재배열'이었다")
    chk(_drift(0.7, 0.6) == "framework_static", "[골격COM·실측회귀] 0.7 Å² 도 마찬가지")
    chk(_drift(5.5, 5.5) == "rearrangement",
        "[골격COM·양성] 골격이 실제로 크게 움직이면 여전히 재배열로 잡는다")
    chk(_drift(10.0, 1.0) == "drift_dominated",
        "[골격COM·양성] COM 을 빼서 대부분 사라지면 흐름 지배다")
    chk(_drift(10.0, 5.0) == "mixed", "[골격COM] 중간은 중간이라 말한다")
    # ── D_inc plateau · 실패 두 층 (2026-08-30, 회신 AK) ─────────────────────
    _tt = [round(0.5 * k, 2) for k in range(1, 201)]              # 0.5 … 100 ps
    _flat = [12.0 + 0.7 * u for u in _tt]                          # 상수 절편
    _pow = [5.0 * u ** 0.6 for u in _tt]                           # 진짜 t^0.6
    _pl = dinc_plateau(_tt, _flat)
    chk(_pl["status"] == "plateau" and _pl["spread"] < 1e-9,
        f"[plateau·양성] 상수 절편이면 D_inc 산포 0 ({_pl['spread']:.1e})")
    _ps = dinc_plateau(_tt, _pow)
    chk(_ps["status"] == "drifting" and _ps["trend"] < 0,
        f"[plateau·음성] t^0.6 은 D_inc 가 **떨어진다** (추세 {_ps['trend']:+.0%})")
    chk(dinc_plateau([1.0, 2.0, 3.0], [1.0, 2.0, 3.0])["status"] == "insufficient",
        "[plateau·음성] 창을 못 채우면 'insufficient' — 평평하다고 하지 않는다")
    chk(dinc_plateau(_tt, [0.0] * len(_tt))["status"] == "insufficient",
        "[plateau·음성] 기울기 0 (D_inc≤0) 은 세지 않는다 — 0 으로 '평평' 을 만들지 않는다")
    # ── 내부리뷰 AX P1-2 (2026-09-04) — **짝수 창** median 편향 회귀 ────────────
    #   지금까지 실물이 항상 3창(200 ps 라 (50,100) 이 빠졌다)이라 짝수 경로가
    #   **한 번도 안 돌았다.** 생산길이를 늘려 4창이 되는 순간 드러난다.
    _ev = [0.122, 0.117, 0.107, 0.100]
    _sv = sorted(_ev)
    _med_true = (_sv[1] + _sv[2]) / 2.0
    _med_old = _sv[2]                       # 옛 구현: 위쪽 중앙값
    chk(abs(_med_true - 0.112) < 1e-9 and abs(_med_old - 0.117) < 1e-9,
        f"[plateau·짝수] 옛 med {_med_old} 는 진짜 median {_med_true} 보다 **크다**")
    chk((max(_ev) - min(_ev)) / _med_true > (max(_ev) - min(_ev)) / _med_old,
        "[plateau·음성] 옛 median 은 spread 를 **작게** 만든다 = 통과 쪽 편향")
    # 실제 함수가 짝수 창에서 진짜 median 을 쓰는가 — 4창이 다 차는 t 범위로 친다
    _t4 = [round(0.5 * k, 2) for k in range(1, 401)]              # 0.5 … 200 ps
    _f4 = [12.0 + 0.7 * u for u in _t4]
    _p4 = dinc_plateau(_t4, _f4)
    chk(_p4["n"] == 4, f"[plateau·짝수] 400 ps 궤적이면 창 4개가 다 찬다 (n={_p4['n']})")
    chk(_p4["status"] == "plateau" and _p4["spread"] < 1e-9,
        "[plateau·짝수·양성] 상수 절편은 4창에서도 산포 0")
    chk(run_verdict(_tt, _flat)[0] == CITABLE,
        "[판정·핵심회귀] 상수 절편 = **인용 가능** (β<1 이어도)")
    chk(run_verdict(_tt, _pow)[0] == NO_VALUE,
        "[판정·음성] 진짜 sub-diffusion = no_value")
    chk(run_verdict(_tt, [0.1 * u for u in _tt])[0] == HOLD,
        "[판정·음성] plateau 인데 홉 부족 = **HOLD** (no_value 아님)")
    chk(run_verdict([], [])[0] == NO_VALUE,
        "[판정·음성] 궤적이 없으면 no_value")
    chk(NO_VALUE != HOLD,
        "[판정·음성] '정의되지 않음' 과 '정밀도 부족' 은 **다른 코드**다 (회신 AK Q5)")
    chk(run_verdict(_tt, _flat, beta=0.55)[0] == CITABLE,
        "[판정·핵심회귀] **β 를 낮게 줘도 판정이 안 바뀐다** — β 는 판정에 안 들어간다")

    # ── Haven 비 (2026-09-07) — **답을 아는 합성 궤적**으로 검증한다 ─────────
    #   실제 궤적으로는 "그럴듯한 수" 가 나와도 맞는지 알 수 없다. 세 극한은 해석적으로
    #   정해져 있으므로 추정기가 그걸 재현하는지가 유일한 진짜 검사다.
    import numpy as _np
    _rng = _np.random.default_rng(0)
    _NT, _N, _DT = 4000, 40, 0.1                      # 4000 프레임 · Li 40 · 0.1 ps

    def _hr(steps):
        """변위 증분 (nt-1, N, 3) → H_R. COM 제거는 끄고(합성계는 드리프트 0) 순수 검사."""
        pos = _np.concatenate([_np.zeros((1, _N, 3)), _np.cumsum(steps, axis=0)])
        tau, mt, mc, _ = haven_curves(pos, _DT)
        st, sc = lin_fit(tau, mt, 5.0, 100.0), lin_fit(tau, mc, 5.0, 100.0)
        return st[0] / sc[0] if (st and sc and sc[0]) else None

    # ① 독립 랜덤워크 → H_R = 1 (정의상)
    _ind = _rng.normal(0, 1, (_NT, _N, 3))
    _h1 = _hr(_ind)
    chk(_h1 is not None and abs(_h1 - 1.0) < 0.25,
        f"[Haven·양성] 독립 랜덤워크 → H_R ≈ 1 (측정 {_h1:.3f})")

    # ② 완전 상관(전 이온이 같이 움직임) → Σ Δr = N·Δr ⇒ MSD_σ = N·MSD* ⇒ H_R = 1/N
    _coh = _np.repeat(_rng.normal(0, 1, (_NT, 1, 3)), _N, axis=1)
    _h2 = _hr(_coh)
    chk(_h2 is not None and abs(_h2 * _N - 1.0) < 0.25,
        f"[Haven·양성] 완전 상관 → H_R = 1/N = {1/_N:.4f} (측정 {_h2:.4f})")

    # ③ 짝 반상관(i 와 i+1 이 반대) → Σ Δr ≡ 0 ⇒ D_σ 가 잡음 바닥
    #   ⛔ 여기서 **큰 유한수를 뱉으면 안 된다** — H_R 은 정의되지 않는다.
    _a = _rng.normal(0, 1, (_NT, _N // 2, 3))
    _anti = _np.concatenate([_a, -_a], axis=1)
    _pa = _np.concatenate([_np.zeros((1, _N, 3)), _np.cumsum(_anti, axis=0)])
    _ta, _mta, _mca, _ = haven_curves(_pa, _DT)
    _sc = lin_fit(_ta, _mca, 5.0, 100.0)
    chk(_sc is not None and (_sc[0] <= 0 or _sc[2] < 0.5),
        f"[Haven·음성] 반상관이면 D_σ 적합이 무너진다 — 큰 유한수가 아니라 **미정**이다 "
        f"(기울기 {_sc[0]:.3e} · R² {_sc[2]:.3f})")

    # ④ ⛔음성: 두 극한이 **실제로 갈린다** (추정기가 상수를 뱉으면 위가 다 통과할 수 있다)
    chk(_h2 < _h1, f"[Haven·음성] 완전상관 {_h2:.4f} < 독립 {_h1:.3f} — 추정기가 상수가 아니다")

    # ⑤ ⛔음성: 프레임이 모자라면 **빈 결과**를 준다 (조용히 H_R=1 을 만들지 않는다)
    chk(haven_curves(_np.zeros((4, _N, 3)), _DT) == ([], [], [], []),
        "[Haven·음성] 프레임 8개 미만이면 빈 결과 — 1.0 을 지어내지 않는다")
    chk(haven_curves(_np.zeros((100, 0, 3)), _DT) == ([], [], [], []),
        "[Haven·음성] 이온이 0개면 빈 결과 (0 나눗셈 대신)")

    # ⑥ ⛔음성 **핵심** — 기준을 잘못 잡으면 신호가 지워진다.
    #   Li 40 + 골격 60 짜리 계에 전 계 등속 표류를 얹는다.
    #     · 기준 없음        → 표류가 집단좌표를 지배 → H_R 붕괴
    #     · 골격 COM 기준    → 복구 (H_R ≈ 1)
    #     · **전 원자 COM**  → Li 가 40 % 섞여 들어가 신호를 갉아먹는다 (첫 판의 버그)
    _NF = 60
    _dr = _np.zeros((_NT, 1, 3)); _dr[:, :, 0] = 0.5
    _li_s = _rng.normal(0, 1, (_NT, _N, 3)) + _dr
    _fw_s = _rng.normal(0, 0.05, (_NT, _NF, 3)) + _dr      # 골격은 거의 안 움직인다
    _P = lambda st_: _np.concatenate([_np.zeros((1, st_.shape[1], 3)), _np.cumsum(st_, axis=0)])
    _pl, _pf = _P(_li_s), _P(_fw_s)
    _pall = _np.concatenate([_pl, _pf], axis=1)

    def _hr2(ref):
        t_, mt_, mc_, _ = haven_curves(_pl, _DT, cart_ref=ref)
        f1, f2 = lin_fit(t_, mt_, 5, 100), lin_fit(t_, mc_, 5, 100)
        return (f1[0] / f2[0]) if (f1 and f2 and f2[0] > 0) else None

    _hno, _hfw, _hall = _hr2(None), _hr2(_pf), _hr2(_pall)
    chk(_hno is not None and _hno < 0.2,
        f"[Haven·음성] 기준을 안 빼면 표류가 집단좌표를 지배한다 (H_R {_hno:.4f})")
    chk(_hfw is not None and abs(_hfw - 1.0) < 0.30,
        f"[Haven·양성] **골격 COM** 기준이면 복구된다 (H_R {_hfw:.3f})")
    chk(_hall is not None and _hall > _hfw * 1.15,
        f"[Haven·음성·핵심] **전 원자 COM** 기준은 Li 신호를 갉아먹어 H_R 을 과대하게 만든다 "
        f"(골격 {_hfw:.3f} → 전원자 {_hall:.3f}) — 첫 판의 버그다")

    # ⑦ ⛔음성 **끝단(end-to-end)** — 위 ①~⑥ 은 순수 함수만 봤다. 실제 실패는
    #   **파일 경로**에서 났다: `_read` 가 다른 함수의 지역 import 라 NameError 였고,
    #   `mto_from_traj` 는 `except BaseException` 이 그걸 삼켜 "traj 읽기 실패" 로만 찍혔다.
    #   ⇒ 수학만 시험하고 I/O 를 안 시험하면 도구가 원격에서 죽는다. 합성 궤적을 실제로 쓴다.
    import tempfile as _tf, os as _os
    with _tf.TemporaryDirectory() as _td:
        _rd = _os.path.join(_td, "T600_s2"); _os.makedirs(_rd)
        _json.dump({"T_K": 600}, open(_os.path.join(_rd, "msd.json"), "w"))
        _nl, _nf, _nfr = 6, 6, 400
        _st = _rng.normal(0, 0.30, (_nfr, _nl, 3))            # Li: 독립 확산 → H_R ≈ 1
        _pli = _np.concatenate([_np.zeros((1, _nl, 3)), _np.cumsum(_st, axis=0)])
        with open(_os.path.join(_rd, "traj.xyz"), "w") as _fh:
            for _k in range(_nfr + 1):
                _fh.write(f"{_nl + _nf}\nFrame {_k}\n")
                for _i in range(_nl):
                    _fh.write("Li %.5f %.5f %.5f\n" % tuple(_pli[_k, _i]))
                for _i in range(_nf):                          # 골격: 고정
                    _fh.write("S %.5f %.5f %.5f\n" % (_i * 2.0, _i * 1.5, 0.0))
        try:
            _r = haven_from_traj(_os.path.join(_rd, "msd.json"),
                                 save_fs=100.0, lo=1.0, hi=15.0)
            _err = None
        except BaseException as _e:                            # noqa: BLE001
            _r, _err = None, f"{type(_e).__name__}: {_e}"
        chk(_err is None,
            f"[Haven·끝단] haven_from_traj 가 예외 없이 돈다 ({_err or 'OK'})")
        chk(_r is not None and _r.get("haven_ratio") is not None,
            "[Haven·끝단·음성] **traj.xyz 를 실제로 읽는다** — None 으로 조용히 빠지지 않는다")
        if _r and _r.get("haven_ratio"):
            chk(0.5 < _r["haven_ratio"] < 2.0,
                f"[Haven·끝단] 독립 확산 합성 궤적 → H_R ≈ 1 (측정 {_r['haven_ratio']:.3f})")
            chk(_r.get("drift_reference", "").startswith("framework"),
                f"[Haven·끝단] 드리프트 기준이 **골격** 이라고 기록된다 ({_r.get('drift_reference')})")
        # 같은 구멍을 공유하던 mto_from_traj 도 함께 본다
        _m = mto_from_traj(_os.path.join(_rd, "msd.json"), save_fs=100.0, cache=False)
        chk(_m is not None and _m.get("msd_Li_A2_mto"),
            "[MTO·끝단·회귀] --rebuild_mto 경로도 궤적을 실제로 읽는다 "
            "(2026-09-07 이전엔 NameError 를 except 가 삼켜 조용히 실패)")

    # ── save_fs 해석 (2026-09-10) ────────────────────────────────────────
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        tdp = pathlib.Path(td)
        mj = tdp / "msd.json"; mj.write_text("{}")
        v, a, src = resolve_save_fs(mj)
        chk((v, a) == (100.0, True), "sidecar 가 없으면 100 fs 를 **가정이라고 밝히고** 쓴다")
        (tdp / "aimd_results.json").write_text(json.dumps({"T_K": 800, "save_fs": 50.0}))
        v, a, src = resolve_save_fs(mj)
        chk((v, a, src) == (50.0, False, "aimd_results.json"), "sidecar 의 save_fs 를 읽는다 (가정 아님)")
        # ⛔음성: 옛 판의 94바이트 빈 sidecar — save_fs 키가 없다
        (tdp / "aimd_results.json").write_text(json.dumps({"T_K": 800}))
        v, a, src = resolve_save_fs(mj)
        chk((v, a) == (100.0, True), "[음성] save_fs 없는 빈 sidecar 를 값으로 읽지 않는다")
        # ⛔음성: 깨진 json 을 예외로 터뜨리지 않고 가정으로 떨어진다
        (tdp / "aimd_results.json").write_text("{not json")
        v, a, src = resolve_save_fs(mj)
        chk((v, a) == (100.0, True), "[음성] 깨진 sidecar 에서 터지지 않는다")
        # ⛔음성: 호출자가 준 값이 sidecar 를 이긴다 (명시가 추론을 이긴다)
        (tdp / "aimd_results.json").write_text(json.dumps({"save_fs": 50.0}))
        v, a, src = resolve_save_fs(mj, 20.0)
        chk((v, a) == (20.0, False), "[음성] 호출자 지정이 sidecar 를 이긴다")
    # ── 런 내부 오차 (2026-09-22, 회신 BT) — **음성 경로가 본체다** ────────────
    #   회신 BS §6 에서 내가 창끝 MSD 를 궤적 전체 공식에 넣어 N_eff 를 8 배
    #   과소평가했다. 코드는 그 계산을 한 적이 없지만, 여기서 같은 실수를 하면
    #   이번엔 **숫자가 실제로 나간다.**
    chk(abs(he2018_neff(48, 24.0) - 128.0) < 1e-9,
        "N_eff = n_Li·max(MSD)/a² (48·24/9 = 128)")
    chk(he2018_neff(48, None) is None and he2018_neff(48, 0.0) is None
        and he2018_neff(0, 24.0) is None,
        "[음성] N_eff: max(MSD) 가 None/0 이거나 n_Li 가 0 이면 **None** (0 이 아니다)")
    chk(abs(he2018_rsd(128) - (3.43 / 128 ** 0.5 + 0.04)) < 1e-12,
        "RSD = 3.43/√N_eff + 0.04 (He 식 9)")
    chk(he2018_rsd(0) is None and he2018_rsd(None) is None,
        "[음성] RSD: N_eff 가 0/None 이면 None (0 으로 나누지 않는다)")
    _ln = lognormal_from_rsd(0.30)
    chk(_ln and _ln["lo68"] < 1.0 < _ln["hi68"] and _ln["median_over_mean"] < 1.0,
        "로그정규: 구간이 평균 1 을 감싸고 **중앙값 < 평균** (오른쪽 치우침)")
    chk(lognormal_from_rsd(0.90)["lo68"] > 0.0,
        "[음성] RSD 0.9 에서도 하한이 **양수** — 대칭 2σ 는 여기서 음수가 된다")
    # ⛔음성(핵심): RSD > 0.30 이면 대칭 ± 를 **막는다**
    _hi = rsd_report({"n_Li": 48, "msd_max_A2": 24.0})          # RSD ≈ 0.343
    _lo = rsd_report({"n_Li": 48, "msd_max_A2": 400.0})         # RSD ≈ 0.10
    chk(_hi["symmetric_pm_allowed"] is False and "why" in " ".join(_hi.keys()),
        "[음성] **RSD > 0.30 이면 대칭 ± 를 막고 이유를 적는다**")
    chk(_lo["symmetric_pm_allowed"] is True,
        "[음성] RSD 가 작으면 막지 않는다 — 정상까지 막으면 도구가 안 쓰인다")
    chk(_hi["sigma_boot"] is None and "못 구했다" in _hi.get("sigma_boot_why", ""),
        "[음성] 부트스트랩이 없으면 **'못 구했다'** 를 적는다 (0 이 아니다)")
    chk("미검증" in _hi.get("rsd_he2018_note", ""),
        "[음성] He 식 열에 **'lag 창 제한 적합에 미검증'** 단서가 붙는다")
    # ⛔음성: 옛 기록(msd_max_A2 없음)은 배열에서 되살린다
    _old = rsd_report({"n_Li": 48, "msd_Li_A2": [0.0, 5.0, 24.0, 11.0]})
    chk(_old["msd_max_A2"] == 24.0 and abs(_old["n_eff_he2018"] - 128.0) < 1e-9,
        "[음성] 2026-09-22 이전 기록도 msd 배열에서 max 를 되살린다")
    # ── 블록 부트스트랩 ────────────────────────────────────────────────
    import numpy as _np
    _rng = _np.random.default_rng(0)
    _t = _np.arange(0, 60.0, 1.0)
    _A = _np.array([2.0 * _t * (1 + 0.05 * _rng.standard_normal()) for _ in range(40)])
    _b = block_bootstrap_D(_A, _t, 2.0, 50.0, block=4, n_boot=120, seed=1)
    chk(_b and _b["sigma_D"] > 0 and _b["lo68"] < _b["hi68"],
        "부트스트랩: σ_D > 0 이고 구간이 정렬돼 있다")
    chk(_b["block"] == 4 and _b["n_origin"] == 40,
        "[음성] block·n_origin 을 **기록한다** (재현 못 하면 숫자가 아니다)")
    chk(block_bootstrap_D(_A[:1], _t, 2.0, 50.0, block=4) is None,
        "[음성] 원점이 1 개면 None — 부트스트랩을 흉내내지 않는다")
    chk(block_bootstrap_D(_A, _t, 200.0, 300.0, block=4) is None,
        "[음성] 창에 점이 3 개 미만이면 None")
    _b1 = block_bootstrap_D(_A, _t, 2.0, 50.0, block=1, n_boot=120, seed=1)
    chk(_b1 and _b1["sigma_D"] > 0,
        "[음성] block=1 도 돈다 (낱개 추출 — 상관을 무시하므로 σ 가 작게 나온다)")
    _same = _np.array([2.0 * _t for _ in range(12)])          # 원점이 전부 동일
    _bs = block_bootstrap_D(_same, _t, 2.0, 50.0, block=3, n_boot=60, seed=2)
    chk(_bs and _bs["sigma_D"] == 0.0,
        "[음성] 원점이 전부 같으면 σ_D = **정확히 0** (산포는 원점 간에서만 온다)")

    # ── 회신 BU ①: 블록 길이 plateau 규칙 ─────────────────────────────
    _cur = [(1, 1.0), (2, 1.6), (3, 2.2), (4, 2.50), (5, 2.52), (6, 2.53), (8, 2.54)]
    _pl = choose_block_plateau(_cur)
    chk(_pl["block"] == 4 and abs(_pl["sigma"] - 2.50) < 1e-12,
        "plateau: 연속 3 점 상대변화 ≤5 % 인 **최소 b** 를 고른다 (b=4)")
    chk(choose_block_plateau([(1, 1.0), (2, 1.2), (3, 1.5), (4, 1.9), (5, 2.4)])["block"] is None,
        "[음성] 단조 상승이면 **b 를 고르지 않는다** (판정 보류)")
    _two = [(1, 1.0), (2, 2.0), (3, 2.02), (4, 3.0), (5, 4.0)]
    chk(choose_block_plateau(_two)["block"] is None,
        "[음성] **연속 2 점**만 평평하면 안 고른다 — run=3 이 실제로 강제된다")
    chk(choose_block_plateau(_two, run=2)["block"] == 2,
        "[음성] run=2 로 주면 같은 곡선에서 b=2 를 고른다 — run 이 배선돼 있다")
    chk(choose_block_plateau([(1, 1.0), (2, 1.0)])["block"] is None
        and "볼 수 없다" in choose_block_plateau([(1, 1.0), (2, 1.0)])["why"],
        "[음성] 점이 run 보다 적으면 **못 본다**고 말한다 (평평해 보여도 안 고른다)")
    chk("plateau 없음" in choose_block_plateau(
        [(1, 1.0), (2, 1.2), (3, 1.5), (4, 1.9), (5, 2.4)])["why"],
        "[음성] 못 고른 이유를 문장으로 남긴다")
    #: 가드 ① 몬테카를로 바닥 — 2026-09-22 실측(B=150 → b=12, B=3000 → b=7)에서 나왔다
    _mc = choose_block_plateau(_cur, n_boot=150)
    chk(_mc["block"] is None and "복제가 모자란다" in _mc["why"] and "B ≥" in _mc["why"],
        "[음성] 복제가 적으면 **고르지 않는다** — tol 이 MC 바닥에 잠기면 잡음이 통과한다")
    chk(choose_block_plateau(_cur, n_boot=10000)["block"] == 4,
        "[음성] 복제가 충분하면 같은 곡선에서 정상적으로 b 를 고른다")
    #: ⭐ 개정 2026-09-22 — b 당 정규화. **개정의 안전성 주장을 시험이 직접 검사한다.**
    _gap = choose_block_plateau([(1, 1.0), (2, 1.6), (4, 2.50), (6, 2.52), (8, 2.53)])
    chk(_gap["block"] == 4 and _gap["gaps"] == [2, 2] and "confirm_at_spacing_1" in _gap,
        "[개정] 성긴 사다리도 **b 당 정규화로 판정한다** — 기권 대신 주의를 단다")
    chk(all(abs(p - r / 2.0) < 1e-12 for p, r in zip(_gap["rel_per_b"], _gap["rel_changes"])),
        "[개정] Δb=2 면 b 당 값이 원 상대변화의 **정확히 1/2** 이다 (정규화가 실제로 돈다)")
    #: ⭐⭐ 개정의 **핵심 주장**: Δb == 1 이면 원 규칙과 수식이 같다 ⇒ 답이 안 바뀐다.
    #:    이 줄이 없으면 "안전하다" 는 말이 시험되지 않은 주장으로 남는다.
    chk(all(abs(p - r) < 1e-12 for p, r in zip(_pl["rel_per_b"], _pl["rel_changes"]))
        and _pl["block"] == 4,
        "[개정·핵심] **연속 정수 사다리에서는 정규화판과 원 규칙이 동일하다** (답 불변)")
    #: 성겨도 진짜로 안 평평하면 여전히 안 고른다 — 정규화가 문턱을 헐겁게 만들지 않는다
    _gap_rise = choose_block_plateau([(1, 1.0), (3, 1.5), (5, 2.2), (7, 3.1)])
    chk(_gap_rise["block"] is None and "plateau 없음" in _gap_rise["why"],
        "[음성] 성긴 사다리라도 **실제로 오르면 안 고른다** (정규화 ≠ 문턱 완화)")
    chk(choose_block_plateau([(2, 1.0), (2, 1.0), (3, 1.0)])["block"] is None,
        "[음성] b 가 중복이면 Δb=0 이라 **나눗셈을 하지 않고** 판정을 포기한다")
    _sc = block_sigma_curve(lambda b: None if b == 3 else float(b), [2, 3, 4])
    chk(_sc == [(2, 2.0), (4, 4.0)],
        "[음성] σ 를 못 낸 b 는 곡선에서 **빠진다** (0 으로 안 채운다)")
    chk(block_sigma_curve(lambda b: 1 / 0, [2, 3]) == [],
        "[음성] σ 계산이 터져도 곡선이 비는 것으로 끝난다 (전체가 안 죽는다)")

    # ── 회신 BU ②③: 3 온도 동시 부트스트랩 + reduced χ² ───────────────
    _Ea, _D0, _Ts = 0.25, 1.0e-3, [600.0, 800.0, 1000.0]
    _lnD = [math.log(_D0) - _Ea / (KB_EV * T) for T in _Ts]
    _fit = ea_from_lnD(_Ts, _lnD)
    chk(_fit and abs(_fit[0] - _Ea) < 1e-9 and max(abs(r) for r in _fit[2]) < 1e-9,
        "아레니우스 적합이 Ea 를 정확히 되돌린다 (잔차 ≈ 0)")
    chk(ea_from_lnD([600.0], [1.0]) is None and ea_from_lnD([600.0, 800.0], [1.0]) is None,
        "[음성] 점이 1 개거나 길이가 안 맞으면 None")
    chk(ea_from_lnD([600.0, 600.0], [1.0, 2.0]) is None,
        "[음성] 온도가 전부 같으면 None (기울기가 정의 안 된다)")
    chk(abs(reduced_chi2([0.1, -0.2, 0.1], [0.1, 0.1, 0.1]) - 6.0) < 1e-12,
        "reduced χ²: dof = 3 − 2 = 1 로 나눈다")
    chk(reduced_chi2([0.1, 0.1], [0.1, 0.1]) is None,
        "[음성] 점 2 개면 dof = 0 ⇒ None (0 으로 안 찍는다)")
    chk(reduced_chi2([0.1, 0.1, 0.1], [0.1, 0.0, 0.1]) is None
        and reduced_chi2([0.1, 0.1, 0.1], [0.1, 0.1]) is None,
        "[음성] σ 가 0 이거나 개수가 안 맞으면 None")

    def _mk(T, noise, n_o=24, seed=7):
        r = _np.random.default_rng(seed + int(T))
        sl = 6e4 * _D0 * math.exp(-_Ea / (KB_EV * T))       # Å²/ps
        return {"T_K": T, "t_ps": _t,
                "msd_per_origin": _np.array(
                    [sl * _t * (1 + noise * r.standard_normal()) for _ in range(n_o)])}
    _runs = [_mk(T, 0.05) for T in _Ts]
    _jb = joint_ea_bootstrap(_runs, 2.0, 50.0, block=4, n_boot=150, seed=3)
    chk(_jb and abs(_jb["Ea_eV"] - _Ea) < 0.05 and _jb["Ea_sigma_eV"] > 0,
        "3 온도 동시 재표본 → Ea 직접 적합 (진값 0.25 eV 를 되찾고 σ > 0)")
    chk(_jb["Ea_lo68_eV"] < _jb["Ea_hi68_eV"] and _jb["dof"] == 1
        and _jb["block"] == 4 and _jb["window_ps"] == [2.0, 50.0],
        "[음성] block·창·dof 를 **기록한다** (재현 못 하면 숫자가 아니다)")
    chk(_jb["red_chi2_point"] is not None and _jb["red_chi2_boot_median"] is not None,
        "reduced χ² 를 점추정과 재표본 양쪽에서 낸다")
    chk(joint_ea_bootstrap(_runs[:1], 2.0, 50.0, block=4) is None,
        "[음성] 온도가 1 개면 None (Ea 를 흉내내지 않는다)")
    chk(joint_ea_bootstrap(_runs, 200.0, 300.0, block=4) is None,
        "[음성] 창에 점이 3 개 미만인 온도가 있으면 None")
    _det = [{"T_K": T, "t_ps": _t,
             "msd_per_origin": _np.array([6e4 * _D0 * math.exp(-_Ea / (KB_EV * T)) * _t
                                          for _ in range(10)])} for T in _Ts]
    _jd = joint_ea_bootstrap(_det, 2.0, 50.0, block=2, n_boot=40, seed=4)
    chk(_jd and _jd["Ea_sigma_eV"] == 0.0 and _jd["red_chi2_point"] is None,
        "[음성] 원점이 전부 같으면 σ_Ea = 0 이고 **χ² 는 None** (0 으로 나누지 않는다)")
    _ov = [dict(r) for r in _runs]
    _ov[0]["mean_curve"] = _runs[0]["msd_per_origin"].mean(axis=0) * 2.0
    _jo = joint_ea_bootstrap(_ov, 2.0, 50.0, block=4, n_boot=40, seed=3)
    chk(_jo and _jo["Ea_eV"] < _jb["Ea_eV"] - 1e-6,
        "[음성] `mean_curve` 가 **실제로 읽힌다** — 600 K D 를 2 배 하면 Ea 가 내려간다")

    # ── β 블록 부트스트랩 (회신 CC Q8-①) ───────────────────────────────
    _rb = _np.random.default_rng(21)
    _tb = _np.linspace(0.1, 60.0, 120)
    _Ab = _np.array([3.0 * _tb ** 0.9 * (1 + 0.05 * _rb.standard_normal()) for _ in range(30)])
    _bb = block_bootstrap_beta(_Ab, _tb, 2.0, 50.0, block=3, n_boot=200, seed=5)
    chk(_bb and abs(_bb["beta_matrix_mean"] - 0.9) < 0.02 and 0 < _bb["sigma_beta"] < 0.05
        and _bb["lo68"] < _bb["hi68"] and _bb["block"] == 3 and _bb["window_ps"] == [2.0, 50.0],
        "β 블록 부트스트랩: 진값 0.9 를 되찾고 σ > 0 · block·창을 기록한다")
    _Adet = _np.array([3.0 * _tb ** 0.9 for _ in range(10)])
    _bd = block_bootstrap_beta(_Adet, _tb, 2.0, 50.0, block=2, n_boot=40, seed=1)
    chk(_bd and _bd["sigma_beta"] == 0.0, "[음성] 원점이 전부 같으면 σ(β) = 0")
    chk(block_bootstrap_beta(_Ab, _tb, 200.0, 300.0, block=3) is None
        and block_bootstrap_beta(_Ab[:1], _tb, 2.0, 50.0, block=3) is None,
        "[음성] 창에 점이 3 개 미만이거나 원점이 1 개면 None (숫자를 지어내지 않는다)")
    _big = block_bootstrap_beta(_Ab, _tb, 2.0, 50.0, block=1, n_boot=200, seed=5)
    chk(_big and _big["sigma_beta"] <= _bb["sigma_beta"] * 1.5 + 1e-9,
        "낱개 재표본(b=1)이 덩이(b=3)보다 σ 를 크게 과대평가하지 않는다 (무상관 합성자료의 일관성 확인)")

    # ── 부트스트랩 입력 생산자 (배선 확인) ─────────────────────────────
    import tempfile as _tf
    with _tf.TemporaryDirectory() as _td:
        _p = pathlib.Path(_td)
        with open(_p / "traj.xyz", "w") as _fh:
            _rg = _np.random.default_rng(11)
            for _k in range(40):
                _fh.write("2\nLattice=\"10.0 0.0 0.0 0.0 10.0 0.0 0.0 0.0 10.0\"\n")
                for _a2 in range(2):
                    _xyz = _rg.standard_normal(3) + _k * 0.1
                    _fh.write("Li %.6f %.6f %.6f\n" % tuple(_xyz))
        json.dump({}, open(_p / "msd.json", "w"))
        _po = msd_per_origin_from_traj(_p / "msd.json", save_fs=100.0)
        chk(_po and _po["msd_per_origin"].shape == (40 - _po["lag_max"], len(_po["t_ps"])),
            "생산자: 공통 원점 행렬 (n_origin, n_lag) 을 만든다 — 부트스트랩 입력이 생겼다")
        chk(_po["save_fs_assumed"] is False
            and msd_per_origin_from_traj(_p / "msd.json")["save_fs_assumed"] is True,
            "[음성] save_fs 를 **가정했는지**를 돌려준다 (조용히 가정하지 않는다)")
        chk(abs(_po["t_ps"][0] - 0.1) < 1e-12,
            "[음성] 시간축이 save_fs 에서 온다 (100 fs ⇒ 첫 lag 0.1 ps)")
        json.dump({}, open(_p / "msd.json", "w"))
        chk(msd_per_origin_from_traj(_p.parent / "없는곳" / "msd.json") is None,
            "[음성] traj.xyz 가 없으면 None (지어내지 않는다)")
    print(f"selftest {'PASS' if not n_bad else 'FAIL'} — {n_ok} ok, {n_bad} bad")
    return 1 if n_bad else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glob", help="msd.json 글롭 (따옴표로 감쌀 것)")
    ap.add_argument("--selftest", action="store_true",
                    help="서버·데이터 없이 판정 로직만 검증 (음성 경로 포함)")
    ap.add_argument("--mto", action="store_true",
                    help="다중 시간원점 곡선(msd_Li_A2_mto)으로 본다. "
                         "케이지/sub-diffusion 을 가르는 c 행 판별을 MTO 에 거는 것이 "
                         "이 플래그의 존재 이유다 (STO 는 늦은 창의 원점이 적어 판별 불가).")
    ap.add_argument("--window", type=float, nargs=2, default=[2.0, 50.0],
                    help="D 를 맞춘 창 (기본 2 50 — 캠페인 규약)")
    ap.add_argument("--average", action="store_true",
                    help="같은 온도의 파일들 **MSD 곡선을 먼저 평균**한 뒤 β 를 잰다. "
                         "독립 시드/config 는 같은 계의 다른 초기속도라 MSD 앙상블 평균이 "
                         "정당하다 — 홉이 적어 자기평균이 안 되는 궤적을 **재계산 없이** "
                         "살리는 유일한 수단.")
    ap.add_argument("--framework_split", action="store_true",
                    help="S 를 결합S(폴리음이온 안)/자유S 로 갈라 β 를 따로 잰다. "
                         "b2o3 서술③('자유 음이온 부격자 이동') 판정용. "
                         "⚠ 결합 불변이 먼저 확인된 계에서만 (분류가 첫 프레임 기준).")
    ap.add_argument("--framework_com", action="store_true",
                    help="골격이 움직일 때 그것이 **전역 흐름**인지 **자리 재배열**인지 "
                         "가른다. 골격 질량중심을 매 프레임 빼고 다시 재서, 남는 몫이 "
                         f"{int(DRIFT_KEEP*100)} %% 이하면 흐름(구제 가능) · "
                         f"{int(DRIFT_LOST*100)} %% 이상이면 재배열(구제 불가). 재계산 0.")
    ap.add_argument("--framework_elems", action="store_true",
                    help="--framework 에서 **원소별 β·ratio·severity 를 전부** 찍는다. "
                         "기본 출력은 max 를 만든 원소 하나뿐이라 '어떤 원소집합의 "
                         "max 인가' 가 안 보인다 — 셀 크기가 달라 판정 원소가 바뀌는 "
                         "비교(b2o3 128 vs 512원자)에서 그게 결론을 가른다.")
    ap.add_argument("--framework", action="store_true",
                    help="골격(비-Li) 원소가 녹고 있는지 같이 본다. Zhang npj 2026 이 "
                         "MACE-MP-0 의 LGPS 골격이 1050 K 부터 인위적으로 녹는 걸 잡았고, "
                         "우리 아레니우스 상한 1000 K 가 그 바로 아래다. 골격이 녹으면 "
                         "Li 의 'D' 는 확산이 아니라 구조 붕괴다.")
    # ── 런 내부 오차 (2026-09-22, 회신 BT) ─────────────────────────────────
    ap.add_argument("--rsd", action="store_true",
                    help="런별 **오차 열**을 낸다 — N_eff · He 2018 RSD(귀무모형) · "
                         "로그정규 비대칭 구간 · median/mean. ⛔ RSD > 0.30 이면 대칭 ± 를 "
                         "**출력하지 않는다**(2σ 가 음수로 간다). ⚠ He 식은 lag 창을 제한한 "
                         "적합에 대해 **검증되지 않았다**(회신 BT §6-e) — 정본은 부트스트랩이다.")
    ap.add_argument("--ea_boot", metavar="T=JSON,T=JSON,T=JSON",
                    help="**3 온도 동시 부트스트랩 → Ea 직접 적합** (회신 BU 2026-09-22). "
                         "`600=…/msd.json,800=…,1000=…`. 같은 시드의 세 온도를 준다. "
                         "블록은 --block_scan 으로 고르거나 --rsd_block 으로 박는다.")
    ap.add_argument("--beta_boot", metavar="JSON",
                    help="한 런의 **β 시간원점 블록 부트스트랩** (회신 CC Q8-①). traj.xyz 에서 공통원점 행렬을 만들어 "
                         "창 [--window] 의 log-log 기울기 β 의 σ 를 잰다. --block_scan 으로 b 를 plateau 규칙으로 고르고, "
                         "STO(카드 곡선)·MTO(정본) β 점추정을 같이 찍는다. 판정은 하지 않는다.")
    ap.add_argument("--block_scan", metavar="1,2,4,8",
                    help="--ea_boot 와 함께: 블록 사다리에서 σ(Ea) plateau 를 찾아 b 를 고른다. "
                         "⛔ plateau 가 없으면 **b 를 고르지 않고 판정을 보류한다**(종료코드 2).")
    ap.add_argument("--n_boot", type=int, default=400, metavar="B",
                    help="부트스트랩 복제 수 (기본 400)")
    ap.add_argument("--save_fs", type=float, default=None, metavar="FS",
                    help="프레임 저장 간격 [fs]. 안 주면 msd.json 에서 읽고, 그것도 없으면 "
                         "캠페인 기본 100 fs 를 **가정하고 그 사실을 찍는다**. "
                         "⚠ 이 값이 틀리면 시간축 전체가 틀린다.")
    ap.add_argument("--out", metavar="JSON", help="결과 JSON 경로 (--ea_boot 용)")
    ap.add_argument("--rsd_block", type=int, default=None, metavar="N",
                    help="--rsd 와 함께: 시간원점 **블록 부트스트랩**의 블록 길이(원점 개수). "
                         "⛔ **기본값을 두지 않는다** — 상관시간에 걸리므로 궤적을 보고 사람이 "
                         "정해야 한다(회신 BT: '결과 전에 못 박는 항목'). 안 주면 He 식만 낸다.")
    ap.add_argument("--haven", action="store_true",
                    help="궤적에서 **Haven 비 H_R = D*/D_σ 를 직접 잰다** (MD 재계산 0). "
                         "우리는 σ 를 H_R=1 로 환산해 왔고 그걸 '상한' 이라고 적어 왔는데 "
                         "**부호가 틀렸다** — H_R<1 이면 NE 는 과소다. 문헌값(Adeli 0.23)을 "
                         "빌리지 말고 우리 계에서 잰다. ⚠ 집단좌표는 표본이 하나라 D* 보다 "
                         "훨씬 잡음이 크다 — 방향 판별용이지 세 자리 숫자가 아니다.")
    ap.add_argument("--rebuild_mto", action="store_true",
                    help="MTO 곡선이 없는 런을 **traj.xyz 에서 되살린다**(MD 재계산 0). "
                         "700/900 K 신규 21런이 MTO 없이 저장돼 --mto 판정이 막혔다. "
                         "궤적이 없는 런은 원리적으로 복구 불가 — 그렇게 보고한다.")
    ap.add_argument("--from_traj", action="store_true",
                    help="--framework 에서 종별 MSD 가 json 에 없으면 옆의 traj.xyz 에서 "
                         "다시 계산한다(재계산 0, 읽기만). 결과는 json 에 되써 둔다.")
    ap.add_argument("--scan", action="store_true",
                    help="여러 창에서 β 를 재서 **어디서부터 확산이 되는지** 찾는다. "
                         "케이지 판정이 나왔을 때 '재계산 없이 구제 가능한가'를 가른다.")
    # ── 방향별·형상 비교 (2026-08-27, 교차리뷰 G/H) ──────────────────────────
    ap.add_argument("--directional", action="store_true",
                    help="traj.xyz 에서 **확산텐서** D_αβ 를 낸다. 이방 셀(3×3×1 등)에서 "
                         "scalar D 를 쓰기 전에 등방성부터 확인하는 용도.")
    ap.add_argument("--crystal_axes", action="store_true",
                    help="변위를 **결정축 â·b̂·ĉ 로 투영**해서 잰다 (비직교 셀 필수). "
                         "안 주면 Cartesian x·y·z 인데, 비직교면 그건 결정축이 아니다.")
    ap.add_argument("--prefixes", default="",
                    help="누적 prefix [ps] 쉼표목록 (예: 100,200,400). 각 시점에서 다시 잰다 "
                         "— D_inc plateau 가 이미 왔으면 완주 전에 끊을 수 있다.")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.directional:
        return cmd_directional(a)
    # ── β 시간원점 블록 부트스트랩 (회신 CC Q8-① · 2026-09-26) ───────────
    if a.beta_boot:
        jp = pathlib.Path(a.beta_boot)
        sf_v, sf_assumed, sf_src = resolve_save_fs(jp, a.save_fs)
        po = msd_per_origin_from_traj(jp, save_fs=sf_v)
        if po is None:
            raise SystemExit(f"⛔ {jp.parent}/traj.xyz 를 못 읽었다 — β 부트스트랩은 궤적 없이 못 한다.")
        d = json.load(open(jp)) if jp.exists() else {}
        lo, hi = a.window
        t_s, y_s = _curve(d, mto=False)
        b_sto = loglog_slope(t_s, y_s, lo, hi) if (t_s and y_s) else None
        t_m, y_m = _curve(d, mto=True, path=jp, rebuild=False)
        b_mto = loglog_slope(t_m, y_m, lo, hi) if (t_m and y_m) else None
        print(f"β 부트스트랩 · {jp.parent.name} · 창 [{lo:g}, {hi:g}] ps · 원점 {po['n_origin']} · lag {len(po['t_ps'])} · "
              f"save_fs {sf_v:g} fs ({sf_src or '캠페인 기본 가정'}){'  ⚠ **가정값**' if sf_assumed else ''}")
        print(f"   β 점추정 — STO(카드 곡선 msd_Li_A2): {b_sto if b_sto is None else f'{b_sto:.4f}'} · "
              f"MTO(정본 msd_Li_A2_mto): {b_mto if b_mto is None else f'{b_mto:.4f}'} · "
              f"공통원점 행렬 평균: {loglog_slope(po['t_ps'], po['msd_per_origin'].mean(axis=0), lo, hi):.4f}")
        blk = a.rsd_block
        scan = None
        if a.block_scan:
            ladder = [int(x) for x in a.block_scan.split(",") if x.strip()]
            print(f"\n블록 사다리 {ladder} 로 σ(β) 를 재고 plateau 를 고른다 "
                  f"(연속 {BLOCK_PLATEAU_RUN} 점 · b 당 상대변화 ≤ {BLOCK_PLATEAU_TOL:.0%})")
            cur = block_sigma_curve(
                lambda b: (block_bootstrap_beta(po["msd_per_origin"], po["t_ps"], lo, hi, b, a.n_boot, seed=0) or {})
                .get("sigma_beta"), ladder)
            for b, s in cur:
                print(f"   b={b:3d}   σ(β) = {s:.5f}")
            scan = choose_block_plateau(cur, n_boot=a.n_boot)
            print(f"\n   → {scan['why']}")
            blk = scan["block"]
        res = {"json": str(jp), "window_ps": [lo, hi], "beta_STO_card_curve": b_sto, "beta_MTO_canonical": b_mto,
               "save_fs": sf_v, "save_fs_src": sf_src, "save_fs_assumed": bool(sf_assumed), "n_origin": po["n_origin"],
               "block_scan": scan,
               "reading": "σ 는 공통원점 행렬(MTO 추정자)의 런 내부 표준편차. 카드의 β* 가 STO(단일 원점)면 그 산포는 이보다 "
                          "작지 않으므로 σ 는 **하한**이다. 회신 CC 규칙: 폭(σ) > 0.005 면 '경계 · 구분 불가'. 판정은 도구가 하지 않는다."}
        if blk is None:
            print("\n⛔ **블록 길이를 고르지 않는다** ⇒ σ(β) 는 '못 구했다' 로 적는다 (회신 BU 규칙). 아무 b 나 골라 숫자를 만들지 않는다.")
            res["status"] = "판정보류_블록_plateau_없음"
            if a.out:
                pathlib.Path(a.out).write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n"); print(f"-> {a.out}")
            return 2
        bb = block_bootstrap_beta(po["msd_per_origin"], po["t_ps"], lo, hi, blk, a.n_boot, seed=0)
        if bb is None:
            raise SystemExit("⛔ 부트스트랩 실패 — 창에 점이 모자라거나 곡선이 0 이하다.")
        res["beta_boot"] = bb
        ref = b_sto if b_sto is not None else b_mto
        if ref is not None:
            res["boundary_vs_0.8"] = {"beta_ref": ref, "ref_curve": "STO" if b_sto is not None else "MTO",
                                     "distance": ref - 0.8, "sigma": bb["sigma_beta"],
                                     "cc_width_rule_0.005": "경계·구분 불가" if bb["sigma_beta"] > 0.005 else "폭 ≤ 0.005",
                                     "distance_over_sigma": (ref - 0.8) / bb["sigma_beta"] if bb["sigma_beta"] > 0 else None}
        print(f"\n  β̂(행렬) = {bb['beta_matrix_mean']:.4f}   σ(β) = {bb['sigma_beta']:.5f}   [68 % {bb['lo68']:.4f}, {bb['hi68']:.4f}]"
              f"   block {bb['block']} · 재표본 {bb['n_boot_used']}/{bb['n_boot']} · 원점 {bb['n_origin']}")
        if ref is not None:
            bv = res["boundary_vs_0.8"]
            print(f"  카드 β*({bv['ref_curve']}) {ref:.4f} 는 0.8 에서 {bv['distance']:+.4f} · σ 의 {bv['distance_over_sigma']:.2f} 배 · "
                  f"회신 CC 폭 규칙(0.005): **{bv['cc_width_rule_0.005']}**")
        if a.out:
            pathlib.Path(a.out).write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n"); print(f"-> {a.out}")
        return 0
    # ── 3 온도 동시 부트스트랩 → Ea (회신 BU · 2026-09-22) ───────────────
    if a.ea_boot:
        import numpy as _np
        runs, bad = [], []
        for tok in a.ea_boot.split(","):
            if "=" not in tok:
                raise SystemExit(f"⛔ --ea_boot 항목 형식은 `온도=msd.json` 이다: {tok!r}")
            Ts, jp = tok.split("=", 1)
            jp = pathlib.Path(jp.strip())
            #: ⛔ `resolve_save_fs` 는 **튜플** `(값, 가정여부, 출처)` 를 준다.
            #:   그대로 넘기면 시간축이 통째로 망가진다 (2026-09-22 에 여기서 한 번 밟았다).
            sf_v, sf_assumed, sf_src = resolve_save_fs(jp, a.save_fs)
            po = msd_per_origin_from_traj(jp, save_fs=sf_v)
            if po is None:
                bad.append(str(jp))
                continue
            d = json.load(open(jp)) if jp.exists() else {}
            mc, src = None, "공통원점 행렬 (⚠ 정본 MTO 아님)"
            if d.get("msd_Li_A2_mto") and len(d["msd_Li_A2_mto"]) == len(po["t_ps"]):
                mc = d["msd_Li_A2_mto"]
                src = "정본 MTO 곡선 (msd_Li_A2_mto)"
            elif d.get("msd_Li_A2_mto"):
                print(f"   ⚠ {jp.parent.name}: 정본 MTO 길이 {len(d['msd_Li_A2_mto'])} ≠ "
                      f"재생성 lag {len(po['t_ps'])} — **점추정을 정본에서 못 낸다**. "
                      "행렬 평균으로 간다 (추정자가 다르다는 것을 기록에 남긴다).")
            runs.append({"T_K": float(Ts), "t_ps": po["t_ps"],
                         "msd_per_origin": po["msd_per_origin"], "mean_curve": mc,
                         "_src": src, "_n_origin": po["n_origin"],
                         "_save_fs": sf_v, "_save_fs_src": sf_src or "캠페인 기본 가정",
                         "_save_fs_assumed": bool(sf_assumed)})
        if bad:
            raise SystemExit(f"⛔ traj.xyz 를 못 읽은 런: {bad} — 부트스트랩을 시작하지 않는다.")
        if len(runs) < 2:
            raise SystemExit("⛔ 온도가 2 개 미만이다.")
        lo, hi = a.window
        for r in runs:
            print(f"   {r['T_K']:.0f} K · 원점 {r['_n_origin']} · 점추정 ← {r['_src']}"
                  + f" · save_fs {r['_save_fs']:g} fs ({r['_save_fs_src']})"
                  + ("  ⚠ **가정값**" if r["_save_fs_assumed"] else ""))
        blk = a.rsd_block
        scan = None
        if a.block_scan:
            ladder = [int(x) for x in a.block_scan.split(",") if x.strip()]
            print(f"\n블록 사다리 {ladder} 로 σ(Ea) 를 재고 plateau 를 고른다 "
                  f"(연속 {BLOCK_PLATEAU_RUN} 점 · 상대변화 ≤ {BLOCK_PLATEAU_TOL:.0%})")
            cur = block_sigma_curve(
                lambda b: (joint_ea_bootstrap(runs, lo, hi, b, a.n_boot, seed=0) or {})
                .get("Ea_sigma_eV"), ladder)
            for b, s in cur:
                print(f"   b={b:3d}   σ(Ea) = {s:.5f} eV")
            scan = choose_block_plateau(cur, n_boot=a.n_boot)
            print(f"\n   → {scan['why']}")
            blk = scan["block"]
        if blk is None:
            print("\n⛔ **블록 길이를 고르지 않는다** ⇒ σ_within 은 '못 구했다' 로 적고 "
                  "판정을 보류한다 (회신 BU 규칙). 아무 b 나 골라 숫자를 만들지 않는다.")
            if a.out:
                pathlib.Path(a.out).write_text(json.dumps(
                    {"status": "판정보류_블록_plateau_없음", "block_scan": scan},
                    ensure_ascii=False, indent=1) + "\n")
                print(f"-> {a.out}")
            return 2
        jb = joint_ea_bootstrap(runs, lo, hi, blk, a.n_boot, seed=0)
        if jb is None:
            raise SystemExit("⛔ 부트스트랩 실패 — 창에 점이 모자라거나 D ≤ 0 인 온도가 있다.")
        jb["block_scan"] = scan
        jb["point_estimate_source"] = {f"{r['T_K']:.0f}K": r["_src"] for r in runs}
        print(f"\n  Ea (점추정)  = {jb['Ea_eV']:.4f} eV")
        print(f"  σ(Ea)        = {jb['Ea_sigma_eV']:.5f} eV   "
              f"[68 % {jb['Ea_lo68_eV']:.4f}, {jb['Ea_hi68_eV']:.4f}]")
        rc = jb["red_chi2_point"]
        print(f"  reduced χ²   = " + (f"{rc:.3f}" if rc is not None else "— (못 냈다)")
              + f"   ({jb['red_chi2_note']})")
        print(f"  재표본 {jb['n_boot_used']}/{jb['n_boot_asked']} · block {jb['block']} · "
              f"창 {jb['window_ps']} ps")
        print("\n  ⚠ 이 σ(Ea) 는 **런 내부**다. 시드 간 산포와의 비교는 "
              "`arrhenius_compat.py --vr` 가 한다 (분산비 판정, 회신 BU).")
        if a.out:
            pathlib.Path(a.out).write_text(json.dumps(jb, ensure_ascii=False, indent=1) + "\n")
            print(f"-> {a.out}")
        return 0

    if not a.glob:
        ap.error('--glob 이 필요하다 (또는 --selftest / --ea_boot)')

    # ⚠⚠ 2026-08-11 — `recursive=True` 가 빠져 있었다. 그러면 `**` 가 재귀가 아니라
    #   **한 단계**로만 동작해서, 캠페인이 실제로 쓰는 경로
    #   `<계>/T700_s2/d0.00_cfg0/T700/msd.json` (두 단계 깊이)를 하나도 못 찾는다.
    #   run_arrhenius_6pt.sh 가 '다음 단계'로 찍어 주는 명령이 바로 그 글롭이었고,
    #   msd_refit_window.py 는 recursive=True 라 같은 글롭으로 21개를 찾았다 —
    #   **도구마다 다른 답**이 나온 게 이 한 줄이다.
    files = sorted(_glob.glob(os.path.expanduser(a.glob), recursive=True))
    if not files:
        # 0개를 '파일 없음'으로만 끝내면 글롭 버그와 정말로 안 돈 것을 구분 못 한다.
        loose = sorted(_glob.glob(os.path.expanduser(a.glob).split("**")[0] + "**/msd.json",
                                  recursive=True)) if "**" in a.glob else []
        msg = [f"파일 없음: {a.glob}"]
        if loose:
            msg.append(f"⚠ 같은 뿌리 아래 msd.json 은 {len(loose)}개 있다 — 글롭 패턴을 볼 것:")
            msg += [f"    {p}" for p in loose[:3]]
        raise SystemExit("\n".join(msg))
    lo, hi = a.window

    def case_label(path, width=34):
        """⚠ 2026-08-11 — 옛 라벨은 `[-3:-1]` 이라 전부 `d0.00_cfg0/T700` 로 찍혔다.
        어느 계(modelc/lpsocl/b2o3)의 어느 시드인지가 **표에서 사라져** 탈락 8건이
        어디 것인지 읽을 수가 없었다. 정보 없는 조각(d*_cfg*, 마지막 T* 중복)을 버린다."""
        import re as _re
        parts = path.split(os.sep)[:-1]                     # msd.json 제외
        drop = _re.compile(r"^d\d+\.\d+_cfg\d+$")
        keep = [p for p in parts[-4:] if not drop.match(p)]
        if len(keep) >= 2 and keep[-1].lstrip("T").isdigit() \
                and keep[-1].lstrip("T") in keep[-2]:
            keep = keep[:-1]                                # T700_s2/T700 → T700_s2
        lab = "/".join(keep)
        return lab[-width:] if len(lab) > width else lab

    # ⛔⛔ 2026-09-10 실측 — 같은 라벨이 한 표에 **세 번** 찍혔다:
    #   arrhenius_6pt(궤적없음) · arrhenius_6pt_traj(있음) · mto_pilot 의 b2o3/T700_s2.
    #   궤적 없는 런의 "종별 MSD 없음" 과 진짜 결과가 같은 이름을 달면, 로그를 나중에
    #   읽는 사람이 **어느 줄이 어느 런인지 가를 방법이 없다**. 라벨은 식별자다.
    #   ⇒ 겹치면 표 전체에 같은 깊이를 더 준다 (줄마다 규칙이 다르면 더 헷갈린다).
    def _label_map(paths, width=46):
        base = {q: case_label(q) for q in paths}
        if len(set(base.values())) == len(set(paths)):
            return base
        for k in range(5, 10):
            cand = {q: "/".join([x for x in q.split(os.sep)[:-1] if x][-k:]) for q in paths}
            if len(set(cand.values())) == len(set(paths)):
                return {q: (v[-width:] if len(v) > width else v) for q, v in cand.items()}
        return {q: q[-width:] for q in paths}

    LBL = _label_map(files)


    # ── 런 내부 오차 (2026-09-22, 회신 BT) ──────────────────────────────
    if a.rsd:
        print(f"런 내부 오차  (창 {lo}–{hi} ps)")
        print("⛔ He 2018 식은 **귀무모형**이다 — lag 창을 제한한 적합에 대해 미검증"
              " (회신 BT §6-e). 정본은 시간원점 블록 부트스트랩이다.")
        if a.rsd_block is None:
            print("⚠ --rsd_block 이 없다 ⇒ **부트스트랩을 못 돌린다**(안 돌린 것이지 0 이 아니다)."
                  " 블록 길이는 상관시간에 걸리므로 궤적을 보고 정한다.")
        print(f"{'런':34s}{'n_Li':>5s}{'maxMSD':>9s}{'N_eff':>9s}{'RSD_He':>8s}"
              f"{'s_ln':>7s}{'lo68':>7s}{'hi68':>7s}{'med/mean':>9s}  대칭±")
        n_blk = 0
        for f in files:
            try:
                rec = json.loads(pathlib.Path(f).read_text())
            except Exception as e:
                print(f"{LBL[f]:34s}  ⚠ 못 읽음 ({e})")
                continue
            rr = rsd_report(rec, block=a.rsd_block)
            if rr["rsd_he2018"] is None:
                print(f"{LBL[f]:34s}{str(rr['n_Li'] or '—'):>5s}"
                      f"{'—':>9s}{'—':>9s}{'—':>8s}"
                      "   ⛔ N_eff 를 못 냈다 — n_Li 또는 max(MSD) 가 없다")
                continue
            blocked = not rr.get("symmetric_pm_allowed", True)
            n_blk += int(blocked)
            print(f"{LBL[f]:34s}{rr['n_Li']:5d}{rr['msd_max_A2']:9.1f}"
                  f"{rr['n_eff_he2018']:9.0f}{rr['rsd_he2018']:8.3f}"
                  f"{rr['s_lognorm']:7.3f}{rr['D_lo68_rel']:7.3f}{rr['D_hi68_rel']:7.3f}"
                  f"{rr['median_over_mean']:9.3f}  {'⛔ 차단' if blocked else '✅'}")
        print(f"\n  lo68·hi68·med/mean 은 **평균 = 1 단위의 상대값**이다 (D 를 곱해 쓴다).")
        if n_blk:
            print(f"  ⛔ **{n_blk} 런에서 대칭 ± 를 막았다** — RSD > {RSD_SYMMETRIC_MAX} 면 "
                  "대칭 2σ 가 음수로 간다. 비대칭 구간만 쓴다.")
        print("  ⚠ median/mean < 1 은 **단일 런 D 가 절반 이상 확률로 참값보다 낮다**는 뜻이다"
              " (D 분포가 오른쪽 치우침 — he2018 `Fig. S2`).")
        print("  ⚠ 단, 짧은 런은 **탄도 오염으로 D 를 과대**평가하기도 한다(he2018 `Fig. S4`)."
              " **두 편향은 부호가 반대**고 어느 쪽이 이기는지는 계마다 다르다.")
        return 0

    # ── Haven 비 직접 측정 (2026-09-07) ─────────────────────────────────
    if a.haven:
        print(f"Haven 비 H_R = D*/D_σ  (창 {lo}–{hi} ps · 자유절편 · COM 드리프트 제거)")
        print("⚠ σ_NE = H_R × σ_true 다 — H_R<1 이면 NE 는 **과소**다 (kb/concepts/md.md §6)")
        print(f"{'런':36s}{'Li':>4s}{'D* cm²/s':>12s}{'D_σ cm²/s':>12s}{'H_R':>8s}  판정")
        got, miss = [], []
        for f in files:
            r = haven_from_traj(f, save_fs=a.save_fs if hasattr(a, "save_fs") else None,
                                lo=lo, hi=hi)
            if not r or r.get("haven_ratio") is None:
                miss.append(LBL.get(f, case_label(f))); continue
            h = r["haven_ratio"]
            v = ("협동 이동 (NE 과소)" if h < 0.8 else
                 "상관 없음 ≈ NE 맞음" if h <= 1.25 else "역상관 (NE 과대)")
            print(f"{case_label(f, 36):36s}{r['n_Li']:4d}{r['D_star_cm2_s']:12.3e}"
                  f"{r['D_sigma_cm2_s']:12.3e}{h:8.3f}  {v}")
            got.append(h)
        if miss:
            print(f"\n⛔ 측정 불가 {len(miss)}런 (traj 없음/창 부족): "
                  + ", ".join(miss[:4]) + (" …" if len(miss) > 4 else ""))
        if got:
            import statistics as _st
            m = _st.mean(got)
            sd = _st.pstdev(got) if len(got) > 1 else float("nan")
            print(f"\n★ H_R 평균 {m:.3f}" + (f" · 런간 SD {sd:.3f} (n={len(got)})"
                                             if len(got) > 1 else " (n=1 — 산포 없음)"))
            print(f"  ⇒ σ_true ≈ {1/m:.2f} × σ_NE" if m > 0 else "  ⇒ 환산 불가")
            print("  ⚠ 집단좌표는 표본이 하나라 D* 보다 훨씬 잡음이 크다. **방향 판별용**이고")
            print("    값으로 쓰려면 estimand 카드·문턱 선등록이 먼저다 (CLAUDE.md 계산 규율).")
        else:
            print("\n⛔ 측정된 런이 하나도 없다 — 궤적이 있는 경로로 글롭할 것")
        return 0

    # ── 계·온도별 MSD 앙상블 평균 ─────────────────────────────────────────
    avg_curves = {}
    if a.average:
        # ⛔⛔ 2026-08-11 — 옛 코드는 **온도로만** 묶었다(`byT[T_K]`). 캠페인 글롭이
        #   세 계를 한꺼번에 덮으므로 T700 에 modelc·lpsocl·b2o3 가 **같이 평균**됐다.
        #   서로 다른 물질의 MSD 곡선을 평균한 것이라 그 값은 아무 뜻이 없다.
        #   (한 계씩 글롭할 때만 우연히 맞았다.) → (계, T) 로 묶는다.
        # ⚠ 시간 격자가 같아야 평균이 의미 있다. 다르면 짧은 쪽에 맞춰 자른다.
        byST = {}
        for f in files:
            d = json.load(open(f))
            t, y = _curve(d, a.mto, f, a.rebuild_mto)
            if not t or not y:
                continue
            lab = LBL.get(f, case_label(f))
            sysname = lab.split("/")[0] if "/" in lab else lab   # 계 이름
            byST.setdefault((sysname, int(d.get("T_K", 0))), []).append((t, y, f))
        print(f"계·온도별 MSD 앙상블 평균 (창 {lo}–{hi} ps)"
              + ("  **곡선: MTO(다중 시간원점)**" if a.mto else "  [곡선: STO]"))
        print(f"{'계':12s} {'T (K)':>7s} {'n_runs':>7s} {'beta':>6s} {'c [Å²]':>8s} "
              f"{'MSD@hi':>9s}  판정")
        for key in sorted(byST):
            sysname, T = key
            runs = byST[key]
            n = min(len(t) for t, _, _ in runs)
            tt = runs[0][0][:n]
            yy = [sum(r[1][i] for r in runs) / len(runs) for i in range(n)]
            avg_curves[f"{sysname}/T{T}_AVG{len(runs)}"] = (tt, yy)
            b = loglog_slope(tt, yy, lo, hi)
            lf = lin_fit(tt, yy, lo, hi)
            m = max((v for u, v in zip(tt, yy) if u <= hi), default=float("nan"))
            ok = b is not None and BETA_OK[0] <= b <= BETA_OK[1] and m >= MSD_MIN_A2
            print(f"{sysname:12s} {T:7d} {len(runs):7d} "
                  f"{b if b is None else round(b, 2):>6} "
                  + (f"{lf[1]:8.2f}" if lf else f"{'—':>8s}")
                  + f" {m:9.1f}  {'✓ 확산' if ok else '⛔ 여전히 비확산'}")
        print("  ⚠ 평균이 살아나도 **개별 런은 여전히 못 쓴다** — config 산포를 평균 뒤에")
        print("    다시 낼 수 없으므로, 오차막대는 다른 방법(블록 평균 등)으로 내야 한다.")
        print("  ★ --scan 을 같이 주면 **이 평균 곡선으로** 창 스캔을 돈다 — 늦은 창의")
        print("    통계가 √n 배 좋아져서 c 판별(케이지 vs sub-diffusion)이 실제로 가능해진다.")
        print()

    print(("**MTO 곡선**" if a.mto else "STO 곡선") + " · "
          + f"창 {lo}–{hi} ps · 판정 = D_inc plateau(창 {len(DINC_WINDOWS)}개, "
          f"산포 ≤ {DINC_PLATEAU_TOL:.0%}) · 홉 ≥ {HOPS_MIN_PER_ION}/이온 · "
          f"창끝 MSD < {MSD_MIN_A2} Å² 면 통계 부족")
    print(f"  D 계열 = **{'MTO' if a.mto else 'STO'}** — β·c·D_inc 와 같은 곡선에서 낸다 "
          "(회신 S P0: 종전엔 --mto 여도 D 만 STO 를 읽어 한 표에 두 추정량이 섞였다)")
    # ⚠⚠ β<0.8 을 곧바로 '케이지' 로 읽지 말 것 — **창끝 MSD 를 같이 본다.**
    #   2026-08-11 귀무분포 검정(tools/ionic/beta_null_test.py): 케이지가 0 인 이상
    #   브라운 운동을 Li 27개·200 ps 로 재면 창 2–50 에서 β = 1.01 (5–95% 0.86–1.14),
    #   0.8 미만이 **1.0%** 뿐이다. 즉 이 창의 β<0.8 은 표본 부족이 아니라 진짜다.
    #   반면 늦은 창(50–200)에서는 이상 계도 10%가 0.8 아래로 떨어진다 — 그 창의
    #   β 로 '구제' 판정을 하면 안 된다. 창마다 게이트의 신뢰도가 다르다.
    print(f"{'case':34s} {'D(cm2/s)':>10s} {'beta*':>6s} {'MSD@hi':>8s}  판정")
    print("  * β 는 **경보**다 — 판정에 안 들어간다 (kb/concepts/beta-gate.md §7-5, "
          "2026-08-26 폐기). 판정축: D_inc plateau · 창 안정성 · 홉 수")
    bad = []
    #: ⏸ HOLD — 값은 있으나 정밀도가 부족한 런. **no-value 와 합치지 않는다** (회신 AK Q5):
    #:   '정의되지 않음' 과 '정밀도 부족' 을 한 코드로 뭉개면 처방이 갈린다
    #:   (전자는 프로토콜을 고치고, 후자는 시드·길이를 늘린다).
    held = []
    #: ⛔⛔ 2026-08-17 fail-open — MSD 배열이 없는 런은 `continue` 로 건너뛰고 bad 에도
    #:   안 들어가서, **아무것도 못 쟀는데** 마지막 줄이 "✅ 전부 확산 영역 — D/Ea
    #:   인용 가능" 으로 찍혔다 (lpsocl 작은 셀 3런이 그랬다: β 세 칸이 전부 '—' 인데 ✅).
    #:   못 잰 것은 통과가 아니다. 따로 세서 총평이 ✅ 로 못 가게 막는다.
    unmeasured = []
    for f in files:
        d = json.load(open(f))
        t, y = _curve(d, a.mto, f, a.rebuild_mto)
        # ⛔⛔ 2026-08-29 (회신 S P0) — **추정량을 섞고 있었다.** `--mto` 를 줘도 이 줄이
        #   저장된 STO `D_Li_cm2_s` 를 읽었다. β·c·D_inc 는 MTO 곡선에서 나오는데 D 만
        #   STO 였으므로, 한 표 안에서 **두 추정량이 섞였다.** 실측 격차:
        #     558원자 1.190e-05(STO) vs 1.238e-05(MTO m/6) · 62원자 6.632e-06 vs 7.817e-06.
        #   생성 코드가 `D_Li_cm2_s` 와 `D_Li_cm2_s_mto` 를 **별도 필드로** 저장하는데
        #   (disorder_ensemble_diffusion.py) 소비 쪽이 그걸 안 봤다.
        #   ⇒ 보고 있는 곡선과 **같은 계열**의 D 만 쓴다. 없으면 조용히 후퇴하지 않는다.
        if a.mto:
            D = d.get("D_Li_cm2_s_mto")
            D_src = "MTO"
            if D is None:                       # 같은 창·같은 곡선에서 직접 낸다
                _lf = lin_fit(t, y, lo, hi) if (t and y) else None
                D = (_lf[0] / 6.0 * 1e-4) if _lf else None
                D_src = "MTO(창내 재적합)" if D is not None else "없음"
        else:
            D = d.get("D_Li_cm2_s")
            D_src = "STO"
        tag = LBL.get(f, case_label(f))
        # ⚠ P1-6 — D 가 null 인 msd.json 하나만 있어도 옛 코드는 TypeError 로 죽어
        #   **전수 게이트가 통째로** 날아갔다 (MD 가 중간에 죽으면 실제로 생긴다).
        _f = (lambda v, sp: "—".rjust(len(sp.format(0)))
              if v is None or v != v else sp.format(v))
        if not t or not y:
            # ⚠ 2026-08-17 — "MSD 배열 없음" 은 **틀린 진단이었다.** lpsocl 작은 셀은
            #   msd_Li_A2/times_ps 를 갖고 있었고, 없는 건 `--mto` 가 찾는
            #   msd_Li_A2_mto 뿐이었다. 두 경우는 처방이 완전히 다르다:
            #     · MTO 만 없다 → --mto 를 빼면 **지금 바로** 잴 수 있다 (재계산 0)
            #     · 정말 아무것도 없다 → MSD 산출 단계를 다시 돌려야 한다
            #   같은 문구로 뭉개면 "재계산해야 한다" 로 읽혀 하루를 버린다.
            sto = bool(d.get("msd_Li_A2") and d.get("times_ps"))
            why = ("MTO 곡선 없음 (STO 배열은 있다) — `--mto` 를 빼면 잴 수 있다"
                   if a.mto and sto else "MSD 배열 없음 — β 를 재지 못했다")
            print(f"{tag:34s} {_f(D, '{:10.3e}')} {'—':>6s} {'—':>8s}  ⚠ {why.split(' —')[0]}")
            unmeasured.append((tag, why))
            continue
        b = loglog_slope(t, y, lo, hi)
        msd_hi = max((v for u, v in zip(t, y) if u <= hi), default=float("nan"))
        # ⛔⛔ 2026-08-30 (회신 AK) — **판정은 D_inc plateau 가 낸다. β 는 경보다.**
        #   kb/concepts/beta-gate.md §7-5·§7-8b 가 2026-08-26/27 에 β=0.8 하드게이트를
        #   폐기했는데 이 도구는 나흘간 안 고쳐졌고, 그 사이 회신 AK 가 폐기된 문턱을
        #   착수 근거로 다시 인용했다. 판정을 바꿀 때 **그 판정을 구현한 도구**를 같이 고친다.
        code, why = run_verdict(t, y, beta=b)
        marks = []
        if b is None:
            marks.append("β 못 잼")
        elif b < BETA_OK[0]:
            # ★ 2026-08-26 잔차 게이트 — β<0.8 을 곧바로 '케이지'로 부르지 않는다.
            #   같은 창의 자유절편 직선 (c, m) 이 함의하는 귀무 β (b_imp) 와 비교한다:
            #   완벽한 Fickian 계도 절편 c>0 이면 β 는 결정론적으로 1 아래다
            #   (홉 스윕 실측: 절편 2 Å²·홉 13.9 에서 귀무 β 중앙값이 정확히 0.80 —
            #    우리 운영점에서 고정문턱 0.8 은 동전던지기다). 관측 β 가 b_imp 의
            #   잡음 범위(−0.12) 안이면 '절편+통계로 설명됨'이고, 그보다 한참 아래일
            #   때만 진짜 sub-diffusion 신호다.
            lf = lin_fit(t, y, lo, hi)
            n_hop = (max(y) / D_HOP_A ** 2) if y else float("nan")   # MSD@end/d² = f·n (이벤트 수의 하한)
            b_imp = None
            if lf and lf[1] > 0:
                xx = [x for x in t if lo <= x <= hi and x > 0]
                b_imp = loglog_slope(xx, [lf[1] + lf[0] * x for x in xx], lo, hi)
            # ⚠ 단일 창에서는 매끈한 멱함수(진짜 sub-diff)도 직선 근사가 잘 돼
            #   Δβ≈0 이 나온다 — 이 분기는 '케이지 확정'이 아니라 '단독판정 불가'다.
            #   케이지 vs 멱함수 확정은 --scan 의 다중 창 c-추세만 가른다.
            if b_imp is not None and (b - b_imp) >= -BETA_NOISE_5PCT:
                marks.append(f"⛔ β{b:.2f}≈귀무{b_imp:.2f} — 절편+홉{n_hop:.0f} 설명가능 "
                             f"(케이지/멱함수 미구분 — --scan c행으로 확정)")
            elif b_imp is not None:
                marks.append(f"⛔ β{b:.2f}≪귀무{b_imp:.2f} (Δ{b - b_imp:+.2f}) — "
                             f"직선으로 근사 안 되는 창 (표본 파탄 또는 급전이 — --scan)")
            else:
                marks.append(f"⛔ β={b:.2f}<{BETA_OK[0]} (절편≤0 — 원인 불명)")
        elif b > BETA_OK[1]:
            marks.append(f"⚠ 드리프트(β={b:.2f})")
        if msd_hi < MSD_MIN_A2:
            marks.append(f"⛔ 통계부족(MSD {msd_hi:.1f} Å²)")
        # β 경보는 **표시만** 한다 — 판정은 code 가 낸다.
        alarm = (" ⚠[" + " · ".join(m.lstrip("⛔⚠ ") for m in marks) + "]") if marks else ""
        verdict = {CITABLE: "✓ " + why[0], HOLD: "⏸ HOLD — " + why[0],
                   NO_VALUE: "⛔ no-value — " + why[0]}[code] + alarm
        if code == NO_VALUE:
            bad.append((tag, verdict))
        elif code == HOLD:
            held.append((tag, verdict))
        print(f"{tag:34s} {_f(D, '{:10.3e}')} {_f(b, '{:6.2f}')} "
              f"{_f(msd_hi, '{:8.1f}')}  {verdict}")

    # ── 창 스캔: 재계산 없이 구제 가능한가 ────────────────────────────────
    if a.scan:
        # ⚠ MSD 는 짧은 시간에서 원래 sub-diffusive 다(케이지 안 진동). 늦은 창에서
        #   β 가 1 로 올라가면 **MD 를 다시 돌 필요 없이 창만 바꾸면 된다.**
        #   끝까지 β<1 이면 그건 궤적이 짧은 것이라 prod 연장 말고는 답이 없다.
        # ⚠⚠ **창 목록이 궤적 길이를 따라가야 한다 (2026-08-03).** 이 목록은 200 ps prod
        #   기준으로 굳어 있어서 최대 창이 100-200 ps 였다. 1600 ps 런이 들어와도 뒤쪽
        #   1400 ps 를 **아예 안 본다** — 연장한 이유가 늦은 창에서 확산 영역을 보려는
        #   것인데 그 창이 목록에 없으면 3일치 GPU 가 그냥 버려진다.
        #   → 궤적 tmax 에 맞춰 늦은 창을 자동으로 덧붙인다 (짧은 창은 대조용으로 유지).
        tmax_all = 0.0
        for f in files:
            try:
                tt = json.load(open(f)).get("times_ps") or []
                tmax_all = max(tmax_all, max(tt) if tt else 0.0)
            except Exception:
                pass
        WINS = [(2, 50), (10, 50), (25, 100), (50, 150), (50, 200), (100, 200)]
        for frac_lo, frac_hi in ((0.10, 0.50), (0.25, 0.75), (0.50, 1.00)):
            lo, hi = round(tmax_all * frac_lo), round(tmax_all * frac_hi)
            if hi > 200 and hi - lo >= 50 and (lo, hi) not in WINS:
                WINS.append((lo, hi))
        if tmax_all > 250:
            print(f"(궤적 tmax {tmax_all:.0f} ps → 늦은 창 자동 추가: "
                  f"{', '.join(f'{l}-{h}' for l, h in WINS[6:])})")

        # ⛔⛔ 2026-08-27 (Codex 회신 F, P0) — **tmax 를 넘는 창을 라벨 그대로 찍고 있었다.**
        #   tmax=100 궤적에서 `50-150` 과 `50-200` 이 **둘 다 50–100 을 잰다.** 화면에는
        #   서로 다른 두 창으로 나오고 값이 같으니 "두 창이 일치한다" 로 읽힌다 —
        #   실제로는 **같은 창을 두 번 찍은 것**이다. 2026-08-27 R2b 표가 이 함정에
        #   걸렸다(lpsocl/T700 의 c 15.07 이 두 열에 같은 값으로 나와 추세로 읽혔다).
        #   → tmax 로 자르고 중복을 없앤다. 자른 창은 라벨에 그렇게 쓴다.
        _seen, _W = set(), []
        for lo, hi in WINS:
            h = min(hi, tmax_all)
            if lo >= tmax_all or h - lo < 5:      # 범위 밖이거나 너무 짧다
                continue
            key = (lo, int(round(h)))
            if key in _seen:
                continue
            _seen.add(key); _W.append(key)
        if len(_W) < len(WINS):
            print(f"(궤적 tmax {tmax_all:.0f} ps → 창 {len(WINS)}개 중 "
                  f"**{len(WINS) - len(_W)}개가 범위 밖/중복이라 제거됨**)")
        WINS = _W

        # ⚠ He/Zhu/Mo 2018 — 최대 lag 이 궤적 길이에 가까우면 그 lag 의 **시간원점이 거의
        #   없다**(lag t 에서 원점 수 ≈ (T−t)/Δ). 상한을 총 길이의 30–70 % 아래로 두라는
        #   권고다. 우리는 자르지 않고 **표시**한다 — 자르면 늦은 창 구제가 아예 막힌다.
        # ⛔⛔ 2026-08-27 (Codex 회신 G) — 초판은 70 % 초과 창에 `!` **경고만** 붙이고
        #   추세 계산에는 그대로 넣었다. 회신 판정: *"경고만 붙일 것이 아니라
        #   판정·plateau 검정에서 **제외**해야 한다."* 이유는 lag t 에서 시간원점 수가
        #   ≈(T−t)/Δ 라 t→T 에서 0 으로 간다 — 그 열은 값이 아니라 잡음이다.
        #   → 세 등급으로 나눈다. 등급이 화면에 보이고, 추세는 PRIMARY+SENS 로만 돈다.
        LAG_PRIMARY_FRAC = 0.50      # 주 판정창 — 보수적으로 t₂ ≤ 0.5T
        LAG_WARN_FRAC = 0.70         # 0.5–0.7T = 민감도 분석 · 0.7T 초과 = 시각 진단 전용
        def _tier(w):
            if not tmax_all:
                return "P"
            if w[1] > LAG_WARN_FRAC * tmax_all:
                return "X"                        # exploratory_only — 판정 금지
            if w[1] > LAG_PRIMARY_FRAC * tmax_all:
                return "S"                        # sensitivity
            return "P"                            # primary
        TIER = {w: _tier(w) for w in WINS}
        HOT = {w for w in WINS if TIER[w] == "X"}
        SENS = {w for w in WINS if TIER[w] == "S"}
        # ★ --average 를 같이 주면 **평균 곡선**으로 돈다. 늦은 창이 살아나는 유일한
        #   공짜 수단이다 (개별 런은 lag 이 길어지면 유효 표본이 몇 개 안 남아 붕괴한다).
        scan_items = ([(k, t, y) for k, (t, y) in sorted(avg_curves.items())]
                      if avg_curves else None)
        print("\n창 스캔 — β 가 1 에 가까워지는 창이 있으면 재계산 없이 구제된다"
              + ("  **[시드 평균 곡선]**" if scan_items else ""))
        _mark = {"P": "", "S": "~", "X": "!"}
        head = " ".join((f"{lo}-{hi}" + _mark[TIER[(lo, hi)]]).rjust(8) for lo, hi in WINS)
        print(f"{'case':34s} {head}   tmax")
        if HOT or SENS:
            print(f"   창 등급 (Codex 회신 G) — lag 이 길수록 그 lag 의 시간원점이 "
                  f"≈(T−t)/Δ 로 **0 에 수렴한다**:")
            print(f"     (표시없음) **primary** t₂ ≤ {LAG_PRIMARY_FRAC:.0%}·T — 판정은 이것으로만")
            if SENS:
                print(f"     `~` sensitivity {LAG_PRIMARY_FRAC:.0%}–{LAG_WARN_FRAC:.0%}·T — 민감도 분석용")
            if HOT:
                print(f"     `!` **exploratory_only** t₂ > {LAG_WARN_FRAC:.0%}·T — "
                      f"**추세 계산에서 제외됐다.** 화면 진단용이지 판정·plateau·오차막대에 쓰지 말 것")
        print("   (행: β · 절편 c [Å²] · 기울기 m [Å²/ps] · **D_inc** = 창 구간 증분기울기/6)")
        print("   ★ **D_inc 가 주 판정축이다** (2026-08-27 Codex 회신 F 반영) — 상수 절편이"
              " 대수적으로 소거되므로")
        print("     케이지 절편이면 창이 바뀌어도 **평평**하고, 진짜 t^α 면 계속 움직인다."
              " c 행은 t=0 외삽이라 보조다.")
        def _spearman(v):
            vv = [x for x in v if x is not None]
            if len(vv) < 4:
                return 0.0
            import statistics as _st
            r = sorted(range(len(vv)), key=lambda i: vv[i])
            rank = [0.0] * len(vv)
            for pos, i in enumerate(r):
                rank[i] = float(pos)
            x = [float(i) for i in range(len(vv))]
            mx, mr = _st.mean(x), _st.mean(rank)
            num = sum((a - mx) * (b - mr) for a, b in zip(x, rank))
            den = (sum((a - mx) ** 2 for a in x) * sum((b - mr) ** 2 for b in rank)) ** 0.5
            return num / den if den > 1e-30 else 0.0

        trends = []
        for _it in (scan_items if scan_items else files):
            if scan_items:
                tag, t, y = _it
            else:
                d = json.load(open(_it))
                t, y = _curve(d, a.mto, _it, a.rebuild_mto)  # ⚠ 이 루프의 변수는 _it 다 (f 를 넘기면 남의 경로)
                if not t or not y:
                    continue
                tag = case_label(_it)
            cells, ints, slps, dincs = [], [], [], []
            for lo, hi in WINS:
                b = loglog_slope(t, y, lo, hi)
                cells.append("   —".rjust(8) if b is None else f"{b:8.2f}")
                lf = lin_fit(t, y, lo, hi)
                ints.append("   —".rjust(8) if lf is None else f"{lf[1]:8.2f}")
                slps.append("   —".rjust(8) if lf is None else f"{lf[0]:8.3f}")
                # ★ D_inc — **상수 절편이 대수적으로 빠지는** 축 (Codex 회신 F 권고).
                #   MSD(t2)−MSD(t1) 은 c 를 소거하므로, c 가 상수 케이지면 창을 옮겨도
                #   평평하다. t^α 면 D_inc ∝ t^(α−1) 로 계속 움직인다.
                di = d_incremental(t, y, lo, hi)
                dincs.append("   —".rjust(8) if di is None else f"{di:8.3f}")
            print(f"{tag:34s} {' '.join(cells)}   {max(t):.0f}")
            print(f"{'  └ c [Å²]':34s} {' '.join(ints)}")
            print(f"{'  └ m [Å²/ps]':34s} {' '.join(slps)}")
            print(f"{'  └ ★D_inc [Å²/ps]/6':34s} {' '.join(dincs)}")
            # ── 추세 통계 (⚠⚠ 2026-08-11 재검토로 **자동 판정 → 진단 제안** 격하) ──
            #   MC 4000회 재검토 실측이 초판 규칙을 죽였다:
            #   · 중첩창 6개의 유효 표본은 n_eff ≈ 3.2 (corr(2-50,10-50)=+0.97) —
            #     Spearman 임계 ±0.6 은 iid 귀무에서도 한쪽당 9% 짜리다.
            #   · 오분류율 8~13%. 특히 'sub-diffusion' 판정은 **느린 전이(D 는 존재,
            #     창만 이르다) 대비 동전(47~50%)** — 처방이 정반대인 세 번째 모형을
            #     초판이 아예 몰랐다 (제거 vs 창 이동).
            #   · 초판 CAGE 분기는 c 를 아예 안 봤다 — 자기 문서("c 행이 가른다")와 모순.
            #     lpsocl/T600 이 c=−4.85(비물리)로 CAGE 를 받은 게 그 구멍이다.
            #   확정은 **MTO 곡선**으로만 한다. 아래는 제안이지 판정이 아니다.
            bv0 = [loglog_slope(t, y, lo, hi) for lo, hi in WINS]
            lfv = [lin_fit(t, y, lo, hi) for lo, hi in WINS]
            triples = [(w, b, lf) for w, b, lf in zip(WINS, bv0, lfv)
                       if b is not None and lf is not None]
            # 비물리 창(절편 c<0)은 추세에서 **버린다** — 순위 매길 대상이 아니다
            # ⛔ 2026-08-27 — `exploratory_only`(lag > 0.7·T) 창도 **여기서 뺀다.**
            #   초판은 화면에만 `!` 를 찍고 추세에는 넣었다. 그 창은 시간원점이 거의 없어
            #   c·m 이 잡음이고, 중첩창 6개 중 둘이 그런 열이면 Spearman 이 그쪽으로 끌린다.
            valid = [(w, b, lf) for w, b, lf in triples if lf[1] >= 0 and TIER.get(w) != "X"]
            n_drop = len(triples) - len(valid)
            n_drop_x = sum(1 for w, _b, _l in triples if TIER.get(w) == "X")
            if len(valid) >= 4:
                bv = [b for _w, b, _l in valid]
                mv = [l[0] for _w, _b, l in valid]
                cv = [l[1] for _w, _b, l in valid]
                tb, tm, tc = _spearman(bv), _spearman(mv), _spearman(cv)
                dm = 100.0 * (mv[-1] - mv[0]) / mv[0] if mv[0] else float("nan")
                # ★ 잔차 검정 — 재검토가 찾은 **실제로 갈리는 통계**. 각 창의 (c,m) 직선이
                #   함의하는 log-log 기울기 β_imp 와 관측 β 의 최대 편차. cage 면 전 창
                #   일치한다 (modelc/700 실측 |Δβ|≤0.025 · cage joint p=0.935).
                dbmax = 0.0
                for (lo_, hi_), b, (m_, c_, _r2) in valid:
                    xx = [x for x in t if lo_ <= x <= hi_ and x > 0]
                    yy = [c_ + m_ * x for x in xx]
                    bi = loglog_slope(xx, yy, lo_, hi_)
                    if bi is not None:
                        dbmax = max(dbmax, abs(b - bi))
                cage_like = tb > 0.6 and abs(dm) < 15 and dbmax <= 0.05
                sub_like = abs(tb) < 0.45 and tm < -0.6 and tc > 0.6
                if cage_like and not sub_like:
                    v = f"케이지 절편 **시사** (잔차 |Δβ|max {dbmax:.3f} ≤ 0.05)"
                elif sub_like and not cage_like:
                    v = "sub-diffusion **또는 느린 전이** — 요약값으로 구분 불가(동전)"
                else:
                    v = "판별 불가"
                trends.append((tag[:26], tb, dm, tm, tc, dbmax, n_drop, v))
        print("  ⚠ 창을 늦추면 통계 점수는 줄어든다 — β 가 1 이어도 창 안 데이터가")
        print("    너무 적으면(점 3개 미만) '—' 로 나온다. tmax 가 창보다 작아도 마찬가지.")
        # ★★ 2026-08-11 — 눈으로 읽지 말고 **추세로 판정**한다. 실측에서 이 판정이
        #   β 게이트와 **반대로** 나오는 사례가 나왔다 (아래 trend_verdict 주석 참조).
        if trends:
            print()
            print("  ═══ 추세 **제안** (자동 판정 아님 — 2026-08-11 재검토로 격하) ═══")
            print(f"  {'case':26s} {'β추세':>6s} {'m변화%':>7s} {'m추세':>6s} {'c추세':>6s} "
                  f"{'|Δβ|max':>8s} {'제외창':>5s}  제안")
            for tag, tb, dm, tm, tc, dbm, nd_, v in trends:
                print(f"  {tag:26s} {tb:+6.2f} {dm:+7.1f} {tm:+6.2f} {tc:+6.2f} "
                      f"{dbm:8.3f} {nd_:5d}  {v}")
            print()
            print("  ⚠ '제외창' 은 절편 c<0(비물리) **+ exploratory_only(lag > "
                  f"{LAG_WARN_FRAC:.0%}·T)** 를 합친 수다 (2026-08-27 Codex 회신 G).")
            print("  ⚠ 이 표는 **제안**이다 — MC 재검토 실측: 오분류 8~13%, 중첩창 n_eff≈3.2,")
            print("    'sub-diffusion' 제안은 느린 전이(D 존재·창만 이르다) 대비 **동전**이다.")
            print("    느린 전이면 처방이 정반대다: 점 제거가 아니라 **창 이동/연장**.")
            print("  · 케이지 시사의 실근거는 Spearman 이 아니라 **잔차 검정**(|Δβ|max ≤ 0.05)이다.")
            print("  ⛔ 아레니우스에서 점을 넣고 빼는 결정은 이 표로 하지 않는다 —")
            print("    ① MTO 곡선으로 재판정 ② 그래도 애매하면 **세 계 같은 온도 집합** 유지가")
            print("    점 제거보다 우선한다 (비대칭 가감은 Ea 비교를 통째로 깨뜨린다).")
        print()
        print("  ★ c 행은 β 보다 정보가 많지만 **만능이 아니다** (2026-08-11 재검토 반영):")
        print("    · cage vs 멱함수는 가르지만, 멱함수 vs **느린 전이**는 요약값으로 못 가른다.")
        print("    · 단일 시간원점의 sd(c)는 iid-OLS 표준오차의 10~40배다 — c 의 창간 요동을")
        print("      과해석하지 말 것. 확정은 MTO 곡선으로.")
        print("     · c 가 창 따라 **거의 상수** + m 도 상수 + β 만 1 로 올라감")
        print("       → 케이지 절편이다. MSD = c + 6Dt 로 이미 직선이고 **D 는 인용 가능**하다.")
        print("         (D 는 자유 절편 맞춤의 **기울기**에서 나오므로 c 에 오염되지 않는다.)")
        print("     · c 가 창 따라 **커지고** m 이 **떨어지며** β 가 모든 창에서 그대로")
        print("       → 진짜 sub-diffusion 이다. 그때만 D 인용 금지가 맞다.")
        print("     ⚠ R² 로는 둘을 못 가른다 — 두 모형 다 0.99 를 넘는다. c 를 볼 것.")

    print()
    if held:
        # ⛔ 회신 AK Q5 — **'정의되지 않음'과 '정밀도 부족'을 한 줄로 합치지 않는다.**
        #   처방이 갈린다: 전자는 프로토콜을 고치고, 후자는 시드·길이를 늘린다.
        print(f"⏸ **HOLD {len(held)}/{len(files)}** — 값은 정의되지만 **정밀도가 부족**하다.")
        for tag, v in held:
            print(f"   {tag}: {v}")
        print("   처방: 시드 추가 또는 생산길이 연장 (프로토콜은 그대로).")
        print("   ⚠ 시드 추가 규칙: kb/methodology/beta_gate_seed_policy.md "
              "— '통과할 때까지 다시' 금지.")
        print()
    if bad:
        # ⚠⚠ 2026-08-11 문구 정정 — "확산 영역이 아니다" 는 **β 가 말할 수 있는 것보다 세다**.
        #   β<0.8 은 (a) 진짜 sub-diffusion 이거나 (b) MSD 절편이 창끝의 ~6% 를 넘은 것이다.
        #   둘을 가르는 건 --scan 의 **c 행**이지 β 값이 아니다.
        print(f"⛔ **no-value {len(bad)}/{len(files)}** — 선언한 창에서 값이 **정의되지 않는다.**")
        for tag, v in bad:
            print(f"   {tag}: {v}")
        print("   ⛔ 여기서 곧바로 'D 인용 금지' 로 가지 말 것 — **--scan 의 c 행을 먼저 본다**:")
        print("     · c 가 창 따라 상수면 케이지 절편이다. D 는 자유 절편 맞춤의 기울기라 무사하다.")
        print("     · c 가 창 따라 커지면 그때가 진짜 sub-diffusion 이고 D 인용 금지가 맞다.")
        print("   처방: ① --scan 으로 c 판별 ② 표본(이온 수·시간원점)을 늘린다 "
              "③ 그래도 c 가 크면 그 온도를 Arrhenius 에서 뺀다")
        print("   ⚠ ③ 은 캠페인 규약(600/800/1000 3점)의 예외다 — 근거를 db 에 남길 것.")
    elif not unmeasured and not held:
        print(f"✅ {len(files)}개 전부 D_inc plateau — D 인용 가능 "
              f"(⚠ Ea 는 별개다: 온도별 상·기전 일치와 구간 Ea 양립을 Arrhenius 단계에서 본다).")

    if unmeasured:
        # ⛔ 못 잰 것과 통과한 것을 **한 줄로 합치지 않는다**. 합치면 "3개 중 3개 확산"
        #   처럼 읽혀서, 게이트를 통과했다고 믿고 D 를 인용하게 된다.
        print(f"⛔ **{len(unmeasured)}/{len(files)} 개는 β 를 아예 재지 못했다 — 통과가 아니다.**")
        for tag, why in unmeasured:
            print(f"   {tag}: {why}")
        print("   msd.json 에 times_ps/msd_A2 배열이 없다 (D 만 저장된 옛 판이거나 "
              "MSD 저장 단계가 빠진 런).")
        print("   → 그 런의 D 는 **이 게이트를 통과한 값이 아니다.** 배열을 다시 만들거나"
              " (tools/ionic/ 의 MSD 산출 단계 재실행) 다른 런으로 비교할 것.")
        if len(unmeasured) == len(files):
            print("   ⚠ 전부 못 쟀다 — 이 실행은 **아무것도 판정하지 않았다**.")

    # ── --framework: 골격(비-Li)이 녹고 있나 ────────────────────────────
    if a.framework_split:
        print("\n결합S vs 자유S 분리 β — 무엇이 움직이는 부격자인가")
        print(f"  분류: 첫 프레임의 P–S/B–S 결합창 (b2o3_all_bond_lengths 와 동일 규약)")
        print(f"  판정(사전 고정): bonded-S β<{SPLIT_RIGID} & (free-S 또는 Cl ≥{SPLIT_RIGID})"
              " → 자유 음이온 부격자 이동")
        print(f"\n{'case':30s} {'그룹':>9s} {'n':>4s} {'beta':>6s} {'MSD끝':>8s}")
        _vs, _us = {}, {}
        for f in files:
            tag = LBL.get(f, case_label(f))
            try:
                _sf = json.load(open(f)).get("save_fs")
            except (OSError, ValueError):
                _sf = None
            r = framework_split(f, lo, hi, save_fs=_sf)
            if r is None:
                print(f"{tag:30s} — 궤적 없음"); continue
            u = r.get("unit") or {}
            if u.get("verdict") != "no_BS3":
                um = {"BS3_driven": "★ BS₃ 단위가 원인 — 도핑이 넣은 것이 움직인다",
                      "host_wide": "⛔ 호스트 PS₄ 도 움직인다 — 계 전체가 무름 (UMA 의심↑)",
                      "both_mobile": "⚠ BS₃ 가 더 심하나 PS₄ 도 움직인다",
                      "inconclusive": "▫ 단위 판정 불충분"}[u["verdict"]]
                print(f"{tag:30s} {'[단위]':>9s} BS₃/PS₄ = {u['ratio_BS3_over_PS4']:.2f}"
                      f"  (PS₄ β={u['PS4_beta']}, MSD {u['PS4_msd_end']:.1f}"
                      f" | BS₃ β={u['BS3_beta']}, MSD {u['BS3_msd_end']:.1f})")
                print(f"{'':30s} {'':>9s} → {um}")
                _us[u["verdict"]] = _us.get(u["verdict"], 0) + 1
            for g in ("PS4_unit", "BS3_unit", "S_on_P", "S_on_B",
                      "bonded_S", "free_S", "Cl", "P", "B", "O"):
                if g not in r["groups"]:
                    continue
                gg = r["groups"][g]
                bstr = f"{gg['beta']:.2f}" if gg["beta"] is not None else "—"
                note = "" if gg["judged"] else "  (n<8 참고용)"
                print(f"{tag:30s} {g:>9s} {gg['n']:4d} {bstr:>6s} "
                      f"{gg['msd_end_A2']:8.1f}{note}")
            mk = {"free_anion_sublattice_mobile": "★ 자유 음이온 부격자 이동 — 서술③ 지지",
                  "polyanion_frame_mobile": "⛔ 폴리음이온 골격 자체가 움직임 — 서술③ 기각",
                  "inconsistent_with_elementwise": "⚠ 원소별 검사와 모순 — 재조사",
                  "insufficient": "▫ 판정 불충분"}[r["verdict"]]
            print(f"{'':30s} → {mk}\n")
            _vs[r["verdict"]] = _vs.get(r["verdict"], 0) + 1
        print("  합계(부격자): " + " · ".join(f"{k} {v}" for k, v in sorted(_vs.items())))
        if _us:
            print("  ★ 합계(단위 BS₃ vs PS₄): "
                  + " · ".join(f"{k} {v}" for k, v in sorted(_us.items())))
            print(f"    기준(사전 고정): 비 ≥{UNIT_RATIO_HI} & PS₄ β<{SPLIT_RIGID} → BS3_driven / "
                  f"비 ≤{UNIT_RATIO_LO} & PS₄ β≥{SPLIT_RIGID} → host_wide")

    if a.framework_com:
        print("\n골격 흐름 vs 재배열 — 골격이 움직일 때 **구제 가능한가**")
        print("  골격 질량중심을 매 프레임 빼고 다시 잰다 (재계산 0, 궤적만 있으면 됨).")
        print(f"  남는 몫 ≤{DRIFT_KEEP:.0%} → 흐름 지배(공동계에서 Li 구제 가능) · "
              f"≥{DRIFT_LOST:.0%} → 자리 재배열(구제 불가)")
        print("  ⛔ '구제 가능' 이 곧 '인용 가능' 은 아니다 — 공동계 Li D 를 **게이트에")
        print("     다시 통과시켜야** 한다.")
        print(f"\n{'case':34s} {'골격MSD':>9s} {'COM제거후':>10s} {'남는몫':>7s} "
              f"{'Li(원)':>8s} {'Li(공동계)':>10s}  판정")
        _cnt = {}
        for f in files:
            tag = LBL.get(f, case_label(f))
            try:
                _sf = json.load(open(f)).get("save_fs")
            except (OSError, ValueError):
                _sf = None
            r = framework_com_split(f, save_fs=_sf)
            if r is None:
                print(f"{tag:34s} {'—':>9s} {'—':>10s} {'—':>7s} {'—':>8s} {'—':>10s}"
                      "  궤적 없음 — 판정 불가")
                _cnt["none"] = _cnt.get("none", 0) + 1
                continue
            mk = {"drift_dominated": "⭕ 흐름 — 구제 가능",
                  "mixed": "⚠ 섞임 — 구제 불확실",
                  "rearrangement": "⛔ 재배열 — 구제 불가",
                  "framework_static": f"· 골격이 거의 안 움직임 (MSD<{DRIFT_MIN_MSD:g} Å²) — 판정 안 함",
                  }[r["verdict"]]
            _cnt[r["verdict"]] = _cnt.get(r["verdict"], 0) + 1
            print(f"{tag:34s} {r['frame_total']:9.1f} {r['frame_internal']:10.1f} "
                  f"{r['kept_frac']:7.2f} {r['li_total']:8.1f} {r['li_internal']:10.1f}  {mk}")
        print("\n  합계: " + " · ".join(f"{k} {v}" for k, v in sorted(_cnt.items())))
        if _cnt.get("framework_static"):
            print(f"  · {_cnt['framework_static']}건은 골격 MSD 가 {DRIFT_MIN_MSD:g} Å² 미만이라 "
                  f"**'흐름이냐 재배열이냐' 가 성립 안 한다** — 골격 β 검사 결과로 판단할 것.")
        if _cnt.get("rearrangement"):
            print("  ⛔ 재배열이 하나라도 있으면 그 온도점의 Li D 는 공동계로도 못 살린다.")
        if _cnt.get("drift_dominated"):
            print("  ⭕ 흐름 지배분은 공동계 Li MSD 로 D 를 다시 뽑고 **β 게이트를 새로** 걸 것.")

    if a.framework:
        print("\n골격(비-Li) 검사 — Li 만 움직여야 한다")
        print("  왜: Zhang npj 2026 이 MACE-MP-0 의 LGPS 골격이 **1050–1500 K 에서**")
        print("      인위적으로 녹는 걸 잡고 샘플링을 1050 K 로 낮췄다.")
        print("      우리 아레니우스 상한 1000 K 가 그 선 바로 아래다.")
        print(f"  ⚠ 원소 {FRAMEWORK_MIN_N}개 미만은 **판정에서 뺀다** — 2~3개짜리 평균은")
        print(f"     한 원자가 한 번 뛰면 β 가 1 을 넘는다(단일 대형 사건). 값은 참고로 찍는다.")
        print(f"\n{'case':34s} {'worst':>7s} {'beta':>6s} {'ratio':>7s} {'MSD_Li':>8s}  판정")
        fw_bad, fw_none = [], []
        for f in files:
            try:
                d = json.load(open(f))
            except (OSError, ValueError):
                continue
            tag = LBL.get(f, case_label(f))
            if a.from_traj and _elem_msd(d) and not (
                    d.get("n_atoms_per_elem")
                    or (d.get("msd_data") or {}).get("n_atoms_per_elem")):
                npe = n_per_elem_from_traj(f)
                if npe:
                    d["n_atoms_per_elem"] = npe
                    try:
                        _d = json.load(open(f)); _d["n_atoms_per_elem"] = npe
                        json.dump(_d, open(f, "w"))
                    except (OSError, ValueError):
                        pass
            r = framework_check(d, lo, hi)
            if r is None and a.from_traj:
                got = elem_msd_from_traj(f, save_fs=d.get("save_fs"))
                if got:
                    d.setdefault("times_ps", got["times_ps"])
                    d["msd_per_elem_A2"] = got["msd_per_elem_A2"]
                    d["n_atoms_per_elem"] = got.get("n_atoms_per_elem", {})
                    r = framework_check(d, lo, hi)
            if r is None:
                fw_none.append(tag)
                print(f"{tag:34s} {'—':>6s} {'—':>7s} {'—':>6s} {'—':>8s}  종별 MSD 없음")
                continue
            we = r["worst_el"]
            b = r["frame"][we]["beta"] if we else None
            n = r["frame"][we].get("n_atoms") if we else None
            mark = {"framework_rigid": "⭕", "framework_mobile": "⚠",
                    "framework_melting": "⛔", "sample_too_thin": "▫"}[r["verdict"]]
            lab = f"{we}({n})" if we and n else (we or "—")
            print(f"{tag:34s} {lab:>7s} {('—' if b is None else f'{b:.2f}'):>6s} "
                  f"{r['worst_ratio']:>7.3f} "
                  f"{r['li_msd_end_A2']:>8.1f}  {mark} {r['verdict']}{thin_note(r)}")
            if a.framework_elems:
                for line in framework_elem_table(r):
                    print(line)
            if r["verdict"] != "framework_rigid":
                fw_bad.append((tag, r))
        print()
        for tag, r in fw_bad:
            print(f"  {tag}: {framework_verdict_text(r['verdict'])}")
        if fw_none:
            # ⛔ 종별 MSD 가 없는 것을 "골격 안 녹았다"로 읽으면 이 검사는 없느니만 못하다.
            print(f"⛔ **{len(fw_none)}/{len(files)} 개는 골격을 아예 보지 못했다 — 통과가 아니다.**")
            print("   종별 MSD(msd_per_elem_A2)가 파일에 없다.")
            print("   → **`--from_traj` 를 붙이면** 옆의 traj.xyz 에서 다시 뽑는다(재계산 0, 읽기만).")
            print("      traj.xyz 도 없는 런은 원리적으로 골격 검사를 못 한다 — 새로 돌려야 한다.")
        elif not fw_bad:
            print(f"✅ {len(files)}개 전부 골격이 고정돼 있다 — 그 온도의 Li D 는 진짜 확산이다.")


if __name__ == "__main__":
    # ⛔⛔ 2026-08-27 — 옛 판은 `main()` 만 부르고 **반환값을 버렸다.** 그래서
    #   `--selftest` 가 FAIL 해도, glob 이 아무것도 못 잡아도, 아무것도 못 재도
    #   **종료코드가 항상 0** 이었다. CI·watch·체인 스크립트에서 실패가 성공으로 읽힌다.
    #   (mlip_committee.py 가 2026-08-26 에 똑같은 버그였다 — 같은 함정을 두 번 팠다.)
    sys.exit(main() or 0)


