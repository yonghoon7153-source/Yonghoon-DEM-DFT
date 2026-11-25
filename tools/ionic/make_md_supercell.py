#!/usr/bin/env python3
"""make_md_supercell.py — MD 셀을 키우고 **유한크기 여유를 감사**한다.

왜 (2026-08-16)
  lpsocl 600 K 가 β̄ 0.77 로 확산영역을 못 넘었다. 시드 3개·800 ps 로도 안 됐다.
  원인은 시간도 시드도 아니고 **상자**였다:

    · 실측 MSD(창끝) 25.8 Å² → RMS 변위 5.08 Å
    · 셀의 **최소 수직 폭** 5.67 Å → 무상관 한계 (d/2)² = 8.0 Å²
    · 비율 **3.21×** — 이온이 짧은 방향에서 상자를 이미 세 번 가로질렀다

  그러면 변위가 자기 주기이미지와 상관되어 늦은 시간 MSD 증가가 눌린다. 관측된
  세 증상이 한꺼번에 설명된다: β 가 1 로 안 가고 0.87 에서 포화 · 절편 c 가 창 따라
  10배 증가 · 시드를 늘려도 안 고쳐짐(모든 시드가 같은 상자).
  comp1 이 1600 ps 에서 오히려 나빠진 것(β 0.64 → 0.37)도 같은 원인이다 — 시간을
  늘리면 wrap 이 더 쌓인다.

⚠ 한계는 |a| 가 아니라 **주기면 사이 수직 거리** d = V / |b×c| 다.
  삼방정계 lpsocl 은 |a| = 6.95 Å 인데 d_a = 5.69 Å 다. |a| 로 재면 여유를 과대평가한다.

⛔ 늘려도 최소 폭이 안 늘면 거부한다
  lpsocl 은 c 축이 이미 28.8 Å 이라 2×2×**2** 가 2×2×1 과 최소 폭이 같다(11.34 Å).
  원자만 2배 쓰고 여유는 그대로 — 그런 배수는 막는다.

  python3 tools/ionic/make_md_supercell.py db/structures/lpsocl_relaxV0.xyz --n 3 3 1
  python3 tools/ionic/make_md_supercell.py <xyz> --audit-only --msd 25.8
  python3 tools/ionic/make_md_supercell.py --selftest

이 도구가 못 하는 것
  · 구조를 이완하지 않는다. 원본 좌표를 그대로 타일링할 뿐이다.
  · MSD 를 예측하지 않는다 — `--msd` 로 준 실측값에 대해 여유만 계산한다.
  · 큰 셀에서 β 가 오른다고 **보장**하지 않는다. 상자가 원인인지를 **시험**하는 도구다.
  · 화학을 안 본다 (도펀트 배치·전하 중성 등은 원본 책임).
"""
import argparse
import os
import re
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def read_xyz(path):
    """확장 xyz → (cell 3×3, [(sym, xyz)], 원본 comment)."""
    L = open(path, encoding="utf-8").read().splitlines()
    n = int(L[0].split()[0])
    m = re.search(r'Lattice="([^"]+)"', L[1])
    if not m:
        raise ValueError(f"Lattice= 가 없다 (확장 xyz 가 아니다): {path}")
    cell = np.array([float(x) for x in m.group(1).split()], float).reshape(3, 3)
    at = []
    for l in L[2:2 + n]:
        p = l.split()
        at.append((p[0], np.array([float(p[1]), float(p[2]), float(p[3])], float)))
    if len(at) != n:
        raise ValueError(f"원자 수가 헤더({n})와 다르다: {len(at)}")
    return cell, at, L[1]


def widths(cell):
    """주기면 사이 **수직 거리** [d_a, d_b, d_c]. 이게 유한크기 한계다."""
    V = abs(float(np.linalg.det(cell)))
    return [V / float(np.linalg.norm(np.cross(cell[(i + 1) % 3], cell[(i + 2) % 3])))
            for i in range(3)], V


#: 포텐셜의 **유효 수용영역** [Å] = cutoff × 메시지패싱 층 수.
#:   UMA-s-1p1 실측 2026-08-26: 층 4 (`mlip_committee.py info`) × cutoff 6 Å (uma2026 digest) = 24 Å.
#:   근거: park2024_sevennet §"GNN-IPs require a broader region for communication,
#:   reaching up to r_c multiplied by the number of message-passing steps".
DEFAULT_RECEPTIVE_FIELD_A = 24.0


