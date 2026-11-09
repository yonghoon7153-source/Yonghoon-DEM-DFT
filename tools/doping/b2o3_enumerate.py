#!/usr/bin/env python3
"""B2O3 doping of LPSCl1.6 (modelC) — Stage 0: Ewald joint pre-rank.

UPGRADED protocol (kb/methodology/b2o3_doping_chemistry.md §5.7).

B2O3 -> bare B3+ at P (4b tetrahedral, -2 acceptor) + O2- at S (16e, isovalent).
Charge compensation: fill existing Li vacancies (LPSCl1.6 has ~0.6 vac/fu).

KEY POINT — what Ewald can / cannot rank:
  charged DOF (Ewald-RIGOROUS)   : B@P (+3 vs +5), halogen S2-/Cl- on free 4a/4d,
                                   Li-fill (+1 vs vacancy 0), acceptor-vacancy assoc.
  isovalent DOF (Ewald-BLIND)    : O@S (both -2) -> O placement decided by COVALENCY,
                                   handled here as chemistry MOTIFS (BO4 / distributed /
                                   free-S) emitted per top config for UMA/DFT to rank.

This avoids the two failure modes of the old sequential-greedy method:
  (1) Li-ordering noise (1162 meV) contaminating a "1 representative Li" ranking,
  (2) greedy cut discarding coupled minima (B-O / acceptor-vacancy coupling).

Pipeline:
  1. supercell -> oxidation states -> site pools
  2. Li-vacancy candidate sites (spglib symmetry-completion; void-finder fallback)
  3. precompute geometric Ewald kernel M once (positions fixed across configs)
  4. random-sample {B sites, halogen pattern, Li-fill sites}; score E = q^T M q
  5. exact config-key dedup -> keep top-N by Ewald
  6. per top-K: emit O motifs (bo4 / distributed / free_s) -> UMA-ready CIFs + ranked.csv

Deps: ase, numpy, scipy (always).  spglib optional (better Li candidates).
Usage:
  python3 b2o3_enumerate.py --base db/structures/modelc_V0_k663.xyz \
      --supercell 1 1 2 --n_B 2 --n_O 3 --n_samples 80000 --top 300 \
      --o_motif_top 20 --out b2o3_stage0
"""
import argparse, json, itertools, hashlib
from pathlib import Path
import numpy as np
from ase.io import read, write
from ase.neighborlist import neighbor_list

KE = 14.399645351950543  # e^2/(4*pi*eps0) in eV*Angstrom
OXI = {"Li": +1, "P": +5, "B": +3, "Nd": +3, "S": -2, "O": -2, "Cl": -1, "VAC": 0}
HALOGENS = ("Cl", "Br", "I")


# ----------------------------------------------------------------------
# Rietveld (부분점유) CIF → 정수 조성 골격          (2026-09-07 신설)
# ----------------------------------------------------------------------
#   왜 여기인가: 이 도구가 이미 "도펀트³⁺@4b + O²⁻@16e + 할로겐 4a/4c + Li 충전" 을
#   Ewald 로 순위매긴다. 빠져 있던 것은 **입력이 정렬 구조여야 한다**는 것뿐이었다.
#   협업자 Rietveld 는 부분점유라 그대로 못 넣는다 → 여기서 정수화해 같은 파이프라인에 얹는다.
#
# ⛔ 이 경로가 **못 하는 것**
#   · 점유율을 "맞추지" 않는다. 자리 수가 모자라면 반올림이고, 그 편차를 report 에 적는다.
#     (4자리에서 0.85 와 0.75 는 둘 다 3 이 된다 — 실측 선호가 뭉개지는 것을 숨기지 않는다.)
#   · 도펀트 농도를 정련값으로 두지 않는다. n_B·n_O 로 **선언**하는 값이다.
#   · 원자를 이완하지 않는다. 격자도 안 건드린다 (Rietveld a 를 그대로 쓴다).
#   · 대칭 축약에 spglib 을 쓰지 않는다 — F-centered 를 fcc 벡터로 직접 내린다.
#     그 외 격자중심(I/C/R)은 지원하지 않고 **거부한다**(조용히 틀리는 것보다 낫다).

def primitive_fcc(atoms, tol=0.02):
    """면심(F) 관용셀 → 원시셀. spglib 없이 fcc 원시벡터로 직접 내린다."""
    C = atoms.cell.array
    M = np.array([[0.0, .5, .5], [.5, 0.0, .5], [.5, .5, 0.0]])
    P = M @ C
    inv = np.linalg.inv(P)
    seen, keep = [], []
    for i, r in enumerate(atoms.get_positions()):
        f = (r @ inv) % 1.0
        if not any(np.linalg.norm((f - u + .5) % 1.0 - .5) < tol for u in seen):
            seen.append(f)
            keep.append(i)
    out = atoms[keep]
    out.set_cell(P)
    out.set_scaled_positions(out.get_positions() @ inv % 1.0)
    return out


def _site_classes(cif_path):
    """CIF 의 자리 클래스 → (atoms, tag별 역할·점유율). ASE store_tags 를 쓴다."""
    a = read(str(cif_path), store_tags=True)
    occ = a.info.get("occupancy")
    kinds = a.arrays.get("spacegroup_kinds")
    if not occ or kinds is None:
        raise SystemExit(f"⛔ {cif_path}: 부분점유 정보가 없다 "
                         f"(occupancy/spacegroup_kinds). Rietveld CIF 가 맞나?")
    occ = {int(k): v for k, v in occ.items()}
    roles = {}
    for tag in sorted(set(int(t) for t in kinds)):
        o = occ.get(tag) or {}
        if not o:
            raise SystemExit(f"⛔ tag {tag} 에 점유율이 없다")
        major = max(o, key=o.get)
        if major == "Li":
            role = "li"
        elif major in HALOGENS:
            role = "free_anion"
        elif major == "S":
            role = "ps4S"
        elif OXI.get(major, 0) > 0:
            role = "cation4b"
        else:
            raise SystemExit(f"⛔ tag {tag} 의 대표 원소 {major} 를 어느 자리로 볼지 모른다 "
                             f"— 추측하지 않는다 (점유율 {o})")
        roles[tag] = (role, o)
    for need in ("li", "cation4b", "ps4S", "free_anion"):
        if not any(r == need for r, _ in roles.values()):
            raise SystemExit(f"⛔ 자리 역할 '{need}' 를 못 찾았다 — argyrodite CIF 가 맞나?")
    return a, roles


