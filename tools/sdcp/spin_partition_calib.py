#!/usr/bin/env python3
"""spin_partition_calib.py — 스핀 국재화 F 의 **두 형태를 같은 격자에서** 재고 차이를 낸다.

⛔⛔ 왜 만들었나 (2026-09-02 · 회신 X P0-1 · 1저자 선택 ③)

  폴라론 pilot 이 보고하는 F 는 **원자 population 형**이다:

      F_G^out = Σ_{A∈G} |s_A| / Σ_A |s_A| ,   s_A = ∫ w_A(r) Δρ(r) dr   (부호 있음)

  비준 결정문이 정의한 것은 **실공간 적분형**이다:

      F_G^in  = ∫ W_G(r) |Δρ(r)| dr / ∫ |Δρ(r)| dr ,   W_G = Σ_{A∈G} w_A

  절댓값이 원자 **밖**(out)이냐 적분 **안**(in)이냐가 다르다. 삼각부등식
  `Σ_A|∫w_AΔρ| ≤ ∫|Δρ|` 은 **원자별 항**에 성립할 뿐이다 — F 는 분자·분모가 둘 다 줄어드는
  비라 **F_out 이 F_in 의 하한이라는 결론은 틀렸다** (회신 Y P0-1 · 2026-09-03 철회).
  반례: 실공간 0.49/0.31/0.20 에서 target 밖에서만 0.10 이 상쇄되면 cancellation_ratio 는
  0.90 인데 population target 은 0.49/0.90 = 0.544 로 0.5 경계를 거짓으로 넘는다.
  ⇒ 비(cancellation_ratio)는 **설명용 QC** 다. 판정은 `direct_comparison_gate` —
    두 형태의 winner · class 경계 통과 · margin 판정 · max|ΔF| 를 **직접** 비교한다.
    (회신 Y Q3 네 조건. 문턱은 소비자 build_v7c_trimer.py 의 PIL_CLASS_MIN ·
     PIL_CLASS_MARGIN · PIL_CALIB_MAX_DF — cube 를 보기 전에 봉인.)

  ⚠ **교란을 없애려고 가중치 계열을 고정한다.** 둘 다 같은 Becke 가중치·같은 격자로
    계산한다. 그래야 차이가 *절댓값 위치* 때문이지 *분할 방식* 때문이 아니다.
    (production 은 Hirshfeld 를 쓴다 — 그래서 이것은 production 값의 재현이 아니라
     **상쇄 손실의 크기 측정**이다. 아래 '못 하는 것' 을 볼 것.)

사용
  python3 tools/sdcp/spin_partition_calib.py --spin_cube <spindens.cube> \\
      --groups groups.json [--json out.json]
  python3 tools/sdcp/spin_partition_calib.py --selftest

  `groups.json` = {"backbone": [0,1,2,...], "sulfonate": [...], "other": [...]}
  (0-based 원자 index — cube 안 원자 순서와 같아야 한다)

⛔ 이 도구가 **못 하는 것**
  · production 의 Hirshfeld F 를 재현하지 않는다. 가중치 계열이 다르다 — 재는 것은
    **같은 계열 안에서 절댓값 위치가 만드는 차이**다. 이 값을 F 로 인용하지 않는다.
    ⇒ 그래서 이 대조가 보증하는 것은 "절댓값 위치가 class 를 바꾸지 않는다" 이고,
      Hirshfeld 분할 자체가 옳은지는 **보증하지 않는다** (회신 Y P1 — 정직한 범위).
  · 격자 오차를 스스로 보정하지 않는다. `qc` 로 **표시**만 한다 (간격·경계 절단·∫Δρ·
    균등 대체 질량). 격자 수렴(dim 을 바꿔 다시 재기)은 호출부 몫이다.
  · 스핀밀도 cube 를 만들지 않는다 — ORCA `%plots` / `orca_plot` 의 몫이다.
  · 원자 분할의 **물리적 타당성**을 판정하지 않는다. Becke 는 기하 분할이다.
  · 두 형태가 **둘 다** 틀린 경우(같은 격자 오차)는 못 본다 — 둘의 일치만 본다.
"""
from __future__ import annotations

import argparse
import json
import math
import sys

# ⚠ 회신 Y P1 — 비-UTF-8 콘솔(기본 Windows)에서 help/selftest 가 죽지 않게 한다.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:                                            # noqa: BLE001
        pass

#: Bragg–Slater 반경 [Å] — Becke 1988 의 원자 크기 조정에 쓴다.
#:  ⚠ H 는 Becke 의 권고대로 0.35 가 아니라 **0.35** 를 그대로 쓴다(원논문 표).
BRAGG = {"H": 0.35, "He": 0.28, "Li": 1.45, "Be": 1.05, "B": 0.85, "C": 0.70,
         "N": 0.65, "O": 0.60, "F": 0.50, "Ne": 0.38, "Na": 1.80, "Mg": 1.50,
         "Al": 1.25, "Si": 1.10, "P": 1.00, "S": 1.00, "Cl": 1.00, "Ar": 0.71,
         "K": 2.20, "Ca": 1.80, "Ni": 1.35, "Nd": 1.85}
Z2SYM = {1: "H", 2: "He", 3: "Li", 4: "Be", 5: "B", 6: "C", 7: "N", 8: "O",
         9: "F", 10: "Ne", 11: "Na", 12: "Mg", 13: "Al", 14: "Si", 15: "P",
         16: "S", 17: "Cl", 18: "Ar", 19: "K", 20: "Ca", 28: "Ni", 60: "Nd"}
