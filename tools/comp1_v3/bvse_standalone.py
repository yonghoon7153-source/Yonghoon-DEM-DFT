#!/usr/bin/env python3
"""Standalone BVSE (Bond-Valence Site Energy) map + percolation barrier for Li.

No ASE/pymatgen — pure numpy + scipy. Parses a P1 CIF directly. Built for
KISTI where only the base conda (numpy/scipy) is guaranteed.

  BVS(r) = Σ_{X in anions} exp((R0_X - d(r,X)) / b)        (anions = S, Cl, O)
  BVSE(r) = (BVS(r) - 1.0)²    (Li⁺ ideal valence = 1.0)
  Li migration barrier ≈ min E such that {BVSE ≤ E} PERCOLATES (spans a full
  period along some axis), measured above the global BVSE minimum.

Usage:
    python3 bvse_standalone.py b2o3_relaxV0.cif --grid 28 --prefix b2o3
    python3 bvse_standalone.py modelc_2x_V0.xyz --grid 28 --prefix modelc2x
    python3 bvse_standalone.py --selftest        # 시험 (음성 경로 포함)
Outputs: <prefix>_bvse_map.npy, <prefix>_bvse_summary.json (+ stdout).
"""
import sys, re, json, argparse, math
import numpy as np
from scipy import ndimage

BV = {  # Li–X bond-valence params (Brown-Altermatt), b=0.37
    "S":  (2.105, 0.37),
    "Cl": (2.249, 0.37),
    "O":  (1.466, 0.37),
}
V_IDEAL = 1.0


def cell_matrix(a, b, c, al_deg, be_deg, ga_deg):
    """(a,b,c,alpha,beta,gamma) -> 격자행렬 A (행 = 격자벡터), **CIF 관례 고정**.

    ⛔ 왜 함수로 뺐나 (2026-09-18): .xyz 입력을 붙이면서 두 경로가 서로 다른 방향의
      A 를 만들면, 같은 셀인데 다른 맵이 나올 수 있다. 두 경로 모두 **여기로** 들어온다.
    """
    al, be, ga = map(math.radians, (al_deg, be_deg, ga_deg))
    cs = math.cos
    v = math.sqrt(1 - cs(al)**2 - cs(be)**2 - cs(ga)**2 + 2*cs(al)*cs(be)*cs(ga))
    return np.array([[a, 0, 0],
                     [b*cs(ga), b*math.sin(ga), 0],
                     [c*cs(be), c*(cs(al)-cs(be)*cs(ga))/math.sin(ga), c*v/math.sin(ga)]])


def parse_xyz(fn):
    """extxyz (Lattice="..." 행 = 격자벡터, 데카르트 좌표) -> (A, frac, sym).

    ⛔ 이 파서가 **하지 않는 것**
      · 대칭을 찾지 않는다 — P1 그대로 쓴다 (CIF 경로와 같다).
      · 점유율(occupancy)을 모른다 — extxyz 에 없다. 부분점유 구조면 쓰면 안 된다.
      · Lattice= 가 없으면 **추측하지 않고 죽는다**. 비주기 xyz 를 주기셀로 오인하면
        BVSE 맵이 통째로 틀린다 (조용히 틀린 경로).
    """
    lines = open(fn).read().splitlines()
    if not lines:
        raise SystemExit("⛔ %s: 빈 파일이다" % fn)
    try:
        n = int(lines[0].split()[0])
    except (ValueError, IndexError):
        raise SystemExit("⛔ %s: 첫 줄이 원자수가 아니다 — xyz 가 아니다" % fn)
    if len(lines) < 2:
        raise SystemExit("⛔ %s: 주석 줄이 없다" % fn)
    m = re.search(r'Lattice="([^"]+)"', lines[1])
    if not m:
        raise SystemExit("⛔ %s: 둘째 줄에 Lattice= 가 없다 — 주기셀을 모른다. "
                         "비주기 xyz 로 BVSE 를 돌리면 맵이 통째로 틀린다." % fn)
    vals = [float(x) for x in m.group(1).split()]
    if len(vals) != 9:
        raise SystemExit("⛔ %s: Lattice 가 9 개가 아니다 (%d 개)" % (fn, len(vals)))
    L = np.array(vals, float).reshape(3, 3)
    if abs(np.linalg.det(L)) < 1e-6:
        raise SystemExit("⛔ %s: 격자 부피가 0 이다 (det = %.3g)" % (fn, np.linalg.det(L)))
    sym, cart = [], []
    for ln in lines[2:2 + n]:
        tok = ln.split()
        if len(tok) < 4:
            raise SystemExit("⛔ %s: 원자 줄이 4 열 미만이다 — %r" % (fn, ln))
        sym.append("".join(ch for ch in tok[0] if ch.isalpha()))
        cart.append([float(tok[1]), float(tok[2]), float(tok[3])])
    if len(sym) != n:
        raise SystemExit("⛔ %s: 첫 줄이 %d 인데 원자 줄이 %d 개다" % (fn, n, len(sym)))
    frac = np.asarray(cart) @ np.linalg.inv(L)
    frac -= np.floor(frac)                      # 셀 안으로 접는다
    a, b, c = np.linalg.norm(L, axis=1)

    def ang(i, j, x, y):
        return math.degrees(math.acos(float(np.clip(np.dot(L[i], L[j]) / (x * y), -1.0, 1.0))))

    return cell_matrix(a, b, c, ang(1, 2, b, c), ang(0, 2, a, c), ang(0, 1, a, b)), frac, sym