def base_from_rietveld(cif_path, supercell, n_dop, n_O, primitive=False):
    """부분점유 CIF → (골격 atoms · Li후보 좌표 · 목표조성 · report).

    골격에는 **Li 를 넣지 않는다** — Li 는 전량 Ewald 가 배치한다(호출자가 n_li_fill 로).
    """
    a0, roles = _site_classes(cif_path)
    if primitive:
        a0 = primitive_fcc(a0)
        kinds = a0.arrays["spacegroup_kinds"]
    a = a0 * tuple(supercell)
    kinds = np.asarray(a.arrays["spacegroup_kinds"], dtype=int)
    idx = {r: [] for r in ("li", "cation4b", "ps4S", "free_anion")}
    for i, t in enumerate(kinds):
        idx[roles[int(t)][0]].append(i)

    # 자유음이온: **tag 마다 따로 반올림** — 4c(0.85) 와 4a(0.75) 의 선호를 뭉개지 않는다
    cl_sites, freeS_sites, rep = [], [], []
    for tag, (role, o) in roles.items():
        if role != "free_anion":
            continue
        sites = [i for i in idx["free_anion"] if int(kinds[i]) == tag]
        pcl = sum(v for e, v in o.items() if e in HALOGENS)
        ncl = int(round(pcl * len(sites)))
        cl_sites += sites[:ncl]
        freeS_sites += sites[ncl:]
        rep.append({"tag": int(tag), "n_sites": len(sites), "occ_halide": round(pcl, 4),
                    "raw": round(pcl * len(sites), 3), "int": ncl,
                    "dev": round(ncl - pcl * len(sites), 3)})

    syms = list(a.get_chemical_symbols())
    for i in idx["cation4b"]:
        syms[i] = "P"
    for i in idx["ps4S"]:
        syms[i] = "S"
    for i in cl_sites:
        syms[i] = "Cl"
    for i in freeS_sites:
        syms[i] = "S"
    a.set_chemical_symbols(syms)
    li_pos = a.get_positions()[idx["li"]].copy()
    base = a[[i for i in range(len(a)) if i not in set(idx["li"])]]

    # ⛔⛔ 2026-09-07 실측 버그 — **정수화해 놓고 부분점유 꼬리표를 안 떼면 도로 부분점유가 된다.**
    #   ASE 의 CIF **라이터**는 `info["occupancy"]` + `arrays["spacegroup_kinds"]` 가 남아
    #   있으면 그걸 보고 혼합 자리를 **복원해서 써낸다**. 실제로 첫 판이
    #       Nd Nd1 1.0 0.5 0.5 0.5 0.0200
    #       P  P1  1.0 0.5 0.0 0.0 0.9800
    #   처럼 같은 자리에 두 원소를 적어, 되읽으면 P4·Nd4·O16 (전하 +6) 이 나왔다.
    #   **조용히 틀린 DFT 입력이 만들어지는 경로**라 여기서 확실히 끊는다.
    for _obj in (a, base):
        _obj.info.pop("occupancy", None)
        if "spacegroup_kinds" in _obj.arrays:
            del _obj.arrays["spacegroup_kinds"]

    # ── 목표 조성: 자리 수는 정확히, Li 는 **전하중성이 결정한다** ────────────
    n4b, n16e = len(idx["cation4b"]), len(idx["ps4S"])
    # ⛔ 자리보다 많은 도펀트를 조용히 받으면 nP 가 음수가 되고, 그 음수가 전하식에
    #   그대로 들어가 **말이 되는 것처럼 보이는 Li 개수**가 나온다 (2026-09-07 시험이 잡음).
    if not (0 <= n_dop <= n4b):
        raise SystemExit(f"⛔ 도펀트 {n_dop} 개가 4b 자리 {n4b} 개를 넘는다")
    if not (0 <= n_O <= n16e):
        raise SystemExit(f"⛔ O {n_O} 개가 16e 자리 {n16e} 개를 넘는다")
    nP, nNd = n4b - n_dop, n_dop
    nS = (n16e - n_O) + len(freeS_sites)
    nCl, nO = len(cl_sites), n_O
    nLi = 2 * nS + nCl + 2 * nO - 5 * nP - 3 * nNd
    if nLi < 0 or nLi > len(idx["li"]):
        raise SystemExit(f"⛔ 전하중성이 요구하는 Li {nLi} 개가 48h 자리 "
                         f"{len(idx['li'])} 개에 안 들어간다 — n_dop/n_O 를 줄여라")
    report = {"n_fu": n4b, "sites": {"4b": n4b, "16e": n16e,
                                     "free_anion": len(idx["free_anion"]),
                                     "48h": len(idx["li"])},
              "free_anion_rounding": rep,
              "target": {"Li": nLi, "P": nP, "dopant": nNd, "S": nS, "Cl": nCl, "O": nO},
              "n_atoms": nLi + nP + nNd + nS + nCl + nO,
              "charge": nLi + 5 * nP + 3 * nNd - 2 * nS - nCl - 2 * nO,
              "cell_A": [round(x, 5) for x in a.cell.cellpar()]}
    return base, li_pos, nLi, report