BOHR_A = 0.529177210903


def read_cube(path):
    """Gaussian cube → dict. **원점·복셀 벡터·원자를 버리지 않는다.**

    ⚠ `tools/ionic/plot_cube_compare.py` 에도 `read_cube` 가 있지만 그것은 격자 배열만
      돌려준다(그 도구는 그림용이라 그걸로 충분하다). 적분에는 dV 와 원자 좌표가
      있어야 해서 여기서 온전히 읽는다.
    """
    L = open(path, encoding="utf-8", errors="replace").read().splitlines()
    if len(L) < 7:
        raise SystemExit("⛔ cube 가 너무 짧다: %s" % path)
    nat = int(L[2].split()[0])
    org = [float(x) for x in L[2].split()[1:4]]
    n, vec = [], []
    for i in range(3):
        w = L[3 + i].split()
        n.append(int(w[0])); vec.append([float(x) for x in w[1:4]])
    # ⚠ cube 규약: 원자 수가 **음수**면 궤도 cube 라 데이터 앞에 한 줄이 더 있다.
    #   그것을 모르고 읽으면 격자가 한 칸 밀린다 (조용히 틀린다).
    if nat < 0:
        raise SystemExit("⛔ 원자 수가 음수다 (궤도 cube) — 스핀밀도 cube 를 주십시오")
    at = []
    for i in range(nat):
        w = L[6 + i].split()
        z = int(w[0])
        # ⚠ cube 원자 줄은 `Z  charge  x  y  z` (5칸)다. 종전엔 `w[4:7]` 로 읽어
        #   z 하나만 잡았고, 그러면 모든 원자가 같은 좌표로 보여 "겹쳤다" 로 죽었다
        #   (2026-09-02 실측). charge 칸이 없는 4칸 판도 있어 둘 다 받는다.
        if len(w) >= 5:
            _xyz = w[2:5]
        elif len(w) == 4:
            _xyz = w[1:4]
        else:
            raise SystemExit("⛔ cube 원자 줄을 못 읽는다 (%d칸): %r" % (len(w), ln))
        at.append({"Z": z, "sym": Z2SYM.get(z, "X"),
                   "xyz": [float(x) * BOHR_A for x in _xyz]})
    data = []
    for ln in L[6 + nat:]:
        data += [float(x) for x in ln.split()]
    want = n[0] * n[1] * n[2]
    if len(data) != want:
        raise SystemExit("⛔ cube 값 개수가 격자와 다르다: %d ≠ %d (%s)"
                         % (len(data), want, path))
    if any(x != x for x in data):                       # NaN
        raise SystemExit("⛔ cube 에 NaN 이 있다 — 계산이 깨진 출력이다: %s" % path)
    # dV = |v1 · (v2 × v3)| (bohr³ → Å³)
    a, b, c = vec
    det = (a[0] * (b[1] * c[2] - b[2] * c[1])
           - a[1] * (b[0] * c[2] - b[2] * c[0])
           + a[2] * (b[0] * c[1] - b[1] * c[0]))
    dv = abs(det) * BOHR_A ** 3
    return {"n": n, "origin": [x * BOHR_A for x in org],
            "vec": [[y * BOHR_A for y in v] for v in vec],
            "atoms": at, "data": data, "dV_A3": dv}


def _becke_s(mu, k=3):
    """Becke 의 매끄러운 자름 함수 s(μ) = ½(1 − f_k(μ)) — f 를 k 번 반복한다."""
    f = mu
    for _ in range(k):
        f = 1.5 * f - 0.5 * f * f * f
    return 0.5 * (1.0 - f)


def _becke_aij(rad):
    """원자 쌍 크기 조정 상수 a_ij (Becke 1988 appendix). → nat×nat 리스트."""
    nat = len(rad)
    A = [[0.0] * nat for _ in range(nat)]
    for i in range(nat):
        for j in range(nat):
            if i == j:
                continue
            chi = rad[i] / rad[j]
            u = (chi - 1.0) / (chi + 1.0)
            A[i][j] = max(-0.5, min(0.5, u / (u * u - 1.0))) if abs(u) > 0 else 0.0
    return A


def becke_weights(pt, atoms, rad, aij=None):
    """격자점 하나에서의 Becke 원자 가중치 목록 (합 = 1). **순수 파이썬 참조 구현.**

    → (가중치 목록, 죽은 점 여부). 죽은 점 = 모든 P_i 가 0 으로 내려가 정의가 안 되는
    점. 종전엔 조용히 균등 가중치를 돌려줬다 — 회신 Y P1: 그 질량을 **기록·차단**해야
    한다. 호출부가 두 번째 값을 세어 QC 에 올린다.

    ⛔ 못 하는 것: 원자가 겹쳐 있으면(R_AB → 0) 의미가 없다 — 호출부가 막는다.
    """
    nat = len(atoms)
    if aij is None:
        aij = _becke_aij(rad)
    d = [math.dist(pt, a["xyz"]) for a in atoms]
    P = [1.0] * nat
    for i in range(nat):
        for j in range(nat):
            if i == j:
                continue
            rij = math.dist(atoms[i]["xyz"], atoms[j]["xyz"])
            mu = (d[i] - d[j]) / rij
            nu = mu + aij[i][j] * (1.0 - mu * mu)
            P[i] *= _becke_s(nu)
    tot = sum(P)
    if tot <= 0:
        return [1.0 / nat] * nat, True     # 죽은 점 — 균등. 호출부가 질량을 센다
    return [p / tot for p in P], False