def parse_structure(fn):
    """확장자로 갈라 (A, frac, sym). 모르는 확장자면 **죽는다**(추측 안 한다)."""
    low = fn.lower()
    if low.endswith(".cif"):
        return parse_cif(fn)
    if low.endswith((".xyz", ".extxyz")):
        return parse_xyz(fn)
    raise SystemExit("⛔ %s: .cif / .xyz 만 읽는다 (확장자로 판단한다)" % fn)


def parse_cif(fn):
    t = open(fn).read()
    g = lambda k: float(re.search(k + r"\s+([\d.]+)", t).group(1))
    a, b, c = g("_cell_length_a"), g("_cell_length_b"), g("_cell_length_c")
    A = cell_matrix(a, b, c, *(g("_cell_angle_" + x) for x in ("alpha", "beta", "gamma")))
    # header-aware atom parse: works for both `label symbol x y z` and
    # `symbol label mult x y z occ` column orders (uses the _atom_site_ header).
    sym, frac = [], []
    lines = t.splitlines(); cols = []; inloop = False
    for ln in lines:
        s = ln.strip()
        if s.startswith("_atom_site_"):
            cols.append(s); inloop = True; continue
        if inloop and cols and s and not s.startswith("_") and s != "loop_":
            tok = ln.split()
            if len(tok) < len(cols):
                if frac: break
                continue
            isym = cols.index("_atom_site_type_symbol") if "_atom_site_type_symbol" in cols \
                else cols.index("_atom_site_label")
            ix = cols.index("_atom_site_fract_x"); iy = cols.index("_atom_site_fract_y"); iz = cols.index("_atom_site_fract_z")
            el = "".join(ch for ch in tok[isym] if ch.isalpha())
            sym.append(el); frac.append([float(tok[ix]), float(tok[iy]), float(tok[iz])])
        elif inloop and frac and (s == "" or s.startswith("loop_")):
            break
    return A, np.array(frac), sym


def bvse_map(A, frac, sym, n):
    # anisotropic grid ~uniform Å spacing: n = points along shortest axis
    L = np.linalg.norm(A, axis=1)
    ns = np.maximum(8, np.round(n * L / L.min()).astype(int))
    gx = [np.linspace(0, 1, ns[k], endpoint=False) for k in range(3)]
    GF = np.stack(np.meshgrid(*gx, indexing="ij"), axis=-1)   # (nx,ny,nz,3) fractional
    anA = [(frac[i], BV[s]) for i, s in enumerate(sym) if s in BV]
    bvs = np.zeros(GF.shape[:3])
    for af, (R0, bb) in anA:
        df = GF - af
        df -= np.round(df)                      # minimum image (fractional)
        d = np.linalg.norm(df @ A, axis=-1)      # cartesian distance
        bvs += np.exp((R0 - d) / bb)
    bvse = (bvs - V_IDEAL) ** 2
    return bvse, ns, L


