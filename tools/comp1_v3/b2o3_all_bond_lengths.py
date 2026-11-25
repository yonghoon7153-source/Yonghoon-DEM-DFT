#!/usr/bin/env python3
"""b2o3_all_bond_lengths.py — comprehensive bond-length statistics.

Pure-numpy (no pymatgen/ASE needed) nearest-neighbour distance statistics on
the B2O3-doped champion (db/structures/b2o3_relaxV0.cif). Reports EVERY relevant
atom-pair type (cation-anion bonds, anion-anion cage contacts) with
mean/std/min/max/n, plus per-environment breakdowns:
  - P tetrahedra classified by O count (PS4 / PS3O / PS2O2) -> P-S, P-O per type
  - S classified by bonding (free-S / B-S / P-S bridging)
  - Cl classified 4a (octahedral, Z>=5) vs 4d (anti-site, Z<5) -> Li-Cl per site

Exact triclinic minimum image (search lattice translations in -1..1).

    python3 tools/comp1_v3/b2o3_all_bond_lengths.py \
        --cif db/structures/b2o3_relaxV0.cif \
        --json db/properties/b2o3_bond_lengths_full.json
"""
import argparse, json, pathlib, re, itertools
import numpy as np


def parse_cif(path):
    a = b = c = al = be = ga = None
    syms, fr = [], []
    in_loop = False
    cols = []
    for line in open(path):
        s = line.strip()
        if s.startswith("_cell_length_a"): a = float(s.split()[1])
        elif s.startswith("_cell_length_b"): b = float(s.split()[1])
        elif s.startswith("_cell_length_c"): c = float(s.split()[1])
        elif s.startswith("_cell_angle_alpha"): al = float(s.split()[1])
        elif s.startswith("_cell_angle_beta"): be = float(s.split()[1])
        elif s.startswith("_cell_angle_gamma"): ga = float(s.split()[1])
        elif s.startswith("_atom_site_"):
            in_loop = True; cols.append(s)
        elif in_loop and s and not s.startswith("_") and not s.startswith("loop_"):
            t = s.split()
            if len(t) >= 5:
                syms.append(t[1])
                fr.append([float(t[2]), float(t[3]), float(t[4])])
    return (a, b, c, al, be, ga), syms, np.array(fr)


def lattice_matrix(a, b, c, al, be, ga):
    al, be, ga = np.radians([al, be, ga])
    ax, ay, az = a, 0.0, 0.0
    bx, by, bz = b * np.cos(ga), b * np.sin(ga), 0.0
    cx = c * np.cos(be)
    cy = c * (np.cos(al) - np.cos(be) * np.cos(ga)) / np.sin(ga)
    cz = np.sqrt(max(c * c - cx * cx - cy * cy, 0.0))
    return np.array([[ax, ay, az], [bx, by, bz], [cx, cy, cz]])



# ══ 궤적 모드 (2026-08-25) — 분해가 시작됐나 ═══════════════════════════════
#   b2o3 도핑상은 hull 위 37.5 meV/atom 이고 분해산물이
#   Li₃PS₄ + LiCl + Li₂S + **Li₃BS₃** + **Li₄B₇ClO₁₂** 다.
#   출발 구조는 이미 **B = trigonal BS₃**(B–O 0개) · **O = P 위 포스페이트**(P–O 3개).
#   ⇒ 분해 신호는 **P–O 끊김 + B–O 생성**이다. B–S 는 이미 목표 motif 라 변할 필요가 없다.
#
#   ⛔ 이 검사가 못 하는 것
#     · 분해의 **완료**를 보지 않는다. 시작 신호(결합 교환)만 본다.
#     · 열적 신축과 진짜 결합 교환을 창 하나로 완벽히 가르지 못한다 —
#       그래서 창 개수와 **원자별 최근접 양이온 정체**를 **둘 다** 낸다.
#     · 인과를 말하지 않는다. 'UMA 가 그렇게 만들었나' 는 이 검사 밖이다.
DECOMP_WINDOWS = {("B", "O"): (1.10, 1.80), ("B", "S"): (1.60, 2.40),
                  ("P", "O"): (1.30, 1.95), ("P", "S"): (1.85, 2.60),
                  ("Li", "O"): (1.60, 2.60)}


def min_image_D(cart, L):
    """최소이미지 거리행렬 (삼사정계 정확 — 병진 -1..1 전수)."""
    trans = np.array(list(itertools.product([-1, 0, 1], repeat=3))) @ L
    N = len(cart)
    D = np.full((N, N), 1e9)
    for i in range(N):
        dd = (cart - cart[i])[:, None, :] + trans[None, :, :]
        D[i] = np.sqrt((dd ** 2).sum(-1)).min(1)
    np.fill_diagonal(D, 1e9)
    return D


