#!/usr/bin/env python3
"""Per-site bond environment for argyrodite Li-PS-X.

Splits bonds by anion site type:
  - 4a-Cl: octahedral Cl[Li6] cage center (Z=6, large V_poly)
  - 4d-Cl: tetrahedral Cl[Li4] anti-site at S-position (Z=4, small V_poly)
  - 4d-S : free S²⁻ at 4d site (no P neighbor)
  - PS4-S: S in PS4 tetrahedra (has P neighbor at ≈ 2.07 Å)

Then reports:
  - Li-Li
  - Li-Cl(4a)  vs  Li-Cl(4d)
  - Li-S(PS4)  vs  Li-S(4d)
  - Cl-Cl  (when present)
  - per-Cl-site bond statistics (each Cl indexed individually with Z, V_poly, mean d)

Usage:
    python3 per_site_bond_analysis.py --cif V0_init.cif --out V0_per_site.json

--framework (2026-10-23 · Nd 결정 D-2026-10-19-nd-q23-ppswap-structure 재개 ① 문턱):
  'argyrodite 골격인가' 네 기준을 09-18 판정 (nd_ppswap_vcrelax_result_2026_09_18.json §3)
  그대로 다시 잰다 — 그때는 손으로 쟀고 재현 도구가 없었다.
    ① 고립 ortho 음이온 — P 마다 Z = 4 (P–S ≤ 2.4 · P–O ≤ 1.9 Å) · 다리 음이온 0
    ② ccp 골격 — P 마다 P–P ≤ 7.6 Å 이웃 12
    ③ 자유 음이온 수지 — P 이웃이 없는 음이온 수 = 2 × P 수 (4a 1 + 4d 1)
    ④ Li 케이지 — 자유 S 마다 Li ≤ 3.2 Å 5 개 이상 (Cl 은 같은 잣대로 4a/4d 만 센다)
  python3 per_site_bond_analysis.py --framework --cif <구조 (cif · xyz · QE 입력)>
  python3 per_site_bond_analysis.py --selftest

⛔ --framework 가 못 하는 것
  · 대칭을 말하지 않는다 (P1 초격자면 P1 이다 — 'F-43m' 근거가 아니다)
  · Li 배열이 바닥상태인지 말하지 않는다
  · 문턱 거리 (2.4 · 1.9 · 7.6 · 3.2 Å) 는 이 계 (Nd/O LPSCl1.6) 의 09-18 · 10-19 값이다 —
    다른 계 (B · 큰 양이온) 에 쓰기 전에 거리 분포부터 본다
"""
import argparse, json
from pathlib import Path
import numpy as np
from ase.io import read
from ase.neighborlist import neighbor_list


# argyrodite-standard cutoffs (Å)
CUTOFFS = {
    ("P", "S"):   2.3,
    ("Li", "S"):  3.2,
    ("Li", "Cl"): 3.4,
    ("Li", "Li"): 3.6,
    ("S", "S"):   4.0,
    ("Cl", "Cl"): 4.6,
    ("P", "Cl"):  4.5,
}


def pair_cut(a, b):
    """Symmetric lookup — try both orderings."""
    return CUTOFFS.get((a, b), CUTOFFS.get((b, a), 0.0))


def neighbors_within(i_idx, j_idx, d, sym, idx, target=None, cut=None):
    sel = (i_idx == idx)
    out = []
    for j, dij in zip(j_idx[sel], d[sel]):
        if target is not None and sym[j] != target:
            continue
        if cut is not None and dij > cut:
            continue
        out.append((j, dij))
    return out


def classify_anion_sites(atoms, sym, i_idx, j_idx, d):
    """Tag each Cl as '4a' (Z=6) or '4d' (Z=4), and each S as 'PS4' or '4d'."""
    tags = {}
    for i, s in enumerate(sym):
        if s == "Cl":
            nbrs_li = neighbors_within(i_idx, j_idx, d, sym, i,
                                        target="Li", cut=pair_cut("Li", "Cl"))
            z_li = len(nbrs_li)
            if z_li >= 5:
                tags[i] = ("Cl", "4a")
            else:
                tags[i] = ("Cl", "4d")
        elif s == "S":
            nbrs_p = neighbors_within(i_idx, j_idx, d, sym, i,
                                       target="P", cut=pair_cut("P", "S"))
            tags[i] = ("S", "PS4" if nbrs_p else "4d")
    return tags


