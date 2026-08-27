#!/usr/bin/env python3
"""msd_diffusive_check.py — MSD 가 **진짜 확산 영역**인지 판정한다 (인용 게이트).

왜 필요한가
  D 는 MSD 를 `fit_window_ps` 에서 직선 맞춤해 얻는데, 그 창이 확산 영역이 아니면
  **케이지 진동·드리프트를 확산으로 오독**한다. 실측 두 건:
    · comp2 disorder d=0.5 — 600 K D 가 1.4~2.3e-05 cm²/s (comp1 의 1000 K 값과 동급),
      D(1000)/D(600) 가 1.98~5.6 밖에 안 됨 (0.276 eV 면 8.5 배 기대)
    · comp1 seed3 — D(600) 1.36e-06 ≈ D(800) 1.37e-06 (비 1.007). 물리적으로 불가능.
  둘 다 "Ea 를 냈다"까지는 갔지만 **그 Ea 를 인용하면 안 되는** 상태였다.

판정
  log-log 기울기 β = d(log MSD)/d(log t) 를 창 안에서 잰다.
    β ≈ 1.0        확산 (Fickian) — 인용 가능
    β < 0.8        아직 케이지/천이 — **인용 금지**, 창을 늦추거나 prod 를 늘려라
    β > 1.2        드리프트/탄도 — 질량중심 표류 의심

⚠ β 만으로는 부족하다. **MSD 절대 크기**도 본다: 창 끝의 MSD 가 이웃 Li–Li 거리²
  (~3 Å² 정도) 보다 작으면 이온이 자기 자리를 못 벗어난 것이라 β 가 1 이어도 통계가 없다.

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


def lin_fit(t, y, lo, hi):
    """[lo,hi] 에서 MSD = c + m·t 를 자유 절편으로 맞춘다. (m, c, R²) 또는 None.

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
    pts = [(a, b) for a, b in zip(t, y) if lo <= a <= hi]
    if len(pts) < 3 or pts[-1][0] - pts[0][0] <= 0:
        return None
    return (pts[-1][1] - pts[0][1]) / (6.0 * (pts[-1][0] - pts[0][0]))


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