def _becke_weights_np(pts, axyz, rij, aij, k=3):
    """numpy 벡터화 — 여러 격자점을 한 번에. → (w [npts×nat], dead [npts] bool).

    순수 파이썬 구현과 **같은 식**이다 (selftest 가 두 경로를 1e-10 으로 대조한다).
    ⚠ 왜 있나: production cube(199원자 · 10⁶점)는 순수 파이썬으로 며칠이 걸린다.
      계산이 안 끝나는 대조는 "생성되지만 아무도 읽지 않는 필드" 와 같다 (회신 Y P0-2).
    """
    import numpy as np
    d = np.sqrt(((pts[:, None, :] - axyz[None, :, :]) ** 2).sum(-1))      # npts×nat
    nat = axyz.shape[0]
    mu = (d[:, :, None] - d[:, None, :]) / rij[None, :, :]                 # npts×nat×nat
    nu = mu + aij[None, :, :] * (1.0 - mu * mu)
    f = nu
    for _ in range(k):
        f = 1.5 * f - 0.5 * f * f * f
    s = 0.5 * (1.0 - f)
    idx = np.arange(nat)
    s[:, idx, idx] = 1.0                                                   # i==j 항 제외
    P = s.prod(axis=2)                                                     # npts×nat
    tot = P.sum(axis=1)
    dead = tot <= 0
    w = np.where(dead[:, None], 1.0 / nat, P / np.where(dead, 1.0, tot)[:, None])
    return w, dead