# ----------------------------------------------------------------------
# Ewald (neutral cell) — geometric kernel M s.t. E = q^T M q  (eV)
# ----------------------------------------------------------------------
def ewald_matrix(pos, cell, alpha=None, rcut=None, kcut=None):
    """Return N×N matrix M with E_ewald = sum_ij q_i q_j M_ij (neutral cell).

    E = ½ Σ_ij Σ_L' q_i q_j erfc(α|r_ij+L|)/|r_ij+L|                       (real)
      + (2π/V) Σ_{G≠0} e^{−G²/4α²}/G² |S(G)|² ,  S(G) = Σ_i q_i e^{iG·r_i}  (reciprocal)
      − (α/√π) Σ_i q_i²                                                     (self)

    ⛔ 2026-11-09 고침 (Codex DU P1-1 · 재현: α 만 바꿔도 −3.51 → −5.53 → −7.56 eV · 독립 합 −2.931):
      ① 역격자 항에 ½ 을 **두 번** 곱했다 — (2π/V) 가 이미 ½ · (4π/V) 다. 그래서 역격자 몫이 절반이었고
        에너지가 α 에 따라 움직였다 (수렴한 Ewald 합은 α 와 무관해야 한다).
      ② (예방) 이미지 범위를 격자 벡터 길이 대신 수직폭으로 · 차 벡터를 분율 [−½, ½) 로 감싼다 · 역격자 범위를
        2π/|a_i| 로 — 기운 셀에서 이론상 컷오프 안 이미지를 빠뜨릴 수 있었다. ⚠ 깨기로 재 보니 정밀도 계수 3.6 에서
        옛 범위의 차이는 10⁻⁶ 상대 이하라 시험이 못 잡는다 (M2–M4 초록) — 실제로 값이 틀렸던 것은 ① 하나다.
      ③ 정밀도 계수 3.2 → 3.6 (3.2 의 역격자 절단 ≈ 3.6e-5 상대 · 기운 원시셀 Madelung 3.0e-5 어긋남).
      selftest: Madelung 상수 (NaCl · CsCl · 외부 기준) · 기운 원시셀 · 길쭉 기운 셀 · α 불변 (modelc 꼴 포함) ·
      전하 0 자리 불변 · 슈퍼셀 가산 — 깨기 M1 (½ 이중 되살림) → 8 빨강.
    ⛔ 이 함수가 못 하는 것: 전하가 0 이 아닌 셀의 배경 보정 (호출부가 중성을 보장해야 한다 — 검사 안 함).
    """
    pos = np.asarray(pos, float); cell = np.asarray(cell, float)
    N = len(pos); V = abs(np.linalg.det(cell))
    if alpha is None:
        alpha = (N * np.pi**3 / V**2) ** (1.0 / 6.0)  # standard heuristic
    ACC = 3.6   # erfc(3.6) ≈ 3.6e-7 · exp(−3.6²) ≈ 2.4e-6 — 2026-11-09 3.2 → 3.6 (3.2 는 역격자 절단 ≈ 3.6e-5 상대오차)
    if rcut is None:
        rcut = ACC / alpha
    if kcut is None:
        kcut = 2.0 * alpha * ACC
    inv = np.linalg.inv(cell)
    recip = 2 * np.pi * inv.T
    lens = np.linalg.norm(cell, axis=1)
    widths = np.array([V / np.linalg.norm(np.cross(cell[(i + 1) % 3], cell[(i + 2) % 3]))
                       for i in range(3)])

    # --- real space (differences wrapped to fractional [-1/2, 1/2) → every image within rcut
    #     has |n_i| <= rcut/w_i + 1/2 along each lattice direction) ---
    nmax = np.ceil(rcut / widths + 0.5).astype(int)
    shifts = np.array(list(itertools.product(
        range(-nmax[0], nmax[0] + 1), range(-nmax[1], nmax[1] + 1),
        range(-nmax[2], nmax[2] + 1))))
    Lvecs = shifts @ cell
    M = np.zeros((N, N))
    from scipy.special import erfc
    dij = pos[:, None, :] - pos[None, :, :]              # N,N,3
    f = dij @ inv
    f -= np.round(f)
    dij = f @ cell
    for L in Lvecs:
        r = np.linalg.norm(dij + L, axis=2)              # N,N
        zero = r < 1e-8
        r[zero] = 1.0
        contrib = erfc(alpha * r) / r
        contrib[zero] = 0.0
        M += 0.5 * contrib                                # 0.5: each pair counted twice over i,j
    # --- reciprocal (reciprocal-cell plane spacing along b_i is 2π/|a_i|) ---
    kmax = np.ceil(kcut * lens / (2 * np.pi)).astype(int)
    ks = np.array(list(itertools.product(
        range(-kmax[0], kmax[0] + 1), range(-kmax[1], kmax[1] + 1),
        range(-kmax[2], kmax[2] + 1))))
    ks = ks[np.any(ks != 0, axis=1)]
    G = ks @ recip
    G2 = np.einsum("ij,ij->i", G, G)
    keep = G2 < kcut**2
    G, G2 = G[keep], G2[keep]
    pref = (2 * np.pi / V) * np.exp(-G2 / (4 * alpha**2)) / G2   # = ½·(4π/V): the ½ is already here
    arg = pos @ G.T                                       # N,K
    C, S = np.cos(arg), np.sin(arg)
    M += (C * pref) @ C.T + (S * pref) @ S.T              # Σ_G pref cos(G·(r_i − r_j))
    # --- self term (diagonal) ---
    M[np.diag_indices(N)] -= alpha / np.sqrt(np.pi)
    return KE * M