def count_bonds(D, syms, e1, e2, lo, hi):
    i1 = np.where(syms == e1)[0]
    i2 = np.where(syms == e2)[0]
    n = 0
    for i in i1:
        for j in i2:
            if e1 == e2 and j <= i:
                continue
            if lo <= D[i, j] <= hi:
                n += 1
    return n


def nearest_cation(D, syms, el, cations=("B", "P", "Li")):
    """el 원자마다 **가장 가까운 양이온의 원소**와 거리. 창(cutoff)에 안 기댄다."""
    out = []
    cmask = np.isin(syms, list(cations))
    ci = np.where(cmask)[0]
    for i in np.where(syms == el)[0]:
        j = ci[np.argmin(D[i, ci])]
        out.append((int(i), str(syms[j]), round(float(D[i, j]), 3)))
    return out


def read_extxyz_frames(path, which=("first", "last")):
    """확장 xyz 에서 첫/끝 프레임만 뽑는다 (ASE 없이 — 이 도구는 순수 numpy 규약).

    ⚠ Lattice= 가 없으면 None 을 돌려준다 — 셀 없이 최소이미지를 흉내내지 않는다.
    """
    frames, buf, want, lat = [], None, 0, None
    with open(path, errors="ignore") as f:
        while True:
            line = f.readline()
            if not line:
                break
            try:
                nat = int(line.split()[0])
            except (ValueError, IndexError):
                continue
            com = f.readline()
            m = re.search(r'Lattice="([^"]+)"', com)
            cell = (np.array([float(x) for x in m.group(1).split()]).reshape(3, 3)
                    if m else None)
            sy, ps = [], []
            for _ in range(nat):
                v = f.readline().split()
                sy.append(v[0]); ps.append([float(v[1]), float(v[2]), float(v[3])])
            frames.append((np.array(sy), np.array(ps), cell))
    if not frames:
        return []
    sel = []
    if "first" in which:
        sel.append(("first", frames[0]))
    if "last" in which and len(frames) > 1:
        sel.append(("last", frames[-1]))
    return sel


def traj_decomp_report(traj_path):
    """첫 프레임 대비 끝 프레임의 결합 교환 → 분해 시작 여부."""
    sel = read_extxyz_frames(traj_path)
    if len(sel) < 2:
        return None
    out = {"traj": str(traj_path), "frames": {}}
    for tag, (sy, cart, cell) in sel:
        if cell is None:
            return {"error": "Lattice= 없음 — 셀 없이 최소이미지를 못 만든다"}
        D = min_image_D(cart, cell)
        sy = np.array(sy)
        out["frames"][tag] = {
            "bonds": {f"{a}-{b}": count_bonds(D, sy, a, b, lo, hi)
                      for (a, b), (lo, hi) in DECOMP_WINDOWS.items()},
            "O_nearest_cation": nearest_cation(D, sy, "O"),
            "B_nearest_cation": nearest_cation(D, sy, "B", cations=("O", "S", "Cl")),
        }
    f0, f1 = out["frames"]["first"]["bonds"], out["frames"]["last"]["bonds"]
    out["delta"] = {k: f1[k] - f0[k] for k in f0}
    # 사전 등록 판정: P–O 가 줄고 B–O 가 생기면 분해 시작
    po, bo = out["delta"].get("P-O", 0), out["delta"].get("B-O", 0)
    out["verdict"] = ("decomposition_started" if (po < 0 and bo > 0) else
                      "partial_signal" if (po < 0 or bo > 0) else
                      "no_bond_exchange")
    return out