def partition_forms(cube, groups, min_points=8000, progress=False, use_numpy=True,
                    max_spacing_A=None, n_unpaired=None, chunk=96):
    """두 형태를 **같은 격자·같은 가중치**로 계산한다 → dict.

    F_G^out = Σ_{A∈G}|s_A| / Σ_A|s_A|      (절댓값이 원자 **밖** — production 형)
    F_G^in  = ∫W_G|Δρ| / ∫|Δρ|             (절댓값이 적분 **안** — 결정문 형)

    ⛔ 회신 Y P1 — 격자 QC 를 같이 낸다 (`qc`). 종전엔 점 개수(`min_points`)만 봤다.
      · `SPACING_TOO_COARSE`   가장 큰 축 간격 > max_spacing_A
      · `BOUNDARY_TRUNCATED`   상자 여섯 면의 max|Δρ| 가 전체 max 의 1e-3 을 넘는다
      · `NORM_OFF`             ∫Δρ (부호 있음) 가 n_unpaired 와 0.05 넘게 다르다
      · `UNIFORM_FALLBACK_MASS` Becke 가 죽은 점(균등 대체)에 실린 |Δρ| 질량 > 1e-3
      · `SKIPPED_MASS`         0 으로 건너뛴 점의 질량 (항상 0 — 건너뛰는 것은 정확히 0 만)
      qc.ok 가 False 면 소비자(build_v7c_trimer)가 그 잡의 class 를 열지 않는다.
    """
    n = cube["n"]
    npts = n[0] * n[1] * n[2]
    if npts < min_points:
        raise SystemExit("⛔ 격자가 너무 성기다 (%d점 < %d) — 두 형태 모두 격자 오차에 "
                         "묻힌다. orca_plot 에서 격자를 키우십시오." % (npts, min_points))
    at = cube["atoms"]
    nat = len(at)
    idx_all = sorted({i for v in groups.values() for i in v})
    if idx_all and (idx_all[0] < 0 or idx_all[-1] >= nat):
        raise SystemExit("⛔ 그룹의 원자 index 가 cube 원자수(%d) 밖이다: %s"
                         % (nat, [i for i in idx_all if i < 0 or i >= nat][:5]))
    _seen = {}
    for g, v in groups.items():
        for i in v:
            if i in _seen:
                raise SystemExit("⛔ 원자 %d 가 두 그룹에 있다 (%s · %s) — 분할은 "
                                 "상호배타여야 한다" % (i, _seen[i], g))
            _seen[i] = g
    if len(_seen) != nat:
        raise SystemExit("⛔ 분할이 완전하지 않다: 그룹에 든 원자 %d ≠ cube 원자 %d "
                         "(빠진 것을 'other' 로 넣으십시오)" % (len(_seen), nat))
    rad = [BRAGG.get(a["sym"], 1.0) for a in at]
    for i in range(nat):
        for j in range(i + 1, nat):
            if math.dist(at[i]["xyz"], at[j]["xyz"]) < 0.3:
                raise SystemExit("⛔ 원자 %d·%d 가 0.3 Å 안에 겹쳐 있다 — Becke 분할이 "
                                 "정의되지 않는다" % (i, j))
    org, vec, dat = cube["origin"], cube["vec"], cube["data"]
    dv = cube["dV_A3"]
    spacing = [math.sqrt(sum(c * c for c in v)) for v in vec]
    aij = _becke_aij(rad)

    s_signed = [0.0] * nat                 # ∫ w_A Δρ        (부호 있음)
    w_abs = [0.0] * nat                    # ∫ w_A |Δρ|      (적분 안)
    tot_abs = 0.0                          # ∫ |Δρ|
    tot_signed = 0.0                       # ∫ Δρ  (부호 있음 — n_unpaired 여야 한다)
    dead_mass = 0.0                        # 죽은 점(균등 대체)에 실린 |Δρ|
    vmax = max((abs(x) for x in dat), default=0.0)
    # 경계 절단 — 여섯 면의 최대 |Δρ|
    bmax = 0.0
    k = 0
    for i0 in range(n[0]):
        for i1 in range(n[1]):
            for i2 in range(n[2]):
                if (i0 in (0, n[0] - 1)) or (i1 in (0, n[1] - 1)) or (i2 in (0, n[2] - 1)):
                    if abs(dat[k]) > bmax:
                        bmax = abs(dat[k])
                k += 1

    _np = None
    if use_numpy:
        try:
            import numpy as _np           # noqa: N816
        except Exception:                 # noqa: BLE001
            _np = None
    if _np is not None:
        arr = _np.asarray(dat, dtype=float).reshape(n[0], n[1], n[2])
        I0, I1, I2 = _np.indices((n[0], n[1], n[2]))
        pts_all = (_np.asarray(org)[None, :]
                   + I0.reshape(-1, 1) * _np.asarray(vec[0])[None, :]
                   + I1.reshape(-1, 1) * _np.asarray(vec[1])[None, :]
                   + I2.reshape(-1, 1) * _np.asarray(vec[2])[None, :])
        vals = arr.reshape(-1)
        nz = vals != 0.0                  # 건너뛰는 것은 **정확히 0** 만 (질량 손실 0)
        pts_all, vals = pts_all[nz], vals[nz]
        axyz = _np.asarray([a["xyz"] for a in at], dtype=float)
        rij = _np.sqrt(((axyz[:, None, :] - axyz[None, :, :]) ** 2).sum(-1))
        _np.fill_diagonal(rij, 1.0)
        aij_np = _np.asarray(aij, dtype=float)
        ss = _np.zeros(nat); wa = _np.zeros(nat)
        tot_abs = float(_np.abs(vals).sum()); tot_signed = float(vals.sum())
        for c0 in range(0, len(vals), chunk):
            w, dead = _becke_weights_np(pts_all[c0:c0 + chunk], axyz, rij, aij_np)
            v = vals[c0:c0 + chunk]
            ss += (w * v[:, None]).sum(axis=0)
            wa += (w * _np.abs(v)[:, None]).sum(axis=0)
            if dead.any():
                dead_mass += float(_np.abs(v[dead]).sum())
            if progress and (c0 // chunk) % 200 == 0:
                print("  … %d/%d 점" % (c0, len(vals)), file=sys.stderr)
        s_signed = [float(x) for x in ss]; w_abs = [float(x) for x in wa]
        backend = "numpy"
    else:
        k = 0
        for i0 in range(n[0]):
            for i1 in range(n[1]):
                for i2 in range(n[2]):
                    v = dat[k]; k += 1
                    if v == 0.0:
                        continue
                    av = abs(v)
                    tot_abs += av; tot_signed += v
                    pt = [org[t] + i0 * vec[0][t] + i1 * vec[1][t] + i2 * vec[2][t]
                          for t in range(3)]
                    w, dead = becke_weights(pt, at, rad, aij)
                    if dead:
                        dead_mass += av
                    for A in range(nat):
                        if w[A] > 1e-12:
                            s_signed[A] += w[A] * v
                            w_abs[A] += w[A] * av
            if progress:
                print("  … %d/%d 평면" % (i0 + 1, n[0]), file=sys.stderr)
        backend = "python"
    s_signed = [x * dv for x in s_signed]
    w_abs = [x * dv for x in w_abs]
    tot_abs *= dv; tot_signed *= dv; dead_mass *= dv
    out_den = sum(abs(x) for x in s_signed)
    if out_den <= 0 or tot_abs <= 0:
        raise SystemExit("⛔ |Δρ| 적분이 0 이다 — 닫힌 껍질이거나 빈 cube 다")
    F_out = {g: sum(abs(s_signed[i]) for i in v) / out_den for g, v in groups.items()}
    F_in = {g: sum(w_abs[i] for i in v) / tot_abs for g, v in groups.items()}
    # ── 격자 QC (회신 Y P1) ──────────────────────────────────────────────
    flags = []
    if max_spacing_A is not None and max(spacing) > max_spacing_A:
        flags.append("SPACING_TOO_COARSE(%.3f Å > %.3f)" % (max(spacing), max_spacing_A))
    b_rel = (bmax / vmax) if vmax > 0 else 0.0
    if b_rel > 1e-3:
        flags.append("BOUNDARY_TRUNCATED(면 max|Δρ|/전체 max = %.2e > 1e-3 — 상자가 "
                     "밀도를 자른다)" % b_rel)
    if n_unpaired is not None and abs(tot_signed - n_unpaired) > 0.05:
        flags.append("NORM_OFF(∫Δρ = %.4f ≠ %s — 격자·상자·cube 종류를 의심)"
                     % (tot_signed, n_unpaired))
    if tot_abs > 0 and dead_mass / tot_abs > 1e-3:
        flags.append("UNIFORM_FALLBACK_MASS(균등 대체 점의 질량 %.2e > 1e-3)"
                     % (dead_mass / tot_abs))
    return {
        "schema": "spin_partition_calib/v2",
        "weight_family": "becke_1988_size_adjusted_k3",
        "backend": backend,
        "n_grid_points": npts, "dV_A3": dv, "n_atoms": nat,
        "grid_spacing_A": spacing, "grid_spacing_max_A": max(spacing),
        "F_out": F_out, "F_in": F_in,
        "delta_F": {g: F_in[g] - F_out[g] for g in groups},
        "max_abs_delta_F": max(abs(F_in[g] - F_out[g]) for g in groups),
        "abs_total_out_eA3": out_den,       # Σ_A |∫ w_A Δρ|
        "abs_total_in_eA3": tot_abs,        # ∫ |Δρ|
        "int_signed_e": tot_signed,         # ∫ Δρ  (= n_unpaired 여야 한다)
        "cancellation_ratio": out_den / tot_abs,
        "qc": {"ok": not flags, "flags": flags,
               "boundary_max_rel": b_rel,
               "uniform_fallback_mass_frac": (dead_mass / tot_abs) if tot_abs > 0 else 0.0,
               "n_unpaired_expected": n_unpaired},
        "⛔_이_수의_뜻": (
            "`cancellation_ratio` = Σ_A|∫w_AΔρ| / ∫|Δρ| ≤ 1 — **설명용 QC 다.** class 판정에 "
            "쓰지 않는다 (회신 Y P0-1: 분자·분모가 같이 줄어 비의 대소가 보장되지 않는다. "
            "0.90 이어도 target 밖 상쇄만 있으면 population 형이 0.5 경계를 거짓으로 넘는다). "
            "판정은 `direct_comparison_gate` — 두 형태의 winner·경계·margin·|ΔF| 를 직접 비교한다."),
        "⛔_이_값을_F_로_인용하지_않는다": (
            "가중치 계열이 production(Hirshfeld)과 다르다. 재는 것은 **같은 계열 안에서 "
            "절댓값 위치가 만드는 차이**이지 production F 의 재현이 아니다."),
    }


def direct_comparison_gate(F_in, F_out, class_min, margin, max_df):
    """두 형태가 **같은 class 판정**을 주는가 — 회신 Y Q3 의 네 조건. → (ok, code, why).

    ⓐ winning group 같음                     → 아니면 CALIB_WINNER_DIFFERS
    ⓑ 모든 집합의 F ≥ class_min 여부 같음     → 아니면 CALIB_CLASS_BOUNDARY_DIFFERS
    ⓒ winner − runner-up ≥ margin 판정 같음  → 아니면 CALIB_MARGIN_DIFFERS
    ⓓ max_G |F_in − F_out| ≤ max_df           → 아니면 CALIB_DF_EXCEEDS
    비(cancellation_ratio)는 여기 들어오지 않는다 — 리뷰어 반례(0.49/0.31/0.20, target 밖
    0.10 상쇄)에서 비는 0.90 인데 ⓑ 가 갈린다. 그 반례가 selftest 에 있다.

    ⛔ 못 하는 것: 두 형태가 **둘 다 틀린** 경우(격자 오차·Becke≠Hirshfeld)는 못 본다.
      같은 격자·같은 가중치에서 절댓값 위치만 다른 두 수의 일치를 볼 뿐이다.
    """
    gs = sorted(F_in)
    if sorted(F_out) != gs or not gs:
        return False, "CALIB_GROUPS_MISMATCH", "두 형태의 집합 이름이 다르다 (%s ≠ %s)" % (
            gs, sorted(F_out))
    def _win(F):
        o = sorted(gs, key=lambda g: -F[g])
        return o[0], (F[o[0]] - (F[o[1]] if len(o) > 1 else 0.0))
    wi, mi = _win(F_in); wo, mo = _win(F_out)
    if wi != wo:
        return False, "CALIB_WINNER_DIFFERS", "적분형 winner %s ≠ population 형 winner %s" % (wi, wo)
    for g in gs:
        if (F_in[g] >= class_min) != (F_out[g] >= class_min):
            return False, "CALIB_CLASS_BOUNDARY_DIFFERS", (
                "집합 %s: 적분형 %.3f / population 형 %.3f 가 class 경계 %.2f 를 다르게 "
                "넘는다" % (g, F_in[g], F_out[g], class_min))
    if (mi >= margin) != (mo >= margin):
        return False, "CALIB_MARGIN_DIFFERS", (
            "winner−runner-up: 적분형 %.3f / population 형 %.3f 가 margin %.2f 판정에서 "
            "갈린다" % (mi, mo, margin))
    dfmax = max(abs(F_in[g] - F_out[g]) for g in gs)
    if dfmax > max_df:
        return False, "CALIB_DF_EXCEEDS", "max_G|F_in−F_out| = %.3f > %.3f" % (dfmax, max_df)
    return True, "CALIB_AGREES", ("winner %s · 경계·margin 판정 일치 · max|ΔF| %.3f ≤ %.3f"
                                   % (wi, dfmax, max_df))


def selftest():
    n_ok, n_bad = [0], [0]

    def chk(c, m):
        print(("  ⭕ " if c else "  ⛔ ") + m)
        (n_ok if c else n_bad)[0] += 1

    import os
    import tempfile
    td = tempfile.mkdtemp()

    def mkcube(path, atoms, n, dx, fn):
        """atoms=[(Z,x,y,z) Å], 격자 n³ · 간격 dx Å, fn(x,y,z)->값."""
        L = ["cube", "selftest",
             "%5d %11.6f %11.6f %11.6f" % (len(atoms), 0.0, 0.0, 0.0)]
        b = dx / BOHR_A
        for i in range(3):
            v = [0.0, 0.0, 0.0]; v[i] = b
            L.append("%5d %11.6f %11.6f %11.6f" % (n, v[0], v[1], v[2]))
        for (z, x, y, zz) in atoms:
            L.append("%5d %11.6f %11.6f %11.6f %11.6f"
                     % (z, float(z), x / BOHR_A, y / BOHR_A, zz / BOHR_A))
        vals = []
        for i0 in range(n):
            for i1 in range(n):
                for i2 in range(n):
                    vals.append(fn(i0 * dx, i1 * dx, i2 * dx))
        for i in range(0, len(vals), 6):
            L.append(" ".join("%13.5e" % v for v in vals[i:i + 6]))
        open(path, "w").write("\n".join(L) + "\n")

    # ── 양성 ① 한 원자에 **한 부호**만 → 두 형태가 같아야 한다 ──────────────
    N, DX = 24, 0.25
    A1, A2 = (1.5, 1.5, 1.5), (4.2, 1.5, 1.5)

    def blob(c, sign, w=0.45):
        return lambda x, y, z: sign * math.exp(
            -((x - c[0]) ** 2 + (y - c[1]) ** 2 + (z - c[2]) ** 2) / (2 * w * w))
    p1 = os.path.join(td, "one_sign.cube")
    mkcube(p1, [(6, *A1), (6, *A2)], N, DX, blob(A1, +1.0))
    g = {"g1": [0], "g2": [1]}
    r1 = partition_forms(read_cube(p1), g, min_points=1000)
    chk(abs(r1["cancellation_ratio"] - 1.0) < 0.02,
        "양성: 부호가 하나면 상쇄가 없다 — cancellation_ratio %.4f ≈ 1"
        % r1["cancellation_ratio"])
    chk(abs(r1["F_out"]["g1"] - r1["F_in"]["g1"]) < 0.02,
        "양성: 그때는 두 형태가 같은 값을 준다 (out %.3f · in %.3f)"
        % (r1["F_out"]["g1"], r1["F_in"]["g1"]))

    # ── ⛔음성 ② **같은 원자 안에서** α·β 가 상쇄 → out 형이 무너져야 한다 ──
    #   이것이 회신 X P0-1 이 말한 바로 그 상황이다. 시험이 이걸 못 잡으면
    #   이 도구는 아무것도 재지 못한다.
    p2 = os.path.join(td, "cancel.cube")
    lo = blob((A1[0] - 0.5, A1[1], A1[2]), +1.0, 0.30)
    hi = blob((A1[0] + 0.5, A1[1], A1[2]), -1.0, 0.30)
    mkcube(p2, [(6, *A1), (6, *A2)], N, DX,
           lambda x, y, z: lo(x, y, z) + hi(x, y, z))
    r2 = partition_forms(read_cube(p2), g, min_points=1000)
    chk(r2["cancellation_ratio"] < 0.25,
        "⛔음성 (회신 X P0-1 그 상황): 한 원자 안에서 α·β 가 상쇄되면 "
        "population 형의 분모가 **무너진다** — ratio %.4f ≪ 1"
        % r2["cancellation_ratio"])
    chk(r2["abs_total_in_eA3"] > r2["abs_total_out_eA3"],
        "⛔음성: ∫|Δρ| > Σ|∫wΔρ| 가 실제로 성립한다 (삼각부등식 · %.4f > %.4f)"
        % (r2["abs_total_in_eA3"], r2["abs_total_out_eA3"]))
    chk(r1["cancellation_ratio"] - r2["cancellation_ratio"] > 0.5,
        "⛔음성: 같은 격자·같은 가중치인데 **부호 배치만** 바꿔 비가 크게 갈린다 "
        "— 차이의 원인이 절댓값 위치임이 분리된다 (%.3f → %.3f)"
        % (r1["cancellation_ratio"], r2["cancellation_ratio"]))

    # ── ⛔음성 ③ 분할이 불완전/중복/범위밖 ────────────────────────────────
    for bad, why in ((({"g1": [0]}), "완전하지 않다"),
                     (({"g1": [0, 1], "g2": [1]}), "두 그룹에 있다"),
                     (({"g1": [0], "g2": [1], "g3": [9]}), "index 가 cube 원자수")):
        try:
            partition_forms(read_cube(p1), bad, min_points=1000)
            chk(False, "⛔음성: 잘못된 분할(%s)을 거부해야 한다" % why)
        except SystemExit as e:
            chk(why in str(e), "⛔음성: 분할이 %s → 거부한다" % why)

    # ── ⛔음성 ④ 성긴 격자 · NaN · 궤도 cube ──────────────────────────────
    try:
        partition_forms(read_cube(p1), g, min_points=10 ** 9)
        chk(False, "⛔음성: 성긴 격자를 거부해야 한다")
    except SystemExit as e:
        chk("너무 성기다" in str(e),
            "⛔음성: 격자가 성기면 **거부한다** — 두 형태 모두 격자 오차에 묻힌다")
    p3 = os.path.join(td, "nan.cube")
    open(p3, "w").write(open(p1).read().replace("1.00000e+00", "        nan", 1))
    try:
        read_cube(p3); chk(False, "⛔음성: NaN cube 를 거부해야 한다")
    except SystemExit as e:
        chk("NaN" in str(e) or "개수가" in str(e),
            "⛔음성: NaN 이 있는 cube 는 거부한다 (계산이 깨진 출력이다)")
    p4 = os.path.join(td, "orb.cube")
    _l = open(p1).read().splitlines()
    _l[2] = "   -2 " + " ".join(_l[2].split()[1:])
    open(p4, "w").write("\n".join(_l) + "\n")
    try:
        read_cube(p4); chk(False, "⛔음성: 궤도 cube 를 거부해야 한다")
    except SystemExit as e:
        chk("궤도 cube" in str(e),
            "⛔음성: 원자 수가 음수인 **궤도 cube** 는 거부한다 (데이터 앞에 줄이 "
            "하나 더 있어 모르고 읽으면 격자가 밀린다)")

    # ── 가중치 합 = 1 ─────────────────────────────────────────────────────
    cb = read_cube(p1)
    _r = [BRAGG.get(a["sym"], 1.0) for a in cb["atoms"]]
    _w, _dead = becke_weights([2.0, 1.5, 1.5], cb["atoms"], _r)
    chk(abs(sum(_w) - 1.0) < 1e-12 and _dead is False,
        "Becke 가중치 합 = 1 (%.15f) · 죽은 점 아님" % sum(_w))
    chk(0.0 <= min(_w) and max(_w) <= 1.0, "가중치가 [0,1] 안이다")
    # ⚠ 종전엔 **키 이름**에 있는 문구를 값에서 찾았다 (2026-09-02 실측).
    chk("production F 의 재현이 아니다" in r1["⛔_이_값을_F_로_인용하지_않는다"]
        and "cancellation_ratio" in r1["⛔_이_수의_뜻"],
        "산출물이 **한계를 스스로 말한다** (production F 의 재현이 아니다 · 비의 뜻)")

    # ══ 회신 Y P0-1 · Q3 (2026-09-03) — **비 문턱은 class gate 가 아니다** ═══════
    # 리뷰어 반례: 실공간 0.49/0.31/0.20, target 밖에서만 0.10 상쇄 → 비 0.90 인데
    # population target = 0.49/0.90 = 0.544 가 0.5 경계를 거짓으로 넘는다.
    _Fin = {"target": 0.49, "b": 0.31, "c": 0.20}
    _Fout = {"target": 0.49 / 0.90, "b": 0.26 / 0.90, "c": 0.15 / 0.90}   # 합 1.0
    _ok, _code, _why = direct_comparison_gate(_Fin, _Fout, 0.50, 0.10, 0.05)
    chk(not _ok and _code == "CALIB_CLASS_BOUNDARY_DIFFERS",
        "⛔음성 Y P0-1 (리뷰어 반례): 비 0.90 통과인데 population 형이 0.5 경계를 "
        "거짓으로 넘는다 → 직접 대조가 잡는다 (%s)" % _code)
    chk(abs(sum(_Fout.values()) - 1.0) < 1e-9 and abs(0.9 - 0.9) < 1e-12,
        "반례의 산수: population 형 합 = 1, cancellation_ratio = 0.90")
    chk(direct_comparison_gate(_Fin, dict(_Fin), 0.50, 0.10, 0.05)[0],
        "양성: 두 형태가 같으면 통과한다")
    chk(direct_comparison_gate({"a": 0.55, "b": 0.45}, {"a": 0.45, "b": 0.55},
                               0.50, 0.10, 0.20)[1] == "CALIB_WINNER_DIFFERS",
        "⛔음성: winner 가 다르면 막는다")
    chk(direct_comparison_gate({"a": 0.62, "b": 0.38}, {"a": 0.54, "b": 0.46},
                               0.50, 0.10, 0.20)[1] == "CALIB_MARGIN_DIFFERS",
        "⛔음성: winner·경계는 같아도 margin(0.10) 판정이 갈리면 막는다")
    chk(direct_comparison_gate({"a": 0.70, "b": 0.30}, {"a": 0.63, "b": 0.37},
                               0.50, 0.10, 0.05)[1] == "CALIB_DF_EXCEEDS",
        "⛔음성: 판정어는 다 같아도 |ΔF| 가 허용치(0.05)를 넘으면 막는다")
    chk(direct_comparison_gate({"a": 0.7, "b": 0.3}, {"a": 0.7, "x": 0.3},
                               0.50, 0.10, 0.05)[1] == "CALIB_GROUPS_MISMATCH",
        "⛔음성: 집합 이름이 다르면 비교하지 않는다")

    # ══ numpy 경로 = 순수 파이썬 경로 (회신 Y P0-2 — 안 끝나는 대조는 대조가 아니다) ══
    _rp = partition_forms(read_cube(p1), g, min_points=1000, use_numpy=False)
    _rn = partition_forms(read_cube(p1), g, min_points=1000, use_numpy=True)
    _dmax = max(abs(_rp["F_in"][k] - _rn["F_in"][k]) for k in g) + \
        max(abs(_rp["F_out"][k] - _rn["F_out"][k]) for k in g)
    chk(_rn["backend"] == "numpy" and _rp["backend"] == "python" and _dmax < 1e-10,
        "numpy 벡터화 경로가 순수 파이썬 참조와 1e-10 안에서 같다 (Δ=%.1e)" % _dmax)
    chk(abs(_rn["cancellation_ratio"] - _rp["cancellation_ratio"]) < 1e-10,
        "두 경로의 cancellation_ratio 도 같다")

    # ══ 격자 QC (회신 Y P1) ═══════════════════════════════════════════════════
    # ⚠ 기존 픽스처 p1 의 blob 은 상자 면에서 3.9e-3 — QC 가 **옳게** 절단을 잡는다.
    #   양성은 면에서 1e-3 아래로 떨어지는 좁은 가우시안으로 따로 만든다.
    chk(any(f.startswith("BOUNDARY_TRUNCATED") for f in _rn["qc"]["flags"]),
        "QC 가 넓은 blob 픽스처(p1)의 면 절단을 잡는다 (경계 %.1e > 1e-3)"
        % _rn["qc"]["boundary_max_rel"])
    _Lbox = (N - 1) * DX
    _sig = 0.12 * _Lbox
    p6 = os.path.join(td, "tight.cube")
    mkcube(p6, [(6, *A1), (6, *A2)], N, DX,
           lambda x, y, z: math.exp(-((x - _Lbox / 2) ** 2 + (y - _Lbox / 2) ** 2
                                      + (z - _Lbox / 2) ** 2) / (2 * _sig * _sig)))
    _r6 = partition_forms(read_cube(p6), g, min_points=1000, max_spacing_A=1.0)
    chk(_r6["qc"]["ok"] and _r6["grid_spacing_max_A"] > 0,
        "양성: 상자 안에 들어오는 밀도는 QC 통과 (간격 %.3f Å · 경계 %.1e)"
        % (_r6["grid_spacing_max_A"], _r6["qc"]["boundary_max_rel"]))
    _rs = partition_forms(read_cube(p1), g, min_points=1000, max_spacing_A=0.01)
    chk(not _rs["qc"]["ok"] and any(f.startswith("SPACING_TOO_COARSE") for f in _rs["qc"]["flags"]),
        "⛔음성 QC: 간격 상한을 넘으면 SPACING_TOO_COARSE (점 개수만 보던 종전과 다르다)")
    p5 = os.path.join(td, "edge.cube")
    mkcube(p5, [(6, *A1), (6, *A2)], N, DX, lambda x, y, z: 1.0)      # 상자 전체가 균일 밀도
    _re = partition_forms(read_cube(p5), g, min_points=1000)
    chk(any(f.startswith("BOUNDARY_TRUNCATED") for f in _re["qc"]["flags"]),
        "⛔음성 QC: 밀도가 상자 면까지 닿으면 BOUNDARY_TRUNCATED")
    _rnorm = partition_forms(read_cube(p1), g, min_points=1000, n_unpaired=1)
    chk(any(f.startswith("NORM_OFF") for f in _rnorm["qc"]["flags"]),
        "⛔음성 QC: ∫Δρ 가 기대 홀전자수와 다르면 NORM_OFF (%.3f vs 1)"
        % _rnorm["int_signed_e"])
    chk(_rn["qc"]["uniform_fallback_mass_frac"] == 0.0,
        "정상 cube 에서 균등 대체(죽은 점) 질량은 0 이다 — 값이 기록된다")

    print("selftest: %d 통과 / %d 실패" % (n_ok[0], n_bad[0]))
    return 1 if n_bad[0] else 0


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spin_cube", help="스핀밀도 cube (orca_plot 산출)")
    ap.add_argument("--groups", help="{그룹: [원자 index]} JSON")
    ap.add_argument("--min_points", type=int, default=8000)
    ap.add_argument("--max_spacing_A", type=float, default=None,
                    help="격자 간격 상한 [Å] — 넘으면 qc.ok=False (회신 Y P1)")
    ap.add_argument("--n_unpaired", type=int, default=None,
                    help="기대 ∫Δρ (doublet=1). 주면 NORM_OFF 검사를 한다")
    ap.add_argument("--gate", nargs=3, type=float, metavar=("CLASS_MIN", "MARGIN", "MAX_DF"),
                    help="직접 대조 게이트 (회신 Y Q3). production 은 빌더가 자기 상수를 준다")
    ap.add_argument("--no_numpy", action="store_true", help="순수 파이썬 참조 경로 (느리다)")
    ap.add_argument("--json", help="결과를 이 파일에 쓴다")
    ap.add_argument("--progress", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.spin_cube and a.groups):
        ap.error("--spin_cube 와 --groups 를 주십시오")
    import hashlib
    grp = json.loads(open(a.groups, encoding="utf-8").read())
    res = partition_forms(read_cube(a.spin_cube), grp, min_points=a.min_points,
                          progress=a.progress, use_numpy=not a.no_numpy,
                          max_spacing_A=a.max_spacing_A, n_unpaired=a.n_unpaired)
    res["spin_cube"] = a.spin_cube
    res["groups_file"] = a.groups
    # 결박 — 소비자가 "어느 cube · 어느 분할 · 어느 도구" 로 만든 수인지 대조한다 (회신 Y P0-2)
    _h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()   # noqa: E731
    res["spin_cube_sha256"] = _h(a.spin_cube)
    res["groups_sha256"] = hashlib.sha256(
        json.dumps(grp, sort_keys=True).encode("utf-8")).hexdigest()
    res["tool_sha256"] = _h(__file__)
    if a.gate:
        ok, code, why = direct_comparison_gate(res["F_in"], res["F_out"], *a.gate)
        res["gate"] = {"ok": ok, "code": code, "why": why,
                       "class_min": a.gate[0], "margin": a.gate[1], "max_dF": a.gate[2]}
    txt = json.dumps(res, ensure_ascii=False, indent=1)
    if a.json:
        open(a.json, "w", encoding="utf-8").write(txt + "\n")
        print("→ %s" % a.json)
    print("  cancellation_ratio = %.4f   (설명용 QC — class 판정에 쓰지 않는다)"
          % res["cancellation_ratio"])
    for g in sorted(res["F_out"]):
        print("  %-12s F_out %.4f   F_in %.4f   Δ %+.4f"
              % (g, res["F_out"][g], res["F_in"][g], res["delta_F"][g]))
    if not res["qc"]["ok"]:
        print("  ⛔ QC: %s" % res["qc"]["flags"])
    if a.gate:
        print("  gate: %s — %s" % (res["gate"]["code"], res["gate"]["why"]))
        return 0 if res["gate"]["ok"] and res["qc"]["ok"] else 3
    return 0 if res["qc"]["ok"] else 3


if __name__ == "__main__":
    sys.exit(main())