def ewald_energy(M, q):
    return float(q @ M @ q)


# ----------------------------------------------------------------------
# site pools
# ----------------------------------------------------------------------
def site_pools(atoms):
    s = atoms.get_chemical_symbols()
    ii, jj = neighbor_list("ij", atoms, {("P", "S"): 2.4})
    ps4 = set()
    for a, b in zip(ii, jj):
        if s[a] == "S": ps4.add(a)
        if s[b] == "S": ps4.add(b)
    P = [i for i in range(len(atoms)) if s[i] == "P"]
    Cl = [i for i in range(len(atoms)) if s[i] == "Cl"]
    freeS = [i for i in range(len(atoms)) if s[i] == "S" and i not in ps4]
    ps4S = sorted(ps4)
    return dict(P=P, Cl=Cl, freeS=freeS, ps4S=ps4S,
                free_anion=sorted(freeS + Cl))  # 4a/4d pool


# ----------------------------------------------------------------------
# Li-vacancy candidate sites
# ----------------------------------------------------------------------
def li_vacancy_candidates(atoms, n_need, min_anion=2.3, max_anion=2.95,
                          min_cation=1.7, grid=0.4):
    """spglib symmetry-completion of the Li sublattice; void-finder fallback."""
    s = atoms.get_chemical_symbols()
    occ_Li = atoms.get_positions()[[i for i in range(len(atoms)) if s[i] == "Li"]]
    cell = atoms.cell.array
    # --- try spglib symmetry completion ---
    try:
        import spglib
        num = atoms.get_atomic_numbers()
        spg = (cell, atoms.get_scaled_positions(), num)
        sym = spglib.get_symmetry(spg, symprec=0.3)
        if sym is not None:
            frac = atoms.get_scaled_positions()
            li_frac = frac[[i for i in range(len(atoms)) if s[i] == "Li"]]
            gen = []
            for R, t in zip(sym["rotations"], sym["translations"]):
                gen.append((li_frac @ R.T + t) % 1.0)
            gen = np.vstack(gen)
            # dedup
            uniq = []
            for f in gen:
                if not any(np.linalg.norm(((f - u + 0.5) % 1.0 - 0.5)) < 0.05 for u in uniq):
                    uniq.append(f)
            uniq = np.array(uniq)
            cart = uniq @ cell
            # vacancy = not near an occupied Li
            cand = [c for c in cart if min_dist(c, occ_Li, cell) > 0.6]
            cand = dedup_cart(cand, cell, 0.6)
            if len(cand) >= n_need:
                return np.array(cand), "spglib_symmetry"
    except Exception:
        pass
    # --- void-finder fallback (grid pockets with REAL Li coordination) ---
    # require Li-like environment: nearest anion in bond range AND >=3 anions
    # coordinating (within 3.25 A) -> rejects surface/over-large pockets that the
    # loose criterion over-generates.
    anion = atoms.get_positions()[[i for i in range(len(atoms)) if s[i] in ("S", "Cl", "O")]]
    cation = atoms.get_positions()[[i for i in range(len(atoms)) if s[i] in ("Li", "P", "B", "Nd")]]
    na = (np.linalg.norm(cell, axis=1) / grid).astype(int)
    gx = np.linspace(0, 1, na[0], endpoint=False)
    gy = np.linspace(0, 1, na[1], endpoint=False)
    gz = np.linspace(0, 1, na[2], endpoint=False)
    gf = np.array(np.meshgrid(gx, gy, gz)).reshape(3, -1).T
    gc = gf @ cell
    inv = np.linalg.inv(cell)
    keep, score = [], []
    for p in gc:
        da_all = anion_dists(p, anion, inv, cell)
        da = da_all.min()
        ncoord = int((da_all < 3.25).sum())
        if min_anion < da < max_anion and ncoord >= 3 and min_dist(p, cation, cell) > min_cation:
            keep.append(p); score.append(ncoord)
    # dedup keeping higher-coordination representative
    order = np.argsort(score)[::-1]
    cand = dedup_cart([keep[i] for i in order], cell, 1.2)
    cand = [c for c in cand if min_dist(c, occ_Li, cell) > 0.9]
    return np.array(cand), "void_finder"


def anion_dists(p, pts, inv, cell):
    d = p[None, :] - pts
    f = (d @ inv + 0.5) % 1.0 - 0.5
    return np.linalg.norm(f @ cell, axis=1)


def min_dist(p, pts, cell):
    if len(pts) == 0:
        return 1e9
    d = p[None, :] - pts
    inv = np.linalg.inv(cell)
    f = (d @ inv + 0.5) % 1.0 - 0.5
    return float(np.linalg.norm(f @ cell, axis=1).min())


def dedup_cart(pts, cell, tol):
    out = []
    for p in pts:
        if not any(min_dist(p, np.array([u]), cell) < tol for u in out):
            out.append(p)
    return out


