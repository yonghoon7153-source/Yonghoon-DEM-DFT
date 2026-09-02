#!/usr/bin/env python3
"""spin_partition_calib.py — 스핀 국재화 F 의 **두 형태를 같은 격자에서** 재고 차이를 낸다.

⛔⛔ 왜 만들었나 (2026-09-02 · 회신 X P0-1 · 1저자 선택 ③)

  폴라론 pilot 이 보고하는 F 는 **원자 population 형**이다:

      F_G^out = Σ_{A∈G} |s_A| / Σ_A |s_A| ,   s_A = ∫ w_A(r) Δρ(r) dr   (부호 있음)

  비준 결정문이 정의한 것은 **실공간 적분형**이다:

      F_G^in  = ∫ W_G(r) |Δρ(r)| dr / ∫ |Δρ(r)| dr ,   W_G = Σ_{A∈G} w_A

  절댓값이 원자 **밖**(out)이냐 적분 **안**(in)이냐가 다르고, 삼각부등식으로
  `Σ_A|∫w_AΔρ| ≤ ∫|Δρ|` 이라 out 형은 하한이다. **얼마나 낮은지는 아무도 모른다** —
  "하한이라 안전하다" 는 크기를 모르는 채 하는 말이다. 이 도구가 그 크기를 잰다.

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
  · 격자 오차를 스스로 보정하지 않는다. cube 가 성기면 두 형태 모두 틀린다
    (`--min_points` 로 최소 격자를 요구하고, 미달이면 거부한다).
  · 스핀밀도 cube 를 만들지 않는다 — ORCA `orca_plot` 의 몫이다.
  · 원자 분할의 **물리적 타당성**을 판정하지 않는다. Becke 는 기하 분할이다.
"""
from __future__ import annotations

import argparse
import json
import math
import sys

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


def becke_weights(pt, atoms, rad):
    """격자점 하나에서의 Becke 원자 가중치 목록 (합 = 1).

    ⛔ 못 하는 것: 원자가 겹쳐 있으면(R_AB → 0) 의미가 없다 — 호출부가 막는다.
    """
    nat = len(atoms)
    d = [math.dist(pt, a["xyz"]) for a in atoms]
    P = [1.0] * nat
    for i in range(nat):
        for j in range(nat):
            if i == j:
                continue
            rij = math.dist(atoms[i]["xyz"], atoms[j]["xyz"])
            mu = (d[i] - d[j]) / rij
            # Becke 1988 §appendix — 원자 크기 조정
            chi = rad[i] / rad[j]
            u = (chi - 1.0) / (chi + 1.0)
            aij = max(-0.5, min(0.5, u / (u * u - 1.0)))
            nu = mu + aij * (1.0 - mu * mu)
            P[i] *= _becke_s(nu)
    tot = sum(P)
    if tot <= 0:
        return [1.0 / nat] * nat        # 수치적으로 죽은 점 — 균등 (기여 0에 가깝다)
    return [p / tot for p in P]