def audit(cell, nat, msd, rf=DEFAULT_RECEPTIVE_FIELD_A):
    """유한크기 감사 — **서로 다른 두 한계**를 각각 재고 섞지 않는다.

    ① **MSD wrap** (동역학): 이온 변위가 상자를 가로지르면 늦은 시간 MSD 가 눌린다.
       한계는 (d_min/2)².
    ② **수용영역 겹침** (포텐셜, 2026-08-26 신설): 메시지패싱 GNN 은 cutoff 하나가 아니라
       `cutoff × 층 수` 만큼 멀리 본다. d_min 이 그보다 작으면 **원자가 자기 주기이미지를
       이웃으로 삼는다**.

    ⛔ 둘은 다른 것이다. ①을 통과해도 ②는 못 통과할 수 있고 그 반대도 된다.
    ⚠ ②를 **자동으로 '틀렸다' 로 읽지 마라.** 완전 주기결정에서는 이미지를 보는 것이
      물리적으로 옳을 수도 있다. ②가 말하는 것은 *"이 셀에서는 그 가정이 검사되지 않았다"* 까지고,
      실제 영향은 **셀을 키워 힘/에너지가 변하는지** 재야 안다 (--n 으로 만들어 비교).
    """
    d, V = widths(cell)
    dmin = min(d)
    lim = (dmin / 2.0) ** 2
    out = {"widths_A": [round(x, 3) for x in d], "min_width_A": round(dmin, 3),
           "volume_A3": round(V, 1), "n_atoms": nat,
           "uncorrelated_msd_limit_A2": round(lim, 2),
           "msd_over_limit": (round(msd / lim, 2) if msd else None),
           "verdict": (None if not msd else
                       ("⛔ 초과 — 이온이 상자를 가로질렀다" if msd / lim > 1 else
                        "⚠ 경계" if msd / lim > 0.5 else "✅ 여유"))}
    if rf:
        # 자기 이미지를 **안** 보려면 d_min > 2 × rf 여야 한다 (양쪽으로 rf 씩).
        out["receptive_field_A"] = rf
        out["rf_shells"] = round(rf / dmin, 2) if dmin else None
        out["rf_verdict"] = (
            "✅ 여유 (d_min > 2×수용영역)" if dmin > 2 * rf else
            "⚠ 경계 (수용영역 < d_min ≤ 2×수용영역)" if dmin > rf else
            f"🔴 원자가 자기 이미지를 본다 — 수용영역 {rf:g} Å 안에 이미지가 "
            f"약 {out['rf_shells']}겹. **셀을 키워 힘이 변하는지 확인할 것**")
    return out


def min_dist(cell, at, cap=400):
    """최소 원자간 거리 (PBC). run_arrhenius_6pt.sh 가 1.2 Å 미만이면 실행을 거부한다."""
    P = np.array([p for _, p in at])
    if len(P) > cap:                      # 큰 셀은 앞쪽 표본만 (전수는 O(N²))
        P = P[:cap]
    inv = np.linalg.inv(cell)
    best = 1e9
    for i in range(len(P)):
        d = P[i + 1:] - P[i]
        if not len(d):
            break
        f = d @ inv
        f -= np.round(f)
        best = min(best, float(np.linalg.norm(f @ cell, axis=1).min()))
    return best


def build(cell, at, n):
    sup = np.diag(n).astype(float) @ cell
    out = []
    for i in range(n[0]):
        for j in range(n[1]):
            for k in range(n[2]):
                sh = i * cell[0] + j * cell[1] + k * cell[2]
                out += [(s, p + sh) for s, p in at]
    return sup, out


def write_xyz(path, cell, at, prov):
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"{len(at)}\n")
        f.write('Lattice="' + " ".join(f"{x:.6f}" for x in cell.reshape(-1)) + '" '
                'Properties=species:S:1:pos:R:3 pbc="T T T" '
                f'provenance="{prov}"\n')
        for s, p in at:
            f.write(f"{s:3s} {p[0]:16.10f} {p[1]:16.10f} {p[2]:16.10f}\n")