def percolates(mask):
    """True if {mask} spans a full period along any axis (PBC percolation)."""
    for ax in range(3):
        N = mask.shape[ax]
        big = np.concatenate([mask, mask], axis=ax)     # 2x tile along ax
        lbl, nlab = ndimage.label(big)
        if nlab == 0:
            continue
        for k in range(1, nlab + 1):
            idx = np.where(lbl == k)[ax]
            if idx.size and (idx.max() - idx.min()) >= N:   # connects through one period
                return True
    return False


def perc_barrier(bvse, n_levels=60):
    """Min BVSE level (above global min) at which sub-threshold region percolates."""
    lo, hi = float(bvse.min()), float(np.percentile(bvse, 60))
    levels = np.linspace(lo, hi, n_levels)
    for E in levels:
        if percolates(bvse <= E):
            return float(E), float(E - lo)
    return None, None


def li_site_bvs(A, frac, sym):
    anA = [(frac[i], BV[s]) for i, s in enumerate(sym) if s in BV]
    out = []
    for i, s in enumerate(sym):
        if s != "Li":
            continue
        bvs = 0.0
        for af, (R0, bb) in anA:
            df = frac[i] - af; df -= np.round(df)
            d = np.linalg.norm(df @ A)
            bvs += math.exp((R0 - d) / bb)
        out.append(bvs)
    return out