def partition_forms(cube, groups, min_points=8000, progress=False):
    """두 형태를 **같은 격자·같은 가중치**로 계산한다 → dict.

    F_G^out = Σ_{A∈G}|s_A| / Σ_A|s_A|      (절댓값이 원자 **밖** — production 형)
    F_G^in  = ∫W_G|Δρ| / ∫|Δρ|             (절댓값이 적분 **안** — 결정문 형)
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
    s_signed = [0.0] * nat                 # ∫ w_A Δρ        (부호 있음)
    w_abs = [0.0] * nat                    # ∫ w_A |Δρ|      (적분 안)
    tot_abs = 0.0                          # ∫ |Δρ|
    k = 0
    for i0 in range(n[0]):
        for i1 in range(n[1]):
            for i2 in range(n[2]):
                v = dat[k]; k += 1
                if v == 0.0:
                    continue
                av = abs(v)
                tot_abs += av
                pt = [org[t] + i0 * vec[0][t] + i1 * vec[1][t] + i2 * vec[2][t]
                      for t in range(3)]
                w = becke_weights(pt, at, rad)
                for A in range(nat):
                    if w[A] > 1e-12:
                        s_signed[A] += w[A] * v
                        w_abs[A] += w[A] * av
        if progress:
            print("  … %d/%d 평면" % (i0 + 1, n[0]), file=sys.stderr)
    s_signed = [x * dv for x in s_signed]
    w_abs = [x * dv for x in w_abs]
    tot_abs *= dv
    out_den = sum(abs(x) for x in s_signed)
    if out_den <= 0 or tot_abs <= 0:
        raise SystemExit("⛔ |Δρ| 적분이 0 이다 — 닫힌 껍질이거나 빈 cube 다")
    F_out = {g: sum(abs(s_signed[i]) for i in v) / out_den for g, v in groups.items()}
    F_in = {g: sum(w_abs[i] for i in v) / tot_abs for g, v in groups.items()}
    return {
        "schema": "spin_partition_calib/v1",
        "weight_family": "becke_1988_size_adjusted_k3",
        "n_grid_points": npts, "dV_A3": dv, "n_atoms": nat,
        "F_out": F_out, "F_in": F_in,
        "delta_F": {g: F_in[g] - F_out[g] for g in groups},
        "abs_total_out_eA3": out_den,       # Σ_A |∫ w_A Δρ|
        "abs_total_in_eA3": tot_abs,        # ∫ |Δρ|
        "cancellation_ratio": out_den / tot_abs,
        "⛔_이_수의_뜻": (
            "`cancellation_ratio` = Σ_A|∫w_AΔρ| / ∫|Δρ| ≤ 1. 1 에 가까우면 원자 내부 "
            "α·β 상쇄가 작아 population 형이 적분형의 좋은 근사다. 작으면 production 이 "
            "보고하는 F 의 **분모가 크게 깎여 있다**는 뜻이고, 그때는 F 자체보다 "
            "이 비를 같이 인용해야 한다."),
        "⛔_이_값을_F_로_인용하지_않는다": (
            "가중치 계열이 production(Hirshfeld)과 다르다. 재는 것은 **같은 계열 안에서 "
            "절댓값 위치가 만드는 차이**이지 production F 의 재현이 아니다."),
    }


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
    _w = becke_weights([2.0, 1.5, 1.5], cb["atoms"], _r)
    chk(abs(sum(_w) - 1.0) < 1e-12, "Becke 가중치 합 = 1 (%.15f)" % sum(_w))
    chk(0.0 <= min(_w) and max(_w) <= 1.0, "가중치가 [0,1] 안이다")
    # ⚠ 종전엔 **키 이름**에 있는 문구를 값에서 찾았다 (2026-09-02 실측).
    chk("production F 의 재현이 아니다" in r1["⛔_이_값을_F_로_인용하지_않는다"]
        and "cancellation_ratio" in r1["⛔_이_수의_뜻"],
        "산출물이 **한계를 스스로 말한다** (production F 의 재현이 아니다 · 비의 뜻)")

    print("selftest: %d 통과 / %d 실패" % (n_ok[0], n_bad[0]))
    return 1 if n_bad[0] else 0


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spin_cube", help="스핀밀도 cube (orca_plot 산출)")
    ap.add_argument("--groups", help="{그룹: [원자 index]} JSON")
    ap.add_argument("--min_points", type=int, default=8000)
    ap.add_argument("--json", help="결과를 이 파일에 쓴다")
    ap.add_argument("--progress", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.spin_cube and a.groups):
        ap.error("--spin_cube 와 --groups 를 주십시오")
    grp = json.loads(open(a.groups, encoding="utf-8").read())
    res = partition_forms(read_cube(a.spin_cube), grp,
                          min_points=a.min_points, progress=a.progress)
    res["spin_cube"] = a.spin_cube
    res["groups_file"] = a.groups
    txt = json.dumps(res, ensure_ascii=False, indent=1)
    if a.json:
        open(a.json, "w", encoding="utf-8").write(txt + "\n")
        print("→ %s" % a.json)
    print("  cancellation_ratio = %.4f   (1 이면 상쇄 없음)"
          % res["cancellation_ratio"])
    for g in sorted(res["F_out"]):
        print("  %-12s F_out %.4f   F_in %.4f   Δ %+.4f"
              % (g, res["F_out"][g], res["F_in"][g], res["delta_F"][g]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