# ----------------------------------------------------------------------
# main
# ----------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", help="정렬된 구조 (xyz/cif). --rietveld_cif 와 택일")
    ap.add_argument("--rietveld_cif", help="부분점유 Rietveld CIF — 여기서 정수화한다")
    ap.add_argument("--primitive", action="store_true",
                    help="관용 F 셀을 원시셀로 내린 뒤 --supercell 적용 (5 f.u. 같은 배수용)")
    ap.add_argument("--dopant", default="B", help="4b 에 넣을 +3 억셉터 (B·Nd·…)")
    ap.add_argument("--n_li_fill", type=int, default=None,
                    help="Ewald 가 놓을 Li 개수. 기본 2×n_B(보상분만). rietveld 경로에서는 전량이 자동 계산된다")
    ap.add_argument("--supercell", nargs=3, type=int, default=[1, 1, 2])
    ap.add_argument("--n_B", type=int, default=2)
    ap.add_argument("--n_O", type=int, default=3)
    ap.add_argument("--n_samples", type=int, default=80000)
    ap.add_argument("--top", type=int, default=300)
    ap.add_argument("--o_motif_top", type=int, default=20)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default="b2o3_stage0")
    A = ap.parse_args()
    rng = np.random.default_rng(A.seed)
    out = Path(A.out); (out / "cif").mkdir(parents=True, exist_ok=True)

    DOP = A.dopant
    if DOP not in OXI:
        raise SystemExit(f"⛔ 도펀트 {DOP} 의 산화수를 모른다 — OXI 에 추가하고 오라 "
                         f"(추측하지 않는다). 아는 것: {sorted(OXI)}")
    if OXI[DOP] != +3:
        raise SystemExit(f"⛔ 이 파이프라인은 **+3 억셉터@4b** 전용이다 "
                         f"({DOP} 는 {OXI[DOP]:+d}). Li 보상 수(2×n)가 안 맞는다.")

    if A.rietveld_cif:
        # 부분점유 CIF 를 정수화해 골격을 만든다. Li 는 골격에 없고 **전량** Ewald 가 놓는다.
        base, licand, n_Li_fill, rep = base_from_rietveld(
            A.rietveld_cif, A.supercell, A.n_B, A.n_O, primitive=A.primitive)
        (out / "integerization.json").write_text(
            json.dumps(rep, ensure_ascii=False, indent=1) + "\n")
        print(f"Rietveld 정수화: {rep['n_fu']} f.u. · 목표 {rep['target']} "
              f"· 총 {rep['n_atoms']}원자 · 전하 {rep['charge']:+d}")
        for r in rep["free_anion_rounding"]:
            print(f"   자유음이온 tag{r['tag']}: {r['n_sites']}자리 × {r['occ_halide']} "
                  f"= {r['raw']} → {r['int']} (편차 {r['dev']:+.2f})")
        src = "rietveld_cif(48h 자리 정본)"
    else:
        base = read(A.base) * tuple(A.supercell)
        n_Li_fill = A.n_li_fill if A.n_li_fill else 2 * A.n_B   # P5+ -> M3+ = -2 each
        licand, src = li_vacancy_candidates(base, n_Li_fill)
    if A.n_li_fill:
        n_Li_fill = A.n_li_fill
    pools = site_pools(base)
    n_freeS = len(pools["freeS"])             # keep same free-S count (halogen reshuffle)
    print(f"supercell {A.supercell}  nat {len(base)}  pools: P {len(pools['P'])} "
          f"free_anion {len(pools['free_anion'])} (freeS {n_freeS}) ps4S {len(pools['ps4S'])}")
    print(f"doping: {A.n_B} {DOP}@P, {A.n_O} O@S, {n_Li_fill} Li 배치")
    print(f"Li 후보 자리: {len(licand)} ({src})")
    if len(licand) < n_Li_fill:
        raise SystemExit(f"need >= {n_Li_fill} Li candidates, got {len(licand)} — "
                         f"pass an ideal Li template or loosen void params")

    # --- master position list: framework + Li-occupied + Li-candidate ---
    s0 = base.get_chemical_symbols()
    fw_idx = [i for i in range(len(base)) if s0[i] != "Li"]   # P/S/Cl positions (fixed)
    li_occ_idx = [i for i in range(len(base)) if s0[i] == "Li"]
    pos = np.vstack([base.get_positions()[fw_idx],
                     base.get_positions()[li_occ_idx],
                     licand])
    cell = base.cell.array
    # index maps into master list
    fw_of = {old: k for k, old in enumerate(fw_idx)}
    nfw = len(fw_idx); nliocc = len(li_occ_idx)
    licand_master = list(range(nfw + nliocc, nfw + nliocc + len(licand)))
    liocc_master = list(range(nfw, nfw + nliocc))

    print("precomputing Ewald kernel ...", flush=True)
    M = ewald_matrix(pos, cell)

    # base charge vector (no doping): framework species + occupied Li(+1) + candidates(0)
    q0 = np.zeros(len(pos))
    for old in fw_idx:
        q0[fw_of[old]] = OXI[s0[old]]
    for m in liocc_master:
        q0[m] = OXI["Li"]
    # candidates start as vacancy (0)
    P_master = [fw_of[i] for i in pools["P"]]
    freeanion_master = [fw_of[i] for i in pools["free_anion"]]
    # halogen counts to preserve: n_freeS S(-2), rest Cl(-1)
    n_free = len(freeanion_master)

    # Deterministic: enumerate B (C(nP,n_B)) × halogen (C(n_free, n_freeS));
    # for each, place n_Li_fill Li GREEDILY at the lowest-marginal-energy candidate
    # sites (acceptor-vacancy association + Li-Li repulsion captured exactly).
    Mdiag = np.diag(M)
    cand_arr = np.array(licand_master)
    B_combos = list(itertools.combinations(range(len(P_master)), A.n_B))
    H_combos = list(itertools.combinations(range(n_free), n_freeS))
    n_total = len(B_combos) * len(H_combos)
    print(f"enumerating {len(B_combos)} B × {len(H_combos)} halogen = {n_total} base "
          f"configs, greedy-Li each ...", flush=True)
    if A.n_samples and n_total > A.n_samples:
        # subsample halogen patterns if the product is too large (keeps all B)
        keep = max(1, A.n_samples // len(B_combos))
        idx = rng.choice(len(H_combos), min(keep, len(H_combos)), replace=False)
        H_combos = [H_combos[i] for i in idx]
        print(f"  halogen subsampled to {len(H_combos)} (n_samples cap {A.n_samples})")

    seen = {}
    done = 0
    for bsel in B_combos:
        for Hsel in H_combos:
            q = q0.copy()
            for b in bsel:
                q[P_master[b]] = OXI[DOP]
            Hset = set(Hsel)
            for k, m in enumerate(freeanion_master):
                q[m] = OXI["S"] if k in Hset else OXI["Cl"]
            # greedy Li fill
            placed = []
            for _ in range(n_Li_fill):
                marg = Mdiag[cand_arr] + 2.0 * (M[cand_arr] @ q)   # ΔE to add +1 at cand
                for p in placed:
                    marg[p] = np.inf
                c = int(np.argmin(marg))
                q[cand_arr[c]] = OXI["Li"]
                placed.append(c)
            key = (tuple(sorted(int(P_master[b]) for b in bsel)),
                   tuple(sorted(int(freeanion_master[k]) for k in Hsel)),
                   tuple(sorted(int(cand_arr[p]) for p in placed)))
            if key not in seen:
                seen[key] = ewald_energy(M, q)
            done += 1
            if done % 20000 == 0:
                print(f"  {done}/{n_total} ...", flush=True)

    ranked = sorted(seen.items(), key=lambda kv: kv[1])
    print(f"unique configs {len(ranked)}; lowest Ewald {ranked[0][1]:.3f} eV, "
          f"highest {ranked[-1][1]:.3f} eV, span {ranked[-1][1]-ranked[0][1]:.3f} eV")

    # --- write top-N (B/halogen/Li only; S not yet O) + O motifs for top-K ---
    rows = []
    for rank, (key, E) in enumerate(ranked[:A.top]):
        bpos, sfree, lifill = key
        st = build_struct(base, fw_idx, li_occ_idx, licand, pos, cell,
                          bpos, sfree, lifill, pools, o_sites=None, dopant=DOP)
        name = f"cfg{rank:04d}_E{E:.3f}"
        write(out / "cif" / f"{name}.cif", st)
        rows.append(dict(rank=rank, ewald_eV=round(E, 4), name=name,
                         B_sites=list(bpos), n_Li_fill=len(lifill)))
        # O motifs for the very top configs (UMA-ready full B2O3 structures)
        if rank < A.o_motif_top:
            for motif in ("bo4", "distributed", "free_s"):
                o_sites = pick_o_sites(base, bpos, pools, A.n_O, motif, rng, fw_idx)
                if o_sites is None:
                    continue
                st_o = build_struct(base, fw_idx, li_occ_idx, licand, pos, cell,
                                    bpos, sfree, lifill, pools, o_sites=o_sites, dopant=DOP)
                write(out / "cif" / f"{name}_O-{motif}.cif", st_o)

    json.dump(rows, open(out / "stage0_ranked.json", "w"), indent=2)
    with open(out / "stage0_ranked.csv", "w") as f:
        f.write("rank,ewald_eV,name,n_B,n_Li_fill\n")
        for r in rows:
            f.write(f"{r['rank']},{r['ewald_eV']},{r['name']},{len(r['B_sites'])},{r['n_Li_fill']}\n")
    print(f"\nwrote top {len(rows)} -> {out}/cif/  (+ O motifs for top {A.o_motif_top})")
    print(f"ranked: {out}/stage0_ranked.csv|json")
    print("NEXT: Stage 1 = UMA relax these (esp. the *_O-{bo4,distributed,free_s}.cif "
          "variants decide O placement by covalency).")


def pick_o_sites(base, bpos, pools, n_O, motif, rng, fw_idx):
    """Choose n_O sulfur sites (in original-index space) for O substitution."""
    s = base.get_chemical_symbols()
    # B-tetrahedron corner S: PS4-S bonded to a B-substituted P
    bP_orig = [fw_idx[b] if False else None for b in bpos]  # placeholder
    # map master P index back to original atom index
    P_orig = pools["P"]
    fwinv = {fw_idx.index(i): i for i in fw_idx}  # not used; keep simple
    # bpos are master indices into framework; recover original P atom indices
    b_orig = [fw_idx[mb] for mb in bpos]
    from ase.neighborlist import neighbor_list
    ii, jj = neighbor_list("ij", base, {("P", "S"): 2.4})
    corner_of = {p: [] for p in b_orig}
    for a, b in zip(ii, jj):
        if a in corner_of and s[b] == "S": corner_of[a].append(b)
        if b in corner_of and s[a] == "S": corner_of[b].append(a)
    b_corners = sorted({c for v in corner_of.values() for c in v})
    if motif == "bo4":
        pool = b_corners
    elif motif == "free_s":
        pool = pools["freeS"]
    else:  # distributed: PS4-S not on B
        pool = [i for i in pools["ps4S"] if i not in set(b_corners)]
    if len(pool) < n_O:
        pool = pools["ps4S"]
    if len(pool) < n_O:
        return None
    return sorted(rng.choice(pool, n_O, replace=False).tolist())


def build_struct(base, fw_idx, li_occ_idx, licand, pos, cell,
                 bpos, sfree, lifill, pools, o_sites, dopant="B"):
    """Assemble ASE Atoms for a given config (bpos/sfree/lifill are master indices)."""
    from ase import Atoms
    s = list(base.get_chemical_symbols())
    new = base.copy()
    syms = list(new.get_chemical_symbols())
    # B@P
    for mb in bpos:
        syms[fw_idx[mb]] = dopant
    # halogen: set free-anion sites
    nfw = len(fw_idx)
    # sfree are master indices in framework space -> original
    sset = set(fw_idx[m] for m in sfree)
    for orig in pools["free_anion"]:
        syms[orig] = "S" if orig in sset else "Cl"
    # O@S
    if o_sites:
        for o in o_sites:
            syms[o] = "O"
    new.set_chemical_symbols(syms)
    # add filled Li
    li_master0 = nfw + len(li_occ_idx)
    from ase import Atom
    for ml in lifill:
        p = pos[ml]
        new.append(Atom("Li", position=p))
    return new


def _selftest():
    """Rietveld 경로 자체시험. **음성 경로 위주** — 양성만 있는 시험은 아무것도 보증 못 한다."""
    import tempfile
    from ase import Atoms
    bad = []
    _checks = []

    def chk(cond, msg):
        _checks.append(msg)
        print(("  ✓ " if cond else "  ✗ ") + msg)
        if not cond:
            bad.append(msg)

    CIF = """data_t
_cell_length_a 9.79770
_cell_length_b 9.79770
_cell_length_c 9.79770
_cell_angle_alpha 90
_cell_angle_beta 90
_cell_angle_gamma 90
_space_group_name_H-M_alt "F -4 3 m"
_symmetry_Int_Tables_number 216
loop_
 _atom_site_label
 _atom_site_type_symbol
 _atom_site_fract_x
 _atom_site_fract_y
 _atom_site_fract_z
 _atom_site_occupancy
s1 Li 0.1626 0.1626 0.0153 0.4533
s2 P  0.5 0.5 0.5 0.98
s2b Nd 0.5 0.5 0.5 0.02
s3 S  0.6235 0.6235 0.6235 0.9925
s3b O  0.6235 0.6235 0.6235 0.0075
s4 Cl 0.25 0.25 0.25 0.85
s4b S  0.25 0.25 0.25 0.15
s5 Cl 0.0 0.0 0.0 0.75
s5b S  0.0 0.0 0.0 0.25
"""
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "t.cif"
        p.write_text(CIF)

        base, li, nLi, rep = base_from_rietveld(p, (1, 1, 1), n_dop=2, n_O=3)
        chk(rep["charge"] == 0, "[양성] 전하중성이 정확히 0")
        chk(rep["n_atoms"] == 54 and nLi == 26,
            f"[양성] 4 f.u. → 54원자 · Li 26 (실제 {rep['n_atoms']}/{nLi})")
        chk(len(li) == 48, f"[양성] 48h 자리를 전부 Li 후보로 준다 (실제 {len(li)})")

        # ⛔음성 ★ 이 버그가 실제로 났다 (2026-09-07): 정수화 후 부분점유 꼬리표가 남으면
        #   ASE CIF 라이터가 혼합 자리를 복원해 써낸다 → 되읽으면 조성·전하가 깨진다.
        chk("occupancy" not in base.info and "spacegroup_kinds" not in base.arrays,
            "⛔음성: 골격에 부분점유 꼬리표가 남지 않는다 (남으면 CIF 로 왕복하며 되살아난다)")
        rt = Path(td) / "rt.cif"
        write(rt, base)
        back = read(rt)
        chk(len(back) == len(base) and
            sorted(back.get_chemical_symbols()) == sorted(base.get_chemical_symbols()),
            "⛔음성: **CIF 로 쓰고 되읽어도 조성이 그대로다** (왕복 시험 — 위 버그의 관문)")

        # ⛔음성: 원시 축약이 실제로 자리 수를 1/4 로 줄이는가 (안 줄면 F 중심을 못 읽은 것)
        b5, li5, nLi5, rep5 = base_from_rietveld(p, (1, 1, 5), 2, 3, primitive=True)
        chk(rep5["n_fu"] == 5 and rep5["n_atoms"] == 66,
            f"[양성] 원시×5 → 5 f.u. · 66원자 (실제 {rep5['n_fu']}/{rep5['n_atoms']})")
        chk(abs(b5.cell.cellpar()[0] - 9.79770 / (2 ** 0.5)) < 1e-3,
            "⛔음성: 원시 격자상수가 a/√2 다 (관용셀 그대로면 F 중심을 안 내린 것)")

        # ⛔음성: 자유음이온을 tag 마다 따로 반올림하는가 (한 통에 몰면 4c 선호가 사라진다)
        chk(len(rep["free_anion_rounding"]) == 2,
            "⛔음성: 자유음이온 tag 를 합치지 않고 **따로** 반올림한다 (4a·4c 두 줄)")

        # ⛔음성: 전하중성이 48h 자리 수를 넘으면 조용히 넘어가지 않는다
        try:
            base_from_rietveld(p, (1, 1, 1), n_dop=5, n_O=3)   # 4b 자리는 4개뿐
            ok = False
        except SystemExit:
            ok = True
        chk(ok, "⛔음성: **자리보다 많은 도펀트**를 SystemExit 로 막는다 "
            "(안 막으면 nP 가 음수가 되어 그럴듯한 Li 개수가 나온다)")

        # ⛔음성: 점유율 정보가 없는 평범한 CIF 는 거부한다
        plain = Path(td) / "plain.cif"
        write(plain, Atoms("LiCl", positions=[[0, 0, 0], [2, 0, 0]], cell=[6, 6, 6], pbc=True))
        try:
            base_from_rietveld(plain, (1, 1, 1), 2, 3)
            ok = False
        except SystemExit:
            ok = True
        chk(ok, "⛔음성: 부분점유가 없는 CIF 를 Rietveld 로 받아주지 않는다")

    # ------------------------------------------------------------------
    # Ewald (2026-11-09 · Codex DU P1-1) — 외부 기준 (Madelung 상수) · α 불변 · 전하 0 자리 · 슈퍼셀
    # ⛔ 이 시험들은 역격자 ½ 이중 · 기운 셀 이미지 누락을 되살리면 빨개져야 한다 (깨기로 확인).
    # ------------------------------------------------------------------
    M_NACL, M_CSCL = 1.74756459463, 1.76267477307
    a = 5.64
    nacl_c = np.array([[0, 0, 0], [0, .5, .5], [.5, 0, .5], [.5, .5, 0],
                       [.5, 0, 0], [0, .5, 0], [0, 0, .5], [.5, .5, .5]]) * a
    q_c = np.array([1, 1, 1, 1, -1, -1, -1, -1], float)
    E = ewald_energy(ewald_matrix(nacl_c, np.eye(3) * a), q_c)
    ref = -4 * KE * M_NACL / (a / 2)
    chk(abs(E / ref - 1) < 2e-5, f"[외부 기준] NaCl 관용셀 Madelung (상대오차 {abs(E / ref - 1):.1e})")
    prim = np.array([[0, a / 2, a / 2], [a / 2, 0, a / 2], [a / 2, a / 2, 0]])
    nacl_p = np.array([[0, 0, 0], [a / 2, a / 2, a / 2]])
    q_p = np.array([1.0, -1.0])
    Ep = ewald_energy(ewald_matrix(nacl_p, prim), q_p)
    refp = -KE * M_NACL / (a / 2)
    chk(abs(Ep / refp - 1) < 2e-5,
        f"⛔음성: **기운 원시셀 (60°)** NaCl 도 같은 Madelung (상대오차 {abs(Ep / refp - 1):.1e})")
    acs = 4.12
    Ecs = ewald_energy(ewald_matrix(np.array([[0, 0, 0], [acs / 2] * 3]), np.eye(3) * acs), q_p)
    refcs = -KE * M_CSCL / (acs * np.sqrt(3) / 2)
    chk(abs(Ecs / refcs - 1) < 2e-5, f"[외부 기준] CsCl Madelung (상대오차 {abs(Ecs / refcs - 1):.1e})")
    N = len(nacl_p); V = abs(np.linalg.det(prim))
    a0 = (N * np.pi**3 / V**2) ** (1.0 / 6.0)
    Es = [ewald_energy(ewald_matrix(nacl_p, prim, alpha=a0 * s), q_p) for s in (0.6, 1.0, 1.6)]
    spread = (max(Es) - min(Es)) / abs(np.mean(Es))
    chk(spread < 1e-5, f"⛔음성: **α 를 0.6–1.6 배로 바꿔도 같은 에너지** (상대 퍼짐 {spread:.1e}) — 역격자 ½ 이중이면 α 따라 움직인다")
    rng0 = np.random.default_rng(7)
    ghost = rng0.random((3, 3)) @ prim
    Eg = ewald_energy(ewald_matrix(np.vstack([nacl_p, ghost]), prim), np.concatenate([q_p, np.zeros(3)]))
    chk(abs(Eg / Ep - 1) < 1e-5, f"⛔음성: 전하 0 자리 (Li 후보) 를 더해도 에너지 그대로 (상대 {abs(Eg / Ep - 1):.1e})")
    sc = (2, 1, 3)
    shifts = np.array(list(itertools.product(*[range(n) for n in sc]))) @ prim
    pos_sc = np.vstack([nacl_p + s for s in shifts])
    q_sc = np.tile(q_p, len(shifts))
    E_sc = ewald_energy(ewald_matrix(pos_sc, np.diag(sc) @ prim), q_sc)
    chk(abs(E_sc / (len(shifts) * Ep) - 1) < 2e-5,
        f"[양성] 슈퍼셀 2×1×3 = 원시 × 6 (상대 {abs(E_sc / (len(shifts) * Ep) - 1):.1e})")

    # 길쭉하고 기운 셀 (우리 셀 꼴 — modelc 원시 1×1×5 는 7.0 × 7.0 × 35.0 Å · 60°) — 작은 원시셀은
    #   이미지 범위 · 감싸기 · 역격자 범위 구멍을 못 건드린다 (깨기 M2–M4 가 첫 판 시험에서 초록이었다).
    long = np.diag([1, 1, 5]) @ prim
    pos_l = np.vstack([nacl_p + k * prim[2] for k in range(5)])
    E_l = ewald_energy(ewald_matrix(pos_l, long), np.tile(q_p, 5))
    chk(abs(E_l / (5 * Ep) - 1) < 1e-5,
        f"⛔음성: **길쭉 · 기운 셀** (원시 × (1,1,5)) = 원시 × 5 (상대 {abs(E_l / (5 * Ep) - 1):.1e})")
    mc = np.array([[7.01, 0, 0], [3.505, 6.0709, 0], [3.505, 2.0236, 28.6122 * 35.04 / 35.04]])
    mc[2] = mc[2] / np.linalg.norm(mc[2]) * 35.04
    rng1 = np.random.default_rng(11)
    pos_r = rng1.random((24, 3)) @ mc
    q_r = np.array([1.0, -1.0] * 12)
    N_r = len(pos_r); V_r = abs(np.linalg.det(mc)); a_r = (N_r * np.pi**3 / V_r**2) ** (1.0 / 6.0)
    Er = [ewald_energy(ewald_matrix(pos_r, mc, alpha=a_r * s), q_r) for s in (0.6, 1.0, 1.6)]
    sp_r = (max(Er) - min(Er)) / abs(np.mean(Er))
    chk(sp_r < 1e-5, f"⛔음성: modelc 꼴 (7 × 7 × 35 Å · 60°) 무작위 중성 전하에서 α 불변 (상대 퍼짐 {sp_r:.1e})")

    n_all = len(_checks)
    print(f"selftest {'PASS' if not bad else 'FAIL'} — {n_all - len(bad)}/{n_all} ok")
    return 1 if bad else 0


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    main()