def dedup_bonds(triples):
    """neighbor_list returns each bond twice (i→j and j→i). Halve the list."""
    seen = set()
    out = []
    for i, j, dij in triples:
        key = (min(i, j), max(i, j))
        if key in seen:
            continue
        seen.add(key)
        out.append((i, j, dij))
    return out


def summarize(distances):
    if not distances:
        return {"n": 0, "mean": None, "std": None, "min": None, "max": None}
    arr = np.array(distances)
    return {
        "n": len(arr),
        "mean": float(arr.mean()),
        "std": float(arr.std()),
        "min": float(arr.min()),
        "max": float(arr.max()),
    }


#: --framework 문턱 (Å) — 09-18 판정 · 10-19 Bader 자리 분류 문턱 그대로
FW_P_ANION = {"S": 2.4, "O": 1.9}   # ① P–음이온 결합 (Cl 은 P 와 결합 안 함)
FW_PP_CN = 7.6                        # ② P–P 첫 껍질 (fcc 최근접 a/√2 ≈ 6.96 · 둘째 a ≈ 9.8)
FW_LI_CAGE = {"S": 3.2, "Cl": 3.4}    # ④ CUTOFFS 의 Li–S · Li–Cl 과 같다
FW_CAGE_MIN = 5
#: ④ 케이지 양이온 = Li 자리에 앉은 양이온 — Nd 는 Li 자리에 있다 (09-18 셈).
#:   Li 만 세면 6 월 champion 의 자유 S 하나 (Li 4 + Nd 1) 가 빠져 3/4 · Cl 4a 9 / 4d 7 이 나온다 —
#:   09-18 기록 (4/4 · 10/6) 은 Li + Nd 를 센 값이다 (2026-10-23 재현으로 확인).
FW_CAGE_CATIONS = ("Li", "Nd")
TETRA = 109.4712206


def _anion_p_bonds(sym, i_idx, j_idx, d):
    """음이온 → 결합한 P 목록 (FW_P_ANION 문턱)."""
    bonds = {}
    for i, j, dij in zip(i_idx, j_idx, d):
        if sym[i] == "P" and sym[j] in FW_P_ANION and dij <= FW_P_ANION[sym[j]]:
            bonds.setdefault(int(j), set()).add(int(i))
    return bonds