def _selftest():
    """합성 궤적으로 판정 로직 검증 — **음성 경로 포함**.

    양성만 있으면 '전부 decomposition_started 반환' 도 통과한다.
    """
    import tempfile
    ok = [0, 0]

    def chk(c, m):
        ok[0] += 1; ok[1] += bool(c)
        print(("  ✔ " if c else "  ✘ ") + m)

    L = "20.0 0.0 0.0 0.0 20.0 0.0 0.0 0.0 20.0"

    def frame(rows):
        s = f"{len(rows)}\nLattice=\"{L}\" Properties=species:S:1:pos:R:3\n"
        return s + "".join(f"{e} {x:.4f} {y:.4f} {z:.4f}\n" for e, x, y, z in rows)

    # 출발: B–S3 (B–O 없음) + P–O 1개
    start = [("B", 0, 0, 0), ("S", 1.82, 0, 0), ("S", -0.91, 1.58, 0), ("S", -0.91, -1.58, 0),
             ("P", 8, 0, 0), ("O", 9.56, 0, 0), ("S", 8, 2.05, 0)]
    # 끝(분해): P–O 끊기고 O 가 B 쪽으로 → B–O 생성
    end_dec = [("B", 0, 0, 0), ("S", 1.82, 0, 0), ("S", -0.91, 1.58, 0), ("S", -0.91, -1.58, 0),
               ("P", 8, 0, 0), ("O", 0, 1.42, 0), ("S", 8, 2.05, 0)]
    # 끝(정상): 열적 신축만 (±0.05 Å)
    end_ok = [("B", 0, 0, 0), ("S", 1.87, 0, 0), ("S", -0.94, 1.62, 0), ("S", -0.94, -1.62, 0),
              ("P", 8, 0, 0), ("O", 9.61, 0, 0), ("S", 8, 2.10, 0)]
    with tempfile.TemporaryDirectory() as d:
        d = pathlib.Path(d)
        (d / "dec.xyz").write_text(frame(start) + frame(end_dec))
        (d / "ok.xyz").write_text(frame(start) + frame(end_ok))
        (d / "one.xyz").write_text(frame(start))
        # ⚠ 프레임 **두 개**를 만들어야 셀 검사까지 간다 (프레임 1개면 그 전에 None 이다)
        _body = "".join(f"{e} {x} {y} {z}\n" for e, x, y, z in start)
        (d / "nolat.xyz").write_text(
            f"{len(start)}\nno lattice here\n{_body}" * 2)

        r = traj_decomp_report(d / "dec.xyz")
        chk(r["verdict"] == "decomposition_started",
            f"양성: P–O 끊김 + B–O 생성 → decomposition_started ({r['delta']})")
        chk(r["delta"]["P-O"] == -1 and r["delta"]["B-O"] == 1,
            f"양성: 변화량이 정확 (P-O -1, B-O +1) — {r['delta']}")
        chk(r["frames"]["first"]["bonds"]["B-S"] == 3, "양성: 출발이 BS3 로 읽힌다")

        r2 = traj_decomp_report(d / "ok.xyz")
        chk(r2["verdict"] == "no_bond_exchange",
            f"⛔음성: 열적 신축만이면 '결합 교환 없음' ({r2['delta']})")
        chk(r2["frames"]["last"]["bonds"]["B-O"] == 0,
            "⛔음성: 신축으로 B–O 를 지어내지 않는다")

        chk(traj_decomp_report(d / "one.xyz") is None,
            "⛔음성: 프레임이 하나뿐이면 None (첫=끝 으로 통과시키지 않는다)")
        chk((traj_decomp_report(d / "nolat.xyz") or {}).get("error"),
            "⛔음성: Lattice= 가 없으면 error — 셀 없이 최소이미지를 흉내내지 않는다")

        # ⛔ 한쪽만 바뀌면 확정하지 않는다
        end_half = list(end_ok); end_half[5] = ("O", 20.0, 10.0, 10.0)   # O 가 멀리 — P–O 만 끊김
        (d / "half.xyz").write_text(frame(start) + frame(end_half))
        r3 = traj_decomp_report(d / "half.xyz")
        chk(r3["verdict"] == "partial_signal",
            f"⛔음성: P–O 만 끊기면 '한쪽만' — 분해 확정 아님 ({r3['delta']})")
    print(f"\n  selftest {ok[1]}/{ok[0]}")
    return 0 if ok[0] == ok[1] else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cif", default="db/structures/b2o3_relaxV0.cif")
    ap.add_argument("--json", default="db/properties/b2o3_bond_lengths_full.json")
    ap.add_argument("--traj", nargs="+", default=None,
                    help="확장 xyz 궤적들. 첫/끝 프레임의 결합을 세어 **분해 시작 여부**를 "
                         "판정한다 (P–O 끊김 + B–O 생성). CIF 모드와 같은 최소이미지 함수를 쓴다.")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return _selftest()

    if args.traj:
        rows = []
        print(f"{'traj':52s} {'P-O':>10s} {'B-O':>10s} {'B-S':>10s}  판정")
        for tp in args.traj:
            r = traj_decomp_report(tp)
            if r is None or r.get("error"):
                print(f"{tp[-52:]:52s} {'—':>10s} {'—':>10s} {'—':>10s}  "
                      f"{(r or {}).get('error', '프레임 부족')}")
                continue
            f0 = r["frames"]["first"]["bonds"]; f1 = r["frames"]["last"]["bonds"]
            mk = {"decomposition_started": "⛔ 분해 시작 (P–O 끊김 + B–O 생성)",
                  "partial_signal": "⚠ 한쪽만",
                  "no_bond_exchange": "⭕ 결합 교환 없음"}[r["verdict"]]
            print(f"{tp[-52:]:52s} {f0['P-O']:4d}→{f1['P-O']:<5d} "
                  f"{f0['B-O']:4d}→{f1['B-O']:<5d} {f0['B-S']:4d}→{f1['B-S']:<5d}  {mk}")
            rows.append(r)
        if args.json and rows:
            with open(args.json, "w") as fh:
                json.dump({"schema": "b2o3_traj_decomp/v1", "runs": rows}, fh,
                          ensure_ascii=False, indent=1)
            print(f"\n→ {args.json}")
        return 0

    cell, syms, fr = parse_cif(args.cif)
    L = lattice_matrix(*cell)
    syms = np.array(syms)
    N = len(syms)
    cart = fr @ L

    # exact minimum-image distance matrix (search translations -1..1)
    trans = np.array(list(itertools.product([-1, 0, 1], repeat=3))) @ L  # (27,3)
    D = np.full((N, N), 1e9)
    for i in range(N):
        diff = cart - cart[i]                         # (N,3)
        # for each j, min over 27 images
        dd = diff[:, None, :] + trans[None, :, :]     # (N,27,3)
        D[i] = np.sqrt((dd ** 2).sum(-1)).min(1)
    np.fill_diagonal(D, 1e9)

    def pairs(e1, e2, lo, hi):
        m1 = syms == e1; m2 = syms == e2
        out = []
        idx1 = np.where(m1)[0]; idx2 = np.where(m2)[0]
        for i in idx1:
            for j in idx2:
                if e1 == e2 and j <= i:
                    continue
                d = D[i, j]
                if lo <= d <= hi:
                    out.append((i, j, d))
        return out

    def stat(lst):
        if not lst:
            return None
        d = np.array([x[2] for x in lst])
        return dict(mean=round(float(d.mean()), 3), std=round(float(d.std()), 3),
                    min=round(float(d.min()), 3), max=round(float(d.max()), 3),
                    n=len(d))

    # --- bond cutoffs (first coordination shell) ---
    cat_anion = {
        "P-S": ("P", "S", 1.8, 2.5),
        "P-O": ("P", "O", 1.3, 1.9),
        "B-S": ("B", "S", 1.5, 2.2),
        "B-O": ("B", "O", 1.2, 1.8),
        "Li-S": ("Li", "S", 1.9, 3.2),
        "Li-Cl": ("Li", "Cl", 2.0, 3.4),
        "Li-O": ("Li", "O", 1.6, 2.8),
    }
    anion_anion = {
        "S-S(cage)": ("S", "S", 3.0, 3.8),
        "S-Cl": ("S", "Cl", 3.0, 4.2),
        "Cl-Cl": ("Cl", "Cl", 3.5, 4.6),
    }
    framework = {
        "P-P": ("P", "P", 3.5, 5.5),
        "Li-Li": ("Li", "Li", 2.0, 3.2),
    }

    result = {"bonds_cation_anion": {}, "anion_anion": {}, "framework": {}}
    for k, (e1, e2, lo, hi) in cat_anion.items():
        result["bonds_cation_anion"][k] = stat(pairs(e1, e2, lo, hi))
    for k, (e1, e2, lo, hi) in anion_anion.items():
        result["anion_anion"][k] = stat(pairs(e1, e2, lo, hi))
    for k, (e1, e2, lo, hi) in framework.items():
        result["framework"][k] = stat(pairs(e1, e2, lo, hi))

    # --- per-P environment (PS4 / PS3O / PS2O2) ---
    Pidx = np.where(syms == "P")[0]
    Sidx = np.where(syms == "S")[0]
    Oidx = np.where(syms == "O")[0]
    p_env = {}
    for p in Pidx:
        nS = [(s, D[p, s]) for s in Sidx if D[p, s] <= 2.5]
        nO = [(o, D[p, o]) for o in Oidx if D[p, o] <= 1.9]
        key = f"PS{len(nS)}" + (f"O{len(nO)}" if nO else "")
        p_env.setdefault(key, {"P-S": [], "P-O": [], "count": 0})
        p_env[key]["count"] += 1
        p_env[key]["P-S"] += [d for _, d in nS]
        p_env[key]["P-O"] += [d for _, d in nO]
    p_env_out = {}
    for k, v in p_env.items():
        ps = np.array(v["P-S"]); po = np.array(v["P-O"])
        p_env_out[k] = {
            "n_P": v["count"] // 1 if False else len(np.unique([1])) and v["count"],
            "P-S_mean": round(float(ps.mean()), 3) if len(ps) else None,
            "P-O_mean": round(float(po.mean()), 3) if len(po) else None,
        }
    # fix n_P
    for k in p_env_out:
        p_env_out[k]["n_P"] = p_env[k]["count"]
    result["P_environments"] = p_env_out

    # --- S classification (free-S / B-S / P-S bridging) ---
    Bidx = np.where(syms == "B")[0]
    s_class = {"free-S": [], "B-S": [], "P-S(bridge)": []}
    for s in Sidx:
        boundB = any(D[s, b] <= 2.2 for b in Bidx)
        boundP = any(D[s, p] <= 2.5 for p in Pidx)
        if boundB:
            s_class["B-S"].append(s)
        elif boundP:
            s_class["P-S(bridge)"].append(s)
        else:
            s_class["free-S"].append(s)
    # Li-S distance per S class
    Liidx = np.where(syms == "Li")[0]
    s_class_out = {}
    for k, slist in s_class.items():
        lis = []
        for s in slist:
            lis += [D[li, s] for li in Liidx if D[li, s] <= 3.2]
        lis = np.array(lis)
        s_class_out[k] = {
            "n_S": len(slist),
            "Li-S_mean": round(float(lis.mean()), 3) if len(lis) else None,
            "Li-S_std": round(float(lis.std()), 3) if len(lis) else None,
            "n_LiS": len(lis),
        }
    result["S_classification"] = s_class_out

    # --- Cl 4a/4d (octahedral Z>=5 vs anti-site Z<5) + per-site Li-Cl ---
    Clidx = np.where(syms == "Cl")[0]
    cl4a, cl4d = [], []
    for cl in Clidx:
        Z = sum(1 for li in Liidx if D[cl, li] <= 3.4)
        (cl4a if Z >= 5 else cl4d).append(cl)
    def licl(clset):
        d = [D[li, cl] for cl in clset for li in Liidx if D[li, cl] <= 3.4]
        d = np.array(d)
        return (dict(mean=round(float(d.mean()), 3), std=round(float(d.std()), 3),
                     min=round(float(d.min()), 3), max=round(float(d.max()), 3),
                     n=len(d)) if len(d) else None)
    result["Cl_sites"] = {
        "n_4a": len(cl4a), "n_4d": len(cl4d),
        "Li-Cl_4a": licl(cl4a), "Li-Cl_4d": licl(cl4d),
        "Li-Cl_all": licl(list(Clidx)),
    }

    # --- print ---
    print("=== cation-anion bonds ===")
    for k, v in result["bonds_cation_anion"].items():
        if v: print(f"  {k:7s} {v['mean']:.3f} +/- {v['std']:.3f}  "
                     f"[{v['min']:.3f},{v['max']:.3f}]  n={v['n']}")
    print("=== anion-anion contacts ===")
    for k, v in result["anion_anion"].items():
        if v: print(f"  {k:11s} {v['mean']:.3f} +/- {v['std']:.3f}  n={v['n']}")
    print("=== framework ===")
    for k, v in result["framework"].items():
        if v: print(f"  {k:7s} {v['mean']:.3f} +/- {v['std']:.3f}  n={v['n']}")
    print("=== P environments ===")
    for k, v in result["P_environments"].items():
        print(f"  {k:7s} n_P={v['n_P']}  P-S={v['P-S_mean']}  P-O={v['P-O_mean']}")
    print("=== S classification ===")
    for k, v in result["S_classification"].items():
        print(f"  {k:13s} n_S={v['n_S']:2d}  Li-S={v['Li-S_mean']} +/-{v['Li-S_std']} (n={v['n_LiS']})")
    print("=== Cl sites ===")
    cs = result["Cl_sites"]
    print(f"  4a n={cs['n_4a']}  Li-Cl={cs['Li-Cl_4a']}")
    print(f"  4d n={cs['n_4d']}  Li-Cl={cs['Li-Cl_4d']}")

    import os
    os.makedirs("db/properties", exist_ok=True) if os.path.dirname(args.json) else None
    json.dump(result, open(args.json, "w"), indent=2)
    print(f"\n-> {args.json}")


if __name__ == "__main__":
    main()