def _selftest():
    """⛔ 음성 경로 포함 — 양성만 있는 selftest 는 통과해도 아무것도 보증 못 한다."""
    import tempfile, os
    ok = [0, 0]

    def chk(c, m):
        print(("  ✓ " if c else "  ✗ ") + m)
        ok[0 if c else 1] += 1

    def dies(fn, why):
        try:
            parse_structure(fn)
            chk(False, "[음성] %s → **죽어야 하는데 통과했다**" % why)
        except SystemExit:
            chk(True, "[음성] %s → 죽는다" % why)
        except Exception as ex:  # noqa: BLE001
            # 죽긴 했지만 계약(SystemExit)이 아니다 — 호출부가 못 잡는 형태다
            chk(False, "[음성] %s → %s 로 죽는다 (SystemExit 이어야 한다)" % (why, type(ex).__name__))

    d = tempfile.mkdtemp()

    def w(name, txt):
        q = os.path.join(d, name)
        open(q, "w").write(txt)
        return q

    CUBE = 'Lattice="10.0 0.0 0.0 0.0 10.0 0.0 0.0 0.0 10.0"'
    good = w("g.xyz", "2\n" + CUBE + " Properties=species:S:1:pos:R:3\nLi 5.0 5.0 5.0\nS 0.0 0.0 0.0\n")
    A, fr, sy = parse_structure(good)
    chk(abs(np.linalg.det(A) - 1000.0) < 1e-6, "[양성] 부피 1000 A^3 (얻은 %.3f)" % np.linalg.det(A))
    chk(sy == ["Li", "S"], "[양성] 원소 순서 보존 %s" % sy)
    chk(np.allclose(fr[0], [.5, .5, .5]) and np.allclose(fr[1], [0, 0, 0]),
        "[양성] 데카르트 -> 분율 변환")

    wrap = w("w.xyz", "1\n" + CUBE + "\nLi -2.0 12.0 5.0\n")
    _, fw, _ = parse_structure(wrap)
    chk(np.allclose(fw[0], [.8, .2, .5]), "[양성] 셀 밖 좌표를 셀 안으로 접는다 -> %s" % fw[0])

    # ⭐ 회전된 격자를 줘도 CIF 경로와 **같은 A** 가 나와야 한다.
    #    안 그러면 같은 셀인데 두 입력 형식이 다른 맵을 낸다 (조용히 틀린 경로).
    # ⛔ 2026-09-18 — 첫 판 fixture 는 **이미 CIF 관례 행렬**이라 `return L` 로 깨도
    #   통과했다. fixture 가 헛것이면 시험도 헛것이다. 그래서 (1) 진짜 회전 격자를 쓰고
    #   (2) **fixture 가 회전돼 있다는 것 자체를 먼저 시험한다**.
    ROT = ("5.5904485703 4.2127051621 0.0000000000 "
           "-0.5630624905 6.5629496561 2.3686815832 "
           "3.0197773438 1.8083606074 6.0506839867")
    Lraw = np.array([float(x) for x in ROT.split()]).reshape(3, 3)
    Ac = cell_matrix(7.0, 7.0, 7.0, 60.0, 60.0, 60.0)
    chk(not np.allclose(Lraw, Ac, atol=1e-6),
        "[전제] fixture 가 **실제로 회전돼 있다** (같으면 아래 시험이 아무것도 못 잰다)")
    chk(abs(abs(np.linalg.det(Lraw)) - abs(np.linalg.det(Ac))) < 1e-6,
        "[전제] 회전이라 부피는 같다")
    tri = w("t.xyz", '1\nLattice="' + ROT + '"\nLi 0.0 0.0 0.0\n')
    At, _, _ = parse_structure(tri)
    chk(np.allclose(At, Ac, atol=1e-6),
        "[양성] 회전된 격자를 CIF 관례로 되돌린다 (두 입력 형식이 같은 A 를 준다)")

    dies(w("nolat.xyz", "1\nno lattice here\nLi 0 0 0\n"), "Lattice= 없음")
    dies(w("short.xyz", "1\n" + CUBE + "\nLi 0 0\n"), "원자 줄이 3 열")
    dies(w("count.xyz", "3\n" + CUBE + "\nLi 0 0 0\n"), "첫 줄 3 인데 원자 1 개")
    dies(w("flat.xyz", '1\nLattice="10 0 0 0 10 0 0 0 0"\nLi 0 0 0\n'), "격자 부피 0")
    dies(w("nine.xyz", '1\nLattice="10 0 0 0 10 0"\nLi 0 0 0\n'), "Lattice 가 9 개가 아님")
    dies(w("bad.xyz", "not a number\n" + CUBE + "\nLi 0 0 0\n"), "첫 줄이 원자수가 아님")
    dies(w("x.poscar", "whatever\n"), "모르는 확장자 (.poscar)")

    print("selftest %s  (%d/%d)" % ("PASS" if ok[1] == 0 else "FAIL", ok[0], ok[0] + ok[1]))
    return ok[1] == 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("struct", nargs="?", help=".cif 또는 extxyz(.xyz, Lattice= 필수)")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--grid", type=int, default=28, help="points along shortest axis")
    ap.add_argument("--prefix", default="bvse")
    args = ap.parse_args()
    if args.selftest:
        raise SystemExit(0 if _selftest() else 1)
    if not args.struct:
        ap.error('struct 가 필요하다 (또는 --selftest)')

    A, frac, sym = parse_structure(args.struct)
    anions = sorted({s for s in sym if s in BV})
    print(f"struct={args.struct}  natoms={len(sym)}  anions={'+'.join(anions)}")
    bvse, ns, L = bvse_map(A, frac, sym, args.grid)
    print(f"cell |a||b||c| = {L[0]:.2f} {L[1]:.2f} {L[2]:.2f} A  grid={tuple(ns)}  ~{L.min()/args.grid:.3f} A/voxel")
    np.save(f"{args.prefix}_bvse_map.npy", bvse)

    Eperc, Ebar = perc_barrier(bvse)
    lis = li_site_bvs(A, frac, sym)
    summary = {
        "structure": args.struct, "n_atoms": len(sym), "anions": anions,
        "grid": [int(x) for x in ns], "voxel_A": round(L.min()/args.grid, 4),
        "bvse_min": round(float(bvse.min()), 5),
        "bvse_perc_level": round(Eperc, 5) if Eperc is not None else None,
        "Li_migration_barrier_BVSE": round(Ebar, 4) if Ebar is not None else None,
        "Li_site_BVS_mean": round(float(np.mean(lis)), 4) if lis else None,
        "Li_site_BVS_std": round(float(np.std(lis)), 4) if lis else None,
        "note": "BVSE barrier = percolation threshold above global min (valence^2 units). "
                "Empirical BVSE; calibrate scale vs comp1/modelc reference run, not absolute eV.",
    }
    json.dump(summary, open(f"{args.prefix}_bvse_summary.json", "w"), indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