def framework_check(atoms):
    """argyrodite 골격 네 기준 → dict (`pass` · `failed` · 측정값). 09-18 판정의 재현."""
    sym = atoms.get_chemical_symbols()
    i_idx, j_idx, d, D = neighbor_list("ijdD", atoms, max(FW_PP_CN, 4.0))
    P = [k for k, s in enumerate(sym) if s == "P"]
    anions = [k for k, s in enumerate(sym) if s in ("S", "Cl", "O")]
    a2p = _anion_p_bonds(sym, i_idx, j_idx, d)
    # ① P 배위 · 다리 · 거리 · 각
    z, pd_s, pd_o, angs = {}, [], [], []
    for p in P:
        sel = (i_idx == p) & np.isin(j_idx, list(a2p)) & np.array(
            [sym[j] in FW_P_ANION and dd <= FW_P_ANION[sym[j]]
             for j, dd in zip(j_idx, d)])
        vecs = D[sel]
        z[p] = int(sel.sum())
        for j, dd in zip(j_idx[sel], d[sel]):
            (pd_s if sym[j] == "S" else pd_o).append(float(dd))
        for a in range(len(vecs)):
            for b in range(a + 1, len(vecs)):
                c = np.dot(vecs[a], vecs[b]) / (np.linalg.norm(vecs[a]) * np.linalg.norm(vecs[b]))
                angs.append(float(np.degrees(np.arccos(np.clip(c, -1, 1)))))
    bridging = sorted(k for k, ps in a2p.items() if len(ps) >= 2)
    # ② P–P 첫 껍질
    cn = {p: int(((i_idx == p) & (np.array(sym)[j_idx] == "P") & (d <= FW_PP_CN)).sum()) for p in P}
    # ③ 자유 음이온
    free = [k for k in anions if k not in a2p]
    # ④ 자유 S · Cl 의 케이지 양이온 수 (Li 자리 양이온 = Li + Nd)
    def z_li(k):
        return int(((i_idx == k) & np.isin(np.array(sym)[j_idx], FW_CAGE_CATIONS)
                    & (d <= FW_LI_CAGE[sym[k]])).sum())
    free_S = [k for k in free if sym[k] == "S"]
    free_O = [k for k in free if sym[k] == "O"]
    S_cage = {k: z_li(k) for k in free_S}
    Cl_z = {k: z_li(k) for k in anions if sym[k] == "Cl"}
    n_fu = len(P)
    a_cub = (4.0 * atoms.get_volume() / n_fu) ** (1 / 3) if n_fu else None
    r = {
        "n_P": n_fu, "Z_P": sorted(set(z.values())), "n_P_Z4": sum(v == 4 for v in z.values()),
        "bridging_anions": bridging,
        "P_S_range_A": [min(pd_s), max(pd_s)] if pd_s else None,
        "P_O_list_A": sorted(round(x, 3) for x in pd_o),
        "XPX_mean_deg": float(np.mean(angs)) if angs else None,
        "XPX_rms_dev_deg": float(np.sqrt(np.mean((np.array(angs) - TETRA) ** 2))) if angs else None,
        "XPX_range_deg": [min(angs), max(angs)] if angs else None,
        "n_P_CN12": sum(v == 12 for v in cn.values()), "PP_CN_values": sorted(set(cn.values())),
        "n_free_anions": len(free), "free_per_P": (len(free) / n_fu) if n_fu else None,
        "free_S": len(free_S), "free_O": len(free_O),
        "free_S_caged": sum(v >= FW_CAGE_MIN for v in S_cage.values()),
        "free_S_ZLi": sorted(S_cage.values()),
        "Cl_4a": sum(v >= FW_CAGE_MIN for v in Cl_z.values()),
        "Cl_4d": sum(v < FW_CAGE_MIN for v in Cl_z.values()),
        "a_cubic_equiv_from_V_A": a_cub,
        "cell_angles_deg": [float(x) for x in atoms.cell.cellpar()[3:]],
        "thresholds_A": {"P_anion": FW_P_ANION, "PP_CN": FW_PP_CN, "Li_cage": FW_LI_CAGE,
                         "cage_min": FW_CAGE_MIN, "cage_cations": list(FW_CAGE_CATIONS)},
    }
    failed = []
    if not n_fu or r["n_P_Z4"] != n_fu or bridging:
        failed.append("①_고립_ortho_음이온")
    if r["n_P_CN12"] != n_fu:
        failed.append("②_ccp_골격")
    if len(free) != 2 * n_fu:
        failed.append("③_자유_음이온_수지")
    if r["free_S_caged"] != len(free_S):
        failed.append("④_Li_케이지")
    r["failed"], r["pass"] = failed, not failed
    return r


def _print_framework(r, name):
    ok = "✅ 충족" if r["pass"] else f"⛔ 불충족 {r['failed']}"
    print(f"[{name}] argyrodite 골격 네 기준 — {ok}")
    print(f"  ① P Z=4 {r['n_P_Z4']}/{r['n_P']} · 다리 음이온 {len(r['bridging_anions'])}"
          f" · P–S {r['P_S_range_A'][0]:.3f}–{r['P_S_range_A'][1]:.3f} Å"
          + (f" · P–O {r['P_O_list_A']}" if r['P_O_list_A'] else "")
          + f" · X–P–X 평균 {r['XPX_mean_deg']:.2f}° (RMS 편차 {r['XPX_rms_dev_deg']:.2f}°,"
            f" 범위 {r['XPX_range_deg'][0]:.1f}–{r['XPX_range_deg'][1]:.1f}°)")
    print(f"  ② P–P ≤ {FW_PP_CN} Å CN=12 {r['n_P_CN12']}/{r['n_P']} (값 {r['PP_CN_values']})"
          f" · 셀 각 {', '.join(f'{x:.2f}' for x in r['cell_angles_deg'])}°"
          f" · 부피 입방 등가 a {r['a_cubic_equiv_from_V_A']:.3f} Å")
    print(f"  ③ 자유 음이온 {r['n_free_anions']} / P {r['n_P']} = {r['free_per_P']:.2f}"
          f" (S {r['free_S']} · O {r['free_O']} · Cl {r['Cl_4a'] + r['Cl_4d']})")
    print(f"  ④ 자유 S 케이지 (Z(Li+Nd) ≥ {FW_CAGE_MIN}) {r['free_S_caged']}/{r['free_S']}"
          f" (Z {r['free_S_ZLi']}) · Cl 4a {r['Cl_4a']} / 4d {r['Cl_4d']}")