def run(a):
    cell, at, _ = read_xyz(a.xyz)
    base = audit(cell, len(at), a.msd)
    print(f"■ 원본 {os.path.basename(a.xyz)}")
    print(f"   |a|,|b|,|c| = " + " ".join(f"{np.linalg.norm(v):.3f}" for v in cell) + " Å")
    print(f"   **수직 폭**  = " + " ".join(f"{x:.3f}" for x in base['widths_A']) +
          f" Å  (최소 {base['min_width_A']})")
    print(f"   원자 {base['n_atoms']} · V {base['volume_A3']} Å³ · "
          f"무상관 한계 (d/2)² = {base['uncorrelated_msd_limit_A2']} Å²")
    if a.msd:
        print(f"   MSD {a.msd} Å² → **{base['msd_over_limit']}×**  {base['verdict']}")
    if a.audit_only:
        return 0

    n = a.n
    sup, sat = build(cell, at, n)
    new = audit(sup, len(sat), a.msd)
    print(f"\n■ {n[0]}×{n[1]}×{n[2]} 슈퍼셀")
    print(f"   수직 폭 = " + " ".join(f"{x:.3f}" for x in new['widths_A']) +
          f" Å  (최소 {new['min_width_A']})")
    print(f"   원자 {new['n_atoms']} ({new['n_atoms']/base['n_atoms']:.0f}배) · "
          f"한계 (d/2)² = {new['uncorrelated_msd_limit_A2']} Å²")
    if a.msd:
        print(f"   MSD {a.msd} Å² → **{new['msd_over_limit']}×**  {new['verdict']}")

    # ⛔ 최소 폭이 안 늘면 원자만 쓰는 배수다 (lpsocl 의 2×2×2 가 그 경우)
    gain = new["min_width_A"] / base["min_width_A"]
    cost = new["n_atoms"] / base["n_atoms"]
    if gain <= 1.001 and not a.force:
        print(f"\n⛔ 최소 수직 폭이 안 늘었다 ({base['min_width_A']} → {new['min_width_A']} Å) "
              f"— 원자만 {cost:.0f}배 쓰고 여유는 그대로다.")
        print(f"   이미 긴 축을 늘렸을 것이다. 짧은 축의 배수를 올릴 것. (--force 로 강행)")
        return 1
    if a.msd and new["msd_over_limit"] and new["msd_over_limit"] > 0.5 and not a.force:
        print(f"\n⚠ 여유가 아직 경계다 ({new['msd_over_limit']}× > 0.5) — 더 키우는 편이 낫다.")
        print(f"   그래도 진행하려면 --force")
        return 1

    md = min_dist(sup, sat)
    print(f"\n   최소 원자간 거리 {md:.3f} Å " +
          ("✅" if md > 1.2 else "⛔ 1.2 Å 미만 — MD 러너가 거부한다"))
    if md <= 1.2 and not a.force:
        return 1

    out = a.out or os.path.join(
        os.path.dirname(a.xyz),
        os.path.basename(a.xyz).replace(".xyz", f"_{n[0]}x{n[1]}x{n[2]}.xyz"))
    prov = (f"{n[0]}x{n[1]}x{n[2]} supercell of {os.path.basename(a.xyz)} "
            f"via tools/ionic/make_md_supercell.py (2026-08-16). "
            f"min perpendicular width {base['min_width_A']} -> {new['min_width_A']} A; "
            f"uncorrelated MSD limit {base['uncorrelated_msd_limit_A2']} -> "
            f"{new['uncorrelated_msd_limit_A2']} A2. "
            f"REASON: lpsocl 600 K beta-bar 0.77 traced to finite size "
            f"(MSD/limit {base['msd_over_limit']}x). Positions are tiled, NOT re-relaxed.")
    write_xyz(out, sup, sat, prov)
    print(f"\n→ {out}")
    print(f"   ⚠ 이완 안 된 타일링이다. UMA MD 는 자체 평형화(equilib 5 ps)로 흡수하지만,")
    print(f"     DFT 로 쓸 거면 먼저 이완할 것.")
    return 0