def directional_msd_tensor(traj_path, save_fs=100.0, species="Li",
                           prefix_ps=None, max_lag_frac=0.5, n_origin=200):
    """`traj.xyz` 에서 **확산텐서** `M_αβ(t) = ⟨Δr_α Δr_β⟩` 를 낸다 (다중 시간원점).

    왜 (2026-08-27, 교차리뷰 G/H): 우리 3×3×1 은 **이방 복제**라 scalar `L` 도 `m/6` 도
      자동으로 정당화되지 않는다. *"수송이 등방인지 방향별 MSD 로 먼저 확인해야 한다."*
      ⚠ 회신 H 정정: 이방계에서도 총 MSD 기울기 `m/6` 은 **수학적으로 `Tr(D)/3`** 이다.
        틀린 계산이 아니라 **"등방 D" 가 아니라 trace-average 라고 불러야** 하는 문제다.

    반환 `(t_ps, M)` — `M[a][b]` 가 각각 길이 len(t_ps) 인 리스트.
      `D_αβ = ½ · dM_αβ/dt`  (성분당 1차원이므로 **분모가 6 이 아니라 2** 다)

    ⛔ 이 함수가 못 하는 것:
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
        frames = frames[:keep]
        if len(frames) < 20:
            return None
    idx = [i for i, s in enumerate(frames[0].get_chemical_symbols()) if s == species]
    if not idx:
        return None
    pos = _np.array([f.get_positions()[idx] for f in frames])   # (nframe, nion, 3)
    nf = len(pos)
    max_lag = max(3, int(nf * max_lag_frac))
    # 시간원점을 균등 추출 — 전부 쓰면 O(nf²) 라 800 ps 에서 느리다
    origins = _np.unique(_np.linspace(0, nf - max_lag - 1,
                                      min(n_origin, nf - max_lag), dtype=int))
    if len(origins) < 2:
        return None
    lags = _np.arange(1, max_lag)
    M = _np.zeros((3, 3, len(lags)))
    for k, L in enumerate(lags):
        d = pos[origins + L] - pos[origins]                 # (norig, nion, 3)
        d = d.reshape(-1, 3)
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
        for pp in pre:
            got = directional_msd_tensor(traj, save_fs=sf, prefix_ps=pp)
            if got is None:
                print(f"{str(traj.parent)[-30:]:30s} {(pp or 'all'):>8} "
                      f" ⛔ 프레임 부족 — 이 prefix 는 아직 못 잰다")
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
    if save_fs is None:
        save_fs, assumed = 100.0, True
    else:
        assumed = False
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
          + (f" (save_fs={save_fs:g} fs **가정**)" if assumed else f" (save_fs={save_fs:g} fs)"))
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
            d["_elem_msd_source"] = f"recomputed from traj.xyz (save_fs={save_fs:g} fs)"
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
        frames = _read(str(traj), index=":")
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
    # 케이지: MSD = c + m t 로 절편이 큰 것 (β < 1)
    cage = {"times_ps": t, "msd_Li_A2": [12.0 + 0.7 * u for u in t], "D_Li_cm2_s": 1.2e-5}
    # ⛔ 문제의 모양: D 는 있는데 MSD 배열이 없다
    nomsd = {"D_Li_cm2_s": 7.4e-6}

    out = run([lin, lin])
    chk("✅ 2개 전부 확산 영역" in out, "[양성] 확산 곡선 2개 → ✅")

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
    chk("✅ 2개 전부 확산 영역" in out,
        "[양성] 같은 파일을 --mto 없이 주면 **바로 잰다** (재계산 불필요 확인)")

    out = run([cage, cage])
    chk("입증하지 못했다" in out, "[양성] 절편 큰 곡선은 케이지로 잡는다")
    chk("✅" not in out, "[음성] 케이지인데 ✅ 가 같이 찍히지 않는다")

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
        chk(directional_msd_tensor(_d / "traj.xyz", save_fs=100.0, prefix_ps=0.5) is None,
            "[음성] prefix 가 너무 짧으면 None — 프레임 20개 미만은 재지 않는다")
        chk(directional_msd_tensor(_d / "traj.xyz", save_fs=100.0, species="Xx") is None,
            "[음성] 없는 원소를 달라면 None — 빈 배열로 0 을 반환하지 않는다")
        import shutil as _sh; _sh.rmtree(_d, ignore_errors=True)
    except ImportError:
        print("  · (ase/numpy 없음 — 방향별 텐서 selftest 건너뜀)")

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
    ap.add_argument("--framework", action="store_true",
                    help="골격(비-Li) 원소가 녹고 있는지 같이 본다. Zhang npj 2026 이 "
                         "MACE-MP-0 의 LGPS 골격이 1050 K 부터 인위적으로 녹는 걸 잡았고, "
                         "우리 아레니우스 상한 1000 K 가 그 바로 아래다. 골격이 녹으면 "
                         "Li 의 'D' 는 확산이 아니라 구조 붕괴다.")
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
    ap.add_argument("--prefixes", default="",
                    help="누적 prefix [ps] 쉼표목록 (예: 100,200,400). 각 시점에서 다시 잰다 "
                         "— D_inc plateau 가 이미 왔으면 완주 전에 끊을 수 있다.")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.directional:
        return cmd_directional(a)
    if not a.glob:
        ap.error('--glob 이 필요하다 (또는 --selftest)')

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
            lab = case_label(f)
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
          + f"창 {lo}–{hi} ps · β=1 확산 · β<{BETA_OK[0]} 케이지 · "
          f"창끝 MSD < {MSD_MIN_A2} Å² 면 통계 부족")
    # ⚠⚠ β<0.8 을 곧바로 '케이지' 로 읽지 말 것 — **창끝 MSD 를 같이 본다.**
    #   2026-08-11 귀무분포 검정(tools/ionic/beta_null_test.py): 케이지가 0 인 이상
    #   브라운 운동을 Li 27개·200 ps 로 재면 창 2–50 에서 β = 1.01 (5–95% 0.86–1.14),
    #   0.8 미만이 **1.0%** 뿐이다. 즉 이 창의 β<0.8 은 표본 부족이 아니라 진짜다.
    #   반면 늦은 창(50–200)에서는 이상 계도 10%가 0.8 아래로 떨어진다 — 그 창의
    #   β 로 '구제' 판정을 하면 안 된다. 창마다 게이트의 신뢰도가 다르다.
    print(f"{'case':34s} {'D(cm2/s)':>10s} {'beta':>6s} {'MSD@hi':>8s}  판정")
    bad = []
    #: ⛔⛔ 2026-08-17 fail-open — MSD 배열이 없는 런은 `continue` 로 건너뛰고 bad 에도
    #:   안 들어가서, **아무것도 못 쟀는데** 마지막 줄이 "✅ 전부 확산 영역 — D/Ea
    #:   인용 가능" 으로 찍혔다 (lpsocl 작은 셀 3런이 그랬다: β 세 칸이 전부 '—' 인데 ✅).
    #:   못 잰 것은 통과가 아니다. 따로 세서 총평이 ✅ 로 못 가게 막는다.
    unmeasured = []
    for f in files:
        d = json.load(open(f))
        t, y = _curve(d, a.mto, f, a.rebuild_mto)
        D = d.get("D_Li_cm2_s")
        tag = case_label(f)
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
            n_hop = (max(y) / D_HOP_A ** 2) if y else float("nan")   # MSD@end/d²(상한)
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
        verdict = " · ".join(marks) if marks else "✓ 확산"
        if marks:
            bad.append((tag, verdict))
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
    if bad:
        # ⚠⚠ 2026-08-11 문구 정정 — "확산 영역이 아니다" 는 **β 가 말할 수 있는 것보다 세다**.
        #   β<0.8 은 (a) 진짜 sub-diffusion 이거나 (b) MSD 절편이 창끝의 ~6% 를 넘은 것이다.
        #   둘을 가르는 건 --scan 의 **c 행**이지 β 값이 아니다.
        print(f"⚠ **{len(bad)}/{len(files)} 개가 선언한 창에서 Fickian scaling 을 입증하지 못했다.**")
        for tag, v in bad:
            print(f"   {tag}: {v}")
        print("   ⛔ 여기서 곧바로 'D 인용 금지' 로 가지 말 것 — **--scan 의 c 행을 먼저 본다**:")
        print("     · c 가 창 따라 상수면 케이지 절편이다. D 는 자유 절편 맞춤의 기울기라 무사하다.")
        print("     · c 가 창 따라 커지면 그때가 진짜 sub-diffusion 이고 D 인용 금지가 맞다.")
        print("   처방: ① --scan 으로 c 판별 ② 표본(이온 수·시간원점)을 늘린다 "
              "③ 그래도 c 가 크면 그 온도를 Arrhenius 에서 뺀다")
        print("   ⚠ ③ 은 캠페인 규약(600/800/1000 3점)의 예외다 — 근거를 db 에 남길 것.")
    elif not unmeasured:
        print(f"✅ {len(files)}개 전부 확산 영역 — D/Ea 인용 가능.")

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
            tag = case_label(f)
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
            tag = case_label(f)
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
                  "rearrangement": "⛔ 재배열 — 구제 불가"}[r["verdict"]]
            _cnt[r["verdict"]] = _cnt.get(r["verdict"], 0) + 1
            print(f"{tag:34s} {r['frame_total']:9.1f} {r['frame_internal']:10.1f} "
                  f"{r['kept_frac']:7.2f} {r['li_total']:8.1f} {r['li_internal']:10.1f}  {mk}")
        print("\n  합계: " + " · ".join(f"{k} {v}" for k, v in sorted(_cnt.items())))
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
            tag = case_label(f)
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
            thin = r["frame"].get("_thin") or []
            note = ("  [제외 " + ",".join(
                f"{e}({r['frame'][e].get('n_atoms')},β{r['frame'][e]['beta']:.2f})"
                for e in thin if r['frame'][e]['beta'] is not None) + "]") if thin else ""
            print(f"{tag:34s} {lab:>7s} {('—' if b is None else f'{b:.2f}'):>6s} "
                  f"{r['worst_ratio']:>7.3f} "
                  f"{r['li_msd_end_A2']:>8.1f}  {mark} {r['verdict']}{note}")
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