def _selftest():
    """양성: 09-18 판정 (손 계산) 재현 · 음성: 기준마다 하나씩 깨서 그 기준만 빨강인지."""
    root = Path(__file__).resolve().parents[2]
    ref = root / "db/structures/modelc_nd_doped_DFTrelax.cif"
    n_ok = n_bad = 0

    def chk(c, m):
        nonlocal n_ok, n_bad
        print(("  ✓ " if c else "  ✗ ") + m)
        n_ok, n_bad = n_ok + bool(c), n_bad + (not c)

    a0 = read(str(ref))
    r = framework_check(a0)
    chk(r["pass"], "[양성] 6 월 champion (09-18 판정 대상) 이 네 기준 충족")
    chk(r["n_P_Z4"] == 10 and not r["bridging_anions"], "[양성] ① 10/10 P Z=4 · 다리 0 (09-18)")
    chk(abs(r["P_S_range_A"][0] - 2.02) < 0.005 and abs(r["P_S_range_A"][1] - 2.10) < 0.005,
        f"[양성] ① P–S 2.02–2.10 Å (09-18) ← {r['P_S_range_A']}")
    chk(abs(r["XPX_mean_deg"] - 109.44) < 0.005 and abs(r["XPX_rms_dev_deg"] - 3.25) < 0.005,
        f"[양성] ① X–P–X 109.44° · RMS 3.25° (09-18) ← {r['XPX_mean_deg']:.3f} · {r['XPX_rms_dev_deg']:.3f}")
    chk(r["n_P_CN12"] == 10, "[양성] ② CN12 10/10 (09-18)")
    chk(r["n_free_anions"] == 20 and r["free_S"] == 4, "[양성] ③ 자유 음이온 20 (S 4) (09-18)")
    chk(r["free_S_caged"] == 4 and r["Cl_4a"] == 10 and r["Cl_4d"] == 6,
        f"[양성] ④ 자유 S 4/4 · Cl 4a 10 / 4d 6 (09-18) ← {r['free_S_caged']} · {r['Cl_4a']}/{r['Cl_4d']}")

    # ① 음성 — PS₄ 의 S 하나를 P 에서 1 Å 더 떼면 Z=3 · 자유 음이온 +1 (①·③ 만)
    a1 = a0.copy()
    sym = a1.get_chemical_symbols()
    ii, jj, dd, DD = neighbor_list("ijdD", a1, 2.4)
    k = next(n for n in range(len(ii)) if sym[ii[n]] == "P" and sym[jj[n]] == "S")
    pos = a1.get_positions()
    pos[jj[k]] += DD[k] / np.linalg.norm(DD[k]) * 1.0
    a1.set_positions(pos)
    r1 = framework_check(a1)
    chk("①_고립_ortho_음이온" in r1["failed"] and "③_자유_음이온_수지" in r1["failed"]
        and "②_ccp_골격" not in r1["failed"],
        f"[음성] S 하나를 떼면 ①·③ 빨강 · ② 는 아님 (뗀 S 가 자유 S 로 세여 ④ 도 걸릴 수 있다) ← {r1['failed']}")
    # ② 음성 — 셀과 원자를 1.12 배 → P–P 7.8 Å > 7.6 (P–S 2.30 < 2.4 라 ① 은 그대로)
    a2 = a0.copy()
    a2.set_cell(a0.cell * 1.12, scale_atoms=True)
    r2 = framework_check(a2)
    chk("②_ccp_골격" in r2["failed"] and "①_고립_ortho_음이온" not in r2["failed"],
        f"[음성] 1.12 배 늘리면 ② 빨강 · ① 은 아님 ← {r2['failed']}")
    # ④ 음성 — 자유 S 하나 주변 Li (≤ 3.2 Å) 를 지우면 ④ 만
    a3 = a0.copy()
    s3 = a3.get_chemical_symbols()
    ii, jj, dd = neighbor_list("ijd", a3, 3.2)
    fs = [n for n in range(len(a3)) if s3[n] == "S"
          and not any(s3[jj[m]] == "P" for m in np.where(ii == n)[0] if dd[m] <= 2.4)][0]
    kill = sorted({int(jj[m]) for m in np.where(ii == fs)[0] if s3[jj[m]] in FW_CAGE_CATIONS})
    del a3[kill]
    r3 = framework_check(a3)
    chk(r3["failed"] == ["④_Li_케이지"],
        f"[음성] 자유 S 주변 케이지 양이온 {len(kill)} 개를 지우면 ④ 만 (음이온 수는 그대로) ← {r3['failed']}")
    # ① 다리 음이온 음성 — P–S–P 를 직접 만든다 (큰 상자)
    from ase import Atoms
    a4 = Atoms("P2S7", positions=[[0, 0, 0], [4.0, 0, 0], [2.0, 0, 0],
                                   [-1.2, 1.7, 0], [-1.2, -1.7, 0], [-1.2, 0, 1.7],
                                   [5.2, 1.7, 0], [5.2, -1.7, 0], [5.2, 0, 1.7]],
               cell=[30, 30, 30], pbc=True)
    r4 = framework_check(a4)
    chk(r4["bridging_anions"] == [2] and "①_고립_ortho_음이온" in r4["failed"],
        f"[음성] P–S–P 다리 → ① 빨강 ← 다리 {r4['bridging_anions']}")
    print(f"framework selftest: ✓ {n_ok} · ✗ {n_bad}")
    return 0 if n_bad == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cif", help="구조 (cif · xyz · QE 입력 — ase 가 읽는 것)")
    ap.add_argument("--out", default="V0_per_site.json")
    ap.add_argument("--framework", action="store_true",
                    help="argyrodite 골격 네 기준만 잰다 (09-18 판정 재현) · 충족이면 끝 0, 아니면 1")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        raise SystemExit(_selftest())
    if not args.cif:
        ap.error("--cif 가 필요하다")
    if args.framework:
        r = framework_check(read(args.cif))
        _print_framework(r, Path(args.cif).name)
        if args.out != "V0_per_site.json":
            Path(args.out).write_text(json.dumps(r, indent=1, ensure_ascii=False))
            print(f"→ {args.out}")
        raise SystemExit(0 if r["pass"] else 1)

    atoms = read(args.cif)
    sym = atoms.get_chemical_symbols()
    print(f"natoms={len(atoms)}, V={atoms.get_volume():.4f} Å³, "
          f"formula={atoms.get_chemical_formula()}")

    i_idx, j_idx, d = neighbor_list("ijd", atoms, 4.6)

    # 1. Classify anion sites
    tags = classify_anion_sites(atoms, sym, i_idx, j_idx, d)
    cl_4a = [i for i, t in tags.items() if t == ("Cl", "4a")]
    cl_4d = [i for i, t in tags.items() if t == ("Cl", "4d")]
    s_ps4 = [i for i, t in tags.items() if t == ("S", "PS4")]
    s_4d  = [i for i, t in tags.items() if t == ("S", "4d")]
    print(f"\n=== Anion site assignment ===")
    print(f"  Cl 4a (Z≥5): {len(cl_4a)}   Cl 4d (Z<5): {len(cl_4d)}")
    print(f"  S in PS4   : {len(s_ps4)}   S free 4d  : {len(s_4d)}")

    # 2. Bond lists per pair type, with per-site split
    bonds = {
        "Li-Li":      [],
        "Li-Cl(4a)":  [],
        "Li-Cl(4d)":  [],
        "Li-S(PS4)":  [],
        "Li-S(4d)":   [],
        "P-S":        [],
        "S-S":        [],
        "Cl-Cl":      [],
        "Cl(4a)-Cl(4a)": [],
        "Cl(4a)-Cl(4d)": [],
        "Cl(4d)-Cl(4d)": [],
    }
    for i, j, dij in zip(i_idx, j_idx, d):
        a, b = sym[i], sym[j]
        cut = pair_cut(a, b)
        if cut == 0 or dij > cut:
            continue
        pair = tuple(sorted([a, b]))
        if pair == ("Li", "Li"):
            bonds["Li-Li"].append((i, j, dij))
        elif pair == ("Cl", "Li"):
            cl_idx = i if a == "Cl" else j
            sub = tags[cl_idx][1]
            bonds[f"Li-Cl({sub})"].append((i, j, dij))
        elif pair == ("Li", "S"):
            s_idx = i if a == "S" else j
            sub = tags[s_idx][1]
            bonds[f"Li-S({sub})"].append((i, j, dij))
        elif pair == ("P", "S"):
            bonds["P-S"].append((i, j, dij))
        elif pair == ("S", "S"):
            bonds["S-S"].append((i, j, dij))
        elif pair == ("Cl", "Cl"):
            bonds["Cl-Cl"].append((i, j, dij))
            ta, tb = tags[i][1], tags[j][1]
            ss = tuple(sorted([ta, tb]))
            key = f"Cl({ss[0]})-Cl({ss[1]})"
            if key in bonds:
                bonds[key].append((i, j, dij))

    # Dedup (neighbor_list double-counts)
    for k in bonds:
        bonds[k] = dedup_bonds(bonds[k])

    # 3. Summary stats per bond category
    print(f"\n=== Per-category bond statistics ===")
    stats = {}
    for k, triples in bonds.items():
        dlist = [t[2] for t in triples]
        s = summarize(dlist)
        stats[k] = s
        if s["n"] > 0:
            print(f"  {k:<18} n={s['n']:3d}  mean={s['mean']:.4f} ± "
                  f"{s['std']:.4f}  [{s['min']:.3f}, {s['max']:.3f}] Å")
        else:
            print(f"  {k:<18} n=0")

    # 4. Per-Cl-site details (each Cl atom individually)
    print(f"\n=== Per-Cl-atom detail ===")
    cl_detail = []
    for i in [k for k in range(len(atoms)) if sym[k] == "Cl"]:
        nbrs_li = neighbors_within(i_idx, j_idx, d, sym, i,
                                    target="Li", cut=pair_cut("Li", "Cl"))
        d_li = [n[1] for n in nbrs_li]
        z_li = len(d_li)
        d_mean = float(np.mean(d_li)) if d_li else None
        d_std = float(np.std(d_li)) if d_li else None
        rec = {
            "atom_idx": int(i),
            "site": tags[i][1],
            "Z_Li": z_li,
            "Li_Cl_mean_A": d_mean,
            "Li_Cl_std_A": d_std,
            "Li_Cl_min_A": float(min(d_li)) if d_li else None,
            "Li_Cl_max_A": float(max(d_li)) if d_li else None,
        }
        cl_detail.append(rec)
        print(f"  Cl[{i:3d}] site={tags[i][1]:>2}  Z(Li)={z_li}  "
              f"mean Li-Cl = {d_mean:.4f} Å"
              f" ± {d_std:.4f}" if d_std else "")

    # 5. Per-Li-atom: Li environment (counts and distances)
    print(f"\n=== Per-Li-atom environment (first 8) ===")
    li_detail = []
    for li_idx in [k for k in range(len(atoms)) if sym[k] == "Li"]:
        nS_ps4 = sum(1 for n, dn in neighbors_within(i_idx, j_idx, d, sym,
                                                       li_idx, target="S",
                                                       cut=pair_cut("Li", "S"))
                      if tags[n][1] == "PS4")
        nS_4d  = sum(1 for n, dn in neighbors_within(i_idx, j_idx, d, sym,
                                                       li_idx, target="S",
                                                       cut=pair_cut("Li", "S"))
                      if tags[n][1] == "4d")
        nCl_4a = sum(1 for n, dn in neighbors_within(i_idx, j_idx, d, sym,
                                                       li_idx, target="Cl",
                                                       cut=pair_cut("Li", "Cl"))
                      if tags[n][1] == "4a")
        nCl_4d = sum(1 for n, dn in neighbors_within(i_idx, j_idx, d, sym,
                                                       li_idx, target="Cl",
                                                       cut=pair_cut("Li", "Cl"))
                      if tags[n][1] == "4d")
        env = f"S(PS4)_{nS_ps4}_S(4d)_{nS_4d}_Cl(4a)_{nCl_4a}_Cl(4d)_{nCl_4d}"
        li_detail.append({
            "atom_idx": int(li_idx), "env": env,
            "nS_PS4": nS_ps4, "nS_4d": nS_4d,
            "nCl_4a": nCl_4a, "nCl_4d": nCl_4d,
        })
    # Aggregate Li env types
    from collections import Counter
    env_counts = Counter(rec["env"] for rec in li_detail)
    print(f"  Li environment types ({len(env_counts)} unique):")
    for env, n in env_counts.most_common():
        print(f"    {env}: {n} Li sites")

    # 6. Dump JSON
    out = {
        "formula": atoms.get_chemical_formula(),
        "natoms": len(atoms),
        "volume_A3": float(atoms.get_volume()),
        "anion_sites": {
            "Cl_4a": len(cl_4a),
            "Cl_4d": len(cl_4d),
            "S_PS4": len(s_ps4),
            "S_4d":  len(s_4d),
            "Cl_4d_fraction": (
                len(cl_4d) / (len(cl_4a) + len(cl_4d))
                if (len(cl_4a) + len(cl_4d)) else 0.0),
        },
        "bond_stats": stats,
        "per_Cl_detail": cl_detail,
        "Li_environment_types": dict(env_counts),
    }
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n→ {args.out}")


if __name__ == "__main__":
    main()