def selftest():
    import tempfile
    ok = True

    def chk(c, m):
        nonlocal ok
        ok &= bool(c)
        print(f"  {'✓' if c else '✗'} {m}")

    # 직교 셀: 수직 폭 = 변 길이
    cube = np.diag([10.0, 10.0, 10.0])
    d, V = widths(cube)
    chk(all(abs(x - 10.0) < 1e-9 for x in d) and abs(V - 1000) < 1e-9,
        "직교 셀은 수직 폭 = 변 길이")

    # ★ 기울어진 셀: |a| 로 재면 과대평가된다 (이 도구의 존재 이유)
    tilt = np.array([[10.0, 0, 0], [9.0, 4.0, 0], [0, 0, 10.0]])
    d2, _ = widths(tilt)
    chk(abs(np.linalg.norm(tilt[1]) - 9.849) < 1e-3 and abs(d2[1] - 4.0) < 1e-9,
        f"[핵심] |b|=9.85 Å 인데 수직 폭 d_b=4.00 Å — |a| 로 재면 2.5배 과대평가")

    # 실제 lpsocl 셀
    lp = os.path.join(ROOT, "db", "structures", "lpsocl_relaxV0.xyz")
    if os.path.isfile(lp):
        c, at, _ = read_xyz(lp)
        a0 = audit(c, len(at), 25.8)
        chk(len(at) == 62 and abs(a0["min_width_A"] - 5.672) < 0.01,
            f"lpsocl 62원자 · 최소 수직 폭 {a0['min_width_A']} Å (|a|=6.95 가 아니다)")
        chk(a0["msd_over_limit"] > 3.0, f"MSD 25.8 Å² 가 한계의 {a0['msd_over_limit']}× ⛔")
        s, sat = build(c, at, [3, 3, 1])
        a1 = audit(s, len(sat), 25.8)
        chk(len(sat) == 558 and a1["msd_over_limit"] < 0.5,
            f"3×3×1 → 558원자 · {a1['msd_over_limit']}× ✅")
        # ⛔ 음성: c 축만 늘리면 최소 폭이 안 는다
        s2, sat2 = build(c, at, [1, 1, 2])
        a2 = audit(s2, len(sat2), 25.8)
        chk(abs(a2["min_width_A"] - a0["min_width_A"]) < 1e-6,
            "[음성] 긴 c 축만 2배 → 최소 폭 그대로 (원자만 2배)")
        s3, sat3 = build(c, at, [2, 2, 2])
        a3 = audit(s3, len(sat3), 25.8)
        s4, sat4 = build(c, at, [2, 2, 1])
        a4 = audit(s4, len(sat4), 25.8)
        chk(abs(a3["min_width_A"] - a4["min_width_A"]) < 1e-6 and len(sat3) == 2 * len(sat4),
            "[음성] 2×2×2 는 2×2×1 과 여유가 같은데 원자는 2배 — 낭비")
    else:
        print("  ⚠ lpsocl 구조가 없어 실셀 검사 생략")

    # 타일링 보존
    c = np.diag([5.0, 5.0, 5.0])
    at = [("Li", np.array([0.0, 0.0, 0.0])), ("S", np.array([2.5, 2.5, 2.5]))]
    s, sat = build(c, at, [2, 1, 1])
    chk(len(sat) == 4 and [x[0] for x in sat].count("Li") == 2, "타일링이 종을 보존한다")
    chk(any(abs(p[0] - 5.0) < 1e-9 and x == "Li" for x, p in sat), "복제가 격자벡터만큼 이동한다")

    # 최소거리
    chk(abs(min_dist(c, at) - float(np.linalg.norm([2.5, 2.5, 2.5]))) < 1e-6,
        "최소 원자간 거리 (PBC)")
    bad = [("Li", np.array([0.0, 0.0, 0.0])), ("Li", np.array([0.3, 0.0, 0.0]))]
    chk(min_dist(c, bad) < 1.2, "[음성] 겹친 원자를 1.2 Å 미만으로 잡는다")

    # xyz 왕복
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "t.xyz")
        write_xyz(p, s, sat, "selftest")
        c2, at2, _ = read_xyz(p)
        chk(np.allclose(c2, s) and len(at2) == len(sat), "xyz 쓰기→읽기 왕복")
        open(os.path.join(td, "bad.xyz"), "w").write("2\nno lattice here\nLi 0 0 0\nLi 1 1 1\n")
        try:
            read_xyz(os.path.join(td, "bad.xyz"))
            chk(False, "[음성] Lattice 없는 xyz 를 거부한다")
        except ValueError:
            chk(True, "[음성] Lattice 없는 xyz 를 거부한다")

    print("selftest", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("xyz", nargs="?", help="확장 xyz (Lattice= 포함)")
    ap.add_argument("--n", nargs=3, type=int, default=[3, 3, 1], metavar=("NA", "NB", "NC"))
    ap.add_argument("--receptive_field", type=float, default=DEFAULT_RECEPTIVE_FIELD_A,
                    help=f"포텐셜 유효 수용영역 Å (기본 {DEFAULT_RECEPTIVE_FIELD_A:g} = UMA 6×4). "
                         f"0 이면 이 검사를 끈다")
    ap.add_argument("--msd", type=float, default=None,
                    help="실측 MSD [Å²] — 여유를 이 값에 대해 계산한다")
    ap.add_argument("--out", default=None)
    ap.add_argument("--audit-only", action="store_true", help="감사만, 파일 안 만듦")
    ap.add_argument("--force", action="store_true", help="여유·최소거리 가드를 무시")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.xyz:
        ap.error("xyz 가 필요하다 (또는 --selftest)")
    return run(a)


if __name__ == "__main__":
    sys.exit(main())
